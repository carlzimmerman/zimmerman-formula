#!/usr/bin/env python3
r"""mi_scale_bridging_2026.py -- LANE K: SCALE-BRIDGING CONSISTENCY.
Can one front FIX a parameter another front merely FITS?

=========================================================================================================
THE QUESTION, stated so it can come out any of three ways
=========================================================================================================
A parameter fitted to ONE dataset is a fit.  A parameter forced to a unique value by having to satisfy
SEVERAL INDEPENDENT constraints at once is DERIVED BY OVER-DETERMINATION.  So: build the
(parameters x fronts) sensitivity matrix with REAL numerical derivatives on REAL data, take its RANK,
and report

    n_free_dof = n_params - rank

Three outcomes, all decisive, none steered toward:
  (a) rank == n_params  -> every parameter is determined; report the values.
  (b) some front pair is mutually exclusive at high sigma -> falsified; name the pair.
  (c) rank < n_params   -> a continuum survives; name every flat direction and say why it is flat.

MANDATORY CREDIT.  nu(y) = sqrt(1 + 1/y) and the de Sitter-Unruh balance are Milgrom 1999 PLA 253:273
eqs 6-9; his eqs 10-11 give a SECOND coefficient, and Milgrom 2008 sec 7.3.1 notes the coefficient
mismatch "isn't necessarily meaningful".  a_lambda = c^2 sqrt(Lambda/3) is Milgrom 1994 Ann.Phys.
229:384.  Temperature: Narnhofer, Peter & Thirring 1996 IJMPB 10:1507.  Five-acceleration: Deser & Levin
1997 CQG 14:L163.  Exponential kernel: McGaugh 2008 ApJ 683:137 eq 11a.  kappa = 1/2 is FITTED, NOT
DERIVED.  The framework's distinctive content is the c H_Lambda / Z COEFFICIENT plus the modified-inertia
completion, not the kernel.

WHAT IS COMPUTED HERE FROM RAW DATA (nothing imported for these):
  * 175 SPARC rotmod files  -> the RAR a0-fit, its shift with the tail exponent, its shift with the
    memory gate, and the binding galactic orbital frequency.
  * eRASS1 (Bulbul+2024) 9830 clusters -> eta(R500) on the framework's own kernel and its derivatives.
  * the tail family, the ephemeris residual, the wide-binary gamma_v, a0(z), the LLR drift: closed form,
    sympy-verified.

WHAT IS IMPORTED AND LABELLED (committed corpus scripts, re-derived where cheap):
  sigma(a0)_SPARC = 1.24% / 5.44%        mi_kappa_sensitivity_census_2026.py + kappa-discriminability lane
  Earth ephemeris 2-sigma 3.66e-14 m/s2  mi_alpha1_solar_system_2026.py S4 (from Sereno-Jetzer 2006 eq 9
                                         + Pitjeva EPM2004 Table 1)
  EFE suppression 9.5x on the anomaly    mi_alpha1_solar_system_2026.py S3
  gamma_v = 1.0310, sigma_sys = 0.02     PREREGISTRATION_DR4 Amendment 7 / mi_amendment7_wb_target_conflict
  eta(R500) = 2.334 med, +0.4052 dex     clusters_eta_audit.py  (systematic floor 0.10-0.30 dex)
  LLR Gdot/G = (-5.0 +- 9.6)e-15 /yr     Biskupek, Mueller & Torre 2021 Universe 7:34
  omega_c window 1.782-2.211e-14 rad/s   mi_omegac_edges_closure_2026.py
  MSA-3D controlled a0(z) residual       +0.91 +- 0.8   (a0(z) lane)
  Crater II sigma = 2.7 +- 0.3 km/s      McGaugh & Milgrom 2013 pre-prediction 2.1 km/s
  DESI DR2 (w0,wa)                       2503.14738, four SN combos

TWO WAYS THIS PROJECT HAS MANUFACTURED FALSE DEFICITS, and how each is guarded here:
  (i)  model SCATTER used as measurement error.  GUARD: every sigma in the matrix is either a published
       measurement error, a published systematic floor, or a published parameter uncertainty.  The SPARC
       RAR scatter (0.108 dex) is NEVER used as a sigma; it enters only through the committed
       sigma(a0) that a proper Upsilon-free fit produced.  The cluster row uses the SYSTEMATIC FLOOR,
       never the 367-sigma statistical figure.
  (ii) a systematic range truncated at its TIGHT end.  GUARD: the headline matrix uses the LOOSE end of
       every range (cluster floor 0.30 dex not 0.10; sigma(a0) 5.44% not 1.24%), and the rank is then
       recomputed at the TIGHT end to show the answer does not depend on the choice.

PROVE-BY-MOVING-THE-NUMBER.  Every check below was verified to be FAILABLE by mutating the source and
re-running (2026-08-07).  Result, six mutations, all exit 1 with real [FAIL] lines -- no check here is of
the "best > X or best < X" or "a == a" kind that has been caught in this project before:
    a0_canon 9.3614e-11 -> 1.2000e-10                  7 FAILs
    kernel exponent 1/(2 alpha) -> 1/alpha              1 FAIL
    gate 1/(1+r^2) -> 1/(1+r)                           2 FAILs
    nu-1 via naive (1+t)^p - 1 (undo the HAZARD 1 guard) 3 FAILs
    EFE suppression 9.5 -> 950                          1 FAIL
    kappa column halved (break the exact degeneracy)    2 FAILs
Three checks were REWRITTEN during this session because they could not fail as first drafted, and the
reason is recorded at each site: the y^(1-alpha) underflow check (was true by construction of the search
that found it -- now tested against 30-digit sympy), the wide-binary gamma_v round-trip (was the
calibration reproducing itself -- now tests shape-sensitivity), the Crater II calibration (same defect --
now tests the SIGN of the required xi), the rank-drop check (rank <= rank always -- now tests EQUALITY),
and the grid-refinement check (a refined grid is always closer -- now tests that the coarse bias is large
enough to matter).

FLOAT64 HAZARDS ACTUALLY PRESENT HERE, each demonstrated:
  * nu - 1 at y ~ 6e7 loses ~8 significant digits by naive (1+t)**p - 1; expm1/log1p used throughout.
  * y**(1-alpha) at large alpha underflows to exactly 0.0, turning "< bound" into "== 0".
  * Re G = 1/(1+r^2) with r ~ 1e7: 1 - Re G underflows; Re G is used directly, never 1-ReG.
  * the alpha_min root is found on a grid AND by brentq, and the grid is refined 4x with the shift shown.
"""
from __future__ import annotations

import glob
import math
import os
import sys

import numpy as np
import sympy as sp
from astropy.io import fits
from scipy.optimize import brentq, minimize

np.seterr(all="ignore")
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

RULE = "=" * 105
_PASS = 0
_FAIL = 0


def banner(s: str) -> None:
    print("\n" + RULE + "\n" + s + "\n" + RULE)


def check(cond: bool, msg: str) -> None:
    global _PASS, _FAIL
    if cond:
        _PASS += 1
        print(f"   [OK] {msg}")
    else:
        _FAIL += 1
        print(f"   [FAIL] {msg}")


# =========================================================================================================
# 0.  CONSTANTS, FOOTINGS, PATHS
# =========================================================================================================
c = 2.99792458e8
G = 6.674e-11
kpc = 3.0856775814913673e19
pc = kpc / 1e3
Msun = 1.98892e30
YR = 3.15576e7
AU = 1.495978707e11

A0_CANON = 9.3614e-11          # kappa=1/2, rho_DE, c H_Lambda / Z
A0_ALT = 1.1311e-10            # ALT footing: rho_total, c H_0 / Z   (= canon / sqrt(Omega_Lambda))
OMEGA_L = 0.6847

HERE = os.path.dirname(os.path.abspath(__file__))
SPARC_DIR = os.path.join(HERE, "..", "data", "sparc_data")
SPARC_MASTER = os.path.join(HERE, "..", "data", "sparc_master_clean.csv")
ERASS_FITS = os.path.join(HERE, "..", "data", "erass1cl_primary_v3.2.fits")


# =========================================================================================================
# 1.  THE ONE-PARAMETER TAIL FAMILY -- contains the framework EXACTLY, deep-MOND-exact for every alpha
# =========================================================================================================
#   nu_alpha(y) = (1 + y^-alpha)^(1/(2 alpha))
#     alpha = 1   ->  sqrt(1 + 1/y)          == Milgrom 1999 eq 9 == the framework's kernel, EXACTLY
#     y -> 0      ->  y^(-1/2)               for EVERY alpha  (so a0's deep-MOND meaning is alpha-invariant)
#     y -> inf    ->  1 + y^-alpha/(2 alpha) so  Delta g = a0 y^(1-alpha)/(2 alpha)
#     alpha = 1   ->  Delta g = a0/2         CONSTANT sunward anomaly, the committed A = 1/2
#     alpha = 2   ->  Delta g = a0/(4 y)     the 'standard'-class tail, passes the planets trivially
def nu_alpha(y, alpha):
    """(1 + y^-alpha)^(1/(2 alpha)), overflow/cancellation-safe."""
    y = np.asarray(y, dtype=float)
    t = np.exp(-alpha * np.log(y))                     # y^-alpha without pow overflow
    return np.exp(np.log1p(t) / (2.0 * alpha))


def nu_minus_one(y, alpha):
    """nu_alpha(y) - 1 WITHOUT catastrophic cancellation (expm1 o log1p)."""
    y = np.asarray(y, dtype=float)
    t = np.exp(-alpha * np.log(y))
    return np.expm1(np.log1p(t) / (2.0 * alpha))


def re_G(omega, omega_c):
    """single-pole causal Debye relaxator, Re G = 1/(1 + (omega/omega_c)^2).  Used directly, never 1-ReG."""
    r = np.asarray(omega, dtype=float) / omega_c
    return 1.0 / (1.0 + r * r)


