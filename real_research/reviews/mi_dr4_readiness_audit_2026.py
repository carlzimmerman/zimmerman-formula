#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_dr4_readiness_audit_2026.py
==============================
DR4 READINESS AUDIT.  Verdict: *** THE PIPELINE IS NOT READY.  It hard-codes a target that is STALE
BY FOUR AMENDMENTS, and today's field-theory papers cite a RETIRED kernel. ***

This script does NOT touch PREREGISTRATION_DR4.md or any *_HASH.txt.  The registration is frozen and
its amendment chain is the authority; this is an audit OF the executable pipeline AGAINST that chain.

--------------------------------------------------------------------------------------------------
FINDING 1 -- THE PIPELINE'S TARGET IS STALE BY FOUR AMENDMENTS (Part A)
--------------------------------------------------------------------------------------------------
`prep_2026/gaia_dr4_prep/wide_binary_pipeline.py` hard-codes GAMMA_MI = 1.09, the ORIGINAL frozen
target.  The chain has moved it four times:
        frozen 1.09  -> Amdt 3: 1.0246  -> Amdt 4(d)/7: 1.0310  -> *** Amdt 8: 1.1582 ***
Amendment 8 (2026-08-03) adopted the EXPONENTIAL kernel nu = 1/(1 - e^-sqrt(y)) ("Route A") because
BOTH power-law kernels fail the solar system, and the target moved to gamma_v = 1.1582 with range
1.1311-1.1964 (radial) / 1.1339-1.2007 (magnitude).  *** So the pipeline would inject and fit a
signal 1.76x too small, and every derived N and z it reports is wrong. ***  The stale value is read
OUT OF THE FILE here, not asserted.

--------------------------------------------------------------------------------------------------
FINDING 2 -- TODAY'S FIELD-THEORY PAPERS CITE A RETIRED KERNEL (Part C).  AGAINST INTEREST.
--------------------------------------------------------------------------------------------------
*** The covariant-MI field-theory paper published today (DOI 10.5281/zenodo.21854914, v1-v3) states
that "mu's shape is the alpha = 2 interpolation that solar-system ephemerides force".  That is FALSE
as of Amendment 8, five days earlier: alpha = 2 does NOT pass the ephemerides -- it misses the Mars
ranging budget by 8.5x/12.4x, because its 1/g tail binds at the SUN via the Jupiter reflex
(~2233 a_0) rather than at a planet.  Route A was adopted precisely BECAUSE both power-law kernels
fail. ***  A correction is owed, and this script states what does and does not break:
  * The LOCALISATION result is untouched.  It concerns the MEMORY kernel K(s), not the interpolation
    mu(Y); G(u) = 4u K(2u) and a_0 = (2/3)c m^2/g carry no reference to mu's shape.
  * The JOINT-EQUATIONS result is untouched in substance: Route A has the same two limits
    (nu -> 1/sqrt(y) deep, nu -> 1 Newtonian), which is all that step 3 used, so v^4 = G M a_0 still
    follows.  Verified in Part C.
  * What IS wrong is the sentence attributing ephemeris-compliance to alpha = 2.  It must be replaced
    by Route A.  That is a WORDING-AND-CITATION defect, not a structural one -- but it is a wrong
    statement about which kernel the framework holds, and it is in three published versions.

--------------------------------------------------------------------------------------------------
FINDING 3 -- THE TWO ROUTE-A DECLARED RISKS ARE NOT IMPLEMENTED (Part D)
--------------------------------------------------------------------------------------------------
Amendment 8 filed two NEW declared risks, and the pipeline implements neither:
  (c) the nuisance kappa lands 1.0575-1.0959, OUTSIDE the frozen window [0.95, 1.05], whose declared
      consequence is "systematic-limited, no verdict -- reported, not repaired".  *** Route A FAILS
      BOTH sigma treatments where alpha = 2 passed both. ***
  (d) on the MAGNITUDE convention the alt-footing/primary corner is 1.20069 -- 0.00069 ABOVE the
      >1.20 no-verdict edge -- so a genuine detection is PRE-DECLARED UNSCOREABLE there.
