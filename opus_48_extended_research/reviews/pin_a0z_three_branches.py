#!/usr/bin/env python3
"""
ROUTE [pin_a0z]: pin the framework's a0(z) prediction RIGOROUSLY, all three readings.

The framework:  a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = cH_Lambda/Z, Z=sqrt(32pi/3).
The DISTINCTIVE content beyond z=0 MOND:  a0 is tied to the DARK-ENERGY density, so
    a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE0 ).

THE SUBTLETY (the whole point of this route):
  (i)  CONSTANT-Lambda (true cosmological constant, w=-1): rho_DE = const  =>  a0(z) = a0(0) FLAT.
       This is the NULL-DISTINCTIVE case: a0(z) flat is INDISTINGUISHABLE from z=0 MOND.
  (ii) DESI-EVOLVING-DE (w0waCDM, w0>-1, wa<0, thawing): rho_DE was LOWER in the past
       => a0(z) DECLINES with z (with a small non-monotonic bump where w crosses -1).
       This is the ONLY case with a distinctive beyond-MOND signal.
  (iii) RIVAL rising branch a0 ∝ cH(z) = cH0 E(z): RISES with z. NOT the framework's
       sqrt(rho_DE) branch (it is the rho_total footing-bug); tabulated to distinguish.

THE IF CANCELS IN THE RATIO: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) does not depend on the
absolute coefficient (9.36e-11) or the interpolation function -> interpolation-robust (banked).

C. Zimmerman framework / opus-4.8 verification, 2026-06-14. numpy only.
"""
import numpy as np

c    = 2.99792458e8          # m/s
G    = 6.674e-11             # SI
H0   = 2.20e-18              # s^-1  (~67.9 km/s/Mpc), for cH0 scale only
OM, OL = 0.3137, 0.6863      # for E(z) (the Verlinde rival) and matter cross-checks

# ---- the absolute coefficient (closed/moot; only the RATIO is the live prediction) ----
Lambda = 1.106e-52           # m^-2 (Planck-ish)
a0_abs = c**2 * np.sqrt(Lambda/(32*np.pi))
print("="*84)
print("FRAMEWORK COEFFICIENT (closed, moot; only the a0(z)/a0(0) RATIO is the live test)")
print("="*84)
print(f"  a0(0) = c^2 sqrt(Lambda/32pi) = {a0_abs:.3e} m/s^2   (canonical 9.36e-11)")
print(f"  Z = sqrt(32pi/3) = {np.sqrt(32*np.pi/3):.4f};  cH0/a0 = {c*H0/9.36e-11:.3f}")
print("  NOTE: the IF (Lambda vs ...) CANCELS in the ratio; below is coefficient-free.\n")

# ============================================================================
#  DESI DR2 (2025) BAO+CMB+SNe CPL fits (three SNe compilations); fiducial = DESY5
# ============================================================================
DESI = {
    "DESY5":     dict(w0=-0.752, wa=-0.86, sw0=0.057, swa=0.22, rho=-0.86),
    "Union3":    dict(w0=-0.667, wa=-1.09, sw0=0.088, swa=0.31, rho=-0.87),
    "Pantheon+": dict(w0=-0.838, wa=-0.62, sw0=0.055, swa=0.28, rho=-0.85),
}
FID = "DESY5"
f = DESI[FID]; w0, wa = f["w0"], f["wa"]

