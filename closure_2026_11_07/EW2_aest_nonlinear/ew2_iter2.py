#!/usr/bin/env python3
"""EW2 iter_2 (criteria iter_2_web_cmb_kids/FROZEN_CRITERIA.md, local 869b3d72ad / origin 041be83e4a):
AeST's dust branch on the linear web (SV5 W1/W2), QX15 primary CMB (C7 read), KiDS hosts G6 (QX10 line).
    nice -n 15 python3 ew2_iter2.py [--mutate]
kappa = 1/2 FITTED; not theory closed. Footings never pooled. 1 thread. Adopts nothing."""
import os, sys, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ew2_lib import *
MUT = "--mutate" in sys.argv; TAG = "ew2_iter2" + ("_MUTATE" if MUT else ""); D = os.path.join(HERE, "iter_2_web_cmb_kids")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()
N3, sigA, AX0, S1 = load_web(); W = Web(N3, sigA, S1)
Q = load_qx10(); LE = Q["LE"]
R = dict(lane=TAG, criteria="869b3d72ad / 041be83e4a", sigma_A_rel=sigA, line_W1=3 * sigA, declared=DECLARED, map=MAP, foot={})
P(f"EW2 iter_2 {'MUTATE (K2 -> 0, mu = 0)' if MUT else 'main'}. kappa = 1/2 FITTED; not theory closed. sigma_A,rel {sigA:.4f} -> W1 line |r-1| <= {3*sigA:.4f}; W2 line {W.I2.DCHI2_LINE}")

# ---------------- known answers (web)
if not MUT:
    k1 = W.grade(1e12, "canonical"); k1a = W.grade(1e12, "alt")
    R["KA1"] = dict(r=[k1["r"], k1a["r"]], dchi2=[k1["dchi2"], k1a["dchi2"]], pass_=bool(max(abs(k1["r"] - 1), abs(k1a["r"] - 1), abs(k1["dchi2"]), abs(k1a["dchi2"])) <= 1e-6))
    P(f"KA1 mu 1e12 (all dust): r {k1['r']:.8f} / {k1a['r']:.8f}, dchi2 {k1['dchi2']:.2e} / {k1a['dchi2']:.2e} -> {'PASS' if R['KA1']['pass_'] else 'FAIL'}")
    ka2 = {}
    for f in A0:
        g_ = W.grade(1e-8, f); ref = S1["foot"][f]["proj"]["r"]; ka2[f] = dict(r=g_["r"], sv5=ref, rel=abs(g_["r"] / ref - 1))
    R["KA2"] = dict(rows=ka2, pass_=bool(all(v["rel"] <= 1e-3 for v in ka2.values())))
    P("KA2 mu 1e-8 (all band) vs SV5 iter_1 r: " + "; ".join(f"{f} {v['r']:.4g} vs {v['sv5']:.4g} (rel {v['rel']:.1e})" for f, v in ka2.items()) + f" -> {'PASS' if R['KA2']['pass_'] else 'FAIL'}")

# ---------------- hosts (G6)
bins = sorted(set(p["Mb"] for p in LE)); rLE = {Mb: np.array([math.sqrt(G * p["Mb"] / p["gbar"]) for p in LE if p["Mb"] == Mb]) for Mb in bins}
RMAX_LE = max(x.max() for x in rLE.values()) / MPC
DEL = np.round(np.arange(-8, 2.0001, 0.25), 4); I0 = int(np.argmin(np.abs(DEL)))
def g6(mu, a0, hmax=0.004, phase=0.08, Dl=DEL):
    """mean over LE points of log10(g_law/g_AeST), per Delta; and whether g_AeST > 0 at every LE radius."""
    sh = []; pos = np.ones(len(Dl), bool)
    for Mb in bins:
        Mf = hernquist(Mb); pc = phi_c(Mf, Mb, a0, mu, Dl) if mu > 0 else np.zeros(len(Dl)); r, g, _ = solve(Mf, a0, mu, pc, max(3.2, 1.05 * RMAX_LE), hmax=hmax, phase=phase)
        x = rLE[Mb]; ga = at(r, g, x); gl = g_aqual(G * Mf(x) / x ** 2, a0)
        pos &= np.all(ga > 0, axis=0); sh.append(np.log10(gl[:, None] / np.where(ga > 0, ga, np.nan)))
    sh = np.concatenate(sh, 0); m = np.nanmean(sh, 0); i0 = int(np.argmin(np.abs(np.asarray(Dl, float))))
    return m, pos, bool(np.isfinite(m[i0]) and abs(m[i0]) <= 0.05 and pos[i0])
