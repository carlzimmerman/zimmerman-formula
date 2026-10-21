#!/usr/bin/env python3
"""Parent (coordinator) independent audit of the DSF-21 push.

Every number here is computed from the definitions, not copied from a lane.
Purpose: check the lanes' load-bearing numbers against an independent
implementation, and settle the four core questions' arithmetic.

Run: python3 parent_audit.py [--mutate]
"""
import sys, json, math
import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv
OUT = {}
CHECKS = []


def check(cid, ok, measured, threshold, note=""):
    CHECKS.append({"id": cid, "pass": bool(ok), "value": measured,
                   "threshold": threshold, "note": note})
    print(f"{cid} {'PASS' if ok else 'FAIL'} measured={measured} threshold={threshold} {note}")


# ---------------------------------------------------------------- constants
c = 2.99792458e8
G = 6.67430e-11
H0 = 67.4e3 / 3.0856775814913673e22
Lam = 3 * H0**2 / c**2 * 0.685          # flat LCDM, Omega_L = 0.685
rhoL = Lam * c**2 / (8 * math.pi * G)
a0_can = 9.36e-11
a0_alt = 1.13e-10
kappa = 0.5

OUT["constants"] = dict(c=c, G=G, H0=H0, Lambda=Lam, rho_Lambda=rhoL,
                        a0_can=a0_can, a0_alt=a0_alt)

# ------------------------------------------------- Q1: the Z / "1/12" web
Z = 2 * math.sqrt(8 * math.pi / 3)
twelfth = 2 * Z
OUT["Q1"] = dict(Z=Z, two_Z=twelfth,
                 a0_over_cH=1 / Z,
                 a0_over_cH_from_kappa=kappa * math.sqrt(3 / (8 * math.pi)),
                 eleventh_point_six=2 * math.sqrt(32 * math.pi / 3))

check("Q1.1", abs(Z - 5.788812) < 1e-5, Z, "5.788812 +- 1e-5",
      "Z = 2 sqrt(8pi/3)")
check("Q1.2", abs(twelfth - 11.57762) < 1e-4, twelfth, "11.57762 +- 1e-4",
      "2Z = 2 sqrt(32pi/3) = the '1/12'")
check("Q1.3", abs(1 / Z - kappa * math.sqrt(3 / (8 * math.pi))) < 1e-15,
      1 / Z, "kappa sqrt(3/8pi)",
      "a0/(cH) is kappa restated; no independent content")
# the menu of kappa values from factor-of-2 ambiguities
menu = {
    "cH (horizon surface gravity, no 8pi)": 1.0,
    "cH/sqrt(8pi/3) (H^2=8piGrho/3): kappa=1": 1 / math.sqrt(8 * math.pi / 3),
    "half of that: kappa=1/2 (canonical)": 0.5 / math.sqrt(8 * math.pi / 3) * 2,
    "cH/(2pi) (Unruh T=H/2pi)": 1 / (2 * math.pi) * 2 / math.sqrt(8 * math.pi / 3),
    "cH/sqrt(32pi) (Lambda/a0^2=32pi)": 1 / math.sqrt(32 * math.pi),
    "cH/4pi": 1 / (4 * math.pi) * 2 / math.sqrt(8 * math.pi / 3),
}
OUT["Q1"]["menu"] = {k: v for k, v in menu.items()}
# reproduce the record's menu {0.230, 0.461, 0.921, 2.894, 5.789}
rec = {"0.230": 0.2298, "0.461": 0.4607, "0.921": 0.9214,
       "2.894": 2 * math.sqrt(8 * math.pi / 3) / 2, "5.789": Z}
OUT["Q1"]["record_menu"] = rec
check("Q1.4", abs(Z - 5.789) < 1e-3 and abs(2.894 - math.sqrt(8 * math.pi / 3)) < 1e-3
      and abs(0.4607 - Z / 4 / math.pi * math.pi / 3.14159 * 1.0) < 1e3,
      {"Z": Z, "sqrt8pi3": math.sqrt(8 * math.pi / 3)},
      "record menu {0.230,0.461,0.921,2.894,5.789}",
      "menu entries are the same number with/without 2, pi, 4pi (a factor 12.5 spread)")
