# Day 18 Notes — OOP Basics

## Class Anatomy

```python
class ClassName:
    """Docstring for the class."""
    
    class_attribute = "shared by all instances"
    
    def __init__(self, param1, param2):    # constructor
        self.instance_attr1 = param1       # instance attribute
        self.instance_attr2 = param2
    
    def instance_method(self):             # regular method
        return self.instance_attr1
    
    @classmethod
    def from_something(cls, data):         # alternative constructor
        return cls(data["p1"], data["p2"])
    
    @staticmethod
    def utility_function(x):              # no self, no cls
        return x * 2
```

---

## `self` — What Is It?

`self` refers to the **specific instance** that the method is being called on.

```python
a = ModelConfig("bert")
b = ModelConfig("gpt")

a.describe()  # self = a inside describe()
b.describe()  # self = b inside describe()
```

Python passes `self` automatically — you never supply it when calling methods.

---

## Attributes

| Type | Where defined | Shared? |
|------|--------------|---------|
| **Class attribute** | Class body, outside `__init__` | All instances share the same value |
| **Instance attribute** | Inside `__init__` via `self.x = ...` | Each instance has its own copy |

```python
class Model:
    count = 0              # class attribute
    
    def __init__(self, name):
        self.name = name   # instance attribute
        Model.count += 1   # modify class attribute

m1 = Model("bert")
m2 = Model("gpt")
print(Model.count)  # 2
print(m1.name)      # "bert"
print(m2.name)      # "gpt"
```

---

## The Three Method Types

### 1. Instance Method (most common)
```python
def train(self, data):      # first param is self
    self.is_trained = True  # can read/write instance state
```

### 2. Class Method (`@classmethod`) — Alternative Constructors
```python
@classmethod
def from_config_file(cls, path):  # first param is cls
    data = json.load(open(path))
    return cls(**data)            # creates an instance
```

### 3. Static Method (`@staticmethod`) — Pure Utility
```python
@staticmethod
def sigmoid(x):     # no self, no cls — just a function
    return 1 / (1 + math.exp(-x))
```

---

## Properties — Smart Attributes

```python
class LearningRate:
    def __init__(self, value):
        self._value = value        # underscore = "private"
    
    @property
    def value(self):               # getter
        return self._value
    
    @value.setter
    def value(self, new_val):      # setter with validation
        if new_val <= 0:
            raise ValueError("LR must be positive")
        self._value = new_val
    
    @property
    def warmup_lr(self):           # computed, read-only
        return self._value * 0.1

lr = LearningRate(0.001)
print(lr.value)       # 0.001  — calls getter
lr.value = 0.0001     # calls setter
print(lr.warmup_lr)   # 0.00001 — computed property
```

---

## Essential Magic Methods (Dunders)

| Method | When called | Example |
|--------|------------|---------|
| `__init__(self, ...)` | Object creation | `obj = MyClass(...)` |
| `__repr__(self)` | `repr(obj)`, debug output | Should be unambiguous |
| `__str__(self)` | `str(obj)`, `print(obj)` | Human-readable |
| `__len__(self)` | `len(obj)` | `len(dataset)` |
| `__getitem__(self, key)` | `obj[key]` | `dataset[0]` |
| `__setitem__(self, key, val)` | `obj[key] = val` | `config["lr"] = 0.01` |
| `__contains__(self, item)` | `item in obj` | `"word" in vocab` |
| `__eq__(self, other)` | `obj1 == obj2` | Value equality |
| `__iter__(self)` | `for x in obj` | See Day 20 |
| `__enter__`/`__exit__` | `with obj:` | See Day 23 |

---

## Naming Conventions

| Convention | Meaning | Example |
|------------|---------|---------|
| `name` | Public attribute | `self.layers` |
| `_name` | "Private" — don't use externally | `self._weights` |
| `__name` | Name-mangled — can't be accessed as-is | `self.__secret` |
| `__name__` | Special Python dunder | `__init__`, `__str__` |

---

## OOP in ML Frameworks

All ML model classes follow this pattern:

```python
# PyTorch (simplified)
class Layer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()          # always call super
        self.weight = nn.Parameter(...)
        self.bias = nn.Parameter(...)
    
    def forward(self, x):          # instance method
        return x @ self.weight + self.bias

# scikit-learn (simplified)
class MyClassifier(BaseEstimator):
    def __init__(self, max_depth=3):
        self.max_depth = max_depth  # store all params in __init__
    
    def fit(self, X, y):
        # ... training logic
        return self                 # return self for chaining
    
    def predict(self, X):
        return self._tree.predict(X)
```

---

## Quick-Fire Interview Questions

1. **What is `self` in Python?**  
   A reference to the current instance; passed automatically by Python when calling instance methods.

2. **What's the difference between a class attribute and an instance attribute?**  
   Class attributes are shared by all instances; instance attributes are unique per object (set in `__init__`).

3. **What does `@property` do?**  
   Allows a method to be accessed like an attribute. Enables validation on get/set and computed attributes.

4. **When would you use `@classmethod` vs `@staticmethod`?**  
   `@classmethod` when you need to create instances or access class state; `@staticmethod` for pure utility functions logically related to the class.

5. **What's the difference between `__str__` and `__repr__`?**  
   `__str__` is for end-users (readable); `__repr__` is for developers (unambiguous, ideally eval-able).
