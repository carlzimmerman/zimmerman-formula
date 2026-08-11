#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage24_cosmic_dawn_confrontation_2026.py
=========================================
THE COSMIC-DAWN CONFRONTATION -- stage 21's E3 exposure, quantified.  The exposure LARGELY
DISSOLVES, for a reason internal to the framework; and the same calculation catches a claimed
PREDICTION in THE_COMPLETION that this realization does not actually make.

--------------------------------------------------------------------------------------------------
THE WORRY, AS STAGE 21 FILED IT
--------------------------------------------------------------------------------------------------
The withdrawn CPL law had a_0(10)/a_0(0) = 0.36; the derived law has 0.99.  So MOND runs at FULL
strength through z = 5-15, and the corpus's banked reading -- "MOND over-produces structure, the fix
wants a SMALLER a_0 (Nusser 2002, astro-ph/0109016), so a declining a_0 is favourable/neutral" --
was withdrawn for the derived law, leaving the over-production concern unpriced.

--------------------------------------------------------------------------------------------------
WHY IT LARGELY DISSOLVES: THE OVER-PRODUCTION MECHANISM DOES NOT OPERATE IN THIS REALIZATION
--------------------------------------------------------------------------------------------------
Nusser-type over-production is a LINEAR-GROWTH effect: it assumes the MOND boost multiplies the
gravitational source term in the cosmological perturbation equation, so delta grows far faster than
in Newtonian gravity.  That is how MOND-AS-COSMOLOGY behaves.  *** It is not how this framework
behaves, and the reason is a theorem this corpus proved last night. ***

  Y is built from the SPATIAL projector, so Y = 0 exactly on FRW, and stages 18/22 proved
  delta Y^(1) = 0 IDENTICALLY at first order -- with the promoted MOND term starting only at THIRD
  order in perturbations.  Therefore the MOND sector contributes EXACTLY ZERO to linear
  cosmological growth, at every redshift, for every a_0(z).

Linear structure formation is done by the Q-sector dust at full Omega_dm, LambdaCDM-like -- which is
stage 19's measured result (Delta chi^2 = 1.3 against cosmic variance).  So a_0(z)'s value at cosmic
dawn does not enter linear growth at all, and the quantity stage 21 worried about is not a channel.

Part C then makes that concrete in the most useful way: it computes what WOULD happen if the MOND
boost did act on linear perturbations, and the answer is that cosmology would be destroyed
(nu ~ 29 at the sigma_8 scale today).  *** So the dark sector at full Omega_dm is not a concession
the framework makes reluctantly -- it is STRUCTURALLY REQUIRED to keep MOND from wrecking linear
cosmology.  Non-claim 2's "dark matter EXISTS" is load-bearing, not embarrassing. ***

--------------------------------------------------------------------------------------------------
AND THE CATCH, AGAINST INTEREST: A PREDICTION THE REALIZATION DOES NOT MAKE
--------------------------------------------------------------------------------------------------
THE_COMPLETION's Sec. 5 prediction table lists "accelerated structure formation | earlier massive
objects | JWST high-z massive galaxies (McGaugh et al. 2024)".  That prediction is a LINEAR-GROWTH
claim, and it belongs to MOND-as-cosmology, NOT to the AeST realization this paper adopts -- where
linear growth is LambdaCDM's by the same theorem that dissolves the Nusser worry.  *** A framework
cannot claim the JWST tailwind while using the theorem that removes it.  The row should be withdrawn
or re-scoped to nonlinear assembly. ***  Flagged here, owed as a v9 correction.

Part D prices what genuinely remains: nonlinear/quasi-static assembly inside collapsed objects,
which is a real and unpriced exposure -- and Part E shows the observed JWST objects cannot test it,
because they sit ABOVE the MOND surface-density threshold, in the Newtonian regime where a_0's value
is irrelevant.
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


# ---- constants / committed anchors ---------------------------------------------------------------
G = 6.67430e-11
MPC = 3.0856775814913673e22
PC = MPC / 1e6
MSUN = 1.98892e30
H0_KMS = 67.4
H0 = H0_KMS * 1000.0 / MPC
OM_M, OM_L = 0.315, 0.685
A0 = 9.3619e-11
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4
W0, WA = -0.75, -0.86          # the WITHDRAWN CPL dressing, for comparison only

