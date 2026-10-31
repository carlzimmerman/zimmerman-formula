#!/usr/bin/env python3
"""ET2_free_core_low_mass: free S and r0 per SPARC galaxy, no M200; does ET1's low-mass rise survive? Via LS1's base exec.
python3 et2_free.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUTF = "--mutate" in sys.argv; sys.argv = [sys.argv[0]]
LSD = os.path.join(REB, "LS1_lstar_analogs"); SRC = open(os.path.join(LSD, "ls1_analogs.py")).read()
_h = HERE; __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(SRC[:SRC.index('P("LS1 SPARC')], "ls1_head", "exec"))
HERE = _h; OUT = []
from scipy.stats import rankdata
def P(s): print(s, flush=True); OUT.append(s)
RS = 20261030; PCONV = MSUNE / PC2; BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); LOW = ("20-60", "60-100", "100-150"); FL = dict(canonical=106.85, alt=129.13)
SG = np.logspace(1, math.log10(3000), 121); RG = np.logspace(-1, 2, 41) * KPC
def gh(q, s_pc, r0): return GE * math.pi * s_pc * PCONV * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
def m200(q): b = BGS[TAG]; return 10 ** (b["a"] + b["b"] * (q["lMb"] - 10))
def r0_et1(q, s_pc):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = m200(q); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); return solve_r0(M * MSUNE, R200, s_pc * PCONV)
def surface(q, iu, go=None):
    ok = q["OK"][:, iu]; o = (np.log10(q["GO"]) if go is None else go)[ok]; W = q["W"][ok]; gb = q["GB"][ok, iu]; T = np.zeros((len(SG), len(RG)))
    for j, r0 in enumerate(RG):
        h = gh(q, 1.0, r0)[ok]
        T[:, j] = np.sum(W * (o[None, :] - np.log10(np.maximum(gb[None, :] + SG[:, None] * h[None, :], 1e-300))) ** 2, 1)
    return T / max(np.sum(W), 1e-300), int(ok.sum())
def fit(q, iu, go=None):
    T, n = surface(q, iu, go); i, j = np.unravel_index(np.argmin(T), T.shape); s = np.where(T <= T[i, j] + 1 / max(n, 1))[0]
    return float(SG[i]), float(RG[j]), bool(np.log10(SG[s.max()] / SG[s.min()]) < 0.5), bool(i in (0, len(SG) - 1) or j in (0, len(RG) - 1))
def boot(x, rng): x = np.asarray(x); return np.percentile(np.median(x[rng.integers(0, len(x), (20000, len(x)))], axis=1), [2.5, 97.5]).tolist()
SAMPLE = [q for q in GALS if q["name"] in TAB and TAB[q["name"]]["vf"] > 0 and TAB[q["name"]]["Q"] <= 2 and TAB[q["name"]]["inc"] >= 30]
Vf = np.array([TAB[q["name"]]["vf"] for q in SAMPLE])
def spear(mask, S):
    x, y = rankdata(np.log10(Vf[mask])), rankdata(np.log10(S[mask])); rho = float(np.corrcoef(x, y)[0, 1]); pr = np.random.default_rng(RS)
    p = float(np.mean(np.abs([np.corrcoef(pr.permutation(x), y)[0, 1] for _ in range(20000)]) >= abs(rho))); return rho, p, ("RISE SURVIVES" if rho > 0 else "FALLS") if p < 0.01 else "RISE GONE"
def verdicts(S, mask, ET, rng):
    bins = {}
    for lo, hi in BINS:
        m = (Vf >= lo) & (Vf < hi if hi < 400 else Vf <= hi); m &= mask
        bins[f"{lo}-{hi}"] = dict(n=int(m.sum()), med=float(np.median(S[m])), ci=boot(S[m], rng)) if m.sum() >= 2 else dict(n=int(m.sum()), med=None, ci=None)
    lm = mask & (Vf < 150); rho, p, rv = spear(lm, S); fl = {}
    for f, v in FL.items():
        side = [0 if bins[k]["ci"][0] <= v <= bins[k]["ci"][1] else (1 if bins[k]["ci"][0] > v else -1) for k in LOW]
        fl[f] = dict(side=side, verdict="FLOOR HOLDS" if all(x == 0 for x in side) else ("FLOOR REJECTED" if side.count(1) >= 2 or side.count(-1) >= 2 else "MIXED"))
    dis = [k for k in LOW if ET and not (bins[k]["ci"][0] <= ET[k]["ci"][1] and ET[k]["ci"][0] <= bins[k]["ci"][1])]
    return dict(bins=bins, rho=rho, p=p, rise=rv, floor=fl, m200="M200-INDEPENDENT" if not dis else "M200-DEPENDENT " + str(dis))
P(f"ET2 free S, r0; no M200; kappa = 1/2 FITTED; footings never pooled; not theory closed{' [MUTATE flat S 100]' if MUTF else ''}\nsample {len(SAMPLE)}")
RES = dict(mutate=MUTF, ups={}); code = 0
ET = json.load(open(os.path.join(REB, "ET1_core_strength_needed", "et1_results.json")))["ups"]
for U0 in ((0.50,) if MUTF else (0.50, 0.40, 0.60)):
    iu = int(np.argmin(abs(UPS - U0))); rng = np.random.default_rng(RS); F = []
    for q in SAMPLE:
        go = np.log10(np.maximum(q["GB"][:, iu] + gh(q, 100.0, r0_et1(q, 100.0)), 1e-300)) if MUTF else None
        F.append(fit(q, iu, go))
    S = np.array([x[0] for x in F]); R0 = np.array([x[1] for x in F]) / KPC; C = np.array([x[2] for x in F]); CE = np.array([x[3] for x in F])
    A = verdicts(S, np.ones(len(S), bool), ET[f"{U0:.2f}"]["bins"], rng); G = verdicts(S, C, None, rng) if all((C & (Vf >= l) & (Vf < h)).sum() >= 2 for l, h in BINS[:3]) else None
    P(f"\n=== Upsilon {U0:.2f}; censored {CE.sum()}/{len(S)}; constrained {C.sum()}/{len(S)}, below 150 km/s {(C & (Vf < 150)).sum()}/{(Vf < 150).sum()}")
    for k, b in A["bins"].items():
        g = G["bins"][k] if G else None; P(f" {k:8s} n {b['n']:3d} S {b['med']:7.1f} [{b['ci'][0]:7.1f},{b['ci'][1]:7.1f}]; ET1 {ET[f'{U0:.2f}']['bins'][k]['med']:7.1f}; constrained n {g['n'] if g else 0} {g['med'] if g else None}")
    gd = lambda a, b: a if (G is None or a == b) else f"GUARD-DEPENDENT (all: {a}; constrained: {b})"
    P(f" rise rho {A['rho']:+.3f} p {A['p']:.4f}: {gd(A['rise'], G['rise'] if G else A['rise'])}" + (f"; constrained rho {G['rho']:+.3f} p {G['p']:.4f}" if G else "; constrained too few"))
    for f in FL: P(f" floor {f}: {gd(A['floor'][f]['verdict'], G['floor'][f]['verdict'] if G else A['floor'][f]['verdict'])} {A['floor'][f]['side']}")
    P(f" {A['m200']}")
    RES["ups"][f"{U0:.2f}"] = dict(all=A, constrained=G, gal={q["name"]: dict(S=float(s), r0_kpc=float(r), constrained=bool(c), censored=bool(e), vf=float(v)) for q, s, r, c, e, v in zip(SAMPLE, S, R0, C, CE, Vf)})
if MUTF:
    v = RES["ups"]["0.50"]["all"]["rise"]; P(f"\nMUTATE flat truth reads: {v}"); code = int(v == "RISE SURVIVES")
else:
    k1 = 0.0
    for q in sel(100, 150)[:3]:
        s = 150.0; r0 = r0_et1(q, s); k1 = max(k1, float(np.max(np.abs(gh(q, s, r0) / (GE * math.pi * s * PCONV * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2) - 1))))
    P(f"\nK1 halo form vs ET1 gh_of: max rel {k1:.1e}: {'PASS' if k1 < 1e-10 else 'FAIL'}"); code |= k1 >= 1e-10
    q = sel(100, 150)[0]; k2 = []
    for ps, pr in ((50.0, 1.0), (200.0, 3.0), (800.0, 10.0)):
        a, b, _, _ = fit(q, I05, np.log10(np.maximum(q["GB"][:, I05] + gh(q, ps, pr * KPC), 1e-300)))
        k2.append(abs(math.log(a / ps)) <= math.log(SG[1] / SG[0]) and abs(math.log(b / KPC / pr)) <= math.log(RG[1] / RG[0])); P(f" K2 planted ({ps}, {pr}) -> ({a:.1f}, {b / KPC:.2f})")
    P(f"K2: {k2}: {'PASS' if all(k2) else 'FAIL'}"); code |= not all(k2); RES["K"] = dict(K1=k1, K2=k2)
tag = "_MUTATE" if MUTF else ""
json.dump(RES, open(os.path.join(HERE, f"et2_results{tag}.json"), "w"), indent=1); open(os.path.join(HERE, f"et2{tag}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(int(code))
