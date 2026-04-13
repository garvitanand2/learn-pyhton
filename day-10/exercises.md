# Day 10 Exercises — Dictionaries

Estimated time: 30–40 minutes

---

## Exercise 1 — Config Resolver

Write a `resolve_config(user_config)` function that:
1. Starts with these defaults:
   ```python
   DEFAULTS = {"temperature": 0.7, "max_tokens": 512, "top_p": 1.0, "n": 1, "stream": False}
   ```
2. Merges the user config on top (user wins)
3. Validates: temperature ∈ [0.0, 2.0], max_tokens ∈ [1, 32000], n ∈ [1, 10]
4. Returns the final merged config or raises `ValueError` with a clear message

```python
resolve_config({"temperature": 0.2, "max_tokens": 2048})
resolve_config({"temperature": 5.0})   # should raise ValueError
```

---

## Exercise 2 — Word Frequency Counter

Write `word_frequency(text)` using only basic dict operations (no Counter):
1. Lowercases and splits the text
2. Strips punctuation from each word
3. Returns a dict of `{word: count}` sorted by count descending
4. Also returns the top-3 most common words

```python
text = """
Transformers changed the world of NLP. Transformers use attention and attention
is all you need. The transformer model is now everywhere in AI.
"""
```

---

## Exercise 3 — Inverted Index Builder

An inverted index maps each word to the list of document IDs that contain it.
This is how search engines work.

```python
documents = {
    0: "the cat sat on the mat",
    1: "the dog ran in the park",
    2: "the cat and the dog played",
    3: "sat and played are common verbs",
}
```

Build `{word: [doc_id, ...]}` using `defaultdict(list)`.  
Then write `search(index, query)` that returns doc IDs containing ALL query words.

```python
search(index, "cat dog")    # → [2]  (both appear in doc 2)
search(index, "the sat")    # → [0]  (both in doc 0)
```

---

## Exercise 4 — Confusion Matrix as Dict

Build a confusion matrix represented as a nested dict:
`{true_label: {predicted_label: count}}`

```python
true_labels = ["cat", "dog", "cat", "bird", "dog", "cat", "bird", "dog"]
pred_labels = ["cat", "dog", "dog", "bird", "cat", "cat", "bird", "dog"]
```

Then compute and print precision for each class:
```
precision(class) = TP / (TP + FP)
```

---

## Exercise 5 — LRU Cache Simulation

Implement a simple LRU (Least Recently Used) cache using an `OrderedDict` from `collections`. It should:
1. Store up to `capacity` items
2. On `get(key)` — return the value (or -1 if not found); mark as recently used
3. On `put(key, value)` — store it; evict the least recently used item if at capacity

```python
from collections import OrderedDict

cache = LRUCache(capacity=3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
print(cache.get("a"))    # 1
cache.put("d", 4)        # evicts "b" (least recently used)
print(cache.get("b"))    # -1 (evicted)
```

This is a classic interview question + used heavily in real caching systems.

---

## Stretch Challenge — JSON Flattener

Flatten a deeply nested dictionary with dot notation:

```python
data = {
    "model": {
        "name": "gpt-4",
        "settings": {
            "temperature": 0.7,
            "sampling": {
                "top_k": 50,
                "top_p": 0.9
            }
        }
    },
    "meta": {
        "version": "v2",
        "created": "2024-01-01"
    }
}

# Expected:
# {
#   "model.name": "gpt-4",
#   "model.settings.temperature": 0.7,
#   "model.settings.sampling.top_k": 50,
#   "model.settings.sampling.top_p": 0.9,
#   "meta.version": "v2",
#   "meta.created": "2024-01-01"
# }
```

Then write the reverse: `unflatten(flat_dict)` that reconstructs the nested structure.
