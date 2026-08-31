#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_full10_w3zero_build.py  (ADJUDICATOR build, reduced: w3=0 WLOG)
===================================================================
Full UNGAUGED base-AeST boosted quadratic action - no gauge fixing, h01 AND
chi both live - with the boost restricted WLOG to the x1-x2 plane (w3 = 0;
rotational symmetry about k = xhat). The x3-odd fields (B3, H13, H23, a3)
then decouple identically and are dropped: 10 fields
   Psi (h00=-2Psi), B1 (h01), B2 (h02), H11, H22, H33, H12, chi, a1, a2.
This is the covariant target system {E_00,E_0i,E_ij,E_A,E_phi}+A^2=-1 of
v9_alpha2_ppn_status.md restricted to the w3=0 plane, which contains every
structure the Will dictionary needs (w_par=w1, w_perp=w2).
Arbitrates the alpha_2 finite-part discrepancy between the route2_v2 gauge
(lost E_01) and the unitary gauge (lost E_phi). Solver:
wf3_full_ungauged_solve.py adapted (wf3_full10_solve.py).
"""
import sympy as sp, time, pickle, os
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = None
root = '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula'
for s in os.listdir(root):
    cand = os.path.join(root, s, 'scratchpad')
    if os.path.isdir(cand):
        SC = cand + '/'
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
w1, w2 = sp.symbols('w1 w2', real=True)
GT, LAM = sp.symbols('G_t Lambda', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
ww = w1**2 + w2**2; S0 = 1 + wb**2*ww/2
Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, 0]); Adn_bg = eta*Aup_bg
dphi_bg = -Q0*Adn_bg
Es, Eis = sp.symbols('E_s E_is'); kx = sp.symbols('k_x', real=True)
kv = [0, kx, 0, 0]
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
FN = {}
for nm in ['Psi', 'B1', 'B2', 'H11', 'H22', 'H33', 'H12', 'chi', 'a1', 'a2']:
    FN[nm] = nf(nm)
rho, Rk, Rb = nf('rho'); a0f, a0k, a0b = nf('a0p')
F = lambda nm: FN[nm][0]
H = sp.zeros(4, 4)
H[0, 0] = -2*F('Psi')
H[0, 1] = F('B1'); H[1, 0] = F('B1')
H[0, 2] = F('B2'); H[2, 0] = F('B2')
H[1, 1] = F('H11'); H[2, 2] = F('H22'); H[3, 3] = F('H33')
H[1, 2] = F('H12'); H[2, 1] = F('H12')
gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
Hup = eta*H*eta
gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*F('a1'),
                 Adn_bg[2]+eps*F('a2'), Adn_bg[3]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
C1 = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
solA = sp.solve([sp.expand(C1).coeff(Es, 1), sp.expand(C1).coeff(Eis, 1)],
                [a0k, a0b], dict=True)[0]
solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
a0f = a0f.subs(solA)
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*F('a1'),
                 Adn_bg[2]+eps*F('a2'), Adn_bg[3]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
P(f"[S1] constraint solved ({time.time()-T0:.1f}s)")
dphi = sp.Matrix([dphi_bg[m] + eps*d(F('chi'), m) for m in range(4)])
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
pickle.dump(L2dc, open(SC+'L2dc_full10.pkl', 'wb'))
P(f"    L2dc built+cached -> L2dc_full10.pkl: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")
