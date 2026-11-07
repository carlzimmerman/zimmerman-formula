#!/usr/bin/env python3
"""EW2 iter_3 (criteria iter_3_clusters_beyond_hydrostatic/FROZEN_CRITERIA.md, local 869b3d72ad / origin 041be83e4a):
A. static (hydrostatic) branch of v4 on X-COP and Lovisari groups; B. the dust branch's reach (gate DB).
    nice -n 15 python3 ew2_iter3.py [--mutate]      (MUTATE: M1 K2 -> 0, M2 positive control)
kappa = 1/2 FITTED; not theory closed. Footings never pooled. 1 thread. Adopts nothing."""
import os, sys, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ew2_lib import *
MUT = "--mutate" in sys.argv; TAG = "ew2_iter3" + ("_MUTATE" if MUT else ""); D = os.path.join(HERE, "iter_3_clusters_beyond_hydrostatic")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()
Q = load_qx10(); XC, GR, profile_from = Q["XC"], Q["GR"], Q["profile_from"]
I2J = json.load(open(os.path.join(HERE, "iter_2_web_cmb_kids", "ew2_iter2.json")))
CL = {}
for z in XC: CL.setdefault(z["name"], []).append(z)
DEL = np.round(np.arange(-8, 2.0001, 0.25), 4); I0 = int(np.argmin(np.abs(DEL)))
def mfun(host): fv = np.vectorize(host); return lambda r: fv(np.asarray(r, float) / KPC) * MSUN
def gN_needed(gobs, a0): return gobs ** 2 / (gobs + a0)          # inverse of g_AQUAL

def systems(fst_list=(0.0, 1.0)):
    S = []
    for nm, pts in CL.items():
        Ml, rl = pts[0]["Mb_last"]; host = profile_from([p["r_kpc"] for p in pts], [p["M_b"] for p in pts], Ml, rl)
        S.append(dict(kind="X", name=nm, Mf=mfun(host), pts=[dict(r=p["r_kpc"] * KPC, Mobs=p["M_obs"] * MSUN, Mb=p["M_b"] * MSUN, eM=p["eM"] * MSUN) for p in pts]))
    for fst in fst_list:
        for gp in GR:
            Mbt = gp["g5"] * (1 + fst); host = profile_from([q["r_kpc"] for q in gp["pts"]], [q["M_gas"] * (1 + fst) for q in gp["pts"]], Mbt, gp["R5"])
            S.append(dict(kind=f"G{fst:g}", name=gp["name"], Mf=mfun(host), pts=[dict(r=q["r_kpc"] * KPC, Mobs=q["M_obs"] * MSUN, Mb=q["M_gas"] * (1 + fst) * MSUN, eM=q["eM"] * MSUN) for q in gp["pts"]]))
    return S
SYS = systems()

def grade(mu, a0, Dl=(0.0,), control=False):
    """D_i = log10(M_obs/M_AeST) per Delta; X-COP and groups gates (QX10 lines) at Delta = 0 (index of 0 in Dl)."""
    Dl = np.asarray(Dl, float); i0 = int(np.argmin(np.abs(Dl))); res = {"X": [], "G0": {}, "G1": {}}; dust = []
    for s in SYS:
        x = np.array([p["r"] for p in s["pts"]]); Mobs = np.array([p["Mobs"] for p in s["pts"]])
        if control:     # M2: baryons replaced by the mass the law needs to return M_obs at each point
            gN = gN_needed(G * Mobs / x ** 2, a0); M = gN * x ** 2 / G; Mf = tabulated(x, M)
        else:
            Mf = s["Mf"]
        Mt = float(Mf(np.array([3.0 * MPC]))[0])
        pc = phi_c(Mf, Mt, a0, mu, Dl) if mu > 0 else np.zeros(len(Dl))
        r, g, Dd = solve(Mf, a0, mu, pc, max(3.2, 1.05 * x.max() / MPC))
        ga = at(r, g, x); Ma = ga * x[:, None] ** 2 / G
        Dv = np.log10(Mobs[:, None] / np.where(Ma > 0, Ma, np.nan))
        if s["kind"] == "X":
            res["X"].append(Dv)
            dd = at(r, Dd, x[-1:])[0, i0]; dust.append(dict(name=s["name"], r_kpc=x[-1] / KPC, dust_over_Mb=float(dd / s["pts"][-1]["Mb"]),
                                                           need_over_Mb=float(gN_needed(G * Mobs[-1] / x[-1] ** 2, a0) * x[-1] ** 2 / G / s["pts"][-1]["Mb"] - 1)))
        else:
            eM = np.array([p["eM"] for p in s["pts"]]); tol = 2 * eM / (Mobs * math.log(10))
            res[s["kind"]][s["name"]] = np.all(np.abs(Dv) <= tol[:, None], axis=0)   # nan -> False
    Xd = np.concatenate(res["X"], 0); mX = np.nanmean(Xd, 0); rX = np.sqrt(np.nanmean(Xd ** 2, 0)); finite = np.all(np.isfinite(Xd), 0)
    Xpass = finite & (np.abs(mX) <= 0.05) & (rX <= 0.10)
    g0 = np.sum([v for v in res["G0"].values()], 0); g1 = np.sum([v for v in res["G1"].values()], 0); Gpass = (g0 >= 16) & (g1 >= 16)
    return dict(X_mean=mX, X_rms=rX, X_finite=finite, X_pass=Xpass, groups_fst0=g0, groups_fst1=g1, groups_pass=Gpass, n_groups=len(res["G0"]), dust=dust, i0=i0)

