import json, os

with open(os.path.expanduser("~") + '/.binaryninja/plugins/binja_explain_instruction/' + 'explanations_en.json', 'r') as explanation_file:
    explanations = json.load(explanation_file)



def preprocess_LLIL_CALL(bv, llil_instruction):
    func = bv.get_function_at(llil_instruction.dest.constant)
    if func is not None:
        llil_instruction.dest = func.name
    return llil_instruction

preprocess_dict = {
    "LLIL_CALL": preprocess_LLIL_CALL
}

def preprocess(bv, llil_instruction):
    if llil_instruction.operation.name in preprocess_dict:
        return preprocess_dict[llil_instruction.operation.name](bv, llil_instruction)
    return llil_instruction

def explain_llil(bv, llil_instruction):
    if llil_instruction.operation.name in explanations:
        return explanations[llil_instruction.operation.name].format(llil=preprocess(bv, llil_instruction))
    return llil_instruction.operation.name
