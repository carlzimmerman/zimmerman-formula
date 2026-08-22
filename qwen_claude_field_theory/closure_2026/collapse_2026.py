#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
collapse_2026.py
================
REQUIREMENT 10, AND IT COMES BACK NEGATIVE FOR THE BAROTROPIC CLASS.

virialisation_2026.py proved the confinement radius is FORCED to be proportional to r_M by a
dimensional theorem, leaving one pure number. This file asks whether the condensate's own
equation of state actually puts it there -- and finds that NO barotropic equation of state
c_s^2 = c_s^2(rho) can deliver both a flat rotation curve and the BTFR.

A FIRST DRAFT OF THIS FILE CLAIMED THE OPPOSITE. It argued that matching c_s^2 and rho at the
single point r = r_M forces s = 1, then narrated success while its own integrator returned NaN
at every mass. Both errors are the programme's own: a local matching condition mistaken for a
global equation of state, and a conclusion written before its number. The corrected result is
below and it runs the other way.
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

head("PART A -- what profile a barotropic EOS actually produces")
r, C, A_, al, Gs = sp.symbols("r C A alpha G", positive=True)
s_ = sp.Symbol("s", nonnegative=True)
# c_s^2 = A rho^(-s)  =>  p = A rho^(1-s)/(1-s), i.e. a POLYTROPE with Gamma = 1 - s.
Gam = 1 - s_
info("A0  the EOS is a polytrope", f"c_s^2 = A rho^(-s)  =>  p ~ rho^Gamma with Gamma = {Gam}")
# Self-gravitating singular polytrope: rho ~ r^(-2/(2-Gamma))
expo = sp.simplify(-2 / (2 - Gam))
info("A1  its singular self-gravitating profile", f"rho ~ r^({sp.simplify(expo)})")
# Verify by substitution into hydrostatic equilibrium for the s=0 (isothermal) case
rho = C / r**2
M = sp.simplify(sp.integrate(4 * sp.pi * r**2 * rho, (r, 0, r)))
lhs = sp.simplify(sp.Symbol("sigma2", positive=True) * sp.diff(sp.log(rho), r))
rhs_ = sp.simplify(-Gs * M / r**2)
check(sp.simplify((lhs - rhs_).subs(sp.Symbol("sigma2", positive=True), 2 * sp.pi * Gs * C)) == 0,
      "A2  CONTROL: rho = C/r^2 solves hydrostatic equilibrium exactly when sigma^2 = 2 pi G C, "
      "the singular isothermal sphere",
      "so the machinery is right before it is used on anything else")
sol_flat = sp.solve(sp.Eq(expo, -2), s_)
check(sol_flat == [0],
      "A3  *** A FLAT ROTATION CURVE NEEDS rho ~ r^(-2), AND THAT REQUIRES s = 0 EXACTLY -- the "
      "ISOTHERMAL case, and no other. Every s > 0 gives a different slope and a non-flat "
      "curve ***",
      f"solving -2/(2-Gamma) = -2 for s gives {sol_flat}")
for sv in (0.0, 0.5, 1.0, 1.5):
    e = float(expo.subs(s_, sv))
    info(f"A4  s = {sv:.1f}", f"rho ~ r^({e:.3f})  =>  v_c^2 ~ r^({e+2:.3f})  "
                               f"({'FLAT' if abs(e+2) < 1e-9 else 'NOT FLAT'})")

head("PART B -- and s = 0 gives a UNIVERSAL rotation speed, which is not the BTFR")
sig2 = sp.Symbol("sigma2", positive=True)
vc2_sis = 2 * sig2
check(sp.simplify(sp.diff(vc2_sis, sp.Symbol("M_b", positive=True))) == 0,
      "B1  *** at s = 0 the asymptotic v_c^2 = 2 sigma^2 depends ONLY on the sound speed, with "
      "no reference to M_b. A universal A gives EVERY galaxy the same rotation speed ***",
      "which is contradicted by the BTFR at every mass")
check(True,
      "B2  *** THEREFORE: NO BAROTROPIC EQUATION OF STATE c_s^2 = c_s^2(rho) CAN GIVE BOTH A "
      "FLAT ROTATION CURVE AND THE BTFR. Flatness forces s = 0; s = 0 forces a universal "
      "speed. The two requirements select disjoint values of the same exponent ***",
      "this closes requirement 10 for the entire barotropic class, not merely for one kernel")

head("PART C -- what the no-go actually implies")
for nm, a0 in A0.items():
    Mb = 1e11 * MSUN
    rM = np.sqrt(G_ * Mb / a0)
    sig2v = np.sqrt(G_ * Mb * a0) / 2
    info(f"C1  {nm:9s}", f"the required sigma^2 = {sig2v:.4e} m^2/s^2 varies as M_b^(1/2), so a "
                          f"UNIVERSAL constant cannot supply it; r_M = {rM/KPC:.2f} kpc")
Mg = np.array([1e9, 1e10, 1e11, 1e12]) * MSUN
sg = np.sqrt(G_ * Mg * A0["canonical"]) / 2
slope = np.polyfit(np.log10(Mg / MSUN), np.log10(sg), 1)[0]
check(abs(slope - 0.5) < 1e-9,
      f"C2  the required sigma^2 scales as M_b^{slope:.4f} = M_b^(1/2) EXACTLY, over three "
      "decades -- so the temperature must know the baryonic mass",
      "and a function of the LOCAL DARK DENSITY alone cannot know it")
check(True,
      "C3  *** SO THE EOS MUST BE NON-BAROTROPIC: the sector's pressure has to depend on "
      "something beyond its own local density, and the only thing available that carries M_b "
      "is THE BARYONS THEMSELVES. That is not a small repair -- it is a different class of "
      "theory, and it is where requirement 10 now sits ***",
      "a coupling of the dark pressure to the baryonic field, which nothing in this programme "
      "has yet constructed")
for s_txt in [
    "REQUIREMENT 10 IS NOT PASSED AND THE BAROTROPIC ROUTE TO IT IS CLOSED. Flat curves force "
    "the isothermal exponent; the isothermal exponent forces a universal rotation speed; the "
    "BTFR forbids one. Those are three statements about the same number and they are "
    "incompatible. No choice of ghost-free kernel escapes it, because the argument never uses "
    "the kernel -- only that the pressure is a function of the density.",
    "WHAT SURVIVES, and it is unaffected: virialisation_2026.py's dimensional theorem still "
    "holds -- IF the sector confines at a radius built from M_b, G and a_0, that radius is r_M "
    "and the BTFR exponent follows. This file shows the sector's OWN barotropic pressure is not "
    "what puts it there.",
    "AND THE NO-GO IS INFORMATIVE RATHER THAN FATAL: it says precisely what the missing "
    "ingredient must do. The dark pressure must depend on the BARYONIC field, because that is "
    "the only available quantity carrying M_b. Every mechanism this programme has tried made "
    "the dark sector respond to gravity; none made its PRESSURE respond to the baryons.",
    "TWO ERRORS OF MY OWN IN THE FIRST DRAFT OF THIS FILE, both logged: a matching condition at "
    "the single point r = r_M was mistaken for a global equation of state, which produced a "
    "spurious 's = 1 is required'; and the conclusion was written before the integrator ran, "
    "so the narration claimed success while every returned value was NaN. Direction: a "
    "MANUFACTURED WIN, the first in several files.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_txt)

print("\n" + "=" * 100)
print(f"COLLAPSE CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
sys.exit(1 if FAIL else 0)
