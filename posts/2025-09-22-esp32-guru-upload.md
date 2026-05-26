---
myst:
    html_meta:
        "property=og:title": "ESP32 Guru Meditation: Remote Crash Diagnostics"
        "language": "en"
---

```{post} September 22, 2025
---
author: Muhammed Abdullah
category: embedded-systems
language: English
title: "ESP32 Guru Meditation: Remote Crash Diagnostics"
tags: esp32, embedded-systems, coredump, qemu, flask
exclude:
---

I had been working on HardFault diagnostics for ARM Cortex-M — capturing crash logs on fault and storing them for later analysis. That naturally led me to look at how ESP32 handles the same problem, which is through its Guru Meditation mechanism. This post walks through a project that captures ESP32 coredumps to flash and uploads them over HTTP to a Flask server for remote analysis.
```

{.hiddenh1}
# ESP32 Guru Meditation: Remote Crash Diagnostics

## Background

Working on [HardFault diagnostics for ARM Cortex-M](https://abd-01.github.io/posts/2025-08-19-ARM-Cortex-M/) put me in the mindset of crash handling — what happens when the CPU panics, how do you capture state, and how do you retrieve it later without a JTAG cable plugged in. ESP32 solves this with Guru Meditation: when the firmware hits a fatal error, the IDF panic handler captures a coredump and can write it to a dedicated flash partition. The question is what you do with that dump afterwards.

The project is on GitHub: [ABD-01/esp32-guru-upload](https://github.com/ABD-01/esp32-guru-upload)  
Live demo: [abd-01.github.io/esp32-guru-upload](https://abd-01.github.io/esp32-guru-upload/coredump/)

{attribution="wikipedia.org/wiki/Guru_Meditation"}
> Guru Meditation is an error notice originally displayed by the Amiga computer when it crashes. It is analogous to the "Blue Screen of Death" in Microsoft Windows operating systems, or a kernel panic in Unix.

## Architecture

Three pieces, each doing one job:

1. **Firmware** — runs on real hardware or under QEMU, intentionally triggers a crash, detects the saved coredump on next boot, and streams it to the server
2. **Flask server** — receives the coredump via HTTP POST, stores it as an ELF file, and runs `idf.py coredump-info` on demand to produce a human-readable stack trace
3. **Dev container** — Docker image with ESP-IDF, the Espressif QEMU fork, and Flask pre-installed; works in GitHub Codespaces or locally

## Triggering the Crash

The crash is deliberate and crafted to produce an interesting stack trace. `crash_app.c` builds a few nested calls with randomized arguments and then writes to `0xDEADBEEF`:

```c
static int baz(int val) {
    if (val < 63 || val > 100) return 78;
    volatile uint32_t *bat_ptr = (uint32_t *)0xDEADBEEF;
    *bat_ptr = 0x12345678;   /* Guru Meditation */
}
```

The stack trace from the coredump then shows the full call chain:

```
==================== THREAD 1 (TCB: 0x3ffb94b0, name: 'CrashTask') =====================
#0  baz  (val=99)  at crash_app.c:49
#1  bar  (val=67)  at crash_app.c:36
#2  foo  (val=67)  at crash_app.c:28
#3  CrashTask (pvParameters=<optimized out>)  at crash_app.c:20
```

## Coredump to Flash

ESP-IDF's `menuconfig` provides a straightforward option to save coredumps in flash (as opposed to dumping over UART):

```
CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH=y
CONFIG_ESP_COREDUMP_DATA_FORMAT_ELF=y
```

On the next boot, `app_main` checks whether a coredump exists before doing anything else:

```c
esp_err_t err = esp_core_dump_image_get(&addr, &size);
if (err == ESP_OK) {
    /* coredump found — start upload task */
}
```

If one exists, an `UploadCoredumpTask` FreeRTOS task is spawned to handle the upload.

## Chunked HTTP Upload

The coredump can be 12 KB or more. Buffering the whole thing in RAM before sending would be a problem on a device with limited heap. Instead, `upload_coredump_app.c` reads the flash partition in 1 KB chunks and streams each one:

```c
while (offset < core_size) {
    esp_partition_read(coredump, offset + sizeof(uint32_t), buf, chunk_size);
    http_upload_send_chunk(client, buf, chunk_size);
    offset += chunk_size;
}
```

This is a standard pattern for resource-constrained devices but worth calling out explicitly — it keeps peak memory usage flat regardless of coredump size.

## QEMU Instead of Hardware

The standard `qemu-system-xtensa` does not support ESP32 targets. Espressif maintains a [fork of QEMU](https://github.com/espressif/qemu) with Xtensa patches. After building it from source, `esp32` appears in the machine list:

```bash
$ qemu-system-xtensa -M help
Supported machines are:
  esp32    Espressif ESP32 machine
  esp32s3  Espressif ESP32S3 machine
  ...
```

Launching the firmware with port forwarding so the Flask server on the host can receive the upload:

```bash
idf.py qemu --qemu-extra-args "-nic user,hostfwd=tcp::8081-:8080"
```

Inside the emulated machine, the device's port 8080 is forwarded to the host at 8081. The firmware is configured to POST to `10.0.2.2:8080` — the standard QEMU user-mode networking address for the host.

For a more detailed look at the QEMU setup see the [QEMU post](https://abd-01.github.io/posts/2025-07-15-QEMU/).

## Flask Server

The server is minimal — four routes:

| Route | Purpose |
|---|---|
| `GET /` | List all received coredumps |
| `POST /upload` | Receive a coredump, save as `.elf` |
| `GET /coredump/<file>` | Run `idf.py coredump-info`, display result |
| `GET /esp_server` | Iframe proxy to the ESP32's own HTTP server |

The analysis route calls the IDF tool directly:

```python
result = subprocess.run(
    ["idf.py", "coredump-info", "--core", str(filepath)],
    stdout=subprocess.PIPE, text=True
)
```

This is the same tool you would run manually at the terminal. The server just wraps it in a web interface so the output is accessible remotely.

## Demo

The static demo pages are hosted at:

- [coredump list](https://abd-01.github.io/esp32-guru-upload/coredump/) — example uploads
- [coredump analysis](https://abd-01.github.io/esp32-guru-upload/coredump/coredump-1758023059.elf/) — stack trace output
- [device log](https://abd-01.github.io/esp32-guru-upload/device_log/) — full firmware serial output
- [ESP32 web server](https://abd-01.github.io/esp32-guru-upload/esp_server/) — the device's own HTTP response
