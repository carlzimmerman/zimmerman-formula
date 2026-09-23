"""Independent control: ADM quadratic equations versus all 16 unitary entries
of the audited spacetime-covariant Minkowski matrix, on an on-shell vacuum.
"""
from pathlib import Path
import json,sympy as s
here=Path(__file__).resolve().parent; root=here.parents[3]
d=json.loads((here/'run_adm/equations.json').read_text())
E=[s.sympify(x) for x in d['ODE']]; S={k:s.sympify(x) for k,x in d['S'].items()}
amps=[s.sympify(x) for x in d['amps']];t=S['t']
ns='omega k Q_0 F_1 F_2 c_2 c14 K_B beta xi'
v=s.symbols(ns,real=True);loc=dict(zip(ns.split(),v));w,k,Q,F1,F2,c2,c14,KB,b,xi=v
bg={S['a']:s.Integer(1),S['Q']:Q,S['F0']:s.Integer(0),S['F1']:s.Integer(0),S['F2']:F2,
    S['c2']:c2,S['c14']:c14,S['KB']:KB,S['beta']:b,S['xi']:xi,S['Lam']:s.Integer(0),S['k']:k}
aa=s.symbols('A0:4');wave=s.exp(-s.I*w*t)
E=[s.expand(z.subs(bg).doit().subs(dict(zip(amps,[q*wave for q in aa]))).doit()/wave) for z in E]
M=s.Matrix(4,4,lambda i,j:s.factor(E[i].coeff(aa[j])))
old=json.loads((root/'real_research/clock_2026/L287_dirac_count_clock_lapse_results.json').read_text())
O=s.Matrix(5,5,lambda i,j:s.sympify(old['M_entries'][str(i)+str(j)],locals=loc))
bad=s.Matrix([[0,s.I*k*Q,-3*s.I*w*Q,0,-k*k]])
good=s.Matrix([[0,0,0,k*k*Q,-k*k]])
O=O+2*(2-KB)*xi**2*s.conjugate(bad.T)*bad-2*(2-KB)*xi**2*s.conjugate(good.T)*good
O=O.subs(F1,0).extract([0,1,2,4],[0,1,2,4])
change=s.diag(1,s.I*k,1,1)
target=s.conjugate(change.T)*O*change
res=[s.simplify(z) for z in M-target]
assert all(z==0 for z in res),res
print('PASS: all 16 ADM Fourier entries equal corrected covariant unitary-clock entries on Minkowski vacuum.')
