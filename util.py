import typing

from PySide6.QtGui import QColor
from binaryninja import InstructionTextTokenType, InstructionTextToken, BinaryView
from binaryninja import log_error as binja_log_error


def get_function_at(bv, addr):
    """Gets the function that contains a given address, even if that address
    isn't the start of the function"""
    functions = bv.get_functions_containing(addr)
    return functions[0] if (functions is not None and len(functions) > 0) else None


def find_llil(func, addr):
    return func.get_llils_at(addr)


def find_lifted_il(func, addr):
    return func.get_lifted_ils_at(addr)


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


def colorize(
    color_map: typing.Dict[InstructionTextTokenType, QColor],
    tokens: typing.List[InstructionTextToken],
) -> typing.List[str]:
    color_format = "<font color={color}>{value}</font>"
    return list(
        color_format.format(
            color=color_map.get(token.type, QColor("white")).name(), value=str(token)
        )
        if len(str(token).strip()) > 0
        else " "
        for token in tokens
    )


def get_instruction(bv: BinaryView, addr: int) -> typing.List[InstructionTextToken]:
    arch = bv.arch
    tokens, _size = arch.get_instruction_text(
        bv.read(addr, arch.max_instr_length), addr
    )
    return tokens


def debug_instruction(bv, addr):
    print("Address:")
    print(" ", hex(addr))
    print("Architecture:")
    print(" ", bv.arch)
    print("bv.read:")
    print(" ", bv.read(addr, bv.arch.max_instr_length).hex())
    print("bv.get_disassembly:")
    print(" ", bv.get_disassembly(addr))
    function = bv.get_functions_containing(addr)[0]
    print("function.get_lifted_il_at:")
    print(" ", function.get_lifted_il_at(addr))
    print("function.get_lifted_ils_at:")
    print(" ", function.get_lifted_ils_at(addr))
    print("function.get_llil_at:")
    print(" ", function.get_llil_at(addr))
    print("function.get_llils_at:")
    print(" ", function.get_llils_at(addr))
    print("architecture.get_low_level_il_from_bytes:")
    print(
        " ",
        bv.arch.get_low_level_il_from_bytes(
            bv.read(addr, bv.arch.max_instr_length), addr
        ),
    )


def log_error(*args):
    binja_log_error(*args)
    binja_log_error(
        "Please consider submitting a bug report at "
        "https://github.com/ehennenfent/binja_explain_instruction/"
        "issues/new?assignees=&labels=bug&template=bug_report.md"
    )


def to_hex(i: int) -> str:
    return hex(i).rstrip("L")


def fmt_instruction(tokens):
    return "".join(
        str(token) if len(str(token).strip()) > 0 else " " for token in tokens
    )
