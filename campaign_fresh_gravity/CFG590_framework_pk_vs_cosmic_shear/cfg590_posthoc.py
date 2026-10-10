#!/usr/bin/env python3
"""CFG590 post-hoc (NOT a verdict input; added after the frozen run, 2026-10-10).
(a) How much of the z = 0 framework excess plausibly survives at lensing redshifts? Crude estimate: the excess is driven by the
    one-halo term of log M 14-15.5 halos (CFG556 drivers). s(z) = share of P(k = 1) from M200m >= 1e14 Msun/h at z, divided by
    the same share at z = 0 (Tinker08 + NFW/Duffy08 halo model, colossus; LCDM). Assumes the per-halo framework/LCDM profile
    ratio at fixed mass is z-independent. Compared with the s thresholds from cfg590_results.json.
(b) HMcode-2020 S_fb(k = 1, z = 0.5) at log T_AGN = 8.3 and 9.0 (9.0 = outside calibration), and Z of the PRIMARY at 9.0 from JSON.
  OMP_NUM_THREADS=2 nice -n 10 python3 cfg590_posthoc.py -> cfg590_posthoc.out, cfg590_posthoc.json"""
import os, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import numpy as np
from scipy.special import sici
from colossus.cosmology import cosmology
from colossus.lss import mass_function
from colossus.halo import concentration, mass_so
import camb
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
h = 0.6736; Om = (0.02237 + 0.12) / h ** 2; Ob = 0.02237 / h ** 2
cosmo = cosmology.setCosmology("cfg590", {"flat": True, "H0": 67.36, "Om0": Om, "Ob0": Ob, "sigma8": 0.811, "ns": 0.965})
RHO = cosmo.rho_m(0) * 1e9                       # Msun h^2 / Mpc^3 comoving
LM = np.linspace(9, 16, 281); M = 10 ** LM; dl = (LM[1] - LM[0]) * math.log(10)
def u_nfw(k, Mh, z):
    c = concentration.concentration(Mh, "200m", z, model="duffy08")
    R = mass_so.M_to_R(Mh, z, "200m") / 1000 * (1 + z)     # comoving Mpc/h
    rs = R / c; x = k * rs; mc = np.log1p(c) - c / (1 + c)
    si1, ci1 = sici((1 + c) * x); si0, ci0 = sici(x)
    return (np.sin(x) * (si1 - si0) - np.sin(c * x) / ((1 + c) * x) + np.cos(x) * (ci1 - ci0)) / mc
def share(z, k=1.0, Mcut=1e14):
    dn = mass_function.massFunction(M, z, mdef="200m", model="tinker08", q_out="dndlnM")
    term = dn * (M / RHO) ** 2 * u_nfw(k, M, z) ** 2 * dl
    p1 = float(np.sum(term)); pc = float(np.sum(term[M >= Mcut])); pl = float(cosmo.matterPowerSpectrum(k, z))
    return pc / (p1 + pl), p1, pl
P("CFG590 post-hoc (not a verdict input). kappa = 1/2 FITTED; cold energy MASS still required; not theory closed.")
s0 = share(0.0)[0]
zs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
S = {}
for z in zs:
    sh, p1, pl = share(z); S[z] = sh / s0
    P(f"  z {z:.1f}: share of P(k=1) from M200m >= 1e14 = {sh:.3f}; s(z) = {S[z]:.3f}")
J = json.load(open(os.path.join(HERE, "cfg590_results.json")))
thr = {f: J["models"][f"{f}|PRIMARY CFG559 kin"]["s_class_changes"] for f in ("canonical", "alt")}
P(f"  frozen-run s thresholds (class changes): {thr}")
# lensing-plane weighting of C_ell for the KiDS-like kernel (same construction as cfg590_shear.py M1, DMO, feedback off)
p = camb.CAMBparams(); p.set_cosmology(H0=67.36, ombh2=0.02237, omch2=0.12, mnu=0.0, omk=0, num_massive_neutrinos=0)
p.InitPower.set_params(ns=0.965, As=2.1e-9); p.set_matter_power(redshifts=[0.0], kmax=60)
r = camb.get_results(p); p.InitPower.set_params(ns=0.965, As=2.1e-9 * (0.811 / r.get_sigma8_0()) ** 2)
p.NonLinearModel.set_params(halofit_version="mead2020")
PNL = camb.get_matter_power_interpolator(p, nonlinear=True, hubble_units=True, k_hunit=True, kmax=60, zmax=3.5)
res = camb.get_results(p)
ZG = np.linspace(0.005, 3.0, 300); CH = np.array([res.comoving_radial_distance(z) * h for z in ZG]); AG = 1 / (1 + ZG)
SE = {}
for surv, zm in (("KiDS", 0.67), ("DES", 0.63)):
    z0 = zm / (math.gamma(4 / 1.5) / math.gamma(3 / 1.5)); n = ZG ** 2 * np.exp(-(ZG / z0) ** 1.5); n /= np.trapz(n, ZG)
    nchi = n / np.gradient(CH, ZG)
    q = np.array([np.trapz(np.where(CH >= c, nchi * (CH - c) / CH, 0), CH) for c in CH]) * 1.5 * Om / 2997.92458 ** 2 * CH / AG
    ell = np.geomspace(100, 2000, 24)
    integ = np.array([[q[j] ** 2 / CH[j] ** 2 * PNL.P(ZG[j], (l + 0.5) / CH[j]) for j in range(len(ZG))] for l in ell])
    wz = np.sum(integ, axis=0) * np.gradient(CH)   # lens-plane weight, summed over the ell bins
    wz /= wz.sum()
    sz = np.interp(ZG, zs, [S[z] for z in zs], right=S[zs[-1]])
    SE[surv] = dict(s_eff=float(np.sum(wz * sz)), z_median_weight=float(np.interp(0.5, np.cumsum(wz), ZG)))
    P(f"  {surv}: lens-plane-weighted s_eff = {SE[surv]['s_eff']:.3f} (median lens-plane z {SE[surv]['z_median_weight']:.2f})")
# (b) HMcode extrapolation
SF = {}
for T in (8.3, 9.0):
    p.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=T)
    pf = camb.get_matter_power_interpolator(p, nonlinear=True, hubble_units=True, k_hunit=True, kmax=60, zmax=3.5)
    p.NonLinearModel.set_params(halofit_version="mead2020")
    SF[T] = float(pf.P(0.5, 1.0) / PNL.P(0.5, 1.0))
    P(f"  S_fb(k = 1, z = 0.5) at log T_AGN = {T}: {SF[T]:.3f}" + ("  (outside HMcode-2020 calibration)" if T > 8.3 else ""))
Z9 = {f: {d: J["models"][f"{f}|PRIMARY CFG559 kin"]["feedback_needed"][d]["Z_at_T"]["9.0"] for d in ("KiDS", "DES")} for f in ("canonical", "alt")}
P(f"  PRIMARY Z at log T_AGN = 9.0 (from cfg590_results.json): {Z9}")
open(os.path.join(HERE, "cfg590_posthoc.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(s_of_z={str(z): v for z, v in S.items()}, s_eff=SE, s_thresholds=thr, S_fb_k1_z05=SF, Z_primary_T9=Z9,
               note="post-hoc, not a verdict input; crude cluster-share scaling; per-halo ratio assumed z-independent"),
          open(os.path.join(HERE, "cfg590_posthoc.json"), "w"), indent=1)
