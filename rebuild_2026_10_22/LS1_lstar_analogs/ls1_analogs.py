#!/usr/bin/env python3
"""LS1_lstar_analogs (criteria 7c800267d0): SPARC Milky Way analogs on route E's X73 PRIMARY halos, via X76's X74 base exec.
python3 ls1_analogs.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; HF = 0.5 if MUT else 1.0
X74F = os.path.join(REB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
END = '{"__file__": os.path.join(HERE, "x74_native_cf.py"), "__name__": "__main__"}'
assert TX.count(END) == 1; TX = TX.replace(END, "LSNS")
os.environ.update(X74_CF="const4", X74_CFMULT="1", X73_FSTAR="0.034", X73_SLOPE="2.7774425603108597", PYTHONHASHSEED="0")
NS = {"__file__": os.path.join(HERE, "ls1_base.py"), "__name__": "__main__"}
D = {"__file__": X74F, "__name__": "x74_ro", "LSNS": NS}; argv0 = sys.argv
try: exec(compile(TX, X74F, "exec"), D)
except SystemExit: pass
sys.argv = argv0
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
GALS, fit_one, pooled, UPS = NS["GALS"], NS["fit_one"], NS["pooled"], NS["EM"]["UPS"] if "EM" in NS else None
if UPS is None: UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
B, solve_r0, sigma_coll, eta_of, SIG, BGS = NS["B"], NS["solve_r0"], NS["sigma_coll"], NS["eta_of"], NS["SIG"], NS["BGS"]
GE, MSUNE, MPCE, PC2 = NS["GE"], NS["MSUNE"], NS["MPCE"], NS["PC2"]
MRT = os.path.join(REB, "..", "real_research", "data", "SPARC_Lelli2016c.mrt")
TAB = {}
for l in open(MRT):
    p = l.split()
    if len(p) < 18: continue
    try: TAB[p[0]] = dict(inc=float(p[5]), rd=float(p[11]), vf=float(p[15]), Q=int(p[17]))
    except ValueError: pass
TAG = "A_c2b_refit"; I05 = int(np.argmin(abs(UPS - 0.50))); assert abs(UPS[I05] - 0.50) < 1e-9
KPC = MPCE / 1e3
def halo(q, f, tag, c):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    M200 = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
    s = max(SIG[f], eta_of(c) * sigma_coll(tag, M200)[0] * MSUNE / PC2); r0 = solve_r0(M200 * MSUNE, R200, s)
    return GE * math.pi * s * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
def dv(q, gh, vobs=None):
    t = TAB[q["name"]]; x = q["Rm"] / KPC / t["rd"]; m = (x >= 2) & (x <= 4) & q["OK"][:, I05]
    if not m.any(): return None
    v = np.sqrt((q["GB"][:, I05] + gh) * q["Rm"]) / 1e3
    return float(np.mean(v[m] - (q["Vobs"][m] if vobs is None else vobs[m])))
def row(q, f, c, tag=TAG):
    gh = HF * halo(q, f, tag, c); w, s_, iu = fit_one(q, np.log10(np.maximum(q["GB"] + gh[:, None], 1e-300)))
    return float(w), float(s_), int(iu), dv(q, gh)
def sel(lo, hi):
    return [q for q in GALS if q["name"] in TAB and lo <= TAB[q["name"]]["vf"] <= hi and TAB[q["name"]]["Q"] <= 2 and TAB[q["name"]]["inc"] >= 30]
def summ(qs, f, c):
    r = [row(q, f, c) for q in qs]; d = [x[3] for x in r if x[3] is not None]
    return dict(n=len(qs), n_nopts=sum(x[3] is None for x in r), U_median=float(np.median(UPS[[x[2] for x in r]])), dV=float(np.median(d)),
                dV16=float(np.percentile(d, 16)), dV84=float(np.percentile(d, 84)),
                gal={q["name"]: dict(U=float(UPS[x[2]]), dV=x[3], vf=TAB[q["name"]]["vf"], rd=TAB[q["name"]]["rd"]) for q, x in zip(qs, r)})
def verdict(s):
    if s["n"] < 5: return "UNDECIDED"
    if s["U_median"] > 0.80 or s["dV"] < -15: return "SYSTEMATIC L* DEFICIT"
    if 0.50 <= s["U_median"] <= 0.70 and abs(s["dV"]) <= 10: return "MILKY WAY IS THE OUTLIER"
    return "MIXED"
P("LS1 SPARC Milky Way analogs (criteria 7c800267d0); kappa = 1/2 FITTED; footings never pooled; not theory closed" + (" [MUTATE halo x 0.5]" if MUT else ""))
RES = dict(criteria="7c800267d0", mutate=MUT, footings={})
if not MUT:
    X = json.load(open(os.path.join(REB, "X73_smooth_core_all_measured", "x73_results_fs0.034_S_nat_s2.7774.json")))["footings"]; d = 0.0
    for f in ("canonical", "alt"):
        for t in BGS:
            r = [row(q, f, 4.0, t) for q in GALS]; s = pooled([a[0] for a in r], [a[1] for a in r], [a[2] for a in r]); j = X[f]["sparc"][t]
            d = max(d, abs(s["rms"] - j["rms"]), abs(s["U_median"] - j["U_median"]))
    P(f"K1 all galaxies c 4 reproduce X73 SPARC: max |d| {d:.1e}: {'PASS' if d == 0 else 'FAIL'}"); RES["K1"] = d == 0
    q = sel(200, 250)[0]; gh = halo(q, "canonical", TAG, 4.0); vm = np.sqrt((q["GB"][:, I05] + gh) * q["Rm"]) / 1e3
    k2 = abs(dv(q, gh, vm)); P(f"K2 synthetic self-match |dV| {k2:.1e}: {'PASS' if k2 < 1e-6 else 'FAIL'}"); RES["K2"] = k2 < 1e-6
for f in ("canonical", "alt"):
    a = summ(sel(200, 250), f, 4.0); c = summ(sel(100, 150), f, 4.0); n = summ(sel(200, 250), f, 8.05); v = verdict(a)
    RES["footings"][f] = dict(analogs=a, control=c, converged_reported=n, verdict=v)
    P(f"{f}: analogs n {a['n']} (no 2-4 R_d pts {a['n_nopts']}), median U {a['U_median']:.2f}, dV {a['dV']:+.1f} [{a['dV16']:+.1f}, {a['dV84']:+.1f}] km/s -> {v}")
    P(f"   control V_flat 100-150: n {c['n']}, median U {c['U_median']:.2f}, dV {c['dV']:+.1f} [{c['dV16']:+.1f}, {c['dV84']:+.1f}]")
    P(f"   reported converged eta (c_f-eq 8.05): median U {n['U_median']:.2f}, dV {n['dV']:+.1f}")
    if f == "canonical":
        for k, g in sorted(a["gal"].items(), key=lambda kv: kv[1]["vf"]): P(f"     {k:<10} Vf {g['vf']:5.1f} Rd {g['rd']:4.2f} U {g['U']:.2f} dV {g['dV'] if g['dV'] is None else round(g['dV'], 1)}")
tag = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"ls1_results{tag}.json"), "w"), indent=1); open(os.path.join(HERE, f"ls1{tag}.out"), "w").write("\n".join(OUT) + "\n")
