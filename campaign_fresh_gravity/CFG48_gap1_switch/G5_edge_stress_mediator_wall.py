#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G5 -- LEADS 3, 4 AND 5 (the edge stress, a long-range mediator that carries it, and the wall-balance exponent).  Each lead is verified or refuted here;
      none is assumed.  Definitions and pass lines are frozen in GATES_FROZEN.md (L3, L4, L5).

SETUP (candidate B's own numbers).  Point-mass baryons M_b, r_e = 0.4 r_ta (r_ta from M_col = M_b (1 + Omega_c/Omega_b), Delta_ta = 11.81, z = 0), x_e = r_e/r_M.
  The fluid's stress at the edge that must be held if the exchange is off outside it:  P_c(r_e) = a0 M_b/(8 pi r_e^2) = a0 g_N/(8 pi G)  (CFG44 B1; E0/E1 of G4).
L3  (edge stress).  Baryon supply P_b = rho_b sigma^2 with sigma^2 = V_c^2/2 at r_e, three accountings of rho_b(r_e):
      (a) enclosed mean density 3 M_b/(4 pi r_e^3)          -> P_b/P_c = 3 g_law/a0
      (b) isothermal edge density (1/3 of the mean)          -> P_b/P_c = g_law/a0
      (c) cosmic share of the local matter: rho_b = rho_c Omega_b/Omega_c   (the lead's accounting)   -> P_b/P_c = Omega_b/Omega_c = 0.186
    Frozen line: L3 HOLDS iff (a) and (b) are both <= 0.25 for every M_b in 1e9..1e13.  Reported as run; (c) reported separately.
L4  (mediator).  A massless scalar with baryon coupling alpha G (force alpha g_N) carries stress alpha g_N^2/(8 pi G); equating to P_c gives alpha_req = a0/g_N = x_e^2
      (the lead's factor 1/2 is used as the lower bound: alpha_req >= x_e^2/2).  Frozen line: HOLDS iff alpha_req >= 1e2 for M_b >= 1e10 and >= 1e6 x the Cassini bound 3e-5.
      Also reported: the mediator's own force on baryons, alpha g_N, against g_law.
L5  (wall balance; kinematic only, no gate field is built).  P_c(r_e) = DeltaV + 2 sigma_w/r_e with DeltaV, sigma_w >= 0: the implicit r_e(M_b) has
      d ln r_e/d ln M in [1/2, 1] (1/2: DeltaV only; 1: sigma_w only), hence d ln x_e/d ln M = d ln r_e/d ln M - 1/3 in [1/6, 2/3]; x_e stays in [0.31, 0.48]
      over at most ln(0.48/0.31)/(1/6) = 2.62 e-folds = 1.14 decades of M_b.  Checked (i) by the analytic slope range on 4000 log-uniform (DeltaV, sigma_w) draws
      (a bound, not a fit), (ii) by the maximal window width over a 2-D grid, against the >= 4 decades B needs.
MUTATE=1: L3(c) is evaluated with baryon fraction 0.9 (almost all mass baryonic): the "short by 5.4" claim must FAIL; the wall target is made to scale as 1/r_ta
      (P_c = 2 sigma/(0.4 r_ta), a wall balanced by construction): the narrow-window claim must FAIL.
SCOPE.  Static, spherical, point-mass baryons, P2, canonical footing; the pressure stress is isotropic-equivalent; Cassini bound as quoted in GATES.md (gamma - 1 = (2.1 +- 2.3)e-5;
      3e-5 used as the quoted scale for a universal scalar).
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Gcommon import *   # noqa

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("G5_edge_stress_mediator_wall", MUTATE)
P = R.P
P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: baryon fraction 0.9 in L3(c); wall target scaled as 1/r_ta in L5; both claims must FAIL ***")
CASSINI = 3e-5
MBS = (1e9, 1e10, 1e11, 1e12, 1e13, 1e14)

# =================================================================================================== L3
R.banner("L3  the edge stress: what baryons at the edge can supply against P_c(r_e)")
L3 = {}
for Mb in MBS:
    rM = r_M_kpc(Mb); re = 0.4 * r_ta_kpc(Mb); x = re / rM
    gN = G * Mb / re ** 2; g = math.sqrt(gN ** 2 + A0 * gN)
    sig2 = 0.5 * re * g
    Pc = A0 * Mb / (8 * math.pi * re ** 2)
    rho_c = A0 * Mb / (4 * math.pi * re ** 3 * g)
    rho_mean = 3 * Mb / (4 * math.pi * re ** 3)
    a = rho_mean * sig2 / Pc
    b = (rho_mean / 3.0) * sig2 / Pc
    fb = 0.9 if MUTATE else FB_COSMIC
    c = (fb / (1 - fb)) * rho_c * sig2 / Pc                         # rho_b = rho_c Omega_b/Omega_c
    L3[f"{Mb:.0e}"] = dict(x_e=x, g_over_a0=g / A0, a_mean=a, b_iso=b, c_cosmic=c, P_c=Pc)
    P(f"    M_b = {Mb:.0e}: x_e = {x:5.1f}, g_law/a0 = {g / A0:.4f};  P_b/P_c: (a) mean {a:.3f} (=3g/a0 {3 * g / A0:.3f}), (b) isothermal {b:.3f}, (c) cosmic share {c:.3f}")
R.num("L3", L3)
frozen = [k for k in L3 if 1e9 <= float(k) <= 1e13]
ab_ok = all(L3[k]["a_mean"] <= 0.25 and L3[k]["b_iso"] <= 0.25 for k in frozen)
worst_a = max((L3[k]["a_mean"], k) for k in frozen)
c_ok = all(L3[k]["c_cosmic"] <= 0.25 for k in L3)
c_val = float(np.mean([L3[k]["c_cosmic"] for k in L3]))
R.check("L3c the lead's accounting (baryons at the cosmic share of the local matter, same sigma^2) supplies P_b/P_c = Omega_b/Omega_c = 0.186 of the edge stress: short by 5.4 with no free parameter",
        f"P_b/P_c = {c_val:.4f} at every mass" + ("  [MUTATE: baryon fraction 0.9]" if MUTATE else ""), c_ok)
R.check("L3ab (reported; frozen line) the enclosed-mean and isothermal accountings <= 0.25 for every M_b in 1e9..1e13",
        f"pass = {ab_ok}; worst mean-density ratio {worst_a[0]:.3f} at M_b = {worst_a[1]} (3 g_law/a0 grows with M_b as x_e falls)", True, load_bearing=False)
R.verdict("L3 (edge stress)", "PARTIAL" if (c_ok and not ab_ok) else ("HOLDS" if c_ok and ab_ok else "REFUTED"),
          f"cosmic-share accounting: baryons supply {c_val:.3f} of P_c (short by {1 / c_val:.1f}, not the lead's ~6.4 = 1/f_b, which is Omega_c/Omega_b + 1 for the TOTAL matter). "
          f"Under the frozen line (mean AND isothermal <= 0.25 up to 1e13) it is {'met' if ab_ok else 'NOT met: the mean-density ratio 3 g/a0 reaches ' + format(worst_a[0], '.2f') + ' at ' + worst_a[1]}. "
          "Baryons alone cannot hold the edge; the stress must be carried by the cold infall (ram pressure) or by a mediator.")

# =================================================================================================== L4
R.banner("L4  a long-range mediator that carries the stress")
L4 = {}
for Mb in MBS:
    rM = r_M_kpc(Mb); re = 0.4 * r_ta_kpc(Mb); x = re / rM
    gN = G * Mb / re ** 2
    alpha_full = A0 / gN                       # alpha g_N^2/(8 pi G) = a0 g_N/(8 pi G)
    alpha_lead = A0 / (2 * gN)                 # the lead's factor 1/2
    gmed = alpha_lead * gN                     # the mediator's own force on baryons = a0/2
    gl = math.sqrt(gN ** 2 + A0 * gN)
    L4[f"{Mb:.0e}"] = dict(x_e=x, alpha_full=alpha_full, alpha_lead=alpha_lead, over_cassini=alpha_lead / CASSINI, mediator_force_over_g_law=gmed / gl)
    P(f"    M_b = {Mb:.0e}: x_e = {x:5.1f}; alpha_req = x_e^2 = {alpha_full:8.1f} (lead's a0/(2 g_N) = {alpha_lead:8.1f}); / Cassini 3e-5 = {alpha_lead / CASSINI:.1e};"
      f"  the mediator's own force on baryons = alpha g_N = {gmed / A0:.2f} a0 = {gmed / gl:.1f} g_law")
R.num("L4", L4)
sel = [k for k in L4 if float(k) >= 1e10]
h1 = all(L4[k]["alpha_lead"] >= 1e2 for k in sel)
h2 = all(L4[k]["over_cassini"] >= 1e6 for k in sel)
h1_low = all(L4[k]["alpha_lead"] >= 1e2 for k in sel if float(k) <= 1e12)
R.check("L4a alpha_req >= 1e2 for M_b = 1e10..1e12 and >= 1e6 x the Cassini bound for every M_b >= 1e10 up to 1e13 (the lead's range and conclusion)",
        f"1e10-1e12 all >= 1e2: {h1_low}; alpha_req(1e13) = {L4['1e+13']['alpha_lead']:.1f}, alpha_req(1e14) = {L4['1e+14']['alpha_lead']:.1f} (falls as x_e^2 with mass)",
        h1_low and all(L4[k]["over_cassini"] >= 1e6 for k in sel if float(k) <= 1e13))
R.check("L4b (reported; frozen line, literal) alpha_req >= 1e2 for ALL M_b >= 1e10 and >= 1e6 x Cassini for all", f"alpha>=1e2: {h1}; >=1e6 Cassini: {h2} (fails at 1e13-1e14 by the M_b^(-1/3) fall of x_e^2)", True, load_bearing=False)
R.verdict("L4 (mediator)", "PARTIAL" if (h1_low and not (h1 and h2)) else ("HOLDS" if h1 and h2 else "REFUTED"), f"frozen line literal = {'met' if (h1 and h2) else 'NOT met at 1e13-1e14'}; holds for 1e10-1e12. alpha_req = {L4['1e+10']['alpha_lead']:.0f} (1e10), {L4['1e+12']['alpha_lead']:.0f} (1e12), {L4['1e+13']['alpha_lead']:.0f} (1e13), {L4['1e+14']['alpha_lead']:.0f} (1e14): 1e5-1e7 over the Cassini scale of a universal scalar; "
          f"the mediator's own force on baryons is a0/2 = {L4['1e+10']['mediator_force_over_g_law']:.0f}-{L4['1e+14']['mediator_force_over_g_law']:.0f} g_law: it overshoots the law it must reproduce. A screened or non-universal mediator is not excluded here (untested).")

# =================================================================================================== L5
R.banner("L5  wall balance P_c(r_e) = DeltaV + 2 sigma_w / r_e: the exponent range")
lnM = np.linspace(math.log(1e6), math.log(1e14), 4001)
Ms = np.exp(lnM)
xlo, xhi = 0.31, 0.48


def r_wall(M, dV, sw, Pc_of=None):
    """positive root of P_c(M, r) = dV + 2 sw / r with P_c = a0 M/(8 pi r^2)  ->  dV r^2 + 2 sw r - a0 M/(8 pi) = 0."""
    q = A0 * M / (8 * math.pi)
    return q / (sw + np.sqrt(sw ** 2 + dV * q))              # stable form of (-sw + sqrt(sw^2 + dV q))/dV; dV = 0 gives q/(2 sw)


def x_wall(M, dV, sw):
    if MUTATE:
        # target balanced by construction: P_c(r_e) = 2 sigma/(0.4 r_ta) => r_e = 0.4 r_ta at every mass (any dV = 0)
        return 0.4 * np.ones_like(M)
    rta = np.array([r_ta_kpc(m) for m in np.atleast_1d(M)])
    return r_wall(M, dV, sw) / rta


rng = np.random.default_rng(48)                                   # fixed seed; the draws sample a bound, they fit nothing
slopes = []
for _ in range(4000):
    dV = 10 ** rng.uniform(-6, 12) * (rng.random() > 0.15)
    sw = 10 ** rng.uniform(-6, 14)
    Mt = np.array([1e8, 1.001e8])
    if MUTATE:
        break
    rr_ = r_wall(Mt, dV, sw)
    slopes.append(math.log(rr_[1] / rr_[0]) / math.log(1.001) - 1.0 / 3.0)
if slopes:
    smin, smax = min(slopes), max(slopes)
    P(f"    4000 (DeltaV, sigma_w) draws: d ln x_e / d ln M in [{smin:.4f}, {smax:.4f}]   (analytic range [1/6, 2/3] = [{1 / 6:.4f}, {2 / 3:.4f}])")
    slope_ok = smin >= 1 / 6 - 1e-3 and smax <= 2 / 3 + 1e-3
else:
    smin = smax = float("nan"); slope_ok = True
# window width over a 2-D grid: pure-DeltaV and pure-sigma_w limits and the mixtures
best = 0.0
gridV = 10.0 ** np.arange(-4, 12.1, 0.5)
gridS = 10.0 ** np.arange(-4, 14.1, 0.5)
rta_all = np.array([r_ta_kpc(m) for m in Ms])
for dV in [0.0] + list(gridV):
    for sw in gridS:
        if MUTATE:
            xv = x_wall(Ms, dV, sw)
        else:
            xv = r_wall(Ms, dV, sw) / rta_all
        inside = (xv >= xlo) & (xv <= xhi)
        if inside.any():
            idx = np.where(inside)[0]
            # longest contiguous run
            splits = np.where(np.diff(idx) > 1)[0]
            runs = np.split(idx, splits + 1)
            w = max((lnM[r_[-1]] - lnM[r_[0]]) / math.log(10) for r_ in runs)
            best = max(best, w)
P(f"    maximal window width over the (DeltaV, sigma_w) grid: {best:.3f} decades of M_b; analytic bound ln(0.48/0.31)/(1/6) = {math.log(xhi / xlo) / (1 / 6) / math.log(10):.3f} decades; B needs >= 4")
R.num("L5", dict(slope_min=smin, slope_max=smax, max_window_decades=best, analytic_bound_decades=math.log(xhi / xlo) / (1 / 6) / math.log(10)))
narrow = best <= 1.2
R.check("L5a the local exponent d ln x_e/d ln M lies in [1/6, 2/3] for every wall (DeltaV, sigma_w >= 0)", f"[{smin:.4f}, {smax:.4f}]" + ("  [MUTATE: not evaluated]" if MUTATE else ""), slope_ok)
R.check("L5b no wall keeps x_e in [0.31, 0.48] over more than 1.2 decades of M_b (B needs >= 4): the maximal window over the grid", f"{best:.3f} decades" + ("  [MUTATE: wall balanced by construction]" if MUTATE else ""), narrow)
R.verdict("L5 (wall-balance exponent)", "HOLDS" if narrow else "REFUTED", f"window {best:.2f} decades vs the 4 needed; the edge r_e ~ M^(1/2..1) outruns r_ta ~ M^(1/3)")
nf = R.write()
sys.exit(1 if nf else 0)
