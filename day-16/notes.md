# Day 16 Notes — File Handling

## The `open()` Function

```python
open(file, mode="r", encoding="utf-8")
```

| Mode | Description |
|------|-------------|
| `"r"` | Read (default). File must exist. |
| `"w"` | Write. Creates file or **overwrites** existing. |
| `"a"` | Append. Creates file or adds to end. |
| `"x"` | Create. Fails if file already exists. |
| `"rb"` / `"wb"` | Binary read/write (for images, models) |

---

## Always Use `with` (Context Manager)

```python
# BAD — file may never close if exception occurs
f = open("data.txt")
data = f.read()
f.close()

# GOOD — `with` guarantees file is closed
with open("data.txt", "r") as f:
    data = f.read()
```

The `with` statement calls `f.__enter__()` on enter and `f.__exit__()` on exit (even if an error occurs). Day 23 covers context managers in depth.

---

## Read Methods

```python
with open("file.txt") as f:
    content   = f.read()       # entire file as one string
    lines_str = f.read()       # ← only works once! seek back with f.seek(0)

with open("file.txt") as f:
    first_line = f.readline()  # one line at a time

with open("file.txt") as f:
    all_lines = f.readlines()  # list of strings, each ending with \n

# Most memory-efficient — iterates lazily:
with open("file.txt") as f:
    for line in f:             # generator — reads one line at a time
        process(line.strip())
```

---

## JSON — The AI Data Format

JSON (JavaScript Object Notation) is the universal format for:
- Model config files (`config.json`)
- API request/response bodies
- Dataset metadata
- Experiment results

```python
import json

# Python → JSON string
data = {"model": "gpt-4", "tokens": 512}
json_str = json.dumps(data, indent=4)

# JSON string → Python
parsed = json.loads(json_str)

# Python → JSON file
with open("config.json", "w") as f:
    json.dump(data, f, indent=4)

# JSON file → Python
with open("config.json", "r") as f:
    config = json.load(f)
```

### Type Mapping

| Python | JSON |
|--------|------|
| `dict` | object `{}` |
| `list` | array `[]` |
| `str` | string `""` |
| `int`/`float` | number |
| `True`/`False` | `true`/`false` |
| `None` | `null` |

---

## JSONL (JSON Lines) — Large Dataset Format

One JSON object per line. Used for large ML datasets.

```
{"id": 1, "text": "hello", "label": "positive"}
{"id": 2, "text": "world", "label": "negative"}
```

```python
# Read JSONL
with open("data.jsonl") as f:
    records = [json.loads(line) for line in f if line.strip()]

# Write JSONL
with open("output.jsonl", "w") as f:
    for record in records:
        f.write(json.dumps(record) + "\n")
```

---

## CSV Files

```python
import csv

# Write
with open("data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "text", "label"])
    writer.writeheader()
    writer.writerows([{"id": 1, "text": "hello", "label": "pos"}])

# Read
with open("data.csv") as f:
    reader = csv.DictReader(f)    # each row is a dict!
    for row in reader:
        print(row["label"])
```

---

## pathlib — Modern File Paths

```python
from pathlib import Path

p = Path("data/train/samples.csv")

# Properties
p.name       # "samples.csv"
p.stem       # "samples"
p.suffix     # ".csv"
p.parent     # Path("data/train")
p.parts      # ("data", "train", "samples.csv")

# Checks
p.exists()   # True/False
p.is_file()  # True/False
p.is_dir()   # True/False

# Create directory (like mkdir -p)
p.parent.mkdir(parents=True, exist_ok=True)

# Simple read/write
Path("output.txt").write_text("results here")
content = Path("input.txt").read_text()
```

---

## Encoding

Always specify encoding when dealing with international text (NLP datasets):

```python
with open("arabic_text.txt", "r", encoding="utf-8") as f:
    text = f.read()
```

UTF-8 is the standard for NLP. Never skip encoding for text data.

---

## Real-World AI File Patterns

```python
# Load experiment checkpoint
def load_checkpoint(checkpoint_dir: str) -> dict:
    path = Path(checkpoint_dir) / "checkpoint.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())

# Save results with timestamped filename
from datetime import datetime
def save_results(results: list, run_name: str) -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path("outputs") / f"{run_name}_{ts}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
```

---

## Quick-Fire Interview Questions

1. **What's the difference between `read()` and `readlines()`?**  
   `read()` returns entire file as string; `readlines()` returns list of line strings.

2. **Why use `with open(...)` instead of `open()` + `close()`?**  
   `with` guarantees file closure even if an exception is raised.

3. **What's `json.dumps()` vs `json.dump()`?**  
   `dumps()` → serialize to string; `dump()` → serialize to file.

4. **What mode creates a file and fails if it already exists?**  
   `"x"` (exclusive creation mode).

5. **What does `newline=""` do in `open()` for CSV?**  
   Prevents Python from adding extra `\r\n` on Windows; required for `csv` module.
