#!/usr/bin/env python3
"""X78_cgm_closure_regrade: route E fair-share halos (smooth core) with Zhang+24's hot CGM gravitating and cut at their
closure radius 3 R_vir; the law with the same baryons. Graded on KiDS lensing (X53 harness, bins 3-4) and GAMA satellites
(X75 frozen measurement, bins 3-4). Frozen criteria: FROZEN_CRITERIA.md (04848505f2). One thread.
kappa = 1/2 FITTED; c_f EXTERNAL; footings never pooled; not theory closed; nothing here says the data favour the framework.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x78_regrade.py
"""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None); os.environ.pop("X75_MUTATE", None); os.environ.pop("X75_MAXNFOF", None)
import numpy as np
from scipy.optimize import brentq
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "X76_galaxy_fair_share_halos")); import x76_patch as XP
OUT, CHK = [], {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CHK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")

# ------------------------------------------------------------ X75 (measurement + Jeans) and its smooth X53 namespace, read-only
S75 = os.path.join(REB, "X75_satellite_kinematics_mass_gap", "x75_satkin.py"); s75 = open(S75).read()
s75 = s75[:s75.index('RES["footings"] = {}')]
G75 = {"__file__": S75, "__name__": "x75_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s75, S75, "exec"), G75)
NS = G75["NS"]["S"]; NF = NS["NF"]; AQ = NF["AQ"]
RG_ALL = NS["RGRID_PC"]; Gpc, a0u, H_NAT = NS["Gpc"], NS["a0u"], NS["H_NAT"]
P(f"X78_cgm_closure_regrade  criteria 04848505f2  [X75 measurement + X53 smooth machinery loaded, {time.time() - T0:.0f} s]")

# ------------------------------------------------------------ CGM model (Zhang+24, MW-mass)
ZT1 = np.array([[10.5, 178e3], [10.75, 210e3], [11.0, 295e3]])
EDGES = {"central": (1.84, 0.43), "generous": (3.25, 0.37), "tight": (0.418, 0.53)}
RC = 6e3


def Rvir(l): return float(np.interp(l, ZT1[:, 0], ZT1[:, 1]))


def hot_profile(Ms, l, norm, beta, k):
    """M_hot(<r) on RG_ALL: beta profile normalised to norm*Ms at R_vir, cut at k R_vir."""
    r = RG_ALL; rho = (1 + (r / RC) ** 2) ** (-1.5 * beta); rho = np.where(r <= k * Rvir(l), rho, 0.0)
    dm = 4 * math.pi * r * r * rho; M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r))]
    return M * (norm * Ms / np.interp(Rvir(l), r, M))


def f2_hot(Ms): return 0.5 * Ms * np.minimum(1.0, (RG_ALL / 1e5) ** 3)


def baryons(l, hot):
    l70 = l - 2 * np.log10(0.70 / H_NAT); Ms = 10 ** l; Mc = Ms * 10 ** (-0.69 * l70 + 6.63)
    Mh = f2_hot(Ms) if hot is None else hot_profile(Ms, l, *hot)
    return Ms, Mc, Mh


def mass_route_e(foot, l, z, hot):
    """fair-share smooth-core halo (X76 rule) + baryons; hot=None -> F2's 0.5 M* hot gas (K1 identity)."""
    Ms, Mc, Mh = baryons(l, hot)
    if hot is None:
        Mbt = Ms + Mc + 0.5 * Ms
    else:
        f = lambda lr: math.log(XP.rta_pc(Ms + Mc + float(np.interp(math.exp(lr), RG_ALL, Mh)), z)) - lr
        rta = math.exp(brentq(f, math.log(1e4), math.log(1e8), xtol=1e-13))
        Mbt = Ms + Mc + float(np.interp(rta, RG_ALL, Mh))
    Mf = XP.RNAT * Mbt; rta = XP.rta_pc(Mbt, z)
    sc = NS["eta_of"](Mf + Mbt, "cf4") * NS["sigma_coll"](Mf + Mbt); Sig = max(NS["SIGA0"][foot], sc)
    r0 = NS["solve_r0"](Mf, rta, Sig)
    Mhalo = math.pi * Sig * r0 ** 2 * NS["B"](np.minimum(RG_ALL, rta) / r0)
    return Ms + Mc + Mh + Mhalo, Mf


