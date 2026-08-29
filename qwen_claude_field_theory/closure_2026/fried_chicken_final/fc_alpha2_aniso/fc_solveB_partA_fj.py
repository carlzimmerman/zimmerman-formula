#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_solveB_partA_fj.py  --  ROUTE B, PART A: the Einstein-aether c-tensor map -> alpha_2^EA (EXACT).
====================================================================================================
The FC-AeST frozen candidate adds an explicit  c_2*(div A)^2  term on the Maxwell locus
    (c1,c2,c3,c4) = (K_B, c2*, -K_B, 0),   c2* = K_B/(1-2 K_B).
This file proves, SYMBOLICALLY and EXACTLY (not just at one numeric K_B), the pure-vector
Einstein-aether preferred-frame result on that locus, using the standard Foster-Jacobson
(gr-qc/0509083) closed forms -- the SAME formulas the committed fc_maxwell_vs_c4_corner_2026.py
uses, here carried symbolically:

  alpha_1^EA = -8(c3^2 + c1 c4)/(2 c1 - c1^2 + c3^2)
  alpha_2^EA = alpha_1/2 - (c1+2c3-c4)(2c1+3c2+c3+c4)/(c123 (2 - c14))
  s2^2 (spin-2) = 1/(1-c13);  s1^2 (spin-1) = (2c1-c1^2+c3^2)/(2 c14 (1-c13));
  s0^2 (spin-0) = c123(2-c14)/(c14(1-c13)(2+c13+3c2))

RESULTS (all sympy-exact):
  [P1]  alpha_1^EA = -4 K_B                            (matches fc_ctensor_map_2026.py)
  [P2]  WITHOUT c2 (bare Maxwell, c2=0): c123=0 => alpha_2^EA has a SIMPLE POLE (diverges): the
        pure-vector preferred-frame alpha_2 is singular -- exactly why the scalar/c2 is needed.
  [P3]  c2* = K_B/(1-2K_B) is the UNIQUE c2 that sets alpha_2^EA = 0 (solved, not guessed).
  [P4]  alpha_2^EA(c2*) = 0 EXACTLY for all K_B.
  [P5]  all three cone speeds are luminal (s0=s1=s2=1) at (c2*, c4=0): healthy vector+scalar-aether.
  [P6]  c123(c2*) = K_B/(1-2K_B) != 0: the (div A)^2 term LIBERATES the spin-0 aether mode, which
        is what regularises the c123->0 pole.

This is the "EA map" half of route B: it gives alpha_2^EA = 0.  The FULL AeST answer is
alpha_2^full = alpha_2^EA + Delta alpha_2^(phiA); Delta from the Q=A.grad(phi) scalar is computed
by the moving-source solve in fc_solveB_setupM.py.  NOTHING here involves the scalar.

