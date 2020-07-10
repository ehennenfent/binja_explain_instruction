#!/usr/bin/env python
# Copyright 2017 Ryan Stortz (@withzombies)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ==== CHANGES ====
# Altered return value for get_state so it's useful outside of this module
# Removed plugin registration
# Altered imports

from binaryninja import MediumLevelILOperation, RegisterValueType


def IsRegisterValueInteresting(reg):
    return (
        reg.type == RegisterValueType.ConstantValue
        or reg.type == RegisterValueType.StackFrameOffset
        or reg.type == RegisterValueType.ReturnAddressValue
    )


def FindMLILCallForAddress(func, addr):
    mlil = func.medium_level_il.ssa_form
    for block in mlil:
        for m in block:
            if (
                m.address == addr
                and m.operation == MediumLevelILOperation.MLIL_CALL_SSA
            ):
                return m

    return None


def get_state(bv, addr):
    blocks = bv.get_basic_blocks_at(addr)
    func = blocks[0].function

    regs = bv.arch.regs
    sp = bv.arch.stack_pointer

    output = []
    for reg in regs:
        out = func.get_reg_value_at(addr, reg)
        if IsRegisterValueInteresting(out):
            output.append("{} = {}".format(reg, out))

    sp_max = func.get_reg_value_at(addr, sp).offset
    # TODO: What happens when sp_max is None?
    for i in range(sp_max, 1):
        out = func.get_stack_contents_at(addr, i, 1)
        if IsRegisterValueInteresting(out):
            output.append("[SP{:#x}] = {}".format(i, out))

    # Label parameters for calls
    il = FindMLILCallForAddress(func, addr)
    if il is not None:
        dest = il.dest
        function_type = None
        params = len(il.params)

        if isinstance(dest, MediumLevelILOperation):
            called_function = bv.get_function_at(dest.constant)
            function_type = called_function.function_type

        for i in range(params):
            out = func.get_parameter_at(addr, function_type, i)
            output.append("arg{} = {}".format(i, out))

    return output
