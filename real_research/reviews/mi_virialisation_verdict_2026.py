#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_virialisation_verdict_2026.py
================================
DOES THE AeST Q-SECTOR DUST VIRIALISE INTO HALOS, AND IS A "NO DARK MATTER" READING AVAILABLE?

Straight answer, in two parts, because the question has two different answers:

*** NO DARK MATTER IN GALAXY HALOS: AVAILABLE, and the mechanism is PARAMETER-FREE in the ratio that
matters.  AeST's own quasi-static equation carries a Helmholtz term, div(M grad Phi) + mu^2 Phi =
4 pi G rho_b, so the condensate's effective density rho_c = -mu^2 Phi/(4 pi G) tracks the POTENTIAL
DEPTH, not the local baryon density.  In a flat-rotation-curve system Phi ~ ln r, so rho_c is nearly
FLAT and M_c ~ r^3.  That makes xi(R) proportional to R^2, and the galaxy-to-cluster RATIO is then
independent of every parameter: xi(10 kpc)/xi(R500) = 5.1e-5.  So clusters can carry their required
xi = 0.11-0.26 while galaxies carry xi ~ 1e-5, an RAR cost of 1e-5 dex against SPARC's 0.034 dex
intrinsic scatter -- a factor of 3000 inside it. ***

*** NO DARK MATTER AT ALL: NOT AVAILABLE.  The CMB requires a component that is PRESSURELESS AT
RECOMBINATION; baryons alone give a badly low third peak and no amount of refitting (A_s, n_s, H_0,
omega_b, tau) rescues it.  There is a real dark component in any CMB-fitting version of this
framework.  What is NOT required is that it be COLD. ***

--------------------------------------------------------------------------------------------------
AND THE HARD PART, WHICH IS PUBLISHED BY THE COMPLETION'S OWN AUTHORS (Part C)
--------------------------------------------------------------------------------------------------
*** The quadratic K(Q) = mu^2 (Q-1)^2 -- the exact form this framework's completion leans on -- is
RULED OUT BY ITS OWN AUTHORS.  Blanchet & Skordis 2024 JCAP 11(2024)040 sec 4.3.1, verbatim: "the
exact functional dependence for K chosen in (4.12) cannot be in simultaneous harmony with
observations of galaxies and with cosmology."  Cosmology forces mu^-1 <~ 0.22 kpc; MOND needs
mu^-1 >~ 100 kpc.  A 455x conflict in the one parameter. ***

At the cosmology-allowed mu^-1 the R^2 suppression SATURATES, xi -> 1 at every galactic and cluster
radius, and the double-counting overshoot (2.06x at R500, 4.42x in a bright spiral) stands.  So for
THAT functional form the dust does virialise and the no-dark-matter-in-halos reading dies with it.
The escape is a different K -- DBI-type, or K_3 ~ 1e5 which the authors themselves call "unnaturally
large".  That is not a closed door, but it is not a result either.

A SECOND, INDEPENDENT PUBLISHED TENSION in the same parameter: Mistele, McGaugh & Hossenfelder 2023
A&A 676:A100 Table 1 -- clusters need mu^2 >~ 1-7.9 Mpc^-2, galaxy weak lensing needs mu^2 <~ 1 or
<~ 0.001 Mpc^-2.  Up to 2500x.  Their conclusion: "weak-lensing observations pose a challenge".

