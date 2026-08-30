#!/usr/bin/env python3
"""Does the slip-constrained MMG (replace D^2 q=0 by D^2 s=0, s=phi+q=(Phi-Psi)/c^2; C_M UNTOUCHED) survive?
Gate 2 (slip) passes (gamma->1). Gate 3 (MOND) passes (unchanged). DECISIVE: does alpha_3 survive?
alpha_3 is set by the g_00 Phi_1 (kinetic-energy potential) coefficient, which C_M fixes at 1 (vs GR's 4)
via its ELLIPTIC (instantaneous) response. The slip repair only touches the SPATIAL sector => the g_00
Phi_1 coefficient stays 1 => re-solve the PPN dictionary at gamma=1 and read alpha_3. Standard PPN
(Will): g_00 ⊃ (2 gamma + 2 + alpha_3 + zeta_1 - 2 xi) Phi_1 ;  GR = 4.  g_0i V-coeff = -(1/2)(4 gamma
+ 3 + alpha_1 - alpha_2 + zeta_1 - 2 xi)."""
import sympy as sp
gamma, beta, a1, a2, a3, z1, z2, z3, z4, xi = sp.symbols('gamma beta alpha_1 alpha_2 alpha_3 zeta_1 zeta_2 zeta_3 zeta_4 xi')

# committed audit invariants (chassis structure, set by C_M + lapse law + momentum constraint):
Phi1_coeff_g00 = 2*gamma + 2 + a3 + z1 - 2*xi     # standard PPN coefficient of Phi_1 in g_00
V_coeff_g0i    = -sp.Rational(1,2)*(4*gamma + 3 + a1 - a2 + z1 - 2*xi)
W_coeff_g0i    = -sp.Rational(1,2)*(1 + a2 - z1 + 2*xi)

# The chassis (C_M elliptic) FIXES, independent of the spatial constraint:
#   g_00 Phi_1 coefficient = 1  (audit Part 1.4; = the instantaneous kinetic-energy response),
#   g_0i = -(7/2) V - (1/2) W    (audit Part 3.4d), and alpha_2 = 0 (audit 4.3).
chassis = [sp.Eq(Phi1_coeff_g00, 1), sp.Eq(V_coeff_g0i, sp.Rational(-7,2)),
           sp.Eq(W_coeff_g0i, sp.Rational(-1,2)), sp.Eq(a2, 0)]

print("=== CURRENT chassis (D^2 q=0 => gamma=0), reproduce the committed audit ===")
sol0 = sp.solve(chassis + [sp.Eq(gamma, 0)], [a1, a3, z1, xi], dict=True)
print("  ", sol0, "   (audit: alpha_1=4, alpha_3=-1, zeta_1=2xi)")

print("\n=== SLIP-REPAIRED chassis (D^2 s=0 => gamma=1), g_00 Phi_1 coeff STILL 1 (C_M untouched) ===")
sol1 = sp.solve(chassis + [sp.Eq(gamma, 1)], [a1, a3, z1, xi], dict=True)
print("  ", sol1)
# read alpha_3
for s in sol1:
    print(f"   => gamma=1 (slip fixed), alpha_1={s.get(a1)}, alpha_3={s.get(a3)}  [alpha_2=0]")

print("\n=== robustness: can alpha_3 be tuned to ~0 while keeping g_00 Phi_1 coeff=1 at gamma=1? ===")
# 2*1 + 2 + a3 + z1 - 2 xi = 1  => a3 = -3 - z1 + 2 xi. To get a3~0 need z1 - 2 xi ~ -3.
a3_expr = sp.solve(sp.Eq(2*1 + 2 + a3 + z1 - 2*xi, 1), a3)[0]
print("   alpha_3 =", a3_expr, "  => alpha_3 ~ 0 needs (zeta_1 - 2 xi) ~ -3")
print("   but |zeta_1| < ~2e-2 and |xi| < ~1e-3 (solar-system bounds) => zeta_1-2xi cannot reach -3")
print("   => alpha_3 = O(1) ROBUSTLY. Bound |alpha_3| < 4e-20 violated by ~7.5e19 x.")

print("\n=== VERDICT: slip-constrained MMG ===")
print("Gate 2 (slip):   PASS -- D^2 s=0 => nabla^2(Phi-Psi)=0 => Phi=Psi => gamma_PPN: 0 -> 1. (verified)")
print("Gate 3 (MOND):   PASS -- C_M untouched => g = sqrt(GM a0)/r. (unchanged)")
print("BONUS:           alpha_1: 4 -> 0 (the alpha_1=4 was a gamma=0 artifact; the slip repair fixes it too).")
print("SURVIVING WALL:  alpha_3 = -3 (O(1)) -- because it is set by the g_00 Phi_1 coefficient = 1, fixed by")
print("                 the ELLIPTIC (instantaneous) C_M, which the slip repair does NOT touch. Pulsar bound")
print("                 |alpha_3| < 4e-20 violated ~7.5e19 x. alpha_3 != 0 = momentum non-conservation /")
print("                 self-accelerating binaries = the PREFERRED-FRAME liability, intrinsic to C_M.")
print("STRUCTURAL DILEMMA: the elliptic constraint that gives the CLEAN MOND eq + 2 DOF is EXACTLY what")
print("                 makes the lapse respond instantaneously (action-at-a-distance) => alpha_3 != 0.")
print("                 Removing alpha_3 needs a RETARDED/hyperbolic (propagating) sector => a dynamical")
print("                 scalar => back under DC-013 slip-lock (frame-free can't lens) / P7 (screening kills")
print("                 the kinetic norm). Can't have instantaneous-MOND AND alpha_3=0.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"mmg-slip-alpha3-survival",
  "status":"slip-constrained MMG: Gate2/Gate3 PASS, but alpha_3=O(1) SURVIVES => not viable",
  "certificate":("The proposed slip-constrained MMG (replace D^2 q=0 by D^2 s=0, s=phi+q=(Phi-Psi)/c^2; keep "
    "C_M) PASSES Gate 2 (nabla^2(Phi-Psi)=0 => Phi=Psi => gamma_PPN 0->1, verified) and Gate 3 (MOND unchanged), "
    "and even repairs alpha_1 (4->0, a gamma=0 artifact). BUT alpha_3 SURVIVES: it is set by the g_00 Phi_1 "
    "(kinetic-energy) coefficient = 1 (vs GR's 4), fixed by the ELLIPTIC/instantaneous C_M which the spatial "
    "slip repair does not touch. Re-solving the PPN dictionary at gamma=1 with that coefficient held gives "
    "alpha_3=-3 (was -1); alpha_3=0 would need zeta_1-2xi=-3, impossible under |zeta_1|<2e-2,|xi|<1e-3 => "
    "alpha_3=O(1) robustly, violating |alpha_3|<4e-20 by ~7.5e19x (momentum non-conservation). STRUCTURAL: "
    "the elliptic constraint giving clean MOND+2DOF IS the instantaneous (action-at-a-distance) response that "
    "forces alpha_3!=0; a retarded/propagating fix returns to DC-013/P7. The slip was never the real wall -- "
    "alpha_3 (preferred-frame, intrinsic to the elliptic MOND constraint) is."),
  "numeric_values":{"gamma_current":0,"gamma_repaired":1,"alpha_1_current":4,"alpha_1_repaired":0,
    "alpha_3_current":-1,"alpha_3_repaired":-3,"alpha_3_bound":"4e-20","violation":"~7.5e19x"}}))
