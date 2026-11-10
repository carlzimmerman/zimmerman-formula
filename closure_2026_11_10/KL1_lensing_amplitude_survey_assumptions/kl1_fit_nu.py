#!/usr/bin/env python3
"""KL1 (FROZEN_CRITERIA.md 99a42c78ef) row A1: CO2's pinned fit redone with the neutrino floor, one footing.
CO2's co2_fit.py objective (F1A's PA + Planck 2018 SimAll low-L EE; interpolated table for the optimiser, exact lookup reported),
with F1A's CAMB call given one 0.06 eV neutrino (mnu 0.06, num_massive_neutrinos 1, nnu 3.046) and the canonical footing's h rule
extended by omega_nu = 0.06 / 93.14 (alt unchanged). Starts: (a) CO2's pinned theta; (b) tau 0.058, ln A_s + 2 (0.058 - tau).
KA1 (i): the same harness with the neutrino mass 0 replays CO2's stored PA (0.1) and exact chi2_E (0.01) at CO2's pinned theta.

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1_fit_nu.py canonical     -> parts/fit_nu_canonical.json
  OMP_NUM_THREADS=1 nice -n 10 python3 kl1_fit_nu.py alt           -> parts/fit_nu_alt.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CO2 = os.path.join(REPO, "closure_2026_11_09", "CO2_form_b_amplitude_pinned"); sys.path.insert(0, CO2)
from co2_fit import chi2E, f1a                                # noqa: E402  read only (CO2 imports F1A read only)
MNU = 0.06; ONU = MNU / 93.14
_footing_h0 = f1a.footing_h
STATE = dict(mnu=0.0)
def camb_theory_nu(h, ob, oc, lnA, ns, tau, nonlin=False):
    """F1A's camb_theory with the neutrino mass as the only change."""
    import camb
    m = STATE["mnu"]
    p = camb.CAMBparams(); p.set_cosmology(H0=100 * h, ombh2=ob, omch2=max(oc, 1e-7), tau=tau, mnu=m, num_massive_neutrinos=1 if m > 0 else 0, nnu=3.046, TCMB=f1a.TCMB)
    p.InitPower.set_params(As=math.exp(lnA) * 1e-10, ns=ns); p.set_for_lmax(f1a.LTH, lens_potential_accuracy=1)
    p.NonLinear = camb.model.NonLinear_lens if nonlin else camb.model.NonLinear_none
    cl = camb.get_results(p).get_total_cls(f1a.LTH, CMB_unit="muK"); return {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}
def footing_h_nu(foot, ob, od):
    if foot == "canonical":
        w = 4 * f1a.FOOT[foot] ** 2 / (f1a.G * f1a.CL ** 2) / f1a.RHO_C100
        return math.sqrt(w + ob + od + f1a.OMR + (ONU if STATE["mnu"] > 0 else 0.0))
    return _footing_h0(foot, ob, od)
f1a.footing_h = footing_h_nu

