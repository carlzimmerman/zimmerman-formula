#!/usr/bin/env python3
r"""mi_routeA_shape_invariant_a0_2026.py -- THE SHARPEST SHAPE-INVARIANT a0 ESTIMATOR, and what it costs.

THE PROBLEM THIS INHERITS. `mi_routeA_a0_estimator_invariance_2026.py` (7/7) established that the corpus's
sharpest single-number a0 constraint, the "a0-line"

    g_obs^2 - g_bar^2 = a0 g_bar

is the ALPHA=1 KERNEL WRITTEN AS A STRAIGHT LINE. It is therefore not shape-free but shape-ASSUMING, and
alpha=1 was retired on 2026-08-02 for ephemeris reasons (Route A's exponential kernel replaced it). The task
here is constructive: BUILD the best genuinely shape-invariant a0 estimator, price it honestly, and say
whether it separates kappa = 1/2 from Milgrom 2020's kappa = 1/2pi.

THE ONE STRUCTURE THAT IS SHAPE-INVARIANT is the deep-MOND limit nu sqrt(y) -> 1, shared by every kernel.
So this script starts by computing the EXACT bias that every deep-limit-based a0 estimator carries:

    Q(y) = nu(y)^2 y = V^4 / (G M a0)     [spherical/asymptotic],   Q(0) = 1 for every kernel

Q is the whole story. The BTFR's "coefficient exactly 1" is Q(0) = 1; a real galaxy's flat part sits at finite
y, so the BTFR measures Q(y_out) a0, not a0. And the central finding of this script is that

    ROUTE A APPROACHES THE DEEP LIMIT AS O(sqrt(y)), NOT O(y):  Q = 1 + sqrt(y) + (5/12) y + (1/12) y^(3/2)

whereas alpha=1 gives Q = 1 + y exactly and alpha=2 gives Q = 1 + y/2 + ... So the ADOPTED kernel is the
SLOWEST of the family to reach the shape-invariant regime, and "just go deeper" is far more expensive under
Route A than it was under either retired kernel. That is an unfavourable structural fact and it drives
everything below.

WHAT IS BUILT AND COMPARED (all on the corpus's own conventions, reproduced to <1% in S5):
  * LINE-GLS / LINE-median  -- the committed a0-line estimators, re-implemented from raw SPARC
  * DEEP                    -- the shape-marginalised deep estimator <g_obs^2/g_bar> over a frozen depth cut
  * BTFR                    -- V_flat^4 / (G M_bar), the deep-limit theorem of the convex field theory
  * SQRTY                   -- NEW: regress ln(g_obs^2/g_bar) on {1, sqrt(y), y, y^(3/2)} and take the
                               INTERCEPT. Shape-invariant BY CONSTRUCTION, because the basis spans the
                               small-y expansion of Q for every kernel in the family.

  S1  the kappa gap is THREE different numbers; which one is the right object
  S2  Q(y): the exact bias of every deep-limit estimator, and Route A's O(sqrt(y)) approach
  S3  SPARC's depth census vs the depth the kappa test would need
  S4  the deep limit's EXACT (a0, Upsilon) degeneracy -- why only the gas breaks it
  S5  conventions validated against the committed a0-line (control, not a fit)
  S6  the synthetic bias matrix: which estimators are shape-invariant
  S7  real data, full error budget, both footings
  S8  *** THE VERDICT on kappa = 1/2 vs 1/2pi, and what would resolve it ***
  S9  the a0-line's owed corrections, with the published Occam bans reproduced then corrected

CIRCULARITY GUARDS. (i) Depth selection and the regression design variable y are FROZEN at a reference a0 with
a fixed Upsilon; re-selecting as a0 varies lets the sample track the parameter. (ii) Upsilon and gas-scale
systematics are evaluated with the SELECTION HELD FIXED. (iii) a0 is never fitted to improve any framework
prediction; the estimators MEASURE it, and are then compared to both footings as postulates.

Exit 0 = ran and every internal check held. No check(True); no check that cannot fail.
"""
from __future__ import annotations

import glob
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import (A0_ALT, A0_CANON, A0_M20, Z_FW, nu,  # noqa: E402
                               nu_alpha1, nu_alpha2)

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 118)
    print(f"  {t}")
    print("=" * 118)


# ---------------------------------------------------------------------------- kernels, as nu(y) and as Q(y)
def nu_simple(y):
    """the literature's 'simple' mu = x/(1+x), inverted in spherical symmetry. A control, not the framework's."""
    y = np.asarray(y, float)
    x = 0.5 * (y + np.sqrt(y * y + 4.0 * y))
    return x / y


KERN = {"RouteA (adopted)": nu, "alpha=1 (retired)": nu_alpha1,
        "alpha=2 (superseded)": nu_alpha2, "simple (control)": nu_simple}


def Qy(kf, y):
    """Q(y) = nu(y)^2 y.  For a spherical/asymptotic system V^4 = Q(y) G M a0, so Q IS the multiplicative
    bias any estimator built on the deep-MOND limit V^4 = G M a0 carries at finite depth y."""
    y = np.asarray(y, float)
    return np.asarray(kf(y)) ** 2 * y


KPC, MSUN, G_N = 3.0857e19, 1.989e30, 6.674e-11
UD_FID, UB_OVER_UD = 0.70, 1.4                 # the a0-line's own convention: Upsilon_bul = 1.4 Upsilon_disk
GAP_LOG = math.log(A0_CANON / A0_M20)          # the object to compare FRACTIONAL errors against
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------- SPARC: table 1 + the mass models
TBL = {}
_mrt = os.path.join(HERE, "data", "SPARC_Lelli2016c.mrt")
for _ln in open(_mrt).read().split("\n"):
    _t = _ln.split()
    if len(_t) != 19:
        continue
    try:
        TBL[_t[0]] = dict(D=float(_t[2]), eD=float(_t[3]), fD=int(_t[4]), inc=float(_t[5]),
                          einc=float(_t[6]), L36=float(_t[7]), MHI=float(_t[13]),
                          Vf=float(_t[15]), eVf=float(_t[16]), Qf=int(_t[17]))
    except ValueError:
        continue

GG = []
for _f in sorted(glob.glob(os.path.join(HERE, "data", "sparc_data", "*_rotmod.dat"))):
    _nm = os.path.basename(_f).replace("_rotmod.dat", "")
    if _nm not in TBL:
        continue
    T = TBL[_nm]
    if T["Qf"] > 2 or T["inc"] < 30.0:                     # the a0-line's cuts, verbatim
        continue
    _d = np.genfromtxt(_f, comments="#")
    if _d.ndim != 2 or _d.shape[1] < 6:
        continue
    R, Vo, eV, Vg, Vd, Vb = (_d[:, i] for i in range(6))
    Vg2 = np.sign(Vg) * Vg ** 2                            # SPARC signs Vgas for inward-pulling annuli
    V2f = Vg2 + UD_FID * Vd ** 2 + UB_OVER_UD * UD_FID * Vb ** 2
    m = ((R > 0) & (Vo > 0) & (V2f > 0) & np.isfinite(V2f)
         & (eV / np.maximum(Vo, 1e-9) < 0.10))             # e_V/V < 10%, the a0-line's third cut
    if m.sum() < 1:
        continue
    GG.append(dict(name=_nm, R=R[m] * KPC, Vo=Vo[m] * 1e3, eVrel=eV[m] / Vo[m],
                   Vg2=Vg2[m] * 1e6, Vd2=Vd[m] ** 2 * 1e6, Vb2=Vb[m] ** 2 * 1e6,
                   Rlast=R[m][-1] * KPC, Vlast=Vo[m][-1] * 1e3, hasbul=bool(np.max(Vb) > 0), **T))
NG = len(GG)


def build(Ud=UD_FID, gasf=1.0, Dfac=None, sinfac=None):
    """(g_bar, g_obs) for every surviving point.

    EXACT distance scaling, as the corpus's own sympy derivation states: a baryonic component's V^2 scales as
    D while R scales as D, so g_bar is distance-INDEPENDENT, while g_obs = V_obs^2/R scales as 1/D. sinfac
    multiplies V_obs (an inclination error rescales the deprojected velocity only).
    """
    gb, go = [], []
    for k, g in enumerate(GG):
        V2 = gasf * g["Vg2"] + Ud * g["Vd2"] + UB_OVER_UD * Ud * g["Vb2"]
        df = 1.0 if Dfac is None else Dfac[k]
        sf = 1.0 if sinfac is None else sinfac[k]
        gb.append(V2 / g["R"])
        go.append((g["Vo"] * sf) ** 2 / (g["R"] * df))
    return np.concatenate(gb), np.concatenate(go)


