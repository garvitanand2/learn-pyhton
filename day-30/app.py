"""
Day 30 — Final Project: SentimentFlow
======================================
A complete end-to-end CLI text analysis pipeline combining all 29 days:

  Day 15 — Modules & stdlib (pathlib, json, collections)
  Day 16 — File I/O (JSONL, CSV)
  Day 17 — Exception handling (custom hierarchy, retry)
  Day 18 — OOP basics (classes, properties, classmethods)
  Day 19 — OOP advanced (inheritance, mixins, Protocol)
  Day 20 — Generators (streaming data source)
  Day 22 — Decorators (timer, retry, lru_cache)
  Day 23 — Context managers (Timer, open)
  Day 24 — Functional tools (map, filter, functools)
  Day 25 — JSON (config, results, serialization)
  Day 27 — Performance (lru_cache, set lookup, join)
  Day 28 — Type hints & dataclasses
  Day 29 — Testable design (pure functions, dependency injection)

Usage:
  python day-30/app.py                   # uses built-in demo data
  python day-30/app.py --input texts.txt # one text per line
  python day-30/app.py --output results.jsonl

Architecture:
  Config (dataclass) → DataSource (generator) → Pipeline (OOP)
    → [Cleaner, Tokenizer, FeatureExtractor, Labeler] steps
    → Reporter → JSONL output
"""

from __future__ import annotations

import json
import sys
import time
import argparse
import functools
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterator, Optional, Protocol, Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VERSION: Final[str] = "1.0.0"
DEFAULT_OUTPUT: Final[str] = "sentimentflow_results.jsonl"


# =============================================================================
# CUSTOM EXCEPTIONS  (Day 17)
# =============================================================================
class PipelineError(Exception):
    """Base error for all SentimentFlow pipeline errors."""

class ConfigError(PipelineError):
    """Raised when configuration is invalid."""

class StepError(PipelineError):
    """Raised when a pipeline step fails irrecoverably."""
    def __init__(self, step_name: str, message: str):
        super().__init__(f"[{step_name}] {message}")
        self.step_name = step_name


# =============================================================================
# CONFIGURATION  (Day 28: dataclass + TypedDict + validation)
# =============================================================================
@dataclass
class PipelineConfig:
    """Immutable pipeline configuration loaded from JSON."""
    min_token_count: int = 2
    max_token_count: int = 500
    positive_words_file: Optional[str] = None
    negative_words_file: Optional[str] = None
    output_path: str = DEFAULT_OUTPUT
    batch_size: int = 64
    verbose: bool = False

    def __post_init__(self):
        if self.min_token_count < 1:
            raise ConfigError("min_token_count must be >= 1")
        if self.max_token_count < self.min_token_count:
            raise ConfigError("max_token_count must be >= min_token_count")
        if self.batch_size < 1:
            raise ConfigError("batch_size must be >= 1")

    @classmethod
    def from_json(cls, path: str) -> "PipelineConfig":
        """Load config from a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


# =============================================================================
# DECORATORS  (Day 22)
# =============================================================================
def timer(fn):
    """Log execution time of any function."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  ⏱  {fn.__name__} completed in {elapsed*1000:.1f}ms")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 0.1):
    """Retry a function up to max_attempts times on exception."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc  # type: ignore
        return wrapper
    return decorator


# =============================================================================
# DATA RECORD  (Day 28: dataclass)
# =============================================================================
@dataclass
class TextRecord:
    """Represents one text item flowing through the pipeline."""
    record_id: int
    raw_text: str
    cleaned_text: str = ""
    tokens: list[str] = field(default_factory=list)
    features: dict[str, object] = field(default_factory=dict)
    label: Optional[str] = None
    score: float = 0.0
    skipped: bool = False
    skip_reason: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        # Keep JSON output compact — omit empty fields
        return {k: v for k, v in d.items() if v or v == 0}


# =============================================================================
# LOGGING MIXIN  (Day 19)
# =============================================================================
class LoggingMixin:
    def log(self, message: str, level: str = "INFO") -> None:
        ts = time.strftime("%H:%M:%S")
        print(f"[{ts}] [{level}] [{self.__class__.__name__}] {message}")


# =============================================================================
# PIPELINE STEP ABC  (Day 19 + Day 18)
# =============================================================================
class PipelineStep(ABC):
    """Base class for all pipeline stages."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self._processed = 0
        self._skipped = 0

    @abstractmethod
    def _process(self, record: TextRecord) -> TextRecord:
        """Core processing logic — implement in subclasses."""
        ...

    def process(self, record: TextRecord) -> TextRecord:
        """Safe wrapper: skip already-skipped records, catch errors."""
        if record.skipped:
            return record
        try:
            result = self._process(record)
            self._processed += 1
            return result
        except Exception as exc:
            record.skipped = True
            record.skip_reason = f"{self.__class__.__name__}: {exc}"
            self._skipped += 1
            return record

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def stats(self) -> dict[str, int]:
        return {"processed": self._processed, "skipped": self._skipped}


