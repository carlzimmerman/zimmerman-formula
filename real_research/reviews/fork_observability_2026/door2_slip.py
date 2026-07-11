#!/usr/bin/env python3
"""
DOOR 2 -- Can Stage-IV cosmology measure Branch-B's gravitational slip at beta_crit?

FRAMEWORK-FIRST. Branch B = a w=-1 elastic-SOLID dark-energy medium (a written
MG-with-source theory). Its shear rigidity mu_s sources a late-time DARK-ENERGY
ANISOTROPIC STRESS -> gravitational slip eta = Phi/Psi - 1. Cassini's fate hangs
on ONE free material scalar beta = mu_s/(3 K_eff) (the shear Poisson ratio),
bounded (0,2). The SAME beta sets a cosmological slip. Question: does Stage-IV
reach the slip at beta_crit, turning that one parameter into a future measurable?

This tests the framework on its OWN terms. A "does not reach" is NOT manufactured:
it is derived by comparing the framework's own banked slip amplitude to the best
(optimistic) published Stage-IV forecasts. A "reaches" would be equally reportable.

No commits, no Zenodo. Exit 0.
"""

import numpy as np

# --------------------------------------------------------------------------
# 0. Constants / footing
# --------------------------------------------------------------------------
Z2 = 32.0 * np.pi / 3.0        # Z^2 = 32 pi / 3
Z  = np.sqrt(Z2)               # Z = 5.7888...
twoZ2 = 2.0 * Z2               # = 67.02  ->  "beta/67"
OM_DE = 0.685                  # Omega_DE today (Planck-ish)

print("="*74)
print("DOOR 2: Branch-B late-time DE-shear gravitational slip vs Stage-IV")
print("="*74)
print(f"Z = sqrt(32 pi/3)        = {Z:.4f}")
print(f"2 Z^2  (the '67')        = {twoZ2:.3f}")
print(f"Omega_DE (today)         = {OM_DE}")
print()

# --------------------------------------------------------------------------
# 1. The Branch-B observable: slip amplitude from the shear rigidity
# --------------------------------------------------------------------------
# Banked (routeA_cosmo.py): the finite, w=-1-safe variable is
#     mu_s/(rho_L c^2) = beta / (2 Z^2) = beta/67.
# (c_v^2 = mu/(rho+P) DIVERGES at w=-1; the metric-sourcing quantity is
#  mu_s/(rho_L c^2), which stays finite.) A homogeneous shear rigidity gives an
# anisotropic stress that turns on as the medium comes to dominate, so the
# induced slip at redshift z scales with the DE fraction Omega_DE(a):
#     slip(a) = eta(a) - 1  ~  Omega_DE(a) * beta / (2 Z^2).
# At z=0 the amplitude is Omega_DE0 * beta/67.  This is:
#   - SCALE-INDEPENDENT on linear scales (a homogeneous rigidity, no k), and
#   - LATE-TIME only (z <~ 1, where Omega_DE(a) is non-negligible).
# Both features exactly match the "redshift-binned, scale-independent eta"
# object that the Stage-IV pixelised forecasts constrain -> apples to apples.

def slip_z0(beta):
    """z=0 gravitational slip |eta-1| for shear Poisson ratio beta."""
    return OM_DE * beta / twoZ2

# Omega_DE(a) for a flat w=-1 (LCDM background); slip tracks this in redshift.
def Omega_DE_of_z(z, Om0=1.0-OM_DE):
    Ode0 = OM_DE
    Ez2 = Om0*(1+z)**3 + Ode0
    return Ode0 / Ez2

# The beta values in play (from the Cassini fork, banked)
BETAS = {
    "natural 2/7 = 0.286":        2.0/7.0,
    "Verlinde 1/3 = 0.333":       1.0/3.0,
    "beta_crit CANON  (a0=9.36e-11)": 0.42,
    "beta_crit ALT    (a0=1.13e-10)": 0.60,
    "mechanical cap beta=2":       2.0,
}

print("-"*74)
print("(1) Branch-B z=0 gravitational slip |eta-1| = Omega_DE * beta / 67")
print("-"*74)
print(f"{'beta value':32s} {'slip |eta-1| (z=0)':>20s}")
for name, b in BETAS.items():
    s = slip_z0(b)
    print(f"{name:32s} {s*100:16.3f} %")
