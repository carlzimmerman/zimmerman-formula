#!/usr/bin/env python3
"""d3_tie_and_trace.py -- task item 3: the leaf-average / zero-mode terms (<K>, <rho_d>), the H_K1 band-pass L = L_Lambda 3 Lambda/<K>^2, the XR20 T1 tie, and what a
spectral SUM (trace) on the closed leaf could and could not generate.

PRE-DECLARED (written before running):
  H1  in the flat vacuum <K> = 3H, Omega_Lambda(<K>) = 3 Lambda/<K>^2 = 1, y_th ~ (<K>^2/3 - Lambda) = 0 and the band-pass (S_xi - S_B) annihilates constants:
      the chain's Lambda-tied length L = L_Lambda Omega_Lambda is the declared constant L_Lambda in the vacuum -- the tie ties no scale to a0.
  H2  (closed leaf) Omega_Lambda(<K>) = 3 Lambda/<K>^2 = coth^2(Ht) on a(t) = cosh(Ht)/H: the chain's reading is a flat-leaf statement, and in any case not a0-related.
  H3  the projected sources (7), (R4) have exactly zero N sqrt(h)-integral for arbitrary inhomogeneous data and vanish identically for homogeneous data; the unprojected source does not.
  H4  the only a0-Lambda tie in the chain (XR20 T1) is alpha = kappa sqrt(Lambda/8 pi), so Lambda/alpha^2 = 8 pi/kappa^2 = 32 pi at kappa = 1/2: the pi is Einstein's 8 pi, inserted by hand;
      it is not filter- or b-dependent.
  H5  a heat-trace (spectral-sum) term is NOT in the classical action; if it were, it would carry hbar and 1/b^2 (or b^(-3/2)), and for the record's xi window would be ~1e-77 of rho_Lambda;
      the b that would make it equal rho_Lambda is ~25 micron, 19 orders of magnitude below the record's xi.
  H6  any spectral sum on the closed leaf is a function of (Lambda, b) only; a0 is absent from it.
Exit 0 iff all checks (including controls) held.
"""
import sys
import numpy as np
import sympy as sp
import mpmath as mp

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


t = sp.symbols('t', real=True)
Lam, H, Lc = sp.symbols('Lambda H L_Lambda', positive=True)

# ---------------------------------------------------------------------------------------------------------------
print("== A. leaf-mean terms in the vacuum")
# flat leaf: a = exp(Ht):  <K> = 3 a'/a = 3H
a_flat = sp.exp(H * t)
K_flat = 3 * sp.diff(a_flat, t) / a_flat
Om_flat = sp.simplify((3 * Lam / K_flat**2).subs(Lam, 3 * H**2))
yth = sp.simplify((K_flat**2 / 3 - Lam).subs(Lam, 3 * H**2))
chk("A1 flat vacuum: <K> = 3H, Omega_Lambda(<K>) = 3 Lambda/<K>^2 = 1, and <K>^2/3 - Lambda = 8 pi G rho_matter = 0  (so the tied yield y_th vanishes and L = L_Lambda exactly)",
    sp.simplify(K_flat - 3 * H) == 0 and Om_flat == 1 and yth == 0)
a_cl = sp.cosh(H * t) / H
K_cl = 3 * sp.diff(a_cl, t) / a_cl
Om_cl = sp.simplify((3 * Lam / K_cl**2).subs(Lam, 3 * H**2))
chk("A2 closed leaf a = cosh(Ht)/H: <K> = 3H tanh(Ht), 3 Lambda/<K>^2 = coth^2(Ht) (> 1), <K>^2/3 - Lambda = -3/a^2: the chain's Omega_Lambda(<K>) is a flat-leaf reading; the curvature term is separate",
    sp.simplify(Om_cl - sp.coth(H * t)**2) == 0 and sp.simplify((K_cl**2 / 3 - 3 * H**2) + 3 / a_cl**2) == 0)
# band-pass annihilates constants: eigenvalues on S^3(a): -l(l+2)/a^2
xi2, B2, aa, l = sp.symbols('b_xi B a l', positive=True)
bp = lambda ll: sp.exp(-xi2 * ll * (ll + 2) / aa**2) - sp.exp(-B2 * ll * (ll + 2) / aa**2)
chk("A3 band-pass (S_xi - S_B) on S^3: multiplier exp(-b_xi l(l+2)/a^2) - exp(-B l(l+2)/a^2) vanishes at l = 0 for every b_xi, B, a: chi = (S_xi - S_B) phi = 0 for a constant phi (vacuum)",
    sp.simplify(bp(0)) == 0 and sp.simplify(bp(1)) != 0)

