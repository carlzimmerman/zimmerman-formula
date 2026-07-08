#!/usr/bin/env python3
r"""
ADJUDICATION of the WINDOW_SURVIVES vs CONTESTED split for "the Saturn thing".

Two adversarial skeptics (passivity_real, applicability_and_wellposed) REFUTED the
positive "well-posed" leg of WINDOW_SURVIVES while ACCEPTING the narrow "aether wall
is mis-applied" leg. The generic-aether-artifact skeptic did NOT refute.

This script independently checks the TWO load-bearing technical claims the refuters raised,
to decide the final binary ON THE FRAMEWORK'S OWN TERMS (passive dS-Unruh frame, MOND-in-matter):

  CLAIM A (refuter passivity_real): once u sits inside Box_u in S_matter, delta S_matter/delta u
    is DIFFERENTIAL in u (contains derivatives of delta u), so 'no kinetic term => 0 dof =>
    trivially well-posed' does NOT follow -- an induced kinetic structure was missed. The
    constraint-term Hessian (2 lambda eta) is the WRONG object.

  CLAIM B (refuter applicability_and_wellposed): the matter 2-point dispersion
    D(w) = w*K(w/a0^2), w=(u.k)^2, is NON-polynomial; large-w expansion = w - sqrt(w)/2 + 1/8 + ...
    The sub-leading sqrt(w)=|u.k| term is NON-analytic in momentum => PSEUDO-differential (nonlocal)
    operator, NOT a local hyperbolic PDE. Matching the leading symbol to GR is necessary but NOT
    sufficient; K has a branch cut at z=-1/4 (K(-1/4)=i) -- the analytic feature that can destroy
    well-posedness. So 'hyperbolic at principal-symbol level' claims MORE than shown.

Default skeptic BOTH ways. Do NOT manufacture a win NOR a deficit.
"""
import sympy as sp
import numpy as np

def H(t): print("\n"+"="*94+"\n "+t+"\n"+"="*94)

# =========================================================================================
H("CLAIM B first (it is the cleaner, decidable one): is the matter symbol a LOCAL PDE or NONLOCAL?")
# =========================================================================================
w = sp.symbols('w', positive=True)   # w = (u.k)^2 >= 0 on real momenta
a0sq = sp.symbols('a0sq', positive=True)
# The framework's g_obs = sqrt(g_bar^2 + g_bar a0) constitutive law, linearized, gives a MATTER
# 2-point structure whose form-factor is K(z), z = Box_u/a0^2. With u fixed, Box_u principal symbol
# = -(u.k)^2 -> in the K argument z ~ (u.k)^2 / a0^2 = w/a0sq. The dispersion multiplier is w*K(w/a0sq).
z = w/a0sq
K = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
D = w*K
Dsimp = sp.simplify(D)
print("  matter dispersion multiplier D(w) = w*K(w/a0^2) =", Dsimp)

# Large-w (UV) expansion -- the refuter's claim: D = w - sqrt(w)/2 + 1/8 + O(1/sqrt w)?
sw = sp.symbols('sw', positive=True)     # sw = sqrt(w)
Dw = D.subs(w, sw**2)
Dw = sp.simplify(Dw)
ser = sp.series(Dw, sw, sp.oo, 4).removeO()
print("  large-|u.k| (sw=sqrt(w)) expansion of D:", sp.expand(ser))
# Extract: is there a sqrt(w) = |u.k| (odd, non-analytic in w) term?
# coefficient of sw^1 (= |u.k|, non-analytic in w) and sw^2 (= w, the local 2nd-order piece)
expl = sp.expand(ser)
coeff_sw2 = expl.coeff(sw, 2)   # w  -> local, sets the cone
coeff_sw1 = expl.coeff(sw, 1)   # |u.k| -> nonlocal, non-analytic in w
print(f"  -> coeff of sw^2 (= (u.k)^2 = w, LOCAL 2nd-order/cone piece): {sp.simplify(coeff_sw2)}")
print(f"  -> coeff of sw^1 (= |u.k|,    NON-ANALYTIC in w, NONLOCAL)  : {sp.simplify(coeff_sw1)}")
assert sp.simplify(coeff_sw2 - 1) == 0, "leading must be the ordinary w term"
assert sp.simplify(coeff_sw1) != 0, "the nonlocal |u.k| term must be present"
print("""
  READING: the leading term is sw^2 = (u.k)^2 = w  -> the ordinary 2nd-order (local, GR-cone) piece.
  The SUB-LEADING term is ~ sw^1 = |u.k|, which is NON-ANALYTIC in w=(u.k)^2 (odd power of |k|).
  => D(w) is NOT a polynomial in the 4-momentum: the operator is genuinely PSEUDO-DIFFERENTIAL
     (NONLOCAL), exactly as the refuter states. The refuter's CLAIM B premise is CORRECT.
""")