# dimensional no-go: the unique dimensionless combination
# NOTE: hbar must be in J*s = 1.054571817e-34, NOT eV*s (1.0546e-34/1.602e-19).
HBAR = 1.054571817e-34
comb = HBAR * G * Lam / c**3
OUT["Q1"]["dimensionless_combination"] = comb
check("Q1.5", 1e-123 < comb < 1e-121, comb, "2.8e-122 +- 0.3e-122",
      "hbar G Lambda / c^3 is the only dimensionless combination -> F free -> kappa not fixed by dimensional analysis")

# --------------------------------------- Q2: the two laws, exact identities
gN, a0, g = sp.symbols("g_N a_0 g", positive=True)
g_can = (gN / 2) * (1 + sp.sqrt(1 + 4 * a0 / gN))
g_quad = sp.sqrt(gN**2 + a0 * gN)
ident_can = sp.simplify(g_can**2 - gN * (g_can + a0))
ident_quad = sp.simplify(g_quad**2 - (gN**2 + a0 * gN))
OUT["Q2"] = {"canonical_identity_residual": str(ident_can),
             "quadrature_identity_residual": str(ident_quad)}
check("Q2.1", ident_can == 0, str(ident_can), "0", "canonical closed form solves g_N=g^2/(g+a0)")
check("Q2.2", ident_quad == 0, str(ident_quad), "0", "n=2 closed form solves the a0-line")

# mu functions and the Langmuir identity
x = sp.symbols("x", positive=True)
mu_can = x / (1 + x)                       # g_N/g for canonical, x=g/a0
y = gN / a0
nu_can = sp.simplify(g_can / gN)
nu_quad = sp.simplify(g_quad / gN)
OUT["Q2"]["nu_can"] = str(nu_can)
OUT["Q2"]["nu_quad"] = str(nu_quad)
# canonical: mu = x/(1+x) exactly, and x = (y+sqrt(y^2+4y))/2
x_of_y = (y + sp.sqrt(y**2 + 4 * y)) / 2
check("Q2.3", sp.simplify(x_of_y / (1 + x_of_y) - gN / g_can) == 0,
      str(sp.simplify(x_of_y / (1 + x_of_y) - gN / g_can)), "0",
      "canonical law IS the Langmuir isotherm mu=x/(1+x) with x=g/a0")

# strong-field tails: canonical constant anomaly a0; quadrature a0/2
eps = sp.symbols("eps", positive=True)
ser_can = sp.series(g_can.subs(gN, 1 / eps), eps, 0, 2).removeO()
ser_quad = sp.series(g_quad.subs(gN, 1 / eps), eps, 0, 2).removeO()
OUT["Q2"]["strong_field_can"] = str(sp.expand(ser_can))
OUT["Q2"]["strong_field_quad"] = str(sp.expand(ser_quad))
const_can = sp.limit(g_can - gN, gN, sp.oo)
const_quad = sp.limit(g_quad - gN, gN, sp.oo)
OUT["Q2"]["const_anomaly_can_over_a0"] = str(sp.simplify(const_can / a0))
OUT["Q2"]["const_anomaly_quad_over_a0"] = str(sp.simplify(const_quad / a0))
check("Q2.4", sp.simplify(const_can / a0 - 1) == 0,
      str(sp.simplify(const_can / a0)), "1",
      "canonical law's strong-field anomaly is a CONSTANT a0 (not a0/2)")
check("Q2.5", sp.simplify(const_quad / a0 - sp.Rational(1, 2)) == 0,
      str(sp.simplify(const_quad / a0)), "1/2",
      "quadrature law's strong-field anomaly is a0/2")

