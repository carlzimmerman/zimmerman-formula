#!/usr/bin/env python3
"""AC10 grade: frozen lines (FROZEN_CRITERIA.md, 552db86f89) applied to parts/, parts_MUTATE/, s1_reduction.json.
Then AMENDMENT A1-POST (declared after the first stress results; check code only, no physical row or threshold
changed): K2/K3 re-read as first-passage folds against X14's exact per-label F1d equation along each cell's own
trajectory. The frozen verdict stands as the verdict; the amendment reading is reported beside it.
Run from the repo root: python3 action_search_2026_11_05/AC10_nonlinear_clock/grade.py
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, glob, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ac10

CL = 2.99792458e8
load = lambda d: [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, d, "*.json")))]
P = load("parts"); PM = load("parts_MUTATE")
S1 = json.load(open(os.path.join(HERE, "s1_reduction.json")))
out, chk = {}, {}


def log(s):
    print(s, flush=True)


chk["S1"] = bool(S1["checks"]["S1"])
by = lambda kind: [p for p in P if p["row"]["kind"] == kind]

# ---------------- K1: zero charge, no pressure: coupled code vs independent pair; thin-sheet delay
k1 = by("K1_zero_charge")[0]
N = 2000
r = ac10.run(N, 1.0, 0.0, 0.0, 0.0, want_traj=True)
sol = r["sol"]; q = r["q"]; dq = r["dq"]; i1 = int((1 - ac10.EDGE) * N)
c = i1 - 1                                                    # front-most interior cell folds first (zero charge)
def pair(t, y):
    from scipy.special import erf
    x = y[:2]; return np.concatenate([y[2:], -0.5 * erf(x / (math.sqrt(2) * ac10.WB))])
def evp(t, y):
    return (y[1] - y[0]) / dq - ac10.JTHR
evp.terminal = True; evp.direction = -1
sp_ = solve_ivp(pair, (0, ac10.TMAX), [q[c], q[c + 1], 1.0, 1.0], method="DOP853", rtol=1e-12, atol=1e-14, events=evp, dense_output=True)
t_pair = float(sp_.t_events[0][0])
# crossing of the cell midpoint
from scipy.optimize import brentq
xm = lambda t: 0.5 * (sp_.sol(t)[0] + sp_.sol(t)[1])
tc = brentq(xm, 0, t_pair); vc = 0.5 * (sp_.sol(tc)[2] + sp_.sol(tc)[3])
delay = t_pair - tc
chk["K1"] = abs(r["t_fold"] - t_pair) <= 1e-6 and abs(delay / vc - 1) <= 0.02
out["K1"] = dict(t_fold_coupled=r["t_fold"], t_fold_pair=t_pair, diff=abs(r["t_fold"] - t_pair), t_cross=tc, v_cross=vc,
                 delay_over_vcross=delay / vc, ladder_label=k1["label"])
log(f"K1 {'PASS' if chk['K1'] else 'FAIL'} coupled {r['t_fold']:.9f} vs pair {t_pair:.9f}; delay/v_cross = {delay / vc:.5f}")

# ---------------- K2/K3 as frozen
st = {p["row"]["tag"]: p for p in P if p["row"]["kind"].startswith("stress")}
labs = {k: v["label"] for k, v in st.items()}
chk["K2"] = labs.get("A1_0.4") == "FOLD" and labs.get("A1_0.6") == "REGULAR"
chk["K3"] = labs.get("A2_0.8") == "FOLD" and labs.get("A2_1.2") == "REGULAR"
out["stress_labels_frozen"] = labs
log(f"K2 {'PASS' if chk['K2'] else 'FAIL'} v3s A1 stress labels {labs.get('A1_0.4')}, {labs.get('A1_0.6')} (frozen expectation FOLD, REGULAR)")
log(f"K3 {'PASS' if chk['K3'] else 'FAIL'} AC2q A2 stress labels {labs.get('A2_0.8')}, {labs.get('A2_1.2')} (frozen expectation FOLD, REGULAR)")

# ---------------- MUTATEs
mm = {p["row"]["kind"]: p["label"] for p in PM}
chk["MUTATE_A"] = mm.get("MUTATE_A_repulsive") == "REGULAR"
chk["MUTATE_B"] = mm.get("MUTATE_B_mach0.3") == "REGULAR"
out["mutate"] = mm
log(f"MUTATE-A {'bites' if chk['MUTATE_A'] else 'DOES NOT BITE'} ({mm.get('MUTATE_A_repulsive')}); "
    f"MUTATE-B power gate {'bites' if chk['MUTATE_B'] else 'DOES NOT BITE'} ({mm.get('MUTATE_B_mach0.3')})")

# ---------------- physical rows
phys = [p for p in P if p["row"]["kind"] in ("phantom", "clock_only", "soft")]
def twin_key(rw):
    return (rw["foot"], rw["r_kpc"], rw["w_kms"], rw["M1"], rw["Lstar_pc"], rw["kind"])
v3 = {twin_key(p["row"]): p for p in phys if p["row"]["model"] == "v3s"}
summ = {}
allfold = True; conv_all = True; within = True; worst_rel = 0.0; xmin = 1.0
for p in phys:
    rw = p["row"]
    if rw["model"] != "AC2q":
        continue
    tw = v3[twin_key(rw)]
    f = rw["foot"]; d = summ.setdefault(f, dict(rows=0, fold=0, regular=0, undecided=0, not_conv=0, max_rel_vs_v3s=0.0,
                                               t_fold_range=[1e9, 0], max_ladder_change=0.0))
    d["rows"] += 1
    lab = p["label"]
    if lab == "FOLD":
        d["fold"] += 1
        tf = p["rungs"][-1]["t_fold"]; tv = tw["rungs"][-1]["t_fold"] if tw["label"] == "FOLD" else None
        d["t_fold_range"] = [min(d["t_fold_range"][0], tf), max(d["t_fold_range"][1], tf)]
        d["max_ladder_change"] = max(d["max_ladder_change"], p["rel_change"])
        if tv is None:
            within = False
        else:
            rel = abs(tf - tv) / tv; d["max_rel_vs_v3s"] = max(d["max_rel_vs_v3s"], rel); worst_rel = max(worst_rel, rel)
            if rel > 1e-2:
                within = False
    elif lab == "REGULAR":
        d["regular"] += 1; allfold = False
    elif lab == "NOT CONVERGED":
        d["not_conv"] += 1; conv_all = False; allfold = False
    else:
        d["undecided"] += 1; allfold = False
    # X > 0 up to the fold: X/X_bg >= 1 - (v_max w / c)^2 at PN order
    xmin = min(xmin, 1 - (p["rungs"][-1]["v_max"] * rw["w_kms"] * 1e3 / CL) ** 2)
out["physical"] = summ
out["X_over_Xbg_min"] = xmin
chk["X_pos"] = xmin > 0.99
for f, d in summ.items():
    log(f"physical [{f}] AC2q rows {d['rows']}: FOLD {d['fold']}, REGULAR {d['regular']}, UNDECIDED {d['undecided']}, "
        f"NOT CONVERGED {d['not_conv']}; t_fold range {d['t_fold_range'][0]:.4f}-{d['t_fold_range'][1]:.4f} tau_f; "
        f"max |t_AC2q/t_v3s - 1| = {d['max_rel_vs_v3s']:.2e}; max ladder change {d['max_ladder_change']:.1e}")
log(f"X > 0 up to the fold: min X/X_bg = {xmin:.9f}")

controls_ok = chk["S1"] and chk["K1"] and chk["K2"] and chk["K3"] and chk["MUTATE_A"] and chk["MUTATE_B"]
n_ac2q = sum(1 for p in phys if p["row"]["model"] == "AC2q"); n_frozen = len([r for r in ac10.physical_rows() if r["model"] == "AC2q"])
out["rows_run"] = dict(AC2q=n_ac2q, frozen_total=n_frozen, complete=n_ac2q == n_frozen)
log(f"physical AC2q rows run: {n_ac2q} of {n_frozen} frozen (subset: information only)" if n_ac2q < n_frozen else "all frozen rows run")
if not conv_all or not controls_ok or n_ac2q < n_frozen:
    verdict = "NO VERDICT"
elif allfold and within:
    verdict = "CAUSTIC-GENERIC"
elif any(d["regular"] for d in summ.values()):
    verdict = "REGULAR"
else:
    verdict = "NO VERDICT"
out["verdict_frozen"] = verdict
out["checks"] = chk
log(f"FROZEN VERDICT: {verdict}  (checks {chk})")

# ---------------- AMENDMENT A1-POST: first-passage reading of K2/K3 (check code only)
from scipy.special import erf
amend = {}
rho_b = lambda x: np.exp(-x ** 2 / (2 * ac10.WB ** 2)) / (math.sqrt(2 * math.pi) * ac10.WB)
for tag, (M1, Pi0, s2) in {"A1_0.4": (1.0, 0.4, 0.0), "A1_0.6": (1.0, 0.6, 0.0),
                           "A2_0.8": (1.0, 0.8, 0.8), "A2_1.2": (1.0, 1.2, 1.2)}.items():
    rr = ac10.run(N, M1, Pi0, s2, 0.0, want_traj=True)
    so = rr["sol"]; c = i1 - 1
    tend = rr["t_fold"] if rr["t_fold"] is not None else ac10.TMAX
    xa = lambda t: so.sol(t)[c]; xb = lambda t: so.sol(t)[c + 1]
    va = lambda t: so.sol(t)[N + 1 + c]
    # first turnaround of the cell's front label (end of first passage)
    tg = np.linspace(0, tend, 4001); vv = np.array([va(t) for t in tg])
    neg = np.where(vv < 0)[0]; t_turn = float(tg[neg[0]]) if len(neg) else tend
    xm = lambda t: 0.5 * (xa(t) + xb(t))
    def fj(t, y):
        return [y[1], -rho_b(xm(t)) * y[0] + M1 * (Pi0 - s2 * y[0])]
    tcr = brentq(xm, 0, t_turn) if xm(0) < 0 < xm(t_turn) else None
    so2 = solve_ivp(fj, (0, t_turn), [1.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-13, max_step=ac10.WB / 4, dense_output=True)
    tt = np.linspace(0, t_turn, 2001)
    Jnum = np.array([(xb(t) - xa(t)) / dq for t in tt]); Jode = so2.sol(tt)[0]
    agree = float(np.max(np.abs(Jnum - Jode) / np.maximum(np.abs(Jode), 1e-2)))
    fp_num = bool(Jnum.min() <= ac10.JTHR * 1.01); fp_ode = bool(Jode.min() <= ac10.JTHR * 1.01)
    vcr = float(0.5 * (so.sol(tcr)[N + 1 + c] + so.sol(tcr)[N + 2 + c])) if tcr else None
    Jc = float(so2.sol(tcr)[0]) if tcr else None
    om = math.sqrt(M1 * Pi0)
    thin = (om * vcr if tcr else None)                        # omega tau_f with the cell's own crossing speed
    amend[tag] = dict(fold_type_first_interior=("FIRST-PASSAGE" if rr["t_fold"] is not None and t_turn >= rr["t_fold"] - 1e-9 else
                                                "TURNAROUND/PHASE-MIXING" if rr["t_fold"] is not None else "none"),
                      t_fold=rr["t_fold"], t_turn_front_cell=t_turn, t_cross=tcr, v_cross=vcr, J_cross=Jc,
                      omega_tau_f_own_vcross=thin, J_ode_vs_numeric_maxrel=agree,
                      first_passage_fold_numeric=fp_num, first_passage_fold_F1d=fp_ode,
                      front_cell_min_J_first_passage=float(Jnum.min()))
    log(f"A1-POST {tag}: earliest interior fold {amend[tag]['fold_type_first_interior']} at {rr['t_fold']}; front cell first passage "
        f"min J {Jnum.min():.4f} (F1d {Jode.min():.4f}, max rel diff {agree:.1e}); omega tau_f with own v_cross {thin}")
ok_am = all(a["first_passage_fold_numeric"] == a["first_passage_fold_F1d"] and a["J_ode_vs_numeric_maxrel"] <= 1e-3 for a in amend.values())
out["amendment_A1_POST"] = dict(rows=amend, K2K3_first_passage_agree=ok_am)
v_am = "CAUSTIC-GENERIC" if (ok_am and n_ac2q == n_frozen and conv_all and allfold and within and chk["S1"] and chk["K1"] and chk["MUTATE_A"] and chk["MUTATE_B"]) else verdict
out["verdict_under_amendment"] = v_am
log(f"A1-POST: first-passage numerics = F1d on all four stress rows: {ok_am}; verdict under the amendment: {v_am}")
# ---------------- AMENDMENT A2-POST: first fold over ALL cells (declared after the first ladder results showed the
# excluded front-edge cells fold first and their post-fold pressure spikes contaminate the interior reading)
summ2 = {}; allf2 = True; conv2 = True; within2 = True
for p in phys:
    rw = p["row"]
    if rw["model"] != "AC2q":
        continue
    tw = v3[twin_key(rw)]
    d = summ2.setdefault(rw["foot"], dict(rows=0, fold=0, other=0, not_conv=0, max_rel_vs_v3s=0.0, t_range=[1e9, 0],
                                          max_ladder_change=0.0, by_kind={}))
    d["rows"] += 1
    la = p["label_all"]; d["by_kind"].setdefault(rw["kind"], {}).setdefault(la, 0); d["by_kind"][rw["kind"]][la] += 1
    if la == "FOLD":
        d["fold"] += 1
        tf = p["rungs"][-1]["t_fold_all"]; tv = tw["rungs"][-1]["t_fold_all"] if tw["label_all"] == "FOLD" else None
        d["t_range"] = [min(d["t_range"][0], tf), max(d["t_range"][1], tf)]
        d["max_ladder_change"] = max(d["max_ladder_change"], p["rel_change_all"])
        if tv is None:
            within2 = False
        else:
            rel = abs(tf - tv) / tv; d["max_rel_vs_v3s"] = max(d["max_rel_vs_v3s"], rel)
            within2 = within2 and rel <= 1e-2
    elif la == "NOT CONVERGED":
        d["not_conv"] += 1; conv2 = False; allf2 = False
    else:
        d["other"] += 1; allf2 = False
for f, d in summ2.items():
    log(f"A2-POST [{f}] AC2q rows {d['rows']}: FOLD {d['fold']}, other {d['other']}, NOT CONVERGED {d['not_conv']}; "
        f"t range {d['t_range'][0]:.5f}-{d['t_range'][1]:.5f} tau_f; max |t/t_v3s - 1| {d['max_rel_vs_v3s']:.2e}; "
        f"max ladder change {d['max_ladder_change']:.1e}; by kind {d['by_kind']}")
base_ok = chk["S1"] and chk["K1"] and chk["MUTATE_A"] and chk["MUTATE_B"] and ok_am
base_ok = base_ok and n_ac2q == n_frozen
v2 = ("CAUSTIC-GENERIC" if (base_ok and conv2 and allf2 and within2) else
      "REGULAR" if (base_ok and any(d["other"] for d in summ2.values()) and conv2) else "NO VERDICT")
out["amendment_A2_POST"] = dict(physical=summ2, verdict_under_A1_and_A2=v2)
log(f"verdict under A1-POST + A2-POST: {v2}")
json.dump(out, open(os.path.join(HERE, "GRADE.json"), "w"), indent=1, default=float)