# =========================================================================================
H("CLAIM B, the DECIDING sub-question: does the NONLOCAL structure THREATEN hyperbolicity,")
print(  "  or is it a BENIGN, IR-confined, causal correction that leaves the UV cone intact?")
# =========================================================================================
print(r"""
  A nonlocal symbol does NOT automatically mean ill-posed. The decisive facts for well-posedness
  of a symbol D(k) are: (1) the HIGHEST-order (UV/short-distance) behavior sets the characteristic
  cone; (2) whether the non-analytic/nonlocal piece is UV-GROWING (dangerous) or IR-CONFINED/decaying
  (benign); (3) the location of singularities of D in COMPLEX momentum relative to the physical sheet
  (retardedness / causality of the kernel).
""")
# (1) UV: ratio of the nonlocal sqrt(w) term to the leading w term
ratio = sp.simplify((sp.sqrt(w)) / w)   # |u.k| / (u.k)^2  ~ 1/|u.k| -> 0 as |u.k|->oo
print("  (1) UV dominance: [sqrt(w) term]/[w term] ~ sqrt(w)/w = 1/sqrt(w) ->",
      sp.limit(ratio, w, sp.oo), " as |u.k|->oo.")
print("      => the nonlocal |u.k| correction is SUB-DOMINANT in the UV; the leading operator is the")
print("      ordinary 2nd-order (u.k)^2. The CHARACTERISTIC CONE (set by the highest-order symbol) is")
print("      the GR/matter light cone, UNMODIFIED. This is the standard criterion for the PRINCIPAL")
print("      symbol, and it is the ordinary hyperbolic one.")

# (2) Is the nonlocal piece IR-confined? The scale in z=w/a0^2: the sqrt correction is
#     -sqrt(w)/2 = -(a0/2) sqrt(z). Relative to leading w = a0^2 z: correction/leading = 1/(2 sqrt z).
corr_over_lead = sp.simplify(sp.sqrt(w)/2 / w)
print("\n  (2) IR-confinement: correction/leading = (sqrt(w)/2)/w = 1/(2 sqrt(w)).")
print("      In z units (w=a0^2 z): = 1/(2 a0 sqrt(z))... the ABSOLUTE size of the nonlocal term is")
print("      sqrt(w)/2 = (a0/2)*sqrt(z_units)... it is BOUNDED by the a0 scale and only MATTERS when")
print("      w ~ a0^2, i.e. |u.k| ~ a0 -- the DEEP-IR (galactic) regime. At solar/lab |u.k| >> a0 the")
print("      correction is negligible. The nonlocality is an IR (long-memory) effect GAPPED by a0.")

# (3) singularity structure of D in complex w: branch points of K at z=0 and z=-1/4 => w=0 and w=-a0^2/4.
print("\n  (3) singularities of D(w): branch points where 1+4z=0 (z=-1/4 => w=-a0^2/4) and z=0 (w=0).")
print("      w=(u.k)^2. For REAL momenta w>=0, so BOTH branch points sit at w<=0 (w=0 boundary and")
print("      w=-a0^2/4 on the NEGATIVE real w axis, i.e. SPACELIKE/off the physical propagating sheet).")
Kbp = (sp.sqrt(1+4*sp.Rational(-1,4))-1)/(2*sp.sqrt(sp.Rational(-1,4)))
print(f"      K at z=-1/4: {sp.simplify(Kbp)}  (=+i or -i: the branch point is at IMAGINARY K, i.e. it is")
print("      NOT on the real-frequency propagating axis; it is an off-shell analytic feature).")
print("""
  ADJUDICATION of CLAIM B:
   * The refuter is RIGHT that the operator is pseudo-differential (nonlocal), and that matching the
     leading real-axis symbol to GR is necessary-not-sufficient for FULL well-posedness.
   * BUT the refuter's inference 'this can destroy well-posedness' is a POSSIBILITY, not a demonstrated
     obstruction: the nonlocal |u.k| piece is UV-SUB-DOMINANT (ratio ->0), IR-CONFINED (matters only at
     |u.k|~a0), and its branch points sit at w<=0 (off the physical timelike-propagating sheet). These
     are the HALLMARKS of a BENIGN nonlocal/causal-memory correction, NOT of a hyperbolicity-breaking
     term (which would need a UV-GROWING non-analytic piece or a branch cut crossing the physical sheet).
   * NET: neither side is DEMONSTRATED. 'Hyperbolic, well-posed' is NOT established at all orders
     (refuter correct); BUT 'ill-posed / hyperbolicity destroyed' is ALSO not established (the nonlocal
     features are benign-looking). The honest status of the FULL Cauchy problem is OPEN -- the leading
     (principal) symbol is the GR cone, the nonlocal correction is IR-gapped and off-physical-sheet, but
     the all-orders proof is not in hand. This is CONTESTED-leaning-favorable on the well-posedness leg.
""")

