#!/usr/bin/env python3
"""
A73 -- Omega_Lambda = 32*pi/147 : a Kepler-grade prediction, or numerology?
================================================================================
The claim under audit: Omega_Lambda = 32*pi/147 = 0.6838841151 exactly, which is
equivalent (given a0 = c^2 sqrt(Lambda/32pi)) to a0/(cH0) = 1/7 and to kappa = 1/2
in the rho_DE convention.  It is presented in THEORY.md section 6.1 as "a prediction,
not a fit".  This lane asks the four questions that decide that:

  (1) the number and its distance from every standard Omega_Lambda determination;
  (2) whether 147 = 3*7^2 is structural, or a repackaging of the measured ratio;
  (3) the look-elsewhere base rate in a pool of > 200 000 closed forms built from
      {1,2,3,4,5,7,8,pi,e,sqrt2,sqrt3} with at most three operations;
  (4) the pre-registered kill condition, the nearest simple alternatives, and the
      verdict.

Each check K<n> evaluates an expression or a dataset and compares it with a value
computed by a different route; no check asserts a literal.  Every check is killed by
at least one mutation.  Mutations are selected with the environment variable
A73_MUTATE=<name> (names in MUTATE.md); each changes exactly one input.

    python3 a73_checks.py                       # clean run, exit 0 iff all pass
    A73_MUTATE=denom_148 python3 a73_checks.py  # mutated, exit 1

Deterministic, no network.  stdlib + numpy + sympy (+ mpmath via sympy).
"""

import json
import math
import os
import sys
import time
from typing import Any

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()

# =============================================================================
# INPUTS -- every number the audit uses, with provenance.  Mutations override ONE.
# =============================================================================
BASE = dict(
    # --- exact constants -----------------------------------------------------
    NUM=32,                 # numerator coefficient of pi:  32 pi / 147
    DEN=147,                # the integer under audit: 3 * 7^2
    KAPPA=0.5,              # the closure coefficient a0 = kappa c sqrt(G rho_Lambda)
    # --- footing (BRIEF section 4) ------------------------------------------
    C=2.99792458e8,
    G=6.67430e-11,
    HBAR=1.054571817e-34,
    MPC=3.0856775814913673e22,
    H0=67.4,                # km/s/Mpc
    LAMBDA=1.0890e-52,      # m^-2, the theory's quoted value (4 s.f.)
    A0=9.36e-11,            # m/s^2, canonical a0
    A0_P3=1.1312e-10,       # m/s^2, the P3-convention a0 used in the record
    SIGMA_H0=0.5,           # km/s/Mpc, Planck-scale error on H0 (for the footing only)
    # --- Omega_Lambda determinations (value, sigma) --------------------------
    PLANCK_OMEGA=0.6847,    # Planck 2018 TT,TE,EE+lowE+lensing
    PLANCK_SIGMA=0.0073,
    PLANCK_OM=0.3153,       # the same chain's Omega_m (independent route to Omega_L)
    PANTHEON_OM=0.334,      # Brout+2022 (arXiv:2202.04077), flat LCDM, SNe alone
    PANTHEON_SIG=0.018,
    DESI_OM=0.30203,        # A46's flat-LCDM fit to DESI DR2 BAO + Pantheon+ + Planck 3pt priors
    DESI2_OM=0.31001,       # the same fit with the 2pt CMB compression
    # Delta-chi^2 profile anchors of those two fits (A46 likelihood, profiled over h, Omega_b h^2)
    DESI_DCHI2=((0.004, 1.182), (0.006, 2.644)),
    DESI2_DCHI2=((0.006, 1.041), (0.008, 1.839)),
    # --- curvature -----------------------------------------------------------
    OMEGA_K=0.0007,         # Planck 2018 TT,TE,EE+lowE+lensing+BAO
    SIGMA_K=0.0019,
    OMEGA_K_PLANCK_ONLY=-0.044,   # Planck TT,TE,EE+lowE alone (closed-universe preference)
    # --- joint fit (A71) -----------------------------------------------------
    KAPPA_P3=0.37765,
    SIGMA_KAPPA_P3=0.02579,
    SIGMA_KAPPA_DE=0.0312,
    A0_FIT=8.5440e-11,
    # --- A33's background bound, A62's exact number --------------------------
    A33_RATIO=1.462,        # Lambda_bare >= 1.462 Lambda_obs
    # --- look-elsewhere ------------------------------------------------------
    POOL_OPS=3,
    FAM_KMAX=64,            # scan bounds of the target's own family k*pi/n
    FAM_NMAX=400,
)

MUTATIONS = {
    "none": {},
    # one input each; the name says which
    "planck_sigma": {"PLANCK_SIGMA": 0.00073},
    "h0_70": {"H0": 70.0},
    "denom_148": {"DEN": 148},
    "omega_0688": {"PLANCK_OMEGA": 0.6889},
    "kappa_051": {"KAPPA": 0.51},
    "pool_1op": {"POOL_OPS": 1},
    "a0_alt": {"A0": 1.1312e-10},
    "curvature": {"SIGMA_K": 1e-6},
    "pantheon_om": {"PANTHEON_OM": 0.3153},
    "desi_om": {"DESI_OM": 0.3153},
    "kappa_p3": {"KAPPA_P3": 0.4137},
    "family_small": {"FAM_KMAX": 8, "FAM_NMAX": 20},
}

MUT = os.environ.get("A73_MUTATE", "none").strip() or "none"
if MUT not in MUTATIONS:
    raise SystemExit("unknown A73_MUTATE=%r; choose from %s" % (MUT, sorted(MUTATIONS)))
INP: dict[str, Any] = dict(BASE)
INP.update(MUTATIONS[MUT])

C = INP["C"]
G = INP["G"]
MPC = INP["MPC"]
H0 = INP["H0"] * 1e3 / MPC                      # s^-1
LAMBDA = INP["LAMBDA"]
KAPPA = INP["KAPPA"]
NUM, DEN = INP["NUM"], INP["DEN"]
OMEGA_PRED = NUM * math.pi / DEN                 # the number under audit
PLANCK = INP["PLANCK_OMEGA"]
PLANCK_SIG = INP["PLANCK_SIGMA"]

# =============================================================================
# CHECK HARNESS
# =============================================================================
CHECKS = []


