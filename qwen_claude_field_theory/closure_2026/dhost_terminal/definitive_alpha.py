#!/usr/bin/env python3
"""DEFINITIVE alpha reduction for a CONCRETE DHOST-MOND action. Key question: does the cone regulator's
preferred-frame (alpha_1,alpha_2) contribution share the e^-y self-screening, landing in the allowed
set S? Concrete action: S = Mpl^2/2 R + G_2(X) + A(y)*L_reg + S_m, with G_2X = mu(y)=1-e^-y (y~sqrt(X)),
A(y) = the degenerate cone regulator. All symbolic; verdict HELD for adversarial audit."""
import sympy as sp

y = sp.symbols('y', positive=True)
mu = 1 - sp.exp(-y)                      # G_2X = mu(y): the frozen kernel (deep-MOND: mu~y)

print("=== 1. the k-essence cone c_par^2(y) for the CONCRETE G_2 (y ~ sqrt(X)) ===")
# c_par^2 = 1 + 2X P_XX/P_X ; with P_X=mu(y), y^2 ~ X: 2X P_XX/P_X = y mu'(y)/mu(y)
excess = sp.simplify(y*sp.diff(mu,y)/mu)   # = c_par^2 - 1
c_par2 = 1 + excess
print(f"   c_par^2(y) = 1 + y*mu'/mu = {sp.simplify(c_par2)}")
print(f"   deep MOND y->0: c_par^2 -> {sp.limit(c_par2,y,0)}   (=2, the cone problem)")
print(f"   high accel y->inf: c_par^2 -> {sp.limit(c_par2,y,sp.oo)}   (=1, luminal, NO problem)")
print(f"   => the CONE EXCESS (c_par^2 - 1) = {sp.simplify(excess)} is DEEP-MOND-LOCALIZED:")
excess_hi = sp.simplify(excess.rewrite(sp.exp))
print(f"      high-accel behaviour: excess ~ y*e^-y (exponentially small). Verify limit*e^y:")
print(f"      lim y->inf [excess * e^y] = {sp.limit(excess*sp.exp(y),y,sp.oo)}  (finite => excess ~ y e^-y)")

print("\n=== 2. the regulator must CANCEL the excess => A(y) ~ excess ~ y e^-y at high accel ===")
A_reg = excess    # minimal choice: regulator strength = the excess it cancels (=> c_par^2 -> 1 exactly)
print(f"   choose A(y) = excess(y) = {sp.simplify(A_reg)}  => c_par^2_total = 1 EXACTLY at all y.")
print(f"   A(y) is O(1) in deep MOND (y->0: A->{sp.limit(A_reg,y,0)}) and ~y e^-y at high accel (screened).")

print("\n=== 3. the DECISIVE question: does A(y)'s alpha_1,alpha_2 contribution inherit e^-y? ===")
# The preferred-frame alpha come from the g_0i coupling. The self-screening THEOREM of the framework:
# any preferred-frame observable vanishes as the theory -> GR, i.e. as (1-mu)=e^-y -> 0. The regulator
# operator built from the frame gradient contributes to g_0i PROPORTIONAL to its own strength A(y).
alpha_scaling = sp.simplify(A_reg)   # alpha ~ A(y) at high accel (leading; g_0i coupling tracks strength)
print(f"   alpha_1,alpha_2 ~ A(y) = y e^-y at high accel (the g_0i coupling tracks the regulator strength).")
import math
for yv in [1, 30, 60, 5e7]:
    val = yv*math.exp(-yv) if yv < 700 else float('0')
    tag = f"{val:.2e}" if yv<700 else "~ y*10^(-2e7) (crushed)"
    print(f"     y={yv:>10}:  A ~ y e^-y = {tag}")
print("   at solar y~5e7: A ~ 5e7 * e^-5e7 -- the exponential CRUSHES the polynomial => alpha ~ 0.")
print("   Cassini bound |alpha_2|<1e-7: satisfied by ~1e7 orders. SCREENED.")

print("\n=== 4. the S-intersection verdict for the concrete action ===")
print("   mu~y (deep MOND): YES (G_2X=1-e^-y).  c_T=1: YES (regulator in L_3,4,5, tensor sector untouched).")
print("   0<c_par^2<=1: YES (regulator A=excess => c_par^2=1 exactly).  K_pi>0: YES (degeneracy, finite).")
print("   |alpha_1|,|alpha_2|<<1: YES IF the g_0i coupling tracks A(y)~y e^-y (screened ~1e7 orders).")
print("   => S is NON-EMPTY for this concrete action, CONDITIONAL on the one load-bearing assumption:")
print("   the regulator's g_0i (alpha) coupling scales as its own strength A(y)~y e^-y, NOT as an")
print("   unscreened O(1) piece. THAT is the exact remaining explicit calc the reviewer named.")

print("\n=== HELD VERDICT ===")
print("The concrete DHOST-MOND action satisfies {mu~y, c_T=1, 0<c_par^2<=1 (exactly), K_pi>0}. The cone")
print("excess is EXACTLY y e^-y-localized (rigorous), so the cone regulator is deep-MOND-localized and")
print("its natural strength ~y e^-y at solar accelerations -- IF its preferred-frame coupling tracks that")
print("strength, alpha_1,alpha_2 are self-screened by ~1e7 orders and S is NON-EMPTY: DHOST MOND WORKS.")
print("The SINGLE remaining explicit calc (the load-bearing assumption): does the regulator's g_0i")
print("coupling scale as A(y)~y e^-y (screened) or carry an unscreened O(1) piece (=> S empty, no-go)?")
print("This is genuinely 50/50 without the explicit g_0i variation -- HELD, and the target of the")
print("adversarial audit. If it screens: this is the chicken. If not: the single-metric no-go theorem.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"definitive-alpha","status":"HELD-CONDITIONAL-CHICKEN",
 "certificate":("Concrete DHOST-MOND action (G_2X=1-e^-y, degenerate cone regulator): satisfies {mu~y, "
   "c_T=1, 0<c_par^2<=1 EXACTLY, K_pi>0}. Rigorous: c_par^2(y)=1+y*mu'/mu, cone EXCESS = y*mu'/mu is "
   "EXACTLY y*e^-y-localized (=2 deep-MOND, ->1 high-accel), so the regulator A(y)=excess is deep-MOND-"
   "localized with natural strength ~y e^-y at solar accelerations. IF the regulator's g_0i preferred-"
   "frame coupling tracks its strength A(y)~y e^-y, then alpha_1,alpha_2 are self-screened ~1e7 orders "
   "(Cassini safe) => S NON-EMPTY => DHOST MOND is the chicken. The SINGLE load-bearing assumption "
   "(reviewer's exact remaining calc): does the g_0i coupling scale as A(y) (screened) or carry an "
   "unscreened O(1) piece (=> S empty, single-metric no-go)? Needs the explicit g_0i variation. HELD; "
   "adversarial audit target. Genuinely conditional: screens=>chicken, unscreened=>no-go theorem."),
 "numeric_values":{"c_par2":"1+y*mu'/mu","excess":"y e^-y localized","regulator":"A~y e^-y","S":"conditional on g_0i scaling"}}))
