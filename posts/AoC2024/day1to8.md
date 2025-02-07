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
// TODO

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

# [Day 6: Guard Gallivant](https://adventofcode.com/2024/day/6)
## [Solution Overview][day6]

```{code-block} cpp
:lineno-start: 8

void Guard::move(std::vector<std::string>& map)
{
    map[position.x][position.y] = 'X';
    Point temp = position+direction;

    if (temp.x < 0 || temp.y < 0 || temp.x >= map.size() || temp.y >= map[0].size())
    {
        can_move = false;
        cout << "Guard left the map" << endl;
        return;
    }

    if (map[temp.x][temp.y] == '#' || map[temp.x][temp.y] == 'O')
    {
        // Guard hit an obstacle, turn right
        turnRight();
        move(map);
        return;
    }

    if(is_looping(temp, direction))
    {
        can_move = false;
        stuck_in_loop = true;
        cout << "Guard stuck in a Loop" << endl;
        return;
    }

    position = temp;

    visited.emplace(position, direction);
}

void Guard::turnRight()
{
    //-1,0  -> 0,1
    // 0,1  -> 1,0
    // 1,0  -> 0,-1
    // 0,-1 -> -1,0
    direction = Point(direction.y, -direction.x);
}

bool Guard::is_looping(Point p, Point d) const
{
    PointMap::const_iterator it = visited.find(p);
    if (it != visited.end() && it->second == d)
        return true;
    return false;
}
```
### Part 1: Predict the Guard's Route
The Guard moves in a 2D grid, turning **right** upon hitting an obstacle (`#` or `O`). The goal is to find **the number of distinct positions visited** before the Guard exits the map.
**Key Logic:**
- Create an **unordered set** ($O(1)$ insert) for visited positions.
- If using a **vector**, check for duplicates before inserting ($O(n)$).
- Move the Guard until it exits the map.
- On obstacle collision → **turn right** → retry movement. 
* Return `visited.size()` for number of distinct positions.

### Part 2: Trap the Guard in a Loop
> You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?

Brute force solution would be to iterate over all possible position on the map. 
A better solution would be to only place obstacles on path that the guard travels. 

* Created an `unordered_map` to store each visited position with its corresponding direction. (`visited.emplace(position, direction)`)
* A loop occurs on visiting same position and have same direction as before

```{code-block} cpp
:lineno-start: 33

using PointMap = std::unordered_map<Point, Point, PointHash>;
...

    PointMap guardVisitedPositions = g.getVisited();  // from part 1
    for(const std::pair<Point, Point>& v: guardVisitedPositions)
    {
        int i(v.first.x), j(v.first.y);
		
        if(i==gx && j==gy) continue;
		
        map[i][j] = 'O';
        g = Guard(Point(gx, gy), Guard::dirUp);
		
        while (g.canMove())
        {
            g.move(map);
        }
        if(g.stuckInLoop())
        {
            ++numObstacles;
        }
        map[i][j] = 'X';
    }
```

## Concepts Learned
### Operator Overload

<details>
<summary>Example Operator Overloading for Point Class</summary>

```cpp
struct Point
{
    int x,y;
    Point(int x, int y): x(x), y(y) {}

    Point operator+(const Point& p)
    {
        return Point(x + p.x, y + p.y);
    }
    bool operator==(const Point& p) const
    {
        return x == p.x && y == p.y;
    }

}
std::ostream& operator<<(std::ostream& os, const Point& p)
{
    os << "(" << p.x << ", " << p.y << ")";
    return os;
}
```
</details>

### `const` Correctness
> **We bind type modifiers and qualifiers to the left**
> - Modern C, Jens Gustedt (Page 18)

1. **`const X* p`**
    ```cpp
    const int* p;  // p points to a constant int (can't modify the value it points to)
    int a = 5;
    p = &a;  // okay, p can point to another int
    *p = 10;  // error, can't modify the value of a through p
    ```
