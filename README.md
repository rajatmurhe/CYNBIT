# Cynbit Discovery Desk

**A first-inquiry assistant that turns a project brief into a suggested route, evidence and useful discovery questions.**

Built for the Cynbit AI/ML Engineer Intern assessment by **Rajat Murhe**.

[![Checks](https://github.com/rajatmurhe/CYNBIT/actions/workflows/checks.yml/badge.svg)](https://github.com/rajatmurhe/CYNBIT/actions/workflows/checks.yml)

## Start here

| Deliverable | What to read or run |
| --- | --- |
| AI Opportunity Report | [Business context, industry analysis, opportunity shortlist and pilot economics](docs/ai-opportunity-report.md) |
| Functional proof of concept | [Streamlit app](app.py) and [Python retrieval engine](cynbit_discovery/engine.py) |
| Technical Approach Report | [Models, data pipeline, architecture, prompt strategy and execution plan](docs/technical-approach.md) |
| Evaluation | [Results and failure analysis](docs/evaluation-report.md), [per-case output](docs/evaluation.json) |
| Submission details | [Links and ready-to-paste execution notes](docs/submission.md) |

## Why this opportunity?

Cynbit's [contact page](https://www.cynbit.in/contact) asks for an open-ended project message before the discovery conversation. A visitor may need a custom project, an existing product or a training program. This prototype helps a reviewer identify a starting point and the questions still worth asking.

It is an internal-assistant proposal, not a claim about Cynbit's current internal systems. The reports distinguish published company information, project assumptions and measured prototype results.

## Run the demo

Python **3.11** is the tested version. No API key, GPU, database or model download is required. Internet access is needed for initial dependency installation; inference then runs locally.

```bash
git clone https://github.com/rajatmurhe/CYNBIT.git
cd CYNBIT
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate with `.venv\Scripts\activate` and use `python` if `python3` is unavailable. Open the local URL printed by Streamlit.

1. Keep the invoice-workflow sample or choose another sample and click **Load sample**.
2. Click **Prepare discovery brief**.
3. Review the suggested route, source, similarity and follow-up questions.
4. Download the brief or JSON. Try an unrelated inquiry to see the clarification path.

Use fictional inputs. The application does not write inquiries to a database or send them to a model provider, but contact masking is incomplete. A hosted instance would process inputs on its server.

## Command-line example

```bash
python -m cynbit_discovery --text "We need tenant rent tracking and payment reminders."
python -m cynbit_discovery --text "We need AWS hosting and deployment support." --format json
python -m cynbit_discovery --file inquiry.txt > discovery-brief.md
```

Prefer `--file` for private inputs because command-line arguments may enter shell history. Do not commit real inquiries or exported customer briefs. A checked-in [synthetic example brief](docs/example-brief.md) shows the output without running anything.

## How it works

The engine fits TF-IDF vectors on eight reviewed catalog entries. Word and character cosine similarities are combined at 80/20 weights. It asks for more context below a score of 0.16 and for review when the top-two gap is below 0.04. These are initial heuristics, not calibrated confidence levels.

Every catalog match carries a source URL and review date. Questions and next steps come from templates; no generative model is used. The prototype makes no pricing, delivery or eligibility commitments and does not send messages.

## What the evaluation actually shows

On **40 synthetic cases**, the combined model places an acceptable route first for **31 of 32** in-scope requests. It makes **30** single-route suggestions, of which **29** match an acceptable route, and abstains on **7 of 8** unsupported requests. Expected behavior is correct on **36 of 40** cases.

The failures matter: a legal-contract request is misrouted, one mixed request is reduced to a single route, and spelling errors and an indirect phrasing trigger fallback. These results demonstrate a baseline, not customer-facing readiness. [Read the full evaluation](docs/evaluation-report.md).

## Run the checks

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
pytest -q
python scripts/evaluate.py
```

`requirements.txt` pins direct runtime dependencies; `requirements-lock.txt` records the full tested development environment. To recreate those exact package versions, install the lock file instead. The evaluation writes its JSON report, so rerunning it may change latency fields.

GitHub Actions runs lint, format checks, 24 tests and evaluation on Python 3.11. The workflow uploads the new evaluation as an artifact; it does not silently replace the committed reference run.

## Repository layout

```text
app.py                       Streamlit review workspace
cynbit_discovery/             Retrieval engine, exports and CLI
data/catalog.json            Sourced service/product/program catalog
data/dev_cases.json          Synthetic development cases
data/evaluation_cases.json   Fixed synthetic challenge set
scripts/evaluate.py          Baseline comparison and per-case results
tests/                       Engine, CLI and UI checks
docs/                        Reports, example output and submission notes
```

## Scope

The public GitHub repository is the published deliverable. The interactive app runs locally; there is no claimed public hosted inference URL. This is an independent assessment project, not an official Cynbit product. Company descriptions were reviewed on 29 October 2026; source pages may change.
