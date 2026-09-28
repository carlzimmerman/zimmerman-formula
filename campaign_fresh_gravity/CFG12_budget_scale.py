#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG12 -- THE TURNED-AROUND SHARE AT THE BUDGET'S OWN SCALE.  CFG4's strict cold budget sums the phantoms of every galaxy down to
M_* = 1e7 Msun, but compares the sum with the cold matter turned around at ONE scale: the Press-Schechter share at k = 1 h/Mpc
(Lagrangian mass 5.45e11 Msun, f_ta = 0.602).  Every budgeted system lives inside a turned-around region at least as massive as
its own turnaround mass, so the global necessary condition pairs the sum with the share above the SMALLEST budgeted system's
turnaround mass.  Is CFG4's strict closure a scale mismatch -- and does the mass-resolved form of the budget bind instead?

THE QUANTITIES (all CFG4's, none new).  Per system: CFG4_target's law profile, turnaround radius r_ta (Delta_ta(0) = 11.81) and
phantom inside x r_ta; the turnaround mass M_ta = the law's enclosed mass at r_ta (CFG4's own convention for r_ta).  The share:
f_ta(M) = erfc(delta_lin,ta / (sqrt 2 sigma(M))), delta_lin,ta(0) = 1.2761 (CFG4_switch D1), sigma from CLASS at the Lagrangian
radius of M (CFG7_common's engine; control C1 against CFG4_switch's committed sigma).  KiDS floors with the 2-halo term and FG001's
grouping ratio R(x) (the most conservative committed sample, D <= 15 Mpc) are read from CFG4_switch and CFG11.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG7_common's sigma reproduces CFG4_switch's committed sigma at k = 0.1/0.3/1 h/Mpc (z = 0) within 0.3%, and f_ta at
      k = 1 h/Mpc within 0.003.
  C2  CONTROL  with CFG4's share (0.6023) the strict edges (every galaxy) reproduce CFG4_target's committed 0.280/0.278/0.243/0.241
      exactly (this lane's copy of the budget; CFG11 C1 verified the same copy).
  D1  (derived, reported) the smallest budgeted system's turnaround mass M_ta,min (M_* = 1e7 and its SPARC gas) and f_ta(M_ta,min),
      both footings, both kernels; bracket: M_ta,min halved (a truncated phantom encloses less).
  H1  [HEADLINE; MUTATE must fail] with the share taken at M_ta,min (CFG4's convention) the strict edge, every galaxy its own system,
      reaches the KiDS floor (2-halo) for both footings and both kernels.  Declared EXPECTATION: canonical yes, alt uncertain.
  H2  the same with FG001's grouping (CFG11's committed D <= 15 Mpc ratio, applied above its mass limit): both footings, both
      kernels.  EXPECTATION: pass.
  H3  (reported, the stronger necessary condition) THE MASS-RESOLVED BUDGET: at every threshold M, the phantoms of systems with
      M_ta >= M (at x = the KiDS floor) fit into the cold matter turned around above M:  SUM_{M_ta >= M} Omega_ph <= Omega_c f_ta(M).
      Reported: the largest ratio LHS/RHS over thresholds and where it binds, every galaxy and FG001-scaled (a uniform R above the
      limit -- an approximation: grouping also moves mass to larger M_ta), with M_ta and M_ta/2.
MUTATE=1: the share is held at CFG4's k = 1 h/Mpc value (0.6023) in H1 -- the edges return to CFG4's and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG12_budget_scale.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json
import numpy as np
from scipy.special import erfc

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG12_budget_scale", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the share held at CFG4's k = 1 h/Mpc value in H1 -- H1 must FAIL ***")
np.seterr(all="ignore")

SW = json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]
T4 = json.load(open(os.path.join(HERE, "CFG4_target_results.json")))["numbers"]["H3"]
C11 = json.load(open(os.path.join(HERE, "CFG11_budget_hierarchy_results.json")))["numbers"]["RES"]
A0 = C.A0
KERN = {"P2": C.nu_p2, "nu_mono": C.nu_mono}

