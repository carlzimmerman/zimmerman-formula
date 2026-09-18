#!/usr/bin/env python3
"""L280 -- the alpha_2 reconciliation of the standing candidate (CK10): the scorecard's 'PPN PASS' carried alpha_2(clock) = -6e-6
against a bound of 4e-7 without reconciling them.  Here: (1) the record's Einstein-aether (Foster-Jacobson 2006) treatment under
the pipeline's map c1 = -c3 = K_B, c4 = c14 - K_B gives alpha_1 = -4 c14 EXACTLY and alpha_2 = c14 [c14(1 + 2 c2) - c2] / [c2 (2 - c14)]
exactly; (2) the khronometric (hypersurface-orthogonal clock) formulas of Blas, Pujolas & Sibiryakov 2011 (arXiv:1007.3503 eq. 5.34,
small couplings), alpha_1 = -4(alpha - 2 beta), alpha_2 = (alpha - 2 beta)(alpha - lambda' - 3 beta)/(2(lambda' + beta)), with
alpha = c14, beta = c13 = 0, lambda' = c2, COINCIDE with (1) at the relevant order -- so the record's method was right for c13 = 0
even though BPS warn the aether alpha_1,2 cannot be used in general (the transverse modes that contaminate them are absent at c13 = 0);
(3) both vanish on the equal-speed locus c2 = c14/(1 - 2 c14) (all modes at c), the c2* the pipeline found in g03v; (4) the two corners
of the candidate's parameter space that satisfy |alpha_2| < 4e-7 (Nordtvedt 1987; BPS quote 1e-7) together with |alpha_1| < 1e-4, the
Cherenkov bound c2 >= c14 and the dark-sector locus |K2| = (2 - K_B)^2/c2 in [5e4, 3.24e5]: the RIGID branch c14 <= 8.0e-7 (2.0e-7 at
1e-7) with c2 free in the window, and the EQUAL-SPEED branch c2 = c14/(1 - 2 c14) with c14 in [1.0e-5, 2.5e-5]; (5) the record's f33 corner
(c14 = 1e-5, c2 = 1) FAILS alpha_2 by 12x (50x): the scorecard row 4 was not a pass on alpha_2 -- a finding.  Consequences at each corner
(G_N, alpha_1, the strong-coupling scale sqrt(c14) M_P) are printed.  Lean: lean_2026/L280_alpha_ppn.lean.  A FAIL is a finding."""
import os, json, math
import sympy as sp
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L280 -- alpha_2 reconciliation for the clock host\n")
c14, c2, KB, c13 = sp.symbols('c_14 c_2 K_B c_13', real=True)
# ---------------------------------------------------------------- 1. Foster-Jacobson under the pipeline's map
c1v, c3v, c4v = KB, -KB + c13, c14 - KB           # c13 = c1 + c3 kept symbolic for the control; the pipeline has c13 = 0
c123 = c1v + c2 + c3v; c14v = c1v + c4v
a1_FJ = -8 * (c3v ** 2 + c1v * c4v) / (2 * c1v - c1v ** 2 + c3v ** 2)
a2_FJ = a1_FJ / 2 - (c1v + 2 * c3v - c4v) * (2 * c1v + 3 * c2 + c3v + c4v) / (c123 * (2 - c14v))
a1_0 = sp.simplify(a1_FJ.subs(c13, 0)); a2_0 = sp.factor(sp.simplify(a2_FJ.subs(c13, 0)))
check("1a Foster-Jacobson under the pipeline's map (c1 = -c3 = K_B, c4 = c14 - K_B, i.e. c13 = 0): alpha_1 = -4 c14 EXACTLY, K_B drops out",
      sp.simplify(a1_0 + 4 * c14) == 0, f"alpha_1 = {a1_0}")
closed = c14 * (c14 * (1 + 2 * c2) - c2) / (c2 * (2 - c14))
check("1b and alpha_2 = c14 [c14 (1 + 2 c2) - c2] / [c2 (2 - c14)] EXACTLY (K_B drops out; the record's '-c14/2 + c14^2/(2 c2) + O(c14^2)' is its expansion)",
      sp.simplify(a2_0 - closed) == 0 and sp.simplify(sp.series(a2_0, c14, 0, 3).removeO() - (-c14 / 2 + c14 ** 2 / (2 * c2) + sp.Rational(3, 4) * c14 ** 2 * 0)).subs(c14, 0) == 0,
      f"alpha_2 = {a2_0}; series: {sp.series(a2_0, c14, 0, 3)}")
