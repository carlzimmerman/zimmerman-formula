#!/usr/bin/env python3
"""X18_beta_growth_forest: does nonlinear saturation (the perturbations' own x = |grad Xi|/a0 switching on
c_A^2 = B c^2 (M_theta - 1)) rescue C1's small-scale growth overshoot, or does the record's Lyman-alpha forest gate
close C1's window?  Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (committed alone, 71e86472ea).

Part S0  reproductions (stop rule)                     -> S0-1 .. S0-4
Part Q   the saturation model from the action           -> Q-KER, Q-DISP, Q-ASY, Q-LIM
Part C   graded cells (both footings, both mu_K)        -> forest gate per cell; Q-CONV
Part V   verdict (per footing, never pooled)

Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x18_beta_growth_forest.py               (exit 0 iff all pass)
      PYTHONHASHSEED=0 X18_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x18_beta_growth_forest.py  (m1..m8; exit 1)

kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle.
beta is never fitted: any beta-dependent pass is a window inside X14's window. Not theory closed.
"""
import os
import sys

if os.environ.get("PYTHONHASHSEED") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED="0"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import hashlib
import json
import math
import re
import resource
import shutil
import subprocess
import tempfile
import time

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

MUTATE = os.environ.get("X18_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"x18_beta_growth_forest{TAG}.out")
JS = os.path.join(HERE, f"x18_beta_growth_forest_results{TAG}.json")
T0 = time.time()
_lines = []
CHECKS = []
RES = {"mutate": MUTATE, "checks": CHECKS, "criteria_commit": "71e86472ea"}


def log(s=""):
    print(s, flush=True)
    _lines.append(s)


def check(cid, ok, value, line, required=True):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": str(value), "line": line, "required": required})
    log(f"  [{'PASS' if ok else 'FAIL'}] {cid}: {value}   (line: {line})")
    return ok


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r * 1024 / 1e9


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return v if math.isfinite(v) else str(v)
    if isinstance(o, (np.integer, int)):
        return int(o)
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, sp.Basic):
        return str(o)
    return o


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def finish(exit_code=None):
    RES["runtime_s"] = time.time() - T0
    RES["peak_rss_gb_self"] = rss_gb()
    RES["peak_rss_gb_children"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9
    req_fail = [c["id"] for c in CHECKS if c["required"] and not c["pass"]]
    RES["required_failures"] = req_fail
    log(f"checks {sum(c['pass'] for c in CHECKS)}/{len(CHECKS)} pass; required failures {req_fail}; "
        f"{RES['runtime_s']:.0f} s; peak RSS self {RES['peak_rss_gb_self']:.3f} GB, children "
        f"{RES['peak_rss_gb_children']:.3f} GB")
    with open(OUT, "w") as fh:
        fh.write("\n".join(_lines) + "\n")
    with open(JS, "w") as fh:
        json.dump(clean(RES), fh, indent=1)
    sys.exit((0 if not req_fail else 1) if exit_code is None else exit_code)


# ------------------------------------------------------------------------------------------- constants (RAW / FITTED)
G = 6.67430e-11
C_SI = 299792458.0
C_KMS = C_SI / 1e3
GM_SUN = 1.32712440018e20
KPC = 3.0856775814913673e19
MPC = 1e3 * KPC
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # FITTED (kappa = 1/2), never pooled
MUK = {"mu_0.1": 0.1 / MPC, "mu_0.03": 0.03 / MPC}             # S4 edges [1/m], physical
P = {k_: os.path.join(ROOT, *v_) for k_, v_ in {
    "x17_py": ("rebuild_2026_10_22", "X17_beta_sound_selector", "x17_beta_sound_selector.py"),
    "x17_json": ("rebuild_2026_10_22", "X17_beta_sound_selector", "x17_beta_sound_selector_results.json"),
    "x4_json": ("rebuild_2026_10_22", "X4_growth_native_cap", "x4_growth_results.json"),
    "x4_dbi_json": ("rebuild_2026_10_22", "X4_growth_native_cap", "x4_dbi_door_results.json"),
    "l346_json": ("real_research", "g03_audit_2026", "L346_switch_forest_gate_results.json"),
    "l319_py": ("real_research", "dark_sector_2026", "L319_lambda_triggered_kicked_decay.py"),
    "f3_json": ("rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json"),
}.items()}
SHA_FROZEN = {"x17_py": "532597c97959434be23955eb77dc3088f996ceaa26fab3833eeb3fa63d13f9f1",
              "x17_json": "4096947f34aac35eb9c4f5c396c856d7ead5ff133a58dc80801062926de4f442",
              "x4_json": "1e3cad6521263aa40bb6c013c733795be81575a49cf4226179c150cf36fd5499",
              "x4_dbi_json": "a6d8ededbcd7f20a928bbbf86f91746a78a38cda066ad34e6c963b9846138d9a",
              "l346_json": "e0be3821894cd776637da7a65596ba4c2230da487ade8eb47d703fa0efa352e4",
              "l319_py": "c14c359eb519b5a1495298c9da68773effc54e047c60ace7c3059947d9eea703",
              "f3_json": "5e0df3b412ddcfebbe6b3eedcaad277dbae74a405c6b56c114539a7084fdf84c"}
SHA_NOW = {k_: sha256(v_) for k_, v_ in P.items()}
RES["input_sha256"] = {k_: {"sha256": SHA_NOW[k_], "matches_frozen": SHA_NOW[k_] == SHA_FROZEN[k_]} for k_ in P}
log("X18_beta_growth_forest" + ("  [MUTATE m1-m8]" if MUTATE else ""))
log("=" * 110)
log("input sha256 vs frozen: " + ", ".join(f"{k_} {'ok' if SHA_NOW[k_] == SHA_FROZEN[k_] else 'CHANGED'}" for k_ in P))
X17 = json.load(open(P["x17_json"]))
X4 = json.load(open(P["x4_json"]))
X4D = json.load(open(P["x4_dbi_json"]))
F3R = json.load(open(P["f3_json"]))


def Bdim(b):
    return b / (2 + 3 * b)


def cmp_json(a, b, path="", skip=("runtime_s", "peak_rss_gb_self", "peak_rss_gb_children", "seconds")):
    """leaf-by-leaf comparison; timing strings '<number> s)' normalised (FROZEN_CRITERIA S0-1)."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        ka, kb = set(a) - set(skip), set(b) - set(skip)
        if ka != kb:
            out.append((path, f"keys differ {sorted(ka ^ kb)[:5]}"))
        for kk in sorted(ka & kb):
            out += cmp_json(a[kk], b[kk], f"{path}/{kk}", skip)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, "length"))
        else:
            for i_, (u, v) in enumerate(zip(a, b)):
                out += cmp_json(u, v, f"{path}[{i_}]", skip)
    elif isinstance(a, bool) or isinstance(b, bool):
        if a != b:
            out.append((path, f"{a} != {b}"))
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if not (a == b or (math.isnan(a) and math.isnan(b)) or
                (math.isfinite(a) and math.isfinite(b) and abs(a - b) <= 1e-12 * max(abs(a), abs(b)))):
            out.append((path, f"{a} != {b}"))
    elif isinstance(a, str) and isinstance(b, str):
        na, nb = (re.sub(r"[0-9.]+ s\)", "T s)", s_) for s_ in (a, b))
        if na != nb:
            out.append((path, f"{a[:60]} != {b[:60]}"))
    elif a != b:
        out.append((path, f"{str(a)[:60]} != {str(b)[:60]}"))
    return out


def count_leaves(o):
    if isinstance(o, dict):
        return sum(count_leaves(v) for v in o.values())
    if isinstance(o, list):
        return sum(count_leaves(v) for v in o)
    return 1


# ===================================================================================================== PART S0
log("")
log("PART S0: reproductions (stop rule)")
# ---- S0-1: X17's own script as a patched copy in a temporary directory
src = open(P["x17_py"]).read()
old_here = 'HERE = os.path.dirname(os.path.abspath(__file__))'
old_root = 'ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))'
# A1 (PRE-RESULT): X17's own source also contains these two lines as strings (for patching X15), so only the first,
# line-start occurrence (the module assignment) is rebound.
patch_ok = ("\n" + old_here + "\n") in src and ("\n" + old_root + "\n") in src and src.index(old_here) < src.index("def log(")
tmpd = tempfile.mkdtemp(prefix="x18_x17copy_")
s01 = {"patch_ok": patch_ok}
try:
    patched = src.replace("\n" + old_here + "\n", f"\nHERE = {tmpd!r}\n", 1).replace("\n" + old_root + "\n", f"\nROOT = {ROOT!r}\n", 1)
    cp = os.path.join(tmpd, "x17_copy.py")
    with open(cp, "w") as fh:
        fh.write(patched)
    env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
    env.pop("X17_MUTATE", None)
    if MUTATE:
        env["X17_MUTATE"] = "1"                              # m1
    t1 = time.time()
    pr = subprocess.run([sys.executable, cp], capture_output=True, text=True, env=env, cwd=tmpd, timeout=1800)
    s01["returncode"] = pr.returncode
    s01["seconds"] = time.time() - t1
    s01["stderr_tail"] = pr.stderr[-600:]
    jn = os.path.join(tmpd, f"x17_beta_sound_selector_results{'_MUTATE' if MUTATE else ''}.json")
    with open(jn) as fh:
        x17_copy = json.load(fh)
finally:
    shutil.rmtree(tmpd, ignore_errors=True)
diffs = cmp_json(x17_copy, X17)
n_pass17 = sum(1 for c in x17_copy["checks"] if c["pass"])
s01.update({"n_pass": n_pass17, "n_checks": len(x17_copy["checks"]), "n_leaves": count_leaves(X17),
            "n_diffs": len(diffs), "first_diffs": diffs[:5], "verdict_copy": x17_copy.get("verdict")})
RES["S0_1"] = s01
check("S0-1", SHA_NOW["x17_py"] == SHA_FROZEN["x17_py"] and SHA_NOW["x17_json"] == SHA_FROZEN["x17_json"] and patch_ok
      and s01["returncode"] == 0 and n_pass17 == 13 and len(x17_copy["checks"]) == 13 and not diffs
      and s01["verdict_copy"] == "WRONG SIGN",
      f"X17 copy exit {s01['returncode']}, {n_pass17}/{len(x17_copy['checks'])} PASS, verdict '{s01['verdict_copy']}', "
      f"{len(diffs)} differing leaves of {s01['n_leaves']} vs the committed JSON"
      + (f"; first {diffs[:2]}" if diffs else ""),
      "X17's own script (patched temp-dir copy) reproduces its committed JSON (timing fields excepted)")

# ---- copied record code: X17 L447-491 (make_E, growth_ratio_x4), background A, sig8, khr_drive, growth_C1 (L896-934)
BETAS = {foot: {bl: X17["S0_2"]["beta"][foot][bl] for bl in ("beta_min", "beta_max_0.1", "beta_max_0.03")}
         for foot in FOOT}


def make_E(Om, h, rad=True):
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL)), Or


def growth_ratio_x4(kk, mu_h, Om, Ob, h, kernel="bsk2", a_i=1e-3, rad=True, mut_s1=False):
    """F3's two-fluid sub-horizon growth, verbatim from x4_growth.py via X17 (m3: kernel s = 1)."""
    Ek, Or = make_E(Om, h, rad); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)
    def s_of(a, mu):
        if mu is None: return np.ones(n)
        if mut_s1: return np.ones(n)
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


