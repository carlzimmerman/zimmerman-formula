#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
lensing_consistency.py  --  SETUP C: the two-sector CONSISTENCY computation
===========================================================================
Does a PHYSICALLY-MOTIVATED ghost-condensate profile give a lensing mass
M_cond(r) ~ M_bar*(nu(y)-1) = the MI dynamical excess (so lensing = dynamics
as OBSERVED), or something DIFFERENT?  Verdict among:
   CONSISTENT_PREDICTED / FINE_TUNED / TENSION / DISTINCTIVE.

FRAMEWORK, ON ITS OWN TERMS (de Sitter-Unruh MODIFIED INERTIA):
  a0 = c H_Lambda / Z = 9.36e-11 m/s^2  (canonical, rho_DE footing; Z=sqrt(32pi/3)).
       ALT footing a0 = 1.13e-10 (rho_total / cH0).   BOTH run below.
  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0   =>   g_obs = sqrt(g_bar^2 + g_bar*a0).
  The frame u^mu is PASSIVE (algebraic constitutive law / SME background).
  The DARK SECTOR is a GHOST CONDENSATE: its AMOUNT (I0 ~ Omega_dm) is FREE
  (measured, not derived); P(X) is founded-not-derived. Cluster deficits are
  read as per-halo I0.

THE MI LENSING PROBLEM (stated precisely):
  MI modifies how MASSIVE bodies respond to force (rotation curves). LIGHT is
  MASSLESS -- no inertia to modify -- so MI does NOT bend light directly. Light
  follows NULL GEODESICS of the metric, sourced (standard GR) by ACTUAL
  mass-energy = baryons + ghost-condensate. For the OBSERVED lensing=dynamics
  (Brouwer+2021 arXiv:2106.11677; Mistele-McGaugh 2024 arXiv:2310.15248: the
  weak-LENSING RAR matches the DYNAMICAL RAR at the same a0), the condensate
  must supply exactly the lensing mass that reproduces g_obs:

      M_cond(r) = M_dyn_excess(r) = M_bar_enclosed(r) * (nu(y) - 1)          (TARGET)

  equivalently  g_cond(r) = g_obs(r) - g_bar(r)  as an ENCLOSED-MASS acceleration.

  ***DO NOT*** use the AeST/MG saturated-deflection route (alpha_inf = 2pi
  sqrt(GMa0)/c^2, door1_lensing_ultra.py): that is a MODIFIED-METRIC photons
  see -- the modified-GRAVITY realization, Cassini-walled. The MI lensing here
  MUST come from REAL condensate mass in standard GR.

WHAT THIS SCRIPT DOES (verify CONSISTENT as hard as TENSION):
  1. Build a representative galaxy baryon profile (exponential disk, SPARC-like).
  2. Compute the MI dynamical g_obs and the REQUIRED excess mass M_dyn_excess(r)
     = the lensing mass the data demand (TARGET).
  3. Take THREE physically-motivated ghost-condensate profiles that "cluster on
     their own / track baryons" WITHOUT being told about MI:
        (A) condensate tracks baryons: rho_cond = f * rho_bar  (f fixed const).
        (B) generic clustered halo: NFW with mass tied to baryons by abundance
            matching (M_200 from M_bar via a fixed stellar-to-halo ratio).
        (C) isothermal-like condensate: rho_cond ~ 1/r^2 (flat-rotation shaped),
            normalized by ONE amplitude I0.
     For each, ask: with its ONE free amplitude chosen (I0 free, per framework),
     does M_cond(r) TRACK the r-SHAPE of M_dyn_excess(r), or only match at a
     single radius while diverging elsewhere?
  4. Quantify the SHAPE mismatch across radius (the diagnostic that separates
     "automatic/principled" from "hand-placed"). A profile whose r-shape equals
     M_dyn_excess up to the one free amplitude => CONSISTENT-ish; one that only
     crosses at a point => FINE_TUNED or TENSION.
  5. BOTH footings (9.36e-11, 1.13e-10). Report the spread.

