import traceback
from dataclasses import FrozenInstanceError, dataclass

from binaryninja import (
    LowLevelILOperation,
    LowLevelILInstruction,
    ILFlag,
    BackgroundTaskThread,
    log_warn,
)

from .explanations import il_explanations as explanations
from .util import *

# Types of instructions that we won't bother surrounding with parentheses because they don't
# substantially clarify anything.
no_paren = {
    LowLevelILOperation.LLIL_CONST,
    LowLevelILOperation.LLIL_REG,
    LowLevelILOperation.LLIL_CONST_PTR,
    LowLevelILOperation.LLIL_POP,
    LowLevelILOperation.LLIL_FLAG,
}


@dataclass
class RecursiveExplainer:
    """Attempts to explain anything passed to __getattr__"""

    bv: BinaryView
    instruction: LowLevelILInstruction

    def __getattr__(self, item):
        if not hasattr(self.instruction, item):
            raise AttributeError(f"{self.instruction} has no attribute '{item}'")
        item = getattr(self.instruction, item)
        if isinstance(item, LowLevelILInstruction):
            return ("{}" if item.operation in no_paren else "({})").format(
                explain_llil(self.bv, item)
            )
        return item


def preprocess_LLIL_CONST(_bv, llil_instruction):
    """Get the rendered string Binja would use, since the values are signed"""
    return {"constant": llil_instruction.tokens[0]}


def preprocess_LLIL_CONST_PTR(bv, llil_instruction):
    """Replaces integer constants with symbols (if available) and hex tokens otherwise"""
    constant = None
    found_symbol = False
    for symbol in bv.get_symbols():
        if symbol.address == llil_instruction.constant:
            constant = symbol.name
            found_symbol = True
            break
    if not found_symbol:
        constant = to_hex(llil_instruction.constant)
    return {"constant": constant}


def preprocess_LLIL_FLAG_COND(_bv, llil_instruction):
    """Expands FLAG_COND enums"""
    return {"condition": explanations[llil_instruction.condition.name]}


def preprocess_LLIL_GOTO(bv, llil_instruction):
    """Replaces integer addresses of llil instructions with hex addresses of assembly"""
    func = get_function_at(bv, llil_instruction.address)
    # We have to use the lifted IL since the LLIL ignores comparisons and tests
    lifted_instruction = list(
        [
            k
            for k in find_lifted_il(func, llil_instruction.address)
            if k.operation == LowLevelILOperation.LLIL_GOTO
        ]
    )[0]
    lifted_il = func.lifted_il
    return {"dest": to_hex(lifted_il[lifted_instruction.dest].address)}


def preprocess_LLIL_IF(bv, llil_instruction):
    """Replaces integer addresses of llil instructions with hex addresses of assembly"""
    func = get_function_at(bv, llil_instruction.address)
    # We have to use the lifted IL since the LLIL ignores comparisons and tests
    lifted_instruction = list(
        [
            k
            for k in find_lifted_il(func, llil_instruction.address)
            if k.operation == LowLevelILOperation.LLIL_IF
        ]
    )[0]
    lifted_il = func.lifted_il
    return {
        "true": to_hex(lifted_il[lifted_instruction.true].address),
        "false": to_hex(lifted_il[lifted_instruction.false].address),
    }


def preprocess_LLIL_FLAG(bv, llil_instruction):
    """Follow back temporary flags and append the address where they're created"""
    source = llil_instruction.src
    address = llil_instruction.address

    if llil_instruction.src.temp:
        flag = llil_instruction.ssa_form.src
        indx = llil_instruction.function.get_ssa_flag_definition(flag).instr_index
        src = llil_instruction.function[indx]
        if hasattr(src, "src"):
            # Make sure that we're actually looking at a instruction that sets something (and not a Phi function)
            source = src.src
            address = to_hex(llil_instruction.src.address)
        elif type(llil_instruction.src == ILFlag):
            # Sometimes we have a temporary flag that resolves to a Phi function, which makes it show up at the same address.
            # Rather than try to build a conditional tree from the phi function (potentially impossible?) we default back to
            # the CPU flags.
            lifted_instruction = list(
                [
                    k
                    for k in find_lifted_il(
                        llil_instruction.function.source_function,
                        llil_instruction.address,
                    )
                    if k.operation == LowLevelILOperation.LLIL_IF
                ]
            )[0]
            source = lifted_instruction.condition
            address = "in multiple code paths"
    elif type(llil_instruction.src) == ILFlag:
        # On occasion, binja won't know what to do with a CPU flag and will use it "raw" without figuring
        # out what the conditional means. Happens with the direction flag on x86 sometimes.
        source = (
            bv.arch.flag_roles[llil_instruction.src.name].name.replace("Role", "")
            + " is set"
        )
        address = "unknown"
    return {"source": source, "address": address}


