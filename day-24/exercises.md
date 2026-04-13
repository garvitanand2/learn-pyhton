# Day 24 Exercises — Lambda, Map, Filter, Reduce

Estimated time: 30–45 minutes

---

## Exercise 1 — Data Pipeline with map/filter

Given a list of raw model prediction records:

```python
raw_records = [
    {"id": 1, "text": "Great model performance", "score": 0.92},
    {"id": 2, "text": "", "score": 0.45},
    {"id": 3, "text": "Bad training run", "score": 0.38},
    {"id": 4, "text": "Outstanding results", "score": 0.95},
    {"id": 5, "text": None, "score": 0.71},
    {"id": 6, "text": "Poor convergence", "score": 0.22},
    {"id": 7, "text": "Average performance", "score": 0.60},
]
```

Using only `map()`, `filter()`, and `lambda` (no for loops):
1. Filter out records with empty/None text or score < 0.5
2. Map each remaining record to `{"id": ..., "label": "positive"/"neutral"/"negative", "words": N}`  
   (positive if score ≥ 0.8, neutral if 0.5-0.8, negative below 0.5)
3. Sort by word count descending

---

## Exercise 2 — Reduce for Aggregation

Using only `reduce()` (no built-ins like `sum`, `max`, `min`):

Given a list of epoch metrics:
```python
epochs = [
    {"epoch": 1, "loss": 0.842, "accuracy": 0.61},
    {"epoch": 2, "loss": 0.621, "accuracy": 0.75},
    {"epoch": 3, "loss": 0.489, "accuracy": 0.83},
    {"epoch": 4, "loss": 0.391, "accuracy": 0.87},
    {"epoch": 5, "loss": 0.312, "accuracy": 0.91},
]
```

1. Compute total loss (sum)
2. Find the epoch with minimum loss
3. Find the epoch with maximum accuracy
4. Compute the vocabulary union: `reduce(lambda a, b: a | b, [{"cat","dog"}, {"cat","fish"}, {"dog","bird"}])`

---

## Exercise 3 — `partial` Factory

Write a `make_preprocessor(**options)` function that uses `partial` to create specialized preprocessors:

```python
en_preprocessor  = make_preprocessor(language="en", lowercase=True, max_len=128)
ar_preprocessor  = make_preprocessor(language="ar", lowercase=False, max_len=64)
quick_processor  = make_preprocessor(max_len=512, strip_only=True)
```

Where the underlying `preprocess(text, language, lowercase, max_len, strip_only)` function exists.
Show each preprocessor working on the same 3 sample texts.

---

## Exercise 4 — Functional Data Summary

Without any for loops, using `map`, `filter`, `reduce`, `sorted`, `lambda`, `functools`:

Given a list of 20 records (generate with list comprehension):
```python
import random; random.seed(42)
data = [{"id": i, "score": round(random.random(), 3), "label": random.choice(["pos","neg","neu"])}
        for i in range(20)]
```

Compute:
1. Mean score (use `reduce` for sum, `len` for count)
2. Count per label (use `reduce` with a dict accumulator)
3. Top 5 records by score
4. Scores for "pos" label only, sorted ascending

---

## Exercise 5 — Compose a Full Transform Chain

Create a `compose(*fns)` utility (right-to-left) and `pipe(*fns)` (left-to-right), then build these pipelines:

**NLP preprocessing pipeline:**
```python
preprocess = pipe(str.strip, str.lower, remove_punctuation, tokenize, remove_stopwords)
result = preprocess("  The quick BROWN fox, jumps!  ")
# → ["quick", "brown", "fox", "jumps"]
```

**Score normalization pipeline:**
```python
normalize = pipe(
    lambda scores: [s - min(scores) for s in scores],  # shift to 0
    lambda scores: [s / max(scores) if max(scores) > 0 else 0 for s in scores],  # scale to 1
)
```

---

## Stretch Challenge — Lazy Pipeline with Generators

Rewrite Exercise 1's pipeline to be **fully lazy** (no materialization until the final list):

1. Use generator expressions everywhere possible
2. Only call `list()` at the very end
3. Count how many records were filtered vs mapped using a counter (without breaking laziness)

Bonus: Wrap the pipeline in a function `process_stream(records_iter)` that works with any iterator.
