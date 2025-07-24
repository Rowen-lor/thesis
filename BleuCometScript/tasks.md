**项目：** 机器翻译质量评估工具包

**阶段1：环境搭建与依赖安装**

*   **任务1.1：创建Python虚拟环境**
    *   创建一个新的Python虚拟环境，例如 `python -m venv mt_eval_env`。
    *   激活该环境：`source mt_eval_env/bin/activate` (Linux/macOS) 或 `mt_eval_env\Scripts\activate` (Windows)。
*   **任务1.2：安装所需库**
    *   使用pip安装所有在 `requirements.md` 中列出的库：
        ```bash
        pip install sacrebleu unbabel-comet pandas tqdm argparse
        ```
    *   （可选）如果COMET模型下载遇到问题，可能需要安装 `transformers` 和 `torch`：
        ```bash
        pip install transformers torch
        ```

**阶段2：数据准备指导**

*   **任务2.1：定义JSONL数据转换脚本（或指导）**
    *   提供一个简单的Python脚本示例，说明如何将原始的 `src.txt`, `hyp.txt`, `ref.txt` (每行一个句子) 转换为 `data.jsonl` 格式。
    *   **示例转换逻辑：**
        *   读取 `src.txt` 到 `sources` 列表。
        *   读取 `hyp.txt` 到 `hypotheses` 列表。
        *   读取 `ref.txt` 到 `references` 列表。
        *   遍历列表，将每条数据构建成JSON对象，并写入 `output.jsonl`。
        *   **注意：** 如果有多个参考译文文件（如 `ref1.txt`, `ref2.txt`），需要将它们合并到 `ref` 字段的数组中。
*   **任务2.2：创建示例数据文件**
    *   在 `data/` 目录下创建一个名为 `sample_data.jsonl` 的文件，包含至少3-5条翻译对，用于测试。
    *   **示例 `data/sample_data.jsonl` 内容：**
        ```json
        {"id": "seg001", "src": "The cat sat on the mat.", "hyp": "猫坐在垫子上。", "ref": ["猫坐在垫子上。"]}
        {"id": "seg002", "src": "How are you today?", "hyp": "你今天怎么样？", "ref": ["你今天好吗？", "你今天过得怎么样？"]}
        {"id": "seg003", "src": "This is a very long sentence that needs to be translated accurately.", "hyp": "这是一个需要准确翻译的非常长的句子。", "ref": ["这是一个需要准确翻译的非常长的句子。"]}
        ```

**阶段3：核心评估脚本开发 (`bleu_comet_evaluator.py`)**

*   **任务3.1：脚本骨架与命令行解析**
    *   创建 `bleu_comet_evaluator.py` 文件。
    *   使用 `argparse` 设置命令行参数：
        *   `--input_file`: JSONL格式的输入文件路径 (必需)。
        *   `--output_dir`: 结果输出目录 (默认为 `results/`)。
        *   `--comet_model`: COMET模型名称 (默认为 `unbabel/wmt20-comet-da`)。
*   **任务3.2：数据加载函数**
    *   实现 `load_data(filepath)` 函数：
        *   读取JSONL文件。
        *   解析每行JSON对象，提取 `src`, `hyp`, `ref`。
        *   返回 `sources`, `hypotheses`, `references` 三个列表。
        *   进行基本的错误检查，如文件是否存在，JSON格式是否正确。
*   **任务3.3：BLEU计算函数**
    *   实现 `calculate_bleu(hypotheses, references)` 函数：
        *   使用 `sacrebleu.corpus_bleu(hypotheses, [references])` 计算BLEU分数。
        *   **注意：** `sacrebleu` 的 `references` 参数需要一个列表的列表，即使只有一个参考译文集。
        *   返回BLEU分数（浮点数）。
*   **任务3.4：COMET计算函数**
    *   实现 `calculate_comet(sources, hypotheses, references, model_name)` 函数：
        *   初始化 `COMET` 模型：`model = COMET(pretrained_model=model_name)`。
        *   构建输入数据字典列表：`data = [{"src": s, "mt": h, "ref": r[0] if len(r) == 1 else r} for s, h, r in zip(sources, hypotheses, references)]`。
            *   **注意：** COMET库的 `predict` 方法对 `ref` 字段的处理：如果只有一个参考，可以直接是字符串；如果有多个，需要是字符串列表。这里统一处理为列表。
        *   使用 `model.predict(data, batch_size=8, gpus=1, progress_bar=True)` 进行预测。
        *   返回COMET分数（浮点数）。
*   **任务3.5：结果保存函数**
    *   实现 `save_results(bleu_score, comet_score, output_dir)` 函数：
        *   创建输出目录（如果不存在）。
        *   将BLEU和COMET分数保存到CSV文件（例如 `results/evaluation_summary.csv`）。
            *   CSV内容：`Metric,Score
BLEU,XX.XX
COMET,YY.YY`
        *   将分数保存到Markdown文件（例如 `results/evaluation_summary.md`）。
            *   Markdown内容：
                ```markdown
                # 翻译质量评估结果

                | Metric | Score |
                |--------|-------|
                | BLEU   | XX.XX |
                | COMET  | YY.YY |
                ```
*   **任务3.6：主执行逻辑**
    *   在 `if __name__ == "__main__":` 块中：
        *   解析命令行参数。
        *   调用 `load_data`。
        *   调用 `calculate_bleu`。
        *   调用 `calculate_comet`。
        *   调用 `save_results`。
        *   打印最终结果到控制台。

**阶段4：测试与验证**

*   **任务4.1：使用示例数据进行测试**
    *   运行 `python bleu_comet_evaluator.py --input_file data/sample_data.jsonl`。
    *   检查 `results/` 目录下是否生成了 `evaluation_summary.csv` 和 `evaluation_summary.md` 文件，并验证其内容是否正确。
*   **任务4.2：边缘情况测试**
    *   测试输入文件不存在的情况。
    *   测试输入文件格式不正确的情况（例如，不是有效的JSONL）。

**阶段5：文档与README**

*   **任务5.1：更新 `README.md`**
    *   添加项目简介。
    *   详细说明环境搭建步骤。
    *   详细说明数据准备（JSONL格式）和转换方法。
    *   提供 `bleu_comet_evaluator.py` 的使用示例和参数说明。
    *   解释输出文件的结构和内容。
    *   添加常见问题解答（FAQ）或故障排除指南。