GB0, GO0 = build()
EVREL = np.concatenate([g["eVrel"] for g in GG])
GIDX = np.concatenate([np.full(len(g["R"]), k) for k, g in enumerate(GG)])
WGAL = np.concatenate([np.full(len(g["R"]), 1.0 / len(g["R"])) for g in GG])   # one galaxy, one vote
ISGAS = np.concatenate([g["Vg2"] > (UD_FID * g["Vd2"] + UB_OVER_UD * UD_FID * g["Vb2"]) for g in GG])
GROWS = [np.where(GIDX == k)[0] for k in range(NG)]
Y0 = GB0 / A0_CANON                                        # the FROZEN design/selection variable
NPT = len(GB0)
print(f"  SPARC loaded: {NPT} points in {NG} galaxies after Q<=2, inc>=30 deg, e_V/V<10% "
      f"(Upsilon_d = {UD_FID}, Upsilon_b = {UB_OVER_UD} Upsilon_d); gas-dominated points {int(ISGAS.sum())} "
      f"in {len(set(GIDX[ISGAS]))} galaxies")


banner("S1  THE kappa GAP IS THREE DIFFERENT NUMBERS -- and only one of them is the right object")

gap_of_canon = 1.0 - A0_M20 / A0_CANON
gap_of_m20 = A0_CANON / A0_M20 - 1.0
print(f"  a0(kappa=1/2)   = {A0_CANON:.5e}      a0(kappa=1/2pi) = {A0_M20:.5e}   ratio = Z/(2pi) = "
      f"{A0_M20/A0_CANON:.6f}")
print(f"    as a fraction of the canonical value : {100*gap_of_canon:.3f}%   <- what the invariance script's "
      f"KAPPA_GAP constant computes, and what the lane brief quotes as 7.87%")
print(f"    as a fraction of Milgrom's value     : {100*gap_of_m20:.3f}%")
print(f"    in the LOG                           : {100*GAP_LOG:.3f}%  = {GAP_LOG/math.log(10):.4f} dex   "
      f"<- what the invariance script's DOCSTRING quotes as 8.20%")
check(abs(A0_M20 / A0_CANON - Z_FW / (2 * math.pi)) < 1e-12
      and abs(gap_of_canon - 0.07868) < 1e-4 and abs(GAP_LOG - 0.08195) < 1e-4
      and (gap_of_m20 - gap_of_canon) > 0.006,
      f"S1 the separation is EXACTLY Z/(2pi) = {A0_M20/A0_CANON:.6f}, independent of H0 and Omega_Lambda, so it "
      f"is a pure number and both footings inherit it unchanged. But it is quotable three ways spanning "
      f"{100*gap_of_canon:.2f}%-{100*gap_of_m20:.2f}%, and the corpus uses two of them interchangeably: the "
      f"invariance script's computed constant is the {100*gap_of_canon:.2f}% ratio while its own docstring "
      f"quotes the {100*GAP_LOG:.2f}% log. Since every a0 error in this corpus is quoted FRACTIONALLY (i.e. "
      f"log-normally), the LOG gap {100*GAP_LOG:.3f}% = {GAP_LOG/math.log(10):.4f} dex is the correct object "
      f"and is used throughout below. This is a labelling item, not an arithmetic error -- both numbers are "
      f"right about different things")


banner("S2  Q(y) = nu^2 y IS THE EXACT BIAS OF EVERY DEEP-LIMIT ESTIMATOR -- and Route A's is O(sqrt(y))")

print("  For a spherical/asymptotic system V^2 = nu(y) g_bar R and G M = g_bar R^2, so")
print("      V^4 / (G M a0)  =  nu(y)^2 y  =:  Q(y),     Q(0) = 1 for every kernel.")
print("  Q(0) = 1 IS the BTFR's 'coefficient exactly 1'. Q(y) - 1 is what a real galaxy at finite depth adds.")
print(f"\n  {'y':>8}" + "".join(f"{k.split(' (')[0]:>14}" for k in KERN) + f"{'half-spread':>13}")
print("  " + "-" * 79)
qtab = {}
for yv in [1e-4, 1e-3, 3e-3, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]:
    qs = {k: float(Qy(f, yv)) for k, f in KERN.items()}
    lq = np.log(list(qs.values()))
    qtab[yv] = 0.5 * (lq.max() - lq.min())
    print(f"  {yv:>8.4g}" + "".join(f"{qs[k]:>14.5f}" for k in KERN) + f"{100*qtab[yv]:>12.2f}%")

# the small-y expansion: s = sqrt(y). Route A: s/(1-e^-s) = 1 + s/2 + s^2/12 + O(s^4)  (Bernoulli), so
# Q = (that)^2 = 1 + s + (5/12) s^2 + (1/12) s^3 + O(s^4).
ser_err = []
for yv in [1e-4, 1e-2, 0.1, 1.0]:
    s = math.sqrt(yv)
    ser = 1.0 + s + (5.0 / 12.0) * yv + (1.0 / 12.0) * yv * s
    ser_err.append((yv, abs(ser / float(Qy(nu, yv)) - 1.0)))
slopes = {}
for kn, kf in KERN.items():
    y1, y2 = 1e-5, 1e-4
    slopes[kn] = math.log((float(Qy(kf, y2)) - 1.0) / (float(Qy(kf, y1)) - 1.0)) / math.log(y2 / y1)
print(f"\n  log-log slope of Q-1 at y ~ 1e-5..1e-4 (the ORDER of the approach to the deep limit):")
for kn in KERN:
    print(f"    {kn:<24} d ln(Q-1)/d ln y = {slopes[kn]:.4f}")
print(f"  Route A series 1 + sqrt(y) + (5/12) y + (1/12) y^(3/2) vs exact: "
      + ", ".join(f"y={a:g}: {100*b:.2e}%" for a, b in ser_err))
check(abs(slopes["RouteA (adopted)"] - 0.5) < 0.02 and abs(slopes["simple (control)"] - 0.5) < 0.02
      and abs(slopes["alpha=1 (retired)"] - 1.0) < 0.02 and abs(slopes["alpha=2 (superseded)"] - 1.0) < 0.02
      and ser_err[1][1] < 1e-6,
      f"S2 *** THE ADOPTED KERNEL IS THE SLOWEST IN THE FAMILY TO REACH THE SHAPE-INVARIANT REGIME. *** "
      f"Q - 1 vanishes as y^{slopes['RouteA (adopted)']:.2f} for Route A (and for simple), against "
      f"y^{slopes['alpha=1 (retired)']:.2f} for alpha=1 and alpha=2. The closed series "
      f"Q = 1 + sqrt(y) + (5/12)y + (1/12)y^(3/2) reproduces the exact kernel to "
      f"{100*ser_err[1][1]:.1e}% at y = 0.01. CONSEQUENCE: at y = 0.1 the deep-limit estimator over-reads a0 "
      f"by {100*(float(Qy(nu,0.1))-1):.0f}% under Route A but only {100*(float(Qy(nu_alpha2,0.1))-1):.0f}% "
      f"under alpha=2, so 'restrict to deep points' buys shape-invariance an ORDER of magnitude more slowly "
      f"than it did under either retired kernel. Route A did not create the shape systematic, but it made it "
      f"much harder to outrun")


banner("S3  SPARC'S DEPTH CENSUS vs THE DEPTH THE kappa TEST WOULD NEED")

need3 = GAP_LOG / 3.0                                      # 3-sigma on the log gap needs sigma <= gap/3
ygrid = np.logspace(-5, 0.5, 400)
hs = np.array([0.5 * (np.log([float(Qy(f, yv)) for f in KERN.values()]).max()
                      - np.log([float(Qy(f, yv)) for f in KERN.values()]).min()) for yv in ygrid])
y_need3 = float(np.interp(need3, hs, ygrid))
y_need1 = float(np.interp(GAP_LOG, hs, ygrid))
print(f"  3 sigma on a {100*GAP_LOG:.3f}% log gap needs sigma(ln a0) <= {100*need3:.3f}%.")
print(f"  The 4-kernel shape half-spread on Q falls below that only at y <= {y_need3:.2e};")
print(f"  it falls below the gap ITSELF (a 1-sigma-quality statement) only at y <= {y_need1:.2e}.")
print(f"\n  {'threshold':>12}{'y_max':>10}{'SPARC points':>14}{'galaxies':>10}")
print("  " + "-" * 47)
census = {}
for lab, ym in [("3 sigma", y_need3), ("1 sigma", y_need1), ("y<0.01", 0.01), ("y<0.03", 0.03),
                ("y<0.1", 0.1), ("all", 1e9)]:
    s = Y0 < ym
    census[lab] = (int(s.sum()), len(set(GIDX[s])))
    print(f"  {lab:>12}{ym:>10.3g}{int(s.sum()):>14}{len(set(GIDX[s])):>10}")
check(census["3 sigma"][0] == 0 and float(np.min(Y0)) > y_need3 and census["1 sigma"][0] < 0.10 * NPT,
      f"S3 *** THE DEPTH THE kappa TEST NEEDS DOES NOT EXIST IN SPARC. *** A 3-sigma separation demands the "
      f"shape systematic be under {100*need3:.2f}%, which needs y <= {y_need3:.1e}; SPARC's deepest single "
      f"point sits at y = {float(np.min(Y0)):.2e}, so {census['3 sigma'][0]} of {NPT} points qualify. Even the "
      f"much weaker requirement 'shape systematic below the gap itself' needs y <= {y_need1:.1e}, where SPARC "
      f"has {census['1 sigma'][0]} points ({100*census['1 sigma'][0]/NPT:.1f}% of the sample) in "
      f"{census['1 sigma'][1]} galaxies. This is not a statistics problem "
      f"that more galaxies fix -- it is a DYNAMIC-RANGE problem, and it is the reason every total error below "
      f"lands in the same place")


