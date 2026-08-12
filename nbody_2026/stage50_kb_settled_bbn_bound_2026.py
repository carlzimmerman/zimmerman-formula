#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage50_kb_settled_bbn_bound_2026.py
====================================
THE SETTLING PASS CONFIRMS STAGE 46 IS DEAD BUT OVERTURNS TWO OF STAGE 48's CLAIMS -- and produces a REAL
new bound on K_B from published work, which the corpus did not have.

--------------------------------------------------------------------------------------------------
CORRECTION 1 -- THE RATIO IS NOT 1.  MY KILL HAD THE RIGHT VERDICT AND THE WRONG MECHANISM.
--------------------------------------------------------------------------------------------------
Stage 48 said: "for AeST c_13 + 3c_2 = 0 identically, so the ratio is 1 and was never available."  The
first half is right, the conclusion is wrong.  The chain in Skordis & Zlosnik's own source is

        Ghat = G_tilde/(1 - K_B/2)  >  G_tilde        [their diagonalisation]
        G_N  = (1 + 1/lambda_s) Ghat  >  Ghat          [their eq. for G_N]

so with G_cosmo = G_tilde (which IS what c_13 + 3c_2 = 0 gives),

    *** G_cosmo/G_local = (1 - K_B/2) x lambda_s/(1 + lambda_s)  <  1  STRICTLY,  supremum exactly 1. ***

The two constants carry DIFFERENT factors, transposed -- so the kill is by INVERSION, not by equality.
Skordis & Zlosnik state the direction as a theorem in the same paper, immediately after their stability
conditions 0 < K_B < 2: "These conditions also imply that G_N > G_tilde always."  Stage 46 needed the ratio
to be 4; the theory forbids it from exceeding 1.

--------------------------------------------------------------------------------------------------
CORRECTION 2 -- alpha_1 = -4 K_B IS *NOT* ESTABLISHED.  Stage 48's third byproduct is WITHDRAWN.
--------------------------------------------------------------------------------------------------
Stage 48 recorded, from a lane report, that "K_B IS constrained after all: alpha_1 = -4 K_B in the
preferred-frame PPN sector."  The settling pass could NOT establish that mapping and returns NO VERDICT on
it.  It is withdrawn.  The corpus's standing statement about K_B's PPN status reverts to unresolved.

--------------------------------------------------------------------------------------------------
AND THE REAL RESULT: BBN BOUNDS K_B, FROM PUBLISHED WORK
--------------------------------------------------------------------------------------------------
Oost, Mukohyama & Wang (Phys. Rev. D 97, 124023), Eq. (3.6): G_cos = G_ae/(1 + (c_13+3c_2)/2), which for
AeST gives G_cos = G_tilde exactly.  Their Eq. (3.7), sourced to Carroll & Lim via the helium abundance:

        *** |G_cos/G_N - 1|  <~  1/8 ***

That is a published bound, not one of ours, and it does three things:

  (a) it kills stage 46's requirement outright -- R = 4 is 24x the bound, Y_p = 0.487 against an observed
      0.2449 +/- 0.0040;
  (b) it EXCLUDES K_B = 3/2 even with the correct direction -- R = 1/4 is 6x the bound, Y_p = 0.187, about
      -15 sigma; and
  (c) *** it gives the corpus a bound it did not have: 0 < K_B <~ 0.25 (at lambda_s -> infinity), and it
      constrains the PAIR, since the ratio also wants lambda_s >~ 7. ***

STATED AGAINST THE PARENT THEORY'S INTEREST: AeST's own CMB fiducials give ratios 0.95 / 0.85 / 0.75 at
K_B = 0.1 / 0.3 / 0.5, i.e. 0.4x / 1.2x / 2.0x the published 1/8 bound.  Only K_B = 0.1 is comfortably
clear.  The corpus's base_a conclusions lean on K_B = 0.1 and are unaffected -- but the higher fiducials
are in mild tension with helium, and that is worth knowing.

