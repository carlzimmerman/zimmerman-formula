#!/usr/bin/env python3
"""EUC13 AMENDMENT A1 (post hoc reading; not the gate): M3 full-form lensing weight with the lens boost fixed at
b = 0 and b = 0.5, with the surviving setting mu = 10 (criteria sec. 2 M3.5 asked for mu marginal, which was dropped
by validation).  Imports euc13.py; changes none of its numbers.

  python3 -I euc13_posthoc.py --data-dir <ECLIPSE dir>
"""
import argparse, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc13 as M
E = M.E

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    OUT = []
    def P(s=""):
        print(s, flush=True); OUT.append(s)
    rows, _ = E.load(a.data_dir); Pm, _ = E.select(rows, ("A",)); N = len(Pm)
    ref = json.load(open(os.path.join(HERE, "euc13_results.json")))
    import csv
    pl = {r["unique_identifier"]: r for r in csv.DictReader(open(os.path.join(HERE, "euc13_per_lens.csv")))}
    marc = np.array([float(pl[r["id"]]["arc_vis_mag"]) if pl[r["id"]]["arc_vis_mag"] else np.nan for r in Pm])
    has = np.isfinite(marc); z0 = E.arr(Pm, "z"); tE0 = E.arr(Pm, "tE")
    ia = np.where(has)[0]; miss = np.where(~has)[0]
    dist = (z0[~has, None] - z0[None, ia]) ** 2 / 0.01 + (np.log10(tE0[~has, None]) - np.log10(tE0[None, ia])) ** 2 / 0.01
    NBR = ia[np.argsort(dist, axis=1)[:, :20]]
    FLD = M.Field(M.load_counts()); NT, _ = M.n_table(FLD, np.where(has, marc, 25.0), "mu10")
    BT0 = M.Btab(Pm, z0, E.arr(Pm, "lm"), tE0, E.arr(Pm, "te"))
    ALL = np.arange(N); RB = {}
    P("EUC13 AMENDMENT A1 (post hoc reading): M3 mu = 10, full weight, lens boost fixed; not the gate")
    for bfix in (0.0, 0.5):
        for nm, a0 in M.FOOT.items():
            w, _ = M.w_full(Pm, z0, np.full(N, 10.0 ** bfix), a0)
            rng = np.random.default_rng(M.SEED); meds = []; zm = []
            for _ in range(50):
                n = NT.copy()
                if len(miss): n[miss] = NT[NBR[np.arange(len(miss)), rng.integers(0, 20, len(miss))]]
                zs = M.draw_rows(n * w, rng); meds.append(float(np.median(BT0.b(ALL, zs, nm)))); zm.append(float(np.median(zs)))
            RB["b%.1f_%s" % (bfix, nm)] = dict(b_med=float(np.median(meds)), z_s_median=float(np.median(zm)))
            P("  boost fixed at b = %.1f  %-9s b_med %+.3f  median z_s %.2f   (frozen self-consistent: %+.3f)"
              % (bfix, nm, np.median(meds), np.median(zm), ref["members"]["M3 mu10 full"][nm]["med"]["point"]))
    json.dump(RB, open(os.path.join(HERE, "euc13_posthoc_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "euc13_posthoc.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