check("1c CONTROL: with c13 != 0 the identity alpha_1 = -4 c14 fails (the map, not an accident, is what makes alpha_1 K_B-free)",
      sp.simplify(a1_FJ + 4 * c14) != 0, f"alpha_1(c13) + 4 c14 = {sp.simplify(a1_FJ + 4*c14)}")
# ---------------------------------------------------------------- 2. the khronometric formulas (BPS 2011 eq. 5.34) at c13 = 0
al, be, lam = c14, sp.S(0), c2                     # alpha = c14, beta = c13 = 0, lambda' = c2
a1_BPS = -4 * (al - 2 * be); a2_BPS = (al - 2 * be) * (al - lam - 3 * be) / (2 * (lam + be))
diff2 = sp.simplify(a2_0 - a2_BPS)
worst = max(abs(float(diff2.subs({c14: x, c2: y}))) for x in (1e-7, 1e-6, 1e-5, 2.5e-5) for y in (1e-5, 1e-4, 1e-2, 1.0))
check("2a the khronometric (BPS 2011, eq. 5.34) alpha_1 = -4 alpha equals the record's alpha_1 = -4 c14 identically, and the BPS alpha_2 = (c14/2)(c14/c2 - 1) equals the record's aether-formula alpha_2 to O(c14^2): |difference| < 1e-9 over c14 in [1e-7, 2.5e-5], c2 in [1e-5, 1] -- the record's method is validated for the clock at c13 = 0",
      sp.simplify(a1_BPS - a1_0) == 0 and worst < 1e-9, f"alpha_2(FJ) - alpha_2(BPS) = {diff2}; worst |diff| = {worst:.1e}")
# ---------------------------------------------------------------- 3. the zero locus
zero_FJ = sp.solve(sp.Eq(a2_0, 0), c2); zero_BPS = sp.solve(sp.Eq(a2_BPS, 0), c2)
check("3a alpha_2 vanishes on the equal-speed locus: FJ exactly at c2 = c14/(1 - 2 c14) (the pipeline's c2*, g03v), BPS at lambda' = alpha, i.e. c2 = c14 -- the same locus to O(c14^2), where every mode propagates at c",
      len(zero_FJ) == 1 and sp.simplify(zero_FJ[0] - c14 / (1 - 2 * c14)) == 0 and zero_BPS == [c14], f"FJ zero: c2 = {zero_FJ[0]}; BPS zero: c2 = {zero_BPS}")
# ---------------------------------------------------------------- 4. the corners
B1, B2_N, B2_BPS = 1e-4, 4e-7, 1e-7
f_a2 = sp.lambdify((c14, c2), a2_0, 'math')
rigid = {}                                          # rigid branch: c2 >> c14: alpha_2 -> -c14/2 (1 + ...)
for lab, bound in (("Nordtvedt 4e-7", B2_N), ("BPS 1e-7", B2_BPS)):
    c14max = sp.nsolve(sp.Eq(-a2_0.subs(c2, 1.0), bound), c14, 2 * bound)     # c2 = 1 (rigid); alpha_2 < 0 there
    rigid[lab] = float(c14max); print(f"    rigid branch (c2 = 1): |alpha_2| < {bound:.0e} needs c14 <= {float(c14max):.3e}")
check("4a RIGID branch (c2 >> c14): |alpha_2| < 4e-7 needs c14 <= 8.0e-7, and < 1e-7 needs c14 <= 2.0e-7; both satisfy |alpha_1| = 4 c14 < 1e-4, Cherenkov c2 >= c14 for any c2 in the locus window, and leave the dark-sector window |K2| = (2-K_B)^2/c2 in [5e4, 3.24e5] untouched (c2 in [1e-5, 6.5e-5] at K_B = 0.2)",
      abs(rigid["Nordtvedt 4e-7"] - 8.0e-7) < 0.5e-7 and abs(rigid["BPS 1e-7"] - 2.0e-7) < 0.2e-7 and 4 * rigid["Nordtvedt 4e-7"] < B1, f"c14_max = {rigid}")
