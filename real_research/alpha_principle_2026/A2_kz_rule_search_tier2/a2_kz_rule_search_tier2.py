#!/usr/bin/env python3
"""A2 -- tier 2 of the decoy-calibrated zero-knob rule search (34,992,000 rules).  Pre-registered in A2_PREREGISTRATION.md; same method as lane A1 with a different declared grammar.
Imports lane Y1's validated running READ-ONLY (path-relative).
Run:    python3 a2_kz_rule_search_tier2.py            (exit 0 iff all declared checks pass; the number of real hits is REPORTED, not asserted)
MUTATE: python3 a2_kz_rule_search_tier2.py MUTATE     (the search grammar loses its largest multiplier while planted rules still use it; exactly S3 must fail: exit 1; exit 3 if broken)
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("Y1_running_precision", "B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
FAILED = []
PI = math.pi
KAPPA = 0.5
Z = 2 * math.sqrt(8 * PI / 3)
MP, MRED = 1.22089e19, 2.435e18
SCALES = {"M_P": MP, "M_red": MRED, "M_red/sqrt(118)": MRED / math.sqrt(118), "M_P/Z": MP / Z}
REL = np.array([0.0023, 0.00021, 0.0012])
NSIG = 3.0
from fractions import Fraction
_fr = sorted({Fraction(a, b) for a in range(1, 9) for b in range(1, 9)})
C_FULL = np.array([float(f) for f in _fr])      # 45 distinct rationals p/q, p, q in 1..8
C = C_FULL[:-1] if MUT else C_FULL             # MUTATE: the search grammar silently LOSES its last multiplier (8/1... the largest value) while planted rules are still drawn from the full set
EXPS_RP = [-1, 0, 1, 2]
EXPS_Q = [-1, 0, 1]
MONO = np.array([PI ** r * Z ** p * KAPPA ** q for r in EXPS_RP for p in EXPS_RP for q in EXPS_Q])
MONO_LAB = [(r, p, q) for r in EXPS_RP for p in EXPS_RP for q in EXPS_Q]


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


def search(targets, tol_sig=NSIG, want_list=False):
    """targets: array (n_sets, 3).  Returns the number of hitting rules and (optionally) the list of hits (set index, mono index, c-triple)."""
    hits = 0
    lst = []
    w = tol_sig * REL
    for si, t in enumerate(targets):
        for mi, A in enumerate(MONO):
            feas = []
            for i in range(3):
                ok = np.abs(C * A - t[i]) <= w[i] * t[i] + (1e-12 if tol_sig == 0.0 else 0.0)
                feas.append(np.where(ok)[0])
            if all(len(f) for f in feas):
                n = len(feas[0]) * len(feas[1]) * len(feas[2])
                hits += n
                if want_list:
                    for a in feas[0]:
                        for b in feas[1]:
                            for c in feas[2]:
                                lst.append((si, mi, (C[a], C[b], C[c])))
    return hits, lst


print("A2: tier-2 decoy-calibrated search over zero-knob rules for the three gauge couplings   (MUTATE=%s)" % MUT)
tr = L.run_central(mu_max=1e21)
labels, targets = [], []
for sn, S in SCALES.items():
    aY, a2, a3 = tr.A(S)
    labels.append((sn, "Y"));   targets.append([aY, a2, a3])
    labels.append((sn, "GUT")); targets.append([0.6 * aY, a2, a3])
targets = np.array(targets)
n_rules = len(MONO) * len(C) ** 3 * len(targets)
print(f"  rules: {len(MONO)} monomials x {len(C)}^3 multiplier triples x {len(targets)} (scale, normalisation) sets = {n_rules:,}")
for (sn, nm), t in zip(labels[:4], targets[:4]):
    print(f"    target ({sn}, {nm}): {t[0]:.4f} {t[1]:.4f} {t[2]:.4f}")

real_hits, real_list = search(targets, want_list=True)
print(f"\n  REAL hits (all three within {NSIG:g} sigma): {real_hits}")
for (si, mi, cs) in real_list[:20]:
    A = MONO[mi]
    off = [(cs[i] * A - targets[si][i]) / (REL[i] * targets[si][i]) for i in range(3)]
    print(f"    {labels[si]} monomial pi^{MONO_LAB[mi][0]} Z^{MONO_LAB[mi][1]} kappa^{MONO_LAB[mi][2]}  c = {tuple(round(float(c), 4) for c in cs)}  offsets (sigma) = {[round(o, 2) for o in off]}")

# decoys
rng = np.random.default_rng(20260929)
K = 4000
dec_hits = 0
dec_counts = []
for _ in range(K):
    u = rng.uniform(0.03, 0.5, size=3) * rng.choice([-1, 1], size=3)
    h, _l = search(targets * (1 + u), tol_sig=NSIG)
    dec_counts.append(h)
    dec_hits += (h > 0)
p_chance = dec_hits / K
print(f"\n  decoys: {K} shifted target sets; decoys with at least one hit: {dec_hits}  ->  P_chance = {p_chance:.4g}  (mean hits per decoy {np.mean(dec_counts):.4g})")
chk("S1 the search is powered: P_chance < 1e-2", p_chance < 1e-2, f"(P_chance = {p_chance:.3g}; 95% upper bound {(3.0 / K if dec_hits == 0 else (dec_hits + 2 * math.sqrt(dec_hits)) / K):.2g})")

# positive control: plant a rule and check it is found
rng2 = np.random.default_rng(7)
found = 0
NPL = 200
for _ in range(NPL):
    mi = int(rng2.integers(len(MONO)))
    cs = C_FULL[rng2.integers(len(C_FULL), size=3)]
    planted = np.array([cs[i] * MONO[mi] for i in range(3)])
    h, _l = search(np.array([planted]), tol_sig=NSIG)
    found += (h > 0)
chk("S3 planted rules are recovered 100% of the time", found == NPL, f"({found}/{NPL})")

print("\nVERDICT (against the declared criteria):")
powered = p_chance < 1e-2
if real_hits == 0:
    print(f"  No hit: none of the {n_rules:,} zero-knob rules reproduces the three couplings at any of the 4 declared scales in either normalisation within 3 sigma of the validated running.")
    if powered:
        print(f"  With P_chance = {p_chance:.3g} the search is powered at the declared standard (< 1e-2): the absence of a hit is informative.")
    else:
        print(f"  BUT P_chance = {p_chance:.3g} is NOT below the declared 1e-2: this tier is NOT powered at the pre-registered standard, so its null is only weakly informative (a real hit would have had a {100 * p_chance:.1f}% chance of being a coincidence).")
else:
    print(f"  {real_hits} real hit(s) listed above. LEAD only if P_chance < 1e-3 (here {p_chance:.3g}); no physical reading is claimed; goes to adversarial follow-up.")
print("  alpha stays an INPUT; kappa = 1/2 FITTED.")
if MUT:
    works = [t.split()[0] for t in FAILED] == ["S3"]
    print("\nMUTATE CONTROL: search grammar missing its largest multiplier; failed:", [t.split()[0] for t in FAILED], "->", "the control works (exit 1)" if works else "CONTROL BROKEN (exit 3): it must fail exactly S3")
    sys.exit(1 if works else 3)
sys.exit(0 if not FAILED else 1)