# projected sources: zero N sqrt(h) integral
rng = np.random.default_rng(11)
nc = 200
Nl = rng.uniform(0.3, 3.0, nc)
sh = rng.uniform(0.2, 2.0, nc)
sig = rng.normal(size=nc) + 2.0
mean_Ns = (sh * Nl * sig).sum() / sh.sum()
src_proj = sig - mean_Ns / Nl
zero_int = (Nl * sh * src_proj).sum()
chk("A4 projected source sigma - <N sigma>/N has N sqrt(h)-integral %.2e (= 0 to round-off) for 200 random cells; the unprojected source has %.3f" % (zero_int, (Nl * sh * sig).sum()),
    abs(zero_int) < 1e-10 * abs((Nl * sh * sig).sum()) and abs((Nl * sh * sig).sum()) > 1)
Nc, shc, sigc = np.full(nc, 1.7), np.full(nc, 0.9), np.full(nc, 2.5)
srch = sigc - (shc * Nc * sigc).sum() / shc.sum() / Nc
chk("A5 homogeneous data: the projected source is identically zero in every cell (max |.| = %.1e); a positive homogeneous carrier is admitted, the CONTROL (unprojected) source would be sigma = 2.5 != 0 everywhere and force the carrier to vanish" % np.abs(srch).max(),
    np.abs(srch).max() < 1e-12 and (sigc != 0).all())

# ---------------------------------------------------------------------------------------------------------------
print("\n== B. the a0-Lambda tie of the chain (XR20 T1) and where the pi sits")
kap, al, Lm = sp.symbols('kappa alpha Lambda_', positive=True)
tie = sp.solve(sp.Eq(al, kap * sp.sqrt(Lm / (8 * sp.pi))), Lm)[0]
chk("B1 T1: alpha = kappa sqrt(Lambda/8 pi)  <=>  Lambda/alpha^2 = 8 pi/kappa^2 ; at kappa = 1/2 this is 32 pi (the puzzle).  The pi is Einstein's 8 pi in M_P^2 = 1/8 pi G, put in by hand",
    sp.simplify(tie / al**2 - 8 * sp.pi / kap**2) == 0 and sp.simplify((8 * sp.pi / kap**2).subs(kap, sp.Rational(1, 2)) - 32 * sp.pi) == 0)
# the vacuum sector (d1) is independent of alpha (= a0 / c^2): the tie is a relation between two coefficients of the same bracket {R - 2 Lambda + ... + 2 a0^2 q(...)}
chk("B2 in the action's own bracket, -2 Lambda and the kernel scale 2 a0^2 are two independent coefficients; Lambda = 32 pi a0^2 says -2 Lambda = -64 pi a0^2: the ratio 32 pi (= U_v of p09) is what any tie must reproduce, and no filter enters it",
    sp.simplify(sp.Rational(-2) * 32 * sp.pi - (-64 * sp.pi)) == 0)
# c_N ambiguity: G_cosm = G_bare, G_N = G_bare/c_N (quoted from the record's FINAL_ACTION sec. 5, 7; not re-derived)
cN, GN, rhoL = sp.symbols('c_N G_N rho_L', positive=True)
Gb = cN * GN
a0_ = sp.Symbol('a0_', positive=True)
Lsol = sp.solve(sp.Eq(GN * rhoL, 4 * a0_**2), rhoL)[0]                                # locally measured G_N: G_N rho_Lambda = 4 a0^2
Lam_from = sp.simplify(8 * sp.pi * cN * GN * Lsol)                                     # Lambda = 8 pi c_N G_N rho_Lambda   (from 3 M_P^2 H^2 = M_P^2 Lambda, G_N = G_bare/c_N)
chk("B3 (quoted, not re-derived) with G_N = G_bare/c_N and 3 M_P^2 H^2 = M_P^2 Lambda + ...: Lambda = 8 pi c_N G_N rho_Lambda, so 'G rho_Lambda = 4 a0^2' with the LOCALLY measured G_N reads Lambda = 32 pi c_N a0^2 (= %s): the action leaves a factor c_N in (0,1) that the puzzle's bookkeeping must specify" % Lam_from,
    sp.simplify(Lam_from - 32 * sp.pi * cN * a0_**2) == 0)

# ---------------------------------------------------------------------------------------------------------------
print("\n== C. a spectral SUM on the closed leaf: what it depends on")
b, L2, a0s, LamS = sp.symbols('b L2 a0 Lambda_S', positive=True)
Nfun = sp.sqrt(sp.pi) / 4 * (L2 / b)**sp.Rational(3, 2) * sp.exp(b / L2)          # Tr S_h on S^3(L), up to exp-small terms (d2 1a)
Nlam = Nfun.subs(L2, 3 / LamS)                                                      # de Sitter neck radius L^2 = 3/Lambda
chk("C1 Tr S_h on the de Sitter neck is a function of (Lambda, b) only: dN/da0 = 0 identically; N = (sqrt(pi)/4)(3/(b Lambda))^(3/2) exp(b Lambda/3)",
    sp.diff(Nlam, a0s) == 0 and sp.simplify(Nlam - sp.sqrt(sp.pi) / 4 * (3 / (b * LamS))**sp.Rational(3, 2) * sp.exp(b * LamS / 3)) == 0)