banner("S4  THE DEEP LIMIT'S EXACT (a0, Upsilon) DEGENERACY -- why only the gas breaks it")

# In the pure deep limit g_obs = sqrt(a0 g_bar) with g_bar = Upsilon g_star + g_gas. If g_gas == 0 then
# g_obs = sqrt(a0 Upsilon g_star) depends only on the PRODUCT a0*Upsilon, so a0 is formally unmeasurable.
def chi2_deep(a0, Ud, gasf, kf=None):
    tot = 0.0
    for g in GG:
        V2 = gasf * g["Vg2"] + Ud * g["Vd2"] + UB_OVER_UD * Ud * g["Vb2"]
        m = V2 > 0
        if m.sum() < 1:
            continue
        gb = V2[m] / g["R"][m]
        gob = g["Vo"][m] ** 2 / g["R"][m]
        pred = np.sqrt(a0 * gb) if kf is None else np.asarray(kf(gb / a0)) * gb
        tot += float(np.sum((np.log(gob) - np.log(pred)) ** 2))
    return tot


f = 1.3
d_nogas = abs(chi2_deep(A0_CANON * f, UD_FID / f, 0.0) / chi2_deep(A0_CANON, UD_FID, 0.0) - 1.0)
c_gas0 = chi2_deep(A0_CANON, UD_FID, 1.0)
d_gas = abs(chi2_deep(A0_CANON * f, UD_FID / f, 1.0) - c_gas0)
d_ra = abs(chi2_deep(A0_CANON * f, UD_FID / f, 0.0, kf=nu) / chi2_deep(A0_CANON, UD_FID, 0.0, kf=nu) - 1.0)
print(f"  chi2 under (a0, Upsilon) -> ({f} a0, Upsilon/{f}), log-space residuals, all {NG} galaxies:")
print(f"    deep limit, gas ZEROED    : fractional change {d_nogas:.3e}   -> EXACTLY degenerate")
print(f"    deep limit, gas RESTORED  : Dchi2 = {d_gas:.2f} on chi2 = {c_gas0:.1f}  -> broken")
print(f"    Route A kernel, gas zeroed: fractional change {d_ra:.3e}   -> broken by the TRANSITION alone")
check(d_nogas < 1e-12 and d_gas > 5.0 and d_ra > 1e-3,
      f"S4 *** A DEEP-ONLY LIKELIHOOD DOES NOT MEASURE a0; IT MEASURES a0 x Upsilon. *** With the gas zeroed "
      f"the deep-limit chi2 is invariant under (a0, Upsilon) -> (f a0, Upsilon/f) to {d_nogas:.1e} -- an exact "
      f"degeneracy, not a near one. Two things break it and only two: the FIXED gas component (Dchi2 = "
      f"{d_gas:.1f}) and the TRANSITION SHAPE ({d_ra:.1e} fractional under Route A with no gas at all). So the "
      f"'shape-free deep-only profile likelihood' is not shape-free in the way it looks: strip the shape and "
      f"the entire a0 signal comes from the gas fraction and from wherever Upsilon is pinned. This is why the "
      f"gas-dominated subsample is not merely convenient -- for a shape-invariant estimator it is the ONLY "
      f"channel carrying a0, and it is why no amount of depth makes the Upsilon prior irrelevant")


banner("S5  CONVENTIONS VALIDATED against the committed a0-line (a control, not a fit)")


def line_gls(gb, go, rel, fint, a0=A0_CANON, niter=8):
    """the a0-line's iterated GLS through the origin with MODEL-based errors, as `estimator_theory.py` states:
    sigma_E = 2 g_model sigma_gobs with sigma_gobs = 2 (e_V/V) g_model, plus an intrinsic floor f_int g_model^2."""
    E = go ** 2 - gb ** 2
    for _ in range(niter):
        gm2 = gb ** 2 + a0 * gb                            # g_model^2 on the estimator's own (alpha=1) law
        sE = np.hypot(4.0 * rel * gm2, fint * gm2)
        w = 1.0 / sE ** 2
        a0 = float(np.sum(w * E * gb) / np.sum(w * gb ** 2))
    return a0


def tune_fint(gb, go, rel):
    lo, hi = 1e-4, 20.0
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        a0 = line_gls(gb, go, rel, mid)
        gm2 = gb ** 2 + a0 * gb
        sE = np.hypot(4.0 * rel * gm2, mid * gm2)
        if float(np.sum(((go ** 2 - gb ** 2 - a0 * gb) / sE) ** 2)) / len(gb) > 1.0:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


rep = {}
print(f"  {'sample':>10}{'N pts':>7}{'N gals':>8}{'f_int':>8}{'GLS slope':>13}{'median E/g':>13}"
      f"{'published GLS':>15}")
print("  " + "-" * 74)
for lab, sel, pub in [("FULL", np.ones(NPT, bool), 1.279e-10), ("GAS-DOM", ISGAS, 1.181e-10)]:
    fi = tune_fint(GB0[sel], GO0[sel], EVREL[sel])
    a = line_gls(GB0[sel], GO0[sel], EVREL[sel], fi)
    med = float(np.median((GO0[sel] ** 2 - GB0[sel] ** 2) / GB0[sel]))
    rep[lab] = dict(fint=fi, gls=a, med=med, n=int(sel.sum()), ng=len(set(GIDX[sel])), pub=pub)
    print(f"  {lab:>10}{int(sel.sum()):>7}{len(set(GIDX[sel])):>8}{fi:>8.3f}{a:>13.4e}{med:>13.4e}"
          f"{pub:>15.4e}")
check(rep["FULL"]["n"] == 2696 and rep["GAS-DOM"]["n"] == 310 and rep["GAS-DOM"]["ng"] == 49
      and abs(rep["FULL"]["gls"] / 1.279e-10 - 1) < 0.01 and abs(rep["GAS-DOM"]["gls"] / 1.181e-10 - 1) < 0.01
      and abs(rep["GAS-DOM"]["med"] / 0.973e-10 - 1) < 0.02 and abs(rep["FULL"]["fint"] - 0.64) < 0.03,
      f"S5 this file's independent read of raw SPARC reproduces the committed a0-line exactly: "
      f"{rep['FULL']['n']} FULL points in {rep['FULL']['ng']} galaxies and {rep['GAS-DOM']['n']} gas-dominated "
      f"points in {rep['GAS-DOM']['ng']} galaxies (published 2696/147 and 310/49); GLS slopes "
      f"{rep['FULL']['gls']:.4e} and {rep['GAS-DOM']['gls']:.4e} (published 1.279e-10 and 1.181e-10); "
      f"medians {rep['FULL']['med']:.3e} and {rep['GAS-DOM']['med']:.3e} (published 0.88e-10 and 0.97e-10); "
      f"intrinsic-scatter floor f_int = {rep['FULL']['fint']:.3f} (published 0.64). Every correction below is "
      f"therefore directly applicable to the committed numbers, not to a look-alike")


banner("S6  THE SYNTHETIC BIAS MATRIX -- which estimators are actually shape-invariant")


def est_deep(gb, go, sel, w=None):
    """<g_obs^2/g_bar>, geometric mean, one-galaxy-one-vote. Returns Q-weighted a0."""
    w = WGAL if w is None else w
    if sel.sum() < 5:
        return float("nan")
    return math.exp(float(np.sum(w[sel] * np.log(go[sel] ** 2 / gb[sel])) / np.sum(w[sel])))


def est_sqrty(gb, go, yref, sel, deg=3, w=None):
    """NEW: intercept of ln(g_obs^2/g_bar) regressed on {1, sqrt(y), y, y^(3/2), ...}.

    Shape-invariant BY CONSTRUCTION: ln Q(y) = b1 sqrt(y) + b2 y + b3 y^(3/2) + ... for EVERY kernel in the
    family (S2), so the y = 0 intercept is a0 whatever the shape, with the shape absorbed into nuisance
    coefficients. It is also invariant to the a0 used to define y, because rescaling y only rescales the b's.
    """
    w = WGAL if w is None else w
    if sel.sum() < deg + 5:
        return float("nan")
    yy = yref[sel]
    X = np.column_stack([np.ones(yy.size)] + [yy ** (0.5 * k) for k in range(1, deg + 1)])
    sw = np.sqrt(w[sel])
    c, *_ = np.linalg.lstsq(X * sw[:, None], np.log(go[sel] ** 2 / gb[sel]) * sw, rcond=None)
    return math.exp(float(c[0]))


SYN = {kn: np.asarray(kf(Y0)) * GB0 for kn, kf in KERN.items()}     # noiseless data at a0 = A0_CANON exactly
SELS = {"all points": np.ones(NPT, bool), "y<1": Y0 < 1.0, "y<0.3": Y0 < 0.3,
        "gas-dom": ISGAS, "gas-dom & y<0.3": ISGAS & (Y0 < 0.3)}
