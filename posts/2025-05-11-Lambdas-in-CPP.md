---
blogpost: true
title: "Getting to know lambdas in C++"
date: 11 May, 2025
category: programming
tags: C, C++, lambda functions
language: English
author: me
myst:
    number_code_blocks: ["cpp"]
    html_meta:
        "property=og:title": "Getting to know lambdas in C++"
        "language": "en"
---

{.hiddenh1}
# Getting to know lambdas in C++

**$\lambda$s in C++:** Nameless functions serving sweet syntactic sugar — just enough to give your codebase diabetes.

## Lambda Expressions
### Lambdas Reduce Boilerplate

{caption="Lambdas Reduce Boilerplate"}
```cpp linenos title:"Lambdas Reduce Boilerplate"
class Plus {
    int value;
public:
    Plus(int v) : value(v) {}

    int operator()(int x) const {
        return x + value;
    }
};

auto plus = Plus(1);
assert(plus(42) == 43);
// turns into
auto plus = [value = 1](int x) { return x + value; };

assert(plus(42) == 43);
// Reference: Back to Basics: Lambdas from Scratch - Arthur O'Dwyer - CppCon 2019
```

### Lambdas Without Captures

- ![Lambdas Without Captures.png](/_static/images/lambdas-without-captures.png)
- Lambdas have 2 types of parameters:
    1. Parameters for behaviour (The capture group)
    2. Parameters when they are called
- Generic Lambdas (C++14) may call arguments of generic type. (`auto`, `const auto&`) 
- What the actual fcuk is this piece of code

```cpp
void f(int, const int (&)[2] = {}) {}   // #1
void f(const int&, const int (&)[1]) {} // #2
// see entire code block at: https://en.cppreference.com/w/cpp/language/lambda
```
### Lambdas are function object.

- have a "unique, unnamed non-union class type" -- closure type
- Examples:

```cpp linenos title:"Lambda is Function Object" collapse
Example: 1
auto add = [](int x, int y) -> int {
	return x + y;
}
// has effect of
class lambda??? { // closure type, compiler decides the name
  public:
	lambda???();    // only callable by the compiler before C++20
	int operator() (int x, int y) const {
		return x + y;
	}
}
auto add = lambda???();
// example taken from Back to Basics: Lambdas - Nicolai Josuttis - CppCon 2021
```

```cpp linenos title: "Lambda with Capture" collapse
// Example: 2
while(...) {
	int min, max;
	...
	p = std::find_if(col1.begin(), col1.end(),
					[min, max](int i) {
						return min <= i <= max;
					});
}
// has effect of
class lambda??? {
  private:
	int min_, max_;
  public:
	lambda???(int min, int max)    // only callable by the compiler
		: _min(min), _max(max) {
	}
	int operator() (int x, int y) const {
		return x + y;
	}
}
while(...) {
	int min, max;
	...
	p = std::find_if(col1.begin(), col1.end(),
					lambda???{min, max});
}
// example taken from Back to Basics: Lambdas - Nicolai Josuttis - CppCon 2021
```

```cpp linenos title:"Genric Lambda" collapse
// Example: 3
auto plus = [] (auto x, auto y) {
	return x + y;
}

// Usage
int i = 42;
double d = plus(7.7,i);

std::string s{"Hi"};
std::cout << plus("s: ", s);

// manually would look like this (but no need to do it this way)
plus.operator()<double, int>(7.7, i);


// has effect of
class lambda??? {
  public:
	lambda???();    // only callable bu the compiler before C++20
	template<typename T1, typename T2>
	auto operator() (T1 x, T2 y) const {
		return x + y;
	}
}
auto plus = lambda???();
// example taken from Back to Basics: Lambdas - Nicolai Josuttis - CppCon 2021
```
### Generic lambda (function object) is different from the templated (generic) function.

```cpp linenos title:"Generic Function vs Generic Lambda" collapse
// Function object with generic `operator()` method
auto printLmbd = [](auto& col1) {
				for (const auto& elem: col1) {
				  std::cout << elem << '\n';
				}
			  };

//  Function template (generic before the call)
template<typename T>
void printFunc(const T& col1) {
	for (const auto& elem: col1) {
	  std::cout << elem << '\n';
	}
}

// usage
std::vector<int> v;
...
printFunc(v);
printLmbd(v);
printFunc<std::string>("hello");  // OK
printLmbd<std::string>("hello");  // Error

call(printFunc, v);               // Error
call(printFunc<decltype(v)>, v);  // OK
call(printLmbd, v);               // OK
```