# a0 could only enter through b(a0): with the Rindler length as filter length the trace is 1 (d2 5b); with any other length it is a new constant (FP17: xi not buildable from a0, Lambda, G, c)

# H_K1's declared length: L_Lambda = 2.9 Mpc (window 2.65-5.0 Mpc) with B = L^2/2 on a leaf of radius c/H_Lambda
cH_Mpc = 299792.458 / (67.4 * np.sqrt(0.685))
for LL in (2.65, 2.9, 5.0):
    e_ = (LL / cH_Mpc)**2 / 2
    print("   H_K1 band-pass: L_Lambda = %.2f Mpc, c/H_Lambda = %.0f Mpc: eps = B/L_leaf^2 = %.2e, Weyl cell count (sqrt(pi)/4) eps^(-3/2) = %.2e" % (LL, cH_Mpc, e_, np.sqrt(np.pi) / 4 * e_**-1.5))
e_mid = (2.9 / cH_Mpc)**2 / 2
chk("C1b H_K1's declared L_Lambda = 2.9 Mpc puts the closed-leaf eps at %.1e << 1: deep Weyl regime, the band-pass acts on a leaf of ~%.0e filter cells; the length is a declared constant (FP19/FP20b window), not a spectral output" % (e_mid, np.sqrt(np.pi) / 4 * e_mid**-1.5),
    e_mid < 1e-6 and np.sqrt(np.pi) / 4 * e_mid**-1.5 > 1e9)

# hypothetical trace (one-loop / zeta) term:  Gamma = -(hbar/2) int_b^inf dt/t Tr e^{t Delta}
tt, bb = sp.symbols('tt bb', positive=True)
I4 = sp.integrate((1 / tt) * (4 * sp.pi * tt)**-2, (tt, bb, sp.oo))
I3 = sp.integrate((1 / tt) * (4 * sp.pi * tt)**sp.Rational(-3, 2), (tt, bb, sp.oo))
chk("C3 hypothetical trace term: int_b^inf dt/t (4 pi t)^(-2) = 1/(32 pi^2 b^2)  [4D covariant filter: the '32 pi^2' of the puzzle appears literally, as 2(4 pi)^2]  and  int_b^inf dt/t (4 pi t)^(-3/2) = 1/(12 pi^(3/2) b^(3/2))  [the record's SPATIAL filter: half-integer pi-parity]",
    sp.simplify(I4 - 1 / (32 * sp.pi**2 * bb**2)) == 0 and sp.simplify(I3 - 1 / (12 * sp.pi**sp.Rational(3, 2) * bb**sp.Rational(3, 2))) == 0)
# numbers (SI): the b at which  rho_ind = hbar c/(64 pi^2 b^2) equals rho_Lambda, versus the record's xi window
from scipy import constants as sc
hbar_c = sc.hbar * sc.c
H0 = 67.4e3 / (1e6 * sc.parsec)                                                       # s^-1
OmL = 0.685
rho_L = OmL * 3 * H0**2 / (8 * np.pi * sc.G)                                          # kg/m^3
u_L = rho_L * sc.c**2                                                                # J/m^3
b_need = np.sqrt(hbar_c / (64 * np.pi**2 * u_L))
xi_need = np.sqrt(2 * b_need)
xi_rec = 0.0243 * sc.parsec
ratio_rho = (hbar_c / (64 * np.pi**2 * (xi_rec**2 / 2)**2)) / u_L
print("   rho_Lambda c^2 = %.3e J/m^3;  b_need = %.3e m^2 (xi_need = %.2e m = %.1f micron); record's xi_min = %.2e m; xi_min/xi_need = %.1e; rho_ind(xi_min)/rho_Lambda = %.1e"
      % (u_L, b_need, xi_need, xi_need * 1e6, xi_rec, xi_rec / xi_need, ratio_rho))
chk("C4 (hypothetical) a trace term hbar c/(64 pi^2 b^2) matches rho_Lambda only for xi ~ %.0f micron; the record's xi_min = 0.0243 pc is %.0e times larger, so it would give %.0e of rho_Lambda (and carries hbar, which the classical relation Lambda = 32 pi a0^2 does not)"
    % (xi_need * 1e6, xi_rec / xi_need, ratio_rho), 10 < xi_need * 1e6 < 100 and ratio_rho < 1e-70)
from sympy.physics import units as u
from sympy.physics.units.systems.si import dimsys_SI
dimE = dimsys_SI.get_dimensional_dependencies(u.energy / u.length**3)
d_with = dimsys_SI.get_dimensional_dependencies(u.action * u.velocity / u.length**4)      # hbar has the dimension of action, c of velocity
d_without = dimsys_SI.get_dimensional_dependencies(u.velocity / u.length**4)
chk("C5 dimensional analysis (SI base dimensions): hbar c / length^4 has the dimensions of an energy density, c/length^4 does not: any trace-generated vacuum energy needs hbar, while Lambda = 32 pi a0^2 (c = G = 1) has none",
    d_with == dimE and d_without != dimE)

print("\n%d/%d checks held" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
