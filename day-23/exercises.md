# Day 23 Exercises — Context Managers

Estimated time: 45–60 minutes

---

## Exercise 1 — Database Connection Simulator

Build `DatabaseContext` class:

```python
class DatabaseContext:
    def __init__(self, db_name: str, readonly: bool = False): ...
    def __enter__(self) -> "DatabaseContext": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool: ...
    
    def query(self, sql: str) -> list[dict]: ...  # simulated
    def insert(self, table: str, record: dict) -> None: ...
```

Rules:
- `__enter__`: "connects" (prints log), returns `self`
- `__exit__`: "disconnects" (prints log)
- If readonly and `insert()` is called → raise `PermissionError`
- If an exception occurs: print `"Transaction rolled back"` then let it propagate
- If no exception: print `"Transaction committed"`

---

## Exercise 2 — Managed Model Training Run

Using `@contextmanager`, write `training_run(config: dict)`:

```python
@contextmanager
def training_run(config: dict):
    ...

with training_run({"model": "bert", "epochs": 5}) as run:
    run["loss_history"] = [0.9, 0.7, 0.5, 0.4, 0.35]
    run["final_accuracy"] = 0.87
```

The context manager should:
1. Create a run dict with `run_id`, `start_time`, `config`
2. `yield` the run dict to the caller
3. On success: add `end_time`, `status: "success"`, save to `runs/{run_id}.json`
4. On failure: add `status: "failed"`, `error: str(e)`, save to `runs/{run_id}_failed.json`

---

## Exercise 3 — Cache Context

Write `@contextmanager` called `cached_computation(key, cache_dir)`:

1. Checks if `{cache_dir}/{key}.json` exists
2. If cache HIT: loads data, then uses `yield data` — caller gets cached result
3. If cache MISS: `yield {}` (empty dict), caller populates it, then saves after yield
4. Print `"Cache HIT"` or `"Cache MISS"` accordingly

```python
with cached_computation("tokenizer_vocab", ".cache") as result:
    if not result:
        result.update(build_vocabulary(corpus))
```

---

## Exercise 4 — `ExitStack` Multi-file Processor

Write a function `process_multiple_files(paths: list[str])` that:
1. Uses `contextlib.ExitStack` to open all files simultaneously
2. Reads the first line from each
3. Computes the total word count across all files
4. Automatically closes all files (via ExitStack)
5. Handles `FileNotFoundError` for individual files using `suppress`

---

## Exercise 5 — Profiling Context Manager

Write `ProfilerContext`:
- Tracks total calls, total time, and per-code-block timings stored in `self.records`
- Supports nested usage: each `with profiler.section("name"):` logs a named section
- After all `with` blocks, `profiler.report()` prints a sorted table of sections:
  `section_name | calls | total_ms | avg_ms`

```python
profiler = ProfilerContext()
for i in range(100):
    with profiler.section("tokenize"):
        tokens = text.split()
    with profiler.section("encode"):  
        ids = [vocab.get(t, 0) for t in tokens]

profiler.report()
```

---

## Stretch Challenge — Thread-Safe Resource Pool

Build a `ResourcePool` context manager that:
1. Manages a fixed pool of reusable resources (e.g., simulated DB connections, list of strings)
2. `with pool.acquire() as resource:` — checks out one resource, yields it
3. On `__exit__`: returns resource to pool
4. If pool is empty: wait up to `timeout` seconds, then raise `TimeoutError`
5. Track metrics: `pool.stats()` returns `{total, available, acquired, wait_events}`

Use `threading.Lock` for thread-safe pool management.