from classy import Class

pa = F3R["K2"]["A_c2b_refit"]["params"]
hA = pa["h"]
cA_ = Class()
cA_.set({"omega_b": pa["omega_b"], "omega_cdm": pa["omega_cdm"], "h": hA, "ln10^{10}A_s": pa["lnAs"], "n_s": pa["n_s"],
         "tau_reio": pa["tau"], "N_ur": 3.044, "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0})
cA_.compute()
KS = np.geomspace(1e-4, 50.0, 1500)
PkA = np.array([cA_.pk_lin(k_ * hA, 0.0) for k_ in KS]) * hA ** 3
cA_.struct_cleanup()
OmA, ObA = (pa["omega_b"] + pa["omega_cdm"]) / hA ** 2, pa["omega_b"] / hA ** 2
OKA = OmA - ObA
W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_trapz = getattr(np, "trapezoid", None) or np.trapz


def sig8(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(_trapz(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))


KT = np.geomspace(1e-3, 3.0, 36)


def sig8_from_T(T):
    Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8(PkA, Tf) / sig8(PkA)


MU_H = {"mu_0.1": 0.1 / hA, "mu_0.03": 0.03 / hA}


def khr_drive(a, kk, beta, mut=False, Bmult=1.0):
    """X17's C1 transport factor F = 1 + B k_p^2/(K rho_tau) = 1 + f1 a and dlnF/dlna (mut: F -> 1/F, m2)."""
    f1 = Bmult * Bdim(beta) * (C_KMS * np.asarray(kk, float) / 100.0) ** 2 / (1.5 * OKA)
    F = 1.0 + f1 * a
    dlnF = f1 * a / F
    if mut:
        return 1.0 / F, -dlnF
    return F, dlnF


def growth_C1(kk, mu_h, beta, a_i=1e-3, a_out=(0.25, 1.0), mut=False):
    """X17 L906-934 verbatim (X17's F3/X4 ODE with C1)."""
    Ek, _ = make_E(OmA, hA, True)
    kk = np.asarray(kk, float)
    n = len(kk)
    Ob, OK = ObA, OKA

    def s_of(a):
        if mu_h is None:
            return np.ones(n)
        x2 = (kk / (a * mu_h)) ** 2
        return 1.0 / (1.0 + x2)

    def rhs(x, st):
        a = math.exp(x); E = Ek(a); eps = 1e-6
        dlnE = (math.log(Ek(a * math.exp(eps))) - math.log(Ek(a * math.exp(-eps)))) / (2 * eps)
        dens = 1.5 * a ** -3 / E ** 2
        db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
        if beta == 0:
            F, dlnF = 1.0, 0.0
        else:
            F, dlnF = khr_drive(a, kk, beta, mut=mut)
        src_b = dens * (Ob * db + OK * dk); src_k = F * dens * (Ob * db + OK * dk * s_of(a))
        return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE - dlnF) * gk + src_k])
    st0 = np.concatenate([np.full(n, a_i)] * 4)
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12,
                    t_eval=[math.log(a_) for a_ in a_out])
    return {a_: (Ob * sol.y[:n, j] + OK * sol.y[2 * n:3 * n, j]) / OmA for j, a_ in enumerate(a_out)}


