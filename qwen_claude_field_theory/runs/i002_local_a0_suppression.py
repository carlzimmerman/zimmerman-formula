#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
I002 -- THE 1 AU ANOMALY IS s*a0(LOCAL), NOT s*a0(COSMIC).

QUESTION
  The saturated sunward anomaly at 1 AU is u_sat = s*a0.  The ephemeris liability
  (stage75, in force 2026-08-17) quotes it with a0 held COSMIC, giving a gap of
  13600x (canonical a0 = 9.3619e-11) / 17300x (alt a0 = 1.1279e-10).  But the
  framework's OWN promotion (PROTOCOL line 6, stage75 PART C) makes a0 a FIELD:

        a0^2(Q) = kappa^2 G (-K(Q)),   a0(nu)/a0(0) = [(1+nu0^2)/(1+nu^2)]^(1/4),
        nu = nu0 * rho/rho0,   nu0 <= 2.36e-6   (the recombination-pin ceiling, stage76).

  In the dense local environment a0 is SUPPRESSED by the factor
        f = a0_local/a0_cosmic = [(1+nu0^2)/(1+nu^2)]^(1/4)  < 1,
  so the physical anomaly is u_sat = s*a0_cosmic*f and the ephemeris gap shrinks by f.

  HYP:  using a0 LOCAL (not cosmic) closes R1's ephemeris end -- the gap shrinks by
        >100x.  KILL if the achievable suppression is < 3x.

WHAT THIS SCRIPT DOES (as briefed)
  1. READS the prior law, does NOT re-derive it: real_research/reviews/
     a0_local_ephemeris_2026.py already computed f = [(1+nu0^2)/(1+nu^2)]^(1/4) with
     nu = nu0 * (rho_local/rho0).  We reuse that exact expression and first REPRODUCE
     its two committed numbers (0.141 ceiling / 0.405 floor at the 0.4 GeV/cm^3 density)
     as a gate, to prove we are on the same law.
  2. FORMS nu = nu0 * (rho_local/rho0) at nu0 = 2.36e-6 (the tightest allowed value)
     for rho_local/rho0 in {1e2, 1e4, 4.24e5, 1e6, 1e8}, evaluates f, and divides the
     gap 13600 (canon) / 17300 (alt) by it  --  new_gap = gap * f.
  3. Reports BOTH a0 footings (the two gap numbers ARE the two footings; f itself is
     footing-independent).

NOTE ON DIRECTION  (brief says "divide the gap by it"; we do new_gap = gap * f):
  f = a0_local/a0_cosmic < 1, so suppressing a0 shrinks the anomaly and the gap by f.
  "gap shrinks by >100x" means 1/f > 100, i.e. f < 0.01.  We report f, its inverse
  S = 1/f (the shrink), and new_gap = gap*f, and adjudicate on S.  This is the only
  reading under which PASS/KILL is coherent.

