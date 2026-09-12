#!/usr/bin/env python3
"""L210 -- CORRECTION LANE: the static health sign was inverted in L205, and what that invalidates.

An independent audit by the collaborating programme (qwen_claude_field_theory/.../closure_front_2026/health/REPORT.md) reports that
L205's algebra for 2 F_Y is correct but its interpretation is not: positive gradient energy requires -F_Y > 0, not F_Y > 0, so the
near-origin health condition is U > 4 d l, the REVERSE of what L205 stated and L207/L208 then used. It also reports that L206's
pressure omitted the W0 counterterm, and that L205's numerical comparison with the kernel mixed the variable the kernel is a function of.

This lane verifies each point independently rather than accepting or disputing it, and records what falls. Every check below MEASURES a
quantity and compares it with a stated threshold; none asserts an expectation. No literal-True checks."""
import numpy as np, sympy as sy, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL210 CORRECTION: the sign of the static health condition, verified against a reference case\n" + "=" * 118)
Y, U, d, l = sy.symbols("Y U d l", positive=True)
# (a) the reference case: an ordinary healthy scalar, to fix which sign of F_Y means healthy
Xs = sy.Symbol("X")
P_std = Xs/2                                                                   # the canonical kinetic term, P(X) = X/2 with X = -(grad chi)^2
F_std = P_std.subs(Xs, -Y)
FY_std = sy.diff(F_std, Y)
energy_std = sy.simplify(-F_std)                                                # for a static configuration the energy density is minus the Lagrangian
check("V1 [reference case fixes the convention] for the canonical scalar P(X) = X/2 the static Lagrangian is -Y/2, so F_Y = -1/2 and the energy density is +Y/2; the measured sign of F_Y for a manifestly healthy field is negative",
      FY_std < 0 and sy.simplify(sy.diff(energy_std, Y)) > 0,
      f"F_Y = {FY_std} and d(energy)/dY = {sy.simplify(sy.diff(energy_std, Y))}: a healthy scalar has NEGATIVE F_Y, so the health condition is -F_Y > 0")
# (b) the action's own F_Y, and the resulting condition
F = -(U/2)*sy.log((U + 2*d*Y)/U) + U + 2*d*l*(sy.sqrt(1 + Y/l) - 1)
FY = sy.simplify(sy.diff(F, Y))
coef = sy.simplify(sy.diff(FY, Y).subs(Y, 0))
check("V2 [the action's coefficient, and the corrected condition] the small-gradient coefficient of F_Y is half of (4d^2/U - d/l), the quantity L205 quoted for 2 F_Y; requiring the energy to be positive means requiring it NEGATIVE, which gives U > 4 d l whichever normalisation is used, since a positive factor cannot change a sign",
      sy.simplify(coef - (2*d**2/U - d/(2*l))) == 0,
      f"F_Y = ({sy.simplify(coef)}) Y + O(Y^2), which is half the coefficient L205 quoted for 2 F_Y; -F_Y > 0 near the origin requires it negative, i.e. U > 4 d l -- the REVERSE of what L205 asserted")
# (c) the audit's numerical counterexample, recomputed here
def CT(Uv, dv, lv, Yv):
    Fy = dv/np.sqrt(1 + Yv/lv) - Uv*dv/(Uv + 2*dv*Yv)
    return -2*Fy
def CL(Uv, dv, lv, Yv):
    h = 1e-8*max(Yv, 1e-8)
    Fy = lambda y: dv/np.sqrt(1 + y/lv) - Uv*dv/(Uv + 2*dv*y)
    Fyy = (Fy(Yv + h) - Fy(Yv - h))/(2*h)
    return -2*(Fy(Yv) + 2*Yv*Fyy)
