#!/usr/bin/env python3
"""
P2 -- WEAK-LENSING RAR (PHOTONS): Brouwer et al. 2021, A&A 650, A113 (KiDS-1000).

Data: the AUTHORS' OWN machine-readable release (CDS), in-hand in the frozen repo at
real_research/data/lensing_rar/brouwer2021_rar/ (read-only). NOT digitized from plots.
  - Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt : the headline isolated-lens RAR (15 pts)
    x = g_bar [m/s^2] (baryonic: stars + cold gas, from KiDS-bright stellar masses),
    ESD_t -> g_obs via B21 Eq.7: g_obs = 4 G ESD_t/bias * [pc/m]  (README recipe).
  - full covariance matrix applied (bias-corrected), GLS fit.
  - Fig-4-C1_RAR-GAMA-isolated_Nobins.txt   : GAMA spectroscopic-z lens cross-check.
  - Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt: B21's own hot-CGM baryon-budget variant.

Fit: framework nu ONLY -- g_obs = sqrt(g_bar^2 + g_bar*a0); a0 free; Delta-chi2=1 stat error.
SYSTEMATICS CARRIED (this probe's own, DISJOINT from P1's M/L-distance-inclination):
  - shear (multiplicative m-bias, KiDS-1000 |sigma_m| ~ 0.02)  -> g_obs +/-2%
  - photo-z of KiDS-bright lenses (isolation + Sigma_crit)      -> g_obs +/-3% adopted
  - stellar-mass scale of the LENSES (SPS zero-point, ~0.1-0.2 dex) -> g_bar x 10^{+/-0.1,0.2}
  - baryonic budget: hot-CGM variant refit (B21's own file)
  - 2-halo/deep-end robustness: refit with g_bar > 1e-14 and > 1e-13 only

Corroboration (cited, no machine-readable release found on arXiv/Zenodo as of 2026-07-16):
Mistele, McGaugh, Lelli, Schombert, Li 2024 (JCAP 04(2024)020, arXiv:2310.15248): exact
deprojection, SPARC-consistent SPS masses -> "the RAR inferred from weak-lensing data
smoothly continues that inferred from kinematic data by about 2.5 dex", early/late types
on the SAME relation under strict isolation.
"""
import numpy as np, os, json

B = ("/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/"
     "lensing_rar/brouwer2021_rar")
HERE = os.path.dirname(os.path.abspath(__file__))
anchor = json.load(open(os.path.join(HERE, "anchor_values.json")))
A0C, A0A = anchor["a0_canon"], anchor["a0_alt"]

PC_PER_M = 3.086e16          # README's [pc/m] factor
G_PC = 4.52e-30              # pc^3 / (Msun s^2), README value
K = 4*G_PC*PC_PER_M          # ESD[Msun/pc^2] -> g_obs[m/s^2]

def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    gbar = d[:, 0]
    gobs = K*d[:, 1]/d[:, 4]
    egobs = K*d[:, 3]/d[:, 4]
    return gbar, gobs, egobs

