#!/usr/bin/env python3
"""DT1_threshold_tournament: pre-registered zero-parameter candidates for the cold dark energy switch threshold T, against
the frozen CF2/CL1 window. FROZEN_CRITERIA.md committed alone first (d782d8ec78).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I dt1_tournament.py      (DT1_MUTATE=1 twin)
"""
import os, sys, io, json, math, contextlib, resource
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import brentq

MUT = os.environ.get("DT1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = open(os.path.join(HERE, f"dt1_tournament{TAG}.out"), "w")
RES = {"lane": "DT1_threshold_tournament", "criteria": "d782d8ec78", "mutate": MUT, "checks": {}, "candidates": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


P("DT1_threshold_tournament" + (" [MUTATE: a0 footings swapped; K0 target x1.01 - control output]" if MUT else "") +
  ": criteria d782d8ec78; kappa = 1/2 FITTED; footings never pooled; not theory closed")

# ---------------- record backgrounds (EM1's CLASS, as X43) ----------------
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- halo profiles")], EM1SRC, "exec"), NE)
sys.argv = argv0
DC, OMEGA, DELTA = 1.686, 0.974, 18 * math.pi ** 2
B1 = 3 * math.log(2) - math.pi / 2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
if MUT:
    A0 = {"canonical": A0["alt"], "alt": A0["canonical"]}
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
SIG_PC = {f: A0[f] / (2 * math.pi * G) * PC ** 2 / MSUN for f in A0}
EPS = {}
for tag, bg in NE["BGS"].items():
    cc = bg["c"]; h = bg["h"]; Om = float(cc.Omega_m())
    zg = np.linspace(0, 30, 3001); Dg = np.array([cc.scale_independent_growth_factor(z) for z in zg]); Dg /= Dg[0]
    lMg = np.linspace(7.0, 16.5, 191); sigf = bg["cB"].__defaults__[1]
    s2 = np.array([float(sigf(10 ** l)[0]) ** 2 for l in lMg])
    EPS[tag] = dict(rhom0=Om * 2.775e11 * h ** 2, zg=zg, Dg=Dg, lMg=lMg, s2=s2, Om=Om, h=h)


def zform(tag, M):
    e = EPS[tag]; s2i = lambda l: float(np.interp(l, e["lMg"], e["s2"]))
    S = math.sqrt(max(s2i(math.log10(M / 2)) - s2i(math.log10(M)), 0.0)); Df = DC / (DC + OMEGA * S)
    return float(np.interp(-Df, -e["Dg"], e["zg"])) if Df < 1 else 0.0


def sigma_coll(tag, M):
    zf = zform(tag, M); e = EPS[tag]; rho = DELTA * e["rhom0"] * (1 + zf) ** 3
    rf = (3 * (M / 2) / (4 * math.pi * rho)) ** (1 / 3)
    return rho * rf / 1e12


eta = lambda cf: 4.0 / (3.0 * B1) * cf ** 1.25
X48 = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_analyze_results_ng48_A2.json")))["cf_by_mass"]
S9 = [X48[k] for k in ("1e+12", "1e+13", "1e+14")]
cf_nat = lambda M: float(np.interp(math.log10(M), [12.0, 13.0, 14.0], S9))
WIN = {"canonical": (12.1, 12.5), "alt": (12.2, 12.5)}


def grade(f, lt):
    if lt is None or not np.isfinite(lt): return "MISS (no root)"
    lo, hi = WIN[f]
    if lo < lt <= hi: return "HIT"
    if lo - 0.15 < lt <= hi + 0.15: return "NEAR"
    return "MISS" + (" (untested above window)" if lt > hi else "")


def root(fun, lo=9.0, hi=16.5):
    xs = np.linspace(lo, hi, 300); v = [fun(x) for x in xs]
    for i in range(len(xs) - 1):
        if np.sign(v[i]) != np.sign(v[i + 1]):
            return brentq(fun, xs[i], xs[i + 1], xtol=1e-6)
    return None


TAGA = "A_c2b_refit"
CAND = {}
for f in ("canonical", "alt"):
    CAND.setdefault("A", {})[f] = root(lambda l: math.log(eta(4.0) * sigma_coll(TAGA, 10 ** l)) - math.log(SIG_PC[f]))
    CAND.setdefault("B", {})[f] = root(lambda l: math.log(eta(2 ** (8 / 9)) * sigma_coll(TAGA, 10 ** l)) - math.log(SIG_PC[f]))
    CAND.setdefault("C", {})[f] = root(lambda l: math.log(eta(cf_nat(10 ** l)) * sigma_coll(TAGA, 10 ** l)) - math.log(SIG_PC[f]))
k0t = {"canonical": 12.09 * (1.01 if MUT else 1.0), "alt": 12.43}
k0 = all(CAND["A"][f] is not None and abs(CAND["A"][f] - k0t[f]) <= 0.01 for f in A0)
check("K0", k0, f"A (c_f 4) crossover {CAND['A']['canonical']:.3f} / {CAND['A']['alt']:.3f}", "12.09 / 12.43 within 0.01")
k1 = abs(zform(TAGA, 1e12) - 0.944) <= 0.005 and abs(zform(TAGA, 10 ** 12.3) - 0.886) <= 0.005
check("K1", k1, f"z_f(1e12) {zform(TAGA, 1e12):.3f}, z_f(1e12.3) {zform(TAGA, 10 ** 12.3):.3f}", "0.944 / 0.886 within 0.005")
# D, E: formation epochs (footing-independent)
Om = EPS[TAGA]["Om"]; OL = 1 - Om
z_acc = (2 * OL / Om) ** (1 / 3) - 1; z_eq = (OL / Om) ** (1 / 3) - 1
for cid, zt in (("D", z_acc), ("E", z_eq)):
    lt = root(lambda l: zform(TAGA, 10 ** l) - zt, 9.0, 16.0)
    CAND[cid] = {"canonical": lt, "alt": lt, "z_target": zt}
# F: GSMF knee via EM1 relation
EMR = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"][TAGA]["R1"]
INP = os.path.join(REB, "..", "closure_program_2026_10_27", "population", "inputs.json")
knee = json.load(open(INP))["driver2022"]["log10_Mstar_h70_minus2"] + 2 * math.log10(0.70 / 0.6856427)
for cid, fac in (("F", 1.0), ("F_var1.2", 1.2)):
    lt = EMR["a"] + EMR["b"] * (knee + math.log10(fac) - 10)
    CAND[cid] = {"canonical": lt, "alt": lt, "log_Mb": knee + math.log10(fac)}
# G: law supplies the fair share at the halo edge
NAT_h, NAT_OM, NAT_wb = 0.6856427, 0.2976016, 0.0223081
OB = NAT_wb / NAT_h ** 2; RR = 1 + (NAT_OM - OB) / OB
rhoc = 3 * (100 * NAT_h * 1e3 / MPC) ** 2 / (8 * math.pi * G)
nu = lambda y: 0.5 + math.sqrt(0.25 + 1.0 / y)
EDGES = {"G (R200)": 200 * rhoc, "G (R500)": 500 * rhoc, "G (r_ta, 5.55 rho_m)": 5.55 * NAT_OM * rhoc}
for cid, rho_edge in EDGES.items():
    for f in ("canonical", "alt"):
        def fun(l):
            Mb = 10 ** l * MSUN; Mt = RR * Mb
            R = (3 * Mt / (4 * math.pi * rho_edge)) ** (1 / 3)
            return math.log(nu(G * Mb / R ** 2 / A0[f])) - math.log(RR)
        lb = root(fun, 6.0, 17.0)
        CAND.setdefault(cid, {})[f] = None if lb is None else lb + math.log10(RR)
# report + verdict
P("\n== CANDIDATES (log10 T / Msun; window canonical (12.1, 12.5], alt (12.2, 12.5])")
best = {}
for cid in ("A", "B", "C", "D", "E", "F", "F_var1.2", "G (R200)", "G (R500)", "G (r_ta, 5.55 rho_m)"):
    v = CAND[cid]
    gr = {f: grade(f, v[f]) for f in ("canonical", "alt")}
    RES["candidates"][cid] = {"logT": {f: v[f] for f in ("canonical", "alt")}, "grade": gr, **{k: x for k, x in v.items() if k not in ("canonical", "alt")}}
    fmt = lambda x: "none" if x is None else f"{x:.2f}"
    P(f"  {cid:22s} canonical {fmt(v['canonical']):>6s} {gr['canonical']:<32s} alt {fmt(v['alt']):>6s} {gr['alt']}" + ("   [reference, not a derivation]" if cid == "A" else ""))
nonref = [c for c in RES["candidates"] if c != "A" and not c.startswith("F_var")]
hits = [c for c in nonref if RES["candidates"][c]["grade"]["canonical"] == "HIT" and RES["candidates"][c]["grade"]["alt"] in ("HIT", "NEAR")]
nears = [c for c in nonref if RES["candidates"][c]["grade"]["canonical"] in ("HIT", "NEAR")]
V = (f"T DERIVED (candidate {', '.join(hits)})" if hits else (f"T NEAR (candidate {', '.join(nears)})" if nears else "T NOT DERIVED"))
RES["verdict"] = V
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("K2", peak < 1.0, f"peak RSS {peak:.2f} GB", "< 1 GB")
P(f"\n== VERDICT: {V}")
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
json.dump(RES, open(os.path.join(HERE, f"dt1_tournament_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
