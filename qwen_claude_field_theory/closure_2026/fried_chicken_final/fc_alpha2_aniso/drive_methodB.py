#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grid sweep + light-scalar limit for METHOD B (imports the cached-build module)."""
import time, itertools, sys, json, importlib
sys.path.insert(0, '.')
import sympy as sp
_MODNAME = sys.argv[1] if len(sys.argv) > 1 else 'fc_alpha2_methodB_2026'
M = importlib.import_module(_MODNAME)
print(f"[driver] using module {_MODNAME}", flush=True)

T = time.time()
P = lambda *a: print(*a, flush=True)

grid = list(itertools.product([0.05, 0.3], [10.0, 300.0], [0.2, 0.9], [1.0, 2.0]))
P("="*100)
P("METHOD B  FC-AeST preferred-frame  alpha_1, alpha_2(perp/par)  full grid")
P(f"{'K_B':>5}{'K2':>7}{'Q0':>5}{'JY':>4} | {'alpha_1':>11} V1 | {'a2_perp':>13}{'a2_par':>13} V2 | gamma | mPsi2=K2Q0^2")
rows = []
for kbv, k2v, q0v, jyv in grid:
    t0 = time.time()
    r = M.solve_point(kbv, k2v, q0v, jyv)
    if r['status'] != 'ok':
        P(f"{kbv:5}{k2v:7}{q0v:5}{jyv:4} | {r['status']}"); continue
    a1 = complex(r['alpha1']); a2p = complex(r['a2_perp']); a2l = complex(r['a2_par'])
    v1 = abs(a1.real + 4*kbv) < 1e-9 and abs(a1.imag) < 1e-9
    v2 = abs(a2p - a2l) < 1e-9
    gam = r['gamma']
    rows.append((kbv, k2v, q0v, jyv, a1.real, a2p.real, a2l.real, v1, v2, str(gam)))
    P(f"{kbv:5}{k2v:7}{q0v:5}{jyv:4} | {a1.real:+11.6f} {'Y' if v1 else 'N'} | "
      f"{a2p.real:13.6g}{a2l.real:13.6g} {'Y' if v2 else 'N'} | {gam} | {k2v*q0v**2:.3g}  [{time.time()-t0:.0f}s]")

P("="*100)
P("gauge-consistency: the 4 UNVARIED gauge-fixed EOMs (H01,H11,H12,H13) must vanish on-solution:")
for (kbv, k2v, q0v, jyv) in [(0.05, 10.0, 0.2, 1.0), (0.3, 300.0, 0.9, 2.0)]:
    gc = M.gauge_consistency(kbv, k2v, q0v, jyv)
    if gc is None:
        P(f"  ({kbv},{k2v},{q0v},{jyv}): solve failed"); continue
    ok = all(all(v == 0 for v in vals) for vals in gc.values())
    P(f"  ({kbv},{k2v},{q0v},{jyv}): {'ALL ZERO (pass)' if ok else 'NONZERO RESIDUAL: '+str(gc)}")
P("="*100)
allV1 = all(x[7] for x in rows) if rows else False
allV2 = all(x[8] for x in rows) if rows else False
P(f"V1 (alpha_1=-4K_B) all points: {'PASS' if allV1 else 'FAIL'}")
P(f"V2 (a2_perp==a2_par) all points: {'PASS' if allV2 else 'FAIL'}")
valid = [x for x in rows if x[8]]
if valid:
    amin = min(valid, key=lambda x: abs(x[5]))
    P(f"min |alpha_2| over V2-consistent points = {abs(amin[5]):.6g}  at (K_B,K2,Q0,JY)={amin[:4]}")
    P(f"bound |alpha_2| < 1e-7 : {'a point satisfies it' if abs(amin[5])<1e-7 else 'ALL POINTS EXCEED (fails bound)'}")
# dump json
with open('methodB_grid.json', 'w') as f:
    json.dump({'rows': [{'K_B':x[0],'K2':x[1],'Q0':x[2],'JY':x[3],'alpha1':x[4],
                         'a2_perp':x[5],'a2_par':x[6],'V1':x[7],'V2':x[8],'gamma':x[9]} for x in rows]}, f, indent=2)
P(f"[grid {time.time()-T:.0f}s]  -> methodB_grid.json")

