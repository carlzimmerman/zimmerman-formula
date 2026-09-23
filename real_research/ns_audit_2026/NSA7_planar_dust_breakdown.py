#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
NSA7 -- DOES THE FRAMEWORK'S OWN FLUID HAVE SMOOTH SOLUTIONS?  The Navier-Stokes question asked of the framework's
equations: pressureless self-gravitating matter under the framework's law (QUMOND reading, kernels nu_RAR and mu_2,
kappa = 1/2, a0 = 9.36e-11 canonical / 1.13e-10 alt), solved exactly in planar symmetry.

WHY PLANAR IS EXACT
  For a slab, the Newtonian field at a Lagrangian sheet is g_N = -2 pi G (M_left - M_right); the mass on either side
  of a sheet is conserved until sheets cross, so g_N -- and therefore the framework's g = a0 F(|g_N|/a0) sign(g_N),
  F(y) = y nu(y) -- is CONSTANT along each sheet until the first crossing.  Every sheet moves with constant
  acceleration: X(t) = x0 + u0 t + g(x0) t^2/2, and the Jacobian is J = 1 + u0' t - 2 pi G nu_eff(y0) rho0 t^2 with
  nu_eff = F'(y) = dg/dg_N.  Density rho = rho0/J; breakdown (J -> 0, rho -> infinity) at
        t*(x0) = [u0' + sqrt(u0'^2 + 8 pi G nu_eff rho0)] / (4 pi G nu_eff rho0).
  (Newton: nu_eff = 1, the classical 1D Euler-Poisson result, Engelberg-Liu-Tadmor 2001.)

