"""CFG803 -- CFG748 infall-filled law and catchment edge D(N) vs KiDS-1000 lensing (CFG801 setup).
Criteria: FROZEN_CRITERIA.md (5c3468ec0).  Run: python3 cfg803.py [alt]  (CFG803_MUTATE=1: fill 0 beyond 5.84 r_M).
kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import quad
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
MUT = os.environ.get("CFG803_MUTATE") == "1"
FOOT = "alt" if "alt" in sys.argv[1:] else "canonical"
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}[FOOT]
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

Gpc = 4.30091e-3; a0 = A0 * 3.0857e16 / 1e6; SUP = 5.364
edge_of = lambda N: math.sqrt(((2 * SUP * N + 1) ** 2 - 1) / 4)
rho = lambda s: 1.0 / (2 * math.pi * s * math.sqrt(1 + 4 * s * s))
FT = np.array([[2, 1.002], [5, 0.994], [10, 0.999], [20, 0.991], [50, 0.948]])
def fill(s):
    if MUT:
        return 1.0 if s <= edge_of(1) else 0.0
    if s <= 2: return 1.0
    if s >= 50: return 0.948
    return float(np.interp(math.log(s), np.log(FT[:, 0]), FT[:, 1]))

X = np.logspace(-3, 3, 600)
def profile(dens, smax):
    Sig = np.empty_like(X)
    for i, x in enumerate(X):
        if smax is not None and x >= smax:
            Sig[i] = 0.0; continue
        tm = math.sqrt(smax ** 2 - x * x) if smax is not None else np.inf
        Sig[i] = 2 * quad(lambda t: dens(math.hypot(x, t)), 0, tm, limit=300)[0]
    integ = 2 * math.pi * X ** 2 * Sig
    Mc = np.concatenate([[math.pi * X[0] ** 2 * Sig[0]], math.pi * X[0] ** 2 * Sig[0] + np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(np.log(X)))])
    return np.maximum(Mc / (math.pi * X ** 2) - Sig + 1.0 / (math.pi * X ** 2), 1e-30)

P(f"CFG803  infall-filled law + catchment edge vs KiDS-1000, footing {FOOT}" + ("  [MUTATE]" if MUT else ""))
fB = profile(rho, None)
fC = profile(lambda s: rho(s) * fill(s), (edge_of(1) if MUT else None))
NG = [1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
fD = {N: profile(rho, edge_of(N)) for N in NG}

R, Y = [], []
for b in range(1, 5):
    d = np.loadtxt(os.path.join(D, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")); R.append(d[:, 0]); Y.append(d[:, 1] / d[:, 4])
R, Y = np.array(R), np.array(Y)
c = np.loadtxt(os.path.join(D, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt")); mins = sorted(set(c[:, 0]))
C = np.zeros((60, 60))
for row in c:
    m, n = mins.index(row[0]), mins.index(row[1]); i, j = int(np.argmin(abs(R[0] - row[2]))), int(np.argmin(abs(R[0] - row[3])))
    C[m * 15 + i, n * 15 + j] = row[4] / row[6]
def model(f, lm, Rb):
    M = 10 ** lm; rM = math.sqrt(Gpc * M / a0); x = Rb * 1e6 / rM
    return M / rM ** 2 * np.exp(np.interp(np.log(x), np.log(X), np.log(f)))
GRID = np.arange(9.0, 12.0001, 0.01); ZK = [10.14, 10.46, 10.70, 10.89]
def chi2(f, L, idx):
    yv = np.concatenate([Y[b] for b in range(4)]); mv = np.concatenate([model(f, L[b], R[b]) for b in range(4)])
    sel = np.concatenate([np.array(idx) + 15 * b for b in range(4)]); r = (yv - mv)[sel]
    if not np.all(np.isfinite(r)): return float("inf")
    with np.errstate(all="ignore"): x2 = float(r @ np.linalg.solve(C[np.ix_(sel, sel)], r))
    return x2 if np.isfinite(x2) else float("inf")
def fit(f, idx):
    L = list(ZK)
    for _ in range(3):
        for b in range(4):
            L[b] = float(min(GRID, key=lambda g: chi2(f, L[:b] + [g] + L[b + 1:], idx)))
    return L, chi2(f, L, idx)
prim = [i for i in range(15) if R[0, i] <= 0.31]; full = list(range(15))
RES = dict(lane="CFG803", footing=FOOT, mutate=MUT)
for lab, idx in (("primary", prim), ("all", full)):
    LB, cB = fit(fB, idx); LC, cC = fit(fC, idx)
    dof = 4 * len(idx) - 4
    Dd = {}
    for N in NG:
        Dd[N] = fit(fD[N], idx)[1] - cB
    nmin = next((N for N in NG if Dd[N] <= 4), None)
    RES[lab] = dict(chi2_B=cB, chi2_C=cC, dC=cC - cB, p_B=stats.chi2.sf(cB, dof), p_C=stats.chi2.sf(cC, dof), D=Dd, N_min=nmin, logMb_C=LC)
    P(f"\n  [{lab}] n {4 * len(idx)}: B (no edge) chi2 {cB:.1f}; C (infall-filled) chi2 {cC:.1f}  dchi2(C-B) {cC - cB:+.1f}  -> {'C RESCUES' if cC - cB <= 4 else 'C FAILS'}")
    P("    D(N) dchi2 vs B: " + ", ".join(f"N={N}: {Dd[N]:+.1f}" for N in NG))
    P(f"    N_min (dchi2 <= 4): {nmin}  -> edge radius {edge_of(nmin):.1f} r_M" if nmin else "    N_min: > 64")
pr = RES["primary"]
k1 = abs(pr["chi2_B"] - 83.9) < 0.15 if FOOT == "canonical" else True
k2 = abs(pr["D"][1] + pr["chi2_B"] - 280.9) < 1.0 if FOOT == "canonical" else True
P(f"\n  K1 B reproduces CFG801 83.9: {'PASS' if k1 else 'FAIL'};  K2 D(1) reproduces CFG801 edge 280.9: {'PASS' if k2 else 'FAIL'}")
P(f"  C's own supply requirement: law mass within 200 r_M = {(math.sqrt(1 + 4 * 200 ** 2) - 1) / 2:.0f} M_b -> N = {(math.sqrt(1 + 4 * 200 ** 2) - 1) / 2 / SUP:.0f}")
cls = "C RESCUES" if pr["dC"] <= 4 else "C FAILS"
P(f"  CLASS (primary): {cls}" + (f"   MUTATE: {'bites' if cls == 'C FAILS' else 'DID NOT BITE'}" if MUT else ""))
RES.update(K1=bool(k1), K2=bool(k2), cls=cls)
sfx = ("_MUTATE" if MUT else "") + ("_alt" if FOOT == "alt" else "")
json.dump(RES, open(os.path.join(HERE, f"cfg803_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg803{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
