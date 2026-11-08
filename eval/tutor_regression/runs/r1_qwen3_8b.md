# Tutor regression: qwen3:8b (r1)

## py01 Python fundamentals
Q: Explain Python variables to a beginner.
checks failed: none

**Idea**: Python variables are like labels for things. You give a label (name) to an object (like a number or list). Two labels can point to the same thing. Example: You can call your bus ticket "ticket" or "my_ticket" — both point to the same ticket.

**Visual**:
```flow
Start -> Assign "ticket" to bus -> "ticket" points to bus -> End
```

**Code**:
```python
# Label "ticket" points to the bus
ticket = "bus"
# Label "my_ticket" points to the same bus
my_ticket = ticket
```

**Step by step**:  
- `ticket = "bus"` gives the label "ticket" to the object "bus".  
- `my_ticket = ticket` gives the label "my_ticket" to the same object "bus".  

**Common mistake**: Beginners think variables are boxes that hold values. But in Python, variables are labels that point to objects. So changing one label doesn't change the other unless they point to the same object.

**Try it**: Create two labels, like "cup" and "my_cup", and make them point to the same object, like "tea". Then change one label to point to a different object, like "coffee". What happens to the other label?

## py02 Python fundamentals
Q: Python me list aur tuple me kya fark hai?
checks failed: [('teaching_quality', 'six-part format, pictures and code are valid', 'array: block is not valid')]

**Idea**: List aur tuple dono data store karte hain, lekin list change ho sakti hai aur tuple change nahi ho sakti. List ko hum bracket [] me likhte hain aur tuple ko bracket () me.  
**Visual**:  
```array
{"title": "List", "items": [1, 2, 3], "pointers": {"i": 0}, "highlight": [0]}
```  
```array
{"title": "Tuple", "items": (1, 2, 3), "pointers": {"i": 0}, "highlight": [0]}
```  
**Code**:  
```py
# List example
my_list = [1, 2, 3]
my_list[0] = 10  # Change value
print(my_list)

# Tuple example
my_tuple = (1, 2, 3)
# my_tuple[0] = 10  # This will give an error
print(my_tuple)
```  
**Step by step**:  
- `my_list = [1, 2, 3]` creates a list with values 1, 2, 3.  
- `my_list[0] = 10` changes the first value to 10.  
- `print(my_list)` shows the updated list.  
- `my_tuple = (1, 2, 3)` creates a tuple with values 1, 2, 3.  
- Trying to change a tuple value gives an error because tuples are immutable.  
- `print(my_tuple)` shows the original tuple.  
**Common mistake**: Beginners think both list and tuple can be changed. Fix: Remember tuples are fixed and lists are changeable.  
**Try it**: Make a list of your favorite fruits and change one fruit. Then try to do the same with a tuple. What happens?

## py03 Python fundamentals
Q: What is the difference between mutable and immutable types in Python?
checks failed: none

**Idea**: In Python, some data types can be changed (mutable), and others cannot (immutable). For example, a list (mutable) can have items added, while a string (immutable) cannot be changed once created.

**Visual**:
```flow
Start -> Read data type -> Is it list? -(yes)-> Can change -> End
Is it list? -(no)-> Is it string? -(yes)-> Cannot change -> End
Is it string? -(no)-> Other types -> End
```

**Code**:
```python
# Example of mutable and immutable types
my_list = [1, 2, 3]  # List is mutable
my_string = "hello"  # String is immutable

my_list.append(4)    # Changes the list
# my_string.append(4)  # This would cause an error
```

**Step by step**:
- `my_list = [1, 2, 3]` creates a list and assigns it to `my_list`.
- `my_list.append(4)` adds the number 4 to the list, changing it.
- `my_string = "hello"` creates a string and assigns it to `my_string`.
- Trying to change `my_string` with `append()` would cause an error because strings are immutable.

**Common mistake**: Beginners often try to change immutable types like strings or tuples, which leads to errors. They should use new variables or functions to create new values.

**Try it**: Create a list and a string. Try to add an item to both and see what happens.

## py04 Python fundamentals
Q: Explain what this prints: a = [1, 2]; b = a; b.append(3); print(a)
checks failed: none

**Idea**: When you assign a list to another variable, both point to the same list. Changing one affects the other. Example: If you share a bowl of chikki with a friend, and you add more chikki, your friend's bowl also gets more.

**Visual**:
```flow
Start -> Read a = [1, 2] -> Read b = a -> b.append(3) -> Print a -> End
```

**Code**:
```python
a = [1, 2]  # Create a list called a with elements 1 and 2
b = a       # b now points to the same list as a
b.append(3) # Add 3 to the list that both a and b point to
print(a)    # Print the list, which now has 1, 2, 3
```

**Step by step**:
1. `a = [1, 2]` creates a list and names it `a`.
2. `b = a` makes `b` point to the same list as `a`.
3. `b.append(3)` adds 3 to the list, which both `a` and `b` point to.
4. `print(a)` shows the updated list `[1, 2, 3]`.

**Common mistake**: Thinking that `b = a` makes a copy of the list. In reality, `b` points to the same list as `a`, so changes to one affect the other.

**Try it**: What happens if you do `a = [1, 2]; b = a; a.append(3); print(b)?`

## py05 Python fundamentals
Q: f-string kya hota hai? Example do.
checks failed: none

**Idea**: F-string is a way to make strings in Python that can include variables and expressions. It makes writing strings easier and cleaner. For example, you can write "My name is Veya" by putting the name in the string.

**Visual**:
```flow
Start -> Read name -> Use f-string to make sentence -> Print sentence -> End
```

**Code**:
```python
name = "Veya"
message = f"Hello, my name is {name}"
print(message)
```
This code stores the name in a variable and then uses an f-string to create a message that includes the name.

**Step by step**: 
1. `name = "Veya"` saves the name in a variable.
2. `message = f"Hello, my name is {name}"` creates a string that includes the value of the `name` variable.
3. `print(message)` shows the message on the screen.

**Common mistake**: Beginners sometimes forget to use the `f` before the string, which makes Python not understand the code.

**Try it**: Change the name to "Rahul" and see what happens.

## py06 Python fundamentals
Q: How do I avoid a KeyError when a dictionary key may be missing?
checks failed: none

**Idea**: You can check if a key exists in a dictionary before trying to access it. This helps avoid a KeyError. For example, you might check if a student's name is in a list of students before giving them a grade.

**Visual**:
```flow
Start -> Check if key exists? -> yes -> Get value -> End
Check if key exists? -> no -> Skip -> End
```

**Code**:
```python
# Create a dictionary of student grades
student_grades = {"Alice": 90, "Bob": 85}

# Check if "Charlie" is in the dictionary before accessing
if "Charlie" in student_grades:
    print(student_grades["Charlie"])
else:
    print("Charlie is not in the list")
```

**Step by step**: 
- The code creates a dictionary called `student_grades` with some student names and their grades.
- It then checks if the key `"Charlie"` is in the dictionary.
- If the key is found, it prints the value (grade) for "Charlie".
- If the key is not found, it prints a message saying "Charlie is not in the list".

**Common mistake**: Forgetting to use the `in` keyword and trying to access a key directly, which causes a KeyError.

**Try it**: Modify the code to check for "Bob" instead of "Charlie". What happens if you try to access "David"?

## lp01 Loops and conditions
Q: Explain a for loop with range().
checks failed: none

**Idea**: A for loop with range() repeats a task a set number of times. For example, you can make your friend drink 3 cups of chai by repeating the action 3 times.

