# Exercise 1 — Model Confidence Router
# Given a confidence score, classify the model's output into one of four tiers:

# Range	Tier	Action
# >= 0.95	"CERTAIN"	Auto-approve and publish
# 0.80 – 0.94	"CONFIDENT"	Approve with logging
# 0.60 – 0.79	"UNCERTAIN"	Flag for human review
# < 0.60	"UNCONFIDENT"	Reject and request re-inference
# Test with scores: 0.97, 0.82, 0.65, 0.42
# //  [0.97, 0.82, 0.65, 0.42]
confidence_scores = [0.97, 0.82, 0.65, 0.42]
for score in confidence_scores:
    if score >= 0.95:
        print(f"Score: {score} - CERTAIN: Auto-approve and publish")
    elif 0.80 <= score < 0.95:
        print(f"Score: {score} - CONFIDENT: Approve with logging")
    elif 0.60 <= score < 0.80:
        print(f"Score: {score} - UNCERTAIN: Flag for human review")
    else:
        print(f"Score: {score} - UNCONFIDENT: Reject and request re-inference")


# Exercise 2 — Token Budget Guard
# Write a function check_token_budget(prompt_tokens, max_tokens) that:

# Raises a printed warning if prompt_tokens uses more than 80% of the budget
# Raises a printed error if prompt_tokens >= max_tokens
# Returns "OK" if within safe limits
# Use guard-clause style (early checks at the top, happy path at the end).

# Test with:

# check_token_budget(3400, 4096) → warning
# check_token_budget(4096, 4096) → error
# check_token_budget(1000, 4096) → OK

def  check_token_budget(prompt_tokens, max_tokens):
    if prompt_tokens >= max_tokens:
        print(f"ERROR: Token budget exceeded! {prompt_tokens} tokens used, but the maximum is {max_tokens}.")
        return
    if prompt_tokens > 0.8 * max_tokens:
        print(f"WARNING: Token budget is nearly exceeded! {prompt_tokens} tokens used, but the maximum is {max_tokens}.")
    print(f"Token budget is within safe limits.")   

check_token_budget(3400, 4096)
check_token_budget(4096, 4096)
check_token_budget(1000, 4096)


# Exercise 3 — Multi-Condition Validator
# A dataset entry is valid only if ALL of the following are true:

# text is a non-empty string
# label is in ["positive", "negative", "neutral"]
# confidence is between 0.0 and 1.0 (inclusive)
# word_count is a positive integer
# Write a validator that checks each condition individually and prints which ones fail.

# Test data:

# entry_1 = {"text": "Great product!", "label": "positive", "confidence": 0.95, "word_count": 2}
# entry_2 = {"text": "", "label": "happy", "confidence": 1.2, "word_count": -1}

def validator(props):
    if not isinstance(props.get("text"), str) or not props.get("text"):
        print("Validation failed: 'text' must be a non-empty string.")
    if props.get("label") not in ["positive", "negative", "neutral"]:
        print("Validation failed: 'label' must be one of ['positive', 'negative', 'neutral'].")
    if not (0.0 <= props.get("confidence", -1) <= 1.0):
        print("Validation failed: 'confidence' must be between 0.0 and 1.0.")
    if not isinstance(props.get("word_count"), int) or props.get("word_count") <= 0:
        print("Validation failed: 'word_count' must be a positive integer.")
    else:
        print("All validations passed.")

validator({"text": "Great product!", "label": "positive", "confidence": 0.95, "word_count": 2})
validator({"text": "", "label": "happy", "confidence": 1.2, "word_count": -1})



# Exercise 4 — FizzBuzz (AI Edition)
# For numbers 1 to 30:

# Print "Batch" if divisible by 3 (batch processing step)
# Print "Epoch" if divisible by 5 (epoch completed)
# Print "Checkpoint" if divisible by both 3 and 5 (save checkpoint!)
# Otherwise print the number
# Hint: Check the combined condition FIRST.

for i in range(1, 31):
    if i % 3 == 0 and i % 5 == 0:
        print(f"{i}: Checkpoint")
    elif i % 3 == 0:
        print(f"{i}: Batch")
    elif i % 5 == 0:
        print(f"{i}: Epoch")
    else:
        print(i)