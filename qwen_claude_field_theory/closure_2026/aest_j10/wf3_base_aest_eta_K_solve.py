#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_base_aest_eta_K_solve.py  (SOLVE A: C0_base / eta_K, owed item 1 of
v9_alpha2_ppn_status.md)
========================================================================
Base AeST (novel v9 terms OFF: bump=0, a0 const, plain K2 quadratic), the
boosted moving-source system {E_00,E_0i,E_ij,E_A,E_phi} + A^2=-1 at O(wU)
and O(w^2 U), independent unit aether retained, scalar retained.

Uses the CACHED quadratic action L2dc_v2.pkl (route2_v2_build.py: gauge
h01=h12=h13=0, s11=0; fields Psi,Phi,B2,B3,s22,s23,a1,a2,a3,chi; static
plane wave k=xhat; aether background A^mu=(1+wb^2 w.w/2, wb w^i); action
R - 2L - (K_B/2)F^2 + 2(2-K_B)J.dphi - (2-K_B)(1+J_Y)Y - K2(Q-Q0)^2 + matter).
Deep-field base-AeST limit: J_Y = dJcal/dY -> mu = 1 (solar u>>1).

EXTRACTION DICTIONARY: certified in wf3_will_dictionary_certificate.py and
validated END-TO-END (incl. w-orientation w_Will = -wb*w) against
Foster-Jacobson pure Einstein-aether in wf3_pure_ea_control_build.py:
    alpha_1 = +2 * [coeff of w2*Rk in B2^(1)] / U_amp
    alpha_2 = (Cpar - Cperp)/2 ,  C* = coeff of w*^2 in (-2 Psi^(2))/Rk/U_amp
    alpha_3 = Cperp + alpha_1   (must be 0: propagating sector, DC-019 gate)
    U_amp   = -Psi^(0)/Rk  (h00 = -2 Psi = 2U)
NOTE the committed fc_alpha2_preferred_frame_2026.py / route2_v2_* dictionaries
are WRONG (sign of alpha_1, missing 1/2 in alpha_2) - documented in the ground.

