#!/usr/bin/env python3
"""regression_published.py -- with the switch OFF, the new code path must reproduce the COMMITTED
                              depth-6 null EXACTLY. Then, with the switch ON, it must produce a
                              DIFFERENT search (or the re-run is pointless).

This is bug-guard #2 made executable: "require any new path to reproduce committed counts EXACTLY
before trusting it on new work." The committed ground truth is read from grind.REPLAY_COMMITTED[6],
not retyped here.

Also enforced:
  #1 field-name guard   -- every filter is applied to a field asserted to exist ('gate_status' on
                           hit dicts, 'status'/'kernel' on the gate verdict). 'fdr_dead'/'verdict'
                           are asserted ABSENT so nobody re-adds the false-jackpot filter.
  #3 holdout guard      -- HOLDOUT_KEYS must be absent from the SEARCH list; the regression sweep
                           deliberately uses include_holdout=True because reproducing the committed
                           259 requires the full historical 20-target list (that is a replay, not
                           a search).
  #4 precision guard    -- value comparisons use mpmath 30-dps value keys, not float64 re-keying.

Exit 0 = regression reproduced + the kappa mode differs.
"""
from __future__ import annotations

import os
import sys
from typing import Dict

import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import exhaust as EX                                        # noqa: E402
from exhaust import build_alphabet                            # noqa: E402
import exhaust_depth5_forced as D5                          # noqa: E402
from exhaust_parallel import sm_target_keys                  # noqa: E402
from targets.pdg_constants import HOLDOUT_KEYS               # noqa: E402

from kappa_forced import (                                   # noqa: E402
    forced_pair, assert_no_holdout, pool_value_multiset,
    PUBLISHED_FORCED_GERM_KEYS, KAPPA_FORCED_GERM_KEYS,
)
from run_forced_pair_depth import build_and_sweep            # noqa: E402

# committed ground truth, READ from the committed file (never retyped)
_cap_before = (D5.HARD_MEM_CAP_GB, D5._MEM_CAP_MB)
import grind as GRIND                                        # noqa: E402
# grind.py raises D5's watchdog cap to 40 GB at import; put the depth-6-era 6 GB cap back so this
# regression runs under the SAME watchdog the committed number was produced under.
D5.HARD_MEM_CAP_GB, D5._MEM_CAP_MB = _cap_before

COMMITTED = GRIND.REPLAY_COMMITTED

_ok = True


def _check(cond: bool, msg: str) -> bool:
    global _ok
    if not cond:
        _ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return bool(cond)


def _banner(s: str):
    print("\n" + "=" * 104)
    print(s)
    print("=" * 104)


def _cmp(name: str, got, want):
    return _check(got == want, f"{name:<30} computed={got!s:<34.34} committed={want!s:<34.34}")


