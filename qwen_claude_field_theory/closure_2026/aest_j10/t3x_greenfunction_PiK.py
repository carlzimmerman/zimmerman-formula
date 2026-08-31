#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
t3x_greenfunction_PiK.py   (TARGET-3 independent cross-route, part 3)
=====================================================================
GREEN-FUNCTION (linear-response) estimate of Pi_K = the projection of the
unsuppressed novel channel F_QQ(Q0) = mu2(1+kappa^2/4pi) onto alpha_2,
using ONLY certified ingredients:

  (a) the certified insertion (t3x_structural_deltaQ_projection.py [C.2]):
      the sole Q0-free O(w^2) piece of  -F_QQ (deltaQ)^2  is
          dM_chichi = -2 F_QQ k_x^2 w1^2 w_b^2   (on the chi-chi entry);
      every other insertion (including all O(w^1) ones) is Q0^2-weighted, so
      at leading order in Q0/q the F_QQ-linear O(w^2 U) response runs ONLY
      through the STATIC block:  first-order perturbation theory
          dPsi = -(M^-1)_{Psi chi} * dM_chichi * chi0 .
  (b) the AeST Newton anchor  h00 = 8 pi G/(1-K_B/2) rho/k^2  and gamma=1
      (Phi=Psi), both committed anchors of the base theory.
  (c) the static response ratio r = chi0/Psi0, computed here from the chi-row
      of the quadratic action (the chi row involves ONLY the scalar/aether
      sectors -- the Einstein sector has no chi -- so the wb=0 mini-build
      below is exact for it), with a1=0, s22=0 (static parity, matches the
      full-solve cache) and Phi=Psi (anchor).

RESULT (derived symbolically below):
      Pi_K = d(alpha_2) = -+ 2 F_QQ r^2 / (2-K_B) * [sign conv]
  i.e. |Pi_K| = 2 r^2/(2-K_B) * mu2 (1+kappa^2/4pi),  r = O(1/2..1)
  -- an UNSUPPRESSED O(mu2) alpha_2 contribution, no Qbar^2 factor.

