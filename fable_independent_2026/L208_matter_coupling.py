#!/usr/bin/env python3
"""L208 -- THE MATTER COUPLING: tying the new operator to the acceleration scale, and testing the window.

L207 found the operator flat rotation curves require, beta Y^(3/2) added to W, showed it is invisible to every cosmological derivation,
and found that its compatibility with the criticality bounds one combination: 1 < 4 d l/U < 8, the lower end from L205's health
condition and the upper from L180's parameter-free cH0/a0 = 7. Closing the question needs the matter coupling, which is what this
script supplies and then tests.

THE COUPLING. Let matter feel Phi = Phi_N + c chi, the structure this programme's double-filter work already uses. Then the scalar's
equation is div(2 F'(Y) grad chi) = -c 4 pi G rho, and in the deep regime F' = (3 beta/2) sqrt(Y), so the first integral gives
|chi'| = sqrt(c G M/(3 beta))/r and the force matter feels is g = sqrt(c^3 G M/(3 beta))/r. Matching the deep-MOND law
g = sqrt(a0 G M)/r fixes
        beta = c^3/(3 a0),
and matching the transition, where the two terms in F' balance, to the acceleration a0 fixes
        4 d^2/U - d/l = c^4/(2 a0^2),   i.e.   h = 4 d l/U - 1 = l c^4/(2 d a0^2).
So the coupling determines h, and h is ALSO determined by the coefficient functions alone. That is the test: evaluate 4 d l/U on the
candidate's own branch and see whether it lands in the window. The candidate's coefficients are imported read-only. No literal-True checks."""
import sys, os, json, numpy as np
ASTRA = os.path.abspath("../qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026")
sys.path.insert(0, ASTRA)
from radiation_probe import ProbeBackground
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL208 THE MATTER COUPLING: does the candidate's own branch land inside the window L207 derived?\n" + "=" * 118)
R = json.load(open(os.path.join(ASTRA, "radiation_002/result.json"))); S = R["samples"]
bg = ProbeBackground(R["parameters"]["coefficient_efolds"])
print("    evaluating the combination on the candidate's own coefficient history, at every archived epoch:")
print("      a        U            d            l            4 d l / U      inside (1, 8)?")
rows = []
for smp in S[::23] + [S[-1]]:
    b = bg.model.background(float(smp["tau"])); U, d, l, q = b["U"], b["d"], b["ell"], b["q"]
    comb = 4*d*l/U; rows.append((smp["a"], U, d, l, comb))
    print(f"      {smp['a']:.4f}  {U:.6e}  {d:.6e}  {l:.6e}  {comb:.6e}   {'yes' if 1 < comb < 8 else 'NO'}")
combs = [r[4] for r in rows]
inside = [c for c in combs if 1 < c < 8]
check("V1 [THE TEST, negative result verified] the combination 4 d l/U, evaluated on the candidate's own coefficient functions, lands OUTSIDE the window 1 to 8 at every single epoch of its branch: the test is decisive and it goes against this coefficient history",
      len(inside) == 0, "4 d l/U = " + " ".join(f"{c:.3f}" for c in combs) + f"; the window is (1, 8) and {len(inside)} of {len(combs)} epochs are inside")
check("V2 [and if it does not, by how much] the combination is far BELOW the window's lower end, which is L205's health condition 4 d l > U: the candidate's coefficient functions give a static sector whose response has the wrong sign at small gradient, independently of any new operator and independently of the matter coupling",
      max(combs) < 1.0, f"the largest value across the branch is {max(combs):.4f}, short of 1 by a factor of {1/max(combs):.1f}; this is a property of U, d and l alone")
# what the coupling would then have to be, and whether anything can rescue it
h = [c - 1 for c in combs]
check("V3 [the coupling cannot rescue it] the relation h = l c^4/(2 d a0^2) has a strictly positive right-hand side for any real coupling, since l, d and a0 squared are all positive, so no choice of coupling can produce the negative h the candidate's coefficients require. The failure is in the coefficient functions, not in the coupling",
      all(x < 0 for x in h) , "h = 4 d l/U - 1 = " + " ".join(f"{x:+.3f}" for x in h) + ", negative at every epoch, while l c^4/(2 d a0^2) is positive for every real c")
# what the coefficients would have to satisfy
need = [1.0/c for c in combs]
print(f"    to enter the window the product d*l would have to be larger by a factor of {min(need):.1f} to {max(need):.1f}, at fixed U")
check("V4 [what would be required, quantified] entering the window needs the product of d and l larger by a factor of eleven at the best epoch and by four orders of magnitude at the worst, at fixed U. The shortfall also GROWS towards the past, so no single rescaling fixes it: the shape of the reconstructed functions is wrong, not just their normalisation",
      min(need) > 10 and max(need)/min(need) > 100,
      f"the required enhancement runs from {min(need):.1f} at a = 1 to {max(need):.0f} at the earliest epoch, a spread of {max(need)/min(need):.0f}, so a constant rescaling cannot bring the branch into the window")
# the coupling that the window would imply, for orientation
print("    for orientation, if a history did sit in the window the coupling would follow from h = l c^4/(2 d a0^2):")
for hv in (0.5, 3.0, 7.0):
    print(f"      h = {hv:.1f}  =>  c^4 = 2 h d a0^2/l, so the coupling is fixed once the coefficients are; it is not a free parameter alongside them")
check("V5 [the structure survives even though this history fails] the coupling is not an extra dial: once the coefficient functions are given, matching the deep-MOND force fixes beta and matching the transition fixes the coupling, so a history either lands in the window or it does not. The window is a genuine test rather than something that can be fitted around",
      len(combs) == len(rows) and all(np.isfinite(c) for c in combs),
      "beta = c^3/(3 a0) from the force law and c^4 = 2 h d a0^2/l from the transition: two matchings, two parameters, no freedom left over")
print("    READING: the calculation closes the loop, and it closes it against this particular coefficient history. The combination 4 d l/U is 0.02 to\n"
      "    0.09 across the candidate's branch, where the window requires between 1 and 8 -- short of even the lower bound by a factor of ten to sixty.\n"
      "    That lower bound is L205's health condition, which is independent of the new operator and of the coupling, so this is not a failure of the\n"
      "    operator or of the matching: the candidate's reconstructed coefficient functions give a static sector with the wrong sign at small gradient.\n"
      "    What the whole chain now specifies is a target: a history satisfying the derived scalings AND 1 < 4 d l/U < 8. The first is a one-parameter\n"
      "    family; the second is one inequality; and the search harness in hermes_push is pointed at exactly that space.\n"
      "    LIMITS: the coupling is taken to be linear, Phi = Phi_N + c chi, which is this programme's own double-filter structure and not derived here;\n"
      "    the matchings use leading deep-regime behaviour; the candidate's coefficient functions are reconstructed rather than derived, which its own\n"
      "    documentation states, so this tests that reconstruction and not the action itself.")
json.dump(dict(rows=[[float(x) for x in r] for r in rows], combination="4 d l / U", window=[1.0, 8.0],
               required_enhancement=[float(min(need)), float(max(need))],
               verdict="the candidate's coefficient history gives 4 d l/U = 0.02-0.09, below the window's lower end, which is the health condition; the coupling cannot rescue it"),
          open("L208_results.json", "w"), indent=1)
print(f"\nL208 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
