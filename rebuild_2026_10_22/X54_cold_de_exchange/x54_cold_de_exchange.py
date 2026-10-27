#!/usr/bin/env python3
"""X54_cold_de_exchange: does CMB + DESI DR2 BAO + SN data allow or prefer an energy exchange between cold dark energy
(rho_c, the gravitating w = 0 clumping field component; never a particle) and dark energy (rho_DE)?

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (04200bb449, committed alone first).
Model C (primary): Q = xi H rho_c; model D (reported): Q = xi H rho_DE; xi > 0 = DE -> cold. Q^mu along u_c (zero
momentum transfer in the cold rest frame, deltaQ = 0 on cold-comoving slices). Patched CLASS (x54_make_patch.py).
Likelihood: C2's plik-lite + low-l TT/EE + A prior; DESI DR2 BAO (CFG689 table verbatim); DES-SN5YR primary, Pantheon+
and Union3 reported (CFG689/CFG684 loaders). Profile likelihood in xi with Gauss-Newton/Broyden refits (X34 template).
No LCDM-derived input: omega_c (cold dark energy abundance), xi and the CMB parameters are free; C7's LCDM refit is the
optimiser's start point only.

Run:  python3 -I x54_make_patch.py   (once; builds the binary outside the repository)
      PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I x54_cold_de_exchange.py
      X54_MUTATE=1 ... -> *_MUTATE outputs; K1 and K3 must FAIL; profiles skipped.
Build dir: $X54_BUILD (default <system temp>/x54_class_build). kappa = 1/2 FITTED; footings never pooled; no particle.
"""
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
from scipy.interpolate import CubicSpline, InterpolatedUnivariateSpline
from scipy.io import FortranFile
from scipy.optimize import minimize, least_squares

T0 = time.time()
MUT = os.environ.get("X54_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
BUILD = os.environ.get("X54_BUILD", os.path.join(tempfile.gettempdir(), "x54_class_build"))
X54B = os.path.join(BUILD, "class_x54", "class")
RUNS = os.path.join(BUILD, f"runs{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x54_cold_de_exchange{TAG}.out"), "w")
RES = {"lane": "X54_cold_de_exchange", "criteria": "04200bb449", "date": "2026-10-26", "mutate": MUT, "checks": {},
       "note": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle"}
CHK = []
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
Z_REC = 1090.0
C_KMS = 299792.458


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
    json.dump(RES, open(os.path.join(HERE, f"x54_cold_de_exchange_results{TAG}.json"), "w"), indent=1, default=float)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P(f"X54_cold_de_exchange {'MUTATE run' if MUT else 'normal run'}; frozen 04200bb449")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; "
  "not theory closed; the cosmological fit contains no a0")
RES["binaries"] = {"vanilla_sha256": sha(VAN), "x54_sha256": sha(X54B), "patch_sha256": sha(os.path.join(HERE, "x54_exchange.patch"))}
P(f"binaries: vanilla {RES['binaries']['vanilla_sha256'][:16]}, x54 {RES['binaries']['x54_sha256'][:16]}, "
  f"patch {RES['binaries']['patch_sha256'][:16]}")

# ------------------------------------------------------------------ C2's CMB likelihood (read-only exec, as Q6/X34)
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
CHI2_C7 = C7F["chi2"]["total"]

# ------------------------------------------------------------------ BAO (DESI DR2, verbatim from CFG689 / cfg681_bao.py)
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
ISO = [(0.295, 7.942, 0.075)]                                   # BGS D_V/r_d
LINV = []
for (_, _, _, s1, _, s2, r) in ANISO:
    Cm = np.array([[s1 ** 2, r * s1 * s2], [r * s1 * s2, s2 ** 2]])
    LINV.append(np.linalg.inv(np.linalg.cholesky(Cm)))
CINV = [np.linalg.inv(np.array([[s1 ** 2, r * s1 * s2], [r * s1 * s2, s2 ** 2]])) for (_, _, _, s1, _, s2, r) in ANISO]


def bao_resid(DMf, Hf, rd):
    """whitened residuals; DMf(z), Hf(z) [km/s/Mpc] callables, rd [Mpc]"""
    out = []
    for (n, z, dm, _, dh, _, _), Li in zip(ANISO, LINV):
        m = np.array([DMf(z) / rd, C_KMS / Hf(z) / rd])
        out.extend(Li @ (np.array([dm, dh]) - m))
    for (z, dv, s) in ISO:
        m = (z * DMf(z) ** 2 * C_KMS / Hf(z)) ** (1 / 3) / rd
        out.append((dv - m) / s)
    return np.array(out)


# ------------------------------------------------------------------ SN loaders (CFG689 / CFG684, verbatim logic)
EXT684 = os.path.join(EXT, "cfg684_inputs")


