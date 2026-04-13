# Day 27 Notes — Performance Basics

## The Golden Rule: Measure Before You Optimize

> "Premature optimization is the root of all evil." — Donald Knuth

**Process:**
1. Write correct code
2. Measure to find bottlenecks
3. Optimize only the bottleneck
4. Measure again to confirm improvement

---

## Timing Tools

### `time.perf_counter()` — Quick benchmarks
```python
import time

start = time.perf_counter()
result = expensive_operation()
elapsed = time.perf_counter() - start
print(f"Took {elapsed*1000:.3f}ms")
```

### `timeit` — Accurate micro-benchmarks
```python
import timeit

# Run 1000 times, return total time
t = timeit.timeit("sum(range(10000))", number=1000)
avg_ms = t / 1000 * 1000
print(f"Average: {avg_ms:.3f}ms")
```

### `cProfile` — Full function-level profiling
```bash
python -m cProfile -s cumulative my_script.py | head -20
```
```python
import cProfile
with cProfile.Profile() as pr:
    my_function()
pr.print_stats("cumulative")
```

---

## Big-O Complexity — Quick Reference

| Complexity | Name | Example | 1M elements |
|------------|------|---------|-------------|
| O(1) | Constant | dict/set lookup | instant |
| O(log n) | Logarithmic | binary search | ~20 ops |
| O(n) | Linear | list scan | 1M ops |
| O(n log n) | Log-linear | sort | ~20M ops |
| O(n²) | Quadratic | nested loops | 1 trillion ops ← avoid! |
| O(2^n) | Exponential | naive recursion | practically forever |

---

## Common Optimization Patterns

### 1. Set/dict for O(1) lookup
```python
# O(n) — list scan
if word in word_list:    # scans entire list

# O(1) — set/dict lookup
vocab = set(word_list)
if word in vocab:        # hash lookup — instant!
```

### 2. `str.join()` for string building
```python
# BAD — O(n²) — creates new string object each iteration
result = ""
for word in words:
    result += " " + word

# GOOD — O(n) — one allocation
result = " ".join(words)
```

### 3. List comprehension over `append`
```python
# Slower
squares = []
for i in range(n):
    squares.append(i**2)

# Faster
squares = [i**2 for i in range(n)]
```

### 4. Local variable caching
```python
# Slower — method lookup on every iteration
for x in data:
    results.append(f(x))

# Faster — cache method as local
_append = results.append
for x in data:
    _append(f(x))
```

### 5. Generator for large data
```python
# Memory-heavy
total = sum([x**2 for x in range(1_000_000)])  # creates list

# Memory-efficient
total = sum(x**2 for x in range(1_000_000))    # generator
```

### 6. `lru_cache` for repeated calls
```python
from functools import lru_cache

@lru_cache(maxsize=256)
def embed_text(text: str) -> list[float]:
    return compute_embedding(text)  # called only once per unique text
```

---

## Memory Sizes

```python
import sys
sys.getsizeof([])          # 56 bytes (empty list)
sys.getsizeof(list(range(1_000_000)))   # ~8MB
sys.getsizeof(tuple(range(1_000_000)))  # ~8MB (slightly smaller)
sys.getsizeof(set(range(1_000_000)))    # ~32MB (hash table overhead)
sys.getsizeof(x for x in range(1_000_000))  # ~200 bytes! (lazy)
```

---

## Data Structure Selection

| Need | Best Choice | Why |
|------|------------|-----|
| Fast lookup by key | `dict` | O(1) hash |
| Membership check | `set` | O(1) hash |
| Ordered sequence | `list` | O(1) index |
| Immutable sequence | `tuple` | slightly smaller |
| Queue (both ends) | `collections.deque` | O(1) popleft |
| Frequency count | `collections.Counter` | specialized dict |
| Large integers | `int` | arbitrary precision |

---

## AI/ML Specific Tips

```python
# 1. Avoid Python loops over large arrays → use vectorized ops (numpy)
# Slow:
result = [x * 0.5 for x in million_values]

# Fast (with numpy):
import numpy as np
arr = np.array(million_values)
result = arr * 0.5   # vectorized C operation

# 2. Batch data processing — avoid one-at-a-time API calls
# Slow:
for text in texts:
    embedding = embed(text)

# Fast:
embeddings = embed_batch(texts)   # one API call for all

# 3. Generator pipelines — process one record at a time
# stream data from disk → never load entire dataset
```

---

## Quick-Fire Interview Questions

1. **What's the difference between `time.time()` and `time.perf_counter()`?**  
   `perf_counter()` has higher resolution and is not affected by system clock changes; prefer it for benchmarking.

2. **What is O(n²) complexity? Why is it dangerous?**  
   Two nested loops each proportional to n; 1M elements → 1 trillion operations. Becomes unusable for large data.

3. **How would you speed up repeated membership checks on a list of 1 million items?**  
   Convert to a `set` for O(1) lookup instead of O(n) list scan.

4. **When should you use a generator instead of a list comprehension?**  
   When the data is large and you only need one pass (don't need random access or multiple iterations).

5. **What does `lru_cache` do, and when is it useful?**  
   Memoizes function results by input; useful for pure functions called repeatedly with the same arguments (tokenization, embeddings, Fibonacci).
