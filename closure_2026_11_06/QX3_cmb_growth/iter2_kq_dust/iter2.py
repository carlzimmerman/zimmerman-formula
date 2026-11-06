#!/usr/bin/env python3
"""QX3 iter2 (FROZEN_CRITERIA.md 93562260e2): v3s K(Q) sector as an n = 1 polytrope dust.
G1 PR4 lensing shape (mu -> inf), G2 mu_min from the Jeans growth ODE, G3 galaxy capture -> mu_max.
kappa = 1/2 FITTED; not theory closed.  No Planck parameter values: brackets only.  1 thread."""
import os, sys, json, math, itertools
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.integrate import solve_ivp, quad
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity/CFG917_cmb_lensing_gate"))
import cfg917_lib as LIB                                     # read only: PR4 data + binning rule
from classy import Class
D = LIB.load_pr4(); LMAX = LIB.LMAX; Larr = np.arange(LMAX + 1.0)
AS0 = 2.0e-9; ZPK = 20.0
CHI2_LINE = 18.48; DCHI2_LINE = 4.0; FCAP = 0.76; MB = 1e10; ROPT = 0.010  # Mpc
GMSUN = 4.30091e-9   # G in Mpc (km/s)^2 / Msun

def run_class(ob, od, H0, ns, pk=False):
    M = Class()
    p = {'output': 'tCl,lCl,mPk' if pk else 'tCl,lCl', 'l_max_scalars': LMAX + 100, 'h': H0 / 100, 'omega_b': ob,
         'omega_cdm': max(od, 1e-7), 'A_s': AS0, 'n_s': ns, 'tau_reio': 0.06, 'N_ur': 3.046, 'T_cmb': 2.7255}
    if pk: p.update({'P_k_max_1/Mpc': 12.0, 'z_max_pk': ZPK})
    M.set(p); M.compute(); return M

def X_of(M):
    pp = M.raw_cl(LMAX)['pp']; return (Larr * (Larr + 1)) ** 2 * pp / (2 * np.pi)

def best_amp_chi2(X):
    u = LIB.wsum(D["W"], X) + LIB.wsum(D["M"], X)
    a = LIB.qform(u, D["Cinv"], D["d"] + D["F"]); b = LIB.qform(u, D["Cinv"]); A = a / b
    r = A * u - D["F"] - D["d"]; return LIB.qform(r, D["Cinv"]), A

def k1():
    return LIB.pr4_chi2(D, LIB.load_ffp10())

# ---------------- G1
def g1_corner(ob, H0, ns):
    cache = {}
    def f(od):
        M = run_class(ob, od, H0, ns); c, A = best_amp_chi2(X_of(M)); M.struct_cleanup(); cache[od] = (c, A); return c
    r = minimize_scalar(f, bounds=(0.03, 0.25), method='bounded', options={'xatol': 2e-3})
    grid = {od: f(od) for od in (0.03, 0.08, 0.13, 0.18, 0.25)}   # guard against a local min
    od_best = min(list(grid) + [r.x], key=lambda o: cache[o][0])
    c, A = cache[od_best]
    Mb = run_class(ob, 1e-7, H0, ns); cm, Am = best_amp_chi2(X_of(Mb)); Mb.struct_cleanup()
    return dict(omega_b=ob, H0=H0, n_s=ns, omega_d_best=float(od_best), chi2_min=float(c), A_s_implied=float(A * AS0),
                chi2_grid={str(k): float(v) for k, v in grid.items()}, mutate_baryons_only_chi2=float(cm),
                mutate_A_s_implied=float(Am * AS0))

