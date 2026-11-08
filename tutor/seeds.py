"""Ten hand-written gold examples (5 Roman Hinglish, 5 English). They have two jobs:
1) few-shot examples that show the teacher model the exact style and picture formats;
2) the first rows of the training set. Add your own good examples here (more gold = better tutor)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from tutor_prompt import TUTOR_SYSTEM  # noqa: E402

SEEDS = [
 {"topic": "variables in Python", "lang": "hinglish", "q": "Python me variable kya hota hai? Simple samjhao.", "a": r'''**Idea**
Variable ek **naam-tag** hai jo kisi value (object) par chipka hota hai. Value alag jagah rehti hai, tag sirf us par point karta hai (jaise `age` naam 25 par laga hai). Bilkul bag ke tag jaisa: tag par naam likha hai, bag alag cheez hai. Ek hi value par do tag bhi lag sakte hain.

**Visual**
```vars
{"title": "Naam (tag) aur object", "vars": [{"name": "age", "value": "25"}, {"name": "name", "value": "\"Ravi\""}, {"name": "is_student", "value": "True"}]}
```

**Code**
```python
age = 25            # age naam ka tag 25 wale object par laga
name = "Ravi"       # text ko quotes me likhte hain
is_student = True   # True ya False ko boolean bolte hain
age = age + 1       # naya object 26 bana, aur age ka tag ab us par laga
print(name, age)    # Ravi 26
```

**Step by step**
1. `age = 25` se Python ne 25 wala object banaya aur `age` naam ka tag us par laga diya.
2. `name = "Ravi"` se text object bana aur `name` ka tag us par laga.
3. `age = age + 1` me pehle `age` ke object (25) se +1 hua, naya object 26 bana, aur `age` ka tag ab naye object par laga.
4. `print` ne tags ke peeche ke objects dikhaye: `Ravi 26`.

**Common mistake**
Beginner `25 = age` likh dete hain. Hamesha **naam pehle, value baad me**: `age = 25`. Aur yaad rakho: `b = a` se value ki copy nahi banti, bas dusra tag lagta hai.

**Try it**
Ek variable `city` banao jisme tumhare sheher ka naam ho, aur use print karo.'''},
 {"topic": "if-else", "lang": "en", "q": "Explain if-else in Python to a complete beginner.", "a": r'''**Idea**
if-else lets a program make a decision. It is like deciding about an umbrella: if it is raining, take it, else leave it at home.

**Visual**
```flow
Start -> Read marks -> marks >= 40?
marks >= 40? -(yes)-> Print "Pass" -> End
marks >= 40? -(no)-> Print "Fail" -> End
```

**Code**
```python
marks = 55
if marks >= 40:        # the condition is checked first
    print("Pass")      # runs only when the condition is True
else:
    print("Fail")      # runs when the condition is False
```

**Step by step**
1. `marks = 55` stores 55.
2. Python checks `55 >= 40`. That is True.
3. So it runs the `if` block and prints `Pass`.
4. The `else` block is skipped completely.

**Common mistake**
Writing `if marks = 40:` with one `=`. One `=` stores a value; to compare use two: `==`.

**Try it**
Write a program that prints "Adult" if `age` is 18 or more, otherwise "Minor".'''},
 {"topic": "for loop", "lang": "hinglish", "q": "for loop samjhao, list ke saath.", "a": r'''**Idea**
for loop ka matlab: "list ki har cheez ke liye yeh kaam karo". Jaise teacher attendance leti hai: har student ka naam ek ek karke bolti hai.

**Visual**
```array
{"title": "Pehla round: n = 3", "items": [3, 5, 2], "pointers": {"n": 0}, "highlight": [0]}
```

**Code**
```python
numbers = [3, 5, 2]
total = 0
for n in numbers:        # n har round me list ki agli value leta hai
    total = total + n    # total me add karte jao
print(total)             # 10
```

**Step by step**
1. Shuru me `total = 0`.
2. Round 1: `n = 3`, to `total = 0 + 3 = 3`.
3. Round 2: `n = 5`, to `total = 3 + 5 = 8`.
4. Round 3: `n = 2`, to `total = 8 + 2 = 10`.
5. List khatam, loop ruk gaya, aur `10` print hua.

**Common mistake**
`total = 0` ko loop ke andar likh dena. Tab har round me total wapas 0 ho jayega. Isse loop ke **bahar** likho.

**Try it**
Isi list ke numbers ka guna (product) nikalo. Soch ke batao: total ki jagah shuru me kaunsi value rakhni chahiye?'''},
 {"topic": "list vs tuple", "lang": "en", "q": "What is the difference between a list and a tuple?", "a": r'''**Idea**
A list is like a shopping list you keep editing. A tuple is like a date of birth: once written, it does not change.

**Visual**
| Feature | list | tuple |
|---|---|---|
| Brackets | `[ ]` | `( )` |
| Can change after creation | Yes | No |
| Good for | data that changes (a cart) | fixed data (a point, a date) |

**Code**
```python
cart = ["milk", "bread"]
cart.append("eggs")        # lists can grow
point = (10, 20)
# point[0] = 5             # would raise TypeError: tuples cannot change
print(cart, point)         # ['milk', 'bread', 'eggs'] (10, 20)
```

**Step by step**
1. `cart` starts with 2 items.
2. `append("eggs")` adds a third item at the end.
3. `point` is a tuple, so we can read `point[0]` but not change it.
4. `print` shows both.

**Common mistake**
`(5)` is just the number 5, not a tuple. A one-item tuple needs a comma: `(5,)`.

**Try it**
Make a list of 3 fruits, add a 4th fruit, and then try to do the same with a tuple. What error do you get?'''},
 {"topic": "functions", "lang": "hinglish", "q": "Function kya hota hai? def aur return samjhao.", "a": r'''**Idea**
Function ek **chhoti machine** hai: tum input daalte ho, wo kaam karti hai, aur result wapas deti hai. Jaise juice machine: fruit daalo, juice nikalo.

**Visual**
```flow
Call add(2, 3) -> a = 2, b = 3 -> Calculate a + b -> return 5 -> result = 5 -> print(result)
```

**Code**
```python
def add(a, b):        # function ka naam add, inputs a aur b
    return a + b      # result wapas bhejta hai

result = add(2, 3)    # function ko bulaya
print(result)         # 5
```

**Step by step**
1. `def add(a, b)` sirf machine banata hai, abhi chalti nahi.
2. `add(2, 3)` se machine chali: `a = 2`, `b = 3`.
3. `a + b` ka answer 5 bana aur `return` ne wapas bhej diya.
4. `result` me 5 rakha gaya, aur `print` ne use dikhaya.

**Common mistake**
`return` ki jagah `print` likhna. `print` sirf screen par dikhata hai, value wapas nahi deta, to `result` me `None` aa jata hai.

**Try it**
Ek function `square(n)` likho jo n ka square return kare, aur `square(4)` print karo.'''},
 {"topic": "recursion", "lang": "en", "q": "Explain recursion with factorial.", "a": r'''**Idea**
Recursion means a function calls itself on a smaller problem. Like opening nested boxes: you keep opening a smaller box until you reach the smallest one.

**Visual**
```sim
{"algo": "factorial", "n": 3}
```

**Code**
```python
def factorial(n):
    if n <= 1:                    # base case: stop here (also covers factorial(0) = 1)
        return 1
    return n * factorial(n - 1)   # call itself with a smaller number

print(factorial(3))               # 6
```

**Step by step**
1. Each call to `factorial` waits on the call stack until the smaller call below it returns. Press play to watch the stack grow.
2. The call that reaches the base case returns 1 without calling itself again.
3. Then the waiting calls finish one by one, each multiplying its own `n` by the value returned to it.

**Common mistake**
Forgetting the base case, or writing `n == 1` only. Then `factorial(0)` never stops and Python raises `RecursionError`.

**Try it**
Write a recursive function `total(n)` that returns 1 + 2 + ... + n.'''},
 {"topic": "binary search", "lang": "hinglish", "q": "Binary search samjhao, easy me.", "a": r'''**Idea**
Binary search me hum **beech wali value** dekhte hain aur aadhi list phenk dete hain. Jaise dictionary me word dhoondhna: seedha beech me kholte ho, phir left ya right jaate ho. Dhyan rakho: list **sorted** honi chahiye.

**Visual**
```sim
{"algo": "binary_search", "input": [2, 5, 8, 12, 16, 23, 38], "target": 23}
```

**Code**
```python
def binary_search(items, target):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2      # beech ka index
        if items[mid] == target:
            return mid               # mil gaya
        elif items[mid] < target:
            low = mid + 1            # right half me dhoondo
        else:
            high = mid - 1           # left half me dhoondo
    return -1                        # nahi mila

print(binary_search([2, 5, 8, 12, 16, 23, 38], 23))   # 5
```

**Step by step**
1. `low` shuru me pehla index hai aur `high` aakhri index. Play dabao aur `low`, `mid`, `high` ko badalte dekho.
2. Har round me `mid` beech ka index hota hai. Agar `items[mid]` target se chhota hai to `low = mid + 1`, bada hai to `high = mid - 1`.
3. Jab `items[mid]` target ke barabar ho jaye to function `mid` return karta hai. Agar `low` `high` se bada ho jaye to `-1`.

**Common mistake**
Unsorted list par binary search chalana. Tab answer galat aa sakta hai. Pehle `sort()` karo.

**Try it**
Same list me 5 dhoondho aur kagaz par `low`, `mid`, `high` ke steps likho.'''},
 {"topic": "bubble sort", "lang": "en", "q": "How does bubble sort work?", "a": r'''**Idea**
Bubble sort compares neighbours and swaps them if they are in the wrong order. After each pass the biggest unsorted number "bubbles up" to the end, like a bubble rising in water.

**Visual**
```sim
{"algo": "bubble_sort", "input": [5, 2, 9, 1]}
```

**Code**
```python
nums = [5, 2, 9, 1]
n = len(nums)
for i in range(n - 1):                                   # each pass fixes one value at the end
    for j in range(n - 1 - i):                           # compare neighbours in the unsorted part
        if nums[j] > nums[j + 1]:                        # left bigger than right?
            nums[j], nums[j + 1] = nums[j + 1], nums[j]  # swap them
print(nums)    # [1, 2, 5, 9]
```

**Step by step**
1. Press play. The orange boxes are the two neighbours being compared.
2. If the left one is bigger, they turn red and swap places.
3. At the end of a pass the last unsorted box turns green: it is in its final place.
4. The counters show the real number of comparisons and swaps so far.

**Common mistake**
Using `range(n)` for the inner loop. Then `nums[j + 1]` goes past the end and raises `IndexError`. Use `n - 1 - i`.

**Try it**
Change the list to `[1, 2, 3, 4]` and play it. How many swaps do you see, and why?'''},
 {"topic": "Big-O notation", "lang": "hinglish", "q": "Big-O kya hota hai? Chart ke saath samjhao.", "a": r'''**Idea**
Big-O batata hai ki data bada hone par program ke **steps kitne badhte hain**. Jaise bus me ticket check karna: pehli seat dekhna ek step hai, par har seat dekhna seats ke hisaab se badhta hai.

**Visual**
```complexity
{"n": 8, "curves": ["1", "log n", "n", "n^2"]}
```

**Code**
```python
numbers = [4, 8, 15, 16, 23, 42, 7, 9]

print(numbers[0])        # O(1): seedha pehla item (4), bas ek step

for n in numbers:        # O(n): har item ek baar dekha
    if n == 23:
        print("mil gaya")
        break
```

**Step by step**
1. `numbers[0]` list ki size se fark nahi padta, hamesha 1 step. Ye O(1) hai.
2. Loop worst case me saare 8 items dekhta hai. Ye O(n) hai.
3. Yahan 23 paanchva item hai, to loop 5 steps me ruk gaya.

**Common mistake**
Sochna ki O(n) ka matlab hamesha n steps. Big-O **worst case** batata hai; kabhi item pehle hi mil sakta hai.

**Try it**
Do loop ek ke andar ek likho (nested loop) aur socho: 8 items par kitne steps lagenge?'''},
 {"topic": "dictionary", "lang": "en", "q": "What is a dictionary in Python?", "a": r'''**Idea**
A dictionary stores data as key and value pairs, like a phone contact: the name is the key and the number is the value. You look up by name, not by position.

**Visual**
```vars
{"title": "student dictionary", "vars": [{"name": "\"name\"", "value": "\"Asha\""}, {"name": "\"age\"", "value": "19"}, {"name": "\"city\"", "value": "\"Pune\""}]}
```

**Code**
```python
student = {"name": "Asha", "age": 19}      # key: value pairs
student["city"] = "Pune"                   # add a new pair
print(student["name"])                     # Asha
print(student.get("phone", "not found"))   # safe lookup with a default
```

**Step by step**
1. The dictionary starts with two pairs.
2. `student["city"] = "Pune"` adds a third pair.
3. `student["name"]` finds the value for the key `"name"`: `Asha`.
4. `get("phone", ...)` finds no such key, so it returns the default `not found`.

**Common mistake**
Writing `student["phone"]` for a key that does not exist raises `KeyError`. Use `.get()` when the key may be missing.

**Try it**
Make a dictionary for a book with `title` and `author`, then print the author.'''},
]


def as_messages(s):
    return {"topic": s["topic"], "lang": s["lang"], "messages": [
        {"role": "system", "content": TUTOR_SYSTEM}, {"role": "user", "content": s["q"]}, {"role": "assistant", "content": s["a"]}]}


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "seed.jsonl")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for s in SEEDS:
            f.write(json.dumps(as_messages(s), ensure_ascii=False) + "\n")
    print(f"wrote {len(SEEDS)} gold examples to {out}")
