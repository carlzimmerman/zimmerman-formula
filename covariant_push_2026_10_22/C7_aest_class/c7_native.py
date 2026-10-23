#!/usr/bin/env python3
"""C7_aest_class step N: AeST's own TT/TE/EE/phiphi and P(k) from the validated patched CLASS, and fits to Planck
plik-lite + low-l with C2's numpy likelihood (FROZEN_CRITERIA step N + AMENDMENTS A2, A3). Numbers only, no verdict.

The a0 sector is absent at linear order on FRW: this tests AeST's dust and gravity sectors (and G_cosmo/G_N) only.
Omega_aest (omega_aest) is the shift charge I0, a FITTED initial condition.  kappa = 1/2 FITTED (does not enter).

Run: OMP_NUM_THREADS=1 nice -n 19 python3 -I c7_native.py      (C7_MUTATE=1: sanity checks with a sign-flipped data
vector and the MUTATE binary, no fits -> *_MUTATE.out/json)
"""
import json
import math
import os
import re
import subprocess
import sys
import time

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.io import FortranFile

T0 = time.time()
MUT = os.environ.get("C7_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
BLD = os.path.join(EXT, "class_aest_build_2026_10_22")
VAN = os.path.join(BLD, "class_vanilla", "class")
AEST = os.path.join(BLD, "class_aest_mutate" if MUT else "class_aest", "class")
RUNS = os.path.join(BLD, f"runs_native{TAG}")
import shutil
shutil.rmtree(RUNS, ignore_errors=True)   # fresh run directory
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"c7_native{TAG}.out"), "w")
RES = {"mutate": MUT, "checks": {}, "note": "numbers only; a0 absent at linear order; Omega_aest FITTED"}
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
    json.dump(RES, open(os.path.join(HERE, f"c7_native_results{TAG}.json"), "w"), indent=1, default=float)


# ------------------------------------------------------------------ C2's likelihood, executed read-only from its file
C2 = os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology")
src = open(os.path.join(C2, "c2b_native_cmb.py")).read()
blk = src[src.index("# ---------------------------------------------------------------- likelihoods"):
          src.index("# ---------------------------------------------------------------- CLASS emulation")]
NS = {"np": np, "math": math, "os": os, "EXT": EXT, "FortranFile": FortranFile,
      "InterpolatedUnivariateSpline": InterpolatedUnivariateSpline}
exec(compile(blk, "c2b_native_cmb.py[likelihoods]", "exec"), NS)
if MUT:
    NS["Xd"] = -NS["Xd"]                       # MUTATE: sign-flipped plik-lite data vector
C2RES = json.load(open(os.path.join(C2, "c2b_native_cmb_results.json")))["P5"]
TAU_HAT, SIG_TAU = C2RES["tau_hat"], C2RES["sig_tau"]
P0 = np.array(C2RES["lcdm_refit"]["params"])
A0 = C2RES["lcdm_refit"]["A"]
P(f"== C7 step N: C2 likelihood block loaded; tau prior {TAU_HAT:.4f} +- {SIG_TAU:.4f} (C2's low-l scan); "
  f"start = C2 LCDM refit {np.round(P0, 5).tolist()}, A_planck {A0:.5f}")

# ------------------------------------------------------------------ CLASS runner
ENV = dict(os.environ, OMP_NUM_THREADS="1")
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}                            # A2
TCMB = 2.7255
OMCDM = 1e-8
NRUN = [0]


