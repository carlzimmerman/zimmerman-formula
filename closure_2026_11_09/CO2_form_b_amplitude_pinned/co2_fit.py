#!/usr/bin/env python3
"""CO2 (FROZEN_CRITERIA.md 2bd776c60d) part 1: the pinned fit for one footing.
F1A's B2 cold fit (its own PA likelihood and CAMB call, imported read-only) with the Planck 2018 SimAll low-L EE table
added: chi2_E = -2 sum_L table[int(D_L^EE / 1e-4), L - 2], L 2..29, calibration 1 (Cobaya's planck_2018_lowl.EE rule,
transcribed). The optimiser sees the table linearly interpolated; reported values are the exact lookup.

  nice -n 10 python3 co2_fit.py canonical     -> parts/fit_canonical.json
  nice -n 10 python3 co2_fit.py alt           -> parts/fit_alt.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit"); sys.path.insert(0, F1AD)
import f1a                                                    # noqa: E402  read only
TABF = os.path.join(REPO, "..", "_external_data", "cobaya_2026_10_22", "packages", "data", "planck_2018_lowE_native", "prob_table.txt")
TAB = np.loadtxt(TABF); assert TAB.shape == (3000, 28), TAB.shape
COLS = np.arange(28)
def chi2E(ee, calib=1.0, exact=True):
    """Planck 2018 SimAll low-L EE, L 2..29; ee = D_L^EE in muK^2, zero-based in L."""
    x = np.asarray(ee[2:30], float) / (calib ** 2 * 1e-4); i = x.astype(int)
    if i.min() < 0 or i.max() >= TAB.shape[0] - 1: return float("inf")
    if exact: return float(-2 * TAB[i, COLS].sum())
    fr = x - i; return float(-2 * ((1 - fr) * TAB[i, COLS] + fr * TAB[i + 1, COLS]).sum())

if __name__ == "__main__":
    foot = sys.argv[1]; assert foot in ("canonical", "alt")
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True); T0 = time.time()
    st = json.load(open(os.path.join(F1AD, "parts", f"fit_B2_{foot}_cold.json"))); th0 = np.array(st["theta"], float)
    x00 = {k: np.array(v) for k, v in st["chi2"]["nuis"].items()}
    lo = np.array([0.0215, 0.0, 1.5, 0.80, 0.01]); hi = np.array([0.0230, 0.40, 4.5, 1.30, 0.15]); step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02])   # F1A's
    state = dict(best=None, x0=dict(x00), n=0)
    def evaluate(x, x0=None):
        pr = f1a.theta_to_pars("B2", foot, "cold", np.asarray(x, float)); D = f1a.camb_theory(**pr); g = f1a.PA(D, x0 if x0 is not None else state["x0"])
        return pr, g, chi2E(D["ee"], exact=False), chi2E(D["ee"], exact=True)
    def f(x):
        x = np.asarray(x, float); pen = float(np.sum(np.clip(lo - x, 0, None) ** 2 + np.clip(x - hi, 0, None) ** 2)) * 1e6; xc = np.clip(x, lo, hi)
        try:
            pr, g, cEi, cEx = evaluate(xc); v = g["PA"] + cEi + pen; state["x0"] = {k: np.array(vv) for k, vv in g["nuis"].items()}
        except Exception:
            v = 1e9; g = None
        state["n"] += 1
        if g is not None and (state["best"] is None or v < state["best"][0]): state["best"] = (v, xc.tolist(), g, cEi, cEx)
        if state["n"] % 25 == 0: print(f"  [{foot}] eval {state['n']}: best {state['best'][0]:.3f} tau {state['best'][1][4]:.4f}  ({time.time() - T0:.0f} s)", flush=True)
        return v
    # the unpinned fit, replayed (KA2) and scored on the low-L table
    pr0, g0, cE0i, cE0x = evaluate(th0, x00)
    ka2 = dict(PA=g0["PA"], stored=st["chi2"]["PA"], d=g0["PA"] - st["chi2"]["PA"], pass_=bool(abs(g0["PA"] - st["chi2"]["PA"]) <= 0.1))
    print(f"[{foot}] F1A's unpinned fit: PA {g0['PA']:.3f} (stored {st['chi2']['PA']:.3f}), tau {th0[4]:.4f}, chi2_E {cE0x:.3f}", flush=True)
    sb = th0.copy(); sb[4] = 0.055; sb[2] = th0[2] - 2 * (th0[4] - 0.055)
    starts = [("a_F1A_best_fit", th0), ("b_tau_0.055", sb)]; per_start = []
    for name, s in starts:
        state["x0"] = dict(x00); n0 = state["n"]; before = state["best"][0] if state["best"] else None
        simplex = np.array([s] + [s + np.eye(5)[i] * step[i] for i in range(5)])
        r = minimize(f, s, method="Nelder-Mead", options=dict(initial_simplex=simplex, maxfev=250, xatol=1e-5, fatol=0.02))
        per_start.append(dict(start=name, fun=float(r.fun), x=[float(v) for v in r.x], nfev=state["n"] - n0))
        print(f"[{foot}] start {name}: chi2 {r.fun:.3f} at tau {r.x[4]:.4f} after {state['n'] - n0} evaluations ({time.time() - T0:.0f} s)", flush=True)
    v, x, g, cEi, cEx = state["best"]; x = np.array(x); pr = f1a.theta_to_pars("B2", foot, "cold", x); nu = {k: np.array(vv) for k, vv in g["nuis"].items()}
    # width along the A_s exp(-2 tau) direction, other parameters held
    def along(dtau):
        y = x.copy(); y[4] += dtau; y[2] += 2 * dtau; _, gg, ci, cx = evaluate(y, nu); return gg["PA"] + ci, gg["PA"], cx
    d = 0.004; (cp, _, _), (cm, _, _) = along(+d), along(-d); c0 = g["PA"] + cEi
    curv = (cp + cm - 2 * c0) / 2.0; sig = d / math.sqrt(curv) if curv > 0 else float("nan")
    m1 = along(0.10 - x[4])
    res = dict(lane="CO2", criteria="2bd776c60d", foot=foot, theta=x.tolist(), pars=pr, chi2=dict(total_interp=float(v), PA=g["PA"], Pcut=g["Pcut"], A=g["A"], E_exact=cEx, E_interp=cEi, nuis=g["nuis"]),
               unpinned=dict(theta=th0.tolist(), pars=pr0, PA=g0["PA"], E_exact=cE0x), dPA=g["PA"] - g0["PA"], dE=cEx - cE0x, per_start=per_start, nfev=state["n"],
               tau_width_along_degeneracy=dict(step=d, chi2_plus=cp, chi2_minus=cm, chi2_0=c0, sigma=sig, note="other parameters held: understates the profile width"),
               KA2=ka2, KA3=dict(d=cEi - cEx, pass_=bool(abs(cEi - cEx) <= 0.25)),
               M1=dict(tau=0.10, E_exact=m1[2], rise=m1[2] - cEx, bites=bool(m1[2] - cEx >= 9)), runtime_s=time.time() - T0, peak_rss_GB=f1a.rss(),
               note="kappa = 1/2 FITTED; not theory closed")
    json.dump(res, open(os.path.join(HERE, "parts", f"fit_{foot}.json"), "w"), indent=1, default=float)
    print(f"[{foot}] PINNED: tau {x[4]:.4f} +- {sig:.4f} (along the degeneracy), ln 1e10 A_s {x[2]:.4f}, omega_b {x[0]:.5f}, omega_d {x[1]:.4f}, n_s {x[3]:.4f}, h {pr['h']:.4f}; "
          f"PA {g['PA']:.3f} (unpinned {g0['PA']:.3f}, +{g['PA'] - g0['PA']:.2f}); chi2_E {cEx:.3f} (unpinned {cE0x:.3f}, {cEx - cE0x:+.2f}); "
          f"M1 tau 0.10: chi2_E +{m1[2] - cEx:.2f} -> {'bites' if m1[2] - cEx >= 9 else 'DOES NOT BITE'}; KA2 {'PASS' if ka2['pass_'] else 'FAIL'}; "
          f"KA3 {cEi - cEx:+.3f}; {state['n']} evaluations, {time.time() - T0:.0f} s", flush=True)
