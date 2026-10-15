"""CFG804 -- catchment supply N = 1/f_ret(M_ta) from the record's census, scored on KiDS-1000 lensing.
Criteria: FROZEN_CRITERIA.md (22cdbecf9).  Run: python3 cfg804.py [alt]  (CFG804_MUTATE=1: f_ret = 1).
kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import quad
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
MUT = os.environ.get("CFG804_MUTATE") == "1"
FOOT = "alt" if "alt" in sys.argv[1:] else "canonical"
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}[FOOT]
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

Gpc = 4.30091e-3; a0 = A0 * 3.0857e16 / 1e6; SUP = 5.364; FB = 1 / (1 + SUP)
def fret_of(lM):                      # CFG416 / CFG556 verbatim
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def N_of(logMb):
    if MUT: return 1.0, logMb - math.log10(FB)
    f = 0.10
    for _ in range(200):
        lMta = logMb - math.log10(f * FB); fn = fret_of(lMta)
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    return 1 / f, lMta
edge_of = lambda N: math.sqrt(((2 * SUP * N + 1) ** 2 - 1) / 4)
rho = lambda s: 1.0 / (2 * math.pi * s * math.sqrt(1 + 4 * s * s))
X = np.logspace(-3, 3, 600)
def profile(smax):
    Sig = np.empty_like(X)
    for i, x in enumerate(X):
        if smax is not None and x >= smax:
            Sig[i] = 0.0; continue
        tm = math.sqrt(smax ** 2 - x * x) if smax is not None else np.inf
        Sig[i] = 2 * quad(lambda t: rho(math.hypot(x, t)), 0, tm, limit=300)[0]
    integ = 2 * math.pi * X ** 2 * Sig
    Mc = np.concatenate([[math.pi * X[0] ** 2 * Sig[0]], math.pi * X[0] ** 2 * Sig[0] + np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(np.log(X)))])
    return np.maximum(Mc / (math.pi * X ** 2) - Sig + 1.0 / (math.pi * X ** 2), 1e-30)

P(f"CFG804  derived catchment supply vs KiDS-1000, footing {FOOT}" + ("  [MUTATE f_ret=1]" if MUT else ""))
Nk, lk = N_of(10.5)
k1 = MUT or (abs(Nk - 10) < 1e-6 and abs(lk - 12.30) < 0.01)
P(f"  K1 log M_b 10.5 -> N {Nk:.3f}, log M_ta {lk:.3f}: {'PASS' if k1 else 'FAIL'}")
fB = profile(None)
NGRID = np.round(np.concatenate([[1.0], np.arange(2.0, 10.01, 0.25)]), 2)
FD = {}
def f_for(N):
    Nn = float(NGRID[np.argmin(abs(NGRID - N))])
    if Nn not in FD: FD[Nn] = profile(edge_of(Nn))
    return FD[Nn]

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
def chi2(fsel, L, idx):
    yv = np.concatenate([Y[b] for b in range(4)])
    mv = np.concatenate([model(fsel(L[b]), L[b], R[b]) for b in range(4)])
    sel = np.concatenate([np.array(idx) + 15 * b for b in range(4)]); r = (yv - mv)[sel]
    if not np.all(np.isfinite(r)): return float("inf")
    with np.errstate(all="ignore"): x2 = float(r @ np.linalg.solve(C[np.ix_(sel, sel)], r))
    return x2 if np.isfinite(x2) else float("inf")
def fit(fsel, idx):
    L = list(ZK)
    for _ in range(3):
        for b in range(4):
            L[b] = float(min(GRID, key=lambda g: chi2(fsel, L[:b] + [g] + L[b + 1:], idx)))
    return L, chi2(fsel, L, idx)
fsB = lambda lm: fB
fsD = lambda lm: f_for(N_of(lm)[0])
prim = [i for i in range(15) if R[0, i] <= 0.31]; full = list(range(15))
RES = dict(lane="CFG804", footing=FOOT, mutate=MUT, K1=bool(k1))
for lab, idx in (("primary", prim), ("all", full)):
    LB, cB = fit(fsB, idx); LD, cD = fit(fsD, idx); d = cD - cB
    RES[lab] = dict(chi2_B=cB, chi2_D=cD, dchi2=d, logMb=LD, p_D=stats.chi2.sf(cD, 4 * len(idx) - 4))
    P(f"\n  [{lab}] B chi2 {cB:.1f}; D_derived chi2 {cD:.1f}; dchi2 {d:+.1f} -> {'DERIVED SUPPLY SUFFICES' if d <= 4 else 'FALLS SHORT'}")
    for b in range(4):
        N, lMta = N_of(LD[b]); rM = math.sqrt(Gpc * 10 ** LD[b] / a0) / 1e3
        P(f"    bin {b + 1}: log M_b {LD[b]:.2f} -> log M_ta {lMta:.2f}, f_ret {1 / N:.3f}, N {N:.2f}, edge {edge_of(N):.1f} r_M = {edge_of(N) * rM:.0f} kpc")
k2 = (abs(RES["primary"]["chi2_B"] - 83.9) < 0.15) if FOOT == "canonical" else True
P(f"\n  K2 B = 83.9: {'PASS' if k2 else 'FAIL'}")
cls = "DERIVED SUPPLY SUFFICES" if RES["primary"]["dchi2"] <= 4 else "FALLS SHORT"
P(f"  CLASS (primary): {cls}" + (f"   MUTATE: {'bites' if cls == 'FALLS SHORT' else 'DID NOT BITE'}" if MUT else ""))
RES.update(K2=bool(k2), cls=cls)
sfx = ("_MUTATE" if MUT else "") + ("_alt" if FOOT == "alt" else "")
json.dump(RES, open(os.path.join(HERE, f"cfg804_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg804{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
