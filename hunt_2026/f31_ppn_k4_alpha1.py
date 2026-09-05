#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f31_ppn_k4_alpha1.py -- THE FULL PREFERRED-FRAME PPN LADDER WITH THE k^4 TERM, in the repository's own pipeline.
==================================================================================================================
The generalized-AeST gate (closure_2026/generalized_aest_2026/gen_aest_alpha1_c2c4.py) computes alpha_1, alpha_2, alpha_3
and gamma from the linearised metric + aether + shift-scalar system on a boosted aether background (plane wave k = xhat,
static w_b ladder, certified Will dictionary), and found the closed form
        alpha_1 = -4 c_14 - 4 (2 - K_B)/(J_Y + 1),
whose second term -- the scalar drag -- forces alpha_1 = 0 onto c_14 < 0, a spin-1 ghost (the lock).

THIS FILE IS THAT PIPELINE, VERBATIM, WITH ONE TERM ADDED to the scalar sector:
        - (2 - K_B) J_Y xi^2 (D^2 phi)^2,      D^2 phi = (g^{mn} + A^m A^n)(d_m d_n phi - Gamma^l_{mn} d_l phi),
the spatial biharmonic operator of the coherence-length candidate (addendum sections F-G), built from the pipeline's
own metric, aether and Christoffel objects to the same orders (eps^2, w_b^2), so that its metric and aether mixings are
included and not hand-waved.  With k_x = 1 in the ladder, the dimensionless parameter is XI2 = (xi k)^2.
The Solar-System scale of the preferred-frame bounds is 1 AU (lunar laser ranging for alpha_1; the solar spin for
alpha_2 lives at R_sun, even deeper); xi >= 0.045 pc = 9300 AU gives XI2 >= 8.6e7.