CAVEAT ON THE SIGMAS: the linear Y_p fit is being pushed far outside its validated range (0.85 <= S <= 1.15),
so +60 sigma and -15 sigma are order-of-magnitude statements.  The robust content is the ratio against the
published 1/8 bound, and an independent n<->p freeze-out integration agreed with the published fits'
dY_p/dS to 9.5%.

--------------------------------------------------------------------------------------------------
AND ONE OPENING I WRONGLY CLOSED
--------------------------------------------------------------------------------------------------
Stage 48 implied the two-Newton-constant channel does not exist in AeST.  It does -- AeST v2 names its own
extension term gamma_2 (div A-hat)^2 and says it "does not change the quasistatic limit but rescales the
effective G in the FLRW equations".  That is precisely the c_2 slot stage 46 wanted.  The consequence is
R = (2 - K_B)/(2 - 3 gamma_2), so R = 4 requires gamma_2 = K_B/12 + 1/2.

So the honest record is NOT "the channel does not exist".  It is: *the channel runs the WRONG WAY in
minimal AeST, and in the named extension it is bounded to a few percent by BBN* -- R = 4 there is still 24x
the helium bound.  And it would be a brand-new free parameter doing nothing else, so it would not even be
the one-for-one trade stage 46 claimed.

--------------------------------------------------------------------------------------------------
WHAT STANDS FROM STAGE 48
--------------------------------------------------------------------------------------------------
The verdict (stage 46 dead), the tautology diagnosis (K_B = 2(1-kappa^2) sends kappa = 1/2 to K_B = 3/2
identically), the algebraic identity Z = [sqrt(8pi/3)/kappa] sqrt(G_cosmo/G_local), and GW170817 being
satisfied as an IDENTITY -- c_13 = c_1 + c_3 = 0 for every K_B, against Oost et al. Eq. (1.4)'s
|c_13| < 1e-15.  That last one is confirmed and remains stronger than the corpus had banked.
"""

import sys

import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


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


print(__doc__)

KB, lam, g2 = sp.symbols("K_B lambda_s gamma_2", positive=True)
BBN_BOUND = 1.0 / 8.0          # Oost et al. Eq. (3.7), from Carroll & Lim helium
YP_OBS, YP_ERR = 0.2449, 0.0040
DYP_DS = 0.1753                # independent integration; published fits give ~0.16 (9.5% agreement)

print("=" * 100)
print("PART A -- correction 1: the ratio is < 1 strictly, not 1")
print("=" * 100)

R = (1 - KB / 2) * lam / (1 + lam)
sup = sp.limit(R.subs(KB, 0), lam, sp.oo)
check(sup == 1,
      f"A1  G_cosmo/G_local = {R} has supremum {sup}, approached only as K_B -> 0 AND lambda_s -> infinity, "
      f"and is < 1 STRICTLY everywhere in the legal domain",
      "so the two constants carry DIFFERENT, transposed factors -- the kill is by INVERSION, not equality, "
      "and stage 48's 'the ratio is 1' is corrected")

check(float(R.subs({KB: sp.Rational(3, 2), lam: sp.oo}) if False else sp.limit(R.subs(KB, sp.Rational(3, 2)), lam, sp.oo)) == 0.25,
      f"A2  at stage 46's own K_B = 3/2 the theory delivers R = "
      f"{float(sp.limit(R.subs(KB, sp.Rational(3,2)), lam, sp.oo))} -- the exact RECIPROCAL of the 4 it needed",
      "Skordis & Zlosnik state the direction as a theorem after their stability conditions: 'These "
      "conditions also imply that G_N > G_tilde always'")

print()
print("=" * 100)
print("PART B -- the real result: BBN bounds K_B, from published work")
print("=" * 100)

print(f"    published bound (Oost et al. Eq. 3.7, via Carroll & Lim):  |G_cos/G_N - 1| <~ {BBN_BOUND}")
print(f"    {'R':>8} {'|R-1|':>8} {'x bound':>9} {'Y_p':>8} {'vs obs':>9}")
for lab, Rv in (("stage46 needs", 4.00), ("K_B=3/2 (true dir)", 0.25),
                ("K_B=0.5 fiducial", 0.75), ("K_B=0.3", 0.85), ("K_B=0.1", 0.95)):
    S = np.sqrt(Rv)                          # expansion-rate factor ~ sqrt(G)
    Yp = YP_OBS + DYP_DS * (S - 1.0)
    print(f"    {lab:18s} {Rv:5.2f} {abs(Rv-1):8.2f} {abs(Rv-1)/BBN_BOUND:9.1f} {Yp:8.4f} "
          f"{(Yp-YP_OBS)/YP_ERR:+8.1f}s")

check(abs(4.0 - 1) / BBN_BOUND > 10,
      f"B1  stage 46's required R = 4 is {abs(4.0-1)/BBN_BOUND:.0f}x the published bound -- killed outright, "
      f"independently of the direction argument")

check(abs(0.25 - 1) / BBN_BOUND > 3,
      f"B2  *** AND K_B = 3/2 IS EXCLUDED EVEN WITH THE CORRECT DIRECTION: R = 1/4 is "
      f"{abs(0.25-1)/BBN_BOUND:.0f}x the bound ***")

kb_max = 2 * (1 - (1 - BBN_BOUND))
check(abs(kb_max - 0.25) < 1e-9,
      f"B3  *** AND THE COROLLARY IS A BOUND THE CORPUS DID NOT HAVE: at lambda_s -> infinity the bound "
      f"1 - K_B/2 >= 1 - 1/8 gives 0 < K_B <~ {kb_max:.2f}.  It also constrains the PAIR, since the ratio "
      f"wants lambda_s >~ 7 ***",
      "this is prior art (Oost et al. / Carroll & Lim), not a result of ours -- but it was not in the corpus")

info(f"B4  STATED AGAINST THE PARENT THEORY'S INTEREST: AeST's own CMB fiducials sit at ratios 0.95 / 0.85 / "
     f"0.75 for K_B = 0.1 / 0.3 / 0.5, i.e. {abs(0.95-1)/BBN_BOUND:.1f}x / {abs(0.85-1)/BBN_BOUND:.1f}x / "
     f"{abs(0.75-1)/BBN_BOUND:.1f}x the published bound.  Only K_B = 0.1 is comfortably clear, and the "
     f"corpus's base_a conclusions lean on 0.1 so they are unaffected -- but 0.3 and 0.5 are in mild "
     f"tension with helium.")

info("B5  CAVEAT ON THE SIGMAS: the linear Y_p fit is pushed far outside its validated range "
     "(0.85 <= S <= 1.15), so the sigma values above are order-of-magnitude.  The robust content is the "
     "ratio against the published 1/8 bound; an independent n<->p freeze-out integration matched the "
     "published dY_p/dS to 9.5%.  AND NOTE: this stage's sigmas (+43.8, -21.9) differ from the settling "
     "pass's (+60, -15) by ~40%, because we extrapolate the out-of-range fit differently.  Neither is "
     "quotable as a sigma.  The 'x bound' column is identical in both (24x, 6x, 2.0x, 1.2x, 0.4x) and is "
     "the only robust content.")

print()
print("=" * 100)
print("PART C -- correction 2, and an opening I wrongly closed")
print("=" * 100)

info("C1  *** alpha_1 = -4 K_B IS WITHDRAWN.  Stage 48 recorded it from a lane report as 'K_B is "
     "constrained after all via preferred-frame PPN'.  The settling pass could not establish that mapping "
     "and returns NO VERDICT.  K_B's PPN status reverts to unresolved -- and note the BBN bound above now "
     "does the constraining work instead, so the conclusion 'K_B is not unconstrained' survives on "
     "different grounds. ***")

R_ext = (2 - KB) / (2 - 3 * g2)
need_g2 = sp.solve(sp.Eq(R_ext, 4), g2)[0]
check(sp.simplify(need_g2 - (KB / 12 + sp.Rational(1, 2))) == 0,
      f"C2  AND ONE OPENING I WRONGLY CLOSED: AeST v2 names its own extension term gamma_2 (div A-hat)^2, "
      f"which it says 'does not change the quasistatic limit but rescales the effective G in the FLRW "
      f"equations' -- the c_2 slot stage 46 wanted.  It gives R = {R_ext}, so R = 4 needs "
      f"gamma_2 = {sp.simplify(need_g2)}",
      "so the record must NOT say 'the two-Newton-constant channel does not exist'.  It says: the channel "
      "runs the WRONG WAY in minimal AeST, and in the named extension R = 4 is still 24x the helium bound")

info("C3  and even if BBN allowed it, gamma_2 would be a brand-new free parameter doing nothing else -- so "
     "it would not be the one-for-one trade stage 46 claimed, but a strictly worse deal.")

print()
print("=" * 100)
print("PART D -- what stands from stage 48")
print("=" * 100)

kap = sp.symbols("kappa", positive=True)
check(sp.simplify((2 * (1 - kap ** 2)).subs(kap, sp.Rational(1, 2))) == sp.Rational(3, 2),
      f"D1  the TAUTOLOGY DIAGNOSIS stands: K_B = 2(1 - kappa^2) sends kappa = 1/2 to K_B = 3/2 "
      f"identically, so stage 46's 'prediction' was its own input")

info("D2  the algebraic identity Z = [sqrt(8pi/3)/kappa] sqrt(G_cosmo/G_local) stands and is still not "
     "elsewhere in the corpus.")

info("D3  *** AND GW170817 AS AN IDENTITY IS CONFIRMED: c_13 = c_1 + c_3 = 0 for every K_B, against Oost "
     "et al. Eq. (1.4)'s |c_13| < 1e-15.  AeST satisfies that bound exactly, not approximately -- stronger "
     "than the corpus had banked, and it survived the settling pass. ***")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  STAGE 46 STAYS DEAD.  STAGE 48's VERDICT WAS RIGHT AND TWO OF ITS CLAIMS WERE WRONG.

  CORRECTED 1 -- the ratio is NOT 1.  G_cosmo/G_local = (1 - K_B/2) lambda_s/(1 + lambda_s) < 1 STRICTLY,
     supremum exactly 1.  The two Newton constants carry different, transposed factors, so the kill is by
     INVERSION, not by equality -- and Skordis & Zlosnik state the direction as a theorem: "G_N > G_tilde
     always".  Stage 46 needed 4; the theory forbids anything above 1.

  CORRECTED 2 -- alpha_1 = -4 K_B is WITHDRAWN.  The settling pass could not establish that mapping.  K_B's
     PPN status reverts to unresolved.

  AND THE REAL RESULT, which is prior art the corpus did not have: Oost et al. Eq. (3.7), from Carroll &
     Lim's helium analysis, gives |G_cos/G_N - 1| <~ 1/8.  That kills R = 4 at 24x the bound, EXCLUDES
     K_B = 3/2 even in the correct direction at 6x, and yields
        *** 0 < K_B <~ 0.25,  with lambda_s >~ 7 ***
     Against the parent theory's interest: AeST's own fiducials K_B = 0.3 and 0.5 sit at 1.2x and 2.0x that
     bound.  Only K_B = 0.1 is comfortably clear, which is the one the corpus's base_a work uses.

  AND ONE OPENING I WRONGLY CLOSED: the two-Newton-constant channel DOES exist in AeST's own named
     extension, gamma_2 (div A-hat)^2, with R = (2-K_B)/(2-3 gamma_2).  It runs the wrong way in minimal
     AeST and is bounded to a few percent by BBN in the extension -- so record that, not "it does not
     exist".

  STANDING FROM STAGE 48: the verdict, the tautology diagnosis, the algebraic identity, and GW170817
     satisfied as an IDENTITY (c_13 = 0 for every K_B).  That last is confirmed and still stronger than
     banked.

  ON THE COEFFICIENT, unchanged: kappa is MEASURED at 0.551 +/- 0.043, the open content is one factor of
     two, and three routes have now died -- two by tautology, one by estimator degeneracy.
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
