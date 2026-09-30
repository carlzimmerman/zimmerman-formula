#!/usr/bin/env python3
"""x04_final_table.py -- the pre-declared menu (PREDECLARED_MENU.md, hash-checked) evaluated once, ranked, with decoy calibration.

Units: c = 1, s = sqrt(G rho_Lambda) (so R* = 1/s, a0 = s/2), Lambda = 8 pi G rho_Lambda.  ratio := entry / a0 = 2 * (entry in units of s).
Exact hit: ratio == 1 (sympy exact).  near: |ratio - 1| < 0.13 (descriptor only).  pi-exponent e: ratio = (algebraic) * pi^e.
Controls: (1) planted R2 must hit; (2) mutating 4 pi -> 8 pi in V4 must move the ratio and not create a hit; (3) shuffled-menu false-positive rate for 'nearest entry within 13%';
(4) a decoy-target sweep t*a0, t in [0.2, 5] (log grid): how many entries fall within 13% of t*a0, and where t = 1 sits in that distribution.
Exit 0 = all pass.
"""
import json
import numpy as np
import sympy as sp
from common import Ledger

L = Ledger("x04")
ck, must = L.check, L.must_fail
pi = sp.pi

# ---- the declared menu (coefficients in units of s = c sqrt(G rho_Lambda)); definitions are the ones in PREDECLARED_MENU.md ----
V = {
    "V1": ("c H_Lambda = c sqrt(Lambda/3)", sp.sqrt(8 * pi / 3)),
    "V2": ("c sqrt(Lambda)  (ESU instability rate)", sp.sqrt(8 * pi)),
    "V3": ("c sqrt(2 Lambda)  (task-listed)", sp.sqrt(16 * pi)),
    "V4": ("c omega_J = c sqrt(4 pi G rho)  (plasma / wave-breaking dictionary)", sp.sqrt(4 * pi)),
    "V5": ("c sqrt(4 pi G rho/3)  (uniform-density oscillation)", sp.sqrt(4 * pi / 3)),
    "V6": ("c / t_ff = c sqrt(32 G rho/(3 pi))", sp.sqrt(32 / (3 * pi))),
}
entries = []
for key, (name, coef) in V.items():
    entries.append((key, name, coef))
for key, (name, coef) in V.items():
    entries.append(("W" + key[1:], "c^2/lambda, lambda = 2 pi c/omega, omega = " + name.split("  ")[0].split("c ", 1)[-1], coef / (2 * pi)))
w2 = [("4 pi G rho", 4 * pi), ("4 pi G rho/3", 4 * pi / 3), ("H_Lambda^2 = 8 pi G rho/3", 8 * pi / 3), ("Lambda = 8 pi G rho", 8 * pi)]
ells = [("R*/2", sp.Rational(1, 2)), ("R*", sp.Integer(1))]
idx = 1
for wn, wv in w2:
    for ln_, lv in ells:
        entries.append((f"P{idx}", f"omega^2 * ell, omega^2 = {wn}, ell = {ln_}", wv * lv))
        idx += 1
entries.append(("R1", "c^2/R*  (reference, not collective)", sp.Integer(1)))
entries.append(("R2", "c^2/(2 R*)  (PLANTED: the target)", sp.Rational(1, 2)))
ck("menu has exactly 22 entries (6 V + 6 W + 8 P + 2 R), as declared", len(entries) == 22)

x = sp.symbols("x", positive=True)


def pi_exponent(r):
    rr = sp.simplify(r).subs(pi, x)
    return sp.simplify(x * sp.diff(sp.log(rr), x))


rows = []
for key, name, coef in entries:
    ratio = sp.simplify(2 * coef)
    e = pi_exponent(ratio)
    rows.append(dict(id=key, name=name, coef=coef, ratio=ratio, ratio_f=float(ratio), e=e, hit=(sp.simplify(ratio - 1) == 0),
                     near=abs(float(ratio) - 1) < 0.13))

print("\nTABLE (unsorted, as declared)")
for rw in rows:
    print(f"  {rw['id']:3s} ratio to a0 = {rw['ratio_f']:9.4f}   pi^e, e = {str(rw['e']):5s}  exact hit: {str(rw['hit']):5s} near(13%): {str(rw['near']):5s}  {rw['name']}")

print("\nRANKED by |ln ratio| (distance from a0)")
ranked = sorted(rows, key=lambda d: abs(np.log(d["ratio_f"])))
for i, rw in enumerate(ranked, 1):
    dev = (rw["ratio_f"] - 1) * 100
    print(f"  {i:2d}. {rw['id']:3s} ratio {rw['ratio_f']:8.4f} ({dev:+7.1f}% vs a0)   factor needed {1 / rw['ratio_f']:7.4f}   e = {str(rw['e']):5s}  {rw['name']}")

