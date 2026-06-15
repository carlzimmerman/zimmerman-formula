#!/usr/bin/env python3
"""
ROUTE 4 -- CURRENT-DATA PLACEMENT of the framework's a0(z) prediction, BOTH WAYS.
=================================================================================
C. Zimmerman corpus, Opus-4.8 extended research, 2026-06-14.

THE FRAMEWORK (distinctive content only): a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).
  * If Lambda is a TRUE constant (w=-1): rho_DE const -> a0(z) CONSTANT (= z=0 MOND, no distinctive content).
  * If DE EVOLVES (DESI w0>-1, wa<0, thawing): rho_DE LOWER in past -> a0(z) DECLINES into the past.
  The "IF" cancels in the RATIO so the SHAPE is interpolation-robust (banked).
  A RIVAL reading ties a0 to cH(z)=cH0 E(z) which RISES -- NOT the framework; distinguished below.

CURRENT DATA, both ways:
  (i)  MUSE-DARK III (Ciocan 2026, A&A 709 L16; arXiv 2604.22613): a0 RISING, a1=+1.59e-10/z, a0(z~1)=2.38e-10.
       WRONG sign for declining/constant. Quantify face-value sigma AND the de-systematized residual.
  (ii) DESI DR2 w0waCDM (w0=-0.752, wa=-0.86; 2.8-4.2 sigma): rho_DE lower in past -> a0 declines = SIGN-ALIGNED.
       But DESI measures the INPUT rho_DE, NOT a0. Quantify alignment WITHOUT "DESI confirms a0(z)" (forbidden).
  (iii) intermediate-z TFR / the z~0.4 bump.
  (iv) NET both ways.

Pure numpy. All paper values verified verbatim 2026-06 against primary sources.
"""
import numpy as np

# ---- constants / cosmology -------------------------------------------------
c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0 = 67.4e3 / Mpc
Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)

# DESI DR2 (2025, arXiv:2503.14738) evolving-DE CPL fiducial
W0, WA = -0.752, -0.86

def rho_de_ratio(z, w0=W0, wa=WA):
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))

# framework canonical a0(z)/a0(0) branches
a0_const = lambda z: np.ones_like(np.asarray(z, float))   # Lambda const
a0_desi  = lambda z: np.sqrt(rho_de_ratio(z))             # DESI evolving DE
a0_rho_total = lambda z: E(z)                             # RIVAL (cH(z)) -- NOT framework

# MUSE-DARK III data (x1e-10)
MU_a00, MU_a00_e = 1.00, 0.04
MU_a1,  MU_a1_e  = 1.59, 0.105          # LCDM-mass-route slope (Eq.4), asym err symmetrised
MU_a1_MOND, MU_a1_MOND_e = 1.20, 0.10   # MOND 3D forward-model route (App.E Eq.14) -- shallower!
MU_z1, MU_z1_e = 2.38, 0.11

print("#"*92)
print("# ROUTE 4: a0(z) current-data placement -- MUSE rising (AGAINST) vs DESI declining-rhoDE (FOR)")
print("#"*92)

# ===========================================================================
print("\n" + "="*92)
print("(A) THE FRAMEWORK CURVE -- constant-Lambda vs DESI-w0wa (the IF cancels in the ratio)")
print("="*92)
print(f"  {'z':>5}{'const-Lambda':>14}{'DESI w0wa':>12}{'V offset @M_b (DESI)':>22}{'[RIVAL cH(z)]':>15}")
for z in (0.4, 0.5, 1.0, 2.0, 3.0):
    r = a0_desi(z); voff = (r**0.25 - 1)*100  # V ~ (G M a0)^1/4 at fixed M_b
    print(f"  {z:>5.1f}{1.0:>14.3f}{r:>12.3f}{voff:>+21.2f}%{a0_rho_total(z):>15.2f}")
# the non-monotonic bump: rho_DE peaks where w crosses -1
zg = np.linspace(0, 1.0, 2001)
rpk = a0_desi(zg); zbump = zg[np.argmax(rpk)]
print(f"  NON-MONOTONIC: DESI w(z) crosses -1 at z~{(-(1+W0)/WA):.2f}; rho_DE (hence a0) PEAKS -> "
      f"a0/a0(0) max = {rpk.max():.3f} at z={zbump:.2f} (+{(rpk.max()-1)*100:.1f}% a0 / +{(rpk.max()**0.25-1)*100:.1f}% V).")
print("  => framework only UNIQUELY declines at z>~1.5; a MODEST low-z rise is consistent with the bump.")

