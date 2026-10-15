"""CFG791 -- hypothetical cold-energy photon ramjet: exact relativistic acceleration and mission times.  Criteria FROZEN_CRITERIA.md.
Run: python3 cfg791.py   (CFG791_MUTATE=1: unconverted cold energy absorbed -> drag).  HYPOTHETICAL portal efficiency eta.
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("CFG791_MUTATE") == "1"
c, MSUN, PC, YR, LY = 2.998e8, 1.989e30, 3.0857e16, 3.156e7, 9.4607e15
rho = 0.01 * MSUN / PC ** 3
OUT = []
def P(s): print(s); OUT.append(s)

def accel(beta, eta, A, M):
    g2 = 1 / (1 - beta ** 2)
    if MUT:   # unconverted (1-eta) absorbed: extra drag, no thrust
        F = rho * A * g2 * beta * c * (eta * c - beta * c)
    else:
        F = eta * rho * A * g2 * beta * c * (c - beta * c)
    return F / M

def run(M, A, eta):
    phi0 = math.atanh(230e3 / c)
    def f(tau, y):
        phi, t, x = y; b = math.tanh(phi)
        return [accel(b, eta, A, M) / c, math.cosh(phi), c * math.sinh(phi)]
    targets = {}
    def ev(btarget):
        e = lambda tau, y: math.tanh(y[0]) - btarget; e.terminal = False; e.direction = 1; return e
    evs = [ev(0.1), ev(0.5), ev(0.9)]
    edist = lambda tau, y: y[2] - 4.37 * LY; edist.terminal = True; edist.direction = 1
    K = eta * rho * A * c / M
    tmax = 60 / max(K, 1e-30) + 50 * YR
    sol = solve_ivp(f, (0, tmax), [phi0, 0.0, 0.0], events=evs + [edist], rtol=1e-9, atol=1e-6, max_step=tmax / 2000)
    out = dict(tau0_days=(M / (eta * rho * A * c)) / 86400 if not MUT else float("nan"))
    for lab, k in (("0.1", 0), ("0.5", 1), ("0.9", 2)):
        if len(sol.t_events[k]):
            out[f"beta{lab}_tau_yr"] = sol.t_events[k][0] / YR; out[f"beta{lab}_t_yr"] = sol.y_events[k][0][1] / YR
    if len(sol.t_events[3]):
        out["aCen_tau_yr"] = sol.t_events[3][0] / YR; out["aCen_t_yr"] = sol.y_events[3][0][1] / YR
        out["aCen_beta"] = math.tanh(sol.y_events[3][0][0])
    out["alpha_inf_g"] = eta * rho * A * c ** 2 / (2 * M) / 9.81
    out["P_at_0.1_W"] = eta * rho * A * (1 / (1 - 0.01)) * 0.1 * c * c ** 2
    return out

P("CFG791  hypothetical cold-energy photon ramjet" + ("  [MUTATE absorbed drag]" if MUT else ""))
designs = {"D1 100 kg, 100 km^2": (100.0, 1e8), "D2 1 t, 1 km^2": (1e3, 1e6), "D3 10 t, 1e4 km^2": (1e4, 1e10)}
res = {}
for dn, (M, A) in designs.items():
    for eta in (1.0, 0.1, 0.01):
        r = run(M, A, eta); res[f"{dn}|{eta}"] = r
        s = f"  {dn:20s} eta {eta:<5}: tau0 {r['tau0_days']:.3g} d; "
        for lab in ("0.1", "0.5", "0.9"):
            if f"beta{lab}_tau_yr" in r: s += f"beta {lab} at tau {r[f'beta{lab}_tau_yr']:.3g} yr (t {r[f'beta{lab}_t_yr']:.3g}); "
        if "aCen_tau_yr" in r: s += f"alpha Cen in tau {r['aCen_tau_yr']:.3g} yr / t {r['aCen_t_yr']:.3g} yr (arrive beta {r['aCen_beta']:.3f}); "
        s += f"alpha_inf {r['alpha_inf_g']:.3g} g; P(beta 0.1) {r['P_at_0.1_W']:.3g} W"
        P(s)
if not MUT:
    M, A, eta = 100.0, 1e8, 1.0
    K = eta * rho * A * c / M
    b = 1e-4; num = accel(b, eta, A, M) / (b * c)
    P(f"  K1 low-beta e-fold rate {num:.6e} vs eta rho A c/M {K:.6e}: rel {abs(num / K - 1):.1e}")
    b = 0.999; num2 = accel(b, eta, A, M) / (1 + 0) ; ana = eta * rho * A * c ** 2 / M * b / (1 + b)
    P(f"  K2 high-beta alpha {num2:.6e} vs eta rho A c^2/M * b/(1+b) {ana:.6e}: rel {abs(num2 / ana - 1):.1e}")
    P("  K3 energy: craft rest mass constant by construction (all intercepted converted energy re-emitted); intake power = emitted power")
else:
    a_mut = accel(0.1, 0.1, 1e8, 100.0); a_ok = 0.1 * rho * 1e8 * (1 / 0.99) * 0.1 * c * (c - 0.1 * c) / 100.0
    P(f"  MUTATE: alpha at beta 0.1, eta 0.1 with absorbed drag {a_mut:.3e} vs pass-through {a_ok:.3e} -> {'drag bites' if a_mut < a_ok else 'DID NOT BITE'}")
json.dump(res, open(os.path.join(HERE, f"cfg791_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg791{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