def mass_law(foot, l, hot):
    Ms, Mc, Mh = baryons(l, hot); Mb = Ms + Mc + Mh
    return Mb * AQ.nu_simple(Gpc * Mb / RG_ALL ** 2 / a0u(foot))


Ms_t = 10 ** 10.8; Mh_t = hot_profile(Ms_t, 10.8, 1.84, 0.43, 3)
check("K3_cgm_norm_at_Rvir", abs(np.interp(Rvir(10.8), RG_ALL, Mh_t) / (1.84 * Ms_t) - 1) < 1e-8, f"{np.interp(Rvir(10.8), RG_ALL, Mh_t) / (1.84 * Ms_t) - 1:+.1e}")

# ------------------------------------------------------------ lensing stacks (X53 conventions)
LMG, INV, Rn, fit = NF["LMG"], NF["INV"], NS["Rn"], NS["fit"]
IDX_ALL = NS["IDX_ALL"]


def stack(fn):
    out = np.empty((4, 15)); h = H_NAT
    tab = np.array([fn(lm) for lm in LMG])                            # (nLMG, 4, 15) built per bin radii
    for b in range(4):
        lMs_nat = INV[b]["logMs70"] + 2 * np.log10(0.70 / h) + 2 * np.log10(INV[b]["qDA"]); w = INV[b]["w"]
        vals = np.array([np.interp(lMs_nat, LMG, tab[:, b, i]) for i in range(15)])
        out[b] = vals @ w / w.sum()
    return out


def ds_all_bins(M):
    return np.array([AQ.delta_sigma(Rn[b] * 1e6, RG_ALL, M, "const") for b in range(4)])


def lens_models(foot, hot):
    mH = stack(lambda lm: ds_all_bins(mass_route_e(foot, lm, 0.285, hot)[0]))
    mL = stack(lambda lm: ds_all_bins(mass_law(foot, lm, hot)))
    return mH, mL


def lens_grade(mH, mL):
    rH, _ = fit(mH, IDX_ALL, True); rL, _ = fit(mL, IDX_ALL, True)
    h34, l34 = sum(rH["per_bin"][2:]), sum(rL["per_bin"][2:])
    return dict(H2H_all=rH["chi2"], L2H_all=rL["chi2"], H2H_b34=h34, L2H_b34=l34, d_b34=h34 - l34, per_bin_H=rH["per_bin"], per_bin_L=rL["per_bin"],
                cls=("LAW" if h34 - l34 >= 9 else ("HALOS" if h34 - l34 <= -9 else "NOT DIAGNOSTIC")))


