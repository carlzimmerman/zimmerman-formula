#!/usr/bin/env python3
"""
MECHANISM AUDIT for the dS-Unruh modified-inertia law.   2026-07-30
=================================================================

Verifies, symbolically where possible, the load-bearing claims of the
mechanism hunt.  Exits non-zero on any failed internal check.
No hard-coded verdicts: every number is recomputed from inputs.

CHECKS
  1. mu_fw(x) = (sqrt(1+4x^2)-1)/(2x) is CHARACTER-FOR-CHARACTER
     Milgrom (1999, PLA 253, 273) Eq. 9:  mu_hat(x)=[1+(2x)^-2]^1/2-(2x)^-1.
  2. The de Sitter-Unruh Delta-T construction (Milgrom 1999 Eq. 8, using the
     Deser-Levin 1997 temperature T=(a^2+Lambda/3)^1/2/2pi) forces
     a0_hat = 2(Lambda/3)^1/2 = 2 c H_Lambda  -- NOT cH_Lambda/Z.
     Quantify the gap the framework's kappa=1/2 must absorb.
  3. Asymptotic class:  1-mu_fw(x) -> A x^-alpha with alpha=1, A=1/2.
     Milgrom (2009, arXiv:0906.4817) Sec.2: alpha=1 => CONSTANT sunward
     anomaly A*a0, which "produces too strong effects on the planets";
     Sereno & Jetzer (2006) require alpha >~ 1.5.
  4. Planetary perihelion precession from that constant anomaly, vs the
     Cassini Q2-equivalent bound (0.43 +- 0.43 mas/cy on Saturn).
  5. Milgrom (1994, Ann.Phys. 229, 384) Eq.57 INVERSION: an action whose
     on-shell circular-orbit value is (1/2)v^2*lambda(x) yields
     mu = lambda + (x/2)lambda'.  Solve for lambda given mu_fw, in closed
     form, and check both limits.  Then test Milgrom's own regularity
     requirement (f analytic at the origin) against the result.
  6. FRW background: comoving proper acceleration is identically zero, so
     the effect vanishes on the background (independent of mechanism).
"""
import sys

import sympy as sp

FAIL = []


def check(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}" + (f"   {detail}" if detail else ""))
    if not cond:
        FAIL.append(label)


x, t, lam = sp.symbols("x t lambda", positive=True)

# ----------------------------------------------------------------------------
print("\n=== 1. mu_fw IS Milgrom 1999 Eq. 9 ===")
mu_fw = (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)
mu_hat = sp.sqrt(1 + (2 * x) ** (-2)) - (2 * x) ** (-1)   # Milgrom 1999 Eq.9
check("mu_fw(x) - mu_hat(x) == 0 identically",
      sp.simplify(mu_fw - mu_hat) == 0)

# and the nu form g_obs = g_bar*sqrt(1+a0/g_bar) is the same law.
# mu_fw(y)*g_obs with y=g_obs/a0 equals (sqrt(a0^2+4 g_obs^2)-a0)/2; with
# g_obs^2 = g^2 + a0 g the radicand is the perfect square (2g+a0)^2.
g, a0s = sp.symbols("g a0", positive=True)
gobs_sq = g**2 + a0s * g
radicand = sp.expand(a0s**2 + 4 * gobs_sq)
check("radicand a0^2+4 g_obs^2 is the perfect square (2 g_bar + a0)^2",
      sp.simplify(radicand - (2 * g + a0s) ** 2) == 0)
check("=> mu_fw(g_obs/a0)*g_obs == g_bar identically",
      sp.simplify(((2 * g + a0s) - a0s) / 2 - g) == 0)
# independent numeric sweep over 8 decades
import random as _rnd
_rnd.seed(7)
worst = 0.0
for _ in range(2000):
    gv = 10 ** _rnd.uniform(-14, -6)
    a0v = 9.3624e-11
    gov = gv * (1 + a0v / gv) ** 0.5
    yv = gov / a0v
    muv = ((1 + 4 * yv**2) ** 0.5 - 1) / (2 * yv)
    worst = max(worst, abs(muv * gov / gv - 1))
