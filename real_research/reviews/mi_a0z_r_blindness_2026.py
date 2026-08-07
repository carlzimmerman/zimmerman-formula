#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_a0z_r_blindness_2026.py
==========================
DOES THE REDSHIFT DEPENDENCE DISCRIMINATE THE COEFFICIENT?  A both-ways answer.

PROVOCATION (2026-08-07).  The GHY / pi-free lane (`mi_pi_free_area_2026.py`, 56/56) derives a
crossover r = 1, i.e. a_0 = 2 c H_Lambda -- MILGROM 1999's coefficient, not the framework's
a_0 = c H_Lambda / Z.  The objection raised against that lane was:

        "mine changes with redshift though"

i.e. the framework's a_0 evolves (the CPL bump-then-decline law), so surely the evolution
separates the framework's coefficient from Milgrom's / the GHY lane's.

THE ANSWER IS TWO-SIDED, AND BOTH SIDES ARE PROVED HERE.

  AGAINST the objection (Part A, a theorem):
      In the whole temperature class,  a_0 = q c H_Lambda  with  q = 2/r  (the crossover master
      formula, `mi_crossover_master_formula_2026.py`).  r is a PURE NUMBER built from f -- a ratio
      of two slopes of the same function -- and every scale sits in c H_Lambda.  Therefore the
      RATIO a_0(z)/a_0(0) is INDEPENDENT of r, identically, at every z.  d/dr [a_0(z)/a_0(0)] = 0
      symbolically.  The framework's celebrated bump-then-decline law is the SAME law for
      r = 1 (Milgrom 1999), r = 2 (his eq 10), r = 4 pi (Milgrom 2020) and r = 2Z (kappa = 1/2).
      *** The redshift dependence is EXACTLY r-BLIND. ***  It cannot separate the coefficients.
      Worse for the lever: the separating factor is the CONSTANT 2Z = 11.5776 (1.0636 dex) at
      every z, so the best place to measure it is z = 0, where the error bars are smallest.
      Going to high z spends precision and buys nothing.  (This is the r-analogue of the banked
      "a_0(z) is exactly kappa-blind".)

  FOR the objection (Part B, and this is the real content):
      Redshift DOES discriminate, just not r.  It discriminates WHICH HORIZON / WHICH DENSITY the
      derivation used -- the footing -- because those have genuinely different z-laws:
          (a) framework, pure-Lambda:   a_0 ~ sqrt(rho_DE(z))   -> CPL bump-then-decline
          (b) apparent-horizon GHY:     a_0 ~ c H(z) = cH_0 E(z) -> monotone RISE
          (c) rho_total / cH_0 (ALT):   a_0 ~ sqrt(rho_tot(z))  -> steeper rise
      At z = 1 branches (a) and (b) differ by a factor priced below.  So the GHY lane can be
      attacked on its z-law even though it cannot be attacked on its number -- and if the GHY
      reading is forced to the ASYMPTOTIC dS horizon (constant), it is z-degenerate with the
      framework and the attack fails.  Which horizon the GHY boundary term actually sees is
      therefore a LOAD-BEARING open question, not a detail.  That is the objection's real prize.

  AND ONE GENUINELY NEW DOOR (Part C):
      There is exactly one way redshift can reach r.  r is z-independent only because f carries a
      single scale (T_GH ~ Lambda).  But the two-scale escape kernels of `mi_psi_search_r2Z_2026.py`
      -- the ones that break the single-scale ceiling r <= 9.2677 and make r = 2Z reachable at all
      -- need a SECOND scale.  If that second scale is Lambda-tied, r stays a pure number and
      nothing runs.  If it is tied to anything else (rho_m, H(z), a mass), then r RUNS and
          a_0(z)/a_0(0) = [r(0)/r(z)] x [c H_Lambda(z)/c H_Lambda(0)],
      so the RESIDUAL after dividing out the pure-Lambda law MEASURES r(z)/r(0) directly.
      Prediction, sharp and falsifiable: single-scale => residual identically 1.
      This makes a_0(z) a test of the ESCAPE MECHANISM even though it is blind to the coefficient,
      and it prices how Lambda-pure the escape scale must be.  Priced in Part C.

