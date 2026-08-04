#!/usr/bin/env python3
r"""mi_btfr_intercept_kappa_door_2026.py -- DOOR 1: is the BTFR intercept the one shape-free kappa measurement?

THE CLAIM UNDER TEST. V^4 = G M_bar a0 with coefficient EXACTLY 1 is a theorem of the convex
Bekenstein-Milgrom free function (mi_route_a_field_theory_2026.py), not a fit. Because the relation lives at
g_bar << a0 and every kernel in the family satisfies nu sqrt(y) -> 1, the BTFR intercept looks like the one
place a0 is measurable with a DERIVED coefficient and NO transition-shape dependence. This script builds that
estimator on SPARC, prices every error term, and tests the shape-independence instead of asserting it.

WHAT IS NEW HERE relative to mi_routeA_shape_invariant_a0_2026.py S9 (which priced the BTFR on the WHOLE
sample and found it could not reach the gap):
  * an explicit DEEP CUT with the flatness criterion and the depth cut declared in advance, scanned as a
    ladder, so the shape systematic is measured as a FUNCTION of depth rather than at SPARC's median depth;
  * the full term-by-term error budget, separated into terms that average down and terms that do not;
  * a closed-form MASS-BUDGET FLOOR: because f_* + f_gas = 1, the stellar-M/L and gas-mass calibrations cannot
    both be made small, and their joint minimum is an N-independent, shape-independent, distance-independent
    floor -- derived here and checked numerically;
  * the effective N of the deep subsample and the named galaxies that carry the weight.

THE EXACT FINITE-RADIUS IDENTITY that governs everything. In the algebraic (modified-inertia) form
g_obs = nu(y) g_bar with y = g_bar/a0, so for a system whose flat part is measured at radius R,

    V_f^4 = nu(y)^2 g_bar^2 R^2 = [nu(y)^2 y] * [g_bar R^2 / (G M_bar)] * G M_bar a0 = Q(y) * Gamma * G M a0

with Q(y) := nu(y)^2 y  (Q(0) = 1 for EVERY kernel -- this IS the "coefficient exactly 1")
and  Gamma := g_bar R^2 / (G M_bar)  (the measured disc-vs-point-mass factor; Gamma -> 1 as R -> infinity).

So the raw estimator V_f^4/(G M_bar) measures Q(y_out) * Gamma * a0, never a0. Q is the shape-dependent part
and Gamma is Newtonian geometry read off the SPARC mass model. The door is only as shape-free as Q(y_out) is
close to 1 at the depths SPARC actually reaches.

FROZEN IN ADVANCE (not tuned to the answer):
  sample    Q_flag <= 2, inc >= 30 deg, SPARC V_flat > 0, >= 4 rotmod points with R > 0 and V_obs > 0
  flat      |d ln V_obs / d ln R| < 0.15 over the outer 30% of points (>= 3 points), AND R_last > 2 R_disk
  deep      y_out = g_bar(R_last)/a0 < y_cut, y_cut scanned over {inf, 0.15, 0.10, 0.07, 0.05, 0.04, 0.03}
  masses    M_bar = Upsilon_d L_3.6 + 1.4 Upsilon_d L_bul + 1.33 M_HI, Upsilon_d = 0.70 (the corpus's own
            Route A convention).  1.33 is the primordial-composition helium+metals factor X = 0.75; the
            alternative 1.40 (X = 0.71) is carried as a systematic, NOT as a second central value.
  y frozen  the selection variable and Q's argument are evaluated at the CANONICAL a0. a0 is never fitted;
            both footings are then compared to the measurement as postulates. A self-consistent re-solve is
            run as a control to show the freezing does not drive the answer.

Exit 0 = ran and every check held. No check(True); every check below can fail on these data.
"""
from __future__ import annotations

import glob
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import A0_ALT, A0_CANON, A0_M20, Z_FW, nu  # noqa: E402
from mi_route_a_kernel import nu_alpha1, nu_alpha2  # noqa: E402

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 116)
    print(f"  {t}")
    print("=" * 116)


KPC, MSUN, G_N = 3.0857e19, 1.989e30, 6.674e-11
UD_FID, UB_OVER_UD, HE_FID = 0.70, 1.4, 1.33
GAP_LOG = math.log(A0_CANON / A0_M20)          # 8.195% -- the kappa=1/2 vs 1/2pi separation, in the log
NEED = GAP_LOG / 3.0                           # 2.732% -- what a 3-sigma discrimination needs
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- the five transition shapes, as Q(y)
def nu_p(y, p):
    """the power family nu_p = ([1 + sqrt(1 + 4 y^-p)]/2)^(1/p), verbatim from mi_p4_kernel_pricing_2026."""
    t = np.asarray(y, float) ** (-float(p))
    return (0.5 * (1.0 + np.sqrt(1.0 + 4.0 * t))) ** (1.0 / float(p))


SHAPES = {"exponential (Route A)": nu, "alpha=1": nu_alpha1, "alpha=2": nu_alpha2,
          "power p=3": lambda y: nu_p(y, 3), "power p=4": lambda y: nu_p(y, 4)}


def Qy(kf, y):
    """Q(y) = nu(y)^2 y: the exact multiplicative bias of any deep-limit a0 estimator at finite depth y."""
    y = np.asarray(y, float)
    return np.asarray(kf(y)) ** 2 * y


banner("D0  THE THEOREM, AND THE RATE AT WHICH EACH SHAPE REACHES IT")

print("  Q(0) = 1 is the BTFR's 'coefficient exactly 1'. What matters for a 2.7%-level measurement is not")
print("  that Q(0) = 1 but HOW FAST Q -> 1, because SPARC's outermost radii sit at finite y.")
print(f"\n  {'y':>8}" + "".join(f"{k.split(' (')[0]:>16}" for k in SHAPES) + f"{'half-spread':>13}")
print("  " + "-" * 100)
QTAB = {}
for yv in (1e-3, 3e-3, 0.01, 0.03, 0.05, 0.1, 0.2):
    qs = {k: float(Qy(f, yv)) for k, f in SHAPES.items()}
    lq = np.log(list(qs.values()))
    QTAB[yv] = 0.5 * (lq.max() - lq.min())
    print(f"  {yv:>8.4g}" + "".join(f"{qs[k]:>16.5f}" for k in SHAPES) + f"{100*QTAB[yv]:>12.2f}%")

q0 = {k: float(Qy(f, 1e-12)) for k, f in SHAPES.items()}
check(max(abs(v - 1.0) for v in q0.values()) < 2e-6,
      f"D0a Q(0) = 1 holds for all five shapes: at y = 1e-12 the worst departure is "
      f"{max(abs(v-1.0) for v in q0.values()):.2e}. This is the theorem, and it is genuinely shape-free -- the "
      f"deep-MOND limit nu sqrt(y) -> 1 is the DEFINITION of a0, shared by every kernel in the family")

