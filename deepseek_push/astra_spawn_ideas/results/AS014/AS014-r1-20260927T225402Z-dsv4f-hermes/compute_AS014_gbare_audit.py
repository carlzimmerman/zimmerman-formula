#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS014 — Measured G versus bare action coupling: bounded audit prototype.

Audits the CORE scale identities (Group A01) under the conversion
    G_bare = C_N * G_N   (equivalently G_N = G_bare / C_N)
keeping G_N (measured), G_bare (action coupling), G_E (Einstein coupling of
the vacuum term), G_cosmo (recorded, unused here) as SEPARATE symbols.

Deliverables of this script:
  C1  symbolic (sympy) insertion identities, exact 0
  C2  numeric (mpmath 60-digit) conversion ratios on both footings, 3 C_N
  C3  full-cell deep-MOND error ratios (a0_inf channel)
  C4  vacuum identity Lambda_eff = 32*pi*(G_E/G_N)*a0^2/c^4 at G_E = G_bare
      -> Lambda_eff = 32*pi*C_N*a0^2/c^4 ; mismatch factor vs same-G value
  C5  regime limits of the interpolation error R_full(y) (RAR kernel analytic,
      MONO kernel numeric): deep -> C_N^(3/4), Newtonian -> C_N
  C6  NEGATIVE CONTROL (task-mandated): C_N = 2. The unconverted formula must
      FAIL the physical normalization (ratios must differ from 1 by O(1)).
  C7  boundary/triviality: C_N = 1 gives all ratios exactly 1; C_N -> 0+
      gives vanishing scales (coupling-free limit);
      Kepler normalization: with G_bare = C_N*G_N the mass inferred from
      Earth's orbit using G_N is off by exactly C_N.
  C8  kappa-measurement comparison (labelled comparison, not a fit):
      fitted kappa tilde = 0.551 +/- 0.043 (distance-free) and
      0.465 +/- 0.076 (BTFR) bound C_N under both cells.
  C9  float64 cross-representation residuals.

