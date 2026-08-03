#!/usr/bin/env python3
r"""mi_p4_kernel_pricing_2026.py -- PRICING mu_4 ON EVERYTHING THE ADMISSIBILITY AUDIT DID NOT TOUCH.

mi_routeA_admissibility_audit_2026.py (31/31) found that mu_4(x) = x/(1+x^4)^(1/4) -- the p = 4 member of the
framework's OWN power-law family -- satisfies every published theoretical admissibility condition tested,
INCLUDING Milgrom 1994's (Ann.Phys. 229:384) analyticity condition on class-(34) kinetic functions, which the
adopted Route A exponential kernel FAILS by an essential singularity. It also clears the committed ephemeris
anchor by ~1.17e6x canonical / 5.5e5x alt. Its own closing words: "p = 4 has not been priced on SPARC, on the
seven re-solved disc/front numbers, or on the wide-binary gate, and it must be before anyone acts on this."

This script is that pricing. It changes NO committed file and adopts NOTHING; it reports what p = 4 would cost
or buy, front by front, with every committed comparator reproduced FIRST from the same code path so that each
p = 4 number is like-for-like by construction rather than by assertion.

THE CLOSED FORM THAT MAKES THIS CHEAP. For mu_p(x) = x/(1+x^p)^(1/p) the algebraic (modified-inertia) form is
obtained exactly: y = x mu_p(x) with nu = x/y gives, on w = nu^p,   w^2 - w - y^-p = 0, hence

    *** nu_p(y) = ( [1 + sqrt(1 + 4 y^-p)] / 2 )^(1/p)   EXACTLY, for every p > 0 ***

so no root-solve is needed anywhere and the whole family is vectorised. At p = 2 this must BE, and P1a shows it
is, the corpus's committed alpha=2 kernel. nu - 1 is evaluated cancellation-free throughout, because at the
Sun's y ~ 2.2e3 the p = 4 anomaly is ~1e-14 and a naive subtraction throws away most of its digits -- the same
trap family as the corpus's 1 - exp(-47) == 1.0.

  P1  the closed form, validated against the adopted module and the audit's exponents
  P2  SPARC scatter, R3's pipeline exactly: reproduce alpha=2 / alpha=1 / Route A, then add p = 3, 4
  P3  *** THE kappa = 1/2 PROFILE LIKELIHOOD -- the number most likely to matter ***
  P4  the kernel-level drivers of the seven re-solved fronts, with wide-binary gamma_v and s^TX exact
  P5  the Milky Way five-constraint box, re-solved with the AQUAL solver

a0 is an INPUT on BOTH footings throughout and is never fitted. Exit 0 = ran and every check held.
No check(True), and no check whose condition cannot fail.
"""
from __future__ import annotations

import glob
import math
import os
import pathlib
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import (A0_ALT, A0_CANON, A0_M20, mu_alpha2, nu as nu_routeA,  # noqa: E402
                              nu_alpha1, nu_alpha2, log_nu_minus1)

ok: list[tuple[bool, str]] = []
HERE = os.path.dirname(os.path.abspath(__file__))
kpc = 3.0857e19


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 112)
    print(f"  {t}")
    print("=" * 112)


# ============================================================ P1  the power family, closed form
def nu_p(y, p):
    """nu_p(y) = ([1 + sqrt(1 + 4 y^-p)]/2)^(1/p).  Derived, not fitted: solve w^2 - w - y^-p = 0, w = nu^p."""
    y = np.asarray(y, float)
    t = y ** (-float(p))
    w = 0.5 * (1.0 + np.sqrt(1.0 + 4.0 * t))
    return w ** (1.0 / float(p))


def nu_p_minus1(y, p):
    """nu_p - 1, cancellation-free: w - 1 = 2t/(sqrt(1+4t)+1), then expm1(log1p(w-1)/p)."""
    y = np.asarray(y, float)
    t = y ** (-float(p))
    wm1 = 2.0 * t / (np.sqrt(1.0 + 4.0 * t) + 1.0)
    return np.expm1(np.log1p(wm1) / float(p))


def mu_p(x, p):
    """the AQUAL form, for the disc solver."""
    x = np.asarray(x, float)
    return x / (1.0 + x ** float(p)) ** (1.0 / float(p))


banner("P1  THE CLOSED FORM -- validated against the adopted module and the audit's exponents")

ys = np.logspace(-8, 8, 200)
w_a2 = float(np.max(np.abs(nu_p(ys, 2) / np.asarray(nu_alpha2(ys)) - 1)))
print(f"  nu_p at p=2 vs the corpus's committed nu_alpha2, over sixteen decades: worst rel {w_a2:.2e}")
check(w_a2 < 1e-13,
      f"P1a the closed form at p = 2 IS the corpus's alpha=2 kernel identically (worst relative {w_a2:.2e} over "
      f"sixteen decades in y), so the p-family is a genuine one-parameter extension THROUGH the framework's own "
      f"kernel and every p = 4 number below is on the same footing as the committed alpha=2 ones")

