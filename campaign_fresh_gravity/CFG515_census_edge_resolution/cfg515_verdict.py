#!/usr/bin/env python3
"""CFG515 (e) cluster unsettled fraction, the growth bookkeeping (section 5, argued + arithmetic), and the frozen verdict
(FROZEN_CRITERIA.md 2bbe75602, sections 3e, 4, 5, 7).
(e) CFG453's per-object X-COP clusters / Lovisari groups (its script executed read-only up to its T15/T16 block); each object's f_ret
    from cfg515_lib; settled(<R500) = min(M_ph(<R500), 5.364 M_b / f_ret); u = median(x_T15 - settled/M_b) / median(x_T15) for b = 0,
    0.3; PASS iff both lie inside the record range [0.433, 0.628] / [0.368, 0.584].  Structurally blind for f_ret <= 1 (declared).
Verdict: reads cfg515_{kids,levels,sparc,mw}_results{,_MUTATE}.json.
MUTATE (CFG515_MUTATE=1): f_ret = 1 and 0.01; M1/M2 teeth.
Run: python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_verdict.py   (after the four scoring scripts)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import cfg515_lib as L                                                       # noqa: E402
MUTATE = os.environ.get("CFG515_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
MODES = L.modes()
FOOTS = ("canonical", "alt")
LOG, CHK = [], {}
RES = {"lane": "CFG515", "script": "cfg515_verdict", "mutate": MUTATE, "modes": list(MODES)}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
# ------------------------------------------------------------------ K2: fret_of = CFG416's
src416 = open(os.path.join(LANES, "CFG416_supply_edge_confinement_512", "cfg416_pm.py")).read()
i0 = src416.index("def fret_of(lM):"); i1 = src416.index("def x_supply")
ns416 = {"FRETX": 1}
exec(src416[i0:i1], ns416)
grid = np.linspace(9.0, 16.0, 7001)
k2 = max(abs(ns416["fret_of"](x) - L.fret_of(x)) for x in grid)
res_sc = []
for Mb in np.geomspace(1e7, 3e14, 400):
    f, lM = L.fret_census(Mb)
    res_sc.append(abs(L.fret_of(lM) - f))
check("K2 this lane's fret_of = CFG416's (function text exec'd) on 7001 points; self-consistency residual < 1e-9 (M_b 1e7-3e14)",
      k2 <= 1e-12 and max(res_sc) < 1e-9, f"max |diff| {k2:.1e}; max residual {max(res_sc):.1e}")

# ------------------------------------------------------------------ (e) clusters / groups
p453 = os.path.join(LANES, "CFG453_t15_deficit_units", "cfg453_deficit_units.py")
s453 = open(p453).read()
mk = "# ------------------------------------------------------------------ T15 / T16"
assert s453.count(mk) == 1
N4 = {"__file__": p453, "__name__": "cfg453_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s453[:s453.index(mk)], "cfg453_ro", "exec"), N4)
CL, GRP, per_object = N4["CL"], N4["GRP"], N4["per_object"]
J453 = json.load(open(os.path.join(LANES, "CFG453_t15_deficit_units", "cfg453_results.json")))["D1"]
RANGE = {"canonical": (0.433, 0.628), "alt": (0.368, 0.584)}
E = {}
k8 = 0.0
for mode in MODES:
    E[mode] = {}
    for foot in FOOTS:
        a0 = N4["A0"][foot]
        r_ = {}
        for b in N4["BS"]:
            for lab, objs in (("cl", CL), ("gr", GRP)):
                po = per_object(objs, b, a0)
                if mode == MODES[0]:
                    k8 = max(k8, abs(float(np.median([o["xT"] for o in po])) - J453[foot]["xT"][lab][N4["BS"].index(b)]))
                fr = np.array([L.fret(mode, o["Mb"]) for o in po])
                xT = np.array([o["xT"] for o in po]); ph = np.array([o["nu"] - 1 for o in po])
                sup = L.COLD_PER_B / fr
                settled = np.minimum(ph, sup)
                u = float(np.median(xT - settled) / np.median(xT))
                r_[f"{lab}|b{b}"] = dict(u=u, fret_median=float(np.median(fr)), fret_min=float(fr.min()), fret_max=float(fr.max()),
                                         n=len(po), n_edge_inside_R500=int(np.sum(sup < ph)),
                                         budget_violations=int(np.sum(xT > sup)), median_xT=float(np.median(xT)), median_supply=float(np.median(sup)))
        ok = all(RANGE[foot][0] - 1e-3 <= r_[f"cl|b{b}"]["u"] <= RANGE[foot][1] + 1e-3 for b in N4["BS"])
        E[mode][foot] = dict(rows=r_, passed=ok)
        P(f"  (e) [{mode:6s}|{foot:9s}] clusters u b0 {r_['cl|b0.0']['u']:.3f} / b0.3 {r_['cl|b0.3']['u']:.3f} (record {RANGE[foot]}); "
          f"f_ret clusters {r_['cl|b0.0']['fret_min']:.2f}-{r_['cl|b0.0']['fret_max']:.2f}, groups {r_['gr|b0.0']['fret_min']:.2f}-{r_['gr|b0.0']['fret_max']:.2f}; "
          f"edge inside R500: {r_['cl|b0.0']['n_edge_inside_R500']}/{r_['cl|b0.0']['n']} cl -> {'PASS' if ok else 'FAIL'}")
        P(f"       budget x_T15 <= 5.364/f_ret (reported): clusters violate {r_['cl|b0.0']['budget_violations']}/{r_['cl|b0.0']['n']} (b0), "
          f"{r_['cl|b0.3']['budget_violations']}/{r_['cl|b0.3']['n']} (b0.3); groups {r_['gr|b0.0']['budget_violations']}/{r_['gr|b0.0']['n']} (b0), "
          f"{r_['gr|b0.3']['budget_violations']}/{r_['gr|b0.3']['n']} (b0.3); group median x_T {r_['gr|b0.0']['median_xT']:.1f} vs supply {r_['gr|b0.0']['median_supply']:.1f}")
    E[mode]["e_pass"] = all(E[mode][f]["passed"] for f in FOOTS)
check("K8 CFG453 objects (read-only prefix) reproduce its committed median x_T15 (clusters, groups; b = 0, 0.3) to 1e-9", k8 < 1e-9, f"max |diff| {k8:.1e}")
RES["e"] = E

# ------------------------------------------------------------------ section 5: growth bookkeeping (arithmetic; the argument is in the README)
P("\n  GROWTH BOOKKEEPING (per halo of original baryons M_o; present M_now = f_ret M_o). Arithmetic only.")
LNE = math.log(1 / (1 - L.FB))
GB = {}
for f in (1.0, 0.18, 0.10, 0.07):
    # PM (f_ret = 1 on undepleted PM baryons): phantom of M_o, edge 5.85 r_M(M_o), settled = 5.364 M_o
    # consistent real halo: phantom of f M_o, edge r_M(f M_o)/ln(1 + f f_b/(1-f_b)), settled = 5.364 f M_o / f = 5.364 M_o (identity)
    edge_ratio = math.sqrt(f) * LNE / L.ln_fac(f)
    # phantom inside the PM edge in the consistent halo, as a share of the supply: M_ph = M_now/(exp(r_M,now/r) - 1)
    rM_now_over_rpm = math.sqrt(f) * LNE                                   # r_M(M_now) / r_edge,PM
    share_in_pm_edge = f / (math.exp(rM_now_over_rpm) - 1.0) / L.COLD_PER_B
    # CFG416 (census radius, phantom of the UNDEPLETED M_o, no supply cap): phantom inside its radius / supply 5.364 M_o
    r416 = math.sqrt(f) / L.ln_fac(f)                                        # r_edge(census) / r_M(M_o)
    over416 = (1.0 / (math.exp(1.0 / r416) - 1.0)) / L.COLD_PER_B
    GB[str(f)] = dict(settled_over_supply_PM=1.0, settled_over_supply_real=1.0, edge_real_over_PM=edge_ratio,
                      share_of_supply_inside_PM_edge_real=share_in_pm_edge, CFG416_phantom_over_supply=over416)
    P(f"    f_ret {f:4.2f}: settled = 5.364 M_o in both pictures; real edge / PM edge {edge_ratio:.2f}; share of the settled mass inside "
      f"the PM edge in the real halo {share_in_pm_edge:.2f}; CFG416's uncapped phantom inside its census radius = {over416:.2f} x the supply")
RES["growth_bookkeeping"] = GB

# ------------------------------------------------------------------ verdict
def load(name):
    p = os.path.join(HERE, f"cfg515_{name}_results{SUF}.json")
    return json.load(open(p))


try:
    K, LV, SP, MW = load("kids"), load("levels"), load("sparc"), load("mw")
except FileNotFoundError as ex:
    P(f"  missing input {ex}; run the four scoring scripts first"); sys.exit(2)
for nm, J in (("kids", K), ("levels", LV), ("sparc", SP), ("mw", MW)):
    bad = [k for k, v in J["checks"].items() if v["load_bearing"] and not v["ok"]]
    check(f"inputs: {nm} controls all pass", not bad, f"failures {bad}")
V = {}
P("\n  PER-TEST VERDICTS (both footings each)")
for mode in MODES:
    t = dict(a=K["rows"][mode]["a_pass"], a1=K["rows"][mode]["a1_pass"], a2=K["rows"][mode]["a2_pass"], b=LV["rows"][mode]["b_pass"],
             c=SP["rows"][mode]["c_pass"], d=MW["rows"][mode]["d_pass"], e=E[mode]["e_pass"])
    core = [t[k] for k in "abcd"]
    if all(core):
        v = "CLASH DISSOLVED" if t["e"] else "PARTLY"
    elif any(core):
        v = "PARTLY"
    else:
        v = "NOT DISSOLVED"
    V[mode] = dict(tests=t, verdict=v)
    P(f"    [{mode:6s}] (a) {'PASS' if t['a'] else 'FAIL'} [a1 {'PASS' if t['a1'] else 'FAIL'}, a2 {'PASS' if t['a2'] else 'FAIL'}]  "
      f"(b) {'PASS' if t['b'] else 'FAIL'}  (c) {'PASS' if t['c'] else 'FAIL'}  (d) {'PASS' if t['d'] else 'FAIL'}  (e) {'PASS' if t['e'] else 'FAIL'}"
      f"  ->  {v}")
if not MUTATE:
    prim = V["census"]
    rob = {k: ("bracket-robust" if V["lo07"]["tests"][k] == prim["tests"][k] == V["hi18"]["tests"][k] else "bracket-sensitive")
           for k in ("a", "a1", "a2", "b", "c", "d", "e")}
    RES["bracket_robustness"] = rob
    RES["verdict"] = prim["verdict"]
    P(f"\n  FROZEN VERDICT (primary census, CFG416 fret_of): {prim['verdict']}")
    P("  bracket robustness: " + ", ".join(f"{k} {v}" for k, v in rob.items()))
else:
    m2 = not all(V["dep01"]["tests"][k] for k in "abcd")
    check("M1 f_ret = 1 for real galaxies: verdict is not DISSOLVED and (a), (b) fail", V["one"]["verdict"] != "CLASH DISSOLVED"
          and not V["one"]["tests"]["a"] and not V["one"]["tests"]["b"], f"{V['one']}")
    check("M2 f_ret = 0.01 fails at least one of (a)-(d)", m2, f"{V['dep01']['tests']}")
RES["verdicts"] = V
RES["checks"] = CHK
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; load-bearing failures {nlb}")
json.dump(RES, open(os.path.join(HERE, f"cfg515_verdict_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg515_verdict{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
