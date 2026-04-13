# =============================================================
# Day 12: List Comprehensions
# Goal: Write expressive, "AI engineer-style" one-liner data
#       transformations. Used everywhere in data processing.
# =============================================================

# --- 1. BASIC LIST COMPREHENSION ------------------------------
# Syntax: [expression for item in iterable]
# Equivalent to a for loop that builds a list, but more concise and faster

# Traditional loop
squared_loop = []
for x in range(10):
    squared_loop.append(x ** 2)

# List comprehension
squared_comp = [x ** 2 for x in range(10)]

print(f"Squared: {squared_comp}")
assert squared_loop == squared_comp    # identical output!

# --- 2. COMPREHENSION WITH CONDITION (filter) -----------------
# Syntax: [expression for item in iterable if condition]

scores = [0.92, 0.45, 0.78, 0.31, 0.88, 0.55, 0.97, 0.62]

high_scores    = [s for s in scores if s >= 0.80]
passing_scores = [round(s, 3) for s in scores if s >= 0.60]
failing_scores = [s for s in scores if s < 0.60]

print(f"\nHigh scores  : {high_scores}")
print(f"Passing      : {passing_scores}")
print(f"Failing      : {failing_scores}")

# --- 3. TRANSFORMING COMPLEX DATA ----------------------------

tokens = ["  Hello ", "WORLD", "  ai ", "Machine", "LEARNING  "]
cleaned = [t.strip().lower() for t in tokens]
print(f"\nCleaned tokens: {cleaned}")

# Extract specific fields from list of dicts
models = [
    {"name": "gpt-4",   "accuracy": 0.95, "cost": 0.03},
    {"name": "bert",    "accuracy": 0.88, "cost": 0.001},
    {"name": "llama-3", "accuracy": 0.91, "cost": 0.0009},
    {"name": "t5",      "accuracy": 0.84, "cost": 0.0005},
]

# Extract names
names = [m["name"] for m in models]
print(f"\nModel names: {names}")

# Extract names of affordable models (cost < 0.01)
affordable = [m["name"] for m in models if m["cost"] < 0.01]
print(f"Affordable: {affordable}")

# Get (name, accuracy) tuples for high-accuracy models
top_models = [(m["name"], m["accuracy"]) for m in models if m["accuracy"] >= 0.90]
print(f"Top models: {top_models}")

# --- 4. NESTED LIST COMPREHENSIONS ---------------------------
# Equivalent to nested for loops — use carefully (readability can drop)

# Flatten a matrix (list of lists) → one flat list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat   = [x for row in matrix for x in row]   # inner loop iterates outer's item
print(f"\nFlattened matrix: {flat}")

# Transpose: rows become columns
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"Transposed:")
for row in transposed:
    print(f"  {row}")

# Cartesian product (all combinations of two lists)
learning_rates = [0.01, 0.001]
batch_sizes    = [32, 64, 128]
combos = [(lr, bs) for lr in learning_rates for bs in batch_sizes]
print(f"\nHyperparameter combos: {combos}")

# --- 5. DICT COMPREHENSIONS ----------------------------------
# Syntax: {key_expr: val_expr for item in iterable}

# Normalize scores to percentages
pct = {name: round(acc * 100, 1) for name, acc in zip(names, [m["accuracy"] for m in models])}
print(f"\nModel accuracy %: {pct}")

# Invert a dict (swap keys and values)
word_to_idx = {"<PAD>": 0, "<UNK>": 1, "cat": 2, "dog": 3}
idx_to_word = {idx: word for word, idx in word_to_idx.items()}
print(f"Inverted: {idx_to_word}")

# Build frequency dict
vocab_list = ["cat", "dog", "cat", "bird", "dog", "cat"]
freq = {word: vocab_list.count(word) for word in set(vocab_list)}
print(f"Frequency: {freq}")

# --- 6. SET COMPREHENSIONS ------------------------------------
# Syntax: {expression for item in iterable}

corpus = ["the cat sat on the mat", "the dog ran fast", "the cat ate a mat"]
all_tokens  = {word for sentence in corpus for word in sentence.split()}
print(f"\nUnique tokens: {sorted(all_tokens)}")

# Stop words removal
stop_words  = {"the", "a", "an", "on"}
content_words = {w for w in all_tokens if w not in stop_words}
print(f"Content words: {sorted(content_words)}")

# --- 7. GENERATOR EXPRESSIONS --------------------------------
# Like list comprehensions but LAZY — don't compute all at once
# Use when you don't need to store all results, just iterate

import sys

# Compare memory usage
scores_list = [s ** 2 for s in range(1_000_000)]    # creates full list in memory
scores_gen  = (s ** 2 for s in range(1_000_000))    # lazy, computes one at a time

print(f"\nList memory: {sys.getsizeof(scores_list):,} bytes")
print(f"Gen memory : {sys.getsizeof(scores_gen):,} bytes")   # ~120 bytes!

# sum() works directly on generators — no need to materialize a list
total  = sum(s ** 2 for s in range(1_000_000))       # O(1) memory
print(f"Sum of squares (0-999999): {total:,}")

# --- 8. WALRUS OPERATOR (:=) IN COMPREHENSIONS (Python 3.8+) --
# Assign and use a value in the same expression

texts = ["Hello world", "AI is great!", "Short", "This is a moderately long sentence"]

# Filter + capture length without computing twice
long_texts = [
    (text, n)
    for text in texts
    if (n := len(text)) > 10   # := assigns len() result to n, reuses it
]
print(f"\nLong texts (>10 chars): {long_texts}")

# --- 9. CONDITIONAL EXPRESSION IN COMPREHENSION ---------------
# Syntax: [x if condition else y for x in iterable]
# The ternary is in the EXPRESSION position, not the filter

labels = [0, 1, 2, 0, 1, 2, 1]
label_names = ["negative" if l == 0 else "positive" if l == 1 else "neutral"
               for l in labels]
print(f"\nLabel names: {label_names}")

# Clip values to [0, 1] range
raw_probs = [-0.1, 0.5, 1.2, 0.8, -0.3, 1.0]
clipped   = [max(0.0, min(1.0, p)) for p in raw_probs]
print(f"Clipped: {clipped}")

# --- 10. PRACTICAL EXAMPLE: Batch Processing -----------------

def batch_normalize(batches: list, eps: float = 1e-8) -> list:
    """
    Normalize each batch of values to mean=0, std=1 (z-score).
    Using list comprehensions throughout.
    """
    normalized = []
    for batch in batches:
        mean = sum(batch) / len(batch)
        std  = (sum((x - mean) ** 2 for x in batch) / len(batch)) ** 0.5
        norm = [(x - mean) / (std + eps) for x in batch]   # comprehension!
        normalized.append(norm)
    return normalized

batches = [
    [1.0, 2.0, 3.0, 4.0, 5.0],
    [10.0, 20.0, 30.0],
    [100.0, 200.0, 150.0, 175.0],
]

result = batch_normalize(batches)
print("\nBatch normalized:")
for b, n in zip(batches, result):
    rounded = [round(x, 3) for x in n]
    print(f"  {b} → {rounded}")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 12 Complete ---")
print("Comprehensions: one-liner data transformations — the mark of Pythonic code.")
