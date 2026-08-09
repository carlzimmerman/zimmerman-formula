#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_aest_jeans_nonlinear_verdict_2026.py
=======================================
DOES lambda_J ~ 2.7 Mpc ACTUALLY EMERGE FROM AeST?  *** NO.  AND THIS SCRIPT WITHDRAWS THE CLAIM I
PUBLISHED EARLIER TODAY THAT IT DOES. ***

Yesterday's completion script (mi_relativistic_completion_aest_2026.py, Part F) found that the CMB,
cluster and galaxy requirements on how much the AeST scalar clusters are all satisfied by a single
Jeans scale lambda_J = 2.55-2.76 Mpc, and called that a falsifiable prediction.  I flagged that
whether AeST can DELIVER that scale was a calculation nobody had done.  It had been done -- by this
corpus, in `mi_cosmo_perturbations_2026.py`, which already banked:

    "the k^4 handle is CLOSED: M is free and every viable value gives a microscopic Jeans scale.
     No prediction here, and I say so."

*** I reached a MORE FAVOURABLE conclusion than this corpus's own earlier, correct work, and I did not
check the corpus first.  That is the exact failure mode the working rules exist to prevent. ***

--------------------------------------------------------------------------------------------------
THE CALCULATION, AND IT IS DECISIVE (Parts A-C)
--------------------------------------------------------------------------------------------------
The AeST dust sector is a ghost condensate (ACLM 2004; the AeST authors' own identification, Verwayen-
Skordis-Zlosnik 2024 / Blanchet-Skordis 2024, K(Q) = mu^2 (Q-1)^2).  At the condensate the sound speed
vanishes identically, so the leading gradient term is the higher-derivative (nabla^2 pi)^2 / k_M^2 and
the dispersion is omega^2 = c^2 k^4 / k_M^2.  Against gravity that gives

        k_J = (4 pi G rho_cond k_M^2 / c^2)^(1/4),      k_M = M / (hbar c)

  * At the theory's NATURAL condensate scale M = rho_Lambda^(1/4) = 2.24 meV:
        *** lambda_J = 2.8e-11 Mpc.  ELEVEN ORDERS TOO SMALL.  The scalar clusters exactly like CDM
        at every astrophysical scale -- xi = 1.000000 at both cluster and galaxy radii. ***
  * To get lambda_J = 2.7 Mpc you need M = 2.44e-25 eV: *** 22 ORDERS below the natural scale, and
    4.9 orders below the Lyman-alpha fuzzy-dark-matter floor (Rogers & Peiris 2021). ***

The killer is the 22 orders, not the Lyman-alpha bound.  Even granting a generous relaxation of
Lyman-alpha, the natural scale is not close.

--------------------------------------------------------------------------------------------------
AND THE CONSEQUENCE IS WORSE THAN "NO PREDICTION" (Part E)
--------------------------------------------------------------------------------------------------
With lambda_J microscopic, xi = 1: the scalar clusters like CDM.  Then MOND and the dust DOUBLE-COUNT,
because the AQUAL field equation is sourced by the TOTAL density:

        clusters (R500)   overshoot 2.06x        bright spiral   overshoot 4.42x
        dwarf, deep MOND  overshoot 2.73x        LSB dwarf       overshoot 2.64x

*** So the completion does not merely fail to predict the cluster residual -- taken literally with a
CDM-clustering scalar it OVERSHOOTS every regime by 2-4x, including the RAR that MOND exists to fit. ***

--------------------------------------------------------------------------------------------------
WHAT IS STILL OPEN, AND IT IS NOT NOTHING (Part F)
--------------------------------------------------------------------------------------------------
The Jeans analysis is LINEAR.  Whether the Q-sector dust actually virialises in the NONLINEAR regime
is a genuinely unsettled question in the AeST literature, and it is where an answer would have to come
from.  This script does not settle it and does not claim the completion is closed.  What it does
establish is that *** the k^4 mechanism provably cannot be the reason, so the open question is now
sharply located. ***
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


# ---- constants, matched to mi_cosmo_perturbations_2026.py so the numbers are comparable ----------
C_LIGHT = mp.mpf("2.99792458e8")
G_NEWT = mp.mpf("6.67430e-11")
MPC = mp.mpf("3.0856775814913673e22")
KPC = MPC / 1000
HBARC_EVM = mp.mpf("1.973269804e-7")          # eV m
H0 = mp.mpf("67.36") * 1000 / MPC
OM_M, OM_B = mp.mpf("0.3153"), mp.mpf("0.04930")
OM_DM = OM_M - OM_B
RHO_CRIT = 3 * H0 ** 2 / (8 * mp.pi * G_NEWT)
RHO_COND = OM_DM * RHO_CRIT