# ================================================================================================ CFG4_target's budget (the copy CFG11 C1 verified)
H_FID = 0.6733167
LMS, PHI1, AL1, PHI2, AL2 = 10.66, 3.96e-3, -0.35, 0.79e-3, -1.47
lmg = np.linspace(7.0, 12.3, 1060)
Mst = 10 ** lmg
x_ = Mst / 10 ** LMS
phi = math.log(10) * np.exp(-x_) * (PHI1 * x_ ** (AL1 + 1) + PHI2 * x_ ** (AL2 + 1))
Mst_h = Mst * (0.7 / H_FID) ** 2
phi_h = phi * (H_FID / 0.7) ** 3
GAL = C.load_sparc()
ls_, lg_ = [], []
for g in GAL:
    m = g["meta"]
    if m and m["MHI"] > 0 and m["L36"] > 0:
        ms_ = 0.5 * m["L36"] * 1e9
        ls_.append(math.log10(ms_)); lg_.append(math.log10(1.33 * m["MHI"] * 1e9 / ms_))
cfit = np.polyfit(ls_, lg_, 1)
fgas = 10 ** np.polyval(cfit, np.log10(Mst_h))
RHOC0 = 3 * (100 * H_FID * 1e3 / C.MPC) ** 2 / (8 * math.pi * C.G_SI)
RHOC0_MSUN = RHOC0 * C.MPC ** 3 / C.MSUN
OM0 = 0.3153; OC0 = 0.1200 / H_FID ** 2
DTA0 = SW["D1"]["0.0"]["one_plus_delta_ta"]
DLIN = SW["D1"]["0.0"]["delta_lin_ta"]
RG = np.geomspace(1e-3, 30.0, 3000) * C.MPC
F_TA_K1 = max(r_["f_ta"] for r_ in SW["V"]["web"] if r_["z"] == 0.0)
KIDS = SW["H2c"]["x_floor"]
MB = Mst_h * (1 + fgas) * C.MSUN


def rta_of(Mb, kfun, a0):
    rhom = OM0 * RHOC0
    MR = Mb[:, None] * kfun(C.G_SI * Mb[:, None] / RG[None, :] ** 2 / a0)
    D = MR / (4 / 3 * math.pi * RG[None, :] ** 3 * rhom)
    j = np.argmax(D < DTA0, axis=1)
    i = np.arange(len(Mb))
    lr = np.log(RG[j - 1]) + (math.log(DTA0) - np.log(D[i, j - 1])) * (np.log(RG[j]) - np.log(RG[j - 1])) / \
        (np.log(D[i, j]) - np.log(D[i, j - 1]))
    return np.exp(lr)


RTA = {(f, kn): rta_of(MB, kf, A0[f]) for f in C.FOOTS for kn, kf in KERN.items()}
MTA = {k: MB * KERN[k[1]](C.G_SI * MB / RTA[k] ** 2 / A0[k[0]]) / C.MSUN for k in RTA}     # the law's enclosed mass at r_ta [Msun]


def mph(f, kn, x):
    rc = x * RTA[(f, kn)]
    return MB * (KERN[kn](C.G_SI * MB / rc ** 2 / A0[f]) - 1.0) / C.MSUN


def omega_ph(f, kn, x, mcut=7.0, sel=None):
    m = np.log10(Mst_h) >= mcut
    if sel is not None:
        m &= sel
    return float(np.trapz((phi_h * mph(f, kn, x))[m], lmg[m]) / RHOC0_MSUN) if m.sum() > 1 else 0.0


XS = np.round(np.arange(0.20, 0.801, 0.005), 3)


def x_edge(fun, limit):
    om = np.array([fun(x) for x in XS])
    if om[0] > limit:
        return 0.0
    if om[-1] <= limit:
        return float(XS[-1])
    return float(np.interp(limit, om, XS))


# ================================================================================================ C1 sigma and the share
R.banner("C1  CONTROL: sigma(M) and the turned-around share against CFG4_switch")
cos = C7.LCDM


def sigma_M(M):
    Rl = float(C7.R_lagr(M, cos))
    return math.sqrt(C7.sig2(Rl, Rl, cos))


