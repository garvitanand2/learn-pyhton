# =============================================================
# Day 14: Week 2 Mini Project — Data Processing Script
# Goal: Apply all Week 2 data structure skills to build a
#       real-world data analysis pipeline.
#
# Project: "DataSight" — A dataset profiler that analyzes a
#           text classification dataset and generates a report.
# =============================================================

import json
import re
import time
from collections import Counter, defaultdict
from typing import Any


# ===== DATA LAYER =============================================

# Sample dataset (simulating a loaded CSV/JSON file)
DATASET = [
    {"id": 1, "text": "The model predicted results with high confidence.", "label": "positive", "source": "twitter"},
    {"id": 2, "text": "System completely failed during inference phase.", "label": "negative", "source": "reddit"},
    {"id": 3, "text": "Performance was average, nothing remarkable.", "label": "neutral", "source": "twitter"},
    {"id": 4, "text": "Absolutely stellar accuracy on all benchmarks!", "label": "positive", "source": "paper"},
    {"id": 5, "text": "Training loss diverged after 3 epochs.", "label": "negative", "source": "reddit"},
    {"id": 6, "text": "The transformer architecture shows promise.", "label": "positive", "source": "paper"},
    {"id": 7, "text": "Latency is too high for production use.", "label": "negative", "source": "twitter"},
    {"id": 8, "text": "Results are inconclusive without more data.", "label": "neutral", "source": "paper"},
    {"id": 9, "text": "Excellent generalization across multiple domains.", "label": "positive", "source": "paper"},
    {"id": 10, "text": "Memory usage is unacceptably high.", "label": "negative", "source": "reddit"},
    {"id": 11, "text": "Model requires fine-tuning for domain adaptation.", "label": "neutral", "source": "paper"},
    {"id": 12, "text": "Benchmark results are state of the art!", "label": "positive", "source": "twitter"},
    {"id": 13, "text": "Overfitting detected after epoch 5.", "label": "negative", "source": "reddit"},
    {"id": 14, "text": "The approach is interesting but unproven.", "label": "neutral", "source": "twitter"},
    {"id": 15, "text": "Achieves 97% accuracy on held-out test set.", "label": "positive", "source": "paper"},
]

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "and", "or", "but", "if",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "that",
    "this", "it", "its", "which", "during", "after", "all", "not", "too"
}


# ===== PREPROCESSING FUNCTIONS ================================