hits = [rw["id"] for rw in rows if rw["hit"]]
print("\nexact hits:", hits)
ck("E1  exact hits are exactly {R2} (the planted target); no collective entry (V, W, P) hits", hits == ["R2"])
coll = [rw for rw in rows if rw["id"][0] in "VWP"]
ck("E2  every collective entry has a NON-ZERO pi exponent e (half-integer or integer) relative to sqrt(G rho_Lambda)", all(rw["e"] != 0 for rw in coll))
ck("E3  by Lindemann (pi transcendental), ratio = algebraic * pi^e with rational e != 0 can never equal 1: no entry of V, W, P can ever be exact; only R1, R2 have e = 0",
   [rw["id"] for rw in rows if rw["e"] == 0] == ["R1", "R2"])
must("E3-mut  a pi-free 'omega_J' (4 G rho instead of 4 pi G rho, ratio 4) would still pass the e != 0 test", pi_exponent(sp.Integer(4)) != 0)

# proper mutation checks
V4_mut = sp.simplify(2 * sp.sqrt(8 * pi))                       # 4 pi -> 8 pi in omega_J
ck("E4  mutation 4 pi -> 8 pi in V4 moves the ratio from 7.0898 to 10.0265 and does not create a hit", abs(float(V4_mut) - 10.0265) < 1e-3 and sp.simplify(V4_mut - 1) != 0)
r2 = [rw for rw in rows if rw["id"] == "R2"][0]
ck("E5  planted control R2 is detected as an exact hit (positive control of the scan)", r2["hit"])

near = [rw["id"] for rw in rows if rw["near"] and rw["id"] != "R2"]
print("\nentries within 13% of a0 (excluding planted R2):", near)
ck("E6  the only non-planted entries within 13% are W1 (=c H_Lambda/2 pi, Milgrom's form with H_Lambda; ratio 0.921) and W4 (=c^2/lambda_J; ratio 1.128)", sorted(near) == ["W1", "W4"])
W1 = [rw for rw in rows if rw["id"] == "W1"][0]
ck("E7  W1 ratio = Z/(2 pi) = sqrt(32 pi/3)/(2 pi) = 0.9213 (this is the known Milgrom-type coefficient 2 pi vs the framework's Z = 5.789)",
   abs(W1["ratio_f"] - float(sp.sqrt(32 * pi / 3) / (2 * pi))) < 1e-12 and abs(W1["ratio_f"] - 0.9213) < 1e-3)

# ---- decoy calibration: target multipliers ----
rat = np.array([rw["ratio_f"] for rw in coll])          # 20 collective entries
c1 = int(np.sum(np.abs(rat - 1) < 0.13))
sweeps = {}
for lo, hi in [(0.2, 5.0), (0.1, 10.0)]:
    ts = np.exp(np.linspace(np.log(lo), np.log(hi), 800))
    counts = np.array([int(np.sum(np.abs(rat / t - 1) < 0.13)) for t in ts])
    p_dec = float(np.mean(counts >= c1))
    sweeps[(lo, hi)] = (p_dec, float(counts.mean()), int(counts.max()), float(np.mean(counts >= 1)))
    print(f"DECOY SWEEP t in [{lo}, {hi}] (800 log-spaced targets t*a0): at t = 1 the number of the 20 collective entries within 13% is {c1};"
          f" mean over decoys {counts.mean():.2f}, max {counts.max()}, share with >= 1: {np.mean(counts >= 1):.2f};  share of decoys with >= {c1}: {p_dec:.3f}")
print("  note: W1 and W4 are not independent (omega_J = sqrt(3/2) H_Lambda, both are c*omega/(2 pi)); the W family alone puts six entries between 0.59 and 2.26.")
print("  FIRST-RUN CORRECTION: my a-priori expectation (>= 25% of decoys do as well) was WRONG; the measured share is 0.14-0.2, i.e. a0 sits at about the 80-86th percentile:")
print("  mildly favourable density, not significant at 5% (and the menu was written knowing the target).")
ck("E8  measured: the share of decoy targets with as many entries within 13% as a0 has is > 5% in both sweeps (a0 is not significantly special; p ~ 0.1-0.2)",
   all(v[0] > 0.05 for v in sweeps.values()))

# shuffled-menu control
rng = np.random.default_rng(20260929)
trials = 20000
ok = 0
for _ in range(trials):
    f = np.exp(rng.uniform(np.log(1 / 3), np.log(3), size=rat.size))
    if np.any(np.abs(rat * f - 1) < 0.13):
        ok += 1
fp = ok / trials
print(f"SHUFFLED-MENU CONTROL: probability that some entry of a random rescaling (log-uniform factor in [1/3, 3]) of this menu lies within 13% of a0: {fp:.3f}")
ck("E9  measured: a nearest entry within 13% occurs for > 5% of shuffled menus (here ~0.5): it is not a rare event", fp > 0.05)

# ---- summary numbers to feed the README ----
out = dict(rows=[dict(id=r["id"], name=r["name"], ratio=r["ratio_f"], pi_exponent=str(r["e"]), hit=r["hit"], near=bool(r["near"])) for r in rows],
           ranked=[r["id"] for r in ranked], exact_hits=hits, near_excluding_planted=near, decoy_counts_at_t1=c1,
           decoy_share_ge_observed={str(k): v[0] for k, v in sweeps.items()}, shuffled_false_positive=fp)
json.dump(out, open("x04_final_table.json", "w"), indent=1)
L.finish()