# ---------------- light-scalar (PPN) limit: alpha_2 as K2 Q0^2 -> 0 -----------------
# Solve with K_2 kept SYMBOLIC (K_B,Q0,JY numeric), extract alpha_2(K2), take K2->0.
P("="*100); P("light-scalar limit  K_2 Q_0^2 -> 0  (Solar-System PPN-relevant):")
K2s = sp.Symbol('K_2', positive=True)
def solve_symbolic_K2(kbv, q0v, jyv):
    sub = {M.KB: sp.nsimplify(kbv), M.Q0: sp.nsimplify(q0v), M.JY: sp.nsimplify(jyv),
           M.GT: 1, M.kx: 1, M.ky: 0, M.kz: 0}   # K_2 stays symbolic
    L = sp.expand(sp.expand(M.L2dc.subs(M.GAUGE)).subs(sub))
    eqf = {A: sp.expand(sp.diff(L, A)) for A in M.BRAS}
    VZ = {M.Bk[1]:0, M.Bk[2]:0, M.ak[1]:0, M.ak[2]:0, M.hk[(2,3)]:0}
    su = [M.Psik, M.hk[(2,2)], M.hk[(3,3)], M.ak[0], M.chik]
    sb = [M.Psib, M.hb[(2,2)], M.hb[(3,3)], M.ab[0], M.chib]
    e0 = [sp.expand(eqf[A].coeff(M.wb,0).subs(VZ)) for A in sb]
    s0s = M.lin_solve(e0, su)
    if s0s is None: return None
    s0 = {**s0s, M.Bk[1]:sp.S(0), M.Bk[2]:sp.S(0), M.ak[1]:sp.S(0), M.ak[2]:sp.S(0), M.hk[(2,3)]:sp.S(0)}
    d1 = {A: sp.Symbol(f'd1_{A}') for A in M.KETS}; d2 = {A: sp.Symbol(f'd2_{A}') for A in M.KETS}
    subFull = {A: s0[A] + M.wb*d1[A] + M.wb**2*d2[A] for A in M.KETS}
    eqW = {A: sp.expand(eqf[A].subs(subFull)) for A in M.BRAS}
    s1 = M.lin_solve([sp.expand(eqW[A].coeff(M.wb,1)) for A in M.BRAS], list(d1.values()))
    if s1 is None: return None
    e2 = [sp.expand(eqW[A].coeff(M.wb,2)).subs(s1) for A in M.BRAS]
    s2 = M.lin_solve(e2, list(d2.values()))
    if s2 is None: return None
    kvl = lambda A: sp.expand(s0[A] + M.wb*d1[A].subs(s1) + M.wb**2*d2[A].subs(s2))
    subU = {M.Rk: -M.Uh/(4*sp.pi)}
    B2 = sp.expand(kvl(M.Bk[1]).coeff(M.wb,1).subs(subU)); a1 = sp.cancel(2*B2.coeff(M.w2*M.Uh))
    Psi2 = sp.expand(kvl(M.Psik).coeff(M.wb,2).subs(subU))
    PA = sp.cancel(-2*Psi2.coeff(M.w2**2*M.Uh)); PApar = sp.cancel(-2*Psi2.coeff(M.w1**2*M.Uh))
    a2p = sp.cancel((PA+a1)/2); a2l = sp.cancel(-(PApar-PA)/2)
    return a1, a2p, a2l

for kbv, q0v, jyv in [(0.05,0.2,1.0),(0.3,0.9,1.0),(0.3,0.2,2.0),(0.05,0.9,2.0)]:
    t0=time.time()
    res = solve_symbolic_K2(kbv,q0v,jyv)
    if res is None:
        P(f"  K_B={kbv} Q0={q0v} JY={jyv}: solve failed"); continue
    a1,a2p,a2l = res
    a1s = sp.nsimplify(a1); dd = sp.simplify(a2p-a2l)
    a2_full = sp.simplify(a2p)
    a2_light = sp.limit(a2_full, K2s, 0)
    a2_heavy = sp.limit(a2_full, K2s, sp.oo)
    P(f"  K_B={kbv} Q0={q0v} JY={jyv}: alpha_1={a1s}  V2diff={dd}")
    P(f"      alpha_2(K2) = {a2_full}")
    P(f"      alpha_2(K2 Q0^2 -> 0, light)  = {a2_light}")
    P(f"      alpha_2(K2 Q0^2 -> oo, heavy) = {a2_heavy}   [{time.time()-t0:.0f}s]")
P(f"[total {time.time()-T:.0f}s]")
