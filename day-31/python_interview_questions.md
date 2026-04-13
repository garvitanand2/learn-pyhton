# Python Interview Questions — 100 Q&As
## Sections: Beginner (1-35) | Intermediate (36-70) | Advanced (71-100)

---

## BEGINNER (1–35)

**1. What is Python? What are its key features?**  
Python is a high-level, interpreted, dynamically-typed general-purpose language. Key features: readable syntax, automatic memory management (garbage collection), large standard library, first-class functions, and cross-platform support.

**2. What is the difference between a list and a tuple?**  
Lists are mutable (can change elements); tuples are immutable (cannot). Tuples are slightly faster and hashable (can be dict keys or set members).

**3. What is a dictionary? How is it different from a list?**  
A dict stores key-value pairs with O(1) average lookup by key. A list stores ordered values with O(1) index access but O(n) search. Dicts use hashing; lists use contiguous memory.

**4. What is `None` in Python?**  
`None` is the singleton object representing "no value". It is the only instance of `NoneType`. Functions return `None` implicitly when no `return` statement is reached.

**5. What is the difference between `==` and `is`?**  
`==` compares value (calls `__eq__`). `is` compares identity (same object in memory). Use `is` only with singletons: `None`, `True`, `False`.

**6. What are Python's built-in data types?**  
`int`, `float`, `complex`, `bool`, `str`, `bytes`, `list`, `tuple`, `dict`, `set`, `frozenset`, `NoneType`.

**7. What is the difference between `append()` and `extend()` on a list?**  
`append(x)` adds `x` as a single element (even if `x` is a list). `extend(iterable)` unpacks `iterable` and adds each element.

**8. How do you reverse a list?**  
Three ways: `lst.reverse()` (in-place), `lst[::-1]` (new list), `list(reversed(lst))` (new list, lazy).

**9. What is list/dict/set comprehension?**  
Concise syntax for creating collections: `[x**2 for x in range(10) if x % 2 == 0]`. Faster than equivalent `for` + `append` and more readable.

**10. What does `*args` and `**kwargs` mean?**  
`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dict. Both can be combined: `def fn(*args, **kwargs)`.

**11. What is a lambda function?**  
An anonymous, one-expression function: `lambda x, y: x + y`. Used inline where a full `def` would be overly verbose (e.g., as a `key=` argument).

**12. What is the difference between `range()` and `list(range())`?**  
`range()` returns a lazy range object (no list in memory). `list(range())` materializes all values. Prefer `range()` in `for` loops.

**13. How does Python handle memory management?**  
Python uses reference counting plus a cyclic garbage collector. When an object's reference count drops to zero, its memory is freed. The `gc` module handles circular references.

**14. What are Python's comparison operators?**  
`==`, `!=`, `<`, `>`, `<=`, `>=`, `is`, `is not`, `in`, `not in`.

**15. What is string slicing?**  
`s[start:stop:step]` — returns a substring. Negative indices count from the end: `s[-3:]` = last 3 chars. Default step=1; `s[::-1]` reverses.

**16. What is the difference between `str.split()` and `str.partition()`?**  
`split(sep, maxsplit=-1)` splits all occurrences (returns list). `partition(sep)` splits at the FIRST occurrence only, returning a 3-tuple `(before, sep, after)`.

**17. What does the `in` operator do?**  
Membership test. Returns `True` if value is in container. O(1) for `set`/`dict`, O(n) for `list`.

**18. What is a generator? How is it different from a list?**  
A generator produces values lazily one at a time using `yield`. It uses O(1) memory regardless of data size. A list stores all elements in memory simultaneously.

**19. What is `enumerate()`?**  
Wraps an iterable, yielding `(index, value)` pairs: `for i, item in enumerate(lst):`.

**20. What is `zip()`?**  
Combines multiple iterables element-by-element into tuples: `zip([1,2], ['a','b'])` → `(1,'a'), (2,'b')`. Stops at the shortest iterable.

**21. What is the difference between `//` and `/`?**  
`/` always returns a float. `//` is floor division — returns the floor of the quotient as an int.

**22. How do you check the type of a variable?**  
`type(x)` returns the exact type. `isinstance(x, MyClass)` also returns True for subclasses — preferred for type checking.

