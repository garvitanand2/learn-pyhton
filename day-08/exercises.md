# Day 8 Exercises — Lists

Estimated time: 25–35 minutes

---

## Exercise 1 — Train/Val/Test Split

Given a dataset of 1000 items (represented as indices 0–999), split it into:
- 70% training
- 15% validation
- 15% test

```python
dataset = list(range(1000))
```

1. Use slicing (not any external library)
2. Print the size of each split
3. Verify: `len(train) + len(val) + len(test) == len(dataset)`

---

## Exercise 2 — Running Average Loss

Given a list of batch loss values, compute the **running average** — the
average of all losses up to and including each batch:

```python
batch_losses = [0.95, 0.82, 0.74, 0.68, 0.61, 0.55, 0.50, 0.47]
```

Expected output:
```
Batch 1: loss=0.9500 | running avg=0.9500
Batch 2: loss=0.8200 | running avg=0.8850
...
```

---

## Exercise 3 — Top-K Predictions

Given a list of confidence scores, find the **top 3** scores and their indices
(without sorting the original list):

```python
scores = [0.12, 0.87, 0.34, 0.95, 0.78, 0.56, 0.91, 0.43]
```

Expected:
```
Top 3:
  #1: index=3, score=0.9500
  #2: index=6, score=0.9100
  #3: index=1, score=0.8700
```

(Hint: use `sorted(enumerate(scores), key=..., reverse=True)`)

---

## Exercise 4 — List Deduplication (Preserve Order)

Given a list of labels that may contain duplicates, return a new list with
duplicates removed but **original order preserved**:

```python
labels = ["cat", "dog", "cat", "bird", "dog", "fish", "cat"]
# Expected: ["cat", "dog", "bird", "fish"]
```

Implement it WITHOUT using `set()` directly (to understand the logic),
then compare with the `set`-based approach (which doesn't preserve order).

---

## Exercise 5 — Matrix Operations

Represent a 3×3 matrix as a list of lists. Implement:
1. `get_row(matrix, i)` → returns row i
2. `get_col(matrix, j)` → returns column j
3. `transpose(matrix)` → returns the transposed matrix

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(get_row(matrix, 1))   # [4, 5, 6]
print(get_col(matrix, 2))   # [3, 6, 9]
print(transpose(matrix))
# [[1, 4, 7],
#  [2, 5, 8],
#  [3, 6, 9]]
```

---

## Stretch Challenge — Weighted Moving Average

Implement a `wma(values, window)` function that computes a weighted moving average
where more recent values have higher weight.

For a window of size 3, weights are: `[1, 2, 3]` (oldest to newest).
Normalized: `[1/6, 2/6, 3/6]`.

```python
prices = [10, 11, 12, 13, 14, 15, 16]
wma_values = wma(prices, window=3)
# For index 2 (first complete window): (10×1 + 11×2 + 12×3) / 6 = 11.33
```

This is the same formula used in technical analysis and time-series forecasting.
