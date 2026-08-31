#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_unitary_gauge_build.py  (ANCHOR iv: second-gauge / second-structure alpha_2)
================================================================================
Rebuild of the base-AeST boosted quadratic action in the UNITARY gauge
    chi = 0 (scalar fluctuation gauged away via xi^0, legitimate at Q0 != 0),
    h12 = h13 = 0, s11 = 0,   h01 = B1 RETAINED as a field
(the route2_v2 gauge was h01=h12=h13=0, s11=0 with chi live). Same action,
background, plane wave k=xhat, wb-ladder, and certified Will dictionary.
Two INDEPENDENT alpha_2 extractions in this gauge:
  [g00]  alpha_2 = (Cpar - Cperp)/2
  [g0i]  parallel channel h01 at O(wb):
         with w_Will = -wb*w (certified orientation),
         coeff(h01^(1), w1)/Rk/U_amp = -(-alpha_1/2 + 2 alpha_2)
Agreement of BOTH with each other and with the route2_v2-gauge closed forms
  alpha_1 = -4(2+K_B J_Y)/(1+J_Y)   (q->0)
  alpha_2(J_Y=1,q->0) = [K2(KB^2-4KB-4) - KB^4+8KB^3-4KB^2-32KB+32]/(KB-2)^3
is the anchor-iv two-gauge/two-setup certification. Also compares the FULL
alpha_2(q) rational function between gauges (identical-function check).
"""
import sympy as sp, time, pickle, os
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = None
root = '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula'
for s in os.listdir(root):
    cand = os.path.join(root, s, 'scratchpad')
    if os.path.isdir(cand):
        SC = cand + '/'
t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT, LAM = sp.symbols('G_t Lambda', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
ww = w1**2 + w2**2 + w3**2; S0 = 1 + wb**2*ww/2
Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, wb*w3]); Adn_bg = eta*Aup_bg
dphi_bg = -Q0*Adn_bg
Es, Eis = sp.symbols('E_s E_is'); kx = sp.symbols('k_x', real=True)
kv = [0, kx, 0, 0]
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
B1f, B1k, B1b = nf('B1')
B2f, B2k, B2b = nf('B2'); B3f, B3k, B3b = nf('B3')
s22, s22k, s22b = nf('s22'); s23, s23k, s23b = nf('s23')
a1f, a1k, a1b = nf('a1'); a2f, a2k, a2b = nf('a2'); a3f, a3k, a3b = nf('a3')
rho, Rk, Rb = nf('rho'); a0f, a0k, a0b = nf('a0p')
H = sp.zeros(4, 4)
H[0, 0] = -2*Psi
H[0, 1] = B1f; H[1, 0] = B1f
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
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f,
                 Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
C1 = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
solA = sp.solve([sp.expand(C1).coeff(Es, 1), sp.expand(C1).coeff(Eis, 1)],
                [a0k, a0b], dict=True)[0]
solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
a0f = a0f.subs(solA)
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f,
                 Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
P(f"[S1] constraint solved ({time.time()-T0:.1f}s)")
dphi = sp.Matrix([dphi_bg[m] for m in range(4)])       # chi = 0 (unitary)
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
AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s))
        for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m)-d(Adn[m], n)))
F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b]
                for m in range(4) for n in range(4)
                for a in range(4) for b in range(4))
Jup = [te(sum(AupT[nu]*(d(AupT[al], nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4)))
       for nu in range(4))) for al in range(4)]
Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
Yc = te(sum((guT[m, n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n]
            for m in range(4) for n in range(4)))
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
gsq = grade(sqg); gR = grade(Rsc)
gS = [gR[n] - (2*LAM if n == 0 else 0) - (KB/2)*gF2[n] + 2*(2-KB)*gJ[n]
      - (2-KB)*gY[n] - gK[n] for n in range(3)]
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
pickle.dump(L2dc, open(SC+'L2dc_unitary.pkl', 'wb'))
P(f"    L2dc built+cached: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")

# ---- solve ladder ----
q = sp.Symbol('q', positive=True)
KETS = [Psik, Phik, B1k, B2k, B3k, s22k, s23k, a1k, a2k, a3k]
BRAS = [Psib, Phib, B1b, B2b, B3b, s22b, s23b, a1b, a2b, a3b]
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
def solve(kbv, k2v, jyv, qval):
    sub = {KB: sp.nsimplify(kbv), K2: sp.nsimplify(k2v), JY: sp.nsimplify(jyv),
           Q0: qval, GT: 1, LAM: 0, kx: 1}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B1k: 0, B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat = [Psib, Phib, s22b, a1b]
    eq0 = [sp.expand(eqf[b].coeff(wb, 0).subs(VZ)) for b in stat]
    s0s = lin(eq0, [Psik, Phik, s22k, a1k])
    if s0s is None: return None
    s0 = {**s0s, B1k: sp.S(0), B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0),
          a2k: sp.S(0), a3k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk)
    gamma = sp.cancel(s0[Phik]/s0[Psik])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return ('SING1', U_amp, gamma)
    c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)
    # parallel g0i channel: coeff(h01^(1), w1) = -(-alpha_1/2 + 2 alpha_2)*U_amp
    C01 = sp.cancel(sp.expand(dk1[B1k].subs(s1)).coeff(w1)/Rk/U_amp)
    alpha2_g0i = sp.cancel((alpha1/2 - C01)/2)
    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS],
             list(dk2.values()))
    if s2 is None: return (alpha1, alpha2_g0i, 'SING2', U_amp, gamma)
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    alpha2_g00 = sp.cancel((Cpar - Cperp)/2)
    alpha3 = sp.cancel(Cperp + alpha1)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2_g0i=alpha2_g0i,
                a2_g00=alpha2_g00, a3=alpha3)

a2form = ((K2*(KB**2 - 4*KB - 4) - KB**4 + 8*KB**3 - 4*KB**2 - 32*KB + 32)
          / (KB - 2)**3)
P("")
P("="*74)
P("UNITARY-GAUGE runs (q symbolic; PPN = q->0 finite part)")
P("="*74)
for kbv, k2v, jyv in [(sp.Rational(1, 5), 10, 1), (sp.Rational(3, 10), 7, 1),
                      (sp.Rational(1, 5), 10, 2)]:
    r = solve(kbv, k2v, jyv, q)
    if not isinstance(r, dict):
        P(f"  KB={kbv} K2={k2v} JY={jyv}: {r[0] if isinstance(r,tuple) else r}")
        continue
    a1_0 = sp.limit(r['a1'], q, 0)
    pred_a1 = sp.nsimplify(-4*(2+sp.nsimplify(kbv)*jyv)/(1+jyv))
    # g0i-channel alpha_2: Laurent finite part
    cm2_i = sp.limit(r['a2_g0i']*q**2, q, 0)
    c0_i = sp.limit(sp.cancel(r['a2_g0i'] - cm2_i/q**2), q, 0)
    cm2_0 = sp.limit(r['a2_g00']*q**2, q, 0)
    c0_0 = sp.limit(sp.cancel(r['a2_g00'] - cm2_0/q**2), q, 0)
    same_fn = sp.simplify(sp.together(r['a2_g0i'] - r['a2_g00'])) == 0
    P(f"  KB={kbv} K2={k2v} JY={jyv}:")
    P(f"    gamma={sp.simplify(r['g'])}  alpha_3=={sp.simplify(r['a3'])}")
    P(f"    alpha_1(q->0)={a1_0}  pred={pred_a1}  ok={sp.simplify(a1_0-pred_a1)==0}")
    P(f"    alpha_2[g00 ] c_-2={sp.nsimplify(cm2_0)} c_0={sp.nsimplify(c0_0)}")
    P(f"    alpha_2[g0i ] c_-2={sp.nsimplify(cm2_i)} c_0={sp.nsimplify(c0_i)}")
    P(f"    two-structure agreement (identical alpha_2(q) fns): {same_fn}")
    if jyv == 1:
        pred_a2 = sp.nsimplify(a2form.subs({KB: sp.nsimplify(kbv), K2: sp.nsimplify(k2v)}))
        P(f"    closed-form alpha_2(J_Y=1) pred={pred_a2} : g00-match="
          f"{sp.simplify(c0_0-pred_a2)==0} g0i-match={sp.simplify(c0_i-pred_a2)==0}")
P(f"done ({time.time()-T0:.1f}s)")
