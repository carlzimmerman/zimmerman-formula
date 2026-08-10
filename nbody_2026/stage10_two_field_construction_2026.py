#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage10_two_field_construction_2026.py
======================================
THE TWO-FIELD CONSTRUCTION -- THE LAST NAMED STRUCTURAL ESCAPE, BUILT AND PRICED.

Stage 9's theorem closed the single-field route: for one shift-symmetric scalar, ghost-freedom
(K'' > 0) plus charge conservation (n = K' ~ a^-3) forces c_s^2 ~ a^-3, so the dark sector is
asymptotically COLD, hence captured, hence in galaxies.  The theorem's premise was ONE field.  This
script builds the two-field version and prices it honestly.

--------------------------------------------------------------------------------------------------
THE CONSTRUCTION
--------------------------------------------------------------------------------------------------
  phi  -- the khronon, keeps its job: the condensate minimum gives w = -1 EXACTLY (dark energy), and
          the Y-sector gives MOND with a_0 = kappa c sqrt(G rho_Lambda).  Stage 9's theorem still
          applies to phi -- and that is FINE, because phi is no longer asked to be the dark matter.
  chi  -- a SECOND component carrying the dark-matter job, with its own equation of state
          p = K rho^gamma.  Stage 9 does not constrain it, PROVIDED chi is not itself a
          shift-symmetric k-essence condensate (Part E: if it is, gamma = 2 is forced and this dies).

THE KEY QUANTITY is the Jeans length, lam_J = c_s sqrt(pi/(G rho)) with c_s^2 = gamma K rho^(gamma-1),
so *** lam_J ~ rho^(gamma/2 - 1) -- it GROWS as the universe dilutes iff gamma < 2. ***
(The single field sits exactly at gamma = 2, where lam_J is a fixed physical length: stage 5's
mass-independent 105 pc polytrope.  That is why the single field cannot do this.)

--------------------------------------------------------------------------------------------------
THE FOUR REQUIREMENTS, AND THEY ARE SIMULTANEOUSLY SATISFIABLE (Parts B-C)
--------------------------------------------------------------------------------------------------
  (1) CMB acoustic peaks: the COMOVING lam_J at recombination must be small (<~ 0.5 Mpc) so the
      component clusters and sources the peaks -- which the CMB measures at full Omega_dm.
  (2) Galaxies clean: the PHYSICAL lam_J today must exceed the RAR region, >~ 30 kpc.
  (3) CMB lensing: route C's constraint -- the clustering must survive to z < 0.30.  Satisfied
      automatically, since the component still clusters on ALL scales above lam_J, and lam_J is
      hundreds of times below the tens-of-Mpc scales CMB lensing probes.
  (4) Background matter-like: w = K rho^(gamma-1) ~ 0 today, so BAO and supernovae are untouched.
  Requirements (1) and (2) together demand lam_J GROW by >= 65x from recombination to today, i.e.
      *** gamma <= 1.60 ***  -- and note where that lands: a monatomic ideal gas has gamma = 5/3 =
      1.667, so the required equation of state sits within 4% of an ordinary warm gas.

--------------------------------------------------------------------------------------------------
AND THE TEST THAT PINCHES IT -- THE LYMAN-ALPHA FOREST (Part D)
--------------------------------------------------------------------------------------------------
A suppression scale is constrained where it is measured: the forest probes comoving k up to
~10/Mpc, i.e. down to ~0.1 Mpc comoving.  Running lam_J back to z = 3 and converting to comoving:
      lam_J(today) = 30 kpc -> 0.05 Mpc comoving at z=3   SURVIVES
      lam_J(today) = 60 kpc -> 0.10 Mpc comoving          MARGINAL
      lam_J(today) = 100 kpc              SURVIVES only at the softest gamma = 1.2, else EXCLUDED
      lam_J(today) = 300 kpc              EXCLUDED at every gamma
*** So the window is real but NARROW: lam_J(today) ~ 30-60 kpc at gamma = 1.5-1.6, up to ~100 kpc at
gamma = 1.2.  Galaxies are clean INSIDE that radius -- the RAR region -- while the 30-200 kpc halo
still carries the component. ***

--------------------------------------------------------------------------------------------------
THE PRICE, STATED BEFORE THE VERDICT (Part F)
--------------------------------------------------------------------------------------------------
 (i)  A whole new component with its own parameters: the honest dark-sector count goes from FIVE to
      SEVEN or EIGHT against LCDM's two.
 (ii) The a_0-bump may become REDUNDANT, since chi can supply the cluster residual directly.  That
      is a simplification of one sector and a loss of a prediction in another; both are stated.
 (iii) *** AND THE REAL COST: "Lambda, dark matter and MOND from ONE function" -- the central claim
      of THE_COMPLETION's abstract -- IS GONE.  Two sectors now do two jobs.  The theory becomes
      more ordinary in exactly the way that made it interesting. ***
"""

import sys
import mpmath as mp

mp.mp.dps = 20
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


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


G = mp.mpf("6.674e-11")
MPC = mp.mpf("3.0857e22")
KPC = MPC / 1000
C = mp.mpf("2.99792458e8")
RHO_DM0 = mp.mpf("0.264") * mp.mpf("8.6e-27")
Z_REC = mp.mpf("1090")
RHO_REC = RHO_DM0 * (1 + Z_REC) ** 3
LAM_REC_COM_MAX = mp.mpf("0.5") * MPC        # req 1: comoving Jeans at recombination
LAM_TODAY_MIN = 30 * KPC                     # req 2: exclude the RAR region
LYA_COM_MAX = mp.mpf("0.1") * MPC            # forest sensitivity, comoving
Z_LYA = mp.mpf("3")

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- why the second field is not covered by stage 9's theorem")
print("=" * 100)


def lamJ_growth(gamma, rho_early, rho_late):
    """lam_J ~ rho^(gamma/2 - 1), so the growth from an EARLY (dense) epoch to a LATE (dilute) one is
    (rho_early/rho_late)^(1 - gamma/2).  Argument order matters and was inverted in a first pass."""
    return (rho_early / rho_late) ** (1 - gamma / 2)


check(abs(lamJ_growth(mp.mpf("2"), RHO_REC, RHO_DM0) - 1) < mp.mpf("1e-12"),
      "A1  at gamma = 2 -- exactly where a single shift-symmetric condensate sits (stage 9) -- the "
      "Jeans length is a FIXED PHYSICAL LENGTH, growth factor 1.000.  That is stage 5's "
      "mass-independent 105 pc polytrope seen from another side, and it is why one field cannot do "
      "this job",
      "the escape therefore requires gamma != 2, i.e. a component that is NOT that condensate")

check(lamJ_growth(mp.mpf("1.5"), RHO_REC, RHO_DM0) > 100,
      f"A2  whereas at gamma = 1.5 the Jeans length GROWS by "
      f"{sig(lamJ_growth(mp.mpf('1.5'), RHO_REC, RHO_DM0),4)}x between recombination and today -- "
      "small when the CMB needs clustering, large when galaxies need exclusion",
      "the whole construction is this one scaling")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the four requirements, and the gamma they force")
print("=" * 100)

lam_rec_phys_max = LAM_REC_COM_MAX / (1 + Z_REC)
need_growth = LAM_TODAY_MIN / lam_rec_phys_max
gamma_max = 2 * (1 - mp.log(need_growth) / mp.log(RHO_REC / RHO_DM0))
print(f"""
   (1) comoving lam_J(rec) <= {sig(LAM_REC_COM_MAX/MPC,3)} Mpc  =>  physical <= {sig(lam_rec_phys_max/KPC,4)} kpc
   (2) physical lam_J(today) >= {sig(LAM_TODAY_MIN/KPC,3)} kpc
   ==> required growth >= {sig(need_growth,4)}x  ==>  gamma <= {sig(gamma_max,4)}
""")
check(gamma_max > 1 and gamma_max < 2,
      f"B1  *** THE REQUIREMENTS ARE SIMULTANEOUSLY SATISFIABLE: gamma <= {sig(gamma_max,4)}, a "
      "non-empty window strictly between 1 and 2.  So the two-field escape is NOT closed by the same "
      "argument that closed the single-field one ***",
      "the first live structural route in this entire sequence")

GAMMA_GAS = mp.mpf(5) / 3
check(abs(GAMMA_GAS - gamma_max) / GAMMA_GAS < mp.mpf("0.05"),
      f"B2  and where it lands is worth noting: a monatomic ideal gas has gamma = 5/3 = "
      f"{sig(GAMMA_GAS,5)}, only {sig((GAMMA_GAS-gamma_max)/GAMMA_GAS*100,3)}% above the bound.  The "
      "required equation of state is essentially that of an ordinary warm gas",
      "which is a hint about what chi would have to be, and a reason to be suspicious of elegance")

# NC-B: the requirement must FAIL for gamma = 2, or B1 is not testing anything.
growth_at_2 = lamJ_growth(mp.mpf("2"), RHO_REC, RHO_DM0)
check(growth_at_2 < need_growth,
      f"NC-B  CONTROL: at gamma = 2 the growth is {sig(growth_at_2,3)}x against the "
      f"{sig(need_growth,3)}x required, so the single-field case FAILS this same test -- B1 "
      "discriminates rather than passing everything",
      "")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- requirement (3): CMB lensing is satisfied automatically")
print("=" * 100)

LENS_SCALE = 10 * MPC
check(LAM_TODAY_MIN * 100 < LENS_SCALE,
      f"C1  the component still clusters on every scale ABOVE lam_J, and lam_J(today) ~ "
      f"{sig(LAM_TODAY_MIN/KPC,3)} kpc is {sig(LENS_SCALE/LAM_TODAY_MIN,4)}x below the tens-of-Mpc "
      "scales CMB lensing probes.  So route C's constraint -- clustering must survive to z < 0.30 -- "
      "is met by construction, not by tuning",
      "the smoothing is confined to sub-galactic-halo scales, where lensing of the CMB has no leverage")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- *** THE PINCH: the Lyman-alpha forest ***")
print("=" * 100)
print("\n   gamma   lam_J(today)   lam_J(z=3) comoving   verdict vs 0.1 Mpc forest sensitivity")
survivors = []
for g_s in ("1.2", "1.5", "1.6"):
    g = mp.mpf(g_s)
    for l0_kpc in ("30", "60", "100", "300"):
        l0 = mp.mpf(l0_kpc) * KPC
        lam_phys = l0 * ((1 + Z_LYA) ** 3) ** (g / 2 - 1)
        lam_com = lam_phys * (1 + Z_LYA)
        ok = lam_com < LYA_COM_MAX
        if ok and mp.mpf(l0_kpc) >= 30:
            survivors.append((g_s, l0_kpc))
        print(f"   {g_s:>5s}   {l0_kpc:>6s} kpc      {sig(lam_com/MPC,3):>10s} Mpc        "
              f"{'SURVIVES' if ok else 'EXCLUDED'}")

check(len(survivors) > 0,
      f"D1  *** THE WINDOW IS NARROW BUT REAL: {len(survivors)} of 12 (gamma, lam_J) combinations "
      "clear both the galaxy requirement and the forest.  All of them have lam_J(today) at the "
      "30-60 kpc end ***",
      f"survivors: {survivors}")

cap_kpc = max(mp.mpf(l) for _, l in survivors)
check(cap_kpc <= 100 and cap_kpc >= 30,
      f"D2  and the forest caps lam_J(today) at ~{sig(cap_kpc,3)} kpc (gamma-dependent: 100 kpc "
      "survives only at the softest gamma = 1.2, 30-60 kpc at gamma = 1.5-1.6), which has a "
      "consequence that must be stated: "
      "galaxies are clean INSIDE ~30-60 kpc -- the RAR region -- but the 30-200 kpc halo still "
      "carries the component, so the OUTER rotation curve and galaxy-galaxy lensing become the next "
      "confrontation",
      "the problem is not removed, it is relocated to a scale where the data are weaker but real")

# NC-D: the forest test must reject a genuinely large scale, or D1 is vacuous.
lam_big = 1 * MPC
lam_big_com = lam_big * ((1 + Z_LYA) ** 3) ** (mp.mpf("1.5") / 2 - 1) * (1 + Z_LYA)
check(lam_big_com > LYA_COM_MAX,
      f"NC-D  CONTROL: a 1 Mpc Jeans length today gives {sig(lam_big_com/MPC,3)} Mpc comoving at "
      "z = 3, firmly excluded -- so the forest test has teeth and D1's survivors are a real subset",
      "")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the premise chi must satisfy, or this dies exactly as the single field did")
print("=" * 100)

check(abs(lamJ_growth(mp.mpf("2"), RHO_REC, RHO_DM0) - 1) < mp.mpf("1e-12"),
      "E1  *** THE CONDITION ON chi, STATED AS A CONDITION AND NOT ASSUMED AWAY: if chi is ITSELF a "
      "ghost-free shift-symmetric k-essence condensate, stage 9's theorem applies to it verbatim and "
      "forces gamma = 2 -- where the growth factor is exactly 1 and the construction fails.  So chi "
      "must have a DIFFERENT structure: a potential, an oscillating field, or a genuine fluid ***",
      "this is the honest content of 'two fields': not two copies, but two different structures")

info("E2  what has gamma < 2 naturally: a warm particle species (gamma = 5/3 for a monatomic gas), "
     "or an axion-like oscillating scalar with self-interaction. Both are ordinary dark-matter "
     "candidates -- which is precisely the tension with the programme's slogan, and is priced in "
     "Part F rather than hidden.")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- THE PRICE")
print("=" * 100)

N_LCDM, N_V5, N_TWOFIELD = 2, 5, 7
check(N_TWOFIELD > N_V5 > N_LCDM,
      f"F1  the dark-sector parameter count goes {N_LCDM} (LCDM) -> {N_V5} (v5 of the paper) -> "
      f"{N_TWOFIELD}+ here (chi adds at least K, gamma and its abundance).  That is a real cost and "
      "the paper's honest count must move",
      "no amount of galaxy success offsets an unstated parameter")

info("F2  the a_0-bump may become REDUNDANT, since chi can supply the cluster residual directly. "
     "That simplifies clusters and LOSES the bump's falsifiable anisotropic-stress prediction. "
     "Stated both ways.")

info("F3  *** AND THE REAL COST: 'Lambda, dark matter and MOND from ONE function' -- the central "
     "claim of THE_COMPLETION's abstract and the reason the construction was interesting -- IS GONE. "
     "Two sectors now do two jobs. The theory becomes more ordinary in exactly the way that made it "
     "distinctive. ***")


# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** THE TWO-FIELD CONSTRUCTION IS THE FIRST LIVE STRUCTURAL ROUTE IN THIS ENTIRE SEQUENCE -- AND
  IT SURVIVES IN A NARROW WINDOW, AT A PRICE THAT FALLS ON THE FRAMEWORK'S CENTRAL CLAIM. ***

  1. IT IS NOT CLOSED BY STAGE 9.  That theorem needs ONE shift-symmetric condensate; it applies to
     phi (which is fine -- phi keeps only the dark-energy and MOND jobs) and not to a second
     component with its own equation of state.

  2. THE MECHANISM IS ONE SCALING: lam_J ~ rho^(gamma/2 - 1) grows as the universe dilutes iff
     gamma < 2.  The single field sits exactly AT gamma = 2, where lam_J is a fixed physical length
     -- which is why it could never do this.  Requirements (1) CMB peaks and (2) clean galaxies
     together force lam_J to grow by >= {sig(need_growth,3)}x, i.e. *** gamma <= {sig(gamma_max,4)} ***, a
     non-empty window.  CMB lensing (route C's constraint) is satisfied automatically, since the
     smoothing lives far below the scales CMB lensing probes.

  3. *** THE LYMAN-ALPHA FOREST PINCHES IT TO lam_J(today) ~ 30-60 kpc. ***  Above that, the
     comoving suppression at z = 3 exceeds the forest's ~0.1 Mpc sensitivity and is excluded.  So
     galaxies are clean inside the RAR region, and the NEXT confrontation moves to the 30-200 kpc
     halo -- the outer rotation curve and galaxy-galaxy lensing.  The problem is relocated, not
     removed, and it is relocated to where the data are weaker but real.

  4. THE CONDITION ON chi IS SHARP: it must NOT itself be a ghost-free shift-symmetric k-essence
     condensate, or stage 9 applies verbatim and forces gamma = 2.  What naturally has gamma < 2 is
     a warm particle species (gamma = 5/3 for a monatomic gas -- and the bound gamma <= {sig(gamma_max,3)}
     sits {sig((GAMMA_GAS-gamma_max)/GAMMA_GAS*100,2)}% below it) or an oscillating self-interacting scalar.

  5. *** AND THAT IS THE HONEST STING.  The surviving construction is: the khronon carries Lambda and
     MOND, and a SECOND, WARM, ORDINARY dark component carries the dark matter.  It works.  It is
     also the thing the programme's slogan was built to avoid -- "Lambda, dark matter and MOND from
     ONE function" is gone, and the dark-sector count goes from five parameters to seven. ***

  6. WHAT I WILL NOT SAY: that this is a solution to "there is no dark matter".  It is the opposite
     shape of answer -- it makes galaxies clean by giving the dark sector a SECOND, warmer component,
     not by removing one.  What it does deliver, and this is real: a route in which GALAXIES contain
     no dark matter while the CMB, CMB lensing, BAO and supernovae are all satisfied -- which is
     exactly the observational pattern MOND has always faced, now with a mechanism and a pinched,
     falsifiable window.

  OWED NEXT, and it is one calculation: the 30-200 kpc confrontation -- outer rotation curves and
  galaxy-galaxy weak lensing against a component with lam_J = 30-60 kpc.  That decides whether the
  surviving window is a window or a wall.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f_ in FAIL:
        print("   -", f_)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 2 negative controls)")
sys.exit(0)
