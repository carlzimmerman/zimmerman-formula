#!/usr/bin/env python3
"""Q7_bs25_cosmology steps B, G, F, C (FROZEN_CRITERIA sections 7-10 + AMENDMENT A1): BBN of the Blanchet-Skordis DBI
background, linear growth (R_B = sigma8/sigma8_dust) at BS's published parameter sets and at the galaxy cap, the
lambda_D,95 requirement (reported, never adopted), Gauss-Newton fits to plik-lite + low-l, and the frozen verdict.

a0 is absent at linear order (Q6 D0): neither footing enters; kappa = 1/2 FITTED does not enter.
omega_K (the khronon dust abundance, the shift charge I0) is a FITTED initial condition (late-time value).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I q7_native.py   (Q7_MUTATE=1: sign-flipped plik-lite data vector and the
MUTATE binary, no scans/fits -> *_MUTATE.out/json; K0a and N0 must FAIL)
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
from scipy.optimize import brentq

T0 = time.time()
MUT = os.environ.get("Q7_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
BLD = os.path.join(EXT, "class_khronon_dbi_build_2026_10_23")
DBI = os.path.join(BLD, "class_dbi_mutate" if MUT else "class_dbi", "class")
RUNS = os.path.join(BLD, f"runs_native{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"q7_native{TAG}.out"), "w")
RES = {"mutate": MUT, "checks": {}, "note": "numbers only; a0 absent at linear order; omega_K FITTED; kappa = 1/2 FITTED"}
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
    json.dump(RES, open(os.path.join(HERE, f"q7_native_results{TAG}.json"), "w"), indent=1, default=float)


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
Q6R = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "Q6_v3_class", "q6_native_results.json")))
SRC = json.load(open(os.path.join(HERE, "q7_source_results.json")))
VAL = json.load(open(os.path.join(HERE, "q7_validate_results.json")))
P(f"== Q7 steps B/G/F/C: C2 likelihood loaded; tau prior {TAU_HAT:.4f} +- {SIG_TAU:.4f}; start = C7 LCDM refit "
  f"{np.round(P0, 6).tolist()}, A_planck {A0:.6f}; step V (A1) DBI ready: {VAL.get('dbi_ready_A1_this_build')}")

# ------------------------------------------------------------------ CLASS runner (Q6's: C7 high precision + start x0.25)
ENV = dict(os.environ, OMP_NUM_THREADS="1")
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
TCMB = 2.7255
OMCDM = 1e-8
HREF = 0.67552
NRUN = [0]
FAILMSG = {}


def run(name, binary, params, pk=False, cmb=True):
    p = {"output": ("tCl,pCl,lCl," if cmb else "") + ("mPk" if (pk or not cmb) else ""), "l_max_scalars": 2508,
         "T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2,
         "fourier_verbose": 1, "overwrite_root": "yes", **HIGH, **START, **params}
    p["output"] = p["output"].rstrip(",")
    if cmb:
        p["lensing"] = "yes"
    if pk or not cmb:
        p["P_k_max_h/Mpc"] = 10.0
    root = os.path.join(RUNS, name + "_")
    p["root"] = root
    with open(root + ".ini", "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    t_launch = time.time()
    r = subprocess.run(["nice", "-n", "15", binary, root + ".ini"], capture_output=True, text=True, env=ENV)
    NRUN[0] += 1
    if r.returncode != 0:
        FAILMSG[name] = (r.stdout + r.stderr).strip().splitlines()[-1][-300:]
        return None
    log = r.stdout
    out = {}
    if cmb:
        assert os.path.getmtime(root + "_cl_lensed.dat") >= t_launch - 1, "stale-output guard"
        cl = np.loadtxt(root + "_cl_lensed.dat")
        L = int(cl[-1, 0])
        f = (TCMB * 1e6) ** 2
        for key, col in (("tt", 1), ("ee", 2), ("te", 3), ("pp", 5)):
            arr = np.zeros(L + 1)
            arr[cl[:, 0].astype(int)] = cl[:, col] * (f if key != "pp" else 1.0)
            out[key] = arr
    m = re.search(r"found 'h = ([0-9.eE+-]+)'", log)
    out["h"] = float(m.group(1)) if m else float(p.get("h", np.nan))
    m = re.search(r"sigma8=([0-9.eE+-]+) for total matter", log)
    out["sigma8"] = float(m.group(1)) if m else np.nan
    m = re.search(r"Non-relativistic\s+Omega = ([0-9.eE+-]+)", log)
    out["Omega_m"] = float(m.group(1)) if m else np.nan
    if pk or not cmb:
        assert os.path.getmtime(root + "_pk.dat") >= t_launch - 1, "stale-output guard"
        out["pk"] = np.loadtxt(root + "_pk.dat")
    return out


# ------------------------------------------------------------------ models
KH = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0}
MU_CAP = 14.8 * HREF                       # Mpc^-1 (mu^-1 = 100.0 kpc)
MU_P1, MU_P2 = 1 / 0.223, 1 / 22.3         # Mpc^-1 (BS24 Fig. 1: 223 kpc, 22.3 Mpc)


def kmodel(ktype, mu=None, lam=None):
    d = {**KH, "aest_K_type": ktype, "aest_K2": 1.0 if mu is None else mu**2}
    if lam is not None:
        d["aest_Z0"] = lam
    return d


SETS = {"P1": (MU_P1, 30.0), "P2": (MU_P2, 1.0), "C1": (MU_CAP, 1.0), "C30": (MU_CAP, 30.0)}
MODELS = {"LCDM": None, "DUST": kmodel(0)}
for nm, (mu, lam) in SETS.items():
    MODELS[nm] = kmodel(5, mu, lam)
RES["sets"] = {nm: {"mu_per_Mpc": mu, "mu_inv_kpc": 1e3 / mu, "mu_hMpc_at_href": mu / HREF, "lambda_D": lam}
               for nm, (mu, lam) in SETS.items()}


def params(model, p):
    wb, wd, th, lnA, ns, tau = p
    base = {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau}
    if model is None:
        return VAN, {**base, "omega_cdm": wd}
    return DBI, {**base, "omega_cdm": OMCDM, "omega_aest": wd - OMCDM, **model}


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


STEP = np.array([1e-4, 1e-3, 2e-4, 0.01, 0.004, 0.004])


def gauss_newton(mname, p, A, nit=4, budget=150):
    n0 = NRUN[0]
    conv = False
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
        if abs(c0 - cn) < 0.05:
            conv = True
            break
        if NRUN[0] - n0 > budget - 10:
            break
    return p, A, NRUN[0] - n0, conv


KREP = (0.1, 0.3, 1.0, 3.0, 10.0)


def kgrid_ratio(o, oref, ks=KREP):
    a, b = o["pk"], oref["pk"]
    la = np.interp(np.log(ks), np.log(a[:, 0]), np.log(a[:, 1]))
    lb = np.interp(np.log(ks), np.log(b[:, 0]), np.log(b[:, 1]))
    return {f"{k_:g}": float(np.exp(x - y)) for k_, x, y in zip(ks, la, lb)}


def tt_ratios(o, oref, ells=(10, 100, 220, 540, 810, 1000, 1500, 2000)):
    return {str(l): float(o["tt"][l] / oref["tt"][l]) for l in ells}


def pp_ratios(o, oref, ells=(10, 100, 300, 1000)):
    return {str(l): float(o["pp"][l] / oref["pp"][l]) for l in ells}


# ------------------------------------------------------------------ K0a: C7's LCDM refit reproduced (pristine binary)
Tb, o = theory("LCDM", P0, tag="K0a")
cK0 = chi2_parts(Tb, o, A0)
check("K0a_C7_LCDM_reproduced", abs(cK0["total"] - 1003.47) <= 2.0,
      f"total chi2 {cK0['total']:.2f} vs Q6/C7 1003.47", "|diff| <= 2")
RES["K0a"] = cK0
if MUT:
    od = run("N0_mut_dust", DBI, params(MODELS["DUST"], P0)[1], pk=True)
    ob = run("N0_mut_dbi_cap_l1e30", DBI, params(kmodel(5, MU_CAP, 1e30), P0)[1], pk=True)
    ok = od is not None and ob is not None and abs(ob["sigma8"] / od["sigma8"] - 1) <= 1e-3
    check("N0_dbi_lambda_inf_equals_DUST", ok, f"MUTATE binary: sigma8 DBI(cap, 1e30) {ob['sigma8'] if ob else None} vs "
          f"DUST {od['sigma8'] if od else None}", "|ratio - 1| <= 1e-3")
    save()
    P(f"Q7_NATIVE COMPLETE: {NP}/{NC} checks PASS.")
    sys.exit(0 if NP == NC else 1)

# ------------------------------------------------------------------ K0b: Q6's LOB / DUST numbers with this lane's binary
P("== K0b: Q6's fixed-parameter sigma8 reproduced with the DBI binary (types 0 and 4 unchanged)")
od = run("K0b_DUST", DBI, params(kmodel(0), P0)[1], pk=True)
ol = run("K0b_LOB14.8", DBI, params(kmodel(4, MU_CAP), P0)[1], pk=True)
q6d, q6l = Q6R["fixed"]["DUST"]["sigma8"], Q6R["fixed"]["LOB_14.8"]["sigma8"]
check("K0b_Q6_reproduced", od is not None and ol is not None and abs(od["sigma8"] / q6d - 1) <= 1e-4
      and abs(ol["sigma8"] / q6l - 1) <= 1e-4,
      f"DUST sigma8 {od['sigma8'] if od else None} vs Q6 {q6d}; LOB 14.8 {ol['sigma8'] if ol else None} vs Q6 {q6l}",
      "each <= 1e-4 relative")
save()

# ------------------------------------------------------------------ step B: the DBI background (Q6's block, generalised)
P("== step B: DBI background and BBN (Q6's step-B constants), omega_K = C7 refit omega_dm, h = 0.67552")
HUB = 1.0 / 2997.92458
H0 = HREF * HUB
OMK = P0[1] / HREF**2
OMG = 2.4728e-5 * (TCMB / 2.7255) ** 4 / HREF**2 * 1.0
OMR = OMG * (1 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3))
TMEV0 = 8.617333e-11 * TCMB


def a_of_T(T_MeV, gs):
    return (TMEV0 / T_MeV) * (3.909 / gs) ** (1 / 3)


BBN = {"1MeV": (a_of_T(1.0, 10.75), 10.75 / (2 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3) * 2) * (3.909 / 10.75) ** (4 / 3), 10.75 / 1.75),
       "0.07MeV": (a_of_T(0.07, 3.909), 1.0, (1 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3)) / (7 / 8 * (4 / 11) ** (4 / 3)))}


def rho8(a, I0, m2, lam):                    # 8 pi G rho_K [Mpc^-2], BS24 Eq. 89a in the cancellation-free form
    Z = I0 / (2 * m2 * a**3)
    r = math.sqrt(1 + lam * Z * Z)
    return I0 / a**3 + 2 * m2 * Z * Z / (r + 1)


def w_of(a, I0, m2, lam):                    # BS24 Eq. 94a
    Z = I0 / (2 * m2 * a**3)
    r = math.sqrt(1 + lam * Z * Z)
    return Z / (r * (r + 1 + Z))


def I0_root(m2, lam):
    tgt = 3 * H0**2 * OMK
    return brentq(lambda I: rho8(1.0, I, m2, lam) - tgt, 1e-3 * tgt, tgt, xtol=1e-30, rtol=1e-14)


def dneff(lab, I0, m2, lam):
    aT, fr, nrel = BBN[lab]
    return rho8(aT, I0, m2, lam) / (3 * H0**2 * OMR / aT**4 * fr) * nrel


# K0c: the quadratic limit (lambda_D = 0) reproduces Q6's step B
def lmu_bbn(lam):
    def f(lmu):
        m2 = (10**lmu) ** 2
        return dneff("1MeV", I0_root(m2, lam), m2, lam) - 0.5
    return brentq(f, 0.0, 15.0, xtol=1e-9)


mubbn = 10 ** lmu_bbn(0.0) / HREF
dn148 = dneff("1MeV", I0_root(MU_CAP**2, 0.0), MU_CAP**2, 0.0)
q6mb, q6dn = Q6R["stepB"]["mu_K_BBN_hMpc"], Q6R["stepB"]["rows"]["14.8"]["dNeff_equiv_1MeV"]
check("K0c_Q6_stepB_reproduced", abs(mubbn / q6mb - 1) <= 1e-3 and abs(dn148 / q6dn - 1) <= 1e-3,
      f"lambda_D = 0: mu_K,BBN {mubbn:.6e} h/Mpc vs Q6 {q6mb:.6e}; dNeff,equiv(1 MeV) at 14.8 {dn148:.6e} vs Q6 {q6dn:.6e}",
      "each <= 1e-3 relative")
AW = np.geomspace(1e-6, 1e-2, 4001)


def bg_row(mu, lam):
    m2 = mu**2
    I0 = I0_root(m2, lam)
    ws = np.array([w_of(a_, I0, m2, lam) for a_ in AW])
    row = {"mu_per_Mpc": mu, "lambda_D": lam, "I0_per_Mpc2": I0, "a1": (I0 / (2 * m2)) ** (1 / 3),
           "early_abundance_ratio_a1e-8": rho8(1e-8, I0, m2, lam) * 1e-24 / rho8(1.0, I0, m2, lam),
           "1_plus_lambda^-1/2": 1 + lam ** -0.5 if lam > 0 else math.inf,
           "w_max_1e-6_to_1e-2": float(ws.max()), "a_at_w_max": float(AW[ws.argmax()]),
           "w_at_a_10^-4.5": w_of(10 ** -4.5, I0, m2, lam), "BS_GDM_line_0.0164_met": w_of(10 ** -4.5, I0, m2, lam) <= 0.0164}
    for lab in BBN:
        row[f"dNeff_equiv_{lab}"] = dneff(lab, I0, m2, lam)
        aT = BBN[lab][0]
        row[f"rhoK_over_rhor_{lab}"] = rho8(aT, I0, m2, lam) / (3 * H0**2 * OMR / aT**4 * BBN[lab][1])
    return row


STEPB = {}
for nm, (mu, lam) in SETS.items():
    STEPB[nm] = bg_row(mu, lam)


# lambda_D,BBN at the cap: smallest lambda_D with dNeff,equiv(1 MeV) <= 0.5 (root in log lambda_D)
def fl(llam):
    lam = 10**llam
    return dneff("1MeV", I0_root(MU_CAP**2, lam), MU_CAP**2, lam) - 0.5


lam_bbn = 10 ** brentq(fl, -60.0, 10.0, xtol=1e-6)
RES["stepB"] = {"rows": STEPB, "lambda_D_BBN_cap": lam_bbn, "K0c": {"mu_K_BBN_hMpc_quadratic": mubbn, "dNeff_14.8": dn148}}
P(f"  lambda_D,BBN at the cap (dNeff,equiv(1 MeV) = 0.5): {lam_bbn:.3e}")
save()

# ------------------------------------------------------------------ step G: growth at fixed parameters
P("== step G: fixed parameters = C7 LCDM refit (omega_K = omega_dm at a = 1), A_planck = C7's")
FIX = {}
for mname in MODELS:
    Tb, o = theory(mname, P0, pk=True, tag="fix")
    if o is None:
        FIX[mname] = {"failed": FAILMSG.get(f"{mname}_fix")}
        P(f"  {mname}: CLASS failed: {FIX[mname]['failed']}")
        continue
    c = chi2_parts(Tb, o, A0)
    FIX[mname] = {"chi2": c, "H0": 100 * o["h"], "sigma8": o["sigma8"], "Omega_m": o["Omega_m"],
                  "S8": o["sigma8"] * math.sqrt(o["Omega_m"] / 0.3), "_o": o}
dref = FIX["DUST"]["_o"]
for mname, row in FIX.items():
    if "failed" in row:
        continue
    o = row["_o"]
    if mname in SETS:
        row["R_B"] = o["sigma8"] / dref["sigma8"]
        row["Pk_over_DUST"] = kgrid_ratio(o, dref)
        row["TT_over_DUST_at_l"] = tt_ratios(o, dref)
        row["pp_over_DUST_at_l"] = pp_ratios(o, dref)
        row["reading"] = "GROWTH RESCUED" if row["R_B"] >= 0.95 else "GROWTH FAILS"
    c = row["chi2"]
    P(f"  {mname}: chi2 {c['total']:.2f} (plik {c['plik']:.2f}, lowTT {c['lowTT']:.2f}, lowEE {c['lowEE']:.2f}); "
      f"H0 {row['H0']:.2f}; sigma8 {row['sigma8']:.4f}; S8 {row['S8']:.4f}"
      + ("" if "R_B" not in row else f"; R_B {row['R_B']:.4f} -> {row['reading']}; P/P_DUST at k[h/Mpc] "
         + ", ".join(f"{k_}: {v:.3e}" for k_, v in row["Pk_over_DUST"].items())
         + "; TT/TT_DUST " + ", ".join(f"l{k_}: {v:.3f}" for k_, v in row["TT_over_DUST_at_l"].items() if k_ in ("220", "540", "1000"))
         + "; pp/pp_DUST " + ", ".join(f"l{k_}: {v:.3f}" for k_, v in row["pp_over_DUST_at_l"].items())))
for nm in SETS:
    STEPB[nm]["class_starts"] = "failed" not in FIX[nm]
    STEPB[nm]["class_message"] = FIX[nm].get("failed", "ran")
    d1 = STEPB[nm]["dNeff_equiv_1MeV"]
    STEPB[nm]["reading"] = ("NO RADIATION ERA (BBN-EXCLUDED)" if d1 > 0.5 else
                            ("BBN-VIABLE" if STEPB[nm]["class_starts"] else "BBN-VIABLE, CLASS REFUSES"))
    r = STEPB[nm]
    P(f"  step B {nm} (mu^-1 = {1e3 / SETS[nm][0]:.4g} kpc, lambda_D = {SETS[nm][1]:g}): dNeff,equiv 1 MeV {r['dNeff_equiv_1MeV']:.3e}, "
      f"0.07 MeV {r['dNeff_equiv_0.07MeV']:.3e}; early/late abundance {r['early_abundance_ratio_a1e-8']:.4f} "
      f"(1 + lambda^-1/2 = {r['1_plus_lambda^-1/2']:.4f}); w_max {r['w_max_1e-6_to_1e-2']:.4f} at a {r['a_at_w_max']:.3e}; "
      f"w(10^-4.5) {r['w_at_a_10^-4.5']:.3e} (BS GDM line 0.0164 met: {r['BS_GDM_line_0.0164_met']}); CLASS starts: "
      f"{r['class_starts']} -> {r['reading']}")
check("B_readings", all(STEPB[nm]["reading"] in ("BBN-VIABLE", "NO RADIATION ERA (BBN-EXCLUDED)", "BBN-VIABLE, CLASS REFUSES")
                        for nm in SETS), "; ".join(f"{nm}: {STEPB[nm]['reading']}" for nm in SETS), "computed (readings are results)")
# N0: lambda_D -> infinity at the cap is dust in the native setting
o_inf = run("N0_dbi_cap_l1e30", DBI, params(kmodel(5, MU_CAP, 1e30), P0)[1], pk=True)
check("N0_dbi_lambda_inf_equals_DUST", o_inf is not None and abs(o_inf["sigma8"] / dref["sigma8"] - 1) <= 1e-3,
      f"sigma8 DBI(cap, 1e30) {o_inf['sigma8'] if o_inf else None} vs DUST {dref['sigma8']}", "|ratio - 1| <= 1e-3")
RES["fixed"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIX.items()}
save()

# ------------------------------------------------------------------ step G: lambda_D,95 requirement scans (REPORTED only)
P("== step G scans: R_B(lambda_D) at fixed mu (REPORTED requirement; never adopted, never fitted)")
ds8 = run("SCAN_DUST", DBI, params(kmodel(0), P0)[1], cmb=False)["sigma8"]


def rb_scan(tag, mu, lam):
    o = run(f"SCAN_{tag}_l{lam:.6g}", DBI, params(kmodel(5, mu, lam), P0)[1], cmb=False)
    return np.nan if o is None else o["sigma8"] / ds8


SCANS = {}
VC = {"MW_220kms": (220.0 / 299792.458) ** 2, "cluster_1000kms": (1000.0 / 299792.458) ** 2}
for tag, mu, top in (("cap", MU_CAP, 24), ("P1mu", MU_P1, 24), ("P2mu", MU_P2, 30)):
    grid = [10.0 ** e for e in range(0, top + 1, 2)]
    rbs = [rb_scan(tag, mu, lam) for lam in grid]
    row = {"mu_per_Mpc": mu, "grid": dict(zip([f"{g:g}" for g in grid], rbs))}
    idx = next((i for i, v in enumerate(rbs) if v >= 0.95), None)
    if idx is None:
        row["lambda_D_95"] = None
        row["text"] = f"beyond the grid (R_B({grid[-1]:g}) = {rbs[-1]:.4f})"
    elif idx == 0:
        row["lambda_D_95"] = grid[0]
        row["text"] = f"<= {grid[0]:g} (R_B = {rbs[0]:.4f})"
    else:
        lo, hi, rlo, rhi = math.log10(grid[idx - 1]), math.log10(grid[idx]), rbs[idx - 1], rbs[idx]
        bis = []
        for _ in range(5):
            mid = 0.5 * (lo + hi)
            rm = rb_scan(tag, mu, 10**mid)
            bis.append((10**mid, rm))
            if rm >= 0.95:
                hi, rhi = mid, rm
            else:
                lo, rlo = mid, rm
        l95 = 10 ** (lo + (0.95 - rlo) / (rhi - rlo) * (hi - lo))
        row["bisection"] = bis
        row["lambda_D_95"] = l95
        row["ceiling_lambda95^-1/2"] = l95 ** -0.5
        row["ceiling_vs_vc2"] = {k: l95 ** -0.5 / v for k, v in VC.items()}
        row["text"] = (f"{l95:.3e} (bracket [{10**lo:.3e}, {10**hi:.3e}], R_B {rlo:.4f} / {rhi:.4f}); DBI ceiling |Q-1| < "
                       f"{l95 ** -0.5:.3e} = " + ", ".join(f"{v:.3g} x v_c^2/c^2 ({k})" for k, v in row["ceiling_vs_vc2"].items()))
    SCANS[tag] = row
    P(f"  mu = {mu:.5g} Mpc^-1 ({tag}): R_B on lambda_D grid " + ", ".join(f"{k}: {v:.4f}" for k, v in row["grid"].items()))
    P(f"    lambda_D,95 = {row['text']}")
    save()
RES["scans"] = SCANS
for tag in SCANS:                             # BBN rows at the requirement points
    if SCANS[tag]["lambda_D_95"]:
        STEPB[f"{tag}@lambda95"] = bg_row(SCANS[tag]["mu_per_Mpc"], SCANS[tag]["lambda_D_95"])
        r = STEPB[f"{tag}@lambda95"]
        P(f"  step B {tag}@lambda_D,95: dNeff,equiv 1 MeV {r['dNeff_equiv_1MeV']:.3e}; early/late abundance "
          f"{r['early_abundance_ratio_a1e-8']:.6f}; w_max {r['w_max_1e-6_to_1e-2']:.3e}")
RES["stepB"]["rows"] = STEPB
save()

# ------------------------------------------------------------------ reported cross-check: F3's ODE with the DBI kernel
P("== reported cross-check: F3's sub-horizon ODE (copied) with kernel s = a^2 M^2/(k^2 + a^2 M^2), M^2 = Qbar^2 K''/2 (DBI)")


def make_E(Om, h, rad=True):                                           # verbatim from F3 f3_growth_audit.py
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL)), Or


def growth_ratio_dbi(kk, Mh, Om, Ob, h, a_i=1e-3, rad=True):           # F3's growth_ratio, kernel from M(a) [h/Mpc]
    Ek, Or = make_E(Om, h, rad); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)
    def s_of(a, M):
        if M is None: return np.ones(n)
        x2 = (kk / (a * M(a))) ** 2
        return 1.0 / (1.0 + x2)
    def solve(M):
        def rhs(x, st):
            a = math.exp(x); E = Ek(a); eps = 1e-6
            dlnE = (math.log(Ek(a * math.exp(eps))) - math.log(Ek(a * math.exp(-eps)))) / (2 * eps)
            dens = 1.5 * a ** -3 / E ** 2
            db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
            src_b = dens * (Ob * db + OK * dk); src_k = dens * (Ob * db + OK * dk * s_of(a, M))
            return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE) * gk + src_k])
        st0 = np.concatenate([np.full(n, a_i), np.full(n, a_i), np.full(n, a_i), np.full(n, a_i)])
        sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12)
        y_ = sol.y[:, -1]; return (Ob * y_[:n] + OK * y_[2 * n:3 * n]) / Om
    return solve(Mh) / solve(None)


W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
KS = np.geomspace(1e-4, 50.0, 1500)
KT = np.geomspace(1e-3, 3.0, 36)
hF = FIX["LCDM"]["H0"] / 100
OmF, ObF = (P0[0] + P0[1]) / hF**2, P0[0] / hF**2
pkD = dref["pk"]
PkF = np.exp(np.interp(np.log(KS), np.log(pkD[:, 0]), np.log(pkD[:, 1]), right=-np.inf))


def sig8F(T=None):
    Pk = PkF if T is None else PkF * T ** 2
    return math.sqrt(np.trapz(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))


ODE = {}
for nm, (mu, lam) in SETS.items():
    a1 = STEPB[nm]["a1"]
    def Mh(a, mu=mu, lam=lam, a1=a1):
        Z = (a1 / a) ** 3
        r = math.sqrt(1 + lam * Z * Z)
        return mu / hF * (1 + Z / r) * r ** 1.5
    ODE[nm] = {}
    for ai in (1e-4, 1e-3):
        T = growth_ratio_dbi(KT, Mh, OmF, ObF, hF, a_i=ai)
        Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
        ODE[nm][f"ai{ai:g}"] = sig8F(Tf) / sig8F()
    P(f"  {nm}: R_ODE a_i=1e-4 {ODE[nm]['ai0.0001']:.4f}, a_i=1e-3 {ODE[nm]['ai0.001']:.4f}  vs  R_B {FIX[nm]['R_B']:.4f}")
RES["ode_crosscheck"] = ODE
save()

# ------------------------------------------------------------------ step F: fits
P("== step F: fits to plik-lite TTTEEE + low-l TT + low-l EE (C2 likelihood; C7's Gauss-Newton, start = C7 LCDM refit)")
if SCANS["cap"]["lambda_D_95"]:
    MODELS["CAP@l95"] = kmodel(5, MU_CAP, SCANS["cap"]["lambda_D_95"])
FIT = {}
for mname in ["LCDM", *SETS, *(["CAP@l95"] if "CAP@l95" in MODELS else [])]:
    pb, Ab, nr, conv = gauss_newton(mname, P0.copy(), A0)
    Tb, o = theory(mname, pb, pk=True, tag="best")
    if o is None:
        FIT[mname] = {"failed": FAILMSG.get(f"{mname}_best")}
        continue
    c = chi2_parts(Tb, o, Ab)
    FIT[mname] = {"params": dict(zip(("omega_b", "omega_K(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau"), pb.tolist())),
                  "A_planck": Ab, "chi2": c, "H0": 100 * o["h"], "sigma8": o["sigma8"], "Omega_m": o["Omega_m"],
                  "S8": o["sigma8"] * math.sqrt(o["Omega_m"] / 0.3), "class_runs": nr, "converged": conv, "_o": o}
    P(f"  {mname}: chi2 {c['total']:.2f} (plik {c['plik']:.2f}, lowTT {c['lowTT']:.2f}, lowEE {c['lowEE']:.2f}); "
      f"H0 {FIT[mname]['H0']:.2f}, sigma8 {o['sigma8']:.4f}, Omega_m {o['Omega_m']:.4f}, S8 {FIT[mname]['S8']:.4f}; "
      f"params {np.round(pb, 5).tolist()}, A {Ab:.5f}; {nr} runs; converged {conv}")
    RES["fits"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIT.items()}
    save()
for mname in FIT:
    if "failed" in FIT[mname]:
        continue
    FIT[mname]["dchi2_vs_LCDM"] = FIT[mname]["chi2"]["total"] - FIT["LCDM"]["chi2"]["total"]
    if mname != "LCDM":
        FIT[mname]["Pk_over_LCDM_bestfits"] = kgrid_ratio(FIT[mname]["_o"], FIT["LCDM"]["_o"])
        FIT[mname]["TT_over_LCDM_bestfits_at_l"] = tt_ratios(FIT[mname]["_o"], FIT["LCDM"]["_o"])
        FIT[mname]["pp_over_LCDM_bestfits_at_l"] = pp_ratios(FIT[mname]["_o"], FIT["LCDM"]["_o"])
RES["fits"] = {k: {kk: vv for kk, vv in v.items() if kk != "_o"} for k, v in FIT.items()}
P("== fit summary (numbers only): model | Delta chi2 vs LCDM refit | converged | H0 | sigma8 | S8 | omega_K | "
  "P/P_LCDM(best fits) at k = " + ", ".join(f"{k_:g}" for k_ in KREP) + " h/Mpc")
for mname, f in RES["fits"].items():
    if "failed" in f:
        P(f"  {mname}: best-fit run failed: {f['failed']}")
        continue
    pkr = f.get("Pk_over_LCDM_bestfits", {})
    P(f"  {mname:9s} {f['dchi2_vs_LCDM']:+10.2f}  {str(f['converged']):5s}  H0 {f['H0']:.2f}  sigma8 {f['sigma8']:.4f}  "
      f"S8 {f['S8']:.4f}  omega_K {f['params']['omega_K(FITTED)']:.5f}  " + " ".join(f"{v:.3e}" for v in pkr.values()))
check("F_fits", "failed" not in RES["fits"]["LCDM"] and 500 <= RES["fits"]["LCDM"]["chi2"]["plik"] <= 750
      and all("failed" not in f and math.isfinite(f["chi2"]["total"]) for f in RES["fits"].values()),
      f"LCDM refit chi2_plik {RES['fits']['LCDM']['chi2'].get('plik', float('nan')):.1f}; all fits finite",
      "plik in [500, 750]; finite")
save()

# ------------------------------------------------------------------ step C: the frozen verdict
P("== step C: frozen verdict (FROZEN_CRITERIA section 10 + A1)")
sc = SRC["checks"]
err = []
if not sc["S7_BS_Eq71_equals_Q6_cs2"]["pass"]:
    err.append("S7: Q6's c_s^2 differs from BS24 Eq. 71")
if not sc["S8_kernel_Upsilon_Xi_Eq66a"]["pass"]:
    err.append("S8: kernel/Upsilon/Eq. 66a mismatch")
if not RES["checks"]["K0b_Q6_reproduced"]["pass"]:
    err.append("K0b: Q6's numbers not reproduced")
if not VAL["checks"].get("V1b_lambda0_bitwise_vs_LIT_A1", {}).get("pass", False):
    err.append("V1b: DBI at lambda_D = 0 differs from Q6's LIT inside CLASS")
per = {}
for nm in SETS:
    f = RES["fits"].get(nm, {})
    per[nm] = {"BBN": STEPB[nm]["reading"], "R_B": FIX[nm]["R_B"], "growth": FIX[nm]["reading"],
               "dchi2_fit": f.get("dchi2_vs_LCDM"), "converged": f.get("converged")}
    per[nm]["A_ok"] = (per[nm]["BBN"] == "BBN-VIABLE" and per[nm]["growth"] == "GROWTH RESCUED"
                       and per[nm]["dchi2_fit"] is not None and per[nm]["dchi2_fit"] <= 10.0)
if err:
    verdict = "(C) OUR LANES HAVE AN ERROR: " + "; ".join(err)
elif any(v["A_ok"] for v in per.values()):
    verdict = "(A) BS25'S SECTOR RESCUES v3 AT GALAXY-ALLOWED mu_K at " + ", ".join(nm for nm, v in per.items() if v["A_ok"])
elif all(v["BBN"] == "BBN-VIABLE" for v in per.values()):
    verdict = "(B) IT FIXES BBN ONLY; GROWTH STILL FAILS"
else:
    verdict = "(B-) NOT EVEN BBN at BS's sets: " + ", ".join(nm for nm, v in per.items() if v["BBN"] != "BBN-VIABLE")
RES["stepC"] = {"per_set": per, "verdict": verdict,
                "frozen_V_unit_ii_and_V1_failed_A1": [n for n in ("V_unit_ii_finite_lambda_vs_BS", "V1_lambda0_vs_LIT")
                                                       if not VAL["checks"][n]["pass"]]}
for nm, v in per.items():
    P(f"  {nm}: {v['BBN']}; R_B {v['R_B']:.4f} -> {v['growth']}; fitted Delta chi2 {v['dchi2_fit']}")
check("C_verdict", verdict[:3] in ("(A)", "(B)", "(C)", "(B-"), verdict, "computed (the verdict is a result)")
RES["class_runs_total"] = NRUN[0]
save()
P(f"  CLASS runs: {NRUN[0]}; elapsed {time.time() - T0:.0f} s")
P(f"Q7_NATIVE COMPLETE: {NP}/{NC} checks PASS.")
OUT.close()
sys.exit(0 if NP == NC else 1)