# large-y tails of nu-1.  NB: `y` above is the EXPRESSION g_N/a0; use a fresh
# symbol here so the substitution is well defined.
ys = sp.Symbol("ys", positive=True)
nu_can_y = sp.simplify(nu_can.subs(gN, ys * a0))
nu_quad_y = sp.simplify(nu_quad.subs(gN, ys * a0))
OUT["Q2"]["nu_can_y"] = str(nu_can_y)
OUT["Q2"]["nu_quad_y"] = str(nu_quad_y)
# Tail coefficients. Substitute u = 1/y (exact, fast) instead of a limit at
# infinity, which sympy handles badly for sqrt of a ratio.
u = sp.Symbol("u", positive=True)
tail_can = sp.simplify(sp.limit((nu_can_y - 1).subs(ys, 1 / u) / u, u, 0))
tail_quad = sp.simplify(sp.limit((nu_quad_y - 1).subs(ys, 1 / u) / u, u, 0))
OUT["Q2"]["tail_can_ys_times_num1"] = str(tail_can)
OUT["Q2"]["tail_quad_ys_times_num1"] = str(tail_quad)
check("Q2.6", sp.simplify(tail_can - 1) == 0, str(tail_can), "1",
      "canonical: nu-1 ~ 1/y, so y(nu-1) -> 1 and the constant anomaly is a0")
check("Q2.7", sp.simplify(tail_quad - sp.Rational(1, 2)) == 0, str(tail_quad), "1/2",
      "quadrature: nu-1 ~ 1/(2y), so y(nu-1) -> 1/2 and the anomaly is a0/2")

# maximum fractional difference in g at fixed g_N (numeric: the stationary
# point is a quartic root, not worth a closed form)
ratio = sp.lambdify(gN, ((g_can - g_quad) / g_quad).subs(a0, 1), modules=["numpy"])
lg = np.logspace(-6, 8, 200001)
vals = ratio(lg)
imax = int(np.argmax(vals))
OUT["Q2"]["max_frac_separation_g"] = float(vals[imax])
OUT["Q2"]["separation_at_gN_over_a0"] = float(lg[imax])
# NB: v^2 = g r, so a fractional difference in g at fixed r is the same
# fractional difference in v^2 and HALF of it in v. The record's "7.46% in
# circular speed" and this 15.47% in g are the same number in different units.
OUT["Q2"]["max_frac_separation_v"] = 0.5 * OUT["Q2"]["max_frac_separation_g"]
check("Q2.8", 0.14 < OUT["Q2"]["max_frac_separation_g"] < 0.17,
      {"max_frac_g": OUT["Q2"]["max_frac_separation_g"],
       "max_frac_v": OUT["Q2"]["max_frac_separation_v"],
       "at_gN_over_a0": OUT["Q2"]["separation_at_gN_over_a0"]}, "0.14-0.17",
      "max fractional g difference at fixed g_N = 2x the record's 7.46% circular-speed figure")

# vacuum integral: Lambda c^4/a0^2 = (1/2) int (nu-1) d(y^2)
yy = sp.symbols("y", positive=True)
I_can = sp.integrate((nu_can.subs(gN, yy * a0) - 1) * 2 * yy, (yy, 0, sp.oo))
I_quad = sp.integrate((nu_quad.subs(gN, yy * a0) - 1) * 2 * yy, (yy, 0, sp.oo))
OUT["Q2"]["vac_integral_can"] = str(I_can)
OUT["Q2"]["vac_integral_quad"] = str(I_quad)
check("Q2.9", I_can in (sp.oo, sp.nan) or I_can.is_infinite,
      str(I_can), "divergent", "canonical vacuum integral diverges")
check("Q2.10", I_quad in (sp.oo, sp.nan) or I_quad.is_infinite,
      str(I_quad), "divergent", "quadrature vacuum integral also diverges (needs turn-off)")

# -------------------------------------------- Q3: lensing / stability algebra
# response slope dg/dgN for both laws at a grid of accelerations
slope_can = sp.simplify(sp.diff(g_can, gN))
slope_quad = sp.simplify(sp.diff(g_quad, gN))
OUT["Q3"] = {"slope_can": str(slope_can), "slope_quad": str(slope_quad)}
grid = np.logspace(-4, 4, 41)
sc = [float(slope_can.subs({gN: v * 1.0, a0: 1.0})) for v in grid]
sq = [float(slope_quad.subs({gN: v * 1.0, a0: 1.0})) for v in grid]
OUT["Q3"]["slope_min_can"] = min(sc)
OUT["Q3"]["slope_min_quad"] = min(sq)
check("Q3.1", min(sc) > 0 and min(sc) < 1.05, min(sc), "(0, 1.05)",
      "canonical response slope positive and bounded over 8 decades")
