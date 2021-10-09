import traceback

from ..util import *


class GenericExplainer:
    # For these instructions, prepend the LLIL instead of replacing it entirely
    dont_supersede_llil = set()

    # Map instructions to function pointers for preprocessing
    preprocess_dict = {}

    # Stores links and details for instruction docs
    instruction_docs = {}

    # Stores explanations for native instructions
    explanations = {}

    def __init__(self, bv: BinaryView):
        self.bv = bv

    @staticmethod
    def canonicalize_name(instruction):
        return str(instruction).strip().upper()

    def preprocess(self, parsed, lifted_il_instrs, name):
        """Apply preprocess functions to instructions"""
        if name in self.preprocess_dict:
            out = self.preprocess_dict[name](self.bv, parsed, lifted_il_instrs)
            return out if out is not None else AttrDict({"name": name})
        return AttrDict({"name": name})

    def explain_instruction(self, instruction, lifted_il_instrs):
        """Returns the explanation string from explanations_en.json,
        formatted with the preprocessed instruction token list"""
        if instruction is None:
            return False, []
        parsed = parse_instruction(instruction)
        if len(parsed) == 0:
            return False, []
        out = []
        should_supersede = False
        for name in parsed:
            name = self.canonicalize_name(name).lower()
            if name in self.explanations:
                try:
                    # Get the string from the JSON and format it
                    should_supersede = (
                        should_supersede or name not in self.dont_supersede_llil
                    )
                    out.append(
                        self.explanations[name].format(
                            instr=self.preprocess(parsed, lifted_il_instrs, name)
                        )
                    )
                except (AttributeError, KeyError):
                    # Usually a bad format string. Shouldn't show up unless something truly weird happens.
                    log_error(f"Bad Format String in {self.__name__}")
                    log_error(traceback.format_exc())
                    out.append(name)
        return should_supersede, out

    def get_doc_url(self, i):
        """Takes in the instruction tokens and returns [(short form, doc url)]"""
        names = map(self.canonicalize_name, i)  # handles instruction prefixes
        output = []
        for name in names:
            if name in self.instruction_docs.keys():
                inst_l = self.instruction_docs[name]
                for inst_data in inst_l:
                    output.append((inst_data["short"], inst_data["link"]))
        if len(output) == 0:
            return [
                (
                    "No documentation for that instruction!",
                    "https://github.com/ehennenfent/binja_explain_instruction/blob/master/CONTRIBUTING.md",
                )
            ]
        return output


class UnavailableExplainer(GenericExplainer):
    def explain_instruction(self, instruction, lifted_il_instrs):
        return False, ["Architecture-specific explanations unavailable"]

    def get_doc_url(self, i):
        return [
            (
                "No documentation available",
                "https://github.com/ehennenfent/binja_explain_instruction/blob/master/CONTRIBUTING.md",
            )
        ]
