import json, traceback
from binaryninja import LowLevelILOperation, LowLevelILInstruction, log_info, log_error, user_plugin_path
from util import *

# Instruction attributes that can contain nested LLIL instructions (see preprocess)
expr_attrs = ['src', 'dest', 'hi', 'lo', 'left', 'right', 'condition']
# Types of instructions that we won't bother surrounding with parentheses because they don't
# substantially clarify anything.
no_paren = [LowLevelILOperation.LLIL_CONST, LowLevelILOperation.LLIL_REG,
LowLevelILOperation.LLIL_CONST_PTR, LowLevelILOperation.LLIL_POP]

with open(user_plugin_path + '/binja_explain_instruction/explanations_en.json', 'r') as explanation_file:
    explanations = json.load(explanation_file)

def preprocess_LLIL_CALL(bv, llil_instruction):
    """ Replaces addresses with function names when available """
    func = bv.get_function_at(llil_instruction.dest.constant)
    if func is not None:
        llil_instruction.dest = func.name
    return llil_instruction

def preprocess_LLIL_CONST(_bv, llil_instruction):
    """ Replaces integer constants with hex tokens """
    llil_instruction.constant = llil_instruction.tokens[0]# hex(llil_instruction.constant).replace('L','')
    return llil_instruction

def preprocess_LLIL_FLAG_COND(_bv, llil_instruction):
    """ Expands FLAG_COND enums """
    llil_instruction.condition = explanations[llil_instruction.condition.name]
    return llil_instruction

def preprocess_LLIL_GOTO(bv, llil_instruction):
    """ Replaces integer addresses of llil instructions with hex addresses of assembly """
    llil = get_function_at(bv, llil_instruction.address).low_level_il
    llil_instruction.dest = hex(llil[llil_instruction.dest].address).replace("L","")
    return llil_instruction

def preprocess_LLIL_IF(bv, llil_instruction):
    """ Replaces integer addresses of llil instructions with hex addresses of assembly """
    llil = get_function_at(bv, llil_instruction.address).low_level_il
    llil_instruction.true = hex(llil[llil_instruction.true].address).replace("L","")
    llil_instruction.false = hex(llil[llil_instruction.false].address).replace("L","")
    return llil_instruction

# Map LLIL operation names to function pointers
preprocess_dict = {
    "LLIL_CALL": preprocess_LLIL_CALL,
    "LLIL_IF": preprocess_LLIL_IF, # I've only ever seen this used for conditional jumps
    "LLIL_GOTO": preprocess_LLIL_GOTO, # Unconditional jumps
    "LLIL_CONST": preprocess_LLIL_CONST,
    "LLIL_CONST_PTR": preprocess_LLIL_CONST, # Seems to refer to a constant in .data - could consider dereferencing these
    "LLIL_FLAG_COND": preprocess_LLIL_FLAG_COND
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
