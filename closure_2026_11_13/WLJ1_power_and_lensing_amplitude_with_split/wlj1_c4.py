#!/usr/bin/env python3
"""WLJ1 (FROZEN_CRITERIA.md, 03f9823de7) part 2: gate G-C4 (CO1 C4, the redistribution on PR4 CMB lensing) for REF, ADOPT and SPLIT.
CO1's co1_linear.py C4 pieces are COPIED (class_B, amp_fit, limber_setup, S_of, Rinterp, c4; source named): CLASS at CO1's stored C1
parameters (co1_linear.json), PR4 bandpowers through QX3 iter2 (imported read-only from its own folder, no bytecode).
Primary: each case's z = 0 R_cold held to z 3 (CO1's frozen convention). z bracket: each case's own R_cold(k, z) on z 0, 0.5, ..., 3,
linear in z between nodes, R = 1 above z 3. Reported: applied at z <= 1 only. Twins: TW-B (2 v*), TW-L (layout change doubled) ->
wlj1_c4_MUTATE.json.
  nice -n 10 python3 -I -B wlj1_c4.py   (after wlj1_hm.py)  -> wlj1_c4.json, wlj1_c4.out, wlj1_c4_MUTATE.json, wlj1_c4_MUTATE.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.interpolate import RegularGridInterpolator
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CO1D = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")
I2D = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust"); sys.path.insert(0, I2D)
with contextlib.redirect_stdout(io.StringIO()):
    import iter2 as I2                                        # noqa: E402  PR4 bandpowers through cfg917_lib, read only
from classy import Class                                      # noqa: E402
LIB, DPR4, LMAX = I2.LIB, I2.D, I2.LMAX
FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
HM = json.load(open(os.path.join(HERE, "wlj1_hm.json"))); MU = json.load(open(os.path.join(HERE, "wlj1_hm_MUTATE.json"))); KH = np.array(HM["k"])
LIN = json.load(open(os.path.join(CO1D, "co1_linear.json")))
ZN = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

# ------------------------------------------------------------------ copied from CO1's co1_linear.py
def class_B(pr):
    M = Class()
    M.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
           'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': 20.0})
    M.compute(); return M
def amp_fit(X):
    u = LIB.wsum(DPR4["W"], X) + LIB.wsum(DPR4["M"], X)
    a = LIB.qform(u, DPR4["Cinv"], DPR4["d"] + DPR4["F"]); b = LIB.qform(u, DPR4["Cinv"]); A = a / b
    r = A * u - DPR4["F"] - DPR4["d"]
    return dict(A=A, sig=1.0 / math.sqrt(b), chi2_shape=LIB.qform(r, DPR4["Cinv"]), chi2_A1=LIB.pr4_chi2(DPR4, X))
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
    KMAT_k = (LG[:, None] + 0.5) / chi[None, :]
    PM = np.array([Pk((LG + 0.5) / c, z) for z, c in zip(zg, chi)]).T
    TW = np.zeros_like(chi); dchi = np.diff(chi); TW[:-1] += 0.5 * dchi; TW[1:] += 0.5 * dchi
    KMAT = PM * (KER * TW)[None, :]
    return dict(zg=zg, chi=chi, LG=LG, KMAT=KMAT, kmat=KMAT_k, DEN=KMAT.sum(axis=1), h=M.h(), H0c=M.Hubble(0.0), Om=M.Omega_m())
def S_of(LS, Rfun, zcut):
    Rm = np.where(LS["zg"][None, :] <= zcut, Rfun(LS["kmat"] / LS["h"]), 1.0)
    s = (LS["KMAT"] * Rm).sum(axis=1) / LS["DEN"]
    Lall = np.arange(LMAX + 1.0); S = np.ones(LMAX + 1); S[2:] = np.interp(np.log(Lall[2:]), np.log(LS["LG"]), s); return S
def Rinterp(Rk):
    lk = np.log(KH); R = np.asarray(Rk, float)
    return lambda kk: np.interp(np.log(np.clip(kk, KH[0], KH[-1])), lk, R)
# ------------------------------------------------------------------ WLJ1: the z-dependent version of S_of (R(k, z) linear in z between nodes, 1 above z 3)
def S_of_z(LS, Rnodes):
    kk = LS["kmat"] / LS["h"]; zg = LS["zg"]; Rm = np.ones_like(kk)
    ev = [Rinterp(R)(kk) for R in Rnodes]
    for i in range(len(ZN) - 1):
        m = (zg >= ZN[i]) & (zg <= ZN[i + 1]) if i == 0 else (zg > ZN[i]) & (zg <= ZN[i + 1])
        w = (zg[m] - ZN[i]) / (ZN[i + 1] - ZN[i]); Rm[:, m] = ev[i][:, m] * (1 - w)[None, :] + ev[i + 1][:, m] * w[None, :]
    s = (LS["KMAT"] * Rm).sum(axis=1) / LS["DEN"]
    Lall = np.arange(LMAX + 1.0); S = np.ones(LMAX + 1); S[2:] = np.interp(np.log(Lall[2:]), np.log(LS["LG"]), s); return S

def Rc(case, ft, z, src=None):
    if case == "REF": return np.ones_like(KH)
    if case == "TWL":
        r = np.array(HM["cases"][f"S2|{ft}|{z}"]["R_cold"]); return 1 + 2 * (r - 1)
    if case == "TWB": return np.array(MU["TWB"][f"TWB|{ft}|{z}"]["R_cold"])
    return np.array(HM["cases"][f"{case}|{ft}|{z}"]["R_cold"])
CASES = ["REF", "ADOPT", "S1.25", "S2", "S3", "Sinf", "U1.25", "U2", "U3"]; TWINS = ["TWB", "TWL"]
RES = dict(lane="WLJ1", part="G-C4 PR4 lensing with the redistribution", criteria="03f9823de7", rows={}, KA={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
MUT = dict(lane="WLJ1", part="G-C4 twins", criteria="03f9823de7", rows={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P("WLJ1 part 2: G-C4 (CO1 C4) for REF, ADOPT and SPLIT. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
for ft in FOOTS:
    pr = LIN["C1"][ft]["pars"]; M = class_B(pr); X = I2.X_of(M); F = amp_fit(X); LS = limber_setup(M); line = 2 * F["sig"] / F["A"]
    def c4(S):
        Fs = amp_fit(X * S); return dict(r_eff=F["A"] / Fs["A"], chi2_shape=Fs["chi2_shape"], S_at={str(Lx): float(S[Lx]) for Lx in (50, 100, 200, 400)})
    for cs in CASES + TWINS:
        held = c4(S_of(LS, Rinterp(Rc(cs, ft, 0.0)), 3.0)); z1 = c4(S_of(LS, Rinterp(Rc(cs, ft, 0.0)), 1.0))
        zb = c4(S_of_z(LS, [Rc(cs, ft, z) for z in ZN])) if cs not in ("U1.25", "U2", "U3") else None
        row = dict(held=held, z_le_1=z1, z_bracket=zb, line=line,
                   status="PASS" if (abs(held["r_eff"] - 1) <= line and held["chi2_shape"] <= 18.48) else "FAIL",
                   status_z_bracket=(None if zb is None else ("PASS" if (abs(zb["r_eff"] - 1) <= line and zb["chi2_shape"] <= 18.48) else "FAIL")))
        (MUT if cs in TWINS else RES)["rows"][f"{cs}|{ft}"] = row
        P(f"  [{ft}] {cs:6s} r_eff - 1 held {held['r_eff'] - 1:+.2e} (shape chi2 {held['chi2_shape']:.4f}); z bracket "
          + (f"{zb['r_eff'] - 1:+.2e}" if zb else "-") + f"; z <= 1 {z1['r_eff'] - 1:+.2e}; line {line:.4f} -> {row['status']}   [{time.time() - T0:.0f} s]")
    for cs in ("ADOPT", "S1.25", "S2", "S3", "Sinf"):                     # HLF1 Part A: the own list (z = 0, held)
        held = c4(S_of(LS, Rinterp(HM["own"][f"{cs}|{ft}"]["R_cold"]), 3.0))
        RES["rows"][f"own:{cs}|{ft}"] = dict(held=held, line=line, status="PASS" if (abs(held["r_eff"] - 1) <= line and held["chi2_shape"] <= 18.48) else "FAIL")
        P(f"  [{ft}] own list {cs:6s} r_eff - 1 held {held['r_eff'] - 1:+.2e} -> {RES['rows'][f'own:{cs}|{ft}']['status']}")
    HO = json.load(open(os.path.join(REPO, "closure_2026_11_10", "HLF1_own_halo_list_forest", "hlf1_linear_own.json")))["C4"][ft]["primary"]
    ao = RES["rows"][f"own:ADOPT|{ft}"]["held"]
    RES["KA"][f"KA_G4_C4_{ft}"] = dict(r_eff=ao["r_eff"], stored=HO["r_eff"], pass_=bool(abs(ao["r_eff"] - HO["r_eff"]) <= 1e-6))
    P(f"  [{ft}] KA-G4 (C4 part) ADOPT own list r_eff {ao['r_eff']:.9f} (HLF1 {HO['r_eff']:.9f}) -> {'PASS' if RES['KA'][f'KA_G4_C4_{ft}']['pass_'] else 'FAIL'}")
    ref = LIN["C4"][ft]["primary"]; a = RES["rows"][f"ADOPT|{ft}"]["held"]
    RES["KA"][f"KA_G2_{ft}"] = dict(r_eff=a["r_eff"], stored=ref["r_eff"], chi2=a["chi2_shape"], stored_chi2=ref["chi2_shape"],
                                   pass_=bool(abs(a["r_eff"] - ref["r_eff"]) <= 1e-6 and abs(a["chi2_shape"] - ref["chi2_shape"]) <= 1e-3))
    r = RES["rows"][f"REF|{ft}"]["held"]; RES["KA"][f"KA_R_{ft}"] = dict(r_eff=r["r_eff"], pass_=bool(r["r_eff"] == 1.0))
    P(f"  [{ft}] KA-G2 ADOPT r_eff {a['r_eff']:.9f} (CO1 {ref['r_eff']:.9f}), shape {a['chi2_shape']:.5f} ({ref['chi2_shape']:.5f}) -> {'PASS' if RES['KA'][f'KA_G2_{ft}']['pass_'] else 'FAIL'}; "
      f"KA-R REF r_eff {r['r_eff']!r} -> {'PASS' if RES['KA'][f'KA_R_{ft}']['pass_'] else 'FAIL'}")
    M.struct_cleanup()
RES["KA_ok"] = bool(all(v["pass_"] for v in RES["KA"].values()))
P(f"\nKnown answers all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "wlj1_c4.json"), "w"), indent=1, default=float)
json.dump(MUT, open(os.path.join(HERE, "wlj1_c4_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "wlj1_c4.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
open(os.path.join(HERE, "wlj1_c4_MUTATE.out"), "w").write("\n".join(l for l in OUT if "TWB" in l or "TWL" in l) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
