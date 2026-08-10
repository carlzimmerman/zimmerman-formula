#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage9_routeB_dust_to_dark_energy_2026.py
=========================================
ROUTE B: THE DUST CONVERTS TO DARK ENERGY (interacting dark sector).

THE IDEA UNDER TEST
    The shift-symmetry-breaking potential V(phi) absorbs the captured dust energy, so
    dust -> Lambda.  Early: more dust, less Lambda (CMB satisfied at full Omega_dm).
    Late: less dust, more Lambda (galaxies cleared).  This has the SHAPE of a solution
    to the coincidence problem, and DESI DR2 favours evolving dark energy.

WHAT THIS SCRIPT SETTLES
   (1) AUDIT of my own prior "47x drift in rho_Lambda" estimate.  It reproduces the
       arithmetic, finds the hidden assumption, and finds that my stated REASON was
       partly wrong while the conclusion (excluded) survives for a DIFFERENT reason.
   (2) The published allowance for dark-matter -> dark-energy conversion, in the SAME
       parametrisation the literature uses, so the comparison is apples-to-apples.
   (3) The SIGN question: does DESI's w0 > -1, wa < 0 help or hurt Route B?
       *** The answer is BOTH, and the two halves must be reported together. ***
   (4) What Route B does to the framework's own a_0(z) law.

STRUCTURAL POINT ESTABLISHED BEFORE ANY DATA (Part 0):
   Route B has exactly two forks and they are not symmetric.
   FORK L (the V-energy stays LOCAL in the galaxy):  already dead.  stage6 Part D/E:
       converting a fraction f to w = -1 makes the dynamical source rho(1-3f), which
       vanishes at f = 1/3, but lensing responds to rho + p = (2/3)rho there.  rho+3p=0
       needs w=-1/3, rho+p=0 needs w=-1; incompatible.  Full conversion f=1 is WORSE:
       the source becomes -2rho, i.e. REPULSIVE.
   FORK S (the V-energy becomes SMOOTH, i.e. actual dark energy):  this script.
       *** The background bound cannot be dodged by localising the conversion, because a
       clumped w=-1 component and a smooth one have the SAME background rho.  Removing
       dust from halos removes it from Omega_m either way. ***

CONVENTION (matched to the literature so the numbers are directly comparable)
   Q = delta * H * rho_d      with      rho_d propto a^(-3+delta)
   delta < 0  <=>  dust loses energy to the vacuum  <=>  ROUTE B.
   Energy conservation then gives, exactly,
       rho_L(a) = rho_L0 + (delta/(3-delta)) * rho_d0 * (a^(-3+delta) - 1)
   Fraction of the dust converted per Hubble time = |delta|.

SOURCES FOR EVERY EXTERNAL NUMBER ARE IN THE `SRC` DICT AND PRINTED AT THE END.
"""

import sys
import math

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    tag = "PASS" if cond else "FAIL"
    if not cond:
        FAIL.append(label)
    print(f"  [{tag}] {label}" + (f"   {detail}" if detail else ""))


def hdr(s):
    print("\n" + "=" * 98)
    print(s)
    print("=" * 98)


# ----------------------------------------------------------------------------------------------
# CONSTANTS.  Framework's own footing (canonical): a_0 = kappa c sqrt(G rho_Lambda).
# ----------------------------------------------------------------------------------------------
OM_L = 0.6847          # Omega_Lambda, Planck 2018 TT,TE,EE+lowE+lensing
OM_DM = 0.264          # Omega_dm  -- the framework's OWN banked CMB requirement
OM_B = 0.0493          # Omega_b
H0_KMS = 67.4          # km/s/Mpc
H0_INV_GYR = 9.77793 / (H0_KMS / 100.0)   # 1/H0 in Gyr
OM_G = 2.47e-5 / (H0_KMS / 100.0) ** 2    # photons
OM_NU = 0.6813 * OM_G                      # 3 massless nu
OM_R = OM_G + OM_NU
Z_STAR = 1089.9        # Planck 2018 recombination redshift
TAU_FF_LSTAR = 2.43    # Gyr, banked: free-fall time of an L* basin (1 Mpc, MOND-boosted)
M_DUST_LSTAR = 2.51e12 # Msun, banked captured share per L* galaxy

SRC = {
    "OM_L, OM_B, Z_STAR, omega_dm=0.1200+/-0.0012, 100theta_*=1.04110+/-0.00031":
        "Planck 2018 VI, A&A 641 A6 (arXiv:1807.06209)",
    "Omega_m = 0.2975 +/- 0.0086 (DESI DR2 BAO alone, LCDM)":
        "DESI DR2 BAO cosmology (arXiv:2503.14738)",
    "Omega_m = 0.3027 +/- 0.0036 (DESI DR2 BAO + CMB, LCDM)":
        "DESI DR2 BAO cosmology (arXiv:2503.14738)",
    "Omega_m = 0.3143 +/- 0.0076 (CMB alone, LCDM)":
        "Planck 2018 / DESI DR2 comparison",
    "w0 = -0.752 +/- 0.057, wa = -0.86 +0.23/-0.21 (DESI DR2+CMB+DESY5)":
        "DESI DR2 (arXiv:2503.14738); 2.8-4.2 sigma dep. on SN set",
    "w0 = -0.838 +/- 0.055, wa = -0.62 +0.22/-0.19 (DESI DR2+CMB+Pantheon+)":
        "DESI DR2 (arXiv:2503.14738)",
    "w0 = -0.42 +/- 0.21, wa = -1.75 +/- 0.58 (DESI DR2+CMB, no SN)":
        "DESI DR2 (arXiv:2503.14738)",
    "Omega_m = 0.334 +/- 0.018 (Pantheon+ SN alone)":
        "Brout et al. 2022, ApJ 938 110",
    "Omega_m = 0.352 +/- 0.017 (DES-Y5 SN alone)":
        "DES Collaboration 2024, ApJL 973 L14",
    "delta_0 = -0.00050 +/- 0.00033 (68%) / +/-0.00067 (95%), CMB+DESI+Pantheon+":
        "Interacting DE after DESI DR2 (arXiv:2504.00994); rho_dm ~ a^(-3+delta_0), "
        "delta_0<0 = DM->DE",
    "epsilon = -0.0073 +0.0029/-0.0033, DESI DR1+CMB priors+CC+Pantheon+fsigma8":
        "arXiv:2505.09879; rho_dm ~ (1+z)^(3-eps), Q = eps H rho_dm",
    "xi = -0.132 +0.087/-0.064 (CMB+DESI-DR2); xi > -0.0220 (CMB+DESI-DR2+DESY5)":
        "Silva et al., PRD 111 123511 (arXiv:2503.23225); Q = xi H rho_DE, xi<0 = DM->DE",
    "zeta < 0.030 (68%, CMB+SN+BAO) = fraction of DM converted over cosmic history":
        "Chen, Huterer et al., PRD 103 123528 (arXiv:2011.04606) [DM->dark radiation]",
    "beta = 0.256 +0.092/-0.063 (Planck+DESI DR2+Pantheon+), coupled quintessence":
        "arXiv / ApJ 10.3847/1538-4357/ae2ff8; beta>0 = DE->DM",
}


# ==============================================================================================
hdr("PART 0 -- THE FORK, AND WHY FORK S CANNOT DODGE THE BACKGROUND BOUND")
# ==============================================================================================
print(r"""
  Dynamical source  = rho + 3p ;  lensing source = rho + p  (AeST: no slip, Phi=Psi, gamma_PPN=1).
  FORK L, full conversion to w=-1 held locally:  rho + 3p = rho(1 - 3) = -2 rho.
