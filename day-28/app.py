"""
Day 28 — Clean Python: Type Hints & Dataclasses
================================================
Topics covered:
  - Type hints: basic, container, Optional, Union
  - TypeVar and generics
  - dataclasses (@dataclass, field, frozen, __post_init__, asdict/astuple)
  - Protocol for structural typing (duck typing with validation)
  - TypedDict for typed dictionaries
  - Final for constants
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict, astuple
from typing import Optional, Union, TypeVar, Protocol, Final, TypedDict, Any
from enum import Enum


# =============================================================================
# SECTION 1: Basic Type Hints
# =============================================================================
print("=" * 60)
print("SECTION 1: Basic Type Hints")
print("=" * 60)

# --- Primitives ---
def greet(name: str, times: int = 1) -> str:
    return (name + " ") * times

# --- Container types (Python 3.9+ can use list[str] directly) ---
def tokenize(text: str) -> list[str]:
    return text.lower().split()

def word_frequency(tokens: list[str]) -> dict[str, int]:
    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq

# --- Optional — a value OR None ---
def find_label(text: str, labels: dict[str, str]) -> Optional[str]:
    return labels.get(text)   # may return None

# --- Union — one of several types ---
def encode_input(x: Union[str, list[str]]) -> list[str]:
    if isinstance(x, str):
        return [x]
    return x

sample = "the quick brown fox jumps over the lazy dog"
tokens = tokenize(sample)
freq   = word_frequency(tokens)
print("Top-3 words:", sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:3])
print("encode_input('hello'):", encode_input("hello"))
print("encode_input(['a','b']):", encode_input(["a", "b"]))


# =============================================================================
# SECTION 2: TypeVar and Generic Functions
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 2: TypeVar — Generic Functions")
print("=" * 60)

T = TypeVar("T")

def first_or_default(items: list[T], default: T) -> T:
    """Return the first item, or default if the list is empty."""
    return items[0] if items else default

def batch(items: list[T], size: int) -> list[list[T]]:
    """Split a list into fixed-size batches."""
    return [items[i : i + size] for i in range(0, len(items), size)]

print("first_or_default([], 'UNK'):", first_or_default([], "UNK"))
print("first_or_default([1,2,3], 0):", first_or_default([1, 2, 3], 0))
print("batch(range(7), 3):", batch(list(range(7)), 3))


# =============================================================================
# SECTION 3: @dataclass — Structured Data Without Boilerplate
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 3: @dataclass")
print("=" * 60)

# --- Basic dataclass ---
@dataclass
class TrainingConfig:
    model_name: str
    learning_rate: float = 3e-4
    epochs: int = 10
    batch_size: int = 32
    dropout: float = 0.1

    # field with default_factory — mutable defaults MUST use field()
    tags: list[str] = field(default_factory=list)

    # __post_init__ — validation after auto-generated __init__
    def __post_init__(self):
        if not (0 < self.learning_rate < 1):
            raise ValueError(f"learning_rate must be in (0,1), got {self.learning_rate}")
        if self.epochs <= 0:
            raise ValueError("epochs must be positive")

cfg = TrainingConfig(model_name="bert-base", epochs=5, tags=["nlp", "classification"])
print("Config:", cfg)
print("Serializable?", asdict(cfg))    # dict — easy JSON export!
print("As tuple:", astuple(cfg))


# --- frozen=True — immutable dataclass (hashable!) ---
@dataclass(frozen=True)
class Vocabulary:
    tokens: tuple[str, ...]
    pad_token: str = "<PAD>"
    unk_token: str = "<UNK>"

    @property
    def size(self) -> int:
        return len(self.tokens) + 2  # +2 for special tokens

vocab = Vocabulary(tokens=("the", "cat", "sat"))
print("\nVocab size:", vocab.size)
print("Vocab hashable (can be dict key):", hash(vocab) != 0)


# --- eq=True allows comparison (auto-generated __eq__) ---
@dataclass(eq=True, order=True)  # order=True adds __lt__, __gt__, etc.
class EpochResult:
    epoch: int
    loss: float
    accuracy: float

    @property
    def score(self) -> float:
        return self.accuracy - self.loss

results = [
    EpochResult(1, 0.82, 0.71),
    EpochResult(2, 0.65, 0.79),
    EpochResult(3, 0.51, 0.85),
]
best = max(results, key=lambda r: r.accuracy)
print("\nBest epoch:", best)
print("Results sorted:", sorted(results))   # uses order=True comparison


# =============================================================================
# SECTION 4: Protocol — Structural Typing (Duck Typing + Safety)
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 4: Protocol — Structural Typing")
print("=" * 60)

class Predictor(Protocol):
    """Any class with a predict(text) method satisfies this Protocol."""
    def predict(self, text: str) -> str: ...

class RuleBasedClassifier:
    def predict(self, text: str) -> str:
        return "positive" if "good" in text else "negative"

class KeywordClassifier:
    def predict(self, text: str) -> str:
        positive_words = {"great", "excellent", "love", "good"}
        return "positive" if any(w in text.lower() for w in positive_words) else "negative"

def run_batch(model: Predictor, texts: list[str]) -> list[str]:
    """Works with ANY class that satisfies the Predictor protocol."""
    return [model.predict(t) for t in texts]

texts = ["This is great!", "Terrible experience", "Good product", "Awful service"]

for clf in [RuleBasedClassifier(), KeywordClassifier()]:
    preds = run_batch(clf, texts)
    print(f"{clf.__class__.__name__}: {preds}")


# =============================================================================
# SECTION 5: TypedDict — Typed Dictionaries
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 5: TypedDict")
print("=" * 60)

class ModelMetrics(TypedDict):
    accuracy: float
    f1_score: float
    precision: float
    recall: float

class ExperimentRecord(TypedDict):
    experiment_id: str
    model_name: str
    metrics: ModelMetrics
    notes: str

def format_metrics(record: ExperimentRecord) -> str:
    m = record["metrics"]
    return (
        f"[{record['experiment_id']}] {record['model_name']}: "
        f"acc={m['accuracy']:.3f}, f1={m['f1_score']:.3f}"
    )

exp: ExperimentRecord = {
    "experiment_id": "exp-001",
    "model_name": "bert-base-uncased",
    "metrics": {"accuracy": 0.924, "f1_score": 0.918, "precision": 0.921, "recall": 0.915},
    "notes": "Baseline experiment",
}
print(format_metrics(exp))


# =============================================================================
# SECTION 6: Final — Constants That Must Not Change
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 6: Final Constants")
print("=" * 60)

MAX_SEQUENCE_LENGTH: Final[int] = 512
DEFAULT_PAD_TOKEN: Final[str]   = "<PAD>"
SUPPORTED_TASKS: Final[list[str]] = ["classification", "ner", "summarization"]

print(f"Max sequence length: {MAX_SEQUENCE_LENGTH}")
print(f"Supported tasks: {SUPPORTED_TASKS}")

# Type checkers (mypy) will flag: MAX_SEQUENCE_LENGTH = 1024
# Python itself won't stop you at runtime — it's a convention + static analysis tool


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("SUMMARY — What You Learned Today")
print("=" * 60)
print("1. Type hints add documentation + static analysis — no runtime cost")
print("2. Optional[X] = Union[X, None] — prefer Optional for nullable values")
print("3. TypeVar enables generic functions that preserve their input types")
print("4. @dataclass auto-generates __init__, __repr__, __eq__ — minimal boilerplate")
print("5. frozen=True makes a dataclass immutable and hashable")
print("6. field(default_factory=list) avoids the mutable default argument trap")
print("7. Protocol enables duck typing with static checking — no inheritance needed")
print("8. TypedDict adds structure to plain dicts — great for config/API responses")
print("9. Final marks constants — mypy enforces no reassignment")
