import sys
if (sys.platform == 'win32'):
    sys.path.append("C:\\Python27\\lib\\site-packages")

from PyQt5.QtWidgets import QApplication, QMainWindow, qApp
from PyQt5.QtCore import QCoreApplication
from binaryninja import LowLevelILOperation, PluginCommand

from gui import ExplanationWindow
from instruction_state import get_state
from explain import explain_llil
from util import get_function_at, find_mlil, find_llil, find_lifted_il, inst_in_func, dereference_symbols

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
architecture_specific_explanation_function = lambda _ : False, "Not Available"

# See comment beginning on line 48
use_low_level_instead_of_lifted = [LowLevelILOperation.LLIL_IF]

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
        elif 'your_architecture_here' in bv.arch.name: # Placeholder for additional arcitectures
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

    # Typically, we use the Lifted IL for explaining instructions, which is a form of Low-Level IL that is somewhat simpler
    # than what's displayed in the Low-Level IL view, and has a closer mapping to individual assembly instructions. However,
    # Lifted IL doesn't fold conditionals into conditional jumps, so in cases like that, for clarity's sake we use the
    # Low-Level IL from the low_level_il attribute instead.
    contains_dependent_instruction = True in [(llil.operation in use_low_level_instead_of_lifted) for llil in llil_list]

    # Give the architecture submodule a chance to supply an explanation for this instruction that takes precedence
    # over the one generated via the LLIL
    should_supersede_llil, explanation = architecture_specific_explanation_function(bv, instruction, lifted_il_list)

    # Display the raw instruction
    main_window.explain_window.instruction = instruction

    if explanation is not None:
        if should_supersede_llil:
            # If we got an architecture-specific explanation and it should supersede the LLIL, use that
            main_window.explain_window.description = [explanation]
        else:
            # Otherwise, just prepend the arch-specific explanation to the LLIL explanation
            main_window.explain_window.description = [explanation] + [explain_llil(bv, llil) for llil in (llil_list if contains_dependent_instruction else lifted_il_list)]
    else:
        # By default, we just use the LLIL explanation
        main_window.explain_window.description = [explain_llil(bv, llil) for llil in (llil_list if contains_dependent_instruction else lifted_il_list)]

    # Display the MLIL and LLIL, dereferencing anything that looks like a hex number into a symbol if possible
    main_window.explain_window.llil = [dereference_symbols(bv, llil) for llil in llil_list]
    main_window.explain_window.mlil = [dereference_symbols(bv, mlil) for mlil in mlil_list]

    # Display what information we can calculate about the program state before the instruction is executed
    main_window.explain_window.state = get_state(bv, addr)

PluginCommand.register_for_address("Explain Instruction", "", explain_instruction)
