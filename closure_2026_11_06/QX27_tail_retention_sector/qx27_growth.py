#!/usr/bin/env python3
"""QX27 G6 (FROZEN_CRITERIA.md 8e1126f9e3): T1 / growth for the tail sector at each n's galaxy-fixed v0.
QX3 iter2/iter3 growth ODE (read-only import of iter2: CLASS background, PR4 lensing, Limber ratio) at iter2's worst
corner; Jeans term for z < z_h only: k_J(a) = sqrt(1.5 Omega_d0 a^-3) H0 / sigma(a) (physical, Mpc^-1).
Graded: sigma(a) = sigma0/a (one-time heating, collisionless), z_h = 10. Reported: sigma constant; z_h = 20.
G6c forest: 2 pi (1+z)/k_J <= 0.42/h Mpc at z = 3.  Reads qx27.json (v0_min, sigma_1D per n and footing).
    python3 qx27_growth.py -> qx27_growth.json/.out
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
Q = json.load(open(os.path.join(HERE, "qx27.json")))

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
P("QX27 G6: growth + forest for the tail sector after z_h. kappa = 1/2 FITTED; not theory closed. Criteria 8e1126f9e3.")
P(f"corner omega_b {ob}, omega_d {od:.4f}, H0 {H0}, n_s {ns}; chi2(cold) {c0:.2f}")
K1 = dchi2(0.01)                          # known answer: sigma 0.01 km/s is cold on every graded scale
P(f"K1 sigma0 0.01 km/s: Delta chi2 {K1:.2e} (line 1e-2) -> {'PASS' if abs(K1) <= 1e-2 else 'FAIL'}")
# baryons-only-like control: sector smooth from z = 1090 on (huge sigma, z_h = 1090) must fail
Kmut = dchi2(1e5, z_h=1089.0)
P(f"control (sector smooth from z 1089, sigma 1e5): Delta chi2 {Kmut:.1f} -> {'BITES' if Kmut > I2.DCHI2_LINE else 'DOES NOT BITE'}")
RES = dict(lane="QX27 G6", criteria="8e1126f9e3", corner=[ob, od, H0, ns], chi2_cold=c0, K1=K1, control_smooth_from_rec=Kmut, rows={},
           note="kappa = 1/2 FITTED; not theory closed")
for n, byf in Q["per_n"].items():
    for f, e in byf.items():
        if e.get("v0_min") is None: continue
        s0 = e["sigma1d"]
        g = dchi2(s0); gc = dchi2(s0, adiabatic=False); g20 = dchi2(s0, z_h=20.0)
        kj3 = kJ_phys(0.25, s0, True); lam = 2 * math.pi * 4.0 / kj3; lamc = 2 * math.pi * 4.0 / kJ_phys(0.25, s0, False)
        row = dict(v0=e["v0_min"], sigma1d=s0, dchi2=g, dchi2_const_sigma=gc, dchi2_zh20=g20, G6b=bool(g <= I2.DCHI2_LINE),
                   forest_lambda_J_Mpc=lam, forest_lambda_J_const_sigma_Mpc=lamc, forest_line_Mpc=0.42 / h, G6c=bool(lam <= 0.42 / h))
        row["G6"] = bool(row["G6b"] and row["G6c"]); RES["rows"][f"{n}|{f}"] = row
        P(f"n {n} [{f}] v0 {e['v0_min']:.1f} sigma {s0:.1f}: G6b Delta chi2 {g:.1f} (const sigma {gc:.1f}; z_h 20 {g20:.1f}) line 4 -> {'PASS' if row['G6b'] else 'FAIL'}; "
              f"G6c lambda_J(z 3) {lam:.1f} Mpc (const sigma {lamc:.1f}) vs {0.42/h:.3f} -> {'PASS' if row['G6c'] else 'FAIL'}")
RES["G6_any_pass"] = bool(any(r["G6"] for r in RES["rows"].values()))
P(f"G6 any (n, footing) passes: {RES['G6_any_pass']}")
json.dump(RES, open(os.path.join(HERE, "qx27_growth.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "qx27_growth.out"), "w").write("\n".join(OUT) + "\n")

# ---------------- reported (not graded): where growth would allow the sector, and the fully smooth limit
P("\nReported: sigma0 at which growth passes (adiabatic, z_h 10), and the fully smooth sector after z_h:")
RES["sigma_scan"] = []
for s0 in (1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 1e5):
    d = dchi2(s0); RES["sigma_scan"].append(dict(sigma0=s0, dchi2=d)); P(f"   sigma0 {s0:8.1f} km/s: Delta chi2 {d:9.2f}  forest lambda_J(z 3) {2*math.pi*4/kJ_phys(0.25, s0):.3f} Mpc")
ok = [r["sigma0"] for r in RES["sigma_scan"] if r["dchi2"] <= I2.DCHI2_LINE]
RES["sigma_max_growth"] = max(ok) if ok else None
P(f"   largest scanned sigma0 passing growth: {RES['sigma_max_growth']}")
json.dump(RES, open(os.path.join(HERE, "qx27_growth.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "qx27_growth.out"), "w").write("\n".join(OUT) + "\n")