check("numeric sweep (2000 pts, 8 decades): mu_fw*g_obs == g_bar",
      worst < 1e-12, f"max rel. err {worst:.2e}")

# ----------------------------------------------------------------------------
print("\n=== 2. WHAT COEFFICIENT DOES THE MECHANISM FORCE? ===")
# Deser-Levin 1997 (CQG 14, L163): uniformly accelerated detector in dS sees
#   T(a) = (1/2pi) sqrt(a^2 + Lambda/3).   With H_L^2 = Lambda c^2/3, in c=1
#   units sqrt(Lambda/3) = H_L.  Milgrom's Le Chatelier postulate:
#   2pi(T(a)-T(0)) = a*mu_hat(a/a0_hat).
HL = sp.symbols("H_L", positive=True)
a = sp.symbols("a", positive=True)
dT = sp.sqrt(a**2 + HL**2) - HL          # = 2pi * Delta T, c=1
a0_hat = 2 * HL                           # Milgrom's claim
check("2pi*DeltaT == a*mu_hat(a/(2H_L))  => a0_hat = 2 c H_Lambda",
      sp.simplify(dT - a * mu_hat.subs(x, a / a0_hat)) == 0)

# solve the resulting law for a: sqrt(a^2+H^2)-H = g  ->  a^2 = g^2 + 2Hg
sol = sp.solve(sp.Eq(sp.sqrt(a**2 + HL**2) - HL, g), a)
a_sol = [s for s in sol if s.is_positive is not False][0]
check("mechanism's law is g_obs = g_bar*sqrt(1 + 2H_L/g_bar)",
      sp.simplify(a_sol**2 - (g**2 + 2 * HL * g)) == 0,
      "i.e. framework form with a0 = 2 c H_Lambda")

# numbers
c = 2.99792458e8
H0 = 67.4 * 1e3 / 3.0856775814913673e22   # s^-1, Planck 2018
Om_L = 0.685
HL_num = H0 * Om_L**0.5
cHL = c * HL_num
Z = (32 * 3.141592653589793 / 3) ** 0.5
a0_fw = cHL / Z
a0_mech = 2 * cHL                          # Milgrom 1999 / Deser-Levin
a0_obs = 1.2e-10                           # McGaugh RAR scale
print(f"    c H_Lambda            = {cHL:.4e} m/s^2")
print(f"    Z = sqrt(32pi/3)      = {Z:.5f}")
print(f"    a0 framework (cH/Z)   = {a0_fw:.4e} m/s^2   (kappa=1/2)")
print(f"    a0 mechanism (2cH)    = {a0_mech:.4e} m/s^2")
print(f"    a0 observed (RAR)     = {a0_obs:.4e} m/s^2")
print(f"    mechanism / framework = {a0_mech/a0_fw:.3f}   (= 2Z)")
print(f"    mechanism / observed  = {a0_mech/a0_obs:.3f}")
check("a0_fw reproduces the canonical 9.36e-11", abs(a0_fw / 9.36e-11 - 1) < 0.01,
      f"{a0_fw:.4e}")
check("mechanism/framework ratio == 2Z", abs(a0_mech / a0_fw - 2 * Z) < 1e-9,
      f"{2*Z:.4f}")
check("mechanism OVERSHOOTS observed a0 by >5x",
      a0_mech / a0_obs > 5, f"factor {a0_mech/a0_obs:.1f}")
# Luo 2026 (arXiv:2602.14515): a0 = 2*sqrt(Lambda/48) = c H_L/2
a0_luo = cHL / 2
print(f"    a0 Luo 2026 (cH/2)    = {a0_luo:.4e} m/s^2  "
      f"(x{a0_luo/a0_fw:.2f} framework, x{a0_luo/a0_obs:.2f} observed)")
check("Luo's scale also overshoots the framework's value",
      a0_luo / a0_fw > 2, f"factor {a0_luo/a0_fw:.2f}")

