#  ClauseSense – AI-Powered Policy Compliance Auditor

ClauseSense is an intelligent multi-agent compliance analysis system that evaluates business documents (contracts, HR policies, NDAs, privacy statements, etc.) against organizational or regulatory policy rules. It identifies non-compliant clauses, suggests corrections, and generates a detailed compliance report — all autonomously.

Built as a CAPSTONE project focused on **AI agents, reasoning models, and enterprise automation**, ClauseSense demonstrates how generative AI can assist legal, HR, and policy teams by drastically reducing manual review time and risk.



##  Project Repository
 [The link of the official Repository](https://github.com/Gaurika-Sethi/ClauseSense.git)



##  Problem Statement

Policy and contract reviews are traditionally manual, time-intensive, and prone to oversight. Organizations routinely struggle with:

- Hidden non-compliant clauses  
- Ambiguous or risky wording in contracts  
- Inconsistent adherence to legal & HR regulations  
- Lack of standardized review processes  

ClauseSense solves this by automating document-to-policy comparison using a structured **multi-agent LLM workflow**, delivering fast, reliable, and standardized compliance insights.



##  Solution Overview

ClauseSense automates compliance assessment through an end-to-end document intelligence pipeline. It begins by ingesting and extracting text from uploaded files, then parses and interprets internal policy rules. Using semantic similarity via embeddings, it identifies the most relevant regulations for each section of the document. An AI-powered reasoning agent evaluates whether clauses align with those policy standards and flags non-compliant ones. These flagged clauses are then improved by a dedicated rewrite agent, which suggests safe and policy-aligned alternatives. Finally, a reporting agent consolidates the findings into a structured compliance report containing detailed insights and metrics.


## Core Features

- **Autonomous Document Ingestion & Parsing**  
  Automatically processes PDF, DOCX, and TXT files with high accuracy, ensuring clean and complete text extraction.

- **Policy-Aware Interpretation**  
  Transforms policy documents into rule-based structures for machine-understandable comparison.

- **Embedding-Based Rule Retrieval**  
  Locates the most relevant compliance rules for each clause using semantic search powered by AI embeddings.

- **Clause-Level Compliance Judgement**  
  Highlights risky, ambiguous, or non-aligned sentences with clear reasoning on why they violate policy.

- **Smart Rewrite Suggestions**  
  Generates refined, legally safe, and policy-adherent alternatives for each flagged clause.

- **Comprehensive Compliance Report**  
  Consolidates results into an easy-to-read professional summary for legal and HR teams.



## Project Structure

ClauseSense/

│

├── main.py

│

├── orchestrator/

│ └── orchestrator_agent.py

│

├── ingestion/

│ ├── ingest_agent.py

│ └── text_extractor.py

│

├── policy/

│ ├── load_policy.py

│ └── rule_agent.py

│

├── retrieval/

│ └── retrieval_agent.py

│

├── compliance/

│ └── compliance_agent.py

│

├── rewrite/

│ └── rewrite_agent.py

│

└── reporting/

└── report_agent.py

---


## Tech Stack 

###  Programming & Core
- Python

###  AI & Reasoning
- Gemini API (LLM reasoning)
- Gemini Embeddings (semantic similarity)

###  Document Processing
- PyPDF
- python-docx

###  Software Design
- Multi-agent modular architecture
- Scalable folder structure

##  Impact of the Project
ClauseSense demonstrates the real-world potential of AI to enhance enterprise workflows by reducing repetitive manual effort while improving compliance accuracy. It provides measurable value for HR, Legal, and Governance departments by minimizing human oversight risk and ensuring organizations remain aligned with internal and external regulations. The project highlights how agentic AI can empower businesses to operate more safely, efficiently, and intelligently.

##  Status
 Active Development – core pipeline implementation in progress.

##  Contributors
| Name | Role |
|------|------|
| Gaurika Sethi (Lead) | AI Agent Architecture & Compliance Reasoning |
| Rishi Raj Goel | Document Processing & Report Automation |

##  License
 This project is developed for CAPSTONE evaluation and educational purposes.

##  Feedback / Issues
For suggestions or collaboration, feel free to open an issue or drop feedback in the repository.
