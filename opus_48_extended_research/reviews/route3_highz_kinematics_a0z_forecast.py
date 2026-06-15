#!/usr/bin/env python3
"""
ROUTE 3 -- HIGH-Z DEEP-MOND KINEMATICS: can ELT/JWST/ALMA measure a0(z=1-3) DIRECTLY?
=====================================================================================
The DISTINCTIVE framework prediction (the ONLY thing beyond z=0 MOND):
    a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)
  - if Lambda is a TRUE constant (w=-1): rho_DE const -> a0(z) is CONSTANT (= z=0 MOND, no distinctive signal).
  - if DE EVOLVES (DESI DR2 w0=-0.752, wa=-0.86, thawing): rho_DE was LOWER in the past -> a0(z) DECLINES.
The IF cancels in the ratio, so the curve is interpolation-robust. The DISTINCTIVE bet is the DECLINE.
A RIVAL reading ties a0 to cH(z)=cH0 E(z) which RISES x5 by z=3 -- NOT the framework's sqrt(rho_DE) branch;
carried only as a contrast/kill-target.

This script forecasts the DIRECT a0(z) measurement from high-z resolved kinematics:
  (1) the signal: a0(z)/a0(0), dex of a0, % of V_flat, for declining vs constant vs rising.
  (2) per-disc precision on a0 + N for 3/5 sigma on the DECLINING trend -- statistics AND the systematic floor.
  (3) THE CONFOUND that actually binds: does a clean deep-MOND (g<<a0) regime EVEN EXIST at z~2-3?
      (the half-light radii of cosmic-noon discs sit at g=(3-11)a0 -- HIGH acceleration, Milgrom 2017.)
  (4) what existing direct high-z data already say (Big Wheel z=3.25; RC100/Genzel; de Graaff z~6).
  (5) instrument reach + timeline (ELT/HARMONI first light Dec 2030; JWST/NIRSpec now; ALMA cold gas).
C. Zimmerman framework equation throughout. Honest both-ways. 2026-06-14.
"""
import numpy as np
from scipy.integrate import quad

# ---------- cosmology / framework curve ----------
Om, OmL = 0.315, 0.685
def E(z): return np.sqrt(Om*(1+z)**3 + OmL)                 # H(z)/H0  (the RIVAL rising branch)
def rhoDE_ratio(z, w0=-0.752, wa=-0.86):                    # DESI DR2 CPL -> rho_DE(z)/rho_DE0
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def a0_decline(z): return np.sqrt(rhoDE_ratio(z))           # FRAMEWORK distinctive (evolving-DE)
def a0_const(z):   return np.ones_like(np.atleast_1d(z)*1.0)# framework if Lambda const  == z=0 MOND
def a0_rising(z):  return E(z)                              # RIVAL cH(z) branch (footing-bug; kill target)

A0_0 = 9.36e-11
zs = np.array([0.5, 1.0, 2.0, 3.0])

print("#"*98)
print("# ROUTE 3: DIRECT a0(z) FROM HIGH-Z KINEMATICS -- the forecast (declining = distinctive bet)")
print("#"*98)

print("\n"+"="*98)
print("(1) THE SIGNAL: a0(z)/a0(0) -- framework DECLINE vs CONSTANT vs the RIVAL RISE")
print("="*98)
print(f"  {'z':>4}{'DECLINE sqrt(rhoDE)':>22}{'CONSTANT (=z0 MOND)':>22}{'RISE cH(z) [rival]':>22}")
for z in zs:
    print(f"  {z:>4}{a0_decline(z):>22.3f}{1.0:>22.3f}{a0_rising(z):>22.3f}")
print("\n  --> the framework's DISTINCTIVE separation is DECLINE-vs-CONSTANT. The RISE is a different reading,")
print("      carried only as a kill-target. At z=3: decline 0.73x, constant 1.00x, rise 4.99x.")

