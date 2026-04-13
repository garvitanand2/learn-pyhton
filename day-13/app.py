# =============================================================
# Day 13: Nested Data Structures
# Goal: Navigate and transform deeply nested data.
#       JSON API responses, model configs, knowledge graphs,
#       and conversation histories are all nested structures.
# =============================================================

import json
import copy

# --- 1. NESTED LISTS (Matrices / 2D Grids) -------------------

# A confusion matrix — 4-class classifier
confusion_matrix = [
    [50,  2,  1,  0],   # true: class 0 — predicted as [0,1,2,3]
    [ 3, 48,  2,  1],   # true: class 1
    [ 1,  2, 49,  0],   # true: class 2
    [ 0,  1,  1, 52],   # true: class 3
]

print("Confusion Matrix:")
class_names = ["cat", "dog", "bird", "fish"]
header = f"{'':8}" + "".join(f"{n:>7}" for n in class_names)
print(header)
for label, row in zip(class_names, confusion_matrix):
    row_str = "".join(f"{v:>7}" for v in row)
    print(f"  {label:<6}{row_str}")

# Compute per-class accuracy (diagonal / row sum)
print("\nPer-class accuracy:")
for i, (label, row) in enumerate(zip(class_names, confusion_matrix)):
    acc = confusion_matrix[i][i] / sum(row)
    print(f"  {label}: {acc:.2%}")

# --- 2. NESTED DICTS (Config Trees) --------------------------

model_suite = {
    "gpt-4": {
        "provider": "openai",
        "capabilities": ["reasoning", "coding", "chat"],
        "limits": {
            "max_tokens":    128000,
            "requests_per_min": 10000,
        },
        "pricing": {
            "input":  0.03,
            "output": 0.06,
        }
    },
    "claude-3-opus": {
        "provider": "anthropic",
        "capabilities": ["reasoning", "analysis", "long-context"],
        "limits": {
            "max_tokens":    200000,
            "requests_per_min": 5000,
        },
        "pricing": {
            "input":  0.015,
            "output": 0.075,
        }
    }
}

# Deep access
gpt4_max     = model_suite["gpt-4"]["limits"]["max_tokens"]
claude_price = model_suite["claude-3-opus"]["pricing"]["output"]
print(f"\nGPT-4 max tokens: {gpt4_max:,}")
print(f"Claude output price: ${claude_price}/1k tokens")

# Safe deep access with .get() chain
def deep_get(d: dict, *keys, default=None):
    """Safely access nested dict keys."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

rpm = deep_get(model_suite, "gpt-4", "limits", "requests_per_min")
missing = deep_get(model_suite, "gpt-4", "limits", "nonexistent", default=0)
print(f"GPT-4 RPM: {rpm}")
print(f"Missing key: {missing}")

# --- 3. LIST OF DICTS (Dataset Records) ----------------------
# The most common structure in ML: a dataset as a list of records

dataset = [
    {"id": 1, "text": "The movie was great!",       "label": "positive", "confidence": 0.95},
    {"id": 2, "text": "Absolutely terrible film.",   "label": "negative", "confidence": 0.92},
    {"id": 3, "text": "It was okay, nothing special.", "label": "neutral",  "confidence": 0.71},
    {"id": 4, "text": "Best movie of the year!",     "label": "positive", "confidence": 0.98},
    {"id": 5, "text": "Waste of two hours.",         "label": "negative", "confidence": 0.87},
]

# Filter: only high-confidence records
high_conf = [r for r in dataset if r["confidence"] >= 0.90]
print(f"\nHigh confidence records: {len(high_conf)}")

# Sort by confidence descending
sorted_data = sorted(dataset, key=lambda r: r["confidence"], reverse=True)
print("Sorted by confidence:")
for r in sorted_data:
    print(f"  [{r['label']:8}] conf={r['confidence']:.2f} | {r['text'][:40]}")

# Group by label
from collections import defaultdict
by_label = defaultdict(list)
for record in dataset:
    by_label[record["label"]].append(record)

print(f"\nClass distribution:")
for label, records in by_label.items():
    print(f"  {label}: {len(records)} samples")

# --- 4. NESTED JSON (API Response Structure) -----------------

api_response = {
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "model": "gpt-4",
    "usage": {
        "prompt_tokens":     150,
        "completion_tokens": 380,
        "total_tokens":      530
    },
    "choices": [
        {
            "index": 0,
            "message": {
                "role":    "assistant",
                "content": "Python is a versatile, readable language..."
            },
            "finish_reason": "stop"
        }
    ]
}

# Extracting values from a real API response
content       = api_response["choices"][0]["message"]["content"]
total_tokens  = api_response["usage"]["total_tokens"]
model_used    = api_response["model"]

print(f"\nModel    : {model_used}")
print(f"Tokens   : {total_tokens}")
print(f"Response : {content[:60]}...")

# Serialize / deserialize
json_str        = json.dumps(api_response, indent=2)
reconstructed   = json.loads(json_str)
print(f"\nJSON roundtrip OK: {reconstructed == api_response}")

# --- 5. CONVERSATION HISTORY (List of Dicts) -----------------

conversation = [
    {"role": "system",    "content": "You are a helpful AI tutor."},
    {"role": "user",      "content": "What is a transformer model?"},
    {"role": "assistant", "content": "A transformer is a neural network..."},
    {"role": "user",      "content": "How does attention work?"},
    {"role": "assistant", "content": "Attention allows the model to..."},
]

# Count messages by role
from collections import Counter
role_counts = Counter(msg["role"] for msg in conversation)
print(f"\nConversation stats: {dict(role_counts)}")

# Get last N messages for context window
def get_context(history: list, n: int) -> list:
    """Return last n messages, always including the system prompt."""
    system_msg = [m for m in history if m["role"] == "system"]
    recent     = [m for m in history if m["role"] != "system"][-n:]
    return system_msg + recent

context = get_context(conversation, n=2)
print(f"\nContext (last 2 non-system): {len(context)} messages")
for m in context:
    print(f"  [{m['role']:9}] {m['content'][:50]}")

# --- 6. DEEP COPY WARNING ------------------------------------

original_data = {"samples": [{"x": 1}, {"x": 2}]}

# Shallow copy fails for nested structures
shallow = original_data.copy()
shallow["samples"][0]["x"] = 99   # modifies ORIGINAL too!
print(f"\nAfter shallow copy mutation: original samples[0]['x'] = {original_data['samples'][0]['x']}")

# Deep copy is safe
original_data["samples"][0]["x"] = 1   # restore
deep = copy.deepcopy(original_data)
deep["samples"][0]["x"] = 99           # does NOT affect original
print(f"After deep copy mutation  : original samples[0]['x'] = {original_data['samples'][0]['x']}")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 13 Complete ---")
print("Nested structures = the universal format of AI data. Navigate them confidently.")