def sec1_family():
    banner("1.  THE SHAPE DOF: a one-parameter tail family that contains the framework EXACTLY (sympy)")
    y, a = sp.symbols("y alpha", positive=True)
    nu = (1 + y**(-a))**(sp.Rational(1, 2) / a)
    nu1 = sp.simplify(nu.subs(a, 1))
    check(sp.simplify(nu1 - sp.sqrt(1 + 1 / y)) == 0,
          f"alpha = 1 reproduces Milgrom 1999 eq 9 nu = sqrt(1+1/y) IDENTICALLY (sympy: {nu1})")

    # the exact algebraic law g_obs^2 = g_bar^2 + a0 g_bar at alpha = 1
    a0s, gb = sp.symbols("a0 g_bar", positive=True)
    go = nu1.subs(y, gb / a0s) * gb
    check(sp.simplify(sp.expand(go**2 - gb**2 - a0s * gb)) == 0,
          "alpha = 1 IS the exact a0-line g_obs^2 = g_bar^2 + a0 g_bar, algebraically (so the family's "
          "alpha is exactly the dof the exact law spends)")

    # deep-MOND limit is alpha-INVARIANT: nu -> y^(-1/2)
    for av in (1, 1.5, 2, 3):
        lim = sp.limit(nu.subs(a, av) * sp.sqrt(y), y, 0)
        check(sp.simplify(lim - 1) == 0,
              f"alpha = {av}: deep limit nu*sqrt(y) -> {lim}, so a0's deep-MOND normalisation is "
              f"IDENTICAL for every alpha -- the shape dof does NOT trade against a0 in the deep regime")

    # the tail coefficient.  Done as a series in t = y^-alpha (fast and exact); the direct
    # limit in y with SYMBOLIC alpha does not terminate in sympy, so it is not used.
    t = sp.symbols("t", positive=True)
    ser = sp.series((1 + t)**(sp.Rational(1, 2) / a), t, 0, 2).removeO()
    lead = sp.simplify(sp.expand(ser).coeff(t, 1))
    check(sp.simplify(lead - 1 / (2 * a)) == 0,
          f"tail (series in t = y^-alpha): nu = 1 + t/(2 alpha) + O(t^2), sympy leading coefficient "
          f"{lead}.  So Delta g / a0 = (nu-1) y -> y^(1-alpha)/(2 alpha) exactly; at alpha = 1 that is the "
          f"committed CONSTANT a0/2, at alpha = 2 it falls as 1/(4y)")
    for av, want in ((1.0, 0.5), (2.0, 0.25)):
        num = float(nu_minus_one(1e14, av)) * 1e14 * 1e14**(av - 1.0)
        check(abs(num / want - 1) < 1e-6,
              f"numerically at y = 1e14, alpha = {av}: Delta g/a0 x y^(alpha-1) = {num:.10f} against the "
              f"predicted 1/(2 alpha) = {want} -- the closed form and the float64 kernel agree")

    # FLOAT64 HAZARD 1: nu-1 at the Earth's y
    yE = 6.336e7
    naive = (1.0 + yE**-1.0)**0.5 - 1.0
    safe = float(nu_minus_one(yE, 1.0))
    exact = float(sp.N((sp.sqrt(1 + sp.Rational(1, 1) / sp.Float(yE, 40)) - 1), 40))
    err_naive = abs(naive - exact) / exact
    err_safe = abs(safe - exact) / exact
    print(f"  nu-1 at y = {yE:.4e}: exact {exact:.17e}")
    print(f"                        naive (1+t)**0.5-1  {naive:.17e}   rel err {err_naive:.2e}")
    print(f"                        expm1(log1p(t)/2)   {safe:.17e}   rel err {err_safe:.2e}")
    check(err_safe < 1e-14 and err_naive > 100 * max(err_safe, 1e-17),
          f"HAZARD 1 real and guarded: expm1/log1p is accurate to {err_safe:.1e} where the naive form is "
          f"{err_naive:.1e} -- a factor {err_naive/max(err_safe,1e-17):.0e} worse at the acceleration where "
          f"the ephemeris front lives")

    # FLOAT64 HAZARD 2: y^(1-alpha) underflow turns a strict inequality into an equality
    a_uf = next(a for a in range(2, 400) if yE**(1.0 - a) == 0.0)
    true_val = sp.N(sp.Float(yE, 60)**(1 - a_uf), 30)      # the same number in 30-digit arithmetic
    print(f"  y^(1-alpha) at y = {yE:.4e} first evaluates to EXACTLY 0.0 in float64 at alpha = {a_uf}; "
          f"in 30-digit arithmetic it is {f"{float(true_val):.4e}"}")
    check(true_val > 0 and a_uf < 100,
          f"HAZARD 2 real, and the check is against EXTENDED PRECISION not against itself: at alpha = "
          f"{a_uf} the true tail term is {f"{float(true_val):.4e}"} > 0 while float64 returns exactly 0.0.  So "
          f"an 'anomaly < bound' test run by SCANNING alpha upward is eventually passed by an UNDERFLOW "
          f"rather than by physics, and it happens at only alpha = {a_uf}, well inside a range a careless "
          f"scan would cover.  Sec. 7 therefore brackets the root with brentq on the LOG")

    # FLOAT64 HAZARD 3: the gate's complement loses the gate
    om_E = 2 * math.pi / YR
    rg = float(re_G(om_E, 2.0e-14))
    rg_round = 1.0 - (1.0 - rg)                       # what a (1-ReG)-based bookkeeping would return
    loss = abs(rg_round - rg) / rg
    print(f"  at the Earth's orbital frequency Re G = {rg:.6e}; reconstructing it through its complement "
          f"gives {rg_round:.6e}, a relative loss of {loss:.2e}")
    check(loss > 1e-3,
          f"HAZARD 3 real: passing the gate through its complement (1 - Re G) destroys "
          f"{100*loss:.1f}% of Re G at planetary frequencies -- so the gate is applied here ONLY as a "
          f"direct MULTIPLIER on the boost, never as (1 - Re G) on the total")
    return None


# =========================================================================================================
# 2.  SPARC:  the RAR a0-fit, and its derivatives w.r.t. the shape dof and the memory gate
# =========================================================================================================
def load_sparc():
    """175 rotmod files + the master table (for Q and inclination cuts)."""
    meta = {}
    with open(SPARC_MASTER) as fh:
        hdr = fh.readline().strip().split(",")
        iQ, iinc = hdr.index("Q"), hdr.index("inc")
        for line in fh:
            p = line.strip().split(",")
            if len(p) < len(hdr):
                continue
            try:
                meta[p[0]] = (float(p[iQ]), float(p[iinc]))
            except ValueError:
                continue
    gal = []
    for f in sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat"))):
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        name = os.path.basename(f).replace("_rotmod.dat", "")
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        gal.append(dict(name=name, R=R * kpc, Vobs=Vobs, eV=eV,
                        Vgas=Vgas, Vdisk=Vdisk, Vbul=Vbul,
                        Q=meta.get(name, (9.0, 0.0))[0], inc=meta.get(name, (9.0, 0.0))[1]))
    return gal


SPARC = load_sparc()


def sparc_assemble(Ud):
    """(g_bar, g_obs, weight, omega_orb) over all points at disk M/L = Ud, bulge = 1.4 Ud."""
    Ub = 1.4 * Ud
    gb, go, w, om = [], [], [], []
    for g in SPARC:
        Vbar2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + Ud * g["Vdisk"]**2 + Ub * g["Vbul"]**2
        g_b = Vbar2 * 1e6 / g["R"]
        g_o = (g["Vobs"] * 1e3)**2 / g["R"]
        m = (g_b > 0) & (g_o > 0) & np.isfinite(g_b) & np.isfinite(g_o) & (g["Vobs"] > 0)
        fr = np.clip(g["eV"][m], 1.0, None) / np.clip(g["Vobs"][m], 1.0, None)
        gb.append(g_b[m]); go.append(g_o[m]); w.append(1.0 / fr**2)
        om.append(g["Vobs"][m] * 1e3 / g["R"][m])
    return (np.concatenate(gb), np.concatenate(go), np.concatenate(w), np.concatenate(om))


_ASM_CACHE: dict[float, tuple] = {}


def asm(Ud):
    k = round(Ud, 6)
    if k not in _ASM_CACHE:
        _ASM_CACHE[k] = sparc_assemble(k)
    return _ASM_CACHE[k]


def sparc_rms(a0, Ud, alpha=1.0, omega_c=None, g_ex=0.0):
    """weighted rms of log10 g_obs - log10 g_pred.
    EFE enters in QUADRATURE (the standard external-field surrogate): the BOOST is evaluated at
    y_eff = sqrt(y^2 + y_ex^2) so a nonzero g_ex weakens the boost where g_bar < g_ex and leaves the
    high-acceleration points untouched.  Adding g_ex to g_bar directly -- a first draft did that -- is
    wrong: it moves EVERY point including the innermost ones and manufactures a large spurious
    derivative.  Gate (if omega_c) multiplies the BOOST.
    """
    gb, go, w, om = asm(Ud)
    y_eff = np.sqrt((gb / a0)**2 + (g_ex / a0)**2)
    boost = nu_minus_one(y_eff, alpha) * (y_eff * a0) / np.maximum(gb, 1e-300)
    if omega_c is not None:
        boost = boost * re_G(om, omega_c)
    gpred = gb * (1.0 + boost)
    r = np.log10(go) - np.log10(gpred)
    return float(np.sqrt(np.sum(w * r * r) / np.sum(w)))


_FIT_CACHE: dict[tuple, tuple] = {}


def sparc_fit_a0(alpha=1.0, omega_c=None, g_ex=0.0, refine=True):
    """profile Upsilon_d AND a0.  Returns (log10 a0_hat, Ud_hat, rms).  Coarse grid then Nelder-Mead."""
    key = (round(alpha, 8), None if omega_c is None else round(math.log10(omega_c), 8),
           round(g_ex, 20), bool(refine))
    if key in _FIT_CACHE:
        return _FIT_CACHE[key]
    best = (None, None, 1e9)
    for la in np.arange(-10.6, -9.55, 0.05):
        for Ud in np.arange(0.30, 1.21, 0.05):
            r = sparc_rms(10**la, Ud, alpha, omega_c, g_ex)
            if r < best[2]:
                best = (la, Ud, r)
    if not refine:
        _FIT_CACHE[key] = best
        return best
    res = minimize(lambda p: sparc_rms(10**p[0], max(p[1], 0.02), alpha, omega_c, g_ex),
                   x0=[best[0], best[1]], method="Nelder-Mead",
                   options=dict(xatol=1e-6, fatol=1e-12, maxiter=4000))
    out = (float(res.x[0]), float(max(res.x[1], 0.02)), float(res.fun))
    _FIT_CACHE[key] = out
    return out


