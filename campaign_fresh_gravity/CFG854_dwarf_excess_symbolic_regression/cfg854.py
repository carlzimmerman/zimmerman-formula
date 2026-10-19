"""CFG854 -- PySR symbolic regression for the satellite-dwarf extra mass from baryonic inputs, blind across hosts.
Criteria: FROZEN_CRITERIA.md (cbdcf72d5).  Run: JULIA_PKG_OFFLINE=true python3 cfg854.py [K1|MUTATE].  kappa = 1/2 FITTED; not theory closed."""
import os, sys, csv, json, math, numpy as np
os.environ.setdefault("JULIA_PKG_OFFLINE", "true"); os.environ.setdefault("PYTHON_JULIAPKG_OFFLINE", "yes")
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = sys.argv[1] if len(sys.argv) > 1 else ""; assert MODE in ("", "K1", "MUTATE"); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def fnum(x):
    try: return float(x)
    except: return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
R44 = json.load(open(os.path.join(LANES, "CFG844_primordial_free_core", "cfg844_results.json")))["rows"]
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
G, Msun, KPC, PC, a0 = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16, 9.3603e-11
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15)))); law = lambda gN: gN * nu(gN / a0)
rows, drop = [], []
for d in R44:
    nm = d["name"]; Z = fnum(LVD[nm].get("metallicity")); t90 = R24.get(nm, {}).get("tau90")
    if Z is None or t90 is None: drop.append(nm); continue
    rh = d["r12"] * KPC; Mb = d["Mb"]; gl = law(G * (Mb / 2) * Msun / rh ** 2)
    Mex = gl * (10 ** d["delta"] - 1) * rh * rh / G / Msun
    rows.append(dict(name=nm, host=d["host"], x=[math.log10(Mb), math.log10(d["r12"]), Z, t90], y=math.log10(Mex)))
P(f"CFG854  symbolic regression for the dwarf extra mass" + (f"  [{MODE}]" if MODE else "") + f"   N {len(rows)} (dropped, missing [Fe/H] or tau90: {drop})")
rng = np.random.default_rng(854)
if MODE == "K1":
    for r in rows: r["y"] = 7 + 0.5 * (r["x"][1] + 0.5) - 0.3 * (r["x"][0] - 6) + rng.normal(0, 0.1)
from pysr import PySRRegressor
def split(name):
    tr = [r for r in rows if (r["host"] == "mw") == (name == "A")]; te = [r for r in rows if (r["host"] == "mw") != (name == "A")]
    return tr, te
RES = dict(lane="CFG854", mode=MODE, N=len(rows), dropped=drop)
for sp in ("A", "B"):
    tr, te = split(sp)
    Xtr, ytr = np.array([r["x"] for r in tr]), np.array([r["y"] for r in tr]); Xte, yte = np.array([r["x"] for r in te]), np.array([r["y"] for r in te])
    if MODE == "MUTATE": ytr = rng.permutation(ytr)
    rmse = lambda p, y: float(np.sqrt(np.mean((p - y) ** 2)))
    b0 = rmse(np.full_like(yte, ytr.mean()), yte)
    A = np.c_[np.ones(len(Xtr)), Xtr[:, 0], Xtr[:, 1]]; cf = np.linalg.lstsq(A, ytr, rcond=None)[0]; b1 = rmse(np.c_[np.ones(len(Xte)), Xte[:, 0], Xte[:, 1]] @ cf, yte)
    m = PySRRegressor(niterations=60, populations=15, maxsize=12, binary_operators=["+", "-", "*", "/"], unary_operators=[], parallelism="serial",
                      deterministic=True, random_state=854, model_selection="best", verbosity=0, progress=False, temp_equation_file=True)
    m.fit(Xtr, ytr, variable_names=["logM", "logr", "FeH", "t90"])
    ps = rmse(m.predict(Xte), yte); ptr = rmse(m.predict(Xtr), ytr)
    eqs = m.equations_.sort_values("score", ascending=False).head(3)
    top = [dict(eq=str(e), complexity=int(c), loss=float(l)) for e, c, l in zip(eqs["equation"], eqs["complexity"], eqs["loss"])]
    RES[sp] = dict(N_train=len(tr), N_test=len(te), formula=str(m.sympy()), rmse_train=ptr, rmse_test=ps, B0_test=b0, B1_test=b1, B1_coef=cf.tolist(), top3=top)
    P(f"\n  [split {sp}: train {'MW' if sp == 'A' else 'M31+field'} N {len(tr)} -> test N {len(te)}]")
    P(f"     PySR selected: y = {m.sympy()}   (train RMSE {ptr:.3f}, TEST RMSE {ps:.3f})")
    P(f"     baselines test RMSE: B0 constant {b0:.3f}, B1 linear(logM, logr) {b1:.3f}  [B1 coef {cf[0]:.2f} {cf[1]:+.3f} logM {cf[2]:+.3f} logr]")
    for t in top: P(f"       Pareto: c{t['complexity']:2d} loss {t['loss']:.4f}  {t['eq']}")
gen = all(RES[s]["rmse_test"] <= 0.8 * min(RES[s]["B0_test"], RES[s]["B1_test"]) for s in "AB")
lin = all(RES[s]["B1_test"] <= 0.8 * RES[s]["B0_test"] for s in "AB")
cls = "GENERALISING LAW" if gen else ("LINEAR SUFFICES" if lin else "NO GENERALISING STRUCTURE")
if MODE == "K1": cls = f"K1 {'PASS' if all(RES[s]['rmse_test'] <= 0.2 for s in 'AB') else 'FAIL'} (test RMSE {RES['A']['rmse_test']:.3f} / {RES['B']['rmse_test']:.3f})"
RES["cls"] = cls; P(f"\n  CLASS: {cls}")
sfx = f"_{MODE}" if MODE else ""
json.dump(RES, open(os.path.join(HERE, f"cfg854_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg854{sfx}.out"), "w").write("\n".join(OUT) + "\n")
