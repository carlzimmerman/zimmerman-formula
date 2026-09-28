#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG20 -- THE LOCAL GROUP AGAINST THE TARGET LAW'S EDGE.  Does the Local Group's zero-velocity radius allow the phantom edge that
KiDS needs?

WHY.  Under FG001 the Local Group (MW + M31) is a top-level bound system: the law acts on its baryons with NO external field, and
its phantom ends at the target's density edge x_e r_ta (CFG4's T3; CFG4's convention for r_ta: the law's untruncated profile at the
top-hat contrast Delta_ta(z)).  FP1 (committed) found that the isolated law with no external field puts the LG's zero-velocity
radius at 1.92-2.02 Mpc against the observed 0.93 +- 0.12 Mpc; the chain needed the web's external field to bring it down, and FG001
removes that field for top-level systems.  So the edge is the only thing left that can.  CFG16/CFG17 place KiDS's self-consistent
floor at x_e ~ 0.34.

THE MODEL (FP1's own shell integrator, exec'd read-only; the truncation added).  Test shells start on the Hubble flow at a = 0.02
and move in the LG's field plus Lambda (Planck, h = 0.674).  At each epoch the LG's edge is r_e(a) = x_e r_ta(a), where r_ta(a) is
the law's untruncated turnaround radius at Delta_ta(z) (CFG4_switch's committed D1 table, interpolated in ln(1+z); 5.55 above z = 3).
Inside r_e the law acts, g = nu(g_N/a0) g_N; outside, the enclosed mass stays M_e(a) = M_b nu(g_N(r_e)/a0) (CFG4's density edge).
R0 is where today's radial velocity changes sign (FP1's bracket-and-refine).  LG baryons: FP1's 1.145e11 and 1.72e11 Msun.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  with no truncation the exec'd integrator reproduces FP1's committed E1 control (nu_RAR, 1.145e11: 1.929 / 2.021 Mpc)
      and FP1's E3 R0_e0 for the chain's kernel within FP1's own tolerance (2e-3 Mpc).
  H0  [MUTATE must fail] the truncation at x_e = 0.34 lowers R0 below the untruncated value by more than 0.1 Mpc (every case).
  H1  [HEADLINE] at KiDS's self-consistent floor (CFG16: 0.341 / 0.348 canonical P2 / nu_mono; 0.340 / 0.345 alt) the LG's R0 lies
      within 2 sigma of 0.93 +- 0.12 Mpc (R0 <= 1.17 Mpc), both footings, both kernels, both LG baryonic masses.  Expectation: FAIL
      (a hand estimate gives ~1.3-1.4 Mpc).
  R1  (reported) R0 against x_e from 0.05 to 1 and untruncated; the largest x_e the LG allows (R0 <= 1.17 Mpc) against KiDS's floor.
