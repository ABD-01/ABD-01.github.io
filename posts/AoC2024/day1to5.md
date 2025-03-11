# [Day 1: Historian Hysteria](https://adventofcode.com/2024/day/1)
## [Solution Overview][day1]
### Part 1: Sorting and Pairing Numbers
Given two lists of numbers.
> Pair up the `smallest number in the left list` with the `smallest number in the right list`, then the `second-smallest left number` with the `second-smallest right number`, and so on.

Sort both lists, take absolute difference of the values elementwise and sum it up.
```{code-block} cpp
:lineno-start: 37

    std::sort(vec1.begin(), vec1.end()); // sorts in ascending order
    std::sort(vec2.begin(), vec2.end());
    //std::ranges::sort(vec2);

    int result = 0;
    for (std::size_t i = 0; i < vec1.size(); i++)
        result += abs(vec1[i] - vec2[i]);
```

### Part 2: Calculating Similarity Scores
> Calculate a total `similarity score` by adding up each number in the left list after multiplying it by the number of times that number appears in the right list.

```{code-block} cpp
:lineno-start: 48

    for (std::size_t i = 0; i < vec1.size(); i++)
    {
        /**
        int count = 0;
        for (std::size_t j = 0; j < vec1.size(); j++)
            if (vec1[i] == vec2[j])
                count++;
        */
        int count = std::count(vec2.begin(), vec2.end(), vec1[i]);
        //int count = std::ranges::count(vec2, vec1[i]);
        result += (count * vec1[i]);
    }
```
Now here using `std::count` inside a loop results in a time complexity of $O(n^2)$. This could be optimized further using a hash map (`std::unordered_map`) to count occurrences in $O(n)$ time.

## Concepts Learned
### Reading from a file
Use **file streams** defined in header `<fstream>`
- **`ifstream`**: Input file stream for reading files.
- **`ofstream`**: Output file stream for writing files.
- **`fstream`**: Input-output file stream for both reading and writing.

**String Streams (`<sstream>`)**: Used to read from or write to strings.
- **`istringstream`**: For input operations from a string.
- **`ostringstream`**: For output operations to a string.
- **`stringstream`**: For both input and output operations on a string.

**standard input/output streams** (`<iostream>`)
### Vectors

```cpp
// 1. Creates a vector 'a' with 'count' elements
vector<int> a(count); 

// 2. Creates a vector 'v' with 'count' elements, all initialized to 'value'
vector<int> v(count, value); 

// 3. Looping over a vector and printing its elements
for (auto i : vec) std::cout << i << " "; 

// 4. Iterators
std::vector<int>::iterator it = vec.begin();
auto it = vec.end();

// 5. Methods
a.size()
a.push_back // adds an element to the end
```
<details>
<summary>Example</summary>

```cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

int main() {
    std::ifstream file("input.txt");
    if (!file.is_open()) {
        std::cerr << "Error opening file!" << std::endl;
        return 1;
    }

    std::vector<int> a, b;
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int num1, num2;
        if (!(iss >> num1 >> num2)) {
            std::cerr << "Error parsing line!" << std::endl;
            continue;
        }
        a.push_back(num1);
        b.push_back(num2);
    }

    file.close();

    return 0;
}
```
</details>

### Ranges
for ranges, use `-std=c++20` during compilation
1. `std::ranges::count`
	1. `count(v, target2);`
	2. Same as `std::count(v.begin(), v.end(), target1);`
2. `std::ranges::sort`
		Same as `std::sort(vec2.begin(), vec2.end());`

### Initializer List
\# TODO

