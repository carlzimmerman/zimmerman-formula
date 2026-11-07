#!/usr/bin/env python3
"""QX28 G6 (FROZEN_CRITERIA.md c5852ac12f): T1 / growth for the condensed-phase equation of state P = K rho^3 at the
cosmic mean (c_s^2 = 3 K rho_bar^2), K = K_min per footing from qx28.json (SPARC G5 + KiDS only).
The growth solver is QX27's qx27_growth.py solver (QX3 iter2 ODE, read-only import of iter2: CLASS background, PR4
lensing, Limber ratio), copied with the Jeans term switched from sigma(a) to c_s(a).
G6a: comoving Jeans length <= 0.42/h Mpc at z = 10, 100, 1089 (as posed). G6b: Delta chi2 <= 4 with Jeans term for
z < 10 only (generous). G6c: forest, comoving Jeans length <= 0.42/h Mpc at z = 3.
    python3 qx28_growth.py -> qx28_growth.json/.out
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


RHO_CRIT_H2 = 277.5                       # Msun/kpc^3 per h^2 (rho_crit = 2.775e11 h^2 Msun/Mpc^3)
def cs(a, K):                              # condensed-phase sound speed at the cosmic mean, km/s: c_s^2 = 3 K rho^2
    return math.sqrt(3 * K) * od * RHO_CRIT_H2 * a ** -3
def kJ_phys(a, K, adiabatic=True):         # physical Jeans wavenumber, Mpc^-1 (second argument kept for the solver)
    return math.sqrt(1.5 * Om_d0 * a ** -3) * H0 / cs(a, K)


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


Q = json.load(open(os.path.join(HERE, "qx28.json")))
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
P("QX28 G6: growth + T1 for the condensed-phase EOS P = K rho^3 at the cosmic mean. kappa = 1/2 FITTED; not theory closed. Criteria c5852ac12f.")
P(f"corner omega_b {ob}, omega_d {od:.4f}, H0 {H0}, n_s {ns}; chi2(cold) {c0:.2f}; rho_d0 {od*RHO_CRIT_H2:.3f} Msun/kpc^3")
K1 = dchi2(1e-30)
P(f"K1 K 1e-30 (cold limit): Delta chi2 {K1:.2e} (line 1e-2) -> {'PASS' if abs(K1) <= 1e-2 else 'FAIL'}")
Kmut = dchi2(1e3)
P(f"control K 1e3 (stiff sector from z 10): Delta chi2 {Kmut:.1f} -> {'BITES' if Kmut > I2.DCHI2_LINE else 'DOES NOT BITE'}")
RES = dict(lane="QX28 G6", criteria="c5852ac12f", corner=[ob, od, H0, ns], chi2_cold=c0, K1=K1, control_K1e3=Kmut, rows={}, note="kappa = 1/2 FITTED; not theory closed")
line = 0.42 / h; CKMS = 299792.458
for f, e in Q["per_foot"].items():
    K = e["K_min"]
    lam = {z: 2 * math.pi * (1 + z) / kJ_phys(1 / (1 + z), K) for z in (3, 10, 100, 1089)}
    w1089 = K * (od * RHO_CRIT_H2 * 1090.0 ** 3) ** 2 / CKMS ** 2
    g = dchi2(K)
    row = dict(K=K, cs_kms={str(z): cs(1 / (1 + z), K) for z in (0, 3, 10, 100, 1089)}, lambda_J_comoving_Mpc={str(z): v for z, v in lam.items()},
               w_1089=w1089, line_Mpc=line, G6a=bool(all(lam[z] <= line for z in (10, 100, 1089))), dchi2=g, G6b=bool(g <= I2.DCHI2_LINE), G6c=bool(lam[3] <= line))
    row["G6"] = bool(row["G6a"] and row["G6b"] and row["G6c"]); RES["rows"][f] = row
    P(f"[{f}] K {K:.4g}: c_s(z 0, 3, 10, 100, 1089) = " + ", ".join(f"{v:.3g}" for v in row["cs_kms"].values()) + " km/s; w(1089) " + f"{w1089:.3g}")
    P(f"   G6a lambda_J comoving z 10 / 100 / 1089: {lam[10]:.3g} / {lam[100]:.3g} / {lam[1089]:.3g} Mpc vs {line:.3f} -> {'PASS' if row['G6a'] else 'FAIL'}")
    P(f"   G6b Delta chi2 {g:.3f} (line 4; Jeans term z < 10 only) -> {'PASS' if row['G6b'] else 'FAIL'}")
    P(f"   G6c forest lambda_J(z 3) {lam[3]:.3f} Mpc vs {line:.3f} -> {'PASS' if row['G6c'] else 'FAIL'}")
    P(f"   G6 -> {'PASS' if row['G6'] else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "qx28_growth.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "qx28_growth.out"), "w").write("\n".join(OUT) + "\n")

# ---------------- reported (not graded): the K at which growth would pass (calibration fails below K_min)
P("\nReported: Delta chi2 against K (Jeans term z < 10), and K_min from qx28.json:")
RES["K_scan"] = []
for K in (1e-10, 1e-9, 1e-8, 3e-8, 1e-7, 3e-7, 1e-6):
    d = dchi2(K); RES["K_scan"].append(dict(K=K, dchi2=d)); P(f"   K {K:.1e}: Delta chi2 {d:9.3f}")
ok = [r["K"] for r in RES["K_scan"] if r["dchi2"] <= I2.DCHI2_LINE]
RES["K_max_growth"] = max(ok) if ok else None
P(f"   largest scanned K passing G6b: {RES['K_max_growth']}; K_min (galaxies) canonical {Q['per_foot']['canonical']['K_min']:.3g}, alt {Q['per_foot']['alt']['K_min']:.3g}")
json.dump(RES, open(os.path.join(HERE, "qx28_growth.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "qx28_growth.out"), "w").write("\n".join(OUT) + "\n")
