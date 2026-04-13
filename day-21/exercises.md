# Day 21 Exercises — TextFlow Pipeline Extensions

Estimated time: 60–90 minutes

---

## Exercise 1 — Deduplication Step

Add a `Deduplicator(PipelineStep)` that:
1. Keeps a set of seen normalized texts (lowercased, stripped)
2. Returns `None` for records that are exact duplicates or very similar  
   (two records are "similar" if their token sets overlap ≥ 80%)
3. Add `stats` property that returns `{"total_seen": N, "duplicates_dropped": M}`

Insert it after `TextCleaner` in the pipeline.

---

## Exercise 2 — Language Detector Step

Add a `LanguageFilter(PipelineStep)` that:
1. Detects if text is "english" using a simple heuristic: the most common English words  
   (`["the", "a", "is", "in", "it", "of", "and", "to", "for"]`) must represent ≥ 10% of tokens
2. Returns `None` (drops) records that appear to be non-English
3. Logs which record IDs were dropped

---

## Exercise 3 — Configurable Pipeline from JSON

Create a `pipeline_from_config(config_path: str)` factory function:

Config file format:
```json
{
  "name": "MyPipeline",
  "steps": [
    {"type": "TextCleaner", "lowercase": true, "remove_urls": true},
    {"type": "Tokenizer", "min_length": 2},
    {"type": "LengthFilter", "min_tokens": 3, "max_tokens": 100},
    {"type": "FeatureExtractor"},
    {"type": "SentimentLabeler"}
  ]
}
```

The function should:
1. Read the config file
2. Instantiate each step by name with the given kwargs  
   (use a registry dict: `{"TextCleaner": TextCleaner, ...}`)
3. Build and return the pipeline

---

## Exercise 4 — Pipeline Metrics + Reporting

Extend `Pipeline.run()` to collect timing metrics:

For each step, record:
- Total time spent
- Number of records processed
- Number of records dropped

Add a `detailed_stats()` method that returns:
```python
{
  "TextCleaner": {"processed": 20, "dropped": 0, "time_ms": 1.2},
  "LengthFilter": {"processed": 18, "dropped": 3, "time_ms": 0.4},
  ...
}
```

And update `print_report()` to show a per-step timing table.

---

## Exercise 5 — Save and Reload Results

Extend the project with round-trip serialization:

1. Save all `Record` objects to `outputs/results.jsonl`
2. Write `load_results(path) → list[Record]` that reads the JSONL and reconstructs `Record` objects
3. Write `get_records_by_label(records, label)` that returns filtered records
4. Write `export_csv(records, path)` that saves `id, text, label, num_tokens, unique_ratio` as CSV

---

## Stretch Challenge — Config-Driven Dynamic Steps

Add a `ConditionalStep(PipelineStep)` that:
1. Takes a predicate function and a step
2. Only applies the step if the predicate returns True for the record
3. Otherwise passes the record through unchanged

```python
ConditionalStep(
    predicate=lambda r: r.features.get("num_tokens", 0) > 10,
    step=FeatureExtractor()
)
```

Then extend the JSON config system to support conditional steps:
```json
{"type": "ConditionalStep", "condition": "long_text", "step": {...}}
```

Where `"long_text"` maps to a predefined predicate in a predicates registry.
