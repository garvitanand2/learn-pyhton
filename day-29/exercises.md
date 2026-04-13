# Day 29 Exercises — Testing with pytest

## Exercise 1: Write Tests for a Calculator Module
Given this calculator, write at least 8 tests covering normal behavior, edge cases, and exceptions.

```python
# calculator.py — code under test
from typing import Union

Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    return a + b

def subtract(a: Number, b: Number) -> Number:
    return a - b

def multiply(a: Number, b: Number) -> Number:
    return a * b

def divide(a: Number, b: Number) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def power(base: Number, exp: int) -> Number:
    if exp < 0:
        raise ValueError("Exponent must be non-negative")
    return base ** exp
```

```python
# test_calculator.py — YOUR TASK: write tests here
import pytest
# from calculator import add, subtract, multiply, divide, power

def test_add_integers():
    assert add(2, 3) == 5

# YOUR TASK: add at least 7 more tests covering:
# - subtract, multiply, divide, power
# - divide by zero raises ZeroDivisionError
# - negative exponent raises ValueError
# - float arithmetic uses pytest.approx
```

---

## Exercise 2: Parametrize a Text Classifier Test
Write a single parametrized test that checks all input-output pairs for a keyword classifier.

```python
# classifier under test
def keyword_classify(text: str, positive_words: set[str], negative_words: set[str]) -> str:
    text_lower = text.lower()
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"

POSITIVE = {"great", "excellent", "love", "good", "amazing"}
NEGATIVE = {"bad", "terrible", "hate", "awful", "poor"}
```

```python
# YOUR TASK: write a parametrized test for these cases:
# ("This is great!", "positive")
# ("Absolutely terrible service", "negative")
# ("Just okay I guess", "neutral")
# ("Great product but awful shipping", "neutral")  ← tie = neutral
# ("", "neutral")

@pytest.mark.parametrize("text,expected", [
    # fill in here
])
def test_keyword_classify(text, expected):
    assert keyword_classify(text, POSITIVE, NEGATIVE) == expected
```

---

## Exercise 3: Fixture for Shared Data
Write a `conftest.py`-style fixture (inside the test file) that provides a shared dataset and use it across multiple test functions.

```python
import pytest
import json
from pathlib import Path

@pytest.fixture
def nlp_dataset():
    """Shared dataset fixture used by multiple tests."""
    return [
        {"text": "The model achieved high accuracy", "label": "positive"},
        {"text": "Training loss diverged after epoch 3", "label": "negative"},
        {"text": "Results were within expected range", "label": "neutral"},
    ]

# YOUR TASK: write these three tests, all using the fixture:

def test_dataset_has_three_records(nlp_dataset):
    assert len(nlp_dataset) == 3

def test_all_records_have_required_keys(nlp_dataset):
    for record in nlp_dataset:
        assert "text" in record
        assert "label" in record

def test_labels_are_valid(nlp_dataset):
    valid_labels = {"positive", "negative", "neutral"}
    for record in nlp_dataset:
        assert record["label"] in valid_labels
```

---

## Exercise 4: Mock an External API Call
The `SentimentAPI` class below calls a real HTTP endpoint. Write tests that mock the network call and verify behavior for both high-score (positive) and low-score (negative) responses.

```python
from unittest.mock import patch, MagicMock

class SentimentAPI:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_score(self, text: str) -> float:
        import urllib.request, json
        url = f"{self.api_url}?text={urllib.parse.quote(text)}"
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())["score"]

    def classify(self, text: str) -> str:
        score = self.get_score(text)
        return "positive" if score >= 0.5 else "negative"

# YOUR TASK: write two tests:
# 1. test_classify_returns_positive when get_score mocked to return 0.85
# 2. test_classify_returns_negative when get_score mocked to return 0.2
# 3. Bonus: assert get_score was called exactly once in each test

def test_classify_returns_positive():
    api = SentimentAPI("http://fake-api/sentiment")
    with patch.object(api, "get_score", return_value=0.85):
        assert api.classify("fantastic service") == "positive"

def test_classify_returns_negative():
    api = SentimentAPI("http://fake-api/sentiment")
    with patch.object(api, "get_score", return_value=0.2) as mock_score:
        result = api.classify("terrible experience")
        assert result == "negative"
        mock_score.assert_called_once_with("terrible experience")
```

---

## Exercise 5: Test File I/O with tmp_path
Write a test that saves a list of experiment results to a JSONL file in `tmp_path`, reads it back, and verifies round-trip correctness.

```python
import json
from pathlib import Path

def save_experiments(experiments: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for exp in experiments:
            f.write(json.dumps(exp) + "\n")

def load_experiments(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]

# YOUR TASK
def test_experiment_roundtrip(tmp_path):
    experiments = [
        {"id": "run-001", "model": "bert", "accuracy": 0.92},
        {"id": "run-002", "model": "roberta", "accuracy": 0.94},
    ]
    output_path = tmp_path / "results" / "experiments.jsonl"
    save_experiments(experiments, output_path)

    # Verify file exists
    assert output_path.exists()

    # Verify content
    loaded = load_experiments(output_path)
    assert len(loaded) == 2
    assert loaded[0]["id"] == "run-001"
    assert loaded[1]["accuracy"] == pytest.approx(0.94)
```

---

## Stretch Challenge: Custom Fixture with Scope
Rewrite the `nlp_dataset` fixture from Exercise 3 with `scope="module"` and add a dependent fixture `label_counts` that computes the count per label. Write a test that uses both fixtures.

```python
import pytest
from collections import Counter

@pytest.fixture(scope="module")
def nlp_dataset():
    return [
        {"text": "Great model performance", "label": "positive"},
        {"text": "Loss exploded during training", "label": "negative"},
        {"text": "Inference speed is acceptable", "label": "neutral"},
        {"text": "Excellent benchmark results", "label": "positive"},
    ]

@pytest.fixture(scope="module")
def label_counts(nlp_dataset):
    return Counter(r["label"] for r in nlp_dataset)

def test_positive_count(label_counts):
    assert label_counts["positive"] == 2

def test_all_labels_covered(label_counts):
    assert set(label_counts.keys()) == {"positive", "negative", "neutral"}
```
