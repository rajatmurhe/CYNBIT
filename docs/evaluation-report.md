# Evaluation Report

**Run date:** 29 October 2026 · **Data:** 40 synthetic inquiries, not customer traffic

## Reproduce

```bash
python scripts/evaluate.py
```

The command writes `docs/evaluation.json`, including every expected label, predicted route, decision status, score and margin. It compares word-only TF-IDF with the combined word/character version. Both use the same catalog and thresholds. The catalog fingerprint and Python/scikit-learn versions are included in the output.

## Results

| Metric | Word-only baseline | Word + character |
| --- | ---: | ---: |
| In-scope top-1 accuracy | 31/32 (96.88%) | 31/32 (96.88%) |
| In-scope top-3 hit rate | 31/32 (96.88%) | 32/32 (100%) |
| Suggestion precision | 29/30 (96.67%) | 29/30 (96.67%) |
| Suggestion coverage | 30/40 (75%) | 30/40 (75%) |
| Unsupported-request abstention | 7/8 (87.5%) | 7/8 (87.5%) |
| Expected behavior achieved | 36/40 (90%) | 36/40 (90%) |
| Local p50 latency | 1.149 ms | 1.086 ms |
| Local p95 latency | 1.750 ms | 1.126 ms |

The character features recovered one acceptable route in the top three, but did not improve suggestion decisions on this set. This does not establish superiority over the simpler baseline. The demo retains the combined model as an inspectable experiment; a real pilot should choose based on independent data and complexity costs.

Latency is for sequential `analyze` calls after catalog fitting, using Python 3.11.4 on the local development machine. It excludes Python startup, model fitting, network transport, UI rendering and concurrent load. p50 is the sorted middle observation; p95 is the value at zero-based index `floor((n−1) × 0.95)`. Tiny differences are not meaningful speed claims. Dependency details are in `requirements-lock.txt`.

## What the metrics mean

**Top-1 accuracy** checks whether the highest-ranked catalog entry is in the acceptable label set for an in-scope request, even if the system abstains. **Top-3 hit rate** requires at least one acceptable route among the leading three; it does not require all intents to be found.

**Suggestion precision** counts correct single-route suggestions divided by all suggestions. **Coverage** is the fraction receiving a suggestion. Mixed-intent cases accept either listed route for retrieval accuracy, but their expected behavior is review; this is why routing accuracy alone can conceal an operational failure.

**Abstention rate** measures how often unsupported cases return `needs_context`. **Behavior accuracy** is stricter: ordinary requests must suggest an acceptable route, mixed requests must avoid a single-route suggestion, and unsupported requests must request context.

## Failure analysis

| Case | Observed behavior | Why it matters | Next experiment |
| --- | --- | --- | --- |
| eval-31: AWS hosting plus SEO | Suggests marketing; misses the need to review both intents | A score margin is not a reliable multi-intent detector | Clause-level retrieval and a multi-label review policy |
| eval-34: several spelling errors | Correct route ranks first, but score falls below the threshold | Cautious fallback reduces useful coverage | Compare spelling normalization and embeddings on new misspellings |
| eval-36: indirect local-discovery request | Asks for context; wrong route ranks first | Shared vocabulary is insufficient for paraphrases | Semantic retrieval with a paraphrase-heavy evaluation set |
| eval-39: legal contract about hosting | Suggests cloud infrastructure | Domain words can overwhelm unsupported intent | Explicit unsupported-intent examples and a separately evaluated rejection stage |

One Hinglish example and one negation example pass; that is not enough to claim multilingual or negation support. Instruction-like text cannot execute actions because there is no agent/tool execution path, but an adversarial inquiry can still distort routing.

## Limits and next validation

The 40 cases were authored in the same project as the catalog and contain many obvious vocabulary matches. They were written before the first challenge run, and the model and thresholds were not retuned afterward. They are still not independent or representative of real traffic. The eight development cases are separate, but also synthetic. No confidence interval or population-level accuracy claim is warranted from this sample design.

Before rollout, collect a consented and de-identified sample, have two reviewers adjudicate ambiguous labels, remove near duplicates, and reserve a time-separated holdout. Tune rejection thresholds on development data only. Report performance by route, language, ambiguity and request length. Evaluate reviewer corrections and net handling time, not just model scores.
