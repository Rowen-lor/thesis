**项目名称：** 机器翻译质量评估工具包 (BLEU & COMET)

**项目目标：**
开发一个Python工具包，用于自动化计算机器翻译（MT）输出的BLEU和COMET分数。该工具包旨在支持翻译学研究，特别是需要对比不同MT系统性能或分析特定翻译现象的学术论文撰写。

**核心功能需求：**

*   **数据管理：**
    *   能够高效存储和读取原文（Source）、机器译文（Hypothesis）和参考译文（Reference）数据。
    *   支持多条原文-译文-参考译文对的评估。
    *   支持单条原文对应多条参考译文的情况。
*   **BLEU分数计算：**
    *   实现标准的BLEU分数计算功能。
    *   优先使用 `sacrebleu` 库，以确保计算结果的标准化和可复现性。
*   **COMET分数计算：**
    *   实现COMET分数计算功能。
    *   优先使用 `unbabel-comet` 库，并允许指定COMET模型（例如 `unbabel/wmt20-comet-da`）。
*   **结果输出：**
    *   将评估结果（包括总体的BLEU和COMET分数）以清晰、易于分析的格式输出。
    *   支持输出到CSV文件，便于导入到电子表格软件进行进一步分析。
    *   支持输出到Markdown表格，便于直接嵌入到报告或论文中。

**数据格式要求：**

*   **主要数据格式：JSON Lines (JSONL)**
    *   **文件结构：** 每个文件包含多行，每行是一个独立的JSON对象。
    *   **每行JSON对象结构：**
        ```json
        {
            "id": "unique_segment_id_001",
            "src": "This is a source sentence.",
            "hyp": "这是源语句。",
            "ref": ["这是一个参考语句。", "这是另一个参考语句。"]
        }
        ```
    *   **字段说明：**
        *   `id` (字符串): 唯一标识符，用于追踪每个翻译对。
        *   `src` (字符串): 原始语言的句子。
        *   `hyp` (字符串): 机器翻译的输出句子。
        *   `ref` (字符串数组): 一个或多个参考译文句子。即使只有一个参考译文，也应以数组形式表示。
    *   **优势：** 这种格式非常适合处理大量数据，每行独立，易于解析，且能灵活支持多参考译文。
*   **输入文件命名约定：**
    *   建议使用 `data/your_dataset_name.jsonl` 这样的路径和命名。

**技术栈要求：**

*   **编程语言：** Python 3.8+
*   **核心库：**
    *   `sacrebleu`：用于BLEU分数计算。
    *   `unbabel-comet`：用于COMET分数计算。
    *   `pandas`：用于数据处理和CSV输出。
    *   `tqdm`：用于显示处理进度条（特别是COMET计算可能耗时）。
    *   `argparse`：用于构建命令行接口，方便用户指定输入/输出文件和参数。

**性能与鲁棒性要求：**

*   **可扩展性：** 能够处理包含数千甚至数万条翻译对的数据集。
*   **错误处理：**
    *   对文件不存在、文件格式错误、数据不一致（如行数不匹配）等情况进行适当的错误提示或处理。
    *   确保COMET模型加载失败时有明确提示。
*   **可复现性：** 确保BLEU和COMET的计算结果在相同输入和参数下是可复现的。

**用户界面要求：**

*   提供命令行接口（CLI），允许用户通过参数指定输入文件、输出路径和COMET模型等。


---

### 使用指南 (给你自己看的，如何使用AI生成的工具)

恭喜你！你的AI已经根据上述需求和步骤为你准备好了翻译质量评估工具。以下是你如何使用它的指南：

**1. 准备工作**

*   **检查AI的输出：** 确保你的AI已经生成了以下文件和目录：
    *   `bleu_comet_evaluator.py` (核心评估脚本)
    *   `data/` 目录 (可能包含 `sample_data.jsonl` 示例数据)
    *   `results/` 目录 (用于存放评估结果，初始可能为空)
    *   `README.md` (项目说明文档)