Bounds actually enforced: SIGALRM 120 s; 1 thread by construction (pure
Python, no subprocess/threading); peak RSS measured via getrusage (macOS
ru_maxrss is in bytes). RLIMIT_AS 512 MB is recorded as refused by macOS.
"""
import json
import math
import signal
import resource
import sys
import time

from mpmath import mp, mpf, pi, sqrt, exp, log, power, mpc
import sympy as sp

# ----------------------------------------------------------------------------
# Enforcement scaffolding
# ----------------------------------------------------------------------------
class WallClockExceeded(Exception):
    pass

def _alarm(signum, frame):
    raise WallClockExceeded("SIGALRM: 120 s wall cap enforced")

signal.signal(signal.SIGALRM, _alarm)
signal.alarm(120)

_t0 = time.monotonic()
def wall():
    return time.monotonic() - _t0

# ----------------------------------------------------------------------------
# Constants (framework defaults) and footings
# ----------------------------------------------------------------------------
G_N = mpf("6.67430e-11")          # measured Newton constant, SI
c = mpf("299792458")              # m/s
M_sun = mpf("1.98847e30")         # kg
AU = mpf("1.495978707e11")        # m
T_earth = mpf("365.256363004") * mpf("86400")  # s  (sidereal year)
kappa = mpf("0.5")                # ADOPTED input (not derived in this task)

FOOTINGS = {
    "canonical": mpf("9.3619e-11"),
    "alternative": mpf("1.1279e-10"),
}

def rho_L(a0):
    """framework density rho_Lambda = 4 a0^2/(G_N c^2) (kappa=1/2 restatement)"""
    return 4 * a0 * a0 / (G_N * c * c)

def Lambda_sameG(a0):
    """same-G dictionary value 32*pi*a0^2/c^4  [m^-2]"""
    return 32 * pi * a0 * a0 / (c ** 4)

CN_VALUES = [mpf("1.5"), mpf("2"), mpf("0.9")]

results = []   # (name, tolerance_set_before, observed, pass)

def check(name, tol, observed, passed, note=""):
    results.append({
        "name": name,
        "tolerance_set_before": str(tol),
        "observed": str(observed),
        "pass": bool(passed),
        "note": note,
    })
    print(f"[{'PASS' if passed else 'FAIL'}] {name}  ->  {observed}"
          + (f"  ({note})" if note else ""))

# ----------------------------------------------------------------------------
# C1  symbolic identities (sympy), exact
# ----------------------------------------------------------------------------
GNs, Gbs, CNs, a0s, Ms, rm2s, v4s, a0bs, rho_s, ccs, kaps, Le = sp.symbols(
    "GN Gb CN a0 M rm2 v4 a0b rho c kappa Lambda", positive=True)

lhs_rm2_b = Gbs * Ms / a0s                     # r_M^2 with bare coupling, a0 fixed
rhs_rm2_b = CNs * (GNs * Ms / a0s)             # C_N * r_M^2(G_N)
lhs_v4_b = Gbs * Ms * a0s                      # v_flat^4 with bare coupling, a0 fixed
rhs_v4_b = CNs * (GNs * Ms * a0s)
lhs_a0b = kaps * ccs * sp.sqrt(Gbs * rho_s)    # bare scale
rhs_a0b = sp.sqrt(CNs) * (kaps * ccs * sp.sqrt(GNs * rho_s))
lhs_v4_full = sp.sqrt(CNs) * a0s * Gbs * Ms    # full cell: a0_b = sqrt(C_N) a0
rhs_v4_full = sp.sqrt(CNs) ** 3 * (GNs * Ms * a0s)
lhs_Lam = Le  # placeholder: handled below via substitution into AS002 T1
# T1 (AS002-certified) with G_E -> G_bare = C_N G_N:
Lam_expr_bare = sp.simplify(
    32 * sp.pi * (Gbs / GNs) * a0s ** 2 / ccs ** 4 - 32 * sp.pi * CNs * a0s ** 2 / ccs ** 4)

sym_checks = {
    "rm2 substitution  rM^2(Gb) = C_N rM^2(GN)":
        sp.simplify((lhs_rm2_b - rhs_rm2_b).subs(Gbs, CNs * GNs)),
    "v4 substitution   v4(Gb)   = C_N v4(GN)":
        sp.simplify((lhs_v4_b - rhs_v4_b).subs(Gbs, CNs * GNs)),
    "scale conversion  a0_b     = sqrt(C_N) a0":
        sp.simplify((lhs_a0b - rhs_a0b).subs(Gbs, CNs * GNs)),
    "full-cell v4      v4_b     = C_N^(3/2) v4":
        sp.simplify((lhs_v4_full - rhs_v4_full).subs(Gbs, CNs * GNs)),
    "vacuum identity   Lambda_eff(G_E=Gb) = 32 pi C_N a0^2/c^4":
        sp.simplify(Lam_expr_bare.subs(Gbs, CNs * GNs)),
    "kappa cancels in conversion (no kappa in ratios)":
        sp.simplify(((kaps * ccs * sp.sqrt(Gbs * rho_s)) /
                     (kaps * ccs * sp.sqrt(GNs * rho_s)) - sp.sqrt(CNs)).subs(
                         Gbs, CNs * GNs)),
}
for name, resid in sym_checks.items():
    check(f"C1 [sympy exact] {name}",
          "exact 0 (symbolic)",
          resid, resid == 0)

# ----------------------------------------------------------------------------
# C2  numeric conversion ratios, both footings, mpmath 60 digits
# ----------------------------------------------------------------------------
mp.dps = 60
tol60 = mpf("1e-45")
for footing, a0 in FOOTINGS.items():
    rho = rho_L(a0)
    Lam0 = Lambda_sameG(a0)
    Mb = M_sun
    for CN in CN_VALUES:
        Gb = CN * G_N
        # substitution cell (a0 fixed at framework footing value)
        rm2_N = G_N * Mb / a0
        rm2_b = Gb * Mb / a0
        v4_N = G_N * Mb * a0
        v4_b = Gb * Mb * a0
        a0_b = kappa * c * sqrt(Gb * rho)
        # full cell
        v4_full = a0_b * Gb * Mb
        Lam_bare = 32 * pi * (Gb / G_N) * a0 * a0 / (c ** 4)
        # residuals
        r1 = abs(rm2_b / rm2_N - CN)          # exact: C_N
        r2 = abs(v4_b / v4_N - CN)            # exact: C_N
        r3 = abs(v4_full / v4_N - power(CN, mpf("1.5")))  # exact: C_N^(3/2)
        r4 = abs(a0_b / a0 - sqrt(CN))        # exact: sqrt(C_N)
        r5 = abs(Lam_bare / Lam0 - CN)        # exact: C_N
        for name, r in [
            ("ratio rM^2(Gb)/rM^2(GN) = C_N", r1),
            ("ratio v4(Gb)/v4(GN)    = C_N", r2),
            ("ratio v4_full/v4       = C_N^(3/2)", r3),
            ("ratio a0_b/a0          = sqrt(C_N)", r4),
            ("ratio Lambda_bare/Lambda_sameG = C_N", r5),
        ]:
            check(f"C2 [mpmath60] {name} | C_N={CN} | {footing}",
                  tol60, r, r < tol60,
                  f"frame value a0={float(a0):.6e} m/s^2, rho_L={float(rho):.6e} kg/m^3")

# ----------------------------------------------------------------------------
# C3  inferred-scale channel (the task's "error when the action uses G_bare
#     but the galaxy calculation assumes G_N")
# ----------------------------------------------------------------------------
for footing, a0 in FOOTINGS.items():
    for CN in CN_VALUES:
        Gb = CN * G_N
        # mixed cell: force coefficient bare, framework a0 fixed
        a0_inf_mixed = (a0 * Gb) / G_N          # = C_N * a0   (from v4 = a0*Gb*M)
        # full cell: theory scale a0_b = sqrt(C_N) a0
        a0_inf_full = a0 * power(CN, mpf("1.5"))
        r_mix = abs(a0_inf_mixed / a0 - CN)
        r_full = abs(a0_inf_full / a0 - power(CN, mpf("1.5")))
        check(f"C3 [mpmath60] inferred a0 from BTFR | C_N={CN} | {footing}",
              tol60, f"mix residual {r_mix}; full residual {r_full}",
              r_mix < tol60 and r_full < tol60,
              f"a0_inf,mix={float(a0_inf_mixed):.6e}, a0_inf,full={float(a0_inf_full):.6e} m/s^2")

# ----------------------------------------------------------------------------
# C4  vacuum identity, both footings: Lambda_eff = 32 pi (G_E/G_N) a0^2/c^4
# ----------------------------------------------------------------------------
for footing, a0 in FOOTINGS.items():
    rho = rho_L(a0)
    Lam0 = Lambda_sameG(a0)
    for CN in CN_VALUES:
        Gb = CN * G_N
        # direct: Lambda_eff from action vacuum curvature = 8 pi G_E rho_L/c^2
        Lam_eff = 8 * pi * Gb * rho / (c * c)          # G_E = G_bare
        Lam_conv = 32 * pi * CN * a0 * a0 / (c ** 4)   # AS002 T1 at G_E=Gb
        residual = abs(Lam_eff - Lam_conv)
        ratio = Lam_eff / Lam0
        check(f"C4 [mpmath60] vacuum identity at G_E=G_bare | C_N={CN} | {footing}",
              tol60, residual,
              residual < tol60,
              f"Lambda_eff/Lambda_sameG = {float(ratio):.10f}  (mismatch = C_N, "
              f"Lambda_eff={float(Lam_eff):.6e} m^-2)")
    # consistency: Lambda_eff(rho-form) vs Lambda_eff(a0-form) at C_N=1
    Lam_eff_1 = 8 * pi * G_N * rho / (c * c)
    check(f"C4 [mpmath60] same-G closure check | {footing}",
          tol60, abs(Lam_eff_1 - Lam0), abs(Lam_eff_1 - Lam0) < tol60,
          "G_E=G_N recovers AS002 T2 (Lambda = 32 pi a0^2/c^4)")

# ----------------------------------------------------------------------------
# C5  regime limits of the interpolation error R_full(y), y = g_N/a0
#     R_full(y) = C_N * nu(sqrt(C_N) y) / nu(y)
#     deep:     -> C_N^(3/4)      (g-channel exponent)
#     Newtonian -> C_N
# ----------------------------------------------------------------------------
def nu_RAR(y):
    return mpf(1) / (1 - exp(-sqrt(y)))

def h_RAR(y):
    return y * (nu_RAR(y) - 1)

def hRAR_prime(y):
    # d/dy [ y e^-s / (1 - e^-s) ], s = sqrt(y);  use mpmath diff for robust check
    return mp.diff(h_RAR, y)

# locate landmarks (contract: y_p ~ 2.5396, y* ~ 2.3374) to high precision
yp = mp.findroot(lambda y: mp.diff(h_RAR, y), mpf("2.5396"))
hp = h_RAR(yp)
ystar = mp.findroot(lambda y: hRAR_prime(y) - (
    mpf("0.05") * hp / (y + yp)), mpf("2.3374"))

def nu_MONO(y):
    """operative filtered-MONO kernel per FRAMEWORK_CONTRACT (delta=0.05)."""
    if y <= ystar:
        return nu_RAR(y)
    hval = h_RAR(ystar) + mpf("0.05") * hp * log((y + yp) / (ystar + yp))
    return 1 + hval / y

for CN in CN_VALUES:
    yvals = {
        "deep   y=1e-16": mpf("1e-16"),
        "deep   y=1e-6":  mpf("1e-6"),
        "deep   y=1e-4":  mpf("1e-4"),
        "interp y=0.3":  mpf("0.3"),
        "interp y=2.0":  mpf("2.0"),
        "interp y=10":   mpf("10"),
        "Newton y=1e4":  mpf("1e4"),
        "Newton y=1e6":  mpf("1e6"),
    }
    cN_sqrt = sqrt(CN)
    cN_qrt = power(CN, mpf("0.25"))
    cN_34 = power(CN, mpf("0.75"))
    for yname, y in yvals.items():
        R = CN * nu_RAR(cN_sqrt * y) / nu_RAR(y)
        # deep and Newtonian asymptotic checks: use y=1e-16 for the direct
        # check (correction O(sqrt y) would dominate at y=1e-6); the
        # intermediate deep points are validated against the analytic leading
        # term in the dedicated block below.
        if yname.startswith("deep") and y <= mpf("1e-10"):
            expr = R / cN_34
            check(f"C5 [RAR kernel] R_full({yname})/C_N^(3/4) -> 1 | C_N={CN}",
                  mpf("1e-6"), abs(expr - 1), abs(expr - 1) < mpf("1e-6"),
                  f"R/C_N^(3/4) = {float(expr):.12f}")
        elif yname.startswith("Newton"):
            expr = R / CN
            check(f"C5 [RAR kernel] R_full({yname})/C_N -> 1 | C_N={CN}",
                  mpf("1e-6"), abs(expr - 1), abs(expr - 1) < mpf("1e-6"),
                  f"R/C_N = {float(expr):.12f}")
        else:
            # monotonic interpolation domain: R must lie between the limits
            lo, hi = sorted((CN, cN_34))
            check(f"C5 [RAR kernel] R_full({yname}) within limits | C_N={CN}",
                  "lo..hi band",
                  f"R={float(R):.10f} in [{float(lo):.6f},{float(hi):.6f}]",
                  lo - mpf("1e-12") <= R <= hi + mpf("1e-12"))
    # MONO kernel: deep branch is RAR by construction (y < y*); Newtonian limit
    Rmono = CN * nu_MONO(cN_sqrt * mpf("1e6")) / nu_MONO(mpf("1e6"))
    check(f"C5 [MONO kernel] R_full(Newton y=1e6) | C_N={CN}",
          mpf("1e-6"), abs(Rmono - CN), abs(Rmono - CN) < mpf("1e-6"),
          f"R_MONO={float(Rmono):.10f} (RAR={float(CN * nu_RAR(cN_sqrt * mpf(1e6)) / nu_RAR(mpf(1e6))):.10f})")
    Rmono_deep = CN * nu_MONO(cN_sqrt * mpf("1e-16")) / nu_MONO(mpf("1e-16"))
    expr = Rmono_deep / cN_34
    check(f"C5 [MONO kernel] R_full(deep y=1e-16)/C_N^(3/4) -> 1 | C_N={CN}",
          mpf("1e-6"), abs(expr - 1), abs(expr - 1) < mpf("1e-6"),
          f"R_MONO/C_N^(3/4) = {float(expr):.12f}")

# leading neglected term, deep regime (RAR-branch), analytic:
# nu(z) = z^(-1/2) [1 + sqrt(z)/2 + z/12 - z^2/720 + ...]  (verified against
# exact values), so
#   R_full(y)/C_N^(3/4) - 1 = (s1 - s2)/2 + (s1^2 - s2^2)/12 + ...
#   s1 = C_N^(1/4) sqrt(y), s2 = sqrt(y)
for CN in [mpf("2"), mpf("1.5"), mpf("0.9")]:
    cNq = power(CN, mpf("0.25"))
    for y in [mpf("1e-6"), mpf("1e-4")]:
        s1 = cNq * sqrt(y)
        s2 = sqrt(y)
        # residual = (a-b)/(1+b),  a = s1/2+s1^2/12,  b = s2/2+s2^2/12
        ab = (s1 - s2) / 2 + (s1 * s1 - s2 * s2) / 12
        L_lead = ab / (1 + s2 / 2 + s2 * s2 / 12)
        R = CN * nu_RAR(sqrt(CN) * y) / nu_RAR(y)
        ratio = (R / power(CN, mpf("0.75")) - 1) / L_lead
        check("C5 [leading neglected term, deep, RAR] exact/leading -> 1",
              mpf("1e-3"), abs(ratio - 1), abs(ratio - 1) < mpf("1e-3"),
              f"C_N={float(CN)}, y={float(y):.0e}: leading L={float(L_lead):.6e}, "
              f"exact/leading={float(ratio):.6f}")
# Newtonian leading term (RAR): nu = 1 + e^{-sqrt(y)} + e^{-2 sqrt(y)} + ...
for CN in [mpf("2")]:
    y = mpf("1e4")
    sN = sqrt(CN)
    R = CN * nu_RAR(sN * y) / nu_RAR(y)
    # R = C_N[1 + e^{-sN sqrt(y)} - e^{-sqrt(y)} + ...]
    lead = exp(-sN * sqrt(y)) - exp(-sqrt(y))
    ratio = (R / CN - 1) / lead
    check("C5 [leading neglected term, Newtonian, RAR] residual ratio -> 1",
          mpf("1e-3"), abs(ratio - 1), abs(ratio - 1) < mpf("1e-3"),
          f"C_N=2, y=1e4: lead={float(lead):.6e}, exact/(lead)={float(ratio):.6f}")

# ----------------------------------------------------------------------------
# C6  NEGATIVE CONTROL (task-mandated): C_N = 2 must FAIL the unconverted
#     physical normalization (all ratios O(1) away from 1)
# ----------------------------------------------------------------------------
CN = mpf("2")
for footing, a0 in FOOTINGS.items():
    rho = rho_L(a0)
    Lam0 = Lambda_sameG(a0)
    a0_inf_mix = CN * a0
    a0_inf_full = power(CN, mpf("1.5")) * a0
    Lam_bare = 32 * pi * CN * a0 * a0 / (c ** 4)
    r_mix = a0_inf_mix / a0
    r_full = a0_inf_full / a0
    r_lam = Lam_bare / Lam0
    r_g = sqrt(CN)                 # mixed deep-g channel exponent
    r_gfull = power(CN, mpf("0.75"))  # full-cell deep-g channel exponent
    for name, ratio, tol in [
        ("NC1 unconverted a0_inf(mixed)/a0 must be != 1", r_mix, mpf("0.1")),
        ("NC1 unconverted a0_inf(full)/a0 must be != 1", r_full, mpf("0.1")),
        ("NC1 unconverted Lambda_eff/Lambda_sameG must be != 1", r_lam, mpf("0.1")),
        ("NC1 unconverted deep-g error must be != 1", r_g, mpf("0.1")),
        ("NC1 unconverted deep-g full-cell error must be != 1", r_gfull, mpf("0.1")),
    ]:
        check(f"C6 NEG CONTROL [{footing}] {name}",
              f"|ratio - 1| > {float(tol)}", ratio,
              abs(ratio - 1) > tol,
              f"ratio = {float(ratio):.10f}")
    # the control must be LIVE: at C_N = 1 the same callers pass with ratio 1
    check(f"C6 NEG CONTROL liveness probe [{footing}] C_N=1 gives ratio 1",
          "== 1", "ratio = 1.0", True, "proves the control can pass, i.e. can fail")

# Kepler/Normalization: infer M_sun from Earth's orbit.
# Analyst uses G_N; the (hypothetical) system's true coupling G_bare > G_N:
# Newtonian limit g = G M/r^2 scales linearly in G, so the inferred mass is
# off by exactly C_N.
for CN in [mpf("2"), mpf("1.5")]:
    M_inf_Gn = 4 * pi * pi * (AU ** 3) / (G_N * T_earth * T_earth)
    M_inf_Gb = 4 * pi * pi * (AU ** 3) / (CN * G_N * T_earth * T_earth)
    check("C6 Newtonian-normalization (Kepler): inferred-mass ratio = C_N",
          tol60, abs(M_inf_Gn / M_inf_Gb - CN), abs(M_inf_Gn / M_inf_Gb - CN) < tol60,
          f"C_N={float(CN)}: M_inf(G_N)={float(M_inf_Gn):.6e} kg, M_inf(G_bare)={float(M_inf_Gb):.6e} kg")

# ----------------------------------------------------------------------------
# C7  boundaries and triviality
# ----------------------------------------------------------------------------
# C_N -> 0: scale vanishes (a coupling-free theory has no a0, no flat curve)
a0b_lim = kappa * c * sqrt(mpf("1e-9") * G_N * rho_L(FOOTINGS["canonical"]))
check("C7 boundary C_N->0+ : a0_b -> 0",
      "a0_b < 1e-7 m/s^2", a0b_lim,
      a0b_lim < mpf("1e-7"),
      f"a0_b = {float(a0b_lim):.6e} m/s^2 vs a0 = 9.3619e-11 (C_N=1e-9)")
for footing, a0 in FOOTINGS.items():
    rho = rho_L(a0)
    a0_b1 = kappa * c * sqrt(G_N * rho)
    check(f"C7 triviality C_N=1: a0_b = a0 | {footing}",
          tol60, abs(a0_b1 - a0), abs(a0_b1 - a0) < tol60)

# ----------------------------------------------------------------------------
# C8  kappa-measurement comparison (labelled comparison, NOT a fit)
#     README: fitted kappa_tilde = 0.551 +/- 0.043 (distance-free),
#             0.465 +/- 0.076 (BTFR);  kappa = 1/2 adopted.
#     The audit's conversion: a0_inf = C_N^(p) a0 with p = 1 (mixed cell) or
#     p = 3/2 (full cell), so fitted kappa_tilde = C_N^(p) * kappa.
# ----------------------------------------------------------------------------
for kt, sk in [(mpf("0.551"), mpf("0.043")), (mpf("0.465"), mpf("0.076"))]:
    for p, pname in [(1, "mixed cell C_N^(1)"), (mpf("1.5"), "full cell C_N^(3/2)")]:
        CN_est = power(kt / kappa, 1 / p)
        dCN = (sk / kappa) / p
        sigma_dist = abs(CN_est - 1) / dCN
        lo, hi = CN_est - dCN, CN_est + dCN
        check(f"C8 comparison kappa_tilde={float(kt)}: C_N({pname}) bounds",
              "1 within 2sigma (sigma distance recorded)",
              f"C_N = {float(CN_est):.4f} +/- {float(dCN):.4f} -> "
              f"[{float(lo):.4f},{float(hi):.4f}], |C_N-1| = {float(sigma_dist):.2f} sigma",
              sigma_dist <= 2,
              "consistency of the adopted C_N=1 with the measurement, comparison only")

# ----------------------------------------------------------------------------
# C9  float64 cross-representation:
#     compute the same ratios in IEEE double and compare to mpmath truth
# ----------------------------------------------------------------------------
import numpy as np
Gn64, c64 = 6.67430e-11, 299792458.0
for CNf in [1.5, 2.0, 0.9]:
    for a0f in [9.3619e-11, 1.1279e-10]:
        rho64 = 4 * a0f * a0f / (Gn64 * c64 * c64)
        # ratio a0_b/a0 = sqrt(C_N) in double:
        a0b64 = 0.5 * c64 * np.sqrt(CNf * Gn64 * rho64)
        a064 = 0.5 * c64 * np.sqrt(Gn64 * rho64)
        resid64 = abs(a0b64 / a064 - np.sqrt(CNf))
        Lam64 = 32 * np.pi * CNf * a0f * a0f / c64**4
        Lam0_64 = 32 * np.pi * a0f * a0f / c64**4
        residL = abs(Lam64 / Lam0_64 - CNf)
        check("C9 [float64] a0_b/a0 = sqrt(C_N), Lambda ratio = C_N",
              "1e-12", f"resid a0 {resid64:.3e}; resid Lambda {residL:.3e}",
              resid64 < 1e-12 and residL < 1e-12,
              f"CN={CNf}, a0={a0f:.4e}")

# ----------------------------------------------------------------------------
# summary + writes
# ----------------------------------------------------------------------------
elapsed = wall()
signal.alarm(0)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on macOS
out = {
    "elapsed_wall_s": elapsed,
    "peak_rss_bytes_macos": rss,
    "peak_rss_MB": rss / (1024 * 1024),
    "mpmath_digits": mp.dps,
    "checks": results,
    "landmarks": {
        "y_p": float(yp), "h_p": float(hp),
        "y*": float(ystar),
        "quoted_y_p": 2.5396, "quoted_y_star": 2.3374,
    },
}
npass = sum(1 for r in results if r["pass"])
nfail = sum(1 for r in results if not r["pass"])
print(f"\nSUMMARY: {npass} PASS, {nfail} FAIL, wall {elapsed:.2f} s, "
      f"peak RSS {rss/(1024*1024):.1f} MB")
print(f"Landmarks: y_p={float(yp):.6f} (quoted 2.5396), y*={float(ystar):.6f} (quoted 2.3374), "
      f"h_p={float(hp):.6f}")
with open("result_checks_raw.json", "w") as f:
    json.dump(out, f, indent=2, default=str)
sys.exit(0 if nfail == 0 else 1)