def rho_DE_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE0 for CPL w(a)=w0+wa(1-a) = a^{-3(1+w0+wa)} exp[-3 wa (1-a)]."""
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))

def a0_const(z):                         # (i) CONSTANT-Lambda: w=-1, rho_DE const
    return np.ones_like(np.atleast_1d(z*1.0))
def a0_desi(z, w0=w0, wa=wa):            # (ii) DESI evolving-DE: a0 ∝ sqrt(rho_DE)
    return np.sqrt(rho_DE_ratio(z, w0, wa))
def a0_verlinde(z):                      # (iii) RIVAL: a0 ∝ cH(z) ∝ E(z)
    return np.sqrt(OM*(1+z)**3 + OL)

def Vfrac(ratio):                        # V_flat^4 = G M_bar a0 => V ∝ a0^{1/4}
    return (ratio**0.25 - 1.0)*100.0
def Vdex(ratio):
    return 0.25*np.log10(ratio)

# ---- the non-monotonic peak of the DESI branch (w crosses -1 at 1-a=(-1-w0)/wa) ----
across = (-1.0 - w0)/wa
z_cross = 1.0/(1.0-across) - 1.0
p = -1.5*(1.0+w0+wa); q = -1.5*wa; a_star = p/q
z_peak = 1.0/a_star - 1.0 if 0 < a_star < 1 else None

print("="*84)
print(f"THE THREE BRANCHES, tabulated   [DESI fiducial: w0={w0}, wa={wa}]")
print("="*84)
print(f"  (i)  CONSTANT-Lambda  -> a0(z)=a0(0) FLAT  [w=-1, NULL-distinctive = z=0 MOND]")
print(f"  (ii) DESI-evolving    -> a0 ∝ sqrt(rho_DE), DECLINES (bump z~{z_cross:.2f} where w=-1)")
print(f"  (iii)RIVAL Verlinde   -> a0 ∝ cH(z), RISES  [NOT the framework's branch]\n")
print(f"  DESI branch peaks at z={z_peak:.2f}: a0/a0(0)={float(a0_desi(z_peak)):.4f} "
      f"(+{(float(a0_desi(z_peak))-1)*100:.1f}% bump), then declines.\n")

hdr = ("   z   | (i)const | (ii)DESI a0/a0(0)   V%    dex   | (iii)Verlinde a0  V%")
print(hdr); print("-"*84)
for z in [0.0, 0.2, 0.41, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 10.0]:
    ad = float(a0_desi(z)); av = float(a0_verlinde(z))
    print(f" {z:5.2f} |  1.0000  |  {ad:6.4f}  {Vfrac(ad):+6.1f}% {Vdex(ad):+6.3f} "
          f"|   {av:6.3f}  {Vfrac(av):+6.1f}%")

# ============================================================================
#  THE DISTINCTIVE TEST (ii): the high-z BTFR offset  (M_b = V^4 / (G a0(z)))
#  banked claim to VERIFY: -0.033 dex / -7% in V by z=3
# ============================================================================
print("\n" + "="*84)
print("DISTINCTIVE TEST: high-z BTFR offset (DESI branch only)  -- verify banked -7%/-0.033dex@z=3")
print("="*84)
for z in [1.0, 2.0, 3.0, 5.0, 6.0]:
    ad = float(a0_desi(z))
    print(f"  z={z:.1f}: a0/a0(0)={ad:.4f}  ->  V offset {Vfrac(ad):+.2f}%   "
          f"BTFR zero-point shift {Vdex(ad):+.4f} dex")
z3 = float(a0_desi(3.0))
print(f"\n  BANKED CHECK @z=3: -7.3% / -0.033 dex  vs computed {Vfrac(z3):+.2f}% / {Vdex(z3):+.4f} dex"
      f"  -> {'MATCH' if abs(Vfrac(z3)+7.3)<0.5 else 'MISMATCH'}")

# ============================================================================
#  DISTINGUISHABILITY: is the DESI declining branch separable from FLAT (const)?
#  propagate the DESI w0-wa covariance; flat=1.000 inside or outside 1 sigma?
# ============================================================================
print("\n" + "="*84)
print("DISTINGUISHABILITY of (ii)DESI-declining from (i)FLAT  [DESI w0-wa covariance, 20k MC]")
print("="*84)
rng = np.random.default_rng(0)
cov = np.array([[f["sw0"]**2, f["rho"]*f["sw0"]*f["swa"]],
                [f["rho"]*f["sw0"]*f["swa"], f["swa"]**2]])
with np.errstate(all="ignore"):   # suppress spurious Accelerate-BLAS matmul FP warnings (output unaffected)
    samp = rng.multivariate_normal([w0,wa], cov, size=20000)
print("   z   | a0/a0(0) [16th,84th]  | flat(1.0) inside 1sig? | V-offset[16,84]%")
print("-"*84)
for z in [0.41, 1.0, 2.0, 3.0, 5.0]:
    vals = np.sqrt(np.array([rho_DE_ratio(z,a,b) for a,b in samp]))
    lo,med,hi = np.percentile(vals,[16,50,84])
    inside = "YES (NOT distinguishable)" if lo<=1.0<=hi else "NO  (distinguishable)"
    print(f" {z:5.2f} | {med:6.3f} [{lo:5.3f},{hi:5.3f}] | {inside:<24} | "
          f"[{Vfrac(lo):+.1f},{Vfrac(hi):+.1f}]")

# ============================================================================
#  FORECAST SNR: can a high-z BTFR sample SEE the -7%/z=3 offset?
#  intrinsic BTFR scatter ~0.025-0.03 dex in log V; signal=|Vdex| ; SNR=sqrt(N)*signal/scatter
# ============================================================================
print("\n" + "="*84)
print("FORECAST SNR for the DESI declining signal (single-redshift BTFR zero-point)")
print("="*84)
sig_logV = 0.026   # intrinsic BTFR scatter in log10 V_flat (McGaugh; ~0.025-0.03)
print(f"  intrinsic BTFR scatter assumed sigma_logV = {sig_logV} dex")
print("   z   | signal |dex| | N for 3sig | N for 5sig | SNR@N=30 | SNR@N=60")
print("-"*84)
for z in [2.0, 3.0, 5.0]:
    s = abs(Vdex(float(a0_desi(z))))
    N3 = (3.0*sig_logV/s)**2; N5 = (5.0*sig_logV/s)**2
    snr30 = np.sqrt(30)*s/sig_logV; snr60 = np.sqrt(60)*s/sig_logV
    print(f" {z:5.1f} | {s:8.4f}   |   {N3:6.0f}   |   {N5:6.0f}   |  {snr30:5.2f}   |  {snr60:5.2f}")

# multi-redshift stacked (z=3 & z=5 each N=30) vs vs flat null
print("\n  Multi-z stack (z=3 N=30 + z=5 N=30):")
s3 = abs(Vdex(float(a0_desi(3.0)))); s5 = abs(Vdex(float(a0_desi(5.0))))
chi = np.sqrt(30*(s3/sig_logV)**2 + 30*(s5/sig_logV)**2)
print(f"   combined SNR vs flat null = {chi:.2f}  (3sig needs ~{ (3/chi)**2*60 :.0f} total discs)")

print("\n" + "="*84)
print("VERLINDE (rival) is EASY to kill; DESI-vs-flat is HARD:")
print("="*84)
for z in [1.0, 2.0, 3.0]:
    sv = abs(Vdex(float(a0_verlinde(z)))); sd = abs(Vdex(float(a0_desi(z))))
    print(f"  z={z}: Verlinde |{Vfrac(float(a0_verlinde(z))):+.1f}%| vs DESI |{Vfrac(float(a0_desi(z))):+.1f}%|"
          f"   -> Verlinde signal is {sv/sd:.0f}x larger")
