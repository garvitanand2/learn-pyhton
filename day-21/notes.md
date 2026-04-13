# Day 21 Notes — Week 3 Mini Project: TextFlow Pipeline

## Architecture Overview

```
Data Source (generator)
       ↓
   Pipeline
   ├── TextCleaner      (OOP: PipelineStep subclass)
   ├── Tokenizer        (OOP: PipelineStep subclass)
   ├── LengthFilter     (OOP: returns None to drop records)
   ├── FeatureExtractor (OOP: enriches records)
   └── SentimentLabeler (OOP: adds labels)
       ↓
     Report +  JSON output (File I/O, Day 16)
```

---

## Concepts Applied

| Concept | Where Used |
|---------|-----------|
| Modules (Day 15) | `re`, `json`, `pathlib`, `collections`, `abc`, `datetime` |
| File I/O (Day 16) | JSON output with `Path.mkdir()` and `open()` |
| Exception handling (Day 17) | `safe_process()` wrapper in PipelineStep |
| OOP basics (Day 18) | `Record` class, `@property`, `__repr__` |
| OOP advanced (Day 19) | ABC interface, LoggingMixin, inheritance chain |
| Generators (Day 20) | `generate_records()` source, pipeline streams records |

---

## Design Patterns Used

### 1. Template Method Pattern
`PipelineStep.safe_process()` calls `self.process()` with error handling.  
Each concrete step only needs to implement `process()`.

### 2. Chain of Responsibility
Each step receives a record, transforms (or drops) it, passes to next.

### 3. Builder/Fluent Interface
```python
pipeline = (
    Pipeline("name")
    .add_step(TextCleaner())
    .add_step(Tokenizer())
    .add_step(LengthFilter())
)
```

### 4. Strategy Pattern (via Polymorphism)
Steps can be swapped/reordered without changing Pipeline code.

### 5. Generator as Data Source
`generate_records()` streams lazily — pipeline never holds all records.

---

## Key Takeaways for Gen AI Engineering

### Modular pipelines are everywhere
- LangChain chains → same pattern
- Hugging Face tokenization pipeline → same pattern
- scikit-learn `Pipeline` → same pattern

### `None` as a drop sentinel
Returning `None` from a step cleanly drops records without exceptions.

### `safe_process` wrapping
Never crash the whole pipeline on one bad record. Catch, log, continue.

### Why ABC?
`@abstractmethod` forces ALL step subclasses to implement `process()`.  
You'll never accidentally create a broken step that compiles but silently does nothing.

---

## How to Extend This Project

| Feature | How to add |
|---------|-----------|
| Parallel processing | Use `concurrent.futures.ThreadPoolExecutor` |
| Database output | Add `DatabaseSink(PipelineStep)` step |
| Config-driven | Load step list from JSON config file |
| Progress bar | Wrap generator with `tqdm` |
| Batch processing | Modify `run()` to yield batches to steps |
| Model inference | Add `ModelInferenceStep` that calls predict() |

---

## Quick Debugging Checklist

When your pipeline produces wrong output:

1. ✅ Add `print(record)` at start of each `process()` to trace data flow
2. ✅ Check `record.errors` for suppressed exceptions  
3. ✅ Temporarily remove steps one at a time to isolate the bug
4. ✅ Verify `generate_records()` is producing expected input
5. ✅ Check filter steps — is something over-aggressively dropping records?
