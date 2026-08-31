#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_pure_ea_control_build.py  (pipeline+dictionary CONTROL for the eta_K solve)
===============================================================================
Runs the EXACT route2_v2 pipeline (same metric ansatz, same gauge h01=h12=h13=0
s11=0, same unit-norm constraint elimination, same Ricci/tadpole bookkeeping,
same static wb-ladder) on PURE EINSTEIN-AETHER with generic c1..c4:
    L = R - c1 D_aA^m D^aA_m - c2 (D_aA^a)^2 - c3 D_aA^m D_mA^a + c4 a.a
      - lam(A^2+1) + matter,
aether background boosted A^mu = (1 + wb^2 w.w/2, wb w^i), source at rest.
It must reproduce the Foster-Jacobson (gr-qc/0509083) closed forms
    alpha_1 = -8(c3^2 + c1 c4)/(2c1 - c1^2 + c3^2)
    alpha_2 = alpha_1/2 - (c1+2c3-c4)(2c1+3c2+c3+c4)/(c123(2-c14))
and G_N = G/(1 - c14/2), alpha_3 = 0, using the Will dictionary certified in
wf3_will_dictionary_certificate.py. Whichever w-orientation (w_Will = -wb w,
the physical one, vs +wb w) matches FJ alpha_1 with alpha_3 = 0 is thereby
CERTIFIED and is the one wf3_base_aest_eta_K_solve.py uses.
Also verifies in-pipeline that (c1,c3)=(K_B,-K_B), c2=c4=0 equals the
-(K_B/2)F^2 Maxwell form (the AeST aether sector), tying the control to the
cached base-AeST L2 (L2dc_v2.pkl).
"""
import sympy as sp, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
C1s, C2s, C3s, C4s = sp.symbols('c1 c2 c3 c4', real=True)
KB = sp.Symbol('K_B', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT = sp.Symbol('G_t', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
ww = w1**2 + w2**2 + w3**2; S0 = 1 + wb**2*ww/2
Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, wb*w3]); Adn_bg = eta*Aup_bg
Es, Eis = sp.symbols('E_s E_is'); kx = sp.symbols('k_x', real=True)
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
rho, Rk, Rb = nf('rho'); a0f, a0k, a0b = nf('a0p')
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
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f,
                 Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
C1c = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
solA = sp.solve([sp.expand(C1c).coeff(Es, 1), sp.expand(C1c).coeff(Eis, 1)],
                [a0k, a0b], dict=True)[0]
solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
a0f = a0f.subs(solA)
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f,
                 Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
P(f"[S1] constraint solved ({time.time()-T0:.1f}s)")
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
Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s))
        for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
# covariant derivative D_a A^m  (a = partial index)
DA = [[te(d(AupT[m], a) + sum(GamT[m][a][r]*AupT[r] for r in range(4)))
       for m in range(4)] for a in range(4)]
P(f"    DA built ({time.time()-T0:.1f}s)")
term1 = te(sum(guT[a, b]*gdT[m, n]*DA[a][m]*DA[b][n]
               for a in range(4) for b in range(4)
               for m in range(4) for n in range(4)))
P(f"    term1 ({time.time()-T0:.1f}s)")
term2 = te(sum(DA[a][a] for a in range(4))**2)
term3 = te(sum(DA[a][m]*DA[m][a] for a in range(4) for m in range(4)))
acc = [te(sum(AupT[a]*DA[a][m] for a in range(4))) for m in range(4)]
term4 = te(sum(gdT[m, n]*acc[m]*acc[n] for m in range(4) for n in range(4)))
P(f"    terms 2-4 ({time.time()-T0:.1f}s)")
L_EA = -C1s*term1 - C2s*term2 - C3s*term3 + C4s*term4
# in-pipeline Maxwell tie-in: c1=K_B,c3=-K_B,c2=c4=0  ==  -(K_B/2) F^2
Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m)-d(Adn[m], n)))
F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b]
                for m in range(4) for n in range(4)
                for a in range(4) for b in range(4))
tie = sp.expand(te(L_EA.subs({C1s: KB, C3s: -KB, C2s: 0, C4s: 0})
                   + (KB/2)*F2))
tie2 = sp.expand(sum(tie.coeff(eps, 2).coeff(wb, j)*wb**j for j in range(3)))
P("MAXWELL TIE-IN: [L_EA(c1=KB,c3=-KB,c2=c4=0) + (KB/2)F^2] at O(eps^2) =",
  sp.simplify(tie2))
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
gEA = grade(L_EA); gsq = grade(sqg); gR = grade(Rsc)
gS = [gR[n] + gEA[n] for n in range(3)]
L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3)))
L2_matt = -16*sp.pi*GT*wtrunc(rho*(-H[0, 0]/2))
L2 = sp.expand(L2_grav + L2_matt)
def DC(e):
    e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
    for mon, c in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            out += c*(Es*Eis)**mon[0]
    return out.subs(Es*Eis, 1) if out != 0 else out
L2dc = DC(L2)
P(f"    L2dc built: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")

# ---- solve ladder (identical to route2_v2) ----
KETS = [Psik, Phik, B2k, B3k, s22k, s23k, a1k, a2k, a3k]
BRAS = [Psib, Phib, B2b, B3b, s22b, s23b, a1b, a2b, a3b]
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin_solve(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk); s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
def run(cs):
    sub = {C1s: sp.nsimplify(cs[0]), C2s: sp.nsimplify(cs[1]),
           C3s: sp.nsimplify(cs[2]), C4s: sp.nsimplify(cs[3]), GT: 1, kx: 1}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    eq0 = [sp.expand(eqf[b].coeff(wb, 0).subs(VZ)) for b in [Psib, Phib, s22b, a1b]]
    s0s = lin_solve(eq0, [Psik, Phik, s22k, a1k])
    if s0s is None: return None
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0), a2k: sp.S(0), a3k: sp.S(0)}
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin_solve([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return (s0, None, None, dk1, dk2)
    eq2 = [sp.expand(eqW[A].coeff(wb, 2)).subs(s1) for A in BRAS]
    s2 = lin_solve(eq2, list(dk2.values()))
    return (s0, s1, s2, dk1, dk2)

# FJ closed forms
def FJ(cs):
    c1, c2, c3, c4 = [sp.nsimplify(v) for v in cs]
    c14 = c1 + c4; c123 = c1 + c2 + c3
    A1 = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
    A2 = A1/2 - (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)/(c123*(2 - c14))
    GN = 1/(1 - c14/2)
    return sp.simplify(A1), sp.simplify(A2), sp.simplify(GN)

print()
P("="*74)
P("CONTROL RUNS: pipeline (Will dictionary, both w-orientations) vs FJ")
P("="*74)
for cs in [(sp.Rational(3, 10), sp.Rational(1, 5), sp.Rational(1, 10), sp.Rational(1, 20)),
           (sp.Rational(1, 5), sp.Rational(2, 5), sp.Rational(-1, 10), sp.Rational(1, 10)),
           (sp.Rational(1, 5), 0, sp.Rational(-1, 5), 0)]:   # last = Maxwell pt (alpha_2 singular, alpha_1 only)
    res = run(cs)
    s0, s1, s2, dk1, dk2 = res
    U_amp = sp.cancel(-s0[Psik]/Rk)            # h00 = -2 Psi = 2U => U = -Psi
    fjA1, fjA2, fjGN = FJ(cs)
    P(f"\n  c = {tuple(map(str,cs))}")
    P(f"    Newton U/(rho) = {sp.nsimplify(U_amp)}  vs FJ 4*pi*G_N = {sp.nsimplify(4*sp.pi*fjGN)}"
      f"   match={sp.simplify(U_amp - 4*sp.pi*fjGN)==0}")
    P(f"    gamma_PPN = {sp.simplify(s0[Phik]/s0[Psik])}")
    if s1 is None:
        P("    O(wb) solve SINGULAR"); continue
    c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)  # transverse g02 coeff
    a1_plus  = sp.simplify(-2*c2t/U_amp)   # orientation w_Will = +wb*w
    a1_minus = sp.simplify(+2*c2t/U_amp)   # orientation w_Will = -wb*w
    P(f"    alpha_1(+w) = {a1_plus} ; alpha_1(-w) = {a1_minus} ; FJ = {fjA1}"
      f"  -> match(+w)={sp.simplify(a1_plus-fjA1)==0} match(-w)={sp.simplify(a1_minus-fjA1)==0}")
    if s2 is None:
        P("    O(wb^2) solve SINGULAR (expected at Maxwell point: c123=0)"); continue
    h2 = sp.cancel(-2*sp.expand(dk2[Psik].subs(s2)))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    alpha2 = sp.simplify((Cpar - Cperp)/2)
    P(f"    alpha_2 = {alpha2} ; FJ = {fjA2}  -> match={sp.simplify(alpha2-fjA2)==0}")
    for lab, a1v in (('+w', a1_plus), ('-w', a1_minus)):
        P(f"    alpha_3 check ({lab}): perp + alpha_1 = {sp.simplify(Cperp + a1v)}")
P(f"\ndone ({time.time()-T0:.1f}s)")
