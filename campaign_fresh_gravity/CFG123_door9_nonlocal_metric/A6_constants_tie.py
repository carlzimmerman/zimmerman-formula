#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A6_constants_tie -- G4 of CFG123_FROZEN_CRITERIA.md.

G4-a count of constants beyond kappa and Omega_c h^2 (readings R-A, R-B, DW).
G4-b tie: a0 appears in neither action; diagnostic a_mech = c^2 m against a0 = kappa c H0 sqrt(3 Omega_L/8 pi) (kappa = 1/2), both footings, and the G1 amplitude requirement
      (c1 m^2 G M = a0/3-type: M-dependent, so no M-independent constant can be a tie).
G4-c implied evolution: if the tie is read as a0(z) proportional to sqrt(rho_DE^eff(z)) (RR's 'Lambda' is not constant), a0(z)/a0(0) for z <= 5; pass line 1% (the framework's flat a0(z) law).
G4 PASS requires G4-a (R-A) AND G4-b AND G4-c.  Pre-registered P7: net new constants = 0 only under R-A; the tie is not produced (G4-b FAIL); a0(5)/a0(0) departs from 1 by > 1% (hand estimate ~30%).
MUTATE a: the tuned m (m_req(1e11, x = 0.1)) is a NEW constant: G4-a must flip to FAIL under R-A.  Other modes: not applicable.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import *

MUT = mutate_mode()
if MUT not in ("", "a"):
    print("A6: MUTATE mode", MUT, "not applicable"); sys.exit(3)
R = Report("A6_constants_tie", MUT)
R.banner(f"A6 G4: constants and the a0 tie.  MUTATE={MUT or 'none'}")
lam, sol = rr_background()
mu = math.sqrt(lam)

# ---------------- G4-a
n_new_RA = 0                                        # m is fixed by H(a=1) = H0 (Lambda replaced): net new = 0
if MUT == "a":
    n_new_RA = 1                                    # a tuned, mass-specific m is a new constant
R.P("  G4-a  constants of the action beyond G, c:")
R.P("    RR reading R-A (RR replaces Lambda): m (1) shot to H(a=1) = H0 -> m/H0 = %.6f. It replaces Lambda: net NEW constants beyond kappa and Omega_c h^2 = %d." % (mu, n_new_RA))
R.P("    RR reading R-B (RR alongside Lambda + CDM): m is free -> net new = 1: FAIL by rule 3.")
R.P("    DW: the free function f (locally fbar, fbar', fbar'' at least; globally infinitely many numbers): FAIL by rule 3 unless f is tied at action level (no tie exists).")
R.P("    MUTATE a (a tuned m to plant a G1-A match at one mass) is a new mass-specific constant: counted as net new = 1." if MUT == "a" else "")
g4a = (n_new_RA == 0)
R.verdict("G4-a (R-A)", "PASS (net new = 0)" if g4a else "FAIL", "m replaces Lambda" if g4a else "tuned m")
R.verdict("G4-a (R-B)", "FAIL", "m is a new constant")
R.verdict("G4-a (DW)", "FAIL", "f is a free function")

# ---------------- G4-b
a0c = A0_FOOT["canonical"]
a0_tie = a0_from_tie()
R.P(f"\n  G4-b  a0 = kappa c H0 sqrt(3 Omega_L/8 pi) with kappa = 1/2, Omega_L = {OL_CANON}: {a0_tie:.4e} m/s^2 (canonical footing 9.3603e-11: agree to {abs(a0_tie / a0c - 1):.1e})")
a_mech = C_SI ** 2 * (mu * H0_SI / C_SI)
R.P(f"    a_mech = c^2 m = mu c H0 = {a_mech:.4e} m/s^2;  a_mech/a0 = {a_mech / a0c:.4f} (canonical), {a_mech / A0_FOOT['alt']:.4f} (alt); "
    f"= mu / (kappa sqrt(3 Omega_L/8 pi)) = {mu / (KAPPA * math.sqrt(3 * OL_CANON / (8 * math.pi))):.4f}.  This ratio is a NUMBER of the RR background (a shot value divided by a fitted kappa), produced by nothing in the action; it is not within 0.9-1.1.")
