# Day 29 Notes — Testing with pytest

## Why Test?

- Catch regressions: changing one function shouldn't silently break another
- Document behavior: tests describe exactly what a function should do
- Enable refactoring: tests are a safety net for cleanup
- Critical in ML: model pipelines have many silent failure modes

---

## pytest Basics

```bash
pip install pytest

pytest                          # run all tests in current project
pytest test_file.py             # run one file
pytest test_file.py -v          # verbose (show each test name)
pytest test_file.py -k "token"  # run only tests matching "token"
pytest -x                       # stop at first failure
pytest --tb=short               # shorter tracebacks
```

### Test Discovery Rules
- Files: must be named `test_*.py` or `*_test.py`
- Functions: must start with `test_`
- Classes: must start with `Test` (no `__init__`)

---

## Assertions

pytest rewrites `assert` at collection time to give rich failure messages:

```python
# All of these give helpful diffs on failure:
assert result == expected
assert result != expected
assert "key" in my_dict
assert len(items) == 3
assert x > 0
assert isinstance(obj, MyClass)

# Floating point — use approx instead of ==
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result == pytest.approx(0.9, abs=1e-3)
```

---

## pytest.raises — Test Exceptions

```python
import pytest

def test_raises_value_error():
    with pytest.raises(ValueError):
        my_function(-1)

# Match the error message with regex
def test_raises_with_message():
    with pytest.raises(ValueError, match="must be positive"):
        my_function(-1)

# Inspect the exception
def test_inspect_exception():
    with pytest.raises(KeyError) as exc_info:
        my_dict["missing"]
    assert "missing" in str(exc_info.value)
```

---

## @pytest.fixture — Reusable Setup

```python
import pytest

@pytest.fixture
def trained_model():
    """Fresh instance for each test that requests it."""
    model = TextClassifier(labels=["pos", "neg"])
    return model

# Any test function that names the fixture in its parameters gets it:
def test_predict(trained_model):
    assert trained_model.predict("positive") == "pos"

def test_batch(trained_model):
    results = trained_model.predict_batch(["positive", "negative"])
    assert len(results) == 2
```

### Fixture Scopes
| Scope | When created | When destroyed |
|-------|-------------|----------------|
| `function` (default) | before each test | after each test |
| `class` | once per class | after last test in class |
| `module` | once per file | after last test in file |
| `session` | once per test run | end of test session |

```python
@pytest.fixture(scope="session")
def loaded_dataset():
    return load_large_file()  # expensive — created only once
```

### Built-in Fixtures
| Fixture | Purpose |
|---------|---------|
| `tmp_path` | `Path` to a unique temp dir (cleaned after test) |
| `tmp_path_factory` | Create multiple temp dirs (session scope) |
| `capsys` | Capture stdout/stderr |
| `monkeypatch` | Temporarily modify objects, env vars, etc. |
| `caplog` | Capture log messages |

```python
def test_file_io(tmp_path):
    file = tmp_path / "output.json"
    save(data, file)
    assert file.exists()
    assert load(file) == data
```

---

## @pytest.mark.parametrize — Data-Driven Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello world", ["hello", "world"]),
    ("UPPER", ["upper"]),
    ("", []),
])
def test_tokenize(input, expected):
    assert tokenize(input) == expected

# Multiple decorators — cartesian product
@pytest.mark.parametrize("model", ["bert", "roberta"])
@pytest.mark.parametrize("dataset", ["sst2", "imdb"])
def test_training(model, dataset):
    ...   # runs 4 times: all (model, dataset) combinations
```

---

## Mocking with unittest.mock

```python
from unittest.mock import patch, MagicMock

# Patch a function for the duration of the test
def test_no_network_call():
    with patch("mymodule.fetch_from_api") as mock_fetch:
        mock_fetch.return_value = {"score": 0.9}
        result = classify("some text")
        assert result == "positive"
        mock_fetch.assert_called_once()

# MagicMock — generic mock object
mock = MagicMock()
mock.predict.return_value = "positive"
mock.predict("input")
mock.predict.assert_called_with("input")

# Mock as decorator (alternative to context manager)
@patch("mymodule.fetch_from_api", return_value=0.7)
def test_with_decorator(mock_fetch):
    assert classify("text") == "positive"
```

### Common Mock Assertions
| Method | Checks |
|--------|--------|
| `.assert_called()` | was called at least once |
| `.assert_called_once()` | was called exactly once |
| `.assert_called_with(args)` | last call had these args |
| `.assert_not_called()` | was never called |
| `.call_count` | total calls |
| `.return_value = x` | what the mock returns |
| `.side_effect = exc` | raise an exception on call |

---

## monkeypatch — Modify Environment

```python
def test_env_variable(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-abc")
    assert get_api_key() == "test-key-abc"

def test_override_function(monkeypatch):
    monkeypatch.setattr("mymodule.expensive_function", lambda x: 42)
    assert compute(10) == 42
```

---

## Test Structure Best Practices

```
my_project/
├── src/
│   └── pipeline/
│       ├── tokenizer.py
│       └── classifier.py
└── tests/
    ├── conftest.py         ← shared fixtures (auto-loaded by pytest)
    ├── test_tokenizer.py
    └── test_classifier.py
```

### conftest.py — Shared Fixtures
```python
# tests/conftest.py — automatically discovered by pytest
import pytest
from src.pipeline.classifier import TextClassifier

@pytest.fixture(scope="session")
def base_classifier():
    return TextClassifier(labels=["pos", "neg", "neutral"])
```

---

## Quick-Fire Interview Questions

1. **What is the difference between a test fixture and a test helper?**  
   A fixture is managed by pytest (setup/teardown lifecycle). A helper is just a plain function you call manually inside tests.

2. **How do you test that a function raises a specific exception?**  
   `with pytest.raises(ExceptionType, match="pattern"):` block.

3. **What does `monkeypatch.setenv` do?**  
   Temporarily sets an environment variable for the duration of a single test, then restores the original value.

4. **Why use `pytest.approx` for float comparisons?**  
   Floating-point arithmetic isn't exact: `0.1 + 0.2 != 0.3` in Python. `approx` adds a small tolerance.

5. **What is a mock, and when would you use one?**  
   A mock replaces a real dependency (API, database, file system) with a controlled stand-in, so tests are fast, isolated, and deterministic.