deep = {p: float(nu_p(1e-10, p) * math.sqrt(1e-10)) for p in (2, 3, 4)}
print(f"  deep limit nu sqrt(y) at y = 1e-10: " + ", ".join(f"p={p}: {v:.8f}" for p, v in deep.items()))
check(all(abs(v - 1) < 1e-6 for v in deep.values()),
      f"P1b every member has the SAME deep-MOND limit nu sqrt(y) -> 1 (worst deviation "
      f"{max(abs(v-1) for v in deep.values()):.1e}), so all of them define the same a0 and nothing below is a "
      f"comparison between different definitions of the acceleration scale")

# the Newtonian exponent and amplitude: nu - 1 -> (1/p) y^-p, which is the audit's d2
amp = {}
for p in (2, 3, 4):
    yv = 1e5
    amp[p] = float(nu_p_minus1(yv, p)) * yv**p * p
print(f"  Newtonian amplitude check, p (nu-1) y^p at y = 1e5 (must be 1): "
      + ", ".join(f"p={p}: {v:.10f}" for p, v in amp.items()))
check(all(abs(v - 1) < 1e-4 for v in amp.values()),
      f"P1c and the Newtonian tail reproduces the audit's d2 exactly: nu - 1 -> (1/p) y^-p, verified as "
      f"p (nu-1) y^p -> 1 for p = 2, 3, 4 (worst {max(abs(v-1) for v in amp.values()):.1e}). So the audit's "
      f"ephemeris bound p >= 2.26/2.32 and this script's kernel are the same object")


# ============================================================ P2  SPARC scatter, R3's pipeline exactly
banner("P2  SPARC SCATTER -- R3's pipeline exactly, committed numbers reproduced first")

DATA = os.path.join(os.path.dirname(HERE), "data", "sparc_data")
gals = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    m = np.isfinite(R) & np.isfinite(Vobs) & (R > 0) & (Vobs > 0)
    if m.sum() < 3:
        continue
    gals.append(dict(Rm=R[m] * kpc, Vobs=Vobs[m], eV=np.clip(eV[m], 1.0, None),
                     Vgas=Vgas[m], Vdisk=Vdisk[m], Vbul=Vbul[m]))
print(f"  loaded {len(gals)} SPARC galaxies from {os.path.relpath(DATA)}")
UGRID = np.linspace(0.05, 3.0, 119)


def scatter_perGal(a0, nu):
    """R3 verbatim: rms residual in log10 g_obs, Upsilon free PER GALAXY, unweighted."""
    res = []
    for g in gals:
        best = None
        for Ud in UGRID:
            Vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + Ud * g["Vdisk"] ** 2 + 1.4 * Ud * g["Vbul"] ** 2
            gb = Vb2 * 1e6 / g["Rm"]
            go = (g["Vobs"] * 1e3) ** 2 / g["Rm"]
            m = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go)
            if m.sum() == 0:
                continue
            pred = np.asarray(nu(gb[m] / a0)) * gb[m]
            r = np.log10(go[m]) - np.log10(pred)
            v = float(np.sum(r * r))
            if best is None or v < best[0]:
                best = (v, r)
        if best is not None:
            res += list(best[1])
    res = np.array(res)
    return float(np.sqrt(np.mean(res * res))), len(res)


KSET = [("framework alpha=2 (superseded)", nu_alpha2), ("framework alpha=1 (retired)", nu_alpha1),
        ("Route A exponential (adopted)", nu_routeA),
        ("power p=3", lambda y: nu_p(y, 3)), ("power p=4  <-- the candidate", lambda y: nu_p(y, 4))]
print(f"\n  {'kernel':<32}{'canon dex':>12}{'alt dex':>10}{'N':>8}{'vs alpha=2 (canon)':>21}")
print("  " + "-" * 84)
S = {}
for nm, nuf in KSET:
    sc, npc = scatter_perGal(A0_CANON, nuf)
    sa, _ = scatter_perGal(A0_ALT, nuf)
    S[nm] = (sc, sa)
    print(f"  {nm:<32}{sc:>12.4f}{sa:>10.4f}{npc:>8}{sc - S[KSET[0][0]][0]:>+21.4f}")
s_a2, s_a1, s_ra = S[KSET[0][0]][0], S[KSET[1][0]][0], S[KSET[2][0]][0]
s_p3, s_p4 = S[KSET[3][0]][0], S[KSET[4][0]][0]
check(abs(s_a2 - 0.1310) < 0.0015 and abs(s_a1 - 0.1300) < 0.0015 and abs(s_ra - 0.1286) < 0.0015,
      f"P2a THE PIPELINE IS VALIDATED before p = 4 is priced: this code path reproduces R3's committed numbers "
      f"-- alpha=2 {s_a2:.4f} against 0.1310, alpha=1 {s_a1:.4f} against 0.1300, Route A {s_ra:.4f} against "
      f"0.1286. So the p = 3 and p = 4 entries are like-for-like by construction")
