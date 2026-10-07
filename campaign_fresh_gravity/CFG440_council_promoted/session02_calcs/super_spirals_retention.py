"""Addendum S: super spirals vs the two retention levels (cm08 definition). Run: python3 super_spirals_retention.py [--mutate]"""
import os, sys, math, json, io, contextlib, runpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
sys.argv = [sys.argv[0]]
os.environ.pop("MUTATE", None)
src56p = os.path.join(REPO, "campaign_fresh_gravity", "CFG56_super_spirals_bulge.py")
src56 = open(src56p).read()
g = {"__file__": src56p, "__name__": "cfg56"}
os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src56[:src56.index("def asym(")], "CFG56", "exec"), g)
GALS, pred = g["GALS"], g["pred"]
OUT = []
def P(s=""): print(s); OUT.append(str(s))
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
COSMIC = 0.1200 / 0.02237
res = {}
for foot in ("canonical", "alt"):
    rows = []
    for gg in GALS:
        vlaw, _, Mb_tot = pred(gg, foot, which="law")[:3]
        # cm08 uses the baryons ENCLOSED in the aperture: Newtonian-equivalent enclosed mass g_N r^2 / G from CFG56's own bulge+disc g_N
        # (bug fix after the first run: v1 divided by the total M_b, which is not cm08's definition; disclosed in RESULTS)
        gN = g["gN_bd"](10 ** gg["lMs"], 10 ** gg["lMg"], gg["Rd"], gg["r"], min(max(gg["BT"], 0.0), 1.0), gg["Reb"])
        Mb = gN * (gg["r"] * KPC) ** 2 / G / MSUN
        v = gg["v"]; dv = gg["dv"]; r = gg["r"] * KPC
        Mdyn = (v * 1e3) ** 2 * r / G / MSUN
        Mlaw = Mb if MUT else (Mdyn * (vlaw / v) ** 2)
        f = (Mdyn - Mlaw) / (COSMIC * Mb)
        T = 0.6 * 1.6726e-27 * (v * 1e3) ** 2 / (2 * 1.380649e-23)
        rows.append(dict(name=gg.get("alt", gg.get("name")), v=v, r=gg["r"], Mb=Mb, f=f, T=T, dv=dv, vlaw=vlaw))
    rows.sort(key=lambda x: -x["v"])
    fast = rows[:9]
    rng = np.random.default_rng(5)
    def med_boot(rs):
        fs = np.array([x["f"] for x in rs]); bs = []
        for _ in range(2000):
            i = rng.integers(0, len(rs), len(rs))
            # per-galaxy perturbation: v error and 0.059 dex on M_b
            ff = []
            for k in i:
                x = rs[k]; vv = x["v"] + rng.normal(0, x["dv"]); mb = x["Mb"] * 10 ** rng.normal(0, 0.059)
                Md = (vv * 1e3) ** 2 * x["r"] * KPC / G / MSUN
                Ml = mb if MUT else (x["vlaw"] * 1e3) ** 2 * x["r"] * KPC / G / MSUN * math.sqrt(mb / x["Mb"])   # deep-ish scaling of M_law with M_b (declared approx.)
                ff.append((Md - Ml) / (COSMIC * mb))
            bs.append(np.median(ff))
        return float(np.median(fs)), float(np.std(bs))
    ma, sa = med_boot(rows); mf, sf = med_boot(fast)
    def reading(m, s):
        if abs(m - 0.13) < 2 * s and abs(m - 0.6) > 2 * s: return "GALAXY-LEVEL"
        if abs(m - 0.6) < 2 * s and abs(m - 0.13) > 2 * s: return "GROUP-LEVEL"
        return "BETWEEN"
    P(f"{foot}: all 23 median f = {ma:.3f} +- {sa:.3f} ({reading(ma, sa)}); nine fastest f = {mf:.3f} +- {sf:.3f} ({reading(mf, sf)})")
    P(f"   nine fastest: V {min(x['v'] for x in fast):.0f}-{max(x['v'] for x in fast):.0f} km/s, T_vir {min(x['T'] for x in fast):.1e}-{max(x['T'] for x in fast):.1e} K (step 0.5-2.3e6 K)")
    for x in rows: P(f"     {str(x['name'])[:24]:24s} v {x['v']:5.0f} r {x['r']:4.0f} kpc  logMb {math.log10(x['Mb']):5.2f}  f {x['f']:+.3f}  T {x['T']:.1e}")
    res[foot] = dict(all=(ma, sa), fast=(mf, sf), reading_fast=reading(mf, sf), rows=rows)
json.dump(res, open(os.path.join(HERE, f"super_spirals_retention{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"super_spirals_retention{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    main = json.load(open(os.path.join(HERE, "super_spirals_retention_results.json")))
    rose = res["canonical"]["fast"][0] - main["canonical"]["fast"][0]
    P(f"MUTATE: nine-fastest f rose by {rose:+.3f} -> {'detected (exit 1)' if rose > 0.1 else 'NOT detected (exit 0: control broken)'}")
    sys.exit(1 if rose > 0.1 else 0)
