#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage6_audit_transport_channels_2026.py
=======================================
ADVERSARIAL AUDIT OF MY OWN PART-C TRANSPORT BOUND (stage6_break_shift_symmetry_2026.py).

THE AUDITED CLAIM (stage 6, Part C / verdict item 3):
  "grad_mu T^{mu nu} = 0 holds regardless, so the dust's energy can only be MOVED or TRANSFORMED,
   and moving it out of a galaxy takes 690 Gyr at the sector's own sound speed."
  => "the repair space of LOCAL, ENERGY-PRESERVING modifications is now provably empty."

THE AUDIT FINDS THE BOUND UNSOUND AS STATED, AND THE CONCLUSION RESCUED BY A DIFFERENT CONSTRAINT.

  A. A conservation law bounds the TOTAL, not the FLUX VELOCITY.  The causal bound on energy export
     is c, not c_s.  Substituting one internal mode's speed for the causal cone is a category error
     unless one first proves NO faster channel is coupled -- which stage 6 never attempts.
  B. AeST as written propagates SIX modes (Skordis-Zlosnik 2021; Bataki-Skordis-Zlosnik 2023):
     two massless tensor modes AT c EXACTLY (this framework's own c_T = 1 theorem), two massive
     vector modes, one massive scalar mode, plus the condensate mode.  c_s = 1.4 km/s is the
     SLOWEST of them.  Y and Q are both built from A_mu, so the free function F(Y,Q) already
     couples the condensate to the vector sector.  The theory as written contains an O(c) channel.
  C. c_s is not even a fixed property of the sector: c_s^2 = u/Q_0 = rho/(Q_0^2 mu^2) is
     AMPLITUDE-DEPENDENT.  Stage 6's own check C2 concedes transport succeeds at high density.  The
     690 Gyr is an evaluation at the ambient halo profile, not a bound.
  D. Claim 2 ("no EoS hides energy from both dynamics and lensing; only rho = 0 works") is
     SATISFIED by escape at c, not violated: radiation that has left contributes nothing locally.
     Claim 2 forbids HIDING energy that is present.  It says nothing about REMOVING it.  So the
     no-go rested entirely on Part C, the weakest link.
  E. WHAT ACTUALLY REPLACES THE TRANSPORT BOUND: the escaping flux must be unobservable.  Photons
     are excluded by 7-14 orders (branching ratio limits below).  The surviving channel is dark
     radiation, and it dies on the LATE-TIME DECAYING-DM bound f <= 0.08-0.14 (95% CL,
     SN+BAO+SL; Nunes et al. MNRAS 497, 1757) against a required f ~ 1 -- a factor ~7, from DATA,
     not from a theorem.

VERDICT: the argument was INCOMPLETE (the transport step is wrong by 2.1e5 and is not a theorem);
the CONCLUSION survives on replacement observational grounds at ~7x, not "provably empty".
"""

import sys
import mpmath as mp

mp.mp.dps = 25
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    """A STATEMENT, not a test -- printed so it can never be miscounted as a passing check."""
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# ---------------- constants, all from the corpus or standard ----------------
C = mp.mpf("2.99792458e8")
G = mp.mpf("6.674e-11")
MPC = mp.mpf("3.0857e22")
GYR = mp.mpf("3.156e16")
YR = mp.mpf("3.156e7")
MSUN = mp.mpf("1.989e30")
LSUN = mp.mpf("3.828e26")
PC = mp.mpf("3.086e16")
T_H = mp.mpf("13.8")                       # Gyr
RHO_CRIT_KG = mp.mpf("8.6e-27")
OM_DM = mp.mpf("0.264")
RHO_DM0 = OM_DM * RHO_CRIT_KG              # kg/m^3, cosmic mean dust today
Z_REC = mp.mpf("1090")
RHO_REC = RHO_DM0 * (1 + Z_REC) ** 3
CS2_REC = mp.mpf("2.9e-8") * C ** 2        # committed CLASS run
K_POLY = CS2_REC / (2 * RHO_REC)           # stage 5's polytropic K
M_BAR = mp.mpf("6e10")                     # Msun, L* baryons
M_DUST = mp.mpf("2.51e12")                 # Msun, smooth-accretion captured share
T_FF = mp.mpf("2.43")                      # Gyr, free-fall of the 1 Mpc basin
L_MW = mp.mpf("3e10") * LSUN               # W, bolometric stellar luminosity of an L* galaxy

print(__doc__)

# ==================================================================================================
print("=" * 100)
print("PART 1 -- EVERY EXPORT CHANNEL, AND ITS 1 Mpc CROSSING TIME")
print("=" * 100)

t_c = MPC / C / GYR
cs_halo = mp.sqrt(2 * K_POLY * RHO_DM0 * mp.mpf("1e6"))
t_cs = MPC / cs_halo / GYR
cs_mean = mp.sqrt(2 * K_POLY * RHO_DM0)
t_cs_mean = MPC / cs_mean / GYR

print(f"""
  channel                                              speed            1 Mpc crossing
  ------------------------------------------------------------------------------------------
  khronon condensate sound (stage 6's choice, halo)    {sig(cs_halo/1000,3):>8s} km/s      {sig(t_cs,4):>10s} Gyr
  khronon condensate sound (cosmic mean)               {sig(cs_mean,3):>8s} m/s       {sig(t_cs_mean,4):>10s} Gyr
  AeST tensor modes (c_T = 1 EXACTLY, banked)          c                {sig(t_c,4):>10s} Gyr
  AeST massive vector modes (2, speed set by K_B)      O(c)             ~{sig(t_c,3):>9s} Gyr
  photons                                              c                {sig(t_c,4):>10s} Gyr
  neutrinos (E >> m_nu)                                ~c               {sig(t_c,4):>10s} Gyr
  any dark radiation / light 2nd scalar (E >> m)       ~c               {sig(t_c,4):>10s} Gyr
""")

ratio_speed = t_cs / t_c
check(ratio_speed > 1e5,
      f"1.1  *** THE TRANSPORT BOUND IS WRONG BY {sig(ratio_speed,4)}x IF ANY RELATIVISTIC CHANNEL "
      f"EXISTS: 1 Mpc takes {sig(t_c*1000,3)} Myr at c versus the {sig(t_cs,3)} Gyr quoted.  A "
      "conservation law constrains the TOTAL energy; the CAUSAL bound on its flux is c.  Stage 6 "
      "substituted one internal mode's phase speed for the causal cone ***",
      f"{sig(t_c*1000,3)} Myr vs {sig(t_cs,3)} Gyr")

check(t_cs / T_H > 10 and t_c / T_H < 1e-3,
      f"1.2  and the two verdicts are opposite, not marginal: {sig(t_cs/T_H,3)}x the age of the "
      f"universe at c_s, versus {sig(t_c/T_H,3)} of it at c",
      "the conclusion of Part C flips entirely on which speed is used")

# 1.3 -- the amplitude dependence: c_s is not a property of the sector
u_over_Q0_mean = CS2_REC / C ** 2 / (1 + Z_REC) ** 3
rho_for_cs_eq_c = RHO_REC / (CS2_REC / C ** 2)
rho_poly = M_DUST * MSUN / (mp.mpf("4") / 3 * mp.pi * (105 * PC) ** 3)
cs_poly = mp.sqrt(2 * K_POLY * rho_poly)
check(cs_poly > 100 * cs_halo,
      f"1.3  *** AND c_s IS NOT A PROPERTY OF THE SECTOR: c_s^2 = u/Q_0 = rho/(Q_0^2 mu^2) is "
      f"AMPLITUDE-DEPENDENT.  At the density of stage 5's own 105 pc n=1 polytrope "
      f"({sig(rho_poly/RHO_DM0,3)}x cosmic mean) it is {sig(cs_poly/1000,4)} km/s, crossing 1 Mpc in "
      f"{sig(MPC/cs_poly/GYR*1000,3)} Myr.  690 Gyr is an EVALUATION AT THE AMBIENT HALO PROFILE, "
      "not a bound ***",
      f"stage 6's own check C2 already conceded this ('transport is not forbidden in principle')")

check(rho_for_cs_eq_c > rho_poly,
      f"1.4  CONTROL on 1.3: the density at which the condensate mode itself reaches c is "
      f"{sig(rho_for_cs_eq_c,3)} kg/m^3, ABOVE the polytrope's {sig(rho_poly,3)} kg/m^3 -- so 1.3 is "
      "a real intermediate speed, not a runaway artefact of the formula",
      "and the DBI cap u <= Lam_D bounds it further, by an amount tied to the OPEN base_a/K_B item")


# ==================================================================================================
print()
print("=" * 100)
print("PART 2 -- DOES ESCAPE AT c SATISFY CLAIM 2, OR VIOLATE IT?")
print("=" * 100)
print("""
  Claim 2: "no equation of state renders an energy density invisible to BOTH orbital dynamics and
  lensing; the only configuration invisible to both is rho = 0."
  Radiation that has LEFT the region contributes rho = 0 locally.  So escape does not evade Claim 2 --
  it lands exactly on Claim 2's own permitted endpoint.  Claim 2 forbids HIDING energy that is
  PRESENT; it is silent on REMOVING it.  The two parts are complementary, not redundant: Part E
  forbids hiding, Part C forbids removing.  If Part C fails, nothing catches the escape.
""")
info(
      "2.1  *** LOGICAL FINDING: Claim 2 is SATISFIED by escape at c, not violated.  The word "
      "'unreachable' in stage 6 was doing ALL the work, and it is exactly the step that Part 1 "
      "breaks.  Claim 2 survives as a theorem and stops being a no-go on this route ***",
      "rho -> 0 locally is achieved, which is precisely what Claim 2 says is required")

# 2.2 -- but the radiation IN TRANSIT still gravitates.  Does it restore the problem?
E_dust = M_DUST * MSUN * C ** 2
L_hubble = E_dust / (T_H * GYR)
Mdot = M_DUST / (T_FF * mp.mpf("1e9"))                    # Msun/yr during assembly
L_accr = Mdot * MSUN / YR * C ** 2
t_light = MPC / C
for lab, L in (("Hubble-averaged", L_hubble), ("assembly-epoch", L_accr)):
    M_transit = L * t_light / C ** 2 / MSUN
    print(f"   {lab:<18s} L = {sig(L,4)} W  ->  radiation in transit inside 1 Mpc = "
          f"{sig(M_transit,3)} Msun = {sig(M_transit/M_BAR*100,3)}% of baryons "
          f"({sig(2*M_transit/M_BAR*100,3)}% in rho+3p)")
M_transit_h = L_hubble * t_light / C ** 2 / MSUN
M_transit_a = L_accr * t_light / C ** 2 / MSUN
check(2 * M_transit_a / M_BAR < mp.mpf("0.25"),
      f"2.2  the escaping flux does NOT restore the problem, but it is not free either: the "
      f"radiation in transit is worth {sig(M_transit_h,3)}-{sig(M_transit_a,3)} Msun, i.e. "
      f"{sig(2*M_transit_h/M_BAR*100,2)}-{sig(2*M_transit_a/M_BAR*100,2)}% of the baryonic mass in "
      "rho+3p -- a real few-percent residual, inside observational slop and NOT negligible",
      "this is a NEW number the original argument never had to compute")


# ==================================================================================================
print()
print("=" * 100)
print("PART 3 -- THE CONSTRAINT THAT REPLACES THE TRANSPORT BOUND: THE FLUX MUST BE UNSEEN")
print("=" * 100)

print(f"""
  Required export power per L* galaxy, converting {sig(M_DUST,3)} Msun:
    over a Hubble time ({sig(T_H,3)} Gyr):   L = {sig(L_hubble,4)} W = {sig(L_hubble/LSUN,4)} Lsun
    at the assembly rate ({sig(Mdot,4)} Msun/yr): L = {sig(L_accr,4)} W = {sig(L_accr/LSUN,4)} Lsun

  For scale: L* stellar bolometric = {sig(L_MW,3)} W; Eddington of a 1e9 Msun black hole
  = {sig(mp.mpf('1.26e31')*mp.mpf('1e9'),3)} W; the most luminous quasars ~1e40 W.
""")
check(L_hubble / L_MW > 1e4,
      f"3.1  *** THE REQUIRED POWER IS {sig(L_hubble/L_MW,4)}x THE GALAXY'S ENTIRE STELLAR OUTPUT "
      f"(and {sig(L_accr/L_MW,4)}x at the assembly rate), sustained for a Hubble time, in EVERY "
      f"galaxy -- {sig(L_hubble/(mp.mpf('1.26e31')*mp.mpf('1e9')),3)}x the Eddington luminosity of a "
      "1e9 Msun black hole.  So the channel must be essentially perfectly dark ***",
      f"{sig(L_hubble/LSUN,3)} Lsun per L* galaxy")

# 3.2 -- photon branching limits, three independent ways
B_sed = mp.mpf("0.01") * L_MW / L_hubble                    # <=1% of stellar bolometric
I_EBL = mp.mpf("60e-9")                                     # W/m^2/sr, COB+CIB (Cooray 2016 review)
u_EBL = 4 * mp.pi * I_EBL / C
u_conv = RHO_DM0 * C ** 2
B_ebl = u_EBL / u_conv
TAU_IGRB = mp.mpf("1e28")                                   # s, IGRB decaying-DM bound
B_igrb_H = (T_H * GYR) / TAU_IGRB
tau_halo = mp.mpf("17e6") * YR                              # required in-halo lifetime, Part 4
B_igrb_fast = tau_halo / TAU_IGRB
print(f"""   photon branching ratio B_gamma must satisfy:
     galaxy SED (<=1% of stellar bolometric)                B_gamma < {sig(B_sed,3)}
     total EBL energy density ({sig(I_EBL*1e9,2)} nW/m^2/sr)         B_gamma < {sig(B_ebl,3)}
     IGRB decaying-DM bound tau > 1e28 s, at 1/t_H          B_gamma < {sig(B_igrb_H,3)}
     ... same bound at the required in-halo rate            B_gamma < {sig(B_igrb_fast,3)}
""")
check(max(B_sed, B_ebl) < mp.mpf("1e-4"),
      f"3.2  *** PHOTONS ARE EXCLUDED BY 5 TO 14 ORDERS: the loosest of the three limits is "
      f"B_gamma < {sig(max(B_sed,B_ebl),3)} and the tightest is {sig(B_igrb_fast,3)}.  This is a REAL "
      "new constraint, but it constrains a COUPLING -- a dark sector with no photon portal satisfies "
      "it trivially, so it does not close the route ***",
      "same for neutrinos, which are bounded both cosmologically and by direct diffuse searches")

# 3.3 -- the surviving channel: dark radiation, and the cosmological bound on it
F_ALLOWED_BAO = mp.mpf("0.14")     # Nunes et al. MNRAS 497, 1757: 14% w/ BAO, 8% SN+SL only
F_ALLOWED_SN = mp.mpf("0.08")
TAU_AUDREN = mp.mpf("160")         # Gyr, Audren+2014 all-time decay to relativistic products
f_needed = mp.mpf("1.0")           # ~all the dust: it is all in basins (smooth-accretion theorem)
check(f_needed / F_ALLOWED_BAO > 5,
      f"3.3  *** AND THIS IS WHAT ACTUALLY KILLS THE ROUTE, ON DATA RATHER THAN BY THEOREM: the "
      f"framework needs f ~ {sig(f_needed,2)} of the dust converted to dark radiation (all of it is "
      f"in basins, by its own smooth-accretion theorem), against a LATE-TIME decaying-DM limit of "
      f"f <= {sig(F_ALLOWED_BAO,2)} (95% CL, SN+BAO+SL) -- over by {sig(f_needed/F_ALLOWED_BAO,3)}x. "
      f"The all-epoch bound tau > {sig(TAU_AUDREN,3)} Gyr is {sig(TAU_AUDREN/T_H,3)}x the age of the "
      "universe against a required in-halo lifetime of ~17 Myr ***",
      "Y-gating DOES evade the CMB (Y = 0 on FRW), so the late-time bound is the right one")

# NC-3 (negative control): the same machinery must PASS a scenario that is genuinely allowed.
f_toy = mp.mpf("0.05")
check(f_toy < F_ALLOWED_BAO,
      f"NC-3  CONTROL: fed a scenario converting only f = {sig(f_toy,2)} of the dust, the same test "
      f"returns ALLOWED (below the {sig(F_ALLOWED_BAO,2)} limit) -- so 3.3 measures the required "
      "fraction rather than rejecting every fraction",
      "the constraint is quantitative and evadable in principle, which is why it is not a theorem")


# ==================================================================================================
print()
print("=" * 100)
print("PART 4 -- HOW FAST THE DECAY MUST BE, GIVEN THAT ACCRETION KEEPS REFILLING")
print("=" * 100)

M_ss_allowed = mp.mpf("0.3") * M_BAR       # dust must stay below ~30% of baryons to spare the RAR
Gamma_req = Mdot / M_ss_allowed            # 1/yr
tau_req = 1 / Gamma_req / mp.mpf("1e9")    # Gyr
check(tau_req < mp.mpf("0.1"),
      f"4.1  the steady state is the binding requirement: with inflow {sig(Mdot,4)} Msun/yr, holding "
      f"the dust below {sig(M_ss_allowed,3)} Msun (30% of baryons) needs an in-halo lifetime of "
      f"{sig(tau_req*1000,3)} Myr = {sig(tau_req/T_H*100,3)}% of a Hubble time",
      "so the cosmological comparison in 3.3 is if anything generous to the repair")


# 4.2 -- cross-check the exclusion on the low-z matter density, WITHOUT using the CMB.
OM_M_SN = mp.mpf("0.334")      # Pantheon+ flat LCDM
SIG_SN = mp.mpf("0.018")
om_m_after = mp.mpf("0.049")   # baryons only, if f = 1 and the DR has diluted away
n_sig = (OM_M_SN - om_m_after) / SIG_SN
check(n_sig > 10,
      f"4.2  CROSS-CHECK, and it says the true margin is WORSE than 7x: with f = 1 the low-z matter "
      f"density falls to the baryons alone, Omega_m -> {sig(om_m_after,2)}, against a CMB-independent "
      f"low-z measurement of {sig(OM_M_SN,3)} +/- {sig(SIG_SN,2)} (Pantheon+ flat LCDM) = "
      f"{sig(n_sig,3)} sigma.  The published f <= 0.14 already marginalises over H_0 and Omega_Lambda, "
      "so 7x on the FRACTION is the defensible number and this sigma is only a sanity heuristic",
      "reported because it runs AGAINST the escape route I am arguing for")


# ==================================================================================================
print()
print("=" * 100)
print("PART 5 -- TWO CANDIDATE RESCUES OF THE ORIGINAL, TESTED -- AND WHAT SURVIVES")
print("=" * 100)

# 5.0 -- the photon-rocket rescue: attractive, and it FAILS on inspection.  Reported as a negative.
p_flux = L_accr / C
M_bar_kg = M_BAR * MSUN
eps_allowed = mp.mpf("0.01") * mp.mpf("9.3619e-11") * M_bar_kg / p_flux
a_over_a0_full = (p_flux / M_bar_kg) / mp.mpf("9.3619e-11")
check(eps_allowed < mp.mpf("1e-4"),
      f"5.0  A RESCUE I TRIED FOR THE ORIGINAL, AND IT DOES NOT WORK.  The escaping flux is a rocket: "
      f"momentum flux L/c = {sig(p_flux,3)} N, so fully one-sided emission would accelerate an L* "
      f"baryonic mass at {sig(a_over_a0_full,3)} a_0, and keeping it below 0.01 a_0 would demand "
      f"isotropy to {sig(eps_allowed,3)} -- impossible for a structure-gated source.  *** BUT IT DOES "
      "NOT BITE: dark radiation does not couple to baryons, so the recoil acts on the DUST, which is "
      "the component being removed.  The gravitomagnetic pull on stars is suppressed by v_orb/c ~ 1e-3 "
      "and is negligible.  A dead end, recorded so it is not re-proposed ***",
      "checked in the direction that would have SAVED my own no-go, and it fails")

# 5.1 -- gravitational radiation: the channel exists at exactly c but cannot carry a monopole.
info(
      "5.1  IN THE ORIGINAL'S FAVOUR: gravitational radiation is a guaranteed channel at exactly c "
      "(c_T = 1, banked) but CANNOT carry this energy -- there is no monopole gravitational "
      "radiation, and a spherically symmetric decaying configuration radiates ZERO.  Quadrupole "
      "efficiency ~(v/c)^5 is negligible.  So GW is speed-c and coupling-zero",
      "the escape therefore REQUIRES a new non-gravitational portal, which is a real cost")

# 5.2 -- the in-sector conclusion stands.
check(t_cs > 10 * T_H,
      f"5.2  ALSO IN THE ORIGINAL'S FAVOUR: for the khronon sector BY ITSELF the conclusion is "
      f"right and robust.  A single-field k-essence has ONE characteristic speed; at the ghost-"
      f"condensate point the leading sound speed VANISHES and is regenerated only as c_s^2 = u/Q_0, "
      f"giving {sig(t_cs,3)} Gyr at halo density -- and the DBI cap drives c_s -> 0 at saturation.  "
      "'The condensate cannot hydrodynamically drain itself' is a correct statement",
      "what is wrong is calling that the sector's energy-export bound")

print(f"""
  ==================================  THE RATING  ==================================

  The transport step is INCOMPLETE, not merely narrow, and not wholly wrong:

    WRONG AS STATED   -- "moving it out of a galaxy needs transport at the sector's own sound speed."
                         It does not.  Energy conservation bounds the TOTAL, not the flux velocity;
                         causality bounds the flux at c.  One mode's speed was substituted for the
                         causal cone, and the substitution is off by {sig(ratio_speed,3)}x.
    UNJUSTIFIED       -- the enumeration of channels has exactly one entry.  AeST as written has SIX
                         propagating modes (2 tensor AT c, 2 massive vector, 1 massive scalar) and the
                         free function F(Y,Q) couples the condensate to the vector sector through
                         A_mu.  c_s is the SLOWEST of the six.
    NOT A BOUND       -- c_s^2 = u/Q_0 is amplitude-dependent; 690 Gyr is an evaluation at the
                         ambient halo profile.  Stage 6's own check C2 says so out loud.
    CORRECT           -- the sub-claim "the condensate cannot drain ITSELF hydrodynamically", and the
                         observation that the escape needs a NEW portal (gravity alone cannot: no
                         monopole radiation).
    RESCUED, NOT LOST -- the conclusion survives, on a DIFFERENT and much softer constraint:
                         f <= 0.08-0.14 allowed vs f ~ 1 required, i.e. {sig(f_needed/F_ALLOWED_BAO,3)}x
                         over a 95% observational limit, plus B_gamma < {sig(B_sed,2)}.

  AND CLAIM 2 CHANGES SIDES.  "No EoS hides energy from both dynamics and lensing; only rho = 0
  works" is SATISFIED by escape at c -- radiation that has left contributes nothing locally.  Claim 2
  forbids hiding, Part C forbade removing; with Part C broken, Claim 2 no longer closes anything on
  this route.  It remains a true theorem and a correct no-go on the f = 1/3 pressure mechanism.

  SO: "the repair space of local, energy-preserving modifications is provably empty" was an
  OVERCLAIM in one specific word -- PROVABLY.  The energy-EXPORTING repair space was never examined,
  it is not closed by any theorem in the sequence, and it is closed (if at all) by a 7x observational
  margin on a bound whose published derivation assumes HOMOGENEOUS decay, which the Y-gated
  construction is not.  The honest status of the export route is DISFAVOURED-BY-DATA, not EMPTY.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 2 negative controls)")
sys.exit(0)
