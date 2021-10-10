import json
from pathlib import Path

from binaryninja import LowLevelILOperation, log_warn

current_directory = Path(__file__).parent

with open(current_directory.joinpath("generic_en.json"), "r") as explanation_file:
    il_explanations = json.load(explanation_file)

with open(current_directory.joinpath("native", "x86_en.json"), "r") as explanation_file:
    x86_explanations = json.load(explanation_file)


def find_missing():
    _missing = set()
    for op in LowLevelILOperation:
        if op.name not in il_explanations and not op.name.endswith("_SSA"):
            _missing.add(op.name)
    if _missing:
        log_warn(
            "Missing explanations for the following LLIL operations:\n"
            + "\n".join(_missing)
        )
