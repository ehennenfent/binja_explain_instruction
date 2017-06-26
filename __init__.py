from PyQt5.QtWidgets import QApplication, QMainWindow
from binaryninja import *

from gui import ExplanationWindow
from instruction_state import get_state
from explain import explain_llil

app = QApplication.instance()
main_window = [x for x in app.allWidgets() if x.__class__ is QMainWindow][0]

def init_gui():
    if not hasattr(main_window, 'explain_window'):
        main_window.explain_window = ExplanationWindow()
    main_window.explain_window.show()

def get_function_at(bv, addr):
    blocks = bv.get_basic_blocks_at(addr)
    return blocks[0].function if blocks is not None else None

def find_in_IL(il, addr):
    for block in il:
        for i in block:
            if i.address == addr:
                return i
    return None

def inst_in_func(func, addr):
    for block in func:
        for i in block.disassembly_text:
            if i.address == addr:
                return i
    return None

def explain_instruction(bv, addr):
    init_gui()

    func = get_function_at(bv, addr)
    llil = find_in_IL(func.low_level_il.non_ssa_form, addr)

    main_window.explain_window.instruction = inst_in_func(func, addr)
    main_window.explain_window.description = explain_llil(bv, llil)
    main_window.explain_window.llil = llil
    main_window.explain_window.mlil = find_in_IL(func.medium_level_il.non_ssa_form, addr)
    main_window.explain_window.state = get_state(bv, addr)

PluginCommand.register_for_address("Explain Instruction", "", explain_instruction)
