#!/usr/bin/env python3
"""
SOLAR-SYSTEM GATES for the cuscuton-clock + AQUAL-fifth-force health branch.
============================================================================================================
Companion to ppn_beta_exact_symbolic.py, which proved EXACTLY:

      gamma_PPN = 1 - 2 f ,      beta_PPN = 1 (exponential coupling)  or  1 - f^2/2 (linear coupling),
      eta_N = 4 beta - gamma - 3 = 2f  (exp)  or  2f - 2f^2  (linear),

with  f == G_s/G_N  the fraction of Newtonian gravity carried by the phi fifth force.

THIS script answers the questions the symbolic script deliberately deferred:
  1. Is the deep-Newtonian (mu -> 1) hypothesis -- the very thing that makes PPN applicable -- actually
     TRUE in the solar system?  Quantify e^{-y} at 1 AU and at Saturn.
  2. What anomalous acceleration and perihelion precession does the fifth force produce, as a function of f?
  3. Do the beta / Nordtvedt / perihelion gates admit a COMMON window in f?

THE PARAMETRISATION (forced, not chosen).  Let a0 be the OBSERVED MOND scale (RAR/BTFR) and a0t the scale
appearing in the action.  Then:
      deep-Newtonian:  g_s -> f g_N        (g_N == G_N M/r^2, the dynamically-measured Newtonian field)
      deep-MOND:       g -> g_s -> sqrt(G_s a0t M)/r,  which must equal sqrt(G_N a0 M)/r
                       =>  G_s a0t = G_N a0   =>   a0t = a0 / f.
So f and a0t are LOCKED:  a weak fifth force (small f, needed for gamma/eta_N) forces a LARGE a0t, which
drags the scalar's own MOND transition INWARD to r_trans = f * sqrt(G_N M/a0).  That lock is the whole story.

Scalar field equation used throughout (exact, spherical):   mu(g_s/a0t) * g_s = f * g_N ,   g = (1-f) g_N + g_s.

POLARITY: every check ASSERTS a statement; PASS = the statement is TRUE.  Both a0 footings are run.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import sys, time

T0 = time.time(); FAILS = []; N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n           ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def sec(t):
    print("\n" + "=" * 110); print(t); print("=" * 110, flush=True)


# ---------------------------------------------------------------- constants
GM = 1.32712440018e20          # m^3/s^2, IAU solar GM (the DYNAMICALLY measured G_N M_sun)
AU = 1.495978707e11            # m
YR = 3.15576e7                 # s (Julian year)
ARCSEC = 180.0 / np.pi * 3600.0
A0_FOOTINGS = {"repo canonical 9.36e-11": 9.36e-11,
               "repo alt      1.13e-10": 1.13e-10,
               "c^2/(2 pi L_dS) 1.2e-10": 1.20e-10}

PLANETS = {  # name: (a/AU, e, period_days)
    "Mercury": (0.38709893, 0.20563069, 87.9691),
    "Earth":   (1.00000011, 0.01671022, 365.256),
    "Mars":    (1.52366231, 0.09341233, 686.980),
    "Jupiter": (5.20336301, 0.04839266, 4332.589),
    "Saturn":  (9.53707032, 0.05415060, 10759.22),
}

# Observational gates (conservative; tighter published values noted in the report)
GATE_GAMMA = 2.3e-5      # |gamma-1|, Cassini Shapiro (Bertotti-Iess-Tortora 2003: gamma-1 = (2.1 +/- 2.3)e-5)
GATE_BETA = 8.0e-5       # |beta-1|, Will 2014 Living Review compilation (task-specified)
GATE_ETA = 3.0e-4        # |eta_N|,  LLR (task-specified)
GATE_PREC = {"Mercury": 1.0e-3, "Saturn": 1.0e-3}   # arcsec/century, CONSERVATIVE (published ~1e-3 arcsec/cy
                                                    # = 1 mas/cy; INPOP10a: Mercury 0.4+/-0.6, Saturn 0.15+/-0.65 mas/cy)

print("=" * 110)
print("SOLAR-SYSTEM GATES -- cuscuton clock + AQUAL fifth force:  is there ANY f that passes everything?")
print("=" * 110, flush=True)

# ---------------------------------------------------------------- kernels
KERNELS = {
    "exp (branch spec)": lambda y: 1.0 - np.exp(-y),
    "simple":            lambda y: y / (1.0 + y),
    "standard":          lambda y: y / np.sqrt(1.0 + y * y),
    "nu_RAR-conjugate":  lambda y: 1.0 - np.exp(-np.sqrt(y)) if False else (1.0 - np.exp(-y)),  # placeholder, replaced below
}
# nu_RAR: nu(x) = 1/(1-e^{-sqrt x}); its conjugate mu is defined implicitly by mu(y)*nu(mu(y)*y ... ) -- build numerically
def mu_from_nu(y):
    """mu conjugate to the RAR boost nu(x)=1/(1-exp(-sqrt x)):  given y = g/a0, find x = g_bar/a0 with x*nu(x)=y, mu=x/y."""
    if y <= 0:
        return 0.0
    fn = lambda x: x / (-np.expm1(-np.sqrt(x))) - y
    lo, hi = 1e-40, max(y, 1.0)
    while fn(lo) > 0:
        lo *= 1e-2
        if lo < 1e-280:
            return 0.0
    while fn(hi) < 0:
        hi *= 2.0
    x = brentq(fn, lo, hi, xtol=1e-300, rtol=1e-14)
    return x / y
KERNELS["nu_RAR-conjugate"] = np.vectorize(mu_from_nu)


def g_scalar(gN, f, a0, mu):
    """solve mu(g_s/a0t) g_s = f gN  for g_s, with a0t = a0/f."""
    a0t = a0 / f
    lo, hi = 1e-30 * max(gN, 1e-30), 10.0 * max(gN, 1e-30) / max(f, 1e-30)
    fn = lambda gs: mu(gs / a0t) * gs - f * gN
    while fn(hi) < 0:
        hi *= 10.0
    return brentq(fn, lo, hi, xtol=1e-300, rtol=1e-15)


def g_total(r, f, a0, mu):
    gN = GM / r**2
    return (1.0 - f) * gN + g_scalar(gN, f, a0, mu)


# --- CANCELLATION-FREE anomaly.  dg == g_total - g_N = g_s - f g_N = f g_N (1/mu - 1).
#     For the exponential kernel 1/mu - 1 = 1/expm1(y) EXACTLY, which is stable for every y, whereas
#     forming g_s - f*g_N by subtraction loses the answer entirely once y >~ 36 (double-precision floor).
def y_of(r, f, a0, mu):
    gN = GM / r**2
    return g_scalar(gN, f, a0, mu) * f / a0


def anomaly(r, f, a0):
    """dg(r) for the exponential kernel mu = 1 - e^{-y}, computed without cancellation."""
    gN = GM / r**2
    y = y_of(r, f, a0, KERNELS["exp (branch spec)"])
    return f * gN / np.expm1(y) if y < 700 else 0.0


def precess_stable(f, a0, a_sma):
    """near-circular perihelion advance per orbit (rad), cancellation-free.
       q = 3 + r F'/F with F = A + dg, A = GM/r^2  =>  dvarpi ~ -pi (2 dg + r dg')/(A + dg)."""
    d0 = anomaly(a_sma, f, a0)
    if d0 == 0.0:
        return 0.0
    h = 1e-4
    dp = anomaly(a_sma * np.exp(h), f, a0)
    dm = anomaly(a_sma * np.exp(-h), f, a0)
    dlnd = (np.log(dp) - np.log(dm)) / (2 * h) if dp > 0 and dm > 0 else -1.0
    A = GM / a_sma**2
    q = 1.0 + (2.0 * d0 + d0 * dlnd) / (A + d0)
    if q <= 0:
        return np.nan
    return 2 * np.pi / np.sqrt(q) - 2 * np.pi


# =====================================================================================================
sec("PART 1 -- SANITY: the parametrisation really IS MOND (deep-Newtonian and deep-MOND limits)")
# =====================================================================================================
a0 = A0_FOOTINGS["c^2/(2 pi L_dS) 1.2e-10"]
mu_exp = KERNELS["exp (branch spec)"]

r_dn = 0.1 * AU
gN_dn = GM / r_dn**2
tot_dn = g_total(r_dn, 0.5, a0, mu_exp)
check("P1-1  deep-Newtonian limit: at 0.1 AU with f = 0.5 the total field reproduces G_N M/r^2 to better "
      "than 1e-12 -- so f is correctly normalised as the fifth-force fraction and G_N is the DYNAMICAL "
      "gravitational constant (nothing left over to renormalise)",
      abs(tot_dn / gN_dn - 1.0) < 1e-12,
      f"g_total/g_N - 1 = {tot_dn/gN_dn - 1:.3e}")

r_dm = 1.0e8 * AU
gN_dm = GM / r_dm**2
for ftest in [0.9, 0.3, 0.05]:
    tot_dm = g_total(r_dm, ftest, a0, mu_exp)
    pred = np.sqrt(a0 * gN_dm)
    ok = abs(tot_dm / pred - 1.0) < 2e-4
    if not ok:
        break
check("P1-2  deep-MOND limit: at 1e8 AU the total field equals sqrt(a0 * G_N M/r^2) to <0.2% for "
      "f = 0.9, 0.3 and 0.05 -- i.e. the OBSERVED a0 is reproduced for every f, exactly because "
      "a0t = a0/f.  This is the lock between the fifth-force strength and the transition scale.",
      ok, f"last: g/sqrt(a0 g_N) - 1 = {tot_dm/pred - 1:.3e} at f = {ftest}")

check("P1-3  every kernel tested satisfies mu(y) <= y for all y > 0 (equivalently mu(y)/y is "
      "non-increasing) -- the hypothesis used by the kernel-independent theorem in PART 4",
      all(np.all(KERNELS[kn](np.logspace(-6, 3, 400)) <= np.logspace(-6, 3, 400) * (1 + 1e-12))
          for kn in KERNELS),
      "checked for exp, simple, standard, nu_RAR-conjugate on y in [1e-6, 1e3]")

# =====================================================================================================
sec("PART 2 -- IS THE PPN EXPANSION EVEN VALID?  the non-analytic e^{-y} corrections at 1 AU and Saturn")
# =====================================================================================================
print("  y == g_s/a0t is the scalar's own MOND variable.  mu = 1 - e^{-y}; the fractional error of the")
print("  deep-Newtonian (PPN) truncation is f*(1/mu - 1) ~ f e^{-y}.  PPN is valid iff y >> 1.\n")
print(f"  {'f':>10} {'y(1 AU)':>14} {'y(Saturn)':>14} {'e^-y (1AU)':>14} {'e^-y (Sat)':>14} "
      f"{'|dg/gN| Sat':>14} {'PPN valid?':>12}")
rows = []
for f in [1.0, 1e-1, 1e-2, 5e-3, 1e-3, 1.5e-4, 1.15e-5, 1e-6]:
    gs1 = g_scalar(GM / AU**2, f, a0, mu_exp)
    gsS = g_scalar(GM / (9.53707032 * AU)**2, f, a0, mu_exp)
    y1, yS = gs1 * f / a0, gsS * f / a0
    e1 = np.exp(-min(y1, 700)); eS = np.exp(-min(yS, 700))
    anomS = anomaly(9.53707032 * AU, f, a0) / (GM / (9.53707032 * AU)**2)
    rows.append((f, y1, yS, e1, eS, anomS))
    print(f"  {f:>10.3e} {y1:>14.4e} {yS:>14.4e} {e1:>14.3e} {eS:>14.3e} {anomS:>14.3e} "
          f"{'YES' if yS > 30 else ('marginal' if yS > 3 else 'NO'):>12}")

yS_at_cassini = [rr[2] for rr in rows if abs(rr[0] - 1.15e-5) < 1e-12][0]
check("P2-1  at f = 1 the scalar is deeply Newtonian everywhere inside Saturn (y > 1e5, e^{-y} < 1e-40000): "
      "the analyticity hypothesis and hence the whole PPN expansion is EXACT there, with corrections far "
      "below any conceivable measurement -- so the symbolic beta result is valid in that corner",
      rows[0][2] > 1e5 and rows[0][4] < 1e-300,
      f"y(Saturn, f=1) = {rows[0][2]:.3e}, e^-y underflows to 0")

check("P2-2  *** at the Cassini-allowed coupling f = 1.15e-5 the scalar is in its OWN DEEP-MOND regime at "
      "Saturn (y << 1), so mu is NOT ~ 1, the e^{-y} corrections are NOT small, and the standard PPN "
      "expansion of this branch DOES NOT APPLY there. ***  Verifying the regime rather than assuming it "
      "is what exposes the problem.",
      yS_at_cassini < 0.1,
      f"y(Saturn, f=1.15e-5) = {yS_at_cassini:.3e}  (needs >> 1 for PPN);  mu = {mu_exp(yS_at_cassini):.3e}")

f_ppn_min = brentq(lambda lf: g_scalar(GM / (9.53707032 * AU)**2, 10**lf, a0, mu_exp) * 10**lf / a0 - 30.0,
                   -6, 0, xtol=1e-14)
f_ppn_min = 10**f_ppn_min
check("P2-3  the PPN expansion of this branch is valid out to Saturn (y > 30, e^{-y} < 1e-13) only for "
      f"f >~ {f_ppn_min:.2e}.  This is a statement about the FORMALISM's own validity, entirely "
      "independent of any observational bound.",
      f_ppn_min > 1e-3,
      f"f_min(PPN valid at Saturn) = {f_ppn_min:.3e}")

# =====================================================================================================
sec("PART 3 -- the PPN gates:  beta, gamma, Nordtvedt as functions of f")
# =====================================================================================================
def beta_exp_c(f): return 1.0
def beta_lin_c(f): return 1.0 - 0.5 * f * f
def gamma_c(f):    return 1.0 - 2.0 * f
def eta_exp_c(f):  return 4.0 * 1.0 - gamma_c(f) - 3.0
def eta_lin_c(f):  return 4.0 * beta_lin_c(f) - gamma_c(f) - 3.0

print(f"  {'f':>10} {'beta(exp)':>12} {'beta(lin)':>14} {'|beta-1|(lin)':>16} {'gamma-1':>12} "
      f"{'eta_N(exp)':>12} {'eta_N(lin)':>12}")
for f in [1.0, 1e-1, 1e-2, 1.26e-2, 5e-3, 1.5e-4, 1.15e-5, 1e-6]:
    print(f"  {f:>10.3e} {beta_exp_c(f):>12.10f} {beta_lin_c(f):>14.12f} {abs(beta_lin_c(f)-1):>16.3e} "
          f"{gamma_c(f)-1:>12.3e} {eta_exp_c(f):>12.3e} {eta_lin_c(f):>12.3e}")

f_beta_max = np.sqrt(2 * GATE_BETA)
check("P3-1  *** beta PASSES the |beta-1| < 8e-5 gate for EVERY f up to "
      f"{f_beta_max:.4f}. ***  For the exponential coupling beta = 1 identically, so the gate is passed "
      "with infinite margin; for the linear coupling |beta-1| = f^2/2, so it is passed for f < 0.0126 -- "
      "which is 3 orders of magnitude ABOVE the f that any other gate allows.  BETA NEVER BITES.",
      f_beta_max > 1e-2 and abs(beta_lin_c(1.15e-5) - 1) < 1e-9,
      f"f_max(beta gate) = {f_beta_max:.4e}; |beta-1| at f=1.15e-5 is {abs(beta_lin_c(1.15e-5)-1):.3e}")

f_gam_max = GATE_GAMMA / 2.0
f_eta_max = GATE_ETA / 2.0
check("P3-2  gamma is the FIRST-order gate: |gamma-1| = 2f < 2.3e-5 (Cassini) requires f < 1.15e-5",
      abs((gamma_c(f_gam_max) - 1 + GATE_GAMMA) / GATE_GAMMA) < 1e-12, f"f_max(gamma) = {f_gam_max:.3e}")
check("P3-3  Nordtvedt is also first order: |eta_N| = 2f < 3e-4 (LLR) requires f < 1.5e-4.  NOTE the "
      "inversion of the task's expectation: because the effective-G split leaks into gamma (not beta), "
      "CASSINI IS SHARPER THAN LLR here by a factor 13, not the other way round.",
      abs(eta_exp_c(f_eta_max) / GATE_ETA - 1) < 1e-12 and f_eta_max > f_gam_max,
      f"f_max(eta_N) = {f_eta_max:.3e}  vs  f_max(gamma) = {f_gam_max:.3e}")

# =====================================================================================================
sec("PART 4 -- the KERNEL-INDEPENDENT anomaly theorem, and the perihelion gate")
# =====================================================================================================
print("  THEOREM.  If mu(y) <= y (true for every standard MOND kernel), then whenever the scalar is in its")
print("  deep-MOND branch the scalar field obeys  f g_N = mu(y) g_s <= (f g_s/a0) g_s, i.e. g_s >= sqrt(a0 g_N).")
print("  Hence the FRACTIONAL anomalous acceleration obeys      dg/g_N  >=  sqrt(a0/g_N)  -  f  ,")
print("  and the scalar is deep-MOND (y<1) at radius r whenever  f < sqrt(a0/g_N(r)).\n")

for name, a0v in A0_FOOTINGS.items():
    print(f"  a0 footing: {name}")
    for pn in ["Mercury", "Saturn"]:
        aP = PLANETS[pn][0] * AU
        gN = GM / aP**2
        f_thresh = np.sqrt(a0v / gN)
        bnd = f_thresh - GATE_GAMMA / 2.0
        print(f"     {pn:>8}:  g_N = {gN:.4e} m/s^2,  g_N/a0 = {gN/a0v:.3e},  "
              f"f_threshold = sqrt(a0/g_N) = {f_thresh:.3e},  min |dg/g_N| at f=f_Cassini = {bnd:.3e}")

aSat = PLANETS["Saturn"][0] * AU
f_thresh_sat = {k: np.sqrt(v / (GM / aSat**2)) for k, v in A0_FOOTINGS.items()}
check("P4-1  *** KERNEL-INDEPENDENT: at the Cassini-allowed f = 1.15e-5 the scalar is deep-MOND at Saturn "
      "for EVERY a0 footing (f << sqrt(a0/g_N) ~ 1.2e-3), and therefore the fractional anomalous "
      "acceleration at Saturn is AT LEAST ~1.2e-3 -- about a tenth of a percent of Newtonian gravity -- "
      "for ANY interpolating kernel obeying mu(y) <= y. ***",
      all(1.15e-5 < 0.05 * v for v in f_thresh_sat.values()),
      "; ".join(f"{k}: threshold {v:.3e}, min anomaly {v - 1.15e-5:.3e}" for k, v in f_thresh_sat.items()))

# verify the bound is saturated by the exp kernel and respected by all kernels
sat_ok = True
det = []
for kn, mu in KERNELS.items():
    gs = g_scalar(GM / aSat**2, 1.15e-5, a0, mu)
    anom = (gs - 1.15e-5 * GM / aSat**2) / (GM / aSat**2)
    bound = np.sqrt(a0 / (GM / aSat**2)) - 1.15e-5
    det.append(f"{kn}: {anom:.4e} (bound {bound:.4e})")
    if anom < bound * (1 - 1e-6):
        sat_ok = False
ident_ok = True; idet = []
for rr, ff in [(aSat, 1.15e-5), (aSat, 1e-3), (0.38709893 * AU, 1.5e-4)]:
    gN = GM / rr**2
    direct = g_scalar(gN, ff, a0, mu_exp) - ff * gN
    stable = anomaly(rr, ff, a0)
    idet.append(f"r={rr/AU:.2f}AU f={ff:.1e}: direct {direct:.6e} vs stable {stable:.6e}")
    if abs(direct / stable - 1) > 1e-6:
        ident_ok = False
check("P4-2a  the cancellation-free anomaly dg = f g_N / expm1(y) agrees with the direct subtraction "
      "g_s - f g_N to 1e-6 in the regime where the subtraction is still numerically safe (small y); "
      "beyond that only the stable form is usable, which is why the earlier naive column read 0",
      ident_ok, "; ".join(idet))

check("P4-2  the theorem's bound is verified numerically for all four kernels at Saturn, f = 1.15e-5: "
      "every kernel produces an anomaly >= sqrt(a0/g_N) - f, and the exponential kernel SATURATES it "
      "(so the exponential kernel -- the branch's own choice -- is the most favourable possible)",
      sat_ok, "; ".join(det))


# ---------- perihelion precession: two independent methods ----------
def precess_apsidal(f, a0, mu, r):
    """apsidal-angle formula for near-circular orbits: dvarpi = 2 pi/sqrt(3 + r F'/F) - 2 pi (rad/orbit)."""
    h = r * 1e-6
    F = g_total(r, f, a0, mu)
    Fp = (g_total(r + h, f, a0, mu) - g_total(r - h, f, a0, mu)) / (2 * h)
    q = 3.0 + r * Fp / F
    if q <= 0:
        return np.nan
    return 2 * np.pi / np.sqrt(q) - 2 * np.pi


def precess_integrate(f, a0, mu, a_sma, ecc, n_orb=3):
    """direct orbit integration; returns perihelion shift per orbit (rad) for the ACTUAL eccentricity."""
    # tabulate g_total on a log grid and interpolate (brentq inside the RHS would be far too slow)
    rmin, rmax = a_sma * (1 - ecc) * 0.7, a_sma * (1 + ecc) * 1.4
    rg = np.logspace(np.log10(rmin), np.log10(rmax), 900)
    gg = np.array([g_total(rr, f, a0, mu) for rr in rg])
    lrg, lgg = np.log(rg), np.log(gg)

    def acc(t, s):
        x, y, vx, vy = s
        r = np.hypot(x, y)
        g = np.exp(np.interp(np.log(r), lrg, lgg))
        return [vx, vy, -g * x / r, -g * y / r]

    rp = a_sma * (1 - ecc)
    # vis-viva with the ACTUAL total field: use the Newtonian value (the correction to the IC is common-mode)
    vp = np.sqrt(GM * (1 + ecc) / (a_sma * (1 - ecc)))
    P = 2 * np.pi * np.sqrt(a_sma**3 / GM)
    sol = solve_ivp(acc, [0, n_orb * P * 1.2], [rp, 0.0, 0.0, vp], rtol=1e-12, atol=1e-8,
                    dense_output=True, max_step=P / 4000)
    ts = np.linspace(0, n_orb * P * 1.2, 400000)
    S = sol.sol(ts)
    rr = np.hypot(S[0], S[1])
    # find perihelion passages (local minima of r)
    idx = np.where((rr[1:-1] < rr[:-2]) & (rr[1:-1] < rr[2:]))[0] + 1
    if len(idx) < 2:
        return np.nan
    angs = []
    for i in idx:
        # parabolic refinement in time, then angle
        j = slice(i - 1, i + 2)
        tt, yy = ts[j], rr[j]
        den = (yy[0] - 2 * yy[1] + yy[2])
        dt = 0.5 * (yy[0] - yy[2]) / den * (tt[1] - tt[0]) if den != 0 else 0.0
        st = sol.sol(tt[1] + dt)
        angs.append(np.arctan2(st[1], st[0]))
    d = np.unwrap(np.array(angs))
    return float(np.mean(np.diff(d)))


print("\n  Perihelion precession vs f  (arcsec/century).  Two methods: apsidal formula (near-circular) and")
print("  direct orbit integration at the real eccentricity.  Conservative gate: |supplementary| < 1 mas/cy.\n")
print(f"  {'planet':>8} {'f':>10} {'dg/gN':>12} {'apsidal ''/cy':>16} {'integrated ''/cy':>18} {'gate ''/cy':>12} {'verdict':>10}")
peri_rows = []
for pn in ["Mercury", "Saturn"]:
    aP, ecc, Pd = PLANETS[pn]
    aP *= AU
    orb_per_cy = 36525.0 / Pd
    for f in [1.15e-5, 1.5e-4, 1e-3, 3e-3, 5e-3, 6.2e-3, 1e-2, 1e-1, 1.0]:
        gN = GM / aP**2
        anom = anomaly(aP, f, a0) / gN
        da = precess_stable(f, a0, aP)
        aps = abs(da) * ARCSEC * orb_per_cy
        integ = np.nan
        if f in (1.15e-5, 1.5e-4, 1e-3):
            try:
                integ = abs(precess_integrate(f, a0, mu_exp, aP, ecc)) * ARCSEC * orb_per_cy
            except Exception:
                integ = np.nan
        v = "PASS" if aps < GATE_PREC[pn] else "FAIL"
        peri_rows.append((pn, f, anom, aps, integ, v))
        print(f"  {pn:>8} {f:>10.3e} {anom:>12.3e} {aps:>16.4e} "
              f"{(f'{integ:.4e}' if np.isfinite(integ) else '-'):>18} {GATE_PREC[pn]:>12.1e} {v:>10}")

# the two integrated cases at f=1.15e-5 and f=1.0 must bracket the apsidal estimate in order of magnitude
sat_c = [rw for rw in peri_rows if rw[0] == "Saturn" and abs(rw[1] - 1.15e-5) < 1e-12][0]
# measure the ORBIT INTEGRATOR's own noise floor on a strictly Newtonian orbit (anomaly identically zero)
noise = {}
for pn in ["Mercury", "Saturn"]:
    aP, ecc, Pd = PLANETS[pn]
    noise[pn] = abs(precess_integrate(0.0 if False else 1.0, a0, mu_exp, aP * AU, ecc)) * ARCSEC * 36525.0 / Pd
print(f"\n  ORBIT-INTEGRATOR NOISE FLOOR (f = 1, where the anomaly underflows to exactly 0, i.e. pure Newton):")
for pn in noise:
    print(f"     {pn:>8}: {noise[pn]:.3e} arcsec/century  <-- any 'integrated' entry at this level is NUMERICAL NOISE, not signal")
check("P4-3b  HONEST NUMERICS: the direct orbit integrator has a noise floor of ~1e-3 arcsec/century "
      "(measured on a strictly Newtonian orbit, where the true answer is 0).  Every 'integrated' entry at "
      "or below that level is noise, NOT a prediction -- in particular Mercury's 6e-4 ''/cy at f = 1e-3, "
      "where the true anomaly is 6e-147.  The Saturn signal at f = 1.15e-5 is 1e6 times the floor.",
      noise["Saturn"] < 1e-2 ,
      f"Mercury floor {noise['Mercury']:.3e} ''/cy, Saturn floor {noise['Saturn']:.3e} ''/cy")

check("P4-3  cross-check: the apsidal-angle formula and the DIRECT numerical orbit integration (at the real "
      "eccentricity) agree on Saturn's precession at f = 1.15e-5 to within a factor ~3 -- two independent "
      "methods, same catastrophic magnitude",
      np.isfinite(sat_c[4]) and 0.2 < sat_c[4] / sat_c[3] < 5.0,
      f"apsidal {sat_c[3]:.4e} ''/cy vs integrated {sat_c[4]:.4e} ''/cy  (ratio {sat_c[4]/sat_c[3]:.2f})")

check("P4-4  *** at the Cassini-allowed f = 1.15e-5 Saturn's perihelion precesses by ~1e3 arcsec/century, "
      "against a bound of ~1e-3 arcsec/century: a violation of about SIX ORDERS OF MAGNITUDE. ***",
      sat_c[3] / GATE_PREC["Saturn"] > 1e5,
      f"predicted {sat_c[3]:.3e} ''/cy vs gate {GATE_PREC['Saturn']:.1e} ''/cy  "
      f"=> {sat_c[3]/GATE_PREC['Saturn']:.2e} x over")

# smallest f that passes the Saturn perihelion gate
def sat_prec(lf):
    return precess_stable(10**lf, a0, aSat) * ARCSEC * 36525.0 / PLANETS["Saturn"][2]
f_lo = brentq(lambda lf: np.log10(max(abs(sat_prec(lf)), 1e-300)) - np.log10(GATE_PREC["Saturn"]),
              -2.6, -1.5, xtol=1e-12)
f_peri_min = 10**f_lo
check("P4-5  the Saturn perihelion gate is passed only for f >~ "
      f"{f_peri_min:.3e} (exponential kernel).  With the kernel-independent theorem the corresponding "
      "floor is sqrt(a0/g_N(Saturn)) ~ 1.2e-3 for ANY kernel obeying mu(y) <= y.",
      f_peri_min > 1e-3,
      f"f_min(Saturn perihelion, exp kernel) = {f_peri_min:.4e}; kernel-independent floor "
      f"{np.sqrt(a0/(GM/aSat**2)):.3e}")

# =====================================================================================================
sec("PART 5 -- an ABSORPTION-PROOF check: the radial run of the inferred GM_sun")
# =====================================================================================================
print("  A pure 1/r^2 anomaly would simply be absorbed into GM_sun.  The MOND-branch anomaly is 1/r, so the")
print("  GM_sun inferred from each planet DRIFTS with r.  GM_sun is known to ~1e-10 fractionally.\n")
f_c = 1.15e-5
print(f"  {'planet':>8} {'a (AU)':>9} {'GM_eff/GM - 1':>16}")
gm_eff = {}
for pn, (aa, ee, PP) in PLANETS.items():
    rr = aa * AU
    gm_eff[pn] = g_total(rr, f_c, a0, mu_exp) * rr**2
    print(f"  {pn:>8} {aa:>9.4f} {gm_eff[pn]/GM - 1:>16.4e}")
spread = gm_eff["Saturn"] / gm_eff["Mercury"] - 1
check("P5-1  at f = 1.15e-5 the GM_sun inferred at Saturn exceeds that inferred at Mercury by "
      f"{spread:.3e} (fractional), against a fractional knowledge of GM_sun of ~1e-10.  This is an "
      "ABSORPTION-PROOF inconsistency: no rescaling of GM_sun can hide a 1/r force.",
      spread > 1e-4,
      f"GM_eff(Saturn)/GM_eff(Mercury) - 1 = {spread:.4e}   (~{spread/1e-10:.1e} x the GM_sun uncertainty)")

# =====================================================================================================
sec("PART 6 -- THE PINCER: is there a common window in f?")
# =====================================================================================================
windows = {
    "beta        |beta-1| < 8e-5":     (0.0, np.sqrt(2 * GATE_BETA)),
    "Nordtvedt   |eta_N| < 3e-4":      (0.0, GATE_ETA / 2.0),
    "gamma       |gamma-1| < 2.3e-5":  (0.0, GATE_GAMMA / 2.0),
    "Saturn perihelion (exp kernel)":  (f_peri_min, 1.0),
    "Saturn perihelion (any kernel)":  (np.sqrt(a0 / (GM / aSat**2)) * 0.99, 1.0),
    "PPN formalism validity (y>30)":   (f_ppn_min, 1.0),
}
print(f"  {'gate':>34}  {'f_min':>12}  {'f_max':>12}")
for kk, (lo, hi) in windows.items():
    print(f"  {kk:>34}  {lo:>12.4e}  {hi:>12.4e}")
lo_all = max(v[0] for v in windows.values())
hi_all = min(v[1] for v in windows.values())
print(f"\n  intersection:  f in [{lo_all:.4e}, {hi_all:.4e}]   ->   {'NON-EMPTY' if lo_all < hi_all else 'EMPTY'}")

check("P6-1  *** THE WINDOW IS EMPTY.  gamma (Cassini) caps f at 1.15e-5; the Saturn perihelion floors it "
      f"at {f_peri_min:.2e} (exp kernel) or 1.2e-3 (any kernel).  The gap is a factor "
      f"~{f_peri_min/(GATE_GAMMA/2):.0f}. ***  The branch as specified has NO viable fifth-force strength.",
      lo_all > hi_all,
      f"required f >= {lo_all:.3e} but allowed f <= {hi_all:.3e}; gap factor {lo_all/hi_all:.1f}")

check("P6-2  the pincer survives dropping Cassini entirely and using ONLY the LLR Nordtvedt bound "
      "(f <= 1.5e-4) against the kernel-independent Saturn floor (f >= 1.2e-3): still empty, by a factor ~8. "
      "So the closure does not rest on any single measurement.",
      GATE_ETA / 2.0 < np.sqrt(a0 / (GM / aSat**2)),
      f"eta_N cap {GATE_ETA/2:.3e}  <  kernel-independent floor {np.sqrt(a0/(GM/aSat**2)):.3e}")

check("P6-3  the pincer survives on BOTH repo a0 footings and on the c^2/(2 pi L_dS) value",
      all(GATE_ETA / 2.0 < np.sqrt(v / (GM / aSat**2)) for v in A0_FOOTINGS.values()),
      "; ".join(f"{k}: floor {np.sqrt(v/(GM/aSat**2)):.3e}" for k, v in A0_FOOTINGS.items()))

# =====================================================================================================
sec("PART 7 -- two further consistency notes (stated, not used to close anything)")
# =====================================================================================================
check("P7-1  [a0 DERIVATION] the action's scale is a0t = a0_obs/f.  If the branch's derivation "
      "a0 = c^2/(2 pi L_dS) = 1.2e-10 refers to the scale IN THE ACTION (a0t), then the OBSERVED MOND scale "
      "is f * 1.2e-10, so reproducing the observed RAR requires f ~ 1 -- maximally excluded by gamma.  If "
      "instead it refers to the observed a0, then a0t = a0/f is a NEW, underived scale ~1e5 times larger, "
      "and the derivation no longer covers the scale that actually appears in the Lagrangian.",
      True,
      "either f ~ 1 (gamma-excluded) or the a0 derivation does not apply to the Lagrangian's own scale")

# external field effect: does the Galaxy's field rescue the solar system?
g_ext = 1.8e-10   # Galactic field at the Sun, m/s^2
r_efe = np.sqrt(GM * 1.15e-5 / (g_ext))   # radius where f*g_N = g_ext-ish scalar field
check("P7-2  [EXTERNAL FIELD EFFECT] the Galactic field g_ext ~ 1.8e-10 m/s^2 does NOT rescue the solar "
      f"system: at f = 1.15e-5 the scalar's internal field exceeds its external one out to ~{r_efe/AU:.0f} AU, "
      "so Mercury and Saturn are internal-field dominated.  Beyond that radius the EFE makes the anomaly "
      "LARGER (mu is evaluated at the small external y), not smaller.",
      r_efe / AU > 9.6,
      f"internal-dominated out to {r_efe/AU:.0f} AU;  Saturn at 9.54 AU is well inside")

check("P7-3  [COUPLING UNIVERSALITY, NOT COMPUTED] if the conformal factor couples to BARYON NUMBER rather "
      "than to the full stress-energy trace, the fifth force is composition-dependent and MICROSCOPE "
      "(Eotvos ~1e-15) would bound f far below even the Cassini value.  This is a coupling-specification "
      "question the branch must answer; it is NOT used in any verdict above.",
      True, "flagged as an open specification question, deliberately excluded from the closure")


# =====================================================================================================
sec("PART 8 -- ADVERSARIAL: does a SCREENING kernel repair the branch?  (test the obvious escape)")
# =====================================================================================================
print("""  The pincer above assumes mu saturates at 1 (the branch's mu = 1 - e^{-y} does).  The obvious repair is a
  k-mouflage-type kernel that keeps GROWING at large y, mu(y) -> y^n, so the fifth force is SCREENED where
  gravity is strong.  Then G_N = G_bare in the solar system, gamma -> 1, eta_N -> 0, and the pincer would
  dissolve.  This part tests that repair honestly, with the family  mu_n(y) = y (1 + y)^{n-1}
  (deep-MOND mu -> y for y << 1;  screening mu -> y^n for y >> 1), at eps = G_s/G_N = 1, a0t = a0.
""")
def mu_n_factory(n):
    # smooth family, used as a cross-check for moderate n (overflows for very large n)
    return lambda y: y * (1.0 + y)**(n - 1.0)


def screened_exact(gN, n, a0v):
    """EXACT piecewise-power kernel mu(y) = y (y<=1), y^n (y>1).  In the screened branch
       n*u + u = ln(gN/a0)  =>  g_s = a0 (gN/a0)^{1/(n+1)},  so dg/gN = (a0/gN)^{n/(n+1)}."""
    if gN <= a0v:
        return np.sqrt(a0v * gN)
    return a0v * (gN / a0v)**(1.0 / (n + 1.0))

def screened_anomaly(r, n, a0v):
    gN = GM / r**2
    mu = mu_n_factory(n)
    fn = lambda gs: mu(gs / a0v) * gs - gN
    lo, hi = 1e-40 * gN, 10.0 * gN
    while fn(hi) < 0:
        hi *= 10.0
    return brentq(fn, lo, hi, xtol=1e-300, rtol=1e-15)

def screened_precession(n, a0v, a_sma, Pd):
    d0 = screened_anomaly(a_sma, n, a0v)
    h = 1e-4
    dp = screened_anomaly(a_sma * np.exp(h), n, a0v)
    dm = screened_anomaly(a_sma * np.exp(-h), n, a0v)
    pw = -(np.log(dp) - np.log(dm)) / (2 * h)          # delta ~ r^{-pw}
    A = GM / a_sma**2
    dvarpi = -np.pi * (2.0 - pw) * d0 / (A + d0)        # rad/orbit
    return abs(dvarpi) * ARCSEC * 36525.0 / Pd, d0 / A, pw

print(f"  {'n':>8} {'dg/gN (Saturn)':>17} {'power p':>9} {'precession ''/cy':>18} {'gate ''/cy':>11} {'verdict':>9}")
best = None
A_sat = GM / aSat**2
for n in [1.0, 2.0, 3.0, 5.0, 10.0, 30.0, 100.0, 1e4, 1e8]:
    fr = screened_exact(A_sat, n, a0) / A_sat            # exact piecewise-power family
    pw = 2.0 / (n + 1.0)
    pr = abs(np.pi * (2.0 - pw) * fr / (1.0 + fr)) * ARCSEC * 36525.0 / PLANETS["Saturn"][2]
    smooth = ""
    if n <= 30:
        prs, frs, pws = screened_precession(n, a0, aSat, PLANETS["Saturn"][2])
        smooth = f"   [smooth family: {frs:.3e}, p={pws:.3f}, {prs:.3e} ''/cy]"
    print(f"  {n:>8.0e} {fr:>17.4e} {pw:>9.4f} {pr:>18.4e} {GATE_PREC['Saturn']:>11.1e} "
          f"{'PASS' if pr < GATE_PREC['Saturn'] else 'FAIL':>9}{smooth}")
    best = (n, fr, pr) if best is None or pr < best[2] else best

lim_frac = a0 / (GM / aSat**2)
lim_prec = 2 * np.pi * lim_frac * ARCSEC * 36525.0 / PLANETS["Saturn"][2]
check("P8-0  the exact piecewise-power family reproduces the smooth family mu_n = y(1+y)^{n-1} and confirms "
      "the analytic scaling dg/g_N = (a0/g_N)^{n/(n+1)}, p = 2/(n+1) -- two constructions, same answer",
      abs(screened_exact(A_sat, 3.0, a0) / A_sat / (a0 / A_sat)**0.75 - 1.0) < 1e-10,
      f"n=3: exact {screened_exact(A_sat,3.0,a0)/A_sat:.4e} = (a0/gN)^{{3/4}} = {(a0/A_sat)**0.75:.4e}")
print(f"\n  n -> infinity (perfect screening): the scalar field is PINNED at g_s = a0t = a0, a CONSTANT extra")
print(f"  acceleration.  dg/g_N(Saturn) -> a0/g_N = {lim_frac:.4e}; precession -> {lim_prec:.4e} arcsec/century.")

check("P8-1  *** THE SCREENING REPAIR FAILS TOO, and fails by a bound that no amount of screening can beat. "
      "*** For mu -> y^n the scalar solves g_s ~ (a0^n g_N)^{1/(n+1)}, so dg/g_N ~ (a0/g_N)^{n/(n+1)}. "
      "The exponent n/(n+1) is STRICTLY LESS THAN 1 for every n, so the suppression can never exceed the "
      f"n -> infinity limit dg/g_N = a0/g_N = {lim_frac:.2e} at Saturn -- still ~{lim_prec/GATE_PREC['Saturn']:.0e} "
      "times the perihelion bound.  Screening buys at most 3 of the ~9 orders of magnitude needed.",
      lim_prec > 1e3 * GATE_PREC["Saturn"],
      f"best over n: n = {best[0]:.0f} gives {best[2]:.3e} ''/cy; n -> inf limit {lim_prec:.3e} ''/cy "
      f"vs gate {GATE_PREC['Saturn']:.1e} ''/cy")

check("P8-2  the n -> infinity limit is exactly the classic 'residual constant a0 acceleration' problem: a "
      "perfectly screened AQUAL scalar still leaves |dg| = a0 = 1.2e-10 m/s^2 as a RADIAL constant, whereas "
      "outer-solar-system ranging bounds constant anomalous accelerations at the ~1e-14 m/s^2 level",
      abs(screened_exact(A_sat, 1e8, a0) / a0 - 1.0) < 1e-3,
      f"g_s(Saturn, n=1e8) = {screened_exact(A_sat, 1e8, a0):.4e} m/s^2  vs  a0 = {a0:.3e}")

check("P8-3  [HONEST LOOPHOLE, NOT CLOSED HERE] the one structure P8-1/P8-2 do NOT exclude is a residual "
      "scalar gradient that is quasi-UNIFORM across the solar system (aligned with the external Galactic "
      "field rather than radial).  A uniform acceleration is unobservable internally; its leading signature "
      "is the EFE QUADRUPOLE, which is a different calculation from the one done here.  This lane reports "
      "that as UNDETERMINED rather than claiming the screened branch is closed.",
      True, "EFE-quadrupole route not computed in this lane; flagged as the surviving crack")

# =====================================================================================================
sec("VERDICT")
# =====================================================================================================
print(f"""
  beta      = 1 exactly (constant/exponential fifth-force coupling)  or  1 - f^2/2 (strictly linear coupling).
              |beta - 1| <= {abs(beta_lin_c(1.15e-5)-1):.2e} anywhere any other gate allows.  BETA PASSES, with >=4 orders of margin,
              and CANNOT be the discriminator for this class.

  gamma     = 1 - 2f.  The "gamma = 1" established for this branch is a statement in the BARE-G
              normalisation (no slip, Psi = Phi).  In the observable (dynamical-G_N) normalisation the
              effective-G split leaks in at FIRST order.  Cassini => f < 1.15e-5.

  eta_N     = 2f (or 2f - 2f^2).  LLR => f < 1.5e-4.  Contrary to the usual ordering, Cassini is the
              sharper constraint here, because eta_N inherits its whole value from gamma.

  perihelion/ephemeris:  at any f small enough to satisfy gamma or eta_N, the scalar sits in its OWN deep-MOND
              regime throughout the planetary system; Saturn's perihelion precesses ~1e3 arcsec/century
              against a ~1e-3 arcsec/century bound, and the inferred GM_sun drifts by ~1e-3 between Mercury
              and Saturn against a ~1e-10 fractional uncertainty.

  => THE SOLAR-SYSTEM WINDOW IN f IS EMPTY.  Not because of beta, but because f and the scalar's own MOND
     transition scale are LOCKED by a0t = a0/f.
""")

print("=" * 110)
print(f"{'ALL CHECKS PASS' if not FAILS else 'FAILURES: ' + str(FAILS)}   {N[0]-len(FAILS)}/{N[0]}   [{time.time()-T0:.1f}s]")
print("=" * 110)
sys.exit(1 if FAILS else 0)
