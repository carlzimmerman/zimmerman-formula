#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR4_lg_zero_velocity_construction.py -- the Local Group's zero-velocity radius R_0 under the assembled construction
(L359 vacuum-gated switch + L361 bound-region kernel + a carrier), against the measured R_0.  Cross-thread review,
2026-09-26.  New code; no committed script is run or edited.

WHY.  The 09-03 hunt found that isolated deep MOND on the Local Group's baryons over-predicts its zero-velocity radius
~2x (hunt_2026/k02_lambda_edge_zvs.out: 1.929 / 2.021 Mpc vs 1.176 measured by that pipeline; 0.96 +- 0.03 published),
and that the only rescue was the EXTERNAL field of Virgo + the Local Volume (k04, k07e) or the LG's own CMB-frame field
(k_dimensional_turnaround_groups: -0.094 dex).  L361's kernel SCREENS every field from outside a bound region (R1:
9.5e-5 through a 2 Mpc gap), so that rescue is not available to the construction.  But the construction adds two things
k02 never had: (a) the phantom exists only inside the region edge, r_e(z) = v_f/(H(z) sqrt(x_c0 E^(2p) + 1.5 Om(z)))
(DE1's closed form of L352's edge law), which was SMALLER in the past; beyond it a shell feels Newtonian gravity of
baryons + carrier only (Gauss, L352 Z1); (b) the carrier's Newtonian pull.  Which way the net goes is not obvious, so it
is computed.

