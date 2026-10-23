#!/usr/bin/env python3
"""X4_growth_native_cap step 0 (D0a-e, F0a-c) + step 2, question (ii) (FROZEN_CRITERIA.md sections 2, 4, 5, 7):
is Q7's large-lambda_D DBI door (R_B = 0.95 at lambda_D,95) closed by its own consistency (linear |dQ| against the DBI
square-root ceiling lambda_D^-1/2) and by the record's Lyman-alpha forest gates (L346 band, L319 line) on linear P(k)?

  OMP_NUM_THREADS=1 nice -n 15 python3 -I x4_dbi_door.py              -> x4_dbi_door.out, x4_dbi_door_results.json
  X4_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 -I x4_dbi_door.py  -> *_MUTATE.* (Q7's MUTATE binary + extraction without
                                                                         the photon/ur subtraction and theta term: D0a and D0c must FAIL)

Read-only use of Q7's validated DBI binary and C7's vanilla binary; parameters from Q7's committed JSON and on-disk .ini
files. Points: Q7's three committed lambda_D,95 values only (no lambda_D or mu scan; no fit). a0 is absent at linear order:
neither footing enters; kappa = 1/2 FITTED does not enter; omega_K FITTED; lambda_D is a growth-set KNOB, graded, never adopted.
"""
import glob
import json
import math
import os
import re
import resource
import shutil
import subprocess
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
MUT = os.environ.get("X4_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
DBI = os.path.join(EXT, "class_khronon_dbi_build_2026_10_23", "class_dbi_mutate" if MUT else "class_dbi", "class")
Q7RUNS = os.path.join(EXT, "class_khronon_dbi_build_2026_10_23", "runs_native")
RUNS = os.path.join(EXT, "x4_growth_native_cap_2026_10_23", f"runs_step2{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"x4_dbi_door{TAG}.out"), "w")
RES = {"lane": "X4_growth_native_cap", "script": "x4_dbi_door.py", "date": "2026-10-23", "mutate": MUT, "checks": {},
       "note": "a0 absent at linear order (neither footing enters); kappa = 1/2 FITTED; omega_K FITTED; lambda_D a KNOB (graded, not adopted)"}
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
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {value}   (line: {thr})")
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}


def save():
    RES["elapsed_s"] = round(time.time() - T0, 1)
    RES["peak_rss_GB_self"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    RES["peak_rss_GB_children"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9
    json.dump(RES, open(os.path.join(HERE, f"x4_dbi_door_results{TAG}.json"), "w"), indent=1, default=float)


P(__doc__)
P(f"MUTATE = {MUT}; DBI binary {os.path.relpath(DBI, REPO)}; vanilla {os.path.relpath(VAN, REPO)}")

Q7R = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "Q7_bs25_cosmology", "q7_native_results.json")))
C7F = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")))["fits"]["LCDM"]
P0 = np.array([C7F["params"][k] for k in ("omega_b", "omega_dm(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau")])

# ------------------------------------------------------------------ CLASS runner (Q7's precision; extra outputs only)
ENV = dict(os.environ, OMP_NUM_THREADS="1")
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
TCMB = 2.7255
OMCDM = 1e-8
ZGRID = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 37.0, 60.0, 100.0, 200.0, 500.0]
KH = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0}
RUNINFO, FAILMSG = {}, {}


def _hdr_z(path):
    with open(path) as fh:
        for line in fh:
            m = re.search(r"redshift z=([0-9.eE+-]+)", line)
            if m:
                return float(m.group(1))
    return None


def _read_cols(path):
    names = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") and re.search(r"(^|\s)1:", line.lstrip("#")):
                toks = re.split(r"\s+(?=\d+:)", line.lstrip("#").strip())
                names = [re.sub(r"^\d+:", "", t).strip() for t in toks]
    arr = np.loadtxt(path)
    assert names is not None and len(names) == arr.shape[1], f"column titles not parsed in {os.path.basename(path)}"
    return names, arr