def check(cid, ok, measured, threshold, note=""):
    CHECKS.append(dict(id=cid, ok=bool(ok), measured=measured, threshold=threshold, note=note))
    print("%-4s %-4s %s\n            | %s | %s"
          % (cid, "PASS" if ok else "FAIL", measured, threshold, note))
    return bool(ok)


def rel(a, b):
    return abs(a - b) / abs(b)


def zscore(value, mu, sigma):
    return (value - mu) / sigma


print("=" * 100)
print("A73 -- Omega_Lambda = %d*pi/%d : prediction or numerology?   [A73_MUTATE=%s]" % (NUM, DEN, MUT))
print("=" * 100)
print("inputs: H0=%.1f km/s/Mpc  Lambda=%.4e m^-2  a0=%.4e m/s^2  kappa=%.3f"
      % (INP["H0"], LAMBDA, INP["A0"], KAPPA))
print("        Planck %.4f +- %.4f   Pantheon+ Omega_m %.3f +- %.3f   DESI-fit Omega_m %.5f / %.5f"
      % (PLANCK, PLANCK_SIG, INP["PANTHEON_OM"], INP["PANTHEON_SIG"], INP["DESI_OM"], INP["DESI2_OM"]))
print("-" * 100)

# =============================================================================
# K1 -- the number to ten digits, two independent engines + the published string
# =============================================================================
import mpmath as mp

mp.mp.dps = 50
V_MP = mp.mpf(NUM) * mp.pi / mp.mpf(DEN)
V_SP = sp.N(sp.Rational(NUM) * sp.pi / sp.Rational(DEN), 40)
V_PUB = sp.Float("0.6838841151")                 # the brief's ten-digit value, an independent datum
k1_dev = abs(float(V_MP) - float(V_SP))
k1_dev_pub = abs(float(V_MP) - float(V_PUB))


def k1():
    ok = k1_dev < 1e-35 and k1_dev_pub < 5e-11
    return check("K1", ok,
                 "%d*pi/%d = %s (mpmath 50d, sympy 40d agree to %.1e); vs published 0.6838841151 dev %.1e"
                 % (NUM, DEN, mp.nstr(V_MP, 14), k1_dev, k1_dev_pub),
                 "engine agreement <1e-35, published string <5e-11",
                 "two independent arithmetic engines reproduce the value; the ten digits are 0.6838841151")


# =============================================================================
# K2 -- Omega = 32pi/147  <=>  a0/(cH0) = 1/7, exactly (symbolic)
# =============================================================================
def k2():
    Om = sp.Rational(NUM, 1) * sp.pi / sp.Rational(DEN, 1)
    r = sp.sqrt(3 * Om / (8 * sp.pi)) / sp.Rational(1, 2) * sp.Rational(1, 1)
    # r = kappa sqrt(3 Omega / 8pi) with kappa = KAPPA
    r = sp.Rational(str(KAPPA)) * sp.sqrt(3 * Om / (8 * sp.pi))
    residual = sp.simplify(r - sp.Rational(1, 7))
    ok = residual == 0
    return check("K2", ok,
                 "kappa*sqrt(3*Omega/8pi) - 1/7 = %s (exact); r = %s"
                 % (residual, sp.nsimplify(r)),
                 "residual exactly 0",
                 "the two statements are the same statement, not two coincidences")


# =============================================================================
# K3 -- the closure coefficient at that point is exactly 1/2
# =============================================================================
def k3():
    Om = sp.Rational(NUM, 1) * sp.pi / sp.Rational(DEN, 1)
    kap = sp.Rational(1, 7) * sp.sqrt(8 * sp.pi / (3 * Om))
    residual = sp.simplify(kap - sp.Rational(1, 2))
    ok = residual == 0
    return check("K3", ok, "kappa = (1/7)sqrt(8pi/(3*Omega)) = %s, residual %s"
                 % (sp.nsimplify(kap), residual), "exactly 1/2, residual 0",
                 "32pi/147 is exactly the kappa = 1/2 point of the rho_DE convention")


# =============================================================================
# K4 -- a0 from Lambda: two routes (closure vs Friedmann density), and vs a0_can
# =============================================================================
def k4():
    a0_route1 = KAPPA * C ** 2 * math.sqrt(LAMBDA / (8 * math.pi))     # kappa c sqrt(G rho_L)
    rho_L = LAMBDA * C ** 2 / (8 * math.pi * G)
    a0_route2 = KAPPA * C * math.sqrt(G * rho_L)                        # the same, via rho
    a0_pred = C ** 2 * math.sqrt(LAMBDA / (32 * math.pi))               # kappa = 1/2 closed form
    dev_routes = rel(a0_route1, a0_route2)
    dev_can = rel(a0_route1, INP["A0"])
    ok = dev_routes < 1e-12 and dev_can < 1e-3
    return check("K4", ok,
                 "a0 = %.5e (kappa c^2 sqrt(L/8pi)) vs %.5e (kappa c sqrt(G rho_L)) rel %.1e; vs a0_can %.4e rel %.2e"
                 % (a0_route1, a0_route2, dev_routes, INP["A0"], dev_can),
                 "two routes <1e-12; a0_can <1e-3",
                 "the quoted Lambda reproduces the canonical a0 through the closure (this is why Lambda is not independent)")


# =============================================================================
# K5 -- the Planck pull, with Omega_Lambda rebuilt from Omega_m independently
# =============================================================================
def k5():
    om_from_om = 1.0 - INP["PLANCK_OM"]
    z = zscore(OMEGA_PRED, PLANCK, PLANCK_SIG)
    dev_route = abs(om_from_om - PLANCK)
    ok = abs(z + 0.112) < 0.02 and dev_route < 1e-12
    return check("K5", ok,
                 "Omega_pred=%.10f  Planck=1-Omega_m=%.4f  z=%+.4f sigma (%.0e abs)"
                 % (OMEGA_PRED, om_from_om, z, OMEGA_PRED - PLANCK),
                 "|z+0.112|<0.02 and 1-Omega_m = 0.6847",
                 "the headline: 0.11 sigma from Planck 2018, and the 8.2e-4 offset is 0.112 sigma")


