# Day 27: Performance Basics — Profiling & Optimization
# Focus: Measure first, optimize second

# ============================================================
# WHAT: Performance optimization means finding bottlenecks
#       in your code and fixing them. Python has built-in
#       tools for timing and profiling.
# WHY:  "Premature optimization is the root of all evil."
#       You cannot optimize what you don't measure. AI pipelines
#       process millions of records — a 10x speedup matters.
# ============================================================

import time
import timeit
import sys
from functools import lru_cache

# ============================================================
# 1. time.perf_counter() — Measuring Wall Time
# ============================================================
print("=== 1. Basic Timing ===")

# perf_counter() is the highest-resolution clock available
def time_it(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

def sum_squares_loop(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total

def sum_squares_builtin(n: int) -> int:
    return sum(i * i for i in range(n))

def sum_squares_math(n: int) -> int:
    # Mathematical formula: n(n-1)(2n-1)/6
    return n * (n - 1) * (2 * n - 1) // 6

N = 1_000_000

_, t_loop    = time_it(sum_squares_loop, N)
_, t_builtin = time_it(sum_squares_builtin, N)
_, t_math    = time_it(sum_squares_math, N)

print(f"  Loop:    {t_loop*1000:.2f}ms")
print(f"  builtin: {t_builtin*1000:.2f}ms")
print(f"  formula: {t_math*1000:.4f}ms")

# ============================================================
# 2. timeit — Accurate Micro-benchmarks
# ============================================================
print("\n=== 2. timeit Module ===")

# timeit runs code many times and returns total time
# This accounts for startup noise and gives stable estimates

# String-based timeit
setup = "data = list(range(10000))"
stmt_loop  = "total = 0\nfor x in data: total += x"
stmt_sum   = "total = sum(data)"

t_loop_avg  = timeit.timeit(stmt_loop, setup=setup, number=1000) / 1000
t_sum_avg   = timeit.timeit(stmt_sum,  setup=setup, number=1000) / 1000

print(f"  for loop:  {t_loop_avg*1000:.3f}ms avg")
print(f"  sum():     {t_sum_avg*1000:.3f}ms avg")
print(f"  sum() is {t_loop_avg/t_sum_avg:.1f}x faster than loop")

# ============================================================
# 3. Memory Measurement
# ============================================================
print("\n=== 3. Memory Usage ===")

# Compare memory: list vs generator vs set
data = list(range(100_000))
data_gen   = (x for x in range(100_000))
data_set   = set(range(100_000))
data_tuple = tuple(range(100_000))

print(f"  list:       {sys.getsizeof(data):>12,} bytes")
print(f"  generator:  {sys.getsizeof(data_gen):>12,} bytes")
print(f"  set:        {sys.getsizeof(data_set):>12,} bytes")
print(f"  tuple:      {sys.getsizeof(data_tuple):>12,} bytes")

# String building — common gotcha
print("\n  String concatenation (SLOW for large N):")
N = 10_000

start = time.perf_counter()
s = ""
for i in range(N):
    s = s + str(i)         # creates new string object every iteration!
slow_time = time.perf_counter() - start

start = time.perf_counter()
s = "".join(str(i) for i in range(N))  # builds all once
fast_time = time.perf_counter() - start

print(f"  str concat:  {slow_time*1000:.3f}ms")
print(f"  str.join():  {fast_time*1000:.3f}ms")
print(f"  join() is {slow_time/fast_time:.1f}x faster")

# ============================================================
# 4. Algorithmic Complexity
# ============================================================
print("\n=== 4. Algorithmic Complexity ===")

# O(n²) vs O(n) vs O(1)
import random, time

def has_duplicate_on2(items: list) -> bool:
    """O(n²) — nested loop"""
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

def has_duplicate_on(items: list) -> bool:
    """O(n) — set membership"""
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False

def has_duplicate_o1_builtin(items: list) -> bool:
    """O(n) — built-in set comparison"""
    return len(items) != len(set(items))

random.seed(42)
test_sizes = [100, 500, 2000]

for size in test_sizes:
    data = random.sample(range(size * 2), size)  # no duplicates guaranteed

    _, t_n2   = time_it(has_duplicate_on2, data)
    _, t_n    = time_it(has_duplicate_on, data)
    _, t_set  = time_it(has_duplicate_o1_builtin, data)

    print(f"  n={size:4d}: O(n²)={t_n2*1000:.3f}ms  O(n)={t_n*1000:.3f}ms  set={t_set*1000:.3f}ms")

# ============================================================
# 5. Caching with lru_cache
# ============================================================
print("\n=== 5. Caching ===")

def fib_slow(n: int) -> int:
    """Without cache — exponential O(2^n)"""
    if n <= 1: return n
    return fib_slow(n-1) + fib_slow(n-2)

@lru_cache(maxsize=None)
def fib_fast(n: int) -> int:
    """With cache — linear O(n)"""
    if n <= 1: return n
    return fib_fast(n-1) + fib_fast(n-2)

n = 35
_, t_slow = time_it(fib_slow, n)
_, t_fast = time_it(fib_fast, n)

print(f"  fib({n}) slow:   {t_slow*1000:.2f}ms")
print(f"  fib({n}) cached: {t_fast*1000:.4f}ms")
print(f"  Speedup: {t_slow/t_fast:.0f}x")
print(f"  Cache info: {fib_fast.cache_info()}")

# ============================================================
# 6. Common Python Performance Tips
# ============================================================
print("\n=== 6. Performance Best Practices ===")

# Tip 1: Use local variable lookup over global
def slow_local():
    result = []
    for i in range(10_000):
        result.append(i * i)   # 'append' looked up on result each time
    return result

def fast_local():
    result = []
    _append = result.append    # cache method as local variable
    for i in range(10_000):
        _append(i * i)
    return result

# Tip 2: Use comprehensions over manual append
def comp_approach():
    return [i * i for i in range(10_000)]

_, t1 = time_it(slow_local)
_, t2 = time_it(fast_local)
_, t3 = time_it(comp_approach)

print(f"  append (global): {t1*1000:.3f}ms")
print(f"  append (local):  {t2*1000:.3f}ms")
print(f"  comprehension:   {t3*1000:.3f}ms  ← usually fastest")

# ============================================================
# 7. Profiling with cProfile
# ============================================================
print("\n=== 7. cProfile (Quick Reference) ===")

profile_example = """
# How to profile your code:

# Option 1: Command line
# python -m cProfile -s cumulative my_script.py

# Option 2: In code
import cProfile, pstats

def my_work():
    data = [x**2 for x in range(100_000)]
    return sorted(data, reverse=True)[:100]

with cProfile.Profile() as pr:
    my_work()

stats = pstats.Stats(pr)
stats.sort_stats("cumulative")
stats.print_stats(10)    # show top 10 functions by cumulative time
"""

print(profile_example)
print("Day 27 complete! Measure first, then optimize where it matters most.")
