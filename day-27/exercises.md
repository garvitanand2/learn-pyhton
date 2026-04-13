# Day 27 Exercises — Performance Basics

## Exercise 1: Benchmark Lookup Methods
Compare membership test speed for `list`, `tuple`, `set`, and `dict` as the data size grows.

```python
import timeit

def benchmark_lookups(sizes: list[int]) -> None:
    for n in sizes:
        data_list = list(range(n))
        data_tuple = tuple(range(n))
        data_set = set(range(n))
        data_dict = dict.fromkeys(range(n))

        target = n - 1  # worst-case for list/tuple

        results = {
            "list":  timeit.timeit(lambda: target in data_list,  number=1000),
            "tuple": timeit.timeit(lambda: target in data_tuple, number=1000),
            "set":   timeit.timeit(lambda: target in data_set,   number=1000),
            "dict":  timeit.timeit(lambda: target in data_dict,  number=1000),
        }
        print(f"\nn={n:>8}")
        for name, t in results.items():
            print(f"  {name:>6}: {t*1000:.2f}ms total")

benchmark_lookups([100, 1_000, 10_000, 100_000])
```

**Challenge:** At what size does the `set` advantage become clearly visible?

---

## Exercise 2: String Building Comparison
Benchmark four methods to join 10,000 words: `+=` concatenation, `str.join()`, `io.StringIO`, and list comprehension join.

```python
import timeit, io

words = ["word"] * 10_000

def join_concat():
    result = ""
    for w in words:
        result += w + " "
    return result

def join_builtin():
    return " ".join(words)

def join_stringio():
    buf = io.StringIO()
    for w in words:
        buf.write(w)
        buf.write(" ")
    return buf.getvalue()

def join_comprehension():
    return " ".join(w for w in words)

for name, fn in [
    ("concatenation", join_concat),
    ("str.join",      join_builtin),
    ("StringIO",      join_stringio),
    ("comprehension", join_comprehension),
]:
    t = timeit.timeit(fn, number=500)
    print(f"{name:>16}: {t*1000:.1f}ms (500 runs)")
```

---

## Exercise 3: Optimize O(n²) → O(n)
The function below checks for duplicate tokens in a list using a naive nested loop. Rewrite it to run in O(n) time.

```python
from typing import Optional

# SLOW VERSION — O(n²)
def find_first_duplicate_slow(tokens: list[str]) -> Optional[str]:
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            if tokens[i] == tokens[j]:
                return tokens[i]
    return None


# YOUR TASK: Write the O(n) version below
def find_first_duplicate_fast(tokens: list[str]) -> Optional[str]:
    seen = set()
    for token in tokens:
        if token in seen:
            return token
        seen.add(token)
    return None


# Verify correctness
sample = ["the", "cat", "sat", "on", "the", "mat"]
assert find_first_duplicate_slow(sample) == "the"
assert find_first_duplicate_fast(sample) == "the"

# Benchmark
import timeit
big = ["token_" + str(i) for i in range(5000)] + ["token_0"]

t_slow = timeit.timeit(lambda: find_first_duplicate_slow(big), number=20)
t_fast = timeit.timeit(lambda: find_first_duplicate_fast(big), number=20)
print(f"Slow: {t_slow:.3f}s | Fast: {t_fast:.4f}s | Speedup: {t_slow/t_fast:.0f}x")
```

---

## Exercise 4: LRU Cache for Tokenization
Implement a `cached_tokenize()` function using `lru_cache` and measure the speedup when the same texts appear repeatedly (a realistic scenario in NLP where the same sentence appears many times in a dataset).

```python
import time, random, string
from functools import lru_cache

# Simulate a "slow" tokenizer (real tokenizers do regex, BPE, etc.)
def slow_tokenize(text: str) -> tuple[str, ...]:
    time.sleep(0.001)  # simulate 1ms processing
    return tuple(text.lower().split())

@lru_cache(maxsize=512)
def cached_tokenize(text: str) -> tuple[str, ...]:
    return slow_tokenize(text)

# Dataset: 100 sentences but only 10 unique ones (90% cache hits)
unique_sentences = [
    "The model achieved high accuracy on the test set",
    "Gradient descent minimizes the loss function",
    "Attention is all you need for transformer models",
    "Tokenization splits text into subword units",
    "Batch normalization stabilizes training",
    "Dropout prevents overfitting in deep networks",
    "Embeddings capture semantic relationships",
    "Transfer learning reuses pretrained weights",
    "The learning rate controls step size",
    "Cross entropy loss is used for classification",
]
dataset = unique_sentences * 10  # 100 total with heavy repetition
random.shuffle(dataset)

# Without cache
t0 = time.perf_counter()
_ = [slow_tokenize(t) for t in dataset]
t_no_cache = time.perf_counter() - t0

# With cache
cached_tokenize.cache_clear()
t0 = time.perf_counter()
_ = [cached_tokenize(t) for t in dataset]
t_cached = time.perf_counter() - t0

print(f"Without cache: {t_no_cache:.2f}s")
print(f"With cache:    {t_cached:.2f}s")
print(f"Speedup:       {t_no_cache/t_cached:.0f}x")
print(f"Cache info:    {cached_tokenize.cache_info()}")
```

---

## Exercise 5: Profile a Pipeline (cProfile)
Profile the data processing pipeline below and identify the bottleneck. Then fix it.

```python
import cProfile
import pstats
import io

# --- Slow pipeline ---
def normalize_text(text: str) -> str:
    # Inefficient: rebuilds string char by char
    result = ""
    for char in text:
        if char.isalnum() or char == " ":
            result += char.lower()
    return result

def tokenize(text: str) -> list[str]:
    return text.split()

def compute_vocab(texts: list[str]) -> set[str]:
    vocab = []
    for text in texts:
        for token in tokenize(normalize_text(text)):
            vocab.append(token)
    return set(vocab)

docs = ["Hello, World! This is sentence #" + str(i) + "."
        for i in range(2000)]

# Profile it
pr = cProfile.Profile()
pr.enable()
vocab = compute_vocab(docs)
pr.disable()

stream = io.StringIO()
stats = pstats.Stats(pr, stream=stream).sort_stats("cumulative")
stats.print_stats(10)
print(stream.getvalue())
print(f"Vocab size: {len(vocab)}")

# --- YOUR TASK: Rewrite normalize_text to use str.join + generator ---
def normalize_text_fast(text: str) -> str:
    return "".join(
        ch.lower() for ch in text if ch.isalnum() or ch == " "
    )

import timeit
t_slow = timeit.timeit(lambda: normalize_text("Hello, World! This is #42."), number=10000)
t_fast = timeit.timeit(lambda: normalize_text_fast("Hello, World! This is #42."), number=10000)
print(f"\nnormalize_text slow: {t_slow:.3f}s | fast: {t_fast:.3f}s | speedup: {t_slow/t_fast:.1f}x")
```

---

## Stretch Challenge: Memory Profiler
Write a decorator `@measure_memory` that prints the memory used by a function before and after calling it (using `tracemalloc`).

```python
import tracemalloc
import functools

def measure_memory(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = fn(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"[{fn.__name__}] peak memory: {peak / 1024:.1f} KB")
        return result
    return wrapper

@measure_memory
def build_list():
    return [i**2 for i in range(100_000)]

@measure_memory
def build_generator():
    return sum(i**2 for i in range(100_000))

build_list()
build_generator()
```
