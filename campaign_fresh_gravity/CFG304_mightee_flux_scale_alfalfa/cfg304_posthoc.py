#!/usr/bin/env python3
"""CFG304 post hoc diagnostics -- NOT frozen.  Written after the main run (decision 'neither': ALFALFA above both
MIGHTEE flux scales) and before this script was first run.  Nothing here changes a frozen number, check or decision.
Reads only cfg304_matched_pairs.csv (main run), the MIGHTEE catalogue, the ALFALFA CSV and CFG301's committed JSON/out.

Reading rules (fixed before the first run of this script):
  PH0  reproduce the main run's C1 / ALL medians of R_cat and R_cube from the pairs CSV (to 1e-9).  check row.
       [Changed after post hoc run 1, kept as *_run1*: run 1 demanded 1e-12, but the pairs CSV is written with 10
       significant figures, so it failed at 2.6e-11 -- a flaw of the check, not of the data.  Nothing else changed.]
  PH1  R_cat by redshift: z < 0.02 (the four nearby, large galaxies) vs z >= 0.02, on C1 and ALL, all and CONF-clean.
       Words allowed: 'the deficit persists at z >= 0.02' iff |median| > 0.10 on ALL-clean z >= 0.02; else 'it shrinks
       below 0.10 dex at z >= 0.02'.
  PH2  CFG301's frozen cut (golden; 0.02 <= z <= 0.093; 45 <= incl <= 80; log M_HI >= 9.0; W50 >= 80 and
       sigma_W/W <= 0.15; SNR_3D >= 8) applied to the matched pairs: N and median R_cat (any hi_code, and C1).  If
       N >= 5, the CFG301 band interpolation (A, B) is repeated at that subset's median ('CFG301-like offset');
       if N < 5, 'too few to transfer'.
  PH3  trends: Spearman of R_cat (ALL) against the HI angular diameter theta_HI = D_HI / D_A
       (D_HI = 10^(0.506 log M_HI - 3.293) kpc, CFG260's relation; D_A = D_L/(1+z)^2), against W50_cat, SNR_3D
       (MIGHTEE-side, independent of the ALFALFA noise) and z.  Words allowed: 'the deficit grows with angular size'
       iff rho < 0 and p < 0.05; else 'not resolved by these pairs'.
  PH4  HI masses: log M_HI (MIGHTEE) - logmhi (ALFALFA) on C1 / ALL, and its residual after removing R_cat and the
       distance term 2 log10[(D_L/(1+z)) / D_ALFALFA] (should be ~0: a check through the published masses).  check row:
       |median residual| <= 0.02 dex.
  PH5  the frozen K2 failure: rows with |z_HI - (nu0/freq - 1)| > 1e-5; whether any is matched; the largest change in
       a converted flux (log10) on the matched pairs if nu_obs came from z_HI instead of freq_MHz.
  PH6  the reach of the frozen rule on these pairs: the paired cube - catalogue offset on the C1 cube set against
       CFG302's -0.30; the C1-OPT decision with the arbiter rescaled onto the catalogue median (S21 x 10^median R_cat)
       and onto the cube median (S21 x 10^median R_cube).  Reported, no verdict.
  PH7  without width-mismatched pairs (|log W50_cat/W50_ALFALFA| > 0.15, possible ALFALFA confusion invisible to CONF):
       C1 and ALL medians of R_cat.
"""
import importlib.util
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cfg304", os.path.join(HERE, "cfg304_flux_scale_alfalfa.py"))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

LINES, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); LINES.append(s); print(s, flush=True)


