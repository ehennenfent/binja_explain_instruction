from .generic import GenericExplainer
from ..instruction_docs import asm6502_instructions


class Asm6502Explainer(GenericExplainer):
    instruction_docs = asm6502_instructions
