from .generic import GenericExplainer
from ..instruction_docs import powerpc_instructions


class PowerPCExplainer(GenericExplainer):
    instruction_docs = powerpc_instructions
