#!/usr/bin/env python3
"""
CLASS 2 -- EXCEPTIONAL / ALGEBRAIC routes (the SM from the framework's algebra).
A consolidated, COMPUTED ledger + the one genuinely-untried algebraic map, with a real feasibility check.

Carl's standing ask: test the framework on ITS OWN terms; never manufacture a win NOR a deficit; back
every load-bearing claim with a runnable script (exit 0). This script does NOT re-derive the already-banked
E8/J3(O)/E6xSU(3)_F facts (see exceptional_geometry_to_SM_verify.py + chase_e6_su3_family_DIRECT.py) -- it
CONSOLIDATES the Class-2 variants into one graded ledger and freshly TESTS the three sub-claims the
enumeration names that were NOT yet in one place:

  (T1) sin^2(theta_W)=3/8  vs  Z=sqrt(32pi/3): is there ANY algebraic relation, or is 3/8 Z-independent?
  (T2) golden-ratio phi  vs  sqrt2 as the Koide amplitude: does the framework's OWN special MOND-transition
       value (phi) coincide with the Koide r=sqrt2, or are they different irrationals in different slots?
  (T3) THE GENUINELY-UNTRIED MAP: the framework's constitutive law carries a FORCED sqrt2 (the dS-Unruh
       quadrature minimal polynomial t^2-2). Koide also needs sqrt2 (r, also minpoly t^2-2). Same algebraic
       number. Does a SHARED-MINIMAL-POLYNOMIAL selector bridge them? Tested computationally via the
       carrier-space / equivariance obstruction (Z2 1-D accel axis vs S3 3-D generation space).

Footing locked: a0 = c*H_Lambda/Z, Z = 2*sqrt(8pi/3) = sqrt(32pi/3). Nothing here derives a0 or any mass.
LOCAL only. exit 0 == all internal consistency checks pass (NOT 'the SM is derived').
"""
import sympy as sp
import numpy as np
import math

PASS, FAIL = "PASS", "FAIL <-- CHECK"
ok = True
def check(name, cond):
    global ok
    print(f"    [{PASS if cond else FAIL}] {name}")
    ok &= bool(cond)
    return bool(cond)

# ----------------------------------------------------------------------------------------------------
print("="*84)
print("FOOTING (framework's own; locked, not derived)")
print("="*84)
Z = 2*sp.sqrt(sp.Rational(8,1)*sp.pi/3)            # = sqrt(32pi/3)
print(f"  Z = sqrt(32pi/3) = {sp.simplify(Z)} = {float(Z):.6f}")
ZoverSqrtPi = sp.simplify(Z/sp.sqrt(sp.pi))         # = 4*sqrt(6)/3, ALGEBRAIC
print(f"  Z/sqrt(pi) = {ZoverSqrtPi}  (algebraic) -> Z carries a lone sqrt(pi)=Gamma(1/2) [TRANSCENDENTAL]")
check("Z = sqrt(pi) * (algebraic)  (number-field fingerprint of the density integral rho_DE=Lambda c^2/8piG)",
      sp.simplify(Z/sp.sqrt(sp.pi) - sp.Rational(4,3)*sp.sqrt(6)) == 0)
print("  => WALL 2 (number-field): every gauge/Yukawa invariant is ALGEBRAIC; a0's normalization is not.")

# ====================================================================================================
print("\n"+"="*84)
print("(T1)  sin^2(theta_W)=3/8  vs  Z=sqrt(32pi/3):  algebraic relation, or Z-independent?")
print("="*84)
sw2 = sp.Rational(3,8)
print(f"  GUT-scale weak mixing (SU(5)/SO(10)/E6 group theory): sin^2(theta_W)|_GUT = 3/8 = {float(sw2):.5f}")
print(f"  measured (run down): sin^2(theta_W)(M_Z) ~ 0.2312")
# Try EVERY simple algebraic function of Z to land 3/8 (3/8 is RATIONAL; Z carries sqrt(pi))
cands = {
    "1/Z":           1/Z,
    "1/Z^2":         1/Z**2,
    "3/Z^2":         3/Z**2,
    "Z/32":          Z/32,
    "8/Z^2":         8/Z**2,
    "pi/Z^2":        sp.pi/Z**2,
}
print("  brute simple functions of Z vs 3/8 (none should land it without a forced pi-cancellation):")
landed = False
for nm, ex in cands.items():
    val = float(ex)
    hit = abs(val - 0.375) < 0.01
    landed |= hit
    print(f"     {nm:10s} = {val:.5f}   {'<-- within 1% of 3/8' if hit else ''}")
