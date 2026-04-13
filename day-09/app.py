# =============================================================
# Day 9: Tuples & Sets
# Goal: Know when to use immutable (tuples) vs unique-collection
#       (sets) structures. Critical for memory efficiency and
#       correctness in AI data pipelines.
# =============================================================

# ============================================================
# PART 1: TUPLES
# ============================================================

# --- 1. CREATING TUPLES --------------------------------------
# What: Ordered, IMMUTABLE, allows duplicates, any type
# Why:  Use when data should not change after creation.
#       Perfect for coordinates, config pairs, function return values

point       = (1.5, 2.3)               # 2D coordinate
rgb         = (255, 128, 0)            # color value
model_info  = ("gpt-4", "openai", 128000)   # (name, provider, max_tokens)
empty_tuple = ()
singleton   = (42,)                    # NOTE: trailing comma required!

print(f"Model: name={model_info[0]}, provider={model_info[1]}")
print(f"Is singleton tuple: {type(singleton)}")   # <class 'tuple'>
print(f"NOT a tuple: {type((42))}")               # <class 'int'>! No comma → int

# --- 2. TUPLE OPERATIONS -------------------------------------

coordinates = (10.5, 20.3, -5.1, 15.8, 10.5)

print(f"\nLength  : {len(coordinates)}")
print(f"Max     : {max(coordinates)}")
print(f"Count of 10.5: {coordinates.count(10.5)}")
print(f"Index of 20.3: {coordinates.index(20.3)}")

# Concatenation (creates NEW tuple)
t1 = (1, 2)
t2 = (3, 4)
t3 = t1 + t2
print(f"\nt1 + t2 = {t3}")

# Repetition
repeated = (0,) * 5
print(f"(0,) * 5 = {repeated}")   # (0, 0, 0, 0, 0)

# --- 3. TUPLE UNPACKING (VERY IMPORTANT) ---------------------
# What: Assign tuple elements to multiple variables at once

x, y        = (3.0, 4.0)
name, score = ("BERT", 0.92)
print(f"\n{name} scored {score}")

# Swap without temp variable — tuple under the hood
a, b = 10, 20
a, b = b, a
print(f"Swapped: a={a}, b={b}")

# Extended unpacking
first, *middle, last = (1, 2, 3, 4, 5)
print(f"first={first}, middle={middle}, last={last}")

# Unpack in a loop
model_perf = [("gpt-4", 0.95), ("bert", 0.88), ("t5", 0.83)]
for model_name, accuracy in model_perf:
    print(f"  {model_name}: {accuracy:.0%}")

# --- 4. TUPLES AS DICTIONARY KEYS ----------------------------
# Lists cannot be dict keys (unhashable) — tuples CAN (if contents are hashable)

# Cache inference results by (model_name, input_hash) pair
inference_cache = {
    ("gpt-4", "hash_abc123"):   "The result is...",
    ("gpt-4", "hash_def456"):   "Another result...",
    ("bert",  "hash_abc123"):   "BERT's answer...",
}

key = ("gpt-4", "hash_abc123")
print(f"\nCached result: {inference_cache[key]}")

# --- 5. NAMED TUPLES (preview) --------------------------------
from collections import namedtuple

ModelResult = namedtuple("ModelResult", ["model", "accuracy", "latency_ms"])

r1 = ModelResult(model="gpt-4", accuracy=0.95, latency_ms=1200)
r2 = ModelResult("bert", 0.88, 45)

print(f"\n{r1.model}: {r1.accuracy:.0%} accuracy, {r1.latency_ms}ms")
print(f"As tuple: {tuple(r1)}")

# ============================================================
# PART 2: SETS
# ============================================================

# --- 6. CREATING SETS ----------------------------------------
# What: Unordered, mutable, NO duplicates, hashable elements only
# Why:  Instant membership checks, deduplication, set algebra

vocab    = {"the", "a", "cat", "dog", "model", "the"}  # duplicate "the" removed
labels   = {0, 1, 2, 1, 0}                              # {0, 1, 2}
empty_s  = set()   # NOTE: {} creates a dict, not a set!

print(f"\nvocab  : {vocab}")    # order not guaranteed
print(f"labels : {labels}")

# --- 7. SET OPERATIONS (CRITICAL) ----------------------------
# These are O(1) per element — dramatically faster than list for lookups

train_words = {"cat", "dog", "bird", "the", "a", "model"}
test_words  = {"cat", "fish", "bird", "the", "transformer"}

# Union: all unique words from both
union = train_words | test_words
print(f"\nUnion      : {sorted(union)}")

# Intersection: words in BOTH
common = train_words & test_words
print(f"Intersection: {sorted(common)}")

# Difference: in train but NOT in test
only_train = train_words - test_words
print(f"Only train : {sorted(only_train)}")

# Symmetric difference: in one but NOT both  (OOV words from both sides)
oov = train_words ^ test_words
print(f"Symmetric diff: {sorted(oov)}")

# --- 8. SET METHODS -------------------------------------------
stop_words = {"the", "a", "an", "is", "are", "was"}

stop_words.add("of")           # add one element
stop_words.update(["to", "in", "for"])  # add multiple
stop_words.discard("xyz")      # remove if exists — no error if missing
# stop_words.remove("xyz")     # would raise KeyError!

print(f"\nStop words count: {len(stop_words)}")

# Membership check — O(1) vs list O(n)
print(f"'the' in stop_words: {'the' in stop_words}")
print(f"'cat' in stop_words: {'cat' not in stop_words}")

# --- 9. SUBSET / SUPERSET CHECKS ----------------------------
required_skills = {"python", "ml", "statistics"}
alice_skills    = {"python", "ml", "statistics", "deep_learning"}
bob_skills      = {"python", "ml"}

print(f"\nAlice has required: {required_skills.issubset(alice_skills)}")  # True
print(f"Alice skills > required: {alice_skills.issuperset(required_skills)}")  # True
print(f"Bob has required: {required_skills.issubset(bob_skills)}")       # False
print(f"Alice & Bob disjoint: {alice_skills.isdisjoint(bob_skills)}")    # False

# --- 10. PRACTICAL EXAMPLE: OOV Detection --------------------

def find_oov_tokens(train_vocab: set, test_tokens: list) -> dict:
    """
    Find out-of-vocabulary (OOV) tokens in a test set.
    Tokens not seen during training → model may not handle them well.
    """
    oov_tokens = [t for t in test_tokens if t not in train_vocab]
    coverage   = (len(test_tokens) - len(oov_tokens)) / len(test_tokens)
    return {
        "oov_tokens":   list(set(oov_tokens)),
        "oov_count":    len(oov_tokens),
        "coverage":     round(coverage, 4),
    }

train_vocab    = {"the", "cat", "sat", "on", "mat", "a", "dog", "ran", "fast"}
test_sentence  = ["the", "quick", "brown", "fox", "sat", "on", "a", "mat"]

result = find_oov_tokens(train_vocab, test_sentence)
print(f"\nOOV Analysis:")
print(f"  OOV tokens : {result['oov_tokens']}")
print(f"  OOV count  : {result['oov_count']}")
print(f"  Coverage   : {result['coverage']:.1%}")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 9 Complete ---")
print("Tuples → immutable records. Sets → unique collections with O(1) lookup.")
