#!/usr/bin/env python3
"""
SETUP B: THE OBSERVED CONSTRAINT.
How tightly do the weak-LENSING RAR and the DYNAMICAL RAR agree, and how much
lensing-dynamical OFFSET would current data allow before excluding it?

Sources (arXiv IDs, quoted vs inferred flagged inline):
  Brouwer et al. 2021, A&A 650 A113, arXiv:2106.11677 (KiDS-1000 / KiDS-bright + GAMA lensing RAR)
  Mistele, McGaugh, Lelli, Schombert, Li 2024, arXiv:2310.15248 (KiDS lensing RAR to ~2.5 dex deeper)
  Reference dynamical RAR: McGaugh, Lelli, Schombert 2016 (M16), SPARC, a0 = 1.20e-10 m/s^2.

This script does NOT re-derive; it assembles the observed agreement into a single
"how large an offset survives" budget, both for a MULTIPLICATIVE lensing-vs-dynamics
mass ratio and in dex, at the framework's a0 forks.
"""
import numpy as np

print("="*74)
print("OBSERVED LENSING = DYNAMICS RAR CONSISTENCY  (Brouwer+2021, Mistele-McGaugh24)")
print("="*74)

# ---------------------------------------------------------------------------
# 1. THE OVERLAP: lensing rotation curves continue SPARC dynamical curves.
# ---------------------------------------------------------------------------
# QUOTED, Brouwer+2021 Sec 5.1 (p.12): the SIS-vs-PPL conversion-method systematic
# on g_obs is <log(g_obs,SIS/g_obs,PPL)> = 0.038 dex  (methodology floor, not physics).
conv_method_dex = 0.038
# QUOTED, Brouwer+2021 Sec 4.4 / Sec 5.1: an extra 0.1 dex added to ALL RAR error
# bars for the ESD->RAR conversion uncertainty.
esd_to_rar_dex = 0.10
# QUOTED, Mistele-McGaugh24 Table 1: per-bin STATISTICAL uncertainty 0.05-0.12 dex;
# systematics <0.07 dex except lowest-g bins.
mm24_stat_dex = np.array([0.05, 0.12])
print("\n[1] OVERLAP / CONTINUITY")
print("  Brouwer Sec5.1 (QUOTED): SPARC dynamical rotation curves and lensing")
print("  rotation curves 'correspond remarkably' at the overlap r ~ 30 h70^-1 kpc;")
print("  'two fully independent RAR observations ... in strong agreement'.")
print("  Mistele-McGaugh24 (QUOTED): lensing 'smoothly continues' the kinematic RAR")
print("  by ~2.5 dex, down to log10(g_bar) ~ -14.86  (g_bar ~ 1e-15 m/s^2).")
print(f"  Conversion-method floor  : {conv_method_dex:.3f} dex (SIS vs PPL, QUOTED)")
print(f"  ESD->RAR error added     : {esd_to_rar_dex:.3f} dex (QUOTED)")
print(f"  M-M24 per-bin stat error : {mm24_stat_dex[0]:.2f}-{mm24_stat_dex[1]:.2f} dex (QUOTED)")

# ---------------------------------------------------------------------------
# 2. THE QUANTIFIED AGREEMENT WITH THE DEEP-MOND (a0) TRACK.
# ---------------------------------------------------------------------------
# QUOTED, Brouwer+2021 Sec 5.2 (p.15): chi^2_red vs MOND(M16,a0=1.2e-10)/EG.
#   GAMA spectroscopic lensing (the clean sample):   chi2_red = 0.8  (~0.4 sigma)
#   KiDS-bright:                                      chi2_red = 4.6 (MOND), 5.0 (EG)  ~6 sigma high
#   KiDS-bright, after z-systematics (R<3 Mpc cut):   chi2_red = 4.0 / 4.4            ~3.8 sigma
#   KiDS-bright, with dM* = +0.2 dex (within syst.):  chi2_red = 1.5 (MOND)           GOOD
#   KiDS-bright, with dM* = -0.2 dex:                 chi2_red = 14                   BAD
# Ndof = 15 gbar-bins.
Ndof = 15
chi2 = {
 "GAMA lensing vs MOND"          : 0.8,
 "GAMA lensing vs EG"            : 0.8,
 "KiDS-bright vs MOND"           : 4.6,
 "KiDS-bright vs EG"            : 5.0,
 "KiDS-bright (z-corr) vs MOND"  : 4.0,
 "KiDS-bright, dM*=+0.2, vs MOND": 1.5,
 "KiDS-bright, dM*=-0.2, vs MOND": 14.0,
}
print("\n[2] QUANTIFIED AGREEMENT WITH THE a0 DEEP-MOND TRACK (chi2_red, Ndof=15; QUOTED)")
for k, v in chi2.items():
    # sigma-equivalent of a reduced chi2 with Ndof dof
    from math import sqrt
    sig = (v - 1.0) * sqrt(Ndof / 2.0)   # ~ (chi2_red-1)*sqrt(Ndof/2)
    flag = "GOOD" if v < 1.6 else ("~"+f"{sig:.1f}sigma high")
    print(f"    {k:36s}: {v:5.2f}   {flag}")
