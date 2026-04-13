# =============================================================
# Day 11: Strings — NLP Thinking
# Goal: Strings are the most common data type in AI applications.
#       Every prompt, label, document, and response is a string.
#       Master string manipulation to master NLP preprocessing.
# =============================================================

# --- 1. STRING BASICS -----------------------------------------
# What: Immutable sequence of Unicode characters
# Why:  Prompts, labels, tokens, documents — ALL strings

text = "Large Language Models are transforming the AI industry."

print(f"Length       : {len(text)}")
print(f"First char   : {text[0]}")
print(f"Last char    : {text[-1]}")
print(f"Slice [6:14] : {text[6:14]}")
print(f"Reversed     : {text[::-1][:20]}...")

# Strings are immutable — no in-place modification
# text[0] = "l"   ← TypeError!

# --- 2. CASE METHODS ------------------------------------------
sample = "  Hello, World! This is AI.  "

print(f"\nOriginal    : '{sample}'")
print(f"lower()     : '{sample.lower()}'")
print(f"upper()     : '{sample.upper()}'")
print(f"title()     : '{sample.title()}'")
print(f"capitalize(): '{sample.strip().capitalize()}'")
print(f"swapcase()  : '{sample.swapcase()}'")

# --- 3. STRIPPING WHITESPACE ----------------------------------
padded = "   \t  trimme this  \n  "
print(f"\nstrip()  : '{padded.strip()}'")
print(f"lstrip() : '{padded.lstrip()}'")
print(f"rstrip() : '{padded.rstrip()}'")

# --- 4. FINDING AND SEARCHING --------------------------------

sentence = "the model predicted the wrong label but the confidence was high"

print(f"\nfind('model')  : {sentence.find('model')}")        # index of first occurrence
print(f"find('xyz')    : {sentence.find('xyz')}")           # -1 if not found
print(f"rfind('the')   : {sentence.rfind('the')}")          # last occurrence
print(f"count('the')   : {sentence.count('the')}")          # number of occurrences
print(f"startswith('the'): {sentence.startswith('the')}")
print(f"endswith('high'): {sentence.endswith('high')}")
print(f"'model' in s   : {'model' in sentence}")

# --- 5. SPLIT AND JOIN ----------------------------------------

# Split on whitespace (default)
tokens = sentence.split()
print(f"\nTokens (split): {tokens[:5]}...")
print(f"Token count   : {len(tokens)}")

# Split on specific delimiter
csv_row = "alice,engineer,openai,92.5"
fields  = csv_row.split(",")
print(f"\nCSV fields: {fields}")

# Split with limit
first_two = csv_row.split(",", maxsplit=2)
print(f"maxsplit=2: {first_two}")

# Join — opposite of split
words = ["Large", "Language", "Models"]
joined = " ".join(words)
print(f"\nJoined     : {joined}")

path_parts = ["data", "processed", "train.csv"]
path = "/".join(path_parts)
print(f"File path  : {path}")

# Rebuild a sentence after preprocessing
clean_tokens = [t for t in tokens if t not in {"the", "was", "but"}]
clean_sentence = " ".join(clean_tokens)
print(f"No stop words: {clean_sentence}")

# --- 6. REPLACING AND CLEANING --------------------------------
template = "Hello {{name}}, your {{task}} request was received by {{model}}."

# replace
result = template.replace("{{name}}", "Alice")
result = result.replace("{{task}}", "summarization")
result = result.replace("{{model}}", "GPT-4")
print(f"\nFilled template: {result}")

# strip specific chars
messy = "###  Important text  ###"
clean = messy.strip("#").strip()
print(f"Stripped: '{clean}'")

# --- 7. STRING FORMATTING ------------------------------------

name        = "GPT-4"
accuracy    = 0.9712
latency_ms  = 1234

# f-string (preferred)
print(f"\n{name}: accuracy={accuracy:.2%}, latency={latency_ms}ms")

# Format spec options
print(f"{'Left':<20}|{'Center':^20}|{'Right':>20}")
print(f"{3.14159:.4f}")     # 4 decimal places
print(f"{1234567:,}")       # thousands separator → 1,234,567
print(f"{0.9712:.1%}")      # percentage → 97.1%
print(f"{255:08b}")         # binary with 8 digits → 11111111
print(f"{255:x}")           # hex → ff

# --- 8. MULTI-LINE STRINGS & RAW STRINGS ----------------------

# Multi-line (preserve newlines)
system_prompt = """You are a helpful AI assistant.
You answer questions concisely and accurately.
You do not make up information."""

print(f"\nPrompt lines: {len(system_prompt.splitlines())}")

# Raw string — backslash is literal (use for regex patterns, file paths on Windows)
pattern    = r"\d{4}-\d{2}-\d{2}"    # date pattern
windows_path = r"C:\Users\alice\data"
print(f"Regex   : {pattern}")
print(f"Win path: {windows_path}")

# --- 9. STRING TESTING METHODS --------------------------------
tests = [
    ("is_digit",  "123",      str.isdigit),
    ("is_alpha",  "hello",    str.isalpha),
    ("is_alnum",  "hello123", str.isalnum),
    ("is_space",  "   ",      str.isspace),
    ("is_upper",  "GPT",      str.isupper),
    ("is_lower",  "bert",     str.islower),
    ("is_title",  "Title Case", str.istitle),
]

print("\nString tests:")
for name, value, fn in tests:
    print(f"  {name}({value!r:15}) = {fn(value)}")

# --- 10. PRACTICAL EXAMPLE: Text Preprocessing Pipeline ------
import re   # regular expressions — the power tool for strings

def preprocess_text(text: str) -> str:
    """
    Production-grade text preprocessing for NLP tasks.
    Steps: lowercase → remove HTML → remove URLs → normalize whitespace
           → remove special chars → strip
    """
    text = text.lower()                              # lowercase
    text = re.sub(r"<[^>]+>", " ", text)            # remove HTML tags
    text = re.sub(r"http\S+|www\S+", " ", text)     # remove URLs
    text = re.sub(r"[^a-z0-9\s.,!?'-]", " ", text) # keep only useful chars
    text = re.sub(r"\s+", " ", text)                 # collapse whitespace
    text = text.strip()
    return text

raw_texts = [
    "  <p>Hello <b>World</b>!</p>  ",
    "Check out https://example.com for more info!!!",
    "GPT-4 achieves 97.1% accuracy on MMLU. Great!!!",
]

print("\nPreprocessed texts:")
for raw in raw_texts:
    clean = preprocess_text(raw)
    print(f"  Raw  : {raw[:60]}")
    print(f"  Clean: {clean}")
    print()

# --- 11. STRING ENCODING (important for file/API work) -------
text_unicode = "AI is transforming the world 🌍"
encoded      = text_unicode.encode("utf-8")
decoded      = encoded.decode("utf-8")

print(f"Unicode  : {text_unicode}")
print(f"UTF-8 len: {len(encoded)} bytes  (vs {len(text_unicode)} chars)")
print(f"Decoded  : {decoded}")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 11 Complete ---")
print("Strings: the universal language of AI. Preprocessing IS engineering.")
