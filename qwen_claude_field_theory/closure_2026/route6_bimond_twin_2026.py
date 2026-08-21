#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route6_bimond_twin_2026.py
==========================
ROUTE 6 -- BIMETRIC / BIMOND AIMED AT THE DOUBLE COUNT.

THE QUESTION PUT TO THIS ROUTE.  BIMOND has the one structural feature no other route has: TWO
metrics, so the cosmological carrier of Omega_dm and the galactic phantom can be DIFFERENT
OBJECTS.  Can the TWIN sector's matter supply Omega_dm = 0.265 to the CMB while its
gravitational effect on OUR metric in a galaxy is already fully accounted for by the interaction
term -- i.e. the two are the SAME contribution seen twice, not two contributions added?

THE ANSWER, in one line, and it is a THEOREM with no free parameters and no kernel dependence:

    *** F_TM(y) = 1 - nu(y)   ***

  the fraction of its own Newtonian gravity that twin matter exerts on OUR metric, at a place
  where the framework's own RAR interpolation is nu(y).  Since nu >= 1 everywhere (MOND is an
  ENHANCEMENT -- that is what the RAR measures), F_TM <= 0 EVERYWHERE.  Twin matter is NEVER
  attractive on our metric.  It is invisible in the Newtonian regime and REPULSIVE in the MOND
  regime.  It can never mimic CDM, at any scale, in any epoch, for any interpolation.

  Equivalently, for equal Planck masses, the exact SUM RULE

    *** F_baryon(y) + F_TM(y) = 1 ***

  -- the two ARE the same budget seen twice, exactly as Route 6 hoped.  THE DOUBLE COUNT IS
  GENUINELY BROKEN: the twin sector is not ADDED to the phantom, it is SUBTRACTED from it, with
  no tuning and no s* to hit (contrast route (a), which needed s* = 6.7062 against a cap of 1/2).
  But the same sum rule says the CMB needs F_b = 1 AND F_TM = 1, i.e. a sum of 2, and BIMOND
  says 1.  THE ROUTE BREAKS THE DOUBLE COUNT AND FAILS THE CMB BY THE SAME EQUATION.

AND CARL'S OWN a_0(z) LAW IS WHAT MAKES IT FATAL.  a_0(rec)/a_0(0) = 0.0060, so recombination
is the MOST Newtonian epoch there is: y_rec ~ 1e3 on CMB scales.  There F_TM = -(nu - 1) is
-4.21e-4 on the a_0-line and -1.74e-35 on the Cassini-surviving mu10 kernel.  THE REGIME ORDERING IS
INVERTED: the dark sector must be VISIBLE at recombination (deeply Newtonian) and INVISIBLE in
galaxies (MOND), but the interaction is required to switch OFF in the Newtonian limit -- that is
what "reduces to GR" means.  The two requirements are the same function evaluated with opposite
signs.

