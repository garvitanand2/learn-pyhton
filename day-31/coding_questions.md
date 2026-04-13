# Python DSA Coding Problems — 25 Problems
## Categories: Arrays/Lists | Strings | Dicts/Sets | Linked Lists | Stack/Queue | Recursion/DP | Sorting/Search

Format per problem:
- Problem statement
- Examples
- Solution with inline comments
- Time & Space complexity

---

## 1. Two Sum
**Problem:** Given a list of integers and a target, return indices of the two numbers that add up to target. Each input has exactly one solution.

**Example:**
```
nums = [2, 7, 11, 15], target = 9 → [0, 1]
nums = [3, 2, 4], target = 6 → [1, 2]
```

**Solution:**
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}           # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []                            # guaranteed to have a solution

assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
```
**Complexity:** Time O(n), Space O(n)

---

## 2. Valid Anagram
**Problem:** Given two strings, return True if one is an anagram of the other.

**Example:**
```
"anagram", "nagaram" → True
"rat", "car" → False
```

**Solution:**
```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# Alternative without Counter — O(n log n)
def is_anagram_sort(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)

assert is_anagram("anagram", "nagaram") is True
assert is_anagram("rat", "car") is False
```
**Complexity:** Time O(n), Space O(n)

---

## 3. Maximum Subarray Sum (Kadane's Algorithm)
**Problem:** Find the contiguous subarray with the largest sum.

**Example:**
```
[-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6  (subarray: [4, -1, 2, 1])
```

**Solution:**
```python
def max_subarray(nums: list[int]) -> int:
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)  # extend or restart
        max_sum = max(max_sum, current_sum)
    return max_sum

assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert max_subarray([-1]) == -1
```
**Complexity:** Time O(n), Space O(1)

---

## 4. Valid Parentheses
**Problem:** Given a string of `()[]{}`, return True if it is valid (every opening bracket has a matching closing bracket in the right order).

**Example:**
```
"()" → True | "()[]{}" → True | "(]" → False | "([)]" → False | "{[]}" → True
```

**Solution:**
```python
def is_valid(s: str) -> bool:
    stack: list[str] = []
    matching = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack[-1] != matching[ch]:
                return False
            stack.pop()
    return len(stack) == 0

assert is_valid("()[]{}") is True
assert is_valid("([)]") is False
assert is_valid("{[]}") is True
```
**Complexity:** Time O(n), Space O(n)

---

## 5. Reverse a Linked List
**Problem:** Reverse a singly linked list. Return the new head.

**Solution:**
```python
from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

@dataclass
class ListNode:
    val: int
    next: Optional[ListNode] = None

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev: Optional[ListNode] = None
    current = head
    while current:
        next_node = current.next   # save next
        current.next = prev        # reverse pointer
        prev = current             # advance prev
        current = next_node        # advance current
    return prev                    # prev is new head

def to_list(head: Optional[ListNode]) -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