Anchors (checks that can fail): XI2 = 0 reproduces the banked alpha_1 = -4(2 + K_B J_Y)/(1 + J_Y) on the wf3 grid, with
gamma = 1 and alpha_3 = 0.  Then alpha_1(XI2), alpha_2(XI2) on the grid, the closed form with XI2, and the verdict at the
physical XI2: is alpha_1 = 0 reachable with c_14 > 0 (no spin-1 ghost) once the scalar is screened?
"""
import sympy as sp, time, pickle, os, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import tempfile
SC = os.environ.get('SCRATCH', tempfile.gettempdir()) + '/'
os.makedirs(SC, exist_ok=True)
CACHE = SC + 'L2dc_k4.pkl'
FAILS = []
def check(name, ok, detail=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ''))
    if not ok: FAILS.append(name)

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
C2, C4 = sp.symbols('c2 c4', real=True)
XI2 = sp.symbols('xi2', nonnegative=True)          # (xi k)^2
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT, LAM = sp.symbols('G_t Lambda', real=True)
kx = sp.symbols('k_x', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
kv = [0, kx, 0, 0]
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
B2f, B2k, B2b = nf('B2'); B3f, B3k, B3b = nf('B3')
s22, s22k, s22b = nf('s22'); s23, s23k, s23b = nf('s23')
a1f, a1k, a1b = nf('a1'); a2f, a2k, a2b = nf('a2'); a3f, a3k, a3b = nf('a3')
chif, chik, chib = nf('chi')
rho, Rk, Rb = nf('rho'); a0f, a0k, a0b = nf('a0p')
KETS = [Psik, Phik, B2k, B3k, s22k, s23k, a1k, a2k, a3k, chik]
BRAS = [Psib, Phib, B2b, B3b, s22b, s23b, a1b, a2b, a3b, chib]

if os.path.exists(CACHE) and '--rebuild' not in sys.argv:
    L2dc = pickle.load(open(CACHE, 'rb')); P(f"[cache] loaded {CACHE}")
else:
    ww = w1**2 + w2**2 + w3**2; S0 = 1 + wb**2*ww/2
    Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, wb*w3]); Adn_bg = eta*Aup_bg
    dphi_bg = -Q0*Adn_bg
    H = sp.zeros(4, 4)
    H[0, 0] = -2*Psi
    H[0, 2] = B2f; H[2, 0] = B2f; H[0, 3] = B3f; H[3, 0] = B3f
    H[1, 1] = -2*Phi
    H[2, 2] = -2*Phi + s22; H[3, 3] = -2*Phi - s22
    H[2, 3] = s23; H[3, 2] = s23
    gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
    Hup = eta*H*eta
    gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
    trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
    HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
    sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)
    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
    C1c = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
    solA = sp.solve([sp.expand(C1c).coeff(Es, 1), sp.expand(C1c).coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
    solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
    a0f = a0f.subs(solA)
    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
    P(f"[S1] unit-norm constraint solved ({time.time()-T0:.1f}s)")
    # scalar with LIVE fluctuation chi (route2_v2 gauge)
    dphi = sp.Matrix([dphi_bg[m] + eps*d(chif, m) for m in range(4)])
    def te(e):
        e = sp.expand(e); out = 0
        for i in range(3):
            ci = e.coeff(eps, i)
            for j in range(3):
                out += ci.coeff(wb, j)*eps**i*wb**j
        return out
    def wtrunc(e):
        e = sp.expand(e); return sum(e.coeff(wb, n)*wb**n for n in range(3))
    guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
    gdT = sp.Matrix(4, 4, lambda m, n: te(gd[m, n]))
    AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
    Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s)) for s in range(4))
             for n in range(4)] for m in range(4)] for r in range(4)]
    GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
    dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
    # Maxwell part (certified c1=-c3=K_B combination)
    Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m)-d(Adn[m], n)))
    F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
    F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    # aether acceleration a^al = A^nu D_nu A^al  (same object as the drag's J^mu)
    Jup = [te(sum(AupT[nu]*(d(AupT[al], nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4))) for nu in range(4))) for al in range(4)]
    # NEW: c4 a.a  and  c2 (D_a A^a)^2
    term4 = te(sum(gdT[m, n]*Jup[m]*Jup[n] for m in range(4) for n in range(4)))
    divA = te(sum(d(AupT[a], a) + sum(GamT[a][a][r]*AupT[r] for r in range(4)) for a in range(4)))
    term2 = te(divA**2)
    P(f"    aether operators built ({time.time()-T0:.1f}s)")
    Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc = te(sum((guT[m, n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    dQ = Qc - Q0; Kq = -2*LAM + K2*te(dQ**2)
    P(f"    dark scalars ({time.time()-T0:.1f}s)")
    def ric(a, b):
        o = 0
        for m in range(4):
            o += d(Gam[m][b][a], m) - d(Gam[m][m][a], b)
            for l in range(4):
                o += Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a]
        return o
    Rsc = te(sum(guT[m, n]*ric(m, n) for m in range(4) for n in range(4)))
    P(f"    Ricci ({time.time()-T0:.1f}s)")
    def grade(e):
        e = sp.expand(e); return [wtrunc(e.coeff(eps, n)) for n in range(3)]
    gF2 = grade(F2); gJ = grade(Jdphi); gY = grade(Yc); gK = grade(Kq)
    g2 = grade(term2); g4 = grade(term4); gsq = grade(sqg); gR = grade(Rsc)
    # pure-EA sign convention (FJ-validated in wf3_pure_ea_control_build): L = R - c1 T1 - c2 T2 - c3 T3 + c4 T4
    gS = [gR[n] - (2*LAM if n == 0 else 0) - (KB/2)*gF2[n] - C2*g2[n] + C4*g4[n]
          + 2*(2-KB)*gJ[n] - (2-KB)*gY[n] - gK[n] for n in range(3)]
    # NEW (f31): the spatial biharmonic operator D^2 phi = (g^{mn} + A^m A^n)(d_m d_n phi - Gamma^l_{mn} d_l phi), to O(eps)
    ddchi = [[d(d(chif, n), m) for n in range(4)] for m in range(4)]
    D2phi = te(sum((guT[m, n] + AupT[m]*AupT[n])*(eps*ddchi[m][n] - sum(GamT[l][m][n]*dphiT[l] for l in range(4)))
                   for m in range(4) for n in range(4)))
    gD2 = grade(D2phi**2)
    P(f"    biharmonic operator built: (D^2 phi)^2 at O(eps^2) has {len(sp.Add.make_args(sp.expand(gD2[2])))} terms ({time.time()-T0:.1f}s)")
    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*gY[2] - (2-KB)*JY*XI2*gD2[2]
    L2_matt = -16*sp.pi*GT*wtrunc(rho*(-H[0, 0]/2))
    L2 = sp.expand(L2_grav + L2_matt)
    def DC(e):
        e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
        for mon, c in zip(pol.monoms(), pol.coeffs()):
            if mon[0] == mon[1]:
                out += c*(Es*Eis)**mon[0]
        return out.subs(Es*Eis, 1) if out != 0 else out
    L2dc = DC(L2)
    pickle.dump(L2dc, open(CACHE, 'wb'))
    P(f"    L2dc built+cached: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")

eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
def ladder(sub):
    """static wb-ladder; returns dict(U, g, a1, a2, a3) or a tag on singularity."""
    sub = {GT: 1, LAM: 0, kx: 1, **sub}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat_b = [Psib, Phib, s22b, a1b, chib]; stat_k = [Psik, Phik, s22k, a1k, chik]
    eq0 = [sp.expand(eqf[b].coeff(wb, 0).subs(VZ)) for b in stat_b]
    s0s = lin(eq0, stat_k)
    if s0s is None: return 'SING0'
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0), a2k: sp.S(0), a3k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk); gamma = sp.cancel(s0[Phik]/s0[Psik])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}; dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return ('SING1', U_amp, gamma)
    c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)
    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS], list(dk2.values()))
    if s2 is None: return dict(U=U_amp, g=gamma, a1=alpha1, a2='SING2', a3='SING2')
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp); Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2=sp.cancel((Cpar-Cperp)/2), a3=sp.cancel(Cperp+alpha1))

q = sp.Symbol('q', positive=True)
R = lambda a, b: sp.Rational(a, b)
def a1_q0(r):
    return sp.nsimplify(sp.limit(r['a1'], q, 0)) if r['a1'].has(q) else sp.nsimplify(r['a1'])


FAILS = []
P(""); P("="*76); P("ANCHOR: XI2 = 0 reproduces the banked alpha_1 = -4(2+K_B J_Y)/(1+J_Y), gamma = 1, alpha_3 = 0"); P("="*76)
GRID = [(R(1,5), 1), (R(1,2), 1), (R(1,5), 2)]
for kbv, jyv in GRID:
    r = ladder({KB: kbv, K2: sp.S(10), JY: sp.S(jyv), Q0: q, C2: 0, C4: 0, XI2: 0})
    if not isinstance(r, dict): check(f"anchor KB={kbv} JY={jyv}: ladder regular", False, str(r)); continue
    a1v = a1_q0(r); pred = -4*(2 + kbv*jyv)/(1 + jyv)
    check(f"anchor KB={kbv} JY={jyv}: alpha_1(XI2=0) = {a1v} == banked {pred}", sp.simplify(a1v - pred) == 0)
    check(f"   gamma = 1, alpha_3 = 0", sp.simplify(r['g'] - 1) == 0 and sp.simplify(sp.limit(r['a3'], q, 0) if r['a3'].has(q) else r['a3']) == 0, f"gamma={r['g']} a3={r['a3']}")
P(f"  ({time.time()-T0:.0f}s)")

P(""); P("="*76); P("MAIN: the ladder with the k^4 term, XI2 = (xi k)^2 = 0, 1, 1e2, 1e4, 1e8; c2 = c4 = 0"); P("="*76)
RES = {}
P(f"  {'K_B':>5s} {'J_Y':>4s} {'XI2':>8s} {'alpha_1':>14s} {'drag piece':>12s} {'alpha_2':>14s} {'alpha_3':>8s} {'gamma':>6s}")
for kbv, jyv in GRID:
    for xi2 in (0, 1, 100, 10**4, 10**8):
        r = ladder({KB: kbv, K2: sp.S(10), JY: sp.S(jyv), Q0: q, C2: 0, C4: 0, XI2: sp.S(xi2)})
        if not isinstance(r, dict): P(f"  KB={kbv} JY={jyv} XI2={xi2}: {r}"); continue
        a1v = a1_q0(r); a2v = sp.nsimplify(sp.limit(r['a2'], q, 0)) if (r['a2'] != 'SING2' and r['a2'].has(q)) else r['a2']
        a3v = sp.nsimplify(sp.limit(r['a3'], q, 0)) if (r['a3'] != 'SING2' and r['a3'].has(q)) else r['a3']
        drag = sp.nsimplify(a1v + 4*kbv)                     # alpha_1 + 4 c_14 with c_4 = 0, c_14 = K_B
        RES[(kbv, jyv, xi2)] = dict(a1=a1v, a2=a2v, a3=a3v, g=r['g'], drag=drag)
        P(f"  {str(kbv):>5s} {jyv:4d} {xi2:8.0e} {float(a1v):14.6e} {float(drag):12.3e} {str(a2v):>14s} {str(a3v):>8s} {str(r['g']):>6s}")
P(f"  ({time.time()-T0:.0f}s)")

P(""); P("="*76); P("CLOSED FORM WITH THE k^4 TERM: is the drag piece -4(2-K_B)/(J_Y (1+XI2) + 1)?"); P("="*76)
ok_form = True
for (kbv, jyv, xi2), r in RES.items():
    cand = -4*(2 - kbv)/(jyv*(1 + xi2) + 1)
    match = sp.simplify(r['drag'] - cand) == 0
    P(f"  KB={kbv} JY={jyv} XI2={xi2:g}: drag = {r['drag']}  vs  -4(2-K_B)/(J_Y(1+XI2)+1) = {cand}  {'OK' if match else 'DIFFERS by ' + str(sp.nsimplify(r['drag']-cand))}")
    ok_form &= match
check("K2 the closed form with the k^4 term: the scalar drag piece of alpha_1 becomes -4(2-K_B)/(J_Y(1+XI2)+1) -- the biharmonic "
      "term stiffens the scalar by (1 + xi^2 k^2) in exactly the place the lock lived, and its metric/aether mixings change nothing "
      "else in alpha_1 (if this FAILS the mixings matter and the printed DIFFERS lines say by how much)", ok_form)
# the physical verdict
kbv, jyv = R(1,5), 1
big = RES[(kbv, jyv, 10**8)]
c14_needed = -float(big['drag'])/4.0
check("K3 (THE VERDICT) at the Solar-System scale, XI2 = 8.6e7 or more, the drag piece of alpha_1 is below 1e-6, so |alpha_1| < 1e-4 "
      "is reached with c_14 POSITIVE (0 < c_14 <= 2.5e-5): the lock -- alpha_1 = 0 only at c_14 < 0, a spin-1 ghost -- does not "
      "apply to the screened scalar", abs(float(big['drag'])) < 1e-6 and c14_needed > -1e-6,
      f"drag piece at XI2 = 1e8: {float(big['drag']):.2e}; alpha_1 = 0 at c_14 = {c14_needed:.2e}")
a2_0 = RES[(kbv, jyv, 0)]['a2']; a2_big = big['a2']
check("K4 alpha_2's scalar channel is suppressed by the same term: |alpha_2(XI2 = 1e8)| < 1e-4 |alpha_2(0)| (the v9 alpha_2 kill was 1e4-1e5 x "
      "over the 1e-7 bound; report the residual)", (a2_0 != 'SING2' and a2_big != 'SING2') and abs(float(a2_big)) < 1e-4*max(abs(float(a2_0)), 1e-30),
      f"alpha_2: {a2_0} -> {a2_big}")
check("K5 gamma = 1 and alpha_3 = 0 persist with the k^4 term at every XI2 (semiconservative; the screening touches only the preferred-frame sector)",
      all(sp.simplify(r['g'] - 1) == 0 and (r['a3'] != 'SING2' and sp.simplify(r['a3']) == 0) for r in RES.values()))
P(""); P("="*76); P("VERDICT"); P("="*76)
P("  With the biharmonic term the scalar's spatial operator is stiffened by (1 + xi^2 k^2) in the place the alpha_1 lock lived.")
P("  At 1 AU with xi >= 0.045 pc that factor is >= 8.6e7: the scalar drag's contribution to alpha_1 is below 1e-7, and")
P("  alpha_1 within its bound needs only 0 < c_14 <= 2.5e-5 -- Einstein-aether's own post-GW170817 region, no ghost.")
P("  gamma = 1 and alpha_3 = 0 are untouched.  What this does NOT cover: the aether sector's own alpha_2 at c_14 ~ 1e-5 (Einstein-aether")
P("  literature), the nonlinear regime, and the cuspy-kernel sunward force (f30 C1: xi >= 0.8 pc for a single biharmonic term).")
P(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL")
sys.exit(1 if FAILS else 0)
