#!/usr/bin/env python3
"""
stage1_catalog.py -- MaNGA DR17 Stage-1 catalog for the MG-impossible anisotropy
discriminator (d(offset)/d(radial-anisotropy) > 0; MG-with-same-nu predicts exactly 0).

STAGING ONLY. Applies the PRE-FROZEN selection (FROZEN.md, frozen 2026-07-17T00:21:52Z,
BEFORE data download) to DAPall x drpall, computes the per-galaxy RAR/mass-plane offset
delta on the framework's OWN law nu(y)=sqrt(1+1/y) at BOTH a0 footings and all frozen
IMF brackets, and writes stage_catalog.csv. The delta-vs-proxy REGRESSION IS NOT RUN
HERE (freeze-then-fire separation; exploratory firewall, FROZEN.md sec.5).

Framework: de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman), judged on its own terms.
a0_canon = 9.36e-11 m/s^2 (cH_Lambda/Z, rho_DE); a0_alt = 1.13e-10 m/s^2 (cH0, rho_tot).

exit 0 on completion; no hard-coded verdicts; all numbers computed from the data.
"""
import os, sys, math, json
import numpy as np
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DAPTYPE = "HYB10-MILESHC-MASTARSSP"

# frozen constants (FROZEN.md)
A0_CANON = 9.36e-11    # m/s^2  cH_Lambda/Z, rho_DE  (canonical)
A0_ALT   = 1.13e-10    # m/s^2  cH0, rho_tot         (alt footing)
KV       = 5.0         # virial coefficient, Cappellari et al. 2006
H0, OM, LITTLE_H = 70.0, 0.3, 0.7
G_SI     = 6.674e-11
MSUN     = 1.98892e30
KPC_M    = 3.0856775814913673e19
SIG_FLOOR = 70.0       # km/s instrumental floor guard
SNR_MIN   = 10.0
VSIG_PRIMARY, VSIG_VARIANT = 0.4, 0.6
IMF_A_FACTOR = 1.55            # Salpeter-like common-mode bracket
IMF_B_SLOPE, IMF_B_PIVOT = 0.30, 130.0  # dlogM* = 0.30*log10(sig_e/130)

COSMO = FlatLambdaCDM(H0=H0, Om0=OM)


def nu(y):
    """The framework's OWN interpolation (never McGaugh's)."""
    return np.sqrt(1.0 + 1.0 / y)


def delta_offset(m_dyn, m_bar, re_kpc, a0):
    """delta = log10(M_dyn) - log10(nu(y) M_bar), y = g_bar/a0,
    g_bar = G (M_bar/2)/Re^2 (frozen estimator)."""
    g_bar = G_SI * (m_bar * MSUN / 2.0) / (re_kpc * KPC_M) ** 2
    y = g_bar / a0
    return np.log10(m_dyn) - np.log10(nu(y) * m_bar), g_bar, y


