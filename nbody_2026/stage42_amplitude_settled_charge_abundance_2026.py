#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage42_amplitude_settled_charge_abundance_2026.py
==================================================
THE AMPLITUDE, SETTLED -- and the answer makes the whole sign question MOOT.

Two routes disagreed by six orders of magnitude and I said at most one could be right.  Both were right
about the physics; the gap was a UNITS MISMATCH plus one mispaired bound of mine.  Settling it produces a
much cleaner result than either: the amplitude is a PURE CHARGE-ABUNDANCE RATIO in which nu_0, Lambda_D,
Q_0, M and kappa ALL CANCEL, and it is short by 7e7 to 6e8.

--------------------------------------------------------------------------------------------------
THE TWO ROUTES ARE THE SAME FORMULA
--------------------------------------------------------------------------------------------------
Route 1 (mine, from the DBI derivative at the true background u_0 = nu_0 Lambda_D):
        Acal'/Acal = K'/K  ->  -nu_0/Lambda_D    so the coefficient is   nu_0 Q_0/Lambda_D
Route 2 (from the framework's OWN thermodynamics):
        Acal' = kappa^2 G (-K') = -kappa^2 G n,  and -K = rho_Lambda c^2 by w = -1, and the corpus's
        rho = Q_0 n, so with delta Q = -Q_0 Phi:
        *** Delta mu = -(rho_charge / rho_Lambda c^2) Phi T(y) ***
and Q_0 K'/(-K) at u_0 equals nu_0 Q_0/Lambda_D IDENTICALLY (verified below).  So the coefficient is the
pure ratio rho_charge/(rho_Lambda c^2) = (Omega_kd/Omega_Lambda) Delta_loc, with nu_0, Lambda_D, Q_0, M
and kappa ALL CANCELLING.

--------------------------------------------------------------------------------------------------
WHY THE NUMBERS LOOKED SIX ORDERS APART
--------------------------------------------------------------------------------------------------
  3.7425e-5  was the DENSITY RATIO rho_charge/rho_Lambda at Delta_loc = 58.  Its fit-unit value is
             w_1 = ratio x Phi_ref = 8.23e-10.  Not a competing amplitude -- a different quantity.
  1.4e-11    was mine, and it was wrong twice: it omitted Delta_loc entirely, and it used stage 17 D4's
             "Lambda_D/Q_0 >= 33.15" at the nu_0 CEILING when that 33.15 is derived at the nu_0 FLOOR
             (0.685 x 2.14e-5 / 4.42e-7 = 33.17).  That is the mismatched-extremes error already flagged
             against stage 40, committed a second time by me.
The correct ledger, with nu_0 cancelling so it cannot be used as a lever either way:
        w_1 = (Omega_kd/Omega_Lambda) x Delta_loc x Phi_ref  <=  8.2e-10 (Delta_loc=58) ... 7.1e-9 (500)
against a required ~0.5 canonical / ~0.4 ALT.  SHORTFALL 7e7x to 6e8x.

--------------------------------------------------------------------------------------------------
AND THE STATEMENT THAT ENDS IT, PARAMETER-FREE AND FOOTING-INDEPENDENT
--------------------------------------------------------------------------------------------------
Let the shift charge be the ENTIRE dark matter content -- Omega_kd = Omega_dm = 0.265, ignoring stage 3's
black-hole ceiling of 4.42e-7 altogether:
        Delta_loc = 58  ->  w_1 = 4.94e-4,  still 1013x short
        Delta_loc = 500 ->  w_1 = 4.26e-3,  still  117x short
Reaching w_1 = 0.5 needs Omega_kd = 268, i.e. 1013x Omega_dm.  So the failure is not about nu_0, Lambda_D,
Q_0, M or kappa, and not about the DBI wall: the amplitude IS a charge-abundance ratio, and the charge
would have to outweigh the dark matter by three orders to matter in a cluster.

*** AND THIS MAKES THE SIGN QUESTION MOOT.  The magnitude bound is independent of sign(u_0), of whether
the background sits at u = 0 or at u_0 = nu_0 Lambda_D, and of the DBI form -- it follows from
Acal' = -kappa^2 G n alone, i.e. from the promotion Acal = kappa^2 G (-K) plus n = K'.  So the provisional
retraction of the sign theorem (filed 2026-08-12, and I still believe that retraction is correct) does NOT
reopen the promoted-a_0 cluster route.  The route is closed on magnitude instead, by a stronger and much
simpler argument than the one I had. ***