# =============================================================================
# PIPELINE STEPS  (Day 19: inheritance)
# =============================================================================

class TextCleaner(PipelineStep):
    """Remove non-alphanumeric characters and normalize whitespace."""

    def _process(self, record: TextRecord) -> TextRecord:
        text = record.raw_text.strip()
        cleaned = " ".join(
            ch if ch.isalnum() or ch == " " else " "
            for ch in text
        )
        record.cleaned_text = " ".join(cleaned.split())
        if not record.cleaned_text:
            record.skipped = True
            record.skip_reason = "empty after cleaning"
        return record


class Tokenizer(PipelineStep):
    """Split cleaned text into lowercase tokens."""

    @functools.lru_cache(maxsize=1024)
    def _tokenize_cached(self, text: str) -> tuple[str, ...]:
        """Cache tokenization for repeated text using lru_cache (Day 27)."""
        return tuple(text.lower().split())

    def _process(self, record: TextRecord) -> TextRecord:
        record.tokens = list(self._tokenize_cached(record.cleaned_text))
        n = len(record.tokens)
        if n < self.config.min_token_count:
            record.skipped = True
            record.skip_reason = f"too short ({n} tokens < {self.config.min_token_count})"
        elif n > self.config.max_token_count:
            record.tokens = record.tokens[: self.config.max_token_count]
        return record


class FeatureExtractor(PipelineStep):
    """Extract lightweight features from token list."""

    def _process(self, record: TextRecord) -> TextRecord:
        tokens = record.tokens
        text = record.cleaned_text.lower()
        record.features = {
            "token_count": len(tokens),
            "unique_tokens": len(set(tokens)),
            "char_count": len(text),
            "avg_token_len": (
                sum(len(t) for t in tokens) / len(tokens) if tokens else 0.0
            ),
            "has_numbers": any(t.isdigit() for t in tokens),
            "type_token_ratio": (
                round(len(set(tokens)) / len(tokens), 3) if tokens else 0.0
            ),
        }
        return record


class SentimentLabeler(PipelineStep, LoggingMixin):
    """
    Keyword-based sentiment labeler.
    Assigns 'positive', 'negative', or 'neutral' based on word overlap.
    """

    POSITIVE_WORDS: Final = frozenset({
        "great", "excellent", "amazing", "good", "fantastic", "wonderful",
        "outstanding", "superb", "brilliant", "love", "best", "perfect",
        "impressive", "recommend", "happy", "satisfied", "fast", "clean",
        "helpful", "efficient", "accurate", "reliable", "easy", "simple",
    })

    NEGATIVE_WORDS: Final = frozenset({
        "bad", "terrible", "awful", "poor", "horrible", "worst", "hate",
        "disappoint", "slow", "broken", "difficult", "confusing", "useless",
        "failed", "error", "bug", "crash", "miss", "wrong", "expensive",
        "frustrating", "annoying", "ugly", "complex", "incomplete",
    })

    def _process(self, record: TextRecord) -> TextRecord:
        token_set = set(record.tokens)
        pos_hits = len(token_set & self.POSITIVE_WORDS)
        neg_hits = len(token_set & self.NEGATIVE_WORDS)
        total = pos_hits + neg_hits

        if total == 0:
            record.label = "neutral"
            record.score = 0.5
        else:
            raw_score = pos_hits / total
            record.score = round(raw_score, 3)
            if raw_score >= 0.6:
                record.label = "positive"
            elif raw_score <= 0.4:
                record.label = "negative"
            else:
                record.label = "neutral"

        return record


# =============================================================================
# PIPELINE ENGINE  (Day 21 pattern)
# =============================================================================
class Pipeline(LoggingMixin):
    """Chains multiple PipelineStep instances and processes a stream of records."""

    def __init__(self, steps: list[PipelineStep], config: PipelineConfig):
        self.steps = steps
        self.config = config

    def run(self, records: Iterator[TextRecord]) -> list[TextRecord]:
        """Process all records through every step sequentially."""
        self.log(f"Starting pipeline with {len(self.steps)} steps")
        results: list[TextRecord] = []

        for record in records:
            for step in self.steps:
                record = step.process(record)
            results.append(record)

        return results

    @property
    def step_stats(self) -> dict[str, dict[str, int]]:
        return {step.name: step.stats for step in self.steps}


# =============================================================================
# DATA SOURCE  (Day 20: generator)
# =============================================================================
def stream_from_list(texts: list[str]) -> Iterator[TextRecord]:
    """Generate TextRecord objects from an in-memory list."""
    for idx, text in enumerate(texts, start=1):
        yield TextRecord(record_id=idx, raw_text=text)


def stream_from_file(path: Path) -> Iterator[TextRecord]:
    """Generate TextRecord objects by streaming a text file line by line."""
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if line:
                yield TextRecord(record_id=idx, raw_text=line)


