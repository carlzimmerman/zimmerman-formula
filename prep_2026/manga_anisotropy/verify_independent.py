#!/usr/bin/env python3
"""Independent adversarial verification of the MaNGA Stage-1 anisotropy firing.
Own code path throughout: sklearn HuberRegressor (not the lane's IRLS), scipy
spearman, own bootstrap, own delta recomputation from the raw FITS.
"""
import os, sys, math
import numpy as np
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM
from scipy import stats
from sklearn.linear_model import HuberRegressor

LANE = "/Users/carlzimmerman/new_physics/prep_2026/manga_anisotropy"
DATA = os.path.join(LANE, "data")
RNG = np.random.default_rng(424242)  # DIFFERENT seed from the lane, on purpose
NB = 6000

A0C, A0A = 9.36e-11, 1.13e-10
G_SI, MSUN, KPC = 6.674e-11, 1.98892e30, 3.0856775814913673e19
COSMO = FlatLambdaCDM(H0=70.0, Om0=0.3)


def load_csv(path):
    import csv
    with open(path) as f:
        rd = csv.DictReader(f)
        rows = list(rd)
    out = {}
    for k in rows[0]:
        try:
            out[k] = np.array([float(r[k]) if r[k] not in ("", "nan") else np.nan for r in rows])
        except ValueError:
            out[k] = np.array([r[k] for r in rows])
    return out


def huber_slope(x, C, y):
    """sklearn Huber, x first column; returns slope on x."""
    X = np.column_stack([x, C])
    # standardize for solver stability, unscale slope
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1.0
    h = HuberRegressor(epsilon=1.345, alpha=0.0, max_iter=500).fit((X - mu) / sd, y)
    return h.coef_[0] / sd[0]


def ols_slope(x, C, y):
    A = np.column_stack([np.ones(len(y)), x, C])
    b, *_ = np.linalg.lstsq(A, y, rcond=None)
    return b[1]


def partial_spearman(y, x, C):
    ry = stats.rankdata(y); rx = stats.rankdata(x)
    RC = np.column_stack([np.ones(len(y))] + [stats.rankdata(C[:, j]) for j in range(C.shape[1])])
    py = ry - RC @ np.linalg.lstsq(RC, ry, rcond=None)[0]
    px = rx - RC @ np.linalg.lstsq(RC, rx, rcond=None)[0]
    return float(np.corrcoef(py, px)[0, 1])


def boot_cell(x, C, y, nb=NB, fit=huber_slope):
    n = len(y)
    s0 = fit(x, C, y)
    bs = []
    for _ in range(nb):
        i = RNG.integers(0, n, n)
        if np.unique(x[i]).size < 3:
            continue
        try:
            bs.append(fit(x[i], C[i], y[i]))
        except Exception:
            pass
    bs = np.array(bs)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    p = min(1.0, 2.0 * min((bs <= 0).mean(), (bs >= 0).mean()))
    return s0, lo, hi, p


def show(tag, x, C, y, fit=huber_slope):
    s, lo, hi, p = boot_cell(x, C, y, fit=fit)
    rho = partial_spearman(y, x, C)
    z = "ZERO-IN" if lo <= 0 <= hi else "zero-OUT"
    print(f"  {tag:<52s} N={len(y):>2d} slope={s:+.4f} [{lo:+.4f},{hi:+.4f}] p0={p:.3f} {z} prho={rho:+.3f}")
    return s, lo, hi, p


