from .generic import GenericExplainer
from ..instruction_docs import aarch64_instructions


class AArch64Explainer(GenericExplainer):
    instruction_docs = aarch64_instructions

    def canonicalize_name(self, instruction):
        out = str(instruction).strip().upper()
        if "B." in out:
            return "B.cond"
        return out