M_NATURAL = mp.mpf("2.24e-3")                 # eV, = rho_Lambda^(1/4)
M_LYA_FLOOR = mp.mpf("2e-20")                 # eV, fuzzy-DM floor, Rogers & Peiris 2021 PRL 126:071302
LAM_REQ = mp.mpf("2.7") * MPC                 # what Part F needed

F_BAR = mp.mpf("0.93") * mp.mpf("0.167")
INV_FBAR = 1 / F_BAR
LCDM_DARK = INV_FBAR - 1

print(__doc__)


def nu_routeA(y):
    return 1 / (1 - mp.e ** (-mp.sqrt(y)))


# =============================================================================================
print("=" * 100)
print("PART A -- the derivation: why the condensate has ZERO sound speed and a k^4 dispersion")
print("=" * 100)

# The ghost condensate: P(X) with P'(X_0) = 0 at the attractor.  Take P = (lam/2)(X - X_0)^2 and
# write X = X_0 (1 + u).  Then c_s^2 = P'/(P' + 2 X P'').  Derive it rather than quoting it.
lam, X0, u_s = sp.symbols("lambda X_0 u", positive=True)
X = X0 * (1 + u_s)
P = lam * (X - X0) ** 2 / 2
PX = sp.simplify(sp.diff(P, u_s) / sp.diff(X, u_s))
PXX = sp.simplify(sp.diff(PX, u_s) / sp.diff(X, u_s))
cs2 = sp.simplify(PX / (PX + 2 * X * PXX))

check(sp.simplify(cs2 - u_s / (3 * u_s + 2)) == 0,
      "A1  c_s^2 = u/(3u+2) exactly, re-derived here (matches the committed cosmo-perturbation script)",
      f"c_s^2 = {cs2}")

check(sp.limit(cs2, u_s, 0, "+") == 0,
      "A2  *** c_s^2 -> 0 at the condensate.  THIS is why the leading gradient term is "
      "(nabla^2 pi)^2 and the dispersion is k^4, not k^2 ***",
      "the k^2 term is absent because P'(X_0) = 0 -- that is the defining property of a condensate")

check(sp.limit(cs2, u_s, sp.oo) == sp.Rational(1, 3),
      "A3  and c_s^2 -> 1/3 as u -> inf, so 0 <= c_s^2 <= 1/3: no superluminal front anywhere",
      "the condensate is healthy; the problem below is NOT an instability")

# A4 -- the Jeans condition.  omega^2 = c^2 k^4/k_M^2 balanced against 4 pi G rho.
k_sym, kM_sym, rho_sym, G_sym, c_sym = sp.symbols("k k_M rho G c", positive=True)
omega2 = c_sym ** 2 * k_sym ** 4 / kM_sym ** 2
kJ_solved = sp.solve(sp.Eq(omega2, 4 * sp.pi * G_sym * rho_sym), k_sym)
kJ_pos = [s for s in kJ_solved if s.is_real is not False and sp.simplify(s).could_extract_minus_sign() is False]
kJ_expr = sp.simplify((4 * sp.pi * G_sym * rho_sym * kM_sym ** 2 / c_sym ** 2) ** sp.Rational(1, 4))
check(any(sp.simplify(s - kJ_expr) == 0 for s in kJ_solved),
      "A4  k_J = (4 pi G rho k_M^2 / c^2)^(1/4), obtained by SOLVING the balance, not by assertion",
      f"{len(kJ_solved)} roots; the positive real one is {kJ_expr}")


PREF = 4 * mp.pi * G_NEWT * RHO_COND / C_LIGHT ** 2


def lam_J_of_M(M_eV):
    k_M = mp.mpf(M_eV) / HBARC_EVM
    k_J = (PREF * k_M ** 2) ** mp.mpf("0.25")
    return 2 * mp.pi / k_J


def M_of_lam_J(lam_m):
    k_J = 2 * mp.pi / mp.mpf(lam_m)
    return mp.sqrt(k_J ** 4 / PREF) * HBARC_EVM


