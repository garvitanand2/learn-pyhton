# =============================================================
# Day 7: Week 1 Mini Project — CLI-Based AI Model Selector
# Goal: Apply everything from Week 1 (variables, operators,
#       conditionals, loops, functions) in one cohesive project.
#
# Project: "ModelMatcher" — A CLI tool where a user describes
#          their task and the tool recommends the best AI model.
# =============================================================

import time


# ===== DATA LAYER =============================================

# Model registry — describes each model's capabilities
MODEL_REGISTRY = [
    {
        "name":         "gpt-4",
        "provider":     "openai",
        "strengths":    ["reasoning", "coding", "complex", "chat"],
        "max_tokens":   128000,
        "cost_per_1k":  0.03,      # $ per 1000 tokens
        "speed":        "slow",
        "tier":         "premium",
    },
    {
        "name":         "gpt-3.5-turbo",
        "provider":     "openai",
        "strengths":    ["chat", "summarization", "qa", "fast"],
        "max_tokens":   16385,
        "cost_per_1k":  0.001,
        "speed":        "fast",
        "tier":         "standard",
    },
    {
        "name":         "claude-3-opus",
        "provider":     "anthropic",
        "strengths":    ["reasoning", "analysis", "long-context", "complex"],
        "max_tokens":   200000,
        "cost_per_1k":  0.015,
        "speed":        "medium",
        "tier":         "premium",
    },
    {
        "name":         "claude-3-haiku",
        "provider":     "anthropic",
        "strengths":    ["chat", "fast", "summarization", "cheap"],
        "max_tokens":   200000,
        "cost_per_1k":  0.00025,
        "speed":        "fast",
        "tier":         "economy",
    },
    {
        "name":         "llama-3-70b",
        "provider":     "meta",
        "strengths":    ["open-source", "coding", "reasoning", "chat"],
        "max_tokens":   8192,
        "cost_per_1k":  0.0009,
        "speed":        "medium",
        "tier":         "standard",
    },
    {
        "name":         "mistral-7b",
        "provider":     "mistral",
        "strengths":    ["fast", "cheap", "summarization", "open-source"],
        "max_tokens":   32768,
        "cost_per_1k":  0.0002,
        "speed":        "fast",
        "tier":         "economy",
    },
]

VALID_TASKS = [
    "chat", "summarization", "coding", "reasoning",
    "analysis", "qa", "long-context", "fast"
]

TIERS = ["economy", "standard", "premium"]


# ===== CORE FUNCTIONS =========================================

def match_models(task: str, max_cost: float = None, prefer_speed: str = None) -> list:
    """
    Find all models that match the given task and optional filters.

    Args:
        task (str): The AI task to match.
        max_cost (float): Maximum cost per 1000 tokens (optional).
        prefer_speed (str): Preferred speed tier: 'fast', 'medium', 'slow' (optional).

    Returns:
        list: Matching model dicts, sorted by cost ascending.
    """
    matches = []

    for model in MODEL_REGISTRY:
        # Check if model supports the task
        if task not in model["strengths"]:
            continue

        # Apply cost filter
        if max_cost is not None and model["cost_per_1k"] > max_cost:
            continue

        # Apply speed filter
        if prefer_speed is not None and model["speed"] != prefer_speed:
            continue

        matches.append(model)

    # Sort by cost (cheapest first)
    matches.sort(key=lambda m: m["cost_per_1k"])
    return matches


def estimate_cost(model: dict, token_count: int) -> float:
    """Estimate cost for a given token count in USD."""
    return (token_count / 1000) * model["cost_per_1k"]


def display_model_card(model: dict, token_count: int = 1000) -> None:
    """Print a formatted model summary card."""
    sep = "─" * 48
    cost = estimate_cost(model, token_count)

    print(f"\n┌{sep}┐")
    print(f"│  {model['name']:<20}  [{model['tier'].upper()}]         │")
    print(f"├{sep}┤")
    print(f"│  Provider   : {model['provider']:<32}│")
    print(f"│  Speed      : {model['speed']:<32}│")
    print(f"│  Max tokens : {str(model['max_tokens']):<32}│")
    print(f"│  Cost/1k    : ${model['cost_per_1k']:<31.5f}│")
    print(f"│  For {token_count:,} tokens: ${cost:.4f}{'  ':27}│")
    print(f"│  Strengths  : {', '.join(model['strengths']):<32}│")
    print(f"└{sep}┘")