""")
f_full = 1.0
src_dyn_full = 1.0 - 3.0 * f_full
print(f"  f = 1.00 : dynamical source coefficient = {src_dyn_full:+.2f} rho  -> REPULSIVE")
M_rep = abs(src_dyn_full) * M_DUST_LSTAR
print(f"  magnitude for an L* basin: {abs(src_dyn_full):.0f} x {M_DUST_LSTAR:.3g} "
      f"= {M_rep:.3g} Msun of REPULSIVE effective mass (~{M_rep/6e10:.0f}x MW baryons)")
check(src_dyn_full < 0, "Fork L at full conversion is repulsive, not merely hidden",
      f"source = {src_dyn_full:+.2f} rho")
f_third = 1.0 / 3.0
print(f"\n  f = 1/3  : dynamical source = {1-3*f_third:+.2f} rho  (vanishes -- stage6 Part D attractor)")
print(f"             but lensing source  = 1 - {f_third:.4f} = {1-f_third:+.4f} rho  -> STILL LENSES")
check(abs(1 - 3 * f_third) < 1e-12 and abs((1 - f_third) - 2.0 / 3.0) < 1e-12,
      "stage6 Part D/E reproduced: f=1/3 kills dynamics, leaves (2/3)rho in lensing")
print("""
  ==> FORK L was already closed by a committed script (stage6).  Route B therefore MUST be
      FORK S: the converted energy becomes smooth dark energy.  And a clumped w=-1 component
      has the same BACKGROUND rho as a smooth one, so localising the conversion buys nothing
      against the expansion-history bound computed below.""")


# ==============================================================================================
hdr("PART 1 -- AUDIT OF MY OWN '47x DRIFT' ESTIMATE")
# ==============================================================================================
ratio = OM_L / OM_DM
print(f"\n  rho_Lambda / rho_dust today = {OM_L}/{OM_DM} = {ratio:.4f}")
check(abs(ratio - 2.60) < 0.01, "the claimed lock ratio 2.60 is reproduced",
      f"{ratio:.4f}")

# Reconstruct the 47x
t_clear, t_span = 1.0, 10.0          # Gyr
drift_exp = math.exp(t_span / ratio)
print(f"\n  Reconstructing 47x:  Gamma_n = 1/{t_clear:.0f} Gyr, Gamma_V = Gamma_n/{ratio:.4f}")
print(f"  exp(Gamma_V * {t_span:.0f} Gyr) = exp({t_span/ratio:.4f}) = {drift_exp:.2f}x")
check(abs(drift_exp - 47.0) < 1.0, "the 47x is exp(10/2.594) -- arithmetic reproduced",
      f"{drift_exp:.2f}")

print(r"""
  *** THE HIDDEN ASSUMPTION: exponential GROWTH of rho_Lambda at a fixed FRACTIONAL rate.
      That requires an unbounded dust reservoir.  rho_Lambda does not dilute, so it can only
      grow by the amount of dust actually fed in. ***""")
cap_today = 1.0 + 1.0 / ratio
print(f"\n  If the conversion happens AT z=0, the cap is 1 + rho_d0/rho_L0 = {cap_today:.4f}x  (+{100*(cap_today-1):.1f}%)")
print(f"  -> the 47x over-states THAT cap by {drift_exp/cap_today:.1f}x")

print(r"""
  *** BUT MY CORRECTION IS ALSO INCOMPLETE, AND IT MATTERS.  Dust dilutes as a^-3, Lambda does
      not.  Converting EARLY feeds a DENSER source into a non-diluting component, so the cap
      grows as (1+z)^3.  The 47x is reachable -- at a price. ***""")
print(f"\n  {'z_conv':>8}  {'cap = 1 + (1+z)^3/2.594':>26}  {'pre-existing rho_L / rho_L0':>30}")
z_reach = None
for zc in [0.0, 0.5, 1.0, 2.0, 3.0, 3.93, 5.0]:
    cap = 1.0 + (1.0 + zc) ** 3 / ratio
    pre = 1.0 - (cap - 1.0)
    print(f"  {zc:>8.2f}  {cap:>26.3f}  {pre:>30.3f}")
    if z_reach is None and cap >= drift_exp:
        z_reach = zc
zc_exact = ((drift_exp - 1.0) * ratio) ** (1.0 / 3.0) - 1.0
print(f"\n  47x is exactly reached by converting all the dust at z = {zc_exact:.3f}")
check(abs(zc_exact - 3.93) < 0.05, "47x IS reachable -- by converting at z~3.9, not by unbounded growth",
      f"z_conv = {zc_exact:.3f}")
pre_at_47 = 1.0 - (drift_exp - 1.0)
print(f"  and it requires the PRE-EXISTING vacuum energy to have been {pre_at_47:.1f} x rho_L0")
check(pre_at_47 < 0, "*** the 47x needs a LARGE NEGATIVE pre-existing vacuum energy ***",
      f"rho_L(pre) = {pre_at_47:.1f} rho_L0")
print(r"""
  VERDICT ON PART 1 (against my own prior write-up):
    - the 47x arithmetic is right; the WORD 'excluded' is right; but my stated MECHANISM
      ('the ratio locks and rho_Lambda grows exponentially') smuggled in an infinite reservoir.
    - the honest statement is: a 47x drift is not forbidden by the dust budget, it is forbidden
      because rho_Lambda(early) would have to be about -46 x rho_L0.  The binding constraint is
      rho_Lambda >= 0 plus the measured expansion history -- NOT the leak-rate lock.
    - the 2.60 'rate lock' is not a lock at all: it is just today's density ratio, and it is
      only the instantaneous ratio of fractional rates.  Do not cite it as a locked relation.""")


# ==============================================================================================
hdr("PART 2 -- HOW MUCH DUST ACTUALLY HAS TO BE CLEARED")
# ==============================================================================================
RHO_CRIT = 2.775e11 * (H0_KMS / 100.0) ** 2      # Msun / Mpc^3
print(f"\n  rho_crit = {RHO_CRIT:.4g} Msun/Mpc^3 ;  banked captured share per L* = {M_DUST_LSTAR:.3g} Msun")
print(f"\n  {'n_Lstar [Mpc^-3]':>18}  {'Omega in L* dust':>18}  {'as fraction of Omega_dm':>25}")
frac_lo = None
for n in [1e-3, 2e-3, 3e-3, 5e-3]:
    om = M_DUST_LSTAR * n / RHO_CRIT
    print(f"  {n:>18.1e}  {om:>18.4f}  {om/OM_DM:>25.3f}")
    if frac_lo is None:
        frac_lo = om / OM_DM
print(f"""
  So L*-type galaxies ALONE hold {frac_lo*100:.0f}-38% of the entire cosmic dust budget, before
  groups, clusters and dwarfs are counted.  The framework's smooth-accretion theorem says EVERY
  halo captures the dust, so the share that must be cleared is a large O(1) fraction of Omega_dm.
  I will carry f_halo = 0.08 (the most conservative, L*-only, lowest n) through to 1.0.""")
check(frac_lo > 0.05, "the share needing clearance is not a negligible corner of Omega_dm",
      f"L*-only lower bound = {frac_lo:.3f} of Omega_dm")


# ==============================================================================================
hdr("PART 3 -- THE RATE ROUTE B NEEDS, vs THE RATE THE DATA ALLOW")
# ==============================================================================================
print(f"\n  1/H0 = {H0_INV_GYR:.3f} Gyr.   |delta| = Gamma_eff / H = fraction converted per Hubble time.")
print(f"\n  {'f_halo':>8} {'tau_clear[Gyr]':>15} {'Gamma_eff[1/Gyr]':>18} {'|delta| needed':>15}")
need = {}
for fh in [1.0, 0.5, 0.08]:
    for tc in [1.0, TAU_FF_LSTAR]:
        g = fh / tc
        d = g * H0_INV_GYR
        need[(fh, tc)] = d
        print(f"  {fh:>8.2f} {tc:>15.2f} {g:>18.4f} {d:>15.3f}")

DELTA_95 = 6.7e-4          # arXiv:2504.00994, 95% CL, CMB+DESI DR2+Pantheon+
EPS_2SIG = 0.0073 + 2 * 0.0029   # arXiv:2505.09879, 2-sigma reach toward zero/positive
ZETA_68 = 0.030            # arXiv:2011.04606, integrated fraction
print(f"""
  PUBLISHED ALLOWANCES, all in the SAME 'fraction per Hubble time' currency:
    |delta_0| <= {DELTA_95:.5f}   (95% CL, CMB + DESI DR2 + Pantheon+)      = {DELTA_95*100:.3f} % per Hubble time
    |epsilon| <= {EPS_2SIG:.5f}   (2 sigma, DESI DR1 + CMB priors + CC + SN) = {EPS_2SIG*100:.3f} % per Hubble time
    zeta      <= {ZETA_68:.3f}     (68% CL, integrated over ALL cosmic history) = {ZETA_68*100:.1f} % total""")

print(f"\n  {'f_halo':>8} {'tau[Gyr]':>10} {'|delta| need':>13} {'/ delta_95':>12} {'/ eps_2sig':>12}")
worst = 1e99
for (fh, tc), d in need.items():
    r1, r2 = d / DELTA_95, d / EPS_2SIG
    worst = min(worst, r1)
    print(f"  {fh:>8.2f} {tc:>10.2f} {d:>13.3f} {r1:>12.0f}x {r2:>12.0f}x")
check(worst > 100, "*** Route B's required rate exceeds the tightest published allowance ***",
      f"most conservative case is still {worst:.0f}x over")
d_max = max(need.values())
print(f"\n  headline: {d_max/DELTA_95:.0f}x over the 95% bound at f_halo=1, tau=1 Gyr;"
      f"  {worst:.0f}x over even at f_halo=0.08, tau=2.43 Gyr")
# integrated-fraction version, which needs no rate model at all
print(f"\n  RATE-FREE VERSION (immune to any objection about Gamma's time dependence):")
print(f"    Route B must convert f_halo = 0.08 to 1.0 of the dust.  zeta bound = {ZETA_68:.3f}.")
print(f"    -> over by {0.08/ZETA_68:.1f}x (most conservative) to {1.0/ZETA_68:.1f}x (full clearance).")
check(0.08 / ZETA_68 > 1.0, "even the integrated fraction alone exceeds the zeta bound",
      f"{0.08/ZETA_68:.1f}x to {1.0/ZETA_68:.1f}x")


# ==============================================================================================
hdr("PART 4 -- COSMOLOGICAL INTEGRATION: SNe Ia, BAO, CMB ACOUSTIC SCALE")
# ==============================================================================================
def rho_L_of_a(a, beta):
    """Exact solution for rho_L(a)/rho_crit0 with rho_d ~ a^(-3-beta), beta = |delta| >= 0."""
    return OM_L - (beta / (3.0 + beta)) * OM_DM * (a ** (-3.0 - beta) - 1.0)


def a_zero_crossing(beta):
    """Scale factor where rho_Lambda hits zero (None if never for a<=1)."""
    if beta <= 0:
        return None
    rhs = 1.0 + (3.0 + beta) / beta * (OM_L / OM_DM)
    return rhs ** (-1.0 / (3.0 + beta))


print(f"\n  Exact:  rho_L(a) = Omega_L - [beta/(3+beta)] Omega_dm (a^(-3-beta) - 1)")
print(f"\n  {'|delta|':>10} {'case':>28} {'a(rho_L=0)':>12} {'z(rho_L=0)':>12}")
rows = [(need[(1.0, 1.0)], "f=1.0, tau=1.0 Gyr"),
        (need[(1.0, TAU_FF_LSTAR)], "f=1.0, tau=2.43 Gyr"),
        (need[(0.5, TAU_FF_LSTAR)], "f=0.5, tau=2.43 Gyr"),
        (need[(0.08, TAU_FF_LSTAR)], "f=0.08, tau=2.43 Gyr"),
        (DELTA_95, "the 95% published bound")]
z_cross = {}
for b, lab in rows:
    a0 = a_zero_crossing(b)
    z0 = 1.0 / a0 - 1.0
    z_cross[lab] = z0
    print(f"  {b:>10.5f} {lab:>28} {a0:>12.5f} {z0:>12.4f}")

Z_TRANS_OBS = 0.63   # LCDM deceleration->acceleration transition, (2 Om_L/Om_m)^(1/3)-1
zt = (2 * OM_L / (OM_DM + OM_B)) ** (1.0 / 3.0) - 1.0
print(f"\n  Measured/LCDM deceleration-acceleration transition: z_t = {zt:.3f}")
print(f"  SNe Ia + BAO see acceleration out to z~1 and DE detected across 0 < z < 2.3 (DESI DR2).")
for lab in ["f=1.0, tau=1.0 Gyr", "f=1.0, tau=2.43 Gyr", "f=0.5, tau=2.43 Gyr",
            "f=0.08, tau=2.43 Gyr"]:
    print(f"    {lab:>24}:  rho_Lambda < 0 for z > {z_cross[lab]:.3f}   "
          f"{'*** INSIDE the SNe/BAO data ***' if z_cross[lab] < 2.33 else ''}")
check(all(z_cross[l] < 2.33 for l in
          ["f=1.0, tau=1.0 Gyr", "f=1.0, tau=2.43 Gyr", "f=0.5, tau=2.43 Gyr",
           "f=0.08, tau=2.43 Gyr"]),
      "*** at every rate Route B needs, rho_Lambda goes NEGATIVE inside the SNe/BAO redshift range ***")
check(z_cross["the 95% published bound"] > 2.33,
      "at the published-allowed rate the pathology is pushed outside the data (why the fits are fine)",
      f"z = {z_cross['the 95% published bound']:.1f}")

print(r"""
  *** BUT THE POWER LAW IS NOT ROUTE B'S ACTUAL HISTORY, AND I ALMOST SCORED IT AS IF IT WERE.
      rho_d ~ a^(-3+delta) runs the conversion all the way back to recombination.  Route B only
      converts once HALOS EXIST, i.e. z <~ 2-3.  Extrapolating the power law to z=1090 destroys
      all the dust and would have let me report a fake ~70 sigma.  The power-law numbers above
      apply ONLY to the SMOOTH variant -- which is exactly the variant the published delta_0,
      epsilon and xi bounds constrain, so they are the right currency for Part 3 and the wrong
      one for the physical model.  Below is the FAIR construction. ***""")

# ==============================================================================================
hdr("PART 4b -- THE FAIR CONSTRUCTION: A LATE BURST, ANCHORED ON theta_* AND SOLVED FOR h")
# ==============================================================================================
print(r"""
  PHYSICAL Route B: the dust is captured as halos assemble, and the halo-resident share f is
  converted promptly (Gamma tau >> 1) around z_conv.  Then, EXACTLY:
      z > z_conv :  dust = full omega_dm ;   rho_L = rho_L,pre
      z < z_conv :  dust = (1-f) omega_dm ;  rho_L = rho_L,pre + f omega_dm (1+z_conv)^3
  (Lambda does not dilute, so energy converted at z_conv keeps that DENSITY forever -- which is
  why converting early over-produces Lambda.)

  I hold the CMB's physical densities FIXED (omega_b = 0.02237, omega_dm = 0.1200, so r_s is
  unchanged), impose flatness, and solve for h so that D_M(z_*) -- hence theta_* -- matches the
  no-conversion baseline to better than Planck's 0.03%.  Then Omega_m(0) and H0 are PREDICTIONS.""")

