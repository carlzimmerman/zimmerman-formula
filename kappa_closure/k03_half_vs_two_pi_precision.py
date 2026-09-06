#!/usr/bin/env python3
"""
k03 -- can the data separate kappa = 1/2 from the horizon-thermodynamic coefficient kappa = sqrt(8 pi/3)/(2 pi) = 0.461?
======================================================================================================================
k01/k02 leave one coefficient-free, right-sign, right-size identification: a0 = c^2/(2 pi L_dS) = c H_Lambda/(2 pi), the
Gibbons-Hawking/Unruh form, i.e. kappa_2pi = sqrt(8 pi/3)/(2 pi) = 0.4607 against the frozen empirical kappa = 1/2.  (This is
NOT Milgrom 1999's de Sitter-Unruh construction, which fixes a0 = 2 c H_Lambda and is excluded at 15.6 sigma in the repo.)
The two differ by 8.5% in a0 (0.036 dex).  This script puts that separation against what the corpus already knows about
the observable side:
  * the BTFR mass-budget floor on a0 is 9.47% (mi_btfr_intercept_kappa_door_2026: f_* + f_gas = 1 forces the stellar M/L
    and gas calibrations to trade), the measurements are 0.465 +/- 0.076 (BTFR) and 0.551 +/- 0.043 (distance-free);
  * Gaia DR4 gives 21% on a0 (d ln gamma_v / d ln a0 = 0.1155);
  * the prediction a0 = kappa c sqrt(G rho_Lambda) scales as H0 at fixed Omega_Lambda, so the H0 tension enters at first order.

  P1 [separation]   8.5% in a0 at 3 sigma needs sigma(a0)/a0 <= 2.8%; the corpus floor is 9.47% -> not reachable from the BTFR;
  P2 [H0 lock]      kappa = 1/2 on Planck H0 (67.4) and kappa = 0.461 on SH0ES H0 (73.0, Omega_Lambda fixed) predict the SAME a0
                    to better than 1%: the coefficient question is degenerate with the H0 tension;
  P3 [today]        each measurement's pull on 1/2 vs 2 pi, and the combined log-likelihood ratio: below 1 sigma (undecided);
  P4 [DR4]          21% on a0 cannot separate 8.5%.
FAIL marks a requirement (separability) the data do not meet.
"""
import math, json, sys
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G = 6.674e-11; c = 2.998e8; MPC = 3.0857e22
OL = 0.685
def a0_pred(kappa, H0kms):
    H0 = H0kms*1e3/MPC; rhoL = OL*3*H0**2/(8*math.pi*G)
    return kappa*c*math.sqrt(G*rhoL)
K_HALF = 0.5; K_2PI = math.sqrt(8*math.pi/3)/(2*math.pi)
MEAS = {"BTFR": (0.465, 0.076), "distance-free": (0.551, 0.043)}; FLOOR = 0.0947; DR4 = 0.21
print("=" * 112); print("k03 -- separating kappa = 1/2 from kappa = sqrt(8 pi/3)/(2 pi) = %.4f" % K_2PI); print("=" * 112)
sep = K_HALF/K_2PI - 1; sep_dex = math.log10(K_HALF/K_2PI)
print(f"    a0(1/2, Planck 67.4) = {a0_pred(K_HALF, 67.4):.4e}; a0(2pi, Planck) = {a0_pred(K_2PI, 67.4):.4e}; separation {100*sep:.1f}% = {sep_dex:.3f} dex")
need3 = sep/3; need2 = sep/2
print(f"    P1: 3 sigma separation needs sigma(a0)/a0 <= {100*need3:.1f}% (2 sigma: {100*need2:.1f}%); corpus BTFR floor {100*FLOOR:.2f}%; best measurement {100*min(e/m for m, e in MEAS.values()):.1f}%")
check("P1 [separation] the BTFR route can reach the 2.8% on a0 that separates 1/2 from 2 pi at 3 sigma", FLOOR <= need3, f"floor {100*FLOOR:.2f}% vs needed {100*need3:.1f}%: a factor {FLOOR/need3:.1f} short, and it is a mass-budget floor, not a statistics floor")
a_half_pl = a0_pred(K_HALF, 67.4); a_2pi_sh = a0_pred(K_2PI, 73.0)
print(f"    P2: a0(1/2, H0 = 67.4) = {a_half_pl:.4e}, a0(2pi, H0 = 73.0) = {a_2pi_sh:.4e}: ratio {a_2pi_sh/a_half_pl:.4f}  (H0 ratio 67.4/73.0 = {67.4/73.0:.4f}, kappa ratio {K_2PI/K_HALF:.4f})")
check("P2 [H0 lock] kappa = 1/2 on Planck H0 and kappa = 2 pi-form on SH0ES H0 predict a0 values that differ by more than 3%", abs(a_2pi_sh/a_half_pl - 1) > 0.03, f"they differ by {100*abs(a_2pi_sh/a_half_pl - 1):.2f}%: the coefficient is degenerate with the H0 tension at fixed Omega_Lambda")
lnLR = 0.0
for n, (m, e) in MEAS.items():
    z_half, z_2pi = (m - K_HALF)/e, (m - K_2PI)/e
    lnLR += 0.5*(z_2pi**2 - z_half**2)
    print(f"    P3: {n:14s} kappa = {m} +/- {e}: {abs(z_half):.2f} sigma from 1/2, {abs(z_2pi):.2f} sigma from 2 pi")
print(f"    P3: combined ln L(1/2)/L(2pi) = {lnLR:+.2f}  (|ln LR| = 4.5 would be 3 sigma)")
check("P3 [today] the two measurements together prefer one coefficient at >= 2 sigma (|ln LR| >= 2)", abs(lnLR) >= 2.0, f"|ln LR| = {abs(lnLR):.2f}: undecided; the two measurements pull opposite ways")
check("P4 [DR4] Gaia DR4's 21% on a0 separates 8.5%", DR4 <= need2, f"21% vs {100*need2:.1f}% needed for 2 sigma")
print("\n  OUTCOME: the only principle-shaped coefficient left standing (kappa = 0.461, the 2 pi horizon form) is 8.5% from the frozen 1/2, below the BTFR"
      "\n           mass-budget floor (9.5%), below DR4's reach (21%), undecided by the two measurements in hand, and exactly degenerate with the H0 tension"
      "\n           at fixed Omega_Lambda.  The coefficient is a precision problem gated by the stellar M/L zero point, the absolute gas scale and H0 --"
      "\n           not by more theory.  kappa = 1/2 stays the frozen empirical target; 0.461 is recorded as the one un-excluded principle-shaped alternative.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