# ---- S0-2: X17's growth cells from the verbatim copy (a_i = 1e-3)
K_REP = np.array([0.1, 0.3, 1.0, 3.0, 10.0])
s02, rel02 = {}, []
ai = 1e-3
dust_T = growth_C1(KT, None, 0.0, ai, a_out=(1.0,))[1.0]
dust_rep = growth_C1(K_REP, None, 0.0, ai)
for foot in FOOT:
    for lab in MU_H:
        R0 = sig8_from_T(growth_C1(KT, MU_H[lab], 0.0, ai, a_out=(1.0,))[1.0] / dust_T)
        rep0 = growth_C1(K_REP, MU_H[lab], 0.0, ai)
        for bl in ("beta_min", "beta_max_0.1" if lab == "mu_0.1" else "beta_max_0.03"):
            bv = BETAS[foot][bl]
            gT = growth_C1(KT, MU_H[lab], bv, ai, a_out=(1.0,), mut=MUTATE)[1.0]
            Rb = sig8_from_T(gT / dust_T)
            rep = growth_C1(K_REP, MU_H[lab], bv, ai, mut=MUTATE)
            rec = X17["growth"][foot][lab][f"{bl}|ai0.001"]
            mine = {"R_beta": Rb, "R_0": R0,
                    "T2": {zl: ((rep[a_] / dust_rep[a_]) ** 2).tolist() for zl, a_ in (("z0", 1.0), ("z3", 0.25))},
                    "T2_beta0": {zl: ((rep0[a_] / dust_rep[a_]) ** 2).tolist() for zl, a_ in (("z0", 1.0), ("z3", 0.25))}}
            r_ = [abs(mine["R_beta"] / rec["R_beta"] - 1)]
            r_ += [abs(u / v - 1) for zl in ("z0", "z3") for u, v in zip(mine["T2"][zl], rec["T2"][zl])]
            r3 = [abs(mine["R_0"] / rec["R_0"] - 1)]
            r3 += [abs(u / v - 1) for zl in ("z0", "z3") for u, v in zip(mine["T2_beta0"][zl], rec["T2_beta0"][zl])]
            s02[f"{foot}|{lab}|{bl}"] = {"max_rel_beta_cells": max(r_), "max_rel_beta0_cells": max(r3),
                                        "R_beta": Rb, "T2_z3": mine["T2"]["z3"], "T2_z0": mine["T2"]["z0"]}
            rel02.append(max(r_))
RES["S0_2"] = s02
check("S0-2", max(rel02) <= 1e-6, f"8 X17 growth cells (R_beta; T^2 z0/z3 at k {K_REP.tolist()}): max rel diff "
      f"{max(rel02):.1e}; e.g. canonical mu 0.1 beta_min R {s02['canonical|mu_0.1|beta_min']['R_beta']:.5f}, T^2(k3, z3) "
      f"{s02['canonical|mu_0.1|beta_min']['T2_z3'][3]:.4g}", "verbatim copy of X17's C1 ODE reproduces X17's growth table "
      "(<= 1e-6)")

# ---- S0-3: X4's beta = 0 row (X4 ODE copy vs X4 JSON) and X17's T2_beta0 cells
s03 = {}
for lab, X4lab in (("mu_0.03", "0.03"), ("mu_0.1", "0.1")):
    for col, ai_ in (("bsk2_ai0.001", 1e-3), ("bsk2_ai0.0001", 1e-4)):
        Tx = growth_ratio_x4(KT, MU_H[lab], OmA, ObA, hA, "bsk2", ai_, mut_s1=MUTATE)
        s03[f"{lab}|{col}"] = {"this": sig8_from_T(Tx), "X4": X4["ode"][X4lab][col]["sigma8_ratio"]}
b0rel = max(v["max_rel_beta0_cells"] for v in s02.values())
RES["S0_3"] = {"x4_rows": s03, "x17_T2_beta0_max_rel": b0rel}
check("S0-3", all(abs(v["this"] / v["X4"] - 1) <= 1e-4 for v in s03.values()) and b0rel <= 1e-6,
      "; ".join(f"{k_} {v['this']:.6f} vs X4 {v['X4']:.6f}" for k_, v in s03.items()) + f"; X17 T2_beta0 max rel {b0rel:.1e}",
      "X4's beta = 0 sigma8 ratios (<= 1e-4) and X17's beta = 0 cells (<= 1e-6) reproduced")

# ---- S0-4: forest gate numbers (L346 JSON; L319 line), against X4's F0a / F0b
L346 = json.load(open(P["l346_json"]))
runs346 = L346["numbers"]["runs"]


def r346(name, z):
    a = np.array(runs346[name]["pk"][z])
    b = np.array(runs346["lcdm"]["pk"][z])
    kk = b[:, 0]
    fo = (kk >= 1.0) & (kk <= 4.0)
    return kk[fo], (a[:, 1] / b[:, 1])[fo]


KB346 = r346("sw5_canon", "3.0")[0]
f0a = {}
for nme in ("sw5_canon", "sw5_alt", "never_on"):
    for z in ("3.0", "2.0"):
        _, rr = r346(nme, z)
        f0a[f"{nme}_{z}"] = (float(rr.min()), float(rr.max()))
pass_sw5 = all(0.8 <= f0a[f"{n_}_{z}"][0] and f0a[f"{n_}_{z}"][1] <= 1.2 for n_ in ("sw5_canon", "sw5_alt") for z in ("3.0", "2.0"))
st346 = L346["numbers"]["F2"]
ok_a = (all(abs(f0a[f"{n_}_{z}"][i] - st346[f"{n_}_{z}"][i]) <= 1e-9 and abs(f0a[f"{n_}_{z}"][i] - X4D["F0a"]["bands"][f"{n_}_{z}"][i]) <= 1e-9
            for n_ in ("sw5_canon", "sw5_alt") for z in ("3.0", "2.0") for i in (0, 1))
        and (not pass_sw5) and all(f0a[f"never_on_{z}"] == (1.0, 1.0) for z in ("3.0", "2.0"))
        and np.max(np.abs(KB346 - np.array(X4D["F0a"]["bins_hMpc"]))) <= 1e-9)
h19 = 0.6736
Om19 = (0.02237 + 0.1200) / h19 ** 2
K_H19 = np.geomspace(0.02, 30.0, 44)
k5 = float(K_H19[int(np.argmin(np.abs(K_H19 - 5.0)))])


def T2_wdm(k_h, m_keV):                                  # L319 L169-171, verbatim formula
    alpha = 0.049 * m_keV ** -1.11 * (Om19 / 0.25) ** 0.11 * (h19 / 0.7) ** 1.22; nu = 1.12
    return (1 + (alpha * k_h) ** (2 * nu)) ** (-10 / nu)


