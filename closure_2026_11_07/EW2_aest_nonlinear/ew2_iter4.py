#!/usr/bin/env python3
"""EW2 iter_4 (criteria iter_4_static_recheck/FROZEN_CRITERIA.md, local 869b3d72ad / origin 041be83e4a):
SPARC, Cassini (mass-term part; v3s part read from C6P), c_T (read), galaxy lensing (iter_1 KA1) on v4's equations.
    nice -n 15 python3 ew2_iter4.py        (the MUTATE is the AX1 AeST class run from a scratch copy: ew2_iter4_MUTATE_ax1_AeST_noGammaL.out)
kappa = 1/2 FITTED; not theory closed. Footings never pooled. 1 thread. Adopts nothing."""
import os, sys, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ew2_lib import *
D = os.path.join(HERE, "iter_4_static_recheck"); OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()
Q = load_qx10(); SP = Q["NS"]["SP"]
I2J = json.load(open(os.path.join(HERE, "iter_2_web_cmb_kids", "ew2_iter2.json")))
GM_SUN = 1.32712440018e20; AU = 1.495978707e11; R_SAT = 9.5826 * AU; PHI0 = (600e3) ** 2; SAT_BOUND, HEES = 7.0e-15, 9.0e-27
R = dict(lane="ew2_iter4", criteria="869b3d72ad / 041be83e4a", foot={})
P(f"EW2 iter_4 main. kappa = 1/2 FITTED; not theory closed. SPARC {len(SP)} galaxies, {sum(len(g['R']) for g in SP)} points")

def sparc(mu, a0):
    sh = []; bad = 0
    for g in SP:
        Mf = tabulated(g["R"], g["vb2"] * g["R"] / G); Mt = float(Mf(np.array([3 * MPC]))[0])
        pc = phi_c(Mf, Mt, a0, mu, [0.0]) if mu > 0 else np.zeros(1)
        r, gg, _ = solve(Mf, a0, mu, pc, 1.05 * g["R"].max() / MPC)
        ga = at(r, gg, g["R"])[:, 0]; gl = g_aqual(G * Mf(g["R"]) / g["R"] ** 2, a0)
        bad += int(np.sum(ga <= 0)); sh.append(np.log10(np.where(ga > 0, ga, np.nan) / gl))
    sh = np.concatenate(sh); rms = float(np.sqrt(np.nanmean(sh ** 2))); mean = float(np.nanmean(sh))
    return dict(rms=rms, mean=mean, n_nonpositive=bad, max_abs=float(np.nanmax(np.abs(sh))), pass_=bool(bad == 0 and rms <= 0.096 and abs(mean) <= 0.05))

def cassini(mu):
    m2 = (mu / MPC) ** 2; dg_self = m2 * GM_SUN / 2; dg_zero = m2 * PHI0 * R_SAT / 3; q2 = m2 * PHI0 / 3
    return dict(dg_self=dg_self, dg_zero=dg_zero, dg_total=dg_self + dg_zero, Q2=q2, pass_=bool(dg_self + dg_zero <= SAT_BOUND and q2 <= HEES))

# KA1 (SPARC at mu 1e-6) and KA2 (the Sun: solver D vs mu^2 M r^2/2)
k1 = sparc(1e-6, A0["canonical"]); R["KA1"] = dict(rms=k1["rms"], pass_=bool(k1["rms"] <= 1e-4)); P(f"KA1 mu 1e-6 SPARC rms shift {k1['rms']:.2e} -> {'PASS' if R['KA1']['pass_'] else 'FAIL'}")
mu_t = 1e8; Ms = GM_SUN / G; r0 = 0.01 * AU / MPC; Mf = lambda r: np.full_like(np.asarray(r, float), Ms)
r, gg, Dd = solve(Mf, A0["canonical"], mu_t, np.array([-GM_SUN / (r0 * MPC)]), 50 * AU / MPC, r0=r0, hmax=1e-3)
x = 50 * AU; num = float(at(r, Dd, np.array([x]))[0, 0]); ana = (mu_t / MPC) ** 2 * Ms * (x ** 2 - (r0 * MPC) ** 2) / 2
R["KA2"] = dict(solver=num, closed=ana, rel=abs(num / ana - 1), pass_=bool(abs(num / ana - 1) <= 1e-3))
P(f"KA2 Sun static dust at 50 AU (mu 1e8): solver {num:.6e} vs closed form {ana:.6e} kg (rel {abs(num/ana-1):.1e}) -> {'PASS' if R['KA2']['pass_'] else 'FAIL'}")

