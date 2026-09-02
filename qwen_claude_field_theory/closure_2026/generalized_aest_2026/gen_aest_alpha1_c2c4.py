#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gen_aest_alpha1_c2c4.py -- GATE 4 of the generalized completion, by hand.
=========================================================================
Question: AeST's aether sector is Maxwell-only (c1=-c3=K_B, c2=c4=0). Restore the two
omitted Einstein-aether couplings
      + c2 (D_a A^a)^2   and   + c4 a_mu a^mu      (a^mu = A^nu D_nu A^mu, tensor-blind)
and recompute the preferred-frame PPN parameter alpha_1 WITH the AeST scalar drag
2(2-K_B) a.grad(phi) included, at the physical deep field J_Y = mu(u0) = 1.
Banked at c2=c4=0 (V9_PPN_KILL_VERDICT.md):  alpha_1 = -4 eta_K,
      eta_K = (K_B J_Y + 2)/(J_Y + 1)  ->  alpha_1 = -2(K_B+2) at J_Y=1 (KILL, un-tunable).
Does c4 (which changes the aether's inertia under a boost) move the K_B-independent "+2"?

Pipeline = the FJ-controlled route2_v2 pipeline (aest_j10/wf3_*): same metric ansatz,
gauge h01=h12=h13=0, s11=0, chi LIVE, unit-norm constraint eliminated, boosted aether
background A^mu = (1 + wb^2 w.w/2, wb w^i), source at rest, plane wave k = xhat, static
wb-ladder, certified Will dictionary: alpha_1 = +2*coeff(g02, w2)/U_amp.
The Maxwell part -(K_B/2)F^2 is the in-pipeline-certified c1=-c3=K_B combination; only the
c2 and c4 operators are added, built from the same Christoffels/acceleration the drag uses.

ANCHORS (checks that can fail):
  A. c2=c4=0 reproduces the banked alpha_1 = -4(2+K_B J_Y)/(1+J_Y) on the wf3 grid.
  B. pure-EA limit (scalar frozen: J_Y->oo, Q0->0) reproduces Foster-Jacobson at c13=0:
     alpha_1 = -4 c14 = -4(K_B + c4)  [FJ: -8(c3^2+c1c4)/(2c1-c1^2+c3^2) at c3=-c1].
  C. gamma_PPN = 1 and alpha_3 == 0 throughout (semiconservative).
MAIN: alpha_1(K_B, c2, c4, J_Y) closed form; c2-dependence; the alpha_1=0 locus at J_Y=1;
      and what eta_K looks like there (health is decided by the companion dispersion script).
"""
import sympy as sp, time, pickle, os, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = os.environ.get('SCRATCH', '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/2842cbcf-b95e-45e6-8ed2-7f6c29341e4f/scratchpad') + '/'
os.makedirs(SC, exist_ok=True)
CACHE = SC + 'L2dc_gen_c2c4.pkl'
FAILS = []
def check(name, ok, detail=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ''))
    if not ok: FAILS.append(name)

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
C2, C4 = sp.symbols('c2 c4', real=True)
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
    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*gY[2]
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

P(""); P("="*76); P("ANCHOR A: c2=c4=0 reproduces the banked alpha_1 = -4(2+K_B J_Y)/(1+J_Y)"); P("="*76)
for kbv, k2v, jyv in [(R(1,5),10,1), (R(1,5),10,2), (R(3,10),10,1), (R(1,2),10,1), (R(1,5),50,1)]:
    r = ladder({KB: kbv, K2: sp.S(k2v), JY: sp.S(jyv), Q0: q, C2: 0, C4: 0})
    if not isinstance(r, dict): check(f"A KB={kbv} JY={jyv}: ladder regular", False, str(r)); continue
    a1v = a1_q0(r); pred = sp.nsimplify(-4*(2+kbv*jyv)/(1+jyv))
    check(f"A KB={kbv} K2={k2v} JY={jyv}: alpha_1(q->0)={a1v} == banked {pred}", sp.simplify(a1v-pred)==0)
    check(f"   gamma=1, alpha_3==0", sp.simplify(r['g']-1)==0 and (r['a3']=='SING2' or sp.simplify(r['a3'])==0), f"gamma={sp.simplify(r['g'])} a3={r['a3'] if r['a3']=='SING2' else sp.simplify(r['a3'])}")
P(f"  ({time.time()-T0:.1f}s)")

P(""); P("="*76); P("MAIN: alpha_1(K_B, c2, c4, J_Y) at q->0 with c2, c4 SYMBOLIC"); P("="*76)
forms = {}
for kbv, jyv in [(R(1,5),1), (R(1,10),1), (R(1,4),1), (R(1,5),2), (R(1,5),5)]:
    r = ladder({KB: kbv, K2: sp.S(10), JY: sp.S(jyv), Q0: q})
    if not isinstance(r, dict): P(f"  KB={kbv} JY={jyv}: {r}"); continue
    a1 = sp.factor(a1_q0(r)); forms[(kbv, jyv)] = a1
    P(f"  KB={kbv} JY={jyv}:  alpha_1 = {a1}")
    check(f"   c2-INDEPENDENT (transverse channel)", not a1.has(C2), f"has c2: {a1.has(C2)}")
    check(f"   c4=0 limit == banked", sp.simplify(a1.subs(C4,0) + 4*(2+kbv*jyv)/(1+jyv))==0)
P(f"  ({time.time()-T0:.1f}s)")

P(""); P("="*76); P("CLOSED FORM: fit alpha_1 = -4*(K_B J_Y + A(c4,J_Y) )/(J_Y+1) style; symbolic K_B, J_Y"); P("="*76)
rsym = ladder({K2: sp.S(10), Q0: 0})
if isinstance(rsym, dict):
    a1s = sp.factor(sp.nsimplify(rsym['a1'])); P(f"  alpha_1(K_B,c2,c4,J_Y; q=0) = {a1s}")
    etaK = sp.factor(-a1s/4); P(f"  eta_K = -alpha_1/4 = {etaK}")
    forms['sym'] = a1s
    check("symbolic: c2-independent", not a1s.has(C2))
    check("symbolic: c2=c4=0 -> (K_B J_Y+2)/(J_Y+1)", sp.simplify(etaK.subs({C2:0,C4:0}) - (KB*JY+2)/(JY+1))==0)
    P(""); P("ANCHOR B: pure-EA limit J_Y->oo (scalar frozen) must give FJ alpha_1 = -4 c14 = -4(K_B+c4)")
    lim = sp.simplify(sp.limit(a1s, JY, sp.oo))
    P(f"  lim_{{J_Y->oo}} alpha_1 = {lim}")
    check("B: FJ pure-EA anchor with c4", sp.simplify(lim + 4*(KB+C4))==0)
    P(""); P("THE LOCUS at the physical deep field J_Y=1:")
    a1_J1 = sp.factor(a1s.subs(JY, 1)); P(f"  alpha_1(J_Y=1) = {a1_J1}")
    sol = sp.solve(sp.Eq(a1_J1, 0), C4)
    P(f"  alpha_1 = 0  <=>  c4 = {sol}")
    for kbv in (R(1,20), R(1,10), R(1,5), R(1,4)):
        vals = [sp.nsimplify(s.subs(KB, kbv)) for s in sol]
        P(f"    K_B={kbv}: c4* = {vals}  -> c14* = K_B + c4* = {[sp.nsimplify(kbv+v) for v in vals]}")
    P(f"  eta_K(J_Y=1) = {sp.factor(etaK.subs(JY,1))}   (alpha_1 = 0 <=> eta_K = 0)")
    # how the drag piece scales with c4: separate the K_B-independent part
    piece = sp.factor(sp.simplify(etaK - KB*JY/(JY+1)))
    P(f"  eta_K - K_B J_Y/(J_Y+1) = {piece}   [the 'drag' piece; at c4=0 it is 2/(J_Y+1)]")
else:
    P(f"  symbolic ladder: {rsym}")
pickle.dump({str(k): sp.srepr(v) for k, v in forms.items()}, open(SC+'gen_aest_alpha1_forms.pkl', 'wb'))
P(""); P(f"FAILED CHECKS: {FAILS if FAILS else 'none'}"); P(f"done ({time.time()-T0:.1f}s)")
sys.exit(1 if FAILS else 0)
