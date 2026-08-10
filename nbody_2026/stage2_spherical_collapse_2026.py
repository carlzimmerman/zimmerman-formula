#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage2_spherical_collapse_2026.py
=================================
NBODY STAGE 2 -- THE ENERGETICS AND THE SHELLS.  Stage 1 asked "can the condensate REARRANGE
(sound-crossing) within a Hubble time?" and found a Lam_D-dependent yes.  Stage 2 asks the question
stage 1 could not: WHAT FORCE holds the rearranged configuration up?  Sound-crossing is NECESSARY,
not SUFFICIENT -- a fluid can be able to move and still have nowhere to stand.

THE THREE PHYSICAL FACTS THIS STAGE RESTS ON (each computed, none assumed)
--------------------------------------------------------------------------------------------------
 (1) THE DBI PRESSURE IS BOUNDED: p = K <= mu^2 Lam_D^2, and the sound speed maxes out at
     c_s^2 = 0.385 Lam_D (banked, mi_dbi_khronon_2026.py) at s = 0.577 -- then FALLS to zero at
     saturation.  Support of a self-gravitating mass M at radius r needs c_s^2 ~ GM/(r c^2).
 (2) THE HELMHOLTZ TERM IS EMPTY AT GALAXY SCALES: the static "rho_c tracks Phi" profile carries
     rho_c = mu^2 |Phi| c^2/(4 pi G).  At the completion's own mu^-1 = 4392 Mpc this is computed
     below to be ~1e-6 of the captured charge -- the evacuated profile CANNOT HOLD the basin's
     dust; it was the equilibrium of a different problem (charge free to leave).
 (3) THE DUST IS A POTENTIAL FLOW: a scalar's charge flux cannot multi-stream, so it cannot
     virialise the way collisionless CDM does (no shell-crossing support).  Cold fluid + bounded
     pressure + gravity = infall until either pressure catches up or the EFT exits validity.