def main() -> int:
    depth = 6
    com = COMMITTED[depth]

    _banner("regression_published -- switch OFF must reproduce the committed depth-6 null EXACTLY")
    print(f"  committed source : grind.REPLAY_COMMITTED[{depth}] (read, not retyped)")
    print(f"  watchdog cap     : {D5.HARD_MEM_CAP_GB:.0f} GB (the depth-6-era cap, restored after "
          f"grind's 40 GB import-time override)")

    # ---- guards ---------------------------------------------------------------------------
    _banner("guards")
    srch = sm_target_keys()
    assert_no_holdout(srch, "sm_target_keys() (the SEARCH list)")
    _check(True, f"bug#3 holdout guard: search list has {len(srch)} targets, "
                 f"HOLDOUT_KEYS={sorted(HOLDOUT_KEYS)}, leak=NONE")
    replay_targets = sm_target_keys(include_holdout=True)
    _check(sorted(set(replay_targets) & set(HOLDOUT_KEYS)) == sorted(HOLDOUT_KEYS - {"r_tau_mu"}),
           f"replay list ({len(replay_targets)} targets) DOES include the holdout "
           f"{sorted(set(replay_targets) & set(HOLDOUT_KEYS))} -- required to reproduce 259")
    _check(not hasattr(GRIND.DN.HitN, "fdr_dead") and "fdr_dead" not in GRIND.DN.HitN.__annotations__,
           "bug#1: field 'fdr_dead' does NOT exist on the hit record (the false-jackpot filter)")
    _check("verdict" not in GRIND.DN.HitN.__annotations__,
           "bug#1: field 'verdict' does NOT exist on the hit record either")
    _check("status" in GRIND.DN.HitN.__annotations__,
           f"bug#1: the REAL gate field on DN.HitN is 'status'; our dict record uses 'gate_status'")

    # ---- the regression -------------------------------------------------------------------
    _banner(f"A. switch OFF (published pair) at depth {depth}")
    with forced_pair(mode="published"):
        alpha = build_alphabet(None, None)
        pool_pub = pool_value_multiset(alpha)
        _check(len(alpha.germs) == 25 and len(alpha.leaves) == 11,
               f"alphabet {len(alpha.leaves)} leaves / {len(alpha.germs)} germs (committed shape)")
        _check(D5._forced_keys_present(alpha) == list(PUBLISHED_FORCED_GERM_KEYS),
               f"forced germ keys = {D5._forced_keys_present(alpha)}")
        pub = build_and_sweep(depth, replay_targets, verbose=True)

    print()
    _cmp("raw candidates", pub["raw_candidates"], com["raw"])
    _cmp("distinct values", pub["distinct_by_value"], com["distinct"])
    _cmp("in-window hits", pub["n_hits"], com["hits"])
    _cmp("CERTIFIED", pub["n_certified"], com["n_certified"])
    _cmp("RE-LABELED", pub["n_relabeled"], com["n_relabeled"])
    t = pub["tightest"]
    _cmp("tightest target", t["target"], com["tightest_target"])
    _check(abs(t["rel_error"] - com["tightest_rel"]) <= 1e-12 * com["tightest_rel"],
           f"{'tightest rel_err':<30} computed={t['rel_error']:.15e} committed={com['tightest_rel']:.15e}")
    _cmp("tightest formula", t["formula"], com["tightest_formula"])

    # ---- the switch ON: must be a DIFFERENT search --------------------------------------
    _banner(f"B. switch ON ({{3, kappa}}) at depth {depth} -- must DIFFER, or the re-run is pointless")
    with forced_pair(mode="kappa"):
        alpha_k = build_alphabet(None, None)
        _check(pool_value_multiset(alpha_k) == pool_pub,
               "germ pool VALUE multiset identical (mpmath 30-dps keys, not float64 -- bug#4)")
        _check(D5._forced_keys_present(alpha_k) == list(KAPPA_FORCED_GERM_KEYS),
               f"forced germ keys = {D5._forced_keys_present(alpha_k)}")
        kap = build_and_sweep(depth, replay_targets, verbose=True)

    print()
    print(f"  {'':<26}{'published':>16}{'kappa':>16}")
    for k in ("raw_candidates", "distinct_by_value", "n_skeletons_total", "n_hits",
              "n_certified", "n_relabeled"):
        print(f"  {k:<26}{pub[k]:>16,}{kap[k]:>16,}")
    tk = kap["tightest"]
    print(f"  tightest (published) : {t['target']} rel={t['rel_error']:.3e}  {t['formula']}")
    print(f"  tightest (kappa)     : "
          + (f"{tk['target']} rel={tk['rel_error']:.3e}  {tk['formula']}" if tk else "none"))

    _check(kap["raw_candidates"] == pub["raw_candidates"],
           f"raw count IDENTICAL ({kap['raw_candidates']:,}) -- same n_free=23 and same budget "
           f"splits, so the SHAPE of the space is unchanged; only WHICH germ is forced moved")
    _check(kap["distinct_by_value"] != pub["distinct_by_value"],
           f"distinct VALUE set DIFFERS: {kap['distinct_by_value']:,} vs {pub['distinct_by_value']:,} "
           f"(delta {kap['distinct_by_value'] - pub['distinct_by_value']:+,}) -- a genuinely "
           f"different search, not a relabel")
    _check(kap["n_hits"] != pub["n_hits"] or kap["distinct_by_value"] != pub["distinct_by_value"],
           f"in-window hits: kappa={kap['n_hits']} vs published={pub['n_hits']}")

    # ---- restoration -------------------------------------------------------------------
    _banner("C. restoration after both contexts")
    alpha2 = build_alphabet(None, None)
    _check(D5._forced_keys_present(alpha2) == list(PUBLISHED_FORCED_GERM_KEYS),
           f"_forced_keys_present back to {D5._forced_keys_present(alpha2)}")
    _check(pool_value_multiset(alpha2) == pool_pub, "germ pool restored")
    _check("kappa_half" not in GRIND.REG.FORCED_CONSTRAINTS if hasattr(GRIND, "REG")
           else "kappa_half" not in __import__("gate.registry", fromlist=["x"]).FORCED_CONSTRAINTS,
           "'kappa_half' is NOT in the registry outside the context (published config intact)")

    _banner("VERDICT")
    print("  " + ("REGRESSION PASSES and the kappa switch is a real change"
                  if _ok else "** SOMETHING FAILED -- read the FAIL lines **"))
    print("=" * 104)
    return 0 if _ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
