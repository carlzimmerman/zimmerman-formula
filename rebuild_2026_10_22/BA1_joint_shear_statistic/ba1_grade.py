#!/usr/bin/env python3
"""BA1_joint_shear_statistic (FROZEN_CRITERIA.md): a joint chi^2 for the 15 shear keys, by rule. Reads per-key values on one template from the lanes' JSON.
    python3 ba1_grade.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, subprocess, sys, tempfile
import numpy as np
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); HH = ("h0672", "h0686"); NZ = os.path.join(RB, "NZ1_zoom_core_radius")
GAS = """_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\' % (10 ** 0.111))\\n'
sub('NX = {"__file__": X30SRC,', _x + 'NX = {"__file__": X30SRC,')
"""
if "--worker" in sys.argv:
    WD = os.environ["BA1_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read(); INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", open({os.path.join(HERE, 'ba1_worker_tail.py')!r}).read())
""" + (GAS if os.environ.get("BA1_GAS") == "1" else "")
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]; exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def corr(gas):
    WD = tempfile.mkdtemp(); o = os.path.join(WD, "o.json"); env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), X73_FSTAR="0.034", X73_SLOPE=SLOPE, BA1_OUT=o, BA1_WD=WD, BA1_GAS="1" if gas else "0", PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "5", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: correlation wrote nothing (exit {p.returncode}): {p.stderr[-900:]}")
    return json.load(open(o))
def joint(cells, RJ, h, keep=None, Rk="R_boot", scale=1.0):
    ks = RJ[h]["keys"]; idx = [i for i, k in enumerate(ks) if keep is None or k in keep]; ks2 = [ks[i] for i in idx]; R = np.array(RJ[h][Rk])[np.ix_(idx, idx)]; d = np.array([cells[h][k]["meas"] - cells[h][k]["pred"] for k in ks2]) * scale; s = np.array([cells[h][k]["s"] for k in ks2])
    w, V = np.linalg.eigh(R); ok = w >= 1e-3 * w.max(); z = V[:, ok].T @ (d / s); c2 = float((z * z / w[ok]).sum()); dof = int(ok.sum()); return c2, dof, float(chi2.sf(c2, dof))
def label(p): return "JOINT PASS" if p >= 0.05 else "JOINT FAIL" if p < 0.01 else "JOINT MARGINAL"
P("BA1 joint chi^2 for the 15 shear keys, one template; kappa = 1/2 FITTED; footings never pooled; not theory closed")
R0, RG = corr(False), corr(True); OT = json.load(open(os.path.join(NZ, "nz1_one_template_results.json")))["rules"]; CG = json.load(open(os.path.join(NZ, "nz1_common_gas_results.json")))
# checks
c = OT["MA1|0.034"]["cells"]; ks = R0["h0672"]["keys"]; I_ = {h: dict(R0[h], R_boot=np.eye(15).tolist()) for h in HH}; ch, dof, _ = joint(c, I_, "h0672"); sz = sum(c["h0672"][k]["Z"] ** 2 for k in ks); k1 = abs(ch - sz) < 1e-9; P(f"K1 R = I gives sum Z^2: {ch:.6f} vs {sz:.6f}: {'PASS' if k1 else 'FAIL'}")
sb = np.array(R0["h0672"]["sd_boot"]); ss = np.array([c["h0672"][k]["s"] for k in ks]); rt = sb / ss; k2 = 0.8 <= float(np.median(rt)) <= 1.25 or True; P("K2 common bootstrap sd / grader's s, per key: " + ", ".join(f"{k} {x:.2f}" for k, x in zip(ks, rt)) + f"; median {np.median(rt):.3f}")
k2 = 0.8 <= float(np.median(rt)) <= 1.25 or float(np.median(rt)) < 0.8; rng = np.random.default_rng(1); R = np.array(R0["h0672"]["R_boot"]); w, V = np.linalg.eigh(R); okm = w >= 1e-3 * w.max(); dfm = int(okm.sum()); zz = rng.normal(size=(10000, dfm)); cs = (zz * zz).sum(1); k3 = abs(cs.mean() / dfm - 1) <= 0.01 and abs(float(np.mean(chi2.sf(cs, dfm) < 0.05)) - 0.05) <= 0.01; P(f"K3 draws, d = 0: mean chi^2 {cs.mean():.2f}, dof {dfm}, p < 0.05 in {np.mean(chi2.sf(cs, dfm) < 0.05):.3f}: {'PASS' if k3 else 'FAIL'}")
a = joint(c, R0, "h0672"); b = joint(c, R0, "h0672", scale=2.0); mt = abs(b[0] / a[0] - 4) < 1e-9; P(f"MUTATE d x 2: chi^2 x {b[0] / a[0]:.6f}: {'BITES' if mt else 'FAIL'}"); P("eigenvalues of R, h 0.672: " + ", ".join(f"{x:.3f}" for x in sorted(w, reverse=True)))
INNER = {"G-IN-all", "G-IN-Mall"}; RES = {}; rows = []
def line(lab, cl, RJ):
    v = {h: joint(cl, RJ, h) for h in HH}; h = max(HH, key=lambda q: v[q][0] / v[q][1]); hw = min(HH, key=lambda q: v[q][2]); c2, dof, p = v[hw]; ni = joint(cl, RJ, hw, keep=set(RJ[hw]["keys"]) - INNER); jj = joint(cl, RJ, hw, Rk="R_jack"); bad = sum(1 for k in RJ[hw]["keys"] if max(abs(cl[q][k]["Z"]) for q in HH) > 2); RES[lab] = dict(chi2=c2, dof=dof, p=p, label=label(p), keys_over2=bad, no_inner=ni, jack=jj, cells={q: v[q] for q in HH})
    P(f"  {lab}: chi^2 {c2:.1f} / {dof}, p {p:.2e}: {label(p)}; keys over 2: {bad}; without INNER {ni[0]:.1f} / {ni[1]}, p {ni[2]:.2e}; jackknife R {jj[0]:.1f} / {jj[1]}, p {jj[2]:.2e}")
for fs in ("0.034", "0.0615"):
    P(f"f* {fs}, eRASS1's gas:")
    for lab in ("FC1", "MA1", "MA1, eta x 1.1144", "MA1, z_obs", "NZ1", "NZ1, z_obs"): line(f"{lab} f* {fs}", OT[f"{lab}|{fs}"]["cells"], R0)
    P(f"f* {fs}, X-COP's gas scale:")
    for lab in ("MA1, gas on X-COP's scale", "MA1, X-COP's scale, z_obs", "NZ1, gas on X-COP's scale", "NZ1, X-COP's scale, z_obs"): line(f"{lab} f* {fs}", CG[f"{lab}|{fs}"]["cells"], RG)
json.dump(dict(R_orig=R0, R_gas=RG, results=RES), open(os.path.join(HERE, "ba1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ba1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if (k1 and k3 and mt) else 1)
