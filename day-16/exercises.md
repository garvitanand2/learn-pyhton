# Day 16 Exercises — File Handling

Estimated time: 45–60 minutes

---

## Exercise 1 — Training Log Writer

Write a function `log_epoch(log_file, epoch, loss, accuracy)` that **appends** one line to a log file in this format:

```
2024-01-15 14:32:01 | Epoch  3 | Loss: 0.3456 | Accuracy: 87.23%
```

Then:
1. Simulate 10 epochs (with `random` generated losses and accuracies)
2. Read the log back and find the epoch with the **lowest loss**
3. Find the epoch with the **highest accuracy**
4. Print a summary

---

## Exercise 2 — Config Manager

Build a `ConfigManager` class that:

1. `load(path)` — reads a JSON file and stores config internally
2. `get(key, default=None)` — safe key access
3. `set(key, value)` — update a value
4. `save(path)` — write updated config back to JSON

Create a config file with at least 5 model settings, load it, update the learning rate, and save it back. Verify the saved file contains the new value.

---

## Exercise 3 — JSONL Dataset Builder

Build a simple dataset pipeline:

1. `create_dataset(records, output_path)` — takes a list of dicts and writes each as a JSON line  
2. `load_dataset(path)` — reads a JSONL file and returns list of dicts  
3. `filter_dataset(records, label)` — returns only records with the given label  
4. `dataset_stats(records)` — returns `{total, by_label: {label: count}}`

Test with at least 10 records across 3 labels.

---

## Exercise 4 — CSV Data Cleaner

Write a function `clean_csv(input_path, output_path)` that:
1. Reads a CSV with columns: `id, text, label`
2. Removes rows where `text` is empty or shorter than 3 characters
3. Converts all `label` values to lowercase
4. Strips whitespace from all fields
5. Writes the cleaned data to a new CSV
6. Returns `(total_rows, kept_rows, removed_rows)`

---

## Exercise 5 — Multi-File Experiment Saver

Write `save_experiment(experiment)` where `experiment` is a dict:

```python
{
    "run_id": "run_001",
    "config": {...},
    "metrics": {"epochs": [...]},
    "errors": ["...log messages..."]
}
```

The function should:
1. Create a folder `experiments/{run_id}/`
2. Save `config.json` with just the config
3. Save `metrics.json` with just the metrics
4. Save `errors.log` as a text file (one error per line)
5. Save `summary.json` with `run_id` + final epoch's loss and accuracy

---

## Stretch Challenge — Vocabulary Builder

Write a complete pipeline:

1. `read_corpus(path)` — reads a text file of sentences (one per line)
2. `build_vocab(sentences)` — returns `{word: count}` dict sorted by frequency
3. `save_vocab(vocab, path)` — saves as JSON with `{word: count}` pairs
4. `load_vocab(path)` → loads and returns the vocab dict
5. `top_k_words(vocab, k=100)` → returns top-k words by count

Test with a paragraph of text you write yourself (at least 20 sentences). Check that the vocabulary file is saved correctly.
