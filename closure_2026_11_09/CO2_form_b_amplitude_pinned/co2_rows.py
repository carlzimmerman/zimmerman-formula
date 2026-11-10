#!/usr/bin/env python3
"""CO2 (FROZEN_CRITERIA.md 2bd776c60d) part 2: known answers of the low-L reader and rows P1, P2, P3 at the pinned fits.
  KA1  the transcribed low-L EE reader at the package's published test point (396.04).
  KA2  F1A's calibration cosmology replays chi2_cal; its chi2_E enters P1.
  P1   Delta_cal' = [PA + chi2_E](pinned) - [PA + chi2_E](calibration point), line <= 9.
  P2   PR4 lensing at the pinned fit (CO1's C2 code path).   P3   DESI DR1 f sigma8 (CO1's C3 code path).
  bracket: one 0.06 eV neutrino at the pinned parameters (sigma8 only; not a refit).

  nice -n 10 python3 co2_rows.py     -> co2_rows.json, co2_rows.out     (after co2_fit.py for both footings)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust"))
from co2_fit import chi2E, f1a                               # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import iter2 as I2                                        # noqa: E402  PR4 bandpowers through cfg917_lib
from classy import Class                                      # noqa: E402
import camb                                                   # noqa: E402
LIB, DPR4, LMAX = I2.LIB, I2.D, I2.LMAX
FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
FIT = {ft: json.load(open(os.path.join(HERE, "parts", f"fit_{ft}.json"))) for ft in FOOTS}
CO1 = json.load(open(os.path.join(HERE, "..", "CO1_form_b_cosmology_computed", "co1_linear.json")))
RES = dict(lane="CO2", part="KA1, KA2, P1, P2, P3", criteria="2bd776c60d", amendment_A1="b6dd6d0641", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, fit={}, P1={}, P2={}, P3={}, brackets={}, MUTATE={})
P("CO2 part 2: the pinned fits (Planck PR4 CamSpec cut + ACT DR6 + Planck 2018 low-L EE) and rows P1, P2, P3.")

# ------------------------------------------------------------------ KA1: the published test point of the low-L EE likelihood
p = camb.CAMBparams(); p.set_cosmology(ombh2=0.022383, omch2=0.12011, cosmomc_theta=1.040909e-2, tau=0.0543, mnu=0.06, num_massive_neutrinos=1, nnu=3.046, TCMB=2.7255)
p.InitPower.set_params(As=math.exp(3.0448) * 1e-10, ns=0.96605); p.set_for_lmax(2500, lens_potential_accuracy=1)
ee = camb.get_results(p).get_total_cls(100, CMB_unit="muK")[:, 1]
k1 = chi2E(ee, calib=1.00044); RES["KA"]["KA1"] = dict(chi2_E=k1, published=396.04, d=k1 - 396.04, pass_=bool(abs(k1 - 396.04) <= 0.3), chi2_E_calib_1=chi2E(ee))
P(f"KA1 low-L EE reader at the published test point: chi2_E {k1:.3f} (published 396.04; tolerance 0.3) -> {'PASS' if RES['KA']['KA1']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ the calibration point (F1A do_cal's cosmology)
p = camb.CAMBparams(); p.set_cosmology(ombh2=0.02235048, omch2=0.12121379, cosmomc_theta=1.04240171e-2, tau=0.05, mnu=0.06, num_massive_neutrinos=1, TCMB=f1a.TCMB)
p.InitPower.set_params(As=math.exp(3.04920413) * 1e-10, ns=0.96399503); p.set_for_lmax(f1a.LTH, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
cl = camb.get_results(p).get_total_cls(f1a.LTH, CMB_unit="muK"); Dc = {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}
gc = f1a.PA(Dc); Ecal = chi2E(Dc["ee"]); CAL = gc["PA"] + Ecal
RES["KA"]["KA2"] = dict(cal_PA=gc["PA"], stored=3805.3675775318825, d=gc["PA"] - 3805.3675775318825, cal_E=Ecal,
                        replay={ft: FIT[ft]["KA2"] for ft in FOOTS}, pass_=bool(abs(gc["PA"] - 3805.3675775318825) <= 0.1 and all(FIT[ft]["KA2"]["pass_"] for ft in FOOTS)))
RES["KA"]["KA3"] = {ft: dict(d=FIT[ft]["KA3"]["d"], tolerance=0.25, pass_=bool(abs(FIT[ft]["KA3"]["d"]) <= 0.25)) for ft in FOOTS}   # AMENDMENT A1 (b6dd6d0641)
P(f"KA2 calibration cosmology: PA {gc['PA']:.3f} (stored 3805.368), chi2_E {Ecal:.3f}; F1A's best fits replayed with the low-L term off: "
  + " / ".join(f"{FIT[ft]['KA2']['d']:+.1e}" for ft in FOOTS) + f" -> {'PASS' if RES['KA']['KA2']['pass_'] else 'FAIL'}")
P("KA3 interpolated minus exact chi2_E at the pinned fits: " + " / ".join(f"{FIT[ft]['KA3']['d']:+.4f}" for ft in FOOTS)
  + f" (tolerance 0.25, A1) -> {'PASS' if all(RES['KA']['KA3'][ft]['pass_'] for ft in FOOTS) else 'FAIL'}")

# ------------------------------------------------------------------ CLASS helpers (as co1_linear.py)
def class_B(pr, nu=False):
    M = Class()
    d = {'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
         'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': 20.0}
    if nu: d.update({'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.06, 'T_ncdm': 0.71611})
    M.set(d); M.compute(); return M
def class_desi_fid():
    M = Class()
    M.set({'output': 'mPk', 'h': 0.6736, 'omega_b': 0.02237, 'omega_cdm': 0.1200, 'A_s': 2.083e-9, 'n_s': 0.9649, 'tau_reio': 0.0544, 'N_ur': 2.0328,
           'N_ncdm': 1, 'm_ncdm': 0.06, 'T_ncdm': 0.71611, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': 3.0})
    M.compute(); return M
def fs8(M, z, dz=0.005):
    R8 = 8.0 / M.h(); return -(1 + z) * (M.sigma(R8, z + dz) - M.sigma(R8, max(z - dz, 0.0))) / (z + dz - max(z - dz, 0.0))
def amp_fit(X):
    u = LIB.wsum(DPR4["W"], X) + LIB.wsum(DPR4["M"], X)
    a = LIB.qform(u, DPR4["Cinv"], DPR4["d"] + DPR4["F"]); b = LIB.qform(u, DPR4["Cinv"]); A = a / b
    r = A * u - DPR4["F"] - DPR4["d"]
    return dict(A=A, sig=1.0 / math.sqrt(b), chi2_shape=LIB.qform(r, DPR4["Cinv"]), chi2_A1=LIB.pr4_chi2(DPR4, X))
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]   # CE2 ce2.py, copied (as CO1)
MF = class_desi_fid(); FID = {t: fs8(MF, z) for (t, z, *_) in DESI}; MF.struct_cleanup()

for ft in FOOTS:
    F = FIT[ft]; pr = F["pars"]; c = F["chi2"]; u = F["unpinned"]
    tot = c["PA"] + c["E_exact"]; dcal = tot - CAL
    RES["fit"][ft] = dict(pars=pr, tau=pr["tau"], tau_sigma_along_degeneracy=F["tau_width_along_degeneracy"]["sigma"], PA=c["PA"], E=c["E_exact"], total=tot, dPA=F["dPA"], dE=F["dE"],
                          unpinned=dict(tau=u["pars"]["tau"], lnA=u["pars"]["lnA"], PA=u["PA"], E=u["E_exact"]), per_start=F["per_start"], nfev=F["nfev"],
                          cold_to_baryon=pr["oc"] / pr["ob"])
    RES["P1"][ft] = dict(Delta_cal=dcal, cal_total=CAL, line=9.0, status="PASS" if dcal <= 9 else "FAIL", Delta_cal_PA_only=c["PA"] - gc["PA"], Delta_E_vs_cal=c["E_exact"] - Ecal)
    RES["MUTATE"].setdefault("M1", {})[ft] = F["M1"]
    P(f"\n[{ft}] pinned fit: tau {pr['tau']:.4f} +- {F['tau_width_along_degeneracy']['sigma']:.4f} (along the degeneracy; unpinned {u['pars']['tau']:.4f}), ln 1e10 A_s {pr['lnA']:.4f} "
      f"(unpinned {u['pars']['lnA']:.4f}), omega_b {pr['ob']:.5f}, omega_d {pr['oc']:.4f}, n_s {pr['ns']:.4f}, h {pr['h']:.4f}; cold / baryon {pr['oc'] / pr['ob']:.3f}")
    P(f"  chi2: PA {c['PA']:.2f} (unpinned {u['PA']:.2f}, {F['dPA']:+.2f}); low-L EE {c['E_exact']:.2f} (unpinned {u['E_exact']:.2f}, {F['dE']:+.2f}); starts: "
      + "; ".join(f"{s['start']} {s['fun']:.2f} at tau {s['x'][4]:.4f} ({s['nfev']} ev.)" for s in F["per_start"]))
    P(f"  P1 Delta_cal' {dcal:+.2f} (PA part {c['PA'] - gc['PA']:+.2f}, low-L part {c['E_exact'] - Ecal:+.2f}; line <= 9) -> {RES['P1'][ft]['status']};  "
      f"M1 tau 0.10: chi2_E +{F['M1']['rise']:.2f} -> {'bites' if F['M1']['bites'] else 'DOES NOT BITE'}")
    M = class_B(pr); X = I2.X_of(M); A = amp_fit(X); s8 = M.sigma8(); Om = M.Omega_m()
    ok2 = bool(A["chi2_shape"] <= 18.48 and abs(A["A"] - 1) <= 2 * A["sig"]); c1 = CO1["C2"][ft]
    RES["P2"][ft] = dict(A=A["A"], sigma_A=A["sig"], pull=(A["A"] - 1) / A["sig"], chi2_shape=A["chi2_shape"], chi2_at_A1=A["chi2_A1"], status="PASS" if ok2 else "FAIL",
                         sigma8=s8, S8=s8 * math.sqrt(Om / 0.3), Omega_m=Om, CO1_unpinned=dict(A=c1["A"], pull=c1["pull"], sigma8=c1["sigma8"], chi2_at_A1=c1["chi2_at_A1"]))
    P(f"  sigma8 {s8:.4f} (unpinned {c1['sigma8']:.4f}; S0 engine 0.811), S8 {s8 * math.sqrt(Om / 0.3):.4f}, Omega_m {Om:.4f}")
    P(f"  P2 PR4 lensing: A {A['A']:.4f} +- {A['sig']:.4f} ({(A['A'] - 1) / A['sig']:+.2f} sigma; unpinned {c1['pull']:+.2f}); shape chi2 {A['chi2_shape']:.2f}; chi2 at A = 1 {A['chi2_A1']:.2f} "
      f"(unpinned {c1['chi2_at_A1']:.2f}) -> {RES['P2'][ft]['status']}")
    rows = []; c2 = [0.0, 0.0]; ok3 = True
    for (t, z, r1, p1, m1, r2, p2, m2) in DESI:
        fB = fs8(M, z); Rf = fB / FID[t]; e1 = 0.5 * (p1 + m1); e2 = 0.5 * (p2 + m2); q1 = (Rf - r1) / e1; q2 = (Rf - r2) / e2
        c2[0] += q1 * q1; c2[1] += q2 * q2; ok3 = ok3 and abs(q1) <= 2 and abs(q2) <= 2; rows.append(dict(bin=t, z=z, fs8_B=fB, pull_SF=q1, pull_SFB=q2))
    RES["P3"][ft] = dict(rows=rows, chi2_SF=c2[0], chi2_SFB=c2[1], status="PASS" if ok3 else "FAIL")
    P(f"  P3 DESI DR1 f sigma8: " + ", ".join(f"{r['bin']} {r['fs8_B']:.3f} ({r['pull_SF']:+.2f} / {r['pull_SFB']:+.2f})" for r in rows)
      + f"; chi2 {c2[0]:.2f} / {c2[1]:.2f} -> {RES['P3'][ft]['status']}")
    M.struct_cleanup()
    Mn = class_B(pr, nu=True); s8n = Mn.sigma8(); An = amp_fit(I2.X_of(Mn)); Mn.struct_cleanup()
    RES["brackets"][ft] = dict(one_0p06eV_neutrino=dict(sigma8=s8n, lensing_A=An["A"], lensing_pull=(An["A"] - 1) / An["sig"], note="pinned parameters, not a refit"))
    P(f"  bracket, one 0.06 eV neutrino at the pinned parameters (not a refit): sigma8 {s8n:.4f}; PR4 lensing A {An['A']:.4f} ({(An['A'] - 1) / An['sig']:+.2f} sigma)")
RES["KA_ok"] = bool(RES["KA"]["KA1"]["pass_"] and RES["KA"]["KA2"]["pass_"] and all(RES["KA"]["KA3"][ft]["pass_"] for ft in FOOTS))
P(f"\nKnown answers of this part all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "co2_rows.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "co2_rows.out"), "w").write("\n".join(OUT) + "\n")
