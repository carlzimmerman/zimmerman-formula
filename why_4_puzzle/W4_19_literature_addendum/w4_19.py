#!/usr/bin/env python3
"""W4-19 -- six published a0-Lambda relations missing from the register: exact kappa, pi content, class.
Criteria: FROZEN_CRITERIA.md (committed alone, 2f0d6413c). Light: sympy only. Run from the repo root:
    python3 why_4_puzzle/W4_19_literature_addendum/w4_19.py > why_4_puzzle/W4_19_literature_addendum/w4_19.out
    W4_19_MUTATE=1 ... > .../w4_19_MUTATE.out   (Omega_L -> 0.70; exit 1 when the control bites)
kappa = 1/2 FITTED. Not theory closed.
"""
import json, os, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("W4_19_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
W_DATA = (0.227, 0.607)
OUT, checks = [], []


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def pi_content(k):
    e = sp.simplify(k ** 2)
    if not e.has(sp.pi):
        return "pi-free"
    num, den = sp.fraction(sp.together(e))
    d = sp.degree(num, sp.pi) - sp.degree(den, sp.pi)
    return f"pi^{d} ({'odd' if d % 2 else 'even'})"


G, c, H0, a0 = sp.symbols("G c H0 a0", positive=True)
OL = sp.Rational(70, 100) if MUT else sp.Rational(685, 1000)
OM = 1 - OL
rhoL = OL * 3 * H0 ** 2 / (8 * sp.pi * G)
HL = sp.sqrt(8 * sp.pi * G * rhoL / 3)
LAM = 8 * sp.pi * G * rhoL / c ** 2
kap = lambda a: sp.simplify(a / (c * sp.sqrt(G * rhoL)))

E = {}
# L1 Zhao 2008: rho_L c^2 = a0^2/(8 pi G) read as an equality
a0_L1 = sp.solve(sp.Eq(rhoL * c ** 2, a0 ** 2 / (8 * sp.pi * G)), a0)[0]
E["L1"] = dict(work="Zhao 2008 arXiv:0802.1775", cls="any", reading="rho_L c^2 = a0^2/(8 pi G) (paper: order statement)", k=kap(a0_L1))
# L2 Maeder 2023 eq. 80 at n = 1
n = 1
E["L2"] = dict(work="Maeder 2023 arXiv:2302.06206", cls="free", reading="a0 = ((1-Om)^2/4) n c H0, n = 1",
               k=kap((1 - OM) ** 2 / 4 * n * c * H0))
# L3 van Putten 2017: a0 = omega0/(2 pi), omega0 = sqrt(1-q) H, Lambda = omega0^2
k3a = kap(c ** 2 * sp.sqrt(LAM) / (2 * sp.pi))                    # (a) Lambda = omega0^2/c^2 with Lambda = 8 pi G rho_L/c^2
q0 = OM / 2 - OL
k3b = kap(sp.sqrt(1 - q0) * c * H0 / (2 * sp.pi))                 # (b) LCDM q0, H = H0
E["L3"] = dict(work="van Putten 2017 arXiv:1707.01619", cls="menu", reading="(a) Lambda = omega0^2; (b) LCDM q0, H = H0",
               members={"a": k3a, "b": k3b})
# L4 Luo 2026: a0 = 2 beta^2 sqrt(Lambda/12) c^2, beta^2 = 1/3 (written as cos^2 alpha average)
beta2 = sp.Integer(1) / 3
E["L4"] = dict(work="Luo 2026 arXiv:2602.14515", cls="odd", reading="a0 = 2 beta^2 c^2 sqrt(Lambda/12), beta^2 ~ 1/3",
               k=kap(2 * beta2 * c ** 2 * sp.sqrt(LAM / 12)))
# L5 Navarro & Van Acoleyen 2006: free
E["L5"] = dict(work="Navarro & Van Acoleyen 2006 arXiv:gr-qc/0512109 (partial)", cls="free", reading="a0 = c mu, mu set by the chosen f(R,P,Q)", k=None)
# L6 Funkhouser 2006: a0 ~ c Lambda^(1/2) with his Lambda = H_L^2
E["L6"] = dict(work="Funkhouser 2006 arXiv:physics/0502049", cls="free", reading="a0 ~ c H_Lambda (order statement; factor b free)",
               k=kap(c * HL))

P("W4-19  published a0-Lambda relations missing from the register" + (f"  [MUTATE Omega_L = {OL}]" if MUT else ""))
P(f"literature lane. Omega_L = {float(OL)}. kappa = 1/2 FITTED. Not theory closed.\n")
res = {}
for key, e in E.items():
    if e.get("members"):
        mem = {m: dict(exact=str(sp.simplify(v)), value=float(v), pi=pi_content(v), in_window=W_DATA[0] <= float(v) <= W_DATA[1])
               for m, v in e["members"].items()}
        res[key] = dict(work=e["work"], cls=e["cls"], reading=e["reading"], members=mem)
        P(f"{key} {e['work']}: {e['reading']} -> MENU")
        for m, d in mem.items():
            P(f"     ({m}) kappa = {d['exact']} = {d['value']:.4f} [{d['pi']}; in W_data {d['in_window']}]")
    elif e["k"] is None:
        res[key] = dict(work=e["work"], cls=e["cls"], reading=e["reading"])
        P(f"{key} {e['work']}: {e['reading']} -> FREE")
    else:
        v = float(e["k"])
        res[key] = dict(work=e["work"], cls=e["cls"], reading=e["reading"], exact=str(e["k"]), value=v, pi=pi_content(e["k"]),
                        in_window=W_DATA[0] <= v <= W_DATA[1])
        P(f"{key} {e['work']}: {e['reading']} -> kappa = {e['k']} = {v:.4f} [{res[key]['pi']}; in W_data {res[key]['in_window']}; class {e['cls']}]")

half = [k for k, d in res.items() if d.get("exact") == "1/2" or any(m["exact"] == "1/2" for m in d.get("members", {}).values())]
lane = "A PUBLISHED ROUTE GIVES 1/2" if half else "NOTHING NEW"
P("")
if not MUT:
    want = {"L1": 5.013, "L2": 0.410, "L4": 0.965, "L6": 2.894}
    got = {k: res[k]["value"] for k in want}
    got3 = (res["L3"]["members"]["a"]["value"], res["L3"]["members"]["b"]["value"])
    check("K1 reproduce the sweep's numbers to 1e-3", f"{ {k: round(v, 4) for k, v in got.items()} }, L3 {tuple(round(x, 4) for x in got3)}",
          all(abs(got[k] - want[k]) < 1e-3 for k in want) and abs(got3[0] - 0.798) < 1e-3 and abs(got3[1] - 0.688) < 1e-3)
    miss = sp.simplify((4 * a0 ** 2 / G) / (a0 ** 2 / (8 * sp.pi * G)))
    check("K2 framework 4 a0^2/G vs field energy a0^2/(8 pi G)", f"ratio {miss}", miss == 32 * sp.pi)
P(f"LANE VERDICT: {lane}")
json.dump(dict(mutate=MUT, omega_L=float(OL), entries=res, lane_verdict=lane, checks=checks),
          open(os.path.join(HERE, f"w4_19_results{SUF}.json"), "w"), indent=1, default=str)
if MUT:
    try:
        b = json.load(open(os.path.join(HERE, "w4_19_results.json")))["entries"]
        moved = abs(res["L2"]["value"] - b["L2"]["value"]) > 1e-6 and abs(res["L3"]["members"]["b"]["value"] - b["L3"]["members"]["b"]["value"]) > 1e-6
        fixed = all(abs(res[k]["value"] - b[k]["value"]) < 1e-12 for k in ("L1", "L4", "L6")) and \
            abs(res["L3"]["members"]["a"]["value"] - b["L3"]["members"]["a"]["value"]) < 1e-12
        P(f"MUTATE: Omega-dependent entries moved {moved}; pure-number entries unchanged {fixed}")
        sys.exit(1 if (moved and fixed) else 2)
    except OSError:
        sys.exit(2)
P(f"checks: {sum(x['pass'] for x in checks)}/{len(checks)} pass")
sys.exit(0 if all(x["pass"] for x in checks) else 1)
