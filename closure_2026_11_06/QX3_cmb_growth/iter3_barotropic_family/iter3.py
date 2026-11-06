#!/usr/bin/env python3
"""QX3 iter3 (FROZEN_CRITERIA.md 93562260e2): barotropic K(Q) class, k_J = mu0 (rho_d/rho_d0)^(-beta).
Grid beta in [-2,2] (41), mu0 in [1e-1,1e5] Mpc^-1 (61). G3' and G4' are analytic; G2' (the growth ODE, iter2's
physics, vectorised over k) is evaluated wherever G3' and G4' both pass: only there can a member pass all three.
kappa = 1/2 FITTED; not theory closed.  QX3_MUTATE=1 flips G3' (separate outputs).  1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../iter2_kq_dust"))
import iter2 as I2
MUT = os.environ.get("QX3_MUTATE") == "1"
GMSUN = I2.GMSUN
it2 = json.load(open(os.path.join(HERE, "../iter2_kq_dust/iter2.json")))
worst = max(it2["G1"], key=lambda r: r["chi2_min"])
ob, od, H0, ns = worst["omega_b"], worst["omega_d_best"], worst["H0"], worst["n_s"]
h = H0 / 100
betas = np.linspace(-2, 2, 41); mu0s = np.logspace(-1, 5, 61)
rhoc0 = 3 * H0**2 / (8 * np.pi * GMSUN); rho_m0 = (ob + od) / h**2 * rhoc0
zc = 2.0; rho_ta = 5.55 * rho_m0 * (1 + zc)**3; r_ta = (10**11.5 / (4 * np.pi / 3 * rho_ta)) ** (1 / 3)   # Mpc
dens_ratio_ta = 5.55 * (1 + zc)**3                     # rho_d at turnaround / rho_d0
def g3(beta, mu0):
    lam = 2 * np.pi / (mu0 * dens_ratio_ta ** (-beta)); return (lam <= r_ta) if MUT else (lam >= r_ta)
def g4(beta, mu0):
    kJ = mu0 * 64.0 ** (-beta); return 2 * np.pi * 4.0 / kJ <= 0.42 / h

M = I2.run_class(ob, od, H0, ns, pk=True)
X0 = I2.X_of(M); c0, _ = I2.best_amp_chi2(X0)
kgrid = np.logspace(-4, 1, 70); zgrid = np.linspace(0.02, I2.ZPK, 120)
lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000)
lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t]); dlnH_t = np.gradient(lnH_t, lna_t)
H0c = M.Hubble(0.0); Om_b0 = ob / h**2; Om_d0 = od / h**2; ai = 1 / 3401.0; adec = 1 / 1091.0
lnz = np.log(1 / (1 + zgrid)); order = np.argsort(lnz); nk = len(kgrid)
def solve(beta, mu0):
    """iter2's implicit-midpoint solver (A1b), with k_J = mu0 a^(3 beta)."""
    grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz]))
    y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai
    rec = {}; tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
    for n in range(len(grid) - 1):
        hh = grid[n + 1] - grid[n]; lna = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lna)
        E2 = math.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c**2; dl = float(np.interp(lna, lna_t, dlnH_t))
        Od = Om_d0 * a**-3 / E2; Ob = Om_b0 * a**-3 / E2; on = a > adec
        jeans = 0.0 if mu0 is None else (kgrid / (a * mu0 * a ** (3 * beta))) ** 2
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
ref = solve(0.0, None)
def g2(beta, mu0):
    R = solve(beta, mu0) / ref; S = I2.limber_ratio(M, H0, kgrid, zgrid, R); c, _ = I2.best_amp_chi2(X0 * S); return float(c - c0)
# K: beta = 0 reproduces iter2's G2 at the same mu (worst corner) to 1e-2 in dchi2
k_iter2 = None
for g in it2["G2"]:
    if g["corner"] == [ob, H0, ns]:
        r = min(g["rows"], key=lambda x: abs(math.log(x["mu"] / 1e3))); k_iter2 = dict(mu=r["mu"], iter2=r["dchi2"], iter3=g2(0.0, r["mu"]))
cand = [(b, m) for b in betas for m in mu0s if g3(b, m) and g4(b, m)]
evaluated = []; passing = []
if MUT:
    cand = sorted(cand, key=lambda t: -t[1])[:3]
for (b, m) in cand:
    d = g2(b, m); evaluated.append(dict(beta=float(b), mu0=float(m), dchi2=d))
    if d <= I2.DCHI2_LINE: passing.append(evaluated[-1])
    if MUT and passing: break
closest = min(evaluated, key=lambda x: x["dchi2"]) if evaluated else None
# map of the analytic gates per beta: allowed mu0 interval from G4' (lower) and G3' (upper)
mp = []
for b in betas:
    lo = 2 * np.pi * 4.0 * 64.0 ** b / (0.42 / h); hi = 2 * np.pi * dens_ratio_ta ** b / r_ta
    mp.append(dict(beta=float(b), mu0_forest_min=float(lo), mu0_galaxy_max=float(hi), G3G4_window=bool(lo <= hi)))
out = dict(mode="MUTATE_flip_G3" if MUT else "main", corner=[ob, od, H0, ns], r_ta_kpc=r_ta * 1e3, chi2_inf=c0, K_beta0_vs_iter2=k_iter2,
           n_G3G4_cells=len(cand), evaluated=evaluated, passing=passing, closest=closest, analytic_map=mp,
           label=("PASS (member found)" if passing else "FAIL (class no-go on grid)") if not MUT else
                 ("MUTATE bites (members pass flipped gates)" if passing else "MUTATE does NOT bite"),
           note="kappa = 1/2 FITTED; not theory closed")
fn = "iter3_MUTATE" if MUT else "iter3"
json.dump(out, open(os.path.join(HERE, fn + ".json"), "w"), indent=1)
print(out["label"], "cells", len(cand), "closest", closest, "K", k_iter2)
