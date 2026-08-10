#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage8_routeA_dust_to_dark_radiation_2026.py
============================================
ROUTE A: BREAK THE SHIFT SYMMETRY WITH A Y-GATE SO THE DUST DECAYS TO DARK RADIATION,
WHICH LEAVES THE GALAXY AT c.

Stage 5's theorem said the dust mass IS the conserved shift charge, so it can only be MOVED or
made NON-conserved.  Stage 6 Part C said moving it fails because transport at the sector's own
polytropic sound speed needs 690 Gyr to cross 1 Mpc.  Route A attacks exactly that step: if the
broken-symmetry decay channel is RELATIVISTIC, the carrier speed is c, not c_s.

*** AND THAT PART WORKS. ***  Radiation crosses 1 Mpc in 3.26 Myr, which beats the 690 Gyr
polytropic bound by 2.1e5.  The local target rho -> 0 -- the ONLY configuration invisible to both
dynamics (rho+3p) and lensing (rho+p) -- is genuinely reachable inside a galaxy.  Route A is the
first mechanism in the whole sequence that defeats stage 6 Part C on its own terms.

*** AND THEN GLOBAL ENERGY BOOKKEEPING KILLS IT. ***  "Escapes the galaxy" is not "leaves the
universe."  grad_mu T^{mu nu} = 0 does not care that the carrier is fast: the energy lands in a
smooth cosmological dark-radiation bath whose density is measured.  This script computes the
required rate, the per-galaxy luminosity, and the cosmological cost, and confronts the published
DM -> DR bounds.

THE SHARPEST RESULT IS NOT THE KILL, IT IS THAT THE GATE IS ADVERSE, NOT NEUTRAL.
The Y-gate's selling point is that Y = 0 identically on FRW, so recombination-era N_eff is untouched
EXACTLY.  That is a real win and it is preserved here.  But the same gate FORCES the conversion to
happen only after halos exist (z <~ 3-10), which is precisely the epoch at which a^-4 dilution has
the least time to act.  The gate buys immunity at recombination by moving the injection to the
worst possible redshift.  A hypothetical UNGATED early conversion at z = 99 would dilute to
Omega_dr,0 = 0.0027; the gate forces Omega_dr,0 = 0.196.  The protection costs a factor 74.

PUBLISHED BOUNDS CONFRONTED (all 95% C.L.):
  [1] Audren, Lesgourgues, Mangano, Serpico, Tram, JCAP 12 (2014) 028, arXiv:1407.2418
      100% of CDM -> invisible relativistic daughters:  tau > 160 Gyr (Planck+WP+WiggleZ+BAO),
      200 Gyr including BICEP2.
  [2] Nygaard, Tram, Hannestad, JCAP (2021), arXiv:2011.01632, "Updated constraints on decaying
      cold dark matter":  f_dcdm < 2.44% (Planck 2018 alone, long-lived), < 1.49% (Planck 2018 +
      BOSS DR12 BAO, short-lived).
  [3] Simon, Franco Abellan, Du, Poulin, Tsai, PRD 106 (2022) 023516, arXiv:2203.07440
      (Planck + BOSS-DR12 under EFTofLSS + Pantheon + BAO):
      f_dcdm <~ 0.022 for tau < age of universe;  tau/f_dcdm >~ 250 Gyr long-lived.
  [4] arXiv:2205.05636, "Do you smell something decaying? Updated linear constraints on decaying
      dark matter scenarios" (Planck 2018 TT,TE,EE+lensing + 6dFGS/SDSS-DR7/BOSS-DR12/eBOSS-DR16
      BAO):  Gamma_dm < 0.129e-18 s^-1, i.e. tau_dm > 246 Gyr.
  [5] *** THE DECISIVE ONE, because it is the LATE-TIME-MARGINALISED version and therefore the
      one a halo gate has to answer: *** McCarthy & Hill, PRD 108 (2023) 063501, arXiv:2210.14339,
      "Converting dark matter to dark radiation does not solve cosmological tensions."  They
      generalise DDM by letting the conversion happen at ANY rate and ANY epoch since
      recombination (transition scale factor a_t marginalised, a_t > 1e-4), and get on the
      converted fraction zeta:
          zeta < 0.0204   (Planck primary CMB)
          zeta < 0.0374   (Planck + lensing + BAO + SN + DES)
          zeta < 0.0321   (+ SH0ES)
      Driver: reduced CMB-lensing peak smearing, and EXCESS ISW from the extra dark energy needed
      to restore flatness after matter is converted away.  The CMB-only posterior peaks at
      zeta = 0 exactly.

