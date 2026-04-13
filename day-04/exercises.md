# Day 4 Exercises — Loops

Estimated time: 25–35 minutes

---

## Exercise 1 — Training Epoch Simulator

Simulate a training loop that:
1. Starts with `loss = 2.0` and `accuracy = 0.0`
2. Each epoch, loss decreases by 15% and accuracy increases by 8% (capped at 1.0)
3. Loop runs until `loss < 0.15` OR `accuracy >= 0.95` OR `epoch > 100`
4. Print a status line per epoch:
```
Epoch  1 | Loss: 1.7000 | Accuracy: 8.00%
Epoch  2 | Loss: 1.4450 | Accuracy: 15.68%
...
```
5. After the loop, print WHY it stopped (loss threshold / accuracy threshold / max epochs)

---

## Exercise 2 — Batch Generator

Write a function `create_batches(data, batch_size)` that:
1. Takes a list and a batch size
2. Returns a list of batches (each batch is a sub-list)
3. The last batch may be smaller than `batch_size`

```python
data = list(range(1, 11))   # [1, 2, ..., 10]
batches = create_batches(data, 3)
# Expected: [[1,2,3], [4,5,6], [7,8,9], [10]]
```

Use only a `for` loop and `range()` with a step — no slicing tricks yet (or try both!).

---

## Exercise 3 — Vocabulary Builder

Given a list of sentences, build a vocabulary dictionary:
- Keys: unique words (lowercased, stripped of punctuation)
- Values: number of times the word appears across all sentences

```python
corpus = [
    "The cat sat on the mat.",
    "The cat ate the rat.",
    "The rat sat on a mat.",
]
```

Print the top 5 most frequent words with a bar chart (use `"█" * count`).

---

## Exercise 4 — Duplicate Detector

Given a list of user IDs, find all duplicates and print them (without using sets — use only loops and conditionals to understand the process, then optimize with a set).

```python
user_ids = [101, 203, 101, 450, 203, 789, 101, 999]
```

Expected output:
```
Duplicates found: [101, 203]
```

**Bonus**: Re-implement using a `set` and compare the approach.

---

## Exercise 5 — Nested Loop: Confusion Matrix Printer

Given a list of true labels and predicted labels:

```python
true_labels = [0, 1, 2, 0, 1, 2, 0, 1, 2]
pred_labels = [0, 2, 2, 0, 0, 2, 1, 1, 2]
num_classes = 3
```

Build and print a 3×3 confusion matrix using nested loops.

Expected:
```
Confusion Matrix:
     Pred 0  Pred 1  Pred 2
True 0   2       1       0
True 1   1       1       1
True 2   0       0       2
```

(No libraries — just loops and list indexing.)

---

## Stretch Challenge — Token Frequency Analyzer

Given a long text (paste any paragraph), write a script that:
1. Counts word frequencies
2. Removes common stop words: `["the", "a", "an", "is", "are", "was", "of", "in", "to", "and"]`
3. Prints the top 10 remaining words sorted by frequency
4. Also prints the total unique word count

Use `for` loops, `dict.get()`, and `sorted()` with a `key` argument.