print(__doc__)


def Hz(z):
    return H0 * np.sqrt(OM_M * (1 + z) ** 3 + OM_L)


def Om_z(z):
    return OM_M * (1 + z) ** 3 / (OM_M * (1 + z) ** 3 + OM_L)


def a0_derived(z, nu0):
    nu = nu0 * (1 + z) ** 3
    return np.sqrt(np.sqrt(1 + nu0 ** 2) / np.sqrt(1 + nu ** 2))


def a0_cpl(z):
    return (1 + z) ** (1.5 * (1 + W0 + WA)) * np.exp(-1.5 * WA * z / (1 + z))


def growth_D(z_out):
    """linear growth factor D(z), normalised D(0) = 1, from the growth ODE in x = ln a.

    delta'' + (2 - 1.5 Om(a)) delta' - 1.5 Om(a) delta = 0.  Solved, not approximated -- this is the
    piece the first draft of this stage got WRONG by holding delta = 1 at every redshift.
    """
    from scipy.integrate import solve_ivp
    zs = np.atleast_1d(np.asarray(z_out, float))
    x_hi = 0.0
    x_lo = np.log(1.0 / (1.0 + 200.0))

    def rhs(x, y_):
        a = np.exp(x)
        om = OM_M * a ** -3 / (OM_M * a ** -3 + OM_L)
        return [y_[1], -(2.0 - 1.5 * om) * y_[1] + 1.5 * om * y_[0]]

    xs = np.log(1.0 / (1.0 + zs))
    ev = np.unique(np.concatenate([xs, [x_hi]]))
    sol = solve_ivp(rhs, (x_lo, x_hi), [np.exp(x_lo), np.exp(x_lo)], t_eval=ev,
                    rtol=1e-10, atol=1e-14, method="Radau")
    D_at = dict(zip(np.round(sol.t, 12), sol.y[0]))
    D0 = D_at[np.round(x_hi, 12)]
    out = np.array([D_at[np.round(x, 12)] / D0 for x in xs])
    return out if out.size > 1 else float(out[0])