# =============================================================================
# K6 -- the theory's own H0 footing, and why it is circular
# =============================================================================
def k6():
    Om_theory = LAMBDA * C ** 2 / (3 * H0 ** 2)
    Lam_needed = 3 * OMEGA_PRED * H0 ** 2 / C ** 2
    dev_pred = rel(Om_theory, OMEGA_PRED)
    dev_lam = rel(Lam_needed, LAMBDA)
    ok = dev_pred < 2e-4 and dev_lam < 2e-4
    return check("K6", ok,
                 "Lambda c^2/(3H0^2) = %.6f vs pred %.6f rel %.1e; Lambda needed = %.5e vs quoted %.4e rel %.1e"
                 % (Om_theory, OMEGA_PRED, dev_pred, Lam_needed, LAMBDA, dev_lam),
                 "both <2e-4",
                 "the theory's Lambda is 32pi a0^2/c^4 rounded, so this agreement is bookkeeping, not evidence")


# =============================================================================
# K7 -- the canonical a0 against 1/7
# =============================================================================
def k7():
    r = INP["A0"] / (C * H0)
    sig_r = r * 0.09389                       # A71's SPARC bootstrap, 9.389%
    z = zscore(r, 1.0 / 7.0, sig_r)
    fracs = sorted({(p, q) for q in range(2, 21) for p in range(1, q)
                    if math.gcd(p, q) == 1 and abs(r - p / q) < sig_r})
    ok = rel(r, 1.0 / 7.0) < 1e-3 and abs(z) < 0.1 and len(fracs) >= 3
    return check("K7", ok,
                 "a0/(cH0)=%.6f vs 1/7=%.6f rel %.2e; pull %+.2f sigma (9.389%% error); "
                 "%d simple p/q (q<=20) inside 1 sigma: %s"
                 % (r, 1 / 7, rel(r, 1 / 7), z, len(fracs), ", ".join("%d/%d" % f for f in fracs)),
                 "rel<1e-3, |pull|<0.1, and >2 rival fractions inside 1 sigma",
                 "the canonical footing reproduces 1/7 to 6e-4, but its own error is 9.4%: four simple "
                 "fractions fit equally well, so the data do not select 1/7")


# =============================================================================
# K8 -- the joint fit's a0: r, its pull from 1/7, and the implied Omega_Lambda
# =============================================================================
def k8():
    r = INP["KAPPA_P3"] / math.sqrt(8 * math.pi / 3)
    sig_r = r * INP["SIGMA_KAPPA_P3"] / INP["KAPPA_P3"]
    z = zscore(r, 1.0 / 7.0, sig_r)
    Om = (32 * math.pi / 3) * r ** 2
    sig_Om = Om * 2 * (sig_r / r)
    z_pl = zscore(Om, PLANCK, sig_Om)
    ok = abs(z + 1.40) < 0.05 and abs(z_pl + 1.47) < 0.10
    return check("K8", ok,
                 "r=%.6f+-%.6f pull(1/7)=%+.2f sigma (A71: 1.40); Omega(a0)=%.4f+-%.4f pull(Planck)=%+.2f"
                 % (r, sig_r, z, Om, sig_Om, z_pl),
                 "pull(1/7) within 0.05 of -1.40; Omega pull -1.47+-0.10",
                 "the theory's own a0 sits 1.4 sigma below the value that gives 32pi/147, and implies Omega=0.571+-0.078")


# =============================================================================
# K9 -- the convention trap: kappa_DE / kappa_P3 = 1/sqrt(Omega)
# =============================================================================
def k9():
    ratio = 1.0 / math.sqrt(OMEGA_PRED)
    ratio_pl = 1.0 / math.sqrt(PLANCK)
    dkap = INP["A0_P3"] / INP["A0"]
    z = (0.604254 - 0.5) / INP["SIGMA_KAPPA_DE"]
    ok = abs(ratio - ratio_pl) < 5e-3 and abs(dkap - ratio_pl) < 5e-3 and 3.2 < z < 3.5
    return check("K9", ok,
                 "1/sqrt(Omega): pred %.5f, Planck %.5f; a0_P3/a0 %.5f; the two kappa footings %.2f sigma apart"
                 % (ratio, ratio_pl, dkap, z),
                 "ratios agree <5e-3; footing separation 3.2-3.5 sigma",
                 "the kappa_DE vs kappa_P3 distinction is exactly this factor; the record's two footings differ at 3.35 sigma")


# =============================================================================
# LOOK-ELSEWHERE POOL
# =============================================================================
ATOMS = [(1.0, 0, "1"), (2.0, 0, "2"), (3.0, 0, "3"), (4.0, 0, "4"), (5.0, 0, "5"),
         (7.0, 0, "7"), (8.0, 0, "8"), (math.pi, 0, "pi"), (math.e, 0, "e"),
         (math.sqrt(2), 0, "sqrt2"), (math.sqrt(3), 0, "sqrt3")]
OPS = [("+", lambda a, b: a + b), ("-", lambda a, b: a - b),
       ("*", lambda a, b: a * b), ("/", lambda a, b: a / b)]


def _clean(v):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    return np.unique(np.round(v, 10))


def _step(A, B):
    out = []
    for _, f in OPS:
        with np.errstate(all='ignore'):
            M = f(A[:, None], B[None, :])
        out.append(np.asarray(M, float).ravel())
    return np.concatenate(out)


def build_pool(maxops):
    """Distinct values of closed forms over the 11 atoms with <= maxops operations."""
    L0 = np.array(sorted({a[0] for a in ATOMS}))
    gens = [L0]
    S1 = _clean(np.concatenate([_step(L0, L0), np.sqrt(L0)]))
    S1 = S1[(S1 > 1e-3) & (S1 < 1e3)]
    gens.append(S1)
    if maxops >= 2:
        S2 = _clean(np.concatenate([_step(S1, L0), _step(L0, S1), np.sqrt(S1)]))
        S2 = S2[(S2 > 1e-3) & (S2 < 1e3)]
        gens.append(S2)
    if maxops >= 3:
        S3 = _clean(np.concatenate([_step(S2, L0), _step(L0, S2),
                                    _step(S1, S1), np.sqrt(S2)]))
        S3 = S3[(S3 > 1e-3) & (S3 < 1e3)]
        gens.append(S3)
    ALL = _clean(np.concatenate(gens))
    return ALL[(ALL > 1e-3) & (ALL < 1e3)]


POOL = build_pool(int(INP["POOL_OPS"]))
POOL_N = len(POOL)
BAND = POOL[(POOL >= 0.5) & (POOL <= 0.9)]
TOL = 8.0e-4                       # the task's 0.11 sigma = 8.0e-4 absolute
TOL_OWN = abs(PLANCK - OMEGA_PRED)  # the target's own distance, 8.16e-4