if __name__ == "__main__":
    foot = sys.argv[1]; assert foot in ("canonical", "alt")
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True); T0 = time.time()
    st = json.load(open(os.path.join(CO2, "parts", f"fit_{foot}.json"))); th0 = np.array(st["theta"], float)
    x00 = {k: np.array(v) for k, v in st["chi2"]["nuis"].items()}
    def evaluate(x, x0):
        pr = f1a.theta_to_pars("B2", foot, "cold", np.asarray(x, float)); D = camb_theory_nu(**pr); g = f1a.PA(D, x0)
        return pr, g, chi2E(D["ee"], exact=False), chi2E(D["ee"], exact=True)
    # KA1 (i): the harness with the neutrino mass 0 replays CO2's pinned fit
    STATE["mnu"] = 0.0
    pr0, g0, cE0i, cE0x = evaluate(th0, x00)
    h_same = abs(pr0["h"] - st["pars"]["h"]) <= 1e-12
    ka1 = dict(PA=g0["PA"], PA_stored=st["chi2"]["PA"], dPA=g0["PA"] - st["chi2"]["PA"], E=cE0x, E_stored=st["chi2"]["E_exact"], dE=cE0x - st["chi2"]["E_exact"], h_same=h_same,
               pass_=bool(abs(g0["PA"] - st["chi2"]["PA"]) <= 0.1 and abs(cE0x - st["chi2"]["E_exact"]) <= 0.01 and h_same))
    print(f"[{foot}] KA1 (i) harness at mnu 0: PA {g0['PA']:.3f} (CO2 {st['chi2']['PA']:.3f}), chi2_E {cE0x:.3f} (CO2 {st['chi2']['E_exact']:.3f}), h same {h_same} -> {'PASS' if ka1['pass_'] else 'FAIL'}", flush=True)
    # the refit with the neutrino floor
    STATE["mnu"] = MNU
    lo = np.array([0.0215, 0.0, 1.5, 0.80, 0.01]); hi = np.array([0.0230, 0.40, 4.5, 1.30, 0.15]); step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02])   # F1A's
    state = dict(best=None, x0=dict(x00), n=0)
    def f(x):
        x = np.asarray(x, float); pen = float(np.sum(np.clip(lo - x, 0, None) ** 2 + np.clip(x - hi, 0, None) ** 2)) * 1e6; xc = np.clip(x, lo, hi)
        try:
            pr, g, cEi, cEx = evaluate(xc, state["x0"]); v = g["PA"] + cEi + pen; state["x0"] = {k: np.array(vv) for k, vv in g["nuis"].items()}
        except Exception:
            v = 1e9; g = None
        state["n"] += 1
        if g is not None and (state["best"] is None or v < state["best"][0]): state["best"] = (v, xc.tolist(), g, cEi, cEx)
        if state["n"] % 25 == 0: print(f"  [{foot}] eval {state['n']}: best {state['best'][0]:.3f} tau {state['best'][1][4]:.4f}  ({time.time() - T0:.0f} s)", flush=True)
        return v
    prs, gs, cEsi, cEsx = evaluate(th0, x00)
    at_co2 = dict(PA=gs["PA"], E_exact=cEsx, total_interp=gs["PA"] + cEsi, h=prs["h"])
    print(f"[{foot}] with the neutrino at CO2's pinned theta: PA {gs['PA']:.3f}, chi2_E {cEsx:.3f}, h {prs['h']:.5f}", flush=True)
    sb = th0.copy(); sb[4] = 0.058; sb[2] = th0[2] + 2 * (0.058 - th0[4])
    per_start = []
    for name, s in (("a_CO2_pinned", th0), ("b_tau_0.058", sb)):
        state["x0"] = dict(x00); n0 = state["n"]
        simplex = np.array([s] + [s + np.eye(5)[i] * step[i] for i in range(5)])
        r = minimize(f, s, method="Nelder-Mead", options=dict(initial_simplex=simplex, maxfev=250, xatol=1e-5, fatol=0.02))
        per_start.append(dict(start=name, fun=float(r.fun), x=[float(v) for v in r.x], nfev=state["n"] - n0))
        print(f"[{foot}] start {name}: chi2 {r.fun:.3f} at tau {r.x[4]:.4f} after {state['n'] - n0} evaluations ({time.time() - T0:.0f} s)", flush=True)
    v, x, g, cEi, cEx = state["best"]; x = np.array(x); pr = f1a.theta_to_pars("B2", foot, "cold", x)
    co2_tot = st["chi2"]["PA"] + st["chi2"]["E_exact"]; tot = g["PA"] + cEx
    res = dict(lane="KL1", row="A1", criteria="99a42c78ef", foot=foot, mnu=MNU, omega_nu=ONU, theta=x.tolist(), pars=pr,
               chi2=dict(total_interp=float(v), PA=g["PA"], E_exact=cEx, E_interp=cEi, nuis=g["nuis"]),
               CO2=dict(theta=th0.tolist(), pars=st["pars"], PA=st["chi2"]["PA"], E_exact=st["chi2"]["E_exact"], total=co2_tot),
               at_CO2_theta_with_nu=at_co2, d_total_vs_CO2=tot - co2_tot, adequate=bool(tot - co2_tot <= 9.0),
               per_start=per_start, nfev=state["n"], KA1_i=ka1, runtime_s=time.time() - T0, note="kappa = 1/2 FITTED; not theory closed")
    json.dump(res, open(os.path.join(HERE, "parts", f"fit_nu_{foot}.json"), "w"), indent=1, default=float)
    print(f"[{foot}] A1 REFIT: tau {x[4]:.4f}, ln 1e10 A_s {x[2]:.4f}, omega_b {x[0]:.5f}, omega_d {x[1]:.4f}, n_s {x[3]:.4f}, h {pr['h']:.5f}; "
          f"PA {g['PA']:.3f}, chi2_E {cEx:.3f}; total {tot:.3f} against CO2's {co2_tot:.3f} ({tot - co2_tot:+.2f}); {state['n']} evaluations, {time.time() - T0:.0f} s", flush=True)