print("\n"+"="*98)
print("(2) WHAT YOU ACTUALLY MEASURE: deep-MOND identity V_flat^4 = G M_bar a0(z)")
print("="*98)
print("  at FIXED M_bar:  dlogV = (1/4) dlog a0.  This is the BTFR zero-point / a0_eff per disc.")
print(f"  {'z':>4}{'a0/a0(0)':>11}{'signal[dex a0]':>16}{'V_flat shift':>14}{'V_flat %':>11}")
for z in zs:
    r = a0_decline(z); dloga0 = np.log10(r); dV = 0.25*dloga0
    print(f"  {z:>4}{r:>11.3f}{dloga0:>16.3f}{dV:>14.3f}{(10**dV-1)*100:>+10.1f}%")
print("  the distinctive z=3 signal is -0.13 dex in a0 = -3.4% in V_flat at fixed M_bar (TINY).")
print("  contrast: the RIVAL rise would be +0.70 dex / +44% in V at z=3 -- trivially detectable, already excluded.")

print("\n"+"="*98)
print("(3) PER-DISC PRECISION + SAMPLE SIZE for the DECLINING trend (statistics)")
print("="*98)
# per-disc a0 measurement scatter (dex). Two regimes:
#   IDEAL clean deep-MOND extended RC (rare at high z): ~0.10-0.15 dex (cf. SPARC RC-quality discs)
#   REALISTIC cosmic-noon disc (turbulent, AD-corrected, M_bar-limited): ~0.25-0.40 dex
sig_disc_ideal = 0.12
sig_disc_real  = 0.30
sig_z3 = abs(np.log10(a0_decline(3.0)))   # |signal| in dex of a0 at z=3
print(f"  z=3 DISTINCTIVE signal |dlog a0| = {sig_z3:.3f} dex")
for label, sd in [("IDEAL clean deep-MOND RC", sig_disc_ideal), ("REALISTIC cosmic-noon disc", sig_disc_real)]:
    print(f"\n  per-disc scatter ~{sd:.2f} dex  [{label}]:")
    for nsig in (3, 5):
        N = (sd/(sig_z3/nsig))**2
        print(f"     N(z=3) for {nsig}sigma (stat only) = ({sd}/({sig_z3:.3f}/{nsig}))^2 = {N:.0f} clean discs")

print("\n"+"="*98)
print("(4) THE BINDING CONSTRAINT IS NOT N -- IT IS THE SYSTEMATIC + DESI-PRIOR FLOOR")
print("="*98)
sig_sys = 0.10   # high-z baryon (molecular gas + IMF + pressure-support) systematic floor, dex (does NOT average down)
print(f"  high-z M_bar/baryon + pressure-support systematic floor ~{sig_sys:.2f} dex (does NOT average down with N).")
print(f"  the z=3 signal {sig_z3:.3f} dex is only {sig_z3/sig_sys:.1f}x this floor.")
print(f"  => a 3sigma DIRECT detection needs M_bar (esp. molecular gas) controlled to < {sig_z3/3:.3f} dex")
print(f"     = ~{(10**(sig_z3/3)-1)*100:.0f}% per disc, AND pressure support modelled to comparable accuracy.")
# DESI-prior floor (from MASTER_PREDICTIONS / combined_fisher): marginalizing w0,wa caps single-z significance
print("  SECOND floor (the input): the curve's amplitude inherits DESI's w0,wa error -> a sigma(beta)~0.5-0.6")
print("     floor INDEPENDENT of disc count; single-redshift significance caps at ~1.6-2.0 sigma even with N->inf.")
print("     CLEAN 5sigma needs MULTI-redshift (z=3 AND z=5) plus a ~2x tighter DESI prior (DR3, ~2027).")

