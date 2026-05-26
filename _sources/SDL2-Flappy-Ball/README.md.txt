# Flappy Ball

* [Play the Game (Web Version)](#play-the-game-web-version)
* [Flappy Ball](#gameplay)
* [Development](#development)
  + [I. Windows](#i-windows)
  + [II. Android](#ii-android)
  + [III. Emscripten (Web Assembly)](#iii-emscripten-web-assembly)

This is my first attempt to work with [SDL2](https://en.wikipedia.org/wiki/Simple_DirectMedia_Layer) and game development in general.  
I also experimented with cross-compilation of native apps for Android and Web Assembly.  
SDL Version: [2.30.5](https://github.com/libsdl-org/SDL/releases/tag/release-2.30.5)  

## Play the Game (Web Version)

You can play the SDL2 Flappy Ball directly in your browser here:

$\Longrightarrow$ **[https://abd-01.github.io/SDL2-Flappy-Ball/](https://abd-01.github.io/SDL2-Flappy-Ball/)**

(No installation required)

## Gameplay

https://github.com/user-attachments/assets/e5b228a9-a830-4789-8a3e-32add45441af

<!-- index.md content start -->

## Development

### I. Windows

1. Verify that `clang`, or another C/C++ compiler is installed.

    ```console
    $ clang --version
    clang version 19.1.5
    Target: x86_64-pc-windows-msvc
    Thread model: posix
    InstalledDir: C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\Llvm\x64\bin
    ```

2. Install CMake for build system. (Optional)

    ```console
    $ cmake --version
    cmake version 3.29.5
    
    CMake suite maintained and supported by Kitware (kitware.com/cmake).
    ```

3. Get SDL2 libraries or build from source code.

    ```console
    # clone or download the soure code
    $ cd SDL2-2.30.5
    $ mkdir -p build-msvc
    
    $ cmake -S . -B build-msvc \
        -G "MinGW Makefiles" \
        -DCMAKE_TOOLCHAIN_FILE=/path/to/clang_x86_64_msvc_toolchain.cmake \
        -DCMAKE_EXPORT_COMPILE_COMMANDS=TRUE \
        -DCMAKE_INSTALL_PREFIX=build-msvc/install
    ```

    The toolchain file is from [github.com/ABD-01/.dotfiles/clang_x86_64_msvc_toolchain.cmake](https://github.com/ABD-01/.dotfiles/blob/master/toolchains/clang_x86_64_msvc_toolchain.cmake)
    
    I install the SDL2 inthe `build` folder for convenience.  
    Use `-DSDL2_DIR=/path/to/SDL2-2.30.5/build-msvc/install/cmake` flag to let the project find the SDL2 package.  
    Or append the install prefix to [`CMAKE_PREFIX_PATH`](https://cmake.org/cmake/help/v3.29/variable/CMAKE_PREFIX_PATH.html)

    ```cmake
    list(APPEND CMAKE_PREFIX_PATH "${SDL_PATH}/build-${CMAKE_C_COMPILER_TARGET}/install")
    ```

4. Build the Game

    ```console
    $ cd flappy-ball
    $ make
    $ make install
    ```

5. Run the application!


### II. Android

Tested on following device:

```console
RMX1807:/ $ uname -a
Linux localhost 4.4.194-perf+ #1 SMP PREEMPT Fri Oct 16 16:27:22 CST 2020 aarch64
RMX1807:/ $ getprop ro.product.cpu.abi
arm64-v8a
RMX1807:/ $ cat /proc/cpuinfo
Processor       : AArch64 Processor rev 4 (aarch64)
processor       : 0
BogoMIPS        : 38.40
Features        : fp asimd evtstrm aes pmull sha1 sha2 crc32
CPU implementer : 0x51
CPU architecture: 8
CPU variant     : 0xa
CPU part        : 0x801
CPU revision    : 4
...
...more 7 cores

Hardware        : Qualcomm Technologies, Inc SDM660
RMX1807:/ $
RMX1807:/ $ getprop ro.build.version.release
10  # Android 10
```

1. Install [Java](https://en.wikipedia.org/wiki/Java_(programming_language))

    Android apps do not run native code directly, but bytes codes in JVM like virtual runtime.
    
    SDL2 uses JNI (Java Native Interface) to call your C/C++ code from the Java activity
    
    See: [The Relationship Between Android and Java-Medium](https://theiconic.tech/android-java-fdbd55aadc51) for more details.
    
    If you already have and Eclipse based IDE (MCUXpresso IDE, STM32CubeIDE, etc), you might already have Java installed in your machine.
    
    For example, I have `STM32CubeIDE 1.19.0` which shipped with JDK 21.0.8 (LTS)
    
    ```console
    $ ls /path/to/STM32CubeMX/jre/bin/java*
    /path/to/STM32CubeMX/jre/bin/java.dll
    /path/to/STM32CubeMX/jre/bin/java.exe
    /path/to/STM32CubeMX/jre/bin/javaaccessbridge.dll
    /path/to/STM32CubeMX/jre/bin/javac.exe
    /path/to/STM32CubeMX/jre/bin/javadoc.exe
    /path/to/STM32CubeMX/jre/bin/javajpeg.dll
    /path/to/STM32CubeMX/jre/bin/javap.exe
    /path/to/STM32CubeMX/jre/bin/javaw.exe
    
    $ export JAVA_HOME=/path/to/STM32CubeMX/jre
    $ export PATH=$JAVA_HOME/bin:$PATH
    $ java --version
    openjdk 21.0.8 2025-07-15 LTS
    OpenJDK Runtime Environment Temurin-21.0.8+9 (build 21.0.8+9-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.8+9 (build 21.0.8+9-LTS, mixed mode)
    ```

2. Install Android SDK
    
    I am not fond of IDEs, so I have installed only the command line tools from [developer.android.com/studio#command-line-tools-only](https://developer.android.com/studio#command-line-tools-only)
    
    Move the unzipped `cmdline-tools` directory into a new directory of your choice, such as `android_sdk`. This new directory is your *Android SDK* directory.
    
    In the unzipped `cmdline-tools` directory, create a sub-directory called `latest`.
    
    Move the original `cmdline-tools` directory contents, including the `lib` directory, bin directory, `NOTICE.txt` file, and `source.properties` file, into the newly created `latest` directory.
    
    Accept the Licenses. This would be a prompt dialog box in case of Android Studio IDE installation.
    
    ```console
    $ export ANDROID_HOME=D:/android_sdk/
    $ cd $ANDROID_HOME/cmdline-tools/latest/
    $ ./bin/sdkmanager.bat --licenses
    ```

3. Creating Android Project

    [**#RTFM**](https://en.wikipedia.org/wiki/RTFM)
    Follow the docs from SDL project: [SDL/docs/README-android.md](https://github.com/libsdl-org/SDL/blob/release-2.30.5/docs/README-android.md)

    1. Copy `SDL/android-project` directory to a suitable location and rename to the project's name: FlappyBall.
    2. Move or symlink the SDL directory into the "FlappyBall/app/jni" directory
    3. Move or symlink this repository to the "FlappyBall/app/jni/src" directory. (Such that this README is at `FlappyBall/app/jni/src/README.md`)
    4. To use CMake edit `FlappyBall/app/build.gradle`, comment out or remove sections containing ndk-build and uncomment the cmake sections.
    5. To customize your application name, edit `FlappyBall/app/src/main/AndroidManifest.xml` or `FlappyBall/app/src/main/res/values/strings.xml` and replace "org.libsdl.app" with an identifier for your product package.

4. Build and Install the application

    Run `./gradlew installDebug` in the project directory. It will build and install your .apk on any connected Android device
    
    ```console
    $ cd FlappyBall
    $ ./gradlew.bat installDebug
    
    > Task :app:installDebug
    Installing APK 'app-debug.apk' on 'RMX1807 - 10' for :app:debug
    Installed on 1 device.
    
    BUILD SUCCESSFUL in 8s
    ```

### III. Emscripten (Web Assembly)

Apart from native and android build, SDL2 also provides support for running application on web using [Emscripten](https://github.com/libsdl-org/SDL/blob/main/docs/README-emscripten.md)

1. Install Emscripten SDK

    ```bash
    git clone https://github.com/emscripten-core/emsdk.git --depth 1
    cd emsdk

    ./emsdk install latest
    ./emsdk activate latest
    source ./emsdk_env.sh
    ```
    Verify:

    ```bash
    emcc -v
    ```

2. Required Code Updates

    Browsers do not allow blocking loops. The main thread needs to be free to do browser stuff. So Emscripten lets you set up a [mainloop](https://emscripten.org/docs/porting/emscripten-runtime-environment.html#browser-main-loop).
    
    So instead of 
    
    ```cpp
    while (!quit) { ... }
    ```
    the code becomes
    
    ```cpp
    int main() {
    
        SDL_Window*   window   = SDL_CreateWindow(...);
        SDL_Renderer* renderer = SDL_CreateRenderer(...);
        
    #ifdef __EMSCRIPTEN__
        emscripten_set_main_loop(gameLoop, 0, 1);
    #else
        while (!quit) {
            gameLoop();
        }
    #endif
    ```

3. Building the application

    Simply compiling with `emcc` and correct flags would be enough.
    
    ```console
    $ emcc main.cpp -s USE_SDL=2 -s ALLOW_MEMORY_GROWTH=1 -O2 -o index.html
    ```
    
    Otherwise, if the project has cmake setup
    
    ```console
    $ mkdir build
    $ cd build
    $ emcmake cmake ..
    $ emmake make -j4
    ```

4. Running in a Web Server

    Start a web server by
    
    ```console
    $ emrun --no_browser --port 8080 .
    # or
    $ python -m http.server 8080
    ```

<!-- index.md content end -->

