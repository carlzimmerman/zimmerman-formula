"""CFG837 numerical cross-check of DERIVATION.md (lane SHELL, parameter-reduction round 2).

STATUS: WRITTEN, NOT RUN, UNTESTED. It was written while a 1024^3 simulation was live and the no-compute rule was in force. It is QUEUED
behind that run. No statement in DERIVATION.md depends on its output; the hand-derived formulas are cross-checked against it here.

Before running: confirm that no 1024^3 job is live (pgrep for the CFG650/T2x engines and the chain log), then set CFG837_I_CHECKED=1.
One process, OMP_NUM_THREADS=1, nice -n 19, < 200 MB. Parts (env CFG837_PART): A takes seconds, B about a minute (pure-python leapfrog, ~10 M steps), C takes tens of minutes (10 runs of the CFG776 integrator).
    CFG837_I_CHECKED=1 CFG837_PART=A OMP_NUM_THREADS=1 nice -n 19 python3 cfg837_shell_check.py
Units G = a0 = M_now = 1 (CFG747/776): r'' = -1/r^2 + m(<r)^2 / r^4. kappa = 1/2 FITTED; not "theory closed".
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.environ.get("CFG837_PART", "A")
if os.environ.get("CFG837_I_CHECKED") != "1":
    sys.exit("refusing to run: set CFG837_I_CHECKED=1 only after confirming that no 1024^3 job is live")
OUT = {"part": PART}
LINES = []


def P(s):
    print(s, flush=True)
    LINES.append(s)


# ---------------------------------------------------------------- analytic formulas of DERIVATION.md
def x_apo(p):
    """apocentre / pericentre for a shell released at rest at r0 with enclosed mass sqrt(p) r0 (needs p < 3)."""
    return (p + math.sqrt(3 * p * (4 - p))) / (2 * (3 - p))


def half_period(p, n=4000):
    """time from pericentre to apocentre in units r0^(3/2) t0, theta-midpoint rule of dt = dx / v."""
    xa = x_apo(p)
    xb = (p - math.sqrt(12 * p - 3 * p * p)) / (2 * (3 - p))
    mid, hw = 0.5 * (1 + xa), 0.5 * (xa - 1)
    pref = math.sqrt(3.0 / (2 * (3 - p)))
    s = 0.0
    for k in range(n):
        th = (k + 0.5) * math.pi / n
        x = mid - hw * math.cos(th)
        s += pref * x ** 1.5 / math.sqrt(x - xb)
    return s * math.pi / n


def eps_sudden(p, r0=1.0):
    return -(3 - p) / (3 * r0)


def single_shell(p, tmax, dt=1e-4, stop_at_apo=True):
    """leapfrog for one shell, r0 = 1, m = sqrt(p) constant (valid until the first shell crossing)."""
    m2 = p
    r, v, t = 1.0, 0.0, 0.0
    a = -1 / r ** 2 + m2 / r ** 4
    rmax, tapo = r, None
    while t < tmax:
        v += 0.5 * dt * a
        r += dt * v
        a = -1 / r ** 2 + m2 / r ** 4
        v += 0.5 * dt * a
        t += dt
        if r > rmax:
            rmax = r
        if stop_at_apo and v < 0:
            tapo = t
            break
    return r, v, t, rmax, tapo


if PART == "A":
    P("PART A: single-shell checks (no crossing) against the closed forms")
    rows = []
    ok = True
    for p in (1.1, 1.5, 2.0, 2.5):
        r, v, t, rmax, tapo = single_shell(p, tmax=400.0, dt=2e-4)
        xa, hp = x_apo(p), half_period(p)
        e_apo = -1 / rmax + p / (3 * rmax ** 3)
        rows.append(dict(p=p, x_apo=xa, x_apo_num=rmax, half_period=hp, half_period_num=tapo, eps0=eps_sudden(p), eps_apo=e_apo))
        good = abs(rmax / xa - 1) < 2e-3 and abs(tapo / hp - 1) < 2e-3 and abs(e_apo / eps_sudden(p) - 1) < 2e-3
        ok &= good
        P(f"  p {p}: x_apo {xa:.4f} (num {rmax:.4f}); half period {hp:.4f} (num {tapo:.4f}); eps(apo) {e_apo:.5f} vs eps(0) {eps_sudden(p):.5f}: {'PASS' if good else 'FAIL'}")
    # marginal case p = 3: v^2 = 2 (r^2 - 1) / r^3 along the whole trajectory
    r, v, t, rmax, _ = single_shell(3.0, tmax=60.0, dt=2e-4, stop_at_apo=False)
    v2_formula = 2 * (r ** 2 - 1) / r ** 3
    good3 = abs(v * v / v2_formula - 1) < 2e-3 and r > 5
    ok &= good3
    P(f"  p 3 (E = 0): at t 60, r {r:.3f}, v^2 {v * v:.5f} vs 2(r^2-1)/r^3 {v2_formula:.5f}: {'PASS' if good3 else 'FAIL'}")
    r, v, t, rmax, _ = single_shell(3.4, tmax=300.0, dt=2e-4, stop_at_apo=False)
    good34 = (v > 0) and (r > 20)
    ok &= good34
    P(f"  p 3.4 (E > 0): r(300) {r:.2f}, v {v:.4f} > 0: {'PASS' if good34 else 'FAIL'}")
    OUT.update(rows=rows, all_pass=ok)
    P(f"PART A all pass: {ok}")

elif PART == "B":
    P("PART B: adiabatic ramp, single shell mu = 1 released at the equilibrium of the peak mass; final energy vs -2/(3 mu) and the sudden value")
    res = []
    T_end = math.pi * math.sqrt(2.0)                   # small-oscillation period at q = 1, mu = 1
    for p in (1.5, 3.0, 5.6, 10.0):
        eps_sud = -(3 - p) * math.sqrt(p) / 3.0         # mu = 1: eps = -(3-p) sqrt(p) / (3 mu)
        for mult in (0.0, 0.1, 1.0, 10.0, 100.0, 1000.0):
            tau = mult * T_end
            dt = 2e-3
            r = 1.0 / math.sqrt(p)
            v = 0.0
            t = 0.0
            nsteps = int((tau + 6 * T_end) / dt)
            for n in range(nsteps):
                q = 1.0 if (tau == 0 or t >= tau) else p + (1.0 - p) * (t / tau)
                a = -q / r ** 2 + 1.0 / r ** 4
                v += 0.5 * dt * a
                r += dt * v
                t += dt
                q = 1.0 if (tau == 0 or t >= tau) else p + (1.0 - p) * (t / tau)
                a = -q / r ** 2 + 1.0 / r ** 4
                v += 0.5 * dt * a
            eps = 0.5 * v * v - 1.0 / r + 1.0 / (3 * r ** 3)
            nu = tau * p ** 0.75                        # nu = tau / r0^(3/2), r0 = mu / sqrt(p) = 1 / sqrt(p) (DERIVATION.md 4.3)
            res.append(dict(p=p, f_loss=1 - 1 / p, tau_over_T=mult, nu=nu, eps_final=eps, eps_adiabatic=-2.0 / 3.0, eps_sudden=eps_sud, r_final=r,
                            unbound=bool(eps >= 0)))
            P(f"  p {p:5.2f} tau/T {mult:7.1f} nu {nu:9.2f}: eps {eps:+.4f} (adiabatic -0.6667, sudden {eps_sud:+.4f}); r {r:.3f}; unbound {eps >= 0}")
    OUT["rows"] = res

elif PART == "C":
    import numpy as np
    P("PART C: rank-shell population (CFG776 integrator) with unbound mass counted by rank energy eps_i = v^2/2 - 1/r + mu_i^2/(3 r^3) > 0")
    N, RMIN, DT, CORE = 4000, 0.5, 0.005, 0.5
    TEND = float(os.environ.get("CFG837_TEND", "1000"))
    EDGES = {"cfg776_R0_50": lambda p: 50.0, "physical_edge_5.364_sqrt_p": lambda p: 5.364 * math.sqrt(p)}

    def accel(r, dm):
        order = np.argsort(r)
        rs = r[order]
        m_in = CORE + dm * np.arange(N)
        a_s = -1 / rs ** 2 + ((m_in + dm) ** 3 - m_in ** 3) / (3 * dm * rs ** 4)
        a = np.empty(N)
        a[order] = a_s
        return a

    def energy(r, v, dm):
        rs = np.sort(r)
        m_in = CORE + dm * np.arange(N)
        m_out = m_in + dm
        E = 0.5 * dm * np.sum(v ** 2) - dm * np.sum(1 / rs)
        E += (CORE ** 3) * (RMIN ** -3 - rs[0] ** -3) / 9
        E += np.sum(m_out[:-1] ** 3 * (rs[:-1] ** -3 - rs[1:] ** -3)) / 9 + m_out[-1] ** 3 * rs[-1] ** -3 / 9
        return float(E)

    def rank_energy(r, v, dm):
        order = np.argsort(r)
        mu = np.empty(N)
        mu[order] = CORE + dm * (np.arange(N) + 0.5)
        return 0.5 * v ** 2 - 1 / r + mu ** 2 / (3 * r ** 3)

    res = []
    for ename, edge in EDGES.items():
        for p in (1.5, 2.0, 3.0, 5.6, 10.0):
            R0 = edge(p)
            if R0 <= RMIN + 1:
                continue
            mtot = math.sqrt(p) * (R0 - CORE)
            dm = mtot / N
            q = (np.arange(N) + 0.5) / N
            r = RMIN + q * (R0 - RMIN)
            v = np.zeros(N)
            e_rank0 = rank_energy(r, v, dm)
            E0 = energy(r, v, dm)
            a = accel(r, dm)
            for n in range(int(TEND / DT)):
                v += 0.5 * DT * a
                r += DT * v
                low = r < RMIN
                r[low] = 2 * RMIN - r[low]
                v[low] = -v[low]
                a = accel(r, dm)
                v += 0.5 * DT * a
            E1 = energy(r, v, dm)
            er = rank_energy(r, v, dm)
            u_unb = float(np.sum(er > 0) * dm / (mtot + CORE))
            u_far = float(np.sum(r > 1000) * dm / (mtot + CORE))
            rs = np.sort(r)
            mr = [float((CORE + dm * np.searchsorted(rs, R)) / R) for R in (2.0, 5.0, 8.0, 11.0, 25.0) if R < R0]
            fl = 1 - 1 / p
            dE = abs(E1 - E0) / abs(E0) if E0 != 0 else float("nan")
            res.append(dict(edge=ename, p=p, f_loss=fl, R0=R0, u_rank_energy_positive=u_unb, u_beyond_1000=u_far,
                            F_dyn=u_unb / fl, E_init_rank_sum=float(np.sum(e_rank0) * dm), dE_rel=dE, m_over_r=mr))
            P(f"  {ename:28s} p {p:5.2f} f_loss {fl:.3f}: u(eps>0) {u_unb:.3f}, u(r>1000) {u_far:.3f}, F_dyn {u_unb / fl:.3f}, dE/E {dE:.1e}"
              f"{'  [UNRESOLVED: dE/E > 1e-3]' if dE > 1e-3 else ''}")
    OUT["rows"] = res
else:
    sys.exit("CFG837_PART must be A, B or C")

open(os.path.join(HERE, f"cfg837_part{PART}.out"), "w").write("\n".join(LINES) + "\n")
json.dump(OUT, open(os.path.join(HERE, f"cfg837_part{PART}_results.json"), "w"), indent=1)
