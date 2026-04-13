# Day 19 Exercises — OOP Advanced

Estimated time: 45–60 minutes

---

## Exercise 1 — Model Hierarchy

Build this class hierarchy:

```
BaseModel (abstract)
├── ClassificationModel
│   ├── BinaryClassifier
│   └── MultiClassClassifier
└── GenerativeModel
    └── LanguageModel
```

Rules:
- `BaseModel`: abstract; requires `predict()` and `evaluate()` to be implemented
- Each subclass should accept a `model_name` and maintain `is_trained` flag
- `ClassificationModel.evaluate(preds, labels)` → returns accuracy
- `GenerativeModel.generate(prompt, max_tokens)` → returns a string
- `LanguageModel` should override `generate()` to prepend "[LM]:" to output

Demonstrate polymorphism by calling `predict()` on a list of mixed model types.

---

## Exercise 2 — Mixin Composition

Create three mixins:

1. **`TimingMixin`**: Adds `timed_predict(text)` that wraps `predict()`, measures execution time with `time.perf_counter()`, and prints `"predict() took X.XXXXms"`

2. **`CachingMixin`**: Adds prediction caching. Stores results in `self._cache` dict. On `predict()`, check cache first — hit → return cached, miss → call method + cache result

3. **`LoggingMixin`**: Adds `self.logs` list; every call to `predict()` appends `{"input": text, "output": label, "time": timestamp}` to the list; adds `get_logs()` method

Compose a `ProductionClassifier(BaseModel, TimingMixin, CachingMixin, LoggingMixin)`.

---

## Exercise 3 — Plugin Architecture

Design a `ModelRegistry` class that:
1. Maintains a `registry: dict[str, type]` of model classes (not instances)
2. `register(name, cls)` — adds a class to registry  
3. `create(name, **kwargs)` — instantiates and returns a model by name
4. `list_models()` — prints available model names
5. `from_config(config_dict)` — reads `"model_type"` key and creates accordingly

```python
registry = ModelRegistry()
registry.register("sentiment", SentimentClassifier)
registry.register("keyword", KeywordClassifier)

model = registry.create("sentiment", model_name="production-v1")
```

---

## Exercise 4 — Gradient Tracker

Build a `GradientTracker` that could simulate monitoring during training:

```python
class GradientTracker:
    def __init__(self, layer_names: list[str]): ...
    
    def record(self, layer_name: str, gradient_norm: float) -> None: ...
    
    @property
    def has_vanishing_gradients(self) -> bool:
        """True if any layer's recent gradient norm < 1e-7"""
    
    @property
    def has_exploding_gradients(self) -> bool:
        """True if any layer's recent gradient norm > 100"""
    
    def summary(self) -> dict:
        """Returns {layer_name: {"mean": ..., "min": ..., "max": ...}}"""
    
    def __repr__(self): ...
```

Test by simulating 10 epochs with random gradient norms (including a few near-zero and very large values).

---

## Exercise 5 — `DataPipeline` with Inheritance

Create a pipeline class hierarchy:

```
DataPipeline (base)
├── TextPipeline
└── BatchPipeline
```

- `DataPipeline.__init__`: stores list of processing steps (`self.steps = []`)
- `DataPipeline.add_step(fn)` → returns `self` (method chaining)
- `DataPipeline.run(data)` → applies all steps sequentially
- `TextPipeline` adds default steps: strip, lowercase, remove_punctuation
- `BatchPipeline.run(records: list)` → applies pipeline to each record

Test:
```python
pipeline = TextPipeline().add_step(lambda s: s.replace("  ", " "))
cleaned = pipeline.run("  Hello, WORLD!!  ")
```

---

## Stretch Challenge — Method Resolution Order Deep Dive

Create this diamond inheritance structure:
```
        Animal
       /      \
    Mammal   Bird
       \      /
        Bat
```

Each class defines `describe()` that returns a string.  
Trace what `Bat().describe()` returns by examining `Bat.__mro__`.

Then add `super().describe()` calls through the chain and verify the output using Python's actual MRO order (print `Bat.__mro__` to confirm).