# =========================================================================================
H("CLAIM A: does u-inside-Box_u induce a differential (kinetic) structure in delta S_matter/delta u?")
# =========================================================================================
print(r"""
  Box_u X = u^a grad_a (u^b grad_b X). Vary w.r.t. u^mu. Two contributions:
    (i) the EXPLICIT u^a, u^b factors -> ALGEBRAIC in delta u (no new derivative of delta u), BUT
        multiplied by grad's acting on X and on u^b grad_b X (derivatives of the FROZEN u and of X);
    (ii) grad_a acting on (u^b grad_b X): when we vary the INNER u^b, delta(u^b grad_b X)=delta u^b grad_b X
        then grad_a hits it -> grad_a(grad_b X . delta u^b) contains grad_a(delta u^b): a DERIVATIVE of
        delta u. So delta(Box_u X)/delta u DOES contain first derivatives of delta u. Refuter A is right
        that the variation is DIFFERENTIAL in delta u.
""")
# 1D toy to make the derivative-of-delta-u explicit
t = sp.symbols('t')
u = sp.Function('u')(t); X = sp.Function('X')(t); du = sp.Function('du')(t)
Boxu_X = u*sp.diff(u*sp.diff(X,t),t)
# first variation u -> u + eps du, take d/deps at eps=0
eps = sp.symbols('eps')
Boxu_var = (u+eps*du)*sp.diff((u+eps*du)*sp.diff(X,t),t)
dBox = sp.diff(Boxu_var, eps).subs(eps,0)
dBox = sp.expand(dBox)
print("  delta(Box_u X) (1D toy) =", dBox)
has_ddu = dBox.has(sp.Derivative(du, t))
print(f"  contains a DERIVATIVE of delta u (du')? {has_ddu}   -> refuter A's premise CONFIRMED.")

print(r"""
  BUT: the DECISIVE question for WINDOW_SURVIVES is not 'is delta S/delta u differential' (it is);
  it is 'does that make u a PROPAGATING dof with a healthy-or-pathological KINETIC term'. Adjudicate:

   * In the framework, u is NOT determined by delta S_matter/delta u = 0. It is a CONSTRAINED field:
     its 4 components are fixed by (unit norm) + (the passive prescription: u = cosmic rest frame /
     u = -grad T/|grad T| with T the horizon clock / the SME background). delta S_matter/delta u is
     the SOURCE side of the multiplier equation lambda-hat u = -(delta S_matter/delta u), which FIXES
     the multiplier / back-reacts on matter -- it is NOT an independent wave equation solved for u.
   * The induced grad(delta u) terms mean u's variation COUPLES to matter derivatives, i.e. there is a
     matter-frame back-reaction. Whether that back-reaction (a) is non-dynamical on the constraint
     surface, (b) yields a healthy hyperbolic reduced system, or (c) is degenerate/ill-posed is EXACTLY
     the all-orders Cauchy question -- it is NOT settled by the constraint-term Hessian (refuter A is
     right that 2 lambda eta is the wrong object to CLOSE the question).
   * CRUCIAL for the GUARD: this induced structure is a MATTER-COUPLING back-reaction, NOT the generic
     2-derivative c_i(grad u)^2 Einstein-aether KINETIC term. It does NOT resurrect the c13=c14=0 wall
     (there are still no c_i, no spin-1/spin-0 aether modes with vanishing norm, no M_sc). So refuter A
     does NOT flip the verdict to WALLED -- it does NOT show a generic dynamical aether is forced. It
     shows the POSITIVE well-posedness claim was ASSERTED, not proven.
""")

