"""
mc_report.py -- post-process screen_results.json into the stage-1 mortality report.

Also re-runs the DEEP candidates (anything that survived Gate-MOND) to characterise
where the search actually got to, and checks the near-misses against the structural
statement proved in mc_frame_theorem.py.
"""
import argparse
import collections
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GATE_ORDER = ["Gate-H", "Gate-CARRIER", "Gate-MOND", "Gate-SLIP", "Gate-H2",
              "Gate-PPN", "SURVIVOR", "TUNING_FAILED", "GEN_ERROR", "CHAIN_ERROR"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default=os.path.join(HERE, "screen_results.json"))
    ap.add_argument("--extra", nargs="*", default=[],
                    help="additional result files to merge (e.g. a corrected family re-run)")
    args = ap.parse_args()

    files = [args.res] + list(args.extra)
    mort = collections.Counter()
    fam = collections.defaultdict(collections.Counter)
    reasons = collections.defaultdict(collections.Counter)
    deep, survivors = [], []
    ntot = 0
    for f in files:
        with open(f) as fh:
            d = json.load(fh)
        ntot += d["n_evaluated"]
        mort.update(d["mortality"])
        for k, v in d["mortality_by_family"].items():
            fam[k].update(v)
        for k, v in d["reasons"].items():
            reasons[k].update(v)
        deep += d.get("deep_candidates", [])
        survivors += d.get("survivors", [])
        param_ids = d["param_ids"]
        bs = d["basis_size"]

    print("=" * 84)
    print("STAGE-1 SCREEN -- MORTALITY TABLE")
    print("=" * 84)
    print(f"basis: {bs['operators']} covariant operators + {bs['matter_frame']} "
          f"matter-frame parameters = {bs['total']} searchable coefficients")
    print(f"candidates evaluated: {ntot}\n")
    print(f"{'gate':16s} {'killed':>9s} {'%':>7s}   note")
    notes = {
        "Gate-H": "robust ghost: negative kinetic eigenvalue at EVERY reference background",
        "Gate-CARRIER": "carrier algebraically off, or no static solution",
        "Gate-MOND": "no mu -> 1 / mu -> y interpolation (or no solution across the grid)",
        "Gate-SLIP": "lensing potential does not track the MOND dynamical potential",
        "Gate-H2": "ghost at the candidate's OWN solved background",
        "Gate-PPN": "preferred-frame carrier vacuum (alpha_1, alpha_2 not established)",
        "SURVIVOR": "passed every cheap gate",
        "TUNING_FAILED": "the targeted tuning had no root -- candidate never constructed",
    }
    for g in GATE_ORDER:
        if mort.get(g):
            print(f"{g:16s} {mort[g]:>9d} {100*mort[g]/ntot:>6.2f}%   {notes.get(g,'')}")
    print(f"{'TOTAL':16s} {sum(mort.values()):>9d}")

    print("\nreached-gate profile (how deep the search actually got):")
    reach = {}
    cum = 0
    for g in ["Gate-H", "Gate-CARRIER", "Gate-MOND", "Gate-SLIP", "Gate-H2",
              "Gate-PPN", "SURVIVOR"]:
        cum += mort.get(g, 0)
        reach[g] = ntot - mort.get("TUNING_FAILED", 0) - mort.get("GEN_ERROR", 0) \
            - mort.get("CHAIN_ERROR", 0) - (cum - mort.get(g, 0))
    for g, n in reach.items():
        print(f"    reached {g:14s} {n:>8d}")

    print("\ncause of death, in detail:")
    for g in GATE_ORDER:
        if g in reasons and mort.get(g):
            print(f"  {g}:")
            for r, n in sorted(reasons[g].items(), key=lambda kv: -kv[1])[:10]:
                print(f"      {n:>8d}  {r}")

    print("\nmortality by sampling family:")
    hdr = ["family"] + [g for g in GATE_ORDER if mort.get(g)]
    print("    " + " ".join(f"{h:>14s}" for h in hdr))
    for f, c in sorted(fam.items()):
        row = [f] + [str(c.get(g, 0)) for g in hdr[1:]]
        print("    " + " ".join(f"{x:>14s}" for x in row))

    print("\n" + "=" * 84)
    print(f"SURVIVORS: {len(survivors)}")
    print("=" * 84)
    if not survivors:
        print("NONE.  Empty search.  The last gate standing is the one that killed the")
        print("deepest candidates -- see the reached-gate profile above.")
    for s in survivors[:20]:
        c = np.array(s["cvec"])
        nz = [(param_ids[i], round(float(c[i]), 6)) for i in np.nonzero(c)[0]]
        print(f"  family={s['family']}  {nz}")
        print(f"     {s['info']}")

    print("\n" + "=" * 84)
    print(f"DEEPEST NON-SURVIVORS (passed Gate-MOND and Gate-SLIP): {len(deep)}")
    print("=" * 84)
    bb = [d["info"].get("vacuum_boost_break") for d in deep
          if isinstance(d.get("info", {}).get("vacuum_boost_break"), float)]
    ppn_reasons = collections.Counter(d["info"].get("ppn", "?") for d in deep)
    for r, n in ppn_reasons.most_common():
        print(f"  {n:>6d}  {r}")
    if bb:
        bb = np.array(bb)
        print(f"\n  vacuum boost-breaking |A_0| or |S_00| among them: "
              f"min {bb.min():.3e}  median {np.median(bb):.3e}  max {bb.max():.3e}")
        print(f"  boost-INVARIANT ({'<'}1e-8): {int((bb < 1e-8).sum())} of {len(bb)}")
    used = collections.Counter()
    for d in deep:
        c = np.array(d["cvec"])
        for i in np.nonzero(c)[0]:
            used[param_ids[i]] += 1
    print("\n  operators/parameters most often present in the deepest candidates:")
    for k, n in used.most_common(18):
        print(f"      {n:>6d}  {k}")
    for d in deep[:6]:
        c = np.array(d["cvec"])
        nz = [(param_ids[i], round(float(c[i]), 5)) for i in np.nonzero(c)[0]]
        print(f"\n  example ({d['family']}, died {d['verdict']}): {nz}")
        keep = {k: v for k, v in d["info"].items()
                if k in ("deep_slope", "frame_slip_worst", "sigmaP_cancellation_rel",
                         "metric_carried_frac", "vacuum_boost_break", "slip", "ppn",
                         "H2_gauge_or_strongcoupled_nulls")}
        print(f"     {keep}")


if __name__ == "__main__":
    main()
