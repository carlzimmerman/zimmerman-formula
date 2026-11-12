#!/usr/bin/env python3
"""EUC6 (WIDE-LENS ENVIRONMENT).  Frozen criteria: FROZEN_CRITERIA.md (commit 62dbaa183b).

Richness = neighbours brighter than H_E = 22 at 30-300 kpc minus the 600-1000 kpc background, around wide lenses (W),
controls matched in redshift and stellar mass (C), expert-flagged group-scale systems (L) and blank fields (R).

Run:
  python3 -I euc6.py --data-dir <dir with the two ECLIPSE csv files>     (needs euc6_targets.csv, euc6_rings.json)
  EUC6_MUTATE=shuffle python3 -I euc6.py --data-dir <dir>                (must exit 1)
"""
import argparse, csv, json, math, os, sys
import numpy as np
from scipy.stats import spearmanr, wilcoxon

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
MUT = (os.environ.get("EUC6_MUTATE", "") or "").strip()
AR = (300.0 ** 2 - 30.0 ** 2) / (1000.0 ** 2 - 600.0 ** 2)
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    tag = "euc6" + ("_MUTATE_" + MUT if MUT else "")
    P("EUC6 (WIDE-LENS ENVIRONMENT)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    T = list(csv.DictReader(open(os.path.join(HERE, "euc6_targets.csv")))); R = json.load(open(os.path.join(HERE, "euc6_rings.json")))
    for t in T:
        c = R.get(t["key"]); t["have"] = c is not None
        if c is not None:
            t["n_in"] = sum(c[3:30]); t["n_bg"] = sum(c[60:100]); t["delta"] = t["n_in"] - AR * t["n_bg"]
        t["pair"] = int(t["pair"]); t["z"] = float(t["z"]); t["lm"] = float(t["lm"]); t["tE"] = float(t["tE"])
    have = [t for t in T if t["have"]]
    P("\n[data] targets %d, with ring counts %d  (W %d, C %d, L %d, R %d)" % (len(T), len(have), *[sum(t["cls"] == k for t in have) for k in "WCLR"]))
    medbg = float(np.median([t["n_bg"] for t in have if t["cls"] in "WCL"])); floor = 0.4 * medbg
    P("  median background count at 600-1000 kpc: %.0f; coverage floor %.0f" % (medbg, floor))
    W = {t["pair"]: t for t in have if t["cls"] == "W"}; C = {t["pair"]: t for t in have if t["cls"] == "C"}
    pairs = [(W[k], C[k]) for k in sorted(set(W) & set(C))]
    nlow = sum(1 for w, c in pairs if w["n_bg"] < floor or c["n_bg"] < floor)
    pairs = [(w, c) for w, c in pairs if w["n_bg"] >= floor and c["n_bg"] >= floor]
    P("  complete pairs: %d (dropped for low coverage: %d)" % (len(pairs), nlow))
    dW = np.array([w["delta"] for w, c in pairs]); dC = np.array([c["delta"] for w, c in pairs]); D = dW - dC
    P("  match quality: median |dz| = %.3f, median |d log M*| = %.3f; W medians z %.3f, log M* %.2f, theta_E %.2f\"; C medians z %.3f, log M* %.2f, theta_E %.2f\""
      % (np.median([abs(w["z"] - c["z"]) for w, c in pairs]), np.median([abs(w["lm"] - c["lm"]) for w, c in pairs]),
         np.median([w["z"] for w, c in pairs]), np.median([w["lm"] for w, c in pairs]), np.median([w["tE"] for w, c in pairs]),
         np.median([c["z"] for w, c in pairs]), np.median([c["lm"] for w, c in pairs]), np.median([c["tE"] for w, c in pairs])))
    if MUT == "shuffle":
        sg = np.where(np.random.default_rng(20261113).random(len(D)) < 0.5, -1.0, 1.0); D = D * sg

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    dR = np.array([t["delta"] for t in have if t["cls"] == "R" and t["n_bg"] >= floor]); dL = np.array([t["delta"] for t in have if t["cls"] == "L" and t["n_bg"] >= floor])
    n1 = abs(float(np.median(dR))) <= 2.0 if len(dR) else False
    n2 = (float(np.median(dL)) - float(np.median(dC)) >= 3.0) if len(dL) else False
    P("  %s N1  blank fields: median richness %+.2f (N = %d; |median| <= 2.0)" % ("PASS" if n1 else "FAIL", np.median(dR) if len(dR) else float("nan"), len(dR)))
    P("  %s N2  expert-flagged group-scale systems: median richness %+.2f (N = %d) against controls %+.2f; difference %+.2f (>= 3.0)"
      % ("PASS" if n2 else "FAIL", np.median(dL) if len(dL) else float("nan"), len(dL), np.median(dC), (np.median(dL) - np.median(dC)) if len(dL) else float("nan")))

    # ---------------------------------------------------------------- statistic
    rng = np.random.default_rng(E.SEED)
    bs = np.array([np.median(D[rng.integers(0, len(D), len(D))]) for _ in range(2000)])
    lo, hi = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)); med = float(np.median(D))
    p = float(wilcoxon(D, alternative="greater").pvalue)
    if len(pairs) < 150 or not (n1 and n2): word = "NOT EVALUABLE"
    elif lo > 0 and p < 0.001: word = "WIDE LENSES SIT IN RICHER ENVIRONMENTS"
    elif hi <= 3.0: word = "NO RICHER"
    else: word = "NO VERDICT"
    P("\n[primary] paired difference in richness, wide minus control: median %+.2f [%+.2f, %+.2f] galaxies; mean %+.2f; Wilcoxon one-sided p = %.2e; N = %d pairs"
      % (med, lo, hi, D.mean(), p, len(D)))
    P("  LANE WORD: %s" % word)
    RES = dict(lane="EUC6", criteria_commit="62dbaa183b", mutate=MUT, n_pairs=len(pairs), median_D=med, lo=lo, hi=hi, mean_D=float(D.mean()), p=p, word=word,
               N1=dict(median=float(np.median(dR)) if len(dR) else None, n=len(dR), ok=bool(n1)), N2=dict(median_L=float(np.median(dL)) if len(dL) else None, n=len(dL), ok=bool(n2)))
    if MUT:
        ok = word != "WIDE LENSES SIT IN RICHER ENVIRONMENTS"
        P("\n[MUTATE %s] labels shuffled within pairs -> word %s; %s" % (MUT, word, "not RICHER, as required; exit 1" if ok else "STILL RICHER"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ok else 2)

    # ---------------------------------------------------------------- reported, no word
    P("\n[reported]")
    q = lambda x: (float(np.median(x)), float(np.percentile(x, 16)), float(np.percentile(x, 84)))
    for nm, x in (("wide lenses W", dW), ("controls C", dC), ("flagged group-scale L", dL), ("blank fields R", dR)):
        if len(x): P("  richness %-22s N = %3d   median %+6.2f   16-84%% %+6.2f to %+6.2f   mean %+6.2f" % (nm, len(x), *q(x), x.mean()))
    P("  fraction of W above the controls' 84th percentile: %.3f (16%% expected if alike)" % float(np.mean(dW > np.percentile(dC, 84))))
    zmed = float(np.median([w["z"] for w, c in pairs])); zl = np.array([w["z"] for w, c in pairs])
    for lab, m in (("z_l below %.2f" % zmed, zl < zmed), ("z_l above %.2f" % zmed, zl >= zmed)):
        P("  %-16s pairs %3d   median D %+.2f   W %+.2f   C %+.2f" % (lab, int(m.sum()), np.median(D[m]), np.median(dW[m]), np.median(dC[m])))
    rows, _ = E.load(a.data_dir); E.OUT.clear(); Sm, _ = E.select(rows, ("A", "B")); byid = {r["id"]: r for r in Sm}
    def binf(ts):
        smp = [byid[t["id"]] for t in ts]; eng, z, RE, Re, n, lm = E.build(smp)
        return eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), E.FOOT["alt"], "S")
    bW = binf([w for w, c in pairs]); bC = binf([c for w, c in pairs])
    r1 = spearmanr(dW, bW); r2 = spearmanr(np.concatenate([dW, dC]), np.concatenate([bW, bC]))
    P("  Spearman of richness with the source-free boost b_inf (law S, alt): inside W %.3f (p = %.2e); W and C together %.3f (p = %.2e)" % (r1[0], r1[1], r2[0], r2[1]))
    RES.update(reported=dict(W=q(dW), C=q(dC), L=q(dL) if len(dL) else None, R=q(dR) if len(dR) else None, frac_above_p84=float(np.mean(dW > np.percentile(dC, 84))),
                             spearman_W=[float(r1[0]), float(r1[1])], spearman_WC=[float(r2[0]), float(r2[1])]))
    with open(os.path.join(HERE, "euc6_per_target.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["key", "class", "pair", "z", "log_Mstar", "theta_E_arcsec", "n_in_30_300kpc", "n_bg_600_1000kpc", "richness"])
        for t in have: w.writerow([t["key"], t["cls"], t["pair"], "%.3f" % t["z"], "%.3f" % t["lm"], "%.3f" % t["tE"], t["n_in"], t["n_bg"], "%.2f" % t["delta"]])
    P("\n[summary]")
    P("  instrument checks: N1 %s, N2 %s" % ("pass" if n1 else "FAIL", "pass" if n2 else "FAIL"))
    P("  LANE WORD: %s" % word)
    P("  kappa = 1/2 FITTED. No outcome favours the framework.")
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if word != "NOT EVALUABLE" else 3)

if __name__ == "__main__":
    main()
