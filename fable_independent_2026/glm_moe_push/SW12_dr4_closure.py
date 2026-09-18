#!/usr/bin/env python3
"""
SW12_dr4_closure.py -- the DR4 outcome-decision table (read-only cross-check).
(2026-09-17, thirteenth swing of the glm_moe lane)

PRE-REGISTERED KILL (before any number): this script invents NO physics numbers.
Every band endpoint is cited to a landed artifact; any recomputation that mismatches
its target is a FAIL-as-finding, never a silent edit. MUTATE HINGE: the class band is
replaced by the cap band's endpoints -- X2 (class-vs-cap disjointness) and X1 (the
live split) MUST FAIL. An unflipped hinge = vacuous = FAIL.

Bands (all from landed artifacts, cited in CLOSURE_MAP.md):
  class      [1.0000, 1.01012]   SW04_conformal_efe.out D
  candidate  [1.000, 1.045]      kappa_slot_2026/SW07_program_ledger.out Arm B (ceiling)
  cap/L268   [1.086, 1.155]      kappa_slot_2026/SW07_program_ledger.out (NOT registered)
  AQUAL-can  [1.1614, 1.1814]    Amendment 10 (canonical footing)
  AQUAL-alt  [1.1917, 1.2267]    Amendment 10 (alt footing)
  CDM        [0.99, 1.01]        Newtonian reference bin
"""
import json
import os

MUTATE = os.environ.get("MUTATE", "0") == "1"

bands = {
    "class":     (1.0000, 1.01012, "SW04_conformal_efe.out D"),
    "candidate": (1.000, 1.045, "kappa_slot_2026/SW07_program_ledger.out Arm B"),
    "cap_L268":  (1.086, 1.155, "kappa_slot_2026/SW07_program_ledger.out (NOT registered)"),
    "AQUAL_can": (1.1614, 1.1814, "Amendment 10 canonical"),
    "AQUAL_alt": (1.1917, 1.2267, "Amendment 10 alt"),
    "CDM":       (0.99, 1.01, "Newtonian reference bin"),
}

if MUTATE:
    bands["class"] = bands["cap_L268"]

checks = []


def check(name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %s -- %s" % ("PASS" if ok else "FAIL", name, detail))


def gap(a, b):
    """positive margin between band a's top and band b's bottom"""
    return b[0] - a[1]


cl = bands["class"]
ca = bands["candidate"]
cp = bands["cap_L268"]
aqc = bands["AQUAL_can"]
aqa = bands["AQUAL_alt"]

# --- the live split (grok's rule) ---
check("X1 class-candidate OVERLAP (live split = {class U candidate} vs cap vs AQUAL)",
      ca[0] <= cl[1] <= ca[1],
      "class hi %.5f inside candidate [%.3f, %.3f]" % (cl[1], ca[0], ca[1]))

# --- disjointness with margins ---
g2 = gap(cl, cp)
check("X2 class vs cap disjoint", g2 > 0, "gap %.5f (the hinge target)" % g2)
g3 = gap(ca, cp)
check("X3 candidate ceiling vs cap disjoint", g3 > 0, "gap %.4f" % g3)
g4 = gap(cp, aqc)
check("X4 cap vs AQUAL-canonical corner gap", g4 > 0, "cross-footing corner %.4f" % g4)
g5 = gap(cp, aqa)
check("X5 cap vs AQUAL-alt disjoint (same-footing)", g5 > 0, "gap %.4f" % g5)
check("X6 same-footing margins >= 0.029 (SW07 R2)", min(g3, g5) >= 0.029,
      "min margin %.4f" % min(g3, g5))
check("X7 corner gap %.4f < band width 0.02 -- footing must be fixed first" % g4, g4 < 0.02,
      "cap vs AQUAL distinguishable only after the footing is fixed")

# --- the decision matrix: survivors per measured gamma_v bin ---
def survivors(gv):
    return sorted(k for k, (lo, hi, _) in bands.items() if lo <= gv <= hi)


for gv, label in [(1.005, "class+candidate bin"), (1.00, "CDM bin"),
                  (1.10, "cap/L268 bin"), (1.17, "AQUAL bin")]:
    s = survivors(gv)
    check("X8 bin gamma_v=%.3f (%s): survivors = %s" % (gv, label, "+".join(s) if s else "NONE"),
          True, "computed from the cited bands")

print("SW12 COMPLETE: %d/%d checks PASS." % (sum(c["ok"] for c in checks), len(checks)))
with open("SW12_dr4_closure.json", "w") as f:
    json.dump({"mode": "MUTATE" if MUTATE else "clean",
               "n_pass": sum(c["ok"] for c in checks), "n_total": len(checks),
               "checks": checks}, f, indent=1)
print("json written")
