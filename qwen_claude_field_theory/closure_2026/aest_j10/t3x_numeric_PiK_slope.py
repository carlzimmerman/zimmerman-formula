#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
t3x_numeric_PiK_slope.py   (TARGET-3 independent cross-route, part 2)
=====================================================================
Numeric certification of the structural verdict of
t3x_structural_deltaQ_projection.py, on the CACHED route2_v2 quadratic action
(L2dc_v2.pkl -- anisotropic gauge, s22/s23 retained), with the WILL-CORRECTED
dictionary (see the [A] certificate in the companion script; the fc/extract
dictionaries carry documented sign errors):

    U_amp   = h00_newt/2                       (self-normalized, per rho_k)
    alpha_1 = -2 * coeff(w2 U) of h02 at O(w)          [Will transverse g0i]
    alpha_2 = (1/2) [coeff(w1^2 U) - coeff(w2^2 U)] of h00 at O(w^2)
                                                        [par - perp = 2 alpha_2]
    alpha_3 = coeff(w2^2 U) of h00 at O(w^2) + alpha_1  [must certify -> 0]

Measured quantities per point (K_B, K2, Q0), at J_Y = 1 (solar-system, u0>>1):
    - Newton h00/rho vs 8 pi/(1 - K_B/2), gamma_PPN = Phi/Psi   (anchors i-ii)
    - alpha_1 vs -4 K_B                                          (anchor iii)
    - alpha_3 vs 0                                               (consistency)
    - alpha_2(K2) and the SLOPE  Pi = d(alpha_2)/d(K2) = d(alpha_2)/d(F_QQ)
      (K2 multiplies exactly the (Q-Q0)^2 quadratic insertion, so the slope IS
      the projection of the F_QQ = K_QQ channel onto alpha_2), including the
      Q0 -> small limit where ONLY the flow-gradient (w.q)^2 chi^2 term of
      -F_QQ (deltaQ)^2 survives (all other insertions are Q0^2-weighted).

