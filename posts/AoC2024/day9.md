# [Day 9: Disk Fragmenter](https://adventofcode.com/2024/day/9)
## [Solution Overview][day9]

{attribution="adventofcode.com/2024/day/9"}
> The disk map uses a dense format to represent the layout of _files_ and _free space_ on the disk. The digits alternate between indicating the length of a file and the length of free space.

Each file on the disk has an _ID number_, assigned sequentially based on its appearance, starting with ID `0`. For example, the disk map `12345` consists of three files: a one-block file (ID `0`), a three-block file (ID `1`), and a five-block file (ID `2`)

For example, in the disk map `24531`
- `2` represents a two-block file.
- `4` represents four blocks of free space.
- `5` represents a five-block file.
- `3` represents three blocks of free space.
- `1` represents a one-block file."
And it will look like

```text
00....11111...2
```
The checksum for the disk map is sum of block's position multiplied by file Id it contains.
Given a disk map, rearrange it to make the disk compact. 

### Part 1: 

![part 1 solution](https://raw.githubusercontent.com/ABD-01/AoC2024/refs/heads/master/Day09_Disk_Fragmenter/input_part1.gif?raw=true){align=center}

The arrangement to be done is by moving a single file block from the end of the disk to the available free space in the beginning of the disk.
For instance disk map= `13212141`
The movement would look like

```text
0...11.22.3333.
03..11.22.333..
033.11.22.33...
033311.22.3....
033311322......
```
**Logic**:
* Iterate over the disk with two pointers. 
	* The first pointer, $i$, starts at `0` and increments by `1`, this will give the index of individual blocks (both files and spaces).
	* Second one, $j$ start at the position of last file block, and decrements by `2` to be always pointing at file block.
* If current position index is even (i.e. file block), do nothing.
* If current position index is odd (i.e. free space), move files from block $j$ into free space until:
	* free space at current position is used up, or
	* length of free space block is more than length of file block at $j$, move $j$ left to next file block and repeat.

{lineno-start=64}
```cpp
void part1(std::vector<int> dm)
{
    Timer t;

    long long unsigned int result = 0;
    int i = 0,j,id_first = 0, id_last;
    j = (dm.size() % 2) ? dm.size() - 1 : dm.size() - 2;
    id_last = j / 2;
    // An individual file/empty space is different from file/empty block. Files in same block have same id. 
    // i is the position of individual file/empty space
    // j is the position of file block starting from the end (decrements by 2 to keep pointing to file block)
    // id_first and id_last is the ids of files blocks. 

    for(int pos = 0; pos < dm.size(); ++pos)
    {
        if( pos % 2 == 0) // even position i.e it is file block
        {
            for(int k = 0; k < dm[pos]; ++k)  // for files in block at pos
            {
                result += (id_first*i);
                ++i;
            }
            ++id_first;
        }
        else // odd position i.e. empty block
        {
            for(int k = 0; k < dm[pos]; ++k) // for empty spaces in block at pos
            {
                while(dm[j] == 0 && j > pos) //  shift j left until 
                {
                    j-=2;
                    --id_last;
                }
                if(j<pos) break;

                --dm[j];
                result += (id_last*i);
                ++i;
            }
        }
        if(j<pos) break;
    }
    cout << "Part 1: " << result << endl;
}
```

### Part 2: 

![part 2 solution](https://raw.githubusercontent.com/ABD-01/AoC2024/refs/heads/master/Day09_Disk_Fragmenter/input_part2.gif?raw=true){align=center}

Rather than moving individual file blocks, move whole file instead to the first available free space.
Using same example from Part 1, the movement would look like
```text
0...11.22.3333.
0...11.22.3333.
022.11....3333.
022.11....3333.
```
The file with ID `3` could not be moved because there was no contiguous free space of length `4` available

I was stuck on this problem for a week, so first wrote the solution in python. Used a list of structure `Block` with two attributes `block_size`, `file_id` to represent the disk map.
The original python code can be found at [AoC2024/Day09_Disk_Fragmenter/main.py](https://github.com/ABD-01/AoC2024/blob/master/Day09_Disk_Fragmenter/main.py).

{lineno-start=145}
```cpp
std::vector<Block> moveBlocks(std::vector<Block>& dm, int j) {
    std::vector<Block> tmp;
    if (dm[j].file_id == -1)
        return dm;  // Selected block is empty, return as is

    for (size_t i = 0; i < dm.size(); i++) {
        if (j < i) {
            tmp.insert(tmp.end(), dm.begin() + i, dm.end());
            break;
        }

        if (dm[i].file_id != -1) {
            tmp.push_back(dm[i]);
            continue;
        }

        if (dm[i].block_size < dm[j].block_size) {
            tmp.push_back(dm[i]);
            continue;
        }

        int diff = dm[i].block_size - dm[j].block_size;
        if (diff > 0) {
            tmp.emplace_back(dm[j].block_size, dm[j].file_id);
            tmp.emplace_back(diff, -1);
            dm[j].file_id = -1;
        } else {
            tmp.emplace_back(dm[j].block_size, dm[j].file_id);
            dm[j].file_id = -1;
        }

        tmp.insert(tmp.end(), dm.begin() + i + 1, dm.end());
        break;
    }

    return tmp;
}

void part2(std::vector<int> data) {
    Timer t;
    std::vector<Block> dm; /*populate the list*/
    printBlocks(dm);

    for (int j = dm.size() - 1; j >= 0; j--) {
        dm = moveBlocks(dm, j);
        printBlocks(dm);
    }

    long long unsigned int result = 0;
    int pos = 0;
    
    for (const auto& b : dm) {
        for (int i = 0; i < b.block_size; i++) {
            if (b.file_id != -1)
                result += (static_cast<unsigned long long>(b.file_id) * pos);
            pos++;
        }
    }

    std::cout << "Part 2: " << result << std::endl;
}
```

#### Optimizations

> See my [discussion on reddit](https://www.reddit.com/r/adventofcode/comments/1im3f7a/2024_day_9_part_2_solution_too_slow_need_a_review/) related this section.

The obvious performance bottleneck in Python was the repeated creation of new copies of the disk map (`dm = moveBlocks(dm, j)`) in each iteration. Additionally, Python’s `append` and `extend` operations are expensive as well.

The solution was to update the disk map in place. This required to not use iterator on list that is changing it's length inside the loop. Using [u/TheZigerionScammer's](https://www.reddit.com/r/adventofcode/comments/1im3f7a/comment/mc13kt7/) suggestion, I iterated backwards over file `id`s and selected index from list based on the `id`.

Apart from that porting the solution to C++, caused massive improvement as Python does not like loops.

{lineno-start=162}
```cpp
void moveBlocks(std::vector<Block>& dm, int j) {
	...
        int diff = dm[i].block_size - dm[j].block_size;
        if (diff > 0) {
            dm[i].block_size = diff;
            dm.emplace(dm.begin()+i, dm[j].block_size, dm[j].file_id);
            dm[j+1].file_id = -1; // to account for len increase
        } else {
            std::swap(dm[i], dm[j]);
        }
	...
}
void part2(std::vector<int> data) {
	...
    for (int id = id_last; id > -1; --id) {
        j = dm.size() - 1;
        while(dm[j].file_id != id) --j;

        moveBlocks(dm, j);
    }
    ...
}
```
```{table} Performance on Day 9 Part 2
:width: 100%

| Solution                                                                                                                          | Time (in secs) | File                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------- | :------------: | ---------------------------------------------------------------------------------------------------------------------- |
| Original Code                                                                                                                     |    7.714727    | [main.py](https://github.com/ABD-01/AoC2024/blob/master/Day09_Disk_Fragmenter/main.py)                                 |
| In Place Update<br>([u/TheZigerionScammer](https://www.reddit.com/r/adventofcode/comments/1im3f7a/comment/mc13kt7/)'s suggestion) |    7.579476    | [main2.py](https://github.com/ABD-01/AoC2024/blob/master/Day09_Disk_Fragmenter/main2.py)                               |
| List of Lists of Block<br>([u/ndunnett](https://www.reddit.com/r/adventofcode/comments/1im3f7a/comment/mc0vft2/)'s suggestion)    |   12.329163    | [main3.py](https://github.com/ABD-01/AoC2024/blob/master/Day09_Disk_Fragmenter/main3.py)                               |
| Original Solution in C++                                                                                                          |    0.428756    | [main.cpp](https://github.com/ABD-01/AoC2024/blob/master/Day09_Disk_Fragmenter/main.cpp) <br>(with macro `USE_LEGACY`) |
| In Place Update in C++                                                                                                            |    0.096095    | [main.cpp](https://github.com/ABD-01/AoC2024/blob/master/Day09_Disk_Fragmenter/main.cpp)                               |
```
Hardware Used: GitHub Codespaces VM: AMD EPYC 7763 (2 vCPUs @ 3.2GHz), 8GB RAM, 32GB

Found a [more optimized solution](https://youtu.be/nJ18foH9EsQ) on the internet, that solves this in $O(N\log N)$.

## Concepts Learned
### std::vector\<T\>::emplace
`std::vector::emplace` inserts a new element into the vector at a specified position by constructing it in place, which can improve performance by avoiding unnecessary copies or moves.
<details>
<summary>Example</summary>

```cpp
int main() {
    std::vector<std::pair<int, std::string>> vec;

    vec.emplace(vec.begin(), 1, "one"); 

    // Without emplace, we would need to create a temporary std::pair and use push/insert:
    // vec.insert(vec.begin(), std::make_pair(1, "one"));
}
```
</details>

### Extending a vector in C++
In C++, the equivalent of Python’s `list1.extend(list2)` can be achieved using `std::vector<T>::insert`.

{lineno-start=241}
```cpp
tmp.insert(tmp.end(), dm.begin() + i, dm.end());
// Appends elements from index 'i' to the end of 'dm' into 'tmp'.
```

### Calling Python from C++ and Compiling with CMake

{lineno-start=8}
```cmake
find_package(Python3 COMPONENTS Interpreter Development)

if(NOT Python3_FOUND)
	message(FATAL_ERROR "Python3 not found")
endif()
# set(Python3_ROOT_DIR "/path/to/Python/Python310")
# set(Python3_INCLUDE_DIRS "${Python3_ROOT_DIR}/include/")
# set(Python3_LIBRARIES "${Python3_ROOT_DIR}/libs/python310.lib")

target_include_directories(day9 PRIVATE ${Python3_INCLUDE_DIRS})
target_link_libraries(day9 PRIVATE ${Python3_LIBRARIES})

if(NOT WIN32)  # Link pthread, dl, and util on non-Windows platforms
    target_link_libraries(day9 PRIVATE pthread dl util)
endif()
```
## References and Resources
* [std::vector<T,Allocator>::emplace - cppreference.com](https://en.cppreference.com/w/cpp/container/vector/emplace)
* [FindPython3 — CMake 3.29.9 Documentation](https://cmake.org/cmake/help/v3.29/module/FindPython3.html)


<!-- Links -->
[day9]: https://github.com/ABD-01/AoC2024/blob/master/Day09_Disk_Fragmenter/main.cpp