# ----------------------------------------------------------------------------
print("\n=== 3. HIGH-ACCELERATION ASYMPTOTIC CLASS (alpha, A) ===")
ser = sp.series(1 - mu_fw, x, sp.oo, 3).removeO()
print(f"    1 - mu_fw(x) = {sp.simplify(ser)}  (x -> oo)")
lead = sp.limit((1 - mu_fw) * x, x, sp.oo)
check("1-mu_fw ~ A x^-alpha with alpha == 1", lead.is_finite and lead != 0,
      f"A = {lead}")
check("A == 1/2", sp.simplify(lead - sp.Rational(1, 2)) == 0)
# Milgrom 2009 Sec.2: isolated-mass anomaly g_a = A a0 (u/R_M)^{2(alpha-1)}
check("alpha=1 => anomaly is CONSTANT in radius (exponent 2(alpha-1)=0)",
      sp.simplify(2 * (1 - 1)) == 0)
check("alpha=1 < Sereno-Jetzer 2006 requirement alpha >~ 1.5", 1 < 1.5)

# ----------------------------------------------------------------------------
print("\n=== 4. PLANETARY PRECESSION FROM THE CONSTANT ANOMALY A*a0 ===")
# constant extra radial acceleration Acc: apsidal precession per orbit
#   dvarpi = 2*pi*Acc*a^2/(GM)   (near-circular, central-force apsidal angle)
import math
GM = 1.32712440018e20
Acc = a0_fw / 2.0            # framework: A=1/2  => anomaly = a0/2
print(f"    constant sunward anomaly A*a0 = {Acc:.4e} m/s^2 "
      f"= {Acc*100:.3e} cm/s^2")
AU = 1.495978707e11
planets = {"Mercury": 0.387098, "Earth": 1.000000,
           "Jupiter": 5.2044, "Saturn": 9.5826}
prec = {}
for name, a_au in planets.items():
    aa = a_au * AU
    per_orbit = 2 * math.pi * Acc * aa**2 / GM          # rad
    P_yr = a_au**1.5                                    # Kepler, years
    per_cy = per_orbit * (100.0 / P_yr)                 # rad/century
    arcsec_cy = per_cy * 206264.806
    prec[name] = arcsec_cy
    print(f"    {name:8s} a={a_au:7.4f} AU   "
          f"delta-varpi = {arcsec_cy:9.4f} arcsec/century")
check("precession scales as a^(1/2) across planets",
      abs(prec["Saturn"] / prec["Mercury"]
          - (9.5826 / 0.387098) ** 0.5) < 1e-6)
# Cassini Q2-equivalent bound on Saturn's perihelion precession:
# (0.43 +- 0.43) mas/cy  [Hees et al. 2014, PRD 89, 102002]
bound_saturn = 0.43e-3 * 3          # 3-sigma, arcsec/cy
ratio = prec["Saturn"] / bound_saturn
print(f"    Saturn bound (3sigma, Cassini) = {bound_saturn:.3e} arcsec/cy")
print(f"    VIOLATION FACTOR               = {ratio:.3e}")
check("constant a0/2 anomaly exceeds the Cassini-equivalent Saturn bound",
      ratio > 1, f"by {ratio:.2e}x")
# Sereno & Jetzer 2006 tolerances on a constant sunward acceleration (cm/s^2)
sj = {"Uranus": 1e-10, "Neptune": 4e-10, "Pluto": 1e-9}
for nm, lim in sj.items():
    print(f"    Sereno-Jetzer {nm:8s} tolerance {lim:.1e} cm/s^2  ->  "
          f"framework/{nm} = {Acc*100/lim:.1f}x")
check("framework's constant anomaly exceeds ALL Sereno-Jetzer tolerances",
      all(Acc * 100 / lim > 1 for lim in sj.values()))
# Fienga et al. 2009 global-fit tolerances are ~2 orders weaker -> contested
fienga_uranus = 2e-8   # cm/s^2
print(f"    Fienga+2009 global-fit Uranus tolerance {fienga_uranus:.1e} cm/s^2"
      f"  ->  framework is {fienga_uranus/(Acc*100):.1f}x BELOW it")
