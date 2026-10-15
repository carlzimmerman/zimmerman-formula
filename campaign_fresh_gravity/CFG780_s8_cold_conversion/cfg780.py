"""CFG780 -- cold energy -> dark energy conversion lowers late growth; rescore raw KiDS with the framework's P_grav x g(z)^2.
Criteria: FROZEN_CRITERIA.md (committed alone first, 977f341e1).
G1: linear growth in the conversion branch vs a no-conversion reference (same baryons, same initial delta at z = 8).
G2: CFG650's scorer (cfg650_native.py, CFG592 machinery) exec'd from its source with two injected changes only:
    (i) the framework run's P_grav at every snapshot is multiplied by g(z)^2; (ii) outputs go to this directory.
Run ONLY after the relaunched T1x has finished and been scored:
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg780.py          (CFG780_MUTATE=1: conversion x3)
kappa = 1/2 FITTED; cold energy mass required; not theory closed. The conversion mechanism is not derived (CFG775/779).
"""
import json
import math
import os
import sys

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
C650 = os.path.join(HERE, "..", "CFG650_theory_v2_combined_pm")
MUT = os.environ.get("CFG780_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


# ---------------------------------------------------------------- G1 growth
B0, CI = 0.0484, 0.2596                               # astra's projected Omega_b, primordial cold (5.364 Omega_b)
OMR = B0 + CI
psi = lambda z: 0.015 * (1 + z) ** 2.7 / (1 + ((1 + z) / 2.9) ** 5.6)
Ez_ref = lambda a: math.sqrt(OMR / a ** 3 + 1 - OMR)
ZS = 8.0
AA = np.exp(np.linspace(math.log(1 / (1 + ZS)), 0.0, 4001))
dt = np.array([psi(1 / a - 1) / (a * Ez_ref(a)) for a in AA])        # psi dt per dln a (reference clock; second order)
cum = np.concatenate([[0.0], np.cumsum(0.5 * (dt[1:] + dt[:-1]) * np.diff(np.log(AA)))])
FC = cum / cum[-1]                                                     # fraction of all conversion done by a


def branch(cold_surv, prop=False):
    """returns arrays B(a), C(a) comoving, V(a) physical (units of rho_ref), E(a)."""
    Dtot = CI * (1 - cold_surv) if not prop else None
    if prop:                                                           # same total loss as the cold-only primary, split proportionally
        Dtot = CI * (1 - 0.894)
        f = Dtot / OMR
        Ba, Ca = B0 * (1 - f * FC), CI * (1 - f * FC)
    else:
        Ba, Ca = B0 * np.ones_like(AA), CI - Dtot * FC
    loss = -(np.gradient(Ba + Ca, np.log(AA)))                        # comoving loss per dln a
    Va = np.concatenate([[0.0], np.cumsum(0.5 * (loss[1:] * AA[1:] ** -3 + loss[:-1] * AA[:-1] ** -3) * np.diff(np.log(AA)))])
    Va = Va + (1.0 - (Ba[-1] + Ca[-1]) - Va[-1])       # flatness today: constant vacuum part so E(1) = 1 (criteria: V0 set by flatness; first run omitted it)
    Ea = np.sqrt((Ba + Ca) / AA ** 3 + Va)
    return Ba, Ca, Va, Ea


def growth(Ba, Ca, Ea):
    lnE = np.log(Ea)
    dlnE = np.gradient(lnE, np.log(AA))
    Om = (Ba + Ca) / AA ** 3 / Ea ** 2
    x = np.log(AA)
    fO = lambda t: np.interp(t, x, Om)
    fd = lambda t: np.interp(t, x, dlnE)
    sol = integrate.solve_ivp(lambda t, y: [y[1], -(2 + fd(t)) * y[1] + 1.5 * fO(t) * y[0]], (x[0], 0.0), [AA[0], AA[0]],
                              t_eval=x, rtol=1e-10, atol=1e-14)
    return sol.y[0]


ref_E = np.array([Ez_ref(a) for a in AA])
D_R = growth(B0 * np.ones_like(AA), CI * np.ones_like(AA), ref_E)
VARS = {"primary (cold-only, survival 0.894)": (0.894, False), "half amount (0.947)": (0.947, False),
        "proportional (eta 5.364, survival 0.911)": (None, True), "zero conversion (K1)": (1.0, False)}
if MUT:
    VARS = {"MUTATE x3 (cold survival 0.682)": (0.682, False)}
G = {}
P("CFG780  growth with cold -> dark-energy conversion" + ("  [MUTATE x3]" if MUT else ""))
for lab, (cs, prop) in VARS.items():
    Ba, Ca, Va, Ea = branch(cs, prop)
    D_C = growth(Ba, Ca, Ea)
    g = (lambda ratio: (lambda z: float(np.interp(math.log(1 / (1 + z)), np.log(AA), ratio))))(D_C / D_R)   # bind per variant (first run: late-binding bug)
    G[lab] = dict(g0=g(0.0), g05=g(0.5), g1=g(1.0), E_today=float(Ea[-1]), V0=float(Va[-1]),
                  P_factor_z0=g(0.0) ** 2, fn=g)
    P(f"  {lab:42s}: E(today) {Ea[-1]:.4f} (flatness check; V0 {Va[-1]:.4f}); g = D_C/D_R at z 0 / 0.5 / 1 = "
      f"{g(0.0):.4f} / {g(0.5):.4f} / {g(1.0):.4f}  -> P x {g(0.0) ** 2:.4f} at z 0")

if not MUT:
    k1 = abs(G["zero conversion (K1)"]["g0"] - 1) < 1e-8
    # K2: reference growth shape vs the scorer's Dgrow
    P(f"  K1 zero conversion g == 1: {k1} (|g0 - 1| = {abs(G['zero conversion (K1)']['g0'] - 1):.1e})")

# ---------------------------------------------------------------- G2 rescore with CFG650's scorer
SRC650 = open(os.path.join(C650, "cfg650_native.py")).read()
INJ_LOOP = "for foot, F, S, N, L in runs_list():\n"
assert SRC650.count(INJ_LOOP) == 1
SCALE = '''for foot, F, S, N, L in runs_list():
    for _k, _v in F["snap"].items():                                  # CFG780 injection: framework P_grav x g(z)^2
        if "P_grav" in _v:
            _z = float(_v.get("z", {"z0": 0.0, "z0.5": 0.5, "z1": 1.0}.get(_k, 0.0)))
            _v["P_grav"] = list(np.array(_v["P_grav"]) * CFG780_G(_z) ** 2)
'''
OUTW_OLD = 'json.dump(RESULT, open(os.path.join(HERE, f"cfg650_native_results{SUF}.json"), "w"), indent=1)\nopen(os.path.join(HERE, f"cfg650_native{SUF}.out"), "w").write("\\n".join(OUT) + "\\n")'
assert SRC650.count(OUTW_OLD) == 1
OUTW_NEW = 'json.dump(RESULT, open(os.path.join(CFG780_DIR, f"rescore_{CFG780_TAG}{SUF}.json"), "w"), indent=1)\nopen(os.path.join(CFG780_DIR, f"rescore_{CFG780_TAG}{SUF}.out"), "w").write("\\n".join(OUT) + "\\n")'
MOD = SRC650.replace(INJ_LOOP, SCALE).replace(OUTW_OLD, OUTW_NEW)


def rescore(gfun, tag, jobset):
    env_backup = dict(os.environ)
    if jobset == "T12":
        os.environ["CFG650_JOBSET"] = "T12"
    else:
        os.environ.pop("CFG650_JOBSET", None)
    os.environ.pop("CFG596_MUTATE", None)
    ns = {"__file__": os.path.join(C650, "cfg650_native.py"), "__name__": "cfg650_rescore", "CFG780_G": gfun,
          "CFG780_DIR": HERE, "CFG780_TAG": tag}
    argv0 = sys.argv
    sys.argv = [argv0[0]]
    try:
        exec(compile(MOD, "cfg650_native_mod", "exec"), ns)
    finally:
        sys.argv = argv0
        os.environ.clear(); os.environ.update(env_backup)
    return ns["RESULT"], ns


def summary(R):
    out = {}
    for n, r in R["runs"].items():
        s = r["surveys"].get("KiDS") or next(iter(r["surveys"].values()))
        fi = s["fits"]["IA"]
        out[n] = dict(chi2_F=fi["F"]["chi2"], chi2_S0=fi["S0"]["chi2"], dchi2=s["dchi2"], p_F=s["p_F"], p_S0=s["p_S0"], cls=s.get("class"))
    return out


RES = {"lane": "CFG780", "mutate": MUT, "growth": {k: {kk: vv for kk, vv in v.items() if kk != "fn"} for k, v in G.items()}, "rescore": {}}
import glob
W650 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data", "cfg650_work")
jobs = ["T12"] + (["T1x"] if glob.glob(os.path.join(W650, "T1x", "cfg650_*_RES_*.json")) else [])
for job in jobs:
    P(f"\n=== rescore {job}")
    R0, ns0 = rescore(lambda z: 1.0, f"{job}_unscaled", job)
    base = summary(R0)
    if not MUT and job == "T12":
        aa = np.array([1.0, 1 / 1.5, 0.5]); dr = np.interp(np.log(aa), np.log(AA), D_R) / D_R[-1]
        dg = np.array([ns0["Dgrow"](a) for a in aa]) / ns0["Dgrow"](1.0)
        k2 = float(np.max(np.abs(dr / dg - 1)))
        P(f"  K2 reference growth shape vs scorer Dgrow at z 0/0.5/1: max rel {k2:.4f} -> {'PASS' if k2 <= 0.01 else 'FAIL'}")
        RES["K2"] = k2
    P(f"  unscaled: {base}")
    RES["rescore"][f"{job}|unscaled"] = base
    if not MUT and job == "T12":
        stored = json.load(open(os.path.join(C650, "cfg650_native_results_T12.json")))
        st = summary(stored)
        k1r = all(abs(base[n]["chi2_F"] - st[n]["chi2_F"]) < 1e-6 for n in base if n in st)
        P(f"  K1 rescore reproduces stored T12 chi2: {k1r}")
        RES["K1_rescore"] = bool(k1r)
    for lab, v in G.items():
        if "zero conversion" in lab:
            continue
        sc = summary(rescore(v["fn"], f"{job}_{lab.split()[0]}", job)[0])
        RES["rescore"][f"{job}|{lab}"] = sc
        for n in sc:
            d_abs = sc[n]["chi2_F"] - base[n]["chi2_F"]
            cls = "IMPROVES" if d_abs <= -4 else ("WORSENS" if d_abs >= 4 else "NEUTRAL")
            sc[n]["d_abs"] = d_abs; sc[n]["class_abs"] = cls
            P(f"  {lab:42s} {n}: chi2_F {base[n]['chi2_F']:.2f} -> {sc[n]['chi2_F']:.2f} (d_abs {d_abs:+.2f}, {cls}); p_F {sc[n]['p_F']:.3f}; "
              f"dchi2 vs S0 {sc[n]['dchi2']:+.2f} ({sc[n]['cls']})")
json.dump(RES, open(os.path.join(HERE, f"cfg780_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg780{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