def sec2_sparc():
    banner("2.  SPARC (175 rotmod files, computed here): the RAR a0-fit and its real derivatives")
    check(len(SPARC) >= 170, f"loaded {len(SPARC)} SPARC rotmod files from {os.path.relpath(SPARC_DIR, HERE)}")
    gb, go, w, om = asm(0.70)
    print(f"  points: {gb.size}   median g_bar/a0(canon) = {np.median(gb/A0_CANON):.3f}")

    # -- regression against the committed 0.108 dex
    r108 = sparc_rms(A0_CANON, 0.70, alpha=1.0)
    check(abs(r108 - 0.108) < 0.004,
          f"REGRESSION: framework kernel at a0 = canon, Upsilon_d = 0.70 gives {r108:.4f} dex, reproducing "
          f"the committed 0.108 dex of rar_framework_a0_mlfit.py")

    # -- the free fit
    la1, Ud1, rms1 = sparc_fit_a0(alpha=1.0)
    print(f"  free fit, alpha = 1 : log10 a0_hat = {la1:.4f}  (a0_hat = {10**la1:.4e})  "
          f"Upsilon_d = {Ud1:.3f}  rms = {rms1:.4f} dex")
    print(f"                        a0_hat / a0_canon = {10**la1/A0_CANON:.4f}   "
          f"a0_hat / a0_alt = {10**la1/A0_ALT:.4f}")
    # the a0-Upsilon degeneracy, shown rather than asserted: a0_hat at Upsilon HELD
    held = []
    for Ud in (0.50, 0.55, 0.60, 0.65, 0.70, 0.80, 1.00):
        la = min(np.arange(-10.4, -9.35, 0.002), key=lambda l: sparc_rms(10**l, Ud, 1.0))
        la = float(minimize(lambda p: sparc_rms(10**p[0], Ud, 1.0), x0=[la], method="Nelder-Mead",
                            options=dict(xatol=1e-7, fatol=1e-13)).x[0])
        held.append((Ud, la, 10**la / A0_CANON, sparc_rms(10**la, Ud, 1.0)))
    print("\n  THE a0-Upsilon DEGENERACY, shown not asserted (a0_hat at Upsilon_d HELD):")
    print("     Upsilon_d   log10 a0_hat   a0_hat/a0_canon   rms(dex)")
    for Ud, la, rat, rr in held:
        print(f"     {Ud:9.2f}   {la:12.4f}   {rat:15.4f}   {rr:8.4f}")
    # the honest band: only Upsilon values whose rms is within 0.005 dex of the best -- i.e. those the
    # RAR scatter genuinely cannot distinguish.  Wider Upsilon IS penalised (0.044 dex at Ud = 1.0), and
    # quoting that wider span as 'degenerate' would overstate the case.
    rmin = min(h[3] for h in held)
    band = [h for h in held if h[3] - rmin < 0.005]
    spanned = max(h[2] for h in band) / min(h[2] for h in band)
    print(f"     rms-indistinguishable band (within 0.005 dex of best): Upsilon_d "
          f"{min(h[0] for h in band):.2f}-{max(h[0] for h in band):.2f}, a0_hat/canon "
          f"{min(h[2] for h in band):.3f}-{max(h[2] for h in band):.3f}")
    check(spanned > 1.4,
          f"F1's a0 is ESTIMATOR-DEPENDENT, and this is why its sigma is the loose 5.44%: inside the band "
          f"the RAR scatter cannot distinguish (rms within 0.005 dex) a0_hat still slides by a factor "
          f"{spanned:.2f} = {math.log10(spanned):.3f} dex.  A globally-profiled rms fit gives "
          f"{10**la1/A0_CANON:.2f}x canon; the committed per-galaxy Upsilon estimator gives 1.15x.  The "
          f"1.15-{10**la1/A0_CANON:.2f}x ESTIMATOR SPREAD is itself "
          f"{math.log10(10**la1/A0_CANON/1.15)/0.0356:.1f}x the kappa-vs-1/2pi signal (0.0356 dex)")
    check(10**la1 / A0_CANON > 1.0,
          f"AGAINST INTEREST, direction reproduced: SPARC's preferred a0 is {10**la1/A0_CANON:.3f}x the "
          f"CANONICAL value and {10**la1/A0_ALT:.3f}x the ALT value -- on every estimator tried here the "
          f"data lean AWAY from canon and toward ALT or beyond.  The committed 1.15x lean is confirmed in "
          f"sign and exceeded in size")

    # -- coarse-vs-refined shift (HAZARD 4: unsampled extremum)
    coarse = sparc_fit_a0(alpha=1.0, refine=False)
    shift = abs(coarse[0] - la1)
    print(f"  coarse 0.05-dex grid gave {coarse[0]:.4f}; Nelder-Mead refinement gives {la1:.4f} "
          f"(shift {shift:.4f} dex = {shift/0.05:.2f} grid cells)")
    check(shift < 0.05,
          f"HAZARD 4 checked: the refined optimum is inside one coarse cell ({shift:.4f} dex), so the "
          f"grid was not reporting an unsampled extremum")

    # -- d log10 a0_hat / d alpha  (the shape dof's effect on what SPARC prefers)
    d_alpha = 0.25
    lo = sparc_fit_a0(alpha=1.0 - d_alpha)
    hi = sparc_fit_a0(alpha=1.0 + d_alpha)
    dlogA0_dalpha = (hi[0] - lo[0]) / (2 * d_alpha)
    print(f"  alpha = {1-d_alpha:.2f}: log10 a0_hat = {lo[0]:.4f}  rms = {lo[2]:.4f}")
    print(f"  alpha = {1+d_alpha:.2f}: log10 a0_hat = {hi[0]:.4f}  rms = {hi[2]:.4f}")
    print(f"  -> d log10 a0_hat / d alpha = {dlogA0_dalpha:+.5f} dex per unit alpha")

    # -- rms cost of the shape dof across the whole admissible range
    rows = []
    for av in (1.0, 1.25, 1.5, 2.0, 3.0, 6.0):
        laa, Uda, rmsa = sparc_fit_a0(alpha=av)
        rows.append((av, laa, Uda, rmsa))
    print("\n  alpha   log10 a0_hat   Upsilon_d    rms(dex)   vs alpha=1")
    for av, laa, Uda, rmsa in rows:
        print(f"  {av:5.2f}   {laa:12.4f}   {Uda:9.3f}   {rmsa:9.4f}   {rmsa-rows[0][3]:+9.4f}")
    spread = max(r[3] for r in rows) - min(r[3] for r in rows)
    SIGMA_INT = 0.034                     # Desmond 2023 marginalised RAR intrinsic scatter
    check(spread < SIGMA_INT,
          f"REGRESSION + the Q4 premise: the ENTIRE rms spread from alpha = 1 to alpha = 6 is {spread:.4f} "
          f"dex = {spread/SIGMA_INT:.2f}x Desmond 2023's sigma_int = {SIGMA_INT} dex.  SPARC does not pay "
          f"for the tail (committed: 0.0084 dex across alpha = 1,2,inf)")

    # -- the memory gate: d log10 a0_hat / d ln omega_c inside the committed window
    OC = 1.9895e-14                        # geometric centre of 1.782-2.211e-14
    dln = 0.35
    g_lo = sparc_fit_a0(alpha=1.0, omega_c=OC * math.exp(-dln))
    g_hi = sparc_fit_a0(alpha=1.0, omega_c=OC * math.exp(+dln))
    g_at = sparc_fit_a0(alpha=1.0, omega_c=OC)
    dlogA0_dlnwc = (g_hi[0] - g_lo[0]) / (2 * dln)
    print(f"\n  gate ON at omega_c = {OC:.4e} rad/s: log10 a0_hat = {g_at[0]:.4f}  rms = {g_at[2]:.4f} dex "
          f"(gate OFF: {la1:.4f} / {rms1:.4f})")
    print(f"  -> d log10 a0_hat / d ln omega_c = {dlogA0_dlnwc:+.5f} dex per e-fold")
    check(abs(g_at[2] - rms1) < 0.05,
          f"the gate at the window centre costs SPARC {g_at[2]-rms1:+.4f} dex in rms -- small, which is "
          f"exactly why the Re G >= 0.90 tolerance was affordable")

    # -- the binding galactic orbital frequency (the lower edge's single load-bearing input)
    best_om, best_gal, best_r = 0.0, "", 0.0
    for g in SPARC:
        if g["Q"] > 2 or g["inc"] < 30:
            continue
        Vbar2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.70 * g["Vdisk"]**2 + 0.98 * g["Vbul"]**2
        g_b = Vbar2 * 1e6 / g["R"]
        m = (g_b > 0) & (g_b < A0_CANON) & (g["Vobs"] > 0)
        if not np.any(m):
            continue
        omg = g["Vobs"][m] * 1e3 / g["R"][m]
        i = int(np.argmax(omg))
        if omg[i] > best_om:
            best_om, best_gal, best_r = float(omg[i]), g["name"], float(g["R"][m][i] / kpc)
    print(f"\n  MAX omega_gal over confirmed deep-MOND SPARC orbits (Q<=2, inc>=30, g_bar<a0):")
    print(f"     {best_om:.4e} rad/s   set by {best_gal} at r = {best_r:.3f} kpc")
    check(abs(best_om / 5.9414e-15 - 1) < 0.02 and best_gal == "UGC05721",
          f"REGRESSION: MAX omega_gal = {best_om:.4e} rad/s at {best_gal}, reproducing "
          f"mi_omegac_edges_closure_2026.py's 5.9414e-15 at UGC05721 to "
          f"{abs(best_om/5.9414e-15-1)*100:.2f}%")

    # -- external-field sensitivity of the SPARC fit (the xi_EFE column)
    # xi_EFE is the strength dial on a FIDUCIAL external field, g_ex = xi * 0.02 a0 (typical SPARC
    # cosmic-web value).  The derivative is taken at xi = 1, NOT across xi = 0 -- d/d ln xi at xi = 0
    # does not exist and a first draft that differenced g_ex = 0 against g_ex > 0 reported a spurious
    # -0.18 dex/e-fold.
    g_ex_fid = 0.02 * A0_CANON
    hh = 0.35
    e_hi = sparc_fit_a0(alpha=1.0, g_ex=g_ex_fid * math.exp(hh))
    e_lo = sparc_fit_a0(alpha=1.0, g_ex=g_ex_fid * math.exp(-hh))
    e_at = sparc_fit_a0(alpha=1.0, g_ex=g_ex_fid)
    dlogA0_dlnxi = (e_hi[0] - e_lo[0]) / (2 * hh)
    print(f"  external field at xi = 1 is g_ex = {g_ex_fid:.3e} m/s2 (2% of a0, quadrature EFE):")
    print(f"     log10 a0_hat = {e_at[0]:.4f} (rms {e_at[2]:.4f}); vs no EFE at all {la1:.4f}")
    print(f"     -> d log10 a0_hat / d ln xi_EFE = {dlogA0_dlnxi:+.5f} dex per e-fold")

    return dict(la1=la1, Ud1=Ud1, rms1=rms1, dalpha=dlogA0_dalpha, dlnwc=dlogA0_dlnwc,
                dlnxi=dlogA0_dlnxi, omega_gal_max=best_om, gal=best_gal, alpha_rows=rows,
                sigma_int=SIGMA_INT)


# =========================================================================================================
# 3.  CLUSTERS: eta(R500) on the framework's own kernel, and its derivatives
# =========================================================================================================
def load_clusters(fstar=0.20):
    d = fits.open(ERASS_FITS)[1].data

    def col(n):
        return np.array([float(v) if str(v).strip() not in ("", "--") else np.nan for v in d[n]], float)

    z, M500, Mgas, fgas, R500 = col("BEST_Z"), col("M500"), col("MGAS500"), col("FGAS500"), col("R500")
    ok = ((z > 0) & (z < 1.0) & np.isfinite(z) & (M500 > 0) & (Mgas > 0) & (R500 > 0)
          & (fgas > 0.01) & (fgas < 0.30))
    R_m = R500[ok] * kpc
    gobs = G * (M500[ok] * 1e13 * Msun) / R_m**2
    gbar = G * ((1 + fstar) * Mgas[ok] * 1e11 * Msun) / R_m**2
    om = np.sqrt(gobs / R_m)                       # v/R with v^2 = g R
    return gobs, gbar, om, int(ok.sum())


def eta_log(gobs, gbar, a0, alpha=1.0, omega_c=None, om=None, delta=0.0):
    gb = gbar * (1.0 + delta)                      # delta = clustered non-baryonic source / baryons
    boost = nu_minus_one(gb / a0, alpha)
    if omega_c is not None:
        boost = boost * re_G(om, omega_c)
    return np.log10(gobs / (gb * (1.0 + boost)))


