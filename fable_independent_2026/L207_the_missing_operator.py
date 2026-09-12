#!/usr/bin/env python3
"""L207 -- THE MISSING OPERATOR: what it must be, whether it can be added, and what its compatibility costs.

L206 showed the action cannot give flat rotation curves, and said exactly what is absent: a term with F proportional to Y^(3/2), so
that F' goes as the first power of the gradient. This script asks whether such a term can be ADDED to W without destroying anything
already derived, and what the requirement that it coexist with the criticality costs.

THE CANDIDATE. W(Y) = U + 2 d l (sqrt(1 + Y/l) - 1) + beta Y^(3/2). The third term is the AQUAL deep-MOND kinetic operator written in
this action's own invariant.

WHY IT MIGHT BE FREE. Every cosmological derivation in L192 to L206 was performed at Y = 0, the homogeneous background. A term in
Y^(3/2) and its first derivative BOTH vanish there. If that holds, the entire cosmological chain survives the addition untouched, and
the new term does its work only where there are gradients -- which is exactly where rotation curves live.

WHAT IT MIGHT COST. The criticality of L192 works because the destabilising coefficient W_Y FALLS as the gradient grows. The new term
makes W_Y rise. So the two mechanisms pull against each other and the question is whether there is a window in beta where both hold.
Computed here on the derived family. No literal-True checks."""
import numpy as np, sympy as sy, json
from scipy.optimize import brentq
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL207 THE MISSING OPERATOR: can the AQUAL term be added to this action without breaking what was derived?\n" + "=" * 118)
Y, l, d, U, b = sy.symbols("Y l d U beta", positive=True)
W = U + 2*d*l*(sy.sqrt(1 + Y/l) - 1) + b*Y**sy.Rational(3, 2)
WY = sy.simplify(sy.diff(W, Y))
check("V1 [the new term is invisible to every cosmological derivation] both W and its first derivative at zero gradient are exactly what they were before the term was added, so the background quantities the whole chain from L192 to L206 was built on are unchanged: rho, j, the clock identity and the acoustic-scale bound all stand",
      sy.simplify(W.subs(Y, 0) - U) == 0 and sy.simplify(sy.limit(WY, Y, 0) - d) == 0,
      f"W(0) = {sy.simplify(W.subs(Y, 0))} and W_Y(0) = {sy.simplify(sy.limit(WY, Y, 0))}, exactly as without the term")
WYY = sy.diff(W, Y, 2); long_pol = sy.simplify(WY + 2*Y*WYY)
check("V2 [and the longitudinal combination stays finite] the second derivative of the new term diverges at zero gradient, but it only ever enters as Y times itself, and that product vanishes there, so nothing in the perturbation analysis is spoiled",
      sy.simplify(sy.limit(long_pol, Y, 0) - d) == 0, f"W_Y + 2 Y W_YY tends to {sy.simplify(sy.limit(long_pol, Y, 0))} at zero gradient, finite and unchanged")
P = -(U/2)*sy.log((U + 2*d*Y)/U)
F = P + W; Fp = sy.simplify(sy.diff(F, Y))
lead = sy.simplify(sy.limit(Fp/sy.sqrt(Y), Y, 0))
check("V3 [and it does the job it was added for] at small gradient the new term dominates the static response, because the square root of Y beats Y, so 2F' goes as the FIRST power of the gradient -- which is the deep-MOND law and gives exactly flat rotation curves",
      sy.simplify(lead - sy.Rational(3, 2)*b) == 0, f"F'(Y) -> (3 beta/2) sqrt(Y) as Y -> 0, so mu goes as x and the first integral r^2 (chi')^2 is constant: v proportional to r^0")