ANCHORS: (ii) Newton + gamma=1; (iii) alpha_1 -> -4K_B; alpha_3 == 0 gate;
K_B-off limit. Then eta_K := -alpha_1/4 and lam2_eff from
alpha_2 = eta_K(eta_K - lam2)/(2 lam2)  (BPS 1007.3503 eq 5.34 at beta=0 form).
kx=1 throughout: Q0 always appears as (Q0/kx); PPN scales = Q0 -> 0.
"""
import sympy as sp, pickle, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import os
SC = None  # locate the route2_v2_build.py cache in the session scratchpad
for root in ['/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula']:
    if os.path.isdir(root):
        for s in os.listdir(root):
            cand = os.path.join(root, s, 'scratchpad', 'L2dc_v2.pkl')
            if os.path.exists(cand):
                SC = os.path.join(root, s, 'scratchpad') + '/'
if SC is None:
    raise SystemExit("L2dc_v2.pkl cache not found; run route2_v2_build.py first")
L2dc = pickle.load(open(SC+'L2dc_v2.pkl', 'rb'))
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
wb = sp.symbols('w_b', positive=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT, LAM, kx = sp.symbols('G_t Lambda k_x', real=True)
def S(t): return sp.Symbol(t)
names = ['Psi', 'Phi', 'B2', 'B3', 's22', 's23', 'a1', 'a2', 'a3', 'chi']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok')
Psik, Phik, s22k, a1k, chik = S('Psik'), S('Phik'), S('s22k'), S('a1k'), S('chik')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None

def solve(sub_extra):
    """Full wb-ladder solve; returns (alpha1, alpha2, alpha3, U_amp, gamma)."""
    sub = {GT: 1, LAM: 0, kx: 1}; sub.update(sub_extra)
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
    eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
    s0s = lin(eq0, [S(n+'k') for n in stat])
    if s0s is None: return None
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0), a2k: sp.S(0), a3k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk)          # h00 = -2Psi = 2U
    gamma = sp.cancel(s0[Phik]/s0[Psik])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return ('SINGULAR-O(w)', U_amp, gamma)
    c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)          # CERTIFIED orientation (control)
    eq2 = [sp.expand(eqW[A].coeff(wb, 2)).subs(s1) for A in BRAS]
    s2 = lin(eq2, list(dk2.values()))
    if s2 is None: return (alpha1, 'SINGULAR-O(w2)', None, U_amp, gamma)
    h2 = sp.cancel(-2*sp.expand(dk2[Psik].subs(s2)))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    alpha2 = sp.cancel((Cpar - Cperp)/2)
    alpha3 = sp.cancel(Cperp + alpha1)
    return (alpha1, alpha2, alpha3, U_amp, gamma)

P("="*74)
P("PASS 1: numeric anchor points, base AeST deep field (J_Y = 1)")
P("="*74)
pts = [(sp.Rational(1, 5), 10, sp.Rational(2, 5)),
       (sp.Rational(3, 10), 7, sp.Rational(3, 5)),
       (sp.Rational(1, 10), 50, sp.Rational(9, 10)),
       (sp.Rational(1, 5), 10, sp.Rational(1, 25))]
for kb, k2, q0 in pts:
    r = solve({KB: kb, K2: sp.nsimplify(k2), Q0: q0, JY: 1})
    a1v, a2v, a3v, Ua, gm = r
    P(f"  K_B={kb} K2={k2} Q0={q0}:")
    P(f"    Newton U/rho = {sp.nsimplify(Ua)} (GR-lim 4pi/(1-KB/2)={sp.nsimplify(4*sp.pi/(1-kb/2))})"
      f"  gamma={sp.simplify(gm)}")
    P(f"    alpha_1 = {sp.simplify(a1v)}   (-4K_B = {-4*kb})  match={sp.simplify(a1v+4*kb)==0}")
    if not isinstance(a2v, str):
        P(f"    alpha_2 = {sp.simplify(a2v)} = {float(a2v):.6g}")
        P(f"    alpha_3 = {sp.simplify(a3v)}   (gate: 0)")
    else:
        P(f"    {a2v}")
P(f"({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("PASS 2: SYMBOLIC solve, K_B,K2,Q0 symbolic, J_Y symbolic")
P("="*74)
try:
    r = solve({})
    a1s, a2s, a3s, Uas, gms = r
    a1s = sp.simplify(a1s); a3s = sp.simplify(a3s)
    P("  U_amp   =", sp.simplify(Uas))
    P("  gamma   =", sp.simplify(gms))
    P("  alpha_1 =", a1s)
    P("  alpha_3 =", a3s)
    a2s = sp.simplify(a2s)
    P("  alpha_2(K_B,K2,Q0,J_Y) =", a2s)
    pickle.dump({'alpha1': a1s, 'alpha2': a2s, 'alpha3': a3s},
                open(SC+'wf3_alphas_symbolic.pkl', 'wb'))
    P(f"  cached -> wf3_alphas_symbolic.pkl ({time.time()-T0:.1f}s)")
    P("")
    P("  eta_K := -alpha_1/4 =", sp.simplify(-a1s/4))
    P("  eta_K - K_B         =", sp.simplify(-a1s/4 - KB))
    a2_J1 = sp.simplify(a2s.subs(JY, 1))
    P("  alpha_2 (J_Y=1)     =", a2_J1)
    a2_ppn = sp.simplify(sp.limit(a2_J1, Q0, 0))
    P("  alpha_2 (J_Y=1, Q0->0 PPN) =", a2_ppn)
    a2_Jinf = sp.simplify(sp.limit(a2s, JY, sp.oo))
    P("  alpha_2 (J_Y->oo)   =", a2_Jinf, "  [Route-3 cross-check: C0=-K_B/2?]")
    etaK = sp.simplify(-a1s/4)
    lam2_eff = sp.simplify(etaK**2/(2*a2s + etaK))
    P("  lam2_eff = etaK^2/(2 alpha2 + etaK) =", sp.simplify(lam2_eff.subs(JY, 1)))
except Exception as e:
    P("  SYMBOLIC PASS FAILED:", repr(e))
P(f"done ({time.time()-T0:.1f}s)")
