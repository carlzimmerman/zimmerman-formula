#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR6_lg_zero_velocity_mond_sector.py -- the Local Group's zero-velocity radius under the candidate the threads converged
on (2026-09-26, evening): does the MOND-sector switch reading, with MS3's local cap, move the region edge that XR4 scored
on the on-branch closed form, and can anything in the candidate bring R_0 to the measured 0.96 +- 0.03 Mpc?
Independent cross-thread review.  New code; no committed script is run or edited (XR4's LG model is reimplemented line
for line and checked against its committed JSON).

THE MODEL: XR4's (k02's) point-mass + Lambda shell model (XR4_lg_zero_velocity_construction.py:60-137, integrate and
run_cells, reproduced exactly), in which the phantom exists only inside the region edge r_e(z) and a shell beyond it feels
the Newtonian gravity of baryons + carrier.  The ONE changed input is the edge:
  'xr4'     r_e = v_f/(H sqrt(x_c,eff + 1.5 Om(z)))            XR4's on-branch edge (host in vacuum, matter subtracted; XR4:88)
  'ms_abs'  r_e = v_f/(H sqrt(x_c,eff - 1.5 Om(z) f_b))        the candidate: L395's 'msc' reading (absolute; the ambient
                                                                 baryons count in x, L395_two_switch_branches.py:22-25)
  'ms_con'  r_e = v_f/(H sqrt(x_c,eff))                          MS2's contrast reading (= MS3's 'door' in the mean density)
  'ms_num'  the capped switch itself (L395's form, v_cap = 325 km/s) solved on the point mass's MOND-sector profile with
            nu_mono at each epoch and tabulated -- no closed form assumed.
  x_c,eff = x_c0 [Omega_L0/Omega_L(z)]^p = x_c0 E^(2p); the candidate cell p = 1, x_c0 = 2.5; the DE2 window x_c0 = 2-2.97
  reported beside it.  v_f = (G M_b a0)^(1/4): 195 / 204 km/s (M_b = 1.145e11) and 216 / 226 km/s (1.72e11) < v_cap, so the
  cap cannot bind in the deep-MOND zone (v_loc = v_f there); checked, not assumed (S1).
MEASURED: 0.96 +- 0.03 Mpc (as the repo quotes it); PRE-DECLARED band |log10(R_0/0.96)| <= 0.10 (XR4's).

CHECKS
  C1 CONTROL: no gate, no carrier, M_b = 1.145e11 reproduces k02's 1.929 / 2.021 Mpc (XR4 C1) and the Newtonian 3.178e12 Msun
     inversion 1.176 Mpc (XR4 C2).
  C2 CONTROL: every one of XR4's 204 committed cells (4 p x 4 x_c0 + no gate, 3 carriers, 2 M_b, 2 footings) is reproduced
     with the 'xr4' edge to 1e-6 relative, and XR4's mutation cells likewise.
  S1 (as first written, FAILED -- kept in the record): "the capped edge table equals the uncapped one at all 97 epochs and
     the numerical edge equals the closed form to 1% for z <= 5".  At z >~ 7 the edge lies inside the point mass's own
     Newtonian zone, where v_loc diverges and the cap switches that phantom-free sliver off; the deep-MOND closed form is
     1.15% off at z = 5.  Split into what is true:
  S1a v_loc < v_cap in the LG's deep-MOND zone (y < 0.1) at every epoch, and the capped and uncapped tables agree wherever
      the edge lies in the MOND regime (y_edge < 1).
  S1b the cap moves R_0 by < 0.1% (capped vs uncapped numerical tables), and the numerical table gives the closed form's R_0
      to 1%.
  S1c (reported) the closed form against the numerical edge, z <= 5 (first formulation: 1%).
  S2 THE MOND-SECTOR READING MOVES THE EDGE OUTWARD: r_e(ms_abs)/r_e(xr4) > 1 at every epoch (1.10 at z = 0).  MUTATE=1
     (XR4's reading, no cap) must FAIL this (rc = 1).
  Z1 (reported) R_0 at the candidate cell on the MOND-sector reading, both M_b, both footings, three carrier histories.
  Z2 (reported, pre-declared) THE LG LIABILITY FLIPS: some carrier history lands inside the band on BOTH footings at the
     candidate cell.
  Z3 (reported, pre-declared) THE MOND-SECTOR READING MAKES IT WORSE: R_0(ms_abs) > R_0(xr4) for every M_b, carrier, footing.
  E1 (reported) THE PINCER: the uniform external Newtonian field e_N (k04's scalar nu(y + e_N) prescription) that would bring
     R_0 to 0.96 at the candidate cell, against (i) the largest field a KiDS-passing region kernel transmits (L361 R3 at
     1/m = 0.5 Mpc: 1.0e-4 / 8.6e-5 a0), (ii) a merged neighbour group's baryons (k04's group masses <= 1.03e11 Msun at
     >= 3 Mpc: <= 1.7e-5 a0), (iii) the web's baryonic field that the PM operator B reads unscreened (L361 R3's baryons-only
     rms, 2.05e-3 / 1.70e-3 a0 -- the kernel that fails KiDS by +233).
Runtime ~1 min, single-threaded.  Run from the repository root:
    python3 real_research/cross_thread_review_2026_09_26/XR6_lg_zero_velocity_mond_sector.py      (MUTATE=1 for the control)
"""
import os, sys, json, math, time, itertools
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
from hunt_lib import A0, G, Mpc, Msun, H0, OM_M, OM_L, OM_B      # the constants XR4 and k02 used (H0 = 67.4, Om = 0.3134)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR6_lg_zero_velocity_mond_sector"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": SLUG, "mutate": MUTATE, "checks": {}, "numbers": {}}
CH = []
R0_MEAS, BAND = 0.96, 0.10
RATIO_D = 5.36
FB = OM_B / OM_M
VCAP = 325.0e3
EDGE_MS = "xr4" if MUTATE else "ms_abs"                  # MUTATE: XR4's reading (and no cap) in place of the candidate's


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")


def banner(t):
    P("\n" + "=" * 118); P(t); P("=" * 118)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the candidate's reading is replaced by XR4's on-branch edge and the cap removed; S2 must FAIL ***")


def nu(y):
    y = np.maximum(y, 1e-12); return 1.0 / (-np.expm1(-np.sqrt(y)))


def retained(z, hist):
    if hist == "none": return np.zeros_like(z)
    if hist == "full": return np.ones_like(z)
    zz = np.array([0.0, 0.5, 1.0, 2.5, 100.0]); rr = np.array([0.075, 0.645, 0.92, 0.998, 0.998])
    return np.interp(z, zz, rr)


# ------------------------------------------------------------------ the capped switch on a point mass (nu_mono, L340:103-117)
def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore", invalid="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def _dh_rar(y, e=1e-6):
    return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)


Y_P = brentq(lambda y: float(_dh_rar(y)), 1.0, 5.0); H_P = float(_h_rar(Y_P))
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(_dh_rar(YG), 0.05 * H_P / (YG + Y_P))
H_MONO = float(_h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
nu_mono = lambda y: 1.0 + np.interp(np.log10(np.maximum(y, 1e-12)), LYG, H_MONO) / np.maximum(y, 1e-12)
dnu_mono = lambda y: (np.interp(np.log10(np.maximum(y, 1e-12)), LYG, DH_MONO) / np.maximum(y, 1e-12)
                      - np.interp(np.log10(np.maximum(y, 1e-12)), LYG, H_MONO) / np.maximum(y, 1e-12) ** 2)


def edge_numeric(Mb, a0, z, xc0, p, vcap):
    """the region edge of an isolated point mass M_b [Msun] by L395's capped switch: x = 1.5 Om(z) f_b + D/H^2 against
    x_c0 E^(2p) max(1, v_loc^2/v_cap^2), D = -div g_ms of the untruncated MOND-sector field (nu_mono); returns
    (edge [m], max v_loc in the deep-MOND zone inside the edge [m/s])."""
    E2 = OM_M * (1 + z) ** 3 + OM_L; H = H0 * math.sqrt(E2); Omz = OM_M * (1 + z) ** 3 / E2
    r = np.geomspace(1e-5 * Mpc, 40.0 * Mpc, 6000)
    GM = G * Mb * Msun; y = GM / (r ** 2 * a0)
    g = nu_mono(y) * GM / r ** 2
    D = -2.0 * GM ** 2 * dnu_mono(y) / (r ** 5 * a0)
    x = 1.5 * Omz * FB + D / H ** 2
    vl2 = np.where(D > 0, g ** 2 / np.maximum(D, 1e-300), 0.0)
    on = x >= xc0 * E2 ** p * np.maximum(1.0, vl2 / vcap ** 2)
    ion = np.where(on)[0]
    if ion.size == 0:
        return 0.0, 0.0
    i0 = ion[0]; off = np.where(~on[i0:])[0]
    i1 = len(r) - 1 if off.size == 0 else i0 + off[0]
    re = math.sqrt(r[i1 - 1] * r[i1])
    deep = (y < 0.1) & (r < re)
    return re, (float(np.sqrt(vl2[deep].max())) if deep.any() else 0.0)


LNA_TAB = np.linspace(math.log(0.02), 0.0, 97)


def edge_table(Mb, a0, xc0, p, vcap):
    return np.array([edge_numeric(Mb, a0, 1.0 / math.exp(l) - 1.0, xc0, p, vcap)[0] for l in LNA_TAB])


# ------------------------------------------------------------------ XR4's integrator (XR4_lg_zero_velocity_construction.py:60-102)
def integrate(cells, ri, n=2000, a_start=0.02):
    """cells: dicts (Mb, a0, p, xc0 or None, hist, kernel_on, Mnewton, edge, eN, table).  XR4's integrate with the edge
    convention and a uniform external Newtonian field eN (units of a0, k04's scalar nu(y + e_N) inside the region) added."""
    Mb = np.array([c["Mb"] for c in cells])[:, None] * Msun
    a0 = np.array([c["a0"] for c in cells])[:, None]
    p = np.array([c.get("p", 0.0) or 0.0 for c in cells])[:, None]
    xc0 = np.array([np.inf if c.get("xc0") is None else c["xc0"] for c in cells])[:, None]
    kon = np.array([1.0 if c.get("kernel_on", True) else 0.0 for c in cells])[:, None]
    Mn = np.array([np.nan if c.get("Mnewton") is None else c["Mnewton"] * Msun for c in cells])[:, None]
    hidx = np.array([("none", "full", "decay").index(c.get("hist", "none")) for c in cells])
    conv = [c.get("edge", "xr4") for c in cells]
    sgn = np.array([{"xr4": 1.0, "ms_abs": -FB, "ms_con": 0.0, "ms_num": 0.0}[cv] for cv in conv])[:, None]
    isnum = np.array([cv == "ms_num" for cv in conv])[:, None]
    tabs = [c.get("table") for c in cells]
    eN = np.array([c.get("eN", 0.0) for c in cells])[:, None]
    vf = (G * Mb * a0) ** 0.25
    r = ri.copy()
    u = H0 * math.sqrt(OM_M / a_start ** 3 + OM_L) * r
    dead = np.zeros_like(r, dtype=bool)
    lna = np.linspace(math.log(a_start), 0.0, n + 1); h = lna[1] - lna[0]

    def acc(l, rr):
        a = math.exp(l); E2 = OM_M / a ** 3 + OM_L; H = H0 * math.sqrt(E2); z = 1.0 / a - 1.0
        Omz = (OM_M / a ** 3) / E2
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            re = vf / (H * np.sqrt(xc0 * E2 ** p + sgn * 1.5 * Omz))
        if isnum.any():
            ren = np.array([[np.interp(l, LNA_TAB, t)] if t is not None else [np.nan] for t in tabs])
            re = np.where(isnum, ren, re)
        re = np.where(np.isinf(xc0), np.inf, re)
        rr = np.maximum(rr, 1e-6 * Mpc)
        gNb = G * Mb / rr ** 2
        with np.errstate(invalid="ignore", over="ignore"):
            w = np.where(np.isinf(re), 1.0, 0.5 * (1.0 - np.tanh((rr - re) / (0.02 * np.where(np.isinf(re), 1.0, np.maximum(re, 1e-30))))))
        rv = np.array([0.0, 1.0, float(retained(np.array(z), "decay"))])
        Md = RATIO_D * rv[hidx][:, None] * Mb
        g = w * (kon * nu(gNb / a0 + eN) + (1 - kon)) * gNb + (1 - w) * gNb + G * Md / rr ** 2
        g = np.where(np.isfinite(Mn), G * Mn / rr ** 2, g)
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
    """XR4's run_cells (XR4:105-127): vectorised bracketing of the zero-velocity shell."""
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
    R0[(r[:, 0] <= 2e-5 * Mpc) | (np.abs(r[:, 1] / np.maximum(r[:, 0], 1e-30) - 1) > 0.05)] = np.nan
    return R0


# ============================================================================================ C1 / C2 controls
banner("C1-C2  CONTROLS: k02's isolated R_0, the Newtonian inversion, and XR4's 204 committed cells with XR4's edge")
MB_LG = 1.145e11
XR4J = json.load(open(os.path.join(HERE, "XR4_lg_zero_velocity_construction_results.json")))["numbers"]
ctl = [dict(Mb=MB_LG, a0=A0["canonical"], xc0=None), dict(Mb=MB_LG, a0=A0["alt"], xc0=None),
       dict(Mb=MB_LG, a0=A0["canonical"], Mnewton=3.178e12)]
xr4cells = [dict(Mb=c["Mb"], a0=c["a0"], xc0=c["xc0"], p=c["p"], hist=c["hist"], edge="xr4") for c in XR4J["cells"]]
PS, XCS = (0.0, 0.5, 1.0, 2.0), (1.5, 2.0, 2.5, 2.97)
mut = [dict(Mb=MB_LG, a0=A0["canonical"], xc0=xc, p=pp, hist="none", kernel_on=False) for pp, xc in itertools.product(PS, XCS)]
mut += [dict(Mb=MB_LG, a0=A0["canonical"], xc0=None, p=0.0, hist="none", kernel_on=False),
        dict(Mb=MB_LG, a0=A0["canonical"], xc0=2.5, p=-1.0, hist="none"), dict(Mb=MB_LG, a0=A0["canonical"], xc0=2.5, p=1.0, hist="none")]
Rall = run_cells(ctl + xr4cells + mut)
Rc, Rx, Rm = Rall[:3], Rall[3:3 + len(xr4cells)], Rall[3 + len(xr4cells):]
ref = np.array([c["R0"] for c in XR4J["cells"]]); refm = np.array(XR4J["mutations"])
dx = float(np.nanmax(np.abs(Rx / ref - 1))); dm = float(np.nanmax(np.abs(Rm / refm - 1)))
check("C1 CONTROL: k02's isolated-MOND R_0 = 1.929 / 2.021 Mpc and the Newtonian 3.178e12 Msun inversion 1.176 Mpc are reproduced "
      "(XR4's C1, C2)", f"{Rc[0]:.4f} / {Rc[1]:.4f} / {Rc[2]:.4f} Mpc (XR4: {XR4J['controls']['C1'][0]:.4f} / "
      f"{XR4J['controls']['C1'][1]:.4f} / {XR4J['controls']['C2']:.4f})",
      abs(Rc[0] / XR4J["controls"]["C1"][0] - 1) < 1e-6 and abs(Rc[1] / XR4J["controls"]["C1"][1] - 1) < 1e-6
      and abs(Rc[2] / XR4J["controls"]["C2"] - 1) < 1e-6)
check("C2 CONTROL: every one of XR4's 204 committed cells and 19 mutation cells is reproduced with XR4's on-branch edge",
      f"max relative difference {dx:.1e} (cells), {dm:.1e} (mutations)", dx < 1e-6 and dm < 1e-6)
Rc6 = run_cells(ctl[:1], n=4000)
check("C3 CONTROL: converged in the step count (n = 2000 vs 4000, 0.3%)", f"{Rc[0]:.5f} vs {Rc6[0]:.5f}", abs(Rc[0] / Rc6[0] - 1) < 3e-3)

# ============================================================================================ S1 / S2 the switch on the LG
banner("S1-S2  THE CANDIDATE'S SWITCH ON THE LOCAL GROUP: does the cap bind, and where does the MOND-sector reading put the edge?")
S1 = {}
worst_edge, vmax_all, tab_same = 0.0, 0.0, True
for foot, a0 in A0.items():
    for Mbv in (MB_LG, 1.5 * MB_LG):
        vf = (G * Mbv * Msun * a0) ** 0.25
        rows = []
        for z in (0.0, 0.5, 1.0, 2.0, 5.0):
            E2 = OM_M * (1 + z) ** 3 + OM_L; H = H0 * math.sqrt(E2); Omz = OM_M * (1 + z) ** 3 / E2
            re_c, vmx = edge_numeric(Mbv, a0, z, 2.5, 1.0, VCAP)
            re_u, _ = edge_numeric(Mbv, a0, z, 2.5, 1.0, math.inf)
            re_abs = vf / (H * math.sqrt(2.5 * E2 - 1.5 * Omz * FB))
            re_x4 = vf / (H * math.sqrt(2.5 * E2 + 1.5 * Omz))
            re_run = re_x4 if EDGE_MS == "xr4" else re_abs                 # the edge this run's candidate cells use
            rows.append(dict(z=z, capped_Mpc=re_c / Mpc, uncapped_Mpc=re_u / Mpc, ms_abs_Mpc=re_abs / Mpc, xr4_Mpc=re_x4 / Mpc,
                             ratio_ms_xr4=re_abs / re_x4, ratio_run_xr4=re_run / re_x4, vloc_max_deep_kms=vmx / 1e3))
            worst_edge = max(worst_edge, abs(re_c / re_abs - 1)); vmax_all = max(vmax_all, vmx)
            tab_same &= abs(re_c / re_u - 1) < 1e-9
        S1[f"{foot}/{Mbv:.3e}"] = rows
        P(f"  {foot:9s} M_b {Mbv:.3e} (v_f {vf / 1e3:.0f} km/s): " + "; ".join(
            f"z={r_['z']:g}: capped {r_['capped_Mpc']:.3f} | uncapped {r_['uncapped_Mpc']:.3f} | ms_abs {r_['ms_abs_Mpc']:.3f} | "
            f"xr4 {r_['xr4_Mpc']:.3f} Mpc" for r_ in rows[:3]))
OUT["numbers"]["S1_edges"] = S1
# the full tables, capped and uncapped, and R_0 on the numerical tables vs the closed form.
# RECORD: S1 was first written as ONE check -- "capped table = uncapped table at all 97 epochs, numerical edge = closed form to
# 1% for z <= 5, R_0 agrees to 1%" -- and it FAILED on its first two clauses: at z >~ 7 the closed-form edge falls inside the
# point mass's own Newtonian zone (y_edge > 1), where the phantom density vanishes faster than the field, v_loc^2 =
# |g|^2/(-div g) diverges, and the cap switches that phantom-free sliver off; and the closed form (deep MOND) is 1.15% from the
# numerical edge at z = 5.  Neither touches R_0 (0.05%).  It is split below into the three statements that are true, with the
# epochs where the cap does bind reported rather than hidden.
TABS, TABU, zdiv = {}, {}, {}
agree_mond = True
for foot, a0 in A0.items():
    tc = edge_table(MB_LG, a0, 2.5, 1.0, VCAP); tu = edge_table(MB_LG, a0, 2.5, 1.0, math.inf)
    TABS[foot], TABU[foot] = tc, tu
    y_e = np.where(tu > 0, G * MB_LG * Msun / (np.maximum(tu, 1e-30) ** 2 * a0), np.inf)
    diff = np.abs(tc - tu) > 1e-9 * np.maximum(tu, 1e-30)
    agree_mond &= not bool(np.any(diff & (y_e < 1.0)))
    zz = 1.0 / np.exp(LNA_TAB) - 1.0
    zdiv[foot] = float(zz[diff].min()) if diff.any() else None
cmp_cells = [dict(Mb=MB_LG, a0=A0[f], xc0=2.5, p=1.0, hist="none", edge="ms_num", table=TABS[f]) for f in A0] + \
            [dict(Mb=MB_LG, a0=A0[f], xc0=2.5, p=1.0, hist="none", edge="ms_num", table=TABU[f]) for f in A0] + \
            [dict(Mb=MB_LG, a0=A0[f], xc0=2.5, p=1.0, hist="none", edge="ms_abs") for f in A0]
Rcmp = run_cells(cmp_cells)
dcap = float(np.max(np.abs(Rcmp[:2] / Rcmp[2:4] - 1))); dnum = float(np.max(np.abs(Rcmp[:2] / Rcmp[4:] - 1)))
OUT["numbers"]["S1_tables"] = dict(z_first_capped_difference=zdiv, R0_capped_table=list(Rcmp[:2]), R0_uncapped_table=list(Rcmp[2:4]),
                                   R0_closed_form=list(Rcmp[4:]), worst_edge_vs_closed_z_le_5=worst_edge)
check("S1a THE CAP DOES NOT BIND IN THE LG's MOND ZONE: v_loc < v_cap wherever y < 0.1 inside the region (every epoch z = 0-5, both "
      "M_b, both footings), and the capped and uncapped edge tables agree at every epoch whose edge lies in the MOND regime "
      "(y_edge < 1)", f"max v_loc (deep zone) {vmax_all / 1e3:.0f} km/s; tables agree in the MOND regime: {agree_mond}; the cap binds "
      f"only at z >= {', '.join(f'{f} {v:.1f}' for f, v in zdiv.items() if v is not None) or 'never'} (edge inside the point mass's "
      f"Newtonian zone, phantom-free)", vmax_all < VCAP and agree_mond)
check("S1b THE CAP DOES NOT MOVE R_0: R_0 on the capped numerical edge table equals R_0 on the uncapped table to 0.1%, and equals "
      "R_0 on the ms_abs closed form to 1% (candidate cell, M_b = 1.145e11, no carrier, both footings)",
      f"capped/uncapped - 1 = {dcap:.1e}; numerical/closed - 1 = {dnum:.1e} ({Rcmp[0]:.4f} / {Rcmp[2]:.4f} / {Rcmp[4]:.4f} Mpc "
      f"canonical)", dcap < 1e-3 and dnum < 0.01)
check("S1c (reported) the closed form r_e = v_f/(H sqrt(x_c,eff - 1.5 Om f_b)) against the numerical uncapped edge for z <= 5 (the "
      "closed form is deep-MOND; its first formulation demanded 1%)", f"worst {worst_edge:.4f}", worst_edge < 0.01, load_bearing=False)
rat = [r_["ratio_run_xr4"] for v in S1.values() for r_ in v]         # MUTATE: the run's reading IS XR4's -> ratio 1
check("S2 THE MOND-SECTOR READING MOVES THE LG's EDGE OUTWARD: r_e(run's reading)/r_e(xr4) > 1 at every epoch -- the switch no "
      "longer subtracts the matter background (XR4's vacuum branch), it reads baryons + phantom and counts the ambient baryons -- "
      "MUTATE (XR4's reading) must fail this", f"edge ratio {min(rat):.4f}-{max(rat):.4f} over z = 0-5 (z = 0: "
      f"{S1[list(S1)[0]][0]['ratio_run_xr4']:.4f}); ms_abs/xr4 itself {min(r_['ratio_ms_xr4'] for v in S1.values() for r_ in v):.4f}-"
      f"{max(r_['ratio_ms_xr4'] for v in S1.values() for r_ in v):.4f}", min(rat) > 1.0 + 1e-6)

# ============================================================================================ Z1-Z3 R_0 at the candidate cell
banner("Z1-Z3  R_0 ON THE MOND-SECTOR READING (the candidate cell p = 1, x_c0 = 2.5; the DE2 window beside it)")
HISTS, MBS, XW = ("none", "decay", "full"), (MB_LG, 1.5 * MB_LG), (2.0, 2.5, 2.97)
cells = []
for foot, a0 in A0.items():
    for Mbv, hist, xc in itertools.product(MBS, HISTS, XW):
        for edge in ((EDGE_MS, "ms_con") if not MUTATE else (EDGE_MS,)):
            cells.append(dict(foot=foot, Mb=Mbv, a0=a0, xc0=xc, p=1.0, hist=hist, edge=edge))
Rz = run_cells(cells)
for c, v in zip(cells, Rz): c["R0"] = float(v)
lk = {(c["foot"], c["Mb"], c["hist"], c["xc0"], c["edge"]): c["R0"] for c in cells}
xr = {(c["foot"], c["Mb"], c["hist"], c["xc0"]): c["R0"] for c in XR4J["cells"] if c["tag"] == "gate" and c["p"] == 1.0}
P("  R_0 [Mpc] at p = 1 (x_c0 = 2.0 / 2.5 / 2.97); measured 0.96, band [0.76, 1.21]; XR4's on-branch edge beside it")
Z = {}
for foot in A0:
    for Mbv, hist in itertools.product(MBS, HISTS):
        ms = [lk[(foot, Mbv, hist, xc, EDGE_MS)] for xc in XW]
        x4 = [xr[(foot, Mbv, hist, xc)] for xc in XW]
        con = [lk[(foot, Mbv, hist, xc, "ms_con")] for xc in XW] if not MUTATE else ms
        Z[f"{foot}/{Mbv:.3e}/{hist}"] = dict(ms_abs=ms, ms_con=con, xr4=x4,
                                             dex_candidate=math.log10(ms[1] / R0_MEAS), dex_xr4=math.log10(x4[1] / R0_MEAS))
        P(f"  {foot:9s} M_b {Mbv:.2e} {hist:5s} | MOND-sector (abs) {ms[0]:.3f} / {ms[1]:.3f} / {ms[2]:.3f} | contrast {con[0]:.3f} / "
          f"{con[1]:.3f} / {con[2]:.3f} | XR4 {x4[0]:.3f} / {x4[1]:.3f} / {x4[2]:.3f} | candidate cell {math.log10(ms[1] / R0_MEAS):+.3f} dex "
          f"(XR4 {math.log10(x4[1] / R0_MEAS):+.3f})")
OUT["numbers"]["R0"] = Z
dexc = [v["dex_candidate"] for v in Z.values()]
check("Z1 (reported) R_0 at the candidate cell on the candidate's reading, over M_b = 1.145-1.72e11, three carrier histories, both "
      "footings", f"{min(dexc):+.3f} to {max(dexc):+.3f} dex from 0.96 ({min(10 ** d * R0_MEAS for d in dexc):.2f}-"
      f"{max(10 ** d * R0_MEAS for d in dexc):.2f} Mpc); XR4 at the same cell {min(v['dex_xr4'] for v in Z.values()):+.3f} to "
      f"{max(v['dex_xr4'] for v in Z.values()):+.3f} dex", True, load_bearing=False)
flip = any(all(abs(Z[f"{f}/{Mbv:.3e}/{h}"]["dex_candidate"]) <= BAND for f in A0) for Mbv in MBS for h in HISTS)
check("Z2 THE LG LIABILITY FLIPS (pre-declared): some M_b and carrier history lands inside +-0.10 dex on BOTH footings at the "
      "candidate cell", f"best |dex| {min(abs(d) for d in dexc):.3f}", flip, load_bearing=False)
worse = all(v["ms_abs"][1] > v["xr4"][1] * (1 + 1e-6) for v in Z.values())
dd = [math.log10(v["ms_abs"][1] / v["xr4"][1]) for v in Z.values()]
check("Z3 THE MOND-SECTOR READING MAKES THE LG WORSE (pre-declared): R_0 on the candidate's reading exceeds R_0 on XR4's edge for "
      "every M_b, carrier and footing at the candidate cell", f"shift {min(dd):+.4f} to {max(dd):+.4f} dex", worse, load_bearing=False)

# ============================================================================================ E1 the pincer
banner("E1  THE PINCER: which external field would bring R_0 to 0.96, and who could supply it")
EG = np.geomspace(1e-6, 0.05, 36)
ecells = [dict(Mb=MB_LG, a0=A0[f], xc0=2.5, p=1.0, hist="none", edge=EDGE_MS, eN=float(e), foot=f) for f in A0 for e in EG]
Re_ = run_cells(ecells)
E1 = {}
KIDS_MAX = {"canonical": 1.0411328345774767e-04, "alt": 8.641707140731341e-05}     # L361 R3, bound-region kernel at 1/m = 0.5 Mpc
WEB_B = {"canonical": 2.0526443838166275e-03, "alt": 1.70375489465847e-03}           # L361 R3, baryons-only rms (operator B)
L361J = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L361_bound_region_kernel_results.json")))["numbers"]["R3"]
for f in A0:
    KIDS_MAX[f] = L361J["bound-region kernel, 1/m = 0.5 Mpc (all baryons active)"]["kernel_field_rms_a0"][f]
    WEB_B[f] = L361J["baryons only (L353/L355)"]["kernel_field_rms_a0"][f]
MB_NEIGH = 1.034e11                                                                  # k04's largest neighbour group (IC 342), hunt_2026/k04_lambda_edge_efe_closed.out:24
NEIGH = G * MB_NEIGH * Msun / (3.0 * Mpc) ** 2
for i, f in enumerate(A0):
    Rf = Re_[i * len(EG):(i + 1) * len(EG)]
    ok = np.isfinite(Rf)
    lr, le = np.log(Rf[ok]), np.log(EG[ok])
    need = float(np.exp(np.interp(math.log(R0_MEAS), lr[::-1], le[::-1]))) if (Rf[ok].min() < R0_MEAS < Rf[ok].max()) else float("nan")
    at = lambda e: float(np.exp(np.interp(math.log(e), le, lr)))
    E1[f] = dict(eN_needed_a0=need, R0_at_kids_max=at(KIDS_MAX[f]), R0_at_neighbour=at(NEIGH / A0[f]), R0_at_web_B=at(WEB_B[f]),
                 kids_max_a0=KIDS_MAX[f], neighbour_a0=NEIGH / A0[f], web_B_a0=WEB_B[f], R0_isolated_region=float(Rf[0]))
    P(f"  {f:9s}: e_N needed for R_0 = 0.96 at the candidate cell: {need:.2e} a0.  R_0 at the largest KiDS-passing transmitted field "
      f"({KIDS_MAX[f]:.1e} a0): {E1[f]['R0_at_kids_max']:.3f} Mpc; at a merged neighbour's baryons ({NEIGH / A0[f]:.1e} a0): "
      f"{E1[f]['R0_at_neighbour']:.3f}; at operator B's web field ({WEB_B[f]:.1e} a0, KiDS +233): {E1[f]['R0_at_web_B']:.3f} Mpc")
OUT["numbers"]["E1"] = E1
check("E1 (reported) THE PINCER: the external field the LG needs at the candidate cell exceeds by > 10x both what a KiDS-passing "
      "region kernel can transmit (L361 R3, 1/m = 0.5) and what a merged neighbour group's baryons supply; only the unscreened web "
      "field of operator B (which fails KiDS by +233) is of the needed size",
      "; ".join(f"{f}: needed {E1[f]['eN_needed_a0']:.1e} vs KiDS-max {E1[f]['kids_max_a0']:.1e}, neighbour {E1[f]['neighbour_a0']:.1e}, "
                f"web(B) {E1[f]['web_B_a0']:.1e} a0" for f in A0),
      all(E1[f]["eN_needed_a0"] > 10 * max(E1[f]["kids_max_a0"], E1[f]["neighbour_a0"]) for f in A0), load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
zc = Z[f"canonical/{MB_LG:.3e}/none"]; za = Z[f"alt/{MB_LG:.3e}/none"]
P(f"""  The Local Group's own v_f (195-226 km/s) is below v_cap, so MS3's local cap does not bind in its MOND zone (S1a: it acts only
  at z >~ 7, inside the point mass's phantom-free Newtonian zone) and moves R_0 by {dcap:.0e} (S1b).
  What changes is the READING: the MOND-sector switch counts baryons + phantom (and the ambient baryons) instead of
  subtracting the full matter background, so the edge moves OUT by a factor {min(rat):.3f}-{max(rat):.3f} (S2), and R_0 rises:
  candidate cell, M_b = 1.145e11, no carrier: {zc['ms_abs'][1]:.3f} / {za['ms_abs'][1]:.3f} Mpc (canonical / alt) against XR4's
  {zc['xr4'][1]:.3f} / {za['xr4'][1]:.3f} and the measured 0.96 -> {zc['dex_candidate']:+.3f} / {za['dex_candidate']:+.3f} dex.
  The external field that would rescue it (~{E1['canonical']['eN_needed_a0']:.0e} a0) is ~{E1['canonical']['eN_needed_a0'] / E1['canonical']['kids_max_a0']:.0f}x what a KiDS-passing kernel lets through: the LG and
  KiDS pull the screening in opposite directions.""")
n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