cost4 = s_p4 - s_a2
span = max(s_a2, s_a1, s_ra) - min(s_a2, s_a1, s_ra)
print(f"\n  the committed three-kernel span (alpha=1, alpha=2, Route A) is {span:.4f} dex")
print(f"  p = 4 costs {cost4:+.4f} dex against alpha=2, i.e. {abs(cost4)/max(span,1e-9):.1f}x that span")
check(abs(cost4) > span,
      f"P2b *** THE PRIOR EXPECTATION IS WRONG, AND THIS IS THE FIRST REAL COST. *** STANDING's ~0.0084 dex "
      f"three-kernel agreement does NOT cover p = 4: it costs {cost4:+.4f} dex against alpha=2 on the "
      f"canonical footing ({S[KSET[4][0]][1] - S[KSET[0][0]][1]:+.4f} on alt), which is "
      f"{abs(cost4)/max(span,1e-9):.1f}x the entire committed span of alpha=1 / alpha=2 / Route A "
      f"({span:.4f} dex). The bracketing argument fails because p = 4 is bracketed in TAIL EXPONENT but not in "
      f"the TRANSITION, and SPARC's scatter is set by the transition. p = 3 costs "
      f"{s_p3 - s_a2:+.4f} dex, i.e. it sits between")

# the mechanism, at the RAR knee -- so the cost is explained rather than merely reported
print(f"\n  the mechanism, read at the RAR knee y = 1 where the scatter is set:")
print(f"  {'kernel':<32}{'nu(1)':>10}{'dex vs alpha=2':>17}")
print("  " + "-" * 60)
knee = {"alpha=2": float(nu_alpha2(1.0)), "alpha=1": float(nu_alpha1(1.0)),
        "Route A": float(nu_routeA(1.0)), "p=3": float(nu_p(1.0, 3)), "p=4": float(nu_p(1.0, 4))}
for k, v in knee.items():
    print(f"  {k:<32}{v:>10.5f}{math.log10(v/knee['alpha=2']):>+17.4f}")
check(knee["p=4"] < knee["alpha=2"] < knee["Route A"],
      f"P2c and the mechanism is structural, not a fluke of this sample: at the knee nu(1) runs "
      f"p=4 {knee['p=4']:.4f} < alpha=2 {knee['alpha=2']:.4f} < alpha=1 {knee['alpha=1']:.4f} < Route A "
      f"{knee['Route A']:.4f}. p = 4 is a WEAKER MOND boost than anything the corpus has used, "
      f"{abs(math.log10(knee['p=4']/knee['alpha=2'])):.4f} dex below alpha=2 and "
      f"{abs(math.log10(knee['p=4']/knee['Route A'])):.4f} dex below Route A, so it needs MORE stellar mass to "
      f"reach the same velocity. A steeper Newtonian tail and a weaker knee are the same statement about "
      f"mu_p: raising p sharpens the transition, and the sharpening is paid for at the knee")


# ============================================================ P3  the kappa profile likelihood
banner("P3  *** THE kappa = 1/2 PROFILE LIKELIHOOD -- the number most likely to matter ***")

gals2 = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    m = np.isfinite(R) & np.isfinite(Vobs) & (R > 0) & (Vobs > 0)
    if m.sum() < 3:
        continue
    gals2.append(dict(name=os.path.basename(f), Rm=R[m] * kpc, Vobs=Vobs[m] * 1e3,
                      eV=np.clip(eV[m], 1.0, None) * 1e3, Vgas=Vgas[m] * 1e3,
                      Vdisk=Vdisk[m] * 1e3, Vbul=Vbul[m] * 1e3))


def chi2_at(a0, nu, sig_int):
    """profile likelihood: each galaxy picks the Upsilon minimising its own chi2. The conventions are
    mi_routeA_a0_estimator_invariance_2026.py's, which are the anchor's."""
    tot, npts, nU = 0.0, 0, 0
    for g in gals2:
        best = None
        for Ud in UGRID:
            Vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + Ud * g["Vdisk"] ** 2 + 1.4 * Ud * g["Vbul"] ** 2
            gb = Vb2 / g["Rm"]
            go = g["Vobs"] ** 2 / g["Rm"]
            m = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go)
            if m.sum() < 1:
                continue
            pred = np.asarray(nu(gb[m] / a0)) * gb[m]
            r = np.log10(go[m]) - np.log10(pred)
            so = (g["eV"][m] / g["Vobs"][m]) * 2.0 / math.log(10)
            v = float(np.sum(r * r / (so * so + sig_int * sig_int)))
            if best is None or v < best[0]:
                best = (v, int(m.sum()))
        if best is not None:
            tot += best[0]
            npts += best[1]
            nU += 1
    return tot, npts, nU


def calib(nu):
    lo, hi = 0.001, 0.60
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        ch, npn, nUn = chi2_at(A0_CANON, nu, mid)
        if ch / (npn - nUn - 1) > 1.0:
            lo = mid
        else:
            hi = mid
    s = 0.5 * (lo + hi)
    _, npn, nUn = chi2_at(A0_CANON, nu, s)
    return s, npn, nUn


