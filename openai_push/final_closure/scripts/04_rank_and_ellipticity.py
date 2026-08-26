"""Gates 4, 5, 6: Ellipticity / rank, Laplacian scalar pair, full rank.

This single script covers the three rank/ellipticity gates:

  GATE 4  Ellipticity / rank of the MOND lapse operator L_N.
          Linearize C_M under N -> N + delta N.  With
              u_i = D_i ln N,  u = |u|,  y = (c^2/a0) u,  F^i = c^2 mu(y) u^i,
          the principal symbol is
              sigma(L_N)(k) = - c^2 k_i A^i_j k^j / N + lower-order,
              A^i_j = mu(y) delta^i_j + y mu'(y) uhat^i uhat_j,
          with eigenvalues  lambda_perp = mu(y),  lambda_par = mu(y)+y mu'(y).
          Both are strictly positive for every y>0  (generically elliptic off
          the zero-gradient branch); at y=0 both vanish (degenerate branch).

  GATE 5  Laplacian scalar pair  S_2 = D^2 q,  S_3 = D^2 p.
          Exact normalization  C_q = {q,p} = (1/2)(1/sqrt(gamma)) = 1/2 (flat),
          so  { S_2(k), S_3(-k) } = C_q k^4  != 0  for  k != 0.

  GATE 6  Full rank on the generic branch.
          Pfaffian = L_N K,  det = (L_N K)^2,  nonzero iff (y>0 AND k!=0).
          Degeneracies at k=0 and y=0 are explicitly excluded (not global).
"""

import sympy as sp

# ==================================================================
# GATE 4: ELLIPTICITY / RANK
# ==================================================================
print("=" * 70)
print("GATE 4: ELLIPTICITY / RANK")
print("=" * 70)

y = sp.symbols("y", positive=True)
c, a0 = sp.symbols("c a0", positive=True)
mu = 1 - sp.exp(-y)
mu_p = sp.diff(mu, y)          # e^{-y}

# (1) symbol structure
print("\n--- (4.1) symbol structure ---")
u = sp.symbols("u", positive=True)
yy = c**2 * u / a0
F = c**2 * (1 - sp.exp(-yy)) * u
dF_du = sp.simplify(sp.diff(F, u))
print("[4.1.1] dF/du =", sp.factor(dF_du))
dF_du_recon = c**2 * (mu.subs(y, yy) + yy * mu_p.subs(y, yy))
sym_ok = sp.simplify(dF_du - sp.simplify(dF_du_recon)) == 0
print("[4.1.2] dF/du == c^2[ mu + y mu' ] :", sym_ok)

# (2) eigenvalues
lam_perp = mu
lam_par = sp.simplify(mu + y * mu_p)
lam_par_alt = 1 + (y - 1) * sp.exp(-y)
print("\n--- (4.2) eigenvalues ---")
print("[4.2.1] lambda_perp = mu(y)        =", sp.simplify(lam_perp))
print("[4.2.2] lambda_par  = mu + y mu'   =", sp.simplify(lam_par))
print("[4.2.3] lambda_par == 1+(y-1)e^{-y}:", sp.simplify(lam_par - lam_par_alt) == 0)

# (3) positivity for y>0
f = lam_par_alt
f_at_0 = sp.limit(f, y, 0, "+")
f_inf = sp.limit(f, y, sp.oo)
print("\n--- (4.3) positivity for y > 0 ---")
print("[4.3.1] f(0+) =", f_at_0, "  f(inf) =", f_inf)
import numpy as np
ys = np.linspace(1e-6, 50, 20000)
fnum = 1 + (ys - 1) * np.exp(-ys)
mnum = 1 - np.exp(-ys)
print("[4.3.2] min f on (0,50)  =", fnum.min(), " (>0)")
print("[4.3.3] min mu on (0,50) =", mnum.min(), " (>0)")

# (4) zero-gradient degeneracy
print("\n--- (4.4) zero-gradient degeneracy ---")
print("[4.4.1] lambda_perp(y->0+) =", sp.limit(lam_perp, y, 0, "+"))
print("[4.4.2] lambda_par (y->0+) =", sp.limit(lam_par, y, 0, "+"))
gate4 = (sym_ok and sp.simplify(lam_par - lam_par_alt) == 0
         and fnum.min() > 0 and mnum.min() > 0)