Run:  python3 stage8_routeA_dust_to_dark_radiation_2026.py
"""

import sys
import mpmath as mp

mp.mp.dps = 30
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(("  [PASS] " if ok else "  [FAIL] ") + label + (("   " + detail) if detail else ""))
    if not ok:
        FAIL.append(label)


def hdr(t):
    print("\n" + "=" * 98)
    print(t)
    print("=" * 98)


# ----------------------------------------------------------------------------------------------
# CONSTANTS  (CODATA / IAU / Planck 2018 TT,TE,EE+lowE+lensing+BAO)
# ----------------------------------------------------------------------------------------------
c = mp.mpf("2.99792458e8")           # m/s
G = mp.mpf("6.67430e-11")            # m^3/kg/s^2
Msun = mp.mpf("1.98892e30")          # kg (IAU nominal 1.98892e30 used by SPARC-era work)
Lsun = mp.mpf("3.828e26")            # W  (IAU nominal solar luminosity)
Mpc = mp.mpf("3.0856775814913673e22")  # m
kpc = Mpc / 1000
yr = mp.mpf("3.1557e7")              # s (Julian year)
Gyr = mp.mpf("1e9") * yr

h = mp.mpf("0.6736")                 # Planck 2018 base
H0 = 100 * h * mp.mpf("1000") / Mpc  # s^-1
rho_crit = 3 * H0**2 / (8 * mp.pi * G)
Om_m = mp.mpf("0.3153")
Om_b = mp.mpf("0.04930")
Om_dm = mp.mpf("0.2645")             # cold/pressureless component the CMB demands (banked)
Om_L = mp.mpf("0.6847")
Om_gam = mp.mpf("2.47282e-5") / h**2  # photons today
# one massless neutrino species worth of energy density (for a Delta N_eff-equivalent yardstick)
Om_per_Neff = mp.mpf("0.2271") * Om_gam
t_H = mp.mpf("13.797") * Gyr         # Planck 2018 age

# BANKED FRAMEWORK NUMBERS (given, from committed prior stages)
tau_ff = mp.mpf("2.43") * Gyr        # free-fall time of an L* basin, MOND-boosted, 1 Mpc
M_cap = mp.mpf("2.51e12") * Msun     # captured dust share per L* galaxy
L_star_stellar = mp.mpf("2e10") * Lsun
t_transport_polytropic = mp.mpf("690") * Gyr  # stage 6 Part C bound
Mb_Lstar = mp.mpf("6e10") * Msun     # baryonic mass of an L* galaxy (stars+gas), for the residual test

print(__doc__)

# ==============================================================================================
hdr("PART 0 -- THE ONE THING ROUTE A GETS RIGHT: THE CARRIER SPEED")
# ==============================================================================================
t_cross_c = Mpc / c
print(f"  1 Mpc at c                          = {float(t_cross_c/ (mp.mpf('1e6')*yr)):.3f} Myr")
print(f"  1 Mpc at the polytropic c_s (banked)= {float(t_transport_polytropic/Gyr):.1f} Gyr")
gain = t_transport_polytropic / t_cross_c
print(f"  speed-up of the escape channel      = {float(gain):.3e}")
check(t_cross_c < mp.mpf("5e6") * yr, "radiation crosses 1 Mpc in < 5 Myr",
      f"{float(t_cross_c/(mp.mpf('1e6')*yr)):.2f} Myr")
check(gain > mp.mpf("1e5"), "Route A defeats stage 6 Part C's 690 Gyr transport bound",
      f"by {float(gain):.2e}")
print("  => the LOCAL step of Route A is sound.  rho -> 0 in the galaxy is reachable.")
print("     Note also: rho+p = (4/3)rho != 0 for radiation, so the stage-6 lensing theorem is NOT")
print("     evaded by the equation of state -- it is evaded only because the energy is GONE from")
print("     the galaxy.  Which means it must be somewhere else.  Part 3 finds out where.")

# ==============================================================================================
hdr("PART 1 -- THE REQUIRED DECAY RATE AND CONVERTED FRACTION")
# ==============================================================================================
# (1a) weak requirement: merely outrun the collapse
tau_weak = tau_ff
Gam_weak = 1 / tau_weak
f_conv_H = 1 - mp.e**(-t_H / tau_weak)
print(f"  (1a) WEAK requirement -- beat free-fall so collapse never completes:")
print(f"       tau <= tau_ff                  = {float(tau_weak/Gyr):.2f} Gyr")
print(f"       Gamma >= 1/tau_ff              = {float(Gam_weak):.4e} s^-1")
print(f"       fraction converted in t_H      = 1 - exp(-{float(t_H/tau_weak):.3f}) = {float(f_conv_H*100):.3f} %")
check(f_conv_H > mp.mpf("0.99"), "the weak requirement already converts >99% of the captured dust",
      f"{float(f_conv_H*100):.2f}%")

# (1b) real requirement: leave a residual small enough that the galaxy is actually dust-free.
# Continuous accretion of M_cap over t_H, drained at rate 1/tau  =>  standing mass ~ Mdot*tau.
Mdot = M_cap / t_H
print(f"\n  (1b) REAL requirement -- the residual STANDING dust mass must be negligible.")
print(f"       mean accretion rate            = {float(Mdot/(Msun/yr)):.1f} Msun/yr")
M_stand_weak = Mdot * tau_weak
print(f"       standing mass at tau = 2.43 Gyr= {float(M_stand_weak/Msun):.3e} Msun "
      f"= {float(M_stand_weak/Mb_Lstar):.2f} x the L* baryonic mass")
check(M_stand_weak > Mb_Lstar, "tau = tau_ff does NOT clear the galaxy -- it only stops runaway",
      f"residual is {float(M_stand_weak/Mb_Lstar):.1f} x M_baryon")
resid_target = mp.mpf("0.10") * Mb_Lstar     # allow 10% of baryons as invisible-enough
tau_real = resid_target / Mdot
print(f"       for residual <= 10% of baryons ({float(resid_target/Msun):.2e} Msun):")
print(f"         tau <= {float(tau_real/(mp.mpf('1e6')*yr)):.1f} Myr   (Gamma >= {float(1/tau_real):.3e} s^-1)")
print(f"       => the honest required lifetime window is  {float(tau_real/(mp.mpf('1e6')*yr)):.0f} Myr "
      f"<= tau <= {float(tau_weak/Gyr):.2f} Gyr.")
print(f"          Everything below uses the FRAMEWORK-FAVOURABLE end, tau = {float(tau_weak/Gyr):.2f} Gyr.")

# ==============================================================================================
hdr("PART 2 -- THE LUMINOSITY OF AN L* GALAXY IN DARK RADIATION")
# ==============================================================================================
L_peak = M_cap * c**2 / tau_weak          # if the whole captured share drains on one e-fold
L_ss = M_cap * c**2 / t_H                 # steady state: accretion-rate-limited (the long-term mean)
print(f"  peak / one-e-fold luminosity   L = M_cap c^2 / tau  = {float(L_peak):.3e} W")
print(f"  steady-state (accretion-limited) L = M_cap c^2 / t_H = {float(L_ss):.3e} W")
print(f"  L* stellar luminosity (2e10 Lsun)                    = {float(L_star_stellar):.3e} W")
print(f"  RATIO  peak / stellar        = {float(L_peak/L_star_stellar):.3e}")
print(f"  RATIO  steady / stellar      = {float(L_ss/L_star_stellar):.3e}")
L_quasar = mp.mpf("1e40")   # 1e47 erg/s, a bright quasar
print(f"  for scale: a bright quasar is ~1e40 W, so this is {float(L_ss/L_quasar):.0f}-{float(L_peak/L_quasar):.0f}"
      f" quasars per galaxy, running for 10 Gyr")
check(L_ss / L_star_stellar > mp.mpf("1e4"),
      "every galaxy must be a 1e42 W dark-radiation source, >1e5 x its starlight",
      f"{float(L_ss/L_star_stellar):.2e}")

# is the radiation IN TRANSIT gravitationally harmless?  (a point in the framework's favour)
r_probe = 20 * kpc
u_transit = L_ss / (4 * mp.pi * r_probe**2 * c)      # J/m^3 of an outward-streaming flux
rho_transit = u_transit / c**2
rho_DM_20kpc = mp.mpf("0.01") * Msun / (mp.mpf("3.0857e16"))**3   # 0.01 Msun/pc^3 -> kg/m^3
print(f"\n  in-transit DR energy density at 20 kpc  rho = L/(4 pi r^2 c^3) = {float(rho_transit):.3e} kg/m^3")
print(f"  local halo density scale (0.01 Msun/pc^3)                       = {float(rho_DM_20kpc):.3e} kg/m^3")
print(f"  ratio = {float(rho_transit/rho_DM_20kpc):.3e}")
check(rho_transit / rho_DM_20kpc < mp.mpf("1e-3"),
      "IN THE FRAMEWORK'S FAVOUR: the radiation in transit is gravitationally negligible",
      f"{float(rho_transit/rho_DM_20kpc):.2e} of the local halo density")

# ==============================================================================================
hdr("PART 3 -- THE COSMOLOGICAL COST (the real test)")
# ==============================================================================================
print("  Bookkeeping.  Convert a fraction f of Omega_dm at scale factor a_c.  The converted")
print("  energy then dilutes as a^-4 instead of a^-3, so today")
print("      Omega_dr,0 = f * Omega_dm * a_c          (exact for instantaneous conversion)")
print("  because rho_dr(a_c) = f rho_dm,0 a_c^-3 and rho_dr(1) = rho_dr(a_c) a_c^4.\n")


def Om_dr_instant(f, a_c):
    return f * Om_dm * a_c


rows = [("z=10 (first structures)", mp.mpf(1) / 11),
        ("z=3", mp.mpf("0.25")),
        ("z=2  (bulk of halo assembly)", mp.mpf(1) / 3),
        ("z=1", mp.mpf("0.5")),
        ("z=0.5", mp.mpf(1) / mp.mpf("1.5")),
        ("z=0", mp.mpf(1))]
print(f"  {'epoch of conversion':32s} {'a_c':>7s}  {'Om_dr,0 (f=1)':>14s} {'(f=0.6)':>10s}"
      f" {'x Om_r,0':>10s} {'DN_eff-equiv':>13s}")
Om_r0 = Om_gam * (1 + 3 * mp.mpf("0.2271"))    # photons + 3 nu
for lab, a_c in rows:
    o1 = Om_dr_instant(1, a_c)
    o6 = Om_dr_instant(mp.mpf("0.6"), a_c)
    print(f"  {lab:32s} {float(a_c):7.4f}  {float(o1):14.5f} {float(o6):10.5f}"
          f" {float(o1/Om_r0):10.1f} {float(o1/Om_per_Neff):13.0f}")

# gradual halo assembly, decay upon capture with the 2.43 Gyr delay folded in:
# Omega_dr,0 = Omega_dm * Int f_coll'(a) * a_eff(a) da, with a_eff the scale factor AT DECAY.
# f_coll rises linearly from 0 at a=0.2 (z=4) to f_h at a=1; delay of tau pushes a_eff up.
def Om_dr_gradual(f_h, a_start=mp.mpf("0.2"), delay=tau_weak):
    # crude but conservative: map capture time -> decay time through a matter-dominated a(t)
    N = 2000
    tot = mp.mpf(0)
    fprime = f_h / (1 - a_start)
    for i in range(N):
        a = a_start + (1 - a_start) * (mp.mpf(i) + mp.mpf("0.5")) / N
        da = (1 - a_start) / N
        # t(a) in a flat matter+Lambda background
        t_a = (2 / (3 * H0 * mp.sqrt(Om_L))) * mp.asinh(mp.sqrt(Om_L / Om_m) * a**mp.mpf("1.5"))
        t_d = t_a + delay
        arg = mp.sinh(3 * H0 * mp.sqrt(Om_L) * t_d / 2)
        a_d = (mp.sqrt(Om_m / Om_L) * arg)**(mp.mpf(2) / 3)
        a_d = min(a_d, mp.mpf(1))            # anything not yet decayed by today is still dust
        tot += fprime * a_d * da
    return Om_dm * tot


for f_h in [mp.mpf("0.6"), mp.mpf("1.0")]:
    o = Om_dr_gradual(f_h)
    print(f"\n  GRADUAL assembly, f_halo={float(f_h):.1f}, tau=2.43 Gyr delay:"
          f"  Omega_dr,0 = {float(o):.4f}"
          f"  ({float(o/Om_r0):.0f} x today's photon+nu background,"
          f" DN_eff-equiv {float(o/Om_per_Neff):.0f})")

Om_dr_fid = Om_dr_gradual(mp.mpf("1.0"))
Om_dr_conserv = Om_dr_instant(mp.mpf("0.6"), mp.mpf(1) / 11)   # most favourable case in the table
print(f"\n  FIDUCIAL   Omega_dr,0 = {float(Om_dr_fid):.4f}")
print(f"  MOST FAVOURABLE possible (f=0.6, everything converted as early as z=10):"
      f" Omega_dr,0 = {float(Om_dr_conserv):.4f}")
check(Om_dr_fid > mp.mpf("0.05"), "fiducial Omega_dr today is a PERCENT-OF-CRITICAL-scale component",
      f"{float(Om_dr_fid):.3f}")

# what is left of the matter budget, and what flatness then demands
print("\n  Consequences for the low-z budget (f = 1, fiducial):")
Om_m_left = Om_b + Om_dm * 0
print(f"    Omega_m(z=0) left            = {float(Om_m_left):.4f}   (baryons only)")
print(f"    Omega_dr(z=0)                = {float(Om_dr_fid):.4f}")
tot_no_refit = Om_m_left + Om_dr_fid + Om_L
print(f"    total without refit          = {float(tot_no_refit):.4f}  -> "
      f"Omega_k = {float(1-tot_no_refit):.4f}")
Om_L_needed = 1 - Om_m_left - Om_dr_fid
print(f"    Omega_Lambda needed for flat = {float(Om_L_needed):.4f} "
      f"(vs {float(Om_L):.4f}), i.e. +{float((Om_L_needed/Om_L-1)*100):.1f}%  <-- McCarthy & Hill's"
      " excess-ISW driver")

# confront Omega_m measurements that are LOW-z and geometric (so no force-law loophole)
meas = [("Planck18 TT,TE,EE+lowE+lensing+BAO", mp.mpf("0.3153"), mp.mpf("0.0073")),
        ("DESI DR1 BAO alone (2024)", mp.mpf("0.295"), mp.mpf("0.015")),
        ("Pantheon+ SNe alone (Brout+22)", mp.mpf("0.334"), mp.mpf("0.018"))]
print("\n  Omega_m(z=0) confrontation -- these are BACKGROUND-EXPANSION measurements, so a modified")
print("  force law cannot supply them:")
for lab, mu, sig in meas:
    nsig = (mu - Om_m_left) / sig
    print(f"    {lab:38s} Om_m = {float(mu):.4f} +/- {float(sig):.4f}"
          f"  ->  {float(nsig):6.1f} sigma discrepancy")
    check(nsig > 5, f"Omega_m kill vs {lab}", f"{float(nsig):.1f} sigma")

# ==============================================================================================
hdr("PART 4 -- DOES THE HALO GATE WEAKEN THE BOUNDS?")
# ==============================================================================================
print("  WHAT THE GATE GENUINELY BUYS (and it is real, and exact):")
print("    Y = 0 identically on FRW, and Y is second order in perturbations, so N_eff at")
print("    recombination and BBN is untouched IDENTICALLY, not approximately.  Every bound that")
print("    is really a bound on pre-recombination dark radiation is evaded exactly.  That kills")
print("    the BBN/CMB DN_eff channel as a constraint.  Correct, and it should be banked.\n")
print("  WHAT IT DOES NOT BUY:")
print("    (i) The decisive published bound is ALREADY marginalised over conversion epoch.")
print("        McCarthy & Hill (arXiv:2210.14339, PRD 108 063501) let a_t float over the whole")
print("        post-recombination range and constrain the converted FRACTION zeta directly.")
zeta_bounds = [("Planck primary CMB", mp.mpf("0.0204")),
               ("Planck+lensing+BAO+SN+DES", mp.mpf("0.0374")),
               ("  ... + SH0ES", mp.mpf("0.0321"))]
# effective global conversion fraction implied by the framework
# cross-check: what cosmic volume does 2.51e12 Msun of DM correspond to?
rho_dm0 = Om_dm * rho_crit
V_per = M_cap / rho_dm0
print(f"\n    cross-check on the banked capture: 2.51e12 Msun of DM occupies"
      f" {float(V_per/Mpc**3):.1f} Mpc^3 of cosmic volume,")
R_equiv = (3 * V_per / (4 * mp.pi))**(mp.mpf(1) / 3)
print(f"    i.e. a sphere of radius {float(R_equiv/Mpc):.2f} Mpc, or one L* galaxy per"
      f" {float(V_per/Mpc**3):.0f} Mpc^3 (n = {float(Mpc**3/V_per):.2e} Mpc^-3).")
print(f"    With Schechter Phi* ~ (1.5-6)e-3 Mpc^-3 the L*-basin share alone is 11%-45% of the")
print(f"    cosmic dark-matter budget -- and the remainder sits in dwarfs, groups and clusters,")
print(f"    where the SAME gate fires.  So the per-galaxy number is a geometry check, not the")
print(f"    global fraction; the global fraction is set by the collapsed fraction.")
print(f"\n    Independently: ~60% of dark matter is in bound halos at z=0 in LCDM N-body")
print(f"    (out-of-halo fraction ~40%), and the AeST dust has c_s = 1.4 m/s at the cosmic mean")
print(f"    so its free-streaming/Jeans scale is nil -- it is captured wherever anything collapses,")
print(f"    and the Y-gate is on in filaments and infall regions too, not just virial radii.")
print(f"    => f_global in [0.6, 1.0].  Take the framework-favourable 0.6.\n")
f_global_fav = mp.mpf("0.60")
for lab, zb in zeta_bounds:
    print(f"    zeta < {float(zb):.4f} ({lab:26s}) vs required {float(f_global_fav):.2f}"
          f"  ->  over by {float(f_global_fav/zb):5.1f} x")
    check(f_global_fav / zb > 5, f"zeta bound violated ({lab})", f"{float(f_global_fav/zb):.1f} x")

print("\n    (i-b) AND THERE IS NO THIRD OPTION FOR THE DAUGHTER.  If the relativistic daughter were")
print("          Standard-Model radiation instead of a dark species, the same energy would land in")
print("          the extragalactic background light:")
u_dr = Om_dr_fid * rho_crit * c**2
I_dr = u_dr * c / (4 * mp.pi)                      # W/m^2/sr for an isotropic bath
I_EBL = mp.mpf("1e-7")                             # ~100 nW/m^2/sr observed COB+CIB
print(f"          Omega_dr = {float(Om_dr_fid):.3f} as photons -> I = {float(I_dr):.3e} W/m^2/sr")
print(f"          observed cosmic optical+infrared background ~ {float(I_EBL):.1e} W/m^2/sr")
print(f"          ratio = {float(I_dr/I_EBL):.2e}")
check(I_dr / I_EBL > mp.mpf("1e3"), "a VISIBLE daughter is excluded by the EBL, so 'dark' is FORCED",
      f"{float(I_dr/I_EBL):.1e} x the observed background")
print("          => the daughter must be DARK, which is exactly why the DDM->DR bounds above are")
print("             the right bounds to apply.  The two options close on each other.")

print("\n    (ii) The gate is not merely unhelpful, it is ADVERSE.  Dilution of the injected")
print("         radiation goes as a_c, so the LATER the injection the WORSE the leftover.  A halo")
print("         gate cannot fire before halos exist, which pins a_c to the least-diluting epoch:")
o_early = Om_dr_instant(1, mp.mpf("0.01"))     # a hypothetical ungated z=99 conversion
print(f"         hypothetical UNGATED conversion at z=99: Omega_dr,0 = {float(o_early):.5f}")
print(f"         gate-forced conversion (fiducial)      : Omega_dr,0 = {float(Om_dr_fid):.5f}")
print(f"         the recombination-era protection costs a factor {float(Om_dr_fid/o_early):.0f}"
      " in late-time dark radiation.")
check(Om_dr_fid / o_early > 10, "the Y-gate is ADVERSE, not neutral, for the late-time budget",
      f"factor {float(Om_dr_fid/o_early):.0f}")

print("\n    (iii) Lifetime bounds, for completeness (these assume f = 1 or scale as tau/f):")
tau_bounds = [("Audren+2014 (arXiv:1407.2418)", mp.mpf("160")),
              ("Audren+2014 incl. BICEP2", mp.mpf("200")),
              ("arXiv:2205.05636 (Planck18+4xBAO)", mp.mpf("246")),
              ("Simon+2022 tau/f > 250 Gyr, f=0.6", mp.mpf("250") * f_global_fav)]
for lab, tb in tau_bounds:
    print(f"         {lab:38s} tau > {float(tb):6.1f} Gyr   vs required"
          f" <= {float(tau_weak/Gyr):.2f} Gyr  ->  {float(tb*Gyr/tau_weak):6.1f} x too short")
    check(tb * Gyr / tau_weak > 20, f"lifetime bound violated ({lab})",
          f"{float(tb*Gyr/tau_weak):.0f} x")
print(f"         and against the REAL requirement (tau <= {float(tau_real/(mp.mpf('1e6')*yr)):.0f} Myr,"
      f" Part 1b): {float(mp.mpf('246')*Gyr/tau_real):.0f} x too short.")

print("\n    (iv) The growth/lensing channel is independent of all of the above.  Removing the")
print("         pressureless component after z~2 stops linear growth (nothing left to drive it)")
print("         and drops Omega_m by 6.4x, so the CMB lensing power C_l^phiphi ~ sigma8^2 Om_m^1.4")
print("         falls by more than an order of magnitude.  Planck 2018's lensing reconstruction is")
print("         a ~40 sigma detection with the amplitude measured to ~2.5%.  This is the")
print("         'reduced peak-smearing' half of McCarthy & Hill's kill and it has no gate-shaped")
print("         escape: CMB lensing integrates the matter distribution over 0 < z < 1100.")

# ==============================================================================================
hdr("PART 5 -- VERDICT")
# ==============================================================================================
print(f"  Required:   tau <= {float(tau_weak/Gyr):.2f} Gyr (to outrun collapse) and realistically")
print(f"              tau <= {float(tau_real/(mp.mpf('1e6')*yr)):.0f} Myr (to actually empty the galaxy);")
print(f"              {float(f_conv_H*100):.1f}% of the captured 2.51e12 Msun converted;")
print(f"              L = {float(L_ss):.2e} - {float(L_peak):.2e} W per L* galaxy"
      f" = {float(L_ss/L_star_stellar):.1e} - {float(L_peak/L_star_stellar):.1e} x its starlight.")
print(f"  Delivered:  Omega_dr,0 = {float(Om_dr_fid):.3f} fiducial"
      f" (>= {float(Om_dr_conserv):.3f} even in the most favourable corner),")
print(f"              converted fraction zeta = 0.6 - 1.0,")
print(f"              Omega_m(z=0) = {float(Om_m_left):.3f} against"
      f" {float(meas[1][1]):.3f} +/- {float(meas[1][2]):.3f} from DESI BAO alone.")
print(f"  Bound:      zeta < 0.0374 (95% C.L., epoch-marginalised, McCarthy & Hill 2023).")
print(f"  Margin:     {float(f_global_fav/mp.mpf('0.0374')):.0f} x on the fraction;"
      f" {float(mp.mpf('246')*Gyr/tau_weak):.0f} x on the lifetime;"
      f" {float((meas[1][1]-Om_m_left)/meas[1][2]):.0f} sigma on Omega_m.")
print("\n  ROUTE A IS EXCLUDED -- but note precisely WHERE it fails, because the failure is not")
print("  where stage 6 predicted.  Stage 6 said the energy cannot LEAVE the galaxy.  Route A")
print("  shows it can: at c, in 3.26 Myr, beating the polytropic bound by 2.1e5.  Stage 6 Part C")
print("  is therefore WRONG as a general statement and should be amended -- the transport bound")
print("  is a bound on the POLYTROPIC channel only, not on the sector.")
print("  What kills Route A is that grad_mu T^{mu nu} = 0 is global.  The energy leaves the galaxy")
print("  and lands in the only place it can: a smooth cosmological bath.  And that bath's density")
print("  is a measured number.  'Invisible to dynamics and lensing LOCALLY' was achieved; the")
print(f"  price is {float(Om_dr_fid):.2f} of critical density in radiation and a universe with no matter in it.")
print("\n  What Route A leaves standing for the next attempt: the ONLY surviving structure is one")
print("  where the dust is never captured in the first place (so nothing has to be disposed of),")
print("  or where the broken-symmetry sink is NOT a new energy species at all.  Any mechanism that")
print("  DISPOSES of the captured 2.51e12 Msun per galaxy must put ~0.26 of critical density")
print("  somewhere between z~3 and now, and every place to put it is measured to a few percent.")

hdr(f"{NCHK[0] - len(FAIL)}/{NCHK[0]} CHECKS PASSED")
if FAIL:
    print("FAILED: " + "; ".join(FAIL))
    sys.exit(1)
print("All checks passed.")
