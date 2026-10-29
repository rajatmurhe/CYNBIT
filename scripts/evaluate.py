"""Compare the retrieval variants against a fixed, synthetic challenge set."""

import argparse
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import sklearn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cynbit_discovery.engine import ROOT, DiscoveryEngine  # noqa: E402


def evaluate(cases, engine, word_only):
    rows = []
    latencies = []
    for case in cases:
        started = perf_counter()
        result = engine.analyze(case["text"], word_only=word_only)
        latencies.append((perf_counter() - started) * 1000)
        expected = case["expected_routes"]
        top_ids = [item["id"] for item in result["candidates"]]
        rows.append(
            {
                "id": case["id"],
                "text": case["text"],
                "expected_routes": expected,
                "expected_behavior": case["expected_behavior"],
                "top_route": top_ids[0],
                "suggested_route": result["suggested_route"],
                "status": result["status"],
                "score": result["candidates"][0]["score"],
                "margin": result["score_margin"],
                "top1_correct": top_ids[0] in expected if expected else None,
                "top3_hit": bool(set(top_ids) & set(expected)) if expected else None,
                "behavior_correct": (
                    result["status"] == "needs_context"
                    if case["expected_behavior"] == "abstain"
                    else result["status"] != "suggested"
                    if case["expected_behavior"] == "review"
                    else result["suggested_route"] in expected
                ),
            }
        )
    in_scope = [row for row in rows if row["expected_routes"]]
    suggested = [row for row in rows if row["status"] == "suggested"]
    ood = [row for row in rows if row["expected_behavior"] == "abstain"]

    def safe_div(total, count):
        return round(total / count, 4) if count else None

    metrics = {
        "cases": len(rows),
        "in_scope_cases": len(in_scope),
        "top1_accuracy_in_scope": safe_div(sum(r["top1_correct"] for r in in_scope), len(in_scope)),
        "top3_hit_rate_in_scope": safe_div(sum(r["top3_hit"] for r in in_scope), len(in_scope)),
        "suggestion_coverage": safe_div(len(suggested), len(rows)),
        "suggestion_precision": safe_div(
            sum(r["suggested_route"] in r["expected_routes"] for r in suggested), len(suggested)
        ),
        "out_of_scope_abstention_rate": safe_div(
            sum(r["status"] == "needs_context" for r in ood), len(ood)
        ),
        "behavior_accuracy": safe_div(sum(r["behavior_correct"] for r in rows), len(rows)),
        "p50_latency_ms": round(sorted(latencies)[len(latencies) // 2], 3),
        "p95_latency_ms": round(sorted(latencies)[int((len(latencies) - 1) * 0.95)], 3),
    }
    return {"metrics": metrics, "cases": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=ROOT / "data/evaluation_cases.json")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/evaluation.json")
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text())
    engine = DiscoveryEngine()
    report = {
        "dataset": args.cases.name,
        "data_type": "synthetic; no customer validation",
        "catalog_version": engine.catalog_version,
        "environment": {"python": platform.python_version(), "sklearn": sklearn.__version__},
        "word_only": evaluate(cases, engine, True),
        "word_char": evaluate(cases, engine, False),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key]["metrics"] for key in ("word_only", "word_char")}, indent=2))


if __name__ == "__main__":
    main()