def from_list(vals: list[int]) -> Optional[ListNode]:
    if not vals: return None
    head = ListNode(vals[0])
    cur = head
    for v in vals[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head

assert to_list(reverse_list(from_list([1,2,3,4,5]))) == [5,4,3,2,1]
```
**Complexity:** Time O(n), Space O(1)

---

## 6. Merge Two Sorted Lists
**Problem:** Merge two sorted linked lists and return the merged sorted list.

**Solution:**
```python
def merge_sorted(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2       # attach remaining
    return dummy.next

l1 = from_list([1, 2, 4])
l2 = from_list([1, 3, 4])
assert to_list(merge_sorted(l1, l2)) == [1, 1, 2, 3, 4, 4]
```
**Complexity:** Time O(n+m), Space O(1)

---

## 7. Binary Search
**Problem:** Given a sorted array and target, return the index if found, else -1.

**Solution:**
```python
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2   # avoid overflow
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
```
**Complexity:** Time O(log n), Space O(1)

---

## 8. Longest Common Prefix
**Problem:** Find the longest common prefix string among a list of strings.

**Example:** `["flower", "flow", "flight"]` → `"fl"`

**Solution:**
```python
def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]             # shrink prefix
            if not prefix:
                return ""
    return prefix

assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
assert longest_common_prefix(["dog", "racecar", "car"]) == ""
```
**Complexity:** Time O(S) where S = total characters, Space O(1)

---

## 9. Fibonacci with Memoization
**Problem:** Return the nth Fibonacci number efficiently.

**Solution:**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Iterative O(1) space version
def fib_iter(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

assert fib(10) == 55
assert fib_iter(10) == 55
```
**Complexity:** Time O(n), Space O(n) recursive | O(1) iterative

---

## 10. Climbing Stairs (DP)
**Problem:** You can climb 1 or 2 steps at a time. How many distinct ways to reach the top of n stairs?

**Example:** n=3 → 3 (1+1+1, 1+2, 2+1)

**Solution:**
```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b   # same recurrence as Fibonacci!
    return b

assert climb_stairs(2) == 2
assert climb_stairs(3) == 3
assert climb_stairs(5) == 8
```
**Complexity:** Time O(n), Space O(1)

---

## 11. Contains Duplicate
**Problem:** Return True if any value appears at least twice in the array.

**Solution:**
```python
def contains_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))

# O(n) single pass
def contains_duplicate_v2(nums: list[int]) -> bool:
    seen: set[int] = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

assert contains_duplicate([1, 2, 3, 1]) is True
assert contains_duplicate([1, 2, 3, 4]) is False
```
**Complexity:** Time O(n), Space O(n)

---

## 12. Move Zeros
**Problem:** Move all zeros to the end of the array while maintaining relative order of non-zero elements. In-place.

**Example:** `[0, 1, 0, 3, 12]` → `[1, 3, 12, 0, 0]`

**Solution:**
```python
def move_zeros(nums: list[int]) -> None:
    write = 0
    for num in nums:
        if num != 0:
            nums[write] = num
            write += 1
    for i in range(write, len(nums)):
        nums[i] = 0

nums = [0, 1, 0, 3, 12]
move_zeros(nums)
assert nums == [1, 3, 12, 0, 0]
```
**Complexity:** Time O(n), Space O(1)

---

## 13. Group Anagrams
**Problem:** Group a list of strings into lists of anagrams.

**Example:** `["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"],["tan","nat"],["bat"]]`

**Solution:**
```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: dict[tuple, list[str]] = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))    # sorted letters are the anagram key
        groups[key].append(s)
    return list(groups.values())

result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
assert sorted(map(sorted, result)) == sorted(map(sorted, [["eat","tea","ate"],["tan","nat"],["bat"]]))
```
**Complexity:** Time O(n * k log k) where k = max string length, Space O(n*k)

---

## 14. Find the Missing Number
**Problem:** Given array containing n distinct numbers from 0 to n, find the missing one.

**Solution:**
```python
def missing_number(nums: list[int]) -> int:
    n = len(nums)
    expected_sum = n * (n + 1) // 2   # Gauss formula
    return expected_sum - sum(nums)

# XOR approach — O(1) extra space, no overflow risk
def missing_number_xor(nums: list[int]) -> int:
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result

assert missing_number([3, 0, 1]) == 2
assert missing_number_xor([9,6,4,2,3,5,7,0,1]) == 8
```
**Complexity:** Time O(n), Space O(1)

---

## 15. Product of Array Except Self
**Problem:** Return an array where each element is the product of all other elements. No division allowed.

**Example:** `[1, 2, 3, 4]` → `[24, 12, 8, 6]`

**Solution:**
```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [1] * n
    # left pass: result[i] = product of nums[0..i-1]
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    # right pass: multiply by product of nums[i+1..n-1]
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result

assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
```
**Complexity:** Time O(n), Space O(1) (output array not counted)

---

## 16. Longest Substring Without Repeating Characters
**Problem:** Find the length of the longest substring with all unique characters (sliding window).

**Example:** `"abcabcbb"` → 3 ("abc")

**Solution:**
```python
def length_of_longest_substring(s: str) -> int:
    char_index: dict[str, int] = {}    # char → last seen index
    start = max_len = 0
    for end, ch in enumerate(s):
        if ch in char_index and char_index[ch] >= start:
            start = char_index[ch] + 1   # shrink window past duplicate
        char_index[ch] = end
        max_len = max(max_len, end - start + 1)
    return max_len

assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3
```
**Complexity:** Time O(n), Space O(min(m, n)) where m = charset size

---

## 17. Level-Order Traversal (BFS on Binary Tree)
**Problem:** Return the level-by-level values of a binary tree as a list of lists.

**Solution:**
```python
from collections import deque
from dataclasses import dataclass

@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None

def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    if not root:
        return []
    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result

root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert level_order(root) == [[3], [9, 20], [15, 7]]
```
**Complexity:** Time O(n), Space O(n)

---

## 18. Number of Islands (DFS)
**Problem:** Count the number of islands in a 2D grid where `"1"` = land and `"0"` = water.

**Solution:**
```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "#"    # mark visited (in-place)
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                count += 1
    return count

grid = [["1","1","0","0"],["1","1","0","0"],["0","0","1","0"],["0","0","0","1"]]
assert num_islands(grid) == 3
```
**Complexity:** Time O(m*n), Space O(m*n) call stack

---

## 19. Word Frequency Counter (NLP flavored)
**Problem:** Given a list of documents, return a dict of {word: total_count} sorted by count descending.

**Solution:**
```python
from collections import Counter

def word_freq(documents: list[str]) -> list[tuple[str, int]]:
    counter: Counter = Counter()
    for doc in documents:
        tokens = doc.lower().split()
        counter.update(tokens)
    return counter.most_common()

docs = ["the cat sat on the mat", "the dog sat on the log", "cats and dogs"]
result = word_freq(docs)
print(result[:3])
assert result[0][0] == "the"   # "the" appears 4 times
```
**Complexity:** Time O(n*m) where n=docs, m=avg tokens; Space O(V) vocabulary

---

## 20. Flatten a Nested List (Recursive)
**Problem:** Flatten an arbitrarily-nested list into a flat list.

**Example:** `[1, [2, [3, 4], 5], 6]` → `[1, 2, 3, 4, 5, 6]`

**Solution:**
```python
def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))   # recurse
        else:
            result.append(item)
    return result

# Generator version — memory efficient
def flatten_gen(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten_gen(item)
        else:
            yield item

assert flatten([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6]
assert list(flatten_gen([1, [2, [3, 4], 5], 6])) == [1, 2, 3, 4, 5, 6]
```
**Complexity:** Time O(n), Space O(depth) recursion stack

---

## 21. Rotating a Matrix 90°
**Problem:** Rotate an N×N matrix 90° clockwise in-place.

**Solution:**
```python
def rotate_matrix(matrix: list[list[int]]) -> None:
    n = len(matrix)
    # Step 1: Transpose (flip along diagonal)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()

m = [[1,2,3],[4,5,6],[7,8,9]]
rotate_matrix(m)
assert m == [[7,4,1],[8,5,2],[9,6,3]]
```
**Complexity:** Time O(n²), Space O(1)

---

## 22. Coin Change (DP)
**Problem:** Given coin denominations and an amount, find the minimum number of coins to make that amount. Return -1 if impossible.

**Solution:**
```python
def coin_change(coins: list[int], amount: int) -> int:
    INF = float("inf")
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1

assert coin_change([1, 5, 10, 25], 41) == 4   # 25+10+5+1
assert coin_change([2], 3) == -1
```
**Complexity:** Time O(amount * coins), Space O(amount)

---

## 23. Longest Increasing Subsequence (DP)
**Problem:** Return the length of the longest strictly increasing subsequence.

**Example:** `[10, 9, 2, 5, 3, 7, 101, 18]` → 4 (2, 3, 7, 101)

**Solution:**
```python
def length_of_lis(nums: list[int]) -> int:
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n   # each element is a subsequence of length 1
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
```
**Complexity:** Time O(n²), Space O(n)  [O(n log n) with patience sorting]

---

## 24. Serialize and Deserialize a Binary Tree
**Problem:** Implement `serialize(root)` → string and `deserialize(data)` → tree that round-trips correctly.

**Solution:**
```python
def serialize(root: Optional[TreeNode]) -> str:
    result: list[str] = []
    def dfs(node: Optional[TreeNode]) -> None:
        if not node:
            result.append("N")
            return
        result.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return ",".join(result)

def deserialize(data: str) -> Optional[TreeNode]:
    vals = iter(data.split(","))
    def dfs() -> Optional[TreeNode]:
        val = next(vals)
        if val == "N":
            return None
        node = TreeNode(int(val))
        node.left  = dfs()
        node.right = dfs()
        return node
    return dfs()

tree = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
reconstructed = deserialize(serialize(tree))
assert level_order(reconstructed) == level_order(tree)
```
**Complexity:** Time O(n), Space O(n)

---

## 25. Top K Frequent Words (Heap)
**Problem:** Given a list of words, return the k most frequent words sorted by frequency (ties broken alphabetically).

**Example:** `["i","love","python","i","love","coding"], k=2` → `["i","love"]`

**Solution:**
```python
import heapq
from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    counts = Counter(words)
    # Min-heap of (-freq, word) — heap size k
    heap: list[tuple[int, str]] = []
    for word, freq in counts.items():
        heapq.heappush(heap, (-freq, word))
    return [heapq.heappop(heap)[1] for _ in range(k)]

result = top_k_frequent(["i","love","python","i","love","coding"], 2)
assert result == ["i", "love"]
```
**Complexity:** Time O(n log k), Space O(n)

---

## Quick Complexity Reference

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| Two Sum | O(n) | O(n) | hash map |
| Binary Search | O(log n) | O(1) | sorted array required |
| Merge Sort | O(n log n) | O(n) | stable |
| Quick Sort | O(n log n) avg | O(log n) | in-place, not stable |
| BFS/DFS (tree) | O(n) | O(n) | |
| Kadane's | O(n) | O(1) | max subarray |
| Sliding Window | O(n) | O(k) | k = window size |
| DP (tabulation) | O(n*m) | O(n) | |
| Heap top-k | O(n log k) | O(k) | |
| Trie insert | O(m) | O(m) | m = word length |
