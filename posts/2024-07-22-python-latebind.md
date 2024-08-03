```{post} July 22, 2024
---
author: Muhammed Abdullah
category: programming
language: English
title: Late Binding of Python Closures
tags: Python, PyQT5, PySide6, lambda functions
exclude:
---

A subtle source of bugs in loops and closures. When lambda functions capture loop variables, they may not behave as you expect.
```

{.hiddenh1}
# Late Binding of Python Closures

## The Unexpected Trouble with Lambda Closures

Have a look at this Python code. At first glance, it seems straightforward. We're iterating over a list of buttons, printing their text, and connecting a lambda function to each button's clicked signal. The lambda should print "BTN_CLICKED:" followed by the text of the button that was clicked. Simple, right?

```py
for btn in self.buttons: 
    print(btn.text())
    btn.clicked.connect(lambda: print("BTN_CLICKED:",btn.text()))
```

Not so fast! If you run this code, you might be surprised to find that no matter which button you click, it always prints the text of the last button in the list. 

### Try it yourself.
Download [python_latebind.py {fas}`download`](python_latebind.py) file and try running it.

There are `TODO`s mentioned which you can follow along with the post.


## The Late (Lazy) Binding Culprit

The issue lies in how Python handles closures and variable scoping. In Python, closures capture variables by reference, not by value.

When the lambda function is created, it doesn't capture the current value of `btn`. Instead, it captures a reference to the variable `btn` itself. By the time the button is clicked and the lambda is executed, the loop has long finished, and `btn` is pointing to the last button in the list. When the lambda function is eventually called, it looks up the current value of `btn`, which is the last button in the loop.

You can even update the `btn` variable after the loop has finished, and notice that the text of this button is printed everytime.

```py
btn = QPushButton(self, text="EXIT")
layout.addWidget(btn)
```

This issue is particularly problematic in UI programming because there's a significant time gap between when the code runs (setting up the UI) and when the user interacts with it (clicking buttons). The late binding behavior isn't apparent until runtime, and it is very frustrating to track down such bugs.

More details can be found in this [StackOverflow question: Creating functions (or lambdas) in a loop (or comprehension)](https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension) and in the [Python docs: Why do lambdas defined in a loop with different values all return the same result?](https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result).


## Solution: Bind Early
To fix this, we can take advantage of default arguments in lambda functions. By using a default argument, we can capture the value of `btn` at at the time the lambda is created. Here's the corrected code:

```py
for btn in self.buttons: 
    print(btn.text())
    btn.clicked.connect(lambda btn=btn: print("BTN_CLICKED:", btn.text()))
```

By using `btn=btn` in the lambda's argument list, we're creating a default argument that captures the current value of `btn`. This effectively creates a new scope for each iteration of the loop, solving our late binding problem

### Alternative: Create a New Scope for Each `lambda`

This solution is inspired by [this StackOverflow answer](https://stackoverflow.com/a/2295368) and the author claims that this is more robust solution.

So, the idea is to create a new function (could alse be a lambda) which binds the `btn` loop variable as its argument.

```py
def create_click_handler(btn):
    return lambda: print("BTN_CLICKED:", btn.text())

for btn in self.buttons:
    print(btn.text())
    btn.clicked.connect(create_click_handler(btn))
```

Or you can use a lambda again:

```py
    btn.clicked.connect((lambda btn: lambda: print("BTN_CLICKED:", btn.text()))(btn))
```

## A Slight Digression

As I was writing this, I remembered the `map` function that applies a function to each item of a list.
So one can write this abomination of a one-line code:

```py
list(map(lambda btn: btn.clicked.connect((lambda btn: lambda: print("BTN_CLICKED:", btn.text()))(btn)), self.buttons))
```

## Conclusion
Late binding in Python closures can be a subtle source of bugs, especially when working with loops and lambda functions. By being aware of this behavior and using techniques like default arguments to force early binding, you can avoid these issues and write more predictable code.

I really love when Python variables wander outside their scopes /s.

Let me know if you’ve encountered similar bugs!
## References

* [What do lambda function closures capture?](https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture)
* [Creating functions (or lambdas) in a loop (or comprehension)](https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension)