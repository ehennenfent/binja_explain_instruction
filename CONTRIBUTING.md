
### Adding new LLIL instructions
For most instructions, this plugin parses the corresponding instruction in Binary Ninja's low level intermediate language. The file `explanations/generic_en.json` contains brief parameterized explanation strings for each type of IL instruction. Adding a new instruction is usually as simple as adding a new line to this file. However, if explaining an instruction requires performing a more sophisticated operation on the instruction object than Python's format strings allow for, you can add a preprocessing function to `explain.py` and add a reference to it in `preprocess_dict`

### Adding new x86 instructions
Like the LLIL instructions, adding a new x86 instruction can be as simple as adding a line to `explanations/native/x86_en.json`. However, if you have to do something complicated, you can modify `x86/explain.py` to add a preprocessing function. Note that if you don't want the description for this instruction to supersede the explanation produced by parsing the LLIL, you'll need to add it to the `dont_supersede_llil` list in `explainers/x86.py`.
