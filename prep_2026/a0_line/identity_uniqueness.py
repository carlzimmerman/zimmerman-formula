#!/usr/bin/env python3
"""
identity_uniqueness.py -- THE a0-LINE IDENTITY, ITS UNIQUENESS, AND THE RIVAL SEPARATION
=========================================================================================
Framework (Zimmerman dS-Unruh MODIFIED-INERTIA, its OWN interpolation, NOT standard MOND):

    g_obs = sqrt(g_bar^2 + a0*g_bar),   a0 = c*H_Lambda/Z,  Z = sqrt(32*pi/3)
    canonical a0 = 9.355e-11 m/s^2 (Planck-anchored);  ALT footing 1.1305e-10 (both always).

Section A  verifies symbolically the exact identity  g_obs^2 - g_bar^2 = a0*g_bar  at EVERY acceleration.
Section B  solves the functional equation for ALL interpolations nu(y) whose squared excess
           is exactly linear in g_bar through the origin, and characterizes the family
           honestly (one-parameter, absorbed by the definition of a0; deep-MOND
           normalization fixes it to nu = sqrt(1+1/y) uniquely).
Section C  derives the rival excess formulas symbolically (McGaugh/RAR-fit exponential nu,
           "simple" nu) with exact asymptotics.
Section D  tabulates the separation ratio R(y) = excess_framework / excess_rival.
Section E  reads the REAL SPARC sample (read-only) and reports where the data actually
           sample y -- i.e. where the separation is observable in principle.

HONESTY RAILS: the identity is an algebraic property of the law, not evidence by itself.
Section B is elementary pointwise algebra -- stated as such, no grandiosity. Section C
shows the "simple" nu ALSO has an asymptotically linear excess (slope 2*a0), so tail
PERSISTENCE alone does not separate it; only exact CONSTANCY of the excess ratio does.
The word "proof" is not used for any data statement. Exit 0 = all symbolic checks pass.
"""
import sympy as sp
import numpy as np, glob, os, csv, json

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research"
HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = "/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger"
anchor = json.load(open(os.path.join(LEDGER, "anchor_values.json")))
A0C, A0A = anchor["a0_canon"], anchor["a0_alt"]      # canonical + ALT footing, BOTH always
GDAG = 1.2e-10                                        # McGaugh/RAR-fit's own g_dagger

bar = "=" * 90
print(bar); print("SECTION A -- THE EXACT IDENTITY"); print(bar)

gb, a0, lam, c = sp.symbols("g_bar a_0 lambda c", positive=True)
y = sp.symbols("y", positive=True)

g_obs = sp.sqrt(gb**2 + a0 * gb)
excess = sp.expand(g_obs**2 - gb**2)
check_A = sp.simplify(excess - a0 * gb)
print(f"  g_obs = sqrt(g_bar^2 + a0*g_bar)")
print(f"  g_obs^2 - g_bar^2 = {excess}")
assert check_A == 0, "identity failed symbolically"
print("  ==> g_obs^2 - g_bar^2 = a0*g_bar  EXACTLY, at every g_bar (no deep-MOND limit,")
print("      no interpolation approximation). The MOND excess of THIS law is a straight")
print("      line through the origin in (g_bar, g_obs^2-g_bar^2) with slope a0.")

print(); print(bar)
print("SECTION B -- UNIQUENESS: which nu(y) have an exactly linear excess?")
print(bar)
# General modified-inertia relation g_obs = nu(y)*g_bar, y = g_bar/a0.
# Excess Delta(y) = g_obs^2 - g_bar^2 = a0^2 * y^2 * (nu(y)^2 - 1).
# Demand Delta = lambda * a0 * g_bar = lambda * a0^2 * y  for ALL y>0  (linear, origin).
nu = sp.Function("nu", positive=True)
eqn = sp.Eq(y**2 * (nu(y) ** 2 - 1), lam * y)
sol = sp.solve(eqn, nu(y))
sol_pos = [s for s in sol if sp.simplify(s.subs({y: 1, lam: 1})) > 0]
print("  Functional equation:  y^2*(nu^2 - 1) = lambda*y   for all y > 0")
print(f"  sympy.solve -> nu(y) = {sol_pos[0]}   (positive branch; the negative branch")
print("  is unphysical since g_obs > 0). NOTE HONESTLY: the equation is pointwise")
print("  algebraic, so this 'uniqueness' is elementary -- but it is EXACT and exhaustive:")
print("  the linear-excess family is EXACTLY the one-parameter family")
print("      nu_lambda(y) = sqrt(1 + lambda/y).")
assert len(sol_pos) == 1
nu_lam = sol_pos[0]

