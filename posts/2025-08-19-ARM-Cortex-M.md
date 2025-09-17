---
myst:
    html_meta:
        "property=og:title": "ARM Cortex M Hardfault Handling"
        "language": "en"
---
```{post} August 19, 2025
---
author: me
category: embedded-systems
language: English
title: ARM Cortex M Hardfault Handling
tags: embedded-systems, arm-cortex, hardfault, panic-handler
exclude:
---

ARM Cortex-M HardFault handling with focus on exception and interrupt behavior, exception return flow, stack usage, and debugging scenarios. Includes references from The Definitive Guide to ARM Cortex-M3/M4 Processors and practical STM32 examples such as startup code, UART I/O, and fault diagnosis.
```

{.hiddenh1}
# ARM Cortex M Hardfault Handling

```{admonition} Draft Status
:class: danger

This page is a public collection of my raw, unorganized notes on this topic. 

It is *not a polished article*. The content and any links are subject to change without notice. Please check back for the final version.
```

## ARM Cortex M3 Hardfault Handling

```{admonition} 7.1 Overview of exceptions and interrupts
:class: hint

- The Cortex-M3 and Cortex-M4 NVIC supports up to 240 IRQs (Interrupt Requests), a Non-Maskable Interrupt (NMI), a SysTick (System Tick) timer interrupt, and a number of system exceptions.
- Exceptions are numbered 1-15 for system exceptions and 16 and above for interrupt inputs
- The exception number is used as the identification for each exception and is used in various places in the ARMv7-M architecture. For example, the value of the currently running exception is indicated by the special register Interrupt Program Status Register (IPSR), or by one of the registers in the NVIC called the Interrupt Control State Register (the VECTACTIVE field)

Ref: *The Definitive Guide to ARM® CORTEX®-M3 and CORTEX®-M4 Processors*, Chapter 7, Page 230
```

IPSR is one of the register from the xPSR

```{admonition} 4.5.1 What are exceptions?
:class: hint
 
Reset is a special kind of exception. When the processor exits from a reset, it executes the reset handler in Thread mode (rather than Handler mode as in other exceptions). Also the exception number in IPSR is read as zero.
 
Ref: *The Definitive Guide to ARM® CORTEX®-M3 and CORTEX®-M4 Processors*, Chapter 4, Page 106
```

```{admonition} 10.3 SVC exception
:class: hint

When the SVC handler is executed, you can determine the immediate data value in the SVC instruction by reading the stacked Program Counter (PC) value, then reading the instruction from that address and masking out the unneeded bits. However, the program that executed the SVC could have either been using the main stack or the process stack. So we need to find out which stack was used for the stacking process before extracting the stacked PC value. 
 
Ref: *The Definitive Guide to ARM® CORTEX®-M3 and CORTEX®-M4 Processors*, Chapter 10, Page 332
```

```{admonition} 4.2.2 link register (LR)
:class: hint

During exception handling, the LR is also updated automatically to a special EXC_RETURN (Exception Return) value, which is then used for triggering the exception return at the end of the exception handler. 

Ref: *The Definitive Guide to ARM® CORTEX®-M3 and CORTEX®-M4 Processors*, Chapter 4, Page 80
```

When returning from an exception, such as `pop {r7, pc}` or `bx lr` causes jump to `EXC_RETURN` whose value is `0xFFFFFFxx`. Based on the pattern of `EXC_RETURN` it pops the saved state from the stack, restores the `PC` to interrupted instruction, restores `xPSR` and other registers saved during exception entry

```{admonition} 7.7.3 Exception handler execution
:class: hint

 
At the end of the exception handler, the program code executes a return that causes the EXC_RETURN value to be loaded into the Program Counter (PC). This triggers the exception return mechanism.

Ref: *The Definitive Guide to ARM® CORTEX®-M3 and CORTEX®-M4 Processors*, Chapter 7, Page 251

Read *Chapter 8 Exception Handling in Detail* for details.
```

````{admonition} 4.2.3 Special Registes
:class: hint

