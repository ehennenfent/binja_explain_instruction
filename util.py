def get_function_at(bv, addr):
    """ Gets the function that contains a given address, even if that address
    isn't the start of the function """
    blocks = bv.get_basic_blocks_at(addr)
    return blocks[0].function if blocks is not None else None

def find_mlil(func, addr):
    out = []
    for block in func.medium_level_il:
        for instr in block:
            if instr.address == addr:
                out.append(instr)
    return out

def find_llil(func, addr):
    first = func.get_low_level_il_at(addr)
    return find_in_IL(func.low_level_il, first)

def find_lifted_il(func, addr):
    first = func.get_lifted_il_at(addr)
    return find_in_IL(func.lifted_il, first)


def find_in_IL(il, first):
    """ Finds everything at the given address within the IL function passed in """
    out = []
    addr = first.address
    index = first.instr_index
    while(index < len(il)):
        if(il[index].address == addr):
            out.append(il[index])
        else:
            break
        index += 1
    return out

def inst_in_func(func, addr):
    """ Finds an assembly function at the address given """
    out = None
    for block in func:
        for i in block.disassembly_text:
            if i.address == addr:
                out = i
    return out

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
