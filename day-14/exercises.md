# Day 14 Exercises — Week 2 Mini Project Extensions

Estimated time: 45–60 minutes

---

## Exercise 1 — Extend the Profiler: Confidence Statistics

Add a new section to the report: "CONFIDENCE DISTRIBUTION".

The dataset has confidence scores (hypothetically). Add them:

```python
import random
random.seed(42)
for r in DATASET:
    r["confidence"] = round(random.uniform(0.5, 1.0), 3)
```

Then add to the profile:
- Mean confidence per label
- Percentage of samples with confidence >= 0.9
- Minimum confidence sample per label (potential label noise)

---

## Exercise 2 — Class Imbalance Handler

Write a function `resample_balanced(dataset, strategy="oversample")`:

- `"oversample"`: duplicate minority class samples until all classes have equal count
- `"undersample"`: remove majority class samples until all classes have equal count

```python
balanced = resample_balanced(DATASET, strategy="oversample")
profile = profile_dataset(balanced)
print(profile["label_distribution"])   # should be equal counts
```

---

## Exercise 3 — N-gram Co-occurrence

Extend the vocabulary analysis with **bigrams** (2-word pairs):

For each label, find the top 5 most frequent bigrams (consecutive word pairs).

Bigrams are used in:
- Phrase detection
- N-gram language models
- Keyword extraction

Expected output:
```
BIGRAM ANALYSIS
positive: [model predicted, high confidence, benchmark results...]
negative: [completely failed, training loss, memory usage...]
```

---

## Exercise 4 — Data Splitter Validation

After splitting the dataset into train/val/test, verify:
1. No data leakage (same `id` appears in multiple splits)
2. All splits together reconstruct the full dataset
3. Class distribution is similar across splits (compare ratios)

Write assertions and print a "Validation: PASSED / FAILED" summary.

---

## Exercise 5 — Export to Multiple Formats

Write functions to export the profiling results:

1. `to_json(profile, filename)` → save as JSON (preview Day 16)
2. `to_csv_summary(profile, filename)` → save label stats as CSV lines
3. `to_markdown(profile)` → return a Markdown formatted string report

For now, print the CSV and Markdown outputs to console (file writing in Day 16).

---

## Stretch Challenge — Anomaly Detector

Build `detect_anomalies(dataset)` that finds suspicious samples:

1. **Length anomalies**: texts more than 2 standard deviations from the mean word count
2. **Label-text mismatch**: texts containing strongly negative words but labeled "positive" (and vice versa)
   - Negative keywords: `["failed", "error", "terrible", "bad", "wrong", "poor"]`
   - Positive keywords: `["excellent", "great", "best", "stellar", "outstanding"]`
3. **Near-duplicates**: texts that share 80%+ of their words (sort tokens, compare sets)

Return a list of anomaly dicts with `type`, `id`, and `reason`.