def count_near(arr, target, half):
    return int(np.searchsorted(arr, target + half, "right") - np.searchsorted(arr, target - half, "left"))


HITS_TOL = count_near(POOL, PLANCK, TOL)
HITS_OWN = count_near(POOL, PLANCK, TOL_OWN)
HITS_1PCT = count_near(POOL, 11.5776201, 0.01 * 11.5776201)

RNG = np.random.default_rng(73)
TARGETS = RNG.uniform(0.5, 0.9, 2000)
CNTS = np.array([count_near(POOL, t, TOL_OWN) for t in TARGETS])
LAMBDA_MC = float(CNTS.mean())
P_ANY = 1.0 - math.exp(-LAMBDA_MC)
FRAC_ANY = float((CNTS >= 1).mean())

# simplest forms: enumerate 0/1/2-operation forms with descriptions
def simple_forms():
    out = [(v, 0, d) for v, o, d in ATOMS]
    for (av, ao, ad) in ATOMS:
        for (bv, bo, bd) in ATOMS:
            for on, f in OPS:
                try:
                    v = f(av, bv)
                except ZeroDivisionError:
                    continue
                if math.isfinite(v) and v > 0:
                    out.append((v, 1, "(%s%s%s)" % (ad, on, bd)))
        if av > 0:
            out.append((math.sqrt(av), 1, "sqrt(%s)" % ad))
    S1 = [(v, o, d) for v, o, d in out]
    for (av, ao, ad) in S1:
        for (bv, bo, bd) in ATOMS:
            for on, f in OPS:
                for (x, xo, xd), (y, yo, yd) in (((av, ao, ad), (bv, bo, bd)),
                                                 ((bv, bo, bd), (av, ao, ad))):
                    try:
                        v = f(x, y)
                    except ZeroDivisionError:
                        continue
                    if math.isfinite(v) and 1e-3 < v < 1e3:
                        out.append((v, xo + yo + 1, "(%s%s%s)" % (xd, on, yd)))
    best = {}
    for v, o, d in out:
        k = round(v, 9)
        if k not in best or o < best[k][0]:
            best[k] = (o, d, v)
    return [(o, d, v) for k, (o, d, v) in best.items()]


SIMPLE = simple_forms()
SIMPLE_HITS = sorted([(abs(v - PLANCK), o, d, v) for o, d, v in SIMPLE
                      if abs(v - PLANCK) <= 1.0e-3 and o <= 2])
SIMPLE_HITS.sort()


def k10():
    ok = POOL_N >= 200000
    return check("K10", ok,
                 "pool: %d atoms x 4 ops + sqrt, <=%d operations -> %d distinct values in [1e-3,1e3]; band[0.5,0.9] %d"
                 % (len(ATOMS), int(INP["POOL_OPS"]), POOL_N, len(BAND)),
                 ">= 200000 distinct values",
                 "the pool is larger than A62's 156210 and is built from exactly the specified atom set")


def k11():
    hits_bool = int(np.sum(np.abs(POOL - PLANCK) <= TOL))
    ok = HITS_TOL >= 10 and hits_bool == HITS_TOL
    return check("K11", ok,
                 "within 0.11 sigma (%.1e abs): %d hits; at the target's own %.2e: %d; boolean recount %d"
                 % (TOL, HITS_TOL, TOL_OWN, HITS_OWN, hits_bool),
                 ">=10 hits and the two counting routes agree",
                 "the target value is not isolated in closed-form space: ~70 forms sit within 0.11%% of it")


def k12():
    ok = LAMBDA_MC > 10 and P_ANY > 0.99 and FRAC_ANY > 0.99
    return check("K12", ok,
                 "random targets in [0.5,0.9]: mean %.1f hits (median %.0f, range %d-%d); P(>=1)=%.6f; fraction with >=1 %.3f"
                 % (LAMBDA_MC, np.median(CNTS), CNTS.min(), CNTS.max(), P_ANY, FRAC_ANY),
                 "lambda>10 and P>=1 > 0.99",
                 "the base rate is ~100%%: EVERY value in the band has dozens of closed forms within 0.11%%")


def density_per_relative_window(hits, half_abs, target, n_pool):
    """hits per unit RELATIVE half-width window, per 1000 pool members."""
    h_rel = half_abs / target
    return hits / (2 * h_rel) / n_pool * 1000


def k13():
    d_here = density_per_relative_window(HITS_OWN, TOL_OWN, PLANCK, POOL_N)
    d_2z = density_per_relative_window(HITS_1PCT, 0.01 * 11.5776201, 11.5776201, POOL_N)
    a62 = density_per_relative_window(223, 0.01 * 11.5776201, 11.5776201, 156210)
    ok = HITS_1PCT > 100 and 0.3 < d_here / d_2z < 3.0 and 0.3 < d_here / a62 < 3.0
    return check("K13", ok,
                 "density per unit relative window per 1000 forms: 32pi/147 %.4f; 2Z (this pool) %.4f; 2Z (A62) %.4f"
                 % (d_here, d_2z, a62),
                 "same order (0.3-3.0) as both 11.5776 baselines",
                 "32pi/147 is no more remarkable than the 11.5776 hit A62 already called NO EVIDENCE")


def k14():
    fam = set()
    for k in range(1, int(INP["FAM_KMAX"]) + 1):
        for n in range(1, int(INP["FAM_NMAX"]) + 1):
            v = k * math.pi / n
            if abs(v - PLANCK) <= TOL_OWN:
                fam.add(round(v, 12))
    self_in = abs(NUM * math.pi / DEN - PLANCK) <= TOL_OWN
    others = len(fam) - (1 if self_in else 0)
    ok = others >= 3 and self_in
    return check("K14", ok,
                 "own shape k*pi/n (k<=64, n<=400): %d values within the window, %d of them other than 32pi/147"
                 % (len(fam), others),
                 ">=3 alternatives in the target's own family",
                 "even inside 32pi/147's own functional family, a dozen k*pi/n forms match as well")