METHOD: Lagrangian shells for the dust in an L* basin (total M(<1 Mpc) ~ 3e12 Msun, NFW-shaped,
captured dust share Om_dm/Om_m -- the smooth-accretion theorem's allocation), MOND-boosted
free-fall via the in-force Route A kernel nu(y) = 1/(1-e^-sqrt(y)) at BOTH a0 footings, and the
anchored c_s^2(rho) chain of stage 1 (anchor: CLASS c_s^2(rec) = 2.9e-8 at Lam_D = 1e-2;
u ~ sqrt(rho); NC-1 of stage 1 verified the dilution bookkeeping).

HONESTY CONSTRAINTS: the fatal branch is a permissible answer; stage 1's favorable branch is
permitted to DIE here (it does -- see Part A); every check can fail; exits non-zero if the
arithmetic does not support the printed verdict.  The fluid description is valid from basin scales
down to where caustics form; the endpoint sits outside the EFT (K''/mu^2 ~ 3e11 at s -> 1, banked)
and THAT regime -- wave dynamics at the caustic -- is stage 3's, not this stage's.
"""

import sys
import mpmath as mp

mp.mp.dps = 30
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# ---------------------------------------------------------------------------------------------
# Constants and banked inputs
# ---------------------------------------------------------------------------------------------
G_KMS = mp.mpf("4.300e-9")        # G in Mpc (km/s)^2 / Msun
C_KMS = mp.mpf("299792.458")
KMS2_TO_MPCGYR2 = mp.mpf("1.0459e-6")   # (km/s)^2 -> Mpc^2/Gyr^2
T_H = mp.mpf("14.0")              # Gyr
CS2_REC = mp.mpf("2.9e-8")        # anchor (mi_dbi_cmb_class_run_2026.py)
Z_REC = mp.mpf("1090")
LAM_HI = mp.mpf("8.4e-7")         # FRW-health ceiling (mi_a0_bump_health_2026.py)
LAM_LO = mp.mpf("1.9e-10")
CS2_MAX_COEF = mp.mpf("0.385")    # c_s^2 max = 0.385 Lam_D at s = 0.577 (mi_dbi_khronon_2026.py)
MU_INV_MPC = mp.mpf("4392")       # completion's Helmholtz scale (item 12)
OM_DM, OM_M, OM_B = mp.mpf("0.264"), mp.mpf("0.315"), mp.mpf("0.051")
RHO_CRIT = mp.mpf("1.27e11")      # Msun/Mpc^3
RHO_DM0 = OM_DM * RHO_CRIT
RHO_REC = RHO_DM0 * (1 + Z_REC) ** 3
A0 = {"canon": mp.mpf("9.3619e-11"), "alt": mp.mpf("1.1279e-10")}   # m/s^2

# The basin (stage 1's, unchanged): total NFW-shaped M(<1 Mpc) = 3e12, r_s = 20 kpc
R_S, R_BASIN = mp.mpf("0.020"), mp.mpf("1.0")
M_TOT = mp.mpf("3.0e12")
M_DUST = M_TOT * OM_DM / OM_M     # the smooth-accretion allocation, 2.51e12 Msun
mfun = lambda c: mp.log(1 + c) - c / (1 + c)
M_of = lambda r: M_TOT * mfun(r / R_S) / mfun(R_BASIN / R_S)
V_C = mp.mpf("200.0")             # km/s, the L* circular speed the RAR region measures


def u_of_rho(rho_msun_mpc3):
    """anchor-units u ~ sqrt(rho_dust), stage 1's chain (NC-verified there)."""
    return CS2_REC * mp.sqrt(rho_msun_mpc3 / RHO_REC)


def cs2(rho, lam):
    s = u_of_rho(rho) / lam
    if s >= 1:
        return mp.mpf(0)
    return lam * s * (1 - s ** 2) / (1 + lam * s)


print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the support theorem: what the DBI cap can hold vs what a galaxy demands")
print("=" * 100)

w_req_halo = (V_C / C_KMS) ** 2          # the virial parameter the RAR region sits at
cs2_ceiling = CS2_MAX_COEF * LAM_HI      # the BEST the theory can ever do, at the health ceiling
print(f"""
  Support of dust bound at circular speed v_c needs c_s^2 >~ (v_c/c)^2 = {sig(w_req_halo)}.
  The DBI sound speed's absolute maximum is 0.385*Lam_D; at the FRW-health ceiling
  Lam_D = 8.4e-7 that is {sig(cs2_ceiling)} -- BELOW the requirement.
""")
check(cs2_ceiling < w_req_halo,
      "A1  *** THE SUPPORT THEOREM: even the OPTIMAL DBI sound speed at the health ceiling is "
      f"below the halo virial parameter ({sig(cs2_ceiling)} < {sig(w_req_halo)}) -- no Lam_D in "
      "the health window can hold dust up anywhere in an L* halo ***",
      f"shortfall {sig(w_req_halo/cs2_ceiling,3)}x at the ceiling; worse everywhere below it")

lam_needed = w_req_halo / CS2_MAX_COEF
check(LAM_HI < lam_needed < 2 * LAM_HI,
      f"A2  *** THE NEAR-MISS, reported against interest in BOTH directions: support would need "
      f"Lam_D >= {sig(lam_needed,3)} -- only {sig(lam_needed/LAM_HI,3)}x ABOVE the FRW-health "
      "ceiling.  The theory misses self-supporting galactic dust by ~40%, not by orders ***",
      "a base_a shift of the FRW bound could reopen this; at the current bound it is closed")

# A3 -- and therefore stage 1's discriminant was the wrong axis:
check(cs2_ceiling < w_req_halo and LAM_HI < lam_needed,
      "A3  *** STAGE 1 CORRECTION: the sound-crossing 'favorable branch' and its lower bound "
      "Lam_D >= 1.2e-9 are WITHDRAWN.  Crossing ability is NECESSARY, not SUFFICIENT: the "
      "evacuated profile has no force to enforce it at galaxy scales.  The Lam_D pinch of stage 1 "
      "dissolves back to the FRW ceiling alone ***",
      "this stage supersedes stage 1's verdict block; 2d's status becomes fatal-by-default, Part E")

# =============================================================================================
print()
print("=" * 100)
print("PART B -- the static (Helmholtz) profile cannot hold the charge at mu^-1 = 4392 Mpc")
print("=" * 100)

# rho_c(static) = mu^2 |Phi| c^2 / (4 pi G).  In Msun/Mpc^3 with Phi ~ (v_c/c)^2:
mu2 = (1 / MU_INV_MPC) ** 2                       # Mpc^-2
phi = w_req_halo                                  # dimensionless potential depth of the basin
rho_c_static = mu2 * phi * C_KMS ** 2 / (4 * mp.pi * G_KMS)   # Msun/Mpc^3
cap_static = rho_c_static * (mp.mpf("4") / 3) * mp.pi * R_BASIN ** 3
check(cap_static / M_DUST < mp.mpf("1e-4"),
      f"B1  *** the static profile's total capacity in the basin is {sig(cap_static,3)} Msun = "
      f"{sig(cap_static/M_DUST,2)} of the captured charge ({sig(M_DUST,3)} Msun) -- the "
      "'evacuated Helmholtz profile' is the equilibrium of a DIFFERENT problem (charge free to "
      "leave); with the charge conserved and bound, it cannot be the end state ***",
      "computed at the completion's own mu^-1 = 4392 Mpc; the old Mpc-scale mu is do-not-cite")

# =============================================================================================
print()
print("=" * 100)
print("PART C -- Lagrangian shells: where does the captured dust actually go, and how fast")
print("=" * 100)

# C1: MOND-boosted free-fall times per shell, both footings.
MPC_PER_MS2 = mp.mpf("3.241e-23") * mp.mpf("1e6")  # not used; keep g in SI via v^2/r instead


def g_newt_si(r_mpc):
    """Newtonian g of the enclosed TOTAL mass, in m/s^2: g = G M / r^2."""
    G_SI, MSUN, MPC = mp.mpf("6.674e-11"), mp.mpf("1.989e30"), mp.mpf("3.086e22")
    return G_SI * M_of(r_mpc) * MSUN / (r_mpc * MPC) ** 2


def nu_routeA(y):
    return 1 / (1 - mp.e ** (-mp.sqrt(y)))


def tff_gyr(r_mpc, a0):
    """free-fall from rest at r with the MOND-boosted field: t = (pi/2) sqrt(r^3/(2 G_eff M))."""
    boost = nu_routeA(g_newt_si(r_mpc) / a0)
    GM = G_KMS * KMS2_TO_MPCGYR2 * M_of(r_mpc) * boost
    return (mp.pi / 2) * mp.sqrt(r_mpc ** 3 / (2 * GM))


print("\n   footing   t_ff(30 kpc)   t_ff(0.3 Mpc)   t_ff(1 Mpc)    settled radius by t_H")
settled = {}
for f, a0 in A0.items():
    lo, hi = mp.mpf("0.005"), R_BASIN
    if tff_gyr(R_BASIN, a0) < T_H:
        r_set = R_BASIN
    else:
        for _ in range(60):
            mid = mp.sqrt(lo * hi)
            if tff_gyr(mid, a0) < T_H:
                lo = mid
            else:
                hi = mid
        r_set = lo
    settled[f] = r_set
    print(f"   {f:7s}   {sig(tff_gyr(mp.mpf('0.030'),a0),3):>8s} Gyr   {sig(tff_gyr(mp.mpf('0.3'),a0),3):>8s} Gyr"
          f"   {sig(tff_gyr(R_BASIN,a0),3):>8s} Gyr    {sig(r_set,3)} Mpc")

check(all(settled[f] >= mp.mpf("0.9") * R_BASIN for f in settled),
      "C1  essentially the WHOLE basin's dust reaches the centre within a Hubble time on both "
      "footings (MOND-boosted free-fall; interior shells in ~1 Gyr)",
      f"settled radius {sig(settled['canon'],3)} / {sig(settled['alt'],3)} Mpc of the 1 Mpc basin")

# C2: can the infall be STOPPED anywhere?  Support needs c_s^2(rho(r)) >= G M_d/(r c^2) with
# rho(r) = 3 M_d/(4 pi r^3).  Scan inward at the health ceiling (the theory's best case).
lam = LAM_HI
r = mp.mpf("0.5")
caught = None
while r > mp.mpf("1e-6"):
    rho = 3 * M_DUST / (4 * mp.pi * r ** 3)
    w_req = G_KMS * M_DUST / (r * C_KMS ** 2)
    if cs2(rho, lam) >= w_req:
        caught = r
        break
    r *= mp.mpf("0.9")
check(caught is None,
      "C2  *** the collapse is NEVER caught: at every radius from 0.5 Mpc down to 1 pc the "
      "required support exceeds the DBI sound speed at the local density (which saturates and "
      "FALLS at high density) -- the dust runs to a central caustic in the s -> 1 / EFT-breakdown "
      "zone.  True at the health ceiling, a fortiori below it ***",
      "the two conditions (anchored c_s^2(rho), support) have no simultaneous solution")

# C3: where does the fluid description exit?  s = 1 crossing radius for the settled mass.
r = mp.mpf("0.5")
while u_of_rho(3 * M_DUST / (4 * mp.pi * r ** 3)) / lam < 1 and r > mp.mpf("1e-7"):
    r *= mp.mpf("0.95")
r_eft = r
check(r_eft < mp.mpf("0.001"),
      f"C3  the EFT exit (s = 1) for the settled mass sits at r ~ {sig(r_eft*1000,2)} kpc -- far "
      "inside the RAR region (5-30 kpc), so the fluid-regime conclusion about the RAR shell is "
      "reached while the description is still valid",
      "what happens AT the caustic is stage 3's wave problem; what happens to the 5-30 kpc shell is not")

# =============================================================================================
print()
print("=" * 100)
print("PART D -- the damage: the RAR overshoot from the collapsed dust, both footings")
print("=" * 100)

print("\n   r         g_dust/g_obs     overshoot in v (dex)    vs 0.034 dex scatter")
worst = {}
for r_kpc in ("5", "10", "30"):
    r = mp.mpf(r_kpc) / 1000
    g_ratio = G_KMS * M_DUST / (r * V_C ** 2)      # (G M_d / r^2) / (v_c^2 / r)
    dexv = mp.log(1 + g_ratio, 10) / 2
    worst[r_kpc] = dexv
    print(f"   {r_kpc:>3s} kpc   {sig(g_ratio,4):>8s}x        {sig(dexv,3):>6s} dex              "
          f"{sig(dexv/mp.mpf('0.034'),3)}x")

check(worst["10"] > mp.mpf("0.5"),
      f"D1  *** FATAL: the settled dust overshoots the 10-kpc rotation point by "
      f"{sig(worst['10'],3)} dex in velocity -- {sig(worst['10']/mp.mpf('0.034'),3)}x the RAR's "
      "intrinsic scatter.  This is WORSE than the banked 2.06-4.42x NFW-distributed overshoot, "
      "because a potential flow cannot virialise into an extended halo ***",
      "footing-independent: M_dust and v_c carry no a0")

# NC-1 (negative control, CDM-like): if the dust COULD virialise like collisionless CDM
# (shells freeze at half their turnaround radius, NFW-like extension), the overshoot at 10 kpc
# must come out at the banked few-x level -- the machinery must distinguish the two endpoints.
M_nfw_10 = M_DUST * mfun(mp.mpf("0.010") / R_S) / mfun(R_BASIN / R_S)
g_ratio_nfw = G_KMS * M_nfw_10 / (mp.mpf("0.010") * V_C ** 2)
check(mp.mpf("0.3") < g_ratio_nfw < mp.mpf("3"),
      "NC-1  CONTROL: distributing the same dust NFW-like (what collisionless CDM would do) gives "
      f"an O(1) overshoot at 10 kpc ({sig(g_ratio_nfw,3)}x in g -- the regime of the banked "
      "2.06-4.42x double-counting class), an order of magnitude MILDER than the caustic's -- the "
      "machinery distinguishes the two endpoints; the caustic verdict is not an artifact",
      "collisionless virialisation is exactly what a potential flow cannot do")

# NC-2 (negative control, support): with an artificial c_s^2 = 1e-6 (> (v_c/c)^2) the collapse
# MUST be caught -- proving C2's 'never caught' is a property of the DBI cap, not of the scanner.
r, caught2 = mp.mpf("0.5"), None
while r > mp.mpf("1e-6"):
    w_req = G_KMS * M_DUST / (r * C_KMS ** 2)
    if mp.mpf("1e-6") >= w_req:
        caught2 = r
        break
    r *= mp.mpf("0.9")
check(caught2 is not None and caught2 > mp.mpf("0.1"),
      f"NC-2  CONTROL: an artificial c_s^2 = 1e-6 catches the collapse at r = {sig(caught2,3)} "
      "Mpc -- the scanner can find support when support exists; the DBI cap is what forbids it",
      "")

# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** STAGE 2 RESULT, stated with both barrels:

  1. STAGE 1'S FAVORABLE BRANCH IS WITHDRAWN.  Sound-crossing was the wrong discriminant; the
     Lam_D >= 1.2e-9 lower bound and the '2.9-decade pinch' die here.  (Published record: v4's
     non-claim 2d postscript needs its 'now narrower' softened -- 2d was and is OPEN; the papers'
     fence held because 2d was never claimed solved.)

  2. WITHIN THE FLUID DESCRIPTION, THE FATAL BRANCH IS THE DEFAULT AT EVERY Lam_D IN THE HEALTH
     WINDOW: bounded DBI pressure cannot support galactic dust (A1: even the optimal sound speed
     at the ceiling falls short; C2: the collapse is never caught), the Helmholtz profile cannot
     hold the charge (B1: capacity ~1e-6 of the captured share at mu^-1 = 4392 Mpc), and the
     basin's dust free-falls to a sub-kpc caustic within a Hubble time (C1), overshooting the
     RAR region catastrophically (D1: ~{sig(worst['10'],2)} dex at 10 kpc).

  3. THE NEAR-MISS THAT NAMES THE STAKES: self-support needs Lam_D ~ {sig(lam_needed,2)} -- a
     factor {sig(lam_needed/LAM_HI,2)} above the FRW-health ceiling.  If base_a moves the FRW
     bound by ~40% the support door reopens (with dust held at ~0.4 Mpc, outskirt scales --
     possibly survivable).  A literature lookup now carries mortal weight.

  4. THE REMAINING DOORS, named: (i) STAGE 3 -- the wave/field dynamics at and around the
     caustic, outside the fluid description, where scalar interference can flatten cores (the
     genuine 'nobody has ever done it' calculation, now decisive rather than optional);
     (ii) base_a shifting the FRW ceiling past {sig(lam_needed,2)} (see 3);
     (iii) a theory-side change to the Q-sector so galactic-scale charge is suppressed -- noting
     honestly that the smooth-accretion theorem closes the obvious versions of this door.

  Non-claim 2d stays OPEN as published; its default branch is now FATAL-pending-stage-3, and
  this script is the committed evidence either way.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 2 negative controls)")
sys.exit(0)