OM_B_H2, OM_DM_H2, OM_R_H2 = 0.02237, 0.1200, 4.152e-5
OMM_DESI, SIG_DESI = 0.2975, 0.0086
OMM_PP, SIG_PP = 0.334, 0.018
H0_SH0ES, SIG_SH0ES = 73.04, 1.04
H0_LOCAL_CONS, SIG_LOCAL_CONS = 70.0, 2.0     # deliberately generous JWST-TRGB-ish local anchor


def build(f, z_conv, h):
    h2 = h * h
    Ob = OM_B_H2 / h2
    Od0 = (1.0 - f) * OM_DM_H2 / h2
    Or = OM_R_H2 / h2
    OL0 = 1.0 - Ob - Od0 - Or                              # flatness
    dOL = f * OM_DM_H2 * (1.0 + z_conv) ** 3 / h2           # increment injected at z_conv
    return Ob, Od0, Or, OL0, OL0 - dOL                      # last = rho_L,pre


def E_burst(z, f, z_conv, h):
    a = 1.0 / (1.0 + z)
    Ob, Od0, Or, OL0, OLpre = build(f, z_conv, h)
    if z < z_conv:
        rd, rl = Od0 * a ** -3, OL0
    else:
        rd, rl = (Od0 / (1.0 - f)) * a ** -3, OLpre
    tot = Ob * a ** -3 + rd + Or * a ** -4 + rl
    return math.sqrt(tot) if tot > 0 else float("nan")