print("  Each estimator is run on NOISELESS data generated from the REAL SPARC g_bar values by each kernel at")
print("  a0 = a0_canon exactly. The entry is the returned a0 / a0_true, so 1.0000 = unbiased.\n")
print(f"  {'sample':>16}  {'estimator':<14}" + "".join(f"{k.split(' (')[0]:>13}" for k in KERN)
      + f"{'half-spread':>13}")
print("  " + "-" * 100)
bias = {}
for slab, sel in SELS.items():
    fi = tune_fint(GB0[sel], GO0[sel], EVREL[sel])
    for elab, fn in [("LINE-GLS", lambda gb, go: line_gls(gb[sel], go[sel], EVREL[sel], fi)),
                     ("LINE-median", lambda gb, go: float(np.median((go[sel] ** 2 - gb[sel] ** 2) / gb[sel]))),
                     ("DEEP", lambda gb, go: est_deep(gb, go, sel)),
                     ("SQRTY deg=3", lambda gb, go: est_sqrty(gb, go, Y0, sel, 3))]:
        row = {kn: fn(GB0, SYN[kn]) / A0_CANON for kn in KERN}
        lr = np.log(list(row.values()))
        bias[(slab, elab)] = dict(row=row, hs=0.5 * (lr.max() - lr.min()), geo=math.exp(float(np.mean(lr))))
        print(f"  {slab:>16}  {elab:<14}" + "".join(f"{row[k]:>13.4f}" for k in KERN)
              + f"{100*bias[(slab, elab)]['hs']:>12.2f}%")
    print()

sq1 = max(abs(v - 1.0) for v in bias[("y<1", "SQRTY deg=3")]["row"].values())
ln_full = bias[("all points", "LINE-GLS")]["row"]
dp_full = bias[("all points", "DEEP")]["row"]
check(sq1 < 0.01 and abs(ln_full["RouteA (adopted)"] - 1) > 0.20 and abs(dp_full["RouteA (adopted)"] - 1) > 0.5
      and abs(ln_full["alpha=1 (retired)"] - 1) < 1e-9,
      f"S6 *** A GENUINELY SHAPE-INVARIANT ESTIMATOR EXISTS AND THIS IS IT: the sqrt(y)-INTERCEPT. *** On "
      f"y < 1 it returns a0 to within {100*sq1:.2f}% under ALL FOUR kernels, because the regression basis "
      f"{{1, sqrt(y), y, y^(3/2)}} spans the small-y expansion of Q for every one of them. On the same data "
      f"the a0-line returns {ln_full['RouteA (adopted)']:.3f}x under Route A and "
      f"{ln_full['alpha=2 (superseded)']:.3f}x under alpha=2 (and exactly 1.000000x under alpha=1, where it "
      f"is an identity), and the bare deep estimator returns {dp_full['RouteA (adopted)']:.3f}x. *** THIS "
      f"ALSO CORRECTS THE COMMITTED E5 NUMBER: mi_routeA_a0_estimator_invariance_2026.py quotes the a0-line's "
      f"Route A bias as +10.3% and its alpha=2 bias as -83.6%, but those were computed on a log-uniform "
      f"synthetic g_bar grid, not on SPARC's actual y distribution with the actual GLS weights. On the real "
      f"FULL sample they are {100*(ln_full['RouteA (adopted)']-1):+.1f}% and "
      f"{100*(ln_full['alpha=2 (superseded)']-1):+.1f}%; on the GAS-DOM sample the 1.181e-10 actually comes "
      f"from, {100*(bias[('gas-dom','LINE-GLS')]['row']['RouteA (adopted)']-1):+.1f}% and "
      f"{100*(bias[('gas-dom','LINE-GLS')]['row']['alpha=2 (superseded)']-1):+.1f}%. The sign was right; the "
      f"magnitudes were not the right object")

# invariance to the reference a0 used to build the design AND the selection. The design half is algebra
# (rescaling y only rescales the nuisance coefficients, which the free regression absorbs); the SELECTION half
# is not -- moving a0_ref up widens the window in physical terms and can break the truncated series. Both are
# varied together here so the check can actually fail.
refbias = {}
for rlab, aref in [("0.5x canon", 0.5 * A0_CANON), ("canon", A0_CANON), ("2x canon", 2.0 * A0_CANON),
                   ("ALT", A0_ALT)]:
    yr = GB0 / aref
    refbias[rlab] = (max(abs(est_sqrty(GB0, SYN[kn], yr, Y0 < 1.0, 3) / A0_CANON - 1.0) for kn in KERN),
                     max(abs(est_sqrty(GB0, SYN[kn], yr, yr < 1.0, 3) / A0_CANON - 1.0) for kn in KERN),
                     int((yr < 1.0).sum()))
print("  and the intercept does not care which a0 was used to define the design variable y:")
print(f"    {'a0_ref':>12}{'design only':>14}{'design+selection':>18}{'N in window':>13}")
for rlab, v in refbias.items():
    print(f"    {rlab:>12}{100*v[0]:>13.3f}%{100*v[1]:>17.3f}%{v[2]:>13}")
check(max(v[0] for v in refbias.values()) < 0.005 and max(v[1] for v in refbias.values()) < 0.03
      and refbias["2x canon"][2] > 1.15 * refbias["canon"][2],
      f"S6b the sqrt(y)-intercept has no footing-dependence and no a0-in-a0-out circularity. Rebuilding the "
      f"DESIGN at 0.5x, 1x, 2x canonical or at ALT leaves the worst bias at "
      f"{100*max(v[0] for v in refbias.values()):.3f}% -- that half is algebra, since rescaling y by 1/f only "
      f"rescales the nuisance coefficients b_k by f^(k/2). Moving the SELECTION with it is the part that could "
      f"break, because a0_ref = 2x canonical widens the window from {refbias['canon'][2]} to "
      f"{refbias['2x canon'][2]} points and pushes the truncated series to y = 2: the worst bias grows to "
      f"{100*max(v[1] for v in refbias.values()):.2f}%, still an order of magnitude under any other "
      f"estimator's shape systematic. Only the SELECTION touches a0, and it is frozen once at canonical")


banner("S7  REAL DATA, FULL ERROR BUDGET, BOTH FOOTINGS")

rng = np.random.default_rng(20260803)
NMC, NBOOT = 160, 400
# perturbed datasets precomputed ONCE: per-galaxy random distance and inclination errors.
PERT_D = [build(Dfac=np.array([max(0.2, 1.0 + rng.normal() * g["eD"] / g["D"]) for g in GG]))
          for _ in range(NMC)]
PERT_I = []
for _ in range(NMC):
    sf = []
    for g in GG:
        i2 = min(89.9, max(20.0, g["inc"] + rng.normal() * max(g["einc"], 1.0)))
        sf.append(math.sin(math.radians(g["inc"])) / math.sin(math.radians(i2)))
    PERT_I.append(build(sinfac=np.array(sf)))
U_LO, U_HI = UD_FID / 10 ** 0.1, UD_FID * 10 ** 0.1         # the a0-line's own sigma_lnUpsilon = 0.1 dex
PERT_U = [build(Ud=U_LO), build(Ud=U_HI)]
PERT_GAS = [build(gasf=0.9), build(gasf=1.1)]               # the a0-line's own 10% global gas calibration
BOOTS = [np.concatenate([GROWS[p] for p in rng.integers(0, NG, NG)]) for _ in range(NBOOT)]


def budget(estname, sel, deg=3):
    """full ensemble error budget for one estimator on one frozen selection."""
    if estname == "DEEP":
        run = lambda gb, go, idx=None: (est_deep(gb, go, sel) if idx is None
                                        else est_deep(gb[idx], go[idx], sel[idx], WGAL[idx]))
    elif estname == "SQRTY":
        run = lambda gb, go, idx=None: (est_sqrty(gb, go, Y0, sel, deg) if idx is None
                                        else est_sqrty(gb[idx], go[idx], Y0[idx], sel[idx], deg, WGAL[idx]))
    else:
        fi = tune_fint(GB0[sel], GO0[sel], EVREL[sel])
        run = lambda gb, go, idx=None: (line_gls(gb[sel], go[sel], EVREL[sel], fi) if idx is None
                                        else line_gls(gb[idx][sel[idx]], go[idx][sel[idx]],
                                                      EVREL[idx][sel[idx]], fi))
    raw = run(GB0, GO0)
    bs = np.array([v for v in (run(GB0, GO0, i) for i in BOOTS) if np.isfinite(v) and v > 0])
    s_stat = float(np.std(np.log(bs)))
    s_D = float(np.std(np.log([run(*p) for p in PERT_D])))
    s_I = float(np.std(np.log([run(*p) for p in PERT_I])))
    s_U = 0.5 * abs(math.log(run(*PERT_U[0]) / run(*PERT_U[1])))
    s_G = 0.5 * abs(math.log(run(*PERT_GAS[0]) / run(*PERT_GAS[1])))
    # shape: half the ln-spread of the estimator's own bias over the four kernels, on this same selection
    perk = {kn: run(GB0, SYN[kn]) / A0_CANON for kn in KERN}
    lb = np.log(list(perk.values()))
    s_shape, geo = 0.5 * float(lb.max() - lb.min()), math.exp(float(np.mean(lb)))
    # the galaxy-to-galaxy bootstrap ALREADY contains the distance and inclination scatter, so adding them
    # again would double count. Charge max(stat, quad(D,I)) once, not the sum.
    s_noise = max(s_stat, math.hypot(s_D, s_I))
    tot = math.sqrt(s_shape ** 2 + s_U ** 2 + s_G ** 2 + s_noise ** 2)
    return dict(raw=raw, deb=raw / geo, stat=s_stat, D=s_D, I=s_I, U=s_U, G=s_G, shape=s_shape,
                noise=s_noise, tot=tot, n=int(sel.sum()), ng=len(set(GIDX[sel])), geo=geo, perk=perk)


