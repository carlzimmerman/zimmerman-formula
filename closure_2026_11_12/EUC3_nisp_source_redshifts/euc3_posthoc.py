#!/usr/bin/env python3
"""EUC3 POST HOC diagnostics (POSTHOC_DIAGNOSTICS.md).  After the frozen gates were seen to fail on the first pass.

Checks whether the purity-null failure is real or a product of how the null was built.  Reads the complete run's
per-system table euc3_systems.csv (written by euc3.py; every evaluable system with every spectrum that passes all
cuts except the S/N threshold).  Nothing here can produce a verdict word.

Run:  python3 -I euc3_posthoc.py --data-dir <dir with the two ECLIPSE csv files>
"""
import argparse, csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

AGREE, NULL_FRAC = 0.02, 0.20
OUT = []
def P(s=""):
    print(s); OUT.append(s)
E.P = lambda s="": None

def load():
    rows = []
    with open(os.path.join(HERE, "euc3_systems.csv"), newline="") as f:
        for r in csv.DictReader(f):
            z = [float(x) for x in r["pass_all_but_snr_z"].split(";") if x]
            sn = [float(x) for x in r["pass_all_but_snr_snr"].split(";") if x]
            ro = [x for x in r["pass_all_but_snr_role"].split(";") if x]
            se = [x for x in r["pass_all_but_snr_second"].split(";") if x]
            rows.append(dict(id=r["unique_identifier"], grade=r["grade"], P=r["in_P"] == "True", S=r["in_S"] == "True", zup=float(r["z_up"]),
                             fh=float(r["lens_H_flux_uJy"]), cand=list(zip(z, sn, ro, se))))
    return rows

def hit(r, thr, flt=None):
    """the system-level SECURE class at an S/N threshold: (z, snr, role, second) of the best spectrum, or None"""
    c = [x for x in r["cand"] if x[1] >= thr]
    if not c or max(abs(x[0] - c[0][0]) for x in c) > AGREE: return None
    return c[0] if (flt is None or flt(c[0])) else None

def rate(rows, thr=5.0, flt=None):
    n = sum(hit(r, thr, flt) is not None for r in rows)
    return n, len(rows), n / max(len(rows), 1)

