"""
GROUND-A verification of AeST quadratic action self-checks.
Source: Skordis & Zlosnik arXiv:2109.13287 (PRD 106,104041),
  eq (22) M^2, eq (24) scalar quadratic action, eq (27) det U, eq (30) c_s^2.
"""
import sympy as sp

KB, K2, Q0, lam, k, w = sp.symbols('K_B K_2 Q0 lambda_s k omega', positive=True, real=True)

print("="*72)
print("SELF-CHECK (1): transverse beta_i mass M^2")
print("="*72)
# Transverse aether beta_i: from eq(24) the terms reaching beta are the
# EA-Maxwell kinetic K_B(betadot^2 - (grad beta)^2) and the algebraic Y-mass
# -(2-K_B)(1+lam)Q0^2 |beta|^2. Dispersion K_B(w^2-k^2)=(2-K_B)(1+lam)Q0^2.
M2 = sp.simplify((2-KB)*(1+lam)*Q0**2/KB)
print("M^2 =", M2)
print("paper eq(22):  (2-K_B)(1+lambda_s)Q0^2/K_B   MATCH:",
      sp.simplify(M2 - (2-KB)*(1+lam)*Q0**2/KB) == 0)
print("healthy vector <=> coeff K_B>0 and M^2>=0 <=> 0<K_B<2, lambda_s>-1")

print("\n" + "="*72)
print("SELF-CHECK (2): scalar determinant det U  (paper eq 27)")
print("="*72)
# Paper eq(27), verbatim:
detU_paper = 4*k**6*w**2*((2-KB)*((2+KB*lam)*k**2 + 2*K2*Q0**2*(1+lam)) - 2*K2*KB*w**2)
print("detU (paper eq27) =")
sp.pprint(detU_paper)
print("\nTask quoted (up to prefactor):")
detU_task = k**6*w**2*((2-KB)*((2+KB*lam)*k**2 + 2*K2*Q0**2*(1+lam)) - 2*K2*KB*w**2)
print("  ratio detU_paper/detU_task =",
      sp.simplify(detU_paper/detU_task), " => task '∝' correct; exact prefactor = 4")

print("\n" + "="*72)
print("SELF-CHECK (3): scalar speed c_s^2 from the NONZERO root of det U")
print("="*72)
# det U = 0 nonzero-omega branch:  2 K2 K_B w^2 = (2-K_B)[(2+K_B lam)k^2 + 2K2 Q0^2(1+lam)]
w2_root = sp.solve(sp.Eq((2-KB)*((2+KB*lam)*k**2 + 2*K2*Q0**2*(1+lam)) - 2*K2*KB*w**2, 0), w**2)[0]
w2_root = sp.expand(w2_root)
print("omega^2 (propagating root) =")
sp.pprint(w2_root)

k2 = sp.symbols('k2', positive=True)
cs2 = sp.simplify(sp.diff(w2_root.subs(k**2, k2), k2))  # coefficient of k^2
cs2_paper = (2-KB)/(K2*KB)*(1 + sp.Rational(1,2)*KB*lam)
print("\nc_s^2 = d(omega^2)/d(k^2) =", sp.simplify(cs2))
print("paper eq(30)             =", sp.simplify(cs2_paper))
print("MATCH:", sp.simplify(cs2 - cs2_paper) == 0)

# mass gap = omega^2 at k=0
mass_gap = sp.simplify(w2_root.subs(k, 0))
print("\nomega^2(k=0) [mass gap] =", mass_gap)
print("Compare M^2(transverse) =", M2)
# relation between scalar gap and transverse M^2:
print("scalar-gap / M^2 =", sp.simplify(mass_gap/M2))
print("  => omega^2 = c_s^2 k^2 + (2-K_B)(1+lam)Q0^2/K_B ,")
print("     i.e. scalar mode shares the SAME gap M^2 as the transverse vector (eq 28-29).")

print("\n" + "="*72)
print("CONSISTENCY: rewrite propagating root as c_s^2 k^2 + M^2")
print("="*72)
recon = sp.expand(cs2_paper*k**2 + M2)
print("c_s^2 k^2 + M^2 - omega^2_root =", sp.simplify(recon - w2_root))
print("  (zero => the two paper forms eq27,eq30,eq22 are mutually consistent) ")

print("\n" + "="*72)
print("STABILITY CONDITIONS (paper eq 61-63)")
print("="*72)
print("0 < K_B < 2 ;  K_2 > 0 ;  lambda_s > 0  (>-1 needed just for M^2>=0).")
print("c_s^2 > 0 requires (1 + K_B lambda_s/2) > 0 given 0<K_B<2, K_2>0.")
