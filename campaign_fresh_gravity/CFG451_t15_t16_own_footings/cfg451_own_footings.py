#!/usr/bin/env python3
"""CFG451: T15 (cold budget) and T16 (coupling gradient) on the framework's own a0.  (criteria: FROZEN_CRITERIA.md, d070de4c1)

T15/T16 formulas copied verbatim from deepseek_push/openai_math_cross_analysis_2026-10/t15_cold_budget and t16_coupling_gradient;
only a0 (in the kernel supply S) and the group/cluster deficits (CFG450, footing-matched) change. Footings never pooled.
Run: python3 cfg451_own_footings.py  |  CFG451_MUTATE=1 plants T15's misread f_law := deficit.  Local data only.
"""
import json, math, os, sys

MUT = os.environ.get("CFG451_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "deepseek_push", "openai_math_cross_analysis_2026-10")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
lines = []
def say(s=""):
    lines.append(s); print(s)

G = 6.674e-11; GYR = 3.156e16; TAU = 10.3 * GYR; KPC = 3.086e19
LAM = 0.028; RHO_R500 = 1.55e-24
F_R500 = 1 - math.exp(-LAM * math.sqrt(4 * math.pi * G * RHO_R500) * TAU)
RATE_R500_TAU = math.sqrt(4 * math.pi * G * RHO_R500) * TAU

def S_of_R(Mb, R, a0):
    return 1.0 / (math.exp(math.sqrt(G * Mb * 1.989e30 / a0) / KPC / R) - 1.0)
def f_law_at(rho):
    return 1 - math.exp(-LAM * math.sqrt(4 * math.pi * G * rho) * TAU)
def lam_from_f(f):
    return -math.log(1 - f) / RATE_R500_TAU if f < 0.999 else 1e9
def lam_max(rate_tau, f):
    return float("inf") if f >= 1.0 else -math.log(1 - f) / rate_tau

def t15(a0, xg0, xg3, xc0, xc3, mut=False):
    SM = {"mw30": S_of_R(7.0e10, 30.0, a0), "groups": S_of_R(6e12, 554.0, a0), "clusters": S_of_R(2.8e13, 985.0, a0)}
    rows = {}
    f30 = f_law_at(200e3 ** 2 / (4 * math.pi * G * (30 * KPC) ** 2))
    for lab, x in {"V188": 1.48, "V200": 1.8, "V230": 2.7}.items():
        rows[f"MW30_{lab}"] = x - (0.86 if mut else f30) * SM["mw30"]
    for lab, x in {"b0": xg0, "b03": xg3}.items():
        rows[f"groups_{lab}"] = x - (x if mut else F_R500) * SM["groups"]
    for lab, x in {"b0": xc0, "b03": xc3}.items():
        rows[f"clusters_{lab}"] = x - (x if mut else F_R500) * SM["clusters"]
    ceil = {k: [x / SM[k], lam_from_f(x / SM[k])] for k, x in (("groups", xg0), ("clusters", xc0))}
    res = {"groups": [xg0 / SM["groups"], xg3 / SM["groups"]], "clusters": [xc0 / SM["clusters"], xc3 / SM["clusters"]]}
    return dict(SM=SM, rows=rows, ceil=ceil, res=res, viol=0.029 / ceil["clusters"][1])

def mw_point(a0, Mb, V):
    S = S_of_R(Mb, 30.0, a0)
    x = ((V * 1e3) ** 2 * (30 * KPC) / G - Mb * 1.989e30) / (Mb * 1.989e30)
    feas = x <= S
    rate_tau = math.sqrt(4 * math.pi * G * (V * 1e3) ** 2 / (4 * math.pi * G * (30 * KPC) ** 2)) * TAU
    return dict(x=x, S=S, feasible=feas, lam_max=lam_max(rate_tau, x / S) if feas else float("inf"))

def t16(a0, xg0, xg3, xc0, xc3):
    mw = {f"Mb{Mb:.0e}_V{V}": mw_point(a0, Mb, V) for Mb in (7.0e10, 1.0e11) for V in (188, 200, 230)}
    Sg, Sc = S_of_R(6e12, 554.0, a0), S_of_R(2.8e13, 985.0, a0)
    others = {"groups_b0": lam_max(RATE_R500_TAU, xg0 / Sg), "groups_b03": lam_max(RATE_R500_TAU, xg3 / Sg),
              "clusters_b0": lam_max(RATE_R500_TAU, xc0 / Sc), "clusters_b03": lam_max(RATE_R500_TAU, xc3 / Sc)}
    def windows(mwkeys):
        mwl = [mw[k]["lam_max"] for k in mwkeys if mw[k]["feasible"]]
        return {"mw": [min(mwl), max(mwl)] if mwl else [math.inf, math.inf],
                "groups": [others["groups_b0"], others["groups_b03"]], "clusters": [others["clusters_b0"], others["clusters_b03"]]}
    out = dict(mw=mw, others=others)
    for lab, keys in (("verbatim_both_Mb", list(mw)), ("frozen_Mb7e10", [k for k in mw if k.startswith("Mb7e+10")])):
        w = windows(keys)
        lo, hi = max(v[0] for v in w.values()), min(v[1] for v in w.values())
        out[lab] = dict(windows=w, inter=[lo, hi], nonempty=lo <= hi)
    out["gap_floor_cl"] = 0.028 / others["clusters_b03"]
    return out

def v_infeasible(a0, Mb=7.0e10):
    lo, hi = 150.0, 300.0
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if mw_point(a0, Mb, m)["feasible"]: lo = m
        else: hi = m
    return 0.5 * (lo + hi)

checks = {}
# ---- C1: reproduce T15/T16 at 1.2e-10 with the rounded deficits
T15J = json.load(open(os.path.join(DS, "t15_cold_budget", "t15_results.json")))
T16J = json.load(open(os.path.join(DS, "t16_coupling_gradient", "t16_results.json")))
r15, r16 = t15(1.2e-10, 0.79, 1.76, 0.41, 0.91), t16(1.2e-10, 0.79, 1.76, 0.41, 0.91)
err = [abs(r15["rows"][k] - T15J["rows"][k]) for k in T15J["rows"]]
err += [abs(a - b) for k in ("groups", "clusters") for a, b in zip(r15["ceil"][k], T15J["ceil"][k])]
err += [abs(a - b) for k in ("groups", "clusters") for a, b in zip(r15["res"][k], T15J["res"][k])] + [abs(r15["viol"] - T15J["viol"])]
err += [abs(r16["mw"][k]["lam_max"] - T16J["mw"][k]["lam_max"]) for k in T16J["mw"] if T16J["mw"][k]["feasible"]]
err += [0.0 if r16["mw"][k]["feasible"] == T16J["mw"][k]["feasible"] else 1.0 for k in T16J["mw"]]
err += [abs(r16["others"][k] - T16J["others"][k]["lam_max"]) for k in T16J["others"]]
err += [abs(a - b) for k in T16J["windows"] for a, b in zip(r16["verbatim_both_Mb"]["windows"][k], T16J["windows"][k])]
err += [abs(a - b) for a, b in zip(r16["verbatim_both_Mb"]["inter"], T16J["inter"])] + [abs(r16["gap_floor_cl"] - T16J["gap_floor_cl"])]
checks["C1_t15_t16_reproduction"] = bool(max(err) < 1e-9)

# ---- C2: CFG450 deficits
D450 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG450_xcop_gas_radius_audit", "cfg450_results.json")))["deficits"]
def xs(fk):
    d = D450[fk]
    return [d["0.0"]["groups"]["med"], d["0.3"]["groups"]["med"], d["0.0"]["clusters_R500"]["med"], d["0.3"]["clusters_R500"]["med"]]
checks["C2_cfg450_inputs"] = bool(abs(xs("canonical")[2] - 0.4135) < 1e-3 and abs(xs("canonical")[3] - 0.9054) < 1e-3)

say(f"CFG451 T15/T16 on the framework's own a0  MUTATE={MUT}")
say(f"held: lambda {LAM}, f_law(R500) {F_R500:.3f}, tau 10.3 Gyr, MW x (V188/200/230) 1.48/1.80/2.70, conventions as T15/T16")
say("")
OUT = {}
rows_to_show = [("T15/T16 as committed (a0 1.2e-10, rounded deficits)", 1.2e-10, [0.79, 1.76, 0.41, 0.91])] + [
    (f"{fk} footing (a0 {a0:.4e}, CFG450 deficits)", a0, xs(fk)) for fk, a0 in A0.items()]
for lab, a0, x in rows_to_show:
    a, b = t15(a0, *x, mut=MUT), t16(a0, *x)
    vinf = v_infeasible(a0)
    V1 = a["rows"]["clusters_b0"] < 0 and a["rows"]["clusters_b03"] < 0
    g = a["rows"]["groups_b03"]
    V2 = "knife-edge" if abs(g) < 0.15 else ("negative" if g < 0 else "positive")
    gap = b["gap_floor_cl"]
    V4 = "STANDS" if gap >= 1.5 else ("WEAKENED" if gap >= 1.0 else "BREAKS (floor fits the cluster window)")
    fz, vb = b["frozen_Mb7e10"], b["verbatim_both_Mb"]
    say(f"  {lab}")
    say(f"     deficits groups {x[0]:.3f}/{x[1]:.3f}  clusters {x[2]:.4f}/{x[3]:.4f};  S/M_b: MW30 {a['SM']['mw30']:.3f}  groups {a['SM']['groups']:.3f}  clusters {a['SM']['clusters']:.3f}")
    say("     T15 M_cold/M_b: " + "  ".join(f"{k} {v:+.3f}" for k, v in a["rows"].items()))
    say(f"     V1 clusters overdraft at b=0 and 0.3: {V1}   V2 groups b=0.3 {g:+.3f} ({V2})   V3 MW-30 infeasible above V = {vinf:.1f} km/s (M_b 7e10)")
    say(f"     T15 f_max cl {a['ceil']['clusters'][0]:.4f} (lam_max {a['ceil']['clusters'][1]:.5f})  gr {a['ceil']['groups'][0]:.4f};  f_res cl [{a['res']['clusters'][0]:.4f}, {a['res']['clusters'][1]:.4f}];  V6 T12/cluster {a['viol']:.2f}x")
    say(f"     T16 windows MW(7e10) [{fz['windows']['mw'][0]:.4f}, {fz['windows']['mw'][1]:.4f}]  groups [{fz['windows']['groups'][0]:.4f}, {fz['windows']['groups'][1]:.4f}]  clusters [{fz['windows']['clusters'][0]:.4f}, {fz['windows']['clusters'][1]:.4f}]")
    say(f"     V5 intersection (frozen, MW M_b 7e10) [{fz['inter'][0]:.4f}, {fz['inter'][1]:.4f}] nonempty {fz['nonempty']};  T16-verbatim (both M_b) [{vb['inter'][0]:.4f}, {vb['inter'][1]:.4f}] nonempty {vb['nonempty']}")
    say(f"     V4 floor 0.028 / cluster upper {b['others']['clusters_b03']:.4f} = {gap:.2f}x -> {V4}")
    OUT[lab] = dict(a0=a0, deficits=x, T15=a, T16=b, V1=V1, V2=[g, V2], V3=vinf, V4=[gap, V4], V5=[fz["inter"], fz["nonempty"]], V6=a["viol"])
say("")
if MUT:
    checks["MUTATE_V1_flips_both"] = bool(not OUT[rows_to_show[1][0]]["V1"] and not OUT[rows_to_show[2][0]]["V1"])
say("checks: " + json.dumps(checks))
json.dump(dict(mutate=MUT, rows=OUT, checks=checks), open(os.path.join(HERE, f"cfg451_results{TAG}.json"), "w"), indent=1, default=float)
ok = all(checks.values())
print("<LANE> COMPLETE: all checks PASS" if ok else "<LANE> COMPLETE: -- SOME CHECKS FAIL")
sys.exit(0 if ok else 1)