def run(name, binary, params, cmb=False, zs=ZGRID, tk=True, retry=True):
    outs = ("tCl,pCl,lCl," if cmb else "") + "mPk" + (",mTk,vTk" if tk else "")
    p = {"output": outs, "l_max_scalars": 2508, "T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1,
         "background_verbose": 2, "fourier_verbose": 1, "overwrite_root": "yes", **HIGH, **START, **params}
    if cmb:
        p["lensing"] = "yes"
    p["P_k_max_h/Mpc"] = 10.0
    p["z_pk"] = ", ".join(f"{z:g}" for z in zs)
    p["write_background"] = "yes"
    root = os.path.join(RUNS, name + "_")
    p["root"] = root
    for f in glob.glob(root + "*"):
        os.remove(f)
    with open(root + ".ini", "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    t_launch = time.time()
    try:
        r = subprocess.run(["nice", "-n", "15", binary, root + ".ini"], capture_output=True, text=True, env=ENV, timeout=1800)
    except subprocess.TimeoutExpired:
        FAILMSG[name] = "timeout 1800 s"
        return None
    RUNINFO[name] = {"seconds": round(time.time() - t_launch, 1), "z_pk": list(zs),
                     "children_peak_rss_GB_so_far": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9}
    if r.returncode != 0:
        FAILMSG[name] = (r.stdout + r.stderr).strip().splitlines()[-1][-300:]
        if retry and len(zs) > 1:                       # pre-declared technical fallback: drop the top z once
            P(f"  run {name} refused ({FAILMSG[name]}); retrying once without z = {zs[-1]:g}")
            return run(name, binary, params, cmb, zs[:-1], tk, retry=False)
        return None
    log = r.stdout
    out = {"zs": list(zs)}
    m = re.search(r"found 'h = ([0-9.eE+-]+)'", log)
    out["h_stdout"] = float(m.group(1)) if m else float(params.get("h", np.nan))
    m = re.search(r"sigma8=([0-9.eE+-]+) for total matter", log)
    out["sigma8"] = float(m.group(1)) if m else np.nan
    m = re.search(r"I0 = ([0-9.eE+-]+) Mpc", log)
    out["I0_class"] = float(m.group(1)) if m else None
    out["pk"], out["tk"] = {}, {}
    for f in sorted(glob.glob(root + "*pk.dat")):
        if not re.search(r"(_z\d+)?_pk\.dat$", f[len(root) - 1:]):
            continue
        assert os.path.getmtime(f) >= t_launch - 1, "stale-output guard"
        z = _hdr_z(f)
        out["pk"][z] = np.loadtxt(f)
    for f in sorted(glob.glob(root + "*tk.dat")):
        z = _hdr_z(f)
        names, arr = _read_cols(f)
        out["tk"][z] = {n: arr[:, i] for i, n in enumerate(names)}
    names, arr = _read_cols(glob.glob(root + "*background.dat")[0])
    out["bg"] = {n: arr[:, i] for i, n in enumerate(names)}
    i0 = int(np.argmin(out["bg"]["z"]))
    out["h"] = float(out["bg"]["H [1/Mpc]"][i0]) * 2997.92458          # 12-digit h from CLASS's own H0 (stdout prints fewer digits)
    assert abs(out["h"] / out["h_stdout"] - 1) < 1e-5, "h from background file disagrees with stdout"
    if cmb:
        out["cl_lensed"] = np.loadtxt(glob.glob(root + "*cl_lensed.dat")[0])
    return out


def read_ini(path):
    d = {}
    for line in open(path):
        if "=" in line:
            k_, v_ = [s.strip() for s in line.split("=", 1)]
            d[k_] = v_
    return d


def fixed_params(ktype=None, mu=None, lam=None):
    wb, wd, th, lnA, ns, tau = P0
    base = {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau}
    if ktype is None:
        return {**base, "omega_cdm": wd}
    d = {**base, "omega_cdm": OMCDM, "omega_aest": wd - OMCDM, **KH, "aest_K_type": ktype,
         "aest_K2": 1.0 if mu is None else mu ** 2}
    if lam is not None:
        d["aest_Z0"] = lam
    return d


def lnP_at(pk, ks):
    return np.interp(np.log(ks), np.log(pk[:, 0]), np.log(pk[:, 1]))


# ------------------------------------------------------------------ the points (Q7's committed lambda_D,95; no scan)
SC = Q7R["scans"]
POINTS = {"cap": (SC["cap"]["mu_per_Mpc"], SC["cap"]["lambda_D_95"]),
          "P1mu": (SC["P1mu"]["mu_per_Mpc"], SC["P1mu"]["lambda_D_95"]),
          "P2mu": (SC["P2mu"]["mu_per_Mpc"], SC["P2mu"]["lambda_D_95"])}
RES["points"] = {k: {"mu_per_Mpc": m, "mu_inv_Mpc": 1 / m, "lambda_D_95": l, "ceiling_lambda^-1/2": l ** -0.5,
                     "line_L_lambda^-1/2_over_3": l ** -0.5 / 3} for k, (m, l) in POINTS.items()}
for k, v in RES["points"].items():
    P(f"  point {k}: mu {v['mu_per_Mpc']:.6g} Mpc^-1 (mu^-1 {v['mu_inv_Mpc']:.4g} Mpc), lambda_D,95 {v['lambda_D_95']:.6e}, "
      f"ceiling {v['ceiling_lambda^-1/2']:.4e}, line L {v['line_L_lambda^-1/2_over_3']:.4e}")
save()

# ------------------------------------------------------------------ runs
P("== CLASS runs (one at a time; Q7 precision; z_pk grid " + ", ".join(f"{z:g}" for z in ZGRID) + ")")
iniC = read_ini(os.path.join(Q7RUNS, "CAP@l95_best_.ini"))
iniL = read_ini(os.path.join(Q7RUNS, "LCDM_best_.ini"))
DROP = {"output", "root", "lensing", "P_k_max_h/Mpc", "l_max_scalars", "T_cmb", "write_parameters", "input_verbose",
        "background_verbose", "fourier_verbose", "overwrite_root", *HIGH, *START}
parC = {k: v for k, v in iniC.items() if k not in DROP}
parL = {k: v for k, v in iniL.items() if k not in DROP}
R = {}
R["CAP_best"] = run("CAP_best", DBI, parC, cmb=True)
R["LCDM_best"] = run("LCDM_best", VAN, parL, cmb=True, tk=False)
R["DUST_fix"] = run("DUST_fix", DBI, fixed_params(0))
R["LCDM_fix"] = run("LCDM_fix", VAN, fixed_params(None), tk=False)
for nm, (mu, lam) in POINTS.items():
    R[f"{nm}_fix"] = run(f"{nm}_fix", DBI, fixed_params(5, mu, lam))
R["N0_cap_1e30"] = run("N0_cap_1e30", DBI, fixed_params(5, POINTS["cap"][0], 1e30), tk=False)
for k, v in R.items():
    P(f"  {k}: {'ran' if v is not None else 'FAILED: ' + FAILMSG.get(k, '?')}; "
      + (f"h {v['h']:.6f}, sigma8 {v['sigma8']}, z with pk {sorted(v['pk'])}, tk z {len(v['tk'])}" if v else "")
      + f"; {RUNINFO.get(k)}")
RES["runinfo"] = RUNINFO
RES["class_failures"] = FAILMSG
save()

# ------------------------------------------------------------------ D0a: Q7's committed best-fit numbers reproduced
P("== D0a: Q7's committed CAP@l95_best / LCDM_best reproduced")
qC = np.loadtxt(os.path.join(Q7RUNS, "CAP@l95_best__pk.dat"))
qL = np.loadtxt(os.path.join(Q7RUNS, "LCDM_best__pk.dat"))
fitC = Q7R["fits"]["CAP@l95"]
d0a = {}
ok = R["CAP_best"] is not None and R["LCDM_best"] is not None
if ok:
    pc, pl = R["CAP_best"]["pk"][0.0], R["LCDM_best"]["pk"][0.0]
    sel = qC[:, 0] <= 10.0
    d0a["max_dlnP_CAP_vs_Q7_file"] = float(np.max(np.abs(lnP_at(pc, qC[sel, 0]) - np.log(qC[sel, 1]))))
    sel = qL[:, 0] <= 10.0
    d0a["max_dlnP_LCDM_vs_Q7_file"] = float(np.max(np.abs(lnP_at(pl, qL[sel, 0]) - np.log(qL[sel, 1]))))
    d0a["ratios_this"] = {f"{k_:g}": float(np.exp(lnP_at(pc, np.array([k_]))[0] - lnP_at(pl, np.array([k_]))[0])) for k_ in (0.1, 1.0, 3.0)}
    d0a["ratios_Q7"] = {k_: fitC["Pk_over_LCDM_bestfits"][k_] for k_ in ("0.1", "1", "3")}
    d0a["sigma8_this"], d0a["sigma8_Q7"] = R["CAP_best"]["sigma8"], fitC["sigma8"]
    ok = (d0a["max_dlnP_CAP_vs_Q7_file"] <= 1e-4 and d0a["max_dlnP_LCDM_vs_Q7_file"] <= 1e-4
          and all(abs(d0a["ratios_this"][k_] - d0a["ratios_Q7"][k_]) <= 1e-3 for k_ in d0a["ratios_Q7"])
          and abs(d0a["sigma8_this"] - d0a["sigma8_Q7"]) <= 1e-5)
RES["D0a"] = d0a
check("D0a_Q7_bestfits_reproduced", ok, json.dumps(d0a, default=float),
      "max |dlnP| <= 1e-4 (k <= 10 h/Mpc); ratios within 1e-3; sigma8 within 1e-5")

# ------------------------------------------------------------------ D0b: lambda_D,95 meaning reproduced at fixed parameters
d0b = {}
for nm in POINTS:
    o, d = R.get(f"{nm}_fix"), R.get("DUST_fix")
    d0b[nm] = (o["sigma8"] / d["sigma8"]) if (o and d) else None
RES["D0b_R_B_at_lambda95"] = d0b
check("D0b_lambda95_R_B", all(v is not None and abs(v - 0.95) <= 0.002 for v in d0b.values()),
      "; ".join(f"{k}: R_B {v:.5f}" if v is not None else f"{k}: missing" for k, v in d0b.items()), "each |R_B - 0.95| <= 0.002")
save()

# ------------------------------------------------------------------ background and extraction machinery
HUB = 1.0 / 2997.92458


def bg0(o):
    """CLASS background columns at z = 0 (last row) and the H0 used."""
    b = o["bg"]
    i = int(np.argmin(b["z"]))
    g = lambda key: float(b[key][i])
    return {"z0": g("z"), "rho_g": g("(.)rho_g"), "rho_b": g("(.)rho_b"), "rho_cdm": g("(.)rho_cdm"),
            "rho_ur": g("(.)rho_ur"), "rho_lambda": g("(.)rho_lambda"), "rho_tot": g("(.)rho_tot")}


def dbi_state(a, I0, mu, lam):
    """DBI background (Q7 dbi.patch / BS24 Eqs. 88-89, cancellation-free): returns Q, K', K, K'', 8piG rho, 8piG p, ca2, headroom."""
    m2 = mu * mu
    Kp = I0 / a ** 3
    Z = Kp / (2 * m2)
    r = math.sqrt(1 + lam * Z * Z)
    Q = 1 + Z / r
    K = 2 * m2 * Z * Z / (r * (r + 1))
    Kpp = 2 * m2 * r ** 3
    rho8 = Kp + 2 * m2 * Z * Z / (r + 1)
    ca2 = Z / (r * r * (r + Z))
    sl = math.sqrt(lam) * Z
    head = lam ** -0.5 / (r * (r + sl)) if lam > 0 else math.inf     # lambda^-1/2 - (Q - 1), cancellation-free
    return {"Q": Q, "Kp": Kp, "K": K, "Kpp": Kpp, "rho8": rho8, "p8": K, "ca2": ca2, "headroom": head, "Z": Z, "r": r}


def I0_solve(o, mu, lam, omega_aest):
    h = o["h"]
    tgt = 3 * (omega_aest / h ** 2) * (h * HUB) ** 2
    f = lambda I: dbi_state(1.0, I, mu, lam)["rho8"] - tgt
    return brentq(f, 1e-3 * tgt, tgt, xtol=1e-30, rtol=1e-15)


def extract(o, z, mu, lam, I0, mutate_extraction=False):
    """delta_K, theta_K (synchronous gauge) by subtraction from d_tot / t_tot; returns k [Mpc^-1] and arrays."""
    b0 = bg0(o)
    a = 1.0 / (1.0 + z)
    rg, rb, rc, ru, rL = (b0["rho_g"] * a ** -4, b0["rho_b"] * a ** -3, b0["rho_cdm"] * a ** -3, b0["rho_ur"] * a ** -4,
                          b0["rho_lambda"])
    st = dbi_state(a, I0, mu, lam) if lam is not None else {"rho8": I0 / a ** 3, "p8": 0.0, "Q": 1.0, "Kp": I0 / a ** 3}
    rK, pK = st["rho8"] / 3.0, st["p8"] / 3.0
    t = o["tk"][z]
    kM = t["k (h/Mpc)"] * o["h"]
    rho_noL = rg + rb + rc + ru + rK
    rpp_tot = 4 / 3 * rg + rb + rc + 4 / 3 * ru + rK + pK
    if mutate_extraction:
        drK = t["d_tot"] * rho_noL - (rb * t["d_b"] + rc * t["d_cdm"])
        rpthK = 0.0 * kM
    else:
        drK = t["d_tot"] * rho_noL - (rg * t["d_g"] + rb * t["d_b"] + rc * t["d_cdm"] + ru * t["d_ur"])
        rpthK = t["t_tot"] * rpp_tot - (4 / 3 * rg * t["t_g"] + rb * t["t_b"] + 4 / 3 * ru * t["t_ur"])
    dK = drK / rK
    thK = rpthK / (rK + pK)
    H = math.sqrt(rg + rb + rc + ru + rK + rL)          # CLASS units: H^2 = rho_tot (flat)
    Hc = a * H                                          # conformal Hubble [Mpc^-1]
    return {"k": kM, "kh": t["k (h/Mpc)"], "dK": dK, "thK": thK, "Hc": Hc, "a": a, "w": pK / rK, "st": st,
            "d_cdm": t["d_cdm"], "d_m": t["d_m"], "rK": rK}


# ------------------------------------------------------------------ D0e: background, I0
P("== D0e: analytic DBI background vs CLASS's background file; own I0 vs CLASS's")
d0e = {}
ok_e = True
for nm, (mu, lam) in POINTS.items():
    for tag in (f"{nm}_fix",) + (("CAP_best",) if nm == "cap" else ()):
        o = R.get(tag)
        if o is None:
            ok_e = False
            continue
        om_aest = float(parC["omega_aest"]) if tag == "CAP_best" else P0[1] - OMCDM
        I0 = I0_solve(o, mu, lam, om_aest)
        b, b0 = o["bg"], bg0(o)
        zz = b["z"]
        sel = zz <= 500.0
        rK_cl = (b["(.)rho_tot"] - b["(.)rho_g"] - b["(.)rho_b"] - b["(.)rho_cdm"] - b["(.)rho_ur"] - b["(.)rho_lambda"])[sel]
        rK_an = np.array([dbi_state(1 / (1 + z_), I0, mu, lam)["rho8"] / 3 for z_ in zz[sel]])
        dev = float(np.max(np.abs(rK_an / rK_cl - 1)))
        dI = abs(I0 / o["I0_class"] - 1) if o["I0_class"] else np.inf
        d0e[tag] = {"I0_own": I0, "I0_class": o["I0_class"], "dI0_rel": dI, "max_rel_dev_rhoK_z<=500": dev, "rows": int(sel.sum())}
        o["I0"] = I0
        ok_e = ok_e and dev <= 1e-6 and dI <= 1e-8
        P(f"  {tag}: I0 own {I0:.12e} vs CLASS {o['I0_class']}; max |rho_K analytic/CLASS - 1| (z <= 500, {sel.sum()} rows) = {dev:.2e}")
o = R.get("DUST_fix")
if o is not None:
    o["I0"] = 3 * ((P0[1] - OMCDM) / o["h"] ** 2) * (o["h"] * HUB) ** 2      # DUST: 8piG rho = I0/a^3
RES["D0e"] = d0e
check("D0e_background_and_I0", ok_e, json.dumps(d0e, default=float), "rho_K <= 1e-6 relative at z <= 500; I0 <= 1e-8 relative")
save()

# ------------------------------------------------------------------ D0c: extraction validated on DUST
P("== D0c: extraction of delta_K, theta_K validated on DUST (delta_K must equal d_cdm, theta_K = 0)")
d0c = {}
okc = R.get("DUST_fix") is not None
if okc:
    o = R["DUST_fix"]
    for z in sorted(o["tk"]):
        e = extract(o, z, None, None, o["I0"], mutate_extraction=MUT)
        sel = e["kh"] <= 10.0
        dc = e["d_cdm"][sel]
        r1 = float(np.max(np.abs(e["dK"][sel] / dc - 1)))
        r2 = float(np.max(np.abs(3 * e["Hc"] * e["thK"][sel] / e["k"][sel] ** 2) / np.abs(dc)))
        d0c[f"{z:g}"] = {"max_rel_dK_vs_dcdm": r1, "max_theta_term_over_dcdm": r2}
        okc = okc and r1 <= 1e-5 and r2 <= 1e-5
    P("  " + "; ".join(f"z {k}: {v['max_rel_dK_vs_dcdm']:.1e} / {v['max_theta_term_over_dcdm']:.1e}" for k, v in d0c.items()))
RES["D0c"] = d0c
check("D0c_extraction_on_DUST", okc, f"worst over z: dK {max((v['max_rel_dK_vs_dcdm'] for v in d0c.values()), default=np.nan):.2e}, "
      f"theta term {max((v['max_theta_term_over_dcdm'] for v in d0c.values()), default=np.nan):.2e}",
      "max |dK/d_cdm - 1| <= 1e-5 and max |3 H theta_K/k^2|/|d_cdm| <= 1e-5 at every z, k <= 10 h/Mpc")
save()

# ------------------------------------------------------------------ D0d: normalisation
P("== D0d: P(k, z) = (2 pi^2/k^3) A_s (k/k_p)^(n_s - 1) d_m^2  (k_p = 0.05 Mpc^-1)")
KP = 0.05


def prim(o, params_):
    As = 1e-10 * math.exp(float(params_["ln10^{10}A_s"]))
    ns = float(params_["n_s"])
    return As, ns


d0d = {}
okd = True
for tag, par in (("CAP_best", parC), ("DUST_fix", fixed_params(0)), ("cap_fix", fixed_params(5, *POINTS["cap"])),
                 ("P1mu_fix", fixed_params(5, *POINTS["P1mu"])), ("P2mu_fix", fixed_params(5, *POINTS["P2mu"]))):
    o = R.get(tag)
    if o is None:
        okd = False
        continue
    As, ns = prim(o, par)
    worst = 0.0
    for z in sorted(o["tk"]):
        t, pk = o["tk"][z], o["pk"][z]
        kM = t["k (h/Mpc)"] * o["h"]
        Pm = 2 * math.pi ** 2 / kM ** 3 * As * (kM / KP) ** (ns - 1) * t["d_m"] ** 2 * o["h"] ** 3
        sel = t["k (h/Mpc)"] <= 10.0
        Pf = np.exp(lnP_at(pk, t["k (h/Mpc)"][sel]))
        worst = max(worst, float(np.max(np.abs(Pm[sel] / Pf - 1))))
    d0d[tag] = worst
    okd = okd and worst <= 1e-3
RES["D0d"] = d0d
check("D0d_normalisation", okd, "; ".join(f"{k}: {v:.2e}" for k, v in d0d.items()), "<= 1e-3 relative at every z, k <= 10 h/Mpc")
save()

# ------------------------------------------------------------------ D: linear dQ against the ceiling
P("== D: linear rest-frame dQ (gauge-invariant, Q6 D2) per point; line L = lambda_D^-1/2 / 3")


def dQ_stats(o, mu, lam, par):
    As, ns = prim(o, par)
    per_z = {}
    for z in sorted(o["tk"]):
        e = extract(o, z, mu, lam, o["I0"], mutate_extraction=MUT)
        st, a, k, Hc, w = e["st"], e["a"], e["k"], e["Hc"], e["w"]
        sel = e["kh"] <= 10.0
        cs2 = st["Q"] * st["Kp"] / (st["Q"] ** 2 * st["Kpp"] + 2 * k ** 2 / a ** 2)
        drest = e["dK"] + 3 * Hc * (1 + w) * e["thK"] / k ** 2
        dQr = st["rho8"] * cs2 * drest / st["Kp"]
        Pi = cs2 * (e["dK"] + 3 * Hc * (1 + w) * e["thK"] / k ** 2) - 3 * Hc * st["ca2"] * (1 + w) * e["thK"] / k ** 2
        dQs = st["rho8"] * Pi / st["Kp"]
        amp = np.sqrt(As * (k / KP) ** (ns - 1))
        Dr, Ds = (amp * np.abs(dQr))[sel], (amp * np.abs(dQs))[sel]
        lnk = np.log(k[sel])
        sr = float(np.sqrt(np.trapz(Dr ** 2, lnk)))
        ss = float(np.sqrt(np.trapz(Ds ** 2, lnk)))
        i = int(np.argmax(Dr))
        Phi_K = 1.5 * (st["rho8"] / 3) * a ** 2 * np.abs(drest) / k ** 2          # the khronon's own potential 4piG a^2 rho dK/k^2, for reference
        per_z[f"{z:g}"] = {"sigma_rest": sr, "max_mode_rest": float(Dr[i]), "k_at_max_hMpc": float(e["kh"][sel][i]),
                           "sigma_sync": ss, "max_mode_sync": float(Ds.max()), "Qbar_minus_1": st["Q"] - 1,
                           "headroom": st["headroom"], "headroom_ratio_3sigma": 3 * sr / st["headroom"],
                           "aM_hMpc": a * math.sqrt(st["Q"] ** 2 * st["Kpp"] / 2) / o["h"],
                           "max_mode_ownpotential_rest": float((amp * Phi_K)[sel].max())}
    S_rms = max(v["sigma_rest"] for v in per_z.values())
    S_mode = max(v["max_mode_rest"] for v in per_z.values())
    zr = max(per_z, key=lambda z_: per_z[z_]["sigma_rest"])
    zm = max(per_z, key=lambda z_: per_z[z_]["max_mode_rest"])
    return per_z, S_rms, S_mode, zr, zm


DRES = {}
for nm, (mu, lam) in POINTS.items():
    L = lam ** -0.5 / 3
    rows = {}
    for tag, par in ((f"{nm}_fix", fixed_params(5, mu, lam)),) + ((("CAP_best", parC),) if nm == "cap" else ()):
        o = R.get(tag)
        if o is None or "I0" not in o:
            rows[tag] = None
            continue
        per_z, S_rms, S_mode, zr, zm = dQ_stats(o, mu, lam, par)
        reading = "FAIL" if (S_rms > L and S_mode > L) else ("PASS" if (S_rms <= L and S_mode <= L) else "UNDECIDED")
        rows[tag] = {"per_z": per_z, "S_rms_max_z": S_rms, "z_at_S_rms": zr, "S_mode_max_kz": S_mode, "z_at_S_mode": zm,
                     "k_at_S_mode_hMpc": per_z[zm]["k_at_max_hMpc"], "line_L": L, "S_rms_over_L": S_rms / L,
                     "S_mode_over_L": S_mode / L, "sync_max_mode": max(v["max_mode_sync"] for v in per_z.values()),
                     "headroom_ratio_max": max(v["headroom_ratio_3sigma"] for v in per_z.values()), "reading": reading}
        P(f"  {tag}: max_z sigma_dQ,rest {S_rms:.3e} (z {zr}), max_(k,z) per-ln-k {S_mode:.3e} (z {zm}, k {per_z[zm]['k_at_max_hMpc']:.3g} h/Mpc) "
          f"vs L {L:.3e} -> S/L {S_rms / L:.3e} / {S_mode / L:.3e}: D = {reading}; sync-gauge max mode {rows[tag]['sync_max_mode']:.3e}; "
          f"headroom ratio (3 sigma, reported) max {rows[tag]['headroom_ratio_max']:.3e}")
        for zk in ("0", "3", "10", "37", "100", "500"):
            if zk in per_z:
                v = per_z[zk]
                P(f"      z {zk:>4s}: sigma_rest {v['sigma_rest']:.3e}, max mode {v['max_mode_rest']:.3e} at k {v['k_at_max_hMpc']:.3g}; "
                  f"Qbar-1 {v['Qbar_minus_1']:.3e}; headroom {v['headroom']:.3e}; aM {v['aM_hMpc']:.3g} h/Mpc")
    prim_tag = "CAP_best" if nm == "cap" else f"{nm}_fix"
    DRES[nm] = {"rows": rows, "primary": prim_tag, "D": rows[prim_tag]["reading"] if rows.get(prim_tag) else "UNDECIDED"}
RES["D"] = DRES
save()

# ------------------------------------------------------------------ F0a: L346's gate reproduced from its JSON
P("== F0a: L346's gate reproduced from its committed JSON")
L346 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L346_switch_forest_gate_results.json")))
runs346 = L346["numbers"]["runs"]


def r346(name, z):
    a = np.array(runs346[name]["pk"][z])
    b = np.array(runs346["lcdm"]["pk"][z])
    kk = b[:, 0]
    fo = (kk >= 1.0) & (kk <= 4.0)
    return kk[fo], (a[:, 1] / b[:, 1])[fo]


KB346 = r346("sw5_canon", "3.0")[0]
f0a = {}
for n in ("sw5_canon", "sw5_alt", "never_on"):
    for z in ("3.0", "2.0"):
        _, rr = r346(n, z)
        f0a[f"{n}_{z}"] = (float(rr.min()), float(rr.max()))
pass_sw5 = all(0.8 <= f0a[f"{n}_{z}"][0] and f0a[f"{n}_{z}"][1] <= 1.2 for n in ("sw5_canon", "sw5_alt") for z in ("3.0", "2.0"))
st346 = L346["numbers"]["F2"]
okf0a = (all(abs(f0a[f"{n}_{z}"][i] - st346[f"{n}_{z}"][i]) <= 1e-9 for n in ("sw5_canon", "sw5_alt") for z in ("3.0", "2.0") for i in (0, 1))
         and (not pass_sw5) and (L346["checks"][[c for c in L346["checks"] if c.startswith("F2")][0]]["ok"] is True)
         and all(f0a[f"never_on_{z}"] == (1.0, 1.0) for z in ("3.0", "2.0")))
RES["F0a"] = {"bands": f0a, "bins_hMpc": KB346.tolist(), "sw5_gate_passes": pass_sw5}
check("F0a_L346_reproduced", okf0a, f"bins {np.round(KB346, 2).tolist()}; sw5_canon z3 {f0a['sw5_canon_3.0'][0]:.4f}-{f0a['sw5_canon_3.0'][1]:.4f}, "
      f"sw5_alt z3 {f0a['sw5_alt_3.0'][0]:.4f}-{f0a['sw5_alt_3.0'][1]:.4f} -> gate {'PASS' if pass_sw5 else 'FAIL'} (L346: FAIL); "
      f"never_on {f0a['never_on_3.0']}", "band ends equal to L346's stored F2 to 1e-9; verdict FAIL; control exactly 1")

# ------------------------------------------------------------------ F0b: L319's strict line
h19 = 0.6736
Om19 = (0.02237 + 0.1200) / h19 ** 2
K_H19 = np.geomspace(0.02, 30.0, 44)
k5 = float(K_H19[int(np.argmin(np.abs(K_H19 - 5.0)))])


def T2_wdm(k_h, m_keV):                                  # L319 L169-171, verbatim formula
    alpha = 0.049 * m_keV ** -1.11 * (Om19 / 0.25) ** 0.11 * (h19 / 0.7) ** 1.22; nu = 1.12
    return (1 + (alpha * k_h) ** (2 * nu)) ** (-10 / nu)


T2_53 = float(T2_wdm(k5, 5.3))
RES["F0b"] = {"k5_hMpc": k5, "T2_5.3keV": T2_53, "L319_printed": 0.995,
              "T2_5.3keV_at_exactly_5.00_hMpc_reported_A1": float(T2_wdm(5.0, 5.3)),
              "note_A1": "L319 evaluates its 'k = 5 h/Mpc' line at its grid point nearest 5 (L184-185): k5 = 4.6199 h/Mpc; this lane does the same"}
check("F0b_L319_line", abs(T2_53 - 0.995) <= 5e-4, f"T^2_5.3keV(k = {k5:.4f} h/Mpc) = {T2_53:.5f} vs L319's printed 0.995", "within 5e-4")
save()

# ------------------------------------------------------------------ gate function (applied identically everywhere)


def gate(o, oref, label):
    out = {}
    for z in (3.0, 2.0):
        if o is None or oref is None or z not in o["pk"] or z not in oref["pk"]:
            out[f"{z:g}"] = None
            continue
        rb = np.exp(lnP_at(o["pk"][z], KB346) - lnP_at(oref["pk"][z], KB346))
        kk = oref["pk"][z][:, 0]
        fo = (kk >= 1.0) & (kk <= 4.0)
        rfull = np.exp(lnP_at(o["pk"][z], kk[fo]) - np.log(oref["pk"][z][fo, 1]))
        t5 = float(np.exp(lnP_at(o["pk"][z], np.array([k5]))[0] - lnP_at(oref["pk"][z], np.array([k5]))[0]))
        t500 = float(np.exp(lnP_at(o["pk"][z], np.array([5.0]))[0] - lnP_at(oref["pk"][z], np.array([5.0]))[0]))
        out[f"{z:g}"] = {"bins": rb.tolist(), "min": float(rb.min()), "max": float(rb.max()),
                         "full_grid_min": float(rfull.min()), "full_grid_max": float(rfull.max()), "T2_k5": t5,
                         "T2_at_exactly_5.00_hMpc_reported_A1": t500}
    ok = all(out[z] is not None for z in ("3", "2"))
    if not ok:
        return {"z": out, "F_L346": None, "F_L319_strict": None, "F_L319_loose": None, "worst_outside_0.5_2": None, "F": "UNDECIDED"}
    l346 = all(0.8 <= out[z]["min"] and out[z]["max"] <= 1.2 for z in ("3", "2"))
    l319s = all(out[z]["T2_k5"] >= T2_53 for z in ("3", "2"))
    l319l = all(out[z]["T2_k5"] >= 0.9 for z in ("3", "2"))
    far = any(out[z]["min"] < 0.5 or out[z]["max"] > 2.0 for z in ("3", "2"))
    F = "FAIL" if ((not l319l) or far) else ("PASS" if (l346 and l319s) else "UNDECIDED")
    z3 = {"F_L346_z3": 0.8 <= out["3"]["min"] and out["3"]["max"] <= 1.2, "F_L319_strict_z3": out["3"]["T2_k5"] >= T2_53,
          "F_L319_loose_z3": out["3"]["T2_k5"] >= 0.9}
    P(f"  {label}: z=3 bins " + " ".join(f"{v:.3g}" for v in out["3"]["bins"]) + f" | T2(k5) {out['3']['T2_k5']:.3g}; "
      f"z=2 bins " + " ".join(f"{v:.3g}" for v in out["2"]["bins"]) + f" | T2(k5) {out['2']['T2_k5']:.3g} -> L346 {'PASS' if l346 else 'FAIL'}, "
      f"L319 strict {'PASS' if l319s else 'FAIL'}, loose {'PASS' if l319l else 'FAIL'}, outside [0.5,2]: {far} => F = {F} "
      f"[A1 reported: T2 at k = 5.00: z3 {out['3']['T2_at_exactly_5.00_hMpc_reported_A1']:.4g}, z2 {out['2']['T2_at_exactly_5.00_hMpc_reported_A1']:.4g}; "
      f"k5 = {k5:.4f}: z3 {out['3']['T2_k5']:.4g}, z2 {out['2']['T2_k5']:.4g}]")
    return {"z": out, "F_L346": l346, "F_L319_strict": l319s, "F_L319_loose": l319l, "worst_outside_0.5_2": far, "F": F, "z3_only": z3}


# ------------------------------------------------------------------ F0c: the gate on LCDM through this pipeline
P("== F0c: the gate on LCDM through this lane's CLASS pipeline")
gD = gate(R.get("DUST_fix"), R.get("LCDM_fix"), "DUST(DBI binary) vs vanilla LCDM, P0")
gN = gate(R.get("N0_cap_1e30"), R.get("DUST_fix"), "DBI(cap, 1e30) vs DUST, P0")


def near1(g):
    return g["F"] == "PASS" and all(abs(v - 1) <= 1e-3 for z in ("3", "2") for v in g["z"][z]["bins"] + [g["z"][z]["T2_k5"]])


RES["F0c"] = {"DUST_vs_LCDM": gD, "N0_vs_DUST": gN}
check("F0c_gate_on_LCDM", near1(gD) and near1(gN),
      f"DUST/LCDM z3 {gD['z']['3']['min']:.6f}-{gD['z']['3']['max']:.6f}, T2(k5) {gD['z']['3']['T2_k5']:.6f}; "
      f"N0/DUST z3 {gN['z']['3']['min']:.6f}-{gN['z']['3']['max']:.6f}" if gD["z"].get("3") and gN["z"].get("3") else "missing",
      "every bin and T2(k5) within 1e-3 of 1 => gate PASS")
save()

# ------------------------------------------------------------------ F: the forest gate per point
P("== F: forest gate per point (linear P(k); L346 band [0.8,1.2] at z = 3 and 2; L319 T2(k5) strict / loose)")
FRES = {}
FRES["cap"] = {"primary": gate(R.get("CAP_best"), R.get("LCDM_best"), "cap (CMB best fit) vs LCDM best fit"),
               "fixed_reported": gate(R.get("cap_fix"), R.get("DUST_fix"), "cap (fixed P0) vs DUST")}
for nm in ("P1mu", "P2mu"):
    FRES[nm] = {"primary": gate(R.get(f"{nm}_fix"), R.get("DUST_fix"), f"{nm} (fixed P0) vs DUST")}
RES["F"] = FRES
# context: P/P_ref at z = 0 and z = 3
CTX = {}
for nm, (o, oref) in {"cap_best": (R.get("CAP_best"), R.get("LCDM_best")), "cap_fix": (R.get("cap_fix"), R.get("DUST_fix")),
                      "P1mu_fix": (R.get("P1mu_fix"), R.get("DUST_fix")), "P2mu_fix": (R.get("P2mu_fix"), R.get("DUST_fix"))}.items():
    if o is None or oref is None:
        continue
    CTX[nm] = {f"z{z:g}": {f"{k_:g}": float(np.exp(lnP_at(o["pk"][z], np.array([k_]))[0] - lnP_at(oref["pk"][z], np.array([k_]))[0]))
                           for k_ in (0.1, 0.3, 1.0, 3.0, 10.0)} for z in (0.0, 3.0) if z in o["pk"] and z in oref["pk"]}
    P(f"  context {nm}: P/P_ref " + "; ".join(f"{zk}: " + ", ".join(f"k{k_} {v:.3g}" for k_, v in d.items()) for zk, d in CTX[nm].items()))
RES["context_Pk_ratios"] = CTX
save()

# ------------------------------------------------------------------ G (inherited from S4) and the verdict
VC220 = (220.0 / 299792.458) ** 2
GRES = {}
for nm, (mu, lam) in POINTS.items():
    G = "FAIL" if mu >= 0.1 else ("PASS" if mu <= 0.03 else "NOT ON S4'S GRID")
    GRES[nm] = {"G": G, "lambda_D_times_vc2_squared_220kms": lam * VC220 ** 2,
                "note": "S4's guard is a quadratic-K static solve; DBI differs from quadratic by O(lambda_D (Q-1)^2) in galaxies"}
    P(f"  G {nm}: mu {mu:.4g} Mpc^-1 -> {G}; lambda_D (v^2/c^2)^2 at 220 km/s = {lam * VC220 ** 2:.2e}")
RES["G_inherited"] = GRES

repro_ok = all(RES["checks"][c]["pass"] for c in ("D0a_Q7_bestfits_reproduced", "D0b_lambda95_R_B", "D0c_extraction_on_DUST",
                                                  "D0d_normalisation", "D0e_background_and_I0", "F0a_L346_reproduced",
                                                  "F0b_L319_line", "F0c_gate_on_LCDM"))
PER = {}
for nm in POINTS:
    D_, F_ = DRES[nm]["D"], FRES[nm]["primary"]["F"]
    closers = [c for c, v in (("D", D_), ("F", F_)) if v == "FAIL"]
    PER[nm] = {"D": D_, "F": F_, "G": GRES[nm]["G"], "closed_by": closers, "passes_D_and_F": D_ == "PASS" and F_ == "PASS"}
if not repro_ok:
    vii = "UNDECIDED (a step-2 reproduction failed)"
elif all(PER[nm]["closed_by"] for nm in POINTS):
    used = sorted({c for nm in POINTS for c in PER[nm]["closed_by"]})
    vii = "DOOR CLOSED BY " + " AND ".join(used) + " (" + "; ".join(f"{nm}: {'+'.join(PER[nm]['closed_by'])}" for nm in POINTS) + ")"
elif any(PER[nm]["passes_D_and_F"] for nm in POINTS):
    vii = "OPEN BUT A KNOB (cannot be adopted): " + ", ".join(f"{nm} (G {PER[nm]['G']})" for nm in POINTS if PER[nm]["passes_D_and_F"])
else:
    vii = "UNDECIDED"
notG = [nm for nm in POINTS if PER[nm]["G"] != "FAIL"]
restricted = {nm: PER[nm] for nm in notG}
RES["verdict_ii"] = {"class": vii, "per_point": PER, "points_not_excluded_by_G": notG, "restricted_reading": restricted}
check("V_ii_verdict", True, f"{vii}; per point " + "; ".join(f"{nm}: D {v['D']}, F {v['F']}, G {v['G']}" for nm, v in PER.items()),
      "computed (the verdict is a result)")
save()
P(f"X4 STEP 2 COMPLETE: {NP}/{NC} checks PASS; elapsed {time.time() - T0:.0f} s; peak RSS self "
  f"{RES['peak_rss_GB_self']:.2f} GB, children {RES['peak_rss_GB_children']:.2f} GB")
sys.exit(0 if NP == NC else 1)
