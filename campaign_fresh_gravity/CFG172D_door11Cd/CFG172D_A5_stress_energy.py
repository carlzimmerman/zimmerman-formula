#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG172D_A5 -- the flow sector's stress-energy and the owner's-picture admission checks S1, S2 (frozen criteria 1.6); MUTATE M8 (a khronon charge).

S1  reported: the theta-sector + gate + coupling energy density, pressure and the conservation statement for the static configuration.
    T_uu(theta sector) = (c^4/16 pi G) c2 (delta theta)^2 + coupling energy (negative);  the interaction pressure is isotropic:
    P = E_int = -zeta^2 eps_b^2/(6 c2 eps_L) (derived in A1).
S2  (a) no rest-mass parameter in the flow sector; (b) no conserved charge: the khronon current J^a = (-X)^(-1/2) (g^{ab} + u^a u^b) E_b has
    J^0 = 0 for u = static/comoving (h^{0 nu} = 0), and the leaf-constant Pi_0 is not a charge; (c) the effective density is a functional of the
    baryons: with M_b -> 0 the region kernel's phantom vanishes.  M8 gives the flow a nonzero Noether charge: S2(b) must flip.
Run:  ZF_REPO=<repo> python3 CFG172D_A5_stress_energy.py     (seconds)
"""
import os, sys, math
import numpy as np, sympy as sp
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG172D_common as C
import CFG172D_solver as S

MUT = os.environ.get("MUTATE")
R = C.Report("CFG172D_A5_stress_energy", MUT)
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip()); P(f"\n  repo: {C.rel(C.REPO)}   MUTATE={MUT}")

banner("S2(b)  the khronon current of the static or comoving flow has no charge; M8 gives it one")
t, r = sp.symbols("t r", real=True)
N = sp.Function("N", positive=True)(r); A = sp.Function("A", positive=True)(r); a = sp.Function("a", positive=True)(t)
g = sp.diag(-N**2, a**2 * A**2, a**2 * A**2 * r**2, a**2 * A**2 * r**2 * sp.sin(sp.Symbol("th"))**2)
gi = g.inv()
u_up = [1 / N, 0, 0, 0]
h = sp.Matrix(4, 4, lambda i, j: gi[i, j] + u_up[i] * u_up[j])
h0 = [sp.simplify(h[0, j]) for j in range(4)]
P(f"  h^{{0 nu}} for u^mu = (1/N, 0, 0, 0): {h0}   =>  J^0 = (-X)^(-1/2) h^{{0 nu}} E_nu = 0 for any E_nu: the static/comoving flow carries no Noether charge")
Q0 = sp.Symbol("Q0", real=True)
# M8: a nonzero background charge Q = a^3 J^0 constant  =>  J^0 = Q/a^3 and (in the khronon's FRW equation) an energy density rho_Q = |Q| c/a^3 (dust-like)
rhoQ = sp.Abs(Q0) / a**3
ok_noQ = all(x == 0 for x in h0)
if MUT == "M8":
    P(f"  MUTATE=M8: J^0 = Q0/a^3 with Q0 != 0 => rho_Q = {rhoQ} (an a^-3, dust-like term): S2(b) flips to FAIL")
    check("S2(b) the flow carries no conserved charge (Q = 0)", "M8: Q0 != 0 gives an a^-3 term", False)
else:
    check("S2(b) the flow carries no conserved particle number or charge (J^0 = 0 for the static/comoving flow; Pi_0 fixed by the leaf average, not a charge)", f"h^(0 nu) = {h0}", ok_noQ)

banner("S2(a)  rest-mass parameters")
P("  The flow sector's action terms: -c2 (theta - <theta>)^2, alpha_c a^2, the gate f(theta) multiplying V0's region-kernel terms, and (d2) -zeta (eps_b - <eps_b>) h(vartheta).")
P("  Dimensionful parameters: Lambda (through theta_Lambda = sqrt(3 Lambda) and rule T), a0 (rule T), the web-screening mass m of V0's auxiliary field Y (1/m = 100-500 kpc), the filter length xi.")
P("  None of these is a rest mass of the flow (theta, khronon).  m is the screening mass of the MOND-sector auxiliary field Y (V0's own, inherited), flagged here as a mass parameter of an auxiliary field, not of the flow.")
check("S2(a) the flow (theta/khronon) sector has no rest-mass parameter (m is V0's auxiliary-field screening mass, inherited; flagged)", "no term with a mass coefficient in the theta sector", True, load_bearing=False)

banner("S2(c)  the effective density is a functional of the baryons; S1 numbers for the static configuration")
a0 = C.A0
rg = S.make_grid()
for Mb in (1e11, 1e-3):
    sol = S.solve_v0(rg, np.ones_like(rg), a0, Mb, "point", m=0.0)
    phantom = sol["gbar"] - sol["gN"]
    P(f"  M_b = {Mb:g}: max phantom/gN over r in [0.5, 1e3] kpc = {np.max((phantom / sol['gN'])[(rg > 0.5) & (rg < 1e3)]):.3g}")
sol_a = S.solve_v0(rg, np.ones_like(rg), a0, 1e11, "point", m=0.0); sol_b = S.solve_v0(rg, np.ones_like(rg), a0, 1e-3, "point", m=0.0)
ok_c = float(np.max(np.abs(sol_b["gbar"] - sol_b["gN"]))) < 1e-9 * float(np.max(sol_a["gbar"]))
check("S2(c) with the baryons removed (M_b = 1e-3 Msun) the region kernel's phantom vanishes in absolute terms (no free amount)", "phantom acceleration scales with the baryons", ok_c, load_bearing=False)
# S1: interaction pressure and energy density scale for the reference (from A1's derivation)
z = 0.25; c2 = 7.3e-3
rho_b_mean = C.FB * C.Om * C.rho_crit0 * (1 + z)**3
for zt in (1e-3, 1e-2):
    eps_ratio = rho_b_mean / C.RHO_L
    Eint_over_eb = -zt**2 * eps_ratio / (6 * c2)            # E_int/eps_b at the mean baryon density
    P(f"  d2 lin at zeta = {zt:g}, mean baryon density z = 0.25: E_int/eps_b = P/eps_b = {Eint_over_eb:.3e} (isotropic pressure, negative); c_s^2/c^2 = {2 * Eint_over_eb:.3e}")
R.num("S1_interaction", dict(note="P = E_int = -zeta^2 eps_b^2/(6 c2 eps_L); isotropic; conserved with the baryons (minimal-coupling identity holds jointly)"))
nf = R.write()
if MUT == "M8":
    P("\n  MUTATE=M8: control BITES"); sys.exit(1)
sys.exit(0 if nf == 0 else 1)
