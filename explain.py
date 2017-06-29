import json, os, traceback
from binaryninja import LowLevelILOperation, LowLevelILInstruction, log_info, log_error

expr_attrs = ['src', 'dest', 'hi', 'lo', 'left', 'right', 'condition']
no_paren = [LowLevelILOperation.LLIL_CONST, LowLevelILOperation.LLIL_REG,
LowLevelILOperation.LLIL_CONST_PTR, LowLevelILOperation.LLIL_POP]

with open(os.path.expanduser("~") + '/.binaryninja/plugins/binja_explain_instruction/' + 'explanations_en.json', 'r') as explanation_file:
    explanations = json.load(explanation_file)

def preprocess_LLIL_CALL(bv, llil_instruction):
    func = bv.get_function_at(llil_instruction.dest.constant)
    if func is not None:
        llil_instruction.dest = func.name
    return llil_instruction

def preprocess_LLIL_CONST(_bv, llil_instruction):
    llil_instruction.constant = llil_instruction.tokens[0]# hex(llil_instruction.constant).replace('L','')
    return llil_instruction

def preprocess_LLIL_FLAG_COND(bv, llil_instruction):
    llil_instruction.condition = explanations[llil_instruction.condition.name]
    return llil_instruction

def preprocess_jump(_bv, llil_instruction):
    llil_instruction.dest = llil_instruction.tokens[-1]
    return llil_instruction

preprocess_dict = {
    "LLIL_CALL": preprocess_LLIL_CALL,
    "LLIL_IF": preprocess_jump,
    "LLIL_GOTO": preprocess_jump,
    "LLIL_CONST": preprocess_LLIL_CONST,
    "LLIL_CONST_PTR": preprocess_LLIL_CONST,
    "LLIL_FLAG_COND": preprocess_LLIL_FLAG_COND
}

def preprocess(bv, llil_instruction):
    if llil_instruction.operation.name in preprocess_dict:
        out = preprocess_dict[llil_instruction.operation.name](bv, llil_instruction)
        llil_instruction = out if out is not None else llil_instruction
    for attr in expr_attrs:
        if hasattr(llil_instruction, attr):
            unexplained = llil_instruction.__getattribute__(attr)
            if type(unexplained) == LowLevelILInstruction:
                llil_instruction.__setattr__(attr, ("{}" if unexplained.operation in no_paren else "({})").format( explain_llil(bv, unexplained) ))
    return llil_instruction

def explain_llil(bv, llil_instruction):
    if llil_instruction is None:
        return
    if llil_instruction.operation.name in explanations:
        try:
            return explanations[llil_instruction.operation.name].format(llil=preprocess(bv, llil_instruction))
        except AttributeError:
            log_error("Bad Format String in binja_explain_instruction")
            traceback.print_exc()
            return llil_instruction.operation.name
    log_info("binja_explain_instruction doen't understand " + llil_instruction.operation.name + " yet")
    return llil_instruction.operation.name
