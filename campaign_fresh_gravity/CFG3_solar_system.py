#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG3_solar_system -- THE SOLAR SYSTEM UNDER THE PRINCIPLE: Cassini's quadrupole, the phantom mass inside Saturn's orbit and the
planets' sunward anomaly, with the answer coherent only above l* (both filters), both footings.

WHY THE SUN IS ANSWERED AT ALL.  The Sun sits inside the Galaxy's held-back region (the gate is open), and the Galaxy's field at
the Sun is internal to that region, so it enters the kernel's argument in full (CFG3_principle D7): the Solar System sees
QUMOND with the Bose kernel in the Galactic field -- exactly the setting in which the strict law fails Cassini by ~6x (FP14 X5,
FP17, f29 V1).  FP17's theorem says (a0, Lambda, G, c) cannot supply the separating length; the principle's (v) does: the
answer is a coarse-grained property of the vacuum state, coherent only above l*, the state's Airy length at a0,
l_A = (hbar^2/(2 m^2 a0))^(1/3) (CFG3_principle D8), TIED to the dark field's mass m (floor 1.9-5.2e-19 eV, FP10):
l* = 1.25-2.60 pc.  Putting the coarse-graining S in the action filters both the source and the answer (D3).

MACHINERY.  f29's phantom-density quadrature (hunt_2026/f29_coherence_length_law.py: QUMOND with nu_RAR -- the Bose kernel --
on a Gaussian-smoothed Sun in the uniform Newtonian Galactic field, axisymmetric log-r x theta grid; its interior quadrupole
in the record's frozen convention Q2 = 3 G I2; its enclosed monopole), exec'd read-only.  f29 filters the SOURCE only.  This
lane adds the OUTPUT filter: the phantom density's l = 0 and l = 2 Legendre parts are convolved with the same 3-D Gaussian,
K_l(r, r') = 4 pi (2 pi s^2)^(-3/2) exp(-(r - r')^2/2s^2) [e^-z i_l(z)], z = r r'/s^2 (the exact radial kernel of an isotropic
Gaussian acting on r^l-type harmonics).  Gates (the record's): Q2 < 5.2e-27 s^-2 (Park 2026 2-sigma ceiling, FP1/f29); extra
mass inside Saturn's orbit < 6.7e-11 Msun (Pitjev & Pitjeva 2013 via f29 S4); sunward anomaly at 1 AU < 3.66e-14 m/s^2 (FP1).

CHECKS
  K1 CONTROL: f29's committed table is reproduced by its own functions at its own footings (hunt_lib's 9.36e-11 / 1.13e-10):
     Q2/ceiling at xi = 0.03 / 0.05 / 0.10 pc (1.1239, 0.2330, 0.0289 canonical; 1.3238, 0.2731, 0.0339 alt) and the Saturn
     monopole ratio (3.405, 0.735, 0.092 canonical) to their printed digits.
  K2 CONTROL: the output-filter kernel is exact on an analytic case: a Gaussian blob of width s1 (l = 0) smoothed by s2 is the
     Gaussian of width sqrt(s1^2 + s2^2), and an l = 2 Gaussian-weighted harmonic r^2 exp(-r^2/2 s1^2) P2 maps to the analytic
     result; both to < 1e-3 on the lane's grids.
  S1 [HEADLINE; load-bearing; MUTATE must fail] AT THE TIE (l* = l_A at m = 1.9e-19 and 5.2e-19 eV, both footings) the Sun clears
     all three gates with both filters: Q2/ceiling < 1, monopole/bound < 1, sunward anomaly/bound < 1.
  S2 (reported) THE FLOOR: the smallest l* clearing all three gates, double filter and source-only (f29's 0.045 pc), both
     footings; through the tie it is an UPPER bound on the dark field's mass: m <= m_max with l_A(m_max) = the floor.
  S3 (reported) the record's other length: ONE_NEW_THING's 0.032 pc (hbar c/2e-22 eV) under the double filter.
PRE-DECLARED HYPOTHESES (written before the first run of this script):
  H1 at the tie every gate is cleared by >= 4 orders of magnitude (f29's xi^-3 law from 0.03 pc to ~1.3 pc).  EXPECT TRUE.
  H2 the output filter LOWERS the floor below f29's source-only 0.045 pc (it spreads the phantom further).  EXPECT TRUE,
     size uncertain (a floor between 0.025 and 0.045 pc expected).
  H3 ONE_NEW_THING's 0.032 pc passes Q2 but not the monopole under the source-only filter (f29's table) and may pass both
     with the double filter.  UNCERTAIN.
MUTATE=1: the coherence length removed (l* -> 0: the answer read and written pointwise) -- S1 must FAIL (the strict law's Q2 is
~6x the ceiling), rc = 1.
Run from the repository root (MUTATE first):  MUTATE=1 python3 campaign_fresh_gravity/CFG3_solar_system.py; python3 campaign_fresh_gravity/CFG3_solar_system.py
"""
import os, sys, math, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG3_common as C
import numpy as np
from scipy.special import ive, spherical_in
from scipy.optimize import brentq

R = C.Run("CFG3_solar_system", __doc__)
P, check = R.P, R.check
if C.MUTATE:
    P("\n  *** MUTATE=1: the coherence length is removed (l* -> 0): S1 must FAIL ***")

sys.path.insert(0, C.HUNT)
F29P = os.path.join(C.HUNT, "f29_coherence_length_law.py")
ns, _ = C.exec_slices(F29P, [(None, 'P("=" * 118); P("f29')], name="f29_ro")
phantom, quadrupole, enclosed, solve_eN = ns["phantom"], ns["quadrupole"], ns["enclosed"], ns["solve_eN"]
A0_HL, GEXT_OBS, Q2_CEIL, G29 = ns["A0"], ns["GEXT_OBS"], ns["Q2_CEIL"], ns["G"]
PCm, MS29 = ns["PC"], 1.98892e30
AU = 1.495978707e11
R_SAT = 9.54 * AU
M_BOUND = 1.1e-17 * 4 / 3 * math.pi * R_SAT ** 3
SUN_BOUND = 3.66e-14                                                     # FP1's EARTH_BOUND (the alpha = 1 ephemeris gate, 2 sigma)
GM_SUN = G29 * MS29


def grid_limits(w, rM):
    return min(1e-4 * rM, 1e-3 * w, 0.1 * R_SAT), max(1e4 * rM, 1e3 * w)


# ================================================================================================ K1
R.banner("K1  CONTROL: f29's committed Solar-System table, from its own functions")
ref_q = {"canonical": {0.03: 1.1239, 0.05: 0.2330, 0.10: 0.0289}, "alt": {0.03: 1.3238, 0.05: 0.2731, 0.10: 0.0339}}
ref_m = {0.03: 3.405, 0.05: 0.735, 0.10: 0.092}
dq, dm = 0.0, 0.0
for foot in C.FOOTS:
    a0 = A0_HL[foot]; eN = solve_eN(GEXT_OBS / a0) * a0; rM = math.sqrt(GM_SUN / a0)
    for xi, qv in ref_q[foot].items():
        r, th, rho = phantom(MS29, xi * PCm, eN, a0, *grid_limits(xi * PCm, rM))
        q_now = abs(quadrupole(r, th, rho)) / Q2_CEIL
        dq = max(dq, abs(round(q_now, 4) - qv))
        if foot == "canonical":
            a0c = A0_HL["canonical"]; eNc = solve_eN(GEXT_OBS / a0c) * a0c; rMc = math.sqrt(GM_SUN / a0c)
            r2, th2, rho2 = phantom(MS29, xi * PCm, eNc, a0c, min(1e-4 * rMc, 1e-3 * xi * PCm, 0.1 * R_SAT), max(1e4 * rMc, 1e3 * xi * PCm))
            m_now = enclosed(r2, th2, rho2, R_SAT) / M_BOUND
            dm = max(dm, abs(round(m_now, 3) - ref_m[xi]))
        P(f"    {foot:9s} xi = {xi:.2f} pc: Q2/ceiling {q_now:.4f} (f29 {qv})" + (f"; monopole/bound {m_now:.3f} (f29 {ref_m[xi]})" if foot == "canonical" else ""))
check("K1 CONTROL: f29's phantom quadrature (exec'd read-only) reproduces its committed Q2/ceiling (canonical and alt) and Saturn-monopole "
      "ratios at xi = 0.03 / 0.05 / 0.10 pc to their printed digits", f"max |d(Q2/ceil)| {dq:.1e}; max |d(monopole ratio)| {dm:.1e}",
      dq <= 1.5e-4 and dm <= 1.5e-3)


# ================================================================================================ the output filter
def lkernel(l, r, s):
    """K_l(r_i, r'_j) r'_j^2 dr'_j on the log grid r (trapezoid weights), for an isotropic 3-D Gaussian of width s."""
    ri, rj = r[:, None], r[None, :]
    z = ri * rj / s ** 2
    with np.errstate(over="ignore", invalid="ignore"):
        small = z < 30.0
        ez = np.where(small, spherical_in(l, np.minimum(z, 30.0)) * np.exp(-np.minimum(z, 30.0)),
                      np.sqrt(math.pi / (2 * np.maximum(z, 1e-300))) * ive(l + 0.5, np.maximum(z, 1e-300)))
    K = 4 * math.pi * (2 * math.pi * s * s) ** (-1.5) * np.exp(-(ri - rj) ** 2 / (2 * s * s)) * ez
    lr = np.log(r)
    wt = np.zeros_like(r); d = np.diff(lr)
    wt[:-1] += 0.5 * d; wt[1:] += 0.5 * d
    return K * (rj ** 3) * wt[None, :]                                  # r'^2 dr' = r'^3 dln r'


def legendre_parts(r, th, rho):
    ct = np.cos(th); st = np.sin(th)
    P2 = 0.5 * (3 * ct ** 2 - 1)
    rho0 = 0.5 * C._trap(rho * st[None, :], th, axis=1)
    rho2 = 2.5 * C._trap(rho * (P2 * st)[None, :], th, axis=1)
    return rho0, rho2


def gates(r, th, rho, s_out):
    """(Q2, monopole inside Saturn, sunward acceleration at 1 AU) with the output filter of width s_out (0 = none)."""
    if s_out > 0:
        rho0, rho2 = legendre_parts(r, th, rho)
        rho0 = lkernel(0, r, s_out) @ rho0
        rho2 = lkernel(2, r, s_out) @ rho2
        q2 = 3 * G29 * 2 * math.pi * (2 / 5) * C._trap(rho2 / r, r)
        mcum = np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * r[1:] ** 2 * rho0[1:] + 4 * math.pi * r[:-1] ** 2 * rho0[:-1]) * np.diff(r))])
        m_sat = float(np.interp(R_SAT, r, mcum)); m_au = float(np.interp(AU, r, mcum))
    else:
        q2 = quadrupole(r, th, rho); m_sat = enclosed(r, th, rho, R_SAT); m_au = enclosed(r, th, rho, AU)
    return abs(q2), m_sat, G29 * abs(m_au) / AU ** 2


