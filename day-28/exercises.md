# Day 28 Exercises — Type Hints & Dataclasses

## Exercise 1: Annotate an Existing Function
Add full type annotations to these untyped helper functions, then verify with `mypy`.

```python
# YOUR TASK: add type hints to every parameter and return type

def clean_texts(texts, lowercase, max_length):
    """Lowercase and truncate a list of texts."""
    result = []
    for text in texts:
        if lowercase:
            text = text.lower()
        result.append(text[:max_length])
    return result


def merge_dicts(base, override):
    """Merge two dicts; override values take priority."""
    return {**base, **override}


def safe_divide(numerator, denominator, default):
    """Return numerator/denominator, or default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


# SOLUTION (uncomment to check):
# def clean_texts(texts: list[str], lowercase: bool, max_length: int) -> list[str]: ...
# def merge_dicts(base: dict[str, object], override: dict[str, object]) -> dict[str, object]: ...
# def safe_divide(numerator: float, denominator: float, default: float) -> float: ...
```

---

## Exercise 2: Build a ModelRun Dataclass
Create a `ModelRun` dataclass with:
- `run_id: str`
- `model_name: str`
- `hyperparams: dict[str, float]` (default empty dict)
- `metrics: list[float]` (default empty list)
- `frozen=False`, `order=True` (sort by best final metric)
- `__post_init__` that validates `run_id` is non-empty
- A computed property `best_metric` that returns `max(metrics)` or `0.0` if empty

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class ModelRun:
    # ... your implementation here ...
    pass

# Tests
r1 = ModelRun("run-001", "bert-base", metrics=[0.71, 0.79, 0.84])
r2 = ModelRun("run-002", "roberta", metrics=[0.88, 0.91])
assert r1.best_metric == 0.84
assert r2.best_metric == 0.91
print("Best run:", max([r1, r2], key=lambda r: r.best_metric))
print("JSON:", __import__("json").dumps(__import__("dataclasses").asdict(r1), indent=2))
```

---

## Exercise 3: Protocol for Data Loaders
Define a `DataLoader` protocol and write a function `evaluate_all(loaders, model)` that accepts any list of objects satisfying it.

```python
from typing import Protocol

class DataLoader(Protocol):
    def __iter__(self): ...
    def __len__(self) -> int: ...
    @property
    def name(self) -> str: ...

# Implement two concrete loaders (no inheritance from DataLoader)
class CSVLoader:
    def __init__(self, path: str, data: list[str]):
        self._data = data
        self._path = path
    def __iter__(self): return iter(self._data)
    def __len__(self): return len(self._data)
    @property
    def name(self) -> str: return f"CSV({self._path})"

class InMemoryLoader:
    def __init__(self, data: list[str]):
        self._data = data
    def __iter__(self): return iter(self._data)
    def __len__(self): return len(self._data)
    @property
    def name(self) -> str: return "InMemory"

# YOUR TASK: implement this function
def evaluate_all(loaders: list[DataLoader]) -> dict[str, int]:
    """Return a dict mapping loader.name → len(loader)."""
    return {loader.name: len(loader) for loader in loaders}

loaders = [
    CSVLoader("train.csv", ["a", "b", "c"]),
    InMemoryLoader(["x", "y"]),
]
print(evaluate_all(loaders))  # {'CSV(train.csv)': 3, 'InMemory': 2}
```

---

## Exercise 4: TypedDict for Configuration
Define a `PipelineConfig` TypedDict and write a `validate_config()` function that checks required keys and value ranges.

```python
from typing import TypedDict, Optional

class PipelineConfig(TypedDict):
    model_name: str
    max_seq_len: int
    batch_size: int
    learning_rate: float
    output_dir: str
    debug: bool

def validate_config(config: PipelineConfig) -> list[str]:
    """Return a list of validation error messages (empty = valid)."""
    errors = []
    if not config.get("model_name"):
        errors.append("model_name cannot be empty")
    if config.get("max_seq_len", 0) > 2048:
        errors.append("max_seq_len exceeds 2048")
    if not (0 < config.get("learning_rate", 0) < 1):
        errors.append("learning_rate must be between 0 and 1")
    return errors

good: PipelineConfig = {
    "model_name": "bert-base-uncased",
    "max_seq_len": 512,
    "batch_size": 32,
    "learning_rate": 3e-4,
    "output_dir": "./output",
    "debug": False,
}
bad: PipelineConfig = {
    "model_name": "",
    "max_seq_len": 4096,
    "batch_size": 32,
    "learning_rate": 1.5,
    "output_dir": "./output",
    "debug": True,
}
print("Good config errors:", validate_config(good))  # []
print("Bad config errors:",  validate_config(bad))   # 3 errors
```

---

## Exercise 5: Frozen Dataclass as Dict Key
Use a frozen dataclass as a cache key for experiment lookup.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ExperimentKey:
    model: str
    dataset: str
    seed: int

# YOUR TASK: build an experiment cache dict
# Use ExperimentKey instances as keys
# Verify that same-value keys hit the same cache entry

results: dict[ExperimentKey, float] = {}

k1 = ExperimentKey("bert", "sst2", 42)
k2 = ExperimentKey("bert", "sst2", 42)   # same values
k3 = ExperimentKey("roberta", "sst2", 42)

results[k1] = 0.923
print("k1 == k2:", k1 == k2)               # True — same values
print("k1 is k2:", k1 is k2)               # False — different objects
print("k2 in results:", k2 in results)     # True — hash equality works
print("k3 in results:", k3 in results)     # False

# Add k3
results[k3] = 0.941
print("Best:", max(results.items(), key=lambda kv: kv[1]))
```

---

## Stretch Challenge: Generic Stack
Implement a type-safe `Stack[T]` dataclass using generics.

```python
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

@dataclass
class Stack(Generic[T]):
    _items: list[T] = field(default_factory=list, repr=False)

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)

# String stack
s: Stack[str] = Stack()
s.push("token_a")
s.push("token_b")
print("Peek:", s.peek())
print("Pop:", s.pop())
print("Size:", len(s))
```