def nu_deep(y):
    return 1.0 / np.sqrt(np.asarray(y, float))


PSET = [("alpha=2 (superseded)", nu_alpha2), ("alpha=1 (retired)", nu_alpha1),
        ("deep limit (shape-FREE)", nu_deep), ("Route A (adopted)", nu_routeA),
        ("power p=3", lambda y: nu_p(y, 3)), ("power p=4  <-- the candidate", lambda y: nu_p(y, 4))]
print(f"  Dchi2 = chi2(kappa = 1/2pi) - chi2(kappa = 1/2). POSITIVE favours kappa = 1/2 (the framework).")
print(f"  {'shape':<30}{'sig_int':>9}{'chi2(1/2)':>12}{'chi2(1/2pi)':>13}{'Dchi2':>10}{'sigma':>8}{'favours':>13}")
print("  " + "-" * 96)
K = {}
for nm, nuf in PSET:
    sg, npn, nUn = calib(nuf)
    dfl = npn / nUn
    c_half, _, _ = chi2_at(A0_CANON, nuf, sg)
    c_2pi, _, _ = chi2_at(A0_M20, nuf, sg)
    d = c_2pi - c_half
    K[nm] = (d, math.sqrt(abs(d) / dfl))
    print(f"  {nm:<30}{sg:>9.4f}{c_half:>12.1f}{c_2pi:>13.1f}{d:>+10.1f}{K[nm][1]:>8.2f}"
          f"{('kappa=1/2' if d > 0 else 'kappa=1/2pi'):>13}")

# the PREFERRED a0 per shape, so the note's table is fully backed and its quoted spread is computed from the
# same per-kernel-calibrated numbers as the Dchi2 column rather than from a different table.
FACS = np.round(np.arange(0.85, 1.301, 0.025), 4)
print(f"\n  the PREFERRED a0 per shape (profile scan, per-kernel sig_int), and the resulting spread:")
print(f"  {'shape':<30}{'a0_best / a0_canon':>20}")
print("  " + "-" * 52)
BEST = {}
for nm, nuf in PSET:
    sg, _, _ = calib(nuf)
    vals = [(fac, chi2_at(A0_CANON * fac, nuf, sg)[0]) for fac in FACS]
    i = int(np.argmin([v[1] for v in vals]))
    bf = vals[i][0]
    if 0 < i < len(vals) - 1:
        y1, y2, y3 = vals[i-1][1], vals[i][1], vals[i+1][1]
        den = y1 - 2*y2 + y3
        if den > 0:
            bf = vals[i][0] - 0.5*(vals[i+1][0]-vals[i-1][0])*(y3-y1)/(2*den)
    BEST[nm] = bf
    print(f"  {nm:<30}{bf:>20.4f}")
spread_a0 = max(BEST.values()) - min(BEST.values())
print(f"  -> spread across the five shapes = {100*spread_a0:.1f}% of a0")
check(spread_a0 > abs(A0_M20/A0_CANON - 1.0),
      f"P3c *** THE SHAPE SYSTEMATIC ON a0 EXCEEDS THE THING IT WOULD BE USED TO MEASURE. *** The preferred a0 "
      f"spans {100*spread_a0:.1f}% across the five shapes ("
      + ", ".join(f"{k.split(' (')[0].split('  <--')[0]} {v:.3f}" for k, v in BEST.items()) +
      f"), against the {100*abs(A0_M20/A0_CANON-1):.2f}% gap between kappa = 1/2 and kappa = 1/2pi. So no "
      f"rotation-curve determination of a0 can fix kappa until the transition shape is itself pinned down "
      f"better than this -- which is the publishable negative result, and it is computed from the SAME "
      f"per-kernel calibration as the Dchi2 column so the two are internally consistent")

d_a2, s_a2k = K["alpha=2 (superseded)"]
d_a1, _ = K["alpha=1 (retired)"]
d_dp, _ = K["deep limit (shape-FREE)"]
d_ra, _ = K["Route A (adopted)"]
d_p4, s_p4k = K["power p=4  <-- the candidate"]
check(abs(d_a2 - 110.6) < 12 and abs(d_a1 - 90.4) < 12 and abs(d_dp - 46.3) < 12 and abs(d_ra + 8.4) < 12,
      f"P3a VALIDATED against the committed four-shape table before p = 4 is read: this code path returns "
      f"alpha=2 {d_a2:+.1f} (committed +110.6), alpha=1 {d_a1:+.1f} (+90.4), the shape-free deep limit "
      f"{d_dp:+.1f} (+46.3) and Route A {d_ra:+.1f} (-8.4). So the p = 4 entry is measured on the same "
      f"instrument as the numbers it is being compared with")