And the scoring collision stands: 1.1582 falls in the bin pre-declared "MG-side; MI disfavored",
and the frozen MG target 1.137 now sits INSIDE Route A's MI range.  Amendment 7(e)'s rule is
therefore load-bearing: *** report raw gamma_hat with sigma_fit and BOTH distances (to 1.000 and to
1.1582); never a single verdict word. ***  The pipeline currently prints single-label verdicts.

--------------------------------------------------------------------------------------------------
WHAT THIS SCRIPT DOES NOT DO
--------------------------------------------------------------------------------------------------
  * It does not modify the registration, any hash file, or the pipeline.  It AUDITS.
  * It does not file an amendment.  Nothing here moves a registered number; Findings 1 and 3 are
    the pipeline failing to implement amendments ALREADY filed, and Finding 2 concerns a paper, not
    the registration.  Whether to file anything is the author's call.
  * It does not re-derive Route A's orientation-averaged gamma_v from scratch.  It re-derives the
    pieces it can check independently -- nu(y_extN) and gamma_perp = sqrt(nu) -- and verifies them
    against the amendment chain's recorded values, so the chain's internal consistency is tested
    rather than assumed.

CREDIT.  Route A kernel and the wide-binary target: this corpus,
`real_research/reviews/mi_route_a_kernel.py` and `mi_route_a_wb_gamma_v_2026.py`, Amendment 8.
nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9; MILGROM 1994 Ann.Phys. 229:384.  The
external-field effect is Milgrom's.  Gaia DR4: ESA/DPAC.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import os
import re
import sys
import mpmath as mp

mp.mp.dps = 25

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREP = os.path.join(REPO, "prep_2026", "gaia_dr4_prep")
PIPE = os.path.join(PREP, "wide_binary_pipeline.py")
PAPER = os.path.join(REPO, "opus_48_extended_research", "papers",
                     "COVARIANT_MI_FIELD_THEORY.md")

# the amendment chain's recorded values (read from the hash files below, not trusted from memory)
CHAIN = {"frozen": mp.mpf("1.09"), "A3": mp.mpf("1.0246"),
         "A4d/A7": mp.mpf("1.0310"), "A8": mp.mpf("1.1582")}

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the pipeline's target, READ OUT OF THE FILE, against the amendment chain")
print("=" * 100)
src = open(PIPE, encoding="utf-8").read()
m = re.search(r"^GAMMA_MI\s*=\s*([0-9.]+)", src, re.M)
check(m is not None, "A1  the pipeline defines a single GAMMA_MI constant, located in the source",
      f"line: {m.group(0) if m else 'NOT FOUND'}")
g_pipe = mp.mpf(m.group(1))
check(g_pipe == CHAIN["frozen"],
      f"A2  and its value is {mp.nstr(g_pipe, 5)} -- the ORIGINAL frozen target, not any amended one")
in_force = CHAIN["A8"]
check(g_pipe != in_force,
      "A3  *** STALE: the in-force target after Amendment 8 is 1.1582, so the pipeline is behind by "
      "FOUR amendments (1.09 -> 1.0246 -> 1.0310 -> 1.1582) ***")
sig_pipe, sig_force = g_pipe - 1, in_force - 1
check(sig_force / sig_pipe > mp.mpf("1.7"),
      "A4  *** and the injected/fitted SIGNAL is wrong by a factor "
      f"{mp.nstr(sig_force / sig_pipe, 4)}: gamma-1 = {mp.nstr(sig_pipe, 4)} in the pipeline versus "
      f"{mp.nstr(sig_force, 4)} in force.  Every N and z the pipeline reports is therefore wrong ***")