def I_of(z, f, z_conv, h, n=800):
    """Integral of dz/E from 0 to z, done in x = ln(1+z) so n=800 is ample to z_*."""
    xmax = math.log1p(z)
    step = xmax / n
    s = 0.0
    for i in range(n + 1):
        x = i * step
        zi = math.expm1(x)
        e = E_burst(zi, f, z_conv, h)
        if not (e == e) or e <= 0:
            return float("nan")
        s += (1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)) * (1.0 + zi) / e
    return s * step / 3.0


C_KMS = 299792.458


def DM_star(f, z_conv, h):
    I = I_of(Z_STAR, f, z_conv, h)
    return float("nan") if not (I == I) else (C_KMS / (100.0 * h)) * I


D_TARGET = DM_star(0.0, 0.0, 0.674)     # the no-conversion baseline, internally consistent
print(f"\n  baseline D_M(z_*) at f=0, h=0.674 : {D_TARGET:.1f} Mpc   "
      f"(Planck chi_* ~ 13870 Mpc -- consistency check on the machinery)")


def solve_h(f, z_conv):
    lo, hi = 0.20, 3.00
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        D = DM_star(f, z_conv, mid)
        if not (D == D):
            lo = mid            # unphysical (rho_L<0 somewhere) -> push h up
            continue
        if D > D_TARGET:
            lo = mid            # D_M too big -> need larger h
        else:
            hi = mid
    return 0.5 * (lo + hi)