# ================================================================================================ K2
R.banner("K2  CONTROL: the output-filter kernel against analytic Gaussian convolutions")
rt = np.geomspace(1e-4, 50.0, 1400); s1, s2 = 1.0, 0.7
g0 = np.exp(-rt ** 2 / (2 * s1 ** 2)) / (2 * math.pi * s1 ** 2) ** 1.5
s12 = math.sqrt(s1 ** 2 + s2 ** 2)
g0_ex = np.exp(-rt ** 2 / (2 * s12 ** 2)) / (2 * math.pi * s12 ** 2) ** 1.5
g0_num = lkernel(0, rt, s2) @ g0
e0 = float(np.max(np.abs(g0_num - g0_ex)) / g0_ex.max())
# l = 2: f(x) = (3 z^2 - r^2)/2 exp(-r^2/2 s1^2) = r^2 P2 exp(...): Gaussian convolution of a harmonic polynomial times a Gaussian
f2 = rt ** 2 * np.exp(-rt ** 2 / (2 * s1 ** 2))
f2_ex = (s1 ** 2 / s12 ** 2) ** 1.5 * (s1 ** 2 / s12 ** 2) ** 2 * rt ** 2 * np.exp(-rt ** 2 / (2 * s12 ** 2))
f2_num = lkernel(2, rt, s2) @ f2
e2 = float(np.max(np.abs(f2_num - f2_ex)) / f2_ex.max())
P(f"    l = 0 Gaussian: max rel error {e0:.1e};  l = 2 harmonic Gaussian: max rel error {e2:.1e}")
check("K2 CONTROL: the output-filter kernel is exact on analytic convolutions (l = 0: Gaussian -> wider Gaussian; l = 2: r^2 P2 e^(-r^2/2s1^2) "
      "-> (s1/s12)^7 r^2 P2 e^(-r^2/2s12^2))", f"l = 0 {e0:.1e}; l = 2 {e2:.1e}", e0 < 1e-3 and e2 < 1e-3)