def f_ta(M):
    return float(erfc(DLIN / (math.sqrt(2) * sigma_M(M))))


dev_s, dev_f = 0.0, 0.0
for r_ in SW["V"]["web"]:
    if r_["z"] != 0.0:
        continue
    s = sigma_M(r_["M"])
    dev_s = max(dev_s, abs(s / r_["sigma"] - 1))
    dev_f = max(dev_f, abs(float(erfc(DLIN / (math.sqrt(2) * s))) - r_["f_ta"]))
    P(f"    k = {r_['k']:.1f} h/Mpc, M = {r_['M']:.3e}: sigma {s:.4f} (CFG4_switch {r_['sigma']:.4f}), f_ta "
      f"{float(erfc(DLIN / (math.sqrt(2) * s))):.4f} ({r_['f_ta']:.4f})")
check("C1 CONTROL: CFG7_common's sigma(M) reproduces CFG4_switch's committed sigma within 0.3% and f_ta within 0.003 (z = 0)",
      f"max sigma deviation {100 * dev_s:.2f}%, max f_ta deviation {dev_f:.4f}", dev_s <= 0.003 and dev_f <= 0.003)

# ================================================================================================ C2 CFG4's edges with CFG4's share
dev2 = 0.0
for f in C.FOOTS:
    for kn in KERN:
        xb = x_edge(lambda x: omega_ph(f, kn, x), OC0 * F_TA_K1)
        ref = T4["x_budget"][f"{f}|{kn}|z0.0|m7.0"]["x_bound"]
        dev2 = max(dev2, abs(xb - ref))
check("C2 CONTROL: with CFG4's share (0.6023) this lane's strict edges reproduce CFG4_target's committed ones (every galaxy)",
      f"max |d x| {dev2:.4f} (CFG4 on a coarser x grid; tolerance 0.003)", dev2 <= 0.003)

# ================================================================================================ D1 the smallest system's scale
R.banner("D1  THE SMALLEST BUDGETED SYSTEM'S TURNAROUND MASS AND ITS SHARE")
D1 = {}
for f in C.FOOTS:
    for kn in KERN:
        mmin = float(MTA[(f, kn)][0])
        D1[(f, kn)] = dict(M_ta_min=mmin, f_ta=f_ta(mmin), f_ta_half=f_ta(mmin / 2), sigma=sigma_M(mmin))
        P(f"    {f:9s} {kn:8s}: M_* = {Mst_h[0]:.2e}, M_b = {MB[0] / C.MSUN:.2e} -> M_ta,min {mmin:.3e} Msun (sigma {D1[(f, kn)]['sigma']:.3f}); "
          f"f_ta {D1[(f, kn)]['f_ta']:.4f} (at M_ta/2: {D1[(f, kn)]['f_ta_half']:.4f}) vs CFG4's {F_TA_K1:.4f}")
check("D1 (reported) the smallest budgeted system's turnaround mass and the turned-around share above it",
      "; ".join(f"{k[0][:3]}/{k[1]}: M_ta,min {v['M_ta_min']:.2e}, f_ta {v['f_ta']:.3f} ({v['f_ta_half']:.3f} at half)" for k, v in D1.items()),
      True, load_bearing=False)


# ================================================================================================ H1 / H2
def R_fg001(f, kn, x):
    v = C11[f"D<=15|{f}|{kn}"]
    return float(np.interp(x, [0.31, 0.40], [v["R031"], v["R04"]]))