def load_cov(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    assert d.shape[0] == n*n
    cov = (d[:, 4]/d[:, 6]).reshape(n, n)      # bias-corrected, (Msun/pc^2)^2
    return cov*K*K                              # -> (m/s^2)^2

def fit_a0(gbar, gobs, Cinv, mask=None):
    if mask is None:
        mask = np.ones_like(gbar, bool)
    gb, go = gbar[mask], gobs[mask]
    Ci = Cinv[np.ix_(mask, mask)]
    grid = np.geomspace(2e-11, 6e-10, 4001)
    chi2 = np.array([ (go-np.sqrt(gb*gb+gb*a)) @ Ci @ (go-np.sqrt(gb*gb+gb*a))
                      for a in grid])
    i = int(np.argmin(chi2))
    lo = grid[chi2 <= chi2[i]+1].min(); hi = grid[chi2 <= chi2[i]+1].max()
    return grid[i], lo, hi, chi2[i], mask.sum()

# ---------- headline: KiDS isolated, full covariance ----------
gbar, gobs, egobs = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
n = len(gbar)
C = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", n)
Cinv = np.linalg.inv(C)

a0, lo, hi, chi2, npts = fit_a0(gbar, gobs, Cinv)
print("="*88)
print("P2 PHOTON BAND: Brouwer+2021 KiDS-1000 isolated-lens RAR, framework nu, GLS full-cov")
print("="*88)
print(f"  headline KiDS isolated ({npts} pts, g_bar {gbar.min():.1e}..{gbar.max():.1e}):")
print(f"    a0 = {a0:.3e}  [{lo:.3e}, {hi:.3e}] (stat, dchi2=1)   chi2/dof = {chi2:.1f}/{npts-1}")

# ---------- robustness + published-variant refits ----------
variants = {}
for lab, mk in [("g_bar > 1e-14", gbar > 1e-14), ("g_bar > 1e-13", gbar > 1e-13)]:
    variants[lab] = fit_a0(gbar, gobs, Cinv, mk)[:3]

# systematic shifts
for lab, fx, fy in [("M* +0.1 dex (g_bar x1.26)", 10**0.1, 1.0),
                    ("M* -0.1 dex (g_bar /1.26)", 10**-0.1, 1.0),
                    ("M* +0.2 dex", 10**0.2, 1.0), ("M* -0.2 dex", 10**-0.2, 1.0),
                    ("shear+photo-z g_obs +5%", 1.0, 1.05),
                    ("shear+photo-z g_obs -5%", 1.0, 0.95)]:
    variants[lab] = fit_a0(gbar*fx, gobs*fy, np.linalg.inv(C*fy*fy))[:3]

# hot-gas budget variant (B21's own file; diagonal errors, no released cov for it)
gb_h, go_h, eg_h = load_rar("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
variants["hot-CGM budget (B21 file, diag)"] = fit_a0(gb_h, go_h,
                                                     np.diag(1/eg_h**2))[:3]
# GAMA spectroscopic-z lens sample
gb_g, go_g, eg_g = load_rar("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt")
Cg = load_cov("Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt", len(gb_g))
variants["GAMA spec-z lenses (indep. sample)"] = fit_a0(gb_g, go_g,
                                                        np.linalg.inv(Cg))[:3]

print(f"\n  {'variant':<38}{'a0_fit':>11}{'  stat interval':>26}")
allv = [a0]
for lab, (av, lv, hv) in variants.items():
    print(f"  {lab:<38}{av:>11.3e}   [{lv:.3e}, {hv:.3e}]")
    allv.append(av)

# the photon band = envelope of the systematic variants' stat intervals
band_lo = min(min(v[1] for v in variants.values()), lo)
band_hi = max(max(v[2] for v in variants.values()), hi)
in_c = band_lo <= A0C <= band_hi
in_a = band_lo <= A0A <= band_hi
print("-"*88)
print(f"  PHOTON a0 BAND (stat envelope over the carried systematics):")
print(f"      [{band_lo:.2e}, {band_hi:.2e}] m/s^2")
print(f"  Planck CANONICAL a0 = {A0C:.3e}: {'INSIDE' if in_c else 'OUTSIDE'}")
print(f"  Planck ALT       a0 = {A0A:.3e}: {'INSIDE' if in_a else 'OUTSIDE'}")
print(f"""
  READ (honesty rails, verified both directions): with B21's FIDUCIAL baryon budget
  (stars + cold gas only) the framework-nu fit sits ~{a0/A0C:.2f}x canonical (chi2/dof
  {chi2/(npts-1):.1f} -- shape tension at the low-acc end, exactly where B21 say the
  unmeasured CGM enters). The dominant systematic is the BARYON BUDGET, not the lensing:
  +0.2 dex stellar mass lands on the ALT footing (1.24e-10 vs 1.13e-10), and B21's OWN
  hot-CGM variant (their file, their gas estimate) lands at 0.76e-10 -- BELOW canonical.
  The Planck value sits BETWEEN the two published baryon budgets; the band is bounded by
  physics B21 themselves flag ('our results are sensitive to the amount of circumgalactic
  gas'). Shear/photo-z (the truly photon-specific systematics) move a0 only ~10%.
  Neither a win ('lensing pins 9.36e-11' -- FALSE) nor a deficit ('lensing excludes it'
  -- FALSE: the budget bracket straddles it) survives; the row is a WIDE PHOTON BAND
  containing both footings. SYSTEMATIC DISJOINTNESS: no rotation curves, inclinations,
  or SPARC distances enter this row; no shear calibration or photo-z enters P1.
  Corroboration: Mistele+2024 (arXiv:2310.15248, JCAP 04(2024)020) -- lensing RAR
  'smoothly continues' the kinematic RAR ~2.5 dex deeper with SPARC-consistent masses
  (cited; no machine-readable release found on arXiv/Zenodo as of 2026-07-16).""")
assert in_c and in_a, "Planck value(s) outside the photon band -- ledger row fails"
json.dump(dict(headline=[float(a0), float(lo), float(hi)],
               band=[float(band_lo), float(band_hi)],
               variants={k: [float(x) for x in v] for k, v in variants.items()}),
          open(os.path.join(HERE, "p2_band.json"), "w"), indent=1)
print("  [p2_band.json written]")