# ================================================================================================ S1-S3
R.banner("S1  THE SUN UNDER THE PRINCIPLE: both filters, the FP0 footings")
TIE = json.load(open(os.path.join(C.HERE, "CFG3_principle_results.json")))["numbers"]["D8"]["l_A_pc"] if os.path.exists(
    os.path.join(C.HERE, "CFG3_principle_results.json")) else None
LA = {}
for mk, mv in (("1.9e-19", 1.9e-19), ("5.2e-19", 5.2e-19)):
    mkg = mv * C.EV / C.C_SI ** 2
    for f in C.FOOTS:
        LA[f"{mk}|{f}"] = (C.HBAR ** 2 / (2 * mkg ** 2 * C.A0[f])) ** (1 / 3) / C.PC
if TIE:
    P("    l_A from CFG3_principle D8 (committed): " + "; ".join(f"{k}: {v:.3f} pc" for k, v in TIE.items()))
XI_GRID = [0.02, 0.025, 0.03, 0.032, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.1, 0.2, 0.5, 1.0, 3.0]
ROWS = {}
for foot in C.FOOTS:
    a0 = C.A0[foot]; eN = solve_eN(GEXT_OBS / a0) * a0; rM = math.sqrt(GM_SUN / a0)
    rows = []
    grid = sorted(set(XI_GRID + [LA[f"1.9e-19|{foot}"], LA[f"5.2e-19|{foot}"]]))
    for xi in grid:
        w = xi * C.PC
        if C.MUTATE:
            w = 1e-3 * rM                                               # l* -> 0: f29's point-mass limit, no output filter
        r, th, rho = phantom(MS29, w, eN, a0, *grid_limits(w, rM))
        qs, ms, as_ = gates(r, th, rho, 0.0)                          # source filter only (f29's law)
        qd, md, ad = (qs, ms, as_) if C.MUTATE else gates(r, th, rho, w)  # source + output filter (the principle)
        rows.append(dict(l=xi, q_src=qs / Q2_CEIL, m_src=ms / M_BOUND, a_src=as_ / SUN_BOUND, q=qd / Q2_CEIL, m=md / M_BOUND, a=ad / SUN_BOUND))
    ROWS[foot] = rows
    P(f"    {foot}: e_N = {eN:.3e} m/s^2 ({eN / a0:.3f} a0), r_M(Sun) = {rM / C.PC:.4f} pc")
    P(f"      {'l* [pc]':>8s} {'Q2/ceil':>10s} {'M(<Sat)/bnd':>12s} {'a(1AU)/bnd':>11s} | source-only: {'Q2/ceil':>9s} {'M/bnd':>9s}")
    for rw in rows:
        P(f"      {rw['l']:8.4f} {rw['q']:10.3e} {rw['m']:12.3e} {rw['a']:11.3e} |              {rw['q_src']:9.3e} {rw['m_src']:9.3e}")
