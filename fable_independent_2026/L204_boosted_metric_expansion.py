#!/usr/bin/env python3
"""L204 -- THE BOOSTED METRIC EXPANSION: the preferred-frame gate, closed against the screening length Cassini already fixes.

THE SETUP. Work in the rest frame of a source moving at velocity w through the clock's frame. There the clock acquires a spatial
gradient, d_mu tau = s0 (1, w), and the unit normal n_mu = -d_mu tau/s is tilted by w. That tilt is the preferred-frame coupling and
alpha_1 is its coefficient.

STEP ONE, AND IT DECIDES THE REST. The background scalar depends only on the clock, chi = chibar(tau), so d_mu chibar = q d_mu tau is
PARALLEL to n_mu. The MOND invariant Y is the part of d chi orthogonal to n. Therefore Y vanishes in the boosted frame exactly as it
does in the rest frame: THE TILT GENERATES NO BACKGROUND MOND GRADIENT. Verified symbolically below to second order in w. Every
preferred-frame effect is therefore second order in the source's own perturbation, not first order in the boost.

STEP TWO. With that established there are two contributions, and both are computed:
  (a) the sector's own stress, boosted -- suppressed by how little of the sector sits inside the solar system;
  (b) the scalar's leakage into the solar system, which is what matter actually feels once the MOND coupling is present. That leakage
      is governed by the double-filter transmission T(x) = 1 - e^-x (1 + x + x^2/2), x = r/xi, the same screening whose length xi the
      Cassini measurement of gamma already bounds from below in this programme. So alpha_1 and gamma - 1 are controlled by the SAME
      length, and the question is which of the two bounds binds.
No literal-True checks."""
import numpy as np, sympy as sy, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL204 THE BOOSTED METRIC EXPANSION: does the tilt reach the solar system, and which bound binds\n" + "=" * 118)
# ---------- step one: the tilt generates no background MOND gradient ----------
wv, q = sy.symbols("w q", real=True); s0 = sy.Symbol("s_0", positive=True)
eta = sy.diag(-1, 1, 1, 1)
inv = sy.diag(-1, 1, 1, 1)
g = sy.Rational(1, 1)/sy.sqrt(1 - wv**2)
dtau = sy.Matrix([s0*g, s0*g*wv, 0, 0])                       # the clock's gradient in the moving source's frame
ssc = sy.sqrt(sy.simplify(-(dtau.T*inv*dtau)[0]))
n_low = -dtau/ssc
dchi = q*dtau                                                  # the background scalar depends only on the clock
n_up = inv*n_low
proj = inv + n_up*n_up.T
Yb = sy.simplify((dchi.T*proj*dchi)[0])
check("V1 [THE STRUCTURAL FACT: the tilt generates no background MOND gradient] because the background scalar depends only on the clock, its gradient is parallel to the clock's normal, so the MOND invariant Y vanishes in the boosted frame exactly as it does at rest -- at every order in the velocity, not just to leading order",
      sy.simplify(Yb) == 0, f"Y in the boosted frame simplifies to {Yb}, identically in w; the boost tilts the normal and the scalar's gradient together, so nothing orthogonal is generated")
sfac = sy.simplify(ssc)
check("V2 [and the clock rate is not merely nearly invariant, it is exactly invariant] s is a scalar built from the clock's gradient, so the boost leaves it untouched at every order in the velocity, not only to second order as one might expect from time dilation. Taken with V1 the entire background clock sector is blind to the motion, so there is nothing at background level for the preferred frame to act upon",
      sy.simplify(sfac - s0) == 0, f"s = {sfac} exactly, with no dependence on w whatsoever; the naive expectation of a second-order time dilation of {(370/2.998e5)**2:.2e} does not appear because s is a scalar")
# ---------- step two (a): the sector's own boosted stress ----------
AU = 1.496e13; PC = 3.086e18; MSUN = 1.989e33; RHO_DM = 0.4*1.783e-24; FRET = 0.135
R_SAT = 9.54*AU
M_sec = 4*np.pi/3*R_SAT**3*RHO_DM*FRET/MSUN
check("V3 [the sector's own stress] boosting the sector's rest-frame stress contributes at the level of its share of the mass inside the orbit, 6e-16 of the Sun, which is eleven orders below the bound on alpha_1",
      M_sec < 1e-10, f"sector mass inside Saturn's orbit = {M_sec:.2e} solar masses; the alpha_1 bound is about 1e-4")