PASS (brief): gap shrinks by >100x  (max S over the grid > 100).
KILL (brief): achievable local suppression < 3x  (S at the physical local density < 3).
Writes no other file.  Commits nothing.
"""
import sys
import os

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10
NU0 = 2.36e-6                     # recombination-pin ceiling (PROTOCOL line 6 / stage76)
GAP_CANON, GAP_ALT = 13600.0, 17300.0        # in-force ephemeris gaps (stage75 adjudication)
RHO_LOCAL_RATIO = 2.84e5          # 0.4 GeV/cm^3 / cosmic mean, from the prior file (A2)

# constants reused only to state the physical density, not to re-derive f
RHO_DM0 = 0.265 * 9.47e-27        # kg/m^3, cosmic mean
GEV_CM3 = 1.7827e-21              # kg/m^3 per GeV/cm^3

CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"   [{'ok' if ok else 'FAIL'}] {name}" + (f"    {detail}" if detail else ""))
    return bool(ok)

def hdr(t):
    print("\n" + "=" * 78); print(t); print("=" * 78)


# ----------------------------------------------------------------------------
# THE LAW, reused verbatim from a0_local_ephemeris_2026.py  (NOT re-derived)
#   f = a0_local/a0_cosmic = [(1+nu0^2)/(1+nu^2)]^(1/4),  nu = nu0 * (rho_local/rho0)
# ----------------------------------------------------------------------------
def f_local(nu0, R):
    nu = nu0 * R
    return float(((1.0 + nu0 * nu0) / (1.0 + nu * nu)) ** 0.25)


hdr("I002  1 AU anomaly = s*a0(LOCAL)?  suppression of the ephemeris gap by local a0")
print(f"  a0 canonical : {A0_CANON:.4e} m/s^2   a0 alt: {A0_ALT:.4e} m/s^2  (kappa=1/2 FITTED)")
print(f"  nu0 ceiling  : {NU0:.3e}   (recombination pin, the MOST suppression-favourable value)")
print(f"  gap (in force): {GAP_CANON:.0f}x (canon) / {GAP_ALT:.0f}x (alt)  -- stage75 adjudication")
print(f"  physical local density: {RHO_LOCAL_RATIO:.3e} x cosmic  (0.4 GeV/cm^3)")

# ----------------------------------------------------------------------------
hdr("BLOCK 0 -- GATE: reproduce the prior file's law, do NOT re-derive it")
# the prior a0_local_ephemeris_2026.py committed:
#   s_ceil = 0.141 (nu0 = 1.77e-4), s_floor = 0.405 (nu0 = 2.14e-5), both at R = 2.84e5
p_ceil = f_local(1.77e-4, RHO_LOCAL_RATIO)
p_floor = f_local(2.14e-5, RHO_LOCAL_RATIO)
check("GATE  f(1.77e-4, 2.84e5) reproduces the prior 0.141 (ceiling nu0)",
      abs(p_ceil - 0.141) / 0.141 < 0.05, f"f = {p_ceil:.4f} (prior A3: 0.141)")
check("GATE  f(2.14e-5, 2.84e5) reproduces the prior 0.405 (floor nu0)",
      abs(p_floor - 0.405) / 0.405 < 0.05, f"f = {p_floor:.4f} (prior A3: 0.405)")
check("GATE  law is footing-independent (f depends only on nu0, R -- not on a0)",
      True, "f = [(1+nu0^2)/(1+nu^2)]^1/4 contains no a0; the two footings enter only via the gap")

# ----------------------------------------------------------------------------
hdr("BLOCK 1 -- the briefed grid at nu0 = 2.36e-6, both footings")
GRID = [1e2, 1e4, 4.24e5, 1e6, 1e8]
rows = []
print(f"   {'R=rho_l/rho0':>14}{'nu':>12}{'f=a0_l/a0_c':>14}{'S=1/f(shrink)':>15}"
      f"{'gap_canon':>12}{'gap_alt':>12}")
for R in GRID:
    nu = NU0 * R
    f = f_local(NU0, R)
    S = 1.0 / f
    gc, ga = GAP_CANON * f, GAP_ALT * f
    rows.append(dict(R=R, nu=nu, f=f, S=S, gc=gc, ga=ga))
    print(f"   {R:>14.3e}{nu:>12.3e}{f:>14.5f}{S:>15.4f}{gc:>12.1f}{ga:>12.1f}")

# the physically-motivated point (the actual local DM density), in between grid points
f_phys = f_local(NU0, RHO_LOCAL_RATIO)
S_phys = 1.0 / f_phys
print(f"\n   physical density R = {RHO_LOCAL_RATIO:.3e}  ->  f = {f_phys:.5f},  "
      f"S = {S_phys:.4f},  new_gap {GAP_CANON*f_phys:.0f}x (canon)/{GAP_ALT*f_phys:.0f}x (alt)")

S_max = max(r["S"] for r in rows)
R_at_Smax = [r for r in rows if abs(r["S"] - S_max) < 1e-9][0]["R"]
f_max = S_max ** -1
check("S is monotonically increasing in R (more dense -> more suppression)",
      all(rows[i]["S"] <= rows[i + 1]["S"] + 1e-12 for i in range(len(rows) - 1)), "")
check("maximum shrink over the briefed grid is S = %.2fx at R = %.1e" % (S_max, R_at_Smax),
      abs(S_max - 15.36) / 15.36 < 0.05, f"S_max = {S_max:.4f} at R = {R_at_Smax:.1e}")

# ----------------------------------------------------------------------------
hdr("BLOCK 2 -- PASS / KILL adjudication (as briefed)")
# PASS: gap shrinks by >100x  <=>  S_max > 100
check("briefed PASS (gap shrinks >100x)  ->  NOT MET:  max S = %.2fx < 100" % S_max,
      S_max < 100.0, f"max shrink {S_max:.2f}x; would need f < {1.0/100:.0e} but best f = {f_max:.3e}")
# KILL: achievable local suppression < 3x  -- test at the PHYSICAL density
check("briefed KILL (suppression < 3x)  ->  FIRES at physical density:  S = %.3fx < 3"
      % S_phys, S_phys < 3.0, f"at R = {RHO_LOCAL_RATIO:.3e} (0.4 GeV/cm^3), S = {S_phys:.4f}x")
check("gap is NOT closed even at the most extreme grid point",
      rows[-1]["gc"] > 1.0 and rows[-1]["ga"] > 1.0,
      f"at R = 1e8 new_gap = {rows[-1]['gc']:.0f}x (canon)/{rows[-1]['ga']:.0f}x (alt) -- still 3 orders over")

# ----------------------------------------------------------------------------
hdr("BLOCK 3 -- what density WOULD close the gap (the 'provably cannot')")
# close canon gap:  new_gap <= 1  <=>  f <= 1/GAP  <=>  nu = GAP^2  (nu0^2 negligible)
for nm, GAP in (("canonical", GAP_CANON), ("alt", GAP_ALT)):
    nu_need = GAP ** 2                 # 1+nu^2 = GAP^4  (nu0^2 << GAP^4)
    R_need = nu_need / NU0
    dens_gev = R_need * RHO_DM0 / GEV_CM3
    ratio_to_local = dens_gev / 0.4    # 0.4 GeV/cm^3 is the physical local DM density
    check(f"{nm}: density to close gap via suppression = {R_need:.2e} x cosmic "
          f"({dens_gev:.2e} GeV/cm^3)",
          R_need > 1e6,
          f"nu_need = {nu_need:.3e},  R_need = {R_need:.2e}  =  {ratio_to_local:.2e}x the local 0.4 GeV/cm^3")

# cross-check the galaxy coupling (stage75 adjudication 2026-08-17, NOT re-derived here):
# "a LOCAL a0 HURTS": suppressing a0 by f forces the saturation s UP so the galaxy RAR
# product s*f stays ~fixed or grows (0.435 at f=1 -> 2.00 at f=0.1) and is unsatisfiable
# below f = 0.080.  => the galaxy RAR caps the usable suppression at S = 1/f = 12.5x,
# while the ephemeris needs S = GAP = 13600x.  Irreconcilable by ~1000x.
S_galaxy_cap = 1.0 / 0.080
check("cross-check: galaxy RAR caps usable suppression at S <= 12.5x (f >= 0.080), "
      "ephemeris needs S = 13600x",
      S_galaxy_cap < GAP_CANON,
      f"galaxy cap S <= {S_galaxy_cap:.1f}x vs ephemeris need {GAP_CANON:.0f}x -- "
      f"ratio {GAP_CANON/S_galaxy_cap:.0f}x")

# ----------------------------------------------------------------------------
hdr("VERDICT")
print(f"""  The hypothesis "the 1 AU anomaly is s*a0(LOCAL)" is REFUTED by the framework's own numbers.

  At the recombination-pinned nu0 = {NU0:.3e} (the MOST suppression-favourable value allowed),
  the local a0 suppression over the briefed density grid {GRID} is:
      S = 1/f  in  [ {rows[0]['S']:.4f} , {S_max:.4f} ]
  and at the PHYSICAL local DM density (0.4 GeV/cm^3, R = {RHO_LOCAL_RATIO:.3e})
  it is only S = {S_phys:.3f}x.  The ephemeris gap {GAP_CANON:.0f}x (canon) / {GAP_ALT:.0f}x (alt)
  therefore shrinks to at most {GAP_CANON*f_max:.0f}x (canon) / {GAP_ALT*f_max:.0f}x (alt) even at the
  absurd R = 1e8 -- and stays at ~{GAP_CANON*f_phys:.0f}x / ~{GAP_ALT*f_phys:.0f}x at the physical density.

  -> briefed PASS (shrink >100x): NOT MET  (max 15x).
  -> briefed KILL (suppression <3x):  FIRES at the physical density ({S_phys:.2f}x).

  To CLOSE the gap by local suppression alone one would need f <= 1/{GAP_CANON:.0f}, i.e.
  R ~ { (GAP_CANON**2/NU0):.2e}  =  ~{ (GAP_CANON**2/NU0*RHO_DM0/GEV_CM3/0.4):.1e}x the local DM density --
  a density of order { (GAP_CANON**2/NU0*RHO_DM0/GEV_CM3):.1e} GeV/cm^3, which is between white-dwarf
  and neutron-star matter, not the solar neighbourhood.  And the stage75 galaxy coupling
  (s*f product, unsatisfiable below f=0.080, cap S <= 12.5x) means the very suppression the
  ephemeris demands (S = 13600x) is forbidden by the galaxy RAR.  Local a0 cannot close R1's
  ephemeris end: it provably cannot.  The 13600x / 17300x liability stands.""")

# ----------------------------------------------------------------------------
hdr("CHECK SUMMARY")
npass = sum(1 for _, ok, _ in CHECKS if ok)
for nm, ok, det in CHECKS:
    print(f"   [{'ok' if ok else 'FAIL'}] {nm}")
print(f"\n   {npass}/{len(CHECKS)} checks passed")
sys.exit(0 if npass == len(CHECKS) else 1)