MODEL (k02's point-mass + Lambda shell model, the standard Lynden-Bell/Sandage/Chernin reading used for LG masses):
   r'' = -[ w(r,t) nu(g_Nb/a0) g_Nb + (1 - w) g_Nb + G M_d(t)/r^2 ] + Omega_L H0^2 r,   g_Nb = G M_b/r^2,
   w = smooth step (1 inside r_e(t), 0 outside, width 2% of r_e);  shells start on the Hubble flow at a = 0.02.
   R_0 = today's radius of the shell whose radial velocity is zero today.
   Carrier: M_d(z) = 5.36 M_b x retained(z); histories: none; full (a CDM-like halo kept); Lambda-triggered decay using
   GP5's retained fractions (0.998 at z = 2.5, 0.92 at z = 1, 0.645 at z = 0.5) and f_d(0) = 0.925 (retained 0.075).
   The carrier is placed inside the shell (a point mass): an UPPER bound on its effect.
MEASURED: 0.96 +- 0.03 Mpc (Karachentsev+2009, as the repo quotes it); repo pipelines 0.906 (k_dimensional, the one
   stable group, MC recovery 0.065 dex) and 1.176 +- 0.106 (k02).  PRE-DECLARED agreement band: |log10(R_0/0.96)| <= 0.10.

CHECKS
  C1 CONTROL: no gate, no carrier, M_b = 1.145e11 reproduces k02's 1.929 / 2.021 Mpc (1.5%).
  C2 CONTROL: Newtonian point mass 3.178e12 Msun reproduces k02's inversion (R_0 = 1.176 Mpc, 1.5%).
  C3 CONTROL: step convergence (n = 2000 vs 4000) on C1 within 0.3%.
  M1 MUTATION: kernel off inside the region (nu = 1) -> the gate cannot matter: every gate cell equals the ungated value.
  M2 MUTATION: reverse the gate (p = -1, edge larger in the past): R_0 must rise above the p = +1 value, toward the
     ungated one.
  Z1 (reported) R_0 over gate cells p in {0, 0.5, 1, 2} x x_c0 in {1.5, 2, 2.5, 2.97} x carrier x M_b x footing.
  Z2 THE VERDICT FOR THE DE2 WINDOW (the linear gate p = 1, x_c0 in [2, 2.97], the gate the record now carries):
     PASS if some carrier history lands inside the band on BOTH footings.  Reported whichever way it falls.
Runtime: ~10-60 s.  Writes XR4_lg_zero_velocity_construction_results.json.
Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR4_lg_zero_velocity_construction.py
"""
import os, sys, json, math, time, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
from hunt_lib import A0, G, Mpc, Msun, H0, OM_M, OM_L   # the constants k02 used (H0 = 67.4, Om = 0.3134)

T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "XR4_lg_zero_velocity_construction", "checks": {}, "numbers": {}}
CH = []
R0_MEAS, BAND = 0.96, 0.10
RATIO_D = 5.36                                  # Omega_c/Omega_b


def check(name, ok, measured):
    ok = bool(ok); CH.append((name, ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


def nu(y):
    y = np.maximum(y, 1e-12); return 1.0 / (-np.expm1(-np.sqrt(y)))


def retained(z, hist):
    if hist == "none": return np.zeros_like(z)
    if hist == "full": return np.ones_like(z)
    zz = np.array([0.0, 0.5, 1.0, 2.5, 100.0]); rr = np.array([0.075, 0.645, 0.92, 0.998, 0.998])
    return np.interp(z, zz, rr)


def integrate(cells, ri, n=2000, a_start=0.02):
    """cells: list of dicts (Mb, a0, p, xc0 or None for no gate, hist, kernel_on, Mnewton or None).
    ri: (ncell, K) initial PHYSICAL radii [m] at a_start, on the Hubble flow (k02's convention).  Returns r, u today."""
    nc = len(cells)
    Mb = np.array([c["Mb"] for c in cells])[:, None] * Msun
    a0 = np.array([c["a0"] for c in cells])[:, None]
    p = np.array([c.get("p", 0.0) or 0.0 for c in cells])[:, None]
    xc0 = np.array([np.inf if c.get("xc0") is None else c["xc0"] for c in cells])[:, None]
    kon = np.array([1.0 if c.get("kernel_on", True) else 0.0 for c in cells])[:, None]
    Mn = np.array([np.nan if c.get("Mnewton") is None else c["Mnewton"] * Msun for c in cells])[:, None]
    hidx = np.array([("none", "full", "decay").index(c.get("hist", "none")) for c in cells])
    vf = (G * Mb * a0) ** 0.25
    r = ri.copy()
    u = H0 * math.sqrt(OM_M / a_start ** 3 + OM_L) * r
    dead = np.zeros_like(r, dtype=bool)
    lna = np.linspace(math.log(a_start), 0.0, n + 1); h = lna[1] - lna[0]

    def acc(l, rr):
        a = math.exp(l); E2 = OM_M / a ** 3 + OM_L; H = H0 * math.sqrt(E2); z = 1.0 / a - 1.0
        Omz = (OM_M / a ** 3) / E2
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            re = vf / (H * np.sqrt(xc0 * E2 ** p + 1.5 * Omz))           # DE1 closed form incl. the mean-density term
        re = np.where(np.isinf(xc0), np.inf, re)
        rr = np.maximum(rr, 1e-6 * Mpc)
        gNb = G * Mb / rr ** 2
        with np.errstate(invalid="ignore", over="ignore"):
            w = np.where(np.isinf(re), 1.0, 0.5 * (1.0 - np.tanh((rr - re) / (0.02 * np.where(np.isinf(re), 1.0, re)))))
        rv = np.array([0.0, 1.0, float(retained(np.array(z), "decay"))])
        Md = RATIO_D * rv[hidx][:, None] * Mb
        g = w * (kon * nu(gNb / a0) + (1 - kon)) * gNb + (1 - w) * gNb + G * Md / rr ** 2
        g = np.where(np.isfinite(Mn), G * Mn / rr ** 2, g)                 # Newtonian point-mass control cells
        return -g + OM_L * H0 ** 2 * rr, H

    for i in range(n):
        l = lna[i]
        a1, H1 = acc(l, r);                 k1r, k1u = u / H1, a1 / H1
        a2, H2 = acc(l + h / 2, r + h * k1r / 2); k2r, k2u = (u + h * k1u / 2) / H2, a2 / H2
        a3, H3 = acc(l + h / 2, r + h * k2r / 2); k3r, k3u = (u + h * k2u / 2) / H3, a3 / H3
        a4, H4 = acc(l + h, r + h * k3r);   k4r, k4u = (u + h * k3u) / H4, a4 / H4
        r = r + h * (k1r + 2 * k2r + 2 * k3r + k4r) / 6
        u = u + h * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        dead |= r <= 1e-5 * Mpc
        r = np.where(dead, 1e-5 * Mpc, r); u = np.where(dead, -1.0, u)
    return r, u


def run_cells(cells, n=2000, K=24, iters=6):
    """R_0 [Mpc] per cell by vectorised iterative bracketing on the initial radius (k02 bisects; the map r_i -> r(today)
    is extremely steep at the zero-velocity shell, so a fixed grid cannot resolve it).  Each pass integrates K shells per
    cell inside the current bracket and keeps the outermost interval where u changes sign from - to +."""
    nc = len(cells)
    lo = np.full(nc, math.log(0.001 * Mpc)); hi = np.full(nc, math.log(30.0 * Mpc))
    ok = np.ones(nc, dtype=bool)
    for _ in range(iters):
        x = lo[:, None] + (hi - lo)[:, None] * np.linspace(0.0, 1.0, K)[None, :]
        r, u = integrate(cells, np.exp(x), n=n)
        for k in range(nc):
            s = np.sign(u[k]); idx = np.where((s[:-1] < 0) & (s[1:] > 0))[0]
            if len(idx) == 0:
                ok[k] = False; continue
            j = idx[-1]; lo[k], hi[k] = x[k, j], x[k, j + 1]
    r, u = integrate(cells, np.exp(np.stack([lo, hi], axis=1)), n=n)
    f = -u[:, 0] / (u[:, 1] - u[:, 0])
    R0 = (r[:, 0] + f * (r[:, 1] - r[:, 0])) / Mpc
    R0[~ok] = np.nan
    # a resolved bracket has both shells near the zero-velocity surface today (neither collapsed nor far out)
    R0[(r[:, 0] <= 2e-5 * Mpc) | (np.abs(r[:, 1] / np.maximum(r[:, 0], 1e-30) - 1) > 0.05)] = np.nan
    return R0


# ---------------------------------------------------------------------------------------------------- controls
MB_LG = 1.145e11
ctl = [dict(Mb=MB_LG, a0=A0["canonical"], xc0=None), dict(Mb=MB_LG, a0=A0["alt"], xc0=None),
       dict(Mb=MB_LG, a0=A0["canonical"], Mnewton=3.178e12)]
Rc = run_cells(ctl)
Rc6 = run_cells(ctl[:1], n=4000)
check("C1 CONTROL: no gate, no carrier, M_b = 1.145e11 reproduces k02's isolated-MOND R_0 = 1.929 / 2.021 Mpc (1.5%)",
      abs(Rc[0] / 1.929 - 1) < 0.015 and abs(Rc[1] / 2.021 - 1) < 0.015, f"{Rc[0]:.3f} / {Rc[1]:.3f} Mpc")
check("C2 CONTROL: a Newtonian point mass of 3.178e12 Msun reproduces k02's inversion (R_0 = 1.176 Mpc, 1.5%)",
      abs(Rc[2] / 1.176 - 1) < 0.015, f"{Rc[2]:.3f} Mpc")
check("C3 CONTROL: converged in the step count (n = 2000 vs 4000, 0.3%)", abs(Rc[0] / Rc6[0] - 1) < 3e-3,
      f"{Rc[0]:.4f} vs {Rc6[0]:.4f}")

# ---------------------------------------------------------------------------------------------------- the scan
PS, XCS, HISTS, MBS = (0.0, 0.5, 1.0, 2.0), (1.5, 2.0, 2.5, 2.97), ("none", "decay", "full"), (MB_LG, 1.5 * MB_LG)
cells = []
for foot, a0 in A0.items():
    for Mbv, hist in itertools.product(MBS, HISTS):
        cells.append(dict(foot=foot, Mb=Mbv, a0=a0, xc0=None, p=0.0, hist=hist, tag="nogate"))
        for pp, xc in itertools.product(PS, XCS):
            cells.append(dict(foot=foot, Mb=Mbv, a0=a0, xc0=xc, p=pp, hist=hist, tag="gate"))
# mutations M1 (kernel off inside the region) and M2 (edge pushed out)
mut = []
for pp, xc in itertools.product(PS, XCS):
    mut.append(dict(foot="canonical", Mb=MB_LG, a0=A0["canonical"], xc0=xc, p=pp, hist="none", kernel_on=False))
mut.append(dict(foot="canonical", Mb=MB_LG, a0=A0["canonical"], xc0=None, p=0.0, hist="none", kernel_on=False))
mut.append(dict(foot="canonical", Mb=MB_LG, a0=A0["canonical"], xc0=2.5, p=-1.0, hist="none"))   # reversed gate
mut.append(dict(foot="canonical", Mb=MB_LG, a0=A0["canonical"], xc0=2.5, p=1.0, hist="none"))
R = run_cells(cells + mut)
Rs, Rm = R[:len(cells)], R[len(cells):]
for c, v in zip(cells, Rs): c["R0"] = float(v)
check("M1 MUTATION: with the kernel off inside the region the gate cannot matter (all 16 gate cells = the ungated Newtonian-"
      "baryon value)", np.nanmax(np.abs(Rm[:16] / Rm[16] - 1)) < 1e-6,
      f"Newtonian-baryon R_0 = {Rm[16]:.3f} Mpc; max relative spread {np.nanmax(np.abs(Rm[:16] / Rm[16] - 1)):.1e}")
check("M2 MUTATION: reversing the gate's time dependence (p = -1: the edge LARGER in the past) must move R_0 back toward "
      "the isolated-MOND value, i.e. above the p = +1 value and at most the ungated one",
      (Rm[17] > Rm[18]) and (Rm[17] <= Rc[0] * 1.01),
      f"R_0(p = -1) = {Rm[17]:.3f}, R_0(p = +1) = {Rm[18]:.3f}, ungated {Rc[0]:.3f} Mpc (x_c0 = 2.5, no carrier)")

P("\n  R_0 [Mpc] (measured 0.96; band |dex| <= 0.10 -> [0.76, 1.21]); rows: M_b, carrier; columns: gate cell")
for foot in A0:
    for Mbv, hist in itertools.product(MBS, HISTS):
        sub = [c for c in cells if c["foot"] == foot and c["Mb"] == Mbv and c["hist"] == hist]
        ng = [c for c in sub if c["tag"] == "nogate"][0]["R0"]
        line = f"  {foot:9s} M_b {Mbv:.2e} {hist:5s} | no gate {ng:5.2f} |"
        for pp in PS:
            line += f" p={pp:g}: " + " ".join(f"{c['R0']:4.2f}" for c in sub if c["tag"] == "gate" and c["p"] == pp) + " |"
        P(line)
P("  (within each p block the four numbers are x_c0 = 1.5, 2.0, 2.5, 2.97)")

inband = lambda v: np.isfinite(v) and abs(math.log10(v / R0_MEAS)) <= BAND
win = [c for c in cells if c["tag"] == "gate" and c["p"] == 1.0 and 2.0 <= c["xc0"] <= 2.97]
ok_hist = {}
for hist in HISTS:
    ok_hist[hist] = all(any(inband(c["R0"]) for c in win if c["hist"] == hist and c["foot"] == f) for f in A0)
dexs = {h: [math.log10(c["R0"] / R0_MEAS) for c in win if c["hist"] == h and np.isfinite(c["R0"])] for h in HISTS}
check("Z2 THE DE2 WINDOW (p = 1, x_c0 = 2-2.97): some carrier history puts the LG zero-velocity radius inside the measured band "
      "on BOTH footings",
      any(ok_hist.values()),
      "; ".join(f"{h}: dex {min(v):+.2f}..{max(v):+.2f}" for h, v in dexs.items() if v))

# mass scaling in one representative cell (the slope is the 1/4-vs-1/3 discriminator k02 named)
ms = [dict(foot="canonical", Mb=m, a0=A0["canonical"], xc0=2.5, p=1.0, hist="none") for m in (3e10, 1e11, 3e11)] + \
     [dict(foot="canonical", Mb=m, a0=A0["canonical"], xc0=None, p=0.0, hist="none") for m in (3e10, 1e11, 3e11)]
Rms = run_cells(ms)
sl_g = np.polyfit(np.log10([3e10, 1e11, 3e11]), np.log10(Rms[:3]), 1)[0]
sl_n = np.polyfit(np.log10([3e10, 1e11, 3e11]), np.log10(Rms[3:]), 1)[0]
P(f"\n  mass scaling, canonical, no carrier: d log R_0/d log M_b = {sl_g:.3f} (gate p = 1, x_c0 = 2.5) vs {sl_n:.3f} (no gate)")
OUT["numbers"] = dict(controls=dict(C1=[float(Rc[0]), float(Rc[1])], C2=float(Rc[2]), C3=float(Rc6[0])),
                      mutations=[float(v) for v in Rm], cells=[{k: (float(v) if isinstance(v, (float, np.floating)) else v)
                                                              for k, v in c.items()} for c in cells],
                      window_dex=dexs, mass_slope=dict(gate=float(sl_g), nogate=float(sl_n)))
nf = sum(1 for _, ok in CH if not ok)
OUT["n_checks"], OUT["n_fail"] = len(CH), nf
json.dump(OUT, open(os.path.join(HERE, "XR4_lg_zero_velocity_construction_results.json"), "w"), indent=1, default=float)
P(f"\n  {len(CH) - nf}/{len(CH)} checks pass  [{time.time() - T0:.0f}s]")
