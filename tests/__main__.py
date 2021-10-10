import argparse
from pathlib import Path
from random import random
from typing import Dict, Set

from binaryninja import BinaryView, BinaryViewType

from .instruction_data import InstructionData, get_instruction_data
from ..explanations import find_missing

find_missing()

SPACER = ""


def sample_instructions(bv: BinaryView) -> Dict[str, Set[InstructionData]]:
    sampled = {}
    for inst, addr in bv.instructions:
        mnemonic = str(inst[0])
        if mnemonic not in sampled or random() < (1 / (len(sampled[mnemonic]) + 1)):
            sampled.setdefault(mnemonic, set()).add(
                get_instruction_data(bv, addr, instruction=inst)
            )

    return sampled


def sample_bv(bv: BinaryView):
    sampled = sample_instructions(bv)
    for k in sorted(sampled.keys()):
        print(SPACER, k, "-")
        for v in sampled[k]:
            print(SPACER, SPACER, v)


def sample_path(path: Path):
    path = str(path)
    print(f"{path}::")
    bv = BinaryViewType.get_view_of_file(path)
    bv.update_analysis_and_wait()
    sample_bv(bv)


def main():
    parser = argparse.ArgumentParser(
        "Sample random instructions from some binaries and print the result"
    )
    parser.add_argument("files", nargs="+")

    args = parser.parse_args()

    files = []

    for file in args.files:
        path = Path(file)
        assert path.exists(), f"No such file: {file}"
        files.append((path, path.stat().st_size))

    for path, _size in sorted(files, key=lambda p: p[1]):
        sample_path(path)