**23. What is a set? When would you use it?**  
An unordered collection of unique hashable elements. Use for: deduplication, fast membership testing, set algebra (union `|`, intersection `&`, difference `-`).

**24. What is `f-string` formatting?**  
`f"Hello {name}!"` — inline expression evaluation in string literals. Faster than `.format()` and more readable. Supports expressions: `f"{x:.2f}"`, `f"{x!r}"`.

**25. What is `pass` in Python?**  
A no-op statement. Used as a syntactic placeholder where a statement is required but no action needed: empty function/class body, bare `except` clause.

**26. What is the `global` keyword?**  
Declares that a variable name inside a function refers to the module-level (global) variable rather than creating a new local one. Avoid in production code; prefer returning values.

**27. What is `__name__ == "__main__"`?**  
`__name__` is `"__main__"` only when the file is run directly (not imported). Guards code that should only run as a script, not when the module is imported.

**28. What is exception handling? Name the keywords.**  
`try` — code that might raise. `except` — handle specific exceptions. `else` — runs if no exception. `finally` — always runs. `raise` — throw an exception.

**29. What is the difference between `break`, `continue`, and `pass`?**  
`break` exits the entire loop. `continue` skips the current iteration. `pass` does nothing (placeholder).

**30. How do you open and read a file in Python?**  
`with open("file.txt", "r", encoding="utf-8") as f: content = f.read()`. Always use `with` to ensure the file is closed.

**31. What is the GIL (Global Interpreter Lock)?**  
A mutex in CPython that allows only one thread to execute Python bytecode at a time. Consequence: CPU-bound threading doesn't speed up on multi-core. Workaround: `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.

**32. What is `*` (star) unpacking?**  
`a, *b, c = [1,2,3,4,5]` → a=1, b=[2,3,4], c=5. Also used to unpack into function calls: `fn(*args)`, merge lists: `[*list1, *list2]`.

**33. What is the difference between shallow and deep copy?**  
Shallow copy (`copy.copy()`) copies the container but shares nested objects. Deep copy (`copy.deepcopy()`) recursively copies everything. Default `list[:]` is shallow.

