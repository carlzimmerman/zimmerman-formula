#!/usr/bin/env python3
"""AC14 grade: frozen lines (FROZEN_CRITERIA.md, ad9d747016) on parts/ and parts_MUTATE/.
Run from the repo root: python3 action_search_2026_11_05/AC14_fold_final/grade.py
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, glob, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ac14
ac10 = ac14.ac10
CL = 2.99792458e8
load = lambda d: [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, d, "*.json")))]
P = load("parts"); PM = load("parts_MUTATE")
out, chk = {}, {}
log = lambda s: print(s, flush=True)
N = 2000

# K0: E1 inert at gamma = 0 (AC14 run == AC10 run)
k0 = {}
soft = [r for r in ac10.physical_rows() if r["kind"] == "soft" and r["model"] == "v3s"][0]
for nm, (M1, Pi0, s2) in {"K1_zero_charge": (1.0, 0.0, 0.0), "soft_v3s_row": (soft["M1"], soft["Pi0"], 0.0)}.items():
    a = ac14.run(N, M1, Pi0, s2, 0.0)["t_fold"]; b = ac10.run(N, M1, Pi0, s2, 0.0)["t_fold"]
    k0[nm] = dict(ac14=a, ac10=b, rel=abs(a - b) / b)
chk["K0"] = all(v["rel"] <= 1e-12 for v in k0.values()); out["K0"] = k0
log(f"K0 {'PASS' if chk['K0'] else 'FAIL'} {k0}")

# K1: zero charge coupled vs independent pair; thin-sheet delay
r = ac14.run(N, 1.0, 0.0, 0.0, 0.0, want_traj=True); q, dq, i1 = r["q"], r["dq"], r["i1"]; c = i1 - 1
def pair(t, y):
    x = y[:2]; return np.concatenate([y[2:], -0.5 * erf(x / (math.sqrt(2) * ac10.WB))])
def evp(t, y):
    return (y[1] - y[0]) / dq - ac10.JTHR
evp.terminal = True; evp.direction = -1
sp = solve_ivp(pair, (0, ac10.TMAX), [q[c], q[c + 1], 1.0, 1.0], method="DOP853", rtol=1e-12, atol=1e-14, events=evp, dense_output=True)
tp = float(sp.t_events[0][0]); xm = lambda t: 0.5 * (sp.sol(t)[0] + sp.sol(t)[1])
tc = brentq(xm, 0, tp); vc = 0.5 * (sp.sol(tc)[2] + sp.sol(tc)[3])
chk["K1"] = abs(r["t_fold"] - tp) <= 1e-6 and abs((tp - tc) / vc - 1) <= 0.02
out["K1"] = dict(t_coupled=r["t_fold"], t_pair=tp, delay_over_vcross=(tp - tc) / vc)
log(f"K1 {'PASS' if chk['K1'] else 'FAIL'} {out['K1']}")

# K2/K3: first passage with own crossing speed
rho_b = lambda x: np.exp(-x ** 2 / (2 * ac10.WB ** 2)) / (math.sqrt(2 * math.pi) * ac10.WB)
kk = {}
for tag, (Pi0, s2, thr) in {"A1_0.2": (0.2, 0.0, 1 / math.sqrt(2)), "A1_1.0": (1.0, 0.0, 1 / math.sqrt(2)),
                            "A2_0.4": (0.4, 0.4, 1.0), "A2_2.0": (2.0, 2.0, 1.0)}.items():
    rr = ac14.run(N, 1.0, Pi0, s2, 0.0, want_traj=True); so = rr["sol"]; c = rr["i1"] - 1
    tend = rr["t_fold"] if rr["t_fold"] is not None else ac10.TMAX
    va = lambda t: so.sol(t)[N + 1 + c]
    tg = np.linspace(0, tend, 4001); vv = np.array([va(t) for t in tg]); neg = np.where(vv < 0)[0]
    t_turn = float(tg[neg[0]]) if len(neg) else tend
    xmid = lambda t: 0.5 * (so.sol(t)[c] + so.sol(t)[c + 1])
    tcr = brentq(xmid, 0, t_turn)
    vcr = float(0.5 * (so.sol(tcr)[N + 1 + c] + so.sol(tcr)[N + 2 + c]))
    f = lambda t, y: [y[1], -rho_b(xmid(t)) * y[0] + (Pi0 - s2 * y[0])]
    s2o = solve_ivp(f, (0, t_turn), [1.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-13, max_step=ac10.WB / 4, dense_output=True)
    tt = np.linspace(0, t_turn, 2001)
    Jn = np.array([(so.sol(t)[c + 1] - so.sol(t)[c]) / dq for t in tt]); Jo = s2o.sol(tt)[0]
    agree = float(np.max(np.abs(Jn - Jo) / np.maximum(np.abs(Jo), 1e-2)))
    pred = math.sqrt(Pi0) * vcr <= thr
    fpn = bool(Jn.min() <= ac10.JTHR * 1.01); fpo = bool(Jo.min() <= ac10.JTHR * 1.01)
    kk[tag] = dict(v_cross=vcr, omega_vc=math.sqrt(Pi0) * vcr, threshold=thr, predict_fold=pred, numeric_fold=fpn,
                   per_label_fold=fpo, J_maxrel=agree, minJ_first_passage=float(Jn.min()))
    log(f"{tag}: {kk[tag]}")
ok = lambda t: kk[t]["predict_fold"] == kk[t]["numeric_fold"] == kk[t]["per_label_fold"] and kk[t]["J_maxrel"] <= 1e-3
chk["K2"] = ok("A1_0.2") and ok("A1_1.0"); chk["K3"] = ok("A2_0.4") and ok("A2_2.0"); out["K2K3"] = kk

mm = {p["row"]["kind"]: dict(label=ac14.label(p["rungs"][-1]), status=p["rungs"][-1]["status"], J_min=p["rungs"][-1]["J_min"]) for p in PM}
chk["MUTATE_A"] = mm.get("MUTATE_A_repulsive", {}).get("label") == "REGULAR"
chk["MUTATE_B"] = mm.get("MUTATE_B_mach0.3", {}).get("label") == "REGULAR"
out["mutate"] = mm; log(f"MUTATE {mm}")

phys = [p for p in P if p["row"]["kind"] in ("phantom", "clock_only", "soft")]
tk = lambda rw: (rw["foot"], rw["r_kpc"], rw["w_kms"], rw["M1"], rw["Lstar_pc"], rw["kind"])
v3 = {tk(p["row"]): p for p in phys if p["row"]["model"] == "v3s"}
ac = [p for p in phys if p["row"]["model"] == "AC2q"]
tab = {}; pairs = []; xmin = 1.0
for p in ac:
    rw = p["row"]; tw = v3.get(tk(rw))
    la = p["label"]; lb = tw["label"] if tw else "MISSING"
    key = f"{rw['foot']}|{rw['kind']}|AC2q {la}|v3s {lb}"; tab[key] = tab.get(key, 0) + 1
    rel = None
    if la == lb == "FOLD":
        rel = abs(p["rungs"][-1]["t_fold"] / tw["rungs"][-1]["t_fold"] - 1)
    pairs.append(dict(foot=rw["foot"], r=rw["r_kpc"], kind=rw["kind"], w=rw["w_kms"], M1=rw["M1"], L=rw["Lstar_pc"],
                      AC2q=la, v3s=lb, rel=rel, status_AC2q=p["rungs"][-1]["status"], status_v3s=tw["rungs"][-1]["status"] if tw else None,
                      Jmin_AC2q=p["rungs"][-1]["J_min"], extra=p["extra_rung"]))
    xmin = min(xmin, 1 - (p["rungs"][-1]["v_max"] * rw["w_kms"] * 1e3 / CL) ** 2)
chk["X_pos"] = xmin > 0.99
rels = [x["rel"] for x in pairs if x["rel"] is not None]
out.update(table=tab, n_AC2q=len(ac), n_v3s=len(v3), max_rel_fold_pairs=max(rels) if rels else None,
           n_fold_pairs=len(rels), X_over_Xbg_min=xmin, pairs=pairs)
for k in sorted(tab):
    log(f"  {k}: {tab[k]}")
log(f"AC2q rows {len(ac)}, both-FOLD pairs {len(rels)}, max |t_AC2q/t_v3s - 1| = {out['max_rel_fold_pairs']}")
labs = [(x["AC2q"], x["v3s"]) for x in pairs]
checks = all(chk.values()) and len(ac) == 240
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
log(f"checks {chk}\nVERDICT (frozen): {v}")
json.dump(out, open(os.path.join(HERE, "GRADE.json"), "w"), indent=1, default=float)
