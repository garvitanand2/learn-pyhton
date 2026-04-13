# Day 23 Notes — Context Managers

## What Is a Context Manager?

A context manager is any object that implements `__enter__` and `__exit__`.  
The `with` statement calls these methods automatically.

```python
with expression as variable:
    # body

# Equivalent to:
ctx = expression
variable = ctx.__enter__()
try:
    # body
except:
    ctx.__exit__(exception_type, exception_value, traceback)
    raise
else:
    ctx.__exit__(None, None, None)
```

---

## The `__exit__` Signature

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    cleanup_resources()
    
    # Return True  → exception is SUPPRESSED (swallowed)
    # Return False/None → exception PROPAGATES
```

| Parameter | Meaning |
|-----------|---------|
| `exc_type` | Exception class (e.g., `ValueError`) or `None` |
| `exc_val` | Exception instance or `None` |
| `exc_tb` | Traceback object or `None` |

---

## Class vs `@contextmanager`

### Class approach
```python
class ManagedConnection:
    def __init__(self, host):
        self.host = host
    
    def __enter__(self):
        self.conn = connect(self.host)
        return self.conn
    
    def __exit__(self, *args):
        self.conn.close()
        return False
```

### `@contextmanager` approach (usually cleaner)
```python
from contextlib import contextmanager

@contextmanager
def managed_connection(host):
    conn = connect(host)
    try:
        yield conn       # ← body of `with` runs here
    finally:
        conn.close()     # ← always runs
```

**The code before `yield` = `__enter__`**  
**The code after `yield` = `__exit__`**  
**`try/finally` ensures cleanup even on exception**

---

## contextlib Utilities

```python
from contextlib import suppress, nullcontext, ExitStack

# suppress: silently ignore specific exceptions
with suppress(FileNotFoundError, PermissionError):
    os.remove("maybe_missing.txt")

# nullcontext: no-op context manager (useful for optional contexts)
ctx = model.eval_context() if inference_mode else nullcontext()
with ctx:
    predictions = model.predict(data)

# ExitStack: manage variable number of context managers
from contextlib import ExitStack
with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in file_list]
    # all files automatically closed when ExitStack exits
```

---

## Real ML/AI Patterns

### PyTorch inference
```python
# torch.no_grad() is a context manager!
with torch.no_grad():          # disables gradient tracking
    output = model(input_ids)  # faster inference, less memory

# model.eval() is a method, used alongside:
model.eval()
with torch.no_grad():
    output = model(batch)
model.train()   # restore for next training step
```

### Managed experiments
```python
@contextmanager
def experiment(name, config):
    run_id = f"{name}_{datetime.now():%Y%m%d_%H%M%S}"
    Path(f"runs/{run_id}").mkdir(parents=True)
    try:
        yield run_id         # caller gets the run_id
    except Exception as e:
        save_failure_log(run_id, e)
        raise
    else:
        save_success_metrics(run_id)

with experiment("bert_finetune", config) as run_id:
    train_model(run_id, config)
```

### Temporary directory
```python
import tempfile
with tempfile.TemporaryDirectory() as tmp_dir:
    # work in tmp_dir
    process_files(tmp_dir)
# directory is automatically deleted here
```

---

## Why Not Just try/finally?

You could always write:
```python
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()
```

But `with` is:
- **Shorter**: less boilerplate
- **Reusable**: encapsulates the whole pattern in a class/function
- **Composable**: stack multiple with one `with` statement
- **Readable**: intent is clear

---

## Quick-Fire Interview Questions

1. **What methods define a context manager?**  
   `__enter__` (setup, returns value for `as` clause) and `__exit__` (teardown, receives exception info).

2. **When does `__exit__` run?**  
   Always — both on normal exit and when an exception occurs.

3. **How do you suppress an exception in `__exit__`?**  
   Return `True`; returning `False` or `None` lets the exception propagate.

4. **What does `@contextmanager` do?**  
   Converts a generator function into a context manager; code before `yield` = `__enter__`, after = `__exit__`.

5. **What is `contextlib.suppress`?**  
   A context manager that silently ignores specific exception types — cleaner than an empty `except` block.