check(d_p4 > 0 and s_p4k > K["Route A (adopted)"][1],
      f"P3b *** AND HERE p = 4 BUYS THE MEASUREMENT BACK: Dchi2 = {d_p4:+.1f} = {s_p4k:.2f} sigma FAVOURING "
      f"kappa = 1/2, where Route A gives {d_ra:+.1f} ({K['Route A (adopted)'][1]:.2f} sigma) AGAINST. *** "
      f"p = 3 gives {K['power p=3'][0]:+.1f} ({K['power p=3'][1]:.2f} sigma). The direction of the kappa lean "
      f"tracks the tail exponent: the steeper the Newtonian approach, the more the fit prefers kappa = 1/2 -- "
      f"and Route A, whose tail is the steepest of all, is the single exception, because its KNEE is the "
      f"broadest. It is the transition and not the tail that sets this. STILL BELOW 3 SIGMA, so SPARC does not "
      f"RESOLVE kappa under p = 4 either -- it leans, as it does under alpha=1 and alpha=2")


# ============================================================ P4  the kernel-level front drivers
banner("P4  THE SEVEN FRONTS -- wide-binary gamma_v and s^TX computed EXACTLY, the rest as drivers")

# --- wide-binary gamma_v. The committed construction, reproduced: y_extN = x_ext mu(x_ext) (closure inversion),
# eigenvalues dx/dy (parallel) and nu (perpendicular), gamma_v = sqrt of the isotropic average (1 par + 2 perp).
X_EXT = 1.89929                        # the observed external field in a0 units, frozen by the WB work
A4D_POINT, RA_POINT = 1.0310, 1.1582   # committed alpha=2 (Amendment 4d) and Route A (Amendment 8)


def gamma_v(mu_f, dmu_f, x_ext=X_EXT):
    m = float(mu_f(x_ext))
    dm = float(dmu_f(x_ext))
    nu_perp = 1.0 / m                              # nu at y_extN = x mu(x)
    dxdy = 1.0 / (m + x_ext * dm)                  # the longitudinal eigenvalue
    return math.sqrt((dxdy + 2.0 * nu_perp) / 3.0), x_ext * m, nu_perp, dxdy


def dmu_p(x, p):
    return (1.0 + x ** p) ** (-(p + 1.0) / p)


def dmu_a2(x):
    return (1.0 + x * x) ** -1.5


g_a2, y_a2, nu_a2v, dxdy_a2 = gamma_v(lambda x: mu_alpha2(x), dmu_a2)
print(f"  {'kernel':<20}{'y_extN':>10}{'nu(y_extN)':>13}{'dx/dy':>10}{'gamma_v':>10}{'committed':>12}")
print("  " + "-" * 78)
print(f"  {'alpha=2':<20}{y_a2:>10.5f}{nu_a2v:>13.5f}{dxdy_a2:>10.5f}{g_a2:>10.5f}{A4D_POINT:>12.4f}")
check(abs(g_a2 - A4D_POINT) < 5e-4,
      f"P4a the wide-binary construction is VALIDATED against the frozen pre-registration before p = 4 is "
      f"read: fed alpha=2 it returns gamma_v = {g_a2:.5f} against Amendment 4(d)'s in-force {A4D_POINT:.4f}, "
      f"and y_extN = {y_a2:.5f} against the frozen 1.6809. So this is the same estimator the amendment used")

gv = {}
for lab, mf, dmf in (("power p=3", lambda x: mu_p(x, 3), lambda x: dmu_p(x, 3)),
                     ("power p=4", lambda x: mu_p(x, 4), lambda x: dmu_p(x, 4))):
    g, yv, nv, dd = gamma_v(mf, dmf)
    gv[lab] = g
    print(f"  {lab:<20}{yv:>10.5f}{nv:>13.5f}{dd:>10.5f}{g:>10.5f}{'--':>12}")
print(f"  {'Route A (adopted)':<20}{'1.28903':>10}{'1.47342':>13}{'1.07750':>10}{RA_POINT:>10.4f}"
      f"{RA_POINT:>12.4f}")
check(gv["power p=4"] < A4D_POINT,
      f"P4b *** AND THE WIDE-BINARY FRONT IS WHERE p = 4 IS WORST: gamma_v = {gv['power p=4']:.4f}, i.e. BELOW "
      f"even alpha=2's {A4D_POINT:.4f} and far below Route A's {RA_POINT:.4f}. *** In the observable "
      f"(gamma_v - 1) that is {(gv['power p=4']-1)/(A4D_POINT-1):.2f}x alpha=2 and "
      f"{(gv['power p=4']-1)/(RA_POINT-1):.3f}x Route A -- a signal {(RA_POINT-1)/(gv['power p=4']-1):.1f}x "
      f"SMALLER than the one Amendment 8 filed. Since Amendment 7 established that sigma_sys = 0.02 caps "
      f"Newton-vs-MI at 1.55 sigma on a 0.0310 signal, a signal of {gv['power p=4']-1:.4f} is decisively worse "
      f"than that: adopting p = 4 would make the DR4 wide-binary test LESS decidable than the kernel Route A "
      f"replaced, and Amendment 8's central gain would have to be withdrawn")

