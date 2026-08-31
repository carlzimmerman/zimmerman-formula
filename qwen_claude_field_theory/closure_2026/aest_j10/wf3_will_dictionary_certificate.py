#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_will_dictionary_certificate.py  (STEP 0 gate for the eta_K solve)
=====================================================================
Sympy certificate of the Will preferred-frame extraction dictionary used by
wf3_base_aest_eta_K_solve.py, replacing the (documented-wrong) dictionaries in
fc_alpha2_preferred_frame_2026.py / route2_v2_build.py / route2_v2_extract.py.

Will (TEGP / Living Rev 17:4 eq 27), mostly-plus, point source AT REST in the
PPN frame, PPN frame moving with velocity w^i relative to the preferred frame
(so V_i = W_i = 0):
  g00 pf-sector = -(a1 - a2 - a3) w^2 U - a2 w^i w^j U_ij
  g0i pf-sector = -(1/2)(a1 - 2 a2) w_i U - a2 w^j U_ij
Certificates produced here:
  (C1) point-source identity U_ij = d_i d_j chi + delta_ij U with chi = -m r,
       U = m/r  (hence Fourier: chi_hat = 2 U_hat/q^2,
       U_ij_hat = delta_ij U_hat - 2 q_i q_j U_hat / q^2).
  (C2) with k = xhat, w = (w1, w2, 0):
       [g00] coeff(w2^2 U) = -a1 + a3          (perp)
             coeff(w1^2 U) = -a1 + 2 a2 + a3   (par)
        =>  a2 = (par - perp)/2   (alpha_3-blind)
            a3 = perp + a1        (must certify to 0 for a semiconservative theory)
      [g0i] transverse (i=2): coeff(w2 U) = -a1/2  =>  a1 = -2*coeff
            parallel  (i=1): coeff(w1 U) = -a1/2 + 2 a2
All statements are sympy identities, printed.
"""
import sympy as sp

m, r = sp.symbols('m r', positive=True)
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
a1, a2, a3 = sp.symbols('alpha_1 alpha_2 alpha_3', real=True)
w1, w2 = sp.symbols('w1 w2', real=True)
Uh = sp.Symbol('U_hat')

print("="*74)
print("C1: point-source superpotential identity U_ij = chi_,ij + delta_ij U")
print("="*74)
R = sp.sqrt(x1**2 + x2**2 + x3**2)
U = m/R
chi = -m*R
X = [x1, x2, x3]
ok = True
for i in range(3):
    for j in range(3):
        Uij = m*X[i]*X[j]/R**3                      # definition (point source)
        rhs = sp.diff(chi, X[i], X[j]) + (U if i == j else 0)
        d = sp.simplify(Uij - rhs)
        ok = ok and (d == 0)
print("  U_ij - (chi_,ij + delta_ij U) == 0 for all i,j :", ok)
lap_chi = sp.simplify(sum(sp.diff(chi, v, v) for v in X) + 2*U)
print("  laplacian(chi) + 2U == 0 :", lap_chi == 0)
print("  => Fourier: U_ij_hat = delta_ij U_hat - 2 q_i q_j U_hat/q^2")

print()
print("="*74)
print("C2: coefficient table with k = xhat  (U_11 -> -U_hat, U_22=U_33 -> +U_hat)")
print("="*74)
# Fourier U_ij with q = (q,0,0):
Uij_hat = lambda i, j: (sp.KroneckerDelta(i, j) - 2*(i == 1)*(j == 1))*Uh
w = {1: w1, 2: w2, 3: 0}
# g00 sector
g00 = -(a1 - a2 - a3)*(w1**2 + w2**2)*Uh - a2*sum(
    w[i]*w[j]*Uij_hat(i, j) for i in (1, 2, 3) for j in (1, 2, 3))
g00 = sp.expand(g00)
cpar = g00.coeff(w1**2).coeff(Uh)
cperp = g00.coeff(w2**2).coeff(Uh)
print("  [g00] coeff(w_par^2  U) =", cpar, "  (claim: -a1+2a2+a3)",
      sp.simplify(cpar - (-a1 + 2*a2 + a3)) == 0)
print("  [g00] coeff(w_perp^2 U) =", cperp, " (claim: -a1+a3)",
      sp.simplify(cperp - (-a1 + a3)) == 0)
print("  => ALPHA_2 = (par - perp)/2 :",
      sp.simplify((cpar - cperp)/2 - a2) == 0, "  (alpha_3-blind)")
print("  => ALPHA_3 = perp + alpha_1 :",
      sp.simplify(cperp + a1 - a3) == 0)
# g0i sector
for i, lab in ((2, 'transverse'), (1, 'parallel')):
    g0i = -sp.Rational(1, 2)*(a1 - 2*a2)*w[i]*Uh - a2*sum(
        w[j]*Uij_hat(i, j) for j in (1, 2, 3))
    c = sp.expand(g0i).coeff(w[i]).coeff(Uh)
    print(f"  [g0{i}] {lab:10s}: coeff(w{i} U) =", c)
print("  => ALPHA_1 = -2 * (transverse g0i coeff)   [Will-normalized]")
print()
print("NOTE (w-sign): in the solve pipeline the AETHER background is boosted")
print("(A^i_bg = wb w^i) while the source sits at rest in the coordinates, i.e.")
print("the PPN frame moves at w_Will = -wb*w relative to the preferred frame.")
print("Odd-in-w structures (alpha_1 g0i) therefore flip sign relative to a naive")
print("w_Will = +wb*w reading. The pure-EA control (wf3_pure_ea_control_build.py)")
print("fixes this orientation empirically against Foster-Jacobson.")
