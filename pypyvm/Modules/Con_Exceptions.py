# Copyright (c) 2011 King's College London, created by Laurence Tratt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.


import sys
import Builtins




def init(vm):
    mod = Builtins.new_c_con_module(vm, "Exceptions", "Exceptions", __file__, \
      ["Exception", "Mod_Defn_Exception", "System_Exit_Exception"])
    vm.set_builtin(Builtins.BUILTIN_EXCEPTIONS_MODULE, mod)
    init_func = Builtins.new_c_con_func(vm, Builtins.new_con_string(vm, "init"), False, import_, mod)
    mod.init_func = init_func
    
    return mod


def import_(vm):
    (mod,),_ = vm.decode_args("O")

    mod.set_defn(vm, "Exception", vm.get_builtin(Builtins.BUILTIN_EXCEPTION_CLASS))
    _mk_simple_exception(vm, mod, "Mod_Defn_Exception")
    _mk_simple_exception(vm, mod, "System_Exit_Exception", init_func=_System_Exit_Exception_init_func)

    vm.return_(vm.get_builtin(Builtins.BUILTIN_NULL_OBJ))


def _mk_simple_exception(vm, mod, n, init_func=None):
    class_class = vm.get_builtin(Builtins.BUILTIN_CLASS_CLASS)
    ex_class = vm.get_builtin(Builtins.BUILTIN_EXCEPTION_CLASS)
    assert isinstance(ex_class, Builtins.Con_Class)
    ex = vm.get_slot_apply(class_class, "new", \
      [Builtins.new_con_string(vm, n), Builtins.new_con_list(vm, [ex_class]), mod])
    if init_func is not None:
        ex.set_field(vm, "init", \
          Builtins.new_c_con_func(vm, Builtins.new_con_string(vm, "init"), True, init_func, ex))
    mod.set_defn(vm, n, ex)


def _System_Exit_Exception_init_func(vm):
    (self, code),_ = vm.decode_args("OO")
    self.set_slot(vm, "code", code)
    vm.return_(vm.get_builtin(Builtins.BUILTIN_NULL_OBJ))