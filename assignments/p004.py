# Exercise 4 — String Exploration
# Given the string:

# text = "Large Language Models are transforming the AI industry."
# Without importing any library, find:

# Total number of characters (including spaces)
# Number of words (hint: .split())
# Whether "AI" appears in the text (bool)
# The first 5 characters
# The text in UPPERCASE

text = "Large Language Models are transforming the AI industry."
no_of_characters = len(text)
no_of_words = len(text.split())
contains_ai = "AI" in text
first_five_characters = text[:5]
uppercase_text = text.upper()
print(f"Total number of characters: {no_of_characters}")
print(f"Number of words: {no_of_words}")
print(f"Does the text contain 'AI'? {contains_ai}")
print(f"First 5 characters: '{first_five_characters}'")
print(f"Text in uppercase: '{uppercase_text}'")