import re
from .generic import GenericExplainer
from ..instruction_docs import ual_instructions


reg = re.compile("B[LNEG][ETQ]")


class UALExplainer(GenericExplainer):
    instruction_docs = ual_instructions

    def canonicalize_name(self, instruction):
        out = str(instruction).strip().upper()
        if reg.match(out):
            return "B"
        return out
