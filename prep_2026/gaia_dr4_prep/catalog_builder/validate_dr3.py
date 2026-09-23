#!/usr/bin/env python3
"""Step 3 (DR3 only): validate the catalog chain against El-Badry+2021.

Compares the builder's DR3 output with the published El-Badry, Rix & Heintz
(2021) eDR3 catalog (Zenodo 4435257, local copy) inside the builder's volume:

  V1  recovery: of El-Badry pairs in-volume with R < 0.1 and s < 30 kAU,
      the fraction the builder also finds after cleaning (stage D);
  V2  purity: of builder pairs with R < 0.1 and s < 30 kAU, the fraction in
      El-Badry's catalog (DR3 vs eDR3 astrometry differ slightly; the two
      releases share the same 34-month data, so disagreement should be small);
  V3  R agreement on matched pairs: Spearman rank correlation of log R and
      the agreement of the frozen R < 0.01 classification;
  V4  the frozen-cut sample written by the builder is fed to the pipeline
      (`--catalog`), and separately El-Badry's matched pairs are put through
      the SAME frozen cuts with El-Badry's own R, so the two gamma_hat values
      differ only by the chance-alignment statistic.

Everything here is DR3-era, contaminated by construction (no DR4 NSS/epoch
screen) and NON-SCORING.  It tests the machinery, not gravity.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EXT = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract"
ELB = REPO / "real_research" / "data" / "widebinaries" / "all_columns_catalog.fits.gz"


def load_elbadry():
    from astropy.io import fits
    with fits.open(ELB, memmap=True) as h:
        d = h[1].data
        out = {c: np.array(d[c]) for c in ["source_id1", "source_id2", "R_chance_align", "sep_AU",
                                           "parallax1", "parallax2", "ra1", "dec1"]}
    return out


def pair_keys(x, y):
    x, y = np.asarray(x, np.int64), np.asarray(y, np.int64)
    lo, hi = np.minimum(x, y), np.maximum(x, y)
    return np.array([f"{p}_{q}" for p, q in zip(lo, hi)])


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("elbadry", "scaled_clean"), default="elbadry")
    ap.add_argument("--skip-v4", action="store_true")
    args = ap.parse_args()
    sfx = "" if args.mode == "elbadry" else f"_{args.mode}"
    sys.path.insert(0, str(HERE))
    from build_catalog import galactic
    S = dict(np.load(EXT / "stage_A.npz"))
    D = dict(np.load(EXT / "stage_D.npz"))
    F = dict(np.load(EXT / f"stage_F{sfx}.npz"))
    E = load_elbadry()
    rep = {}

    # in-volume El-Badry pairs (same volume definition as the builder's extract)
    _, bE = galactic(E["ra1"], E["dec1"])
    inE = (E["parallax1"] > 3.5) & (E["parallax2"] > 3.5) & (np.abs(bE) > 10)
    kE = pair_keys(E["source_id1"], E["source_id2"])
    R_E = dict(zip(kE[inE], E["R_chance_align"][inE]))
    s_E = dict(zip(kE[inE], E["sep_AU"][inE]))

    kD = pair_keys(S["source_id"][D["a"]], S["source_id"][D["b"]])
    kF = pair_keys(S["source_id"][F["a"]], S["source_id"][F["b"]])
    R_F = dict(zip(kF, F["R"]))
    sep_F = dict(zip(kF, 1000 / S["parallax"][F["a"]] * F["th"]))
    setD = set(kD.tolist())

    # V1 recovery
    good_E = [k for k in R_E if R_E[k] < 0.1 and s_E[k] < 30000]
    rec = np.mean([k in setD for k in good_E]) if good_E else float("nan")
    rep["V1_recovery"] = {"elbadry_pairs_R<0.1_s<30kAU_in_volume": len(good_E),
                          "fraction_found_by_builder": float(rec)}
    # V2 purity
    good_F = [k for k in R_F if R_F[k] < 0.1 and sep_F[k] < 30000]
    setE = set(R_E)
    pur = np.mean([k in setE for k in good_F]) if good_F else float("nan")
    rep["V2_purity"] = {"builder_pairs_R<0.1_s<30kAU": len(good_F),
                        "fraction_in_elbadry": float(pur)}
    # V3 R agreement
    common = [k for k in R_F if k in R_E and sep_F[k] < 30000]
    if common:
        from scipy.stats import spearmanr
        rf = np.array([R_F[k] for k in common])
        re = np.array([R_E[k] for k in common])
        fl = np.log10(np.clip(rf, 1e-30, None))
        el = np.log10(np.clip(re, 1e-30, None))
        rho = spearmanr(fl, el).correlation
        agree = np.mean((rf < 0.01) == (re < 0.01))
        both = np.mean((rf < 0.01) & (re < 0.01))
        only_f = np.mean((rf < 0.01) & ~(re < 0.01))
        only_e = np.mean(~(rf < 0.01) & (re < 0.01))
        rep["V3_R_agreement"] = {"matched_pairs_s<30kAU": len(common), "spearman_logR": float(rho),
                                 "R<0.01_classification_agreement": float(agree),
                                 "both_pass": float(both), "builder_only": float(only_f),
                                 "elbadry_only": float(only_e)}
    # V4 gamma_hat: builder sample vs El-Badry's pairs through the SAME frozen cuts
    rep["chance_mode"] = args.mode
    if not args.skip_v4:
        rep["V4_gamma"] = v4_gamma(S, E, inE, EXT / f"wide_binaries_dr3{sfx}.csv")
    (HERE / f"validation_dr3{sfx}.json").write_text(json.dumps(rep, indent=2) + "\n")
    print(json.dumps(rep, indent=2))


def v4_gamma(S, E, inE, builder_csv):
    """Both samples fitted with the pipeline's own estimator against a
    DR3-NOISE forward model (as its --dry-run does; its --catalog path models
    DR4 noise, which would be wrong for DR3 data).  NON-SCORING."""
    import csv
    sys.path.insert(0, str(HERE.parent))
    import wide_binary_pipeline as wbp
    from build_catalog import (frozen_cuts, third_star_flags, fetch_correlations, vt_error_mc,
                               ang_sep_arcsec, av_sfd98)
    out = {}
    # (a) El-Badry pairs in-volume whose stars are both in the extract, with El-Badry's own R
    pos = {int(x): i for i, x in enumerate(S["source_id"])}
    i1 = np.array([pos.get(int(x), -1) for x in E["source_id1"][inE]])
    i2 = np.array([pos.get(int(x), -1) for x in E["source_id2"][inE]])
    ok = (i1 >= 0) & (i2 >= 0)
    a, b, R = i1[ok], i2[ok], E["R_chance_align"][inE][ok]
    sw = S["phot_g_mean_mag"][a] > S["phot_g_mean_mag"][b]
    a, b = np.where(sw, b, a), np.where(sw, a, b)
    th = ang_sep_arcsec(S["ra"][a], S["dec"][a], S["ra"][b], S["dec"][b])
    extra = {"third": np.zeros(len(a), bool)}
    pre, _, _ = frozen_cuts(S, a, b, R, extra)
    idx = np.flatnonzero(pre)
    extra["third"][idx] = third_star_flags(S, a[idx], b[idx])
    pre2, _, tab0 = frozen_cuts(S, a, b, R, extra)
    idx2 = np.flatnonzero(pre2)
    corr = fetch_correlations("dr3", np.concatenate([S["source_id"][a[idx2]], S["source_id"][b[idx2]]]),
                              EXT / "stage_G_corr_elbadry.npz")
    sig = vt_error_mc(S, a[idx2], b[idx2], th[idx2], corr)
    vc0 = np.sqrt(wbp.G * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * wbp.MSUN
                  / (tab0["sep_kAU"][idx2] * 1e3 * wbp.AU)) / 1e3
    vt0 = tab0["v_perp_kms"][idx2] / vc0
    okv = np.zeros(len(a), bool)
    okv[idx2] = sig <= 0.1 * np.maximum(1.0, vt0 / 2)
    extra["vt_err_ok"] = okv
    z = av_sfd98(S, EXT / "AV_sfd98.npz")
    extra["AV_ok"] = (z["av"][a] < 0.5) & (z["av"][b] < 0.5)
    keep, flow, table = frozen_cuts(S, a, b, R, extra)
    csv_e = EXT / "wide_binaries_dr3_elbadryR.csv"
    cols = list(table)
    with open(csv_e, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for i in np.flatnonzero(keep):
            w.writerow([table[c][i] for c in cols])
    out["elbadry_R_cut_flow"] = flow
    # (b) fits against the DR3-noise forward model, both footings
    rng = np.random.default_rng(20261216)
    pop = wbp.make_population(3_000_000, rng, dr4=False)
    mods = {"canonical": (wbp.A0_CAN, wbp.model_medians(pop, wbp.A0_CAN, wbp.GRID, rng)),
            "alt": (wbp.A0_ALT, wbp.model_medians(pop, wbp.A0_ALT, wbp.GRID, rng))}
    for name, path in (("builder_R", builder_csv), ("elbadry_R", csv_e)):
        gN, vt, _ = wbp.ingest_csv(str(path))
        out[name] = {"N": int(len(vt))}
        for foot, (a0v, mod) in mods.items():
            g, sg, *_ = wbp.run_fit(np.log10(gN / a0v), vt, mod, rng, f"{name} [{foot}]")
            out[name][foot] = {"gamma_hat": float(g), "sigma_fit": float(sg)}
    return out


if __name__ == "__main__":
    main()
