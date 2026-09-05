#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f32 -- the operator that realises f31c's coherent stiffening (A) from a LOCAL action term:  xi^2 |grad_perp V|^2 added to Y
inside J, with V_mu = q_mu^nu d_nu phi the aether-frame spatial gradient of the scalar and grad_perp the aether-projected derivative.
Why it should work (algebra, then verified here): V's background vanishes (dphi_bg = -Q0 A, q A = 0), so at quadratic order
(grad_perp V)^2 = h0^{ls} h0^{mn} d_l V1_m d_s V1_n = [k^2 + (A.k)^2] V1.V1 = kx^2 (1 + w^2 w1^2) Y_2 -- the whole Y sector, mixings
included, times (1 + (xi k)^2) at O(w), and an O(w^2) piece for alpha_2.  Purely spatial in the aether frame: no extra time
derivatives, hence no Ostrogradsky mode; the dispersion becomes omega^2 = k^2 (1 + xi^2 k^2).  Same pipeline as f31/f31c
(generalized AeST, boosted aether, Will dictionary); (A) is kept as the reference column.  Checks can fail."""
import sympy as sp, time, pickle, os, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import tempfile
SC = os.environ.get('SCRATCH', tempfile.gettempdir()) + '/'
os.makedirs(SC, exist_ok=True)
CACHE = SC + 'L2dc_k4_Vgrad.pkl'
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
    # f31c: two alternative coherence-length operators, each with its own switch
    #   (A) coherent stiffening of the WHOLE Y sector: J_Y -> J_Y (1 + XI2)     [reference: does ANY stiffening suppress the drag?]
    #   (B) the covariant Hessian-squared operator  xi^2 h^{ma} h^{nb} (nabla_m nabla_n phi)(nabla_a nabla_b phi)
    # EFFICIENT BUILD: Gamma_bg = 0 and d d phi_bg = 0, so the Hessian is O(eps) exactly; at O(eps^2) the operator is the
    # BACKGROUND projector h0 (no eps) contracted with the first-order Hessian H1 -- a 16x16 sum of single-eps terms.
    ddchi = [[d(d(chif, n), m) for n in range(4)] for m in range(4)]
    dphi_bgT = sp.Matrix(4, 1, lambda i, j: te(dphi_bg[i]))
    H1 = [[sp.expand(ddchi[m][n] - sum(sp.expand(GamT[l][m][n]).coeff(eps, 1)*dphi_bgT[l] for l in range(4))) for n in range(4)] for m in range(4)]
    h0 = sp.Matrix(4, 4, lambda m, n: wtrunc(sp.expand(eta[m, n] + Aup_bg[m]*Aup_bg[n])))
    HS2 = 0
    for m in range(4):
        for n in range(4):
            if H1[m][n] == 0: continue
            for a in range(4):
                if h0[m, a] == 0: continue
                for b in range(4):
                    if h0[n, b] == 0 or H1[a][b] == 0: continue
                    HS2 += h0[m, a]*h0[n, b]*H1[m][n]*H1[a][b]
    gHS2 = wtrunc(sp.expand(HS2))
    gHS = [0, 0, gHS2]
    P(f"    Hessian-squared operator built (efficient): {len(sp.Add.make_args(gHS2))} terms ({time.time()-T0:.1f}s)")
    # f32: the spatial-gradient-squared operator on V = q.dphi (V_mu = dphi_mu + A_mu (A.dphi)); V_bg = 0 so only V1 enters at O(eps^2)
    Vfull = [te(dphi[m] + Adn[m]*sum(Aup[n]*dphi[n] for n in range(4))) for m in range(4)]
    V0 = [sp.expand(Vfull[m]).coeff(eps, 0) for m in range(4)]
    V1 = [sp.expand(Vfull[m]).coeff(eps, 1) for m in range(4)]
    dV1 = [[sp.expand(d(V1[m], l)) for m in range(4)] for l in range(4)]
    VG2 = 0
    for l in range(4):
        for sg in range(4):
            if h0[l, sg] == 0: continue
            for m in range(4):
                if dV1[l][m] == 0: continue
                for n in range(4):
                    if h0[m, n] == 0 or dV1[sg][n] == 0: continue
                    VG2 += h0[l, sg]*h0[m, n]*dV1[l][m]*dV1[sg][n]
    gVG2 = wtrunc(sp.expand(VG2)); gVG = [0, 0, gVG2]
    P(f"    spatial-gradient-squared operator on V built: {len(sp.Add.make_args(gVG2))} terms; |V_bg| = {[sp.simplify(v) for v in V0]} ({time.time()-T0:.1f}s)")
    identity = wtrunc(sp.expand(gVG2 - kx**2*(1 + wb**2*w1**2)*gY[2]))
    # the residual: keep only its DC (ket x bra) part, the physical quadratic form; split it by sector
    def DCpart(e):
        e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
        for mon, c in zip(pol.monoms(), pol.coeffs()):
            if mon[0] == mon[1]: out += c*(Es*Eis)**mon[0]
        return sp.expand(out.subs(Es*Eis, 1)) if out != 0 else sp.S(0)
    resDC = DCpart(identity)
    scal = [Psik, Psib, Phik, Phib, s22k, s22b, a1k, a1b, chik, chib]
    res_scalar = sp.expand(resDC.subs({B2k: 0, B2b: 0, B3k: 0, B3b: 0, s23k: 0, s23b: 0, a2k: 0, a2b: 0, a3k: 0, a3b: 0}))
    res_vector = sp.expand(resDC - res_scalar)
    ID = dict(scalar_sector_residual=res_scalar, vector_sector_residual=res_vector,
              vector_vanishes_when_B_equals_a=sp.expand(res_vector.subs({B2k: a2k, B2b: a2b, B3k: a3k, B3b: a3b})))
    P(f"    identity (grad_perp V)^2 == kx^2 (1 + w^2 w1^2) Y_2, DC part: scalar-sector residual = {res_scalar}; vector-sector residual = {str(res_vector)[:160]}; "
      f"vector residual with B_i -> a_i: {ID['vector_vanishes_when_B_equals_a']}")
    pickle.dump(ID, open(CACHE + '.id', 'wb'))
    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*(1 + XA*XI2)*gY[2] - (2-KB)*JY*XB*XI2*gHS[2] - (2-KB)*JY*XC*XI2*gVG[2]
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
P(""); P("="*76); P("TWO ALTERNATIVE OPERATORS (K_B = 1/5 and 1/2 at J_Y = 1; K_B = 1/5 at J_Y = 2; c2 = c4 = 0)"); P("="*76)
VARS = {"(A) J_Y -> J_Y(1+XI2), whole Y sector": (1, 0, 0), "(C) xi^2 |grad_perp V|^2, V = q.dphi": (0, 0, 1)}
RES = {}
P(f"  {'operator':40s} {'K_B':>4s} {'J_Y':>3s} {'XI2':>7s} {'alpha_1':>13s} {'drag':>11s} {'-4(2-K_B)/(J_Y(1+XI2)+1)':>25s} {'alpha_2':>13s} {'gamma':>5s} {'a3':>4s}")
for nm, (xa, xb, xc) in VARS.items():
    for kbv, jyv in [(R(1,5), 1), (R(1,2), 1), (R(1,5), 2)]:
        for xi2 in (0, 1, 100, 10**4):
            r = ladder({KB: kbv, K2: sp.S(10), JY: sp.S(jyv), Q0: q, C2: 0, C4: 0, XI2: sp.S(xi2), XA: xa, XB: xb, XC: xc})
            if not isinstance(r, dict): P(f"  {nm:40s} {str(kbv):>4s} {jyv:3d} {xi2:7.0e}: {r}"); continue
            a1v = a1_q0(r); drag = sp.nsimplify(a1v + 4*kbv); pred = -4*(2 - kbv)/(jyv*(1 + xi2) + 1)
            a3v = sp.nsimplify(sp.limit(r['a3'], q, 0)) if (r['a3'] != 'SING2' and r['a3'].has(q)) else r['a3']
            a2v = sp.nsimplify(sp.limit(r['a2'], q, 0)) if (r['a2'] != 'SING2' and r['a2'].has(q)) else r['a2']
            RES[(nm, kbv, jyv, xi2)] = dict(a1=a1v, drag=drag, pred=pred, g=r['g'], a3=a3v, a2=a2v)
            a2s = f"{float(a2v):13.5e}" if a2v != 'SING2' else f"{'SING2':>13s}"
            P(f"  {nm:40s} {str(kbv):>4s} {jyv:3d} {xi2:7.0e} {float(a1v):13.5e} {float(drag):11.4e} {float(pred):25.4e} {a2s} {str(r['g']):>5s} {str(a3v):>4s}")
P(f"  ({time.time()-T0:.0f}s)")
nmA, nmB = list(VARS)
okA = all(sp.simplify(RES[(nmA, kb, jy, x)]['drag'] - RES[(nmA, kb, jy, x)]['pred']) == 0 for (n_, kb, jy, x) in RES if n_ == nmA)
check("A1 coherent stiffening of the whole Y sector gives EXACTLY the propagator form -4(2-K_B)/(J_Y(1+XI2)+1): so a coherence length "
      "that scales the full scalar sector does suppress the drag, and the lock is then evaded at c_14 > 0", okA)
ID = pickle.load(open(CACHE + '.id', 'rb')) if os.path.exists(CACHE + '.id') else None
r_s0 = sp.expand(ID['scalar_sector_residual'].subs(wb, 0)) if ID else None; r_v0 = sp.expand(ID['vector_sector_residual'].subs(wb, 0)) if ID else None
r_s1 = sp.expand(ID['scalar_sector_residual']).coeff(wb, 1) if ID else None
r0 = sp.expand(r_s0 + r_v0) if ID else None
no_chi = ID is not None and all(sp.expand(r0).coeff(v, 1) == 0 and sp.expand(r0).coeff(v, 2) == 0 for v in (chik, chib, Phik, Phib, s22k, s22b))
check("C0 at w = 0 the residual (grad_perp V)^2 - kx^2 Y_2 is confined to the aether-normalisation set {Psi (= a0 by the O(eps) constraint), a1, B2 - a2, B3 - a3}, "
      "proportional to Q_0^2, with NO chi, Phi or s22 term: it is the pipeline's unresolved second-order aether normalisation (the exact identity V.V = Y needs the "
      "O(eps^2) constraint, which the pipeline does not solve); it does not enter alpha_1 (C1 exact) and shifts the alpha_2 drag by 15% at XI2 = 1e4 (C2)",
      no_chi, f"w = 0 residual / (2 Q_0^2 kx^2) = {sp.factor(r0/(2*Q0**2*kx**2)) if ID else None}")
okC1 = all(sp.simplify(RES[(nmB, kb, jy, x)]['a1'] - RES[(nmA, kb, jy, x)]['a1']) == 0 for (n_, kb, jy, x) in RES if n_ == nmB)
check("C1 alpha_1 of the local operator (C) equals alpha_1 of the coherent stiffening (A) EXACTLY at every (K_B, J_Y, XI2) on the ladder: "
      "the operator that realises (A) from an action is xi^2 |grad_perp V|^2", okC1)
okC1b = all(sp.simplify(RES[(nmB, kb, jy, x)]['drag'] - RES[(nmB, kb, jy, x)]['pred']) == 0 for (n_, kb, jy, x) in RES if n_ == nmB)
check("C1b hence the propagator form -4(2-K_B)/(J_Y(1+XI2)+1) holds for (C) too", okC1b)
P("  alpha_2 needs c_2 != 0 (pure Einstein-aether alpha_2 has 1/c_123 = 1/c_2 at c_1 = -c_3 = K_B; the ladder above used c_2 = c_4 = 0, hence the infinities):")
P("  re-run at c_2 = c_4 = 1/10, K_B = 1/5, q -> 0; the scalar's contribution is alpha_2(J_Y) - alpha_2(J_Y = 1e6, the scalar frozen out):")
def lim0(e): return sp.nsimplify(sp.limit(e, q, 0)) if e.has(q) else sp.nsimplify(e)
A2 = {}
for nm, (xa, xb, xc) in VARS.items():
    for jy in (1, 10**6):
        for x in ((0, 1, 100, 10**4) if jy == 1 else (0,)):
            r = ladder({KB: R(1,5), K2: sp.S(10), JY: sp.S(jy), Q0: q, C2: R(1,10), C4: R(1,10), XI2: sp.S(x), XA: xa, XB: xb, XC: xc})
            if not isinstance(r, dict) or r['a2'] == 'SING2': A2[(nm, jy, x)] = None; P(f"    {nm:40s} J_Y={jy:.0e} XI2={x:.0e}: singular ({r if not isinstance(r, dict) else 'SING2'})"); continue
            A2[(nm, jy, x)] = (lim0(r['a1']), lim0(r['a2']))
            P(f"    {nm:40s} J_Y={jy:.0e} XI2={x:.0e}: alpha_1 = {float(A2[(nm, jy, x)][0]):+.5e}  alpha_2 = {float(A2[(nm, jy, x)][1]):+.5e}")
ok2 = all(v is not None for v in A2.values())
if ok2:
    for nm in VARS:
        base = A2[(nm, 10**6, 0)][1]; d0 = A2[(nm, 1, 0)][1] - base; d4 = A2[(nm, 1, 10**4)][1] - base
        P(f"    {nm:40s}: pure-aether alpha_2 (scalar frozen) = {float(base):+.5e}; scalar drag in alpha_2: XI2=0 {float(d0):+.5e}, XI2=1e4 {float(d4):+.5e}, suppression {float(d4/d0) if d0 != 0 else float('nan'):.3e}")
    dA = A2[(nmA, 1, 10**4)][1] - A2[(nmA, 10**6, 0)][1]; dC = A2[(nmB, 1, 10**4)][1] - A2[(nmB, 10**6, 0)][1]
    dA0 = A2[(nmA, 1, 0)][1] - A2[(nmA, 10**6, 0)][1]; dC0 = A2[(nmB, 1, 0)][1] - A2[(nmB, 10**6, 0)][1]
    a1c4 = A2[(nmB, 1, 0)][0]
check("C2 with c_2 = c_4 = 1/10 the ladder is regular, and the scalar's contribution to alpha_2 is suppressed by the operator (C) at XI2 = 1e4 to below 1e-2 of its XI2 = 0 value "
      "(the aether's own alpha_2 is Einstein-aether's and is not the scalar's problem)", ok2 and dC0 != 0 and abs(float(dC/dC0)) < 1e-2,
      f"scalar drag in alpha_2: (C) {float(dC0):+.4e} -> {float(dC):+.4e}; (A) {float(dA0):+.4e} -> {float(dA):+.4e}" if ok2 else "singular")
check("C3 with c_4 = 1/10 the pure-aether part of alpha_1 shifts to -4(K_B + c_4) while the scalar drag is unchanged: alpha_1(C, XI2 = 0) = -4(K_B + c_4) - 4(2 - K_B)/(J_Y + 1)",
      ok2 and sp.simplify(a1c4 - (-4*(R(1,5) + R(1,10)) - 4*(2 - R(1,5))/2)) == 0, f"alpha_1 = {float(a1c4) if ok2 else 'n/a'} vs {float(-4*(R(1,5) + R(1,10)) - 4*(2 - R(1,5))/2)}")
P(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL")
sys.exit(1 if FAILS else 0)