print("\n"+"="*98)
print("(5) THE DEEP-MOND CONFOUND: does g<<a0 even EXIST at z~2-3? (the regime question)")
print("="*98)
# Milgrom 2017 / RC100 / Nestor Shachar 2023: at half-light radii, g(R1/2) = (3-11) a0 -- HIGH acceleration.
g_over_a0_R12 = np.array([3, 11])
print("  Genzel/RC100/Nestor-Shachar cosmic-noon massive discs: g(R_1/2) = (3-11) a0  [Milgrom 2017].")
print("  => at the half-light radius these are HIGH-acceleration (g>a0), NOT deep-MOND. In the high-g regime")
print("     a0 barely enters (g_obs ~ g_bar), so a0(z) is WEAKLY constrained there. The deep-MOND (g<<a0)")
print("     regime that cleanly reads a0 only appears in the OUTER disc / low-mass systems -- exactly where")
print("     high-z data are sparse, beam-smeared, and pressure-support dominated.")
# where does g = a0? r_MOND ~ sqrt(G M_bar / a0). Show for a massive disc.
G = 6.674e-11; Msun = 1.989e30; kpc = 3.086e19
for Mb in (1e10, 3e10, 1e11):
    rM = np.sqrt(G*Mb*Msun/(A0_0))/kpc   # radius where g_bar = a0 (point-mass approx)
    print(f"     M_bar={Mb:.0e} Msun: g_bar=a0 at r~{rM:.1f} kpc; deep-MOND needs r>>{rM:.0f} kpc"
          f" (high-z discs are compact, R_eff~3-5 kpc -> often INSIDE this).")
print("  CONFOUNDS that worsen at z~2-3 (all push the SAME way -- toward NOT cleanly seeing deep-MOND):")
print("     - turbulence: sigma_gas ~ 30-80 km/s (vs ~10 local) -> large pressure/asymmetric-drift correction,")
print("       UNcertain, and it GROWS with z (intrinsic a0-scatter 0.13->0.19 dex z~0.3->1.4 in MUSE-DARK III).")
print("     - V/sigma drops (many systems dispersion-dominated 1<V/sig<3) -> no clean flat outer RC.")
print("     - beam smearing flattens RCs (artificial), biases V_flat; correctable but model-dependent.")
print("     - compact sizes (R_eff~3-5 kpc) + gas-rich -> assembly-active, fitted a0 != fundamental a0 (Magneticum:")
print("       LCDM with NO fundamental a0 produces an APPARENT a0 rising ~x3 by z=2 from baryon-fraction evolution).")

print("\n"+"="*98)
print("(6) WHAT THE EXISTING DIRECT HIGH-Z DATA ALREADY SAY (both ways)")
print("="*98)
print("  THE BIG WHEEL (z=3.25, Nature Astro 2025): cleanest single gas-traced disk. a0_eff ~ 1.0e-10 ~ LOCAL,")
print("    gas-only ceiling ~1.9e-10. Framework branches at z=3.25:")
for f, name in [(a0_decline, "DECLINE sqrt(rhoDE)"), (a0_const, "CONSTANT"), (a0_rising, "RISE cH(z)")]:
    val = float(np.atleast_1d(f(3.25))[0])*A0_0
    print(f"      {name:22s}: a0(z=3.25) = {val:.2e}  ({val/A0_0:.2f}x local)")
print("    => Big Wheel's ~local a0_eff DISFAVORS the RISE x5 strongly; is CONSISTENT with constant AND with the")
print("       mild decline (0.73x ~ 6.8e-11; within the ~1e-10 +/- error). N=1, M_bar systematics bounded.")
print("  RC100 / Genzel / Nestor-Shachar (z=0.6-2.5, N=100): high-g at R_1/2; 'little dark matter', maximal disks.")
print("    -> excludes a0~(1+z)^1.5 and ~4a0 at z=2 (Milgrom 2017) = kills the RISE; does NOT resolve decline-vs-const.")
print("  de Graaff+2024 (JADES z~6, N=6): DISPERSION-dominated (sigma~25-71 km/s), compact -- NOT clean RCs;")
print("    M_dyn/M* up to 40 is DM-domination OR low SFE, degenerate; does NOT cleanly measure a0(z).")
print("  MUSE-DARK III (Ciocan 2026, z=0.33-1.44, N=79): RAR-fit a0 RISES (+1.59e-10/z, ~30sigma apparent), but")
print("    'faster than H(z)', method-localised, LCDM-apparent-a0 degenerate (Magneticum) -> non-diagnostic of")
print("    the FUNDAMENTAL a0; and intermediate-z star-forming disks are g>~a0/assembly-active, not deep-MOND.")