WHAT THIS LANE SHOWS
  D1 THE FORCE IS HOLDER-1/2 AT EVERY FIELD NULL.  F(y) = sqrt(y)(1 + O(sqrt y)) for both kernels (series), so near
     a point where g_N = 0 inside matter (a symmetry plane of an isolated slab; every galaxy centre in 3D),
        g ~ -sign(x) sqrt(4 pi G rho_c a0 |x|),     nu_eff(y) ~ 1/(2 sqrt y) -> infinity.
     The force is continuous but not Lipschitz: for an INVISCID fluid no C^2 (hence no smooth) solution of the
     momentum equation can exist for t > 0 there, with or without pressure -- differentiating it once in x equates a
     continuous left side with g_x ~ |x|^(-1/2).  In the pressureless limit even C^1 fails (D2); with viscosity see D7.
  D2 INSTANT BREAKDOWN, T* = 0 (theorem, exact, planar).  For a uniform region at rest t*(x0) = t_N / sqrt(nu_eff),
     t_N = 1/sqrt(2 pi G rho); since nu_eff -> infinity at the null, inf t* = 0.  Checked on an independent sheet
     model: the first crossing time of N sheets falls as N^(-1/4) (MOND) but stays exactly t_N (Newton).
  D3 THE CAUSTIC GROWS AS t^4.  The crossed (multi-stream) region is |x0| < x_c(t) with nu_eff(y_c) = (t_N/t)^2;
     in the deep regime x_c = (pi/4) G rho a0 t^4, i.e. y_c = (t/t_N)^4 / 4.  Sheet-model slope and coefficient.
  D4 THE FRONT REACHES nu_eff = 1 AT EXACTLY THE NEWTONIAN TIME.  At t = t_N the caustic sits where nu_eff = 1:
     y1 = 2.540 (nu_RAR, root of 2 - s - 2e^-s = 0, s = sqrt y) and y1 = 3/2 (mu_2, x = g/a0 = 2).  Everything
     inside y1 collapses before t_N; beyond it the framework is WEAKER than Newton (nu_eff < 1, negative planar
     phantom density rho(nu_eff - 1)), the only place it delays collapse -- by at most the minimum-nu_eff margin.
  D5 3D COROLLARY.  At the centre of any cored sphere g_N = (4 pi/3) G rho_c r, the deep-MOND zone is
     r < 3 a0/(4 pi G rho_c), g ~ sqrt(r) (phantom density ~ r^(-1/2), the known integrable cusp), and a dust shell
     from rest reaches the centre in t = r0 sqrt(pi/2) (G M a0)^(-1/4) ~ r0^(1/4): inner shells arrive first and
     cross the outer ones at once, so T* = 0 at every galaxy centre too; the collapsed region grows as
     r_c = (16/(3 pi)) G rho a0 t^4 (symbolic).
  D8 THE EXTERNAL FIELD: a uniform external Newtonian field e_N a0 shifts the null to d = e_N r_D; isolated
     galaxies keep a singular point inside their matter, strongly EFE-dominated satellites can lose it.
  D7 WITH VISCOSITY (the Navier-Stokes case): the inviscid statement of D1 does not carry over -- viscosity absorbs
     two derivatives, so u is C^(2,1/2) at the null (classical solutions can exist) but never C^3: the framework's
     Navier-Stokes has no smooth (C^infinity) solution through a field null.  Symbolic + viscous grid refinement.
  D6 WHERE THE NULLS ARE.  A disk midplane is NOT a null (the radial galactic field survives there); nulls with
     matter present are galaxy centres.  Numbers for a cored dwarf centre and a bulge centre, both footings.
  READING.  This is about the classical (single-stream, smooth) description.  Collisionless matter simply
  multi-streams through the caustic, and codes smooth the force; nothing unphysical happens.  But the answer to the
  Navier-Stokes-style question for the framework's own fluid is NO: its equations have no smooth (C^2) solution for
  any positive time at a Newtonian field null inside matter (no C^1 one in the dust limit), unlike Newtonian gravity (T* > 0 always) and unlike
  Navier-Stokes (smooth locally, the open question is global).
  PRIOR WORK (cite, do not re-claim).  The field behaviour of D1 is known: Frenkler, 'A mathematical foundation for
  QUMOND', J. Math. Phys. 66, 012501 (2025; arXiv:2403.13498) proves that in spherical symmetry the second
  derivatives of the MOND potential lie only in L^r, 1 < r < 2, 'due to the square root appearing ... in the basic
  MOND paradigm' -- a term ~ r^(-1/2) where the Newtonian field vanishes -- and that this is optimal.  Frenkler,
  'Stability of spherical models in MOND', Kinet. Relat. Models 18 (2025; arXiv:2402.11043) proves nonlinear
  stability of spherical MOND equilibria for the Vlasov and Euler systems; those equilibria are consistent with this
  lane (u = 0 is smooth, the density is only C^(1,1/2) at the centre, D1).  The r^(-1/2) phantom cusp is standard
  (Milgrom 1986, 2009).  NOT found in the literature (three searches): the time-dependent consequences computed here
  -- T* = 0 for smooth dust data (D2), the t^4 caustic laws in planar and spherical symmetry (D3, D5), the
  front-at-nu_eff = 1-at-t_N identity and the nu_eff < 1 delay band of the framework's kernels (D4), and the viscous
  C^(2,1/2) ceiling (D7).
  MUTATE=1 sets nu = 1 (Newton): T*(N) stays t_N, the t^4 law disappears, D2/D3 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/ns_audit_2026/NSA7_planar_dust_breakdown.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "NSA7_planar_dust_breakdown"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "NSA7", "mutate": MUTATE, "checks": {}, "numbers": {}}

G = 6.674e-11
MSUN, PC = 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


# ------------------------------------------------------------------ kernels: F(y) = g/a0 as a function of y = g_N/a0
def F_rar(y):
    y = np.asarray(y, float)
    return y / (-np.expm1(-np.sqrt(y)))


def x_mu2(y):
    """mu_2 (AQUAL form, kappa = 1/2): x mu(x) = y, mu(x) = 1 - (1 + x/2)^-2; returns x = g/a0 (vectorised Newton,
    started above the root from max(sqrt(y), y) + 1e-300 so the iteration is monotone)."""
    y = np.atleast_1d(np.asarray(y, float))
    x = np.maximum(np.sqrt(y), y) + 1e-300
    for _ in range(80):
        f = x * (1 - (1 + x / 2) ** -2) - y
        fp = 1 - (1 - x / 2) * (1 + x / 2) ** -3
        x = np.maximum(x - f / fp, 0.5 * x)
    return x


