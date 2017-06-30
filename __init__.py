from PyQt5.QtWidgets import QApplication, QMainWindow
from binaryninja import *

from gui import ExplanationWindow
from instruction_state import get_state
from explain import explain_llil
from util import get_function_at, find_in_IL, inst_in_func, dereference_symbols

app = QApplication.instance()
main_window = [x for x in app.allWidgets() if x.__class__ is QMainWindow][0]

arch = None
architecture_specific_explanation_function = lambda _ : False, "Not Available"

def init_plugin(bv):
    global arch, architecture_specific_explanation_function
    if not hasattr(main_window, 'explain_window'):
        main_window.explain_window = ExplanationWindow()
    if bv.arch.name != arch:
        if 'x86' in bv.arch.name:
            import x86, x86.explain
            main_window.explain_window.get_doc_url = x86.get_doc_url
            architecture_specific_explanation_function = x86.explain.arch_explain_instruction
        arch = bv.arch.name
    main_window.explain_window.show()

def explain_instruction(bv, addr):
    init_plugin(bv)

    func = get_function_at(bv, addr)
    instruction = inst_in_func(func, addr)
    lifted_il_list = find_in_IL(func.lifted_il.non_ssa_form, addr)

    should_supersede_llil, explanation = architecture_specific_explanation_function(bv, instruction, lifted_il_list)

    main_window.explain_window.instruction = instruction
    if explanation is not None:
        if should_supersede_llil:
            main_window.explain_window.description = [explanation]
        else:
            main_window.explain_window.description = [explanation] + [explain_llil(bv, llil) for llil in lifted_il_list]
    else:
        main_window.explain_window.description = [explain_llil(bv, llil) for llil in lifted_il_list]
    main_window.explain_window.llil = [dereference_symbols(bv, llil) for llil in find_in_IL(func.low_level_il.non_ssa_form, addr)]
    main_window.explain_window.mlil = [dereference_symbols(bv, mlil) for mlil in find_in_IL(func.medium_level_il.non_ssa_form, addr)]
    main_window.explain_window.state = get_state(bv, addr)

PluginCommand.register_for_address("Explain Instruction", "", explain_instruction)
