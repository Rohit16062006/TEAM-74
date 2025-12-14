
KNOWLEDGE_BASE = {
    # --------------------------------------------------------------------------------
    # SQL & DATABASES
    # --------------------------------------------------------------------------------
    "Write a query to find the second highest salary.": 
        """
🏆 **Concept:** Subqueries, OFFSET, and Aggregate Functions.

**Understanding the Problem:**
You need to find the salary that is strictly less than the maximum salary but greater than all others below it.

**Method 1: Using Subquery (Universal Approach)**
We first find the maximum salary, then find the maximum salary strictly *less* than that.

```sql
SELECT MAX(salary) 
FROM employees 
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**Method 2: Using LIMIT & OFFSET (MySQL/PostgreSQL)**
Sort salaries in descending order, skip the first one (highest), and take the next one.
```sql
SELECT DISTINCT salary 
FROM employees 
ORDER BY salary DESC 
LIMIT 1 OFFSET 1;
```

**Method 3: Using Window Functions (Advanced)**
Using `DENSE_RANK()` handles cases where multiple employees have the same top salary.
```sql
WITH RankedSalaries AS (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
)
SELECT salary FROM RankedSalaries WHERE rank = 2;
```

**🤔 Critical Thinking Check:**
*   **Edge Case:** What if the table has only 1 record? (Method 1 returns NULL, Method 2 returns empty set).
*   **Duplicate Max:** If two people earn the same top salary, does "Second Highest" mean the same value or the next distinct value? (Use `DISTINCT` or `DENSE_RANK` to be safe).
""",
    
    "Explain the difference between DELETE and TRUNCATE.":
        """
🔥 **DELETE vs TRUNCATE**

| Feature | DELETE | TRUNCATE |
| :--- | :--- | :--- |
| **Type** | DML (Data Manipulation Language) | DDL (Data Definition Language) |
| **Operation** | Scans table and deletes rows one by one. | Deallocates data pages (very fast). |
| **WHERE Clause** | Allowed (`DELETE FROM x WHERE id=1`) | NOT Allowed (Removes ALL rows). |
| **Rollback** | Can be rolled back (if using transaction). | Cannot be rolled back in some DBs (though PostgreSQL allows it in transaction). |
| **Triggers** | Fires `ON DELETE` triggers. | Does NOT fire triggers. |
| **Resets Identity** | No, auto-increment continues. | Yes, resets auto-increment counters. |

**Key Takeaway:** Use `DELETE` when you need conditional removal or trigger execution. Use `TRUNCATE` for fast, complete cleanup.

**🤔 Critical Thinking Check:**
*   **Safety:** Why is TRUNCATE faster? (It logs page deallocations, not individual row deletions).
*   **Scenario:** If you accidentally TRUNCATE a table in Production, can you recover it? (Only from Backups, usually not from Transaction Logs easily).
""",
    
    "Design a schema for a library management system.":
        """
📚 **Library Management System Schema**

**Core Entities & Relationships:**
1.  **Books** (ISBN, Title, Author, Year, Genre)
2.  **Authors** (AuthorID, Name) - *Many-to-Many with Books*
3.  **Members** (MemberID, Name, DateJoined)
4.  **Loans** (LoanID, BookID, MemberID, DueDate, ReturnDate) - *Transaction Table*

**Schema Definition (SQL):**

```sql
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Books (
    BookID INT PRIMARY KEY,
    Title VARCHAR(200),
    ISBN VARCHAR(13) UNIQUE
);

-- Many-to-Many Junction Table
CREATE TABLE Book_Authors (
    BookID INT,
    AuthorID INT,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
);

CREATE TABLE Members (
    MemberID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE
);

CREATE TABLE Loans (
    LoanID INT PRIMARY KEY,
    BookID INT,
    MemberID INT,
    LoanDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);
```

**🤔 Critical Thinking Check:**
*   **Scalability:** How would you handle multiple copies of the same book? (Split `Books` into `Titles` and `PhysicalBook` entities).
*   **History:** How do you track fine payments for overdue books? (Add a `Fines` table linked to `Loans`).
""",
        
    "Write a query to join three tables.":
        """
🔗 **Joining Multiple tables**

**Concept:**
To join 3 tables (A, B, C), you simply chain the `JOIN` clauses.
Assume common scenario: Users -> Orders -> Products.

**Scenario:** Get User Name, Order Date, and Product Name.

```sql
SELECT 
    Users.Name, 
    Orders.OrderDate, 
    Products.ProductName
FROM Users
JOIN Orders 
    ON Users.UserID = Orders.UserID
JOIN OrderDetails
    ON Orders.OrderID = OrderDetails.OrderID
JOIN Products 
    ON OrderDetails.ProductID = Products.ProductID;
```

**Tip:** Always ensure you are joining on the correct Foreign Keys. Use Table Aliases (e.g., `u`, `o`, `p`) for readability.

**🤔 Critical Thinking Check:**
*   **Data Loss:** What happens if a User has no Orders? (Using `JOIN` or `INNER JOIN` will exclude the user. Use `LEFT JOIN` to keep the user).
*   **Performance:** Which table should be first in the FROM clause? (Optimizers handle this, but logical flow matters).
""",
        
    "What is normalization? Explain 1NF, 2NF, 3NF.":
        """
🏗️ **Normalization** is the process of organizing data to reduce redundancy and improve data integrity.

**1NF (First Normal Form)**
*   **Rule:** Atomic columns (no multi-valued attributes like "red,blue,green").
*   **Fix:** Split into new rows or a separate table.
*   **Rule:** Unique rows (Primary Key).

**2NF (Second Normal Form)**
*   **Rule:** Must be in 1NF.
*   **Rule:** No Partial Dependency. All non-key attributes must depend on the *whole* primary key, not just part of it (relevant for composite keys).

**3NF (Third Normal Form)**
*   **Rule:** Must be in 2NF.
*   **Rule:** No Transitive Dependency. Non-key columns shouldn't depend on other non-key columns (e.g., storing `City` based on `ZipCode` in a User table -> move Zip/City to a separate location table).

**🤔 Critical Thinking Check:**
*   **Trade-off:** Why might we *Denormalize*? (To reduce JOIN complexity and improve read performance in analytics/reporting).
*   **Scenario:** Is a JSON column in PostgreSQL normalized? (Technically no, but practically useful).
""",

    # --------------------------------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------------------------------
    "Explain list comprehension with an example.":
        """
🐍 **List Comprehension**

**Definition:** A concise syntax to create lists based on existing lists.
**Syntax:** `[expression for item in iterable if condition]`

**Example 1: Basic**
```python
# Old way
squares = []
for x in range(10):
    squares.append(x**2)

# List Comprehension
squares = [x**2 for x in range(10)]
```

**Example 2: With Condition**
```python
# Get only even numbers
evens = [x for x in range(20) if x % 2 == 0]
```

**Example 3: Nested**
```python
# Flatten a matrix
matrix = [[1,2], [3,4]]
flat = [num for row in matrix for num in row]
# Result: [1, 2, 3, 4]
```

**🤔 Critical Thinking Check:**
*   **Memory:** What if the range is 1 Billion? (List comprehension creates the whole list in memory immediately. Use a **Generator Expression** `(...)` instead to save memory).
*   **Readability:** When should you avoid it? (When the logic is too complex/nested, a for-loop is more readable).
""",
        
    "Write a function to reverse a string without slice.":
        """
🔄 **Reversing a String (Manual Approach)**

**Method 1: Two Pointers (List Swap)**
Strings are immutable in Python, so verify first convert to list.
```python
def reverse_string(s):
    chars = list(s)
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)
```

**Method 2: Acumulator Loop**
```python
def reverse_string(s):
    reversed_s = ""
    for char in s:
        reversed_s = char + reversed_s  # Prepend char
    return reversed_s
```

**Method 3: Built-in (Pythonic)**
`''.join(reversed(s))` - efficient iterator based approach.

**🤔 Critical Thinking Check:**
*   **Type Safety:** What if input is None? (Add a check `if s is None: return None`).
*   **Unicode:** Does this work for emojis/special characters? (Python strings are Unicode, so usually yes, but be careful with grapheme clusters).
""",
    
    "What are decorators in Python?":
        """
🎁 **Decorators**

**Concept:** A design pattern that allows you to modify the behavior of a function or class without changing its source code. In Python, strictly, it's a higher-order function that takes a function and returns a wrapper function.

**Syntax:** `@decorator_name`

**Example: Logging Decorator**
```python
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished execution")
        return result
    return wrapper

@log_execution
def add(a, b):
    return a + b

add(2, 3) 
# Output:
# Calling function: add
# Finished execution
```

**🤔 Critical Thinking Check:**
*   **Metadata:** What happens to `add.__name__` after decoration? (It becomes `wrapper`. Use `@functools.wraps(func)` inside the decorator to preserve original metadata).
*   **Stacking:** Can you use multiple decorators? (Yes, they are applied bottom-up).
""",
        
    "Implement a singleton class.":
        """
🦄 **Singleton Pattern**

**Goal:** Ensure a class has only ONE instance and provide a global point of access.

**Method 1: Using `__new__` (Recommended)**
We check if `_instance` exists before creating a new one.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print("Creating new instance...")
            # Call super to actually create object
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()

print(s1 is s2)  # True
```

**Method 2: Using Decorators**
You can also write a `@singleton` decorator that manages a dictionary of instances.

**🤔 Critical Thinking Check:**
*   **Thread Safety:** What happens if two threads call `Singleton()` at the exact same time? (They might create two instances. Use a `Lock` object to make it thread-safe).
*   **Testing:** Why are Singletons hated in Unit Testing? (Global state makes tests dependent on each other).
""",
        
    "Explain the difference between deep copy and shallow copy.":
        """
🧬 **Deep vs Shallow Copy**

**Shallow Copy (`copy.copy`)**
*   Creates a new object, but inserts *references* into it.
*   If the original object contains mutable items (like lists), modifying them in the copy *changes* the original too.

```python
import copy
a = [[1, 2], [3, 4]]
b = copy.copy(a)
b[0][0] = 99
print(a) # [[99, 2], [3, 4]] -> CHANGED!
```

**Deep Copy (`copy.deepcopy`)**
*   Creates a new object and recursively copies everything.
*   Complete independence.

```python
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
b[0][0] = 99
print(a) # [[1, 2], [3, 4]] -> UNCHANGED
```

**🤔 Critical Thinking Check:**
*   **Performance:** Which is slower? (Deep copy is much slower as it traverses the whole object graph).
*   **Recursion:** What if the object links to itself? (`deepcopy` handles circular references automatically using a memo dictionary).
""",

    # --------------------------------------------------------------------------------
    # REACT
    # --------------------------------------------------------------------------------
    "Explain the Virtual DOM.":
        """
⚡ **Virtual DOM (VDOM)**

**The Concept:**
Manipulating the real DOM is slow (layout thrashing). React creates a lightweight copy of the DOM in memory called the Virtual DOM.

**The Process (Reconciliation):**
1.  **Render:** Application state changes.
2.  **Diffing:** React updates the VDOM and compares it with the previous VDOM snapshot. It identifies *exactly* what changed (e.g., "only this <span> text changed").
3.  **Patching:** It updates the Real DOM with only those specific changes.

**Answer Key:**
*   It is a JavaScript object representation of the UI.
*   It minimizes direct DOM manipulation.
*   Uses a "diffing" algorithm to determine updates.

**🤔 Critical Thinking Check:**
*   **Frameworks:** Do Svelte or Angular use VDOM? (Svelte does not; it compiles updates directly. Angular uses Incremental DOM).
*   **Keys:** Why are keys important in lists? (They help the Diffing algorithm identify which items changed, added, or removed efficiently).
""",
        
    "Create a counter component using hooks.":
        """
🔢 **React Hooks: Counter Example**

To build a counter, we need:
1.  State to hold the number (`useState`).
2.  Functions to increment/decrement.

```jsx
import React, { useState } from 'react';

const Counter = () => {
    // [currentState, updateFunction] = useState(initialValue)
    const [count, setCount] = useState(0);

    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2>Count: {count}</h2>
            <div style={{ gap: '10px', display: 'flex', justifyContent: 'center' }}>
                <button onClick={() => setCount(count - 1)}>Decrement</button>
                <button onClick={() => setCount(count + 1)}>Increment</button>
                <button onClick={() => setCount(0)}>Reset</button>
            </div>
        </div>
    );
};

export default Counter;
```

**🤔 Critical Thinking Check:**
*   **Async:** Is `setCount` synchronous? (No, state updates are batched/asynchronous).
*   **Staleness:** If you call `setCount(count + 1)` three times in a row, what happens? (It increments only by 1. Use the functional form `setCount(prev => prev + 1)` to fix this).
""",
        
    "What is the difference between state and props?":
        """
🎭 **State vs Props**

| Feature | Props (Properties) | State |
| :--- | :--- | :--- |
| **Source** | Passed from Parent Component. | Managed internally by the Component. |
| **Mutability** | **Immutable** (Read-only). | **Mutable** (via `setState` / `useState`). |
| **Purpose** | To configure a component (like function arguments). | To manage dynamic data (like local variables). |
| **Changes** | Parent changes props -> Child re-renders. | Component changes state -> Component re-renders. |

**Analogy:**
*   **Props:** Your DNA (passed from parents, can't change).
*   **State:** Your Mood (internal, changes often).

**🤔 Critical Thinking Check:**
*   **Drilling:** What if you need to pass props down 5 levels? (This is "Prop Drilling". Use **Context API** or Redux/Zustand instead).
*   **Derived State:** Should you copy props into state? (Avoid it "single source of truth". Calculate values on the fly).
""",
        
    "Explain useEffect dependency array.":
        """
♻️ **useEffect Dependency Array**

`useEffect(callback, dependencies)`

**1. No Array (Missing 2nd Arg)**
```js
useEffect(() => { ... })
```
*   Runs on **Every Render**.
*   **Risk:** Infinite loops if you update state inside.

**2. Empty Array `[]`**
```js
useEffect(() => { ... }, [])
```
*   Runs **Once** on Mount (like `componentDidMount`).
*   Example: API calls, setting up listeners.

**3. Array with Variables `[prop, state]`**
```js
useEffect(() => { ... }, [userId])
```
*   Runs on Mount + whenever `userId` changes.
*   Acts like `componentDidUpdate`.

**🤔 Critical Thinking Check:**
*   **Objects:** What if you put an object `{id: 1}` in the array? (Since objects are compared by reference, it will likely run on every render unless memoized with `useMemo`).
*   **Cleanup:** How do you handle unmounting? (Return a cleanup function from the effect).
""",
        
    "Implement a simple Todo list.":
        """
📝 **Simple Todo Implementation**

**Key Concept:** State Array + Mapping.

```jsx
import React, { useState } from 'react';

export default function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    if (!input) return;
    const newTodo = { id: Date.now(), text: input };
    setTodos([...todos, newTodo]); // Immutable update
    setInput('');
  };

  return (
    <div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
      />
      <button onClick={addTodo}>Add</button>
      
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>
    </div>
  );
}
```
**Pitfall:** Assuming `key` can be index. Always use a stable unique ID (`todo.id`).

**🤔 Critical Thinking Check:**
*   **Performance:** What if the list has 10,000 items? (Rendering will be slow. Use **Virtualization** like `react-window`).
*   **Persistence:** How to save on refresh? (Use `localStorage` inside a `useEffect`).
""",

    # --------------------------------------------------------------------------------
    # JAVASCRIPT
    # --------------------------------------------------------------------------------
    "What is event bubbling?":
        """
🫧 **Event Bubbling & Capturing**

**Bubbling (Default Phase):**
When an event happens on an element (e.g., `<button>`), it runs the handlers on the button first, then moves **upwards** to its parent, then the parent's parent, all the way to `window`.

**Analogy:** A bubble floating up from the bottom of the ocean to the surface.

**Delegation Pattern:**
We use bubbling to attach a single listener to a parent `<ul>` instead of 100 listeners to `<li>`.

```js
// Bubbles up
child.addEventListener('click', () => console.log('Child Clicked'));
parent.addEventListener('click', () => console.log('Parent Clicked'));
```

**Stopping Bubbling:**
```js
event.stopPropagation();
```

**🤔 Critical Thinking Check:**
*   **Opposite:** What is Event Capturing? (The phase where event goes down from Window -> Target. Enabled with `{capture: true}`).
*   **Default Action:** Does `stopPropagation` stop the default action? (No, `preventDefault()` does that).
""",
        
    "Explain closures with an example.":
        """
📦 **Closures**

**Definition:**
A closure is a function that remembers its outer variables even after the outer function has finished executing.

**Why?** Data Privacy, Factory Functions, Memoization.

**Example: Counter Factory**
```javascript
function createCounter() {
    let count = 0; // Private variable
    
    return {
        increment: function() {
            count++;
            return count;
        },
        getCount: function() {
            return count;
        }
    };
}

const counterA = createCounter();
console.log(counterA.increment()); // 1
console.log(counterA.increment()); // 2
console.log(counterA.count); // undefined (Private!)
```

**🤔 Critical Thinking Check:**
*   **Memory:** Are closures memory expensive? (Yes, because variables are not garbage collected as long as the closure exists).
*   **Loop:** The classic `for(var i...) setTimeout` problem. (Closures capture `i` by reference. Use `let` to fix it).
""",
        
    "Implement Promise.all polyfill.":
        """
🤝 **Promise.all Polyfill**

`Promise.all` takes an array of promises and resolves when **ALL** resolve, or rejects if **ANY** rejects.

```javascript
function myPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    let results = [];
    let completed = 0;
    
    if (promises.length === 0) resolve([]);
    
    promises.forEach((promise, index) => {
      // Use Promise.resolve in case item is just a value
      Promise.resolve(promise)
        .then(value => {
            results[index] = value; // Maintain order
            completed++;
            if (completed === promises.length) {
                resolve(results);
            }
        })
        .catch(reject); // Fail immediately on first error
    });
  });
}
```

**🤔 Critical Thinking Check:**
*   **Fail Safe:** What if you want to wait for all even if some fail? (Use `Promise.allSettled()`).
*   **Concurrency:** Does `Promise.all` run promises in parallel? (Yes, effectively, as they are initiated immediately).
""",
        
    "Difference between let, const, and var.":
        """
📦 **var vs let vs const**

| | var | let | const |
|---|---|---|---|
| **Scope** | Function Scope | Block Scope (`{}`) | Block Scope (`{}`) |
| **Hoisting** | Yes (initialized `undefined`) | Yes (TDZ - ReferenceError) | Yes (TDZ - ReferenceError) |
| **Reassignable?** | Yes | Yes | No |
| **Redeclarable?** | Yes | No | No |

**Best Practice:** Default to `const`. Use `let` only if value changes. Avoid `var`.

**🤔 Critical Thinking Check:**
*   **Objects:** Can you mutate a `const` object? (Yes! `const obj = {}` prevents reassignment `obj = {}`, but you can still do `obj.key = 5`).
""",
        
    "Explain the 'this' keyword.":
        """
👉 **'this' Keyword**

Values depends on **how function is called**:

1.  **Global Context:** `window` (or `{}` in Node).
2.  **Object Method:** `this` = the object.
    ```js
    const obj = { 
        name: 'Me', 
        print: function() { console.log(this.name) } 
    };
    obj.print(); // 'Me'
    ```
3.  **Arrow Function:** `this` = lexically binding (takes from surrounding scope). It does **not** have its own `this`.
4.  **Constructor:** `this` = the new instance.
5.  **Event Listener:** `this` = the element that fired event.

**🤔 Critical Thinking Check:**
*   **Loss of Context:** passing `obj.print` as a callback often loses `this`. (Fix using `.bind(obj)` or arrow functions).
""",

    # --------------------------------------------------------------------------------
    # DSA
    # --------------------------------------------------------------------------------
    "Implement Binary Search.":
        """
🔍 **Binary Search**

**Pre-requisite:** Array must be **SORTED**.
**Complexity:** O(log n) time, O(1) space.

**Algorithm:**
1.  Set `low` and `high` pointers.
2.  Calculate `mid`.
3.  If `arr[mid] == target`, return.
4.  If `arr[mid] < target`, search right (`low = mid + 1`).
5.  Else, search left (`high = mid - 1`).

**Code (Iterative):**
```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return -1
```

**🤔 Critical Thinking Check:**
*   **Overflow:** In languages like C++/Java, `(low + high) // 2` can overflow. (Use `low + (high - low) // 2`).
*   **Duplicates:** Does this basic code find the first or last occurrence? (It finds *any*. You need logic changes to specifically find boundaries).
""",
        
    "Reverse a linked list.":
        """
↩️ **Reverse Linked List**

**Goal:** Change pointers `1 -> 2 -> 3` to `1 <- 2 <- 3`.

**Visualizing:**
Need 3 pointers: `prev`, `curr`, `next_node`.

**Algorithm:**
1.  Initialize `prev = None`, `curr = head`.
2.  Loop while `curr` is not None:
    - Save `next_node = curr.next`
    - Reverse! `curr.next = prev`
    - Move `prev = curr`
    - Move `curr = next_node`
3.  Return `prev` (new head).

**Code:**
```python
def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
```

**🤔 Critical Thinking Check:**
*   **Recursion:** Can you do this recursively? (Yes, `node.next.next = node`).
*   **Cycles:** What if the list has a cycle? (This code will loop forever. Detect cycles first).
""",
        
    "Check for balanced parentheses.":
        """
⚖️ **Balanced Parentheses**

**Pattern:** Stack (LIFO).
**Problem:** `({[]})` is valid. `([)]` is invalid.

**Algorithm:**
1.  Iterate char by char.
2.  If Open bracket `[ { (` -> Push to Stack.
3.  If Close bracket:
    - Check if stack is empty (Invalid!).
    - Pop top. Does it match pair? `( -> )`, `{ -> }`.
    - If mismatch -> Invalid.
4.  At end, stack must be empty.

**Code:**
```python
def isValid(s):
    stack = []
    map = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in map: # Closing bracket
            top = stack.pop() if stack else '#'
            if map[char] != top:
                return False
        else: # Opening bracket
            stack.append(char)
            
    return not stack
```

**🤔 Critical Thinking Check:**
*   **Space:** What is the space complexity? (O(n) in worst case `((((`).
*   **Optimization:** Can you do O(1) space? (Only if there is one type of bracket `( )`, using a counter. With multiple types, Stack is necessary).
""",
        
    "Find the LCA of a binary tree.":
        """
🌳 **Lowest Common Ancestor (LCA)**

**Definition:** The lowest node `T` that has both `p` and `q` as descendants.

**Logic (Recursion):**
1.  Base case: If root is `None` or matches `p` or matches `q`, return `root`.
2.  Search Left: `left = lca(root.left, p, q)`
3.  Search Right: `right = lca(root.right, p, q)`
4.  If both `left` and `right` return non-None values, `root` is the split point (LCA).
5.  If only one returns a value, propagate that back up.

**Code:**
```python
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
        
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    if left and right:
        return root
        
    return left or right
```

**🤔 Critical Thinking Check:**
*   **BST:** What if it's a Binary Search Tree (BST)? (It's easier! If both p,q < root, go left. If both > root, go right. Else, root is LCA).
""",
        
    "Explain QuickSort algorithm.":
        """
⚡ **QuickSort**

**Concept:** Divide and Conquer.
1.  **Pivot:** Pick an element.
2.  **Partition:** Move smaller elements to left, larger to right.
3.  **Recurse:** Sort left and right parts.

**Complexity:** Average O(n log n). Worst O(n^2) (if sorted).

**🤔 Critical Thinking Check:**
*   **Stability:** Is QuickSort stable? (No, swapping elements can change relative order of equal items).
*   **Worst Case:** How to avoid O(n^2)? (Pick random pivot or median-of-three).
""",

    # --------------------------------------------------------------------------------
    # SYSTEM DESIGN
    # --------------------------------------------------------------------------------
    "Design a URL shortener.":
        """
🌐 **System Design: URL Shortener (TinyURL)**

**1. Requirements:**
*   Functional: Long URL -> Short URL, Short URL -> Redirect.
*   Non-Functional: Highly available, low latency, read-heavy (100:1).

**2. API Design:**
*   `POST /shorten(longUrl) -> shortUrl`
*   `GET /{shortUrl} -> 301 Redirect`

**3. Database Choice:**
*   **NoSQL (Cassandra/DynamoDB)** or **RDBMS (MySQL)**.
*   Schema: `(id, short_code, long_url, created_at)`. Index on `short_code`.
*   Data size: Billions of records. NoSQL scales better for writes.

**4. Core Logic (Encoding):**
*   **Base62 Encoding:** [a-z, A-Z, 0-9]. 62 characters.
*   A 7-character string allows $62^7 \approx 3.5$ Trillion URLs.
*   Auto-increment ID -> Base62 Encode.
    *   ID 100 -> "1C"
*   Distributed ID Generation needed (Snowflake or Zookeeper).

**5. Caching (Redis):**
*   Cache top 20% URLs (80-20 rule).
*   Structure: `{short_code: long_url}`.

**🤔 Critical Thinking Check:**
*   **Collisions:** Can Base62 collide? (No, because it maps 1-to-1 with a Unique ID).
*   **Security:** Users can guess next URL. Solution? (Add random salt or non-sequential IDs).
""",
        
    "Design Rate Limiter.":
        """
🚦 **System Design: Rate Limiter**

**Goal:** Limit user requests (e.g., 10 req/sec) to prevent DoS.

**Algorithms:**
1.  **Token Bucket:** Bucket has tokens. Request costs 1 token. Refill tokens at rate `r`. Flexible (bursts allowed).
2.  **Leaky Bucket:** Queue with constant outflow rate. Smooths traffic.
3.  **Fixed Window:** Counter per minute. Issue: spike at window edges.
4.  **Sliding Window Log:** Precise but memory heavy.

**Implementation (Redis):**
*   **Sliding Window Counter:** Store timestamp-counts in sorted sets.
*   Key: `user_id`, Value: `counter` with expiry.

**Middleware/Gateway:**
Often implemented in API Gateway (Kong, Nginx).

**🤔 Critical Thinking Check:**
*   **Distributed Env:** How to sync counters across multiple servers? (Use Redis as central store. Watch out for Race Conditions—use Lua scripts).
""",
        
    "Design Instagram feed.":
        """
📸 **System Design: News Feed (Instagram/Facebook)**

**The Challenge:**
Showing relevant posts from friends/followings quickly. Read heavy vs Write heavy.

**Approach 1: Pull Model (Fan-out on Load)**
*   User opens app -> Query DB for all followings' posts -> Merge & Sort in memory.
*   **Pros:** Simple writes.
*   **Cons:** Very slow reads for users following 1000s of people.

**Approach 2: Push Model (Fan-out on Write)**
*   User posts photo -> System inserts post ID into every follower's pre-computed "Feed List" (Redis).
*   User opens app -> Read strictly from their feed list. Fast!
*   **Cons:** Celebrity problem (Justin Bieber posts -> 100M writes).

**Approach 3: Hybrid**
*   Push for normal users.
*   Pull for celebrities (check Justin Bieber's timeline separately and merge).

**🤔 Critical Thinking Check:**
*   **Staleness:** How to handle edited/deleted posts in Push model? (You need a side-channel to propagate updates or check validity on read).
""",
    
    # --------------------------------------------------------------------------------
    # BEHAVIORAL
    # --------------------------------------------------------------------------------
    "Tell me about yourself.":
        """
🗣️ **"Tell Me About Yourself"**

**The Formula:**
Present -> Past -> Future

**Example Structure:**
1.  **Present:** "Currently, I am a software engineer at X, focusing on Backend systems using Python/FastAPI."
2.  **Past:** "Before that, I completed my degree in CS where I interned at Y, building React dashboards."
3.  **Key Highlight:** "I’m really proud of a project where I optimized a legacy SQL query reducing load times by 40%."
4.  **Future (The Hook):** "I've been following your company's work in AI, and I’m excited to bring my backend skills to help solve [specific problem]."

**Tips:**
*   Keep it under 2 minutes.
*   Tailor the "Future" part to the specific job description.

**🤔 Critical Thinking Check:**
*   **Relevance:** Did you mention your childhood/hobbies? (Avoid unless relevant. Keep it professional).
""",

    "Why do you want this job?":
        """
🎯 **"Why do you want this job?"**

**Goal:** Connect your personal goals with the company's mission.

**The "Why" Framework:**
1.  **Company Mission:** "I've always admired [Company]'s commitment to [Mission/Product]."
2.  **Role Fit:** "This role sits at the intersection of my skills in [Skill A] and [Skill B]."
3.  **Growth:** "I see a huge opportunity to learn from the [Specific Team] here."

**Sample Answer:**
"I've been using your platform for years and I love how you solve [Problem]. I'm looking for a role where I can apply my React experience to high-scale applications, and your engineering blog post about [Topic] really convinced me that this is the best place to grow as a frontend engineer."

**🤔 Critical Thinking Check:**
*   **Generality:** Could this answer apply to *any* company? (If yes, rewrite it. Mention specific products/values).
""",

    "Describe a challenging situation you faced.":
        """
🏔️ **Behavioral: Challenging Situation (STAR Method)**

**S - Situation:**
"In my last Hackathon, our team's main Database crashed 4 hours before submission."

**T - Task:**
"I was responsible for the backend. We had to either fix the corruption or switch to a backup which was 12 hours old."

**A - Action:**
"I gathered the team to remain calm. I quickly wrote a script to parse our local application logs to reconstruct the data loss. While I did that, I asked the frontend team to mock the data so they could record the demo video."

**R - Result:**
"We recovered 95% of the data. We submitted on time and actually won 2nd place for resilience. It taught me the importance of robust logging."

**🤔 Critical Thinking Check:**
*   **Ownership:** Did you blame others? ("My teammate broke the DB"). (Never blame. Focus on the solution).
"""
}