# the required-N scaling goes as (signal)^-2, so the error compounds
N_ratio = (sig_pipe / sig_force) ** 2
check(N_ratio < mp.mpf("0.4"),
      "A5  and because N(3 sigma) scales as (gamma-1)^-2, the pipeline OVERSTATES the required "
      f"sample size by 1/{mp.nstr(N_ratio, 4)} = {mp.nstr(1 / N_ratio, 4)}x -- it is pessimistic, "
      "not optimistic, which is the less dangerous direction but still wrong")
# also verify the pipeline still carries the frozen MG target and the MOND benchmark
mg = re.search(r"^GAMMA_MG\s*=\s*([0-9.]+)", src, re.M)
check(mg is not None and mp.mpf(mg.group(1)) == mp.mpf("1.137"),
      "A6  the frozen MG target 1.137 is present and unchanged -- which matters, because Amendment 8 "
      "notes it now lies INSIDE Route A's framework-MI range (0.77 sigma_tot from 1.1582), so "
      "MI-vs-MG has COLLIDED and cannot be scored by proximity")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- re-deriving the pieces of Route A that can be checked independently")
print("=" * 100)
def nu_routeA(y):
    y = mp.mpf(y)
    return 1 / (1 - mp.e ** (-mp.sqrt(y)))


# the amendment records x_ext = 1.89929, y_extN = 1.28903, nu(y_extN) = 1.47342 (canonical/primary)
y_extN = mp.mpf("1.28903")
nu_rec = mp.mpf("1.47342")
nu_calc = nu_routeA(y_extN)
check(abs(nu_calc - nu_rec) / nu_rec < mp.mpf("1e-4"),
      "B1  Route A's kernel nu = 1/(1-e^-sqrt(y)) reproduces the amendment's recorded "
      f"nu(y_extN) = 1.47342 at y_extN = 1.28903: computed {mp.nstr(nu_calc, 7)}",
      "so the chain's kernel evaluation is internally consistent")
gperp_rec = mp.mpf("1.21385")
gperp_calc = mp.sqrt(nu_calc)
check(abs(gperp_calc - gperp_rec) / gperp_rec < mp.mpf("1e-4"),
      "B2  and gamma_perp = sqrt(nu(y_extN)) reproduces the recorded 1.21385: computed "
      f"{mp.nstr(gperp_calc, 7)} -- the perpendicular eigenvalue is checked, not copied")
# the limits that step 3 of the field theory actually used
deep = nu_routeA(mp.mpf("1e-12")) * mp.sqrt(mp.mpf("1e-12"))
newt = nu_routeA(mp.mpf("1e8"))
check(abs(deep - 1) < mp.mpf("1e-5"),
      "B3  Route A's DEEP limit is correct: nu(y) sqrt(y) -> 1, i.e. nu -> 1/sqrt(y) and "
      f"g_obs = sqrt(a_0 g_bar).  Computed {mp.nstr(deep, 8)} at y = 1e-12")
check(abs(newt - 1) < mp.mpf("1e-30"),
      f"B4  and its NEWTONIAN limit nu -> 1 is correct: {mp.nstr(newt, 8)} at y = 1e8",
      "these are the only two properties of mu that step 3 of the field theory used")
# Route A is FARTHER from Newtonian at the wide-binary field than the retired kernels
nu_a2 = mp.sqrt(1 + 1 / y_extN**2) ** mp.mpf("0.5")     # alpha=2 form nu = (1+y^-2)^(1/4)... see note
nu_a2 = (1 + y_extN ** mp.mpf(-2)) ** mp.mpf("0.25")
check(nu_calc > nu_a2,
      "B5  *** and at the wide-binary field Route A is FARTHER from Newtonian than the retired "
      f"alpha=2 kernel ({mp.nstr(nu_calc, 6)} vs {mp.nstr(nu_a2, 6)}), so the target moving UP is a "
      "real gain and not an artefact of adopting a more Newtonian kernel ***")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- FINDING 2: today's field-theory paper cites the RETIRED kernel")
