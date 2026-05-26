# Random stuff I keep doing to learn about new topics, packages, languages, frameworks and whatever else is out there

## Table of Contents
- [Building Paho Library and writing MQTT Client in C](#mqtt-client-sub)
- [Fota server in python, punching CRC to Bin and other CRC related scripts](#server-fota-crc-multithreading)
- [Service Tool for 2G telematic using PyQt5](#tcu-2g-service-tool-dealer)
- [A work timer watchdog created in C using GTK3](#task-control-gtk3)
- [Post Build program for boot_info and CRC punch](#bootinfo-and-appcrc)
- [CMake based buildsystem for MC25 OpenCPU Quectel](#cmake-build-embedded)
- [Bumblenet - A Network Library (Incomplete)](#network-library-bumblenet)
- [Data Structures Algorithms Practice](#data-structures-algorithms)

Branches:

## [mqtt-client-sub](https://github.com/ABD-01/quantum-harmony/tree/mqtt-client-sub)

**Theme**: The requirement was to provide a firmware for testing EC20 Modem. The telematics device connects to test.mosquitto.org public broker and publishes packet of size 60kB (default, configurable) at interval of 30secs (default, configurable).

[Chats with ChatGPT](https://chat.openai.com/share/ac0b190c-9788-4057-b782-878e5e2d3a86)

**Features**: 
* I had already used paho mqtt library on python and [`mqtt_server.py`](mqtt_server.py) script would have been enough. 
* I decided to work with the C version of paho mqtt. Compiled the [paho.mqtt.c](https://github.com/eclipse/paho.mqtt.c) from source and as well as using vcpkg.
* I learned to use CMake with different compilers such as Clang (`C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/Llvm/bin/clang.exe`) and GCC (`C:/msys64/ucrt64/bin/gcc.exe`)
* Wrote my own CMakeLists.txt. 

**File Details**:
#### 1. [hexdump](https://github.com/ABD-01/quantum-harmony/blob/mqtt-client-sub/hexdump/hexdump.c)
Contains a function to print or dump the content of a buffer in hex format.
Compiling the hexdump.c file: 
* `cl .\hexdump\hexdump.c /I .\hexdump\ /c /Fo.\hexdump\hexdump.o`
* `clang -c .\hexdump\hexdump.c -o .\hexdump\hexdump.o`
* `gcc -c hexdump/hexdump.c -o hexdump/hexdump.o`

One can add default Pre-Processor macro value in CMakeLists.txt like this
```cmake
# Define NUMCOLS during the build (default value is 24)
set(NUMCOLS 24 CACHE INTEGER "Number of columns in hexdump")

# Pass NUMCOLS as preprocessor definition
target_compile_definitions(${target_name} PRIVATE NUMCOLS=${NUMCOLS})
```

#### 2. [mkPktRand](https://github.com/ABD-01/quantum-harmony/blob/mqtt-client-sub/mkPktRand.c)
Creates a random buffer for given size using [XOR Shift](https://en.wikipedia.org/wiki/Xorshift) random number generator.

<details>
<summary>32 Bit XOR Shift RNG</summary>
<br>
<pre><code class="lang-c"><span class="hljs-function"><span class="hljs-keyword">static</span> <span class="hljs-keyword">void</span> <span class="hljs-title">generatRandomBuffer</span><span class="hljs-params">(<span class="hljs-keyword">uint8_t</span> buffer[], <span class="hljs-keyword">size_t</span> size)</span>
</span>{
    <span class="hljs-keyword">uint32_t</span> *ptr = (<span class="hljs-keyword">uint32_t</span> *)buffer;
    <span class="hljs-keyword">size_t</span> numIterations = size / <span class="hljs-keyword">sizeof</span>(<span class="hljs-keyword">uint32_t</span>);
    <span class="hljs-keyword">for</span> (<span class="hljs-keyword">size_t</span> i = <span class="hljs-number">0</span>; i &lt; numIterations; ++i) {
        g_randSeed ^= (g_randSeed &lt;&lt; <span class="hljs-number">13</span>);
        g_randSeed ^= (g_randSeed &gt;&gt; <span class="hljs-number">17</span>);
        g_randSeed ^= (g_randSeed &lt;&lt; <span class="hljs-number">5</span>);
        ptr[i] = g_randSeed;
    }
}
</code></pre>
</details>

#### 3. [**mqtt_client.c**](https://github.com/ABD-01/quantum-harmony/blob/mqtt-client-sub/mqtt_client.c)
This is the main file that creates a client with(out) SSL, connetcs to broker and subcribes to a topic. 
This file uses the paho.mqtt.c library and the hexdump.

Also, $\text{ceil}(\frac{a}{b}) = \frac{a+b-1}{b}$

Logging to file as well as console.
```c
/**
 * The delay in log file updates may be due to output buffering. By default,
 * `printf` buffers output, delaying the write to the console or file until the
 * program exits. To address this, use `fflush(stdout)` and `fflush(logfile)` 
 * after printf and fprintf to ensure immediate writing to both console and file.
*/
#define PRINT(format, ...) do { printf(format, ##__VA_ARGS__); fprintf(logfile, format, ##__VA_ARGS__); fflush(stdout); fflush(logfile); } while (0)
```

<details>
<summary>Compiling mqtt_client.c file</summary>
<br>
<ul>
<li>GCC<pre><code class="lang-bash">gcc mqtt_client.c -I eclipse-paho-mqtt-c/<span class="hljs-keyword">include</span>/ -I hexdump/ -L eclipse-paho-mqtt-c/<span class="hljs-class"><span class="hljs-keyword">lib</span>/ <span class="hljs-title">hexdump</span>/<span class="hljs-title">hexdump</span>.<span class="hljs-title">o</span> -<span class="hljs-title">lpaho</span>-<span class="hljs-title">mqtt3cs</span>-<span class="hljs-title">static</span></span>
</code></pre>
</li>
<li>cl (MSVC)<pre><code class="lang-bash">cl .<span class="hljs-symbol">\m</span>qtt_client.c /I .<span class="hljs-symbol">\h</span>exdump<span class="hljs-symbol">\ </span>/I C:<span class="hljs-symbol">\d</span>ev<span class="hljs-symbol">\v</span>cpkg<span class="hljs-symbol">\p</span>ackages<span class="hljs-symbol">\p</span>aho-mqtt_x64-windows<span class="hljs-symbol">\i</span>nclude<span class="hljs-symbol">\ </span>/I C:<span class="hljs-symbol">\d</span>ev<span class="hljs-symbol">\v</span>cpkg<span class="hljs-symbol">\p</span>ackages<span class="hljs-symbol">\o</span>penssl_x64-windows<span class="hljs-symbol">\i</span>nclude<span class="hljs-symbol">\ </span>/link C:<span class="hljs-symbol">\d</span>ev<span class="hljs-symbol">\v</span>cpkg<span class="hljs-symbol">\p</span>ackages<span class="hljs-symbol">\p</span>aho-mqtt_x64-windows<span class="hljs-symbol">\l</span>ib<span class="hljs-symbol">\p</span>aho-mqtt3cs.lib .<span class="hljs-symbol">\h</span>exdump<span class="hljs-symbol">\h</span>exdump.o
</code></pre>
</li>
<li>Clang<pre><code class="lang-bash">clang .<span class="hljs-symbol">\m</span>qtt_client.c -I 'C:<span class="hljs-symbol">\d</span>ev<span class="hljs-symbol">\v</span>cpkg<span class="hljs-symbol">\p</span>ackages<span class="hljs-symbol">\p</span>aho-mqtt_x64-windows<span class="hljs-symbol">\i</span>nclude<span class="hljs-symbol">\'</span> -I .<span class="hljs-symbol">\h</span>exdump<span class="hljs-symbol">\ </span>-L C:<span class="hljs-symbol">\d</span>ev<span class="hljs-symbol">\v</span>cpkg<span class="hljs-symbol">\p</span>ackages<span class="hljs-symbol">\p</span>aho-mqtt_x64-windows<span class="hljs-symbol">\l</span>ib<span class="hljs-symbol">\ </span>-l paho-mqtt3cs .<span class="hljs-symbol">\h</span>exdump<span class="hljs-symbol">\h</span>exdump.o -o .<span class="hljs-symbol">\m</span>qtt_client.exe
</code></pre>
</li>
</ul>
</details>

<!-- 
* GCC
```bash
gcc mqtt_client.c -I eclipse-paho-mqtt-c/include/ -I hexdump/ -L eclipse-paho-mqtt-c/lib/ hexdump/hexdump.o -lpaho-mqtt3cs-static
```
* cl (MSVC)
```bash
cl .\mqtt_client.c /I .\hexdump\ /I C:\dev\vcpkg\packages\paho-mqtt_x64-windows\include\ /I C:\dev\vcpkg\packages\openssl_x64-windows\include\ /link C:\dev\vcpkg\packages\paho-mqtt_x64-windows\lib\paho-mqtt3cs.lib .\hexdump\hexdump.o
```
* Clang
```bash
clang .\mqtt_client.c -I 'C:\dev\vcpkg\packages\paho-mqtt_x64-windows\include\' -I .\hexdump\ -L C:\dev\vcpkg\packages\paho-mqtt_x64-windows\lib\ -l paho-mqtt3cs .\hexdump\hexdump.o -o .\mqtt_client.exe
``` 
-->

Refernce: [MQTTClient_subscribe.c](https://github.com/eclipse/paho.mqtt.c/blob/master/src/samples/MQTTClient_subscribe.c)

#### 4. [CMakeLists.txt](https://github.com/ABD-01/quantum-harmony/blob/mqtt-client-sub/CMakeLists.txt)

Used to create my package. Also see [CMakeLists.txt.bak](CMakeLists.txt.bak) wich uses `vcpkg` cmake toolchain.

Also learned that [PreLoad.cmake](PreLoad.cmake) runs before running the CMakeLists.txt. (Ref: https://stackoverflow.com/a/45247784).

So PreLoad.cmake contains: `set (CMAKE_GENERATOR "MSYS Makefiles" CACHE INTERNAL "" FORCE)`

Running cmake:
* `cmake .. -DCMAKE_C_COMPILER='C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/Llvm/bin/clang.exe'`
* `cmake .. -G "MSYS Makefiles" -DCMAKE_C_COMPILER=C:/msys64/ucrt64/bin/gcc.exe -DCMAKE_AR=C:/msys64/ucrt64/bin/ar.exe`

#### 5. [cmake_command_for_building_paho.bat/sh](https://github.com/ABD-01/quantum-harmony/blob/mqtt-client-sub/cmake_command_for_building_paho.sh)

The command I used to build paho.mqtt.c

#### 6. [mqtt_server.py](https://github.com/ABD-01/quantum-harmony/blob/mqtt-client-sub/mqtt_server.py)
The first thing I wrote which satisfies the requirements in python file


## [server-fota-crc-multithreading](https://github.com/ABD-01/quantum-harmony/tree/server-fota-crc-multithreading)

\# TODO: Add readme

## [tcu-2g-service-tool-dealer](https://github.com/ABD-01/quantum-harmony/tree/tcu-2g-service-tool-dealer)

Created a replacement of a legacy flashing utility for 2G devices. Integrated the the original UART communication C program with Python based GUI using ctypes. Also used IPC for communication progress to GUI.

## [task-control-gtk3](https://github.com/ABD-01/quantum-harmony/tree/taskControlC)

A tool created  tool for enforcing strict work-hour boundaries. It uses a scheduled GTK3-based visual timer and app killer to automatically shut down your PC and close running applications at the end of a configured work session.

### 1. [`schedule_task.c`](https://github.com/ABD-01/quantum-harmony/blob/taskControlC/schedule_task.c)
- Auto-starts on Windows boot.
- Asks user for confirmation or input of work start time.
- Calculates shutdown time = `start_time + 9h30m - 15min`.
- Creates a scheduled task (`stop_tasks.exe`) at the calculated time using `schtasks`.

### 2. [`stop_tasks.c`](https://github.com/ABD-01/quantum-harmony/blob/taskControlC/stop_tasks.c)
- Launches a warning popup (Window's blue colored screen with text).
- Starts a 15-minute GTK3 countdown timer.
- When timer hits 0:
  - Kills specified applications (e.g., VSCode, Edge, etc.)
  - Shuts down the PC.


## [bootinfo-and-appcrc](https://github.com/ABD-01/quantum-harmony/tree/bootinfo-and-appcrc)

Performs post build tasks
- Generate `bin` and `hex` files from `elf` frile created from project compilation  
- Puches CRC32 MPEG-2 at the end of the binary file.
- Creates `boot_info_data.c` file with structure containing firmware related metadata such as BL start address, APP start address, lenght, crc, debug flags, etc.
- Provides a linker script and a make file to compile the boot information file into `boot_info.hex`
- Clang Format file

Important Files' Details:
### 1. [**crc32_bootinfo.cpp**](https://github.com/ABD-01/quantum-harmony/blob/bootinfo-and-appcrc/crc32_bootinfo.cpp)
CPP program that reads binary file, calculates CRC32 and appends it. Generates `boot_info_data.c` file and also 3 other files, two srec commad files, crc32.bin (a 4 byte size file).

Using [`constexpr`](https://en.cppreference.com/w/cpp/language/constexpr) to create a crc table

```cpp
constexpr uint32_t POLYNOMIAL = 0x04C11DB7;
constexpr auto crc_table = [] {
    std::array<uint32_t, 256> table{};
    for (uint32_t i = 0; i < 256; i++) {
        uint32_t crc = i << 24;
        for (int j = 0; j < 8; j++)
            crc = (crc << 1) ^ (crc & 0x80000000 ? POLYNOMIAL : 0);
        table[i] = crc;
    }
    return table;
}();
```

Learnt about [SFINAE](https://en.cppreference.com/w/cpp/language/sfinae) and unnecessarily used [`std::enable_if`](https://en.cppreference.com/w/cpp/types/enable_if) for crc function.

```cpp
template <typename T>
using crc32_result_t = typename std::enable_if<std::is_integral<T>::value, uint32_t>::type;

template <typename T>
crc32_result_t<T> crc32(const T *data, size_t size);


template <typename T>
crc32_result_t<T> crc32(const T *data, size_t size)
{
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < size; ++i) {
        uint8_t index = ((crc >> 24) ^ static_cast<uint8_t>(data[i])) & 0xFF;
        crc = crc_table[index] ^ (crc << 8);
    }
    return crc;
}
```

Compilation:
```
clang crc32_bootinfo.cpp \
        -std=c++20 \
        -Wall -Wpedantic -Wextra \
        -O3 \
        -o generate_bootinfo_file.exe
```

### 2. [boot_info.mk](https://github.com/ABD-01/quantum-harmony/blob/bootinfo-and-appcrc/boot_info.mk)

Makefile that uses toochain compiler for making boot_info.hex.

```
{CG_TOOL_MAKE} -f boot_info.mk -k -j 8 all -O
```

### 3. [linker.cmd](https://github.com/ABD-01/quantum-harmony/blob/bootinfo-and-appcrc/linker.cmd)
Linker file to place boot_info strcture in proper memory address.


## [cmake-build-embedded](https://github.com/ABD-01/quantum-harmony/tree/cmake-for-mc25)

Created a build system using CMake for OpenCPU based project on Quectel's MC25 4G LTE module.

For more see [cmake-build-embedded/README.md](https://github.com/ABD-01/quantum-harmony/blob/cmake-for-mc25/README.md)

## [network-library-bumblenet](https://github.com/ABD-01/quantum-harmony/tree/network-library-bumblenet)

\# TODO: Add Readme

## [data-structures-algorithms](https://github.com/ABD-01/quantum-harmony/tree/DSA)

\# TODO: Add Readme
