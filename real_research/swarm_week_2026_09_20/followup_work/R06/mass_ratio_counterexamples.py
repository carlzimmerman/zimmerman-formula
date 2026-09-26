#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
R06 -- LOCK DOWN THE UNEQUAL-MASS CONSERVATION OBSTRUCTION (numeric face).

Target (FOLLOWUP_PACKETS.md R06):  m1*sqrt(m2) = m2*sqrt(m1)  iff  m1 = m2.
PD20's per-body ansatz (g1 = sqrt(a0 G m2)/r on body 1, g2 = sqrt(a0 G m1)/r on
body 2) gives opposing force magnitudes F1 = m1 sqrt(a0 G m2)/r and
F2 = m2 sqrt(a0 G m1)/r; translation invariance (Newton III) requires F1 = F2.
Masses 1 and 4 with a0 G r = 1 give F1 = 2 and F2 = 4 -- momentum is not
conserved.  Companion Lean certificate: PairObstruction.lean (exit 0, zero
sorry, axioms = [propext, Classical.choice, Quot.sound]).
"""
import json, os, math
import numpy as np

OUT = {"lane": "R06", "checks": {}, "numbers": {}}
CH = []

def check(name, measured, ok, reading=""):
    CH.append(bool(ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading: print(f"         reading:  {reading}")

# the stated counterexample:  m1 = 1, m2 = 4, sqrt(a0 G)/r = 1
F1 = 1.0 * math.sqrt(4.0)          # m1 * sqrt(m2)
F2 = 4.0 * math.sqrt(1.0)          # m2 * sqrt(m1)
check("C1 the (1, 4) counterexample: opposing force magnitudes are 2 and 4 -- "
      "the per-body ansatz violates momentum conservation for unequal masses",
      f"F1 = {F1}, F2 = {F2}, F1/F2 = {F1/F2}", abs(F1 - F2) > 1e-12,
      "the corpus's PD20 two-body amplitude (sqrt(2) factor) rests on an unequal-mass violation")

# scan: balance holds iff m1 = m2 (positive masses); include true on-diagonal pairs
pairs = [(0.25, 0.25), (1.0, 1.0), (4.0, 4.0), (10.0, 10.0)]
ratios = []
for m1, m2 in pairs + [(m, m) for m in (1e-3, 1e-1, 1.0, 10.0, 1e3)]:
    b = m1 * math.sqrt(m2) - m2 * math.sqrt(m1)
    exact = abs(b) < 1e-12
    ratios.append((m1, m2, b, exact))
for m1 in (1e-3, 1e-1, 1.0, 10.0, 1e3):
    for m2 in (1e-4, 0.25, 2.0, 4.0, 9.0, 1e4):
        if m1 == m2:
            continue
        b = m1 * math.sqrt(m2) - m2 * math.sqrt(m1)
        exact = abs(b) < 1e-12
        ratios.append((m1, m2, b, exact))
OUT["numbers"]["grid"] = ratios
n_off_diag = sum(1 for m1, m2, b, ex in ratios if abs(m1 - m2) > 1e-12 and ex)
n_on_diag = sum(1 for m1, m2, b, ex in ratios if abs(m1 - m2) < 1e-12 and ex)
n_on_tot = sum(1 for m1, m2, b, ex in ratios if abs(m1 - m2) < 1e-12)
check("C2 the scan: the balance m1 sqrt(m2) = m2 sqrt(m1) holds at m1 = m2 and nowhere else "
      "on an extensive positive-mass grid (Lean-certified for all positive reals)",
      f"{n_off_diag} off-diagonal false balances, {n_on_diag}/{n_on_tot} diagonal balances hold",
      n_off_diag == 0 and n_on_diag == n_on_tot,
      "the equal-mass case is the only conserving configuration of the per-body ansatz")

# the test-particle limit is the only consistent limit:
tp = [m2 * math.sqrt(1.0) for m2 in (1e-1, 1e-2, 1e-4, 1e-6)]
check("C3 the test-particle limit: F2 = m2 sqrt(m1) -> 0 as m2 -> 0 and F1 = m1 sqrt(m2) -> 0 "
      "(both forces vanish, so the isolated test-body law is a consistent limit)",
      f"F2 chain {[f'{v:.1e}' for v in tp]} (strictly decreasing to 0); F1 at m2=1e-6: {1.0*math.sqrt(1e-6):.1e}",
      all(tp[i] > tp[i + 1] for i in range(len(tp) - 1)) and tp[-1] < 2e-3
      and 1.0 * math.sqrt(1e-6) < 2e-3,
      "PD18's isolated test-body statement survives as a limit; PD20's equal-mass factor is a special case")

# ------------------------------------------------------------------ premise scope
scope = {
    "claim": "m1 sqrt(m2) = m2 sqrt(m1) iff m1 = m2 (positive masses)",
    "applies_to": ["PD20 per-body ansatz: each comparable mass follows the other mass's isolated "
                   "test-body law, forces summed for the relative acceleration"],
    "does_NOT_apply_to": [
        "an action-derived two-body force with field momentum (R07's route): momentum can be "
        "balanced by field stress, which changes the physical problem",
        "test-particle limits (m2 -> 0): both forces vanish consistently",
        "equal-mass pairs: the sqrt-2 factor is the legitimately registered special case"],
    "consequence": "PD20/PD21 survive as CONDITIONAL algebra; their 'derived' unequal-mass "
                   "amplitude is not supportable from the per-body ansatz; the actual two-body "
                   "force must be derived from the action's translation identity (R07).",
    "translation_conservation_obligation": "for the intended action, the pair's force law must "
        "satisfy F1 = -F2 (or the field must carry the missing momentum explicitly); "
        "the per-body ansatz satisfies neither."
}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "premise_scope.md"), "w") as fh:
    fh.write("# R06 premise scope\n\n")
    for k, v in scope.items():
        if isinstance(v, list):
            fh.write(f"**{k}:**\n" + "".join(f"- {x}\n" for x in v))
        else:
            fh.write(f"**{k}:** {v}\n")
OUT["premise_scope"] = scope

print("\nR06 COMPLETE:", f"{sum(CH)}/{len(CH)} checks PASS")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
import sys; sys.exit(0 if all(CH) else 1)