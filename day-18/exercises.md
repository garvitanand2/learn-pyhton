# Day 18 Exercises — OOP Basics

Estimated time: 45–60 minutes

---

## Exercise 1 — `TrainingConfig` Class

Build a `TrainingConfig` class with:

**Attributes:** `model_name`, `learning_rate`, `batch_size`, `epochs`, `device`

**Methods:**
- `validate()` — raises `ValueError` for out-of-range values
- `warmup_steps(dataset_size)` — computes 10% of total training steps
- `__str__` — formatted summary table
- `to_dict()` — returns all params as a dict
- `from_dict(data)` — `@classmethod` alternative constructor

Test by creating two configs and verifying validation rejects bad inputs.

---

## Exercise 2 — `TextDataset` Class

Build a `TextDataset` class:

**`__init__(self, records: list[dict])`** where each record has `"id"`, `"text"`, `"label"`

**Implement these dunders:**
- `__len__` — total number of samples
- `__getitem__` — index access, both positive and negative
- `__repr__` and `__str__`
- `__iter__` — (bonus) iterate over records

**Add methods:**
- `filter(label)` → returns new `TextDataset` with only that label
- `label_stats()` → returns `{label: count}` dict
- `split(ratio=0.8)` → returns `(train_dataset, val_dataset)` tuple

---

## Exercise 3 — `Vocabulary` Class

Build a vocabulary class often used in NLP:

```python
class Vocabulary:
    PAD = 0; UNK = 1; BOS = 2; EOS = 3
```

**Methods:**
- `__init__`: initializes with special tokens pre-added
- `add(word)` — adds a word, returns its ID
- `encode(sentence: str)` — returns list of IDs (unknown → UNK)
- `decode(ids: list[int])` — returns list of words
- `__len__` — vocabulary size
- `__contains__` — `"word" in vocab`
- `@classmethod from_corpus(texts)` — build vocab from a list of strings

---

## Exercise 4 — `EarlyStopping` Class

Implement a classic training utility:

```python
class EarlyStopping:
    def __init__(self, patience=3, min_delta=0.001):
        ...
    
    def step(self, val_loss: float) -> bool:
        """Returns True if training should stop."""
        ...
    
    @property
    def best_loss(self) -> float: ...
    
    @property
    def epochs_without_improvement(self) -> int: ...
```

Rules:
- Stop if validation loss doesn't improve by at least `min_delta` for `patience` consecutive epochs
- Track the best loss seen so far

Simulate 15 epochs with these losses and check when it would stop:
```python
losses = [0.90, 0.75, 0.61, 0.58, 0.57, 0.57, 0.58, 0.57, 0.56, 0.56, 0.56, 0.56, 0.55, 0.55, 0.55]
```

---

## Exercise 5 — `ConfusionMatrix` Class

Build a confusion matrix tracker:

```python
class ConfusionMatrix:
    def __init__(self, classes: list[str]): ...
    
    def update(self, predicted: str, actual: str) -> None: ...
    def accuracy(self) -> float: ...
    def precision(self, label: str) -> float: ...
    def recall(self, label: str) -> float: ...
    def __str__(self) -> str:  # formatted matrix table
```

Test with at least 20 prediction/label pairs across 3 classes.

---

## Stretch Challenge — Fluent Interface (Method Chaining)

Redesign `TrainingConfig` to support method chaining:

```python
config = (
    TrainingConfig("bert")
    .set_lr(3e-5)
    .set_batch_size(32)
    .set_epochs(10)
    .use_device("cuda")
    .validate()
)
```

Each setter method must return `self` to enable chaining.

Then add a `clone()` method that returns a deep copy so you can create variations:
```python
small_config = config.clone().set_batch_size(8).set_lr(1e-5)
```
