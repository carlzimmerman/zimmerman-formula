#!/usr/bin/env python3
"""Piecewise debug of the AS138 heat-sector chain-rule identity at one jet."""
import numpy as np
src = open("AS138_ward_heat_check.py").read()
cut = src.index("# =====================================================================")
ns = {}
exec(compile(src[:cut], "mod", "exec"), ns)
sp = ns['sp']; x = ns['x']; t = ns['t']

# reconstruct the main objects
E_all = ns['euler_derivatives'](ns['heat_density_fn'], ns['fields_all'])
sum_chain = 0
for name in ns['fields_all']:
    sum_chain += ns['pair_E_lie'](E_all[name], name, ns['lie_map'][name])
sum_chain = ns['combine'](sum_chain)
d_fields = ns['dvariation_full_mode']('fields')
delta1 = ns['combine'](sum_chain - d_fields)

rng = np.random.default_rng(123)
def ev(e, rr=None):
    rr = rng if rr is None else rr
    syms = list(e.free_symbols)
    subs = {s: float(rr.uniform(-1,1)) for s in syms}
    if ns['Nvar'] in subs and abs(subs[ns['Nvar']])<1e-3: subs[ns['Nvar']]=1.0
    return float(e.subs(subs).evalf())

print("=== delta1 at 3 jets:", [abs(ev(delta1)) for _ in range(3)])

# per-sector comparison: split sum_chain by field-type
W_part = ns['combine'](sum(ns['pair_E_lie'](E_all[n], n, ns['lie_map'][n]) for n in ['W0','W1','W2','W3']))
L_part = ns['combine'](sum(ns['pair_E_lie'](E_all[n], n, ns['lie_map'][n]) for n in ['L0','L1','L2','L3']))
O_part = ns['combine'](sum(ns['pair_E_lie'](E_all[n], n, ns['lie_map'][n]) for n in ['lam0','U']))
print("W,L,O parts:", [abs(ev(W_part)), abs(ev(L_part)), abs(ev(O_part))])

# d_fields decomposition
Np = ns['N_poly']; A = ns['A_fun']; Gp, Jd, ell = ns['Gp'], ns['Jd'], ns['ell']
dLg = ns['combine'](Gp*(Jd*sp.diff(ns['LieF'](ns['W'][3]), x) + ell*sp.diff(ns['LieF'](ns['W'][3]), x, 2))
                    + ell*A*sp.diff(ns['LieF'](ns['W'][3]), x))
dLb = 0
for k in range(3):
    dLb += ns['poly'](ns['L'][k])*( ns['LieF'](ns['W'][k+1]) - ns['LieF'](ns['W'][k]) - sp.diff(ns['LieF'](ns['W'][k]), x, 2) )
    dLb += ns['LieF'](ns['L'][k])*( (ns['poly'](ns['W'][k+1])-ns['poly'](ns['W'][k])) - sp.diff(ns['poly'](ns['W'][k]), x, 2) )
dLc = ns['LieF'](ns['lam0'])*(ns['poly'](ns['W'][0])-ns['poly'](ns['U'])) + ns['poly'](ns['lam0'])*(ns['LieF'](ns['W'][0])-ns['LieF'](ns['U']))
dLb = ns['combine'](dLb); dLc = ns['combine'](dLc); dLg = ns['combine'](dLg)
print("d_fields sectors gate/bulk/lam0:", [abs(ev(Np*dLg)), abs(ev(Np*dLb)), abs(ev(Np*dLc))])
print("E-gate part:", abs(ev(ns['pair_E_lie'](E_all['W3'],'W3',ns['lie_map']['W3']))))
print("Np*dLg - E_W3 etc:", abs(ev(Np*dLg - ns['pair_E_lie'](E_all['W3'],'W3',ns['lie_map']['W3']))))
print("Np*dLc - E_lam0 - E_U - E_W0(lam0 part) ...")
# E_W0 - bulk part of E_W0:
print("E_W0 full:", abs(ev(ns['pair_E_lie'](E_all['W0'],'W0',ns['lie_map']['W0']))))
print("E_lam0:", abs(ev(ns['pair_E_lie'](E_all['lam0'],'lam0',ns['lie_map']['lam0']))))
print("E_U:", abs(ev(ns['pair_E_lie'](E_all['U'],'U',ns['lie_map']['U']))))
print("comb dLc vs E_W0+E_lam0+E_U:", abs(ev(Np*dLc - (ns['pair_E_lie'](E_all['W0'],'W0',ns['lie_map']['W0'])
                                        + ns['pair_E_lie'](E_all['lam0'],'lam0',ns['lie_map']['lam0'])
                                        + ns['pair_E_lie'](E_all['U'],'U',ns['lie_map']['U'])))))
# bulk: E_W0..E_W3 + E_L0..E_L3 vs Np*dLb
EW = ns['combine'](sum(ns['pair_E_lie'](E_all[n], n, ns['lie_map'][n]) for n in ['W0','W1','W2','W3']))
EL = ns['combine'](sum(ns['pair_E_lie'](E_all[n], n, ns['lie_map'][n]) for n in ['L0','L1','L2','L3']))
print("Np*dLb - (EW+EL):", abs(ev(Np*dLb - ns['combine'](EW+EL))))
print("Np*dLb - EW:", abs(ev(Np*dLb - EW)), " Np*dLb - EL:", abs(ev(Np*dLb - EL)))