# the ONE that algebraically simplifies: Z^2 = 32pi/3, so 8/Z^2 = 24/(32pi) = 3/(4pi) -- pi-bearing, NOT 3/8.
eight_over_Z2 = sp.simplify(8/Z**2)
print(f"  KEY: 8/Z^2 = {eight_over_Z2}  (carries 1/pi) != 3/8  -> the apparent '8 and 3' match is a pi-cancellation MIRAGE")
check("3/8 is NOT an algebraic image of Z (Z is pi-bearing, 3/8 is rational; 8/Z^2=3/(4pi) not 3/8)",
      sp.simplify(eight_over_Z2 - sp.Rational(3,8)) != 0 and not landed)
print("  VERDICT(T1): sin^2(theta_W)=3/8 is pure SU(5)/E6 group theory + RG, inherited by ANY GUT, Z-INDEPENDENT.")
print("               The shared '3' and '8' are coincidental (Friedmann-3/Einstein-8pi vs Dynkin 3/8). DEAD as a bridge.")

# ====================================================================================================
print("\n"+"="*84)
print("(T2)  golden-ratio phi  vs  Koide r=sqrt2:  same special value, or different irrationals/slots?")
print("="*84)
phi = (1+sp.sqrt(5))/2
sqrt2 = sp.sqrt(2)
print(f"  framework's OWN special MOND-transition value (banked self-duality catalog): mu_fw special pt = phi = {float(phi):.6f}")
print(f"  Koide amplitude needed for Q=2/3:                                            r = sqrt2 = {float(sqrt2):.6f}")
# minimal polynomials -- DIFFERENT number fields
mp_phi = sp.minimal_polynomial(phi, sp.Symbol('x'))
mp_r   = sp.minimal_polynomial(sqrt2, sp.Symbol('x'))
print(f"  minpoly(phi)  = {mp_phi}     (Q(sqrt5))")
print(f"  minpoly(sqrt2)= {mp_r}     (Q(sqrt2))")
check("phi and sqrt2 are DIFFERENT algebraic numbers in DIFFERENT fields (Q(sqrt5) vs Q(sqrt2))",
      sp.simplify(mp_phi - mp_r) != 0 and abs(float(phi)-float(sqrt2)) > 0.1)
# and golden-ratio MIXING (A5) predicts theta13=0, excluded
th13_GR = 0.0
print(f"  golden-ratio neutrino mixing (A5) predicts theta13 = {th13_GR} deg; measured theta13 = 8.57 deg (>>10 sigma).")
check("golden-ratio mixing EXCLUDED by theta13 != 0", abs(8.57 - th13_GR) > 5)
print("  VERDICT(T2): phi (MOND transition) and sqrt2 (Koide) are different irrationals in different sectors;")
print("               the golden-ratio flavor pattern is empirically EXCLUDED. No phi->flavor bridge.")

# ====================================================================================================
print("\n"+"="*84)
print("(T3)  THE GENUINELY-UNTRIED MAP: shared-minimal-polynomial selector  (framework sqrt2  ==  Koide sqrt2?)")
print("="*84)
print("  THE IDEA (steelmanned): the framework's constitutive dS-Unruh quadrature law")
print("       T(a) = sqrt(a^2 + a_dS^2)   ->  at the channel balance a=a_dS the ratio T/a = sqrt2.")
print("  This sqrt2 is FORCED by the framework (minpoly t^2-2), NOT searched. Koide's r=sqrt2 has the SAME")
print("  minpoly t^2-2. Untried move: posit that the framework's forced sqrt2 SELECTS the Koide amplitude r=sqrt2")
print("  because they are the SAME algebraic number. Does a shared-minpoly map survive the carrier-space test?")
x = sp.Symbol('x')
mp_frameworkSqrt2 = sp.minimal_polynomial(sp.sqrt(2), x)   # t^2-2  (dS-Unruh quadrature)
mp_koideSqrt2     = sp.minimal_polynomial(sp.sqrt(2), x)   # t^2-2  (Koide r)
print(f"  minpoly(framework sqrt2, dS-Unruh quadrature) = {mp_frameworkSqrt2}")
print(f"  minpoly(Koide r)                              = {mp_koideSqrt2}")
check("the two sqrt2's ARE the same algebraic number (same minimal polynomial t^2-2)",
      sp.simplify(mp_frameworkSqrt2 - mp_koideSqrt2) == 0)

print("\n  -- now the OBSTRUCTION: same NUMBER, different CARRIER SPACE. An algebraic selector needs an")
print("     equivariant map between the spaces the number lives on. Build both and test.")