def load_sn(which):
    if which == "PP":
        E = os.path.join(EXT, "pantheonplus_dr")
        raw = np.genfromtxt(os.path.join(E, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
        cov = np.loadtxt(os.path.join(E, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1)
        n = int(round(np.sqrt(cov.size)))
        cov = cov.reshape(n, n)
        sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)
        z, zh, mb = raw["zHD"][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float)
        W = np.linalg.inv(cov[np.ix_(sel, sel)])
        lab = "Pantheon+ non-calibrators, zHD > 0.01"
    elif which == "DES5":
        rows = [l.split() for l in open(os.path.join(EXT684, "des5", "DES-Dovekie_HD.csv")) if l.startswith("SN:")]
        dz = np.array([float(r[3]) for r in rows]); dzh = np.array([float(r[4]) for r in rows])
        dmu = np.array([float(r[5]) for r in rows])
        npz = np.load(os.path.join(EXT684, "des5", "STAT+SYS.npz"))
        n_ = int(npz[npz.files[0]][0])
        Wd = np.zeros((n_, n_)); Wd[np.triu_indices(n_)] = npz[npz.files[1]]
        Wd = Wd + np.triu(Wd, 1).T
        ww = dz > 0
        Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]
        z, zh, mb, W = dz[ww], dzh[ww], dmu[ww], np.linalg.inv(Cd)
        lab = "DES-SN5YR Dovekie (CFG684 loader)"
    else:
        from astropy.io import fits
        M_ = fits.open(os.path.join(EXT684, "union3", "mu_mat_union3_cosmo=2_mu.fits"))[0].data
        z, mb, W = M_[0, 1:], M_[1:, 0], M_[1:, 1:]
        zh = z
        lab = "Union3 nodes (CFG684 loader)"
    one = np.ones(len(mb))
    w1 = W @ one
    Wp = W - np.outer(w1, w1) / (one @ w1)                    # M marginalised analytically
    Wp = 0.5 * (Wp + Wp.T)
    ev, U = np.linalg.eigh(Wp)
    keep = ev > ev.max() * 1e-12
    S = (U[:, keep] * np.sqrt(ev[keep])).T                    # residual = S r, r^T Wp r = |S r|^2
    return dict(z=z, zh=zh, mb=mb, W=W, Wp=Wp, S=S, lab=lab, n=len(mb), A11=one @ w1, one=one)


SN = {k: load_sn(k) for k in ("DES5", "PP", "U3")}
for k, v in SN.items():
    P(f"SN {k}: {v['n']} {v['lab']}")


def sn_resid(sn, DMf):
    r = sn["mb"] - 5 * np.log10((1 + sn["zh"]) * DMf(sn["z"]))
    return sn["S"] @ r


def sn_chi2_cfg689(sn, DMf):                                  # CFG689's sn_chi2 form (S0-2)
    r = sn["mb"] - 5 * np.log10((1 + sn["zh"]) * DMf(sn["z"]))
    v = sn["W"] @ r
    b = sn["one"] @ v
    return r @ v - b * b / sn["A11"]


# ------------------------------------------------------------------ CLASS runner (Q6/X34 precision)
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
TCMB = 2.7255
NRUN = [0]
FAILMSG = {}


def run(name, binary, params, xi=None, model="C", pk=False, cmb=True, extra=None, keep=False):
    p = {"T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2, "thermodynamics_verbose": 1,
         "fourier_verbose": 1, "overwrite_root": "yes", "write_background": "yes", **params}
    if cmb:
        p.update({"output": "tCl,pCl,lCl,mPk" if pk else "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": 2508, **HIGH, **START})
        if pk:
            p["P_k_max_h/Mpc"] = 10.0
    if extra:
        p.update(extra)
    root = os.path.join(RUNS, name + "_")
    p["root"] = root
    with open(root + ".ini", "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    env = dict(os.environ, OMP_NUM_THREADS="1")
    for k_ in ("X54_XI", "X54_MODEL", "X54_BUG"):
        env.pop(k_, None)
    if xi is not None:
        env["X54_XI"] = repr(float(xi))
        env["X54_MODEL"] = model
        if MUT:
            env["X54_BUG"] = "1"
    t_launch = time.time()
    r = subprocess.run(["nice", "-n", "15", binary, root + ".ini"], capture_output=True, text=True, env=env)
    NRUN[0] += 1
    pre = root + "_"
    if r.returncode != 0:
        txt = (r.stdout + r.stderr).strip()
        FAILMSG[name] = txt.splitlines()[-1][-300:] if txt else "?"
        for f in os.listdir(RUNS):
            if f.startswith(name + "_"):
                os.remove(os.path.join(RUNS, f))
        return None
    log = r.stdout
    out = {"log": log, "root": pre}
    if cmb:
        assert os.path.getmtime(pre + "cl_lensed.dat") >= t_launch - 1, "stale-output guard"
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
    out["bg"] = {k: bg[:, cols[c]][::-1][sel] for k, c in (("z", "z"), ("H", "H [1/Mpc]"), ("DM", "comov. dist."),
                                                         ("rc", "(.)rho_cdm"), ("rl", "(.)rho_lambda"), ("rb", "(.)rho_b"),
                                                         ("rg", "(.)rho_g"), ("rur", "(.)rho_ur"), ("rtot", "(.)rho_tot"))}
    zb = out["bg"]["z"]
    m = zb <= 3.0
    out["DMf"] = CubicSpline(zb[m], out["bg"]["DM"][m])
    out["Hf"] = CubicSpline(zb[m], out["bg"]["H"][m] * C_KMS)
    mm = re.search(r"found 'h = ([0-9.eE+-]+)'", log)
    out["h"] = float(mm.group(1)) if mm else float(p.get("h", np.nan))
    mm = re.search(r"sigma8=([0-9.]+) for total matter", log)
    out["sigma8"] = float(mm.group(1)) if mm else np.nan
    mm = re.search(r"baryon drag stops at z = [0-9.eE+-]+\s+corresponding to conformal time = [0-9.eE+-]+ Mpc\s+"
                   r"with comoving sound horizon rs = ([0-9.eE+-]+) Mpc", log)
    out["rd"] = float(mm.group(1)) if mm else np.nan
    if not keep:
        for f in os.listdir(RUNS):
            if f.startswith(name + "_"):
                os.remove(os.path.join(RUNS, f))
    return out


def binned(o):
    return NS["binned"](o["tt"], o["te"], o["ee"])


def chi2_cmb(o, A):
    Tb = binned(o)
    c = {"plik": NS["chi2_plik"](Tb, A), "lowTT": NS["chi2_lowTT"](o["tt"], A), "lowEE": NS["chi2_lowEE"](o["ee"], A),
         "Aprior": ((A - 1) / 0.0025) ** 2}
    c["cmb"] = sum(c.values())
    return c


def chi2_all(o, A, sn):
    c = chi2_cmb(o, A)
    c["bao"] = float(np.sum(bao_resid(o["DMf"], o["Hf"], o["rd"]) ** 2))
    c["sn"] = float(np.sum(sn_resid(SN[sn], o["DMf"]) ** 2))
    c["total"] = c["cmb"] + c["bao"] + c["sn"]
    return c


def resid(o, A, tau, sn):
    Tb = binned(o)
    return np.concatenate((np.linalg.solve(NS["Lc"], NS["Xd"] - Tb / A ** 2), [(A - 1) / 0.0025, (tau - TAU_HAT) / SIG_TAU],
                           bao_resid(o["DMf"], o["Hf"], o["rd"]), sn_resid(SN[sn], o["DMf"])))


def base(p):
    wb, wc, th, lnA, ns, tau = p
    return {"omega_b": wb, "omega_cdm": wc, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau}


# ------------------------------------------------------------------ analytic exchange background (frozen section 1)
def rho_cl(model, xi, oc, ol, a):
    """rho_c, rho_DE in units of H0^2 (Omega0 units)"""
    a = np.asarray(a, float)
    if model == "C":
        return oc * a ** (-(3 - xi)), ol + xi * oc / (3 - xi) * (a ** (-(3 - xi)) - 1)
    B = xi * ol / (3 - xi)
    return (oc - B) * a ** -3 + B * a ** (-xi), ol * a ** (-xi)


def sqrtX(model, xi, oc, ol, z):
    rl = rho_cl(model, xi, oc, ol, 1 / (1 + np.asarray(z, float)))[1]
    return np.where(rl > 0, np.sqrt(np.maximum(rl, 0) / ol), 0.0)


def F_made(model, xi, oc, ol):
    a = 1 / (1 + Z_REC)
    rc = rho_cl(model, xi, oc, ol, a)[0]
    return float(1 - rc * a ** 3 / oc)


# ================================================================== STEP 0
P("\n== STEP 0 (stop rule)")
o_l = run("S0_lcdm", VAN, base(P0), pk=True)
c_l = chi2_cmb(o_l, A0)
check("S0-1_C7_LCDM_chi2", abs(c_l["cmb"] - CHI2_C7) <= 2.0,
      f"chi2 {c_l['cmb']:.3f} (plik {c_l['plik']:.2f}, lowTT {c_l['lowTT']:.2f}, lowEE {c_l['lowEE']:.2f}) vs C7 {CHI2_C7:.3f}",
      "|diff| <= 2")
# S0-2: CFG681's flat-LCDM BAO-only and BAO + Pantheon+ numbers (CFG689 K3's construction, Omega_r exactly CFG681's)
zg = np.linspace(0, 2.5, 5001)


def cumchi(Hg):
    return np.r_[0, np.cumsum(0.5 * (1 / Hg[1:] + 1 / Hg[:-1]) * np.diff(zg))] * C_KMS


OMR681 = 2.469e-5 / 0.68 ** 2 * (1 + 0.2271 * 3.046)


def chi681(om, use_sn):
    if not 0.15 <= om <= 0.45:
        return 1e9
    Hg = 100 * 0.68 * np.sqrt(om * (1 + zg) ** 3 + OMR681 * (1 + zg) ** 4 + (1 - om - OMR681))
    I = cumchi(Hg)
    DMf = lambda z: np.interp(z, zg, I)
    Hf = lambda z: np.interp(z, zg, Hg)
    ms = [np.array([DMf(t[1]), C_KMS / Hf(t[1])]) for t in ANISO]
    mv = [(t[0] * DMf(t[0]) ** 2 * C_KMS / Hf(t[0])) ** (1 / 3) for t in ISO]
    ds = [np.array([t[2], t[4]]) for t in ANISO]
    s = (sum(m @ Ci @ d for m, d, Ci in zip(ms, ds, CINV)) + sum(v * t[1] / t[2] ** 2 for v, t in zip(mv, ISO))) / (
        sum(m @ Ci @ m for m, Ci in zip(ms, CINV)) + sum(v * v / t[2] ** 2 for v, t in zip(mv, ISO)))
    c = sum((d - s * m) @ Ci @ (d - s * m) for m, d, Ci in zip(ms, ds, CINV)) + sum(((t[1] - s * v) / t[2]) ** 2 for v, t in zip(mv, ISO))
    return c + (sn_chi2_cfg689(SN["PP"], DMf) if use_sn else 0.0)


r1 = minimize(lambda q: chi681(q[0], False), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
r2 = minimize(lambda q: chi681(q[0], True), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
check("S0-2_CFG681_BAO_SN", abs(r1.fun - 10.5515) <= 0.02 and abs(r1.x[0] - 0.2970) <= 5e-4 and abs(r2.fun - 1400.143) <= 0.02
      and abs(r2.x[0] - 0.3039) <= 5e-4,
      f"BAO chi2 {r1.fun:.4f} Om {r1.x[0]:.5f}; BAO+PP chi2 {r2.fun:.3f} Om {r2.x[0]:.5f}", "(10.5515, 0.2970), (1400.143, 0.3039)")
# S0-3: DESI DR2 DES-SN5YR w0wa chain means (burn-in 0.3, getdist default) vs its margestats
CH = os.path.join(EXT, "desi_dr2_chains")


def chain_wwa(ds):
    W, w, wa = [], [], []
    for i in range(1, 5):
        d = np.loadtxt(os.path.join(CH, ds, f"chain.{i}.txt"))
        d = d[int(0.3 * len(d)):]
        W.append(d[:, 0]); w.append(d[:, 8]); wa.append(d[:, 9])
    W, w, wa = map(np.concatenate, (W, w, wa))
    return float((W * w).sum() / W.sum()), float((W * wa).sum() / W.sum()), float(np.sqrt((W * (w - (W * w).sum() / W.sum()) ** 2).sum() / W.sum())), \
        float(np.sqrt((W * (wa - (W * wa).sum() / W.sum()) ** 2).sum() / W.sum()))


DESI = {ds: chain_wwa(ds) for ds in ("desy5", "pantheonplus", "union3")}
check("S0-3_DESI_chain_w0wa", abs(DESI["desy5"][0] + 0.752) <= 0.005 and abs(DESI["desy5"][1] + 0.86) <= 0.03,
      f"desy5 w {DESI['desy5'][0]:.4f} wa {DESI['desy5'][1]:.4f}", "margestats -0.752, -0.86")
RES["S0"] = {"chi2_C7": c_l, "sigma8_C7": o_l["sigma8"], "rd_C7_start": o_l["rd"], "CFG681": [r1.fun, r1.x[0], r2.fun, r2.x[0]],
             "DESI_chains_w_wa_sd": DESI}
P(f"  DESI chains (w, wa, sd): {DESI}")
if not all(ok for n, ok, mu in CHK):
    P("STEP 0 FAILED: lane stops UNDECIDED")
    RES["verdict"] = "UNDECIDED (Step 0 failed)"
    save()
    sys.exit(1)

# ================================================================== machinery checks
P("\n== machinery checks")
# K2: exchange code at xi = 0 equals vanilla (the bug switch is inert at xi = 0)
o_off = run("K2_x54_xi0", X54B, base(P0), xi=0.0, pk=True)
mk = np.arange(len(o_l["tt"])) >= 2
dmax = max(float(np.max(np.abs(o_off[k][mk] / o_l[k][mk] - 1))) for k in ("tt", "ee", "pp"))
check("K2_xi0_equals_vanilla", dmax <= 1e-4 and abs(o_off["sigma8"] / o_l["sigma8"] - 1) <= 1e-5,
      f"max |dC/C| {dmax:.2e}; sigma8 {o_off['sigma8']:.6f} vs {o_l['sigma8']:.6f}", "<= 1e-4; <= 1e-5")

# K1: background identity and sign
k1 = {}
okk1 = True
for model, xi in (("C", 0.01), ("D", 0.3)):
    o = run(f"K1_{model}", X54B, base(P0), xi=xi, model=model, cmb=False)
    b = o["bg"]
    sel = b["z"] <= 1e4
    lna = -np.log(1 + b["z"][sel])
    rc, rl = b["rc"][sel], b["rl"][sel]
    N = rc * np.exp(3 * lna)
    dlnN = np.gradient(np.log(N), lna)
    want = xi if model == "C" else xi * rl / rc                 # (Q/H)/rho_c with the frozen sign
    e1 = float(np.max(np.abs(dlnN - want)) / np.max(np.abs(want)))
    dsum = np.gradient(rc + rl, lna)
    e2 = float(np.max(np.abs(dsum + 3 * rc) / (3 * rc)))
    k1[model] = {"xi": xi, "rel_err_rate": e1, "rel_err_total": e2}
    okk1 &= e1 <= 2e-3 and e2 <= 2e-3
check("K1_background_identity_sign", okk1, k1, "<= 2e-3 each", must=not MUT)

# K3: perturbation growth z 10 -> 0 vs an independent ODE (frozen section 8)
KMPC = 0.0338                                                 # 0.05 h/Mpc at the C7 start h 0.6755 (k in 1/Mpc, fixed)
k3 = {}


def k3_run(xi):
    o = run(f"K3_{xi}", X54B, base(P0), xi=xi, model="C", cmb=False, keep=True,
            extra={"output": "mTk", "k_output_values": KMPC, "z_pk": 0})
    d = np.loadtxt(o["root"] + "perturbations_k0_s.dat")
    hdr = [ln for ln in open(o["root"] + "perturbations_k0_s.dat") if ln.startswith("#")][-1]
    cols = {re.sub(r"^\d+:", "", c.strip()).split()[0]: i for i, c in enumerate(re.split(r"\s{2,}", hdr.lstrip("#").strip()))}
    for f in os.listdir(RUNS):
        if f.startswith(f"K3_{xi}_"):
            os.remove(os.path.join(RUNS, f))
    return o, d, cols


def k3_eval(xi):
    o, d, cols = k3_run(xi)
    tau, a = d[:, cols["tau"]], d[:, cols["a"]]
    dc, db, tb = d[:, cols["delta_cdm"]], d[:, cols["delta_b"]], d[:, cols["theta_b"]]
    b = o["bg"]
    # CLASS prints the k-output file in Newtonian gauge (perturbations.c L8429-8450: delta -= 3 aH alpha, theta += k^2 alpha,
    # theta_cdm = k^2 alpha since theta_cdm(sync) = 0); undo that exactly to recover the synchronous-gauge variables
    aH_rows = a * np.interp(np.log(a), (-np.log(1 + b["z"]))[::-1], b["H"][::-1])
    alpha_k2 = d[:, cols["theta_cdm"]]
    dc = dc + 3 * aH_rows * alpha_k2 / KMPC ** 2
    db = db + 3 * aH_rows * alpha_k2 / KMPC ** 2
    tb = tb - alpha_k2
    lnab = -np.log(1 + b["z"])[::-1]                           # increasing ln a
    # background (CLASS's own table) as functions of ln a: H [1/Mpc], density fractions
    Hc = CubicSpline(lnab, b["H"][::-1])
    fc = CubicSpline(lnab, (b["rc"] / b["rtot"])[::-1])
    fb = CubicSpline(lnab, (b["rb"] / b["rtot"])[::-1])
    # initial values at z = 10 from CLASS; h'/2 from the (unpatched) baryon equation: delta_b' = -theta_b - h'/2
    lna_d, iu = np.unique(np.log(a), return_index=True)
    dc, db, tb = dc[iu], db[iu], tb[iu]
    x0 = math.log(1 / 11.0)
    sb = CubicSpline(lna_d, db)
    i0 = {"dc": float(CubicSpline(lna_d, dc)(x0)), "db": float(sb(x0)), "tb": float(CubicSpline(lna_d, tb)(x0))}
    aH0 = math.exp(x0) * float(Hc(x0))
    hp0 = 2 * (-float(sb(x0, 1)) * aH0 - i0["tb"])             # conformal derivative = aH d/dlna

    def rhs(x, y, r):
        dcx, dbx, tbx, hp = y
        aH = math.exp(x) * float(Hc(x))
        ddc = (-hp / 2 - r * aH * dcx) / aH
        ddb = (-hp / 2 - tbx) / aH
        dtb = -tbx
        # h'' + aH h' = -3 (aH)^2 (f_c delta_c + f_b delta_b); in ln a: d h'/dlna = h''/aH
        dhp = (-aH * hp - 3 * aH ** 2 * (float(fc(x)) * dcx + float(fb(x)) * dbx)) / aH
        return [ddc, ddb, dtb, dhp]

    y0 = [i0["dc"], i0["db"], i0["tb"], hp0]
    ode = solve_ivp(rhs, (x0, 0.0), y0, args=(xi,), rtol=1e-9, atol=1e-14).y[0, -1] / i0["dc"]
    ode_nodil = solve_ivp(rhs, (x0, 0.0), y0, args=(0.0,), rtol=1e-9, atol=1e-14).y[0, -1] / i0["dc"]
    cl_ = float(CubicSpline(lna_d, dc)(0.0)) / i0["dc"]
    return ode, cl_, ode_nodil


ode_x, cls_x, ode_x_nodil = k3_eval(0.05)
ode_0, cls_0, _ = k3_eval(0.0)
eff = abs(ode_x / ode_x_nodil - 1)                              # the dilution term's own effect (same background)
err = abs(cls_x / ode_x - 1)
k3 = {"xi": 0.05, "k_1_over_Mpc": KMPC, "class_growth": cls_x, "ode_growth": ode_x, "rel_err": err,
      "class_growth_xi0": cls_0, "ode_growth_xi0": ode_0, "rel_err_xi0": abs(cls_0 / ode_0 - 1), "dilution_effect": eff,
      "total_effect_vs_xi0": abs(cls_x / cls_0 - 1)}
check("K3_perturbation_growth", err <= 3e-3 and eff >= 0.01, k3, "rel err <= 3e-3 and effect >= 1 %", must=not MUT)
RES["K"] = {"K1": k1, "K2": dmax, "K3": k3}

if MUT:
    good = all(ok == mu for n, ok, mu in CHK)
    RES["verdict"] = "MUTATE run: checks only"
    save()
    P(f"\nX54 MUTATE COMPLETE: {sum(ok == mu for n, ok, mu in CHK)}/{len(CHK)} checks have their required outcome; "
      f"failing as required: {[n for n, ok, mu in CHK if not mu and not ok]}")
    sys.exit(0 if good else 1)

# K4: CLASS distances vs this lane's analytic background (at a model-C point)
o4 = run("K4_C", X54B, base(P0), xi=0.008, model="C", cmb=False)
b = o4["bg"]
H0c = float(o4["Hf"](0.0)) / C_KMS
i0 = 0
Om = {k: float(b[k][i0]) / H0c ** 2 for k in ("rc", "rl", "rb", "rg", "rur")}
zz = np.linspace(0, 2.5, 25001)
aa = 1 / (1 + zz)
rc_, rl_ = rho_cl("C", 0.008, Om["rc"], Om["rl"], aa)
Han = H0c * np.sqrt(rc_ + rl_ + Om["rb"] * aa ** -3 + (Om["rg"] + Om["rur"]) * aa ** -4)
DMan = np.r_[0, np.cumsum(0.5 * (1 / Han[1:] + 1 / Han[:-1]) * np.diff(zz))]
zt = np.array([0.1, 0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33])
e4 = float(max(np.max(np.abs(o4["DMf"](zt) / np.interp(zt, zz, DMan) - 1)),
               np.max(np.abs(o4["Hf"](zt) / C_KMS / np.interp(zt, zz, Han) - 1))))
check("K4_distances_vs_analytic", e4 <= 1e-4, f"max rel dev D_M, H at BAO z: {e4:.2e}", "<= 1e-4")
if not all(ok for n, ok, mu in CHK):
    P("A machinery check FAILED: lane stops UNDECIDED")
    RES["verdict"] = "UNDECIDED (check failed)"
    save()
    sys.exit(1)

# ================================================================== profiles
STEP = np.array([1e-4, 1e-3, 2e-4, 0.01, 0.004, 0.004])


def fit(model, xi, sn, p_start, A_start, J_start=None):
    n0 = NRUN[0]
    nm = f"{model}_{sn}_{xi:+.4f}"
    p, A = np.array(p_start, float), float(A_start)
    o = run(nm + "_s", X54B, base(p), xi=xi, model=model)
    if o is None:
        return {"status": "CLASS_FAIL", "msg": FAILMSG.get(nm + "_s")}
    r = resid(o, A, p[5], sn)
    nr = len(r)
    def fresh_J(p, A, o, r):
        J = np.zeros((nr, 7))
        for kx in range(6):
            pp = p.copy(); pp[kx] += STEP[kx]
            ok_ = run(nm + "_j", X54B, base(pp), xi=xi, model=model)
            sgn = 1
            if ok_ is None:
                pp[kx] -= 2 * STEP[kx]; sgn = -1
                ok_ = run(nm + "_j", X54B, base(pp), xi=xi, model=model)
                if ok_ is None:
                    return None
            J[:, kx] = sgn * (resid(ok_, A, pp[5], sn) - r) / STEP[kx]
        J[:613, 6] = np.linalg.solve(NS["Lc"], 2 * binned(o) / A ** 3)
        J[613, 6] = 1 / 0.0025
        return J

    fresh = not (J_start is not None and J_start.shape[0] == nr)
    J = fresh_J(p, A, o, r) if fresh else J_start.copy()
    if J is None:
        return {"status": "CLASS_FAIL", "msg": FAILMSG.get(nm + "_j")}
    hist, stop = [], False
    o_cur = o
    for it in range(10):
        cs = r @ r
        d = -np.linalg.lstsq(J, r, rcond=None)[0]
        lam = 1.0
        while True:
            pn, An = p + lam * d[:6], A + lam * d[6]
            on = run(nm + "_l", X54B, base(pn), xi=xi, model=model)
            rn = None if on is None else resid(on, An, pn[5], sn)
            cn = np.inf if rn is None else rn @ rn
            if cn <= cs or lam < 1 / 16:
                break
            lam /= 2
        if cn > cs:
            if not fresh:                                       # a reused (Broyden) Jacobian failed: rebuild it once
                fresh = True
                J = fresh_J(p, A, o_cur, r)
                if J is None:
                    return {"status": "CLASS_FAIL", "msg": FAILMSG.get(nm + "_j")}
                hist.append({"it": it + 1, "steered": float(cs), "fall": 0.0, "step": lam, "jacobian": "rebuilt"})
                continue
            hist.append({"it": it + 1, "steered": float(cs), "fall": 0.0, "step": lam})
            stop = True
            break
        dx = np.concatenate((pn - p, [An - A]))
        J = J + np.outer(rn - r - J @ dx, dx) / (dx @ dx)
        p, A, r, o_cur = pn, An, rn, on
        hist.append({"it": it + 1, "steered": float(cn), "fall": float(cs - cn), "step": lam})
        if cs - cn < 0.05:
            if not fresh:                                       # small fall on a reused Jacobian: confirm with a fresh one
                fresh = True
                J = fresh_J(p, A, o_cur, r)
                if J is None:
                    return {"status": "CLASS_FAIL", "msg": FAILMSG.get(nm + "_j")}
                continue
            stop = True
            break
    of = run(nm + "_f", X54B, base(p), xi=xi, model=model, pk=True)
    c = chi2_all(of, A, sn)
    h = of["h"]
    om = (p[0] + p[1]) / h ** 2
    oc, ol = float(of["bg"]["rc"][0]) / (of["Hf"](0.0) / C_KMS) ** 2, float(of["bg"]["rl"][0]) / (of["Hf"](0.0) / C_KMS) ** 2
    rec = {"xi": xi, "params": p.tolist(), "A": A, "chi2": c, "h": h, "H0": 100 * h, "Omega_m": om, "Omega_c": oc,
           "Omega_DE": ol, "sigma8": of["sigma8"], "S8": of["sigma8"] * math.sqrt(om / 0.3), "rd": of["rd"],
           "gn": hist, "converged": bool(stop), "runs": NRUN[0] - n0,
           "b_D": (xi * ol / ((3 - xi) * oc)) if model == "D" else None}
    return rec, J


def profile(model, sn, grid0, ext_step, ext_max, seed=None):
    recs = {}
    Js = {}

    def do(xi, nb):
        if nb is None:
            ps, As, Js_ = (P0, A0, None) if seed is None else (seed["params"], seed["A"], None)
        else:
            ps, As, Js_ = recs[nb]["params"], recs[nb]["A"], Js.get(nb)
        out = fit(model, xi, sn, ps, As, Js_)
        if isinstance(out, dict):
            recs[xi] = {**out, "xi": xi}
            P(f"  {model} {sn} xi={xi:+.4f}: CLASS FAIL {out.get('msg')}")
            return
        rec, J = out
        recs[xi] = rec
        Js[xi] = J
        P(f"  {model} {sn} xi={xi:+.4f}: chi2 {rec['chi2']['total']:.3f} (cmb {rec['chi2']['cmb']:.2f}, bao {rec['chi2']['bao']:.2f}, "
          f"sn {rec['chi2']['sn']:.2f}); H0 {rec['H0']:.2f}, omega_c {rec['params'][1]:.5f}, Om {rec['Omega_m']:.4f}, S8 {rec['S8']:.4f}; "
          f"conv {rec['converged']}, runs {rec['runs']}")
        RES.setdefault("profiles", {}).setdefault(f"{model}_{sn}", {})[f"{xi:+.4f}"] = rec
        save()

    grid = sorted(grid0)
    do(0.0, None)
    pos = [x for x in grid if x > 0]
    neg = sorted([x for x in grid if x < 0], reverse=True)
    for side in (pos, neg):
        prev = 0.0
        for x in side:
            do(x, prev if "chi2" in recs.get(prev, {}) else 0.0)
            prev = x
        # extension rule: double outward while delta chi2 < 3.84 at the edge
        while True:
            ok = {x: r for x, r in recs.items() if "chi2" in r}
            if not ok:
                break
            cmin = min(r["chi2"]["total"] for r in ok.values())
            edge = side[-1] if side else 0.0
            if "chi2" not in recs.get(edge, {}) or recs[edge]["chi2"]["total"] - cmin >= 3.84:
                break
            nx = edge * 2 if edge != 0 else ext_step
            if abs(nx) > ext_max + 1e-12:
                break
            do(nx, edge)
            side.append(nx)
    return recs


def analyse(model, sn, recs):
    ok = {x: r for x, r in recs.items() if "chi2" in r and r["converged"]}   # frozen section 3: converged points only
    xs = np.array(sorted(ok))
    cs = np.array([ok[x]["chi2"]["total"] for x in xs])
    spl = CubicSpline(xs, cs)
    fine = np.linspace(xs[0], xs[-1], 20001)
    cf = spl(fine)
    i = int(np.argmin(cf))
    xhat, cmin = float(fine[i]), float(cf[i])
    d0 = float(ok[0.0]["chi2"]["total"] - cmin)
    inside = cf - cmin <= 3.84
    lo, hi = float(fine[inside][0]), float(fine[inside][-1])
    closed = bool(cf[0] - cmin > 3.84 and cf[-1] - cmin > 3.84)
    # points needed: every grid point inside the interval converged and none failed
    bad_in = [x for x, r in recs.items() if lo - 1e-12 <= x <= hi + 1e-12 and ("chi2" not in r or not r["converged"])]
    oc, ol = ok[0.0]["Omega_c"], ok[0.0]["Omega_DE"]

    def at(xi):                                                # interpolate the refit densities to xi
        occ = float(np.interp(xi, xs, [ok[x]["Omega_c"] for x in xs]))
        oll = float(np.interp(xi, xs, [ok[x]["Omega_DE"] for x in xs]))
        return occ, oll

    rep = {}
    for lab, xi in (("best", xhat), ("lo95", lo), ("hi95", hi), ("xi0", 0.0)):
        occ, oll = at(xi)
        sx = float(sqrtX(model, xi, occ, oll, 2.33))
        rep[lab] = {"xi": xi, "F_made": F_made(model, xi, occ, oll), "sqrtX_2.33": sx,
                    "sqrtX_z": {str(z): float(sqrtX(model, xi, occ, oll, z)) for z in (0.5, 1.0, 1.5, 2.33, 5.0)},
                    "a0_2.33": {f: v * sx for f, v in FOOT.items()},
                    "S8": float(np.interp(xi, xs, [ok[x]["S8"] for x in xs])),
                    "sigma8": float(np.interp(xi, xs, [ok[x]["sigma8"] for x in xs])),
                    "H0": float(np.interp(xi, xs, [ok[x]["H0"] for x in xs])),
                    "Omega_m": float(np.interp(xi, xs, [ok[x]["Omega_m"] for x in xs])),
                    "omega_c": float(np.interp(xi, xs, [ok[x]["params"][1] for x in xs])),
                    "w": weff(model, xi, occ, oll, float(np.interp(xi, xs, [ok[x]["Omega_m"] for x in xs])) - occ)}
    fm = [abs(rep["lo95"]["F_made"]), abs(rep["hi95"]["F_made"])]
    if d0 >= 4.0:
        cls = f"EXCHANGE PREFERRED ({'DE -> cold' if xhat > 0 else 'cold -> DE'})"
    elif not closed or bad_in or not (lo <= 0 <= hi):
        cls = "UNDECIDED"
    elif max(fm) >= 0.03:
        cls = f"EXCHANGE ALLOWED (bound xi in [{lo:+.4f}, {hi:+.4f}])"
    else:
        cls = f"EXCHANGE EXCLUDED BEYOND [{lo:+.4f}, {hi:+.4f}]"
    band = BAND689[sn]
    sb = rep["best"]["sqrtX_2.33"]
    sec = "CONSISTENT" if (band[0] <= sb <= band[1] and sb > 0) else "TENSION"
    s_lo, s_hi = sorted((rep["lo95"]["sqrtX_2.33"], rep["hi95"]["sqrtX_2.33"]))
    out = {"grid": xs.tolist(), "chi2": cs.tolist(), "xi_hat": xhat, "chi2_min": cmin, "dchi2_xi0": d0, "int95": [lo, hi],
           "closed": closed, "bad_inside": bad_in, "class": cls, "report": rep, "secondary": sec, "band_flat_theta": band,
           "band_curvature_free": BAND689_K[sn], "reaches_0909": bool(s_lo <= 0.909 <= s_hi),
           "sqrtX_range_95": [s_lo, s_hi]}
    P(f"\n  [{model} {sn}] xi_hat {xhat:+.5f}; dchi2(xi=0) {d0:.3f}; 95% [{lo:+.5f}, {hi:+.5f}] (closed {closed}; "
      f"unconverged/failed inside {bad_in}) -> {cls}")
    P(f"    F_made best {rep['best']['F_made']:+.4f}, ends {rep['lo95']['F_made']:+.4f} / {rep['hi95']['F_made']:+.4f} (CFG253 convention 0.03)")
    P(f"    sqrtX(2.33) best {sb:.4f}, 95% range [{s_lo:.4f}, {s_hi:.4f}] vs CFG689 flat+theta* {band} -> {sec}; "
      f"curvature-free {BAND689_K[sn]}; reaches 0.909: {out['reaches_0909']}")
    P(f"    a0(2.33) best: canonical {rep['best']['a0_2.33']['canonical']:.4e}, alt {rep['best']['a0_2.33']['alt']:.4e} m/s^2")
    P(f"    S8 xi=0 {rep['xi0']['S8']:.4f}, best {rep['best']['S8']:.4f}, ends {rep['lo95']['S8']:.4f} / {rep['hi95']['S8']:.4f}")
    P(f"    w_eff best: {rep['best']['w']}")
    return out


BAND689 = {"DES5": (0.68, 1.04), "PP": (0.68, 1.05), "U3": (0.69, 1.07)}      # CFG689 TD5F / TF / TU3F, 68 %
BAND689_K = {"DES5": (0.34, 1.21), "PP": (0.32, 1.21), "U3": (0.42, 1.26)}    # CFG689 D5 / primary / U3


def weff(model, xi, oc, ol, ob):
    """intrinsic w_DE(z), apparent w_app(z) and a CPL fit of the apparent dark energy (frozen section 6)"""
    z = np.linspace(0, 2.5, 501)
    a = 1 / (1 + z)
    rc, rl = rho_cl(model, xi, oc, ol, a)
    q_over_h = xi * rc if model == "C" else xi * rl            # Q/H in H0^2 units
    w_int = -1 + q_over_h / (3 * rl)
    rapp = rc + rl - oc * a ** -3
    lna = np.log(a)
    w_app = -1 - np.gradient(np.log(rapp), lna) / 3
    f = rapp / rapp[0]

    def cpl(q):
        w0, wa = q
        return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z)) - f
    fitq = least_squares(cpl, [-1.0, 0.0]).x
    pick = [0, 100, 200, 400]
    return {"z": [float(z[i]) for i in pick], "w_intrinsic": [float(w_int[i]) for i in pick],
            "w_apparent": [float(w_app[i]) for i in pick], "cpl_w0": float(fitq[0]), "cpl_wa": float(fitq[1])}


P("\n== profiles (graded chi2 = plik + lowTT + lowEE + Aprior + BAO + SN)")
GRID = {"C": [-0.012, -0.008, -0.004, -0.002, 0.0, 0.002, 0.004, 0.008, 0.012],
        "D": [-0.6, -0.4, -0.2, -0.1, 0.0, 0.1, 0.2, 0.4, 0.6]}
INNER = {"C": [-0.004, -0.002, 0.0, 0.002, 0.004], "D": [-0.2, -0.1, 0.0, 0.1, 0.2]}
EXTX = {"C": (0.012, 0.1), "D": (0.6, 1.5)}
AN = {}
REAN = os.environ.get("X54_REANALYSE", "")                       # path to a previous results JSON: reuse its refits
if REAN:
    PREV = json.load(open(REAN))["profiles"]
    P(f"REANALYSE: refits reused from {os.path.basename(REAN)} (no new profile fits)")


def load_prev(key):
    return {float(k): ({**v, "xi": float(k)} if "chi2" in v else v) for k, v in PREV[key].items()}


ALLRECS = {}
for model in ("C", "D"):
    recs = load_prev(f"{model}_DES5") if REAN else profile(model, "DES5", GRID[model], *EXTX[model])
    ALLRECS[f"{model}_DES5"] = recs
    AN[f"{model}_DES5"] = analyse(model, "DES5", recs)
    RES["analysis"] = AN
    save()
    seed = recs[0.0]
    for sn in ("PP", "U3"):
        recs2 = load_prev(f"{model}_{sn}") if REAN else profile(model, sn, INNER[model], EXTX[model][0] / 3, EXTX[model][1], seed=seed)
        ALLRECS[f"{model}_{sn}"] = recs2
        AN[f"{model}_{sn}"] = analyse(model, sn, recs2)
        RES["analysis"] = AN
        save()
RES["profiles"] = {k: {f"{x:+.4f}": r for x, r in v.items()} for k, v in ALLRECS.items()}
save()

# ------------------------------------------------------------------ POST-HOC supplement S1 (reported only; no frozen class)
# M-D's frozen grid has no converged point above xi = 0.2 (0.4: CLASS shooting failed; 0.6: started from xi = 0, not
# converged), so its upper 95 % end is not closed. S1 adds xi = 0.3 and 0.4 started from the xi = 0.2 refit.
if os.environ.get("X54_SUPP", "0") == "1":
    P("\n== POST-HOC S1 (reported only): M-D upper side, xi = 0.3, 0.4 seeded from the xi = 0.2 refit")
    S1 = {}
    for sn in ("DES5", "PP", "U3"):
        recs = dict(ALLRECS[f"D_{sn}"])
        prev = recs[0.2]
        Jp = None
        for xi in (0.3, 0.4):
            out = fit("D", xi, sn, prev["params"], prev["A"], Jp)
            if isinstance(out, dict):
                P(f"  S1 D {sn} xi={xi:+.4f}: CLASS FAIL {out.get('msg')}")
                recs[xi] = {**out, "xi": xi}
                break
            rec, Jp = out
            recs[xi] = rec
            prev = rec
            P(f"  S1 D {sn} xi={xi:+.4f}: chi2 {rec['chi2']['total']:.3f} (cmb {rec['chi2']['cmb']:.2f}, bao {rec['chi2']['bao']:.2f}, "
              f"sn {rec['chi2']['sn']:.2f}); H0 {rec['H0']:.2f}, omega_c {rec['params'][1]:.5f}, S8 {rec['S8']:.4f}; conv {rec['converged']}")
        recs = {x: r for x, r in recs.items() if x != 0.6}           # the unconverged frozen 0.6 point is dropped
        S1[f"D_{sn}"] = {"points": {f"{x:+.4f}": r for x, r in recs.items()}, "analysis": analyse("D", sn, recs)}
        RES["S1_posthoc"] = S1
        save()

# ================================================================== verdict
prim = AN["C_DES5"]
RES["verdict"] = {"primary_M-C_DES5": prim["class"], "secondary_a0": prim["secondary"],
                  "all": {k: (v["class"], v["secondary"]) for k, v in AN.items()}}
P("\n== VERDICT (primary M-C, DES-SN5YR): " + prim["class"] + f"; a0 secondary: {prim['secondary']}")
for k, v in AN.items():
    P(f"  {k}: {v['class']}; dchi2(xi=0) {v['dchi2_xi0']:.3f}; xi_hat {v['xi_hat']:+.5f}; 95% {v['int95']}; a0: {v['secondary']}")
P(f"checks: {sum(ok == mu for n, ok, mu in CHK)}/{len(CHK)} have their required outcome; CLASS runs {NRUN[0]}")
save()
P(f"done in {time.time() - T0:.0f} s")