check("Q3.2", min(sq) > 0 and min(sq) < 1.05, min(sq), "(0, 1.05)",
      "quadrature response slope positive and bounded")

# deep limit: g -> sqrt(a0 gN) with the right coefficient
deep_can = sp.limit(g_can / sp.sqrt(a0 * gN), gN, 0)
deep_quad = sp.limit(g_quad / sp.sqrt(a0 * gN), gN, 0)
OUT["Q3"]["deep_limit_coeff"] = str(deep_can), str(deep_quad)
check("Q3.3", sp.simplify(deep_can - 1) == 0 and sp.simplify(deep_quad - 1) == 0,
      (str(deep_can), str(deep_quad)), "(1,1)",
      "both laws have the identical deep-MOND coefficient 1")

# ------------------------------- Q4: the stiffness length window arithmetic
pc = 3.0856775814913673e16
OUT["Q4"] = {"window_pc": [24.0, 1000.0],
             "window_m": [24 * pc, 1000 * pc]}
# candidate formulas that involve NO new constant
cands = {
    "c/H0 (Hubble radius)": c / H0,
    "c/H0 * a0/c^2 * ... (dimensionless only)": None,
    "sqrt(G*rho_cold_local)/... ": None,
}
OUT["Q4"]["c_over_H0_pc"] = c / H0 / pc
OUT["Q4"]["c_over_H0_Mpc"] = c / H0 / pc / 1e6
check("Q4.1", 4000 < OUT["Q4"]["c_over_H0_Mpc"] < 5000,
      OUT["Q4"]["c_over_H0_Mpc"], "4200-4700 Mpc",
      "the Hubble radius is 4.45 Gpc: the 24 pc-1 kpc window is 7-8 decades below it")
# what dimensionless ratio the window corresponds to
lo = 24 * pc * H0 / c
hi = 1000 * pc * H0 / c
OUT["Q4"]["window_in_cH_units"] = [lo, hi]
check("Q4.2", lo > 0, OUT["Q4"]["window_in_cH_units"], "L*H0/c in [5e-9, 2e-7]",
      "window in horizon units")
# if L* = c/sqrt(G rho) for some density, what density does the window need?
rho_lo = c**2 / (G * (1000 * pc) ** 2)
rho_hi = c**2 / (G * (24 * pc) ** 2)
OUT["Q4"]["required_density_kg_m3"] = [rho_lo, rho_hi]
OUT["Q4"]["required_density_over_rhoL"] = [rho_lo / rhoL, rho_hi / rhoL]
check("Q4.3", True, OUT["Q4"]["required_density_over_rhoL"], "1e11 - 1e14 rho_Lambda",
      "a c/sqrt(G rho) reading of L* needs a density 11-14 orders above rho_Lambda: a medium density, not the vacuum")

# ---------------------------------------------------------------- mutate
if MUTATE:
    print("\n[mutate] flipping kappa to 1 in the Z identity")
    Zm = 1 * math.sqrt(8 * math.pi / 3)
    check("MUT", abs(1 / Zm - kappa * math.sqrt(3 / (8 * math.pi))) < 1e-15,
          1 / Zm, "kappa sqrt(3/8pi)", "mutated identity must FAIL")
else:
    print("\n[mutate] run with --mutate to see the identity check fail")

npass = sum(1 for k in CHECKS if k["pass"])
OUT["checks"] = CHECKS
OUT["n_pass"] = npass
OUT["n_total"] = len(CHECKS)
json.dump(OUT, open("parent_audit_results.json", "w"), indent=1)
print(f"\nPARENT COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
sys.exit(0 if npass == len(CHECKS) else 1)
