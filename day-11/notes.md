# Day 11 Notes — Strings

## What & Why

Strings are the primary data type in NLP and AI applications.
Every user message, model response, document, label, and prompt template
is a string. Mastering string manipulation = mastering data preparation.

**Key property**: Strings are **immutable** — every operation creates a new string.

---

## Essential Methods Reference

### Case & Normalization
```python
s.lower()        # all lowercase
s.upper()        # ALL UPPERCASE
s.title()        # Title Case Each Word
s.capitalize()   # First letter cap only
s.swapcase()     # InVeRt CaSe
```

### Whitespace
```python
s.strip()        # remove leading/trailing whitespace
s.lstrip()       # left only
s.rstrip()       # right only
s.strip("chars") # strip specific characters
```

### Search
```python
s.find("sub")    # first index, -1 if missing
s.rfind("sub")   # last index
s.index("sub")   # first index, ValueError if missing
s.count("sub")   # number of occurrences
"sub" in s       # boolean — use this for existence checks
s.startswith("prefix")
s.endswith("suffix")
```

### Split & Join
```python
s.split()          # split on any whitespace
s.split(",")       # split on comma
s.split(",", 2)    # max 2 splits
s.splitlines()     # split on \n
" ".join(words)    # join list with space between
```

### Replace
```python
s.replace("old", "new")         # replace all
s.replace("old", "new", count)  # replace first N
```

### Testing
```python
s.isdigit()   s.isalpha()   s.isalnum()
s.isspace()   s.isupper()   s.islower()   s.istitle()
```

---

## f-String Format Specifications

```python
f"{value:.4f}"      # 4 decimal places
f"{value:.2%}"      # percentage (× 100, 2 decimals)
f"{value:,}"        # thousands separator
f"{value:>10}"      # right-align in 10 chars
f"{value:<10}"      # left-align   
f"{value:^10}"      # center
f"{value:010}"      # zero-pad to width 10
f"{value:x}"        # hex  f"{value:b}"  binary  f"{value:e}" scientific
```

---

## Raw Strings

```python
path    = r"C:\Users\alice\data"   # \U \a \d treated literally
pattern = r"\d{4}-\d{2}-\d{2}"    # regex pattern — always use r""
```

Without `r""` prefix, `\n`, `\t`, `\r`, `\b` etc. are escape sequences.

---

## Regular Expressions (Brief Intro)

```python
import re

re.sub(pattern, replacement, text)   # replace matches
re.findall(pattern, text)            # list of all matches
re.match(pattern, text)              # match at start
re.search(pattern, text)             # match anywhere
```

Key patterns:
- `\d` — digit, `\w` — word char, `\s` — whitespace
- `.` — any char, `+` — 1+, `*` — 0+, `?` — 0 or 1
- `[a-z]` — char class, `^` — start, `$` — end
- `{n,m}` — repeat n to m times

---

## Encoding

Python 3 strings are Unicode. When writing to files or sending over network:
```python
text.encode("utf-8")    # str → bytes
data.decode("utf-8")    # bytes → str
```

Most modern systems use UTF-8. Emojis and non-ASCII chars take multiple bytes.

---

## Performance Notes

- String concatenation in a loop is O(n²) — use `"".join(parts)` instead
- `str.split()` returns a list — O(n) to create
- Membership `"x" in s` scans linearly — O(n)
- For repeated search/replace, compile regex patterns: `compiled = re.compile(r"...")`

---

## Real-World Analogy

String methods are like a **text editor's find-and-replace + formatting toolbar**,
but programmable. In NLP preprocessing:
1. `lower()` → normalize case (same word, different spellings)
2. `strip()` + `split()` → tokenize
3. `replace()` / `re.sub()` → clean noise
4. `join()` → reassemble cleaned tokens

Every NLP framework (NLTK, spaCy, Hugging Face) uses these under the hood.

---

## Interview Quick-Fire

1. **Why are strings immutable?** → Immutability makes strings hashable (usable as dict keys), thread-safe, and easier to reason about. Modifications create new strings.

2. **`find()` vs `index()`?** → `find()` returns -1 if not found; `index()` raises `ValueError`. Use `find()` when absence is expected.

3. **How do you efficiently build a large string?** → Collect parts in a list, then `"".join(parts)`. Repeated `+=` is O(n²).

4. **What is a raw string?** → A string prefixed with `r` where backslashes are treated literally. Essential for regex patterns and Windows paths.

5. **What does `"hello".encode()` return?** → A `bytes` object. Default encoding is UTF-8. Used when writing files or making HTTP requests.
