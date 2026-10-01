#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_A_g5_solar_stability -- route A (L14a), G5 Solar System (frozen plan section 4.2, gate order 5): POST-HOC CONTINUATION (arms A2/A3 stopped at G0).

FROZEN (shared G5, verbatim): 'No ghost, no gradient instability, hyperbolic/causal (the DE12/DE13/XC criteria); Solar System safe (Cassini) by an explicit statement.'
Frozen plan: 'Q2 (the Sun's own latch; A2 replays CFG251 (iii-b); A3 uses the inhibitor), stability of the coupled latch-fluid-mediator operator (CFG72 found growing
modes for a bath of time tau under its declared operator; the quadratic form is re-derived here and reported), no ghost, hyperbolic.'
Done here: Q2 for the Sun's own cold-fluid cloud (target M_c(<r) = M_sun (sqrt(1+x^2) - 1), a real mass; force a0 sqrt(1+x^2)/... at Saturn) with the bound
Q2 <= 5.2e-27 s^-2 (the record's gate 4.01 / CFG7 H1 recipe: tide = max(|d(dg)/dR|, dg/R)), as a function of the Sun's latch value n.  NOT done: the stability of the coupled
latch-fluid-mediator operator (NOT ADDRESSED: the arm stopped at G0 and the operator needs the funded-ledger field's own equation, which the frozen class does not give).
The 'isolated Sun' numbers differ from CFG251's 1258-1545 x (a different recipe: that lane reports the P2 monopole under its own convention); this script uses CFG230's
(a0/2)/R recipe, which reproduces CFG230's 6.28e3 (a0/2) / 3.54e3 (minimal).
"""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG242_common as C
R = C.Run("CFG242_A_g5_solar_stability")
P = R.P
P(__doc__.strip())
GM_SUN = 1.32712440018e20          # m^3 s^-2
AU = 1.495978707e11
R_SAT = 9.5388 * AU
Q2_BOUND = 5.2e-27
out = {}
for foot, a0 in (("canonical", C.A0_SI_CAN), ("alt", C.A0_SI_ALT)):
    gN = GM_SUN / R_SAT ** 2
    x2 = a0 / gN
    dg = gN * (math.sqrt(1 + x2) - 1.0)            # P2 phantom acceleration at Saturn (isolated Sun, latch fully on)
    # tide recipe: max(|d(dg)/dR|, dg/R), derivative by finite difference
    f = lambda R_: (GM_SUN / R_ ** 2) * (math.sqrt(1 + a0 / (GM_SUN / R_ ** 2)) - 1.0)
    h = 1e-4 * R_SAT
    dd = abs((f(R_SAT + h) - f(R_SAT - h)) / (2 * h))
    q2 = max(dd, dg / R_SAT)
    out[foot] = dict(g_N=gN, x2=x2, dg_over_a0=dg / a0, Q2=q2, ratio=q2 / Q2_BOUND, n_max=Q2_BOUND / q2)
    P(f"    {foot:9s}: g_N(Saturn) = {gN:.3e} m/s^2; x^2 = {x2:.2e}; delta g = {dg / a0:.4f} a0; Q2(n = 1) = {q2:.2e} s^-2 = {q2 / Q2_BOUND:.2e} x the bound; the bound needs the Sun's latch n <= {Q2_BOUND / q2:.1e}")
R.num("Q2", out)
n_frozen_E3 = (0.1473, 0.8484)    # the late-time range of n for a bound shell under the frozen E3 (CFG242_A_g0_legality.py, B3)
P(f"    A2 (iota = 0): the Sun's own latch is on whenever it collapses: n between {n_frozen_E3[0]} and {n_frozen_E3[1]} under the frozen E3 (B3), 1 under the post-hoc E3'': Q2 = n x {out['canonical']['ratio']:.2e} x the bound")
R.check("G5 Q2 arm A2 (iota = 0): the Sun's own latch leaves Q2 <= 5.2e-27 s^-2", out["canonical"]["n_max"] >= n_frozen_E3[0], f"needs n <= {out['canonical']['n_max']:.1e}; the shell latch gives n >= {n_frozen_E3[0]}", kind="result")
R.check("G5 Q2 arm A3 (inhibitor): the Sun forms inside the latched Milky Way, n_Sun = 0", True,
        "PASS BY CONSTRUCTION of the inhibitor (embedded collapse n <= 1e-6, CFG242_A_g0_legality H(i), post-hoc E3''); the host's own phantom tide passes (CFG230: 2.9e-5-7.4e-5 of the bound)", kind="result")
P("  [NOT ADDRESSED] G5 stability / ghost / hyperbolicity of the coupled latch-fluid-mediator operator: the arms stopped at G0; the operator needs the vacuum field's own equation, which the frozen class does not give")
R.verdict("G5 arm A2 (post-hoc)", "FAIL", f"Q2 = n x {out['canonical']['ratio']:.1e} x the bound (canonical; alt {out['alt']['ratio']:.1e}); stability NOT ADDRESSED")
R.verdict("G5 arm A3 (post-hoc)", "UNDEFINED", "Q2 passes only through the inhibitor (by construction); stability NOT ADDRESSED")
R.finish()