**Visual**:
```flow
Start -> Read number n -> n % 2 == 0?
n % 2 == 0? -(yes)-> Print "even" -> End
n % 2 == 0? -(no)-> Print "odd" -> End
```

**Code**:
```py
# Make your friend drink 3 cups of chai
for _ in range(3):
    print("Drink a cup of chai!")
```

**Step by step**:
1. The `for` loop starts with `range(3)`, which creates a sequence of numbers 0, 1, 2.
2. The loop runs for each number in the sequence.
3. Inside the loop, it prints "Drink a cup of chai!" each time.

**Common mistake**: Forgetting to use `range()` correctly can cause the loop to run forever or not at all. Always use `range()` with a number to set the number of repetitions.

**Try it**: Change the number in `range()` to 5 and see how many times the message appears.

## lp02 Loops and conditions
Q: while loop kaise rukta hai? Infinite loop se kaise bachein?
checks failed: [('technical_accuracy', "any of ['update|badal|\\\\+= ?1|increment']", '')]

**Idea**: While loop runs until a condition is false. To stop it, we change the condition. Infinite loop happens when the condition never becomes false, so we must make sure the condition changes inside the loop.

**Visual**:
```flow
Start -> Read number n -> n > 0?
n > 0? -(yes)-> Print "n is positive" -> n = n - 1 -> Loop
n > 0? -(no)-> End
```

**Code**:
```python
n = 5
while n > 0:
    print("n is", n)
    n = n - 1
```

**Step by step**:
- Line 1: Start with `n = 5`.
- Line 2: Check if `n > 0` (yes, 5 > 0).
- Line 3: Print "n is 5".
- Line 4: Subtract 1 from `n` (now `n = 4`).
- Loop again: Check `n > 0` (yes, 4 > 0).
- Repeat until `n` becomes 0.

**Common mistake**: Forgetting to change the condition inside the loop, which makes the loop never stop.

**Try it**: Change the code so that the loop runs 10 times, not 5. What line should you change?

## lp03 Loops and conditions
Q: What do break and continue do in a loop?
checks failed: none

**Idea**:  
Break stops the loop immediately. Continue skips the rest of the loop and starts again.  
Example: In a canteen, break is like leaving the line, and continue is like skipping a person in line and moving to the next.

**Visual**:  
```flow
Start -> Read number n -> n == 10? -(yes)-> Print "Found 10" -> End
n == 10? -(no)-> Continue -> Read number n
```

**Code**:  
```python
# Example of break and continue in a loop
for i in range(1, 11):
    if i == 5:
        continue  # Skip 5
    if i == 10:
        break      # Stop at 10
    print(i)
```

**Step by step**:  
- The loop starts with `i = 1`.  
- When `i == 5`, `continue` skips the `print(i)` and moves to the next number.  
- When `i == 10`, `break` stops the loop immediately.  
- Numbers 1 to 4 and 6 to 9 are printed, but 5 is skipped and 10 is not printed.

**Common mistake**:  
Using `break` and `continue` in the wrong places can cause the loop to stop or skip too much. Always test with small examples.

**Try it**:  
Write a loop that prints numbers from 1 to 10, but skips 7 and stops at 9.

## lp04 Loops and conditions
Q: Show how to print a right-angled triangle of stars with nested loops.
checks failed: [('teaching_quality', 'six-part format, pictures and code are valid', 'no picture: add a flow/chart/array/vars block or a table')]

**Idea**: We use two loops. The outer loop decides how many rows. The inner loop prints stars for each row. For example, 5 rows will have 1, 2, 3, 4, 5 stars.

**Visual**:
```
*
**
***
****
*****
```

**Code**:
```python
for i in range(5):
    print('*' * (i + 1))
```

**Step by step**:
- The outer loop runs from 0 to 4 (5 times).
- In each iteration, the inner loop prints `i + 1` stars.
- So, first row has 1 star, second has 2, and so on.

**Common mistake**: Forgetting to add 1 to `i` in the inner loop, which makes the number of stars less than expected.

**Try it**: Change the number of rows from 5 to 7 and see what happens.

## lp05 Loops and conditions
Q: Explain if, elif and else with a grading example.
checks failed: none

**Idea**: `if`, `elif`, and `else` help decide what to do based on conditions. For example, a teacher can give grades based on marks.  
**Visual**:  
```flow
Start -> Read marks -> marks >= 90? -(yes)-> Print "A" -> End  
marks >= 90? -(no)-> marks >= 80? -(yes)-> Print "B" -> End  
marks >= 80? -(no)-> Print "C" -> End
```  
**Code**:  
```python  
marks = 85  
if marks >= 90:  
    print("A")  
elif marks >= 80:  
    print("B")  
else:  
    print("C")  
```  
**Step by step**:  
- The code checks if `marks` is >= 90. If yes, it prints "A" and stops.  
- If not, it checks if `marks` is >= 80. If yes, it prints "B" and stops.  
- If neither is true, it prints "C".  
**Common mistake**: Forgetting to use `else` for the default case. Always include it to cover all possibilities.  
**Try it**: Change the `marks` value to 75 and see what grade you get.

## rc01 Recursion
Q: Explain recursion with factorial.
checks failed: [('visual_correctness', 'valid sim: factorial', '')]

**Idea**: Recursion is when a function calls itself to solve a smaller part of a problem. For example, calculating factorial of 5 (5 × 4 × 3 × 2 × 1) can be done by calling the factorial function for 4 and multiplying it by 5.

**Visual**:
```flow
Start -> Read number n -> n == 0?
n == 0? -(yes)-> Return 1 -> End
n == 0? -(no)-> Return n * factorial(n-1) -> End
```

**Code**:
```python
def factorial(n):
    # Base case: if n is 0, return 1
    if n == 0:
        return 1
    # Recursive case: multiply n by factorial of n-1
    return n * factorial(n - 1)

# Example: Calculate factorial of 5
result = factorial(5)
print(result)
```

**Step by step**:
1. The function `factorial` is called with `n = 5`.
2. Since `n` is not 0, it calls `factorial(4)` and multiplies it by 5.
3. This continues until `n = 0`, where it returns 1.
4. The results are multiplied back as the function calls return, giving the final result of 120.

**Common mistake**: Forgetting the base case, which leads to infinite recursion and a crash. Always define the base case to stop the recursion.

**Try it**: Write a recursive function to calculate the factorial of 6.

## rc02 Recursion
Q: Fibonacci recursion ki time complexity kya hoti hai?
checks failed: none

**Idea**: Fibonacci recursion calculates Fibonacci numbers using a function that calls itself. Time complexity means how long it takes to run. This method is slow because it repeats calculations.

**Visual**:
```complexity
{"n": 8, "curves": ["1", "log n", "n", "n^2", "n^2", "n^2"]}
```

**Code**:
```python
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Example: fibonacci(5)
```

**Step by step**:  
- The function `fibonacci(n)` checks if `n` is 0 or 1. If yes, it returns `n`.  
- If not, it calls itself twice: once for `n-1` and once for `n-2`.  
- This creates many repeated calculations, making it very slow for large `n`.

**Common mistake**: Beginners often think the time complexity is O(n), but it's actually O(2^n) because each call branches into two more calls.

**Try it**: What happens if you call `fibonacci(10)`? How many times does the function call itself?

## rc03 Recursion
Q: What is a base case, and what happens without one?
checks failed: none