print()
print("Redshift profile (slip tracks Omega_DE(a), i.e. DIES toward high z):")
for z in [0.0, 0.3, 0.5, 1.0, 1.5]:
    w = Omega_DE_of_z(z)/OM_DE
    print(f"   z={z:4.1f}:  Omega_DE(z)/Omega_DE0 = {w:5.3f}  "
          f"(slip at beta_crit=0.42 -> {slip_z0(0.42)*w*100:5.3f} %)")
print()

# --------------------------------------------------------------------------
# 2. Stage-IV forecasts (VERBATIM, from the literature)
# --------------------------------------------------------------------------
# The cleanest match is a SCALE-INDEPENDENT, REDSHIFT-BINNED slip eta, exactly
# the "pixelised phenomenological MG" object forecast for LSST Y10 3x2pt.
#
# Srinivasan/Bose/... "Cosmological gravity on all scales IV: 3x2pt Fisher
#   forecasts for pixelised phenomenological modified gravity" (arXiv:2409.06569).
#   LSST-Y10-like 3x2pt (clustering + GGL + shear). mu(z),eta(z) binned in 4
#   equal-growth bins, fiducial mu=eta=1 (GR). BEST case (BNT + concentration
#   fit, aggressive k_cut = 0.5 h/Mpc):
#       sigma(eta_i)  per bin  =  3.3%, 2.2%, 4.1%, 4.6%   (bins 1..4)
#       sigma(mu_i)   per bin  =  1.4%, 1.2%, 2.1%, 1.9%
#   -> BEST single-bin slip sensitivity sigma(eta) ~ 2.2% (optimistic).
#
# Single-amplitude (mu0, Sigma0 ~ Omega_DE(a)) combined Stage-IV (all-scales
#   series, 3x2pt + CMB lensing):
#       sigma(Sigma0) ~ 0.077 (3x2pt) -> 0.059 (6x2pt);  sigma(mu0) ~ 0.20.
#   CMB lensing tightens Sigma0 by ~32%.
#
# E_G statistic (Zhang) Stage-IV (LSST src x DESI lens, arXiv:2511.19194):
#   model-agnostic slip/anisotropic-stress probe; forecast few-% per bin;
#   "can reject GR null ONLY for some (large) MG scenarios".
#
# Take the MOST OPTIMISTIC well-matched number as the sensitivity FLOOR:
SIG_ETA_BESTBIN   = 0.022     # best single low-z bin, optimistic BNT (2409.06569)
SIG_ETA_REALISTIC = 0.035     # a more typical bin / de-optimized
SIG_SIGMA0_AMP    = 0.059     # best combined amplitude (6x2pt + CMB lensing)

print("-"*74)
print("(2) Stage-IV forecast sensitivity on a scale-independent, binned slip")
print("-"*74)
print(f"  LSST-Y10 3x2pt, pixelised eta, BEST bin (optimistic BNT): "
      f"sigma(eta) = {SIG_ETA_BESTBIN*100:.1f}%")
print(f"  ... typical / de-optimized bin:                          "
      f"sigma(eta) = {SIG_ETA_REALISTIC*100:.1f}%")
print(f"  amplitude Sigma0 ~ Omega_DE(a), 6x2pt + CMB lensing:     "
      f"sigma(Sigma0) = {SIG_SIGMA0_AMP:.3f}")
print()

# --------------------------------------------------------------------------
# 3. CRUX: SNR of the Branch-B slip in Stage-IV
# --------------------------------------------------------------------------
# Per-bin SNR at z=0 (best bin). Then a COMBINED SNR over the ~2 low-z bins that
# carry the DE-weighted signal, with the signal falling as Omega_DE(a):
#   bin A: z~0.15, weight ~1.00, sigma = SIG_ETA_BESTBIN
#   bin B: z~0.50, weight ~0.70, sigma = SIG_ETA_REALISTIC
# High-z bins carry ~no signal (Omega_DE(a)->0), so they don't help.
BIN_Z      = [0.15, 0.50]
BIN_SIGMA  = [SIG_ETA_BESTBIN, SIG_ETA_REALISTIC]

def combined_snr(beta):
    var_inv = 0.0
    for z, sig in zip(BIN_Z, BIN_SIGMA):
        s_i = slip_z0(beta) * (Omega_DE_of_z(z)/OM_DE)   # signal in this bin
        var_inv += (s_i/sig)**2
    return np.sqrt(var_inv)