def nueff_rar(y):
    s = np.sqrt(np.asarray(y, float)); e = np.exp(-s)
    return (2 * (1 - e) - s * e) / (2 * (1 - e) ** 2)


def nueff_mu2(y):
    x = x_mu2(y)
    return 1.0 / (1 - (1 - x / 2) * (1 + x / 2) ** -3)          # dg/dg_N = 1/(mu + x mu')


KER = {"nu_RAR": (F_rar, nueff_rar), "mu_2": (lambda y: x_mu2(y), nueff_mu2)}
if MUTATE:
    KER = {k: (lambda y: np.asarray(y, float), lambda y: np.ones_like(np.asarray(y, float))) for k in KER}

# ============================================================================================ D1
banner("D1  THE FRAMEWORK FORCE IS HOLDER-1/2 AT A FIELD NULL: F(y) = sqrt(y)(1 + O(sqrt y))")
s, xx, yy = sp.symbols("s x y", positive=True)
ser_rar = sp.series(s ** 2 / (1 - sp.exp(-s)), s, 0, 4).removeO()       # y nu_RAR(y) in s = sqrt(y)
# mu_2 inversion: x mu_2(x) = y  ->  x = sqrt(y) + c1 y + ...
c1, c2 = sp.symbols("c1 c2")
xs = s + c1 * s ** 2 + c2 * s ** 3
eq = sp.series(xs * (1 - (1 + xs / 2) ** -2) - s ** 2, s, 0, 5).removeO()
sol = sp.solve([sp.expand(eq).coeff(s, 3), sp.expand(eq).coeff(s, 4)], [c1, c2], dict=True)[0]
ser_mu2 = sp.expand(xs.subs(sol))
lead_rar, lead_mu2 = sp.expand(ser_rar).coeff(s, 1), ser_mu2.coeff(s, 1)
P(f"    nu_RAR: y nu(y) = {sp.expand(ser_rar)} + ...   (s = sqrt y)")
P(f"    mu_2  : g/a0    = {ser_mu2} + ...")
ys = np.array([1e-8, 1e-6, 1e-4])
ne = {k: [float(v[1](np.array([y0]))[0] * 2 * math.sqrt(y0)) for y0 in ys] for k, v in KER.items()}
P(f"    2 sqrt(y) nu_eff(y) at y = 1e-8, 1e-6, 1e-4: " + "; ".join(f"{k}: {[round(x, 5) for x in v]}" for k, v in ne.items()))
OUT["numbers"]["D1"] = {"series_rar": str(sp.expand(ser_rar)), "series_mu2": str(ser_mu2), "2sqrt(y)nu_eff": ne}
check("D1 both kernels have F(y) = sqrt(y) + O(y): the force is exactly Holder-1/2 at a null and nu_eff ~ 1/(2 sqrt y)",
      f"leading coefficients {lead_rar}, {lead_mu2}; 2 sqrt(y) nu_eff -> {[v[0] for v in ne.values()]}",
      lead_rar == 1 and lead_mu2 == 1 and all(abs(v[0] - 1) < 1e-3 for v in ne.values()),
      "continuous but not Lipschitz: no C^2 solution at the null, with or without pressure")

# ============================================================================================ D2
banner("D2  INSTANT BREAKDOWN: THE FIRST SHEET CROSSING TIME vs N (units: t_N = 1, y = 1 at x = 1)")
# uniform slab at rest, half-width W in units l = a0/(4 pi G rho); a0 = 2 l/t_N^2; sheet acceleration -2 F(|X0|) sgn(X0)
W = 1.0                                         # only the pair straddling the null sets T*
Ns = [2000, 20000, 200000, 2000000]
tstar = {}
for k, (F, _) in KER.items():
    row = []
    for Nn in Ns:
        d = 2 * W / Nn
        X0 = -W + (np.arange(Nn) + 0.5) * d
        g = -2.0 * np.sign(X0) * np.asarray(F(np.abs(X0)))
        dg = g[:-1] - g[1:]                                             # closing rate of each neighbour pair
        with np.errstate(divide="ignore", invalid="ignore"):
            tp = np.where(dg > 0, np.sqrt(2 * d / dg), np.inf)
        row.append(float(tp.min()))
    tstar[k] = row
    P(f"    {k:7s} T*(N) for N = {Ns}: {[f'{v:.5f}' for v in row]}")