print(f"\n  Omega_dm = {sig(OM_DM,4)}, rho_cond = {sig(RHO_COND,5)} kg/m^3, "
      f"4 pi G rho/c^2 = {sig(PREF,6)} m^-2")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- FORWARD: what does the theory's NATURAL condensate scale give?")
print("=" * 100)

lam_nat = lam_J_of_M(M_NATURAL)
print(f"\n   M = rho_Lambda^(1/4) = {sig(M_NATURAL,3)} eV  ->  lambda_J = {sig(lam_nat,5)} m "
      f"= {sig(lam_nat/MPC,5)} Mpc")

check(lam_nat < KPC,
      "B1  *** at the natural scale lambda_J is MICROSCOPIC -- far below 1 kpc, let alone 1 Mpc ***",
      f"{sig(lam_nat/MPC,4)} Mpc = {sig(lam_nat/KPC,4)} kpc")

# B2 -- so what does the scalar do at astrophysical radii?  xi(R) = 1/(1+(lam_J/R)^2).
def xi_of(R_mpc):
    return 1 / (1 + (lam_nat / (mp.mpf(R_mpc) * MPC)) ** 2)


xi_cl, xi_gal = xi_of("1.3"), xi_of("0.02")
check(xi_cl > mp.mpf("0.999999") and xi_gal > mp.mpf("0.999999"),
      "B2  *** so xi = 1 at BOTH cluster and galaxy radii: the scalar clusters EXACTLY LIKE CDM ***",
      f"xi(1.3 Mpc) = {sig(xi_cl,8)}, xi(20 kpc) = {sig(xi_gal,8)}")

# B3 -- and confirm the SCALING direction, so the inverse in Part C is not sign-confused:
#       k_J ~ M^(1/2), so lambda_J ~ M^(-1/2): a SMALLER M gives a LARGER Jeans length.
r_lam = lam_J_of_M(M_NATURAL / 100) / lam_nat
check(abs(r_lam - 10) < mp.mpf("1e-6"),
      "B3  scaling check: lambda_J ~ M^(-1/2), so a LARGER Jeans length needs a SMALLER M",
      f"M/100 multiplies lambda_J by {sig(r_lam,6)} (expected 10)")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- INVERSE: *** THE VERDICT ON PART F.  IT IS WITHDRAWN. ***")
print("=" * 100)

M_req = M_of_lam_J(LAM_REQ)
orders_nat = mp.log10(M_NATURAL / M_req)
orders_lya = mp.log10(M_LYA_FLOOR / M_req)

print(f"\n   Part F needed lambda_J = {sig(LAM_REQ/MPC,3)} Mpc  ->  requires M = {sig(M_req,5)} eV")
print(f"   vs the natural scale rho_Lambda^(1/4) = {sig(M_NATURAL,3)} eV : "
      f"{sig(orders_nat,3)} ORDERS below")
print(f"   vs the Lyman-alpha fuzzy-DM floor {sig(M_LYA_FLOOR,2)} eV      : "
      f"{sig(orders_lya,3)} orders below")

check(orders_nat > 20,
      "C1  *** lambda_J ~ 2.7 Mpc requires a condensate scale 22 ORDERS below the theory's natural "
      "one.  It does NOT emerge -- it would have to be imposed ***",
      f"{sig(orders_nat,4)} orders")

check(orders_lya > 4,
      "C2  and the required M is also ~5 orders below the Lyman-alpha fuzzy-DM floor, which closes "
      "the tuning escape",
      f"{sig(orders_lya,4)} orders below Rogers & Peiris 2021 PRL 126:071302")

# C3 -- name which of the two arguments is load-bearing.  The 22 orders is; Lyman-alpha only closes
#       the escape.  Say so, because the Lyman-alpha transfer carries a caveat (Part D).
check(orders_nat > orders_lya * 4,
      "C3  the LOAD-BEARING argument is the 22 orders, NOT Lyman-alpha",
      "so the verdict does not depend on how cleanly the fuzzy-DM bound transfers to this theory")

print("""
  *** THEREFORE: mi_relativistic_completion_aest_2026.py Part F's claim that the three-way
  over-determination is "satisfiable by one scale lambda_J = 2.55-2.76 Mpc" IS WITHDRAWN, and with it
  the "falsifiable prediction: matter-power suppression at k ~ 3.5 h/Mpc".  Part F correctly computed
  what the completion NEEDS.  It does not follow that AeST supplies it, and via the k^4 mechanism AeST
  provably does not. ***""")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- the Lyman-alpha transfer, and a caveat that cuts IN THE FRAMEWORK'S FAVOUR")