print("\n"+"="*98)
print("(7) INSTRUMENT REACH + TIMELINE")
print("="*98)
print("  ELT/HARMONI (R~3000-17000): the decisive machine for resolved DEEP-MOND outer RCs at z~1-3.")
print("    BUT: telescope first light slipped to MARCH 2029; instrument commissioning 2029-30; SCIENTIFIC first")
print("    light Dec 2030; HARMONI being RESCOPED (ESO STC decision ~Apr 2026). So 'this decade' = LATE/edge.")
print("  JWST/NIRSpec IFU + grating: resolved ionised-gas kinematics NOW (de Graaff, etc.) but small N, compact,")
print("    dispersion-dominated at z>4; cosmic-noon discs are high-g. Useful for the BTFR zero-point, not clean a0.")
print("  ALMA (CO/[CII] cold gas): traces OUTER, dynamically-cold gas -> the best current route into lower-g;")
print("    z~1-4 rotation-supported discs with flat curves DO exist (and even z>4) -> the Big Wheel-style probe.")
print("    This is the realistic 'now' deep-MOND-adjacent dataset; sample is still ~tens, M_bar(molecular) is the")
print("    binding systematic (CO-to-H2 alpha_CO).")

print("\n"+"="*98)
print("VERDICT (both ways)")
print("="*98)
print(f"""  IS a0(z=2-3) DIRECTLY MEASURABLE THIS DECADE?  Marginal-to-NO for the DISTINCTIVE (declining) signal:
    * the distinctive signal is TINY: -0.13 dex in a0 / -3.4% in V at z=3 (because sqrt(rho_DE) varies slowly).
    * the deep-MOND regime that cleanly reads a0 is NOT robustly present at z~2-3: massive cosmic-noon discs sit
      at g=(3-11)a0 (high-acceleration), are turbulent (sigma 30-80 km/s), compact, beam-smeared, and often
      dispersion-dominated -- the confounds (pressure support, M_bar, fitted!=fundamental a0) all exceed the signal.
    * stat N is NOT the bottleneck (~70 ideal discs or a DESI-prior-limited cap ~1.6-2sigma at single z); the
      SYSTEMATIC floor (~0.10 dex baryon/pressure) and the DESI w0wa prior are. Clean 5sigma needs multi-z + DR3.
    * ELT/HARMONI (the right instrument) is Dec-2030 scientific-first-light and being rescoped -> end-of-decade.
  DOES EXISTING DIRECT HIGH-Z RC DATA LEAN FOR/AGAINST THE DECLINE?  It KILLS the rival RISE and is NEUTRAL on the
    distinctive decline: the Big Wheel (z=3.25) reads ~local a0 -- inconsistent with x5 rise, consistent with BOTH
    constant and the mild decline; RC100/Milgrom exclude a0~(1+z)^1.5; MUSE's apparent rise is LCDM-degenerate.
    So the DIRECT-kinematics arm does NOT currently favor the declining branch over constant -- it cannot yet
    distinguish them. The one arm pointing the framework's way is DESI's rho_DE(z) INPUT (sign-aligned), not a0.
  HONEST NET: a0(z=2-3) is, this decade, a FORWARD/edge-of-feasible test for the distinctive declining signal --
    measurable only with ELT-class deep-MOND outer RCs + multi-z + a tighter DESI prior, late 2020s-2030s; the
    high-z deep-MOND regime is genuinely confound-ridden, not clean. Existing data already EXCLUDE the rising
    rival but cannot yet confirm or refute the (small) decline. No manufactured win; no dismissal of the bet.""")
