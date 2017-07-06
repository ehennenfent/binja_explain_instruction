import json, traceback
from binaryninja import user_plugin_path, log_error
from ..explain import explain_llil

with open(user_plugin_path + '/binja_explain_instruction/x86/explanations_en.json', 'r') as explanation_file:
    explanations = json.load(explanation_file)

# List of instructions for which we'll just prepend the parsed LLIL explanation rather than
# replacing it entirely
dont_supersede_llil = ['cmp', 'test']

class AttrDict(dict):
    """ Borrowed from https://stackoverflow.com/a/14620633. Lets us use the . notation
    in format strings. """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def preprocess_cmp(bv, _parsed, lifted_il_instrs):
    """ Add IL tokens to make the message less generic """
    il = lifted_il_instrs[0]
    return AttrDict({'left': explain_llil(bv, il.left), 'right': explain_llil(bv, il.right)})

# Map instructions to function pointers
preprocess_dict = {
    "cmp": preprocess_cmp,
    "test": preprocess_cmp,
}

def parse_instruction(_bv, instruction, _lifted_il_instrs):
    """ Removes whitespace and commas from the instruction tokens """
    tokens = filter(lambda x : len(x) > 0, [str(token).strip().replace(',', '') for token in str(instruction).split(' ')])
    return tokens

def preprocess(bv, parsed, lifted_il_instrs):
    """ Apply preprocess functions to instructions """
    name = parsed[0]
    if name in preprocess_dict:
        out = preprocess_dict[name](bv, parsed, lifted_il_instrs)
        return out if out is not None else AttrDict({'name': name})
    return AttrDict({'name': name})

def arch_explain_instruction(bv, instruction, lifted_il_instrs):
    """ Returns the explanation string from explanations_en.json, formatted with the preprocessed instruction token list """
    if instruction is None:
        return False, None
    parsed = parse_instruction(bv, instruction, lifted_il_instrs)
    if(len(parsed) == 0):
        return False, None
    name = parsed[0]
    if name in explanations:
        try:
            # Get the string from the JSON and format it
            return name not in dont_supersede_llil, explanations[name].format(instr=preprocess(bv, parsed, lifted_il_instrs))
        except AttributeError:
            # Usually a bad format string. Shouldn't show up unless something truly weird happens.
            log_error("Bad Format String in binja_explain_instruction")
            traceback.print_exc()
            return False, name
    return False, None
