#!/usr/bin/env python3
"""EXR1 AMENDMENT A1 (POST HOC; see AMENDMENT_A1.md).  Reads the frozen run's per-lens arrays (exr1_arrays.npz) and checks.

Reading A1 (ESZ1's construction): each tested lens's value = its net aperture flux minus the mean of its valid shifted
positions (at least 6 of 8); null k = shifted position k minus the mean of that lens's other valid shifted positions;
sigma = max(bootstrap, rms of the 8 null stacks); K8 as frozen on these nulls; frozen thresholds and brackets.
Reading R (conservative): the frozen, unsubtracted stack; sigma = max(bootstrap, rms of the 8 null stacks about their
mean); K8 scatter half only.
Run:  python3 -I exr1_a1.py          EXR1_A1_MUTATE=inject python3 -I exr1_a1.py   (must exit 1)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = (os.environ.get("EXR1_A1_MUTATE", "") or "").strip()
SEED, NBOOT, FCLIP, MINOFF = 20261112, 2000, 1.0e-12, 6
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
clip = lambda v: np.minimum(np.asarray(v, float), FCLIP)
def boot(v):
    v = np.asarray(v, float); N = len(v); rng = np.random.default_rng(SEED); return v[rng.integers(0, N, (NBOOT, N))].mean(1)
def word(meas, sig, pmin):
    if not (np.isfinite(meas) and np.isfinite(sig) and np.isfinite(pmin)) or pmin < 3.0 * sig: return "NO POWER"
    return "EXCLUDED" if meas + 2.0 * sig < pmin else "ALLOWED"

def main():
    A = np.load(os.path.join(HERE, "exr1_arrays.npz")); R0 = json.load(open(os.path.join(HERE, "exr1_results.json")))
    tag = "exr1_a1" + ("_MUTATE_" + MUT if MUT else "")
    P("EXR1 AMENDMENT A1 (POST HOC)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    f, nul, z, gA = A["f"].astype(float), A["nulls"].astype(float), A["z"].astype(float), A["gradeA"].astype(bool)
    pred = {k.split("|", 1)[1]: A[k].astype(float) for k in A.files if k.startswith("pred|")}
    if MUT == "inject": f = f + pred["canonical|primary"]; P("[MUTATE inject] the primary canonical prediction added to every tested lens's measured value")
    frozen_ok = {k: v["ok"] for k, v in R0["checks"].items()}
    P("frozen checks: " + ", ".join("%s %s" % (k, "pass" if v else "FAIL") for k, v in sorted(frozen_ok.items())))
    other_ok = all(v for k, v in frozen_ok.items() if k != "K8")
    nv = np.isfinite(nul).sum(1); keep = nv >= MINOFF
    cn = clip(nul); off = np.nanmean(cn, axis=1)
    P("lenses with >= %d valid shifted positions: %d of %d" % (MINOFF, keep.sum(), len(f)))
    # A1 values and nulls
    va = clip(f) - off
    na = np.full_like(cn, np.nan)
    for k in range(8):
        others = (np.nansum(cn, 1) - np.where(np.isfinite(cn[:, k]), cn[:, k], 0.0)) / np.maximum(nv - np.isfinite(cn[:, k]), 1)
        na[:, k] = np.where(np.isfinite(cn[:, k]), cn[:, k] - others, np.nan)
    def st_a1(sel):
        v = va[sel]; bs = boot(v); ns = np.array([np.nanmean(na[sel, k]) for k in range(8)])
        return dict(N=int(len(v)), mean=float(v.mean()), sigma=max(float(bs.std()), float(np.sqrt(np.mean(ns ** 2)))), sb=float(bs.std()), sn=float(np.sqrt(np.mean(ns ** 2))), nulls=ns)
    def st_r(sel):
        v = clip(f[sel]); bs = boot(v); ns = np.array([np.nanmean(cn[sel, k]) for k in range(8)]); sn = float(np.sqrt(np.mean((ns - ns.mean()) ** 2)))
        return dict(N=int(len(v)), mean=float(v.mean()), sigma=max(float(bs.std()), sn), sb=float(bs.std()), sn=sn, nulls=ns)
    allA = np.where(keep)[0]; allR = np.arange(len(f))
    sA, sR = st_a1(allA), st_r(allR)
    k8a = abs(sA["nulls"].mean()) <= 0.75 * sA["sigma"] and np.abs(sA["nulls"]).max() <= 3.5 * sA["sigma"]
    k8r = np.abs(sR["nulls"] - sR["nulls"].mean()).max() <= 3.5 * sR["sigma"]
    P("\n[A1: lens minus its shifted positions; units 1e-15 erg/s/cm^2]  N = %d, %+.3f, sigma %.3f (bootstrap %.3f, nulls %.3f); null stacks %s"
      % (sA["N"], 1e15 * sA["mean"], 1e15 * sA["sigma"], 1e15 * sA["sb"], 1e15 * sA["sn"], " ".join("%+.2f" % (1e15 * x) for x in sA["nulls"])))
    P("  K8 (A1 nulls): mean %+.3f within 3 sigma/4, largest %.3f within 3.5 sigma -> %s" % (1e15 * sA["nulls"].mean(), 1e15 * np.abs(sA["nulls"]).max(), "PASS" if k8a else "FAIL"))
    P("[R: frozen unsubtracted stack]  N = %d, %+.3f, sigma %.3f (bootstrap %.3f, null scatter about its mean %.3f); null mean %+.3f; K8 scatter half -> %s"
      % (sR["N"], 1e15 * sR["mean"], 1e15 * sR["sigma"], 1e15 * sR["sb"], 1e15 * sR["sn"], 1e15 * sR["nulls"].mean(), "PASS" if k8r else "FAIL"))
    SETS = ["primary", "Z = 0 (H and He only)", "Z = 0.3", "N_H = 1 x N_HI", "point source", "r_in = R_E over 2", "r_in = 1 kpc",
            "Z = 1.0 (reported)", "central source (reported)", "b* = 0 (reported)"]
    TAGS = ("Z = 0 (H and He only)", "Z = 0.3", "N_H = 1 x N_HI", "point source", "r_in = R_E over 2", "r_in = 1 kpc", "grade A only", "z_l <= 0.6 only")
    RES = dict(lane="EXR1", amendment="A1 (post hoc)", mutate=MUT, readings={})
    for lab, stf, base, okk in (("A1", st_a1, allA, k8a and other_ok), ("R", st_r, allR, k8r and other_ok)):
        rows, W = {}, {}
        groups = [(s, base) for s in SETS] + [("grade A only", base[gA[base]]), ("z_l <= 0.6 only", base[z[base] <= 0.6])]
        P("\n[reading %s: words; pred_min / measured +- sigma in 1e-15; (pred - meas)/sigma; pred/(meas + 2 sigma)]" % lab)
        for sname, sel in groups:
            s = stf(sel); pkey = sname if sname in SETS else "primary"
            for nm in ("canonical", "alt"):
                pmin = float(clip(pred["%s|%s" % (nm, pkey)][sel]).mean()); w = word(s["mean"], s["sigma"], pmin) if okk and s["N"] >= 100 else "NOT EVALUABLE"
                rows["%s|%s" % (sname, nm)] = dict(N=s["N"], meas=s["mean"], sigma=s["sigma"], pred_min=pmin, word=w, z=(pmin - s["mean"]) / s["sigma"], ratio=pmin / (s["mean"] + 2 * s["sigma"]),
                                                   f_M=math.sqrt(max(s["mean"] + 2 * s["sigma"], 0.0) / pmin) if pmin > 0 else float("nan"))
                r = rows["%s|%s" % (sname, nm)]
                P("    %-26s %-9s N %3d  %8.2f / %+7.3f +- %.3f   %7.1f   %6.2f   f_M %.3f -> %s" % (sname, nm, r["N"], 1e15 * pmin, 1e15 * s["mean"], 1e15 * s["sigma"], r["z"], r["ratio"], r["f_M"], w))
        for nm in ("canonical", "alt"):
            w0 = rows["primary|%s" % nm]["word"]; moved = [t for t in TAGS if rows["%s|%s" % (t, nm)]["word"] != w0]
            W[nm] = w0 + (" [BRACKET-DEPENDENT: %s]" % ", ".join(moved) if moved and w0 != "NOT EVALUABLE" else "")
        P("  reading %s word: %s / %s" % (lab, W["canonical"], W["alt"]))
        RES["readings"][lab] = dict(rows=rows, word=W, k8=bool(k8a if lab == "A1" else k8r))
    # Part C under A1: the sky offset cancels in the difference; the checks other than K8 pass
    D = clip(f[A["pair_w"]]) - clip(A["pair_c_f"]); bd = boot(D); lo, hi = float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5))
    wc = ("WIDE LENSES ARE BRIGHTER IN X-RAYS" if lo > 0 else "NO EXCESS DETECTED") if (len(D) >= 100 and other_ok) else "NOT EVALUABLE"
    P("\n[Part C under A1] %d pairs: wide minus control %+.3f [%+.3f, %+.3f] x 1e-15 -> %s" % (len(D), 1e15 * D.mean(), 1e15 * lo, 1e15 * hi, wc))
    RES["partC"] = dict(N=len(D), mean=float(D.mean()), lo=lo, hi=hi, word=wc)
    if MUT:
        okm = MUT == "inject" and all(RES["readings"]["A1"]["rows"]["primary|%s" % nm]["word"] == "ALLOWED" for nm in ("canonical", "alt"))
        P("\n[MUTATE %s] A1 primary words %s / %s -> %s" % (MUT, RES["readings"]["A1"]["rows"]["primary|canonical"]["word"], RES["readings"]["A1"]["rows"]["primary|alt"]["word"],
          "BITES (exit 1)" if okm else "DOES NOT BITE (exit 2)"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(1 if okm else 2)
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
