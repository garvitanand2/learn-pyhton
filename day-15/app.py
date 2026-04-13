# Day 15: Modules & Packages
# Focus: Organizing Python for scalable AI projects

# ============================================================
# WHAT: A module is any .py file. A package is a directory
#       with an __init__.py. Python ships with hundreds of
#       built-in modules (the Standard Library).
# WHY:  Real AI projects have dozens of files — importing
#       the right utilities keeps your code clean and reusable.
# ============================================================

import os
import sys
import math
import random
import time
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path
from functools import partial

# ============================================================
# 1. os Module — filesystem and environment
# ============================================================
print("=== 1. os Module ===")

cwd = os.getcwd()
print(f"Current directory: {cwd}")

# Build file paths cross-platform (works on Windows & Mac/Linux)
config_path = os.path.join("models", "bert-base", "config.json")
print(f"Config path:  {config_path}")

# Environment variables — common for API keys, settings
api_key = os.environ.get("OPENAI_API_KEY", "NOT_SET")
print(f"API Key set: {api_key != 'NOT_SET'}")

# ============================================================
# 2. pathlib — Modern, object-oriented filesystem
# ============================================================
print("\n=== 2. pathlib ===")

p = Path(".")
print(f"Resolved path:  {p.resolve()}")
print(f"Parent:         {p.resolve().parent}")

# Check extensions, stems
log_file = Path("training_run_2024.log")
print(f"Stem:      {log_file.stem}")
print(f"Extension: {log_file.suffix}")

# ============================================================
# 3. math — Mathematical utilities
# ============================================================
print("\n=== 3. math Module ===")

# Log — used in cross-entropy loss: -log(p)
prob = 0.85
loss = -math.log(prob)
print(f"Cross-entropy loss (p=0.85): {loss:.4f}")

# Ceil / floor — batch size calculations
total_samples = 10_000
batch_size = 64
num_batches = math.ceil(total_samples / batch_size)
print(f"Batches needed: {num_batches}")

# Sigmoid approximation using math.exp
def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

print(f"sigmoid(0)   = {sigmoid(0):.4f}")
print(f"sigmoid(2)   = {sigmoid(2):.4f}")
print(f"sigmoid(-2)  = {sigmoid(-2):.4f}")

# ============================================================
# 4. random — Controlled randomness (seed = reproducibility)
# ============================================================
print("\n=== 4. random Module ===")

random.seed(42)          # Fix seed → same results every run
sample = random.sample(range(1000), 10)
print(f"Random sample: {sample}")

# Shuffle a dataset before training (in-place!)
data = list(range(20))
random.shuffle(data)
print(f"Shuffled: {data}")

# random.choice → simulate label sampling
labels = ["positive", "negative", "neutral"]
picked = random.choice(labels)
print(f"Random label: {picked}")

# ============================================================
# 5. datetime — Timestamps for experiment tracking
# ============================================================
print("\n=== 5. datetime Module ===")

now = datetime.now()
run_id = now.strftime("%Y%m%d_%H%M%S")
print(f"Run ID:        {run_id}")
print(f"Readable time: {now.strftime('%B %d, %Y at %I:%M %p')}")

# ============================================================
# 6. collections — Specialized data structures
# ============================================================
print("\n=== 6. collections Module ===")

# Counter — instant frequency table (great for label analysis)
labels = ["pos", "neg", "pos", "neu", "pos", "neg", "pos"]
dist = Counter(labels)
print(f"Label dist: {dict(dist)}")
print(f"Most common: {dist.most_common(2)}")

# defaultdict — avoid KeyError when building indexes
inverted_index: dict = defaultdict(list)
documents = [
    (0, "machine learning model"),
    (1, "deep learning model"),
    (2, "machine translation"),
]
for doc_id, text in documents:
    for word in text.split():
        inverted_index[word].append(doc_id)

print(f"inverted_index['model']: {inverted_index['model']}")
print(f"inverted_index['deep']: {inverted_index['deep']}")

# ============================================================
# 7. functools.partial — Fix arguments for reusable functions
# ============================================================
print("\n=== 7. functools.partial ===")

def scale(value: float, factor: float) -> float:
    return value * factor

# Create specialized versions
normalize_to_255 = partial(scale, factor=255.0)
normalize_to_100 = partial(scale, factor=100.0)

print(f"0.5 → 255 scale: {normalize_to_255(0.5)}")
print(f"0.5 → 100 scale: {normalize_to_100(0.5)}")

# ============================================================
# 8. __name__ == "__main__" — Module Guard
# ============================================================
# This is the most important pattern for reusable modules.
#
# When Python runs a file → __name__ = "__main__"
# When Python IMPORTS a file → __name__ = "module_name"
#
# This means: code inside `if __name__ == "__main__":` 
# ONLY runs when the file is executed directly, NOT when
# another module imports it.
#
# Example project structure:
#   my_project/
#     __init__.py       ← makes it a package
#     config.py         ← constants and config
#     preprocessing.py  ← text cleaning utilities
#     evaluation.py     ← metrics and reporting
#     main.py           ← entry point (imports the others)

def get_system_info() -> dict:
    """Collect system info for experiment logging."""
    return {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "run_time": datetime.now().isoformat(),
    }

if __name__ == "__main__":
    print("\n=== Running as Script (not imported) ===")
    info = get_system_info()
    for k, v in info.items():
        print(f"  {k}: {v}")
    print("\nDay 15 complete! Modules are the backbone of real Python projects.")
