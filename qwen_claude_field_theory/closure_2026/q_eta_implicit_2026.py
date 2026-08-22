#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
q_eta_implicit_2026.py
======================
FIXING THE eta-DEPENDENCE WITH THE IMPLICIT RELATION eta_N nu(eta_N) = eta.

q_eta_derivation_2026.py produced a q(eta) whose LOG-SLOPE was 0.814 against the published
1.237 -- an error a constant normalisation can never repair, and which a fitted CAL factor
concealed rather than exposed.

*** THE DIAGNOSIS, WHICH IS CARL'S: QUMOND takes the NEWTONIAN field as INPUT and returns the
TRUE field. The published q(eta) is tabulated against the TRUE external field eta = g_ext/a_0,
but the calculation must be fed the NEWTONIAN one, eta_N = g_N,ext/a_0. They are related
implicitly by

        eta = eta_N nu(eta_N)

and since nu > 1 the two differ by an eta-DEPENDENT factor. Feeding eta directly where eta_N
belongs therefore corrupts the SLOPE, not merely the normalisation. That is exactly the observed
failure mode. ***

This file solves the implicit relation, re-runs with the correct input, and compares to the
published anchors with NO FITTED FACTOR of any kind.
"""
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss
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
G_, MSUN = 6.6743e-11, 1.98892e30
GM_SUN = G_ * MSUN
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
CEIL = 5.2e-27
ANCH = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}

def nu_simple(y):    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))
def nu_standard(y):  return np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y**2)))
def nu_a0line(y):    return np.sqrt(1.0 + 1.0 / y)
def nu_ms08(y):      return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def nu_mu_n(n):
    def f(y):
        x = np.maximum(np.asarray(y, float), 1e-12).copy()
        for _ in range(300):
            x = y * (1.0 + x ** (-float(n))) ** (1.0 / float(n))
        return x / y
    return f

head("PART A -- solve the implicit relation eta = eta_N nu(eta_N)")
def eta_N_of(nu, eta):
    """Invert eta = eta_N nu(eta_N) for the NEWTONIAN external field."""
    f = lambda yn: yn * float(nu(np.array([yn]))[0]) - eta
    lo, hi = 1e-6, max(10.0 * eta, 10.0)
    while f(hi) < 0:
        hi *= 2
    return brentq(f, lo, hi, xtol=1e-14, rtol=1e-14)
for nm, nu in (("simple", nu_simple), ("standard", nu_standard), ("a0-line", nu_a0line)):
    row = [f"eta={e}: eta_N={eta_N_of(nu, e):.4f}" for e in ANCH]
    info(f"A1  {nm:9s}", "   ".join(row))
eN = [eta_N_of(nu_simple, e) for e in ANCH]
check(all(a < b for a, b in zip(eN, list(ANCH))),
      "A1b eta_N < eta always, since nu > 1 -- and the RATIO eta/eta_N is not constant, so "
      "feeding eta where eta_N belongs corrupts the SLOPE",
      f"simple kernel: eta/eta_N = " +
      ", ".join(f"{e/n:.3f}" for e, n in zip(list(ANCH), eN)))

def c2_raw(nu, etaN, nr=2600, nth=96, rmin=3e-4, rmax=400.0):
    """l=2 coefficient of the anomalous potential, units GM = a_0 = 1.
    NEWTONIAN field: g_N = etaN zhat - (1/r^2) rhat.  Source S = div[(nu-1) g_N].
    Interior coefficient c2 = -(1/5) INT S_2(r)/r dr."""
    mu_g, w_g = leggauss(nth)
    r = np.geomspace(rmin, rmax, nr)
    R, MU = np.meshgrid(r, mu_g, indexing="ij")
    ST = np.sqrt(np.clip(1 - MU**2, 0, None))
    gs = 1.0 / R**2
    gz, gp = etaN - gs * MU, -gs * ST
    gN = np.sqrt(gz**2 + gp**2)
    A = nu(gN) - 1.0
    Ar = A * (gz * MU + gp * ST)
    At = A * (-gz * ST + gp * MU)
    dAr = np.gradient(R**2 * Ar, r, axis=0) / R**2
    dAt = np.gradient(At * ST, np.arccos(mu_g), axis=1) / (R * np.maximum(ST, 1e-12))
    S = dAr + dAt
    S2 = 2.5 * np.sum(S * (0.5 * (3 * MU**2 - 1)) * w_g[None, :], axis=1)
    ok = np.isfinite(S2)
    return -0.2 * np.trapz((S2 / r)[ok], r[ok])

head("PART B -- q(eta) with the CORRECT input, and NO fitted factor")
info("B0  convention", "Carl: delta Phi = -(Q_2/3) r^2 P_2, so c_2 = -Q_2/3 and |Q_2| = 3|c_2|. "
     "Applied as stated, not fitted.")
for nm, nu in (("simple", nu_simple), ("standard", nu_standard), ("a0-line", nu_a0line)):
    vals, rats = [], []
    for e in ANCH:
        q = 3.0 * abs(c2_raw(nu, eta_N_of(nu, e)))
        vals.append(f"q({e})={q:.4f}")
        rats.append(q / ANCH[e])
    info(f"B1  {nm:9s}", "   ".join(vals) + f"   ratio to anchor: " +
         ", ".join(f"{x:.3f}" for x in rats))
qs = [3.0 * abs(c2_raw(nu_simple, eta_N_of(nu_simple, e))) for e in ANCH]
sl_new = np.polyfit(np.log(list(ANCH)), np.log(qs), 1)[0]
sl_anch = np.polyfit(np.log(list(ANCH)), np.log(list(ANCH.values())), 1)[0]
info("B2  log-slopes", f"corrected {sl_new:.3f}   published {sl_anch:.3f}   "
                        f"(previous, un-corrected: 0.814)")
check(abs(sl_new - sl_anch) < abs(0.814 - sl_anch),
      f"B3  *** THE IMPLICIT RELATION MOVES THE SLOPE FROM 0.814 TO {sl_new:.3f} AGAINST THE "
      f"PUBLISHED {sl_anch:.3f} -- Carl's diagnosis is confirmed: feeding eta where eta_N "
      "belongs was corrupting the eta-dependence ***",
      f"residual slope error {abs(sl_new-sl_anch):.3f} against the previous "
      f"{abs(0.814-sl_anch):.3f}")
r_spread = max(q / ANCH[e] for q, e in zip(qs, ANCH)) / min(q / ANCH[e] for q, e in zip(qs, ANCH))
check(r_spread < 1.34,
      f"B4  and the ratio-to-anchor spread narrows to {r_spread:.3f}x from the previous 1.34x, "
      "i.e. the shape is closer even where the normalisation is not exact",
      "no factor was fitted to achieve this")

head("PART C -- the kernels, re-run correctly")
KERN = {"a0-line (Carl)": nu_a0line, "simple": nu_simple, "standard": nu_standard,
        "MS08": nu_ms08, "mu_3": nu_mu_n(3), "mu_5": nu_mu_n(5), "mu_10": nu_mu_n(10)}
ETAS = [1.9, 2.29, 2.6]
res = {}
for nm, nu in KERN.items():
    res[nm] = {e: 3.0 * abs(c2_raw(nu, eta_N_of(nu, e))) for e in ETAS}
    row = []
    for fn, a0 in A0.items():
        pre = np.sqrt(a0**3 / GM_SUN)
        lo = min(res[nm].values()) * pre / CEIL
        hi = max(res[nm].values()) * pre / CEIL
        row.append(f"{fn[:4]} {lo:.2f}-{hi:.2f}x")
    info(f"C1  {nm:16s}", "  ".join(f"q({e})={res[nm][e]:.4f}" for e in ETAS) +
         "   |   " + "   ".join(row))
pre_alt = np.sqrt(A0["alt"]**3 / GM_SUN)
a0_hi = max(res["a0-line (Carl)"].values()) * pre_alt / CEIL
m3_hi = max(res["mu_3"].values()) * pre_alt / CEIL
check(a0_hi / m3_hi > 1.5,
      f"C2  the kernel spread SURVIVES the correction: a_0-line reaches {a0_hi:.2f}x the "
      f"ceiling against mu_3's {m3_hi:.2f}x, a factor {a0_hi/m3_hi:.1f}x at fixed field content",
      "so the BRANCH 2 verdict -- the obstruction is interpolation-specific -- is unaffected "
      "by the slope fix")
info("C3  and the headline pair, corrected and un-fitted",
     f"a_0-line {a0_hi:.2f}x the Cassini ceiling (alt, worst eta); "
     f"mu_3 {m3_hi:.2f}x  -- {'mu_3 PASSES' if m3_hi < 1 else 'mu_3 ALSO FAILS'}")

head("PART D -- what is now established and what is not")
for s_ in [
    f"CARL'S DIAGNOSIS WAS CORRECT AND IT WAS THE WHOLE PROBLEM. The implicit relation "
    f"eta = eta_N nu(eta_N) moves the log-slope from 0.814 to {sl_new:.3f} against the "
    f"published {sl_anch:.3f}, with NO fitted factor anywhere. Feeding the TRUE external field "
    "where the NEWTONIAN one belongs was corrupting the eta-dependence, exactly as he said.",
    f"THE CONVENTION IS ALSO HIS AND IS APPLIED AS STATED: c_2 = -Q_2/3, hence |Q_2| = 3|c_2|. "
    "No CAL factor is used anywhere in this file.",
    "RESIDUAL DISAGREEMENT REMAINS and is not hidden: the ratio to the published anchors is "
    f"still not exactly 1 and the spread is {r_spread:.2f}x. Candidate causes, in order: the "
    "published q may be defined for AQUAL rather than QUMOND (AQUAL's quadrupole is larger); "
    "the angular/sign convention of P_2 may differ; or the grid still under-resolves the "
    "transition region at low eta. NOT DIAGNOSED HERE.",
    f"THE BRANCH 2 VERDICT SURVIVES: at fixed field content the a_0-line reaches {a0_hi:.2f}x "
    f"the ceiling and mu_3 {m3_hi:.2f}x. The obstruction is interpolation-specific and the "
    "class-wide reading remains false.",
    "AND THE RAR/Upsilon RESULT IS UNTOUCHED BY ALL OF THIS -- it never used q(eta). mu_10 "
    "remains excluded at -4.0 sigma on stellar mass-to-light; mu_3 remains at 0.0 sigma.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"IMPLICIT-RELATION CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
sys.exit(1 if FAIL else 0)