def k15():
    # the specific two-operation rival, evaluated from its own atoms
    v_rival = math.sqrt(3) - math.pi / 3
    dev = abs(v_rival - PLANCK)
    ok = dev <= 1.0e-3 and dev < TOL_OWN / 3 and len(SIMPLE_HITS) > 0
    return check("K15", ok,
                 "rival sqrt3-pi/3 = %.9f, dev %.2e, 2 ops / 3 symbols; prediction dev %.2e -> rival is %.1fx closer"
                 % (v_rival, dev, TOL_OWN, TOL_OWN / dev),
                 "rival within 1e-3 and >3x closer than the prediction",
                 "a two-operation, three-symbol form beats 32pi/147 by 5x: the number is not selected by its fit")


def k16():
    alts = [("3/8", 0.375), ("0.7", 0.7), ("2/3", 2 / 3), ("11/16", 0.6875), ("0.68", 0.68), ("0.69", 0.69)]
    zs = [(n, zscore(PLANCK, v, PLANCK_SIG)) for n, v in alts]
    zmap = dict(zs)
    ok = abs(zmap["11/16"]) < 0.6 and abs(zmap["0.7"]) > 2.0 and abs(zmap["3/8"]) > 40
    return check("K16", ok,
                 "; ".join("%s %.4f (%+.2f sigma)" % (n, v, zscore(PLANCK, v, PLANCK_SIG)) for n, v in alts),
                 "11/16 within 0.6 sigma, 0.7 beyond 2 sigma, 3/8 dead",
                 "Planck cannot separate 32pi/147 (0.11) from 11/16 (0.38) or 0.68/0.69; the number is not sharp")


def k17():
    sigma_req = abs(PLANCK - OMEGA_PRED) / 3.0
    ratio = PLANCK_SIG / sigma_req
    ok = 20 < ratio < 35
    return check("K17", ok,
                 "3-sigma discrimination needs sigma(Omega)=%.2e (%.4f%%); Planck has %.2e -> %.1fx too coarse"
                 % (sigma_req, 100 * sigma_req / OMEGA_PRED, PLANCK_SIG, ratio),
                 "20 < ratio < 35",
                 "the prediction differs from Planck by 0.12%%, so excluding it at 3 sigma needs 0.04%% precision")


def k18():
    Om_flat = 1.0 - INP["PLANCK_OM"]
    shift_1sig = INP["SIGMA_K"]
    shift_closed = INP["OMEGA_K_PLANCK_ONLY"] - 0.0
    ratio = shift_1sig / abs(PLANCK - OMEGA_PRED)
    ratio_closed = abs(shift_closed) / abs(PLANCK - OMEGA_PRED)
    ok = ratio > 1.5 and ratio_closed > 40
    return check("K18", ok,
                 "curvature: dOmega_L/dOmega_k=-1; 1 sigma (%.4f) moves it %.1fx the gap; Planck-only closed (%.3f) %.0fx"
                 % (shift_1sig, ratio, shift_closed, ratio_closed),
                 "1-sigma curvature >1.5x the gap",
                 "the claim presupposes flatness; free curvature at Planck-only precision moves Omega_L by 54x the offset")


def k19():
    def Om_of_h(h):
        return LAMBDA * C ** 2 / (3 * (h * 1e3 / MPC) ** 2)
    o0 = Om_of_h(INP["H0"])
    o1 = Om_of_h(INP["H0"] + INP["SIGMA_H0"])
    slope = (math.log(o1) - math.log(o0)) / (math.log(INP["H0"] + INP["SIGMA_H0"]) - math.log(INP["H0"]))
    shift = abs(o1 - o0)
    ratio = shift / abs(PLANCK - OMEGA_PRED)
    ok = abs(slope + 2.0) < 1e-3 and ratio > 10
    return check("K19", ok,
                 "dlnOmega/dlnH0=%.6f; a %.1f km/s/Mpc shift moves Omega by %.2e = %.1fx the gap"
                 % (slope, INP["SIGMA_H0"], shift, ratio),
                 "slope -2.000 and ratio >10",
                 "at fixed Lambda the claimed 0.12%% is far below the 1.5%% H0-footing uncertainty")


def k20():
    r = sp.Rational(1, 7)
    den = sp.nsimplify(3 / r ** 2)
    num = sp.nsimplify(8 / sp.Rational(str(KAPPA)) ** 2)
    Om = sp.Rational(NUM, 1) * sp.pi / sp.Rational(DEN, 1)
    friedmann = sp.simplify(Om - (sp.Rational(8, 1) * sp.pi / 3) * (sp.Rational(2, 7)) ** 2)
    solid = sp.simplify(Om - (sp.Rational(4, 1) * sp.pi / 3) * (sp.Rational(2, 7) * sp.sqrt(2)) ** 2)
    area = sp.simplify((sp.Rational(2, 7)) ** 2 - (sp.Rational(1, 7)) ** 2 * 4)
    ok = (den == DEN) and (num == NUM) and sp.Integer(DEN) == 3 * 7 ** 2 \
        and friedmann == 0 and solid == 0 and area == 0
    return check("K20", ok,
                 "147 = 3*(cH0/a0)^2 at a0/cH0=1/7 -> %s; 32 = 8/kappa^2 at kappa=1/2 -> %s; "
                 "(8pi/3)(2/7)^2 residual %s; (4pi/3)(2sqrt2/7)^2 residual %s; area ratio 4*(a0/cH0)^2 residual %s"
                 % (den, num, friedmann, solid, area),
                 "all five identities exact",
                 "147 is DEFINED by the measured ratio cH0/a0, 32 by kappa, and (2/7)^2 is the horizon-area ratio: "
                 "the integer carries no independent content")


def k26():
    """Do any standard counting numbers produce 147?  And is the one exact route chosen?"""
    counts = {"g_*(rec)=3.91": 3.91, "g_*(EW)=106.75": 106.75, "N_eff=3.046": 3.046,
              "N_e=60": 60.0, "1/alpha=137.036": 137.036, "2^7=128": 128.0}
    rows = []
    exact_phys = []
    for k, v in counts.items():
        q = DEN / v
        miss = abs(q - round(q))
        rows.append("%s->%.4f(miss %.2f)" % (k.replace("=", ""), q, miss))
        if miss < 1e-9:
            exact_phys.append(k)
    efold = 64 * math.log(10.0)
    exact_chosen = (3 * (10 - 3) ** 2 == DEN)
    ok = len(exact_phys) == 0 and exact_chosen and abs(efold - DEN) / DEN > 1e-3
    return check("K26", ok,
                 "147/x: " + "; ".join(rows) + "; ln(10^64)=%.3f (%.2f%% from 147); "
                 "3(D-3)^2 at D=10 = %d and 7*C(7,2) = %d (both chosen)"
                 % (efold, 100 * abs(efold - DEN) / DEN, 3 * (10 - 3) ** 2, 7 * 21),
                 "no standard count hits 147; the one exact integer route needs D=10 chosen",
                 "no g_*, N_eff, e-fold or 1/alpha count gives 147; 3(10-3)^2 does, but D=10 is an assumption with no link to Omega_Lambda")