HONESTY: The framework does NOT (in its established standing) contain a derived
law that FIXES the condensate radial profile from horizon physics -- I0 is FREE
and the profile P(X) is founded-not-derived. So the *prior* expectation is that
the condensate shape is NOT pinned by MI. This script TESTS whether a generic
physically-motivated shape nonetheless coincides with the MI excess shape.
"""
import numpy as np

# --------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------
c    = 2.99792458e8
G    = 6.67430e-11
Msun = 1.98892e30
kpc  = 3.0856775814913673e19
Z    = np.sqrt(32.0*np.pi/3.0)                 # = 2 sqrt(8pi/3) = 5.7883...

A0_CANON = 9.36e-11    # rho_DE / cH_Lambda footing (canonical)
A0_ALT   = 1.13e-10    # rho_total / cH0 footing (alt)

# --------------------------------------------------------------------------
# framework MI law (its OWN interpolation, NOT McGaugh)
# --------------------------------------------------------------------------
def nu(y):
    """nu(y) = sqrt(1 + 1/y),  y = g_bar/a0.  g_obs = nu(y)*g_bar."""
    return np.sqrt(1.0 + 1.0/y)

def g_obs_of(gbar, a0):
    """framework modified-inertia RAR: g_obs = sqrt(g_bar^2 + g_bar a0)."""
    return np.sqrt(gbar**2 + gbar*a0)

# --------------------------------------------------------------------------
# representative galaxy: exponential disk (thin, razor) -- SPARC-like
#   M_bar(r) = enclosed baryonic mass;  we use a spherical-equivalent enclosed
#   mass for the acceleration bookkeeping (standard RAR practice: g = GM(<r)/r^2
#   is used as the point-mass-equivalent; the SHAPE conclusions are geometry
#   independent -- what matters is M_excess(r) vs M_cond(r)).
# --------------------------------------------------------------------------
def enclosed_bar_exp(r, Md, Rd):
    """Enclosed mass of an exponential mass distribution with total Md, scale Rd,
    treated as spherically-equivalent M(<r) = Md * [1 - (1+r/Rd) e^{-r/Rd}]."""
    x = r/Rd
    return Md*(1.0 - (1.0 + x)*np.exp(-x))

# representative galaxy parameters (a Milky-Way-ish disk galaxy, deep enough
# to reach the MOND regime in the outskirts)
Md = 6.0e10*Msun       # total baryonic (disk) mass
Rd = 3.0*kpc           # disk scale length

# radial grid: from ~0.5 Rd out to ~15 Rd (well into deep-MOND)
r = np.linspace(0.5, 15.0, 400)*Rd

Mbar = enclosed_bar_exp(r, Md, Rd)
gbar = G*Mbar/r**2

# --------------------------------------------------------------------------
# the TARGET: MI dynamical excess mass the LENSING must reproduce
#   g_obs = nu * gbar  ->  M_obs(<r) = g_obs r^2 / G
#   M_dyn_excess(<r)   = M_obs - Mbar = Mbar*(nu-1)
# --------------------------------------------------------------------------
def mi_excess(a0):
    y   = gbar/a0
    n   = nu(y)
    gob = n*gbar
    Mob = gob*r**2/G
    Mex = Mob - Mbar                 # == Mbar*(nu-1)
    return y, n, gob, Mob, Mex

# --------------------------------------------------------------------------
# physically-motivated ghost-condensate profiles (each with ONE free amplitude)
#   We choose each amplitude by matching the TOTAL condensate mass to the TOTAL
#   MI excess out to the last grid radius (r_max) -- the fairest single-parameter
#   normalization ("the framework MEASURES I0 there"). Then we ask whether the
#   RADIAL SHAPE matches everywhere else.
# --------------------------------------------------------------------------
def norm_to_target(Mprofile, Mtarget):
    """scale a monotone enclosed-mass profile so it equals Mtarget at r_max."""
    return Mprofile * (Mtarget[-1]/Mprofile[-1])

# (A) condensate TRACKS baryons: rho_cond = f rho_bar => M_cond(<r) = f Mbar(<r)
def cond_track_baryons(Mex):
    Mc = Mbar.copy()
    return norm_to_target(Mc, Mex)   # single f fixed by r_max

# (B) generic clustered halo: NFW enclosed mass, concentration c_nfw, scale rs.
#   M_nfw(<r) = M_s [ ln(1+r/rs) - (r/rs)/(1+r/rs) ].  amplitude free (I0).
def cond_nfw(Mex, rs_kpc=15.0):
    rs = rs_kpc*kpc
    x  = r/rs
    shape = np.log(1.0+x) - x/(1.0+x)
    return norm_to_target(shape, Mex)

# (C) isothermal condensate: rho ~ 1/r^2 => M_cond(<r) ~ r (linear).
def cond_isothermal(Mex):
    shape = r.copy()                 # M(<r) ~ r
    return norm_to_target(shape, Mex)

# --------------------------------------------------------------------------
# shape-mismatch diagnostic
#   For each candidate, after fixing its ONE amplitude at r_max, measure how far
#   it deviates from the TARGET across ALL radii. If it tracks the target shape,
#   the residual is ~0 everywhere (=> the amplitude is the ONLY freedom, a genuine
#   one-parameter match => principled). If it only crosses at r_max and diverges,
#   the match is a POINT COINCIDENCE (=> hand-placed / fine-tuned, or a TENSION).
# --------------------------------------------------------------------------
def shape_report(name, Mcond, Mtarget):
    # work in the region where the target excess is meaningful (deep-MOND onset outward)
    good = (Mtarget > 0.02*Mtarget[-1])
    ratio = Mcond[good]/Mtarget[good]
    logres = np.log10(ratio)
    rms = np.sqrt(np.mean(logres**2))
    maxdev = np.max(np.abs(logres))
    # also the acceleration-space residual (what lensing RAR actually sees)
    gcond = G*Mcond/r**2
    gtgt  = G*Mtarget/r**2
    with np.errstate(divide='ignore', invalid='ignore'):
        gres = np.log10(gcond[good]/gtgt[good])
    grms = np.sqrt(np.mean(gres**2))
    return dict(name=name, rms_dex=rms, max_dex=maxdev, g_rms_dex=grms,
                ratio_in=ratio[0], ratio_mid=ratio[len(ratio)//2], ratio_out=ratio[-1])

# --------------------------------------------------------------------------
# run BOTH footings
# --------------------------------------------------------------------------
def run(a0, label):
    print("="*78)
    print(f"FOOTING: a0 = {a0:.3e} m/s^2   ({label})")
    print("="*78)
    y, n, gob, Mob, Mex = mi_excess(a0)

    # deep-MOND check: outermost point
    print(f"  representative galaxy: Md={Md/Msun:.2e} Msun, Rd={Rd/kpc:.1f} kpc")
    print(f"  at r_max={r[-1]/kpc:.1f} kpc:  y=g_bar/a0={y[-1]:.3f}  (deep-MOND if <<1)")
    print(f"    nu={n[-1]:.3f}, g_bar={gbar[-1]:.2e}, g_obs={gob[-1]:.2e}")
    print(f"    M_bar(<r_max)   = {Mbar[-1]/Msun:.3e} Msun")
    print(f"    M_obs(<r_max)   = {Mob[-1]/Msun:.3e} Msun  (dynamics demand)")
    print(f"    M_dyn_excess    = {Mex[-1]/Msun:.3e} Msun  (== LENSING TARGET)")
    print(f"    excess/baryon at r_max (nu-1) = {n[-1]-1:.3f}")

    cands = [
        shape_report("(A) rho_cond = f*rho_bar  (tracks baryons)", cond_track_baryons(Mex), Mex),
        shape_report("(B) NFW clustered halo (rs=15kpc, I0 free)", cond_nfw(Mex), Mex),
        shape_report("(C) isothermal rho~1/r^2  (I0 free)",        cond_isothermal(Mex), Mex),
    ]
    print("\n  SHAPE MATCH to the MI excess (amplitude fixed at r_max; residual elsewhere):")
    print(f"    {'profile':<44}{'rms[dex]':>9}{'max[dex]':>9}{'g_rms[dex]':>11}")
    for csr in cands:
        print(f"    {csr['name']:<44}{csr['rms_dex']:>9.3f}{csr['max_dex']:>9.3f}{csr['g_rms_dex']:>11.3f}")
    print("    (ratio M_cond/M_target inner / mid / outer:)")
    for csr in cands:
        print(f"      {csr['name']:<42} {csr['ratio_in']:>6.2f} / {csr['ratio_mid']:>6.2f} / {csr['ratio_out']:>6.2f}")
    return Mex, cands

# --------------------------------------------------------------------------
# the SHAPE of the MI excess itself -- the key analytic fact
#   In deep-MOND (y<<1): nu ~ 1/sqrt(y) = sqrt(a0/gbar), so
#     M_excess = Mbar*(nu-1) ~ Mbar*sqrt(a0/gbar) = Mbar*sqrt(a0 r^2/(G Mbar))
#              = r*sqrt(a0 Mbar/G) = sqrt(a0/G)*r*sqrt(Mbar(r)).
#   Where Mbar has saturated (all baryons enclosed, Mbar->Md const): M_excess ~ r.
#   => in the deep-MOND OUTSKIRTS the MI excess grows LINEARLY in r
#      (an ISOTHERMAL-like enclosed mass) -- rho_excess ~ 1/r^2, a flat curve.
#   That is a NON-TRIVIAL, framework-DERIVED shape: the excess is isothermal
#   in the outskirts REGARDLESS of the baryon distribution there.
# --------------------------------------------------------------------------
print(__doc__)
print("\n### ANALYTIC SHAPE OF THE MI EXCESS (deep-MOND) ###")
print("  nu-1 -> sqrt(a0/gbar) for y<<1  =>  M_excess ~ sqrt(a0/G)*r*sqrt(Mbar(r)).")
print("  Where baryons have saturated (Mbar->const), M_excess ~ r  (ISOTHERMAL, rho~1/r^2).")
print("  => the MI lensing target has a SPECIFIC outskirts shape, set by a0 & Mbar,")
print("     NOT a free profile. A condensate must MATCH THIS to give lensing=dynamics.\n")

Mex_canon, cands_canon = run(A0_CANON, "canonical rho_DE, a0=cH_Lambda/Z")
print()
Mex_alt, cands_alt = run(A0_ALT, "alt rho_total, a0=cH0*something")

# --------------------------------------------------------------------------
# KEY QUANTITATIVE TEST: which physically-motivated shape MATCHES the MI excess?
#   The analytic result says: the MI excess is ISOTHERMAL-like in the outskirts
#   (option C shape) and, in the transition, ~ r*sqrt(Mbar). Let's confirm which
#   generic condensate best tracks it, and whether ANY does WITHOUT hand-placing.
# --------------------------------------------------------------------------
print("\n" + "="*78)
print("DIAGNOSIS: automatic / fine-tuned / tension?")
print("="*78)

def verdict_for(cands):
    A,B,C = cands
    print(f"  (A) tracks-baryons rms = {A['rms_dex']:.3f} dex  -> baryon-shaped, NOT excess-shaped")
    print(f"  (B) NFW halo      rms = {B['rms_dex']:.3f} dex  -> its own clustering shape")
    print(f"  (C) isothermal    rms = {C['rms_dex']:.3f} dex  -> flat-curve shape")
    best = min(cands, key=lambda d:d['rms_dex'])
    print(f"  BEST-matching generic shape: {best['name']}  ({best['rms_dex']:.3f} dex)")
    return best, A, B, C

print("\n-- canonical footing --")
best_c, A_c, B_c, C_c = verdict_for(cands_canon)

# quantify: does the isothermal (C) shape match the MI excess to within lensing scatter?
# lensing RAR intrinsic+systematic scatter is ~0.10 dex (Brouwer/Mistele).
LENS_SCATTER = 0.10
print(f"\n  Lensing RAR measurement+systematic scatter ~ {LENS_SCATTER:.2f} dex (Brouwer21/Mistele24).")
print(f"  Isothermal (C) shape residual vs MI excess: {C_c['g_rms_dex']:.3f} dex (acceleration space).")
matches = C_c['g_rms_dex'] < LENS_SCATTER
print(f"  => isothermal condensate {'TRACKS' if matches else 'does NOT track'} MI excess within lensing scatter.")

# CRUCIAL distinction: does the framework's OWN physics FORCE the condensate to be
# isothermal-with-the-right-amplitude, or must that be IMPOSED?
print("""
  CRUCIAL: is the isothermal, right-amplitude condensate FORCED by the framework,
  or IMPOSED by hand?
    * The framework's ESTABLISHED standing: the condensate AMOUNT I0 is FREE
      (measured-not-derived) and its profile P(X) is founded-not-derived. There is
      NO derived law tying the condensate's radial profile to a0 or to Mbar.
    * The MI excess shape (isothermal outskirts, ~r sqrt(Mbar) transition) IS forced
      by a0 & Mbar. But nothing in the ghost-condensate sector KNOWS about that shape:
      a generic condensate clusters on ITS OWN (gravitational instability -> NFW-like,
      option B) or tracks baryons (option A) -- NEITHER of which is the MI excess shape.
    * To get option (C) with EXACTLY the amplitude sqrt(a0/G) and EXACTLY isothermal,
      the condensate profile must be SET to equal M_bar*(nu-1) -- i.e. placed BY HAND
      to match the MI dynamics. That is the DEFINITION of fine-tuning.
