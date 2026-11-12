#!/usr/bin/env python3
"""EUC1 POST HOC readings (written after the frozen run was seen; none of this is the verdict).

A1  the source redshift below which the ceiling would break: f25 on sample P, law S, with every
    source placed at one redshift z_s, on a grid; and the z_s at which the lower 95% bound of f25
    reaches 0.25.
A2  first-order noise correction of f25 at z_s = infinity: observed f25 minus the rise produced by
    adding the catalogued errors a second time (the frozen Monte Carlo of robustness run 6).
A3  disc deflectors against the other lenses, matched in (log M*, z_l) by nearest neighbour without
    replacement: difference in b (source at infinity), with a bootstrap interval.  Only meaningful if
    the two classes share a source-redshift distribution.

Run:  python3 -I euc1_posthoc.py --data-dir <dir with the two ECLIPSE csv files>
"""
import argparse, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc1 as E

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    out = []
    def P(s=""):
        print(s); out.append(s)
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Pm, _ = E.select(rows, ("A",))
    eng, z, RE, Re, n, lm = E.build(Pm)
    ref = json.load(open(os.path.join(HERE, "euc1_results.json")))
    RES = {}
    P("EUC1 POST HOC (after the frozen run; not the verdict).  Sample P, N = %d, law S." % len(Pm))

    # ---------------- A1
    P("\n[A1] every source at one redshift z_s: f25 [95%] and median b")
    grid = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 20.0, 1100.0]
    A1 = {}
    for nm, a0 in E.FOOT.items():
        rng = np.random.default_rng(E.SEED); rowsA = []
        for zs in grid:
            keep = z < zs - 0.2
            b = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, np.where(keep, zs, z + 5.0)), a0, "S")[keep]
            st = E.stats(b, rng); rowsA.append(dict(zs=zs, **st))
            P("  %-9s z_s = %7.1f  N=%4d  f25 = %.3f [%.3f, %.3f]  b_med = %+.3f" % (nm, zs, st["N"], st["f25"], st["f25_lo"], st["f25_hi"], st["b_med"]))
        # crossing of the lower bound through 0.25, linear in 1/z_s between grid points
        x = np.array([1.0 / r["zs"] for r in rowsA]); y = np.array([r["f25_lo"] for r in rowsA])
        o = np.argsort(x); zstar = float("nan")
        for i in range(len(o) - 1):
            x0, x1, y0, y1 = x[o[i]], x[o[i + 1]], y[o[i]], y[o[i + 1]]
            if (y0 - 0.25) * (y1 - 0.25) <= 0 and y1 != y0:
                zstar = 1.0 / (x0 + (0.25 - y0) * (x1 - x0) / (y1 - y0)); break
        A1[nm] = dict(rows=rowsA, zs_star=zstar)
        P("  %-9s the lower bound of f25 reaches 0.25 at a common source redshift z_s* = %.2f" % (nm, zstar))
    RES["A1"] = A1

    # ---------------- A2
    P("\n[A2] first-order noise correction at z_s = infinity (observed f25 minus the Monte Carlo rise)")
    A2 = {}
    for nm in E.FOOT:
        obs = ref["primary"]["S_" + nm]["f25"]; mc = ref["robustness"]["6_MC_" + nm]["mean"]
        A2[nm] = dict(observed=obs, mc_mean=mc, corrected=obs - (mc - obs))
        P("  %-9s observed %.3f, errors added once more %.3f, first-order corrected %.3f" % (nm, obs, mc, obs - (mc - obs)))
    RES["A2"] = A2

    # ---------------- A3
    P("\n[A3] disc deflectors vs the other lenses, matched in (log M*, z_l)")
    disc = np.array([r["disc"] for r in Pm]); A3 = {}
    di = np.where(disc)[0]; oi = np.where(~disc)[0]
    X = np.column_stack([lm / 0.2, z / 0.1])
    used = np.zeros(len(Pm), bool); pairs = []
    for i in di:
        d2 = np.sum((X[oi] - X[i]) ** 2, axis=1); d2[used[oi]] = np.inf
        j = oi[int(np.argmin(d2))]
        if np.isfinite(d2.min()) and d2.min() < 1.0:
            used[j] = True; pairs.append((i, j))
    pairs = np.array(pairs)
    P("  discs %d, matched pairs %d (within 0.2 dex and 0.1 in z, combined)" % (len(di), len(pairs)))
    for nm, a0 in E.FOOT.items():
        b = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, "S")
        d = b[pairs[:, 1]] - b[pairs[:, 0]]
        rng = np.random.default_rng(E.SEED)
        bs = np.array([np.median(d[rng.integers(0, len(d), len(d))]) for _ in range(2000)])
        A3[nm] = dict(N=int(len(d)), median_other_minus_disc=float(np.median(d)), lo=float(np.percentile(bs, 2.5)),
                      hi=float(np.percentile(bs, 97.5)), disc_b_med=float(np.median(b[pairs[:, 0]])),
                      other_b_med=float(np.median(b[pairs[:, 1]])),
                      dlm=float(np.median(lm[pairs[:, 1]] - lm[pairs[:, 0]])), dz=float(np.median(z[pairs[:, 1]] - z[pairs[:, 0]])))
        P("  %-9s median b: discs %+.3f, matched others %+.3f; paired difference (other - disc) = %+.3f [%+.3f, %+.3f] dex"
          % (nm, A3[nm]["disc_b_med"], A3[nm]["other_b_med"], A3[nm]["median_other_minus_disc"], A3[nm]["lo"], A3[nm]["hi"]))
    P("  match quality: median d(log M*) = %+.3f, d(z_l) = %+.3f" % (A3["alt"]["dlm"], A3["alt"]["dz"]))
    P("  the catalogue applies one Salpeter IMF to both classes; a Chabrier disc would raise the disc b by 0.2-0.25 dex / 0.77")
    RES["A3"] = A3
    json.dump(RES, open(os.path.join(HERE, "euc1_posthoc_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "euc1_posthoc.out"), "w").write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