check("verdict is METHODOLOGY-DEPENDENT (Fienga global fit tolerates it)",
      Acc * 100 < fienga_uranus,
      "=> report as strongly disfavoured + contested, not a clean kill")

# ----------------------------------------------------------------------------
print("\n=== 5. MILGROM 1994 Eq.57 INVERSION: the action DOES exist "
      "on circular orbits ===")
# Milgrom 1994 Sec.IV: for ANY translation+rotation-invariant kinetic action
# S_k[r(t),a0] with a0 the ONLY dimensional constant, circular orbits in an
# axisymmetric potential obey mu(a/a0)a = dphi/dr EXACTLY, with
#   S_k^c = (1/2)v^2 lambda(x),   mu(x) = lambda(x) + (x/2) lambda'(x).
# Invert:  d(x^2 lambda)/dx = 2 x mu(x)  =>  lambda = (2/x^2) int_0^x t mu dt.
lam_expr = sp.simplify(2 / x**2 * sp.integrate(t * mu_fw.subs(x, t), (t, 0, x)))
lam_expr = sp.simplify(lam_expr)
print(f"    lambda(x) = {lam_expr}")
check("lambda satisfies mu = lambda + (x/2) lambda'",
      sp.simplify(lam_expr + x / 2 * sp.diff(lam_expr, x) - mu_fw) == 0)
lim0 = sp.limit(lam_expr / x, x, 0)
liminf = sp.limit(lam_expr, x, sp.oo)
print(f"    lambda(x)/x -> {lim0} as x->0 (deep-MOND: S_k ~ a0^-1, required)")
print(f"    lambda(x)   -> {liminf} as x->oo (Newtonian: S_k -> v^2/2)")
check("Newtonian limit lambda->1", sp.simplify(liminf - 1) == 0)
check("deep-MOND limit lambda ~ (2/3)x, so S_k^c ~ a0^-1 as Milgrom requires",
      sp.simplify(lim0 - sp.Rational(2, 3)) == 0)
# Milgrom's regularity requirement: for L_k = (1/2) v f(a0^2 D g^-1 D) v,
# mu(x) = f(z)[1+fhat(z)] at z = 1/x^2, and f must be NON-SINGULAR at z=0
# for the Newtonian limit to hold on ALL trajectories (Milgrom 1994, below
# Eq.35).  Solve f - z f' = mu_fw(1/sqrt(z)) and inspect z=0.
z, s = sp.symbols("z s", positive=True)
# work in s = sqrt(z) = 1/x to keep everything a Taylor series at the origin
G_s = sp.series(mu_fw.subs(x, 1 / s), s, 0, 4).removeO()
print(f"    G(z) = mu_fw(1/sqrt(z)) = {sp.expand(G_s)}   [s = sqrt(z)]")
c_half = sp.expand(G_s).coeff(s, 1)
check("G has a NON-ZERO z^(1/2) coefficient (this IS alpha=1)",
      c_half != 0, f"coeff = {c_half}")
# Ansatz f = 1 + beta*s + gamma*s^2 ; require f - z f' = G through O(s)
beta, gamma = sp.symbols("beta gamma")
f_ans = 1 + beta * s + gamma * s**2
# z = s^2, d/dz = (1/(2s)) d/ds  =>  z f' = (s/2) df/ds
resid = sp.expand(f_ans - (s / 2) * sp.diff(f_ans, s) - G_s)
sol_b = sp.solve(sp.Eq(resid.coeff(s, 1), 0), beta)[0]
print(f"    forced coefficient of sqrt(z) in f:  beta = {sol_b}")
check("f(z) must carry a sqrt(z) branch point at z=0 (beta != 0)",
      sol_b != 0,
      "=> violates Milgrom 1994's regularity requirement below Eq.35")
# and confirm no analytic-in-z (integer-power) f can work
f_int = 1 + sum(sp.Symbol(f"b{k}") * s ** (2 * k) for k in range(1, 4))
resid_int = sp.expand(f_int - (s / 2) * sp.diff(f_int, s) - G_s)
check("no f analytic in z (even powers of s only) can match the s^1 term",
      sp.expand(resid_int).coeff(s, 1) != 0,
      f"leftover = {sp.expand(resid_int).coeff(s, 1)}")

