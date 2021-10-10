from dataclasses import dataclass
from traceback import format_exception
from typing import List, Optional

from binaryninja import (
    InstructionTextToken,
    LowLevelILInstruction,
    BinaryView,
    Function,
)

from ..explain import make_description
from ..explainers import explainer_for_architecture
from ..util import get_function_at, get_instruction, fmt_instruction


def _process_exception(exc):
    items = format_exception(type(exc), exc, exc.__traceback__, limit=-1)
    return ": ".join(token.rstrip("\n") for token in items[1:])


@dataclass
class InstructionData:
    address: int
    instruction: List[InstructionTextToken]
    lifted_il: List[LowLevelILInstruction]
    llil: List[LowLevelILInstruction]
    description: str
    exception: Optional[Exception]

    def __str__(self):
        if self.exception is not None:
            return (
                f"{self.address:x}: {fmt_instruction(self.instruction)} -!-> "
                f"{_process_exception(self.exception)}"
            )
        return f"{self.address:x}: {fmt_instruction(self.instruction)} ---> {' | '.join(self.description)}"

    def __hash__(self):
        return hash(self.address)


def get_instruction_data(
    bv: BinaryView, addr: int, instruction: Optional[List[InstructionTextToken]] = None
):
    function: Function = get_function_at(bv, addr)
    if instruction is None:
        instruction = get_instruction(bv, addr)
    lifted = function.get_lifted_ils_at(addr)
    llil = function.get_llils_at(addr)

    try:
        description = make_description(
            bv, explainer_for_architecture(bv.arch)(bv), instruction, lifted, llil
        )
        exception = None
    except Exception as e:
        description = []
        exception = e

    return InstructionData(
        address=addr,
        instruction=instruction,
        lifted_il=lifted,
        llil=llil,
        description=description,
        exception=exception,
    )
