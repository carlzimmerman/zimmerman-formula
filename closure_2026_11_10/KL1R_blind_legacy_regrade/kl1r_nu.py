#!/usr/bin/env python3
"""KL1R (FROZEN_CRITERIA.md 1792bd07ea, section 2.2): the neutrino floor, my own refit, one footing per call.
Objective: F1A's PA (imported read-only) + CO2's Planck 2018 low-L EE term (CO2's chi2E), with my CAMB call = F1A's camb_theory
re-written with one 0.06 eV neutrino (mnu 0.06, num_massive_neutrinos 1, nnu 3.046). h rule: canonical h^2 = footing_h^2 + 0.06/93.14;
alt unchanged. Nelder-Mead, F1A's bounds and steps, <= 250 evaluations per start, starts (a) CO2's pinned theta, (b) tau 0.058 with
ln A_s raised by 2 (0.058 - tau). Target sigma8 = CLASS (total matter) at the refit with the neutrino (CO2's class_B settings).
Also KA1 (i) / (ii) and MA1.

  nice -n 15 python3 kl1r_nu.py canonical   -> parts/nu_canonical.json   (checkpoint parts/nu_canonical_ckpt.json; SIGTERM-safe)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit"); CO2D = os.path.join(REPO, "closure_2026_11_09", "CO2_form_b_amplitude_pinned")
sys.path.insert(0, F1AD); sys.path.insert(0, CO2D)
import f1a                      # noqa: E402  read only
from co2_fit import chi2E       # noqa: E402  CO2's low-L EE reader (module body defines functions and loads the table only)
OMNU = 0.06 / 93.14

def camb_nu(h, ob, oc, lnA, ns, tau, mnu=0.06):
    import camb
    p = camb.CAMBparams()
    if mnu > 0: p.set_cosmology(H0=100 * h, ombh2=ob, omch2=max(oc, 1e-7), tau=tau, mnu=mnu, num_massive_neutrinos=1, nnu=3.046, TCMB=f1a.TCMB)
    else: p.set_cosmology(H0=100 * h, ombh2=ob, omch2=max(oc, 1e-7), tau=tau, mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=f1a.TCMB)
    p.InitPower.set_params(As=math.exp(lnA) * 1e-10, ns=ns); p.set_for_lmax(f1a.LTH, lens_potential_accuracy=1)
    p.NonLinear = camb.model.NonLinear_none
    cl = camb.get_results(p).get_total_cls(f1a.LTH, CMB_unit="muK"); return {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}

def pars_nu(foot, th, nu=True):
    ob, od, lnA, ns, tau = th
    h0 = f1a.footing_h(foot, ob, od)
    h = math.sqrt(h0 ** 2 + OMNU) if (nu and foot == "canonical") else h0
    return dict(h=h, ob=ob, oc=od, lnA=lnA, ns=ns, tau=tau)

def class_sigma8(pr, mnu=0.06):
    from classy import Class
    M = Class()
    d = {'output': 'mPk', 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
         'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': 20.0}
    if mnu > 0: d.update({'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': mnu, 'T_ncdm': 0.71611})
    M.set(d); M.compute(); s = M.sigma8(); Om = M.Omega_m(); M.struct_cleanup(); M.empty(); return s, Om

if __name__ == "__main__":
    foot = sys.argv[1]; assert foot in ("canonical", "alt")
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True); T0 = time.time()
    CK = os.path.join(HERE, "parts", f"nu_{foot}_ckpt.json")
    co2 = json.load(open(os.path.join(CO2D, "parts", f"fit_{foot}.json"))); th_pin = np.array(co2["theta"], float)
    nu0 = {k: np.array(v) for k, v in co2["chi2"]["nuis"].items()}
    # ---- KA1 (i): my call with mnu 0 and no neutrino in h at CO2's pinned theta
    pr0 = pars_nu(foot, th_pin, nu=False); D0 = camb_nu(**pr0, mnu=0.0); g0 = f1a.PA(D0, nu0); e0 = chi2E(D0["ee"], exact=True)
    ka1i = dict(PA=g0["PA"], PA_CO2=co2["chi2"]["PA"], E=e0, E_CO2=co2["chi2"]["E_exact"],
                pass_=bool(abs(g0["PA"] - co2["chi2"]["PA"]) <= 0.1 and abs(e0 - co2["chi2"]["E_exact"]) <= 0.01))
    print(f"[{foot}] KA1(i) mnu 0 at CO2's pinned theta: PA {g0['PA']:.3f} (CO2 {co2['chi2']['PA']:.3f}), chi2_E {e0:.3f} (CO2 {co2['chi2']['E_exact']:.3f}) -> {'PASS' if ka1i['pass_'] else 'FAIL'}", flush=True)
    s8_bracket, _ = class_sigma8(pr0, 0.06)
    ka1ii = dict(sigma8=s8_bracket, ref=0.8152, pass_=bool(abs(s8_bracket - 0.8152) <= 0.0005))
    print(f"[{foot}] KA1(ii) CLASS sigma8 with one 0.06 eV neutrino at CO2's pinned parameters: {s8_bracket:.5f} (0.8152) -> {'PASS' if ka1ii['pass_'] else 'FAIL'}", flush=True)
    pin_total = co2["chi2"]["PA"] + co2["chi2"]["E_exact"]
    lo = np.array([0.0215, 0.0, 1.5, 0.80, 0.01]); hi = np.array([0.0230, 0.40, 4.5, 1.30, 0.15]); step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02])
    state = dict(best=None, x0=dict(nu0), n=0)
    if os.path.exists(CK):
        ck = json.load(open(CK)); print(f"[{foot}] resuming from checkpoint: best {ck['best'][0]:.3f} after {ck['n']} evaluations", flush=True)
    def save():
        if state["best"] is not None:
            v, x, g, ci, cx = state["best"]; json.dump(dict(best=[v, x, g, ci, cx], n=state["n"]), open(CK, "w"), default=float)
    def onterm(sig, frm):
        save(); print(f"[{foot}] SIGTERM: checkpoint written", flush=True); sys.exit(143)
    signal.signal(signal.SIGTERM, onterm)
    def evaluate(x, x0=None):
        pr = pars_nu(foot, np.asarray(x, float)); D = camb_nu(**pr); g = f1a.PA(D, x0 if x0 is not None else state["x0"])
        return pr, g, chi2E(D["ee"], exact=False), chi2E(D["ee"], exact=True)
    def f(x):
        x = np.asarray(x, float); pen = float(np.sum(np.clip(lo - x, 0, None) ** 2 + np.clip(x - hi, 0, None) ** 2)) * 1e6; xc = np.clip(x, lo, hi)
        try:
            pr, g, cEi, cEx = evaluate(xc); v = g["PA"] + cEi + pen; state["x0"] = {k: np.array(vv) for k, vv in g["nuis"].items()}
        except Exception:
            v = 1e9; g = None; cEi = cEx = None
        state["n"] += 1
        if g is not None and (state["best"] is None or v < state["best"][0]): state["best"] = (v, xc.tolist(), g, cEi, cEx)
        if state["n"] % 25 == 0:
            save(); print(f"  [{foot}] eval {state['n']}: best {state['best'][0]:.3f} tau {state['best'][1][4]:.4f} ({time.time() - T0:.0f} s)", flush=True)
        return v
    sb = th_pin.copy(); sb[4] = 0.058; sb[2] = th_pin[2] + 2 * (0.058 - th_pin[4])
    per = []
    for name, s in (("a_CO2_pinned", th_pin), ("b_tau_0.058", sb)):
        state["x0"] = dict(nu0); n0 = state["n"]
        simplex = np.array([s] + [s + np.eye(5)[i] * step[i] for i in range(5)])
        r = minimize(f, s, method="Nelder-Mead", options=dict(initial_simplex=simplex, maxfev=250, xatol=1e-5, fatol=0.02))
        per.append(dict(start=name, fun=float(r.fun), x=[float(v) for v in r.x], nfev=state["n"] - n0))
        print(f"[{foot}] start {name}: {r.fun:.3f} at tau {r.x[4]:.4f} after {state['n'] - n0} evaluations ({time.time() - T0:.0f} s)", flush=True)
    v, x, g, cEi, cEx = state["best"]; x = np.array(x); pr = pars_nu(foot, x)
    s8, Om = class_sigma8(pr, 0.06); s8_06, _ = class_sigma8(pr, 0.6)
    tot = g["PA"] + cEx; cost = tot - pin_total
    res = dict(lane="KL1R", criteria="1792bd07ea", foot=foot, theta=x.tolist(), pars=pr, sigma8_target=s8, Omega_m=Om, S8=s8 * math.sqrt(Om / 0.3),
               chi2=dict(PA=g["PA"], E_exact=cEx, E_interp=cEi, total=tot, total_interp=v, nuis=g["nuis"]),
               CO2_pinned=dict(theta=th_pin.tolist(), PA=co2["chi2"]["PA"], E_exact=co2["chi2"]["E_exact"], total=pin_total),
               cmb_cost=cost, flag_inadequate=bool(cost > 9), per_start=per, nfev=state["n"],
               KA1=dict(i=ka1i, ii=ka1ii), MA1=dict(sigma8_0p6eV=s8_06, drop=s8 - s8_06, bites=bool(s8 - s8_06 >= 0.03)),
               runtime_s=time.time() - T0, note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
    json.dump(res, open(os.path.join(HERE, "parts", f"nu_{foot}.json"), "w"), indent=1, default=float)
    print(f"[{foot}] REFIT with one 0.06 eV neutrino: tau {x[4]:.4f}, ln 1e10 A_s {x[2]:.4f}, omega_b {x[0]:.5f}, omega_d {x[1]:.4f}, n_s {x[3]:.4f}, h {pr['h']:.4f}; "
          f"PA {g['PA']:.3f}, chi2_E {cEx:.3f}, total {tot:.3f} (CO2 pinned {pin_total:.3f}; cost {cost:+.2f}); CLASS sigma8 {s8:.4f} (Omega_m {Om:.4f}); "
          f"MA1 0.6 eV: sigma8 {s8_06:.4f}, drop {s8 - s8_06:.4f} -> {'bites' if s8 - s8_06 >= 0.03 else 'DOES NOT BITE'}  ({time.time() - T0:.0f} s)", flush=True)
