#!/usr/bin/env python3
"""
SCOUT C: systematic floor on the high-z BTFR *offset* (dex), vs the framework's
predicted BRANCH-A signal of -0.033 dex in v (discs BELOW the z=0 BTFR).

Convention (stated by orchestrator):
  at fixed M_b:  dlog10(v) = (1/4) log10(a0(z)/a0(0))
  BRANCH A a0(3)/a0(0)=0.737 -> dlog10(v) = 0.25*log10(0.737) = -0.0331 dex.

The BTFR offset is measured as an offset in log10(v) at fixed M_b (or equivalently
-4x the M_b offset at fixed v). Each systematic below is expressed as its effect on
the *inferred* log10(v) offset relative to a perfectly-corrected local disc:
  - a POSITIVE number here means the effect pushes the inferred disc ABOVE the z=0 BTFR
  - a NEGATIVE number means it pushes the disc BELOW the z=0 BTFR
(so it can be compared directly, sign and all, to the -0.033 dex Branch-A prediction).

All input numbers are representative literature values (z~2-2.5 cosmic-noon discs):
  sigma0 ~ 40-60 km/s (Ubler+2017, Genzel+2017, Wisnioski+2015)
  v_rot ~ 150-220 km/s for the massive TFR discs
  v/sigma ~ 2-5 (rotation-dominated after selection); dispersion-dominated tail v/sigma~1-2
"""
import numpy as np

log10 = np.log10

# ---- reference disc (massive cosmic-noon rotator on the TFR) ----
v_rot = 180.0     # km/s, observed (projection-corrected) rotation velocity at R_out
sigma0 = 50.0     # km/s, intrinsic velocity dispersion (Ubler+2017 median ~ 40-60)
# Burkert+2010 exponential-disk AD: v_circ^2 = v_rot^2 + 2*(R/Rd)*sigma0^2 ; at R=2.2Rd -> factor ~ 2*2.2
# Simpler isotropic-turbulence form used widely: v_circ^2 = v_rot^2 + 3.35*(R/Rd)*sigma0^2 (Burkert2010)
# and a common floor v_circ^2 = v_rot^2 + 3*sigma0^2 (isotropic). We bracket with both.

def dex_offset_from_vcorr(v_obs, v_corr):
    """offset in log10(v) that IGNORING the correction introduces.
    If a study reports v_obs but the *true* circular speed is v_corr>v_obs,
    then plotting v_obs puts the disc LOW by log10(v_obs/v_corr) (<0)."""
    return log10(v_obs / v_corr)

print("="*70)
print("REFERENCE DISC: v_rot=%.0f, sigma0=%.0f km/s (v/sigma=%.1f)"%(v_rot,sigma0,v_rot/sigma0))
print("="*70)

# ---------- (2) PRESSURE SUPPORT / ASYMMETRIC DRIFT ----------
# If a study does NOT apply AD correction, it plots v_rot instead of v_circ.
# v_circ > v_rot, so the UNCORRECTED disc sits BELOW the true relation (negative offset).
# Bracket the correction size:
vcirc_iso3   = np.sqrt(v_rot**2 + 3.0*sigma0**2)       # v_c^2=v_rot^2+3 sigma^2
vcirc_burk22 = np.sqrt(v_rot**2 + 2*2.2*sigma0**2)     # exp disk at R=2.2Rd
vcirc_burk34 = np.sqrt(v_rot**2 + 3.35*2.2*sigma0**2)  # Burkert2010 outer disk (steep)
ad_iso  = dex_offset_from_vcorr(v_rot, vcirc_iso3)
ad_b22  = dex_offset_from_vcorr(v_rot, vcirc_burk22)
ad_b34  = dex_offset_from_vcorr(v_rot, vcirc_burk34)
print("\n(2) ASYMMETRIC DRIFT (if uncorrected, disc plots at v_rot < v_circ):")
print("    v_circ (iso 3sig)  =%.1f -> offset %+.4f dex"%(vcirc_iso3, ad_iso))
print("    v_circ (Burk 2.2)  =%.1f -> offset %+.4f dex"%(vcirc_burk22, ad_b22))
print("    v_circ (Burk 3.35) =%.1f -> offset %+.4f dex"%(vcirc_burk34, ad_b34))
# dispersion-dominated tail sigma/v~0.3-0.5 (i.e. v/sigma 2-3.3): worst case
for vs in [0.3,0.4,0.5]:
    sig = vs*v_rot
    vc = np.sqrt(v_rot**2+3*sig**2)
    print("    sigma/v=%.1f (sig=%.0f): iso-3 offset %+.4f dex"%(vs,sig,dex_offset_from_vcorr(v_rot,vc)))
# residual AFTER a correction is applied: correction itself uncertain at ~30-50%
resid_ad = 0.4*abs(ad_iso)   # ~40% residual on a ~0.06-0.10 dex correction
print("    => magnitude of correction ~0.04-0.10 dex; RESIDUAL after correction ~%.3f dex"%resid_ad)
print("    DIRECTION: uncorrected -> BELOW; over-correction -> ABOVE. Dominant risk: BELOW.")

