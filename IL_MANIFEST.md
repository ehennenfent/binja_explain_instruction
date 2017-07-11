# IL Manifest
----
## Usage of the Binary Ninja Intermediate Languages in the Explain Instruction Plugin
Last updated 2017-July-11

For absolute beginners who are unaware: Binary Ninja's different IL views can be accessed through the options menu at the bottom right corner of the window. You can quickly switch between the Low Level IL and the assembly via the `i` key.

### Low Level IL
The Low Level Intermediate Language (LLIL) is Binary Ninja's way of representing many different versions of assembly in a consistent language over which it can perform powerful analysis. Rather than looking at the instructions themselves, this plugin usually reads the LLIL corresponding to an instruction in order to generate an explanation. This accomplishes multiple things:
1. It reduces the number of unique operations that need explanations by about 90% (from "completely infeasible" to "reasonable")
2. It abstracts away the need to parse the myriad ways an individual instruction can work
3. It provides a limited degree of compatibility with architectures other than x86

Most LLIL instructions are produced by nesting other LLIL instructions in a manner similar to a tree. The important fields on the LowLevelILInstruction object that we parse in the code are enumerated below:
* `address` - The address of the assembly instruction the LLIL instruction corresponds to
* `function` - The LLIL Function object that contains this instruction
* `instr_index` - The index of the instruction within the function
* `operation` - Member of the LowLevelILOperation enum that indicates what action this instruction performs
* `ssa_form` - The SSA (see below) form of the instruction
* `tokens` - The raw text tokens used to display the instruction
* Instruction specific attributes - Provide data about the instruction. Can contain strings ints, or most commonly, other LLIL instructions. Examples include `src`, `dest`, `constant`. See the `ILOperations` dictionary in the [source code](https://api.binary.ninja/_modules/binaryninja/lowlevelil.html#LowLevelILInstruction) for details.

For more information about the LowLevelILInstruction object, you can consult [the documentation](https://api.binary.ninja/binaryninja.lowlevelil.LowLevelILInstruction.html#binaryninja.lowlevelil.LowLevelILInstruction).

In order to explain an LLIL instruction, this plugin recursively follows all the instruction specific attributes that contain nested LLIL instructions and replaces them with explanation strings, flattening the entire explanation into a single string on the way up. Before an LLIL instruction is explained, it is run through a preprocessing function that will run the instruction through a function specific to its LLIL operation, in case any additional processing is needed before using it to format the explanation string. See `explain.py` to better understand this.

### Lifted IL
The Lifted Intermediate Language is a slightly simpler version of the LLIL that corresponds more closely to the assembly. It is not used very often in plugins because while there are very few differences between it and the LLIL, it lacks several useful features. Notably, it interprets conditionals based on the CPU flag state, whereas the LLIL directly folds the results of previous instructions into conditional statements. For this reason, we typically use the LLIL for generating explanations. However, in some cases (like `test` and `cmp`) the LLIL folds an instruction that exists only to set flags into a later conditional move/set/jump, so we fall back to Lifted IL when there is no LLIL available for an instruction.

In the case where a jump statement in the assembly lands on a `test` or a `cmp`, the addresses used by reading the LLIL destination of the jump are incorrect, since the LLIL ignores `test` and `cmp`. In this case, the preprocessor finds the lifted IL corresponding to the LLIL_GOTO or LLIL_IF in question, and overwrites the LLIL address with the lifted address.

While there is still not a 1-to-1 correspondence between the Lifted IL and the assembly, it is generally safer to assume that to be the case with the Lifted IL than with any other of the intermediate languages.

### Medium Level IL
The Medium Level Intermediate Language (MLIL) is a relatively high level interpretation of the LLIL that often greatly simplifies program logic. As noted in the limitations section of README.md, the MLIL and the assembly most definitely do not have a 1-to-1 relationship. This plugin doesn't use the MLIL for much of anything, although it does display it in the viewer, mostly because it makes it very easy to identify the arguments to a call instruction.

### Architecture-Specific Features
The links to the documentation for each instruction are not a part of Binary Ninja, so they must be implemented separately for each architecture. At this time, only documentation for x86 is included.

This plugin does not solely rely on the LLIL to generate explanations. Sometimes an architecture exhibits a behavior that has no equivalent in the LLIL, and sometimes the nuances of a specific instruction require a specific explanation to make clear. For cases like this, the plugin imports a function based on the architecture of the binary that can take the raw instruction tokens and return an instruction-specific explanation if one is available. This explanation will either prepend the explanation generated by parsing the LLIL or replace it entirely, depending on the output of the function.

### Temporary Variables
In many cases, the intermediate languages will create temporary registers or conditional flags to provide a simpler abstraction for the assembly. This is necessary to represent the way certain instructions work, as these instructions may do things that would correspond to multiple LLIL operations all at once (for instance, setting multiple registers) or make decisions based on the CPU flags, which the LLIL tries its best to abstract away. Though this is by no means an exhaustive list, several cases specific to x86 that have been observed to produce this behavior are listed below.
* The CPU flags are set by a `cmp` instruction, then one of the items involved in the comparison is modified before the conditional statement occurs
* The CPU flag are set by an instruction that stores its result in one of the operands
* One assembly instruction performs the equivalent of multiple LLIL operations (see `idiv` example below)

##### Example 1
The following example displays the second case:
```
0x400a7f:   xor rcx, rax
0x400a88:   je 0x400a8f

```
Which corresponds to the following LLIL:
```
0x400a7f:   temp0.q = rcx ^ rax
0x400a7f:   rcx = temp0.q
0x400a88:   if (temp0.q == 0) then 0x400a8f else 0x400a8a
```
And the jump instruction produces the following explanation:
```
Jumps to 0x400a8f if the CPU flags indicate that ((rcx ^ rax) (at instruction 0x400a7f) == 0), otherwise, falls through to 0x400a8a
```

Wherever possible, this plugin attempts to fold the expressions responsible for setting these registers/flags back into the LLIL instruction before producing an explanation. This is done by consulting the SSA form of the LLIL (explained below) and backtracing to the instruction that set the value of the register/flag. However, since the expression might not evaluate to the same result if executed as part of the conditional expression instead of when it was originally executed, explanations produced in this manner are annotated with "(at address 0x*****)" to indicate that the expression shown should be interpreted as executed at the address it actually appears at in the program, not the address of the current instruction. In the above example, note the annotation of "at instruction 0x400a7f" to indicate that the value of `rcx` is not the same if evaluated at `0x400a88` as it is at `0x400a7f`.

##### Example 2
Consider the instruction `idiv rxc`, which is lifted to the following LLIL:
```
115 @ 0x40069e  temp0.q = divs.dp.q(rdx:rax, rcx)
116 @ 0x40069e  temp1.q = mods.dp.q(rdx:rax, rcx)
117 @ 0x40069e  rax = temp0.q
118 @ 0x40069e  rdx = temp1.q
```
Now let's look at the explanation:
```
Sets rax to (rdx:rax / rcx (signed)) (at instruction 0x40069e)
Sets rdx to (rdx:rax % rcx (signed)) (at instruction 0x40069e)
```
Look closely at what's happened here. If you read the explanation, but don't take into account the annotations after each explanation noting the address in the program at which the source value is calculated, it looks as though the explanation and the LLIL itself say two different things. The second line of the explanation relies on `rax`, but `rax` is set in the first line. In contrast, the use of a temporary variable in the LLIL makes it very clear that the value that gets stored in `rdx` is calculated before `rax` is modified.

While the address annotation does provide an indication that the two explanations correspond to operations that are executed simultaneously, it's not the most clear way of showing it. If the LLIL included an operation that was used to wrap multiple other LLIL operations in order to indicate that they all correspond to one assembly instruction, this relationship would be easier to display. However, since the LLIL is meant to be a simpler language with which to break down the assembly, it is likely at odds with its goal to bundle operations into groups in such a manner.

The plugin does attempt to simplify blocks where a temporary register or flags was folded into another instruction by filtering instructions that do nothing but set a temporary register/flag out of the list of LLIL instructions that are passed to the explanation generator. While this could become confusing if an instruction references a temporary variable for which the assignment instruction has been filtered out of the explanation, at this time, this behavior would only occur due to a bug in this plugin that resulted in the temporary variable not being properly traced back to its source. If you encounter this problem, please feel free to file an issue.

### Conditional Instructions
While `Jcc` instructions are handled quite nicely by the LLIL, formerly, some conditional instructions such as `CMOVcc` and `SETcc` resulted in large blocks of LLIL that only made sense upon consulting the CFG. The explanations for these instructions have now been greatly improved by creating x86-specific functions to handle them. These functions now examine the `true` and `false` destinations of the LLIL_IF statement and replace them with explanations of the instructions residing at each of these locations. This compresses the explanation for several blocks of code down into a single line. See the preprocessing functions in `x86/explain.py` for more specifics.

### SSA Form
The Static Single Assignment (SSA) form view can look fairly intimidating if you've looked at it without already knowing what it is. Fortunately, SSA is actually fairly simple to understand. [This graph](https://en.wikipedia.org/wiki/Static_single_assignment_form#Converting_to_SSA) on wikipedia should make it fairly clear, but for the purposes of this section, there are only three things you need to understand:
* SSA Variables are only ever assigned once.
* Since the value of a variable never changes once assigned, every assignment statement creates a new variable.
* The Φ (Phi) function consolidates two versions of a variable into a third if the value is dependent on the code path that the program followed.

Both the Medium Level IL and the Low Level IL offer an SSA form. This plugin uses the SSA form of the LLIL in order to follow temporary registers and flags back to the place they were assigned. The LLIL Function object provides functions `get_ssa_flag_definition` and `get_ssa_reg_definition` to get the index of the LLIL instruction that sets a given SSA flag or variable.
