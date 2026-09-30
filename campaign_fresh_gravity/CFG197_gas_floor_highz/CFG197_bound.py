#!/usr/bin/env python3
"""CFG197 -- the gas-floor lemma (phase 1, pure mathematics: no data, no M_dyn, no velocity).

Claim.  For an algebraic law g_obs = nu(g_bar/a0) g_bar, write x = g_star(r)/a0 and mu = g_gas(r)/g_star(r) >= 0 at the radius r.
The predicted ratio of the dynamical to the stellar acceleration (= M_dyn(<r)/M_star(<r) in spherical-equivalent units) is
      F(mu; x) = g_obs/g_star = (1 + mu) nu((1 + mu) x) = Phi((1 + mu) x)/x,        Phi(y) = y nu(y)  (= g_obs/a0).
  L0  dF/dmu = Phi'((1 + mu) x).  So F is non-decreasing in mu for every x > 0 iff Phi is non-decreasing on (0, inf), and then
      F(mu; x) >= F(0; x) = nu(x): the gas-free prediction is a FLOOR for ANY unknown gas amount.  For a general law the floor is
      inf_{y >= x} Phi(y)/x, which can be < nu(x).
  L1  P2 (nu = sqrt(1 + 1/y)): Phi = sqrt(y^2 + y), Phi' = (2y + 1)/(2 sqrt(y^2 + y)) > 1 > 0.
  L2  nu_mono (FP1 / L340): Phi = y + h(y), h' = max(h_RAR', 0.05 H_P/(y + Y_P)) > 0, so Phi' > 1.  Checked on the committed table.
  L3  Corollary (the record's own L340 A1 health condition C_L = Phi' - 1 > 0): F(mu; x) >= nu(x) + mu.  Holds for P2 and nu_mono;
      nu_RAR satisfies L0 (Phi' > 0) but NOT the corollary (its phantom falls past Y_P).  Newton: F = 1 + mu exactly.
  L4  The M_star rescaling each law requires: s_req = Phi^-1(x R)/x (R the observed ratio); closed forms for Newton and P2; s_req
      increases with x, so at fixed data the rival a0 = a0 E(z) (smaller x) ALWAYS requires a smaller s_req than the flat law:
      the floor can single out the rival, never the flat law (the flat law can only lose together with the rival, or to Newton).
  L5  Where it fails: a law whose boost switches off above a threshold, h(y) = 1/(1 + (y/y_c)^n): Phi'(y_c) = 1 - n/(4 y_c) < 0 for
      n > 4 y_c; then adding gas LOWERS the predicted ratio and the nu(x) floor is not a bound.
Premises (declared, not derived): the algebraic relation holds locally at r (no external field, no non-local phantom correction);
the gas's own radial pull at r is non-negative (g_gas(r) >= 0: exact in spherical symmetry; for a disc it fails only for a gas
distribution with a central depression, e.g. a ring outside r); the stellar term g_star(r) is computed in a declared geometry.
Run: python3 campaign_fresh_gravity/CFG197_gas_floor_highz/CFG197_bound.py   (about 1-3 s)
"""
import os, sys, math, builtins
import numpy as np
import sympy as sp

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)          # the committed CFG4_common is imported with MUTATE unset (read-only)
try:
    import CFG4_common as K
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut

LINES, CHECKS = [], []


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


def check(name, detail, ok, load_bearing=True):
    CHECKS.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")


def banner(s):
    P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)


P(__doc__.split("Run: python3")[0].strip())

x, mu, y, s, R, n, yc = sp.symbols("x mu y s R n y_c", positive=True)
nu = sp.Function("nu")

# ============================================================================================================ L0
banner("L0  GENERAL: dF/dmu = Phi'((1 + mu) x) for an arbitrary kernel nu")
F = (1 + mu) * nu((1 + mu) * x)
Phi = y * nu(y)
dF = sp.diff(F, mu).doit()
dPhi_at = sp.diff(Phi, y).subs(y, (1 + mu) * x).doit()
diff0 = sp.simplify(dF - dPhi_at)
P(f"  dF/dmu            = {dF}")
P(f"  Phi'((1+mu)x)     = {dPhi_at}")
check("L0a dF/dmu - Phi'((1 + mu) x) = 0 identically (symbolic, nu arbitrary)", f"difference = {diff0}", diff0 == 0)
F0 = F.subs(mu, 0)
check("L0b F(0; x) = nu(x) (the gas-free prediction)", f"F(0) = {F0}", sp.simplify(F0 - nu(x)) == 0)
P("  => if Phi' > 0 on (0, inf), F(mu) >= F(0) = nu(x) for every mu >= 0 and x > 0 (monotone in mu).  Conversely, if Phi'(y0) < 0,")
P("     take x = y0: F decreases for small mu > 0, so nu(x) is not a floor.  The general floor is inf_{y >= x} Phi(y)/x.")

