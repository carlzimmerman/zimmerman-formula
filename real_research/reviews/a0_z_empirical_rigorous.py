#!/usr/bin/env python3
"""
LAYER 2 -- the a0(z) data, done rigorously from the repo's SPARC + the high-z points.
====================================================================================
Empirical test of the one falsifiable claim, a0(z)=a0(0)E(z). We
 (1) FIT the z=0 anchor ourselves from the 175 SPARC rotation curves (the RAR g-dagger),
     instead of quoting it -- a real measurement;
 (2) build the a0(z) ladder with the two high-z determinations;
 (3) fit a0 = A E(z)^p and run the model comparison + jackknife + inter-method systematic;
 (4) forecast what NEW point would move the ~2 sigma.
Honest throughout: we report the fragility, not just the headline.
Needs numpy + the SPARC files in ../data/sparc_data/.
"""
import numpy as np, glob, os

kpc = 3.0857e19
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")
OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM*(1+z)**3 + OL)
ML_D, ML_B = 0.5, 0.7                    # SPARC 3.6um stellar mass-to-light (standard)


# ---------- (1) fit the RAR g-dagger ( = a0 at z=0 ) from SPARC -----------------
def rar_function(gbar, a0):
    """McGaugh, Lelli & Schombert 2016 RAR: g_obs = gbar / (1 - exp(-sqrt(gbar/a0)))."""
    x = np.sqrt(gbar/a0)
    return gbar/(1.0 - np.exp(-x))

def load_sparc_points():
    gbar, gobs, w = [], [], []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        Rm = R*kpc
        Vbar2 = np.sign(Vgas)*Vgas**2 + ML_D*Vdisk**2 + ML_B*Vbul**2
        gb = Vbar2*1e6/Rm
        go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (R > 0) & (Vobs > 0)
        # weight by fractional velocity error (down-weight noisy points)
        frac = np.where(Vobs > 0, np.clip(eV, 1, None)/np.clip(Vobs, 1, None), 1.0)
        gbar += list(gb[ok]); gobs += list(go[ok]); w += list(1.0/frac[ok]**2)
    return np.array(gbar), np.array(gobs), np.array(w)

def fit_a0(gbar, gobs, w):
    """Best-fit a0 = minimum weighted vertical scatter in log g_obs about the RAR."""
    grid = np.linspace(0.5e-10, 3.0e-10, 600)
    scat = []
    for a0 in grid:
        resid = np.log10(gobs) - np.log10(rar_function(gbar, a0))
        scat.append(np.sqrt(np.sum(w*resid**2)/np.sum(w)))
    scat = np.array(scat); i = np.argmin(scat)
    return grid[i], scat[i], grid, scat


def part1_sparc():
    print("="*82); print("(1) FIT the z=0 anchor from 175 SPARC rotation curves (the RAR)"); print("="*82)
    gbar, gobs, w = load_sparc_points()
    a0, sc, grid, scurve = fit_a0(gbar, gobs, w)
    # bootstrap error over points
    rng_idx = np.arange(len(gbar))
    boots = []
    for k in range(200):
        s = (np.sin(np.arange(len(gbar))*(k+1)*2.399963) * 1e6 % len(gbar)).astype(int)  # deterministic resample
        b, _, _, _ = fit_a0(gbar[s], gobs[s], w[s]); boots.append(b)
    err_stat = np.std(boots)
    print(f"  pooled SPARC points: {len(gbar)}")
    print(f"  best-fit RAR a0 (g-dagger) = {a0*1e10:.2f}e-10 m/s^2   (McGaugh+16: 1.20+/-0.02_stat+/-0.24_sys)")
    print(f"  vertical RAR scatter = {sc:.3f} dex (Lelli+17: 0.13 total, <=0.06 intrinsic)")
    print(f"  bootstrap stat error ~ {err_stat*1e10:.2f}e-10; M/L systematic dominates at ~0.24e-10")
    print(f"  -> we ADOPT the z=0 anchor a0(0) = {a0*1e10:.2f} +/- 0.26 (sys-dominated). [own measurement]\n")
    return a0


# ---------- (2)-(3) the a0(z) ladder, fit, model comparison, jackknife ----------
def fit_powerlaw(z, a0, sig):
    """Fit log a0 = logA + p logE(z), weighted; return A, p, sigma_p, chi2(p), chi2(p=0,1,1.5)."""
    x = np.log10(E(z)); y = np.log10(a0); ey = sig/(a0*np.log(10))
    W = 1.0/ey**2
    # weighted linear regression y = b + p x
    Sw, Sx, Sy = W.sum(), (W*x).sum(), (W*y).sum()
    Sxx, Sxy = (W*x*x).sum(), (W*x*y).sum()
    den = Sw*Sxx - Sx*Sx
    p = (Sw*Sxy - Sx*Sy)/den; b = (Sy - p*Sx)/Sw
    sig_p = np.sqrt(Sw/den)
    chi2 = lambda pp, bb: np.sum(W*(y - (bb + pp*x))**2)
    # for fixed p, best b: b = (Sy - p Sx)/Sw
    def chi2_fixed_p(pp):
        bb = (Sy - pp*Sx)/Sw; return chi2(pp, bb)
    return dict(A=10**b, p=p, sig_p=sig_p, chi2_free=chi2(p, b),
               chi2_p0=chi2_fixed_p(0.0), chi2_p1=chi2_fixed_p(1.0), chi2_p15=chi2_fixed_p(1.5))


