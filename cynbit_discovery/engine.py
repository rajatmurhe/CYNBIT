"""Rank a reviewed catalog and prepare a brief for a human discovery call."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "catalog.json"
MIN_SCORE = 0.16
MIN_MARGIN = 0.04
MAX_CHARS = 6000


def redact_contacts(text: str) -> str:
    """Best-effort contact masking; this is not a general PII detector."""
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[email removed]", text)
    return re.sub(r"(?<!\w)\+?\d[\d ()-]{7,}\d(?!\w)", "[number removed]", text)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


class DiscoveryEngine:
    def __init__(self, catalog_path: Path = CATALOG_PATH):
        raw = catalog_path.read_bytes()
        self.catalog_version = hashlib.sha256(raw).hexdigest()[:12]
        self.catalog = json.loads(raw)
        ids = [item["id"] for item in self.catalog]
        if len(ids) != len(set(ids)) or len(ids) < 2:
            raise ValueError("Catalog must have at least two distinct entries.")
        documents = [
            f"{item['title']} {item['summary']} {item['search_terms']}" for item in self.catalog
        ]
        self.words = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.chars = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
        self.word_matrix = self.words.fit_transform(documents)
        self.char_matrix = self.chars.fit_transform(documents)

    def rank(self, text: str, *, word_only: bool = False) -> list[dict]:
        query = normalize(redact_contacts(text))
        word_query = self.words.transform([query])
        word_scores = cosine_similarity(word_query, self.word_matrix).ravel()
        char_scores = cosine_similarity(self.chars.transform([query]), self.char_matrix).ravel()
        scores = word_scores if word_only else 0.8 * word_scores + 0.2 * char_scores
        order = np.argsort(-scores, kind="stable")
        terms = self.words.get_feature_names_out()
        matches = []
        for index in order:
            overlap = self.word_matrix[index].multiply(word_query).tocoo()
            contributions = sorted(
                zip(overlap.col, overlap.data), key=lambda pair: pair[1], reverse=True
            )
            matches.append(
                {
                    **self.catalog[index],
                    "score": round(float(scores[index]), 6),
                    "matched_terms": [str(terms[col]) for col, _ in contributions[:6]],
                }
            )
        return matches

    def analyze(self, text: str, *, word_only: bool = False) -> dict:
        if not isinstance(text, str):
            raise ValueError("Enter a text brief.")
        if len(text) > MAX_CHARS:
            raise ValueError(f"Keep the brief within {MAX_CHARS:,} characters.")
        clean = redact_contacts(text.strip())
        if len(re.findall(r"\b\w+\b", clean)) < 3:
            raise ValueError("Add at least three words describing what you need.")
        ranked = self.rank(clean, word_only=word_only)
        top, second = ranked[:2]
        margin = round(top["score"] - second["score"], 6)
        if top["score"] < MIN_SCORE:
            status = "needs_context"
            reason = "The catalog does not provide a strong enough match. Ask for more context."
            selected = []
        elif margin < MIN_MARGIN:
            status = "needs_review"
            reason = "Two routes score closely. A reviewer should clarify the main requirement."
            selected = ranked[:2]
        else:
            status = "suggested"
            reason = "One route has a clearer vocabulary match. Confirm its fit during discovery."
            selected = ranked[:1]
        questions = []
        if status == "needs_context":
            questions = [
                "What business problem or learning goal are you trying to address?",
                "What does the current process look like?",
                "What outcome would make this project worthwhile?",
            ]
        else:
            if status == "needs_review":
                questions.append("Which requirement is the main priority for the first discussion?")
            for item in selected:
                questions.extend(item["questions"][:2] if len(selected) > 1 else item["questions"])
        questions.extend(
            [
                "What budget range and target date should the team plan around?",
                "Who will confirm the requirements and approve the next step?",
            ]
        )
        warnings = [
            "Review required before sharing. No price, delivery date or eligibility is confirmed.",
            "Contact masking is partial; names, addresses and other sensitive details may remain.",
        ]
        if re.search(r"ignore.*instructions|system prompt|reveal.*secret", clean, re.I):
            warnings.append("Instruction-like text detected. Treat the brief as untrusted input.")
        return {
            "status": status,
            "reason": reason,
            "brief": clean,
            "suggested_route": top["id"] if status == "suggested" else None,
            "candidates": ranked[:3],
            "score_margin": margin,
            "questions": questions,
            "next_step": (
                top["next_step"]
                if status == "suggested"
                else "A team member should clarify the request before choosing a route."
            ),
            "warnings": warnings,
            "catalog_version": self.catalog_version,
            "method": "word_tfidf" if word_only else "word_char_tfidf",
            "thresholds": {"minimum_score": MIN_SCORE, "minimum_margin": MIN_MARGIN},
        }


def render_markdown(result: dict) -> str:
    """Export plain text fields without allowing an inquiry to inject Markdown links."""

    def plain(value: str) -> str:
        return re.sub(r"([\\`*_{}\[\]()<>#+.!|~-])", r"\\\1", value)

    lines = [
        "# Discovery brief",
        "",
        "Draft for human review",
        "",
        "## Inquiry",
        "",
        plain(result["brief"]),
        "",
        "## Routing decision",
        "",
        plain(result["reason"]),
        "",
        f"Status: {result['status']}",
        "",
    ]
    if result["status"] != "needs_context":
        lines.extend(["## Catalog matches", ""])
        for match in result["candidates"]:
            lines.append(
                f"- **{match['title']}** — similarity {match['score']:.3f}. "
                f"[Source]({match['source_url']}); section: {match['source_section']}."
            )
        lines.extend(["", "Similarity is not a probability of fit.", ""])
    lines.extend(["## Questions for discovery", ""])
    lines.extend(f"- {question}" for question in result["questions"])
    lines.extend(["", "## Next step", "", result["next_step"], "", "## Review notes", ""])
    lines.extend(f"- {warning}" for warning in result["warnings"])
    lines.extend(["", f"Catalog version: `{result['catalog_version']}`", ""])
    return "\n".join(lines)