# ============================================================================================================ L1
banner("L1  P2: nu = sqrt(1 + 1/y)")
nuP2 = sp.sqrt(1 + 1 / y)
PhiP2 = sp.simplify(y * nuP2)
id_sq = sp.simplify(PhiP2 ** 2 - (y ** 2 + y))
dPhiP2 = sp.simplify(sp.diff(sp.sqrt(y ** 2 + y), y))
num, den = sp.fraction(sp.together(dPhiP2))
check("L1a Phi_P2 = sqrt(y^2 + y) for y > 0", f"Phi^2 - (y^2 + y) = {id_sq}; Phi = {PhiP2}", id_sq == 0)
check("L1b Phi_P2' = (2y + 1)/(2 sqrt(y^2 + y)) > 0 for y > 0 (numerator and denominator positive)",
      f"Phi' = {dPhiP2};  numerator {num} positive: {num.is_positive};  denominator {den} positive: {den.is_positive}",
      bool(num.is_positive) and bool(den.is_positive))
b = sp.expand((2 * y + 1) ** 2 - 4 * (y ** 2 + y))
check("L1c Phi_P2' > 1 (the record's C_L > 0): (2y + 1)^2 - 4(y^2 + y) = 1 > 0", f"= {b}", b == 1)
dnuP2 = sp.simplify(sp.diff(nuP2, y))
check("L1d nu_P2 is strictly decreasing (so a larger a0 raises the floor): dnu/dy < 0", f"dnu/dy = {dnuP2}", bool((-dnuP2).is_positive))

# ============================================================================================================ L2
banner("L2  nu_mono (FP1's committed construction, exec'd read-only through CFG4_common)")
# symbolic: h' = Max(h_RAR', phi_floor) with phi_floor = 0.05 H_P/(y + Y_P) > 0
HP, YP = sp.symbols("H_P Y_P", positive=True)
u = sp.Symbol("u", nonnegative=True)
phi_fl = sp.Rational(1, 20) * HP / (y + YP)
# h' = Max(h_RAR', phi_fl).  Two exhaustive cases for h_RAR' = phi_fl + u (above the floor) or phi_fl - u (below it), u >= 0:
case_above = sp.Max(phi_fl + u, phi_fl) - phi_fl
case_below = sp.Max(phi_fl - u, phi_fl) - phi_fl
P("  h' = Max(h_RAR', 0.05 H_P/(y + Y_P)).  Case h_RAR' = floor + u:  h' - floor = " + str(case_above)
  + ";   case h_RAR' = floor - u:  h' - floor = " + str(case_below) + "   (u >= 0)")
dPhi_mono_min = 1 + phi_fl
check("L2a in both exhaustive cases h' - floor >= 0, and the floor 0.05 H_P/(y + Y_P) > 0, so Phi' = 1 + h' >= 1 + floor > 1",
      f"case above: {case_above} (nonnegative: {case_above.is_nonnegative}); case below: {case_below}; floor positive: "
      f"{bool(phi_fl.is_positive)};  Phi' >= {dPhi_mono_min}",
      bool(case_above.is_nonnegative) and case_below == 0 and bool(phi_fl.is_positive))
# the RAR phantom's peak (the constants of the floor), from sympy
sq = sp.sqrt(y)
h_rar = y / (sp.exp(sq) - 1)
YP_num = float(sp.nsolve(sp.diff(h_rar, y), y, 2.5))
HP_num = float(h_rar.subs(y, YP_num))
check("L2b the RAR phantom's peak from sympy equals FP1's committed constants (Y_P, H_P)",
      f"sympy Y_P = {YP_num:.6f}, H_P = {HP_num:.6f};  FP1 Y_P = {K.Y_PEAK_RAR:.6f}", abs(YP_num - K.Y_PEAK_RAR) < 1e-4, load_bearing=False)
# numerics on the committed table (the kernel the record actually uses)
yy = np.logspace(-12, 12, 24001)
PhiM = yy * K.nu_mono(yy)
dmin = float(np.min(np.diff(PhiM) / np.diff(yy)))
check("L2c the committed nu_mono table: Phi = y nu_mono(y) is strictly increasing on y = 1e-12..1e12 (24001 log points; "
      "min secant slope > 0)", f"min secant slope dPhi/dy = {dmin:.6f}", dmin > 0)
yq = np.logspace(-6, 3, 4001)
e_ = 1e-5
CLm = ((yq * (1 + e_)) * K.nu_mono(yq * (1 + e_)) - (yq * (1 - e_)) * K.nu_mono(yq * (1 - e_))) / (2 * yq * e_) - 1.0
check("L2d the committed table satisfies the corollary condition C_L = Phi' - 1 > 0 on y = 1e-6..1e3 (FP1 B4's resolvable range)",
      f"min C_L = {CLm.min():+.3e}", CLm.min() > 0)

