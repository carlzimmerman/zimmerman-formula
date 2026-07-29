#!/usr/bin/env python3
"""value_set_delta.py -- is the {3, kappa} search reaching values the published {3, sqrt(8pi/3)}
                         search could NOT reach? Computed on the FULL depth-D value sets.

audit_interlock/kappa_forced_equivalence.py answered a proxy question (germ-FACTOR values only,
3 decorate steps, on engine.alphabet._geometry_germs which is NOT the pool exhaust.py searches).
This script answers it on the real thing: the actual Gate-B-passable DIMENSIONLESS value sets that
exhaust_depthN_forced.constructive_gate_b_reachables produces at depth D under each forced pair.

Comparison is at the pipeline's OWN dedup precision -- exhaust._value_key = mp.nstr(v, 30) --
never float64 (bug-guard #4).

Exit 0 = the comparison ran. There is no hard-coded verdict; the numbers are printed either way.
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import exhaust as EX                                    # noqa: E402
from exhaust import build_alphabet                        # noqa: E402
import exhaust_depth5_forced as D5                      # noqa: E402
import exhaust_depthN_forced as DN                       # noqa: E402
from kappa_forced import forced_pair                     # noqa: E402


def value_set(depth: int, mode: str):
    with forced_pair(mode=mode):
        alpha = build_alphabet(None, None)
        forced = D5._forced_keys_present(alpha)
        t0 = time.time()
        reach, counts = DN.constructive_gate_b_reachables(alpha, depth, value_cap=None)
        wall = time.time() - t0
        keys = {EX._value_key(r.value) for r in reach}
    print(f"  {mode:<10} forced={forced}  raw={counts['raw_candidates']:,} "
          f"distinct={counts['distinct_by_value']:,}  keys={len(keys):,}  ({wall:.1f}s)")
    if len(keys) != counts["distinct_by_value"]:
        raise SystemExit(f"KEY-COLLISION GUARD: {len(keys):,} 30-dps keys != "
                         f"{counts['distinct_by_value']:,} distinct values -- re-keying LOST values "
                         f"(this is bug #2/#4; do not trust any downstream number)")
    return keys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=6)
    args = ap.parse_args()
    d = args.depth

    print("=" * 100)
    print(f"value_set_delta -- depth {d}: {{3, sqrt(8pi/3)}} vs {{3, kappa}} reachable VALUE sets")
    print("=" * 100)
    A = value_set(d, "published")
    B = value_set(d, "kappa")

    onlyA = A - B
    onlyB = B - A
    both = A & B
    print("-" * 100)
    print(f"  |A| published      : {len(A):,}")
    print(f"  |B| kappa          : {len(B):,}")
    print(f"  shared             : {len(both):,}  ({100*len(both)/len(A|B):.2f}% of the union)")
    print(f"  ONLY under A       : {len(onlyA):,}")
    print(f"  ONLY under B       : {len(onlyB):,}")
    print("-" * 100)
    if onlyB:
        print(f"  The {{3, kappa}} search REACHES {len(onlyB):,} values the published search could not.")
        print("  Sample (mpmath 30-dps keys):")
        for v in sorted(onlyB)[:6]:
            print("   ", v)
    else:
        print("  The {3, kappa} search reaches NOTHING new: B is a subset of A. Under the value-dedup")
        print("  invariant the published null already covered every value kappa-forcing can build,")
        print("  so a full re-run cannot change the certified count -- only which expressions are")
        print("  LABELLED Gate-B-passing.")
    if onlyA:
        print(f"\n  Conversely the published search reaches {len(onlyA):,} values kappa-forcing loses")
        print("  (sqrt(8pi/3) is demoted to a FREE germ, so it can appear only once per expression,")
        print("   whereas as a FORCED germ it was guaranteed >=1 step and could take >1).")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
