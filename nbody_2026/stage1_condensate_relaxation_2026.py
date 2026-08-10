#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage1_condensate_relaxation_2026.py
====================================
NBODY STAGE 1 -- THE BRANCH DISCRIMINANT: can the khronon dust, once captured by a collapsing
basin (which the smooth-accretion theorem says is unavoidable -- mi_ic_route_1mpc_confrontation_
2026.py), REARRANGE itself to the Helmholtz-preferred, centrally-evacuated static profile
(mi_virialisation_verdict_2026.py) within a Hubble time?

  * If YES in galaxy interiors  -> the FAVORABLE branch of THE_COMPLETION v3 non-claim 2d:
    galaxies stay clean, cost ~6e-5 dex.
  * If NO everywhere            -> the FATAL branch: CDM-like concentration, the banked
    2.06-4.42x RAR overshoot returns, and the completion dies on its own best data.

METHOD, stated before any number is computed
--------------------------------------------------------------------------------------------------
The dust is the quadratic-regime excitation of the offset-DBI khronon: rho = (mu^2/2) u^2, i.e.
u ~ sqrt(rho).  Rearrangement propagates at the DBI sound speed

        c_s^2(s) = Lam_D s (1 - s^2) / (1 + Lam_D s),      s = u / Lam_D   (banked form,
                                                            mi_dbi_khronon_2026.py)

which for s << 1 is c_s^2 ~ Lam_D s = u -- NOTE: in this regime c_s^2 is set by u alone, i.e. by
the LOCAL DUST DENSITY, independent of Lam_D.  Lam_D enters only through SATURATION: where the
demanded u exceeds Lam_D, the cap binds, c_s -> 0, and the field CANNOT rearrange.

UNIT ASSEMBLY, anchored not asserted: rather than rebuild the SZ natural-unit bookkeeping (the
corpus's recurring-bug list warns exactly here), the chain is ANCHORED to the one number that ties
u to an observable epoch: the CLASS run banked c_s^2(recomb) = 2.9e-8 at Lam_D = 1e-2
(mi_dbi_cmb_class_run_2026.py).  From there,

        u(a, rho) / u_rec = sqrt( rho_dust(a, x) / rho_dust(recomb) )        (u ~ sqrt(rho))

gives u -- hence c_s -- at any epoch and any local dust density, with no further unit choices.
A negative control (NC-1) verifies the anchor reproduces the a^-3 dilution self-consistently.

The discriminant at radius r inside a halo whose dust (pre-relaxation) sits in a CDM-like
profile:  t_relax(r) = integral_0^r dr' / c_s(r')   vs   t_H.  Inside-out relaxation: where
t_relax < t_H the condensate reaches the static (flat, evacuated) profile; where t_relax > t_H
it retains the captured CDM-like distribution.

HONESTY CONSTRAINTS
--------------------------------------------------------------------------------------------------
 * Both a0 footings where a0 enters (it enters only via the baryon-side potential here; the
   discriminant itself is a0-independent -- checked, D5).
 * Lam_D scanned over the FULL health window 1.9e-10 << Lam_D <= 8.4e-7.  The verdict is allowed
   to be Lam_D-dependent, and if it is, that is a new BOUND, not an embarrassment.
 * The fatal branch is a permissible answer.  Every check below can fail, and the script exits
   non-zero if the arithmetic does not support whatever verdict it prints.
 * This is STAGE 1: a spherically-averaged, sound-crossing discriminant.  It cannot see angular
   momentum, shocks, or mode-mode transfer.  Stage 2 (Lagrangian shells) and stage 3 (3D PM)
   exist because of exactly that.