ymax_gas = float(np.max(Y0[ISGAS]))
print(f"  NOTE: the gas-dominated cut is ITSELF a depth cut -- the deepest gas-dominated point sits at "
      f"y = {ymax_gas:.3f}, so gas-dom is a subset of y < {math.ceil(ymax_gas*10)/10:g} and 'gas & y<0.3' "
      f"would be the same {int(ISGAS.sum())} points. The two cuts are not independent levers.\n")
CAND = [("DEEP", "all y<0.05", Y0 < 0.05), ("DEEP", "all y<0.1", Y0 < 0.1), ("DEEP", "all y<0.3", Y0 < 0.3),
        ("DEEP", "gas & y<0.1", ISGAS & (Y0 < 0.1)), ("DEEP", "gas-dom", ISGAS),
        ("SQRTY", "all y<1", Y0 < 1.0), ("SQRTY", "all y<3", Y0 < 3.0),
        ("LINE", "gas-dom", ISGAS), ("LINE", "all points", np.ones(NPT, bool))]
res = {}
print(f"  {'estimator':>10}{'sample':>13}{'Npt':>6}{'Ngal':>6}{'raw/can':>9}{'debias/can':>12}"
      f"{'shape':>8}{'stat':>7}{'dist':>7}{'inc':>7}{'Ups':>7}{'gas':>7}{'TOTAL':>8}")
print("  " + "-" * 108)
for en, slab, sel in CAND:
    b = budget(en, sel)
    res[(en, slab)] = b
    print(f"  {en:>10}{slab:>13}{b['n']:>6}{b['ng']:>6}{b['raw']/A0_CANON:>9.3f}{b['deb']/A0_CANON:>12.3f}"
          + "".join(f"{100*b[k]:>6.1f}%" for k in ("shape", "stat", "D", "I", "U", "G"))
          + f"{100*b['tot']:>7.1f}%")

best = min(res.items(), key=lambda kv: kv[1]["tot"])
bk, bb = best
print(f"\n  SHARPEST shape-invariant estimator = {bk[0]} on {bk[1]}: a0 = {bb['deb']:.4e} +- "
      f"{100*bb['tot']:.1f}% (shape-marginalised over the four kernels)")
print(f"    vs canonical {A0_CANON:.4e}: {math.log(bb['deb']/A0_CANON)/bb['tot']:+.2f} sigma")
print(f"    vs ALT       {A0_ALT:.4e}: {math.log(bb['deb']/A0_ALT)/bb['tot']:+.2f} sigma")
print(f"    vs 1/2pi     {A0_M20:.4e}: {math.log(bb['deb']/A0_M20)/bb['tot']:+.2f} sigma")
print(f"  MARGINALISING HIDES A REAL SPREAD -- the same estimator debiased kernel by kernel instead:")
for kn in KERN:
    v = bb["raw"] / bb["perk"][kn]
    print(f"    if {kn:<22} is the law: a0 = {v:.4e} = {v/A0_CANON:.3f}x canonical, "
          f"{math.log(v/A0_CANON)/bb['tot']:+.2f} sigma from canonical, "
          f"{math.log(v/A0_M20)/bb['tot']:+.2f} sigma from 1/2pi")
gas_b, all_b = res[("DEEP", "gas-dom")], res[("DEEP", "all y<0.3")]
print(f"\n  the gas cut, priced: Upsilon {100*all_b['U']:.1f}% -> {100*gas_b['U']:.1f}% but distance "
      f"{100*all_b['D']:.1f}% -> {100*gas_b['D']:.1f}% and inclination {100*all_b['I']:.1f}% -> "
      f"{100*gas_b['I']:.1f}%; TOTAL {100*all_b['tot']:.1f}% -> {100*gas_b['tot']:.1f}%")
check(bb["tot"] > 0.10 and all(v["tot"] > 0.10 for v in res.values())
      and res[("SQRTY", "all y<1")]["stat"] > 2 * res[("DEEP", "all y<0.3")]["stat"],
      f"S7 EVERY shape-invariant route lands in the same place, {100*min(v['tot'] for v in res.values()):.0f}"
      f"-{100*max(v['tot'] for v in res.values()):.0f}%, and it is not a coincidence: the two currencies are "
      f"interchangeable. The sqrt(y)-intercept pays its shape-invariance in VARIANCE -- its bootstrap "
      f"statistical error is {100*res[('SQRTY','all y<1')]['stat']:.0f}% against "
      f"{100*res[('DEEP','all y<0.3')]['stat']:.0f}% for the depth-cut deep estimator, because extrapolating "
      f"an intercept through three collinear nuisance terms is expensive. The deep estimator pays it in "
      f"SHAPE SYSTEMATIC. The best total is {100*bb['tot']:.1f}% ({bk[0]} on {bk[1]}). Note the gas cut is "
      f"close to a WASH, exactly as the a0-line's own sympy derivation says it must be: it suppresses "
      f"Upsilon and nothing else, and gas-rich dwarfs carry WORSE distances and inclinations")


banner("S8  *** THE VERDICT ON kappa = 1/2 vs kappa = 1/2pi ***")

sig = GAP_LOG / bb["tot"]
need_sigma3 = GAP_LOG / 3.0
floor = math.sqrt(bb["shape"] ** 2 + bb["U"] ** 2 + bb["G"] ** 2)     # N -> infinity: noise term to zero
n_for_1pct = bb["ng"] * (bb["noise"] / 0.01) ** 2
print(f"  gap (log) {100*GAP_LOG:.3f}%   best shape-invariant total error {100*bb['tot']:.2f}%   "
      f"separation = {sig:.2f} sigma")
print(f"  ANSWER: NO. A shape-invariant a0 estimator on SPARC separates kappa = 1/2 from kappa = 1/2pi at "
      f"{sig:.2f} sigma.")
print(f"\n  WHY MORE GALAXIES CANNOT FIX IT:")
print(f"    the N-independent floor (shape + Upsilon + gas calibration) is {100*floor:.2f}%, already "
      f"{floor/need_sigma3:.1f}x the {100*need_sigma3:.2f}% a 3-sigma test needs.")
print(f"    driving the noise term alone to 1% would take ~{n_for_1pct:.0f} galaxies and would still leave "
      f"{100*floor:.2f}%.")
print(f"  WHAT WOULD ACTUALLY RESOLVE IT, in order of how much each buys:")
print(f"    1. DYNAMIC RANGE, not sample size. The shape term needs y <~ {y_need3:.1e}, i.e. g_bar <~ "
      f"{y_need3*A0_CANON:.1e} m/s^2. SPARC's floor is g_bar = {float(np.min(GB0)):.1e}. The probes that")
print(f"       reach there are weak-lensing / satellite-kinematics RARs at 100 kpc-1 Mpc, NOT rotation curves;")
print(f"       HI discs truncate two decades short.")
print(f"    2. A KERNEL COMMITMENT. Assuming Route A alone zeroes the shape term and the total falls to "
      f"{100*math.sqrt(bb['tot']**2-bb['shape']**2):.1f}% -> {GAP_LOG/math.sqrt(bb['tot']**2-bb['shape']**2):.2f}"
      f" sigma. Still short of 3, and no longer shape-invariant.")
print(f"    3. Upsilon at {100*bb['U']:.0f}% -> a few %: resolved stellar populations (JWST/IFU) or a sample")
print(f"       with NO stars to speak of. Gas calibration at {100*bb['G']:.0f}% needs CO + HI self-absorption")
print(f"       modelling. Both are irreducible-by-N and both are already at the size of the gap.")
check(sig < 3.0 and floor > need_sigma3,
      f"S8 *** THE ANSWER IS NO, AND IT IS A CLEAN NO. *** The sharpest shape-invariant a0 estimator this "
      f"script can build separates kappa = 1/2 from kappa = 1/2pi at {sig:.2f} sigma, against the 3 sigma a "
      f"claim would need. The obstruction is structural rather than statistical: the N-independent floor "
      f"(shape {100*bb['shape']:.1f}% + Upsilon {100*bb['U']:.1f}% + gas {100*bb['G']:.1f}% = "
      f"{100*floor:.1f}%) already exceeds the {100*need_sigma3:.2f}% budget by {floor/need_sigma3:.1f}x, so "
      f"BIG-SPARC's ~4000 galaxies would not do it either. The honest position stands: SPARC does not measure "
      f"kappa, in either direction, without assuming a transition shape -- and the shape-invariant central "
      f"value happens to sit {math.log(bb['deb']/A0_CANON)/bb['tot']:+.2f} sigma from canonical and "
      f"{math.log(bb['deb']/A0_M20)/bb['tot']:+.2f} sigma from 1/2pi, which is to say it is consistent with "
      f"both and discriminates neither")