R = dict(lane=TAG, criteria="869b3d72ad / 041be83e4a", foot={}, n_xcop_pts=sum(len(s["pts"]) for s in SYS if s["kind"] == "X"), n_groups=len(GR))
P(f"EW2 iter_3 {'MUTATE' if MUT else 'main'}. kappa = 1/2 FITTED; not theory closed. X-COP {R['n_xcop_pts']} points in {len(CL)} clusters; groups {len(GR)}")
if not MUT:
    k = {}
    for f, a0 in A0.items():
        o = grade(1e-6, a0); k[f] = dict(X_mean=float(o["X_mean"][0]), G_fst0_mean=None)
    # groups plain-law mean at fst 0 (QX20's G0 key), direct
    for f, a0 in A0.items():
        d = []
        for gp in GR:
            for q in gp["pts"]:
                rm = q["r_kpc"] * KPC; Mb = q["M_gas"] * MSUN; gl = g_aqual(G * Mb / rm ** 2, a0); d.append(math.log10(q["M_obs"] * MSUN / (gl * rm ** 2 / G)))
        k[f]["G_fst0_mean"] = float(np.mean(d))
    ref = {"canonical": (0.467499, 0.358644), "alt": (0.434523, 0.320274)}
    R["KA1"] = dict(rows=k, ref=ref, pass_=bool(all(abs(k[f]["X_mean"] - ref[f][0]) <= 1e-3 and abs(k[f]["G_fst0_mean"] - ref[f][1]) <= 1e-3 for f in A0)))
    P("KA1 mu 1e-6 plain law: " + "; ".join(f"{f} X {k[f]['X_mean']:.6f} (QX20 {ref[f][0]}), groups fst0 {k[f]['G_fst0_mean']:.6f} (QX20 {ref[f][1]})" for f in A0) + f" -> {'PASS' if R['KA1']['pass_'] else 'FAIL'}")
    s0 = [s for s in SYS if s["kind"] == "X"][0]; a0 = A0["canonical"]; Mf = s0["Mf"]; Mt = float(Mf(np.array([3 * MPC]))[0]); mu = 0.3
    r, g, Dd, Ph = solve(Mf, a0, mu, phi_c(Mf, Mt, a0, mu, [0.0]), 3.2, retphi=True)
    R5 = s0["pts"][-1]["r"]; m = r <= R5; from scipy.integrate import simpson
    k5 = int(np.searchsorted(r, R5)); m = slice(0, k5 + 1); integ = -(mu / MPC) ** 2 / G * simpson(Ph[m, 0] * r[m] ** 3, x=np.log(r[m])); dd = Dd[k5, 0]
    rel = abs(integ / dd - 1); R["KA2"] = dict(D_solver=float(dd), D_trapz=float(integ), rel=float(rel), pass_=bool(rel <= 1e-6))
    P(f"KA2 dust bookkeeping ({s0['name']}, mu 0.3, R {R5/KPC:.0f} kpc): solver {dd:.6e} vs trapezoid {integ:.6e} kg (rel {rel:.1e}; line 1e-6; Simpson in ln r on the solver's nodes, read at node r {r[k5]/KPC:.1f} kpc) -> {'PASS' if rel <= 1e-6 else 'FAIL'}")

