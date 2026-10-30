#!/usr/bin/env python3
"""X81_core_convergence (committed as X80; renamed) (criteria 62ddc553d0): is X77's native eta a resolution artefact?
T1 same-seed d ln(r0/rvir) / d ln(rconv/rvir), ng 48 -> 64; T2 analytic NFW / Einasto(0.17) cusp fitted with X77's objective.
    python3 x80_core_convergence.py [--mutate]"""
import glob, json, math, os, sys
import numpy as np
from scipy.special import gammainc
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
X77P = os.path.join(RB, "X77_direct_core_surface_density", "x77_direct_eta.py"); X48 = os.path.join(RB, "X48_native_cf_zoom")
src = open(X77P).read(); src = src[:src.index("# K2: formula vs direct integration")]
NS = dict(__file__=X77P, __name__="x77_prefix"); argv0 = sys.argv; sys.argv = [X77P]; exec(compile(src, X77P, "exec"), NS); sys.argv = argv0
fit, BS, AG, XA = NS["fit"], NS["BS"], NS["AG"], NS["XA"]
MUT = "--mutate" in sys.argv
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
eta_of = lambda a: 4 / 3 * a * a / BS(a)

def a_fit_profile(Mfun, xc, n=2000):
    """X77 objective on points uniform in enclosed mass between xc and 1 (as particles are)."""
    xs = np.geomspace(xc, 1, 20001); Ms = Mfun(xs); q = np.linspace(Ms[0], Ms[-1], n)
    u = np.interp(q, Ms, xs); y = np.log(q / Ms[-1])
    return float(min(AG, key=lambda aa: float(np.sum((np.log(BS(aa * u) / BS(aa)) - y) ** 2))))
M_nfw = lambda c: (lambda x: np.log1p(c * x) - c * x / (1 + c * x))
def M_ein(c, al=0.17):
    return lambda x: gammainc(3 / al, 2 / al * (c * x) ** al)
M_sc = lambda a: (lambda x: BS(a * x))

# K1: exact smooth core a = 6 at several xc
k1v = [a_fit_profile(M_sc(6.0), xc) for xc in (0.01, 0.03, 0.1)]
K1 = all(abs(v / 6 - 1) <= 0.02 for v in k1v)
P(f"K1 exact smooth core a=6 at xc 0.01/0.03/0.1 -> a {k1v}: {'PASS' if K1 else 'FAIL'}")