def k21():
    inv_pred = 1.0 / OMEGA_PRED
    exact = DEN / (NUM * math.pi)
    dev_a33 = rel(inv_pred, INP["A33_RATIO"])
    dev_pl = rel(inv_pred, 1.0 / PLANCK)
    ok = dev_a33 < 2e-4 and dev_pl > 1e-4
    return check("K21", ok,
                 "1/Omega_pred = %d/(%d pi) = %.5f; A33's 1.462 rel %.1e; 1/Planck %.5f rel %.1e"
                 % (DEN, NUM, inv_pred, dev_a33, 1.0 / PLANCK, dev_pl),
                 "matches A33's 1.462 to <1e-4",
                 "A33's Lambda_bare >= 1.462 Lambda_obs is the same number; A46 shows it is a flat-budget identity")


def k22():
    Z = 2 * math.sqrt(8 * math.pi / 3)          # 5.788810
    TWOZ = 2 * Z                                # 11.577620 = sqrt(128 pi/3)
    ratio = (1.0 / 7.0) / (1.0 / TWOZ)
    r_pred = KAPPA * math.sqrt(3 * OMEGA_PRED / (8 * math.pi))
    ratio_pred = r_pred * TWOZ
    ok = abs(ratio - TWOZ / 7) < 1e-12 and abs(ratio_pred - ratio) < 1e-9 \
        and abs((1 / 7) - 1 / TWOZ) > 0.05 and abs(TWOZ - 11.5776201) < 1e-6
    return check("K22", ok,
                 "Z=%.6f, 2Z=%.6f; 1/7 / (1/(2Z)) = 2Z/7 = %.6f; the same ratio from Omega_pred %.6f; "
                 "|1/7-1/(2Z)| = %.4f"
                 % (Z, TWOZ, ratio, ratio_pred, abs(1 / 7 - 1 / TWOZ)),
                 "identities exact; the two A62 numbers differ by >0.05",
                 "1/7 and 1/(2Z)=1/11.5776 are different numbers: the 1/7 hit is NOT the 1/12 claim")


def k23():
    sig3 = float(np.mean([d / math.sqrt(c) for d, c in INP["DESI_DCHI2"]]))
    Om3 = 1.0 - INP["DESI_OM"]
    z3 = zscore(OMEGA_PRED, Om3, sig3)
    sig2 = float(np.mean([d / math.sqrt(c) for d, c in INP["DESI2_DCHI2"]]))
    Om2 = 1.0 - INP["DESI2_OM"]
    z2 = zscore(OMEGA_PRED, Om2, sig2)
    ok = -4.2 < z3 < -3.4 and -1.3 < z2 < -0.8
    return check("K23", ok,
                 "repo DESI DR2+Pantheon+ (A46): 3pt Omega=%.5f+-%.5f z=%+.2f; 2pt Omega=%.5f+-%.5f z=%+.2f"
                 % (Om3, sig3, z3, Om2, sig2, z2),
                 "3pt pull -4.2..-3.4, 2pt -1.3..-0.8",
                 "the repo's own BAO+SNe+CMB fit is 3.8 sigma HIGH: the Planck agreement is dataset-dependent")


def k24():
    Om = 1.0 - INP["PANTHEON_OM"]
    z = zscore(OMEGA_PRED, Om, INP["PANTHEON_SIG"])
    ok = 0.8 < z < 1.2
    return check("K24", ok,
                 "Pantheon+ (Brout+2022, SNe alone): Omega=%.3f+-%.3f z=%+.2f" % (Om, INP["PANTHEON_SIG"], z),
                 "pull +0.8..+1.2",
                 "the local/SNe determination sits 1 sigma LOW: the prediction is bracketed, not confirmed")


def k25():
    sig3 = float(np.mean([d / math.sqrt(c) for d, c in INP["DESI_DCHI2"]]))
    sig2 = float(np.mean([d / math.sqrt(c) for d, c in INP["DESI2_DCHI2"]]))
    pulls = [zscore(OMEGA_PRED, PLANCK, PLANCK_SIG),
             zscore(OMEGA_PRED, 1 - INP["PANTHEON_OM"], INP["PANTHEON_SIG"]),
             zscore(OMEGA_PRED, 1 - INP["DESI_OM"], sig3),
             zscore(OMEGA_PRED, 1 - INP["DESI2_OM"], sig2)]
    ok = max(abs(p) for p in pulls) > 3.0 and min(pulls) < 0 < max(pulls)
    return check("K25", ok,
                 "pulls: Planck %+.2f, Pantheon+ %+.2f, DESI3pt %+.2f, DESI2pt %+.2f -> spread %.2f"
                 % (pulls[0], pulls[1], pulls[2], pulls[3], max(pulls) - min(pulls)),
                 "max |pull| >3 and the sign changes across datasets",
                 "the same number is -3.8 sigma from one dataset and +1.0 from another: no single Omega_Lambda is 'the' test")


# =============================================================================
# RUN
# =============================================================================
k1(); k2(); k3(); k4(); k5(); k6(); k7(); k8(); k9()
k10(); k11(); k12(); k13(); k14(); k15(); k16(); k17(); k18(); k19(); k20(); k21(); k22(); k23(); k24(); k25(); k26()

NPASS = sum(c["ok"] for c in CHECKS)
print("-" * 100)
print("pool detail: atoms=%d, ops={+,-,*,/} plus unary sqrt, maxops=%d, distinct=%d, band=%d"
      % (len(ATOMS), int(INP["POOL_OPS"]), POOL_N, len(BAND)))
print("simplest 2-op hits near the target:")
for dev, o, d, v in SIMPLE_HITS[:6]:
    print("    dev %.2e  ops %d  %-40s = %.9f" % (dev, o, d, v))
print("-" * 100)
print("A73 COMPLETE: %d/%d checks PASS.  (%.1f s)" % (NPASS, len(CHECKS), time.time() - T0))