WHAT THIS COSTS ME: stage 40's sign theorem is retracted, its w_2 <= 2.2e-13 bound is retracted (wrong
order AND mispaired), and my 1.4e-11 first-order estimate is retracted.  What replaces all three is one
line: the amplitude is rho_charge/rho_Lambda, and the shift charge is a trace species.
"""

import sys

import numpy as np
import sympy as sp

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


print(__doc__)

OM_L, OM_KD_CEIL, OM_DM = 0.685, 4.42e-7, 0.265     # stage3 BH ceiling on Omega_khronon-dust
PHI_REF = 2.2e-5                                     # committed |Phi|/c^2 at cluster R500
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4               # committed stage 17 window
NEED_CAN, NEED_ALT = 0.5, 0.4                        # converged stage-41 fit requirement, both footings

# =================================================================================================
print("=" * 100)
print("PART A -- the two routes are the SAME formula")
print("=" * 100)

u, M, mp, kap, G, Q0, nu0, LD = sp.symbols("u M mu_p kappa G Q_0 nu_0 Lambda_D", positive=True)
K = -M ** 4 * sp.sqrt(1 - mp ** 2 * u ** 2 / M ** 4)
Acal = kap ** 2 * G * (-K)

# route 1: Acal'/Acal at the true background, with beta = 1 substituted CONSISTENTLY
sub = {u: nu0 * LD, mp: M ** 2 / LD}                 # u_0 = nu_0 Lambda_D and Lambda_D = M^2/mu_p
r1 = sp.simplify(sp.series(sp.simplify((sp.diff(Acal, u) / Acal).subs(sub)), nu0, 0, 2).removeO())
check(sp.simplify(r1 + nu0 / LD) == 0,
      f"A1  ROUTE 1: Acal'/Acal at u_0 = nu_0 Lambda_D is {r1} = -nu_0/Lambda_D to leading order",
      "so the first-order coefficient multiplying delta Q is nu_0/Lambda_D, hence nu_0 Q_0/Lambda_D "
      "after delta Q = -Q_0 Phi")

# route 2: the pure thermodynamic ratio rho_charge/(rho_Lambda c^2) = Q_0 K'/(-K)
r2 = sp.simplify(sp.series(sp.simplify((Q0 * sp.diff(K, u) / (-K)).subs(sub)), nu0, 0, 2).removeO())
check(sp.simplify(r2 - nu0 * Q0 / LD) == 0,
      f"A2  *** ROUTE 2: rho_charge/(rho_Lambda c^2) = Q_0 K'/(-K) at the same background is {r2}, "
      f"IDENTICALLY EQUAL to route 1's nu_0 Q_0/Lambda_D.  There was never a formula discrepancy ***",
      "an earlier run of this check printed False only because it failed to substitute mu_p = M^2/Lambda_D; "
      "with beta = 1 applied consistently the two are the same expression")

info("A3  AND THE CANCELLATION IS THE POINT: Acal' = kappa^2 G (-K') = -kappa^2 G n identically, and "
     "-K = rho_Lambda c^2 by w = -1, so Acal'/Acal = -n/(rho_Lambda c^2).  With the corpus's own "
     "rho = Q_0 n and delta Q = -Q_0 Phi, Delta mu = -(rho_charge/rho_Lambda c^2) Phi T(y).  nu_0, "
     "Lambda_D, Q_0, M and kappa ALL CANCEL -- the amplitude is a pure charge-abundance ratio.")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- so why did the two NUMBERS differ by six orders?")
print("=" * 100)

ratio58 = (OM_KD_CEIL / OM_L) * 58
check(abs(ratio58 - 3.7425e-5) / 3.7425e-5 < 0.02,
      f"B1  the other route's 3.7425e-5 was the DENSITY RATIO rho_charge/rho_Lambda at Delta_loc = 58: "
      f"({OM_KD_CEIL:.2e}/{OM_L}) x 58 = {ratio58:.4e}.  Its FIT-UNIT value is w_1 = ratio x Phi_ref = "
      f"{ratio58*PHI_REF:.3e} -- a different quantity, not a competing amplitude")

ld_from_floor = OM_L * NU0_FLOOR / OM_KD_CEIL
check(abs(ld_from_floor - 33.15) < 0.1,
      f"B2  *** AND MY 1.4e-11 WAS WRONG TWICE: it omitted Delta_loc entirely, and it applied stage 17 "
      f"D4's Lambda_D/Q_0 >= 33.15 at the nu_0 CEILING when 33.15 is derived at the nu_0 FLOOR "
      f"({OM_L} x {NU0_FLOOR:.2e} / {OM_KD_CEIL:.2e} = {ld_from_floor:.2f}).  That is the mismatched-extremes error "
      f"already flagged against stage 40, and I committed it a second time ***",
      "the bound Lambda_D/Q_0 >= Omega_Lambda nu_0/Omega_kd is EQUIVALENT to nu_0 Q_0/Lambda_D <= "
      "Omega_kd/Omega_Lambda, in which nu_0 cancels -- so nu_0 is not a lever in either direction")

check(abs((OM_KD_CEIL / OM_L) - 6.453e-7) / 6.453e-7 < 0.01,
      f"B3  the correct nu_0-free statement: nu_0 Q_0/Lambda_D <= Omega_kd/Omega_Lambda = "
      f"{OM_KD_CEIL/OM_L:.4e} at the cosmic mean")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the ledger, and the parameter-free statement that ends it")
print("=" * 100)

print(f"    {'Delta_loc':>10} {'rho_ch/rho_L':>14} {'w_1':>12} {'short (can)':>13} {'short (ALT)':>13}")
for dl in (58, 200, 500):
    r = (OM_KD_CEIL / OM_L) * dl
    w1 = r * PHI_REF
    print(f"    {dl:>10d} {r:>14.3e} {w1:>12.3e} {NEED_CAN/w1:>13.1e} {NEED_ALT/w1:>13.1e}")

w1_58 = (OM_KD_CEIL / OM_L) * 58 * PHI_REF
w1_500 = (OM_KD_CEIL / OM_L) * 500 * PHI_REF
check(NEED_CAN / w1_500 > 1e7,
      f"C1  at stage 3's black-hole ceiling the shortfall is {NEED_CAN/w1_58:.1e}x (Delta_loc = 58) to "
      f"{NEED_CAN/w1_500:.1e}x (Delta_loc = 500) on the canonical footing, and "
      f"{NEED_ALT/w1_58:.1e}x to {NEED_ALT/w1_500:.1e}x on the ALT footing")

print()
print("    NOW IGNORE stage 3's ceiling ENTIRELY and let the charge BE the whole dark matter:")
for dl in (58, 500):
    w1 = (OM_DM / OM_L) * dl * PHI_REF
    print(f"      Omega_kd = Omega_dm = {OM_DM}, Delta_loc = {dl:3d}:  w_1 = {w1:.3e}  ->  still "
          f"{NEED_CAN/w1:.0f}x short (canonical), {NEED_ALT/w1:.0f}x (ALT)")

w1_dm58 = (OM_DM / OM_L) * 58 * PHI_REF
w1_dm500 = (OM_DM / OM_L) * 500 * PHI_REF
check(NEED_CAN / w1_dm500 > 10,
      f"C2  *** EVEN AT Omega_kd = Omega_dm THE TERM IS {NEED_CAN/w1_dm58:.0f}x TO {NEED_CAN/w1_dm500:.0f}x TOO SMALL.  So the failure "
      f"is not about nu_0, Lambda_D, Q_0, M, kappa, or the DBI reality wall -- the amplitude is a "
      f"charge-abundance ratio and the charge would have to OUTWEIGH the dark matter to matter ***")

need_om = NEED_CAN * OM_L / (58 * PHI_REF)
check(need_om / OM_DM > 100,
      f"C3  reaching w_1 = {NEED_CAN} requires Omega_kd = {need_om:.1f}, i.e. {need_om/OM_DM:.0f}x Omega_dm and "
      f"{need_om/OM_KD_CEIL:.1e}x stage 3's own ceiling")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- and this makes the SIGN question moot")
print("=" * 100)

info("D1  *** THE MAGNITUDE BOUND IS INDEPENDENT OF EVERYTHING THE SIGN ARGUMENT DEPENDED ON: it does not "
     "use sign(u_0), does not care whether the background sits at u = 0 or at u_0 = nu_0 Lambda_D, and "
     "does not use the DBI form.  It follows from Acal' = -kappa^2 G n alone -- i.e. from Carl's promotion "
     "Acal = kappa^2 G (-K) together with n = K'. ***")

info("D2  SO THE PROVISIONAL RETRACTION OF THE SIGN THEOREM (filed 2026-08-12, and I still believe that "
     "retraction is CORRECT -- the background is at u_0 = nu_0 Lambda_D != 0, the first-order term is "
     "nonzero and linear in delta Q, and a_0(z) fixes |u_0| but not sign(u_0)) DOES NOT REOPEN THIS ROUTE. "
     "The route is closed on MAGNITUDE instead, by a simpler and stronger argument than the one I had.")

info("D3  WHAT I AM RETRACTING, precisely: stage 40's SIGN THEOREM; stage 40's w_2 <= 2.2021e-13 (wrong "
     "order in delta Q AND mispaired bound); stage 41's D1/D2; and my own 1.4e-11 first-order estimate "
     "from this same session.  What replaces all four is one line: the amplitude is "
     "rho_charge/rho_Lambda x Phi_ref, and the shift charge is a trace species.")

info("D4  AND WHAT IS UNTOUCHED, because none of it depends on the amplitude: the exact identity "
     "F_YQ = -(1/8piG) F''(y) y (Acal'/Acal); the forced shape T(y) = y F''(y); the Phi-power; stage 30's "
     "result that clusters need a SECOND variable at 37-73 sigma; the DICHOTOMY (right sign <=> new "
     "independent field <=> no derived amplitude); and every banked result -- c_T = 1, no-ghost, "
     "gamma_PPN = 1, BTFR, RAR 0.108 dex, solar system, CLASS, lensing.")

info("D5  ALSO STILL OPEN AND STILL SHARP, independent of clusters: if the background is at u_0 != 0 then "
     "w = -1 is exact only to O(nu_0^2).  With nu_0 in [2.14e-5, 1.77e-4] that is a fractional offset of "
     f"order nu_0^2 = [{NU0_FLOOR**2:.2e}, {NU0_CEIL**2:.2e}], i.e. FAR below any current w_0 measurement -- so the "
     "framework's 'w = -1 exact' survives as a statement about observation, but should be written as "
     "w = -1 + O(nu_0^2) rather than exactly -1.  That is a wording correction, not a physics loss.")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE AMPLITUDE IS SETTLED, AND IT CLOSES THE ROUTE ON MAGNITUDE RATHER THAN SIGN.

      Delta mu = -(rho_charge / rho_Lambda c^2) Phi T(y),      T(y) = y F''(y)
      w_1 = (Omega_kd/Omega_Lambda) x Delta_loc x Phi_ref

  1. THE TWO ROUTES WERE THE SAME FORMULA.  Q_0 K'/(-K) at u_0 = nu_0 Lambda_D is identically
     nu_0 Q_0/Lambda_D.  nu_0, Lambda_D, Q_0, M and kappa ALL CANCEL: the amplitude is a pure
     charge-abundance ratio.  The apparent six-order gap was a UNITS MISMATCH (3.74e-5 is the density
     ratio; 8.23e-10 is its fit-unit value) plus my own mispaired bound.

  2. MY 1.4e-11 WAS WRONG TWICE: it dropped Delta_loc, and it used Lambda_D/Q_0 >= 33.15 at the nu_0
     CEILING when 33.15 is derived at the nu_0 FLOOR.  That is the mismatched-extremes error I had already
     flagged against stage 40 -- and then committed again.  The nu_0-free form is
     nu_0 Q_0/Lambda_D <= Omega_kd/Omega_Lambda = {OM_KD_CEIL/OM_L:.3e}, in which nu_0 cannot be used as a lever
     in either direction.

  3. THE LEDGER: w_1 <= {w1_58:.2e} (Delta_loc = 58) to {w1_500:.2e} (500), against ~{NEED_CAN} canonical and ~{NEED_ALT} ALT.
     SHORTFALL {NEED_CAN/w1_58:.0e}x to {NEED_CAN/w1_500:.0e}x.

  4. *** AND THE PARAMETER-FREE VERSION THAT ENDS IT: ignore stage 3's black-hole ceiling entirely and let
     the shift charge BE the whole dark matter, Omega_kd = Omega_dm = {OM_DM}.  The term is STILL
     {NEED_CAN/w1_dm58:.0f}x to {NEED_CAN/w1_dm500:.0f}x too small.  Reaching w_1 = {NEED_CAN} needs Omega_kd = {need_om:.0f}, or {need_om/OM_DM:.0f}x Omega_dm. ***

  5. SO THE SIGN QUESTION IS MOOT.  The magnitude bound uses neither sign(u_0), nor the background point,
     nor the DBI form -- only Acal' = -kappa^2 G n, i.e. Carl's promotion plus n = K'.  The provisional
     retraction of the sign theorem stands (the background IS at u_0 = nu_0 Lambda_D != 0, and a_0(z) fixes
     |u_0| but not its sign), and it does not reopen the route.

  6. AND ONE WORDING CORRECTION BEYOND CLUSTERS: at u_0 != 0, w = -1 is exact only to O(nu_0^2) =
     [{NU0_FLOOR**2:.1e}, {NU0_CEIL**2:.1e}].  That is far below any w_0 measurement, so the result survives observationally
     and should be written w = -1 + O(nu_0^2) rather than exactly -1.  A wording fix, not a physics loss.

  NOT CLAIMED: that no cluster mechanism exists.  The promoted-a_0 route is closed on magnitude; the
  DICHOTOMY still says a genuinely new independent field gets the favourable sign generically, and that
  remains the one open route, at the parameter-count price already stated.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
