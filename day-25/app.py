# Day 25: Working with JSON & APIs
# Focus: The data exchange layer of every AI application

# ============================================================
# WHAT: JSON is the universal data format. APIs are how
#       services communicate. Every AI product calls an API.
# WHY:  To build/use AI products you need to: serialize data
#       to JSON, call REST APIs, parse responses, handle
#       errors. This is the glue between your code and the world.
# ============================================================

import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime

# ============================================================
# 1. JSON Deep Dive
# ============================================================
print("=== 1. JSON Deep Dive ===")

# Complex nested data structure (simulating an API response)
api_response = {
    "status": "success",
    "request_id": "req_abc123",
    "model": "text-classifier-v2",
    "usage": {
        "prompt_tokens": 12,
        "completion_tokens": 3,
        "total_tokens": 15,
    },
    "predictions": [
        {"id": 1, "text": "great model", "label": "positive", "score": 0.934},
        {"id": 2, "text": "bad results", "label": "negative", "score": 0.891},
        {"id": 3, "text": "average run", "label": "neutral",  "score": 0.712},
    ],
    "metadata": {
        "latency_ms": 42.3,
        "timestamp": "2024-01-15T14:32:01Z",
        "version": "2.1.0",
    }
}

# Serialize to JSON string
json_str = json.dumps(api_response, indent=2)
print(f"JSON (first 100 chars): {json_str[:100]}...")
print(f"Total length: {len(json_str)} chars")

# Parse back
parsed = json.loads(json_str)
print(f"\nStatus: {parsed['status']}")
print(f"Total tokens: {parsed['usage']['total_tokens']}")
print(f"First prediction: {parsed['predictions'][0]}")

# Accessing nested data safely
def safe_get(data: dict, *keys, default=None):
    """Safely traverse nested dict with multiple keys."""
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data

latency = safe_get(parsed, "metadata", "latency_ms")
missing = safe_get(parsed, "metadata", "model_version", "sha", default="unknown")
print(f"\nLatency: {latency}ms")
print(f"Missing path: {missing}")

# ============================================================
# 2. JSON Serialization Edge Cases
# ============================================================
print("\n=== 2. Serialization Details ===")

# Custom encoder for non-serializable types
class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return sorted(list(obj))  # sorted for deterministic output
        if hasattr(obj, "__dict__"):  # any object with attributes
            return obj.__dict__
        return super().default(obj)

data_with_custom_types = {
    "timestamp": datetime.now(),
    "vocab_set": {"the", "cat", "sat"},
    "score": 0.94,
}

encoded = json.dumps(data_with_custom_types, cls=ModelEncoder, indent=2)
print(encoded)

# sort_keys=True for deterministic output (useful for caching/hashing)
config = {"z_param": 1, "a_param": 2, "m_param": 3}
print(json.dumps(config, sort_keys=True))  # always same order

# ============================================================
# 3. Making HTTP Requests with urllib (Standard Library)
# ============================================================
print("\n=== 3. HTTP Requests (urllib) ===")

def http_get(url: str, headers: dict | None = None) -> dict:
    """Simple GET request returning parsed JSON."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

def http_post(url: str, payload: dict, headers: dict | None = None) -> dict:
    """Simple POST request with JSON body."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "body": e.read().decode()}
    except Exception as e:
        return {"error": str(e)}

# Test with a real public API (JSONPlaceholder)
print("Fetching public API (JSONPlaceholder)...")
result = http_get("https://jsonplaceholder.typicode.com/todos/1")
print(f"  Response: {result}")

# ============================================================
# 4. Simulating an AI API Client
# ============================================================
print("\n=== 4. AI API Client Pattern ===")

class AIAPIClient:
    """Simulates calling an AI inference API.
    
    Pattern used by: OpenAI client, Anthropic client, 
    HuggingFace Inference API clients.
    """

    BASE_URL = "https://api.example.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        if not api_key:
            raise ValueError("API key is required")
        self._api_key = api_key
        self.timeout = timeout
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self._request_count = 0

    def classify(self, text: str, labels: list[str]) -> dict:
        """POST /classify endpoint."""
        self._request_count += 1
        payload = {"text": text, "candidate_labels": labels}

        # Simulate successful response
        return self._simulate_response("classify", payload)

    def embed(self, texts: list[str]) -> dict:
        """POST /embed endpoint."""
        self._request_count += 1
        payload = {"inputs": texts}
        return self._simulate_response("embed", payload)

    def _simulate_response(self, endpoint: str, payload: dict) -> dict:
        """Simulate what an API would return."""
        import random
        random.seed(len(str(payload)))
        return {
            "request_id": f"req_{self._request_count:04d}",
            "endpoint": endpoint,
            "status": "success",
            "usage": {"input_tokens": sum(len(str(v)) for v in payload.values()) // 4},
            "result": f"<simulated response for {endpoint}>",
        }

    def health_check(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"AIAPIClient(requests_made={self._request_count})"

# Usage
client = AIAPIClient(api_key="sk-demo-key-12345")
print(repr(client))

result = client.classify(
    text="The model performance exceeded all benchmarks",
    labels=["positive", "negative", "neutral"]
)
print(f"\nClassify result: {json.dumps(result, indent=2)}")

embed_result = client.embed(["Hello world", "Deep learning"])
print(f"\nEmbed result: {json.dumps(embed_result, indent=2)}")
print(repr(client))

# ============================================================
# 5. Reading & Writing JSON Files (Patterns)
# ============================================================
print("\n=== 5. Config & Results Patterns ===")

def load_config(path: str, required_keys: list[str] | None = None) -> dict:
    """Load and validate a JSON config file."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with open(file_path) as f:
        config = json.load(f)

    if required_keys:
        missing = [k for k in required_keys if k not in config]
        if missing:
            raise ValueError(f"Config missing keys: {missing}")

    return config

def save_results(results: list[dict], output_path: str) -> str:
    """Save results as JSONL (one record per line)."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    return str(path)

# Demo
sample_results = [
    {"id": i, "text": f"sample {i}", "label": "positive", "score": 0.9 - i * 0.05}
    for i in range(5)
]
out = save_results(sample_results, "outputs/day25_results.jsonl")
print(f"Saved {len(sample_results)} results to: {out}")

print("\nDay 25 complete! JSON + APIs = the connective tissue of AI applications.")
