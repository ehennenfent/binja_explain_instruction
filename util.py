def get_function_at(bv, addr):
    """Gets the function that contains a given address, even if that address
    isn't the start of the function"""
    blocks = bv.get_basic_blocks_at(addr)
    return blocks[0].function if (blocks is not None and len(blocks) > 0) else None


def find_mlil(func, addr):
    return find_in_IL(func.medium_level_il, addr)


def find_llil(func, addr):
    return find_in_IL(func.low_level_il, addr)


def find_lifted_il(func, addr):
    return find_in_IL(func.lifted_il, addr)


def find_in_IL(il, addr):
    """Finds everything at the given address within the IL function passed in"""
    out = []
    for block in il:
        for instruction in block:
            if instruction.address == addr:
                out.append(instruction)
    return out


def inst_in_func(func, addr):
    """Finds an assembly function at the address given"""
    return func.view.get_disassembly(addr)


def dereference_symbols(bv, il_instruction):
    """If the instruction contains anything that looks vaguely like a hex
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


def rec_replace(in_str, old, new):
    """Recursively replace a string in a string"""
    if old == new:
        return in_str
    if old not in in_str:
        return in_str
    return rec_replace(in_str.replace(old, new), old, new)


class AttrDict(dict):
    """Borrowed from https://stackoverflow.com/a/14620633. Lets us use the . notation
    in format strings."""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def parse_instruction(instruction):
    """Removes whitespace and commas from the instruction tokens"""
    tokens = filter(
        lambda x: len(x) > 0,
        [str(token).strip().replace(",", "") for token in str(instruction).split(" ")],
    )
    return list(tokens)
