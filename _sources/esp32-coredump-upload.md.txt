# esp32-guru-upload

Upload Guru Meditation crashdumps from an ESP32 to a Flask server endpoint.

ESP32 firmware captures crashdumps from the dedicated coredump partition.

Crashdumps are uploaded via HTTP POST to a [Flask server](https://abd-01.github.io/esp32-guru-upload/coredump/)


## How To

### 1. Open in Codespaces

This repository is preconfigured with a development container.

Open it in GitHub Codespaces to get the ESP-IDF and Python environment ready.

### 2. Start ESP32 Firmware in QEMU

Launch the emulated ESP32 firmware with port forwarding:

```bash
cd esp32-guru-upload
get_idf   # setup ESP-IDF environment
idf.py qemu --qemu-extra-args "-nic user,hostfwd=tcp::8081-:8080"
```

For more insight on QEMU visit my [Blog](https://abd-01.github.io/posts/2025-07-15-QEMU/).

### 3. Start the Flask Server

In another terminal:

```bash
cd esp32-guru-upload
python endpoint_app.py
```

* Flask server will run at [`http://localhost:8080/`](https://abd-01.github.io/esp32-guru-upload/coredump/).

***Demo view of the server: [abd-01.github.io/esp32-guru-upload](https://abd-01.github.io/esp32-guru-upload/coredump/)***

### 4. Access the Web UI

Visit:
[http://localhost:8080/](https://abd-01.github.io/esp32-guru-upload/coredump/) or the GitHub Codespaces-provided URL.

## Overview

### ESP32 Firmware

Runs on real hardware or in QEMU. It intentionally triggers crashes, captures crashdumps from the dedicated coredump partition, and uploads them over HTTP.

### Flask Server

Receives crashdumps via POST `/upload`, stores them as `.elf` files, and provides a simple web interface to browse and analyze dumps using ESP-IDF tools.

### Development Container

Preconfigured for GitHub Codespaces or VS Code Dev Containers. Includes the ESP-IDF toolchain, QEMU emulator, and Python environment.

### Project Structure

```
abd-01-esp32-guru-upload/
├── .devcontainer/         # Devcontainer setup (ESP-IDF, QEMU, Flask)
├── main/                  # ESP32 firmware sources
│   ├── crash_app.c        # Crash simulation
│   ├── dummy_app.c        # Random dummy tasks
│   ├── guru-upload.c      # Main app, Wi-Fi & tasks
│   ├── upload_coredump_app.c # Upload task
│   └── http_service/      # HTTP client helpers
├── templates/             # Flask HTML templates
├── endpoint_app.py        # Flask server entrypoint
└── README.md
```

## Explanation

### Background

I was recently working on Hardfault Diagnostics for ARM Cortex-M, which could create crashlogs in the event of a Hardfault.

My work is in progress and can be viewed [here](https://github.com/ABD-01/hardfault-coredump-arm-cortex-m).

I would have eventually looked into ESP32, however, this gave me the chance to get into the [Guru Meditation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/fatal-errors.html) earlier.

### Software

[QEMU](https://www.qemu.org/docs/master/) has been an integral part of my work for the last couple of months, as it allowed me to get into different machines without needing the actual hardware. (I also use QEMU as my go-to virtual machine emulator instead of VMware or other software.) You can check out my [blog](https://abd-01.github.io/posts/2025-07-15-QEMU/) on QEMU if you like.

The official [`qemu-system-xtensa`](https://www.qemu.org/docs/master/system/target-xtensa.html) does not support ESP32 targets. Thankfully, [Espressif maintains a fork of QEMU](https://github.com/espressif/esp-toolchain-docs/blob/main/qemu/README.md) with patches that support these chips.

Fork of QEMU with Espressif patches: [github.com/espressif/qemu](https://github.com/espressif/qemu)

Build this version from source, and if everything works correctly, we have `esp32` in the supported machines list:

```
$ qemu-system-xtensa -M help
Supported machines are:
esp32                Espressif ESP32 machine
esp32s3              Espressif ESP32S3 machine
kc705                kc705 EVB (dc232b)
kc705-nommu          kc705 noMMU EVB (de212)
lx200                lx200 EVB (dc232b)
lx200-nommu          lx200 noMMU EVB (de212)
lx60                 lx60 EVB (dc232b)
lx60-nommu           lx60 noMMU EVB (de212)
ml605                ml605 EVB (dc232b)
ml605-nommu          ml605 noMMU EVB (de212)
none                 empty machine
sim                  sim machine (dc232b) (default)
virt                 virt machine (dc232b)
```

The next thing used is the [ESP-IDF (Espressif IoT Development Framework)](https://github.com/espressif/esp-idf). Just follow the manual for installation.

I have set up all the installation into the devcontainer so you don't have to worry about installing any prerequisite software.

### Implementation

For a Guru Meditation to be triggered, there has to be a piece of notorious code.

I have written [crash\_app.c](https://github.com/ABD-01/esp32-guru-upload/blob/master/main/crash_app.c), which just calls a few functions (to showcase stack depth) and writes to a prohibited location:

```c
==================== THREAD 1 (TCB: 0x3ffb94b0, name: 'CrashTask') =====================
#0  0x400da38f in baz (val=99) at esp32-guru-upload/main/crash_app.c:49
#1  bar (val=67) at esp32-guru-upload/main/crash_app.c:36
#2  foo (val=67) at esp32-guru-upload/main/crash_app.c:28
#3  CrashTask (pvParameters=<optimized out>) at esp32-guru-upload/main/crash_app.c:20
#4  0x40085f54 in vPortTaskWrapper (pxCode=0x400da2f0 <CrashTask>, pvParameters=0x0) at esp-idf/components/freertos/FreeRTOS-Kernel/portable/xtensa/port.c:139
```

***Visit [abd-01.github.io/esp32-guru-upload/device_log](https://abd-01.github.io/esp32-guru-upload/device_log/) for complete logs.***

[ESP-IDF (Espressif IoT Development Framework)](https://github.com/espressif/esp-idf) through its `menuconfig` provides an option for coredumps to be sent over UART or saved in Flash. See [sdkconfig](https://github.com/ABD-01/esp32-guru-upload/blob/master/sdkconfig) or run `idf.py menuconfig`:

```
# Core dump

CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH=y
CONFIG_ESP_COREDUMP_ENABLE_TO_UART=n
CONFIG_ESP_COREDUMP_ENABLE_TO_NONE=n
CONFIG_ESP_COREDUMP_DATA_FORMAT_BIN=n
CONFIG_ESP_COREDUMP_DATA_FORMAT_ELF=y
CONFIG_ESP_COREDUMP_CHECKSUM_CRC32=y
CONFIG_ESP_COREDUMP_CHECK_BOOT=y
CONFIG_ESP_COREDUMP_ENABLE=y
CONFIG_ESP_COREDUMP_LOGS=y
CONFIG_ESP_COREDUMP_MAX_TASKS_NUM=64
```

Coredump-related public APIs can be used by including [esp\_core\_dump.h](https://github.com/espressif/esp-idf/blob/master/components/espcoredump/include/esp_core_dump.h).

[guru\_upload.c](https://github.com/ABD-01/esp32-guru-upload/blob/master/main/guru-upload.c) is the main file of the project implementing `app_main`, and the first thing it does is check if a coredump exists in flash:

```c
esp_err_t err = esp_core_dump_image_get(&addr, &size);
```

If a coredump is found, `UploadCoredumpTask` is invoked as a separate RTOS task (implementation in [upload\_coredump\_app.c](https://github.com/ABD-01/esp32-guru-upload/blob/master/main/upload_coredump_app.c)).

Other than that, [guru\_upload.c](https://github.com/ABD-01/esp32-guru-upload/blob/master/main/guru-upload.c) starts a dummy application (which just prints logs based on a pseudorandom number) and an HTTP webserver that responds with *"Hello from ESP32"*.

***The project, instead of being created from scratch, was created using the [HTTP Request Example](https://github.com/espressif/esp-idf/tree/master/examples/protocols/http_request) template.***

The HTTP client operations are also inspired by the provided examples.
See [esp\_http\_client\_example.c#http\_native\_request](https://github.com/espressif/esp-idf/blob/f38b8fec92a0e389b733cb4fbf49be86e5144333/examples/protocols/esp_http_client/main/esp_http_client_example.c#L763-L792).

[upload\_coredump\_app.c](https://github.com/ABD-01/esp32-guru-upload/blob/master/main/upload_coredump_app.c) reads the coredump saved in flash and posts it chunk by chunk to the server:

```c
coredump = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_DATA_COREDUMP, NULL);
esp_err_t err = esp_partition_read(coredump, offset, buffer, buffer_size);
http_upload_send_chunk(client, buffer, buffer_size);
```

### Server

I had a fair share of experience with Flask, and having worked with connected vehicle protocols and protobuf, I also put together a Flask-based server where I can upload the coredump data. See [endpoint\_app.py](https://github.com/ABD-01/esp32-guru-upload/blob/master/endpoint_app.py) for internal details.

[http://localhost:8080/](https://abd-01.github.io/esp32-guru-upload/coredump/) displays the list of coredumps received.
[http://localhost:8080/coredump/coredump-\<timestamp>.elf](https://abd-01.github.io/esp32-guru-upload/coredump/coredump-1758023059.elf/) will run `esp_coredump` on the file and display the results.

***For demo visit: [abd-01.github.io/esp32-guru-upload/coredump/coredump-1758023059.elf](https://abd-01.github.io/esp32-guru-upload/coredump/coredump-1758023059.elf)***

[http://localhost:8080/upload](https://abd-01.github.io/esp32-guru-upload/coredump/) is the endpoint that receives the coredump via POST method.

The ESP32 is also running an HTTP server which can be viewed at [http://localhost:8080/esp_server](https://abd-01.github.io/esp32-guru-upload/esp_server/)

## License

GNU Affero General Public License v3.0 (AGPL-3.0). See [LICENSE](https://github.com/ABD-01/esp32-guru-upload/blob/master/LICENSE) for details.
