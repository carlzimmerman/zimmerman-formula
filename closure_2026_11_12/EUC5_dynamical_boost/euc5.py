#!/usr/bin/env python3
"""EUC5 (DYNAMICAL BOOST).  Frozen criteria: FROZEN_CRITERIA.md (commit 7fa4e74869).

The stellar-mass boost b the law needs, read from SDSS/BOSS velocity dispersions of Euclid lens galaxies: spherical
Jeans, Sersic stars (catalogue n, R_e), law S / B, constant anisotropy, fibre aperture with seeing.  No source redshift.

Run:
  python3 -I euc5.py --data-dir <dir with the two ECLIPSE csv files>          (needs euc5_sdss_matches.csv)
  python3 -I euc5.py --data-dir <dir> --checks-only                          (instrument checks J1-J4 only)
  EUC5_MUTATE=newton python3 -I euc5.py --data-dir <dir>                     (must exit 1)
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
from scipy.special import gammainc, i0e

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
MUT = (os.environ.get("EUC5_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
G, MSUN, KPC, ARCSEC = E.G, E.MSUN, E.KPC, E.ARCSEC
GX, GW = np.polynomial.legendre.leggauss(64); GX = 0.5 * (GX + 1.0); GW = 0.5 * GW
XG = np.logspace(-4.0, 3.0, 600)                       # radius grid in units of R_e
RANG = np.logspace(-2.5, 1.2, 70)                      # projected radius grid, arcsec
LB = np.arange(-1.5, 1.5001, 0.1)                      # log10 boost grid
OUT = []
def P(s=""):
    print(s); OUT.append(s)

# ------------------------------------------------------------------ Jeans machinery
def nu_sigr2(r, nu, g, beta):
    """F = nu * sigma_r^2 for constant anisotropy: r^(-2 beta) int_r^inf s^(2 beta) nu g ds.  g is (nB, nr)."""
    y = r ** (2.0 * beta) * nu * g * r
    seg = 0.5 * (y[:, 1:] + y[:, :-1]) * np.diff(np.log(r))
    S = np.concatenate([np.cumsum(seg[:, ::-1], axis=1)[:, ::-1], np.zeros((y.shape[0], 1))], axis=1)
    return S * r ** (-2.0 * beta)

def project(r, f, R, beta=0.0):
    """2 int_R^inf f(r) (1 - beta R^2/r^2) r dr / sqrt(r^2 - R^2), r = R cosh u; f is (nr,) and log-interpolated."""
    U = np.arccosh(np.maximum(r[-1] / R, 1.0 + 1e-12))
    u = GX[None, :] * U[:, None]; rr = R[:, None] * np.cosh(u)
    val = np.exp(np.interp(np.log(rr).ravel(), np.log(r), np.log(np.maximum(f, 1e-300)))).reshape(rr.shape)
    return 2.0 * R * np.sum(GW[None, :] * U[:, None] * val * (1.0 - beta * (R[:, None] / rr) ** 2) * np.cosh(u), axis=1)

def ap_weight(Rang, a, fwhm):
    """fraction of the light emitted at projected radius R (arcsec) that lands in a fibre of radius a after Gaussian seeing."""
    s = fwhm / 2.3548200450309493; t = GX * a
    return np.array([np.sum(GW * a * (t / s ** 2) * np.exp(-0.5 * ((R - t) / s) ** 2) * i0e(R * t / s ** 2)) for R in Rang])

def sigma_ap(r, nu, g, beta, Rphys, W):
    """aperture dispersion (m/s) for each row of g (nB, nr)."""
    I = project(r, nu, Rphys, 0.0)
    F = nu_sigr2(r, nu, g, beta)
    wt = W * Rphys ** 2                                  # d ln R measure
    den = np.sum(I * wt)
    return np.sqrt(np.array([np.sum(project(r, F[k], Rphys, beta) * wt) for k in range(F.shape[0])]) / den)

def sersic_model(M, Re, n):
    r = XG * Re; p = 1.0 - 0.6097 / n + 0.05463 / (n * n); b = float(E.b_ser(n))
    nu = XG ** (-p) * np.exp(-b * XG ** (1.0 / n))
    gN = G * M * gammainc(n * (3.0 - p), b * XG ** (1.0 / n)) / r ** 2
    return r, nu, gN

def sig_of_B(M, Re, n, DA, a0, law, beta, a_fib, fwhm, logB=LB):
    r, nu, gN = sersic_model(M, Re, n)
    g = E.g_law((10.0 ** np.asarray(logB))[:, None] * gN[None, :], a0, law)
    return sigma_ap(r, nu, g, beta, RANG * ARCSEC * DA, ap_weight(RANG, a_fib, fwhm))

def b_dyn(sig_obs, *args, **kw):
    s = sig_of_B(*args, **kw)
    return float(np.interp(math.log(sig_obs), np.log(s), LB, left=LB[0], right=LB[-1]))

# ================================================================== main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--checks-only", action="store_true")
    a = ap.parse_args(); t0 = time.time(); tag = "euc5" + ("_MUTATE_" + MUT if MUT else "")
    P("EUC5 (DYNAMICAL BOOST)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    RES = dict(lane="EUC5", criteria_commit="7fa4e74869", mutate=MUT, footings=E.FOOT); CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    # J1 Plummer, isotropic, Newtonian
    Mp, ap_ = 1.0e11 * MSUN, 3.0 * KPC
    r = np.logspace(-4, 3.5, 900) * ap_; nu = (1.0 + (r / ap_) ** 2) ** -2.5
    g = (G * Mp * r / (r * r + ap_ * ap_) ** 1.5)[None, :]
    Rt = np.array([0.5, 2.0]) * ap_
    sp2 = project(r, nu_sigr2(r, nu, g, 0.0)[0], Rt) / project(r, nu, Rt)
    ana = (3.0 * math.pi / 64.0) * G * Mp / ap_ / np.sqrt(1.0 + (Rt / ap_) ** 2)
    e1 = float(np.max(np.abs(sp2 / ana - 1.0)))
    ck("J1", "Plummer sphere projected dispersion at 0.5a and 2a to 1%", "max error %.2e" % e1, e1 < 0.01)
    # J2 nu ~ r^-3 in a flat rotation curve, beta = 0.3
    vc = 300.0e3; r = np.logspace(-6, 6, 2400) * KPC; nu = r ** -3.0; g = (vc * vc / r)[None, :]
    Rt = np.array([1.0, 10.0]) * KPC
    sp2 = project(r, nu_sigr2(r, nu, g, 0.3)[0], Rt, 0.3) / project(r, nu, Rt)
    e2 = float(np.max(np.abs(sp2 / (vc * vc / 3.0) - 1.0)))
    ck("J2", "power-law tracer in a flat rotation curve, beta = 0.3: sigma^2 = v_c^2/3 to 1%", "max error %.2e" % e2, e2 < 0.01)
    # J3 / J4 SLACS (A85's test)
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}; SL = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"): continue
        q = l.split("\t")
        if len(q) < len(hdr): continue
        d = dict(zl=E.fl(q[col["zlens"]]), zs=E.fl(q[col["zsrc"]]), RE=E.fl(q[col["RE"]]), lME=E.fl(q[col["Mass"]]),
                 Fs=E.fl(q[col["Fs"]]), ReV=E.fl(q[col["Re(V)"]]), sig=E.fl(q[col["sigma"]]))
        if all(np.isfinite(list(d.values()))) and d["RE"] > 0 and d["sig"] > 0: SL.append(d)
    a0k = 1.132e-10
    zl = np.array([d["zl"] for d in SL]); zs = np.array([d["zs"] for d in SL]); DAs = E.AUGER.DA(zl)
    REs = np.array([d["RE"] for d in SL]) * KPC; Res = np.array([d["ReV"] for d in SL]) * ARCSEC * DAs
    Ms = np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / E.M2D_frac(REs, Res, 4.0) * MSUN
    bl = E.Engine(REs, Res, np.full(len(SL), 4.0), Ms).solve_b(math.pi * REs ** 2 * E.AUGER.sigcr(zl, zs), a0k, "S")
    ratio, dif = [], []
    for i, d in enumerate(SL):
        s = sig_of_B(Ms[i], Res[i], 4.0, DAs[i], a0k, "S", 0.0, 1.5, 1.5)
        ratio.append(float(np.exp(np.interp(bl[i], LB, np.log(s)))) / (d["sig"] * 1.0e3))
        dif.append(float(np.interp(math.log(d["sig"] * 1.0e3), np.log(s), LB)) - bl[i])
    mr = float(np.median(ratio))
    ck("J3", "SLACS, lensing-calibrated masses: median predicted/measured dispersion within 0.977 +- 0.05 (N = %d)" % len(SL),
       "%.4f (mean %.4f, scatter %.3f)" % (mr, np.mean(ratio), np.std(ratio)), abs(mr - 0.977) <= 0.05)
    P("       J4  SLACS median (b_dyn - b_lens at the true source redshift) = %+.3f dex; median b_dyn = %+.3f, median b_lens = %+.3f"
      % (np.median(dif), np.median(np.array(dif) + bl), np.median(bl)))
    CK["J4"] = dict(what="SLACS b_dyn - b_lens", value=float(np.median(dif)), ok=True)
    RES["checks"] = CK
    if a.checks_only:
        open(os.path.join(HERE, "euc5_checks.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if all(v["ok"] for v in CK.values()) else 3)

    # ---------------------------------------------------------------- data
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Sm, _ = E.select(rows, ("A", "B")); byid = {r["id"]: r for r in Sm}
    M = list(csv.DictReader(open(os.path.join(HERE, "euc5_sdss_matches.csv"))))
    P("\n[data] SDSS DR17 rows within 1 arcsec: %d on %d lenses of S" % (len(M), len({m["unique_identifier"] for m in M})))
    good = {}; ncut = dict(notprimary=0, notgalaxy=0, zwarn=0, vdisp=0, zmis=0)
    for m in M:
        k = byid.get(m["unique_identifier"])
        if k is None: continue
        v, ve, z = E.fl(m["veldisp"]), E.fl(m["veldisperr"]), E.fl(m["z"])
        if str(m["scienceprimary"]).strip() not in ("1", "1.0", "True", "true"): ncut["notprimary"] += 1; continue
        if m["class"].strip() != "GALAXY": ncut["notgalaxy"] += 1; continue
        if int(float(m["zwarning"])) != 0: ncut["zwarn"] += 1; continue
        if not (70.0 <= v <= 500.0 and ve > 0 and ve / v <= 0.25): ncut["vdisp"] += 1; continue
        if not (k["zlo"] - 0.1 <= z <= k["zhi"] + 0.1): ncut["zmis"] += 1; continue
        if m["unique_identifier"] not in good or ve / v < good[m["unique_identifier"]]["fe"]:
            good[m["unique_identifier"]] = dict(v=v, ve=ve, fe=ve / v, z=z, inst=m["instrument"].strip().upper(), snr=E.fl(m["snmedian"]))
    P("  removed: not primary %d, not GALAXY %d, zwarning %d, dispersion cuts %d, redshift outside the photo-z interval %d"
      % tuple(ncut[k] for k in ("notprimary", "notgalaxy", "zwarn", "vdisp", "zmis")))
    sel = [byid[i] for i in sorted(good)]
    P("  lenses with a qualifying dispersion: %d (grade A / sample P: %d)" % (len(sel), sum(r["grade"] == "A" for r in sel)))
    if len(sel) == 0: sys.exit("no qualifying lens")
    zl = np.array([good[r["id"]]["z"] for r in sel]); vv = np.array([good[r["id"]]["v"] for r in sel]) * 1.0e3
    afib = np.array([1.5 if good[r["id"]]["inst"] == "SDSS" else 1.0 for r in sel])
    lm = E.arr(sel, "lm") + 2.0 * np.log10(E.EUCLID.DL(zl) / E.EUCLID.DL(E.arr(sel, "z")))
    eng, z, RE, Re, n, lm = E.build(sel, z=zl, lm=lm)
    DA = E.EUCLID.DA(zl); Ms = 10.0 ** lm * MSUN; isP = np.array([r["grade"] == "A" for r in sel]); tE = E.arr(sel, "tE")
    P("  medians: z_l = %.3f, veldisp = %.0f km/s (error %.0f%%), log M* = %.2f, theta_E = %.2f\", fibre BOSS %d / SDSS %d"
      % (np.median(zl), np.median(vv) / 1e3, 100 * np.median([good[r["id"]]["fe"] for r in sel]), np.median(lm), np.median(tE),
         int(np.sum(afib == 1.0)), int(np.sum(afib == 1.5))))

    def run(a0, law, beta=0.0, fwhm=1.5):
        return np.array([b_dyn(vv[i], Ms[i], Re[i], n[i], DA[i], a0, law, beta, afib[i], fwhm) for i in range(len(sel))])
    def word(st):
        if st["N"] < 30: return "NOT EVALUABLE"
        if st["b_med_hi"] <= 0.15: return "DYNAMICAL GATE HOLDS"
        if st["b_med_lo"] >= 0.25: return "DYNAMICAL GATE FAILS"
        return "NO VERDICT"
    P("\n[primary: b_dyn, beta = 0, seeing 1.5 arcsec]")
    B, PRI = {}, {}
    for law in ("S", "B"):
        for nm, a0 in E.FOOT.items():
            b = run(a0, law); B[(law, nm)] = b
            for sname, msk in (("P", isP), ("S", np.ones(len(sel), bool))):
                st = E.stats(b[msk]); st["word"] = word(st); st["at_edge"] = int(np.sum(np.abs(b[msk]) >= 1.499)); PRI["%s_%s_%s" % (sname, law, nm)] = st
                P("  %s law %s %-9s N=%4d  b_med = %+.3f [%+.3f, %+.3f]   f(b > 0.25) = %.3f   at the grid edge %d   -> %s"
                  % (sname, law, nm, st["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"], st["f25"], st["at_edge"], st["word"] if sname == "P" else "(reading)"))
    RES["primary"] = PRI

    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc5_results.json")))["primary"]
        up = all(PRI["P_S_" + k]["b_med"] > ref["P_S_" + k]["b_med"] for k in E.FOOT)
        P("\n[MUTATE %s] b_med on P, law S: canonical %+.3f (ref %+.3f), alt %+.3f (ref %+.3f) -> %s" % (MUT, PRI["P_S_canonical"]["b_med"],
          ref["P_S_canonical"]["b_med"], PRI["P_S_alt"]["b_med"], ref["P_S_alt"]["b_med"], "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if up else 2)

    # ---------------------------------------------------------------- systematics that can change the word
    P("\n[anisotropy and seeing, law S, sample P]")
    VAR = {}; words = {nm: {PRI["P_S_" + nm]["word"]} for nm in E.FOOT}
    for lab, kw in (("beta = -0.2", dict(beta=-0.2)), ("beta = +0.2", dict(beta=0.2)), ("seeing 1.2 arcsec", dict(fwhm=1.2)), ("seeing 1.8 arcsec", dict(fwhm=1.8))):
        for nm, a0 in E.FOOT.items():
            st = E.stats(run(a0, "S", **kw)[isP]); st["word"] = word(st); VAR[lab + "_" + nm] = st; words[nm].add(st["word"])
            P("  %-18s %-9s b_med = %+.3f [%+.3f, %+.3f]   %s" % (lab, nm, st["b_med"], st["b_med_lo"], st["b_med_hi"], st["word"]))
    RES["variants"] = VAR
    final = {nm: (PRI["P_S_" + nm]["word"] if len(words[nm]) == 1 else "NO VERDICT (word not robust: %s)" % " | ".join(sorted(words[nm]))) for nm in E.FOOT}
    verdict = "%s / %s" % (final["canonical"], final["alt"]); RES["verdict"] = verdict
    P("  LANE WORD (sample P, law S, canonical / alt): %s" % verdict)

    # ---------------------------------------------------------------- reported, no word
    P("\n[reported: by Einstein radius, law S, all qualifying lenses of S]")
    BYT = {}
    for lo, hi in ((0.0, 1.0), (1.0, 1.3), (1.3, 1.7), (1.7, 99.0)):
        m = (tE >= lo) & (tE < hi)
        if m.sum() < 5: continue
        row = dict(N=int(m.sum()))
        for nm in E.FOOT:
            st = E.stats(B[("S", nm)][m]); row[nm] = st
        BYT["%.1f-%.1f" % (lo, hi)] = row
        P("  theta_E [%.1f, %4.1f)  N=%4d  b_dyn med canonical %+.3f [%+.3f, %+.3f]  alt %+.3f [%+.3f, %+.3f]"
          % (lo, hi, row["N"], row["canonical"]["b_med"], row["canonical"]["b_med_lo"], row["canonical"]["b_med_hi"],
             row["alt"]["b_med"], row["alt"]["b_med_lo"], row["alt"]["b_med_hi"]))
    RES["by_thetaE"] = BYT
    P("\n[reported: dynamics against the source-free lensing bound (same lens, same redshift, law S)]")
    DL = {}
    zgrid = np.concatenate([np.arange(0.05, 3.0, 0.05), np.arange(3.0, 10.01, 0.5), [20.0, E.ZS_INF]])
    for nm, a0 in E.FOOT.items():
        binf = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, "S"); d = B[("S", nm)] - binf
        bz = np.array([eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, np.maximum(z + dz, z + 0.05) if dz < 50 else E.ZS_INF), a0, "S") for dz in zgrid])
        zsol = np.full(len(sel), np.nan)
        for i in range(len(sel)):
            col = bz[:, i]                                   # decreasing with source redshift
            if B[("S", nm)][i] >= col[-1] and B[("S", nm)][i] <= col[0]:
                zsol[i] = z[i] + float(np.interp(-B[("S", nm)][i], -col[:-1], zgrid[:-1])) if B[("S", nm)][i] > col[-2] else np.inf
        nosol = float(np.mean(B[("S", nm)] < binf)); fin = np.isfinite(zsol)
        DL[nm] = dict(med_diff=float(np.median(d)), frac_below_m025=float(np.mean(d < -0.25)), frac_no_solution=nosol,
                      zs_med=float(np.nanmedian(np.where(np.isinf(zsol), 99.0, zsol))) if np.isfinite(zsol).any() or np.isinf(zsol).any() else float("nan"),
                      b_inf_med=float(np.median(binf)))
        for sname, msk in (("P", isP), ("S", np.ones(len(sel), bool))):
            dd = d[msk]
            P("  %s %-9s median b_dyn %+.3f, median b_inf %+.3f, median (b_dyn - b_inf) = %+.3f; fraction below -0.25: %.3f; dynamics below the lensing bound: %.3f"
              % (sname, nm, np.median(B[("S", nm)][msk]), np.median(binf[msk]), np.median(dd), np.mean(dd < -0.25), np.mean(dd < 0)))
        zz = zsol[fin]
        P("  S %-9s CONDITIONAL source redshift where lensing boost = dynamical boost: solvable %d of %d (median z_s = %.2f, 16-84%% %.2f to %.2f); no solution (dynamics below the bound) %d; beyond the grid %d"
          % (nm, int(fin.sum()), len(sel), np.median(zz) if len(zz) else float("nan"), np.percentile(zz, 16) if len(zz) else float("nan"),
             np.percentile(zz, 84) if len(zz) else float("nan"), int(np.sum(B[("S", nm)] < binf)), int(np.sum(np.isinf(zsol)))))
        DL[nm]["zs_solvable"] = int(fin.sum()); DL[nm]["zs_median"] = float(np.median(zz)) if len(zz) else float("nan")
    RES["dyn_vs_lens"] = DL

    with open(os.path.join(HERE, "euc5_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["unique_identifier", "grade", "z_spec", "veldisp_kms", "veldisperr_kms", "instrument", "theta_E_arcsec", "theta_e_arcsec", "sersic_n",
                                       "log_Mstar", "b_dyn_S_canonical", "b_dyn_S_alt", "b_dyn_B_canonical", "b_dyn_B_alt"])
        for i, r in enumerate(sel):
            gdt = good[r["id"]]
            w.writerow([r["id"], r["grade"], "%.4f" % zl[i], "%.1f" % gdt["v"], "%.1f" % gdt["ve"], gdt["inst"], "%.3f" % r["tE"], "%.3f" % r["te"], "%.2f" % n[i], "%.3f" % lm[i]]
                       + ["%.3f" % B[k][i] for k in (("S", "canonical"), ("S", "alt"), ("B", "canonical"), ("B", "alt"))])
    allok = all(CK[k]["ok"] for k in ("J1", "J2", "J3")); RES["checks_all_pass"] = allok
    P("\n[summary]")
    P("  instrument checks J1-J3: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  LANE WORD (sample P, law S, canonical / alt): %s" % (verdict if allok else "NOT EVALUABLE"))
    P("  kappa = 1/2 FITTED. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