# ============================================================================================================ reference kernels
banner("REFERENCE  Newton and nu_RAR")
check("R1 Newton: Phi = y, Phi' = 1 > 0; F(mu) = 1 + mu exactly (floor 1)", "trivial", True, load_bearing=False)
# nu_RAR: Phi = s^2/(1 - e^-s), s = sqrt(y); dPhi/ds = s (2 - (2 + s) e^-s)/(1 - e^-s)^2; sign <- g(s) = 2 e^s - 2 - s
gS = 2 * sp.exp(s) - 2 - s
PhiR_s = s ** 2 / (1 - sp.exp(-s))
dPhiR_ds = sp.simplify(sp.diff(PhiR_s, s))
target = s * (2 - (2 + s) * sp.exp(-s)) / (1 - sp.exp(-s)) ** 2
id_r = sp.simplify(dPhiR_ds - target)
g0, gprime = gS.subs(s, 0), sp.diff(gS, s)
check("R2 nu_RAR (reference only): dPhi/ds = s(2 - (2 + s)e^-s)/(1 - e^-s)^2 and 2 - (2 + s)e^-s = e^-s g(s), g(s) = 2e^s - 2 - s: "
      "g(0) = 0 and g'(s) = 2e^s - 1 > 0, so Phi' > 0 (L0 holds for nu_RAR)",
      f"identity residual {id_r}; g(0) = {g0}; g'(s) = {gprime}", id_r == 0 and g0 == 0, load_bearing=False)
yr = np.logspace(-6, 3, 4001)
CLr = ((yr * (1 + e_)) * K.nu_rar(yr * (1 + e_)) - (yr * (1 - e_)) * K.nu_rar(yr * (1 - e_))) / (2 * yr * e_) - 1.0
check("R3 nu_RAR violates the corollary: C_L < 0 somewhere (its phantom decreases past Y_P), so F(mu) >= nu(x) + mu "
      "fails for nu_RAR although F(mu) >= nu(x) holds", f"min C_L = {CLr.min():+.4f} at y = {yr[np.argmin(CLr)]:.2f}", CLr.min() < 0,
      load_bearing=False)

# ============================================================================================================ L3 numeric
banner("L3  NUMERIC CONFIRMATION: min over the gas amount mu of the predicted ratio equals nu(x) (and >= nu(x) + mu)")
mus = np.concatenate([[0.0], np.logspace(-4, 3, 701)])
xs = np.logspace(-4, 4, 161)
worst = {}
for name, f in (("P2", K.nu_p2), ("nu_mono", K.nu_mono)):
    Fm = (1 + mus[None, :]) * f((1 + mus[None, :]) * xs[:, None])
    floor_ok = float(np.min(Fm.min(axis=1) / f(xs) - 1.0))
    cor_ok = float(np.min(Fm - (f(xs)[:, None] + mus[None, :])))
    worst[name] = (floor_ok, cor_ok)
    check(f"L3 {name}: min_mu F(mu; x)/nu(x) - 1 >= -1e-12 on x = 1e-4..1e4, mu = 0..1e3; and F - (nu(x) + mu) >= -1e-9",
          f"min ratio - 1 = {floor_ok:+.2e};  min F - (nu + mu) = {cor_ok:+.2e}", floor_ok >= -1e-12 and cor_ok >= -1e-9)

# ============================================================================================================ L4
banner("L4  THE REQUIRED M_STAR RESCALING s_req, AND THE STRUCTURAL ASYMMETRY BETWEEN THE FLAT LAW AND THE RIVAL")
P("  If the true stellar mass is s M_star: x -> s x and the observed ratio R -> R/s.  The law needs R/s >= nu(s x), i.e. Phi(s x) <= x R,")
P("  so s <= s_req = Phi^-1(x R)/x.  log s_req < 0 means M_star must be LOWERED (overestimated) for the law to survive with ANY gas.")
sN = R
PhiP2_of = lambda v: sp.sqrt(v ** 2 + v)
sP2 = (sp.sqrt(1 + 4 * x ** 2 * R ** 2) - 1) / (2 * x)
chk = sp.simplify(PhiP2_of(sP2 * x) / x - R)
check("L4a P2 closed form s_req = (sqrt(1 + 4 x^2 R^2) - 1)/(2x) solves Phi(s x)/x = R; Newton s_req = R",
      f"residual {chk}", chk == 0)