banner("S9  THE BTFR, PRICED -- the deep-limit theorem meets a finite outermost radius")

btf = []
for g in GG:
    if g["Vf"] <= 0:
        continue
    Mb = (UD_FID * g["L36"] + 1.33 * g["MHI"]) * 1e9 * MSUN
    if Mb <= 0 or len(g["R"]) < 3:
        continue
    V2 = g["Vg2"] + UD_FID * g["Vd2"] + UB_OVER_UD * UD_FID * g["Vb2"]
    gbl = V2[-1] / g["R"][-1]
    btf.append(dict(a0=(g["Vf"] * 1e3) ** 4 / (G_N * Mb), y=gbl / A0_CANON,
                    Gam=gbl * g["R"][-1] ** 2 / (G_N * Mb), fst=UD_FID * g["L36"] / (Mb / MSUN / 1e9)))
ab = np.array([r["a0"] for r in btf])
yb = np.array([r["y"] for r in btf])
Gb = np.array([r["Gam"] for r in btf])
raw_b = math.exp(float(np.mean(np.log(ab))))
lnBb = [float(np.mean(np.log(Qy(kf, yb) * Gb))) for kf in KERN.values()]
hs_b = 0.5 * (max(lnBb) - min(lnBb))
geo_b = math.exp(float(np.mean(lnBb)))
st_b = float(np.std(np.log(ab))) / math.sqrt(len(ab))
print(f"  {len(btf)} galaxies with a quality V_flat. raw V_flat^4/(G M_bar) = {raw_b:.4e} = "
      f"{raw_b/A0_CANON:.3f}x canonical -- and that excess is NOT a framework failure, it is Q x Gamma:")
print(f"    y at the outermost measured radius : median {np.median(yb):.3f}  (5-95% "
      f"{np.percentile(yb,5):.3f}-{np.percentile(yb,95):.3f})")
print(f"    Gamma = g_bar R^2/(G M_bar) at R_last (disc vs point mass): median {np.median(Gb):.3f}  "
      f"(16-84% {np.percentile(Gb,16):.3f}-{np.percentile(Gb,84):.3f})")
for kn, lb in zip(KERN, lnBb):
    print(f"    predicted bias <Q(y_out) Gamma> under {kn:<22} {math.exp(lb):.4f}  -> a0 = "
          f"{raw_b/math.exp(lb):.4e} ({raw_b/math.exp(lb)/A0_CANON:.3f}x)")
print(f"    shape-marginalised: a0 = {raw_b/geo_b:.4e} = {raw_b/geo_b/A0_CANON:.3f}x canonical; "
      f"shape {100*hs_b:.2f}%, ensemble stat {100*st_b:.2f}%")
check(abs(raw_b / A0_CANON - 1.0) > 0.15 and hs_b > GAP_LOG and np.median(Gb) > 1.0
      and math.hypot(hs_b, st_b) > GAP_LOG,
      f"S9 the BTFR does NOT escape the shape systematic, and the reason is worth stating plainly: its "
      f"'coefficient exactly 1' is Q(0) = 1, a statement about y = 0, while SPARC's outermost measured radii "
      f"sit at a median y = {np.median(yb):.2f}. The raw estimator therefore reads {raw_b/A0_CANON:.2f}x "
      f"canonical, and that {100*(raw_b/A0_CANON-1):.0f}% is fully accounted for by Q(y_out) x Gamma with "
      f"Gamma = {np.median(Gb):.2f} the measured disc-vs-point-mass factor at R_last -- not by a0 being wrong. "
      f"Shape-marginalising gives {raw_b/geo_b/A0_CANON:.2f}x canonical with a {100*hs_b:.1f}% shape and only "
      f"{100*st_b:.1f}% ensemble statistical error, i.e. the BTFR is the most statistically efficient of the "
      f"estimators here and still cannot reach the {100*GAP_LOG:.2f}% gap. It is also the cleanest "
      f"demonstration that the long-standing BTFR-vs-RAR a0 normalisation offset is a finite-radius Q effect")


banner("S10  WHAT THE CORPUS OWES: the a0-line's corrections, computed")


def bans(ahat, astar, s, W_dec=2.0, s_anchor=0.01):
    """B01 in bans for M0 {a0 fixed} vs M1 {a0 free, log-flat prior of width W_dec decades}, the a0-line's
    own formula: B01 = [W/(sqrt(2pi) s)] exp(-t^2/2), t = ln(a0*/ahat)/sqrt(s^2 + s_anchor^2)."""
    W = W_dec * math.log(10.0)
    t = math.log(astar / ahat) / math.sqrt(s * s + s_anchor * s_anchor)
    return math.log10(W / (math.sqrt(2 * math.pi) * s)) - t * t / (2 * math.log(10.0))


A0L_CANON, A0L_ALT, A0L_HAT, A0L_MED, S_PUB = 9.355e-11, 1.1305e-10, 1.181e-10, 0.973e-10, 0.161
pub = dict(canon=bans(A0L_HAT, A0L_CANON, S_PUB), alt=bans(A0L_HAT, A0L_ALT, S_PUB),
           canon3=bans(A0L_HAT, A0L_CANON, S_PUB / 3), alt3=bans(A0L_HAT, A0L_ALT, S_PUB / 3))
print(f"  first, the Occam machinery is validated by reproducing all FOUR published bans from the published")
print(f"  inputs (s = {S_PUB}, W = 2 decades, a_hat = 1.181e-10, s_anchor = 0.01):")
print(f"    headline  canonical {pub['canon']:+.3f} (published +0.60)   ALT {pub['alt']:+.3f} (published +1.04)")
print(f"    at sigma/3 canonical {pub['canon3']:+.3f} (published -2.45)   ALT {pub['alt3']:+.3f} "
      f"(published +1.39)")
check(abs(pub["canon"] - 0.60) < 0.05 and abs(pub["alt"] - 1.04) < 0.05
      and abs(pub["canon3"] + 2.45) < 0.10 and abs(pub["alt3"] - 1.39) < 0.05,
      f"S10a the published Occam ledger is reproduced exactly from its stated inputs -- {pub['canon']:+.2f} / "
      f"{pub['alt']:+.2f} bans headline and {pub['canon3']:+.2f} / {pub['alt3']:+.2f} at sigma/3, against the "
      f"published +0.60 / +1.04 and -2.45 / +1.39. So the corrected bans below are computed with the same "
      f"machinery on the same convention and are directly substitutable")

gasB = bias[("gas-dom", "LINE-GLS")]
deb_gls, deb_med = A0L_HAT / gasB["geo"], A0L_MED / gasB["geo"]
ra_gls = A0L_HAT / gasB["row"]["RouteA (adopted)"]
s_new = math.hypot(S_PUB, gasB["hs"])
print(f"\n  the gas-dominated a0-line, corrected for the shape systematic it never carried:")
print("    shape bias factors on THIS sample: "
      + ", ".join(f"{k.split(' (')[0]} {gasB['row'][k]:.4f}" for k in KERN)
      + f"  -> half-spread {100*gasB['hs']:.2f}%")
print(f"    GLS    1.181e-10 +- 16%  ->  shape-marginalised {deb_gls:.4e} +- {100*s_new:.1f}%   "
      f"(under Route A alone: {ra_gls:.4e})")
print(f"    median 0.973e-10         ->  shape-marginalised {deb_med:.4e}")
print(f"    Lambda = 3 Z^2 a0^2/c^4 : published 1.74e-52 (GLS) -> {1.74e-52*(deb_gls/A0L_HAT)**2:.3e}; "
      f"Planck 1.089e-52; ratio {1.59*(deb_gls/A0L_HAT)**2:.2f} at sigma_lnLambda = {2*s_new:.2f} "
      f"-> {math.log(1.74e-52*(deb_gls/A0L_HAT)**2/1.089e-52)/(2*s_new):+.2f} sigma (published +1.45)")
cor = dict(canon=bans(deb_gls, A0L_CANON, s_new), alt=bans(deb_gls, A0L_ALT, s_new),
           canon3=bans(ra_gls, A0L_CANON, S_PUB / 3), alt3=bans(ra_gls, A0L_ALT, S_PUB / 3))
print(f"    Occam  +0.60/+1.04 bans  ->  {cor['canon']:+.2f} canonical / {cor['alt']:+.2f} ALT")
print(f"    the advertised sigma/3 FALSIFICATION EXPOSURE, -2.45 bans against canonical, evaluated at the "
      f"Route-A-debiased central value instead: {cor['canon3']:+.2f} canonical / {cor['alt3']:+.2f} ALT")