**34. What are Python's truthy and falsy values?**  
Falsy: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`. Everything else is truthy. Used in `if x:` guards.

**35. What is a docstring?**  
A string literal as the first statement in a function, class, or module: `"""Description."""`. Accessible via `help()` and `fn.__doc__`.

---

## INTERMEDIATE (36–70)

**36. What is a decorator? How does it work?**  
A decorator is a callable that wraps a function to modify or extend its behavior. `@dec` is syntactic sugar for `fn = dec(fn)`. Always use `functools.wraps` to preserve the wrapped function's metadata.

**37. What is `@functools.wraps` and why is it needed?**  
`@wraps(fn)` copies `__name__`, `__doc__`, `__module__` from the wrapped function to the wrapper. Without it, `fn.__name__` becomes `"wrapper"` and `help(fn)` shows the wrong docstring.

**38. What is a context manager? Name two ways to implement one.**  
An object implementing `__enter__` and `__exit__` used in `with` statements for resource management. Ways: (1) class with `__enter__`/`__exit__`; (2) `@contextlib.contextmanager` generator.

**39. What is `__enter__` and `__exit__`?**  
`__enter__` runs at the start of the `with` block; its return value is bound to the `as` variable. `__exit__(exc_type, exc_val, exc_tb)` runs at the end; returning `True` suppresses any exception.

**40. What is a generator expression vs. list comprehension?**  
Both produce values but a generator expression uses `()` and yields lazily (O(1) memory). A list comprehension uses `[]` and creates the full list immediately.

**41. What is `yield from`?**  
Delegates to another iterable/generator. `yield from sub_gen()` is equivalent to `for item in sub_gen(): yield item` but more efficient and forwards `throw` and `close` calls.

**42. What is `*args` vs `**kwargs` — can you use both?**  
Yes: `def fn(pos, *args, kw_only=True, **kwargs)`. Order rule: regular args → `*args` → keyword-only args → `**kwargs`.

**43. What is the difference between `classmethod` and `staticmethod`?**  
`@classmethod` receives `cls` (the class) as first argument — can create instances or access class state. `@staticmethod` receives no implicit first argument — just a namespaced function with no class/instance access needed.

**44. What is `@property`?**  
A decorator that makes a method behave like an attribute. `@prop.setter` defines the setter. Used for computed properties or validation on attribute access.

**45. What is MRO (Method Resolution Order)?**  
The order Python searches for methods in multiple inheritance. Determined by the C3 linearization algorithm. View with `ClassName.__mro__` or `ClassName.mro()`.

**46. What is the difference between `__str__` and `__repr__`?**  
`__str__` is the human-readable string (used by `print`/`str()`). `__repr__` is the unambiguous developer representation (used in REPL/debugging). If only one is defined, `__str__` falls back to `__repr__`.

**47. What is `__slots__`?**  
Replaces the instance `__dict__` with a fixed-size C struct, reducing per-instance memory by ~60%. Useful for classes with many instances. Disallows dynamic attribute assignment.

**48. What is `lru_cache` and how does it work?**  
`@functools.lru_cache(maxsize=N)` memoizes function results in a dict keyed by arguments (LRU eviction when maxsize exceeded). Works only with hashable arguments. Check stats with `.cache_info()`.

**49. What is the difference between `map()`, `filter()`, and `reduce()`?**  
`map(fn, iter)` applies `fn` to each element (returns iterator). `filter(pred, iter)` keeps elements where `pred(x)` is truthy. `reduce(fn, iter, init)` accumulates a single value.

**50. What is `functools.partial`?**  
Creates a new callable with some arguments pre-filled: `multiply_by_2 = partial(operator.mul, 2)`.

**51. What is a namedtuple?**  
`from collections import namedtuple; Point = namedtuple("Point", ["x","y"])`. Immutable, lighter than a class, field access by name or index. For mutable named fields, use `@dataclass`.

**52. What is `defaultdict`?**  
A `dict` subclass that calls a factory for missing keys: `dd = defaultdict(list)` → `dd["new_key"].append(1)` without KeyError.

**53. What is `Counter`?**  
A `dict` subclass for counting hashable objects. `Counter(items).most_common(n)` returns the n most frequent elements.

**54. What is `deque`?**  
`collections.deque` — a double-ended queue with O(1) `append`/`appendleft`/`pop`/`popleft`. More efficient than `list.insert(0, x)` which is O(n).

**55. What is the difference between `is` and `==` for strings?**  
`==` compares content. `is` compares identity. CPython interns short strings, so `"hello" is "hello"` may be `True` but this should never be relied upon — always use `==` for strings.

**56. What is `__init__` vs `__new__`?**  
`__new__` creates the object (class method, allocates memory). `__init__` initializes it (instance method, sets attributes). Usually only override `__new__` for immutable types or singletons.

**57. What is `super()`?**  
Returns a proxy to the next class in the MRO. Used to call a parent method without hard-coding the parent class name, enabling cooperative multiple inheritance.

**58. What are abstract methods? How do you define them?**  
Methods that MUST be overridden in subclasses. Use `from abc import ABC, abstractmethod` and decorate with `@abstractmethod`. Instantiating an ABC with unimplemented abstract methods raises `TypeError`.

**59. What is the `with` statement good for?**  
Resource management: ensures teardown (file close, lock release, connection close) even if an exception is raised. Cleaner than try/finally.

**60. What is `PYTHONPATH`?**  
An environment variable containing extra directories Python adds to `sys.path` for `import` resolution. Set it to include your project root when running outside a virtual environment.

**61. What is monkey patching?**  
Replacing methods or attributes on a class/module at runtime: `MyClass.method = new_function`. Used in testing (via `unittest.mock.patch`) but dangerous in production due to hidden side effects.

**62. How does `pickle` work? When is it unsafe?**  
`pickle` serializes Python objects to bytes and deserializes them. UNSAFE to unpickle data from untrusted sources — arbitrary code can be executed during deserialization.

**63. What is the difference between threads and processes in Python?**  
Threads share memory but the GIL limits CPU parallelism — good for I/O-bound tasks. Processes each have a separate Python interpreter — true CPU parallelism, but higher overhead and no shared memory by default.

**64. What is `asyncio`?**  
Python's async framework for concurrent I/O-bound tasks on a single thread using cooperative multitasking (`async def`, `await`). Does NOT bypass the GIL and is not for CPU-bound work.

**65. What is a `Protocol` in Python?**  
From `typing.Protocol` — defines an interface via structural subtyping (duck typing). Any class with the required methods/attributes satisfies the Protocol without explicit inheritance. Checked by `mypy`.

**66. What is `TypeVar`?**  
A generic type variable: `T = TypeVar("T")`. Used to write type-safe generic functions that preserve the type of their inputs: `def first(lst: list[T]) -> T`.

**67. What is `dataclasses.field()`?**  
Provides per-field customization in `@dataclass`. Important uses: `field(default_factory=list)` for mutable defaults, `field(repr=False)` to hide from `__repr__`, `field(compare=False)` to exclude from `__eq__`.

**68. What is `__post_init__` in a dataclass?**  
A hook called automatically at the end of the generated `__init__`. Used for validation, computed fields, or any setup that depends on multiple fields.

**69. What is `json.dumps` vs `json.dump`?**  
`dumps` serializes to a string. `dump` serializes to a file object. Same for `loads` (from string) vs `load` (from file).

**70. What is the `pathlib` module?**  
Object-oriented filesystem paths (`Path`). Replaces `os.path`. Key methods: `Path.read_text()`, `Path.write_text()`, `Path.glob()`, `Path.mkdir(parents=True)`, `Path.exists()`, `/` operator for joining.

---

## ADVANCED (71–100)

**71. Explain Python's data model (dunder methods).**  
Python objects expose behavior through special methods. `__len__`, `__getitem__`, `__iter__`, `__contains__` make objects "feel like" built-in containers. `__enter__`/`__exit__` enable context managers. `__call__` makes objects callable. This is what enables duck typing.

**72. What is a descriptor?**  
An object that defines `__get__`, `__set__`, `__delete__` and is used as a class attribute. Python's `property`, `classmethod`, `staticmethod` are all descriptors. Used to implement ORM fields, validation logic, lazy properties.

**73. What is `__getattr__` vs `__getattribute__`?**  
`__getattribute__` is called for EVERY attribute access. `__getattr__` is called only when the normal lookup fails. Override `__getattr__` for dynamic attribute generation; `__getattribute__` rarely.

**74. What is the difference between `__del__` and a context manager?**  
`__del__` (finalizer) is called when an object is garbage collected — timing is non-deterministic. Context managers have deterministic cleanup via `__exit__`. Always prefer context managers for resource management.

**75. What is a metaclass?**  
A class whose instances are classes. `type` is the default metaclass of all classes. Override `type.__new__` in a metaclass to customize class creation (auto-register subclasses, validate class definitions, add methods).

**76. What is `__init_subclass__`?**  
A hook called on the base class whenever a subclass is defined. Simpler than a metaclass for most registration/validation patterns: `class Base: def __init_subclass__(cls, **kwargs): registry.append(cls)`.

**77. What is a coroutine? How is it different from a regular generator?**  
A coroutine is defined with `async def` and can `await` other coroutines/awaitables. Regular generators use `yield` for data production. Coroutines use `await` for cooperative suspension at I/O points.

**78. What is `asyncio.gather()` vs `asyncio.create_task()`?**  
`gather(*coros)` runs coroutines concurrently and returns all results together. `create_task(coro)` schedules a coroutine without waiting — allows background tasks. `gather` = concurrent fan-out; `create_task` = fire-and-forget.

**79. Explain Python's import system.**  
`import` first checks `sys.modules` cache. If not cached, searches `sys.path` directories in order, compiles to bytecode, executes the module, caches in `sys.modules`. Relative imports use dot notation within packages.

**80. What is `__all__` in a module?**  
A list of names that `from module import *` should export. If missing, `*` imports all names not starting with `_`. Good practice: always define `__all__` in public modules.

**81. How does `lru_cache` handle mutable arguments?**  
It doesn't — `lru_cache` requires hashable arguments. Calling it with a `list` or `dict` raises `TypeError: unhashable type`. Workaround: convert to `tuple` before passing.

**82. What is `__slots__`? What are its trade-offs?**  
Replaces per-instance `__dict__` with a C-level struct. Pro: ~60% memory reduction, faster attribute access. Con: no dynamic attributes, needs re-declaration in subclasses, breaks `__weakref__` unless added explicitly.

**83. What is the decorator order for stacked decorators?**  
Applied bottom-up at decoration time: `@A @B def fn` → `fn = A(B(fn))`. Called top-down at call time: A's wrapper calls B's wrapper calls fn.

**84. What is `contextlib.ExitStack`?**  
A context manager that dynamically stacks other context managers. Useful when the number of context managers is variable (e.g., open N files): `with ExitStack() as stack: [stack.enter_context(open(f)) for f in files]`.

**85. What is `__future__` and why use `from __future__ import annotations`?**  
`from __future__ import annotations` makes all annotations strings (PEP 563 — postponed evaluation). Allows forward references: `def fn(x: "MyClass") -> "MyClass"` without quotes.

**86. What is `typing.TypedDict` vs `@dataclass`?**  
Both annotate structured data. `TypedDict` is a regular `dict` at runtime — backwards-compatible serialization, JSON-like access. `@dataclass` is a class with methods — supports `@property`, inheritance, `asdict`. Use TypedDict for API schemas/config dicts; dataclass for objects with behavior.

**87. What is `typing.Literal`?**  
Restricts a type to specific constant values: `def fn(mode: Literal["train", "eval"]) -> None`. `mypy` flags calls with any other string.

**88. What is `typing.Annotated`?**  
Attaches metadata to a type for runtime inspection by frameworks (FastAPI, Pydantic): `Annotated[int, Field(gt=0)]`. The type checker uses only the first argument; frameworks use the rest.

**89. What is `sys.getsizeof()`? What does it NOT show?**  
Returns the immediate memory size of an object in bytes. Does NOT include the memory of referenced objects (a list's getsizeof gives the list overhead, not the size of its elements).

**90. What is monkey patching in tests vs production?**  
In tests: safe, scoped via `unittest.mock.patch` — restored after each test. In production: dangerous — permanently alters global state, breaks encapsulation, causes hard-to-debug behavior.

**91. How would you implement a thread-safe singleton?**  
Use a module — Python module imports are themselves singletons (only executed once). For class-based: use `threading.Lock` with double-checked locking, or a metaclass.

**92. What is `weakref`?**  
A reference to an object that doesn't prevent garbage collection. Used for caches and circular reference breaking: `import weakref; cache[id] = weakref.ref(obj)`.

**93. What is the difference between `@staticmethod` and a module-level function?**  
No functional difference — both have no implicit first argument. `@staticmethod` is inside the class namespace (accessed as `ClassName.method()`). Module-level functions are accessed via `import`. Use `@staticmethod` for conceptually class-related utilities.

**94. How does Python's `sorted()` work under the hood?**  
Uses Timsort — a hybrid merge sort + insertion sort with O(n log n) worst-case and O(n) best-case (already-sorted data). Stable (preserves relative order of equal elements).

**95. What is the difference between `__eq__` and `__hash__` rules?**  
Objects that compare equal (`==`) MUST have the same `__hash__`. If you define `__eq__`, Python sets `__hash__` to `None` (unhashable) — you must also define `__hash__`. `frozen=True` dataclasses do this correctly.

**96. What is `tracemalloc`?**  
Python's memory allocation tracer: `tracemalloc.start()` → run code → `tracemalloc.get_traced_memory()` returns `(current, peak)` bytes. Used to find memory leaks.

**97. What is `cProfile` vs `line_profiler`?**  
`cProfile` profiles at the function level (total/cumulative time per function). `line_profiler` profiles line-by-line inside a function. Use `cProfile` first to find the slow function, then `line_profiler` to pinpoint the exact line.

**98. What is `__enter__` return value used for?**  
It's the value bound to the `as` variable: `with open("f") as file:`. `file` is the return value of `open().__enter__()`. Returning `None` is valid for context managers used purely for setup/teardown.

**99. How does `import` work with `__init__.py`?**  
A directory with `__init__.py` is a Python package. Importing `mypackage.module` executes `mypackage/__init__.py` first, then `mypackage/module.py`. `__init__.py` can re-export names to provide a public API.

**100. What is PEP 8? Name 5 key conventions.**  
PEP 8 is Python's official style guide. Key rules:
1. 4-space indentation
2. `snake_case` for variables/functions, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
3. Max 79 characters per line
4. Two blank lines between top-level definitions
5. Imports at the top, grouped: stdlib → third-party → local
