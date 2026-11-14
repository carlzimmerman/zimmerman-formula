#!/usr/bin/env python3
"""EUC20, exact-shift part.  Frozen criteria: FROZEN_CRITERIA.md (commit cbd14e4ca4).

G1: EUC4's secondary bin (grade B, 1.3 <= theta_E < 1.7 arcsec) re-read with the in-mask stellar mass, by
b_corr = b + log10 f on boosts computed at full precision with EUC1's and EUC4's imported code.  Reported: EUC4's
complement bin (theta_E < 1.0), and W_B as a cross-check against EUC17.  A lens without a mask keeps its catalogued
mass; a bin with more than 5 % such lenses is NOT EVALUABLE.

Also the EUC6 reading: the mass mismatch the correction opens between each wide lens and its control.

  python3 -I euc20_bins.py --data-dir <dir with the two ECLIPSE csv files>
  EUC20_MUTATE=invert python3 -I euc20_bins.py --data-dir <dir>      (must exit 1)
"""
import argparse, csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12")
sys.path.insert(0, os.path.join(D12, "EUC1_eclipse_saturation_ceiling"))
sys.path.insert(0, os.path.join(D12, "EUC4_wide_lenses"))
import euc1 as E          # noqa: E402
import euc4 as W          # noqa: E402
TABLES = [os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_masks.csv"),
          os.path.join(REPO, "closure_2026_11_14", "EUC19_grade_b_mask_table", "euc19_masks.csv")]