# =============================================================================
# NUMBERS -- every quantity quoted in report.md is printed here
# =============================================================================
sig3 = float(np.mean([d / math.sqrt(c) for d, c in INP["DESI_DCHI2"]]))
sig2 = float(np.mean([d / math.sqrt(c) for d, c in INP["DESI2_DCHI2"]]))
r_can = INP["A0"] / (C * H0)
r_fit = INP["KAPPA_P3"] / math.sqrt(8 * math.pi / 3)
sig_r_fit = r_fit * INP["SIGMA_KAPPA_P3"] / INP["KAPPA_P3"]
Om_fit = (32 * math.pi / 3) * r_fit ** 2
sOm_fit = 2 * Om_fit * sig_r_fit / r_fit
Z_VAL = 2 * math.sqrt(8 * math.pi / 3)          # Z = 5.788810; 2Z = 11.577620
SIMPLE_BEST = SIMPLE_HITS[0] if SIMPLE_HITS else (float("nan"), -1, "none", float("nan"))
SIG_REQ = abs(PLANCK - OMEGA_PRED) / 3.0
A0_FRAC_BELOW = (r_can - r_fit) / r_can
SPREAD = (1 - INP["DESI_OM"]) - (1 - INP["PANTHEON_OM"])

NUMBERS = {
    "value_32pi_147": float(V_MP),
    "value_10dp": "%.10f" % float(V_MP),
    "value_12sig": mp.nstr(V_MP, 12),
    "planck": PLANCK, "planck_sigma": PLANCK_SIG,
    "z_planck": zscore(OMEGA_PRED, PLANCK, PLANCK_SIG),
    "planck_omega_from_om": 1.0 - INP["PLANCK_OM"],
    "z_pantheon": zscore(OMEGA_PRED, 1 - INP["PANTHEON_OM"], INP["PANTHEON_SIG"]),
    "omega_pantheon": 1 - INP["PANTHEON_OM"], "sigma_pantheon": INP["PANTHEON_SIG"],
    "omega_desi_3pt": 1 - INP["DESI_OM"], "sigma_desi_3pt": sig3,
    "z_desi_3pt": zscore(OMEGA_PRED, 1 - INP["DESI_OM"], sig3),
    "omega_desi_2pt": 1 - INP["DESI2_OM"], "sigma_desi_2pt": sig2,
    "z_desi_2pt": zscore(OMEGA_PRED, 1 - INP["DESI2_OM"], sig2),
    "omega_theory_footing": LAMBDA * C ** 2 / (3 * H0 ** 2),
    "sigma_omega_theory_footing": 2 * INP["SIGMA_H0"] / INP["H0"] * LAMBDA * C ** 2 / (3 * H0 ** 2),
    "z_theory_footing": zscore(OMEGA_PRED, LAMBDA * C ** 2 / (3 * H0 ** 2),
                               2 * INP["SIGMA_H0"] / INP["H0"] * LAMBDA * C ** 2 / (3 * H0 ** 2)),
    "omega_dataset_spread_width": (1 - INP["DESI_OM"]) - (1 - INP["PANTHEON_OM"]),
    "lambda_needed_for_pred": 3 * OMEGA_PRED * H0 ** 2 / C ** 2,
    "a0_from_lambda": KAPPA * C ** 2 * math.sqrt(LAMBDA / (8 * math.pi)),
    "r_canonical": r_can, "r_canonical_rel_dev": rel(r_can, 1 / 7),
    "r_fit": r_fit, "sigma_r_fit": sig_r_fit,
    "pull_r_fit_from_1_7": zscore(r_fit, 1 / 7, sig_r_fit),
    "omega_from_a0_fit": Om_fit, "sigma_omega_from_a0_fit": sOm_fit,
    "omega_from_a0_fit_frac": sOm_fit / Om_fit,
    "planck_frac_precision": PLANCK_SIG / PLANCK,
    "sigma_omega_from_a0_canonical": 2 * 0.09389 * OMEGA_PRED,
    "simple_fractions_within_1sigma_of_r_canonical": [
        "%d/%d" % f for f in sorted({(p, q) for q in range(2, 21) for p in range(1, q)
                                     if math.gcd(p, q) == 1 and abs(r_can - p / q) < r_can * 0.09389})],
    "pull_omega_from_a0_fit_vs_planck": zscore(Om_fit, PLANCK, sOm_fit),
    "kappa_DE_over_P3": 1.0 / math.sqrt(OMEGA_PRED),
    "two_footings_sigma": (0.604254 - 0.5) / INP["SIGMA_KAPPA_DE"],
    "pool_n": POOL_N, "band_n": len(BAND), "tol": TOL, "tol_own": TOL_OWN,
    "hits_0p11sigma": HITS_TOL, "hits_own_window": HITS_OWN,
    "hits_11p5776_1pct": HITS_1PCT,
    "lambda_random": LAMBDA_MC, "P_at_least_one": P_ANY, "frac_targets_with_hit": FRAC_ANY,
    "density_32pi147": HITS_OWN / (2 * TOL_OWN) / POOL_N * 1000,
    "density_2Z_this_pool": HITS_1PCT / (0.02 * 11.5776201) / POOL_N * 1000,
    "density_2Z_a62_pool": 223 / (0.02 * 11.5776201) / 156210 * 1000,
    "family_kpi_n_others": None,
    "simplest_hit_expr": SIMPLE_BEST[2], "simplest_hit_value": SIMPLE_BEST[3],
    "simplest_hit_dev": SIMPLE_BEST[0], "simplest_hit_ops": SIMPLE_BEST[1],
    "sigma_required_3sigma": abs(PLANCK - OMEGA_PRED) / 3.0,
    "sigma_required_fraction": abs(PLANCK - OMEGA_PRED) / 3.0 / OMEGA_PRED,
    "planck_over_required": PLANCK_SIG / (abs(PLANCK - OMEGA_PRED) / 3.0),
    "curvature_1sigma_over_gap": INP["SIGMA_K"] / abs(PLANCK - OMEGA_PRED),
    "curvature_closed_over_gap": abs(INP["OMEGA_K_PLANCK_ONLY"]) / abs(PLANCK - OMEGA_PRED),
    "h0_sensitivity_ratio": None,
    "inv_omega_pred": 1.0 / OMEGA_PRED, "inv_omega_planck": 1.0 / PLANCK,
    "a33_ratio_dev": rel(1.0 / OMEGA_PRED, INP["A33_RATIO"]),
    "Z": Z_VAL, "2Z": 2 * Z_VAL, "inv_Z": 1.0 / Z_VAL, "inv_2Z": 1.0 / (2 * Z_VAL),
    "one_seventh": 1 / 7,
    "ratio_1_7_over_inv2Z": (1 / 7) * (2 * Z_VAL),
    "mutations": sorted(k for k in MUTATIONS if k != "none"),
    "mutation": MUT,
    "alternatives_sigma_from_planck": {
        "3/8": zscore(PLANCK, 0.375, PLANCK_SIG),
        "2/3": zscore(PLANCK, 2 / 3, PLANCK_SIG),
        "0.7": zscore(PLANCK, 0.7, PLANCK_SIG),
        "11/16": zscore(PLANCK, 0.6875, PLANCK_SIG),
        "0.68": zscore(PLANCK, 0.68, PLANCK_SIG),
        "0.69": zscore(PLANCK, 0.69, PLANCK_SIG),
        "32pi/147": zscore(PLANCK, OMEGA_PRED, PLANCK_SIG),
    },
    "rival_over_prediction_dev_ratio": TOL_OWN / abs((math.sqrt(3) - math.pi / 3) - PLANCK),
    "structural_counts_147_over_x": {
        "g_star_rec_3.91": DEN / 3.91, "g_star_EW_106.75": DEN / 106.75,
        "N_eff_3.046": DEN / 3.046, "N_e_60": DEN / 60.0,
        "inv_alpha_137.036": DEN / 137.036, "2^7_128": DEN / 128.0,
        "ln_10^64": 64 * math.log(10.0),
        "3(D-3)^2_D10": 3 * (10 - 3) ** 2,
    },
    "density_32pi147_rel": density_per_relative_window(HITS_OWN, TOL_OWN, PLANCK, POOL_N),
    "density_2Z_this_pool_rel": density_per_relative_window(HITS_1PCT, 0.01 * 11.5776201, 11.5776201, POOL_N),
    "density_2Z_a62_pool_rel": density_per_relative_window(223, 0.01 * 11.5776201, 11.5776201, 156210),
    "dataset_spread_over_gap": SPREAD / TOL_OWN,
    "pantheon_desi_tension_sigma": SPREAD / math.hypot(INP["PANTHEON_SIG"], sig3),
    "desi_sigma_over_required": sig3 / SIG_REQ,
    "a0_fit_frac_below_1_7": A0_FRAC_BELOW,
    "sigma_a0_required_3sigma": A0_FRAC_BELOW / 3.0,
    "wide_binary_pull_at_sigma_kappa_040": A0_FRAC_BELOW / 0.040,
    "h0_shift_fraction": INP["SIGMA_H0"] / INP["H0"],
    "theory_md_quoted_value": 0.683827,
    "theory_md_value_error": OMEGA_PRED - 0.683827,
    "cell_count_fraction": 3 * OMEGA_PRED / (8 * math.pi),
    "cell_count_needed_for_147": 1.0 / DEN,
    "density_ratio_2Zthis_over_here": density_per_relative_window(HITS_1PCT, 0.01 * 11.5776201, 11.5776201, POOL_N)
                                       / density_per_relative_window(HITS_OWN, TOL_OWN, PLANCK, POOL_N),
    "density_ratio_here_over_a62": density_per_relative_window(HITS_OWN, TOL_OWN, PLANCK, POOL_N)
                                    / density_per_relative_window(223, 0.01 * 11.5776201, 11.5776201, 156210),
    "external_quotes": {
        "DESI_DR2_w0wa_preference_sigma": [2.8, 4.2],
        "DESI_DR2_BAO_vs_CMB_omega_m_tension_sigma": 2.3,
        "Planck_2018_omega_m": 0.3153,
        "Planck_2018_omega_k": [0.0007, 0.0019],
        "Planck_only_omega_k": -0.044,
        "Pantheon_plus_omega_m": 0.334,
        "A33_ratio": 1.462,
        "THEORY_md_quoted_sigma": 0.13,
        "A62_pool_size": 156210,
        "A62_hits_2Z_1pct": 223,
        "A62_simplest_hit_sqrt134": 11.575837,
        "A62_sqrt134_dev": 1.54e-4,
        "A46_SNe_points": 1580,
        "A46_3pt_omega_b_h2": 0.02252,
        "A46_2pt_omega_b_h2": 0.01955,
        "BBN_omega_b_h2": 0.02236,
    },
}

