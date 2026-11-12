#!/usr/bin/env python3
"""EUC5 POST HOC scale calibration (after A1's failed recovery gate; nothing here is a gate).

Step 1  noise bias on REAL spectra: the 30 SLACS SDSS spectra of check F4 are refitted after noise is added to bring
        them to DESI's signal-to-noise (3.7 per 1 A pixel = 3.3 per 0.8 A pixel), 10 realisations each.  The ratio
        sigma(noisy) / sigma(as observed) is the fitter's low signal-to-noise bias on real early-type spectra.
Step 2  the DESI-fitted dispersions of Euclid lens galaxies (A1) are put on the scale of the published SLACS
        dispersions: sigma_cal = sigma_raw / (noise ratio x 1.068), 1.068 being F4's fitted / published ratio.
        b_dyn is recomputed, whole sample and by Einstein radius, with the calibration's own uncertainty.

Run:  python3 -I euc5_a2_scale.py --data-dir <ECLIPSE dir> --templates <E-MILES dir> --cache <dir with the SLACS spectra>
"""
import argparse, csv, glob, json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc5 as D
import euc5_a1_fit as FIT
E = D.E
TARGET_SNR = 3.3 * math.sqrt(1.0 / 0.8)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--templates", required=True); ap.add_argument("--cache", required=True)
    a = ap.parse_args(); t0 = time.time(); out = []
    def P(s=""):
        print(s, flush=True); out.append(s)
    P("EUC5 POST HOC scale calibration (not a gate)")
    F = FIT.Fitter(a.templates); FIT.DEGREE, FIT.MDEGREE = 8, 0
    f4 = json.load(open(os.path.join(HERE, "euc5_f4_slacs.json"))); zmap = {}
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]; hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    for l in lines[hi + 3:]:
        q = l.split("\t")
        if len(q) >= len(hdr) and q[col["zlens"]].strip(): zmap[q[col["SDSS"]].strip()] = float(q[col["zlens"]])
    rng = np.random.default_rng(E.SEED); rows = []
    for r in f4["rows"]:
        sp = np.load(os.path.join(a.cache, r["name"] + ".npz")); wl = sp["wavelength"].astype(float); ivr = sp["ivar"].astype(float)
        lin = np.arange(wl[0], wl[-1], 1.0); fl = np.interp(lin, wl, sp["flux"].astype(float))
        iv = np.interp(lin, wl, ivr) * np.interp(lin, wl, np.gradient(wl)); iv = np.where(np.interp(lin, wl, (ivr > 0).astype(float)) > 0.99, iv, 0.0)
        ws = np.interp(lin, wl, sp["wave_sigma"].astype(float))
        if np.nanmedian(ws[ws > 0]) < 3.0 and np.nanmedian(ws[(lin > 8000) & (ws > 0)]) < 1.25 * np.nanmedian(ws[(lin < 4500) & (ws > 0)]): ws = ws * 1.0e-4 * math.log(10.0) * lin
        z = zmap[r["name"]]; base = FIT.Fitter.fit(F, lin, fl, iv, np.zeros(len(lin), int), ws, z)
        if base is None or base["snr"] <= TARGET_SNR: continue
        # extra noise so that the fit's own signal-to-noise measure comes down to the target
        sig0 = np.where(iv > 0, 1.0 / np.sqrt(np.where(iv > 0, iv, 1.0)), 0.0); k = base["snr"] / TARGET_SNR
        add = sig0 * math.sqrt(max(k * k - 1.0, 0.0)); rec = []
        for _ in range(10):
            fn = fl + rng.standard_normal(len(lin)) * add
            rr = FIT.Fitter.fit(F, lin, fn, np.where(iv > 0, iv / (k * k), 0.0), np.zeros(len(lin), int), ws, z)
            if rr is not None and np.isfinite(rr["sigma"]): rec.append(rr["sigma"])
        if len(rec) >= 5: rows.append(dict(name=r["name"], s_hi=base["sigma"], s_noisy=float(np.median(rec)), n=len(rec), sd=float(np.std(rec)), pub=r["pub"]))
    rat = np.array([x["s_noisy"] / x["s_hi"] for x in rows]); shi = np.array([x["s_hi"] for x in rows])
    bs = np.array([np.median(rat[rng.integers(0, len(rat), len(rat))]) for _ in range(2000)])
    P("\n[step 1] noise bias on real spectra at S/N %.1f per 1 A pixel: %d SLACS spectra, 10 realisations each" % (TARGET_SNR, len(rows)))
    P("  sigma(noisy) / sigma(as observed): median %.3f [%.3f, %.3f], mean %.3f; per-realisation scatter %.0f%%"
      % (np.median(rat), np.percentile(bs, 2.5), np.percentile(bs, 97.5), rat.mean(), 100 * np.median([x["sd"] / x["s_hi"] for x in rows])))
    for lo, hi in ((0, 240), (240, 290), (290, 999)):
        m = (shi >= lo) & (shi < hi)
        if m.sum() >= 4: P("    sigma %3d-%3d km/s: N = %2d, ratio %.3f" % (lo, hi, int(m.sum()), np.median(rat[m])))
    nb = float(np.median(rat)); nb_lo, nb_hi = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
    f4r = np.array([x["fit"] / x["pub"] for x in f4["rows"]]); b4 = np.array([np.median(f4r[rng.integers(0, len(f4r), len(f4r))]) for _ in range(2000)])
    m4, m4_lo, m4_hi = float(np.median(f4r)), float(np.percentile(b4, 2.5)), float(np.percentile(b4, 97.5))
    scale = nb * m4; sc = np.array([np.median(rat[rng.integers(0, len(rat), len(rat))]) * np.median(f4r[rng.integers(0, len(f4r), len(f4r))]) for _ in range(2000)])
    s_lo, s_hi = float(np.percentile(sc, 2.5)), float(np.percentile(sc, 97.5))
    P("  method offset on real spectra (F4, fitted / published): %.3f [%.3f, %.3f]" % (m4, m4_lo, m4_hi))
    P("  DESI-fit scale relative to the published SLACS scale = noise ratio x method offset = %.3f [%.3f, %.3f]" % (scale, s_lo, s_hi))

    # ---------------------------------------------------------------- step 2
    rowsE, _ = E.load(a.data_dir); E.OUT.clear(); Sm, _ = E.select(rowsE, ("A", "B")); byid = {r["id"]: r for r in Sm}
    L = [r for r in csv.DictReader(open(os.path.join(HERE, "euc5_a1_per_lens.csv"))) if r["unique_identifier"] in byid]
    sel = [byid[r["unique_identifier"]] for r in L]; zl = np.array([float(r["z_ref"]) for r in L]); vv = np.array([float(r["sigma_kms"]) for r in L])
    lm = E.arr(sel, "lm") + 2.0 * np.log10(E.EUCLID.DL(zl) / E.EUCLID.DL(E.arr(sel, "z")))
    eng, z, RE, Re, n, lm = E.build(sel, z=zl, lm=lm); DA = E.EUCLID.DA(zl); Ms = 10.0 ** lm * E.MSUN; tE = E.arr(sel, "tE"); isP = np.array([r["grade"] == "A" for r in sel])
    def run(sig, a0): return np.array([D.b_dyn(sig[i] * 1.0e3, Ms[i], Re[i], n[i], DA[i], a0, "S", 0.0, 0.75, 1.1) for i in range(len(sel))])
    P("\n[step 2] b_dyn of Euclid lens galaxies on the published SLACS scale (law S; SLACS itself reads +0.085)")
    RES = dict(noise_ratio=[nb, nb_lo, nb_hi], method_offset=[m4, m4_lo, m4_hi], scale=[scale, s_lo, s_hi], classes={})
    resp = 2.0 / 0.77                                             # d b / d log sigma, from EUC1's response 0.77
    sys_dex = resp * 0.5 * (math.log10(s_hi) - math.log10(s_lo))  # half-width of the scale interval, in b
    P("  scale uncertainty carried into b: +-%.3f dex" % sys_dex)
    for nm, a0 in E.FOOT.items():
        b = run(vv / scale, a0)
        for lab, m in (("P", isP), ("S", np.ones(len(sel), bool)), ("theta_E < 1.0", tE < 1.0), ("1.0 - 1.3", (tE >= 1.0) & (tE < 1.3)), ("theta_E >= 1.3", tE >= 1.3)):
            x = b[m]; bb = np.array([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(2000)])
            st = dict(N=int(m.sum()), med=float(np.median(x)), lo=float(np.percentile(bb, 2.5)), hi=float(np.percentile(bb, 97.5)))
            RES["classes"]["%s_%s" % (lab, nm)] = st
            P("  %-9s %-15s N = %2d   b_dyn = %+.3f [%+.3f, %+.3f] (statistical) +- %.3f (scale)" % (nm, lab, st["N"], st["med"], st["lo"], st["hi"], sys_dex))
    RES["sys_dex"] = sys_dex
    json.dump(RES, open(os.path.join(HERE, "euc5_a2_scale.json"), "w"), indent=1)
    P("(%.0f s)" % (time.time() - t0)); open(os.path.join(HERE, "euc5_a2_scale.out"), "w").write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
