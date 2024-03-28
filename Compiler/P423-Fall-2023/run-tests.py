import os
import sys

sys.path.append('../P423-Fall-2023')
sys.path.append('../P423-Fall-2023/interp_x86')

import compiler
import interp_Lwhile
import interp_Cif
import interp_Ltup
import interp_Ctup
import type_check_Cwhile
import type_check_Lwhile
import type_check_Ctup
import type_check_Ltup
from utils import run_tests, run_one_test, enable_tracing
from interp_x86.eval_x86 import interp_x86

enable_tracing()

compiler = compiler.Compiler()

typecheck_Lwhile = type_check_Lwhile.TypeCheckLwhile().type_check
typecheck_Cwhile = type_check_Cwhile.TypeCheckCwhile().type_check
typecheck_Ltup = type_check_Ltup.TypeCheckLtup().type_check
typecheck_Ctup = type_check_Ctup.TypeCheckCtup().type_check

typecheck_dict = {
    'source': typecheck_Ltup,
    'expose_allocation': typecheck_Ltup,
    'remove_complex_operands': typecheck_Ltup,
    'explicate_control': typecheck_Ctup
}
interpLwhile = interp_Lwhile.InterpLwhile().interp
interpCif = interp_Cif.InterpCif().interp
interpLtup = interp_Ltup.InterpLtup().interp
interpCtup = interp_Ctup.InterpCtup().interp
interp_dict = {
    'expose_allocation': interpLtup,
    'remove_complex_operands': interpLtup,
    'explicate_control': interpCtup,
    # 'select_instructions': interp_x86,
    # 'assign_homes': interp_x86,
    # 'patch_instructions': interp_x86,
}

if True:
    run_one_test(os.getcwd() + '/tests/var/program.py',
                 'var',
                 compiler,
                 'var',
                 typecheck_dict,
                 interp_dict)
else:
    run_tests('var', compiler, 'var',
              typecheck_dict,
              interp_dict)