# ---------- step two (b): the scalar's leakage, through the screening the programme already has ----------
def T(x): return 1 - np.exp(-x)*(1 + x + x**2/2)
XI_CASSINI = 0.03                                              # pc, the floor the Cassini measurement of gamma imposes in this programme
r_sat_pc = R_SAT/PC
print(f"    Saturn's orbit is {r_sat_pc:.2e} pc, so at the Cassini floor xi = {XI_CASSINI} pc the screening argument is x = r/xi = {r_sat_pc/XI_CASSINI:.2e}")
print("    xi [pc]      x = r/xi      transmission T(x)     implied alpha_1 scale")
rows = []
for xi in (5e-4, 1e-3, 3e-3, 1e-2, XI_CASSINI, 0.1):
    x = r_sat_pc/xi; t = T(x); rows.append((xi, x, t))
    print(f"    {xi:<12.0e} {x:.3e}     {t:.3e}            {t:.3e}")
t_cassini = T(r_sat_pc/XI_CASSINI)
check("V4 [the scalar's leakage at the length Cassini already requires] with the screening length at its Cassini floor the transmission into Saturn's orbit is 6e-10, so the scalar's contribution to the preferred-frame amplitude is six orders below the alpha_1 bound: the gate is cleared by the same length that the static test already fixes",
      t_cassini < 1e-6, f"T = {t_cassini:.2e} at xi = {XI_CASSINI} pc, against the alpha_1 bound of about 1e-4; the transmission falls as (r/xi)^3/6, so it is a steep function of the length")
# which bound binds
from scipy.optimize import brentq
xi_alpha = brentq(lambda L: T(r_sat_pc/L) - 1e-4, 1e-5, 1.0)
xi_gamma = brentq(lambda L: T(r_sat_pc/L) - 2.3e-5, 1e-5, 1.0)
check("V5 [WHICH BOUND BINDS, computed] the preferred-frame bound requires a screening length above 5e-4 pc while the static Cassini bound on gamma requires above 9e-4 pc: the static test is the more demanding of the two by a factor of two, so alpha_1 is satisfied automatically wherever gamma is, and the programme's existing floor of 0.03 pc clears both by more than an order of magnitude in length",
      xi_alpha < xi_gamma < XI_CASSINI, f"alpha_1 needs xi > {xi_alpha:.2e} pc; gamma needs xi > {xi_gamma:.2e} pc; the programme's floor is {XI_CASSINI} pc, which exceeds the binding one by a factor {XI_CASSINI/xi_gamma:.0f}")
check("V6 [THE GATE] taking the two contributions together -- the sector's boosted stress at 1e-15 and the scalar's leakage at 6e-10, against a bound of 1e-4 -- the preferred-frame gate is cleared, and it is cleared by structure rather than by tuning: the tilt generates no background MOND gradient at all, and what leakage remains is screened by the same length the static test already fixes",
      max(M_sec, t_cassini) < 1e-6, f"the larger of the two contributions is {max(M_sec, t_cassini):.2e}, which is {1e-4/max(M_sec, t_cassini):.0e} times below the bound")
print("    READING: the gate is closed, and the reason is the structural fact in V1. A boost tilts the clock's normal and the background scalar's gradient TOGETHER, because\n"
      "    the scalar depends on the clock alone, so no orthogonal gradient is generated and there is no first-order preferred-frame coupling to screen. What remains is the\n"
      "    scalar's ordinary leakage into the solar system, and that is governed by the same screening length the Cassini measurement of gamma already bounds -- more tightly\n"
      "    than the preferred-frame measurement does. This is why the earlier action died and this one does not: there the clock was coupled to matter directly.\n"
      "    LIMITS: the leakage estimate assumes the preferred-frame amplitude is controlled by the same double-filter transmission as the static one, which is the same scalar\n"
      "    reaching the same place but is an assumption rather than a derivation; the screening floor 0.03 pc is this programme's own; the sector's local density is the standard\n"
      "    0.4 GeV/cm^3 scaled by the retained fraction; no full post-Newtonian parameter is extracted from a metric expansion, and none is claimed to be.")
json.dump(dict(Y_boosted=str(Yb), sector_mass=float(M_sec), transmission_at_cassini=float(t_cassini),
               xi_needed_alpha1=float(xi_alpha), xi_needed_gamma=float(xi_gamma), xi_floor=XI_CASSINI,
               rows=[[float(a), float(b), float(c)] for a, b, c in rows]), open("L204_results.json", "w"), indent=1)
print(f"\nL204 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
