# Exercise 5 — Identity Puzzle (Interview-Focused)
# Predict the output of each line before running it. Then verify:

# a = 256
# b = 256
# print(a is b)   # ?

# c = 257
# d = 257
# print(c is d)   # ?

# x = None
# y = None
# print(x is y)   # ?

# p = "hello"
# q = "hello"
# print(p is q)   # ?  (string interning — research this!)
# Explain in a comment WHY each result is what it is.

a = 256
b = 256
print(a is b)   # True — In Python, small integers (typically between -5 and 256) are cached and reused, so a and b point to the same memory location.

c = 257
d = 257
print(c is d)   # False — Large integers are not cached, so c and d point to different memory locations.

x = None
y = None
print(x is y)   # True — None is a singleton in Python, so x and y point to the same memory location.

p = "hello"
q = "hello"
print(p is q)   # True — String interning is a mechanism where Python automatically reuses string objects for identical string literals, so p and q point to the same memory location.