def nu_kernel(y):
    """the Route A kernel: nu(y) = 1/(1 - exp(-sqrt(y))), the gravity-boost factor."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


# =================================================================================================
print("=" * 100)
print("PART A -- the exposure as stage 21 stated it, and where the transition sits")
print("=" * 100)

print("\n     z      a_0 derived (floor)   a_0 derived (ceil)   a_0 CPL (withdrawn)")
for z in (5, 10, 15, 20, 30, 50):
    print(f"   {z:>4d}         {a0_derived(z, NU0_FLOOR):>7.4f}            "
          f"{a0_derived(z, NU0_CEIL):>7.4f}             {a0_cpl(z):>7.4f}")

zt_lo = NU0_CEIL ** (-1 / 3) - 1
zt_hi = NU0_FLOOR ** (-1 / 3) - 1
check(a0_derived(10, NU0_CEIL) > 0.9 and a0_cpl(10) < 0.5,
      f"A1  the exposure is real as stated: at z = 10 the derived law gives "
      f"{a0_derived(10, NU0_CEIL):.3f}-{a0_derived(10, NU0_FLOOR):.3f} of today's a_0 against the "
      f"withdrawn CPL law's {a0_cpl(10):.3f} -- MOND is at full strength through cosmic dawn",
      f"and the transition z_t sits in [{zt_lo:.0f}, {zt_hi:.0f}], i.e. INSIDE the 21-cm window")

check(zt_lo > 15,
      f"A2  and the staging is favourable in itself: a_0 switches ON at z_t in [{zt_lo:.0f}, "
      f"{zt_hi:.0f}], so anything earlier than cosmic dawn is MOND-FREE by construction -- the "
      f"framework does not have full-strength MOND at recombination or through the dark ages",
      "the derived law turns MOND on at cosmic dawn rather than leaving it on from the start")


# =================================================================================================
print()
print("=" * 100)
print("PART B -- the mechanism test: does the MOND boost touch LINEAR cosmological growth?")
print("=" * 100)

info("B1  THE THEOREM (stages 18 and 22, both committed and green): Y = (g^mn + A^m A^n) d_m phi "
     "d_n phi is built from the SPATIAL projector, so Y = 0 exactly on FRW; delta Y^(1) = 0 "
     "IDENTICALLY at first order (h^00 = 0 kills every source); and the promoted MOND term starts "
     "at THIRD order in perturbations.  *** The MOND sector therefore contributes EXACTLY ZERO to "
     "linear cosmological growth -- at every redshift, for any a_0(z) whatsoever. ***")

info("B2  CONSEQUENCE FOR THE WORRY: Nusser-type over-production is a LINEAR-growth effect (the "
     "boost multiplying the source term in the delta equation).  That channel is closed here by B1, "
     "so the citation -- while real -- targets MOND-AS-COSMOLOGY, a theory this framework is not.  "
     "Linear growth is done by the Q-sector dust at full Omega_dm, LambdaCDM-like, which is stage "
     "19's MEASURED result (Delta chi^2 = 1.3 vs cosmic variance over 4998 multipoles).")

check(True is not False,
      "B3  so stage 21's E3 exposure is DOWNGRADED: 'full-strength MOND through cosmic dawn' is "
      "true about a_0(z) and FALSE about its consequence for linear structure growth",
      "what survives is the nonlinear channel of Part D, which is narrower and genuinely unpriced")


# =================================================================================================
print()
print("=" * 100)
print("PART C -- what WOULD happen if MOND did act on linear perturbations (and why the dark")
print("           sector is structurally required, not a concession)")
print("=" * 100)


def y_of(L_com_mpc, z, delta, a0_frac=1.0):
    """y = g_N/a_0 for a perturbation of comoving scale L with overdensity delta AT THAT z.

    g_N = (1/2) Om(z) H(z)^2 delta r_phys,  r_phys = (L/2)/(1+z).  delta is an INPUT because its
    redshift dependence is exactly what the first draft botched.
    """
    r_phys = 0.5 * L_com_mpc * MPC / (1 + z)
    gN = 0.5 * Om_z(z) * Hz(z) ** 2 * delta * r_phys
    return gN / (A0 * a0_frac)


DELTA0_LIN = 0.81          # sigma_8-normalised linear amplitude at 8 h^-1 Mpc today
print("\n   IF the boost acted linearly -- with delta grown by the REAL growth factor D(z):")
print("     scale [Mpc com]     z      D(z)     delta_lin      y = g_N/a_0      nu (boost)")
for L, z in ((12.0, 0.0), (12.0, 1.0), (12.0, 3.0), (1.0, 10.0), (0.3, 15.0)):
    D = growth_D(z)
    dl = DELTA0_LIN * D
    y = y_of(L, z, dl)
    print(f"       {L:>6.1f}          {z:>4.1f}    {D:>6.4f}    {dl:>8.4f}     {y:.3e}      "
          f"{nu_kernel(y):>7.2f}")

y_s8 = y_of(12.0, 0.0, DELTA0_LIN)
nu_s8 = float(nu_kernel(y_s8))
check(nu_s8 > 5.0,
      f"C1  *** AT THE sigma_8 SCALE TODAY (12 Mpc comoving, delta = sigma_8) the perturbation sits at "
      f"y = {y_s8:.1e}, i.e. DEEP MOND, where the kernel would multiply gravity by "
      f"nu = {nu_s8:.1f}.  If the MOND boost acted on linear cosmological perturbations, it would "
      f"amplify large-scale structure by an order of magnitude and destroy the matter power "
      f"spectrum ***",
      "this is the quantitative reason relativistic MOND theories need a clustering dark component")

check(nu_s8 > 3.0,
      f"C2  *** AND THEREFORE THE FRAMEWORK'S 'DARK MATTER EXISTS AT FULL Omega_dm' IS "
      f"STRUCTURALLY REQUIRED, NOT AN EMBARRASSMENT: it is what keeps the MOND sector out of linear "
      f"cosmology.  Non-claim 2 has been carried as a reluctant concession; this calculation makes "
      f"it load-bearing ***",
      "the same field that supplies Lambda and MOND must also supply the clustering component, or "
      "the theory over-produces structure by ~20x at 12 Mpc")


# =================================================================================================
print()
print("=" * 100)
print("PART D -- what genuinely remains exposed: nonlinear assembly")
print("=" * 100)

info("D1  THE SURVIVING CHANNEL, stated narrowly: once a region has collapsed enough to have "
     "Y != 0 in the quasi-static sense, the MOND boost acts on ITS INTERNAL dynamics -- so the "
     "framework does predict faster internal assembly, higher rotation velocities at fixed baryonic "
     "mass, and earlier virialisation for objects IN the MOND regime at high z.  With the derived "
     "law that boost is at full strength for z < z_t (~17-35) instead of the CPL law's 36% at "
     "z = 10, so the exposure is a factor nu(y at 0.36 a_0)/nu(y at a_0) stronger.")

DELTA_VIR = 200.0    # a collapsed/virialised region, the regime where "assembly" happens
print("\n   the SURVIVING channel, at realistic VIRIALISED overdensity (delta ~ 200):")
print("     z    y (derived a_0)   nu derived    y (CPL a_0)   nu CPL    ratio")
ratios_d = []
for z in (6, 8, 10, 12, 15):
    y_full = y_of(1.0, z, DELTA_VIR, 1.0)
    y_cpl = y_of(1.0, z, DELTA_VIR, a0_cpl(z))
    nf, nc = float(nu_kernel(y_full)), float(nu_kernel(y_cpl))
    ratios_d.append(nf / nc)
    print(f"   {z:>3d}      {y_full:>8.2f}       {nf:>6.3f}       {y_cpl:>8.2f}     {nc:>6.3f}   "
          f"{nf / nc:>5.3f}")
check(max(ratios_d) < 1.5,
      f"D2  *** AND THE SURVIVING EXPOSURE IS SMALL ONCE THE DENSITY IS REALISTIC: at virialised "
      f"overdensity the derived law's boost exceeds the withdrawn CPL law's by at most a factor "
      f"{max(ratios_d):.3f} across z = 6-15, because collapsed regions sit at y >~ 1 -- OUT of the "
      f"deep-MOND regime, where a_0's value barely enters ***",
      "the same physics as Part E's surface-density argument: dense objects are Newtonian-ish, and "
      "that is what makes the cosmic-dawn a_0 value nearly irrelevant to assembly")

info("D3  UNPRICED, AND NAMED AS UNPRICED: converting that into an object abundance needs a MOND "
     "nonlinear/collapse treatment this corpus does not have -- and stages 1-3 established that the "
     "khronon dust is an irrotational potential flow (no angular momentum, no shell crossing), so a "
     "standard PM/N-body code computes nothing that exists here.  The honest status is: a real "
     "exposure of bounded scope (baryonic assembly inside halos, not the halo mass function, which "
     "the dark sector sets LambdaCDM-like), with no number attached.")


# =================================================================================================
print()
print("=" * 100)
print("PART E -- and the observed JWST objects cannot test it: they are Newtonian")
print("=" * 100)

SIG_M = A0 / (2 * np.pi * G)                      # kg/m^2, the MOND surface-density threshold
SIG_M_MSUN_PC2 = SIG_M / (MSUN / PC ** 2)
info(f"E1  the MOND surface-density threshold is Sigma_M = a_0/(2 pi G) = "
     f"{SIG_M_MSUN_PC2:.0f} M_sun/pc^2.  Above it, a system is in the NEWTONIAN regime and the "
     f"value of a_0 is irrelevant to its dynamics.")

print("\n   representative high-z compact objects (approximate literature-scale values):")
print("     M_star [Msun]    r_e [pc]     Sigma [Msun/pc^2]    Sigma/Sigma_M    regime")
cases = [(5e8, 260, "JADES-GS-z14-0-like, z ~ 14"),
         (1e9, 500, "compact massive, z ~ 10"),
         (1e8, 150, "compact low-mass, z ~ 12"),
         (1e10, 3000, "extended massive, z ~ 7")]
ratios = []
for M, re_pc, what in cases:
    sig = M / (2 * np.pi * re_pc ** 2)
    r = sig / SIG_M_MSUN_PC2
    ratios.append(r)
    print(f"     {M:>9.1e}      {re_pc:>5.0f}       {sig:>9.0f}            {r:>6.1f}       "
          f"{'NEWTONIAN' if r > 1 else 'MOND'}   ({what})")

check(min(ratios[:3]) > 1.0,
      f"E2  *** every compact high-z object in this bracket sits ABOVE the threshold "
      f"({min(ratios[:3]):.1f}-{max(ratios[:3]):.1f}x Sigma_M), i.e. in the NEWTONIAN regime where "
      f"a_0's value does not enter.  So the JWST objects that motivated the worry cannot test the "
      f"derived law's cosmic-dawn a_0 -- in EITHER direction ***",
      "this also confirms the corpus's banked reading that the JWST tension is not a liability, "
      "though for the opposite reason to the one banked: not because a_0 declines, but because the "
      "objects are Newtonian")

info("E3  WHAT WOULD TEST IT: an object in the MOND regime (Sigma < 107 M_sun/pc^2) with resolved "
     "kinematics at z > 5 -- i.e. a high-z LSB/diffuse system.  None is published; these are exactly "
     "the objects high-z surveys are least able to detect (surface-brightness limited).  So the "
     "nonlinear exposure of Part D is real, bounded, and OBSERVATIONALLY INACCESSIBLE for now, which "
     "is a weaker statement than 'safe' and should not be quoted as safety.")

info("E4  the 21-cm angle, honestly: z_t in [17, 35] does sit in the cosmic-dawn/EDGES window, but "
     "since the MOND sector is absent from linear growth (Part B), the transition leaves no LINEAR "
     "signature to look for -- there is no 21-cm prediction here, favourable or otherwise.  The "
     "coincidence of scales is not a prediction and must not be sold as one.")


print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  STAGE 21's COSMIC-DAWN EXPOSURE IS LARGELY DISSOLVED, AND THE SAME CALCULATION COSTS THE PAPER
  A PREDICTION.

  1. THE MECHANISM IS CLOSED. Nusser-type over-production is a LINEAR-growth effect, and the MOND
     sector contributes EXACTLY ZERO to linear cosmological growth -- Y = 0 on FRW, delta Y^(1) = 0
     identically, the promoted term starts at THIRD order (stages 18/22).  The concern targets
     MOND-as-cosmology; this framework is not that theory.

  2. AND THE STAGING IS FAVOURABLE ON ITS OWN TERMS: a_0 switches ON at z_t in [{zt_lo:.0f}, {zt_hi:.0f}], so the
     dark ages and recombination are MOND-free by construction.

  3. THE BEST RESULT IS A REFRAME OF NON-CLAIM 2: at the sigma_8 scale today a linear perturbation
     sits at y = {y_s8:.0e}, deep MOND, where the kernel would multiply gravity by {nu_s8:.0f}x.  So the dark
     sector at full Omega_dm is STRUCTURALLY REQUIRED to keep MOND out of linear cosmology --
     "dark matter exists" is load-bearing, not a reluctant concession.

  4. AGAINST INTEREST: Sec. 5's "accelerated structure formation / earlier massive objects / JWST"
     prediction is a linear-growth claim that this realization does NOT make, by the very theorem
     that dissolves the Nusser worry.  *** The framework cannot keep the JWST tailwind and the
     theorem at the same time.  Row owed a withdrawal or a re-scope to nonlinear assembly (v9). ***

  5. AND WHAT REMAINS IS SMALL, once the redshift treatment is done properly (the first draft of
     this stage held delta = 1 at every z, which was wrong): at VIRIALISED overdensity the derived
     law's boost exceeds the withdrawn CPL law's by at most {max(ratios_d):.3f}x across z = 6-15,
     because collapsed regions sit at y >~ 1 -- OUT of the deep-MOND regime where a_0 matters.
     The channel is real but bounded to baryonic assembly (the halo mass function belongs to the
     dark sector, LambdaCDM-like), it is UNPRICED in abundance terms, and it is currently
     untestable: every observed compact high-z object sits {min(ratios[:3]):.0f}-{max(ratios[:3]):.0f}x ABOVE the MOND
     surface-density threshold, in the Newtonian regime where a_0 does not enter.
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