# The lambda parameter is pure a0 redefinition: nu_lambda(g/a0) == nu_1(g/(lambda*a0))
resc = sp.simplify(
    sp.sqrt(1 + lam / (gb / a0)) - sp.sqrt(1 + 1 / (gb / (lam * a0)))
)
assert resc == 0
print("  Rescaling check: sqrt(1 + lambda/(g/a0)) == sqrt(1 + 1/(g/(lambda*a0)))  [OK]")
print("  ==> lambda only rescales a0. Fixing the NORMALIZATION of a0 by the deep limit")

# Deep-MOND normalization: g_obs -> sqrt(a0*g_bar) as y->0 defines a0. Compute the limit.
deep = sp.limit(nu_lam * sp.sqrt(y), y, 0, "+")
print(f"      lim_(y->0) nu_lambda(y)*sqrt(y) = {deep}  ==> g_obs -> sqrt(lambda*a0*g_bar)")
lam_fixed = sp.solve(sp.Eq(deep, 1), lam)
assert lam_fixed == [1]
print("  demanding g_obs -> sqrt(a0*g_bar) (the standard definition of a0) forces")
print("  lambda = 1. CONCLUSION: nu(y) = sqrt(1+1/y) is the UNIQUE interpolation whose")
print("  excess g_obs^2-g_bar^2 is exactly linear in g_bar at all y, up to the")
print("  definition of a0 itself. Any other nu bends the line somewhere.")

# physicality of the unique member: nu>1, monotone g_obs(g_bar)
mono = sp.simplify(sp.diff(sp.sqrt(y**2 + y), y))
assert sp.simplify(mono > 0) or sp.ask(sp.Q.positive(mono), sp.Q.positive(y)) in (True, None)
mono_num = [float(mono.subs(y, v)) for v in (0.01, 1, 100)]
assert all(m > 0 for m in mono_num)
print(f"  Physicality: d(nu*y)/dy = {mono} > 0 (checked at y=0.01,1,100:"
      f" {['%.3f' % m for m in mono_num]}) -- g_obs monotone in g_bar. [OK]")

print(); print(bar)
print("SECTION C -- RIVAL EXCESS FORMULAS (exact + asymptotic, each in its OWN convention)")
print(bar)
# Dimensionless excess ratio eps(y) := (g_obs^2 - g_bar^2)/(a0*g_bar) = y*(nu(y)^2 - 1),
# with y = g_bar/(that convention's own acceleration scale).
eps_fw = sp.simplify(y * (sp.sqrt(1 + 1 / y) ** 2 - 1))
print(f"  FRAMEWORK   nu = sqrt(1+1/y):        eps(y) = {eps_fw}   (exactly 1 at all y)")
assert eps_fw == 1

nu_mcg = 1 / (1 - sp.exp(-sp.sqrt(y)))
eps_mcg = sp.simplify(y * (nu_mcg**2 - 1))
# large-y behavior: substitute t = exp(-sqrt(y)) and expand
t = sp.symbols("t", positive=True)
nu_t = 1 / (1 - t)
tail = sp.series(nu_t**2 - 1, t, 0, 3).removeO()
print(f"  McGAUGH/RAR-FIT nu = 1/(1-e^-sqrt(y)) (y=g_bar/g_dagger, g_dagger=1.2e-10 its own fit):")
print(f"      eps(y) = y*(nu^2-1);   with t=e^-sqrt(y):  nu^2-1 = {tail} + O(t^3)")
print(f"      ==> eps(y) ~ 2*y*e^-sqrt(y)  at high y: the excess DIES superexponentially.")
lim_mcg = sp.limit(eps_mcg, y, sp.oo)
assert lim_mcg == 0
print(f"      lim_(y->oo) eps_McG = {lim_mcg}   [verified symbolically]")
deep_mcg = sp.limit(nu_mcg * sp.sqrt(y), y, 0, "+")
print(f"      deep limit: nu*sqrt(y) -> {deep_mcg} (same a0 normalization, so the")
print("      comparison at matched scale is fair in the deep regime).")

nu_simple = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y)
eps_simple = sp.simplify(y * (nu_simple**2 - 1))
lim_s_hi = sp.limit(eps_simple, y, sp.oo)
lim_s_lo = sp.limit(eps_simple, y, 0, "+")
print(f"  SIMPLE      nu = 1/2 + sqrt(1/4+1/y):  eps(y) = {sp.simplify(eps_simple)}")
print(f"      lim_(y->0) eps = {lim_s_lo},  lim_(y->oo) eps = {lim_s_hi}")
assert lim_s_lo == 1 and lim_s_hi == 2
print("      HONESTY: the simple nu ALSO has a persistent asymptotically-LINEAR excess")
print("      (slope 2*a0). Tail persistence alone does NOT separate framework from")
print("      simple-nu; the discriminant there is the exact CONSTANCY of eps (1 vs a")
print("      factor-2 drift from 1 to 2) -- which is partially degenerate with an")
print("      a0 rescaling in any narrow y window (only the full-range shape breaks it).")
print("      The RAR-FIT family (g_dagger free) is the McGaugh form with a rescaled y:")
print("      same superexponential tail death, so the high-y separation from the")
print("      framework survives ANY choice of g_dagger.")

