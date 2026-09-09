"""Check the actual L49 kernel against the user's exact constitutive equation.

Extract only its two pure kernel functions and their saturation constants;
do not import/run its empirical pipeline or certify its cosmological claims.
"""
import ast
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq


def exponential_inverse(gN):
    if gN<0:raise ValueError('Nonnegative spherical acceleration magnitude required')
    if gN==0:return 0.
    return brentq(lambda y:y*(-math.expm1(-y))-gN,0.,gN+math.sqrt(gN)+1.,xtol=1e-14)


def audit():
    path=Path(__file__).resolve().parents[3]/'fable_independent_2026/L49_minimum_addition.py'
    tree=ast.parse(path.read_text());selected=[]
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name in ('Delta','g_kernel'):selected.append(node)
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Tuple):
            if [getattr(x,'id',None) for x in node.targets[0].elts]==['S_SAT','D_SAT']:selected.append(node)
    if len(selected)!=3:raise ValueError('L49 kernel interface changed; re-audit its source')
    namespace={'np':np}
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(path),'exec'),namespace)
    rows=[]
    for gN in (.001,.1,1.,10.,100.):
        y=exponential_inverse(gN);rival=float(namespace['g_kernel'](gN,1.))
        rows.append(dict(gN_over_a0=gN,exact_g_over_a0=y,L49_g_over_a0=rival,
                         exact_equation_residual=y*(-math.expm1(-y))-gN,
                         L49_equation_residual=rival*(-math.expm1(-rival))-gN))
    return dict(rows=rows,max_exact_equation_residual=max(abs(r['exact_equation_residual']) for r in rows),
                max_l49_equation_residual=max(abs(r['L49_equation_residual']) for r in rows),
                conclusion='L49 uses a different kernel; its empirical numbers are not results for IC29/30/39',
                full_theory='OPEN')


if __name__=='__main__':print(json.dumps(audit(),indent=2))