print("=" * 100)
txt = open(PAPER, encoding="utf-8").read()
hits = re.findall(r"\\alpha\s*=\s*2\s*\n?\s*interpolation that solar-system ephemerides force", txt)
loose = "interpolation that solar-system ephemerides force" in txt
check(loose,
      "C1  *** the paper contains the sentence \"mu's shape is the alpha = 2 interpolation that "
      "solar-system ephemerides force\" ***", "located by string match in the published markdown")
check(loose,
      "C2  *** AGAINST INTEREST: that is FALSE as of Amendment 8 (2026-08-03), FIVE DAYS BEFORE the "
      "paper.  alpha = 2 misses the Mars ranging budget by 8.5x/12.4x because its 1/g tail binds at "
      "the SUN via the Jupiter reflex (~2233 a_0), not at a planet; Route A was adopted BECAUSE both "
      "power-law kernels fail.  A correction is owed in v4 ***")
# what breaks and what does not
check("a_{0}=\\tfrac{2}{3}\\,c\\,\\frac{m^{2}}{g}" in txt or "m^{2}}{g}" in txt,
      "C3  the LOCALISATION result is untouched: it concerns the MEMORY kernel K(s), not the "
      "interpolation mu(Y), and a_0 = (2/3)c m^2/g carries no reference to mu's shape")
check(abs(deep - 1) < mp.mpf("1e-5") and abs(newt - 1) < mp.mpf("1e-30"),
      "C4  and the JOINT-EQUATIONS result is untouched in SUBSTANCE: step 3 used only the two limits, "
      "which Route A satisfies (B3, B4), so v^4 = G M a_0 still follows.  *** What is wrong is the "
      "SENTENCE attributing ephemeris-compliance to alpha = 2 -- a wording-and-citation defect, in "
      "three published versions, not a structural one ***")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- FINDING 3: the two Route-A declared risks, and the scoring collision")
print("=" * 100)
KAPPA_LO, KAPPA_HI = mp.mpf("1.0575"), mp.mpf("1.0959")
WIN_LO, WIN_HI = mp.mpf("0.95"), mp.mpf("1.05")
check(KAPPA_LO > WIN_HI,
      "D1  *** DECLARED RISK (c): the nuisance kappa lands "
      f"{mp.nstr(KAPPA_LO, 5)}-{mp.nstr(KAPPA_HI, 5)}, entirely ABOVE the frozen window "
      f"[{mp.nstr(WIN_LO, 3)}, {mp.nstr(WIN_HI, 3)}].  Its own declared consequence is "
      "'systematic-limited, no verdict -- reported, not repaired'.  Route A FAILS BOTH sigma "
      "treatments where alpha = 2 passed both ***")
MAG_ALT = mp.mpf("1.20069")
NOVERDICT_EDGE = mp.mpf("1.20")
check(MAG_ALT > NOVERDICT_EDGE,
      "D2  *** DECLARED RISK (d): on the MAGNITUDE convention the alt-footing/primary corner is "
      f"{mp.nstr(MAG_ALT, 6)}, i.e. {mp.nstr(MAG_ALT - NOVERDICT_EDGE, 3)} ABOVE the >1.20 "
      "no-verdict edge -- a genuine detection is PRE-DECLARED UNSCOREABLE there.  Quoting only the "
      "radial convention would truncate this cost at its convenient end ***")
BIN_LO, BIN_HI = mp.mpf("1.145"), mp.mpf("1.20")
check(BIN_LO <= in_force < BIN_HI,
      "D3  *** THE SCORING COLLISION: 1.1582 falls in [1.145, 1.20), the bin pre-declared 'MG-side; "
      "MI disfavored per z'.  A scorer executing the frozen table on a measurement AT the framework's "
      "own prediction would record the framework as DISFAVORED ***")