print(f"\n  {'f':>6} {'z_conv':>7} {'h':>7} {'H0':>7} {'Om_m(0)':>9} {'rho_L,pre/rho_L0':>17} "
      f"{'sig(Om_m,DESI)':>15} {'sig(H0,SH0ES)':>14} {'sig(H0,70+/-2)':>15}")
fair = {}
for f in [0.0, 0.08, 0.20, 0.30, 0.50, 0.75, 0.90]:
    for zc in ([0.0] if f == 0.0 else [0.5, 1.0, 2.0]):
        h = solve_h(f, zc)
        Ob, Od0, Or, OL0, OLpre = build(f, zc, h)
        om_m = Ob + Od0
        H0 = 100.0 * h
        pre_ratio = OLpre / OL0
        s_om = (om_m - OMM_DESI) / SIG_DESI
        s_h1 = (H0 - H0_SH0ES) / SIG_SH0ES
        s_h2 = (H0 - H0_LOCAL_CONS) / SIG_LOCAL_CONS
        fair[(f, zc)] = (H0, om_m, pre_ratio, s_om, s_h1, s_h2)
        print(f"  {f:>6.2f} {zc:>7.1f} {h:>7.4f} {H0:>7.2f} {om_m:>9.4f} {pre_ratio:>+17.3f} "
              f"{s_om:>14.1f}s {s_h1:>13.1f}s {s_h2:>14.1f}s")

print(r"""
  *** READ THE TABLE HONESTLY -- IT DOES NOT SAY WHAT MY FIRST PASS SAID. ***
    - f = 0.08 (the L*-only FLOOR) is close to FINE: H0 = 68.5-70.8 and Omega_m = 0.265-0.283,
      i.e. within ~1-4 sigma.  Route B at the 8% level is NOT excluded by cosmology.
    - the binding axis is Omega_m(0), NOT H0.  Removing matter while injecting non-diluting
      Lambda at z_conv pushes h UP to hold theta_* fixed, and Omega_m = (omega_b + (1-f)omega_dm)/h^2
      then falls on BOTH counts -- less matter and larger h.
    - AND A POINT FOR ROUTE B THAT I HAVE TO STATE: f ~ 0.2 at z_conv ~ 1 lands H0 = 72.4, which
      is 0.6 sigma from SH0ES and would RESOLVE the Hubble tension.  Route B is not a cosmological
      dead weight; it is a live H0 mechanism that happens to be killed by Omega_m (8.4 sigma).
    - rho_L,pre < 0 (a negative pre-existing vacuum energy) appears once f and z_conv are both
      moderate -- exactly the pathology Part 1 identified for the 47x.""")

worst_f = None
for f in [0.20, 0.30, 0.50, 0.75, 0.90]:
    H0, om_m, pre, s_om, s_h1, s_h2 = fair[(f, 1.0)]
    verdict = ("EXCLUDED" if (abs(s_h2) > 3 or abs(s_om) > 3 or pre < 0) else "survives")
    print(f"    f = {f:.2f}, z_conv = 1.0 : H0 = {H0:.1f}, Omega_m = {om_m:.4f}, "
          f"rho_L,pre = {pre:+.2f} rho_L0  -> {verdict}")
    if worst_f is None and verdict == "EXCLUDED":
        worst_f = f
print(f"\n  => the background allows at most f ~ 0.1; it EXCLUDES f >= {worst_f:.2f} at z_conv = 1.")
check(max(abs(fair[(0.08, 1.0)][3]), abs(fair[(0.08, 1.0)][5])) < 4.0,
      "AGAINST INTEREST: at the L*-only floor f=0.08 Route B's background is NOT excluded",
      f"H0 = {fair[(0.08,1.0)][0]:.1f} ({abs(fair[(0.08,1.0)][5]):.1f}s), "
      f"Omega_m = {fair[(0.08,1.0)][1]:.4f} ({abs(fair[(0.08,1.0)][3]):.1f}s)")
check(abs(fair[(0.50, 1.0)][5]) > 3.0 or fair[(0.50, 1.0)][2] < 0,
      "but f=0.50 at z_conv=1 IS excluded",
      f"H0 = {fair[(0.50,1.0)][0]:.1f} ({abs(fair[(0.50,1.0)][5]):.1f}s vs 70+/-2), "
      f"rho_L,pre = {fair[(0.50,1.0)][2]:+.2f}")

# the fraction bound, stated cleanly and h-free
print(r"""
  ------------------------------------------------------------------------------------------
  THE ONE NUMBER THAT DECIDES ROUTE B: the CONVERTED FRACTION f.
  ------------------------------------------------------------------------------------------""")
def f_max_fair(z_conv, om_floor):
    """Largest f whose FAIR (theta_*-anchored) Omega_m(0) still reaches om_floor."""
    lo, hi = 0.0, 0.99
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        h = solve_h(mid, z_conv)
        Ob, Od0, _, _, _ = build(mid, z_conv, h)
        if Ob + Od0 > om_floor:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


f_bound = {}
print("  (computed INSIDE the fair theta_*-anchored construction, not with h held fixed)")
for name, (val, sig) in [("DESI DR2 BAO alone (0.2975+/-0.0086)", (OMM_DESI, SIG_DESI)),
                         ("Pantheon+ SN alone (0.334+/-0.018)", (OMM_PP, SIG_PP))]:
    floor = val - 2 * sig                     # 2-sigma low edge on Omega_m(0)
    cells = []
    for zc in [0.5, 1.0, 2.0]:
        cells.append((zc, f_max_fair(zc, floor)))
    f_bound[name] = max(v for _, v in cells)   # most GENEROUS z_conv, i.e. best case for Route B
    txt = ", ".join(f"z_conv={zc:.1f}: f<={v:.3f}" for zc, v in cells)
    print(f"    {name:>40}: {txt}")
