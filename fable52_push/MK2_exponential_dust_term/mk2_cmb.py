#!/usr/bin/env python3
"""MK2 row a2 (criteria 3b4f515ff8): the record's primary-CMB likelihood (F1A: CAMB 1.6.6, lmax 7000, own P-ACT likelihood PA, nuisances
profiled) at F1A's B2 cold best fit per footing, with the cold component replaced by a constant (w, c_s^2) = (x_T, x_T) fluid carried
with Lambda in CAMB's tabulated-w dark-energy fluid (cs2 = x_T); its unlensed spectra lensed by the cold reference's lensing potential
(camb.correlations, PJ1's construction). Delta chi^2 against the same pipeline at x_T = 1e-12 (the cold reference) <= 10, graded before
refit; a 5-parameter refit at the first failing grid value (and upward while it passes).
KA-C1: F1A's PA chi^2 at B2 (|d| <= 3). KA-C2: the fluid at x_T = 1e-12 against CAMB's own cold run through the same likelihood (|d| <= 3).
If either fails, row a2 is NOT EVALUABLE.
    MK2_FOOT=canonical|alt python3 mk2_cmb.py  -> parts/cmb/cmb_<footing>.json ; python3 mk2_cmb.py merge -> mk2_cmb.json / .out
F1A's f1a.py is executed read-only up to its KA section. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit")
PARTS = os.path.join(HERE, "parts", "cmb"); os.makedirs(PARTS, exist_ok=True)
NOTE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
T0 = time.time(); OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30
C_KMS = 299792.458
if len(sys.argv) > 1 and sys.argv[1] == "merge":
    R = {f: json.load(open(os.path.join(PARTS, f"cmb_{f}.json"))) for f in ("canonical", "alt")}
    json.dump(dict(lane="MK2", row="a2 primary CMB", footings=R, note=NOTE), open(os.path.join(HERE, "mk2_cmb.json"), "w"), indent=1)
    lines = []
    for f, r in R.items(): lines += r.get("log", [])
    open(os.path.join(HERE, "mk2_cmb.out"), "w").write("\n".join(lines + [NOTE]) + "\n"); sys.exit(0)
FOOT_SEL = os.environ.get("MK2_FOOT", "canonical")
src = open(os.path.join(F1AD, "f1a.py")).read()
NS = dict(__file__=os.path.join(F1AD, "f1a.py"), __name__="f1a_prefix")
exec(compile(src[:src.index("# ------------------------------------------------------------------ KA")], os.path.join(F1AD, "f1a.py"), "exec"), NS)
PA, camb_theory, footing_h, TCMB, OMR, LTH = NS["PA"], NS["camb_theory"], NS["footing_h"], NS["TCMB"], NS["OMR"], NS["LTH"]
import camb
import camb.correlations
from camb.dark_energy import DarkEnergyFluid
fit = json.load(open(os.path.join(F1AD, "parts", f"fit_B2_{FOOT_SEL}_cold.json"))); B2 = dict(fit["pars"]); F1A_PA = fit["chi2"]["PA"]
P(f"MK2 row a2 [{FOOT_SEL}] F1A B2 best fit {B2}; F1A PA {F1A_PA:.2f}  [{time.time() - T0:.0f} s {rss():.2f} GB]")

REFLENS = {}
def ref_clpp(pr):
    key = tuple(round(v, 10) for v in pr.values())
    if key not in REFLENS:
        p = camb.CAMBparams(); p.set_cosmology(H0=100 * pr["h"], ombh2=pr["ob"], omch2=pr["oc"], tau=pr["tau"], mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
        p.InitPower.set_params(As=math.exp(pr["lnA"]) * 1e-10, ns=pr["ns"]); p.set_for_lmax(LTH, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
        r = camb.get_results(p); REFLENS.clear(); REFLENS[key] = r.get_lens_potential_cls(LTH)[:, 0]
    return REFLENS[key]
def fluid_D(pr, xT):
    """unlensed spectra with the cold component as a (w, c_s^2) = (xT, xT) fluid carried with Lambda; lensed by the reference potential."""
    h, ob, od = pr["h"], pr["ob"], pr["oc"]; h2 = h * h
    p = camb.CAMBparams(); p.set_cosmology(H0=100 * h, ombh2=ob, omch2=1e-7, tau=pr["tau"], mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
    Oc = od / h2; OL = 1.0 - (ob + 1e-7) / h2 - OMR / h2 - Oc
    a = np.logspace(-9, 0, 2000); rf = Oc * a ** (-3 * (1 + xT)); wa = (-OL + xT * rf) / (OL + rf)
    de = DarkEnergyFluid(cs2=xT); de.set_w_a_table(a, wa); p.DarkEnergy = de
    p.InitPower.set_params(As=math.exp(pr["lnA"]) * 1e-10, ns=pr["ns"]); p.set_for_lmax(LTH, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
    r = camb.get_results(p); un = r.get_unlensed_scalar_cls(LTH, CMB_unit="muK")
    le = camb.correlations.lensed_cls(un, ref_clpp(pr))
    return {"tt": le[:, 0], "ee": le[:, 1], "te": le[:, 3]}
RES = dict(footing=FOOT_SEL, B2=B2, log=[])
def L_(s): P(s); RES["log"].append(s)
# KA-C1
g = PA(camb_theory(**B2)); dC1 = g["PA"] - F1A_PA; RES["KA_C1"] = dict(PA=g["PA"], ref=F1A_PA, d=dC1, ok=bool(abs(dC1) <= 3))
L_(f"[{FOOT_SEL}] KA-C1 F1A PA at B2: {g['PA']:.2f} (F1A {F1A_PA:.2f}, d {dC1:+.2f}) -> {'PASS' if abs(dC1) <= 3 else 'FAIL'}  [{time.time() - T0:.0f} s {rss():.2f} GB]")
# KA-C2
base = PA(fluid_D(B2, 1e-12)); dC2 = base["PA"] - g["PA"]; RES["KA_C2"] = dict(PA_fluid=base["PA"], PA_cold=g["PA"], d=dC2, ok=bool(abs(dC2) <= 3))
L_(f"[{FOOT_SEL}] KA-C2 fluid at x_T 1e-12 lensed by the reference potential: PA {base['PA']:.2f} vs CAMB's cold {g['PA']:.2f} (d {dC2:+.2f}) -> {'PASS' if abs(dC2) <= 3 else 'FAIL'}  [{time.time() - T0:.0f} s {rss():.2f} GB]")
if not (RES["KA_C1"]["ok"] and RES["KA_C2"]["ok"]):
    RES["status"] = "NOT EVALUABLE (a CMB known answer failed)"; L_(f"[{FOOT_SEL}] row a2 NOT EVALUABLE")
else:
    pts = {}
    def at(cs):
        xT = (cs / C_KMS) ** 2; c2 = PA(fluid_D(B2, xT))["PA"]; d = c2 - base["PA"]; pts[cs] = dict(cs=cs, xT=xT, PA=c2, dchi2=d, PASS=bool(d <= 10))
        L_(f"[{FOOT_SEL}]   c_s {cs:8.1f} km/s (x_T {xT:.2e}): Delta chi^2 {d:+.2f} -> {'PASS' if d <= 10 else 'FAIL'} (no refit)  [{time.time() - T0:.0f} s {rss():.2f} GB]")
        return pts[cs]
    for cs in (30.0, 100.0, 300.0, 1000.0, 3000.0, 1e4, 3e4):
        if not at(cs)["PASS"]: break
    srt = sorted(pts); last = max([c for c in srt if pts[c]["PASS"]], default=None); first = min([c for c in srt if not pts[c]["PASS"]], default=None)
    if last is not None and first is not None:
        for cs in np.geomspace(last, first, 4)[1:3]: at(float(f"{cs:.4g}"))
    srt = sorted(pts); last = None
    for c in srt:
        if pts[c]["PASS"]: last = c
        else: break
    first = next((c for c in srt if not pts[c]["PASS"]), None); refit = None
    if first is not None:
        xT = (first / C_KMS) ** 2; lo = np.array([0.0215, 0.05, 2.5, 0.85, 0.02]); hi = np.array([0.0230, 0.25, 3.5, 1.10, 0.12]); state = dict(best=(1e99, None), n=0)
        def fun(x):
            xc = np.clip(x, lo, hi); pen = float(np.sum((x - xc) ** 2)) * 1e6
            pr = dict(h=footing_h(FOOT_SEL, xc[0], xc[1]), ob=xc[0], oc=xc[1], lnA=xc[2], ns=xc[3], tau=xc[4])
            try: c2 = PA(fluid_D(pr, xT))["PA"]
            except Exception: c2 = 1e9
            state["n"] += 1
            if c2 + pen < state["best"][0]: state["best"] = (c2 + pen, pr)
            return c2 + pen
        s0 = np.array([B2["ob"], B2["oc"], B2["lnA"], B2["ns"], B2["tau"]]); st_ = np.array([3e-4, 0.005, 0.03, 0.01, 0.01])
        minimize(fun, s0, method="Nelder-Mead", options=dict(initial_simplex=np.array([s0] + [s0 + np.eye(5)[i] * st_[i] for i in range(5)]), maxfev=60, xatol=1e-5, fatol=0.05))
        d = state["best"][0] - base["PA"]; refit = dict(cs=first, dchi2_refit=d, PASS=bool(d <= 10), nfev=state["n"], pars=state["best"][1])
        L_(f"[{FOOT_SEL}] refit at c_s {first}: Delta chi^2 {d:+.2f} after {state['n']} evaluations -> {'PASS' if d <= 10 else 'FAIL'}")
        if refit["PASS"]: last = first
    RES.update(points={f"{k:g}": v for k, v in sorted(pts.items())}, cs_max=last, first_fail=first, refit=refit, base_PA=base["PA"], status="EVALUATED")
    L_(f"[{FOOT_SEL}] row a2: c_s <= {last} km/s passes (first fail {first}; refit {None if refit is None else round(refit['dchi2_refit'], 2)})")
RES["seconds"] = time.time() - T0; RES["peak_GiB"] = rss()
json.dump(RES, open(os.path.join(PARTS, f"cmb_{FOOT_SEL}.json"), "w"), indent=1, default=float)
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
