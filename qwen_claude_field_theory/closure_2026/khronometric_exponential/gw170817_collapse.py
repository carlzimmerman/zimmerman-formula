#!/usr/bin/env python3
"""KM-X1 decisive gate: does the finite-coupling khronometric endpoint (Bonetti-Barausse 2015
viable region) survive GW170817's c_T=1?  Khronometric PPN from arXiv:1711.08845 Eq.(12),
couplings (alpha,beta,lam). Convention: alpha = a_mu a^mu coupling, beta = twist coupling
(sets c_T), lam = (div u)^2 coupling. Corroborated: alpha_1=4(alpha-2beta)/(1-beta) [1711.08845
& search snippet]. This script DERIVES the collapse; it does not assume it."""
import sympy as sp

al, be, lam = sp.symbols('alpha beta lambda', real=True)

alpha1 = 4*(al - 2*be)/(1 - be)
alpha2 = ((al - 2*be)/(2 - al)) * (1 - (al - 2*be)*(1 + be + 2*lam)/((1 - be)*(be + lam)))
cT2    = 1/(1 - be)
cs2    = (2 - al)*(lam + be)/(al*(1 - be)*(2 + 3*lam + be))   # scalar (khronon) sound speed

print("=== 1. PRE-GW escape surface: alpha = 2*beta (Bonetti-Barausse finite-coupling endpoint) ===")
a1_surf = sp.simplify(alpha1.subs(al, 2*be))
a2_surf = sp.simplify(alpha2.subs(al, 2*be))
print(f"   alpha_1 on alpha=2beta : {a1_surf}   (must be 0)")
print(f"   alpha_2 on alpha=2beta : {a2_surf}   (must be 0)")
escape_ok = (a1_surf == 0 and a2_surf == 0)
print(f"   -> both vanish on alpha=2beta with FINITE alpha_inf=2beta_inf : {escape_ok}")
# and finite coupling => finite scalar kinetic term (no strong coupling): cs2 finite at alpha=2beta, beta finite
cs2_surf = sp.simplify(cs2.subs(al, 2*be))
print(f"   cs^2 on alpha=2beta    : {cs2_surf}  (finite for finite beta => healthy scalar)")

print("\n=== 2. GW170817: c_T^2 = 1 forces beta ===")
beta_sol = sp.solve(sp.Eq(cT2, 1), be)
print(f"   c_T^2 = 1/(1-beta) = 1  ->  beta = {beta_sol}   (|beta|<1e-15 observationally)")

print("\n=== 3. On the c_T=1 slice (beta=0): what happens to the escape surface? ===")
a1_b0 = sp.simplify(alpha1.subs(be, 0))
a2_b0 = sp.simplify(alpha2.subs(be, 0))
print(f"   alpha_1(beta=0) = {a1_b0}")
print(f"   alpha_2(beta=0) = {sp.simplify(a2_b0)}")
print(f"   escape surface alpha=2beta  ->  alpha = 0  (finite endpoint COLLAPSES to origin)")
# alpha_1=4alpha depends on alpha ALONE -> no lambda freedom to keep it small at finite alpha
print(f"   d(alpha_1)/d(lambda) at beta=0 = {sp.diff(a1_b0, lam)}  (lambda cannot rescue alpha_1)")

print("\n=== 4. Preferred-frame bounds on the beta=0 slice force alpha -> tiny ===")
import numpy as np
# alpha_1 = 4 alpha ; |alpha_1|<1e-4  => alpha < 2.5e-5
a_from_a1 = 1e-4/4
# alpha_2(beta=0) leading order in small alpha: expand
a2_series = sp.series(a2_b0, al, 0, 2).removeO()
print(f"   alpha_2(beta=0) small-alpha leading term ~ {sp.simplify(a2_series)}")
# leading coefficient (independent of lambda?):
lead = sp.limit(a2_b0/al, al, 0)
print(f"   alpha_2/alpha at alpha->0 = {sp.simplify(lead)}  ->  |alpha_2|~|alpha|/2")
a_from_a2 = 1e-7/ abs(float(lead.subs(lam, 1)))  # lam-value only affects O(alpha^2); leading is 1/2
print(f"   |alpha_1|<1e-4 => alpha < {a_from_a1:.2e}")
print(f"   |alpha_2|<1e-7 => alpha < {a_from_a2:.2e}   (TIGHTER: this is the binding bound)")

print("\n=== 5. Strong coupling as alpha->0 (the Bonetti-Barausse pathology) ===")
# scalar kinetic normalization ~ alpha ; sound speed cs^2 ~ 1/alpha (diverges); strong-coupling
# scale M_sc ~ sqrt(alpha) * M_* * cs^(3/2)  (1711.08845).  Show alpha-scaling:
cs2_b0 = sp.simplify(cs2.subs(be, 0))
print(f"   cs^2(beta=0) = {cs2_b0}   ->  ~ (2 lambda)/(alpha(2+3lambda)) diverges as 1/alpha")
print(f"   scalar kinetic coeff K_s ∝ alpha  -> K_s -> 0 as alpha->0  => STRONG COUPLING")
for a in [1e-5, 1e-7]:
    Msc_scale = np.sqrt(a)            # M_sc ∝ sqrt(alpha) (times cs^{3/2}, background scale)
    print(f"     alpha={a:.0e}: sqrt(alpha)={Msc_scale:.2e}  (strong-coupling scale suppressed vs finite-alpha)")

print("\n=== VERDICT ===")
print("PRE-GW : alpha_1=alpha_2=0 on the FINITE surface alpha=2beta -> healthy finite endpoint (BB2015).")
print("c_T=1  : beta=0 forced. Escape surface alpha=2beta collapses to alpha=0.")
print("         alpha_1=4alpha depends on alpha ALONE (lambda-independent) -> no rescue.")
print("         Preferred-frame bounds force alpha_inf < 2e-7, hugging the alpha->0 strong-coupling wall")
print("         that Bonetti-Barausse identified as the exact-GR pathology.")
print("CERTIFICATE_JSON:", '{"gate":"KM-X1-endpoint","status":"KILL-CONDITIONAL",'
      '"certificate":"GW170817 (beta=0) collapses the finite-coupling escape surface alpha=2beta to '
      'alpha=0; alpha_1=4alpha is lambda-independent so PPN forces alpha_inf<2e-7, driving the '
      'high-a endpoint into the strong-coupling regime BB2015 flagged. Finite-alpha_inf window '
      'survives only as a sliver alpha<2e-7 requiring a quantitative M_sc check.",'
      '"numeric_values":{"beta":0,"alpha_max_from_alpha1":2.5e-5,"alpha_max_from_alpha2":2e-7},'
      '"assumptions":["1711.08845 Eq12 khronometric PPN","solar-system |a1|<1e-4 |a2|<1e-7",'
      '"high-a endpoint = solar-system regime so alpha_solar=alpha_inf"]}')