check(gasB["hs"] > 0.05 and s_new > S_PUB and cor["canon3"] > 0.0 and abs(deb_gls / A0L_HAT - 1) > 0.05,
      f"S10b *** THE a0-LINE'S OWED CORRECTIONS, AND THEY CUT BOTH WAYS. *** Charging the shape systematic it "
      f"never carried moves the gas-dominated slope from 1.181e-10 +- 16% to {deb_gls:.3e} +- "
      f"{100*s_new:.0f}% shape-marginalised ({ra_gls:.3e} under the adopted kernel alone), which lands "
      f"NEARER both footings and softens the Lambda inversion from +1.45 sigma to "
      f"{math.log(1.74e-52*(deb_gls/A0L_HAT)**2/1.089e-52)/(2*s_new):+.2f} sigma -- favourable. But it also "
      f"DESTROYS the door's advertised falsification exposure: the '-2.45 bans against canonical if the "
      f"central value holds at sigma/3' becomes {cor['canon3']:+.2f} bans FOR canonical once the central value "
      f"is debiased onto the adopted kernel, and the sigma/3 reduction is itself unreachable while the "
      f"estimator stays shape-invariant, because {100*gasB['hs']:.0f}% of the budget no longer shrinks with "
      f"data. A measurement that cannot be sharpened cannot falsify; that is the real cost, and it is larger "
      f"than the cosmetic gain in the central value")

nHF = sum(1 for g in GG if g["fD"] == 1)
gas_gal = sorted(set(GIDX[ISGAS]))
mean2eD = float(np.mean([2 * GG[k]["eD"] / GG[k]["D"] for k in gas_gal]))
ens_pred = mean2eD / math.sqrt(len(gas_gal))
# EXACT first-order propagation of a per-galaxy distance error through the GLS slope, no 1/sqrt(N) shortcut:
#   a_hat = sum(w E g)/sum(w g^2),  dE_i/dlnD = -2 g_obs,i^2   =>   dln a_hat/dlnD_k = -2 sum_{i in k} w g
#   g_obs^2 / (a_hat sum w g^2).  Then sigma = sqrt(sum_k (lever_k sigma_lnD,k)^2) -- which correctly keeps the
# CORRELATION between which galaxies carry weight and which have bad distances.
fi_g = tune_fint(GB0[ISGAS], GO0[ISGAS], EVREL[ISGAS])
_a = line_gls(GB0[ISGAS], GO0[ISGAS], EVREL[ISGAS], fi_g)
_gb, _go, _gi = GB0[ISGAS], GO0[ISGAS], GIDX[ISGAS]
_gm2 = _gb ** 2 + _a * _gb
_w = 1.0 / np.hypot(4.0 * EVREL[ISGAS] * _gm2, fi_g * _gm2) ** 2
_den = float(np.sum(_w * _gb ** 2))
_num = _w * _gb * _go ** 2
lever = np.array([2.0 * float(np.sum(_num[_gi == k])) / (_a * _den) for k in gas_gal])
sig_lnD = np.array([2.0 * GG[k]["eD"] / GG[k]["D"] for k in gas_gal])
pred_D = float(np.sqrt(np.sum((lever * sig_lnD) ** 2)))
N_eff = float(np.sum(lever) ** 2 / np.sum(lever ** 2))
top = np.argsort(-np.abs(lever * sig_lnD))[:3]
print("\n  and the 'per-object vs ensemble' question the lane brief asks, answered on the numbers:")
print("    the published GAS-DOM distance term is 0.08e-10 on a 1.181e-10 central value = 6.8%.")
print(f"    2 <e_D/D> over those {len(gas_gal)} galaxies = {100*mean2eD:.1f}% PER GALAXY; divided by "
      f"sqrt({len(gas_gal)}) that is {100*ens_pred:.1f}% -- so 6.8% is an ENSEMBLE number, not a per-galaxy one.")
print(f"    but 1/sqrt(N) is the wrong average here. EXACT first-order propagation through the GLS slope, "
      f"keeping each galaxy's own lever and its own e_D:")
print(f"      sum(lever) = {float(np.sum(lever)):.2f} (the -2 total, split unequally), effective N = "
      f"{N_eff:.1f} of {len(gas_gal)}, and the three biggest single contributions are "
      + ", ".join(f"{GG[gas_gal[i]]['name']} {100*abs(lever[i]*sig_lnD[i]):.1f}%" for i in top))
print(f"      predicted ensemble distance term {100*pred_D:.1f}%;  this file's MC over the same quoted e_D "
      f"gives {100*res[('LINE','gas-dom')]['D']:.1f}%  ({res[('LINE','gas-dom')]['D']/0.068:.1f}x the charged "
      f"6.8%)")
check(abs(ens_pred / 0.068 - 1.0) < 0.5 and mean2eD > 3 * 0.068
      and res[("LINE", "gas-dom")]["D"] > 1.5 * 0.068
      and abs(pred_D / res[("LINE", "gas-dom")]["D"] - 1.0) < 0.35 and N_eff < 0.7 * len(gas_gal),
      f"S10c TWO findings, and the second is AGAINST INTEREST. (i) The +-16% budget was ALREADY an ensemble "
      f"number, not a per-galaxy one -- its 6.8% distance term is 2<e_D/D>/sqrt(N) = {100*mean2eD:.0f}%/"
      f"sqrt({len(gas_gal)}) = {100*ens_pred:.1f}%, against a {100*mean2eD:.0f}% PER-GALAXY value "
      f"{mean2eD/0.068:.0f}x larger. So EXECUTIVE_SUMMARY_2026-07-20_to_08-02.md's description of the +-16% as "
      f"'the per-galaxy budget' is a MISLABEL; its 16 -> 13% correction stands but for a different reason (13% "
      f"is the same ensemble budget at N -> infinity). (ii) That 1/sqrt(49) is nevertheless the WRONG AVERAGE, "
      f"and this is the part that is against interest: an exact first-order propagation that keeps each "
      f"galaxy's own GLS lever alongside its own quoted e_D predicts {100*pred_D:.1f}%, and a direct MC through "
      f"the same estimator gives {100*res[('LINE','gas-dom')]['D']:.1f}% -- agreeing with each other and both "
      f"about {res[('LINE','gas-dom')]['D']/0.068:.1f}x the charged 6.8%. The mechanism is a CORRELATION the "
      f"square-root law cannot see: the gas-dominated galaxies that carry the most weight are the same "
      f"Hubble-flow dwarfs that carry 25-30% distance errors, so effective N is {N_eff:.1f} rather than "
      f"{len(gas_gal)} and a handful of objects ({GG[gas_gal[top[0]]]['name']} alone contributes "
      f"{100*abs(lever[top[0]]*sig_lnD[top[0]]):.1f}%) dominate. The a0-line's distance systematic is "
      f"UNDER-charged, which is why this file's independent total for that same estimator is "
      f"{100*res[('LINE','gas-dom')]['tot']:.0f}% rather than the {100*math.hypot(0.16, gasB['hs']):.0f}% you "
      f"get by simply adding shape in quadrature to the published 16%")

h0 = {}
for H0 in (67.4, 70.0, 73.0, 74.6):
    Df = np.array([73.0 / H0 if g["fD"] == 1 else 1.0 for g in GG])
    gbh, goh = build(Dfac=Df)
    h0[H0] = est_deep(gbh, goh, ISGAS) / est_deep(GB0, GO0, ISGAS)
print(f"\n  one more coherent systematic nobody has charged: SPARC's {nHF} Hubble-flow distances assume "
      f"H0 = 73. a0 ~ 1/D^2, so")
print("    " + "   ".join(f"H0={k}: {v:.4f}x" for k, v in h0.items()))
check(abs(h0[67.4] - 1.0) > 0.05 and abs(h0[73.0] - 1.0) < 1e-12,
      f"S10d a COHERENT distance-scale systematic is missing from every a0 budget in this corpus: "
      f"{nHF} of {NG} galaxies carry Hubble-flow distances computed at H0 = 73, and a0 scales as 1/D^2, so "
      f"re-reading them at Planck's 67.4 moves the measured a0 by {100*(h0[67.4]-1):+.1f}% coherently -- "
      f"{abs(math.log(h0[67.4]))/GAP_LOG:.1f}x the kappa gap, and it does not average down. AGAINST INTEREST, "
      f"and this must be said in the same breath: the shift is TOWARD canonical, but the corpus's own "
      f"clean-distance work went the other way (a0_line_trgb found the TRGB-only central value +13% HIGHER, "
      f"not lower), so this lever is not evidence for the canonical footing. It is one more irreducible "
      f"term, and the honest use of it is to widen the error, not to move the answer")


banner("THE CORRECTION LIST for the primary agent -- documents NOT edited by this script")

