#!/usr/bin/env python3
"""HLF1 copy of closure_2026_11_09/CO1_form_b_cosmology_computed/co1_linear.py (CO1 commit 020522140a lineage), unchanged except: input / output
file names carry the halo list HLF1_LIST=inherited|own (HLF1 FROZEN_CRITERIA 123947b9dc, A.3). Original docstring follows.
CO1 (FROZEN_CRITERIA.md 020522140a, AMENDMENT_A1 5e1496298d) part 2: the linear rows C1, C2, C3 and the lensing row C4.
  C1  F1A's stored B2 cold best fit replayed through F1A's own likelihood (read-only import); M3 = its stored baryons-only fit.
  C2  PR4 lensing bandpowers (cfg917_lib via QX3 iter2, read-only) against CLASS at the B2 best fit with its own A_s and tau.
  C3  DESI DR1 f sigma8 ratio rows (CE2's transcription) against f sigma8 of the B2 best fit.
  C4  the redistribution R_cold(k) of co1_hm.json on the PR4 amplitude and shape; M2 = a flat 1.10.

  nice -n 10 python3 co1_linear.py     -> co1_linear.json, co1_linear.out      (run co1_hm.py first)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.interpolate import RegularGridInterpolator
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LIST = os.environ.get("HLF1_LIST", "inherited")
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit"); I2D = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust")
sys.path.insert(0, F1AD); sys.path.insert(0, I2D)
import f1a                                                    # noqa: E402  F1A's likelihoods and CAMB call, read only
with contextlib.redirect_stdout(io.StringIO()):
    import iter2 as I2                                        # noqa: E402  loads the PR4 bandpowers through cfg917_lib
from classy import Class                                      # noqa: E402
LIB, DPR4, LMAX = I2.LIB, I2.D, I2.LMAX
FOOTS = ("canonical", "alt")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
HM = json.load(open(os.path.join(HERE, f"hlf1_hm_{LIST}.json"))); KH = np.array(HM["k"])
RES = dict(lane="CO1", part="linear rows and C4", criteria="020522140a", amendment_A1="5e1496298d",
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, C1={}, C2={}, C3={}, C4={}, MUTATE={"M2": {}, "M3": {}})
P("CO1 part 2: linear rows (C1 primary CMB re-run, C2 PR4 lensing, C3 DESI DR1 f sigma8) and C4 (the redistribution on PR4 lensing).")

def stored(foot, mode): return json.load(open(os.path.join(F1AD, "parts", f"fit_B2_{foot}_{mode}.json")))
CAL = json.load(open(os.path.join(F1AD, "parts", "cal.json")))["chi2_cal"]["PA"]

# ------------------------------------------------------------------ C1 and M3
P(f"\nC1 primary CMB: F1A's stored B2 best fits replayed (PR4 CamSpec cut + ACT DR6). chi2_cal (the likelihood package's test point, F1A cal.json) {CAL:.2f}")
ka6 = {}
for ft in FOOTS:
    row = {}
    for mode in ("cold", "MB"):
        st = stored(ft, mode); pr = st["pars"]; x0 = {k: np.array(v) for k, v in st["chi2"]["nuis"].items()}
        g = f1a.PA(f1a.camb_theory(**pr), x0)
        row[mode] = dict(PA=g["PA"], Pcut=g["Pcut"], A=g["A"], stored=st["chi2"]["PA"], d_stored=g["PA"] - st["chi2"]["PA"], Delta_cal=g["PA"] - CAL, pars=pr)
        P(f"  {ft:9s} {mode:4s}: PA chi2 {g['PA']:.3f} (stored {st['chi2']['PA']:.3f}, d {g['PA'] - st['chi2']['PA']:+.1e}); Delta_cal {g['PA'] - CAL:+.2f}   [{time.time() - T0:.0f} s]")
    c = row["cold"]; ka6[ft] = dict(d=c["d_stored"], pass_=bool(abs(c["d_stored"]) <= 0.1))
    RES["C1"][ft] = dict(PA=c["PA"], Delta_cal=c["Delta_cal"], line=9.0, status="PASS" if c["Delta_cal"] <= 9 else "FAIL", pars=c["pars"],
                         R_cold_to_baryon=c["pars"]["oc"] / c["pars"]["ob"], N_points=None)
    RES["MUTATE"]["M3"][ft] = dict(Delta_cal=row["MB"]["Delta_cal"], d_stored=row["MB"]["d_stored"], bites=bool(row["MB"]["Delta_cal"] > 25))
    P(f"  {ft:9s} C1 {RES['C1'][ft]['status']} (Delta_cal {c['Delta_cal']:+.2f} against <= 9); cold / baryon {c['pars']['oc'] / c['pars']['ob']:.3f}; "
      f"KA6 replay {'PASS' if ka6[ft]['pass_'] else 'FAIL'}; M3 baryons-only Delta_cal {row['MB']['Delta_cal']:+.1f} -> {'bites' if row['MB']['Delta_cal'] > 25 else 'DOES NOT BITE'}")
RES["KA"]["KA6"] = ka6

# ------------------------------------------------------------------ CLASS models
def class_B(pr):
    M = Class()
    M.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
           'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': 20.0})
    M.compute(); return M
def class_desi_fid():
    M = Class()
    M.set({'output': 'mPk', 'h': 0.6736, 'omega_b': 0.02237, 'omega_cdm': 0.1200, 'A_s': 2.083e-9, 'n_s': 0.9649, 'tau_reio': 0.0544, 'N_ur': 2.0328,
           'N_ncdm': 1, 'm_ncdm': 0.06, 'T_ncdm': 0.71611, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': 3.0})
    M.compute(); return M
def fs8(M, z, dz=0.005):
    """f sigma8 = d sigma8 / d ln a of the total-matter sigma8(z), R = 8 / h Mpc."""
    R8 = 8.0 / M.h(); return -(1 + z) * (M.sigma(R8, z + dz) - M.sigma(R8, max(z - dz, 0.0))) / (z + dz - max(z - dz, 0.0))
def amp_fit(X):
    u = LIB.wsum(DPR4["W"], X) + LIB.wsum(DPR4["M"], X)
    a = LIB.qform(u, DPR4["Cinv"], DPR4["d"] + DPR4["F"]); b = LIB.qform(u, DPR4["Cinv"]); A = a / b
    r = A * u - DPR4["F"] - DPR4["d"]
    return dict(A=A, sig=1.0 / math.sqrt(b), chi2_shape=LIB.qform(r, DPR4["Cinv"]), chi2_A1=LIB.pr4_chi2(DPR4, X))

# KA5: the record's reference row
M0 = I2.run_class(0.0215, 0.11958060485606123, 65.0, 0.95, pk=False); F0 = amp_fit(I2.X_of(M0)); M0.struct_cleanup()
ka5 = dict(chi2=F0["chi2_shape"], A=F0["A"], chi2_record=8.5708, A_record=1.0210287, pass_=bool(abs(F0["chi2_shape"] - 8.5708) <= 2e-3 and abs(F0["A"] - 1.0210287) <= 1e-5))
RES["KA"]["KA5"] = ka5
P(f"\nKA5 PR4 row of the record's reference X0: shape chi2 {F0['chi2_shape']:.4f} (8.5708), A {F0['A']:.7f} (1.0210287) -> {'PASS' if ka5['pass_'] else 'FAIL'}")

DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]   # CE2 ce2.py, copied
MF = class_desi_fid(); FID = {t: fs8(MF, z) for (t, z, *_) in DESI}; S8FID = MF.sigma8()
P(f"DESI fiducial (unit of the published ratios): sigma8 {S8FID:.4f}; f sigma8 at the four bins " + ", ".join(f"{t} {v:.4f}" for t, v in FID.items()))

ZSTAR = 1089.0
def limber_setup(M):
    CHIS = M.angular_distance(ZSTAR) * (1 + ZSTAR)
    zg = np.concatenate([np.linspace(1e-4, 6.5, 3251), np.geomspace(6.5, ZSTAR, 801)[1:-1], [ZSTAR * (1 - 1e-9)]])
    zg = np.unique(np.concatenate([zg, [s + e for s in (1.0, 3.0) for e in (-1e-7, 1e-7)]]))
    chi = np.array([M.angular_distance(z) * (1 + z) for z in zg])
    LG = np.unique(np.concatenate([np.round(np.geomspace(2, 2500, 400)).astype(int), [100, 200, 300, 400]])).astype(float)
    KT = np.geomspace(1e-5, 10.0, 320); ZT = np.unique(np.concatenate([np.linspace(0, 7, 141), np.linspace(7, 20, 53)]))
    LPT = np.log(np.array([[M.pk_lin(k, z) for z in ZT] for k in KT]))
    PINT = RegularGridInterpolator((np.log(KT), ZT), LPT, bounds_error=False, fill_value=None)
    D20 = M.scale_independent_growth_factor(20.0)
    def Pk(k, z):
        k = np.asarray(k, float); out = np.zeros_like(k); m = (k >= KT[0]) & (k <= KT[-1])
        if m.any():
            zz = min(z, 20.0); out[m] = np.exp(PINT(np.column_stack([np.log(k[m]), np.full(m.sum(), zz)])))
            if z > 20.0: out[m] *= (M.scale_independent_growth_factor(z) / D20) ** 2
        return out
    KER = ((1 + zg) * (CHIS - chi) / CHIS) ** 2
    KMAT_k = (LG[:, None] + 0.5) / chi[None, :]                # k in 1/Mpc at (L, z)
    PM = np.array([Pk((LG + 0.5) / c, z) for z, c in zip(zg, chi)]).T
    TW = np.zeros_like(chi); dchi = np.diff(chi); TW[:-1] += 0.5 * dchi; TW[1:] += 0.5 * dchi
    KMAT = PM * (KER * TW)[None, :]
    return dict(zg=zg, chi=chi, LG=LG, KMAT=KMAT, kmat=KMAT_k, DEN=KMAT.sum(axis=1), h=M.h(), H0c=M.Hubble(0.0), Om=M.Omega_m())
def S_of(LS, Rfun, zcut):
    """S(L) on 0..LMAX for a boost R(k [h/Mpc]) applied at z <= zcut."""
    Rm = np.where(LS["zg"][None, :] <= zcut, Rfun(LS["kmat"] / LS["h"]), 1.0)
    s = (LS["KMAT"] * Rm).sum(axis=1) / LS["DEN"]
    Lall = np.arange(LMAX + 1.0); S = np.ones(LMAX + 1); S[2:] = np.interp(np.log(Lall[2:]), np.log(LS["LG"]), s); return S
def Rinterp(Rk):
    lk = np.log(KH); R = np.asarray(Rk, float)
    return lambda kk: np.interp(np.log(np.clip(kk, KH[0], KH[-1])), lk, R)

for ft in FOOTS:
    pr = RES["C1"][ft]["pars"]; M = class_B(pr); X = I2.X_of(M); F = amp_fit(X); s8 = M.sigma8()
    ok2 = bool(F["chi2_shape"] <= 18.48 and abs(F["A"] - 1) <= 2 * F["sig"])
    RES["C2"][ft] = dict(A=F["A"], sigma_A=F["sig"], pull=(F["A"] - 1) / F["sig"], chi2_shape=F["chi2_shape"], chi2_at_A1=F["chi2_A1"], n_bandpowers=int(DPR4["n"]),
                         line_shape=18.48, status="PASS" if ok2 else "FAIL", A_s=math.exp(pr["lnA"]) * 1e-10, tau=pr["tau"], sigma8=s8)
    P(f"\n[{ft}] B2 best fit: h {pr['h']:.4f}, omega_b {pr['ob']:.5f}, omega_d {pr['oc']:.4f}, ln 1e10 A_s {pr['lnA']:.4f}, n_s {pr['ns']:.4f}, tau {pr['tau']:.4f}; sigma8 {s8:.4f}, "
      f"S8 {s8 * math.sqrt(M.Omega_m() / 0.3):.4f}, Omega_m {M.Omega_m():.4f}")
    P(f"  C2 PR4 lensing: A {F['A']:.4f} +- {F['sig']:.4f} ({(F['A'] - 1) / F['sig']:+.2f} sigma from the prediction; line 2); shape chi2 {F['chi2_shape']:.2f} (line 18.48, "
      f"{DPR4['n']} bandpowers); chi2 at A = 1 {F['chi2_A1']:.2f} -> {RES['C2'][ft]['status']}")
    # C3
    rows = []; c2 = [0.0, 0.0]; ok3 = True
    for (t, z, r1, p1, m1, r2, p2, m2) in DESI:
        fB = fs8(M, z); Rf = fB / FID[t]; e1 = 0.5 * (p1 + m1); e2 = 0.5 * (p2 + m2); q1 = (Rf - r1) / e1; q2 = (Rf - r2) / e2
        c2[0] += q1 * q1; c2[1] += q2 * q2; ok3 = ok3 and abs(q1) <= 2 and abs(q2) <= 2
        rows.append(dict(bin=t, z=z, fs8_B=fB, fs8_fid=FID[t], Rf=Rf, data_SF=r1 * FID[t], err_SF=e1 * FID[t], pull_SF=q1, data_SFB=r2 * FID[t], err_SFB=e2 * FID[t], pull_SFB=q2))
    RES["C3"][ft] = dict(rows=rows, chi2_SF=c2[0], chi2_SFB=c2[1], sigma8=s8, sigma8_engine=0.811, status="PASS" if ok3 else "FAIL")
    P("  C3 DESI DR1 f sigma8 (form B / measured +- err; pull): " + "; ".join(f"{r['bin']} z {r['z']}: {r['fs8_B']:.3f} / SF {r['data_SF']:.3f} +- {r['err_SF']:.3f} ({r['pull_SF']:+.2f}), "
      f"SF+BAO {r['data_SFB']:.3f} +- {r['err_SFB']:.3f} ({r['pull_SFB']:+.2f})" for r in rows))
    P(f"     chi2 over 4 bins: ShapeFit {c2[0]:.2f}, ShapeFit+BAO {c2[1]:.2f} -> {RES['C3'][ft]['status']}")
    # C4
    LS = limber_setup(M)
    kaL = dict(const=float(np.max(np.abs(S_of(LS, lambda kk: np.full_like(kk, 1.37), 1e9)[2:] / 1.37 - 1))))
    pref = (1.5 * LS["Om"] * LS["H0c"] ** 2) ** 2; CL = 4.0 / (LS["LG"] + 0.5) ** 4 * pref * LS["DEN"]; XA = dict(zip(LS["LG"].astype(int), (LS["LG"] * (LS["LG"] + 1)) ** 2 * CL / (2 * math.pi)))
    kaL["abs"] = {str(Lx): float(XA[Lx] / X[Lx] - 1) for Lx in (100, 200, 300, 400)}; kaL["pass_"] = bool(kaL["const"] <= 1e-10 and max(abs(v) for v in kaL["abs"].values()) <= 0.02)
    RES["KA"].setdefault("KA_limber", {})[ft] = kaL
    P(f"  Limber check: constant boost recovered to {kaL['const']:.1e}; absolute X_L against CLASS at L 100/200/300/400 " + "/".join(f"{v:+.4f}" for v in kaL["abs"].values())
      + f" -> {'PASS' if kaL['pass_'] else 'FAIL'}")
    def c4(Rk, zcut):
        S = S_of(LS, Rinterp(Rk), zcut); Fs = amp_fit(X * S)
        return dict(r_eff=F["A"] / Fs["A"], chi2_shape=Fs["chi2_shape"], S_at={str(Lx): float(S[Lx]) for Lx in (50, 100, 200, 400)})
    line = 2 * F["sig"] / F["A"]
    pri = c4(HM["primary"][ft]["R_cold"], 3.0); ok4 = bool(abs(pri["r_eff"] - 1) <= line and pri["chi2_shape"] <= 18.48)
    z1 = c4(HM["primary"][ft]["R_cold"], 1.0); tot = c4(HM["primary"][ft]["R_tot"], 3.0)
    br = {}
    for name, b in HM["brackets"][ft].items():
        br[name] = c4((np.array(b["R_tot"]) / np.array(b["R_bar"])).tolist(), 3.0)["r_eff"]
    m2 = c4(np.full_like(KH, 1.10).tolist(), 3.0)
    RES["C4"][ft] = dict(primary=pri, line=line, status="PASS" if ok4 else "FAIL", reported=dict(z_le_1=z1, R_tot_in_place_of_R_cold=tot, brackets_r_eff=br))
    RES["MUTATE"]["M2"][ft] = dict(r_eff=m2["r_eff"], line=line, bites=bool(abs(m2["r_eff"] - 1) > line))
    P(f"  C4 redistribution on PR4 lensing: S(L 50/100/200/400) " + "/".join(f"{v:.5f}" for v in pri["S_at"].values()) + f"; r_eff {pri['r_eff']:.5f} (|r_eff - 1| {abs(pri['r_eff'] - 1):.5f} "
      f"against {line:.4f}); shape chi2 {pri['chi2_shape']:.2f} -> {RES['C4'][ft]['status']}")
    P(f"     reported: applied at z <= 1 only r_eff {z1['r_eff']:.5f}; R_tot in place of R_cold {tot['r_eff']:.5f}; brackets |r_eff - 1| max "
      f"{max(abs(v - 1) for v in br.values()):.5f} ({max(br, key=lambda n: abs(br[n] - 1))}); M2 flat 1.10: r_eff {m2['r_eff']:.4f} -> {'bites' if RES['MUTATE']['M2'][ft]['bites'] else 'DOES NOT BITE'}")
    M.struct_cleanup()
MF.struct_cleanup()
RES["KA_ok"] = bool(all(v["pass_"] for v in ka6.values()) and ka5["pass_"] and all(v["pass_"] for v in RES["KA"]["KA_limber"].values()))
P(f"\nKnown answers of this part all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s, peak RSS {f1a.rss():.2f} GB)")
json.dump(RES, open(os.path.join(HERE, f"hlf1_linear_{LIST}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"hlf1_linear_{LIST}.out"), "w").write("\n".join(OUT) + "\n")
