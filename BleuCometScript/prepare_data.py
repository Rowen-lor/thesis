import json
import argparse
from pathlib import Path

def create_jsonl(src_path, hyp_path, ref_paths, output_path):
    """
    将源文本、假设文本和参考文本文件转换为JSONL文件。

    Args:
        src_path (str): 源文本文件的路径。
        hyp_path (str): 假设文本文件的路径。
        ref_paths (list): 参考文本文件路径的列表。
        output_path (str): 输出JSONL文件的路径。
    """
    try:
        with open(src_path, 'r', encoding='utf-8') as f_src:
            sources = [line.strip() for line in f_src]
        
        with open(hyp_path, 'r', encoding='utf-8') as f_hyp:
            hypotheses = [line.strip() for line in f_hyp]

        references_list = []
        for ref_path in ref_paths:
            with open(ref_path, 'r', encoding='utf-8') as f_ref:
                references_list.append([line.strip() for line in f_ref])
        
        # 转置引用列表，以便按句子分组
        # 从 [[ref1_sent1, ref1_sent2], [ref2_sent1, ref2_sent2]]
        # 转换为 [[ref1_sent1, ref2_sent1], [ref1_sent2, ref2_sent2]]
        references = list(zip(*references_list))

        if not (len(sources) == len(hypotheses) == len(references)):
            print("错误: 源文件、假设文件和参考文件中的行数必须相同。")
            return

        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f_out:
            for i, (src, hyp, ref_tuple) in enumerate(zip(sources, hypotheses, references)):
                data = {
                    "id": f"segment_{i+1:03d}",
                    "src": src,
                    "hyp": hyp,
                    "ref": list(ref_tuple)
                }
                f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
        
        print(f"成功创建JSONL文件于: {output_path}")

    except FileNotFoundError as e:
        print(f"错误: 文件未找到 - {e}")
    except Exception as e:
        print(f"发生意外错误: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将原始文本文件 (src, hyp, ref) 转换为JSONL格式。")
    parser.add_argument("--src", required=True, help="源句子文件的路径。")
    parser.add_argument("--hyp", required=True, help="机器翻译假设文件的路径。")
    parser.add_argument("--ref", required=True, nargs='+', help="一个或多个参考翻译文件的路径。")
    parser.add_argument("--output", required=True, help="输出JSONL文件的路径。")

    args = parser.parse_args()

    create_jsonl(args.src, args.hyp, args.ref, args.output)

    # 示例用法:
    # python prepare_data.py --src data/raw/src.txt --hyp data/raw/hyp.txt --ref data/raw/ref1.txt data/raw/ref2.txt --output data/converted.jsonl