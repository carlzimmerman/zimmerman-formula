#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage23_s8_confrontation_2026.py
================================
DOES THE chi SECTOR'S PRESSURE CUTOFF ALLEVIATE THE S8 TENSION?  Computed, and the answer is NO --
by a factor ~35 in amplitude and ~7x in scale.  The idea is a dud, and the way it fails is informative.

THE IDEA (mine, flagged as a "sleeper" 2026-08-11): weak-lensing surveys measure S8 = sigma_8
sqrt(Omega_m/0.3) ~ 0.77 while CMB-calibrated LambdaCDM predicts ~0.83 -- less small-scale structure
than expected.  The gamma = 0 sector (stages 10-13) has p_chi = K ln(rho/rho_*), giving an exact
c_s^2 = K/rho and a Jeans length lam_J proportional to rho^-1, calibrated to lam_J(today) = 2.2 Mpc
comoving by stage 12's weak-lensing exclusion radius.  A real suppression of small-scale power, at a
scale nobody had checked against S8.  If it landed at the right scale and amplitude, a standing
LambdaCDM tension would become the framework's second cosmological success.

IT DOES NOT LAND THERE, and the scale arithmetic kills it before any amplitude question arises:
  * the cutoff sits at k_J = 2 pi / 2.2 Mpc = 4.24 h/Mpc;
  * S8 lives at k ~ 0.2-1 h/Mpc (the sigma_8 top-hat is R = 8 h^-1 Mpc, and its window is already
    down by ~10^-5 in power at k_J);
  * so the suppression is a factor ~5-20 in k ABOVE where S8 is measured, and the computed
    sigma_8 response is 0.23% at best against the 8.2% S8 relief needs -- short by 35x.
AND THE REDSHIFT DEPENDENCE MAKES IT WORSE, not better: lam_J proportional to rho^-1 means the
COMOVING cutoff scales as a^2, so 2.2 Mpc today is the LARGEST it has ever been -- at z = 0.5 (where
lensing S8 is measured) it is 0.98 Mpc, i.e. k_J = 9.5 h/Mpc.  The mechanism is weakest exactly
where the measurement is made.

Parts D-F then ask the two questions that make this worth committing rather than deleting:
  D  what lam_J WOULD be needed for S8 relief, and is that window open?  (It is not: the required
     value collides with the same weak-lensing RAR fit that calibrated lam_J in the first place.)
  E  does the framework push S8 the OTHER way?  At linear order, no -- stages 18/19 proved the FRW
     perturbation equations are LambdaCDM's, so S8 is INHERITED UNCHANGED, tension and all.  The
     MOND enhancement is a nonlinear effect and its sign is adverse (more structure, higher S8).
  F  and that makes S8 the LOW-REDSHIFT END OF THE SAME FRONT as stage 21's cosmic-dawn exposure:
     one problem, two ends -- full-strength MOND growth with a constant a_0, now that the derived
     law has removed the decline that used to soften it.