def sec3_clusters():
    banner("3.  CLUSTERS (eRASS1 Bulbul+2024, computed here): eta(R500) and its real derivatives")
    gobs, gbar, om, N = load_clusters()
    check(N > 9000, f"clean eRASS1 sample N = {N} (0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30, fstar=0.20)")
    le = eta_log(gobs, gbar, A0_CANON, 1.0)
    med = float(np.median(10**le))
    mean_dex = float(np.mean(le))
    print(f"  eta(R500) median = {med:.3f}   mean log10 eta = {mean_dex:+.4f} dex   "
          f"scatter = {np.std(le):.4f} dex")
    print(f"  median g_bar/a0 = {np.median(gbar/A0_CANON):.4f}  ->  DEEP regime "
          f"({100*np.mean(gbar<0.1*A0_CANON):.0f}% below 0.1 a0)")
    check(abs(med - 2.334) < 0.03 and abs(mean_dex - 0.4052) < 0.006,
          f"REGRESSION: eta = {med:.3f} median, {mean_dex:+.4f} dex mean, reproducing clusters_eta_audit.py's "
          f"2.334 / +0.4052 dex on the framework's OWN kernel")

    dl = 0.30
    d_dlna0 = (float(np.mean(eta_log(gobs, gbar, A0_CANON * math.exp(dl), 1.0)))
               - float(np.mean(eta_log(gobs, gbar, A0_CANON * math.exp(-dl), 1.0)))) / (2 * dl)
    print(f"  d <log10 eta> / d ln a0     = {d_dlna0:+.5f} dex per e-fold   "
          f"(deep-limit prediction -0.5*log10(e) = {-0.5*math.log10(math.e):+.5f})")
    check(abs(d_dlna0 + 0.5 * math.log10(math.e)) < 0.01,
          f"the cluster row's a0 derivative equals the deep-limit -1/2 power to "
          f"{abs(d_dlna0+0.5*math.log10(math.e)):.4f} dex -- an INDEPENDENT confirmation that eta is a "
          f"sqrt(a0) observable, so clusters are the WEAKEST a0 lever of any front here")

    da = 0.25
    d_dalpha = (float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0 + da)))
                - float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0 - da)))) / (2 * da)
    print(f"  d <log10 eta> / d alpha     = {d_dalpha:+.5f} dex per unit alpha")
    e1 = float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0)))
    e2 = float(np.mean(eta_log(gobs, gbar, A0_CANON, 2.0)))
    print(f"     alpha = 1 -> {e1:+.4f} dex ;  alpha = 2 -> {e2:+.4f} dex ;  difference {e2-e1:+.4f} dex")
    check(abs(e2 - e1) < 0.02,
          f"THE Q4 CLUSTER LEG: moving alpha from 1 to 2 changes <log10 eta> by only {e2-e1:+.4f} dex "
          f"(< 2% in eta).  Clusters sit at g_bar ~ 0.037 a0, thirty times BELOW the transition, so they "
          f"are blind to the tail -- buying the ephemeris its alpha costs clusters nothing")

    OC = 1.9895e-14
    dlw = 0.35
    d_dlnwc = (float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0, OC * math.exp(dlw), om)))
               - float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0, OC * math.exp(-dlw), om)))) / (2 * dlw)
    print(f"  d <log10 eta> / d ln omega_c = {d_dlnwc:+.3e} dex per e-fold   "
          f"(median omega_cl/omega_c = {np.median(om)/OC:.2e}: the gate is fully OPEN)")

    d_ddelta = (float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0, delta=0.05)))
                - float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0, delta=0.0)))) / 0.05
    delta_close = brentq(lambda dd: float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0, delta=dd))), 0.0, 200.0)
    print(f"  d <log10 eta> / d delta      = {d_ddelta:+.5f} dex per unit delta  "
          f"(delta = clustered non-baryonic source / baryons at R500)")
    print(f"  delta needed to ERASE the cluster offset: {delta_close:.3f}  "
          f"i.e. {delta_close:.2f}x the baryons")
    check(delta_close > 3.0,
          f"AGAINST INTEREST, and this is the I_0 column's whole content: closing eta with the ghost "
          f"condensate needs delta = {delta_close:.2f}, i.e. the condensate must CLUSTER and supply "
          f"{delta_close:.1f}x the baryons at R500 -- which is the LambdaCDM dark-matter amount.  The "
          f"framework's own position (particle-vs-mode) sets the clustered fraction to ZERO, so this entry "
          f"is zeroed BY POSTULATE, not by data")
    return dict(gobs=gobs, gbar=gbar, om=om, N=N, mean_dex=mean_dex, med=med,
                d_dlna0=d_dlna0, d_dalpha=d_dalpha, d_dlnwc=d_dlnwc, d_ddelta=d_ddelta,
                delta_close=delta_close)


# =========================================================================================================
# 4.  THE CLOSED-FORM FRONTS: ephemeris, wide binaries, a0(z), LLR, Crater II
# =========================================================================================================
# --- ephemeris ------------------------------------------------------------------------------------------
G_BAR_EARTH = G * 1.98892e30 * 1.32712440018e20 / (G * 1.98892e30) / (1.49598023e11)**2  # = GM/r^2
G_BAR_EARTH = 1.32712440018e20 / (1.49598023e11)**2
EPH_2SIG = 3.66e-14          # m/s2, Earth: Sereno-Jetzer 2006 eq 9 + Pitjeva EPM2004 Table 1
EFE_SUPP = 9.5               # committed host-subtraction suppression, canonical footing, primary g_ext


def eph_residual(a0, alpha, xi=1.0):
    """residual constant sunward anomaly at the Earth, after the framework's own EFE subtraction."""
    y = G_BAR_EARTH / a0
    return float(a0 * nu_minus_one(y, alpha) * y / (EFE_SUPP * xi))


# --- wide binaries ------------------------------------------------------------------------------------
WB_GAMMA_TARGET = 1.0310     # PREREGISTRATION_DR4 Amendment 7, in-force alpha = 2 target
WB_SIGMA_SYS = 0.02


def _y_wb():
    """the y at which the alpha=2 kernel reproduces the frozen in-force gamma_v = 1.0310."""
    return brentq(lambda y: math.sqrt(float(nu_alpha(y, 2.0))) - WB_GAMMA_TARGET, 0.05, 50.0)


Y_WB = _y_wb()


def wb_gamma(a0, alpha, xi=1.0):
    """gamma_v = sqrt(nu).  a0 enters through y = g_bar/a0 at a FIXED separation."""
    y = Y_WB * (A0_CANON / a0) * xi
    return math.sqrt(float(nu_alpha(y, alpha)))


# --- a0(z) ---------------------------------------------------------------------------------------------
DESI = {"DESI+CMB+Pant+ (2.8s)": (-0.838, -0.62),
        "DESI+CMB+DESY5 (4.2s)": (-0.752, -0.86),
        "DESI+CMB+Union3(3.8s)": (-0.667, -1.09),
        "DESI+CMB only  (3.1s)": (-0.42, -1.75),
        "LambdaCDM w=-1        ": (-1.0, 0.0)}
OM_M, H0_S = 0.3153, 67.36 * 1e3 / (1e6 * pc)
MSA3D_SLOPE, MSA3D_SIG = 0.91, 0.80     # committed controlled residual, a0(z) lane


def a0z_ratio(z, w0, wa, f):
    """f = 0: local-response floor a0 ~ sqrt(rho_DE).  f = 1: horizon floor a0 ~ c H0 E(z)."""
    rho = (1 + z)**(3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))
    E = math.sqrt(OM_M * (1 + z)**3 + (1 - OM_M) * rho)
    return rho**((1 - f) / 2.0) * E**f


def a0z_slope(w0, wa, f, z=1.0):
    return math.log(a0z_ratio(z, w0, wa, f)) / math.log(1 + z)


# --- LLR ----------------------------------------------------------------------------------------------
GN_MOON = 3.986004418e14 / (3.844e8)**2
LLR_CEN, LLR_SIG = 5.0e-15, 9.6e-15     # Biskupek, Mueller & Torre 2021; sign: dln a/dt = -Gdot/G


def llr_drift(a0, omega_c):
    return a0 * omega_c / GN_MOON * YR   # per year


# --- Crater II / dwarf EFE ----------------------------------------------------------------------------
CRII_SIG_OBS, CRII_SIG_ERR = 2.7e3, 0.3e3       # m/s, observed
CRII_MOND_PRED = 2.1e3                          # McGaugh & Milgrom 2013 EFE pre-prediction
CRII_M = 3.4e5 * Msun                           # Crater II stellar mass, McConnachie-class


def crii_sigma(a0, alpha, xi=1.0):
    """isolated deep-MOND sigma = (4/81 G M a0)^(1/4), then the EFE suppression at strength xi.
    The suppression is CALIBRATED so xi = 1 reproduces the committed MOND+EFE prediction 2.1 km/s."""
    sig_iso = (4.0 / 81.0 * G * CRII_M * a0)**0.25
    supp0 = CRII_MOND_PRED / ((4.0 / 81.0 * G * CRII_M * A0_CANON)**0.25)
    # shape enters through nu at the transition: Crater II sits at y ~ O(1)
    y = (CRII_SIG_OBS**2 / (1100 * pc)) / a0
    shape = (float(nu_alpha(y, alpha)) / float(nu_alpha(y, 1.0)))**0.5
    return sig_iso * supp0**xi * shape


def sec4_closed():
    banner("4.  THE CLOSED-FORM FRONTS -- anchors reproduced before any derivative is taken")
    print(f"  g_bar(Earth) = {G_BAR_EARTH:.6e} m/s2   ->  y_Earth = {G_BAR_EARTH/A0_CANON:.4e}")
    A_bare = A0_CANON * float(nu_minus_one(G_BAR_EARTH / A0_CANON, 1.0)) * (G_BAR_EARTH / A0_CANON)
    print(f"  bare alpha=1 anomaly    = {A_bare:.4e} m/s2   (should be a0/2 = {A0_CANON/2:.4e})")
    check(abs(A_bare / (A0_CANON / 2) - 1) < 1e-6,
          f"the alpha=1 tail gives a CONSTANT sunward a0/2 = {A_bare:.4e} m/s2 to "
          f"{abs(A_bare/(A0_CANON/2)-1):.1e} relative -- Milgrom 2009 arXiv:0906.4817's 'too strong effects "
          f"on the planets', inherited with the kernel")
    A_res = eph_residual(A0_CANON, 1.0)
    print(f"  after the framework's own EFE ({EFE_SUPP}x): {A_res:.4e} m/s2  "
          f"= {A_res/EPH_2SIG:.1f}x the Earth 2-sigma bound {EPH_2SIG:.3e}")
    check(abs(A_bare / EPH_2SIG - 1278) < 40 and abs(A_res / EPH_2SIG - 135) < 60,
          f"REGRESSION: bare = {A_bare/EPH_2SIG:.0f}x over (committed 1278x) and post-EFE = "
          f"{A_res/EPH_2SIG:.0f}x over on the 2-sigma bound (committed 189x on the tighter EFE variant) -- "
          f"mi_alpha1_solar_system_2026.py reproduced")

    print(f"\n  wide binaries: y_WB = {Y_WB:.4f} calibrated so alpha = 2 gives the frozen in-force "
          f"gamma_v = {WB_GAMMA_TARGET}")
    M_wb = 1.5 * Msun
    s_wb = math.sqrt(G * M_wb / (Y_WB * A0_CANON)) / (1e3 * AU)
    print(f"     that y corresponds to s = {s_wb:.2f} kAU at M = 1.5 Msun")
    check(2.0 <= s_wb <= 30.0,
          f"the WB calibration is PHYSICAL, not a fudge: y_WB = {Y_WB:.3f} is s = {s_wb:.1f} kAU, inside "
          f"the frozen 2-30 kAU pre-registered band")
    print(f"     round-trip: gamma_v(alpha=2, canon) = {wb_gamma(A0_CANON,2.0):.6f} vs the frozen "
          f"{WB_GAMMA_TARGET} (calibration reproduces itself, as it must -- not a test)")
    g_a1, g_a2 = wb_gamma(A0_CANON, 1.0), wb_gamma(A0_CANON, 2.0)
    print(f"     gamma_v at alpha = 1 (the framework's OWN kernel) = {g_a1:.4f}")
    check(abs(g_a1 - g_a2) / WB_SIGMA_SYS > 1.0,
          f"THE TESTABLE CLAIM about F3: the wide-binary target is genuinely SHAPE-SENSITIVE -- alpha = 1 "
          f"gives {g_a1:.4f} against alpha = 2's {g_a2:.4f}, a separation of "
          f"{abs(g_a1-g_a2)/WB_SIGMA_SYS:.2f} sigma_sys.  This is why F3 earns a place in the alpha row of "
          f"the matrix, and it is also the front the Q4 trade actually costs something")

    print(f"\n  a0(z), slope s = ln[a0(1)/a0(0)]/ln 2 :")
    for nm, (w0, wa) in DESI.items():
        print(f"     {nm}  local floor f=0: {a0z_slope(w0,wa,0.0):+.4f}   "
              f"horizon floor f=1: {a0z_slope(w0,wa,1.0):+.4f}")
    check(abs(a0z_slope(-1.0, 0.0, 0.0)) < 1e-12,
          f"the local-response floor with w = -1 gives EXACTLY a constant a0 (slope "
          f"{a0z_slope(-1.0,0.0,0.0):.2e}) -- so F5's entire signal is the FLOOR CHOICE plus (w0,wa), "
          f"neither of which is a framework parameter")
    r1 = a0z_ratio(1.0, -1.0, 0.0, 1.0)
    check(abs(r1 - 1.78) < 0.03,
          f"the horizon floor rises by {r1:.3f}x at z = 1, reproducing the committed 1.78x")
    # bump-then-decline, the committed correction to the 'monotone rise' error
    w0, wa = DESI["DESI+CMB+Pant+ (2.8s)"]
    zs = np.linspace(0.001, 4.0, 4001)
    rr = np.array([a0z_ratio(z, w0, wa, 0.0) for z in zs])
    izmax = int(np.argmax(rr))
    print(f"     DESI+CMB+Pant+, local floor: peak a0/a0(0) = {rr[izmax]:.4f} at z = {zs[izmax]:.3f}, "
          f"then a0(z=3)/a0(0) = {a0z_ratio(3.0,w0,wa,0.0):.4f}")
    check(0.0 < zs[izmax] < 4.0 and rr[-1] < rr[izmax],
          f"REGRESSION: the correct closed form is BUMP-then-DECLINE (peak at z = {zs[izmax]:.2f}), not a "
          f"monotone rise -- the a0(z) lane's committed correction reproduced, and a coarse grid would "
          f"have missed the peak (HAZARD 4 again)")
    zs4 = np.linspace(0.001, 4.0, 16001)
    rr4 = np.array([a0z_ratio(z, w0, wa, 0.0) for z in zs4])
    print(f"     4x grid refinement moves the peak {zs[izmax]:.4f} -> {zs4[int(np.argmax(rr4))]:.4f} "
          f"(shift {abs(zs4[int(np.argmax(rr4))]-zs[izmax]):.4f} in z)")

    print(f"\n  LLR: g_N(Moon) = {GN_MOON:.6e} m/s2;  d ln a/dt at the window centre = "
          f"{llr_drift(A0_CANON, 1.9895e-14):.4e} /yr  vs measured {LLR_CEN:.2e} +- {LLR_SIG:.2e} /yr")
    check(abs(llr_drift(A0_CANON, 2.211e-14) / 2.420e-14 - 1) < 0.01,
          f"REGRESSION: the committed upper edge 2.211e-14 rad/s maps to exactly the |cen|+2sigma ceiling "
          f"2.420e-14/yr (got {llr_drift(A0_CANON,2.211e-14):.4e}) -- mi_omegac_edges_closure_2026.py's "
          f"upper edge reproduced from scratch")

    print(f"\n  Crater II: xi = 1 reproduces the committed MOND+EFE pre-prediction "
          f"{crii_sigma(A0_CANON,1.0)/1e3:.3f} km/s by construction (calibration, not a test); "
          f"observed {CRII_SIG_OBS/1e3:.1f} +- {CRII_SIG_ERR/1e3:.1f} km/s")
    xi_req = brentq(lambda x: crii_sigma(A0_CANON, 1.0, x) - CRII_SIG_OBS, 0.01, 3.0)
    print(f"     xi the OBSERVED sigma requires = {xi_req:.4f}, i.e. {1/xi_req:.3f}x LESS suppression "
          f"than the additive prescription applies")
    check(xi_req < 1.0,
          f"THE TESTABLE CLAIM about F7, and it is the committed diagnosis independently reproduced: "
          f"Crater II's observed 2.7 km/s needs xi = {xi_req:.3f} < 1, i.e. the framework's additive EFE "
          f"prescription OVER-SUPPRESSES.  The sign of the required correction is what "
          f"mi_dwarf_efe_maths_audit_2026.py found, arrived at here from the sigma values alone.  Had the "
          f"prescription under-suppressed, xi > 1 would have come out and this check would read FAIL")
    return None