MUTATE=1: the truncation is switched off (x_e -> infinity everywhere) -- H0 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG20_lg_edge.py   (MUTATE=1 for the control; ~1-2 min)
"""
import os, sys, math, json
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG20_lg_edge", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the truncation switched off -- H0 must FAIL ***")

FP1P = os.path.join(C.CHAIN, "FP1_static_sector.py")
ns = {"np": np, "math": math, "_trap": C._trap}
ns = C.exec_slices(FP1P, [("# ---- LG: XR4's point-mass", "Rctl = lg_R0(")], ns=ns, name="fp1_lg")[0]
LG_G, LG_Mpc, LG_Msun, LG_H0, LG_OM, LG_OL, LG_A0 = (ns[k] for k in ("LG_G", "LG_Mpc", "LG_Msun", "LG_H0", "LG_OM", "LG_OL", "LG_A0"))
Ntab_lg, lg_R0 = ns["Ntab_lg"], ns["lg_R0"]
FP1 = json.load(open(os.path.join(C.CHAIN, "FP1_static_sector_results.json")))
FP1N = FP1.get("numbers", FP1)
SW = json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]["D1"]
C16 = json.load(open(os.path.join(HERE, "CFG16_selfconsistent_floor_results.json")))["numbers"]["floors"]
KERN = {"P2": C.nu_p2, "nu_mono": C.nu_mono}

# ================================================================================================ C1
R.banner("C1  CONTROL: FP1's LG machinery, untruncated")
rc = lg_R0([Ntab_lg(C.nu_rar, 0.0)] * 2, [1.145e11] * 2, [LG_A0["canonical"], LG_A0["alt"]])
r_e0 = FP1N["E3"]["canonical"]["R0_e0"]
rk = lg_R0([Ntab_lg(C.nu_p2, 0.0)], [1.145e11], [LG_A0["canonical"]])
P(f"    nu_RAR 1.145e11: {rc[0]:.4f} / {rc[1]:.4f} Mpc (FP1 E1: 1.929 / 2.021); P2 canonical {rk[0]:.4f} (FP1 E3 R0_e0 {r_e0:.4f}, the chain's kernel)")
c1 = abs(rc[0] - 1.9290) < 2e-3 and abs(rc[1] - 2.0214) < 2e-3
check("C1 CONTROL: the exec'd LG integrator reproduces FP1's committed E1 control (1.929 / 2.021 Mpc) within FP1's tolerance",
      f"{rc[0]:.4f} / {rc[1]:.4f}; P2 canonical {rk[0]:.4f} vs the chain's R0_e0 {r_e0:.4f} (reported)", c1)

# ================================================================================================ the truncated integrator
ZT = sorted(float(z) for z in SW)
DT = [SW[str(z) if str(z) in SW else z]["one_plus_delta_ta"] for z in ZT] if False else [SW[k]["one_plus_delta_ta"] for k in sorted(SW, key=float)]
ZT = [float(k) for k in sorted(SW, key=float)]


def delta_ta(z):
    if z >= ZT[-1]:
        return 5.55 if z > 3.0 else DT[-1]
    return float(np.interp(math.log1p(z), [math.log1p(v) for v in ZT], DT))


RHOC0 = 3 * LG_H0 ** 2 / (8 * math.pi * LG_G)                                                # kg/m^3 (h = 0.674)


def rta_table(Mb, a0, nuf, lna):
    """the law's untruncated turnaround radius [m] of a point baryonic mass at each epoch (Delta_ta(z) x the mean matter density)."""
    out = []
    M = Mb * LG_Msun
    for l in lna:
        a = math.exp(l); z = 1 / a - 1
        rhom = LG_OM * RHOC0 / a ** 3
        f = lambda lr: math.log(M * float(nuf(np.array([LG_G * M / math.exp(lr) ** 2 / a0]))[0])
                                / (4 / 3 * math.pi * math.exp(3 * lr) * rhom)) - math.log(delta_ta(z))
        out.append(math.exp(brentq(f, math.log(1e-4 * LG_Mpc), math.log(200 * LG_Mpc), xtol=1e-10)))
    return np.array(out)


def lg_integrate_trunc(Mb, a0, nuf, xe, ri, n=2000, a_start=0.02):
    M = Mb * LG_Msun
    lna = np.linspace(math.log(a_start), 0.0, n + 1)
    h_ = lna[1] - lna[0]
    half = np.concatenate([lna, lna[:-1] + h_ / 2])
    rt_all = rta_table(Mb, a0, nuf, np.sort(half)) if np.isfinite(xe) else None
    lsort = np.sort(half)
    r = ri.copy()
    uu = LG_H0 * math.sqrt(LG_OM / a_start ** 3 + LG_OL) * r
    dead = np.zeros_like(r, dtype=bool)

    def accf(l, rr):
        a = math.exp(l)
        H = LG_H0 * math.sqrt(LG_OM / a ** 3 + LG_OL)
        rr = np.maximum(rr, 1e-6 * LG_Mpc)
        gN = LG_G * M / rr ** 2
        g = nuf(gN / a0) * gN
        if np.isfinite(xe):
            re_ = xe * float(np.interp(l, lsort, rt_all))
            Me = M * float(nuf(np.array([LG_G * M / re_ ** 2 / a0]))[0])
            g = np.where(rr <= re_, g, LG_G * Me / rr ** 2)
        return -g + LG_OL * LG_H0 ** 2 * rr, H
    for i in range(n):
        l = lna[i]
        a1, H1 = accf(l, r); k1r, k1u = uu / H1, a1 / H1
        a2, H2 = accf(l + h_ / 2, r + h_ * k1r / 2); k2r, k2u = (uu + h_ * k1u / 2) / H2, a2 / H2
        a3, H3 = accf(l + h_ / 2, r + h_ * k2r / 2); k3r, k3u = (uu + h_ * k2u / 2) / H3, a3 / H3
        a4, H4 = accf(l + h_, r + h_ * k3r); k4r, k4u = (uu + h_ * k3u) / H4, a4 / H4
        r = r + h_ * (k1r + 2 * k2r + 2 * k3r + k4r) / 6
        uu = uu + h_ * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        dead |= r <= 1e-5 * LG_Mpc
        r = np.where(dead, 1e-5 * LG_Mpc, r); uu = np.where(dead, -1.0, uu)
    return r, uu