T2_53 = float(T2_wdm(k5, 3.0 if MUTATE else 5.3))            # m4: 3 keV
ok_b = abs(T2_53 - X4D["F0b"]["T2_5.3keV"]) <= 1e-9 and abs(T2_53 - 0.995) <= 5e-4 and abs(k5 - X4D["F0b"]["k5_hMpc"]) <= 1e-12
RES["S0_4"] = {"L346_bins_hMpc": KB346.tolist(), "L346_bands": f0a, "sw5_gate_passes": pass_sw5, "k5_hMpc": k5,
               "T2_5.3keV": T2_53}
check("S0-4", ok_a and ok_b, f"L346 bins {np.round(KB346, 3).tolist()}; sw5_canon z3 {f0a['sw5_canon_3.0'][0]:.4f}-"
      f"{f0a['sw5_canon_3.0'][1]:.4f}, sw5_alt z3 {f0a['sw5_alt_3.0'][0]:.4f}-{f0a['sw5_alt_3.0'][1]:.4f} -> gate "
      f"{'PASS' if pass_sw5 else 'FAIL'} (L346, X4: FAIL); never_on {f0a['never_on_3.0']}; T^2_5.3keV(k5 = {k5:.4f}) = "
      f"{T2_53:.5f} (X4 F0b {X4D['F0b']['T2_5.3keV']:.5f})", "L346 bands/bins = L346 F2 = X4 F0a (1e-9); L319 line = "
      "X4 F0b (1e-9), within 5e-4 of 0.995")
S0_OK = all(c["pass"] for c in CHECKS if c["id"].startswith("S0-"))
RES["S0_all_pass"] = S0_OK
if not S0_OK and not MUTATE:
    log("STOP RULE: a step-0 reproduction failed; verdict UNDECIDED, nothing further is scored.")
    RES["verdict"] = "UNDECIDED (step 0 failed)"
    finish(1)

# ===================================================================================================== PART Q
log("")
log("PART Q: the saturation model from the action")
k, om = sp.symbols("k omega", positive=True)
r0 = sp.Symbol("rho0", real=True)
th = sp.Symbol("theta", real=True)
ML, MT = sp.symbols("M_L M_T", positive=True)
Kc, gL, muK = sp.symbols("K gamma_L mu_K", positive=True)
Bc = sp.Symbol("B", positive=True)
W2 = sp.Symbol("W2")
Mth = sp.Symbol("M_theta", positive=True)
Ms = sp.Symbol("M", positive=True)


def chi(theta_val, mu2=None):
    m2 = muK ** 2 if mu2 is None else mu2
    return k ** 2 / (Kc * Mth + theta_val * gL * k ** 2) + m2 / Kc


def disp_system(theta_val, cont_extra=0, muK2=None, source=None, baryons=None):
    """X14's disp (X3 B1-S) equations, as copied in X17 L350-372."""
    dphi, dsig, dXi, drho = sp.symbols("dphi dsigma dXi drho")
    dP = sp.symbols("dP0:3")
    kh = sp.Matrix([0, 0, 1])
    Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hm = Kc * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T)
    dPv = sp.Matrix(dP)
    mu2 = muK ** 2 if muK2 is None else muK2
    Peq = sp.I * k * kh * dXi - theta_val * gL * k ** 2 * kh * (kh.dot(dPv)) - Hm * dPv
    unknowns = [dphi, dsig, dXi, drho] + list(dP)
    pois_src = 0
    extra = []
    if source is not None:
        pois_src = source
    if baryons is not None:
        rb, drb, dvb = baryons
        pois_src = drb
        unknowns += [drb, dvb]
        extra = [-sp.I * om * drb + sp.I * rb * k * dvb, -sp.I * om * dvb + sp.I * k * dphi]
    eqs_ = [-k ** 2 * dphi - Kc * (drho + pois_src), drho - (sp.I * k * kh.dot(dPv) - mu2 * dXi / Kc),
            -sp.I * om * drho + (r0 + cont_extra) * k ** 2 * dsig, dXi - (dphi + sp.I * om * dsig)] + list(Peq) + extra
    return eqs_, unknowns


def disp(theta_val, cont_extra=0, muK2=None):
    eqs_, unk = disp_system(theta_val, cont_extra, muK2)
    Msys = sp.linear_eq_to_matrix(eqs_, unk)[0]
    det = sp.factor(sp.simplify(Msys.det()))
    sol_ = sp.solve(sp.Eq(det.subs(om, sp.sqrt(W2)), 0), W2)
    return sp.simplify(sol_[0]) if len(sol_) == 1 else None


def to_Mth(expr):
    e = sp.simplify(expr.subs(ML, 1 / ((1 / Mth - sp.sin(th) ** 2 / MT) / sp.cos(th) ** 2)))
    return sp.simplify(e)


def sM_sym(M, mut=False):
    sgn = 1 if mut else -1                                       # m5: wrong sign of the (M - 1) k^2 term
    return (M * muK ** 2 + sgn * (M - 1) * k ** 2) / (k ** 2 + M * muK ** 2)


# ---- Q-KER
t_q = time.time()
w2M = to_Mth(disp(0, cont_extra=Bc * k ** 2 / Kc))
qker = sp.simplify(w2M + (Kc * r0 + Bc * k ** 2) * sM_sym(Mth, mut=MUTATE))
f0 = sp.Symbol("f0")
rec_kernel = (muK ** 2 - f0 * k ** 2) / ((1 - f0) * k ** 2 + muK ** 2)
qker_rec = sp.simplify(rec_kernel.subs(f0, 1 - 1 / Mth) - sM_sym(Mth))
qker_jx = sp.simplify(sM_sym(Mth).subs(Mth, 1) - muK ** 2 / (k ** 2 + muK ** 2))
thr = sp.solve(sp.Eq(sp.numer(sp.together(sM_sym(1 + sp.Symbol("x", positive=True)))), 0), sp.Symbol("x", positive=True))
RES["Q_KER"] = {"omega2_general_M_theta": str(w2M), "residual": str(qker), "record_kernel_f0_1_minus_1_over_M": str(qker_rec),
                "M1_limit_minus_Jx": str(qker_jx), "onset_x_perp": str(thr)}
check("Q-KER", qker == 0 and qker_rec == 0 and qker_jx == 0,
      f"omega^2 + (K rho + B k^2) s_M = {qker}; s_M - s(k; f0 = 1 - 1/M) = {qker_rec}; s_M(M = 1) - J_x = {qker_jx}; "
      f"s_M = 0 at x = {thr} (perp) ({time.time() - t_q:.1f} s)",
      "X14's disp with C1 at general M_theta gives omega^2 = -(K rho + B k^2) s_M; s_M is the record's M1 kernel at "
      "f0 = 1 - 1/M and X4's J_x kernel at M = 1")

