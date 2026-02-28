# Reproducing Multi-Agent Text-to-SQL Frameworks (FTEC5660)

**Course:** FTEC5660 - Msc in Financial Technology, CUHK
**Objective:** Reproduce, evaluate, and enhance a Multi-Agent Text-to-SQL pipeline utilizing Google's Gemini LLMs to parse complex database schemas dynamically.

## 📌 Project Overview

This repository contains the reproduction and evaluation of a Multi-Agent Text-to-SQL framework. Instead of relying on a single zero-shot LLM prompt, this pipeline utilizes a sequential agentic workflow (Schema Linker $\rightarrow$ Subproblem Decomposer $\rightarrow$ Query Planner $\rightarrow$ SQL Generator) to accurately translate natural language into complex relational algebra.

The evaluation exposes the critical divergence between traditional string-matching metrics (**Exact Match**) and dynamic execution metrics (**Execution Accuracy**), while addressing the MLOps engineering challenges of cloud API rate-limiting in production FinTech systems.

---

## 📂 Directory Architecture

To run this project successfully, your local workspace must be structured as follows. Ensure that the `spider` dataset is located exactly two directories up relative to the execution scripts (as mapped in `utils.py`).

```text
Workspace-Root/
│
├── spider/                             <-- The downloaded Spider Dataset
│   ├── dev.json                        <-- The 1034-sample validation set
│   ├── train_spider.json         
│   └── database/                       <-- Contains the SQLite databases
│       ├── concert_singer/
│       │   ├── concert_singer.sqlite   <-- The actual database file
│       │   └── schema.sql              <-- DDL schema file
│       ├── stadium/
│       └── ... (other 160+ databases)
│
└── 25ftec/5660/SQL-of-Thought/         <-- Your Execution Directory
    ├── run_eval_single_schemalink.py   <-- Main execution loop
    ├── utils.py                        <-- LLM API calls, Auto-Retry, & DB Engine
    ├── prompts.py                      <-- System prompts for all Agents
    ├── README.md                       <-- This documentation
    └── ablations_actual/
        └── 60_gemini_3_flash_preview.json <-- Final output statistics
```

## 💾 Dataset Download: Spider

This project evaluates performance using the **Spider Dataset** (a large-scale, complex, cross-domain Text-to-SQL dataset).

1. Download the official dataset from the [Yale Spider Homepage](https://yale-lily.github.io/spider).
2. Extract the downloaded `spider.zip` file.
3. Place the extracted `spider` folder in the root directory as shown in the architecture tree above.

---

## 🚀 Environment Setup & Execution

### 1. Install Dependencies

This pipeline has been optimized to remove heavy local ML dependencies (like PyTorch or Transformers) by outsourcing the reasoning to Google's Generative AI SDK.

**Bash**

```
pip install google-generativeai
```

### 2. Configure API Keys

You must provide a valid Gemini API Key. Set it as an environment variable in your terminal before running the script.

**For Windows PowerShell:**

**PowerShell**

```
$env:GEMINI_API_KEY="AIzaSyYourActualKeyHere..."
```

**For macOS/Linux/GitBash:**

**Bash**

```
export GEMINI_API_KEY="AIzaSyYourActualKeyHere..."
```

### 3. Run the Evaluation

Navigate to the execution directory and run the main pipeline. The script is configured to process a 60-sample batch to balance rigorous evaluation with cloud API constraints.

**Bash**

```
python run_eval_single_schemalink.py
```

---

## 🛠️ Key Engineering Enhancements (MLOps)

During batch evaluation, cloud LLM endpoints frequently suffer from global traffic throttling. A direct API call will fatally crash the pipeline with `504 Gateway Timeout` or `503 Service Unavailable` errors.

To make this pipeline enterprise-ready,  **a robust Auto-Retry & Exponential Backoff wrapper was engineered in `utils.py`** .

* Catches asynchronous `grpc._channel._InactiveRpcError` exceptions.
* Implements a 60-second hard timeout to prevent zombie connections.
* Automatically sleeps for 5 seconds and retries (up to 5 attempts) to seamlessly bypass cloud server congestion without halting the 60-sample batch evaluation.

---


## 📊 Evaluation Results & Comparative Study

To evaluate both logical reasoning capabilities and cloud API reliability, a comparative ablation study was conducted using two different LLM backends on an identical 60-sample batch.

### Experimental Run 1: `gemini-3-flash-preview` (N=60 Batch)

*Focus: Bleeding-edge reasoning capabilities vs. preview API stability.*

| Metric                            | Score           | Implication                                                                                                                               |
| :-------------------------------- | :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **Valid SQL Rate**          | 100.00% (60/60) | Flawless syntax generation; 0 SQL compilation errors.                                                                                     |
| **Execution Accuracy (EA)** | 98.33% (59/60)  | Near-perfect semantic retrieval and logical reasoning.                                                                                    |
| **Exact Match (EM)**        | 45.00% (27/60)  | Heavily penalized due to algebraic variations (e.g., swapping `JOIN` aliases or using `INTERSECT`), proving EM is an obsolete metric. |

### Experimental Run 2: `gemini-2.5-flash` (N=60 Batch)

*Focus: Production-stable model baseline and concurrency reliability.*

| Metric                            | Score           | Implication                                                                                                                  |
| :-------------------------------- | :-------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Valid SQL Rate**          | 100.00% (60/60) | Demonstrates the framework's strict structural constraints remain effective across model generations.                        |
| **Execution Accuracy (EA)** | 98.33% (59/60)  | Matches the preview model exactly, proving that the multi-agent SQL-of-Thought pipeline is highly robust and model-agnostic. |
| **Exact Match (EM)**        | 45.00% (27/60)  | Further exposes the fundamental unreliability of strict string-matching evaluation in agentic AI.                            |

*Detailed qualitative error analysis regarding the EA vs. EM divergence, as well as the MLOps troubleshooting for API timeouts, is available in the final project report.*



### 🛑 Appendix: API Throttling & Partial Execution Artifact (N=36 Batch)

*Focus: Documenting cloud API volatility and the necessity of the Auto-Retry mechanism.*

Prior to the final engineering of the robust Auto-Retry MLOps wrapper, an initial batch execution using `gemini-2.5-flash` experienced a fatal pipeline crash at Sample 37. This was caused by severe, unhandled `504 Deadline Exceeded` errors from the global API server during peak traffic. The data from the surviving 36 samples is preserved below as empirical evidence of both the framework's baseline accuracy and the absolute necessity of fault-tolerant engineering in production:

| Metric                            | Score           | Implication                                                                             |
| :-------------------------------- | :-------------- | :-------------------------------------------------------------------------------------- |
| **Valid SQL Rate**          | 100.00% (36/36) | Flawless syntax generation was maintained right up until network failure.               |
| **Execution Accuracy (EA)** | 97.22% (35/36)  | Consistent high logical reasoning, matching the 60-sample batch.                        |
| **Exact Match (EM)**        | 55.56% (20/36)  | The EM vs. EA metric divergence remains stark regardless of the batch truncation point. |

```

```