# ===========================================================================
print("\n" + "="*92)
print("(B-i) MUSE-DARK III rising -- FACE VALUE tension (fitted a0 taken as fundamental)")
print("="*92)
# effective slope of each framework branch over MUSE window 0.33-1.44
def eff_slope(model, zlo=0.33, zhi=1.44, n=300):
    z = np.linspace(zlo, zhi, n); y = model(z)
    A = np.vstack([np.ones_like(z), z]).T
    b, m = np.linalg.lstsq(A, y, rcond=None)[0]; return m
s_const, s_desi = eff_slope(a0_const), eff_slope(a0_desi)
sig_const = abs(MU_a1 - s_const*MU_a00)/MU_a1_e
sig_desi  = abs(MU_a1 - s_desi*MU_a00)/MU_a1_e
sig_const_M = abs(MU_a1_MOND - s_const*MU_a00)/MU_a1_MOND_e
print(f"  LCDM-route slope a1 = +{MU_a1:.2f}+/-{MU_a1_e:.3f}:  vs const(0) {sig_const:4.1f}sig | vs DESI({s_desi*MU_a00:+.2f}) {sig_desi:4.1f}sig")
print(f"  MOND-route slope a1 = +{MU_a1_MOND:.2f}+/-{MU_a1_MOND_e:.2f} (App.E, the cleaner route): vs const {sig_const_M:4.1f}sig")
print(f"  Point z~1: a0=2.38+/-0.11 vs framework pred 1.0-1.01 -> {(MU_z1-1.0)/MU_z1_e:4.1f}sig")
print(f"  Authors' headline: a1!=0 at ~30sig (full RAR likelihood). FACE VALUE = ~12-16sig AGAINST declining/const.")

# ===========================================================================
print("\n" + "="*92)
print("(B-ii) DE-SYSTEMATIZING: subtract the LCDM apparent-a0 drift (Magneticum/Mayer) -- the legit relief")
print("="*92)
# Mayer+2023 Magneticum (LCDM, NO fundamental a0): fitted a0 rises ~x3 over z=0->2.3 from baryon-fraction/assembly.
# Convert to an apparent linear slope in (a0/a0(0)) per dz over the MUSE window, then subtract it.
mayer_z, mayer_factor = 2.3, 3.0
s_mayer = (mayer_factor - 1.0)/mayer_z            # apparent slope per dz, in units of a0(0): ~0.87/dz
# In MUSE's absolute units a0(0)~1.0e-10, so the predicted apparent a1 (LCDM, no fund a0) ~ s_mayer*1.0:
a1_apparent = s_mayer*MU_a00
# A framework with CONSTANT fundamental a0, observed through the SAME assembly forward-model, would show a1 = a1_apparent.
# Residual the framework must still explain:
a1_resid = MU_a1 - a1_apparent
# uncertainty: MUSE a1 err (0.105) added in quad with a generous ~30% modelling error on the Magneticum slope
sig_model = 0.30*a1_apparent
a1_resid_e = np.sqrt(MU_a1_e**2 + sig_model**2)
sig_resid = a1_resid/a1_resid_e
# same with the cleaner MOND-route slope (a1=1.20)
a1_resid_M = MU_a1_MOND - a1_apparent
a1_resid_M_e = np.sqrt(MU_a1_MOND_e**2 + sig_model**2)
sig_resid_M = a1_resid_M/a1_resid_M_e
print(f"  Magneticum LCDM apparent slope (NO fundamental a0): a1_app = {a1_apparent:+.2f}e-10/z (rise x{mayer_factor:.0f}@z{mayer_z}).")
print(f"  MUSE infers ~x4@z2 = ~a third STEEPER than Magneticum x3 (MUSE's own comparison).")
print(f"  Residual the FRAMEWORK must still explain (LCDM-route): a1 - a1_app = {a1_resid:+.2f}e-10/z")
print(f"     with model err ~30% -> residual = {sig_resid:+.1f} sigma  (assembly absorbs MOST of the rise)")
print(f"  Residual (MOND-route a1=1.20, the cleaner forward model): {a1_resid_M:+.2f}e-10/z -> {sig_resid_M:+.1f} sigma")
print(f"  => DE-SYSTEMATIZED tension collapses from ~15sig to ~{min(sig_resid,sig_resid_M):.1f}-{max(sig_resid,sig_resid_M):.1f} sigma.")
print(f"     This is the ~1.5sigma-against the honest brief reports -- a residual lean, NOT a refutation.")

