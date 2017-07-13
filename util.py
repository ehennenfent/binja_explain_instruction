def get_function_at(bv, addr):
    """ Gets the function that contains a given address, even if that address
    isn't the start of the function """
    blocks = bv.get_basic_blocks_at(addr)
    return blocks[0].function if (blocks is not None and len(blocks) > 0) else None

def find_mlil(func, addr):
    return find_in_IL(func.medium_level_il, addr)

def find_llil(func, addr):
    return find_in_IL(func.low_level_il, addr)

def find_lifted_il(func, addr):
    return find_in_IL(func.lifted_il, addr)

def find_in_IL(il, addr):
    """ Finds everything at the given address within the IL function passed in """
    out = []
    for block in il:
        for instruction in block:
            if instruction.address == addr:
                out.append(instruction)
    return out

def inst_in_func(func, addr):
    """ Finds an assembly function at the address given """
    return func.view.get_disassembly(addr)

def dereference_symbols(bv, il_instruction):
    """ If the instruction contains anything that looks vaguely like a hex
    number, see if there's a function there, and if so, replace it with the
    function symbol."""
    if il_instruction is not None:
        out = []
        for item in il_instruction.tokens:
            try:
                addr = int(str(item), 16)
                func = bv.get_function_at(addr)
                if func is not None:
                    out.append(func.name)
                    continue
            except ValueError:
                pass
            out.append(item)
        il_instruction.deref_tokens = out
    return il_instruction