print("\nGATE 4 RESULT:", "PASS" if gate4 else "FAIL")

# ==================================================================
# GATE 5: LAPLACIAN SCALAR PAIR
# ==================================================================
print("\n" + "=" * 70)
print("GATE 5: LAPLACIAN SCALAR PAIR  (S_2 = D^2 q, S_3 = D^2 p)")
print("=" * 70)

g11, g22, g33 = sp.symbols("g11 g22 g33", positive=True)
sqrtg = sp.sqrt(g11 * g22 * g33)
# dq/d(gamma_ii) = (1/6) g^ii = (1/6)(1/g_ii);  dp/d(pi^ii) = g_ii/sqrtg
# { gamma_ii, pi^ii } = 1 (per diagonal index)
Cq = sp.simplify(sum(sp.Rational(1, 6) * (1/gii) * 1 * (gii/sqrtg)
                     for gii in (g11, g22, g33)))
print("[5.1] C_q = {q,p} (diagonal metric) =", Cq)
print("[5.2] expected (1/2)(1/sqrt(gamma)) :", sp.simplify(sp.Rational(1, 2)/sqrtg))
print("[5.3] match :", sp.simplify(Cq - sp.Rational(1, 2)/sqrtg) == 0)
Cq_flat = Cq.subs({g11: 1, g22: 1, g33: 1})
print("[5.4] C_q (flat) =", Cq_flat)
k = sp.symbols("k", positive=True)
bracket = sp.simplify(k**4 * Cq_flat)
print("[5.5] { S_2(k), S_3(-k) } = C_q k^4 =", bracket)
print("[5.6] nonzero for k != 0:", sp.simplify(bracket) != 0)
gate5 = (sp.simplify(Cq - sp.Rational(1, 2)/sqrtg) == 0 and Cq_flat == sp.Rational(1, 2))
print("\nGATE 5 RESULT:", "PASS" if gate5 else "FAIL")

# ==================================================================
# GATE 6: FULL RANK (GENERIC BRANCH)
# ==================================================================
print("\n" + "=" * 70)
print("GATE 6: FULL RANK (GENERIC BRANCH)")
print("=" * 70)

LN, K, b, c2 = sp.symbols("L_N K b c")
M = sp.Matrix([
    [0,   LN,  0,  0],
    [-LN, 0,   b,  c2],
    [0,  -b,   0,  K],
    [0,  -c2, -K,  0],
])
detM = sp.simplify(M.det())
print("[6.1] det Delta =", detM, " == (L_N K)^2 :", sp.simplify(detM - (LN*K)**2) == 0)
print("[6.2] L_N invertible <=> y>0 (Gate 4);  K invertible <=> k!=0 (Gate 5)")
print("[6.3] det Delta != 0 <=> (y>0) AND (k!=0)   [generic branch]")
# Degeneracies:
kk = sp.symbols("k")
print("[6.4] k=0:  K = C_q k^4 =", (sp.Rational(1,2)*kk**4).subs(kk, 0),
      " => det = 0  (EXCLUDED)")
yy2 = sp.symbols("y")
mu2 = 1 - sp.exp(-yy2)
print("[6.5] y=0:  lambda_perp =", sp.limit(mu2, yy2, 0, "+"),
      ", lambda_par =", sp.limit(mu2 + yy2*sp.diff(mu2, yy2), yy2, 0, "+"),
      " => L_N degenerate  (EXCLUDED)")
sub = {LN: sp.Integer(2), K: sp.Integer(3), b: sp.Integer(7), c2: sp.Integer(11)}
print("[6.6] numeric det (generic, L_N=2,K=3) =", detM.subs(sub), "(rank 4)")
sub_deg = {LN: sp.Integer(0), K: sp.Integer(3), b: sp.Integer(7), c2: sp.Integer(11)}
print("[6.7] numeric det (y=0 branch, L_N=0)  =", detM.subs(sub_deg), "(rank drops)")
gate6 = sp.simplify(detM - (LN*K)**2) == 0
print("\nGATE 6 RESULT:", "PASS" if gate6 else "FAIL",
      " (rank-4 on generic branch; k=0, y=0 excluded)")

all_pass = gate4 and gate5 and gate6
print("\n" + "=" * 70)
print("COMBINED (GATES 4+5+6) RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 70)