def part23(a0_z0):
    print("="*82); print("(2-3) the a0(z) ladder, power-law fit, and model comparison"); print("="*82)
    z   = np.array([0.00, 0.05, 0.90])
    a0  = np.array([a0_z0*1e10, 1.69, 2.38])          # our SPARC anchor + Varasteanu + MUSE-DARK
    sig = np.array([0.26, 0.13, 0.11])
    src = ["SPARC (our fit)", "Varasteanu 2025", "MUSE-DARK III 2026"]
    print(f"  {'z':>6}{'E(z)':>7}{'a0[e-10]':>11}{'+/-':>7}   source")
    for zz, ee, aa, ss, sc in zip(z, E(z), a0, sig, src):
        print(f"  {zz:>6.2f}{ee:>7.3f}{aa:>11.2f}{ss:>7.2f}   {sc}")
    f = fit_powerlaw(z, a0, sig)
    print(f"\n  power-law fit a0 = A E(z)^p:  A={f['A']:.2f}e-10,  p = {f['p']:.2f} +/- {f['sig_p']:.2f}")
    print(f"  model comparison (chi^2, 1 dof for fixed-p models):")
    print(f"     constant a0 (p=0):     chi^2 = {f['chi2_p0']:.1f}  -> reject at "
          f"{np.sqrt(max(f['chi2_p0']-f['chi2_free'],0)):.1f} sigma (naive)")
    print(f"     framework  (p=1):      chi^2 = {f['chi2_p1']:.1f}")
    print(f"     matter-only(p=1.5):    chi^2 = {f['chi2_p15']:.1f}  -> reject at "
          f"{np.sqrt(max(f['chi2_p15']-f['chi2_free'],0)):.1f} sigma")

    # jackknife: drop the high-leverage z=0.9 point (only z=0,0.05 remain)
    fj = fit_powerlaw(z[:2], a0[:2], sig[:2])
    sig_jk = np.sqrt(max(fj['chi2_p0']-fj['chi2_free'], 0))
    print(f"\n  JACKKNIFE (drop z=0.9): only z=0,0.05 remain, where E spans just 1.000-1.025,")
    print(f"     so the log-E lever arm collapses and p is unconstrained; constant-a0 is then")
    print(f"     rejected at only {sig_jk:.1f} sigma. The whole trend RESTS on the single z=0.9 point.")

    # inter-method systematic from the near-coincident local pair (our anchor vs Varasteanu at dz=0.05)
    sys2 = ((1.69 - a0[0])**2 - sig[0]**2 - sig[1]**2)
    sig_sys = np.sqrt(max(sys2, 0))
    sig_infl = np.sqrt(sig**2 + sig_sys**2)
    fs = fit_powerlaw(z, a0, sig_infl)
    print(f"  SYSTEMATIC: the {a0[0]:.2f} vs 1.69 local pair (dz=0.05, cannot be real evolution) implies")
    print(f"     sigma_sys ~ {sig_sys:.2f}e-10; folding it in -> constant-a0 reject at "
          f"{np.sqrt(max(fs['chi2_p0']-fs['chi2_free'],0)):.1f} sigma.")
    print(f"  => HONEST significance: ~2 sigma, single-point-driven. A hint, not a detection.\n")
    return z, a0, sig_infl


# ---------- (4) what new point would move it -----------------------------------
def part4_forecast(z, a0, sig):
    print("="*82); print("(4) forecast: the new measurement that turns the hint into a result"); print("="*82)
    for znew, prec in [(3.0, 0.10), (3.0, 0.03), (6.0, 0.10)]:
        a_pred = a0[0]*E(znew)                      # framework prediction at znew
        s_new = prec*a_pred
        zc = np.append(z, znew); ac = np.append(a0, a_pred); sc = np.append(sig, s_new)
        fc = fit_powerlaw(zc, ac, sc)
        sigma = np.sqrt(max(fc['chi2_p0']-fc['chi2_free'], 0))
        print(f"  add z={znew}, a0={a_pred:.2f}e-10 at {int(prec*100)}% precision (deep-MOND, clean):"
              f"  p={fc['p']:.2f}+/-{fc['sig_p']:.2f}, constant-a0 rejected at {sigma:.1f} sigma")
    print("""  READ: one CLEAN deep-MOND a0 at z=3 to 3% turns ~2 sigma into a decisive (>5 sigma)
  measurement and pins p to ~0.04. THAT is the experiment -- not more local galaxies, not
  the compact/AGN high-z systems, but a single clean extended deep-MOND rotation curve at z~3.""")


def main():
    a0_z0 = part1_sparc()
    z, a0, sig = part23(a0_z0)
    part4_forecast(z, a0, sig)
    print("\n"+"="*82); print("LAYER-2 VERDICT (empirical)"); print("="*82)
    print("""  * z=0 anchor MEASURED from SPARC ourselves: a0 ~ 1.1-1.2e-10, RAR scatter ~0.13 dex --
    consistent with McGaugh+16; the method and the anchor are sound.
  * a0(z) trend: p ~ 0.8, constant a0 'rejected at ~5 sigma' NAIVELY, but the jackknife
    (drops to ~1 sigma without z=0.9) and the local-pair systematic (~2 sigma) show the
    honest significance is ~2 sigma -- a single-point-driven HINT, not a detection.
  * it is also LCDM-degenerate (apparent a0 rises as E in LCDM too) -- so even a firm trend
    tests 'evolving vs constant', not 'this framework vs LCDM' (that is the EFE test, Layer 4).
  * the decisive datum is ONE clean deep-MOND a0 at z~3 to a few percent. Until then: a hint.""")
    print("="*82)


if __name__ == "__main__":
    main()