# =============================================================================
# REPORTER  (pure function — Day 24 functional style)
# =============================================================================
@timer
def save_jsonl(records: list[TextRecord], output_path: Path) -> int:
    """Save processed records as JSONL. Returns count written."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    successful = [r for r in records if not r.skipped]
    with open(output_path, "w", encoding="utf-8") as f:
        for record in successful:
            f.write(json.dumps(record.to_dict()) + "\n")
    return len(successful)


def print_report(records: list[TextRecord], step_stats: dict) -> None:
    """Pretty-print a summary of the pipeline run to stdout."""
    total = len(records)
    skipped = sum(1 for r in records if r.skipped)
    processed = total - skipped

    label_counts = Counter(
        r.label for r in records if not r.skipped and r.label
    )
    avg_score_by_label: dict[str, float] = {}
    for label in label_counts:
        scores = [r.score for r in records if not r.skipped and r.label == label]
        avg_score_by_label[label] = round(sum(scores) / len(scores), 3) if scores else 0.0

    print("\n" + "=" * 60)
    print(f"  SentimentFlow v{VERSION} — Run Complete")
    print("=" * 60)
    print(f"  Total records   : {total}")
    print(f"  Processed       : {processed}")
    print(f"  Skipped         : {skipped}")
    print()
    print("  Label Distribution:")
    for label, count in sorted(label_counts.items(), key=lambda kv: kv[1], reverse=True):
        bar_len = int(count / max(label_counts.values()) * 30)
        bar = "█" * bar_len
        pct = count / processed * 100 if processed else 0
        avg = avg_score_by_label[label]
        print(f"    {label:<10} {bar:<32} {count:>4} ({pct:.1f}%)  avg_score={avg}")

    print()
    print("  Step Statistics:")
    for step_name, stats in step_stats.items():
        print(f"    {step_name:<22} processed={stats['processed']:>4}  skipped={stats['skipped']:>3}")
    print("=" * 60)


# =============================================================================
# DEMO DATA
# =============================================================================
DEMO_TEXTS = [
    "The model achieved excellent accuracy on all benchmark datasets.",
    "Training failed with a CUDA out of memory error again.",
    "Simple and efficient architecture, highly recommend it.",
    "Terrible documentation and confusing setup process.",
    "The embeddings look reasonable after fine tuning.",
    "Slow inference speed makes it unusable for production.",
    "Amazing results with minimal code changes required.",
    "Found a critical bug in the data preprocessing pipeline.",
    "The API is clean and easy to integrate with existing systems.",
    "Complex configuration file with missing required parameters.",
    "Outstanding performance on the NER evaluation benchmark.",
    "The model keeps crashing during the validation phase.",
    "Fast and reliable, works perfectly for our use case.",
    "Gradients exploded after epoch 5, frustrating experience.",
    "Beautiful visualizations and comprehensive logging support.",
    "The tokenizer is broken for non-English input texts.",
    "Lightweight and simple architecture without compromising accuracy.",
    "Poor error messages make debugging extremely difficult.",
    "Impressive zero-shot performance across multiple languages.",
    "Dataset loading is incomplete and missing important samples.",
    "I",           # too short — will be filtered
    "",            # empty — will be filtered
    "The",         # too short
]


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
@timer
def run_pipeline(texts: list[str], config: PipelineConfig) -> list[TextRecord]:
    """Build and run the full pipeline."""
    steps: list[PipelineStep] = [
        TextCleaner(config),
        Tokenizer(config),
        FeatureExtractor(config),
        SentimentLabeler(config),
    ]
    pipeline = Pipeline(steps, config)
    source = stream_from_list(texts)
    results = pipeline.run(source)
    return results, pipeline.step_stats


def main():
    parser = argparse.ArgumentParser(description="SentimentFlow — NLP Analysis Pipeline")
    parser.add_argument("--input",   type=str, help="Path to input text file (one text per line)")
    parser.add_argument("--output",  type=str, default=DEFAULT_OUTPUT, help="Output JSONL path")
    parser.add_argument("--min-tokens", type=int, default=2)
    parser.add_argument("--max-tokens", type=int, default=500)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    try:
        config = PipelineConfig(
            min_token_count=args.min_tokens,
            max_token_count=args.max_tokens,
            output_path=args.output,
            verbose=args.verbose,
        )
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    # Load texts
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Input file not found: {input_path}", file=sys.stderr)
            sys.exit(1)
        texts = list(input_path.read_text(encoding="utf-8").splitlines())
    else:
        print(f"No --input provided. Using {len(DEMO_TEXTS)} demo texts.")
        texts = DEMO_TEXTS

    # Run
    records, step_stats = run_pipeline(texts, config)

    # Report
    print_report(records, step_stats)

    # Save
    output_path = Path(config.output_path)
    count = save_jsonl(records, output_path)
    print(f"\n  Results saved: {output_path} ({count} records)")


if __name__ == "__main__":
    main()
