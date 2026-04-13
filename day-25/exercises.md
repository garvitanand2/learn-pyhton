# Day 25 Exercises — JSON & APIs

Estimated time: 45–60 minutes

---

## Exercise 1 — Deep Nested JSON Navigator

Write a `JSONPath` class that navigates nested JSON using dot notation:

```python
nav = JSONPath(api_response)

nav.get("status")                          # "success"
nav.get("usage.total_tokens")              # 15
nav.get("predictions.0.label")             # "positive"
nav.get("metadata.missing_key", "default") # "default"
nav.set("metadata.version", "2.2.0")       # updates nested value
nav.keys("predictions.0")                  # ["id", "text", "label", "score"]
```

---

## Exercise 2 — JSONPlaceholder API Explorer

Using Python's built-in `urllib`, write functions to interact with `https://jsonplaceholder.typicode.com`:

1. `get_user(user_id: int) -> dict` — GET `/users/{id}`
2. `get_user_posts(user_id: int) -> list[dict]` — GET `/posts?userId={id}`
3. `get_post_comments(post_id: int) -> list[dict]` — GET `/comments?postId={id}`

Then write `user_profile(user_id)` that returns:
```python
{
    "user": {...},
    "post_count": N,
    "total_comments": M,
    "posts": [{"id": ..., "title": ..., "comment_count": K}, ...]
}
```

---

## Exercise 3 — Custom JSON Encoder/Decoder

Write `ModelResultEncoder(json.JSONEncoder)` that handles:
- `datetime` objects → ISO string
- `set` objects → sorted list
- `float` values → rounded to 4 decimal places
- Any object with `.to_dict()` method → call it

And `model_result_decoder(d: dict)` (used as `object_hook`) that:
- Converts any string with "T" matching ISO datetime format back to `datetime`

Test round-trip serialization.

---

## Exercise 4 — AI API Client with Rate Limiting

Extend the `AIAPIClient` from the lesson:

1. Add `max_requests_per_minute=60` to `__init__`
2. Track request timestamps in a `deque(maxlen=60)`
3. Before each request, if the oldest request in the queue is within 60 seconds and the queue is full → sleep until it's not
4. Add `usage_stats()` → `{"total_requests": N, "avg_latency_ms": X, "errors": M}`
5. Add `batch_classify(texts: list[str], labels: list[str]) -> list[dict]` that calls `classify()` for each text and returns collected results

---

## Exercise 5 — Config Validator

Build a `ConfigValidator` class:

```python
schema = {
    "model_name": {"type": str, "required": True},
    "learning_rate": {"type": float, "required": True, "min": 1e-6, "max": 0.1},
    "batch_size": {"type": int, "required": True, "min": 1, "max": 2048},
    "output_dir": {"type": str, "required": False, "default": "./outputs"},
    "labels": {"type": list, "required": True, "min_len": 2},
}

validator = ConfigValidator(schema)
config = validator.validate({"model_name": "bert", "learning_rate": 3e-5, ...})
# Returns config with defaults filled in, or raises with clear error message
```

---

## Stretch Challenge — Mock API Server Simulator

Build a `MockAPIServer` class that simulates an AI API for offline testing:

```python
server = MockAPIServer()
server.register_endpoint(
    "POST /classify",
    handler=lambda payload: {
        "label": "positive" if "good" in payload["text"] else "negative",
        "score": 0.9,
    }
)
server.register_endpoint(
    "GET /models",
    handler=lambda payload: {"models": ["bert", "gpt2", "t5"]}
)

# Usage
response = server.call("POST /classify", {"text": "good model performance"})
```

Add response latency simulation, error injection (configurable failure rate), and request logging.