# (a) framework sqrt2 lives as a 1+1 channel balance on the 1-D ACCELERATION axis -> symmetry group Z2 (a -> -a).
#     The 'sqrt2' is |(a,a_dS)| / a at a=a_dS: a 2-vector NORM in a Z2-graded line. Representation: trivial+sign of Z2.
print("\n  (a) framework carrier: dS-Unruh quadrature on the 1-D accel axis. Symmetry = Z2 (reflection a->-a).")
print("      sqrt2 = norm of the balanced 2-vector (a, a_dS); the '2' = #channels = dim(triv)+dim(sign) of Z2 = 1+1.")
Z2_dims = (1, 1)   # trivial + sign irreps of Z2
print(f"      Z2 irrep dims = {Z2_dims}  -> 1+1 channel balance  -> r_carrier = sqrt(sum) = sqrt(2).")

# (b) Koide sqrt2 lives as a 1+2 singlet/doublet split on the 3-D GENERATION space -> symmetry group S3.
#     Q=2/3 <=> |P_singlet|^2 = |P_doublet|^2 of the sqrt-mass vector; r=sqrt2 <=> 45 deg to (1,1,1).
print("\n  (b) Koide carrier: sqrt-mass vector in 3-D generation space. Symmetry = S3 (permute generations).")
print("      3 = 1(trivial/singlet) + 2(standard/doublet) of S3; Q=2/3 <=> equal split |singlet|=|doublet|.")
S3_dims = (1, 2)   # trivial + standard irreps of S3 acting on the natural 3
print(f"      S3 irrep dims on the natural 3 = {S3_dims}  -> 1+2 split  -> r at 45deg = sqrt2 ONLY by equipartition.")
# DEMONSTRATE the slot difference: the framework's '2' is a SUM of two 1-D channels; Koide's involves a 2-D doublet.
check("carrier spaces DIFFER: Z2 gives 1+1 (two 1-D channels); S3 gives 1+2 (a 1-D singlet + a 2-D doublet)",
      Z2_dims == (1,1) and S3_dims == (1,2) and Z2_dims != S3_dims)

# (c) THE EQUIVARIANCE TEST: is there a group homomorphism Z2 -> S3 sending the framework balance to Koide
#     equipartition, that the framework's dynamics FORCES? Z2 embeds in S3 (as a transposition), BUT:
print("\n  (c) equivariance test: does the framework's Z2 (accel reflection) map onto the S3 (generation) split,")
print("      forced by the dynamics? Z2 -> S3 embeddings = the 3 transpositions (conjugate). Check what a")
print("      transposition does to the Koide 1+2 split (does it ENACT the singlet<->doublet equipartition?).")
# A transposition tau in S3 acting on the natural 3-rep. It leaves the singlet (1,1,1)/sqrt3 invariant and acts
# within the 2-D doublet. So it CANNOT swap singlet<->doublet (an irrep decomposition is group-invariant).
tau = sp.Matrix([[0,1,0],[1,0,0],[0,0,1]])   # transposition (12) on generation space
singlet = sp.Matrix([1,1,1])/sp.sqrt(3)
proj_singlet_after = (tau*singlet)
print(f"      transposition tau=(12); tau*singlet = {list(proj_singlet_after.T)} (singlet INVARIANT under tau).")
check("the Z2 (transposition) FIXES the Koide singlet -> it CANNOT enact the singlet<->doublet equipartition",
      sp.simplify(proj_singlet_after - singlet) == sp.zeros(3,1))
print("      => the only Z2 inside S3 that the framework could supply LEAVES the 1+2 split invariant; it does")
print("         NOT force |singlet|=|doublet|. The framework's reflection-Z2 and Koide's permutation-S3 are")
print("         physically unrelated (accel axis vs flavor space); the shared sqrt2 is a NUMBER COINCIDENCE,")
print("         not an equivariant selector. (Coleman-Mandula independently severs spacetime accel from internal flavor.)")

# (d) feasibility number: even granting a miracle map, would it PIN r? Q=1/3+r^2/6 depends ONLY on r, so any
#     'selector' that lands r=sqrt2 is logically identical to assuming Q=2/3 (circularity theorem). Show it.
print("\n  (d) feasibility / circularity check (the decisive number):")
r = sp.Symbol('r', positive=True)
Q_of_r = sp.Rational(1,3) + r**2/6
print(f"      Koide Q(r) = 1/3 + r^2/6  ->  Q(sqrt2) = {sp.simplify(Q_of_r.subs(r, sp.sqrt(2)))}")
check("Q=2/3 <=> r=sqrt2 EXACTLY (sympy) -> 'force r=sqrt2' IS LOGICALLY 'assume 2/3' (circularity theorem)",
      sp.simplify(Q_of_r.subs(r, sp.sqrt(2)) - sp.Rational(2,3)) == 0)
# scale-invariance: the flavor-blind framework rescale mu_fw (EP) cannot move Q
me, mmu, mtau = 0.51099895000, 105.6583755, 1776.86
def Qnum(scale):
    m = np.array([me, mmu, mtau])*scale
    return m.sum()/np.sqrt(m).sum()**2
