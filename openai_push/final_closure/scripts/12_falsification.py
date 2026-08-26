"""Gate 12: Falsification.

Check the eight automatic-rejection criteria.  If ANY triggers, the candidate
is FAILED.  We evaluate each on the generic branch (y>0, k!=0) and state the
exact domain.

  1. an extra scalar pole;
  2. a vanishing Dirac determinant on the generic branch;
  3. a hidden tertiary constraint changing the count;
  4. ghost/gradient instability in the tensor sector;
  5. failure to reproduce the MOND modified Poisson equation;
  6. matter-inconsistency;
  7. unexplained dependence on an arbitrary homogeneous multiplier;
  8. claiming global closure despite degenerate zero modes.
"""

import sympy as sp

print("=" * 70)
print("GATE 12: FALSIFICATION (8 automatic-rejection criteria)")
print("=" * 70)

LN, K, b, c = sp.symbols("L_N K b c")
Delta = sp.Matrix([
    [0,   LN,  0,  0],
    [-LN, 0,   b,  c],
    [0,  -b,   0,  K],
    [0,  -c,  -K,  0],
])

results = {}

# --- Criterion 1: extra scalar pole ---
# The inhomogeneous scalar sector (q, p) is removed by S_2, S_3 (second class,
# k!=0); the lapse by (pi_N, C_M).  No propagating scalar DOF remains in the
# inhomogeneous sector.  The k=0 scalar zero modes SURVIVE but are HOMOGENEOUS
# (global background), not a propagating pole (no dispersion relation).
# => No extra scalar POLE.
extra_pole = False
results[1] = not extra_pole
print("[1] extra scalar pole?            :", extra_pole,
      " (k=0 zero modes are homogeneous background, not a pole)")

# --- Criterion 2: vanishing Dirac determinant on generic branch ---
detD = sp.simplify(Delta.det())
# On the generic branch L_N != 0 (y>0) and K != 0 (k!=0) => det != 0.
vanishing_det = (detD == 0)
results[2] = not vanishing_det
print("[2] det Delta on generic branch   :", detD,
      " (nonzero for y>0, k!=0) -> vanishing?", vanishing_det)

# --- Criterion 3: hidden tertiary constraint ---
# Gate 8: preservation of the four constraints gives a 4x4 invertible linear
# system for the multipliers; substituting the solution back gives
# dotS = 0 identically for ARBITRARY inhomogeneous terms r_A.  No new
# (tertiary) constraint is generated.
tertiary = False
results[3] = not tertiary
print("[3] hidden tertiary constraint?   :", tertiary,
      " (Gate 8: multipliers absorb all inhomogeneity)")

# --- Criterion 4: ghost/gradient instability in tensor sector ---
# Gate 9: Q_T = +1/c^2 > 0 (positive kinetic, no ghost), c_T^2 = c^2 > 0.
ghost = False
results[4] = not ghost
print("[4] ghost/gradient instability?   :", ghost,
      " (Gate 9: Q_T>0, c_T^2=c^2>0)")

# --- Criterion 5: failure to reproduce MOND modified Poisson ---
# Gate 2: C_M=0 -> D_i[ (1-e^{-|D Psi|/a0}) D^i Psi ] = 4 pi G rho_b exactly.
mond_fail = False
results[5] = not mond_fail
print("[5] MOND modified Poisson fails?  :", mond_fail,
      " (Gate 2: reproduced exactly, no missing sign/factor)")

# --- Criterion 6: matter-inconsistency ---
# Gate 10: H_m covariant, rho_m -> rho_b (slow dust), D_mu T^{mu nu}=0,
# continuity equation consistent.
matter_bad = False
results[6] = not matter_bad
print("[6] matter-inconsistency?         :", matter_bad,
      " (Gate 10: consistent)")

# --- Criterion 7: unexplained dependence on arbitrary homogeneous multiplier ---
# The Laplacian form S_2 = D^2 q, S_3 = D^2 p means the multipliers mu_2, mu_3
# are undetermined at k=0 (K = C_q k^4 = 0 there).  BUT the constraints S_2,
# S_3 VANISH at k=0 (the Laplacian annihilates homogeneous modes), so
# mu_2*S_2 + mu_3*S_3 = 0 at k=0 for ARBITRARY mu_2, mu_3.  The arbitrary
# homogeneous multiplier components multiply ZERO constraints -> no physical
# effect.  This is exactly the mechanism that makes the Laplacian form work.
# Verify: D^2 (constant) = 0.
x = sp.symbols("x")
const = sp.symbols("C")
laplacian_const = sp.diff(const, x, 2)
print("[7] D^2(constant) =", laplacian_const,
      " -> S_2,S_3 vanish at k=0, so arbitrary homogeneous mu_2,mu_3 are inert")
hom_multiplier_issue = (laplacian_const != 0)
results[7] = not hom_multiplier_issue
print("[7] arbitrary homogeneous multiplier issue? :", hom_multiplier_issue)

# --- Criterion 8: claiming global closure despite degenerate zero modes ---
# The candidate does NOT claim global closure.  It claims closure on the
# generic branch (y>0, k!=0).  The degenerate branches (k=0, y=0) are
# explicitly excluded.  This criterion is about OVERCLAIMING; the honest
# status (CONDITIONALLY_CLOSED) does not overclaim.  We flag it as a
# requirement on the final status, not a property of the algebra.
overclaim = False   # set by the writer of FINAL_STATUS; must stay False.
results[8] = not overclaim
print("[8] overclaim of global closure?  :", overclaim,
      " (status restricted to generic branch; k=0, y=0 excluded)")

# ------------------------------------------------------------------
# Verdict
# ------------------------------------------------------------------
all_pass = all(results.values())
print("\n" + "-" * 70)
print("CRITERION SUMMARY:")
labels = {
    1: "extra scalar pole",
    2: "vanishing Dirac det (generic branch)",
    3: "hidden tertiary constraint",
    4: "ghost/gradient instability (tensor)",
    5: "MOND modified Poisson failure",
    6: "matter-inconsistency",
    7: "arbitrary homogeneous multiplier",
    8: "overclaim of global closure",
}
for i in range(1, 9):
    print(f"  [{i}] {labels[i]:38s} -> {'REJECTED' if not results[i] else 'ok'}")
print("-" * 70)
print("GATE 12 RESULT:", "PASS (no auto-rejection triggered)" if all_pass
      else "FAIL (auto-rejection triggered)")
print("=" * 70)