print(); print(bar)
print("SECTION D -- SEPARATION RATIO R(y) = eps_framework / eps_rival  (matched scale)")
print(bar)
f_mcg = sp.lambdify(y, eps_mcg, "numpy")
f_simple = sp.lambdify(y, eps_simple, "numpy")
ys = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 50.0, 100.0]
print(f"  {'y':>7} {'eps_fw':>8} {'eps_McG':>10} {'R_McG':>10} {'eps_simple':>11} {'R_simple':>9}")
rows_D = []
for yy in ys:
    em, es = float(f_mcg(yy)), float(f_simple(yy))
    rows_D.append((yy, em, es))
    print(f"  {yy:>7.1f} {1.0:>8.3f} {em:>10.4g} {1/em:>10.3g} {es:>11.4g} {1/es:>9.3g}")
r100 = 1 / float(f_mcg(100.0))
print(f"\n  At y = 100 the framework excess exceeds the McGaugh-nu excess by x{r100:.0f}")
print("  (the 'x100 at g_bar ~ 100*a0' statement -- verified, not assumed). Against the")
print("  simple nu the ratio saturates at 1/2: a SHAPE (factor-2) difference, not a decay.")
print("  Convention offset: canonical a0=9.355e-11 vs g_dagger=1.2e-10 shifts y by x1.283;")
print("  this moves R_McG by less than one row of the table -- immaterial to the contrast.")

print(); print(bar)
print("SECTION E -- WHERE REAL SPARC SAMPLES y (Q<=2, inc>=30; Upsilon_d=0.70, Ub=1.4*Ud)")
print(bar)
kpc = 3.0857e19
meta = {}
with open(os.path.join(REPO, "data", "sparc_master_clean.csv")) as fh:
    for r in csv.DictReader(fh):
        meta[r["name"]] = (int(r["Q"]), float(r["inc"]))
UD, UB = 0.70, 1.4 * 0.70
ally, gasdom, ngal = [], [], 0
for f in sorted(glob.glob(os.path.join(REPO, "data", "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(f).replace("_rotmod.dat", "")
    if name not in meta:
        continue
    Q, inc = meta[name]
    if Q > 2 or inc < 30:
        continue
    d = np.genfromtxt(f, comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    Vbar2 = np.sign(Vgas) * Vgas**2 + UD * Vdisk**2 + UB * Vbul**2
    gbv = Vbar2 * 1e6 / (R * kpc)
    ok = (gbv > 0) & (Vobs > 0) & np.isfinite(gbv)
    if not ok.any():
        continue
    ngal += 1
    yv = gbv[ok] / A0C
    ally += list(yv)
    gd = (np.sign(Vgas) * Vgas**2 > UD * Vdisk**2 + UB * Vbul**2)[ok]
    gasdom += list(yv[gd])
ally, gasdom = np.array(ally), np.array(gasdom)
print(f"  Galaxies passing cuts: {ngal};  points: {len(ally)};"
      f"  gas-dominated points (Vgas^2 > Ud*Vdisk^2+Ub*Vbul^2): {len(gasdom)}")
print(f"  y = g_bar/a0_canon distribution:  median {np.median(ally):.2f},"
      f"  90th pct {np.percentile(ally,90):.1f},  max {ally.max():.1f}")
print(f"  {'cut':>10} {'N(y>cut)':>9} {'N_gasdom(y>cut)':>16} {'R_McG at cut':>13}")
for cut in (1, 3, 10, 30, 50, 100):
    print(f"  {cut:>10} {(ally>cut).sum():>9} {(gasdom>cut).sum():>16} "
          f"{1/float(f_mcg(cut)):>13.3g}")
print(f"  ALT footing (a0={A0A:.3e}): all y values scale by x{A0C/A0A:.3f} -- same picture.")
print()
print(f"  READING (honest): SPARC samples y>30 (R_McG ~ {1/float(f_mcg(30)):.1f}) with "
      f"{(ally>30).sum()} points, y>50 (R_McG ~ {1/float(f_mcg(50)):.0f}) with "
      f"{(ally>50).sum()}, and y>100 (R_McG ~ {1/float(f_mcg(100)):.0f}) with only "
      f"{(ally>100).sum()}. The x100 separation zone is at the EXTREME EDGE of SPARC;")
print("  the bulk of the usable McGaugh-vs-framework contrast sits at y ~ 30-60 where")
print("  R_McG ~ 4-20, carried by a few tens of star-dominated inner points.")
print("  The gas-dominated subsample lives almost entirely at y <~ a few -- it is the")
print("  a0-SLOPE sample, NOT the tail-shape sample. The tail-shape test rides on")
print("  star-dominated high-g points where M/L errors are largest: the quantitative")
print("  discriminating power (with errors) is computed in estimator_theory.py, not here.")
print("\nEXIT 0: all symbolic identities and limits verified.")
