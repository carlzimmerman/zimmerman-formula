#!/usr/bin/env python3
"""X34_recombination_release: is recombination a release boundary for the cold sector (the owner's idea)?

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (6c5d581400, committed alone first).
Q1 timing (CLASS: R1 patched turn-on, R2 stock idm-photon kinetic release; C2 likelihood; refits), Q2 relic speed
(Gilbert free streaming + X4/X22 forest rule; phase-space floor vs X24's c0), Q3 scale link (dimensional enumeration).

Run:  python3 -I x34_make_patch.py   (once; builds the R1 binary outside the repository)
      PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I x34_recombination_release.py
      X34_MUTATE=1 ... -> *_MUTATE outputs; K1, K2, K5, K7 must FAIL; Q1 refits skipped.
Build dir: $X34_BUILD (default <system temp>/x34_class_build). kappa = 1/2 FITTED; footings never pooled; no particle.
"""
import csv
import hashlib
import json
import math
import os
import re
import resource
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.io import FortranFile
from scipy.optimize import brentq, minimize_scalar

T0 = time.time()
MUT = os.environ.get("X34_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
BUILD = os.environ.get("X34_BUILD", os.path.join(tempfile.gettempdir(), "x34_class_build"))
X34B = os.path.join(BUILD, "class_x34", "class")
RUNS = os.path.join(BUILD, f"runs{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x34_recombination_release{TAG}.out"), "w")
RES = {"lane": "X34_recombination_release", "criteria": "6c5d581400", "date": "2026-10-24", "mutate": MUT,
       "checks": {}, "note": "kappa = 1/2 FITTED; footings never pooled; cold sector = field mass, never a particle"}
CHK = []
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUTF.write(s + "\n")
    OUTF.flush()


def check(name, ok, value, thr, must=True):
    """must = required outcome (True: PASS, False: FAIL)."""
    ok = bool(ok)
    CHK.append((name, ok, must))
    P(f"{name} {'PASS' if ok else 'FAIL'} (required {'PASS' if must else 'FAIL'}) {value} | {thr}")
    RES["checks"][name] = {"pass": ok, "required": "PASS" if must else "FAIL", "value": value, "threshold": thr}


def save():
    RES["elapsed_s"] = round(time.time() - T0, 1)
    RES["peak_rss_GB_python"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
    RES["peak_rss_GB_children"] = round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"x34_recombination_release_results{TAG}.json"), "w"), indent=1,
              default=float)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P(f"X34_recombination_release {'MUTATE run' if MUT else 'normal run'}; frozen 6c5d581400")
P("kappa = 1/2 FITTED; footings never pooled; cold sector = gravitating field mass, never a particle; not theory closed")
RES["binaries"] = {"vanilla_sha256": sha(VAN), "x34_sha256": sha(X34B),
                   "patch_sha256": sha(os.path.join(HERE, "x34_turnon.patch"))}
P(f"binaries: vanilla {RES['binaries']['vanilla_sha256'][:16]}, x34 {RES['binaries']['x34_sha256'][:16]}, "
  f"patch {RES['binaries']['patch_sha256'][:16]}")

# ------------------------------------------------------------------ C2's likelihood (read-only exec, as Q6)
C2 = os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology")
src = open(os.path.join(C2, "c2b_native_cmb.py")).read()
blk = src[src.index("# ---------------------------------------------------------------- likelihoods"):
          src.index("# ---------------------------------------------------------------- CLASS emulation")]
NS = {"np": np, "math": math, "os": os, "EXT": EXT, "FortranFile": FortranFile,
      "InterpolatedUnivariateSpline": InterpolatedUnivariateSpline}
exec(compile(blk, "c2b_native_cmb.py[likelihoods]", "exec"), NS)
C2RES = json.load(open(os.path.join(C2, "c2b_native_cmb_results.json")))["P5"]
TAU_HAT, SIG_TAU = C2RES["tau_hat"], C2RES["sig_tau"]
C7F = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")))["fits"]["LCDM"]
P0 = np.array([C7F["params"][k] for k in ("omega_b", "omega_dm(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau")])
A0 = C7F["A_planck"]
CHI2_LCDM = C7F["chi2"]["total"]

# ------------------------------------------------------------------ CLASS runner (Q6 precision: C7 A2 + start x0.25)
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
TCMB = 2.7255
NRUN = [0]
FAILMSG = {}


