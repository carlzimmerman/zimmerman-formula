#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
SECTION 15: EFT operator analysis and technical naturalness of the frozen action

    S = (M_Pl^2 c^3/2) INT d^4x N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
        - (2 a0^2/c^4) F(X,Y) ] + S_m,
    F(X,Y) = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps [X^2/(1+X)^4] Y,
    X = c^4 a.a/a0^2,  Y = c^8 Rbar_ij Rbar^ij / a0^4.

Every check below is either a sympy identity (exact) or a numeric evaluation of a
derived formula.  Labels: DERIVED / ASSUMED / IMPORTED(cite) printed with each block.
Nothing here modifies the action; failures would be reported as failures.

Checks:
  C1  mu = 1 + F_X = x/(1+x)                                   [DERIVED, sympy]
  C2  small-X series of F has half-integer powers (X^{3/2}, X^{5/2}, ...)
      => F is NOT analytic at X=0; the -X piece renormalises eta_K by +2
                                                               [DERIVED, sympy]
  C3  large-X: F = -2 sqrt(X) + ln X + o(1): the |a|-linear non-analytic term
                                                               [DERIVED, sympy]
  C4  Hessian of |a| w.r.t. a_i has transverse eigenvalues 1/|a| -> diverges at
      a=0: no vertex expansion about the vacuum exists          [DERIVED, sympy]
  C5  F_XX = 1/(2 sqrt(X)(1+sqrt(X))^2) > 0, ~ X^{-3/2}/2 at large X: local
      strong-coupling scale RISES on high-X backgrounds (Vainshtein-type)
                                                               [DERIVED, sympy]
  C6  Milgrom space-time scaling (t,x)->(lam t, lam x), M fixed, selects the
      deep-MOND exponent p=3/2 in div(|grad phi|^{2p-2} grad phi) = 4 pi G rho
      UNIQUELY; the Newtonian term is NOT invariant             [DERIVED, sympy]
  C7  sqrt(h) N D_i a^i = total derivative + sqrt(h) N a_i a^i  (flat 3d check)
      => D.a is redundant at 2nd order; the 2nd-order operator basis is
      {(3)R, K_ij K^ij, K^2, a^2} and the action contains ALL of them
                                                               [DERIVED, sympy]
  C8  chi(M) = eps c^4/(G M a0) = M_*/M with M_* = eps c^4/(G a0)  (identity);
      Lambda_sun = 6.50e23; eps_cap = 1.73/Lambda_sun = 2.7e-24;
      M_*(eps_cap) = 1.73 Msun;  M_*(eps=1) = 6.5e23 Msun       [DERIVED + numeric]
  C9  the F-sector energy-density scale is Lambda_sc^4 = a0^2/(8 pi G)
      = (Mbar_Pl a0)^2 in natural units -> Lambda_sc = 0.71 meV = (0.28 mm)^-1;
      cubic-vertex estimate gives the same scale x O(2);
      identity Lambda_sc^4/(rho_Lam c^2) = kappa^2/(8 pi) = 1/(32 pi) for
      a0 = (1/2) c sqrt(G rho_Lam)                              [DERIVED + numeric]
  C10 the dimensionless (hbar-unit) coefficient of the Rbar^2 operator is
      beta = eps A(X) c^7/(8 pi G hbar a0^2) = eps A(X) x 1.40e122
      (identity: c^7/(8 pi G hbar a0^2) = (Mbar_Pl c^2 / (hbar a0/c))^2);
      graviton-loop-natural beta ~ 1/16pi^2 => eps_loop ~ 7e-124 << eps_cap:
      eps is radiatively STABLE but NOT protected by any symmetry [DERIVED + numeric]
