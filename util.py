def get_function_at(bv, addr):
    """ Gets the function that contains a given address, even if that address
    isn't the start of the function """
    blocks = bv.get_basic_blocks_at(addr)
    return blocks[0].function if (blocks is not None and len(blocks) > 0) else None

def find_mlil(func, addr):
    return find_in_IL(func.medium_level_il, addr)

def find_llil(func, addr):
    return find_in_IL(func.low_level_il, addr)

def find_lifted_il(func, addr):
    return find_in_IL(func.lifted_il, addr)

def find_in_IL(il, addr):
    """ Finds everything at the given address within the IL function passed in """
    out = []
    for block in il:
        for instruction in block:
            if instruction.address == addr:
                out.append(instruction)
    return out

def inst_in_func(func, addr):
    """ Finds an assembly function at the address given """
    return func.view.get_disassembly(addr)

def dereference_symbols(bv, il_instruction):
    """ If the instruction contains anything that looks vaguely like a hex
    number, see if there's a function there, and if so, replace it with the
    function symbol."""
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

def parse_instruction(context, instr):
    if instr is not None:
        docs = context.get_doc_url(instr.split(' '))
        instruction = context.escape(instr.replace('    ', ' '))
        shortForm = context.newline.join("<a href=\"{href}\">{form}</a>".format(href=url, form=context.escape(short_form)) for short_form, url in docs)
        return instruction, shortForm
    else:
        return 'None', 'None'

def parse_description(context, desc_list):
    return context.newline.join(context.escape(new_description) for new_description in desc_list)

def parse_llil(context, llil_list):
    newText = ""
    for llil in llil_list:
        if llil is not None:
            tokens = llil.deref_tokens if hasattr(llil, 'deref_tokens') else llil.tokens
            newText += "{}: ".format(llil.instr_index)
            newText += ''.join(context.escape(str(token)) for token in tokens)
        else:
            newText += 'None'
        newText += context.newline
    if(len(llil_list) > 0):
        return newText.strip(context.newline)
    else:
        return 'None'

def parse_mlil(context, mlil_list):
    newText = ""
    for mlil in mlil_list:
        if mlil is not None:
            tokens = mlil.deref_tokens if hasattr(mlil, 'deref_tokens') else mlil.tokens
            newText += "{}: ".format(mlil.instr_index)
            newText += (''.join(context.escape(str(token)) for token in tokens))
        else:
            newText += ('None')
        newText += context.newline
    if(len(mlil_list) > 0):
        return newText.strip(context.newline)
    else:
        return 'None'

def parse_state(context, state_list):
    if state_list is not None:
        return context.newline.join(context.escape(state) for state in state_list)
    else:
        return 'None'

def rec_replace(in_str, old, new):
    if old == new:
        return in_str
    if old not in in_str:
        return in_str
    return rec_replace(in_str.replace(old, new), old, new)

def parse_flags(context, tuple_list_list):
    out = ""
    for f_read, f_written, lifted in tuple_list_list:
        if len(f_read) > 0:
            out += ("(Lifted IL: {}) ".format(lifted.instr_index) if len(tuple_list_list) > 1 else "") + "Reads: " + ', '.join(f_read) + context.newline
        if len(f_written) > 0:
            out += ("(Lifted IL: {}) ".format(lifted.instr_index) if len(tuple_list_list) > 1 else "") + "Writes: " + ', '.join(f_written) + context.newline
        out += context.newline
    out = rec_replace(out.strip(context.newline), context.newline*2, context.newline)
    out = "None" if len(out) == 0 else out
    return out
