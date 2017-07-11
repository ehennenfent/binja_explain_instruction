import sys
if (sys.platform == 'win32'):
    sys.path.append("C:\\Python27\\lib\\site-packages")

from PyQt5.QtWidgets import QApplication, QMainWindow, qApp
from PyQt5.QtCore import QCoreApplication
from binaryninja import LowLevelILOperation, PluginCommand

from gui import ExplanationWindow
from instruction_state import get_state
from explain import explain_llil, fold_multi_il
from util import get_function_at, find_mlil, find_llil, find_lifted_il, inst_in_func, dereference_symbols

import traceback

app = QApplication.instance()
if app is None:
    app = QCoreApplication.instance()
if app is None:
    app = qApp
try:
    main_window = [x for x in app.allWidgets() if x.__class__ is QMainWindow][0]
except IndexError:
    raise Exception("Could not attach to main window!")

arch = None
architecture_specific_explanation_function = lambda *_: (False, ["Architecture-specific explanations unavailable"])

def init_plugin(bv):
    """ Creates the plugin window and sets up the architecture-specfic functions """
    global arch, architecture_specific_explanation_function

    # Creates a new window if it doesn't already exist
    if not hasattr(main_window, 'explain_window'):
        main_window.explain_window = ExplanationWindow()

    # Sets up architecture-specific functions
    if bv.arch.name != arch:
        if 'x86' in bv.arch.name:
            import x86, x86.explain
            main_window.explain_window.get_doc_url = x86.get_doc_url
            architecture_specific_explanation_function = x86.explain.arch_explain_instruction
        elif 'your_architecture_here' in bv.arch.name: # Placeholder for additional architectures
            pass
        arch = bv.arch.name
    main_window.explain_window.show()

def explain_instruction(bv, addr):
    """ Callback for the menu item that passes the information to the GUI """
    init_plugin(bv)

    # Get the relevant information for this address
    func = get_function_at(bv, addr)
    instruction = inst_in_func(func, addr)
    lifted_il_list = find_lifted_il(func, addr)
    llil_list = find_llil(func, addr)
    mlil_list = find_mlil(func, addr)

    # Typically, we use the Low Level IL for parsing instructions. However, sometimes there isn't a corresponding
    # LLIL instruction (like for cmp), so in cases like that, we use the lifted IL, which is closer to the raw assembly
    parse_il = fold_multi_il(bv, llil_list if len(llil_list) > 0 else lifted_il_list)

    # Give the architecture submodule a chance to supply an explanation for this instruction that takes precedence
    # over the one generated via the LLIL
    should_supersede_llil, explanation_list = architecture_specific_explanation_function(bv, instruction, lifted_il_list)

    # Display the raw instruction
    try:
        main_window.explain_window.instruction = "{addr}:  {inst}".format(addr=hex(addr).replace("L", ""), inst=instruction)
    except Exception:
        traceback.print_exc()

    if len(explanation_list) > 0:
        if should_supersede_llil:
            # If we got an architecture-specific explanation and it should supersede the LLIL, use that
            main_window.explain_window.description = [explanation for explanation in explanation_list]
        else:
            # Otherwise, just prepend the arch-specific explanation to the LLIL explanation
            main_window.explain_window.description = [explanation for explanation in explanation_list] + [explain_llil(bv, llil) for llil in (parse_il)]
    else:
        # By default, we just use the LLIL explanation
        # We append the line number if we're displaying a conditional.
        main_window.explain_window.description = [explain_llil(bv, llil) for llil in parse_il]

    # Display the MLIL and LLIL, dereferencing anything that looks like a hex number into a symbol if possible
    main_window.explain_window.llil = [dereference_symbols(bv, llil) for llil in llil_list]
    main_window.explain_window.mlil = [dereference_symbols(bv, mlil) for mlil in mlil_list]

    # Display what information we can calculate about the program state before the instruction is executed
    main_window.explain_window.state = get_state(bv, addr)

PluginCommand.register_for_address("Explain Instruction", "", explain_instruction)