print(f"\n  WHAT ROUTE B NEEDS (the share of the dust sitting in halos, from Part 2 + the")
print(f"  framework's own smooth-accretion theorem that EVERY halo captures it):")
print(f"    L*-galaxies only, lowest number density  : f = 0.075   <- a FLOOR, not the answer")
print(f"    L*-galaxies only, higher number density  : f = 0.38")
print(f"    all galaxy-scale halos (1e11-1e13 Msun)  : f ~ 0.3-0.5")
print(f"    every halo (what the theorem actually says): f ~ 0.7-0.9")
fb = f_bound["DESI DR2 BAO alone (0.2975+/-0.0086)"]
fb_sn = f_bound["Pantheon+ SN alone (0.334+/-0.018)"]
print(f"\n  MOST GENEROUS corner for Route B (loosest probe, loosest z_conv): f <= {max(fb,fb_sn):.3f}")
print(f"  bound f <= {max(fb,fb_sn):.3f} vs needed f ~ 0.3-0.9  ->  "
      f"short by {0.3/max(fb,fb_sn):.1f}x to {0.9/max(fb,fb_sn):.1f}x")
print(f"\n  and in sigma, from the FAIR table at z_conv = 1.0:")
for fneed in [0.3, 0.5, 0.9]:
    print(f"    f = {fneed:.1f} : Omega_m(0) = {fair[(fneed,1.0)][1]:.4f}, H0 = {fair[(fneed,1.0)][0]:.1f}"
          f"  -> {abs(fair[(fneed,1.0)][3]):.0f} sigma (Omega_m, DESI DR2 BAO), "
          f"{abs(fair[(fneed,1.0)][5]):.1f} sigma (H0, 70+/-2)")
check(max(fb, fb_sn) < 0.3,
      "*** the converted fraction Route B needs exceeds what the expansion history allows ***",
      f"allowed f <= {max(fb,fb_sn):.3f}, needed 0.3-0.9")
F_ALLOWED = max(fb, fb_sn)


# ==============================================================================================
hdr("PART 5 -- THE SIGN QUESTION: DOES DESI'S w0 > -1, wa < 0 HELP OR HURT?")
# ==============================================================================================
print(r"""
  Route B has Q > 0 into a w=-1 vacuum at all times, so
      d rho_L/dt = +Q > 0  =>  1 + w_eff = -Q/(3 H rho_L) < 0  =>  w_eff < -1 ALWAYS.
  Route B can ONLY produce the PHANTOM side.  It cannot cross w = -1.""")
for b, lab in rows[:3]:
    weff0 = -1.0 - b / (3.0 * ratio)
    print(f"    |delta| = {b:>7.3f} ({lab:>22}) : w_eff(0) = {weff0:+.3f}")
w95 = -1.0 - DELTA_95 / (3.0 * ratio)
print(f"    |delta| = {DELTA_95:.5f} (the 95% bound        ) : w_eff(0) = {w95:+.7f}")

print("\n  DESI DR2 w0waCDM best fits (all three dataset combinations):")
DESI = {"DR2+CMB+DESY5": (-0.752, 0.057, -0.86, 0.22),
        "DR2+CMB+Pantheon+": (-0.838, 0.055, -0.62, 0.205),
        "DR2+CMB (no SN)": (-0.42, 0.21, -1.75, 0.58)}
for k, (w0, sw0, wa, swa) in DESI.items():
    zpk = wa / (1 + w0 + wa) - 1.0 if (1 + w0 + wa) != 0 else float("nan")
    dlnrho_dz0 = 3.0 * (1.0 + w0)
    print(f"    {k:>20}: w0 = {w0:+.3f}+/-{sw0:.3f}, wa = {wa:+.2f}+/-{swa:.2f}")
    print(f"        {'':>20}  dln(rho_DE)/dz at z=0 = 3(1+w0) = {dlnrho_dz0:+.3f}  "
          f"=> rho_DE is {'DECREASING' if dlnrho_dz0 > 0 else 'INCREASING'} with time TODAY")
    print(f"        {'':>20}  rho_DE peaks at z = {zpk:.3f}; w crosses -1 at that same z")
    for b, lab in rows[:2]:
        weff0 = -1.0 - b / (3.0 * ratio)
        print(f"        {'':>20}  Route B ({lab}): w_eff(0) = {weff0:+.3f} "
              f"=> {abs(weff0 - w0)/sw0:.0f} sigma from this w0")

print(r"""
  *** SO THE SIGN ANSWER IS TWO-SIDED AND BOTH HALVES ARE REAL. ***

  AGAINST Route B -- the CPL reading.  Every DESI DR2 combination has w0 > -1, so
  d ln rho_DE/dz|_0 = 3(1+w0) > 0: the DE density is DECREASING with time today, peaking at
  z ~ 0.29-0.44 and falling since.  Route B requires rho_Lambda to be monotonically INCREASING.
  DESI's shape is 'grow then shrink'; Route B can only give 'grow, always'.  The mismatch sits
  in the present epoch, where the data are strongest.  At the rate Route B needs, w_eff(0) is
  -2.9 to -1.8, which is 18-37 sigma from DESI's w0.

  FOR Route B -- the interacting reading, and I have to give it its due.  When the SAME data are
  fit with a true w = -1 vacuum plus a dark-sector coupling, the preferred transfer direction is
  DUST -> DARK ENERGY, i.e. Route B's own sign:
      delta_0 = -0.00050 +/- 0.00033   (arXiv:2504.00994, delta_0 < 0 = DM -> DE), ~1.5 sigma
      epsilon = -0.0073 +0.0029/-0.0033 (arXiv:2505.09879, same sign), ~2.4 sigma
      xi      = -0.132 +0.087/-0.064    (arXiv:2503.23225, xi < 0 = DM -> DE)
  These are not contradicting the CPL fit -- they are an alternative absorption of the SAME mild
  anomaly (DESI's late-time Omega_m = 0.2975 +/- 0.0086 sitting low against the CMB's
  0.3143 +/- 0.0076).  Bleeding dark matter into the vacuum is one way to lower late-time
  Omega_m, and that is qualitatively what Route B does.

  *** Route B is therefore pointed the RIGHT WAY and overshoots in AMOUNT.  In the smooth
      parametrisation the overshoot reads as 10^3-10^4 x in RATE; in the physical late-burst model
      (Part 4b) it is 3-10 x in converted FRACTION.  The fraction number is the honest one -- the
      rate factors assume conversion running since recombination, which Route B does not do. ***""")