EUC6 = os.path.join(D12, "EUC6_wide_lens_environment")
MUT = (os.environ.get("EUC20_MUTATE", "") or "").strip()
if MUT not in ("", "invert"): sys.exit("unknown EUC20_MUTATE")
TAG = "euc20_bins" + ("_MUTATE_" + MUT if MUT else "")
VARIANTS = ("primary", "F1a", "F1b")
KEYS = [(law, nm) for law in ("S", "B") for nm in E.FOOT]
NAMES = [("W_B", "W_B: theta_E >= 1.7 arcsec (primary)"), ("secondary", "secondary: 1.3 <= theta_E < 1.7"), ("complement", "complement: theta_E < 1.0")]
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def fmt(st):
    return "N=%4d  f25 = %.3f [%.3f, %.3f]  f0 = %.3f  b_med = %+.3f [%+.3f, %+.3f]" % (
        st["N"], st["f25"], st["f25_lo"], st["f25_hi"], st["f0"], st["b_med"], st["b_med_lo"], st["b_med_hi"])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    P("EUC20 exact-shift part (EUC4's grade-B bins; EUC6 reading)%s   criteria cbd14e4ca4" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    R = {}
    for t in TABLES:
        for r in csv.DictReader(open(t, newline="")):
            if r["has_mask"] == "1": R[r["unique_identifier"]] = float(r["mask_radius_arcsec"])
    rows, _ = E.load(a.data_dir)
    for s in E.OUT: OUT.append(s)
    E.OUT.clear()
    byid = {r["id"]: r for r in rows}
    Bm, _ = E.select(rows, ("B",))
    G = {"W_B": [r for r in Bm if r["tE"] >= 1.7], "secondary": [r for r in Bm if 1.3 <= r["tE"] < 1.7], "complement": [r for r in Bm if r["tE"] < 1.0]}
    RES = dict(lane="EUC20", part="bins", criteria_commit="cbd14e4ca4", mutate=MUT, masks=len(R))

    def lf_of(smp, variant):
        sc = 0.80 if variant == "F1a" else 1.25 if variant == "F1b" else 1.0
        lf = np.array([math.log10(float(E.M2D_frac(R[r["id"]], r["te"] * sc, r["n"]))) if r["id"] in R else 0.0 for r in smp])
        return -lf if MUT == "invert" else lf

    Bst = {}
    for g, _n in NAMES:
        eng, z, RE, Re, n, lm = E.build(G[g])
        Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        Bst[g] = {k: eng.solve_b(Mmin, E.FOOT[k[1]], k[0]) for k in KEYS}
    ref = json.load(open(os.path.join(D12, "EUC4_wide_lenses", "euc4_results.json")))["partA"]

    P("\n[checks]")
    bad = []; rng = np.random.default_rng(E.SEED)
    for g, name in NAMES:
        for law, nm in KEYS:
            st = E.stats(Bst[g][(law, nm)], rng); st["word"] = W.word(st); c = ref[name]["%s_%s" % (law, nm)]
            if abs(st["f25"] - c["f25"]) > 1e-9 or abs(st["b_med"] - c["b_med"]) > 1e-9 or abs(st["f0"] - c["f0"]) > 1e-9 \
               or any(abs(st[k] - c[k]) > 0.01 for k in ("f25_lo", "f25_hi", "f0_lo", "f0_hi", "b_med_lo", "b_med_hi")) or st["word"] != c["word"] or st["N"] != c["N"]:
                bad.append("%s %s %s" % (g, law, nm))
    k0 = not bad
    P("  %s H0  f = 1 reproduces every committed statistic and word of EUC4's three grade-B bins%s" % ("PASS" if k0 else "FAIL", "" if k0 else ": " + ", ".join(bad)))
    cov = {g: dict(N=len(G[g]), without_mask=sum(1 for r in G[g] if r["id"] not in R)) for g, _n in NAMES}
    P("  note H4  lenses without a mask (they keep the catalogued mass): " + "; ".join("%s %d of %d" % (g, cov[g]["without_mask"], cov[g]["N"]) for g, _n in NAMES))
    RES["H0"] = bool(k0); RES["coverage"] = cov

    ALL = {}
    for v in VARIANTS:
        rng = np.random.default_rng(E.SEED); ALL[v] = {}
        for g, _n in NAMES:
            lf = lf_of(G[g], v); ALL[v][g] = {}
            for law, nm in KEYS:
                st = E.stats(Bst[g][(law, nm)] + lf, rng); st["word"] = W.word(st)
                if cov[g]["without_mask"] > 0.05 * cov[g]["N"]: st["word_before_5pct_rule"] = st["word"]; st["word"] = "NOT EVALUABLE"
                st["uncorrected_f25"] = float(np.mean(Bst[g][(law, nm)] > E.B_STAR))
                ALL[v][g]["%s_%s" % (law, nm)] = st
            ALL[v][g]["median_correction_dex"] = float(np.median(-lf))
    RES["reread"] = ALL

    P("\n[re-read, corrected stellar mass: committed -> corrected (primary f)]")
    for g, name in NAMES:
        P("  %s (median correction %.3f dex)" % (name, abs(ALL["primary"][g]["median_correction_dex"])))
        for law, nm in KEYS:
            c = ref[name]["%s_%s" % (law, nm)]; s = ALL["primary"][g]["%s_%s" % (law, nm)]
            P("    law %s %-9s f25 %.3f [%.3f, %.3f] %s  ->  %s  -> %s" % (law, nm, c["f25"], c["f25_lo"], c["f25_hi"], c["word"], fmt(s), s["word"]))
    P("\n[labels: G1, EUC4's secondary bin, law S]")
    LAB = {}
    for nm in E.FOOT:
        com = ref[NAMES[1][1]]["S_" + nm]["word"]; w = ALL["primary"]["secondary"]["S_" + nm]["word"]
        other = [v for v in ("F1a", "F1b") if ALL[v]["secondary"]["S_" + nm]["word"] != w]
        if not k0: w = "NOT EVALUABLE"
        LAB[nm] = dict(committed=com, corrected=w, change="UNCHANGED" if w == com else "CHANGED", stability="FRAGILE" if other else "ROBUST", brackets_with_other_word=other)
        P("  G1 %-9s committed %s -> corrected %s: %s, %s%s" % (nm, com, w, LAB[nm]["change"], LAB[nm]["stability"], (" (" + ", ".join(other) + ")") if other else ""))
    RES["labels_G1"] = LAB
    P("\n[brackets, law S f25 (lower, upper), canonical / alt]")
    for v in VARIANTS:
        P("  %-8s " % v + " | ".join("%s %.3f [%.3f, %.3f] / %.3f [%.3f, %.3f] %s / %s" % (
            g, ALL[v][g]["S_canonical"]["f25"], ALL[v][g]["S_canonical"]["f25_lo"], ALL[v][g]["S_canonical"]["f25_hi"],
            ALL[v][g]["S_alt"]["f25"], ALL[v][g]["S_alt"]["f25_lo"], ALL[v][g]["S_alt"]["f25_hi"],
            ALL[v][g]["S_canonical"]["word"], ALL[v][g]["S_alt"]["word"]) for g, _n in NAMES))

    code = 0 if k0 else 2
    if MUT == "invert":
        ok = all(ALL["primary"]["secondary"]["S_" + nm]["f25"] >= ALL["primary"]["secondary"]["S_" + nm]["uncorrected_f25"] - 1e-12 for nm in E.FOOT)
        P("\n[twin invert] with the shift reversed G1's f25 does not fall on either footing: %s" % ("YES" if ok else "NO"))
        RES["twin_ok"] = bool(ok); code = 1 if ok else 3
    else:
        # ------------------------------------------------------------ EUC6 reading
        P("\n[EUC6 reading: mass mismatch between each wide lens and its control once the mass is corrected]")
        T = {r["key"]: r for r in csv.DictReader(open(os.path.join(EUC6, "euc6_targets.csv")))}
        rich = {r["key"]: float(r["richness"]) for r in csv.DictReader(open(os.path.join(EUC6, "euc6_per_target.csv")))}
        def lmc(t):
            r = byid.get(t["id"]); lm = float(t["lm"])
            if r is None or t["id"] not in R: return lm, False
            return lm - math.log10(float(E.M2D_frac(R[t["id"]], r["te"], r["n"]))), True
        pairs = {}
        for k, t in T.items():
            if t["cls"] in ("W", "C") and k in rich: pairs.setdefault(t["pair"], {})[t["cls"]] = t
        pr = [(p["W"], p["C"]) for p in pairs.values() if "W" in p and "C" in p]
        d0 = np.array([float(w["lm"]) - float(c["lm"]) for w, c in pr])
        lw = [lmc(w) for w, c in pr]; lc = [lmc(c) for w, c in pr]
        d1 = np.array([x[0] - y[0] for x, y in zip(lw, lc)])
        nomask = sum(1 for x in lw if not x[1]) + sum(1 for x in lc if not x[1])
        D = np.array([rich[w["key"]] - rich[c["key"]] for w, c in pr])
        xc = np.array([y[0] for y in lc]); yc = np.array([rich[c["key"]] for w, c in pr])
        rng = np.random.default_rng(E.SEED); N = len(pr)
        bs_d, bs_s, bs_w = [], [], []
        for _ in range(2000):
            i = rng.integers(0, N, N)
            s = np.polyfit(xc[i], yc[i], 1)[0]; m = np.median(d1[i])
            bs_d.append(m); bs_s.append(s); bs_w.append(s * m)
        slope = float(np.polyfit(xc, yc, 1)[0]); med = float(np.median(d1))
        ci = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
        e6 = json.load(open(os.path.join(EUC6, "euc6_results.json")))
        P("  pairs with a wide lens and a control: %d (targets without a mask: %d); median paired richness difference %+.2f" % (N, nomask, float(np.median(D))))
        P("  median log-mass difference, wide minus control: catalogue %+.3f dex -> corrected %+.3f dex [%+.3f, %+.3f]" % (float(np.median(d0)), med, ci(bs_d)[0], ci(bs_d)[1]))
        P("  controls' richness-mass slope (least squares, corrected mass): %+.2f galaxies per dex [%+.2f, %+.2f]" % (slope, ci(bs_s)[0], ci(bs_s)[1]))
        P("  richness that mass difference is worth on that slope: %+.2f galaxies [%+.2f, %+.2f]" % (slope * med, ci(bs_w)[0], ci(bs_w)[1]))
        RES["EUC6_reading"] = dict(pairs=N, targets_without_mask=nomask, median_D=float(np.median(D)), mass_diff_catalogue=float(np.median(d0)),
                                   mass_diff_corrected=med, mass_diff_ci=ci(bs_d), slope=slope, slope_ci=ci(bs_s), worth=slope * med, worth_ci=ci(bs_w),
                                   euc6_keys=sorted(e6.keys())[:12])
    P("\nexit %d" % code)
    json.dump(RES, open(os.path.join(HERE, TAG + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)


if __name__ == "__main__":
    main()
