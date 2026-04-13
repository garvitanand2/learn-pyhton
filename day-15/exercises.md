# Day 15 Exercises — Modules & Packages

Estimated time: 30–45 minutes

---

## Exercise 1 — Standard Library Exploration

Use only Python standard library modules (no pip install).

Write a script that:
1. Uses `os.listdir(".")` to list files in the current directory
2. Filters to show only `.py` files using a list comprehension
3. For each `.py` file, print its name and size using `os.path.getsize()`
4. Prints the total size in KB

**Bonus:** Use `pathlib.Path` to do the same thing with `Path(".").glob("*.py")`.

---

## Exercise 2 — Experiment Timer

Using `time` and `datetime`:

1. Write a function `timed_run(func, *args)` that:
   - Records start time with `time.perf_counter()`
   - Calls `func(*args)`
   - Records end time
   - Returns `(result, elapsed_seconds)`

2. Test it with:
   - A function that sorts a list of 100,000 random integers
   - A loop that runs 1,000,000 iterations

3. Format the output: `"sort took 0.0423 seconds"`

---

## Exercise 3 — Build a Config Module (Simulated)

Simulate a `config.py` module by defining a dictionary at the top of your script:

```python
CONFIG = {
    "model_name": "bert-base-uncased",
    "max_tokens": 512,
    "batch_size": 32,
    "learning_rate": 3e-5,
    "num_epochs": 10,
    "device": "cuda",
    "seed": 42,
}
```

Then write:
1. `validate_config(config)` — checks that all required keys exist and values are valid types
2. `print_config(config)` — prints a formatted table of all settings
3. `update_config(config, **overrides)` — returns a new config dict with overrides applied

---

## Exercise 4 — Enhanced `Counter` Analysis

Use `collections.Counter` to analyze a list of model predictions:

```python
predictions = ["positive"]*45 + ["negative"]*30 + ["neutral"]*25
```

1. Count each label
2. Calculate percentage for each label
3. Find the majority and minority class
4. Simulate what happens if you add 20 more "positive" predictions
5. Find the difference using Counter arithmetic: `new_dist - old_dist`

---

## Exercise 5 — Module Guard Practice

Write a file (conceptually) that contains:
1. A function `generate_run_id()` that returns a timestamp-based string like `"run_20240115_143022"`
2. A function `setup_directories(run_id)` that returns a list of paths that would be created: `["runs/{run_id}/checkpoints", "runs/{run_id}/logs", "runs/{run_id}/outputs"]`
3. A `main()` function that calls both and prints results
4. A proper `if __name__ == "__main__": main()` guard

---

## Stretch Challenge — Build a Mini Package Structure

Create a mental model for this package:

```
ml_toolkit/
├── __init__.py
├── preprocessing/
│   ├── __init__.py
│   └── text.py
├── evaluation/
│   ├── __init__.py
│   └── metrics.py
└── utils/
    ├── __init__.py
    └── io.py
```

Write out (in Python, in one file using classes/functions to simulate):
- `text.py`: `clean()`, `tokenize()`, `pad_sequences()` functions
- `metrics.py`: `accuracy()`, `f1_score()`, `confusion_matrix()` functions
- `io.py`: `save_json()`, `load_json()` functions with realistic docstrings

Then demonstrate how you'd "import" them as if the package existed.
