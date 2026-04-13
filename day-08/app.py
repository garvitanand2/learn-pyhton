# =============================================================
# Day 8: Lists — The Most Important Data Structure in Python
# Goal: Master list operations. In AI/ML, you constantly store
#       data in lists — samples, tokens, predictions, embeddings.
# =============================================================

# --- 1. CREATING LISTS ----------------------------------------
# What: Ordered, mutable, allows duplicates, any type
# Why:  Store sequences — tokens, labels, embeddings dimensions

tokens      = ["the", "model", "predicted", "correctly"]
labels      = [0, 1, 2, 1, 0, 2]           # class labels
loss_values = [0.92, 0.78, 0.65, 0.53, 0.41]  # training losses
mixed       = [1, "text", 3.14, True, None]    # any types (avoid this in practice)
empty       = []
nested      = [[1, 2], [3, 4], [5, 6]]     # matrix-like

print(f"Tokens     : {tokens}")
print(f"Labels     : {labels}")
print(f"Loss values: {loss_values}")

# --- 2. INDEXING AND SLICING ----------------------------------
# Positive index: 0 = first, 1 = second ...
# Negative index: -1 = last, -2 = second last ...

print(f"\nFirst token : {tokens[0]}")   # "the"
print(f"Last token  : {tokens[-1]}")   # "correctly"
print(f"Last loss   : {loss_values[-1]}")

# Slicing: list[start:stop:step]  (stop is EXCLUSIVE)
print(f"\nFirst 3 losses: {loss_values[:3]}")       # [0.92, 0.78, 0.65]
print(f"Last 2 losses : {loss_values[-2:]}")       # [0.53, 0.41]
print(f"Every 2nd     : {loss_values[::2]}")       # [0.92, 0.65, 0.41]
print(f"Reversed      : {loss_values[::-1]}")      # reverse!

# Slicing creates a COPY — original is unchanged
batch = labels[2:5]
batch[0] = 99        # modifying batch
print(f"\nOriginal labels unchanged: {labels}")
print(f"Modified batch            : {batch}")

# --- 3. MODIFYING LISTS ---------------------------------------

# append — add one item to the end (O(1))
loss_values.append(0.32)
print(f"\nAfter append: {loss_values}")

# extend — add all items from another iterable (O(k))
new_losses = [0.28, 0.21]
loss_values.extend(new_losses)
print(f"After extend: {loss_values}")

# insert — at a specific index (O(n) — shifts elements)
tokens.insert(1, "[MASK]")     # insert at index 1
print(f"\nAfter insert: {tokens}")

# remove — removes first occurrence of VALUE (O(n))
tokens.remove("[MASK]")
print(f"After remove: {tokens}")

# pop — removes and returns item at index (O(1) for -1, O(n) otherwise)
last_loss = loss_values.pop()    # removes last item
print(f"Popped: {last_loss} | Remaining: {loss_values}")

# del — remove by index or slice
del loss_values[0]               # removes 0.78
print(f"After del: {loss_values}")

# --- 4. SEARCHING AND SORTING ---------------------------------

scores = [0.85, 0.92, 0.71, 0.88, 0.95, 0.67, 0.88]

print(f"\nScores       : {scores}")
print(f"Max score    : {max(scores)}")
print(f"Min score    : {min(scores)}")
print(f"Sum          : {round(sum(scores), 4)}")
print(f"Count of 0.88: {scores.count(0.88)}")
print(f"Index of max : {scores.index(max(scores))}")

# Sort IN PLACE (modifies original)
scores.sort()
print(f"Sorted asc   : {scores}")

scores.sort(reverse=True)
print(f"Sorted desc  : {scores}")

# sorted() — returns NEW list, original unchanged
labels_copy  = sorted(labels)
print(f"\nOriginal labels : {labels}")
print(f"Sorted copy     : {labels_copy}")

# Sort by custom key — sort models by accuracy
models_with_scores = [
    {"name": "v1", "accuracy": 0.82},
    {"name": "v3", "accuracy": 0.95},
    {"name": "v2", "accuracy": 0.78},
]
models_with_scores.sort(key=lambda m: m["accuracy"], reverse=True)
print(f"\nModels by accuracy: {[m['name'] for m in models_with_scores]}")

# --- 5. COPYING LISTS -----------------------------------------
# CRITICAL: Assignment does NOT copy — it creates a second reference!

original = [1, 2, 3]
alias    = original          # NOT a copy — same object!
alias[0] = 99
print(f"\noriginal after modifying alias: {original}")   # [99, 2, 3] — changed!

# Shallow copy methods (all equivalent)
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

copy1[0] = 0
print(f"original after modifying copy1: {original}")   # unchanged

# Deep copy for nested structures (import copy)
import copy
nested_original = [[1, 2], [3, 4]]
shallow = nested_original.copy()
deep    = copy.deepcopy(nested_original)

shallow[0][0] = 99     # modifies nested_original too!
deep[0][0]    = 42     # does NOT modify nested_original

print(f"\nNested original after shallow copy mod: {nested_original}")  # [[99,2],[3,4]]
print(f"Deep copy modification didn't affect original: {nested_original}")  # unchanged

# --- 6. USEFUL BUILT-INS FOR LISTS ----------------------------

numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

print(f"\nlen     : {len(numbers)}")
print(f"sorted  : {sorted(numbers)}")
print(f"sum     : {sum(numbers)}")
print(f"min/max : {min(numbers)} / {max(numbers)}")
print(f"any > 8 : {any(n > 8 for n in numbers)}")   # True
print(f"all > 0 : {all(n > 0 for n in numbers)}")   # True

# zip — combine lists (Day 4 revisit, but important)
texts  = ["this is positive", "this is negative", "neutral text"]
preds  = ["positive", "negative", "positive"]
correct = [t.split()[3].split()[0] in p for t, p in zip(texts, preds)]
print(f"\nCorrect predictions: {correct}")

# enumerate — index + value
print("\nDataset samples:")
for i, (text, pred) in enumerate(zip(texts, preds), 1):
    print(f"  {i}. [{pred.upper()}] '{text}'")

# --- 7. PRACTICAL EXAMPLE: Sliding Window for Text -----------

def sliding_window(tokens: list, window_size: int, stride: int = 1) -> list:
    """
    Create overlapping windows from a token list.
    Used in NLP for chunk-based inference on long documents.
    """
    windows = []
    for start in range(0, len(tokens) - window_size + 1, stride):
        window = tokens[start : start + window_size]
        windows.append(window)
    return windows

sentence_tokens = ["The", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"]
windows = sliding_window(sentence_tokens, window_size=4, stride=2)
print("\nSliding windows (size=4, stride=2):")
for i, w in enumerate(windows):
    print(f"  Window {i}: {w}")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 8 Complete ---")
print("Lists: ordered, mutable, indexed sequences — the backbone of data pipelines.")