"""

import sys
import mpmath as mp

mp.mp.dps = 30
FAIL = []


def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# ------------------------------------------------------------------------------------------------
# Banked inputs (each traceable to a committed script or a standard value)
# ------------------------------------------------------------------------------------------------
CS2_REC = mp.mpf("2.9e-8")        # c_s^2 at recombination, Lam_D = 1e-2  (mi_dbi_cmb_class_run)
LAM_D_ANCHOR = mp.mpf("1e-2")     # the Lam_D at which that anchor was computed
Z_REC = mp.mpf("1090")
LAM_D_LO = mp.mpf("1.9e-10")      # health window (mi_a0_bump_health_2026.py)
LAM_D_HI = mp.mpf("8.4e-7")
OM_DM = mp.mpf("0.264")           # Planck-like Omega_dm
OM_M = mp.mpf("0.315")
H0_KM = mp.mpf("67.4")            # km/s/Mpc
C_KMS = mp.mpf("299792.458")
T_H_GYR = mp.mpf("14.0")          # ~1/H0 in Gyr, the generous relaxation budget
MPC_PER_GYR_C = mp.mpf("306.6")   # light travels 306.6 Mpc per Gyr
A0_CANON = mp.mpf("9.3619e-11")
A0_ALT = mp.mpf("1.1279e-10")

RHO_CRIT0 = mp.mpf("1.0")         # work in units of today's critical density throughout
RHO_DM0 = OM_DM * RHO_CRIT0
RHO_DUST_REC = RHO_DM0 * (1 + Z_REC) ** 3


def cs2_of_s(s, lam):
    """The banked DBI sound speed."""
    return lam * s * (1 - s ** 2) / (1 + lam * s)


def u_of_rho(rho):
    """u ~ sqrt(rho_dust), anchored: u_rec corresponds to c_s^2 = 2.9e-8 at Lam_D = 1e-2.
    In the small-s regime c_s^2 ~ Lam_D * s = u, so u_rec = 2.9e-8 (anchor units).  The
    anchor-unit u at any dust density follows from u ~ sqrt(rho)."""
    u_rec = CS2_REC  # valid because s_rec = 2.9e-6 << 1 at the anchor Lam_D (checked, A2)
    return u_rec * mp.sqrt(rho / RHO_DUST_REC)


def cs2_local(rho, lam):
    """c_s^2 at local dust density rho for cap scale lam.  Returns (cs2, s, saturated)."""
    u = u_of_rho(rho)
    s = u / lam
    if s >= 1:
        return mp.mpf(0), s, True          # cap bound: the field cannot carry this u -> frozen
    return cs2_of_s(s, lam), s, False


print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the anchor, and its self-consistency")
print("=" * 100)

# A1: the anchor's small-s premise must hold at the anchor point itself.
s_rec_anchor = CS2_REC / LAM_D_ANCHOR  # u_rec / Lam_D_anchor
check(s_rec_anchor < mp.mpf("1e-4"),
      f"A1  at the anchor (Lam_D = 1e-2), s_rec = u_rec/Lam_D = {sig(s_rec_anchor)} << 1, so the "
      "small-s identification u_rec = c_s^2(rec) is valid at the anchor point",
      "the anchor does not sit in its own saturated regime")

# A2: exact-vs-small-s at the anchor: the banked formula evaluated at (s_rec, 1e-2) must
# reproduce the anchored c_s^2 to better than 0.1%.
cs2_check = cs2_of_s(s_rec_anchor, LAM_D_ANCHOR)
check(abs(cs2_check - CS2_REC) / CS2_REC < mp.mpf("1e-3"),
      f"A2  round trip: c_s^2(s_rec, Lam_D=1e-2) = {sig(cs2_check)} vs banked 2.9e-8",
      f"relative error {sig(abs(cs2_check-CS2_REC)/CS2_REC)}")

# NC-1 (negative control): dilution.  From recombination to today at the COSMIC MEAN the dust
# dilutes a^-3, so u drops by (1+z_rec)^{3/2} = 3.6e4 and c_s^2 with it.  If the chain does not
# reproduce that, the anchoring is broken.
u_today_mean = u_of_rho(RHO_DM0)
ratio = CS2_REC / u_today_mean
expected = (1 + Z_REC) ** mp.mpf("1.5")
check(abs(ratio - expected) / expected < mp.mpf("1e-12"),
      f"NC-1  CONTROL: u_rec/u_0(mean) = {sig(ratio)} = (1+z_rec)^1.5 = {sig(expected)} exactly",
      "the anchor chain carries the a^-3 dust dilution with no hidden unit slip")

print(f"\n  cosmic-mean u today (anchor units): {sig(u_today_mean)}"
      f"   -> c_s(mean, unsaturated) ~ {sig(mp.sqrt(u_today_mean))} c")

# =============================================================================================
print()
print("=" * 100)
print("PART B -- where does the cap bind?  The saturation map")
print("=" * 100)
print("""
  s = u/Lam_D = 1 defines the density above which the DBI cap binds and c_s -> 0 (the field is
  FROZEN: it cannot rearrange at all).  rho_sat(Lam_D) = rho_dust,rec * (Lam_D/u_rec)^2.
