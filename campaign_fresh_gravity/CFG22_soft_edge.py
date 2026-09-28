#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG22 -- A SOFT EDGE: can one phantom SHAPE satisfy KiDS and the Local Group together?

WHY.  CFG21 excluded a universal SHARP edge at 5-7 sigma: KiDS's isolated lenses want the phantom to run to x_e ~ 0.62 r_ta, the
LG's zero-velocity radius wants it to stop near 0.1 r_ta.  A sharp edge makes the enclosed mass jump from 'growing like r' to
'constant', so KiDS's large-radius signal can only be bought with a long phantom, which overloads the LG.  Collapsed matter does not
stop dead: its density steepens.  The soft edge keeps the law's phantom (rho ~ r^-2) inside r_s = x_s r_ta and continues it as
rho = rho_s (r_s/r)^3 -- continuous at r_s, no new amplitude -- out to r_ta (CFG4's convention for r_ta), constant enclosed mass beyond:
      M(r) = M_law(r)                                       r <= r_s
           = M_law(r_s) + r_s M_law'(r_s) ln(r / r_s)       r_s < r <= r_ta
           = M(r_ta)                                        r > r_ta
The shape is the one change; x_s replaces x_e as the one declared number.

THE TESTS (exactly CFG21's, with the soft profile).  KiDS: CFG16's machinery (CFG4_switch's KiDS slices exec'd read-only), the 2-halo
cap of each lens bin at the peak-background bias of the SOFT profile's own turnaround mass (self-consistent, as CFG16).  LG: CFG20's
shell integrator (FP1's, exec'd read-only) with r_s(t) = x_s r_ta(t) and the tail to r_ta(t).  Joint: T = [chi2_KiDS - min chi2_KiDS]
+ [(R0 - 0.93)/0.12]^2, minimised over x_s.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  with the tail switched off (rho = 0 beyond r_s) the lane reproduces CFG21's committed sharp-edge KiDS numbers (its own
      best x_e and minimum) and CFG20's committed R0 at x_e = 0.2 and 0.34 (canonical P2, 1.145e11) exactly.
  H0  [MUTATE must fail] the soft tail lowers the joint minimum T_min below the sharp edge's by more than 3, on the canonical footing.
  H1  [HEADLINE] one soft edge is jointly acceptable: T_min <= 9 on the canonical footing, both kernels, LG M_b 1.145e11.
      Expectation: uncertain.
  R1  (reported) every case (both footings, both kernels, both LG masses): x_s at the joint minimum, KiDS's and the LG's own best x_s,
      the R0 there, and the soft profile's mass at r_ta relative to the sharp edge's at KiDS's sharp best (the budget direction).
MUTATE=1: the tail is switched off (the sharp edge) -- H0 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG22_soft_edge.py   (MUTATE=1 for the control; several minutes)
"""
import os, sys, math, json, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG22_soft_edge", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the tail switched off (the sharp edge) -- H0 must FAIL ***")
np.seterr(all="ignore")
C20 = json.load(open(os.path.join(HERE, "CFG20_lg_edge_results.json")))["numbers"]["RES"]
C21 = json.load(open(os.path.join(HERE, "CFG21_kids_lg_joint_results.json")))["numbers"]["RES"]

# ================================================================================================ KiDS: CFG16's machinery
C16P = os.path.join(HERE, "CFG16_selfconsistent_floor.py")
src = open(C16P).read()
ns = {"__file__": C16P, "__name__": "cfg16_slices", "json": json, "os": os, "sys": sys, "math": math, "time": time, "np": np,
      "C7": C7, "C": C, "HERE": HERE, "MUTATE": False, "P": lambda *a, **k: None, "check": lambda *a, **k: None,
      "R": type("Q", (), {"banner": lambda self, *a, **k: None, "num": lambda self, *a, **k: None})()}
a_ = src.index("SWJ = json.load(")
b_ = src.index("# ================================================================================================ C1\n")
exec(compile("\n" * src[:a_].count("\n") + src[a_:b_], C16P, "exec"), ns)
GK, FIX, r_bound, M_law, BASE, KERN = ns["GK"], ns["FIX"], ns["r_bound"], ns["M_law"], ns["BASE"], ns["KERN"]
kfit_caps, bias_of, DTA25, LMB = ns["kfit_caps"], ns["bias_of"], ns["DTA25"], ns["LMB"]
LM, NPB, RPK, MPCK, MSK, RRK = GK["LM"], GK["npb"], GK["Rp"], GK["MPCm"], GK["MS"], GK["rrK"]


def M_soft(kfun, xs, tail=True):
    """the soft-edge profile on KiDS's r-grid: the law inside r_s = xs r_ta, rho ~ r^-3 (continuous) to r_ta, constant beyond."""
    def f_(Mb, a0):
        M = M_law(kfun)(Mb, a0)
        rta = r_bound(M, DTA25)
        rs = xs * rta
        Ms = float(np.interp(rs, RRK, M))
        dM = float(np.interp(rs, RRK, np.gradient(M, RRK)))
        out = np.where(RRK <= rs, M, Ms + (dM * rs * np.log(np.maximum(RRK, rs) / rs) if tail else 0.0))
        Mta = Ms + (dM * rs * math.log(max(rta, rs) / rs) if tail else 0.0)
        return np.where(RRK > rta, Mta, out)
    return f_


def table(Mfun, foot):
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, C.A0[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return T


def caps_soft(f, kn, xs, tail):
    out = []
    for lm in LMB:
        Mb = 10 ** lm * MSK
        M = M_soft(KERN[kn], xs, tail)(Mb, C.A0[f])
        rta2 = r_bound(M, DTA25)
        out.append(bias_of(float(np.interp(rta2, RRK, M)) / GK["MS"])[0])
    return out


def kids_scan(f, kn, xs_list, tail):
    return np.array([kfit_caps(table(M_soft(KERN[kn], float(x), tail), f), caps_soft(f, kn, float(x), tail)) - BASE[(f, kn)]
                     for x in xs_list])


# ================================================================================================ LG: CFG20's integrator (FP1's, exec'd)
FP1P = os.path.join(C.CHAIN, "FP1_static_sector.py")
lg = {"np": np, "math": math, "_trap": C._trap}
lg = C.exec_slices(FP1P, [("# ---- LG: XR4's point-mass", "Rctl = lg_R0(")], ns=lg, name="fp1_lg")[0]
C20P = os.path.join(HERE, "CFG20_lg_edge.py")
src20 = open(C20P).read()
lg.update({"json": json, "os": os, "HERE": HERE, "brentq": brentq,
           "SW": json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]["D1"]})
a2 = src20.index("ZT = sorted(")
b2 = src20.index("def lg_integrate_trunc(")
exec(compile("\n" * src20[:a2].count("\n") + src20[a2:b2], C20P, "exec"), lg)
LG_G, LG_Mpc, LG_Msun, LG_H0, LG_OM, LG_OL, LG_A0 = (lg[k] for k in ("LG_G", "LG_Mpc", "LG_Msun", "LG_H0", "LG_OM", "LG_OL", "LG_A0"))
rta_table = lg["rta_table"]


def lg_integrate_soft(Mb, a0, nuf, xs, ri, tail=True, n=2000, a_start=0.02):
    M = Mb * LG_Msun
    lna = np.linspace(math.log(a_start), 0.0, n + 1)
    h_ = lna[1] - lna[0]
    lsort = np.sort(np.concatenate([lna, lna[:-1] + h_ / 2]))
    rt_all = rta_table(Mb, a0, nuf, lsort)
    r = ri.copy()
    uu = LG_H0 * math.sqrt(LG_OM / a_start ** 3 + LG_OL) * r
    dead = np.zeros_like(r, dtype=bool)

    def Mlaw(rr):
        return M * nuf(LG_G * M / np.maximum(rr, 1e-6 * LG_Mpc) ** 2 / a0)

    def accf(l, rr):
        a = math.exp(l)
        H = LG_H0 * math.sqrt(LG_OM / a ** 3 + LG_OL)
        rr = np.maximum(rr, 1e-6 * LG_Mpc)
        rta = float(np.interp(l, lsort, rt_all)); rs = xs * rta
        Ms = float(Mlaw(np.array([rs]))[0])
        dM = float((Mlaw(np.array([rs * 1.0001]))[0] - Mlaw(np.array([rs * 0.9999]))[0]) / (0.0002 * rs))
        Mt = Ms + (dM * rs * np.log(np.minimum(np.maximum(rr, rs), rta) / rs) if tail else 0.0)
        Menc = np.where(rr <= rs, Mlaw(rr), Mt)
        return -LG_G * Menc / rr ** 2 + LG_OL * LG_H0 ** 2 * rr, H
    for i in range(n):
        l = lna[i]
        a1, H1 = accf(l, r); k1r, k1u = uu / H1, a1 / H1
        a2_, H2 = accf(l + h_ / 2, r + h_ * k1r / 2); k2r, k2u = (uu + h_ * k1u / 2) / H2, a2_ / H2
        a3, H3 = accf(l + h_ / 2, r + h_ * k2r / 2); k3r, k3u = (uu + h_ * k2u / 2) / H3, a3 / H3
        a4, H4 = accf(l + h_, r + h_ * k3r); k4r, k4u = (uu + h_ * k3u) / H4, a4 / H4
        r = r + h_ * (k1r + 2 * k2r + 2 * k3r + k4r) / 6
        uu = uu + h_ * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        dead |= r <= 1e-5 * LG_Mpc
        r = np.where(dead, 1e-5 * LG_Mpc, r); uu = np.where(dead, -1.0, uu)
    return r, uu


def R0_soft(Mb, a0, nuf, xs, tail=True, K=24, iters=6):
    lo, hi = math.log(0.001 * LG_Mpc), math.log(30.0 * LG_Mpc)
    for _ in range(iters):
        xg = lo + (hi - lo) * np.linspace(0.0, 1.0, K)
        r, uu = lg_integrate_soft(Mb, a0, nuf, xs, np.exp(xg), tail)
        s_ = np.sign(uu); idx = np.where((s_[:-1] < 0) & (s_[1:] > 0))[0]
        if not len(idx):
            return float("nan")
        j = idx[-1]; lo, hi = xg[j], xg[j + 1]
    r, uu = lg_integrate_soft(Mb, a0, nuf, xs, np.exp(np.array([lo, hi])), tail)
    fr_ = -uu[0] / (uu[1] - uu[0])
    return float((r[0] + fr_ * (r[1] - r[0])) / LG_Mpc)


# ================================================================================================ C1 the sharp limit
R.banner("C1  CONTROL: tail off = the sharp edge (CFG21's KiDS, CFG20's LG)")
XK = np.round(np.arange(0.10, 1.0001, 0.01), 2)
dk_sharp = kids_scan("canonical", "P2", XK, tail=False)
jk = int(np.argmin(dk_sharp))
ref = C21["canonical|P2|1.145e+11"]
d_k = max(abs(float(XK[jk]) - ref["kids_best_x"]), abs(float(dk_sharp.min()) - ref["kids_min"]))
r02 = R0_soft(1.145e11, LG_A0["canonical"], C.nu_p2, 0.2, tail=False)
r034 = R0_soft(1.145e11, LG_A0["canonical"], C.nu_p2, 0.34, tail=False)
d_l = max(abs(r02 - C20["canonical|P2|1.145e+11"]["0.2"]), abs(r034 - C20["canonical|P2|1.145e+11"]["0.34"]))
P(f"    sharp KiDS best x {XK[jk]:.2f} ({dk_sharp.min():+.3f}) vs CFG21 {ref['kids_best_x']:.2f} ({ref['kids_min']:+.3f}); LG R0 at 0.2 / 0.34: "
  f"{r02:.4f} / {r034:.4f} vs CFG20 {C20['canonical|P2|1.145e+11']['0.2']:.4f} / {C20['canonical|P2|1.145e+11']['0.34']:.4f}")
check("C1 CONTROL: with the tail off the lane reproduces CFG21's sharp-edge KiDS best and minimum and CFG20's R0 at 0.2 / 0.34",
      f"KiDS max |d| {d_k:.1e}; LG max |d R0| {d_l:.1e} Mpc", d_k <= 1e-9 and d_l <= 1e-6)

# ================================================================================================ the soft scan
R.banner("THE SOFT EDGE: KiDS and the LG against x_s")
XSS = np.round(np.concatenate([np.arange(0.02, 0.10, 0.01), np.arange(0.10, 0.601, 0.02)]), 3)
XL = [0.02, 0.03, 0.05, 0.07, 0.10, 0.14, 0.20, 0.30, 0.45, 0.60]
RES = {}
for f in C.FOOTS:
    for kn, kf in KERN.items():
        dk = kids_scan(f, kn, XSS, tail=not MUTATE)
        for mb in (1.145e11, 1.72e11):
            r0 = [R0_soft(mb, LG_A0[f], kf, x, tail=not MUTATE) for x in XL]
            r0i = np.interp(XSS, XL, r0)
            lgc = ((r0i - 0.93) / 0.12) ** 2
            T = (dk - dk.min()) + lgc
            j = int(np.argmin(T))
            sharp = C21[f"{f}|{kn}|{mb:.4g}".replace("1.145e+11", "1.145e+11")] if f"{f}|{kn}|{mb:.4g}" in C21 else \
                C21[f"{f}|{kn}|{'1.145e+11' if mb < 1.5e11 else '1.72e+11'}"]
            RES[(f, kn, mb)] = dict(x_best=float(XSS[j]), T_min=float(T[j]), sigma=float(math.sqrt(max(T[j], 0))),
                                    kids_best_x=float(XSS[int(np.argmin(dk))]), kids_excess=float(dk[j] - dk.min()),
                                    lg_best_x=float(XSS[int(np.argmin(lgc))]), R0_at=float(r0i[j]), T_sharp=sharp["T_min"],
                                    r0_grid=dict(zip([str(x) for x in XL], r0)))
            v = RES[(f, kn, mb)]
            P(f"    {f:9s} {kn:8s} LG {mb:.3g}: KiDS best x_s {v['kids_best_x']:.2f}; LG best {v['lg_best_x']:.2f}; joint x_s "
              f"{v['x_best']:.2f}: KiDS excess {v['kids_excess']:.1f}, R0 {v['R0_at']:.3f} -> T_min {v['T_min']:.1f} (~{v['sigma']:.1f} sigma); "
              f"sharp edge T_min {v['T_sharp']:.1f}")
h0 = all(RES[("canonical", kn, mb)]["T_min"] < RES[("canonical", kn, mb)]["T_sharp"] - 3 for kn in KERN for mb in (1.145e11, 1.72e11))
check("H0 the soft tail lowers the joint minimum below the sharp edge's by more than 3 (canonical)" + ("  [MUTATE: tail off]" if MUTATE else ""),
      "; ".join(f"{kn}/{mb:.3g}: {RES[('canonical', kn, mb)]['T_min']:.1f} vs sharp {RES[('canonical', kn, mb)]['T_sharp']:.1f}"
                for kn in KERN for mb in (1.145e11, 1.72e11)), h0)
h1 = all(RES[("canonical", kn, 1.145e11)]["T_min"] <= 9 for kn in KERN)
check("H1 [HEADLINE] one soft edge is jointly acceptable (T_min <= 9) on the canonical footing, both kernels, LG M_b 1.145e11",
      "; ".join(f"{kn}: T_min {RES[('canonical', kn, 1.145e11)]['T_min']:.1f} at x_s {RES[('canonical', kn, 1.145e11)]['x_best']:.2f}"
                for kn in KERN), h1)
check("R1 (reported) every case", "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]:.3g}: T {v['T_min']:.1f} at {v['x_best']:.2f} (KiDS {v['kids_best_x']:.2f}, "
                                            f"LG {v['lg_best_x']:.2f})" for k, v in RES.items()), True, load_bearing=False)
R.num("RES", {f"{k[0]}|{k[1]}|{k[2]:.4g}": v for k, v in RES.items()})
nf = R.write()
sys.exit(1 if nf else 0)
