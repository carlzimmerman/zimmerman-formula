#!/usr/bin/env python3
"""UX2 P2b and the row-11 benchmark BAO/SN evaluation. Frozen: FROZEN_CRITERIA.md. Vanilla CLASS with a fluid x as the dust-like term.
Modes: scan | bench. Per-cell JSON checkpoints: kill and rerun resumes. UX2_MUTATE=1: plik sign flip, separate outputs.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I ux2_scan.py scan
kappa = 1/2 FITTED; cold sector stays retired; not theory closed."""
import json, math, os, re, subprocess, sys
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.interpolate import CubicSpline, InterpolatedUnivariateSpline
from scipy.io import FortranFile
from scipy.stats import chi2 as CHI2
MUT = os.environ.get("UX2_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
VAN = os.path.join(EXT, "ux2_class_build", "class_noguard", "class"); AEST = os.path.join(EXT, "class_aest_build_2026_10_22", "class_aest", "class")
WORK = os.path.join(EXT, "ux2_work" + TAG); CELLS = os.path.join(HERE, "cells" + TAG); os.makedirs(WORK, exist_ok=True); os.makedirs(CELLS, exist_ok=True)
C_KMS = 299792.458; TCMB = 2.7255; OMCDM = 1e-8
src = open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb.py")).read()
blk = src[src.index("# ---------------------------------------------------------------- likelihoods"):src.index("# ---------------------------------------------------------------- CLASS emulation")]
L = {"np": np, "math": math, "os": os, "EXT": EXT, "FortranFile": FortranFile, "InterpolatedUnivariateSpline": InterpolatedUnivariateSpline}
exec(compile(blk, "c2b[lik]", "exec"), L)
if MUT: L["Xd"] = -L["Xd"]
src = open(os.path.join(HERE, "..", "X54_cold_de_exchange", "x54_cold_de_exchange.py")).read()
blk = src[src.index("# ------------------------------------------------------------------ BAO (DESI DR2"):src.index("# ------------------------------------------------------------------ CLASS runner")].replace('("DES5", "PP", "U3")', '("DES5",)')
B = {"np": np, "os": os, "EXT": EXT, "C_KMS": C_KMS, "P": lambda *a: None}; exec(compile(blk, "x54[bao,sn]", "exec"), B)
C2R = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb_results.json")))["P5"]; TAU, ST = C2R["tau_hat"], C2R["sig_tau"]
C7 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")))
S0 = C7["fits"]["LCDM"]["params"]
P0 = np.array([S0["omega_b"], S0["omega_dm(FITTED)"], C7["fits"]["LCDM"]["H0"] / 100, S0["ln10^10A_s"], S0["n_s"], S0["tau"]]); A0_ = C7["fits"]["LCDM"]["A_planck"]
STEP = np.array([1e-4, 1e-3, 2e-3, 0.01, 0.004, 0.004]); NAMES = ["omega_b", "omega_x", "h", "lnA", "n_s", "tau"]

def run(name, d, binary=VAN):
    d = dict(d, T_cmb=TCMB, write_parameters="no", input_verbose=1, background_verbose=2, thermodynamics_verbose=1, overwrite_root="yes", write_background="yes",
             output="tCl,pCl,lCl", lensing="yes", l_max_scalars=2508)
    root = os.path.join(WORK, name + "_"); d["root"] = root
    with open(root + ".ini", "w") as fh:
        for k, v in d.items(): fh.write(f"{k} = {v}\n")
    pr = subprocess.run(["nice", "-n", "15", binary, root + ".ini"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    if pr.returncode != 0: return {"err": (pr.stdout + pr.stderr).strip()[-300:]}
    cl = np.loadtxt(root + "_cl_lensed.dat"); Lm = int(cl[-1, 0]); f = (TCMB * 1e6) ** 2; o = {}
    for k, c in (("tt", 1), ("ee", 2), ("te", 3)):
        a = np.zeros(Lm + 1); a[cl[:, 0].astype(int)] = cl[:, c] * f; o[k] = a
    bg = np.loadtxt(root + "_background.dat"); hdr = [l for l in open(root + "_background.dat") if l.startswith("#")][-1]
    cols = {re.sub(r"^\d+:", "", c.strip()): i for i, c in enumerate(re.split(r"\s{2,}", hdr.lstrip("#").strip()))}
    z = bg[:, cols["z"]][::-1]; m = z <= 6
    o["DMf"] = CubicSpline(z[m], bg[:, cols["comov. dist."]][::-1][m]); o["Hf"] = CubicSpline(z[m], bg[:, cols["H [1/Mpc]"]][::-1][m] * C_KMS)
    mm = re.search(r"baryon drag stops at z = [0-9.eE+-]+\s+corresponding to conformal time = [0-9.eE+-]+ Mpc\s+with comoving sound horizon rs = ([0-9.eE+-]+) Mpc", pr.stdout)
    o["rd"] = float(mm.group(1)) if mm else float("nan")
    for fn in os.listdir(WORK):
        if fn.startswith(name + "_"): os.remove(os.path.join(WORK, fn))
    return o

def params(p, c):
    wb, wx, h, lnA, ns, tau = p; wx = max(wx, 5e-4) if c.get("fix") is None else c["fix"]
    q = {"omega_b": wb, "h": h, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau}
    if c.get("cdm"): q["omega_cdm"] = wx
    else: q.update(omega_cdm=OMCDM, Omega_fld=wx / h ** 2, w0_fld=c["w"], wa_fld=0.0, cs2_fld=c["cs2"], use_ppf="no")
    return q

def resid(o, A, tau):
    Tb = L["binned"](o["tt"], o["te"], o["ee"]); return np.concatenate((np.linalg.solve(L["Lc"], L["Xd"] - Tb / A ** 2), [(A - 1) / 0.0025, (tau - TAU) / ST]))

def parts(o, A):
    Tb = L["binned"](o["tt"], o["te"], o["ee"]); out = dict(plik=float(L["chi2_plik"](Tb, A)), Aprior=((A - 1) / 0.0025) ** 2, lowTT=float(L["chi2_lowTT"](o["tt"], A)), lowEE=float(L["chi2_lowEE"](o["ee"], A)))
    out["bao"] = float(np.sum(B["bao_resid"](o["DMf"], o["Hf"], o["rd"]) ** 2)); s = B["SN"]["DES5"]; out["sn"] = float(np.sum(B["sn_resid"](s, o["DMf"]) ** 2)); out["n_sn"] = int(s["n"])
    out["p_plik"] = float(CHI2.sf(out["plik"], 605)); out["p_bao"] = float(CHI2.sf(out["bao"], 13)); out["p_sn"] = float(CHI2.sf(out["sn"], out["n_sn"] - 1)); out["rd"] = o["rd"]; return out

def fit(c, maxit=10):
    free = [0, 2, 3, 4, 5] if c.get("fix") is not None else list(range(6))
    p = P0.copy(); A = A0_; hist = []; lam = 0.0; conv = False
    o = run(c["name"] + "_s", params(p, c))
    if "err" in o: return dict(status="CLASS_FAIL", msg=o["err"])
    r = resid(o, A, p[5]); cs = float(r @ r)
    for it in range(maxit):
        J = np.zeros((len(r), len(free) + 1))
        for j, k in enumerate(free):
            pp = p.copy(); pp[k] += STEP[k]; oo = run(c["name"] + "_j", params(pp, c))
            if "err" in oo: return dict(status="CLASS_FAIL", msg=oo["err"], p=p.tolist())
            J[:, j] = (resid(oo, A, pp[5]) - r) / STEP[k]
        Tb = L["binned"](o["tt"], o["te"], o["ee"]); J[:613, -1] = np.linalg.solve(L["Lc"], 2 * Tb / A ** 3); J[613, -1] = 1 / 0.0025
        d = -np.linalg.lstsq(J, r, rcond=None)[0]; ok = False
        for s in (1.0, 0.5, 0.25, 0.125, 0.0625):
            pn = p.copy(); pn[free] += s * d[:-1]; An = A + s * d[-1]
            on = run(c["name"] + "_t", params(pn, c))
            if "err" in on: continue
            rn = resid(on, An, pn[5]); cn = float(rn @ rn)
            if cn < cs: ok = True; break
        if not ok: hist.append((it, cs, 0.0, "no_descent")); conv = True; break
        fall = cs - cn; p, A, o, r, cs = pn, An, on, rn, cn; hist.append((it, cs, fall, s))
        if fall < 0.1: conv = True; break
    out = dict(status="OK", cell=c, params=dict(zip(NAMES, map(float, p))), A=float(A), chi2=parts(o, A), steer=cs, hist=hist, converged=conv)
    if c.get("fix") is not None: out["params"]["omega_x"] = c["fix"]
    return out

GRID = [dict(name="CDMref", cdm=True)] + [dict(name=f"w{w:+g}", w=w, cs2=0.0) for w in (0.0, 1e-3, -1e-3, 3e-3, -3e-3, 1e-2, -1e-2)] + [dict(name=f"cs2{c:g}", w=0.0, cs2=c) for c in (1e-6, 1e-5, 1e-4)] + [dict(name="control_noX", w=0.0, cs2=0.0, fix=5e-4)]
if MUT: GRID = GRID[:2]

def mode_scan():
    for c in GRID:
        fn = os.path.join(CELLS, c["name"] + ".json")
        if os.path.exists(fn): continue
        rec = fit(c); 
        with open(fn + ".tmp", "w") as fh: json.dump(rec, fh, indent=1, sort_keys=True)
        os.replace(fn + ".tmp", fn); print(c["name"], rec.get("status"), rec.get("chi2", {}).get("plik"), rec.get("msg", ""), flush=True)
    # K2: same parameters, fluid against CDM
    r = json.load(open(os.path.join(CELLS, "CDMref.json")))
    if r["status"] == "OK":
        p = np.array([r["params"][k] for k in NAMES]); oc = run("k2c", params(p, dict(cdm=True))); of = run("k2f", params(p, dict(w=0.0, cs2=0.0)))
        k2 = dict(plik_cdm=parts(oc, r["A"])["plik"], plik_fluid=parts(of, r["A"])["plik"]) if "err" not in of else dict(err=of["err"])
        if "plik_cdm" in k2: k2["d"] = abs(k2["plik_cdm"] - k2["plik_fluid"]); k2["pass"] = k2["d"] <= 0.5
        if MUT: k2["pass"] = bool(k2.get("pass")) and r["chi2"]["plik"] < 1e4
        json.dump(k2, open(os.path.join(HERE, f"ux2_k2{TAG}.json"), "w"), indent=1, sort_keys=True); print("K2", k2, flush=True)

def mode_bench():
    out = {}
    for m in ("B-Cosh", "B-Exp", "B-Cosh-g", "B-Exp-g"):
        f = C7["fits"][m]; p = f["params"]; g = C7["models"][m]["aest_g"]
        q = {"omega_b": p["omega_b"], "omega_cdm": OMCDM, "omega_aest": p["omega_dm(FITTED)"] - OMCDM, "100*theta_s": p["100theta_s"], "ln10^{10}A_s": p["ln10^10A_s"], "n_s": p["n_s"], "tau_reio": p["tau"], **C7["models"][m]}
        o = run("b" + m, q, AEST)
        if "err" in o: out[m] = dict(err=o["err"]); print(m, o["err"]); continue
        c = parts(o, f["A_planck"]); c.update(g=g, c7_plik=f["chi2"]["plik"], d_plik=abs(c["plik"] - f["chi2"]["plik"]), H0=f["H0"], omega_x=p["omega_dm(FITTED)"], omega_b=p["omega_b"], bbn_g_line=0.9611, bbn_pass=g > 0.9611); out[m] = c; print(m, c, flush=True)
    json.dump(out, open(os.path.join(HERE, f"ux2_bench{TAG}.json"), "w"), indent=1, sort_keys=True)

if __name__ == "__main__": {"scan": mode_scan, "bench": mode_bench}[sys.argv[1]]()
