from PyQt5.QtWidgets import QApplication, QMainWindow
from binaryninja import *

from gui import ExplanationWindow
from instruction_state import get_state
from explain import explain_llil

app = QApplication.instance()
main_window = [x for x in app.allWidgets() if x.__class__ is QMainWindow][0]

from x86 import get_doc_url

def init_gui():
    if not hasattr(main_window, 'explain_window'):
        main_window.explain_window = ExplanationWindow()
        main_window.explain_window.get_doc_url = get_doc_url
    main_window.explain_window.show()

def get_function_at(bv, addr):
    blocks = bv.get_basic_blocks_at(addr)
    return blocks[0].function if blocks is not None else None

def find_in_IL(il, addr):
    out = []
    for block in il:
        for i in block:
            if i.address == addr:
                out.append(i)
    return out

def inst_in_func(func, addr):
    out = None
    for block in func:
        for i in block.disassembly_text:
            if i.address == addr:
                out = i
    return out

def dereference_symbols(bv, il_instruction):
    if il_instruction is not None:
        out = []
        for item in il_instruction.tokens:
            try:
                addr = int(str(item), 16)
                func = bv.get_function_at(addr)
                if func is not None:
                    out.append(func.name)
                    continue
            except ValueError:
                pass
            out.append(item)
        il_instruction.deref_tokens = out
    return il_instruction

def explain_instruction(bv, addr):
    init_gui()

    func = get_function_at(bv, addr)
    llil_list = find_in_IL(func.lifted_il.non_ssa_form, addr)

    main_window.explain_window.instruction = inst_in_func(func, addr)
    main_window.explain_window.description = [explain_llil(bv, llil) for llil in llil_list]
    main_window.explain_window.llil = [dereference_symbols(bv, llil) for llil in find_in_IL(func.low_level_il.non_ssa_form, addr)]
    main_window.explain_window.mlil = [dereference_symbols(bv, mlil) for mlil in find_in_IL(func.medium_level_il.non_ssa_form, addr)]
    main_window.explain_window.state = get_state(bv, addr)

PluginCommand.register_for_address("Explain Instruction", "", explain_instruction)