def main():
    cat = load_csv(os.path.join(LANE, "stage_catalog.csv"))
    res = load_csv(os.path.join(LANE, "resolved_proxies.csv"))

    idx = {p: i for i, p in enumerate(cat["plateifu"])}
    keep = [k for k, p in enumerate(res["plateifu"]) if p in idx and res["ok"][k] == 1]
    ci = np.array([idx[res["plateifu"][k]] for k in keep])
    ri = np.array(keep)

    P2 = res["P2_dlnsig_dlnR"][ri]
    P1 = res["P1_sigmaj_over_sigmin"][ri]
    vres = res["vsig_resolved"][ri]
    logM = cat["log_mstar"][ci]; logRe = np.log10(cat["re_kpc"][ci]); zred = cat["z"][ci]
    logsig = np.log10(cat["sigma_e"][ci]); ba = cat["ba"][ci]
    vsig_glob = cat["vsig_glob"][ci]
    dC = cat["delta_canon"][ci]; dA = cat["delta_alt"][ci]
    dCB = cat["delta_canon_imfB"][ci]
    C3 = np.column_stack([logM, logRe, zred])
    C4 = np.column_stack([logM, logRe, zred, logsig])

    # ---------------- 0. independent delta recomputation straight from the FITS
    print("=" * 100)
    print("[0] INDEPENDENT delta RECOMPUTATION from raw DAPall/drpall FITS (own code)")
    with fits.open(os.path.join(DATA, "dapall-v3_1_1-3.1.0.fits")) as h:
        dap = h["HYB10-MILESHC-MASTARSSP"].data
    with fits.open(os.path.join(DATA, "drpall-v3_1_1.fits")) as h:
        drp = h["MANGA"].data
    di = {p.strip(): i for i, p in enumerate(dap["PLATEIFU"])}
    dj = {p.strip(): i for i, p in enumerate(drp["plateifu"])}
    maxd = 0.0
    maxsig = 0.0
    for k in range(len(ci)):
        p = cat["plateifu"][ci[k]]
        i, j = di[p], dj[p]
        sig = float(dap["STELLAR_SIGMA_1RE"][i])
        th50 = float(drp["nsa_elpetro_th50_r"][j]); z = float(drp["nsa_z"][j])
        mst = float(drp["nsa_elpetro_mass"][j]) / 0.7 ** 2
        da = COSMO.angular_diameter_distance(z).to_value("kpc")
        re = th50 / 206265.0 * da
        mdyn = 5.0 * (sig * 1e3) ** 2 * re * KPC / G_SI / MSUN
        gb = G_SI * (mst * MSUN / 2) / (re * KPC) ** 2
        y = gb / A0C
        delta = math.log10(mdyn) - math.log10(math.sqrt(1 + 1 / y) * mst)
        maxd = max(maxd, abs(delta - dC[k]))
        maxsig = max(maxsig, abs(math.log10(sig) - logsig[k]))
    print(f"  max |delta_mine - delta_catalog| over the 48 = {maxd:.2e} dex  "
          f"(csv rounding ~1e-5 expected); max |dlogsig| = {maxsig:.2e}")

    # also recompute the cut cascade independently
    snr = np.array([r[0] for r in dap["SNR_MED"]])
    ok = np.ones(len(dap), bool)
    matched = np.array([p.strip() in dj for p in dap["PLATEIFU"]])
    ok &= matched
    n0 = ok.sum()
    ok &= dap["DAPDONE"].astype(bool); n1 = ok.sum()
    ok &= (dap["DAPQUAL"] == 0); n2 = ok.sum()
    jrow = np.array([dj.get(p.strip(), -1) for p in dap["PLATEIFU"]])
    t1 = np.where(jrow >= 0, drp["mngtarg1"][np.clip(jrow, 0, None)], 0)
    ok &= (t1 > 0); n3 = ok.sum()
    ms = np.where(jrow >= 0, drp["nsa_elpetro_mass"][np.clip(jrow, 0, None)], 0)
    t5 = np.where(jrow >= 0, drp["nsa_elpetro_th50_r"][np.clip(jrow, 0, None)], 0)
    zz = np.where(jrow >= 0, drp["nsa_z"][np.clip(jrow, 0, None)], 0)
    ok &= (ms > 0) & (t5 > 0) & (zz > 0.005) & (zz < 0.15); n4 = ok.sum()
    ok &= np.isfinite(snr) & (snr >= 10); n5 = ok.sum()
    s1 = dap["STELLAR_SIGMA_1RE"]
    ok &= np.isfinite(s1) & (s1 >= 70); n6 = ok.sum()
    print(f"  independent cascade: matched {n0} dapdone {n1} qual {n2} targ {n3} nsa {n4} snr {n5} sig {n6}"
          f"  (lane: 10782/10735/9027/8771/8766/3159/2442)")

    # ---------------- 1. independent regression, frozen cells
    print("=" * 100)
    print("[1] INDEPENDENT REGRESSION (sklearn Huber + own bootstrap seed 424242 + scipy ranks)")
    show("P2|canon|fixedIMF|C3   (lane: -0.6355 [-1.14,-0.20])", P2, C3, dC)
    show("P2|alt  |fixedIMF|C3   (lane: -0.6358)", P2, C3, dA)
    show("P2|canon|imfB|C4       (lane: +0.0020 zero-in)", P2, C4, dCB)
    show("P2|canon|fixedIMF|C3 OLS (estimator swap)", P2, C3, dC, fit=ols_slope)
    m1 = np.isfinite(P1)
    show("P1|canon|fixedIMF|C3 N=33 (lane: -1.086 zero-in)", P1[m1], C3[m1], dC[m1])

    # ---------------- 2. rotation/inclination contamination: strictest slow rotators
    print("=" * 100)
    print("[2] STRICTEST SLOW-ROTATOR SUBSETS (rotation/inclination contamination probe)")
    for cut in (0.30, 0.25, 0.20):
        m = vsig_glob < cut
        print(f"  DAPall (V/sig)_glob < {cut:.2f}: N={m.sum()}")
        if m.sum() >= 12:
            show(f"   P2|canon|fixedIMF|C3, vsig_glob<{cut}", P2[m], C3[m], dC[m])
    for cut in (0.10, 0.08):
        m = vres < cut
        print(f"  resolved V/sig < {cut:.2f}: N={m.sum()}")
        if m.sum() >= 12:
            show(f"   P2|canon|fixedIMF|C3, vsig_res<{cut}", P2[m], C3[m], dC[m])
    # inclination: add b/a as a control
    C3b = np.column_stack([logM, logRe, zred, ba])
    show("P2|canon|fixedIMF|C3+b/a control (inclination guard)", P2, C3b, dC)
    r_p2_ba = np.corrcoef(P2, ba)[0, 1]
    print(f"  corr(P2, b/a) = {r_p2_ba:+.3f}   corr(P2, vsig_res) = {np.corrcoef(P2, vres)[0,1]:+.3f}")

    # ---------------- 3. the IMF trap run the OTHER way: how much slope does a
    # literature-amplitude sigma-correlated IMF FAKE on its own?
    print("=" * 100)
    print("[3] IMF-FAKE BRACKET (impose dlog(M*/L)/dlog sigma = gamma; the faked slope is the")
    print("    change of the C3 fixed-IMF slope when the IMF trend is put IN; literature gamma:")
    print("    Treu+2010 ~0.31; Cappellari+2012/13 ~0.3-0.4; Li+2017 MaNGA ~0.3; La Barbera+2013 up to ~0.5-0.6)")
    s_fix = huber_slope(P2, C3, dC)
    for gam in (0.20, 0.30, 0.40, 0.60):
        fB = 10 ** (gam * (logsig - math.log10(130.0)))
        mst = 10 ** logM * fB
        # recompute delta with the IMF-corrected mass (nu recomputed too)
        gb = G_SI * (mst * MSUN / 2) / (10 ** logRe * KPC) ** 2
        y = gb / A0C
        dcorr = (dC + np.log10(10 ** logM) - np.log10(mst)
                 + np.log10(np.sqrt(1 + 1 / (cat["gbar_canon"][ci] / A0C))) - np.log10(np.sqrt(1 + 1 / y)))
        s_g = huber_slope(P2, C3, dcorr)
        print(f"  gamma={gam:.2f}: corrected-IMF slope {s_g:+.4f}; FAKED by fixed-IMF assumption = {s_fix - s_g:+.4f} "
              f"({100 * (s_fix - s_g) / s_fix:.0f}% of the observed {s_fix:+.4f})")
    print("  -> does the observed fixed-IMF slope exceed the literature-amplitude fake?")

    # ---------------- 4. STRUCTURAL TAUTOLOGY AUDIT (manufactured-null hunt)
    print("=" * 100)
    print("[4] STRUCTURAL AUDIT: delta is an EXACT function of (logsig, logRe, logM*) + log nu")
    A = np.column_stack([np.ones(48), logM, logRe, logsig, zred])
    r = dC - A @ np.linalg.lstsq(A, dC, rcond=None)[0]
    print(f"  OLS residual of delta_canon on (logM*,logRe,logsig,z): rms = {np.std(r):.5f} dex")
    print(f"  -> with logsig controlled, delta has ~NO free variation: the bracket-B cell is an")
    print(f"     algebraic identity, its ~0 slope was determined BEFORE any data (manufactured-null")
    print(f"     structure, though pre-registered).")
    # and the fixed-IMF slope is exactly the sigma channel:
    s_sig = huber_slope(P2, C3, 2.0 * logsig)
    print(f"  Huber slope of (2 log sigma_e) on P2 | C3 = {s_sig:+.4f} vs delta slope {s_fix:+.4f}")
    print(f"  -> the 'MI-signed' fixed-IMF slope IS the sigma_e-P2 structural relation (nu adds ~0).")

    # placebo proxy: sigma-matched noise with NO dynamical content
    print("  PLACEBO (manufactured-positive hunt): fake proxy = logsig-correlated pure noise,")
    print("  matched to corr(P2,logsig)=-0.62; if it 'fires' like P2, the P2 slope has no")
    print("  anisotropy-specific content:")
    rP2s = np.corrcoef(P2, logsig)[0, 1]
    zs = (logsig - logsig.mean()) / logsig.std()
    fires = 0; slopes = []
    for t in range(400):
        noise = RNG.standard_normal(48)
        fake = rP2s * zs + math.sqrt(1 - rP2s ** 2) * noise
        fake = fake * P2.std() + P2.mean()
        s, lo, hi, p = boot_cell(fake, C3, dC, nb=300)
        slopes.append(s)
        if hi < 0:
            fires += 1
    slopes = np.array(slopes)
    print(f"  400 placebo proxies: median slope {np.median(slopes):+.3f} "
          f"(16-84% [{np.percentile(slopes,16):+.3f},{np.percentile(slopes,84):+.3f}]); "
          f"{fires}/400 = {100*fires/400:.0f}% fire 'MI-like zero-OUT' at 95%")

    # ---------------- 5. cut-scan / influence
    print("=" * 100)
    print("[5] SELECTION HONESTY: cut-scan within the 48 + jackknife influence")
    for floor in (80, 90, 100, 120):
        m = 10 ** logsig >= floor
        if m.sum() >= 12:
            show(f"  sigma_e >= {floor} km/s (floor scan)", P2[m], C3[m], dC[m])
    for zmax in (0.06, 0.04):
        m = zred < zmax
        if m.sum() >= 12:
            show(f"  z < {zmax} (distance scan)", P2[m], C3[m], dC[m])
    # jackknife
    js = np.array([huber_slope(np.delete(P2, k), np.delete(C3, k, 0), np.delete(dC, k)) for k in range(48)])
    print(f"  jackknife slopes: min {js.min():+.3f} max {js.max():+.3f} (all same sign: {bool((js < 0).all())})")

    # ---------------- 6. P2-window drift (re-extract from the local MAPS)
    print("=" * 100)
    print("[6] P2 WINDOW SENSITIVITY (re-extracted from the 48 local MAPS files, own code)")
    import glob
    def p2_window(path, rlo, rhi):
        with fits.open(path) as h:
            sig = h["STELLAR_SIGMA"].data.astype(float)
            msk = h["STELLAR_SIGMA_MASK"].data
            iv = h["STELLAR_SIGMA_IVAR"].data.astype(float)
            corr = h["STELLAR_SIGMACORR"].data
            corr = corr[0] if corr.ndim == 3 else corr
            ell = h["SPX_ELLCOO"].data
            pifu = h[0].header.get("PLATEIFU")
        sc = np.sqrt(np.clip(sig ** 2 - np.nan_to_num(corr) ** 2, 0, None))
        v = np.isfinite(sc) & (sc > 1.0) & (msk == 0) & np.isfinite(iv) & (iv > 0) & np.isfinite(ell[1])
        w = v & (ell[1] >= rlo) & (ell[1] <= rhi)
        if w.sum() < 20:
            return pifu, np.nan
        b = np.polyfit(np.log10(ell[1][w]), np.log10(sc[w]), 1)
        return pifu, float(b[0])
    files = sorted(glob.glob(os.path.join(DATA, "maps", "*.fits.gz")))
    for rlo, rhi in ((0.5, 1.5), (0.5, 1.0), (0.75, 1.5), (0.3, 1.2)):
        p2w = {}
        for f in files:
            p, v = p2_window(f, rlo, rhi)
            p2w[p] = v
        arr = np.array([p2w.get(cat["plateifu"][c], np.nan) for c in ci])
        m = np.isfinite(arr)
        if m.sum() >= 20:
            show(f"  P2 window {rlo}-{rhi} Re (N={m.sum()})", arr[m], C3[m], dC[m])

    # ---------------- 7. amplitude budget, independent
    print("=" * 100)
    print("[7] MI AMPLITUDE BUDGET (independent)")
    yv = cat["y_canon"][ci]
    lnu = np.log10(np.sqrt(1 + 1 / yv))
    amp = abs(s_fix) * P2.std()
    lever = np.percentile(lnu, 84) - np.percentile(lnu, 16)
    print(f"  y median {np.median(yv):.1f}; log nu median {np.median(lnu):.4f}; trend amplitude "
          f"{amp:.3f} dex vs log-nu 16-84 spread {lever:.3f} dex -> ratio {amp/lever:.0f}x; "
          f"vs median log nu itself {amp/np.median(lnu):.1f}x")
    print("=" * 100)
    print("done (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
