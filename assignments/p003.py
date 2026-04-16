# Exercise 3 — Token Budget Calculator
# An LLM has a context window of 4096 tokens.

# System prompt uses 150 tokens
# User message uses 320 tokens
# Model response is allowed the rest
# Calculate and print:

# Tokens used so far (system + user)
# Tokens remaining for the response
# Percentage of context window used (as a float, rounded to 2 decimal places)
# Whether the conversation is under 50% context usage (bool)

context_window = 4096
system_tokens = 150
user_tokens = 320
model_response_tokens = context_window - (system_tokens + user_tokens)

print(f"Tokens used so far: {system_tokens + user_tokens}")
print(f"Tokens remaining for the response: {model_response_tokens}")
print(f"Percentage of context window used: {((system_tokens + user_tokens) / context_window) * 100:.2f}%")
print(f"Whether the conversation is under 50% context usage: {(system_tokens + user_tokens) < (context_window * 0.5)}")