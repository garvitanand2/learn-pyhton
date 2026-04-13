# Day 20 Notes — Iterators & Generators

## The Iterator Protocol

Python's `for` loop works with **any object that implements the iterator protocol**:

```python
# What `for x in obj:` actually does:
it = iter(obj)       # calls obj.__iter__()  → returns iterator
while True:
    try:
        x = next(it)  # calls it.__next__() → next value
        # ... body of loop
    except StopIteration:
        break
```

To make a class iterable, implement:
- `__iter__(self)` → returns self (or another iterator)  
- `__next__(self)` → returns next value, raises `StopIteration` when done

---

## `yield` — The Heart of Generators

```python
def count_up(n):
    i = 0
    while i < n:
        yield i      # ← pause here, return i
        i += 1       # ← resumes here on next()
```

When Python sees `yield`:
1. Returns the value to the caller
2. **Suspends** the function's execution (keeps local variables!)
3. Resumes from the `yield` line on the next `next()` call
4. Raises `StopIteration` when the function returns

---

## Generator vs List Comprehension

```python
# List comprehension — EAGER: builds entire list in memory NOW
squares = [x**2 for x in range(1_000_000)]  # ~8 MB

# Generator expression — LAZY: computes values on demand
squares = (x**2 for x in range(1_000_000))  # ~120 bytes

# Both work identically in for loops and sum():
total = sum(x**2 for x in range(1_000_000))    # no extra memory!
```

**Rule of thumb:**  
- Need random access or multiple passes → list  
- One-time stream of large data → generator

---

## `yield from` — Delegation

```python
def chain(*iterables):
    for iterable in iterables:
        yield from iterable   # equivalent to: for item in iterable: yield item

list(chain([1, 2], [3, 4], [5]))  # [1, 2, 3, 4, 5]
```

Also used for recursive generators:
```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # recurse
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))  # [1, 2, 3, 4, 5]
```

---

## Generator Pipeline Pattern

Chain generators like Unix pipes — data flows lazily through stages:

```python
# Source
def read_lines(path):
    with open(path) as f:
        yield from f

# Filter
def non_empty(lines):
    for line in lines:
        if line.strip():
            yield line

# Transform
def tokenize(lines):
    for line in lines:
        yield line.lower().split()

# Sink (consumes)
pipeline = tokenize(non_empty(read_lines("corpus.txt")))
for tokens in pipeline:
    process(tokens)
```

Nothing runs until you consume the final generator. Memory: only ONE record in memory at a time.

---

## `itertools` — Powerful Iterator Utilities

```python
from itertools import chain, islice, cycle, product, combinations

# islice — take first N items from any iterator
first_10 = list(islice(my_generator(), 10))

# chain — combine multiple iterables
all_data = chain(train_data, val_data, test_data)

# cycle — repeat an iterable infinitely
augmentation_fns = cycle([flip, rotate, crop])

# product — Cartesian product (hyperparameter grid search!)
from itertools import product
lr_values = [1e-3, 1e-4, 1e-5]
batch_sizes = [16, 32, 64]
configs = list(product(lr_values, batch_sizes))
# [(0.001, 16), (0.001, 32), ..., (1e-5, 64)] — 9 combos

# combinations — unique pairs (ensemble selection)
from itertools import combinations
models = ["bert", "gpt", "t5"]
pairs = list(combinations(models, 2))
# [("bert", "gpt"), ("bert", "t5"), ("gpt", "t5")]
```

---

## Generators Are Consumed Once!

```python
gen = (x * 2 for x in range(5))

first_pass = list(gen)   # [0, 2, 4, 6, 8]
second_pass = list(gen)  # []  ← exhausted!

# To iterate multiple times: use a list or create a new generator
```

---

## Real-World Pattern: Streaming DataLoader

```python
def dataset_stream(file_path, batch_size=32):
    """Streams a large JSONL dataset in batches — never loads it all!"""
    import json
    batch = []
    with open(file_path) as f:
        for line in f:
            record = json.loads(line)
            batch.append(record)
            if len(batch) == batch_size:
                yield batch
                batch = []
    if batch:          # yield final partial batch
        yield batch

# Usage
for batch in dataset_stream("large_dataset.jsonl", batch_size=64):
    process_batch(batch)   # only 64 records in memory at a time!
```

---

## Quick-Fire Interview Questions

1. **What is an iterator?**  
   An object implementing `__iter__` and `__next__`; yields values one at a time, raises `StopIteration` when done.

2. **What does `yield` do in a function?**  
   Pauses execution, returns a value to the caller, and resumes from the same point on the next `next()` call.

3. **What's the difference between a generator expression and a list comprehension?**  
   List comp evaluates all values eagerly; generator expression is lazy — values computed on demand.

4. **Why are generators useful for ML data pipelines?**  
   Datasets can be too large to fit in RAM; generators stream data one batch at a time with minimal memory.

5. **What does `yield from` do?**  
   Delegates iteration to a sub-generator or iterable, forwarding all its values.
