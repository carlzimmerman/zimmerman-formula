#!/usr/bin/env python3
"""EUC20R exact-shift route and catalogue-side readings (READING.md sections 2, 4 H4, 5).

  python3 -I -B euc20r_shift.py

- EUC4's three grade-B bins (W_B, secondary = row G1, complement): b at full precision with EUC1's and EUC4's imported
  code, b_corr = b + log10 f (f1: no shift; invert: b - log10 f), EUC1's stats from one generator seeded 20261112 in
  EUC4's order, EUC4's words.  One output file per mode: runs/<mode>/euc4_bins.json.
- Mask coverage of the catalogue samples (H4): runs/coverage.json.
- EUC6 reading: the 243 pairs rebuilt from EUC6's committed targets and ring counts; corrected log-mass difference
  wide minus control; the controls' richness-mass slope; the worth.  runs/<mode>/euc6_reading.json (primary, F1a, F1b).
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import builtins, csv, json, math, os, sys
sys.dont_write_bytecode = True
for _v in ("EUC1_MUTATE", "EUC4_MUTATE"):
    os.environ.pop(_v, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import euc20r_common as C

E = C.euc1()
sys.path.insert(0, C.DIRS["EUC4"])
import euc4 as W4                                   # EUC4's word rule; its import of euc1 is the same module
assert W4.E is E


def logf_vec(sample, mode):
    sh = C.Shifter(mode)
    lf = np.zeros(len(sample)); has = np.zeros(len(sample), bool)
    for i, r in enumerate(sample):
        lf[i], has[i] = sh.logf(r["id"], r["te"], r["n"])
    return lf, has


def main():
    os.chdir(C.REPO)
    rows, _ = E.load(C.rel(C.DATA)); E.OUT.clear()
    Pm, _ = E.select(rows, ("A",)); Bm, _ = E.select(rows, ("B",)); Sm, _ = E.select(rows, ("A", "B"))
    bins = [("W_B: theta_E >= 1.7 arcsec (primary)", [r for r in Bm if r["tE"] >= 1.7]),
            ("secondary: 1.3 <= theta_E < 1.7", [r for r in Bm if 1.3 <= r["tE"] < 1.7]),
            ("complement: theta_E < 1.0", [r for r in Bm if r["tE"] < 1.0])]

    # ---------------------------------------------------------------- b at full precision, once
    B = {}
    for name, smp in bins:
        eng, z, RE, Re, n, lm = E.build(smp)
        Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        B[name] = {law + "_" + nm: eng.solve_b(Mmin, a0, law) for law in ("S", "B") for nm, a0 in E.FOOT.items()}

    # ---------------------------------------------------------------- coverage (H4), primary share
    cov = {}
    for lab, smp in (("P", Pm), ("S", Sm), ("grade_B", Bm)) + tuple((nm.split(":")[0], s) for nm, s in bins):
        _, has = logf_vec(smp, "primary")
        cov[lab] = dict(N=len(smp), with_mask=int(has.sum()), without=int((~has).sum()),
                        frac_without=float(np.mean(~has)) if len(smp) else float("nan"),
                        ids_without=[r["id"] for r, h in zip(smp, has) if not h][:50])
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    with builtins.open(os.path.join(HERE, "runs", "coverage.json"), "w") as f:
        json.dump(cov, f, indent=1)

    # ---------------------------------------------------------------- the bins under each mode
    for mode in C.MODES:
        rng = np.random.default_rng(E.SEED)
        out = dict(mode=mode, re_scale=C.RE_SCALE[mode], bins={})
        for name, smp in bins:
            lf, has = logf_vec(smp, mode)
            sgn = 0.0 if mode == "f1" else (-1.0 if mode == "invert" else 1.0)
            g = {}
            for k in ("S_canonical", "S_alt", "B_canonical", "B_alt"):
                bc = B[name][k] + sgn * lf if sgn != 0.0 else B[name][k]
                st = E.stats(bc, rng); st["word"] = W4.word(st); g[k] = st
            g["coverage"] = dict(N=len(smp), with_mask=int(has.sum()))
            g["minus_logf"] = dict(median=float(np.median(-lf[has])) if has.any() else float("nan"),
                                   p16=float(np.percentile(-lf[has], 16)) if has.any() else float("nan"),
                                   p84=float(np.percentile(-lf[has], 84)) if has.any() else float("nan"))
            out["bins"][name] = g
        d = os.path.join(HERE, "runs", mode); os.makedirs(d, exist_ok=True)
        with builtins.open(os.path.join(d, "euc4_bins.json"), "w") as f:
            json.dump(out, f, indent=1)
        for name in out["bins"]:
            g = out["bins"][name]
            print("[%s] %-38s S %s / %s   f25 %.3f [%.3f, %.3f] / %.3f [%.3f, %.3f]" % (
                mode, name, g["S_canonical"]["word"], g["S_alt"]["word"], g["S_canonical"]["f25"], g["S_canonical"]["f25_lo"],
                g["S_canonical"]["f25_hi"], g["S_alt"]["f25"], g["S_alt"]["f25_lo"], g["S_alt"]["f25_hi"]))

    # ---------------------------------------------------------------- EUC6 reading
    d6 = C.DIRS["EUC6"]
    T = list(csv.DictReader(builtins.open(os.path.join(d6, "euc6_targets.csv"))))
    R = json.load(builtins.open(os.path.join(d6, "euc6_rings.json")))
    AR = (300.0 ** 2 - 30.0 ** 2) / (1000.0 ** 2 - 600.0 ** 2)
    for t in T:                                               # EUC6's own reconstruction, line for line
        c = R.get(t["key"]); t["have"] = c is not None
        if c is not None:
            t["n_in"] = sum(c[3:30]); t["n_bg"] = sum(c[60:100]); t["delta"] = t["n_in"] - AR * t["n_bg"]
        t["pair"] = int(t["pair"]); t["z"] = float(t["z"]); t["lm"] = float(t["lm"]); t["tE"] = float(t["tE"])
    have = [t for t in T if t["have"]]
    medbg = float(np.median([t["n_bg"] for t in have if t["cls"] in "WCL"])); floor = 0.4 * medbg
    Wd = {t["pair"]: t for t in have if t["cls"] == "W"}; Cd = {t["pair"]: t for t in have if t["cls"] == "C"}
    pairs = [(Wd[k], Cd[k]) for k in sorted(set(Wd) & set(Cd))]
    pairs = [(w, c) for w, c in pairs if w["n_bg"] >= floor and c["n_bg"] >= floor]
    Dv = np.array([w["delta"] - c["delta"] for w, c in pairs])
    byid = {r["id"]: r for r in Sm}
    lm_dev = max(abs(byid[t["id"]]["lm"] - t["lm"]) for w, c in pairs for t in (w, c))
    harness = dict(pairs=len(pairs), median_D=float(np.median(Dv)), max_lm_target_vs_loader=float(lm_dev),
                   ok=bool(len(pairs) == 243 and abs(float(np.median(Dv)) - 3.38) <= 0.005 and lm_dev <= 1e-5))
    print("[EUC6 harness] pairs %d, median D %+.3f, max |lm target - loader| %.1e -> %s" % (len(pairs), np.median(Dv), lm_dev, "ok" if harness["ok"] else "FAIL"))
    for mode in ("primary", "F1a", "F1b"):
        sh = C.Shifter(mode)
        def corr(t):
            r = byid[t["id"]]; lf, ok = sh.logf(r["id"], r["te"], r["n"]); return r["lm"] - lf, ok
        cw = [corr(w) for w, c in pairs]; cc = [corr(c) for w, c in pairs]
        lmW = np.array([x[0] for x in cw]); lmC = np.array([x[0] for x in cc])
        lmW0 = np.array([byid[w["id"]]["lm"] for w, c in pairs]); lmC0 = np.array([byid[c["id"]]["lm"] for w, c in pairs])
        hasW = np.array([x[1] for x in cw]); hasC = np.array([x[1] for x in cc])
        dC = np.array([c["delta"] for w, c in pairs])
        dl = lmW - lmC; dl0 = lmW0 - lmC0
        slope = float(np.polyfit(lmC, dC, 1)[0]); slope0 = float(np.polyfit(lmC0, dC, 1)[0])
        worth = slope * float(np.median(dl))
        rng = np.random.default_rng(E.SEED); bw, bsl, bdl = [], [], []
        for _ in range(2000):
            ix = rng.integers(0, len(pairs), len(pairs))
            s_ = float(np.polyfit(lmC[ix], dC[ix], 1)[0]); m_ = float(np.median(dl[ix]))
            bw.append(s_ * m_); bsl.append(s_); bdl.append(m_)
        rd = dict(mode=mode, pairs=len(pairs), lenses=2 * len(pairs), with_mask=int(hasW.sum() + hasC.sum()),
                  W_with_mask=int(hasW.sum()), C_with_mask=int(hasC.sum()),
                  median_dlm_corrected=float(np.median(dl)), dlm_corr_lo=float(np.percentile(bdl, 2.5)), dlm_corr_hi=float(np.percentile(bdl, 97.5)),
                  median_dlm_catalogued=float(np.median(dl0)),
                  median_minus_logf_W=float(np.median(lmW - lmW0)), median_minus_logf_C=float(np.median(lmC - lmC0)),
                  slope_controls_corrected=slope, slope_lo=float(np.percentile(bsl, 2.5)), slope_hi=float(np.percentile(bsl, 97.5)),
                  slope_controls_catalogued=slope0,
                  worth=worth, worth_lo=float(np.percentile(bw, 2.5)), worth_hi=float(np.percentile(bw, 97.5)),
                  worth_catalogued_slope=slope0 * float(np.median(dl)),
                  euc6_excess=3.38, euc6_lower_bound=2.28, share_of_excess=worth / 3.38,
                  needs_rematch=bool(abs(worth) >= 3.38 / 3.0), reaches_lower_bound=bool(worth >= 2.28),
                  harness=harness)
        d = os.path.join(HERE, "runs", mode); os.makedirs(d, exist_ok=True)
        with builtins.open(os.path.join(d, "euc6_reading.json"), "w") as f:
            json.dump(rd, f, indent=1)
        print("[EUC6 %s] median dlm corrected %+.4f (catalogued %+.4f); slope %.2f gal/dex [%.2f, %.2f]; worth %+.2f [%+.2f, %+.2f] galaxies"
              % (mode, rd["median_dlm_corrected"], rd["median_dlm_catalogued"], slope, rd["slope_lo"], rd["slope_hi"], worth, rd["worth_lo"], rd["worth_hi"]))


if __name__ == "__main__":
    main()
