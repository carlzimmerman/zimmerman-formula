#!/usr/bin/env python3
"""Exact identities plus bounded checks of the existing isolated-law functions.

No production solver is imported or evolved. Run with --out RESULT.json;
the computation contract supplies the finite range and provenance.
"""
import argparse
import ast
import json
import math
from pathlib import Path
import resource
import sys

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
x, b, e, z = s.symbols('x b e z', positive=True)
y = x**2/(1+x)
mu_s = x/(1+x)
mu_b = (s.sqrt(1+4*x*x)-1)/(2*x)
checks = {}

def zero(name, expression):
    residual = s.simplify(expression)
    checks[name] = bool(residual == 0)
    assert checks[name], (name, str(residual))

def pure_functions(path, names):
    tree = ast.parse(path.read_text())
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in selected} == set(names)
    ns = {'np': np}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), 'exec'), ns)
    return ns

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    fs = x*x-2*x+2*s.log(1+x)
    fb = x*s.sqrt(1+4*x*x)/2+s.asinh(2*x)/4-x
    zero('S_action_derivative', s.diff(fs,x)/(2*x)-mu_s)
    zero('B_action_derivative', s.diff(fb,x)/(2*x)-mu_b)
    zero('S_J_derivative', 1+s.diff(fs-x*x,x)/(2*x)-mu_s)
    zero('B_J_derivative', 1+s.diff(fb-x*x,x)/(2*x)-mu_b)
    zero('S_identity', x*x-y*(x+1))
    zero('S_minus_B_identity_residual', x*x-y*y-y-x**3/(1+x)**2)
    zero('S_excess', x-y-x/(1+x))
    zero('S_squared_excess_ratio', (x*x-y*y)/y-(1+2*x)/(1+x))
    zero('ratio_square', x*x/(y*y+y)-(1+x)**2/(x*x+x+1))
    zero('ratio_bound_certificate', 4*(x*x+x+1)-3*(1+x)**2-(x-1)**2)
    slope = s.simplify(1/(s.diff(y,x)*x/y))
    curvature = s.simplify(s.diff(slope,x)*y/s.diff(y,x))
    zero('S_log_slope', slope-(x+1)/(x+2))
    zero('S_log_curvature', curvature-x*(x+1)/(x+2)**3)
    zero('S_curvature_derivative_sign', s.diff(curvature,x)-(-x*x+2*x+2)/(x+2)**4)
    zero('S_curvature_peak_y', y.subs(x,1+s.sqrt(3))-2)
    zero('S_curvature_peak_value', curvature.subs(x,1+s.sqrt(3))-1/(6*s.sqrt(3)))
    zero('S_EFE_quadratic', (1+x+e)*(x*(x+e)/(1+x+e)-b)-(x*x+(e-b)*x-b*(1+e)))
    zero('S_EFE_discriminant', (e-b)**2+4*b*(1+e)-((e+b)**2+4*b))
    zero('S_EFE_susceptibility_at_zero', -(x-y)/(2*x-y)+1/(x+2))
    zero('B_EFE_squaring_identity', x*x*(1+4*(x+e)**2)-(2*b*(x+e)+x)**2-4*(x+e)*((x*x-b*b)*(x+e)-b*x))
    zero('B_curvature_peak_certificate', s.Rational(1,8)-z/(2*(z+1)**2)-(z-1)**2/(8*(z+1)**2))
    # Exact regression witness: a0=g=1, gN=1/2 satisfies S but violates B.
    assert y.subs(x,1) == s.Rational(1,2)
    assert (x*x-y*y-y).subs(x,1) == s.Rational(1,4)
    checks['false_identity_detected_exactly'] = True
    p4 = pure_functions(ROOT/'rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_solver.py', ['nu1','g_from_gN'])
    cl3 = pure_functions(ROOT/'rebuild_2026_10_22/CL3_one_number/cl3_one_number.py', ['nu'])
    grid = np.logspace(-10,10,2001)
    gx = p4['g_from_gN'](grid)
    formula = (grid+np.sqrt(grid*grid+4*grid))/2
    discrepancies = {
        'P4_inverse_vs_S': float(np.max(abs(gx/formula-1))),
        'P4_nu_vs_S': float(np.max(abs(p4['nu1'](grid)*grid/formula-1))),
        'CL3_nu_vs_S': float(np.max(abs(cl3['nu'](grid)*grid/formula-1))),
    }
    assert all(v < 3e-15 for v in discrepancies.values())
    checks['actual_P4_CL3_functions_match_S_on_2001_points'] = True
    # Scalar S EFE, including e=0; b=0 has only a nonnegative zero root.
    efe_count = 0
    for bb in [1e-6, 0.01, 0.5, 1., 100.]:
        for ee in [0., 0.01, 0.5, 1., 100.]:
            root = 2*bb*(1+ee)/(math.sqrt((ee+bb)**2+4*bb)+ee-bb)
            assert root > 0
            assert abs(root*(root+ee)/(1+root+ee)/bb-1) < 3e-14
            efe_count += 1
    checks['S_scalar_EFE_25_cases'] = True
    zero_b_roots = [max(0., -ee) for ee in [0., 0.01, 1., 100.]]
    assert zero_b_roots == [0.]*4
    checks['zero_b_has_no_positive_S_root'] = True
    result = {
        'assertion_tested': '20 symbolic identities; exact S/B counterexample; 2001-point existing P4/CL3 function comparison; 25 positive-b and four zero-b scalar S EFE cases',
        'checks': checks, 'all_checks_pass': all(checks.values()),
        'existing_function_discrepancies': discrepancies,
        'finite_grid': {'y_min':1e-10,'y_max':1e10,'count':2001},
        'scalar_EFE_positive_b_cases': efe_count,
        'S_at_y_one': (1+math.sqrt(5))/2,
        'B_at_y_one': math.sqrt(2),
        'maximum_S_over_B': 2/math.sqrt(3),
        'maximum_relative_difference': 2/math.sqrt(3)-1,
        'maximum_dex_difference': math.log10(2/math.sqrt(3)),
        'S_curvature_peak': {'y':2., 'x':1+math.sqrt(3), 'value':1/(6*math.sqrt(3))},
        'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'software': {'python':sys.version,'sympy':s.__version__,'numpy':np.__version__},
        'non_claims': ['No empirical refit, PDE EFE solution, production simulation, or full covariant health theorem', 'Finite checks do not prove a universal identity; the written algebra and adapter provide their stated universal implications', 'The B-law certificates retain their original hypotheses']}
    assert result['peak_RSS_bytes'] < 1073741824
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':len(checks),'all_checks_pass':all(checks.values()),'maximum_relative_difference':result['maximum_relative_difference']}))

if __name__ == '__main__':
    main()
