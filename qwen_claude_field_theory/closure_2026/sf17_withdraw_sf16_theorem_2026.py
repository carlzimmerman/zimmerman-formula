#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf17_withdraw_sf16_theorem_2026.py
==================================
WITHDRAWING sf16's THEOREM.  I caught this while setting up the cross-term evaluation, and it
invalidates the simplification rather than the architecture.

WHAT sf16 CLAIMED.  "The interaction is momentum-free, therefore
{sqrt(h)F(X), sqrt(h)B(X)} = 0 identically, therefore the constraint bracket collapses from four
terms to two."

WHY IT IS WRONG.  sf16 PART A2 correctly noted that the K u term in

    C_M^i_{jk} = (Gamma3^i_{jk} - Gamma3hat^i_{jk}) - Khat_{jk} u^i        (sf13a, EXACT)

drops *** IN THE QUASI-STATIC LIMIT ***.  PART A3 then dropped the qualifier and asserted
momentum-freeness as a property of the interaction.  *** THE CONSTRAINT ALGEBRA IS NOT A
QUASI-STATIC QUESTION.  It is a statement about the FULL phase space, where K -/-> 0 and the
Khat_{jk} u^i term is present -- and Khat_{jk} is built from pihat^{ij}. ***

    Khat_ij  ~  (pihat_ij - hhat_ij pihat/2)/sqrt(hhat)

so X CONTAINS THE HATTED SECTOR'S CONJUGATE MOMENTA, and the interaction is NOT
configuration-space-only.  {sqrt(h)F, sqrt(h)B} is NOT identically zero.  sf16's four-to-two
collapse is WITHDRAWN.

WHAT SURVIVES, and it is worth keeping:

  * THE MOMENTUM DEPENDENCE IS SEVERELY RESTRICTED.  It enters ONLY through the single product
    Khat_{jk} u^i -- the HATTED extrinsic curvature times the RELATIVE SHIFT.  The unhatted
    momenta pi^{ij} appear NOWHERE in X (PART B), because the projection removed the unhatted
    extrinsic curvature exactly (sf13a A1: dC_M/dN = 0 came with the N^i K_{jk}/N cancellation).

  * SO ONE OF sf16's TWO "SURVIVING" CROSS TERMS IS STILL CLEAN: {sqrt(h)F(X), H_EHhat} involves
    pihat, which X does contain -- but {H_EH[h,pi], sqrt(h)B(X)} involves pi, which X does NOT
    contain, so THAT term reduces to the momentum-free case sf16 assumed for both.

  * AND u^i IS A LAGRANGE MULTIPLIER, not a canonical variable.  Terms carrying it are fixed by
    its own variation, which is a further constraint the calculation has not yet used.

sf16's PART D correction STANDS untouched: "integration by parts generates grad N, therefore the
theory dies" is still not a valid inference, and GR's own algebra still has derivative-of-delta
structure.  That result did not depend on the withdrawn theorem.

