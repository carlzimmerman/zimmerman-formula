#!/usr/bin/env python3
"""W4-20 -- can the touching-horizon lattice (W4-18 B7, the record's only pi-free 1/2) be the vacuum?
Criteria: FROZEN_CRITERIA.md (committed alone, 5d7db2b16). V1 von Laue, V2 assigned-w reading, V3 frozen p-brane networks.
Light: sympy only. Run from the repo root:
    python3 why_4_puzzle/W4_20_can_the_lattice_be_the_vacuum/w4_20.py > why_4_puzzle/W4_20_can_the_lattice_be_the_vacuum/w4_20.out
    W4_20_MUTATE=1 ... > .../w4_20_MUTATE.out    (MU1 no shell, MU2 non-relativistic string, MU3 w = 0; exit 1 when all bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import json, os, re, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("W4_20_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, checks, res = [], [], {}


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


G, c, rho, R, m, d, r, w = sp.symbols("G c rho R m d r w", real=True)
pos = dict(positive=True)
G, c, rho, R, m, d, r = [sp.Symbol(s.name, **pos) for s in (G, c, rho, R, m, d, r)]
P("W4-20  can the touching-horizon lattice be the vacuum?" + ("  [MUTATE MU1-MU3]" if MUT else ""))
P("theory lane. kappa = 1/2 FITTED. Not theory closed.\n")

# --- COMPUTE START ---
SHELL = not MUT                 # MU1: remove the shell
STRING_TZZ = 0 if MUT else -1   # MU2: non-relativistic string (T^zz = 0) instead of Nambu-Goto (T^zz = -mu c^2)
W_V2 = 0 if MUT else -1         # MU3: w = 0 in V2

# V1 von Laue: ball of vacuum held static by a thin shell with surface stress -gamma
P("V1 von Laue: ball of vacuum (T00 = rho c^2, P = -rho c^2) inside a thin shell with surface stress -gamma")
gam, sig_s = sp.symbols("gamma sigma_s", real=True)
P_in, P_out = -rho * c ** 2, 0
V, A = sp.Rational(4, 3) * sp.pi * R ** 3, 4 * sp.pi * R ** 2
if SHELL:
    # radial force balance on a shell patch of half-angle th: pressure push (P_in - P_out) * pi (R th)^2 against the
    # inward pull of the rim tension gamma * 2 pi R th * sin(th), to leading order in th
    th = sp.symbols("theta", positive=True)
    balance = sp.series((P_in - P_out) * sp.pi * (R * th) ** 2 - gam * 2 * sp.pi * R * th * sp.sin(th), th, 0, 3).removeO()
    gsol = sp.solve(sp.Eq(balance, 0), gam)[0]
    trace = sp.simplify(3 * P_in * V + (-gsol) * 2 * A)
    E_shell = sig_s * A
    M_act = sp.simplify((rho * c ** 2 * V + E_shell + trace) / c ** 2)
    P(f"  static balance -> gamma = {gsol}  ({'compressive: gamma < 0' if sp.simplify(gsol).is_negative else 'tensile'})")
    P(f"  von Laue trace  int T^ii dV = 3 P_in V + 2(-gamma) A = {trace}")
    P(f"  active (Tolman) mass = (rho c^2 V + sigma_s A + int T^ii)/c^2 = {M_act}  (> 0 for shell energy sigma_s >= |gamma| >= 0)")
    w_eff = sp.simplify(trace / 3 / (rho * c ** 2 * V + E_shell))
    P(f"  lattice of such elements: <T^ii>/3 / <T00> = w_eff = {w_eff}")
    res["V1"] = dict(gamma=str(gsol), trace=str(trace), M_act=str(M_act), w_eff=str(w_eff), dust=bool(w_eff == 0))
else:
    trace = sp.simplify(3 * P_in * V)
    M_act = sp.simplify((rho * c ** 2 * V + trace) / c ** 2)
    P(f"  [MU1] no shell: int T^ii dV = {trace}; Komar active mass = {M_act} (not self-bound, repulsive)")
    res["V1"] = dict(trace=str(trace), M_act=str(M_act), w_eff=None, dust=False)

# V2 assigned-w reading
P("\nV2 assigned-w reading: active mass m(1+3w), pull G m_act/d^2, touching d = 2 r_s(m_act), rho = m/d^3 (simple cubic)")
mact = m * (1 + 3 * w)
rs = 2 * G * mact / c ** 2
dsol = 2 * rs                                       # touching: spacing equals two horizon radii
pull = G * mact / d ** 2
k2 = sp.simplify((pull ** 2 / (G * (m / d ** 3) * c ** 2)).subs(d, dsol))
P(f"  kappa^2(w) = {sp.factor(k2)}")
horizon = sp.solve(sp.Gt(1 + 3 * w, 0), w)
P(f"  a horizon (r_s > 0) needs m_act > 0: {horizon}")
wv = sp.Integer(W_V2)
defined = bool((1 + 3 * wv) > 0)
k2v = k2.subs(w, wv)
P(f"  at w = {wv}: m_act = {mact.subs(w, wv)}; touching condition {'defined' if defined else 'UNDEFINED (no horizon for negative mass)'}"
  + (f"; kappa = {sp.sqrt(k2v)}" if defined else ""))
res["V2"] = dict(kappa2_w=str(sp.factor(k2)), w=int(W_V2), defined=defined, kappa=(str(sp.sqrt(k2v)) if defined else None))

# V3 frozen p-brane networks
P("\nV3 frozen p-brane networks (single element at rest; Gauss-law weak field of the active density)")
mu, lam, Sig = sp.symbols("mu lambda Sigma", positive=True)
elements = {
    "p=0 point": dict(T00=m * c ** 2, Tii=0, field=lambda q: 4 * sp.pi * G * q / (4 * sp.pi * r ** 2), dim=0),
    "p=1 string": dict(T00=mu * c ** 2, Tii=STRING_TZZ * mu * c ** 2, field=lambda q: 4 * sp.pi * G * q / (2 * sp.pi * r), dim=1),
    "p=2 wall": dict(T00=Sig * c ** 2, Tii=-2 * Sig * c ** 2, field=lambda q: 4 * sp.pi * G * q / 2, dim=2),
}
v3 = {}
for nm, e in elements.items():
    act = sp.simplify((e["T00"] + e["Tii"]) / c ** 2)
    g = sp.simplify(e["field"](act))
    w_net = sp.simplify(e["Tii"] / 3 / e["T00"])
    pifree = (g != 0) and not g.has(sp.pi)
    v3[nm] = dict(active=str(act), field=str(g), w_network=str(w_net), pi_free_nonzero=bool(pifree))
    P(f"  {nm:10s}: active density {act}; weak-field pull {g}; network w = {w_net}; pi-free nonzero pull {pifree}")
P(f"  string conical deficit (Nambu-Goto): 8 pi G mu / c^2 = {8 * sp.pi * G * mu / c ** 2}")
neg_ok = [nm for nm, x in v3.items() if sp.sympify(x["w_network"]) < 0 and x["pi_free_nonzero"]]
P(f"  w < 0 elements with a pi-free nonzero pull: {neg_ok or 'none'}")
res["V3"] = dict(elements=v3, negative_w_pifree=neg_ok)
# --- COMPUTE END ---

P("")
if not MUT:
    check("K1 von Laue trace = 0 at the static-balance gamma", res["V1"]["trace"], res["V1"]["trace"] == "0")
    komar = sp.simplify((rho * c ** 2 + 3 * P_in) * V / c ** 2)
    check("K2 bare vacuum ball Komar active mass = -2 rho V", komar, sp.simplify(komar + 2 * rho * V) == 0)
    q = sp.symbols("q", positive=True)
    k3 = [sp.simplify(elements[k]["field"](q)) for k in elements]
    check("K3 Gauss fields point/line/sheet = G q/r^2, 2 G q/r, 2 pi G q", k3,
          [sp.simplify(k3[0] - G * q / r ** 2), sp.simplify(k3[1] - 2 * G * q / r), sp.simplify(k3[2] - 2 * sp.pi * G * q)] == [0, 0, 0])
    k4 = sp.sqrt(k2.subs(w, 0))
    w418 = json.load(open(os.path.join(os.path.dirname(HERE), "W4_18_borrowed_exact_numbers", "w4_18_results.json")))["items"]["B7"]["members"]["sc"]["kappa_exact"]
    check("K4 V2 at w = 0 reproduces W4-18's simple-cubic kappa", f"{k4} vs {w418}", str(k4) == w418)
    src = open(os.path.abspath(__file__)).read()
    blk = src.split("# --- COMPUTE START ---")[1].split("# --- COMPUTE END ---")[0]
    bad = [p for p in (r"(?<![\d.])0\.5(?!\d)", r"(?<![\w.)])1\s*/\s*2(?!\d)", r"(?<![\d.])0\.25(?!\d)", r"(?<![\w.)])1\s*/\s*4(?!\d)",
                       r"Rational\(\s*1\s*,\s*[24]\s*\)", r"S\.Half") if re.search(p, blk)]
    check("I1 forbidden-token scan of the compute block", bad or "clean", not bad)

v1 = res["V1"]["dust"]
v2 = not res["V2"]["defined"]
v3c = not res["V3"]["negative_w_pifree"]
lane = ("THE LATTICE 1/2 CANNOT BE THE VACUUM" if (v1 and v2 and v3c) else
        "A VACUUM LATTICE KEEPS 1/2" if (res["V2"]["defined"] and W_V2 == -1) or res["V3"]["negative_w_pifree"] else "PARTIAL")
P(f"V1 static self-bound lattice is dust: {v1};  V2 touching undefined at w = -1: {v2};  V3 no w<0 pi-free pull: {v3c}")
P(f"LANE VERDICT: {lane}")
json.dump(dict(mutate=MUT, results=res, lane_verdict=lane, checks=checks), open(os.path.join(HERE, f"w4_20_results{SUF}.json"), "w"),
          indent=1, default=str)
if MUT:
    try:
        b = json.load(open(os.path.join(HERE, "w4_20_results.json")))["results"]
        mu_ok = {"MU1 no shell: not dust, active mass changes sign": (not res["V1"]["dust"]) and b["V1"]["dust"],
                 "MU2 non-relativistic string: pi-free pull returns": res["V3"]["elements"]["p=1 string"]["pi_free_nonzero"]
                 and not b["V3"]["elements"]["p=1 string"]["pi_free_nonzero"],
                 "MU3 w = 0: touching defined, simple-cubic kappa returns": res["V2"]["defined"] and not b["V2"]["defined"]}
        for k, ok in mu_ok.items():
            P(f"MUTATE {k}: {ok}")
        sys.exit(1 if all(mu_ok.values()) else 2)
    except OSError:
        sys.exit(2)
P(f"checks: {sum(x['pass'] for x in checks)}/{len(checks)} pass")
sys.exit(0 if all(x["pass"] for x in checks) else 1)