ds_dx = sp.simplify(sp.diff(sP2, x))
num4, den4 = sp.fraction(sp.together(ds_dx))
xs4 = np.logspace(-4, 4, 81)
Rs4 = np.logspace(-1, 2, 61)
f_ds = sp.lambdify((x, R), ds_dx, "numpy")
min_ds = float(np.min(f_ds(xs4[:, None], Rs4[None, :])))
check("L4b ds_req/dx > 0 for P2 (so the rival, x_rival = x_flat/E(z) < x_flat, always needs a SMALLER s_req than the flat law at the "
      "same data): symbolic derivative, and its minimum on x = 1e-4..1e4, R = 0.1..100",
      f"ds/dx = {ds_dx};  min on grid = {min_ds:.3e}", min_ds > 0)
lim0 = sp.limit(sP2 / (x * R ** 2), x, 0)
limI = sp.limit(sP2 - R, x, sp.oo)
check("L4c P2 limits: s_req -> x R^2 (deep regime; so s_req scales as 1/a0 and the rival/flat ratio is 1/E(z)) and s_req -> R "
      "(Newtonian regime; the laws coincide)", f"lim s/(x R^2) as x->0 = {lim0};  lim (s - R) as x->oo = {limI}", lim0 == 1 and limI == 0)
chk1 = sp.simplify(sP2.subs(R, 1))
P(f"  Planted galaxy R = 1 (M_dyn = M_star): Newton s_req = 1 (on the floor); P2 s_req = {chk1} < 1 for every x > 0.")
vals = [float(chk1.subs(x, v)) for v in (0.01, 0.1, 1.0, 10.0, 100.0)]
check("L4d a planted galaxy with M_dyn/M_star = 1 lies BELOW the P2 floor at every x (s_req < 1), i.e. it is flagged against both "
      "the flat law and the rival; Newton's s_req is exactly 1", f"P2 s_req at x = 0.01, 0.1, 1, 10, 100: {[round(v, 5) for v in vals]}",
      all(v < 1 for v in vals))

# ============================================================================================================ L5
banner("L5  WHERE THE BOUND FAILS: a law whose boost switches off above a threshold (Phi non-monotone)")
h_sw = 1 / (1 + (y / yc) ** n)
Phi_sw = y + h_sw
dPhi_sw_at = sp.simplify(sp.diff(Phi_sw, y).subs(y, yc))
check("L5a switch law h(y) = 1/(1 + (y/y_c)^n) (nu = 1 + h/y): Phi'(y_c) = 1 - n/(4 y_c), negative for n > 4 y_c",
      f"Phi'(y_c) = {dPhi_sw_at}", sp.simplify(dPhi_sw_at - (1 - n / (4 * yc))) == 0)
nv, ycv = 8, 1.0
nu_sw = lambda v: 1.0 + (1.0 / (1.0 + (np.asarray(v, float) / ycv) ** nv)) / np.asarray(v, float)
xsw = np.linspace(0.5, 1.2, 71)
viol = []
for xv in xsw:
    Fm = (1 + mus) * nu_sw((1 + mus) * xv)
    i = int(np.argmin(Fm))
    viol.append((xv, float(nu_sw(xv)), float(Fm[i]), float(mus[i])))
vmax = max(viol, key=lambda t: t[1] / t[2])
P(f"  n = {nv}, y_c = {ycv}: Phi'(y_c) = {1 - nv / (4 * ycv):+.2f}.  Largest violation of the nu(x) 'floor':")
P(f"    x = {vmax[0]:.3f}: nu(x) = {vmax[1]:.4f}, but with gas mu = {vmax[3]:.3f} the predicted ratio is {vmax[2]:.4f} "
  f"({math.log10(vmax[2] / vmax[1]):+.3f} dex)")
nviol = sum(1 for t in viol if t[2] < t[1] * (1 - 1e-9))
check("L5b the switch law violates the nu(x) floor for x below the end of Phi's decreasing stretch (adding gas lowers the predicted ratio), so the gas-floor "
      "test does NOT apply to such laws; the general floor inf_{y >= x} Phi(y)/x must be used instead",
      f"{nviol} of {len(xsw)} x values in [0.5, 1.2] violate it; worst {math.log10(vmax[2] / vmax[1]):+.3f} dex", nviol > 0)
P("  Record relevance: P2 and nu_mono satisfy L0 and the corollary (both pass the record's C_L > 0 health condition, FP1 B4);")
P("  any candidate whose boost is switched off by the baryons above a threshold must first be checked for a decreasing stretch of")
P("  Phi before this floor is applied to it.")

# ============================================================================================================ finish
lb = [c for c in CHECKS if c[2]]
nf = sum(not c[1] for c in lb)
P(f"\n  {sum(c[1] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}")
builtins.open(os.path.join(LANE, "CFG197_bound.out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf else 0)