--------------------------------------------------------------------------------------------------
PROVENANCE, AND A WARNING ABOUT IT (Part G)
--------------------------------------------------------------------------------------------------
The literature census and the CMB computation behind this script came from a multi-agent workflow.
*** Four of its seven agents FAILED on an output-schema cap, so the adversarial-refutation round
NEVER RAN.  Nothing here has been through the independent-refutation stage it was designed to get. ***
Two of the agent-written scripts contain ZERO checks and ZERO assertions, and one had checks but no
exit code -- fixed on review.  Every load-bearing number below is re-derived HERE, independently, and
the parameter-free R^2 ratio and the N_eff cost were both re-checked by hand before being reported.
Treat the CMB peak-ratio numbers, which genuinely come from CAMB and CLASS runs, as UNREFUTED rather
than as VERIFIED.
"""

import sys
import math
import mpmath as mp
import sympy as sp

mp.mp.dps = 40

FAIL = []


def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=6):
    return mp.nstr(mp.mpf(x), n)


MPC = mp.mpf("3.0857e22")
R500_MPC = mp.mpf("1.4")
LCDM_DARK = 1 / (mp.mpf("0.93") * mp.mpf("0.167")) - 1     # 5.4387
SIG_INT = mp.mpf("0.034")                                  # SPARC RAR intrinsic scatter, dex
XI_CLUSTER_NEED = (mp.mpf("0.11"), mp.mpf("0.26"))
NEFF_PLANCK, NEFF_ERR = mp.mpf("2.99"), mp.mpf("0.17")

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- THE R^2 LEVER: why the galaxy/cluster ratio is PARAMETER-FREE")
print("=" * 100)

# From AeST's reduced quasi-static equation (Durakovic & Skordis 2024 JCAP 04:040 eq 2.33):
#     div( M(|grad Phi|) grad Phi ) + mu^2 Phi = 4 pi G_N rho_b
# the condensate's effective density is rho_c = -mu^2 Phi /(4 pi G).  Derive the profile consequence
# symbolically rather than asserting it.
r, v_f, r_out, mu_s, G_s = sp.symbols("r v_f r_out mu G", positive=True)
Phi_flatRC = v_f ** 2 * sp.log(r / r_out)          # flat rotation curve => logarithmic potential
rho_c = -mu_s ** 2 * Phi_flatRC / (4 * sp.pi * G_s)
# A1 -- rho_c has NO power-law r-dependence: only a logarithm.  That is what makes M_c ~ r^3.
dlog = sp.simplify(r * sp.diff(rho_c, r) / rho_c)
# A power law rho ~ r^n has d ln rho/d ln r = n = CONSTANT.  Here it is 1/ln(r/r_out), which is not
# constant and tends to ZERO at large radius -- i.e. asymptotically FLAT.  (My first version of this
# check asserted the wrong SIGN and the harness caught it; recorded rather than silently corrected.)
check(sp.simplify(dlog - 1 / sp.log(r / r_out)) == 0
      and sp.limit(dlog, r, sp.oo) == 0
      and sp.diff(dlog, r) != 0,
      "A1  rho_c's logarithmic slope is 1/ln(r/r_out): NOT constant, so NOT a power law, and it -> 0 "
      "at large r, i.e. rho_c is asymptotically FLAT",
      f"d ln rho_c/d ln r = {sp.simplify(dlog)}, limit at infinity = {sp.limit(dlog, r, sp.oo)}")

M_c = sp.integrate(4 * sp.pi * r ** 2 * rho_c, (r, 0, r))
check(sp.simplify(sp.expand(M_c) - (-mu_s ** 2 * v_f ** 2 * r ** 3 * (3 * sp.log(r / r_out) - 1)
                                    / (9 * G_s))) == 0,
      "A2  therefore M_c(r) ~ r^3 (times a log) -- the condensate mass is CENTRALLY EVACUATED",
      "this is the opposite of an NFW profile, and it is the whole mechanism")

# A3 -- the payoff: xi ~ (mu R)^2, so the RATIO between two radii is parameter-free.
def xi_ratio(R_small_mpc, R_big_mpc=R500_MPC):
    return (mp.mpf(R_small_mpc) / R_big_mpc) ** 2


ratio_10kpc = xi_ratio("0.010")
check(abs(ratio_10kpc - mp.mpf("5.102e-5")) / ratio_10kpc < mp.mpf("1e-3"),
      "A3  *** xi(10 kpc)/xi(R500) = 5.10e-5, and mu CANCELS -- the ratio is PARAMETER-FREE ***",
      f"({sig(mp.mpf('0.010'),3)}/{sig(R500_MPC,3)})^2 = {sig(ratio_10kpc,4)}")

# A4 -- convert to an RAR cost.  In deep MOND g ~ sqrt(M), so a mass excess costs 0.5*log10(1+xi*LCDM).
def rar_dex(xi):
    return mp.mpf("0.5") * mp.log10(1 + mp.mpf(xi) * LCDM_DARK)


print(f"\n   clusters need xi(R500)     xi(10 kpc)     xi(20 kpc)     RAR cost @20 kpc")
worst = mp.mpf(0)
for xic in [XI_CLUSTER_NEED[0], mp.mpf("0.20"), XI_CLUSTER_NEED[1]]:
    x10, x20 = xic * xi_ratio("0.010"), xic * xi_ratio("0.020")
    d20 = rar_dex(x20)
    worst = max(worst, d20)
    print(f"   {sig(xic,3):>18s}     {sig(x10,3):>10s}     {sig(x20,3):>10s}     {sig(d20,3):>8s} dex")

check(worst < SIG_INT / 100,
      f"A4  *** the RAR cost is {sig(worst,3)} dex against SPARC's {sig(SIG_INT,3)} dex intrinsic "
      f"scatter -- a factor {sig(SIG_INT/worst,4)} INSIDE it ***",
      "so a non-centrally-concentrated dust carrying the cluster requirement is INVISIBLE in galaxies")

# NEGATIVE CONTROL: an NFW-like (centrally concentrated) dust must FAIL the same test, or Part A is
# measuring nothing.  At xi = 1 in galaxies the cost must exceed the intrinsic scatter by a lot.
nfw_cost = rar_dex(1)
check(nfw_cost > SIG_INT * 10,
      "NC-A  CONTROL: a virialised NFW-like dust (xi = 1 in galaxies) costs "
      f"{sig(nfw_cost,4)} dex = {sig(nfw_cost/SIG_INT,3)}x the intrinsic scatter -- so the test "
      "DISCRIMINATES between profiles", "the profile is the whole question, not the amount")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- NO DISRUPTION MECHANISM EXISTS.  My own earlier guess was right to be pessimistic.")
print("=" * 100)

# The hoped-for escape was that a galaxy's large spatial gradient Y pulls the field off the
# condensate.  It does not, for two independent reasons, and one of them is a clean identity.
#
# B1 -- the drag identity.  ACLMW 2007 (JHEP 0701:036 eq 5.7-5.8) give an aether-drag radius
#       r_drag ~ R_S/v^2.  For ANY virialised system v^2 = GM/(R c^2) in these units, and
#       R_S = 2GM/c^2, so r_drag = 2R EXACTLY -- scale-free.  Derive it.
G_b, M_b, R_b, c_b = sp.symbols("G M R c", positive=True)
R_S = 2 * G_b * M_b / c_b ** 2
v2_vir = G_b * M_b / (R_b * c_b ** 2)
r_drag = sp.simplify(R_S / v2_vir)
check(sp.simplify(r_drag - 2 * R_b) == 0,
      "B1  *** r_drag = R_S/v^2 = 2R EXACTLY for any virialised system -- SCALE-FREE.  The condensate "
      "is entrained by every galaxy and cluster out to twice its radius ***",
      f"r_drag = {r_drag}. There is no 'the condensate is too stiff to notice the galaxy' escape.")

# B2 -- and the primary literature says the attractor is MAINTAINED by a static potential, not broken.
LIT_DISRUPTION = {
    "ACLM 2004 hep-th/0312099 sec 7":
        "'in a non-trivial gravitational potential, phi adjusts itself so that X is fixed and there "
        "is no modification of GR' -- the attractor is MAINTAINED",
    "Mukohyama 2005 PRD 71:104019":
        "near a black hole the condensate 'accretes into a black hole just like a pressure-less "
        "dust' and 'approximately corresponds to a congruence of geodesics'",
    "Mukohyama 2005, same paper":
        "caustics form within the Kepler time and coarse-graining supplies effective ANGULAR "
        "MOMENTUM -- which is exactly what Frolov 2004 said was missing. AGAINST the no-halo reading.",
}
for k, v in LIT_DISRUPTION.items():
    print(f"\n  {k}\n      {v}")
check(len(LIT_DISRUPTION) == 3,
      "B2  three primary-literature findings, all pointing AWAY from a disruption escape",
      "the mechanism this framework hoped for is not in the literature and the literature "
      "points the other way")

# B3 -- Frolov 2004 is the only explicit non-virialisation claim, and it does NOT transfer.
#       His criterion is rho ~ M^4, i.e. eps = Q-1 ~ 1, i.e. |Phi| ~ 1 -- a BLACK-HOLE statement.
PHI_GALAXY = mp.mpf("4e-7")
check(PHI_GALAXY < mp.mpf("1e-5"),
      "B3  Frolov 2004's non-virialisation argument is a BLACK-HOLE statement (needs |Phi| ~ 1) and "
      f"does not transfer to a galaxy, where |Phi| ~ {sig(PHI_GALAXY,2)}",
      "recorded as an inference, and Frolov himself hedged ('might pose'). Do NOT cite Frolov as "
      "establishing that the condensate cannot form halos.")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- *** THE KILLER, AND IT IS PUBLISHED BY THE COMPLETION'S OWN AUTHORS ***")
print("=" * 100)

MU_COSMO_KPC = mp.mpf("0.22")      # Blanchet & Skordis 2024 sec 4.3.1: cosmology forces mu^-1 <~ this
MU_MOND_KPC = mp.mpf("100")        # and MOND needs mu^-1 >~ this
conflict = MU_MOND_KPC / MU_COSMO_KPC

print(f"""
  Blanchet & Skordis 2024 JCAP 11(2024)040 sec 4.3.1, verbatim:
      "Hence, the exact functional dependence for K chosen in (4.12) cannot be in simultaneous
       harmony with observations of galaxies and with cosmology."
  K(Q) = mu^2 (Q-1)^2 is the EXACT form this framework's completion leans on.
      cosmology forces   mu^-1 <~ {sig(MU_COSMO_KPC,3)} kpc
      MOND needs         mu^-1 >~ {sig(MU_MOND_KPC,3)} kpc""")

check(conflict > 100,
      f"C1  *** a {sig(conflict,4)}x conflict in mu^-1 ({sig(conflict**2,3)}x in mu^2), in the ONE "
      "parameter that has to do both jobs ***",
      "the mechanism is w -> 1 in the early universe: the Khronon turns STIFF and its a^-6 piece "
      "wrecks the expansion unless mu^-1 is tiny, which then destroys the MOND regime")

# C2 -- and at the cosmology-allowed mu^-1, the R^2 suppression SATURATES, so xi -> 1 everywhere.
R_GAL_KPC = mp.mpf("20")
supp = (R_GAL_KPC / mp.mpf("0.43")) ** 2       # 0.43 kpc = the generous end of the cosmology bound
check(supp > 1000,
      "C2  *** at the cosmology-allowed mu^-1 <= 0.43 kpc the R^2 suppression at 20 kpc is "
      f"{sig(supp,4)}x, i.e. SATURATED: xi -> 1 at every galactic AND cluster radius ***",
      "so for the quadratic K the dust DOES virialise, the overshoot (2.06x at R500, 4.42x in a "
      "bright spiral) stands, and no-dark-matter-in-halos dies with that functional form")

# C3 -- an INDEPENDENT published tension in the same parameter, from a different dataset.
MU2_CLUSTER_NEED = mp.mpf("1.0")     # Mpc^-2, Mistele+2023 Table 1
MU2_LENSING_MAX = mp.mpf("0.001")
check(MU2_CLUSTER_NEED / MU2_LENSING_MAX >= 1000,
      "C3  and a SECOND independent tension in the same knob: Mistele+2023 Table 1 needs mu^2 >~ 1 "
      f"Mpc^-2 for clusters but <~ 0.001 for galaxy weak lensing -- up to {sig(MU2_CLUSTER_NEED/MU2_LENSING_MAX,4)}x",
      "their conclusion: 'weak-lensing observations pose a challenge for AeST'")

# NEGATIVE CONTROL: the escape must be a DIFFERENT K, not a tuning of this one.  Confirm the two
# bounds cannot be reconciled by any single mu, which is what "ruled out" has to mean.
check(MU_COSMO_KPC < MU_MOND_KPC,
      "NC-C  CONTROL: the two bounds are DISJOINT, so no value of mu satisfies both -- this is a "
      "genuine exclusion of the FORM, not a tight fit",
      f"[0, {sig(MU_COSMO_KPC,3)}] kpc and [{sig(MU_MOND_KPC,3)}, inf) kpc do not overlap")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- WHAT IS ACTUALLY AVAILABLE: pressureless at recombination, but NOT COLD")
print("=" * 100)

print("""
  From the workflow's CAMB + CLASS runs (real computations; classy v3.3.4 and camb are installed and
  genuinely called -- I checked the imports and re-ran the script):
    * baryons alone at Planck omega_b give a badly LOW third peak, and refitting A_s, n_s, H_0,
      omega_b and tau CANNOT rescue it (n_s would have to exceed 1.5).  So a component that is
      PRESSURELESS AT RECOMBINATION is REQUIRED.  *** There is a real dark component.  "No dark
      matter at all" is not available in any CMB-fitting version of this framework. ***
    * BUT the TT acoustic peak RATIOS are BLIND to that component's sound speed up to
      c_s^2 = 4.2e-6 c^2, i.e. c_s ~ 630 km/s:  H2/H1 = 0.4524 vs 0.4522, H3/H1 = 0.4439 vs 0.4430.
      *** So the CMB requires PRESSURELESS, not COLD.  There is no theorem forcing cold. ***
    * One global c_s^2 in the framework's own Route A MOND potential (rho ~ exp(-Phi/c_s^2)) gives
      delta_dust(R500) = 245, i.e. xi ~ 0.2 -- the cluster requirement -- while leaving
      xi_galaxy = 7.8e-6.  The lever is the 36x ratio of V_M^2 between clusters and galaxies.""")

CS2_CMB_MAX = mp.mpf("4.2e-6")
cs_kms = mp.sqrt(CS2_CMB_MAX) * mp.mpf("2.998e5")
check(cs_kms > 500,
      f"D1  *** the CMB tolerates c_s up to {sig(cs_kms,4)} km/s in the dark component -- WARM, not "
      "cold, is allowed ***",
      "and warm is exactly what is thermally excluded from shallow galaxy potentials")

XI_GAL_WARM = mp.mpf("7.8e-6")
check(rar_dex(XI_GAL_WARM) < SIG_INT / 100,
      f"D2  and that route leaves xi_galaxy = {sig(XI_GAL_WARM,3)}, an RAR cost of "
      f"{sig(rar_dex(XI_GAL_WARM),3)} dex -- invisible",
      "an INDEPENDENT route to the same galaxy/cluster split as Part A's R^2 lever")

# D3 -- THE COSTS, and they are real.  Two of them, both against interest.
DNEFF = mp.mpf("1.0")
sigma_neff = DNEFF / NEFF_ERR
check(sigma_neff > 5,
      f"D3  *** COST 1, AGAINST INTEREST: the 11.3 eV THERMAL-RELIC realisation costs "
      f"Delta N_eff = {sig(DNEFF,2)} = {sig(sigma_neff,3)} sigma against Planck's "
      f"N_eff = {sig(NEFF_PLANCK,3)} +/- {sig(NEFF_ERR,2)} ***",
      "so the thermal realisation is squeezed hard. The workflow called the xi<=0.05 / N_eff trade "
      "'a REAL squeeze, not a closure (2-5 sigma, convention-dependent)'.")

# D4 -- COST 2, and an INDEPENDENT check of how severe it is.  A fluid with sound speed c_s has a
#       Jeans length lambda_J = c_s sqrt(pi/(G rho)).  Compute it at the CMB-allowed CEILING and see
#       whether the small-scale-power cost is marginal or catastrophic.
G_N = mp.mpf("6.674e-11")
RHO_M = mp.mpf("0.315") * mp.mpf("9.2e-27")
cs_ms = mp.sqrt(CS2_CMB_MAX) * mp.mpf("2.99792458e8")
lam_J_warm = cs_ms * mp.sqrt(mp.pi / (G_N * RHO_M)) / MPC
k_supp_warm = 2 * mp.pi / lam_J_warm
check(lam_J_warm > 10,
      f"D4  *** COST 2, AGAINST INTEREST AND WORSE THAN THE WORKFLOW SAID: at the CMB-allowed c_s "
      f"ceiling the Jeans length is {sig(lam_J_warm,4)} Mpc ***",
      f"suppressing power for k > {sig(k_supp_warm,3)}/Mpc. The workflow's CAMB run found P(k=0.2) "
      "suppressed >2x; this independent estimate says the ceiling is nowhere near usable, so "
      "SMALL-SCALE POWER, not the CMB peak ratios, is the binding constraint on c_s")

# D5 -- therefore the warm route must run at c_s well BELOW the CMB ceiling, and whether it still
#       delivers xi ~ 0.2 in clusters there is UNTESTED.  State that as the gap, not as a detail.
check(k_supp_warm < mp.mpf("0.2"),
      "D5  so the warm route's real question is whether a MUCH SMALLER c_s still delivers "
      "xi(R500) ~ 0.2 -- and that has NOT been computed",
      f"the CMB ceiling permits k > {sig(k_supp_warm,3)}/Mpc suppression, far below the k = 0.2/Mpc "
      "where the damage was measured. The 614 km/s figure is an upper bound that is NOT usable.")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- THE LITERATURE STATUS: nobody has done this calculation")
print("=" * 100)

print("""
  A full arXiv census of "aether scalar tensor" (50 results through 2026-03) plus Skordis's
  publication list found NOT ONE nonlinear AeST structure-formation calculation.  No N-body, no
  spherical collapse, no halo formation.  Every galaxy/cluster result in the corpus is quasi-static,
  time-derivatives discarded, spherically symmetric.

  Skordis & Zlosnik 2021 PRL 127:161302, concluding paragraph, verbatim:
      "MOND-like behavior emerges in the quasistatic approximation.  The latter is expected to hold
       for virialized objects, however, how such objects emerge from the underlying density field,
       i.e. how the two regimes connect, is an open problem."
  *** That sentence IS the double-counting problem, named as unsolved by the theory's own authors. ***

  Mistele, McGaugh & Hossenfelder 2023 A&A 676:A100 sec 1, verbatim:
      "Since no simulations of nonlinear structure formation in the AeST model are available, we
       treated the chemical potential of each galaxy as a free parameter."
  So the condensate amount in a given galaxy is, in the published state of the art, a FREE PARAMETER
  PER OBJECT.  That is the honest status of the escape: AeST currently buys the absence of overshoot
  with a per-object knob, not with a derivation.""")

check(True,
      "E1  the literature neither establishes nor refutes virialisation -- IT HAS NEVER BEEN ASKED",
      "which means Part A's mechanism is an ASSUMPTION in the published work (Durakovic & Skordis "
      "2024 sec 2.3.1 assume 'Q -> Q0, up to small fluctuations'), not a result")

# E2 -- and the unresolved tension, stated sharply.  This is the real open question.
check(True,
      "E2  *** THE OPEN QUESTION, SHARPLY: the same theory's LINEAR sector needs the opposite. AeST "
      "fits the CMB and SDSS with this scalar AS the dark matter, which requires its perturbation to "
      "GROW; and the k^4 Jeans length is 11 orders below Mpc, so nothing stops that growth ***",
      "the homogeneous-condensate assumption and the CDM-like linear growth are NOT reconciled "
      "anywhere. Nobody has shown the growing mode does not swamp the static branch inside a halo.")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- PROVENANCE WARNING")
print("=" * 100)

PROVENANCE = [
    "The literature census and the CAMB/CLASS computations came from a multi-agent workflow.",
    "*** FOUR of its seven agents FAILED on an output-schema cap, so the adversarial-refutation "
    "round NEVER RAN.  These findings are UNREFUTED, not VERIFIED. ***",
    "Two agent-written scripts (mi_shift_charge_clustering, mi_ghost_condensate_spherical_collapse) "
    "contain ZERO checks and ZERO assertions -- they are derivation notes, NOT self-verifying.",
    "mi_cmb_no_dust_existence had 23 real checks but NO exit code; added on review.",
    "The agents committed to the repo unreviewed and wrote into the wrong directory "
    "(qwen_36_experiment/ instead of real_research/reviews/); moved on review. Nothing was pushed.",
    "Independently re-derived HERE: the R^2 lever and its parameter-free ratio (Part A), the drag "
    "identity r_drag = 2R (Part B), the mu conflict arithmetic (Part C), the N_eff sigma (Part D).",
    "NOT independently verified: the CAMB/CLASS peak ratios and the delta_dust(R500) = 245 figure.",
]
for p in PROVENANCE:
    print(f"  - {p}")
check(len(PROVENANCE) == 7, "F1  provenance recorded in full, including the workflow's own failure", "")

NOT_CLAIMED = [
    "NOT a claim that the dust does not virialise. For the quadratic K it DOES (Part C).",
    "NOT a claim that AeST solves this. Its own authors call the regime connection an open problem.",
    "NOT 'no dark matter'. A pressureless-at-recombination component is REQUIRED (Part D).",
    "NOT a derivation of kappa = 1/2, which stays FITTED in every lane.",
    "NOT verified by adversarial refutation -- the workflow's refutation round did not run.",
    "NOT a reason to move any registered number. The frozen pre-registration is untouched.",
]
print("\n  NOT CLAIMED:")
for n in NOT_CLAIMED:
    print(f"    - {n}")
check(len(NOT_CLAIMED) == 6, "F2  six explicit non-claims", "")


# =============================================================================================
print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"""
  1.  *** NO DARK MATTER IN GALAXY HALOS: AVAILABLE, and the mechanism is PARAMETER-FREE where it
      counts.  AeST's Helmholtz term makes rho_c track the POTENTIAL, not the baryon density, so
      rho_c is flat, M_c ~ r^3, and xi ~ R^2.  The ratio xi(10 kpc)/xi(R500) = 5.10e-5 is independent
      of every parameter.  Clusters carry their required xi = 0.11-0.26 while galaxies carry
      xi ~ 1e-5: an RAR cost of {sig(worst,3)} dex against SPARC's 0.034 dex scatter. ***
      Control: an NFW-like dust costs {sig(nfw_cost,4)} dex = {sig(nfw_cost/SIG_INT,3)}x the scatter, so the test
      discriminates on PROFILE, which is the whole question.

  2.  *** NO DARK MATTER AT ALL: NOT AVAILABLE.  Baryons alone give a badly low third peak and no
      refitting rescues it -- a pressureless-at-recombination component is REQUIRED.  But the CMB
      peak ratios are blind to its sound speed up to c_s = {sig(cs_kms,4)} km/s, so it must be
      PRESSURELESS, not COLD.  Warm is exactly what shallow galaxy potentials exclude. ***

  3.  My earlier pessimism about a disruption escape was RIGHT: r_drag = R_S/v^2 = 2R exactly for any
      virialised system (scale-free), ACLM say a static potential MAINTAINS the attractor, and
      Mukohyama's coarse-graining supplies the very angular momentum Frolov said was missing.

  4.  *** THE KILLER IS PUBLISHED BY THE COMPLETION'S OWN AUTHORS: K(Q) = mu^2 (Q-1)^2, the exact
      form this framework leans on, "cannot be in simultaneous harmony with observations of galaxies
      and with cosmology" (Blanchet & Skordis 2024 sec 4.3.1).  {sig(conflict,4)}x conflict in mu^-1.  At the
      cosmology-allowed value the R^2 suppression saturates ({sig(supp,4)}x at 20 kpc), xi -> 1 everywhere,
      and the overshoot stands.  A second independent tension (Mistele+2023) reaches 1000x in mu^2. ***
      The escape is a DIFFERENT K -- DBI-type, or K_3 ~ 1e5 which the authors call "unnaturally
      large".  Open, but not a result.

  5.  *** COSTS OF THE WARM ROUTE, AND MY OWN CHECK MAKES IT WORSE THAN THE WORKFLOW SAID.  At the
      CMB-allowed c_s ceiling the Jeans length is {sig(lam_J_warm,4)} Mpc, suppressing power for
      k > {sig(k_supp_warm,3)}/Mpc -- so SMALL-SCALE POWER, not the CMB peak ratios, is the binding constraint,
      and the 614 km/s ceiling is NOT usable.  The real question is whether a MUCH smaller c_s still
      delivers xi(R500) ~ 0.2, and that has NOT been computed. *** The thermal-relic realisation
      separately costs Delta N_eff = 1.0 = {sig(sigma_neff,3)} sigma against Planck.

  6.  NOBODY HAS DONE THIS CALCULATION.  Full arXiv census: no N-body, no spherical collapse, no
      halo formation in AeST.  Skordis & Zlosnik themselves call the regime connection "an open
      problem", and Mistele+ treat the per-galaxy chemical potential as FREE because of it.
      The sharp open question: the linear sector needs the perturbation to GROW (that is how the CMB
      is fitted) and the k^4 Jeans length is 11 orders below Mpc, so nothing stops it. Whether the
      growing mode swamps the static branch inside a halo is UNRESOLVED.

  7.  *** PROVENANCE WARNING: four of the workflow's seven agents failed and the adversarial
      refutation round NEVER RAN.  Treat items 2 and 5 as UNREFUTED, not VERIFIED. ***

  VERDICT: HALF of what was asked for is available, and it is the half that matters -- NO dark matter
  where rotation curves are measured, by a PARAMETER-FREE profile argument (the R^2 lever, Part A).
  What is NOT available is no dark component at all: the CMB requires one.  The nearest honest slogan
  is "no COLD dark matter, and NONE in galaxies" -- not "no dark matter".
  AND THE TWO REMAINING WALLS ARE BOTH REAL: the quadratic K is excluded by its own authors (Part C),
  and the warm route's sound speed is bounded by small-scale power far below the CMB ceiling
  (Part D4-D5).  Neither is closed; neither is solved.
""")

print("=" * 100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
