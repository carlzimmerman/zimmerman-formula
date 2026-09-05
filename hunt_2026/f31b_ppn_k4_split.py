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
CACHE = SC + 'L2dc_k4_split.pkl'
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
XA, XB, XC = sp.symbols('xA xB xC', nonnegative=True)
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
    XA, XB, XC = sp.symbols('xA xB xC', nonnegative=True)     # switches for the three pieces of (D^2 phi)^2
    D2q = sp.expand(gD2[2]); D2chi2 = 0; D2cross = 0; D2metric = 0
    for term in sp.Add.make_args(D2q):
        nchi = sum(sp.degree(term, s_) for s_ in (chik, chib))
        if nchi == 2: D2chi2 += term
        elif nchi == 1: D2cross += term
        else: D2metric += term
    P(f"    (D^2 phi)^2 split: chi-chi {len(sp.Add.make_args(sp.expand(D2chi2)))} terms, chi-metric/aether {len(sp.Add.make_args(sp.expand(D2cross)))}, metric/aether only {len(sp.Add.make_args(sp.expand(D2metric)))}")
    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*gY[2] - (2-KB)*JY*XI2*(XA*D2chi2 + XB*D2cross + XC*D2metric)
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
P(""); P("="*76); P("SPLIT DIAGNOSTIC: which piece of (D^2 phi)^2 drives alpha_1 at large XI2?  (K_B = 1/5, J_Y = 1, c2 = c4 = 0)"); P("="*76)
kbv, jyv = R(1,5), 1
PIECES = {"full": (1, 1, 1), "chi-chi only": (1, 0, 0), "chi-metric cross only": (0, 1, 0), "metric/aether only": (0, 0, 1), "chi-chi + cross": (1, 1, 0)}
RES = {}
P(f"  {'piece':24s} {'XI2':>8s} {'alpha_1':>14s} {'drag piece':>12s} {'gamma':>6s} {'alpha_3':>8s}")
for nm, (xa, xb, xc) in PIECES.items():
    for xi2 in (0, 1, 100, 10**4):
        r = ladder({KB: kbv, K2: sp.S(10), JY: sp.S(jyv), Q0: q, C2: 0, C4: 0, XI2: sp.S(xi2), XA: xa, XB: xb, XC: xc})
        if not isinstance(r, dict): P(f"  {nm:24s} {xi2:8.0e}: {r}"); continue
        a1v = a1_q0(r); drag = sp.nsimplify(a1v + 4*kbv)
        a3v = sp.nsimplify(sp.limit(r['a3'], q, 0)) if (r['a3'] != 'SING2' and r['a3'].has(q)) else r['a3']
        RES[(nm, xi2)] = dict(a1=a1v, drag=drag, g=r['g'], a3=a3v)
        P(f"  {nm:24s} {xi2:8.0e} {float(a1v):14.6e} {float(drag):12.4e} {str(r['g']):>6s} {str(a3v):>8s}")
P(f"  ({time.time()-T0:.0f}s)")
chi_only_big = RES[("chi-chi only", 10**4)]['drag']; metric_big = RES[("metric/aether only", 10**4)]['drag']; cross_big = RES[("chi-metric cross only", 10**4)]['drag']
check("D1 the pure chi-chi stiffening alone SUPPRESSES the drag piece (|drag| at XI2 = 1e4 below 1e-2 of its XI2 = 0 value)",
      abs(float(chi_only_big)) < 1e-2*abs(float(RES[("chi-chi only", 0)]['drag'])), f"chi-chi only: drag {float(RES[('chi-chi only', 0)]['drag']):+.3f} -> {float(chi_only_big):+.3e}")
check("D2 the growth ~ +(2 - K_B J_Y) XI2 comes from the pieces the operator generates by acting on the scalar's BACKGROUND gradient "
      "(the chi-metric cross and/or metric/aether-only terms), not from the stiffening",
      abs(float(metric_big) + float(cross_big)) > 0.5*abs(float(RES[("full", 10**4)]['drag'])), f"cross {float(cross_big):+.3e}, metric-only {float(metric_big):+.3e}, full {float(RES[('full', 10**4)]['drag']):+.3e}")
# alpha_2 at finite q for the chi-chi-only piece (the pipeline's alpha_2 diverges as q -> 0 in every variant: the v9 'novel channel')
P(""); P("alpha_2 at finite q (q = 1/10, 1/100), chi-chi-only piece and full, XI2 = 0 and 1e4:")
for nm in ("chi-chi only", "full"):
    xa, xb, xc = PIECES[nm]
    for xi2 in (0, 10**4):
        for qv in (R(1,10), R(1,100)):
            r = ladder({KB: kbv, K2: sp.S(10), JY: sp.S(jyv), Q0: qv, C2: 0, C4: 0, XI2: sp.S(xi2), XA: xa, XB: xb, XC: xc})
            if isinstance(r, dict) and r['a2'] != 'SING2':
                P(f"  {nm:14s} XI2={xi2:6.0e} q={str(qv):6s}: alpha_1 = {float(r['a1']):+.4e}, alpha_2 = {float(r['a2']):+.4e}, alpha_3 = {float(r['a3']):+.2e}")
            else: P(f"  {nm:14s} XI2={xi2:6.0e} q={str(qv):6s}: {r if not isinstance(r, dict) else r['a2']}")
P(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL")
sys.exit(1 if FAILS else 0)
