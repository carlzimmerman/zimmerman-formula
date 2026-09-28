#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG30 -- BINARY GALAXIES UNDER CANDIDATE B, REFEREED ADVERSARIALLY: do isolated galaxy pairs move faster than B's law
allows, or was the September result an artefact of assuming circular orbits?

WHY.  FAILURES_EXECUTIVE_SUMMARY_2026-09-28 lists binary galaxies as the largest unscored risk (B1): isolated 2MRS major
pairs move 1.8-1.9x faster than Milgrom's isolated deep-MOND two-body law predicts at d3 > 5 r_p
(hunt_2026/h48_h69b_relative_isolation.py; 19 sigma statistically), while LambdaCDM's abundance-matched halos land on
their own prediction.  Candidate B drops the external field for top-level systems (FG001's ownership), so B's prediction
for an isolated pair IS that two-body law.  The estimator, though, assumed every pair is on a circular orbit.  Two things
make that the assumption to referee:
  * a scratch look at the committed sample, made before this script was written, found the fitted dispersion FALLING with
    separation (238 -> 196 -> 170 km/s across the separation tertiles at d3 > 5 r_p), faster than the circular prediction
    of EITHER law allows;
  * in B's logarithmic two-body potential an L* pair at 100-500 kpc has a circular period of ~3-18 Gyr.  Unless something
    removes orbital energy (dynamical friction), such pairs are not virialised: they are still on the orbit the timing
    argument describes (Kahn & Woltjer 1959) -- separating with the Hubble flow, turning around, falling back.  In a log
    potential that infall is fast: v = v_c sqrt(2 ln(R/r)), and the timing fixes R ~ v_c t0 / 2.5 ~ 1 Mpc, so v ~ 2 v_c at
    140 kpc (a hand estimate, made before this script's first run).
The same timing argument in the same law is already on record for the one pair whose full velocity is measured: FP11 T4
found the plain MOND law's first approach TOO FAST for the Milky Way and M31 (-142 to -203 km/s against -109.3 +- 4.4).
This lane computes the timing prediction for the 2MRS pairs, pre-declared, with h48b's sample, estimator and projection
prior, and referees the baryons as well.

THE MODELS (one machinery for both laws; between the two orbit models only the pair's speed changes)
  circular  h48b's prediction, unchanged: the circular two-body speed (B: Milgrom's deep-MOND law; LambdaCDM: Moster+13
            halos as NFW), <dv_los^2> = <v^2>/3 over h48b's projection prior (3-D separation log-uniform in [r_p, 20 r_p]
            with the random-orientation kernel -- a companion density n(r) ~ r^-2).
  timing    the radial timing orbit from the Big Bang in the law's own two-body force plus Lambda (B: r'' = -v_c^2/r +
            Omega_L H0^2 r, v_c the deep-MOND two-body circular speed; LambdaCDM: the halos as point masses M_h1 + M_h2 +
            Lambda, the classic Kahn-Woltjer form), on the first approach; the speed at each 3-D separation follows from
            r(t0) = r; the same prior, truncated at the separation turning around today (farther configurations are not
            bound and belong to the interloper term); <dv_los^2> = <v^2>/3.
  Estimator and sample: h48b's own (Gaussian pairs + a uniform interloper term; 2MRS major pairs, d3 > 5 r_p), exec'd
  read-only.  Both a0 footings.  Cosmology: CFG7's Planck 2018 (t0 = 13.80 Gyr, Omega_L = 0.685).

