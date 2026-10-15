"""CFG805 -- framework-native two-halo term (T1x P_grav at z=0.2562) on KiDS-1000 lensing.  Criteria: FROZEN_CRITERIA.md (11b9e3f03).
Run: python3 cfg805.py   (CFG805_MUTATE=1: no exclusion).  Reuses CFG804's profiles/fixed point by import.
kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys, importlib.util
import numpy as np
from scipy.integrate import quad
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG805_MUTATE") == "1"
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# --- CFG804 machinery (read-only import; its module-level run is guarded by being a script, so re-implement minimal parts)
src = os.path.join(HERE, "..", "CFG804_catchment_supply_derived", "cfg804.py")
txt = open(src).read().split('P(f"CFG804')[0]                       # definitions only
G = {"__file__": src, "__name__": "cfg804_defs"}; sys.argv = [src]
exec(compile(txt, src, "exec"), G)
profile, N_of, edge_of, Gpc, a0 = G["profile"], G["N_of"], G["edge_of"], G["Gpc"], G["a0"]
X = G["X"]

# --- T1x P_grav at z = 0.2562
J = json.load(open("/Users/carlzimmerman/new_physics/_external_data/cfg650_work/T1x/cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json"))
S = J["snap"]["x0.2562"]; z = S["z"]; k = np.array(S["k"]); Pk = np.array(S["P_grav"])
ok = (k > 0) & np.isfinite(Pk) & (Pk > 0); k, Pk = k[ok], Pk[ok]
hh = 0.6736; Om = (0.02237 + 0.1200) / hh ** 2
W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
s8 = math.sqrt(np.trapz(k ** 2 * Pk * W(8 * k) ** 2, k) / (2 * math.pi ** 2))
k2 = abs(s8 / S["sigma8_grav"] - 1) < 0.02
P(f"CFG805  two-halo term from T1x P_grav(z={z:.4f})" + ("  [MUTATE no exclusion]" if MUT else ""))
P(f"  K2 sigma8_grav recomputed {s8:.4f} vs snapshot {S['sigma8_grav']:.4f}: {'PASS' if k2 else 'FAIL'}  (k {k.min():.3f}-{k.max():.1f} h/Mpc)")
rs = 0.05
rg = np.logspace(-2.5, 2, 900)                                        # comoving Mpc/h
xi = np.array([np.trapz(k ** 2 * Pk * np.sinc(k * r / math.pi) * np.exp(-(k * rs) ** 2), k) / (2 * math.pi ** 2) for r in rg])
xi_of = lambda r: np.interp(np.log(r), np.log(rg), xi, left=xi[0], right=0.0)
rho_c = Om * 2.775e11                                                 # h^2 Msun / Mpc^3 comoving

def esd2h(R_phys_Mpc, rex_phys_Mpc):
    """b=1 two-halo ESD [Msun/pc^2 physical] at physical radii (h70=1 units), excluding r < rex."""
    a = 1 / (1 + z)
    Rc = R_phys_Mpc / a * hh; rexc = rex_phys_Mpc / a * hh
    Rg = np.logspace(-3, math.log10(max(Rc.max(), 1e-3) * 1.01), 220)
    def Sig(Rv):
        f = lambda t: (xi_of(math.hypot(Rv, t)) if math.hypot(Rv, t) > rexc else 0.0)
        return 2 * rho_c * quad(f, 0, 80.0, limit=400)[0]
    Sg = np.array([Sig(r) for r in Rg])
    Mcyl = np.concatenate([[0.0], np.cumsum(0.5 * (2 * math.pi * Rg[1:] * Sg[1:] + 2 * math.pi * Rg[:-1] * Sg[:-1]) * np.diff(Rg))])
    Sbar = np.where(Rg > 0, Mcyl / (math.pi * Rg ** 2), 0)
    dS = np.interp(Rc, Rg, Sbar - Sg)                                  # h Msun / Mpc^2 comoving
    return dS * hh / 1e12 / a ** 2                                     # Msun/pc^2 physical

# --- data
D = os.path.join(HERE, "..", "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
R, Y = [], []
for b in range(1, 5):
    d = np.loadtxt(os.path.join(D, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")); R.append(d[:, 0]); Y.append(d[:, 1] / d[:, 4])
R, Y = np.array(R), np.array(Y)
c = np.loadtxt(os.path.join(D, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt")); mins = sorted(set(c[:, 0]))
C = np.zeros((60, 60))
for row in c:
    m, n = mins.index(row[0]), mins.index(row[1]); i, j = int(np.argmin(abs(R[0] - row[2]))), int(np.argmin(abs(R[0] - row[3])))
    C[m * 15 + i, n * 15 + j] = row[4] / row[6]
REX = [0.343, 0.442, 0.433, 0.429]                                    # CFG804 all-radii derived edges (Mpc)
T2 = [esd2h(R[b], 0.0 if MUT else REX[b]) for b in range(4)]
P("  two-halo template (b=1) at R = 0.5 / 1 / 2.6 Mpc, bin 2: " + " / ".join(f"{np.interp(x, R[1], T2[1]):.2f}" for x in (0.5, 1.0, 2.6)) + " Msun/pc^2")

fB = profile(None)
NGRID = np.round(np.concatenate([[1.0], np.arange(2.0, 10.01, 0.25)]), 2); FD = {}
def f_for(N):
    Nn = float(NGRID[np.argmin(abs(NGRID - N))])
    if Nn not in FD: FD[Nn] = profile(edge_of(Nn))
    return FD[Nn]
def model1(f, lm, Rb):
    M = 10 ** lm; rM = math.sqrt(Gpc * M / a0); x = Rb * 1e6 / rM
    return M / rM ** 2 * np.exp(np.interp(np.log(x), np.log(X), np.log(f)))
GRID = np.arange(9.5, 12.0001, 0.01); ZK = [10.14, 10.46, 10.70, 10.89]
def solve(fsel, idx, use2h):
    sel = np.concatenate([np.array(idx) + 15 * b for b in range(4)]); Ci = np.linalg.inv(C[np.ix_(sel, sel)])
    yv = np.concatenate([Y[b] for b in range(4)])[sel]
    L = list(ZK); Bb = [0.0] * 4
    def vec(L, Bb):
        return np.concatenate([model1(fsel(L[b]), L[b], R[b]) + Bb[b] * T2[b] for b in range(4)])[sel]
    for _ in range(4):
        for b in range(4):
            best = (np.inf, None, None)
            tb = np.zeros(60); tb[15 * b:15 * b + 15] = T2[b]; tb = tb[sel]
            for g in GRID:
                Lt = L[:b] + [g] + L[b + 1:]; Bt = Bb[:b] + [0.0] + Bb[b + 1:]
                r0 = yv - vec(Lt, Bt)
                bb = max(0.0, float(tb @ Ci @ r0) / float(tb @ Ci @ tb)) if use2h else 0.0
                r = r0 - bb * tb; x2 = float(r @ Ci @ r)
                if x2 < best[0]: best = (x2, g, bb)
            L[b], Bb[b] = best[1], best[2]
    r = yv - vec(L, Bb)
    return float(r @ Ci @ r), L, Bb, len(sel)
fsB = lambda lm: fB
fsD = lambda lm: f_for(N_of(lm)[0])
full = list(range(15)); prim = [i for i in range(15) if R[0, i] <= 0.31]
RES = dict(lane="CFG805", mutate=MUT, K2=bool(k2), sigma8=s8)
cB0, *_ = solve(fsB, full, False); cD0, *_ = solve(fsD, full, False)
k1 = abs((cD0 - cB0) - 148.7) < 0.5 or MUT
P(f"  K1 b=0: dchi2(D-B) all radii {cD0 - cB0:+.1f} (CFG804 +148.7): {'PASS' if k1 else 'FAIL'}")
for lab, idx in (("all", full), ("primary", prim)):
    cB, LB, bB, n = solve(fsB, idx, True); cD, LD, bD, _ = solve(fsD, idx, True)
    d = cD - cB; pD = stats.chi2.sf(cD, n - 8)
    RES[lab] = dict(chi2_B2h=cB, chi2_D2h=cD, dchi2=d, p_D2h=pD, b_D=bD, b_B=bB, logMb_D=LD)
    P(f"\n  [{lab}] B+2h chi2 {cB:.1f} (b {['%.2f' % v for v in bB]}); D_der+2h chi2 {cD:.1f} (b {['%.2f' % v for v in bD]}, p {pD:.3f}); dchi2 {d:+.1f}")
a = RES["all"]
cls = "OUTER GAP CLOSED" if (a["dchi2"] <= 4 and a["p_D2h"] >= 0.01) else ("NARROWED" if a["dchi2"] < 148.7 / 2 else "OPEN")
P(f"\n  CLASS (all radii): {cls}")
RES.update(K1=bool(k1), cls=cls)
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg805_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg805{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