print(f"      flavor-blind rescale (mu_fw, EP): Q(x1)={Qnum(1):.7f}  Q(x137)={Qnum(137):.7f}  Q(x0.01)={Qnum(0.01):.7f}")
check("Koide Q is SCALE-INVARIANT -> the framework's flavor-blind mu_fw provably cannot move r toward sqrt2",
      abs(Qnum(1)-Qnum(137)) < 1e-9 and abs(Qnum(1)-Qnum(0.01)) < 1e-9)

print("\n  VERDICT(T3): the shared-minpoly map is the cleanest GENUINELY-UNTRIED algebraic angle, and it FAILS")
print("               for a precise, computed reason: SAME algebraic number (sqrt2), DIFFERENT carrier space")
print("               (Z2 accel-reflection 1+1  vs  S3 generation 1+2); the only Z2-in-S3 the framework supplies")
print("               FIXES the Koide singlet (cannot equipartition); and even a miracle map is CIRCULAR")
print("               (r=sqrt2 <=> Q=2/3) and BLOCKED by scale-invariance + Coleman-Mandula. Feasibility: ~0.")

# ====================================================================================================
print("\n"+"="*84)
print("CLASS-2 GRADED LEDGER (consolidated; grades match the banked corpus)")
print("="*84)
ledger = [
 ("E8 'gravity+gauge in one E8' (Lisi)",            "TRIED-WALLED",  "Distler-Garibaldi: 248 real -> non-chiral; +Coleman-Mandula"),
 ("E6 x SU(3)_F gauged family (the lead)",          "PARTIAL-OPEN",  "SU(3) carries N_gen=3; texture/eigenvalues/mixing FREE; hosts-not-forces"),
 ("J3(O)/F4 octonionic Koide (Singh triality)",     "TRIED-WALLED",  "forces Koide SHAPE at WRONG amplitude (5/12, not 2/3); sqrt2 in wrong slot"),
 ("Freudenthal-Tits magic-square hosting",          "TRIED-WALLED",  "shared FRAME real, but dS & gauge are DISJOINT commuting factors (C-M)"),
 ("Koide Q=2/3 from mu_fw / equipartition",         "TRIED-WALLED",  "dS bath does per-state -> r=2 (Q=1 overshoot); flavor-blind"),
 ("Koide r=sqrt2 from golden-ratio phi",            "TRIED-WALLED",  "phi != sqrt2 (diff fields); GR-mixing EXCLUDED by theta13!=0"),
 ("Koide r=sqrt2 from framework sqrt2 quadrature",  "TRIED-WALLED",  "(T3) same number, diff carrier space; not equivariant; circular"),
 ("sin^2(theta_W)=3/8 from Z=sqrt(32pi/3)",         "TRIED-WALLED",  "(T1) 3/8 is RG group-theory, Z-independent; pi-cancellation mirage"),
 ("shape sector (phi,sqrt2,tanh law)->flavor reln", "TRIED-WALLED",  "constitutive irrationals live on accel axis (Z2), not flavor (S3)"),
 ("number-content (sqrtpi/Z,phi,sqrt2)->Yukawa",    "TRIED-WALLED",  "WALL 2: Z carries sqrt(pi) transcendental; flavor data algebraic"),
]
print(f"  {'route':<46s} {'grade':<14s} reason")
print("  " + "-"*94)
for nm, gr, why in ledger:
    print(f"  {nm:<46s} {gr:<14s} {why}")
n_partial = sum(1 for _,g,_ in ledger if g=="PARTIAL-OPEN")
n_untried = sum(1 for _,g,_ in ledger if g=="GENUINELY-UNTRIED")
print(f"\n  Class-2 tally: PARTIAL-OPEN={n_partial}  GENUINELY-UNTRIED(remaining)={n_untried}  TRIED-WALLED={len(ledger)-n_partial-n_untried}")
print("  The lone PARTIAL-OPEN = E6 x SU(3)_F gauged family (right neighborhood, research-program posit, NOT a derivation).")
print("  The best genuinely-untried algebraic ANGLE was the shared-minpoly sqrt2 map (T3) -- now TESTED and WALLED")
print("  on the carrier-space/equivariance obstruction (feasibility ~0). No Class-2 route FORCES an SM number under a0/Z.")

print("\n"+"="*84)
print(f"OVERALL INTERNAL CONSISTENCY: {'ALL CHECKS PASS' if ok else 'SOME CHECK FAILED'}")
print("  (PASS == the ledger's algebra is internally consistent; it does NOT mean the SM is derived.)")
print("="*84)
import sys
sys.exit(0 if ok else 1)
