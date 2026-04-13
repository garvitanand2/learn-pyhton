# Day 20: Iterators & Generators
# Focus: Lazy evaluation — efficient data streaming for large datasets

# ============================================================
# WHAT: An iterator is an object that yields values one at a
#       time. A generator is a function that produces an
#       iterator using `yield`.
# WHY:  AI datasets can be billions of samples — you CANNOT
#       load them all into RAM. Generators let you stream
#       data lazily, computing each value only when needed.
#       Every PyTorch DataLoader is built on this principle.
# ============================================================

import sys
import time

# ============================================================
# 1. The Iterator Protocol
# ============================================================
print("=== 1. Iterator Protocol ===")

# A `for` loop secretly calls:
# 1. iter(obj)  → calls obj.__iter__() → returns iterator
# 2. next(it)   → calls it.__next__() → returns next value
# 3. Repeats until StopIteration is raised

# Manually iterate:
my_list = [1, 2, 3]
it = iter(my_list)
print(next(it))   # 1
print(next(it))   # 2
print(next(it))   # 3
try:
    print(next(it))   # StopIteration!
except StopIteration:
    print("Iterator exhausted!")

# ============================================================
# 2. A Custom Iterator Class
# ============================================================
print("\n=== 2. Custom Iterator ===")

class BatchIterator:
    """Yields fixed-size batches from a dataset.
    
    This is exactly what PyTorch's DataLoader does internally.
    """

    def __init__(self, data: list, batch_size: int):
        self.data = data
        self.batch_size = batch_size
        self._index = 0

    def __iter__(self):
        """Returns the iterator object (self in this case)."""
        self._index = 0  # reset to allow re-iteration
        return self

    def __next__(self):
        """Returns the next batch."""
        if self._index >= len(self.data):
            raise StopIteration
        batch = self.data[self._index : self._index + self.batch_size]
        self._index += self.batch_size
        return batch


dataset = list(range(25))
loader = BatchIterator(dataset, batch_size=8)

for batch_num, batch in enumerate(loader, 1):
    print(f"  Batch {batch_num}: {batch}")

# ============================================================
# 3. Generators — The Pythonic Way
# ============================================================
print("\n=== 3. Generator Functions ===")

# A function with `yield` becomes a generator function.
# Calling it returns a generator object (lazy iterator).

def batch_generator(data: list, batch_size: int):
    """Generator version of BatchIterator — much simpler!"""
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]
        # Execution PAUSES here until next() is called again


# Exact same behavior, 10x less code:
for batch_num, batch in enumerate(batch_generator(dataset, 8), 1):
    print(f"  Batch {batch_num}: {batch}")

# ============================================================
# 4. Generator Expressions
# ============================================================
print("\n=== 4. Generator Expressions ===")

# List comprehension — all values computed NOW (in memory)
squares_list = [x**2 for x in range(1_000_000)]
print(f"List memory: {sys.getsizeof(squares_list):,} bytes")

# Generator expression — values computed ON DEMAND
squares_gen = (x**2 for x in range(1_000_000))
print(f"Gen  memory: {sys.getsizeof(squares_gen):,} bytes")

# Generators are consumed once:
gen = (x * 2 for x in range(5))
print(f"List from gen: {list(gen)}")
print(f"Second pass:   {list(gen)}")   # empty!

# ============================================================
# 5. yield from — Delegating to Sub-generators
# ============================================================
print("\n=== 5. yield from ===")

def read_texts(file_path: str):
    """Simulates reading text from a file lazily."""
    # In real code: open(file_path) and yield each stripped line
    sentences = [
        "the cat sat on the mat",
        "deep learning is powerful",
        "generators save memory",
    ]
    yield from sentences   # equivalent to: for s in sentences: yield s

def multi_file_reader(paths: list[str]):
    """Reads multiple sources into one stream."""
    for path in paths:
        yield from read_texts(path)

all_texts = list(multi_file_reader(["train.txt", "val.txt"]))
print(f"  Total texts: {len(all_texts)}")
for t in all_texts[:4]:
    print(f"  → {t}")

# ============================================================
# 6. Infinite Generators
# ============================================================
print("\n=== 6. Infinite Generators ===")

def learning_rate_schedule(initial_lr: float, decay: float = 0.95):
    """Generates learning rates with exponential decay — never ends!"""
    lr = initial_lr
    step = 0
    while True:
        yield step, lr
        lr *= decay
        step += 1

# Only take as many as you need
lr_gen = learning_rate_schedule(0.01, decay=0.9)
for _ in range(6):
    step, lr = next(lr_gen)
    print(f"  Step {step:2d}: lr = {lr:.6f}")

# ============================================================
# 7. Generator Pipeline — Stream Processing
# ============================================================
print("\n=== 7. Stream Processing Pipeline ===")

def load_records(n: int):
    """Source: generates n fake records."""
    for i in range(n):
        yield {"id": i, "text": f"sample text {i}", "raw_score": i * 0.1}

def filter_low_scores(records, threshold: float = 0.3):
    """Filter stage: removes low-scoring records."""
    for record in records:
        if record["raw_score"] >= threshold:
            yield record

def normalize_scores(records, max_score: float = 1.0):
    """Transform stage: normalizes scores to [0, 1]."""
    for record in records:
        record["score"] = round(record["raw_score"] / max_score, 3)
        yield record

def add_label(records):
    """Enrich stage: assigns label based on score."""
    for record in records:
        record["label"] = "positive" if record["score"] > 0.6 else "negative"
        yield record

# Connect pipeline — no data flows until we consume it!
pipeline = add_label(
    normalize_scores(
        filter_low_scores(
            load_records(20),
            threshold=0.3,
        )
    )
)

print("  Processed records:")
for record in pipeline:
    print(f"  id={record['id']:2d} | score={record['score']:.3f} | {record['label']}")

# ============================================================
# 8. Memory Comparison
# ============================================================
print("\n=== 8. Memory Comparison ===")

def eager_approach(n: int) -> list:
    """Load everything into memory."""
    return [{"id": i, "value": i * 2} for i in range(n)]

def lazy_approach(n: int):
    """Stream one at a time."""
    for i in range(n):
        yield {"id": i, "value": i * 2}

N = 100_000
eager = eager_approach(N)
lazy = lazy_approach(N)

print(f"  Eager (list):     {sys.getsizeof(eager):>12,} bytes")
print(f"  Lazy (generator): {sys.getsizeof(lazy):>12,} bytes")
print(f"  Memory ratio: {sys.getsizeof(eager) / sys.getsizeof(lazy):.0f}x smaller with generators")

print("\nDay 20 complete! Generators are essential for efficient data pipelines.")