slopes = {k: float(np.polyfit(np.log(Ns), np.log(v), 1)[0]) for k, v in tstar.items()}
P(f"    log-log slope d ln T* / d ln N: {slopes}   (MOND prediction -1/4; Newton 0 with T* = 1 exactly)")
OUT["numbers"]["D2"] = {"N": Ns, "Tstar": tstar, "slopes": slopes}
check("D2 the first crossing time falls as N^(-1/4) for both kernels (T* -> 0 in the continuum): no classical "
      "solution exists for any t > 0", f"slopes {slopes}", all(abs(v + 0.25) < 0.02 for v in slopes.values()),
      "Newton gives T* = t_N for every N (MUTATE); the framework's null makes the fluid ill-posed at t = 0+")

# ============================================================================================ D3
banner("D3  THE CAUSTIC GROWS AS t^4: x_c = (pi/4) G rho a0 t^4  (y_c = tau^4/4 in these units)")
Nn, W3 = 400000, 0.5
d = 2 * W3 / Nn
X0 = -W3 + (np.arange(Nn) + 0.5) * d
res3 = {}
for k, (F, _) in KER.items():
    g = -2.0 * np.sign(X0) * np.asarray(F(np.abs(X0)))
    dg = g[:-1] - g[1:]
    with np.errstate(divide="ignore", invalid="ignore"):
        tp = np.where(dg > 0, np.sqrt(2 * d / dg), np.inf)
    xm = np.abs(0.5 * (X0[:-1] + X0[1:]))
    taus = np.array([0.10, 0.12, 0.15, 0.18, 0.22])
    xc = np.array([xm[tp <= t].max() if np.any(tp <= t) else 0.0 for t in taus])
    ok_pts = xc > 5 * d
    sl = float(np.polyfit(np.log(taus[ok_pts]), np.log(xc[ok_pts]), 1)[0]) if ok_pts.sum() >= 3 else float("nan")
    coef = float(np.median(xc[ok_pts] / (taus[ok_pts] ** 4 / 4))) if ok_pts.any() else float("nan")
    res3[k] = {"tau": taus.tolist(), "x_c": xc.tolist(), "slope": sl, "coef_over_deep": coef}
    P(f"    {k:7s} x_c(tau) = {[f'{v:.3e}' for v in xc]}  slope {sl:.3f}  x_c / (tau^4/4) = {coef:.3f}")
OUT["numbers"]["D3"] = res3
check("D3 the multi-stream region grows as t^4 with the deep-MOND coefficient (pi/4) G rho a0",
      {k: (round(v["slope"], 3), round(v["coef_over_deep"], 3)) for k, v in res3.items()},
      all(abs(v["slope"] - 4) < 0.15 and abs(v["coef_over_deep"] - 1) < 0.15 for v in res3.values()),
      "a0 sets the caustic rate: x_c/l = tau^4/4 with l = a0/(4 pi G rho)")

