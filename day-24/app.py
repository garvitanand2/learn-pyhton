# Day 24: Lambda, Map, Filter, Reduce & Functional Toolbox
# Focus: Concise, expressive transformations for data pipelines

# ============================================================
# WHAT: Functional Python tools let you write compact data
#       transformation code using first-class functions.
# WHY:  Data preprocessing, feature engineering, and pipeline
#       steps often reduce to: filter bad data, map a transform,
#       reduce to a summary. Knowing these well means cleaner,
#       faster-to-write data code.
# ============================================================

from functools import reduce, partial
import operator

# ============================================================
# 1. Lambda Functions — Anonymous One-Liners
# ============================================================
print("=== 1. Lambda ===")

# syntax: lambda args: expression
double = lambda x: x * 2
add = lambda x, y: x + y
clamp = lambda x, lo, hi: max(lo, min(hi, x))

print(f"double(5)     = {double(5)}")
print(f"add(3, 4)     = {add(3, 4)}")
print(f"clamp(1.5, 0, 1) = {clamp(1.5, 0.0, 1.0)}")

# Best used for short, inline operations (sorting, key functions):
records = [
    {"model": "bert", "accuracy": 0.918},
    {"model": "gpt2", "accuracy": 0.883},
    {"model": "t5",   "accuracy": 0.941},
    {"model": "xlm",  "accuracy": 0.897},
]

sorted_by_acc = sorted(records, key=lambda r: r["accuracy"], reverse=True)
print("\nSorted by accuracy:")
for r in sorted_by_acc:
    print(f"  {r['model']:<8} {r['accuracy']:.3f}")

# ============================================================
# 2. map() — Transform Every Element
# ============================================================
print("\n=== 2. map() ===")

texts = ["Hello World", "  DEEP LEARNING  ", "Natural Language Processing"]

# map() returns a lazy iterator, not a list — use list() to materialize
cleaned = list(map(str.lower, texts))
print(f"Lowercase: {cleaned}")

stripped = list(map(str.strip, texts))
print(f"Stripped:  {stripped}")

# Multi-step with composed functions (or lambda)
def normalize(text: str) -> str:
    import re
    return re.sub(r"\s+", " ", text.strip().lower())

normalized = list(map(normalize, texts))
print(f"Normalized: {normalized}")

# map with lambda
word_counts = list(map(lambda t: len(t.split()), normalized))
print(f"Word counts: {word_counts}")

# map over two iterables with zip alternative
scores_a = [0.9, 0.8, 0.7]
scores_b = [0.85, 0.88, 0.75]
ensemble = list(map(lambda a, b: (a + b) / 2, scores_a, scores_b))
print(f"Ensemble avg: {ensemble}")

# ============================================================
# 3. filter() — Keep Matching Elements
# ============================================================
print("\n=== 3. filter() ===")

predictions = [
    {"text": "great model",   "confidence": 0.92, "label": "positive"},
    {"text": "bad training",  "confidence": 0.41, "label": "negative"},
    {"text": "average run",   "confidence": 0.55, "label": "neutral"},
    {"text": "best result",   "confidence": 0.88, "label": "positive"},
    {"text": "poor accuracy", "confidence": 0.37, "label": "negative"},
    {"text": "okay base",     "confidence": 0.62, "label": "neutral"},
]

# filter() also returns a lazy iterator
high_conf = list(filter(lambda p: p["confidence"] >= 0.6, predictions))
print(f"High confidence ({len(high_conf)} samples):")
for p in high_conf:
    print(f"  [{p['label']:<10}] {p['confidence']:.2f} — {p['text']}")

positives = list(filter(lambda p: p["label"] == "positive", predictions))
print(f"\nPositive samples: {len(positives)}")

# Filter + Map pipeline (process only valid records)
valid_texts = list(map(
    lambda p: p["text"],
    filter(lambda p: p["confidence"] >= 0.5, predictions)
))
print(f"High-conf texts: {valid_texts}")

# ============================================================
# 4. reduce() — Fold a Sequence to a Single Value
# ============================================================
print("\n=== 4. reduce() ===")

# reduce(fn, iterable) calls fn(accumulator, next_item) repeatedly
losses = [0.842, 0.621, 0.489, 0.391, 0.312]

# Sum manually with reduce:
total = reduce(lambda acc, x: acc + x, losses)
print(f"Sum of losses: {total:.4f}")

# Product
terms = [2, 3, 4, 5]
product = reduce(operator.mul, terms)
print(f"Product: {product}")

# Finding the best epoch
best = reduce(lambda best, x: x if x["loss"] < best["loss"] else best, [
    {"epoch": i + 1, "loss": loss} for i, loss in enumerate(losses)
])
print(f"Best epoch: {best}")

# Building vocab from records with reduce
records2 = [
    {"tokens": ["the", "cat", "sat"]},
    {"tokens": ["the", "dog", "ran"]},
    {"tokens": ["cat", "and", "dog"]},
]
vocab = reduce(lambda acc, r: acc | set(r["tokens"]), records2, set())
print(f"Vocab: {sorted(vocab)}")

# ============================================================
# 5. functools.partial — Fix Arguments
# ============================================================
print("\n=== 5. partial() ===")

def preprocess(text: str, lowercase: bool = True,
               max_len: int = 512, language: str = "en") -> str:
    import re
    if lowercase:
        text = text.lower()
    tokens = re.sub(r"[^\w\s]", "", text).split()[:max_len]
    return " ".join(tokens)

# Create specialized versions by fixing arguments:
simple_preprocess = partial(preprocess, lowercase=True, max_len=128)
en_preprocess      = partial(preprocess, language="en", lowercase=True)

samples = ["Hello, World!", "Deep Learning is AMAZING."]
for s in samples:
    print(f"  simple: {simple_preprocess(s)}")

# partial is great with map():
documents = ["Text One.", "Text Two.", "TEXT THREE."]
processed = list(map(partial(preprocess, max_len=50), documents))
print(f"  Processed: {processed}")

# ============================================================
# 6. Composing Functions
# ============================================================
print("\n=== 6. Function Composition ===")

def compose(*fns):
    """Compose functions right-to-left: compose(f, g)(x) = f(g(x))"""
    def composed(x):
        return reduce(lambda v, fn: fn(v), reversed(fns), x)
    return composed

def strip_text(t): return t.strip()
def lower_text(t): return t.lower()
def remove_punct(t):
    import re
    return re.sub(r"[^\w\s]", "", t)

clean_pipeline = compose(remove_punct, lower_text, strip_text)

for text in ["  Hello, WORLD!  ", "\tDeep Learning!!  "]:
    print(f"  '{text}' → '{clean_pipeline(text)}'")

# ============================================================
# 7. List Comprehension vs map/filter
# ============================================================
print("\n=== 7. Comprehension vs Functional ===")

data = list(range(1, 21))

# These are equivalent:
squares_a = [x**2 for x in data if x % 2 == 0]
squares_b = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, data)))

print(f"Comprehension: {squares_a[:5]}...")
print(f"Functional:    {squares_b[:5]}...")
print(f"Equal: {squares_a == squares_b}")

# Comprehension is generally preferred for readability.
# map/filter shine with named functions (not lambdas):
def is_even(n): return n % 2 == 0
def square(n):  return n ** 2

squares_c = list(map(square, filter(is_even, data)))  # cleanest with named fns

print("\nDay 24 complete! Functional tools make data transformations concise and composable.")
