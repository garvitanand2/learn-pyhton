# =============================================================
# Day 10: Dictionaries — Deep Dive
# Goal: Master the most versatile data structure in Python AI.
#       Dicts represent configs, model outputs, API responses,
#       feature vectors, and cached results — everywhere.
# =============================================================

# --- 1. CREATING DICTIONARIES --------------------------------
# What: Ordered (Python 3.7+), mutable, key-value pairs, unique keys
# Why:  Named access to data — configs, records, counters, caches

model_config = {
    "model":        "gpt-4",
    "temperature":  0.7,
    "max_tokens":   1024,
    "stream":       True,
    "stop":         ["\n\n", "END"],   # values can be any type
}

# Other creation methods
from_pairs     = dict([("lr", 0.001), ("epochs", 100)])
from_keywords  = dict(model="bert", task="classification")
empty          = {}

print(f"Config  : {model_config}")
print(f"Pairs   : {from_pairs}")
print(f"Keywords: {from_keywords}")

# --- 2. ACCESSING VALUES -------------------------------------

# Direct access — KeyError if missing
print(f"\nModel    : {model_config['model']}")
print(f"Max tok  : {model_config['max_tokens']}")

# .get() — safe access with optional default (use this!)
timeout = model_config.get("timeout", 30)     # key missing → returns 30
print(f"Timeout  : {timeout}")

api_key = model_config.get("api_key")         # missing → returns None
print(f"API key  : {api_key}")

# --- 3. ADDING, UPDATING, DELETING ---------------------------

config = model_config.copy()

# Add new key
config["top_p"] = 0.95
print(f"\nAfter add: {list(config.keys())}")

# Update existing
config["temperature"] = 0.2
print(f"Updated temp: {config['temperature']}")

# update() from another dict
overrides = {"max_tokens": 2048, "stream": False, "user": "alice"}
config.update(overrides)
print(f"After update: max_tokens={config['max_tokens']}, user={config['user']}")

# Delete
del config["user"]
removed = config.pop("top_p")    # pop returns and removes
print(f"Removed: top_p={removed}")

# popitem() — removes and returns LAST inserted key-value pair
last_key, last_val = config.popitem()
print(f"popitem: {last_key}={last_val}")

# --- 4. ITERATING OVER DICTIONARIES --------------------------

sample_metrics = {
    "accuracy":  0.9712,
    "precision": 0.9658,
    "recall":    0.9731,
    "f1":        0.9694,
}

print("\n--- Iterating ---")

# Keys only
for key in sample_metrics:            # or .keys()
    print(f"  Key: {key}")

# Values only
for val in sample_metrics.values():
    print(f"  Val: {val:.4f}")

# Key-value pairs (.items() — most common)
print("\nMetrics Report:")
for metric, value in sample_metrics.items():
    bar = "█" * int(value * 20)
    print(f"  {metric:<12}: {value:.4f}  {bar}")

# --- 5. DICT COMPREHENSION -----------------------------------
# One-liner dict construction — critical pattern in data pipelines

# Normalize all metric values to percentage
pct_metrics = {k: round(v * 100, 2) for k, v in sample_metrics.items()}
print(f"\nPercentages: {pct_metrics}")

# Filter: only metrics above 0.97
high_metrics = {k: v for k, v in sample_metrics.items() if v >= 0.97}
print(f"High (>=0.97): {high_metrics}")

# Build vocab-to-index mapping from a list
vocab = ["<PAD>", "<UNK>", "the", "cat", "sat", "on", "mat"]
word_to_idx = {word: idx for idx, word in enumerate(vocab)}
idx_to_word = {idx: word for word, idx in word_to_idx.items()}
print(f"\nword_to_idx: {word_to_idx}")

# --- 6. DEFAULTDICT — Never worry about missing keys ----------
from collections import defaultdict

# Without defaultdict:
word_counts = {}
for word in ["cat", "dog", "cat", "bird", "dog", "cat"]:
    word_counts[word] = word_counts.get(word, 0) + 1

# With defaultdict:
word_counts2 = defaultdict(int)   # default value: 0
for word in ["cat", "dog", "cat", "bird", "dog", "cat"]:
    word_counts2[word] += 1    # no KeyError on missing key

print(f"\nWord counts: {dict(word_counts2)}")

# defaultdict for lists
class_samples = defaultdict(list)
labels = [("img1.jpg", "cat"), ("img2.jpg", "dog"), ("img3.jpg", "cat")]
for filename, label in labels:
    class_samples[label].append(filename)

print(f"Class samples: {dict(class_samples)}")

# --- 7. COUNTER — Frequency counting -------------------------
from collections import Counter

tokens = "the cat sat on the mat the cat sat".split()
freq   = Counter(tokens)

print(f"\nTop 3 tokens: {freq.most_common(3)}")
print(f"Count of 'the': {freq['the']}")
print(f"Count of 'xyz': {freq['xyz']}")   # 0 — not KeyError!

# Merge counters
c1 = Counter({"a": 3, "b": 2})
c2 = Counter({"b": 5, "c": 1})
print(f"Merged: {c1 + c2}")

# --- 8. ORDERED OPERATIONS (Python 3.7+) ---------------------
# Dicts maintain insertion order — can use this!

training_log = {}
for epoch in range(1, 6):
    training_log[f"epoch_{epoch}"] = {
        "loss":     round(1.0 * (0.8 ** epoch), 4),
        "accuracy": round(1 - 0.5 * (0.7 ** epoch), 4),
    }

print("\nTraining log (insertion order preserved):")
for epoch, metrics in training_log.items():
    print(f"  {epoch}: loss={metrics['loss']}, acc={metrics['accuracy']}")

# --- 9. SETDEFAULT & DICT MERGING ----------------------------

# setdefault: set key only if it doesn't exist
cfg = {"model": "gpt-4"}
cfg.setdefault("temperature", 0.7)    # sets it
cfg.setdefault("temperature", 0.9)   # does NOT overwrite
print(f"\ntemperature: {cfg['temperature']}")  # still 0.7

# Merge dicts (Python 3.9+): |= update, | create new
base     = {"a": 1, "b": 2}
override = {"b": 99, "c": 3}

merged_new    = base | override       # new dict
base         |= override             # in-place update
print(f"Merged: {merged_new}")

# --- 10. PRACTICAL EXAMPLE: Config Manager -------------------

class ConfigManager:
    """Manages model configuration with defaults and overrides."""

    DEFAULTS = {
        "temperature": 0.7,
        "max_tokens":  512,
        "top_p":       1.0,
        "n":           1,
        "stream":      False,
    }

    def __init__(self, model_name: str):
        self._config = {
            "model": model_name,
            **self.DEFAULTS
        }

    def update(self, **kwargs) -> None:
        """Update config, validating temperature range."""
        if "temperature" in kwargs:
            if not 0.0 <= kwargs["temperature"] <= 2.0:
                raise ValueError(f"Temperature must be in [0, 2], got {kwargs['temperature']}")
        self._config.update(kwargs)

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    def to_dict(self) -> dict:
        return self._config.copy()

    def __repr__(self) -> str:
        return f"ConfigManager({self._config})"


cfg = ConfigManager("gpt-4")
cfg.update(temperature=0.2, max_tokens=2048)
print(f"\nConfig: {cfg.to_dict()}")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 10 Complete ---")
print("Dictionaries: the 'database' of Python. Master them.")