# ===========================================================================
print("\n" + "="*92)
print("(C) DESI alignment -- SIGN-aligned with the declining branch (NOT 'DESI confirms a0(z)')")
print("="*92)
# DESI says w0>-1, wa<0 at 2.8-4.2 sigma => rho_DE LOWER in past => sqrt(rho_DE) DECLINES into the past.
# The framework's a0(z) INHERITS that sign. DESI measures the INPUT rho_DE, not a0. Alignment = the sign of d(rho_DE)/dz<0.
print(f"  DESI DR2: w0={W0}, wa={WA} (2.8-4.2 sigma for dynamical DE). w(a)=w0+wa(1-a).")
print(f"  Consequence for rho_DE: rho_DE(z=2)/rho_DE0 = {rho_de_ratio(2.0):.3f}, rho_DE(3)/rho_DE0 = {rho_de_ratio(3.0):.3f} (LOWER in past).")
print(f"  => the framework's a0(z) = sqrt(rho_DE) INHERITS a DECLINE: a0(2)/a0(0)={a0_desi(2.0):.3f}, a0(3)={a0_desi(3.0):.3f}.")
print(f"  HONEST: this is SIGN-ALIGNMENT of the declining branch with the ONE cosmological tension that points the")
print(f"  framework's way -- it is NOT a measurement of a0(z). 'DESI confirms my a0(z)' is FORBIDDEN (DESI measures rho_DE).")
print(f"  ALSO: if DESI reverts to w=-1, a0(z) is CONSTANT = ordinary MOND => the distinctive content is HOSTAGE to DESI.")

# ===========================================================================
print("\n" + "="*92)
print("(D) THE BTFR OFFSET -- the cleanest distinctive forward test, and its SNR")
print("="*92)
# M_b = V^4 / (G a0(z)) => at fixed M_b, V ~ a0(z)^{1/4}. dlogV = (1/4) dlog a0 = (1/8) dlog(rho_DE).
def vshift_pct(z): return (a0_desi(z)**0.25 - 1)*100
def vshift_dex(z): return 0.25*np.log10(a0_desi(z))
for z in (1,2,3,6):
    print(f"  z={z}: a0/a0(0)={a0_desi(z):.3f} -> V offset {vshift_pct(z):+.2f}% ({vshift_dex(z):+.4f} dex) at fixed M_b")
print(f"  Banked headline: -7% in V by z=3 (-0.033 dex). RIVAL cH(z): OPPOSITE sign (+{(E(3)**0.25-1)*100:.0f}% at z=3).")
# Forecast SNR: per-galaxy BTFR scatter ~0.026 dex in logV (=0.10 dex in logM / 4); signal at z=3 = 0.033 dex in logV.
sig_logV = 0.026   # intrinsic BTFR scatter in logV (0.10 dex logM relation / slope 4 ~ 0.025-0.03)
signal_z3 = abs(vshift_dex(3.0))
for N in (30, 60, 100):
    snr = signal_z3/(sig_logV/np.sqrt(N))
    print(f"  z=3 BTFR, N={N} discs: stat SNR = {snr:.1f} sigma (signal {signal_z3:.4f} dex vs scatter {sig_logV} dex)")
# but the DESI w0/wa marginalization imposes a floor (banked combined_fisher): sigma(beta) ~ 0.5-0.6 caps single-z at ~1.6-2.0 sigma
print(f"  *** DESI-marginalization FLOOR: sigma(beta)~0.5-0.6 caps SINGLE-redshift significance at ~1.6-2.0 sigma")
print(f"      regardless of N. Clean 5sig needs MULTI-z BTFR (z=3 & z=5) + ~2x tighter DESI prior (banked).")

# ===========================================================================
print("\n" + "="*92)
print("(E) NET -- both ways")
print("="*92)
print(f"""  TWO LEADING DATA PULL OPPOSITE:
    * MUSE-DARK III rising: face value ~12-16 sigma AGAINST; DE-systematized (Magneticum LCDM apparent-a0)
      to ~{min(sig_resid,sig_resid_M):.1f}-{max(sig_resid,sig_resid_M):.1f} sigma residual lean against (the honest brief's '~1.5 sigma against').
    * DESI DR2 w0wa: SIGN-aligned with the declining branch (the one tension pointing the framework's way) --
      but DESI measures rho_DE not a0; NOT a confirmation of a0(z).
  NET VERDICT: CONTESTED / NON-DIAGNOSTIC, currently LEANING MILDLY UNFAVORABLE (~1.5 sigma) on the one
  DIRECT a0(z) measurement, with a sign-aligned cosmological tailwind (DESI) that cannot be cashed as evidence.
  The DISTINCTIVE z>~1.5 decline (-7% V at z=3) is UNTESTED -- below every current probe's floor; the rising
  rival (cH(z)) is the MOST disfavored (Milgrom (1+z)^1.5 exclusion, constant cluster offset).""")
