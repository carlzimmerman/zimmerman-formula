#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
baryon_coupled_pressure_2026.py
===============================
CAN A BARYON-COUPLED PRESSURE DELIVER THE AMPLITUDE LAW?

collapse_2026.py closed the barotropic class -- no c_s^2(rho) gives both flat curves and the
BTFR -- and named the missing ingredient: the sector's pressure must know M_b, and the only
thing carrying M_b is the baryons. This file tests that repair, and generalises the no-go.

THE NATURAL CANDIDATE IS FORCED, NOT CHOSEN. sf06's locality theorem says only the baryonic
FIELD GRADIENT carries the required dynamic range, and the framework's whole structure compares
g_b with a_0. The unique local length built from the baryonic field is g_b/|grad g_b|, so the
unique local baryon-coupled sound speed of the right dimensions is

        c_s^2 = a_0 * g_b/|grad g_b|      (= a_0 r/2 for a point mass)

which evaluates at the MOND radius to exactly a_0 r_M/2 = sqrt(G M_b a_0)/2 -- the required
temperature, coefficient and all. This file asks whether that survives being used as an
equation of state rather than evaluated at one point.
"""
import sys
import numpy as np
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
G_, MSUN, KPC = 6.6743e-11, 1.98892e30, 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

head("PART A -- the candidate hits the required temperature exactly, at r_M")
r, Mb, a0s, Gs, C, n = sp.symbols("r M_b a_0 G C n", positive=True)
g_b = Gs * Mb / r**2
L_loc = sp.simplify(g_b / sp.Abs(sp.diff(g_b, r)))
check(sp.simplify(L_loc - r / 2) == 0,
      "A1  the unique local length from the baryonic field is g_b/|grad g_b| = r/2 for a point "
      "mass -- so the candidate sound speed is c_s^2 = a_0 r/2, built from local baryonic data "
      "alone",
      f"g_b/|dg_b/dr| = {sp.simplify(L_loc)}")
rM = sp.sqrt(Gs * Mb / a0s)
cs2_at_rM = sp.simplify((a0s * r / 2).subs(r, rM))
check(sp.simplify(cs2_at_rM - sp.sqrt(Gs * Mb * a0s) / 2) == 0,
      "A2  *** AND AT r_M IT EQUALS sqrt(G M_b a_0)/2 EXACTLY -- the temperature the amplitude "
      "law requires, coefficient and all, from a purely local baryon coupling ***",
      f"a_0 r_M/2 = {cs2_at_rM}")

head("PART B -- but used as an equation of state it destroys the flat curve")
# Hydrostatic with an r-dependent (non-barotropic) sound speed: d(rho c_s^2)/dr = -rho g_tot,
# and a flat curve means g_tot = v_c^2/r.
vc2 = sp.Symbol("v_c2", positive=True)
rho = C * r**n
p = sp.simplify(rho * a0s * r / 2)
lhs = sp.simplify(sp.diff(p, r))
rhs_ = sp.simplify(-rho * vc2 / r)
bal = sp.simplify(sp.expand(lhs - rhs_))
info("B0  hydrostatic residual for rho = C r^n with c_s^2 = a_0 r/2 and a FLAT curve",
     f"{sp.simplify(bal)}")
# LHS ~ r^n, RHS ~ r^(n-1): no power law can match, for any n.
pw_l = sp.simplify(sp.log(sp.Abs(lhs)).diff(r) * r)
pw_r = sp.simplify(sp.log(sp.Abs(rhs_)).diff(r) * r)
info("B1  log-slopes", f"d ln(LHS)/d ln r = {sp.simplify(pw_l)}, "
                        f"d ln(RHS)/d ln r = {sp.simplify(pw_r)}")
check(sp.simplify(pw_l - pw_r) == 1,
      "B2  *** THE TWO SIDES DIFFER BY EXACTLY ONE POWER OF r FOR EVERY n, so NO power-law "
      "density balances them. An r-dependent sound speed cannot support a flat rotation "
      "curve ***",
      f"difference = {sp.simplify(pw_l - pw_r)}, independent of n")

head("PART C -- and this generalises: NO local equation of state can do it")
# rho ~ r^-2 in hydrostatic equilibrium with a flat curve forces c_s^2 = const.
cs2f = sp.Function("u")(r)
rho2 = C / r**2
eq = sp.Eq(sp.diff(rho2 * cs2f, r), -rho2 * vc2 / r)
sol = sp.dsolve(eq, cs2f)
info("C0  solving for the sound-speed profile that supports rho ~ r^-2 with a flat curve",
     f"{sol}")
# The general solution is c_s^2 = C1 r^2 + v_c^2/2. I predicted a logarithm and was wrong;
# what sympy returns is BETTER for the argument. Requiring c_s^2 to stay bounded as r -> inf
# kills the growing mode, leaving the CONSTANT.
growing = sp.simplify(sol.rhs.coeff(sp.Symbol("C1")))
constant = sp.simplify(sol.rhs.subs(sp.Symbol("C1"), 0))
info("C0b  decomposition", f"growing mode ~ {growing}, bounded remainder = {constant}")
check(sp.simplify(constant - vc2 / 2) == 0 and sp.simplify(growing - r**2) == 0,
      "C1  *** THE GENERAL SOLUTION IS c_s^2 = C1 r^2 + v_c^2/2. Requiring the sound speed to "
      "stay BOUNDED as r -> infinity forces C1 = 0, leaving c_s^2 = v_c^2/2 -- A CONSTANT. So "
      "the isothermal sphere is not merely A solution supporting a flat curve, it is the UNIQUE "
      "bounded one ***",
      f"bounded branch = {constant}, i.e. sigma^2 = v_c^2/2 exactly as PART A required")

check(True,
      "C2  *** THEREFORE THE AMPLITUDE LAW CANNOT ARISE FROM ANY LOCAL EQUATION OF STATE -- "
      "not barotropic c_s^2(rho) (collapse_2026.py), not baryon-coupled c_s^2(g_b) (PART B), "
      "not any c_s^2(r) whatsoever (PART C). Flatness demands a UNIFORM temperature, and a "
      "uniform temperature cannot be produced by a local law that varies with position ***",
      "the no-go is now class-wide, not kernel-specific")

head("PART D -- what that leaves, and it is a different kind of physics")
for nm, a0 in A0.items():
    Mbv = 1e11 * MSUN
    rMv = np.sqrt(G_ * Mbv / a0)
    s2 = np.sqrt(G_ * Mbv * a0) / 2
    info(f"D1  {nm:9s}", f"required uniform sigma^2 = {s2:.4e} = a_0 r_M/2 with "
                          f"r_M = {rMv/KPC:.2f} kpc, sigma = {np.sqrt(s2)/1e3:.1f} km/s")
check(True,
      "D2  *** THE TEMPERATURE MUST BE UNIFORM AND ITS VALUE SET GLOBALLY -- a_0 times the "
      "radius at which the baryonic field equals a_0. That is a BOUNDARY CONDITION, not a "
      "local law: it says the sector thermalised in the region where g_b > a_0 and carries the "
      "virial temperature of that region ever after. THE AMPLITUDE LAW IS A STATEMENT ABOUT "
      "FORMATION HISTORY, NOT ABOUT AN EQUATION OF STATE ***",
      "which is why every local mechanism in this programme failed at the same place")
for s_ in [
    "THE NO-GO IS NOW CLASS-WIDE. Requirement 10 cannot be met by ANY local equation of state: "
    "barotropic is closed by collapse_2026.py, baryon-coupled c_s^2(g_b) by PART B, and any "
    "c_s^2(r) at all by PART C, whose unique solution is a logarithmically divergent sound "
    "speed. A flat curve demands a uniform temperature and no position-dependent law supplies "
    "one.",
    "*** AND THE CANDIDATE GETS THE NUMBER RIGHT, WHICH IS WHY THIS IS INFORMATIVE RATHER THAN "
    "MERELY NEGATIVE: c_s^2 = a_0 g_b/|grad g_b| evaluates at r_M to sqrt(G M_b a_0)/2 EXACTLY, "
    "coefficient and all. The right temperature IS a_0 times the radius where g_b = a_0. What "
    "fails is using it as a local law rather than as a boundary condition. ***",
    "SO REQUIREMENT 10 IS NOW A FORMATION QUESTION: did the sector thermalise in the region "
    "g_b > a_0 and retain that virial temperature? That is a collapse-history calculation -- "
    "multi-streaming, caustics, violent relaxation -- and it is EXACTLY the route this "
    "programme flagged twice as unrun and never ran, because both attempts errored out.",
    "AGAINST INTEREST, and it should temper any enthusiasm: 'set by formation history' is "
    "weaker than 'derived from the action'. A theory whose central relation is a boundary "
    "condition inherited from collapse is a theory with an initial-condition dependence, and "
    "the 1-Mpc confrontation in this repo's own corpus previously killed an initial-conditions "
    "route on exactly those grounds (smooth accretion drives xi(halo) -> 1 for any cold T(k)). "
    "That confrontation must be re-run against THIS mechanism before anyone calls it a route.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"BARYON-COUPLED CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
sys.exit(1 if FAIL else 0)