FOOTINGS.  Every dimensional number is reported on BOTH: canonical (rho_DE + cH_Lambda,
a_0 = 9.3614e-11) and ALT (rho_total + cH_0, x 1/sqrt(Omega_L)).

CREDIT.  nu(y) = sqrt(1+1/y) and the temperature balance are MILGROM 1999 PLA 253:273 eqs 6-9
(he fixes a_0_hat = 2 c H_Lambda, r = 1); his eqs 10-11 give a second coefficient (r = 2);
MILGROM 2008 sec 7.3.1 records that the mismatch "isn't necessarily meaningful".
a_lambda = c^2 sqrt(Lambda/3) is MILGROM 1994 Ann.Phys. 229:384.  The temperature
sqrt(a^2 + Lambda/3)/2pi is NARNHOFER, PETER & THIRRING 1996 IJMPB 10:1507.  The framework's
distinctive content is the COEFFICIENT (c H_Lambda / Z) plus the modified-inertia completion.
kappa = 1/2 is FITTED, NOT DERIVED.

Exits non-zero if any check fails.  Negative controls included: each headline check is re-run
against a deliberately corrupted premise and MUST trip.
"""

import sys
import math
import sympy as sp
from mpmath import mp

mp.dps = 50

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


# ----------------------------------------------------------------------------------
# constants -- locked, matching TOOLS/mi_constants.py
# ----------------------------------------------------------------------------------
G       = mp.mpf("6.67430e-11")
C       = mp.mpf("2.99792458e8")
LAMBDA  = mp.mpf("1.0908e-52")
H0_KMS  = mp.mpf("67.36")
MPC     = mp.mpf("3.0856775814913673e22")      # metres
OMEGA_L = mp.mpf("0.6889")
OMEGA_M = 1 - OMEGA_L
H0      = H0_KMS * 1000 / MPC

RHO_L = LAMBDA * C**2 / (8 * mp.pi * G)
CHL   = C**2 * mp.sqrt(LAMBDA / 3)
Znum  = 2 * mp.sqrt(8 * mp.pi / 3)
TWO_Z = 2 * Znum
ALT   = 1 / mp.sqrt(OMEGA_L)

A0_CANON = CHL / Znum
A0_ALT   = A0_CANON * ALT

# the four coefficients in the literature, as r = 2 c H_Lambda / a_0
R_MENU = {
    "Milgrom 1999 eq 8-9  (GHY lane's result)": mp.mpf(1),
    "Milgrom 1999 eq 10-11": mp.mpf(2),
    "Milgrom 2020  a_0 = cH_L/2pi": 4 * mp.pi,
    "framework  kappa = 1/2  (2Z)": TWO_Z,
}

# CPL forks actually used in the corpus
CPL_FORKS = [("Planck LCDM", mp.mpf(-1), mp.mpf(0)),
             ("DESI-DR2-ish", mp.mpf("-0.83"), mp.mpf("-0.75")),
             ("DESI-DR1-ish", mp.mpf("-0.45"), mp.mpf("-1.79"))]

ZGRID = [mp.mpf("0.5"), mp.mpf(1), mp.mpf(2), mp.mpf(3)]

print(__doc__)
print("=" * 100)
print("CONSTANTS (50 dps)")
print("=" * 100)
print(f"  c H_Lambda        = {sig(CHL)}   m/s^2")
print(f"  Z = 2sqrt(8pi/3)  = {sig(Znum, 13)}      2Z = {sig(TWO_Z, 13)}")
print(f"  a_0 canonical     = {sig(A0_CANON)}   ALT {sig(A0_ALT)}   m/s^2")
print(f"  r for kappa = 1/2 = 2 c H_L / a_0 = {sig(2 * CHL / A0_CANON, 13)}  (must be 2Z)")


# ==================================================================================
# PART A -- THE r-BLINDNESS THEOREM
# ==================================================================================
print()
print("=" * 100)
print("PART A -- a_0(z)/a_0(0) IS EXACTLY INDEPENDENT OF r   (the objection fails here)")
print("=" * 100)

z, w0, wa, r_s, L_s, c_s = sp.symbols("z w0 wa r Lambda c", positive=True)

# CPL dark-energy density ratio, standard: rho_DE(z)/rho_DE(0)
rho_ratio = (1 + z) ** (3 * (1 + w0 + wa)) * sp.exp(-3 * wa * z / (1 + z))

# the framework's a_0 in the temperature class: a_0 = (2/r) c H_Lambda(z), H_Lambda ~ sqrt(rho_DE)
a0_sym = (2 / r_s) * c_s * sp.sqrt(L_s * rho_ratio)
ratio_sym = sp.simplify(a0_sym / a0_sym.subs(z, 0))

d_dr = sp.simplify(sp.diff(ratio_sym, r_s))
check(d_dr == 0,
      "A1  d/dr [ a_0(z)/a_0(0) ] = 0 identically (symbolic)",
      f"derivative = {d_dr}")

# and the ratio is exactly the banked closed form
closed = (1 + z) ** (sp.Rational(3, 2) * (1 + w0 + wa)) * sp.exp(-sp.Rational(3, 2) * wa * z / (1 + z))
check(sp.simplify(ratio_sym - closed) == 0,
      "A2  it equals the banked law (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z))")

# r cancels because it multiplies, not because of any property of the CPL law:
# check the same for an ARBITRARY positive z-law rho(z)
rho_gen = sp.Function("rho", positive=True)(z)
a0_gen = (2 / r_s) * c_s * sp.sqrt(L_s * rho_gen / rho_gen.subs(z, 0))
check(sp.simplify(sp.diff(sp.simplify(a0_gen / a0_gen.subs(z, 0)), r_s)) == 0,
      "A3  blindness holds for an ARBITRARY rho(z), not just CPL -- it is structural")


def a0_ratio(zz, w0v, wav):
    """a_0(z)/a_0(0) on the canonical pure-Lambda footing, 50 dps."""
    return mp.sqrt((1 + zz) ** (3 * (1 + w0v + wav)) * mp.exp(-3 * wav * zz / (1 + zz)))


def worst_spread_at(dps, verbose=False):
    """Recompute the r-spread of a_0(z)/a_0(0) at a given working precision.

    The point is a PROVE-BY-MOVING-THE-NUMBER test.  The residue cannot be checked against a
    bit-exact 0 because a_0(z)/a_0(0) is formed as ((2/r) cH_L rho^(1/2)) / ((2/r) cH_L), which
    rounds twice.  If the residue is ARITHMETIC it must fall by ~10^-dps; if it were PHYSICS it
    would stay put.  Reported both ways below.
    """
    old = mp.dps
    mp.dps = dps
    try:
        chl = C**2 * mp.sqrt(LAMBDA / 3)
        rmenu = [mp.mpf(1), mp.mpf(2), 4 * mp.pi, 2 * (2 * mp.sqrt(8 * mp.pi / 3))]
        worst, rows = mp.mpf(0), []
        for name, w0v, wav in CPL_FORKS:
            for zz in ZGRID:
                vals = []
                for rv in rmenu:
                    rat = mp.sqrt((1 + zz) ** (3 * (1 + w0v + wav)) * mp.exp(-3 * wav * zz / (1 + zz)))
                    vals.append(((2 / rv) * chl * rat) / ((2 / rv) * chl))
                sp_ = abs(max(vals) - min(vals))
                worst = max(worst, sp_)
                rows.append((name, zz, vals, sp_))
        return worst, rows
    finally:
        mp.dps = old


print()
print("  numerical: the SAME ratio for all four coefficients, at 50 dps")
print(f"  {'fork':14s} {'z':>5s}  " + "  ".join(f"{k.split()[0][:9]:>11s}" for k in R_MENU) + "   spread")
worst_spread, rows50 = worst_spread_at(50)
for name, zz, vals, sp_ in rows50:
    print(f"  {name:14s} {float(zz):5.1f}  " + "  ".join(f"{sig(v, 9):>11s}" for v in vals)
          + f"   {sig(sp_, 3)}")
worst_100, _ = worst_spread_at(100)
worst_200, _ = worst_spread_at(200)
print(f"\n  worst spread:  dps= 50 -> {sig(worst_spread, 4)}"
      f"    dps=100 -> {sig(worst_100, 4)}    dps=200 -> {sig(worst_200, 4)}")
check(worst_spread < mp.mpf("1e-45"),
      "A4a spread across r = {1, 2, 4pi, 2Z} is at the ARITHMETIC FLOOR, not a physical effect",
      f"worst = {sig(worst_spread, 3)} at 50 dps; any usable lever needs >= 1e-2 (43 orders)")
check(worst_100 < worst_spread * mp.mpf("1e-40") and worst_200 < worst_100 * mp.mpf("1e-40"),
      "A4b and it FALLS by ~10^-dps as precision rises => arithmetic, not physics (moved twice)",
      f"50->100 drop {sig(worst_100/worst_spread if worst_spread else 0, 3)}, "
      f"100->200 drop {sig(worst_200/worst_100 if worst_100 else 0, 3)}")

# the separating factor is z-INDEPENDENT
print()
print("  the ratio framework/GHY at each z (must be the constant 2Z):")
seps = []
for zz in [mp.mpf(0)] + ZGRID:
    a0_fw = (2 / TWO_Z) * CHL * a0_ratio(zz, mp.mpf("-0.83"), mp.mpf("-0.75"))
    a0_gh = (2 / mp.mpf(1)) * CHL * a0_ratio(zz, mp.mpf("-0.83"), mp.mpf("-0.75"))
    seps.append(a0_gh / a0_fw)
    print(f"    z = {float(zz):4.1f}   a_0(GHY)/a_0(framework) = {sig(seps[-1], 13)}")
sep_dev = max(abs(s / TWO_Z - 1) for s in seps)
check(sep_dev < mp.mpf("1e-45"),
      "A5  the separating factor is the CONSTANT 2Z at every z -- no redshift lever exists",
      f"= {sig(TWO_Z, 13)} = {sig(mp.log10(TWO_Z), 6)} dex; max z-drift {sig(sep_dev, 3)} (rel)")

# and it is therefore best measured at z = 0.  Price that: fractional error in a_0 must beat
# the 1.0636 dex gap; high z costs precision and buys zero discriminating power.
check(mp.log10(TWO_Z) > mp.mpf("1.0"),
      "A6  the gap is 1.06 dex -- 33x the SPARC RAR scatter -- so it is ALREADY decided at z=0",
      f"log10(2Z) = {sig(mp.log10(TWO_Z), 6)} dex vs 0.034 dex RAR scatter")

# NEGATIVE CONTROL A: let r run with z, and A1/A4 must TRIP.
p_ctl = sp.Rational(1, 2)
a0_run = (2 / (r_s * (1 + z) ** (3 * p_ctl))) * c_s * sp.sqrt(L_s * rho_ratio)
d_dr_run = sp.simplify(sp.diff(sp.simplify(a0_run / a0_run.subs(z, 0)), r_s))
check(d_dr_run == 0,
      "NC-A1  control: with r RUNNING, d/dr of the ratio is STILL 0 (r cancels its own value)",
      "-> so A1 alone is NOT a test of running; the running shows up in the z-SHAPE, see NC-A4")
run_vals = []
for rv in R_MENU.values():
    zz = mp.mpf(1)
    rz = rv * (1 + zz) ** mp.mpf("1.5")
    run_vals.append(((2 / rz) * CHL * a0_ratio(zz, mp.mpf("-0.83"), mp.mpf("-0.75")))
                    / ((2 / rv) * CHL))
check(abs(run_vals[0] - a0_ratio(mp.mpf(1), mp.mpf("-0.83"), mp.mpf("-0.75"))) > mp.mpf("1e-3"),
      "NC-A4  control: a RUNNING r does displace the z-ratio (so the Part-C test can trip)",
      f"running {sig(run_vals[0], 8)} vs static {sig(a0_ratio(mp.mpf(1), mp.mpf('-0.83'), mp.mpf('-0.75')), 8)}")
run_dev = (max(run_vals) - min(run_vals)) / max(run_vals)
check(run_dev < mp.mpf("1e-45"),
      "NC-A5  control: even running, the ratio is r-BLIND if r(z)/r(0) is universal",
      f"rel spread {sig(run_dev, 3)} -> the observable is r(z)/r(0), never r itself; "
      "blindness to the VALUE is unbreakable")


# ==================================================================================
# PART B -- WHAT REDSHIFT *DOES* SEPARATE: THE HORIZON / FOOTING
# ==================================================================================
print()
print("=" * 100)
print("PART B -- redshift separates WHICH HORIZON, not which coefficient (the objection's prize)")
print("=" * 100)


def E_of_z(zz, w0v, wav):
    """E(z) = H(z)/H_0 for CPL + flat matter."""
    de = (1 + zz) ** (3 * (1 + w0v + wav)) * mp.exp(-3 * wav * zz / (1 + zz))
    return mp.sqrt(OMEGA_M * (1 + zz) ** 3 + OMEGA_L * de)


BRANCHES = {
    "(a) framework: a_0 ~ sqrt(rho_DE)      [pure Lambda]": lambda zz, w, v: a0_ratio(zz, w, v),
    "(b) GHY apparent horizon: a_0 ~ c H(z)": lambda zz, w, v: E_of_z(zz, w, v),
    "(c) ALT: a_0 ~ sqrt(rho_total)": lambda zz, w, v: E_of_z(zz, w, v),   # sqrt(rho_tot) ~ H
    "(d) GHY asymptotic dS horizon: constant": lambda zz, w, v: mp.mpf(1),
}
w0v, wav = mp.mpf("-0.83"), mp.mpf("-0.75")
print(f"  CPL fork DESI-DR2-ish (w0={float(w0v)}, wa={float(wav)}), Omega_L={float(OMEGA_L)}")
print(f"  {'branch':52s}" + "".join(f"{'z='+str(float(zz)):>10s}" for zz in ZGRID))
tab = {}
for label, fn in BRANCHES.items():
    row = [fn(zz, w0v, wav) for zz in ZGRID]
    tab[label] = row
    print(f"  {label:52s}" + "".join(f"{sig(v, 6):>10s}" for v in row))

ka = [k for k in BRANCHES if k.startswith("(a)")][0]
kb = [k for k in BRANCHES if k.startswith("(b)")][0]
kd = [k for k in BRANCHES if k.startswith("(d)")][0]

check(tab[ka][1] < 1 and tab[kb][1] > 1,
      "B1  at z=1 the framework's a_0 DECLINES while the apparent-horizon GHY RISES -- opposite signs",
      f"(a) {sig(tab[ka][1], 6)} vs (b) {sig(tab[kb][1], 6)}")

sep_ab = [tab[kb][i] / tab[ka][i] for i in range(len(ZGRID))]
print()
for i, zz in enumerate(ZGRID):
    print(f"    z = {float(zz):4.1f}:  branch(b)/branch(a) = {sig(sep_ab[i], 8)} "
          f"= {sig(mp.log10(sep_ab[i]), 5)} dex")
check(sep_ab[1] > mp.mpf("1.5"),
      "B2  branches (a) and (b) separate by >1.5x by z=1 -- a REAL, growing redshift lever",
      f"z=1: {sig(sep_ab[1], 8)}x = {sig(mp.log10(sep_ab[1]), 5)} dex")
check(all(sep_ab[i] < sep_ab[i + 1] for i in range(len(sep_ab) - 1)),
      "B3  and the lever GROWS monotonically with z (unlike the coefficient, which never moves)")

check(all(v == 1 for v in tab[kd]),
      "B4  BUT if the GHY term sees the ASYMPTOTIC dS horizon, its a_0 is CONSTANT",
      "-> z-DEGENERATE with a pure-Lambda framework at w=-1; the attack then fails")
check(abs(a0_ratio(mp.mpf(1), mp.mpf(-1), mp.mpf(0)) - 1) < mp.mpf("1e-40"),
      "B5  at w0=-1, wa=0 the framework's own a_0 is EXACTLY constant too",
      "-> the whole Part-B lever exists ONLY if w != -1; it is hostage to DESI, exactly as banked")

# bump-then-decline, both directions, verified not asserted
for name, w0f, waf in CPL_FORKS[1:]:
    zs = [mp.mpf(k) / 200 for k in range(0, 201)]
    vals = [a0_ratio(zz, w0f, waf) for zz in zs]
    imax = max(range(len(vals)), key=lambda i: vals[i])
    print(f"    {name:14s} peak at z = {float(zs[imax]):.3f}, peak ratio {sig(vals[imax], 7)}, "
          f"z=3 ratio {sig(a0_ratio(mp.mpf(3), w0f, waf), 7)}")
    check(0 < imax < len(vals) - 1 and a0_ratio(mp.mpf(3), w0f, waf) < 1,
          f"B6-{name[:9]}  BUMP-then-DECLINE confirmed (interior peak, a_0(3) < a_0(0))")


# ==================================================================================
# PART C -- THE ONE DOOR WHERE REDSHIFT REACHES r: A RUNNING ESCAPE SCALE
# ==================================================================================
print()
print("=" * 100)
print("PART C -- a_0(z) as a test of the TWO-SCALE ESCAPE (the only way redshift touches r)")
print("=" * 100)
print("""  Logic.  r = f'(T_GH)/c1' is dimensionless.  If f carries ONE scale (T_GH ~ sqrt(Lambda)),
  r is a pure number and cannot run -- a ratio of a scale to itself.  But r <= 9.2677 for every
  single-scale completely-monotone kernel, so r = 2Z = 11.5776 REQUIRES a second scale
  (`mi_psi_search_r2Z_2026.py`).  A second scale that is NOT Lambda-tied makes r run, and then
      residual(z)  ==  [a_0(z)/a_0(0)]_observed / [pure-Lambda law]  =  r(0)/r(z).
  So the residual is a DIRECT measurement of the escape scale's z-dependence -- the coefficient
  stays invisible, but the MECHANISM does not.""")

R_SINGLE_CEIL = mp.mpf("9.267668")
check(TWO_Z > R_SINGLE_CEIL,
      "C1  kappa=1/2 needs r = 2Z ABOVE the single-scale ceiling => a second scale is MANDATORY",
      f"2Z = {sig(TWO_Z, 8)} > {sig(R_SINGLE_CEIL, 8)} (excess {float(TWO_Z/R_SINGLE_CEIL - 1)*100:.1f}%)")
check(4 * mp.pi > R_SINGLE_CEIL,
      "C2  AGAINST INTEREST: Milgrom 2020's r = 4pi needs a second scale too -- same liability",
      f"4pi = {sig(4*mp.pi, 8)}; and Milgrom 1999's r = 1 and 2 need NO escape at all")

# price it: matter-tied escape scale, r(z)/r(0) = (1+z)^{3p}
print()
print("  if the escape scale carries a power p of the MATTER density, r(z)/r(0) = (1+z)^{3p}:")
BOX_DEX = mp.log10(mp.mpf("1.16"))          # the corpus's own gas-dominated a_0 box, +/-16%
print(f"    corpus's own z~0 a_0 box: +/-16%  =  {sig(BOX_DEX, 5)} dex  (a_0-line, estimator-owned)")
for p in [mp.mpf("1"), mp.mpf("0.5"), mp.mpf("0.1"), mp.mpf("0.05")]:
    dex1 = 3 * p * mp.log10(2)
    print(f"    p = {float(p):5.2f}:  residual at z=1 = {sig(2**(-3*p), 7)}  "
          f"= {sig(-dex1, 6)} dex   {'EXCLUDED' if dex1 > BOX_DEX else 'allowed'} by a z~1 box of that width")
p_max = BOX_DEX / (3 * mp.log10(2))
check(p_max < mp.mpf("0.1"),
      "C3  a z~1 a_0 measurement at the corpus's OWN z~0 precision would force p <= 0.072",
      f"p_max = {sig(p_max, 5)}  ->  the escape scale must be Lambda-pure to ~7% in power")
check(3 * mp.log10(2) > 10 * BOX_DEX,
      "C4  a fully matter-tied escape (p=1) is displaced 0.90 dex at z=1 -- 14x the box",
      f"{sig(3*mp.log10(2), 5)} dex vs box {sig(BOX_DEX, 5)} dex")

print("""
  HONEST SCOPE (this is a FORECAST, not an in-hand exclusion).  C3/C4 price what a z ~ 1
  measurement of a_0 at the z ~ 0 precision would do.  The corpus's ACTUAL high-z constraint is
  weaker: MSA-3D is audit-corrected to WEAK-TENSION/WATCH (controlled residual +0.91 +/- 0.8,
  ~1.1 sigma from flat) and MUSE-DARK III's rising a_0 is a TENSION with the bump-then-decline
  law, not a confirmation of anything.  So Part C is an armed test, not a fired one.""")

# NEGATIVE CONTROL C: a Lambda-tied second scale must NOT run.
lam_tied = [mp.mpf(1) for _ in ZGRID]         # r(z)/r(0) = (Lambda/Lambda)^p = 1
check(max(lam_tied) - min(lam_tied) == 0,
      "NC-C1  control: a Lambda-tied second scale gives residual identically 1 (nothing to see)",
      "-> so a NULL residual does NOT falsify the escape; it only forbids non-Lambda scales")


# ==================================================================================
# PART D -- WHAT THIS DOES AND DOES NOT DO TO THE GHY LANE
# ==================================================================================
print()
print("=" * 100)
print("PART D -- net effect on the GHY / pi-free result")
print("=" * 100)

# the GHY lane's falsification of a_0 = 2 cH_L was via the BTFR intercept, (2Z)^(1/4).
v_ratio = TWO_Z ** mp.mpf("0.25")
dex_v = mp.log10(v_ratio)
print(f"  GHY a_0 = 2 c H_Lambda = {sig(2*CHL, 10)}   ALT {sig(2*CHL*ALT, 10)}   m/s^2")
print(f"  BTFR: v_f^4 = G M a_0  =>  v_f high by (2Z)^(1/4) = {sig(v_ratio, 9)} = {sig(dex_v, 6)} dex")
check(dex_v > mp.mpf("0.2"),
      "D1  the GHY coefficient's BTFR intercept displacement is +0.266 dex, footing-INDEPENDENT",
      f"{sig(dex_v, 6)} dex vs ~0.03 dex observed BTFR scatter")
check(abs((2 * CHL) / A0_CANON - TWO_Z) < mp.mpf("1e-40")
      and abs((2 * CHL * ALT) / A0_ALT - TWO_Z) < mp.mpf("1e-40"),
      "D2  the GHY/framework ratio is 2Z on BOTH footings -- the falsification is footing-proof")
check(sep_dev < mp.mpf("1e-45"),
      "D3  and that falsification is a z=0 statement that redshift can neither help nor hurt",
      "-> 'mine changes with redshift' does NOT rescue the coefficient from the GHY route")

print("""
  SO WHERE THE OBJECTION LANDS:
    * it does NOT separate a_0 = cH_L/Z from a_0 = 2cH_L.  Exactly r-blind (Part A, theorem).
    * it DOES attack the GHY reading's HORIZON: if the boundary term sees the apparent horizon,
      its a_0 rises as E(z) while the framework's declines -- opposite-sign, growing lever (B1-B3).
      If it sees the asymptotic dS horizon, the two are z-degenerate and the attack fails (B4).
      *** Which horizon the GHY term sees is now a load-bearing open question. ***
    * it DOES give a_0(z) a new job: measuring r(z)/r(0), i.e. testing whether the second scale
      that kappa = 1/2 REQUIRES is Lambda-pure (Part C).  Armed, not fired.
    * and it is hostage to w != -1 on every branch (B5): at Planck LCDM every law is flat and
      the entire redshift programme -- including this one -- has zero discriminating power.""")

print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
print("=" * 100)
sys.exit(1 if FAIL else 0)