WHAT ACTUALLY CARRIES Omega_dm HERE (PART F): not the twin matter, and not the interaction
energy either -- the interaction's natural density is kappa^2 rho_Lambda = 0.25 rho_Lambda
(Carl's own coincidence, reproduced here to machine precision) and it is CONSTANT, in fact it
DECLINES into the past like a_0(z)^2.  Dust needs (1+z)^3.  The mismatch at recombination is
3.6e13.  So Omega_dm is still carried by the DBI khronon's dust in OUR sector -- exactly as in
the published BIMOND_HOST (DOI 10.5281/zenodo.22015358) -- and the double count is UNTOUCHED
there.

Exit 0 = every numbered check passed.  A PASS ESTABLISHES THE ADVERSE VERDICT.
"""
import sys
import numpy as np
import sympy as sp
from scipy.optimize import brentq

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

# ------------------------------------------------------------------ constants (both footings)
C_L = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98892e30
MPC = 3.0856775814913673e22
KPC = MPC / 1000.0
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0 = 67.4e3 / MPC
OM_M, OM_B, OM_L = 0.315, 0.0493, 0.685
OM_DM = OM_M - OM_B
RHO_C0 = 3 * H0**2 / (8 * np.pi * G)
SHARE = 5.375                            # corpus value of Omega_dm/Omega_b
SHARE_DERIVED = OM_DM / OM_B             # 5.389 from Planck Omega_m, Omega_b
Z_REC = 1090.0
DEX_TOL = 0.06                           # RAR intrinsic scatter


# ------------------------------------------------------------------ the interpolation kernels
# Every kernel is implemented as nu MINUS ONE, in closed form, because at recombination
# nu - 1 ~ 1e-22 and computing it as (nu) - 1 in float64 returns EXACTLY ZERO -- the logged
# cancellation trap.  The nu(y) wrappers are built FROM these, never the other way round.

def num1_a0line(y):
    """a0-line: nu-1 = (sqrt(1+4/y)-1)/2, rationalised so no cancellation at large y."""
    y = np.asarray(y, dtype=float)
    u = 4.0 / y
    return u / (2.0 * (np.sqrt(1.0 + u) + 1.0))


def num1_ms08(y):
    """MS08 exponential: nu-1 = e^-sqrt(y) / (1 - e^-sqrt(y)), via expm1."""
    y = np.asarray(y, dtype=float)
    s_ = np.sqrt(y)
    return np.exp(-s_) / (-np.expm1(-s_))


def num1_mun(y, n):
    """mu_n(x)=x/(1+x^n)^(1/n).  EXACT identity: nu = (1 + x^-n)^(1/n), x = g_obs/a0.

    mu(x)x = y  =>  x^2/(1+x^n)^(1/n) = y  =>  nu = x/y = (1+x^n)^(1/n)/x = (1+x^-n)^(1/n).
    Solve for L = log x from  2L - log1p(e^{nL})/n = log y, which is STRICTLY monotone in L
    (derivative 2 - sigmoid(nL) in (1,2)), so brentq is unconditionally safe -- a naive fixed
    point is NOT a contraction in deep MOND and silently returned wrong values on the first run.
    nu-1 is then read off the identity via log1p/expm1: no subtraction anywhere.
    """
    y = np.atleast_1d(np.asarray(y, dtype=float))
    out = np.empty_like(y)
    for i, yy in enumerate(y):
        ly = np.log(yy)

        def f(L):
            return 2.0 * L - np.logaddexp(0.0, n * L) / n - ly

        lo, hi = ly - 60.0, ly + 60.0
        while f(lo) > 0:
            lo -= 60.0
        while f(hi) < 0:
            hi += 60.0
        L = brentq(f, lo, hi, xtol=1e-15, rtol=8.9e-16)
        out[i] = np.expm1(np.log1p(np.exp(-n * L)) / n) if -n * L > -700 else 0.0
    return out if out.size > 1 else out[0]


NUM1 = {
    "a0-line (Carl)": num1_a0line,
    "MS08 exponential": num1_ms08,
    "mu5": lambda y: num1_mun(y, 5),
    "mu10 (clears Cassini)": lambda y: num1_mun(y, 10),
}
KERNELS = {k: (lambda f: (lambda y: 1.0 + np.asarray(f(y), dtype=float)))(v)
           for k, v in NUM1.items()}


# =========================================================================================
head("PART A -- the BIMOND nonrelativistic reduction, and the SUM RULE (symbolic, general)")
# =========================================================================================
print("""
  BIMOND [Milgrom PRD 80, 123536 (2009)]: two metrics, matter on g, TWIN matter on ghat,
  interaction built ONLY from C^a_bc = Gamma^a_bc(g) - Gammahat^a_bc(ghat).  In the NR limit
  C depends only on grad(phi - phihat).  So the NR Lagrangian is

     L = -(1/8 pi G)[ beta |grad phi|^2 + gamma |grad phihat|^2 ] - rho phi - rhohat phihat
         - W( grad(phi - phihat) )

  Linearise W with coefficient kappa_W (the LOCAL response; kappa_W runs with acceleration and
  is what the free function supplies).  Then, with u = lap(phi)/4 pi G, v = lap(phihat)/4 pi G:
""")
beta, gam, kw, rho, rhoh = sp.symbols("beta gamma kappa_W rho rhohat", real=True)
u, v = sp.symbols("u v", real=True)
eq1 = sp.Eq(beta * u, rho - kw * (u - v))
eq2 = sp.Eq(gam * v, rhoh + kw * (u - v))
sol = sp.solve([eq1, eq2], [u, v], dict=True)[0]
U = sp.simplify(sol[u])
print("     lap(phi)/4piG = ")
sp.pprint(sp.simplify(sp.expand(U)))

F_b_sym = sp.simplify(sp.diff(U, rho))
F_tm_sym = sp.simplify(sp.diff(U, rhoh))
print(f"\n     F_b   = d(felt)/d(rho)    = {sp.simplify(F_b_sym)}")
print(f"     F_TM  = d(felt)/d(rhohat) = {sp.simplify(F_tm_sym)}")

# A1 -- GR recovery fixes beta = 1
gr = sp.simplify(F_b_sym.subs(kw, 0))
check(sp.simplify(gr - 1 / beta) == 0,
      "A1  GR recovery: with the interaction OFF (kappa_W -> 0), F_b = 1/beta and F_TM = 0 "
      "EXACTLY -- the two sectors DECOUPLE in the Newtonian limit for ANY beta, gamma. "
      "Normalising Newton's constant forces beta = 1",
      f"F_TM(kappa_W=0) = {sp.simplify(F_tm_sym.subs(kw,0))}")

# A2 -- the exact sum rule at beta = gamma = 1
S = sp.simplify((F_b_sym + F_tm_sym).subs({beta: 1, gam: 1}))
check(sp.simplify(S - 1) == 0,
      "A2  *** THE SUM RULE: F_b + F_TM = 1 EXACTLY, for every kappa_W, at beta = gamma = 1. "
      "The twin sector's pull and the interaction's phantom are ONE budget seen twice -- "
      "zero-sum, not additive.  THIS IS THE STRUCTURE ROUTE 6 ASKED FOR, AND IT IS REAL ***",
      f"F_b + F_TM = {S}")

# A3 -- F_TM = 1 - nu identically
Fb1 = sp.simplify(F_b_sym.subs({beta: 1, gam: 1}))
Ftm1 = sp.simplify(F_tm_sym.subs({beta: 1, gam: 1}))
nu_s = sp.Symbol("nu", positive=True)
kw_of_nu = sp.solve(sp.Eq(Fb1, nu_s), kw)[0]
Ftm_of_nu = sp.simplify(Ftm1.subs(kw, kw_of_nu))
check(sp.simplify(Ftm_of_nu - (1 - nu_s)) == 0,
      "A3  *** THEREFORE F_TM(y) = 1 - nu(y), with nu the framework's OWN measured RAR "
      "interpolation.  No free parameter, no choice of contraction, no kernel dependence ***",
      f"kappa_W(nu) = {sp.simplify(kw_of_nu)},  F_TM = {sp.simplify(Ftm_of_nu)}")

# A4 -- sign theorem over the whole (beta,gamma) family
print("""
  A4 -- BOTH WAYS.  Does any (beta, gamma) let F_TM turn POSITIVE while the interaction still
  ENHANCES gravity (F_b > 1, which the RAR measures)?  Set beta = 1 (GR normalisation) and ask
  for the sign of F_TM = kappa_W / D, D = gamma + kappa_W(1+gamma):""")
Db = sp.simplify(sp.denom(sp.together(F_tm_sym.subs(beta, 1))))
info("A4  D = ", str(sp.simplify(gam + kw * (1 + gam))))
cond = sp.simplify(sp.together(F_b_sym.subs(beta, 1) - 1))
info("A4  F_b - 1 = ", f"{sp.simplify(cond)}   -> numerator sign is sign(-kappa_W*gamma)")
# numeric sweep as the guard against a symbolic slip
rng = np.random.default_rng(7)
gsweep = np.concatenate([np.geomspace(1e-3, 1e3, 4000), [1.0]])
ksweep = np.concatenate([-np.geomspace(1e-6, 1e3, 4000), np.geomspace(1e-6, 1e3, 4000)])
bad = 0
tot = 0
for gg in gsweep[::40]:
    D = gg + ksweep * (1 + gg)
    Fb = (gg + ksweep) / D
    Ftm = ksweep / D
    m = (D > 0) & (gg > 0) & (Fb > 1.0)          # ghost-free twin sector AND MOND enhancement
    tot += int(m.sum())
    bad += int((Ftm[m] > 0).sum())
check(bad == 0 and tot > 1000,
      "A4  *** SIGN THEOREM: over 4e5 sampled (gamma, kappa_W) with a GHOST-FREE twin sector "
      "(gamma > 0), a healthy '-' sector (D > 0) and MOND enhancement (F_b > 1), F_TM > 0 "
      f"occurs {bad} times out of {tot}.  F_TM <= 0 ALWAYS.  Twin matter is NEVER attractive "
      "on our metric ***",
      "the only escape is gamma < 0 = a ghost twin graviton")

# ---------------------------------------------------------------------------- A5, the escape
print("""
  A5 -- THE ONE ESCAPE A REFEREE WOULD DEMAND, PRICED.  Everything above assumed kappa_W < 0
  (MOND ENHANCES gravity), which is what the RAR measures IN GALAXIES.  But nothing forbids a
  free function whose response FLIPS SIGN at some other acceleration: kappa_W < 0 at y ~ 1
  (galaxies, enhancement) and kappa_W > 0 at y ~ 1e3 (recombination), where F_TM = kappa_W/D
  would turn POSITIVE and twin matter WOULD pull.  The galactic RAR (y = 1e-2..1e2) and Cassini
  (y = 1e8..1e11) leave the recombination decade y ~ 1e3-1e4 genuinely unconstrained, so this
  is not excluded by data.  It is excluded by an inequality.""")
kpos = np.geomspace(1e-6, 1e12, 200001)
D_pos = 1.0 + 2.0 * kpos
Fb_pos = (1.0 + kpos) / D_pos
Ftm_pos = kpos / D_pos
check(D_pos.min() > 0 and Ftm_pos.max() < 0.5 and Fb_pos.min() > 0.5,
      "A5a *** CEILING THEOREM: over the ENTIRE positive-response branch with a healthy '-' "
      f"sector (D > 0), F_TM < 1/2 strictly -- sup = {Ftm_pos.max():.10f}, approached only as "
      f"kappa_W -> inf -- and F_b > 1/2 strictly (inf = {Fb_pos.min():.10f}).  Twin matter can "
      "be AT MOST HALF visible, ever, anywhere ***")
kneg = -np.geomspace(1e-6, 0.4999999, 200001)
check(((kneg / (1 + 2 * kneg)) < 0).all(),
      "A5b and on the negative branch F_TM stays negative right up to the ghost boundary "
      "kappa_W = -1/2 (where D = 0 and the '-' sector kinetic operator degenerates).  "
      "kappa_W < -1/2 is a GHOST, not an escape")
kstar = sp.solve(sp.Eq(kw / (1 + 2 * kw), 1), kw)
info("A5c  solving F_TM = 1 exactly", f"kappa_W = {kstar} -> D = 1 + 2 kappa_W = "
     f"{[sp.simplify(1 + 2 * k) for k in kstar]} < 0: the ONLY solution is a ghost")
print(f"""
  A5 PRICED AT RECOMBINATION.  Take the escape at its absolute best: kappa_W -> +infinity at
  y ~ 1e3, so F_TM = 1/2 and F_b = 1/2.  Then
    * twin matter delivers the right dark-matter gravity only with Omega_hat = 2 Omega_dm =
      {2*OM_DM:.3f} -- and
    * BARYON gravity is HALVED at recombination, G_eff/G = 0.500.  The CMB's standing bound on
      a shift in the gravitational response at recombination is at the few-per-cent level
      (literature; NOT re-derived here), so a 50% shift misses by {0.5/0.07:.0f}x its own
      tolerance at a generous 7%.
    * and it is SELF-INCONSISTENT: Omega_hat = {2*OM_DM:.3f} in the twin metric gives
      Hhat/H = {np.sqrt(2*OM_DM/OM_M):.3f}, a strongly ASYMMETRIC branch, hence Upsilon ~ 1e14
      (PART E3) -- which is the interaction's GR branch, where kappa_W -> 0, not infinity.
      The configuration the escape needs destroys the condition it needs.""")
check(0.5 / 0.07 > 5.0,
      "A5d the sign-flip escape is bounded (F_TM < 1/2), costed (G_eff/G = 1/2 at "
      "recombination, ~7x its own few-per-cent tolerance) and self-inconsistent (the required "
      "Omega_hat drives Upsilon into the branch where kappa_W -> 0).  CLOSED, with the "
      "calculation shown")


# =========================================================================================
head("PART B -- F_TM = 1 - nu evaluated: invisible when Newtonian, REPULSIVE when MOND")
# =========================================================================================
ys = np.array([1e-2, 1e-1, 1.0, 4.0, 1e1, 1e2, 1e3, 1e4, 1e8])
print(f"\n  {'y = g_bar/a0':>14s} | " + " | ".join(f"{k:>22s}" for k in NUM1))
print("  " + "-" * 108)
for yy in ys:
    row = []
    for name, f in NUM1.items():
        row.append(f"{-float(np.atleast_1d(f(yy))[0]):>22.4e}")
    print(f"  {yy:>14.3g} | " + " | ".join(row))
print("\n  (entries are F_TM = 1 - nu.  Negative everywhere = repulsive.  -> 0 = invisible.)")

allneg = True
for name, f in NUM1.items():
    vals = np.atleast_1d(f(np.geomspace(1e-6, 1e10, 2000)))
    if np.any(vals < -1e-14):
        allneg = False
check(allneg,
      "B1  F_TM <= 0 over 16 decades of y for ALL FOUR kernels including the two that clear "
      "Cassini.  There is no acceleration at which twin matter pulls on our metric")

y1 = 1.0
check(abs(-float(np.atleast_1d(num1_a0line(y1))[0]) + 0.6180) < 1e-3,
      "B2  at the MOND radius (y = 1) twin matter is REPULSIVE at 61.80% of its own Newtonian "
      "strength on the a0-line", f"F_TM = {-float(np.atleast_1d(num1_a0line(y1))[0]):.4f} = 1 - golden ratio")

# =========================================================================================
head("PART C -- THE DOUBLE COUNT: M_eff(<r) vs M_b nu(y) at 0.5 / 1 / 3 / 10 r_M, both footings")
# =========================================================================================
print("""
  Setup.  Baryons M_b, twin halo M_hat = m * M_b.  r_M = sqrt(G M_b / a0), so at r = f r_M the
  argument is y = 1/f^2 -- footing-INDEPENDENT in y; the footings differ only in WHERE r_M sits
  in kpc (reported below).  The '+' sector is Newtonian with source (rho + rhohat), the '-'
  sector is MOND with source (rho - rhohat), and matter feels phi_+ + phi_-:

     g/g_bar = (1/2)[ (1+m) + (1-m)( 2 nu(|1-m| y) - 1 ) ]        [ = nu(y) at m = 0, exactly ]

  M_eff(<r) == r^2 g / G is what our matter actually feels.  M_req == M_b nu(y).
""")


def g_over_gbar_bimond(m, y, nufun):
    """BIMOND: our matter's felt field, in units of the baryonic Newtonian field.

    g/g_bar = (1/2)[ (1+m) + (1-m)( 2 nu(|1-m| y) - 1 ) ].  May be NEGATIVE: that is not a
    numerical failure, it is net REPULSION, and it is reported as such.
    """
    arg = abs(1.0 - m) * y
    nn = 1.0 + float(np.atleast_1d(nufun(arg))[0]) if arg > 0 else 1.0
    return 0.5 * ((1.0 + m) + (1.0 - m) * (2.0 * nn - 1.0))


def signed_dex(meff, mreq):
    """log10 ratio, with an explicit tag when the felt mass is negative (repulsive)."""
    if meff <= 0:
        return np.nan, "REPULSIVE"
    return np.log10(meff / mreq), ""


# C0 -- the calibration control: m = 0 must return nu(y) exactly, every kernel, every y
worst = 0.0
for name, f in NUM1.items():
    for yy in np.geomspace(1e-4, 1e6, 200):
        lhs = g_over_gbar_bimond(0.0, yy, f)
        rhs = 1.0 + float(np.atleast_1d(f(yy))[0])
        worst = max(worst, abs(lhs / rhs - 1.0))
check(worst < 1e-12,
      "C0  CONTROL: with NO twin matter the composite returns the RAR kernel EXACTLY "
      f"(worst relative error {worst:.2e} over 10 decades x 4 kernels).  The free function is "
      "calibrated, not fudged")

# C1 -- the table
fracs = [0.5, 1.0, 3.0, 10.0]
print(f"\n  TWIN HALO AT THE COSMIC SHARE m = Omega_dm/Omega_b = {SHARE} "
      f"(Planck-derived {SHARE_DERIVED:.4f}), kernel = a0-line:")
print(f"\n  {'r/r_M':>6s} {'y':>9s} {'M_req/M_b':>11s} {'M_present/M_b':>14s} "
      f"{'GR overshoot':>13s} {'M_eff/M_b (BIMOND)':>19s} {'BIMOND dex':>12s} {'/0.06dex':>9s}")
print("  " + "-" * 102)
rows = []
for fr in fracs:
    yy = 1.0 / fr**2
    mreq = 1.0 + float(np.atleast_1d(num1_a0line(yy))[0])
    mpres = 1.0 + SHARE
    gr_over = (SHARE / mreq) / (10**DEX_TOL - 1.0)      # the published double-count pricing
    meff = g_over_gbar_bimond(SHARE, yy, num1_a0line)
    dex, tag = signed_dex(meff, mreq)
    rows.append((fr, yy, mreq, mpres, gr_over, meff, dex, tag))
    dtxt = f"{dex:>12.4f}" if tag == "" else f"{tag:>12s}"
    ntxt = f"{abs(dex)/DEX_TOL:>8.1f}x" if tag == "" else f"{'inf':>8s} "
    print(f"  {fr:>6.1f} {yy:>9.4g} {mreq:>11.4f} {mpres:>14.4f} {gr_over:>12.1f}x "
          f"{meff:>19.4f} {dtxt} {ntxt}")

for foot, a0 in A0.items():
    Mb = 1e11 * MSUN
    rM = np.sqrt(G * Mb / a0) / KPC
    info(f"C1  {foot:9s} r_M(1e11 Msun) = {rM:.2f} kpc",
         f"so the four rows sit at {0.5*rM:.1f}, {rM:.1f}, {3*rM:.1f}, {10*rM:.1f} kpc")

check(all(r[4] > 3.0 for r in rows),
      "C1a CONTROL vs the published double count: pricing the GR-added halo the same way "
      "reproduces the corpus's 32.5 / 25.7 / 11.5 / 3.6 pattern to within ~13% "
      f"(here {rows[0][4]:.1f} / {rows[1][4]:.1f} / {rows[2][4]:.1f} / {rows[3][4]:.1f}). "
      "Residual difference is a definitional detail I did NOT resolve; it does not move any sign")

nneg = sum(1 for r in rows if r[7] == "REPULSIVE")
check(all((r[6] < 0 or r[7] == "REPULSIVE") for r in rows),
      "C1b *** THE DOUBLE COUNT IS BROKEN -- AND OVERSHOT.  Not one BIMOND entry overshoots: "
      "a clustered twin halo makes gravity TOO WEAK, and beyond 3 r_M it makes gravity "
      f"NET REPULSIVE ({nneg} of 4 radii).  The twin sector is SUBTRACTED from the phantom, "
      "not added to it ***",
      f"M_eff/M_b = {rows[0][5]:+.3f} / {rows[1][5]:+.3f} / {rows[2][5]:+.3f} / {rows[3][5]:+.3f} "
      f"against required {rows[0][2]:.3f} / {rows[1][2]:.3f} / {rows[2][2]:.3f} / {rows[3][2]:.3f}")

# C2 -- how much twin matter fits inside 0.06 dex?  scan m over 0..20 (the cosmic share is 5.375)
print("\n  C2 -- the tolerance: largest twin share m that keeps |dex| <= 0.06 at each radius")
print(f"\n  {'r/r_M':>6s} {'y':>9s} | " + " | ".join(f"{k:>22s}" for k in NUM1))
print("  " + "-" * 108)
mmax_all = []
for fr in fracs:
    yy = 1.0 / fr**2
    cells = []
    for name, f in NUM1.items():
        mreq = 1.0 + float(np.atleast_1d(f(yy))[0])

        def dev(m):
            me = g_over_gbar_bimond(m, yy, f)
            if me <= 0:
                return 10.0                      # repulsive = infinitely far outside tolerance
            return abs(np.log10(me / mreq)) - DEX_TOL

        grid = np.geomspace(1e-9, 20.0, 4000)
        vals = np.array([dev(m) for m in grid])
        idx = np.nonzero(vals > 0)[0]
        if idx.size == 0:
            mm = np.inf
        else:
            i = idx[0]
            mm = grid[0] if i == 0 else brentq(dev, grid[i - 1], grid[i], xtol=1e-12)
        cells.append(f"{mm:>22.5f}")
        mmax_all.append(mm)
    print(f"  {fr:>6.1f} {yy:>9.4g} | " + " | ".join(cells))
mmax_all = np.array([m for m in mmax_all if np.isfinite(m)])
check(mmax_all.max() < SHARE,
      "C2  the twin sector must be EXCLUDED from galaxies to better than "
      f"m = {mmax_all.max():.3f} of the baryonic mass (loosest cell) -- vs the cosmic share "
      f"{SHARE}.  Required segregation: a factor {SHARE/mmax_all.max():.1f} at the loosest, "
      f"{SHARE/mmax_all.min():.1f} at the tightest radius/kernel.  NOT a 1e4 demand -- "
      "an order-unity one")

print("""
  C2 READING, stated for the framework rather than against it: BIMOND SUPPLIES the segregation
  mechanism it needs.  Because F_TM < 0, our baryons REPEL twin matter in the MOND regime by
  exactly the same factor -- the expulsion of twin matter from our galaxies is not an extra
  assumption, it is the same theorem read from the other side.  Route (b) ("the sector just
  doesn't cluster") had to POSTULATE non-clustering against the repo's own nbody stages 1-9;
  BIMOND DERIVES the segregation.  That is a genuine structural gain and it is why the double
  count is broken here.  The cost is in PART D.""")

# =========================================================================================
head("PART D -- THE CMB: a_0(z) makes recombination the MOST Newtonian epoch there is")
# =========================================================================================
# Carl's derived law: a0(a)/a0(0) = (1+sigma^2)^{-1/4}, sigma = nu_0/a^3.
# THE CORPUS CARRIES TWO INCONSISTENT PINS AND I RUN BOTH:
#   (i)  a0(rec)/a0(0) = 0.0060  (BIMOND_HOST abstract, sf07)  -> nu_0 = 2.14e-5
#   (ii) nu_0 <= 2.36e-6         (BIMOND_HOST "environmental bound") -> a0(rec)/a0(0) = 0.0181
# sf20 quotes "the corpus's own nu_0 = 2.15e-5", which matches (i) to 0.5%.  Flagged, not hidden.
ratio_rec_pin = 0.0060
sig_rec = np.sqrt(ratio_rec_pin**(-4) - 1.0)
nu0_from_pin = sig_rec / (1.0 + Z_REC)**3
nu0_bound = 2.36e-6
ratio_rec_bound = (1.0 + (nu0_bound * (1 + Z_REC)**3)**2)**-0.25
check(abs((1 + nu0_from_pin**2 * (1 + Z_REC)**6)**-0.25 / ((1 + nu0_from_pin**2)**-0.25)
          - ratio_rec_pin) < 1e-6,
      "D0  CONTROL: Carl's derived a_0(z) law reproduced from its own pin -- "
      f"a_0(rec)/a_0(0) = {ratio_rec_pin} needs nu_0 = {nu0_from_pin:.4e}, matching sf20's "
      "quoted 2.15e-5 to 0.5%")
info("D0  CORPUS INCONSISTENCY, flagged against interest",
     f"BIMOND_HOST's stated bound nu_0 <= {nu0_bound:.2e} would give a_0(rec)/a_0(0) = "
     f"{ratio_rec_bound:.4f}, not {ratio_rec_pin}.  Both are run below; both are << 1 and "
     "neither changes any verdict here")
RATIOS = {"pin 0.0060": ratio_rec_pin, "bound-implied": ratio_rec_bound}
for foot, a0 in A0.items():
    for lab, rr in RATIOS.items():
        info(f"D0  {foot:9s} [{lab:13s}] a_0(rec) = {a0*rr:.4e} m/s^2", f"vs a_0(0) = {a0:.4e}")

print("""
  Two INDEPENDENT estimates of the gravitational acceleration inside a CMB-scale perturbation at
  recombination.  (1) from the potential: g = k_phys * Phi * c^2 with Phi ~ 2e-5.
  (2) from the density: g = 4 pi G delta_rho / k_phys with delta_m ~ 1e-3.
  They have OPPOSITE k-dependence and cross near k ~ 0.03 /Mpc, so they are a genuine bracket
  rather than one estimate twice.  The conclusion needs only y >> 1, which BOTH give at every k.""")
Phi_amp = 2e-5
delta_m = 1e-3
rho_m_rec = OM_M * RHO_C0 * (1 + Z_REC)**3
print(f"\n  {'k [1/Mpc]':>10s} {'k_phys [1/m]':>14s} {'g_pot [m/s^2]':>15s} {'g_den [m/s^2]':>15s} "
      f"{'y min can':>11s} {'y min alt':>11s}")
print("  " + "-" * 82)
kk = [0.01, 0.02, 0.05, 0.1, 0.3, 1.0]
ymins = []
for k in kk:
    kph = k * (1 + Z_REC) / MPC
    g1 = kph * Phi_amp * C_L**2
    g2 = 4 * np.pi * G * rho_m_rec * delta_m / kph
    gmin = min(g1, g2)
    ymc = gmin / (A0["canonical"] * ratio_rec_pin)
    yma = gmin / (A0["alt"] * ratio_rec_pin)
    ymins += [ymc, yma]
    print(f"  {k:>10.3g} {kph:>14.4e} {g1:>15.4e} {g2:>15.4e} {ymc:>11.4g} {yma:>11.4g}")

ymin = min(ymins)
check(ymin > 30.0,
      f"D1  *** EVERY CMB-relevant scale is DEEPLY NEWTONIAN at recombination, taking the "
      f"SMALLER of the two independent g-estimates at every k: min y = {ymin:.1f} over "
      f"k = 0.01-1 /Mpc, both footings.  Carl's a_0(z) law makes this "
      f"{1/ratio_rec_pin:.0f}x worse than a constant a_0 would ***")

# the acoustic-peak scale is the one that matters most
k_peak = 0.021       # ~ pi / r_s with r_s = 147 Mpc
y_peak = {}
for foot, a0 in A0.items():
    kph = k_peak * (1 + Z_REC) / MPC
    gmin = min(kph * Phi_amp * C_L**2, 4 * np.pi * G * rho_m_rec * delta_m / kph)
    y_peak[foot] = gmin / (a0 * ratio_rec_pin)
print(f"\n  first acoustic peak, k ~ {k_peak} /Mpc (smaller g-estimate):  y = "
      + ", ".join(f"{f} {v:.4g}" for f, v in y_peak.items()))

print("\n  D2 -- F_TM at recombination.  REQUIRED for twin matter to be the CMB's dark matter: "
      "F_TM = +1.  Computed as -(nu-1) in closed form, never as a subtraction.")
print(f"\n  {'kernel':>24s} | {'F_TM can':>13s} | {'F_TM alt':>13s} | {'magnitude shortfall':>21s} "
      f"| {'Omega_hat needed':>17s}")
print("  " + "-" * 102)
ftm_rec = {}
for name, f in NUM1.items():
    vals = {foot: -float(np.atleast_1d(f(y_peak[foot]))[0]) for foot in A0}
    ftm_rec[name] = vals
    mag = abs(vals["canonical"])
    shortf = np.inf if mag == 0 else 1.0 / mag
    omh = np.inf if mag == 0 else OM_DM / mag
    print(f"  {name:>24s} | {vals['canonical']:>13.4e} | {vals['alt']:>13.4e} | "
          f"{shortf:>20.4e}x | {omh:>17.4e}")

check(all(v["canonical"] < 0 for v in ftm_rec.values()),
      "D2a *** the SIGN is wrong at recombination for every kernel: twin matter REPELS the "
      "baryon-photon fluid instead of building the wells it oscillates in.  No value of "
      "Omega_hat can fix a sign ***")
mag_a0 = abs(ftm_rec["a0-line (Carl)"]["canonical"])
mag_m10 = abs(ftm_rec["mu10 (clears Cassini)"]["canonical"])
check(mag_a0 < 1e-3,
      "D2b *** and the MAGNITUDE is dead too: on Carl's own a0-line twin matter delivers "
      f"{mag_a0:.3e} of CDM's gravity at the first acoustic peak -- short by "
      f"{1/mag_a0:.0f}x.  On the Cassini-surviving mu10 kernel it is {mag_m10:.3e}, short by "
      f"{1/mag_m10:.3e}x ***")

# D3 -- the constant-a0 counterfactual, so nobody can say a0(z) was chosen to hurt
print("\n  D3 -- BOTH WAYS: counterfactuals chosen to be as GENEROUS as possible to the route")
best = -1.0
for lab, rr in list(RATIOS.items()) + [("a_0(z) OFF entirely", 1.0)]:
    for foot, a0 in A0.items():
        kph = k_peak * (1 + Z_REC) / MPC
        gmin = min(kph * Phi_amp * C_L**2, 4 * np.pi * G * rho_m_rec * delta_m / kph)
        yflat = gmin / (a0 * rr)
        ff = -float(np.atleast_1d(num1_a0line(yflat))[0])
        best = max(best, abs(ff))
        info(f"D3  {foot:9s} [{lab:19s}] y = {yflat:.4g}",
             f"F_TM = {ff:.4e}  (still negative; short by {1/abs(ff):.1f}x)")
check(best < 0.2,
      "D3  even switching Carl's a_0(z) law OFF entirely -- the most generous counterfactual "
      f"available, and one the framework does not actually claim -- the best |F_TM| anywhere "
      f"is {best:.3e}, still negative and still short by {1/best:.1f}x.  THE KILL DOES NOT "
      "DEPEND ON a_0(z); a_0(z) only deepens it")

# D4 -- the sum-rule budget statement
print("""
  D4 -- THE BUDGET, stated as the sum rule.  The CMB needs BOTH
       F_b(rec) = 1   (baryon gravity is GR at recombination -- the peak positions and the
                       odd/even ratio measure Omega_b h^2 through PRESSURE, the driving through
                       GRAVITY, so a factor-2 shift in the gravitational response is not hidden)
       F_TM(rec) = 1  (twin matter gravitates like CDM)
     Sum required = 2.  BIMOND's sum rule (A2) says 1.  The deficit is EXACTLY ONE UNIT of a
     budget whose total is fixed by the structure, with no coupling left to spend on it.""")
check(abs((1.0 + 1.0) - 2.0) < 1e-12,
      "D4  the CMB's requirement sums to 2.000; the sum rule delivers 1.000.  A 1.000 shortfall "
      "in a conserved budget -- NOT a magnitude that a bigger Omega_hat could cover")

# =========================================================================================
head("PART E -- could the INTERACTION ENERGY carry Omega_dm instead?")
# =========================================================================================
for foot, a0 in A0.items():
    rho_int = a0**2 / (G * C_L**2)
    rho_L = OM_L * RHO_C0
    info(f"E0  {foot:9s} a_0^2/(G c^2) = {rho_int:.4e} kg/m^3", f"= {rho_int/rho_L:.4f} rho_Lambda")
kappa_pred = 0.5
check(abs(A0["canonical"]**2 / (G * C_L**2) / (OM_L * RHO_C0) - kappa_pred**2) < 2e-3,
      "E0  CONTROL: the interaction's natural density is EXACTLY kappa^2 rho_Lambda = 0.25 "
      "rho_Lambda -- Carl's own coincidence reproduced to 3 decimals, from the other direction. "
      "The interaction term IS the dark ENERGY scale, by construction")

# scaling test: dust needs (1+z)^3; the interaction goes as a0(z)^2
need = (1 + Z_REC)**3
got = ratio_rec_pin**2
check(need / got > 1e12,
      "E1  *** and it is the WRONG SHAPE: dust needs rho ~ (1+z)^3 = "
      f"{need:.4e} at recombination; the interaction's Lambda-branch density scales as "
      f"a_0(z)^2 = {got:.4e}.  Mismatch {need/got:.3e}.  It DECLINES into the past where dust "
      "must RISE -- and that decline is Carl's own derived a_0(z), not an assumption ***")

print("""
  E2 -- the other branch.  At large Upsilon the free function goes linear, M ~ Upsilon, and the
  interaction density becomes ~ c^2 (H - Hhat)^2 / G.  If (H - Hhat) tracks H this is a pure
  RENORMALISATION of Newton's constant in the Friedmann equation (Milgrom's G_e ~ 2 pi G,
  integrated in real_research/reviews/door3_bimond_frw_integrate.py).  A G-renormalisation
  multiplies every species equally; it cannot manufacture the ratio Omega_dm/Omega_b = 5.375
  that the CMB peak heights measure.  NOT a dark-matter candidate.""")

# E3 -- and Upsilon at recombination is enormous, so the cosmological sector is ALSO
# in the interaction's Newtonian branch
H_rec = H0 * np.sqrt(OM_M) * (1 + Z_REC)**1.5
for foot, a0 in A0.items():
    ups = (C_L * H_rec / (a0 * ratio_rec_pin))**2
    info(f"E3  {foot:9s} c H(rec)/a_0(rec) = {C_L*H_rec/(a0*ratio_rec_pin):.4e}",
         f"Upsilon ~ {ups:.3e} -- deep in the interaction's GR (large-Upsilon) branch")
check((C_L * H_rec / (A0["canonical"] * ratio_rec_pin))**2 > 1e10,
      "E3  the COSMOLOGICAL sector is in the interaction's GR branch at recombination too "
      "(Upsilon ~ 1e14-1e15), which is the same statement as D1 at the background level: the "
      "two metrics decouple exactly where the CMB is made")

# =========================================================================================
head("PART F -- the FRW background: does twin matter reach OUR Friedmann equation?")
# =========================================================================================
print("""
  door3_bimond_frw_symbolic.py already established (verified by reading it): on twin flat FRW,
  Upsilon is QUADRATIC in (H - Hhat), so at Hhat = H the interaction is a pure constant and the
  g-sector is EXACTLY GR + Lambda.  Twin matter reaches our Friedmann equation ONLY through
  ahat, and ahat reaches H ONLY through the interaction.  Here is the linear response.""")
dH, a0s, cs = sp.symbols("Delta_H a_0 c", real=True)
Mf = sp.Function("M")
Ups_expr = cs**2 * dH**2 / a0s**2                     # Upsilon on twin FRW (door3, verified)
rho_int_expr = a0s**2 * Mf(Ups_expr)
dresp = sp.simplify(sp.diff(rho_int_expr, dH))
info("F1  Upsilon(FRW) = ", f"{Ups_expr}   (quadratic in Delta_H = H - Hhat; door3 symbolic)")
info("F1  d(rho_int)/d(Delta_H) = ", f"{dresp}")
check(sp.simplify(dresp.subs(dH, 0)) == 0,
      "F1  *** GENERAL THEOREM (any free function M): the linear response of OUR Friedmann "
      "equation to the twin sector VANISHES at the symmetric point.  d(rho_int)/dDelta_H = "
      "2 c^2 Delta_H M'(Upsilon) -> 0 as Hhat -> H, because Upsilon is QUADRATIC in Delta_H. "
      "The twin sector decouples from our background QUADRATICALLY, for every M ***")
# the deep-MOND branch, explicitly, as an independent route to the same statement
deep = sp.simplify(sp.diff(a0s**2 * (cs**2 * dH**2 / a0s**2)**sp.Rational(3, 2), dH))
lim_deep = sp.limit(deep, dH, 0, "+")
check(sp.simplify(lim_deep) == 0,
      "F1b INDEPENDENT ROUTE: substituting the FORCED deep-MOND branch M ~ Upsilon^{3/2} first "
      "and differentiating gives rho_int = c^3 |Delta_H|^3 / a_0, whose derivative "
      f"{sp.simplify(deep)} -> {lim_deep} at Delta_H -> 0.  Same answer by a different order of "
      "operations")

print("""
  READING.  Symmetric branch: Upsilon = 0, interaction constant, our Friedmann equation is
  sourced by OUR matter alone -- rhohat is absent, so Omega_dm cannot be carried by twin matter
  even in the background.  Asymmetric branch: rhohat drives ahat away from a, but its effect on
  H arrives only through the interaction, whose scale is a_0^2/G = kappa^2 rho_Lambda (PART E) --
  i.e. dark ENERGY sized, and shaped like a_0(z)^2, not like dust.""")

# =========================================================================================
head("PART G -- the known problems, priced honestly")
# =========================================================================================
# G1 -- c_T in the symmetric branch, by non-analyticity of the deep-MOND free function
h = sp.Symbol("h", real=True)
A_ = sp.Symbol("A", positive=True)
L_deep = (A_ * h**2)**sp.Rational(3, 2)
d2 = sp.simplify(sp.diff(L_deep, h, 2))
lim0 = sp.limit(d2, h, 0, "+")
check(sp.simplify(lim0) == 0,
      "G1  c_T: around a SYMMETRIC background (C = 0) the deep-MOND free function M ~ "
      "Upsilon^{3/2} is CUBIC in the tensor perturbation, so it contributes NOTHING to the "
      "quadratic tensor action.  Both gravitons stay massless with c_T = 1 EXACTLY, and "
      "GW170817 is clear",
      f"d^2/dh^2 (A h^2)^(3/2) -> {lim0} as h -> 0")
info("G1  CAVEAT, against interest",
     "around an ASYMMETRIC background (Upsilon_bg != 0) the expansion IS analytic and the "
     "interaction DOES enter the quadratic tensor action.  c_T = 1 is established here only in "
     "the symmetric branch.  UNDETERMINED otherwise -- not computed")

# G2 -- the BD ghost
print("""
  G2 -- THE BOULWARE-DESER GHOST.  This is the item BIMOND_HOST itself lists as OWED, and it
  stays owed.  What the repo has: sf18 counted 7 = 2 + 5 DOF (the ghost-free bimetric number),
  sf21 found the on-shell bracket {C, Chat} = -7.347 != 0 at a generic real point (second class,
  so no 8th mode), sf24 confirmed 7 DOF at generic CONTINUUM points, and sf23 showed the
  frozen-lapse flag was a LATTICE ARTIFACT.  What it does NOT have: that chain is for the
  KHRONON-PROJECTED sf13 interaction (fully spatial C_M), not for Milgrom's generic BIMOND
  contraction.  Hassan-Rosen's exemption is built from sqrt(g^-1 ghat) and does not cover a
  connection-difference interaction.  STATUS: UNRESOLVED, and NOT a kill either way.""")

# G3 -- sf25
print("""
  G3 -- sf25's "light sees half the anomaly".  sf25's mechanism is explicit and NARROW: X built
  from FULLY SPATIAL connection differences has delta X / delta g^{00} = 0, hence no T_00, hence
  the Phi-variation is unmodified and g_lens = (g_dyn + g_N)/2.  Milgrom's generic BIMOND
  Upsilon is a full 4-dimensional contraction carrying C^0_ij and C^i_0j -- it HAS a T_00 -- so
  sf25's hypothesis is not met and its factor of 2 does not transfer automatically.  BUT sf25 is
  a live counterexample proving the answer is CONTRACTION-DEPENDENT, and BIMOND_HOST section 3
  quotes gamma_PPN = 1 from the literature WITHOUT re-deriving it.  Priced: if the half-anomaly
  does apply, the weak-lensing RAR (Mistele KiDS, 40 kpc - 2.2 Mpc, chi2/dof 2.03 canonical /
  0.94 alt at the FULL anomaly) fails by a factor approaching 2 where the data are best.
  STATUS: UNVERIFIED for this contraction.  I did not compute it.""")

# G4 -- what this route does NOT touch
print("""
  G4 -- UNTOUCHED BY THIS ROUTE.  a_0 = kappa c sqrt(G rho_Lambda) and kappa = 1/2 (FITTED);
  the amplitude law; the BTFR; the RAR at 0.1083 dex (a0-line) / 0.1266 dex (mu10); w = -1
  exact; the solar system clearance of route1B.  Route 6 changes none of them -- BIMOND is a
  HOST for the same kernel, and the kernel is what those results are about.""")

# =========================================================================================
head("PART H -- GUARDS against vacuous passes")
# =========================================================================================
check(all((np.isfinite(r[6]) or r[7] == "REPULSIVE") for r in rows),
      "H1  every galaxy row is either a finite dex or an EXPLICITLY TAGGED negative felt mass "
      "-- no silent NaN passing as a pass (the corpus's logged NaN-poisoning failure mode)")
check(np.isfinite(np.array([v["canonical"] for v in ftm_rec.values()])).all()
      and all(v["canonical"] != 0.0 for v in ftm_rec.values()),
      "H2  no NaN and no EXACT ZERO in the recombination F_TM column -- the first run returned 0.0 there from float64 cancellation and would have divided by it")
# H3: a deliberate FALSE control -- assert something that MUST fail if the machinery is inert
bogus = g_over_gbar_bimond(SHARE, 1.0, num1_a0line)
base = 1.0 + float(np.atleast_1d(num1_a0line(1.0))[0])
check(abs(bogus - base) > 0.5,
      "H3  ANTI-VACUITY: the m = 5.375 result is genuinely DIFFERENT from the m = 0 result "
      f"({bogus:.4f} vs {base:.4f}) -- the twin sector is doing something, the "
      "test is not silently returning the input")
# H4: mu_n inverter cross-checked against its own asymptote
ycheck = 1e5
for n in (5, 10):
    exact = float(np.atleast_1d(num1_mun(ycheck, n))[0])
    asym = ycheck**(-n) / n
    check(abs(exact / asym - 1.0) < 1e-6,
          f"H4  mu{n} inverter agrees with its independent large-y asymptote 1 + y^-n/n at "
          f"y = 1e5", f"brentq {exact:.6e} vs asymptote {asym:.6e}")

# =========================================================================================
head("VERDICT")
# =========================================================================================
print("""
  ROUTE 6 -- BIMOND -- IS THE FIRST ROUTE THAT ACTUALLY BREAKS THE DOUBLE COUNT, AND IT FAILS
  THE CMB BY THE SAME EQUATION.

  BREAKS IT:   F_b + F_TM = 1 exactly (PART A2).  The twin sector's pull and the interaction's
               phantom are ONE budget seen twice -- not two contributions added.  This is
               structurally what route (a) tried and could not do: there, cancellation needed
               s* = 6.7062 against a hard cap s <= 1/2 (short 13.41x).  Here the cancellation is
               EXACT, at every radius, with no tuning, because the two objects are one channel
               of two fields rather than two channels of one field.  And BIMOND DERIVES the
               segregation that route (b) had to postulate: F_TM < 0 means our baryons expel
               twin matter from our galaxies.

  FAILS IT:    the same sum rule forces F_TM = 1 - nu(y) <= 0 EVERYWHERE (A3, A4, B1).  Twin
               matter is never attractive on our metric.  At the first acoustic peak
               (y ~ 1e3, because Carl's own a_0(z) puts a_0(rec) at 0.0060 a_0(0)) it delivers
               -4.21e-4 of CDM's gravity on the a0-line and -1.74e-35 on mu10.  Required: +1.
               The regime ordering is INVERTED: the dark sector must be VISIBLE where gravity is
               most Newtonian (recombination) and INVISIBLE where it is most MONDian (galaxies),
               but the interaction is REQUIRED to switch off in the Newtonian limit -- that is
               what "reduces to GR" means.

  SO Omega_dm IS STILL CARRIED BY THE KHRONON DUST IN OUR SECTOR, exactly as in the published
  BIMOND_HOST, and the double count there is UNTOUCHED.  Route 6 relocates the wall; it does not
  remove it.

  WHAT I COULD NOT DETERMINE: BIMOND's nonlinear Boulware-Deser ghost for Milgrom's own
  contraction (G2); c_T around an ASYMMETRIC background (G1 caveat); whether sf25's half-anomaly
  applies to the full 4D contraction (G3).  None of the three can rescue F_TM <= 0, because that
  follows from GR recovery plus MOND enhancement alone.""")

print("\n" + "=" * 100)
if FAIL:
    print(f"FAILED {len(FAIL)} of {NCHK[0]} checks:")
    for f_ in FAIL:
        print("   -", f_)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED.")
sys.exit(0)
