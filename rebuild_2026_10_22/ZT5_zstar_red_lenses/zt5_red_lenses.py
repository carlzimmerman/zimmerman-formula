#!/usr/bin/env python3
"""ZT5_zstar_red_lenses: Z-star test Z-T5 (red lenses from baryon loss), as frozen in Z1 TEST_PLAN (0d1959a4f5).

Criteria: FROZEN_CRITERIA.md (2e8ab8f42f, committed alone first).  kappa = 1/2 FITTED.  Not "theory closed".
Run:   OMP_NUM_THREADS=1 nice -n 15 python3 zt5_red_lenses.py [--mutate]
"""
import os, sys, json, math, resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUTL = []
RES = dict(lane="ZT5_zstar_red_lenses", criteria="2e8ab8f42f", mutate=MUT, checks={})
FOOTS = ("canonical", "alt")


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(key, ok, value):
    RES["checks"][key] = dict(ok=bool(ok), value=value); P(f"{key} {'PASS' if ok else 'FAIL'}  {value}")


# observed (S2 committed)
S2 = json.load(open(os.path.join(os.path.dirname(HERE), "S2_v3_lowg_lensing", "s2_v3_lowg_lensing_results.json")))["ladder"]
L4 = "L4 + hot CGM 0.5 M* (v3 at y_e = 0)"
OBS = {f: dict(red=S2[f][L4]["red"]["A"], s_red=S2[f][L4]["red"]["sA"], blue=S2[f][L4]["blue"]["A"]) for f in FOOTS}
plan = {"canonical": (1.313, 0.063, 0.878), "alt": (1.200, 0.058, 0.802)}
ks = all(abs(OBS[f]["red"] - plan[f][0]) <= 1e-3 and abs(OBS[f]["s_red"] - plan[f][1]) <= 1e-3 and abs(OBS[f]["blue"] - plan[f][2]) <= 1e-3 for f in FOOTS)
check("KS", ks, "; ".join(f"{f} red {OBS[f]['red']:.4f} +- {OBS[f]['s_red']:.4f}, blue {OBS[f]['blue']:.4f}" for f in FOOTS))

# red lenses
LN = np.load(os.path.join(DATA, "lensing_rar", "lr_lenses.npz"))
lmr = LN["logM"][LN["typ"] == 1]
P(f"red lenses (typ 1): N {lmr.size}, log M* 16/50/84 % = " + ", ".join(f"{v:.3f}" for v in np.percentile(lmr, [16, 50, 84])))

# ALFALFA-SDSS gas scaling (G1, RAW, HI-selected => upper bound)
rows = []
for line in open(os.path.join(DATA, "alfalfa_sdss_durbala2020_t2.tsv")):
    if line.startswith("#") or not line.strip():
        continue
    t = line.rstrip("\n").split("\t")
    if len(t) < 9:
        continue
    try:
        gi, lmt, lhi = float(t[2]), float(t[3]), float(t[7])
    except ValueError:
        continue
    rows.append((gi, lmt, lhi))
A = np.array(rows); gi, lms, lhi = A[:, 0], A[:, 1], A[:, 2]
lf = np.log10(1.33) + lhi - lms + (-np.inf if MUT else 0.0)


def scaling(sel):
    edges = np.round(np.arange(7.0, 12.01, 0.1), 2); xc, yc, nmin = [], [], 10 ** 9
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = sel & (lms >= lo) & (lms < hi)
        if m.sum() >= 20:
            xc.append(0.5 * (lo + hi)); yc.append(float(np.median(lf[m]))); nmin = min(nmin, int(m.sum()))
    return np.array(xc), np.array(yc), nmin


def predict(xc, yc, lm):
    return np.sqrt(1 + 10 ** np.interp(lm, xc, yc))