def diff(a, b):
    """rate difference a - b with a 95 % normal interval"""
    pa, pb = a[0] / a[1], b[0] / b[1]
    se = math.sqrt(pa * (1 - pa) / a[1] + pb * (1 - pb) / b[1])
    return pa - pb, pa - pb - 1.96 * se, pa - pb + 1.96 * se

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    R = load(); RES = {}
    S = [r for r in R if r["S"]]; L = [r for r in R if r["grade"] in ("A", "B")]; X = [r for r in R if r["grade"] == "X"]
    Pm = [r for r in R if r["P"]]
    P("EUC3 POST HOC DIAGNOSTICS (after the frozen gates failed; no verdict can come from here)")
    P("evaluable systems: S %d, P %d, all grade A/B %d, grade X %d" % (len(S), len(Pm), len(L), len(X)))

    P("\n[1] rates against the H-alpha S/N threshold (everything else as frozen)")
    RES["thresholds"] = {}
    for thr in (5.0, 8.0, 12.0, 20.0):
        s, l, x = rate(S, thr), rate(L, thr), rate(X, thr)
        lim = max(1.0, NULL_FRAC * s[0] * x[1] / s[1])
        RES["thresholds"]["%g" % thr] = dict(S=s, AB=l, X=x, limit=lim)
        P("  S/N >= %4.0f: S %3d / %d = %.4f;  all A/B %3d / %d = %.4f;  X %2d / %d = %.4f;  H2 limit %.1f -> %s"
          % (thr, s[0], s[1], s[2], l[0], l[1], l[2], x[0], x[1], x[2], lim, "pass" if x[0] <= lim else "fail"))

    P("\n[2] T5 rates by split (S | all A/B | X)")
    fmed = float(np.median([r["fh"] for r in S if np.isfinite(r["fh"])]))
    splits = (("z_up < 0.60", lambda r: r["zup"] < 0.60, None), ("z_up >= 0.60", lambda r: r["zup"] >= 0.60, None),
              ("lens H flux >= S median (%.1f uJy)" % fmed, lambda r: r["fh"] >= fmed, None), ("lens H flux < S median", lambda r: r["fh"] < fmed, None),
              ("hit on the lens object", None, lambda c: c[2] == "lens object"), ("hit on a neighbour", None, lambda c: c[2] == "neighbour"),
              ("hit with a second line", None, lambda c: c[3] != "-"), ("hit with H-alpha only", None, lambda c: c[3] == "-"))
    RES["splits"] = {}
    for nm, sel, flt in splits:
        out = []
        for grp in (S, L, X):
            g = [r for r in grp if sel(r)] if sel else grp
            out.append(rate(g, 5.0, flt))
        RES["splits"][nm] = out
        P("  %-36s S %3d / %4d = %.4f | A/B %3d / %4d = %.4f | X %2d / %4d = %.4f | X/S rate ratio %.2f"
          % (nm, *out[0], *out[1], *out[2], (out[2][2] / out[0][2]) if out[0][2] > 0 else float("nan")))

    P("\n[3] X reweighted to S's joint distribution in (H-flux tercile x z_up tercile)")
    fq = np.nanpercentile([r["fh"] for r in S], [100 / 3, 200 / 3]); zq = np.percentile([r["zup"] for r in S], [100 / 3, 200 / 3])
    cell = lambda r: (int(np.searchsorted(fq, r["fh"])) if np.isfinite(r["fh"]) else 0, int(np.searchsorted(zq, r["zup"])))
    wS, cells = {}, {}
    for r in S: wS[cell(r)] = wS.get(cell(r), 0) + 1
    for r in X: cells.setdefault(cell(r), []).append(r)
    rw = 0.0; cov = 0
    for c, n in sorted(wS.items()):
        xs = cells.get(c, [])
        rx = rate(xs)[2] if xs else float("nan")
        P("    cell (flux tercile %d, z_up tercile %d): S %4d systems, X %3d systems, X rate %s" % (c[0], c[1], n, len(xs), "%.4f" % rx if xs else "none"))
        if xs: rw += n * rx; cov += n
    rmatch = rw / max(cov, 1); s5 = rate(S)
    P("  matched null rate %.4f (raw X rate %.4f; S rate %.4f): expected false among S's %d hits = %.1f;  H2 limit as a rate = %.4f -> %s"
      % (rmatch, rate(X)[2], s5[2], s5[0], rmatch * s5[1], NULL_FRAC * s5[2], "pass" if rmatch <= NULL_FRAC * s5[2] else "fail"))
    RES["matched"] = dict(rate=rmatch, expected_false_S=rmatch * s5[1], fq=list(map(float, fq)), zq=list(map(float, zq)))

    P("\n[4] excess rate over the null, T5")
    x5 = rate(X); RES["excess"] = {}
    for nm, grp in (("S", S), ("all A/B", L), ("P", Pm)):
        g = rate(grp); d = diff(g, x5)
        RES["excess"][nm] = dict(rate=g, diff=d)
        P("  %-8s rate %.4f - X %.4f = %+.4f [%+.4f, %+.4f];  real sources this allows among its %d hits: %.1f [%.1f, %.1f]"
          % (nm, g[2], x5[2], d[0], d[1], d[2], g[0], max(d[0], 0) * g[1], max(d[1], 0) * g[1], max(d[2], 0) * g[1]))

    P("\n[5] margin z_s - z_up of the T5 hits")
    for nm, grp in (("S", S), ("all A/B", L), ("X", X)):
        m = np.array([hit(r, 5.0)[0] - r["zup"] for r in grp if hit(r, 5.0) is not None])
        if len(m): P("  %-8s N = %3d: median %.2f, fraction below 0.40: %.2f, fraction above 0.80: %.2f" % (nm, len(m), np.median(m), np.mean(m < 0.4), np.mean(m > 0.8)))

    P("\n[6] EUCL-DR1-L015763 at its rank-1 redshift (one lens; not a rule)")
    rows, _ = E.load(a.data_dir); key = {r["id"]: r for r in rows}
    obj = {r["Unique_Identifier"]: r for r in csv.DictReader(open(os.path.join(a.data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8"))}
    ar = key["EUCL-DR1-L015763"]; zsp = float(obj["EUCL-DR1-L015763"]["desi_deflector_specz"])
    lma = ar["lm"] + 2.0 * math.log10(float(E.EUCLID.DL(zsp)) / float(E.EUCLID.DL(ar["z"])))
    eng, z, RE, _, _, _ = E.build([ar], z=np.array([zsp]), lm=np.array([lma]))
    RES["L015763"] = {}
    for zs in (1.3657, 1.3768):
        b = {nm: float(E.run_b(eng, z, RE, zs, a0, "S")[0]) for nm, a0 in E.FOOT.items()}
        RES["L015763"]["%.4f" % zs] = b
        P("  z_s = %.4f (%s): b = %+.3f / %+.3f" % (zs, "DESI [O II]" if zs < 1.37 else "grism rank 1", b["canonical"], b["alt"]))

    P("\nkappa = 1/2 FITTED. Post hoc: none of this is a verdict.")
    json.dump(RES, open(os.path.join(HERE, "euc3_posthoc_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "euc3_posthoc.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
