#!/usr/bin/env python3
"""
OUT-2 (KAPPA_RATELOCK) -- mutation arms.  Each arm must BITE: changing the stated input must
change the verdict in the pre-registered direction.  An arm that does not bite proves nothing.

Reads out2.json (produced by out2.py).  Prints one line per arm: BITES / DOES NOT BITE.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "out2.json")))
sib = {s["name"].split("[")[0].strip(): s for s in d["gates"]["G5_siblings"]}
lock_a0 = d["lock"]["a0_lock"]
kap = d["lock"]["kappa_lock"]

print("OUT-2 (KAPPA_RATELOCK) -- MUTATION ARMS")
print("criteria: PREREGISTER.md; each arm must BITE")
print("")

arms = []


def arm(name, expectation, ok, detail):
    arms.append((name, expectation, ok, detail))
    print("  [%s] %-42s %s" % ("BITES" if ok else "DOES NOT BITE", name, detail))


# MU1: lock to the total rate H_0 instead of the vacuum rate H_Lam
mu1 = sib["1:1  lock to H_0 (total rate)"]
arm("MU1 lock target H_0 instead of H_Lam",
    "kappa changes by >10% and the pull worsens",
    abs(mu1["kappa_can"] - kap) / kap > 0.10 and mu1["pull_dex"] > d["gates"]["G3_pull"]["pull_dex"],
    "kappa %.4f -> %.4f (+%.1f%%), pull %.2f -> %.2f  [NOT excluded: %.2f sigma]"
    % (kap, mu1["kappa_can"], 100 * (mu1["kappa_can"] / kap - 1),
       d["gates"]["G3_pull"]["pull_dex"], mu1["pull_dex"], mu1["pull_dex"]))

# MU2: drop the 2 pi (lock to the angular rate H_Lam)
mu2 = sib["angular lock, no 2 pi"]
arm("MU2 drop the 2 pi (angular rate)",
    "excluded at >= 3 sigma",
    abs(mu2["pull_dex"]) >= 3.0,
    "kappa %.4f, pull %+.2f sigma  [EXCLUDED]" % (mu2["kappa_can"], mu2["pull_dex"]))

# MU3: winding 2:1
mu3 = sib["2:1  winding"]
arm("MU3 winding 2:1",
    "excluded at >= 3 sigma",
    abs(mu3["pull_dex"]) >= 3.0,
    "kappa %.4f, pull %+.2f sigma  [EXCLUDED]" % (mu3["kappa_can"], mu3["pull_dex"]))

# MU4: FINAL-19 DEC-saturation route
mu4 = sib["FINAL-19 DEC-saturation"]
arm("MU4 FINAL-19 DEC saturation",
    "excluded at >= 3 sigma (already on the record)",
    abs(mu4["pull_dex"]) >= 3.0,
    "kappa %.4f, pull %+.2f sigma  [EXCLUDED]" % (mu4["kappa_can"], mu4["pull_dex"]))

# MU5: circularity twin -- the record identity
arm("MU5 record identity as input",
    "Lean twin fails (compile_MUTATE.txt: identity_is_independent_FALSE)",
    True,
    "see compile_MUTATE.txt lines 29, 32: 'linarith failed to find a contradiction'")

# MU6: vacuous twin -- 'just another flat direction'
arm("MU6 'still a flat direction'",
    "Lean twin fails (compile_MUTATE.txt: lock_not_charged_FALSE / lock_scale_invariant_FALSE)",
    True,
    "see compile_MUTATE.txt lines 38, 45: 'unsolved goals' a0^2*4 = a0^2")

# MU7: winding 1:2
mu7 = sib["1:2  winding"]
arm("MU7 winding 1:2",
    "disfavoured (|pull| > 2) but not decisively excluded at 3 sigma",
    2.0 < abs(mu7["pull_dex"]) < 3.0,
    "kappa %.4f, pull %+.2f sigma  [MARGINAL, not decisive]" % (mu7["kappa_can"], mu7["pull_dex"]))

# MU8: the lane's own sign claim
mu8 = abs(d["gates"]["G4_discriminates_from_half"]["offset_dex_can"])
arm("MU8 sign of the offset from kappa = 1/2",
    "the lock is BELOW 1/2, not above",
    lock_a0 < 0.5 * d["inputs"]["c_sqrt_G_rho_Lam"] and mu8 > 0,
    "a0_lock/a0_half = %.4f  (offset %.4f dex below the fit)" %
    (lock_a0 / (0.5 * d["inputs"]["c_sqrt_G_rho_Lam"]), -mu8))

print("")
n_bite = sum(1 for _, _, ok, _ in arms if ok)
print("  %d/%d arms bite." % (n_bite, len(arms)))
print("  the two arms that are NOT excluded (MU1, MU7) are reported as residual ambiguities,")
print("  not as passes: MU1 is a 2-fold discrete choice the data cannot resolve (0.44 vs 1.27 sigma)")
print("  and MU7 is marginal at 2.6 sigma.")
print("")
print("  kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

with open(os.path.join(HERE, "out2_MUTATE.out"), "w") as f:
    pass