MLIM = C11["D<=15|canonical|P2"]["log_mstar_lim"]
R.banner("H1 / H2  THE STRICT EDGE WITH THE SHARE AT THE BUDGET'S OWN SCALE")
H = {}
for f in C.FOOTS:
    for kn in KERN:
        share = F_TA_K1 if MUTATE else D1[(f, kn)]["f_ta"]
        lim = OC0 * share
        x1 = x_edge(lambda x: omega_ph(f, kn, x), lim)
        x1h = x_edge(lambda x: omega_ph(f, kn, x), OC0 * D1[(f, kn)]["f_ta_half"])
        fun2 = lambda x: omega_ph(f, kn, x) - (1.0 - R_fg001(f, kn, x)) * omega_ph(f, kn, x, MLIM)
        x2 = x_edge(fun2, lim)
        x2h = x_edge(fun2, OC0 * D1[(f, kn)]["f_ta_half"])
        H[(f, kn)] = dict(share=share, x_every=x1, x_every_half=x1h, x_fg001=x2, x_fg001_half=x2h,
                          floor=KIDS[f"{f}|{kn}|A2"][0], x_cfg4=T4["x_budget"][f"{f}|{kn}|z0.0|m7.0"]["x_bound"])
        v = H[(f, kn)]
        P(f"    {f:9s} {kn:8s}: share {share:.4f} -> strict edge every galaxy {x1:.3f} (M_ta/2: {x1h:.3f}); FG001 {x2:.3f} "
          f"({x2h:.3f}); KiDS floor {v['floor']:.3f}; CFG4 {v['x_cfg4']:.3f}")
check("H1 [HEADLINE] with the share at the smallest budgeted system's turnaround scale, the strict edge (every galaxy) reaches the "
      "KiDS floor on both footings and both kernels" + ("  [MUTATE: share held at 0.6023]" if MUTATE else ""),
      "; ".join(f"{k[0][:3]}/{k[1]}: {v['x_every']:.3f} vs {v['floor']:.3f}" for k, v in H.items()),
      all(v["x_every"] >= v["floor"] for v in H.values()))
check("H2 the same with FG001's grouping (CFG11, D <= 15 Mpc, the most conservative committed sample)",
      "; ".join(f"{k[0][:3]}/{k[1]}: {v['x_fg001']:.3f} vs {v['floor']:.3f}" for k, v in H.items()),
      all(v["x_fg001"] >= v["floor"] for v in H.values()))

# ================================================================================================ H3 the mass-resolved budget
R.banner("H3  THE MASS-RESOLVED BUDGET (reported): at every threshold M, the phantoms above M against the share above M")
H3 = {}
for f in C.FOOTS:
    for kn in KERN:
        xf = KIDS[f"{f}|{kn}|A2"][0]
        for lab, scale in (("M_ta", 1.0), ("M_ta/2", 0.5)):
            mta = MTA[(f, kn)] * scale
            thr = np.geomspace(mta[0], mta[-1] / 3, 40)
            worst = (0.0, None, None)
            worst_fg = (0.0, None)
            for Mt in thr:
                sel = mta >= Mt
                lhs = omega_ph(f, kn, xf, sel=sel)
                lhs_fg = lhs - (1.0 - R_fg001(f, kn, xf)) * omega_ph(f, kn, xf, MLIM, sel=sel)
                rhs = OC0 * f_ta(Mt)
                if lhs / rhs > worst[0]:
                    worst = (lhs / rhs, Mt, f_ta(Mt))
                if lhs_fg / rhs > worst_fg[0]:
                    worst_fg = (lhs_fg / rhs, Mt)
            H3[(f, kn, lab)] = dict(max_ratio=worst[0], M_bind=worst[1], f_ta_bind=worst[2], max_ratio_fg001=worst_fg[0], M_bind_fg001=worst_fg[1])
            P(f"    {f:9s} {kn:8s} {lab:7s}: at x = {xf:.3f} the largest (phantoms above M)/(share above M) = {worst[0]:.3f} at M = "
              f"{worst[1]:.2e} (f_ta {worst[2]:.3f}); FG001-scaled {worst_fg[0]:.3f} at {worst_fg[1]:.2e}")
check("H3 (reported) the mass-resolved budget at the KiDS floor: largest ratio over thresholds (<= 1 means it holds at every scale)",
      "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]}: {v['max_ratio']:.2f} (FG001 {v['max_ratio_fg001']:.2f}) at {v['M_bind']:.1e}" for k, v in H3.items()),
      True, load_bearing=False)
R.num("D1", {f"{k[0]}|{k[1]}": v for k, v in D1.items()})
R.num("H", {f"{k[0]}|{k[1]}": v for k, v in H.items()})
R.num("H3", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in H3.items()})
nf = R.write()
sys.exit(1 if nf else 0)
