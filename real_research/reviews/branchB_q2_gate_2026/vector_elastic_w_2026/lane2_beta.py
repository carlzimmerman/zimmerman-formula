#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE 2 -- DERIVE or BOUND  beta = mu_s / (3 K_eff)  for the written elastic-medium action.
==========================================================================================
w  = 1/(1 + 4 beta/kappa_t)   (both Branch-B solvers reduce to this P-wave form; Lane 1 owns
                               kappa_t, Lane 2 owns beta).  Larger beta -> smaller w -> smaller
                               Q2_medium -> EASIER Cassini pass.  beta_crit is a FLOOR.

QUESTION: is beta PINNED (a single number the action forces), BOUNDED (a named window), or a
CONVENTION-HOSTAGE (an undetermined lever)?

The action's written constraints on the shear sector:
  E_med = 1 + [V(J) + mu_s Sigma]/(rho_L c^2)                          (published action)
  Sigma = (1/2)[tr B_tilde - 3] -> (1/2) e_ij e^ij = (1/2) J2         (small-strain, paper)
  deep radial profile compatibility lemma (lane1, EXACT):   J2 = J1^2/6
  Verlinde displacement match fixes the TOTAL deep stiffness:  V + shear = (1/2) K_eff J1^2
  K_eff = a0^2/(16 pi G)
  ghost-free / gradient-stable:  V'' = K_F > 0,  mu_s > 0
  shear-wave causality (6 Z^2 refusal):  v_T = sqrt(mu_s/rho_L) <= 0.17c  <=>  mu_s <= ~6 K_eff

