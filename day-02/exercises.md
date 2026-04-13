# Day 2 Exercises — Operators & Input/Output

Estimated time: 20–30 minutes

---

## Exercise 1 — Loss Metrics Calculator

Given a list of predicted vs actual values:

```python
actual    = [3.0, 5.0, 2.5, 7.0, 4.0]
predicted = [2.8, 5.3, 2.0, 6.5, 4.2]
```

Calculate and print:
1. **MAE** — Mean Absolute Error: average of `|actual - predicted|`
2. **MSE** — Mean Squared Error: average of `(actual - predicted)²`
3. **RMSE** — Root Mean Squared Error: `√MSE` (use `** 0.5`)

Expected formatting:
```
MAE  : 0.3400
MSE  : 0.1580
RMSE : 0.3975
```

---

## Exercise 2 — Batch Partitioner

Write a script that:
1. Sets `dataset_size = 5000` and `batch_size = 128`
2. Computes the number of full batches
3. Computes the size of the last partial batch (if any)
4. Prints a summary table using f-string alignment:

```
Dataset size  :  5000
Batch size    :   128
Full batches  :    39
Last batch    :     8
```

---

## Exercise 3 — Threshold Decision

A spam classifier returns confidence scores:

```python
scores = [0.92, 0.45, 0.78, 0.31, 0.88, 0.55]
```

For each score, use comparison operators to print whether it's:
- `SPAM` if score >= 0.75
- `UNSURE` if 0.50 <= score < 0.75
- `NOT SPAM` if score < 0.50

(Try to use chained comparisons and logical operators. You'll need a loop — use `for score in scores:`)

---

## Exercise 4 — Operator Precedence Puzzle

Predict the output of each expression **without running it** first, then verify:

```python
print(2 + 3 * 4)        # ?
print((2 + 3) * 4)      # ?
print(2 ** 3 ** 2)      # ?
print(10 - 4 / 2)       # ?
print(10 - 4 // 2)      # ?
print(5 % 3 + 1)        # ?
print(not True or False and True)  # ?  (operator precedence with not/and/or)
```

Write a comment next to each line explaining the order of operations.

---

## Exercise 5 — AI Training Report Formatter

Write a function (or just a script) that prints a training summary table for
3 epochs with the following data:

```python
epoch_data = [
    {"epoch": 1, "loss": 0.9832, "accuracy": 0.6120},
    {"epoch": 2, "loss": 0.5421, "accuracy": 0.7845},
    {"epoch": 3, "loss": 0.2834, "accuracy": 0.9012},
]
```

Format it as:
```
Epoch  |   Loss   | Accuracy
-------|----------|----------
  1    |  0.9832  |  61.20%
  2    |  0.5421  |  78.45%
  3    |  0.2834  |  90.12%
```

Use f-string format specs for alignment and decimal places.

---

## Stretch Challenge — Interactive Metric Calculator

Build a simple CLI tool (using `input()`) that:
1. Asks for true value and predicted value
2. Calculates and prints: absolute error, squared error, percentage error
3. Handles the case where `true_value == 0` (division by zero in % error)
   — print `"Cannot compute % error: true value is zero"` in that case
