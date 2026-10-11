"""CFG591 ADDENDUM 1 helper: switch the epoch machinery to the DESI-tracking variant (flat w0waCDM background, a0(z) = a0(0) sqrt(f(z))).
activate(w0, wa) patches, IN THIS PROCESS ONLY, cfg557_lib's background (Hof -> w0wa H; Dgrow -> growth ODE solution, D ~ a early;
shell -> spherical collapse with the w(a) dark-energy term and a(t) integrated alongside; T0) and sets cfg591_lib.DE.  Omega_m, h, omega_b,
n_s, sigma8(z = 0) unchanged (declared).  Delta_ta anchor: 11.81 / Delta_ODE,Lambda(0) (computed before patching).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json, math
import numpy as np
from scipy.integrate import solve_ivp
import cfg591_lib as C
L = C.L
HERE = os.path.dirname(os.path.abspath(__file__))
J549 = os.path.join(C.LANES, "CFG549_dark_energy_evolution_prediction", "cfg549_results.json")


def desi_w0wa():
    m = json.load(open(J549))["chains"]["desy5"]["w0wa_mean"]
    return float(m[0]), float(m[1])


def other_chain_ratios(zs=(0.5, 1.0, 2.0)):
    out = {}
    for nm, d in json.load(open(J549))["chains"].items():
        w0, wa = d["w0wa_mean"]
        out[nm] = {str(z): math.sqrt((1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))) for z in zs}
    return out


def activate(w0, wa):
    C.delta_ta(0.0)                    # Lambda anchor Delta_ODE(0) computed with the unpatched (w = -1) machinery
    C._EP.clear()
    C.DE = dict(w0=w0, wa=wa)
    Om, OL = L.Om, L.OL
    f = lambda a: a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
    wof = lambda a: w0 + wa * (1 - a)
    def Hof(a): return math.sqrt(Om / a ** 3 + OL * f(a))
    L.Hof = Hof
    # growth: d2D/dlna2 + (2 + dlnH/dlna) dD/dlna - 1.5 Om/(a^3 H^2) D = 0, D = a at a = 1e-5
    def dlnH(a):
        return (-3 * Om / a ** 3 - 3 * (1 + wof(a)) * OL * f(a)) / (2 * Hof(a) ** 2)
    def rhs(x, y):
        a = math.exp(x)
        return [y[1], -(2 + dlnH(a)) * y[1] + 1.5 * Om / (a ** 3 * Hof(a) ** 2) * y[0]]
    a_i = 1e-5
    sol = solve_ivp(rhs, (math.log(a_i), math.log(60.0)), [a_i, a_i], rtol=1e-12, atol=1e-20, method="DOP853", dense_output=True)
    def Dgrow(a): return float(sol.sol(math.log(a))[0])
    L.Dgrow = Dgrow
    L.T0 = L.age(1.0)
    def shell(dL, a_obs, t_end=None):
        di = dL * Dgrow(L.AI) / Dgrow(a_obs)
        ti = L.age(L.AI)
        ri = L.AI * (1 - di / 3.0); vi = Hof(L.AI) * L.AI * (1 - 2 * di / 3.0)
        rh = lambda t, y: [y[1], -0.5 * Om / y[0] ** 2 - 0.5 * OL * f(y[2]) * (1 + 3 * wof(y[2])) * y[0], y[2] * Hof(y[2])]
        ev = lambda t, y: y[1]; ev.terminal = True; ev.direction = -1
        te = t_end if t_end is not None else 400.0
        s1 = solve_ivp(rh, (ti, te), [ri, vi, L.AI], events=ev, rtol=1e-11, atol=1e-14, method="DOP853")
        if not s1.t_events[0].size:
            return None
        tta = s1.t_events[0][0]; rta = s1.y_events[0][0][0]; ata = s1.y_events[0][0][2]
        ev2 = lambda t, y: y[0] - 0.002 * rta; ev2.terminal = True; ev2.direction = -1
        s2 = solve_ivp(rh, (tta, tta + 400.0), [rta, 0.0, ata], events=ev2, rtol=1e-11, atol=1e-14, method="DOP853", dense_output=True)
        tc = s2.t_events[0][0]
        tt = np.linspace(tta, tc, 4000); rr = s2.sol(tt)[0]
        dt = np.interp(L.UGRID, rr[::-1] / rta, (tt - tta)[::-1])
        tcoll = tc + (2.0 / 3.0) * (0.002 * rta) ** 1.5 / math.sqrt(Om)
        return dict(t_ta=tta, r_ta=rta, a_ta=ata, t_coll=tcoll, dt=dt)
    L.shell = shell
    return dict(w0=w0, wa=wa, T0_gyr=L.T0 * L.GYR_PER_HINV)
