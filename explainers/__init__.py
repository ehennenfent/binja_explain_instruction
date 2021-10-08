# Import as lowercase here so we can use string formatting to import them later
from binaryninja import Architecture

from .x86 import X86Explainer
from .mips import MipsExplainer
from .aarch64 import AArch64Explainer
from .ual import UALExplainer
from .asm6502 import Asm6502Explainer
from .msp430 import MSP430Explainer
from .powerpc import PowerPCExplainer

from .generic import UnavailableExplainer


def explainer_for_architecture(arch: Architecture):
    return {
        "x86": X86Explainer,
        "x86_64": X86Explainer,
        "mips": MipsExplainer,
        "aarch64": AArch64Explainer,
        "arm": UALExplainer,
        "thumb2": UALExplainer,
        "6502": Asm6502Explainer,
        "msp430": MSP430Explainer,
        "powerpc": PowerPCExplainer,
    }.get(arch.name, UnavailableExplainer)
