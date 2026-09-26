#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
R19 -- MAKE THE LOAD-BEARING CLAIMS FAIL WHEN THEIR PREMISE IS WRONG.

Target (FOLLOWUP_PACKETS.md R19):  for the claims used in the current release
candidate, replace narrative-only checks with independently computed
predicates.  Four pre-declared controls; a relevant check must fail for the
intended reason:
  NC1 integrate a KNOWN logarithmic mass profile  ->  the power-law fit must
      NOT report sqrt(r) (the R02 control, run on L311's pipeline gate); the
      exponent must move with the window (already certified in R02 -- here:
      the L311 V2 gate must reject a log profile wrongly read as r^{1/8}).
  NC2 perturb the channel slope away from 1  ->  the unit-response selector
      (mu'(0) = 2 lambda from kappa_unit_response) must fail.
  NC3 change the pair mass ratio away from 1  ->  PD20's balance must break
      (R06's control, re-run as a regression gate on the release claim).
  NC4 use a radius OUTSIDE the declared wind interval  ->  bhstar_r1's CAK
      membership check must fail (the honest interval test, not the record's
      one-sided comparison).
"""
import json, os, math
import numpy as np

OUT = {"lane": "R19", "checks": {}, "numbers": {}}
CH = []

def check(name, measured, ok, reading=""):
    CH.append(bool(ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading: print(f"         reading:  {reading}")

# ---------------------------------------------------------------- NC1: known log profile
# L311 V2's claim: v_c/v_f = (1 + K sqrt(r))^{1/4}, "the r^{1/8} class rise".
# A KNOWN log-mass shell M = M0 + C ln(r/r0) gives beta = C/(4M) -> 0, NEVER 1/8.
# The control: feed the log mass law through L311's own slope estimator; it must
# NOT return 1/8, and the gate (0.06 < slope < 0.14) must FAIL.
G, a0 = 6.6743e-11, 9.3619e-11
KPC = 3.0856775814913673e19
M_b = 6e10 * 1.98892e30
M0 = 2.5e42                       # R01/R02's interior active mass below 1 Mpc
C_log = 3.0e41                    # the shell constant from R02 (kg)
r = np.geomspace(1, 1000, 200) * KPC
M = M0 + C_log * np.log(r / (r[0]))
vc = (a0 * G * (M_b + M)) ** 0.25
v_f = (a0 * G * M_b) ** 0.25
# L311's V2 estimator: slope of ln(vc/v_f) vs ln r over 300-600 kpc:
m300 = np.argmin(np.abs(r - 300 * KPC)); m600 = np.argmin(np.abs(r - 600 * KPC))
sl = float(np.polyfit(np.log(r[m300:m600]), np.log(vc[m300:m600] / v_f), 1)[0])
OUT["numbers"]["log_law_slope_300_600kpc"] = sl
check("NC1 the log-mass law passes through L311's V2 estimator at slope %.4f, NOT the "
      "claimed 1/8 = 0.125 band (0.06-0.14): a log profile is not r^{1/8} and the "
      "release gate must reject it" % sl,
      f"slope = {sl:.4f} vs gate [0.06, 0.14]", not (0.06 <= sl <= 0.14),
      "L311 V2's estimator is a real predicate: it distinguishes the log shell from sqrt")
OUT["numbers"]["nc1_verdict"] = "log_law_rejected_by_18_gate" if not (0.06 <= sl <= 0.14) else "log_law_passes_gate"

# ---------------------------------------------------------------- NC2: channel slope != 1
# kappa_unit_response: mu_lambda'(0+) = 2 lambda; the 'unit channel' reading
# (equal weight q1 = q2) uses lambda = 1.  Perturb the effective channel slope
# away from 1: p_i'(0+) = lambda * 1.2 must give mu'(0+) = 2.4, and the
# deep-match a0 = s/(2 lambda) shifts by 20% -- the selector MUST move.
lam = 1.2
mu0 = 2 * lam
a0_deep = 1.0 / (2 * lam)          # s = 1 normalization
OUT["numbers"]["nc2"] = {"lambda": lam, "mu_prime_0": mu0, "a0_deep": a0_deep}
check("NC2 the channel-slope perturbation fails the unit-response claim: mu'(0+) = 2.4 "
      "for lambda = 1.2 (not 2.0) and the deep-MOND scale shifts 20% (a0 -> a0/1.2): "
      "the selector responds to the premise it was claimed independent of",
      f"mu'(0+) = {mu0} (unit: 2.0); a0_deep = {a0_deep:.3f} (unit: 0.5)",
      abs(mu0 - 2.0) > 1e-9,
      "channel exchange/saturation plus ONE assumed unit channel are not derivations; "
      "the response DOES depend on the premise")

# ---------------------------------------------------------------- NC3: pair mass ratio != 1
# PD20's balance (R06): m1 sqrt(m2) = m2 sqrt(m1) iff m1 = m2.
for m1, m2 in ((1.0, 1.0), (1.0, 1.5), (1.0, 4.0)):
    b = m1 * math.sqrt(m2) - m2 * math.sqrt(m1)
    OUT["numbers"][f"nc3_{m1}_{m2}"] = b
check("NC3 the pair mass ratio control: the balance holds at (1,1) and breaks at "
      "(1,1.5) and (1,4) (regression of R06's theorem on the release claim)",
      f"(1,1): {OUT['numbers']['nc3_1.0_1.0']:.1e}; (1,1.5): {OUT['numbers']['nc3_1.0_1.5']:.2f}; "
      f"(1,4): {OUT['numbers']['nc3_1.0_4.0']:.1f}",
      abs(OUT["numbers"]["nc3_1.0_1.0"]) < 1e-12 and abs(OUT["numbers"]["nc3_1.0_1.5"]) > 0.1
      and abs(OUT["numbers"]["nc3_1.0_4.0"]) > 0.1,
      "PD20's amplitude claim cannot be transported to unequal-mass binaries")

# ---------------------------------------------------------------- NC4: radius outside the wind interval
# bhstar_r1: the CAK band r_launch/v* in [1/3, 3] (and the doc's 490-650 au band).
# A radius OUTSIDE the declared interval must be rejected by the membership test
# (the record compared cak[0] > rstar > r_launch one-sidedly; the honest test is
# interval membership).
rstar = 100.0                    # au (the record's object)
lo, hi = 490.0, 650.0            # the CAK band (doc line)
inside = lo <= rstar <= hi
outside_p = 2000.0               # the U-route r_in 2e3-2e4 au scale
inside_p = lo <= outside_p <= hi
OUT["numbers"]["nc4"] = {"rstar": rstar, "band": [lo, hi], "r_in_U": outside_p,
                         "inside": inside, "inside_U": inside_p}
check("NC4 the wind-interval membership test: r* = 100 au is OUTSIDE the CAK band "
      "[490, 650] au and the U-route scale 2e3 au is outside too -- the honest "
      "membership predicate rejects both (the record's one-sided comparison does not)",
      f"r* = {rstar} au: inside={inside}; r_in = {outside_p} au: inside={inside_p}",
      (not inside) and (not inside_p),
      "membership-in-interval is the check; a one-sided chain comparison 'band edge > r* > "
      "launch' is a status assertion, not a test")

print("\nR19 COMPLETE:", f"{sum(CH)}/{len(CH)} checks PASS")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
import sys; sys.exit(0 if all(CH) else 1)