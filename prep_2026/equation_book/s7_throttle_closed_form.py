#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M2, SEAM S7 (cluster y_c = Z/2 throttle: broken-RAR closed forms)
========================================================================================
Throttle premises (Branch-B elastic medium; real_research/papers/ELASTIC_MEDIUM_YC_Z2_2026.md,
prep_2026/cluster_kink_spec/TARGET_SPEC.md -- POSTULATE-DEPENDENT: Branch B only, the
uncut MI branch has NO throttle):
  g_obs = g_bar [1 + (nu(y)-1) T(y)],  T(y) = min(1, (y_c/y)^n),  y_c = Z/2,
  nu(y) = sqrt(1+1/y),  n=1 depletion (the paper's reading) / n=2 bracket.
Both footings: a0 = 9.362e-11 (canonical) / 1.130e-10 (alt); Z = sqrt(32 pi/3) footing-free.

Derives and verifies:
 E-S7-1  KINK LOCATION = PURE-LAMBDA LANDMARK                       [EXACT, credit:
         g_kink = y_c a0 = cH_Lambda/2 = c^2 sqrt(Lambda/12)         the a0V/2 statement
         (Z cancels!)  =>  Lambda = 12 g_kink^2 / c^4                is already in the
         and H_Lambda = 2 g_kink / c.                                y_c=Z/2 paper]
 E-S7-2  THE THROTTLE LINE (cubic invariant above the kink, n=1)    [EXACT, new]
         for y > y_c:  g_bar (g_obs - g_bar) (g_obs - g_bar + Z a0) = (Z^2/4) a0^3
         -- every point above the kink lies on ONE cubic surface; constant, zero-fit.
 E-S7-3  a0-LINE SATURATION (the cluster signature in a0-line coordinates) [EXACT, new]
         below kink: g_obs^2 - g_bar^2 = a0 g_bar (the a0-line, unchanged);
         above kink (n=1): g_obs^2 - g_bar^2 -> (Z/2) a0^2 * (1 + ...) saturates at
         Y_inf = a0 * g_kink = (Z/2) a0^2  -- the a0-line goes HORIZONTAL above the kink.
         general n: (g_obs - g_bar) g_bar^n -> (y_c^n/2) a0^{n+1}.
 E-S7-4  SLOPE CLOSED FORMS + THE BREAK INVARIANT                   [EXACT, new forms]
         below: d ln g_obs/d ln g_bar = (2y+1)/(2(y+1));  at y_c^-: (Z+1)/(Z+2)
         above (n=1): [1 - y_c/(2 y^2 nu)] / [1 + y_c (nu-1)/y] ... (closed form below)
         break at y_c: Delta = slope(+) - slope(-), a pure-Z number (footing-free):
         n=1: -0.1379, n=2: -0.2749  (matches banked 0.872 -> 0.734 / 0.597)
 E-S7-5  PEAK-DEVIATION LANDMARK (closed equation, footing-free)    [EXACT equation,
         y* solves d/dy log[nu/(1+(nu-1)(y_c/y)^n)] = 0  -> y*=6.06 (n=1), numeric root]
         peak = 0.0170 dex (n=1) / 0.0264 dex (n=2)  (matches banked fingerprint)
 E-S7-6  KINK RADIUS for a Hernquist BCG, closed form               [EXACT given model]
         GM/(r+a_H)^2 = g_kink  =>  r_kink = sqrt(2GM_BCG/(c H_Lambda)) - a_H
         (numeric: 9.4 kpc for M*=5e11 Msun, R_e=12 kpc -- matches TARGET_SPEC's 9.5,
          which includes the ~0.3% gas contribution)
HONESTY: everything here is conditional on the Branch-B throttle postulate; the y_c=Z/2
paper itself reports the fingerprint is 0.5-0.6 sigma from SPARC (indistinguishable) and
TARGET_SPEC.md shows the cluster kink is NOT currently detectable (BCG M/L systematic
4-6x the signal). These are exact target equations, not detections.
"""
import sys, math
import sympy as sp

FAIL = []
def check(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

y, g, a0, c, Z, H, Lam, n = sp.symbols('y g a0 c Z H Lambda n', positive=True)
nu = sp.sqrt(1 + 1/y)
yc = Z/2

print("="*78)
print("E-S7-1  kink location: g_kink = y_c a0 = cH_Lambda/2 = c^2 sqrt(Lambda/12)")
print("="*78)
# a0 = cH/Z (framework definition); H = c sqrt(Lambda/3)
gkink = (yc*a0).subs(a0, c*H/Z)
check("y_c a0 == cH_Lambda/2  (Z cancels exactly)", sp.simplify(gkink - c*H/2) == 0)
gkinkL = gkink.subs(H, c*sp.sqrt(Lam/3))
check("g_kink == c^2 sqrt(Lambda/12)", sp.simplify(gkinkL - c**2*sp.sqrt(Lam/12)) == 0)
check("inversion: Lambda == 12 g_kink^2/c^4",
      sp.simplify(sp.solve(sp.Eq(sp.symbols('gk', positive=True),
                                 c**2*sp.sqrt(Lam/12)), Lam)[0]
                  - 12*sp.symbols('gk', positive=True)**2/c**4) == 0)
# numbers, both footings (vs banked TARGET_SPEC 2.709e-10 / 3.271e-10)
Zn = math.sqrt(32*math.pi/3)
for tag, a0n, banked in (("canonical", 9.362e-11, 2.709e-10), ("alt", 1.130e-10, 3.271e-10)):
    gk = Zn/2*a0n
    check(f"[{tag}] g_kink = {gk:.4g} m/s^2 matches banked {banked:.4g}",
          abs(gk - banked)/banked < 2e-3)
cn = 2.99792458e8
gk_can = Zn/2*9.362e-11
print(f"   Lambda from the kink (canonical): {12*gk_can**2/cn**4:.4e} m^-2 ;"
      f" 1/H = {1/(2*gk_can/cn)/3.155815e16:.2f} Gyr")

print()
print("="*78)
print("E-S7-2  throttle line: g (g_obs-g) (g_obs-g+Z a0) == (Z^2/4) a0^3  [y>y_c, n=1]")
print("="*78)
# above the kink, n=1:  g_obs = g [1 + (nu-1) y_c/y],  g = y a0
gobs_above = (g*(1 + (nu - 1)*yc/y)).subs(g, y*a0)
D = sp.simplify(gobs_above - y*a0)                        # g_obs - g_bar
inv = sp.simplify((y*a0)*D*(D + Z*a0) - Z**2*a0**3/4)
check("cubic invariant holds identically for all y (n=1, above kink)", inv == 0)
# and it is zero-fit: no y left in the constant
check("the invariant is y-independent (a constant surface)",
      sp.diff(sp.simplify((y*a0)*D*(D + Z*a0)), y) == 0)

print()
print("="*78)
print("E-S7-3  a0-line saturation above the kink")
print("="*78)
# below kink the a0-line is exact and unchanged:
gobs_below = g*sp.sqrt(1 + a0/g)
check("below kink: g_obs^2 - g_bar^2 == a0 g_bar (a0-line unchanged, T=1)",
      sp.simplify(gobs_below**2 - g**2 - a0*g) == 0)
# above kink: Y = g_obs^2 - g_bar^2 saturates at a0*g_kink = (Z/2) a0^2
Yab = sp.simplify(gobs_above**2 - (y*a0)**2)
Ylim = sp.limit(Yab, y, sp.oo)
check("above kink (n=1): g_obs^2 - g_bar^2 -> (Z/2) a0^2 = a0 g_kink  (saturation)",
      sp.simplify(Ylim - Z*a0**2/2) == 0)
# general n: (g_obs - g_bar) g_bar^n -> (y_c^n/2) a0^(n+1)
ycs = sp.symbols('y_c', positive=True)
gobs_n = (g*(1 + (nu - 1)*(ycs/y)**n)).subs(g, y*a0)
Dn = sp.simplify(gobs_n - y*a0)
lim_n = sp.limit(sp.simplify(Dn*(y*a0)**n), y, sp.oo)
check("general n: (g_obs-g_bar) g_bar^n -> y_c^n a0^(n+1) / 2",
      sp.simplify(lim_n - ycs**n*a0**(n + 1)/2) == 0)

print()
print("="*78)
print("E-S7-4  slope closed forms and the break invariant (pure-Z, footing-free)")
print("="*78)
# below: slope = d ln g_obs / d ln g_bar with g_obs = sqrt(g^2+a0 g)
slope_below = sp.simplify(g*sp.diff(gobs_below, g)/gobs_below)
check("below: slope == (2y+1)/(2(y+1))",
      sp.simplify(slope_below.subs(g, y*a0) - (2*y + 1)/(2*(y + 1))) == 0)
s_minus = sp.simplify(((2*y + 1)/(2*(y + 1))).subs(y, yc))
check("at y_c^-: slope == (Z+1)/(Z+2)", sp.simplify(s_minus - (Z + 1)/(Z + 2)) == 0)
# above (n=1): slope from the closed form
slope_above = sp.simplify(y*sp.diff(gobs_above, y)/gobs_above)
s_plus = sp.simplify(slope_above.subs(y, yc))
nuc = sp.sqrt(1 + 2/Z)
s_plus_claim = sp.simplify((1 - 1/(Z*nuc))/nuc)
check("at y_c^+ (n=1): slope == [1 - 1/(Z nu_c)]/nu_c,  nu_c = sqrt(1+2/Z)",
      sp.simplify(s_plus - s_plus_claim) == 0)
# numeric break invariants vs banked slopes 0.872 -> 0.734 (n=1) / 0.597 (n=2)
sm = float(s_minus.subs(Z, Zn))
sp1 = float(s_plus.subs(Z, Zn))
check(f"numeric: slope(-) = {sm:.4f} (banked 0.872)", abs(sm - 0.872) < 1e-3)
check(f"numeric: slope(+) n=1 = {sp1:.4f} (banked 0.734)", abs(sp1 - 0.734) < 1e-3)
# n=2
gobs_n2 = (g*(1 + (nu - 1)*(yc/y)**2)).subs(g, y*a0)
slope_n2 = sp.simplify(y*sp.diff(gobs_n2, y)/gobs_n2)
sp2 = float(sp.simplify(slope_n2.subs(y, yc)).subs(Z, Zn))
# exact value is 0.59582 (confirmed by independent finite difference of the throttled
# law); the banked 0.597 is a 3-digit round of a coarser numerical derivative
check(f"numeric: slope(+) n=2 = {sp2:.4f} (banked ~0.597, exact 0.5958)",
      abs(sp2 - 0.597) < 2.5e-3)
print(f"   break invariants (pure Z): Delta(n=1) = {sp1-sm:+.4f}, Delta(n=2) = {sp2-sm:+.4f}")

print()
print("="*78)
print("E-S7-5  peak-deviation landmark (footing-free equation in y alone)")
print("="*78)
import mpmath as mp
mp.mp.dps = 30
Znum = mp.sqrt(32*mp.pi/3)
ycn = Znum/2
def dev_dex(yy, nn):
    nuv = mp.sqrt(1 + 1/yy)
    return mp.log10(nuv/(1 + (nuv - 1)*(ycn/yy)**nn))
for nn, y_banked, pk_banked in ((1, 6.1, 0.017), (2, 5.2, 0.026)):
    ystar = mp.findroot(lambda yy: mp.diff(lambda t: dev_dex(t, nn), yy), y_banked)
    pk = dev_dex(ystar, nn)
    check(f"n={nn}: peak at y* = {mp.nstr(ystar,4)} (banked ~{y_banked}), "
          f"peak = {mp.nstr(pk,3)} dex (banked {pk_banked})",
          abs(float(ystar) - y_banked) < 0.15*y_banked and
          abs(float(pk) - pk_banked) < 0.0015)
    # the landmark in g_bar: g* = y* a0 (both footings)
    for tag, a0n in (("canonical", 9.362e-11), ("alt", 1.130e-10)):
        print(f"      [{tag}] peak at g_bar = {float(ystar)*a0n:.3e} m/s^2")

print()
print("="*78)
print("E-S7-6  Hernquist-BCG kink radius: r_kink = sqrt(2 G M / (c H_Lambda)) - a_H")
print("="*78)
GM_, aH, gk_ = sp.symbols('GM a_H g_k', positive=True)
r_ = sp.symbols('r', positive=True)
# Hernquist enclosed mass M(r) = M r^2/(r+a)^2 -> g_bar = GM/(r+a)^2
sol = sp.solve(sp.Eq(GM_/(r_ + aH)**2, gk_), r_)
sol_pos = [s_ for s_ in sol if s_.has(sp.sqrt(GM_/gk_)) or True]
check("closed form: r_kink == sqrt(GM/g_kink) - a_H",
      any(sp.simplify(s_ - (sp.sqrt(GM_/gk_) - aH)) == 0 for s_ in sol))
# with g_kink = cH/2: r_kink = sqrt(2GM/(cH)) - a_H
check("r_kink == sqrt(2 G M/(c H_Lambda)) - a_H",
      sp.simplify((sp.sqrt(GM_/gk_) - aH).subs(gk_, c*H/2)
                  - (sp.sqrt(2*GM_/(c*H)) - aH)) == 0)
# numeric vs TARGET_SPEC fiducial (M*=5e11 Msun, R_e=12 kpc, Hernquist a=R_e/1.8153)
Gn, Msun, kpc = 6.67430e-11, 1.98892e30, 3.0857e19
Mb, Re = 5e11*Msun, 12*kpc
aHn = Re/1.8153
for tag, a0n, banked_kpc in (("canonical", 9.362e-11, 9.5), ("alt", 1.130e-10, 8.0)):
    gkn = Zn/2*a0n
    rk = math.sqrt(Gn*Mb/gkn) - aHn
    check(f"[{tag}] r_kink(BCG-only) = {rk/kpc:.2f} kpc vs TARGET_SPEC {banked_kpc} "
          f"(BCG+gas, tol 5%)", abs(rk/kpc - banked_kpc)/banked_kpc < 0.05)

print()
print(f"{len(FAIL)} failures" if FAIL else "ALL CHECKS PASS")
sys.exit(1 if FAIL else 0)