# ============================================================================================ D4
banner("D4  AT t = t_N THE FRONT SITS EXACTLY WHERE nu_eff = 1; BEYOND IT THE FRAMEWORK IS WEAKER THAN NEWTON")
y1 = {"nu_RAR": brentq(lambda s_: 2 - s_ - 2 * math.exp(-s_), 0.5, 3.0) ** 2, "mu_2": 1.5}
Nn, W4 = 400000, 20.0
d = 2 * W4 / Nn
X0 = -W4 + (np.arange(Nn) + 0.5) * d
chk4 = {}
for k, (F, nue) in {"nu_RAR": (F_rar, nueff_rar), "mu_2": (lambda y: x_mu2(y), nueff_mu2)}.items():
    v1 = float(nue(np.array([y1[k]]))[0])
    grid = np.logspace(-3, 3, 4001)
    ne_g = np.asarray(nue(grid))
    imin = int(np.argmin(ne_g))
    g = -2.0 * np.sign(X0) * np.asarray(F(np.abs(X0))) if not MUTATE else -2.0 * X0
    dg = g[:-1] - g[1:]
    with np.errstate(divide="ignore", invalid="ignore"):
        tp = np.where(dg > 0, np.sqrt(2 * d / dg), np.inf)
    xm = np.abs(0.5 * (X0[:-1] + X0[1:]))
    front = float(xm[tp <= 1.0].max()) if np.any(tp <= 1.0) else 0.0
    chk4[k] = {"y1": y1[k], "nu_eff(y1)": v1, "front_at_tN": front, "min_nu_eff": float(ne_g[imin]),
               "y_at_min": float(grid[imin]), "max_delay_pct": 100 * (1 / math.sqrt(ne_g[imin]) - 1)}
    P(f"    {k:7s} nu_eff = 1 at y1 = {y1[k]:.4f} (check {v1:.12f}); sheet front at tau = 1: y = {front:.4f}; "
      f"min nu_eff {ne_g[imin]:.4f} at y = {grid[imin]:.2f} -> collapse delayed at most {chk4[k]['max_delay_pct']:.2f}%")
OUT["numbers"]["D4"] = chk4
check("D4 at t = t_N the caustic front is at nu_eff = 1 (y1 = 2.540 nu_RAR, 3/2 mu_2); beyond y1 nu_eff < 1 "
      "(negative planar phantom density), the only regime where the framework delays collapse, by a few percent",
      {k: (round(v["front_at_tN"], 3), round(v["y1"], 3), round(v["max_delay_pct"], 2)) for k, v in chk4.items()},
      all(abs(v["nu_eff(y1)"] - 1) < 1e-9 and abs(v["front_at_tN"] - v["y1"]) < 0.02 and v["min_nu_eff"] < 1
          for v in chk4.values()),
      "an exact identity: the MOND caustic keeps Newtonian time at the nu_eff = 1 surface")

# ============================================================================================ D5
banner("D5  3D COROLLARY: EVERY CORED CENTRE BREAKS AT t = 0")
r0, M, a0s, Gs, rho, r = sp.symbols("r0 M a0 G rho r", positive=True)
# deep MOND shell from rest: r'' = -sqrt(G M a0)/r  =>  (1/2) r'^2 = sqrt(G M a0) ln(r0/r)
q = sp.symbols("q", positive=True)
t_arr = r0 / sp.sqrt(2 * sp.sqrt(Gs * M * a0s)) * sp.integrate(1 / sp.sqrt(sp.log(1 / q)), (q, 0, 1))
t_arr = sp.simplify(t_arr.subs(M, sp.Rational(4, 3) * sp.pi * rho * r0 ** 3))
expo = sp.simplify(sp.diff(sp.log(t_arr), r0) * r0)
tt = sp.symbols("t", positive=True)
r_c = sp.solve(sp.Eq(t_arr, tt), r0)[0]                                 # shells that have reached the centre by t
r_c_coef = sp.simplify(r_c / (Gs * rho * a0s * tt ** 4))
ph = sp.simplify(sp.diff(r ** 2 * sp.sqrt(sp.Rational(4, 3) * sp.pi * Gs * rho * a0s * r), r) / r ** 2)
ph_expo = sp.simplify(sp.diff(sp.log(ph), r) * r)
P(f"    shell arrival time from rest: t = {t_arr}   ->  d ln t / d ln r0 = {expo}")
P(f"    region that has reached the centre by t: r_c = {sp.simplify(r_c)}  (coefficient of G rho a0 t^4: {r_c_coef})")
P(f"    phantom density ~ (1/r^2) d(r^2 g)/dr with g ~ sqrt(r): exponent {ph_expo}")
OUT["numbers"]["D5"] = {"t_arrival": str(t_arr), "exponent": str(expo), "r_c": str(r_c), "r_c_coef": str(r_c_coef),
                        "phantom_exponent": str(ph_expo)}
