# Day 6 Exercises — *args, **kwargs, Recursion

Estimated time: 30–40 minutes

---

## Exercise 1 — Flexible Logger

Write a function `log(level, *messages, **context)` that:
- `level` is a required string: `"INFO"`, `"WARN"`, or `"ERROR"`
- `*messages` — any number of message strings to log
- `**context` — optional key-value pairs to attach to the log

Output format:
```
[INFO] Starting pipeline | model=gpt-4, batch_size=32
[WARN] High memory usage | usage_mb=14200
[ERROR] Request failed | status=500, retry=3
```

Test:
```python
log("INFO", "Starting pipeline", model="gpt-4", batch_size=32)
log("WARN", "High memory usage", usage_mb=14200)
log("ERROR", "Request failed", status=500, retry=3)
```

---

## Exercise 2 — Config Merger

Write a function `build_config(base_config, **overrides)` that:
1. Starts with a copy of `base_config` (dict)
2. Applies all overrides (keyword arguments win)
3. Validates that `temperature` is between 0 and 2 (raise `ValueError` if not)
4. Returns the final config

```python
DEFAULT_CONFIG = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 512,
    "top_p": 1.0,
}

cfg = build_config(DEFAULT_CONFIG, model="gpt-4", temperature=0.2, max_tokens=2048)
print(cfg)
```

---

## Exercise 3 — Recursive Sum of Nested List

Write `recursive_sum(data)` that sums all numbers in an arbitrarily nested list:

```python
data = [1, [2, 3], [4, [5, 6]], 7]
print(recursive_sum(data))   # 28
```

Handle: integers, floats, and arbitrarily deep nesting.
No `flatten` imports — pure recursion only.

---

## Exercise 4 — Recursive File Path Expander

Given a nested dictionary representing a file system, write `list_files(tree, path="")`
that returns a list of all file paths (leaves):

```python
file_system = {
    "src": {
        "models": {
            "bert.py": None,
            "gpt.py": None,
        },
        "utils": {
            "tokenizer.py": None,
        },
    },
    "tests": {
        "test_models.py": None,
    },
    "README.md": None,
}

paths = list_files(file_system)
# Expected (order may vary):
# ["src/models/bert.py", "src/models/gpt.py",
#  "src/utils/tokenizer.py", "tests/test_models.py", "README.md"]
```

---

## Exercise 5 — Recursive Binary Search

Implement binary search recursively:

```python
def binary_search(arr, target, low, high):
    ...
```

- Returns the index of `target` in `arr` (sorted), or `-1` if not found
- Must use recursion (not iteration)

Test:
```python
data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(data, 23, 0, len(data) - 1))  # 5
print(binary_search(data, 10, 0, len(data) - 1))  # -1
```

What is the time complexity? Space complexity (considering the call stack)?

---

## Stretch Challenge — Power Set Generator

The power set of `[1, 2, 3]` is all possible subsets: `[[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]`.

Write a recursive function `power_set(items)` that returns all subsets.

**Hint**: The power set of `[1, 2, 3]` = (subsets without 1) + (subsets with 1 prepended to each subset without 1).

This is used in feature selection for ML — trying all possible combinations of features.