# ---- Q-DISP: coupled khronon + baryons at M_L = M_T = M
t_q = time.time()
rb, dvb_, drb_ = sp.symbols("rho_b dv_b drho_bdyn")
lam = sp.Symbol("lambda")
eqs_g, unk_g = disp_system(0, cont_extra=Bc * k ** 2 / Kc, baryons=(rb, drb_, dvb_))
Mg = sp.linear_eq_to_matrix([e.subs({ML: Ms, MT: Ms}) for e in eqs_g], unk_g)[0]
detg = sp.expand(Mg.det(method="berkowitz"))
poly_l = sp.expand(detg.subs(om, sp.sqrt(-lam)))
sMs = sM_sym(Ms)
Tsym = Kc * rb + (Kc * r0 + Bc * k ** 2) * sMs
Dsym = -Kc * rb * (Kc * r0 + Bc * k ** 2) * ((1 + sMs) if MUTATE else (1 - sMs))   # m6
target = sp.together(lam ** 2 - Tsym * lam + Dsym)
quo = sp.cancel(poly_l / sp.expand(sp.numer(target)))
qdisp_ok = quo.free_symbols.isdisjoint({lam, om}) and quo != 0
RES["Q_DISP"] = {"quotient": str(quo), "T": str(sp.simplify(Tsym)), "D": str(sp.simplify(Dsym))}
check("Q-DISP", qdisp_ok, f"det(baryons + khronon, M_L = M_T = M) / numer(lambda^2 - T lambda + D) = {quo} "
      f"({time.time() - t_q:.1f} s)", "coupled FRW system at general M: T = K rho_b + (K rho_tau + B k^2) s_M, "
      "D = -K rho_b (K rho_tau + B k^2)(1 - s_M); the saturated ODE is X17's growth_C1 with s -> s_M")

# ---- Q-ASY: k -> infinity limit of the growing root
t_q = time.time()
Tn_, Dn_ = (Kc * rb + (Kc * r0 + Bc * k ** 2) * sM_sym(Ms)), (-Kc * rb * (Kc * r0 + Bc * k ** 2) * (1 - sM_sym(Ms)))
eps = sp.Symbol("epsilon", positive=True)
lp = (Tn_ + sp.sqrt(Tn_ ** 2 - 4 * Dn_)) / 2
lim_DT = sp.limit(sp.simplify((Dn_ / Tn_).subs(k, 1 / eps)), eps, 0)
asy_target = Kc * rb * Ms if MUTATE else Kc * rb * Ms / (Ms - 1)                  # m7
num_pts = []
for (Mv, rbv, r0v, Bv, muv) in ((1.001, 0.05, 0.25, 1e-6, 0.01), (1.3, 0.05, 0.25, 3e-5, 0.03), (4.0, 1.0, 5.0, 1e-4, 1.0)):
    # A1 (PRE-RESULT, check code): exact rationals, so T + sqrt(T^2 - 4D) does not cancel in 15-digit floats
    sub = {Ms: sp.nsimplify(Mv), rb: sp.nsimplify(rbv), r0: sp.nsimplify(r0v), Bc: sp.nsimplify(Bv), Kc: 1,
           muK: sp.nsimplify(muv)}
    big = float(sp.N(lp.subs(sub).subs(k, sp.Integer(10) ** 9), 50))
    tgt = float(asy_target.subs(sub))
    num_pts.append(abs(big / tgt - 1))
qasy = sp.simplify(lim_DT - asy_target)
RES["Q_ASY"] = {"lim_D_over_T": str(lim_DT), "residual": str(qasy), "numeric_rel_at_k1e9": num_pts}
check("Q-ASY", qasy == 0 and max(num_pts) <= 1e-6,
      f"lim_(k->inf) D/T = {lim_DT}; minus K rho_b M/(M-1): {qasy}; lambda+ at k = 1e9 vs target max rel "
      f"{max(num_pts):.1e} ({time.time() - t_q:.1f} s)",
      "the saturated growing root tends to K rho_b M/(M - 1): no Jeans cut-off in the total; khronon Jeans k_J = "
      "mu sqrt(M/(M - 1))")

# ===================================================================================================== saturated ODE
H0_SI = 100e3 * hA / MPC
KG = np.unique(np.round(np.concatenate([KT, K_REP, KB346, [k5], np.geomspace(3.0, 50.0, 20)]), 12))
LNKG = np.log(KG)
DA_G = np.sqrt(np.exp(np.interp(LNKG, np.log(KS), np.log(PkA))) * KG ** 3 / (2 * math.pi ** 2))   # Delta_A(k), z = 0
D1 = {}


def dust_D1(a_i):
    if a_i not in D1:
        D1[a_i] = float(growth_C1(KT[:1], None, 0.0, a_i, a_out=(1.0,))[1.0][0])
    return D1[a_i]


IDX = {"rep": [int(np.argmin(np.abs(KG - v))) for v in K_REP], "bins": [int(np.argmin(np.abs(KG - v))) for v in KB346],
       "k5": int(np.argmin(np.abs(KG - k5))), "KT": [int(np.argmin(np.abs(KG - v))) for v in KT]}
assert all(abs(KG[i] / v - 1) < 1e-9 for i, v in zip(IDX["bins"], KB346)) and abs(KG[IDX["k5"]] / k5 - 1) < 1e-9


def y_of(a, dk, a0v, mu_lab, model, a_i):
    """Per-ln-k khronon acceleration from the linear Gauss law (incl. mu_K), Newtonian-from-charge part, / a0."""
    kp = KG * hA / MPC / a
    mu = MUK[mu_lab]
    Krho = 1.5 * OKA * H0_SI ** 2 * a ** -3
    yS = Krho * DA_G * np.abs(dk) / dust_D1(a_i) * kp / (kp ** 2 + mu ** 2) / a0v
    if model == "S":
        return yS
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (yS[1:] ** 2 + yS[:-1] ** 2) * np.diff(LNKG))])
    return np.maximum(yS, np.sqrt(cum))                         # A1: environment includes the mode itself


YCLIP = 0.99


def M_of(y, orient, yclip=None):
    yc = YCLIP if yclip is None else yclip
    x = np.minimum(y, yc) / (1.0 - np.minimum(y, yc))     # X14 cap inversion x = y/(1 - y)
    return (1.0 + x) if orient == "perp" else (1.0 + x) ** 2, x


def sM_num(a, mu_h, M):
    x2 = (KG / (a * mu_h)) ** 2
    return (M - (M - 1.0) * x2) / (x2 + M)


A_OUT = (0.25, 1.0 / 3.0, 1.0)


def growth_sat(beta, foot, mu_lab, model, orient, a_i=1e-3, rtol=1e-7, force_x0=False, Bmult=1.0, n_eval=240, yclip=None, method=None):
    Ek, _ = make_E(OmA, hA, True)
    n = len(KG)
    Ob, OK = ObA, OKA
    a0v = FOOT[foot]
    mu_h = MU_H[mu_lab]
    nfev = [0]

    def rhs(xx, st):
        nfev[0] += 1
        a = math.exp(xx); E = Ek(a); eps_ = 1e-6
        dlnE = (math.log(Ek(a * math.exp(eps_))) - math.log(Ek(a * math.exp(-eps_)))) / (2 * eps_)
        dens = 1.5 * a ** -3 / E ** 2
        db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
        if beta == 0:
            F, dlnF = 1.0, 0.0
        else:
            F, dlnF = khr_drive(a, KG, beta, Bmult=Bmult)
        if force_x0:
            M = np.ones(n)
        else:
            M, _ = M_of(y_of(a, dk, a0v, mu_lab, model, a_i), orient, yclip)
        s = sM_num(a, mu_h, M)
        src_b = dens * (Ob * db + OK * dk); src_k = F * dens * (Ob * db + OK * dk * s)
        return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE - dlnF) * gk + src_k])
    st0 = np.concatenate([np.full(n, a_i)] * 4)
    lte = np.unique(np.concatenate([np.linspace(math.log(a_i), 0.0, n_eval), [math.log(a_) for a_ in A_OUT]]))
    t1 = time.time()
    # A3 (implementation, after 9 of 24 graded canonical rows): the saturated E|par runs are stiff (DOP853 needed
    # 170-520 s per cell), so saturated runs use LSODA (auto stiff switching), same rtol/atol; the x = 0 path (Q-LIM)
    # stays DOP853, bit-comparable with X17. Q-CONV and the reported LSODA-vs-DOP853 diagnostic test the switch.
    meth = method or ("DOP853" if force_x0 else "LSODA")
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method=meth, rtol=rtol, atol=1e-12, t_eval=lte)
    out = {"ok": bool(sol.success), "nfev": nfev[0], "sec": time.time() - t1, "lna": sol.t,
           "db": sol.y[:n].T, "dk": sol.y[2 * n:3 * n].T}
    out["dm"] = (Ob * out["db"] + OK * out["dk"]) / OmA
    return out


