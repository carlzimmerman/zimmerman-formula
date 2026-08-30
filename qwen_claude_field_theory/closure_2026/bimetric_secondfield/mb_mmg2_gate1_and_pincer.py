#!/usr/bin/env python3
"""MB-MMG-2 (slip-constrained MMG): Gate 1 (Dirac rank) at principal-symbol level, + the decisive point
that Gate 1 passing does NOT save it (alpha_3), + the terminal single-metric PINCER."""
import sympy as sp

print("=== GATE 1: principal-symbol Dirac rank of the NEW scalar constraint set {P_s, C_M, D^2 s, C_P} ===")
# variables: independent (s, q); phi = s - q; P_s conjugate to s. C_M depends on phi=s-q (so on s).
# Fourier symbol k; L = linearized MOND operator symbol {P_s,C_M}; c={D^2s,C_P}!=0 by construction;
# b={C_M,C_P}; a={P_s,C_P}. Determinable: {P_s,C_M}=-L, {P_s,D^2s}=-k^2 (D^2s depends on s), {C_M,D^2s}=0
# (both config-only in s,q). NOTE the NEW cross term {P_s,D^2s}=-k^2 that the OLD block-diagonal lacked.
L, k, a, b, cc = sp.symbols('L k a b c', positive=True)
Delta = sp.Matrix([
    [0,   -L,   -k**2, -a],
    [L,    0,    0,    -b],
    [k**2, 0,    0,    -cc],
    [a,    b,    cc,    0]])
# Pfaffian of a 4x4 antisymmetric: Pf = D12 D34 - D13 D24 + D14 D23
Pf = Delta[0,1]*Delta[2,3] - Delta[0,2]*Delta[1,3] + Delta[0,3]*Delta[1,2]
Pf = sp.simplify(Pf)
det = sp.simplify(Delta.det())
print("  Pf(Delta_MB) =", Pf, "   (det = Pf^2 =", sp.factor(det), ")")
print("  => rank 4 (det != 0)  GENERICALLY, i.e. UNLESS the fine-tuned degeneracy L*c = k^2*b holds.")
print("  So Gate 1 PLAUSIBLY PASSES: MB-MMG-2 is a consistent 2-DOF theory at principal-symbol level")
print("  (20-12-4=4 => N_grav=2), inheriting the SAME uncertified {D^2 s, H_i} momentum-bracket caveat")
print("  the old theory had (committed audit Part 0.6: {D^2 q, H_i} !=0 at q=0, count asserted not proven).")
print("  Honest scope: b,c need the FULL nonlinear H_0 to pin down; principal symbol only shows genericity.")

print("\n=== BUT GATE 1 PASSING DOES NOT SAVE IT: the omitted gate is alpha_3 (sympy-verified separately) ===")
print("  Carl's 3 gates {rank, slip, MOND} OMIT the PPN/alpha_3 gate. MB-MMG-2 keeps C_M untouched, and")
print("  alpha_3 is set by C_M's g_00 Phi_1 coefficient = 1 (elliptic/instantaneous), NOT by the spatial")
print("  slip sector. Slip repair gives gamma:0->1, alpha_1:4->0, but alpha_3: -1 -> -3 (still O(1)).")
print("  |alpha_3| < 4e-20 (pulsar) violated ~7.5e19x. => MB-MMG-2 EXCLUDED regardless of Gate 1.")

print("\n=== THE TERMINAL SINGLE-METRIC PINCER (both horns now closed) ===")
print("  A single physical metric must carry MOND either by a PROPAGATING scalar or by a CONSTRAINT:")
print("  HORN 1 (frame-free propagating scalar): DC-013 slip-lock -- diff-invariance locks (Phi,Psi) to the")
print("          (1,-2) ray => eta!=1 => CANNOT lens; and P7 -- the screening e^-y that protects PPN kills")
print("          the kinetic normalization => strong coupling. CLOSED.")
print("  HORN 2 (preferred-frame elliptic CONSTRAINT = constraint-first MMG, incl. slip-repaired MB-MMG-2):")
print("          CAN lens (slip repairable, Gate 2 pass; Gate 1 rank-4 plausible) BUT the elliptic")
print("          (instantaneous, action-at-a-distance) MOND constraint forces alpha_3 = O(1) (momentum")
print("          non-conservation) => pulsar-excluded ~7.5e19x. CLOSED.")
print("  The two horns are EXHAUSTIVE: alpha_3=0 <=> retarded/hyperbolic MOND sector <=> a propagating field")
print("  <=> HORN 1 (DC-013/P7). So a single metric CANNOT simultaneously give MOND + lensing + alpha_3=0.")
print("  EXIT = second metric => DC-018 (non-derivative bimetric can't give MOND 1/r) + BD ghost (derivative")
print("  bimetric revives the 6th mode). The whole class is a closed pincer; the only genuinely-open door is")
print("  the ghost-free-tuned derivative-bimetric subspace (NOT yet shown to keep BOTH MOND and a dynamical")
print("  2nd metric).")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"mb-mmg2-gate1-and-pincer",
  "status":"MB-MMG-2 Gate1 plausibly PASS (rank-4) but EXCLUDED by alpha_3; single-metric PINCER closed both horns",
  "certificate":("Gate 1 principal-symbol: Pf(Delta_MB) = L*c - k^2*b (det=Pf^2), so the new scalar constraint "
    "set {P_s,C_M,D^2s,C_P} is rank-4 (N_grav=2) GENERICALLY (unless the fine-tuned degeneracy L c = k^2 b), "
    "inheriting the old theory's uncertified {D^2s,H_i} caveat. So MB-MMG-2 is plausibly a consistent 2-DOF "
    "theory AND passes Gate 2 (slip: gamma 0->1) and Gate 3 (MOND). BUT it is EXCLUDED by the OMITTED gate: "
    "alpha_3 = O(1) (=-3 after the slip repair) because C_M's elliptic/instantaneous g_00 Phi_1 coefficient=1 "
    "is untouched by the spatial slip sector; pulsar bound 4e-20 violated ~7.5e19x (momentum non-conservation). "
    "TERMINAL PINCER: a single metric carries MOND by a PROPAGATING scalar (HORN 1: DC-013 slip-lock can't "
    "lens + P7 kinetic-norm collapse) OR by an elliptic CONSTRAINT (HORN 2: lenses but alpha_3=O(1) "
    "preferred-frame). The horns are exhaustive (alpha_3=0 <=> retarded <=> propagating <=> HORN 1). So no "
    "single metric gives MOND+lensing+alpha_3=0. EXIT=2nd metric => DC-018 (non-derivative can't MOND) + BD "
    "ghost (derivative revives 6th mode). Only open door: ghost-free-tuned derivative-bimetric subspace."),
  "numeric_values":{"Pf_Delta_MB":"L*c - k^2*b (rank-4 generic)","N_grav":2,"gamma":"0->1","alpha_1":"4->0",
    "alpha_3":"-1->-3 (O(1), pulsar 7.5e19x)","horns":"propagating=DC-013/P7 ; elliptic-constraint=alpha_3"}}))
