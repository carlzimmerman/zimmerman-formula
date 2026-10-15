"""CFG801 -- ARGON02 kill test (b): settled-halo edge at 5.84 r_M vs no-edge continuation on Brouwer+21 KiDS-1000
isolated lensing rotation curves.  Criteria: FROZEN_CRITERIA.md (0ff46e530).  Seconds, 1 process.
Run: python3 cfg801.py [alt]   (CFG801_MUTATE=1: data := edge model + covariance noise).  kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import quad
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
MUT = os.environ.get("CFG801_MUTATE") == "1"
FOOT = "alt" if "alt" in sys.argv[1:] else "canonical"
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}[FOOT]
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

Gpc = 4.30091e-3                       # pc (km/s)^2 / Msun
a0 = A0 * 3.0857e16 / 1e6              # (km/s)^2 / pc
SUP = 5.364
se = math.sqrt(((2 * SUP + 1) ** 2 - 1) / 4)
rho = lambda s: 1.0 / (2 * math.pi * s * math.sqrt(1 + 4 * s * s))     # units M_b / r_M^3

X = np.logspace(-3, 3, 700)
def profile(edge):
    Sig = np.empty_like(X)
    for i, x in enumerate(X):
        if edge:
            tm = math.sqrt(se * se - x * x) if x < se else 0.0
            Sig[i] = 2 * quad(lambda t: rho(math.hypot(x, t)), 0, tm, limit=200)[0] if tm > 0 else 0.0
        else:
            Sig[i] = 2 * quad(lambda t: rho(math.hypot(x, t)), 0, np.inf, limit=400)[0]
    integ = 2 * math.pi * X ** 2 * Sig                                  # d M_cyl / d ln x
    Mcyl = np.concatenate([[math.pi * X[0] ** 2 * Sig[0]], math.pi * X[0] ** 2 * Sig[0] + np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(np.log(X)))])
    return Mcyl / (math.pi * X ** 2) - Sig + 1.0 / (math.pi * X ** 2), Mcyl, Sig   # incl. baryon point mass
fE, McE, _ = profile(True)
fN, McN, SgN = profile(False)
P(f"CFG801  settled edge vs no edge on KiDS-1000 (B21 Fig.3), footing {FOOT}" + ("  [MUTATE]" if MUT else ""))
k1 = abs(se - 5.843) < 1e-3
cold20 = np.interp(math.log(20), np.log(X), fN - 1.0 / (math.pi * X ** 2))
k2 = abs(cold20 / (1 / (4 * 20)) / 0.969 - 1) < 0.01
P(f"  K1 r_e/r_M = {se:.4f}: {'PASS' if k1 else 'FAIL'};  K2 no-edge cold ESD at 20 r_M = {cold20 / (1 / 80):.4f} x deep (ARGON02 0.969): {'PASS' if k2 else 'FAIL'}")
P(f"  edge model cold projected mass M_cyl(inf)/M_b = {McE[-1]:.3f} (expect 5.364)")

# data
R, Y, B = [], [], []
for b in range(1, 5):
    d = np.loadtxt(os.path.join(D, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"))
    R.append(d[:, 0]); Y.append(d[:, 1] / d[:, 4]); B.append(d[:, 4])
R, Y = np.array(R), np.array(Y)
c = np.loadtxt(os.path.join(D, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"))
mins = sorted(set(c[:, 0])); radii = list(R[0])
C = np.zeros((60, 60))
for row in c:
    m, n = mins.index(row[0]), mins.index(row[1])
    i, j = int(np.argmin(abs(R[0] - row[2]))), int(np.argmin(abs(R[0] - row[3])))
    C[m * 15 + i, n * 15 + j] = row[4] / row[6]
v = math.sqrt(4 * 4.52e-30 * Y[0, 0] * R[0, 0] * 1e6) * 3.086e13
k3 = v > 0
P(f"  K3 B21 Eq.23 v_circ(bin1, R0) = {v:.1f} km/s: {'PASS' if k3 else 'FAIL'}")

def model(f, logM, Rb):
    M = 10 ** logM; rM = math.sqrt(Gpc * M / a0)
    x = Rb * 1e6 / rM
    return M / rM ** 2 * np.exp(np.interp(np.log(x), np.log(X), np.log(f)))
GRID = np.arange(9.0, 12.0001, 0.01)
ZK = [10.14, 10.46, 10.70, 10.89]

def chi2(f, logMs, idx, y):
    yv = np.concatenate([y[b] for b in range(4)])
    mv = np.concatenate([model(f, logMs[b], R[b]) for b in range(4)])
    sel = np.concatenate([np.array(idx) + 15 * b for b in range(4)])
    r = (yv - mv)[sel]
    if not np.all(np.isfinite(r)):
        return float('inf'), len(sel)
    with np.errstate(all='ignore'):
        x2 = float(r @ np.linalg.solve(C[np.ix_(sel, sel)], r))
    return (x2 if np.isfinite(x2) else float('inf')), len(sel)

def profile_fit(f, idx, y):
    L = list(ZK)
    for _ in range(3):
        for b in range(4):
            best = min(GRID, key=lambda g: chi2(f, L[:b] + [g] + L[b + 1:], idx, y)[0]); L[b] = float(best)
    return L, chi2(f, L, idx, y)

prim = [i for i in range(15) if R[0, i] <= 0.31]
full = list(range(15))
y = Y.copy()
if MUT:
    Le, _ = profile_fit(fE, prim, Y)
    mv = np.concatenate([model(fE, Le[b], R[b]) for b in range(4)])
    y = (mv + np.random.default_rng(801).multivariate_normal(np.zeros(60), C)).reshape(4, 15)
RES = dict(lane="CFG801", footing=FOOT, mutate=MUT, K1=k1, K2=bool(k2), K3=k3, r_e_over_rM=se)
for lab, idx in (("primary R<=0.31 Mpc", prim), ("all radii", full)):
    LE, (cE, n) = profile_fit(fE, idx, y); LN, (cN, _) = profile_fit(fN, idx, y)
    zE, _ = chi2(fE, ZK, idx, y); zN, _ = chi2(fN, ZK, idx, y)
    dof = n - 4
    d = cE - cN
    cls = "EDGE EXCLUDED" if d >= 9 else ("EDGE FAVOURED" if d <= -9 else "UNDECIDED")
    RES[lab] = dict(n=n, chi2_edge=cE, chi2_noedge=cN, dchi2=d, p_edge=stats.chi2.sf(cE, dof), p_noedge=stats.chi2.sf(cN, dof),
                    logMb_edge=LE, logMb_noedge=LN, Z_chi2_edge=zE, Z_chi2_noedge=zN, Z_dchi2=zE - zN, cls=cls)
    P(f"\n  [{lab}] n = {n}")
    P(f"    (P) profiled: edge chi2 {cE:.1f} (p {stats.chi2.sf(cE, dof):.3f}, logMb {['%.2f' % v for v in LE]})")
    P(f"                  no-edge chi2 {cN:.1f} (p {stats.chi2.sf(cN, dof):.3f}, logMb {['%.2f' % v for v in LN]})")
    P(f"        dchi2 (edge - no edge) = {d:+.1f} -> {cls}")
    P(f"    (Z) zero-knob logM* {ZK}: edge {zE:.1f}, no-edge {zN:.1f}, dchi2 {zE - zN:+.1f}")
    for b in range(4):
        rM = math.sqrt(Gpc * 10 ** LE[b] / a0) / 1e3
        P(f"      bin {b + 1}: r_M {rM:.1f} kpc, edge r_e {se * rM:.0f} kpc")
pc = RES["primary R<=0.31 Mpc"]["cls"]
P(f"\n  CLASS (primary, profiled): {pc}" + ("" if not MUT else f"   MUTATE: {'bites' if pc == 'EDGE FAVOURED' else 'DID NOT BITE'}"))
sfx = ("_MUTATE" if MUT else "") + ("_alt" if FOOT == "alt" else "")
json.dump(RES, open(os.path.join(HERE, f"cfg801_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg801{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