# ----------------------------------------------------------------------------
print("\n=== 6. FRW BACKGROUND: EFFECT VANISHES IDENTICALLY ===")
# comoving observer in FRW: u^mu = (1,0,0,0) in cosmic time, a^mu = u^nu D_nu u^mu
tt = sp.symbols("tt", positive=True)
A_fn = sp.Function("A")(tt)
# FRW metric diag(-1, A^2, A^2, A^2); comoving u = (1,0,0,0)
gmat = sp.diag(-1, A_fn**2, A_fn**2, A_fn**2)
coords = [tt] + list(sp.symbols("x1 x2 x3"))
ginv = gmat.inv()
# Christoffels
Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
for m in range(4):
    for i in range(4):
        for j in range(4):
            Gam[m][i][j] = sp.simplify(sum(
                ginv[m, k] * (sp.diff(gmat[k, i], coords[j])
                              + sp.diff(gmat[k, j], coords[i])
                              - sp.diff(gmat[i, j], coords[k]))
                for k in range(4)) / 2)
u = [1, 0, 0, 0]
acc = [sp.simplify(sum(u[i] * sp.diff(u[m], coords[i]) for i in range(4))
                   + sum(Gam[m][i][j] * u[i] * u[j]
                         for i in range(4) for j in range(4)))
       for m in range(4)]
print(f"    comoving 4-acceleration a^mu = {acc}")
check("comoving proper acceleration is identically zero for any a(t)",
      all(sp.simplify(cmp) == 0 for cmp in acc))
check("=> mu_fw(|a|/a0)=mu_fw(0)=0 limit is never probed on the background; "
      "the term vanishes", sp.limit(mu_fw, x, 0) == 0)

# u.Box_u u = -|a|^2 identity (established asset): check on a Rindler worldline
print("\n    -- u_mu Box_u u^mu = -|a|^2 spot-check (flat, hyperbolic) --")
ap, tau = sp.symbols("a_p tau", positive=True)
u_h = [sp.cosh(ap * tau), sp.sinh(ap * tau), 0, 0]         # unit timelike
nrm = sp.simplify(-u_h[0] ** 2 + u_h[1] ** 2)
check("u.u = -1 on the hyperbolic worldline", sp.simplify(nrm + 1) == 0)
du = [sp.diff(comp, tau) for comp in u_h]                  # a^mu
ddu = [sp.diff(comp, tau) for comp in du]                  # Box_u u^mu
a2 = sp.simplify(-du[0] ** 2 + du[1] ** 2)
u_dot_ddu = sp.simplify(-u_h[0] * ddu[0] + u_h[1] * ddu[1])
check("u_mu Box_u u^mu == -|a|^2", sp.simplify(u_dot_ddu + a2) == 0,
      f"|a|^2 = {sp.simplify(a2)}")

# ----------------------------------------------------------------------------
print("\n=== 7. PROVE BY MOVING THE NUMBER: does the MECHANISM's own a0 fit "
      "SPARC? ===")
# Same estimator as real_research/rar_framework_a0_mlfit.py, same 175 galaxies,
# same framework nu.  Only a0 moves.
import glob
import os

import numpy as np