PRE-DECLARED (written before this script's first run; H2 was SEEN in the scratch look and is confirmed here, not predicted)
  C1  CONTROL  h48b's committed d3 > 5 r_p amplitudes reproduced (deep-MOND 1.89 / 1.80, LambdaCDM 0.95).
  C2  CONTROL  the timing solver: (a) the Lambda = 0 analytic limits (log potential: t = sqrt(pi/2) (R/v_c) [1 + erf sqrt(ln
      R/r)]; Kepler: the radial half-period) to 1e-6; (b) a direct integration of the ODE lands on the tabulated (r, v) to
      1e-4, and the ODE shooter (used for the growing-mass variant) reproduces the quadrature table to 2e-3 at constant mass;
      (c) the general-potential solver (used for the NFW variant) reproduces the Kepler table within 0.5% on a point mass;
      (d) the Local Group: B's first approach at 0.78 Mpc reproduces FP11's committed full two-body integration of the plain
      P2 law (T4: -142 / -175 / -203 km/s at M_b = 1.145 / 1.75 / 2.4e11 canonical, and the alt values) within 10%.
  C3  CONTROL  the estimator on the timing model's own non-Gaussian velocities: mock pairs drawn from B's timing prediction
      (A = 1, 17% interlopers) come back at A = 1 within 0.05 (mean of 5 mocks).
  H1  THE BARYONS CANNOT CLOSE THE CIRCULAR GAP: with the most favourable baryons -- Upsilon_K = 1.0, +0.3 mag of total K
      light, xGASS cold gas with the non-detections at their upper limits, doubled for molecular and ionised gas; generous
      ceilings, not measurements -- the circular amplitude stays > 1.3 and > 5 sigma above 1, both footings.
  H2  THE CIRCULAR MODEL FAILS THE DATA'S OWN PROFILE for BOTH laws: the circular amplitude falls from the inner to the outer
      separation tertile by > 3 sigma (B canonical, and LambdaCDM).  [seen in the scratch look]
  H3  [HEADLINE; MUTATE must fail] UNDER B'S OWN TIMING ARGUMENT THE PAIRS ARE NOT TOO FAST: with h48b's baryons (Upsilon_K
      = 0.6, no gas), so that only the orbit changes, the timing amplitude lies in [0.80, 1.25], both footings.
  H4  THE TIMING PROFILE: under B's timing speeds the amplitude changes by < 2 sigma between the inner and the outer separation
      tertile (canonical): the fall of the dispersion with separation is predicted with no free parameter.
  H5  THE ORBIT MODEL IS NOT A UNIVERSAL RESCUE: LambdaCDM's abundance-matched halos under the same timing argument give
      A < 0.80 (they over-predict), so the pair test measures (law x orbits) and the two laws sit in opposite orbit models.
  R1-R10 (reported): the radial-orbit and the geometry-consistent circular projections; a steeper companion density (n ~
      r^-3); the later timing branches (outgoing after the first pericentre; the second approach); a growing mass (M ~ t);
      favourable and realistic baryons under timing; the Local Group against B's timing; the mass tertiles; the isolation
      scan F = 2-8; the ALFALFA dwarf pairs of h47 (d3 > 5 r_p); LambdaCDM's halos as NFW under timing.
  READING (declared):
    H3 in [0.80, 1.25] -> B1 is not a failure of B's law as such.  It was one only under circular orbits, which the data
      reject for both laws (H2).  Under the law's own timing orbits B gives the pair speeds; LambdaCDM's halos under the
      same orbits over-predict (H5).  Which orbits apply is B's to specify, not a knob: timing orbits if B's dark density
      exerts no dynamical friction on the pair (T5's identity read literally -- the dark density is the law's phantom,
      slaved to the baryons); virialised orbits if its cold component acts as a free medium, and then B1 stands at H1's
      level.
    H3 < 0.80 -> the two orbit models bracket the data for B (circular too slow, timing too fast): B1 is orbit-degenerate,
      not an established failure.
    H3 > 1.25 -> B1 stands under both orbit models.
MUTATE=1: every velocity difference halved -- H3 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG30_binary_galaxies_referee.py   (MUTATE=1 for the control; ~3-6 min)
"""
import os, sys, math, json, re
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG30_binary_galaxies_referee", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every velocity difference halved -- H3 must FAIL ***")
MUT = 0.5 if MUTATE else 1.0
FOOTS = ("canonical", "alt")

HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)
# ------------------------------------------------------------------------------------------------ h48b, exec'd read-only
P48 = os.path.join(HUNT, "h48_h69b_relative_isolation.py")
g48, _ = C4.exec_slices(P48, [(None, 'P(""); P("-"*122)\ninfo("THE SCAN.')], name="h48b_prefix")
rp = np.asarray(g48["rp"], float); dv0 = np.asarray(g48["dv"], float)
M1, M2, L1, L2 = (np.asarray(g48[k], float) for k in ("M1", "M2", "L1", "L2"))
ml_sigma, sigma_pred, mask_rel = g48["ml_sigma"], g48["sigma_pred"], g48["mask_rel"]
v_rel_deepmond, halo_mass, nfw_enclosed = g48["v_rel_deepmond"], g48["halo_mass"], g48["nfw_enclosed"]
A0H, UPS_K = g48["A0"], g48["UPS_K"]
G_SI, MSUN_KG, KPC_M = g48["G"], g48["Msun"], g48["kpc"]
V_ERR, DV_MAX = g48["V_ERR"], g48["DV_MAX"]
dv = MUT * dv0
m5 = mask_rel(5.0)
P(f"\n  h48b's sample (exec'd read-only): {len(rp)} candidate major pairs; d3 > 5 r_p: {int(m5.sum())}; Upsilon_K = {UPS_K}")

# ================================================================================================ C1
R.banner("C1  CONTROL: h48b's committed d3 > 5 r_p amplitudes")
o48 = open(os.path.join(HUNT, "h48_h69b_relative_isolation.out")).read()
com = {}
for f in FOOTS:
    mm = re.search(rf"{f}\s*: A\(isolated deep-MOND\) = ([0-9.]+) \+/- ([0-9.]+)", o48)
    com[f] = (float(mm.group(1)), float(mm.group(2)))
row5 = re.search(r"^\s+5\s+(\d+)\s+(\d+)\s+([0-9.]+)\s+([0-9.]+) \+/-\s*([0-9.]+)\s+([0-9.]+) \+/-\s*([0-9.]+)\s+([0-9.]+) \+/-\s*"
                 r"([0-9.]+)\s+([0-9.]+) \+/-\s*([0-9.]+)", o48, re.M)
com["lcdm"] = (float(row5.group(10)), float(row5.group(11)))
n5_com = int(row5.group(1))
C1 = {f: ml_sigma(dv0[m5], sig_shape=sigma_pred(M1[m5], M2[m5], rp[m5], "deepmond", a0=A0H[f])) for f in FOOTS}
C1["lcdm"] = ml_sigma(dv0[m5], sig_shape=sigma_pred(M1[m5], M2[m5], rp[m5], "lcdm"))
dev1 = max(max(abs(C1[k][0] - com[k][0]), abs(C1[k][1] - com[k][1])) for k in com)
check("C1 CONTROL: h48b's committed d3 > 5 r_p amplitudes reproduced to the printed precision (deep-MOND canonical / alt, LambdaCDM)",
      "; ".join(f"{k}: {C1[k][0]:.4f} +- {C1[k][1]:.4f} (committed {com[k][0]:.2f} +- {com[k][1]:.2f})" for k in com)
      + f"; N = {int(m5.sum())} (committed {n5_com})",
      dev1 <= 0.005 + 1e-9 and int(m5.sum()) == n5_com)

# ================================================================================================ the timing solver
T0 = float(C.LCDM.t(1.0))                                                      # Mpc/(km/s)
LAMP = float(C.LCDM.OL * C.LCDM.H0 ** 2)                                       # Omega_L H0^2 [(km/s/Mpc)^2]
LAM = LAMP * T0 ** 2                                                           # dimensionless, in units of t0
GLX, GLW = np.polynomial.legendre.leggauss(160)
WMAX = 6.0
PMAX_B, PMAX_K = 1.0 / math.sqrt(LAM), LAM ** (-1.0 / 3.0)                     # the Lambda-balance radii (units below)
P(f"\n  timing units: t0 = {T0 * C.UNIT_GYR:.3f} Gyr; lambda = Omega_L (H0 t0)^2 = {LAM:.4f}")


def _gl(lo, hi):
    lo = np.asarray(lo, float)[..., None]; hi = np.asarray(hi, float)[..., None]
    return 0.5 * (hi - lo) * GLX + 0.5 * (hi + lo), 0.5 * (hi - lo) * GLW


# B: the deep-MOND two-body law + Lambda; units v_c = 1, length v_c t0, time t0; phi = ln rho - lam rho^2 / 2.
# rho = P exp(-w^2) makes the integrand smooth at both ends.
def tB(P_, wlo, whi, lam=LAM):
    P_ = np.asarray(P_, float)
    x, w = _gl(wlo, whi)
    Pb = P_[..., None]
    den = 2 * x ** 2 + lam * Pb ** 2 * np.expm1(-2 * x ** 2)                   # 2 w^2 - lam P^2 (1 - e^-2w^2) > 0 for lam P^2 < 1
    return np.sum(w * 2 * Pb * x * np.exp(-x ** 2) / np.sqrt(den), axis=-1)


def tB_rise(P_, lam=LAM):
    P_ = np.asarray(P_, float)
    return tB(P_, np.zeros_like(P_), np.full_like(P_, WMAX), lam)


def tB_fall(P_, rho, lam=LAM):
    P_ = np.asarray(P_, float)
    return tB(P_, np.zeros_like(P_), np.sqrt(np.log(P_ / rho)), lam)


def vB(P_, rho, lam=LAM):
    return np.sqrt(np.maximum(2 * np.log(P_ / rho) - lam * (P_ ** 2 - rho ** 2), 0.0))


# K: point masses + Lambda; units G M = 1, t0 = 1; phi = -1/rho - lam rho^2 / 2; rho = P sin^2(eta).
def tK(P_, elo, ehi, lam=LAM):
    P_ = np.asarray(P_, float)
    x, w = _gl(elo, ehi)
    Pb = P_[..., None]; s2 = np.sin(x) ** 2
    return np.sum(w * math.sqrt(2) * Pb * s2 / np.sqrt(1 / Pb - 0.5 * lam * Pb ** 2 * s2 * (1 + s2)), axis=-1)


def tK_rise(P_, lam=LAM):
    P_ = np.asarray(P_, float)
    return tK(P_, np.zeros_like(P_), np.full_like(P_, math.pi / 2), lam)


def tK_fall(P_, rho, lam=LAM):
    P_ = np.asarray(P_, float)
    return tK(P_, np.arcsin(np.sqrt(np.clip(rho / P_, 0, 1))), np.full_like(P_, math.pi / 2), lam)


def vK(P_, rho, lam=LAM):
    return np.sqrt(np.maximum(2 * (1 / rho - 1 / P_) - lam * (P_ ** 2 - rho ** 2), 0.0))


def T_of(law, P_, rho, k):
    tr, tf = (tB_rise(P_), tB_fall(P_, rho)) if law == "B" else (tK_rise(P_), tK_fall(P_, rho))
    return {0: tr + tf, 1: 3 * tr - tf, 2: 3 * tr + tf}[k] - 1.0                # first approach; outgoing after pericentre; second approach


GGRID = np.concatenate([np.geomspace(1e-10, 0.5, 120), 1 - np.geomspace(0.5, 1e-10, 120)[1:]])


def solve_branch(rho, k, law, chunk=40):
    """the apocentre P with T_k(P, rho) = t0 (first upward crossing on a dense grid, then bisection); NaN where none."""
    pmax = PMAX_B if law == "B" else PMAX_K
    rho = np.atleast_1d(np.asarray(rho, float)); out = np.full(rho.shape, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        for i0 in range(0, len(rho), chunk):
            rr = rho[i0:i0 + chunk]; n = len(rr); ix = np.arange(n)
            Pg = rr[:, None] + (pmax * (1 - 1e-12) - rr)[:, None] * GGRID[None, :]
            T = T_of(law, Pg, np.broadcast_to(rr[:, None], Pg.shape), k)
            cross = (T[:, 1:] >= 0) & (T[:, :-1] < 0)
            has = cross.any(axis=1); j = np.argmax(cross, axis=1)
            lo = np.where(has, Pg[ix, j], rr * 1.5); hi = np.where(has, Pg[ix, j + 1], rr * 1.5)
            for _ in range(64):
                mid = 0.5 * (lo + hi)
                neg = T_of(law, mid, rr, k) < 0
                lo = np.where(neg, mid, lo); hi = np.where(neg, hi, mid)
            out[i0:i0 + n] = np.where(has, 0.5 * (lo + hi), np.nan)
    return out


def rho_ta0(law):
    tr, pmax = (tB_rise, PMAX_B) if law == "B" else (tK_rise, PMAX_K)
    lo, hi = 1e-6, pmax * (1 - 1e-12)
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if float(tr(np.array([mid]))[0]) < 1.0 else (lo, mid)
    return lo


def build_table(law):
    rta = rho_ta0(law)
    rho = np.unique(np.concatenate([np.geomspace(1e-4, 0.5 * rta, 300), rta * (1 - np.geomspace(0.5, 1e-7, 250))]))
    tab = {"rho": rho, "rta": rta}
    vf = vB if law == "B" else vK
    for k in (0, 1, 2):
        Pk = solve_branch(rho, k, law)
        with np.errstate(invalid="ignore"):
            tab[k] = np.where(np.isfinite(Pk), vf(Pk, rho) ** 2, np.nan)
        tab[f"P{k}"] = Pk
    return tab


def nu2_of(tab, k, rho):
    rho = np.asarray(rho, float); sh = rho.shape
    y = tab[k]; ok = np.isfinite(y)
    out = np.interp(np.log(rho.ravel()), np.log(tab["rho"][ok]), y[ok], left=np.nan, right=np.nan)
    return out.reshape(sh)


TAB_B, TAB_K = build_table("B"), build_table("K")
P(f"  B (deep-MOND two-body + Lambda): turnaround today at rho = {TAB_B['rta']:.4f} v_c t0; first approach at rho = 0.02 / 0.06 / 0.2: "
  f"v/v_c = " + " / ".join(f"{math.sqrt(nu2_of(TAB_B, 0, np.array([x]))[0]):.3f}" for x in (0.02, 0.06, 0.2)))
P(f"  K (point masses + Lambda): turnaround today at rho = {TAB_K['rta']:.4f} (G M t0^2)^(1/3)")

# ================================================================================================ C2
R.banner("C2  CONTROL: the timing solver")
Pt = np.array([0.05, 0.3, 0.9]); rt = np.array([0.004, 0.1, 0.5])
eB = max(float(np.max(np.abs(tB_rise(Pt, 0.0) / (math.sqrt(math.pi / 2) * Pt) - 1))),
         float(np.max(np.abs(tB_fall(Pt, rt, 0.0) / (math.sqrt(math.pi / 2) * Pt * erf(np.sqrt(np.log(Pt / rt)))) - 1))))
eta = np.arcsin(np.sqrt(rt / Pt))
eK = max(float(np.max(np.abs(tK_rise(Pt, 0.0) / (math.pi / (2 * math.sqrt(2)) * Pt ** 1.5) - 1))),
         float(np.max(np.abs(tK_fall(Pt, rt, 0.0) / (math.sqrt(2) * Pt ** 1.5 * (math.pi / 4 - eta / 2 + np.sin(2 * eta) / 4)) - 1))))
check("C2a CONTROL: the Lambda = 0 analytic limits (log potential and Kepler, rise and fall) to 1e-6",
      f"max relative error: log {eB:.1e}, Kepler {eK:.1e}", max(eB, eK) < 1e-6)

# (b) direct ODE integration from the apocentre (forward to t0, backward to the Big Bang)
rho_c = np.array([0.02, 0.06, 0.2]); Pc = solve_branch(rho_c, 0, "B"); vcc = vB(Pc, rho_c); tap = tB_rise(Pc)
e_ode, e_bb = 0.0, 0.0
for P_, t_, r_, v_ in zip(Pc, tap, rho_c, vcc):
    rhs = lambda t, y: [y[1], -1.0 / y[0] + LAM * y[0]]
    s = solve_ivp(rhs, (t_, 1.0), [P_, 0.0], method="DOP853", rtol=1e-12, atol=1e-14)
    e_ode = max(e_ode, abs(s.y[0, -1] / r_ - 1), abs(-s.y[1, -1] / v_ - 1))
    ev = lambda t, y: y[0] - 1e-7
    ev.terminal = True; ev.direction = -1
    sb = solve_ivp(rhs, (t_, 1e-6), [P_, 0.0], method="DOP853", rtol=1e-12, atol=1e-15, events=ev)
    t_end = sb.t_events[0][0] if len(sb.t_events[0]) else sb.t[-1]
    e_bb = max(e_bb, abs(t_end))


def shoot(a, growth):
    ti = 1e-6
    rhs = (lambda t, y: [y[1], -math.sqrt(t) / y[0] + LAM * y[0]]) if growth else (lambda t, y: [y[1], -1.0 / y[0] + LAM * y[0]])
    ev = lambda t, y: y[0] - 1e-9
    ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, (ti, 1.0), [a * ti, a], method="DOP853", rtol=1e-10, atol=1e-14, events=ev)
    return s.status == 1, float(s.y[0, -1]), float(s.y[1, -1])


def shoot_table(growth):
    """the first-approach (rho(t0), v(t0)) family from the Big Bang by shooting on the initial expansion speed."""
    As = np.geomspace(0.05, 60.0, 90)
    res = [shoot(a, growth) for a in As]
    coll = np.array([r_[0] for r_ in res]); vend = np.array([r_[2] for r_ in res])
    i = int(np.where(coll[:-1] & ~coll[1:])[0][0])
    lo, hi = As[i], As[i + 1]
    for _ in range(55):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if shoot(mid, growth)[0] else (lo, mid)
    a_c = hi
    # the infall window can be narrower than the scan's step (the log potential's Big-Bang start makes it so): bracket it from a_c
    k_ = int(np.where((np.arange(len(As)) > i) & ~coll & (vend > 0))[0][0])
    lo, hi = a_c, As[k_]
    for _ in range(55):
        mid = 0.5 * (lo + hi)
        c_, _, v1 = shoot(mid, growth)
        lo, hi = (mid, hi) if (not c_ and v1 < 0) else (lo, mid)
    a_ta = lo
    gg = np.concatenate([np.geomspace(1e-11, 0.5, 150), 1 - np.geomspace(0.5, 1e-7, 70)[1:]])
    rows = []
    for g_ in gg:
        c_, r1, v1 = shoot(a_c + (a_ta - a_c) * g_, growth)
        if not c_ and v1 < 0 and r1 > 0:
            rows.append((r1, v1 * v1))
    arr = np.array(sorted(rows))
    keep = np.concatenate([[True], np.diff(arr[:, 0]) > 0])
    arr = arr[keep]
    return {"rho": arr[:, 0], 0: arr[:, 1], "rta": float(arr[-1, 0]), "a": (a_c, a_ta)}


SH0 = shoot_table(False)
sel_ = (SH0["rho"] > 2e-3) & (SH0["rho"] < 0.9 * TAB_B["rta"])
e_sh = float(np.max(np.abs(np.sqrt(SH0[0][sel_] / nu2_of(TAB_B, 0, SH0["rho"][sel_])) - 1)))
check("C2b CONTROL: a direct ODE integration from the apocentre lands on the tabulated first-approach (r, v) to 1e-4 and passes r = 0 "
      "at the Big Bang; the ODE shooter reproduces the quadrature table to 2e-3 at constant mass",
      f"forward landing max relative error {e_ode:.1e}; backward: r -> 0 at t = {e_bb:.1e} t0; shooter vs quadrature (v, {int(sel_.sum())} "
      f"points, 2e-3 < rho < 0.9 rho_ta) max {e_sh:.1e}",
      e_ode < 1e-4 and e_bb < 2e-3 and e_sh < 2e-3)


# (c) the general-potential solver (for the NFW variant), validated on a point mass
def gen_timing(Menc, rg, rq_kpc):
    """per row: the first-approach speed^2 [(km/s)^2] at the radii rq for the enclosed-mass potential Menc(rg) (constant beyond the
    grid) + Lambda; radial timing from the Big Bang by the quadrature r' = P (1 - s^2)."""
    N = Menc.shape[0]; lr = np.log(rg / 1e3); dl = lr[1] - lr[0]
    integ = Menc / (rg / 1e3)[None, :]
    seg = 0.5 * (integ[:, 1:] + integ[:, :-1]) * np.diff(lr)[None, :]
    cum = np.concatenate([np.cumsum(seg[:, ::-1], axis=1)[:, ::-1], np.zeros((N, 1))], axis=1)
    phig = -C.GMPC * (cum + (Menc[:, -1] / (rg[-1] / 1e3))[:, None]) - 0.5 * LAMP * (rg / 1e3)[None, :] ** 2
    rows = np.arange(N)[:, None]

    def phi_at(rr):
        x = (np.log(rr) - lr[0]) / dl
        j = np.clip(np.floor(x).astype(int), 0, len(lr) - 2); t = np.clip(x - j, 0.0, 1.0)
        return (1 - t) * phig[rows, j] + t * phig[rows, j + 1]
    pmax = rg[np.argmax(phig, axis=1)] / 1e3 * (1 - 1e-9)
    XQ, WQ = np.polynomial.legendre.leggauss(96)

    def slope_at(Pv):                                           # d phi / d ln r of the interpolant in P's own segment
        j = np.clip(np.floor((np.log(Pv) - lr[0]) / dl).astype(int), 0, len(lr) - 2)
        return (phig[np.arange(N), j + 1] - phig[np.arange(N), j]) / dl

    def t_int(Pv, shi):
        x = 0.5 * shi[:, None] * (XQ + 1); w = 0.5 * shi[:, None] * WQ
        rr = np.maximum(Pv[:, None] * (1 - x ** 2), 1e-9)
        d = phi_at(Pv[:, None]) - phi_at(rr)
        dlnr = -np.log1p(-np.minimum(x ** 2, 1 - 1e-16))
        d = np.where(dlnr < 1e-6, slope_at(Pv)[:, None] * dlnr, d)  # the interpolant is linear in ln r there: exact, no cancellation
        return np.sum(w * 2 * Pv[:, None] * x / np.sqrt(np.maximum(2 * d, 1e-300)), axis=1)
    out = np.full((N, len(rq_kpc)), np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        for iq, rq in enumerate(np.asarray(rq_kpc, float) / 1e3):
            r0 = np.full(N, rq)
            Tm = lambda Pv: t_int(Pv, np.ones(N)) + t_int(Pv, np.sqrt(np.clip(1 - r0 / Pv, 0, 1))) - T0
            lo = r0 * (1 + 1e-6); hi = np.maximum(pmax, lo * (1 + 1e-6))
            ok = (pmax > lo) & (Tm(lo) < 0) & (Tm(hi) > 0)
            for _ in range(55):
                mid = 0.5 * (lo + hi)
                neg = Tm(mid) < 0
                lo = np.where(neg, mid, lo); hi = np.where(neg, hi, mid)
            Pv = 0.5 * (lo + hi)
            out[:, iq] = np.where(ok, 2 * (phi_at(Pv[:, None]) - phi_at(r0[:, None]))[:, 0], np.nan)
    return out


RG = np.geomspace(0.5, 3e4, 700)
MPT = 1e13
rq_t = np.array([20.0, 100.0, 300.0, 800.0])
v2_gen = gen_timing(np.full((1, len(RG)), MPT), RG, rq_t)[0]
lu_pt = (C.GMPC * MPT * T0 ** 2) ** (1 / 3) * 1e3; vu_pt = (C.GMPC * MPT / T0) ** (1 / 3)
v2_K = vu_pt ** 2 * nu2_of(TAB_K, 0, rq_t / lu_pt)
e_gen = float(np.max(np.abs(np.sqrt(v2_gen / v2_K) - 1)))
check("C2c CONTROL: the general-potential solver reproduces the Kepler table within 0.5% on a point mass (1e13 Msun, 20-800 kpc)",
      "v(general) / v(Kepler) - 1: " + ", ".join(f"{r_:.0f} kpc {math.sqrt(a_ / b_) - 1:+.1e}" for r_, a_, b_ in zip(rq_t, v2_gen, v2_K)),
      e_gen < 5e-3)


# (d) the Local Group against FP11's committed full two-body integration of the plain P2 law
def vunits_B(m1, m2, a0):
    vc = v_rel_deepmond(np.asarray(m1, float), np.asarray(m2, float), a0) / 1e3          # km/s
    return vc, vc * T0 * 1e3                                                            # velocity unit, length unit [kpc]


def vunits_K(m1s, m2s):
    Mt = halo_mass(np.asarray(m1s, float)) + halo_mass(np.asarray(m2s, float))
    return (C.GMPC * Mt / T0) ** (1 / 3), (C.GMPC * Mt * T0 ** 2) ** (1 / 3) * 1e3


FP11 = json.load(open(os.path.join(C.REPO, "real_research", "derivation_chain_2026", "FP11_local_group_flyby_results.json")))["numbers"]
SHARE, M_NOM = FP11["baryons"]["share_MW"], FP11["baryons"]["total"]
FPV = {}
for key, v in FP11["timing_scan"].items():
    law_, f_, M_ = key.split("/")
    if law_ == "P2":
        k0 = [b_["vr"] for b_ in v["A"] if b_["k"] == 0]
        if k0:
            FPV[(f_, float(M_))] = k0[0]
D_LG, VR_LG, EVR_LG = 0.78, -109.3, 4.4                          # FP11's committed inputs (van der Marel+2012)


def vB_at(Mb, f, d_mpc=D_LG, k=0, tab=None):
    vu, lu = vunits_B(np.array([SHARE * Mb]), np.array([(1 - SHARE) * Mb]), A0H[f])
    return float(vu[0] * np.sqrt(nu2_of(tab or TAB_B, k, np.array([d_mpc * 1e3 / lu[0]]))[0]))


lg_rows, lg_ok = [], True
for f in FOOTS:
    for Mb in (1.145e11, 1.75e11, 2.4e11):
        vm, vf_ = vB_at(Mb, f), abs(FPV[(f, Mb)])
        lg_rows.append(f"{f} {Mb:.3g}: {vm:.1f} vs FP11 {vf_:.1f} ({vm / vf_ - 1:+.1%})")
        lg_ok &= abs(vm / vf_ - 1) <= 0.10
check("C2d CONTROL: the Local Group -- B's first-approach speed at 0.78 Mpc (this lane's radial timing, pure deep-MOND two-body law + "
      "Lambda) reproduces FP11's committed full two-body integration of the plain P2 law (T4) within 10%, both footings",
      "; ".join(lg_rows), lg_ok)


# ================================================================================================ per-pair predictions
def prior(rpx, gamma=2, nmc=400, seed=1):
    """h48b's projection prior exactly (same generator, seed and draws); gamma = 3 tilts it to n(r) ~ r^-3."""
    g = np.random.default_rng(seed)
    u = g.random((len(rpx), nmc))
    r = rpx[:, None] * np.exp(u * math.log(20.0)) * 1.0001
    w = 1.0 / np.sqrt(np.maximum((r / rpx[:, None]) ** 2 - 1.0, 1e-6))
    if gamma == 3:
        w = w * rpx[:, None] / r
    return r, w


def sig_from(v2, r, w, rpx, geom="iso"):
    fg = {"iso": 1.0 / 3.0, "radial": 1 - (rpx[:, None] / r) ** 2, "circ": 0.5 * (rpx[:, None] / r) ** 2}[geom]
    ok = np.isfinite(v2)
    wb = np.where(ok, w, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.sqrt(np.sum(wb * np.where(ok, v2, 0.0) * fg, axis=1) / np.sum(wb, axis=1))


def sig_timing(law, m1, m2, rpx, a0=None, k=0, geom="iso", gamma=2, tab=None):
    vu, lu = vunits_B(m1, m2, a0) if law == "B" else vunits_K(m1, m2)
    r, w = prior(rpx, gamma)
    tab = tab if tab is not None else (TAB_B if law == "B" else TAB_K)
    return sig_from(nu2_of(tab, k, r / lu[:, None]) * vu[:, None] ** 2, r, w, rpx, geom)


def fitA(mask, shape, dvv=None):
    d = (dv if dvv is None else dvv)[mask]
    ok = np.isfinite(shape) & (shape > 0)
    if ok.sum() < 20:
        return dict(A=float("nan"), e=float("nan"), fint=float("nan"), n=int(ok.sum()), excl=int((~ok).sum()))
    A, e, fi = ml_sigma(d[ok], sig_shape=shape[ok])
    return dict(A=float(A), e=float(e), fint=float(fi), n=int(ok.sum()), excl=int((~ok).sum()))


def fmt(x):
    return f"{x['A']:.3f} +- {x['e']:.3f}"


circ_B = lambda f, m: sigma_pred(M1[m], M2[m], rp[m], "deepmond", a0=A0H[f])
circ_L = lambda m: sigma_pred(M1[m], M2[m], rp[m], "lcdm")
tim_B = lambda f, m, **kw: sig_timing("B", M1[m], M2[m], rp[m], a0=A0H[f], **kw)
tim_K = lambda m, **kw: sig_timing("K", M1[m], M2[m], rp[m], **kw)

# ================================================================================================ C3 the estimator on timing mocks
R.banner("C3  CONTROL: the estimator on the timing model's own velocities (B canonical, d3 > 5 r_p)")
vu5, lu5 = vunits_B(M1[m5], M2[m5], A0H["canonical"])
r5, w5 = prior(rp[m5])
nu5 = nu2_of(TAB_B, 0, r5 / lu5[:, None])
wb5 = np.where(np.isfinite(nu5), w5, 0.0); wb5 = wb5 / wb5.sum(axis=1, keepdims=True); cw5 = np.cumsum(wb5, axis=1)
s5 = tim_B("canonical", m5)
Amock = []
for sd in range(5):
    gm = np.random.default_rng(3000 + sd); n_ = len(vu5)
    jj = np.minimum((cw5 < gm.random(n_)[:, None]).sum(axis=1), r5.shape[1] - 1)
    vv = vu5 * np.sqrt(np.where(np.isfinite(nu5), nu5, 0.0)[np.arange(n_), jj])
    dm = vv * gm.uniform(-1, 1, n_) + gm.normal(0, V_ERR, n_)
    dm = np.where(gm.random(n_) < 0.17, gm.uniform(-DV_MAX, DV_MAX, n_), dm)
    Amock.append(ml_sigma(dm, sig_shape=s5))
mA = float(np.mean([a_[0] for a_ in Amock]))
check("C3 CONTROL: mock pairs drawn from B's timing prediction (isotropic directions, 40 km/s errors, 17% interlopers; A = 1) come "
      "back at A = 1 within 0.05 (mean of 5)",
      "recovered A: " + ", ".join(f"{a_[0]:.3f} +- {a_[1]:.3f} (f_int {a_[2]:.2f})" for a_ in Amock) + f"; mean {mA:.3f}", abs(mA - 1) < 0.05)

# ================================================================================================ H1 the baryons
R.banner("H1  THE BARYONS: the most favourable baryons under the circular model")
XD = os.path.join(C.REPO, "real_research", "data", "xgass", "xGASS_representative_sample.ascii")
hdr = open(XD).readline().lstrip("#").split()
tab_x = np.genfromtxt(XD, comments="#", dtype=None, encoding=None, names=hdr)
lms_x = np.asarray(tab_x["lgMstar"], float); lgHI = np.asarray(tab_x["lgMHI"], float)
det_x = np.asarray(tab_x["HIsrc"], int) != 4; wts_x = np.asarray(tab_x["weight"], float)
GAS_UL = 1.33 * 10 ** lgHI; GAS_DET = np.where(det_x, GAS_UL, 0.0)
BINS = np.round(np.arange(9.0, 11.501, 0.1), 2); BC = 0.5 * (BINS[:-1] + BINS[1:])


def fgas_fn(gas):
    fb = []
    for lo_, hi_ in zip(BINS[:-1], BINS[1:]):
        mm = (lms_x >= lo_) & (lms_x < hi_)
        fb.append(np.sum(wts_x[mm] * gas[mm] / 10 ** lms_x[mm]) / np.sum(wts_x[mm]) if mm.sum() >= 3 else np.nan)
    fb = np.array(fb); ok = np.isfinite(fb)
    return lambda lm: np.interp(lm, BC[ok], fb[ok])


fg_UL, fg_DET = fgas_fn(GAS_UL), fgas_fn(GAS_DET)
LBOOST = 10 ** (0.4 * 0.3)
Ms1f, Ms2f = 1.0 * L1 * LBOOST, 1.0 * L2 * LBOOST
Mb1f, Mb2f = Ms1f * (1 + 2 * fg_UL(np.log10(Ms1f))), Ms2f * (1 + 2 * fg_UL(np.log10(Ms2f)))
Mb1r, Mb2r = UPS_K * L1 * (1 + fg_DET(np.log10(UPS_K * L1))), UPS_K * L2 * (1 + fg_DET(np.log10(UPS_K * L2)))
boost = np.median(np.log10((Mb1f + Mb2f)[m5] / (M1 + M2)[m5]))
P(f"    xGASS gas fraction (upper limits) at log M* = 10.5 / 11.0 / 11.4: " + " / ".join(f"{fg_UL(x):.3f}" for x in (10.5, 11.0, 11.4))
  + f"; favourable baryons are +{boost:.3f} dex over h48b's (median, d3 > 5 r_p)")
H1 = {}
for f in FOOTS:
    H1[f] = fitA(m5, sigma_pred(Mb1f[m5], Mb2f[m5], rp[m5], "deepmond", a0=A0H[f]))
    H1[f]["z"] = (H1[f]["A"] - 1) / H1[f]["e"]
check("H1 THE BARYONS CANNOT CLOSE THE CIRCULAR GAP: with Upsilon_K = 1.0, +0.3 mag of K light and doubled xGASS gas (upper limits) the "
      "circular amplitude stays > 1.3 and > 5 sigma above 1, both footings",
      "; ".join(f"{f}: A = {fmt(H1[f])} ({H1[f]['z']:.1f} sigma above 1)" for f in FOOTS),
      all(H1[f]["A"] > 1.3 and H1[f]["z"] > 5 for f in FOOTS))

# ================================================================================================ H2 / H4 the separation profile
R.banner("H2 / H4  THE SEPARATION PROFILE (tertiles of r_p at d3 > 5 r_p)")
q1, q2 = np.quantile(rp[m5], [1 / 3, 2 / 3])
TER = {"inner": m5 & (rp < q1), "middle": m5 & (rp >= q1) & (rp < q2), "outer": m5 & (rp >= q2)}
PROF = {}
for lab, mm in TER.items():
    s_, e_, fi_ = ml_sigma(dv[mm])
    PROF[lab] = dict(n=int(mm.sum()), rp_med=float(np.median(rp[mm])), sigma=float(s_), esig=float(e_), fint=float(fi_),
                     circ_B=fitA(mm, circ_B("canonical", mm)), circ_L=fitA(mm, circ_L(mm)),
                     tim_B=fitA(mm, tim_B("canonical", mm)), tim_Balt=fitA(mm, tim_B("alt", mm)), tim_K=fitA(mm, tim_K(mm)))
    p_ = PROF[lab]
    P(f"    {lab:6s} (N {p_['n']}, median r_p {p_['rp_med']:5.0f} kpc): sigma {p_['sigma']:5.1f} +- {p_['esig']:4.1f} km/s, f_int {p_['fint']:.2f};  "
      f"A circular B {fmt(p_['circ_B'])}, LCDM {fmt(p_['circ_L'])};  A timing B {fmt(p_['tim_B'])} (alt {fmt(p_['tim_Balt'])}), LCDM {fmt(p_['tim_K'])}")


def zdrop(key):
    a, b = PROF["inner"][key], PROF["outer"][key]
    return (a["A"] - b["A"]) / math.hypot(a["e"], b["e"])


zB, zL, zT, zTa = zdrop("circ_B"), zdrop("circ_L"), zdrop("tim_B"), zdrop("tim_Balt")
check("H2 THE CIRCULAR MODEL FAILS THE DATA'S OWN PROFILE for BOTH laws: the circular amplitude falls from the inner to the outer tertile "
      "by > 3 sigma (B canonical, LambdaCDM)  [seen in the scratch look]",
      f"inner - outer: B {PROF['inner']['circ_B']['A'] - PROF['outer']['circ_B']['A']:+.3f} ({zB:.1f} sigma); LambdaCDM "
      f"{PROF['inner']['circ_L']['A'] - PROF['outer']['circ_L']['A']:+.3f} ({zL:.1f} sigma)", zB > 3 and zL > 3)

# ================================================================================================ H3 the headline
R.banner("H3  THE HEADLINE: B's own timing argument, h48b's baryons, d3 > 5 r_p")
H3 = {f: fitA(m5, tim_B(f, m5)) for f in FOOTS}
for f in FOOTS:
    P(f"    {f:9s}: timing A = {fmt(H3[f])} (f_int {H3[f]['fint']:.2f}, {H3[f]['n']} pairs, {H3[f]['excl']} without a bound configuration); "
      f"circular A = {C1[f][0]:.3f}")
check("H3 [HEADLINE] UNDER B'S OWN TIMING ARGUMENT THE PAIRS ARE NOT TOO FAST: with h48b's baryons the timing amplitude lies in [0.80, 1.25], "
      "both footings" + ("  [MUTATE: velocities halved]" if MUTATE else ""),
      "; ".join(f"{f}: A = {fmt(H3[f])}" for f in FOOTS), all(0.80 <= H3[f]["A"] <= 1.25 for f in FOOTS))
check("R0 (reported; added after the MUTATE run) H3 divided by the estimator's bias on the timing model's own velocities (C3's mean "
      "recovery)", "; ".join(f"{f}: {H3[f]['A'] / mA:.3f} +- {H3[f]['e'] / mA:.3f}" for f in FOOTS), True, load_bearing=False)
check("H4 THE TIMING PROFILE: under B's timing speeds the amplitude changes by < 2 sigma between the inner and outer tertile (canonical)",
      f"inner {fmt(PROF['inner']['tim_B'])}, middle {fmt(PROF['middle']['tim_B'])}, outer {fmt(PROF['outer']['tim_B'])}: "
      f"inner - outer {zT:+.1f} sigma (alt {zTa:+.1f} sigma)", abs(zT) < 2)

# ================================================================================================ H5 LambdaCDM under timing
R.banner("H5  LambdaCDM's halos under the same timing argument")
H5 = fitA(m5, tim_K(m5))
check("H5 THE ORBIT MODEL IS NOT A UNIVERSAL RESCUE: LambdaCDM's abundance-matched halos (point masses + Lambda) under the same timing "
      "argument give A < 0.80 at d3 > 5 r_p",
      f"LambdaCDM timing A = {fmt(H5)} (circular {C1['lcdm'][0]:.3f})", H5["A"] < 0.80)

# ================================================================================================ the reported rows
R.banner("R1-R10  REPORTED VARIANTS")
REP = {}
# R1 geometry
REP["R1"] = dict(tim_B_radial=fitA(m5, tim_B("canonical", m5, geom="radial")),
                 circ_B_consistent=fitA(m5, sig_from(np.repeat((v_rel_deepmond(M1[m5], M2[m5], A0H["canonical"]) / 1e3)[:, None] ** 2, 400, axis=1),
                                                     *prior(rp[m5]), rp[m5], "circ")))
r5_, w5_ = prior(rp[m5])
v2L = G_SI * (nfw_enclosed(halo_mass(M1[m5])[:, None], r5_) + nfw_enclosed(halo_mass(M2[m5])[:, None], r5_)) * MSUN_KG / (r5_ * KPC_M) / 1e6
REP["R1"]["circ_L_consistent"] = fitA(m5, sig_from(v2L, r5_, w5_, rp[m5], "circ"))
REP["R1"]["tim_K_radial"] = fitA(m5, tim_K(m5, geom="radial"))
check("R1 (reported) projection geometry: radial-orbit projection for the timing speeds; geometry-consistent projection for circular orbits",
      f"B timing radial {fmt(REP['R1']['tim_B_radial'])}; LCDM timing radial {fmt(REP['R1']['tim_K_radial'])}; B circular consistent "
      f"{fmt(REP['R1']['circ_B_consistent'])}; LCDM circular consistent {fmt(REP['R1']['circ_L_consistent'])}", True, load_bearing=False)
# R2 steeper companion density
REP["R2"] = dict(tim_B=fitA(m5, tim_B("canonical", m5, gamma=3)), tim_K=fitA(m5, tim_K(m5, gamma=3)))
check("R2 (reported) a steeper companion density n(r) ~ r^-3 in the projection prior (timing)",
      f"B {fmt(REP['R2']['tim_B'])}; LCDM {fmt(REP['R2']['tim_K'])}", True, load_bearing=False)
# R3 later branches
REP["R3"] = {f"k{k}": fitA(m5, tim_B("canonical", m5, k=k)) for k in (1, 2)}
check("R3 (reported) the later timing branches for B (k = 1: outgoing after the first pericentre; k = 2: the second approach)",
      "; ".join(f"{k}: A = {fmt(v)} ({v['excl']} pairs without a configuration on the branch)" for k, v in REP["R3"].items()), True, load_bearing=False)
# R4 growing mass
SHG = shoot_table(True)
REP["R4"] = {f: fitA(m5, tim_B(f, m5, tab=SHG)) for f in FOOTS}
check("R4 (reported) a growing baryonic mass, M ~ t (so v_c^2 ~ t^1/2 in deep MOND), by the ODE shooter",
      f"turnaround today at rho = {SHG['rta']:.3f} (constant mass {TAB_B['rta']:.3f}); A = " + "; ".join(f"{f} {fmt(REP['R4'][f])}" for f in FOOTS),
      True, load_bearing=False)
# R5 favourable and realistic baryons under timing
REP["R5"] = {}
for f in FOOTS:
    REP["R5"][f] = dict(fav=fitA(m5, sig_timing("B", Mb1f[m5], Mb2f[m5], rp[m5], a0=A0H[f])),
                        real=fitA(m5, sig_timing("B", Mb1r[m5], Mb2r[m5], rp[m5], a0=A0H[f])),
                        real_circ=fitA(m5, sigma_pred(Mb1r[m5], Mb2r[m5], rp[m5], "deepmond", a0=A0H[f])))
check("R5 (reported) baryons under timing: H1's favourable ceilings, and realistic (Upsilon_K = 0.6 + xGASS detected gas)",
      "; ".join(f"{f}: favourable {fmt(v['fav'])}, realistic {fmt(v['real'])} (circular {fmt(v['real_circ'])})" for f, v in REP["R5"].items()),
      True, load_bearing=False)
# R6 the Local Group
REP["R6"] = {}
for f in FOOTS:
    vn = vB_at(M_NOM, f)
    lo_, hi_ = 1e9, 1e12
    for _ in range(80):
        mid = math.sqrt(lo_ * hi_)
        vm_ = vB_at(mid, f)                                          # NaN = not yet turned around: slower than any bound approach
        lo_, hi_ = (mid, hi_) if (not np.isfinite(vm_) or vm_ < abs(VR_LG)) else (lo_, mid)
    REP["R6"][f] = dict(v_nom=vn, ratio=vn / abs(VR_LG), z=(vn - abs(VR_LG)) / EVR_LG, M_timing=math.sqrt(lo_ * hi_),
                        v_window=[vB_at(1.145e11, f), vB_at(2.4e11, f)])
check("R6 (reported) THE LOCAL GROUP AGAINST B'S TIMING: MW-M31 at 0.78 Mpc, FP11's baryons (nominal 1.75e11, window 1.145-2.4e11) vs the "
      "measured -109.3 +- 4.4 km/s",
      "; ".join(f"{f}: predicted -{v['v_nom']:.0f} km/s at the nominal mass (window -{v['v_window'][0]:.0f} to -{v['v_window'][1]:.0f}), "
                f"{v['ratio']:.2f}x the measured speed; the timing would need M_b = {v['M_timing']:.2e}" for f, v in REP["R6"].items()),
      True, load_bearing=False)
# R7 mass tertiles
lmb = np.log10(M1 + M2)
mq1, mq2 = np.quantile(lmb[m5], [1 / 3, 2 / 3])
MT = {"low": m5 & (lmb < mq1), "mid": m5 & (lmb >= mq1) & (lmb < mq2), "high": m5 & (lmb >= mq2)}
REP["R7"] = {k: dict(tim_B=fitA(mm, tim_B("canonical", mm)), circ_B=fitA(mm, circ_B("canonical", mm)), circ_L=fitA(mm, circ_L(mm)),
                    tim_K=fitA(mm, tim_K(mm)), logMb=float(np.median(lmb[mm]))) for k, mm in MT.items()}
ztr = {key: (REP["R7"]["high"][key]["A"] - REP["R7"]["low"][key]["A"]) / math.hypot(REP["R7"]["high"][key]["e"], REP["R7"]["low"][key]["e"])
       for key in ("tim_B", "circ_B", "circ_L", "tim_K")}
REP["R7_trend_z"] = ztr
check("R7 (reported; the LambdaCDM columns and the trend significance added after the MUTATE run) the mass tertiles",
      "; ".join(f"{k} (log M_b {v['logMb']:.2f}): B timing {fmt(v['tim_B'])}, B circular {fmt(v['circ_B'])}, LCDM circular {fmt(v['circ_L'])}, "
                f"LCDM timing {fmt(v['tim_K'])}" for k, v in REP["R7"].items() if isinstance(v, dict) and "logMb" in v)
      + "; high - low: " + ", ".join(f"{k} {z:+.1f} sigma" for k, z in ztr.items()), True, load_bearing=False)
# R8 the isolation scan
REP["R8"] = {}
for F_ in (2.0, 3.0, 5.0, 8.0):
    mm = mask_rel(F_)
    REP["R8"][F_] = dict(n=int(mm.sum()), tim_B=fitA(mm, tim_B("canonical", mm)), tim_K=fitA(mm, tim_K(mm)), circ_B=fitA(mm, circ_B("canonical", mm)))
check("R8 (reported) the isolation scan d3 > F r_p under timing (B canonical, LambdaCDM point masses) and circular (B)",
      "; ".join(f"F {F_:.0f} (N {v['n']}): B timing {fmt(v['tim_B'])}, LCDM timing {fmt(v['tim_K'])}, B circular {fmt(v['circ_B'])}"
                for F_, v in REP["R8"].items()), True, load_bearing=False)
# R9 the ALFALFA dwarf pairs of h47
P47 = os.path.join(HUNT, "h47_dwarf_pairs.py")
g47, _ = C4.exec_slices(P47, [(None, 'P("="*122); P("SECTION 1'), ("rows = [l.rstrip", 'info(f"FINAL SAMPLE')], name="h47_slices")
m47 = g47["sample_mask"](5.0)
i1, i2 = g47["ia"][g47["p"][m47]], g47["ia"][g47["q"][m47]]
mb1, mb2 = g47["mb_of"](i1), g47["mb_of"](i2)
rp47, dv47 = np.asarray(g47["rp"][m47], float), MUT * np.asarray(g47["dv"][m47], float)
ml47 = lambda s: g47["ml_sigma"](dv47[np.isfinite(s)], sig_shape=s[np.isfinite(s)], dvmax=g47["DV_WIN"], verr=g47["V_ERR_HI"])
REP["R9"] = dict(n=int(m47.sum()), circ=ml47(g47["sigma_pred"](mb1, mb2, rp47, "deepmond", a0=g47["A0"]["canonical"])),
                 tim={f: ml47(sig_timing("B", mb1, mb2, rp47, a0=A0H[f])) for f in FOOTS}, tim_K=ml47(sig_timing("K", mb1, mb2, rp47)))
check("R9 (reported) the ALFALFA dwarf pairs of h47 at d3 > 5 r_p (h47's sample, masses and estimator, exec'd read-only)",
      f"N = {REP['R9']['n']}; circular {REP['R9']['circ'][0]:.2f} +- {REP['R9']['circ'][1]:.2f} (h47 committed 1.12 +- 0.29); B timing "
      + ", ".join(f"{f} {v[0]:.2f} +- {v[1]:.2f}" for f, v in REP["R9"]["tim"].items())
      + f"; LCDM timing (h47's halo convention) {REP['R9']['tim_K'][0]:.2f} +- {REP['R9']['tim_K'][1]:.2f}", True, load_bearing=False)
# R10 LambdaCDM's halos as NFW under timing
RQ = np.geomspace(10.0, 4000.0, 36)
Menc5 = nfw_enclosed(halo_mass(M1[m5])[:, None], RG[None, :]) + nfw_enclosed(halo_mass(M2[m5])[:, None], RG[None, :])
v2q = gen_timing(Menc5, RG, RQ)
r10, w10 = prior(rp[m5])
v2p = np.full(r10.shape, np.nan)
for i_ in range(len(r10)):
    okq = np.isfinite(v2q[i_])
    if okq.sum() >= 2:
        v2p[i_] = np.interp(np.log(r10[i_]), np.log(RQ[okq]), v2q[i_, okq], left=np.nan, right=np.nan)
REP["R10"] = fitA(m5, sig_from(v2p, r10, w10, rp[m5]))
check("R10 (reported) LambdaCDM's halos as NFW (h48b's enclosed-mass model) under the same timing argument",
      f"A = {fmt(REP['R10'])} ({REP['R10']['excl']} pairs without a bound configuration)", True, load_bearing=False)

# ================================================================================================ reading
R.banner("READING")
A3 = [H3[f]["A"] for f in FOOTS]
if all(0.80 <= a_ <= 1.25 for a_ in A3):
    reading = ("B1 is not a failure of B's law as such: it was one only under circular orbits, which the data reject for both laws (H2). "
               "Under the law's own timing orbits B gives the pair speeds; " + ("LambdaCDM's halos under the same orbits over-predict (H5). " if H5["A"] < 0.80 else
               "and LambdaCDM's halos under the same orbits do not over-predict (H5 failed). ") +
               "Which orbits apply is B's to specify: timing orbits if B's dark density exerts no dynamical friction on the pair (T5's identity "
               "read literally), virialised orbits if its cold component acts as a free medium, and then B1 stands at H1's level.")
elif all(a_ < 0.80 for a_ in A3):
    reading = ("the two orbit models bracket the data for B (circular too slow, timing too fast): B1 is orbit-degenerate, not an established "
               "failure.")
elif all(a_ > 1.25 for a_ in A3):
    reading = "B1 stands under both orbit models."
else:
    reading = "mixed across the footings: " + ", ".join(f"{f} {H3[f]['A']:.2f}" for f in FOOTS)
P(f"    READING (declared): {reading}")
P(f"    profile under timing (H4): {'predicted' if abs(zT) < 2 else 'NOT predicted'} (inner - outer {zT:+.1f} sigma)")
P(f"    the Local Group under the same timing (R6, canonical): {REP['R6']['canonical']['ratio']:.2f}x the measured approach speed")

R.num("C1", dict(computed={k: list(v) for k, v in C1.items()}, committed=com, n=int(m5.sum())))
R.num("C2", dict(eB=eB, eK=eK, e_ode=e_ode, e_bb=e_bb, e_shoot=e_sh, e_gen=e_gen, lg=lg_rows, rho_ta_B=TAB_B["rta"], rho_ta_K=TAB_K["rta"],
                 lam=LAM, t0_gyr=T0 * C.UNIT_GYR))
R.num("C3", dict(mocks=[list(a_) for a_ in Amock], mean=mA))
R.num("H1", dict(fits=H1, boost_dex=float(boost)))
R.num("profile", dict(edges=[float(q1), float(q2)], tertiles=PROF, z_circ_B=zB, z_circ_L=zL, z_tim_B=zT, z_tim_B_alt=zTa))
R.num("H3", H3); R.num("H5", H5); R.num("reported", REP); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