check("D5 in 3D the deep-MOND centre has t_arrival ~ r0^(1/4) (inner shells first -> instant crossing) and a "
      "phantom density ~ r^(-1/2); the collapsed region grows as r_c = (16/(3 pi)) G rho a0 t^4",
      f"exponents {expo}, {ph_expo}; r_c coefficient {r_c_coef}",
      expo == sp.Rational(1, 4) and ph_expo == -sp.Rational(1, 2) and sp.simplify(r_c_coef - 16 / (3 * sp.pi)) == 0,
      "every galaxy centre with rho > 0 is a Newtonian null: the framework fluid is ill-posed there too")

# ============================================================================================ D6
banner("D6  WHERE THE NULLS ARE, AND THE NUMBERS (BOTH FOOTINGS)")
# A disk midplane is NOT a null: the radial galactic field (~2 a0 near the Sun) survives there, so the TOTAL
# Newtonian field never vanishes.  Nulls with matter present are galaxy centres (and symmetric configurations);
# field saddles between galaxies carry the singularity only if gas sits at the saddle.  The slab of D2-D4 is the
# exact idealisation; the physical cases are cored centres (spherical: y = (4 pi/3) G rho_c r / a0).
Myr = 3.156e13
rows6 = {}
for label, rho_msun in (("cored dwarf centre", 0.1), ("bulge centre", 100.0)):
    rho_c = rho_msun * MSUN / PC ** 3
    t_ff = math.sqrt(3 * math.pi / (32 * G * rho_c))                      # Newtonian uniform-sphere free fall
    for foot, a0 in A0.items():
        r_D = 3 * a0 / (4 * math.pi * G * rho_c)                          # deep-MOND zone radius (y = 1)
        t_D = (3 * math.pi) ** 0.25 * r_D ** 0.25 / (2 * (G * a0 * rho_c) ** 0.25)   # D5 arrival time at r_D
        rows6[f"{label} / {foot}"] = {"rho_c_Msun_pc3": rho_msun, "r_D_pc": r_D / PC, "t_arrival_rD_Myr": t_D / Myr,
                                     "t_ff_newton_Myr": t_ff / Myr}
        P(f"    {label:19s} rho_c = {rho_msun:6.1f} Msun/pc^3, {foot:9s}: deep zone r < {r_D / PC:8.1f} pc; a shell "
          f"from its edge reaches the centre in {t_D / Myr:6.2f} Myr (deep formula) vs Newtonian free fall "
          f"{t_ff / Myr:6.2f} Myr")
OUT["numbers"]["D6"] = rows6
check("D6 numbers (documentary): real nulls are galaxy centres; the deep zone is kpc-scale in cored dwarfs and "
      "pc-scale in bulges, and it is crossed on the Newtonian free-fall time", {k: round(v["r_D_pc"], 1) for k, v in rows6.items()},
      True, "disk midplanes are NOT nulls (the radial field survives); the slab of D2-D4 is an idealisation",
      load_bearing=False)