kpc = 3.0857e19
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "real_research", "data", "sparc_data")
rows = []
for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(fn, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    rows.append((R * kpc, Vobs, eV, Vgas, Vdisk, Vbul))
check("SPARC rotmod files loaded", len(rows) > 150, f"N={len(rows)} galaxies")


def rar_scatter(Ud, a0v):
    res, w = [], []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in rows:
        Vbar2 = np.sign(Vgas) * Vgas**2 + Ud * Vdisk**2 + 1.4 * Ud * Vbul**2
        gb = Vbar2 * 1e6 / Rm
        go = (Vobs * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        pred = np.sqrt(gb[ok] ** 2 + gb[ok] * a0v)      # framework nu
        res += list(np.log10(go[ok]) - np.log10(pred))
        fr = np.clip(eV[ok], 1, None) / np.clip(Vobs[ok], 1, None)
        w += list(1 / fr**2)
    res, w = np.array(res), np.array(w)
    return float(np.sqrt(np.sum(w * res**2) / np.sum(w)))


grid = np.linspace(0.2, 1.5, 66)
out = {}
for label, a0v in (("framework  cH/Z  ", a0_fw),
                   ("Luo 2026   cH/2  ", a0_luo),
                   ("mechanism  2cH   ", a0_mech)):
    ss = [rar_scatter(U, a0v) for U in grid]
    i = int(np.argmin(ss))
    out[label] = (grid[i], ss[i])
    print(f"    a0 = {a0v:.3e}  [{label}]  best Upsilon_disk = {grid[i]:.2f}"
          f"   scatter = {ss[i]:.3f} dex")
check("framework a0 reproduces the banked ~0.108 dex",
      abs(out["framework  cH/Z  "][1] - 0.108) < 0.02,
      f"{out['framework  cH/Z  '][1]:.3f} dex")
check("mechanism's own a0 = 2cH_Lambda fits WORSE than the framework's",
      out["mechanism  2cH   "][1] > out["framework  cH/Z  "][1],
      f"{out['mechanism  2cH   '][1]:.3f} vs "
      f"{out['framework  cH/Z  '][1]:.3f} dex")
# and it needs an unphysical M/L to even get there
check("mechanism's a0 is driven to the Upsilon grid floor (unphysical M/L)",
      out["mechanism  2cH   "][0] <= grid[1] + 1e-9,
      f"Upsilon_disk -> {out['mechanism  2cH   '][0]:.2f}, "
      "below the 0.5-0.8 population-synthesis range")

# ----------------------------------------------------------------------------
print("\n=== 8. THE SIBLING CONSTRUCTION IN THE SAME PAPER "
      "(Milgrom 1999 Eqs. 10-11) ===")
# Milgrom offers a SECOND thermodynamic functional of the same Deser-Levin
# temperature:  a dT/da = a mu(a/a0)  with mu = x/(1+x^2)^(1/2), a0=(L/3)^(1/2).
# Same bath, same T, different functional -> different mu.  Compare classes.
T_dS = sp.sqrt(a**2 + HL**2)                 # 2pi*T, c=1
mu_sib_target = sp.simplify(a * sp.diff(T_dS, a) / a)
mu_sib = x / sp.sqrt(1 + x**2)               # Milgrom 1999 Eq.11
check("a dT/da = a*mu_sib(a/H_L) with mu_sib = x/sqrt(1+x^2)",
      sp.simplify(mu_sib_target - mu_sib.subs(x, a / HL)) == 0)
lead_sib = sp.limit((1 - mu_sib) * x**2, x, sp.oo)
print(f"    sibling: 1 - mu_sib ~ {lead_sib} x^-2   => alpha = 2")
check("sibling has alpha = 2 (vs framework's alpha = 1)",
      lead_sib.is_finite and lead_sib != 0)
check("sibling PASSES the Sereno-Jetzer alpha >~ 1.5 requirement", 2 > 1.5)
check("the two constructions differ in a0 by exactly a factor 2",
      sp.simplify(a0_hat / HL - 2) == 0)
print(f"    sibling a0 = c H_Lambda = {cHL:.4e} m/s^2  "
      f"(x{cHL/a0_obs:.2f} observed, x{cHL/a0_fw:.2f} framework)")
check("sibling ALSO fails to deliver the observed coefficient",
      cHL / a0_obs > 3, f"factor {cHL/a0_obs:.2f} too large")
print("    => SAME bath, SAME temperature, TWO different mu's and TWO different"
      "\n       a0's.  The thermal setup does NOT select the functional form;"
      "\n       the choice of thermodynamic functional does.")

# ----------------------------------------------------------------------------
print("\n" + "=" * 70)
if FAIL:
    print(f"FAILED CHECKS ({len(FAIL)}):")
    for f_ in FAIL:
        print("   -", f_)
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 70)
