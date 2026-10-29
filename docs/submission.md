# Submission links and notes

## Primary deliverable

https://github.com/rajatmurhe/CYNBIT

## Optional additional links

1. AI Opportunity Report: https://github.com/rajatmurhe/CYNBIT/blob/main/docs/ai-opportunity-report.md
2. Technical Approach Report: https://github.com/rajatmurhe/CYNBIT/blob/main/docs/technical-approach.md
3. Functional prototype: https://github.com/rajatmurhe/CYNBIT/blob/main/app.py
4. Evaluation and limitations: https://github.com/rajatmurhe/CYNBIT/blob/main/docs/evaluation-report.md

## Execution notes

Cynbit Discovery Desk helps a reviewer turn an incoming inquiry into a relevant service, product or training route, with supporting sources and discovery questions. The project includes an opportunity analysis, a working Streamlit app and CLI, and a technical approach report. The prototype uses local word/character TF-IDF retrieval and template-based briefs, so it needs no model API key. Run `pip install -r requirements.txt` followed by `streamlit run app.py`. The repository includes 24 automated tests and a 40-case synthetic evaluation with per-case results and documented failures. All suggested routes need human review; business-impact estimates are assumptions for a pilot, not measured company results.