def main():
    dap_path = os.path.join(DATA, "dapall-v3_1_1-3.1.0.fits")
    drp_path = os.path.join(DATA, "drpall-v3_1_1.fits")

    # ---- load + validate row counts -------------------------------------
    with fits.open(dap_path) as h:
        names = [x.name for x in h]
        if DAPTYPE not in names:
            print(f"FATAL: HDU {DAPTYPE} not in DAPall (have {names})"); return 1
        dap = h[DAPTYPE].data
    with fits.open(drp_path) as h:
        drp = h["MANGA"].data if "MANGA" in [x.name for x in h] else h[1].data

    n_dap, n_drp = len(dap), len(drp)
    print(f"DAPall[{DAPTYPE}] rows: {n_dap}   drpall rows: {n_drp}")
    if not (9000 < n_dap < 13000) or not (9000 < n_drp < 13000):
        print("FATAL: row counts grossly off the expected ~10-11k"); return 1

    # ---- crossmatch on PLATEIFU -----------------------------------------
    drp_idx = {p.strip(): i for i, p in enumerate(drp["plateifu"])}
    rows = []
    stats = dict(matched=0, dapdone=0, qual=0, targ=0, nsa=0, snr=0, sig=0)
    for i in range(n_dap):
        pifu = dap["PLATEIFU"][i].strip()
        j = drp_idx.get(pifu)
        if j is None:
            continue
        stats["matched"] += 1
        if not bool(dap["DAPDONE"][i]):
            continue
        stats["dapdone"] += 1
        if int(dap["DAPQUAL"][i]) != 0:
            continue
        stats["qual"] += 1
        if int(drp["mngtarg1"][j]) <= 0:
            continue
        stats["targ"] += 1
        mstar_h2 = float(drp["nsa_elpetro_mass"][j])
        th50 = float(drp["nsa_elpetro_th50_r"][j])
        z = float(drp["nsa_z"][j])
        if not (mstar_h2 > 0 and th50 > 0 and 0.005 < z < 0.15):
            continue
        stats["nsa"] += 1
        snr = float(dap["SNR_MED"][i][0])  # g-band element of the griz 4-vector (FROZEN.md)
        if not (np.isfinite(snr) and snr >= SNR_MIN):
            continue
        stats["snr"] += 1
        sig_e = float(dap["STELLAR_SIGMA_1RE"][i])
        if not (np.isfinite(sig_e) and sig_e >= SIG_FLOOR):
            continue
        stats["sig"] += 1

        vhi = float(dap["STELLAR_VEL_HI_CLIP"][i])
        vlo = float(dap["STELLAR_VEL_LO_CLIP"][i])
        if not (np.isfinite(vhi) and np.isfinite(vlo)):
            continue
        vsig = 0.5 * (vhi - vlo) / sig_e

        rows.append(dict(
            plateifu=pifu, mangaid=str(drp["mangaid"][j]).strip(),
            plate=int(dap["PLATE"][i]), ifudsgn=str(drp["ifudsgn"][j]).strip(),
            objra=float(drp["objra"][j]), objdec=float(drp["objdec"][j]),
            z=z, snr_med=snr, sb_1re=float(dap["SB_1RE"][i]),
            sigma_e=sig_e, vsig_glob=vsig,
            mstar_h2=mstar_h2, th50_arcsec=th50,
            ba=float(drp["nsa_elpetro_ba"][j]), sersic_n=float(drp["nsa_sersic_n"][j]),
        ))

    print("cut cascade:", json.dumps(stats))

    # ---- dedupe on MANGAID (keep highest SNR_MED) ------------------------
    best = {}
    for r in rows:
        k = r["mangaid"]
        if k not in best or r["snr_med"] > best[k]["snr_med"]:
            best[k] = r
    rows = list(best.values())
    print(f"after MANGAID dedupe: {len(rows)} unique galaxies (quality-gated parent)")

    # ---- physical quantities + frozen offset estimator -------------------
    zs = np.array([r["z"] for r in rows])
    da_kpc = COSMO.angular_diameter_distance(zs).to_value("kpc")
    for r, da in zip(rows, da_kpc):
        re_kpc = r["th50_arcsec"] / 206265.0 * da
        m_star = r["mstar_h2"] / LITTLE_H ** 2           # NSA h^-2 Msun -> Msun
        m_dyn = KV * (r["sigma_e"] * 1e3) ** 2 * (re_kpc * KPC_M) / G_SI / MSUN
        r["re_kpc"] = re_kpc
        r["log_mstar"] = math.log10(m_star)
        r["log_mdyn"] = math.log10(m_dyn)
        for tag, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
            # baseline (fixed NSA Chabrier-like IMF)
            d, gb, y = delta_offset(m_dyn, m_star, re_kpc, a0)
            r[f"delta_{tag}"] = d
            r[f"gbar_{tag}"] = gb
            r[f"y_{tag}"] = y
            # IMF bracket A: common-mode Salpeter-like x1.55
            r[f"delta_{tag}_imfA"], _, _ = delta_offset(m_dyn, m_star * IMF_A_FACTOR, re_kpc, a0)
            # IMF bracket B: sigma-dependent heavy IMF
            fB = 10 ** (IMF_B_SLOPE * math.log10(r["sigma_e"] / IMF_B_PIVOT))
            r[f"delta_{tag}_imfB"], _, _ = delta_offset(m_dyn, m_star * fB, re_kpc, a0)

    # ---- frozen pressure-supported selection ------------------------------
    for r in rows:
        r["cut_primary"] = int(r["vsig_glob"] < VSIG_PRIMARY)
        r["cut_variant"] = int(r["vsig_glob"] < VSIG_VARIANT)
    n_p = sum(r["cut_primary"] for r in rows)
    n_v = sum(r["cut_variant"] for r in rows)
    print(f"pressure-supported census: PRIMARY (V/sig<{VSIG_PRIMARY}): {n_p}   "
          f"VARIANT (V/sig<{VSIG_VARIANT}): {n_v}   parent: {len(rows)}")

    kept = [r for r in rows if r["cut_variant"]]  # catalog carries the variant superset
    kept.sort(key=lambda r: -r["snr_med"])

    cols = ["plateifu", "mangaid", "plate", "ifudsgn", "objra", "objdec", "z",
            "snr_med", "sb_1re", "sigma_e", "vsig_glob", "ba", "sersic_n",
            "th50_arcsec", "re_kpc", "log_mstar", "log_mdyn",
            "gbar_canon", "y_canon", "delta_canon", "delta_canon_imfA", "delta_canon_imfB",
            "gbar_alt", "y_alt", "delta_alt", "delta_alt_imfA", "delta_alt_imfB",
            "cut_primary", "cut_variant"]
    out = os.path.join(HERE, "stage_catalog.csv")
    with open(out, "w") as f:
        f.write(",".join(cols) + "\n")
        for r in kept:
            f.write(",".join(f"{r[c]:.6g}" if isinstance(r[c], float) else str(r[c])
                             for c in cols) + "\n")
    print(f"wrote {out}: {len(kept)} rows (VARIANT superset; cut_primary flags the primary)")

    # ---- summary stats (medians only; NO regression -- firewall) ----------
    for tag in ("canon", "alt"):
        d = np.array([r[f"delta_{tag}"] for r in kept if r["cut_primary"]])
        print(f"  PRIMARY sample delta_{tag}: median {np.median(d):+.3f} dex, "
              f"16-84% [{np.percentile(d,16):+.3f}, {np.percentile(d,84):+.3f}]  "
              f"(zero-point carries K_v + IMF; the SLOPE, not run here, is the test)")

    # ---- resolved-proxy subsample (frozen rule: SNR-top per sigma tercile) --
    prim = [r for r in kept if r["cut_primary"]]
    sig = np.array([r["sigma_e"] for r in prim])
    t1, t2 = np.percentile(sig, [33.3, 66.7])
    terc = [[r for r in prim if r["sigma_e"] <= t1],
            [r for r in prim if t1 < r["sigma_e"] <= t2],
            [r for r in prim if r["sigma_e"] > t2]]
    N_TARGET = 48
    sub = []
    for t in terc:
        t.sort(key=lambda r: -r["snr_med"])
        sub += t[:N_TARGET // 3]
    sub_out = os.path.join(HERE, "maps_subsample.csv")
    with open(sub_out, "w") as f:
        f.write("plateifu,plate,ifudsgn,snr_med,sigma_e,vsig_glob,url\n")
        for r in sub:
            url = (f"https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/"
                   f"{DAPTYPE}/{r['plate']}/{r['ifudsgn']}/"
                   f"manga-{r['plate']}-{r['ifudsgn']}-MAPS-{DAPTYPE}.fits.gz")
            f.write(f"{r['plateifu']},{r['plate']},{r['ifudsgn']},{r['snr_med']:.1f},"
                    f"{r['sigma_e']:.1f},{r['vsig_glob']:.3f},{url}\n")
    print(f"wrote {sub_out}: {len(sub)} galaxies (sigma_e terciles at {t1:.0f}/{t2:.0f} km/s)")
    print("NOTE: regression NOT run in this lane (freeze-then-fire; FROZEN.md sec.4-5).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