# ---------- (1) BEAM SMEARING ----------
# Beam smearing lowers peak v_rot and raises sigma. Literature: >=0.1 dex on v for
# marginally-resolved sources (Ubler+2017), translating to >=0.4 dex in M_*.
# For WELL-resolved AO/forward-modelled discs the residual is smaller, ~0.02-0.05 dex.
# Direction: SUPPRESSES v -> disc artificially BELOW.
bs_worst = -0.10   # marginally resolved, uncorrected
bs_resid = -0.03   # residual after forward-model correction (well-resolved)
print("\n(1) BEAM SMEARING: lowers v -> BELOW.")
print("    uncorrected/marginal: %+.3f dex ; residual after forward-model: %+.3f dex"%(bs_worst,bs_resid))

# ---------- (3) INCLINATION ----------
# v_deproj = v_obs/sin(i). A random inclination error delta_i propagates as
# d ln v = -cot(i) di. Typical delta_i ~ 5-10 deg.
def incl_dex(i_deg, di_deg):
    i=np.radians(i_deg); di=np.radians(di_deg)
    dlnv = (1.0/np.tan(i))*di     # magnitude
    return dlnv/np.log(10)
print("\n(3) INCLINATION (v=v_obs/sin i): random scatter, ~symmetric, but low-i biases high")
for i in [40,50,60,70]:
    print("    i=%d, di=7deg -> +/-%.3f dex"%(i, incl_dex(i,7)))
incl_sys = incl_dex(55,7)  # representative random per-galaxy; averages down in a mean offset
print("    per-galaxy ~%.3f dex; DIRECTION: random (scatter), small net bias unless i mis-est."%incl_sys)

# ---------- (4) STELLAR MASS IMF/SED ----------
# M_* systematic ~0.2-0.3 dex (IMF choice ~0.25 dex; SED/SFH ~0.1-0.2). On the BTFR
# this enters M_b; converted to the v-axis offset it is /4 (since dlogM_b=-4 dlogv? no:
# BTFR M_b prop v^4 so a dlogM_b shifts the horizontal position; the vertical(v) offset
# at fixed M_b = (1/4) dlogM_b ). A 0.25 dex M_* error where M_* dominates M_b -> ~0.06 dex in v.
# For gas-rich cosmic-noon discs M_gas can dominate, diluting the stellar effect.
mstar_dex = 0.25
f_star = 0.5   # fraction of M_b that is stars (gas-rich at z~2, ~0.3-0.6)
mb_from_star = mstar_dex*f_star
v_from_mstar = mb_from_star/4.0
print("\n(4) STELLAR MASS IMF/SED: M_* sys ~%.2f dex, f_*~%.1f -> M_b %.3f -> v-offset %.3f dex"
      %(mstar_dex,f_star,mb_from_star,v_from_mstar))
print("    DIRECTION: random/systematic-per-calibration; can push either way (mostly a zero-point).")

# ---------- (5) GAS MASS / alpha_CO ----------
# M_gas from CO (alpha_CO factor ~2-4x, ~0.3 dex) or [CII]/scaling (~0.3 dex). Gas can
# dominate M_b at z~2 (f_gas 0.3-0.7). A 0.3 dex M_gas error with f_gas~0.5 -> ~0.15 dex M_b
# -> /4 -> ~0.04 dex in v. alpha_CO metallicity trend can be SYSTEMATIC (low-Z high-z ->
# higher alpha_CO -> MORE gas -> M_b UP -> disc plots ABOVE at fixed v; i.e. mimics Branch B).
mgas_dex = 0.30
f_gas = 0.5
mb_from_gas = mgas_dex*f_gas
v_from_gas = mb_from_gas/4.0
print("\n(5) GAS MASS/alpha_CO: M_gas sys ~%.2f dex, f_gas~%.1f -> M_b %.3f -> v-offset %.3f dex"
      %(mgas_dex,f_gas,mb_from_gas,v_from_gas))
print("    DIRECTION: metallicity-driven alpha_CO underestimate -> M_b LOW -> disc BELOW;")
print("    but if high-z alpha_CO higher -> M_b HIGH -> disc ABOVE. Net: sign-ambiguous, ~0.04 dex.")

# ---------- NET FLOOR ----------
print("\n"+"="*70)
print("NET SYSTEMATIC FLOOR (quadrature of RESIDUALS after standard corrections):")
comps = {
    'beam_smear_resid': 0.03,
    'asym_drift_resid': resid_ad,       # ~0.03
    'inclination':      0.015,          # net after averaging many discs in a mean offset
    'Mstar_IMF':        v_from_mstar,   # ~0.03
    'gas_alphaCO':      v_from_gas,     # ~0.04
}
for k,v in comps.items(): print("   %-18s %.3f dex"%(k,v))
net = np.sqrt(sum(x**2 for x in comps.values()))
print("   ---------------------------------")
print("   NET (quadrature)  = %.3f dex"%net)

# worst-case coherent (all AD+beam push BELOW, uncorrected):
worst_below = abs(bs_worst)+abs(ad_iso)
print("   WORST-CASE coherent BELOW (uncorrected beam+AD) = %.3f dex"%worst_below)

print("\nFRAMEWORK BRANCH-A SIGNAL = -0.033 dex")
print("Detectable above floor? signal/floor = %.2f"%(0.033/net))
print("="*70)