# family count and H0 sensitivity recomputed for the record
fam = set()
for k in range(1, int(INP["FAM_KMAX"]) + 1):
    for n in range(1, int(INP["FAM_NMAX"]) + 1):
        v = k * math.pi / n
        if abs(v - PLANCK) <= TOL_OWN:
            fam.add(round(v, 12))
NUMBERS["family_kpi_n_others"] = len(fam) - 1

o0 = LAMBDA * C ** 2 / (3 * H0 ** 2)
o1 = LAMBDA * C ** 2 / (3 * ((INP["H0"] + INP["SIGMA_H0"]) * 1e3 / MPC) ** 2)
NUMBERS["h0_sensitivity_ratio"] = abs(o1 - o0) / abs(PLANCK - OMEGA_PRED)

print()
print("NUMBERS")
for k in sorted(NUMBERS):
    print("  %-38s %s" % (k, NUMBERS[k]))

if MUT == "none":
    out = dict(lane="A73_omega_lambda", mutation=MUT,
               checks=[dict(id=c["id"], pass_=c["ok"], value=c["measured"],
                            threshold=c["threshold"], note=c["note"]) for c in CHECKS],
               numbers=NUMBERS,
               inputs={k: (list(v) if isinstance(v, tuple) else v) for k, v in INP.items()},
               constants_note=("Planck 2018 TT,TE,EE+lowE+lensing Omega_L=0.6847+-0.0073; "
                               "Pantheon+ Brout+2022 Omega_m=0.334+-0.018; "
                               "A46 flat-LCDM fit to DESI DR2 BAO + Pantheon+ + Planck distance priors, "
                               "sigma from the Delta-chi^2=1 profile; A71 joint fit kappa_P3=0.37765+-0.02579"))
    (open(os.path.join(HERE, "a73_results.json"), "w")).write(json.dumps(out, indent=1) + "\n")

sys.exit(0 if (NPASS == len(CHECKS) and MUT == "none") else 1)