"""
import sympy as sp
import numpy as np

PASS = []
def head(t): print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100, flush=True)
def ok(c, l, d=""):
    print(f"  [{'ok' if c else 'FAIL'}] {l}" + (f"   {d}" if d else ""), flush=True)
    PASS.append(bool(c)); return c
def info(l, d=""): print(f"  [info] {l}" + (f"   {d}" if d else ""), flush=True)

X = sp.symbols('X', positive=True)
u = sp.symbols('u', positive=True)          # u = sqrt(X) = g/a0
F0 = -2*sp.sqrt(X) + 2*sp.log(1 + sp.sqrt(X))   # the X-part of F (Y=0)

# ----------------------------------------------------------------- C1
head("C1  [DERIVED]  mu = 1 + F_X = x/(1+x)")
FX = sp.simplify(sp.diff(F0, X))
ok(sp.simplify(FX + 1/(1 + sp.sqrt(X))) == 0, "C1a  F_X = -1/(1+sqrt X)")
mu = sp.simplify(1 + FX)
ok(sp.simplify(mu - sp.sqrt(X)/(1 + sp.sqrt(X))) == 0, "C1b  mu = x/(1+x)")

# ----------------------------------------------------------------- C2
head("C2  [DERIVED]  small-X structure: F = -X + (2/3)X^{3/2} - X^2/2 + (2/5)X^{5/2} - ...")
Fu = F0.subs(X, u**2)                        # F as a function of u = sqrt(X)
ser = sp.series(Fu, u, 0, 8).removeO().expand()
target = -u**2 + sp.Rational(2,3)*u**3 - u**4/2 + sp.Rational(2,5)*u**5 - u**6/3 + sp.Rational(2,7)*u**7
ok(sp.simplify(ser - target) == 0, "C2a  series in u = sqrt(X) confirmed to u^7")
c32 = ser.coeff(u, 3); c52 = ser.coeff(u, 5)
ok(c32 == sp.Rational(2,3) and c52 == sp.Rational(2,5),
   "C2b  the X^{3/2} and X^{5/2} coefficients are NONZERO",
   "=> F has no Taylor series in X at X=0: non-analytic at the vacuum")
# the -X piece renormalises eta_K:  -(2 a0^2/c^4)(-X) = +2 a_i a^i
ok(sp.simplify(ser.coeff(u, 2) + 1) == 0,
   "C2c  the analytic -X piece contributes exactly +2 to eta_K",
   "-(2 a0^2/c^4)(-X) = +2 a.a : the deep-MOND sector keeps a healthy quadratic term")

# ----------------------------------------------------------------- C3
head("C3  [DERIVED]  large-X: F + 2 sqrt(X) - ln(X) -> 0")
lim = sp.limit(F0 + 2*sp.sqrt(X) - sp.log(X), X, sp.oo)
ok(lim == 0, "C3a  F = -2 sqrt(X) + ln X + o(1)",
   "the -2 sqrt(X) term is LINEAR in |a|: L contains +(a0/(4 pi G))|grad Phi| -- no local")
info("C3b", "analytic operator basis contains a term linear in a field gradient; scale a0 explicit")

# ----------------------------------------------------------------- C4
head("C4  [DERIVED]  the vacuum vertex expansion does not exist")
a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
r = sp.sqrt(a1**2 + a2**2 + a3**2)
H = sp.hessian(r, (a1, a2, a3))
ev = list(H.subs({a1: sp.Symbol('s', positive=True), a2: 0, a3: 0}).eigenvals().keys())
ev = sorted([sp.simplify(e) for e in ev], key=str)
s = sp.Symbol('s', positive=True)
ok(set(map(str, ev)) == {"0", "1/s"},
   "C4a  Hessian of |a| has eigenvalues {0 (radial), 1/|a| x2 (transverse)}",
   "second variation of the -2 sqrt(X) term about a=0 DIVERGES: no perturbative vacuum")
ok(sp.limit(1/s, s, 0) == sp.oo, "C4b  transverse eigenvalue -> infinity as |a| -> 0")

# ----------------------------------------------------------------- C5
head("C5  [DERIVED]  F_XX > 0 and decays: strong coupling is a VACUUM problem only")
FXX = sp.simplify(sp.diff(F0, X, 2))
ok(sp.simplify(FXX - 1/(2*sp.sqrt(X)*(1 + sp.sqrt(X))**2)) == 0,
   "C5a  F_XX = 1/(2 sqrt(X)(1+sqrt(X))^2)")
ok(sp.limit(FXX*2*X**sp.Rational(3,2), X, sp.oo) == 1,
   "C5b  F_XX ~ X^{-3/2}/2 at large X",
   "on solar-system backgrounds (X ~ 1e22) self-interactions are suppressed by the")
info("C5c", "background: the local strong-coupling scale is raised far above Lambda_sc (Vainshtein-type)")

# ----------------------------------------------------------------- C6
head("C6  [DERIVED]  Milgrom scaling selects p = 3/2 uniquely (deep-MOND protection)")
# under (t,x) -> (lam t, lam x) with phi (units v^2) invariant and M fixed:
# each spatial derivative carries weight -1  =>  weight[div(|grad phi|^{2p-2} grad phi)] = -2p
# source: rho = M/vol -> weight -3.  Invariance of the EOM: -2p = -3.
p, lam = sp.symbols('p lam', positive=True)
wLHS = -2*p          # (2p-2) gradients inside + 1 gradient + 1 divergence
wRHS = -3            # G M / r^3 with M fixed
sol = sp.solve(sp.Eq(wLHS, wRHS), p)
ok(sol == [sp.Rational(3, 2)], "C6a  -2p = -3  =>  p = 3/2, uniquely",
   "the deep-MOND exponent X^{3/2} is the ONLY power compatible with Milgrom scaling")
ok(wLHS.subs(p, 1) != wRHS, "C6b  the Newtonian term (p=1, weight -2) is NOT scale invariant",
   "=> the symmetry protects the deep-MOND ENDPOINT, not the crossover function or a0")

# ----------------------------------------------------------------- C7
head("C7  [DERIVED]  D_i a^i is redundant; the 2nd-order basis is complete and fully used")
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
N = sp.Function('N', positive=True)(x1, x2, x3)
av = [sp.diff(sp.log(N), xi) for xi in (x1, x2, x3)]           # a_i = D_i ln N (flat 3d)
divNa = sum(sp.diff(N*av[i], xi) for i, xi in enumerate((x1, x2, x3)))
NDa   = N*sum(sp.diff(av[i], xi) for i, xi in enumerate((x1, x2, x3)))
Naa   = N*sum(ai**2 for ai in av)
ok(sp.simplify(divNa - (NDa + Naa)) == 0,
   "C7a  N D_i a^i = div(N a) - N a.a   (exact, flat-space representative)",
   "so at 2 derivatives the independent T-even scalars are exactly")
info("C7b", "{(3)R, K_ij K^ij, K^2, a_i a^i} -- ALL present with free coefficients (1,1,-lam_K,eta_K)")
info("C7c", "[IMPORTED: Blas-Pujolas-Sibiryakov 0909.3525] confirms this is the complete L_2;")
info("C7d", "vorticity terms vanish IDENTICALLY (u hypersurface-orthogonal), not omitted")

# ----------------------------------------------------------------- C8
head("C8  [DERIVED + numeric]  the emergent mass scale M_* and the eps hierarchy")
epsS, c_, G_, M_, a0_ = sp.symbols('eps c G M a0', positive=True)
chi = epsS*c_**4/(G_*M_*a0_)
Mstar = epsS*c_**4/(G_*a0_)
ok(sp.simplify(chi - Mstar/M_) == 0, "C8a  chi(M) = M_*/M with M_* = eps c^4/(G a0)  (identity)",
   "=> chi_sun <= 1.73  <=>  M_* <= 1.73 Msun  EXACTLY")
C = 2.99792458e8; G = 6.6743e-11; MSUN = 1.98892e30; A0 = 9.3619e-11
HBAR = 1.054571817e-34; EV = 1.602176634e-19
Lam_sun = C**4/(G*MSUN*A0)
eps_cap = 1.73/Lam_sun
ok(abs(Lam_sun/6.50e23 - 1) < 0.02, f"C8b  Lambda_sun = {Lam_sun:.3e} (= 6.50e23)")
ok(abs(eps_cap/2.7e-24 - 1) < 0.02,
   f"C8c  eps_cap = 1.73/Lambda_sun = {eps_cap:.2e}  (the repo ellipticity bound 2.7e-24)")
Mstar_cap = eps_cap*C**4/(G*A0)/MSUN
ok(abs(Mstar_cap - 1.73) < 0.01, f"C8d  M_*(eps_cap) = {Mstar_cap:.3f} Msun")
Mstar_nat = 1.0*C**4/(G*A0)/MSUN
ok(0.9 < Mstar_nat/6.5e23 < 1.1,
   f"C8e  the natural value eps = O(1) gives M_* = {Mstar_nat:.2e} Msun",
   "i.e. the Y-sector would be active for EVERY bound structure in the universe")
info("C8f", f"the hierarchy demanded: eps/eps_natural = {eps_cap:.1e} -- 24 orders of magnitude")

# ----------------------------------------------------------------- C9
head("C9  [DERIVED + numeric]  the strong-coupling / F-sector scale Lambda_sc")
# static weak-field anchor (given): the F-term contributes -(a0^2/(8 pi G)) F per unit dt d^3x
uF = A0**2/(8*np.pi*G)                                   # J/m^3
# convert to eV^4:  u[SI] = Lambda_eV^4 * e / (hbar c / e)^3
hbarc_eVm = HBAR*C/EV                                    # eV.m
conv = EV/hbarc_eVm**3                                   # (J/m^3) per eV^4
Lam_sc = (uF/conv)**0.25                                 # eV
info("C9a", f"u_F = a0^2/(8 pi G) = {uF:.3e} J/m^3  ->  Lambda_sc = {Lam_sc*1e3:.2f} meV")
ok(0.6e-3 < Lam_sc < 0.8e-3, f"C9b  Lambda_sc = {Lam_sc:.2e} eV ~ 0.7 meV")
ok(abs(hbarc_eVm/Lam_sc/2.8e-4 - 1) < 0.05,
   f"C9c  corresponding length hbar c/Lambda_sc = {hbarc_eVm/Lam_sc*1e3:.2f} mm ~ 0.28 mm")
# identity route: Lambda_sc^2 = Mbar_Pl * a0  in natural units
Mbar_eV = np.sqrt(HBAR*C**5/(8*np.pi*G))/EV              # reduced Planck ENERGY in eV
a0_eV = HBAR*(A0/C)/EV                                   # a0 as an energy in eV
ok(abs(np.sqrt(Mbar_eV*a0_eV)/Lam_sc - 1) < 1e-6,
   f"C9d  identity: Lambda_sc = sqrt(Mbar_Pl a0) exactly "
   f"(Mbar={Mbar_eV:.3e} eV, a0={a0_eV:.3e} eV)")
# cubic-vertex estimate: canonical Phi_c = Phi/sqrt(4 pi G); cubic term
# (2/3)|grad Phi|^3/(8 pi G a0) -> (sqrt(4 pi G)/(3 sqrt(4 pi G)... )):
# 1/Lambda_v^2 = sqrt(4 pi G)/(3 a0) * (2/ (8 pi G) * (4 pi G)^{3/2})/... keep it honest:
# coeff of (grad Phi_c)^3 is (2/3)(4 pi G)^{3/2}/(8 pi G a0) = (sqrt(4 pi G)/a0)*(1/3)
inv_Lv2_SI = (1.0/3.0)*np.sqrt(4*np.pi*G)/A0             # SI: s^2 kg^-1/2 m^-3/2 ... (natural below)
# natural units: sqrt(4 pi G) = sqrt(4 pi/(8 pi))/Mbar = 1/(sqrt(2) Mbar)
Lam_v = np.sqrt(3*np.sqrt(2)*Mbar_eV*a0_eV)
ok(1.0 < Lam_v/Lam_sc < 3.0,
   f"C9e  cubic-vertex scale Lambda_v = {Lam_v*1e3:.2f} meV = {Lam_v/Lam_sc:.2f} x Lambda_sc",
   "same scale up to O(1): the vacuum strong-coupling scale of the sqrt(X) sector is ~1 meV")
# dark-energy identity: with a0 = kappa c sqrt(G rho_L):  u_F/(rho_L c^2) = kappa^2/(8 pi)
kap, rhoL = sp.symbols('kappa rho_L', positive=True)
idty = sp.simplify(((kap*c_*sp.sqrt(G_*rhoL))**2/(8*sp.pi*G_))/(rhoL*c_**2) - kap**2/(8*sp.pi))
ok(idty == 0, "C9f  identity: [a0^2/(8 pi G)]/(rho_L c^2) = kappa^2/(8 pi) = 1/(32 pi) at kappa=1/2")
H0 = 67.36e3/3.0857e22; OL = 0.6889
rho_L = OL*3*H0**2/(8*np.pi*G)
ratio = uF/(rho_L*C**2)
ok(abs(ratio*32*np.pi - 1) < 0.05,
   f"C9g  numeric: u_F/rho_DE = {ratio:.4f} = 1/{1/ratio:.1f} (= 1/(32 pi) = 1/{32*np.pi:.1f})",
   "the entire MOND sector is a dark-energy-scale Lagrangian Lambda_sc^4 F(X,Y)")

# ----------------------------------------------------------------- C10
head("C10 [DERIVED + numeric]  radiative status of eps")
# Y-term operator:  -(a0^2/(8 pi G)) eps A(X) Y = -[eps A(X) c^8/(8 pi G a0^2)] Rbar_ij Rbar^ij
# dimensionless (hbar-unit) curvature-squared coefficient: beta = eps A(X) c^7/(8 pi G hbar a0^2)
hb = sp.symbols('hbar', positive=True)
beta_over = c_**7/(8*sp.pi*G_*hb*a0_**2)
Mbar2c4 = hb*c_**5/(8*sp.pi*G_)                          # (Mbar_Pl c^2)^2
a0nat = hb*a0_/c_
ok(sp.simplify(beta_over - Mbar2c4/a0nat**2) == 0,
   "C10a  identity: c^7/(8 pi G hbar a0^2) = (Mbar_Pl c^2)^2/(hbar a0/c)^2")
beta_num = C**7/(8*np.pi*G*HBAR*A0**2)
ok(abs(beta_num/1.40e122 - 1) < 0.02,
   f"C10b  beta/(eps A) = {beta_num:.3e}  (~1.4e122)")
A1 = 1.0/16.0                                            # A(1) = 1/16 (verified in repo)
beta_cap = eps_cap*A1*beta_num
info("C10c", f"at eps_cap and X=1: beta = {beta_cap:.2e} -- the Y-term is ~1e97 in hbar units,")
info("C10d", "i.e. eps is SMALL in a0-units but COLOSSAL in curvature-EFT units")
beta_loop = 1.0/(16*np.pi**2)                            # graviton/matter log-running, O(1) coeff
eps_loop = beta_loop/(A1*beta_num)
ok(eps_loop < 1e-120,
   f"C10e  loop-natural R^2 coefficient beta ~ 1/16pi^2 => eps_loop ~ {eps_loop:.1e}",
   f"= {eps_loop/eps_cap:.1e} x eps_cap: radiative corrections CANNOT destabilise eps")
# the same 1e122 unit mismatch applies to every analytic coefficient of the F-tower:
w_X2 = (Mbar_eV/a0_eV)**2                                # (a^2)^2 coefficient in hbar units
ok(abs(w_X2/beta_num - 1) < 1e-6,
   f"C10f  the (a.a)^2 coefficient (from -X^2/2) is the SAME (Mbar/a0)^2 = {w_X2:.2e}",
   "every analytic Wilson coefficient of the F-tower sits ~1e122 above its loop-natural size")
info("C10g", "eps -> 0 enhances NO symmetry (F(X,0) has the same FDiff x T-reflection x T-shift")
info("C10h", "invariance): eps is 't Hooft-UNNATURAL, merely stabilised by the weakness of gravity")

# ----------------------------------------------------------------- summary
head("SUMMARY")
n_ok = sum(PASS); n_all = len(PASS)
print(f"  {n_ok}/{n_all} checks passed")
print("""
  OPERATOR CENSUS (symmetries: spatial diffs + t -> f(t), parity, T-reflection
  [T -> -T, t -> -t: a_i, (3)R_ij even; K_ij odd], T-shift [T -> T + const]):

  order 2 (complete basis, 4 terms):  (3)R, K_ij K^ij, K^2, a_i a^i
      -> ALL PRESENT (1, 1, -lam_K, eta_K).  Generic.  D_i a^i redundant (C7).
  order 4, pure-potential, MISSING from the action:
      (3)R^2, Rbar_ij Rbar^ij alone (present ONLY dressed by eps A(X) ~ eps X^2:
      its coefficient VANISHES at a=0), (3)R a^2, R_ij a^i a^j, (D_i a^i)^2,
      D_i a_j D^i a^j, a^i D_i (3)R.
  order 4, K-sector (T-even), MISSING:
      K_ij K^ij (3)R, K K_ij Rbar^ij, K^2 (3)R, K^i_j K^j_k Rbar^k_i, K^2 a^2,
      K_ij K^ij a^2, (K_ij a^j)^2, and (Lie_u K_ij)^2 [4 time derivatives --
      allowed by FDiff; its absence is the 2nd-order-in-time ASSUMPTION, not a
      symmetry; no z=3 anisotropic scaling is present to make it irrelevant].
  order 6 (z=3, required for Horava-type power-counting renormalisability):
      ENTIRELY MISSING -> the action is a pure EFT below Lambda_sc, not a
      renormalisable khronometric theory.
  PRESENT beyond order 2: the infinite non-analytic tower |a|^3, |a|^5, ...,
      (a^2)^2, ... and (a^2-dressed) Rbar^2 -- an infinite set of Wilson
      coefficients locked to the 2-parameter family (a0, eps): a measure-zero
      trajectory in coefficient space, enforced by NO symmetry.
""")
ok(n_ok == n_all, "ALL CHECKS PASSED" if n_ok == n_all else "SOME CHECKS FAILED")
