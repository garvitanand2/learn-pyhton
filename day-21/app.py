# Day 21: Week 3 Mini Project — NLP Pipeline Engine
# ============================================================
# Project: TextFlow — A modular, streaming NLP processing pipeline
#
# Applies everything from Week 3:
#   • Modules & imports (Day 15)
#   • File I/O with JSON/CSV (Day 16)
#   • Exception handling (Day 17)
#   • OOP basics: classes, properties (Day 18)
#   • OOP advanced: inheritance, mixins (Day 19)
#   • Generators & iterators (Day 20)
# ============================================================

import re
import json
import sys
import time
from pathlib import Path
from collections import Counter, defaultdict
from abc import ABC, abstractmethod
from datetime import datetime

# ============================================================
# STAGE 1: DATA MODELS
# ============================================================

class Record:
    """Represents a single text record in the pipeline."""

    def __init__(self, record_id: int, text: str, metadata: dict | None = None):
        self.id = record_id
        self.text = text
        self.metadata: dict = metadata or {}
        self.tokens: list[str] = []
        self.label: str | None = None
        self.features: dict = {}
        self.errors: list[str] = []

    def __repr__(self) -> str:
        return f"Record(id={self.id}, len={len(self.text)}, label={self.label!r})"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "tokens": self.tokens,
            "label": self.label,
            "features": self.features,
            "metadata": self.metadata,
        }

# ============================================================
# STAGE 2: BASE PIPELINE STEP
# ============================================================