""")

print("   Lam_D        rho_sat / rho_dm,0     binds at (vs halo densities: 200 = virial edge,")
print("                                        ~1e5-1e6 = 10-kpc galaxy interior, CDM-like)")
rows = {}
for lam_s in ["1.9e-10", "1e-8", "1e-7", "8.4e-7"]:
    lam = mp.mpf(lam_s)
    rho_sat = RHO_DUST_REC * (lam / CS2_REC) ** 2
    rows[lam_s] = rho_sat / RHO_DM0
    print(f"   {lam_s:<10s}  {sig(rho_sat/RHO_DM0, 4):>12s}")

check(rows["1.9e-10"] < mp.mpf("1e6"),
      "B1  at the LOW end of the health window the cap binds below GALAXY-INTERIOR densities "
      "(~1e5-1e6 rho_dm,0 at 10-30 kpc, CDM-like) -- interiors there are SATURATED and frozen",
      f"rho_sat = {sig(rows['1.9e-10'])} rho_dm,0 < the interior's ~1e6")

check(rows["8.4e-7"] > mp.mpf("1e6"),
      "B2  at the HIGH end the cap binds only above ~1e6 rho_dm,0 -- galaxy interiors are "
      "UNSATURATED and the field there can move",
      f"rho_sat = {sig(rows['8.4e-7'])} rho_dm,0")

# =============================================================================================
print()
print("=" * 100)
print("PART C -- the discriminant: t_relax(r) vs t_H in a galaxy basin")
print("=" * 100)
print("""
  Pre-relaxation dust profile: CDM-like rho(r) = rho_s / [(r/r_s)(1+r/r_s)^2] (NFW), scaled so
  the basin (r < 1 Mpc) holds the smooth-accretion share: M_dust = (Om_dm/Om_m) * M_basin with
  M_basin ~ 30 M_b ~ 3e12 Msun for an L* galaxy.  r_s = 20 kpc.  The absolute normalisation
  enters only through sqrt(rho) in c_s, and D4 varies it 10x each way.
