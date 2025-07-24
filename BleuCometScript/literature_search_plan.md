# Academic Literature Search: A Multi-Phased Action Plan

**Research Project Parameters:**

*   **Research Topic/Question:** How can prompt engineering, specifically prompt formatting, be leveraged to improve the performance of Large Language Models (LLMs) on translation tasks?
*   **Academic Discipline:** Computer Science, Computational Linguistics, Translation Studies.
*   **Scope and Constraints:** Focus on sources published in the last 5 years (2020-Present). Include English and Chinese language sources. Prioritize empirical studies and technical reports over purely theoretical work.
*   **Target Output:** A literature review section for a research paper, supported by a 15-25 source bibliography.

---

## Phase 1: Foundational Strategy & Keyword Development

*   [ ] **Deconstruct the Research Question:** Break down the topic into its constituent concepts.
    *   **Concept 1:** Large Language Models (LLMs) / Generative AI
    *   **Concept 2:** Prompt Engineering / Prompt Design
    *   **Concept 3:** Translation / Machine Translation
    *   **Concept 4:** Performance Improvement / Optimization / Evaluation

*   [ ] **Develop a Keyword Matrix:** Brainstorm primary, secondary, and tertiary keywords for each concept.

| Concept             | Primary Keywords                      | Secondary Keywords                                       | Tertiary/Related Keywords                                     |
| ------------------- | ------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| **LLMs**            | "Large Language Model", "LLM", "GPT-4" | "Generative AI", "Transformer models"                    | "Foundation models", "ChatGPT"                                |
| **Prompting**       | "Prompt Engineering", "Prompt Design" | "Prompt Formatting", "In-context learning", "Few-shot"   | "Instruction tuning", "Chain of Thought", "Zero-shot"         |
| **Translation**     | "Translation", "Machine Translation"  | "Translation Quality", "Human-AI collaboration"          | "Cross-lingual transfer", "MTPE", "智能翻译" (Smart Translation) |
| **Performance**     | "Performance", "Evaluation", "Impact" | "Optimization", "Benchmark", "BLEU score", "COMET score" | "Robustness", "Consistency", "Efficiency", "提示素养" (Prompt Literacy) |

*   [ ] **Identify Seminal Texts & Authors:** Find initial anchor points for the search.
    *   **Action:** Review the bibliographies of the initial seed articles (`从“搜商”到“问商”...`, `Does_Prompt_Formatting...`, `GenAI时代的智能翻译素养...`).
    *   **Action:** Identify authors who are frequently cited (e.g., a paper on "Chain of Thought" will likely cite Wei et al.).
    *   **Action:** Search for foundational papers like "Attention Is All You Need" (Vaswani et al.) to understand the technological underpinnings.

---

## Phase 2: Systematic Search Execution

*   [ ] **Prioritize Search Platforms:** Select the most relevant databases and search engines.
    *   **Priority 1 (Core CS/AI):** arXiv, Google Scholar, ACL Anthology.
    *   **Priority 2 (Broader Academic Context):** Scopus, IEEE Xplore, Web of Science.
    *   **Priority 3 (Chinese Scholarship):** CNKI (中国知网) for articles on "智能翻译" and "提示素养".

*   [ ] **Execute Advanced Searches:** Combine keywords using Boolean operators for precision.
    *   **Search String 1 (Broad):** `( "prompt engineering" OR "prompt design" ) AND ( "translation" OR "machine translation" ) AND ( "LLM" OR "large language model" )`
    *   **Search String 2 (Specific):** `( "prompt format*" OR "prompt structure" ) AND ( "LLM" OR "GPT" ) AND "performance"`
    *   **Search String 3 (Technique-focused):** `( "chain of thought" OR "few-shot" ) AND "translation"`

*   [ ] **Implement Citation Mining (Snowballing):**
    *   **Action:** For every highly relevant article found, meticulously review its bibliography for other potential sources.
    *   **Action:** Use Google Scholar's "Cited by" and "Related articles" features for the most relevant papers to find more recent or related work.

---

## Phase 3: Source Triage & Critical Evaluation

*   [ ] **Conduct Initial Screening (Title/Abstract Review):**
    *   [ ] Does the title/abstract explicitly mention the core concepts (prompting, translation, LLMs)?
    *   [ ] Does the abstract promise empirical results, a new technique, or a valuable survey?
    *   [ ] Is the publication venue reputable (e.g., top-tier conference, high-impact journal)?
    *   [ ] Is it within the 5-year publication window?

*   [ ] **Critically Evaluate Shortlisted Sources:** Apply a deeper set of criteria to the most promising articles.
    *   **Credibility:** Is it peer-reviewed? Who are the authors and what are their affiliations (academic institution vs. industry lab)?
    *   **Methodology:** Is the experimental setup clear? Are the evaluation metrics well-defined and appropriate (e.g., BLEU, COMET, human evaluation)?
    *   **Contribution:** Does the paper offer a novel technique, a significant result, or a comprehensive overview?
    *   **Relevance:** How directly does it address the research question about *prompting's impact on translation*?

*   [ ] **Define Inclusion/Exclusion Criteria:**
    *   **Include:** Papers with quantitative results; comparative studies of different prompt techniques; work introducing novel prompting methods for translation.
    *   **Exclude:** Papers on non-LLM machine translation; purely theoretical or opinion pieces without data; papers where translation is only a trivial example for a broader claim.

---

## Phase 4: Organization & Management

*   [ ] **Establish a Citation Management Workflow:**
    *   **Action:** Choose and set up a citation manager (e.g., Zotero, Mendeley).
    *   **Action:** Create a dedicated project folder/collection (e.g., "LLM_Translation_Prompting").
    *   **Action:** Use the tool's browser connector to save sources directly from the web, ensuring metadata is captured correctly.
    *   **Action:** Immediately download and attach the full-text PDF to its corresponding entry.

*   [ ] **Create Preliminary Annotations:** For each selected source, create a structured note to capture key information.
    *   **Action:** In your citation manager, create a note for each entry.
    *   **Template for Notes:**
        *   **Core Argument:** (1-2 sentences on the paper's main finding).
        *   **Methodology:** (Briefly describe the experiment, e.g., "Compared JSON vs. Markdown prompts on GPT-3.5/4").
        *   **Key Result:** (A specific, powerful data point, e.g., "Found up to a 40% performance variance on code translation based on format").
        *   **Relevance:** (How it connects to your paper, e.g., "Direct evidence that prompt format is a critical variable").

*   [ ] **Organize for Final Output:**
    *   **Action:** Use tags within your citation manager to categorize sources (e.g., #Formatting, #CoT, #Evaluation, #Theory).
    *   **Action:** Set the required citation style (e.g., APA 7th, MLA 9th) within the tool.
    *   **Action:** When ready, use the tool to automatically generate a formatted bibliography for your literature review. Manually proofread the generated list for any minor errors.