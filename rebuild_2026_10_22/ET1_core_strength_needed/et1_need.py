#!/usr/bin/env python3
"""ET1_core_strength_needed: S = rho0 r0 each SPARC galaxy asks for at fixed Upsilon, vs the floor and route E's rule. Via LS1's base exec.
python3 et1_need.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUTF = "--mutate" in sys.argv; sys.argv = [sys.argv[0]]
LSD = os.path.join(REB, "LS1_lstar_analogs"); SRC = open(os.path.join(LSD, "ls1_analogs.py")).read()
_h = HERE; __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(SRC[:SRC.index('P("LS1 SPARC')], "ls1_head", "exec"))
HERE = _h; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
MF = 0.5 if MUTF else 1.0; RS = 20261030
GRID = np.logspace(1, math.log10(3000), 121); BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); ETA1 = 10.82
PCONV = MSUNE / PC2                       # M_sun/pc^2 -> kg/m^2
def m200(q): b = BGS[TAG]; return MF * 10 ** (b["a"] + b["b"] * (q["lMb"] - 10))
def gh_of(q, s_pc):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = m200(q)
    R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); s = s_pc * PCONV; r0 = solve_r0(M * MSUNE, R200, s)
    return GE * math.pi * s * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
def mse(q, gh, iu, go=None):
    ok = q["OK"][:, iu]; lg = np.log10(np.maximum(q["GB"][:, iu] + gh, 1e-300)); o = np.log10(q["GO"]) if go is None else go
    return float(np.sum(q["W"][ok] * (o[ok] - lg[ok]) ** 2) / max(np.sum(q["W"][ok]), 1e-300))
def need(q, iu, go=None, grid=GRID):
    return float(grid[int(np.argmin([mse(q, gh_of(q, s), iu, go) for s in grid]))])
def fbul(q, name_rows):
    g = name_rows[q["name"]]; ok = q["OK"][:, I05]
    return float(np.sum(g["Vbul"][ok] ** 2) / max(np.sum(g["Vdisk"][ok] ** 2 + g["Vbul"][ok] ** 2), 1e-30))
def boot(x, rng, n=20000):
    x = np.asarray(x); return np.percentile(np.median(x[rng.integers(0, len(x), (n, len(x)))], axis=1), [2.5, 97.5]).tolist()
def sig_pc(f): return SIG[f] / PCONV
def p1(f, M): return max(sig_pc(f), ETA1 * sigma_coll(TAG, M)[0])
def econv(M): return float(np.interp(math.log10(M), [12, 13, 14], [25.94, 17.67, 16.91]))
def p2(f, M): return max(sig_pc(f), econv(M) * sigma_coll(TAG, M)[0])
SAMPLE = [q for q in GALS if q["name"] in TAB and TAB[q["name"]]["vf"] > 0 and TAB[q["name"]]["Q"] <= 2 and TAB[q["name"]]["inc"] >= 30]
P(f"ET1 S_need by V_flat; kappa = 1/2 FITTED; footings never pooled; not theory closed{' [MUTATE M200 x 0.5]' if MUTF else ''}")
P(f"sample {len(SAMPLE)}; no V_flat or cut out {len(GALS) - len(SAMPLE)}; base background {TAG}")
ROWS = {}
RMD = os.path.join(REB, "..", "real_research", "data", "sparc_data")
def rot(name):
    for d, _, fs in os.walk(RMD):
        if name + "_rotmod.dat" in fs:
            a = np.loadtxt(os.path.join(d, name + "_rotmod.dat")); return dict(Vdisk=a[:, 4], Vbul=a[:, 5])
    raise FileNotFoundError(name)
for q in SAMPLE: ROWS[q["name"]] = rot(q["name"])
RES = dict(mutate=MUTF, n=len(SAMPLE), ups={})
for U0 in (0.50, 0.40, 0.60):
    iu = int(np.argmin(abs(UPS - U0))); rng = np.random.default_rng(RS); nsat0 = NS["SAT"]["n"] if "SAT" in NS else None
    Sn = np.array([need(q, iu) for q in SAMPLE]); Vf = np.array([TAB[q["name"]]["vf"] for q in SAMPLE]); LM = np.log10([m200(q) for q in SAMPLE]); Fb = np.array([fbul(q, ROWS) for q in SAMPLE])
    cen = int(np.sum((Sn <= GRID[0]) | (Sn >= GRID[-1]))); bins = {}
    for lo, hi in BINS:
        m = (Vf >= lo) & (Vf < hi) if hi < 400 else (Vf >= lo) & (Vf <= hi)
        bins[f"{lo}-{hi}"] = dict(n=int(m.sum()), med=float(np.median(Sn[m])), ci=boot(Sn[m], rng), lgM=float(np.median(LM[m])), cens=int(np.sum((Sn[m] <= GRID[0]) | (Sn[m] >= GRID[-1]))))
    R = dict(bins=bins, censored=cen, gal={q["name"]: dict(S=float(s), vf=float(v), lgM=float(l), fb=float(b)) for q, s, v, l, b in zip(SAMPLE, Sn, Vf, LM, Fb)})
    P(f"\n=== Upsilon {U0:.2f}; censored {cen}/{len(SAMPLE)}")
    for k, b in bins.items():
        M = 10 ** b["lgM"]; P(f" {k:8s} n {b['n']:3d} lgM {b['lgM']:.2f} S_need {b['med']:7.1f} [{b['ci'][0]:7.1f},{b['ci'][1]:7.1f}] cens {b['cens']}; P1 can/alt {p1('canonical', M):.0f}/{p1('alt', M):.0f}; P2 {p2('canonical', M):.0f}/{p2('alt', M):.0f}")
    R["verdicts"] = {}
    for f in ("canonical", "alt"):
        V = {}; S0 = sig_pc(f)
        for nm, pf in (("P1", p1), ("P2", p2)):
            miss = []
            for k, b in bins.items():
                p = pf(f, 10 ** b["lgM"])
                if not b["ci"][0] <= p <= b["ci"][1]: miss.append((k, "needs MORE" if b["ci"][0] > p else "needs LESS"))
            V[nm] = "MATCHES" if not miss else "FAILS " + str(miss)
        low = ["20-60", "60-100", "100-150"]; side = [0 if bins[k]["ci"][0] <= S0 <= bins[k]["ci"][1] else (1 if bins[k]["ci"][0] > S0 else -1) for k in low]
        V["plateau"] = "PLATEAU SUPPORTED" if all(s == 0 for s in side) else ("PLATEAU REJECTED" if side.count(1) >= 2 or side.count(-1) >= 2 else "MIXED"); V["plateau_sides"] = side
        a, b = bins["150-200"], bins["200-250"]
        if a["ci"][1] >= b["ci"][0] and b["ci"][1] >= a["ci"][0]: t = "SAMPLE-LEVEL"
        else:
            st = math.log10(p2(f, 10 ** b["lgM"]) / p2(f, 10 ** a["lgM"]))
            lo_ = math.log10(b["ci"][0] / a["ci"][1]); hi_ = math.log10(b["ci"][1] / a["ci"][0])
            t = "NON-MONOTONIC" if lo_ - st > 0.3 and hi_ - st > 0.3 else "STEEPER THAN P2"
        V["tension"] = t; R["verdicts"][f] = V
        P(f" {f}: P1 {V['P1']}\n    P2 {V['P2']}\n    plateau {V['plateau']} {side}; L* tension {t}")
    hi = Vf >= 150; g0 = hi & (Fb < 0.1); g1 = hi & (Fb >= 0.1)
    if g0.sum() < 8 or g1.sum() < 8: bv = "UNDECIDED"; c0 = c1 = None
    else:
        c0, c1 = boot(Sn[g0], rng), boot(Sn[g1], rng); bv = "BARYON-MODEL SIGNAL" if c0[1] < c1[0] or c1[1] < c0[0] else "NO BULGE SIGNAL"
    P(f" bulge: bulgeless n {g0.sum()} med {np.median(Sn[g0]):.1f} {c0}; bulged n {g1.sum()} med {np.median(Sn[g1]):.1f} {c1} -> {bv}")
    from scipy.stats import rankdata
    x, y = rankdata(LM[hi]), rankdata(Sn[hi]); rho = float(np.corrcoef(x, y)[0, 1]); pr = np.random.default_rng(RS)
    nul = np.array([np.corrcoef(pr.permutation(x), y)[0, 1] for _ in range(20000)]); p = float(np.mean(np.abs(nul) >= abs(rho)))
    tr = ("OPPOSITE TO NATIVE TREND" if rho > 0 else "NATIVE SIGN") if p < 0.01 else "NO TREND"
    P(f" mass trend V_flat>=150: n {hi.sum()} Spearman {rho:+.3f} p {p:.4f} -> {tr}")
    R["bulge"] = dict(verdict=bv, c0=c0, c1=c1, n0=int(g0.sum()), n1=int(g1.sum())); R["trend"] = dict(rho=rho, p=p, verdict=tr); RES["ups"][f"{U0:.2f}"] = R
code = 0
if not MUTF:
    k1 = 0.0
    for q in sel(200, 250)[:3]:
        s = max(SIG["canonical"], eta_of(4.0) * sigma_coll(TAG, m200(q))[0] * MSUNE / PC2)
        k1 = max(k1, float(np.max(np.abs(gh_of(q, s / PCONV) / halo(q, "canonical", TAG, 4.0) - 1))))
    P(f"\nK1 own S vs LS1 halo: max rel {k1:.1e}: {'PASS' if k1 < 1e-10 else 'FAIL'}"); code |= k1 >= 1e-10
    q = sel(100, 150)[0]; iu = I05; k2 = []
    for ps in (50.0, 200.0, 800.0):
        g = np.log10(np.maximum(q["GB"][:, iu] + gh_of(q, ps), 1e-300)); k2.append(abs(math.log(need(q, iu, g) / ps)) <= math.log(GRID[1] / GRID[0]))
    P(f"K2 planted S 50/200/800 recovered within a step: {k2}: {'PASS' if all(k2) else 'FAIL'}"); code |= not all(k2)
    gh = gh_of(q, 150.0); r = np.where(q["OK"][:, iu], np.log10(q["GO"]) - np.log10(np.maximum(q["GB"][:, iu] + gh, 1e-300)), 0)
    d = float(np.sum(np.where(q["OK"][:, iu], q["W"], 0) * r * r) / np.sum(np.where(q["OK"][:, iu], q["W"], 0))); k3 = abs(d - mse(q, gh, iu))
    P(f"K3 mse direct |d| {k3:.1e}: {'PASS' if k3 < 1e-10 else 'FAIL'}"); code |= k3 >= 1e-10
    RES["K"] = dict(K1=k1, K2=k2, K3=k3)
else:
    B0 = json.load(open(os.path.join(HERE, "et1_results.json")))["ups"]["0.50"]["bins"]["200-250"]["med"]; B1 = RES["ups"]["0.50"]["bins"]["200-250"]["med"]
    P(f"\nMUTATE 200-250 median S_need {B0:.1f} -> {B1:.1f}: {'bites' if B1 > B0 else 'NO BITE'}"); code = 0 if B1 > B0 else 1
tag = "_MUTATE" if MUTF else ""
json.dump(RES, open(os.path.join(HERE, f"et1_results{tag}.json"), "w"), indent=1); open(os.path.join(HERE, f"et1{tag}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(int(code))
