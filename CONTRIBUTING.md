
### Adding new LLIL instructions
For most instructions, this plugin parses the corresponding instruction in Binary Ninja's low level intermediate language. The file `explanations_en.json` contains brief parameterized explanation strings for each type of IL instruction. Adding a new instruction can be as simple as adding a new line to this file. However, if explaining an instruction requires performing a more sophisticated operation on the instruction object than Python's format strings allow for, you can add a preprocessing function to `explain.py` and add a reference to it in `preprocess_dict`

### Adding new x86 instructions
Like the LLIL instructions, adding a new x86 instruction can be as simple as adding a line to `x86/explanations_en.json`. However, if you have to do something complicated, you can modify `x86/explain.py` to add a preprocessing function.

### Adding new architectures
1. Create a new submodule (`cp -rf x86 my_new_architecture` or something like that)
2. In `my_new_architecture/__init__.py` create a function that takes in an instruction as a list of tokens and returns a list of tuples, each containing the short name for an instruction and a url for the documentation.
3. In `my_new_architecture/explain.py` create a function that takes in an instruction as a list of tokens and returns a boolean indicating whether the description returned should prepend or replace the LLIL explanation and string explaining that instruction.
 * If you decide to use the existing `arch_explain_instruction` function in `x86/explain.py`, you can simply add instructions to `x86/explanations_en.json` to have them automatically preempt the default explanation.
4. In `__init__.py` modify the `init_plugin` function to import the functions for your architecture and bind them to the relevant variables
