#!/usr/bin/env python3
"""EW4 primary CMB (criteria origin 8833a24300, section 4.8): QX15's grader (PR4 CamSpec cut + ACT DR6, qx15_like, read-only) on
CLASS spectra with the cold component replaced by one thermal fermion (m 11.1377 eV, T_ncdm 0.71611, deg 1, omega_cdm ~ 0),
footing background by QX15's background() with od = omega_f fixed. Fit (omega_b, ln A_s, n_s, tau) by Nelder-Mead from QX15's
main best fit, maxfev 120, QX15's brackets. Linear lensing in CLASS (QX15's CAMB default NonLinear_none).
    python3 ew4_cmb.py ka            -> parts/cmb_ka.json   (timing gate + KA-CMB: CLASS cold at QX15 canonical theta vs 3741.08)
    python3 ew4_cmb.py fit <foot>    -> parts/cmb_fit_<foot>.json
    python3 ew4_cmb.py grade         -> ew4_cmb.json / .out
TEST lane; adopts nothing; no-particle rule relaxed for EW4 only. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
Q15 = os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood"); sys.path.insert(0, Q15)
import qx15 as QX
QL = QX.QL
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
OMF = 0.11958060485606123; M_EV = 93.14 * OMF; TNCDM = 0.71611; CHI2_CAL = 3805.80; LMAX = 7000
NOTE = "TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed"

def class_D(foot, ob, lnA, ns, tau, cold_od=None):
    from classy import Class
    od = OMF if cold_od is None else cold_od
    h, _ = QX.background(foot, ob, od)
    p = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LMAX, 'h': h, 'omega_b': ob, 'A_s': math.exp(lnA) * 1e-10,
         'n_s': ns, 'tau_reio': tau, 'N_ur': 3.046, 'T_cmb': QX.TCMB}
    if cold_od is None: p.update({'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': M_EV, 'T_ncdm': TNCDM, 'deg_ncdm': 1})
    else: p.update({'omega_cdm': cold_od})
    M = Class(); M.set(p); M.compute(); cl = M.lensed_cl(LMAX); f = (QX.TCMB * 1e6) ** 2
    extra = {}
    if cold_od is None: extra = dict(omega_ncdm=float(M.Omega0_m() * h * h - ob - 1e-7), h=h)
    l = np.arange(LMAX + 1); arr = np.zeros((LMAX + 1, 4))
    for j, X in ((0, "tt"), (1, "ee"), (3, "te")): arr[:, j] = l * (l + 1) * cl[X][:LMAX + 1] * f / (2 * np.pi)
    M.struct_cleanup(); M.empty(); return QX.pad(arr), extra

def theta0(foot):
    t = json.load(open(os.path.join(Q15, "parts", f"fit_{foot}_main.json")))["theta"]
    return t, np.array([t["omega_b"], t["lnAs1e10"], t["n_s"], t["tau"]])

def do_ka():
    t, x = theta0("canonical"); t0 = time.time()
    D, ex = class_D("canonical", x[0], x[1], x[2], x[3]); dt = time.time() - t0
    t1 = time.time(); Dc, _ = class_D("canonical", x[0], x[1], x[2], x[3], cold_od=t["omega_d"]); dtc = time.time() - t1
    g = QL.grade_spectra(Dc)["PA"]
    r = dict(eval_seconds_ncdm=dt, eval_seconds_cold=dtc, timing_gate=bool(dt <= 60), omega_ncdm_class=ex["omega_ncdm"],
             ka_cmb_chi2=g, ka_cmb_ref=3741.0811439694075, ka_cmb_diff=g - 3741.0811439694075, ka_cmb_pass=bool(abs(g - 3741.0811439694075) <= 5), note=NOTE)
    json.dump(r, open(os.path.join(PARTS, "cmb_ka.json"), "w"), indent=1, default=float); print(json.dumps(r, default=float))

def pen(x):
    ob, lnA, ns, tau = x; s = 0.0
    s += (max(0, QX.OB_BR[0] - ob) + max(0, ob - QX.OB_BR[1])) / 1e-4
    s += (max(0, QX.TAU_BR[0] - tau) + max(0, tau - QX.TAU_BR[1])) / 1e-3
    s += (max(0, 0.7 - ns) + max(0, ns - 1.3)) / 1e-3
    return s

def do_fit(foot):
    _, x0 = theta0(foot); cache = {}; st = {"best": None, "x0": None}
    def f(x):
        x = np.array(x, float); key = tuple(np.round(x, 9))
        if key in cache: return cache[key]
        pp = pen(x)
        if pp > 0: cache[key] = 1e7 + 1e4 * pp; return cache[key]
        try:
            D, _ = class_D(foot, *x); g = QL.grade_spectra(D, x0=st["x0"]); v = g["PA"]
            if not np.isfinite(v): raise ValueError("non-finite")
            st["x0"] = {"Pcut": np.array(g["Pcut"]["nuis"]), "A": np.array(g["A"]["nuis"])}
            if st["best"] is None or v < st["best"][0]: st["best"] = (v, x.tolist())
        except Exception as e:
            v = 1e8; print("ERR", repr(e), flush=True)
        cache[key] = v; print(len(cache), round(v, 2), "best", round(st["best"][0], 2) if st["best"] else None, flush=True); return v
    step = np.array([3e-4, 0.05, 0.02, 0.02]); simplex = [x0] + [x0 + np.eye(4)[i] * step[i] for i in range(4)]
    minimize(f, x0, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=120, xatol=1e-5, fatol=0.05))
    v, x = st["best"]; h, _ = QX.background(foot, x[0], OMF)
    r = dict(foot=foot, chi2_PA=v, delta=v - CHI2_CAL, theta=dict(zip(["omega_b", "lnAs1e10", "n_s", "tau"], x)), h=h, start=x0.tolist(),
             nfev=len(cache), note=NOTE)
    json.dump(r, open(os.path.join(PARTS, f"cmb_fit_{foot}.json"), "w"), indent=1, default=float); print(json.dumps(r, default=float))

def lab(d): return "PASS" if d <= 9 else ("FAIL" if d > 25 else "TENSION")
def do_grade():
    ka = json.load(open(os.path.join(PARTS, "cmb_ka.json"))); L = [f"EW4 primary CMB (QX15 grader, CLASS ncdm m {M_EV:.4f} eV). {NOTE}."]
    L.append(f"timing gate: one ncdm evaluation {ka['eval_seconds_ncdm']:.1f} s (line 60) -> {'run' if ka['timing_gate'] else 'NOT EVALUABLE'}; CLASS omega_ncdm {ka['omega_ncdm_class']:.5f}")
    L.append(f"KA-CMB: CLASS cold at QX15 canonical main theta chi2_PA {ka['ka_cmb_chi2']:.2f} vs 3741.08 ({ka['ka_cmb_diff']:+.2f}, line 5) -> {'PASS' if ka['ka_cmb_pass'] else 'FAIL'}")
    J = dict(ka=ka)
    for foot in ("canonical", "alt"):
        fn = os.path.join(PARTS, f"cmb_fit_{foot}.json")
        if not (ka["timing_gate"] and ka["ka_cmb_pass"] and os.path.exists(fn)): J[foot] = "NOT EVALUABLE"; L.append(f"{foot}: NOT EVALUABLE"); continue
        r = json.load(open(fn)); r["label"] = lab(r["delta"]); J[foot] = r
        L.append(f"{foot}: chi2_PA {r['chi2_PA']:.2f}, Delta vs 3805.80 {r['delta']:+.2f} -> {r['label']} (h {r['h']:.4f}, theta {json.dumps({k: round(v, 5) for k, v in r['theta'].items()})}, nfev {r['nfev']})")
    json.dump(J, open(os.path.join(HERE, "ew4_cmb.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "ew4_cmb.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "ka": do_ka()
    elif a[0] == "fit": do_fit(a[1])
    elif a[0] == "grade": do_grade()