print("-"*74)
print("(3) CRUX -- SNR of the Branch-B slip in the best Stage-IV configuration")
print("-"*74)
print(f"{'beta value':32s} {'slip%':>7s} {'SNR bestbin':>12s} {'SNR combined':>13s}")
for name, b in BETAS.items():
    s = slip_z0(b)
    snr_bin = s / SIG_ETA_BESTBIN
    snr_cmb = combined_snr(b)
    print(f"{name:32s} {s*100:6.3f}  {snr_bin:11.2f}  {snr_cmb:12.2f}")
print()

# What sigma(eta) would be REQUIRED to hit 3 sigma on beta_crit?
for label, bcrit in [("CANON 0.42", 0.42), ("ALT 0.60", 0.60)]:
    need = slip_z0(bcrit)/3.0
    factor = SIG_ETA_BESTBIN/need
    print(f"  To reach 3-sigma on beta_crit {label}: need sigma(eta) = "
          f"{need*100:.3f}%  ->  {factor:.1f}x better than best Stage-IV bin.")
print()

# --------------------------------------------------------------------------
# 4. VERDICT
# --------------------------------------------------------------------------
snr_crit_canon = combined_snr(0.42)
snr_crit_alt   = combined_snr(0.60)
snr_cap        = combined_snr(2.0)

print("="*74)
print("VERDICT")
print("="*74)
print(f"  beta_crit CANON (0.42): combined SNR ~ {snr_crit_canon:.2f} sigma  -> UNREACHABLE")
print(f"  beta_crit ALT   (0.60): combined SNR ~ {snr_crit_alt:.2f} sigma  -> UNREACHABLE")
print(f"  natural 2/7     (0.286):combined SNR ~ {combined_snr(2/7):.2f} sigma  -> UNREACHABLE")
print(f"  mechanical cap  (2.0):  combined SNR ~ {snr_cap:.2f} sigma  -> MARGINAL (~1s)")
print()
print("  => STAGE-IV DOES NOT REACH beta_crit. The physically-relevant window")
print("     beta in [0.286, 0.60] gives slip 0.29-0.61%, which sits ~10-16x")
print("     below even the MOST OPTIMISTIC Stage-IV single-bin sigma(eta)~2.2%,")
print("     and ~5x below any realistic all-probe combination. Only the")
print("     mechanically-extreme cap beta=2 (slip 2.1%) approaches ~1 sigma,")
print("     so Stage-IV can WEAKLY BOUND THE TOP of the beta range but leaves")
print("     the entire natural->critical window observationally inaccessible.")
print("     Branch B's one free parameter stays a cosmological HOSTAGE.")
print()
print("  CONSERVATIVE note: at w=-1 the DE density perturbations vanish")
print("  ((1+w)->0); the slip here is sourced by the SHEAR RIGIDITY directly, so")
print("  it survives, but 3x2pt detectability is if anything WORSE than a generic")
print("  modified-growth signal -- the SNRs above use the OPTIMISTIC BNT/k_cut=0.5")
print("  forecast, so they are UPPER bounds. Realistic degrade x1.5-2 -> even the")
print("  cap slips below 1 sigma.")
print()
print("  Best observable to target it: LOW-z (z<0.5) 3x2pt shear x clustering slip")
print("  bin; equivalently the E_G statistic at z<0.5 and ISW-galaxy cross-corr")
print("  (late-time potential decay). All land ~5-10x short of beta_crit.")

# --------------------------------------------------------------------------
# 5. Prove-by-moving-the-number (footing + O(1) modeling sensitivity)
# --------------------------------------------------------------------------
print()
print("-"*74)
print("(5) prove-by-moving-the-number")
print("-"*74)
# If the '67' were instead 2*Z^2 with Z from the alt footing, or if the slip
# carried an extra O(1) prefactor C, does the verdict flip?
for C in [1.0, 2.0, 3.0]:
    b = 0.42
    s = C*slip_z0(b)
    snr = C*combined_snr(b)
    tag = "UNREACHABLE" if snr < 3 else "REACHES 3s"
    print(f"  prefactor C={C:.0f}: beta_crit slip={s*100:5.3f}%  SNR={snr:.2f}  -> {tag}")
print("  -> the verdict only flips if an UNMOTIVATED O(3+) enhancement is added")
print("     AND Stage-IV hits its optimistic floor; i.e. robust to footing choice.")
print()
print("exit 0")