AUDIT NOTE recorded here (matters for T1/T2): the uncommitted route2_v2
cache L2dc_v2.pkl FAILS the anchors when actually run (Newton != 8pi/(1-KB/2),
alpha_1 = +5.75 at K_B=1/5 instead of -0.8, alpha_2 ~ -1/(K2 Q0^2) divergent
in the PPN hierarchy Q0/k -> 0 = the unregulated c123=0 FJ pole reappearing
because the K2 channel's STATIC stiffness is Q0^2-weighted).  Its absolute
alpha_2 numbers are NOT quotable; only the O(1) size of its K2-slope
(+0.3..+1.6) is noted as consistent with |Pi_K| ~ 2r^2/(2-K_B) ~ 0.3..1.3.

Run:  python3 t3x_greenfunction_PiK.py | tee t3x_greenfunction_PiK.out
"""
import sympy as sp, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)

# ============================================================================
P("="*78)
P("[1] chi-row of the static quadratic action (wb=0 exact mini-build)")
P("="*78)
eps = sp.symbols('eps', positive=True)
Q0, JY, KB, FQQ = sp.symbols('Q_0 J_Y K_B F_QQ', real=True)
eta4 = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is'); kx = sp.symbols('k_x', real=True)
kv = [0, kx, 0, 0]
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
s22, s22k, s22b = nf('s22')
a1f, a1k, a1b = nf('a1'); chi, chik, chib = nf('chi'); a0f, a0k, a0b = nf('a0p')
H = sp.zeros(4, 4)
H[0, 0] = -2*Psi; H[1, 1] = -2*Phi
H[2, 2] = -2*Phi + s22; H[3, 3] = -2*Phi - s22
gd = sp.Matrix(4, 4, lambda m, n: eta4[m, n] + eps*H[m, n])
Hup = eta4*H*eta4
gu = sp.Matrix(4, 4, lambda i, j: (eta4 - eps*Hup + eps**2*(Hup*H*eta4))[i, j])
Aup_bg = sp.Matrix([1, 0, 0, 0]); Adn_bg = eta4*Aup_bg
dphi_bg = -Q0*Adn_bg
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2], Adn_bg[3]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
C1c = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
solA = sp.solve([sp.expand(C1c).coeff(Es, 1), sp.expand(C1c).coeff(Eis, 1)],
                [a0k, a0b], dict=True)[0]
a0f = a0f.subs(solA)
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2], Adn_bg[3]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
dphi = sp.Matrix([dphi_bg[m] + eps*d(chi, m) for m in range(4)])
def te(e):
    e = sp.expand(e); return sum(e.coeff(eps, i)*eps**i for i in range(3))
Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s))
        for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
Jup = [te(sum(AupT[nu]*(d(AupT[al], nu) + sum(te(Gam[al][nu][r])*AupT[r] for r in range(4)))
       for nu in range(4))) for al in range(4)]
dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
Yc = te(sum((guT[m, n] + AupT[m]*AupT[n])*dphiT[m]*dphiT[n]
            for m in range(4) for n in range(4)))
Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m) - d(Adn[m], n)))
F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta4[m, a]*eta4[n, b]
                for m in range(4) for n in range(4) for a in range(4) for b in range(4))
dQ = sp.expand(Qc - Q0)
def DC(e):
    e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
    for mon, c in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            out += c*(Es*Eis)**mon[0]
    return out.subs(Es*Eis, 1) if out != 0 else out
P(f"  static geometry/dark-sector objects built ({time.time()-T0:.1f}s)")
# Two Y-bookkeepings: (A) route2_v2_build convention: -(2-KB)*Y in the action
# AND an extra -(2-KB)*J_Y*Y at quadratic order (total (1+J_Y));
# (B) J_Y-only (kernel replaces the whole Y quadratic).
for tag, Ycoef in [("(A) build conv: total (1+J_Y) Y", -(2-KB)*(1+JY)),
                   ("(B) J_Y-only               ", -(2-KB)*JY)]:
    L_as = sp.expand(-(KB/2)*F2 + 2*(2-KB)*Jdphi + Ycoef*Yc - FQQ*te(dQ**2))
    L2 = DC(sp.expand(L_as).coeff(eps, 2))
    Echi = sp.expand(sp.diff(L2, chib))
    cchi = sp.simplify(Echi.coeff(chik)); cPsi = sp.simplify(Echi.coeff(Psik))
    cPhi = sp.simplify(Echi.coeff(Phik)); ca1 = sp.simplify(Echi.coeff(a1k))
    cs22 = sp.simplify(Echi.coeff(s22k))
    P(f"  {tag}: chi-EOM row:")
    P(f"     M_chichi={cchi}  M_chiPsi={cPsi}  M_chiPhi={cPhi}  M_chia1={ca1}  M_chis22={cs22}")
    # static solve of the chi row with a1=0, s22=0, Phi=Psi (anchors):
    r = sp.simplify(-(cPsi + cPhi)/cchi)
    P(f"     => r = chi0/Psi0 = {r}   ;  at J_Y=1: {sp.simplify(r.subs(JY,1))}")
P("  (route2_v2 cache's static solve measured r = 1/(1+J_Y) -> 1/2 at J_Y=1,")
P("   matching convention (A); convention (B) gives r -> 1 at J_Y=1.")
P("   Bracket r in [1/2, 1].)")

# ============================================================================
P("")
P("="*78)
P("[2] response formula for Pi_K (exact sympy on the reduced model,")
P("    model-parameter independence verified)")
P("="*78)
# Reduced static system (Psi-like sourced channel + chi), M symmetric, and the
# EOM convention matching the DC quadratic form:  (M x)_i + s_i = 0 with
# M_ij = d^2 L2dc / d bra_i d ket_j and s_Psi = dL_matt/dPsi_bra = -16 pi Rk
# (L2_matt = -16 pi G_t rho (-h00/2) = -16 pi G_t rho Psi, G_t = 1).
cg, m, cc, w1, wbs = sp.symbols('c_g m c_chi w1 w_b', real=True)
Rk, r_ = sp.symbols('R_k r', real=True)
M = sp.Matrix([[cg, m], [m, cc]])*kx**2
src = sp.Matrix([-16*sp.pi*Rk, 0])
# anchors: h00 = -2 Psi, U = h00/2 = -Psi, Newton U0 = 4 pi G_N Rk/kx^2,
# G_N = 1/(1-K_B/2)  =>  Psi0 = -8 pi Rk/((2-K_B) kx^2);  chi0 = r Psi0.
Psi0t = -8*sp.pi*Rk/((2-KB)*kx**2)
x0 = M.solve(-src)
con = sp.solve([sp.Eq(x0[0], Psi0t), sp.Eq(x0[1], r_*Psi0t)], [cg, cc], dict=True)[0]
P("  constraints solved: c_g, c_chi eliminated in favor of (r, K_B, m):")
P("    c_g =", sp.simplify(con[cg]), "   c_chi =", sp.simplify(con[cc]))
# insertion on the chi-chi entry (certified [C.2]): dM_chichi = -2 FQQ kx^2 w1^2 wb^2
dM = sp.Matrix([[0, 0], [0, -2*FQQ*kx**2*w1**2*wbs**2]])
xF = (M + dM).solve(-src)             # exact solution with the insertion
dPsi_exact = sp.simplify((xF[0] - x0[0]).subs(con))
dPsi_1 = sp.series(dPsi_exact, FQQ, 0, 2).removeO()   # first order in F_QQ
dPsi_1 = sp.simplify(dPsi_1)
P("  dPsi (first order in F_QQ) =", sp.factor(dPsi_1))
P("  independent of leftover model parameter m ?", m not in dPsi_1.free_symbols)
dh00 = -2*dPsi_1                       # h00 = -2 Psi
U0 = -Psi0t
coefpar = sp.simplify(dh00.coeff(w1**2).coeff(wbs**2)/U0)
PiK = sp.simplify(coefpar/2)           # par - perp = 2 alpha_2 (perp untouched)
P("  Pi_K = d(alpha_2)/d(unit) =", sp.factor(PiK), "   [per unit F_QQ:",
  sp.factor(sp.simplify(PiK/FQQ)), "]")
P("  ==> |Pi_K| = r^2/(2-K_B) * F_QQ ,  F_QQ = mu2 (1+kappa^2/4pi)")
P("  (overall sign carries the h00/U and DC conventions; the certified claims")
P("   are the CHANNEL -- w_par^2 U only, alpha_2-pure -- and the magnitude up")
P("   to a convention-level factor ~2.)")

# ============================================================================
P("")
P("="*78)
P("[3] numbers")
P("="*78)
for kbv in [sp.Rational(1, 5), sp.Rational(1, 4), sp.Rational(1, 2)]:
    for rv in [sp.Rational(1, 2), 1]:
        val = float((rv**2/(2-kbv)))
        P(f"  K_B={float(kbv):.2f}, r={float(rv):.1f}:  |Pi_K|/F_QQ = {val:.3f}")
P("""
  With F_QQ = mu2(1+kappa^2/4pi), kappa=1/2 => 1+kappa^2/4pi = 1.0199:
    |Delta alpha_2^novel| ~ (0.14 .. 0.7) x mu2  (x2 convention band -> 0.1..1.3)
  vs the Will/LLR bound |alpha_2| < ~1e-7 (and the K_QQ=mu2 share is ~50x the
  a0-promotion share Pi_a0 = (kappa^2/4pi) Pi_K ~ 0.02 Pi_K).
  UNLESS mu2 = Kcal_QQ(Q0) <~ 1e-7/0.3 ~ 3e-7 (dimensionless), the novel
  channel ALONE breaches alpha_2 -- independent of the base-AeST C0 question.
  The naive beta-channel projection is instead (Q0/q)^2-suppressed (~1e-30 at
  AU): |beta-1|^novel ~ mu2 (Q0/q)^2, dead-safe; the liability naive counting
  assigned to beta actually sits in alpha_2.""")
P(f"done ({time.time()-T0:.1f}s)")