MUS = [m for m in DECLARED if m <= 1e3]
MAPV = [m for m in MAP if m <= 1e3]
for f, a0 in A0.items():
    rows = {}
    if MUT:
        for mu in (0.1, 1.0, 10.0):
            m1 = grade(0.0, a0); main = grade(mu, a0); m2 = grade(0.0, a0, control=True)   # M2: the law (no mass term) on the needed mass
            rows[f"{mu:g}"] = dict(M1_X_mean=float(m1["X_mean"][0]), main_X_mean=float(main["X_mean"][0]), M1_X_pass=bool(m1["X_pass"][0]),
                                   M2_X_mean=float(m2["X_mean"][0]), M2_X_pass=bool(m2["X_pass"][0]))
            P(f"[{f}] mu {mu:g}: M1 (K2 -> 0) X mean {m1['X_mean'][0]:+.4f} -> {'PASS' if m1['X_pass'][0] else 'FAIL'} (main {main['X_mean'][0]:+.4f}); "
              f"M2 positive control X mean {m2['X_mean'][0]:+.2e} -> {'PASS' if m2['X_pass'][0] else 'FAIL'}")
        R["foot"][f] = rows; continue
    for mu in sorted(set(MUS + MAPV)):
        Dl = DEL if mu in MUS else [0.0]; o = grade(mu, a0, Dl); i0 = o["i0"]
        env = [float(d) for d, p_, q_ in zip(Dl, o["X_pass"], o["groups_pass"]) if p_ and q_] if len(Dl) > 1 else None
        envX = [float(d) for d, p_ in zip(Dl, o["X_pass"]) if p_] if len(Dl) > 1 else None
        rows[f"{mu:.6g}"] = dict(mu=mu, X_mean=float(o["X_mean"][i0]), X_rms=float(o["X_rms"][i0]), X_finite=bool(o["X_finite"][i0]), X_pass=bool(o["X_pass"][i0]),
                                 groups_fst0=int(o["groups_fst0"][i0]), groups_fst1=int(o["groups_fst1"][i0]), groups_pass=bool(o["groups_pass"][i0]),
                                 Delta_passing_both=env, Delta_passing_X=envX, dust=o["dust"] if mu in MUS else None, declared=bool(mu in MUS))
    # gate DB at host-compatible members (iter_2 G6, Delta = 0) and at every declared member
    host_ok = [v["mu"] for v in I2J["foot"][f]["rows"].values() if v["host"]["pass_"] and v["mu"] <= 1e3]
    xr = np.array([p["r"] for s in SYS if s["kind"] == "X" for p in s["pts"]]) / MPC
    db = {f"{mu:.6g}": dict(frac=float(np.mean(mu * xr >= 1.0)), pass_=bool(np.mean(mu * xr >= 1.0) >= 0.9)) for mu in sorted(set(host_ok + DECLARED))}
    dbh = [db[f"{mu:.6g}"] for mu in host_ok]
    R["foot"][f] = dict(rows=rows, DB=db, host_ok=host_ok, DB_any_host_ok=bool(any(x["pass_"] for x in dbh)), xcop_r_Mpc=[float(xr.min()), float(xr.max())])
    P(f"\n[{f}] declared members, Delta = 0 (X-COP mean/rms dex, groups passing fst0/fst1 of {len(GR)}), Delta envelope, static dust at the last X-COP point")
    for mu in MUS:
        x = rows[f"{mu:.6g}"]; dq = np.median([d_["dust_over_Mb"] for d_ in x["dust"]]); nq = np.median([d_["need_over_Mb"] for d_ in x["dust"]])
        P(f"  mu {mu:<6g}: X {x['X_mean']:+.3f}/{x['X_rms']:.3f}{'' if x['X_finite'] else ' (M_AeST<=0 somewhere)'} -> {'PASS' if x['X_pass'] else 'FAIL'}; groups {x['groups_fst0']}/{x['groups_fst1']} -> {'PASS' if x['groups_pass'] else 'FAIL'}; "
          f"Delta passing X: {x['Delta_passing_X'] or 'none'}, both: {x['Delta_passing_both'] or 'none'}; median static dust/M_b {dq:+.3g} vs need {nq:.3g}; DB frac {db[f'{mu:.6g}']['frac']:.2f}")
    xs = [(v["mu"], v["X_pass"], v["groups_pass"]) for v in rows.values()]
    P(f"[{f}] map (Delta = 0) mu:XG -> " + " ".join(f"{m:.3g}:{'X' if a else '-'}{'G' if b else '-'}" for m, a, b in xs))
    P(f"[{f}] gate DB at host-compatible members {['%.3g' % m for m in host_ok]}: max fraction of X-COP points with mu r >= 1 = {max([x['frac'] for x in dbh] or [0]):.3f} (line 0.9); X-COP r range {xr.min():.2f}-{xr.max():.2f} Mpc")
if not MUT:
    lab = {}
    for f in A0:
        A_pass = any(v["X_pass"] and v["groups_pass"] for v in R["foot"][f]["rows"].values())
        A_host = any(R["foot"][f]["rows"][f"{m:.6g}"]["X_pass"] and R["foot"][f]["rows"][f"{m:.6g}"]["groups_pass"] for m in R["foot"][f]["host_ok"] if f"{m:.6g}" in R["foot"][f]["rows"])
        lab[f] = ("PASS (A at a host-compatible member)" if A_host else ("NOT EVALUABLE (DB passes; past the fold not computed)" if R["foot"][f]["DB_any_host_ok"] else "FAIL")) + (f"; A passes at some member: {A_pass}")
    R["label"] = lab; P(f"\nLABEL iter_3: {lab}; past the fold: NOT EVALUABLE")
else:
    R["M1_bites"] = bool(any(abs(v["M1_X_mean"] - v["main_X_mean"]) > 1e-3 for f in A0 for v in R["foot"][f].values()))
    R["M2_bites"] = bool(all(v["M2_X_pass"] for f in A0 for v in R["foot"][f].values())); P(f"\nM1 bites: {R['M1_bites']}; M2 positive control passes: {R['M2_bites']}")
R["runtime_s"] = time.time() - T0
json.dump(R, open(os.path.join(D, TAG + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (None if o is None else (bool(o) if isinstance(o, np.bool_) else float(o))))
open(os.path.join(D, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
P(f"runtime {time.time()-T0:.0f} s")
