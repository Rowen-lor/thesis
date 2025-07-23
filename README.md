# 翻译质量评估工具

此项目提供一个 Python 脚本 `bleu_comet_evaluator.py`，用于使用 BLEU 和 COMET 指标评估机器翻译的质量。

## 文件说明

-   `bleu_comet_evaluator.py`: 核心评估脚本，用于计算 BLEU 和 COMET 分数。
-   `requirements.txt`: 项目所需的 Python 依赖库列表。

## 安装

1.  **克隆仓库** (如果您还没有克隆):
    ```bash
    git clone https://github.com/your_username/your_repository_name.git
    cd your_repository_name
    ```
2.  **创建并激活虚拟环境** (推荐):
    ```bash
    python -m venv venv
    # 在 Windows 上
    .\venv\Scripts\activate
    # 在 macOS/Linux 上
    source venv/bin/activate
    ```
3.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

脚本接受一个 JSONL 格式的输入文件，并生成评估结果。

### 运行脚本

```bash
python bleu_comet_evaluator.py --input_file <input_file.jsonl> [--output_dir <output_directory>] [--comet_model <comet_model_name>]
```

**参数**:
-   `--input_file`: (必填) 包含源句子、机器翻译输出和参考译文的 JSONL 文件路径。
-   `--output_dir`: (可选) 保存评估结果的目录。默认为 `results`。
-   `--comet_model`: (可选) 要使用的 COMET 模型名称。默认为 `eamt22-cometinho-da`。您可以在 COMET 模型中心找到更多模型：[https://www.unbabel.com/comet/models/](https://www.unbabel.com/comet/models/)

### 输入文件格式 (`.jsonl`)

输入文件应为 JSONL (每行一个 JSON 对象) 格式，每个 JSON 对象包含以下键：
-   `src`: 源句子 (string)
-   `hyp`: 机器翻译输出 (string)
-   `ref`: 参考译文 (string 或 string 列表)。如果只有一个参考译文，可以是字符串；如果有多个参考译文，必须是字符串列表。

**示例输入文件 (`sample_data.jsonl`)**:
```jsonl
{"src": "Hello, world.", "hyp": "你好，世界。", "ref": "你好，世界。"}
{"src": "How are you?", "hyp": "你怎么样？", "ref": ["你怎么样？", "你好吗？"]}
```

### 输出文件

脚本将在 `--output_dir` 指定的目录下生成以下文件：
-   `evaluation_summary.csv`: 包含整体 BLEU 和 COMET 分数的 CSV 摘要。
-   `evaluation_summary.md`: 包含整体 BLEU 和 COMET 分数的 Markdown 摘要。
-   `evaluation_details.csv`: (如果存在) 包含每个句子 COMET 分数的详细 CSV 文件，以及源句子、机器翻译和参考译文。

## 示例

```bash
python bleu_comet_evaluator.py --input_file sample_data.jsonl --output_dir my_evaluation_results --comet_model XLM-RoBERTa-Large-XNLI-COMET-XXL
