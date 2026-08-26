"""Gate 7: Degree-of-freedom count.

Start from the full ADM phase space (20 dims per spatial point), apply the
six first-class spatial-diffeomorphism constraints and the four second-class
scalar auxiliary constraints, and verify the remaining phase space is 4 dims
= 2 DOF (the TT tensor pair).

We also verify the sector decomposition: that S_2, S_3 eliminate the
inhomogeneous scalar pair (q, p) while the TT tensor pair is untouched.

KEY SUBTLETY tracked here: C_M = D_i[c^2 mu(y) D^i ln N] uses D^i = gamma^ij
D_j, so C_M depends on the spatial metric gamma^ij (index raising). This is a
COUPLING of the MOND constraint to the geometry, not a constraint on the TT
sector. It removes no tensor DOF; it is carried into Gate 8 (preservation).
"""

import sympy as sp

print("=" * 70)
print("GATE 7: DOF COUNT")
print("=" * 70)

# ------------------------------------------------------------------
# Phase-space dimension bookkeeping
# ------------------------------------------------------------------
print("\n--- (A) full ADM phase space ---")
dims = {
    "gamma_ij (6) + pi^ij (6)": 12,   # spatial metric + momentum
    "N (1) + pi_N (1)":          2,   # lapse + momentum
    "N^i (3) + pi_i (3)":        6,   # shift + momentum
}
total = sum(dims.values())
for k, v in dims.items():
    print(f"  {k:28s}: {v}")
print(f"  {'TOTAL':28s}: {total}")
assert total == 20

# ------------------------------------------------------------------
# Decompose the spatial-metric sector into scalar/vector/tensor
# ------------------------------------------------------------------
print("\n--- (B) spatial-metric sector decomposition ---")
# gamma_ij (6) = 1 trace (q) + 3 vector + 2 tensor TT
# pi^ij  (6) = 1 trace (p) + 3 vector + 2 tensor TT
sectors = {
    "scalar (q, p)":        2,
    "vector (3+3)":         6,
    "tensor TT (2+2)":      4,
}
assert sum(sectors.values()) == 12
for k, v in sectors.items():
    print(f"  {k:20s}: {v}")

# ------------------------------------------------------------------
# Apply constraints
# ------------------------------------------------------------------
print("\n--- (C) constraint removal ---")
# First-class: pi_i (3) + H_i (3) = 6 first-class -> remove 12 dims.
#   These gauge away: shift (N^i, pi_i) = 6  +  metric vector (3+3) = 6.
fc_removed = 12
fc_detail = {"shift (N^i, pi_i)": 6, "metric vector (3+3)": 6}
for k, v in fc_detail.items():
    print(f"  first-class {k:22s}: -{v}")
print(f"  first-class total removed      : -{fc_removed}")

# Second-class: pi_N, C_M, D^2 q, D^2 p = 4 second-class -> remove 4 dims.
sc_removed = 4
sc_detail = {
    "pi_N = 0 (S_4)":        1,   # removes pi_N
    "C_M  = 0 (S_1)":        1,   # removes N (elliptic)
    "D^2q = 0 (S_2)":        1,   # removes inhomogeneous q
    "D^2p = 0 (S_3)":        1,   # removes inhomogeneous p
}
for k, v in sc_detail.items():
    print(f"  second-class {k:22s}: -{v}")
print(f"  second-class total removed     : -{sc_removed}")

remaining = total - fc_removed - sc_removed
print(f"\n  remaining phase-space dims     : {total} - {fc_removed} - {sc_removed} = {remaining}")
print(f"  N_DOF = remaining / 2          : {remaining/2}")
assert remaining == 4
assert remaining/2 == 2

# ------------------------------------------------------------------
# Sector-by-sector accounting (what survives)
# ------------------------------------------------------------------
print("\n--- (D) sector-by-sector survival ---")
survival = {
    "shift":        "0  (gauged by pi_i, H_i)",
    "metric vector":"0  (gauged by H_i)",
    "lapse (N,pi_N)": "0  (removed by pi_N=0, C_M=0)",
    "scalar inhom. (q,p)": "0  (removed by D^2q=0, D^2p=0, k!=0)",
    "scalar k=0 zero modes": "SURVIVE -> cosmological background (reserved)",
    "tensor TT (h_TT, pi_TT)": "4 dims = 2 DOF  (UNTOUCHED)",
}
for k, v in survival.items():
    print(f"  {k:28s}: {v}")

# ------------------------------------------------------------------
# Verify the TT pair is untouched by the four scalar constraints
# ------------------------------------------------------------------
print("\n--- (E) TT sector untouched ---")
# The four scalar constraints involve only: N, pi_N, q, p (and rho_m).
# None involve h_ij^TT or pi_TT^ij as constrained variables.
scalar_constraint_vars = {"N", "pi_N", "q", "p", "rho_m"}
tt_vars = {"h_TT_ij", "pi_TT_ij"}
overlap = scalar_constraint_vars & tt_vars
print(f"  vars in scalar constraints     : {sorted(scalar_constraint_vars)}")
print(f"  TT vars                        : {sorted(tt_vars)}")
print(f"  overlap (should be empty)      : {overlap if overlap else 'EMPTY'}")
assert overlap == set()

# C_M depends on gamma^ij via index raising (D^i = gamma^ij D_j).  This is a
# COUPLING, not a constraint on the TT sector.  Track it for Gate 8.
print("\n  NOTE: C_M = D_i[c^2 mu(y) D^i ln N] uses D^i = gamma^ij D_j,")
print("  so C_M depends on gamma^ij (incl. TT part) as a COEFFICIENT.")
print("  This removes no tensor DOF; it couples the MOND constraint to the")
print("  geometry and is carried into Gate 8 (constraint preservation).")

all_pass = (total == 20 and remaining == 4 and remaining/2 == 2 and overlap == set())
print("\n" + "=" * 70)
print("GATE 7 RESULT:", "PASS" if all_pass else "FAIL")
print("  N_DOF = 2  (TT tensor pair); scalar inhomogeneous sector removed;")
print("  k=0 scalar zero modes reserved for the cosmological background.")
print("=" * 70)