def dust_track(a_i, lna):
    """dust delta(a) (k-independent) at the same evaluation points"""
    Ek, _ = make_E(OmA, hA, True)
    def rhs(xx, st):
        a = math.exp(xx); E = Ek(a); eps_ = 1e-6
        dlnE = (math.log(Ek(a * math.exp(eps_))) - math.log(Ek(a * math.exp(-eps_)))) / (2 * eps_)
        return [st[1], -(2 + dlnE) * st[1] + 1.5 * a ** -3 / E ** 2 * OmA * st[0]]
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], [a_i, a_i], method="DOP853", rtol=1e-10, atol=1e-14, t_eval=lna)
    return sol.y[0]


# ---- Q-LIM: x forced to 0 equals X17's growth_C1
t_q = time.time()
qlim = []
for lab, bl in (("mu_0.1", "beta_min"), ("mu_0.03", "beta_max_0.03")):
    bv = BETAS["canonical"][bl]
    ref = growth_C1(KG, MU_H[lab], bv, 1e-3, a_out=A_OUT)
    gs = growth_sat(bv, "canonical", lab, "S", "perp", force_x0=True, Bmult=2.0 if MUTATE else 1.0)    # m8
    for a_ in A_OUT:
        j = int(np.argmin(np.abs(gs["lna"] - math.log(a_))))
        qlim.append(float(np.max(np.abs(gs["dm"][j] / ref[a_] - 1))))
RES["Q_LIM"] = {"max_rel": max(qlim)}
check("Q-LIM", max(qlim) <= 1e-10,
      f"saturated ODE with x = 0 vs X17's growth_C1 (lane grid, z = 3/2/0): max rel {max(qlim):.1e} "
      f"({time.time() - t_q:.1f} s)", "the saturated ODE reduces to X17's ODE at x = 0 (<= 1e-10)")


# ===================================================================================================== PART C
def gate(T2z3, T2z2):
    out = {}
    for zl, T2 in (("3", T2z3), ("2", T2z2)):
        bins = [float(T2[i]) for i in IDX["bins"]]
        out[zl] = {"bins": bins, "min": min(bins), "max": max(bins), "T2_k5": float(T2[IDX["k5"]])}
    l346 = all(0.8 <= out[z]["min"] and out[z]["max"] <= 1.2 for z in ("3", "2"))
    l319s = all(out[z]["T2_k5"] >= T2_53 for z in ("3", "2"))
    l319l = all(out[z]["T2_k5"] >= 0.9 for z in ("3", "2"))
    far = any(out[z]["min"] < 0.5 or out[z]["max"] > 2.0 for z in ("3", "2"))
    F = "FAIL" if (not l319l or far) else ("PASS" if (l346 and l319s) else "UNDECIDED")
    return {"z": out, "F_L346": l346, "F_L319_strict": l319s, "F_L319_loose": l319l, "outside_0.5_2": far, "F": F}


def sig_class(R):
    return "below" if R < 0.95 else ("above" if R > 1.05 else "in")


def run_cell(beta, foot, mu_lab, model, orient, a_i=1e-3, rtol=1e-7, full=True, yclip=None, method=None):
    g = growth_sat(beta, foot, mu_lab, model, orient, a_i=a_i, rtol=rtol, yclip=yclip, method=method)
    dust = dust_track(a_i, g["lna"])
    a_arr = np.exp(g["lna"])
    jz = {zl: int(np.argmin(np.abs(g["lna"] - math.log(a_)))) for zl, a_ in (("z3", 0.25), ("z2", 1 / 3), ("z0", 1.0))}
    T2 = {zl: (g["dm"][j] / dust[j]) ** 2 for zl, j in jz.items()}
    Tb2 = {zl: (g["db"][j] / dust[j]) ** 2 for zl, j in jz.items()}
    R = sig8_from_T(np.abs(g["dm"][jz["z0"]][IDX["KT"]] / dust[jz["z0"]]))
    gt = gate(T2["z3"], T2["z2"])
    # y, x, s_M along the run
    a0v, mu_h = FOOT[foot], MU_H[mu_lab]
    ytr = np.array([y_of(a_, g["dk"][i], a0v, mu_lab, model, a_i) for i, a_ in enumerate(a_arr)])
    Mtr, xtr = M_of(ytr, orient, yclip)
    smtr = np.array([sM_num(a_, mu_h, Mtr[i]) for i, a_ in enumerate(a_arr)])
    s0tr = np.array([sM_num(a_, mu_h, np.ones(len(KG))) for a_ in a_arr])
    forest_k = KG <= 5.1
    cap = bool(np.any(ytr[a_arr <= 1 / 3 + 1e-12][:, forest_k] >= 1.0))
    # A2 (reported only): latest epoch at which a forest-scale mode is at or above the cap, and the forest-epoch y
    wcap = np.where(np.any(ytr[:, forest_k] >= 1.0, axis=1))[0]
    z_cap_last = float(1 / a_arr[wcap[-1]] - 1) if len(wcap) else None
    jz3 = int(np.argmin(np.abs(np.log(a_arr) - math.log(0.25))))
    y_forest_z3_max = float(np.max(ytr[jz3][forest_k]))
    # Delta_m at z = 3 in the bins (FORMAL flag)
    Dz3 = DA_G * np.abs(g["dm"][jz["z3"]]) / dust_D1(a_i)
    formal = bool(max(Dz3[i] for i in IDX["bins"]) > 1.0)
    res = {"beta": beta, "ok": g["ok"], "nfev": g["nfev"], "sec": g["sec"], "R_sigma8": R, "R_class": sig_class(R),
           "gate": gt, "F": "UNDECIDED" if cap else gt["F"], "F_raw": gt["F"], "CAP": cap, "FORMAL_z3": formal,
           "y_max_forest_to_z2": float(np.max(ytr[a_arr <= 1 / 3 + 1e-12][:, forest_k])),
           "z_cap_last_forest": z_cap_last, "y_forest_max_at_z3": y_forest_z3_max}
    if not full:
        return res
    onset, onset_proxy = {}, {}
    for kl, i in [(f"{K_REP[j]:g}", IDX["rep"][j]) for j in range(5)] + [(f"bin{j}", IDX["bins"][j]) for j in range(6)]:
        w = np.where(smtr[:, i] <= 0)[0]
        onset[kl] = float(1 / a_arr[w[0]] - 1) if len(w) else None
        w2 = np.where(xtr[:, i] >= s0tr[:, i])[0]
        onset_proxy[kl] = float(1 / a_arr[w2[0]] - 1) if len(w2) else None
    kJ = {}
    for zl, j in jz.items():
        w = np.where(smtr[j] <= 0)[0]
        kJ[zl] = float(KG[w[0]]) if len(w) else None
    rates = {}
    Ek, _ = make_E(OmA, hA, True)
    for zl, j in jz.items():
        a_ = a_arr[j]
        dens = 1.5 * a_ ** -3
        for kv in (1.0, 3.0, 10.0):
            i = int(np.argmin(np.abs(KG - kv)))
            Bk2 = Bdim(beta) * (C_KMS * kv / 100.0) ** 2 / a_ ** 2
            def rate(s):
                Tn = dens * ObA + (dens * OKA + Bk2) * s
                Dn = -dens * ObA * (dens * OKA + Bk2) * (1 - s)
                return math.sqrt((Tn + math.sqrt(Tn * Tn - 4 * Dn)) / 2) / Ek(a_)
            rates[f"{zl}|k{kv:g}"] = {"sat": rate(smtr[j, i]), "x0": rate(s0tr[j, i])}
    P1D = {}
    for zl in ("z3", "z2"):
        Pq = DA_G ** 2 / KG ** 3                                # ~ P_A up to 2 pi^2 (cancels in the ratio)
        rat = []
        for i in IDX["bins"]:
            sl = slice(i, None)
            num = _trapz(Pq[sl] * T2[zl][sl] * KG[sl] ** 2, LNKG[sl])
            den = _trapz(Pq[sl] * KG[sl] ** 2, LNKG[sl])
            rat.append(float(num / den))
        P1D[zl] = rat
    res.update({"T2_rep": {zl: [float(T2[zl][i]) for i in IDX["rep"]] for zl in T2},
                "Tb2_rep": {zl: [float(Tb2[zl][i]) for i in IDX["rep"]] for zl in Tb2},
                "Tb2_bins": {zl: [float(Tb2[zl][i]) for i in IDX["bins"]] for zl in ("z3", "z2")},
                "y_rep": {zl: [float(ytr[j, i]) for i in IDX["rep"]] for zl, j in jz.items()},
                "x_rep": {zl: [float(xtr[j, i]) for i in IDX["rep"]] for zl, j in jz.items()},
                "Delta_m_z3_bins": [float(Dz3[i]) for i in IDX["bins"]],
                "z_onset_sM_le_0": onset, "z_onset_x_ge_s": onset_proxy, "k_J_hMpc": kJ, "rate_over_H": rates,
                "P1D_ratio_bins": P1D})
    return res