2. **`X const* p`** 
    ```cpp
    int const* p;  // Same as `const int* p`
    ```
3. **`X* const p`**
    ```cpp
    int* const p = &a;  // p is a constant pointer, it always points to the same location
    *p = 10;  // okay, the value of the object p points to can be modified
    p = &b;  // error, can't change p to point to another object
    ```
4. **`const X* const p`**
    ```cpp
    const int* const p = &a;  // p is a constant pointer to a constant int
    *p = 10;  // error, can't modify the value of the object p points to
    p = &b;  // error, can't change p to point to another object
    ```

5. The `const` at the end of member function does not modify the state of object.
```cpp
class Fred {
public:
  void inspect() const;   // This member promises NOT to change *this
  void mutate();          // This member function might change *this
};
void userCode(Fred& changeable, const Fred& unchangeable)
{
  changeable.inspect();   // Okay: doesn't change a changeable object
  changeable.mutate();    // Okay: changes a changeable object
  unchangeable.inspect(); // Okay: doesn't change an unchangeable object
  unchangeable.mutate();  // ERROR: attempt to change unchangeable object
}
```

6. `const Point&` Return type
```cpp
class Guard
{
public:
    // Getter functions to access position and direction
    const Point& getPosition() const { return position; }
    const Point& getDirection() const { return direction; }
    /**
    By returning a constant reference (const Point&), you provide read-only access to the position and direction. 
    This ensures that the caller cannot modify the values.
    */
```

### Dangling References
```cpp
const int& getTemp() {
    int temp = 10;  // Local variable
    return temp;  // Dangling reference (temp goes out of scope)
}

Point p1(1, 2);
const int& a = p1.getX();
p1 = Point(3, 4);  // a now refers to a destroyed object!
```
In C++, there is no built-in way to directly check if a reference is dangling

### Unordered set
Used Hash Table to store elements
Steps to use `unordered_set` with a custom class:
1. **Define a hash function** for your `Point` class.
2. **Override `==` operator** to check for equality, as `unordered_set` uses it to compare elements.
3. **Use the custom hash function** in `unordered_set`.

<details>
<summary>Example Code</summary>

```cpp
struct Point
{
    int x,y;
    Point(int x, int y): x(x), y(y) {}
    Point() : x(0), y(0) {}

    Point operator+(const Point& p) const
    {
        return Point(x + p.x, y + p.y);
    }
    bool operator==(const Point& p) const
    {
        return x == p.x && y == p.y;
    }
};
struct HashPoint {
	std::size_t operator()(const Point& p) const {
		return std::hash<int>()(p.x) ^ (std::hash<int>()(p.y) << 1);
	}
};
std::unordered_set<Point, HashPoint> visited;
```
</details>

For unordered_set of `std::pair<Point, Point>`
<details>
<summary>Code</summary>

```cpp
// Define a custom hash for std::pair<Point, Point>
struct PairHash {
    size_t operator()(const std::pair<Point, Point>& pair) const {
        PointHash pointHash;
        // Combine the hash values of the two points in the pair
        return pointHash(pair.first) ^ (pointHash(pair.second) << 1);
    }
};

// Overload equality operator for std::pair<Point, Point>
struct PairEqual {
    bool operator()(const std::pair<Point, Point>& a, const std::pair<Point, Point>& b) const {
        return a.first == b.first && a.second == b.second;
    }
};
/** This can also be omitted
The == operator for std::pair is already defined (since std::pair is a standard library type).
It compares both elements of the pair for equality.
*/

std::unordered_set<std::pair<Point, Point>, PairHash, PairEqual> pointPairs;
std::unordered_set<std::pair<Point, Point>, PairHash> point_pairs;

// Aliases 
using PointSet = std::unordered_set<Point, PointHash>;
using PointPairSet = std::unordered_set<std::pair<Point, Point>, PairHash>;
```
</details>