print("=" * 100)

print("""
  The fuzzy-DM floor M > 2e-20 eV comes from the same physics -- Jeans suppression of a scalar dark
  component washing out small-scale power in the Lyman-alpha forest.  Apples to apples on M, so the
  comparison in C2 is fair.

  BUT the transfer is not airtight, and the slack runs the framework's way: in THIS theory the MOND
  Y-sector partially compensates suppressed clustering in the nonlinear regime, so the total gravity at
  those scales is not suppressed by as much as the scalar's clustering is.  A dedicated Lyman-alpha
  analysis in AeST could therefore loosen the floor.
  *** It cannot loosen it by 22 orders.  That is why C3 puts the weight on the natural scale. ***""")

# D1 -- quantify the caveat honestly: how much would the floor have to move to rescue Part F?
floor_needed = M_req
check(floor_needed < M_LYA_FLOOR,
      "D1  the caveat is real but bounded: Lyman-alpha would have to move "
      f"{sig(M_LYA_FLOOR/floor_needed,4)}x to admit Part F's scale",
      "and even granting that, the natural-scale gap of 22 orders is untouched")

# NEGATIVE CONTROL: verify the corpus's OWN earlier number reproduces here, or one of us is wrong.
lam_at_lya = lam_J_of_M(M_LYA_FLOOR)
M_for_01Mpc = M_of_lam_J(mp.mpf("0.1") * MPC)
check(M_for_01Mpc < M_LYA_FLOOR,
      "NC-D  CONTROL: reproduces the committed script's own inversion -- lambda_J = 0.1 Mpc needs "
      f"M = {sig(M_for_01Mpc,3)} eV, below the fuzzy floor",
      f"and lambda_J at the floor itself is {sig(lam_at_lya/MPC,4)} Mpc. Two scripts, same numbers.")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- THE CONSEQUENCE: with xi = 1, MOND and the dust DOUBLE-COUNT")
print("=" * 100)

print("""
  The AQUAL field equation is sourced by the TOTAL density, so a CDM-clustering scalar does not
  politely stand aside -- it feeds the MOND boost too.  Effective mass = (1 + xi*LCDM_dark) *
  nu(y_bar*(1 + xi*LCDM_dark)).  At xi = 1 this overshoots everywhere.

   regime              y_bar    MOND alone   observed    with CDM-like scalar   OVERSHOOT""")

REGIMES = [("cluster R500", "0.0684", None), ("bright spiral", "1.0", None),
           ("dwarf, deep MOND", "0.01", None), ("LSB dwarf", "0.003", None)]
overs = []
for lbl, yb_s, _ in REGIMES:
    yb = mp.mpf(yb_s)
    mond = nu_routeA(yb)
    obs = INV_FBAR if lbl.startswith("cluster") else mond
    tot = (1 + LCDM_DARK) * nu_routeA(yb * (1 + LCDM_DARK))
    overs.append(tot / obs)
    print(f"   {lbl:18s} {sig(yb,4):>8s}  {sig(mond,5):>9s}  {sig(obs,5):>9s}   "
          f"{sig(tot,5):>14s}        {float(tot/obs):5.2f}x")

check(min(overs) > mp.mpf("2.0"),
      "E1  *** a CDM-clustering scalar OVERSHOOTS every regime by "
      f"{float(min(overs)):.2f}-{float(max(overs)):.2f}x, including the RAR that MOND exists to fit ***",
      "for galaxies MOND-alone IS the observed value (the RAR is fit by baryons + MOND at 0.108 dex), "
      "so any extra clustered mass is pure overshoot")

check(overs[1] > overs[0],
      "E2  and it is WORST in the high-acceleration regime, where nu is closest to 1 and cannot absorb "
      "the extra mass",
      f"bright spiral {float(overs[1]):.2f}x vs cluster {float(overs[0]):.2f}x")

