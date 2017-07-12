import json, traceback
from binaryninja import LowLevelILOperation, LowLevelILInstruction, log_info, log_error, user_plugin_path, ILFlag
from util import *

# Instruction attributes that can contain nested LLIL instructions (see preprocess)
expr_attrs = ['src', 'dest', 'hi', 'lo', 'left', 'right', 'condition']
# Types of instructions that we won't bother surrounding with parentheses because they don't
# substantially clarify anything.
no_paren = [LowLevelILOperation.LLIL_CONST, LowLevelILOperation.LLIL_REG,
LowLevelILOperation.LLIL_CONST_PTR, LowLevelILOperation.LLIL_POP, LowLevelILOperation.LLIL_FLAG]

with open(user_plugin_path + '/binja_explain_instruction/explanations_en.json', 'r') as explanation_file:
    explanations = json.load(explanation_file)

def preprocess_LLIL_CONST(_bv, llil_instruction):
    """ Replaces integer constants with hex tokens """
    llil_instruction.constant = llil_instruction.tokens[0]# hex(llil_instruction.constant).replace('L','')
    return llil_instruction

def preprocess_LLIL_CONST_PTR(bv, llil_instruction):
    """ Replaces integer constants with hex tokens """
    for symbol in bv.get_symbols():
        if symbol.address == llil_instruction.constant:
            llil_instruction.constant = symbol.name
            break
    return llil_instruction

def preprocess_LLIL_FLAG_COND(_bv, llil_instruction):
    """ Expands FLAG_COND enums """
    llil_instruction.condition = explanations[llil_instruction.condition.name]
    return llil_instruction

def preprocess_LLIL_GOTO(bv, llil_instruction):
    """ Replaces integer addresses of llil instructions with hex addresses of assembly """
    func = get_function_at(bv, llil_instruction.address)
    # We have to use the lifted IL since the LLIL ignores comparisons and tests
    lifted_instruction = list(filter(lambda k: k.operation == LowLevelILOperation.LLIL_GOTO , find_lifted_il(func, llil_instruction.address)))[0]
    lifted_il = func.lifted_il
    llil_instruction.dest = hex(lifted_il[lifted_instruction.dest].address).replace("L","")
    return llil_instruction

def preprocess_LLIL_IF(bv, llil_instruction):
    """ Replaces integer addresses of llil instructions with hex addresses of assembly """
    func = get_function_at(bv, llil_instruction.address)
    # We have to use the lifted IL since the LLIL ignores comparisons and tests
    lifted_instruction = list(filter(lambda k: k.operation == LowLevelILOperation.LLIL_IF , find_lifted_il(func, llil_instruction.address)))[0]
    lifted_il = func.lifted_il
    llil_instruction.true = hex(lifted_il[lifted_instruction.true].address).replace("L","")
    llil_instruction.false = hex(lifted_il[lifted_instruction.false].address).replace("L","")
    return llil_instruction

def preprocess_LLIL_FLAG(bv, llil_instruction):
    """ Follow back temporary flags and append the address where they're created """
    if llil_instruction.src.temp:
        flag = llil_instruction.ssa_form.src
        indx = llil_instruction.function.get_ssa_flag_definition(flag)
        src = llil_instruction.function[indx]
        llil_instruction.src = src.src
        llil_instruction.address = hex(llil_instruction.src.address).replace("L","")
    elif type(llil_instruction.src) == ILFlag:
        llil_instruction.src = bv.arch.flag_roles[llil_instruction.src.name].name.replace("Role","") + " is set"
        llil_instruction.address = "unknown"
    return llil_instruction

def preprocess_LLIL_REG(_bv, llil_instruction):
    """ Follow back temporary registers and append the address where they're created """
    if llil_instruction.src.temp:
        reg = llil_instruction.ssa_form.src
        indx = llil_instruction.function.get_ssa_reg_definition(reg)
        src = llil_instruction.function[indx]
        llil_instruction.src = src.src
        # Add a location flag so it's clear where in the program execution we actually got the source values from,
        # in case they've changed since then
        llil_instruction.loc = " (at instruction {})".format(hex(src.address).replace("L",""))
    else:
        llil_instruction.loc = ""
    return llil_instruction

# Map LLIL operation names to function pointers
preprocess_dict = {
    "LLIL_IF": preprocess_LLIL_IF, # Conditional jumps
    "LLIL_GOTO": preprocess_LLIL_GOTO, # Unconditional jumps
    "LLIL_CONST": preprocess_LLIL_CONST,
    "LLIL_CONST_PTR": preprocess_LLIL_CONST_PTR, # Seems to refer to a constant in .data - could consider dereferencing these
    "LLIL_FLAG_COND": preprocess_LLIL_FLAG_COND,
    "LLIL_REG": preprocess_LLIL_REG, # Registers (including temporary)
    "LLIL_FLAG": preprocess_LLIL_FLAG, # Temporary flags
}

def preprocess(bv, llil_instruction):
    """ Apply preprocess functions to instructions and expand explanations for nested LLIL operations """
    if llil_instruction.operation.name in preprocess_dict:
        out = preprocess_dict[llil_instruction.operation.name](bv, llil_instruction)
        llil_instruction = out if out is not None else llil_instruction
    # LLIL instructions are structured as trees of instructions. This loop iterates over the possible instruction attributes
    # that can contain a nested LLIL instruction and recursively explains them.
    for attr in expr_attrs:
        if hasattr(llil_instruction, attr): # Not all instructions will have the same attributes
            unexplained = llil_instruction.__getattribute__(attr)
            if type(unexplained) == LowLevelILInstruction: # Even if the attribute is there, it's sometimes just a string or an int
                # Overwrite the attribute with a string containing the recursive explanation for the nested instruction
                llil_instruction.__setattr__(attr, ("{}" if unexplained.operation in no_paren else "({})").format( explain_llil(bv, unexplained) ))
    return llil_instruction

def explain_llil(bv, llil_instruction):
    """ Returns the explanation string from explanations_en.json, formatted with the preprocessed LLIL instruction """
    if llil_instruction is None:
        return
    if llil_instruction.operation.name in explanations:
        try:
            # Get the string from the JSON and format it
            return explanations[llil_instruction.operation.name].format(llil=preprocess(bv, llil_instruction))
        except AttributeError:
            # Usually a bad format string. Shouldn't show up unless something truly weird happens.
            log_error("Bad Format String in binja_explain_instruction")
            traceback.print_exc()
            return llil_instruction.operation.name
    # If there's anything in the LLIL that doesn't have an explanation, yell about it in the logs
    log_info("binja_explain_instruction doen't understand " + llil_instruction.operation.name + " yet")
    return llil_instruction.operation.name

def fold_multi_il(_bv, llil_list):
    """ Filters out the setting of temporary registers and flags """
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
