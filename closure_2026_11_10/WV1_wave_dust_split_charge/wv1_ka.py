#!/usr/bin/env python3
"""WV1 solver known answers: KA4 (COL1's fold time with Psi off: (i) COL1's test-shell focus time recomputed with its own
equations; (ii) this lane's SP solver at nu = 0.2 kpc km/s puts the central density maximum within 5 % of it), KA5 (the
SP ground state: G M r_1/2 / nu^2 = 3.925 within 2 %), and MUTATE M5 (nu x 10 on KA4(ii)'s run: the peak central density
must drop by at least 30 x).

KA4(ii) FAILS as frozen (AMENDMENT_A1.md: the global central-density maximum is not the focusing event); it is
recorded, and KA4(ii') of A1 (Lagrangian radii against COL1's test-shell equation) is run beside it.

Run:  python3 wv1_ka.py -> wv1_ka.out, wv1_ka.json  (exit 0 iff KA4(i), KA4(ii') [A1], KA5 pass and M5 bites)
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wv1_sp_lib as S
L = S.L
T0 = time.time()
KD1 = json.load(open(os.path.join(HERE, "..", "..", "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")))
LINES, RES, OK = [], {}, True


def P_(s=""):
    LINES.append(s); print(s, flush=True)


P_("WV1 solver known answers. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.")
COL1_PRINTED = {10.7: 0.0712, 9.4: 0.1533}     # col1_focus_check.out, r0 = 0.001 kpc, both footings

# ---------------------------------------------------------------- KA4(i): COL1's test shell (its equations, copied)
P_("")
P_("=== KA4(i): COL1's focusing time (test shell at rest in Hubble flow at z 10, softened ramping point mass) ===")
ka4i = {}
for fo in ("canonical", "alt"):
    s = KD1["footings"][fo]["setting"]; cos = L.Cosmo(s["h"], s["omega_d"], s["omega_b"])
    ti = cos.t_of_a(1 / 11); H = cos.H_of_a(1 / 11)
    for lM in (10.7, 9.4):
        Mb = 10 ** lM; r0 = 0.001
        def rhs(t, y):
            a = cos.a_of_t(t); M = Mb * float(L.smoothstep((t - ti) / (1 / L.TU)))
            g = -L.G * M * y[0] / (y[0] ** 2 + 1.0) ** 1.5 + (-(4 * math.pi / 3) * L.G * (cos.nbar0 + cos.rhob0) * a ** -3 + cos.OL * cos.H0 ** 2) * y[0]
            return [y[1], g]
        ev = lambda t, y: y[0] - 1e-6 * r0; ev.terminal = True; ev.direction = -1
        sol = solve_ivp(rhs, (ti, ti + 1 / L.TU), [r0, H * r0], events=ev, rtol=1e-10, atol=1e-14, max_step=1e-4)
        tf = (sol.t_events[0][0] - ti) * L.TU
        ok = abs(tf / COL1_PRINTED[lM] - 1) < 1e-3
        OK = OK and ok
        ka4i[f"{fo}_{lM}"] = {"t_focus_Gyr": tf, "printed": COL1_PRINTED[lM], "ok": ok}
        P_(f"[{'PASS' if ok else 'FAIL'}] {fo} log M_b {lM}: centre reached {tf:.5f} Gyr after z 10 (COL1 printed {COL1_PRINTED[lM]})")
RES["KA4i"] = ka4i
P_("   This is V2's frame at zero charge (mimetic: test shells): it focuses at COL1's time.")


# ---------------------------------------------------------------- KA4(ii) and M5: SP central focusing
def central_peak(nu, fo="canonical", lM=10.7, t_end_gyr=0.12, x_max=100.0, v_est=150.0):
    a_i = 1 / 11
    dx = math.pi * nu / (3 * a_i * v_est)                       # comoving; a v / nu phase gradient resolved 6 x
    run = S.Run(nu, lM, fo, KD1, x_max=x_max, dx=dx)
    tend = run.ti + t_end_gyr / L.TU
    V, d = run.V(run.t)
    hist = []
    while run.t < tend - 1e-12:
        dt = min(run.choose_dt(d, 2e-4), tend - run.t)
        V, d = run.step(dt, V)
        rc = float(np.mean(np.abs(run.u[:3]) ** 2 / run.x[:3] ** 2))
        hist.append(((run.t - run.ti) * L.TU, rc))
    h = np.array(hist)
    i = int(np.argmax(h[:, 1]))
    return dict(nu=nu, N=run.N, dx=run.dx, steps=run.steps, t_peak_Gyr=float(h[i, 0]), peak_over_bar=float(h[i, 1] / run.rbar),
                end_over_bar=float(h[-1, 1] / run.rbar))


P_("")
P_("=== KA4(ii): this lane's SP solver, nu = 0.2 kpc km/s, central density maximum vs COL1's focus time ===")
k2 = central_peak(0.2)
ok42 = abs(k2["t_peak_Gyr"] / COL1_PRINTED[10.7] - 1) < 0.05
RES["KA4ii_as_frozen"] = dict(k2, ok=ok42)
P_(f"[{'PASS' if ok42 else 'FAIL'} as frozen] canonical log M_b 10.7: central density peaks at {k2['t_peak_Gyr']:.5f} Gyr after z 10 "
   f"(COL1 {COL1_PRINTED[10.7]}; {100 * (k2['t_peak_Gyr'] / COL1_PRINTED[10.7] - 1):+.2f} %), peak {k2['peak_over_bar']:.4g} x rhobar "
   f"(N {k2['N']}, dx {k2['dx']:.4g} kpc, {k2['steps']} steps). Finite: the wave focuses without a singular fold.")
P_("")
P_("=== KA4(ii') (AMENDMENT A1): Psi's Lagrangian radii against COL1's test-shell equation, nu = 0.2 ===")
ka4p = {}
for fo in ("canonical", "alt"):
    s_ = KD1["footings"][fo]["setting"]; cos = L.Cosmo(s_["h"], s_["omega_d"], s_["omega_b"])
    a_i = 1 / 11; nu_ = 0.2
    run = S.Run(nu_, 10.7, fo, KD1, x_max=100.0, dx=math.pi * nu_ / (3 * a_i * 150.0))
    ti = run.ti; Mb = 10 ** 10.7; tf = ka4i[f"{fo}_10.7"]["t_focus_Gyr"] / L.TU
    def shell(r0):
        H = cos.H_of_a(a_i)
        def rhs(t, y):
            a = cos.a_of_t(t); M = Mb * float(L.smoothstep((t - ti) / (1 / L.TU)))
            g = -L.G * M * y[0] / (y[0] ** 2 + 1.0) ** 1.5 + (-(4 * math.pi / 3) * L.G * (cos.nbar0 + cos.rhob0) * a ** -3 + cos.OL * cos.H0 ** 2) * y[0]
            return [y[1], g]
        return solve_ivp(rhs, (ti, ti + tf), [r0, H * r0], rtol=1e-10, atol=1e-14, max_step=1e-4, dense_output=True)
    x0s = [2.0, 5.0, 8.0, 15.0, 30.0]
    M0 = {x0: 4 * math.pi / 3 * run.rbar * x0 ** 3 for x0 in x0s}
    sols = {x0: shell(a_i * x0) for x0 in x0s}
    V, d = run.V(run.t)
    worst = 0.0; rows = []
    for frac in (0.25, 0.5, 0.75, 0.9):
        tn = ti + frac * tf
        while run.t < tn - 1e-13:
            dt = min(run.choose_dt(d, 2e-4), tn - run.t)
            V, d = run.step(dt, V)
        a = run.a(); u2 = np.abs(run.u) ** 2
        Mx = 4 * math.pi * (np.concatenate([[0.0], np.cumsum(0.5 * (u2[1:] + u2[:-1]) * run.dx)]) + 0.5 * u2[0] * run.x[0])
        for x0 in x0s:
            rsp = a * float(np.interp(M0[x0], Mx, run.x)); rcl = float(sols[x0].sol(run.t)[0])
            dev = abs(rsp / rcl - 1); worst = max(worst, dev)
            rows.append({"t_over_tf": frac, "x0": x0, "r_SP": rsp, "r_shell": rcl, "rel_dev": dev})
    okp = worst < 0.05
    OK = OK and okp
    ka4p[fo] = {"worst_rel_dev": worst, "rows": rows, "ok": okp}
    P_(f"[{'PASS' if okp else 'FAIL'}] {fo}: worst |r_SP/r_shell - 1| = {worst:.2e} over x0 = 2-30 kpc, t/t_f = 0.25-0.9 (line 5 %)")
RES["KA4ii_prime_A1"] = ka4p

P_("")
P_("=== MUTATE M5: nu x 10 on the same run ===")
m5 = central_peak(2.0)
ratio = k2["peak_over_bar"] / m5["peak_over_bar"]
bites5 = ratio >= 30
RES["M5"] = dict(m5, ratio_peak_nu_over_10nu=ratio, bites=bites5)
P_(f"[{'BITES' if bites5 else 'DOES NOT BITE'}] nu = 2.0: peak {m5['peak_over_bar']:.4g} x rhobar at {m5['t_peak_Gyr']:.5f} Gyr; "
   f"ratio peak(nu)/peak(10 nu) = {ratio:.4g} (need >= 30): the focus sharpens toward the classical fold as nu falls")
OK = OK and bites5

# ---------------------------------------------------------------- KA5: SP ground state (isolated, imaginary time)
P_("")
P_("=== KA5: SP ground state by imaginary-time relaxation ===")
from scipy.fft import dst
nu, M = 25.37, 1e10
rh_exp = 3.925 * nu ** 2 / (S.G * M)
xmax, N = 30 * rh_exp, 2000
dx = xmax / (N + 1); x = dx * np.arange(1, N + 1); kk = math.pi * np.arange(1, N + 1) / xmax
u = x * np.exp(-(x / (3 * rh_exp)) ** 2)


def norm(u):
    return u * math.sqrt(M / (4 * math.pi * np.sum(u ** 2) * dx))


def encl(u):
    f = 4 * math.pi * u ** 2
    return np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * dx)]) + 0.5 * f[0] * x[0]


def pot(u):
    Mx = encl(u)
    d = S.G * Mx / x ** 2
    c = np.concatenate([[0.0], np.cumsum(0.5 * (d[1:] + d[:-1]) * dx)])
    return (-S.G * Mx[-1] / xmax) - (c[-1] - c) - d[-1] * dx


u = norm(u)
Vmax = abs(pot(u)).max()
dtau = 0.005 * nu / Vmax
E_old = None
for it in range(400000):
    V = pot(u)
    u = u * np.exp(-V * dtau / (2 * nu))
    U = dst(u, type=1, norm="ortho"); U *= np.exp(-nu * kk ** 2 * dtau / 2); u = dst(U, type=1, norm="ortho")
    u = u * np.exp(-pot(u) * dtau / (2 * nu))
    u = norm(u)
    if it % 500 == 0:
        V = pot(u)
        up = np.gradient(u, dx)
        E = 4 * math.pi * np.sum(nu ** 2 * up ** 2 / 2 + 0.5 * V * u ** 2) * dx
        if E_old is not None and abs(E - E_old) < 1e-12 * abs(E):
            break
        E_old = E
Mx = encl(u)
rh = float(np.interp(M / 2, Mx, x))
c = S.G * M * rh / nu ** 2
ok5 = abs(c / 3.925 - 1) < 0.02
OK = OK and ok5
RES["KA5"] = {"G_M_rhalf_over_nu2": c, "iterations": it, "ok": ok5}
P_(f"[{'PASS' if ok5 else 'FAIL'}] G M r_1/2 / nu^2 = {c:.4f} (expected 3.925; {it} iterations, N {N})")

RES["all_ok"] = OK
RES["runtime_s"] = round(time.time() - T0, 1)
P_("")
P_(f"known answers {'all pass (KA4(ii) under A1; FAILS as frozen) and M5 bites' if OK else 'NOT all pass'}; runtime {RES['runtime_s']} s")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "wv1_ka.out"), "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(os.path.join(HERE, "wv1_ka.json"), "w"), indent=1, default=str)
sys.exit(0 if OK else 1)