def display_results(models: list, token_count: int) -> None:
    """Display a list of model cards."""
    if not models:
        print("\n  ⚠  No models matched your criteria.")
        print("  Try a different task or relax your filters.\n")
        return

    print(f"\n  Found {len(models)} matching model(s):\n")
    for i, model in enumerate(models, 1):
        print(f"  #{i}", end="")
        display_model_card(model, token_count)


def get_recommendation(models: list) -> dict:
    """Return the single best recommendation (cheapest matching model)."""
    return models[0] if models else None


def validate_task(task: str) -> bool:
    """Check if the task is in the supported list."""
    return task.lower().strip() in VALID_TASKS


def print_banner() -> None:
    """Print the application banner."""
    print("\n" + "═" * 52)
    print("       ModelMatcher — AI Model Selector CLI       ")
    print("       Week 1 Mini Project · Python 30 Days       ")
    print("═" * 52)


def print_task_menu() -> None:
    """Print all available tasks."""
    print("\n  Available tasks:")
    for i, task in enumerate(VALID_TASKS, 1):
        print(f"    {i:2d}. {task}")


# ===== MAIN APPLICATION =======================================

def run_cli():
    """Main CLI loop."""
    print_banner()

    session_history = []   # track queries this session

    while True:
        print("\n" + "─" * 52)
        print("  Commands: [search] [history] [models] [quit]")
        print("─" * 52)

        command = input("\n  > ").strip().lower()

        # ── quit ────────────────────────────────────────────
        if command in ("quit", "q", "exit"):
            print(f"\n  Session ended. You made {len(session_history)} search(es).")
            print("  Keep building. See you on Day 8! 🚀\n")
            break

        # ── list all models ──────────────────────────────────
        elif command == "models":
            print(f"\n  All {len(MODEL_REGISTRY)} registered models:\n")
            for m in MODEL_REGISTRY:
                print(f"  • {m['name']:<25} {m['provider']:<12} ${m['cost_per_1k']:.5f}/1k")

        # ── search ──────────────────────────────────────────
        elif command == "search":
            print_task_menu()

            # --- Task input
            task_input = input("\n  Task (or number): ").strip().lower()
            if task_input.isdigit():
                idx = int(task_input) - 1
                if 0 <= idx < len(VALID_TASKS):
                    task_input = VALID_TASKS[idx]
                else:
                    print("  Invalid number.")
                    continue

            if not validate_task(task_input):
                print(f"  ✗ Unknown task '{task_input}'.")
                print(f"  Valid tasks: {', '.join(VALID_TASKS)}")
                continue

            # --- Token count
            raw_tokens = input("  Estimated token count [default: 1000]: ").strip()
            token_count = int(raw_tokens) if raw_tokens.isdigit() else 1000

            # --- Budget filter
            raw_budget = input("  Max cost per 1k tokens in $ [press Enter to skip]: ").strip()
            max_cost = float(raw_budget) if raw_budget else None

            # --- Speed preference
            raw_speed = input("  Preferred speed (fast/medium/slow) [Enter to skip]: ").strip().lower()
            prefer_speed = raw_speed if raw_speed in ("fast", "medium", "slow") else None

            # --- Search
            print("\n  Searching", end="")
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)

            results = match_models(task_input, max_cost=max_cost, prefer_speed=prefer_speed)

            display_results(results, token_count)

            if results:
                top = get_recommendation(results)
                print(f"\n  ★  TOP RECOMMENDATION: {top['name']} (cheapest match)")

            # Store in session history
            session_history.append({
                "task":        task_input,
                "filters":     {"max_cost": max_cost, "prefer_speed": prefer_speed},
                "results":     len(results),
                "top_pick":    results[0]["name"] if results else None,
            })

        # ── history ─────────────────────────────────────────
        elif command == "history":
            if not session_history:
                print("\n  No searches yet.")
            else:
                print(f"\n  Session history ({len(session_history)} searches):\n")
                for i, h in enumerate(session_history, 1):
                    print(f"  {i}. Task: {h['task']:<20} | Results: {h['results']} | Best: {h['top_pick']}")

        else:
            print(f"  Unknown command: '{command}'. Type 'search', 'models', 'history', or 'quit'.")


# ===== ENTRY POINT ============================================

if __name__ == "__main__":
    run_cli()