def preprocess_LLIL_REG(_bv, llil_instruction: LowLevelILInstruction):
    """Follow back temporary registers and append the address where they're created"""
    loc = ""
    source = llil_instruction.src
    if llil_instruction.src.temp:
        reg = llil_instruction.ssa_form.src
        src = llil_instruction.function.get_ssa_reg_definition(reg)
        if hasattr(src, "src"):
            # I've never seen it in the wild, but it's probably possible for a temporary variable to be sourced
            # from a Phi function on the same instruction, which could lead to infinite recursion
            source = src.src
            # Add a location flag so it's clear where in the program execution we actually got the source values from,
            # in case they've changed since then
            loc = " (at instruction {})".format(to_hex(src.address))
        else:
            loc = " (value dependent on code path used to reach this instruction)"
    return {"location": loc, "source": source}


# Map LLIL operation names to function pointers
preprocess_dict = {
    "LLIL_IF": preprocess_LLIL_IF,  # Conditional jumps
    "LLIL_GOTO": preprocess_LLIL_GOTO,  # Unconditional jumps
    "LLIL_CONST": preprocess_LLIL_CONST,
    "LLIL_CONST_PTR": preprocess_LLIL_CONST_PTR,  # Seems to refer to a constant in .data - could consider dereferencing these
    "LLIL_FLAG_COND": preprocess_LLIL_FLAG_COND,
    "LLIL_REG": preprocess_LLIL_REG,  # Registers (including temporary)
    # "LLIL_FLAG": preprocess_LLIL_FLAG,  # Temporary flags  # TODO: Fix flag handling
}


def preprocess(bv, llil_instruction):
    """Apply preprocess functions to instructions and expand explanations for nested LLIL operations"""
    environment = {
        # Any additional information for formatting explanations can be added here
        "llil": RecursiveExplainer(bv, llil_instruction),
        "arch": bv.arch,
    }
    environment.update(
        preprocess_dict.get(llil_instruction.operation.name, lambda *_: {})(
            bv, llil_instruction
        )
    )
    return environment


def explain_llil(bv, llil_instruction):
    """Returns the explanation string from explanations_en.json, formatted with the preprocessed LLIL instruction"""
    if llil_instruction is None:
        return None
    name = llil_instruction.operation.name
    if name in explanations:
        try:
            # Get the string from the JSON and format it
            return explanations[name].format(**preprocess(bv, llil_instruction))
        except FrozenInstanceError as e:
            # Trying to assign data to the LLIL instruction. Definitely a bug.
            raise e
        except AttributeError:
            # Usually a bad format string. Shouldn't show up unless something truly weird happens.
            log_error(traceback.format_exc())
            return name
    # If there's anything in the LLIL that doesn't have an explanation, yell about it in the logs
    log_warn(f"Explain Instruction doesn't understand {name} yet")
    return name


def fold_multi_il(_bv, llil_list):
    """Filters out the setting of temporary registers and flags"""
    out = []
    # This doesn't do any "folding" right now. In the future, we could fold temporary variables into
    # instructions that use them rather than seeking them in the preprocess functions, but there are some issues
    # with this. Notably, there's no way to accurately represent atomic combinations of instructions without temporary
    # variables, which means that we might present innacurate explanations if we just got rid of them entirely.
    # It might be possible to detect those cases, or a hypothetical LLIL_ATOMIC operation could save us from having
    # to think about it, but until I figure those out, this function is just going to be a simple filter.
    for llil in llil_list:
        if llil.operation == LowLevelILOperation.LLIL_SET_FLAG:
            pass
        elif llil.operation == LowLevelILOperation.LLIL_SET_REG and llil.dest.temp:
            pass
        else:
            out.append(llil)
    return out


def make_description(bv, arch_explainer, instruction, lifted_il_list, llil_list):
    # Typically, we use the Low Level IL for parsing instructions. However, sometimes there isn't a corresponding
    # LLIL instruction (like for cmp), so in cases like that, we use the lifted IL, which is closer to the raw assembly
    parse_il = fold_multi_il(bv, llil_list if len(llil_list) > 0 else lifted_il_list)
    # Give the architecture submodule a chance to supply an explanation for this instruction that takes precedence
    # over the one generated via the LLIL
    (
        should_supersede,
        explanation_list,
    ) = arch_explainer.explain_instruction(instruction, lifted_il_list)
    return explanation_list + (
        [] if should_supersede else [explain_llil(bv, llil) for llil in parse_il]
    )


class ThreadExplainer(BackgroundTaskThread):
    def __init__(
        self, bv, arch_explainer, instruction, lifted_il_list, llil_list, final_callback
    ):
        super().__init__(
            f"Generating Explanation for {fmt_instruction(instruction)}...",
            can_cancel=True,
        )
        self.bv = bv
        self.arch_explainer = arch_explainer
        self.instruction = instruction
        self.lifted_il_list = lifted_il_list
        self.llil_list = llil_list
        self.final_callback = final_callback
        self.descriptions = []

    def run(self):
        self.descriptions = make_description(
            self.bv,
            self.arch_explainer,
            self.instruction,
            self.lifted_il_list,
            self.llil_list,
        )

    def cancel(self):
        self.final_callback = lambda *_: None
        super().cancel()

    def finish(self):
        super().finish()
        self.final_callback(self.descriptions)
