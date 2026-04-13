"""
Day 29 — Testing with pytest
=============================
Topics covered:
  - pytest basics: test functions, assertions
  - pytest.raises for exception testing
  - Fixtures (@pytest.fixture, tmp_path, capsys)
  - Parametrize (@pytest.mark.parametrize)
  - Mocking (unittest.mock.patch, MagicMock)
  - Testing patterns for ML-style code

Run this file with: pytest day-29/app.py -v

NOTE: This file IS the test file. All functions prefixed test_ are run by pytest.
"""

# =============================================================================
# CODE UNDER TEST — functions we want to test
# =============================================================================

import json
import math
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


# --- Pure functions (easiest to test) ---

def tokenize(text: str) -> list[str]:
    """Split text into lowercase tokens, removing empty strings."""
    return [t for t in text.lower().split() if t]

def word_count(tokens: list[str]) -> dict[str, int]:
    """Count occurrences of each token."""
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts

def top_k(counts: dict[str, int], k: int) -> list[tuple[str, int]]:
    """Return the k most frequent tokens as (token, count) pairs."""
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:k]

def normalize_score(score: float) -> float:
    """Clamp a score to [0, 1]."""
    return max(0.0, min(1.0, score))


# --- Class under test ---

@dataclass
class TextClassifier:
    labels: list[str]
    threshold: float = 0.5

    def predict(self, text: str) -> Optional[str]:
        """Return label if any label word appears in text, else None."""
        text_lower = text.lower()
        for label in self.labels:
            if label.lower() in text_lower:
                return label
        return None

    def predict_batch(self, texts: list[str]) -> list[Optional[str]]:
        return [self.predict(t) for t in texts]

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str) -> "TextClassifier":
        return cls(**json.loads(data))


# --- Function that reads/writes files ---