runs = {}
X77R = json.load(open(os.path.join(RB, "X77_direct_core_surface_density", "x77_results.json")))["runs"]
rng = np.random.default_rng(20261030)
for d in sorted(glob.glob(os.path.join(X48, "runs", "M1e12_*"))):
    sn = os.path.join(d, "snap_zf.npz")
    if not os.path.exists(sn): continue
    Z = np.load(sn); x, m = Z["x"], float(Z["m"]); meta = json.loads(str(Z["meta"]))
    rho_mz = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3
    if MUT:
        o0 = XA.measure(x, m, rho_mz, meta["eps"]); c0 = XA.centre(x, m); rr = np.sqrt(((x - c0) ** 2).sum(1))
        inner = np.where(rr < 2 * o0.get("rconv", 0))[0]; drop = rng.choice(inner, len(inner) // 2, replace=False)
        x = np.delete(x, drop, axis=0)
    o, res = fit(x, m, rho_mz, meta["eps"])
    nm = os.path.basename(d)
    if res is None: runs[nm] = dict(flag=o.get("flag")); continue
    runs[nm] = dict(seed=meta["seed"], ng=meta["ng"], a=res["S"]["a"], eta=res["S"]["eta"], xc=o["rconv"] / o["rvir"],
                    x3eps=3 * meta["eps"] / o["rvir"], c_nfw=o.get("c_nfw_fit"), rconv_is_3eps=bool(o["rconv"] <= 3 * meta["eps"] * 1.0000001))
K2 = (not MUT) and abs(runs["M1e12_s1_ng64"]["a"] - X77R["M1e12_s1_ng64"]["S"]["a"]) == 0
if not MUT: P(f"K2 imported X77 fit reproduces X77 a for M1e12_s1_ng64: {runs['M1e12_s1_ng64']['a']} vs {X77R['M1e12_s1_ng64']['S']['a']}: {'PASS' if K2 else 'FAIL'}")

P("\nper run (1e12): ng seed | x_c=rconv/rvir (3eps/rvir) | a  eta | c_nfw | a_cusp NFW  Einasto | a/a_NFW")
for nm, r in sorted(runs.items(), key=lambda kv: (kv[1].get("ng", 0), kv[1].get("seed", 0))):
    if "a" not in r: P(f"  {nm}: {r}"); continue
    if r["c_nfw"]:
        r["a_nfw"] = a_fit_profile(M_nfw(r["c_nfw"]), r["xc"]); r["a_ein"] = a_fit_profile(M_ein(r["c_nfw"]), r["xc"])
    P(f"  ng {r['ng']:2d} s{r['seed']} | {r['xc']:.4f} ({r['x3eps']:.4f}){' 3eps' if r['rconv_is_3eps'] else ''} | {r['a']:6.2f} {r['eta']:6.2f} | {r['c_nfw']} | "
      f"{r.get('a_nfw', float('nan')):6.2f} {r.get('a_ein', float('nan')):6.2f} | {r['a'] / r.get('a_nfw', float('nan')):.2f}")

# T1
S = []
for s in range(1, 10):
    p, q = runs.get(f"M1e12_s{s}_ng48"), runs.get(f"M1e12_s{s}_ng64")
    if p and q and "a" in p and "a" in q and q["xc"] != p["xc"]:
        S.append(dict(seed=s, s=math.log((1 / q["a"]) / (1 / p["a"])) / math.log(q["xc"] / p["xc"]), dlnxc=math.log(q["xc"] / p["xc"]), dlny=math.log(p["a"] / q["a"])))
sv = np.array([d["s"] for d in S]); med = float(np.median(sv))
bt = np.median(sv[np.random.default_rng(20261030).integers(0, len(sv), (10000, len(sv)))], axis=1); b68 = [float(np.percentile(bt, 16)), float(np.percentile(bt, 84))]
P("\nT1 same seed ng 48 -> 64: " + ", ".join(f"s{d['seed']} {d['s']:+.2f} (dln xc {d['dlnxc']:+.2f})" for d in S))
if b68[0] >= 0.5: T1 = "CORE NUMERICAL"
elif b68[1] <= 0.2: T1 = "CORE CONVERGED"
else: T1 = "UNDECIDED"
P(f"T1 median s {med:+.2f} [68% {b68[0]:+.2f}, {b68[1]:+.2f}] (n {len(sv)}): {T1}")
# T2
n64 = [r for r in runs.values() if r.get("ng") == 64 and "a_nfw" in r]
hitN = sum(abs(r["a"] / r["a_nfw"] - 1) <= 0.2 for r in n64); hitE = sum(abs(r["a"] / r["a_ein"] - 1) <= 0.2 for r in n64)
T2 = hitN * 3 >= 2 * len(n64) or hitE * 3 >= 2 * len(n64)
P(f"T2 ng 64: |a/a_cusp - 1| <= 0.2 in NFW {hitN}/{len(n64)}, Einasto {hitE}/{len(n64)}: "
  + ("zoom cores = cusp seen through the resolution cut" if T2 else "zoom cores are not a cusp under the cut"))
V = ("COLLAPSE BRANCH HAS NO CONVERGED eta" if (T1 == "CORE NUMERICAL" and T2) else "NATIVE eta STANDS" if T1 == "CORE CONVERGED" else "UNDECIDED")
P(f"VERDICT: {V}")
# forecast (reported only)
cmed = float(np.median([r["c_nfw"] for r in n64])); xc64 = float(np.median([r["xc"] for r in n64])); x3 = float(np.median([r["x3eps"] for r in n64]))
FC = {}
for lab, xc in (("ng64 median xc", xc64), ("ng80 frozen (64/80)^1", xc64 * 64 / 80), ("ng80 cusp (64/80)^1.5", xc64 * (64 / 80) ** 1.5), ("3eps floor", x3), ("xc 0.01", 0.01)):
    aN = a_fit_profile(M_nfw(cmed), max(xc, 1e-4)); FC[lab] = dict(xc=xc, a=aN, eta=float(eta_of(aN)))
    P(f"  forecast NFW c {cmed:.2f} at {lab} (xc {xc:.4f}): a {aN:.2f}, eta {eta_of(aN):.2f}  [SPARC limit 21.2]")
P("kappa = 1/2 FITTED; not theory closed; zooms are collisionless (floor physics not in them)")
tag = "_MUTATE" if MUT else ""
if MUT:
    base = json.load(open(os.path.join(HERE, "x80_results.json")))["runs"]
    mv = [runs[k]["a"] < base[k]["a"] for k in runs if "a" in runs[k] and "a" in base.get(k, {})]
    P(f"MUTATE: fitted a fell in {sum(mv)}/{len(mv)} runs: {'PASS' if sum(mv) * 3 >= 2 * len(mv) else 'FAIL'}")
json.dump(dict(K1=K1, K2=K2, runs=runs, T1=dict(per_seed=S, median=med, b68=b68, label=T1), T2=dict(nfw=hitN, ein=hitE, n=len(n64), match=T2),
               verdict=V, forecast=FC), open(os.path.join(HERE, f"x80_results{tag}.json"), "w"), indent=1)
open(os.path.join(HERE, f"x80{tag}.out"), "w").write("\n".join(OUT) + "\n")
