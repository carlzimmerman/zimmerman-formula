#!/usr/bin/env python3
"""Two-kernel audit of the EXISTING frozen C-H/K block; no full-theory claim."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import sympy as s
from scipy.optimize import brentq

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
checks = {}

def exact(name, residual):
    residual = s.factor(s.simplify(residual))
    checks[name] = {'passed': residual == 0, 'residual': str(residual)}
    assert residual == 0, (name, residual)

z, x = s.symbols('z x', positive=True)
A, B, C, k = s.symbols('A B C k', real=True)
psi, phi, u, beta, dp = s.symbols('psi phi u beta dp', real=True)
h_rar = z**2/(s.exp(z)-1)
c_rar = (s.exp(z)*(1-z/2)-1)/(s.exp(z)-1)**2
c_exp = (1-x)/(s.exp(x)+x-1)
exact('RAR_phantom_derivative', s.diff(h_rar,z)/(2*z)-c_rar)
exact('EXP_phantom_derivative', s.diff(x*s.exp(-x),x)/s.diff(x*(1-s.exp(-x)),x)-c_exp)
# Derive from the displayed real-time block, not from stored output formulas.
L = (-6*dp**2+4*k**2*beta*dp+2*k**2*psi**2-4*k**2*phi*psi
     +2*k**2*(u-phi)**2+2*k**2*C*u**2-B*(3*dp-k**2*beta)**2+A*k**2*phi**2)
aux = s.solve([s.diff(L,q) for q in [phi,u,beta]], [phi,u,beta], dict=True)[0]
D, N = A+(A+2)*C, 2-A*(1+C)
exact('reduced_action', L.subs(aux)-(2*(2+3*B)/B*dp**2-2*k**2*N/D*psi**2))
exact('negative_C_alpha_boundary', D.subs(A,-2*C/(1+C)))
exact('numerator_at_D_zero', N.subs(C,-A/(A+2))-4/(A+2))
exact('EXP_alpha_bound', -2*c_exp/(1+c_exp)-2*(x-1)*s.exp(-x))
exact('EXP_bound_derivative', s.diff(2*(x-1)*s.exp(-x),x)-2*(2-x)*s.exp(-x))
# This reproduces an existing EXP result; the RAR witness is the extension.
ar = -2*c_rar/(1+c_rar)
ar3 = float(ar.subs(z,3).evalf(40))
ce2 = float(c_exp.subs(x,2).evalf(40))
cr3 = float(c_rar.subs(z,3).evalf(40))
assert cr3 < 0 and ce2 < 0
alpha_cap = 3.2e-9  # L340 stated ceiling, not a freshly rederived empirical limit.
samples = []
for name, c0, witness in [('RAR',cr3,'gN/a0=9'),('EXP',ce2,'g/a0=2')]:
    crit = math.sqrt(math.log(-(alpha_cap+2)*c0/alpha_cap))
    vals = []
    for q in [0.1,1.0,crit-0.1,crit+0.1]:
        ck = c0*math.exp(-q*q)
        speed2 = 0.01*(2-alpha_cap*(1+ck))/((2+0.03)*(alpha_cap+(alpha_cap+2)*ck))
        vals.append({'k_xi':q,'C_filtered':ck,'speed_squared_over_c2':speed2})
    assert vals[0]['speed_squared_over_c2'] < 0
    assert vals[-1]['speed_squared_over_c2'] > 0
    samples.append({'kernel':name,'witness':witness,'C_L':c0,'alpha_needed_at_kxi_zero':-2*c0/(1+c0),
                    'critical_k_xi_at_alpha_cap':crit,'frozen_values':vals})
checks['filter_does_not_remove_negative_low_k_branch'] = {'passed':True,'rows':samples}

# Compare physical spherical responses at identical gN/a0, using explicit variables.
rows = []
for t in [0.01,0.1,1.0,9.0,100.0]:
    xr = t/(-math.expm1(-math.sqrt(t)))
    xe = brentq(lambda q:q*(-math.expm1(-q))-t,1e-12,t+math.sqrt(t)+2,xtol=1e-13)
    rows.append({'gN_over_a0':t,'RAR_g_over_a0':xr,'EXP_g_over_a0':xe,
                 'RAR_over_EXP_dex':math.log10(xr/xe)})
assert abs(rows[2]['RAR_over_EXP_dex']) > 0.05
checks['same_argument_kernels_are_distinct'] = {'passed':True,'rows':rows}

# Static-block Newton normalization and zero-field issue of constant alpha.
gain = (1+C)/(1-A*(1+C)/2)
gn_gain = 1/(1-A/2)
exact('measured_G_normalized_gain',gain/gn_gain-(1+C)*(1-A/2)/(1-A*(1+C)/2))
exact('static_transverse_pole', N.subs(C,2/A-1))
smallx = -math.log1p(-alpha_cap/2)
zero_rows = {'alpha':alpha_cap, 'RAR_gN_over_a0_pole':smallx**2,
             'EXP_gN_over_a0_pole':smallx*alpha_cap/2,
             'interpretation':'Frozen unsuppressed transverse block only; extrapolation outside L340 tested acceleration range.'}
checks['zero_field_not_covered_by_constant_alpha_block'] = {'passed':True,'rows':zero_rows}

result = {'verdict':'Existing frozen C-H/K completion does not preserve healthy exact RAR or EXP branches in its stated small-alpha window.',
          'checks':checks,'RAR_exact_witness_alpha':str(ar.subs(z,3)),
          'RAR_witness_alpha_numeric':ar3,'EXP_all_negative_branch_alpha_threshold':2/math.e**2,
          'inherited_work':'EXP threshold and scalar reduction already in closure_resume_2026_09_26; checked as controls, not claimed new.',
          'new_scope':'Explicit RAR witness, parallel branch provenance, finite-k filter crossing and separate zero-field warning.',
          'non_claims':['No universal no-go for either kernel or another action',
                        'No full action-to-frozen-block derivation or nonlinear health certificate',
                        'Large-alpha repair not accepted as preserving static law, measured G or PPN',
                        'No empirical re-fit; alpha ceiling is a conditional input from L340',
                        'No transfer between spherical inversion and nonspherical AQUAL/QUMOND PDEs']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(checks),'RAR_alpha_witness':ar3,
                  'EXP_alpha_threshold':2/math.e**2,'pole_rows':zero_rows,'filter_rows':samples},indent=2))
