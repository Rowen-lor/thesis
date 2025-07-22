import argparse
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import sacrebleu
from comet import download_model, load_from_checkpoint

def load_data(filepath):
    """
    从JSONL文件中加载数据。

    Args:
        filepath (str): JSONL文件的路径。

    Returns:
        tuple: 包含三个列表的元组 (sources, hypotheses, references)。
    """
    sources, hypotheses, references = [], [], []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    sources.append(data['src'])
                    hypotheses.append(data['hyp'])
                    references.append(data['ref'])
                except json.JSONDecodeError:
                    print(f"警告: 跳过无效的JSON行: {line.strip()}")
                    continue
                except KeyError as e:
                    print(f"警告: 跳过缺少键的行 {e}: {line.strip()}")
                    continue
    except FileNotFoundError:
        print(f"错误: 输入文件未找到于 '{filepath}'")
        exit(1)
    return sources, hypotheses, references

def calculate_bleu(hypotheses, references):
    """
    计算BLEU分数。

    Args:
        hypotheses (list): 机器翻译的输出列表。
        references (list): 参考译文的列表（每个元素本身就是一个列表）。

    Returns:
        float: BLEU分数。
    """
    # sacrebleu期望每个假设有多个引用，因此引用的格式应为[[ref1_for_sent1, ref2_for_sent1], [ref1_for_sent2], ...]
    # 但我们的结构是 [[ref1_sent1, ref1_sent2], [ref2_sent1, ref2_sent2]]
    # 我们需要将其转置为 sacrebleu 的格式
    max_refs = max(len(r) for r in references)
    refs_transposed = [[] for _ in range(max_refs)]
    for ref_group in references:
        for i in range(max_refs):
            refs_transposed[i].append(ref_group[i] if i < len(ref_group) else "")

    bleu = sacrebleu.corpus_bleu(hypotheses, refs_transposed)
    return bleu.score

def calculate_comet(sources, hypotheses, references, model_path):
    """
    计算COMET分数。

    Args:
        sources (list): 源句子列表。
        hypotheses (list): 机器翻译的输出列表。
        references (list): 参考译文的列表。
        model_path (str): COMET模型的路径或名称。

    Returns:
        float: COMET分数。
    """
    print("开始下载和加载COMET模型...")
    try:
        model_path = download_model(model_path)
        print(f"模型已下载至: {model_path}")
        print("准备从checkpoint加载模型...")
        model = load_from_checkpoint(model_path)
        print("COMET模型加载成功。")
    except Exception as e:
        print(f"错误: 加载COMET模型失败 '{model_path}'.")
        print(f"请确保模型名称正确，并且已安装 'comet-core'。")
        print(f"原始错误: {e}")
        exit(1)
        
    print("准备COMET输入数据...")
    data = []
    for src, hyp, ref_list in zip(sources, hypotheses, references):
        # unbabel-comet的 'predict' 方法可以处理一个引用列表
        data.append({"src": src, "mt": hyp, "ref": ref_list})
    print("COMET输入数据准备完毕。")

    # 使用tqdm显示进度条
    try:
        print("开始COMET分数计算...")
        with tqdm(total=len(data), desc="Calculating COMET score") as pbar:
            model_output = model.predict(data, batch_size=8, gpus=1, progress_bar=True)
        print("COMET分数计算完成。")
        return model_output.scores, model_output.system_score
    except Exception as e:
        print(f"错误: 在COMET预测期间发生错误: {e}")
        exit(1)


def save_results(bleu_score, comet_score, output_dir, segment_scores=None, data=None):
    """
    将评估结果保存到CSV和Markdown文件。

    Args:
        bleu_score (float): 整体BLEU分数。
        comet_score (float): 整体COMET分数。
        output_dir (str): 结果输出目录。
        segment_scores (list, optional): 每个句子的COMET分数。
        data (dict, optional): 包含 'src', 'hyp', 'ref' 的原始数据。
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 保存摘要
    summary_df = pd.DataFrame([
        {'Metric': 'BLEU', 'Score': f"{bleu_score:.2f}"},
        {'Metric': 'COMET', 'Score': f"{comet_score:.4f}"}
    ])
    
    # 保存到CSV
    summary_csv_path = output_path / 'evaluation_summary.csv'
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"摘要结果已保存到: {summary_csv_path}")

    # 保存到Markdown
    summary_md_path = output_path / 'evaluation_summary.md'
    with open(summary_md_path, 'w', encoding='utf-8') as f:
        f.write("# 翻译质量评估结果\n\n")
        f.write(summary_df.to_markdown(index=False))
    print(f"摘要结果已保存到: {summary_md_path}")

    # 保存详细的句子级别分数
    if segment_scores and data:
        details_df = pd.DataFrame({
            'ID': [f"seg{i+1:03d}" for i in range(len(data['src']))],
            'Source': data['src'],
            'Hypothesis': data['hyp'],
            'Reference': ['; '.join(refs) for refs in data['ref']],
            'COMET_Score': segment_scores
        })
        details_csv_path = output_path / 'evaluation_details.csv'
        details_df.to_csv(details_csv_path, index=False)
        print(f"详细结果已保存到: {details_csv_path}")


def main():
    parser = argparse.ArgumentParser(description="使用BLEU和COMET评估机器翻译质量。")
    parser.add_argument('--input_file', type=str, required=True, help='包含src, hyp, 和 ref 的JSONL输入文件。')
    parser.add_argument('--output_dir', type=str, default='results', help='保存结果的目录。')
    parser.add_argument('--comet_model', type=str, default='eamt22-cometinho-da', help='要使用的COMET模型。')
    
    args = parser.parse_args()

    # 1. 加载数据
    sources, hypotheses, references = load_data(args.input_file)
    if not sources:
        print("未加载任何数据，正在退出。")
        return

    # 2. 计算BLEU
    print("正在计算BLEU分数...")
    bleu_score = calculate_bleu(hypotheses, references)
    print(f"BLEU 分数: {bleu_score:.2f}")

    # 3. 计算COMET
    print(f"正在使用 '{args.comet_model}' 计算COMET分数...")
    scores, system_score = calculate_comet(sources, hypotheses, references, args.comet_model)
    print(f"COMET 分数: {system_score:.4f}")

    # 4. 保存结果
    save_results(
        bleu_score,
        system_score,
        args.output_dir,
        segment_scores=scores,
        data={'src': sources, 'hyp': hypotheses, 'ref': references}
    )

    print("\n评估完成。")

if __name__ == "__main__":
    main()