### `explicit` specifier
When a constructor is marked as [`explicit`]([explicit specifier - cppreference.com](https://en.cppreference.com/w/cpp/language/explicit)), the compiler will **not** use that constructor for  **[implicit type conversions](https://en.cppreference.com/w/cpp/language/implicit_conversion)** or **[copy-initialization](https://en.cppreference.com/w/cpp/language/copy_initialization)**, meaning it will not automatically convert or create an object from a single argument when the compiler thinks it's needed (for example, in assignments or function calls).

<details>
<summary>Example</summary>

```cpp
#include <iostream>

class MyClass {
public:
    explicit MyClass(int x) { std::cout << "Constructor called with " << x << std::endl; }
};

void display(MyClass obj) {
    std::cout << "In display function\n";
}

int main() {
    // display(10);  // Error: no implicit conversion from int to MyClass
    display(MyClass(10));  // Must explicitly create MyClass
    return 0;
}
```
</details>

### Insertion Sort
<details>
<summary>Code</summary>

```{code-block} cpp
:lineno-start: 95

template<typename T>
void insertionSort(T& vec)
{
    typename T::iterator first = vec.begin();
    typename T::iterator last = vec.end();

    for(auto current = first + 1; current != last; current++)
    {
       auto key = *current;
       //auto position = current - 1;
       auto position = current;
       for (; position != first && *(position-1) > key; position--)
       {
            //*(position+1) = *position;
            *(position) = *(position-1);
       }
       //*(position+1) = key;
       *(position) = key;
    }
    return;
}
```
</details>

## References and Resources
* [File Handling in CPP: A Quick and Easy Guide](https://cppscripts.com/file-handling-in-cpp)
* [Ranges: the STL to the Next Level - Fluent C++](https://www.fluentcpp.com/2017/01/12/ranges-stl-to-the-next-level/)
* [explicit specifier - cppreference.com](https://en.cppreference.com/w/cpp/language/explicit)
* [Sorting (Bubble, Selection, Insertion, Merge, Quick, Counting, Radix) - VisuAlgo](https://visualgo.net/en/sorting?slide=1)
* [Classes Part 22 - Curly brace versus parenthesis and std::initializer_list| Modern cpp Series Ep. 59](https://youtu.be/krcSaMmSt2E)

<hr>

# [Day 2: Red-Nosed Reports](https://adventofcode.com/2024/day/2)
## [Solution Overview][day2]
### Part 1: Count Safe Reports
For a given list of numbers check if
- it is _all increasing_ or _all decreasing_.
- Any two adjacent values differ by _at least one_ and _at most three_.

```{code-block} cpp
:lineno-start: 17

bool isReportSafe(const std::vector<int>& v)
{
	if (v.size() < 2) return true; // A single-element or empty list is trivially safe.

    bool isSafe = true;
    // Must be all increasing or all decreasing.
    bool isSorted = (v[0] > v[1]) // If first element is greater than second, assume it should be decreasing
        ? std::is_sorted(v.begin(), v.end(), std::greater<int>{})
        : std::is_sorted(v.begin(), v.end()); 

    if(!isSorted) return false;

    for (std::size_t i = 1; i < v.size(); ++i)
    {
       int diff = abs(v[i]-v[i-1]); 
       // Any two adjacent values must differ by at least one and at most three.
       if (!(1 <= diff && diff<= 3)) 
       {
            isSafe = false;
            break;
       }
    }
    // Could also use std::adjacent_find 
    return isSafe;
}
```

### Part 2: Tolerate a Single Unsafe Report
For a given list, remove one element and check is it safe or not
```{code-block} cpp
:lineno-start: 64

bool part2(const std::vector<int>& vec)
    for(std::size_t i = 0; i < vec.size(); ++i)
    {
        std::vector<int> temp = vec;
        temp.erase(temp.begin() + i);
        if (isReportSafe(temp)) 
            return true;
    }
```

## Key Takeaways
### Vector of Vectors
### `std::is_sorted` and `std::greater`
### `std::adjacent_find`
Source: [gcc-mirror/gcc/libstdc++-v3/include/bits/stl_algo.h](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/include/bits/stl_algo.h#L823)

<details>
<summary>Code</summary>

```cpp
bool funct(const std::vector<int>& vec)
    
    std::vector<int> v{1, 2, 3, 4, 4, 5};
	auto it = std::adjacent_find(v.begin(), v.end());
	if (it != v.end())
		std::cout << "First pair of repeated elements: " << *it << '\n';
		
	// Solution using adjacent_find
    return std::adjacent_find(v.begin(), v.end(), 
        [](int a, int b) {
            int diff = std::abs(b - a);
            return diff < 1 || diff > 3;
        }) == v.end();
```
</details>

### `std::count_if`
<details>
<summary>Example</summary>

```cpp
bool funct(const std::vector<int>& vec)
#include <algorithm>

bool isSorted = (v[0] > v[1]) 
	? std::is_sorted(v.begin(), v.end(), std::greater<>{})
	: std::is_sorted(v.begin(), v.end());

return std::adjacent_find(v.begin(), v.end(), 
	[](int a, int b) {
		int diff = std::abs(b - a);
		return diff < MIN_DIFF || diff > MAX_DIFF;
	}) == v.end();

static int countSafeReports(const std::vector<std::vector<int>>& reports)
{
	return std::count_if(reports.begin(), reports.end(), isReportSafe);
}
```
</details>

## References and Resources
* [How to split a string in C++ - Fluent C++](https://www.fluentcpp.com/2017/04/21/how-to-split-a-string-in-c/)
* [std::is_sorted - cppreference.com](https://en.cppreference.com/w/cpp/algorithm/is_sorted)
* [std::adjacent_find - cppreference.com](https://en.cppreference.com/w/cpp/algorithm/adjacent_find)
* [std::count, std::count_if - cppreference.com](https://en.cppreference.com/w/cpp/algorithm/count)

<hr>

# [Day 3: Mull It Over](https://adventofcode.com/2024/day/3)
## [Solution Overview][day3]
### Part 1: Multiplication in Trash
Parse the given corrupted string and look for pattern `mul(X,Y)`, where `X` and `Y` are each 1-3 digit numbers. Add up all the results of the multiplications of `X` and `Y`.
```{code-block} cpp
:lineno-start: 36

    std::istreambuf_iterator<char> it(file), end;
    auto first = it;
    auto second = it;

	std::vector<std::pair<int, int>> mulVec;
    unsigned int result(0);

    for(first = it; it != end; ++it)
    {
        if (
            (char)*first == 'm' && 
            (char)*++first == 'u' &&
            (char)*++first == 'l' &&
            (char)*++first == '('
        )
        {
            bool secondNum = false;
            unsigned int num1(0), num2(0); 

            for(second=++first; second != end; ++second)    
            {
                if(std::isdigit(*second))
                {
                    if(secondNum)
                        num2 = num2*10 + (*second - '0');
                    else
                        num1 = num1*10 + (*second - '0');
                }
                else if ((char)*second == ',')
                    secondNum=true;
                else if ((char)*second == ')' && secondNum)
                {
                    mulVec.emplace_back(num1, num2);
                    result += (num1*num2);
                    break;
                }
                else
                    break;
            }
        }

    }

```
### Part 2: Do/Don't Multiply
> There are two new instructions you'll need to handle:
> - The `do()` instruction _enables_ future `mul` instructions.
> - The `don't()` instruction _disables_ future `mul` instructions.

```{code-block} cpp
:lineno-start: 96

    std::regex regex(R"((mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\)))");
    
    std::sregex_iterator start{ std::sregex_iterator(contents.begin(), contents.end(), regex) };
    std::sregex_iterator end{ std::sregex_iterator() };

    unsigned int result(0);

    int mulEnabled(1);
    for (auto i = start; i != end; ++i)
    {
        //std::smatch match = *i;
        std::string match = (*i).str();

        if(match.compare("don't()") == 0)
            mulEnabled = 0;

        else if (match.compare("do()") == 0) 
            mulEnabled = 1;

        else
        {
            int num1(0), num2(0);
            auto j = 4;
            while(match[j] != ',')
                num1 = num1*10 + (match[j++] - '0'); 
            ++j;
            while(match[j] != ')')
                num2 = num2*10 + (match[j++] - '0');

            result += (mulEnabled * num1 * num2); 
        }
    }
```

## Concepts Learned
### Stream Iterators
1. `std::istream_iterator`
2. `std::istreambuf_iterator`
3. Read entire file into a string:

```cpp
std::ifstream file(filename);
std::string contents{std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>()};
// or into a vector of strings
```

```{tip}
When reading characters, `std::istream_iterator` skips whitespace by default (unless disabled with [std::noskipws](https://en.cppreference.com/w/cpp/io/manip/skipws "cpp/io/manip/skipws") or equivalent), while [std::istreambuf_iterator](https://en.cppreference.com/w/cpp/iterator/istreambuf_iterator "cpp/iterator/istreambuf iterator") does not. In addition, [std::istreambuf_iterator](https://en.cppreference.com/w/cpp/iterator/istreambuf_iterator "cpp/iterator/istreambuf iterator") is more efficient, since it avoids the overhead of constructing and destructing the sentry object once per character.
```

### Regex
1. `std::cmatch` for `std::match_results<const char*>`: cannot be used with iterators.
2. `std::smatch` for `std::match_results<std::string::const_iterator>` to be used with iterators
3. `std::regex_match` for entire sequence
4. `std::sregex_iterator` for iterators, which dereferences to `std::smatch`

<details>
<summary>Examples</summary>

```cpp
std::regex pattern(R"(mul\(\d{1,3},\d{1,3}\))");
std::string input = "mul(123,456)";
if (std::regex_match(input, pattern)) {
    std::cout << "Pattern matched!" << std::endl;
}
```
```cpp
    std::regex regex(R"((mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\)))");
    
    std::sregex_iterator start{ std::sregex_iterator(contents.begin(), contents.end(), regex) };
    std::sregex_iterator end{ std::sregex_iterator() };

    for (auto i = start; i != end; ++i)
    {
        std::smatch match = *i;
        cout << match.str() << endl;
    }
```
</details>

### Strings
1. `std::string::compare`: returns 0 if equal
2. `std::stoi` - String to Int

## References and Resources
* [std::regex_iterator - cppreference.com](https://en.cppreference.com/w/cpp/regex/regex_iterator)
* [C++ Weekly - Ep 62 - std::regex](https://youtu.be/IOxKjqC1Ozo)

<hr>

# [Day4: Ceres Search](https://adventofcode.com/2024/day/4)
## [Solution Overview][day4]
### Part 1: Find XMAS
Find the word `XMAS` in a given grid such that it can be horizontal, vertical, diagonal, written backwards, or even overlapping other words.
```{code-block} cpp
:lineno-start: 70

std::vector<std::string> contents = {std::istream_iterator<std::string>(file), std::istream_iterator<std::string>()};

int rows{(int)contents.size()}, cols{(int)contents[0].size()};
std::stringstream ss{};
for (auto j = 0; j < cols; ++j)
{
	for(auto i = 0; i < rows; ++i)
		ss << contents[i][j];
	ss << endl;
}
std::vector<std::string> rotated_contents = {std::istream_iterator<std::string>(ss), std::istream_iterator<std::string>()};

std::vector<std::string> diag_contents = get_diagonals(contents);
std::vector<std::string> antidiag_contents = get_diagonals(contents, true);

int result(0);
std::string xmas("XMAS");
std::string samx("SAMX");

// repeat this for rotated_contents, diag_contents, antidiag_contents
for(const auto& line : contents)
{
	for(auto i = 0; i <= line.size() - xmas.size(); ++i)
	{
		if(line.substr(i, xmas.size()) == xmas || line.substr(i, samx.size()) == samx)
			++result;
	}
}
```

### Part 2: Find `MAS` in `X`
> find two `MAS` in the shape of an `X`.

```text
M.S
.A.
M.S
```

{lineno-start=45}
```cpp
    std::vector<std::string> grid = {std::istream_iterator<std::string>(file), std::istream_iterator<std::string>()};

    int rows{(int)grid.size()}, cols{(int)grid[0].size()};
    int result = 0;

    for (int i = 1; i < rows - 1; ++i)
    {
        for(int j = 1; j < cols - 1; ++j)
        {
            if(grid[i][j] != 'A') continue;
            result += checkMAS(grid, i, j, 1) & checkMAS(grid, i, j, -1);
        }
    }

bool checkMAS(const std::vector<std::string>& grid, int x, int y, int dir)
{
    char c1 = grid[x-1][y-dir];
    char c2 = grid[x+1][y+dir];

    if(c1 == 'M' && c2 == 'S') return true;
    if(c2 == 'M' && c1 == 'S') return true;
    return false;
}
```
## Key Takeaways
### Get diagonals and AntiDiagonals of a 2d Grid
Number of diagonals in a Grid: $R+C−1$

<details>
<summary>Code</summary>

```cpp
    int maxRow = 4;
    int maxCol = 3;

    std::cout << "Diagonals" << std::endl;
    int row_start = 0; // begin a 0
    int col_start = maxCol - 1; // begins at maxCol - 1 (the top-right corner).
    for (int i = 0; i < maxCol+maxRow-1; ++i) // Iterates over all diagonals
    { 
        std::cout << i << ": ";
        row_start += (col_start < 0); // clever mechanism to shift the starting row when column goes out of bounds using `(col_start < 0)`
        // row_start increments by 1 when col_start goes out of bounds (negative), ensuring the starting row shifts downward.
        for (
	        int j = std::max(0, col_start), k = row_start;  // `j` for columns and `k` for rows
	        j < maxCol && k < maxRow;
	        ++j, ++k
	    )
        {
                std::cout << k << "," << j << " ";
        }
        --col_start;  // shifts the starting column leftward
        std::cout << std::endl;
    }

    std::cout << "Anti Diagonals" << std::endl;
    row_start = 0;
    col_start = 0; //begins at 0 (the top-left corner)
    for (int i = 0; i < maxCol+maxRow-1; ++i) // Iterates over all diagonals
    { 
        std::cout << i << ": ";
        row_start += (col_start > maxCol-1); // shift row when col goes out of bounds
        for (
	        int j = std::min(maxCol-1, col_start), k = row_start;
	        j > -1 && k < maxRow;
	        --j, ++k
	    )
        {
                std::cout << k << "," << j << " ";
        }
        ++col_start; // shifts the starting column rightward
        std::cout << std::endl;
    }

/**
Output:
Diagonals
0: 0,2
1: 0,1 1,2     
2: 0,0 1,1 2,2 
3: 1,0 2,1 3,2 
4: 2,0 3,1     
5: 3,0
Anti Diagonals 
0: 0,0
1: 0,1 1,0     
2: 0,2 1,1 2,0 
3: 1,2 2,1 3,0
4: 2,2 3,1
5: 3,2

*/
```
</details>

Another method suggested by Claude 3.5
Instead of managing starting points (`row_start`, `col_start`) explicitly, we can use the property that:
- **Diagonal Index:** $k=j−i$
- **Anti-Diagonal Index:** $k=i+j$
- Diagonals will have $k\in[−(C−1),(R−1)]$.
- Anti-diagonals will have $k\in[0,R+C−2]$.

<details>
<summary>Code</summary>

```cpp
void printDiagonals(int maxRow, int maxCol) {
    std::cout << "Diagonals\n";
    // For main diagonals, points on same diagonal have same (row-col)
    for (int diff = -(maxCol-1); diff < maxRow; ++diff) {
        std::cout << (diff + maxCol - 1) << ": ";
        int startRow = std::max(0, diff);
        int startCol = startRow - diff;
        for (int row = startRow; row < maxRow && (row-diff) < maxCol; ++row) {
            std::cout << row << "," << (row-diff) << " ";
        }
        std::cout << '\n';
    }
    
    std::cout << "\nAnti Diagonals\n";
    // For anti-diagonals, points on same diagonal have same (row+col)
    for (int sum = 0; sum < maxRow + maxCol - 1; ++sum) {
        std::cout << sum << ": ";
        int startRow = std::max(0, sum - (maxCol - 1));
        int endRow = std::min(maxRow - 1, sum);
        for (int row = startRow; row <= endRow; ++row) {
            std::cout << row << "," << (sum-row) << " ";
        }
        std::cout << '\n';
    }
}
```
</details>

<hr>

# [Day 5: Print Queue](https://adventofcode.com/2024/day/5)
## [Solution Overview][day5]
### Part 1: Check Page Order
The first part of the input contains a list of rules `X|Y` which states that page `X` must be printed at some point before page `Y`. Next part have list page sequences, identify which one of those are in right order.

* Iterates over all pairs `(i,j)` in the given page sequence where `i<j`.
* For each pair, checking if it violates any of the rule.
* If no rule violated, the order is valid.

```{code-block} cpp
:lineno-start: 126

bool isOrderValid(const std::vector<int>& o, const std::vector<std::pair<int, int>>& rule)
{
    for(auto i=0; i < o.size()-1; ++i) 
    {
        for(auto j=i+1; j < o.size(); ++j) 
        {
            for(auto r: rule)
            {
                if(o[i] == r.second && o[j] == r.first) // incorrect order
                {
                    return false;
                }
            }
        }
    }
    return true;
}
```

This is simply brute force and horrible time complexity of $O(n^2\times m)$ where $n$ is length of the page sequence (`o.size()`) and $m$ is a number of rules(`rule.size()`).

#### Optimization
A faster [solution (aoc2024/day05/solution.cpp at main · UnicycleBloke/aoc2024)](https://github.com/UnicycleBloke/aoc2024/blob/main/day05/solution.cpp#L5-L18) ($O(m\times n)$) I found on Reddit:
* Iterate over rules $O(m)$
* For each rule find its first and second elements in the sequence (Linear search $O(2n)$, might short-circuit if first not found $O(n + n/2)$)
* check if both finds follow the rule, based on position they appear in the sequence. Else order is not valid.

More optimized solution would require a Hash Map:
```{code-block} cpp
:lineno-start: 145

bool isOrderValid(const std::vector<int>& o, const std::vector<std::pair<int, int>>& rule) {
    // Map elements in 'o' to their indices for fast lookup
    std::unordered_map<int, int> indexMap;
    for (int i = 0; i < o.size(); ++i) {
        indexMap[o[i]] = i;
    }

    // Check if any rule is violated
    for (const auto& r : rule) {
        if (indexMap.find(r.first) != indexMap.end() && indexMap.find(r.second) != indexMap.end()) {
            if (indexMap[r.first] > indexMap[r.second]) {
                // Order is invalid
                return false;
            }
        }
    }
    // Order is valid
    return true;
}
```
Bringing time complexity to $O(m + n)$ as `find` in Hash Map is $O(1)$ operation. 

{emphasize-lines="4,6,13,15"}
```text
// Before
[100%] Built target day5
Part 1: 4790
Elapsed time: 7330 us
Part 2: 6319
Elapsed time: 9174 us
Elapsed time: 45189 us
[100%] Built target run5

// After Optimization
[100%] Built target day5
Part 1: 4790
Elapsed time: 2959 us
Part 2: 6319
Elapsed time: 3437 us
Elapsed time: 38453 us
[100%] Built target run5
```
### Part 2: Sort pages as per the Rules
> For each of the _incorrectly-ordered updates_, use the page ordering rules to put the page numbers in the right order.

Implemented a bubble sort such that while not sorted keep swapping the elements in incorrect order.
```{code-block} cpp
:lineno-start: 93

    for(std::vector<int>& o: incorrect_orders)
    {
        while(true)
        {
            bool order_valid = true;

            for(auto r: rule)
            {
                auto i=0,j=0;
                for(; i < o.size(); ++i)
                {
                    if(o[i] == r.first) break;
                }
                for(; j < o.size(); ++j) 
                {
                    if(o[j] == r.second) break;
                }

                if(i==o.size() || j==o.size()) continue;
                if(j < i)
                {
                    std::swap(o[i], o[j]);
                    order_valid = false;
                    break;
                }
            }

            if (order_valid) break;
        }
    }
```

Found a [more optimized solution](https://blog.jverkamp.com/2024/12/05/aoc-2024-day-5-not-transitivinator/#optimization-1-drop-the-hashmap) on the internet, using $m\times m$ matrix `data`, where `data[a][b] == true` means `a` must come before `b` in any valid sequence.  

## Key Takeaways
### `std::move`
<details>
<summary>Example std::move</summary>

```cpp
    while (std::getline(file, line))
    {
        cout << line << endl;
        std::istringstream iss(line);
        std::vector<int> pages;
        std::string page;
        while (std::getline(iss, page, ','))
        {
            pages.push_back(std::stoi(page));
        }
        order.push_back(std::move(pages));
        /**
        order.push_back(pages);           - Copies the content of pages into order
        order.push_back(std::move(pages)) - Moves the contents, no copying, ownership of interal is transferred
        When use std::move??
        -> Don't need the original vector
        -> performance optimization
		*/
    }
```
</details>

### for loop with pass by reference
1. `for(auto o: orders)`: The copy constructor of `std::vector<int>` is called for each element of `orders`.

```cpp
    for(std::vector<int> o: incorrect_orders)
    {
	    // some condition
        std::swap(o[i], o[j]);
	}
	// Does NOT change the original
	// Instead do
	for(std::vector<int>& o: incorrect_orders) 
```

#### Fun
![](https://preview.redd.it/2024-day-5-part-2-non-transitivity-non-schmansitivity-v0-cah9pzcbd35e1.jpeg?auto=webp&s=dcd7519a3dca70b9ba1f58c9ca5ae76f9699528e)
Ref: [2024 Day 5 (part 2) Non-Transitivity, non-schmansitivity : r/adventofcode](https://www.reddit.com/r/adventofcode/comments/1h7jbqu/2024_day_5_part_2_nontransitivity/)
## References and Resources
* [C++ Weekly - Ep 278 - `emplace_back` vs `push_back`](https://youtu.be/jKS9dSHkAZY)

<hr>

<!-- Links -->
[day1]: https://github.com/ABD-01/AoC2024/blob/master/Day01_Historian_Hysteria/main.cpp
[day2]: https://github.com/ABD-01/AoC2024/blob/master/Day02_Red-Nosed_Reports/main.cpp
[day3]: https://github.com/ABD-01/AoC2024/blob/master/Day03_Mull_It_Over/main.cpp
[day4]: https://github.com/ABD-01/AoC2024/blob/master/Day04_Ceres_Search/main.cpp
[day5]: https://github.com/ABD-01/AoC2024/blob/master/Day05_Print_Queue/main.cpp