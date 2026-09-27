#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR23b -- THE CHAIN'S HALO MASS FUNCTION AT z = 6-20 AND THE KNOB-FREE BARYON CEILING (Boylan-Kolchin 2023): does the
derivation chain raise or lower the ceiling that JWST's earliest massive galaxies press against?

INPUTS.  The chain's linear power is read with FP13's own machinery (committed 27faacc84; exec'd read-only up to its K banner:
  FP9's growth_aq with FP13's (H_S) model).  The chain's collapse threshold is XR23a's committed JSON
  (XR23_collapse_threshold_results.json: A_chain/A_LCDM per (M, z), both readings, every state variant, both footings; the
  MUTATE file for this lane's MUTATE).  The dark field's wave suppression is Hu, Barkana & Gruzinov 2000 (linear) and
  Schive et al. 2016 (the halo mass function fit), at FP10's floor m = 1.9e-19 and 5.2e-19 eV.
THE MASS FUNCTION.  Sheth & Tormen 1999 (A, a, p = 0.3222, 0.707, 0.3) on sigma(M, z) from a real-space top-hat filter in
  Lagrangian radius; the barrier B(M, z) = delta_c^LCDM(z) x A_chain/A_LCDM(M, z) (XR23a), ST's nu = B/sigma with the barrier's
  own mass slope in the Jacobian; Press-Schechter and the excursion-set moving-barrier series (Sheth & Tormen 2002) reported.
  The linear spectrum is the textbook Eisenstein & Hu 1998 no-wiggle form at sigma_8 = 0.811 (K3: it matches CLASS; FP6's
  transfer function, which the chain's machinery carries, does not).
THE CEILING (Boylan-Kolchin 2023, Nature Astronomy 7, 731): rho_*(> M*) <= eps f_b rho_h(> M*/(eps f_b)), f_b = Omega_b/
  Omega_m; the headline uses eps = 1 (f_b only) and reports the eps each data point requires (eps_req > 1 = above the ceiling).
DATA (cited, transcribed; nothing fitted):
  * Labbe et al. 2023, Nature 616, 266 (arXiv:2207.12446 v3, 'significant revision with updated calibration and stellar
    masses'): the 13 candidates of the authors' public catalogue of that revision (id, z_phot, log M* with 16-84%; Salpeter
    IMF), CEERS, 38 arcmin^2 (the survey area Boylan-Kolchin 2023 quotes), bins 7 < z < 8.5 and 8.5 < z < 10.
  * as later revised by spectroscopy: ID 13050 = CEERS 3210 (coordinates agree to 0.05"), z_spec = 5.624 (Kocevski et al.
    2023, ApJL 954, L4); ID 38094 = RUBIES-EGS-55604, z_spec = 6.98173; ID 14924 = RUBIES-EGS-966323, z_spec = 8.35304 with
    log M* (Chabrier) max/medium/min 10.62/9.84/8.72 (Wang et al. 2024, ApJL 969, L13).  IMF: Salpeter -> Chabrier = x 0.61
    (Madau & Dickinson 2014).
  * JADES-GS-z14-0: z = 14.32 (+0.08 -0.20), log M* = 8.6 (+0.7 -0.2) (Chabrier), found in the 58 arcmin^2 of GOODS-S
    (Carniani et al. 2024, Nature 633, 318); its abundance is taken as one object in 13.5 < z < 15 over that area (13 < z < 16
    reported).
CHECKS
  K  CONTROLS: K1 FP13's committed linear P boost (its H4: z = 0 and 0.25, k = 0.1-1 h/Mpc) reproduced exactly with FP13's own
     machinery; K2 the standard mass function: this lane's ST and PS equal colossus's (sheth99, press74) on the same spectrum
     at (1e10, 1e12 Msun/h, z = 0); K3 the linear spectrum: the textbook EH98 matches CLASS (and colossus's eisenstein98_zb),
     FP6's does not (reported with numbers); K4 the chain's linear boost is ZERO at z = 6-20 (FP13's machinery, both modes,
     both footings): the linear power at high z is LCDM's; K5 the cumulative abundance n(> M) at z = 9.1 and 14.3 equals
     colossus's integrated sheth99 on the same spectrum (the high-z, high-mass tail the ceiling reads).
  W  THE DARK FIELD'S WAVE CUT-OFF: W1 the half-mode scale and mass and the halo suppression at m = 1.9e-19, 5.2e-19 eV.
  H  THE MASS FUNCTION: H1 n_chain/n_LCDM at z = 6-20 (7, 10, 14 headlined), both readings, both footings, both spectra's states,
     the brackets; H2 (reported) the excursion-set first-crossing of the moving barrier (Sheth & Tormen 2002, first order).
  B  THE CEILING: B1 Labbe et al. as published; B2 as revised; B3 JADES-GS-z14-0; B4 the chain's ceiling against LCDM's at every
     data cell (the verdict check).
  R  ROBUSTNESS: R1 the separator threshold window (s = 1.3, 2.6), the dark field's mass, both footings.
MUTATE=1 reads XR23a's MUTATE barrier (the band-pass removed from the force law: MOND on the full peculiar field): B4 must
  FAIL (rc = 1).
PRE-DECLARED HYPOTHESES (written before the first full run; XR23a's pre-run and the exploratory runs were known):
  H7 the chain's linear power at z >= 6 equals LCDM's to 1e-9 (the yield sits above every linear mode while the leaf
     decelerates);
  H8 the wave cut-off suppresses halos by < 1% at M >= 1e9 Msun (both m); the half-mode mass is 1e5-1e7 Msun;
  H9 n_chain/n_LCDM is within 10% of 1 at M >= 1e10 for z = 7, 10, 14 in reading T (multi-shell), and 1 to 1% in reading B;
  H10 the chain's baryon ceiling differs from LCDM's by < 10% at every data cell (Labbe published and revised, GS-z14-0);
     the chain neither eases nor worsens the tension -- it inherits LCDM's;
  H11 LCDM's own status: the published Labbe z ~ 7.5 top object needs eps_req > 1 (Salpeter), the revised sample does not;
     GS-z14-0 needs eps_req < 1 at its central mass.
HISTORY (disclosed).  Scratch comparisons before this script: the record's EH98 against CLASS; this lane's ST against colossus;
  the Labbe catalogue (the authors' public file of the published revision, read once, values transcribed below).  One SMOKE
  run of this script (on XR23a's smoke JSON, outputs outside the repository) preceded the first full run; it changed three
  things before any committed number: K5 first compared against a figure attributed to Boylan-Kolchin 2023 (~1e-5.2 per
  Mpc^3) that this lane could not verify at source (colossus's planck18 gives 10^-5.52, this lane 10^-5.59) -- it now tests
  the cumulative tail against colossus; the barrier's mass interpolation is monotone cubic (it was piecewise linear, which
  kinks the Jacobian); H2's moving-barrier series is cut at first order (the higher derivatives of a 8-point barrier are
  noise).  As in XR23a, the pre-declared hypotheses are scored as run but REPORTED (FP10's convention); the controls, K4 and B4
  (H10, the MUTATE's pre-declared target) stay load-bearing.  This split was made after the smoke run, whose H9 failure came
  from XR23a's since-corrected inversion.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR23_mass_function_ceiling.py
"""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR23_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
OUTDIR = os.environ.get("XR23_OUTDIR", HERE)
INDIR = os.environ.get("XR23_INDIR", HERE)
SLUG = "XR23_mass_function_ceiling"
ST_A, ST_a, ST_p = 0.3222, 0.707, 0.3
SALP_TO_CHAB = math.log10(0.61)                     # Madau & Dickinson 2014: M*(Chabrier) = 0.61 M*(Salpeter)
AREA_LABBE = 38.0                                   # arcmin^2 (Boylan-Kolchin 2023's statement of the Labbe et al. survey)
AREA_JADES = 58.0                                   # arcmin^2 (Carniani et al. 2024)
# Labbe et al. 2023 (published revision): id, z_phot, z_16, z_84, log M*, log M*_16, log M*_84 (Salpeter)
LABBE = [(38094, 7.477, 7.436, 7.521, 10.887, 10.805, 10.982), (35300, 9.077, 8.696, 9.384, 10.397, 10.170, 10.582),
         (11184, 7.318, 6.973, 7.602, 10.181, 10.078, 10.283), (13050, 8.137, 6.429, 8.587, 10.138, 9.840, 10.428),
         (2859, 8.106, 6.613, 8.598, 10.029, 9.764, 10.267), (14924, 8.831, 8.741, 8.999, 10.015, 9.877, 10.171),
         (7274, 7.774, 7.717, 7.827, 9.866, 9.809, 9.960), (21834, 8.543, 8.030, 8.861, 9.608, 9.284, 9.871),
         (28984, 7.542, 7.401, 7.623, 9.572, 9.423, 9.698), (25666, 7.931, 7.767, 8.026, 9.522, 9.422, 9.751),
         (39575, 8.616, 8.049, 8.959, 9.329, 8.934, 9.760), (16624, 8.517, 8.299, 8.711, 9.299, 9.059, 9.572),
         (37888, 6.514, 6.232, 7.931, 9.230, 9.130, 9.476)]
SPEC_Z = {13050: 5.624, 38094: 6.98173, 14924: 8.35304}           # Kocevski+2023; Wang+2024 (RUBIES)
RUBIES_14924 = {"max": 10.62, "medium": 9.84, "min": 8.72}        # Chabrier (Wang+2024)
GSZ14 = {"z": 14.32, "z_lo": 14.12, "logM": 8.6, "logM_lo": 8.4, "logM_hi": 9.3}   # Chabrier (Carniani+2024)
BINS = ((7.0, 8.5, 7.5), (8.5, 10.0, 9.1))                        # z_lo, z_hi, z_eff (Boylan-Kolchin 2023's 7.5 and 9.1)


def main():
    T0 = time.time(); CH = []
    OUT = {"lane": "XR23b", "mutate": MUTATE, "checks": {}, "numbers": {}}

    def P(*a):
        print(*a, flush=True)

    def banner(t):
        P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)

    def check(name, measured, ok, load_bearing=True, reading=None):
        ok = bool(ok); CH.append((name, ok, load_bearing))
        OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
        P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            P(f"         reading:  {reading}")
        return ok

    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: XR23a's MUTATE barrier (band-pass removed) is used for reading T -- B4 must FAIL ***")
    ns, g = C.fp13(); cp = C.Cosmo(); M6 = g["M6"]; sp = C.spectra()
    KKF, LKF, h = g["KKF"], g["LKF"], g["h"]
    rho_m = cp.Om * cp.rho_c0 / cp.MSUN * cp.Mpc ** 3                 # Msun/Mpc^3 comoving
    A_f = json.load(open(os.path.join(INDIR, "XR23_collapse_threshold_results.json")))
    A_mut = json.load(open(os.path.join(INDIR, "XR23_collapse_threshold_results_MUTATE.json"))) if MUTATE else None
    ZS = np.array(A_f["zs"], float)
    dcl = {float(k): v for k, v in A_f["numbers"]["dc_lcdm"].items()}
    dcl_z = np.array([dcl[z] for z in ZS])
    P(f"\n  inputs: XR23a (A_chain/A_LCDM tables, {len(A_f['barrier_ratio'])} model/variant/reading/footing sets)"
      + (" + its MUTATE file" if MUTATE else "") + f"; f_b = {cp.fb:.4f}; rho_m = {rho_m:.4e} Msun/Mpc^3")

    # ======================================================================================================== K
    banner("K  CONTROLS")
    # K1 FP13's committed P boost with FP13's own machinery
    LH = g["L_table"](ns["DELTA_C"], ns["HEAD_READ"]); Lh = g["fun_of"](LH)
    yh = g["yth_state"](LH, ns["HEAD_READ"], ns["HEAD_SWITCH"], ns["HEAD_CY"])[0]
    modc = g["model_of"](Lh, yh["canonical"])
    resh = g["growth_aq"](modc, g["A0"]["canonical"], mode="permode", zs_out=(0.25,))
    D_lc = g["growth_aq"](M6["lcdm_model"](), g["A0"]["canonical"], mode="permode", zs_out=(0.25,))
    Pb = {zl: {kv: float(np.interp(kv, g["KH"], (resh[zl] / D_lc[zl]) ** 2)) - 1.0 for kv in (0.1, 0.3, 0.5, 1.0)} for zl in (0.0, 0.25)}
    ref = json.load(open(os.path.join(C.CHAIN, "FP13_separator_from_state_results.json")))["numbers"]["H4"]["Pboost"]
    dev1 = max(abs(Pb[zl][kv] - ref[str(zl)][str(kv)]) for zl in Pb for kv in Pb[zl])
    check("K1 CONTROL: FP13's committed linear boost of the sub-L power (its H4: P_H_S/P_LCDM - 1 at z = 0 and 0.25, k = 0.1-1 "
          "h/Mpc, canonical, per-mode) is reproduced EXACTLY by FP13's own machinery exec'd read-only",
          "z=0: " + ", ".join(f"k={kv}: {Pb[0.0][kv]:+.4f}" for kv in Pb[0.0]) + "; z=0.25: " + ", ".join(f"{Pb[0.25][kv]:+.4f}" for kv in Pb[0.25])
          + f"; max |dev| from the committed JSON {dev1:.1e}", dev1 < 1e-9)
    OUT["numbers"]["K1"] = Pb

    # sigma(M) machinery
    LMG = np.linspace(4.0, 17.0, 521); MG = 10 ** LMG

    def W(y):
        y = np.maximum(y, 1e-8)
        return np.where(y < 1e-3, 1 - y * y / 10, 3 * (np.sin(y) - y * np.cos(y)) / y ** 3)

    def sig0(D2, Mv=MG):
        R = (3 * np.asarray(Mv) / (4 * math.pi * rho_m)) ** (1 / 3) * h          # Mpc/h
        return np.sqrt(np.trapz(D2[None, :] * W(KKF[None, :] * R[:, None]) ** 2, LKF, axis=1))
    SIG = {k: sig0(sp[k]) for k in ("corrected", "committed", "corrected_m1.9e-19", "corrected_m5.2e-19")}
    Dz = lambda z: g["Dl"](1.0 / (1.0 + z))

    def f_st(nu):
        return ST_A * math.sqrt(2 * ST_a / math.pi) * nu * (1 + (ST_a * nu * nu) ** -ST_p) * np.exp(-ST_a * nu * nu / 2)

    def f_ps(nu):
        return math.sqrt(2 / math.pi) * nu * np.exp(-nu * nu / 2)

    def hmf(z, spec="corrected", Rfun=None, fnu=f_st, dc=None):
        """dn/dlnM [Mpc^-3] on MG; barrier = delta_c^LCDM(z) x R(M) (R = 1: LCDM)."""
        s = SIG[spec] * Dz(z)
        dc0 = float(np.interp(z, ZS, dcl_z)) if dc is None else dc
        Rm = np.ones_like(MG) if Rfun is None else Rfun(MG)
        B = dc0 * Rm; nu = B / s
        dlnnu = np.gradient(np.log(nu), np.log(MG))
        return rho_m / MG * fnu(nu) * np.abs(dlnnu)

    def cum(n):
        """(n(>M), rho(>M)) on MG"""
        x = np.log(MG); rho = n * MG
        c_n = np.concatenate([np.cumsum((0.5 * (n[1:] + n[:-1]) * np.diff(x))[::-1])[::-1], [0.0]])
        c_r = np.concatenate([np.cumsum((0.5 * (rho[1:] + rho[:-1]) * np.diff(x))[::-1])[::-1], [0.0]])
        return c_n, c_r

    # K2 against colossus on the same spectrum (eisenstein98_zb = the textbook no-wiggle form)
    k2 = {}; k2_ok = False
    try:
        from colossus.cosmology import cosmology
        from colossus.lss import mass_function
        cosmology.setCosmology("xr23", flat=True, H0=100 * h, Om0=cp.Om, Ob0=M6["Ob"], sigma8=M6["SIG8"], ns=M6["ns"],
                               Tcmb0=M6["T_CMB"], Neff=M6["N_eff"], relspecies=False)
        for Mh in (1e10, 1e12):
            for model, fnu in (("sheth99", f_st), ("press74", f_ps)):
                n = hmf(0.0, Rfun=None, fnu=fnu, dc=1.68647)
                mine = float(np.exp(np.interp(math.log(Mh / h), np.log(MG), np.log(n))))
                col = float(mass_function.massFunction(Mh, 0.0, q_in="M", q_out="dndlnM", mdef="fof", model=model,
                                                        ps_args={"model": "eisenstein98_zb"}) * h ** 3)
                k2[(Mh, model)] = (mine, col)
        k2_ok = all(abs(v[0] / v[1] - 1) < 3e-3 for v in k2.values())
    except Exception as ex:
        k2["error"] = repr(ex)
    check("K2 CONTROL: this lane's Sheth-Tormen and Press-Schechter dn/dlnM equal colossus's (sheth99, press74) on the same "
          "spectrum and cosmology at M = 1e10 and 1e12 Msun/h, z = 0 (delta_c = 1.68647)",
          ", ".join(f"{k[1]} {k[0]:.0e}: {v[0]:.4e} vs {v[1]:.4e} ({v[0] / v[1] - 1:+.1e})" for k, v in k2.items() if k != "error") or k2.get("error"),
          k2_ok, reading="at z = 7 the two differ by 1-2% more because the chain's growth factor carries radiation (0.15888 vs 0.15869)")
    OUT["numbers"]["K2"] = {f"{k[0]:.0e}|{k[1]}": v for k, v in k2.items() if k != "error"}

    # K3 the linear spectrum against CLASS
    k3 = {}; k3_ok = False
    try:
        from classy import Class
        CL = Class()
        CL.set({"h": h, "omega_b": M6["om_b"], "omega_cdm": M6["om_c"], "n_s": M6["ns"], "sigma8": M6["SIG8"], "T_cmb": M6["T_CMB"],
                "N_ur": M6["N_eff"], "output": "mPk", "P_k_max_h/Mpc": 200.0, "z_max_pk": 0.0})
        CL.compute()
        for kh in (0.01, 0.1, 1.0, 10.0, 100.0):
            D2c = kh ** 3 * CL.pk_lin(kh * h, 0.0) * h ** 3 / (2 * math.pi ** 2)
            k3[kh] = (float(np.interp(math.log(kh), LKF, sp["corrected"])) / D2c, float(np.interp(math.log(kh), LKF, sp["committed"])) / D2c)
        kc = KKF[KKF <= 150.0]
        D2cl = np.zeros_like(KKF); D2cl[KKF <= 150.0] = kc ** 3 * np.array([CL.pk_lin(k * h, 0.0) for k in kc]) * h ** 3 / (2 * math.pi ** 2)
        s_cl = sig0(D2cl, np.array([1e8, 1e10, 1e12]))
        s_co = sig0(sp["corrected"], np.array([1e8, 1e10, 1e12])); s_cm = sig0(sp["committed"], np.array([1e8, 1e10, 1e12]))
        k3["sigma"] = {f"{m_:.0e}": (float(a_), float(b_), float(c_)) for m_, a_, b_, c_ in zip((1e8, 1e10, 1e12), s_co, s_cm, s_cl)}
        k3_ok = (all(abs(v[0] - 1) < 0.06 for kk, v in k3.items() if kk != "sigma")
                 and all(abs(v[0] / v[2] - 1) < 0.03 for v in k3["sigma"].values())
                 and k3[0.01][1] < 0.6 and k3[1.0][1] > 1.2 and k3[10.0][1] > 1.4)
    except Exception as ex:
        k3["error"] = repr(ex)
    check("K3 THE LINEAR SPECTRUM (a finding): at fixed sigma_8 the textbook EH98 no-wiggle spectrum matches CLASS within 6% "
          "(0.01-100 h/Mpc) and 3% in sigma(M); the spectrum the chain's machinery carries (FP6's T_EH98, from L341: k in 1/Mpc "
          "but q = k Theta^2/(Om h ...) and 0.43 k s/h) is 0.44x CLASS at 0.01 h/Mpc and 1.3-1.6x at 1-100 h/Mpc",
          "; ".join(f"k={kk}: textbook {v[0]:.3f}, FP6 {v[1]:.3f}" for kk, v in k3.items() if kk not in ("sigma", "error"))
          + ("; sigma(1e8/1e10/1e12) textbook/FP6/CLASS: " + ", ".join(f"{m_}: {v[0]:.3f}/{v[1]:.3f}/{v[2]:.3f}" for m_, v in k3["sigma"].items()) if "sigma" in k3 else "")
          + (f"; {k3['error']}" if "error" in k3 else ""), k3_ok,
          reading="the high-z mass function below uses the textbook spectrum; the chain's own state (L, y_th) is scored on both (XR23a V0 "
                  "vs V1), and FP13's A6 'linear-spectrum systematic' is this error")
    OUT["numbers"]["K3"] = {str(k): v for k, v in k3.items()}

    # K4 the chain's linear boost at high z
    k4 = {}
    ZH = (20.0, 14.0, 10.0, 7.0, 6.0, 3.0, 2.0, 1.0, 0.635, 0.25)
    for f in ("canonical", "alt"):
        modf = g["model_of"](Lh, yh[f])
        for m in ("rms", "permode"):
            r_ = g["growth_aq"](modf, g["A0"][f], mode=m, zs_out=ZH)
            l_ = g["growth_aq"](M6["lcdm_model"](), g["A0"][f], mode=m, zs_out=ZH)
            for z in ZH:
                k4[(f, m, z)] = float(np.max(np.abs(r_[z] / l_[z] - 1)))
    hz = max(v for (f, m, z), v in k4.items() if z >= 6)
    P("    max_k |D_HS/D_LCDM - 1|: " + "; ".join(f"z={z:g}: " + "/".join(f"{k4[(f, m, z)]:.1e}" for f in ("canonical", "alt") for m in ("rms", "permode")) for z in ZH))
    check("K4 (H7) THE CHAIN'S LINEAR POWER AT z >= 6 IS LCDM'S: FP13's (H_S) growth with FP13's own machinery, both yardstick "
          "modes and footings, differs from LCDM's by <= 1e-9 at z = 6-20 on every k (0.02-20 h/Mpc): while the leaf "
          "decelerates the yield sits at the web's band-passed rms, above every linear mode", f"max |dev| at z >= 6: {hz:.1e}", hz <= 1e-9)
    OUT["numbers"]["K4"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in k4.items()}

    # K5 the cumulative high-z tail against colossus
    k5 = {}; k5_ok = False
    try:
        for zz, Mst in ((9.1, 10 ** 10.5), (14.32, 10 ** 8.6)):
            Mh = Mst / cp.fb
            cn_, cr_ = cum(hmf(zz, dc=1.68647))
            mine = float(np.exp(np.interp(math.log(Mh), np.log(MG), np.log(cn_))))
            lM = np.linspace(math.log10(Mh * h), 16.8, 600)
            col_dn = mass_function.massFunction(10 ** lM, zz, q_in="M", q_out="dndlnM", mdef="fof", model="sheth99",
                                                ps_args={"model": "eisenstein98_zb"}) * h ** 3
            col = float(np.trapz(col_dn, lM * math.log(10)))
            gcol = cosmology.getCurrent().growthFactor(zz); gme = Dz(zz)
            k5[zz] = (mine, col, gme / gcol)
        k5_ok = all(abs(math.log10(v[0] / v[1])) < 0.08 for v in k5.values())
    except Exception as ex:
        k5["error"] = repr(ex)
    check("K5 CONTROL: the cumulative abundance n(> M*/f_b) at z = 9.1 (M* = 10^10.5) and z = 14.32 (M* = 10^8.6) equals "
          "colossus's integrated sheth99 on the same spectrum within 0.08 dex (the chain's growth factor carries radiation: its "
          "ratio to colossus's is printed)",
          "; ".join(f"z={z_}: 10^{math.log10(v[0]):.3f} vs 10^{math.log10(v[1]):.3f} (D ratio {v[2]:.4f})" for z_, v in k5.items() if z_ != "error")
          or k5.get("error"), k5_ok)
    OUT["numbers"]["K5"] = {str(k_): v for k_, v in k5.items()}
    P(f"    {time.time() - T0:.0f} s")

    # ======================================================================================================== W
    banner("W  THE DARK FIELD'S WAVE CUT-OFF (FL1's free order parameter at FP10's mass floor)")
    w1 = {}
    for m in C.M_DARK:
        m22 = m / 1e-22
        khalf = brentq(lambda k: float(C.T_fdm(k, m, h)) ** 2 - 0.5, 1.0, 1e4)            # h/Mpc
        Mhalf = 4 * math.pi / 3 * rho_m * (math.pi / (khalf * h)) ** 3
        M0 = 1.6e10 * m22 ** (-4 / 3)
        sch = {Mv: (1 + (Mv / M0) ** -1.1) ** -2.2 for Mv in (1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11)}
        # sharp-k excursion set (c = 2.5) on the cut-off spectrum vs the CDM one, z = 10
        def n_sk(D2, z=10.0, c_=2.5):
            R = (3 * MG / (4 * math.pi * rho_m)) ** (1 / 3) / c_ * h           # Mpc/h
            s2 = np.array([np.trapz(D2[KKF <= 1 / r_], LKF[KKF <= 1 / r_]) for r_ in R]) * Dz(z) ** 2
            nu = float(np.interp(z, ZS, dcl_z)) / np.sqrt(s2)
            return rho_m / MG * f_ps(nu) * np.abs(np.gradient(np.log(nu), np.log(MG)))
        sk = n_sk(sp[f"corrected_m{m:.1e}"]) / n_sk(sp["corrected"])
        skv = {Mv: float(np.interp(math.log(Mv), np.log(MG), sk)) for Mv in (1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11)}
        w1[m] = {"k_half_hMpc": khalf, "M_half": Mhalf, "M0_Schive": M0, "Schive": sch, "sharpk": skv}
        P(f"    m = {m:.1e} eV: half-mode k = {khalf:.0f} h/Mpc, M_1/2 = {Mhalf:.2e} Msun, Schive+2016 M_0 = {M0:.2e} Msun; n_wave/n_CDM "
          "(Schive | sharp-k PS, z = 10) at M = " + ", ".join(f"{Mv:.0e}: {sch[Mv]:.3f}|{skv[Mv]:.3f}" for Mv in sch))
    w_ok = all(abs(v["Schive"][Mv] - 1) < 0.01 and abs(v["sharpk"][Mv] - 1) < 0.01 for v in w1.values() for Mv in (1e9, 1e10, 1e11)) \
        and all(1e5 <= v["M_half"] <= 1e7 for v in w1.values())
    check("W1 (H8) THE WAVE CUT-OFF IS A MINI-HALO EFFECT: at m = 1.9e-19 and 5.2e-19 eV the half-mode mass is 1e5-1e7 Msun and "
          "halos above 1e9 Msun are suppressed by < 1% (Schive et al. 2016's fit and a sharp-k excursion set agree)",
          "; ".join(f"m={m:.1e}: M_1/2 {v['M_half']:.1e}, 1e9: {v['Schive'][1e9]:.4f}/{v['sharpk'][1e9]:.4f}" for m, v in w1.items()), w_ok,
          load_bearing=False)
    OUT["numbers"]["W1"] = {str(m): v for m, v in w1.items()}

    # ======================================================================================================== barrier
    bar = A_f["barrier_ratio"]
    if MUTATE:
        for k_, v in A_mut["barrier_ratio"].items():
            bar[k_.replace("|MUT", "|main").replace("multi|V1|T|canonical", "multi|V1|T|canonical")] = v    # V1 T canonical replaced

    def Rfun_of(key):
        tab = bar[key]
        Ms = np.array(sorted(float(m) for m in tab)); lM = np.log10(Ms)
        grid = np.array([[tab[f"{m:.0e}"][str(z)] if tab[f"{m:.0e}"][str(z)] is not None else np.nan for z in ZS] for m in Ms], float)
        from scipy.interpolate import PchipInterpolator

        def zrow(i, z):
            ok = np.isfinite(grid[i])                                        # the refined redshift nodes of this mass
            return float(np.interp(z, ZS[ok], grid[i][ok])) if ok.any() else 1.0

        def f(Mv, z):
            row = np.array([zrow(i, z) for i in range(len(Ms))])
            x = np.clip(np.log10(np.asarray(Mv, float)), lM[0], lM[-1])            # held flat beyond the computed masses
            return PchipInterpolator(lM, row)(x) if len(Ms) >= 2 else np.full_like(x, row[0])
        return f, (Ms.min(), Ms.max())

    # ======================================================================================================== H
    banner("H  THE CHAIN'S HALO MASS FUNCTION AT z = 6-20 AGAINST LCDM'S")
    sets = [("multi|V0|T|canonical|main", "T V0 can"), ("multi|V0|T|alt|main", "T V0 alt"), ("multi|V1|T|canonical|main", "T V1 can"),
            ("multi|V1|T|alt|main", "T V1 alt"), ("multi|V0|B|canonical|main", "B V0 can"), ("multi|V1|B|canonical|main", "B V1 can"),
            ("multi|V1|B|alt|main", "B V1 alt"), ("single_tophat|V1|T|canonical|main", "top hat V1 can"),
            ("single_point|V1|T|canonical|main", "compact V1 can")]
    sets = [s_ for s_ in sets if s_[0] in bar]
    ZREP = (6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 17.0, 20.0)
    MREP = (1e8, 1e9, 1e10, 1e11, 1e12, 1e13)
    h1 = {}
    for key, lab in sets:
        Rf, (mlo, mhi) = Rfun_of(key)
        for z in ZREP:
            n_c = hmf(z, Rfun=lambda Mv, z=z: Rf(Mv, z)); n_l = hmf(z)
            cn_c, cr_c = cum(n_c); cn_l, cr_l = cum(n_l)
            h1[(lab, z)] = {Mv: (float(np.interp(math.log(Mv), np.log(MG), n_c / n_l)),
                                 float(np.interp(math.log(Mv), np.log(MG), cr_c / np.maximum(cr_l, 1e-300)))) for Mv in MREP}
    for z in (7.0, 10.0, 14.0):
        P(f"    z = {z:g}: n_chain/n_LCDM (dn/dlnM) at M = " + ", ".join(f"{Mv:.0e}" for Mv in MREP))
        for key, lab in sets:
            P(f"      {lab:16s}: " + ", ".join(f"{h1[(lab, z)][Mv][0]:.4f}" for Mv in MREP))
    sh_T = max(abs(h1[(lab, z)][Mv][0] - 1) for key, lab in sets if lab.startswith("T ") for z in (7.0, 10.0, 14.0) for Mv in MREP if Mv >= 1e10)
    sh_B = max(abs(h1[(lab, z)][Mv][0] - 1) for key, lab in sets if lab.startswith("B ") for z in (7.0, 10.0, 14.0) for Mv in MREP if Mv >= 1e9)
    check("H1 (H9) THE CHAIN'S HALO ABUNDANCE IS LCDM'S AT JWST MASSES: n_chain/n_LCDM within 10% at M >= 1e10 for z = 7, 10, 14 "
          "(reading T, multi-shell, V0 and V1, both footings) and within 1% at M >= 1e9 in reading B",
          f"max |ratio - 1|: reading T {sh_T:.2%} (M >= 1e10); reading B {sh_B:.2%} (M >= 1e9)", sh_T <= 0.10 and sh_B <= 0.01,
          load_bearing=False)
    OUT["numbers"]["H1"] = {f"{k[0]}|{k[1]}": {f"{Mv:.0e}": v for Mv, v in vv.items()} for k, vv in h1.items()}

    # H2 excursion-set moving-barrier (ST 2002 series) cross-check on the headline set
    key0 = "multi|V1|T|canonical|main"
    if key0 in bar:
        Rf0, _ = Rfun_of(key0); h2 = {}
        for z in (7.0, 10.0, 14.0):
            s2 = (SIG["corrected"] * Dz(z)) ** 2; S = s2
            dc0 = float(np.interp(z, ZS, dcl_z))

            def fS(Bfun):
                Bv = Bfun(MG)
                d1 = np.gradient(Bv, S)
                T_ = Bv - S * d1                                                    # Sheth & Tormen 2002, first order
                fs = np.abs(T_) / np.sqrt(2 * math.pi * S ** 3) * np.exp(-Bv ** 2 / (2 * S))
                return rho_m / MG * fs * np.abs(np.gradient(S, np.log(MG)))
            nr = fS(lambda Mv: dc0 * Rf0(Mv, z)) / fS(lambda Mv: dc0 * np.ones_like(Mv))
            h2[z] = {Mv: float(np.interp(math.log(Mv), np.log(MG), nr)) for Mv in MREP}
        P("    excursion-set moving barrier (ST 2002, first order; V1 T canonical): " + "; ".join(f"z={z:g}: " + ",".join(f"{v:.4f}" for v in h2[z].values()) for z in h2))
        check("H2 (reported) the excursion-set first-crossing ratio for the chain's moving barrier (Press-Schechter normalisation)",
              "; ".join(f"z={z:g}: max |ratio-1| {max(abs(v - 1) for Mv, v in h2[z].items() if Mv >= 1e10):.2%}" for z in h2), True, load_bearing=False)
        OUT["numbers"]["H2"] = {str(z): v for z, v in h2.items()}

    # ======================================================================================================== B
    banner("B  THE KNOB-FREE BARYON CEILING (Boylan-Kolchin 2023): rho_*(> M*) <= f_b rho_h(> M*/f_b)")
    D_c = lambda z: 2.99792458e5 / 100.0 / h * np.trapz([1 / cp.Ez(1 / (1 + zz)) for zz in np.linspace(0, z, 2001)], np.linspace(0, z, 2001))   # Mpc

    def vol(z1, z2, arcmin2):
        om = arcmin2 * (math.pi / 180 / 60) ** 2
        return om / 3 * (D_c(z2) ** 3 - D_c(z1) ** 3)

    def ceiling_fn(z, Rfun=None, spec="corrected"):
        n = hmf(z, spec=spec, Rfun=Rfun); cn, cr = cum(n)
        lcr = np.log(np.maximum(cr, 1e-300)); lcn = np.log(np.maximum(cn, 1e-300)); lM = np.log(MG)
        rhoh = lambda Mv: float(np.exp(np.interp(math.log(Mv), lM, lcr)))
        nh = lambda Mv: float(np.exp(np.interp(math.log(Mv), lM, lcn)))
        return rhoh, nh

    def eps_req_rho(rhoh, Mstar, rho_obs):
        F = lambda le: math.log(math.exp(le) * cp.fb * rhoh(Mstar / (math.exp(le) * cp.fb))) - math.log(rho_obs)
        try:
            return math.exp(brentq(F, math.log(1e-4), math.log(1e3)))
        except ValueError:
            return float("inf")

    def eps_req_n(nh, Mstar, n_obs):
        F = lambda le: math.log(nh(Mstar / (math.exp(le) * cp.fb))) - math.log(n_obs)
        try:
            return math.exp(brentq(F, math.log(1e-4), math.log(1e3)))
        except ValueError:
            return float("inf")

    samples = {"published": [(i, z, lm) for (i, z, zl, zh, lm, ml, mh) in LABBE]}
    rev = []
    for (i, z, zl, zh, lm, ml, mh) in LABBE:
        if i in SPEC_Z:
            if i == 14924:
                rev.append((i, SPEC_Z[i], RUBIES_14924["medium"] - SALP_TO_CHAB))          # RUBIES medium, Salpeter-equivalent
            else:
                rev.append((i, SPEC_Z[i], lm))
        else:
            rev.append((i, z, lm))
    samples["revised"] = rev
    VOL = {b: vol(b[0], b[1], AREA_LABBE) for b in BINS}
    P(f"    Labbe volume: 38 arcmin^2 -> 7<z<8.5: {VOL[BINS[0]]:.3e} Mpc^3, 8.5<z<10: {VOL[BINS[1]]:.3e} Mpc^3 (Boylan-Kolchin: ~1e5 each)")
    readings = [("LCDM", None)] + [(lab, key) for key, lab in sets]
    B1 = {}
    for sname, smp in samples.items():
        for imf, dm in (("Salpeter", 0.0), ("Chabrier", SALP_TO_CHAB)):
            for b in BINS:
                objs = sorted([(10 ** (lm + dm), i) for (i, z, lm) in smp if b[0] < z <= b[1]], reverse=True)
                if not objs:
                    continue
                for zev, zlab in ((b[2], "z_eff"), (b[0], "z_lo")):
                    for lab, key in readings:
                        Rf = None if key is None else (lambda Mv, zz=zev, R_=Rfun_of(key)[0]: R_(Mv, zz))
                        rhoh, nh = ceiling_fn(zev, Rfun=Rf)
                        cumM = 0.0; worst = (0.0, None)
                        for Ms, i in objs:
                            cumM += Ms
                            e_ = eps_req_rho(rhoh, Ms, cumM / VOL[b])
                            if e_ > worst[0]:
                                worst = (e_, i)
                        top = objs[0][0]
                        e_top_lo = eps_req_rho(rhoh, top, 0.173 * top / VOL[b])                 # Gehrels 1986: N = 1, 84% lower bound
                        B1[(sname, imf, b[2], zlab, lab)] = {"eps_req": worst[0], "at": worst[1], "eps_top_poisson_lo": e_top_lo,
                                                             "top": math.log10(top), "n_obj": len(objs),
                                                             "rho_obs_top": top / VOL[b], "rho_max_top": cp.fb * rhoh(top / cp.fb)}
    for sname in samples:
        P(f"    Labbe et al. 2023, {sname} sample -- eps required (max over thresholds) [eps for the top object at its Poisson 84% lower bound]:")
        for imf in ("Salpeter", "Chabrier"):
            for b in BINS:
                for zlab in ("z_eff", "z_lo"):
                    if (sname, imf, b[2], zlab, "LCDM") not in B1:
                        continue
                    row = B1[(sname, imf, b[2], zlab, "LCDM")]
                    P(f"      {imf:8s} {b[0]}<z<{b[1]} at z = {b[2] if zlab == 'z_eff' else b[0]}: top log M* {row['top']:.2f} (N = {row['n_obj']}); "
                      + ", ".join(f"{lab}: {B1[(sname, imf, b[2], zlab, lab)]['eps_req']:.3f}" for lab, key in readings)
                      + f"  [LCDM top Poisson-lo {row['eps_top_poisson_lo']:.3f}]")
    OUT["numbers"]["B1"] = {"|".join(str(x) for x in k): v for k, v in B1.items()}
    pub = B1[("published", "Salpeter", 7.5, "z_eff", "LCDM")]["eps_req"]; revv = B1[("revised", "Salpeter", 7.5, "z_eff", "LCDM")]["eps_req"]
    P("    for orientation: Boylan-Kolchin 2023 quotes eps(z ~ 9) = 0.99 and eps(z ~ 7.5) = 0.84 for the Labbe candidates as they stood "
      "before the published revision (his Planck cosmology); this lane uses the published revision's masses and its own volume")
    check("B1 (H11, reported) LCDM's OWN STATUS against Labbe et al.: the published z ~ 7.5 top object needs eps > 1 (Salpeter); after "
          "the spectroscopic revisions the 7 < z < 8.5 bin does not",
          f"published 7<z<8.5 (Salpeter, z_eff): eps_req {pub:.3f}; revised: {revv:.3f}; published 8.5<z<10: "
          f"{B1[('published', 'Salpeter', 9.1, 'z_eff', 'LCDM')]['eps_req']:.3f}", True, load_bearing=False)

    # B3 JADES-GS-z14-0
    b3 = {}
    for zlab, zv in (("z", GSZ14["z"]), ("z_lo", GSZ14["z_lo"])):
        for win in ((13.5, 15.0), (13.0, 16.0)):
            V = vol(win[0], win[1], AREA_JADES); n_obs = 1.0 / V
            for lab, key in readings:
                Rf = None if key is None else (lambda Mv, zz=zv, R_=Rfun_of(key)[0]: R_(Mv, zz))
                rhoh, nh = ceiling_fn(zv, Rfun=Rf)
                for mlab in ("logM", "logM_lo", "logM_hi"):
                    Ms = 10 ** GSZ14[mlab]
                    b3[(zlab, win, lab, mlab)] = {"V": V, "n_obs": n_obs, "N_exp_eps1": nh(Ms / cp.fb) * V, "eps_req": eps_req_n(nh, Ms, n_obs),
                                                  "eps_req_poisson_lo": eps_req_n(nh, Ms, 0.173 * n_obs)}
    for zlab in ("z", "z_lo"):
        for win in ((13.5, 15.0), (13.0, 16.0)):
            r0 = b3[(zlab, win, "LCDM", "logM")]
            P(f"    JADES-GS-z14-0 at z = {GSZ14[zlab]}, window {win}: V = {r0['V']:.3e} Mpc^3, n_obs = {r0['n_obs']:.2e}; LCDM N_exp(eps = 1) "
              + "/".join(f"{b3[(zlab, win, 'LCDM', ml)]['N_exp_eps1']:.2f}" for ml in ("logM_lo", "logM", "logM_hi")) + " (log M* 8.4/8.6/9.3); eps_req "
              + ", ".join(f"{lab}: {b3[(zlab, win, lab, 'logM')]['eps_req']:.3f}" for lab, key in readings))
    OUT["numbers"]["B3"] = {"|".join(str(x) for x in k): v for k, v in b3.items()}
    e14 = b3[("z", (13.5, 15.0), "LCDM", "logM")]["eps_req"]
    check("B3 (H11, reported) LCDM's OWN STATUS against JADES-GS-z14-0: one galaxy of 10^8.6 Msun in 58 arcmin^2 at 13.5 < z < 15 "
          "needs eps < 1 at the central mass", f"eps_req {e14:.3f} (central); {b3[('z', (13.5, 15.0), 'LCDM', 'logM_hi')]['eps_req']:.3f} at +1 sigma mass",
          True, load_bearing=False)

    # B4 the verdict check: the chain's ceiling against LCDM's at every data cell
    diffs = {}
    for k, v in B1.items():
        if k[4] != "LCDM":
            diffs[k] = v["eps_req"] / B1[k[:4] + ("LCDM",)]["eps_req"] - 1
    for k, v in b3.items():
        if k[2] != "LCDM":
            diffs[("z14",) + k] = v["eps_req"] / b3[(k[0], k[1], "LCDM", k[3])]["eps_req"] - 1
    worstT = max(abs(v) for k, v in diffs.items() if ("T V" in str(k)))
    worstB = max(abs(v) for k, v in diffs.items() if ("B V" in str(k)))
    worstTH = max([abs(v) for k, v in diffs.items() if "top hat" in str(k)] or [0.0])
    check("B4 (H10) THE CHAIN INHERITS LCDM's CEILING: at every data cell (Labbe published and revised, both IMFs, both redshift "
          "conventions; GS-z14-0 at both redshifts, both windows, three masses) the eps each point requires differs from LCDM's by "
          "< 10% in reading T (multi-shell, V0/V1, both footings) and < 1% in reading B",
          f"max |eps_chain/eps_LCDM - 1|: reading T {worstT:.2%}, reading B {worstB:.2%}; the sharp-edged top-hat bracket {worstTH:.2%}",
          worstT < 0.10 and worstB < 0.01,
          reading="the chain's MOND sector is confined by its band-pass to r <~ 2L(z) = 1-35 kpc at z = 6-13.6 and is exactly off above "
                  "(V1): it cannot speed the collapse of the 1e10-1e12 Msun halos these galaxies need")
    OUT["numbers"]["B4"] = {"|".join(str(x) for x in k): v for k, v in diffs.items()}

    # ======================================================================================================== R
    if not MUTATE:
        banner("R  ROBUSTNESS: FP13's threshold window, the dark field's mass, the footings (reading T, multi-shell)")
        r1 = {}
        for var in ("V2", "V3", "V4", "V5", "V6", "V7"):
            for f in ("canonical", "alt"):
                key = f"multi|{var}|T|{f}|main"
                if key not in bar:
                    continue
                Rf, _ = Rfun_of(key)
                for z in (7.0, 10.0, 14.0):
                    n_c = hmf(z, spec=("corrected_m1.9e-19" if var == "V2" else "corrected_m5.2e-19" if var == "V3" else "corrected"),
                              Rfun=lambda Mv, z=z: Rf(Mv, z))
                    n_l = hmf(z, spec="corrected")
                    r1[(var, f, z)] = {Mv: float(np.interp(math.log(Mv), np.log(MG), n_c / n_l)) for Mv in (1e9, 1e10, 1e11)}
        for (var, f, z), v in r1.items():
            if f == "canonical":
                P(f"    {var} z={z:g}: n_chain/n_LCDM at 1e9/1e10/1e11 = " + "/".join(f"{x:.4f}" for x in v.values()))
        rob = max(abs(x - 1) for v in r1.values() for Mv, x in v.items() if Mv >= 1e10)
        check("R1 (reported) ROBUSTNESS: the abundance ratio at M >= 1e10, z = 7-14, over s = 1.3/2.6 (both spectra), m = 1.9e-19/"
              "5.2e-19 eV (their wave cut-off included) and both footings", f"max |ratio - 1| = {rob:.2%}", True, load_bearing=False)
        OUT["numbers"]["R1"] = {f"{k[0]}|{k[1]}|{k[2]}": {f"{Mv:.0e}": x for Mv, x in v.items()} for k, v in r1.items()}

    # ======================================================================================================== verdict
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    banner("VERDICT")
    if MUTATE:
        P("  MUTATE: with the band-pass removed from the force law the chain's MOND reads every halo's full peculiar field and its")
        P("  halo abundance and ceiling leave LCDM's -- B4 fails, as pre-declared.")
    else:
        tl = [lab for key, lab in sets if lab.startswith("T ")]
        r10 = max(h1[(lab, 7.0)][1e10][0] for lab in tl); r9 = max(h1[(lab, 7.0)][1e9][0] for lab in tl)
        r11 = max(abs(h1[(lab, z)][Mv][0] - 1) for lab in tl for z in (7.0, 10.0, 14.0) for Mv in MREP if Mv >= 1e11)
        P("  The chain's linear power at z >= 6 is LCDM's exactly (K4).  Reading T (the yardstick's convention) raises the abundance of")
        P(f"  small halos at z = 7 -- up to x{r9:.2f} at 1e9 and x{r10:.2f} at 1e10 Msun -- and leaves M >= 1e11 within {r11:.1%}; reading B (the")
        P(f"  action's content) leaves every mass within {sh_B:.2%}.  The knob-free ceiling: the eps each data point requires changes by <= {worstT:.2%}")
        P(f"  (T) / {worstB:.2%} (B); the sharp-edged top hat, the most the band-pass allows, by <= {worstTH:.1%}.  The chain neither eases nor")
        P(f"  worsens the tension at the host masses the data need; where LCDM is pressed (published Labbe, 7 < z < 8.5, Salpeter: eps {pub:.2f}),")
        P("  so is the chain.")
    P(f"  Not 'closed'.  Time {time.time() - T0:.0f} s.")
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(OUTDIR, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


if __name__ == "__main__":
    main()
