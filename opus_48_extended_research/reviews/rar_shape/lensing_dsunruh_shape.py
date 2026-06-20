#!/usr/bin/env python3
"""
GLOBAL RAR shape test: dS-Unruh vs McGaugh-exp vs simple-mu
against SPARC dynamical (Ups=0.70) + Brouwer+2021 KiDS-1000 weak-lensing RAR.

BOTH-WAYS (Carl #1): do NOT manufacture a shape-win for the framework; do NOT
high-priest a real shape-tension. Report convention-robustly. Run on the
framework's OWN dS-Unruh nu, but show the spread vs McGaugh/simple.

QUARANTINE: a0=9.36e-11 is an INPUT (c^2 sqrt(Lambda/32pi)); nothing here
derives a0/Z/kappa. The dS-Unruh interpolation g_obs=sqrt(g_bar^2+g_bar*a0) is
the framework's STATED functional form, tested as a falsifiable prediction.

Data:
  - real_research/data/lensing_rar/brouwer2021_rar/  (released ESD + 15x15 cov,
    B21 Eq.7 conversion to g_obs)
  - real_research/data/sparc_data/  (175 rotmod files: Rad, Vobs, errV, Vgas, Vdisk, Vbul)

References: Brouwer+2021 (A&A 650 A113, arXiv:2106.11677);
Mistele+2024 (JCAP 04 020, arXiv:2310.15248); Lelli/McGaugh/Schombert 2016 (SPARC);
McGaugh+2016 (M16, g_dagger=1.2e-10).
"""

import os
import numpy as np

np.set_printoptions(precision=4, suppress=False, linewidth=140)

# ----------------------------------------------------------------------
# Constants / paths
# ----------------------------------------------------------------------
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
LENS_DIR = os.path.join(REPO, "real_research/data/lensing_rar/brouwer2021_rar")
SPARC_DIR = os.path.join(REPO, "real_research/data/sparc_data")

A0_FRAMEWORK = 9.36e-11      # c^2 sqrt(Lambda/32pi) -- INPUT, quarantined
A0_CANON = 1.20e-10          # M16 g_dagger, canonical RAR a0
UPS = 0.70                   # framework's stellar M/L (disk); bulge 1.4*UPS standard

# B21 Eq.7 ESD->g_obs conversion constants
G_pc = 4.52e-30              # pc^3/(Msun s^2)
pc_per_m = 3.086e16          # pc/m
KCONV = 4.0 * G_pc * pc_per_m  # g_obs = KCONV * (ESD_t/bias)

# kpc->m, km/s->m/s for SPARC
KPC_M = 3.0857e19
KMS_MS = 1.0e3
G_SI = 6.674e-11
# SPARC accelerations: g = v^2/r  with v in m/s, r in m


# ----------------------------------------------------------------------
# Interpolation functions  nu(gbar) = g_obs/g_bar ; x = g_bar/a0
# All three share deep-MOND g_obs->sqrt(a0 gbar) and Newtonian g_obs->gbar
# ----------------------------------------------------------------------
def gobs_dsunruh(gbar, a0):
    """Framework dS-Unruh: g_obs = sqrt(gbar^2 + gbar*a0).  nu=sqrt(1+1/x)."""
    return np.sqrt(gbar * gbar + gbar * a0)

def gobs_mcgaugh(gbar, a0):
    """McGaugh-exp (B21 Eq.11, RAR fit): g_obs = gbar/(1-exp(-sqrt(gbar/a0)))."""
    x = gbar / a0
    return gbar / (1.0 - np.exp(-np.sqrt(x)))

def gobs_simple(gbar, a0):
    """simple-mu (mu=X/(1+X)): nu = 0.5 + sqrt(0.25 + 1/x)."""
    x = gbar / a0
    nu = 0.5 + np.sqrt(0.25 + 1.0 / x)
    return gbar * nu

MODELS = {
    "dS-Unruh": gobs_dsunruh,
    "McGaugh":  gobs_mcgaugh,
    "simple":   gobs_simple,
}


