# Day 13 Exercises — Nested Data Structures

Estimated time: 30–40 minutes

---

## Exercise 1 — API Response Parser

Parse this mock LLM API response and extract all meaningful fields:

```python
response = {
    "id": "chatcmpl-xyz789",
    "model": "gpt-4-turbo",
    "usage": {
        "prompt_tokens": 245,
        "completion_tokens": 512,
        "total_tokens": 757
    },
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "Transformers use self-attention..."},
            "finish_reason": "stop"
        }
    ],
    "metadata": {
        "latency_ms": 1243,
        "region": "us-east-1"
    }
}
```

Write a function `parse_response(response)` that returns:
```python
{
    "content": "...",
    "tokens_used": 757,
    "cost_usd": 0.0227,   # assume $0.03/1k tokens
    "latency_ms": 1243,
    "finish_reason": "stop"
}
```

---

## Exercise 2 — Conversation Manager

Build a `ConversationManager` class (just using dicts and lists, no OOP required):

Functions:
1. `create_conversation(system_prompt)` → returns initial conversation dict
2. `add_message(conversation, role, content)` → appends message
3. `get_context(conversation, max_messages=10)` → returns last N messages (always include system)
4. `get_stats(conversation)` → returns `{total_messages, user_turns, assistant_turns, total_chars}`

Test with a multi-turn conversation of your choice.

---

## Exercise 3 — Deep Diff

Write `dict_diff(d1, d2)` that returns what changed between two nested dicts:

```python
config_v1 = {
    "model": "gpt-3.5-turbo",
    "settings": {"temperature": 0.7, "max_tokens": 512},
    "tags": ["stable", "prod"]
}

config_v2 = {
    "model": "gpt-4",
    "settings": {"temperature": 0.2, "max_tokens": 2048, "stream": True},
    "version": "2.0"
}

diff = dict_diff(config_v1, config_v2)
# {
#     "changed": {"model": ("gpt-3.5-turbo", "gpt-4"), "settings.temperature": (0.7, 0.2), ...}
#     "added":   {"version": "2.0", "settings.stream": True},
#     "removed": {"tags": ["stable", "prod"]}
# }
```

---

## Exercise 4 — Dataset Aggregator

Given a list of training run records, compute aggregated stats per model:

```python
runs = [
    {"model": "gpt-4",   "epoch": 1, "loss": 0.92, "accuracy": 0.61},
    {"model": "gpt-4",   "epoch": 2, "loss": 0.71, "accuracy": 0.78},
    {"model": "gpt-4",   "epoch": 3, "loss": 0.52, "accuracy": 0.88},
    {"model": "bert",    "epoch": 1, "loss": 0.85, "accuracy": 0.65},
    {"model": "bert",    "epoch": 2, "loss": 0.60, "accuracy": 0.81},
    {"model": "llama-3", "epoch": 1, "loss": 0.78, "accuracy": 0.72},
    {"model": "llama-3", "epoch": 2, "loss": 0.55, "accuracy": 0.85},
    {"model": "llama-3", "epoch": 3, "loss": 0.40, "accuracy": 0.91},
]
```

Output:
```
Model    | Best Loss | Best Acc | Runs
---------|-----------|----------|-----
gpt-4    |   0.5200  |  88.00%  |  3
bert     |   0.6000  |  81.00%  |  2
llama-3  |   0.4000  |  91.00%  |  3
```

---

## Exercise 5 — JSON Schema Validator

Write a function `validate_schema(data, schema)` where schema is a dict
describing the expected types:

```python
schema = {
    "name":  str,
    "score": float,
    "tags":  list,
    "meta":  {
        "model": str,
        "version": int
    }
}

sample = {"name": "test", "score": 0.92, "tags": ["a", "b"], "meta": {"model": "gpt-4", "version": 2}}
print(validate_schema(sample, schema))   # True

bad = {"name": 123, "score": "high", "tags": [], "meta": {"model": "gpt-4", "version": "2"}}
print(validate_schema(bad, schema))   # False — print which fields fail
```

---

## Stretch Challenge — Knowledge Graph (Nested Dict)

Represent a knowledge graph as a nested dict:
```python
graph = {
    "transformer": {
        "is_a": "neural_network",
        "invented_by": "vaswani_et_al",
        "uses": ["self_attention", "feed_forward", "layer_norm"],
        "variants": {
            "gpt": {"type": "decoder_only"},
            "bert": {"type": "encoder_only"},
            "t5": {"type": "encoder_decoder"}
        }
    }
}
```

1. Write `find_paths(graph, target)` — find all paths to a given value
2. Write `get_all_leaves(graph)` — return all leaf values recursively
3. Write `flatten_graph(graph)` — dot-notation keys as before