# K1 / K2 identities (F2 hot gas)
X76L = json.load(open(os.path.join(REB, "X76_galaxy_fair_share_halos", "x76_lensing_results_fair.json")))
X53L = json.load(open(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing_results.json")))
mH0, _ = lens_models("canonical", None)
mL0 = NF["stack_model"]("canonical", Rn, NS["CENTRAL0"])            # X53's own law stack (F2 baryons)
mL0b = stack(lambda lm: ds_all_bins(mass_law("canonical", lm, None)))
k1 = fit(mH0, IDX_ALL, True)[0]["chi2"] / X76L["footings"]["canonical"]["all"]["H2H"]["chi2"] - 1
k2 = fit(mL0b, IDX_ALL, True)[0]["chi2"] / X53L["footings"]["canonical"]["all"]["L2H"]["chi2"] - 1
check("K1_fair_H2H_reproduces_X76", abs(k1) < 1e-6, f"{k1:+.1e}")
check("K2_law_L2H_reproduces_X53", abs(k2) < 1e-6, f"{k2:+.1e}")
P(f"  [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------ satellites (X75 frozen measurement, bins 3-4)
LG, SEL, sigma2_ap, stk, GAM, meas = G75["LGRID"], G75["SEL"], G75["sigma2_ap"], G75["stack"], G75["GAM"], G75["meas"]["pair"]
ms, me = np.array(meas["sigma"]), np.array(meas["err"])


def sat_pred(foot, kind, hot):
    out = []
    for b in range(4):
        tab = np.array([sigma2_ap((mass_route_e(foot, l, 0.1797, hot)[0] if kind == "H" else mass_law(foot, l, hot))[SEL], GAM[b])[0] for l in LG])
        out.append(stk(tab, b))
    return np.array(out)


def sat_grade(pred):
    return dict(pred=pred.tolist(), chi2_b34=float((((pred[2:] - ms[2:]) / me[2:]) ** 2).sum()), chi2_all=float((((pred - ms) / me) ** 2).sum()))


RES = {"criteria": "04848505f2", "measured_sigma": ms.tolist(), "err": me.tolist(), "checks": CHK, "footings": {}}
for foot in ("canonical", "alt"):
    fo = {}
    for lab, (norm, beta) in EDGES.items():
        for k in ((3, 2, 5) if lab == "central" else (3,)):
            hot = (norm, beta, k); key = f"{lab}_k{k}"
            mH, mL = lens_models(foot, hot); lg = lens_grade(mH, mL)
            sH, sL = sat_grade(sat_pred(foot, "H", hot)), sat_grade(sat_pred(foot, "L", hot))
            fo[key] = dict(lens=lg, sat_H=sH, sat_L=sL)
            P(f"  [{foot} {key:12s}] lensing b3-4: H2H {lg['H2H_b34']:.1f} L2H {lg['L2H_b34']:.1f} d {lg['d_b34']:+.1f} ({lg['cls']}); all-bins H2H {lg['H2H_all']:.1f} L2H {lg['L2H_all']:.1f} | "
              f"sat H {np.round(sH['pred'], 1).tolist()} chi2 b3-4 {sH['chi2_b34']:.1f}; law {np.round(sL['pred'], 1).tolist()} chi2 b3-4 {sL['chi2_b34']:.1f}  [{time.time() - T0:.0f} s]")
    c = fo["central_k3"]; fails = ([] if c["sat_H"]["chi2_b34"] <= 6.0 else [f"satellites chi2 {c['sat_H']['chi2_b34']:.1f} > 6"]) + \
        ([] if c["lens"]["d_b34"] < 9 else [f"lensing d {c['lens']['d_b34']:+.1f} >= 9 (LAW)"])
    fo["verdict"] = "CGM-CLOSURE HALOS PASS" if not fails else "CGM-CLOSURE HALOS FAIL: " + "; ".join(fails)
    P(f"=== [{foot}] {fo['verdict']}"); RES["footings"][foot] = fo
# MUTATE: k = 1 lowers sigma_sat(H) in bins 3-4 (canonical)
p1 = sat_pred("canonical", "H", (1.84, 0.43, 1)); p3 = np.array(RES["footings"]["canonical"]["central_k3"]["sat_H"]["pred"])
check("MUTATE_k1_lowers_sigma", bool(np.all(p1[2:] < p3[2:])), f"k=1 {np.round(p1[2:], 1).tolist()} vs k=3 {np.round(p3[2:], 1).tolist()}")
V = {f: RES["footings"][f]["verdict"] for f in ("canonical", "alt")}
cls_ = {f: V[f].split(":")[0] + (":" + ";".join(x.split(" chi2")[0].split(" d ")[0] for x in V[f].split(": ", 1)[1].split("; ")) if ":" in V[f] else "") for f in V}   # class + failing lines, numbers stripped
RES["verdict"] = (V["canonical"] + " | alt: " + V["alt"]) if cls_["canonical"] == cls_["alt"] else f"FOOTINGS DISAGREE: {V}"
n = sum(CHK.values()); P(f"\n=== VERDICT: {RES['verdict']}\nchecks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, "x78_regrade_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "x78_regrade.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)
