# Day 20 Exercises — Iterators & Generators

Estimated time: 45–60 minutes

---

## Exercise 1 — Custom Sliding Window Iterator

Build a class `SlidingWindow` that implements the iterator protocol:

```python
class SlidingWindow:
    def __init__(self, data: list, window_size: int, stride: int = 1): ...
    def __iter__(self): ...
    def __next__(self): ...
    def __len__(self) -> int: ...  # number of windows
```

Test with a sequence of 10 tokens and window size 3:
```python
tokens = ["<BOS>", "the", "cat", "sat", "on", "mat", "<EOS>"]
for window in SlidingWindow(tokens, window_size=3, stride=1):
    print(window)
```

This is used in language modeling to create context windows.

---

## Exercise 2 — Infinite Data Augmentation Stream

Write a generator `augmented_stream(texts: list[str])` that:
1. Cycles infinitely through the texts
2. Applies a **random** augmentation to each:
   - "reverse": reverse the word order
   - "upper": convert to uppercase
   - "repeat": repeat each word twice
   - "none": return unchanged
3. Generates `(original, augmented, augmentation_name)` tuples

Use `itertools.cycle` and `random.choice`.

Take the first 20 samples from the stream and verify a variety of augmentations.

---

## Exercise 3 — Generator Pipeline

Build a complete streaming text pipeline using generators:

```
read_records(n)
    → filter_valid_records (drop records with no "text" or text < 5 chars)
    → clean_text (lowercase, strip punctuation)
    → tokenize (split into words)
    → pad_or_truncate (max 10 tokens: pad with "<PAD>", truncate)
    → encode (replace words with integer IDs from a vocab)
```

Create a small vocab dict first (10+ words).  
Run 15 records through the pipeline and print the encoded output.

---

## Exercise 4 — Memory Benchmark

Compare memory usage of these three approaches to compute the sum of squares
for numbers 1 to 1,000,000:

1. **List**: `sum([x**2 for x in range(1_000_000)])`
2. **Generator expression**: `sum(x**2 for x in range(1_000_000))`
3. **Generator function**: `sum(gen_squares(1_000_000))`

Use `sys.getsizeof()` to show memory at the point of the intermediate object creation.  
Use `time.perf_counter()` to compare execution times.

---

## Exercise 5 — `itertools` Grid Search

Use `itertools.product` to generate all hyperparameter combinations:

```python
from itertools import product

search_space = {
    "learning_rate": [1e-5, 3e-5, 1e-4],
    "batch_size": [16, 32, 64],
    "dropout": [0.1, 0.3],
    "warmup_steps": [100, 500],
}
```

1. Generate all configurations (how many total?)
2. Filter to only configs where `batch_size >= 32` and `learning_rate <= 3e-5`
3. Sort filtered configs by `learning_rate` descending
4. Print first 5

Do all of this using lazy generators — only convert to list at step 4.

---

## Stretch Challenge — Chunked File Reader

Write a generator `chunked_reader(file_path, chunk_size=1024)` that:
1. Opens a file in binary mode (`"rb"`)
2. Yields `chunk_size`-byte chunks
3. Reports total bytes read when exhausted

Then write `line_reader(file_path)` using it that:
1. Uses `chunked_reader` internally
2. Reassembles complete lines across chunk boundaries
3. Yields one decoded line at a time

Test by creating a temp file with 100 lines and streaming through it.