R.num("S1_rows", ROWS)


def at(foot, xi):
    for rw in ROWS[foot]:
        if abs(rw["l"] - xi) < 1e-12:
            return rw
    raise KeyError


tie_rows = {f"{mk}|{f}": at(f, LA[f"{mk}|{f}"]) for mk in ("1.9e-19", "5.2e-19") for f in C.FOOTS}
worst = max(max(v["q"], v["m"], v["a"]) for v in tie_rows.values())
check("S1 [HEADLINE; MUTATE must fail] AT THE TIE the Sun clears Cassini's quadrupole, the ephemeris mass bound inside Saturn's orbit and the "
      "sunward-anomaly bound, with both filters, at both dark-field mass floors and both footings (l* = l_A = 1.25-2.60 pc)",
      "; ".join(f"{k}: l* {LA[k]:.3f} pc, Q2 {v['q']:.1e}, M {v['m']:.1e}, a {v['a']:.1e}" for k, v in tie_rows.items()) + f"; worst {worst:.1e}",
      worst < 1.0)
R.num("S1_tie", dict(l_A=LA, rows=tie_rows, worst=worst))


def floor_of(foot, key_q, key_m, key_a):
    rows = ROWS[foot]
    ok = [max(rw[key_q], rw[key_m], rw[key_a]) < 1.0 for rw in rows]
    for i in range(1, len(rows)):
        if (not ok[i - 1]) and ok[i] and all(ok[i:]):
            y0 = math.log(max(rows[i - 1][key_q], rows[i - 1][key_m], rows[i - 1][key_a]))
            y1 = math.log(max(rows[i][key_q], rows[i][key_m], rows[i][key_a]))
            return math.exp(np.interp(0.0, [y1, y0], [math.log(rows[i]["l"]), math.log(rows[i - 1]["l"])]))
    return rows[0]["l"] if all(ok) else float("nan")