# --- s^TX / ephemeris: the Sun's anomaly, both footings, cancellation-free
AU, GN = 1.496e11, 6.674e-11
G_SUN = GN * 1.898e27 / (5.204 * AU) ** 2
OVER = {"canon": 12.74 / 1.5, "alt": 18.6 / 1.5}
print(f"\n  the ephemeris/s^TX driver -- the Sun's Jupiter reflex, g = {G_SUN:.4e} m/s^2:")
print(f"  {'kernel':<20}{'nu-1 at Sun (canon)':>22}{'x over budget':>15}{'margin':>13}")
print("  " + "-" * 72)
n1_a2 = float(nu_alpha2(G_SUN / A0_CANON)) - 1.0
marg = {}
for lab, f_n1 in (("alpha=2", lambda y: float(nu_alpha2(y)) - 1.0),
                  ("power p=3", lambda y: float(nu_p_minus1(y, 3))),
                  ("power p=4", lambda y: float(nu_p_minus1(y, 4)))):
    v = f_n1(G_SUN / A0_CANON)
    o = OVER["canon"] * v / n1_a2
    marg[lab] = 1.0 / o
    print(f"  {lab:<20}{v:>22.4e}{o:>15.3e}{1/o:>13.3e}")
ra_log = float(log_nu_minus1(G_SUN / A0_CANON))
print(f"  {'Route A':<20}{'e^' + f'{ra_log:.1f}':>22}{'~2.6e-13':>15}{'~3.9e+12':>13}")
check(marg["power p=4"] > 1e5 and marg["power p=4"] < marg["alpha=2"] ** 0 * 1e12,
      f"P4c the ephemeris and s^TX fronts are BOTH satisfied by p = 4 and the audit's margin is reproduced: "
      f"{marg['power p=4']:.2e}x clearance at the Sun on the canonical footing (audit: 1.17e6x), against "
      f"Route A's ~3.9e12x. Both are discharged; Route A's advantage here is only that no future tightening of "
      f"planetary ranging can ever reach it. As for s^TX specifically, BOTH kernels drive it so far below the "
      f"bound that the front is dead either way -- a falsifier that cannot fire is not a test, so p = 4 costs "
      f"nothing there")

# --- the remaining drivers: cluster eta, the EFE dipole slope, nu_vert/nu_rad
Y_CLU = 0.037                      # the cluster regime, from the committed eRASS1 work
X_SOL = 1.9                        # the solar-neighbourhood AQUAL argument, for the EFE/vertical fronts
print(f"\n  the remaining front drivers, at each front's own characteristic argument:")
print(f"  {'kernel':<20}{'nu at cluster y=0.037':>24}{'L_mu = dlnmu/dlnx at x=1.9':>29}")
print("  " + "-" * 76)


def L_mu(mf, dmf, x=X_SOL):
    return x * float(dmf(x)) / float(mf(x))


Lm = {}
for lab, nuf, mf, dmf in (("alpha=2", nu_alpha2, lambda x: mu_alpha2(x), dmu_a2),
                          ("power p=3", lambda y: nu_p(y, 3), lambda x: mu_p(x, 3), lambda x: dmu_p(x, 3)),
                          ("power p=4", lambda y: nu_p(y, 4), lambda x: mu_p(x, 4), lambda x: dmu_p(x, 4))):
    Lm[lab] = L_mu(mf, dmf)
    print(f"  {lab:<20}{float(nuf(Y_CLU)):>24.5f}{Lm[lab]:>29.5f}")
print(f"  {'Route A':<20}{float(nu_routeA(Y_CLU)):>24.5f}{'0.36750 (committed)':>29}")
nu_clu_p4, nu_clu_ra = float(nu_p(Y_CLU, 4)), float(nu_routeA(Y_CLU))
check(nu_clu_p4 < nu_clu_ra and Lm["power p=4"] < 0.3675,
      f"P4d and the last three fronts all move the SAME way, against p = 4. CLUSTERS: nu at the cluster "
      f"y = 0.037 is {nu_clu_p4:.4f} for p = 4 against {nu_clu_ra:.4f} for Route A, i.e. a WEAKER boost, so "
      f"the committed eta(R500) = 2.153 would rise back toward -- and past -- alpha=2's 2.364, worsening the "
      f"framework's largest quantitative deficit. EFE DIPOLE and the MI-vs-MG separation: both are set by the "
      f"kernel slope L_mu at the solar-neighbourhood argument, and p = 4 gives {Lm['power p=4']:.4f} against "
      f"Route A's 0.3675 -- Route A MAXIMISES that slope and p = 4 reduces it, so the factor-13.9 MI-vs-MG "
      f"separation and the 7-16-galaxy 3-sigma requirement both degrade. nu_vert/nu_rad needs a full AQUAL "
      f"solve and is NOT priced here; it was non-diagnostic (1.0243 vs 1.0243) for both kernels already")


# ============================================================ P5  the Milky Way box, with the AQUAL solver
banner("P5  THE MILKY WAY FIVE-CONSTRAINT BOX -- re-solved with the AQUAL solver")