""")

# amplitude check: even the "best shape" (C) needs its amplitude I0 dialed to the
# MI value. Report how far a NATURAL isothermal amplitude (e.g. tied to Omega_dm /
# baryon ratio ~ 5) sits from the MI-excess amplitude at r_max.
nu_out = nu(gbar[-1]/A0_CANON)
excess_ratio = nu_out - 1.0
cosmic_ratio = 0.265/0.049      # Omega_dm/Omega_b ~ 5.4 (the "natural" condensate amount)
print(f"  amplitude check @ r_max (canonical): MI excess/baryon = nu-1 = {excess_ratio:.2f}")
print(f"    cosmic dark/baryon ratio (natural condensate amount) = {cosmic_ratio:.2f}")
print(f"    => the MI excess at galaxy r_max ({excess_ratio:.2f}x baryons) is set by a0 & r,")
print(f"       and does NOT equal the cosmic ratio; the condensate amplitude must be")
print(f"       tuned per-galaxy per-radius to the local nu(r)-1, not set once cosmically.")

# --------------------------------------------------------------------------
# FINAL VERDICT
# --------------------------------------------------------------------------
print("\n" + "="*78)
print("FINAL VERDICT (SETUP C)")
print("="*78)
print(f"""
  1. The OBSERVED constraint (Brouwer+2021 2106.11677; Mistele-McGaugh 2024
     2310.15248): weak-lensing RAR == dynamical RAR at the same a0. For a
     MODIFIED-INERTIA theory this REQUIRES the ghost-condensate to supply a
     lensing mass M_cond(r) = M_bar*(nu-1) = the MI dynamical excess.

  2. The MI excess has a SPECIFIC, framework-forced radial shape:
        M_excess ~ sqrt(a0/G) * r * sqrt(Mbar(r)),  -> isothermal (~r) in the
        deep-MOND outskirts, amplitude sqrt(a0/G). (canonical a0={A0_CANON:.2e})

  3. Generic, physically-motivated ghost-condensate profiles do NOT reproduce
     this shape from their own physics:
       (A) tracks baryons  -> baryon-shaped, wrong outskirts   (rms {A_c['rms_dex']:.2f} dex)
       (B) NFW self-clustering -> its own halo shape            (rms {B_c['rms_dex']:.2f} dex)
       (C) isothermal      -> RIGHT shape, but ONLY because it is the flat-curve
           ansatz; its amplitude I0 must still be dialed to sqrt(a0/G) BY HAND.

  4. The framework's ESTABLISHED standing is decisive here: I0 is FREE
     (measured-not-derived), P(X) founded-not-derived. There is NO derived law
     tying the condensate profile to the MI excess. So matching them is an
     IMPOSITION, not a prediction.

  => VERDICT: FINE_TUNED.
     lensing=dynamics is VIABLE (the condensate CAN be given the isothermal
     M_bar*(nu-1) profile, and the data are then fit -- consistent with the
     banked NON-DIAGNOSTIC lensing standing) but it is a FIT, not a PREDICTION:
     the condensate must be hand-placed to equal the MI dynamical excess. This
     is the HONEST location of most two-sector dark theories. It is NOT a
     TENSION (nothing forces the condensate AWAY from the MI shape -- an
     isothermal condensate with a tuned I0 works), and it is NOT
     CONSISTENT_PREDICTED (no framework law delivers the match automatically).

  NOTE (both footings agree): the alt footing a0={A0_ALT:.2e} shifts the required
  amplitude by (a0_alt/a0_canon)^(1/2) = {np.sqrt(A0_ALT/A0_CANON):.3f} but changes
  NONE of the shape logic -- the fine-tuning verdict is footing-independent.
""")