"""

import sys
import numpy as np

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
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


# ---- committed / literature anchors -------------------------------------------------------------
H = 0.674
OM_M, OM_B = 0.315, 0.0493
F_CHI = (OM_M - OM_B) / OM_M              # the fraction of matter carried by the chi sector
LAM_J0 = 2.2                              # Mpc comoving, stage 12/13 calibration
S8_CMB, S8_CMB_ERR = 0.834, 0.016         # Planck 2018 TT,TE,EE+lowE+lensing
S8_WL, S8_WL_ERR = 0.766, 0.020           # representative KiDS-1000 / DES-Y3 lensing scale
R8 = 8.0 / H                              # Mpc (the sigma_8 sphere)

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the scale arithmetic, before any amplitude question")
print("=" * 100)

k_J0 = 2 * np.pi / LAM_J0                 # Mpc^-1
k_J0_h = k_J0 / H                         # h/Mpc
info(f"A0  the chi cutoff today: lam_J = {LAM_J0} Mpc comoving  =>  k_J = {k_J0:.3f} /Mpc = "
     f"{k_J0_h:.2f} h/Mpc.  The sigma_8 sphere is R = 8 h^-1 Mpc = {R8:.2f} Mpc, i.e. k ~ "
     f"{2 * np.pi / R8 / H:.2f} h/Mpc.")


def W_tophat(kR):
    kR = np.asarray(kR, float)
    out = np.ones_like(kR)
    m = kR > 1e-6
    x = kR[m]
    out[m] = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return out


w_at_kJ = float(W_tophat(np.array([k_J0 * R8]))[0])
check(w_at_kJ ** 2 < 1e-4,
      f"A1  *** THE KILL, AND IT IS GEOMETRIC: the sigma_8 top-hat window at the cutoff is "
      f"W(k_J R_8) = {w_at_kJ:.2e}, so W^2 = {w_at_kJ ** 2:.2e}.  sigma_8 is already blind to the "
      f"scale where the mechanism acts, by five orders of magnitude in power ***",
      "no amplitude of suppression at k_J can matter to sigma_8 -- the window has closed")

# the redshift dependence runs the wrong way: comoving lam_J ~ a^2
print("\n     z     lam_J comoving [Mpc]    k_J [h/Mpc]     W^2(k_J R_8)")
for z in (0.0, 0.3, 0.5, 1.0, 2.0):
    lam = LAM_J0 / (1 + z) ** 2
    kj = 2 * np.pi / lam
    w2 = float(W_tophat(np.array([kj * R8]))[0]) ** 2
    print(f"   {z:>4.1f}        {lam:>7.3f}              {kj / H:>6.2f}        {w2:.2e}")

check(LAM_J0 / (1 + 0.5) ** 2 < LAM_J0,
      f"A2  and the redshift trend is ADVERSE: comoving lam_J scales as a^2 (because lam_J ~ rho^-1 "
      f"physical), so today's 2.2 Mpc is the LARGEST it has ever been -- at z = 0.5, where lensing "
      f"S8 is measured, it is {LAM_J0 / 1.5 ** 2:.2f} Mpc (k_J = {2 * np.pi / (LAM_J0 / 1.5 ** 2) / H:.1f} "
      f"h/Mpc).  The mechanism is weakest exactly where the measurement is made",
      "the same a^2 growth that makes the sector safe for the Lyman-alpha forest makes it useless "
      "for S8 -- one property, two consequences, and they point opposite ways")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- compute sigma_8 with the suppression, from a real linear P(k)")
print("=" * 100)

try:
    from classy import Class
    cosmo = Class()
    cosmo.set({"output": "mPk", "P_k_max_h/Mpc": 200.0, "z_max_pk": 3.0,
               "h": H, "omega_b": 0.02237, "omega_cdm": 0.1200,
               "A_s": 2.100e-9, "n_s": 0.9649, "tau_reio": 0.0544,
               "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "T_ncdm": 0.71611})
    cosmo.compute()
    kk = np.logspace(-4, np.log10(190.0), 4000)          # h/Mpc
    Pk = np.array([cosmo.pk_lin(k * H, 0.0) for k in kk]) * H ** 3   # (Mpc/h)^3
    s8_class = cosmo.sigma8()
    cosmo.struct_cleanup(); cosmo.empty()
    HAVE = True
except Exception as exc:                                  # pragma: no cover
    HAVE = False
    info(f"B0  classy unavailable ({exc}) -- Part B cannot run; Parts A, D-F stand on their own")

if HAVE:
    kR = kk * (R8 * H)                                    # dimensionless, k[h/Mpc] * R[Mpc/h]
    W2 = W_tophat(kR) ** 2
    integ = kk ** 2 * Pk * W2 / (2 * np.pi ** 2)

    def sigma8_of(Tk):
        return float(np.sqrt(np.trapz(integ * Tk ** 2, kk)))

    s8_ref = sigma8_of(np.ones_like(kk))
    check(abs(s8_ref / s8_class - 1) < 0.02,
          f"B1  the integrator is validated against CLASS's own sigma8: {s8_ref:.4f} vs "
          f"{s8_class:.4f} ({100 * abs(s8_ref / s8_class - 1):.2f}%)",
          "so the numbers below are a real integral, not a scaling argument")

    # the chi sector's suppression: only f_chi of the matter is affected; baryons still cluster.
    # Two bracketing shapes for the cutoff, both applied at k_J0.
    def T_soft(k, kj):    # gentle, Gnedin-Hui-like pressure filter
        return 1.0 / (1.0 + (k / kj) ** 2)

    def T_hard(k, kj):    # a step: the harshest possible version of the same cutoff
        return (k < kj).astype(float)

    shifts = {}
    print("\n   suppression shape        sigma_8      shift        needed for S8 relief")
    need_frac = 1.0 - S8_WL / S8_CMB
    for name, Tf in (("soft 1/(1+(k/k_J)^2)", T_soft), ("hard step at k_J", T_hard)):
        Tk = 1.0 - F_CHI * (1.0 - Tf(kk, k_J0_h))         # matter = baryons + suppressed chi
        s8 = sigma8_of(Tk)
        print(f"   {name:<24s} {s8:.5f}    {100 * (s8 / s8_ref - 1):+7.3f}%      "
              f"{-100 * need_frac:+.1f}% required")
        shifts[name] = abs(s8 / s8_ref - 1)

    # NOTE the ordering, which is instructive rather than a bug: the STEP is the WEAKEST for
    # sigma_8, because it acts only above k_J where the top-hat window is already closed.  The
    # Gnedin-Hui-type filter suppresses MORE only because its 1/(1+(k/k_J)^2) tail leaks down to
    # k << k_J, i.e. into the scales sigma_8 can see.  A genuine Jeans cutoff does not do that, so
    # the soft filter is the OPTIMISTIC bracket for this idea, not the pessimistic one.
    got = max(shifts.values())
    check(got < 0.3 * need_frac,
          f"B2  *** COMPUTED, taking the shape MOST FAVOURABLE to the idea: the largest sigma_8 "
          f"response any bracket gives is {100 * got:.3f}% (step {100 * shifts['hard step at k_J']:.3f}%, "
          f"filter {100 * shifts['soft 1/(1+(k/k_J)^2)']:.3f}%), against the {100 * need_frac:.1f}% "
          f"S8 relief needs -- short by a factor {need_frac / max(got, 1e-9):.0f} ***",
          "and the ordering is instructive: the STEP is weakest because it acts only where the "
          "top-hat window is shut; the filter only does better via a low-k tail a real Jeans cutoff "
          "does not have")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- what lam_J WOULD S8 relief require, and is that window open?")
print("=" * 100)

if HAVE:
    def lam_needed(Tf):
        lo, hi = 2.0, 800.0
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            kj = (2 * np.pi / mid) / H
            Tk = 1.0 - F_CHI * (1.0 - Tf(kk, kj))
            if abs(sigma8_of(Tk) / s8_ref - 1) < need_frac:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    lam_need_hard = lam_needed(T_hard)
    lam_need = lam_needed(T_soft)          # the FAVOURABLE shape -> the smallest requirement
    print(f"\n   lam_J(today) required for {100 * need_frac:.1f}% S8 relief:")
    print(f"     {lam_need:.1f} Mpc  (soft filter -- the shape most favourable to the idea)")
    print(f"     {lam_need_hard:.1f} Mpc  (hard step)")
    check(lam_need > 4 * LAM_J0,
          f"D1  S8 relief would require lam_J(today) ~ {lam_need:.1f} Mpc comoving -- "
          f"{lam_need / LAM_J0:.0f}x the committed {LAM_J0} Mpc, taking the SOFT filter (the shape "
          f"most favourable to the idea; the step needs {lam_need_hard:.0f} Mpc)",
          "and this is the number that closes the door, for a reason internal to the framework")

    info(f"D2  WHY THAT WINDOW IS CLOSED, and it is closed by the framework's OWN best result: "
         f"lam_J(today) = {LAM_J0} Mpc was not a free choice -- it is stage 12's weak-lensing "
         f"exclusion radius, the outer edge over which the pure MOND kernel fits the KiDS RAR at "
         f"chi^2/dof ~ 1 with NO dark component.  Pushing lam_J to ~{lam_need:.0f} Mpc does not "
         f"conflict with that fit (a LARGER cutoff means even less chi clustering, which stage 12 "
         f"prefers) -- it conflicts with everything ELSE: a matter power spectrum missing "
         f"{100 * F_CHI:.0f}% of its power below ~{lam_need:.0f} Mpc comoving would erase galaxy "
         f"clustering and cluster abundance wholesale.  Stage 13's own upper bound is the binding "
         f"one: route C's CMB-lensing requirement forces the chi sector to still CLUSTER down to "
         f"z < 0.30, which caps lam_J near the committed value.")

    info("D3  so the honest structure of the result: the sector's Jeans scale is pinned near 2.2 Mpc "
         "from BOTH sides -- a lower bound from stage 12's lensing fit, an upper bound from CMB "
         "lensing -- and the S8-relief value sits far outside that pin.  There is no version of the "
         "gamma = 0 sector that fixes S8 and survives its own constraints.")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- does the framework push S8 the OTHER way?  (the against-interest half)")
print("=" * 100)

info("E1  AT LINEAR ORDER, NO -- AND THAT IS A THEOREM FROM THIS WEEK, NOT AN ASSUMPTION.  Stage 18 "
    "proved every promotion-generated coupling vanishes on FRW (delta Y^(1) = 0 identically; the "
    "promoted MOND term starts at THIRD order) and stage 19 showed the resulting background differs "
    "from LambdaCDM by one cold a^-3 trace, with Delta chi^2 = 1.3 against cosmic variance.  So the "
    "framework's LINEAR growth, sigma_8 and S8 are LambdaCDM's -- *** the S8 tension is INHERITED "
    "UNCHANGED, neither alleviated nor aggravated at linear order. ***")

info("E2  AT NONLINEAR ORDER THE SIGN IS ADVERSE, and it is the framework's own published "
    "prediction: row 5 of THE_COMPLETION lists 'accelerated structure formation -- earlier massive "
    "objects' as a falsifiable consequence.  MOND enhances collapse; enhanced collapse means MORE "
    "structure, i.e. a HIGHER effective S8, which is the wrong direction for the tension.  "
    "Quantifying it needs a MOND nonlinear/N-body treatment that this corpus does not have (and the "
    "stage 1-3 sequence established that the khronon dust is an irrotational potential flow, so a "
    "standard PM code computes nothing that exists here).  UNPRICED, and named as unpriced.")

info("E3  AND THE v8 DERIVED LAW REMOVED THE ONLY SOFTENER.  The withdrawn CPL-dressed a_0(z) "
    "declined to 0.74 by z = 3, which would have damped exactly this enhanced early growth.  The "
    "derived law is flat to <1% below z ~ 5, so MOND runs at FULL strength through all of structure "
    "formation.  This is the same exposure stage 21 opened at the high-z end (a_0(10) = 0.99 vs the "
    "old 0.36, Nusser over-production unpriced) -- *** S8 and cosmic dawn are the two ends of ONE "
    "front, and the derived law made both harder. ***  That is the real result of this stage.")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
if HAVE:
    print(f"""
  THE S8 IDEA IS DEAD, AND IT DIED ON SCALE, NOT AMPLITUDE.

  1. GEOMETRIC KILL: the sigma_8 top-hat window at the chi cutoff is W^2 = {w_at_kJ ** 2:.1e}.
     sigma_8 is blind to the scale where the mechanism acts, by five orders of magnitude in power.
  2. COMPUTED: the largest sigma_8 response any bracket gives (soft filter at k_J = {k_J0_h:.2f} h/Mpc)
     is {100 * got:.3f}%, against the {100 * need_frac:.1f}% that S8 relief requires -- short by ~{need_frac / max(got, 1e-9):.0f}x.
  3. THE REDSHIFT TREND IS ADVERSE: comoving lam_J ~ a^2, so the cutoff is SMALLEST in the past and
     the mechanism is weakest exactly at the z ~ 0.5 where lensing S8 is measured.
  4. NO REPAIR EXISTS: S8 relief needs lam_J ~ {lam_need:.0f} Mpc, and the sector's Jeans scale is pinned
     near 2.2 Mpc from both sides (stage 12's lensing fit below, CMB lensing above).
  5. AGAINST INTEREST, and the part worth keeping: at linear order the framework's S8 IS LambdaCDM's
     by stages 18/19, so the tension is inherited unchanged; at nonlinear order MOND's enhanced
     collapse pushes S8 UP, the wrong way, and the v8 derived law removed the a_0(z) decline that
     used to soften it.  S8 and stage 21's cosmic-dawn exposure are ONE front seen from two ends.

  A dud, reported as a dud.  The sleeper does not wake up.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
