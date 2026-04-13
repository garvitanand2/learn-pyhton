# Day 15 Notes — Modules & Packages

## What is a Module?

A **module** is simply a `.py` file. Any `.py` file you write is automatically a module.

```python
# utils.py  ← this IS a module
def clean_text(text): ...
def tokenize(text): ...
```

```python
# main.py
import utils          # import the whole module
utils.clean_text("Hello!")

from utils import tokenize  # import specific function
tokenize("Hello!")
```

---

## What is a Package?

A **package** is a folder containing an `__init__.py` file.

```
my_nlp_project/
├── __init__.py         ← makes this folder a package
├── preprocessing.py
├── evaluation.py
├── config.py
└── main.py
```

```python
from my_nlp_project import preprocessing
from my_nlp_project.evaluation import compute_f1
```

---

## Import Styles

| Style | Example | Use when |
|---|---|---|
| `import module` | `import os` | Need multiple things from module |
| `from module import x` | `from math import sqrt` | Need one specific thing |
| `from module import *` | `from os import *` | ⚠️ Avoid — pollutes namespace |
| `import module as alias` | `import numpy as np` | Long module name |
| `from module import x as y` | `from datetime import datetime as dt` | Rename for clarity |

---

## The Standard Library (Free Tools)

Python ships with a vast standard library — you don't need `pip install` for these:

| Module | Purpose | AI Use |
|---|---|---|
| `os` | Filesystem, env vars | Check paths, read env keys |
| `pathlib` | Modern filesystem | Build cross-platform paths |
| `math` | Math functions | log, exp, ceil for ML math |
| `random` | Random numbers | Data shuffling, sampling |
| `datetime` | Dates & times | Experiment run IDs |
| `collections` | Counter, deque, defaultdict | Frequency analysis |
| `functools` | partial, lru_cache, reduce | Memoization, currying |
| `itertools` | chain, product, cycle | Batch iteration |
| `json` | JSON encode/decode | Config files, API responses |
| `re` | Regular expressions | Text preprocessing |
| `sys` | Python interpreter | sys.path, sys.argv |
| `time` | Time utilities | Benchmarking |
| `typing` | Type hints | Code documentation |

---

## The `__name__` Guard — Critical Pattern

```python
# my_module.py

def train_model(data):
    print("Training...")

# This code ONLY runs when you run: python my_module.py
# It is SKIPPED when someone imports this module
if __name__ == "__main__":
    data = load_data()
    train_model(data)
```

**Why this matters:**  
When building a reusable module, you want colleagues to be able to `import` it without triggering all your test/demo code. The guard ensures the module does nothing when imported — only when run directly.

---

## `sys.path` — Python's Module Search Order

When you write `import something`, Python searches:
1. Current directory
2. Standard library directories
3. Installed packages (site-packages)

```python
import sys
print(sys.path)  # list of directories Python searches
```

You can add custom paths:
```python
sys.path.append("/path/to/my/custom/modules")
```

---

## `pathlib.Path` — The Modern Way

```python
from pathlib import Path

p = Path("/home/user/project")

# Navigation
p / "data" / "train.csv"        # /home/user/project/data/train.csv

# Properties
p.name                          # "project"
p.parent                        # /home/user
p.suffix                        # "" (no extension)

# Checks
p.exists()                      # True/False
p.is_file()                     # True if file
p.is_dir()                      # True if directory

# Read/write (preview of Day 16)
text = Path("file.txt").read_text()
Path("output.txt").write_text("results")
```

---

## AI / Production Patterns

### Config module pattern
```python
# config.py
MAX_TOKENS = 512
BATCH_SIZE = 32
LEARNING_RATE = 3e-5
MODEL_NAME = "bert-base-uncased"
```

### Lazy imports (avoiding slow startup)
```python
def load_model():
    import torch          # imported only when function is called
    return torch.load(...)
```

### `__all__` — Control public API
```python
# preprocessing.py
__all__ = ["clean_text", "tokenize"]  # only these are exposed on `from x import *`
def clean_text(): ...
def tokenize(): ...
def _internal_helper(): ...  # underscore = "private"
```

---

## Quick-Fire Interview Questions

1. **What's the difference between a module and a package?**  
   Module = single .py file; Package = directory with `__init__.py`

2. **What does `if __name__ == "__main__":` do?**  
   Runs code only when the file is executed directly, not when imported.

3. **What is `__init__.py`?**  
   Marks a directory as a Python package; can also run package-level setup code.

4. **What is `sys.path`?**  
   List of directories Python searches when resolving `import` statements.

5. **What's the difference between `import math` and `from math import sqrt`?**  
   First loads the module object; second imports only `sqrt` into current namespace.