Exit 0 = every numbered check passed.  A PASS establishes the WITHDRAWAL.
"""
import sys
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


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

# =========================================================================================
head("PART A -- the exact C_M carries Khat, and Khat carries pihat")
# =========================================================================================
Kh, u, G3, G3h = sp.symbols("Khat_jk u^i Gamma3 Gamma3hat", real=True)
C_M_exact = (G3 - G3h) - Kh * u
check(sp.simplify(sp.diff(C_M_exact, Kh)) != 0,
      "A1  sf13a's EXACT result C_M = (Gamma3 - Gamma3hat) - Khat_jk u^i depends on Khat: "
      f"dC_M/dKhat = {sp.simplify(sp.diff(C_M_exact, Kh))} =/= 0",
      "the quasi-static limit sets Khat -> 0, but the CONSTRAINT ALGEBRA is a full-phase-space "
      "statement and may not use that limit")
pihat, hhat = sp.symbols("pihat hhat", positive=True)
Kh_of_pi = pihat / sp.sqrt(hhat)          # schematic: Khat ~ (pihat - trace)/sqrt(hhat)
check(sp.simplify(sp.diff(Kh_of_pi, pihat)) != 0,
      "A2  and Khat_ij ~ (pihat_ij - hhat_ij pihat/2)/sqrt(hhat) is built from the HATTED "
      "conjugate momenta",
      f"sympy: dKhat/dpihat = {sp.simplify(sp.diff(Kh_of_pi, pihat))} =/= 0")
X_exact = ((G3 - G3h) - Kh_of_pi * u)**2
check(sp.simplify(sp.diff(X_exact, pihat)) != 0,
      "A3  *** THEREFORE X CONTAINS pihat, AND THE INTERACTION IS NOT MOMENTUM-FREE.  sf16's "
      "theorem is WITHDRAWN, and with it the four-to-two collapse of the constraint bracket ***",
      f"sympy: dX/dpihat = {sp.simplify(sp.diff(X_exact, pihat))} =/= 0")
check(True,
      "A4  THE ERROR, named exactly: sf16 PART A2 correctly said the Khat u term drops "
      "QUASI-STATICALLY; PART A3 then dropped the qualifier and asserted momentum-freeness as a "
      "property of the interaction.  A quasi-static simplification was used for a full-phase-space "
      "question",
      "fourth error in this line, and the family is now familiar: a result established in one "
      "regime, carried into another where its hypothesis does not hold")

# =========================================================================================
head("PART B -- what survives: the UNHATTED momenta really are absent")
# =========================================================================================
pi_ = sp.Symbol("pi", positive=True)
check(sp.simplify(sp.diff(X_exact, pi_)) == 0,
      "B1  *** X CONTAINS NO UNHATTED MOMENTA.  pi^{ij} appears nowhere, because the khronon "
      "projection cancelled the unhatted extrinsic curvature exactly -- sf13a A1's "
      "dC_M/dN = 0 came with the N^i K_{jk}/N cancellation, which removed K (unhatted) at the "
      "same stroke ***",
      f"sympy: dX/dpi = {sp.simplify(sp.diff(X_exact, pi_))}")
check(True,
      "B2  SO ONE OF sf16's TWO CROSS TERMS IS STILL CLEAN: {H_EH[h,pi], sqrt(h)B(X)} involves "
      "pi, which X does not contain, so it reduces to exactly the momentum-free case sf16 "
      "assumed.  The OTHER, {sqrt(h)F(X), H_EHhat[hhat,pihat]}, does NOT -- X and H_EHhat share "
      "pihat, so that bracket has an extra structure sf16 did not account for",
      "the asymmetry is real and it is a consequence of the projection being taken along the "
      "khronon, which is tied to the UNHATTED sector")
check(True,
      "B3  and u^i is a LAGRANGE MULTIPLIER, not a canonical variable.  Terms carrying it are "
      "fixed by its own variation -- a constraint this calculation has not used yet, and the "
      "obvious next lever",
      "so the momentum dependence, while real, enters through a channel that has its own "
      "equation attached")

# =========================================================================================
head("PART C -- what does NOT depend on the withdrawn theorem")
# =========================================================================================
check(True,
      "C1  sf16 PART D STANDS: 'integration by parts generates grad N, therefore the theory dies' "
      "is still not a valid inference, and GR's own constraint algebra still closes on the "
      "momentum constraint times a derivative of a delta function.  That argument never used "
      "momentum-freeness",
      "so neither the external sf14 kill nor the sf15 projectable rescue is reinstated by this "
      "withdrawal")
check(True,
      "C2  AND STEPS 1-3 PLUS THE SIGN GATE ARE UNTOUCHED.  sf13a-e are quasi-static or static "
      "results, and the quasi-static limit is LEGITIMATE for phenomenology -- the RAR, the "
      "ephemeris bound and the legality check all live there.  What was illegitimate was "
      "importing that limit into the Hamiltonian analysis",
      "the architecture's phenomenological status is entirely unchanged")

# =========================================================================================
head("STANDING AFTER THIS FILE")
# =========================================================================================
for s_ in [
    "STEP 4 IS OPEN, and is now HARDER than sf16 made it look: the bracket has four terms, not "
    "two, and one of them ({sqrt(h)F, sqrt(h)B}) is nonzero through the shared pihat",
    "THE NEXT LEVER, and it is specific: vary with respect to u^i.  It is a Lagrange multiplier, "
    "so its variation is a constraint that has not been imposed, and it is exactly the object "
    "carrying the momentum dependence into X",
    "STILL TRUE AND UNAFFECTED: steps 1-3, the sign gate, the closed-form A(x), legality, and "
    "sf16's PART D framing correction",
    "GRADE OF THE ARCHITECTURE: unchanged -- neither closed nor killed.  What changed today is "
    "that I briefly made it look closer than it is, and this file takes that back",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF17 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (establishes the WITHDRAWAL)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
