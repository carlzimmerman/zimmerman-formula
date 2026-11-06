#!/usr/bin/env python3
"""QX10 iter_2 time-dependent heating run (FROZEN_CRITERIA.md c1f0cadb7a, AMENDMENT_A1.md 168db297bd).
1D Lagrangian spherical barotropic hydro, p = K(t) rho^2 + von Neumann-Richtmyer q, leapfrog, host baryons static at
their z = 0 profile, a0 law on: g = glaw(G (M_b(<r) + M_d(<r))/r^2). Start z_s (lambda_J(z_s)/2 = 10 kpc) from the
static A equilibrium; evolve to z = 0. Hosts: reference galaxy, X-COP median-Mb_last cluster; cells C1, C2; both
footings; 200 and 400 shells. Known answers KA3 (perturbed Lane-Emden, K fixed, Newton) and KA4 (static hold).
  python3 qx10_i2_hydro.py -> qx10_i2_hydro.json/.out
kappa = 1/2 FITTED; not theory closed. Units kpc, Msun, km/s; time unit kpc/(km/s) = 0.9778 Gyr."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
argv0 = sys.argv; sys.argv = [argv0[0]]
import qx10_i2 as S                                   # static solver, hosts, constants (no grading runs on import)
sys.argv = argv0
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

GK, glaw = S.GK, S.glaw
H0 = 65.0 / 1e3                                        # km/s/kpc
h = 0.65; OM = (S.OB + S.OD) / h ** 2; ORAD = 4.1834e-5 / h ** 2; OL = 1 - OM - ORAD
def E(a): return math.sqrt(ORAD / a ** 4 + OM / a ** 3 + OL)
def ode(a): return OL / E(a) ** 2
def t_of(a): return quad(lambda x: 1 / (x * H0 * E(x)), 1e-8, a, limit=200)[0]
OD0 = ode(1.0)
def lamJ(a, l0, p): return l0 * (ode(a) / OD0) ** p             # kpc, physical
def K_t(a, l0, p): return GK * lamJ(a, l0, p) ** 2 / (2 * math.pi)


def a_of_t_table():
    aa = np.geomspace(0.05, 1.0, 4000); tt = np.array([t_of(x) for x in aa]); return aa, tt
AA, TT = a_of_t_table()
def a_of(t): return float(np.interp(t, TT, AA))


def shells_from_static(sol, N):
    Md = sol["Md"]; r = sol["r"]; Mt = Md[-1]
    targets = Mt * np.arange(1, N + 1) / N
    rr = np.interp(targets, Md, r); rr[-1] = sol["Rs"]
    return np.concatenate([[0.0], rr]), Mt / N


def run(Mb_fn, sol0, N, l0, p, a0k, a_start, a_end=1.0, freeze_K=None, law=True, host=True, t_span=None, rec_R=None):
    r, dm = shells_from_static(sol0, N); v = np.zeros(N + 1); m_in = dm * np.arange(N + 1)
    Mb = (lambda x: np.array([Mb_fn(y) for y in x])) if host else (lambda x: np.zeros_like(x))
    # baryon profile on a fine log table for speed
    tab_r = np.geomspace(1e-3, 1e5, 3000); tab_M = np.array([Mb_fn(y) for y in tab_r]) if host else np.zeros(3000)
    def Mbar(x): return np.interp(np.log(np.maximum(x, 1e-3)), np.log(tab_r), tab_M)
    t0 = t_of(a_start); t1 = t_of(a_end) if t_span is None else t0 + t_span
    t = t0; Cq = 2.0; steps = 0; hist = []
    def accel(r, v, t):
        K = freeze_K if freeze_K is not None else K_t(a_of(t), l0, p)
        vol = 4 * math.pi / 3 * (r[1:] ** 3 - r[:-1] ** 3); rho = dm / vol
        dv = v[1:] - v[:-1]; q = np.where(dv < 0, Cq ** 2 * rho * dv ** 2, 0.0)
        Pr = K * rho ** 2 + q; Pn = np.concatenate([Pr, [0.0]])
        ri = r[1:]; gN = GK * (Mbar(ri) + m_in[1:]) / ri ** 2
        g = glaw(gN, a0k) if law else gN
        dmavg = np.concatenate([0.5 * (dm + dm) * np.ones(N - 1), [0.5 * dm]])
        acc = -4 * math.pi * ri ** 2 * (Pn[1:] - Pn[:-1]) / dmavg - g
        cs = np.sqrt(2 * K * rho)
        dt = 0.25 * float(np.min((r[1:] - r[:-1]) / (cs + np.abs(dv) + 1e-30)))
        dt = min(dt, 0.02 * float(np.min(np.sqrt(ri / np.maximum(g, 1e-30)))))
        return np.concatenate([[0.0], acc]), dt
    acc, dt = accel(r, v, t)
    while t < t1 and steps < 3_000_000:
        dt = min(dt, t1 - t)
        v_half = v + 0.5 * dt * acc; r = r + dt * v_half; r[0] = 0.0
        if np.any(np.diff(r) <= 0): return dict(ok=False, reason="shell crossing", t=t, steps=steps)
        t += dt; acc, dtn = accel(r, v_half, t); v = v_half + 0.5 * dt * acc; dt = dtn; steps += 1
        if rec_R is not None and steps % 20 == 0: hist.append((t, float(np.interp(0.5, m_in / m_in[-1], r))))
    return dict(ok=True, r=r, v=v, dm=dm, m_in=m_in, steps=steps, t=t, hist=hist)


def M_inside(res, x):
    return float(np.interp(x, res["r"], res["m_in"]))


def main():
    P("QX10 iter_2 time-dependent heating run (A1: start where lambda_J/2 = 10 kpc, from the static equilibrium).")
    P("kappa = 1/2 FITTED; not theory closed. Host baryons static at z = 0 (stated approximation).")
    RES = dict(lane="QX10 iter_2 hydro", criteria="c1f0cadb7a", amendment="168db297bd", note="kappa = 1/2 FITTED; not theory closed")
    # KA3: perturbed Lane-Emden, Newton, no host, K fixed
    lam = 100.0; K = S.K_of(lam); s0 = S.solve_static(S.pointmass(0.0), 1e10, K, 5 * lam, 1.0, law=False, host=False, n=4000)
    sol = dict(s0); sol["r"] = s0["r"] * 1.1; sol["Rs"] = s0["Rs"] * 1.1           # stretched 10 %
    rhm_LE = float(np.interp(0.5 * s0["Md"][-1], s0["Md"], s0["r"]))
    tsc = (lam / 2) / math.sqrt(2 * K * float(s0["rho"][0]))
    out = run(S.pointmass(0.0), sol, 200, lam, 0.0, 1.0, 1.0, freeze_K=K, law=False, host=False, t_span=10 * tsc, rec_R=True)
    if out["ok"]:
        hh = np.array([x for x in out["hist"] if x[0] - out["hist"][0][0] >= 5 * tsc]); mean_rh = float(hh[:, 1].mean())
        RES["KA3"] = dict(rhalf_LE=rhm_LE, rhalf_mean_late=mean_rh, rel=mean_rh / rhm_LE - 1, pass_=bool(abs(mean_rh / rhm_LE - 1) <= 0.05), steps=out["steps"])
    else:
        RES["KA3"] = dict(pass_=False, reason=out["reason"])
    P(f"KA3 perturbed Lane-Emden (x1.1, K fixed, Newton): late mean half-mass radius / LE {1 + RES['KA3'].get('rel', float('nan')):.4f} -> {'PASS' if RES['KA3']['pass_'] else 'FAIL'}")
    # hosts
    clus = sorted(S.clusters.items(), key=lambda kv: kv[1][0]["Mb_last"][0]); cname, cpts = clus[len(clus) // 2]
    Ml, rl = cpts[0]["Mb_last"]; chost = S.profile_from([q["r_kpc"] for q in cpts], [q["M_b"] for q in cpts], Ml, rl)
    R500 = max(q["r_kpc"] for q in cpts) / 0.7
    HOSTS = {"reference": (S.expdisc(1e10, 10.0), 1e10, 10.0), f"X-COP {cname}": (chost, Ml, 0.5 * R500)}
    RES["runs"] = {}; RES["KA4"] = {}
    for c in ("C1", "C2"):
        l0, p = S.CELLS[c]; l0k = l0 * 1e3
        a_s = brentq(lambda a: lamJ(a, l0k, p) / 2 - 10.0, 0.05, 1.0) if lamJ(1.0, l0k, p) / 2 > 10.0 else 1.0
        for f, a0k in S.A0K.items():
            for hn, (hfn, Mbt, Rref) in HOSTS.items():
                Mt = S.FCAP * S.R * Mbt; rta = S.r_ta(Mbt)
                st0 = S.solve_static(hfn, Mt, K_t(a_s, l0k, p), rta, a0k, n=4000)
                stA = S.solve_static(hfn, Mt, K_t(1.0, l0k, p), rta, a0k, n=4000)
                A_val = S.Mdust_at(stA, Rref)
                key = f"{c} {f} {hn}"; row = dict(z_s=1 / a_s - 1, static_A_M_Rref=A_val, static_A_retained=stA["retained"], Mt=Mt, Mb=Mbt, R_ref=Rref, r_ta=rta)
                # KA4 static hold (400 shells, 5 sound-crossing times)
                if c == "C1":
                    Kz = K_t(a_s, l0k, p); rc0 = float(st0["rho"][0]); tsc = st0["Rs"] / math.sqrt(2 * Kz * max(rc0, 1e-300))
                    h4 = run(hfn, st0, 400, l0k, p, a0k, a_s, freeze_K=Kz, t_span=5 * tsc)
                    if h4["ok"]:
                        m0 = S.Mdust_at(st0, Rref); m1 = M_inside(h4, Rref)
                        RES["KA4"][f"{f} {hn}"] = dict(M0=m0, M1=m1, rel=(m1 - m0) / max(m0, 1e-300), pass_=bool(abs(m1 - m0) <= 0.01 * max(m0, 1e-6 * Mt)), steps=h4["steps"])
                    else:
                        RES["KA4"][f"{f} {hn}"] = dict(pass_=False, reason=h4["reason"])
                    k4 = RES["KA4"][f"{f} {hn}"]
                    P(f"KA4 static hold {f} {hn}: {'rel %+.2e' % k4['rel'] if 'rel' in k4 else k4.get('reason')} -> {'PASS' if k4['pass_'] else 'FAIL'}")
                vals = {}
                for N in (200, 400):
                    rr = run(hfn, st0, N, l0k, p, a0k, a_s)
                    if rr["ok"]:
                        vals[N] = dict(M_Rref=M_inside(rr, Rref), M_beyond_rta=float(rr["m_in"][-1] - np.interp(rta, rr["r"], rr["m_in"])) if rr["r"][-1] > rta else 0.0,
                                       R_outer=float(rr["r"][-1]), steps=rr["steps"])
                    else:
                        vals[N] = dict(failed=rr["reason"], steps=rr["steps"])
                row["runs"] = vals
                ok2 = all("M_Rref" in vals[N] for N in vals)
                if ok2:
                    m2, m4 = vals[200]["M_Rref"], vals[400]["M_Rref"]
                    row["converged"] = bool(abs(m2 - m4) <= 0.10 * max(m4, 1e-6 * Mt) or (m2 < 0.01 * Mbt and m4 < 0.01 * Mbt))
                    row["D_consistent"] = bool(abs(m4 - A_val) <= 0.20 * max(A_val, 1e-300) or (m4 < 0.01 * Mbt and A_val < 0.01 * Mbt))
                else:
                    row["converged"] = False; row["D_consistent"] = False
                RES["runs"][key] = row
                P(f"{key}: z_s {row['z_s']:.3f}; static A M_d(<{Rref:.0f} kpc) {A_val:.3e} (retained {stA['retained'] / Mt:.3f} of {Mt:.2e}); "
                  + "; ".join(f"N={N}: " + (f"M {vals[N]['M_Rref']:.3e}, beyond r_ta {vals[N]['M_beyond_rta']:.2e}, R_out {vals[N]['R_outer']:.0f} kpc, {vals[N]['steps']} steps" if "M_Rref" in vals[N] else f"FAILED {vals[N]['failed']}") for N in vals)
                  + f"; converged {row['converged']}, D-consistent {row['D_consistent']}")
    json.dump(RES, open(os.path.join(HERE, "qx10_i2_hydro.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "qx10_i2_hydro.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