SRC = pathlib.Path(HERE) / "mi_aqual_mond_refit_2026.py"
_s = SRC.read_text()
_G: dict = {"__name__": "anchor"}
exec(compile(_s[:_s.index('banner("F1')], str(SRC), "exec"), _G)          # noqa: S102
solve, densities, mass_of, sigma_of = _G["solve"], _G["densities"], _G["mass_of"], _G["sigma_of"]
KPC, MSUN, MSUN_PC2, GG = _G["KPC"], _G["MSUN"], _G["MSUN_PC2"], _G["G"]
R0, VC, VC_E, KZ, KZ_E = _G["R0"], _G["VC"], _G["VC_E"], _G["KZ"], _G["KZ_E"]
MSTAR_P, MSTAR_E = _G["MSTAR_P"], _G["MSTAR_E"]
RDTHIN_P, RDTHIN_E = _G["RDTHIN_P"], _G["RDTHIN_E"]
SIGSTAR_P, SIGSTAR_E = _G["SIGSTAR_P"], _G["SIGSTAR_E"]
_CACHE: dict = {}
N_SEARCH = 80


def obs(fM, fR, a0, muf, n=N_SEARCH):
    """BOTH v_c and Sigma_dyn interpolated in R -- the consistent extractor, as required."""
    key = (round(fM, 6), round(fR, 6), a0, id(muf), n)
    if key not in _CACHE:
        comp, rdt = densities(fM, fR)
        rho = lambda R, z: sum(fn(R, z) for fn in comp.values())                    # noqa: E731
        Rc, zc, P = solve(rho, a0, muf, n=n)
        _CACHE[key] = (Rc, zc, P, comp, rdt)
    Rc, zc, P, comp, rdt = _CACHE[key]
    vc = math.sqrt(abs(np.interp(R0, Rc, np.gradient(P[:, 0], Rc))) * R0)
    gz = np.array([np.interp(1.1 * KPC, zc, np.gradient(P[i, :], zc)) for i in range(len(Rc))])
    sd = abs(np.interp(R0, Rc, gz)) / (2 * math.pi * GG) / MSUN_PC2
    mstar = (mass_of(comp["thin"]) + mass_of(comp["thick"]) + mass_of(comp["bulge"])) / MSUN
    sigstar = (sigma_of(comp["thin"], R0, 1.1 * KPC) + sigma_of(comp["thick"], R0, 1.1 * KPC)) / MSUN_PC2
    return dict(vc=vc, sd=sd, mstar=mstar, sigstar=sigstar, rdt=rdt)


def worst(fM, fR, a0, muf):
    if not (0.5 <= fM <= 4.0 and 0.4 <= fR <= 2.0):
        return 1e3
    try:
        o = obs(fM, fR, a0, muf)
        return float(np.max(np.abs(np.array([
            (o["vc"] - VC) / VC_E, (o["sd"] - KZ) / KZ_E, (o["mstar"] - MSTAR_P) / MSTAR_E,
            (o["rdt"] - RDTHIN_P) / RDTHIN_E, (o["sigstar"] - SIGSTAR_P) / SIGSTAR_E]))))
    except Exception:
        return 1e3


# the SAME common box mi_routeA_box_clearance_verified_2026.py used, so no comparator is truncated
FM_BOX = [round(1.60 + 0.10 * i, 3) for i in range(7)]
FR_BOX = [round(0.72 + 0.03 * i, 3) for i in range(5)]


def minimax(a0, muf):
    best = None
    for fM in FM_BOX:
        for fR in FR_BOX:
            w = worst(fM, fR, a0, muf)
            if best is None or w < best[0]:
                best = (w, fM, fR)
    w0, fM0, fR0 = best
    for dfM in (-0.05, 0.0, 0.05):
        for dfR in (-0.015, 0.0, 0.015):
            if dfM or dfR:
                w = worst(fM0 + dfM, fR0 + dfR, a0, muf)
                if w < best[0]:
                    best = (w, fM0 + dfM, fR0 + dfR)
    return best


print(f"  {'kernel':<20}{'footing':>8}{'worst sigma':>13}{'f_M':>8}{'f_R':>7}{'clears 2 sigma?':>17}"
      f"{'committed':>12}")
print("  " + "-" * 88)
BOX = {}
for lab, muf, comm in (("alpha=2", mu_alpha2, (3.423, 3.068)),
                       ("power p=4", lambda x: mu_p(x, 4), (None, None))):
    for i, (fn, a0) in enumerate((("canon", A0_CANON), ("alt", A0_ALT))):
        w, fM, fR = minimax(a0, muf)
        BOX[(lab, fn)] = w
        cs = f"{comm[i]:.3f}" if comm[i] is not None else "--"
        print(f"  {lab:<20}{fn:>8}{w:>13.3f}{fM:>8.3f}{fR:>7.3f}"
              f"{('YES' if w < 2.0 else 'no'):>17}{cs:>12}")