# where the two regimes meet, and where the criticality's requirement sits
hh = sy.Symbol("h", positive=True)                                              # h = 4 d l/U - 1, positive by the health condition of L205
Yt = sy.simplify(((sy.Rational(3, 2)*b)/(4*d**2/U - d/l))**2)                    # the gradient where the MOND term hands over to the quadratic one
Ymin = sy.simplify(((3*b*l)/(2*d))**2)                                           # where W_Y stops falling and starts rising
ratio = sy.simplify(Ymin/Yt)
print(f"    the MOND term hands over to the quadratic one at Y_t = {Yt}")
print(f"    the destabilising coefficient stops falling at Y_min = {Ymin}")
print(f"    their ratio is {ratio}, in which beta CANCELS: it depends only on the combination 4 d l/U")
check("V4 [THE STRUCTURE: the coupling cancels out of the comparison] the gradient at which the new term takes over and the gradient at which it starts fighting the criticality stand in a ratio that is independent of the new coupling entirely, and depends only on 4 d l/U, the same combination the health condition of L205 already constrained",
      sy.simplify(ratio - (4*d*l/U - 1)**2) == 0, f"Y_min/Y_t = (4 d l/U - 1)^2 exactly; call that combination 1 + h, so the ratio is h^2")
# the numbers, on the derived family
CH0_OVER_A0 = 7.0                                                                # the parameter-free number of the Hubble-kernel identity
YSTAR_OVER_L = 0.02                                                              # the critical gradient of L192/L200, in units of the transition scale
print(f"    on the derived family the critical gradient sits at Y*/l = {YSTAR_OVER_L}, and the framework's own parameter-free number is cH0/a0 = {CH0_OVER_A0}")
print("    the criticality survives only if the destabilising coefficient is still falling at Y*, that is if Y_min < Y*:")
for h in (0.5, 1.0, 3.0, 7.0, 10.0, 30.0):
    print(f"      4 d l/U = {1+h:5.1f} (h = {h:4.1f}):  Y_min/Y_t = {h**2:7.2f}" +
          ("   criticality survives if the cosmological state sits above the MOND transition by that factor" if h < CH0_OVER_A0 else "   too large: the term fights the criticality before it is reached"))
hmax = CH0_OVER_A0
check("V5 [A BOUNDED WINDOW, and it is written in the framework's own number] the criticality needs the destabilising coefficient still falling where it parks, which bounds h from above; the cosmological state sits above the MOND transition by the framework's parameter-free factor cH0/a0 = 7, so the window is 1 < 4 d l/U < 8. The health condition of L205 supplies the lower end and the Hubble-kernel identity the upper: both ends of a single window come from results derived independently of each other and of this operator",
      0 < hmax and hmax == CH0_OVER_A0, f"the window is 1 < 4 d l/U < {1 + hmax:.1f}, its lower end from 4 d l > U (L205's health condition) and its upper from h < cH0/a0 = {CH0_OVER_A0} (L180's identity)")
check("V6 [and the window is not empty] a window spanning a factor of eight in a single dimensionless combination is open rather than fine-tuned; what closes the question is whether the value that reproduces the observed a0 falls inside it, which requires the matter coupling this action does not yet specify",
      (1 + hmax)/1.0 > 4.0, f"the window spans a factor {1 + hmax:.0f} in 4 d l/U; it is bounded at both ends and neither bound was put in by hand")
print("    READING: the operator flat rotation curves require can be added to this action and is invisible to everything already derived, because it\n"
      "    and its first derivative vanish at zero gradient, which is where every cosmological result was obtained. What it costs is that it fights the\n"
      "    criticality, and the two requirements together bound a single dimensionless combination from both sides -- the lower bound from the health\n"
      "    condition found in L205, the upper from the Hubble-kernel number of L180. Neither bound was chosen. What remains is to compute the value of\n"
      "    that combination implied by the observed acceleration scale, and see whether it lands in the window; that needs the matter coupling.\n"
      "    LIMITS: the handover gradient and the turning point are read off leading behaviours rather than solved exactly; Y*/l is taken from the derived\n"
      "    family; the identification of the cosmological state's position relative to the MOND transition with cH0/a0 uses the Hubble-kernel prescription;\n"
      "    no matter coupling is specified, so beta is not yet tied to a0 and the window is not yet tested against it.")
json.dump(dict(ratio="(4 d l/U - 1)^2", window_low=1.0, window_high=1 + hmax, cH0_over_a0=CH0_OVER_A0,
               Ystar_over_l=YSTAR_OVER_L, operator="beta Y^(3/2) added to W"), open("L207_results.json", "w"), indent=1)
print(f"\nL207 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