### Initializer in lambda capture (since C++14)
```cpp linenos 
auto price = [disc = getDiscount(cust)] (auto item) {
	return getPrice(item) * disc;
}
```
### Lambdas are **stateless** by default -- Not allowed to modify local copies from captured by value

- `mutable` makes them stateful (modification allowed)
	
```cpp linenos title:"Stateless Lambdas" collapse
auto changed = [prev = 0] (auto val) {
	bool changed = prev!=val;
	prev = val;  // Error: prev is read-only copy
	return changed;
}
```

```cpp linenos title:"Mutable Lambdas" collapse
auto changed = [prev = 0] (auto val) mutable {
	bool changed = prev!=val;
	prev = val;  // OK due to mutable
	return changed;
}
std::vector<int> col1{7, 42, 42, 0, 3, 3, 7};
std::copy_if(col1.begin(), col1.end(),
			std::ostream_iterator<int>{std::cout, ""},
			changed);
// Output: 7, 42, 0, 3, 7

std::copy_if(col1.begin(), col1.end(),
			std::ostream_iterator<int>{std::cout, ""},
			changed);
// calling it again will not cause the 7 to removed.
// standard algorithms takes callables by value, 
// so next call is operated over a copy of changed
// Ref: Back to Basics: Lambdas - Nicolai Josuttis - CppCon 2021
```
### Per-lambda Mutable State (Wrong Approach)

```cpp linenos title:"Static in a Lambda"
auto counter = []() { static int i; return ++i; };
// This closure behaves like following class type:
class Counter {
    // No captured data members
public:
    int operator()() const {
        static int i;
        return ++i;
    }
};
// example from Back to Basics: Lambdas from Scratch - Arthur O'Dwyer - CppCon 2019
```

There is **just one static variable `i`**, shared by **all** callers of `Counter::operator()()`!
* Lambda capture behaviour `[=]` vs `[g=g]`

```cpp linenos
int g = 10;

auto kitten = [=]() { return g + 1; };     // Implicit capture by value
auto cat    = [g = g]() { return g + 1; }; // Explicit capture by value (copy of g)

int main() {
    g = 20;

    printf("%d %d\n", kitten(), cat()); // Output: 21 11
}
// example from Back to Basics: Lambdas from Scratch - Arthur O'Dwyer - CppCon 2019
```
- **Never** use `[=]` i.e. capture all by value. You might accidentally capture a vector of strings!!
- Also see slides 18...24 of [Back to Basics: Lambdas from Scratch - Arthur O'Dwyer - CppCon 2019](https://github.com/CppCon/CppCon2019/blob/master/Presentations/back_to_basics_lambdas_from_scratch/back_to_basics_lambdas_from_scratch__arthur_odwyer__cppcon_2019.pdf) on different ways of capturing a  variable

### Variadic Lambdas reduce boilerplate

```cpp linenos title:"Variadic Lambdas"
class Plus {
    int value;
public:
    Plus(int v);

	template<class... As>
    auto operator()(As... as) {
        return sum(as..., value);
    }
};

auto plus = Plus(1);
assert(plus(42, 3.14, 1) == 47.14);

// turns into

auto plus = [value = 1](auto... as) {
	return sum(as..., value);
};

assert(plus(42, 3.14, 1) == 47.14);
// Reference: Back to Basics: Lambdas from Scratch - Arthur O'Dwyer - CppCon 2019
```

## References
- [Lambda expressions in modern C++ (in depth step by step tutorial) - YouTube](https://youtu.be/MH8mLFqj-n8)
- [What is the type of lambda when deduced with "auto" in C++11? - StackOverflow](https://stackoverflow.com/questions/7951377/what-is-the-type-of-lambda-when-deduced-with-auto-in-c11)
- [Back to Basics: Lambdas - Nicolai Josuttis - CppCon 2021 - YouTube](https://youtu.be/IgNUBw3vcO4)
- [Back to Basics: Lambdas from Scratch - Arthur O'Dwyer - CppCon 2019 - YouTube](https://youtu.be/3jCOwajNch0)