def tokenize(text: str, remove_stopwords: bool = True) -> list:
    """Tokenize text into clean tokens."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # remove punctuation
    tokens = text.split()
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOP_WORDS]
    return tokens


def compute_text_stats(text: str) -> dict:
    """Compute length statistics for a text field."""
    tokens = text.split()
    return {
        "char_count":    len(text),
        "word_count":    len(tokens),
        "avg_word_len":  round(sum(len(w) for w in tokens) / len(tokens), 2) if tokens else 0,
        "sentence_count": len(re.findall(r"[.!?]", text)) or 1,
    }


# ===== ANALYSIS FUNCTIONS =====================================

def profile_dataset(dataset: list) -> dict:
    """Generate a full profile of the dataset."""
    total = len(dataset)
    if total == 0:
        return {"error": "Empty dataset"}

    # Label distribution
    label_counts   = Counter(r["label"] for r in dataset)
    source_counts  = Counter(r["source"] for r in dataset)

    # Text statistics per record
    all_stats = [compute_text_stats(r["text"]) for r in dataset]
    char_counts  = [s["char_count"]  for s in all_stats]
    word_counts  = [s["word_count"]  for s in all_stats]

    # Global vocabulary
    all_tokens  = [t for r in dataset for t in tokenize(r["text"])]
    vocab       = set(all_tokens)
    token_freq  = Counter(all_tokens)

    # Per-label vocabulary
    label_tokens = defaultdict(list)
    for r in dataset:
        label_tokens[r["label"]].extend(tokenize(r["text"]))

    return {
        "total_records":     total,
        "label_distribution": dict(label_counts),
        "source_distribution": dict(source_counts),
        "text_stats": {
            "min_chars":   min(char_counts),
            "max_chars":   max(char_counts),
            "avg_chars":   round(sum(char_counts) / total, 1),
            "min_words":   min(word_counts),
            "max_words":   max(word_counts),
            "avg_words":   round(sum(word_counts) / total, 1),
        },
        "vocabulary": {
            "total_tokens":   len(all_tokens),
            "unique_tokens":  len(vocab),
            "top_tokens":     token_freq.most_common(10),
            "per_label_top":  {
                label: Counter(tokens).most_common(5)
                for label, tokens in label_tokens.items()
            }
        },
        "balance_score": _compute_balance(label_counts),
    }


def _compute_balance(counts: Counter) -> float:
    """
    Compute class balance score.
    1.0 = perfectly balanced, 0.0 = completely imbalanced.
    Based on ratio of min/max class count.
    """
    if not counts:
        return 0.0
    values    = list(counts.values())
    min_count = min(values)
    max_count = max(values)
    return round(min_count / max_count, 4) if max_count > 0 else 1.0


def detect_issues(dataset: list) -> list:
    """Detect potential data quality issues."""
    issues = []

    seen_texts = {}
    for r in dataset:
        text_lower = r["text"].lower().strip()

        # Duplicate texts
        if text_lower in seen_texts:
            issues.append({
                "type":  "DUPLICATE",
                "ids":   [seen_texts[text_lower], r["id"]],
                "detail": f"Duplicate text: '{r['text'][:40]}...'"
            })
        seen_texts[text_lower] = r["id"]

        # Very short text
        if len(r["text"].split()) < 3:
            issues.append({
                "type":   "SHORT",
                "id":     r["id"],
                "detail": f"Only {len(r['text'].split())} words: '{r['text']}'"
            })

        # Missing label
        if not r.get("label"):
            issues.append({
                "type":   "MISSING_LABEL",
                "id":     r["id"],
                "detail": "No label field"
            })

    return issues


def split_dataset(dataset: list, train_pct: float = 0.7, val_pct: float = 0.15) -> dict:
    """Split dataset into train/val/test, stratified by label."""
    by_label = defaultdict(list)
    for r in dataset:
        by_label[r["label"]].append(r)

    train, val, test = [], [], []
    for label, records in by_label.items():
        n     = len(records)
        t_end = int(n * train_pct)
        v_end = t_end + int(n * val_pct)
        train.extend(records[:t_end])
        val.extend(records[t_end:v_end])
        test.extend(records[v_end:])

    return {"train": train, "val": val, "test": test}


# ===== REPORT GENERATION ======================================

def print_report(profile: dict, issues: list, splits: dict) -> None:
    """Print a formatted dataset profiling report."""
    sep = "═" * 60

    print(f"\n{sep}")
    print(f"  DataSight — Dataset Profile Report")
    print(sep)

    # Overview
    print(f"\n  OVERVIEW")
    print(f"  ────────────────────────────────────")
    print(f"  Total records : {profile['total_records']}")

    # Label distribution
    print(f"\n  LABEL DISTRIBUTION")
    print(f"  ────────────────────────────────────")
    for label, count in sorted(profile["label_distribution"].items()):
        pct = count / profile["total_records"]
        bar = "█" * int(pct * 30)
        print(f"  {label:<12} {count:>3} ({pct:.1%}) {bar}")
    print(f"  Balance score : {profile['balance_score']:.4f} (1.0 = perfect)")

    # Source distribution
    print(f"\n  SOURCE DISTRIBUTION")
    print(f"  ────────────────────────────────────")
    for src, cnt in sorted(profile["source_distribution"].items()):
        print(f"  {src:<12} {cnt:>3} records")

    # Text stats
    ts = profile["text_stats"]
    print(f"\n  TEXT STATISTICS")
    print(f"  ────────────────────────────────────")
    print(f"  Chars : min={ts['min_chars']:4d}  avg={ts['avg_chars']:6.1f}  max={ts['max_chars']:4d}")
    print(f"  Words : min={ts['min_words']:4d}  avg={ts['avg_words']:6.1f}  max={ts['max_words']:4d}")

    # Vocabulary
    v = profile["vocabulary"]
    print(f"\n  VOCABULARY")
    print(f"  ────────────────────────────────────")
    print(f"  Total tokens  : {v['total_tokens']:,}")
    print(f"  Unique tokens : {v['unique_tokens']:,}")
    print(f"  Top tokens    : {', '.join(t for t, _ in v['top_tokens'][:7])}")

    # Per-label top tokens
    print(f"\n  PER-LABEL TOP TOKENS")
    print(f"  ────────────────────────────────────")
    for label, top in v["per_label_top"].items():
        tokens_str = ", ".join(f"{t}({c})" for t, c in top)
        print(f"  {label:<12}: {tokens_str}")

    # Issues
    print(f"\n  DATA QUALITY ISSUES")
    print(f"  ────────────────────────────────────")
    if not issues:
        print("  ✓ No issues detected.")
    else:
        for issue in issues:
            print(f"  ⚠ [{issue['type']}] {issue['detail']}")

    # Splits
    print(f"\n  DATASET SPLITS")
    print(f"  ────────────────────────────────────")
    for split_name, records in splits.items():
        label_dist = Counter(r["label"] for r in records)
        dist_str   = ", ".join(f"{l}:{c}" for l, c in sorted(label_dist.items()))
        print(f"  {split_name:<6} : {len(records):3d} records  [{dist_str}]")

    print(f"\n{sep}\n")


# ===== ENTRY POINT ============================================

if __name__ == "__main__":
    start = time.time()

    print("Running DataSight analysis...")

    profile = profile_dataset(DATASET)
    issues  = detect_issues(DATASET)
    splits  = split_dataset(DATASET)

    elapsed = round(time.time() - start, 4)

    print_report(profile, issues, splits)

    print(f"  Analysis completed in {elapsed}s")
    print(f"  Results saved to profile in memory (Day 16: save to JSON file)\n")
