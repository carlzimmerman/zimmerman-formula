#!/usr/bin/env python3
"""EUC5 AMENDMENT A1, step 2: the dynamical boost from the DESI-fitted dispersions (AMENDMENT_A1.md, commit 286752fa9c).

Reads euc5_a1_dispersions.csv and euc5_a1_fit.json (step 1).  EUC5's Jeans model; DESI fibre 0.75 arcsec, seeing 1.1.
If validation F1 or F2 failed, the word is NOT EVALUABLE and everything printed is a reading, shown raw and with the
first-order correction for the recovery bias F1 measured.

Run:  python3 -I euc5_a1.py --data-dir <dir with the two ECLIPSE csv files>
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc5 as D
E = D.E
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args(); t0 = time.time()
    P("EUC5 under AMENDMENT A1 (DESI-fitted dispersions)")
    fj = json.load(open(os.path.join(HERE, "euc5_a1_fit.json")))
    f1 = {float(k): v["median"] / float(k) for k, v in fj["F1"].items()}
    P("\n[validation] F1 recovery ratios at 150 / 250 / 350 km/s: %.3f / %.3f / %.3f -> %s"
      % (f1[150.0], f1[250.0], f1[350.0], "PASS" if fj["F1_pass"] else "FAIL (gate: within 5% at all three)"))
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Sm, _ = E.select(rows, ("A", "B")); byid = {r["id"]: r for r in Sm}
    best = {}
    for r in csv.DictReader(open(os.path.join(HERE, "euc5_a1_dispersions.csv"))):
        s, e, V, npx = float(r["sigma"]), float(r["err"]), float(r["V"]), int(r["npix"])
        if not (np.isfinite(s) and 70 <= s <= 500 and e > 0 and e / s <= 0.25 and abs(V) <= 300 and npx >= 800): continue
        prim = r["primary"] in ("True", "true", "1"); k = r["unique_identifier"]
        cand = dict(s=s, e=e, z=float(r["z_ref"]), prim=prim, snr=float(r["snr"]))
        if k not in best or (prim and not best[k]["prim"]) or (prim == best[k]["prim"] and e / s < best[k]["e"] / best[k]["s"]): best[k] = cand
    sel = [byid[i] for i in sorted(best) if i in byid]
    isP = np.array([r["grade"] == "A" for r in sel]); P("  lenses of S with a qualifying DESI dispersion: %d (sample P: %d)" % (len(sel), int(isP.sum())))
    # F2 against SDSS
    sd = {r["unique_identifier"]: float(r["veldisp_kms"]) for r in csv.DictReader(open(os.path.join(HERE, "euc5_per_lens.csv")))}
    both = [(best[i]["s"], sd[i]) for i in best if i in sd]
    okF2 = True
    if both:
        rat = [x / y for x, y in both]; P("  F2 lenses with both a DESI fit and an SDSS dispersion: %d; DESI/SDSS ratios: %s" % (len(both), ", ".join("%.2f" % x for x in rat)))
        if len(both) >= 5: okF2 = 0.85 <= float(np.median(rat)) <= 1.15
    else: P("  F2 no lens has both a DESI fit and an SDSS dispersion")
    evaluable = fj["F1_pass"] and okF2 and int(isP.sum()) >= 30

    zl = np.array([best[r["id"]]["z"] for r in sel]); vv = np.array([best[r["id"]]["s"] for r in sel])
    corr = np.interp(vv, [150.0, 250.0, 350.0], [f1[150.0], f1[250.0], f1[350.0]])        # first-order bias correction from F1
    lm = E.arr(sel, "lm") + 2.0 * np.log10(E.EUCLID.DL(zl) / E.EUCLID.DL(E.arr(sel, "z")))
    eng, z, RE, Re, n, lm = E.build(sel, z=zl, lm=lm); DA = E.EUCLID.DA(zl); Ms = 10.0 ** lm * E.MSUN; tE = E.arr(sel, "tE")
    P("  medians: z_l = %.3f, sigma = %.0f km/s (error %.0f%%), log M* = %.2f, theta_E = %.2f\"" % (np.median(zl), np.median(vv), 100 * np.median([best[r["id"]]["e"] / best[r["id"]]["s"] for r in sel]), np.median(lm), np.median(tE)))
    def run(sig, a0, law="S", beta=0.0, fwhm=1.1):
        return np.array([D.b_dyn(sig[i] * 1.0e3, Ms[i], Re[i], n[i], DA[i], a0, law, beta, 0.75, fwhm) for i in range(len(sel))])
    RES = dict(F1=f1, F1_pass=fj["F1_pass"], F2=both, N_S=len(sel), N_P=int(isP.sum()), evaluable=bool(evaluable)); B = {}
    P("\n[b_dyn, beta = 0, fibre 0.75 arcsec, seeing 1.1 arcsec]   raw  |  corrected for the F1 recovery bias")
    for law in ("S", "B"):
        for nm, a0 in E.FOOT.items():
            br = run(vv, a0, law); bc = run(vv / corr, a0, law); B[(law, nm)] = (br, bc)
            for sname, msk in (("P", isP), ("S", np.ones(len(sel), bool))):
                sr, sc = E.stats(br[msk]), E.stats(bc[msk]); RES["%s_%s_%s" % (sname, law, nm)] = dict(raw=sr, corrected=sc)
                P("  %s law %s %-9s N=%3d  raw %+.3f [%+.3f, %+.3f]  |  corrected %+.3f [%+.3f, %+.3f]"
                  % (sname, law, nm, sr["N"], sr["b_med"], sr["b_med_lo"], sr["b_med_hi"], sc["b_med"], sc["b_med_lo"], sc["b_med_hi"]))
    P("\n[anisotropy and seeing, law S, sample S, raw]")
    for lab, kw in (("beta = -0.2", dict(beta=-0.2)), ("beta = +0.2", dict(beta=0.2)), ("seeing 0.9 arcsec", dict(fwhm=0.9)), ("seeing 1.3 arcsec", dict(fwhm=1.3))):
        P("  %-18s canonical %+.3f   alt %+.3f" % (lab, np.median(run(vv, E.FOOT["canonical"], **kw)), np.median(run(vv, E.FOOT["alt"], **kw))))
    P("\n[by Einstein radius, law S, sample S]   N, b_dyn raw / corrected (alt), source-free lensing bound b_inf (alt)")
    binf = {nm: eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, "S") for nm, a0 in E.FOOT.items()}
    BYT = {}
    for lo, hi in ((0.0, 1.0), (1.0, 1.3), (1.3, 1.7), (1.7, 99.0)):
        m = (tE >= lo) & (tE < hi)
        if m.sum() < 5: continue
        BYT["%.1f-%.1f" % (lo, hi)] = dict(N=int(m.sum()), raw=float(np.median(B[("S", "alt")][0][m])), corr=float(np.median(B[("S", "alt")][1][m])), binf=float(np.median(binf["alt"][m])))
        P("  theta_E [%.1f, %4.1f)  N=%3d   %+.3f / %+.3f    b_inf %+.3f" % (lo, hi, int(m.sum()), np.median(B[("S", "alt")][0][m]), np.median(B[("S", "alt")][1][m]), np.median(binf["alt"][m])))
    RES["by_thetaE"] = BYT
    P("\n[dynamics against the source-free lensing bound, law S, sample S]")
    rng = np.random.default_rng(E.SEED)
    for nm in E.FOOT:
        for lab, k in (("raw", 0), ("corrected", 1)):
            d = B[("S", nm)][k] - binf[nm]
            bs = np.array([np.median(d[rng.integers(0, len(d), len(d))]) for _ in range(2000)])
            RES["dyn_minus_binf_%s_%s" % (nm, lab)] = dict(med=float(np.median(d)), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), below=float(np.mean(d < 0)))
            P("  %-9s %-9s median (b_dyn - b_inf) = %+.3f [%+.3f, %+.3f]; lenses with dynamics below the lensing bound: %d of %d"
              % (nm, lab, np.median(d), np.percentile(bs, 2.5), np.percentile(bs, 97.5), int(np.sum(d < 0)), len(d)))
    with open(os.path.join(HERE, "euc5_a1_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["unique_identifier", "grade", "z_ref", "sigma_kms", "err_kms", "snr", "theta_E_arcsec", "log_Mstar", "b_dyn_raw_S_canonical", "b_dyn_raw_S_alt", "b_dyn_corr_S_alt", "b_inf_S_alt"])
        for i, r in enumerate(sel):
            w.writerow([r["id"], r["grade"], "%.4f" % zl[i], "%.1f" % vv[i], "%.1f" % best[r["id"]]["e"], "%.1f" % best[r["id"]]["snr"], "%.3f" % r["tE"], "%.3f" % lm[i],
                        "%.3f" % B[("S", "canonical")][0][i], "%.3f" % B[("S", "alt")][0][i], "%.3f" % B[("S", "alt")][1][i], "%.3f" % binf["alt"][i]])
    P("\n[summary]")
    P("  word under A1: %s" % ("gate applies" if evaluable else "NOT EVALUABLE (F1 %s, F2 %s, N(P) = %d)" % ("pass" if fj["F1_pass"] else "FAIL", "pass" if okF2 else "FAIL", int(isP.sum()))))
    P("  kappa = 1/2 FITTED. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, "euc5_a1_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "euc5_a1.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
