#!/usr/bin/env python3
"""SV3 grade: frozen lines (FROZEN_CRITERIA.md, 2febd29269) on parts/ and parts_MUTATE/, plus K0, K1, K2/K3, MUTATE-C.
Run from the repo root: nice -n 15 python3 action_search_2026_11_05/SV3_fold_implicit/grade.py
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, glob, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sv3
ac10 = sv3.ac10
CL = 2.99792458e8
load = lambda d: [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, d, "*.json")))
                  if "_N" not in os.path.basename(f)]
P = load("parts"); PM = load("parts_MUTATE")
out, chk = {}, {}
log = lambda s: print(s, flush=True)
N = 2000

# K0: Radau + E3 at gamma 0 vs AC10's DOP853
k0 = {}
soft = [r for r in ac10.physical_rows() if r["kind"] == "soft" and r["model"] == "v3s"][0]
for nm, (M1, Pi0, s2) in {"K1_zero_charge": (1.0, 0.0, 0.0), "soft_v3s_row": (soft["M1"], soft["Pi0"], 0.0)}.items():
    a = sv3.run(N, M1, Pi0, s2, 0.0)["t_fold"]; b = ac10.run(N, M1, Pi0, s2, 0.0)["t_fold"]
    k0[nm] = dict(sv3=a, ac10=b, rel=abs(a - b) / b)
chk["K0"] = all(v["rel"] <= 1e-6 for v in k0.values()); out["K0"] = k0
log(f"K0 {'PASS' if chk['K0'] else 'FAIL'} {k0}")

# K1
r = sv3.run(N, 1.0, 0.0, 0.0, 0.0, want_traj=True); q, dq, i1 = r["q"], r["dq"], r["i1"]; c = i1 - 1
def pair(t, y):
    x = y[:2]; return np.concatenate([y[2:], -0.5 * erf(x / (math.sqrt(2) * ac10.WB))])
def evp(t, y):
    return (y[1] - y[0]) / dq - ac10.JTHR
evp.terminal = True; evp.direction = -1
spr = solve_ivp(pair, (0, ac10.TMAX), [q[c], q[c + 1], 1.0, 1.0], method="DOP853", rtol=1e-12, atol=1e-14, events=evp, dense_output=True)
tp = float(spr.t_events[0][0]); xm = lambda t: 0.5 * (spr.sol(t)[0] + spr.sol(t)[1])
tc = brentq(xm, 0, tp); vc = 0.5 * (spr.sol(tc)[2] + spr.sol(tc)[3])
chk["K1"] = abs(r["t_fold"] - tp) <= 1e-6 and abs((tp - tc) / vc - 1) <= 0.02
out["K1"] = dict(t_coupled=r["t_fold"], t_pair=tp, delay_over_vcross=(tp - tc) / vc)
log(f"K1 {'PASS' if chk['K1'] else 'FAIL'} {out['K1']}")

# K2/K3 re-posed
rho_b = lambda x: np.exp(-x ** 2 / (2 * ac10.WB ** 2)) / (math.sqrt(2 * math.pi) * ac10.WB)
kk = {}
for tag, (Pi0, s2, thr) in {"A1_0.2": (0.2, 0.0, 1 / math.sqrt(2)), "A1_1.0": (1.0, 0.0, 1 / math.sqrt(2)),
                            "A2_0.4": (0.4, 0.4, 1.0), "A2_2.0": (2.0, 2.0, 1.0)}.items():
    rr = sv3.run(N, 1.0, Pi0, s2, 0.0, want_traj=True); so = rr["sol"]; c = rr["i1"] - 1
    tend = rr["t_fold"] if rr["t_fold"] is not None else ac10.TMAX
    va = lambda t: so.sol(t)[N + 1 + c]
    tg = np.linspace(0, tend, 4001); vv = np.array([va(t) for t in tg]); neg = np.where(vv < 0)[0]
    t_turn = float(tg[neg[0]]) if len(neg) else tend
    xmid = lambda t: 0.5 * (so.sol(t)[c] + so.sol(t)[c + 1])
    tcr = brentq(xmid, 0, t_turn)
    vcr = float(0.5 * (so.sol(tcr)[N + 1 + c] + so.sol(tcr)[N + 2 + c]))
    f = lambda t, y: [y[1], -rho_b(xmid(t)) * y[0] + (Pi0 - s2 * y[0])]
    evj = lambda t, y: y[0] - ac10.JTHR; evj.terminal = False; evj.direction = -1
    s2o = solve_ivp(f, (0, t_turn), [1.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-13, max_step=ac10.WB / 4,
                    dense_output=True, events=evj)
    Jn_f = lambda t: (so.sol(t)[c + 1] - so.sol(t)[c]) / dq
    tt = np.linspace(0, t_turn, 4001)
    Jn = np.array([Jn_f(t) for t in tt]); Jo = s2o.sol(tt)[0]
    m = Jo >= ac10.JREG
    agree = float(np.max(np.abs(Jn[m] - Jo[m]) / Jo[m]))
    pred = math.sqrt(Pi0) * vcr <= thr
    fpn = bool(Jn.min() <= ac10.JTHR * 1.01); fpo = len(s2o.t_events[0]) > 0
    tn = to = rel_t = None
    if fpn:
        k = int(np.where(Jn <= ac10.JTHR * 1.01)[0][0])
        tn = brentq(lambda t: Jn_f(t) - ac10.JTHR, tt[max(k - 50, 0)], min(tt[k] + 1e-9, tend)) if Jn_f(tt[k]) <= ac10.JTHR else float(tt[k])
    if fpo:
        to = float(s2o.t_events[0][0])
    if tn is not None and to is not None:
        rel_t = abs(tn - to) / to
    kk[tag] = dict(v_cross=vcr, omega_vc=math.sqrt(Pi0) * vcr, threshold=thr, predict_fold=pred, numeric_fold=fpn,
                   per_label_fold=fpo, t_fold_numeric=tn, t_fold_per_label=to, t_fold_rel=rel_t,
                   J_maxrel_where_J_ge_Jreg=agree, minJ_first_passage=float(Jn.min()))
    log(f"{tag}: {kk[tag]}")
def ok(t):
    d = kk[t]
    o = d["predict_fold"] == d["numeric_fold"] == d["per_label_fold"] and d["J_maxrel_where_J_ge_Jreg"] <= 1e-3
    if d["predict_fold"]:
        o = o and d["t_fold_rel"] is not None and d["t_fold_rel"] <= 5e-3
    return o
chk["K2"] = ok("A1_0.2") and ok("A1_1.0"); chk["K3"] = ok("A2_0.4") and ok("A2_2.0"); out["K2K3"] = kk

# MUTATE-A / MUTATE-B (from parts_MUTATE)
mm = {p["row"]["kind"]: dict(label=p["label"], converged=p["converged"],
                             t_fold=p["rungs"][-1]["t_fold"], J_min=p["rungs"][-1]["J_min"]) for p in PM}
chk["MUTATE_A"] = mm.get("MUTATE_A_repulsive", {}).get("label") == "REGULAR"
td = (1 - ac10.JTHR) / (sv3.AB * sv3.KB)
dt = mm.get("MUTATE_B_dust_twin", {})
chk["MUTATE_B"] = (mm.get("MUTATE_B_acoustic_mach0.3", {}).get("label") == "REGULAR" and dt.get("label") == "FOLD"
                   and abs(dt["t_fold"] / td - 1) <= 1e-3)
out["mutate"] = mm; out["MUTATE_B_t_d_analytic"] = td
log(f"MUTATE {mm}  t_d analytic {td}")

# MUTATE-C: K4 has power (vacuum ghost must differ from E3a)
ra = sv3.run(N, 1.0, 0.2, 0.0, 1e-2, ghost="E3a"); rv = sv3.run(N, 1.0, 0.2, 0.0, 1e-2, ghost="VAC")
la, lv = sv3.label(ra), sv3.label(rv)
relc = abs(rv["t_fold"] / ra["t_fold"] - 1) if (la == lv == "FOLD") else None
chk["MUTATE_C"] = (la != lv) or (relc is not None and relc > 1e-3)
out["MUTATE_C"] = dict(E3a=la, VAC=lv, t_E3a=ra["t_fold"], t_VAC=rv["t_fold"], rel=relc)
log(f"MUTATE_C {out['MUTATE_C']}")

# physical subset
phys = [p for p in P if p["row"].get("kind") in ("phantom", "clock_only")]
tk = lambda rw: (rw["foot"], rw["r_kpc"], rw["w_kms"], rw["M1"], rw["Lstar_pc"], rw["kind"])
v3 = {tk(p["row"]): p for p in phys if p["row"]["model"] == "v3s"}
ac = [p for p in phys if p["row"]["model"] == "AC2q"]
tab = {}; pairs = []; xmin = 1.0
for p in ac:
    rw = p["row"]; tw = v3.get(tk(rw))
    la = p["label"]; lb = tw["label"] if tw else "MISSING"
    kkey = f"{rw['foot']}|{rw['kind']}|AC2q {la}|v3s {lb}"; tab[kkey] = tab.get(kkey, 0) + 1
    rel = abs(p["rungs"][-1]["t_fold"] / tw["rungs"][-1]["t_fold"] - 1) if la == lb == "FOLD" else None
    pairs.append(dict(foot=rw["foot"], r=rw["r_kpc"], kind=rw["kind"], w=rw["w_kms"], M1=rw["M1"], L=rw["Lstar_pc"],
                      AC2q=la, v3s=lb, rel=rel, t_AC2q=p["rungs"][-1]["t_fold"],
                      t_v3s=tw["rungs"][-1]["t_fold"] if tw else None, K4_AC2q=p.get("K4"),
                      K4_v3s=tw.get("K4") if tw else None, extra=p["extra_rung"], timeout=p.get("timeout")))
    for x in (p, tw):
        if x and x["rungs"][-1].get("v_max") is not None:
            xmin = min(xmin, 1 - (x["rungs"][-1]["v_max"] * rw["w_kms"] * 1e3 / CL) ** 2)
chk["X_pos"] = xmin > 0.99
rels = [x["rel"] for x in pairs if x["rel"] is not None]
k4r = [d["rel"] for x in pairs for d in (x["K4_AC2q"], x["K4_v3s"]) if d and d.get("rel") is not None]
out.update(table=tab, n_AC2q=len(ac), n_v3s=len(v3), max_rel_fold_pairs=max(rels) if rels else None,
           n_fold_pairs=len(rels), max_K4_rel=max(k4r) if k4r else None, X_over_Xbg_min=xmin, pairs=pairs)
for k in sorted(tab):
    log(f"  {k}: {tab[k]}")
log(f"AC2q rows {len(ac)}, both-FOLD pairs {len(rels)}, max |t_AC2q/t_v3s - 1| = {out['max_rel_fold_pairs']}, max K4 rel {out['max_K4_rel']}")
labs = [(x["AC2q"], x["v3s"]) for x in pairs]
checks = all(chk.values()) and len(ac) == 32 and len(v3) == 32
bad = any(a in ("NOT CONVERGED", "UNDECIDED") or b in ("NOT CONVERGED", "UNDECIDED", "MISSING") for a, b in labs)
if not checks or bad:
    v = "NO VERDICT"
elif any(a == "REGULAR" and b == "FOLD" for a, b in labs):
    v = "PASS (AC2q regularizes)"
elif any(a == "FOLD" and b == "REGULAR" for a, b in labs):
    v = "WORSE"
elif all(a == b == "FOLD" for a, b in labs) and max(rels) <= 1e-2:
    v = "FAIL-SAME-AS-V3S"
elif all(a == b for a, b in labs):
    v = "SAME-AS-V3S, NOT ALL FOLD"
else:
    v = "NO VERDICT"
out["checks"] = chk; out["verdict"] = v
log(f"checks {chk}\nVERDICT (frozen, subset-scoped): {v}")
json.dump(out, open(os.path.join(HERE, "GRADE.json"), "w"), indent=1, default=float)
