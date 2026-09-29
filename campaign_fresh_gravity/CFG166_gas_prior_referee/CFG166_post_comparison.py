#!/usr/bin/env python3
"""CFG166 POST-COMPARISON diagnostics (written AFTER my main, MUTATE and attack runs were saved; not part of the frozen main).
Reads CFG164's committed results JSON (read-only) and prints a class-probability/statistics comparison against my converged run.
Run: ZF_REPO=<repo> python3 CFG166_post_comparison.py > CFG166_post_comparison.out   (after CFG166_main_results.json exists)"""
import os, sys, json, math
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("ZF_REPO")
if not REPO:
    d = HERE
    for _ in range(10):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            REPO = d; break
        d = os.path.dirname(d)
T = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG164_gas_prior_results.json")))["numbers"]
M = json.load(open(os.path.join(HERE, "CFG166_main_results.json")))
conv, par = M["converged"], M["parity"]
mp = {"primary, h 0": "primary", "primary, h 0.5": "h=0.5", "primary, h 1": "h=1.0", "variant M, h 0": "variantM", "variant Z, h 0": "variantZ", "alpha_CO ULIRG, h 0": "alphaCO_ULIRG"}
cm = {"lean flat": "flat", "lean rival": "rival", "both within 2 sigma": "both", "neither": "neither"}
print("CFG164 (theirs, N=4000 seed 164) vs CFG166 converged (N=40000) and parity (N=4000, seed 164, different stream)")
mxall = 0.0
for k, v in T["priors"].items():
    c, p = conv[mp[k]], par[mp[k]]
    print(f"\n[{k}] mu-bar median/16/84: theirs {v['mu_bar_16_50_84'][1]:.3f}/{v['mu_bar_16_50_84'][0]:.3f}/{v['mu_bar_16_50_84'][2]:.3f}  mine {c['median']:.3f}/{c['p16']:.3f}/{c['p84']:.3f}  (parity {p['median']:.3f})")
    print(f"   windows (median mu) theirs {dict((a, round(b, 3)) for a, b in v['windows_median'].items())}")
    print(f"                       mine   {dict((a, round(b, 3)) for a, b in c['P1_mbar'].items())}")
    print(f"   per-disc windows theirs {dict((a, round(b, 3)) for a, b in v['windows_per_disc'].items())} mine {dict((a, round(b, 3)) for a, b in c['P1_disc'].items())}")
    print(f"   KURVS-15 theirs {dict((a, round(b, 3)) for a, b in v['kurvs15'].items())}" + (f" mine {dict((a, round(b, 3)) for a, b in c['P3'].items())}" if 'P3' in c else ""))
    worst = 0.0
    for s, pr in v["probs"].items():
        for kk, cc in cm.items():
            d = abs(pr.get(kk, 0.0) - c["P2"][s][cc])
            worst = max(worst, d)
            sd = math.sqrt(max(pr.get(kk, 0.0) * (1 - pr.get(kk, 0.0)), 1e-6) / 4000)
    mxall = max(mxall, worst)
    print(f"   max |class prob diff| over 5 s x 4 classes: {worst:.3f}")
    for s in ("1.00", "1.42", "1.62", "1.69", "3.00"):
        print(f"   s={s}: theirs " + ", ".join(f"{a} {b:.3f}" for a, b in v["probs"][s].items()) + " | mine " + ", ".join(f"{a} {c['P2'][s][a]:.3f}" for a in ('flat', 'rival', 'both', 'neither')))
print(f"\nlargest class-probability difference anywhere: {mxall:.3f}")
print("their X:", T["X"]["p_lean_rival"], T["X"]["median_mu"])
print("their verdict:", T["verdict"])