om_gap = (0.3143 - 0.2975)
om_gap_sig = om_gap / math.sqrt(0.0076 ** 2 + 0.0086 ** 2)
print(f"\n  the anomaly Route B is aligned with: Omega_m(CMB) - Omega_m(DESI BAO) = "
      f"{om_gap:+.4f} = {om_gap_sig:.2f} sigma")
frac_gap = om_gap / OM_DM
print(f"  as a converted fraction of the dust that would explain it: {frac_gap*100:.1f} %")
print(f"  Route B needs f ~ 0.3-0.9  ->  over by {0.3/frac_gap:.1f}x to {0.9/frac_gap:.1f}x")
print(f"  (and its L*-only FLOOR, f = 0.075, is only {0.075/frac_gap:.2f}x the anomaly -- i.e. the floor of what")
print(f"   Route B needs is essentially the size of a discrepancy that is already in the data)")
check(0.3 / frac_gap > 1.0,
      "Route B overshoots the anomaly it is aligned with",
      f"{0.3/frac_gap:.1f}x - {0.9/frac_gap:.1f}x")
check(all((-1.0 - need[(1.0, 1.0)] / (3.0 * ratio)) < w0 - 3 * sw0
          for w0, sw0, _, _ in DESI.values()),
      "Route B's w_eff(0) is far below every DESI w0 central value")


# ==============================================================================================
hdr("PART 6 -- WHAT ROUTE B DOES TO THE FRAMEWORK'S OWN a_0(z) LAW")
# ==============================================================================================
print(r"""
  a_0 = kappa c sqrt(G rho_Lambda)  =>  a_0(z)/a_0(0) = sqrt(rho_L(z)/rho_L0).
  Canonical (CPL) form, banked:  a_0(z)/a_0(0) = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z)).""")


def a0_cpl(z, w0, wa):
    return (1 + z) ** (1.5 * (1 + w0 + wa)) * math.exp(-1.5 * wa * z / (1 + z))


w0d, _, wad, _ = DESI["DR2+CMB+Pantheon+"]
zpk = wad / (1 + w0d + wad) - 1.0
print(f"\n  CANONICAL, DESI DR2+CMB+Pantheon+ (w0={w0d}, wa={wad}):")
print(f"    bump peak at z = {zpk:.3f}, height = {a0_cpl(zpk, w0d, wad):.4f}  "
      f"(+{100*(a0_cpl(zpk,w0d,wad)-1):.1f}%)")
for z in [0.3, 1.0, 3.0]:
    print(f"    a_0({z})/a_0(0) = {a0_cpl(z, w0d, wad):.4f}")
check(a0_cpl(zpk, w0d, wad) > 1.0,
      "canonical law has a BUMP -- and the bump exists ONLY because w0 > -1")

print("\n  ROUTE B:  rho_L grows monotonically with time  =>  a_0 declines monotonically in z, NO BUMP.")
print(f"\n  {'z':>6} " + " ".join(f"{lab.split(',')[0]+lab.split(',')[1]:>22}"
                                  for _, lab in rows[:2]) + f" {'the 95% bound':>16}")
for z in [0.1, 0.3, 1.0, 3.0]:
    a = 1.0 / (1 + z)
    cells = []
    for b, _ in rows[:2]:
        r = rho_L_of_a(a, b) / OM_L
        cells.append(f"{'IMAGINARY (rho_L<0)':>22}" if r < 0 else f"{math.sqrt(r):>22.4f}")
    r95 = rho_L_of_a(a, DELTA_95) / OM_L
    print(f"  {z:>6.2f} " + " ".join(cells) + f" {math.sqrt(r95):>16.5f}")

r95_z3 = math.sqrt(rho_L_of_a(0.25, DELTA_95) / OM_L)
print(f"""
  THREE INTERNAL COSTS, stated plainly:

  (1) NO BUMP.  The canonical a_0(z) bump (+{100*(a0_cpl(zpk,w0d,wad)-1):.1f}% at z~{zpk:.2f}) exists only because
      w0 > -1.  Route B forbids w0 > -1 identically.  *** Route B and the canonical a_0(z) law
      cannot both be true. ***  The law takes DESI's (w0, wa) as INPUT; Route B claims to be the
      CAUSE of the DE evolution and its cause can only ever give w < -1.  The pre-registered
      section 11 shape (bump at z~0.4, +6%) would have to be amended.

  (2) AT THE REQUIRED RATE THE LAW HAS NO VALUES.  rho_L < 0 for z > {z_cross['f=1.0, tau=1.0 Gyr']:.3f} (tau=1 Gyr)
      or z > {z_cross['f=0.08, tau=2.43 Gyr']:.3f} (most conservative case), so a_0(z) is imaginary across most of
      the data.  This is not a tension, it is a breakdown.

  (3) AT THE ALLOWED RATE IT IS INVISIBLE.  a_0(z=3)/a_0(0) = {r95_z3:.5f} -- a {100*(1-r95_z3):.2f}% effect,
      against a committed observational floor of 0.30 dex.  So Route B cannot be the mechanism
      behind ANY a_0(z) signal either.

  ONE GENUINE STRUCTURAL ATTRACTION, recorded because it is real:  Route B makes rho_Lambda small
  in the past FOR A REASON, and stage8's escape needs exactly that ('MOND switched off at
  recombination').  Route B would supply that feature from the mechanism instead of borrowing it
  from DESI's CPL fit.  But stage8 derives it USING w0 = -0.75 > -1, which Route B forbids -- so
  stage8's arithmetic and Route B are alternative derivations, not compatible ones.""")
check(r95_z3 > 0.99, "at the allowed rate Route B's a_0(z) effect is sub-percent",
      f"a_0(3)/a_0(0) = {r95_z3:.5f}")


