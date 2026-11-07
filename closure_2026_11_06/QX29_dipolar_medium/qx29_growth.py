#!/usr/bin/env python3
"""QX29 G6 (FROZEN_CRITERIA.md 346612b24b): growth + CMB-lensing shape for the dipolar medium's monopole.
The monopole is pressureless dust from before recombination, so it is QX27's cold reference (no Jeans term).
The solver below is QX27's G6 machinery (qx27_growth.py, copied verbatim up to its output block; QX3 iter2 read-only:
CLASS background, PR4 lensing, Limber ratio, iter2's worst corner). Graded under QX3's assumption A-web: the
polarization (a0) does not enter at linear order; AQUAL about g = 0 is not linearizable, so this is CONDITIONAL.
a0 does not enter here, so the two footings give the same number (stated, not pooled).
    python3 qx29_growth.py -> qx29_growth.json/.out
kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
I2DIR = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust"); sys.path.insert(0, I2DIR)
import iter2 as I2                                                       # read-only
it2 = json.load(open(os.path.join(I2DIR, "iter2.json")))
worst = max(it2["G1"], key=lambda r: r["chi2_min"])
ob, od, H0, ns = worst["omega_b"], worst["omega_d_best"], worst["H0"], worst["n_s"]
h = H0 / 100

M = I2.run_class(ob, od, H0, ns, pk=True)
X0 = I2.X_of(M); c0, _ = I2.best_amp_chi2(X0)
kgrid = np.logspace(-4, 1, 70); zgrid = np.linspace(0.02, I2.ZPK, 120)
lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000)
lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t]); dlnH_t = np.gradient(lnH_t, lna_t)
H0c = M.Hubble(0.0); Om_b0 = ob / h**2; Om_d0 = od / h**2; ai = 1 / 3401.0; adec = 1 / 1091.0
lnz = np.log(1 / (1 + zgrid)); nk = len(kgrid)


def kJ_phys(a, sigma0, adiabatic=True):
    sig = sigma0 / a if adiabatic else sigma0
    return math.sqrt(1.5 * Om_d0 * a ** -3) * H0 / sig


def solve(sigma0, z_h=10.0, adiabatic=True):
    """iter3's implicit-midpoint solver; Jeans term on for a > a_h only (sigma0 None: cold reference)."""
    a_h = 1 / (1 + z_h)
    grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz]))
    y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai
    rec = {}; tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
    for n in range(len(grid) - 1):
        hh = grid[n + 1] - grid[n]; lna = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lna)
        E2 = math.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c**2; dl = float(np.interp(lna, lna_t, dlnH_t))
        Od = Om_d0 * a**-3 / E2; Ob = Om_b0 * a**-3 / E2; on = a > adec
        jeans = 0.0 if (sigma0 is None or a <= a_h) else (kgrid / (a * kJ_phys(a, sigma0, adiabatic))) ** 2
        A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od * (1 - jeans); A[:, 1, 1] = -(2 + dl)
        if on:
            A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
        y = np.linalg.solve(I4 - 0.5 * hh * A, ((I4 + 0.5 * hh * A) @ y[:, :, None]))[:, :, 0]
        t = float(grid[n + 1])
        if t in tset: rec[tset[t]] = y.copy()
    dm = np.empty((nk, len(zgrid)))
    for jz in range(len(zgrid)):
        yy = rec[jz]; a = 1 / (1 + zgrid[jz]); E2 = math.exp(2 * np.interp(math.log(a), lna_t, lnH_t)) / H0c**2
        Od = Om_d0 * a**-3 / E2; Ob = Om_b0 * a**-3 / E2; dm[:, jz] = (Od * yy[:, 0] + Ob * yy[:, 2]) / (Od + Ob)
    return dm


ref = solve(None)
def dchi2(sigma0, **kw):
    R = solve(sigma0, **kw) / ref; S = I2.limber_ratio(M, H0, kgrid, zgrid, R); c, _ = I2.best_amp_chi2(X0 * S); return float(c - c0)



OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
P("QX29 G6: dipolar medium monopole = cold dust. kappa = 1/2 FITTED; not theory closed. Criteria 346612b24b.")
P(f"corner omega_b {ob}, omega_d {od:.4f}, H0 {H0}, n_s {ns}; chi2(cold) {c0:.2f}")
R_med = solve(None) / ref; S = I2.limber_ratio(M, H0, kgrid, zgrid, R_med); cm, _ = I2.best_amp_chi2(X0 * S); dmed = float(cm - c0)
K1 = dchi2(0.01); Kmut = dchi2(1e5, z_h=1089.0)
P(f"medium (pressureless monopole, A-web): Delta chi2 {dmed:.2e} (line {I2.DCHI2_LINE}) -> {'PASS [A-web CONDITIONAL]' if dmed <= I2.DCHI2_LINE else 'FAIL'}")
P(f"control K1 sigma0 0.01 km/s: Delta chi2 {K1:.2e} (cold limit recovered: {'yes' if abs(K1) <= 1e-2 else 'no'})")
P(f"control medium smooth from z 1089 (sigma 1e5): Delta chi2 {Kmut:.1f} -> {'gate has power' if Kmut > I2.DCHI2_LINE else 'NO POWER'}")
RES = dict(lane="QX29 G6", criteria="346612b24b", corner=[ob, od, H0, ns], chi2_cold=c0, dchi2_medium=dmed, K1=K1, control_smooth=Kmut,
           G6=("PASS [A-web CONDITIONAL]" if dmed <= I2.DCHI2_LINE and Kmut > I2.DCHI2_LINE else "FAIL or NO POWER"), note="kappa = 1/2 FITTED; not theory closed")
json.dump(RES, open(os.path.join(HERE, "qx29_growth.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "qx29_growth.out"), "w").write("\n".join(OUT) + "\n")