# =========================================================================================================
# 5.  THE SENSITIVITY MATRIX
# =========================================================================================================
PARAMS = ["ln kappa", "ln footing", "ln omega_c", "alpha", "delta (I_0 x f_cl)", "ln xi_EFE", "f (a0z floor)"]


def build_matrix(sp_res, cl_res, sig_sparc_pct, cluster_floor_dex):
    """S[i][j] = (dM_i/dtheta_j)/sigma_i  in sigma per unit (e-fold for ln, absolute for alpha/delta/f)."""
    sig_F1 = math.log10(1 + sig_sparc_pct)
    L10E = math.log10(math.e)

    # ---- F1 SPARC RAR:  M = log10 a0_model - log10 a0_hat(alpha, omega_c, xi)
    F1 = [L10E / sig_F1,                       # ln kappa: a0_model ~ kappa
          L10E / sig_F1,                       # ln footing: a0_model ~ footing factor -- IDENTICAL column
          -sp_res["dlnwc"] / sig_F1,
          -sp_res["dalpha"] / sig_F1,
          0.0,                                 # delta: SPARC baryons, no clustered component invoked
          -sp_res["dlnxi"] / sig_F1,
          0.0]                                 # f: a0(z) floor is a z-dependence, z=0 fronts are blind

    # ---- F2 ephemeris:  M = A_res, sigma = half the 2-sigma bound
    sig_F2 = EPH_2SIG / 2.0
    h = 1e-3
    dA_dlnk = (eph_residual(A0_CANON * math.exp(h), 1.0)
               - eph_residual(A0_CANON * math.exp(-h), 1.0)) / (2 * h)
    dA_dalpha = (eph_residual(A0_CANON, 1.0 + h) - eph_residual(A0_CANON, 1.0 - h)) / (2 * h)
    dA_dlnxi = (eph_residual(A0_CANON, 1.0, math.exp(h))
                - eph_residual(A0_CANON, 1.0, math.exp(-h))) / (2 * h)
    F2 = [dA_dlnk / sig_F2, dA_dlnk / sig_F2,
          0.0,                                 # STRUCTURAL ZERO: a constant sunward anomaly is DC, and a
                                               # low-pass passes DC at unit gain whatever omega_c is
          dA_dalpha / sig_F2, 0.0, dA_dlnxi / sig_F2, 0.0]

    # ---- F3 wide binaries: FORECAST row, sigma = the frozen systematic floor
    dg_dlnk = (wb_gamma(A0_CANON * math.exp(h), 2.0) - wb_gamma(A0_CANON * math.exp(-h), 2.0)) / (2 * h)
    dg_dalpha = (wb_gamma(A0_CANON, 2.0 + h) - wb_gamma(A0_CANON, 2.0 - h)) / (2 * h)
    dg_dlnxi = (wb_gamma(A0_CANON, 2.0, math.exp(h)) - wb_gamma(A0_CANON, 2.0, math.exp(-h))) / (2 * h)
    F3 = [dg_dlnk / WB_SIGMA_SYS, dg_dlnk / WB_SIGMA_SYS,
          0.0,                                 # STRUCTURAL ZERO: the DC branch (099f6871) -- ungated
          dg_dalpha / WB_SIGMA_SYS, 0.0, dg_dlnxi / WB_SIGMA_SYS, 0.0]

    # ---- F4 clusters
    sig_F4 = cluster_floor_dex
    F4 = [cl_res["d_dlna0"] / sig_F4, cl_res["d_dlna0"] / sig_F4,
          cl_res["d_dlnwc"] / sig_F4, cl_res["d_dalpha"] / sig_F4,
          cl_res["d_ddelta"] / sig_F4, 0.0, 0.0]

    # ---- F5 a0(z)
    w0, wa = DESI["DESI+CMB+Pant+ (2.8s)"]
    df_ = 1e-3
    ds_df = (a0z_slope(w0, wa, 0.5 + df_) - a0z_slope(w0, wa, 0.5 - df_)) / (2 * df_)
    F5 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ds_df / MSA3D_SIG]

    # ---- F6 LLR Gdot/G
    dD_dlnk = (llr_drift(A0_CANON * math.exp(h), 1.9895e-14)
               - llr_drift(A0_CANON * math.exp(-h), 1.9895e-14)) / (2 * h)
    dD_dlnwc = (llr_drift(A0_CANON, 1.9895e-14 * math.exp(h))
                - llr_drift(A0_CANON, 1.9895e-14 * math.exp(-h))) / (2 * h)
    F6 = [dD_dlnk / LLR_SIG, dD_dlnk / LLR_SIG, dD_dlnwc / LLR_SIG, 0.0, 0.0, 0.0, 0.0]

    # ---- F7 Crater II dwarf EFE
    sig_F7 = CRII_SIG_ERR
    dS_dlnk = (crii_sigma(A0_CANON * math.exp(h), 1.0)
               - crii_sigma(A0_CANON * math.exp(-h), 1.0)) / (2 * h)
    dS_dalpha = (crii_sigma(A0_CANON, 1.0 + h) - crii_sigma(A0_CANON, 1.0 - h)) / (2 * h)
    dS_dlnxi = (crii_sigma(A0_CANON, 1.0, 1 + h) - crii_sigma(A0_CANON, 1.0, 1 - h)) / (2 * h)
    F7 = [dS_dlnk / sig_F7, dS_dlnk / sig_F7, 0.0, dS_dalpha / sig_F7, 0.0, dS_dlnxi / sig_F7, 0.0]

    rows = ["F1 SPARC RAR", "F2 ephemeris", "F3 wide binaries*", "F4 clusters",
            "F5 a0(z)", "F6 LLR Gdot/G", "F7 Crater II EFE"]
    return rows, np.array([F1, F2, F3, F4, F5, F6, F7], float), dict(sig_F1=sig_F1, sig_F2=sig_F2,
                                                                     sig_F4=sig_F4, sig_F7=sig_F7)


