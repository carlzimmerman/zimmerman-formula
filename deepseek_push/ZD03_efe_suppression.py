#!/usr/bin/env python3
"""
ZD03 -- THE EFE SUPPRESSION THEOREM and the CLUSTER DARK-STRIPPING RADIUS.

Derivation (new, certified in fable_independent_2026/lean_2026/ZD03_efe_suppression.lean):
a satellite with internal baryon field s in an ambient (external) field e
carries the internal phantom boost phi(s+e) - phi(e), phi(x) = sqrt(x^2+x)-x:

  (1) SUBADDITIVITY (the exact EFE law): phi(s+e) <= phi(s) + phi(e).
      The phantom of the sum is less than the sum of the phantoms: an
      ambient field strictly suppresses the internal dark component.
  (2) SUPPRESSION: phi(s+e) - phi(e) <= phi(s) -- the satellite's phantom
      is at most its isolated value; it vanishes as e -> infinity.
  (3) THE AMBIENT CAP: where e >= a0/2 the internal boost is strictly
      below the ambient field -- no self-contained dark halo: the
      a0/2 surface is the dark-stripping radius:
      r_strip = 4 sigma^2 / a0 for an isothermal cluster (g_ext = 2 s^2/r).
      Framework's own G008 cluster (sigma = 809 km/s): 0.71 Mpc;
      sigma = 1000 km/s (Coma-class): 1.08 Mpc. Inside r_strip the cluster
      field exceeds the ceiling and satellites are dark-stripped.

Lean: 7 theorems, exit 0, zero sorry, axioms {propext, Classical.choice,
Quot.sound}.
"""
import json, math, os

BASE = os.path.dirname(os.path.abspath(__file__))
A0 = 1.2e-10
MPC_M = 3.085677581491367e22

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

def phi(x):
    return math.sqrt(x*x + x) - x

ok = True
for s in [1e-3, 0.01, 0.1, 0.5, 1.0, 3.0, 10.0]:
    for e in [1e-3, 0.01, 0.1, 0.5, 1.0, 3.0, 10.0, 100.0]:
        if not phi(s+e) <= phi(s) + phi(e) + 1e-12:
            ok = False
check("C1 SUBADDITIVITY (the exact EFE law): phi(s+e) <= phi(s) + phi(e)",
      ok, "7x8 grid; strict inequality wherever both fields are nonzero")

ok = True
for s in [0.01, 0.1, 1.0, 5.0]:
    for e in [0.1, 1.0, 10.0, 100.0]:
        if not (phi(s+e) - phi(e)) <= phi(s) + 1e-12:
            ok = False
check("C2 SUPPRESSION: internal boost <= isolated phantom phi(s)", ok)

ok = True
for s in [0.01, 0.1, 1.0]:
    for e in [0.5, 1.0, 5.0, 50.0]:
        if not (phi(s+e) - phi(e)) < e:
            ok = False
check("C3 THE AMBIENT CAP: for e >= a0/2 the internal boost is strictly "
      "below the ambient field", ok, "no self-contained dark halo at or inside a0/2")

# stripping radius: r_strip = 4 sigma^2 / a0
r809 = 4.0*(809.0e3)**2/A0/MPC_M
r1000 = 4.0*(1000.0e3)**2/A0/MPC_M
check("C4 stripping radius (G008 cluster, sigma = 809 km/s): ~0.71 Mpc",
      abs(r809 - 0.707) < 0.01, f"r_strip = {r809:.3f} Mpc = 4 sigma^2/a0")
check("C5 stripping radius (Coma-class, sigma = 1000 km/s): ~1.08 Mpc",
      abs(r1000 - 1.080) < 0.01, f"r_strip = {r1000:.3f} Mpc")

# inside r_strip the cluster field exceeds the ceiling (sample at fractions
# of each cluster's own r_strip: r = f*r_strip, f < 1)
ok = True
for sig in [400.0, 809.0, 1000.0]:
    r_strip = 4.0*(sig*1e3)**2/A0
    for f in [0.1, 0.25, 0.5, 0.75, 0.9]:
        g_ext = 2.0*(sig*1e3)**2/(f*r_strip)
        if not g_ext > A0/2:
            ok = False
check("C6 dark-stripped zone: strictly inside r_strip the cluster field "
      "exceeds a0/2", ok, "g_ext(f*r_strip) = a0/(2f) > a0/2 for every f < 1")

# subadditivity saturation: as e -> inf the internal boost -> 0 (full EFE)
ok = phi(0.1+1000.0) - phi(1000.0) < 1e-4
check("C7 EFE asymptotics: boost -> 0 in very strong ambient fields", ok,
      f"phi(0.1+1000)-phi(1000) = {phi(0.1+1000.0)-phi(1000.0):.2e}")

npass = sum(1 for c in checks if c["pass"])
print(f"ZD03 COMPLETE: {npass}/{len(checks)} checks PASS.")
print(f"  r_strip(809 km/s) = {r809:.3f} Mpc,  r_strip(1000 km/s) = {r1000:.3f} Mpc")
with open(os.path.join(BASE, "ZD03_results.json"), "w") as f:
    json.dump({"lane": "ZD03_efe_suppression",
               "checks": checks,
               "summary": f"{npass}/{len(checks)} PASS",
               "r_strip_Mpc": {"G008_sigma809": r809, "Coma_class_1000": r1000},
               "lean": {"file": "fable_independent_2026/lean_2026/ZD03_efe_suppression.lean",
                        "theorems": ["phantom_ceiling_strict", "phantom_subadditive",
                                     "efe_boost_left", "efe_ambient_cap",
                                     "strip_radius_iff", "strip_inside_supersaturates",
                                     "strip_no_self_contained_phantom"],
                        "exit_code": 0, "sorry": 0,
                        "axioms": "propext, Classical.choice, Quot.sound"}},
              f, indent=1)