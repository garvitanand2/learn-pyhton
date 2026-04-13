# Day 4 Notes — Loops

## What & Why

**Loops** let you repeat code — processing each row of a dataset, each token
in a prompt, each epoch of training, or each item returned by an API.
Without loops, you'd have to write every operation manually.

---

## `for` Loop

Iterates over any **iterable** — list, tuple, string, dict, range, file, generator.

```python
for item in iterable:
    # code runs once per item
```

### `range()`

| Call | Produces |
|------|----------|
| `range(5)` | `0, 1, 2, 3, 4` |
| `range(1, 6)` | `1, 2, 3, 4, 5` |
| `range(0, 10, 2)` | `0, 2, 4, 6, 8` |
| `range(10, 0, -1)` | `10, 9, ..., 1` |

`range()` is **lazy** — it generates numbers one at a time, not a full list.
This is critical when working with large indices.

### `enumerate()` — index + value together

```python
for i, value in enumerate(my_list):
    print(i, value)

# Start from a custom index
for i, value in enumerate(my_list, start=1):
    ...
```

### `zip()` — iterate multiple sequences in parallel

```python
for text, label in zip(texts, labels):
    ...
```

`zip()` stops at the shortest sequence. Use `itertools.zip_longest()` if you
need to fill gaps with a default value.

---

## `while` Loop

Runs as long as a condition is True. Use when you don't know how many
iterations are needed in advance.

```python
while condition:
    # code

    # Always include a way to exit:
    # - modify the condition
    # - or use break
```

### Safety Pattern — Always Add a Guard

```python
max_retries = 5
attempts = 0
while not success:
    attempts += 1
    if attempts >= max_retries:
        break
    try_again()
```

Never write `while True:` without a `break` — it creates an infinite loop.

---

## `break` and `continue`

| Keyword   | Effect                                         |
|-----------|------------------------------------------------|
| `break`   | Exit the loop entirely                         |
| `continue`| Skip the rest of this iteration, go to next    |

```python
for item in data:
    if item is None:
        continue        # skip bad data
    if item == STOP_TOKEN:
        break           # stop processing
    process(item)
```

---

## `for...else` and `while...else`

The `else` block runs **only if the loop completed without hitting `break`**.
This is unique to Python and very useful for "search and not found" patterns.

```python
for model in candidates:
    if model.accuracy >= target:
        deploy(model)
        break
else:
    alert("No model met the deployment threshold")
```

---

## Iterating Dictionaries

```python
for key in d:              # iterates over keys
for key, value in d.items():  # key-value pairs
for value in d.values():  # just values
```

---

## Nested Loops

Useful for:
- Hyperparameter grid search
- Matrix operations
- Comparing all pairs of items

Time complexity of nested loops: **O(n × m)** — watch out for large inputs.

---

## Real-World Analogy

Think of a `for` loop as a **data pipeline conveyor belt**:
- Items (training samples) come in one by one
- Each item is processed (normalized, tokenized, labeled)
- `continue` → drop a defective item
- `break`    → shut down the belt when quota is reached
- `else`     → signal when the batch is fully processed

A `while` loop is like a **training loop**:  
"Keep training until loss is low enough OR max epochs reached."

---

## Interview Quick-Fire

1. **What is the difference between `break` and `continue`?**
   → `break` exits the loop; `continue` skips only the current iteration.

2. **When does the `else` block of a `for` loop execute?**
   → When the loop finishes normally (without a `break`).

3. **Is `range()` a list?**
   → No. It's a lazy sequence object. `list(range(5))` converts it to a list.

4. **What's the time complexity of `x in my_list` inside a loop?**
   → O(n) per lookup → O(n²) total. Use a `set` instead for O(1) lookups.

5. **How do you iterate over dictionary keys and values at the same time?**
   → `for key, value in d.items():`