# =========================================================================================
H("FLAT-vs-CURVED dof caveat (refuter passivity_real's second point)")
# =========================================================================================
print(r"""
  Refuter also cites: the flat-space Dirac 2x2 invertible-block dof count (det=b^2) does NOT
  automatically carry to CURVED spacetime, where the presymplectic 2-form can be degenerate and a
  purely non-dynamical preferred frame 'likely creates pathologies'. This is a REAL caveat: the
  clean second-class count was done in flat Minkowski. In curved spacetime the constraint algebra
  must be re-checked; the literature flags that Lagrange-multiplier preferred-frame theories need
  care. This does NOT show a pathology EXISTS for the framework -- it shows the flat count is
  necessary-not-sufficient. Another necessary-not-sufficient => OPEN, not closed, not walled.
""")

# =========================================================================================
H("SYNTHESIS -- the honest binary ON THE FRAMEWORK'S OWN TERMS")
# =========================================================================================
print(r"""
  TWO LEGS of the original WINDOW_SURVIVES:

  LEG 1 (aether wall MIS-APPLIED): the generic Einstein-aether/Horava c13=c14=0 strong-coupling wall
    is a property of a PROPAGATING aether mode's vanishing kinetic norm (M_sc~sqrt(N)Mpl). The
    framework's frame is passive (its own paper: u = the Cassini-constrained cosmic-rest-frame /
    SME background; MOND in MATTER, not a frame EOM). Local covariance does NOT force the generic
    kinetic term (khronon / Lagrange-multiplier / SME-background realizations exist with 0-or-1 gapped
    dof). ==> LEG 1 STANDS. All THREE skeptics (including both refuters) AGREE the wall does not wall
    the framework. The 'Saturn thing' as an AETHER-STRONG-COUPLING objection is genuinely MIS-APPLIED
    to the framework's passive-frame MOND-in-matter realization. The wall binds only the rejected
    AeST/MG limb (D4 +6..14 sigma).

  LEG 2 (positive: passive frame is a HEALTHY WELL-POSED covariant realization): NOT established.
    - CLAIM A confirmed: u inside Box_u makes delta S_matter/delta u DIFFERENTIAL in u; the
      'no-kinetic-term=>0-dof=>trivially-wellposed' inference used the wrong (constraint-only) Hessian.
    - CLAIM B confirmed as premise: the matter symbol is pseudo-differential (nonlocal, |u.k| term);
      leading-symbol match to GR is necessary-not-sufficient. The nonlocal features look BENIGN
      (UV-subdominant, IR-gapped by a0, branch points off the physical sheet) but an all-orders
      well-posedness PROOF is not in hand.
    - flat->curved dof count is necessary-not-sufficient.
    ==> LEG 2 is OPEN (CONTESTED-leaning-favorable): NOT demonstrated well-posed, and NOT demonstrated
        ill-posed. Positive well-posedness was ASSERTED beyond what was shown.

  RULE APPLIED (2/3 refuted => downgrade): the passivity_real and applicability skeptics BOTH refuted
  the POSITIVE well-posedness leg of WINDOW_SURVIVES (while affirming LEG 1). Per the task rule, 2/3
  refuted => DOWNGRADE from WINDOW_SURVIVES to CONTESTED.

  BUT the downgrade is NOT to WALLED: no skeptic showed the framework's own structure FORCES a
  dynamical generic aether hitting the wall. Both refuters EXPLICITLY declined the WALLED stamp. The
  aether wall genuinely does NOT apply to the framework's passive frame.

  ==> FINAL: CONTESTED (leaning favorable). The aether wall is mis-applied (not WALLED); the passive-
      frame + nonlocal-K covariant realization's full Cauchy well-posedness is genuinely open (not a
      clean WINDOW_SURVIVES). 'The Saturn thing' is DISARMED as an aether-strong-coupling objection but
      NOT fully closed as a positive well-posedness result on the framework's own terms.
""")
print("EXIT_OK")
import sys; sys.exit(0)