```{image} ARM-Cortex-M-media/Special-Registers.png
:alt: Special Registers.png
:align: center
```

|      | 31  | 30  | 29  | 28  | 27  | 26:25  | 24  | 23:20 | 19:16 | 15:10  |  9  |        8:0         |
| :--: | :-: | :-: | :-: | :-: | :-: | :----: | :-: | :---: | :---: | :----: | :-: | :--------------: |
| xPSR |  N  |  Z  |  C  |  V  |  Q  | ICI/IT |  T  |       |  GE\* | ICI/IT |     | Exception Number |

Ref: *The Definitive Guide to ARM® CORTEX®-M3 and CORTEX®-M4 Processors*, Chapter 4, Page 82, Figure 4.6

````

### Fault status registers

> Ref: *12.4 Fault status registers and fault address registers*, _The Definitive Guide to ARM® CORTEX®-M3 and CORTEX®-M4 Processors_, Page 386

#### HFSR (HardFault Status Register)

`HFSR` is Hard Fault status register which gives hint to the cause of Hard fault
Located at `0xE000ED2C` and can be access via `SCB->HFSR` when using CMSIS Pack

| Bits | Name     | Type | Reset Value | Description                                                                                 |
| ---- | -------- | ---- | ----------- | ------------------------------------------------------------------------------------------- |
| 31   | DEBUGEVT | R/Wc | 0           | Indicates hard fault is triggered by debug event                                            |
| 30   | FORCED   | R/Wc | 0           | Indicates hard fault is taken because of bus fault, memory management fault, or usage fault |
| 29:2 | –        | –    | –           | –                                                                                           |
| 1    | VECTBL   | R/Wc | 0           | Indicates hard fault is caused by failed vector fetch                                       |
| 0    | –        | –    | –           | –                                                                                           |

#### CFSR (Configurable Fault Status Register)
- Hint information for causes of fault exceptions
- Address: `0xE000ED28`
It is further subdivided into 3 parts
CFSR (Configurable Fault Status Register, at `SCB->CFSR`) → 32 bits:
- Bits [0–7] : MMFSR (MemManage Fault Status Register)
- Bits [8–15]: BFSR (BusFault Status Register)
- Bits [16–31]: UFSR (UsageFault Status Register)

#### MMFAR (0xE000ED34) → faulting address for MemManage
    
#### BFAR (0xE000ED38) → faulting address for BusFault

#### Example Scenario: 
Hardfault with `HFSR`: `0x 4000 0000`  
Bit `30` is `1` i.e. it is a Forced.  
This means the HardFault is not direct, but an escalation from another fault type (MemManage, BusFault, UsageFault) that was either:  
- Disabled, or
- Had lower priority, so it escalated to HardFault.

Reading `CFSR`: `0b 0000 0000 0000 0000 1000 0010 0000 0000`  

This points to Bus Fault as bits `8:15` have values set.   
`CFSR`'s bit `15` states `BFAR` (Bus fault address register is valid)  
`CFSR`'s bit `9` states `BFAR` (Precise data bus error on a load/store)  

Reading `BFAR`: `0x 4002 1018` which is `RCC_APB2ENR`  

This register on `STM32F1` is used to enable/disable clocks for peripherals on `APB2` (in my case `USART1`)



## ARM Cortex-M CPUs