**Idea**: A base case is the simplest form of a problem that stops the recursion. Without it, the program runs forever.  
**Visual**:  
```flow
Start -> Call function -> Call function -> Call function -> ... -> No end
```  
**Code**:  
```python
# This code will crash without a base case
def count_down(n):
    print(n)
    count_down(n - 1)  # No base case here
count_down(5)
```  
**Step by step**:  
1. The function `count_down` is called with `n = 5`.  
2. It prints `5` and calls `count_down(4)`.  
3. This repeats until `n` becomes a negative number, and the program crashes.  
**Common mistake**: Forgetting to write a base case leads to infinite recursion and crashes.  
**Try it**: Add a base case to the `count_down` function so it stops when `n` is 0.

## rc04 Recursion
Q: Write a recursive function for the sum of the digits of a number.
checks failed: none

**Idea**: A recursive function adds the last digit of a number to the sum of the remaining digits. For example, 123 becomes 3 + sum(12).  
**Visual**:  
```flow
Start -> Read number n -> n < 10?  
n < 10? -(yes)-> Print n -> End  
n < 10? -(no)-> Add n % 10 to sum of n // 10 -> End
```  
**Code**:  
```python
def sum_digits(n):
    # Base case: if n is a single digit, return n
    if n < 10:
        return n
    # Recursive case: add last digit to sum of remaining digits
    return n % 10 + sum_digits(n // 10)
```  
**Step by step**:  
1. The function checks if the number is less than 10 (single digit). If yes, it returns the number.  
2. If not, it takes the last digit (n % 10) and adds it to the result of the function called with the remaining digits (n // 10).  
**Common mistake**: Forgetting the base case can cause infinite recursion. Always define a base case for the smallest input.  
**Try it**: What is the sum of the digits of 456? Write a small test case.

## rc05 Recursion
Q: Recursion versus iteration: when should I use which?
checks failed: [('technical_accuracy', "any of ['stack|memory|depth']", '')]

**Idea**: Recursion is when a function calls itself to solve smaller parts of a problem. Iteration uses loops to repeat steps. For example, counting down from 10 can be done with a loop or by calling a function that calls itself with 9, then 8, etc.

**Visual**:
```flow
Start -> Call function -> Function calls itself -> Base case reached -> Return value -> End
```

**Code**:
```python
# Recursion example: Count down from 10
def count_down(n):
    if n == 0:  # Base case
        print("Done!")
    else:
        print(n)
        count_down(n - 1)  # Recursive call

count_down(10)
```

**Step by step**:
1. The function `count_down` is called with `n = 10`.
2. It checks if `n == 0`. Since it's not, it prints `10` and calls `count_down(9)`.
3. This repeats until `n == 0`, then it prints "Done!" and ends.

**Common mistake**: Forgetting the base case can cause infinite recursion and crash the program. Always make sure the function stops at the smallest input.

**Try it**: Write a recursive function to calculate the sum of numbers from 1 to 10.

## ds01 Data structures
Q: What is a stack?
checks failed: [('technical_accuracy', "any of ['LIFO|last.in.first.out|last in, first out']", '')]

**Idea**: A stack is like a pile of plates. You can only add or remove a plate from the top. For example, when you stack books on a shelf, you always put a new book on top or take one from the top.  
**Visual**:  
```flow
Start -> Push item -> Stack full? -(yes)-> Error -> End
Stack full? -(no)-> Pop item -> End
```  
**Code**:  
```python
# Create a stack using a list
stack = []
stack.append("book1")  # Push
stack.append("book2")  # Push
print(stack.pop())     # Pop
```  
**Step by step**:  
1. `stack = []` creates an empty list to act as the stack.  
2. `stack.append("book1")` adds "book1" to the top of the stack.  
3. `stack.append("book2")` adds "book2" on top of "book1".  
4. `print(stack.pop())` removes "book2" from the top and prints it.  
**Common mistake**: Forgetting that you can only add or remove from the top of the stack.  
**Try it**: Add three items to the stack and then remove them one by one. What is the order of removal?

## ds02 Data structures
Q: What is a queue?
checks failed: [('technical_accuracy', "any of ['FIFO|first.in.first.out|first in, first out']", '')]

**Idea**: A queue is like a line of people waiting for a bus. The first person in line gets on the bus first, and new people join the end of the line.  
**Visual**:  
```flow
Start -> Add to end -> Remove from front -> End
```  
**Code**:  
```python
# Create a queue using a list
queue = []
queue.append("Rahul")  # Add Rahul to the end of the queue
queue.append("Priya")  # Add Priya to the end
print(queue.pop(0))    # Remove and print the first person (Rahul)
```  
**Step by step**:  
1. `queue = []` creates an empty list to act as the queue.  
2. `queue.append("Rahul")` adds Rahul to the end of the list.  
3. `queue.append("Priya")` adds Priya to the end.  
4. `print(queue.pop(0))` removes and prints the first item (Rahul).  
**Common mistake**: Using `pop()` without index may remove the last item instead of the first. Always use `pop(0)` for queues.  
**Try it**: Add "Ankit" and "Sita" to the queue and print the first person.

## ds03 Data structures
Q: What is a linked list?
checks failed: [('technical_accuracy', 'require node', '')]

**Idea**: A linked list is a way to store numbers or words in a line, but each part only knows the next part. Like a line of people holding hands, each person only knows who is next.  
**Visual**:  
```flow
Start -> Read number n -> n % 2 == 0?
n % 2 == 0? -(yes)-> Print "even" -> End
n % 2 == 0? -(no)-> Print "odd" -> End
```  
**Code**:  
```python  
# This code is not for a linked list, but for checking even or odd numbers.  
n = 5  
if n % 2 == 0:  
    print("even")  
else:  
    print("odd")  
```  
**Step by step**:  
- The code starts with a number `n = 5`.  
- It checks if `n % 2 == 0` (if the number is even).  
- Since 5 is not even, it prints "odd".  
**Common mistake**: Beginners might think a linked list is like a list in Python, but a linked list is different because each part only knows the next part.  
**Try it**: Can you think of another example where a linked list might be useful, like a playlist of songs?

## ds04 Data structures
Q: How does a hash table work?
checks failed: [('technical_accuracy', "any of ['collision']", '')]

**Idea**: A hash table is like a special box that stores things (like your favorite snacks) using a secret code (hash). This code helps find the snack quickly, like finding your favorite chocolate in a candy jar.  
**Visual**:  
```flow
Start -> Calculate hash code -> Use hash code to find slot -> Insert item -> End
```  
**Code**:  
```python
# Create a simple hash table using a dictionary
hash_table = {}

# Add items to the hash table
hash_table["apple"] = 1
hash_table["banana"] = 2
hash_table["cherry"] = 3

# Get an item from the hash table
print(hash_table["banana"])  # Output: 2
```  
**Step by step**:  
1. The code creates an empty dictionary (hash table).  
2. It adds items using keys ("apple", "banana", etc.) and values (1, 2, etc.).  
3. When you ask for "banana", the hash table uses the key to find and return the value (2).  
**Common mistake**: Using the same key multiple times can cause overwriting. Always use unique keys.  
**Try it**: Add "date" with value 4 to the hash table and print it.

## ds05 Data structures
Q: Explain binary tree traversal.
checks failed: [('technical_accuracy', "any of ['inorder|in-order|preorder|pre-order|postorder|post-order']", '')]

**Idea**: Binary tree traversal is a way to visit all nodes in a tree. One common way is to go left first, then right. Imagine a tree with a root, and you check the left branch first, then the right branch.  
**Visual**:  
```flow
Start -> Read root -> root.left? -(yes)-> Check left -> root.left? -(no)-> Check right -> End
```  
**Code**:  
```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def traverse(root):
    if root is None:
        return
    print(root.value)
    traverse(root.left)
    traverse(root.right)

# Example tree: 1 is root, 2 is left, 3 is right
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
traverse(root)
```  
**Step by step**:  
1. The function starts with the root node.  
2. It prints the value of the root.  
3. Then it calls itself with the left child.  
4. This repeats until there are no more left children.  
5. Then it goes to the right child and repeats the process.  
**Common mistake**: Forgetting to check if the node is `None` can cause an error. Always add a check for `None`.  
**Try it**: Create a tree with 4 as root, 5 as left, and 6 as right. What will the traversal print?

## so01 Sorting and searching
Q: How does bubble sort work?
checks failed: [('visual_correctness', 'valid sim: bubble_sort', '')]

**Idea**: Bubble sort is like comparing pairs of friends in a line and swapping them if they are not in the right order. We keep doing this until the whole line is sorted. For example, if we have friends named Aman, Bhavik, and Chintan, we compare Aman and Bhavik first. If Bhavik is smaller, we swap them. Then we move to Bhavik and Chintan, and so on.

**Visual**:
```flow
Start -> Read list -> Compare first two elements -> Are they in order? -(no)-> Swap -> Move to next pair -> Are all elements in order? -(no)-> Repeat -> End
```

**Code**:
```python
# Bubble sort example
my_list = [5, 2, 8, 1, 3]
for i in range(len(my_list)):
    for j in range(len(my_list) - 1):
        if my_list[j] > my_list[j + 1]:
            my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]
print(my_list)
```

**Step by step**:
1. The first `for` loop runs for the number of elements in the list.
2. The second `for` loop compares each pair of adjacent elements.
3. If the first element is greater than the second, they are swapped.
4. This process repeats until the entire list is sorted.

**Common mistake**: Beginners often forget to use `range(len(my_list) - 1)` in the inner loop, which causes an index error. Make sure the inner loop stops one element before the end.

**Try it**: Try changing the list to `[9, 3, 1, 7, 5]` and see what happens. Can you predict the final sorted list?

## so02 Sorting and searching
Q: Selection sort samjhao.
checks failed: [('visual_correctness', 'valid sim: selection_sort', '')]

**Idea**: Selection sort is a way to sort things by finding the smallest item and putting it in the right place, then repeating for the next smallest. Like arranging your books in order by picking the smallest book first.  
**Visual**:  
```flow
Start -> Read list -> Find smallest -> Swap -> Repeat -> End
```  
**Code**:  
```py
# Selection sort example
numbers = [5, 2, 9, 1, 5]
for i in range(len(numbers)):
    min_index = i
    for j in range(i + 1, len(numbers)):
        if numbers[j] < numbers[min_index]:
            min_index = j
    numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
print(numbers)
```  
**Step by step**:  
1. Start with the list `[5, 2, 9, 1, 5]`.  
2. Find the smallest number (1) and swap it with the first position. List becomes `[1, 2, 9, 5, 5]`.  
3. Move to the next position (index 1). Find the smallest number in the rest of the list (2) and swap it with index 1. List remains `[1, 2, 9, 5, 5]`.  
4. Move to index 2. Find the smallest number in the rest of the list (5) and swap it with index 2. List becomes `[1, 2, 5, 9, 5]`.  
5. Repeat until the list is sorted.  
**Common mistake**: Forgetting to update the `min_index` correctly when a smaller number is found. Fix: Always update `min_index` when a smaller number is found.  
**Try it**: Sort the list `[7, 3, 8, 1, 4]` using selection sort. What will the list look like after the first swap?

## so03 Sorting and searching
Q: Explain insertion sort.
checks failed: [('visual_correctness', 'valid sim: insertion_sort', '')]

**Idea**: Insertion sort is like arranging cards in your hand. You take one card at a time and place it in the correct position among the ones you've already sorted. For example, if you're sorting numbers on a table, you pick up one number and put it where it belongs among the others.

**Visual**:
```flow
Start -> Read number n -> n % 2 == 0?
n % 2 == 0? -(yes)-> Print "even" -> End
n % 2 == 0? -(no)-> Print "odd" -> End
```

**Code**:
```python
# Insertion sort example with numbers
numbers = [5, 2, 9, 1, 5]
for i in range(1, len(numbers)):
    key = numbers[i]
    j = i - 1
    while j >= 0 and numbers[j] > key:
        numbers[j + 1] = numbers[j]
        j -= 1
    numbers[j + 1] = key
print(numbers)
```

**Step by step**:
1. Start with the first number (5) as the sorted part.
2. Take the next number (2) and compare it with 5. Since 2 is smaller, move 5 to the right and place 2 in the correct position.
3. Take the next number (9) and compare it with the sorted part (2, 5). Since 9 is larger, it stays at the end.
4. Take the next number (1) and compare it with 2, 5, and 9. Move all larger numbers to the right and place 1 at the beginning.
5. Take the last number (5) and compare it with the sorted part (1, 2, 5, 9). Since it's already in the correct position, no changes are needed.

**Common mistake**: Beginners often try to move numbers directly to their correct position without shifting others. Fix: Always shift larger numbers to the right before placing the current number.

**Try it**: Sort the list [8, 3, 6, 2, 9] using insertion sort. What is the final sorted list?

## so04 Sorting and searching
Q: Binary search samjhao.
checks failed: [('visual_correctness', 'valid sim: binary_search', '')]

**Idea**: Binary search is a fast way to find a number in a sorted list. Imagine you have a list of cricket scores and you want to find if a particular score exists. You start by checking the middle score, then decide to look in the higher or lower half.

**Visual**:
```flow
Start -> Read number n -> n % 2 == 0?
n % 2 == 0? -(yes)-> Print "even" -> End
n % 2 == 0? -(no)-> Print "odd" -> End
```

**Code**:
```python
# Binary search to find if a number exists in a sorted list
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False

# Example list of cricket scores
cricket_scores = [12, 25, 38, 50, 65, 80, 95]
print(binary_search(cricket_scores, 50))
```

**Step by step**:
1. Start with the full list of scores.
2. Find the middle score and check if it matches the target.
3. If it matches, the number is found.
4. If it's less than the target, search the higher half.
5. If it's more than the target, search the lower half.
6. Repeat until the number is found or the list is exhausted.

**Common mistake**: Forgetting to sort the list before using binary search. Binary search only works on sorted lists.

**Try it**: Change the target score to 80 and see if the code finds it.

## so05 Sorting and searching
Q: Explain linear search.
checks failed: none

**Idea**: Linear search checks each item in a list one by one until it finds what you're looking for. For example, you might search for a book in a shelf by checking each book one by one.

**Visual**:
```sim
{"algo": "linear_search", "input": [10, 20, 30, 40, 50], "target": 30}
```

**Code**:
```python
# List of numbers
numbers = [10, 20, 30, 40, 50]

# What we are looking for
target = 30

# Check each number in the list
for number in numbers:
    if number == target:
        print("Found it!")
        break
```

**Step by step**:
1. The code starts with a list of numbers.
2. It checks each number in the list one by one.
3. If the number matches the target, it prints "Found it!" and stops checking.
4. If it goes through all numbers and doesn't find the target, it just ends without printing anything.

**Common mistake**: Forgetting to use `break` after finding the target can make the code check unnecessary items, which is slower.

**Try it**: Change the target to 40 and see what happens. What message do you get?

## so06 Sorting and searching
Q: What is the time complexity of merge sort and why?
checks failed: [('technical_accuracy', "any of ['n\\\\s*log\\\\s*n|O\\\\(n log n\\\\)']", '')]

**Idea**: Merge sort splits a list into smaller parts, sorts them, and merges them. It works quickly even for big lists, like sorting many books on a shelf.  
**Visual**:  
```flow
Start -> Split list into halves -> Sort each half -> Merge sorted halves -> End
```  
**Code**:  
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```  
**Step by step**:  
1. The list is split into halves until each part has 1 item.  
2. Each small list is sorted (already sorted).  
3. The sorted halves are merged by comparing items from each.  
4. This process repeats until the whole list is sorted.  
**Common mistake**: Beginners think merge sort is faster than other sorts, but it has the same time complexity as quicksort in average cases.  
**Try it**: Sort a list of 10 numbers using merge sort and see how it works.

## sq01 SQL
Q: Explain SELECT and WHERE in SQL.
checks failed: none

**Idea**: SELECT and WHERE are used to get specific data from a table. For example, you can use SELECT to get only the names of students and WHERE to find students who scored more than 80 in a test.

**Visual**:
```flow
Start -> Read table -> SELECT column -> WHERE condition -> Show result -> End
```

**Code**:
```sql
-- Example: Get names of students who scored more than 80
SELECT name FROM students WHERE score > 80;
```

**Step by step**:
- `SELECT name` tells the database to get the `name` column.
- `FROM students` tells the database to look in the `students` table.
- `WHERE score > 80` filters the rows to only those where the `score` is greater than 80.

**Common mistake**: Forgetting to use `WHERE` when you need to filter data. Always use `WHERE` if you want to get only specific rows.

**Try it**: Write a query to get the names of students who scored less than 50.

## sq02 SQL
Q: Explain SQL INNER JOIN to a beginner.
checks failed: [('visual_correctness', 'markdown table', '')]

**Idea**: SQL INNER JOIN combines rows from two tables where the values in a specific column match. For example, if you have a table of students and a table of their grades, INNER JOIN will show only the students who have grades.  

**Visual**:  
```flow
Start -> Read table1 -> Read table2 -> Match rows -> Show matched rows -> End
```  

**Code**:  
```sql
SELECT students.name, grades.score
FROM students
INNER JOIN grades ON students.id = grades.student_id;
```
This code selects the student names and their scores from the `students` and `grades` tables where the `id` in `students` matches the `student_id` in `grades`.  

**Step by step**:  
1. The `SELECT` statement picks the columns you want to see (name and score).  
2. The `FROM students` part starts with the `students` table.  
3. The `INNER JOIN grades` part connects the `students` table with the `grades` table.  
4. The `ON students.id = grades.student_id` part tells SQL which columns to match.  
5. SQL combines the rows where the `id` in `students` matches the `student_id` in `grades`.  

**Common mistake**: Forgetting to use `ON` with the matching columns. Always specify which columns to match.  

**Try it**: Write a query to find the names of students and their scores using INNER JOIN. Make sure to match the correct columns.

## sq03 SQL
Q: Explain GROUP BY with an example.
checks failed: none

**Idea**: GROUP BY is used to group rows that have the same values in a column. For example, if you have a list of students and their favorite subjects, you can use GROUP BY to find out how many students like each subject.

**Visual**:
```flow
Start -> Read data -> Group by subject -> Count students -> Show results -> End
```

**Code**:
```python
# List of students and their favorite subjects
students = [
    ("Alice", "Math"),
    ("Bob", "Science"),
    ("Charlie", "Math"),
    ("David", "Science"),
    ("Eve", "Math")
]

# Group by subject and count students
from collections import defaultdict

subject_counts = defaultdict(int)
for student, subject in students:
    subject_counts[subject] += 1

print(subject_counts)
```

**Step by step**:
1. We start with a list of students and their favorite subjects.
2. We use a dictionary to count how many times each subject appears.
3. For each student, we look at their subject and increase the count for that subject in the dictionary.
4. Finally, we print the dictionary, which shows how many students like each subject.

**Common mistake**: Forgetting to import the `defaultdict` from the `collections` module can cause an error. Always make sure to import it if you're using it.

**Try it**: Modify the code to count how many students like "English" instead of "Math". What changes do you need to make?

## sq04 SQL
Q: What is the difference between a primary key and a foreign key?
checks failed: none

**Idea**: A primary key is a special field in a table that uniquely identifies each row. A foreign key is a field that links to the primary key of another table. For example, in a school, the student ID is a primary key in the students table, and the class ID in the attendance table is a foreign key that links to the class ID in the classes table.

**Visual**:
```
Students Table        Classes Table
+----------------+     +----------------+
| Student ID     |     | Class ID       |
| Name           |     | Class Name     |
|----------------|     |----------------|
| 1              |     | 101            |
| 2              |     | 102            |
+----------------+     +----------------+
```

**Code**: 
```python
# Example of primary and foreign keys in Python (simulating a database)
students = {
    1: {"name": "Alice"},
    2: {"name": "Bob"}
}

classes = {
    101: {"name": "Math"},
    102: {"name": "Science"}
}

attendance = {
    1: {"class_id": 101},
    2: {"class_id": 102}
}
```

**Step by step**: 
- The `students` dictionary uses `Student ID` as the primary key to uniquely identify each student.
- The `classes` dictionary uses `Class ID` as the primary key to uniquely identify each class.
- The `attendance` dictionary uses `class_id` as a foreign key, linking each student to a class in the `classes` table.

**Common mistake**: 
- Beginners often confuse primary and foreign keys. Remember, a primary key is unique to its table, while a foreign key links to another table's primary key.

**Try it**: 
- Create a `teachers` table with a primary key `Teacher ID` and a `subject` field. Then, create a `teaching` table with a foreign key `teacher_id` that links to the `Teacher ID` in the `teachers` table.

## os01 Operating systems
Q: What is the difference between a process and a thread?
checks failed: none

**Idea**: A process is like a separate tea cup in the canteen. Each has its own tea and spoon. A thread is like a spoon in the same cup—shares the tea but uses the spoon differently.  
**Visual**:  
```flow
Start -> Process: Separate cup with tea and spoon -> Thread: Same cup, different spoon -> End
```  
**Code**:  
```python  
# Processes and threads are different in Python  
# Processes use multiprocessing, threads use threading  
import multiprocessing  
import threading  

def tea():  
    print("Tea is ready!")  

if __name__ == "__main__":  
    # Process: Runs in separate memory  
    p = multiprocessing.Process(target=tea)  
    p.start()  
    p.join()  

    # Thread: Shares memory with main program  
    t = threading.Thread(target=tea)  
    t.start()  
    t.join()  
```  
**Step by step**:  
- The `multiprocessing.Process` creates a new process, which runs the `tea` function in its own memory.  
- The `threading.Thread` creates a new thread, which runs the `tea` function but shares memory with the main program.  
**Common mistake**: Beginners think threads are faster than processes, but threads are slower because they share memory and can cause conflicts.  
**Try it**: Run the code and see what happens. Can you tell the difference between the process and thread output?

## os02 Operating systems
Q: What is a deadlock and what are the conditions for it?
checks failed: [('technical_accuracy', 'require mutual exclusion', ''), ('technical_accuracy', 'require hold and wait', ''), ('technical_accuracy', 'require no preemption', ''), ('teaching_quality', 'six-part format, pictures and code are valid', 'no code block with a language tag')]

**Idea**: A deadlock is when two or more programs are stuck waiting for each other to finish. Imagine two friends waiting for each other to pass a ball in a game.  
**Visual**:  
```flow
Start -> Friend A waits for Friend B -> Friend B waits for Friend A -> Deadlock -> End
```  
**Code**: Not applicable (deadlock is a concept, not a code example).  
**Step by step**: Deadlock happens when each program holds a resource and waits for another. It’s like a circular wait where no one can move.  
**Common mistake**: Thinking that a single program can cause a deadlock. Fix: Deadlock needs at least two programs or processes.  
**Try it**: Can you think of a real-life situation where a deadlock might happen?

## os03 Operating systems
Q: Explain Round Robin CPU scheduling.
checks failed: none

**Idea**: Round Robin is a way to share a computer's time among many tasks. Each task gets a small slice of time to run, like taking turns drinking chai from a shared pot.  
**Visual**:  
```flow
Start -> Add tasks to queue -> Pick first task -> Run for time slice -> Check if task done?
Run for time slice -(no)-> Add task to end of queue -> Repeat
Run for time slice -(yes)-> Remove task -> End
```  
**Code**:  
```python
# Simulate Round Robin scheduling with 3 tasks and a time slice of 2
tasks = ["Task1", "Task2", "Task3"]
time_slice = 2
current_time = 0

while tasks:
    task = tasks.pop(0)
    print(f"Running {task} for {time_slice} units")
    current_time += time_slice
    if current_time >= 6:  # Simulate task completion after 6 units
        print(f"{task} completed")
    else:
        tasks.append(task)
```  
**Step by step**:  
1. The code starts with a list of tasks and a time slice of 2 units.  
2. It picks the first task and runs it for 2 units.  
3. If the task hasn't finished (current_time < 6), it is added back to the end of the queue.  
4. This repeats until all tasks are completed.  
**Common mistake**: Forgetting to add the task back to the queue if it hasn't finished. Fix: Always append the task to the queue after running it.  
**Try it**: Change the time slice to 3 and see how the order of tasks changes.

## os04 Operating systems
Q: Paging versus segmentation: what is the difference?
checks failed: none

**Idea**: Paging and segmentation are ways to manage memory. Paging divides memory into fixed-size blocks, while segmentation divides it into variable-size blocks based on logical units like programs or data. For example, a cricket team's gear (bat, ball, helmet) is like segmentation—each item is a different size. Paging is like dividing a bus into fixed seats.

**Visual**:
```flow
Start -> Read number n -> n % 2 == 0?
n % 2 == 0? -(yes)-> Print "even" -> End
n % 2 == 0? -(no)-> Print "odd" -> End
```

**Code**:  
```python
# No code needed for this concept. It's more about understanding memory management.
```

**Step by step**:  
- Paging divides memory into fixed-size blocks called pages. Each page is assigned to a process.  
- Segmentation divides memory into variable-sized blocks called segments, based on logical units like code, data, or stack.  
- Both help manage memory, but paging is simpler and more efficient for modern systems.

**Common mistake**:  
- Confusing pages with segments. Pages are fixed size, segments vary in size.  
- Thinking segmentation is only for programs, but it can also be used for data like a canteen's menu (different sections for different items).

**Try it**:  
- Think of two ways to organize your school bag: one with fixed-sized compartments (paging) and one with sections for different subjects (segmentation). Which is easier to manage?

## nn01 Neural networks
Q: Why can't a single perceptron learn XOR?
checks failed: [('technical_accuracy', 'require hidden', '')]

**Idea**: A single perceptron can only learn simple patterns, like straight lines. XOR is a tricky pattern that needs a more complex setup.  
**Visual**:  
```flow
Start -> Read input (0,0) -> Perceptron gives 0 -> End
Read input (0,1) -> Perceptron gives 1 -> End
Read input (1,0) -> Perceptron gives 1 -> End
Read input (1,1) -> Perceptron gives 0 -> End
```  
**Code**:  
```python
# This code shows how a single perceptron can't learn XOR
# We use a simple model with weights and a threshold
weights = [0.5, 0.5]
threshold = 1

def perceptron(input1, input2):
    total = input1 * weights[0] + input2 * weights[1]
    return 1 if total >= threshold else 0

print(perceptron(0, 0))  # Should be 0
print(perceptron(0, 1))  # Should be 1
print(perceptron(1, 0))  # Should be 1
print(perceptron(1, 1))  # Should be 0
```  
**Step by step**:  
1. The perceptron uses weights and a threshold to decide the output.  
2. For inputs (0,0), the total is 0, which is less than the threshold, so it returns 0.  
3. For inputs (0,1), the total is 0.5, which is less than the threshold, so it returns 1.  
4. For inputs (1,0), the total is 0.5, which is less than the threshold, so it returns 1.  
5. For inputs (1,1), the total is 1.0, which is equal to the threshold, so it returns 0.  
**Common mistake**: Beginners might think the perceptron can learn XOR by adjusting weights, but it can't because the pattern is not linear.  
**Try it**: Can you adjust the weights and threshold to make the perceptron return the correct output for all four cases?

## nn02 Neural networks
Q: Explain gradient descent.
checks failed: [('technical_accuracy', 'require loss', '')]

**Idea**: Gradient descent is a way to find the best answer to a problem by moving step by step in the direction that makes things better. Imagine you are on a mountain and want to reach the bottom. You look around and take small steps downhill until you reach the lowest point.

**Visual**:
```flow
Start -> Calculate slope -> Move in direction of steepest descent -> Check if slope is close to zero? -> If yes, stop -> If no, repeat -> End
```

**Code**:
```python
# Simple example of gradient descent for a function
def gradient_descent(start, learning_rate, steps):
    current = start
    for _ in range(steps):
        gradient = 2 * current  # Example gradient for function f(x) = x^2
        current -= learning_rate * gradient
    return current

result = gradient_descent(10, 0.1, 100)
print(result)
```

**Step by step**:
1. Start at a point (like being on a mountain).
2. Calculate the slope (like looking around to see which way is downhill).
3. Move a small step in the direction that reduces the slope (like taking a step downhill).
4. Repeat until the slope is very small (like reaching the bottom of the mountain).

**Common mistake**: Using a learning rate that is too big or too small. If it's too big, you might overshoot the minimum. If it's too small, it might take too long to reach the minimum.

**Try it**: Change the learning rate and number of steps in the code and see how the result changes. What happens if you use a learning rate of 0.5 instead of 0.1?

## nn03 Neural networks
Q: Activation function kyu zaroori hota hai?
checks failed: none

**Idea**: Activation function is like a switch in a neuron. It decides whether the neuron should fire or not. For example, in a cricket match, the bowler decides whether to bowl a good ball or not based on the situation.  
**Visual**:  
```flow
Start -> Read input -> Activation function -> Output -> End
```  
**Code**:  
```python
# Simple neuron with activation function
input_value = 5
weight = 2
bias = 1
activation_output = input_value * weight + bias  # Linear activation
print(activation_output)
```  
**Step by step**:  
1. `input_value = 5` sets the input to the neuron.  
2. `weight = 2` is like how much the input matters.  
3. `bias = 1` is like a small push to the output.  
4. `activation_output = input_value * weight + bias` calculates the output.  
5. `print(activation_output)` shows the result.  
**Common mistake**: Beginners often forget to use an activation function, which can make the model not learn properly.  
**Try it**: Change the `activation_output` to use a non-linear function like `max(0, input_value * weight + bias)` and see what happens.

## nn04 Neural networks
Q: What is overfitting and how can I detect it?
checks failed: [('teaching_quality', 'six-part format, pictures and code are valid', 'no code block with a language tag')]

**Idea**: Overfitting is when a model learns the training data too well, including noise and details that don't help with new data. For example, if you train a model to recognize cats using only pictures of cats with green backgrounds, it might fail to recognize cats on a normal background.

**Visual**:
```flow
Start -> Train model on data -> Model memorizes data? -(yes)-> Overfitting -> End
Model memorizes data? -(no)-> Generalizes well -> End
```

**Code**:  
No code example for overfitting, as it is a concept, not a direct coding task.

**Step by step**:  
Overfitting happens when a model learns the training data too well, including noise and irrelevant patterns. This makes the model perform well on the training data but poorly on new, unseen data. To detect overfitting, compare the model's performance on the training data and a separate test dataset. If the model performs much better on the training data than on the test data, it is likely overfitting.

**Common mistake**:  
Using a model that is too complex for the data, or not having enough training data, can lead to overfitting. To fix this, simplify the model or use more data.

**Try it**:  
Train a model on a small dataset and test it on a different dataset. If the model performs much better on the training data, it might be overfitting. What can you do to improve this?

## tf01 Transformers
Q: Explain attention in a Transformer simply.
checks failed: none

**Idea**: Attention is like when you focus on one thing in a group. In a Transformer, it helps the model focus on important words in a sentence. For example, when you read "The cat sat on the mat," attention helps the model focus on "cat" when it sees "sat."

**Visual**:
```flow
Start -> Read sentence -> Split into words -> Use attention to focus on key words -> Make meaning -> End
```

**Code**:  
```python
# This is a simple example of attention in code
words = ["The", "cat", "sat", "on", "the", "mat"]
attention_weights = [0.1, 0.4, 0.3, 0.1, 0.05, 0.05]
print("Attention weights:", attention_weights)
```

**Step by step**:  
- The code starts by reading a sentence and splitting it into words.  
- It then assigns attention weights to each word, which show how much focus the model should give to each word.  
- The weights add up to 1, meaning the model is focusing on all words but giving more attention to some.  
- The model uses these weights to understand the sentence better.

**Common mistake**:  
- Beginners might think attention is about choosing one word, but it's actually about giving different levels of focus to all words.

**Try it**:  
- Change the attention weights to give more focus to "cat" and "mat." What happens to the weights?

## tf02 Transformers
Q: Is GPT an encoder-decoder model? Compare it with the original Transformer.
checks failed: [('teaching_quality', 'six-part format, pictures and code are valid', 'no code block with a language tag')]

**Idea**: GPT is a decoder-only model, while the original Transformer is encoder-decoder. Both use attention, but GPT only uses the decoder part for generating text.

**Visual**:
```flow
Start -> Read model type -> Is it GPT? -(yes)-> Use decoder only -> End
Is it GPT? -(no)-> Use encoder-decoder -> End
```

**Code**:  
No code needed for this comparison. We use concepts instead.

**Step by step**:  
- The original Transformer has both encoder and decoder parts. The encoder processes input, and the decoder uses that to generate output.  
- GPT uses only the decoder part. It takes input and generates output step by step, like writing a story.

**Common mistake**:  
People often think all Transformers are encoder-decoder, but GPT is decoder-only. Always check if the model is GPT or the original Transformer.

**Try it**:  
Can you explain why GPT is good for tasks like writing stories or answering questions?

## tf03 Transformers
Q: What are tokens and embeddings in LLMs?
checks failed: none

**Idea**: Tokens are the smallest units of text that LLMs understand, like words or parts of words. Embeddings are special numbers that show how tokens are related to each other in meaning.  
**Visual**:  
```flow
Start -> Split text into tokens -> Convert tokens to embeddings -> Use embeddings to understand meaning -> End
```  
**Code**:  
```python
# Example: Tokenizing and converting to embeddings (using a simple mock)
tokens = ["hello", "world"]
embeddings = [ [0.1, 0.2], [0.3, 0.4] ]  # Mock embeddings
print("Tokens:", tokens)
print("Embeddings:", embeddings)
```  
**Step by step**:  
- `tokens = ["hello", "world"]`: Split the text into individual words.  
- `embeddings = [ [0.1, 0.2], [0.3, 0.4] ]`: Assign special numbers to each token to show their meaning.  
- `print("Tokens:", tokens)`: Show the tokens.  
- `print("Embeddings:", embeddings)`: Show the embeddings.  
**Common mistake**: Thinking tokens are the same as words. Tokens can be parts of words or special symbols.  
**Try it**: Split the sentence "I love chai" into tokens. What would their embeddings look like?

## db01 Debugging
Q: My loop gives IndexError: list index out of range on nums[i+1]. Why?
checks failed: [('technical_accuracy', 'require IndexError', '')]

**Idea**: This error happens when you try to access an element in a list that doesn't exist. It often happens when you use a loop that goes beyond the list's length.

**Visual**:
```flow
Start -> Read list nums -> i from 0 to len(nums)-1 -> Check nums[i+1] -> i+1 >= len(nums)? -(yes)-> Error -> End
```

**Code**:
```python
nums = [1, 2, 3]
for i in range(len(nums)):
    print(nums[i+1])
```

**Step by step**:
- The loop runs for `i` from 0 to 2 (since `len(nums)` is 3).
- When `i` is 2, `i+1` is 3, which is equal to `len(nums)`, so it tries to access `nums[3]`, which doesn't exist.

**Common mistake**: Forgetting that the last index of a list is `len(nums) - 1`, so `i+1` can go out of range.

**Try it**: Fix the code so it doesn't give an error. What should the loop condition be?

## db02 Debugging
Q: What does NameError: name 'total' is not defined mean?
checks failed: none

**Idea**: This error happens when you try to use a variable that hasn't been created yet. Like trying to drink chai from an empty cup.

**Visual**:
```flow
Start -> Assign total = 0 -> Add 5 to total -> Print total -> End
```

**Code**:
```py
# This code will cause a NameError
print(total)
```

**Step by step**: The code tries to print `total`, but `total` hasn't been defined yet. Python doesn't know what `total` is, so it throws an error.

**Common mistake**: Forgetting to define a variable before using it. Always make sure to create variables before you try to use them.

**Try it**: Write a program that adds 10 to a variable called `score`. What happens if you try to print `score` before you assign it?

## db03 Debugging
Q: Why does print('Age: ' + 25) fail?
checks failed: [('technical_accuracy', 'require TypeError', ''), ('teaching_quality', 'six-part format, pictures and code are valid', 'no picture: add a flow/chart/array/vars block or a table')]

**Idea**: In Python, you can't add a string and a number directly. You need to convert the number to a string first, like telling your friend to say "Age: 25" instead of trying to mix a sentence with a number.

**Visual**:
```
"Age: " + 25
        ❌
```

**Code**:
```python
# This code will cause an error
print('Age: ' + 25)
```

**Step by step**:
- The code tries to add a string `'Age: '` with the number `25`.
- Python doesn't know how to mix strings and numbers like that.
- It throws an error because you can't add a string and a number directly.

**Common mistake**:
- Forgetting to convert the number to a string using `str()`.

**Try it**:
- Fix the code by converting `25` to a string. What should you write instead of `25`?

## db04 Debugging
Q: My while loop never ends: i = 0, while i < 5: print(i). Why?
checks failed: [('technical_accuracy', "any of ['i\\\\s*\\\\+=\\\\s*1|i\\\\s*=\\\\s*i\\\\s*\\\\+\\\\s*1|increment']", '')]

**Idea**: Your loop runs as long as `i` is less than 5. But `i` never increases, so it keeps printing 0 forever.  
**Visual**:  
```flow
Start -> Read i = 0 -> i < 5? -(yes)-> Print i -> i < 5? -(loop)
```  
**Code**:  
```py
i = 0
while i < 5:
    print(i)
```  
**Step by step**:  
1. `i` is set to 0.  
2. The loop checks if `i < 5` (yes, 0 < 5).  
3. It prints 0.  
4. The loop checks again if `i < 5` (still yes).  
5. It keeps printing 0 forever because `i` never changes.  
**Common mistake**: Forgetting to update the loop condition variable (`i`).  
**Try it**: Add a line to increase `i` by 1 each time. What happens?

## vz01 Visual correctness
Q: Show the Big-O growth for n = 16 as a chart.
checks failed: [('teaching_quality', 'six-part format, pictures and code are valid', 'no code block with a language tag')]

**Idea**: Big-O shows how long a task takes as the input size (n) grows. For n = 16, we see how different algorithms scale.  
**Visual**:  
```complexity
{"n": 16, "curves": ["1", "log n", "n", "n^2"]}
```  
**Code**:  
No code needed. The app calculates and shows the Big-O growth.  
**Step by step**: The app uses the complexity chart to show how many steps each algorithm takes for n = 16.  
**Common mistake**: Beginners often confuse Big-O with exact time, but it's about growth, not exact numbers.  
**Try it**: Press play on the chart to see how the steps grow for n = 16.

## vz02 Visual correctness
Q: Draw a flowchart for checking whether a number is prime.
checks failed: none

**Idea**: A prime number is a number that has only two factors: 1 and itself. For example, 7 is prime because it can only be divided by 1 and 7. We check if any number between 2 and the number itself divides it evenly.

**Visual**:
```flow
Start -> Read number n -> n < 2? -(yes)-> Print "not prime" -> End
n < 2? -(no)-> i = 2 -> i > sqrt(n)? -(yes)-> Print "prime" -> End
i > sqrt(n)? -(no)-> n % i == 0? -(yes)-> Print "not prime" -> End
n % i == 0? -(no)-> i = i + 1 -> Repeat
```

**Code**:
```python
import math

n = 7
is_prime = True
for i in range(2, int(math.sqrt(n)) + 1):
    if n % i == 0:
        is_prime = False
        break
print("Prime" if is_prime else "Not prime")
```

**Step by step**:
1. Read the number `n`.
2. If `n` is less than 2, it is not prime.
3. Start a loop from 2 to the square root of `n`.
4. Check if `n` is divisible by the current number `i`.
5. If it is divisible, mark it as not prime and stop the loop.
6. If the loop finishes without finding a divisor, the number is prime.

**Common mistake**: Beginners often check up to `n` instead of the square root of `n`, which makes the code slower. Use `sqrt(n)` to make it faster.

**Try it**: Change the value of `n` to 15 and see what the code outputs. What happens if you try `n = 2`?

## vz03 Visual correctness
Q: Show how two Python names can point to the same list.
checks failed: none

**Idea**: Two Python names can point to the same list. For example, if you have a list of your favorite snacks, you can call it "snacks" and also call it "my_snacks" if you want.

**Visual**:
```vars
{"title": "Names and objects", "vars": [{"name": "a", "value": "[1, 2]"}, {"name": "b", "same_as": "a"}]}
```

**Code**:
```python
# Create a list of favorite snacks
snacks = [1, 2]

# Make another name point to the same list
my_snacks = snacks

# Show the list using both names
print(snacks)       # Output: [1, 2]
print(my_snacks)    # Output: [1, 2]
```

**Step by step**:
- `snacks = [1, 2]` creates a list and assigns the name "snacks" to it.
- `my_snacks = snacks` makes the name "my_snacks" point to the same list as "snacks".
- `print(snacks)` and `print(my_snacks)` both show the same list because they point to the same object.

**Common mistake**: Beginners might think that `my_snacks = snacks` makes a copy of the list, but it actually makes both names point to the same list.

**Try it**: Change the list using one name and check if the other name shows the same change.

## ad01 Adaptive tutoring
Q: Quiz me on Python for loops. Ask one question at a time and do not give the answer.
checks failed: none

**Question**: Which keyword is used to exit a for loop early in Python?  
A) break  
B) exit  
C) stop  
D) end

## ad02 Adaptive tutoring
Q: I think it prints 1 2 3.
checks failed: none

**Idea**: This code prints numbers from 0 to 2 because `range(3)` gives 0, 1, 2.  
**Visual**:  
```flow
Start -> Read number 3 -> Loop from 0 to 2 -> Print each number -> End
```  
**Code**:  
```python
for i in range(3):  
    print(i)  
# range(3) gives 0, 1, 2  
```  
**Step by step**:  
1. The loop starts with `i = 0`.  
2. It prints `0`, then `i` becomes `1`.  
3. It prints `1`, then `i` becomes `2`.  
4. It prints `2`, then `i` becomes `3`, and the loop stops.  
**Common mistake**: People often think `range(3)` starts at 1, but it starts at 0.  
**Try it**: What happens if you change `range(3)` to `range(5)`?

## ad03 Adaptive tutoring
Q: Ab ek question do.
checks failed: none

**Question**: Kya `for` loop ka use karte waqt `range()` ka use karna zaroori hai?

## pv01 Privacy and context
Q: Explain bubble sort.
checks failed: [('visual_correctness', 'valid sim: bubble_sort', '')]

**Idea**: Bubble sort is a way to sort numbers like arranging books on a shelf. It compares pairs of numbers and swaps them if they are in the wrong order, like moving a heavier book to the right.  
**Visual**:  
```flow
Start -> Read list -> Compare first two elements -> Are they in wrong order?
Are they in wrong order? -(yes)-> Swap them -> Go back to compare first two elements
Are they in wrong order? -(no)-> Move to next pair -> Are there more pairs?
Are there more pairs? -(no)-> End
```  
**Code**:  
```python
# Bubble sort example with numbers [5, 2, 9, 1]
numbers = [5, 2, 9, 1]
for i in range(len(numbers)):
    for j in range(len(numbers) - 1):
        if numbers[j] > numbers[j + 1]:
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
print(numbers)
```  
**Step by step**:  
1. The first loop runs for each number in the list.  
2. The second loop compares each pair of numbers.  
3. If the first number is bigger than the second, they swap places.  
4. This continues until the whole list is sorted.  
**Common mistake**: Forgetting to update the second loop to stop at the end of the list. Fix it by using `len(numbers) - 1` in the second loop.  
**Try it**: Sort the list [3, 1, 4, 2] using bubble sort. What happens to the numbers after each pass?

## pv02 Privacy and context
Q: Teach me recursion.
checks failed: none

**Idea**: Recursion is when a function calls itself to solve a smaller part of a problem. For example, counting down from 10 to 0 by calling the function with 9, then 8, and so on.

**Visual**:
```flow
Start -> Call function -> n > 0?
n > 0? -(yes)-> Print n -> Call function with n-1 -> End
n > 0? -(no)-> End
```

**Code**:
```python
def count_down(n):
    if n > 0:
        print(n)
        count_down(n - 1)
```

**Step by step**: 
- The function `count_down` takes a number `n`.
- If `n` is greater than 0, it prints `n` and calls itself with `n - 1`.
- This continues until `n` is 0, and the function stops.

**Common mistake**: Forgetting to include a base case that stops the recursion. This leads to infinite loops and crashes the program.

**Try it**: Modify the code to count up from 1 to 10 instead of counting down.

## pv03 Privacy and context
Q: What do you know about me?
checks failed: none

Idea: I don't know anything about you yet. We can learn together as we chat and code.  
Visual:  
```flow
Start -> Ask question -> Learn about you -> Continue
```  
Code:  
```python  
# This code does nothing because we are just getting to know each other  
# We will write real code soon!  
```  
Step by step:  
- The code is empty because we are just starting.  
- We will write code together once we know more about each other.  
Common mistake: Thinking I already know you.  
Try it: Tell me something about yourself!