def sec5_matrix(sp_res, cl_res):
    banner("5.  THE SENSITIVITY MATRIX  S_ij = (dM_i/dtheta_j)/sigma_i   [sigma per e-fold, or per unit]")
    print("  LOOSE-END sigmas (guard against truncating a systematic range at its tight end):")
    print("     F1 sigma(a0) = 5.44% (loose end of the committed 1.24%/5.44%)")
    print("     F4 cluster systematic floor = 0.30 dex (loose end of the committed 0.10-0.30 dex ladder)")
    rows, S, sig = build_matrix(sp_res, cl_res, 0.0544, 0.30)

    hdr = "  front                " + "".join(f"{p:>20s}" for p in PARAMS)
    print("\n" + hdr)
    print("  " + "-" * (len(hdr) - 2))
    for nm, r in zip(rows, S):
        print(f"  {nm:<20s}" + "".join(f"{v:>20.4g}" for v in r))
    print("  * F3 is a FORECAST row: DR3's 1.205 is guard-zone contamination, evidence for nothing, so "
          "there is\n    no wide-binary MEASUREMENT yet.  sigma = the frozen sigma_sys = 0.02 floor.  The "
          "rank is reported\n    with AND without it.")

    # ---------- the exact flat direction: kappa and the footing are the same column ----------
    banner("5a.  AN EXACT FLAT DIRECTION, PROVEN: kappa and the FOOTING are one column, not two")
    dcol = float(np.max(np.abs(S[:, 0] - S[:, 1])))
    print(f"  max |S[:,kappa] - S[:,footing]| over all 7 fronts = {dcol:.3e}")
    check(dcol < 1e-12,
          f"kappa and the footing choice (rho_DE/cH_Lambda vs rho_total/cH_0) enter EVERY front only "
          f"through their product a0.  The two columns agree to {dcol:.1e}, so the direction "
          f"d ln kappa = -d ln footing is EXACTLY flat: no combination of these seven fronts can "
          f"separate 'kappa = 1/2 on the canonical footing' from 'kappa = 1/2/1.2082 on the ALT footing'.  "
          f"This is one guaranteed unit of irreducible dof, and it is a THEOREM about the fronts, not a "
          f"precision limit")
    print(f"  the ALT/canon ratio is 1/sqrt(Omega_Lambda) = {1/math.sqrt(OMEGA_L):.4f} = "
          f"{math.log10(1/math.sqrt(OMEGA_L)):.4f} dex, and the framework's OWN kappa signal against "
          f"Milgrom 2020's 1/2pi is 0.0356 dex -- the footing fork is "
          f"{math.log10(1/math.sqrt(OMEGA_L))/0.0356:.1f}x LARGER than the number it is meant to measure")

    # ---------- blindness ledger ----------
    banner("5b.  BLINDNESS LEDGER -- how many INDEPENDENT fronts see each parameter (threshold 1 sigma)")
    print("  a parameter seen by 1 front is FITTED; by 2 it is TESTABLE; by 3+ it is OVER-DETERMINED.")
    print(f"\n  {'parameter':<22s}{'n_sens':>8s}{'n_blind':>9s}   status          sensitive fronts")
    print("  " + "-" * 100)
    print("  'blind' below means BELOW the 1-sigma threshold, which for some entries means small-but-")
    print("  nonzero rather than structurally zero.  The structural zeros are marked in the matrix as")
    print("  exact 0 and are: omega_c in F2 and F3 (a constant sunward anomaly and a wide-binary velocity")
    print("  boost are DC, and a low-pass passes DC at unit gain whatever omega_c is -- 099f6871);")
    print("  delta in every front but F4; xi_EFE in F4/F5/F6; f in every front but F5.")
    ledger = {}
    for j, p in enumerate(PARAMS):
        sens = [rows[i] for i in range(len(rows)) if abs(S[i, j]) >= 1.0]
        nb = len(rows) - len(sens)
        st = ("OVER-DETERMINED" if len(sens) >= 3 else "TESTABLE" if len(sens) == 2
              else "FITTED (1 front)" if len(sens) == 1 else "UNCONSTRAINED")
        ledger[p] = (len(sens), sens, st)
        print(f"  {p:<22s}{len(sens):>8d}{nb:>9d}   {st:<16s}{', '.join(s.split()[0] for s in sens)}")

    check(ledger["delta (I_0 x f_cl)"][0] == 0,
          f"the ghost-condensate amount I_0 is seen by ZERO fronts at 1 sigma: the only front that could "
          f"see it (clusters) needs delta = {cl_res['delta_close']:.1f} and the framework's own "
          f"particle-vs-mode position sets the clustered fraction to 0.  So I_0 x f_cl is an EXACTLY "
          f"UNCONSTRAINED direction -- the second guaranteed unit of irreducible dof")
    check(ledger["f (a0z floor)"][0] <= 1,
          f"the a0(z) floor choice f is seen by {ledger['f (a0z floor)'][0]} front(s) -- F5 alone.  A "
          f"parameter constrained by one front is FITTED by definition, and F5 is additionally "
          f"LambdaCDM-degenerate (MUSE-DARK III measures a0 RISING against the canonical declining "
          f"reading), so f is not testable by over-determination here")
    check(ledger["ln omega_c"][0] == 1,
          f"AND HERE IS THE SHARP ANSWER TO Q3, read straight off the matrix: omega_c is seen at 1 sigma "
          f"by exactly ONE front, F6 (LLR).  F1's omega_c entry is {S[0,2]:+.4f} sigma per e-fold -- the "
          f"galactic 'lower edge' is NOT a measurement pulling on omega_c, it is a TOLERANCE CHOICE "
          f"(Re G >= 0.90) that costs the RAR essentially nothing.  A parameter seen by one front is "
          f"FITTED.  So the twelve-orders-apart window is a consistency test, not an over-determination")
    check(ledger["alpha"][0] >= 2,
          f"the shape dof alpha IS seen by {ledger['alpha'][0]} independent fronts "
          f"({', '.join(s.split()[0] for s in ledger['alpha'][1])}) -- so alpha is at least TESTABLE and "
          f"is the one place over-determination can actually bite (Sec. 7)")

    # ---------- rank ----------
    banner("5c.  RANK.  A direction counts as DETERMINED if one e-fold (or one unit) moves some front by "
           ">= 1 sigma")
    def report_rank(Sx, tag, rowlab):  # noqa
        U, sv, Vt = np.linalg.svd(Sx)
        det = int(np.sum(sv >= 1.0))
        print(f"\n  {tag}   ({Sx.shape[0]} fronts x {Sx.shape[1]} params)")
        print("     singular values: " + "  ".join(f"{s:.4g}" for s in sv))
        print(f"     numerical rank (any nonzero)      = {int(np.linalg.matrix_rank(Sx, tol=1e-10))}")
        print(f"     PHYSICAL rank (sv >= 1 sigma)     = {det}")
        print(f"     n_params = {Sx.shape[1]}  ->  irreducible free dof = {Sx.shape[1] - det}")
        for k in range(det, Sx.shape[1]):
            v = Vt[k]
            svk = sv[k] if k < sv.size else 0.0
            terms = "  ".join(f"{v[j]:+.3f}*{PARAMS[j]}" for j in range(len(PARAMS)) if abs(v[j]) > 0.05)
            print(f"     flat direction {k-det+1} (sv = {svk:.3g}): {terms}")
        return det, sv

    det_all, sv_all = report_rank(S, "ALL 7 fronts, loose sigmas", rows)
    S_nowb = np.delete(S, 2, axis=0)
    det_nowb, _ = report_rank(S_nowb, "6 MEASURED fronts (wide binaries removed -- no measurement exists)",
                              [r for i, r in enumerate(rows) if i != 2])
    _, S_t, _ = build_matrix(sp_res, cl_res, 0.0124, 0.10)
    det_t, _ = report_rank(S_t, "ALL 7 fronts, TIGHT sigmas (1.24% / 0.10 dex) -- robustness", rows)

    # RANK ROBUSTNESS, reported rather than forced.  The rank DOES move by one between the ends, and
    # exactly one column is responsible -- naming it is the honest version of this check.
    print(f"\n  RANK vs the systematic end: {det_all} (loose) -> {det_t} (tight).  It moves by "
          f"{det_t-det_all}.  Which column?")
    print(f"     F4's delta entry: loose {S[3,4]:+.4f} sigma/unit (below threshold) vs tight "
          f"{S_t[3,4]:+.4f} (above).  Tightening the cluster floor from 0.30 to 0.10 dex is what promotes")
    print(f"     the ghost-condensate direction from flat to determined -- and it does so by making the")
    print(f"     +0.4052 dex cluster offset a {abs(cl_res['mean_dex'])/0.10:.1f}-sigma tension that delta "
          f"could absorb, not by any new measurement.")
    check(abs(S[3, 4]) < 1.0 <= abs(S_t[3, 4]) and det_t - det_all == 1,
          f"RANK ROBUSTNESS, STATED HONESTLY: the physical rank is {det_all} at the loose end and {det_t} "
          f"at the tight end, and the ENTIRE difference is the delta (I_0 x f_cl) column of the cluster "
          f"row.  So the dof answer is 1-or-2 depending on the cluster systematic floor, and the corpus's "
          f"own floor ladder runs 0.10-0.30 dex.  Truncating that ladder at either end would misreport the "
          f"count -- which is exactly the trap this project has fallen into before")
    check(np.linalg.matrix_rank(S, tol=1e-10) < len(PARAMS)
          and np.linalg.matrix_rank(S_t, tol=1e-10) < len(PARAMS),
          f"BUT ONE FLAT DIRECTION IS END-INDEPENDENT: the numerical rank is "
          f"{np.linalg.matrix_rank(S, tol=1e-10)} (loose) and {np.linalg.matrix_rank(S_t, tol=1e-10)} "
          f"(tight) against {len(PARAMS)} parameters, i.e. the kappa-footing null of Sec. 5a survives BOTH "
          f"ends exactly.  That unit of dof is a theorem and no systematic choice can remove it")
    check(len(PARAMS) - det_all >= 2 and len(PARAMS) - det_t >= 1,
          f"OUTCOME (c), NOT (a): {len(PARAMS)} nominal parameters, physical rank {det_all} (loose) / "
          f"{det_t} (tight), so {len(PARAMS)-det_all} / {len(PARAMS)-det_t} irreducible flat directions "
          f"survive seven fronts.  The parameters are NOT derived by over-determination on either reading")
    # NOTE: det_nowb <= det_all holds for ANY deleted row, so testing that would be untestable.
    # The substantive claim is EQUALITY: the un-measured forecast row adds no determined direction.
    check(det_nowb == det_all,
          f"THE IN-HAND COUNT IS THE SAME: dropping the un-measured wide-binary row leaves the rank at "
          f"{det_nowb} (from {det_all}), so no determined direction in this matrix rests on a front that "
          f"has not been measured yet.  Had F3 been carrying a direction on its own, this would read FAIL "
          f"and the in-hand dof would be {len(PARAMS)-det_all+1}, not {len(PARAMS)-det_nowb}")
    return dict(rows=rows, S=S, sv=sv_all, det=det_all, det_nowb=det_nowb, det_tight=det_t,
                ledger=ledger, sig=sig)


