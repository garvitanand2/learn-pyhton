# Day 25 Notes — JSON & APIs

## JSON Overview

JSON (JavaScript Object Notation) is the universal data interchange format.

```
Python      ↔   JSON
dict        ↔   object  {}
list        ↔   array   []
str         ↔   string  ""
int/float   ↔   number
True/False  ↔   true/false
None        ↔   null
```

---

## Core json Functions

```python
import json

# Serialize (Python → JSON)
json.dumps(obj)                   # → str
json.dumps(obj, indent=2)         # → pretty str
json.dumps(obj, sort_keys=True)   # → deterministic
json.dump(obj, file_obj)          # → write to file

# Deserialize (JSON → Python)
json.loads(json_str)              # str → Python
json.load(file_obj)               # file → Python
```

---

## Custom JSON Encoding

```python
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()   # → "2024-01-15T14:32:01"
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)  # raises TypeError for unknowns

json.dumps(data, cls=CustomEncoder)
```

---

## REST API Concepts

| Concept | Meaning |
|---------|---------|
| **URL** | Resource location: `https://api.example.com/v1/predict` |
| **Method** | `GET` (read), `POST` (create), `PUT/PATCH` (update), `DELETE` (delete) |
| **Headers** | Metadata: `Authorization`, `Content-Type`, `Accept` |
| **Body** | Request data (JSON for POST/PUT) |
| **Status Code** | 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 429 Rate Limited, 500 Server Error |

---

## Using `requests` Library (Install Required)

```bash
pip install requests
```

```python
import requests

# GET
response = requests.get(
    "https://api.example.com/models",
    headers={"Authorization": "Bearer my-api-key"},
    params={"limit": 10},       # → ?limit=10
    timeout=30,
)
response.raise_for_status()     # raises for 4xx/5xx
data = response.json()          # parse JSON body

# POST
response = requests.post(
    "https://api.example.com/classify",
    headers={"Authorization": "Bearer my-api-key"},
    json={"text": "hello", "labels": ["pos", "neg"]},  # auto-sets Content-Type
    timeout=30,
)
```

---

## Standard Library: urllib

No install needed:

```python
import urllib.request, json

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read())
```

---

## Error Handling Pattern for API Calls

```python
import requests
from requests.exceptions import (
    Timeout, ConnectionError, HTTPError, RequestException
)

def call_api(url, payload, api_key, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30,
            )
            resp.raise_for_status()    # raises HTTPError for 4xx/5xx
            return resp.json()
        
        except Timeout:
            print(f"Attempt {attempt+1}: Timeout")
        except ConnectionError:
            print(f"Attempt {attempt+1}: Network error")
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                time.sleep(2 ** attempt)       # Exponential backoff
            elif 400 <= e.response.status_code < 500:
                raise  # Client error — don't retry
            else:
                print(f"Server error: {e}")    # 5xx — retry
        except RequestException as e:
            raise  # Unknown error — don't retry
    
    raise RuntimeError(f"Failed after {retries} attempts")
```

---

## OpenAI-Style Client Pattern

```python
class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })
    
    def chat(self, messages, model="gpt-4", **kwargs) -> str:
        resp = self._session.post(
            "https://api.openai.com/v1/chat/completions",
            json={"model": model, "messages": messages, **kwargs},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
```

---

## JSONL Format (Large Datasets)

```python
# Write JSONL
with open("data.jsonl", "w") as f:
    for record in records:
        f.write(json.dumps(record) + "\n")

# Read JSONL lazily
def load_jsonl(path):
    with open(path) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)
```

Standard for: HuggingFace datasets, OpenAI fine-tuning format, The Pile.

---

## Quick-Fire Interview Questions

1. **What's the difference between `json.dump()` and `json.dumps()`?**  
   `dump()` writes to a file object; `dumps()` returns a string.

2. **How do you handle non-serializable types with `json`?**  
   Subclass `json.JSONEncoder` and override `default()`.

3. **What HTTP status code means "rate limited"?**  
   429 Too Many Requests.

4. **What does `response.raise_for_status()` do?**  
   Raises `HTTPError` for 4xx and 5xx status codes; does nothing for 2xx.

5. **What is JSONL format?**  
   JSON Lines — one valid JSON object per line. Used for large datasets because a single line can be read/processed without loading the whole file.