ALT_KNOWLEDGE_BASE = {
    # SQL
    "Write a query to find the second highest salary.": 
        """
🍰 **Explain it like I'm 5: The Cake Analogy**

Imagine you have a stack of cakes of different heights.
1.  You find the **Tallest Cake** (Max Salary).
2.  You take that cake away.
3.  Now, you look at the remaining cakes and find the **Tallest one left**.

That "Tallest one left" was originally the *Second* Tallest!

**In SQL Terms:**
"Select the MAX salary from the list of salaries that are NOT the MAX salary."
""",

    "Explain the difference between DELETE and TRUNCATE.":
        """
🏠 **Analogy: Cleaning a House**

*   **DELETE** is like throwing out trash one piece at a time. It takes time, you check each item before tossing it, and if you make a mistake, you might be able to run and grab it back from the bin.
*   **TRUNCATE** is like bulldozing the house and rebuilding it empty. It's instant, powerful, but everything is gone forever immediately.
""",

    # Python
    "Explain list comprehension with an example.":
        """
🏭 **Analogy: The Assembly Line**

*   **Old Way (For Loop):** You have a basket of apples. You pick one up, wash it, check if it's rotten, then put it in a new box. You repeat this manually for every apple.
*   **List Comprehension:** You build a machine. You pour the basket of apples in one end, and the machine automatically washes and filters them, shooting clean apples into the new box instantly.

It's the same result, just a more efficient "sentence" to describe the process.
""",

    "Explain the difference between deep copy and shallow copy.":
        """
📄 **Analogy: Photocopying a Document**

*   **Shallow Copy:** You take a photo of a piece of paper that has a post-it note stuck to it. You have a new photo, but it shows **the exact same physical post-it note**. If someone writes on the real post-it note, your photo technically "updates" (in programming terms, they point to the same memory).
*   **Deep Copy:** You re-write the entire document and the post-it note on a brand new sheet of paper. If someone burns the original, your copy is safe and unchanged.
""",

    # React
    "Explain the Virtual DOM.":
        """
👷 **Analogy: The Blueprint vs The Building**

*   **The Real DOM** is the actual Building. Changing a wall (DOM node) is slow, dusty, and expensive.
*   **The Virtual DOM** is a Digital Blueprint.
*   **React's Job:** When you want to change the building, React first changes the Blueprint (instantly). It then looks at the difference between the Old Blueprint and New Blueprint. It realizes "Oh, only this one window changed".
*   Then, it sends the construction crew to change *only that one window* in the real building.
""",
    
    "What is the difference between state and props?":
        """
👕 **Analogy: Clothes vs Uniform**

*   **Props (Uniform):** Your boss gives you a uniform. You cannot change it. You appear how they tell you to appear. (Passed from Parent, Immutable).
*   **State (Mood):** You are happy or sad inside. You control this. Your boss can't directly force you to be happy, only you can change it based on events (like getting a raise!). (Internal, Mutable).
""",

    # JavaScript
    "Explain closures with an example.":
        """
🎒 **Analogy: The Backpack**

Imagine a Hiker (Inner Function) walking out of a House (Outer Function). 
Even though the Hiker has left the House, they are wearing a **Backpack**.
Inside that backpack are all the items (variables) they took from the House.
No matter how far they travel, they still have access to the snacks in that backpack. 

That Backpack is the **Closure**.
""",

    "Explain the 'this' keyword.":
        """
👉 **Analogy: "My"**

If I say "My car", it depends on *Who* is speaking.
*   If **I** say it -> It's Rohit's car.
*   If **You** say it -> It's Your car.

The word "My" (`this`) changes meaning depending on the **Context** of the speaker.
In JS, `this` changes depending on *Who called the function*.
"""
}

# IMPORTANT: Renamed from get_explanation to support the new structure, 
# but we can keep get_explanation as a wrapper or just replace.
# The plan says we need both.
def get_explanations(task_text):
    return {
        "standard": KNOWLEDGE_BASE.get(task_text, "No specific explanation available."),
        "alt": ALT_KNOWLEDGE_BASE.get(task_text, None)
    }

def get_explanation(task_text):
    # Backwards compatibility wrapper just in case
    return KNOWLEDGE_BASE.get(task_text, "No specific explanation available.")