FL = {f: dict(double=floor_of(f, "q", "m", "a"), source_only=floor_of(f, "q_src", "m_src", "a_src")) for f in C.FOOTS}
MMAX = {}
for f in C.FOOTS:
    fl = FL[f]["double"]
    if math.isfinite(fl):
        MMAX[f] = math.sqrt(C.HBAR ** 2 / (2 * C.A0[f] * (fl * C.PC) ** 3)) * C.C_SI ** 2 / C.EV
P("    floors (all three gates): " + "; ".join(f"{f}: double filter {FL[f]['double']:.4f} pc, source only {FL[f]['source_only']:.4f} pc" for f in C.FOOTS))
P("    through the tie l_A(m) >= floor:  m <= " + "; ".join(f"{f}: {v:.2e} eV" for f, v in MMAX.items()))
check("S2 (H2, reported) THE FLOOR: the output filter lowers the Solar-System floor below the source-only one (f29: 0.045 pc); through the tie "
      "the floor is an upper bound on the dark field's mass", "; ".join(f"{f}: {FL[f]['double']:.4f} vs {FL[f]['source_only']:.4f} pc, m <= "
                                                                        f"{MMAX.get(f, float('nan')):.2e} eV" for f in C.FOOTS),
      all(FL[f]["double"] < FL[f]["source_only"] for f in C.FOOTS), load_bearing=False)
R.num("S2", dict(floors_pc=FL, m_max_eV=MMAX))
one = {f: at(f, 0.032) for f in C.FOOTS}
check("S3 (H3, reported) ONE_NEW_THING's 0.032 pc (hbar c/2e-22 eV) under the double filter: all three gates", "; ".join(
    f"{f}: Q2 {v['q']:.2f}, M {v['m']:.2f}, a {v['a']:.2e} (source-only Q2 {v['q_src']:.2f}, M {v['m_src']:.2f})" for f, v in one.items()),
      all(max(v["q"], v["m"], v["a"]) < 1 for v in one.values()), load_bearing=False)
R.num("S3", one)

R.banner("W  THE LEDGER")
R.ledger("SS1", "PASS" if worst < 1 else "FAIL", f"at the tie (l* = l_A(m_floor) = 1.25-2.60 pc) the Sun clears every gate, worst ratio {worst:.1e}", "S1")
R.ledger("SS2", "TIED", "l* = l_A = (hbar^2/(2 m^2 a0))^(1/3); the Solar System bounds it from below: l* >= " +
         " / ".join(f"{FL[f]['double']:.3f}" for f in C.FOOTS) + " pc => m <= " + " / ".join(f"{MMAX.get(f, float('nan')):.1e}" for f in C.FOOTS) + " eV", "S2")
sys.exit(R.finish())