def run(name, binary, params, pk=False, zon=None, extra_out=False):
    p = {"output": "tCl,pCl,lCl,mPk" if pk else "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": 2508,
         "T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2,
         "thermodynamics_verbose": 1, "fourier_verbose": 1, "overwrite_root": "yes", **HIGH, **START, **params}
    if pk:
        p["P_k_max_h/Mpc"] = 10.0
    if extra_out:
        p["write_background"] = "yes"
        p["write_thermodynamics"] = "yes"
    root = os.path.join(RUNS, name + "_")
    p["root"] = root
    with open(root + ".ini", "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    env = dict(os.environ, OMP_NUM_THREADS="1")
    env.pop("X34_ZON", None)
    if zon is not None:
        env["X34_ZON"] = repr(float(zon))
    t_launch = time.time()
    r = subprocess.run(["nice", "-n", "15", binary, root + ".ini"], capture_output=True, text=True, env=env)
    NRUN[0] += 1
    if r.returncode != 0:
        FAILMSG[name] = (r.stdout + r.stderr).strip().splitlines()[-1][-300:] if (r.stdout + r.stderr).strip() else "?"
        return None
    pre = root + "_"                                                     # CLASS output prefix with overwrite_root
    assert os.path.getmtime(pre + "cl_lensed.dat") >= t_launch - 1, "stale-output guard"
    log = r.stdout
    cl = np.loadtxt(pre + "cl_lensed.dat")
    L = int(cl[-1, 0])
    f = (TCMB * 1e6) ** 2
    out = {"log": log, "root": pre}
    for key, col in (("tt", 1), ("ee", 2), ("te", 3), ("pp", 5)):
        arr = np.zeros(L + 1)
        arr[cl[:, 0].astype(int)] = cl[:, col] * (f if key != "pp" else 1.0)
        out[key] = arr
    m = re.search(r"found 'h = ([0-9.eE+-]+)'", log)
    out["h"] = float(m.group(1)) if m else float(p.get("h", np.nan))
    m = re.search(r"sigma8=([0-9.]+) for total matter", log)
    out["sigma8"] = float(m.group(1)) if m else np.nan
    m = re.search(r"radiation/matter equality at z = ([0-9.eE+-]+)", log)
    out["z_eq"] = float(m.group(1)) if m else np.nan
    m = re.search(r"recombination \(maximum of visibility function\) at z = ([0-9.eE+-]+)", log)
    out["z_rec"] = float(m.group(1)) if m else np.nan
    m = re.search(r"maximum of visibility function\) at z = [0-9.eE+-]+\s+corresponding to conformal time = [0-9.eE+-]+ Mpc\s+"
                  r"with comoving sound horizon = ([0-9.eE+-]+) Mpc", log)
    out["rs_rec"] = float(m.group(1)) if m else np.nan
    m = re.search(r"z_idm_dec = ([0-9.eE+-]+)", log)
    out["z_idm_dec"] = float(m.group(1)) if m else np.nan
    return out


def binned(o):
    return NS["binned"](o["tt"], o["te"], o["ee"])


def chi2_parts(o, A):
    Tb = binned(o)
    c = {"plik": NS["chi2_plik"](Tb, A), "lowTT": NS["chi2_lowTT"](o["tt"], A), "lowEE": NS["chi2_lowEE"](o["ee"], A),
         "Aprior": ((A - 1) / 0.0025) ** 2}
    c["total"] = sum(c.values())
    return c


def resid(Tb, A, tau):
    return np.concatenate((np.linalg.solve(NS["Lc"], NS["Xd"] - Tb / A**2), [(A - 1) / 0.0025, (tau - TAU_HAT) / SIG_TAU]))


def base(p):
    wb, wd, th, lnA, ns, tau = p
    return {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau, "omega_cdm": wd}


def peaks(o):
    tt = o["tt"]
    l = np.arange(len(tt))
    d = tt * l * (l + 1) / (2 * np.pi)
    p1 = float(np.max(d[180:261]))
    p3 = float(np.max(d[750:871]))
    return {"D1": p1, "D3": p3, "D3_over_D1": p3 / p1}


# ================================================================== STEP 0
P("\n== STEP 0 (stop rule)")
o_l = run("S0_lcdm", VAN, base(P0), pk=True, extra_out=True)
c_l = chi2_parts(o_l, A0)
check("S0-1_C7_LCDM_chi2", abs(c_l["total"] - CHI2_LCDM) <= 2.0,
      f"chi2 {c_l['total']:.3f} (plik {c_l['plik']:.2f}, lowTT {c_l['lowTT']:.2f}, lowEE {c_l['lowEE']:.2f}) vs C7 {CHI2_LCDM:.3f}",
      "|diff| <= 2")
S8L = o_l["sigma8"]
check("S0-2_C7_sigma8", abs(S8L / C7F["sigma8"] - 1) <= 2e-3, f"sigma8 {S8L:.6f} vs C7 {C7F['sigma8']:.6f}", "<= 2e-3")
o_off = run("S0_x34_off", X34B, base(P0), pk=True)
m = np.arange(len(o_l["tt"])) >= 2
dmax = max(float(np.max(np.abs(o_off[k][m] / o_l[k][m] - 1))) for k in ("tt", "ee", "pp"))
check("S0-3_patched_off_equals_vanilla", dmax <= 1e-4 and abs(o_off["sigma8"] / S8L - 1) <= 1e-5,
      f"max |dC/C| (TT,EE,pp) {dmax:.2e}; sigma8 {o_off['sigma8']:.6f}", "<= 1e-4; sigma8 <= 1e-5")
RES["S0"] = {"chi2_LCDM": c_l, "sigma8_LCDM": S8L, "h": o_l["h"], "z_eq": o_l["z_eq"], "z_rec": o_l["z_rec"],
             "rs_rec_Mpc": o_l["rs_rec"], "patched_off_maxdev": dmax, "peaks_LCDM": peaks(o_l)}
P(f"  LCDM: h {o_l['h']:.5f}, z_eq {o_l['z_eq']:.2f}, z_rec {o_l['z_rec']:.3f}, r_s(rec) {o_l['rs_rec']:.3f} Mpc, "
  f"D3/D1 {RES['S0']['peaks_LCDM']['D3_over_D1']:.4f}")

# S0-4: X22 forest gate (L319 family)
X22J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X22_cosmic_dust_window", "x22_cosmic_dust_window_results.json")))
X4J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X4_growth_native_cap", "x4_dbi_door_results.json")))
NU = 1.12


def khm_L319(alpha):
    return (4 ** (NU / 10) - 1) ** (1 / (2 * NU)) / alpha


ok4 = True
s04 = {}
for key in ("alpha_NF", "alpha_PASS"):
    a_ = X22J["step1"][key]["alpha_Mpc_h"]
    k_ = khm_L319(a_)
    lam = 2 * math.pi / k_
    s04[key] = {"k_hm": k_, "lambda_hm": lam}
    ok4 &= abs(k_ / X22J["step1"][key]["k_hm_hMpc"] - 1) <= 1e-6 and abs(lam / X22J["step1"][key]["lambda_hm_Mpc_h"] - 1) <= 1e-6
KB346 = np.array(X4J["F0a"]["bins_hMpc"])
K5 = X4J["F0b"]["k5_hMpc"]
T2_53 = X4J["F0b"]["T2_5.3keV"]
ok4 &= len(KB346) == 6 and abs(T2_53 - 0.99519) <= 1e-5
LAM_NF = s04["alpha_NF"]["lambda_hm"]
LAM_PASS = s04["alpha_PASS"]["lambda_hm"]
LAM_LOOSE = 2 * math.pi / khm_L319(X22J["step1"]["alpha_lines"]["bin_0.5"])
check("S0-4_X22_forest_gate", ok4, f"lambda_hm NF {LAM_NF:.5f}, PASS {LAM_PASS:.5f} Mpc/h; bins {np.round(KB346, 3).tolist()}; "
      f"T2_5.3keV(k5 {K5:.4f}) {T2_53:.6f}; loosest (bin 0.5) lambda {LAM_LOOSE:.4f}", "<= 1e-6 rel")
RES["S0"]["forest"] = {**s04, "lambda_loose_bin05": LAM_LOOSE, "bins": KB346.tolist(), "k5": K5, "T2_53": T2_53}


def forest_class(t2bins_by_z, t2k5_by_z):                                # X22 verbatim
    allbins = [v for z in t2bins_by_z for v in t2bins_by_z[z]]
    k5s = list(t2k5_by_z.values())
    if min(k5s) < 0.9 or min(allbins) < 0.5 or max(allbins) > 2.0:
        return "FAIL"
    if all(0.8 <= v <= 1.2 for v in allbins) and min(k5s) >= T2_53:
        return "PASS"
    return "UNDECIDED"


# S0-5: X24 c0 and field rows (X24's load() and calib(), copied with provenance: x24_dwarf_velocity_floor.py L34-69)
X24J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X24_dwarf_velocity_floor", "x24_dwarf_velocity_floor_results.json")))
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping",
                                            "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))
ECOL, SCOL = "Delta[iso AQUAL L*0]", "sdMC[iso AQUAL L*0]"


def load(foot, classes):
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in classes:
            continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b
        E = float(r[ECOL])
        out.append(dict(name=r["name"], cls=r["cls"], E=E, s=float(r[SCOL]), sc=sc, siso=sc * 10 ** (-E / 2),
                        rh=float(r["rh_pc"])))
    return out


def chi2_x24(R, c0):
    E = np.array([q["E"] for q in R]); s = np.array([q["s"] for q in R]); si = np.array([q["siso"] for q in R])
    return float(np.sum(((E - np.log10(1.0 + (c0 / si) ** 2)) / s) ** 2))


C0 = {}
ok5 = True
for f in FOOT:
    FLD = load(f, ("LG field",))
    res_ = minimize_scalar(lambda c: chi2_x24(FLD, c), bounds=(0.0, 20.0), method="bounded", options={"xatol": 1e-6})
    c0 = float(res_.x)
    B = X24J["footings"][f]["B"]
    C0[f] = {"c0": B["c0"], "lo": B["c0_lo"], "hi": B["c0_hi"], "c0_rederived": c0, "N_field": len(FLD)}
    ok5 &= len(FLD) == 13 and abs(c0 - B["c0"]) <= 1e-9
check("S0-5_X24_c0_and_rows", ok5, {f: (round(C0[f]["c0_rederived"], 6), C0[f]["N_field"]) for f in C0}, "c0 equal to 1e-9; N = 13")
RES["S0"]["c0"] = C0

if not all(ok for n, ok, mu in CHK):
    P("STEP 0 FAILED: lane stops UNDECIDED")
    RES["verdict"] = "UNDECIDED (Step 0 failed)"
    save()
    sys.exit(1)

# ================================================================== K checks on the machinery
P("\n== machinery checks")
# K1: energy identity on the R1 background at z_on = 1100
o_k1 = run("K1_r1_1100", X34B, base(P0), zon=1100.0, extra_out=True)
bg = np.loadtxt(o_k1["root"] + "background.dat")
hdr = [ln for ln in open(o_k1["root"] + "background.dat") if ln.startswith("#")][-1]
cols = {re.sub(r"^\d+:", "", c.strip()): i for i, c in enumerate(re.split(r"\s{2,}", hdr.lstrip("#").strip()))}
z_b = bg[:, cols["z"]]
rc = bg[:, cols["(.)rho_cdm"]]
others = sum(bg[:, cols[k]] for k in ("(.)rho_g", "(.)rho_b", "(.)rho_cdm", "(.)rho_lambda", "(.)rho_ur"))
rres = bg[:, cols["(.)rho_tot"]] - others
x_b = -np.log(1 + z_b)
sel = (z_b > 1100 * math.exp(-0.5)) & (z_b < 1100 * math.exp(0.5))
tot = rc + (0.0 if MUT else rres)
dtot = np.gradient(tot, x_b)
viol = float(np.max(np.abs(dtot[sel] + 3 * rc[sel])) / np.max(3 * rc[sel]))
check("K1_energy", viol <= 2e-3, f"max |d(rho_c+rho_res)/dlna + 3 rho_c| / max 3 rho_c = {viol:.2e} over the turn-on"
      + (" [MUTATE: rho_res dropped]" if MUT else ""), "<= 2e-3", must=not MUT)
# K5: the turn-on bites
o_k5 = run("K5_r1_1100_tt", VAN if MUT else X34B, base(P0), zon=1100.0)
r810 = float(o_k5["tt"][810] / o_l["tt"][810])
check("K5_turnon_bites", abs(r810 - 1) > 0.01, f"TT(810) ratio z_on=1100 / LCDM = {r810:.4f}" + (" [MUTATE: vanilla binary]" if MUT else ""),
      "|ratio - 1| > 1 %", must=not MUT)

# R2: u_idm_g for a target kinetic decoupling z_d (CLASS's own formula, thermodynamics.c L157)
_G, _c, _eV, _Mpc, _sig = 6.67428e-11, 2.99792458e8, 1.602176487e-19, 3.085677581282e22, 6.6524616e-29
Hz_b = bg[:, cols["H [1/Mpc]"]]
o_lb = np.loadtxt(o_l["root"] + "background.dat")
H_l = o_lb[:, cols["H [1/Mpc]"]]
z_l = o_lb[:, cols["z"]]
rg_l = o_lb[:, cols["(.)rho_g"]]
H0_l = float(np.interp(0.0, z_l[::-1], H_l[::-1]))
FIDM = 0.9999


def u_for_zd(zd, p=P0, hh=None):
    hh = o_l["h"] if hh is None else hh
    Om_idm = FIDM * p[1] / hh ** 2
    Cpref = 3. / 8. / math.pi / _G * Om_idm * H0_l ** 2 * _c ** 4 * _sig / 1.e11 / _eV / _Mpc   # dmu = Cpref u (1+z)^2
    Hz = float(np.interp(zd, z_l[::-1], H_l[::-1]))
    rg = float(np.interp(zd, z_l[::-1], rg_l[::-1]))
    rho_idm = Om_idm * H0_l ** 2 * (1 + zd) ** 3
    S_idm = 4. / 3. * rg / rho_idm
    aH = Hz / (1 + zd)
    return aH / (S_idm * Cpref * (1 + zd) ** 2)


def r2params(p, u):
    return {**base(p), "f_idm": FIDM, "u_idm_g": u, "n_index_idm_g": 0}


u2500 = u_for_zd(2500.0)
o_k4 = run("K4_r2_2500", VAN, r2params(P0, u2500), extra_out=True)
th = np.loadtxt(o_k4["root"] + "thermodynamics.dat")
thh = [ln for ln in open(o_k4["root"] + "thermodynamics.dat") if ln.startswith("#")][-1]
tcols = {re.sub(r"^\d+:", "", c.strip()): i for i, c in enumerate(re.split(r"\s{2,}", thh.lstrip("#").strip()))}
zt = th[:, tcols["z"]]
assert np.all(np.diff(zt) > 0) and np.all(np.diff(z_l) < 0), "table ordering"
dmu = th[:, tcols["dmu_idm_g"]]
bg4 = np.loadtxt(o_k4["root"] + "background.dat")
z4 = bg4[:, cols["z"]]
hdr4 = [ln for ln in open(o_k4["root"] + "background.dat") if ln.startswith("#")][-1]
cols4 = {re.sub(r"^\d+:", "", c.strip()): i for i, c in enumerate(re.split(r"\s{2,}", hdr4.lstrip("#").strip()))}


def bgi(col, z):
    return float(np.interp(z, z4[::-1], bg4[:, cols4[col]][::-1]))


def rate_ratio(z):
    S = 4. / 3. * bgi("(.)rho_g", z) / bgi("(.)rho_idm", z)
    return S * float(np.interp(z, zt, dmu)) / (bgi("H [1/Mpc]", z) / (1 + z))      # thermodynamics.dat runs z = 0 upwards


rr = rate_ratio(2500.0)
check("K4_idm_rate", abs(rr - 1) <= 0.02, f"CLASS S_idm_g dmu_idm_g/(a'/a) at z_d 2500 = {rr:.4f} (u {u2500:.4e}); "
      f"n_index 0", "within 2 %")

# Gilbert free-streaming solver (Q2)
h_l = o_l["h"]
Om_l = (P0[0] + P0[1]) / h_l ** 2
fc_l = P0[1] / (P0[0] + P0[1])
zeq = o_l["z_eq"]
lnH = InterpolatedUnivariateSpline(-np.log(1 + z_l), np.log(H_l), k=3)        # background.dat runs from high z to 0
CKMS = 299792.458
GSIGN = -1.0 if MUT else 1.0


def gilbert(kh, sig0_kms, zd, zouts=(3.0, 2.0, 0.0), N=2000, sign=1.0):
    """delta_m(k, z) for a Maxwellian relic (1D comoving dispersion sig0 today) + cold baryons, from z_d."""
    xd = -math.log(1 + zd)
    x = np.linspace(xd, 0.0, N)
    a = np.exp(x)
    H = np.exp(lnH(x))
    dsdx = 1.0 / (a ** 2 * H)
    s = np.concatenate(([0.0], np.cumsum(0.5 * (dsdx[1:] + dsdx[:-1]) * np.diff(x))))
    ds = np.diff(s)
    w = np.zeros(N)
    w[0] = 0.5 * ds[0]
    w[1:-1] = 0.5 * (ds[:-1] + ds[1:])
    Asrc = sign * 1.5 * H0_l ** 2 * Om_l * a
    y = (1 + zd) / (1 + zeq)
    fd = y / (y + 2. / 3.)
    dprime = fd * a[0] ** 2 * H[0]
    k = np.atleast_1d(kh) * h_l
    sg = sig0_kms / CKMS
    Nk = len(k)
    dc = np.zeros((Nk, N))
    db = np.zeros((Nk, N))
    src = np.zeros((Nk, N))
    for i in range(N):
        Ds = s[i] - s[:i]
        Fb = 1.0 + dprime * s[i]
        Kc0 = np.exp(-0.5 * (k * sg * s[i]) ** 2)
        if i == 0:
            dc[:, 0] = 1.0
            db[:, 0] = 1.0
        else:
            Kc = np.exp(-0.5 * (k[:, None] * sg * Ds[None, :]) ** 2)
            integ_b = np.sum(src[:, :i] * (w[:i] * Ds)[None, :], axis=1)
            integ_c = np.sum(src[:, :i] * (w[:i] * Ds)[None, :] * Kc, axis=1)
            dc[:, i] = Fb * Kc0 + integ_c
            db[:, i] = Fb + integ_b
        src[:, i] = Asrc[i] * (fc_l * dc[:, i] + (1 - fc_l) * db[:, i])
    dm = fc_l * dc + (1 - fc_l) * db
    out = {}
    for zo in zouts:
        xo = -math.log(1 + zo)
        out[zo] = np.array([np.interp(xo, x, dm[j]) for j in range(Nk)])
    return out


def growth_ode(zd, zouts=(3.0, 0.0)):
    y = (1 + zd) / (1 + zeq)
    fd = y / (y + 2. / 3.)

    def rhs(x, v):
        a = math.exp(x)
        H = math.exp(lnH(x))
        dlnH = float(lnH.derivative()(x))
        Omx = Om_l * H0_l ** 2 * a ** -3 / H ** 2
        return [v[1], -(2 + dlnH) * v[1] + 1.5 * Omx * v[0]]

    sol = solve_ivp(rhs, (-math.log(1 + zd), 0.0), [1.0, fd], rtol=1e-10, atol=1e-12, dense_output=True)
    return {zo: float(sol.sol(-math.log(1 + zo))[0]) for zo in zouts}


g0 = gilbert([0.1], 0.0, 1100.0, zouts=(3.0, 0.0), sign=GSIGN)
gode = growth_ode(1100.0)
dev2 = max(abs(g0[z][0] / gode[z] - 1) for z in (3.0, 0.0))
check("K2_growth", dev2 <= 1e-3, f"Gilbert(sigma0=0)/ODE - 1 at z=3, 0: {dev2:.2e}" + (" [MUTATE: gravity sign flipped]" if MUT else ""),
      "<= 1e-3", must=not MUT)
ad = 1 / 1101.
kJd = math.sqrt(1.5 * Om_l) * H0_l * math.sqrt(ad) / (0.05 / CKMS) / h_l
gj = gilbert([0.1, 10 * kJd], 0.05, 1100.0, zouts=(0.0,))
gj0 = gilbert([0.1, 10 * kJd], 0.0, 1100.0, zouts=(0.0,))
Tj = gj[0.0] / gj0[0.0]
check("K3_jeans", Tj[0] > 0.99 and abs(Tj[1]) < 0.1, f"T(0.1 h/Mpc) {Tj[0]:.5f}; T(10 k_J,d = {10 * kJd:.1f} h/Mpc) {Tj[1]:.2e}",
      "> 0.99 and < 0.1")
RES_CK = {"growth_dev": dev2, "kJd_hMpc": kJd, "T_jeans": Tj.tolist()}

# K6: TG identity; K7: a0 vs Lambda
RHO_C0 = P0[1] * 2.77536627e11 * 1e-18                                   # Msun/pc^3 (omega_c rho_crit/h^2)
check("K6_TG", abs(0.05 * (RHO_C0 / RHO_C0) ** (1 / 3) / 0.05 - 1) < 1e-12, f"sigma_min(rho_c0) = sigma0; rho_c0 {RHO_C0:.4e} Msun/pc^3",
      "identity")
OmL = 1 - Om_l - float(np.interp(0.0, z_l[::-1], (o_lb[:, cols["(.)rho_g"]] + o_lb[:, cols["(.)rho_ur"]])[::-1])) / H0_l ** 2
H0_SI = h_l * 100 * 1e3 / 3.085677581e22
LAM = 3 * OmL * H0_SI ** 2 / _c ** 2
a0_from_L = _c ** 2 * math.sqrt(LAM / ((16 if MUT else 32) * math.pi))
rat7 = {f: FOOT[f] / a0_from_L for f in FOOT}
check("K7_a0_lambda", abs(rat7["canonical"] - 1) <= 0.05, f"a0/(c^2 sqrt(Lambda/32pi)) canonical {rat7['canonical']:.4f}, alt "
      f"{rat7['alt']:.4f} (Lambda {LAM:.4e} m^-2, Omega_L {OmL:.5f})" + (" [MUTATE: 16 pi]" if MUT else ""), "canonical within 5 %",
      must=not MUT)
RES["machinery"] = {**RES_CK, "K1_violation": viol, "K5_TT810_ratio": r810, "K4_rate_ratio": rr, "u_2500": u2500,
                    "Lambda_m2": LAM, "a0_over_Lambda_a0": rat7}

if MUT:
    good = all(ok == mu for n, ok, mu in CHK)
    RES["verdict"] = "MUTATE run: checks only"
    save()
    P(f"\nX34 MUTATE COMPLETE: {sum(ok == mu for n, ok, mu in CHK)}/{len(CHK)} checks have their required outcome; "
      f"failing as required: {[n for n, ok, mu in CHK if not mu and not ok]}")
    sys.exit(0 if good else 1)

# ================================================================== Q1 timing
P("\n== Q1 timing (footing-independent)")
STEP = np.array([1e-4, 1e-3, 2e-4, 0.01, 0.004, 0.004])
GRID = (1100.0, 1500.0, 2500.0, 4000.0, 7000.0, 12000.0, 20000.0, 50000.0, 100000.0)


def theory(reading, z, p, pk=False, tag="fit"):
    nm = f"{reading}_{int(z)}_{tag}"
    if reading == "R1":
        return run(nm, X34B, base(p), pk=pk, zon=z)
    return run(nm, VAN, r2params(p, U2[z]), pk=pk)


U2 = {z: u_for_zd(z) for z in GRID}


def fit(reading, z):
    n0 = NRUN[0]
    p, A = P0.copy(), A0
    o0 = theory(reading, z, p, pk=True, tag="start")
    if o0 is None:
        return {"status": "CLASS_FAIL", "msg": FAILMSG.get(f"{reading}_{int(z)}_start")}
    c0 = chi2_parts(o0, A)
    rec = {"start_chi2": c0["total"], "start_dchi2": c0["total"] - CHI2_LCDM, "start_sigma8": o0["sigma8"],
           "start_peaks": peaks(o0)}
    if c0["total"] - CHI2_LCDM < 4:
        rec.update({"refit": False, "dchi2": c0["total"] - CHI2_LCDM, "sigma8": o0["sigma8"], "params": p.tolist(), "A": A,
                    "chi2": c0, "converged": True, "peaks": peaks(o0), "runs": NRUN[0] - n0, "h": o0["h"]})
        return rec
    Tb = binned(o0)
    r = resid(Tb, A, p[5])
    J = np.zeros((615, 7))
    for kx in range(6):
        pp = p.copy()
        pp[kx] += STEP[kx]
        ok_ = theory(reading, z, pp, tag="jac")
        if ok_ is None:
            pp[kx] -= 2 * STEP[kx]
            ok_ = theory(reading, z, pp, tag="jac")
            sgn = -1
        else:
            sgn = 1
        J[:613, kx] = sgn * -np.linalg.solve(NS["Lc"], (binned(ok_) - Tb) / A ** 2) / STEP[kx]
    J[614, 5] = 1 / SIG_TAU
    J[:613, 6] = np.linalg.solve(NS["Lc"], 2 * Tb / A ** 3)
    J[613, 6] = 1 / 0.0025
    hist = []
    stop_rule = False
    for it in range(8):
        cs = r @ r
        d = -np.linalg.lstsq(J, r, rcond=None)[0]
        lam = 1.0
        while True:
            pn, An = p + lam * d[:6], A + lam * d[6]
            on = theory(reading, z, pn, tag="ls")
            rn = None if on is None else resid(binned(on), An, pn[5])
            cn = np.inf if rn is None else rn @ rn
            if cn <= cs or lam < 1 / 16:
                break
            lam /= 2
        if cn > cs:
            hist.append({"it": it + 1, "steered": cs, "fall": 0.0, "step": lam})
            stop_rule = True
            break
        dx = np.concatenate((pn - p, [An - A]))
        J = J + np.outer(rn - r - J @ dx, dx) / (dx @ dx)                # Broyden rank-1
        p, A, r = pn, An, rn
        hist.append({"it": it + 1, "steered": cn, "fall": cs - cn, "step": lam})
        P(f"    {reading} z={z:g}: it{it + 1} steered {cs:.2f} -> {cn:.2f} (step {lam})")
        if cs - cn < 0.05:
            stop_rule = True
            break
    of = theory(reading, z, p, pk=True, tag="final")
    cf = chi2_parts(of, A)
    rec.update({"refit": True, "dchi2": cf["total"] - CHI2_LCDM, "sigma8": of["sigma8"], "params": p.tolist(), "A": A,
                "chi2": cf, "gn": hist, "stop_rule": stop_rule, "last_fall": hist[-1]["fall"] if hist else 0.0,
                "peaks": peaks(of), "runs": NRUN[0] - n0, "h": of["h"]})
    rec["converged"] = stop_rule or 3 * rec["last_fall"] < rec["dchi2"] - 25
    if reading == "R2":
        rec["z_idm_dec_CLASS"] = of["z_idm_dec"]
    return rec


def classify(rec):
    if rec.get("status") == "CLASS_FAIL":
        return "UNDECIDED", "CLASS failed"
    s8ok = abs(rec["sigma8"] / S8L - 1) <= 0.05
    if rec["dchi2"] < 4 and s8ok:
        return "PASS", ""
    if not s8ok:
        return "EXCLUDED", "sigma8" + (" only" if rec["dchi2"] <= 25 else " + chi2")
    if rec["dchi2"] > 25 and rec["converged"]:
        return "EXCLUDED", "chi2"
    return "UNDECIDED", "between lines" if rec["dchi2"] <= 25 else "chi2 > 25 not converged"


Q1 = {}
for reading in ("R1", "R2"):
    Q1[reading] = {}
    for z in sorted(GRID, reverse=True):
        rec = fit(reading, z)
        cl_, why = classify(rec)
        rec["class"], rec["why"] = cl_, why
        Q1[reading][str(int(z))] = rec
        if rec.get("status") == "CLASS_FAIL":
            P(f"  {reading} z={z:g}: CLASS FAIL {rec.get('msg')}")
        else:
            P(f"  {reading} z={z:g}: start dchi2 {rec['start_dchi2']:+.2f}; final dchi2 {rec['dchi2']:+.2f} (refit {rec['refit']}, "
              f"conv {rec['converged']}); sigma8 {rec['sigma8']:.4f} (ratio {rec['sigma8'] / S8L:.4f}); D3/D1 "
              f"{rec['peaks']['D3_over_D1']:.4f} (LCDM {RES['S0']['peaks_LCDM']['D3_over_D1']:.4f}); runs {rec['runs']} -> {cl_} {why}")
        RES["Q1"] = Q1
        save()


def summarise(reading):
    recs = Q1[reading]
    zs = sorted(GRID)
    allowed = None
    for i, z in enumerate(zs):
        if all(recs[str(int(zz))]["class"] == "PASS" for zz in zs[i:]):
            allowed = z
            break
    excl = [z for z in zs if recs[str(int(z))]["class"] == "EXCLUDED"]
    zx = max(excl) if excl else None

    def cross(line):
        pts = [(math.log(z), recs[str(int(z))].get("dchi2", np.nan)) for z in zs]
        for (l1, d1), (l2, d2) in zip(pts[:-1], pts[1:]):
            if np.isfinite(d1) and np.isfinite(d2) and d1 > line >= d2:
                return math.exp(l1 + (line - d1) * (l2 - l1) / (d2 - d1))
        return None

    c1500 = recs["1500"]["class"]
    q = "PASS" if (allowed is not None and allowed <= 1500) else ("EXCLUDED" if c1500 == "EXCLUDED" else "UNDECIDED")
    return {"z_on_allowed": allowed, "z_on_excl": zx, "z_cross_dchi2_4": cross(4.0), "z_cross_dchi2_25": cross(25.0),
            "margin_allowed_over_1100": (allowed / 1100.0) if allowed else None, "class": q,
            "dchi2_1100": recs["1100"].get("dchi2"), "dchi2_1500": recs["1500"].get("dchi2")}


# reported only (not graded): R2 near recombination with CLASS's idm_g TCA trigger raised (CLASS refuses at its default
# 0.01 because the idm opacity exceeds 1 % of Thomson; the TCA is then outside its validated regime)
SENS = {}
for z in (1100.0, 1500.0):
    o_s = run(f"R2sens_{int(z)}", VAN, {**r2params(P0, U2[z]), "tight_coupling_trigger_tau_c_over_tau_dmu_idm_g": 1e6}, pk=True)
    if o_s is None:
        SENS[str(int(z))] = {"status": "CLASS_FAIL", "msg": FAILMSG.get(f"R2sens_{int(z)}")}
    else:
        SENS[str(int(z))] = {"dchi2_start": chi2_parts(o_s, A0)["total"] - CHI2_LCDM, "sigma8": o_s["sigma8"], "peaks": peaks(o_s)}
    P(f"  R2 sensitivity (TCA trigger raised, reported only) z_d={z:g}: {SENS[str(int(z))]}")
RES["Q1_R2_trigger_sensitivity_reported"] = SENS

Q1S = {r_: summarise(r_) for r_ in ("R1", "R2")}
RES["Q1_summary"] = Q1S
for r_ in Q1S:
    P(f"  {r_}: z_on,allowed {Q1S[r_]['z_on_allowed']}; z_on,excl {Q1S[r_]['z_on_excl']}; dchi2 crosses 25 at z "
      f"{Q1S[r_]['z_cross_dchi2_25']}, 4 at z {Q1S[r_]['z_cross_dchi2_4']}; margin {Q1S[r_]['margin_allowed_over_1100']} -> Q1 {Q1S[r_]['class']}")
save()

# ================================================================== Q2 relic speed
P("\n== Q2 relic speed")
KGRID = np.exp(np.linspace(math.log(0.5), math.log(2000.0), 70))
KF = np.concatenate((KB346, [K5]))


G0C = {}


def ref0(kk, zd, zouts):
    key = (tuple(np.round(kk, 12)), zd, zouts)
    if key not in G0C:
        G0C[key] = gilbert(kk, 0.0, zd, zouts=zouts)
    return G0C[key]


def forest_of(sig, zd):
    g = gilbert(KF, sig, zd, zouts=(3.0, 2.0))
    g0_ = ref0(KF, zd, (3.0, 2.0))
    T2 = {zz: (g[zz] / g0_[zz]) ** 2 for zz in (3.0, 2.0)}
    return forest_class({str(int(zz)): T2[zz][:6].tolist() for zz in T2}, {str(int(zz)): float(T2[zz][6]) for zz in T2}), T2


def lam_hm(sig, zd, zo=3.0):
    g = gilbert(KGRID, sig, zd, zouts=(zo,))[zo]
    g0_ = ref0(KGRID, zd, (zo,))[zo]
    T = g / g0_
    idx = np.where(T < 0.5)[0]
    if len(idx) == 0:
        return float("nan")
    i = idx[0]
    if i == 0:
        return 2 * math.pi / KGRID[0]
    l1, l2 = math.log(KGRID[i - 1]), math.log(KGRID[i])
    kh = math.exp(l1 + (0.5 - T[i - 1]) * (l2 - l1) / (T[i] - T[i - 1]))
    return 2 * math.pi / kh


def bisect_sig(pred, lo=1e-5, hi=30.0, it=40):
    """largest sig with pred(sig) True, assuming monotone (True below, False above)."""
    if not pred(lo):
        return 0.0
    if pred(hi):
        return hi
    for _ in range(it):
        mid = math.sqrt(lo * hi)
        if pred(mid):
            lo = mid
        else:
            hi = mid
        if hi / lo < 1.0005:
            break
    return lo


# dwarf densities (field dwarfs; footing-independent rows) and ultra-faints (reported)
GPC = 4.30091e-3                                                         # pc (km/s)^2 / Msun


def rho_half(q):
    r12 = 4. / 3. * q["rh"]
    return 9 * q["sc"] ** 2 / (4 * math.pi * GPC * r12 ** 2)


DW = {}
for f in FOOT:
    fld = load(f, ("LG field",))
    ufd = load(f, ("MW ultra-faint",))
    Df = np.array([rho_half(q) / RHO_C0 for q in fld])
    Du = np.array([rho_half(q) / RHO_C0 for q in ufd])
    DW[f] = {"Delta_field": Df, "Delta_ufd": Du}
P(f"  rho_c0 {RHO_C0:.4e} Msun/pc^3; field-dwarf Delta = rho_1/2/rho_c0: min {DW['canonical']['Delta_field'].min():.3e}, "
  f"median {np.median(DW['canonical']['Delta_field']):.3e}, max {DW['canonical']['Delta_field'].max():.3e}; "
  f"ultra-faints median {np.median(DW['canonical']['Delta_ufd']):.3e}")

ZD_GRADE = (1100.0, 1500.0)
zd_rep = [zeq]
if Q1S["R2"]["z_on_allowed"]:
    zd_rep.append(float(Q1S["R2"]["z_on_allowed"]))
Q2 = {"zd": {}, "footings": {}}
KTD = 8.617333262e-5 * TCMB                                              # eV per (1+z)
for zd in list(ZD_GRADE) + zd_rep:
    sPASS = bisect_sig(lambda s_: forest_of(s_, zd)[0] == "PASS")
    sNF = bisect_sig(lambda s_: forest_of(s_, zd)[0] != "FAIL")
    sLOOSE = bisect_sig(lambda s_: not (lam_hm(s_, zd) > LAM_LOOSE))
    lamNF = lam_hm(sNF, zd)
    sLAM = bisect_sig(lambda s_: not (lam_hm(s_, zd) > LAM_NF))
    Q2["zd"][f"{zd:.1f}"] = {"sig0_PASS": sPASS, "sig0_NF": sNF, "sig0_loose": sLOOSE, "lambda_hm_at_sig0_NF": lamNF,
                             "sig0_at_lambda_forest_0.417": sLAM}
    P(f"  z_d {zd:.0f}: forest sigma0,PASS {sPASS:.4e}, sigma0,NF {sNF:.4e} (lambda_hm z3 {lamNF:.3f} Mpc/h), "
      f"sigma0 at lambda_hm = 0.417: {sLAM:.4e}, sigma0,loose {sLOOSE:.4e} km/s")
    save()

for f in FOOT:
    c = C0[f]
    Df = DW[f]["Delta_field"]
    lo, hi = c["lo"] / Df.max() ** (1 / 3), c["hi"] / Df.min() ** (1 / 3)
    cen = c["c0"] / np.median(Df) ** (1 / 3)
    lo_w, hi_w = 3.41 / Df.max() ** (1 / 3), 5.14 / Df.min() ** (1 / 3)
    FF = {"floor_interval_sig0": [lo, hi], "floor_central_sig0": cen, "floor_widest_sig0": [lo_w, hi_w], "zd": {}}
    any_pass, any_loose = False, False
    for zd in list(ZD_GRADE) + zd_rep:
        zz = Q2["zd"][f"{zd:.1f}"]
        inter_NF = [lo, min(hi, zz["sig0_NF"])]
        inter_P = [lo, min(hi, zz["sig0_PASS"])]
        inter_L = [lo_w, min(hi_w, zz["sig0_loose"])]
        ne = inter_NF[0] <= inter_NF[1]
        row = {"intersection_NF": inter_NF if ne else None,
               "intersection_strict": inter_P if inter_P[0] <= inter_P[1] else None,
               "intersection_loosest": inter_L if inter_L[0] <= inter_L[1] else None}
        if ne:
            sd = np.array(inter_NF) * (1 + zd)
            row["sigma_d_kms"] = sd.tolist()
            row["e_d_km2s2"] = (1.5 * sd ** 2).tolist()
            row["mu_c2_eV"] = (KTD * (1 + zd) * (CKMS / sd) ** 2).tolist()[::-1]
            row["NR_ok"] = bool(min(row["mu_c2_eV"]) > 30 * KTD * (1 + zd))
        row["ufd_floor_at_central_kms"] = float(cen * np.median(DW[f]["Delta_ufd"]) ** (1 / 3))
        row["floor_at_sig0_NF_field_median_kms"] = float(zz["sig0_NF"] * np.median(Df) ** (1 / 3))
        FF["zd"][f"{zd:.1f}"] = row
        if zd in ZD_GRADE:
            any_pass |= ne
            any_loose |= row["intersection_loosest"] is not None
        P(f"  [{f}] z_d {zd:.0f}: floor sigma0 in [{lo:.3e}, {hi:.3e}] (central {cen:.3e}); forest NF <= {zz['sig0_NF']:.3e} "
          f"-> intersection {row['intersection_NF']}; strict {row['intersection_strict']}; loosest {row['intersection_loosest']}; "
          f"max floor the forest allows (field median) {row['floor_at_sig0_NF_field_median_kms']:.3f} km/s")
    FF["class"] = "PASS" if any_pass else ("EXCLUDED" if not any_loose else "UNDECIDED")
    Q2["footings"][f] = FF
    P(f"  [{f}] Q2 {FF['class']}")
RES["Q2"] = Q2
save()

# ================================================================== Q3 scale link
P("\n== Q3 scale link")
zs_ = o_l["z_rec"]
Hs = float(np.exp(lnH(-math.log(1 + zs_)))) * _c / 3.085677581e22     # 1/s
rcom = o_l["rs_rec"] * 3.085677581e22
rphys = rcom / (1 + zs_)
Rb = 0.75 * float(np.interp(zs_, z_l[::-1], o_lb[:, cols["(.)rho_b"]][::-1])) / float(np.interp(zs_, z_l[::-1], rg_l[::-1]))
cs = _c / math.sqrt(3 * (1 + Rb))
kB, mp, me = 1.380649e-23, 1.67262192e-27, 9.1093837e-31
Ts = TCMB * (1 + zs_)
vp, ve = math.sqrt(kB * Ts / mp), math.sqrt(kB * Ts / me)
V = {"c": _c, "c_s*": cs, "v_p": vp, "v_e": ve}
Rr = {"r_s,com": rcom, "r_s,phys": rphys}
PC, MPC = 3.085677581e16, 3.085677581e22
Q3 = {"base": {"z_*": zs_, "H_*_per_s": Hs, "r_s_com_Mpc": rcom / MPC, "r_s_phys_kpc": rphys / PC / 1e3, "R_*": Rb,
               "c_s_kms": cs / 1e3, "v_p_kms": vp / 1e3, "v_e_kms": ve / 1e3, "T_*_K": Ts}, "footings": {}}
for f in FOOT:
    a0 = FOOT[f]
    acc = {f"{vn}*H_*": vv * Hs for vn, vv in V.items()}
    acc.update({f"{rn}*H_*^2": rv * Hs ** 2 for rn, rv in Rr.items()})
    acc.update({f"{vn}^2/{rn}": vv ** 2 / rv for vn, vv in V.items() for rn, rv in Rr.items()})
    spd = {"a0/H_*": a0 / Hs, "sqrt(a0 r_s,com)": math.sqrt(a0 * rcom), "sqrt(a0 r_s,phys)": math.sqrt(a0 * rphys)}
    spd.update({vn: vv for vn, vv in V.items() if vn != "c"})
    spd.update({f"{rn}*H_*": rv * Hs for rn, rv in Rr.items()})
    lng = {"a0/H_*^2": a0 / Hs ** 2}
    lng.update({f"{vn}^2/a0": vv ** 2 / a0 for vn, vv in V.items()})
    lng.update(Rr)
    lng.update({f"{vn}/H_*": vv / Hs for vn, vv in V.items()})
    targets = {"acc": {"a0": a0}, "spd": {"c0": C0[f]["c0"] * 1e3},
               "len": {"L*": (21.7 if f == "canonical" else 22.9) * PC, "lambda_forest(com)": LAM_NF / h_l * MPC}}
    rows, N = [], 0
    for dim, cand in (("acc", acc), ("spd", spd), ("len", lng)):
        logs = [math.log10(v) for v in cand.values()]
        span = max(logs) - min(logs)
        for cn, cv in cand.items():
            for tn, tv in targets[dim].items():
                variants = [("as is", cv)]
                if tn == "lambda_forest(com)" and ("phys" in cn or cn in ("a0/H_*^2",) or "/H_*" in cn or "/a0" in cn):
                    variants.append(("x(1+z_*)", cv * (1 + zs_)))
                for vn_, vv_ in variants:
                    N += 1
                    d = math.log10(vv_ / tv)
                    rows.append({"dim": dim, "candidate": cn, "variant": vn_, "target": tn, "log10_ratio": d,
                                 "match": abs(d) <= 0.1, "uses_a0": "a0" in cn, "p_chance": min(1.0, 0.2 / span) if span > 0 else 1.0})
    nm = [r_ for r_ in rows if r_["match"]]
    expch = sum(r_["p_chance"] for r_ in rows)
    Q3["footings"][f] = {"N_trials": N, "matches": nm, "expected_chance_matches": expch, "rows": rows,
                         "class": "UNDECIDED (NUMEROLOGY ONLY)" if nm else "EXCLUDED (NO MATCH)"}
    P(f"  [{f}] trials {N}; matches {len(nm)}; expected by chance {expch:.2f}")
    for r_ in nm:
        P(f"     MATCH (numerology, not derived): {r_['candidate']} [{r_['variant']}] vs {r_['target']}: "
          f"log10 ratio {r_['log10_ratio']:+.3f}{' (uses a0)' if r_['uses_a0'] else ' (no a0)'}")
RES["Q3"] = Q3
P(f"  base: z_* {zs_:.2f}, H_* {Hs:.4e} /s, r_s {rcom / MPC:.3f} Mpc com ({rphys / PC / 1e3:.2f} kpc phys), R_* {Rb:.4f}, "
  f"c_s {cs / 1e3:.0f} km/s, v_p {vp / 1e3:.3f} km/s, v_e {ve / 1e3:.1f} km/s, T_* {Ts:.1f} K")

# ================================================================== overall
q1 = Q1S["R1"]["class"]
q2 = {f: Q2["footings"][f]["class"] for f in FOOT}
if q1 == "EXCLUDED":
    za, zb = Q1S["R1"]["z_on_allowed"], Q1S["R2"]["z_on_allowed"]
    overall = ("RRB REDUCES TO ORDINARY CDM" if (za and zb and za >= zeq and zb >= zeq) else "RRB EXCLUDED BY TIMING")
elif q1 == "PASS" and all(v == "EXCLUDED" for v in q2.values()):
    overall = "RRB EXCLUDED BY RELIC SPEED"
elif q1 == "PASS" and all(v == "PASS" for v in q2.values()):
    overall = "RRB VIABLE"
else:
    overall = "UNDECIDED"
RES["verdict"] = {"overall": overall, "Q1_R1": q1, "Q1_R2": Q1S["R2"]["class"], "Q2": q2,
                  "Q3": {f: Q3["footings"][f]["class"] for f in FOOT}, "z_eq": zeq}
P(f"\nVERDICT: {overall}; Q1 R1 {q1}, R2 {Q1S['R2']['class']}; Q2 {q2}; Q3 {RES['verdict']['Q3']}")
good = all(ok == mu for n, ok, mu in CHK)
save()
P(f"X34 COMPLETE: {sum(ok == mu for n, ok, mu in CHK)}/{len(CHK)} checks have their required outcome; CLASS runs {NRUN[0]}; "
  f"failed runs {len(FAILMSG)}; elapsed {time.time() - T0:.0f} s")
sys.exit(0 if good else 1)