G = {}
for lab, sel in (("G1_all", np.isfinite(lms) & np.isfinite(lhi)), ("G1b_gi_le_0.9", np.isfinite(lms) & np.isfinite(lhi) & (gi <= 0.9))):
    xc, yc, nmin = scaling(sel)
    out = (lmr < xc[0]) | (lmr > xc[-1])
    pr = float(np.mean(predict(xc, yc, lmr)))
    fmed = float(10 ** np.interp(np.median(lmr), xc, yc))
    G[lab] = dict(n_rows=int(sel.sum()), bin_range=[float(xc[0]), float(xc[-1])], min_bin_n=nmin, frac_red_outside=float(out.mean()),
                  f_gas_at_median=fmed, pred=pr, f_lens=10 ** np.interp(lmr, xc, yc))
    P(f"{lab}: {sel.sum()} rows, bins {xc[0]:.2f}-{xc[-1]:.2f} (min n {nmin}); f_gas at red median M* {fmed:.3f}; "
      f"red lenses outside binned range {out.mean():.3f}; prediction <sqrt(1+f)> = {pr:.4f}")
fG2 = 10 ** (-0.69 * lmr + 6.63)
predG2 = float(np.mean(np.sqrt(1 + fG2)))
P(f"G2 (B21 relation, SURVEY-CALIBRATION, reported): f_cold at red median {10 ** (-0.69 * np.median(lmr) + 6.63):.3f}; prediction {predG2:.4f}")
check("KG", abs(10 ** (-0.69 * 10.7 + 6.63) - 10 ** (-0.753)) < 1e-9, "B21 relation at 10.7")
check("KN", G["G1_all"]["n_rows"] >= 1000 and G["G1_all"]["min_bin_n"] >= 20, f"rows {G['G1_all']['n_rows']}, min bin {G['G1_all']['min_bin_n']}")
check("KM", G["G1_all"]["pred"] > 1.0, f"prediction {G['G1_all']['pred']:.4f} > 1")
cons = float(np.mean(np.sqrt((1 + G["G1_all"]["f_lens"] + 0.5) / (1 + fG2 + 0.5))))
P(f"reported: baseline-consistent prediction sqrt[(1+f_G1+0.5)/(1+f_G2+0.5)] = {cons:.4f}")

pr = G["G1_all"]["pred"]
for f in FOOTS:
    d = OBS[f]["red"] - pr; z = d / OBS[f]["s_red"]
    cls = "PASS" if abs(z) <= 2 else ("FAIL (ROBUST: data above the upper-bound prediction)" if z > 2 else "FAIL")
    zv = {k: (OBS[f]["red"] - v) / OBS[f]["s_red"] for k, v in (("G1b", G["G1b_gi_le_0.9"]["pred"]), ("G2", predG2), ("consistent", cons))}
    RES[f] = dict(obs=OBS[f], pred_G1=pr, z_G1=z, z_reported=zv, cls=cls)
    P(f"[{f}] A_red {OBS[f]['red']:.3f} +- {OBS[f]['s_red']:.3f} vs predicted {pr:.3f}: z {z:+.2f} -> {cls};  reported z: G1b {zv['G1b']:+.2f}, "
      f"G2 {zv['G2']:+.2f}, baseline-consistent {zv['consistent']:+.2f};  blue {OBS[f]['blue']:.3f} (by construction)")
cl = [RES[f]["cls"].split()[0] for f in FOOTS]
V = "PASS" if cl == ["PASS", "PASS"] else ("FAIL" if cl == ["FAIL", "FAIL"] else "SPLIT")
RES["verdict"] = V
for k in G:
    G[k].pop("f_lens")
RES["scalings"] = G; RES["pred_G2"] = predG2; RES["pred_consistent"] = cons
P(f"VERDICT Z-T5: {V}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("KR", rss < 1.0, f"{rss:.2f} GB")
allok = all(v["ok"] for v in RES["checks"].values())
P(f"checks: {'ALL PASS' if allok else 'SOME FAIL'}")
open(os.path.join(HERE, f"zt5_red_lenses{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
json.dump(RES, open(os.path.join(HERE, f"zt5_red_lenses_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if allok else 1)
