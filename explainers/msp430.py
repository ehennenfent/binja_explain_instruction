from .generic import GenericExplainer
from ..instruction_docs import msp430_instructions


class MSP430Explainer(GenericExplainer):
    instruction_docs = msp430_instructions