# ----------------------------------------------------------------------
# (A) Pure-shape divergence table (no data) -- where do the forms differ?
# ----------------------------------------------------------------------
def shape_divergence():
    print("=" * 72)
    print("(A) PURE SHAPE DIVERGENCE  (offset in dex of log10 g_obs, a0-independent in x)")
    print("=" * 72)
    a0 = A0_FRAMEWORK
    xs = [1e-5, 1e-4, 1e-3, 1e-2, 0.033, 0.1, 0.3, 1.0, 3.0, 10.0]
    print(f"{'x=gbar/a0':>10} {'dS-McG[dex]':>12} {'dS-simple[dex]':>15} {'lensing?':>9} {'rotcurve?':>10}")
    for x in xs:
        gbar = x * a0
        gd = gobs_dsunruh(gbar, a0)
        gm = gobs_mcgaugh(gbar, a0)
        gs = gobs_simple(gbar, a0)
        d_dm = np.log10(gd) - np.log10(gm)
        d_ds = np.log10(gd) - np.log10(gs)
        lens = "YES" if x <= 3.3e-2 else "-"
        rc = "YES" if 5e-3 <= x <= 20 else "-"
        print(f"{x:>10.0e} {d_dm:>+12.4f} {d_ds:>+15.4f} {lens:>9} {rc:>10}")
    # locate max divergence
    xg = np.logspace(-5, 1.3, 4000)
    gbar = xg * a0
    dm = np.log10(gobs_dsunruh(gbar, a0)) - np.log10(gobs_mcgaugh(gbar, a0))
    ds = np.log10(gobs_dsunruh(gbar, a0)) - np.log10(gobs_simple(gbar, a0))
    print(f"\n  max |dS-McG|  = {np.max(np.abs(dm)):.4f} dex at x={xg[np.argmax(np.abs(dm))]:.3f}")
    print(f"  max |dS-simple|= {np.max(np.abs(ds)):.4f} dex at x={xg[np.argmax(np.abs(ds))]:.3f}")
    print("  NOTE: max divergence sits at x~0.1-1 = ROTATION-CURVE regime, NOT the deep-lensing tail.")