log("")
log("PART C: graded cells (both footings never pooled; brackets S/E x perp/par)")
BR = [("S", "perp"), ("S", "par"), ("E", "perp"), ("E", "par")]
GRID = {}
for foot in FOOT:
    GRID[foot] = {"mu_0.1": np.geomspace(BETAS[foot]["beta_min"], BETAS[foot]["beta_max_0.1"], 5).tolist(),
                  "mu_0.03": np.geomspace(BETAS[foot]["beta_min"], BETAS[foot]["beta_max_0.03"], 7).tolist()}
if MUTATE:
    GRID = {"canonical": {"mu_0.1": [BETAS["canonical"]["beta_min"]]}}
    BR = [("S", "perp")]
RES["beta_grid"] = GRID
CELLS = {}
REF0 = {}
for foot in GRID:
    CELLS[foot] = {}
    REF0[foot] = {}
    for lab in GRID[foot]:
        CELLS[foot][lab] = []
        if not MUTATE:
            # A4: the beta = 0 reference (reported only) skips the stiff E|par bracket
            REF0[foot][lab] = {f"{m}|{o}": run_cell(0.0, foot, lab, m, o) for m, o in BR if (m, o) != ("E", "par")}
            r0_ = REF0[foot][lab]
            log(f"  {foot} {lab} beta = 0 (v3s ref): " + "; ".join(
                f"{b_} R {v['R_sigma8']:.4f} z3 bins {v['gate']['z']['3']['min']:.3g}-{v['gate']['z']['3']['max']:.3g} F {v['F']} (F_raw {v['F_raw']}, CAP {v['CAP']}, last cap z {v['z_cap_last_forest']})"
                for b_, v in r0_.items()))
        for ib, bv in enumerate(GRID[foot][lab]):
            row = {"beta": bv, "brackets": {}}
            for m, o in BR:
                # A4 (implementation, compute budget): E|par costs 100-500 s per cell. It is run at the grid ends; at
                # interior beta it is run only if no cheaper bracket is CAP/UNDECIDED. Otherwise that beta is already
                # "mixed" under section 6 whatever E|par gives, so skipping it cannot change the verdict.
                interior = 0 < ib < len(GRID[foot][lab]) - 1
                if (m, o) == ("E", "par") and interior and any(v["F"] == "UNDECIDED" for v in row["brackets"].values()):
                    row["brackets"]["E|par"] = {"F": "NOT RUN (A4)", "F_raw": "NOT RUN (A4)"}
                    continue
                c_ = run_cell(bv, foot, lab, m, o)
                row["brackets"][f"{m}|{o}"] = c_
            Fs = [v["F"] for v in row["brackets"].values()]
            row["robust"] = "FAIL" if all(f_ == "FAIL" for f_ in Fs) else ("PASS" if all(f_ == "PASS" for f_ in Fs) else "mixed")
            CELLS[foot][lab].append(row)
            log(f"  {foot} {lab} beta {bv:.3e}: " + "; ".join(
                f"{b_} R {v['R_sigma8']:.3g} z3 [{v['gate']['z']['3']['min']:.3g}, {v['gate']['z']['3']['max']:.3g}] "
                f"z2 [{v['gate']['z']['2']['min']:.3g}, {v['gate']['z']['2']['max']:.3g}] T2k5 "
                f"{v['gate']['z']['3']['T2_k5']:.3g}/{v['gate']['z']['2']['T2_k5']:.3g} F {v['F']}"
                f"{' CAP(last z ' + format(v['z_cap_last_forest'], '.2f') + ', F_raw ' + v['F_raw'] + ')' if v['CAP'] else ''}"
                f"{' FORMAL' if v['FORMAL_z3'] else ''} y_z3 {v['y_forest_max_at_z3']:.2g} ({v['sec']:.0f} s)"
                for b_, v in row["brackets"].items() if "gate" in v) + ("; E|par NOT RUN (A4)" if "gate" not in
                row["brackets"].get("E|par", {"gate": 1}) else "") + f" -> {row['robust']}")
RES["cells"] = CELLS
RES["beta0_reference"] = REF0