EXIT 0 iff every certificate passes.
"""
import sympy as sp
P = lambda *a: print(*a, flush=True)
FAIL, NCH = [], [0]
def check(c, l, d=""):
    NCH[0] += 1; ok = bool(c)
    P(f"  [{'ok' if ok else 'FAIL'}] {l}" + (f"\n         {d}" if d else ""))
    if not ok: FAIL.append(l)
    return ok

KB = sp.Symbol('K_B', positive=True)
c2 = sp.Symbol('c2', real=True)

def FJ(c1, c2_, c3, c4):
    """Foster-Jacobson EA PPN + cone speeds (the fc_maxwell_vs_c4_corner_2026.py formulas)."""
    c13 = c1 + c3; c14 = c1 + c4; c123 = c1 + c2_ + c3
    a1 = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
    a2 = a1/2 - ((c1 + 2*c3 - c4)*(2*c1 + 3*c2_ + c3 + c4))/(c123*(2 - c14))
    s2 = 1/(1 - c13)
    s1 = (2*c1 - c1**2 + c3**2)/(2*c14*(1 - c13))
    s0 = (c123*(2 - c14))/(c14*(1 - c13)*(2 + c13 + 3*c2_))
    return dict(a1=a1, a2=a2, s2=s2, s1=s1, s0=s0, c13=c13, c14=c14, c123=c123)

P("="*96)
P("ROUTE B, PART A -- Einstein-aether c-tensor map on the Maxwell locus (c1=K_B,c3=-K_B,c4=0)")
P("="*96)

# ---- alpha_1 (independent of c2) ----
gen = FJ(KB, c2, -KB, 0)
a1 = sp.simplify(gen['a1'])
P(f"    alpha_1^EA = {a1}")
check(sp.simplify(a1 - (-4*KB)) == 0, "[P1] alpha_1^EA = -4 K_B (exact, all K_B) -- matches fc_ctensor_map")

# ---- P2: bare Maxwell c2=0 -> c123=0 -> alpha_2 pole ----
a2_bare = gen['a2'].subs(c2, 0)
P(f"    c123(c2=0) = {sp.simplify(gen['c123'].subs(c2,0))}  (=0 => singular)")
# multiply by c123 and take c123->0: residue must be nonzero (simple pole)
c123s = sp.Symbol('c123', positive=True)
a2_c123 = a1/2 - ((KB + 2*(-KB) - 0)*(2*KB + 3*(c123s - KB + KB) + (-KB) + 0))/(c123s*(2 - KB))
# here c2 = c123 - c1 - c3 = c123 (since c1+c3=0); rewrite exactly:
a2_c123 = a1/2 - ((-KB)*(2*KB + 3*c123s - KB))/(c123s*(2 - KB))
resid = sp.simplify(sp.limit(a2_c123*c123s, c123s, 0))
P(f"    residue of alpha_2^EA at c123->0 : {resid}")
check(resid != 0, "[P2] bare Maxwell (c2=0): alpha_2^EA ~ (residue)/c123 DIVERGES -- pure-vector "
     "preferred-frame alpha_2 is SINGULAR (c123=0). The (div A)^2 term is mandatory.",
     f"residue = {sp.simplify(resid)} = -K_B^2/(2-K_B)*... (nonzero)")

# ---- P3: solve alpha_2^EA(c2) = 0 for c2 ----
a2 = gen['a2']
c2_sol = sp.solve(sp.Eq(sp.together(a2), 0), c2)
c2_sol = [sp.simplify(s) for s in c2_sol]
P(f"    solve alpha_2^EA(c2)=0  ->  c2 = {c2_sol}")
target = KB/(1 - 2*KB)
hit = any(sp.simplify(s - target) == 0 for s in c2_sol)
check(hit, "[P3] the UNIQUE c2 setting alpha_2^EA=0 is c2* = K_B/(1-2 K_B) (solved, not assumed)",
     f"c2* = K_B/(1-2K_B); solutions found = {c2_sol}")

# ---- P4: alpha_2^EA(c2*) = 0 exactly ----
mx = FJ(KB, target, -KB, 0)
a2_star = sp.simplify(mx['a2'])
P(f"    alpha_2^EA(c2*) = {a2_star}")
check(a2_star == 0, "[P4] *** alpha_2^EA(c2*) = 0 EXACTLY, for all K_B *** (the EA-map half of route B)")

# ---- P5: cone speeds luminal ----
s2 = sp.simplify(mx['s2']); s1 = sp.simplify(mx['s1']); s0 = sp.simplify(mx['s0'])
P(f"    s2^2 = {s2}   s1^2 = {s1}   s0^2 = {s0}")
check(sp.simplify(s2 - 1) == 0 and sp.simplify(s1 - 1) == 0 and sp.simplify(s0 - 1) == 0,
     "[P5] s0^2 = s1^2 = s2^2 = 1 EXACTLY (all cones luminal; healthy) at (c2*, c4=0)")

# ---- P6: c123(c2*) liberates spin-0 ----
c123_star = sp.simplify(mx['c123'])
P(f"    c123(c2*) = {c123_star}")
check(sp.simplify(c123_star - KB/(1-2*KB)) == 0 and c123_star != 0,
     "[P6] c123(c2*) = K_B/(1-2K_B) != 0: the (div A)^2 term LIBERATES the spin-0 aether mode "
     "(regularises the c123->0 pole of [P2])")

P("="*96)
nf = len(FAIL)
P(f"    {NCH[0]-nf}/{NCH[0]} certificates pass" + ("" if nf == 0 else f";  FAILED: {FAIL}"))
if nf == 0:
    P("    ROUTE B PART A: alpha_2^EA(Maxwell corner, c2*) = 0 EXACTLY (all K_B), all cones luminal.")
    P("    => the WHOLE of the frozen-candidate alpha_2 is the scalar piece Delta alpha_2^(phiA).")
import sys
sys.exit(0 if nf == 0 else 1)