# ----------------------------------------------------------------------
# (B) Load Brouwer+2021 lensing RAR (GAMA clean + KiDS-bright) + covariance
# ----------------------------------------------------------------------
def load_lensing(sample):
    if sample == "GAMA":
        nob = os.path.join(LENS_DIR, "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt")
        cov = os.path.join(LENS_DIR, "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt")
    elif sample == "KiDS":
        nob = os.path.join(LENS_DIR, "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
        cov = os.path.join(LENS_DIR, "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt")
    else:
        raise ValueError(sample)

    d = np.loadtxt(nob)
    gbar = d[:, 0]                       # m/s^2 (Radius column = g_bar for RAR files)
    esd_t = d[:, 1]
    bias = d[:, 4]
    gobs = KCONV * (esd_t / bias)        # B21 Eq.7, bias-corrected
    n = len(gbar)

    # covariance: cols [m_min, n_min, Radius_i, Radius_j, covariance, correlation, bias_ij]
    c = np.loadtxt(cov)
    C_esd = np.zeros((n, n))
    log_gbar = np.log10(gbar)
    def nearest(rval):
        return int(np.argmin(np.abs(log_gbar - np.log10(rval))))
    for row in c:
        ri, rj, covv, biasij = row[2], row[3], row[4], row[6]
        i = nearest(ri)
        j = nearest(rj)
        C_esd[i, j] = covv / biasij      # bias-correct the covariance (README)
    # propagate ESD-cov -> g_obs cov:  g_obs = KCONV * ESD/bias  (bias already in)
    # Jacobian per element = KCONV  (linear); bias handled per-row above as in README
    C_gobs = (KCONV ** 2) * C_esd
    gobs_err = np.sqrt(np.diag(C_gobs))
    return gbar, gobs, gobs_err, C_gobs


def chi2_full(gbar, gobs, C, model_fn, a0):
    pred = model_fn(gbar, a0)
    r = gobs - pred
    Cinv = np.linalg.inv(C)
    return float(r @ Cinv @ r)


def chi2_diag(gbar, gobs, gobs_err, model_fn, a0):
    pred = model_fn(gbar, a0)
    r = (gobs - pred) / gobs_err
    return float(np.sum(r * r))


def lensing_fits():
    print("\n" + "=" * 72)
    print("(B) BROUWER+2021 LENSING RAR FITS  (full 15x15 covariance, bias-corrected)")
    print("=" * 72)
    results = {}
    for sample in ["GAMA", "KiDS"]:
        gbar, gobs, gerr, C = load_lensing(sample)
        n = len(gbar)
        print(f"\n--- {sample} isolated  (n={n} bins; gbar range "
              f"{gbar.min():.2e}..{gbar.max():.2e} m/s^2 = {gbar.min()/A0_CANON:.1e}..{gbar.max()/A0_CANON:.1e} a0_canon)")
        # deepest bin: deep-MOND check
        print(f"    deepest bin: gbar={gbar[0]:.3e}, gobs_meas={gobs[0]:.3e}, "
              f"sqrt(a0c*gbar)={np.sqrt(A0_CANON*gbar[0]):.3e} (canon), "
              f"sqrt(a0f*gbar)={np.sqrt(A0_FRAMEWORK*gbar[0]):.3e} (fw)")
        results[sample] = {}
        for a0lab, a0 in [("a0=1.20e-10(canon)", A0_CANON), ("a0=9.36e-11(framework)", A0_FRAMEWORK)]:
            print(f"   [{a0lab}]")
            for mname, mfn in MODELS.items():
                c2f = chi2_full(gbar, gobs, C, mfn, a0)
                c2d = chi2_diag(gbar, gobs, gerr, mfn, a0)
                print(f"      {mname:9s}: chi2_full={c2f:7.2f} (red={c2f/n:5.3f})   "
                      f"chi2_diag={c2d:7.2f} (red={c2d/n:5.3f})")
                results[sample][(a0lab, mname)] = (c2f, c2f / n, c2d, c2d / n)
    return results


# ----------------------------------------------------------------------
# (B2) Deep-MOND normalization from the lensing tail (no-slip a0 match)
# ----------------------------------------------------------------------
def deep_mond_norm():
    print("\n" + "=" * 72)
    print("(B2) DEEP-MOND NORMALIZATION from lensing tail  <g_obs^2/g_bar>  (a0 match test)")
    print("=" * 72)
    for sample in ["GAMA", "KiDS"]:
        gbar, gobs, gerr, C = load_lensing(sample)
        # deepest bins where x<<1 (use x < 0.05 a0_canon)
        mask = gbar < 0.05 * A0_CANON
        a0_est = gobs[mask] ** 2 / gbar[mask]
        # inverse-variance-ish weight by g_obs error propagated to a0=gobs^2/gbar
        w = 1.0 / (2 * gobs[mask] * gerr[mask] / gbar[mask]) ** 2
        a0_wmean = np.sum(w * a0_est) / np.sum(w)
        print(f"  {sample}: deep bins (x<0.05) n={mask.sum()};  "
              f"per-bin a0=gobs^2/gbar range [{a0_est.min():.2e}, {a0_est.max():.2e}]")
        print(f"        weighted-mean lensing a0 = {a0_wmean:.3e} m/s^2  "
              f"(framework 9.36e-11; canon 1.2e-10; SPARC ~0.9-1.2e-10)")
    print("  => no-slip test: lensing-regime a0 vs dynamical a0 (compare to SPARC fit below).")


# ----------------------------------------------------------------------
# (C) SPARC dynamical RAR (175 galaxies, Ups=0.70) -- best-fit a0 per model
# ----------------------------------------------------------------------
def load_sparc():
    files = [f for f in os.listdir(SPARC_DIR) if f.endswith("_rotmod.dat")]
    gbar_all, gobs_all = [], []
    for f in sorted(files):
        try:
            d = np.loadtxt(os.path.join(SPARC_DIR, f))
        except Exception:
            continue
        if d.ndim == 1:
            d = d[None, :]
        rad = d[:, 0] * KPC_M           # m
        vobs = d[:, 1] * KMS_MS         # m/s
        vgas = d[:, 3] * KMS_MS
        vdisk = d[:, 4] * KMS_MS
        vbul = d[:, 5] * KMS_MS
        # baryonic velocity with Ups: gas as-is, disk*sqrt(Ups), bulge*sqrt(1.4*Ups)
        vbar2 = vgas * np.abs(vgas) + UPS * vdisk * np.abs(vdisk) + (1.4 * UPS) * vbul * np.abs(vbul)
        good = (rad > 0) & (vbar2 > 0) & (vobs > 0)
        rad, vobs, vbar2 = rad[good], vobs[good], vbar2[good]
        gbar = vbar2 / rad
        gobs = vobs * vobs / rad
        gbar_all.append(gbar)
        gobs_all.append(gobs)
    return np.concatenate(gbar_all), np.concatenate(gobs_all)


def sparc_fit():
    print("\n" + "=" * 72)
    print("(C) SPARC DYNAMICAL RAR  (175 gals, Ups=0.70)  best-fit a0 per interpolation")
    print("=" * 72)
    gbar, gobs = load_sparc()
    n = len(gbar)
    print(f"  total points n={n};  gbar range {gbar.min():.2e}..{gbar.max():.2e} "
          f"= {gbar.min()/A0_CANON:.3f}..{gbar.max()/A0_CANON:.1f} a0_canon")
    # scatter (dex) of log gobs about the model prediction; minimize over a0
    a0grid = np.logspace(np.log10(3e-11), np.log10(3e-10), 200)
    out = {}
    for mname, mfn in MODELS.items():
        scat = []
        for a0 in a0grid:
            pred = mfn(gbar, a0)
            d = np.log10(gobs) - np.log10(pred)
            scat.append(np.std(d))
        scat = np.array(scat)
        k = np.argmin(scat)
        a0best = a0grid[k]
        out[mname] = (a0best, scat[k])
        # scatter penalty of forcing framework a0
        pred_fw = mfn(gbar, A0_FRAMEWORK)
        scat_fw = np.std(np.log10(gobs) - np.log10(pred_fw))
        pen = (scat_fw - scat[k]) / scat[k] * 100
        print(f"  {mname:9s}: best-fit a0={a0best:.3e}  scatter={scat[k]:.4f} dex   "
              f"| force a0=9.36e-11 -> scatter={scat_fw:.4f} dex (penalty {pen:+.2f}%)")
    return out, gbar, gobs


# ----------------------------------------------------------------------
# (D) GLOBAL fit: SPARC + lensing jointly -- best a0 and per-model scatter
# ----------------------------------------------------------------------
def global_fit():
    print("\n" + "=" * 72)
    print("(D) GLOBAL RAR  (SPARC dynamical + GAMA lensing)  joint best-fit a0")
    print("=" * 72)
    gbar_s, gobs_s = load_sparc()
    gbar_l, gobs_l, gerr_l, _ = load_lensing("GAMA")
    # build combined log-residual scatter; weight lensing by per-bin log error
    logerr_l = gerr_l / (gobs_l * np.log(10))
    a0grid = np.logspace(np.log10(3e-11), np.log10(3e-10), 200)
    for mname, mfn in MODELS.items():
        best = None
        for a0 in a0grid:
            # SPARC: unweighted log scatter (intrinsic-dominated)
            ds = np.log10(gobs_s) - np.log10(mfn(gbar_s, a0))
            chi_s = np.sum((ds / 0.13) ** 2)          # 0.13 dex intrinsic per pt (M16)
            # lensing: weighted by measurement log error
            dl = np.log10(gobs_l) - np.log10(mfn(gbar_l, a0))
            chi_l = np.sum((dl / logerr_l) ** 2)
            tot = chi_s + chi_l
            if best is None or tot < best[0]:
                best = (tot, a0)
        # report at framework a0 too
        ds = np.log10(gobs_s) - np.log10(mfn(gbar_s, A0_FRAMEWORK))
        dl = np.log10(gobs_l) - np.log10(mfn(gbar_l, A0_FRAMEWORK))
        chi_fw = np.sum((ds / 0.13) ** 2) + np.sum((dl / logerr_l) ** 2)
        print(f"  {mname:9s}: joint best a0={best[1]:.3e} (chi2={best[0]:.1f})   "
              f"| a0=9.36e-11 chi2={chi_fw:.1f} (dchi2={chi_fw-best[0]:+.1f})")


# ----------------------------------------------------------------------
# (E) Headline both-ways comparison on the lensing data
# ----------------------------------------------------------------------
def headline(results):
    print("\n" + "=" * 72)
    print("(E) HEADLINE both-ways:  dS-Unruh vs McGaugh on lensing  (Delta chi2 -> sigma)")
    print("=" * 72)
    for sample in ["GAMA", "KiDS"]:
        for a0lab in ["a0=1.20e-10(canon)", "a0=9.36e-11(framework)"]:
            c2_ds = results[sample][(a0lab, "dS-Unruh")][0]
            c2_mg = results[sample][(a0lab, "McGaugh")][0]
            c2_sm = results[sample][(a0lab, "simple")][0]
            dchi = c2_ds - c2_mg
            sig = np.sqrt(abs(dchi))    # 1-dof model swap, no free param differs
            who = "McGaugh better" if dchi > 0 else "dS-Unruh better"
            print(f"  {sample:5s} [{a0lab:22s}]: chi2(dS)={c2_ds:6.2f} chi2(McG)={c2_mg:6.2f} "
                  f"chi2(simple)={c2_sm:6.2f}  dchi2={dchi:+5.2f} ~{sig:.2f}sigma ({who})")


if __name__ == "__main__":
    shape_divergence()
    res = lensing_fits()
    deep_mond_norm()
    sparc_fit()
    global_fit()
    headline(res)
    print("\nDONE.")