# ---- Q-CONV
t_q = time.time()
conv = []
for foot in GRID:
    for lab in GRID[foot]:
        for idx_b in sorted({0, len(GRID[foot][lab]) - 1}):
            row = CELLS[foot][lab][idx_b]
            for m, o in BR:
                base = row["brackets"][f"{m}|{o}"]
                variants = (("ai1e-4", {"a_i": 1e-4}), ("rtol1e-9", {"rtol": 1e-9}))
                if (m, o) == ("E", "par"):                     # A4: E|par only a_i 1e-4, only at beta_min
                    if idx_b != 0:
                        continue
                    variants = variants[:1]
                for tag, kw in variants:
                    alt_ = run_cell(row["beta"], foot, lab, m, o, full=False, **kw)
                    conv.append({"foot": foot, "mu": lab, "beta": row["beta"], "bracket": f"{m}|{o}", "variant": tag,
                                 "F": alt_["F"], "F_base": base["F"], "R_class": alt_["R_class"],
                                 "R_class_base": base["R_class"], "R": alt_["R_sigma8"], "R_base": base["R_sigma8"],
                                 "z3_max": alt_["gate"]["z"]["3"]["max"], "z3_max_base": base["gate"]["z"]["3"]["max"],
                                 "same": alt_["F"] == base["F"] and alt_["R_class"] == base["R_class"]})
RES["Q_CONV"] = conv
nbad = sum(1 for c_ in conv if not c_["same"])
check("Q-CONV", nbad == 0, f"{len(conv)} variant runs (a_i 1e-4, rtol 1e-9) on the (beta_min, beta_max) cells: {nbad} change F "
      f"or the sigma8 class ({time.time() - t_q:.0f} s)", "gate class and sigma8 class unchanged under a_i and rtol")

# ---- A2 (reported only, no verdict weight): sensitivity of F_raw to the cap clip (canonical; S perp and E par)
CLIPS = {}
if not MUTATE:
    for lab in GRID["canonical"]:
        for idx_b in sorted({0, len(GRID["canonical"][lab]) - 1}):
            bv = GRID["canonical"][lab][idx_b]
            for m, o in (("S", "perp"), ("E", "perp")):      # A4: E|par replaced by E|perp here
                for yc in (0.9, 0.995):
                    c_ = run_cell(bv, "canonical", lab, m, o, full=False, yclip=yc)
                    CLIPS[f"{lab}|{bv:.3e}|{m}|{o}|clip{yc}"] = {"F_raw": c_["F_raw"], "R": c_["R_sigma8"],
                                                                  "z3": [c_["gate"]["z"]["3"]["min"], c_["gate"]["z"]["3"]["max"]],
                                                                  "z2": [c_["gate"]["z"]["2"]["min"], c_["gate"]["z"]["2"]["max"]],
                                                                  "z_cap_last": c_["z_cap_last_forest"]}
    log("  A2 clip sensitivity (F_raw ignores CAP): " + "; ".join(f"{k_} F_raw {v['F_raw']} z3 [{v['z3'][0]:.3g}, {v['z3'][1]:.3g}]"
                                                                  for k_, v in CLIPS.items()))
RES["A2_clip_sensitivity"] = CLIPS
# ---- A3 diagnostic (reported only): LSODA vs DOP853 on the cheap brackets at beta_min, canonical
SOLV = {}
if not MUTATE:
    for lab in GRID["canonical"]:
        bv = GRID["canonical"][lab][0]
        for m, o in (("S", "perp"), ("S", "par"), ("E", "perp")):
            c_d = run_cell(bv, "canonical", lab, m, o, full=False, method="DOP853")
            c_l = CELLS["canonical"][lab][0]["brackets"][f"{m}|{o}"]
            rels = [abs(u / v - 1) for zl in ("3", "2") for u, v in zip(c_d["gate"]["z"][zl]["bins"], c_l["gate"]["z"][zl]["bins"])]
            SOLV[f"{lab}|{m}|{o}"] = {"F_raw_dop853": c_d["F_raw"], "F_raw_lsoda": c_l["F_raw"], "max_rel_bins": max(rels),
                                      "R_dop853": c_d["R_sigma8"], "R_lsoda": c_l["R_sigma8"]}
    log("  A3 LSODA vs DOP853 (beta_min, canonical): " + "; ".join(
        f"{k_} F {v['F_raw_lsoda']}/{v['F_raw_dop853']} max rel bins {v['max_rel_bins']:.1e}" for k_, v in SOLV.items()))
RES["A3_solver_diagnostic"] = SOLV

# ===================================================================================================== PART V
log("")
log("VERDICT")
req_ok = all(c["pass"] for c in CHECKS if c["required"])
foot_v = {}
for foot in GRID:
    labs = {}
    for lab in GRID[foot]:
        labs[lab] = [(row["beta"], row["robust"]) for row in CELLS[foot][lab]]
    allrows = [r_ for lab in labs for r_ in labs[lab]]
    n_fail = sum(1 for _, r_ in allrows if r_ == "FAIL")
    n_pass = sum(1 for _, r_ in allrows if r_ == "PASS")
    if not req_ok:
        v = "UNDECIDED (a required check failed)"
    elif n_fail == len(allrows):
        v = "C1 WINDOW CLOSED BY THE FOREST"
    elif n_pass > 0:
        v = "SATURATION RESCUES (forest passes for beta in " + "; ".join(
            f"{lab}: " + ", ".join(f"{b_:.3e}" for b_, r_ in labs[lab] if r_ == "PASS") for lab in labs) + ") [a window, not a fit]"
    elif n_fail > 0:
        v = "WINDOW NARROWED TO " + "; ".join(
            f"{lab}: " + (", ".join(f"{b_:.3e}" for b_, r_ in labs[lab] if r_ != "FAIL") or "none") for lab in labs)
    else:
        v = "UNDECIDED (no beta robust FAIL or robust PASS)"
    foot_v[foot] = {"verdict": v, "robust_by_beta": labs}
RES["verdict_per_footing"] = foot_v
if len(set(v["verdict"] for v in foot_v.values())) == 1:
    verdict = list(foot_v.values())[0]["verdict"] + " (both footings)" if len(foot_v) == 2 else list(foot_v.values())[0]["verdict"]
else:
    verdict = " | ".join(f"{f_}: {v['verdict']}" for f_, v in foot_v.items())
RES["verdict"] = verdict
# reported: sigma8 and forest jointly within lines
joint = []
for foot in GRID:
    for lab in GRID[foot]:
        for row in CELLS[foot][lab]:
            for b_, v in row["brackets"].items():
                if v.get("R_class") == "in" and v["F"] == "PASS":
                    joint.append({"foot": foot, "mu": lab, "beta": row["beta"], "bracket": b_})
RES["sigma8_and_forest_both_within_lines"] = joint
log(f"  {verdict}")
log(f"  sigma8 in [0.95, 1.05] AND forest PASS (reported only): {joint if joint else 'no cell'}")
if MUTATE:
    must_fail = {"S0-1": "m1", "S0-2": "m2", "S0-3": "m3", "S0-4": "m4", "Q-KER": "m5", "Q-DISP": "m6", "Q-ASY": "m7",
                 "Q-LIM": "m8"}
    failed = {c["id"] for c in CHECKS if not c["pass"]}
    RES["mutate_required_failures"] = {cid: (cid in failed) for cid in must_fail}
    RES["mutate_exact"] = failed == set(must_fail)
    log(f"  MUTATE: required failures {RES['mutate_required_failures']}; all failed checks {sorted(failed)}; exact "
        f"{RES['mutate_exact']} (the MUTATE verdict line is the control's output, not physics)")
finish()
