from .generic import GenericExplainer
from ..instruction_docs import mips_instructions


class MipsExplainer(GenericExplainer):
    instruction_docs = mips_instructions