Important Slides: [Introduction to ARM Systems-11-12-2012.pptx](https://www.opensecuritytraining.info/IntroARM_files/Introduction%20to%20ARM%20Systems-11-17-2012.pdf)

[3. The STM32L476 microcontroller — Embedded Systems II documentation](https://tha.de/~hhoegl/home/es2/skript/stm32l4.html)

An architecture is a specification to what all functionality a processor must have.
Micro-Architecture is the actual implementation of it.

Eg:
Mv6,v7,v8 defines what cpu should do how it should behave.
The implementation looks like Cortext-M3,M4, M23, M33

ARM CPUs are based on the load/store architecture which is also RISC architecture

ARM TDMI 7 -> 7th version of the 32bit architecture.

A class: application grade, can run high level operating systems.

ARM v8 A class -> 64 bit CPUs
Now knows as AArch64 architecture.

ARM M class: for simple state machines, microcontrollers

Class R: Real time systems, deterministic system, eg: ECU

```{image} ARM-Cortex-M-media/Arm-Processor-Family.png
:alt: Arm Processor Family.png
:align: center
:width: 800px
````

Ref: [Cortex-M for Beginners](https://community.arm.com/cfs-file/__key/communityserver-discussions-components-files/18/Cortex_2D00_M-for-Beginners-_2D00_-2017_5F00_EN_5F00_v2.pdf)

```{image} ARM-Cortex-M-media/ARM-Cortex-M4-Programmers-Model.png
:alt: ARM Cortex M4 Programmer's Model.png
:align: center
:width: 800px
```

> Ref: [Cortex-M for Beginners](https://community.arm.com/cfs-file/__key/communityserver-discussions-components-files/18/Cortex_2D00_M-for-Beginners-_2D00_-2017_5F00_EN_5F00_v2.pdf)


16 General purpose registers.

![Cortex M3 Implementation|1000](https://documentation-service.arm.com/static/5ea823e69931941038df1b16?token=)


```{image} ARM-Cortex-M-media/Cortex-M3-Implementation.png
:alt: Cortex M3 Implementation.png
:align: center
```

  - WIC: wake-On Interrupt controller
  - MPU: memory protection unit
  - NVIC: Nested Vector Interrupt Controller

<!-- end list -->

```{image} ARM-Cortex-M-media/Cortex-M3-peripherals.png
:alt: Cortex-M3 peripherals.png
:align: center
:width: 500px
```

> Ref: [Cortex-M3 Devices Generic User Guide](https://developer.arm.com/documentation/dui0552/a/introduction/about-the-cortex-m3-processor-and-core-peripherals/cortex-m3-core-peripherals?lang=en)

```{image} ARM-Cortex-M-media/processor-modes.png
:alt: processor modes.png
:align: center
:width: 500px
```

CPU starts in Thread Mode - Privileged

### Stacks

  - Handler mode is where interrupts are handled
  - 2 registeres for 2 potential stacks: MSP (main stack pointer) and PSP (process stack pointer)
  - CPU boots using the MSP
  - Handler Mode uses MSP only
  - Privileged Thread Mode can use PSP or MSP, Unprivilegedd uses PSP

> Ref: [Cortex-M3 Devices Generic User Guide](https://developer.arm.com/documentation/dui0552/a/the-cortex-m3-processor/programmers-model/stacks?lang=en)

```{image} ARM-Cortex-M-media/Core-Registers.png
:alt: Core Registers.png
:align: center
:width: 500px
```

The *Program Status Register* (PSR) in Cortex M combines:

  - *Application Program Status Register* (APSR)
  - *Interrupt Program Status Register* (IPSR)
  - *Execution Program Status Register* (EPSR).

<!-- end list -->

```{admonition} Reference
:class: note

Might be useful: [embedded - ARM Cortex M3 How do I determine the program counter value before a hard fault? - Stack Overflow](https://stackoverflow.com/questions/3764119/arm-cortex-m3-how-do-i-determine-the-program-counter-value-before-a-hard-fault?rq=3)

- [Using Cortex-M3/M4/M7 Fault Exceptions](https://www.keil.com/appnotes/files/apnt209.pdf) 
- [Cortex-M3 Fault Handlers - EmbDev.net](https://embdev.net/topic/170640#1636052)
```

There are 16 Expections. and after then rest are all interrupts.

```{image} ARM-Cortex-M-media/Vector-Table.png
:alt: Vector Table.png
:align: center
:width: 500px
```

Ref: [ARM Cortex-M for Beginners](https://community.arm.com/cfs-file/__key/telligent-evolution-components-attachments/01-2057-00-00-00-01-28-35/Cortex_2D00_M-for-Beginners-_2D00_-2017_5F00_EN_5F00_v2.pdf)

```{image} ARM-Cortex-M-media/Control-Register.png
:alt: Control Register.png
:align: center
:width: 500px
```

```{image} ARM-Cortex-M-media/PSR-Register.png
:alt: PSR Register.png
:align: center
:width: 500px
```

```{image} ARM-Cortex-M-media/Pasted-image-20250727011453.png
:alt: Pasted image 20250727011453.png
:align: center
:width: 500px
```

```{image} ARM-Cortex-M-media/Cortex-M0-M3-and-M4.png
:alt: Cortex M0. M3 and M4.png
:align: center
:width: 700px
```

### Assembly

Plain text file
Extension:
`.s`: pre-processor is not run
`.S`: pre-processor is run on this file
In file you have: *directives*, *labels*, *comments* and *instructions*

  - Directives: mostly starts with a dot (`.`). Hints for the assembly
  - Labels: anything that has a colon (`:`) in the end. It is a human-readable name to a location.
  - 
Example:

```s
.section .vectors
vector_table:
	.word    0xABCD
	.word    reset_handler
	.zero    400

	.section .text
	.aign    1
	.type    reset_handler, %function
reset_handler:
	mov    r1, #0x7
	mov    r2, #0x3
	add    r3, r1, r2
	bl     .
```

### Instructions in ARM Cortex-M3

> See: [Instruction set summary - Cortex-M3 Devices Generic User Guide](https://developer.arm.com/documentation/dui0552/a/the-cortex-m3-instruction-set/instruction-set-summary?lang=en)

## MRS

Move the contents of a special register to a general-purpose register.

```asm
MRS{cond} Rd, spec_reg
```

### MSR

Move the contents of a general-purpose register into the specified special register.

```asm
MSR{cond} spec_reg, Rn
```

`spec_reg` can be any of: `APSR`, `IPSR`, `EPSR`, `IEPSR`, `IAPSR`, `EAPSR`, `PSR`, `MSP`, `PSP`, `PRIMASK`, `BASEPRI`, `BASEPRI_MAX`, `FAULTMASK`, or `CONTROL`.

### Hello World

Using device STM32F100RBT6, see [STM32F100xx manual](https://www.st.com/resource/en/reference_manual/rm0041-stm32f100xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)  
The Flash starts at  `0x8000 0000`, and SRAM starts at `0x2000 0000`

Therefore, the linker script will be:

```c
ENTRY(reset_handler)

MEMORY
{
	FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 128K
}

SECTIONS
{
	.text :
	{
		KEEP(*(.isr_vector))
		*(.text)
	} >FLASH
}

_estack = 0x20000800;
PROVIDE(_estack = 0x20000800);
```

startup.c
```c
const uint32_t isr_vectors[] __attribute__((section(".isr_vector"))) = {
    (uint32_t)&_estack,
    (uint32_t) reset_handler,	/* code entry point */
    (uint32_t) nmi_handler,
    (uint32_t) hardfault_handler,
    (uint32_t) memmanage_handler,
    (uint32_t) busfault_handler,
    (uint32_t) usagefault_handler,
    0,
    0,
    0
};
```

main.c
```c
#include <stdint.h>
#include "reg.h"

#define USART_FLAG_TXE	((uint16_t) 1 << 7)

#define USARTx      USART1
#define USARTx_SR   USART1_SR
#define USARTx_DR   USART1_DR
#define USARTx_CR1  USART1_CR1

int puts(const char *str)
{
	while (*str) {
		while (!(*(USARTx_SR) & USART_FLAG_TXE));
		*(USARTx_DR) = *str++ & 0xFF;
	}
	return 0;
}

void main(void)
{
	*(RCC_APB2ENR) |= (uint32_t) (0x00000001 | 0x00000004);
	*(RCC_APB1ENR) |= (uint32_t) (0x00020000);

	/* USARTx Configuration */
	*(GPIOA_CRL) = 0x00004B00;
	*(GPIOA_CRH) = 0x44444444;

	*(USARTx_CR1) = 0x0000000C;
	*(USARTx_CR1) |= 0x2000;

	puts("Hello World!\n");

	while (1);
}
```


### Button Debouncing

```{image} ARM-Cortex-M-media/voltage-signal-when-button-is-pressed-or-released.png
:alt: voltage signal when button is pressed or released.png
:align: center
:width: 600px
```

```{image} ARM-Cortex-M-media/Button-Debounce-FSM.png
:alt: Button Debounce FSM.png
:align: center
:width: 600px
```

### Enabling `stdio` (fgets, printf) on Bare-metal STM32 with Newlib-nano

1.  **Objective**: Use `fgets()` and `printf()` over UART in a bare-metal STM32 project using `newlib-nano`.

#### Linker and Compiler Setup

  - Used `arm-none-eabi-gcc` instead of `ld` directly.
  - Removed `-nostdlib` to allow standard libc dependencies.
  - Used flags:

<!-- end list -->

```sh
-mcpu=cortex-m3 -mthumb -mfloat-abi=soft
-nostartfiles --specs=nano.specs -lc -lnosys
-Wl,-Tlinker.ld,--print-memory-usage,-Map=kernel.map
```

#### UART I/O Functions

Implemented minimal UART functions for newlib-nano hooks:

```c
int __io_putchar(int ch) {
    while (!(*USARTx_SR & USART_FLAG_TXE));
    *USARTx_DR = ch & 0xFF;
    return ch;
}

int __io_getchar(void) {
    while (!(*USARTx_SR & USART_FLAG_RXNE));
    return *USARTx_DR & 0xFF;
}
```

#### Syscalls Implementation

Defined `_read()` to hook `fgets()`:

```c
int _read(int file, char *ptr, int len) {
    int i;
    for (i = 0; i < len; ++i) {
        ptr[i] = __io_getchar();
        if (ptr[i] == '\n' || ptr[i] == '\r') break;
    }
    return i;
}
```

Linked with `-lc -lnosys`.

#### Runtime Behavior

  - `fgets()` worked after correctly linking and implementing `_read`.
  - Needed to disable buffering for `stdout`:

<!-- end list -->

```c
setvbuf(stdout, NULL, _IONBF, 0);
```
    
This ensures immediate UART output with `printf()`.

```c
char RxBuf[32];
setvbuf(stdout, NULL, _IONBF, 0);
while (1) {
    if (fgets(RxBuf, sizeof(RxBuf), stdin)) {
        printf("Received: %s\n", RxBuf);
    }
}
```

> Possible Reference:
>
>   - [How stack trace on ARM works. Some time ago I faced a small problem… | by alexkalmuk | Medium](https://alexkalmuk.medium.com/how-stack-trace-on-arm-works-5634b35ddca1)


### Something about addr2line that I do not understand

```{image} ARM-Cortex-M-media/stack-unwind-commitid-0a0d814.png
:alt: stack-unwind-commitid-0a0d814.png
:align: center
```

````{admonition} addr2line (AI Generated)
:class: info

**You ran:**

```python
x/x 0x080001f4
```

Got:

```
0x080001f4 <uart_init+72>:  0x40021018
```

And:

```bash
addr2line 0x080001f4
```

→ points to **end of `uart_init`**

#### **Why this happens:**

1. **Literal Pools in ARM/Thumb**:
    - ARM stores constants (like peripheral addresses) near code in Flash.
    - These are not instructions — they're just **data embedded in the `.text` section**.
    - Placed usually at the **end of a function** (or sometimes in-between if needed).
        
2. **Disassembler confuses literal as code**:
    - `addr2line` assumes all `.text` is code, not data.
    - So it maps `0x080001f4` to the last instruction of `uart_init`, even though it's **actually a literal constant** used earlier.
        

#### **What's really at 0x080001f4:**

A 32-bit value:

```bash
0x40021018  → some peripheral register (likely RCC or similar on STM32)
```

#### **Conclusion:**
- `0x080001f4` is a **literal (constant address)** stored in Flash.
- GDB disassembled it correctly.
- `addr2line` doesn't differentiate between code and data in `.text`.
- This is **normal and expected behavior** in ARM systems using literal pools.
    
````

### Calling convention

I have notices different function prologues and epilogues at different functions

[assembly - What registers to save in the ARM C calling convention? - Stack Overflow](https://stackoverflow.com/questions/261419/what-registers-to-save-in-the-arm-c-calling-convention)

See AAPCS (ARM Architecture Procedure Call Standard) docs at [abi-aa/aapcs32/aapcs32.rst at main · ARM-software/abi-aa](https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst#the-base-procedure-call-standard)

### Check if inside an ISR

```c
bool memfault_arch_is_inside_isr(void) {
  // We query the "Interrupt Control State Register" to determine
  // if there is an active Exception Handler
  volatile uint32_t *ICSR = (uint32_t *)0xE000ED04;
  // Bottom byte makes up "VECTACTIVE"
  return ((*ICSR & 0xff) != 0x0);
}
```

### Notes from [ARM System Developer's Guide: Designing and Optimizing System Software - Andrew Sloss, Dominic Symes, Chris Wright](https://books.google.co.in/books?id=vdk4ZGRqMskC&redir_esc=y)

```{image} ARM-Cortex-M-media/nested-interrupt-handler.png
:alt: nested interrupt handler.png
:align: center
:width: 600px
```

```{image} ARM-Cortex-M-media/reenterent-interrupt-handler.png
:alt: reenterent interrupt handler.png
:align: center
:width: 600px
```

````{admonition} Pipelining (AI Generated)
:class: info


- **Pipelining** means splitting instruction execution into smaller stages (fetch, decode, execute, etc.) so multiple instructions are in different stages at once.
    
    - Example: While instruction A is being executed, instruction B can be decoded, and instruction C can be fetched — all in the same clock cycle.
        
- **"Pipeline advances by one step on each cycle"** means that in the best case, every clock tick pushes each instruction to the next stage — so one instruction finishes every cycle (max throughput).
    
- **"Decoded in one pipeline stage"** → ARM's simpler RISC instructions are designed so decoding is quick and predictable, done in a single stage, unlike some CISC CPUs that need more complex decoding.
    
- **"No microcode"** → In CISC processors (like x86), a single complex instruction might be internally translated into several simpler “micro-ops” by running a small _microprogram_ (microcode). ARM avoids this — instructions map directly to hardware actions, which makes them faster and simpler to pipeline.
    

**In short:** ARM's RISC design means each instruction flows directly through the pipeline without microcode translation, making execution more predictable and efficient.

```{image} ARM-Cortex-M-media/5-stage-instruction-pipeline.png
:alt: 5 stage instruction pipeline.png
:align: center
:width: 600px
```
````


````{admonition} Microcode (AI Generated)
:class: info

In a CISC CPU (like x86), **microcode** is a hidden layer of firmware inside the processor that translates complex instructions into a sequence of simpler, internal operations (_micro-operations_ or _micro-ops_) that the hardware can actually execute.

**Why it exists in CISC:**  
CISC ISAs often have instructions that are:

- Multi-step (e.g., `MOVS` with memory-to-memory move, or `REP MOVSB` to copy a block)
    
- Conditional or variable-length in execution
    
- Architecturally specified long before modern microarchitectures existed (for backward compatibility)
    

Since these instructions can't be directly hardwired into a simple datapath, the CPU stores a **microprogram** in ROM-like storage inside the chip.  
When the CPU sees such an instruction, it:

1. Uses the opcode to look up a _microcode entry_.
    
2. Runs the microcode sequence (like a tiny program) to orchestrate internal hardware: ALUs, registers, buses, memory accesses.
    

**Example (x86)**

```asm
LODSB     ; Load byte from [SI] into AL, increment SI
```

Internally might become micro-ops like:

```
uop1: Read from memory at SI into temp_reg
uop2: Move temp_reg to AL
uop3: Increment SI
```

These uops are executed by the pipeline as if they were normal simple instructions.

**ARM's RISC difference:**  
ARM avoids microcode for regular instructions — each instruction directly corresponds to a fixed set of hardware control signals that can be triggered in one or a few cycles. No “hidden” microprogram is needed for decoding.

So when the book says _“no need for microcode”_, it's highlighting that ARM avoids this translation layer — which makes the pipeline simpler, faster, and more predictable.
````

```{image} ARM-Cortex-M-media/Advanced-Microcontroller-Bus-Architecture-Example.png
:alt: Advanced Microcontroller Bus Architecture Example.png
:align: center
:width: 600px
```

````{admonition} Inline Barrel Shifter (AI Genrated)
:class: info

This is about one of ARM's classic RISC “superpowers” — the **inline barrel shifter**.

**What it is:**  
A **barrel shifter** is hardware that can shift or rotate a binary value by any number of bits in a single cycle.

**Why “inline”:**  
In ARM, the barrel shifter is built _into the datapath before the ALU_. This means that for most ALU instructions, **one operand can be shifted or rotated automatically before the arithmetic/logic is done** — without using a separate instruction.

**Example** (simplified):

```asm
ADD   R0, R1, R2, LSL #3
```

Meaning:

```
R0 = R1 + (R2 << 3)
```

Here, `(R2 << 3)` is done by the inline barrel shifter **inside the same ADD instruction**, so no extra `LSL` instruction is needed.

**Effect on “more complex instructions”:**

- A single ARM instruction can do **two things**: shift/rotate + arithmetic/logic.
    
- This makes the instruction set more powerful _without_ being true CISC — still fixed length, still single-cycle decode.
    

**Benefits:**

- **Performance**: fewer instructions to execute.
    
- **Code density**: smaller program size since shifts are “free” inside many instructions.
````

````{admonition} Interrupt Controller (AI Generated)
:class: info

**1. Standard interrupt controller vs. Vector Interrupt Controller (VIC)**

- **Standard interrupt controller**
    - Collects interrupt requests from peripherals.
    - Signals the CPU with a single “IRQ” line.
    - CPU must run _common ISR entry code_, then read a status register to figure out which device caused the interrupt.
    - More software work → slightly slower.
- **Vector Interrupt Controller (VIC)**
    - Each interrupt source is assigned a unique **vector address** in hardware.
    - When an interrupt happens, the VIC _directly provides_ the CPU with the address of the correct ISR.
    - No extra software dispatch needed — CPU jumps straight to the right handler.
    - Faster interrupt response.

Example:

```
Standard PIC flow:
IRQ -> CPU -> Common handler -> Read interrupt ID -> Branch to ISR

VIC flow:
IRQ -> CPU -> VIC gives ISR address -> CPU jumps straight there
```


**2. What does “nested VIC” mean?**

- **Nested** means you can service a higher-priority interrupt _while_ handling a lower-priority one.
- In a **nested VIC**, the hardware supports:
    - Multiple priority levels.
    - Automatic masking of lower-priority interrupts while in a higher-priority ISR.
    - Allowing high-priority IRQs to interrupt low-priority ISR execution.
        

Example:
- You're in a UART ISR (priority 3).
- A timer interrupt (priority 1 — higher priority) occurs.
- Nested VIC lets the timer interrupt preempt the UART ISR.
- After the timer ISR finishes, control returns to the UART ISR.
````

#### ARM Core Data Flow Model

```{image} ARM-Cortex-M-media/ARM-core-data-flow-model.png
:alt: ARM core data flow model.png
:align: center
:width: 600px
```

### Exception Entry

```{image} ARM-Cortex-M-media/Exception-Entry.png
:alt: Exception Entry.png
:align: center
:width: 600px
```

```{raw} html
<script>
window.onload=()=>(e=document.querySelector('.announcement-content'))&&(e.textContent='This page is in Draft phase.');
</script>
```