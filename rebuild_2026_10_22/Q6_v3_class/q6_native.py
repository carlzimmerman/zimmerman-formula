#!/usr/bin/env python3
"""Q6_v3_class steps B, N, C (FROZEN_CRITERIA sections 7-9 + AMENDMENTS A1-A3): v3's literal background, v3's native
TT/TE/EE/phiphi, P(k), sigma8/S8 from the validated Khronon CLASS (LOB model), Gauss-Newton fits to plik-lite + low-l
(C2's numpy likelihood, executed read-only), and the comparison with F3's sub-horizon ODE. Numbers only; the frozen
readings are step B's literal-background class and step C's CONFIRMED / CONFIRMED, WEAKER / NOT CONFIRMED.

a0 is absent at linear order (q6_derive D0): neither footing enters; kappa = 1/2 FITTED does not enter.
omega_K (the khronon dust abundance, the shift charge I0) is a FITTED initial condition.
Run: OMP_NUM_THREADS=1 nice -n 19 python3 -I q6_native.py   (Q6_MUTATE=1: sign-flipped plik-lite data vector and the
MUTATE binary, no fits -> *_MUTATE.out/json; K0a and N0 must FAIL)
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.io import FortranFile

T0 = time.time()
MUT = os.environ.get("Q6_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
BLD = os.path.join(EXT, "class_khronon_build_2026_10_23")
KHR = os.path.join(BLD, "class_khronon_mutate" if MUT else "class_khronon", "class")
RUNS = os.path.join(BLD, f"runs_native{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"q6_native{TAG}.out"), "w")
RES = {"mutate": MUT, "checks": {}, "note": "numbers only; a0 absent at linear order; omega_K FITTED; model LOB (A2)"}
NP = NC = 0


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, ok, value, thr):
    global NP, NC
    NC += 1
    NP += bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}")
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}


def save():
    RES["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(RES, open(os.path.join(HERE, f"q6_native_results{TAG}.json"), "w"), indent=1, default=float)


# ------------------------------------------------------------------ C2's likelihood, executed read-only from its file
C2 = os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology")
src = open(os.path.join(C2, "c2b_native_cmb.py")).read()
blk = src[src.index("# ---------------------------------------------------------------- likelihoods"):
          src.index("# ---------------------------------------------------------------- CLASS emulation")]
NS = {"np": np, "math": math, "os": os, "EXT": EXT, "FortranFile": FortranFile,
      "InterpolatedUnivariateSpline": InterpolatedUnivariateSpline}
exec(compile(blk, "c2b_native_cmb.py[likelihoods]", "exec"), NS)
if MUT:
    NS["Xd"] = -NS["Xd"]
C2RES = json.load(open(os.path.join(C2, "c2b_native_cmb_results.json")))["P5"]
TAU_HAT, SIG_TAU = C2RES["tau_hat"], C2RES["sig_tau"]
C7F = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")))["fits"]["LCDM"]
P0 = np.array([C7F["params"][k] for k in ("omega_b", "omega_dm(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau")])
A0 = C7F["A_planck"]
P(f"== Q6 steps B/N/C: C2 likelihood loaded; tau prior {TAU_HAT:.4f} +- {SIG_TAU:.4f}; start = C7 LCDM refit "
  f"{np.round(P0, 6).tolist()}, A_planck {A0:.6f} (C7 chi2 {C7F['chi2']['total']:.2f})")

# ------------------------------------------------------------------ CLASS runner (C7 high precision + start x0.25, A3)
ENV = dict(os.environ, OMP_NUM_THREADS="1")
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
TCMB = 2.7255
OMCDM = 1e-8
HREF = 0.67552
NRUN = [0]
FAILMSG = {}


def run(name, binary, params, pk=False):
    p = {"output": "tCl,pCl,lCl,mPk" if pk else "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": 2508,
         "T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2,
         "fourier_verbose": 1, "overwrite_root": "yes", **HIGH, **START, **params}
    if pk:
        p["P_k_max_h/Mpc"] = 10.0
    root = os.path.join(RUNS, name + "_")
    p["root"] = root
    with open(root + ".ini", "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    t_launch = time.time()
    r = subprocess.run(["nice", "-n", "19", binary, root + ".ini"], capture_output=True, text=True, env=ENV)
    NRUN[0] += 1
    if r.returncode != 0:
        FAILMSG[name] = (r.stdout + r.stderr).strip().splitlines()[-1][-300:]
        return None
    assert os.path.getmtime(root + "_cl_lensed.dat") >= t_launch - 1, "stale-output guard"
    log = r.stdout
    cl = np.loadtxt(root + "_cl_lensed.dat")
    L = int(cl[-1, 0])
    f = (TCMB * 1e6) ** 2
    out = {}
    for key, col in (("tt", 1), ("ee", 2), ("te", 3), ("pp", 5)):
        arr = np.zeros(L + 1)
        arr[cl[:, 0].astype(int)] = cl[:, col] * (f if key != "pp" else 1.0)
        out[key] = arr
    m = re.search(r"found 'h = ([0-9.eE+-]+)'", log)
    out["h"] = float(m.group(1)) if m else float(p.get("h", np.nan))
    m = re.search(r"sigma8=([0-9.]+) for total matter", log)
    out["sigma8"] = float(m.group(1)) if m else np.nan
    m = re.search(r"Non-relativistic\s+Omega = ([0-9.eE+-]+)", log)
    out["Omega_m"] = float(m.group(1)) if m else np.nan
    if pk:
        out["pk"] = np.loadtxt(root + "_pk.dat")
    return out


# ------------------------------------------------------------------ models
GRID = (14.8, 50.0, 150.0, 361.0, 1000.0, 2542.0)                    # h/Mpc (fixed in Mpc^-1 via HREF)
KH = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0}


def kmodel(ktype, mu_h=None):
    return {**KH, "aest_K_type": ktype, "aest_K2": 1.0 if mu_h is None else (mu_h * HREF) ** 2}


MODELS = {"LCDM": None, "DUST": kmodel(0)}
for mu in GRID:
    MODELS[f"LOB_{mu:g}"] = kmodel(4, mu)
RES["models"] = MODELS
RES["mu_grid_hMpc"] = GRID
RES["mu_grid_per_Mpc"] = [mu * HREF for mu in GRID]


def params(model, p):
    wb, wd, th, lnA, ns, tau = p
    base = {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau}
    if model is None:
        return VAN, {**base, "omega_cdm": wd}
    return KHR, {**base, "omega_cdm": OMCDM, "omega_aest": wd - OMCDM, **model}


def theory(mname, p, pk=False, tag="fit"):
    b, pr = params(MODELS[mname], p)
    o = run(f"{mname}_{tag}", b, pr, pk=pk)
    if o is None:
        return None, None
    return NS["binned"](o["tt"], o["te"], o["ee"]), o


def chi2_parts(Tb, o, A):
    c = {"plik": NS["chi2_plik"](Tb, A), "lowTT": NS["chi2_lowTT"](o["tt"], A), "lowEE": NS["chi2_lowEE"](o["ee"], A),
         "Aprior": ((A - 1) / 0.0025) ** 2}
    c["total"] = sum(c.values())
    return c


def resid(Tb, A, tau):
    return np.concatenate((np.linalg.solve(NS["Lc"], NS["Xd"] - Tb / A**2), [(A - 1) / 0.0025, (tau - TAU_HAT) / SIG_TAU]))


STEP = np.array([1e-4, 1e-3, 2e-4, 0.01, 0.004, 0.004])                 # C2's / C7's steps


def gauss_newton(mname, p, A, nit=4, budget=150):
    n0 = NRUN[0]
    for it in range(nit):
        Tb, _ = theory(mname, p)
        r = resid(Tb, A, p[5])
        c0 = r @ r
        J = np.zeros((615, 7))
        for kx in range(6):
            pp = p.copy()
            pp[kx] += STEP[kx]
            Tk, _ = theory(mname, pp, tag="jac")
            J[:613, kx] = -np.linalg.solve(NS["Lc"], (Tk - Tb) / A**2) / STEP[kx]
        J[614, 5] = 1 / SIG_TAU
        J[:613, 6] = np.linalg.solve(NS["Lc"], 2 * Tb / A**3)
        J[613, 6] = 1 / 0.0025
        d = -np.linalg.lstsq(J, r, rcond=None)[0]
        lam = 1.0
        while True:
            pn, An = p + lam * d[:6], A + lam * d[6]
            Tn, _ = theory(mname, pn, tag="ls")
            cn = np.inf if Tn is None else resid(Tn, An, pn[5]) @ resid(Tn, An, pn[5])
            if cn <= c0 or lam < 1 / 16:
                break
            lam /= 2
        if cn <= c0:
            p, A = pn, An
        P(f"    {mname}: GN it{it + 1}: steered chi2 {c0:.2f} -> {min(cn, c0):.2f} (step {lam}); runs {NRUN[0] - n0}")
        if NRUN[0] - n0 > budget - 10 or abs(c0 - cn) < 0.05:
            break
    return p, A, NRUN[0] - n0


KREP = (0.1, 0.3, 1.0, 3.0, 10.0)


def kgrid_ratio(o, oref, ks=KREP):
    a, b = o["pk"], oref["pk"]
    la = np.interp(np.log(ks), np.log(a[:, 0]), np.log(a[:, 1]))
    lb = np.interp(np.log(ks), np.log(b[:, 0]), np.log(b[:, 1]))
    return {f"{k_:g}": float(np.exp(x - y)) for k_, x, y in zip(ks, la, lb)}


def spec_diff(o, oref):
    m = np.arange(len(oref["tt"])) >= 2
    return {"TT": float(np.max(np.abs(o["tt"][m] / oref["tt"][m] - 1))),
            "EE": float(np.max(np.abs(o["ee"][m] / oref["ee"][m] - 1))),
            "TE": float(np.max(np.abs(o["te"][m] - oref["te"][m]) / np.sqrt(oref["tt"][m] * oref["ee"][m]))),
            "pp": float(np.max(np.abs(o["pp"][m] / oref["pp"][m] - 1)))}


def tt_ratios(o, oref, ells=(10, 100, 220, 540, 810, 1000, 1500, 2000)):
    return {str(l): float(o["tt"][l] / oref["tt"][l]) for l in ells}


W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3


def sig8_own(pk):
    ks, P_ = pk[:, 0], pk[:, 1]
    return math.sqrt(np.trapz(P_ * W8(ks * 8.0) ** 2 * ks ** 2, ks) / (2 * math.pi ** 2))


# ------------------------------------------------------------------ K0a: C7's LCDM refit reproduced (pristine binary)
Tb, o = theory("LCDM", P0, tag="K0a")
cK0 = chi2_parts(Tb, o, A0)
check("K0a_C7_LCDM_reproduced", abs(cK0["total"] - C7F["chi2"]["total"]) <= 2.0,
      f"total chi2 {cK0['total']:.2f} vs C7 {C7F['chi2']['total']:.2f} (this lane's precision: C7 A2 + start x0.25)",
      "|diff| <= 2")
RES["K0a"] = cK0
if MUT:
    vl = run("N0_mut_lcdm", VAN, params(None, P0)[1], pk=True)
    vd = run("N0_mut_dust", KHR, params(MODELS["DUST"], P0)[1], pk=True)
    ok = vl is not None and vd is not None and abs(vd["sigma8"] / vl["sigma8"] - 1) <= 1e-3
    check("N0_dust_equals_LCDM", ok, f"MUTATE binary: DUST sigma8 {vd['sigma8'] if vd else None} vs LCDM "
          f"{vl['sigma8'] if vl else None}", "|ratio-1| <= 1e-3")
    save()
    P(f"Q6_NATIVE COMPLETE: {NP}/{NC} checks PASS.")
    sys.exit(0 if NP == NC else 1)

# ------------------------------------------------------------------ K0b: F3's sub-horizon ODE reproduced (F3 K4)
from classy import Class                                               # noqa: E402 (as F3; one in-process CLASS run)


def make_E(Om, h, rad=True):                                           # verbatim from F3 f3_growth_audit.py
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL)), Or


def growth_ratio(kk, mu_h, Om, Ob, h, kernel="jeans", a_i=1e-3, rad=True):   # verbatim from F3
    Ek, Or = make_E(Om, h, rad); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)
    def s_of(a, mu):
        if mu is None: return np.ones(n)
        x2 = (kk / (a * mu)) ** 2
        return (1.0 - x2) if kernel == "jeans" else 1.0 / (1.0 + x2)
    def solve(mu):
        def rhs(x, st):
            a = math.exp(x); E = Ek(a); eps = 1e-6
            dlnE = (math.log(Ek(a * math.exp(eps))) - math.log(Ek(a * math.exp(-eps)))) / (2 * eps)
            dens = 1.5 * a ** -3 / E ** 2
            db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
            src_b = dens * (Ob * db + OK * dk); src_k = dens * (Ob * db + OK * dk * s_of(a, mu))
            return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE) * gk + src_k])
        st0 = np.concatenate([np.full(n, a_i), np.full(n, a_i), np.full(n, a_i), np.full(n, a_i)])
        sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12)
        y_ = sol.y[:, -1]; return (Ob * y_[:n] + OK * y_[2 * n:3 * n]) / Om
    return solve(mu_h) / solve(None)


KS = np.geomspace(1e-4, 50.0, 1500)
KT = np.geomspace(1e-3, 3.0, 36)


def sig8_F3(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(np.trapz(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))


def sig8_ratio_F3(Pk, mu_h, Om, Ob, h, kernel, a_i):
    T = growth_ratio(KT, mu_h, Om, Ob, h, kernel, a_i)
    Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8_F3(Pk, Tf) / sig8_F3(Pk), T


F3R = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json")))
pA = F3R["K2"]["A_c2b_refit"]["params"]
cA = Class()
cA.set({"omega_b": pA["omega_b"], "omega_cdm": pA["omega_cdm"], "h": pA["h"], "ln10^{10}A_s": pA["lnAs"],
        "n_s": pA["n_s"], "tau_reio": pA["tau"], "N_ur": 3.044, "T_cmb": 2.7255, "output": "mPk",
        "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0})
cA.compute()
PkA = np.array([cA.pk_lin(k * pA["h"], 0.0) for k in KS]) * pA["h"] ** 3
OmA, ObA = (pA["omega_b"] + pA["omega_cdm"]) / pA["h"] ** 2, pA["omega_b"] / pA["h"] ** 2
cA.struct_cleanup()
MU_F3 = F3R["K4"]["BS24_Eq39_edge_100kpc"]["mu_hMpc"]
K0b = {}
for kern, ai in (("bsk2", 1e-3), ("bsk2", 1e-4), ("jeans", 1e-3)):
    r_, _ = sig8_ratio_F3(PkA, MU_F3, OmA, ObA, pA["h"], kern, ai)
    rec = F3R["K4"]["BS24_Eq39_edge_100kpc"][f"{kern}_ai{ai:g}"]["sigma8_ratio"]
    K0b[f"{kern}_ai{ai:g}"] = {"this": r_, "F3": rec, "rel": abs(r_ / rec - 1)}
check("K0b_F3_reproduced", all(v["rel"] <= 1e-3 for v in K0b.values()),
      "; ".join(f"{k}: {v['this']:.5f} vs F3 {v['F3']:.5f}" for k, v in K0b.items()),
      "each <= 1e-3 relative (F3's committed JSON; the frozen text's 0.20313 is a slip for F3's 0.202602)")
RES["K0b"] = K0b
save()

# ------------------------------------------------------------------ step B: the literal background (LIT)
P("== step B: literal quadratic-K background (LIT) at the grid mu_K, omega_K = C7 refit omega_dm, h = 0.67552")
HUB = 1.0 / 2997.92458                                                 # Mpc^-1 per (100 km/s/Mpc)
H0 = HREF * HUB
OMK = P0[1] / HREF**2
OMG = 2.4728e-5 * (TCMB / 2.7255) ** 4 / HREF**2 * 1.0                   # photons (T_cmb 2.7255)
OMR = OMG * (1 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3))
TMEV0 = 8.617333e-11 * TCMB                                            # T0 in MeV


def a_of_T(T_MeV, gs):
    return (TMEV0 / T_MeV) * (3.909 / gs) ** (1 / 3)


BBN = {"1MeV": (a_of_T(1.0, 10.75), 10.75 / (2 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3) * 2) * (3.909 / 10.75) ** (4 / 3), 10.75 / 1.75),
       "0.07MeV": (a_of_T(0.07, 3.909), 1.0, (1 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3)) / (7 / 8 * (4 / 11) ** (4 / 3)))}
LIT = {}
for mu in GRID:
    m2 = (mu * HREF) ** 2
    I0 = 6 * H0**2 * OMK / (math.sqrt(1 + 3 * H0**2 * OMK / m2) + 1)   # root of I0 + I0^2/(4 mu^2) = 3 H0^2 Om_K (no cancellation)
    eps0 = I0 / (2 * m2)
    rhoK = lambda a: (I0 / a**3) * (1 + I0 / (4 * m2 * a**3))
    rhoR = lambda a: 3 * H0**2 * OMR / a**4
    a_st = eps0 ** (1 / 3)
    a_eq = math.sqrt(I0**2 / (12 * m2 * H0**2 * OMR))
    row = {"mu_per_Mpc": mu * HREF, "eps0": eps0, "z_stiff_eps1": 1 / a_st - 1, "z_stiff_equals_radiation": 1 / a_eq - 1,
           "eps_rec_z1090": eps0 * 1091**3, "rho_stiff_over_dust_rec": eps0 * 1091**3 / 2}
    for lab, (aT, fr, nrel) in BBN.items():
        ratio = rhoK(aT) / (rhoR(aT) * fr)
        row[f"rhoK_over_rhor_{lab}"] = ratio
        row[f"dNeff_equiv_{lab}"] = ratio * nrel
    # CLASS's own start test on the literal model
    b, pr = params(kmodel(3, mu), P0)
    oL = run(f"LIT_{mu:g}", b, pr)
    row["class_runs"] = oL is not None
    row["class_message"] = FAILMSG.get(f"LIT_{mu:g}", "ran")
    row["reading"] = "NO RADIATION ERA (BBN-EXCLUDED)" if row["dNeff_equiv_1MeV"] > 0.5 else "VIABLE BACKGROUND"
    LIT[f"{mu:g}"] = row
    P(f"  mu {mu:g} h/Mpc: z(eps=1) {row['z_stiff_eps1']:.4g}; stiff = radiation at z {row['z_stiff_equals_radiation']:.4g}; "
      f"rho_K/rho_r: 1 MeV {row['rhoK_over_rhor_1MeV']:.3g}, 0.07 MeV {row['rhoK_over_rhor_0.07MeV']:.3g}; "
      f"dNeff,equiv(1 MeV) {row['dNeff_equiv_1MeV']:.3g}; eps(rec) {row['eps_rec_z1090']:.3g}; CLASS: {row['class_message'][-110:]}; "
      f"{row['reading']}")
# mu_K,BBN: dNeff_equiv(1 MeV) = 0.5 (the stiff term dominates rho_K there; root on the exact expression)
from scipy.optimize import brentq                                       # noqa: E402


def dneff1(lmu):
    m2 = (10**lmu) ** 2
    I0 = 6 * H0**2 * OMK / (math.sqrt(1 + 3 * H0**2 * OMK / m2) + 1)
    aT, fr, nrel = BBN["1MeV"]
    return (I0 / aT**3) * (1 + I0 / (4 * m2 * aT**3)) / (3 * H0**2 * OMR / aT**4 * fr) * nrel - 0.5


lmu_bbn = brentq(dneff1, 0.0, 15.0, xtol=1e-6)
RES["stepB"] = {"rows": LIT, "mu_K_BBN_per_Mpc": 10**lmu_bbn, "mu_K_BBN_hMpc": 10**lmu_bbn / HREF,
                "gap_over_BS_cap": 10**lmu_bbn / HREF / 14.8, "a_1MeV": BBN["1MeV"][0], "a_0.07MeV": BBN["0.07MeV"][0]}
check("B_literal_background", all(np.isfinite(r["dNeff_equiv_1MeV"]) for r in LIT.values()),
      f"readings {[r['reading'] for r in LIT.values()]}; CLASS ran LIT at {[k for k, r in LIT.items() if r['class_runs']]}; "
      f"mu_K,BBN = {10**lmu_bbn / HREF:.3e} h/Mpc ({10**lmu_bbn / HREF / 14.8:.2e} x the BS cap)", "computed")
save()

# ------------------------------------------------------------------ step N (a): fixed parameters (C7 LCDM refit)
P("== step N (a): fixed parameters = C7 LCDM refit (omega_K = omega_dm, FITTED value of LCDM), A_planck = C7's")
FIX = {}
for mname, model in MODELS.items():
    Tb, o = theory(mname, P0, pk=True, tag="fix")
    if o is None:
        FIX[mname] = {"failed": FAILMSG.get(f"{mname}_fix")}
        P(f"  {mname}: CLASS failed: {FIX[mname]['failed']}")
        continue
    c = chi2_parts(Tb, o, A0)
    row = {"chi2": c, "H0": 100 * o["h"], "sigma8": o["sigma8"], "sigma8_own": sig8_own(o["pk"]), "Omega_m": o["Omega_m"],
           "S8": o["sigma8"] * math.sqrt(o["Omega_m"] / 0.3), "_o": o}
    FIX[mname] = row
dref = FIX["DUST"]["_o"]
for mname, row in FIX.items():
    if "failed" in row:
        continue
    o = row["_o"]
    if mname not in ("LCDM", "DUST"):
        row["R_B"] = o["sigma8"] / dref["sigma8"]
        row["Pk_over_DUST"] = kgrid_ratio(o, dref)
        row["Cl_vs_DUST_maxrel"] = spec_diff(o, dref)
        row["TT_over_DUST_at_l"] = tt_ratios(o, dref)
    if mname == "DUST":
        row["vs_LCDM"] = spec_diff(o, FIX["LCDM"]["_o"])
    c = row["chi2"]
    P(f"  {mname}: chi2 {c['total']:.2f} (plik {c['plik']:.2f}, lowTT {c['lowTT']:.2f}, lowEE {c['lowEE']:.2f}); "
      f"sigma8 {row['sigma8']:.4f} (own {row['sigma8_own']:.4f}); S8 {row['S8']:.4f}; Omega_m {row['Omega_m']:.4f}"
      + ("" if "R_B" not in row else f"; R_B {row['R_B']:.4f}; P/P_DUST at k[h/Mpc] "
         + ", ".join(f"{k_}: {v:.3e}" for k_, v in row["Pk_over_DUST"].items())
         + "; TT/TT_DUST at l " + ", ".join(f"{k_}: {v:.3f}" for k_, v in row["TT_over_DUST_at_l"].items())))
RUNAWAY = [m for m, r in FIX.items() if m not in ("LCDM", "DUST") and ("failed" in r or not math.isfinite(r["chi2"]["total"])
                                                                       or max(r["Pk_over_DUST"].values()) > 10)]
RES["runaway"] = RUNAWAY
RES["fixed"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIX.items()}
check("N1_fixed_runs", all("failed" not in FIX[m] for m in MODELS) and
      abs(FIX["DUST"]["sigma8"] / FIX["LCDM"]["sigma8"] - 1) <= 1e-3,
      f"all fixed runs complete; DUST/LCDM sigma8 {FIX['DUST']['sigma8'] / FIX['LCDM']['sigma8']:.6f}; RUNAWAY {RUNAWAY}",
      "complete; DUST = LCDM to 1e-3")
save()

# ------------------------------------------------------------------ step C: comparison with F3's ODE at these parameters
P("== step C: R_B (Boltzmann, LOB) vs R_F3 (F3's ODE, BSK2 kernel, a_i = 1e-3 / 1e-4) at the same parameters")
hF = FIX["LCDM"]["h"] if "h" in FIX["LCDM"] else FIX["LCDM"]["H0"] / 100
OmF = (P0[0] + P0[1]) / hF**2
ObF = P0[0] / hF**2
pkD = dref["pk"]
PkF = np.exp(np.interp(np.log(KS), np.log(pkD[:, 0]), np.log(pkD[:, 1]), right=-np.inf))   # zero beyond 10 h/Mpc
CMP = {}
for mu in GRID:
    rb = FIX[f"LOB_{mu:g}"]["R_B"]
    r3 = {f"bsk2_ai{ai:g}": sig8_ratio_F3(PkF, mu, OmF, ObF, hF, "bsk2", ai)[0] for ai in (1e-3, 1e-4)}
    CMP[f"{mu:g}"] = {"R_B": rb, **{f"R_F3_{k}": v for k, v in r3.items()}}
    P(f"  mu {mu:g} h/Mpc: R_B {rb:.4f}; R_F3 bsk2 a_i=1e-3 {r3['bsk2_ai0.001']:.4f}, a_i=1e-4 {r3['bsk2_ai0.0001']:.4f}")
cap = CMP["14.8"]
if cap["R_B"] <= cap["R_F3_bsk2_ai0.001"]:
    reading = "CONFIRMED"
elif cap["R_B"] < 0.95:
    reading = "CONFIRMED, WEAKER"
else:
    reading = "NOT CONFIRMED"
lm = np.log(np.array(GRID))
rb_arr = np.array([CMP[f"{mu:g}"]["R_B"] for mu in GRID])
if rb_arr.max() < 0.95:
    mu_min_B = None
    mu_min_txt = f"beyond the grid (R_B({GRID[-1]:g}) = {rb_arr[-1]:.4f} < 0.95)"
else:
    i = int(np.argmax(rb_arr >= 0.95))
    if i == 0:
        mu_min_B, mu_min_txt = GRID[0], "at or below the BS cap"
    else:
        f_ = (math.log(0.95) - math.log(rb_arr[i - 1])) / (math.log(rb_arr[i]) - math.log(rb_arr[i - 1]))
        mu_min_B = float(math.exp(lm[i - 1] + f_ * (lm[i] - lm[i - 1])))
        mu_min_txt = f"{mu_min_B:.4g} h/Mpc (log-log interpolation between {GRID[i - 1]:g} and {GRID[i]:g})"
RES["stepC"] = {"table": CMP, "reading_at_BS_cap": reading, "mu_min_B_hMpc": mu_min_B, "mu_min_B_text": mu_min_txt,
                "F3_mu_min_hMpc": [361, 2542], "BS_cap_hMpc": 14.8}
check("C_reading", reading in ("CONFIRMED", "CONFIRMED, WEAKER", "NOT CONFIRMED"),
      f"at mu_K = 14.8 h/Mpc: R_B {cap['R_B']:.4f} vs R_F3(a_i=1e-3) {cap['R_F3_bsk2_ai0.001']:.4f} -> {reading}; "
      f"mu_min,B (R_B = 0.95): {mu_min_txt}", "computed (the reading is a result)")
save()

# ------------------------------------------------------------------ step N (b): fits
P("== step N (b): fits to plik-lite TTTEEE + low-l TT + low-l EE (C2 likelihood; C7's Gauss-Newton, start = C7 LCDM refit)")
FIT = {}
for mname, model in MODELS.items():
    if mname in RUNAWAY or mname == "DUST":
        continue
    pb, Ab, nr = gauss_newton(mname, P0.copy(), A0)
    Tb, o = theory(mname, pb, pk=True, tag="best")
    c = chi2_parts(Tb, o, Ab)
    FIT[mname] = {"params": dict(zip(("omega_b", "omega_K(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau"), pb.tolist())),
                  "A_planck": Ab, "chi2": c, "H0": 100 * o["h"], "sigma8": o["sigma8"], "Omega_m": o["Omega_m"],
                  "S8": o["sigma8"] * math.sqrt(o["Omega_m"] / 0.3), "class_runs": nr, "_o": o}
    P(f"  {mname}: chi2 {c['total']:.2f} (plik {c['plik']:.2f}, lowTT {c['lowTT']:.2f}, lowEE {c['lowEE']:.2f}); "
      f"H0 {FIT[mname]['H0']:.2f}, sigma8 {o['sigma8']:.4f}, Omega_m {o['Omega_m']:.4f}, S8 {FIT[mname]['S8']:.4f}; "
      f"params {np.round(pb, 5).tolist()}, A {Ab:.5f}; {nr} runs")
    RES["fits"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIT.items()}
    save()
for mname in FIT:
    FIT[mname]["dchi2_vs_LCDM"] = FIT[mname]["chi2"]["total"] - FIT["LCDM"]["chi2"]["total"]
    if mname != "LCDM":
        FIT[mname]["Pk_over_LCDM_bestfits"] = kgrid_ratio(FIT[mname]["_o"], FIT["LCDM"]["_o"])
        FIT[mname]["TT_over_LCDM_bestfits_at_l"] = tt_ratios(FIT[mname]["_o"], FIT["LCDM"]["_o"])
RES["fits"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIT.items()}
P("== summary (numbers only): model | Delta chi2 vs LCDM refit | H0 | sigma8 | S8 | P/P_LCDM(best fits) at k = "
  + ", ".join(f"{k_:g}" for k_ in KREP) + " h/Mpc")
for mname, f in RES["fits"].items():
    pkr = f.get("Pk_over_LCDM_bestfits", {})
    P(f"  {mname:12s} {f['dchi2_vs_LCDM']:+10.2f}  H0 {f['H0']:.2f}  sigma8 {f['sigma8']:.4f}  S8 {f['S8']:.4f}  "
      + " ".join(f"{v:.3e}" for v in pkr.values()))
check("N2_fits", 500 <= RES["fits"]["LCDM"]["chi2"]["plik"] <= 750 and all(math.isfinite(f["chi2"]["total"]) for f in RES["fits"].values()),
      f"LCDM refit chi2_plik {RES['fits']['LCDM']['chi2']['plik']:.1f}; all fits finite", "plik in [500, 750]; finite")
RES["class_runs_total"] = NRUN[0]
save()
P(f"  CLASS runs: {NRUN[0]}; elapsed {time.time() - T0:.0f} s")
P(f"Q6_NATIVE COMPLETE: {NP}/{NC} checks PASS.")
OUT.close()
sys.exit(0 if NP == NC else 1)