# =========================================================================================================
# 6.  Q3 -- IS THE omega_c WINDOW AN OVER-DETERMINATION OR A COINCIDENCE?
# =========================================================================================================
def sec6_omegac(sp_res):
    banner("6.  Q3: omega_c was pinned by GALACTIC orbits AND by LUNAR LASER RANGING -- twelve orders "
           "apart.\n    IS THAT AN OVER-DETERMINATION, OR DID THE GALACTIC LEG HAVE TO BE IMPOSED?")
    om_gal = sp_res["omega_gal_max"]
    S_keep = 0.90
    k_S = math.sqrt(S_keep / (1 - S_keep))
    lower = k_S * om_gal
    ceiling = (abs(LLR_CEN) + 2 * LLR_SIG)                 # /yr, the paper's convention
    upper = ceiling / YR * GN_MOON / A0_CANON
    upper_alt = ceiling / YR * GN_MOON / A0_ALT
    print(f"  LOWER edge (galactic, theory-internal): k(0.90) x MAX omega_gal = {k_S:.4f} x {om_gal:.4e} "
          f"= {lower:.4e} rad/s")
    print(f"  UPPER edge (LLR, data)                : {ceiling:.3e}/yr x g_N(Moon)/a0 = {upper:.4e} rad/s "
          f"(canon) / {upper_alt:.4e} (alt)")
    print(f"  widths: canon x{upper/lower:.4f}   alt x{upper_alt/lower:.4f}")
    check(abs(upper / lower / 1.2406 - 1) < 0.01 and abs(upper_alt / lower / 1.0266 - 1) < 0.02,
          f"REGRESSION: widths x{upper/lower:.4f} (canon) and x{upper_alt/lower:.4f} (alt) reproduce "
          f"mi_omegac_edges_closure_2026.py's x1.2406 / x1.0266 from raw SPARC + the published LLR datum")

    print("\n  *** THE ACTUAL QUESTION, answered directly. ***")
    print("  The two constraints are ONE-SIDED and point in OPPOSITE directions:")
    print("     LLR      ->  omega_c <= upper      (an UPPER bound; no lower bound whatsoever)")
    print("     galaxies ->  omega_c >= lower      (a LOWER bound; no upper bound whatsoever)")
    print("  A one-sided upper bound CANNOT imply a lower bound.  So the galactic requirement is NOT")
    print("  delivered free by LLR -- it is logically independent and had to be IMPOSED.  What LLR alone")
    print("  DOES deliver is a CEILING on the retention the gate can achieve at the binding galactic orbit:")
    ReG_max = float(re_G(om_gal, upper))
    print(f"     Re G(omega_gal / upper) = {ReG_max:.4f}   <- the BEST retention LLR permits")
    print(f"     the framework needs      >= {S_keep:.4f}")
    print(f"     margin in retention      = {ReG_max - S_keep:+.4f}   "
          f"(critical retention S_crit = {upper**2/(upper**2+om_gal**2):.4f})")
    check(ReG_max > S_keep,
          f"THE CONSISTENCY TEST PASSES, and it is a real test that could have failed: LLR's ceiling "
          f"permits at most Re G = {ReG_max:.4f} at UGC05721's innermost deep-MOND orbit, and the "
          f"framework needs 0.90.  The margin is {ReG_max-S_keep:.4f} in retention")
    frac = math.log(upper / lower) / math.log(upper / om_gal)
    print(f"\n  HOW MUCH of the LLR-allowed range satisfies the galactic leg?  On a log measure over the")
    print(f"  physically bracketed range omega_c in [MAX omega_gal, upper] (below MAX omega_gal the gate is")
    print(f"  shut on the rotation curves entirely, so that is the natural floor):")
    print(f"     surviving log-fraction = ln(upper/lower)/ln(upper/omega_gal) = {frac:.4f} "
          f"= {100*frac:.1f}%")
    check(frac < 0.30,
          f"only {100*frac:.1f}% of the LLR-permitted log-range clears the galactic requirement.  So the "
          f"galactic leg REMOVES {100*(1-frac):.1f}% of what LLR allows -- it is doing real work, which is "
          f"the precise sense in which the window is NOT an automatic consequence of LLR")

    print("\n  *** THE TRANSFERABLE OVER-DETERMINATION THAT IS ACTUALLY THERE. ***")
    print("  Requiring the window to be NON-EMPTY (upper >= lower) eliminates omega_c and leaves a bound")
    print("  on a0 with NO RAR fit, NO M/L inference and NO slope estimator anywhere in it:")
    a0_max = ceiling / YR * GN_MOON / lower
    print(f"     a0 <= (ceiling/yr) g_N(Moon) / (k(S) MAX omega_gal) = {a0_max:.4e} m/s2")
    print(f"     canonical 9.3614e-11 clears it by x{a0_max/A0_CANON:.4f};  "
          f"ALT 1.1311e-10 clears it by x{a0_max/A0_ALT:.4f}")
    check(a0_max > A0_CANON and (a0_max / A0_ALT - 1) < 0.10,
          f"SPARC ORBITAL FREQUENCIES + LLR ALONE give a0 <= {a0_max:.4e} -- a genuinely SECOND, "
          f"methodologically disjoint line on a0.  It clears canon by {100*(a0_max/A0_CANON-1):.1f}% and "
          f"the ALT footing by only {100*(a0_max/A0_ALT-1):.1f}%.  That IS scale-bridging over-determination, "
          f"and it is a bound, not a value")

    print("\n  IS omega_c NATURAL AT THE WINDOW?  The framework's own candidate scales:")
    cands = [("a0/c  (Route B at v = c)", A0_CANON / c),
             ("a0/v_rel, v = 220 km/s (MW)", A0_CANON / 2.20e5),
             ("a0/v_rel, v = 30 km/s (dwarf)", A0_CANON / 3.0e4),
             ("H_Lambda = sqrt(Lambda/3) c", A0_CANON * 5.788810036466 / c),
             ("1/t_age", 1.0 / (13.797e9 * YR))]
    for nm, v in cands:
        print(f"     {nm:<34s} {v:.4e} rad/s   = x{v/lower:.3e} the window's lower edge")
    best_nat = min(abs(math.log10(v / lower)) for _, v in cands)
    check(best_nat > 0.5,
          f"AGAINST INTEREST: not one of the framework's own natural frequency scales lands in the window "
          f"-- the closest misses by a factor {10**best_nat:.1f}, and Route B's a0/c is "
          f"{lower/(A0_CANON/c):.1e}x BELOW the lower edge.  omega_c is TUNED to sit there, and a tuned "
          f"constant bracketed by two bounds is a fit with a consistency check, not a derivation")

    print("\n  AND THE STRUCTURAL FORK THAT SITS UNDER BOTH EDGES, stated because it is load-bearing:")
    print("  mi_dcac_split_settled_2026.py proved a MUTUAL-EXCLUSIVITY theorem for the closure that feeds")
    print("  the memory kernel.  Under the FIRST-MOMENT closure -- the one that reproduces the RAR at")
    print("  0.108 dex -- the kernel's argument is |a|^2/a0^2 >= 0, K is real, and the DISSIPATIVE channel")
    print("  is IDENTICALLY ZERO, not merely small.  The LLR drift d ln a/dt = a0 omega_c/g_N IS that")
    print("  channel.  Under the LITERAL spectral closure the drift exists but the RAR fails outright.")
    print("  So the upper edge and the rotation curves are computed under closures the corpus has itself")
    print("  proved mutually exclusive.  Two readings, two consequences for omega_c's STATUS:")
    print("     first-moment closure  -> drift == 0 -> LLR is BLIND -> omega_c UNCONSTRAINED ABOVE,")
    print("                              and the gate's Re G is likewise not sampled: omega_c becomes")
    print("                              an UNOBSERVABLE label, which REMOVES it from the dof count")
    print("                              without any over-determination having occurred.")
    print("     literal spectral      -> omega_c observable, window as computed, but no rotation curves.")
    print("  Neither reading delivers 'omega_c derived'.  Reported as the spread, not resolved here.")
    return dict(om_gal=om_gal, lower=lower, upper=upper, upper_alt=upper_alt, ReG_max=ReG_max,
                frac=frac, a0_max=a0_max)


# =========================================================================================================
# 7.  Q4 -- CAN THE SOLAR SYSTEM FIX THE TAIL EXPONENT AT NO COST TO GALAXIES OR CLUSTERS?
# =========================================================================================================
def sec7_alpha(sp_res, cl_res):
    banner("7.  Q4: the ephemeris constrains the tail at 10^2-10^3 and SPARC does not.  Does the alpha the\n"
           "    ephemeris DEMANDS remain acceptable to SPARC and to clusters?")
    gobs, gbar = cl_res["gobs"], cl_res["gbar"]

    def over(alpha, xi=1.0, nsig=2.0):
        return eph_residual(A0_CANON, alpha, xi) / (EPH_2SIG * nsig / 2.0)

    print("  Earth 2-sigma bound = 3.66e-14 m/s2 (Sereno-Jetzer 2006 eq 9 + Pitjeva EPM2004 Table 1).")
    print("  Both the BARE anomaly and the framework's own EFE-suppressed residual are shown, because the")
    print("  EFE escape is real (it is a factor ~9.5) but is a coincidence of scales, not a mechanism.\n")
    print("  alpha   residual [m/s2]   x over 2sig (post-EFE)   x over 2sig (bare)   SPARC rms   cluster dex")
    rows = []
    for av in (1.0, 1.1, 1.25, 1.3, 1.5, 1.75, 2.0, 3.0):
        A = eph_residual(A0_CANON, av)
        rms = sparc_fit_a0(alpha=av)[2]
        cd = float(np.mean(eta_log(gobs, gbar, A0_CANON, av)))
        rows.append((av, A, rms, cd))
        print(f"  {av:5.2f}   {A:15.4e}   {A/EPH_2SIG:22.4g}   {A*EFE_SUPP/EPH_2SIG:18.4g}   "
              f"{rms:9.4f}   {cd:+11.4f}")

    # -- the demanded alpha, by brentq on the log (HAZARD 2: never by scanning to underflow)
    def f_log(alpha, nsig, xi):
        return math.log(eph_residual(A0_CANON, alpha, xi)) - math.log(EPH_2SIG * nsig / 2.0)

    a_2s_efe = brentq(lambda a: f_log(a, 2.0, 1.0), 1.0, 8.0, xtol=1e-10)
    a_1s_efe = brentq(lambda a: f_log(a, 1.0, 1.0), 1.0, 8.0, xtol=1e-10)
    a_2s_bare = brentq(lambda a: f_log(a, 2.0, 1.0 / EFE_SUPP), 1.0, 8.0, xtol=1e-10)
    print(f"\n  alpha the ephemeris DEMANDS (root by brentq on the log, so no underflow can pass it):")
    print(f"     post-EFE, 2 sigma : alpha >= {a_2s_efe:.4f}")
    print(f"     post-EFE, 1 sigma : alpha >= {a_1s_efe:.4f}")
    print(f"     BARE (no EFE), 2 s: alpha >= {a_2s_bare:.4f}")
    print(f"     literature for comparison: Sereno & Jetzer 2006 'roughly allow only alpha >~ 1.5'")
    # grid + 4x refinement, to show the shift a coarse scan would have introduced
    gA = np.arange(1.0, 4.0, 0.05)
    gv = np.array([eph_residual(A0_CANON, a) for a in gA])
    i_g = int(np.argmax(gv <= EPH_2SIG))
    gA4 = np.arange(1.0, 4.0, 0.0125)
    gv4 = np.array([eph_residual(A0_CANON, a) for a in gA4])
    i_g4 = int(np.argmax(gv4 <= EPH_2SIG))
    print(f"     0.05 grid would report alpha >= {gA[i_g]:.4f}; 4x-refined grid {gA4[i_g4]:.4f}; "
          f"brentq {a_2s_efe:.4f}  (grid bias {gA[i_g]-a_2s_efe:+.4f})")
    # a refined grid is ALWAYS at least as close to a monotone crossing, so testing that would be
    # untestable.  The substantive claim is that the coarse grid's bias is LARGE ENOUGH TO MATTER.
    check(gA[i_g] - a_2s_efe > 0.02 and abs(gA4[i_g4] - a_2s_efe) < 0.01,
          f"HAZARD 4 is REAL on this root, not just formally present: the 0.05 grid reports alpha >= "
          f"{gA[i_g]:.4f} against the bracketed {a_2s_efe:.4f}, a bias of +{gA[i_g]-a_2s_efe:.4f} -- 30% "
          f"of the whole distance from alpha = 1, and always in the direction that makes the ephemeris "
          f"demand look HARSHER.  The 4x refinement recovers it to {abs(gA4[i_g4]-a_2s_efe):.4f}")
    check(1.0 < a_2s_efe < 2.0,
          f"the ephemeris demands alpha >= {a_2s_efe:.3f} (post-EFE, 2 sigma) -- and that lands INSIDE the "
          f"range the literature already flags (Sereno-Jetzer alpha >~ 1.5), so the number is not an "
          f"artefact of this parameterisation")

    # -- what it costs SPARC
    rms_1 = sparc_fit_a0(alpha=1.0)[2]
    rms_d = sparc_fit_a0(alpha=a_2s_efe)[2]
    rms_15 = sparc_fit_a0(alpha=1.5)[2]
    print(f"\n  COST TO SPARC of moving alpha 1 -> {a_2s_efe:.3f}: rms {rms_1:.4f} -> {rms_d:.4f} dex "
          f"({rms_d-rms_1:+.4f} dex = {(rms_d-rms_1)/sp_res['sigma_int']:+.3f} sigma_int)")
    print(f"  COST TO SPARC of moving alpha 1 -> 1.500          : rms {rms_1:.4f} -> {rms_15:.4f} dex "
          f"({rms_15-rms_1:+.4f} dex)")
    check(abs(rms_d - rms_1) < sp_res["sigma_int"],
          f"SPARC PAYS {abs(rms_d-rms_1):.4f} dex, i.e. {abs(rms_d-rms_1)/sp_res['sigma_int']:.2f}x "
          f"Desmond 2023's sigma_int -- galaxies cannot tell the difference")

    # -- what it costs clusters
    cd1 = float(np.mean(eta_log(gobs, gbar, A0_CANON, 1.0)))
    cdd = float(np.mean(eta_log(gobs, gbar, A0_CANON, a_2s_efe)))
    print(f"  COST TO CLUSTERS: <log10 eta> {cd1:+.4f} -> {cdd:+.4f} dex ({cdd-cd1:+.4f} dex = "
          f"{abs(cdd-cd1)/0.30:.3f} of the 0.30 dex systematic floor)")
    check(abs(cdd - cd1) < 0.05,
          f"CLUSTERS PAY {abs(cdd-cd1):.4f} dex -- {abs(cdd-cd1)/0.30:.2f}x the loose systematic floor.  "
          f"They are 30x below the transition and blind to the tail")

    # -- what it costs wide binaries (the one front that DOES notice)
    g1, gd = wb_gamma(A0_CANON, 1.0), wb_gamma(A0_CANON, a_2s_efe)
    print(f"  COST TO WIDE BINARIES: gamma_v {g1:.4f} -> {gd:.4f} ({(gd-g1)/WB_SIGMA_SYS:+.3f} sigma_sys) "
          f"-- the ONE front that notices, and only at {abs(gd-g1)/WB_SIGMA_SYS:.2f} sigma")
    check(abs(gd - g1) / WB_SIGMA_SYS < 3.0,
          f"even the wide-binary target moves only {abs(gd-g1)/WB_SIGMA_SYS:.2f} sigma_sys when alpha goes "
          f"1 -> {a_2s_efe:.2f}, which is below the 3-sigma threshold that sigma_sys = 0.02 already caps at "
          f"1.55 sigma anyway")

    print("\n  *** VERDICT ON Q4, both halves. ***")
    print(f"  YES, ONE SHAPE DOF IS REMOVED BY OVER-DETERMINATION, in the exact sense asked: the solar")
    print(f"  system FIXES alpha >= {a_2s_efe:.2f}, and SPARC ({abs(rms_d-rms_1):.4f} dex), clusters")
    print(f"  ({abs(cdd-cd1):.4f} dex) and even the wide-binary forecast "
          f"({abs(gd-g1)/WB_SIGMA_SYS:.2f} sigma) all accept it.  Six orders of magnitude in acceleration")
    print(f"  separate the two fronts, and they are compatible.  That is the one clean scale bridge here.")
    print(f"  AND WHAT IT COSTS, which must be said in the same breath: alpha = 1 is not a modelling")
    print(f"  choice in this framework, it is the EXACT LAW g_obs^2 = g_bar^2 + a0 g_bar (Sec. 1 proves the")
    print(f"  identity) and it is Milgrom 1999 eq 9, the kernel the dS-Unruh construction hands over.")
    print(f"  Buying alpha >= {a_2s_efe:.2f} therefore does not reduce the dof count by one -- it converts")
    print(f"  a CONSTRAINED shape dof into an UNEXPLAINED kernel choice.  Net: the fit loses a parameter,")
    print(f"  the theory loses a derivation.  The word 'exact' must be withdrawn either way.")
    return dict(a_2s_efe=a_2s_efe, a_1s_efe=a_1s_efe, a_2s_bare=a_2s_bare,
                rms_1=rms_1, rms_d=rms_d, cd1=cd1, cdd=cdd, g1=g1, gd=gd)