# ============================================================================================ D7
banner("D7  WITH VISCOSITY (THE NAVIER-STOKES CASE): C^2 SURVIVES, C^3 DOES NOT")
# Viscosity absorbs two derivatives of the Holder-1/2 force: nu u_xx = -g gives u ~ |x|^(5/2), so u is C^(2,1/2) but
# u_xxx ~ |x|^(-1/2).  Symbolic particular solution + a time-dependent viscous solve (Crank-Nicolson, u_t = nu u_xx + g,
# u(x,0) = 0, Dirichlet 0 on [-1,1], to t = 0.1) under grid refinement: max|D^3 u| near the null grows ~ h^(-1/2), and
# the local profile u_xx = a sqrt(x) + b x + ... has a = 1/nu (the particular solution's coefficient).
xv, nuv = sp.symbols("x nu", positive=True)
g_deep = -sp.sqrt(xv)                                   # x > 0 side of g = -sign(x) sqrt(|x|) (units: 4 pi G rho a0 = 1)
up = sp.integrate(sp.integrate(-g_deep / nuv, xv), xv)  # nu u'' = -g on x > 0 (odd extension)
u3 = sp.diff(up, xv, 3)
u2_exp = sp.limit(sp.log(sp.diff(up, xv, 2)) / sp.log(xv), xv, 0, "+")
u3_exp = sp.limit(sp.log(u3 * nuv) / sp.log(xv), xv, 0, "+")
P(f"    particular solution (x > 0): u = {sp.simplify(up)};  u_xx ~ x^{u2_exp};  u_xxx ~ x^{u3_exp}")
from scipy.sparse import diags
from scipy.sparse.linalg import splu
NUV, TEND = 1.0, 0.1
gfun = (lambda x: -x) if MUTATE else (lambda x: -np.sign(x) * np.sqrt(np.abs(x)))
rows7 = {}
for M in (401, 801, 1601, 3201):
    xg = np.linspace(-1, 1, M); h = xg[1] - xg[0]
    n = M - 2
    Lap = diags([1, -2, 1], [-1, 0, 1], shape=(n, n)) / h ** 2
    dt = 1e-4
    A = (diags([1.0], [0], shape=(n, n)) - 0.5 * dt * NUV * Lap).tocsc()
    B = (diags([1.0], [0], shape=(n, n)) + 0.5 * dt * NUV * Lap).tocsr()
    lu = splu(A)
    uu = np.zeros(n); src = dt * gfun(xg[1:-1])
    for _ in range(int(round(TEND / dt))):
        uu = lu.solve(B @ uu + src)
    ufull = np.concatenate([[0.0], uu, [0.0]])
    c = slice(M // 2 - 20, M // 2 + 21)                  # a fixed number of cells around the null
    d2 = np.diff(ufull, 2) / h ** 2
    d3 = np.diff(ufull, 3) / h ** 3
    rows7[M] = {"h": h, "max_d2": float(np.max(np.abs(d2[M // 2 - 20:M // 2 + 20]))),
                "max_d3": float(np.max(np.abs(d3[M // 2 - 20:M // 2 + 20])))}
    # local profile of u_xx on 0 < x <= 32 h: fit a sqrt(x) + b x + c x^2 (u_xx is odd, so no constant term);
    # a Holder-1/2 force predicts a = 1/nu exactly (the particular solution), a Lipschitz force a = 0
    k = np.arange(1, 33)
    xs_ = xg[M // 2 + k]; d2s_ = d2[M // 2 + k - 1]            # d2[i] is centred on node i+1
    Afit = np.vstack([np.sqrt(xs_), xs_, xs_ ** 2]).T
    coef_fit = np.linalg.lstsq(Afit, d2s_, rcond=None)[0]
    rows7[M]["fit_a_sqrt"] = float(coef_fit[0]); rows7[M]["fit_b_lin"] = float(coef_fit[1])
    P(f"    M = {M:5d} (h = {h:.2e}): max|u_xxx| near null {rows7[M]['max_d3']:.3f}; u_xx ~ "
      f"{rows7[M]['fit_a_sqrt']:.4f} sqrt(x) {rows7[M]['fit_b_lin']:+.3f} x near the null")
hs = np.array([v["h"] for v in rows7.values()]); d3s = np.array([v["max_d3"] for v in rows7.values()])
d2s = np.array([v["max_d2"] for v in rows7.values()])
sl3 = float(np.polyfit(np.log(hs), np.log(d3s), 1)[0])
a_fin = rows7[max(rows7)]["fit_a_sqrt"]
P(f"    d ln max|u_xxx| / d ln h = {sl3:.3f} (Holder-1/2 force: -1/2; Lipschitz: 0);  finest-grid sqrt(x) coefficient "
  f"of u_xx = {a_fin:.4f} (Holder-1/2 force: 1/nu = {1 / NUV:.1f}; Lipschitz: 0)")
OUT["numbers"]["D7"] = {"particular": str(sp.simplify(up)), "u_xx_exponent": str(u2_exp), "u_xxx_exponent": str(u3_exp),
                        "grid": {str(k): v for k, v in rows7.items()}, "slope_d3": sl3, "a_sqrt_finest": a_fin}
check("D7 with viscosity the solution is C^(2,1/2) at the null but not C^3: u_xx ~ |x|^(1/2), u_xxx ~ |x|^(-1/2); a "
      "viscous time-dependent solve reproduces both exponents under grid refinement",
      f"exponents {u2_exp}, {u3_exp}; u_xxx grid slope {sl3:.3f}; u_xx sqrt(x) coefficient {a_fin:.4f} (1/nu = 1)",
      u2_exp == sp.Rational(1, 2) and u3_exp == -sp.Rational(1, 2) and abs(sl3 + 0.5) < 0.1 and abs(a_fin - 1 / NUV) < 0.03,
      "viscosity rescues classical (C^2) solutions but not smoothness: the framework's Navier-Stokes has no C^infinity "
      "solution through a field null")

# ============================================================================================ D8
banner("D8  THE EXTERNAL FIELD MOVES THE NULL; IT REMOVES IT ONLY IF THE SHIFT LEAVES THE MATTER")
# In a uniform core g_N,int = -(4 pi/3) G rho_c r; a uniform external Newtonian field e_N a0 shifts the null of the
# TOTAL Newtonian field (where the framework's force is Holder-1/2) to d = 3 e_N a0/(4 pi G rho_c) = e_N r_D.
ee = sp.symbols("e_N", positive=True)
d_null = sp.solve(sp.Eq(sp.Rational(4, 3) * sp.pi * Gs * rho * r, ee * a0s), r)[0]
d_over_rD = sp.simplify(d_null / (3 * a0s / (4 * sp.pi * Gs * rho)))
P(f"    null displacement d = {d_null}  =  e_N x r_D  (check: d/r_D = {d_over_rD})")
cases = [("isolated field dwarf", 0.1, 0.02, 1500.0), ("MW-satellite dSph", 0.01, 0.10, 300.0),
         ("bulge of an isolated spiral", 100.0, 0.02, 500.0)]
rows8 = {}
for label, rho_msun, eN, size_pc in cases:
    rho_c = rho_msun * MSUN / PC ** 3
    for foot, a0 in A0.items():
        rD = 3 * a0 / (4 * math.pi * G * rho_c)
        d_pc = eN * rD / PC
        rows8[f"{label} / {foot}"] = {"rho_c": rho_msun, "e_N": eN, "size_pc": size_pc, "d_pc": d_pc,
                                     "null_inside_matter": bool(d_pc < size_pc)}
        P(f"    {label:27s} rho_c = {rho_msun:6.2f}, e_N = {eN:.2f}, size ~ {size_pc:6.0f} pc, {foot:9s}: null shifted "
          f"{d_pc:9.1f} pc -> {'STILL INSIDE the matter (singular point persists)' if d_pc < size_pc else 'outside the matter (regular)'}")
OUT["numbers"]["D8"] = {"d_over_rD": str(d_over_rD), "cases": rows8}
check("D8 the external field displaces the null by exactly e_N r_D: isolated galaxies keep a singular point inside "
      "their matter; strongly external-field-dominated satellites can lose it (representative numbers)",
      {k: round(v["d_pc"], 1) for k, v in rows8.items()}, sp.simplify(d_over_rD - ee) == 0,
      "the framework's own EFE regularises only systems whose field null is pushed out of the matter")

# ============================================================================================ verdict
banner("VERDICT")
P("""  The Navier-Stokes question, asked of the framework's own equations, has a definite answer: no.  Under the
  framework's law the force is exactly Holder-1/2 wherever the Newtonian field vanishes inside matter -- in
  practice every cored galaxy centre -- so the self-gravitating fluid has no smooth solution for any positive time
  there: an inviscid one is not even C^2, a viscous (Navier-Stokes) one is at best C^(2,1/2), and in the
  pressureless limit not even C^1 -- the density goes singular at t = 0+ with a multi-stream region growing as
  (pi/4) G rho a0 t^4.  Newtonian gravity keeps T* > 0; the framework does not.  Physically this
  is benign (collisionless matter multi-streams; hydrodynamics must be posed in a Holder/weak class), but it is a
  structural fact about the equations: the framework makes regularity WORSE, not better, at field nulls.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