def run(name, binary, params, pk=False):
    p = {"output": "tCl,pCl,lCl,mPk" if pk else "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": 2508,
         "T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2,
         "fourier_verbose": 1, "overwrite_root": "yes", **HIGH, **params}   # overwrite_root: never read stale _00_ files
    if pk:
        p["P_k_max_h/Mpc"] = 10.0
    root = os.path.join(RUNS, name + "_")
    p["root"] = root
    ini = root + ".ini"
    with open(ini, "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    t_launch = time.time()
    r = subprocess.run(["nice", "-n", "19", binary, ini], capture_output=True, text=True, env=ENV)
    NRUN[0] += 1
    if r.returncode != 0:
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
    m = re.search(r"AeST: K_type=\d+, I0 = ([0-9.eE+-]+) Mpc\^-1, Q\(1\) = ([0-9.eE+-]+), ca2\(1\) = ([0-9.eE+-]+)", log)
    if m:
        out["I0"], out["Q1"], out["ca2_1"] = (float(m.group(i)) for i in (1, 2, 3))
    if pk:
        out["pk"] = np.loadtxt(root + "_pk.dat")
    return out


# ------------------------------------------------------------------ models
CAP = np.array([0.02235, 0.1202, 1.04171, math.log(20.78), 0.963, 0.049])   # SZ21 caption (lnA = ln(10^10 A_s))
HUB = 1.0 / 2997.92458                                                    # (100 km/s/Mpc)/c in Mpc^-1
COSH = {"aest_K_type": 1, "aest_K_B": 0.5, "aest_Q0": 0.1, "aest_K2": 7.5e3, "aest_Z0": 1e-9}
EXPB = {"aest_K_type": 2, "aest_K_B": 0.1, "aest_Q0": 1e-4, "aest_K2": 9.5e3, "aest_Z0": 1e-17}


def v4(KB, mu_inv, lam_s=math.inf):
    """v4: AeST + capped F at Y = 0 (lambda_c = 0), lambda_s -> g; K-shape Cosh POSTULATED (A3)."""
    mu = 1.0 / mu_inv
    Q0 = 0.1
    K2 = mu**2 * (2 - KB) / (2 * Q0**2)
    I0cap = 3 * CAP[1] * HUB**2 / Q0
    Z0 = I0cap / (2 * K2 * 0.1)
    g = (1 - KB / 2) * (1.0 if math.isinf(lam_s) else lam_s / (1 + lam_s))
    return {"aest_K_type": 1, "aest_K_B": KB, "aest_Q0": Q0, "aest_K2": K2, "aest_Z0": Z0, "aest_g": g,
            "aest_lambda_c": 0.0}


MODELS = {
    "LCDM": None,
    "B-Cosh": {**COSH, "aest_g": 1.0},
    "B-Exp": {**EXPB, "aest_g": 1.0},
    "B-Cosh-g": {**COSH, "aest_g": 1 - 0.5 / 2},
    "B-Exp-g": {**EXPB, "aest_g": 1 - 0.1 / 2},
    "N1": {**COSH, "aest_K_B": 0.05, "aest_g": 1 - 0.05 / 2},
    "N2": {**COSH, "aest_K_B": 0.07, "aest_g": (1 - 0.07 / 2) * 400 / 401},
    "v4_KB0.01_mu1": v4(0.01, 1.0),
    "v4_KB0.05_mu1": v4(0.05, 1.0),
    "v4_KB0.078_mu1": v4(0.078, 1.0),
    "v4_KB0.05_mu10": v4(0.05, 10.0),
}
RES["models"] = {k: v for k, v in MODELS.items()}


def mu_eff(model, out):
    if model is None or "I0" not in out:
        return None
    s = out["I0"] / (2 * model["aest_K2"] * model["aest_Z0"])
    kpp = 2 * model["aest_K2"] * math.sqrt(1 + s * s)
    return math.sqrt(kpp * out["Q1"] ** 2 / (2 - model["aest_K_B"]))


def params(model, p):
    wb, wd, th, lnA, ns, tau = p
    base = {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau}
    if model is None:
        return VAN, {**base, "omega_cdm": wd}
    return AEST, {**base, "omega_cdm": OMCDM, "omega_aest": wd - OMCDM, **model}


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


STEP = np.array([1e-4, 1e-3, 2e-4, 0.01, 0.004, 0.004])                 # C2's steps


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


def kgrid_ratio(o, oref, ks=(0.1, 0.3, 1.0, 3.0, 10.0)):
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


# ------------------------------------------------------------------ K1: C2 LCDM refit reproduced with the pristine binary
Tb, o = theory("LCDM", P0, tag="K1")
cK1 = chi2_parts(Tb, o, A0)
check("K1_C2_reproduced", abs(cK1["total"] - C2RES["lcdm_refit"]["chi2"]["total"]) <= 2.0,
      f"total chi2 {cK1['total']:.2f} vs C2 {C2RES['lcdm_refit']['chi2']['total']:.2f} (classy default precision)",
      "|diff| <= 2")
RES["K1"] = cK1
if MUT:
    vo = run("lam_inf_mut", AEST, params(MODELS["v4_KB0.05_mu1"], CAP)[1])
    check("K2_mutate_binary_runs_finite", vo is not None and np.all(np.isfinite(vo["tt"][2:])), "MUTATE binary", "finite")
    save()
    P(f"C7_NATIVE COMPLETE: {NP}/{NC} checks PASS.")
    sys.exit(0 if NP == NC else 1)

# ------------------------------------------------------------------ (a) fixed caption parameters: spectra, P(k), chi2
P("== (a) SZ21 caption parameters (fixed), A_planck = 1: native spectra and chi2 (numbers only)")
FIX = {}
ref = None
for mname, model in MODELS.items():
    Tb, o = theory(mname, CAP, pk=True, tag="cap")
    if o is None:
        P(f"  {mname}: CLASS failed at caption parameters")
        FIX[mname] = {"failed": True}
        continue
    if mname == "LCDM":
        ref = o
    c = chi2_parts(Tb, o, 1.0)
    row = {"chi2": c, "H0": 100 * o["h"], "sigma8": o["sigma8"], "Omega_m": o["Omega_m"],
           "S8": o["sigma8"] * math.sqrt(o["Omega_m"] / 0.3)}
    if model is not None:
        row["mu_eff_z0_per_Mpc"] = mu_eff(model, o)
        row["g"] = model.get("aest_g", 1.0)
        row["spec_vs_LCDM"] = spec_diff(o, ref)
        row["Pk_over_LCDM"] = kgrid_ratio(o, ref)
    FIX[mname] = row
    P(f"  {mname}: chi2 total {c['total']:.2f} (plik {c['plik']:.2f}, lowTT {c['lowTT']:.2f}, lowEE {c['lowEE']:.2f}); "
      f"H0 {row['H0']:.2f}, sigma8 {row['sigma8']:.4f}, S8 {row['S8']:.4f}"
      + ("" if model is None else f"; mu_eff(z=0) {row['mu_eff_z0_per_Mpc']:.3g}/Mpc; P/P_LCDM at k[h/Mpc] "
         + ", ".join(f"{k_}: {v:.4f}" for k_, v in row["Pk_over_LCDM"].items())
         + "; max|dCl|: " + ", ".join(f"{k_} {v:.1e}" for k_, v in row["spec_vs_LCDM"].items())))
RES["fixed_caption"] = FIX
RUNAWAY = []
for mname, row in FIX.items():
    if mname == "LCDM":
        continue
    bad = row.get("failed") or not math.isfinite(row["chi2"]["total"]) or max(row["Pk_over_LCDM"].values()) > 10
    row["RUNAWAY"] = bool(bad)
    if bad:
        RUNAWAY.append(mname)
P(f"  RUNAWAY at caption parameters (A4; not fitted): {RUNAWAY}")
RES["runaway"] = RUNAWAY
save()

# K5/K6 (A4): the runaway is gauge-consistent and converged
for mname in ("N1", "v4_KB0.078_mu1"):
    b, pr = params(MODELS[mname], CAP)
    o7 = run(f"{mname}_cap", b, pr, pk=True)
    oN = run(f"{mname}_capN", b, {**pr, "gauge": "newtonian"}, pk=True)
    o9 = run(f"{mname}_capT9", b, {**pr, "tol_perturbations_integration": 1e-9}, pk=True)
    dN = {**spec_diff(oN, o7), "pk": max(abs(v - 1) for v in kgrid_ratio(oN, o7).values())}
    d9 = {**spec_diff(o9, o7), "pk": max(abs(v - 1) for v in kgrid_ratio(o9, o7).values())}
    check(f"K5_gauge_{mname}", max(dN.values()) <= 1e-2, json.dumps({k: round(v, 8) for k, v in dN.items()}), "<= 1e-2")
    check(f"K6_tol_{mname}", max(d9.values()) <= 1e-3, json.dumps({k: round(v, 8) for k, v in d9.items()}), "<= 1e-3")
save()

# ------------------------------------------------------------------ lambda_s -> inf convergence (v4, K_B = 0.05, mu^-1 = 1)
P("== lambda_s -> infinity convergence at caption parameters: v4 (K_B = 0.05, mu^-1 = 1 Mpc) and the stable B-Cosh shape")
LAM = {}
for base, mk in (("v4_KB0.05_mu1", lambda ls: v4(0.05, 1.0, ls)),
                 ("B-Cosh", lambda ls: {**COSH, "aest_g": (1 - 0.5 / 2) * (1.0 if math.isinf(ls) else ls / (1 + ls))})):
    MODELS["_lam"] = mk(math.inf)
    _, oinf = theory("_lam", CAP, tag="laminf")
    LAM[base] = {}
    for ls in (1e2, 1e3, 1e4):
        MODELS["_lam"] = mk(ls)
        _, ol = theory("_lam", CAP, tag=f"lam{ls:.0e}")
        LAM[base][f"{ls:.0e}"] = {"g": MODELS["_lam"]["aest_g"], "max_rel_vs_inf": spec_diff(ol, oinf)}
        P(f"  {base}: lambda_s = {ls:.0e}: g = {MODELS['_lam']['aest_g']:.6f}; vs inf: "
          + ", ".join(f"{k}={v:.2e}" for k, v in LAM[base][f"{ls:.0e}"]["max_rel_vs_inf"].items()))
del MODELS["_lam"]
RES["lambda_s_convergence"] = LAM
bc = LAM["B-Cosh"]
m4, m2 = max(bc["1e+04"]["max_rel_vs_inf"].values()), max(bc["1e+02"]["max_rel_vs_inf"].values())
check("K3_lambda_s_converges_BCosh", m4 <= 1e-3 and m4 < m2, f"B-Cosh shape: max at 1e4 {m4:.2e}, at 1e2 {m2:.2e}",
      "<= 1e-3 at 1e4 and shrinking (stable model; the v4 runaway is reported, not scored)")
save()

# ------------------------------------------------------------------ (b) fits
P("== (b) fits to plik-lite TTTEEE + low-l TT + low-l EE (C2 likelihood; Gauss-Newton, start = C2 LCDM refit)")
FIT = {}
for mname, model in MODELS.items():
    if mname in RUNAWAY:
        continue
    pstart = P0.copy()
    pb, Ab, nr = gauss_newton(mname, pstart, A0)
    Tb, o = theory(mname, pb, pk=True, tag="best")
    c = chi2_parts(Tb, o, Ab)
    FIT[mname] = {"params": dict(zip(("omega_b", "omega_dm(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau"), pb.tolist())),
                  "A_planck": Ab, "chi2": c, "H0": 100 * o["h"], "sigma8": o["sigma8"], "Omega_m": o["Omega_m"],
                  "S8": o["sigma8"] * math.sqrt(o["Omega_m"] / 0.3), "class_runs": nr, "_o": o}
    if model is not None:
        FIT[mname]["mu_eff_z0_per_Mpc"] = mu_eff(model, o)
    P(f"  {mname}: chi2 total {c['total']:.2f} (plik {c['plik']:.2f}); H0 {FIT[mname]['H0']:.2f}, sigma8 "
      f"{o['sigma8']:.4f}, Omega_m {o['Omega_m']:.4f}, S8 {FIT[mname]['S8']:.4f}; params {np.round(pb, 5).tolist()}, "
      f"A {Ab:.5f}; {nr} runs")
    RES["fits"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIT.items()}
    save()
for mname in FIT:
    FIT[mname]["dchi2_vs_LCDM"] = FIT[mname]["chi2"]["total"] - FIT["LCDM"]["chi2"]["total"]
    if mname != "LCDM":
        FIT[mname]["Pk_over_LCDM_bestfits"] = kgrid_ratio(FIT[mname]["_o"], FIT["LCDM"]["_o"])
RES["fits"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIT.items()}
P("== summary (numbers only; no verdict): model | Delta chi2 vs LCDM refit | H0 | sigma8 | S8 | P/P_LCDM(best fits) at "
  "k = 0.1, 0.3, 1, 3, 10 h/Mpc")
for mname, f in RES["fits"].items():
    pkr = f.get("Pk_over_LCDM_bestfits", {})
    P(f"  {mname:16s} {f['dchi2_vs_LCDM']:+8.2f}  H0 {f['H0']:.2f}  sigma8 {f['sigma8']:.4f}  S8 {f['S8']:.4f}  "
      + " ".join(f"{v:.4f}" for v in pkr.values()))

# ------------------------------------------------------------------ H1 Jeans-swindle reference ratio (not scored)
REF = {}
for mname in ("v4_KB0.01_mu1", "v4_KB0.05_mu1", "v4_KB0.078_mu1", "v4_KB0.05_mu10"):
    m = MODELS[mname]
    mu = math.sqrt(2 * m["aest_K2"] / (2 - m["aest_K_B"])) * m["aest_Q0"]
    h = FIX[mname]["H0"] / 100
    REF[mname] = {f"{k_:g}": 1 / (1 + 2 * (k_ * h) ** 2 / ((2 - m["aest_K_B"]) * mu**2)) for k_ in (0.1, 0.3, 1, 3, 10)}
    kc = 243 * mu
    REF[mname]["gammaL_weight_(k/kc)^4_at_10h/Mpc"] = (10 * h / kc) ** 4
RES["H1_jeans_reference_Gamma2_ratio"] = REF
# Estimate (labelled): with c_ad^2 -> 0 the derived E, chi equations give chi'' ~ (a^2 Q/K_B)[K' - (2-K_B)(1+lam_c)Q] chi
# (cosmic-time rate^2 = Q(K' - (2-K_B)Q)/K_B, i.e. 8piG~rho(1+w)/K_B early). Window end a_c^3 = I0/((2-K_B)Q0);
# matter-era power-law index p with p(p-1) = 3*4*f_aest/K_B (f_aest = rho_aest/rho_m).
WIN = {}
for mname in FIX:
    m = MODELS[mname]
    if m is None:
        continue
    I0 = 3 * CAP[1] * HUB**2 / m["aest_Q0"]
    ac = (I0 / ((2 - m["aest_K_B"]) * m["aest_Q0"])) ** (1 / 3)
    fa = CAP[1] / (CAP[0] + CAP[1])
    pidx = 0.5 + math.sqrt(0.25 + 12 * fa / m["aest_K_B"])
    WIN[mname] = {"a_c_window_end": ac, "z_c": 1 / ac - 1, "matter_era_power_index_p_in_tau": pidx}
RES["E_chi_window_estimate"] = WIN
P("  E-chi early tachyonic window (estimate): " + json.dumps({k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in WIN.items()}))
P("  H1 Jeans-swindle Gamma^2/Gamma^2_GR (reference, different quantity): " + json.dumps(REF))
check("K4_LCDM_refit_sane", 500 <= RES["fits"]["LCDM"]["chi2"]["plik"] <= 750,
      f"chi2_plik {RES['fits']['LCDM']['chi2']['plik']:.1f}", "in [500, 750] for 613 bins")
RES["class_runs_total"] = NRUN[0]
save()
P(f"  CLASS runs: {NRUN[0]}; elapsed {time.time() - T0:.0f} s")
P(f"C7_NATIVE COMPLETE: {NP}/{NC} checks PASS.")
OUT.close()
sys.exit(0 if NP == NC else 1)
