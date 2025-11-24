# ClauseSense AI – Automated Policy Compliance Analyzer

A Gemini-powered document compliance engine with rule matching, violation detection, severity scoring, rewrite suggestions, and a Streamlit web UI.

Project Link: [Repository link](https://github.com/Gaurika-Sethi/ClauseSense.git)

## Overview
ClauseSense AI is an intelligent compliance-analysis system that scans documents for violations of company policies such as:

- Privacy & data protection
- Password sharing
- PII leakage
- Client information handling
- USB/Device misuse
- Encryption requirements

It combines Gemini AI, local embeddings, and a multi-agent architecture to automatically:

- Extract text
- Match policy rules
- Detect violations
- Explain the reasoning behind each violation
- Rate severity (Low/Medium/High)
- Suggest rewrites
- Generate a final report (.txt + .json)

A fully interactive Streamlit UI makes it easy to upload documents and view/download results.

## Core Features
Multi-Agent Processing Pipeline

ClauseSense uses modular agents, each responsible for one phase:

|Phase | Agent | Function |
|:-----|:---:|-----:|
| 0 | Orchestrator | Initialize document metadata & shared state |
| 1 | Ingestion Agent | Extract & sectionize text |
| 2 | Policy Agent | Load + parse policy rules |
| 3 | Retrieval Agent | Match relevant rules |
| 4 | Compliance Agent | Detect violations & evidence |
| 5 | Rewrite Agent | Suggest Gemini rewrite fixes |
| 6 | Report Agent | Final text & JSON report |
| 7 | AI Enhancements | Explanations, confidence scoring, severity classification |
| 8 | Streamlit UI | Upload + report interface |
| 9 | Deployment | Streamlit Cloud deployment |

## Gemini Integration

ClauseSense integrates Gemini 2.0 Flash for:

- Natural-language reasoning
- Violation explanation
- Rewrite suggestions
- Severity classification

Local embeddings (SentenceTransformers) provide:

- Reliable rule-section similarity
- Confidence scores
- No API usage or cost for embeddings

Streamlit Cloud uses Secrets Manager:
```bash
GEMINI_API_KEY = "your-key-here"
GEMINI_MODEL = "gemini-2.0-flash"
```

## Project Structure

```bash
ClauseSense/
│
├── main.py
├── ui.py                          # Streamlit front-end
│
├── orchestrator/
│   └── orchestrator_agent.py
│
├── ingestion/
│   ├── ingest_agent.py
│   └── text_extractor.py
│
├── policy/
│   ├── load_policy.py
│   └── rule_agent.py
│
├── retrieval/
│   └── retrieval_agent.py
│
├── compliance/
│   └── compliance_agent.py
│
├── rewrite/
│   └── rewrite_agent.py
│
├── reporting/
│   └── report_agent.py
│
├── reconstruction/
│   └── unifier.py
│
├── gemini/
│   ├── gemini_client.py
│   ├── utils.py
│   └── prompts/
│       └── compliance_prompts.py
│
└── assets/
    └── logo.png
```

## Streamlit Web App

The UI supports:

- Uploading a document file
- Uploading a policy file
- Running the full analysis pipeline
- Displaying the final compliance report

Downloading:

- final_report.txt
- final_report.json

Branding includes:

- Custom dark theme
- Logo on header
- Clean layout

Run locally:
```bash
streamlit run ui.py
```

## How It Works
1. Upload document & policy

User uploads:

- Document (.txt)
- Policy (.txt)

2. Agents process the data

Pipeline runs phases 0–7.

3. Violations detected

Each rule → section pair analyzed for:

- Violation or not
- Evidence snippet
- Severity
- Confidence score
- Explanation (Gemini)
- Rewrite suggestion

4. Report Generated

Final outputs:

```bash
final_report.txt
final_report.json
```
Automatically stored and available for download.

## Installation

Follow these steps to run the project locally:

### Clone the repository  
```bash
   git clone https://github.com/Gaurika-Sethi/ClauseSense.git
  ```

### Install dependencies 
```bash
pip install -r requirements.txt
```
### Create .env for local use
```bash
GEMINI_API_KEY="your-key"
GEMINI_MODEL="gemini-2.0-flash"
```
## Run locally

```bash
streamlit run ui.py
```
## Deployment (Streamlit Cloud)

### Add secrets:
Go to:

```bash
Settings → Secrets
```

Paste:

```bash
GEMINI_API_KEY="your_key"
GEMINI_MODEL="gemini-2.0-flash"
```
Choose:

- repo → gaurika-sethi/ClauseSense
- branch → main
- file → ui.py

Deploy.

## Testing

Sample files are included:

- sample_doc.txt
- sample_policy.txt

The system supports:

- edge cases
- missing rules
- long documents
- tokenization fallback mode

## Tech Stack

- Python 3.13
- Google Gemini API
- SentenceTransformers
- Streamlit
- Report Generation (TXT + JSON)

## Contributors

- Gaurika Sethi 
- Rishi Raj Goel

## Contact

### Gaurika Sethi
- LinkedIn: https://www.linkedin.com/in/gaurika-sethi-53043b321
- Medium: https://medium.com/@pixelsnsyntax
- Twitter: https://twitter.com/pixelsnsyntax

### Rishi Raj Goel
- LinkedIn: https://www.linkedin.com/in/rishi-raj-goel-a77350326

## License

This project is licensed under the **MIT License**  see the [LICENSE](LICENSE) file for full details. 
