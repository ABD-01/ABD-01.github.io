# [Day 10: Hoof It](https://adventofcode.com/2024/day/10) - Finding Hiking Trails on a Topographic Map
## [Solution Overview][day10]
Given a [topographic map](https://en.wikipedia.org/wiki/Topographic_map) where each position's height ranges from `0` (lowest) to `9` (highest), the goal is to find a valid hiking trail. A valid trail is one where the height increases gradually (i.e., by 1 unit at each step) from a trailhead (`0-height`) to a `9-height` position.

![TopographicalMap.png](https://github.com/ABD-01/AoC2024/blob/master/Day10_Hoof_It/AoC2024-Day10-TopographicalMap.png?raw=true)

**Part 1 :** For each trailhead, find number of distinct  `9-height` position that can be reached.
Perform a **Depth First Search (DFS)** from each trailhead. When reaching a `9-height` position, increment the result count. To ensure distinct target counting, keep track of visited positions.

**Part 2:** For each trailhead, find the number of distinct trails leading to `9-height` position.
Same as before, perform a DFS. However, this time, multiple trails can lead to same target (i.e. `9-height`), hence will not stop exploration even if position is already visited.

{lineno-start=76}
```cpp
void DFS(const std::vector<std::vector<int>>& map, const std::pair<int, int>& idx, std::unordered_set<int>& visited, int& result)
{
    static std::pair<int, int> dirs[4] = {
        {-1, 0}, {0, 1}, {1, 0}, {0, -1}
    };

    int curr = map[idx.first][idx.second];

#if PART_2
    if(visited.find((idx.first*map[0].size() + idx.second)) != visited.end()) return; 
    visited.insert((idx.first*map[0].size() + idx.second));
#endif

    if(curr == 9)
    {
        cout << "Found 9-height position" << endl;
        ++result;
        return;
    }

    for(const auto& dir: dirs)
    {
        int i = idx.first+dir.first, j = idx.second+dir.second;
        if(i<0||i>map.size()-1||j<0||j>map[0].size()-1)
        {
            continue;
        }
        int temp = map[i][j];
        if(temp-curr != 1)
        {
            continue;
        }
        DFS(map, {i,j}, visited, result);
    }
}

int main(int argc, char* argv[])
{
    while(!toVisit.empty())
    {
        int result = 0;
        std::unordered_set<int> visited = {};
        DFS(map, toVisit.top(), visited, result);
        toVisit.pop();
        r += result;
    }
    cout << "Part " <<  (PART_2 ? 2 : 1) <<  ": " << r << endl;
}
```

### Optimizations
Instead of using `unordered_set<int>` data structure for keeping record of visited, tried using different data structures.

```{table} Performance on Day 10 Part 2
:widths: 2,1
:width: 80%

| Data Structure                                                                        | Time (µs) |
| ------------------------------------------------------------------------------------- | :-------: |
| [vector\<vector\<bool\>\>](https://en.cppreference.com/w/cpp/container/vector/vector) |   1044    |
| [set\<int\>](https://en.cppreference.com/w/cpp/container/set)                         |    402    |
| [unordered_set\<int\>](https://en.cppreference.com/w/cpp/container/unordered_set)     |    314    |
| [vector\<char\>](https://en.cppreference.com/w/cpp/container/vector)                  |    134    |
| [vector\<bool\>](https://en.cppreference.com/w/cpp/container/vector_bool)             |    113    |
```

1. **`vector<vector<bool>>`** performs poorly due to:
	- It has **double indirection overhead**.
	- Memory layout is **non-contiguous**, this means elements of different rows are not stored contiguously, leading to inefficient memory access.
2.  **`set<int>`** is relatively slower:
	- Uses balanced tree (typically **Red-Black Tree**) with $O(\log N)$ insertion and lookups.
1. **`unordered_set<int>`**:
	- hashing overhead
	- **amortized insertion time is $O(1)$**, even though **worst-case insertion (rehashing) is $O(n)$**.
	- `unordered_set<int>` is useful when grid is **extremely sparse**, meaning only a few cells need to be marked as visited. However, in dense grids, it adds hashing overhead.
2. **`vector<char>`** and **`vector<bool>`** are fastest:
	- both use **contiguous in memory**,  which minimizes cache misses and improves performance
	- `vector<bool>` packs multiple boolean values (up to 8) into a single byte.

{lineno-start=39}
```cpp
template<typename VisitedType>
void DFS(const std::vector<std::vector<int>>& map, const std::pair<int, int>& idx, VisitedType& visited, int& result);

template <typename VisitedType>
bool isVisitedAndMark(VisitedType& visited, const std::pair<int, int>& idx, int width);

// Specialization for std::unordered_set<int>
template<>
bool isVisitedAndMark<std::unordered_set<int>>(std::unordered_set<int>& visited, const std::pair<int, int>& idx, int width) {
    int pos = idx.first * width + idx.second;
    if (visited.find(pos) != visited.end()) return true;
    visited.insert(pos);
    return false;
}

// Specialization for std::vector<std::vector<bool>>
template<>
bool isVisitedAndMark(std::vector<std::vector<bool>>& visited, const std::pair<int, int>& idx, int) {
    if (visited[idx.first][idx.second]) return true;
    visited[idx.first][idx.second] = true;
    return false;
}
```
## Concepts Learned
### vector\<bool\>
`std::vector<bool>` is **bit-packed**, meaning it stores multiple `bool` values in a **single byte**, reducing memory footprint.
> `std::vector<bool>` is a possibly space-efficient specialization of [std::vector](https://en.cppreference.com/w/cpp/container/vector "cpp/container/vector") for the type bool.

Source: [gcc/libstdc++-v3/include/bits/stl_bvector.h](https://github.com/gcc-mirror/gcc/blob/3880271e94b7598b4f5d98c615b7fcddddee6d4c/libstdc%2B%2B-v3/include/bits/stl_bvector.h#L745)

Best for very large boolean datasets where memory efficiency is critical or need a dynamically resizable bit-array but don't require direct bit manipulation.

| Pros                                                      | Cons                                                                           |
| --------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Space-efficient (bit-packed), dynamic resizing.           | no direct memory access.                                                       |
| Contiguous memory allows for efficient cache utilization. | performance issues due to bit manipulations. (Slower per-element modification) |
```cpp
std::vector<bool> vec = {false, false, true, false};
// std::vector<bool> does not store actual bools
for(auto& i: vec) // compilation error: cannot bind `bool&` to `std::vector<bool>::reference
{
	std::cout << i << " "; 
}
```
#### Alternatives
- **`std::bitset<N>`**: Faster but requires compile-time size.
- **`std::vector<char>`**: Uses 1 byte per value, avoids bit-packing overhead, direct memory access.
### Return Value Optimization
\# TODO
<details>
<summary>Example</summary>

```cpp
std::vector<std::pair<int, int>> my_function() {
    std::vector<std::pair<int, int>> local_variable;
    return std::move(local_variable);
}
// warning: moving a local object in a return statement prevents copy elision [-Wpessimizing-move]
```
</details>

### Template Specialization
In C++, function template specialization allows you to define custom implementations of a function template for specific types. This is useful when the default behavior is inefficient or incorrect for certain data structures.

```cpp
template <typename T>
bool isVisitedAndMark(T& visited, const std::pair<int, int>& idx, int width);

template <>  // explicit specialization for T = std::unordered_set<int>
bool isVisitedAndMark<std::unordered_set<int>>(std::unordered_set<int>& visited,...) {
    // Implementation for std::unordered_set<int>
}
```
{attribution="Explicit specializations of function templates - cppreference.com"}
> When specializing a function template, its template arguments can be omitted if [template argument deduction](https://en.cppreference.com/w/cpp/language/template_argument_deduction "cpp/language/template argument deduction") can provide them from the function arguments:

### std::find

<details>
<summary>Example</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {10, 20, 30, 40, 50};
    std::vector<int>::iterator it = std::find(nums.begin(), nums.end(), 30);

    if (it != nums.end())
        std::cout << "Found at index: " << std::distance(nums.begin(), it) << std::endl;
    else
        std::cout << "Not found." << std::endl;
}
```
</details>

Source: [gcc/libstdc++-v3/include/bits/stl_algo.h](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/include/bits/stl_algo.h#L3826)

### Stack in CPP
\# TODO

## References and Resources
* [On vector\<bool\> -- Howard Hinnant : Standard C++](https://isocpp.org/blog/2012/11/on-vectorbool)
* [c++ - Why isn't vector\<bool\> a STL container? - Stack Overflow](https://stackoverflow.com/questions/17794569/why-isnt-vectorbool-a-stl-container)
* [c++ - What are copy elision and return value optimization? - Stack Overflow](https://stackoverflow.com/questions/12953127/what-are-copy-elision-and-return-value-optimization)
* [Explicit (full) template specialization - cppreference.com](https://en.cppreference.com/w/cpp/language/template_specialization)
* [C++ From Scratch: Template Specialization](https://www.youtube.com/watch?v=PbMGJdru6w4)
* [Function Templates Partial Specialization in C++ - Fluent C++](https://www.fluentcpp.com/2017/08/15/function-templates-partial-specialization-cpp/)

<hr>

# [Day 11: Plutonian Pebbles](https://adventofcode.com/2024/day/11)
## [Solution Overview][day11]
Given a list of pebbles, each with a numerical value. After each blink, the number of pebbles and their values change according to specific rules. The goal is to find the total number of pebbles after a set number of blinks.

The conditions are:
$
f(n+1) =
\begin{cases}
    1 & \text{if } n = 0 \\
    (\text{HIGH}(n), \text{LOW}(n)) & \text{if } \operatorname{numDigits}(n) \text{ is even} \\
    n \times 2024 & \text{otherwise}
\end{cases}
$

where $\text{HIGH}(n)$ refers to the first half of digits., $\text{LOW}(n)$ refers to the second half of digits.
- Example: If $n = 123456 ,\ \text{HIGH}(n) = 123, \  \text{LOW}(n) = 456$

My solution was to use a recursive function where each call represents a single blink.  It has a `depth` parameter that terminates the recursion when the desired number of blinks is achieved.

**Part 1**: 25 Blinks
**Part 2**: 75 Blinks

{lineno-start=134}
```cpp
void blink(ull value, ull& result, int numBlinks,  int depth)
{
    if(depth > numBlinks - 1) // depth start with 0
        return;
    
    if(value == 0) 
    {
        value = 1;
        return blink(value, result, numBlinks, depth+1);
    }
    int n = numDigits(value);
    if (!(n%2)) // n is even
    {
        ull splitValue = 0;
        int lastDigit = 0;
        int base10 = 1;
        for(auto i = 0; i < n/2; ++i)
        {
            lastDigit = value % 10;
            value /= 10;
            splitValue += (lastDigit * base10);
            base10 *= 10;
        }
        result++;
        blink(value, result, numBlinks, depth+1);
        blink(splitValue, result, numBlinks, depth+1);
        return;
    }
    value = value * 2024;
    return blink(value, result, numBlinks, depth+1);
}
```
This approach works well for Part 1, but for Part 2, the sheer number of recursive calls makes the program infeasible. The exponential growth in the number of pebbles causes excessive memory usage and function calls, leading to stack overflow.

We cannot store the entire list of stones, however we can store the count of each different stone instead.
I could make a map that store value as key, and it's count as the value, but I was unsure of how many different stones are possible.
To get a very rough upper bound assume, in the worst case each pebble split into 2 every blink, we will have $2^{numBlinks}$ pebbles at the end. How many distinct?? I don't know... Help me with that if you solved it that way.
If you've computed this bound more rigorously, let me know in the comments! 

Since, I was skeptical about the memory used to store each stone and it's count. I used a different method, just caching the result for stones with values 0 to 9 for $numBlinks$.

{lineno-start=42}
```cpp
std::vector<std::vector<ull>> cache(10, std::vector<ull>(MAX_NUM_BLINKS, 0));
// stores the resulting number of stones for values from 0 to 9
// cache[v][b-1] represent number of pebbles after blinking b times starting with pebble of value v
```

{lineno-start=121}
```cpp
void fill_cache(int numBlinks)
{
    for(auto nb = 0; nb < numBlinks; ++nb)
    {
        for(ull i = 0; i < 10; ++i)
        {
            ull r = 1;
            blink(i, r, nb+1);
            cache[i][nb] = r;
        }
    }
}
```
So before I start solving, I already know that `cache[3][55]` is what would happen if stone with value $3$ is blinked $56$ times. This will help short-circuit the entire blink calls for that value. 

While pebbles may have values greater than 9, many will eventually be reduced to a single-digit value due to repeated splitting. Thus, caching results for numbers `0-9` is a memory-efficient approximation

This caching enabled finding the number of stones for large values.

{lineno-start=141}
```cpp
    if(value < 10)
    {
        if (cache[value][numBlinks - depth - 1] != 0)
        {
            numShortCircuited++;
            DEBUG("Short circuited (" << g_numShortCircuited << ")" << endl);
            DEBUG("Pebble " << value << " after " << numBlinks - depth << " blinks will be split into " << cache[value][numBlinks-1 - depth] << endl);
            result += (cache[value][numBlinks-1 - depth] - 1); 
            // that -1 is there because the current stone is being counted twice.
            return; // no more recursive call again
        }
    }
```

Also, a bit about **`numDigits`**  
See file: [Day11_Plutonian_Pebbles/numDigits.cpp](https://github.com/ABD-01/AoC2024/blob/master/Day11_Plutonian_Pebbles/numDigits.cpp)

{lineno-start=108}
```cpp
int numDigits(unsigned long long i)
{
    int n = 1;
    if ( i >= 10000000000000000 ) { n += 16; i /= 10000000000000000; }
    if ( i >= 100000000         ) { n += 8; i /= 100000000; }
    if ( i >= 10000             ) { n += 4; i /= 10000; }
    if ( i >= 100               ) { n += 2; i /= 100; }
    if ( i >= 10                ) { n += 1; }

    return n;
    // ref: https://stackoverflow.com/a/6655759
}
```


```{table} Performance on Day 11 Part 2
:widths: 2,1,1,1,1
:width: 100%

| **Approach**                             | **g++ (No -O3)** | **g++ -O3**   | **Clang -O3**     | **Speedup (g++ No -O3 → Clang -O3)** |
| ---------------------------------------- | ---------------- | ------------- | ----------------- | ------------------------------------ |
| **StackOverflow (Bitwise Check)**        | 4,148,573 ns     | 2,298,124 ns  | **120 ns**        | **~34,500x Faster**                  |
| **Logarithmic (`log10`)**                | 14,081,701 ns    | 10,078,787 ns | **40 ns**         | **~350,000x Faster**                 |
| **Iterative Division (`/ 10`)**          | 38,035,651 ns    | 11,254,840 ns | **30 ns**         | **~1.26M× Faster**                   |
| **String Conversion (`std::to_string`)** | 73,341,935 ns    | 34,854,592 ns | **31,866,131 ns** | **~2.3x Faster**                     |
| **Builtin CLZ (`__builtin_clzll`)**      | 2,909,022 ns     | 2,799,729 ns  | **30 ns**         |  **~72,000x Faster**                 |
```

## Concepts Learned
### Constant Expression
Introduced in C++11.
* can be evaluated at compile time
* give the compiler deep insight
* constexpr is by design thread safe (A data race requires shared mutable state, something which is `const` is not mutable).
## References and Resources
* [algorithm - Finding the number of digits of an integer - Stack Overflow](https://stackoverflow.com/a/6655759)
* [Back to Basics: const and constexpr - Rainer Grimm - CppCon 2021](https://youtu.be/tA6LbPyYdco)

<hr>

<!-- Links -->
[day10]: https://github.com/ABD-01/AoC2024/blob/master/Day10_Hoof_It/main.cpp
[day11]: https://github.com/ABD-01/AoC2024/blob/master/Day11_Plutonian_Pebbles/main.cpp
