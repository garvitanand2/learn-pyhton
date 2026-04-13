# Day 13 Notes — Nested Data Structures

## What & Why

Real-world data is nested. API responses are JSON. Datasets are lists of dicts.
Configs are nested dicts. Conversation history is a list of dicts with nested content.
Every AI system you build will involve navigating and transforming nested data.

---

## Common Nested Patterns

### List of Dicts (Dataset Records)
```python
dataset = [
    {"id": 1, "text": "...", "label": "positive", "score": 0.92},
    {"id": 2, "text": "...", "label": "negative", "score": 0.88},
]
```
**Access**: `dataset[0]["label"]`  
**Filter**: `[r for r in dataset if r["score"] > 0.9]`  
**Sort**: `sorted(dataset, key=lambda r: r["score"])`

### Dict of Dicts (Config Tree)
```python
config = {
    "model": {"name": "gpt-4", "settings": {"lr": 0.001}},
    "eval":  {"metric": "f1", "threshold": 0.8}
}
```
**Access**: `config["model"]["settings"]["lr"]`  
**Safe access**: `config.get("model", {}).get("settings", {}).get("lr", 0.001)`

### Nested Lists (Matrix / Grid)
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matrix[1][2]  # row 1, col 2 → 6
```

---

## Safe Deep Access

Regular `d["key"]["subkey"]` raises `KeyError` if any key is missing.

**Pattern 1**: Chained `.get()`
```python
lr = config.get("model", {}).get("settings", {}).get("lr", 0.001)
```

**Pattern 2**: Helper function
```python
def deep_get(d, *keys, default=None):
    for key in keys:
        d = d.get(key, default) if isinstance(d, dict) else default
    return d
```

**Pattern 3**: `try/except KeyError` (Day 17)
```python
try:
    lr = config["model"]["settings"]["lr"]
except KeyError:
    lr = 0.001
```

---

## Deep Copy vs Shallow Copy

This is critical and often causes subtle bugs in data pipelines:

```python
import copy

original = {"data": [{"x": 1}, {"x": 2}]}

# Shallow copy — nested objects are SHARED
shallow = original.copy()           # or dict(original)
shallow["data"][0]["x"] = 99       # also changes original["data"][0]["x"]!

# Deep copy — completely independent
deep = copy.deepcopy(original)
deep["data"][0]["x"] = 99          # original is unchanged
```

**Rule**: Use `copy.deepcopy()` when you need to modify nested data without
affecting the original. It's slower but safe.

---

## JSON Serialization

```python
import json

# Python dict → JSON string
json_str = json.dumps(data, indent=2)

# JSON string → Python dict
data = json.loads(json_str)

# Write to file
with open("config.json", "w") as f:
    json.dump(data, f, indent=2)

# Read from file
with open("config.json") as f:
    data = json.load(f)
```

**JSON ↔ Python type mapping**:
| JSON | Python |
|------|--------|
| object | dict |
| array | list |
| string | str |
| number | int or float |
| true/false | True/False |
| null | None |

---

## Grouping with defaultdict

```python
from collections import defaultdict

by_label = defaultdict(list)
for record in dataset:
    by_label[record["label"]].append(record)

# Result: {"positive": [...], "negative": [...], "neutral": [...]}
```

---

## Real-World Analogy

A nested data structure is like a **folder hierarchy on your hard drive**:
- Top level: categories (models, datasets, configs)
- Second level: sub-categories or named resources
- Leaf level: actual values (numbers, strings)

Navigating it requires knowing the "path" to each value — just like a file path.

---

## Interview Quick-Fire

1. **How do you safely access deeply nested dict keys?**
   → Chain `.get()` calls with empty dict defaults: `d.get("k1", {}).get("k2", {}).get("k3", default)`. Or use a custom `deep_get()` helper.

2. **What is the difference between shallow and deep copy?**
   → Shallow copy duplicates the outer container but shares references to nested objects. Deep copy recursively duplicates everything. Use `copy.deepcopy()` for full independence.

3. **How do you convert a Python dict to JSON?**
   → `json.dumps(d)` → string; `json.dump(d, file)` → write to file.

4. **What Python types cannot be serialized to JSON?**
   → `set`, `tuple` (becomes list), `datetime`, custom objects. You need a custom encoder for these.

5. **How do you sort a list of dicts by a nested key?**
   → `sorted(data, key=lambda x: x["outer"]["inner"])`