def bound_fail(mu): return bool(mu * RMAX_LE > 12.3)       # H-inf (README), octave [R/2, R] at the largest LE radius

if not MUT:
    # KA3: H2's galaxy guard on H2's nodes (searchsorted read)
    Mg = 1e11 * MSUN; Mf = hernquist(Mg); a0 = A0["canonical"]; RGg = np.logspace(-5, np.log10(30), 4000)
    xn = np.array([RGg[np.searchsorted(RGg, 1.0)] * MPC]); ref = {0.1: (0.090, 0.003), 0.3: (-0.163, 0.016), 1.0: (-1.749, 0.086)}; ka3 = {}
    for mu, (d1, m2) in ref.items():
        pc = phi_c(Mf, Mg, a0, mu, [0.0]); r, g, _ = solve(Mf, a0, mu, pc, 30.0)
        dv1 = float(at(r, g, xn)[0, 0] / g_aqual(G * Mf(xn) / xn ** 2, a0)[0] - 1)
        rr = RGg[RGg <= 0.2] * MPC; dvm = float(np.max(np.abs(at(r, g, rr)[:, 0] / g_aqual(G * Mf(rr) / rr ** 2, a0) - 1)))
        ka3[str(mu)] = dict(dev_1Mpc=dv1, ref=d1, maxdev_200=dvm, ref200=m2, ok=bool(abs(dv1 - d1) <= 0.005 and abs(dvm - m2) <= 0.002))
    R["KA3"] = dict(rows=ka3, pass_=bool(all(v["ok"] for v in ka3.values())))
    P("KA3 H2 galaxy guard: " + "; ".join(f"mu {k}: dev1Mpc {v['dev_1Mpc']:+.4f} (H2 {v['ref']:+.3f}), max200 {v['maxdev_200']:.4f} (H2 {v['ref200']:.3f})" for k, v in ka3.items()) + f" -> {'PASS' if R['KA3']['pass_'] else 'FAIL'}")
    m, pos, _ = g6(1e-6, A0["canonical"]); m = m[I0:I0 + 1] if False else m; R["KA4"] = dict(G6=float(m[I0]), pass_=bool(abs(m[I0]) <= 1e-4)); P(f"KA4 mu 1e-6: G6 {m[I0]:+.2e} -> {'PASS' if R['KA4']['pass_'] else 'FAIL'}")
    ka5 = {}
    for mu in (0.3, 10.0):
        a, _, _ = g6(mu, A0["canonical"], Dl=[0.0]); b, _, _ = g6(mu, A0["canonical"], hmax=0.002, phase=0.04, Dl=[0.0]); ka5[str(mu)] = dict(G6=float(a[0]), G6_half=float(b[0]), d=float(abs(a[0] - b[0])))
    R["KA5"] = dict(rows=ka5, pass_=bool(all(np.isfinite(v["d"]) and v["d"] <= 1e-3 for v in ka5.values())))
    P("KA5 step halving: " + "; ".join(f"mu {k}: {v['G6']:+.5f} vs {v['G6_half']:+.5f}" for k, v in ka5.items()) + f" -> {'PASS' if R['KA5']['pass_'] else 'FAIL'}")