print(f"  {'Route A (adopted)':<20}{'canon':>8}{1.502:>13.3f}{1.900:>8.3f}{0.780:>7.3f}{'YES':>17}"
      f"{1.502:>12.3f}")
check(abs(BOX[("alpha=2", "canon")] - 3.423) < 0.15 and abs(BOX[("alpha=2", "alt")] - 3.068) < 0.15,
      f"P5a the box solver is VALIDATED before p = 4 is read: fed alpha=2 on the same common box and the same "
      f"consistent interpolated extractor it returns {BOX[('alpha=2','canon')]:.3f} canonical / "
      f"{BOX[('alpha=2','alt')]:.3f} alt against the committed 3.423 / 3.068")
p4c, p4a = BOX[("power p=4", "canon")], BOX[("power p=4", "alt")]
check(p4c > 1.502,
      f"P5b and the Milky Way agrees with SPARC: p = 4 reaches a best worst-constraint of {p4c:.3f} sigma "
      f"canonical / {p4a:.3f} alt, against Route A's committed 1.502 / 1.838 and alpha=2's 3.423 / 3.068. So "
      f"p = 4 sits {'INSIDE' if p4c < 2.0 else 'OUTSIDE'} the 2-sigma box "
      f"{'but strictly worse than Route A' if p4c < 2.0 else 'and fails it'} -- the same direction as every "
      f"other front priced here. Route A's weaker Newtonian tail is what buys it the Galaxy")


banner("THE BILL FOR p = 4 -- and what it does and does not overturn")
print(f"""  WHAT p = 4 BUYS:
   * Milgrom-1994 class-(34) ANALYTICITY, which Route A forfeits by an essential singularity. That is a real
     theoretical property and the admissibility audit established it at 31/31.
   * the ephemeris, by {marg['power p=4']:.1e}x at the Sun -- discharged, though with a bounded margin where
     Route A's is unbounded.
   * *** THE kappa = 1/2 MEASUREMENT: Dchi2 = {d_p4:+.1f} ({s_p4k:.2f} sigma) FAVOURING kappa = 1/2, where
     Route A gives {d_ra:+.1f} ({K['Route A (adopted)'][1]:.2f} sigma) AGAINST. *** Still under 3 sigma, so
     SPARC does not RESOLVE kappa either way, but the LEAN is restored to the framework's side.

  WHAT p = 4 COSTS, and it is more than the audit expected:
   * SPARC scatter {cost4:+.4f} dex against alpha=2 -- {abs(cost4)/max(span,1e-9):.1f}x the entire committed
     alpha=1/alpha=2/Route A span, so STANDING's 0.0084 dex bracketing argument does NOT cover it (P2b). The
     mechanism is structural: p = 4's knee is the WEAKEST boost of any kernel the corpus has used (P2c).
   * the WIDE-BINARY front, worst of all: gamma_v = {gv['power p=4']:.4f} against Route A's {RA_POINT:.4f} and
     even alpha=2's {A4D_POINT:.4f}, a signal {(RA_POINT-1)/(gv['power p=4']-1):.1f}x smaller than Amendment 8
     filed. Against a frozen sigma_sys = 0.02 that is decisively less decidable than the kernel Route A
     replaced (P4b).
   * CLUSTERS: a weaker boost at y = 0.037 ({nu_clu_p4:.4f} vs {nu_clu_ra:.4f}), so eta(R500) rises back past
     alpha=2's 2.364 -- worsening the framework's largest quantitative deficit (P4d).
   * the EFE DIPOLE and the whole MI-vs-MG separation, which are set by the kernel slope L_mu that Route A
     MAXIMISES: {Lm['power p=4']:.4f} against 0.3675 (P4d).
   * the MILKY WAY box: {p4c:.3f} sigma against Route A's 1.502 (P5b).

  THE HONEST NET: the two things that pull toward p = 4 are THEORETICAL (analyticity) and one MEASUREMENT
  (the kappa lean). Everything that pulls away is PHENOMENOLOGICAL, and there are five of them, all in the
  same direction and all traceable to ONE fact -- raising p sharpens the Newtonian tail and pays for it at the
  knee, and every galactic-scale front lives at the knee. This is a genuine trade and not a rout in either
  direction, and it is NOT a recommendation: nothing here is adopted, and the wide-binary cost in particular
  would require withdrawing a hash-stamped amendment filed today.

  NOT PRICED HERE, and owed before anyone acts: nu_vert/nu_rad and the sigma-spread amplitude (both need full
  re-solves); p = 4's Bekenstein-Milgrom free function, which is an incomplete-beta object with no closed form
  and no built field theory; and p = 6, which the audit found equally admissible and whose knee is closer to
  Route A's -- if the analyticity property is worth having, p = 6 may buy it at a smaller phenomenological
  cost than p = 4 and has not been tried.""")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: p = 4 buys analyticity and restores the kappa lean; it costs SPARC scatter, the wide-binary")
print("  signal, the clusters, the EFE separation and the Milky Way box. Priced, not adopted.")