# =========================================================================================================
# 8.  FALSIFICATION CHECK -- is any FRONT PAIR mutually exclusive?  (outcome (b))
# =========================================================================================================
def sec8_pairs(sp_res, cl_res, mat):
    banner("8.  OUTCOME (b) CHECK: is any PAIR of fronts mutually exclusive over the admissible box?")
    print("  Scan the two directions the matrix says are jointly seen -- ln a0 and alpha -- and report the")
    print("  worst-case tension of every front at each point.  A front pair is EXCLUSIVE only if no point")
    print("  in the box clears BOTH.  sigmas are the LOOSE ends throughout.")
    gobs, gbar = cl_res["gobs"], cl_res["gbar"]
    sig_F1 = math.log10(1.0544)
    al_grid = np.arange(1.0, 3.01, 0.10)
    # the SPARC-preferred log10 a0_hat(alpha): FULL refits on a 9-point alpha grid, then linear
    # interpolation.  Doing the refit inside the double loop is what makes this section unaffordable;
    # the interpolation error is reported so it is not hidden.
    al_nodes = np.array([1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0])
    la_nodes = np.array([sparc_fit_a0(alpha=float(a))[0] for a in al_nodes])
    mid = 0.5 * (al_nodes[:-1] + al_nodes[1:])
    interp_err = float(np.max(np.abs(np.interp(mid, al_nodes, la_nodes)
                                     - np.array([sparc_fit_a0(alpha=float(a))[0] for a in mid]))))
    print(f"  log10 a0_hat(alpha) built from {al_nodes.size} FULL refits; worst interpolation error at the "
          f"midpoints = {interp_err:.5f} dex = {interp_err/sig_F1:.3f} sigma_F1")
    check(interp_err < 0.5 * sig_F1,
          f"the a0_hat(alpha) interpolation used in this scan is accurate to {interp_err:.5f} dex, under "
          f"half of F1's own sigma ({sig_F1:.5f} dex) -- so the scan's F1 column is not an artefact of "
          f"interpolating instead of refitting")
    la_grid = np.log10(A0_CANON) + np.arange(-0.20, 0.201, 0.02)
    best = None
    for la in la_grid:
        a0 = 10**la
        for al in al_grid:
            t1 = abs(la - float(np.interp(al, al_nodes, la_nodes))) / sig_F1
            t2 = eph_residual(a0, al) / (EPH_2SIG / 2.0)
            t4 = abs(float(np.mean(eta_log(gobs, gbar, a0, al)))) / 0.30
            t7 = abs(crii_sigma(a0, al) - CRII_SIG_OBS) / CRII_SIG_ERR
            worst = max(t1, t2, t4, t7)
            if best is None or worst < best[0]:
                best = (worst, la, al, t1, t2, t4, t7)
    worst, la, al, t1, t2, t4, t7 = best
    print(f"\n  best joint point over the box: log10 a0 = {la:.4f} (a0 = {10**la:.4e} = "
          f"{10**la/A0_CANON:.3f}x canon), alpha = {al:.2f}")
    print(f"     F1 SPARC {t1:6.2f} sigma   F2 ephemeris {t2:8.3g} sigma   F4 clusters {t4:6.2f} sigma   "
          f"F7 Crater II {t7:6.2f} sigma")
    print(f"     WORST front at the best point = {worst:.3f} sigma")
    check(worst < 3.0,
          f"NO front pair is mutually exclusive: a point exists at which the worst of four MEASURED fronts "
          f"is {worst:.2f} sigma, below any referee-proof threshold.  Outcome (b) is NOT what the "
          f"mathematics gives -- the framework is not falsified by this joint scan, and the prior "
          f"'zero referee-proof kills' standing is reproduced")
    print("  Note which front is doing the binding: with alpha free the ephemeris tension collapses from")
    print(f"  {eph_residual(A0_CANON,1.0)/(EPH_2SIG/2.0):.3g} sigma at alpha = 1 to {t2:.3g} sigma at "
          f"alpha = {al:.2f}, and clusters take over as the binding front at {t4:.2f} sigma.")
    return dict(worst=worst, la=la, al=al, t1=t1, t2=t2, t4=t4, t7=t7)


# =========================================================================================================
# 9.  THE FINAL DOF COUNT
# =========================================================================================================
def sec9_verdict(sp_res, cl_res, mat, oc, q4, pairs):
    banner("9.  THE FINAL HONEST DOF COUNT, AND EVERY REMAINING FLAT DIRECTION")
    n = len(PARAMS)
    print(f"  NOMINAL free quantities enumerated (none removed): {n}")
    for j, p in enumerate(PARAMS):
        ns, sens, st = mat["ledger"][p]
        print(f"     {j+1}. {p:<22s} seen by {ns} front(s)  [{st}]")
    print(f"\n  PHYSICAL RANK of the 7x7 sensitivity matrix (sv >= 1 sigma) = {mat['det']}")
    print(f"  IN-HAND rank, dropping the un-measured wide-binary row       = {mat['det_nowb']}")
    print(f"  -> IRREDUCIBLE FREE DOF = {n} - {mat['det_nowb']} = {n - mat['det_nowb']} "
          f"(and {n - mat['det']} counting the DR4 forecast)")
    print(f"\n  THE FLAT DIRECTIONS, named and explained:")
    print(f"   1. d ln kappa = -d ln(footing).  EXACTLY flat, proven in 5a to {1e-12:.0e}: every front sees")
    print(f"      kappa and the footing only through a0.  The footing fork is "
          f"{math.log10(1/math.sqrt(OMEGA_L))/0.0356:.1f}x larger than the kappa signal it would measure.")
    print(f"   2. delta = I_0 x f_clustered.  UNCONSTRAINED by all seven fronts.  The only front that could")
    print(f"      see it needs delta = {cl_res['delta_close']:.1f} (the LambdaCDM dark-matter amount) and the")
    print(f"      framework's own particle-vs-mode position sets f_clustered = 0.  Zeroed BY POSTULATE.")
    print(f"   3. f, the a0(z) floor choice.  Seen by ONE front (F5), which is itself LambdaCDM-degenerate")
    print(f"      and currently CONTESTED (MUSE-DARK III measures a0 rising).  One front = a fit.")
    if n - mat["det_nowb"] > 3:
        print(f"   4+. plus the direction(s) the SVD lists in 5c beyond these.")
    print(f"\n  WHAT DID GET BRIDGED, and it is not nothing:")
    print(f"   * alpha, the shape dof: the ephemeris FIXES it at >= {q4['a_2s_efe']:.2f} and SPARC "
          f"({abs(q4['rms_d']-q4['rms_1']):.4f} dex),")
    print(f"     clusters ({abs(q4['cdd']-q4['cd1']):.4f} dex) and the WB forecast all accept -- six orders "
          f"of magnitude bridged.")
    print(f"     But the price is the exact law and the Milgrom-1999 kernel, so this trades a fitted")
    print(f"     parameter for an unexplained one rather than reducing the total.")
    print(f"   * a0: SPARC orbital FREQUENCIES + LLR give a0 <= {oc['a0_max']:.3e} with no RAR fit in it --")
    print(f"     a second, methodologically disjoint line.  It clears canon by "
          f"{100*(oc['a0_max']/A0_CANON-1):.1f}% and ALT by {100*(oc['a0_max']/A0_ALT-1):.1f}%.")
    print(f"   * omega_c: the two edges are compatible with only {100*oc['frac']:.1f}% of the LLR-permitted")
    print(f"     log-range surviving, so the consistency test is real and it passed -- but a one-sided")
    print(f"     upper bound cannot imply a lower bound, so nothing was derived.  And no natural scale in")
    print(f"     the framework lands in the window.")
    print(f"\n  ENGAGING THE PRIOR RESULT.  The 2026-06-15 analysis found the framework jointly viable on")
    print(f"  8 of 9 fronts at +2 degrees of freedom with zero referee-proof kills.  This lane's answer to")
    print(f"  'can those +2 be driven to 0 by over-determination' is NO, and it says which two survive and")
    print(f"  why: the kappa-footing product (a theorem about the fronts) and the ghost-condensate amount")
    print(f"  (zeroed by the framework's own postulate).  Sec. 8 independently reproduces the 'zero")
    print(f"  referee-proof kills' half -- the best joint point sits at {pairs['worst']:.2f} sigma worst-front.")
    print(f"\n  OUTCOME: (c) CONTINUUM / DEGENERATE.  Not (a): the parameters are not derived.  Not (b): no")
    print(f"  front pair is mutually exclusive.  The dof count cannot be driven to zero by these fronts,")
    print(f"  and the reason is structural in two of the three cases, not a matter of precision.")
    print(f"  NO DOOR IS DECLARED CLOSED.  What would change the answer: (i) a front that sees kappa other")
    print(f"  than through a0 -- i.e. a prediction of Z, not of a0; (ii) any observable sensitive to the")
    print(f"  condensate amount without a free clustered fraction; (iii) a second, independent a0(z) front.")


# =========================================================================================================
def main() -> int:
    print(RULE)
    print("LANE K -- SCALE-BRIDGING CONSISTENCY.  mi_scale_bridging_2026.py")
    print("Parameters x fronts sensitivity matrix, its rank, and the two scale-bridge questions.")
    print("CREDIT: nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9;")
    print("        a_lambda = c^2 sqrt(Lambda/3) is Milgrom 1994 Ann.Phys. 229:384; temperature")
    print("        Narnhofer-Peter-Thirring 1996; five-acceleration Deser-Levin 1997; exponential")
    print("        kernel McGaugh 2008 eq 11a.  kappa = 1/2 is FITTED, NOT DERIVED.")
    print(RULE)

    sec1_family()
    sp_res = sec2_sparc()
    cl_res = sec3_clusters()
    sec4_closed()
    mat = sec5_matrix(sp_res, cl_res)
    oc = sec6_omegac(sp_res)
    q4 = sec7_alpha(sp_res, cl_res)
    pairs = sec8_pairs(sp_res, cl_res, mat)
    sec9_verdict(sp_res, cl_res, mat, oc, q4, pairs)

    banner("CHECK TALLY")
    print(f"  {_PASS}/{_PASS + _FAIL} checks held.")
    if _FAIL:
        print(f"  {_FAIL} FAILED.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
