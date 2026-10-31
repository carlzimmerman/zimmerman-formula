#!/usr/bin/env python3
"""RF5_growth_native_yardstick: the cold sector's turn-on epoch against raw CMB bandpowers, BAO, SN, shear and forest,
on the framework's own background. Frozen: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (469657249b).

Modes (each preemptible: SIGTERM -> checkpoint -> exit 75; rerun resumes):
  rf5.py checks          K1-K6 machinery
  rf5.py chain           F-R1 fits z_on high to low (one driver + up to 3 CLASS children)
  rf5.py khronon         F-K fits, mu_K 0.03 and 0.1 per Mpc
  rf5.py channel CELL    shear + forest for one finished cell
  rf5.py k9              preemption test
  rf5.py grade           gates, verdicts, rf5_results.json, rf5.out (exit 0 on the result)
RF5_MUTATE=1: separate outputs, one cell; m1 plik sign, m2 shear sign, m3 K1 target; G-CMB, G-SHEAR, K1 must FAIL.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf5.py <mode>
Build (outside the repository): X34_BUILD=<external>/rf5_class_build python3 -I ../X34_recombination_release/x34_make_patch.py

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed.
"""
import hashlib
import json
import math
import os
import re
import resource
import shutil
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.interpolate import CubicSpline, InterpolatedUnivariateSpline, RectBivariateSpline
from scipy.io import FortranFile
from scipy.special import j0
from scipy.stats import chi2 as CHI2

MUT = os.environ.get("RF5_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
R1B = os.path.join(EXT, "rf5_class_build", "class_x34", "class")
KHR = os.path.join(EXT, "class_khronon_build_2026_10_23", "class_khronon", "class")
WORK = os.path.join(EXT, f"rf5_work{TAG}")
CELLS = os.path.join(HERE, f"cells{TAG}")
os.makedirs(WORK, exist_ok=True)
os.makedirs(CELLS, exist_ok=True)
ZONS = [1e6] if MUT else [1e6, 3e5, 1e5, 5e4, 3e4, 2e4, 1.2e4, 7000.0, 4000.0, 2500.0, 1500.0, 1100.0, 300.0, 30.0]
KCELLS = {} if MUT else {"K0.03": 0.03, "K0.1": 0.1}
C_KMS = 299792.458
TCMB = 2.7255
OMCDM = 1e-8
KH = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0}
FOOT_RECORD = {"canonical": 9.3603e-11, "alt": 1.1312e-10}             # comparison only (ledger A3), never graded
BAND = {1.0: (0.76, 1.03), 1.5: (0.71, 1.12), 2.33: (0.33, 1.21)}      # CFG689 curvature free (primary)
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
NAMES = ["omega_b", "omega_c", "100theta_s", "lnA", "n_s", "tau", "w0", "wa"]
STEP = np.array([1e-4, 1e-3, 2e-4, 0.01, 0.004, 0.004, 0.02, 0.08])
NP = len(STEP)
NCLASS = 3
STOP = {"flag": False}
CHILD = set()


def on_term(sig, frm):
    STOP["flag"] = True
    for c in list(CHILD):
        try:
            c.terminate()
        except OSError:
            pass


signal.signal(signal.SIGTERM, on_term)


class Preempted(Exception):
    pass


def cellname(z):
    return f"R1_{z:.0f}"


def jw(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=1, default=float)
    os.replace(tmp, path)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ likelihood blocks, read-only exec (C2, X54)
def load_cmb():
    src = open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb.py")).read()
    blk = src[src.index("# ---------------------------------------------------------------- likelihoods"):
              src.index("# ---------------------------------------------------------------- CLASS emulation")]
    ns = {"np": np, "math": math, "os": os, "EXT": EXT, "FortranFile": FortranFile,
          "InterpolatedUnivariateSpline": InterpolatedUnivariateSpline}
    exec(compile(blk, "c2b_native_cmb.py[likelihoods]", "exec"), ns)
    if MUT:
        ns["Xd"] = -ns["Xd"]                                           # m1
    return ns


def load_bao_sn():
    src = open(os.path.join(HERE, "..", "X54_cold_de_exchange", "x54_cold_de_exchange.py")).read()
    blk = src[src.index("# ------------------------------------------------------------------ BAO (DESI DR2"):
              src.index("# ------------------------------------------------------------------ CLASS runner")]
    blk = blk.replace('("DES5", "PP", "U3")', '("DES5",)')
    ns = {"np": np, "os": os, "EXT": EXT, "C_KMS": C_KMS, "P": lambda *a: None}
    exec(compile(blk, "x54[bao,sn]", "exec"), ns)
    return ns


C2R = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb_results.json")))["P5"]
TAU_HAT, SIG_TAU = C2R["tau_hat"], C2R["sig_tau"]
C7F = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")))["fits"]["LCDM"]
P_START = np.array([C7F["params"][k] for k in ("omega_b", "omega_dm(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau")] + [-1.0, 0.0])
A_START = C7F["A_planck"]


# ------------------------------------------------------------------ CLASS
def cparams(p, cell):
    wb, wc, th, lnA, ns_, tau, w0, wa = p
    q = {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns_, "tau_reio": tau, "Omega_Lambda": 0.0,
         "w0_fld": w0, "wa_fld": wa, "cs2_fld": 1.0, "use_ppf": "yes"}
    if cell["kind"] == "R1":
        q["omega_cdm"] = max(wc, 5e-4)
    else:
        q.update({"omega_cdm": OMCDM, "omega_aest": max(wc, 5e-4) - OMCDM, **KH, "aest_K_type": 4, "aest_K2": cell["mu"] ** 2})
    return q


