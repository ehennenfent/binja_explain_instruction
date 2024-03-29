# Explain Instruction plugin for Binary Ninja
This plugin adds a sidebar window to Binary Ninja that explains in simple English what an assembly instruction does.

![Example Screenshot](https://raw.githubusercontent.com/ehennenfent/binja_explain_instruction/master/Examples/screenshot.png)

## Examples
The explanations are closer to English than the notation used in Binary Ninja, but may sometimes be strangely worded due to the fact that they are programmatically generated.
```
mov edx, 0x11
----
Sets edx to 0x11
```
```
movsx eax, al
----
Sets eax to (4 sign-extended bytes from al)
```
```
leave
----
Sets rsp to rbp
Sets rbp to the 8 bytes at the top of the stack, then increments the stack pointer by 8.
```
```
add dword [rbp-0x54], 0xa
----
Copies ((the 4 bytes of memory starting at (rbp + -0x54)) + 0xa) into memory at address (rbp + -0x54) (4 bytes)
```

## Assumed Knowledge Level
The descriptions are intended to be simple enough for a novice to understand. They assume basic knowledge of computer architecture concepts, like registers, the stack, CPU flags, etc. Consider taking a look at [Beginners.re](https://beginners.re/) if you need help with the background.

## Limitations
There are over 600 instructions in the current x86 instruction set alone. Rather than attempt to parse them all, the explanations here are generated by reading the corresponding Binary Ninja Low-Level Intermediate Language (LLIL), which operates at a higher level. LLIL covers most (but not all) of the x86 instruction set. A small portion of the x86 instructions with no LLIL equivalent have been added, but many are still missing. This project will aid beginners in understanding what common instructions do, and will hopefully help with some of those "What on earth does that instruction do?" moments, but probably can't replace consulting the documentation.

Since this project is based on LLIL, it may provide useful results on architectures other than x86. Rudimentary documentation has been added for MIPS, MSP430, UAL (ARM32 and Thumb-2), ARM64, and 6502. However, these architectures have not been subject to as much testing as x86 - indeed, many of them are completely untested, and thus unlikely to meet any reasonable standard of completeness. Pull requests to improve support for additional architectures are very welcome!

LLIL can have a number of quirks that may not be obvious to most Binary Ninja users. This plugin takes steps to mitigate such quirks, which are documented in the [IL Manifest](https://github.com/ehennenfent/binja_explain_instruction/blob/master/IL_MANIFEST.md).

## Contributing
This plugin is designed to make it simple to add support for new LLIL instructions or additional architectures. See [CONTRIBUTING.md](https://github.com/ehennenfent/binja_explain_instruction/blob/master/CONTRIBUTING.md). If you come across any inaccuracies, please file a pull request or create an issue.

## Miscellany
The icon for Explain Instruction is [blackboard by lastspark from the Noun Project](https://thenounproject.com/term/blackboard/367906/)