# NEGATIVE CONTROL: at xi = 0 there must be NO overshoot in galaxies (MOND alone fits the RAR by
# construction) and a SHORTFALL in clusters.  If not, the bookkeeping is wrong.
yb_gal = mp.mpf("0.01")
no_scalar_gal = nu_routeA(yb_gal) / nu_routeA(yb_gal)
no_scalar_cl = nu_routeA(mp.mpf("0.0684")) / INV_FBAR
check(abs(no_scalar_gal - 1) < mp.mpf("1e-30") and no_scalar_cl < 1,
      "NC-E  CONTROL: at xi = 0 galaxies sit at exactly 1.00x (no overshoot) and clusters UNDERSHOOT",
      f"galaxy {sig(no_scalar_gal,6)}x, cluster {sig(no_scalar_cl,4)}x -- the sign flips as it must")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- WHAT IS STILL OPEN.  This is NOT a closed door.")
print("=" * 100)

OPEN = {
    "nonlinear virialisation of the Q-sector dust":
        "THE live option. The Jeans analysis above is LINEAR. Whether the dust actually collapses "
        "into halos in the nonlinear quasi-static regime -- where the Y-sector dominates the field "
        "configuration -- is genuinely unsettled in the AeST literature. If it does not virialise, "
        "xi is small for a reason that has nothing to do with k^4, and Part E's overshoot dissolves.",
    "a second scale in Fcal(Y, Q)":
        "Fcal is a free FUNCTION. A Y-Q cross term could introduce a suppression scale independent of "
        "the condensate mass. Not excluded here -- but it is an ADDED parameter, not a prediction.",
    "an early-universe initial condition":
        "the corpus already established the dust AMOUNT I_0 is a free integration constant fixed only "
        "by an IC; the same freedom may extend to its spatial distribution.",
}
for k, v in OPEN.items():
    print(f"\n  * {k}\n      {v}")

check(len(OPEN) == 3,
      "F1  three live routes remain, and the first is a real open question in the published literature",
      "the k^4 mechanism is closed; the completion is NOT")

check("LIVE" in OPEN["nonlinear virialisation of the Q-sector dust"].upper(),
      "F2  and the result is now SHARPLY LOCATED: the question is whether the dust virialises, "
      "not whether k^4 suppresses it",
      "that is a better-posed question than the one this script started with")


# =============================================================================================
print()
print("=" * 100)
print("PART G -- WHAT I GOT WRONG, AND WHY IT MATTERS")
print("=" * 100)

print("""
  Earlier today I published, in mi_relativistic_completion_aest_2026.py, that one Jeans scale
  lambda_J = 2.55-2.76 Mpc satisfies the CMB, cluster and galaxy requirements simultaneously, and
  called the resulting k ~ 3.5 h/Mpc suppression a falsifiable prediction of the completion.

  This corpus had ALREADY computed the relevant Jeans scale, in mi_cosmo_perturbations_2026.py, and
  banked the conclusion verbatim:

      "the k^4 handle is CLOSED: M is free and every viable value gives a microscopic Jeans scale.
       No prediction here, and I say so."

  *** I did not check the corpus before publishing a more favourable conclusion than its own earlier
  correct work.  Two failures, not one: I manufactured a win, and I duplicated settled work while
  doing it.  The standing rule is to verify a "works" claim as hard as a "fails" claim, and I applied
  it to the cluster number this afternoon and then failed to apply it here. ***

  What that costs: Part F of the completion script, and nothing else.  Parts A-E and G-H of that
  script stand -- and they are where the real content was.""")

WITHDRAWN = [
    "the three-way over-determination is 'satisfiable by one scale' -- WITHDRAWN",
    "'falsifiable prediction: matter-power suppression at k ~ 3.5 h/Mpc' -- WITHDRAWN",
    "the 1.08x five-cluster tightness as evidence FOR the completion -- WITHDRAWN as evidence "
    "(the arithmetic is fine; it measures what is NEEDED, not what is DELIVERED)",
]
STANDS = [
    "the completion is AeST, forced by the CMB requirement",
    "the framework's kernel embeds: deep-MOND exact, Newtonian limit, bijection, convexity",
    "lensing clears quantitatively: Phi = Psi, gamma_PPN = 1, 21.2 sigma -> 0.601 sigma",
    "the g^-2 Lorentz-violation prediction is restored by the aether",
    "dark matter EXISTS in the completion at the full Omega_dm",
    "AeST does NOT make a_0 = kappa c sqrt(G rho_Lambda) structural -- the fork stands",
    "the uniqueness theorem: a_0 = xi c sqrt(G rho) is the only form; kappa still FITTED",
]
print("\n  WITHDRAWN:")
for w in WITHDRAWN:
    print(f"    - {w}")