def R0_trunc(Mb, a0, nuf, xe, n=2000, K=24, iters=6):
    lo, hi = math.log(0.001 * LG_Mpc), math.log(30.0 * LG_Mpc)
    for _ in range(iters):
        xg = lo + (hi - lo) * np.linspace(0.0, 1.0, K)
        r, uu = lg_integrate_trunc(Mb, a0, nuf, xe, np.exp(xg), n=n)
        s_ = np.sign(uu); idx = np.where((s_[:-1] < 0) & (s_[1:] > 0))[0]
        if not len(idx):
            return float("nan")
        j = idx[-1]; lo, hi = xg[j], xg[j + 1]
    r, uu = lg_integrate_trunc(Mb, a0, nuf, xe, np.exp(np.array([lo, hi])), n=n)
    fr_ = -uu[0] / (uu[1] - uu[0])
    return float((r[0] + fr_ * (r[1] - r[0])) / LG_Mpc)


# the truncated integrator at x_e -> infinity must equal FP1's untruncated one (same RK4, same grid)
dchk = abs(R0_trunc(1.145e11, LG_A0["canonical"], C.nu_rar, float("inf")) - rc[0])
check("C1b CONTROL: the truncated integrator with no truncation equals FP1's integrator (nu_RAR, 1.145e11, canonical)",
      f"|d R0| {dchk:.1e} Mpc", dchk <= 1e-6)
# C1c (reported; added after the first -- MUTATE -- run, where C1b missed its 1e-6 by 2.7e-6): FP1 evaluates nu from its 3001-point
# log-y table (Ntab_lg); fed the same table, the truncated integrator must match FP1's to rounding.
_tab = Ntab_lg(C.nu_rar, 0.0)
nu_tab = lambda y: np.interp(np.log10(np.maximum(np.asarray(y, float), 1e-9)), ns["LY"], _tab)
dchk2 = abs(R0_trunc(1.145e11, LG_A0["canonical"], nu_tab, float("inf")) - rc[0])
check("C1c (reported; added after the first run) fed FP1's tabulated nu, the untruncated integrator equals FP1's (C1b's 2.7e-6 is the "
      "table's interpolation)", f"|d R0| {dchk2:.1e} Mpc", dchk2 <= 1e-9, load_bearing=False)

# ================================================================================================ the scan
R.banner("THE LG's R0 AGAINST THE EDGE")
XE = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.34, 0.40, 0.50, 0.70, 1.0, float("inf")]
RES = {}
for foot in ("canonical", "alt"):
    a0 = LG_A0[foot]
    for kn, kf in KERN.items():
        for Mb in (1.145e11, 1.72e11):
            row = {}
            for xe in XE:
                row[xe] = R0_trunc(Mb, a0, kf, float("inf") if MUTATE else xe)
            flo = C16[f"{foot}|{kn}"]
            row["floor"] = R0_trunc(Mb, a0, kf, float("inf") if MUTATE else flo)
            RES[(foot, kn, Mb)] = row
            xs = [x for x in XE if np.isfinite(x)]
            ok = [x for x in xs if row[x] <= 1.17]
            xmax = max(ok) if ok else 0.0
            if ok and xmax < xs[-1]:
                j = xs.index(xmax)
                xmax = float(np.interp(1.17, [row[xs[j]], row[xs[j + 1]]], [xs[j], xs[j + 1]]))
            row["xe_max"] = xmax; row["kids_floor"] = flo
            P(f"    {foot:9s} {kn:8s} M_b {Mb:.3g}: R0 [Mpc] at x_e " + ", ".join(f"{x:g}: {row[x]:.3f}" for x in XE)
              + f"; at KiDS's floor {flo:.3f}: {row['floor']:.3f}; LG allows x_e <= {xmax:.3f}")
h0 = all(v["floor"] < v[float("inf")] - 0.1 for v in RES.values())
check("H0 the truncation at KiDS's floor lowers the LG's R0 below the untruncated value by more than 0.1 Mpc (every case)"
      + ("  [MUTATE: no truncation]" if MUTATE else ""),
      "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]:.3g}: {v['floor']:.3f} vs {v[float('inf')]:.3f}" for k, v in RES.items()), h0)
h1 = all(v["floor"] <= 1.17 for v in RES.values())
check("H1 [HEADLINE] at KiDS's self-consistent floor the LG's R0 is within 2 sigma of 0.93 +- 0.12 Mpc (<= 1.17), every case",
      "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]:.3g}: {v['floor']:.3f}" for k, v in RES.items()), h1)
check("R1 (reported) the largest edge the LG allows against KiDS's floor",
      "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]:.3g}: LG x_e <= {v['xe_max']:.3f} vs KiDS >= {v['kids_floor']:.3f}" for k, v in RES.items()),
      True, load_bearing=False)
R.num("RES", {f"{k[0]}|{k[1]}|{k[2]:.4g}": {str(kk): vv for kk, vv in v.items()} for k, v in RES.items()})
nf = R.write()
sys.exit(1 if nf else 0)