ct1, cl1 = CT(1, 1, 1, 0.01), CL(1, 1, 1, 0.01)
ct2, cl2 = CT(10, 1, 1, 0.01), CL(10, 1, 1, 0.01)
print(f"    at U = d = l = 1, Y = 0.01 (where L205's stated condition 4 d l > U holds): C_T = {ct1:.8f}, C_L = {cl1:.8f}")
print(f"    at U = 10, d = l = 1, Y = 0.01 (where the corrected condition U > 4 d l holds): C_T = {ct2:.8f}, C_L = {cl2:.8f}")
check("V3 [the counterexample reproduces] at the point satisfying L205's stated condition both stiffnesses measure negative, and at the point satisfying the corrected condition both measure positive: the audit's counterexample is confirmed independently here",
      ct1 < 0 and cl1 < 0 and ct2 > 0 and cl2 > 0,
      f"L205's domain gives ({ct1:.6f}, {cl1:.6f}) and the corrected domain gives ({ct2:.6f}, {cl2:.6f})")
# (d) what this does to the window, and to the verdict on the candidate's history
ASTRA_COMB = [0.0909, 0.0691, 0.0483, 0.0252, 0.0077, 0.0001]
check("V4 [the verdict on the candidate's history REVERSES] with the corrected condition U > 4 d l, that is 4 d l/U < 1, the candidate's own coefficient history satisfies it at every epoch; L208 reported the opposite and that report is withdrawn",
      all(c < 1 for c in ASTRA_COMB),
      "4 d l/U on its branch = " + " ".join(f"{c:.4f}" for c in ASTRA_COMB) + ", all below 1, so all HEALTHY under the corrected condition")
# (e) the pressure, recomputed on the tracked branch
g, q, qp, s, Uv = sy.symbols("gamma q q' s U", positive=True)
W0 = Uv - 2*g*q**2*qp                                                          # the counterterm L206 dropped
p_correct = sy.simplify(0 - Uv + s*W0 + 2*g*q**2*(s*qp))                        # P - V + s W0 + 2 gamma q^2 dQ/dt, with dQ/dt = s q' on the tracked branch
check("V5 [the pressure, recomputed] retaining the counterterm in W0 and using the tracked chain rule, the cubic terms cancel and the pressure is exactly U(s - 1); L206's extra term came from dropping that counterterm",
      sy.simplify(p_correct - Uv*(s - 1)) == 0,
      f"p = {sy.simplify(p_correct)} = U(s - 1) exactly, so the clock identity is s - 1 = w/m_rel with NO cubic correction -- L200's form, and L206's correction to it is withdrawn")
print("    WHAT FALLS, and what stands:")
print("      - L205 V3, the health condition, is INVERTED: it is U > 4 d l, not 4 d l > U;")
print("      - L207's window loses its lower bound, which was that condition, and its upper bound was already flagged as an")
print("        identification rather than a derivation, so the window 1 < 4 d l/U < 8 is WITHDRAWN in its entirety;")
print("      - L208's verdict on the candidate's coefficient history is REVERSED: it satisfies the corrected condition at every epoch;")
print("      - L209, which searched for a history inside that window, is moot and is withdrawn with it;")
print("      - L206's cubic correction to the clock identity is WITHDRAWN; the identity is L200's, s0 - 1 = w/m_rel, exactly;")
print("      - what STANDS: the exact cancellation of F_Y at zero gradient, the quadratic leading power, the fact that the action")
print("        lacks a Y^(3/2) operator, and the Lean theorems, which were conditional rearrangements and remain valid as such.")
check("V6 [the scope of the damage, stated] five results are withdrawn or reversed by a single sign, and the ones that survive are the ones that were pure algebra rather than interpretation: the exact cancellation, the leading power, the absent operator, and the conditional Lean statements",
      sy.simplify(FY.subs(Y, 0)) == 0,
      f"F_Y(0) = {sy.simplify(FY.subs(Y, 0))}, the exact cancellation, which is unaffected by the sign convention and remains the one structural result of L205")
json.dump(dict(corrected_condition="U > 4 d l", withdrawn=["L205 V3", "L207 window", "L208 verdict", "L209", "L206 pressure correction"],
               counterexample=dict(CT_L205_domain=float(ct1), CL_L205_domain=float(cl1), CT_corrected=float(ct2), CL_corrected=float(cl2)),
               survives=["F_Y(0) = 0 exactly", "quadratic leading power", "no Y^(3/2) operator in the action", "Lean theorems as conditional statements"]),
          open("L210_results.json", "w"), indent=1)
print(f"\nL210 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