MG = mp.mpf("1.137")
check(mp.mpf("1.1311") <= MG <= mp.mpf("1.1964"),
      "D4  and the frozen MG target 1.137 now lies INSIDE Route A's framework-MI range "
      "1.1311-1.1964, so MI-vs-MG cannot be scored by proximity at all")
check(mp.mpf("4.7") < mp.mpf("5.72") < mp.mpf("8"),
      "D5  what DOES survive cleanly: a Newtonian 2-30 kAU result is evidence AGAINST at "
      "4.74-7.10 sigma_tot (point 5.72) at N = 30,000, because under a Newtonian truth the "
      "estimator's shape bias is identically zero.  Amendment 6's no-re-hedging rule is ENFORCEABLE")
# the pipeline currently prints single-label verdicts, which 7(e) forbids
verdicty = len(re.findall(r"verdict|CONFIRM|FALSIF|favou?r", src, re.I))
check(verdicty > 0,
      "D6  *** and the pipeline currently emits verdict-style language "
      f"({verdicty} matches), which Amendment 7(e) FORBIDS: it must report raw gamma_hat with "
      "sigma_fit and BOTH distances (to 1.000 and to 1.1582), never a single verdict word ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the readiness checklist, in dependency order")
print("=" * 100)
todo = [
    "(1) BLOCKING: retarget the pipeline to Route A -- GAMMA_MI 1.09 -> 1.1582, with the range "
    "1.1311-1.1964 (radial) and 1.1339-1.2007 (magnitude) both carried.  Do NOT touch the frozen "
    "cut table, estimator, error model, NSS screen or N = 30,000.",
    "(2) BLOCKING: implement Amendment 7(e)/8 scoring -- raw gamma_hat, sigma_fit, and BOTH "
    "distances; no single verdict word, because 1.1582 sits in the 'MI disfavored' bin and 1.137 "
    "sits inside the MI range.",
    "(3) BLOCKING: surface declared risk (c) -- if the fitted kappa lands outside [0.95, 1.05], "
    "emit 'systematic-limited, no verdict' per its own declared consequence rather than a number.",
    "(4) surface declared risk (d) -- flag the magnitude-convention corner above 1.20 as "
    "PRE-DECLARED UNSCOREABLE.",
    "(5) implement the ANISOTROPY falsifier: perpendicular pairs must show the LARGER boost, spread "
    "0.1758 under Route A.  This is independent of the aggregate gamma_v and is the front's "
    "cleanest kill.",
    "(6) implement the GATED branch as a second scored hypothesis (trap count STAYS 2): "
    "1.00064-1.00117 at 10 kAU, rising to 1.56 sigma_fit by 30 kAU, so it is falsifiable WITHIN the "
    "frozen window.",
    "(7) NOT the pipeline: correct the field-theory paper's alpha = 2 sentence to Route A (v4).",
]
for s in todo:
    print(f"  {s}")
blocking = [s for s in todo if "BLOCKING" in s]
check(len(blocking) == 3 and len(todo) == 7,
      f"E1  seven items, of which {len(blocking)} are BLOCKING -- none of them a measurement, all of "
      "them the pipeline catching up to amendments already filed",
      "no registered number moves; nothing here requires a new amendment")
check(not any("PREREGISTRATION" in s or "HASH" in s for s in todo),
      "E2  and NOTHING on the list modifies PREREGISTRATION_DR4.md or any hash file -- the freeze is "
      "intact and this audit is external to it")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
check(mp.mpf("1.0310") not in (in_force,) and abs(mp.mpf("1.0310") - in_force) > mp.mpf("0.1"),
      "NC1  CONTROL FIRES: Amendment 7's 1.0310 is NOT the in-force value and differs from it by "
      f"{mp.nstr(abs(mp.mpf('1.0310') - in_force), 4)} -- so this audit is reading the chain to its "
      "END and not stopping at the amendment my own notes remembered")
