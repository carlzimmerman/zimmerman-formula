#!/usr/bin/env python3
"""run_forced_pair_depth.py -- the SWITCHED runner: build + sweep one depth with the forced pair
                               chosen by ATOMOS_FORCED_PAIR (default = the PUBLISHED pair).

    python3 kappa_rerun/run_forced_pair_depth.py --depth 6                     # published pair
    ATOMOS_FORCED_PAIR=kappa python3 kappa_rerun/run_forced_pair_depth.py --depth 6   # {3, kappa}
    python3 kappa_rerun/run_forced_pair_depth.py --depth 6 --mode kappa        # explicit

NOTHING committed is edited. The forced pair is swapped only inside kappa_forced.forced_pair(),
which snapshots and restores gate.registry.FORCED_CONSTRAINTS in place and restores
exhaust._default_germs. With the switch OFF this file runs the COMMITTED machinery verbatim
(exhaust_depthN_forced.constructive_gate_b_reachables + the real gate.validate), which is why
regression_published.py can use it to reproduce the committed depth-6 numbers exactly.

The sweep predicate is the committed one, byte-for-byte:
    tol  = engine.scoring.measurement_tol(target)
    hit <=> engine.scoring.score_value(value, target).rel_error <= tol
and every hit is judged by the REAL gate (gate.validate on exhaust.gate_candidate_for) --
never a reimplementation.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import mpmath as mp
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import exhaust as EX                                            # noqa: E402
from exhaust import build_alphabet, Reachable, gate_candidate_for, resolve_target  # noqa: E402
from engine.scoring import score_value, measurement_tol         # noqa: E402
from gate import validate                                       # noqa: E402
import exhaust_depth5_forced as D5                              # noqa: E402
import exhaust_depthN_forced as DN                               # noqa: E402
from exhaust_depth5_forced import N_TARGETS                     # noqa: E402
from exhaust_parallel import sm_target_keys                     # noqa: E402

from kappa_forced import (                                      # noqa: E402
    forced_pair, mode_from_env, assert_field_exists, assert_no_holdout,
)

RESULTS = Path(_HERE) / "results_kappa_rerun"


def build_and_sweep(depth: int, targets: List[str], verbose: bool = True) -> Dict:
    """Build the Gate-B-passable dimensionless set at `depth` with the CURRENTLY ACTIVE forced
    pair, then sweep `targets`. Must be called INSIDE a forced_pair(...) context."""
    alpha = build_alphabet(None, None)
    forced_now = D5._forced_keys_present(alpha)
    if len(forced_now) != 2:
        raise SystemExit(f"FORCED-PAIR GUARD: {len(forced_now)} forced germ keys present "
                         f"({forced_now}); exhaust_depthN_forced._germ_recipes assumes EXACTLY 2 "
                         f"(keys=(forced[0],forced[1],free)) -- refusing to run a mis-specified search")
    free_now = D5._free_germ_keys(alpha)
    if verbose:
        print(f"  alphabet: {len(alpha.leaves)} leaves, {len(alpha.germs)} germs")
        print(f"  FORCED germ keys : {forced_now}")
        print(f"  n_free germs     : {len(free_now)}")
        print(f"  budget splits    : {DN.budget_splits(depth)}")

    t0 = time.time()
    reach, counts = DN.constructive_gate_b_reachables(alpha, depth, value_cap=None)
    build_s = time.time() - t0
    if verbose:
        print(f"  build: raw={counts['raw_candidates']:,} distinct={counts['distinct_by_value']:,} "
              f"skeletons={counts['n_skeletons_total']:,}  ({build_s:.1f}s)")

    vals = np.fromiter((float(r.value) for r in reach), dtype=np.float64, count=len(reach))

    reports = []
    all_hits = []
    for tk in targets:
        tspec = resolve_target(tk)
        tol = measurement_tol(tspec.pdg_target)
        tv = float(tspec.value)
        idxs = np.nonzero(np.abs(vals - tv) <= abs(tv) * tol * (1.0 + 1e-9))[0]
        hits = []
        for i in idxs:
            r = reach[int(i)]
            card = score_value(float(r.value), tspec.pdg_target)
            if card.rel_error > tol:
                continue
            gc = gate_candidate_for(r, alpha, tk, tspec.pdg_target, N_TARGETS)
            v = validate(gc)                       # THE REAL COMMITTED GATE
            assert_field_exists(v, "status", "gate verdict")       # bug-#1 field guard
            assert_field_exists(v, "kernel", "gate verdict")
            h = dict(target=tk, formula=r.formula, value=float(r.value),
                     rel_error=card.rel_error, n_sigma=card.n_sigma,
                     gate_status=v.status, kernel_passed=bool(v.kernel.passed),
                     fdr_bits=v.fdr.bits, fdr_mode=v.fdr.mode, gate_tell=v.tell)
            hits.append(h)
        hits.sort(key=lambda h: h["rel_error"])
        # FILTER BY THE FIELD THAT EXISTS (bug #1: 'fdr_dead'/'verdict' do NOT exist)
        for h in hits:
            assert_field_exists(h, "gate_status", "hit record")
        cert = [h for h in hits if h["gate_status"] == "CERTIFIED"]
        relab = [h for h in hits if h["gate_status"] == "REAL-PUZZLE-RE-LABELED"]
        reports.append(dict(target=tk, tol=tol, n_hits=len(hits), n_certified=len(cert),
                            n_relabeled=len(relab), hits=hits[:5]))
        all_hits.extend(hits)
        if verbose:
            tight = (f"{hits[0]['rel_error']:.2e} ({hits[0]['formula'][:56]})" if hits else "-")
            print(f"  [sweep d{depth}] {tk:18} hits={len(hits):>4} CERT={len(cert)} "
                  f"RELAB={len(relab)} tightest={tight}", flush=True)

    all_hits.sort(key=lambda h: h["rel_error"])
    tightest = all_hits[0] if all_hits else None
    agg = dict(
        depth=depth,
        forced_germ_keys=forced_now,
        n_free_germs=len(free_now),
        raw_candidates=counts["raw_candidates"],
        distinct_by_value=counts["distinct_by_value"],
        n_skeletons_total=counts["n_skeletons_total"],
        splits=counts["splits"],
        n_targets_swept=len(targets),
        n_hits=sum(r["n_hits"] for r in reports),
        n_certified=sum(r["n_certified"] for r in reports),
        n_relabeled=sum(r["n_relabeled"] for r in reports),
        tightest=tightest,
        build_wall_s=round(build_s, 1),
        per_target=reports,
    )
    return agg


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--depth", type=int, required=True)
    ap.add_argument("--mode", default=None, choices=("published", "kappa"),
                    help="override ATOMOS_FORCED_PAIR (which itself defaults to 'published')")
    ap.add_argument("--include-holdout", action="store_true",
                    help="replay/regression only: sweep the full historical 20-target list")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    mode = args.mode or mode_from_env()
    targets = sm_target_keys(include_holdout=bool(args.include_holdout))
    if not args.include_holdout:
        assert_no_holdout(targets, "the search target list")     # bug-#3 guard

    print("=" * 100)
    print(f"run_forced_pair_depth  depth={args.depth}  mode={mode}  "
          f"targets={len(targets)}  include_holdout={bool(args.include_holdout)}")
    print("=" * 100)
    with forced_pair(mode=mode):
        agg = build_and_sweep(args.depth, targets, verbose=True)

    print("-" * 100)
    print(f"depth {args.depth} / forced {agg['forced_germ_keys']} : "
          f"raw={agg['raw_candidates']:,} distinct={agg['distinct_by_value']:,} "
          f"hits={agg['n_hits']} CERT={agg['n_certified']} RELAB={agg['n_relabeled']}")
    if agg["tightest"]:
        t = agg["tightest"]
        print(f"tightest: {t['target']} rel={t['rel_error']:.6e}  {t['formula']}")
    print("-" * 100)

    RESULTS.mkdir(exist_ok=True)
    out = Path(args.out) if args.out else RESULTS / f"depth{args.depth}_{mode}.json"
    out.write_text(json.dumps(agg, indent=2, default=str))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
