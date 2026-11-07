#!/usr/bin/env python3
"""NC2 (FROZEN_CRITERIA.md b1ed7d2541): G2 (CMB lensing L <= 400, corrected Limber kernel for the clumps), G4 (mu distortion),
and the implied peaks bias b, both footings (QX15 main fits).
    python3 nc2_g2g4.py            -> nc2_g2g4.json / .out
    python3 nc2_g2g4.py --mutate   -> nc2_g2g4_MUTATE.json / .out  (M2: f_in 0 must reproduce the mean component and pass)
QX3 iter2 (PR4 lensing machinery) imported read-only. Cold dark energy, never dark matter; no particle.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, resource, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
trap = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
CL6 = os.path.join(REPO, "closure_2026_11_06")
MUT = "--mutate" in sys.argv; TAG = "nc2_g2g4_MUTATE" if MUT else "nc2_g2g4"; OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
D2 = os.path.join(CL6, "QX3_cmb_growth", "iter2_kq_dust"); sys.path.insert(0, D2)
cwd = os.getcwd(); os.chdir(D2)
with contextlib.redirect_stdout(io.StringIO()): import iter2 as I2
os.chdir(cwd)
from classy import Class
RHOU = 2.77536627e11                       # Msun/Mpc^3 per unit omega
MCL = (1e13, 1e14, 1e15); FIN = 0.0 if MUT else 1.0
KP = 0.05; ZREC = 1090.0; DC = 1.686; STP, STQ = 0.3, 0.707

def limber_n(M, kgrid, zgrid, R, n):
    """GL1's kernel: I2.limber_ratio's code with the weight x (chi/(L + 1/2))^n (n = 4 corrected, n = 0 record)."""
    chis = M.angular_distance(1089.0) * 1090.0
    chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid]); lnk = np.log(kgrid)
    Pm = np.array([[M.pk_lin(k, z) for z in zgrid] for k in kgrid])
    w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])
    Ls = np.arange(2, I2.LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
    for j in range(len(zgrid)):
        kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
        Pj = np.interp(np.log(kk[m]), lnk, Pm[:, j]); Rj = np.interp(np.log(kk[m]), lnk, R[:, j])
        ex = (chi[j] / (Ls[m] + 0.5)) ** n if n else 1.0
        num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex
    S = np.ones(I2.LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]; return S
def u(x):
    x = np.maximum(np.asarray(x, float), 1e-8); return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3

RES = dict(lane="NC2", part="G2 G4 implied-b", tag=TAG, criteria="b1ed7d2541", KA={}, footings={}, note="kappa = 1/2 FITTED; not theory closed")
# ---------------------------------------------------------------- KA2 (GL1's kernel on QX3 iter2's worst corner)
it2 = json.load(open(os.path.join(D2, "iter2.json"))); wst = max(it2["G1"], key=lambda r: r["chi2_min"])
MW = I2.run_class(wst["omega_b"], wst["omega_d_best"], wst["H0"], wst["n_s"], pk=True)
kg = np.logspace(-4, 1, 70); zg = np.linspace(0.02, I2.ZPK, 120)
Rt = 1 - 0.1 * np.outer(np.tanh(kg), np.exp(-zg / 2))
d0 = float(np.max(np.abs(limber_n(MW, kg, zg, Rt, 0) / I2.limber_ratio(MW, wst["H0"], kg, zg, Rt) - 1)))
s1 = float(np.max(np.abs(limber_n(MW, kg, zg, np.ones((70, 120)), 4)[2:] - 1)))
chis = MW.angular_distance(1089.0) * 1090.0; chi = np.array([MW.angular_distance(z) * (1 + z) for z in zg]); Hz = np.array([MW.Hubble(z) for z in zg])
Pm = np.array([[MW.pk_lin(k, z) for z in zg] for k in kg]); dz = np.gradient(zg); shp = []
for L in (20, 50, 100, 200, 300, 400):
    kk = (L + 0.5) / chi; m = (kk >= kg[0]) & (kk <= kg[-1]); v = 0.0
    for j in np.where(m)[0]:
        v += ((chis - chi[j]) / (chi[j] * chis)) ** 2 * (1 + zg[j]) ** 2 / Hz[j] * math.exp(np.interp(math.log(kk[j]), np.log(kg), np.log(Pm[:, j]))) / chi[j] ** 2 * (chi[j] / (L + 0.5)) ** 4 * dz[j]
    shp.append(v)
pp = MW.raw_cl(500)["pp"]; r = np.array(shp) / pp[[20, 50, 100, 200, 300, 400]]; r = (r / r[2]).tolist()
gl1 = [1.005, 1.006, 1.0, 0.991, 0.984, 0.980]; dsh = max(abs(a - b) for a, b in zip(r, gl1))
MW.struct_cleanup()
RES["KA"]["KA2"] = dict(n0_vs_record=d0, n4_S_at_R1=s1, shape=r, gl1=gl1, max_d=dsh, pass_=bool(d0 <= 1e-12 and s1 <= 1e-12 and dsh <= 1e-3 + 5e-4))
P(f"KA2: n 0 vs iter2 limber_ratio {d0:.1e}; n 4 at R = 1 |S-1| {s1:.1e}; shape " + " ".join(f"{x:.3f}" for x in r) + f" vs GL1 (max |d| {dsh:.1e}) -> {'PASS' if RES['KA']['KA2']['pass_'] else 'FAIL'}")

# ---------------------------------------------------------------- per footing
def nu_bL(M, sigM):
    nu = DC / sigM; qn = STQ * nu ** 2
    return nu, (qn - 1) / DC + 2 * STP / (DC * (1 + qn ** STP))
for foot in ("canonical", "alt"):
    fit = json.load(open(os.path.join(CL6, "QX15_cmb_primary_likelihood", "parts", f"fit_{foot}_main.json")))
    th = fit["theta"]; h = fit["h"]; ob, od = th["omega_b"], th["omega_d"]; R = od / ob; fc = R / (1 + R)
    rho_c = od * RHOU; rho_m = (ob + od) * RHOU
    M = Class(); M.set({'output': 'tCl,lCl,mPk,mTk', 'l_max_scalars': I2.LMAX + 100, 'h': h, 'omega_b': ob, 'omega_cdm': od,
                        'A_s': math.exp(th["lnAs1e10"]) * 1e-10, 'n_s': th["n_s"], 'tau_reio': th["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255,
                        'P_k_max_1/Mpc': 60.0, 'z_max_pk': I2.ZPK}); M.compute()
    MT = Class(); MT.set({'output': 'dTk', 'gauge': 'synchronous', 'matter_source_in_current_gauge': 'yes', 'h': h, 'omega_b': ob, 'omega_cdm': od, 'A_s': math.exp(th["lnAs1e10"]) * 1e-10, 'n_s': th["n_s"],
                          'tau_reio': th["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 1.0, 'z_max_pk': 1100.0}); MT.compute()
    X0 = I2.X_of(M); c_mean, A_mean = I2.best_amp_chi2(X0)
    F = dict(setting=dict(omega_b=ob, omega_d=od, h=h, R=R, f_c=fc, theta=th), G2a=dict(chi2=float(c_mean), A_refit=float(A_mean), pass_=bool(c_mean <= 18.48)))
    P(f"[{foot}] G2a mean component: PR4 lensing chi2 {c_mean:.3f} (A refit {A_mean:.4f}) -> {'PASS' if c_mean <= 18.48 else 'FAIL'}")
    # implied peaks bias
    kk_ = np.logspace(-4, math.log10(59.0), 900); lk_ = np.log(kk_); pk0 = np.array([M.pk_lin(k, 0.0) for k in kk_])
    t0 = MT.get_transfer(z=0.0); tr = MT.get_transfer(z=ZREC); MT.struct_cleanup()
    kt = t0["k (h/Mpc)"] * h
    ratio_kp = float(np.interp(math.log(KP), np.log(kt), t0["d_cdm"]) / np.interp(math.log(KP), np.log(kt), tr["d_cdm"]))
    F["implied_b"] = {}; F["G2b"] = {}; F["G4"] = {}
    for Mc in MCL:
        Mt = Mc * (1 + 1 / R); rcl = (3 * Mt / (4 * math.pi * rho_m)) ** (1 / 3); ncl = rho_c / Mc
        sig = math.sqrt(trap(u(kk_ * rcl) ** 2 * kk_ ** 3 * pk0 / (2 * math.pi ** 2), lk_))
        nu, bL = nu_bL(Mt, sig); bimp = 1 + bL * ratio_kp
        F["implied_b"][f"{Mc:.0e}"] = dict(M_tot=Mt, r_cl=rcl, n_cl=ncl, sigma=sig, nu=nu, b_L=bL, b_E=1 + bL, d_cdm_ratio_z0_over_zrec_kp=ratio_kp, b_implied_rec=bimp)
        P(f"[{foot}] M_cl {Mc:.0e}: M_tot {Mt:.3e}, r_cl {rcl:.2f} Mpc, n_cl {ncl:.3e} /Mpc^3; nu {nu:.3f}, b_L {bL:.3f} (b_E {1+bL:.3f}); delta_c(z0)/delta_c(z_rec) at k_p {ratio_kp:.1f} -> implied b at recombination {bimp:.4g}")
        # G2b: clumps' Poisson power through the corrected kernel
        Pcl = lambda k: FIN ** 2 * fc ** 2 * u(k * rcl) ** 2 / ncl
        Pad = np.array([[M.pk_lin(k, z) for z in zg] for k in kg])
        Rr = np.sqrt(1 + Pcl(kg)[:, None] / Pad)
        S4 = limber_n(M, kg, zg, Rr, 4); c4, _ = I2.best_amp_chi2(X0 * S4)
        g2b = dict(chi2=float(c4), dchi2=float(c4 - c_mean), S_L100=float(S4[100]), S_L400=float(S4[400]), pass_=bool(c4 <= 18.48 and c4 - c_mean <= 4))
        F["G2b"][f"{Mc:.0e}"] = g2b
        P(f"[{foot}] G2b M_cl {Mc:.0e}: S(L 100) {S4[100]:.4g}, S(L 400) {S4[400]:.4g}; chi2 {c4:.2f} (d {c4 - c_mean:+.2f}) -> {'PASS' if g2b['pass_'] else 'FAIL'}")
        # G4 mu distortion (clump power treated as adiabatic: upper bound)
        kmu = np.logspace(-1, 5, 3000); lkm = np.log(kmu)
        Wmu = 2.27 * (np.exp(-(kmu / 1360.0) ** 2 / (1 + (kmu / 260.0) ** 0.3 + kmu / 340.0)) - np.exp(-(kmu / 32.0) ** 2))
        out = {}
        for rd in ("P", "C"):
            PS = FIN ** 2 * u(kmu * rcl) ** 2 / ncl * (1.0 if rd == "P" else np.minimum(1.0, (kmu * rcl) ** 4))
            D2S = kmu ** 3 * PS / (2 * math.pi ** 2); integ = D2S * Wmu
            mu = float(trap(integ, lkm)); lo = float(trap(np.where(kmu < 50, integ, 0.0), lkm))
            out[rd] = dict(mu=mu, mu_from_k_lt_50=lo, frac_below_50=(lo / mu if mu != 0 else None), Delta2S_k50=float(np.interp(math.log(50), lkm, D2S)),
                           pass_=bool(abs(mu) <= 9e-5))
        F["G4"][f"{Mc:.0e}"] = out
        P(f"[{foot}] G4 M_cl {Mc:.0e}: mu P {out['P']['mu']:.3e} (k<50 part {out['P']['mu_from_k_lt_50']:.2e}), C {out['C']['mu']:.3e} -> P {'PASS' if out['P']['pass_'] else 'FAIL'}, C {'PASS' if out['C']['pass_'] else 'FAIL'}")
    M.struct_cleanup()
    RES["footings"][foot] = F
if MUT:
    ok = all(abs(F["G2b"][k]["dchi2"]) <= 1e-9 and F["G4"][k]["P"]["mu"] == 0 for F in RES["footings"].values() for k in F["G2b"])
    RES["MUTATE"] = dict(M2_uniform_reproduces_mean=bool(ok)); P(f"MUTATE M2 (f_in 0): G2b = mean component and mu = 0: {'OK' if ok else 'NOT OK'}")
RES["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6; RES["seconds"] = time.time() - T0
P(f"peak RSS {RES['peak_rss_MB']:.0f} MB; {RES['seconds']:.0f} s. kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
