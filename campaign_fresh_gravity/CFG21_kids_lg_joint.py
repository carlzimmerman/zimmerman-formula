#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG21 -- ONE NUMBER FOR THE TARGET LAW'S EDGE CONFLICT: KiDS's isolated lenses and the Local Group's zero-velocity radius, jointly.

WHY.  CFG16 put KiDS's self-consistent floor at x_e ~ 0.34 (the 2-halo cap of each lens bin at the peak-background bias of its
truncated turnaround mass); CFG20 found the LG allows only x_e <= 0.16-0.26 (R0 <= 1.17 Mpc).  A universal edge serves both only if
there is an x_e where the two are jointly acceptable.  This lane scans x_e and scores both data sets on one chi^2:
      chi^2(x_e) = d chi^2_KiDS(x_e; self-consistent caps)  +  [(R0(x_e) - 0.93) / 0.12]^2
with d chi^2_KiDS from CFG16's exact machinery (CFG4_switch's KiDS slices exec'd read-only, the untruncated law as reference) and
R0(x_e) from CFG20's committed table (interpolated in x_e).  One parameter (x_e) is fitted to two data sets.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  the recomputed self-consistent KiDS floor equals CFG16's committed floor, and R0 at CFG20's grid points equals CFG20's
      committed values (exact).
  H1  [HEADLINE; MUTATE must fail] a universal edge is jointly acceptable: min over x_e of chi^2(x_e) <= 9 (the two data sets agree
      within 3 sigma at the best edge) on the canonical footing, both kernels, the lower LG baryon mass (1.145e11, the easier case).
      Declared EXPECTATION: FAIL.
  R1  (reported) the best edge, the joint minimum and its sigma equivalent (sqrt of the joint minimum), every case (both footings,
      both kernels, both LG masses); the minimum with KiDS's tolerance halved/doubled is not scored.
MUTATE=1: the LG term is dropped (KiDS alone) -- the check that must fail in MUTATE is
  H0: the LG term raises the joint minimum above KiDS's own minimum by more than 9 in every case.
REVISION (after the first -- MUTATE -- run, before any main run; disclosed): H1 as first written scored chi^2 = d chi^2_KiDS (against
  the UNTRUNCATED law) + chi^2_LG and asked min <= 9.  The MUTATE run showed KiDS's own best edge (x_e ~ 0.5-0.6) sits 27-34 BELOW
  that reference, so the declared statistic passes trivially whatever the LG does.  The operative statistic is the standard
  parameter-difference tension -- each data set against its own best:  T(x_e) = [chi^2_KiDS(x_e) - min chi^2_KiDS] + chi^2_LG(x_e),
  T_min ~ (sigma)^2 for one shared parameter -- with the scan extended to x_e = 1.  H1 (operative): T_min <= 9 on the canonical footing,
  both kernels, LG M_b 1.145e11.  The first-written statistic is still printed (reported).
Run: python3 campaign_fresh_gravity/CFG21_kids_lg_joint.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG21_kids_lg_joint", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the LG term dropped -- H0 must FAIL ***")
np.seterr(all="ignore")
SWJ = json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]
C16 = json.load(open(os.path.join(HERE, "CFG16_selfconsistent_floor_results.json")))["numbers"]["floors"]
C20 = json.load(open(os.path.join(HERE, "CFG20_lg_edge_results.json")))["numbers"]["RES"]

# ================================================================================================ CFG16's machinery (exec'd slices, as CFG16)
C16P = os.path.join(HERE, "CFG16_selfconsistent_floor.py")
src = open(C16P).read()
ns = {"__file__": C16P, "__name__": "cfg16_slices", "json": json, "os": os, "sys": sys, "math": math, "time": time, "np": np,
      "C7": C7, "C": C, "HERE": HERE, "MUTATE": False, "P": lambda *a, **k: None,
      "check": lambda *a, **k: None, "R": type("Q", (), {"banner": lambda self, *a, **k: None, "num": lambda self, *a, **k: None})()}
a = src.index("SWJ = json.load(")
b = src.index("# ================================================================================================ C1\n")
exec(compile("\n" * src[:a].count("\n") + src[a:b], C16P, "exec"), ns)
floor, caps_at, TAB, XF, KERN = ns["floor"], ns["caps_at"], ns["TAB"], ns["XF"], ns["KERN"]
table, kfit_caps, M_trunc_xta, BASE = ns["table"], ns["kfit_caps"], ns["M_trunc_xta"], ns["BASE"]


def kids_scan(f, kn, xs):
    out = []
    for x in xs:
        key = (f, kn, float(x))
        if key not in TAB:
            TAB[key] = table(M_trunc_xta(KERN[kn], float(x)), f)
        out.append(kfit_caps(TAB[key], caps_at(f, kn, float(x))) - BASE[(f, kn)])
    return np.array(out)