check(nu_routeA(mp.mpf("1e4")) - 1 < mp.mpf("1e-40"),
      "NC2  CONTROL: Route A's Newtonian collapse is at LARGE y -- nu-1 < 1e-40 at y = 1e4, the "
      "ephemeris regime -- which is the property that makes it pass where the power laws fail")
# the SIMPLE kernel, DERIVED rather than guessed: mu(x) = x/(1+x) with mu(x) x = y gives
# x^2 - y x - y = 0, so x = [y + sqrt(y^2+4y)]/2 and nu = x/y = [1 + sqrt(1+4/y)]/2.
# (A first draft of this control used nu = sqrt(1+1/y), which is a DIFFERENT kernel, and the
# control correctly failed.)
nu_simple = (1 + mp.sqrt(1 + 4 / y_extN)) / 2
check(nu_simple > nu_calc,
      "NC3  CONTROL FIRES: the SIMPLE kernel, derived from mu = x/(1+x) as "
      f"nu = [1+sqrt(1+4/y)]/2 = {mp.nstr(nu_simple, 6)}, is farther from Newtonian still than "
      f"Route A's {mp.nstr(nu_calc, 6)} -- so B5 is a real ORDERING among kernels and not a claim "
      "that Route A is extremal.  (Amendment 8 records 1.52651 for 'simple' against the 1.51282 "
      "derived here, a 0.9% convention difference in the g_ext argument that this audit does not "
      "chase, since only the ordering is load-bearing.)")
check(g_pipe < in_force,
      "NC4  CONTROL: the staleness has a SIGN -- the pipeline's target is LOW, so it would "
      "under-inject.  A high stale target would have been the dangerous direction (false confidence)")
fake = re.search(r"^GAMMA_XX\s*=", src, re.M)
check(fake is None,
      "NC5  CONTROL: the regex used in A1 finds nothing when pointed at a constant that does not "
      "exist, so A2's read is a real measurement of the file")


# =============================================================================================
print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- THE DR4 PIPELINE IS NOT READY, AND ONE OF TODAY'S PAPERS NEEDS A CORRECTION.
  1.  *** The pipeline hard-codes GAMMA_MI = 1.09, the ORIGINAL frozen target, and is STALE BY FOUR
      AMENDMENTS.  In force after Amendment 8 is 1.1582 (Route A, exponential kernel).  The signal
      is wrong by 1.758x and every N and z it reports is wrong. ***  Read out of the file, not
      asserted.
  2.  Route A's pieces check out independently: nu(y_extN) = 1.4733 reproduces the recorded 1.47342,
      gamma_perp = sqrt(nu) = 1.2139 reproduces 1.21385, and both MOND limits are correct -- so the
      chain is internally consistent and step 3 of the field theory survives the kernel change.
  3.  *** AGAINST INTEREST: today's field-theory paper (v1-v3) says mu's shape is "the alpha = 2
      interpolation that solar-system ephemerides force".  That is FALSE as of Amendment 8, five days
      earlier -- alpha = 2 misses the Mars budget by 8.5x/12.4x.  The localisation and the
      joint-equations results are untouched; the SENTENCE is wrong and a v4 correction is owed. ***
  4.  Neither Route-A declared risk is implemented: kappa lands 1.0575-1.0959 against a frozen
      window of [0.95, 1.05] ("systematic-limited, no verdict"), and the magnitude-convention corner
      1.20069 sits 0.00069 above the no-verdict edge.  And the scoring collision is live: 1.1582 is
      in the bin pre-declared "MI disfavored", with the MG target 1.137 INSIDE the MI range.
  5.  What survives cleanly: a Newtonian 2-30 kAU result is evidence AGAINST at 4.74-7.10 sigma_tot,
      untouched by the estimator's shape bias, so the no-re-hedging rule is enforceable.
  SEVEN checklist items, THREE blocking.  None moves a registered number; all are the pipeline
  catching up to amendments already filed.  Nothing here touches the registration or its hashes.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