# ---------------- G2: Jeans growth ratio
def growth_ratio(M, ob, od, H0, mus, kgrid, zgrid):
    h = H0 / 100; Om_b0 = ob / h**2; Om_d0 = od / h**2
    lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000)
    lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t])
    dlnH_t = np.gradient(lnH_t, lna_t)
    Hz = lambda z: math.exp(np.interp(math.log(1 / (1 + z)), lna_t, lnH_t))
    H0c = M.Hubble(0.0)
    ai = 1 / 3401.0; adec = 1 / 1091.0
    lnz = np.log(1 / (1 + np.asarray(zgrid))); order = np.argsort(lnz); kv = np.asarray(kgrid); nk = len(kv)
    def solve(mu):
        """vectorised over k: implicit midpoint (A-stable, amplitude-preserving) on a fixed ln a grid that contains the output
        epochs; same linear equations as the frozen text."""
        grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz]))
        y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai
        rec = {}; tset = {float(x): i for i, x in enumerate(lnz)}
        I4 = np.eye(4)[None, :, :]
        def Amat(lna):
            a = math.exp(lna); E2 = math.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c**2; dl = float(np.interp(lna, lna_t, dlnH_t))
            Od = Om_d0 * a**-3 / E2; Ob = Om_b0 * a**-3 / E2; on = a > adec
            jeans = 0.0 if mu is None else (kv / (a * mu)) ** 2
            A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od * (1 - jeans); A[:, 1, 1] = -(2 + dl)
            if on:
                A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
            return A
        for n in range(len(grid) - 1):
            h_ = grid[n + 1] - grid[n]; A = Amat(0.5 * (grid[n] + grid[n + 1]))
            y = np.linalg.solve(I4 - 0.5 * h_ * A, ((I4 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
            t = float(grid[n + 1])
            if t in tset: rec[tset[t]] = y.copy()
        out = np.empty((nk, len(zgrid)))
        for jz in range(len(zgrid)):
            yy = rec[jz]; a = 1 / (1 + zgrid[jz]); E2 = math.exp(2 * np.interp(math.log(a), lna_t, lnH_t)) / H0c**2
            Od = Om_d0 * a**-3 / E2; Ob = Om_b0 * a**-3 / E2
            out[:, jz] = (Od * yy[:, 0] + Ob * yy[:, 2]) / (Od + Ob)
        return out
    ref = solve(None)
    return {mu: solve(mu) / ref for mu in mus}

def limber_ratio(M, H0, kgrid, zgrid, R):
    """S(L) = C_L^Limber[P R^2] / C_L^Limber[P], P = CLASS linear, weights (chi*-chi)/(chi chi*), (1+z)^2 Omega_m^2 constants cancel."""
    chis = M.angular_distance(1089.0) * (1 + 1089.0)
    chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid])
    lnk = np.log(kgrid)
    P = np.array([[M.pk_lin(k, z) for z in zgrid] for k in kgrid])
    w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])  # dchi = dz/H
    Ls = np.arange(2, LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
    for j in range(len(zgrid)):
        kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
        Pj = np.interp(np.log(kk[m]), lnk, P[:, j]); Rj = np.interp(np.log(kk[m]), lnk, R[:, j])
        num[m] += w[j] * Pj * Rj**2 / chi[j]**2; den[m] += w[j] * Pj / chi[j]**2
    S = np.ones(LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]
    zw = np.gradient(np.asarray(zgrid)); return S

def enclosed(xi):
    xi = np.minimum(xi, np.pi); return (np.sin(xi) - xi * np.cos(xi)) / np.pi

def g3(ob, od, H0, mus):
    h = H0 / 100; rhoc0 = 3 * (H0) ** 2 / (8 * np.pi * GMSUN)        # Msun/Mpc^3
    rho_m0 = (ob + od) / h**2 * rhoc0; rho_ta = 5.55 * rho_m0 * (1 + 2.0) ** 3
    Mhalo = MB * (ob + od) / ob                                        # generous (smallest halo holding M_b)
    rows = []
    for mu in mus:
        R = np.pi / mu; MJ = 4 * np.pi / 3 * rho_ta * R**3
        ratio = FCAP * (od / ob) * float(enclosed(np.array(mu * ROPT * 1.0)))   # xi = pi r/R = mu r
        captured = Mhalo > MJ
        rows.append(dict(mu=float(mu), core_R_kpc=R * 1e3, M_J=float(MJ), M_halo=float(Mhalo), captured=bool(captured),
                         Md_in_Ropt_over_Mb=float(ratio) if captured else 0.0,
                         pass_=bool((not captured) or ratio <= 0.3)))
    return rows

if __name__ == "__main__":
    out = dict(K1_ffp10_chi2=k1(), note="kappa = 1/2 FITTED; not theory closed")
    Mr = Class(); Mr.set({'output': 'tCl,lCl', 'l_max_scalars': LMAX + 100, 'h': 0.67, 'omega_b': 0.0224, 'omega_cdm': 0.12,
                          'A_s': 2.1e-9, 'n_s': 0.965, 'tau_reio': 0.06}); Mr.compute(); Xr = X_of(Mr); Mr.struct_cleanup()
    Xf = LIB.load_ffp10(); out["K1b_class_over_ffp10"] = {str(L): float(Xr[L] / Xf[L]) for L in (10, 40, 100, 400)}
    out["K1b_pass"] = all(abs(v - 1) <= 0.10 for v in out["K1b_class_over_ffp10"].values())
    print("K1b", out["K1b_class_over_ffp10"], out["K1b_pass"], flush=True)
    corners = list(itertools.product((0.0215, 0.0230), (65.0, 75.0), (0.95, 0.98)))
    G1 = [g1_corner(*c) for c in corners]; out["G1"] = G1
    worst = max(G1, key=lambda r: r["chi2_min"])
    out["G1_worst_chi2"] = worst["chi2_min"]; out["G1_pass"] = worst["chi2_min"] <= CHI2_LINE
    out["MUTATE_bites"] = all(r["mutate_baryons_only_chi2"] > CHI2_LINE for r in G1)
    print("G1 done", out["G1_worst_chi2"], out["MUTATE_bites"], flush=True)
    mus = np.logspace(0, 5, 26); kgrid = np.logspace(-4, 1, 70); zgrid = np.linspace(0.02, ZPK, 120)
    G2 = []
    for r in G1:
        M = run_class(r["omega_b"], r["omega_d_best"], r["H0"], r["n_s"], pk=True)
        X0 = X_of(M) ; c0, _ = best_amp_chi2(X0)
        Rs = growth_ratio(M, r["omega_b"], r["omega_d_best"], r["H0"], list(mus) + [1e6], kgrid, zgrid)
        k2 = float(np.max(np.abs(Rs[1e6] - 1)))
        rows = []
        for mu in mus:
            S = limber_ratio(M, r["H0"], kgrid, zgrid, Rs[mu]); c, _ = best_amp_chi2(X0 * S)
            rows.append(dict(mu=float(mu), dchi2=float(c - c0), S_L100=float(S[100]), S_L400=float(S[400])))
        okm = [x["mu"] for x in rows if x["dchi2"] <= DCHI2_LINE]
        # mu_min: smallest mu above which every grid mu passes
        mu_min = None
        for i in range(len(rows)):
            if all(x["dchi2"] <= DCHI2_LINE for x in rows[i:]): mu_min = rows[i]["mu"]; break
        G2.append(dict(corner=[r["omega_b"], r["H0"], r["n_s"]], K2_maxdev_mu1e6=k2, chi2_inf=float(c0), rows=rows, mu_min=mu_min))
        M.struct_cleanup(); print("G2 corner", G2[-1]["corner"], mu_min, k2, flush=True)
    out["G2"] = G2
    out["mu_min_worst"] = max(g["mu_min"] for g in G2 if g["mu_min"] is not None) if all(g["mu_min"] for g in G2) else None
    out["K2_pass"] = all(g["K2_maxdev_mu1e6"] <= 1e-3 for g in G2)
    G3 = []
    for r in G1:
        rows = g3(r["omega_b"], r["omega_d_best"], r["H0"], list(np.logspace(-1, 5, 61)))
        passing = [x["mu"] for x in rows if x["pass_"]]
        # mu_max: largest mu with every smaller mu passing
        mu_max = None
        for x in rows:
            if x["pass_"]: mu_max = x["mu"]
            else: break
        G3.append(dict(corner=[r["omega_b"], r["H0"], r["n_s"]], mu_max=mu_max, rows=rows))
    out["G3"] = G3
    out["mu_max_best"] = max((g["mu_max"] or 0) for g in G3)
    out["window"] = (out["mu_min_worst"] is not None) and out["mu_min_worst"] <= out["mu_max_best"]
    if not out["K1b_pass"]: lab = "NO VERDICT (K1b)"
    elif not out["G1_pass"]: lab = "FAIL (G1 shape)"
    elif not out["MUTATE_bites"]: lab = "NO VERDICT (G1 MUTATE does not bite)"
    elif out["window"]: lab = "PASS (window exists)"
    else: lab = "FAIL (no window: mu_min > mu_max)"
    out["label"] = lab
    json.dump(out, open(os.path.join(HERE, "iter2.json"), "w"), indent=1)
    print("LABEL", lab, "mu_min", out["mu_min_worst"], "mu_max", out["mu_max_best"], "G1 worst", out["G1_worst_chi2"])