ratio = a_mech / a0c
tie_pure = 0.9 <= ratio <= 1.1
R.check("G4-b(i): a_mech/a0 (canonical) is a pure number in [0.9, 1.1] produced by the action (kappa = 1/2, no new number)", f"{ratio:.4f}", tie_pure)
# G1-linked requirement: the amplitude condition |c1| m^2 G M = a0 / (something O(1)) is mass dependent
Ms = np.array(MASSES) * MSUN
need = a0c / (G_SI * Ms) / (1.0 / 3.0)
R.P("    G1-linked: |R_A| = (1/3) m^2 G M sqrt(1+x^2)/a0 = 1 needs m^2 = 3 a0/(G M sqrt(1+x^2)):  m_req^2 / m^2 = " + ", ".join(f"{q:.2e}" for q in need / (mu * H0_SI / C_SI) ** 2) + " for M_b = 1e9..1e12 (x = 0): M-dependent, so no M-independent constant (a tie) can equal it.")
R.check("G4-b(ii): the linear response's scale can equal a0 for an M-independent constant (m or a tie) at every mass", "m_req^2 varies as 1/M by a factor 1000 over 1e9-1e12 (A2, exact)", False)

# ---------------- G4-c
xs = np.array([math.log(1 / (1 + z)) for z in (0.0, 1.0, 2.0, 5.0, 10.0)])
rho = []
for x_ in xs:
    d, h2, zeta = rr_rhs(x_, sol.sol(x_), lam)
    rho.append(h2 - OM * math.exp(-3 * x_) - OR * math.exp(-4 * x_))
rho = np.array(rho)
ratio_a0 = np.sqrt(rho / rho[0])
R.P("\n  G4-c  a0(z)/a0(0) if a0 ~ sqrt(rho_DE^eff(z)):  " + ", ".join(f"z={z:g}: {v:.4f}" for z, v in zip((0, 1, 2, 5, 10), ratio_a0)) + "   (rho_DE^eff(z)/rho_DE^eff(0) = " + ", ".join(f"{v:.4f}" for v in rho / rho[0]) + ")")
dev5 = abs(ratio_a0[3] - 1)
R.P(f"    departure at z = 5: {dev5:.3%} against the 1% flat-a0 line (hand estimate in the frozen file: 'about 30%', from w = -1.15 held constant; the solved background gives the number above)")
R.check("G4-c: implied a0(z)/a0(0) within 1% for z <= 5", f"z = 5: {ratio_a0[3]:.4f}", dev5 <= 0.01)
R.P("    if instead a0 is pinned to its z = 0 value by hand, the tie is POSTULATED (a0 is not in the RR action), which is the CFG43-type statement, not an RR property.")
R.num("a_mech_over_a0", ratio); R.num("a0_ratio_z5", float(ratio_a0[3]))
# ---------------- pre-registered P7
R.check("P7a (pre-registered): net new constants = 0 only under R-A (R-B: 1; DW: f free)", f"R-A {n_new_RA}, R-B 1, DW free function", n_new_RA == 0)
R.check("P7b (pre-registered): the tie is not produced by the action (G4-b FAIL)", f"a_mech/a0 = {ratio:.3f}; m_req is M-dependent", not tie_pure)
R.check("P7c (pre-registered): implied a0(5)/a0(0) departs from 1 by more than 1%", f"{dev5:.3%}", dev5 > 0.01)
R.check("P7d (pre-registered hand number): the departure at z = 5 is 'about 30%' (25-40%)", f"{dev5:.3%}", 0.25 <= dev5 <= 0.40, load_bearing=False)
R.verdict("G4 (constants)", "FAIL", f"G4-a R-A {'PASS' if g4a else 'FAIL'} (m replaces Lambda), G4-b FAIL (a_mech/a0 = {ratio:.3f}, no tie; m_req M-dependent), G4-c FAIL (a0(5)/a0(0) = {ratio_a0[3]:.3f}); R-B and DW FAIL G4-a")
sys.exit(finish(R, MUT))