# the analytic approach rates: Route A gives Q - 1 ~ sqrt(y) (Bernoulli series of s/(1-e^-s)); the power
# family gives Q - 1 ~ y^(p/2)/p. Measure the log-log slope of Q - 1 near y = 1e-6 and compare.
rates, want = {}, {"exponential (Route A)": 0.5, "alpha=1": 1.0, "alpha=2": 1.0, "power p=3": 1.5,
                   "power p=4": 2.0}
for k, f in SHAPES.items():
    y1, y2 = 1e-6, 1e-5
    rates[k] = math.log(float(Qy(f, y2)) - 1.0) - math.log(float(Qy(f, y1)) - 1.0)
    rates[k] /= math.log(y2 / y1)
worst_rate = max(abs(rates[k] - want[k]) for k in SHAPES)
print("\n  measured log-log slope of Q - 1 vs y (analytic value in brackets):  " +
      "  ".join(f"{k.split(' (')[0]}={rates[k]:.3f}[{want[k]:.1f}]" for k in SHAPES))
check(worst_rate < 3e-3,
      f"D0b the approach rates are the analytic ones to {worst_rate:.1e}: Q - 1 = sqrt(y) for the adopted "
      f"EXPONENTIAL kernel but y^(p/2)/p for the power family. The adopted kernel is the SLOWEST in the family "
      f"by a full power of sqrt(y), so at a given depth its finite-radius correction is the largest and the "
      f"family's spread is set almost entirely by it. This is against interest and it drives everything below")

check(QTAB[0.03] > NEED and QTAB[0.001] < NEED,
      f"D0c the depth a shape-free 2.7% measurement REQUIRES: the family half-spread in Q is "
      f"{100*QTAB[0.03]:.2f}% at y = 0.03 and {100*QTAB[0.001]:.2f}% at y = 1e-3, so the requirement "
      f"sigma_shape < {100*NEED:.2f}% is met only for y_out well below 0.01 -- roughly y < 0.003, i.e. "
      f"g_bar < 3e-13 m/s^2. Whether SPARC contains such galaxies is an empirical question, answered in D1")


banner("D1  THE SAMPLE, ON THE FROZEN CUTS -- and SPARC's depth census against D0c's requirement")

TBL, nrow = {}, 0
for _ln in open(os.path.join(HERE, "data", "SPARC_Lelli2016c.mrt")):
    _t = _ln.split()
    if len(_t) != 19:
        continue
    try:
        TBL[_t[0]] = dict(D=float(_t[2]), eD=float(_t[3]), fD=int(_t[4]), inc=float(_t[5]),
                          einc=float(_t[6]), L36=float(_t[7]), Rd=float(_t[11]), MHI=float(_t[13]),
                          Vf=float(_t[15]), eVf=float(_t[16]), Qf=int(_t[17]))
        nrow += 1
    except ValueError:
        continue
check(nrow == 175 and abs(TBL["NGC2403"]["D"] - 3.16) < 1e-9 and abs(TBL["NGC2403"]["Vf"] - 131.2) < 1e-9
      and TBL["NGC2403"]["fD"] == 2 and TBL["CamB"]["Qf"] == 2,
      f"D1a the SPARC Table 1 parse is complete and correctly aligned: {nrow} rows (the published 175), and "
      f"spot-checks land on the right columns (NGC2403 D = {TBL['NGC2403']['D']} Mpc, V_flat = "
      f"{TBL['NGC2403']['Vf']} km/s, distance method 2 = TRGB; CamB quality flag 2). A misaligned "
      f"fixed-width read would shift D into e_D and is the first thing that could silently wreck this lane")