print(f"""  Every item below is computed above. Nothing in prep_2026/, papers/, explainers/, STANDING.md or
  README.md has been touched.

  1. prep_2026/a0_line/A0_LINE.md, "THE EQUATION SET": the boxed claim
       g_obs^2 - g_bar^2 = a0 g_bar   "EXACTLY, at every acceleration"
     is TRUE ONLY FOR THE RETIRED alpha=1 KERNEL. Under the adopted Route A kernel it holds only as
     y -> 0, with a fractional error {100*(float(Qy(nu,0.03))-0.03-1):.0f}% at y = 0.03 and
     {100*(float(Qy(nu,0.3))-0.3-1):.0f}% at y = 0.3. RELABEL: "exact identity of the alpha=1 kernel; under
     Route A an asymptotic identity with O(sqrt(y)) corrections."

  2. Same file, E1: "a_hat_0^gas = (0.97-1.18)e-10 +- 16%" and the header claim "the sharpest available
     measurement". ADD the shape systematic {100*gasB['hs']:.1f}% -> +-{100*s_new:.0f}% by simple quadrature on
     the published 16%, or +-{100*res[('LINE','gas-dom')]['tot']:.0f}% on this file's independent budget for
     the same estimator (item 7), and re-centre:
       GLS    1.181e-10 -> {deb_gls:.3e} shape-marginalised ({ra_gls:.3e} under Route A alone)
       median 0.973e-10 -> {deb_med:.3e} shape-marginalised
     "Sharpest" survives only in the weak sense that every OTHER shape-invariant route also lands at
     {100*min(v['tot'] for v in res.values()):.0f}-{100*max(v['tot'] for v in res.values()):.0f}%.

  3. Same file, E2 (the Lambda inversion): 1.74e-52 / +1.45 sigma -> {1.74e-52*(deb_gls/A0L_HAT)**2:.3e} /
     {math.log(1.74e-52*(deb_gls/A0L_HAT)**2/1.089e-52)/(2*s_new):+.2f} sigma at sigma_lnLambda = {2*s_new:.2f}.
     The "factor 1.1-1.6 recovery of Lambda" becomes a factor {1.59*(deb_gls/A0L_HAT)**2:.2f}
     (GLS) / {1.08*(deb_med/A0L_MED)**2:.2f} (median) -- BETTER, not worse.

  4. Same file, E3 and the "WHAT SHARPENS IT NEXT" list: the headline bans go +0.60/+1.04 ->
     {cor['canon']:+.2f}/{cor['alt']:+.2f}. The advertised two-sided lever ("if the GLS central value holds at
     sigma/3, canonical goes to -2.45 bans") must be WITHDRAWN AS STATED: at the Route-A-debiased central
     value the same lever gives {cor['canon3']:+.2f} bans FOR canonical, and sigma/3 is unreachable at all
     while {100*gasB['hs']:.0f}% of the budget is shape systematic that no data reduce. Replace with: "the
     falsification exposure exists only CONDITIONAL on a fixed transition kernel."

  5. real_research/reviews/mi_routeA_a0_estimator_invariance_2026.py, E5: the a0-line's quoted shape biases
     "+10.3% (Route A) / -83.6% (alpha=2)" are LOG-UNIFORM-GRID artefacts. On the real FULL sample with the
     real GLS weights: {100*(ln_full['RouteA (adopted)']-1):+.1f}% / {100*(ln_full['alpha=2 (superseded)']-1):+.1f}%.
     On the GAS-DOM sample the 1.181e-10 comes from:
     {100*(gasB['row']['RouteA (adopted)']-1):+.1f}% / {100*(gasB['row']['alpha=2 (superseded)']-1):+.1f}%.
     Same sign, different magnitudes; the GAS number is the one the standing needs.

  6. Same file, docstring vs code: "the 8.20% gap between kappa = 1/2 and kappa = 1/2pi" is the LOG gap while
     the script's own KAPPA_GAP constant is the {100*gap_of_canon:.2f}% ratio-of-canonical. Both are right
     about different objects; since a0 errors here are fractional, quote {100*GAP_LOG:.3f}%
     ({GAP_LOG/math.log(10):.4f} dex) and say which.

  7. EXECUTIVE_SUMMARY_2026-07-20_to_08-02.md section 4 item 3 ("Per-object != ensemble: the a0-line row used
     the per-galaxy +-16% budget"): the +-16% is ALREADY an ensemble budget (its distance term is
     {100*mean2eD:.0f}%/sqrt({len(gas_gal)}) = {100*ens_pred:.1f}%, not the {100*mean2eD:.0f}% per-galaxy
     value). The 16 -> 13% correction stands but for a different reason -- 13% is the N -> infinity floor of
     the SAME ensemble budget. Fix the label, keep the number, and note that with shape charged the floor is
     {100*math.hypot(0.13, gasB['hs']):.0f}%, not 13%. SEPARATELY AND AGAINST INTEREST: the 1/sqrt(49) in that
     ensemble average is too optimistic for the GLS estimator, whose weights w g^2 ~ g^-2 give a Kish
     effective sample size of only {N_eff:.1f} galaxies -- the heavily-weighted gas dwarfs are the same
     objects with 25-30% Hubble-flow distance errors. Exact propagation gives {100*pred_D:.1f}% and the MC
     {100*res[('LINE','gas-dom')]['D']:.1f}%, not 6.8%; this file's independent total for the same estimator
     is {100*res[('LINE','gas-dom')]['tot']:.0f}%.

  8. NEW, owed everywhere a0 is measured from SPARC: a coherent H0 systematic. {nHF} of {NG} galaxies have
     Hubble-flow distances at H0 = 73; a0 ~ 1/D^2 gives {100*(h0[67.4]-1):+.1f}% at H0 = 67.4. Not in any
     budget in the corpus. Widens; does not decide.

  9. Anywhere the BTFR is quoted as giving "a0 with coefficient exactly 1": the coefficient is exactly 1 at
     y = 0. At SPARC's outermost radii (median y = {np.median(yb):.2f}) the raw estimator reads
     {raw_b/A0_CANON:.2f}x canonical, and Q(y_out) x Gamma accounts for all of it. RELABEL, do not retract:
     the theorem is asymptotic and the data are not asymptotic.

 10. NOT a correction, a warning for future lanes: the deep-limit-only likelihood is EXACTLY degenerate in
     a0 x Upsilon once the gas is removed (S4). Any future "deep-only, shape-free" a0 measurement is really a
     measurement of the gas fraction times a Upsilon prior. Say so up front.""")


banner("SCOPE AND WHAT IS NOT CLAIMED")
print(f"""  ESTABLISHED HERE:
   * Q(y) = nu^2 y is the exact, kernel-labelled bias of every deep-limit a0 estimator, and Route A's
     Q = 1 + sqrt(y) + (5/12)y + (1/12)y^(3/2) approaches 1 as sqrt(y) -- the SLOWEST in the family (S2).
   * SPARC has {census['3 sigma'][0]} points deep enough for the shape systematic to permit a 3-sigma kappa
     test and {census['1 sigma'][0]} deep enough to get it below the gap itself (S3).
   * a genuinely shape-invariant estimator exists -- the sqrt(y)-intercept, unbiased to {100*sq1:.2f}% across
     four kernels and independent of the reference a0 (S6) -- but it pays in variance, {100*res[('SQRTY','all y<1')]['stat']:.0f}%
     statistical (S7).
   * every shape-invariant route totals {100*min(v['tot'] for v in res.values()):.0f}-{100*max(v['tot'] for v in res.values()):.0f}%;
     best {100*bb['tot']:.1f}% ({bk[0]}, {bk[1]}); kappa separation {sig:.2f} sigma. NO.
   * the N-independent floor {100*floor:.1f}% is {floor/need_sigma3:.1f}x the 3-sigma budget, so BIG-SPARC
     does not rescue it either.
   * the corpus's own a0-line is reproduced to <1% (S5) and its owed corrections are computed (S10).

  NOT CLAIMED:
   * NOT that the framework fails. The best shape-invariant central value sits
     {math.log(bb['deb']/A0_CANON)/bb['tot']:+.2f} sigma from canonical, {math.log(bb['deb']/A0_ALT)/bb['tot']:+.2f}
     from ALT and {math.log(bb['deb']/A0_M20)/bb['tot']:+.2f} from Milgrom's 1/2pi; that is non-discrimination,
     not deficit -- and it does NOT lean kappa = 1/2. The Route-A-debiased a0-line moves ONTO canonical,
     which is a favourable arithmetic change and is reported as such -- and it costs the door its
     falsification exposure, which is reported in the same breath.
   * NOT that kappa = 1/2 is wrong. It is unmeasured by this data at any useful significance.
   * a0 is an INPUT throughout. The estimators MEASURE it in order to compare against the two footings as
     postulates; nothing here is tuned to improve a framework prediction.
   * the four-kernel family is a CHOICE. A narrower family (Route A alone) gives no shape systematic but no
     shape-invariance either; a wider one gives more. Note that alpha=1 and alpha=2 were retired on their
     NEWTONIAN tails, which leaves them perfectly legitimate members of a DEEP-limit shape family -- the
     shape systematic on a deep estimator does NOT shrink because they were retired.
   * BOTH footings carried: canonical {A0_CANON:.4e}, ALT {A0_ALT:.4e} ({A0_ALT/A0_CANON:.4f}x). The footing
     fork is {100*math.log(A0_ALT/A0_CANON):.1f}% in the log, i.e. {math.log(A0_ALT/A0_CANON)/bb['tot']:.2f}
     of this measurement's total error -- SPARC does not decide it either.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: a shape-invariant a0 estimator was built and priced. It does not resolve kappa, the reason")
print("  is dynamic range rather than sample size, and the a0-line's owed corrections are computed above.")