# ================================================================================================ C1
R.banner("C1  CONTROL: CFG16's floor and CFG20's R0 reproduced")
dev_f = 0.0
for f in C.FOOTS:
    for kn in KERN:
        fl = floor(f, kn, lambda x, _f=f, _k=kn: caps_at(_f, _k, x))
        dev_f = max(dev_f, abs(fl - C16[f"{f}|{kn}"]))
XE_G = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.34, 0.40, 0.50, 0.70, 1.0]


def r0_of(f, kn, mb, x):
    row = C20[f"{f}|{kn}|{mb}"]
    return float(np.interp(x, XE_G, [row[str(v)] for v in XE_G]))


dev_r = max(abs(r0_of(f, kn, mb, x) - C20[f"{f}|{kn}|{mb}"][str(x)]) for f in C.FOOTS for kn in KERN for mb in ("1.145e+11", "1.72e+11")
            for x in XE_G)
check("C1 CONTROL: CFG16's committed self-consistent floors and CFG20's committed R0 grid reproduced exactly",
      f"max |d floor| {dev_f:.1e}; max |d R0| {dev_r:.1e}", dev_f <= 1e-12 and dev_r <= 1e-12)

# ================================================================================================ the joint scan
R.banner("THE JOINT SCAN: KiDS (self-consistent 2-halo) + the LG's R0, one universal edge")
XS = np.round(np.arange(0.10, 1.0001, 0.01), 2)
RES = {}
for f in C.FOOTS:
    for kn in KERN:
        dk = kids_scan(f, kn, XS)
        for mb in ("1.145e+11", "1.72e+11"):
            lg = np.array([((r0_of(f, kn, mb, float(x)) - 0.93) / 0.12) ** 2 for x in XS])
            tot = dk + (0.0 if MUTATE else lg)                                                  # first-written (reported)
            T = (dk - dk.min()) + (0.0 if MUTATE else lg)                                      # operative tension
            j = int(np.argmin(tot)); jt = int(np.argmin(T)); jk = int(np.argmin(dk)); jl = int(np.argmin(lg))
            RES[(f, kn, mb)] = dict(x_best=float(XS[jt]), T_min=float(T[jt]), sigma_eq=float(math.sqrt(max(T[jt], 0.0))),
                                    kids_best_x=float(XS[jk]), kids_min=float(dk.min()), lg_best_x=float(XS[jl]),
                                    kids_excess_at=float(dk[jt] - dk.min()), lg_at=float(lg[jt]),
                                    chi2_min=float(tot[j]), x_first=float(XS[j]))
            v = RES[(f, kn, mb)]
            P(f"    {f:9s} {kn:8s} LG M_b {mb}: KiDS best x_e {v['kids_best_x']:.2f} (d chi^2 {v['kids_min']:+.1f} vs untruncated); LG best "
              f"{v['lg_best_x']:.2f}; joint best {v['x_best']:.2f}: KiDS excess {v['kids_excess_at']:.1f} + LG {v['lg_at']:.1f} = T_min "
              f"{v['T_min']:.1f} (~{v['sigma_eq']:.1f} sigma) | first-written statistic {v['chi2_min']:.1f} at {v['x_first']:.2f}")
h0 = all(v["T_min"] > 9 for v in RES.values())
check("H0 the LG term raises the joint minimum above KiDS's own minimum by more than 9 in every case" + ("  [MUTATE: LG dropped]" if MUTATE else ""),
      "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]}: T_min {v['T_min']:.1f}" for k, v in RES.items()), h0)
h1 = all(RES[("canonical", kn, "1.145e+11")]["T_min"] <= 9 for kn in KERN)
check("H1 [HEADLINE, operative statistic -- see REVISION] a universal edge is jointly acceptable (T_min <= 9) on the canonical footing, "
      "both kernels, LG M_b 1.145e11 [declared expectation: FAIL]",
      "; ".join(f"{kn}: T_min {RES[('canonical', kn, '1.145e+11')]['T_min']:.1f} at x_e {RES[('canonical', kn, '1.145e+11')]['x_best']:.2f}"
                for kn in KERN), h1)
check("R1 (reported) every case's tension, best edges, and the first-written statistic",
      "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]}: T {v['T_min']:.1f} (~{v['sigma_eq']:.1f} sigma) at {v['x_best']:.2f}; KiDS best {v['kids_best_x']:.2f}, "
                f"LG best {v['lg_best_x']:.2f}; first-written {v['chi2_min']:.1f}" for k, v in RES.items()), True, load_bearing=False)
R.num("RES", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in RES.items()})
nf = R.write()
sys.exit(1 if nf else 0)