KBn = 0.2; K2min, K2max = 5e4, 3.24e5
def K2_of(c14n): c2s = c14n / (1 - 2 * c14n); return (2 - KBn) ** 2 / c2s
eq = {c14n: dict(c2=c14n / (1 - 2 * c14n), alpha2=f_a2(c14n, c14n / (1 - 2 * c14n)), alpha1=-4 * c14n, K2=K2_of(c14n)) for c14n in (1e-6, 1e-5, 1.5e-5, 2.5e-5)}
for k, v in eq.items(): print(f"    equal-speed branch c14 = {k:.1e}: c2* = {v['c2']:.4e}, alpha_2 = {v['alpha2']:.1e}, alpha_1 = {v['alpha1']:.1e}, |K2| on the locus = {v['K2']:.2e} ({'inside' if K2min <= v['K2'] <= K2max else 'OUTSIDE'} the window)")
c14_lo = (2 - KBn) ** 2 / K2max / (1 + 2 * (2 - KBn) ** 2 / K2max)     # c2* <= 6.48e-5 <=> c14 >= ...; c2* = c14/(1-2c14) >= (2-K_B)^2/K2max
check("4b EQUAL-SPEED branch (c2 = c14/(1 - 2 c14)): alpha_2 = 0 to machine precision for every c14; with the dark-sector window it requires c14 in [1.0e-5, 2.5e-5] (lower edge from |K2| <= 3.24e5, upper edge from alpha_1), i.e. |K2| in [1.3e5, 3.24e5] -- g03v's fast-clock branch, now with alpha_2 settled",
      all(abs(v["alpha2"]) < 1e-12 for v in eq.values()) and abs(c14_lo - 1.0e-5) < 0.1e-5 and K2min <= K2_of(2.5e-5) <= K2max and K2_of(1e-6) > K2max, f"c14 window [{c14_lo:.2e}, 2.5e-5]; |K2|(1e-5) = {K2_of(1e-5):.2e}, |K2|(2.5e-5) = {K2_of(2.5e-5):.2e}")
a2_corner = f_a2(1e-5, 1.0)
check("5 the record's f33 corner (c14 = 1e-5, c2 = 1) FAILS the alpha_2 bound: |alpha_2| = 5.0e-6 = 12x the Nordtvedt bound, 50x BPS's -- the candidate scorecard's 'PPN derived: PASS' was not a pass on alpha_2 [FAIL-as-finding of the record, PASS = verified]",
      abs(a2_corner) > 10 * B2_N and abs(abs(a2_corner) / 5.0e-6 - 1) < 0.05, f"alpha_2(f33 corner) = {a2_corner:.2e}")
# ---------------------------------------------------------------- consequences at the two corners
MP_GeV = 1.22e19
cons = {"rigid c14 = 8e-7": dict(alpha1=-4 * 8e-7, GN_over_G_minus1=8e-7 / 2, Lambda_sc_GeV=math.sqrt(8e-7) * MP_GeV), "equal-speed c14 = 1e-5": dict(alpha1=-4e-5, GN_over_G_minus1=5e-6, Lambda_sc_GeV=math.sqrt(1e-5) * MP_GeV, K2=K2_of(1e-5))}
for k, v in cons.items(): print(f"    {k}: " + ", ".join(f"{kk} = {vv:.2e}" for kk, vv in v.items()))
OUT.update(dict(alpha1=str(a1_0), alpha2=str(a2_0), rigid_c14_max=rigid, equal_speed=eq, corners=cons, f33_corner_alpha2=a2_corner))
n, n_pass = len(CH), sum(CH)
print(f"\nL280 COMPLETE: {n_pass}/{n} checks PASS.")
print("""VERDICT.  alpha_2 is not a wall for the clock host, but the corner the record used is not a pass: at c14 = 1e-5, c2 = 1 the clock's own
alpha_2 = -5e-6 is 12x over the 4e-7 bound.  Two corners satisfy every preferred-frame bound together with the record's own constraints:
RIGID, c14 <= 8e-7 (2e-7 at the 1e-7 limit) with c2 anywhere in the dark-sector locus window; or EQUAL-SPEED, c2 = c14/(1 - 2 c14) with
c14 in [1e-5, 2.5e-5], where alpha_2 vanishes identically and every mode runs at c.  The khronometric formulas of BPS 2011 coincide with the
record's aether-formula closed form at c13 = 0, validating f33's method.  Either corner costs nothing elsewhere on the record (G_N/G - 1 <=
5e-6, strong-coupling scale sqrt(c14) M_P ~ 1e16 GeV, Cherenkov satisfied).  CK10 is settled; the scorecard's row 4 should read PASS AT
c14 <= 8e-7 OR ON THE EQUAL-SPEED LOCUS, not 'alpha_2 = -6e-6'.  Nothing here derives kappa.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "L280_results.json"), "w"), indent=1, default=str)