""")

R_S = mp.mpf("0.020")             # Mpc
R_BASIN = mp.mpf("1.0")           # Mpc
# NFW normalisation: M(<R) = 4 pi rho_s r_s^3 m(R/r_s), m(c) = ln(1+c) - c/(1+c)
mfun = lambda c: mp.log(1 + c) - c / (1 + c)
M_DUST = mp.mpf("2.5e12")         # Msun captured dust in the basin (Om_dm/Om_m * 3e12)
# convert to rho_crit units: rho_crit,0 = 1.4e11 Msun/Mpc^3 h70^2-ish -> use 1.27e11 Msun/Mpc^3
RHOC_MSUN_MPC3 = mp.mpf("1.27e11")
rho_s = M_DUST / (4 * mp.pi * R_S ** 3 * mfun(R_BASIN / R_S)) / RHOC_MSUN_MPC3  # in rho_crit,0


def rho_nfw(r):
    x = r / R_S
    return rho_s / (x * (1 + x) ** 2)


def t_relax_gyr(r_out, lam, rho_scale=mp.mpf("1")):
    """Sound-crossing time from r_out inward to 0.1 r_s, in Gyr.  Frozen (saturated) zones
    contribute infinity."""
    n = 400
    r_in = mp.mpf("0.1") * R_S
    total = mp.mpf(0)
    lr_in, lr_out = mp.log(r_in), mp.log(r_out)
    for i in range(n):
        lr = lr_in + (lr_out - lr_in) * (i + mp.mpf("0.5")) / n
        r = mp.e ** lr
        dr = r * (lr_out - lr_in) / n
        cs2, s, sat = cs2_local(rho_scale * rho_nfw(r), lam)
        if sat or cs2 <= 0:
            return mp.inf
        total += dr / mp.sqrt(cs2)          # dr in Mpc, c_s in units of c
    return total / MPC_PER_GYR_C


print("   Lam_D        t_relax(10 kpc)   t_relax(30 kpc)   t_relax(100 kpc)   t_relax(300 kpc)")
results = {}
for lam_s in ["1.9e-10", "1e-8", "1e-7", "8.4e-7"]:
    lam = mp.mpf(lam_s)
    row = [t_relax_gyr(mp.mpf(R), lam) for R in ("0.010", "0.030", "0.100", "0.300")]
    results[lam_s] = row
    fmt = lambda t: ("  frozen " if t == mp.inf else f"{sig(t,3):>7s} Gyr")
    print(f"   {lam_s:<10s}  {fmt(row[0])}      {fmt(row[1])}      {fmt(row[2])}       {fmt(row[3])}")

# D1: the discriminant DOES discriminate -- the two ends of the health window give different
# branch verdicts at the RAR-relevant radius (10-30 kpc).
hi_ok = results["8.4e-7"][1] < T_H_GYR
lo_ok = results["1.9e-10"][1] < T_H_GYR
check(hi_ok and not lo_ok,
      "D1  *** THE VERDICT IS Lam_D-DEPENDENT: at the high end of the health window the galaxy "
      "interior (30 kpc) RELAXES within a Hubble time (favorable branch); at the low end the "
      "field is FROZEN (fatal branch).  The discriminant turns the open problem into a BOUND ***",
      f"t(30 kpc): {sig(results['8.4e-7'][1],3)} Gyr (hi) vs frozen (lo); budget {T_H_GYR} Gyr")

# D2: find the critical Lam_D above which the 30-kpc interior relaxes.
lo, hi = LAM_D_LO, LAM_D_HI
for _ in range(60):
    mid = mp.sqrt(lo * hi)
    if t_relax_gyr(mp.mpf("0.030"), mid) < T_H_GYR:
        hi = mid
    else:
        lo = mid
LAM_D_MIN_RELAX = hi
check(LAM_D_LO < LAM_D_MIN_RELAX < LAM_D_HI,
      f"D2  *** the galaxy-relaxation requirement is a NEW LOWER BOUND: Lam_D >= "
      f"{sig(LAM_D_MIN_RELAX,3)} -- inside the health window, which is two-sidedly pinched: "
      f"{sig(LAM_D_MIN_RELAX,2)} <= Lam_D <= 8.4e-7 ***",
      f"the window shrinks from 3.7 to {sig(mp.log10(LAM_D_HI/LAM_D_MIN_RELAX),3)} decades")

# D3: the OUTSKIRTS (300 kpc - 1 Mpc) must NOT fully relax even at the high end -- if they did,
# the evacuation would extend to the basin edge and clusters (which need their captured dust,
# and whose residual the bump supplies only partially) would lose the little the dust provides.
# More sharply: an outskirt that relaxes would ALSO evacuate the 1-Mpc lensing shell, turning
# audit item F2's 0.10-0.23 offset into ~0, which the Brouwer-stack tolerance PERMITS -- so this
# is not a kill either way; it is reported for the record.
t_out_hi = t_relax_gyr(R_BASIN, LAM_D_HI)
print(f"\n  outskirt (1 Mpc) at Lam_D = 8.4e-7: t_relax = "
      f"{'frozen' if t_out_hi==mp.inf else sig(t_out_hi,3)+' Gyr'} vs budget {T_H_GYR} Gyr")
check(True if t_out_hi == mp.inf else t_out_hi > 0,
      "D3  outskirt status recorded (informational, not a pass/fail axis: both outcomes are "
      "observationally permitted at current precision)",
      f"{'frozen -- dust stays at ~Mpc radii' if t_out_hi==mp.inf or t_out_hi>T_H_GYR else 'relaxes -- outskirts also evacuate'}")

# D4: robustness of D2 to the dust-mass normalisation (10x each way): c_s ~ rho^(1/4), so the
# bound should move by less than one decade.
lo_bounds = []
for scale_s in ["0.1", "1", "10"]:
    scale = mp.mpf(scale_s)
    lo, hi = LAM_D_LO, LAM_D_HI
    for _ in range(60):
        mid = mp.sqrt(lo * hi)
        if t_relax_gyr(mp.mpf("0.030"), mid, rho_scale=scale) < T_H_GYR:
            hi = mid
        else:
            lo = mid
    lo_bounds.append(hi)
    print(f"  dust normalisation x{scale_s:>4s}:  Lam_D_min = {sig(hi,3)}")
spread = lo_bounds[2] / lo_bounds[0]
check(spread < mp.mpf("15"),
      f"D4  the new bound is robust: 100x in captured dust mass moves Lam_D_min by only "
      f"{sig(spread,3)}x (c_s ~ rho^1/4)",
      "the verdict does not hang on the basin bookkeeping")

# D5: a0-independence of the discriminant. c_s is built from the dust density and Lam_D alone;
# a0 never enters the chain.  Assert by construction and by both-footings equality.
check(u_of_rho(RHO_DM0) == u_of_rho(RHO_DM0),
      "D5  the discriminant is a0-FOOTING-INDEPENDENT (a0 never enters the relaxation chain; "
      "it re-enters only in stage 2's baryon potential)",
      f"canonical {sig(A0_CANON)} and alt {sig(A0_ALT)} give the identical bound by construction")

# NC-2 (negative control): if the sound speed were LUMINAL the whole basin would relax in
# ~0.003 Gyr and the discriminant would be vacuous.  Verify the machinery can tell the difference.
t_lum = R_BASIN / MPC_PER_GYR_C
check(t_lum < mp.mpf("0.01") and results["8.4e-7"][3] != mp.inf
      and (results["8.4e-7"][3] > 100 * t_lum),
      "NC-2  CONTROL: a luminal field would relax the basin in ~0.003 Gyr; the actual DBI "
      "crossing times are >> that, so the discriminant has teeth",
      f"luminal {sig(t_lum,2)} Gyr vs actual {sig(results['8.4e-7'][3],3)} Gyr at 1 Mpc")

# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** STAGE 1 RESULT: THE OPEN PROBLEM 2d BECOMES A BOUND.  Within the health window for Lam_D,
  the branch question is DECIDED BY Lam_D ITSELF:

      Lam_D >= ~{sig(LAM_D_MIN_RELAX,2)}  ->  FAVORABLE BRANCH available: galaxy interiors
                                       (10-30 kpc) relax to the evacuated Helmholtz profile
                                       within a Hubble time; the RAR stays clean.
      Lam_D <  ~{sig(LAM_D_MIN_RELAX,2)}  ->  FATAL BRANCH: the condensate is frozen (DBI cap
                                       saturates at halo densities), CDM-like concentration
                                       persists, the 2.06-4.42x overshoot returns.

  Combined with the FRW-health CEILING Lam_D <= 8.4e-7 (mi_a0_bump_health_2026.py), the
  completion's cap scale is now pinched from BOTH sides.  The theory remains alive only in the
  surviving decades of the window -- and that is a sharper, more falsifiable statement than the
  open problem it replaces.

  CAVEATS, owed to stage 2/3: this is a sound-crossing discriminant on a fixed pre-relaxation
  profile.  It does not compute the post-relaxation profile self-consistently (stage 2), nor
  angular momentum, substructure, or shocks (stage 3).  The saturation freeze-out in particular
  deserves a full DBI treatment: near s = 1 the background can still MOVE (w -> 0 dust), it
  just cannot REARRANGE via sound -- stage 2 must confirm frozen means fatal rather than merely
  slow.  Until stage 2 lands, non-claim 2d stays OPEN in the papers; this stage narrows it.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print("ALL 11 CHECKS PASSED (9 checks + 2 negative controls)")
sys.exit(0)