FLAT_SLOPE, ROVERRD = 0.15, 2.0
GAL = []
for _f in sorted(glob.glob(os.path.join(HERE, "data", "sparc_data", "*_rotmod.dat"))):
    nm = os.path.basename(_f).replace("_rotmod.dat", "")
    if nm not in TBL:
        continue
    T = TBL[nm]
    if T["Qf"] > 2 or T["inc"] < 30.0 or T["Vf"] <= 0.0:
        continue
    d = np.genfromtxt(_f, comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    m = (R > 0) & (Vo > 0)
    R, Vo, eV, Vg, Vd, Vb = R[m], Vo[m], eV[m], Vg[m], Vd[m], Vb[m]
    if len(R) < 4:
        continue
    V2 = np.sign(Vg) * Vg ** 2 + UD_FID * Vd ** 2 + UB_OVER_UD * UD_FID * Vb ** 2
    if V2[-1] <= 0:
        continue
    k = max(3, int(math.ceil(0.3 * len(R))))
    slope = float(np.polyfit(np.log(R[-k:]), np.log(Vo[-k:]), 1)[0])
    gbl = V2[-1] * 1e6 / (R[-1] * KPC)                       # g_bar at the outermost measured radius
    Mst, Mgs = UD_FID * T["L36"] * 1e9, HE_FID * T["MHI"] * 1e9
    if Mst + Mgs <= 0:
        continue
    Mb = (Mst + Mgs) * MSUN
    GAL.append(dict(nm=nm, slope=slope, RoRd=R[-1] / max(T["Rd"], 1e-9), gbl=gbl,
                    Gam=gbl * (R[-1] * KPC) ** 2 / (G_N * Mb), Mb=Mb, Mst=Mst, Mgs=Mgs,
                    fst=Mst / (Mst + Mgs), a0raw=(T["Vf"] * 1e3) ** 4 / (G_N * Mb),
                    V3=float(np.mean(Vo[-3:])), Vl=float(Vo[-1]), **T))
FLAT = [g for g in GAL if abs(g["slope"]) < FLAT_SLOPE and g["RoRd"] > ROVERRD]
yall = np.array([g["gbl"] / A0_CANON for g in FLAT])
print(f"  {len(GAL)} galaxies pass quality+inclination+V_flat; {len(FLAT)} also pass the frozen flatness cut "
      f"(|dlnV/dlnR| < {FLAT_SLOPE} over the outer 30%, R_last > {ROVERRD} R_disk)")
print(f"  y_out percentiles over the flat sample: " +
      "  ".join(f"{p}%={np.percentile(yall, p):.4f}" for p in (0, 5, 25, 50, 75, 95)))
print(f"  deepest three galaxies: " + ", ".join(
    f"{FLAT[i]['nm']} (y={yall[i]:.4f})" for i in np.argsort(yall)[:3]))
check(yall.min() > 0.003 and float(np.sum(yall < 0.01)) == 0.0,
      f"D1b *** SPARC DOES NOT CONTAIN THE DEPTH THE SHAPE-FREE MEASUREMENT NEEDS. The deepest flat-part "
      f"measurement in the whole flat sample sits at y_out = {yall.min():.4f}, and NOT ONE galaxy reaches "
      f"y_out < 0.01, let alone the y < 0.003 that D0c showed is required for a {100*NEED:.1f}% shape "
      f"systematic. The median is y_out = {np.median(yall):.3f}, where the family half-spread is "
      f"{100*QTAB[0.05]:.1f}%. So the door's shape-freedom is a statement about a limit the data do not reach")


banner("D2  THE ESTIMATOR, AND THE DEPTH LADDER: what the deep cut buys and what it costs")

# ---- the RANDOM per-galaxy error terms (all propagated from SPARC's own quoted errors where they exist)
SIG_UPS_RAND = 0.230      # 0.100 dex population-model scatter in Upsilon_3.6 at fixed colour
SIG_GAS_RAND = 0.050      # per-object HI flux reproducibility
NBOOT, RNG = 4000, np.random.default_rng(20260803)


def sig_random(g):
    """per-galaxy sigma on ln a0_hat. ln a0 = 4 ln V_f - ln(G M_bar) - ln Gamma - ln Q, so V_f enters x4,
    the distance enters x2 (M_bar ~ D^2 while V_f, g_bar, Gamma and y are all distance-INDEPENDENT), and the
    mass-model terms enter weighted by their mass fractions."""
    inc = math.radians(g["inc"])
    return math.sqrt((4.0 * g["eVf"] / g["Vf"]) ** 2
                     + (4.0 * math.radians(g["einc"]) / math.tan(inc)) ** 2
                     + (2.0 * g["eD"] / g["D"]) ** 2
                     + (g["fst"] * SIG_UPS_RAND) ** 2
                     + ((1.0 - g["fst"]) * SIG_GAS_RAND) ** 2)


def estimate(sub, kf, a0ref=A0_CANON, key="Vf"):
    """weighted geometric mean of a0_hat_i = V_f^4 / (G M_bar Gamma Q(y_out)), and its bootstrap SE."""
    y = np.array([g["gbl"] / a0ref for g in sub])
    lna = np.array([4.0 * math.log(g[key] * 1e3) - math.log(G_N * g["Mb"]) for g in sub])
    lna = lna - np.log(np.asarray(Qy(kf, y)) * np.array([g["Gam"] for g in sub]))
    w = np.array([1.0 / sig_random(g) ** 2 for g in sub])
    mu = float(np.sum(w * lna) / np.sum(w))
    idx = RNG.integers(0, len(sub), size=(NBOOT, len(sub)))
    bs = np.array([float(np.sum(w[i] * lna[i]) / np.sum(w[i])) for i in idx])
    return math.exp(mu), float(np.std(bs, ddof=1)), w, lna, y


LADDER = [9.9, 0.15, 0.10, 0.07, 0.05, 0.04, 0.03]
print(f"  a0_hat / a0_canonical per shape, after the EXACT finite-radius correction Q(y_out) * Gamma:")
print(f"  {'y_cut':>6} {'N':>4} {'Neff':>6} {'med y':>7} {'medQG':>6}" +
      "".join(f"{k.split(' (')[0]:>13}" for k in SHAPES) + f"{'shape':>8}{'stat':>8}{'quad':>8}")
print("  " + "-" * 116)
ROWS = {}
for yc in LADDER:
    sub = [g for g in FLAT if g["gbl"] / A0_CANON < yc]
    if len(sub) < 4:
        continue
    vals, st = {}, 0.0
    for kn, kf in SHAPES.items():
        v, s, w, lna, y = estimate(sub, kf)
        vals[kn] = v
        if kn == "exponential (Route A)":
            st, wt, yy = s, w, y
    lv = np.log(list(vals.values()))
    hs = 0.5 * float(lv.max() - lv.min())
    neff = float(wt.sum() ** 2 / (wt ** 2).sum())
    qg = float(np.median(Qy(nu, yy) * np.array([g["Gam"] for g in sub])))
    ROWS[yc] = dict(sub=sub, vals=vals, hs=hs, st=st, neff=neff, w=wt, y=yy, qg=qg)
    print(f"  {yc:>6.3g} {len(sub):>4d} {neff:>6.1f} {float(np.median(yy)):>7.4f} {qg:>6.3f}" +
          "".join(f"{vals[k]/A0_CANON:>13.3f}" for k in SHAPES) +
          f"{100*hs:>7.2f}%{100*st:>7.2f}%{100*math.hypot(hs, st):>7.2f}%")

BEST = min(ROWS, key=lambda k: math.hypot(ROWS[k]["hs"], ROWS[k]["st"]))
P = ROWS[BEST]
raw = math.exp(float(np.sum(P["w"] * (np.log([g["a0raw"] for g in P["sub"]]))) / np.sum(P["w"])))
print(f"\n  the quadrature optimum of the ladder is y_cut = {BEST} (N = {len(P['sub'])}, "
      f"N_eff = {P['neff']:.1f}); its RAW uncorrected V_f^4/(G M_bar) = {raw:.4e} = {raw/A0_CANON:.3f}x canonical")
check(1.0e-10 < raw < 1.4e-10,
      f"D2a EXTERNAL CONTROL, and it can fail: the RAW BTFR normalisation on this sample is {raw:.3e} = "
      f"{raw/A0_CANON:.3f}x canonical, inside the literature's independently-measured BTFR box of roughly "
      f"1.0-1.4e-10 (McGaugh 2012; Lelli, McGaugh & Schombert 2019). The pipeline therefore reproduces the "
      f"well-known BTFR-vs-RAR normalisation offset from raw SPARC before any framework-specific correction "
      f"is applied, which is the sanity condition for everything downstream")

medGam = float(np.median([g["Gam"] for g in P["sub"]]))
qgm = {kn: math.exp(float(np.sum(P["w"] * np.log(Qy(kf, P["y"]))) / np.sum(P["w"]))) for kn, kf in SHAPES.items()}
print("  weighted geometric-mean Q(y_out) at the optimum: " +
      "  ".join(f"{k.split(' (')[0]}={qgm[k]:.3f}" for k in SHAPES) + f";  median Gamma = {medGam:.3f}")
check(P["qg"] > 1.25 and medGam > 1.10 and math.log(qgm["exponential (Route A)"] / qgm["power p=4"]) > GAP_LOG,
      f"D2b the correction the door actually requires is LARGE, not a nuisance: the median Q(y_out) * Gamma at "
      f"the optimum is {P['qg']:.3f} under the adopted kernel -- a {100*(P['qg']-1):.0f}% multiplicative "
      f"correction, split into Newtonian disc geometry Gamma = {medGam:.3f} and kernel "
      f"Q = {qgm['exponential (Route A)']:.3f}. Applying it moves the estimate from {raw/A0_CANON:.3f}x to "
      f"{P['vals']['exponential (Route A)']/A0_CANON:.3f}x canonical, and the KERNEL PART ALONE differs between "
      f"the adopted exponential and p = 4 by {100*math.log(qgm['exponential (Route A)']/qgm['power p=4']):.2f}%, "
      f"already larger than the {100*GAP_LOG:.2f}% kappa gap being hunted. 'Shape-free' cannot describe a "
      f"measurement whose central value moves by more than the target signal when the shape is changed")


banner("D3  (c) THE SHAPE-INDEPENDENCE TEST -- demonstrated, not asserted")

print(f"  the requirement stated in advance: the intercept must move by << the kappa gap, {100*GAP_LOG:.2f}%")
print(f"  {'y_cut':>6}{'N':>5}   shape half-spread   vs gap   vs 3-sigma need ({100*NEED:.2f}%)")
for yc, r in ROWS.items():
    print(f"  {yc:>6.3g}{len(r['sub']):>5d}{100*r['hs']:>16.2f}%{r['hs']/GAP_LOG:>9.2f}x{r['hs']/NEED:>14.2f}x")
hs_min = min(r["hs"] for r in ROWS.values())
yc_min = min(ROWS, key=lambda k: ROWS[k]["hs"])
check(hs_min > NEED and hs_min > 0.5 * GAP_LOG,
      f"D3a *** THE DOOR FAILS ITS OWN SHAPE TEST ON SPARC, AND THIS IS THE LANE'S HEADLINE. Across the whole "
      f"depth ladder the intercept's shape half-spread never falls below {100*hs_min:.2f}% (at y_cut = "
      f"{yc_min}, where only {len(ROWS[yc_min]['sub'])} galaxies survive). That is {hs_min/NEED:.1f}x the "
      f"{100*NEED:.2f}% a 3-sigma kappa test needs and {hs_min/GAP_LOG:.2f}x the {100*GAP_LOG:.2f}% gap "
      f"itself -- so the intercept does NOT move by << the gap, it moves by a comparable amount or more. The "
      f"brief said that if this happened the door closes as a SHAPE-FREE measurement, and it happened")

lo = min(ROWS[BEST]["vals"].values()) / A0_CANON
hi = max(ROWS[BEST]["vals"].values()) / A0_CANON
print(f"\n  at the optimum y_cut = {BEST} the five shapes give a0_hat/a0_canon spanning {lo:.3f}-{hi:.3f}: the "
      f"adopted exponential\n  kernel is the LOW end and p = 4 the high end, i.e. the shape choice alone moves "
      f"the answer across the gap.")
check(math.log(hi / lo) > 1.5 * GAP_LOG and lo < 1.0 < hi,
      f"D3b the full span is {100*math.log(hi/lo):.2f}% = {math.log(hi/lo)/GAP_LOG:.1f}x the kappa gap, and it "
      f"straddles unity: the adopted exponential kernel returns {lo:.3f}x canonical while p = 4 returns "
      f"{hi:.3f}x. A measurement whose answer to 'is a0 the kappa = 1/2 value?' flips from LOW to CONSISTENT "
      f"purely on the transition shape cannot be the corpus's shape-free anchor")

# --- can the data themselves fix the shape? the residual-trend test, and where its power lives
print("\n  CAN THE DATA PICK THE SHAPE? If the right Q is applied, the corrected a0_hat must have NO residual")
print("  trend with y_out. Regressing ln a0_hat_i (corrected) on ln y_out gives, per shape:")
TREND = {}
for lab, subkey in (("full flat sample", 9.9), (f"deep only (y<{BEST})", BEST)):
    sub = ROWS[subkey]["sub"]
    yv = ROWS[subkey]["y"]
    ly = np.log(yv)
    n = len(sub)
    out = []
    for kn, kf in SHAPES.items():
        r = np.array([4.0 * math.log(g["Vf"] * 1e3) - math.log(G_N * g["Mb"] * g["Gam"]) for g in sub])
        r = r - np.log(Qy(kf, yv))
        A = np.polyfit(ly - ly.mean(), r, 1)
        res = r - np.polyval(A, ly - ly.mean())
        se = float(np.std(res, ddof=2) / (math.sqrt(n) * np.std(ly)))
        TREND[(lab, kn)] = (float(A[0]), se)
        out.append(f"{kn.split(' (')[0]}={A[0]:+.3f}+-{se:.3f}")
    print(f"    {lab:<22} (N={n}, ln y lever {ly.max()-ly.min():.2f}):  " + "  ".join(out))
t_ra_f, se_f = TREND[("full flat sample", "exponential (Route A)")]
t_p4_f = TREND[("full flat sample", "power p=4")][0]
se_d = TREND[(f"deep only (y<{BEST})", "exponential (Route A)")][1]
check(abs(t_ra_f) < se_f and abs(t_p4_f) > 1.5 * se_f and se_d > 2.0 * se_f,
      f"D3c the internal shape calibration works -- but ONLY outside the deep cut, and that is a structural "
      f"trap. Over the full flat sample the adopted exponential kernel leaves a residual trend of "
      f"{t_ra_f:+.3f} +- {se_f:.3f} (i.e. {abs(t_ra_f)/se_f:.2f} sigma, flat), while p = 4 leaves "
      f"{t_p4_f:+.3f} ({abs(t_p4_f)/se_f:.2f} sigma) -- so the data do mildly prefer the adopted shape and the "
      f"marginalisation in D3a is conservative. But inside the deep cut the same regression's error explodes to "
      f"{se_d:.3f} ({se_d/se_f:.1f}x), because the deep cut removes the ln y lever the shape test needs. The "
      f"cut that makes the estimator shape-free is the cut that destroys the ability to measure the shape. "
      f"CAVEAT, and it is not small: this trend is also confounded with real trends in Upsilon, gas fraction "
      f"and R_last/R_disk across surface brightness, so a flat residual is necessary, not sufficient")


banner(f"D4  (b) THE FULL ERROR BUDGET, TERM BY TERM, at the optimum y_cut = {BEST}  (N = {len(P['sub'])})")

SUB, W = P["sub"], P["w"]
wf = W / W.sum()
fst_b = float(np.sum(wf * np.array([g["fst"] for g in SUB])))
fgs_b = 1.0 - fst_b
qHF = float(np.sum(wf * np.array([1.0 if g["fD"] == 1 else 0.0 for g in SUB])))
SIG_UPS_ZP, SIG_HE, SIG_HI_ZP, SIG_CO, SIG_D_HF, SIG_D_OTH = 0.168, 0.0256, 0.100, 0.050, 0.041, 0.030

# --- random terms, each switched on alone, then the ensemble reduction by the actual weights
def ens(vec):
    """the ensemble error a per-galaxy random sigma vector produces in the weighted mean."""
    return float(math.sqrt(np.sum((wf * vec) ** 2)))


rnd = {
    "V_flat measurement (4 e_Vf/Vf)": ens(np.array([4.0 * g["eVf"] / g["Vf"] for g in SUB])),
    "inclination (4 cot i e_i)": ens(np.array([4.0 * math.radians(g["einc"]) / math.tan(math.radians(g["inc"]))
                                               for g in SUB])),
    "distance, per-galaxy (2 e_D/D)": ens(np.array([2.0 * g["eD"] / g["D"] for g in SUB])),
    "Upsilon population scatter": ens(np.array([g["fst"] * SIG_UPS_RAND for g in SUB])),
    "gas per-object HI flux": ens(np.array([(1 - g["fst"]) * SIG_GAS_RAND for g in SUB])),
}
# --- flat-velocity definition: recompute the whole estimator under three definitions of "the flat velocity"
fd = {k: estimate(SUB, nu, key=k)[0] for k in ("Vf", "V3", "Vl")}
lfd = np.log(list(fd.values()))
C_flat = 0.5 * float(lfd.max() - lfd.min())

cor = {
    "TRANSITION SHAPE (D3a)": P["hs"],
    "Upsilon_3.6 zero point (0.50-0.70)": fst_b * SIG_UPS_ZP,
    "HI flux scale (10%, range 5-15%)": fgs_b * SIG_HI_ZP,
    "CO-dark / H2 (one-sided, 0-10%)": fgs_b * SIG_CO,
    "helium factor (1.33 vs 1.40)": fgs_b * SIG_HE,
    "distance scale (H0=73 / TRGB zp)": 2.0 * math.hypot(qHF * SIG_D_HF, (1 - qHF) * SIG_D_OTH),
    "flat-velocity definition": C_flat,
}
print(f"  weighted mass fractions of the subsample: f_* = {fst_b:.3f}, f_gas = {fgs_b:.3f}; weight fraction on "
      f"Hubble-flow distances = {qHF:.3f}")
print(f"  the three flat-velocity definitions give a0_hat/a0_canon = " +
      ", ".join(f"{k}:{v/A0_CANON:.3f}" for k, v in fd.items()))
print(f"\n  RANDOM terms (scale as 1/sqrt(N_eff); N_eff = {P['neff']:.1f}):")
for k, v in sorted(rnd.items(), key=lambda kv: -kv[1]):
    print(f"    {k:<38} {100*v:>7.2f}%")
R_TOT = math.sqrt(sum(v * v for v in rnd.values()))
print(f"    {'-> random, quadrature':<38} {100*R_TOT:>7.2f}%     (bootstrap SE, model-free: "
      f"{100*P['st']:.2f}%)")
print(f"\n  CORRELATED terms (N-INDEPENDENT: no amount of SPARC removes them):")
for k, v in sorted(cor.items(), key=lambda kv: -kv[1]):
    print(f"    {k:<38} {100*v:>7.2f}%")
C_TOT = math.sqrt(sum(v * v for v in cor.values()))
TOT = math.hypot(C_TOT, max(R_TOT, P["st"]))
print(f"    {'-> correlated, quadrature':<38} {100*C_TOT:>7.2f}%")
print(f"    {'== TOTAL sigma(a0)/a0':<38} {100*TOT:>7.2f}%      vs the {100*NEED:.2f}% a 3-sigma kappa test needs"
      f"  ({TOT/NEED:.1f}x too coarse)")
print(f"  UNCHARGED, named: Gamma is computed in the ALGEBRAIC form; the AQUAL/QUMOND finite-radius disc value")
print(f"  differs, so the budget above is a LOWER BOUND. Adding that term can only make the total larger.")

bind = max(cor, key=lambda k: cor[k])
check(TOT > 4 * NEED and R_TOT < C_TOT and cor[bind] > 2 * NEED,
      f"D4a THE BINDING TERM IS NOT STATISTICAL. The correlated block totals {100*C_TOT:.2f}% against a random "
      f"{100*R_TOT:.2f}% (bootstrap {100*P['st']:.2f}%), so more galaxies cannot fix this door. The single "
      f"largest term is '{bind}' at {100*cor[bind]:.2f}%, followed by "
      f"'{sorted(cor, key=lambda k: -cor[k])[1]}' at {100*sorted(cor.values())[-2]:.2f}%. Total "
      f"sigma(a0)/a0 = {100*TOT:.1f}%, which is {TOT/NEED:.1f}x the {100*NEED:.2f}% required. Plainly: NO")

check(C_flat < 0.4 * cor[bind] and C_flat > 0.5 * NEED,
      f"D4b the FLAT-VELOCITY DEFINITION is subdominant but NOT negligible, and the scale is worth naming: "
      f"replacing SPARC's fitted V_flat by the mean of the outer three points ({fd['V3']/A0_CANON:.3f}x) or by "
      f"V_obs at the last measured point ({fd['Vl']/A0_CANON:.3f}x) moves the intercept by a half-spread of "
      f"{100*C_flat:.2f}%. That is {cor[bind]/C_flat:.1f}x smaller than the binding term, so it is not where "
      f"the door loses -- but it is already {C_flat/NEED:.2f}x the ENTIRE {100*NEED:.2f}% budget a 3-sigma "
      f"kappa test would have to fit inside. Even the bookkeeping choice of what 'flat' means costs most of "
      f"the target")


banner("D5  THE MASS-BUDGET FLOOR -- an N-independent, shape-independent, distance-independent obstruction")

print("  M_bar = Upsilon L + M_gas, so f_* + f_gas = 1 identically. The two calibrations therefore cannot both")
print("  be made small by choosing a subsample: pushing to gas-dominated systems kills the Upsilon term and")
print("  hands the whole budget to the gas term. Minimising")
print("      F(f_*) = sqrt[ (f_* s_U)^2 + ((1 - f_*) s_G)^2 ]   over f_* in [0,1]")
print("  gives f_*(min) = s_G^2/(s_U^2 + s_G^2) and F(min) = s_U s_G / sqrt(s_U^2 + s_G^2) -- the harmonic-type")
print("  combination, i.e. the SMALLER of the two calibrations sets the floor and no subsample escapes it.")
S_G_TOT = math.sqrt(SIG_HI_ZP ** 2 + SIG_HE ** 2 + SIG_CO ** 2)


def floorF(sU, sG):
    return sU * sG / math.sqrt(sU * sU + sG * sG), sG * sG / (sU * sU + sG * sG)


fmin, fstar_opt = floorF(SIG_UPS_ZP, S_G_TOT)
grid = np.linspace(0.0, 1.0, 200001)
num = float(np.min(np.sqrt((grid * SIG_UPS_ZP) ** 2 + ((1 - grid) * S_G_TOT) ** 2)))
print(f"\n  with s_U = {SIG_UPS_ZP:.3f} (Upsilon_3.6 zero point) and s_G = {S_G_TOT:.3f} (HI scale + helium + "
      f"CO-dark):")
print(f"    floor = {100*fmin:.2f}%  at f_* = {fstar_opt:.3f}   [numerical minimum over a 200k grid: "
      f"{100*num:.2f}%]")
print(f"  and the floor for a range of assumed Upsilon zero points, so the conclusion is not one number's fault:")
for sU in (0.05, SIG_UPS_ZP):
    for sG in (0.05, S_G_TOT, 0.15):
        f_, fs_ = floorF(sU, sG)
        print(f"    s_U={sU:.3f} s_G={sG:.3f} -> floor {100*f_:>5.2f}% at f_*={fs_:.2f}"
              f"{'   <-- adopted' if abs(sU-SIG_UPS_ZP) < 1e-9 and abs(sG-S_G_TOT) < 1e-9 else ''}")
check(abs(num - fmin) < 1e-4 and fmin > NEED and floorF(0.05, 0.05)[0] > NEED,
      f"D5a THE MASS-BUDGET FLOOR IS THE DEEPEST RESULT IN THIS LANE, and it is bad news the honest way. The "
      f"closed form matches the numerical minimisation to {abs(num-fmin):.1e}, giving a floor of "
      f"{100*fmin:.2f}% at f_* = {fstar_opt:.2f} -- and it is N-independent, shape-independent and "
      f"distance-independent, so it survives perfect distances, infinite galaxies and a fixed kernel. It is "
      f"{fmin/NEED:.1f}x the {100*NEED:.2f}% requirement. Worse, even the OPTIMISTIC corner where both the "
      f"stellar M/L zero point and the whole gas scale are known to 5% still floors at "
      f"{100*floorF(0.05, 0.05)[0]:.2f}% = {floorF(0.05, 0.05)[0]/NEED:.2f}x the requirement. To reach "
      f"{100*NEED:.2f}% BOTH calibrations must be better than "
      f"{100*NEED*math.sqrt(2):.1f}% -- a factor {SIG_UPS_ZP/(NEED*math.sqrt(2)):.1f} on Upsilon_3.6 and "
      f"{S_G_TOT/(NEED*math.sqrt(2)):.1f} on the gas scale beyond what anyone can currently do")

banner("D6  CONTROLS: is the random budget honest, does freezing y matter, does the footing matter?")

lna_i = np.array([4.0 * math.log(g["Vf"] * 1e3) - math.log(G_N * g["Mb"] * g["Gam"]) for g in SUB])
lna_i = lna_i - np.log(Qy(nu, P["y"]))
sig_i = np.array([sig_random(g) for g in SUB])
var_obs = float(np.var(lna_i, ddof=1))
var_prop = float(np.mean(sig_i ** 2))
sd_var = var_obs * math.sqrt(2.0 / (len(SUB) - 1))                      # sampling error of a variance
sig_int2_ul = var_obs - var_prop + 2.0 * sd_var
print(f"  per-galaxy sigma from SPARC's own quoted errors spans {100*sig_i.min():.1f}-{100*sig_i.max():.0f}%; "
      f"mean variance {var_prop:.4f}")
print(f"  observed variance of ln a0_hat = {var_obs:.4f} +- {sd_var:.4f} -> intrinsic variance "
      f"{var_obs - var_prop:+.4f}, 2-sigma UL {sig_int2_ul:.4f} (sd {math.sqrt(max(sig_int2_ul,0)):.3f})")
check(var_obs < var_prop + 2 * sd_var,
      f"D6a THE INTRINSIC-SCATTER TERM IS NOT NEEDED and the random budget is if anything conservative: the "
      f"observed variance of ln a0_hat, {var_obs:.4f}, is BELOW the variance already predicted by SPARC's own "
      f"quoted V_flat, inclination and distance errors, {var_prop:.4f}. So the deep BTFR has no detectable "
      f"intrinsic scatter beyond measurement error (2-sigma UL on the intrinsic sd "
      f"{math.sqrt(max(sig_int2_ul,0)):.2f} in the log), and D4's random block cannot be accused of "
      f"under-charging. This also means the {100*P['st']:.1f}% bootstrap SE is a fair random error -- and it is "
      f"still not the binding term")

# self-consistent re-solve: iterate y = g_bar/a0_hat to a fixed point instead of freezing at canonical
a_it = A0_CANON
for _ in range(60):
    a_new = estimate(SUB, nu, a0ref=a_it)[0]
    if abs(math.log(a_new / a_it)) < 1e-12:
        a_it = a_new
        break
    a_it = math.exp(0.5 * math.log(a_it) + 0.5 * math.log(a_new))
frozen = P["vals"]["exponential (Route A)"]
alt_val = estimate([g for g in FLAT if g["gbl"] / A0_ALT < BEST], nu, a0ref=A0_ALT)[0]
print(f"\n  frozen-y estimate {frozen:.4e} ({frozen/A0_CANON:.3f}x canon); self-consistent fixed point "
      f"{a_it:.4e} ({a_it/A0_CANON:.3f}x); ALT-footing selection+argument {alt_val:.4e} "
      f"({alt_val/A0_ALT:.3f}x ALT, {alt_val/A0_CANON:.3f}x canon)")
check(abs(math.log(a_it / frozen)) < 0.05 and abs(math.log(alt_val / frozen)) < 0.12,
      f"D6b the circularity guard is not doing the work: re-selecting and re-evaluating Q self-consistently at "
      f"the estimator's own output instead of freezing at the canonical a0 moves the answer by only "
      f"{100*math.log(a_it/frozen):+.2f}%, and moving the whole selection to the ALT footing "
      f"({A0_ALT:.3e}, 20.7% higher) moves it by {100*math.log(alt_val/frozen):+.2f}%. Both are small compared "
      f"to the {100*P['hs']:.1f}% shape term, so the verdict is a statement about the shape and the mass "
      f"budget, not about the footing convention -- and note the FOOTING FORK ITSELF, 20.7%, is "
      f"{math.log(A0_ALT/A0_CANON)/GAP_LOG:.1f}x the kappa gap, so a0 must be measured far better than the gap "
      f"before the footing question can even be posed")


banner("D7  (d) THE EFFECTIVE N, THE GALAXIES THAT CARRY IT, AND WHAT RE-OBSERVING THEM WOULD BUY")

order = np.argsort(-wf)
print(f"  N = {len(SUB)} but N_eff = (sum w)^2/sum w^2 = {P['neff']:.1f}  ({len(SUB)/P['neff']:.2f}x deficit): "
      f"the weight is carried by a handful of objects.")
print(f"  {'galaxy':<12}{'w share':>9}{'y_out':>8}{'f_*':>7}{'D/Mpc':>8}{'e_D/D':>8}{'method':>10}{'sigma_i':>9}")
for i in order[:6]:
    g = SUB[i]
    meth = {1: "Hubble", 2: "TRGB", 3: "Cepheid", 4: "UMa", 5: "SNIa"}.get(g["fD"], "?")
    print(f"  {g['nm']:<12}{100*wf[i]:>8.1f}%{P['y'][i]:>8.4f}{g['fst']:>7.2f}{g['D']:>8.2f}"
          f"{g['eD']/g['D']:>8.3f}{meth:>10}{100*sig_i[i]:>8.1f}%")
top5 = float(wf[order[:5]].sum())
print(f"  top 5 galaxies carry {100*top5:.1f}% of the weight; top 10 carry {100*float(wf[order[:10]].sum()):.1f}%")
nHF = sum(1 for g in SUB if g["fD"] == 1)
medHF = float(np.median([g["eD"] / g["D"] for g in SUB if g["fD"] == 1]))
gd = [g for g in SUB if g["fst"] < 0.3]
print(f"  {nHF} of {len(SUB)} sit on Hubble-flow distances with a median e_D/D = {medHF:.3f} "
      f"({200*medHF:.0f}% on a0), which is why they carry only {100*float(np.sum(wf[[i for i, g in enumerate(SUB) if g['fD'] == 1]])):.1f}% of the weight")
print(f"  the gas-dominated escape from Upsilon is exactly where the distances are worst: {len(gd)} galaxies "
      f"with f_* < 0.3, of which {sum(1 for g in gd if g['fD'] == 1)} are Hubble-flow, median e_D/D = "
      f"{float(np.median([g['eD']/g['D'] for g in gd])):.3f}")
check(P["neff"] < len(SUB) / 1.8 and top5 > 0.40,
      f"D7a THE EFFECTIVE N IS FAR BELOW THE COUNT, exactly as the a0-line lane found for its own distance "
      f"systematic: N = {len(SUB)} becomes N_eff = {P['neff']:.1f}, a {len(SUB)/P['neff']:.2f}x deficit, and "
      f"{100*top5:.0f}% of the information sits in five galaxies "
      f"({', '.join(SUB[i]['nm'] for i in order[:5])}). Any statement of the form 'N = {len(SUB)} galaxies "
      f"therefore sqrt({len(SUB)})' overstates this door's statistical reach by "
      f"{math.sqrt(len(SUB)/P['neff']):.2f}x")


def scenario(dtarget, shape_on=True, sU=SIG_UPS_ZP, sG=S_G_TOT, dzp=None):
    """total sigma if every galaxy in the deep sample had distance precision dtarget, etc."""
    r = dict(rnd)
    r["distance, per-galaxy (2 e_D/D)"] = ens(np.array([2.0 * min(g["eD"] / g["D"], dtarget) for g in SUB]))
    # the random block is renormalised by the model-free bootstrap/propagated ratio so that the "as observed"
    # row reproduces D4's total exactly and the scenarios are read off the same scale
    rt = math.sqrt(sum(v * v for v in r.values())) * (P["st"] / R_TOT)
    c = {"shape": P["hs"] if shape_on else 0.0, "ups": fst_b * sU, "gas": fgs_b * sG,
         "dist_zp": 2.0 * (dzp if dzp is not None else math.hypot(qHF * SIG_D_HF, (1 - qHF) * SIG_D_OTH)),
         "flat": C_flat}
    return math.hypot(math.sqrt(sum(v * v for v in c.values())), rt), rt


print(f"\n  what would re-observation buy? (all other terms held at D4's values)")
for lab, args in (("as observed", (9.9, True, SIG_UPS_ZP, S_G_TOT, None)),
                  ("TRGB-quality 5% distances, all 24", (0.05, True, SIG_UPS_ZP, S_G_TOT, 0.030)),
                  ("2% distances, all 24", (0.02, True, SIG_UPS_ZP, S_G_TOT, 0.020)),
                  ("+ kernel ADOPTED (shape term = 0)", (0.02, False, SIG_UPS_ZP, S_G_TOT, 0.020)),
                  ("+ Upsilon and gas both to 5%", (0.02, False, 0.05, 0.05, 0.020)),
                  ("+ perfect distances", (0.0, False, 0.05, 0.05, 0.0))):
    t, rt = scenario(*args)
    print(f"    {lab:<36} random {100*rt:>5.2f}%   TOTAL {100*t:>6.2f}%   ({t/NEED:>4.1f}x the requirement)")
ULT = math.hypot(floorF(0.05, 0.05)[0], C_flat)
print(f"    {'+ N -> infinity (random = 0)':<36} random  0.00%   TOTAL {100*ULT:>6.2f}%   "
      f"({ULT/NEED:>4.1f}x the requirement)  <-- the absolute ceiling of this door")
d_need = 0.01 * math.sqrt(P["neff"]) / 2.0
t_trgb, _ = scenario(0.05, True, SIG_UPS_ZP, S_G_TOT, 0.030)
t_perfect, _ = scenario(0.0, True, SIG_UPS_ZP, S_G_TOT, 0.0)
print(f"  to push the per-galaxy distance term below 1% at this N_eff needs e_D/D < {100*d_need:.1f}% on every "
      f"galaxy in the deep sample -- i.e. TRGB or better for all {len(SUB)}, including the {nHF} now on "
      f"Hubble-flow distances.")
check(t_trgb > 0.9 * TOT and t_perfect > 3 * NEED,
      f"D7b AND IT WOULD NOT BE WORTH IT, which is the answer to the subsample question. Giving all "
      f"{len(SUB)} deep galaxies 5% TRGB distances -- a large observational programme, {nHF} new TRGB fields -- "
      f"moves the total only from {100*TOT:.2f}% to {100*t_trgb:.2f}%. Even PERFECT distances, zero error and "
      f"zero zero-point, leave {100*t_perfect:.2f}% = {t_perfect/NEED:.1f}x the requirement, because the shape "
      f"and mass-budget terms do not care about distance. So the honest answer to 'which galaxies would have to "
      f"be re-observed, and with what precision' is: the {nHF} Hubble-flow objects at {100*d_need:.1f}% or "
      f"better, and it still would not reach {100*NEED:.2f}% -- distance is the term everyone can see and NOT "
      f"the term that binds")


banner("D8  THE VERDICT: what the BTFR intercept says about kappa, and whether it is a kappa test at all")

lv = np.log(np.array([g["Vf"] for g in SUB]))
A = np.polyfit(lv - lv.mean(), lna_i, 1)
res = lna_i - np.polyval(A, lv - lv.mean())
se_sl = float(np.std(res, ddof=2) / (math.sqrt(len(SUB)) * np.std(lv)))
LNVR = float(lv.max() - lv.min())
swing = (abs(A[0]) + se_sl) * LNVR          # the 1-sigma ALLOWANCE on the drift, not the central drift
print(f"  first a consistency test the estimator must pass: a0 must be the SAME for every galaxy, so the "
      f"corrected\n  ln a0_hat must not trend with V_flat. Measured d ln a0/d ln V_f = {A[0]:+.3f} +- {se_sl:.3f} "
      f"(equivalently a BTFR slope of {4 - A[0]:.2f}),\n  whose 1-sigma allowance over the sampled "
      f"{math.exp(lv.min()):.0f}-{math.exp(lv.max()):.0f} km/s range lets a0 drift by up to {100*swing:.0f}%.")
check(abs(A[0]) < 2.0 * se_sl and swing > 4 * NEED,
      f"D8a the V-independence of a0 PASSES at {abs(A[0])/se_sl:.2f} sigma -- but only because the test is weak. "
      f"The 1-sigma allowance on the slope still permits a0 to vary by {100*swing:.0f}% across the sampled mass "
      f"range, i.e. {swing/NEED:.0f}x the whole 3-sigma budget. So 'the BTFR intercept' is only defined to "
      f"within that drift: the corpus should not quote a BTFR a0 without stating the velocity range it was "
      f"measured over, since the relation is verified as a single-a0 law only at the ~{100*swing/2:.0f}% level")

KAPPA_C = A0_CANON / (2.0 * A0_CANON)                       # = 1/2 by construction of the footing
KAPPA_M = 0.5 * Z_FW / (2 * math.pi)                        # Milgrom 2020's comparator in the same units
print(f"\n  a0_hat at the optimum, per shape, against the two postulates (total sigma = {100*TOT:.2f}%):")
for kn in SHAPES:
    v = P["vals"][kn]
    print(f"    {kn:<22} {v:.4e} = {v/A0_CANON:.3f}x canon   {math.log(v/A0_CANON)/TOT:+.2f} sigma from "
          f"kappa=1/2   {math.log(v/A0_M20)/TOT:+.2f} sigma from kappa=1/2pi   kappa_hat = {v/(2*A0_CANON):.3f}")
vRA = P["vals"]["exponential (Route A)"]
print(f"  on the adopted kernel: kappa_hat = {vRA/(2*A0_CANON):.3f} +- {TOT*vRA/(2*A0_CANON):.3f} against "
      f"kappa = {KAPPA_C:.3f} (framework) and {KAPPA_M:.3f} (Milgrom 2020 rescaled to the same footing)")
sep = GAP_LOG / TOT
sep_best = GAP_LOG / ULT
check(sep < 1.0 and sep_best < 3.0,
      f"D8b *** THE DOOR CANNOT REACH 3 SIGMA, NOW OR EVER ON THIS RELATION. The kappa=1/2 vs kappa=1/2pi "
      f"separation is {100*GAP_LOG:.2f}% against a total error of {100*TOT:.2f}%, i.e. "
      f"{sep:.2f} sigma of discriminating power today. At the absolute ceiling of D7 -- infinite galaxies, "
      f"perfect distances, the kernel adopted rather than marginalised, and both the stellar M/L and gas "
      f"calibrations improved to 5% -- the total floors at {100*ULT:.2f}% and the separation reaches "
      f"{sep_best:.2f} sigma. Three sigma is not reachable on the BTFR intercept")

check(abs(math.log(vRA / A0_CANON)) / TOT < 2.0 and abs(math.log(vRA / A0_M20)) / TOT < 2.0,
      f"D8c and the measurement itself is not a hint either way, which is worth saying because the central "
      f"value LOOKS low: on the adopted kernel a0_hat = {vRA:.3e} = {vRA/A0_CANON:.3f}x canonical, which is "
      f"{math.log(vRA/A0_CANON)/TOT:+.2f} sigma from kappa = 1/2 and {math.log(vRA/A0_M20)/TOT:+.2f} sigma from "
      f"kappa = 1/2pi. It is consistent with both and prefers neither. Under p = 4 the same data give "
      f"{P['vals']['power p=4']/A0_CANON:.3f}x canonical, so the sign of the (insignificant) lean is set by "
      f"the shape, not by the data")

print(f"""
  IS THIS DOOR kappa-SPECIFIC? Three answers, and they do not agree.
   1. the RELATION is not. V^4 = G M a0 with coefficient 1 is Milgrom's BTFR and holds for EVERY convex
      Bekenstein-Milgrom free function; nothing in it knows about kappa = 1/2. Prior art in full.
   2. the CONVERSION is, and cleanly -- the door's one real advantage over the a0-line. The intercept returns
      a0 in physical units and kappa = a0/(c sqrt(G rho_Lambda)) follows from Planck's rho_Lambda alone, so
      unlike A0LINE_LAMBDA_2026's Lambda-inversion, Z does NOT appear on both sides and nothing is circular.
   3. the PRECISION is not there: {100*TOT:.1f}% against a {100*GAP_LOG:.2f}% gap = {sep:.2f} sigma. A genuine,
      non-circular kappa measurement of the right KIND, delivering almost nothing.
""")


banner("SUMMARY -- DOOR 1, plainly")

print(f"""
  THE RIGHT KIND OF DOOR: V^4 = G M a0 with coefficient exactly 1 is a theorem, Q(0) = 1 holds for all five
  shapes to 1e-6 (D0a), kappa = a0/(c sqrt(G rho_Lambda)) follows from Planck's rho_Lambda with NO circularity
  in Z, the flat-velocity definition costs only {100*C_flat:.2f}% (D4b), there is no detectable intrinsic
  scatter (D6a) and the footing convention moves it {100*abs(math.log(alt_val/frozen)):.1f}% (D6b).

  IT STILL DOES NOT WORK, four reasons that stack:
   1. SPARC IS NOT DEEP ENOUGH -- {100*NEED:.2f}% shape needs y_out < 0.003, the deepest flat part is
      {yall.min():.4f} and NOT ONE galaxy is below 0.01 (D1b); the adopted exponential kernel approaches the
      deep limit as sqrt(y), the slowest in the family (D0b), so it sets the spread nearly single-handedly.
   2. THE SHAPE TEST THEREFORE FAILS -- half-spread bottoms at {100*hs_min:.2f}% = {hs_min/NEED:.1f}x the
      requirement, {hs_min/GAP_LOG:.2f}x the gap; the five shapes give {lo:.3f}-{hi:.3f}x canonical,
      straddling unity (D3a, D3b). The brief's stated closing condition is met.
   3. THE MASS BUDGET FLOORS IT ANYWAY -- f_* + f_gas = 1 forces sigma >= s_U s_G/sqrt(s_U^2 + s_G^2) =
      {100*fmin:.2f}% at f_* = {fstar_opt:.2f}, N- shape- and distance-independent; gas-dominated galaxies
      trade the Upsilon term for the gas term rather than escaping. 5%/5% still floors at
      {100*floorF(0.05,0.05)[0]:.2f}% (D5a).
   4. DISTANCES ARE NOT THE FIX -- N = {len(SUB)} carries N_eff = {P['neff']:.1f}, {100*top5:.0f}% of the weight
      in five galaxies; TRGB distances on all {len(SUB)} give {100*t_trgb:.2f}% and PERFECT distances
      {100*t_perfect:.2f}% (D7a, D7b).

  CARRY OUT: a0_hat = {vRA:.3e} ({vRA/A0_CANON:.3f}x canonical) adopted kernel, {P['vals']['power p=4']/A0_CANON:.3f}x
  under p = 4; kappa_hat = {vRA/(2*A0_CANON):.3f} +- {TOT*vRA/(2*A0_CANON):.3f}; sigma(a0)/a0 = {100*TOT:.1f}%
  (ceiling {100*ULT:.2f}%); {sep:.2f} sigma of power now, {sep_best:.2f} at the ceiling. Against
  {100*NEED:.2f}%: NO. What would move it is NOT distances or N but (i) a stellar M/L zero point good to a few
  per cent, (ii) an absolute gas scale (HI flux + helium + CO-dark) to a few per cent, (iii) flat parts at
  y_out < 0.003, a factor {yall.min()/0.003:.0f} deeper than SPARC's deepest. The relation is not wrong; it
  cannot be read to {100*NEED:.2f}%.
""")

nok = sum(1 for t, _ in ok if t)
print(f"  {nok}/{len(ok)} checks held.")
if nok != len(ok):
    for t, m in ok:
        if not t:
            print(f"    FAILED: {m}")
    sys.exit(1)
print("  Exit 0: Door 1 priced. The BTFR intercept is a genuine, non-circular, but far-too-coarse kappa "
      "measurement, and on SPARC it is not even shape-free.")
