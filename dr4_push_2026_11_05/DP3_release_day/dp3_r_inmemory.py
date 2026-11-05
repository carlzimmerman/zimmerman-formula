#!/usr/bin/env python3
"""DP3: CFG825's R statistic on a pair table, IN MEMORY, for the DR3 dry run only (NEW file).

Imports campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r.py READ-ONLY and calls its own read_table and score with
its own seed and B, exactly as its --dr3 / --dr4 modes do, but writes ONLY to --out-json / --out (in this lane). It never touches
CFG825's once-only slots (cfg816_r_dr3_results.json exists; cfg816_r_dr4_results.json must stay absent until the owner's yes) and
refuses to run if --out-json points into the CFG816 folder. The release-day R run is `cfg816_r.py --dr4`, once, on the owner's yes.
Run: python3 -B dp3_r_inmemory.py --table pairs.csv --out-json r_dryrun.json
kappa = 1/2 FITTED; not theory closed. DR3 numbers are code-path tests, never results.
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.abspath(os.path.join(HERE, "..", "..", "campaign_fresh_gravity", "CFG816_dr4_r_statistic_scoring"))
sys.path.insert(0, CFG)
import cfg816_r as C  # noqa: E402  (read-only import)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True); ap.add_argument("--out-json", required=True); ap.add_argument("--label", default="DP3 DRY RUN (not the official C4)")
    a = ap.parse_args(argv)
    if os.path.abspath(a.out_json).startswith(CFG):
        raise SystemExit("REFUSING: this helper never writes into the CFG816 folder")
    dr4_slot = os.path.join(CFG, "cfg816_r_dr4_results.json")
    before = os.path.exists(dr4_slot)
    rng = np.random.default_rng(C.SEED)
    t = C.read_table(a.table)
    res, final = C.score(t, rng, C.B_RUN, a.label)
    out = dict(lane="DP3 (in-memory CFG825 score)", seed=C.SEED, B=C.B_RUN, table=os.path.basename(a.table), branches=res, primary_label=final,
               dr4_slot_present_before=before, dr4_slot_present_after=os.path.exists(dr4_slot))
    json.dump(out, open(a.out_json, "w"), indent=1, default=float)
    open(os.path.splitext(a.out_json)[0] + ".out", "w").write("\n".join(C.OUT) + "\n")
    print("\n".join(C.OUT))
    return 0 if not out["dr4_slot_present_after"] else 2


if __name__ == "__main__":
    sys.exit(main())
