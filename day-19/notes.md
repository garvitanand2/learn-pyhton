# Day 19 Notes — OOP Advanced: Inheritance & Polymorphism

## Inheritance in One Diagram

```
BaseModel
├── SentimentClassifier
│   └── PreprocessingModel     ← inherits from SentimentClassifier
├── KeywordClassifier
└── ZeroShotClassifier
```

**Key rule:** A subclass IS-A parent class.  
`SentimentClassifier` IS-A `BaseModel` ✓

---

## Syntax

```python
class Child(Parent):
    def __init__(self, child_param, *args, **kwargs):
        super().__init__(*args, **kwargs)  # ALWAYS call super().__init__
        self.child_specific = child_param  # add new attributes
    
    def overridden_method(self):           # override parent behavior
        result = super().overridden_method()  # optionally call parent
        return result + " plus child behavior"
    
    def new_method(self):                  # completely new behavior
        pass
```

---

## `super()` — Calling the Parent

`super()` returns a proxy to the **parent class** (following MRO order).

```python
class ChildModel(BaseModel):
    def train(self, data):
        super().train(data)       # runs BaseModel.train() first
        self._extra_step(data)    # then do extra stuff
```

**Without `super().__init__`:** parent's `__init__` never runs → missing attributes!

---

## Method Resolution Order (MRO)

Python uses C3 linearization to determine which method to call in multiple inheritance.

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass   # multiple inheritance

print(D.__mro__)
# (D, B, C, A, object)
```

Python searches methods **left to right** in the MRO chain.

---

## Polymorphism

**Poly** = many, **morph** = form.  
Same method name, different behavior per class.

```python
# All share .predict(text) interface
models = [SentimentClassifier(), KeywordClassifier(), ZeroShotClassifier()]

for model in models:
    label = model.predict("test text")   # ← different code runs for each
    print(f"{type(model).__name__}: {label}")
```

In ML, polymorphism lets you write:
```python
for model in [bert, gpt, t5, roberta]:
    predictions = model.predict(test_data)  # each works differently
```

---

## Abstract Methods (Using abc)

Force subclasses to implement specific methods:

```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def predict(self, text: str) -> str:
        """All subclasses MUST implement this."""
        pass
    
    @abstractmethod
    def train(self, data: list) -> None:
        pass

# This would CRASH at instantiation:
# model = BaseModel()  # TypeError: Can't instantiate abstract class

# Subclass MUST implement predict() and train()
class MyModel(BaseModel):
    def predict(self, text): return "positive"
    def train(self, data): self.is_trained = True
```

---

## Mixins

A **mixin** is a class designed to add specific functionality via multiple inheritance:

```python
class LoggingMixin:
    def log(self, msg):
        print(f"[{type(self).__name__}] {msg}")

class SerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.to_dict())

# Compose behavior:
class MyModel(BaseModel, LoggingMixin, SerializableMixin):
    def predict(self, text):
        self.log(f"Predicting: {text}")
        return "positive"
    def to_dict(self):
        return {"name": self.model_name}
```

Mixins should:
- Be small and focused (single responsibility)
- Not define `__init__` (or use `super()` carefully)
- Never stand alone as useful classes

---

## `isinstance()` and `issubclass()`

```python
clf = SentimentClassifier("my-model")

isinstance(clf, SentimentClassifier)  # True
isinstance(clf, BaseModel)            # True — IS-A relationship!
isinstance(clf, KeywordClassifier)    # False

issubclass(SentimentClassifier, BaseModel)  # True
issubclass(str, object)                     # True — everything inherits from object
```

**Production use:** Validate inputs to Pipeline classes:
```python
def add_model(self, model):
    if not isinstance(model, BaseModel):
        raise TypeError(f"Expected BaseModel, got {type(model).__name__}")
```

---

## Key Patterns in ML Frameworks

### PyTorch-style
```python
class MyLayer(nn.Module):
    def __init__(self):
        super().__init__()         # required!
        self.linear = nn.Linear(768, 256)
    
    def forward(self, x):          # override
        return self.linear(x)
```

### scikit-learn style
```python
class MyTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        # learn from data
        return self                # always return self
    
    def transform(self, X):
        return X * self.scale_
```

---

## Quick-Fire Interview Questions

1. **What does `super()` do?**  
   Returns a proxy to the parent class (following MRO), used to call parent methods.

2. **Why must you always call `super().__init__()` in subclass `__init__`?**  
   Without it, the parent class constructor never runs, so parent attributes are never initialized.

3. **What is polymorphism? Give an ML example.**  
   Same method name on different classes with different implementations. E.g., BERT, GPT, T5 all have `.predict()` but implement it differently.

4. **What is a mixin?**  
   A class designed to be mixed into another via multiple inheritance to add one specific capability (logging, serialization, etc.).

5. **What does `isinstance(x, ParentClass)` return for a child instance?**  
   `True` — because a child IS-A parent via inheritance.