def save_results(results: list[dict], output_path: Path) -> int:
    """Save results as JSONL. Returns number of records written."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for record in results:
            f.write(json.dumps(record) + "\n")
            count += 1
    return count

def load_results(input_path: Path) -> list[dict]:
    """Load JSONL file into a list of dicts."""
    with open(input_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# =============================================================================
# SECTION 1: Basic Test Functions
# =============================================================================

def test_tokenize_basic():
    assert tokenize("Hello World") == ["hello", "world"]

def test_tokenize_extra_spaces():
    assert tokenize("  hello   world  ") == ["hello", "world"]

def test_tokenize_empty_string():
    assert tokenize("") == []

def test_tokenize_single_word():
    assert tokenize("Python") == ["python"]

def test_word_count_single_word():
    assert word_count(["hello"]) == {"hello": 1}

def test_word_count_repeated():
    tokens = ["the", "cat", "sat", "on", "the", "mat", "the"]
    counts = word_count(tokens)
    assert counts["the"] == 3
    assert counts["cat"] == 1

def test_word_count_empty():
    assert word_count([]) == {}

def test_top_k_returns_correct_count():
    counts = {"a": 3, "b": 1, "c": 5, "d": 2}
    result = top_k(counts, k=2)
    assert len(result) == 2

def test_top_k_sorted_by_frequency():
    counts = {"a": 3, "b": 1, "c": 5}
    result = top_k(counts, k=3)
    assert result[0] == ("c", 5)
    assert result[1] == ("a", 3)

def test_normalize_score_clamps_above_one():
    assert normalize_score(1.5) == 1.0

def test_normalize_score_clamps_below_zero():
    assert normalize_score(-0.3) == 0.0

def test_normalize_score_midpoint():
    assert normalize_score(0.7) == 0.7

def test_normalize_score_boundaries():
    assert normalize_score(0.0) == 0.0
    assert normalize_score(1.0) == 1.0


# =============================================================================
# SECTION 2: Testing Exceptions with pytest.raises
# =============================================================================
import pytest

def test_top_k_raises_on_zero_k():
    with pytest.raises(ValueError, match="k must be positive"):
        top_k({"a": 1}, k=0)

def test_top_k_raises_on_negative_k():
    with pytest.raises(ValueError):
        top_k({"a": 1}, k=-5)

def test_load_results_raises_on_missing_file():
    with pytest.raises(FileNotFoundError):
        load_results(Path("/nonexistent/path/file.jsonl"))


# =============================================================================
# SECTION 3: Parametrize — test many inputs with one function
# =============================================================================

@pytest.mark.parametrize("text,expected", [
    ("Hello World", ["hello", "world"]),
    ("UPPER CASE", ["upper", "case"]),
    ("  spaces  ", ["spaces"]),
    ("one", ["one"]),
    ("", []),
])
def test_tokenize_parametrized(text, expected):
    assert tokenize(text) == expected


@pytest.mark.parametrize("score,expected", [
    (0.5, 0.5),
    (1.5, 1.0),
    (-0.5, 0.0),
    (0.0, 0.0),
    (1.0, 1.0),
    (99.9, 1.0),
])
def test_normalize_score_parametrized(score, expected):
    assert normalize_score(score) == pytest.approx(expected)


# =============================================================================
# SECTION 4: Fixtures — shared, reusable setup
# =============================================================================

@pytest.fixture
def sample_classifier():
    """Shared TextClassifier instance for tests below."""
    return TextClassifier(labels=["positive", "negative", "neutral"])

@pytest.fixture
def sample_texts():
    return [
        "This is a positive review",
        "Very negative experience",
        "The product is neutral overall",
        "Random text with no label",
    ]

def test_classifier_predict_positive(sample_classifier):
    assert sample_classifier.predict("This is a positive review") == "positive"

def test_classifier_predict_none_for_unknown(sample_classifier):
    assert sample_classifier.predict("random words here") is None

def test_classifier_predict_batch(sample_classifier, sample_texts):
    results = sample_classifier.predict_batch(sample_texts)
    assert results[0] == "positive"
    assert results[1] == "negative"
    assert results[3] is None

def test_classifier_serialization_roundtrip(sample_classifier):
    """Serialized and deserialized classifier should behave the same."""
    json_str = sample_classifier.to_json()
    restored = TextClassifier.from_json(json_str)
    assert restored.labels == sample_classifier.labels
    assert restored.threshold == sample_classifier.threshold
    assert restored.predict("positive outcome") == "positive"


# =============================================================================
# SECTION 5: tmp_path Fixture — safe file I/O tests
# =============================================================================

def test_save_and_load_results(tmp_path):
    """Use tmp_path to get a temp directory — cleaned up after test."""
    output = tmp_path / "results" / "out.jsonl"
    data = [
        {"text": "hello", "label": "positive", "score": 0.9},
        {"text": "goodbye", "label": "negative", "score": 0.2},
    ]

    count = save_results(data, output)
    assert count == 2
    assert output.exists()

    loaded = load_results(output)
    assert len(loaded) == 2
    assert loaded[0]["text"] == "hello"
    assert loaded[1]["label"] == "negative"

def test_save_results_creates_parent_dirs(tmp_path):
    output = tmp_path / "deeply" / "nested" / "dir" / "out.jsonl"
    save_results([{"x": 1}], output)
    assert output.exists()


# =============================================================================
# SECTION 6: Mocking — replace dependencies for isolation
# =============================================================================
from unittest.mock import patch, MagicMock

# Suppose this function calls an external API
def fetch_model_score(text: str, api_url: str) -> float:
    """In production, calls an HTTP API. In tests, we mock this."""
    import urllib.request
    with urllib.request.urlopen(api_url) as resp:
        return json.loads(resp.read())["score"]

def classify_with_api(text: str, api_url: str, threshold: float = 0.5) -> str:
    score = fetch_model_score(text, api_url)
    return "positive" if score >= threshold else "negative"

def test_classify_with_api_positive():
    """Mock the HTTP call so the test never hits the network."""
    with patch("__main__.fetch_model_score") as mock_fetch:
        mock_fetch.return_value = 0.9
        result = classify_with_api("great product", "http://fake-api/score")
        assert result == "positive"
        mock_fetch.assert_called_once_with("great product", "http://fake-api/score")

def test_classify_with_api_negative():
    with patch("__main__.fetch_model_score", return_value=0.2):
        result = classify_with_api("terrible experience", "http://fake-api/score")
        assert result == "negative"

def test_mock_call_count():
    """Verify that batch processing calls the API exactly once per text."""
    texts = ["text1", "text2", "text3"]
    with patch("__main__.fetch_model_score", return_value=0.8) as mock_fetch:
        for t in texts:
            classify_with_api(t, "http://fake-api/score")
        assert mock_fetch.call_count == len(texts)


# =============================================================================
# SECTION 7: capsys — capture printed output
# =============================================================================

def report_results(predictions: list[str]) -> None:
    pos = predictions.count("positive")
    neg = predictions.count("negative")
    print(f"Positive: {pos}, Negative: {neg}")

def test_report_results_output(capsys):
    report_results(["positive", "negative", "positive", "positive"])
    captured = capsys.readouterr()
    assert "Positive: 3" in captured.out
    assert "Negative: 1" in captured.out


print("=" * 60)
print("pytest demo file — run with: pytest day-29/app.py -v")
print("All test functions start with test_")
print("=" * 60)