class LoggingMixin:
    """Adds minimal logging to any pipeline step."""

    def log(self, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  [{ts}] [{type(self).__name__}] {message}")


class PipelineStep(ABC, LoggingMixin):
    """Abstract base class for all pipeline stages."""

    @abstractmethod
    def process(self, record: Record) -> Record | None:
        """Transform a record. Return None to drop it from the pipeline."""
        pass

    def safe_process(self, record: Record) -> Record | None:
        """Wraps process() with error handling."""
        try:
            return self.process(record)
        except Exception as e:
            record.errors.append(f"{type(self).__name__}: {e}")
            return record  # don't drop on error, just note it


# ============================================================
# STAGE 3: CONCRETE STEPS
# ============================================================

class TextCleaner(PipelineStep):
    """Cleans raw text: strips, lowercases, removes noise."""

    def __init__(self, lowercase: bool = True, remove_urls: bool = True):
        self.lowercase = lowercase
        self.remove_urls = remove_urls

    def process(self, record: Record) -> Record:
        text = record.text.strip()
        if self.lowercase:
            text = text.lower()
        if self.remove_urls:
            text = re.sub(r"https?://\S+|www\.\S+", "<URL>", text)
        text = re.sub(r"\s+", " ", text)        # collapse whitespace
        text = re.sub(r"[^\w\s<>]", "", text)   # remove punctuation (keep tokens)
        record.text = text
        return record


class Tokenizer(PipelineStep):
    """Splits text into tokens (word-level)."""

    def __init__(self, min_length: int = 1):
        self.min_length = min_length

    def process(self, record: Record) -> Record:
        tokens = record.text.split()
        record.tokens = [t for t in tokens if len(t) >= self.min_length]
        return record


class LengthFilter(PipelineStep):
    """Drops records that are too short or too long."""

    def __init__(self, min_tokens: int = 3, max_tokens: int = 500):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens

    def process(self, record: Record) -> Record | None:
        n = len(record.tokens)
        if n < self.min_tokens:
            self.log(f"Drop record {record.id}: too short ({n} tokens)")
            return None
        if n > self.max_tokens:
            record.tokens = record.tokens[:self.max_tokens]  # truncate
        return record


class FeatureExtractor(PipelineStep):
    """Computes text features used in downstream models."""

    def process(self, record: Record) -> Record:
        tokens = record.tokens
        record.features = {
            "num_tokens": len(tokens),
            "avg_token_len": round(sum(len(t) for t in tokens) / max(len(tokens), 1), 2),
            "unique_ratio": round(len(set(tokens)) / max(len(tokens), 1), 3),
            "has_url": "<URL>" in tokens,
        }
        return record


class SentimentLabeler(PipelineStep):
    """Simple lexicon-based sentiment labeler."""

    POSITIVE = {"great", "excellent", "best", "love", "perfect", "outstanding", "fantastic"}
    NEGATIVE = {"bad", "poor", "terrible", "awful", "worst", "hate", "failed"}

    def process(self, record: Record) -> Record:
        token_set = set(record.tokens)
        pos = len(token_set & self.POSITIVE)
        neg = len(token_set & self.NEGATIVE)
        record.label = "positive" if pos > neg else ("negative" if neg > pos else "neutral")
        record.features["pos_keywords"] = pos
        record.features["neg_keywords"] = neg
        return record


# ============================================================
# STAGE 4: THE PIPELINE ENGINE
# ============================================================

class Pipeline(LoggingMixin):
    """Orchestrates steps and streams records through them."""

    def __init__(self, name: str = "TextFlow"):
        self.name = name
        self._steps: list[PipelineStep] = []
        self._stats = {"total": 0, "passed": 0, "dropped": 0, "errors": 0}

    def add_step(self, step: PipelineStep) -> "Pipeline":
        self._steps.append(step)
        return self

    def run(self, records_gen) -> list[Record]:
        """Streams records through all pipeline steps."""
        self.log(f"Starting pipeline '{self.name}' with {len(self._steps)} steps")
        results = []

        for record in records_gen:
            self._stats["total"] += 1
            current = record

            for step in self._steps:
                if current is None:
                    break
                current = step.safe_process(current)

            if current is None:
                self._stats["dropped"] += 1
            else:
                if current.errors:
                    self._stats["errors"] += 1
                self._stats["passed"] += 1
                results.append(current)

        self.log(f"Done: {self._stats}")
        return results

    def stats(self) -> dict:
        return dict(self._stats)


# ============================================================
# STAGE 5: DATA SOURCE (Generator)
# ============================================================

def generate_records(n: int = 20):
    """Simulates streaming records from a data source."""
    sample_texts = [
        "great model performance and excellent results",
        "bad training run with terrible loss divergence",
        "average baseline with some improvements",
        "best architecture we have tested so far",
        "poor memory management caused the crash",
        "",                                             # should be dropped
        "check out http://example.com for more info",
        "hi",                                           # too short
        "outstanding results achieved with this model",
        "failed to converge after 100 epochs",
        "neutral performance across all benchmarks",
        "love the simplicity of this approach",
        "awful documentation made debugging hard",
        "model weights saved successfully to disk",
        "the experiment ran perfectly without errors",
        "worst hyperparameter search in history",
        "great data augmentation improved accuracy",
        "fantastic precision on held out test set",
        "bad recall on the minority class labels",
        "excellent engineering and clean code structure",
    ]

    for i, text in enumerate(sample_texts[:n]):
        yield Record(
            record_id=i + 1,
            text=text,
            metadata={"source": "synthetic", "index": i},
        )


# ============================================================
# STAGE 6: REPORTING
# ============================================================

def print_report(records: list[Record], pipeline_stats: dict) -> None:
    """Prints a comprehensive pipeline report."""
    label_dist = Counter(r.label for r in records)
    avg_tokens = sum(r.features.get("num_tokens", 0) for r in records) / max(len(records), 1)

    print("\n" + "=" * 55)
    print(f"  TEXTFLOW PIPELINE REPORT")
    print("=" * 55)
    print(f"  Records processed:    {pipeline_stats['total']}")
    print(f"  Records passed:       {pipeline_stats['passed']}")
    print(f"  Records dropped:      {pipeline_stats['dropped']}")
    print(f"  Records with errors:  {pipeline_stats['errors']}")
    print(f"  Avg tokens (passed):  {avg_tokens:.1f}")
    print()
    print("  LABEL DISTRIBUTION:")
    for label, count in sorted(label_dist.items()):
        bar = "█" * count
        print(f"    {label:<12} {count:3d}  {bar}")
    print()
    print("  SAMPLE OUTPUTS:")
    for r in records[:5]:
        print(f"    [{r.label.upper():<10}] {r.text[:45]}")
    print("=" * 55)


# ============================================================
# MAIN
# ============================================================

def main():
    print("TextFlow NLP Pipeline Engine")
    print("-" * 40)

    # Build pipeline
    pipeline = (
        Pipeline("TextFlow-v1")
        .add_step(TextCleaner(lowercase=True, remove_urls=True))
        .add_step(Tokenizer(min_length=2))
        .add_step(LengthFilter(min_tokens=3, max_tokens=50))
        .add_step(FeatureExtractor())
        .add_step(SentimentLabeler())
    )

    # Run
    results = pipeline.run(generate_records(20))

    # Report
    print_report(results, pipeline.stats())

    # Save to JSON
    output_path = Path("outputs")
    output_path.mkdir(exist_ok=True)
    out_file = output_path / "pipeline_results.jsonl"
    with open(out_file, "w") as f:
        for r in results:
            f.write(json.dumps(r.to_dict()) + "\n")
    print(f"\n  Results saved to {out_file}")


if __name__ == "__main__":
    main()