def check(name, detail, ok):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok))); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def med(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return (float(np.median(x)) if x.size else np.nan), int(x.size)


def main():
    df = pd.read_csv(os.path.join(HERE, "cfg304_matched_pairs.csv"))
    J = json.load(open(os.path.join(HERE, "cfg304_flux_scale_alfalfa_results.json")))["numbers"]["results"]
    cat = pd.read_csv(M.CAT)
    alf = pd.read_csv(M.ALF, dtype={"sdss_objid": "string", "name_oc": "string"})
    df = df.merge(cat[["ID_catalogue", "incl_deg", "W_50_km_s_err", "D_L_Mpc", "low_confidence_flag", "bad_ellipse_flag",
                       "contaminated_source_flag"]], left_on="ID", right_on="ID_catalogue", how="left")
    df = df.merge(alf[["agc", "dist_mpc", "logmhi"]], on="agc", how="left")
    c1, allc, clean = df.hi_code == 1, df.hi_code.isin([1, 2]), df.CONF == 0
    out = {}
    P("CFG304 post hoc diagnostics (NOT frozen; reading rules in the docstring, fixed before the first run)")

    P("\nPH0 reproduction of the main run")
    dev = max(abs(med(df.loc[c1, "R_cat_OPT"])[0] - J["cat"]["C1"]["OPT"]["median"]), abs(med(df.loc[allc, "R_cat_OPT"])[0] - J["cat"]["ALL"]["OPT"]["median"]),
              abs(med(df.loc[c1 & (df.cube_set == 1), "R_cube_OPT"])[0] - J["cube"]["C1"]["OPT"]["median"]))
    check("PH0 C1/ALL R_cat and C1 R_cube medians reproduced from the pairs CSV (to 1e-9; the CSV has 10 significant figures)", f"max deviation {dev:.1e}", dev <= 1e-9)

    P("\nPH1 R_cat (OPT) by redshift")
    lowz = df.z_HI < 0.02
    ph1 = {}
    for nm, m in (("C1", c1), ("ALL", allc), ("C1_clean", c1 & clean), ("ALL_clean", allc & clean)):
        a, na = med(df.loc[m & lowz, "R_cat_OPT"]); b, nb = med(df.loc[m & ~lowz, "R_cat_OPT"])
        ph1[nm] = dict(z_lt_002=[a, na], z_ge_002=[b, nb])
        P(f"  {nm:10s} z < 0.02: {a:+.3f} (N {na});  z >= 0.02: {b:+.3f} (N {nb})")
    w = ph1["ALL_clean"]["z_ge_002"][0]
    ph1["reading"] = "the deficit persists at z >= 0.02" if abs(w) > 0.10 else "it shrinks below 0.10 dex at z >= 0.02"
    P(f"  reading (ALL-clean, z >= 0.02): {ph1['reading']} ({w:+.3f})")
    out["PH1"] = ph1

    P("\nPH2 CFG301's frozen cut applied to the matched pairs")
    cut = ((df.golden == 1) & df.z_HI.between(0.02, 0.093) & df.incl_deg.between(45, 80) & (df.log_M_HI >= 9.0)
           & (df.W50_cat >= 80) & (df.W_50_km_s_err / df.W50_cat <= 0.15) & (df.SNR_3D >= 8))
    ph2 = {}
    for nm, m in (("any_code", cut & allc), ("C1", cut & c1)):
        r, n = med(df.loc[m, "R_cat_OPT"]); rk, nk = med(df.loc[m & (df.cube_set == 1), "R_cube_OPT"])
        ph2[nm] = dict(N=n, R_cat=r, IDs=df.loc[m, "ID"].tolist(), R_cube=rk, N_cube=nk)
        P(f"  {nm:9s} N {n}: median R_cat {r:+.3f}; cube detections among them N {nk}, median R_cube {rk:+.3f}; IDs {df.loc[m, 'ID'].tolist()}")
    r0, n0 = ph2["any_code"]["R_cat"], ph2["any_code"]["N"]
    if n0 >= 5:
        x = df.loc[cut & allc, "R_cat_OPT"].values
        b = M.boot(x, np.random.SeedSequence(3042))
        cons = M.cfg301_consequence(r0, b)
        ph2["consequence"] = dict(boot68=[b["p16"], b["p84"]], A=cons["A"], B=cons["B"])
        P(f"  CFG301-like offset (any code, N {n0}): R_cat {r0:+.3f} (68 % {b['p16']:+.3f}..{b['p84']:+.3f}) -> (A) {M.fmt_a(cons['A']['central'])} "
          f"[68 % {M.fmt_a(cons['A']['lo'])} .. {M.fmt_a(cons['A']['hi'])}]; (B) {M.fmt_a(cons['B']['central'])} [68 % {M.fmt_a(cons['B']['lo'])} .. {M.fmt_a(cons['B']['hi'])}]")
    else:
        ph2["consequence"] = "too few to transfer"
        P("  too few to transfer")
    out["PH2"] = ph2

    P("\nPH3 trends of R_cat (OPT, ALL)")
    DA = df.D_L_Mpc / (1 + df.z_HI) ** 2
    df["theta_HI_arcsec"] = 10 ** (0.506 * df.log_M_HI - 3.293) / (DA * 1e3) * 206265.0
    ph3 = {}
    m = allc & np.isfinite(df.R_cat_OPT)
    for nm, col in (("theta_HI", "theta_HI_arcsec"), ("W50_cat", "W50_cat"), ("SNR_3D", "SNR_3D"), ("z", "z_HI")):
        r = spearmanr(df.loc[m, col], df.loc[m, "R_cat_OPT"]); ph3[nm] = [float(r[0]), float(r[1])]
        P(f"  R_cat vs {nm:9s}: rho {r[0]:+.2f} (p {r[1]:.2g}), N {int(m.sum())}")
    P(f"  theta_HI range {df.loc[m, 'theta_HI_arcsec'].min():.0f}-{df.loc[m, 'theta_HI_arcsec'].max():.0f} arcsec (catalogue beam ~15.5 arcsec; ALFALFA ~210 arcsec)")
    ph3["reading"] = "the deficit grows with angular size" if (ph3["theta_HI"][0] < 0 and ph3["theta_HI"][1] < 0.05) else "not resolved by these pairs"
    P(f"  reading: {ph3['reading']}")
    out["PH3"] = ph3

    P("\nPH4 HI masses through the published values")
    dlm = df.log_M_HI - df.logmhi
    dist = 2 * np.log10((df.D_L_Mpc / (1 + df.z_HI)) / df.dist_mpc)
    resid = dlm - df.R_cat_OPT - dist
    ph4 = {}
    for nm, mm in (("C1", c1), ("ALL", allc)):
        ph4[nm] = dict(dlogM=med(dlm[mm]), dist_term=med(dist[mm]), residual=med(resid[mm]))
        P(f"  {nm:4s} median log M_HI(MIGHTEE) - logmhi(ALFALFA) {ph4[nm]['dlogM'][0]:+.3f} (N {ph4[nm]['dlogM'][1]}); distance term {ph4[nm]['dist_term'][0]:+.3f}; "
          f"residual after R_cat and distance {ph4[nm]['residual'][0]:+.4f}")
    check("PH4 |median residual| <= 0.02 dex on ALL (published masses agree with the flux comparison)", f"{ph4['ALL']['residual'][0]:+.4f}", abs(ph4["ALL"]["residual"][0]) <= 0.02)
    out["PH4"] = ph4

    P("\nPH5 the frozen K2 failure (catalogue z_HI vs freq_MHz)")
    dz = cat.z_HI - (M.NU0_HZ / (cat.freq_MHz * 1e6) - 1)
    bad = cat.loc[np.abs(dz) > 1e-5, ["ID_catalogue", "z_HI", "freq_MHz"]].assign(dz=dz[np.abs(dz) > 1e-5])
    matched_bad = sorted(set(bad.ID_catalogue) & set(df.ID))
    nu_from_z = M.NU0_HZ / (1 + df.z_HI)
    dS = np.abs(2 * np.log10(df.freq_MHz * 1e6 / nu_from_z))
    P(f"  rows with |dz| > 1e-5: {len(bad)} of {len(cat)}; |dz| median among them {np.median(np.abs(bad.dz)) if len(bad) else 0:.2e}, max {np.max(np.abs(bad.dz)) if len(bad) else 0:.2e}")
    P(f"  matched pairs among them: {len(matched_bad)} {matched_bad}; largest |delta log10 S_V,OPT| on the pairs if nu came from z_HI: {dS.max():.1e} dex")
    P(f"  the five largest: {[(a, round(b, 5), round(c, 3), f'{d:+.1e}') for a, b, c, d in bad.reindex(bad.dz.abs().sort_values(ascending=False).index).head(5).itertuples(index=False)]}")
    out["PH5"] = dict(n_bad=int(len(bad)), max_abs_dz=float(np.max(np.abs(bad.dz))) if len(bad) else 0.0, matched=matched_bad, max_dlogS_pairs=float(dS.max()))

    P("\nPH6 the reach of the frozen rule on these pairs")
    cs = c1 & (df.cube_set == 1)
    pdiff, npd = med(df.loc[cs, "R_cube_OPT"] - df.loc[cs, "R_cat_OPT"])
    rc, nc = med(df.loc[c1, "R_cat_OPT"]); rk, nk = med(df.loc[cs, "R_cube_OPT"])
    d_on_cat = M.decide(rc - rc, rk - rc, nc, nk); d_on_cube = M.decide(rc - rk, rk - rk, nc, nk)
    P(f"  paired R_cube - R_cat on the C1 cube set: {pdiff:+.3f} (N {npd}); CFG302 over its 58 detections: -0.30")
    P(f"  arbiter moved onto the catalogue median: R_cat {0:+.3f}, R_cube {rk - rc:+.3f} -> '{d_on_cat}'")
    P(f"  arbiter moved onto the cube median:      R_cat {rc - rk:+.3f}, R_cube {0:+.3f} -> '{d_on_cube}'")
    out["PH6"] = dict(paired_diff=[pdiff, npd], arbiter_on_catalogue=d_on_cat, arbiter_on_cube=d_on_cube)

    P("\nPH7 without width-mismatched pairs (|log W50_cat/W50_ALFALFA| > 0.15)")
    wm = np.abs(df.logW50_cat_A) > 0.15
    P(f"  width-mismatched: {df.loc[wm, 'ID'].tolist()} (W50 cat/ALFALFA {list(zip(df.loc[wm, 'W50_cat'], df.loc[wm, 'w50_A']))})")
    ph7 = {}
    for nm, mm in (("C1", c1), ("ALL", allc)):
        ph7[nm] = med(df.loc[mm & ~wm, "R_cat_OPT"])
        P(f"  {nm:4s} median R_cat without them {ph7[nm][0]:+.3f} (N {ph7[nm][1]})")
    out["PH7"] = dict(mismatched=df.loc[wm, "ID"].tolist(), **ph7)

    npass = sum(c["ok"] for c in CHECKS)
    P(f"\n{npass}/{len(CHECKS)} checks pass")
    json.dump(dict(stage="CFG304_posthoc", checks=CHECKS, numbers=out), open(os.path.join(HERE, "cfg304_posthoc_results.json"), "w"), indent=1, default=float)
    with open(os.path.join(HERE, "cfg304_posthoc.out"), "w") as f:
        f.write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
