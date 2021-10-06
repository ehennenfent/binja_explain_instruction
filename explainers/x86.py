import re

from .generic import GenericExplainer
from ..explain import explain_llil
from ..instruction_docs import x86_instructions
from ..explanations import x86_explanations
from ..util import *

regexes = {
    "CMOV[A-Z][A-Z]?[A-Z]?": "CMOVcc",
    "J[A-L,N-Z][A-N,Q-Z]?[A-Z]?[A-Z]?": "Jcc",
    "SET[A-Z][A-Z]?[A-Z]?": "SETcc",
    "LOOP[A-Z][A-Z]?[A-Z]?": "LOOPcc",
    "FCMOV[A-Z][A-Z]?[A-Z]?": "FCMOVcc",
}

reg_cache = {}


def preprocess_cmp(bv, _parsed, lifted_il_instrs):
    """Add IL tokens to make the message less generic"""
    il = lifted_il_instrs[0]
    return AttrDict(
        {"left": explain_llil(bv, il.left), "right": explain_llil(bv, il.right)}
    )


def preprocess_setcc(bv, _parsed, lifted_il_instrs):
    """Replace instruction references with actual operations"""
    il = lifted_il_instrs[0]
    lifted = get_function_at(bv, il.address).lifted_il
    t, f = lifted[il.true], lifted[il.false]
    low_level = find_llil(get_function_at(bv, il.address), il.address)
    return AttrDict(
        {
            "true": explain_llil(bv, t),
            "false": explain_llil(bv, f).lower(),
            "condition": explain_llil(bv, low_level[0].condition),
        }
    )


def preprocess_cmovcc(bv, _parsed, lifted_il_instrs):
    """Replace instruction references with actual operations"""
    il = lifted_il_instrs[0]
    lifted = get_function_at(bv, il.address).lifted_il
    t = lifted[il.true]
    low_level = find_llil(get_function_at(bv, il.address), il.address)
    return AttrDict(
        {
            "true": explain_llil(bv, t),
            "condition": explain_llil(bv, low_level[0].condition),
        }
    )


class X86Explainer(GenericExplainer):
    instruction_docs = x86_instructions

    # List of instructions for which we'll just prepend the parsed LLIL explanation rather than
    # replacing it entirely
    dont_supersede_llil = {"cmp", "test"}

    # Map instructions to function pointers
    preprocess_dict = {
        "cmp": preprocess_cmp,
        "test": preprocess_cmp,
        "setcc": preprocess_setcc,
        "cmovcc": preprocess_cmovcc,
    }

    explanations = x86_explanations

    @staticmethod
    def canonicalize_name(instruction):
        global reg_cache
        """ Matches Jcc, CMOVcc, etc to their proper indices in the documentation dict """
        out = str(instruction).strip().upper()
        for regex in regexes:
            if regex not in reg_cache:
                reg_cache[regex] = re.compile(regex)
            reg = reg_cache[regex]
            if reg.match(out):
                out = regexes[regex]
                break
        return out

    def get_doc_url(self, i):
        """Takes in the instruction tokens and returns [(short form, doc url)]"""
        names = map(self.canonicalize_name, i)  # handles instruction prefixes
        output = []
        for name in names:
            if name in self.instruction_docs.keys():
                inst_data = self.instruction_docs[name][0]
                output.append((inst_data["short"], inst_data["link"]))
        # For 90% of instructions, output could just be a tuple and we could be done with it.
        # However, the lock and rep* prefixes should be documented too (to prevent major "WTH" moments)
        # so we have to structure everything around having a list of results
        return output