CRUX to test: do these pin mu_s, or only the SUM K_F + (shear share)?  If the only relation is
the deep-energy sum, beta is BOUNDED and the Poisson ratio (=mu_s/K_F split) is a free choice.
"""
import numpy as np
import sympy as sp

# ---------------------------------------------------------------- constants (SI) + footings
c_l  = 2.99792458e8
G    = 6.674e-11
Mpc  = 3.0857e22
Z    = float(np.sqrt(32*np.pi/3.0))          # 5.7888
A0_CANON = 9.36e-11
A0_ALT   = 1.13e-10
Q2_CEIL  = 5.2e-27                            # Cassini 2-sigma ceiling [s^-2]
# banked scalar-class Q2 (both solvers agree), central + range, both footings:
Q2_SCAL  = {"canonical": (2.0e-26, 2.2e-26, 2.5e-26),   # (lo, central, hi)
            "alt":       (2.7e-26, 3.0e-26, 3.3e-26)}
KAPPA_T  = {"A_sqrt": 0.5, "A_stiff": 1.0}   # Lane-1 faithful-map readings (Method A)

def w_pwave(beta, kappa_t):
    return 1.0/(1.0 + 4.0*beta/kappa_t)      # = K_t/(K_t + 4 mu_s/3), mu_s = 3 beta K_eff

def beta_crit(kappa_t, Q2_scalar):
    # PASS iff w*Q2_scalar <= CEIL  <=>  1/(1+4beta/kt) <= CEIL/Q2  <=> beta >= kt*(Q2/CEIL -1)/4
    return kappa_t*(Q2_scalar/Q2_CEIL - 1.0)/4.0

print("="*94)
print(" LANE 2 -- beta = mu_s/(3 K_eff):  DERIVE or BOUND")
print("="*94)

# ==========================================================================================
# STEP 1 -- REPRODUCE the P5 relation  K_F + mu_s/6 = K_eff  (sympy, explicit conventions)
# ==========================================================================================
print("\n[1] Deep-energy match, exact (sympy). Conventions stated:")
J1, KF, mus, Keff = sp.symbols('J1 K_F mu_s K_eff', positive=True)
J2   = J1**2/6                               # compatibility lemma (lane1, deep profile n=0)
Sig  = sp.Rational(1,2)*J2                   # Sigma = (1/2) e:e = (1/2) J2   (paper small-strain)
u_shear = mus*Sig                            # action writes  mu_s * Sigma  (energy density)
u_bulk  = sp.Rational(1,2)*KF*J1**2          # V(J) deep quadratic-equivalent, modulus K_F=V''
u_total = u_shear + u_bulk
u_el    = sp.Rational(1,2)*Keff*J1**2        # Verlinde deep target = (1/2) K_eff J1^2
match   = sp.Eq(u_total, u_el)
# divide out (1/2)J1^2:
rel = sp.simplify(sp.Eq((u_total)/( sp.Rational(1,2)*J1**2 ), Keff))
print("    Sigma=(1/2)J2, J2=J1^2/6, u_shear=mu_s*Sigma, u_bulk=(1/2)K_F J1^2, target=(1/2)K_eff J1^2")
KF_sol = sp.solve(match, KF)[0]
print(f"    => solve: K_F = {KF_sol}")
# express as the P5 relation:
p5 = sp.simplify(KF + mus/6 - Keff)
print(f"    P5 relation reproduced:  K_F + mu_s/6 - K_eff = {sp.simplify(KF_sol + mus/6 - Keff)}  (== 0)  [VERIFIED]")
print("    => the shear sector contributes exactly  mu_s/6  to the total deep stiffness K_eff.")
print("    => K_F = K_eff - mu_s/6.  ONE equation, TWO unknowns (K_F, mu_s).")

# beta in terms of the shear share:
#   mu_s = 3 beta K_eff  =>  shear share mu_s/6 = beta K_eff/2  =>  K_F = K_eff (1 - beta/2)
print("\n    In beta:  mu_s = 3 beta K_eff  =>  K_F = K_eff (1 - beta/2).")
print("    Positivity K_F>0  =>  beta < 2.   Causality mu_s<=6K_eff  =>  beta<=2 (SAME endpoint).")
print("    => the action ALONE pins only the SUM; beta is BOUNDED in (0, 2), NOT pinned.")
print("       The undetermined lever is the Poisson ratio (the mu_s/K_F split) -- the Verlinde")
print("       monopole displacement match is BLIND to it (it fixes only the l=0 combination).")

# ==========================================================================================
# STEP 2 -- beta for the natural elastic closures
# ==========================================================================================
print("\n" + "="*94)
print("[2] beta for the natural closures (each ADDS one relation to pin the split):")
print("="*94)
b = sp.symbols('beta', positive=True)
KF_of_b = Keff*(1 - b/2)                      # from step 1
mus_of_b = 3*b*Keff

closures = {}

# (a) J2 lemma read as "shear energy = 1/6 of bulk energy" at the deep profile
#     u_shear/u_bulk = (mu_s/12 J1^2)/(K_F/2 J1^2) = mu_s/(6 K_F) = 1/6  => mu_s = K_F
eq_a = sp.Eq(mus_of_b, KF_of_b)               # mu_s = K_F
beta_a = sp.solve(eq_a, b)[0]
closures["(a) shear-energy = 1/6 bulk  [mu_s=K_F]"] = float(beta_a)

# (a') alt read: "shear SHARE = 1/6 of K_eff"  => mu_s/6 = K_eff/6 => mu_s = K_eff
eq_ap = sp.Eq(mus_of_b, Keff)
beta_ap = sp.solve(eq_ap, b)[0]
closures["(a') shear share = K_eff/6  [mu_s=K_eff]"] = float(beta_ap)

# (b) Poisson 1/4 as the task states it: mu_s = K_F (lambda=mu reading) -> identical to (a)
closures["(b) Poisson 1/4, task reading [mu_s=K_F]"] = float(beta_a)

# (b') Poisson 1/4 with K_F = BULK modulus: nu_P=1/4 => K_bulk = (5/3) mu_s
eq_bp = sp.Eq(KF_of_b, sp.Rational(5,3)*mus_of_b)
beta_bp = sp.solve(eq_bp, b)[0]
closures["(b') Poisson 1/4, K_F=bulk [K_F=(5/3)mu_s]"] = float(beta_bp)

# (c) shear saturates the causal bound: mu_s = 6 K_eff (K_F -> 0)
closures["(c) shear saturates bound [mu_s=6K_eff]"] = 2.0

print(f"    {'closure':<44}{'beta':>8}{'mu_s/K_eff':>12}{'K_F/K_eff':>11}")
for name, bv in closures.items():
    print(f"    {name:<44}{bv:>8.3f}{3*bv:>12.3f}{1-bv/2:>11.3f}")

nat = [closures["(a) shear-energy = 1/6 bulk  [mu_s=K_F]"],
       closures["(a') shear share = K_eff/6  [mu_s=K_eff]"],
       closures["(b') Poisson 1/4, K_F=bulk [K_F=(5/3)mu_s]"]]
nat_lo, nat_hi = min(nat), max(nat)
print(f"\n    NATURAL-ELASTICITY WINDOW (a,a',b,b'):  beta = [{nat_lo:.3f}, {nat_hi:.3f}], central ~0.29")
print(f"    FULL ACTION BOUND (positivity + causality):  beta in (0, 2)")

# ==========================================================================================
# STEP 3 -- map beta onto the Cassini test (both footings, both kappa_t)
# ==========================================================================================
print("\n" + "="*94)
print("[3] Cassini map:  PASS iff beta >= beta_crit.   Ceiling Q2 = 5.2e-27 s^-2")
print("="*94)
print("    beta_crit = kappa_t*(Q2_scalar/CEIL - 1)/4")
for foot in ("canonical", "alt"):
    q2lo, q2c, q2hi = Q2_SCAL[foot]
    print(f"\n    [{foot}]  Q2_scalar central={q2c:.2e} (range {q2lo:.1e}-{q2hi:.1e})")
    for ktag, kt in KAPPA_T.items():
        bc_c  = beta_crit(kt, q2c)
        bc_lo = beta_crit(kt, q2lo)   # most favorable (lowest Q2_scalar)
        bc_hi = beta_crit(kt, q2hi)
        print(f"      kappa_t={kt:<3} ({ktag:<7}): beta_crit central={bc_c:.3f}  (range {bc_lo:.3f}-{bc_hi:.3f})")

print("\n    --- verdict grid: does each beta land in [beta_crit, 2] (PASS) or below (FAIL)? ---")
print(f"    {'beta source':<38}", end="")
cols = []
for foot in ("canonical","alt"):
    for kt in (0.5,1.0):
        cols.append((foot,kt)); print(f"{foot[:4]}/kt{kt}".rjust(14), end="")
print()
def cell(bv, foot, kt):
    q2c = Q2_SCAL[foot][1]
    bc  = beta_crit(kt, q2c)
    w   = w_pwave(bv, kt); q2 = w*Q2_SCAL[foot][1]
    tag = "PASS" if bv >= bc else f"FAIL{q2/Q2_CEIL:.1f}x"
    return f"{tag}"
rows = [("(a=b) mu_s=K_F  beta=0.286", 2/7),
        ("(a') mu_s=K_eff beta=0.333", 1/3),
        ("(b') Poisson-bulk beta=0.182", closures["(b') Poisson 1/4, K_F=bulk [K_F=(5/3)mu_s]"]),
        ("natural-window LOW  beta=0.182", nat_lo),
        ("natural-window HIGH beta=0.333", nat_hi),
        ("(c) saturated  beta=2.000", 2.0)]
for label, bv in rows:
    print(f"    {label:<38}", end="")
    for foot,kt in cols:
        print(cell(bv,foot,kt).rjust(14), end="")
    print()

# ==========================================================================================
# STEP 4 -- explicit Q2_medium at the natural closure (the reportable number)
# ==========================================================================================
print("\n" + "="*94)
print("[4] Q2_medium = w(beta,kappa_t) * Q2_scalar at the NATURAL closure beta=0.286 (mu_s=K_F):")
print("="*94)
bv = 2/7
for foot in ("canonical","alt"):
    q2c = Q2_SCAL[foot][1]
    for kt in (0.5,1.0):
        w = w_pwave(bv, kt); q2 = w*q2c
        print(f"    {foot:<10} kappa_t={kt}: w={w:.3f}  Q2_med={q2:.2e}  vs ceiling {Q2_CEIL:.1e}"
              f"  => {'PASS' if q2<=Q2_CEIL else f'FAIL by {q2/Q2_CEIL:.2f}x'}")

# ==========================================================================================
# VERDICT
# ==========================================================================================
print("\n" + "="*94)
print(" LANE 2 VERDICT")
print("="*94)
print(f"""  STATUS: beta is BOUNDED, not pinned.
    * The action writes ONE relation on the shear sector: K_F + mu_s/6 = K_eff (P5, reproduced
      symbolically). The Verlinde monopole displacement match fixes only the SUM (the l=0 deep
      stiffness); it is blind to the mu_s/K_F split (the medium's Poisson ratio). No second
      written relation pins mu_s. => beta in (0, 2), BOUNDED.
    * Endpoints coincide by three independent walls: K_F>0 (ghost/stability), mu_s<=6 K_eff
      (v_T<=0.17c causality, the 6 Z^2 refusal) -- both give beta<2. beta=2 is the all-shear
      corner (K_F->0).
  NATURAL VALUE: the standard elastic closures (shear-energy=1/6-bulk, mu_s=K_F, Poisson 1/4)
    cluster at beta = [0.18, 0.33], central ~0.29. These ADD an elasticity assumption the action
    does not itself contain.
  CASSINI: beta_crit (the PASS floor) = 0.36-0.40 (canonical, kt=0.5) up to 0.81 (kt=1.0),
    0.60-1.19 (alt). The natural window [0.18,0.33] lands BELOW every beta_crit
    => Cassini FAILS at natural elasticity, by ~1.3-2x in Q2 (canonical, kt=0.5-1.0).
    The BOUNDED window [0,2] STRADDLES: beta > beta_crit (i.e. shear share LARGER than natural
    elasticity predicts) passes; the natural sub-window does not.
  HONEST READING: Cassini WANTS a shear-STIFF medium (high beta damps the l=2). Natural
    elasticity delivers a shear-SOFT medium (beta~0.29). So the action's natural closure marginally
    FAILS Cassini -- not by a manufactured deficit but because the Poisson ratio the pass needs
    (beta>~0.4, mu_s>~1.2 K_eff) is stiffer than the lemma-natural mu_s~=K_F. beta remains a
    convention-tunable lever WITHIN [0,2]; only an independent Poisson-ratio pin would decide it,
    and the action provides none.""")
print("EXIT 0")