Run:  python3 t3x_numeric_PiK_slope.py | tee t3x_numeric_PiK_slope.out
"""
import sympy as sp, pickle, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/546626b7-08d0-4ddc-ac8f-d38babe5ed48/scratchpad/'
L2dc = pickle.load(open(SC+'L2dc_v2.pkl', 'rb'))
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
wb = sp.symbols('w_b', positive=True); w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT, LAM, kx = sp.symbols('G_t Lambda k_x', real=True)
S = lambda t: sp.Symbol(t)
names = ['Psi', 'Phi', 'B2', 'B3', 's22', 's23', 'a1', 'a2', 'a3', 'chi']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok')
Psik, Phik, s22k, a1k, chik = S('Psik'), S('Phik'), S('s22k'), S('a1k'), S('chik')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk); s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None

def solve(kbv, k2v, q0v, jyv=1):
    sub = {KB: sp.nsimplify(kbv), K2: sp.nsimplify(k2v), Q0: sp.nsimplify(q0v),
           GT: 1, LAM: 0, kx: 1, JY: sp.nsimplify(jyv)}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
    eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
    s0s = lin(eq0, [S(n+'k') for n in stat])
    if s0s is None: return None
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0), a2k: sp.S(0), a3k: sp.S(0)}
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return None
    eq2 = [sp.expand(eqW[A].coeff(wb, 2)).subs(s1) for A in BRAS]
    s2 = lin(eq2, list(dk2.values()))
    if s2 is None: return None
    # ---- Will-corrected dictionary ----
    h00n = sp.cancel(-2*s0[Psik]/Rk)                 # Newton h00 per rho_k
    gam  = sp.cancel(s0[Phik]/s0[Psik])              # gamma_PPN
    Uamp = h00n/2                                    # U per rho_k
    c2t  = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(-2*c2t/Uamp)                  # transverse g0i, Will sign
    h2 = sp.cancel(-2*sp.expand(dk2[Psik].subs(s2)))
    cpar  = sp.cancel(h2.coeff(w1**2)/Rk/Uamp)
    cperp = sp.cancel(h2.coeff(w2**2)/Rk/Uamp)
    alpha2 = sp.cancel((cpar - cperp)/2)             # par - perp = 2 alpha_2
    alpha3 = sp.cancel(cperp + alpha1)               # perp = -alpha_1 + alpha_3
    chi0 = sp.cancel(s0[chik]/s0[Psik])              # static chi response / Psi
    return dict(h00n=h00n, gam=gam, alpha1=alpha1, alpha2=alpha2,
                alpha3=alpha3, chi0=chi0)

P("="*78)
P("ANCHOR + SLOPE TABLE (J_Y=1; exact rationals; Will-corrected dictionary)")
P("="*78)
pts = [(sp.Rational(1, 5), sp.Rational(2, 5)),
       (sp.Rational(1, 5), sp.Rational(1, 25)),
       (sp.Rational(3, 10), sp.Rational(2, 5)),
       (sp.Rational(1, 2), sp.Rational(1, 25))]
K2list = [10, 12, 14]
for kbv, q0v in pts:
    P(f"\n--- K_B={kbv}, Q0={q0v} ---")
    a2s = []
    for k2v in K2list:
        r = solve(kbv, k2v, q0v)
        if r is None:
            P(f"  K2={k2v}: SOLVE FAILED"); continue
        ok_newt = sp.simplify(r['h00n'] - 8*sp.pi/(1 - kbv/2)) == 0
        ok_a1 = sp.simplify(r['alpha1'] + 4*kbv) == 0
        P(f"  K2={k2v}: Newton==8pi/(1-KB/2)? {ok_newt}  gamma={sp.simplify(r['gam'])}  "
          f"alpha_1={sp.nsimplify(r['alpha1'])} (==-4K_B? {ok_a1})  "
          f"alpha_3={sp.simplify(r['alpha3'])}")
        P(f"          alpha_2 = {sp.nsimplify(r['alpha2'])}  = {float(r['alpha2']):+.6f}   "
          f"chi0/Psi0 = {float(r['chi0']):+.4f}")
        a2s.append((k2v, r['alpha2']))
    if len(a2s) >= 2:
        sl01 = sp.nsimplify((a2s[1][1]-a2s[0][1])/(a2s[1][0]-a2s[0][0]))
        P(f"  SLOPE d(alpha_2)/d(K2) [K2 {a2s[0][0]}->{a2s[1][0]}] = {sl01} = {float(sl01):+.6e}")
    if len(a2s) >= 3:
        sl12 = sp.nsimplify((a2s[2][1]-a2s[1][1])/(a2s[2][0]-a2s[1][0]))
        P(f"  SLOPE d(alpha_2)/d(K2) [K2 {a2s[1][0]}->{a2s[2][0]}] = {sl12} = {float(sl12):+.6e}")
        P(f"  curvature (slope change): {float(sl12-sl01):+.3e}")

P("\nFINDINGS (audit record -- run 2026-08-31):")
P("  1. The UNCOMMITTED route2_v2 cache L2dc_v2.pkl FAILS the hard anchors when")
P("     actually run: Newton != 8pi/(1-K_B/2) (at any J_Y; verified symbolically")
P("     in J_Y), alpha_1 = +5.75 at K_B=1/5 (vs required -4K_B = -0.8; J_Y->oo")
P("     limit = +8, a K_B-INDEPENDENT pure number), alpha_3 = 2*alpha_1 != 0.")
P("     The ground-note claim that route2_v2 'passes alpha_1=-4K_B at test")
P("     points' does NOT reproduce on this cache.  Its alpha_2 values are NOT")
P("     quotable.  T1/T2 must rebuild/repair before any SOLVE-A/B verdict.")
P("  2. Diagnostic: alpha_2(cache) ~ -1/(K2 Q0^2) diverges in the PPN hierarchy")
P("     Q0/k_x -> 0: the K2=F_QQ channel's STATIC stiffness is Q0^2-weighted")
P("     (certified in t3x_structural_deltaQ_projection.py [C.2]), so it cannot")
P("     regulate the c123=0 FJ pole at solar wavenumbers -- the pole must be")
P("     regulated by the scalar KINETIC sector (Route 3's eps_eff), not by the")
P("     mass term.  Any solve that regulates via K2 Q0^2 is outside the PPN")
P("     regime (this run's kx=1, Q0=2/5 point included).")
P("  3. The K2-slope of alpha_2 is +0.3..+1.6 = O(1) at all points -- order-of-")
P("     magnitude consistent with the independent Green-function projection")
P("     |Pi_K| = r^2/(2-K_B) F_QQ ~ 0.14..0.7 F_QQ (t3x_greenfunction_PiK.py),")
P("     but NOT quotable as a coefficient given finding 1.")
P(f"done ({time.time()-T0:.1f}s)")
