# 🏛️ CBSL Compliance & Transaction Categorization Engine (PoC)

> **A proposal for automating regulatory returns in Sri Lankan Banking using On-Premise AI.**

![Status](https://img.shields.io/badge/Status-Prototype-orange) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## ⚠️ DISCLAIMER: Educational Prototype Only
This software is a Proof of Concept (PoC) designed to demonstrate the capabilities of **Local LLMs** in regulatory reporting. It is **not** a production-ready banking system and has not been audited for security by the Central Bank of Sri Lanka (CBSL). Use this code for research and testing purposes only. The author (Amila Dayananda) assumes no liability for financial losses or non-compliance resulting from the use of this code in a live environment.
*Note: All data shown in screenshots is synthetically generated.*

## 📖 Overview
Sri Lankan banks face a challenge: **Automating CBSL reporting (ITRS, FinNet, goAML)** without sending sensitive customer data to the cloud.

This solution proposes a **Hybrid "Local AI" Pipeline**:
1.  **Product Mapping:** Instant categorization for internal codes (e.g., `LN_PMT`).
2.  **Local LLM:** A privacy-first AI model (e.g., Llama 3) running on-premise to categorize vague narrations (e.g., "Uni fees") into ITRS Purpose Codes.
3.  **Human-in-the-Loop UI:** A dashboard for Compliance Officers to review low-confidence transactions.

## 🏗 Architecture
[Core Banking DB] -> [Python ETL] -> [Local LLM (Ollama)] -> [Streamlit Dashboard] -> [FinNet XML/CSV]

## 💻 Tech Stack
* **Python 3.10**
* **Streamlit** (For the Compliance Dashboard UI)
* **Pandas** (Data Processing)
* **Mock Local LLM** (Simulated for this demo)

## 🚀 How to Run
1.  Install dependencies:
    ```bash
    pip install streamlit pandas
    ```
2.  Run the application:
    ```bash
    streamlit run app.py
    ```



CBSL Total Transaction Reporting Engine 🇱🇰
A production-ready framework for Sri Lankan financial institutions to automate 100% of regulatory returns. This engine ingests daily transaction logs and categorizes every single line item using a "Waterfall" logic approach to balance speed and accuracy.

🌊 The Waterfall Logic
Product-Based (Level 1): Immediate mapping of Core Banking "Tran Codes" (e.g., LN_PMT → Loan Repayment).

Rule-Based (Level 2): Keyword matching for common descriptors (e.g., ATM → Cash Withdrawal).

Local LLM (Level 3): Uses a quantized Llama-3 model running locally to infer purpose codes from unstructured customer narrations.

🚀 Supported Returns
FinNet: Standard CSV/XML uploads for periodic returns.

ITRS: Cross-border purpose code classification (Directions No. 1 of 2021/Updates).

goAML: XML Schema 4.0 generation for CTR (Cash Transaction Reports) > 1M LKR.

🛠 Tech Stack
Language: Python 3.10

AI: Ollama (Llama 3) + LangChain

Full Prototype & Working Plan
1. Functional Architecture
The system processes data in three stages to ensure every transaction is captured.

2. Python Code (The Hybrid Engine)
This script implements the "Waterfall" logic to handle all transactions efficiently.

ETL: Pandas, SQLAlchemy

Validation: Tableau Prep / Great Expectations

3. Validation & Reporting Dashboard
A Tableau Prep flow is essential to visualize the classification breakdown before submission.

Views:

Classification Confidence: A bar chart showing how many transactions were caught by Tier 1 (Product Codes) vs Tier 3 (AI).

The "Unknown" Bin: A specific list of transactions where the AI returned "MANUAL_REVIEW". This is the only list the officer needs to work on.

CBSL Threshold Alerts: Highlights any Cash transaction > 1M LKR or Electronic Transfer > 5M LKR for immediate scrutiny.

4. Data Migration Plan
To implement this into a live environment:

Day 1-5: Historical Mapping: Export 3 months of transaction history. Run the script to build the PRODUCT_CODE_MAP (Tier 1) so it covers 80% of volume immediately.

Day 6-10: AI Tuning: Fine-tune the Llama 3 system prompt using the "General Transfers" from the history logs to teach it Sri Lankan context (e.g., "Kade" means shop/merchant).

Day 15: Parallel Run: Generate the FinNet files using the new Python engine but do not submit. Compare them with the manually created files to verify accuracy.