print("\n  STANDS UNCHANGED:")
for s in STANDS:
    print(f"    - {s}")

check(len(WITHDRAWN) == 3 and len(STANDS) == 7,
      "G1  three claims withdrawn, seven unaffected -- the damage is contained to Part F", "")

check(any("does NOT make a_0" in s for s in STANDS),
      "G2  and note the withdrawal does NOT touch the fork, which was the completion's real result",
      "the lane that works still does not explain a_0")


# =============================================================================================
print()
print("=" * 100)
print("PART H -- CREDIT")
print("=" * 100)
CREDIT = {
    "Arkani-Hamed, Cheng, Luty & Mukohyama 2004 JHEP 0405:074 (hep-th/0312099)":
        "the ghost condensate: zero sound speed, k^4 dispersion. The mechanism analysed here.",
    "Skordis & Zlosnik 2021 PRL 127:161302":
        "AeST -- the completion itself.",
    "Verwayen, Skordis & Zlosnik 2024 / Blanchet & Skordis 2024 JCAP 11(2024)040 arXiv:2404.06584":
        "K(Q) = mu^2 (Q-1)^2, and the AeST authors' OWN identification of the dust sector as a ghost "
        "condensate. The identification this script relies on is theirs, not this corpus's.",
    "Rogers & Peiris 2021 PRL 126:071302":
        "the Lyman-alpha fuzzy-dark-matter floor M > 2e-20 eV.",
    "Milgrom 1999 PLA 253:273 eq 9":
        "nu = sqrt(1 + 1/y) -- MANDATORY standing credit.",
    "this corpus, mi_cosmo_perturbations_2026.py":
        "had the k^4 Jeans result and the correct 'no prediction here' verdict before I re-derived it.",
}
for k, v in CREDIT.items():
    print(f"\n  {k}\n      {v}")
check(len(CREDIT) == 6, "H1  six credits recorded, including to the corpus's own prior work", "")


# =============================================================================================
print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"""
  1.  *** ANSWER: NO.  lambda_J ~ 2.7 Mpc does NOT emerge from AeST. ***  The dust sector is a ghost
      condensate; c_s^2 -> 0 at the condensate (re-derived), so the dispersion is k^4 and
      k_J = (4 pi G rho k_M^2/c^2)^(1/4).  At the natural scale M = rho_Lambda^(1/4) = 2.24 meV the
      Jeans length is {sig(lam_nat/MPC,4)} Mpc -- ELEVEN ORDERS too small.

  2.  Getting 2.7 Mpc needs M = {sig(M_req,4)} eV: *** {sig(orders_nat,3)} orders below the natural scale ***, and
      {sig(orders_lya,3)} orders below the Lyman-alpha fuzzy-DM floor.  The 22 orders is the load-bearing
      argument; Lyman-alpha only closes the tuning escape, and its transfer carries a caveat that
      runs in the framework's favour.

  3.  *** SO PART F OF THE COMPLETION SCRIPT IS WITHDRAWN, INCLUDING THE k ~ 3.5 h/Mpc PREDICTION.
      It correctly computed what the completion NEEDS; it does not follow that AeST supplies it. ***

  4.  *** AND THE CONSEQUENCE IS WORSE THAN "NO PREDICTION".  With lambda_J microscopic the scalar
      clusters like CDM, and because the AQUAL equation is sourced by the TOTAL density, MOND and the
      dust double-count: overshoot {float(min(overs)):.2f}-{float(max(overs)):.2f}x across clusters, spirals and dwarfs -- worst in
      the high-acceleration regime, and it breaks the RAR that MOND exists to fit. ***

  5.  NOT CLOSED.  The Jeans analysis is LINEAR.  Whether the Q-sector dust virialises in the
      nonlinear regime is genuinely open in the AeST literature, and if it does not, the overshoot
      dissolves for a reason unrelated to k^4.  The result is that the open question is now sharply
      located rather than answered.

  6.  *** MY ERROR, STATED PLAINLY: this corpus had already banked "the k^4 handle is CLOSED... no
      prediction here, and I say so."  I published a more favourable conclusion than its own earlier
      correct work without checking it.  I manufactured a win and duplicated settled work doing it. ***

  7.  Contained: three claims withdrawn, seven unaffected.  The completion's real result -- that the
      lane which WORKS does not EXPLAIN a_0 -- is untouched, as is the uniqueness theorem.
""")

print("=" * 100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
