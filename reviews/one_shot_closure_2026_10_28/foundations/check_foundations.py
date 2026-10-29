#!/usr/bin/env python3
"""Bounded symbolic checks for the foundations review; no simulation imported.

Run from repository root:
python3 reviews/one_shot_closure_2026_10_28/foundations/check_foundations.py
The handwritten proofs in FOUNDATIONS_REVIEW.md supply the universal arguments.
"""
import ast
import json
import math
import pathlib
import sys

import numpy as np
import sympy as s

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'run_001' / 'result.json'
x, e, b, k, alpha, a, L = s.symbols('x e b k alpha a L', positive=True)
y = x*x/(1+x)
mu_s = x/(1+x)
mu_b = (s.sqrt(1+4*x*x)-1)/(2*x)
f_s = x*x-2*x+2*s.log(1+x)
f_b = x*s.sqrt(1+4*x*x)/2+s.asinh(2*x)/4-x

checks = {}
def zero(name, expr):
    val = s.simplify(expr)
    checks[name] = bool(val == 0)
    assert checks[name], (name, val)

zero('F_simple_derivative', s.diff(f_s,x)/(2*x)-mu_s)
zero('F_line_derivative', s.diff(f_b,x)/(2*x)-mu_b)
zero('J_simple_derivative', 1+s.diff(f_s-x*x,x)/(2*x)-mu_s)
zero('J_line_derivative', 1+s.diff(f_b-x*x,x)/(2*x)-mu_b)
zero('simple_spherical_identity', x*x-y*(x+1))
zero('simple_not_exact_line_residual', (x*x-y*y-y)-x**3/(1+x)**2)
zero('simple_to_line_ratio', x*x/(y*y+y)-(1+x)**2/(x*x+x+1))
zero('ratio_max_square_certificate', 4*(x*x+x+1)-3*(1+x)**2-(x-1)**2)
zero('simple_aligned_efe_quadratic', (1+x+e)*(x*(x+e)/(1+x+e)-b)-(x*x+(e-b)*x-b*(1+e)))
zero('simple_newton_excess', (x-y)-x/(1+x))
zero('simple_excess_ratio', (x*x-y*y)/y-(1+2*x)/(1+x))
zero('four_form_modulus', 2/(2/k**2-2*b+2*b)-k**2)
zero('crossover_scaling', s.diff(s.log((a/L**s.Rational(5,4))**(1/alpha)), L)*L+s.Rational(5,4)/alpha)

# Extract only pure law functions from actual solver source, not its engine.
source_path = ROOT/'rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_solver.py'
tree = ast.parse(source_path.read_text())
selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ('nu1', 'g_from_gN')]
assert len(selected) == 2
ns = {'np': np}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(source_path), 'exec'), ns)
grid = np.logspace(-10,10,2001)
actual = ns['nu1'](grid)*grid
inverse = ns['g_from_gN'](grid)
relative = float(np.max(np.abs(actual/inverse-1)))
checks['solver_two_functions_agree_2001_points'] = relative < 2e-15
assert checks['solver_two_functions_agree_2001_points']

anchor_simple = float(ns['g_from_gN'](1.0))
anchor_line = math.sqrt(2)
assert abs(anchor_simple-(1+math.sqrt(5))/2)<1e-15
max_ratio = 2/math.sqrt(3)
eta = 4/(3*(3*math.log(2)-math.pi/2))*4**1.25
result = {
 'assertion_tested': '13 exact symbolic identities and agreement of two isolated P4 law functions on 2001 points; no cosmology or halo production run',
 'checks': checks,
 'all_checks_pass': all(checks.values()),
 'solver_sample_range_gN_over_a0': [1e-10,1e10],
 'solver_relative_disagreement': relative,
 'simple_g_over_a0_at_gN_a0': anchor_simple,
 'line_g_over_a0_at_gN_a0': anchor_line,
 'anchor_ratio': anchor_simple/anchor_line,
 'anchor_log10_difference': math.log10(anchor_simple/anchor_line),
 'exact_global_max_ratio': '2/sqrt(3), attained when g_simple/a0=1 and gN/a0=1/2',
 'global_max_ratio_numeric': max_ratio,
 'global_max_dex_numeric': math.log10(max_ratio),
 'eta_at_cf4': eta,
 'crossover_log_sensitivity_at_alpha_0_23': -1.25/0.23,
 'software': {'python': sys.version, 'sympy': s.__version__, 'numpy': np.__version__},
 'non_claims': ['No original numerical fit rerun', 'No physical viability or complete covariant theory established', 'No current Lean compiler rerun', 'The symbolic library is checked evidence; handwritten algebra is the proof']
}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
