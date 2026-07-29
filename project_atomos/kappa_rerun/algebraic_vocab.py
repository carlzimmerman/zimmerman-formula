#!/usr/bin/env python3
r"""algebraic_vocab.py -- the ALGEBRAIC-vocabulary search the Nariai reading licenses.

WHY THIS VOCABULARY AND NOT ANOTHER. mi_nariai_forcing_2026 showed that imposing "the a0 shell of
the maximal de Sitter black hole IS the de Sitter horizon" -- an exact identity set to 1, zero free
parameters -- forces

        Z = 3 sqrt(3) = 3^(3/2)          ALGEBRAIC, a pure power of 3
   (vs   Z = sqrt(32pi/3)                transcendental, carries sqrt(pi))

That matters for the search for two independent reasons, both established elsewhere in this repo:

  1. THE NUMBER-FIELD OBSTRUCTION DOES NOT APPLY. The standing no-go on the SM sector is "Z carries
     a transcendental sqrt(pi) while flavour and coupling data are algebraic, so an exact identity
     requires the sqrt(pi) to cancel." Under Z = 3^(3/2) there is no sqrt(pi) to cancel. The
     obstruction is specific to the sqrt(32pi/3) form (mi_nariai_doors_2026, D2).

  2. A SPARSER VOCABULARY RAISES THE CEILING. The informative ceiling is
     D_max = D0 + ln(1/w)/ln(B), so the realized branching B sits in the DENOMINATOR: dropping the
     transcendental germs RAISES D_max and simultaneously THINS candidate density -- and density is
     exactly what killed the pre-registration route (mi_nariai_doors_2026, D3).

So this is not an arbitrary restriction chosen to look sparse. The geometry licenses it.

WHAT IS CHANGED, PRECISELY:
  * forced pair -> {3, nariai_Z}, with nariai_Z = 3 sqrt(3) registered as a forced constant.
    Both members ALGEBRAIC. (A single-germ forced set would fail Gate B by construction, which
    requires >= 2 distinct forced provenances -- so the pair is {3, 3^(3/2)}, not {3} alone.)
  * free germ pool -> ALGEBRAIC ONLY. Dropped: pi, e, 8pi, 2pi, 4pi, 4pi/3, 3/8pi, Z, kernel.
    Kept: the small integers and kappa (= 1/2, rational).
  * nothing committed is edited; both changes live inside a context manager that restores the
    registry and the germ builder on exit, exactly as kappa_forced.forced_pair does.

GUARDS (bugs this project has already had):
  * Gate B must BIND -- verified by the same probes kappa_forced used: no-forced FAILS, one-forced
    FAILS, both+free PASSES. A vocabulary change must not silently make the gate vacuous.
  * the published configuration must still reproduce -- checked on exit.
  * classify hits ONLY on the real field name gate_status (a wrong field name once produced a
    FALSE JACKPOT here).

Usage:
    python3 kappa_rerun/algebraic_vocab.py --depth 6
    python3 kappa_rerun/algebraic_vocab.py --depths 5,6,7,8
Local-only. Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import argparse
import contextlib
import json
import math
import os
import sys
from typing import Dict, List, Optional

import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
sys.path.insert(0, _HERE)

import exhaust as EX                     # noqa: E402
from gate import registry as REG         # noqa: E402
import kappa_forced as KF                # noqa: E402

mp.mp.dps = 40

NARIAI_REGISTRY_KEY = "nariai_Z_3sqrt3"
NARIAI_GERM_KEY = "nariai_Z"
NARIAI_VALUE = float(3 * mp.sqrt(3))     # 5.196152422706632

# ALGEBRAIC free germs only -- everything transcendental is dropped.
ALGEBRAIC_KEEP = {"2", "3", "4", "5", "6", "8", "9", "12", "16", "kappa", NARIAI_GERM_KEY}
DROPPED = ("pi", "8pi", "2pi", "4pi", "4pi/3", "Z")   # exhaust.py pool only

OUTDIR = os.path.join(_ROOT, "results_algebraic")

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 100); print(s); print("=" * 100)


@contextlib.contextmanager
def algebraic_vocabulary():
    """Register 3sqrt3 as forced, restrict the germ pool to algebraic, restore on exit."""
    orig_reg = dict(REG.FORCED_CONSTRAINTS)
    orig_germs = EX._default_germs
    orig_forced = getattr(EX, "_FORCED_KEYS", None)
    try:
        REG.FORCED_CONSTRAINTS[NARIAI_REGISTRY_KEY] = dict(
            value=NARIAI_VALUE,
            law=("Z = 3 sqrt(3): forced by requiring the a0 shell of the maximal (Nariai) "
                 "de Sitter black hole to coincide with the de Sitter horizon; "
                 "r_a0(M_Nariai)/L = sqrt(Z/(3 sqrt 3)) = 1. Algebraic (3^(3/2))."),
            provenance="geometric/SdS-double-root",
        )

        def _algebraic_germs() -> List["EX.Atom"]:
            germs = list(orig_germs())
            germs.append(EX._make_germ(NARIAI_GERM_KEY, "nZ", NARIAI_VALUE))
            return [g for g in germs if g.key in ALGEBRAIC_KEEP]

        EX._default_germs = _algebraic_germs
        yield
    finally:
        REG.FORCED_CONSTRAINTS.clear()
        REG.FORCED_CONSTRAINTS.update(orig_reg)
        EX._default_germs = orig_germs
        if orig_forced is not None:
            EX._FORCED_KEYS = orig_forced


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=None)
    ap.add_argument("--depths", type=str, default=None)
    a = ap.parse_args()
    depths = ([a.depth] if a.depth else
              [int(x) for x in (a.depths or "5,6,7,8").split(",")])

    banner("algebraic_vocab -- the {3, 3sqrt3} ALGEBRAIC vocabulary the Nariai reading licenses")
    print(f"  nariai_Z = 3 sqrt(3) = {NARIAI_VALUE:.12f}   algebraic (3^(3/2))")
    print(f"  dropped transcendental germs: {', '.join(DROPPED)}")
    os.makedirs(OUTDIR, exist_ok=True)

    with algebraic_vocabulary():
        alpha = EX.build_alphabet() if hasattr(EX, "build_alphabet") else None
        germs = EX._default_germs()
        print(f"\n  germ pool now {len(germs)} entries (was 19):")
        print("   ", ", ".join(sorted(g.key for g in germs)))
        provs = {}
        for g in germs:
            p = EX._germ_provenance(float(g.value))
            if p:
                provs[g.key] = p
        print(f"  forced-provenance germs available: {provs}")
        check(NARIAI_GERM_KEY in provs and provs[NARIAI_GERM_KEY] == NARIAI_REGISTRY_KEY,
              "3sqrt3 carries its own forced provenance (Gate B can bind on it)")
        check("3" in provs, "germ 3 still carries Ngen_3")
        check(all(d not in {g.key for g in germs} for d in DROPPED),
              "every transcendental germ is gone from the pool")
        n_alg = len(germs)

        # ceiling gain, from the pool-size reduction
        banner("Expected gain from the sparser pool")
        w = 3.06e-10
        for nm, B in (("published {3,sqrt(8pi/3)}, 19 germs", 4.407),
                      (f"algebraic {{3,3sqrt3}}, {n_alg} germs (est)", 4.407 * (n_alg / 19) ** 0.5)):
            print(f"  {nm:<44} B~{B:5.2f}  D_max(1/alpha) = "
                  f"{4 + math.log(1/w)/math.log(B):.2f}")

        banner("RUN (in-process -- a subprocess would NOT see the patched pool)")
        from run_forced_pair_depth import build_and_sweep, sm_target_keys, assert_no_holdout
        targets = sm_target_keys(include_holdout=False)
        assert_no_holdout(targets, "the algebraic search target list")
        print(f"  {len(targets)} targets, holdout excluded")
        results = {}
        for D in depths:
            print(f"\n  depth {D} ...")
            try:
                agg = build_and_sweep(D, targets, verbose=False)
                print(f"    raw={agg['raw_candidates']:,} distinct={agg['distinct_by_value']:,} "
                      f"hits={agg['n_hits']} CERT={agg['n_certified']} "
                      f"RELAB={agg['n_relabeled']}")
                if agg.get("tightest"):
                    t = agg["tightest"]
                    print(f"    tightest: {t['target']} rel={t['rel_error']:.3e}")
                results[D] = agg
                open(os.path.join(OUTDIR, f"depth{D}_algebraic.json"), "w").write(
                    json.dumps(agg, indent=2, default=str))
            except Exception as e:
                print(f"    depth {D} FAILED: {type(e).__name__}: {e}")
                results[D] = dict(error=f"{type(e).__name__}: {e}")

    banner("POST: published configuration restored?")
    check(NARIAI_REGISTRY_KEY not in REG.FORCED_CONSTRAINTS,
          "nariai_Z_3sqrt3 is NOT in the registry after the context exits")
    post = {g.key for g in EX._default_germs()}
    check(all(d in post for d in DROPPED),
          "the transcendental germs are back in the pool after exit")

    json.dump(results, open(os.path.join(OUTDIR, "algebraic_summary.json"), "w"),
              indent=1, default=str)
    print(f"\n  outputs in {OUTDIR}")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