print("  => GAMA (clean, spectroscopic) lensing is a 0.4-sigma MATCH to the a0 track.")
print("  => KiDS-bright's ~0.1-0.2 dex EXCESS above the track is ABSORBED by the")
print("     +0.2 dex stellar-mass systematic (chi2_red 4.6 -> 1.5). i.e. the offset")
print("     the data 'see' is a BARYONIC-side (g_bar / M*) systematic, not a real")
print("     lensing-vs-dynamics disagreement.")

# ---------------------------------------------------------------------------
# 3. THE OFFSET BUDGET: how large a lensing-vs-dynamics OFFSET survives?
# ---------------------------------------------------------------------------
# The observable is a VERTICAL offset in g_obs at fixed g_bar between the two
# probes. A lensing mass that is a factor f times the dynamical (MI) mass shifts
# g_obs by log10(f) in the deep-MOND regime g_obs ~ sqrt(g_bar*a0) IF the offset
# is a mass rescaling... but note: photons see the FULL enclosed mass, so a lensing
# excess M_L = f_M * M_dyn maps to g_obs,L = f_M * g_obs,dyn (linear, not sqrt),
# hence a dex offset delta = log10(f_M).
#
# Tightest clean constraint = GAMA's 0.4-sigma agreement over 15 bins with the
# a0 track, plus the ESD conversion floor. Take the allowed 1-sigma band as the
# quadrature of (per-bin stat) and (conversion), and the ensemble (15-bin) pull.
per_bin = 0.12                       # representative per-bin 1-sigma (dex)
ensemble = per_bin / np.sqrt(Ndof)   # if offset is COHERENT across all bins
budget_1sig_coherent = np.sqrt(ensemble**2 + conv_method_dex**2)
budget_1sig_perbin   = np.sqrt(per_bin**2 + esd_to_rar_dex**2)
print("\n[3] LENSING-vs-DYNAMICS OFFSET BUDGET  (delta = log10(M_lens/M_dyn), dex)")
print(f"    coherent (all-15-bin) 1-sigma allowance : {budget_1sig_coherent:.3f} dex")
print(f"       -> multiplicative mass ratio 1-sigma : {10**budget_1sig_coherent:.3f}  (i.e. +/-{100*(10**budget_1sig_coherent-1):.0f}%)")
print(f"    per-bin 1-sigma allowance (incl ESD)    : {budget_1sig_perbin:.3f} dex")
print(f"       -> multiplicative mass ratio 1-sigma : {10**budget_1sig_perbin:.3f}")
# 2-sigma (exclusion-ish) coherent bound:
excl = 2*budget_1sig_coherent
print(f"    ~2-sigma coherent EXCLUSION threshold   : {excl:.3f} dex  (ratio {10**excl:.2f})")
print("    NOTE: this clean ~0.05 dex coherent bound assumes the g_bar (baryon)")
print("    axis is FIXED. Brouwer's DOMINANT real-world systematic is g_bar itself")
print("    (missing baryons / hot gas up to x3 at large R; +/-0.2 dex M*), which")
print("    inflates the honest offset that current data tolerate to ~0.2-0.3 dex.")

# ---------------------------------------------------------------------------
# 4. THE FRAMEWORK'S a0 FORKS vs the lensing-preferred a0.
# ---------------------------------------------------------------------------
a0_lensing   = 1.20e-10   # QUOTED M16/SPARC value used by both lensing papers (1.20-1.24e-10)
a0_canonical = 9.36e-11   # framework canonical: cH_Lambda/Z, rho_DE
a0_alt       = 1.13e-10   # framework alt: rho_total / cH0
print("\n[4] a0 FORKS vs lensing-preferred a0 = 1.20e-10 m/s^2 (M16, QUOTED)")
for name, a0 in [("canonical cH_Lambda/Z (rho_DE)", a0_canonical), ("alt rho_total/cH0", a0_alt)]:
    # deep-MOND g_obs ~ sqrt(g_bar*a0): a fractional a0 shift -> HALF that in g_obs (dex)
    dex_shift = 0.5*np.log10(a0/a0_lensing)
    print(f"    {name:34s} a0={a0:.3e}  =>  deep-MOND g_obs shift {dex_shift:+.3f} dex")
print("    Both forks shift the a0 TRACK by <~0.05 dex in g_obs -- SMALLER than the")
print("    lensing scatter/systematic floor. The lensing RAR is a0-degenerate at this")
print("    level: it does NOT discriminate 9.36e-11 from 1.20e-10 (consistent with")
print("    the dynamical-RAR non-diagnosticity already on record).")

print("\n" + "="*74)
print("BOTTOM LINE (observed constraint the framework must match):")
print("  Lensing RAR = dynamical RAR to ~0.05 dex (clean GAMA, coherent) / ~0.1-0.2")
print("  dex per bin, over ~2.5 dex extra in g_bar down to ~1e-15 m/s^2, at a shared")
print("  a0 ~ 1.2e-10. A COHERENT lensing-vs-dynamics mass offset > ~0.1 dex (factor")
print("  ~1.3) is excluded by the clean sample; the honest budget once the g_bar")
print("  (baryon) systematic is folded in is ~0.2-0.3 dex. Any MI theory must deliver")
print("  a lensing (real-mass) excess = the MI dynamical excess to WITHIN this ~0.1-0.3")
print("  dex, with NO room for a large offset.")
print("="*74)