def run(name, cell, p, pk=False, cmb=True, zon_off=False, vanilla=False, lcdm_params=None, keep=False):
    d = {"T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2, "thermodynamics_verbose": 1,
         "fourier_verbose": 1, "overwrite_root": "yes", "write_background": "yes"}
    d.update(lcdm_params if lcdm_params is not None else cparams(p, cell))
    if cmb:
        d.update({"output": "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": 2508, **HIGH, **START})
    if pk:
        d.update({"output": "mPk", "P_k_max_h/Mpc": 30.0, "k_per_decade_for_pk": 20, "z_max_pk": 5.0, "z_pk": ", ".join(f"{z:.2f}" for z in ZPK), **START})
    wd = os.path.join(WORK, cell["name"])
    os.makedirs(wd, exist_ok=True)
    root = os.path.join(wd, name + "_")
    d["root"] = root
    with open(root + ".ini", "w") as fh:
        for k, v in d.items():
            fh.write(f"{k} = {v}\n")
    env = dict(os.environ, OMP_NUM_THREADS="1")
    env.pop("X34_ZON", None)
    binary = VAN if vanilla else (KHR if cell["kind"] == "K" else R1B)
    if cell["kind"] == "R1" and not zon_off and not vanilla:
        env["X34_ZON"] = repr(float(cell["zon"]))
    if STOP["flag"]:
        raise Preempted()
    pr = subprocess.Popen(["nice", "-n", "15", binary, root + ".ini"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    CHILD.add(pr)
    log, _ = pr.communicate()
    CHILD.discard(pr)
    if STOP["flag"]:
        raise Preempted()
    pre = root + "_"
    if pr.returncode != 0:
        lines = log.strip().splitlines()
        cell.setdefault("class_fail", []).append((lines[-1][-200:] if lines else "?"))
        _clean(wd, name)
        return None
    out = {"log": log, "pre": pre}
    if cmb:
        cl = np.loadtxt(pre + "cl_lensed.dat")
        L = int(cl[-1, 0])
        f = (TCMB * 1e6) ** 2
        for key, col in (("tt", 1), ("ee", 2), ("te", 3), ("pp", 5)):
            arr = np.zeros(L + 1)
            arr[cl[:, 0].astype(int)] = cl[:, col] * (f if key != "pp" else 1.0)
            out[key] = arr
    bg = np.loadtxt(pre + "background.dat")
    hdr = [ln for ln in open(pre + "background.dat") if ln.startswith("#")][-1]
    cols = {re.sub(r"^\d+:", "", c.strip()): i for i, c in enumerate(re.split(r"\s{2,}", hdr.lstrip("#").strip()))}
    z = bg[:, cols["z"]][::-1]
    sel = z <= 1.2e4
    gk = {"z": "z", "H": "H [1/Mpc]", "DM": "comov. dist.", "rt": "(.)rho_tot"}
    for k, c in (("rc", "(.)rho_cdm"), ("rb", "(.)rho_b"), ("rd", "(.)rho_fld"), ("rg", "(.)rho_g"), ("rl", "(.)rho_lambda"), ("rur", "(.)rho_ur"), ("rae", "(.)rho_aest")):
        if c in cols:
            gk[k] = c
    out["bg"] = {k: bg[:, cols[c]][::-1][sel] for k, c in gk.items()}
    if keep:
        out["bg_all"] = (bg, cols)
    zb = out["bg"]["z"]
    m = zb <= 6.0
    out["DMf"] = CubicSpline(zb[m], out["bg"]["DM"][m])
    out["Hf"] = CubicSpline(zb[m], out["bg"]["H"][m] * C_KMS)
    mm = re.search(r"found 'h = ([0-9.eE+-]+)'", log)
    out["h"] = float(mm.group(1)) if mm else out["bg"]["H"][0] * C_KMS / 100
    mm = re.search(r"sigma8=([0-9.]+) for total matter", log)
    out["sigma8"] = float(mm.group(1)) if mm else np.nan
    mm = re.search(r"baryon drag stops at z = [0-9.eE+-]+\s+corresponding to conformal time = [0-9.eE+-]+ Mpc\s+"
                   r"with comoving sound horizon rs = ([0-9.eE+-]+) Mpc", log)
    out["rd"] = float(mm.group(1)) if mm else np.nan
    if pk:
        out["pk"] = {}
        for i, zz in enumerate(ZPK):
            fn = pre + f"z{i + 1}_pk.dat"
            out["pk"][round(float(zz), 2)] = np.loadtxt(fn)
    if not keep:
        _clean(wd, name)
    return out


def _clean(wd, name):
    for f in os.listdir(wd):
        if f.startswith(name + "_"):
            try:
                os.remove(os.path.join(wd, f))
            except OSError:
                pass


ZPK = np.round(np.concatenate((np.arange(0.0, 3.01, 0.1), [3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5])), 2)


# ------------------------------------------------------------------ fit
class Lik:
    def __init__(self):
        self.c = load_cmb()
        b = load_bao_sn()
        self.bao, self.sn_resid, self.sn = b["bao_resid"], b["sn_resid"], b["SN"]["DES5"]

    def binned(self, o):
        return self.c["binned"](o["tt"], o["te"], o["ee"])

    def resid(self, o, A, tau):
        Tb = self.binned(o)
        return np.concatenate((np.linalg.solve(self.c["Lc"], self.c["Xd"] - Tb / A ** 2), [(A - 1) / 0.0025, (tau - TAU_HAT) / SIG_TAU],
                               self.bao(o["DMf"], o["Hf"], o["rd"]), self.sn_resid(self.sn, o["DMf"])))

    def parts(self, o, A):
        Tb = self.binned(o)
        c = {"plik": self.c["chi2_plik"](Tb, A), "lowTT": self.c["chi2_lowTT"](o["tt"], A), "lowEE": self.c["chi2_lowEE"](o["ee"], A),
             "Aprior": ((A - 1) / 0.0025) ** 2, "bao": float(np.sum(self.bao(o["DMf"], o["Hf"], o["rd"]) ** 2)),
             "sn": float(np.sum(self.sn_resid(self.sn, o["DMf"]) ** 2)), "n_sn": int(self.sn["n"])}
        return c


def fit_cell(L, cell, pstart, Astart, maxit=10):
    """Gauss-Newton + Broyden as X54; 8 CLASS parameters + A; checkpoint after every Jacobian and every accepted step."""
    ck = os.path.join(WORK, cell["name"] + "_ck.npz")
    state = {"p": np.array(pstart, float), "A": float(Astart), "J": None, "it": 0, "hist": [], "fresh": True}
    if os.path.exists(ck):
        z = np.load(ck, allow_pickle=True)
        state.update(p=z["p"], A=float(z["A"]), J=z["J"] if z["J"].ndim == 2 else None, it=int(z["it"]), hist=list(z["hist"]), fresh=bool(z["fresh"]))

    def save():
        np.savez(ck, p=state["p"], A=state["A"], J=state["J"] if state["J"] is not None else np.zeros(1), it=state["it"],
                 hist=np.array(state["hist"], dtype=object), fresh=state["fresh"])

    p, A = state["p"], state["A"]
    o = run("s", cell, p)
    if o is None:
        return {"status": "CLASS_FAIL", "msg": cell.get("class_fail", ["?"])[-1]}
    r = L.resid(o, A, p[5])

    def fresh_J(p, A, o, r):
        def col(kx):
            pp = p.copy()
            pp[kx] += STEP[kx]
            oo = run(f"j{kx}", cell, pp)
            sgn = 1.0
            if oo is None:
                pp[kx] -= 2 * STEP[kx]
                sgn = -1.0
                oo = run(f"j{kx}", cell, pp)
                if oo is None:
                    return None
            return sgn * (L.resid(oo, A, pp[5]) - r) / STEP[kx]
        with ThreadPoolExecutor(NCLASS) as ex:
            cols = list(ex.map(col, range(NP)))
        if any(c is None for c in cols):
            return None
        J = np.zeros((len(r), NP + 1))
        for kx, c in enumerate(cols):
            J[:, kx] = c
        J[:613, NP] = np.linalg.solve(L.c["Lc"], 2 * L.binned(o) / A ** 3)
        J[613, NP] = 1 / 0.0025
        return J

    J = state["J"]
    fresh = state["fresh"]
    if J is None or J.shape[0] != len(r):
        fresh = True
        J = fresh_J(p, A, o, r)
        if J is None:
            return {"status": "CLASS_FAIL", "msg": cell.get("class_fail", ["?"])[-1]}
        state.update(J=J, fresh=True)
        save()
    converged = False
    o_cur = o
    for it in range(state["it"], maxit):
        cs = float(r @ r)
        d = -np.linalg.lstsq(J, r, rcond=None)[0]
        lam = 1.0
        while True:
            pn, An = p + lam * d[:NP], A + lam * d[NP]
            pn[1] = max(pn[1], 5e-4)
            on = run("l", cell, pn)
            rn = None if on is None else L.resid(on, An, pn[5])
            cn = np.inf if rn is None else float(rn @ rn)
            if cn <= cs or lam < 1 / 16:
                break
            lam /= 2
        if cn > cs:
            if not fresh:
                fresh = True
                J = fresh_J(p, A, o_cur, r)
                if J is None:
                    return {"status": "CLASS_FAIL", "msg": cell.get("class_fail", ["?"])[-1]}
                state.update(J=J, fresh=True, it=it + 1)
                save()
                continue
            state["hist"].append((it + 1, cs, 0.0, lam))
            converged = True
            break
        dx = np.concatenate((pn - p, [An - A]))
        J = J + np.outer(rn - r - J @ dx, dx) / (dx @ dx)
        p, A, r, o_cur = pn, An, rn, on
        fall = cs - cn
        state["hist"].append((it + 1, cn, fall, lam))
        state.update(p=p, A=A, J=J, it=it + 1, fresh=False)
        fresh = False
        save()
        if fall < 0.1:
            fresh = True
            J = fresh_J(p, A, o_cur, r)
            if J is None:
                return {"status": "CLASS_FAIL", "msg": cell.get("class_fail", ["?"])[-1]}
            d2 = -np.linalg.lstsq(J, r, rcond=None)[0]
            pred = float(np.sum((r + J @ d2) ** 2))
            state.update(J=J, fresh=True)
            save()
            if cs - pred < 0.1 or cn - pred < 0.1:
                converged = True
                break
    ofin = run("f", cell, p)
    if ofin is None:
        return {"status": "CLASS_FAIL", "msg": cell.get("class_fail", ["?"])[-1]}
    c = L.parts(ofin, A)
    bg = ofin["bg"]
    h = ofin["h"]
    H0 = float(ofin["Hf"](0.0))
    rd_f = CubicSpline(bg["z"], bg["rd"]) if "rd" in bg else None
    H2 = (H0 / C_KMS) ** 2
    wc_key = bg.get("rc", 0 * bg["z"]) + bg.get("rae", 0 * bg["z"])
    sx = {str(z): float(math.sqrt(max(float(rd_f(z)) / float(rd_f(0.0)), 0.0))) for z in (0.5, 1.0, 1.5, 2.33)} if rd_f is not None else {}
    Ode = float(bg["rd"][0]) / H2 if rd_f is not None else np.nan
    Oc = float(wc_key[0]) / H2
    Ob = float(bg["rb"][0]) / H2
    rec = {"cell": cell["name"], "kind": cell["kind"], "zon": cell.get("zon"), "mu": cell.get("mu"), "status": "OK", "params": dict(zip(NAMES, map(float, p))),
           "A": A, "chi2": c, "h": h, "Omega_m": Oc + Ob, "Omega_c": Oc, "Omega_b": Ob, "Omega_DE": Ode, "sigma8": ofin["sigma8"], "rd": ofin["rd"],
           "sqrtX": sx, "gn": [list(map(float, x)) for x in state["hist"]], "converged": bool(converged), "class_fail_n": len(cell.get("class_fail", []))}
    return rec


# ------------------------------------------------------------------ shear
SHEAR_FILE = os.path.join(REPO, "campaign_fresh_gravity", "_external_data", "cfg679_des", "2pt_maglim.fits")
M_MEAN, M_SIG = np.array([-0.006, -0.020, -0.024, -0.037]), np.array([0.009, 0.008, 0.008, 0.008])
DZ_SIG = np.array([0.018, 0.015, 0.011, 0.017])
KNL, CUTFRAC = 0.2, 0.20
ELL = np.geomspace(1.0, 2e5, 240)
ELLF = np.geomspace(1.0, 2e5, 24000)
LNLF = np.log(ELLF)


def load_shear():
    from astropy.io import fits
    h = fits.open(SHEAR_FILE)
    x = h["xip"].data
    n = len(x)
    C = np.asarray(h["COVMAT"].data[:n, :n], float)
    nz = h["nz_source"].data
    v = np.asarray(x["VALUE"], float)
    if MUT:
        v = -v                                                         # m2
    return {"i": np.asarray(x["BIN1"]) - 1, "j": np.asarray(x["BIN2"]) - 1, "ang": np.asarray(x["ANG"], float) * math.pi / 180 / 60, "val": v, "C": C,
            "z": np.asarray(nz["Z_MID"], float), "nz": np.array([nz[f"BIN{b}"] for b in range(1, 5)], float), "n": n}


def hankel(cl_on_ell, theta):
    """xi+(theta) = (1/2pi) int l C_l J0(l theta) dl on the fine log grid; cl_on_ell on ELL, positive or signed."""
    fine = CubicSpline(np.log(ELL), cl_on_ell)(LNLF)
    return np.trapz(ELLF ** 2 * fine * j0(np.outer(theta, ELLF)), LNLF, axis=1) / (2 * math.pi)


def shear_templates(S, o, Om, knl=None, dz=None):
    """Per bin-pair C_l templates GG, GI+IG (per unit A_IA), II (per unit A_IA^2); Mpc/h units; linear P(k,z)."""
    h = o["h"]
    zs = np.array(sorted(o["pk"].keys()))
    zs = zs[zs <= 3.0]
    k = o["pk"][0.0][:, 0]
    lnP = np.array([np.log(o["pk"][float(z)][:, 1]) for z in zs])
    spl = RectBivariateSpline(zs, np.log(k), lnP, kx=2, ky=3)
    zg = np.linspace(0.005, 2.995, 300)
    chi = o["DMf"](zg) * h                                             # Mpc/h
    Dg = np.exp(0.5 * spl(zg, math.log(0.05), grid=True)[:, 0] - 0.5 * spl(0.0, math.log(0.05), grid=True)[0, 0])
    Hh = o["Hf"](zg) / (100 * h)                                       # E(z)
    dchi = C_KMS / (100 * Hh)                                          # dchi/dz, Mpc/h
    nzs = []
    for b in range(4):
        zz = S["z"] - (0.0 if dz is None else dz[b])
        nb = np.interp(zg, zz, S["nz"][b], left=0.0, right=0.0)
        nb = nb / np.trapz(nb, zg)
        nzs.append(nb)
    nzs = np.array(nzs)
    pref = 1.5 * Om * (100.0 / C_KMS) ** 2
    q = np.zeros((4, len(zg)))
    for b in range(4):
        for iz in range(len(zg)):
            s = zg >= zg[iz]
            q[b, iz] = pref * chi[iz] * (1 + zg[iz]) * np.trapz(nzs[b][s] * (chi[s] - chi[iz]) / chi[s], zg[s])
    nchi = nzs / dchi                                                  # per Mpc/h
    F = -0.0134 * Om / Dg
    weight = dchi / chi ** 2
    G = {}
    for b1 in range(4):
        for b2 in range(b1, 4):
            G[(b1, b2)] = [np.zeros(len(ELL)), np.zeros(len(ELL)), np.zeros(len(ELL))]
    for il, ell in enumerate(ELL):
        kv = (ell + 0.5) / chi
        lnk = np.log(np.clip(kv, k[0], k[-1]))
        pv = np.exp(spl.ev(zg, lnk))
        over = kv > k[-1]
        pv[over] *= (kv[over] / k[-1]) ** -3
        if knl is not None:
            pv = np.where(kv <= knl, pv, 0.0)
        for (b1, b2), t in G.items():
            t[0][il] = np.trapz(weight * q[b1] * q[b2] * pv, zg)
            t[1][il] = np.trapz(weight * (nchi[b1] * q[b2] + nchi[b2] * q[b1]) * F * pv, zg)
            t[2][il] = np.trapz(weight * nchi[b1] * nchi[b2] * F ** 2 * pv, zg)
    return G


def shear_xi(S, G):
    """xi+ on the data ordering: GG, GI, II templates."""
    out = np.zeros((3, S["n"]))
    for (b1, b2), t in G.items():
        m = (S["i"] == b1) & (S["j"] == b2)
        if m.sum() == 0:
            m = (S["i"] == b2) & (S["j"] == b1)
        if m.sum():
            for a in range(3):
                out[a, m] = hankel(t[a], S["ang"][m])
    return out


def scale_cut_fix(S, o, Om):
    full = shear_xi(S, shear_templates(S, o, Om))[0]
    cut = shear_xi(S, shear_templates(S, o, Om, knl=KNL))[0]
    frac = np.abs(full - cut) / np.maximum(np.abs(full), 1e-30)
    return (frac <= CUTFRAC), frac


def shear_chi2(S, keep, o, Om):
    T = shear_xi(S, shear_templates(S, o, Om))
    gg = T[0]
    mi, mj = M_MEAN[S["i"]], M_MEAN[S["j"]]
    mfac = (1 + mi) * (1 + mj)
    Cadd = np.zeros_like(S["C"])
    for b in range(4):
        t = gg * ((S["i"] == b).astype(float) + (S["j"] == b).astype(float)) * mfac
        Cadd += M_SIG[b] ** 2 * np.outer(t, t)
        dz = np.zeros(4)
        dz[b] = DZ_SIG[b] * 0.5
        gp = shear_xi(S, shear_templates(S, o, Om, dz=dz))[0]
        t = (gp - gg) / (DZ_SIG[b] * 0.5) * mfac
        Cadd += DZ_SIG[b] ** 2 * np.outer(t, t)
    C = (S["C"] + Cadd)[np.ix_(keep, keep)]
    Ci = np.linalg.inv(C)
    d = S["val"][keep]
    Ag = np.linspace(-3, 3, 121)
    best = (np.inf, None)
    for a in Ag:
        m = ((T[0] + a * T[1] + a * a * T[2]) * mfac)[keep]
        r = d - m
        x = float(r @ Ci @ r)
        if x < best[0]:
            best = (x, float(a))
    # A_shear: one amplitude on the power, with A_IA profiled (reported)
    amps = np.geomspace(0.03, 30.0, 141)
    ba = (np.inf, None, None)
    for al in amps:
        for a in Ag[::2]:
            m = (al * (T[0] + a * T[1] + a * a * T[2]) * mfac)[keep]
            r = d - m
            x = float(r @ Ci @ r)
            if x < ba[0]:
                ba = (x, float(al), float(a))
    null = float(d @ Ci @ d)
    return {"chi2": best[0], "A_IA": best[1], "n": int(keep.sum()), "A_shear": ba[1], "chi2_at_A_shear": ba[0], "A_IA_at_A_shear": ba[2], "chi2_zero_signal": null}


# ------------------------------------------------------------------ forest
ZFOR = [3.6, 3.8, 4.0, 4.2, 4.4]
FGAM, FRJ = [1.0, 1.3, 1.6], [0.05, 0.12, 0.20]
FBS = np.array([6.0, 9.0, 13.0, 18.0, 23.0, 29.0, 35.0])
FFB = np.linspace(0.15, 0.90, 10)
NBOX, LBOX, STRIDE = 256, 64.0, 4


def forest_mod():
    sys.path.insert(0, os.path.join(HERE, "..", "P1D4_m6_native_3d_forest"))
    import forest3d as F3
    sys.path.pop(0)
    return F3


def forest_data():
    import io
    import tarfile
    from astropy.io import fits
    F3 = forest_mod()
    raw = os.path.join(REPO, "_external_data", "desi_dr1_p1d_qmle", "raw", "data_points.tar")
    with tarfile.open(raw) as tf:
        H = fits.open(io.BytesIO(tf.extractfile("desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits").read()))
        T = H["P1D_BLIND"].data
        Z = np.round(np.asarray(T["Z"], float), 2)
        K = np.asarray(T["K"], float)
        Pd = np.asarray(T["PLYA"], float)
        C = np.asarray(H["COVARIANCE"].data, float)
    BG = F3.Background()                                               # selection only (frozen as P1D4)
    KF = 2 * math.pi / LBOX
    D = {}
    for z in ZFOR:
        kmax = 0.5 * math.pi / (C_KMS * 0.8 / ((1 + z) * 1215.67))
        idx = np.where((Z == z) & (K > 0.001) & (K < kmax) & (K >= 2 * KF / BG.cz(z)))[0]
        D[z] = {"k": K[idx], "P": Pd[idx], "C": C[np.ix_(idx, idx)]}
    return D, F3


class Shim:
    """forest3d's Background interface fed by one cell's CLASS P(k,z) (Mpc/h), H(z) and growth rate."""

    def __init__(self, o, z):
        h = o["h"]
        arr = o["pk"][round(float(z), 2)]
        self.lk, self.lp = np.log(arr[:, 0]), np.log(arr[:, 1])
        pm, pp = o["pk"][round(z - 0.1, 2)], o["pk"][round(z + 0.1, 2)]
        i1 = int(np.argmin(np.abs(arr[:, 0] - 1.0)))
        self.f = float((0.5 * math.log(pp[i1, 1] / pm[i1, 1])) / (math.log((1 + z - 0.1) / (1 + z + 0.1))))
        self.cz_ = float(o["Hf"](z)) / (h * (1 + z))

    def P0(self, k):
        k = np.asarray(k, float)
        return np.exp(np.interp(np.log(k), self.lk, self.lp))

    def Dz(self, z):
        return 1.0

    def fz(self, z):
        return self.f

    def cz(self, z):
        return self.cz_


def forest_table(F3, bg, z, kd, tabpath):
    if os.path.exists(tabpath):
        return np.load(tabpath)["tab"]
    bx = F3.Box(NBOX, LBOX, 0, STRIDE)
    fz, cz = bg.fz(z), bg.cz(z)
    tab = np.zeros((len(FGAM), len(FRJ), len(FBS), len(FFB), len(kd)), np.float32)
    for j, rj in enumerate(FRJ):
        if STOP["flag"]:
            raise Preempted()
        dl, ps, vr = bx.gaussian(bg, z, rj)
        Dl = np.exp(dl - vr / 2).astype(np.float32)
        for g, gam in enumerate(FGAM):
            tr = F3.tau_redshift(Dl, ps, fz, gam, bx.dx)
            for ib, b in enumerate(FBS):
                for iF, Fb in enumerate(FFB):
                    kv, Pk, _, _ = F3.flux_p1d(tr, b, Fb, cz, bx.dx, bx.L)
                    m = kv > 0
                    tab[g, j, ib, iF] = np.exp(np.interp(np.log(kd), np.log(kv[m]), np.log(np.maximum(Pk[m], 1e-30))))
            del tr
    tmp = tabpath + ".tmp.npz"
    np.savez_compressed(tmp, tab=tab)
    os.replace(tmp, tabpath)
    return tab


def becker(z):
    return math.exp(-(0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132))


def forest_profile(tab, d, z):
    """chi2 at 2 % floor, profiled over (gamma, R_J) nodes and continuously-gridded (b, logit Fbar); also V-Fbar."""
    x1, x2 = FBS, np.log(FFB / (1 - FFB))
    fb = np.linspace(x1[0], x1[-1], 29)
    fx = np.linspace(x2[0], x2[-1], 37)
    FF = np.exp(fx) / (1 + np.exp(fx))
    tgt = becker(z)
    best = {"free": (np.inf,), "vfbar": (np.inf,)}
    for g in range(len(FGAM)):
        for j in range(len(FRJ)):
            lg = np.log(np.maximum(tab[g, j], 1e-30)).astype(float)
            fine = np.zeros((len(fb), len(fx), lg.shape[-1]))
            for ik in range(lg.shape[-1]):
                fine[:, :, ik] = RectBivariateSpline(x1, x2, lg[:, :, ik], kx=3, ky=3)(fb, fx)
            Pm = np.exp(fine)
            for ib in range(len(fb)):
                for iF in range(len(fx)):
                    m = Pm[ib, iF]
                    C = d["C"] + np.diag((0.02 * m) ** 2)
                    r = d["P"] - m
                    x = float(r @ np.linalg.solve(C, r))
                    if x < best["free"][0]:
                        best["free"] = (x, FGAM[g], FRJ[j], float(fb[ib]), float(FF[iF]))
                    if abs(FF[iF] / tgt - 1) <= 0.05 and x < best["vfbar"][0]:
                        best["vfbar"] = (x, FGAM[g], FRJ[j], float(fb[ib]), float(FF[iF]))
    return {"n": int(len(d["P"])), "F_becker": tgt, "free": best["free"], "vfbar": best["vfbar"]}


# ------------------------------------------------------------------ modes
def cell_obj(z=None, k=None):
    if k is not None:
        return {"name": k, "kind": "K", "mu": KCELLS[k]}
    return {"name": cellname(z), "kind": "R1", "zon": float(z)}


def mode_chain():
    L = Lik()
    pv, Av = P_START, A_START
    for z in ZONS:
        c = cell_obj(z=z)
        path = os.path.join(CELLS, c["name"] + ".json")
        if os.path.exists(path):
            rec = json.load(open(path))
        else:
            t0 = time.time()
            try:
                rec = fit_cell(L, c, pv, Av, maxit=1 if MUT else 10)
            except Preempted:
                print("preempted", c["name"], flush=True)
                sys.exit(75)
            if STOP["flag"]:
                sys.exit(75)
            rec.update(cell=c["name"], kind="R1", zon=c["zon"], elapsed_s=time.time() - t0)
            jw(path, rec)
        print(c["name"], rec.get("status"), (rec.get("chi2") or {}).get("plik"), rec.get("sigma8"), rec.get("converged"), flush=True)
        if rec.get("status") == "OK":
            pv, Av = np.array([rec["params"][n] for n in NAMES]), rec["A"]


def mode_khronon():
    L = Lik()
    d = None
    p1 = os.path.join(CELLS, f"{cellname(1e6)}.json")
    r = json.load(open(p1))
    pv, Av = np.array([r["params"][n] for n in NAMES]), r["A"]
    for k in KCELLS:
        c = cell_obj(k=k)
        path = os.path.join(CELLS, c["name"] + ".json")
        if os.path.exists(path):
            continue
        t0 = time.time()
        try:
            rec = fit_cell(L, c, pv, Av)
        except Preempted:
            sys.exit(75)
        if STOP["flag"]:
            sys.exit(75)
        rec.update(cell=c["name"], kind="K", mu=c["mu"], elapsed_s=time.time() - t0)
        jw(path, rec)
        print(c["name"], rec.get("status"), (rec.get("chi2") or {}).get("plik"), rec.get("sigma8"), flush=True)


def fixed_cut():
    """Scale cut, fixed once at z_on = 1e6's best fit, before any shear chi2 (FROZEN §4)."""
    cp = os.path.join(CELLS, "shear_scale_cut.json")
    S = load_shear()
    if os.path.exists(cp):
        q = json.load(open(cp))
        return S, np.array(q["keep"], bool), q
    r = json.load(open(os.path.join(CELLS, f"{cellname(1e6)}.json")))
    c = cell_obj(z=1e6)
    o = run("pkcut", c, np.array([r["params"][n] for n in NAMES]), pk=True, cmb=False)
    keep, frac = scale_cut_fix(S, o, r["Omega_m"])
    q = {"keep": keep.tolist(), "frac": frac.tolist(), "n_keep": int(keep.sum()), "rule": f"k_NL {KNL} h/Mpc, change <= {CUTFRAC}", "sha256_file": sha(SHEAR_FILE),
         "theta_kept_arcmin": sorted(set(np.round(S["ang"][keep] * 180 * 60 / math.pi, 1).tolist()))}
    jw(cp, q)
    return S, keep, q


def mode_channel(name, do_forest=True):
    rp = os.path.join(CELLS, name + ".json")
    r = json.load(open(rp))
    if r.get("status") != "OK":
        return
    outp = os.path.join(CELLS, name + "_channels.json")
    res = json.load(open(outp)) if os.path.exists(outp) else {}
    if "shear" in res and ("forest" in res or not do_forest):
        return
    c = {"name": name, "kind": r["kind"], "zon": r.get("zon"), "mu": r.get("mu")}
    S, keep, q = fixed_cut()
    p = np.array([r["params"][n] for n in NAMES])
    o = run("pk", c, p, pk=True, cmb=False)
    if o is None:
        res["status"] = "PK_FAIL"
        res["msg"] = c.get("class_fail", ["?"])[-1]
        jw(outp, res)
        return
    if "shear" not in res:
        res["shear"] = shear_chi2(S, keep, o, r["Omega_m"])
        jw(outp, res)
    if not do_forest:
        return
    D, F3 = forest_data()
    fo = res.get("forest", {})
    tabdir = os.path.join(WORK, "forest", name)
    os.makedirs(tabdir, exist_ok=True)
    for z in ZFOR:
        kz = f"{z:.1f}"
        if kz in fo:
            continue
        try:
            t = forest_table(F3, Shim(o, z), z, D[z]["k"], os.path.join(tabdir, f"z{z:.1f}.npz"))
        except Preempted:
            sys.exit(75)
        fo[kz] = forest_profile(t, D[z], z)
        res["forest"] = fo
        jw(outp, res)
        if STOP["flag"]:
            sys.exit(75)


def mode_checks():
    res = {"mutate": MUT}
    L = Lik()
    c0 = {"name": "checks", "kind": "R1", "zon": 1100.0}
    # K2: harness on C7's parameters (tool check, not a yardstick)
    lc = {"omega_b": P_START[0], "omega_cdm": P_START[1], "100*theta_s": P_START[2], "ln10^{10}A_s": P_START[3], "n_s": P_START[4], "tau_reio": P_START[5]}
    v = run("van", c0, None, vanilla=True, lcdm_params=lc)
    q = L.parts(v, A_START)
    tot = q["plik"] + q["lowTT"] + q["lowEE"] + q["Aprior"]
    res["K2"] = {"value": tot, "target": C7F["chi2"]["total"], "pass": abs(tot - C7F["chi2"]["total"]) <= 2.0}
    # K1
    w = run("off", c0, None, zon_off=True, lcdm_params=lc)
    m = np.arange(len(v["tt"])) >= 2
    dmax = max(float(np.max(np.abs(w[k][m] / v[k][m] - 1))) for k in ("tt", "ee", "pp"))
    if MUT:
        dmax = max(dmax, float(np.max(np.abs(w["tt"][m] * 1.01 / v["tt"][m] - 1))))   # m3
    res["K1"] = {"value": dmax, "pass": dmax <= 1e-4}
    # K3
    o = run("k3", c0, None, lcdm_params=lc, keep=True)
    bg, cols = o["bg_all"]
    zb = bg[:, cols["z"]]
    rc = bg[:, cols["(.)rho_cdm"]]
    oth = sum(bg[:, cols[k]] for k in ("(.)rho_g", "(.)rho_b", "(.)rho_cdm", "(.)rho_lambda", "(.)rho_ur"))
    rres = bg[:, cols["(.)rho_tot"]] - oth
    xb = -np.log(1 + zb)
    sel = (zb > 1100 * math.exp(-0.5)) & (zb < 1100 * math.exp(0.5))
    vi = float(np.max(np.abs(np.gradient(rc + rres, xb)[sel] + 3 * rc[sel])) / np.max(3 * rc[sel]))
    res["K3"] = {"value": vi, "pass": vi <= 2e-3}
    _clean(os.path.join(WORK, "checks"), "k3")
    # K4
    s = 1e-3
    S = load_shear()
    th = np.unique(S["ang"])
    an = np.exp(-th ** 2 / (4 * s * s)) / (4 * math.pi * s * s)
    nu = hankel(np.exp(-ELL ** 2 * s * s), th)
    mk = an > 1e-3 * an.max()
    e4 = float(np.max(np.abs(nu[mk] / an[mk] - 1)))
    res["K4"] = {"value": e4, "pass": e4 <= 1e-3}
    # K5
    ev = np.linalg.eigvalsh(S["C"])
    res["K5"] = {"sha256": sha(SHEAR_FILE), "n": S["n"], "min_eig": float(ev.min()), "pass": S["n"] == 200 and ev.min() > 0}
    # K6
    D, F3 = forest_data()
    bgn = F3.Background()

    class Pass:
        P0, Dz, fz, cz = bgn.P0, bgn.Dz, bgn.fz, bgn.cz
    bx = F3.Box(NBOX, LBOX, 0, STRIDE)
    d1, _, _ = bx.gaussian(bgn, 3.0, 0.1)
    d2, _, _ = bx.gaussian(Pass, 3.0, 0.1)
    e6 = float(np.max(np.abs(d1 - d2)))
    pg = (np.abs(bx.dx * np.fft.rfft(d1, axis=2)) ** 2 / bx.L).mean(axis=(0, 1))
    ana = F3.p1d_analytic(bgn, 3.0, 0.1, bx.kpar)
    mk = (bx.kpar >= bx.kf) & (bx.kpar <= 6.0)
    e6b = float(np.max(np.abs(pg[mk] / ana[mk] - 1)))
    res["K6_profile"] = {"k": bx.kpar[mk].tolist(), "ratio": (pg[mk] / ana[mk]).tolist()}
    res["K6"] = {"shim_max_abs": e6, "gauss_vs_analytic": e6b, "pass": e6 <= 1e-5 and e6b <= 0.05}
    # K7
    src = open(os.path.abspath(__file__)).read().splitlines()
    bad = [i for i, ln in enumerate(src) if re.search(r"5\.364|0\.674|HMcode|halofit|Halofit", ln) and "BANNED_GUARD" not in ln]   # BANNED_GUARD
    res["K7"] = {"lines": bad, "pass": not bad}
    # K8
    p = P_START
    c1 = cell_obj(z=1e6)
    a = L.parts(run("k8a", c1, p), A_START)
    b = L.parts(run("k8b", c1, p), A_START)
    res["K8"] = {"delta": abs(a["plik"] - b["plik"]), "plik": a["plik"], "pass": abs(a["plik"] - b["plik"]) <= 1e-6}
    jw(os.path.join(CELLS, "checks.json"), res)
    print({k: v.get("pass") for k, v in res.items() if isinstance(v, dict)}, flush=True)


def mode_k9():
    env = dict(os.environ, RF5_K9_CELL="1", OMP_NUM_THREADS="1")
    tcell = "R1_K9TEST"
    ck = os.path.join(WORK, tcell + "_ck.npz")
    if os.path.exists(ck):
        os.remove(ck)
    pr = subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), "k9child"], env=env)
    time.sleep(240)
    has_before = os.path.exists(ck)
    pr.terminate()
    rc = pr.wait()
    z0 = np.load(ck, allow_pickle=True) if os.path.exists(ck) else None
    res = {"rc_first": rc, "checkpoint_written": has_before or z0 is not None, "pass": rc == 75 and z0 is not None}
    if z0 is not None:
        it0 = int(z0["it"])
        p2 = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "k9child", "1"], env=env, capture_output=True, text=True)
        res["rc_resume"] = p2.returncode
        res["resume_out"] = p2.stdout[-200:]
        z1 = np.load(ck, allow_pickle=True)
        res["it_before"], res["it_after"] = it0, int(z1["it"])
        res["pass"] = res["pass"] and p2.returncode == 0 and "RESUMED_FROM_CHECKPOINT" in p2.stdout
    jw(os.path.join(CELLS, "k9.json"), res)
    print(res, flush=True)