*   **激活Python环境：**
    *   打开你的终端或命令提示符。
    *   进入项目根目录。
    *   激活AI为你创建的Python虚拟环境（如果AI没有创建，你需要手动创建并安装依赖）：
        ```bash
        # Linux/macOS
        source mt_eval_env/bin/activate
        # Windows
        .\mt_eval_env\Scripts\activate
        ```
    *   如果提示找不到 `mt_eval_env`，请查看 `README.md` 或询问AI如何创建和激活环境。

**2. 准备你的翻译数据**

这是最关键的一步。你需要将你的原文、机器译文和参考译文整理成AI所要求的 **JSON Lines (JSONL)** 格式。

*   **JSONL格式要求：**
    *   一个 `.jsonl` 文件，每行是一个JSON对象。
    *   每个JSON对象包含 `id` (唯一ID), `src` (原文), `hyp` (机器译文), `ref` (参考译文列表)。
    *   **示例：**
        ```json
        {"id": "doc1_seg1", "src": "The quick brown fox.", "hyp": "敏捷的棕色狐狸。", "ref": ["那只敏捷的棕色狐狸。"]}
        {"id": "doc1_seg2", "src": "Jumped over the lazy dog.", "hyp": "跳过了懒惰的狗。", "ref": ["跳过那只懒惰的狗。", "跳过那条懒狗。"]}
        ```
*   **如何转换你的数据：**
    *   如果你的数据是 `src.txt`, `hyp.txt`, `ref.txt` (每行一个句子)，请查阅AI生成的 `todo.md` 或 `README.md` 中关于“数据准备”的部分。AI应该提供了一个简单的Python脚本或指导，帮助你将这些文件转换为JSONL格式。
    *   将你准备好的JSONL文件放到 `data/` 目录下，例如命名为 `my_translation_data.jsonl`。

**3. 运行评估脚本**

*   在已激活Python环境的终端中，运行核心评估脚本：
    ```bash
    python bleu_comet_evaluator.py --input_file data/my_translation_data.jsonl --output_dir results --comet_model unbabel/wmt20-comet-da
    ```
*   **参数说明：**
    *   `--input_file`: 你的JSONL数据文件的路径。
    *   `--output_dir`: 评估结果将保存到的目录。默认为 `results/`。
    *   `--comet_model`: 你想使用的COMET模型名称。`unbabel/wmt20-comet-da` 是一个常用的模型。如果你想尝试其他模型，可以查阅 `unbabel-comet` 库的文档。
*   脚本运行过程中，你可能会看到COMET模型下载的进度条（首次运行）和评估的进度条。

**4. 查看评估结果**

*   脚本运行完成后，你会在 `--output_dir` 指定的目录下（默认为 `results/`）找到评估结果文件：
    *   `evaluation_summary.csv`: 包含BLEU和COMET分数的CSV文件，便于导入Excel或Pandas进行分析。
    *   `evaluation_summary.md`: 包含BLEU和COMET分数的Markdown表格，可以直接复制粘贴到你的论文或报告中。
*   打开这些文件，你就可以看到你的机器翻译系统的BLEU和COMET分数了。

**5. 撰写论文**

*   **数据分析：** 使用CSV文件中的分数，结合你的研究问题，进行深入分析。你可以比较不同翻译系统、不同语料库或不同翻译策略的性能。
*   **结果呈现：** 将Markdown表格直接嵌入到你的论文中，或根据CSV数据制作更复杂的图表。
*   **讨论：** 结合BLEU和COMET分数的特点（BLEU侧重词汇重叠，COMET侧重语义和流畅度），讨论你的发现。例如，一个系统可能BLEU分数不高但COMET分数很高，这可能意味着它在语义上更准确，但在词汇选择上与参考译文差异较大。

**6. 故障排除**

*   **"ModuleNotFoundError"：** 确保你已激活正确的Python虚拟环境，并且所有依赖库都已安装。
*   **"FileNotFoundError"：** 检查 `--input_file` 和 `--output_dir` 的路径是否正确。
*   **COMET模型下载失败：** 检查你的网络连接，或尝试手动下载模型（查阅 `unbabel-comet` 文档）。
*   **数据格式错误：** 仔细检查你的JSONL文件是否严格遵循了要求的格式。

希望这份详细的指南能帮助你顺利完成翻译学论文！如果你在任何步骤中遇到问题，随时向我提问。