lens_ok = "8/8 checks PASS" in open(os.path.join(HERE, "iter_1_action_statement", "ew2_c1_replay.out")).read()
for f, a0 in A0.items():
    extra = [I2J["foot"][f]["mu_w"], I2J["foot"][f]["mu_h"]]
    rows = {}
    for mu in sorted(set([m for m in DECLARED if m <= 1e5] + [e for e in extra if e])):
        s = sparc(mu, a0); c = cassini(mu)
        rows[f"{mu:.6g}"] = dict(mu=mu, SPARC=s, Cassini=c, c_T="PASS [read: tensor modes couple only through R]", lensing="PASS [iter_1 KA1]" if lens_ok else "NOT EVALUABLE")
    for mu in [m for m in DECLARED if m > 1e5]:
        c = cassini(mu); rows[f"{mu:.6g}"] = dict(mu=mu, SPARC=dict(pass_=not (mu * 0.03 > 12.3), how="bound H-inf (iter_2) at R = 30 kpc; numerically infeasible (> 1e7 steps)", muR=mu * 0.03),
                                                 Cassini=c, c_T="PASS [read]", lensing="PASS [iter_1 KA1]" if lens_ok else "NOT EVALUABLE")
    R["foot"][f] = dict(rows=rows, mu_w=extra[0], mu_h=extra[1])
    P(f"\n[{f}] member (mu /Mpc): SPARC rms/mean shift dex | Cassini dg(Saturn) m/s^2, Q2 s^-2 (v3s part: C6P PASS, read) | c_T | lensing")
    for k, v in rows.items():
        s = v["SPARC"]; c = v["Cassini"]
        ss = (f"rms {s['rms']:.4f} mean {s['mean']:+.4f}{'' if s['n_nonpositive'] == 0 else ' (%d pts g<=0)' % s['n_nonpositive']}" if "rms" in s else f"bound mu R(30 kpc) {s['muR']:.3g} > 12.3")
        tag = (" [mu_w]" if v["mu"] == extra[0] else "") + (" [mu_h]" if v["mu"] == extra[1] else "")
        P(f"  mu {v['mu']:<8.4g}{tag}: SPARC {ss} -> {'PASS' if s['pass_'] else 'FAIL'} | Cassini dg {c['dg_total']:.2e} (line {SAT_BOUND:.1e}), Q2 {c['Q2']:.1e} (line {HEES:.0e}) -> {'PASS' if c['pass_'] else 'FAIL'} | c_T PASS [read] | lensing {v['lensing'].split()[0]}")
R["MUTATE"] = "AX1 engine, class AeST (no gamma_L), scratch copy: output identical to rebuild_2026_10_22/AX1_action_for_law/AeST/ax1_AeST.out; Q2/Hees 2.44-4.55 (canonical AQUAL) / 2.85-5.15 (alt): Cassini FAIL in every cell -> bites"
P("\nMUTATE (drop gamma_L, plain AeST): " + R["MUTATE"])
R["runtime_s"] = time.time() - T0
json.dump(R, open(os.path.join(D, "ew2_iter4.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else float(o)))
open(os.path.join(D, "ew2_iter4.out"), "w").write("\n".join(OUT) + "\n")
P(f"runtime {time.time()-T0:.0f} s")