def mode_k9child(resume=False):
    L = Lik()
    c = {"name": "R1_K9TEST", "kind": "R1", "zon": 1e6}
    ck = os.path.join(WORK, c["name"] + "_ck.npz")
    if resume and os.path.exists(ck):
        print("RESUMED_FROM_CHECKPOINT", flush=True)
    try:
        rec = fit_cell(L, c, P_START, A_START, maxit=2 if not resume else max(1, int(np.load(ck, allow_pickle=True)["it"]) + 1))
    except Preempted:
        sys.exit(75)
    if STOP["flag"]:
        sys.exit(75)
    print(rec.get("status"), flush=True)


def pval(x, dof):
    return float(CHI2.sf(x, dof))


def mode_grade():
    out = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        out.append(s)

    RES = {"lane": "RF5_growth_native_yardstick", "criteria": "469657249b", "mutate": MUT, "cells": {}, "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed"}
    P("RF5_growth_native_yardstick" + (" MUTATE" if MUT else "") + ": criteria 469657249b; kappa = 1/2 FITTED; no Delta chi2 to LCDM anywhere; footings share the surface (a0 absent at linear order)")
    ck = json.load(open(os.path.join(CELLS, "checks.json"))) if os.path.exists(os.path.join(CELLS, "checks.json")) else {}
    k9 = json.load(open(os.path.join(HERE, "cells", "k9.json"))) if os.path.exists(os.path.join(HERE, "cells", "k9.json")) else {}
    RES["checks"] = ck
    RES["K9"] = k9
    P("checks:", {k: v.get("pass") for k, v in ck.items() if isinstance(v, dict)}, "K9", k9.get("pass"))
    cut = json.load(open(os.path.join(CELLS, "shear_scale_cut.json"))) if os.path.exists(os.path.join(CELLS, "shear_scale_cut.json")) else {}
    RES["shear_cut"] = {k: cut.get(k) for k in ("n_keep", "rule", "theta_kept_arcmin", "sha256_file")}
    rows = {}
    names = [cellname(z) for z in ZONS] + list(KCELLS)
    for n in names:
        p = os.path.join(CELLS, n + ".json")
        if not os.path.exists(p):
            rows[n] = {"status": "UNDETERMINED (not finished)"}
            continue
        r = json.load(open(p))
        if r.get("status") != "OK":
            rows[n] = {"status": "UNDETERMINED (CLASS failed)", "msg": r.get("msg")}
            continue
        c = r["chi2"]
        pc = os.path.join(CELLS, n + "_channels.json")
        ch = json.load(open(pc)) if os.path.exists(pc) else {}
        row = {"status": "OK", "zon": r.get("zon"), "plik": c["plik"], "lowTT": c["lowTT"], "lowEE": c["lowEE"], "Aprior": c["Aprior"], "bao": c["bao"], "sn": c["sn"], "n_sn": c["n_sn"],
               "p_plik": pval(c["plik"], 605), "p_bao": pval(c["bao"], 13), "p_sn": pval(c["sn"], c["n_sn"] - 1), "sigma8": r["sigma8"], "h": r["h"], "Omega_m": r["Omega_m"], "params": r["params"],
               "converged": r["converged"], "sqrtX": r["sqrtX"], "A": r["A"]}
        row["G_A0"] = all(BAND[z][0] <= r["sqrtX"].get(str(z), -1) <= BAND[z][1] for z in BAND) if r["sqrtX"] else None
        H2 = (100 * r["h"] * 1e3 / 3.0857e22) ** 2
        rc = 3 * H2 / (8 * math.pi * 6.6743e-11)
        cc = 299792458.0
        a0c = 0.5 * cc * math.sqrt(6.6743e-11 * rc * r["Omega_DE"]) if r["Omega_DE"] == r["Omega_DE"] else None
        a0a = 0.5 * cc * math.sqrt(6.6743e-11 * rc)
        sx233 = r["sqrtX"].get("2.33")
        row["a0"] = {"canonical": {"a0_0": a0c, "a0_2.33": a0c * sx233 if a0c and sx233 else None}, "alt": {"a0_0": a0a, "a0_2.33": a0a * sx233 if sx233 else None}}
        sh = ch.get("shear")
        if sh:
            row["shear"] = sh
            row["p_shear"] = pval(sh["chi2"], sh["n"] - 1)
        fo = ch.get("forest", {})
        if fo:
            row["forest"] = {"n_z": len(fo)}
            if len(fo) == len(ZFOR):
                x = sum(v["free"][0] for v in fo.values())
                nb = sum(v["n"] for v in fo.values())
                row["forest"].update(chi2=x, dof=nb - 4 * len(ZFOR), p=pval(x, nb - 4 * len(ZFOR)), p_min_z=min(pval(v["free"][0], v["n"] - 4) for v in fo.values()),
                                     vfbar=sum(v["vfbar"][0] for v in fo.values()), per_z={k: v["free"] for k, v in fo.items()})
        rows[n] = row
    # surface
    S = {}
    for n in [cellname(z) for z in ZONS]:
        w = rows[n]
        if w["status"] == "OK" and "shear" in w:
            S[n] = w["plik"] + w["Aprior"] + w["bao"] + w["sn"] + w["shear"]["chi2"]
    # forest G0 at the best forest cell
    ff = {n: rows[n]["forest"] for n in rows if rows[n].get("forest", {}).get("chi2") is not None and rows[n].get("zon")}
    g0 = None
    if ff:
        nb = min(ff, key=lambda n: ff[n]["chi2"])
        g0 = {"best_cell": nb, "chi2": ff[nb]["chi2"], "dof": ff[nb]["dof"], "p": ff[nb]["p"], "p_min_z": ff[nb]["p_min_z"], "pass": ff[nb]["p"] >= 0.01 and ff[nb]["p_min_z"] >= 1e-3}
    RES["G0_forest"] = g0
    live_forest = bool(g0 and g0["pass"])
    if live_forest:
        for n in list(S):
            if rows[n].get("forest", {}).get("chi2") is not None:
                S[n] += rows[n]["forest"]["chi2"]
    Smin = min(S.values()) if S else None
    RES["S_min"] = Smin
    P(f"forest G0: {g0}; live in verdict: {live_forest}")
    P(f"S_min {Smin}")
    P(f"{'cell':10s} {'plik':>9s} {'p':>8s} {'lowTT':>9s} {'lowEE':>8s} {'bao':>8s} {'sn':>8s} {'shear/n':>12s} {'A_sh':>6s} {'s8':>6s} {'Om':>6s} {'h':>6s} {'w0':>6s} {'wa':>6s} {'S-Smin':>9s} {'forest':>12s} {'G':>4s}")
    window, window_abs = [], []
    for n in names:
        w = rows[n]
        if w["status"] != "OK":
            P(f"{n:10s} {w['status']} {w.get('msg', '')}")
            continue
        g = {"G_CMB": w["p_plik"] >= 1e-3, "G_BAO": w["p_bao"] >= 1e-3, "G_SN": w["p_sn"] >= 1e-3, "G_A0": bool(w["G_A0"])}
        if "shear" in w and w["shear"]["n"] >= 10:
            g["G_SHEAR"] = w["p_shear"] >= 1e-3
        else:
            g["G_SHEAR"] = None
        if live_forest:
            g["G_FOREST"] = (w.get("forest", {}).get("p", 0) >= 1e-3) if w.get("forest", {}).get("chi2") is not None else None
        if n in S:
            w["S"] = S[n]
            w["S_minus_Smin"] = S[n] - Smin
            g["G_S"] = S[n] - Smin <= 25
        w["gates"] = g
        absok = all(v for k, v in g.items() if k != "G_S") and None not in [v for k, v in g.items() if k != "G_S"]
        fully = absok and g.get("G_S") is True
        w["abs_pass"], w["window_pass"] = bool(absok), bool(fully)
        if w.get("zon") and absok:
            window_abs.append(w["zon"])
        if w.get("zon") and fully:
            window.append(w["zon"])
        sh = w.get("shear", {})
        fx = w.get("forest", {})
        ftxt = f"{fx.get('chi2', float('nan')):.0f}/{fx.get('dof', 0)}" if fx.get("chi2") is not None else "-"
        P(f"{n:10s} {w['plik']:9.1f} {w['p_plik']:8.1e} {w['lowTT']:9.1f} {w['lowEE']:8.1f} {w['bao']:8.1f} {w['sn']:8.1f} {sh.get('chi2', float('nan')):7.1f}/{sh.get('n', 0):<4d} {sh.get('A_shear') or float('nan'):6.2f} "
          f"{w['sigma8']:6.3f} {w['Omega_m']:6.3f} {w['h']:6.3f} {w['params']['w0']:6.2f} {w['params']['wa']:6.2f} {w.get('S_minus_Smin', float('nan')):9.1f} {ftxt:>12s} {'Y' if fully else ('a' if absok else 'n'):>4s} conv={w['converged']}")
    RES["cells"] = rows
    RES["window_grid"] = sorted(window)
    RES["window_abs_only"] = sorted(window_abs)
    undet = [n for n in names if rows[n]["status"] != "OK" or "shear" not in rows[n]]
    RES["undetermined"] = undet
    fl = "forest live" if live_forest else ("forest NOT DIAGNOSTIC (G0)" if g0 else "forest UNDETERMINED (not finished)")
    if window:
        v = f"a window exists at z_on in [{min(window):.0f}, {max(window):.0f}] ({fl}; CMB = plik-lite; shear = DES Y3 xi+ linear-safe)"
    elif not undet:
        v = f"FAILS on raw forest + CMB spectra + shear at every turn-on epoch ({fl})"
    else:
        v = f"UNDETERMINED: no window among finished cells; unfinished {undet} ({fl})"
    RES["verdict"] = {"canonical": v, "alt": v, "note": "same surface: a0 absent at linear order; per-footing a0 readings are in cells[*].a0"}
    kv = {}
    for k in KCELLS:
        w = rows[k]
        kv[k] = "UNDETERMINED" if w["status"] != "OK" else ("PASSES" if w.get("abs_pass") else "FAILS")
    RES["verdict_khronon"] = kv
    P("VERDICT canonical:", v)
    P("VERDICT alt:", v)
    P("v3s khronon rows:", kv)
    if MUT:
        w = rows.get(cellname(1e6), {})
        m = {"G_CMB_fails": w.get("p_plik", 1) < 1e-3, "G_SHEAR_fails": (w.get("p_shear", 1) < 1e-3), "K1_fails": not ck.get("K1", {}).get("pass", True)}
        RES["mutate_bites"] = m
        P("MUTATE:", m)
    RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    jw(os.path.join(HERE, f"rf5_results{TAG}.json"), RES)
    open(os.path.join(HERE, f"rf5{TAG}.out"), "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "grade"
    if mode == "checks":
        mode_checks()
    elif mode == "chain":
        mode_chain()
    elif mode == "khronon":
        mode_khronon()
    elif mode == "channel":
        mode_channel(sys.argv[2], do_forest=(len(sys.argv) < 4 or sys.argv[3] != "noforest"))
    elif mode == "k9":
        mode_k9()
    elif mode == "k9child":
        mode_k9child(len(sys.argv) > 2)
    elif mode == "grade":
        mode_grade()
    else:
        sys.exit("unknown mode")
