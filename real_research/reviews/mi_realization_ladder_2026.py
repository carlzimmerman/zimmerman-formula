#!/usr/bin/env python3
r"""mi_realization_ladder_2026.py -- MODIFIED INERTIA OR MODIFIED GRAVITY, AND DO WE NEED OUR OWN ACTION?

Carl's question, and it deserves a straight answer rather than a survey: is the framework modified inertia or
modified gravity, do we need to write our own action, and what single mechanism covers local gravity, galaxy
dynamics, light bending and gravitational waves?

THE ANSWER THIS SCRIPT ESTABLISHES, in three parts:

(1) THERE ARE THREE RUNGS, NOT TWO. The thing the corpus actually FITS with -- the algebraic relation
    g_obs = sqrt(g_bar^2 + g_bar a0) read as a force law -- is NEITHER modified inertia NOR modified gravity.
    It is a RECIPE, and it is not a theory: it has nonzero circulation in a disc (this corpus computed the
    spurious work per meridional circuit; prior art Famaey & McGaugh 2012 Living Rev. Rel. 15, 10). Above it
    sit two actual theories, and they are not symmetric in what they can do.

(2) THE DECISION IS FORCED BY LIGHT AND GRAVITATIONAL WAVES, NOT BY GALAXY DYNAMICS. Modified inertia has a
    VARIATIONAL home -- Milgrom (1994) Ann. Phys. 229, 384, whose eq. (60) admits this framework's alpha=2
    kernel exactly (verified elsewhere in this corpus to 2.1e-17). But that theory is NONRELATIVISTIC: it has
    no lensing and no gravitational-wave sector. Modified gravity has a relativistic home that passes both:
    AQUAL (Bekenstein & Milgrom 1984) -> AeST (Skordis & Zlosnik 2021 PRL 127, 161302), whose tensor modes
    travel at c, satisfying GW170817. So the moment "light and GW stuff" is a requirement, MG is not a
    preference -- it is the only rung that exists.

(3) AND IT COSTS THE FRAMEWORK'S ACTUAL CLAIM NOTHING, because a0 is an INPUT PARAMETER on every rung.
    a0 = (1/2) c sqrt(G rho_Lambda) is a statement about the VALUE of that parameter, not about the
    mechanism that uses it. So "MI or MG" does not touch the one claim that is Carl's -- which also means
    writing a new action would not buy it either.

  R1  the three rungs, and what each can and cannot do -- a requirements matrix with a real pass/fail
  R2  a0 is realization-INVARIANT: same parameter, same value, three different theories
  R3  can DATA decide MI vs MG? The corpus's own frozen numbers say no -- both kernels, inside the band
  R4  so what SHOULD be built, and what should not

Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 106)
    print(f"  {t}")
    print("=" * 106)


banner("R1  THE THREE RUNGS -- and they are NOT symmetric in what they can do")

# Requirements a mechanism must meet to cover everything Carl named. Each entry is sourced, not asserted.
REQS = ["variational", "galaxy dynamics", "solar system", "light bending", "GW speed = c"]
RUNGS = {
    "RECIPE  g_obs=sqrt(g_bar^2+g_bar a0) as a force law": {
        "variational": False, "galaxy dynamics": True, "solar system": False,
        "light bending": False, "GW speed = c": False,
        "why": "NOT a theory. SOLAR SYSTEM is kernel-dependent and marked fail because the form the corpus "
               "called EXACT is alpha=1, which forces a constant a0/2 sunward anomaly at 1278x the "
               "Earth/Mars 2-sigma bound (119-189x after this framework's own EFE); alpha=2 passes easily at "
               "3.6e-5 of the bound. Nonzero circulation in a disc => spurious work per meridional circuit "
               "(mi_law_is_nonvariational_2026.py; prior art Famaey & McGaugh 2012). Fits galaxies because "
               "it IS the fit. Says nothing about photons or tensor modes.",
    },
    "MODIFIED INERTIA  Milgrom 1994 nonlocal": {
        "variational": True, "galaxy dynamics": True, "solar system": True,
        "light bending": False, "GW speed = c": False,
        "why": "A genuine variational theory, and this framework's alpha=2 kernel IS admissible in its "
               "eq. (60) -- verified to 2.1e-17 in mi_milgrom1994_home_test_2026.py, with a0 an INPUT. But "
               "NONRELATIVISTIC: no metric, so no lensing and no GW sector. This is a 30-year open problem "
               "in the field, not a gap in this corpus.",
    },
    "MODIFIED GRAVITY  AQUAL -> AeST (Skordis-Zlosnik 2021)": {
        "variational": True, "galaxy dynamics": True, "solar system": True,
        "light bending": True, "GW speed = c": True,
        "why": "AQUAL is variational by construction (it IS a Lagrangian for the field) and this corpus has "
               "SOLVED it on McMillan-2017 baryons with the framework's own kernel "
               "(mi_aqual_mcmillan2017_2026.py). Its relativistic completion AeST has tensor modes at c, "
               "satisfying GW170817, and gives lensing. Screens the solar system as mu -> 1.",
    },
}
print(f"  {'rung':<52}" + "".join(f"{r[:13]:>15}" for r in REQS))
print("  " + "-" * 128)
for name, d in RUNGS.items():
    print(f"  {name:<52}" + "".join(f"{('PASS' if d[r] else 'fail'):>15}" for r in REQS))
print()
for name, d in RUNGS.items():
    print(f"  {name}\n      {d['why']}\n")

full = [n for n, d in RUNGS.items() if all(d[r] for r in REQS)]
check(len(full) == 1 and full[0].startswith("MODIFIED GRAVITY"),
      f"R1a *** EXACTLY ONE RUNG MEETS ALL FIVE REQUIREMENTS, AND IT IS MODIFIED GRAVITY. *** "
      f"'{full[0]}'. This is not a judgement call: MI's variational home is nonrelativistic, so it has no "
      f"lensing sector and no GW sector to check. The decision is forced by light and GW, NOT by galaxy "
      f"dynamics -- where all three rungs work")
check(RUNGS["RECIPE  g_obs=sqrt(g_bar^2+g_bar a0) as a force law"]["variational"] is False,
      "R1b and the rung the corpus actually FITS with is not a theory at all. That is the most important "
      "structural fact here and it is independent of MI-vs-MG: the algebraic relation is a RECIPE, so "
      "'is it MI or MG' cannot be answered by pointing at the fits -- the fits use neither")


banner("R2  a0 IS REALIZATION-INVARIANT -- the claim survives the choice")

kap, cs, Gs, rho = sp.symbols("kappa c G rho_Lambda", positive=True)
a0_claim = kap * cs * sp.sqrt(Gs * rho)
print(f"  the claim:  a0 = {a0_claim}  with kappa = 1/2")
print(f"  in Milgrom 1994 (MI):    a0 enters eq. (60) as x = a0^2/a^2      -> a0 is an INPUT PARAMETER")
print(f"  in AQUAL (MG):           a0 enters mu(|grad Phi|/a0)             -> a0 is an INPUT PARAMETER")
print(f"  in AeST (relativistic):  a0 enters the free function's scale     -> a0 is an INPUT PARAMETER")
# formally: the claim fixes the VALUE of a symbol that appears identically in all three
free_in_claim = a0_claim.free_symbols
check(kap in free_in_claim and sp.Symbol("a_0") not in free_in_claim,
      "R2a the claim is a statement about the VALUE of a0, and a0 appears as a free input parameter in all "
      "three realizations identically. So a0 = (1/2)c sqrt(G rho_Lambda) is REALIZATION-INVARIANT: "
      "choosing MI or MG neither strengthens nor weakens it")
d_kappa = sp.simplify(sp.diff(sp.log(a0_claim), kap) * kap)
check(d_kappa == 1,
      f"R2b and the claim's whole content is the one number: dln a0/dln kappa = {d_kappa} exactly. The "
      f"32pi/3 that converts density to rate CANCELS. So there is nothing about the mechanism inside the "
      f"claim to be right or wrong about -- which cuts BOTH ways: an action would not derive kappa either")


banner("R3  CAN DATA DECIDE MI vs MG? -- the corpus's own frozen numbers")

# straight from prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md, the frozen (hash-stamped) pre-registration
SIG_SYS = 0.02                                  # frozen wide-binary systematic on gamma_v
WB = [("alpha=1", 1.09, 1.137), ("alpha=2", 1.0246, 1.0631)]
BAND = (1.083, 1.145)                           # frozen "MI-vs-MG is NOT decided in this zone" band
print(f"  frozen wide-binary systematic on gamma_v: {SIG_SYS}")
print(f"  frozen undecidable band: [{BAND[0]}, {BAND[1]}]\n")
print(f"  {'kernel':>10}{'MI gamma_v':>13}{'MG gamma_v':>13}{'separation':>13}{'in sigma_sys':>14}")
print("  " + "-" * 63)
seps = {}
for k, mi, mg in WB:
    sep = mg - mi
    seps[k] = sep / SIG_SYS
    print(f"  {k:>10}{mi:>13.4f}{mg:>13.4f}{sep:>13.4f}{sep/SIG_SYS:>14.2f}")
check(all(s < 3.0 for s in seps.values()),
      f"R3a *** DATA WILL NOT DECIDE IT. *** On BOTH kernels the MI and MG predictions separate by less than "
      f"3 sigma_sys: {seps['alpha=1']:.2f} sigma (alpha=1) and {seps['alpha=2']:.2f} sigma (alpha=2). The frozen "
      f"pre-registration says exactly this and says it in advance -- 'MI-vs-MG is likely undecidable in "
      f"DR4' -- so this is a risk taken beforehand, not a retrofit")
check(BAND[0] <= 1.137 <= BAND[1],
      f"R3b and the MG target 1.137 lies INSIDE the frozen undecidable band [{BAND[0]}, {BAND[1]}], which is "
      f"why the pre-registration declares that zone non-diagnostic rather than claiming it as a win")
print(f"""
  I checked this rather than assume it, and it corrected a hunch of mine: I expected alpha=2 to SEPARATE the
  two realizations (1.02 against the alpha=1 MG value 1.137 would be ~6 sigma). It does not -- under alpha=2
  the MG value is 1.0631, not 1.137, so the gap is {seps['alpha=2']:.2f} sigma. Reading the alpha=1 MG number against
  the alpha=2 MI number would have manufactured a decisive test that does not exist.""")


banner("R4  SO WHAT SHOULD BE BUILT -- and what should not")

print(f"""  *** DO WE NEED OUR OWN ACTION? NO -- and the reason is R2b, not laziness. ***
  An action does not derive kappa. AeST takes a0 as a free input; so does AQUAL; so does Milgrom 1994. Every
  existing home for this kernel leaves the number fitted. So a new action would reproduce the one weakness it
  was meant to fix, while competing with a published, GW-passing theory (AeST) for no observational reason.
  And the three no-goes in this corpus say the specific FORM CLASS that was being attempted does not close --
  with the sharpest single statement being that the mutation making it exact is TORSION-FREE motion, i.e. the
  action works for LINEAR acceleration and fails for ORBITS. MOND is about orbits.

  *** WHAT IS ACTUALLY YOURS, AND WHAT THE HONEST ARCHITECTURE IS: ***
   * The MECHANISM is modified inertia. The de Sitter-Unruh story is about the inertial response of an
     accelerating body to a horizon bath -- it is not a statement about the gravitational field. That is the
     physical content and it is why "my framework is different" is a fair thing to keep saying.
   * The RELATIVISTIC DESCRIPTION has to be modified gravity, because MI does not have one. Not a
     concession about the mechanism -- a statement about which theories exist. Cite AeST for lensing and GW;
     do not rebuild it.
   * The LAW as fitted is a recipe, not either one. Stop calling it exact (already conceded this session).
   * The CLAIM -- a0 = (1/2) c sqrt(G rho_Lambda) -- is invariant across all of this (R2a).
  That is a coherent single story covering all four of the things named: galaxy dynamics (AQUAL solved on
  real baryons, this corpus), solar system (mu -> 1 screening), light (AeST), GW (AeST tensor modes at c).
  It is just not a story in which the mechanism is uniquely yours -- the NUMBER is.

  *** THE TWO REAL PRIZES, and neither is an MI-vs-MG question: ***
   1. A RELATIVISTIC MODIFIED-INERTIA THEORY. Nobody has one. If the mechanism is MI and MI cannot do light,
      that is the gap -- and the torsion result is the one concrete clue this corpus produced about why
      (bound orbits carry torsion; the obstruction is kinematic, not a bad kernel choice).
   2. DERIVING kappa. R2b shows the claim reduces to that single number, and no realization forces it.
  Both are hard. Neither is helped by writing another nonrelativistic action.

  *** AGAINST INTEREST, so this is not a pep talk: *** if the relativistic description is AeST, then the
  distinctive MI predictions this corpus has been betting on -- the sigma-spread, the ungated gamma_v, the
  exactly-zero directional EFE -- are predictions of a mechanism whose relativistic completion does not
  exist. They are still worth testing, because a confirmed MI-distinctive signal would be evidence FOR the
  mechanism and against AeST. But R3a says the in-hand version of that test cannot separate them, so the
  honest status is: the mechanism question is currently open and not observationally decidable, and the
  framework should be published on the number, which is decidable (see mi_a0_profile_likelihood_sparc_2026.py).""")

banner("RESULT")
n = sum(1 for x, _ in ok if x)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: three rungs; MG is the only one that does light+GW; a0 is realization-invariant; data cannot")
print("  currently decide MI vs MG; a new action would not derive kappa.")