### Unordered Map
![](https://media.geeksforgeeks.org/wp-content/uploads/20220725162222/unorderedmapsyntax-660x190.png)

```cpp
std::unordered_map<Point, Point, PointHash> visited;

// ### Check if value is in HashMap
std::map<char,int> mymap;
std::map<char,int>::iterator it;

if (visited.find(current) != visited.end() && visited[current] == direction) {
    return true; 
}
// If current is not already in the map, accessing visited[current] will insert a new entry

auto it = visited.find(current);
if (it != visited.end() && it->second == direction) {
    return true; 
}

// ### Looping through HashMap
for(const std::pair<Point, Point>& v: visited)
{
    cout << v.first << ":" << v.second << endl;
}
```

### Static Constant Members in C++ Classes
* `static const` is used for class-level constants, meaning these constants are shared across all instances of the class.
* The `static` keyword ensures the constant is a class-wide (not instance-specific) member, while `const` ensures the values cannot be modified.
* Static members must be defined outside the class, even if they're `const`.
* You cannot initialize static members within constructors. Integral types you can initialize inline at their declaration.

```cpp
class Guard{
public:
    static const Point dirUp, dirDown, dirLeft, dirRight;
    static const int a = 4; // works
};
const Point Guard::dirUp(-1, 0);
const Point Guard::dirDown(1, 0);
const Point Guard::dirLeft(0, -1);
const Point Guard::dirRight(0, 1);
```

## References and Resources
* [c++ - What is the meaning of 'const' at the end of a member function declaration? - Stack Overflow](https://stackoverflow.com/questions/751681/what-is-the-meaning-of-const-at-the-end-of-a-member-function-declaration)
* [Const Correctness, C++ FAQ](https://isocpp.org/wiki/faq/const-correctness#const-member-fns)
* [The C++ 'const' Declaration: Why & How](http://duramecho.com/ComputerInformation/WhyHowCppConst.html)
* [How to create an unordered_set of user defined class or struct in C++? - GeeksforGeeks](https://www.geeksforgeeks.org/how-to-create-an-unordered_set-of-user-defined-class-or-struct-in-c/) or [unordered set - How can I use a C++ unordered_set for a custom class? - Stack Overflow](https://stackoverflow.com/questions/38554083/how-can-i-use-a-c-unordered-set-for-a-custom-class)
*  [hash - C++ unordered_map using a custom class type as the key - Stack Overflow](https://stackoverflow.com/questions/17016175/c-unordered-map-using-a-custom-class-type-as-the-key)
* [c++ - How do you loop through a std::map? - Stack Overflow](https://stackoverflow.com/questions/26281979/how-do-you-loop-through-a-stdmap)
* [How to initialize a "static const" data member in C++? - Stack Overflow](https://stackoverflow.com/questions/3531060/how-to-initialize-a-static-const-data-member-in-c)
* [ChatGPT](https://chatgpt.com/share/677d5d52-2aa0-8004-97f6-69f0ab1fd1ef)

<hr>

# [Day 7: Bridge Repair](https://adventofcode.com/2024/day/7)
## [Solution Overview][day7]

 **Part 1**: Given a test value and a list of numbers, determine whether the numbers can be combined using the operators `+` (addition) and `*` (multiplication) to produce the test value
> Operators are _always evaluated left-to-right_, _not_ according to precedence rules.

 **Part 2**: Introduces a third operator: [concatenation](https://en.wikipedia.org/wiki/Concatenation) (`||`), alongside `+` and `*`.
 
Using a recursive call, with using one operator from left at each call.

```{code-block} cpp
:lineno-start: 68

using ll = long long;

bool check_target1(const std::vector<int>& operands, int index, ll current_value, ll target)
{
	// reached end and found thr test value
    if(index==(int)operands.size()) return current_value == target;

	// If current value is already greater than the target, no point in continuing
	// small improvement by short circuiting
    if(current_value > target) return false;

    // subtle Bug! You only want to check for equality when list is exhausted
    //if(current_value == target) return true;

    return check_target1(operands, index+1, current_value + operands[index], target) 
        || check_target1(operands, index+1, current_value * operands[index], target);
}

bool check_target2(const std::vector<int>& operands, int index, ll current_value, ll target)
{
    if(index==(int)operands.size()) return current_value == target;

    if(current_value > target) return false;

    return check_target2(operands, index+1, current_value + operands[index], target) 
        || check_target2(operands, index+1, current_value * operands[index], target)
        || check_target2(operands, index+1, concat(current_value, operands[index]), target);
}

void part(const std::vector<std::pair<ll, std::vector<int>>>& data)
{
    ll result = 0;
    for(const std::pair<ll, std::vector<int>>& d: data)
        if(check_target(d.second, 0, 1, d.first))
}
```
The time complexity is $O(n^2)$ for Part 1and $O(n^3)$ for Part 2.
While this works, it can be optimized.

#### Optimization
With each recursive call the `current_value` increases. One way to optimize is to process the operations in reverse order, starting from the right, and try to undo the operations to see if the target value can be constructed. resulting in `current value` to be `0` at the end.

**For example:**
Given `292: 11 6 16 20`, the goal is to check if `292` can be made from these numbers.
The **left-to-right approach**:
- `[11+6, 16, 20]` → `[17*16, 20]` → `[292]`
The **right-to-left approach**:
- `[11, 6, 16, 292-20]` → `[11, 6, 272/16]` → `[11, 17-6]` → `[11-11]` → `[0]`
To undo concatenation (`||`), the `check_int_contains` function is used to check if an integer is present in another integer.

```{code-block} cpp
:lineno-start: 134

bool check_target1_v2(const std::vector<int>& operands, int index, ll target)
{
    if(index < 0) return target == 0 || target == 1;

    if(target < 0) return false;

    if(target % operands[index] == 0)
    {
        if(check_target1_v2(operands, index-1, target/operands[index]))
            return true;
        // Here too there can be a subtle Bug
        // if you return check_target1_v2(i-1, target/operands[i])
        // it fails to account for check_target1_v2(i-1, target-operands[i])
        // example: 103304: 269 4 96 8
    }

    return check_target1_v2(operands, index-1, target-operands[index]);
}
bool check_int_contains(ll target, ll subint, ll& new_target)
{
    int lt, ls;
    while(subint > 0)
    {
       lt = target % 10;
       target /= 10;
       ls = subint % 10;
       subint /= 10;
       if(lt != ls)
       {
           return false;
       }
    }
    new_target = target;
    return true;
}

bool check_target2_v2(const std::vector<int>& operands, int index, ll target)
{
    if(index < 0) return target == 0 || target == 1;

    if(target < 0) return false;

    if(target % operands[index] == 0)
    {
        if(check_target2_v2(operands, index-1, target/operands[index]))
            return true;
    }
    
    ll new_target;
    if(check_int_contains(target, operands[index], new_target))
    {
        if(check_target2_v2(operands, index-1, new_target))
            return true;
    }

    return check_target2_v2(operands, index-1, target-operands[index]);
}
```

While the time complexity still remains the same, there is significant improvement in the time taken.
{emphasize-lines="5,7,9,11"}
```text
[100%] Linking CXX executable day7.exe
Copying input.txt to input7.txt
[100%] Built target day7
Part 1: 6392012777720
Elapsed time: 2283 us
Part 2: 61561126043536
Elapsed time: 121022 us
Part 1 (Version 2): 6392012777720
Elapsed time: 1268 us
Part 2 (Version 2): 61561126043536
Elapsed time: 1498 us
[100%] Built target run7
```
## Concepts Learned
### Subsets of an array/vector using bit manipulation
- For an array of size $n$, there are $2^n$ possible subsets.
- Each subset corresponds to a binary number between `0` and $2^n - 1$.

<details>
<summary>Example</summary>

```cpp
// ### Problem: Find All Subsets That Sum to a Target Value
#include <iostream>
#include <vector>
using namespace std;

void findSubsetsThatSumToTarget(vector<int>& nums, int target) {
    int n = nums.size();
    vector<vector<int>> result;

    // Iterate over all possible subsets
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> subset;
        int sum = 0;

        // Generate the subset for the current bitmask
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) { // If the i-th bit is 1, include nums[i]
                subset.push_back(nums[i]);
                sum += nums[i];
            }
        }

        // Check if the subset sum equals the target
        if (sum == target) {
            result.push_back(subset);
        }
    }

    // Print the result
    cout << "Subsets that sum to " << target << ":\n";
    for (auto& subset : result) {
        cout << "[ ";
        for (int num : subset) {
            cout << num << " ";
        }
        cout << "]\n";
    }
}

int main() {
    vector<int> nums = {2, 3, 5};
    int target = 5;
    findSubsetsThatSumToTarget(nums, target);
    return 0;
}
```
</details>

## References and Resources
* [Print all subsets of a given Set or Array - GeeksforGeeks](https://www.geeksforgeeks.org/backtracking-to-find-all-subsets/)
* [Binary Tree Target Check - ChatGPT](https://chatgpt.com/share/67a21dc8-5358-8001-9671-7055a5f2e3ad)

<hr>

# [Day 8: Resonant Collinearity](https://adventofcode.com/2024/day/8)
## [Solution Overview][day8]
The grid is parsed into a dictionary (`unordered_map<char, vector<Vec2<int>>>`) with antenna labels as the key and a list of all the label’s positions as values.
### Part 1: Find the Antinodes
> an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other.

The words are complicated, see the diagram below. Basically, an antinode is a point that lies on the line extending from a pair of antennas at an equal distance beyond one of them

```text
..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
```

**Logic**:
* iterate over each pair of antennas with the same frequency. 
* for each pair, compute the distance between the two antennas and calculate the potential antinode positions on either side of the pair. 
* Check if the antinodes lie within the grid boundaries, and if they do, add them to an `unordered_set` to ensure uniqueness.

```{code-block} cpp
:lineno-start: 128

std::unordered_set<int> antinodes;
for(const std::pair<const char, std::vector<V2>>& antenas: data)
{
    const std::vector<V2>& a = antenas.second;
    for(int i = 0; i < static_cast<int>(a.size()); ++i)
    {
        for (int j = i + 1; j < static_cast<int>(a.size()); ++j)
        {
            // Calculate distance and antinode positions
            V2 dist = a[i] - a[j];
            V2 antinode1(a[i] + dist), antinode2(a[j] - dist);
            
            // Check if antinode positions are within bounds
            if(antinode1.x < maxX && antinode1.y < maxY && antinode1.x >= 0 && antinode1.y >= 0)
            {
                antinodes.insert(antinode1.x * maxY + antinode1.y);
            }
            if(antinode2.x < maxX && antinode2.y < maxY && antinode2.x >= 0 && antinode2.y >= 0)
            {
                antinodes.insert(antinode2.x * maxY + antinode2.y);
            }
        }
    }
}
```
To track the unique antinode positions, we need to map each `(x, y)` coordinate to a unique integer value. This is done by using a simple mathematical formula: `antinode1.x*maxY + antinode1.y`

### Part 2: I mean Harmonic Antinodes
> it turns out that an antinode occurs at _any grid position_ exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

Again, the words doesn't explain much, see the diagram.
Similar to Part 1, but instead of stopping at the first antinode, continue along the line of collinearity to count all antinodes.

```text
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
```
**Logic**:
* for each pair, compute the distance between the two antennas and calculate the potential antinode positions on either side of the pair. 
* expand the antinode positions by moving along the calculated distance in both directions until we reach the boundary of the grid.

```{code-block} cpp
:lineno-start: 176

while(antinode1.x < maxX && antinode1.y < maxY && antinode1.x >= 0 && antinode1.y >= 0)
{
    antinodes.insert(antinode1.x * maxY + antinode1.y);
    antinode1 += dist;  // Move along the distance
}
while(antinode2.x < maxX && antinode2.y < maxY && antinode2.x >= 0 && antinode2.y >= 0)
{
    antinodes.insert(antinode2.x * maxY + antinode2.y);
    antinode2 -= dist;  // Move along the distance
}
```
## Concepts Learned
### Operator Overloading for custom class
Operator overloading to work with the custom `Vec2` class representing a 2D vector. This allows to simplify the code when working with positions and distances, such as adding, subtracting, or comparing positions.

<details open>
<summary>Example</summary>

```cpp
template <typename T>
struct Vec2
{
    T x, y;
    Vec2(T x_val, T y_val) : x(x_val), y(y_val) {}
};

using V2 = Vec2<int>;
using mapV2 = std::unordered_map<char, std::vector<Vec2<int>>>;

template <typename T> Vec2<T> constexpr operator+(Vec2<T> a, Vec2<T> b) { return {a.x + b.x, a.y + b.y}; }
template <typename T> Vec2<T> constexpr operator-(Vec2<T> a, Vec2<T> b) { return {a.x - b.x, a.y - b.y}; }
template <typename T> Vec2<T> constexpr operator-(Vec2<T> a) { return {-a.x, -a.y}; }
template <typename T> Vec2<T> constexpr operator*(Vec2<T> a, Vec2<T> b) { return {a.x * b.x, a.y * b.y}; }
template <typename T> Vec2<T> constexpr operator*(Vec2<T> a, T b) { return {a.x * b, a.y * b}; }
template <typename T> Vec2<T> constexpr &operator+=(Vec2<T> &a, Vec2<T> b) { a = a + b; return a; }
template <typename T> Vec2<T> constexpr &operator-=(Vec2<T> &a, Vec2<T> b) { a = a - b; return a; }
template <typename T> bool constexpr operator==(Vec2<T> a, Vec2<T> b) { return a.x == b.x && a.y == b.y; }
template <typename T>
std::ostream& operator<<(std::ostream& os, const Vec2<T>& v)
{
    os << "(" << v.x << "," << v.y << ")";
    return os;
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& v)
{
    os << "[";
    for (auto i = v.begin(); i != v.end(); ++i) {
        if (i != v.begin()) os << ", ";
        os << *i;
    }
    os << "]";
    return os;
}
```
</details>

### Constexpr
Enable compile-time evaluation of simple functions, improving performance.
// TODO: write in detail

### this pointer
// TODO

### Unique Number for each element in 2D grid
for $arr[i][j]$ $\rightarrow$ $i\times Cols + j$, where $Cols$ is number of columns.

<hr>


<!-- Links -->
[day1]: https://github.com/ABD-01/AoC2024/blob/master/Day1_Historian_Hysteria/main.cpp
[day2]: https://github.com/ABD-01/AoC2024/blob/master/Day2_Red-Nosed_Reports/main.cpp
[day3]: https://github.com/ABD-01/AoC2024/blob/master/Day3_Mull_It_Over/main.cpp
[day4]: https://github.com/ABD-01/AoC2024/blob/master/Day4_Ceres_Search/main.cpp
[day5]: https://github.com/ABD-01/AoC2024/blob/master/Day5_Print_Queue/main.cpp
[day6]: https://github.com/ABD-01/AoC2024/blob/master/Day6_Guard_Gallivant/main.cpp
[day7]: https://github.com/ABD-01/AoC2024/blob/master/Day7_Bridge_Repair/main.cpp
[day8]: https://github.com/ABD-01/AoC2024/blob/master/Day8_Resonant_Collinearity/main.cpp