# ---------------- members and map
for f, a0 in A0.items():
    rows = {}
    for mu in (DECLARED if MUT else sorted(set(DECLARED + MAP))):
        mu_eff = 0.0 if MUT else mu
        wW = W.grade(None if MUT else mu, f, "W"); wF = W.grade(None if MUT else mu, f, "floor")
        if MUT:
            m, pos, ok = g6(0.0, a0, Dl=[0.0]); hostrow = dict(G6=float(m[0]), pos=bool(pos[0]), pass_=ok, how="solver")
        elif mu <= 1e3:
            m, pos, ok = g6(mu, a0); env = [float(d) for d, mm, pp in zip(DEL, m, pos) if np.isfinite(mm) and abs(mm) <= 0.05 and pp]
            hostrow = dict(G6=float(m[I0]), pos=bool(pos[I0]), pass_=ok, how="solver", Delta_passing=env)
        else:
            hostrow = dict(G6=None, pos=None, pass_=not bound_fail(mu), how="bound H-inf", muR=mu * RMAX_LE)
        rows[f"{mu:.6g}"] = dict(mu=mu, W=wW, floor=wF, host=hostrow, ksw_zstar=mu_eff / 1091.0, declared=bool(mu in DECLARED))
    mapv = [rows[f"{mu:.6g}"] for mu in (DECLARED if MUT else MAP)]
    webok = [x["W"]["W1"] and x["W"]["W2"] for x in mapv]; hostok = [x["host"]["pass_"] for x in mapv]
    MV = DECLARED if MUT else MAP
    mu_w = next((MV[i] for i in range(len(MV)) if all(webok[i:])), None)
    mu_h = None
    for i in range(len(MV)):
        if not hostok[i]: break
        mu_h = MV[i]
    both = [x["mu"] for x in rows.values() if x["W"]["W1"] and x["W"]["W2"] and x["host"]["pass_"]]
    R["foot"][f] = dict(rows=rows, mu_w=mu_w, mu_h=mu_h, members_passing_all=both)
    P(f"\n[{f}] declared members (mu /Mpc: W1 r, W2 dchi2 | floor r | G6 shift dex, g>0 | k_sw(z*) /Mpc)")
    for mu in DECLARED:
        x = rows[f"{mu:.6g}"]; h = x["host"]
        hs = (f"G6 {h['G6']:+.4f}{'' if h['pos'] else ' (g<=0 at an LE radius)'} -> {'PASS' if h['pass_'] else 'FAIL'}" if h["how"] == "solver" and h["G6"] is not None and np.isfinite(h["G6"])
              else (f"G6 undefined (g<=0) -> FAIL" if h["how"] == "solver" else f"bound: mu R_LE {h['muR']:.3g} > 12.3 -> {'FAIL [bound]' if not h['pass_'] else 'not excluded'}"))
        P(f"  mu {mu:<8g}: r {x['W']['r']:.4g} ({'P' if x['W']['W1'] else 'F'}), dchi2 {x['W']['dchi2']:.2f} ({'P' if x['W']['W2'] else 'F'}) | floor r {x['floor']['r']:.4g} | {hs} | k_sw(z*) {x['ksw_zstar']:.3g}")
    P(f"[{f}] map: mu_w (web passes from here up) = {mu_w}; mu_h (hosts pass up to here) = {mu_h}; members passing W1+W2+G6: {both if both else 'none'}")
    P(f"[{f}] map rows: " + " ".join(f"{x['mu']:.3g}:{'W' if (x['W']['W1'] and x['W']['W2']) else '-'}{'H' if x['host']['pass_'] else '-'}" for x in mapv))

if not MUT:
    ok_ka = all(R[k]["pass_"] for k in ("KA1", "KA2", "KA3", "KA4"))
    nogo = all(not R["foot"][f]["members_passing_all"] for f in A0)
    lab = "NOT EVALUABLE (known answer failed)" if not ok_ka else ("NO-GO FOR CLASS A_mu (web + KiDS)" if nogo else ("PASS at " + str({f: R['foot'][f]['members_passing_all'] for f in A0})))
    R["label"] = lab; R["QX15"] = "FAIL [C7 read: v4 runs away at linear order; not rerun]"; R["amount_I0"] = "NOT EVALUABLE as a prediction (initial datum, C2)"
    P(f"\nLABEL iter_2: {lab}; QX15 primary CMB: {R['QX15']}; dust amount: {R['amount_I0']}")
else:
    bites = any(R["foot"][f]["rows"][f"{mu:.6g}"]["W"]["W1"] is False for f in A0 for mu in DECLARED)
    allfail = all(not R["foot"][f]["rows"][f"{mu:.6g}"]["W"]["W1"] for f in A0 for mu in DECLARED)
    R["MUTATE_W1_fails_everywhere"] = bool(allfail); P(f"\nMUTATE: W1 fails at every member: {allfail} (bites iff the main run's W1 passes somewhere)")
R["runtime_s"] = time.time() - T0
json.dump(R, open(os.path.join(D, TAG + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (None if o is None else float(o)))
open(os.path.join(D, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
P(f"runtime {time.time()-T0:.0f} s")