# ==============================================================================================
hdr("PART 7 -- VERDICT")
# ==============================================================================================
print(f"""
  ROUTE B (dust -> dark energy) FAILS as a solution to the galaxy problem -- but it fails on the
  CONVERTED FRACTION, not on the leak rate, and it fails much more narrowly than my prior
  write-up claimed.  It is the most nearly-viable route in this sequence so far.

  THE DECIDING NUMBER (fair, theta_*-anchored, h solved for, conversion switched on at z_conv):
    allowed  f <= {F_ALLOWED:.3f}     (2 sigma, MOST GENEROUS corner: DESI DR2 BAO alone, z_conv=0.5;
                              Pantheon+ SN alone tightens this to f <= 0.040)
    needed   f ~= 0.3-0.5   (all galaxy-scale halos)
             f ~= 0.7-0.9   (EVERY halo -- what the framework's smooth-accretion theorem says)
             f  = 0.075     is a FLOOR: L*-galaxies only, at the lowest plausible number density
    short by {0.3/F_ALLOWED:.1f}x to {0.9/F_ALLOWED:.1f}x.
    consequences at z_conv = 1: f=0.3 -> Omega_m(0) = {fair[(0.3,1.0)][1]:.4f} ({abs(fair[(0.3,1.0)][3]):.0f} sigma), H0 = {fair[(0.3,1.0)][0]:.1f}
                                f=0.9 -> Omega_m(0) = {fair[(0.9,1.0)][1]:.4f} ({abs(fair[(0.9,1.0)][3]):.0f} sigma), H0 = {fair[(0.9,1.0)][0]:.1f}
    plus rho_L,pre < 0 (negative pre-existing vacuum energy) for f >~ 0.2 at z_conv = 2.

  A SECOND, INDEPENDENT AXIS -- but it only bites the SMOOTH variant:
    if the conversion is smooth in time (rho_d ~ a^(-3+delta), the form the literature fits),
    Route B needs |delta| = {need[(0.08, TAU_FF_LSTAR)]:.3f}-{need[(1.0, 1.0)]:.2f} against |delta_0| <= {DELTA_95:.5f} (95% CL,
    arXiv:2504.00994) = {worst:.0f}x-{d_max/DELTA_95:.0f}x too fast, and rho_Lambda < 0 for z > {z_cross['f=1.0, tau=1.0 Gyr']:.2f}-{z_cross['f=0.08, tau=2.43 Gyr']:.2f}.
    *** Do NOT quote those factors against the physical late-burst model.  They are the same
    information as the f bound, in a parametrisation that assumes conversion since recombination. ***

  THREE CORRECTIONS TO MY OWN PRIOR WRITE-UP, ALL AGAINST INTEREST
    - the '47x drift' arithmetic is right (exp(10/2.594) = 47.3) but its stated MECHANISM was
      wrong: it assumed exponential growth at fixed fractional rate = an unbounded dust reservoir.
      47x IS reachable, by converting all the dust at z = {zc_exact:.2f}.  What kills it is that the
      pre-existing vacuum energy would then have to be {pre_at_47:.1f} x rho_L0.  And 'the leak rates
      lock at Gamma_n/Gamma_V = 2.60' is not a lock at all -- 2.60 is just today's density ratio.
    - my first pass at this script scored Route B at ~70 sigma by extrapolating the power law
      back to recombination, which destroys all the dust.  That was a MANUFACTURED DEFICIT.  The
      fair number is {abs(fair[(0.3,1.0)][3]):.0f}-{abs(fair[(0.9,1.0)][3]):.0f} sigma, and f = 0.08 is not excluded at all.
    - the 690 Gyr khronon-transport bound is NOT what excludes Route B, and the brief was right
      to flag it as possibly the wrong speed.  Route B does not need slow transport to fail; it
      fails on the background energy budget, which is transport-speed-independent.  A relativistic
      decay channel makes the smooth-fork bound apply HARDER, not softer.

  WHAT ROUTE B GETS RIGHT (three things, and none of them should be buried)
    1. SIGN.  Every interacting fit of the DESI-era data mildly prefers dust -> dark energy:
       delta_0 = -0.00050 +/- 0.00033 (arXiv:2504.00994), epsilon = -0.0073 +0.0029/-0.0033
       (arXiv:2505.09879), xi = -0.132 +0.087/-0.064 (arXiv:2503.23225), at 1.5-2.4 sigma.
       Route B is pointed the right way.
    2. It is aligned with a real {om_gap_sig:.1f} sigma anomaly (Omega_m: CMB 0.3143+/-0.0076 vs DESI DR2
       BAO 0.2975+/-0.0086), whose size in converted-dust units is {frac_gap*100:.1f}% -- and Route B's own
       L*-only floor is 7.5%.  *** The floor of what Route B needs is within a factor 1.2 of the
       size of an anomaly that already exists in the data. ***
    3. H0.  f ~ 0.2 at z_conv ~ 1 gives H0 = {fair[(0.2,1.0)][0]:.1f}, i.e. 0.6 sigma from SH0ES.  Route B is a
       live Hubble-tension mechanism.  It is Omega_m that kills it, not H0.

  SO THE HONEST SHAPE OF THE RESULT
    Route B is viable at f <~ 0.1 and needed at f ~ 0.3-0.9.  It can clear the L*-only floor of
    the dust and nothing beyond it.  Since the framework's own smooth-accretion theorem says
    EVERY halo captures the dust, clearing 10% of it does not deliver 'no dark matter in
    galaxies' -- it leaves 90% of the captured share exactly where stages 3-7 found it.
    *** Route B is EXCLUDED as THE mechanism, and is NOT excluded as a real sub-dominant
    component of the dark sector at the ~5-10% level. Those are different claims; keep them apart. ***

  WHAT WOULD CHANGE THE VERDICT
    Route B is defined as moving energy between the background dust and the background vacuum, so
    the expansion history always sees it and no tuning inside Route B escapes the f bound.  A
    genuine escape must clear halos WITHOUT that transfer.  This does NOT close the wider problem:
    stage8's 'the dust never clusters in the first place' route is untouched by everything here,
    because it never puts the energy in the galaxy and so never has to take it out.""")

print("\n" + "-" * 98)
print("SOURCES")
print("-" * 98)
for k, v in SRC.items():
    print(f"  {k}\n      <- {v}")

print("\n" + "=" * 98)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED: " + "; ".join(FAIL))
    sys.exit(1)
print("=" * 98)
