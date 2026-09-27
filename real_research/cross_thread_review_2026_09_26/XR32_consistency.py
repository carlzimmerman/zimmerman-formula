#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR32 (3/3) -- WHAT THE CONVERSION MUST ALSO PASS: CMB lensing (ACT DR6 + Planck PR4), cluster counts (eRASS1, SPT),
DESI redshift-space distortions (f sigma8) and DESI's sum m_nu preference.

WHY.  A late-time suppression that lowers weak-lensing S8 must not lower the high-z lensing (z ~ 1-3), must leave the
cluster counts (recapture keeps clusters' carrier), and must not strain RSD growth or DESI's preference for little
growth suppression (a positive neutrino mass suppresses growth; DESI + CMB prefer less than the minimal mass).

METHOD (the chain's P(k, z) as in XR32_matter_power: L319's two-component linear solve on XR19's histories, the halo-model
response R(k, z) on Planck-2018 HMcode-2020; normalised to Planck 2018 -- an ASSUMPTION pending XR26)
  CMB LENSING.  C_L^kappakappa by Limber to the last-scattering distance (P above z = 10 continued as a^2); the chain uses
    R(k, z) to z = 4 and the linear T^2(k, z) above.  The amplitude over ACT DR6's baseline L = 40-763: (a) equal weight
    per band in ten log-spaced bands (ACT's per-band S/N is roughly flat; a proxy, not ACT's bandpower covariance), (b)
    cosmic-variance weights (2L + 1).  Against ACT DR6 A_lens = 1.013 +- 0.023 (Qu+24) and ACT+Planck sigma8 = 0.812 +-
    0.013 (Madhavacheril+24).  Control: this Limber against CAMB's own (non-Limber) lensing potential.
  CLUSTER COUNTS.  Sheth-Tormen counts per steradian, N(> M_thr) = int dz (dV/dz dOmega) int dlnM n(M) P(M_obs > M_thr),
    lognormal scatter 0.2 in ln M (same for LCDM and the chain); M500c from M_vir (NFW, Duffy+08).  The chain's cluster
    (weak-lensing-calibrated) mass: M_obs = M500c (f_b + f_c ret(M, z)) [+ the stand-in phantom inside R500: (nu_mono - 1)
    x the GP0 observed bound baryons, both footings].  Halo population LCDM's (primary) or the cold field's (bracket).
    Selections (proxies, disclosed): eRASS1-like z 0.1-0.8, M500c > 1.5e14 (and 3e14) Msun; SPT-like z 0.25-1.78, M500c >
    3.5e14 (and 5e14) Msun.  The count-equivalent S8: the LCDM sigma8 (Omega_m fixed) that gives the same count.  Against
    eRASS1 S8 = 0.86 +- 0.01 (Ghirardini+24) and SPT S8 = 0.795 +- 0.029 (Bocquet+24).
  RSD.  f = d ln delta/d ln a at k ~ 0.1 h/Mpc (0.05 and 0.2 reported) from the solver, sigma8(z) from T^2; f sigma8 of
    the chain against LCDM's at DESI DR1's z_eff (0.295, 0.510, 0.706, 0.930, 1.317, 1.491); the implied sigma8 against
    DESI DR1 full shape + BAO, sigma8 = 0.842 +- 0.034 (DESI 2024 VII; equal weights per bin: a proxy).
  SUM m_nu.  CAMB (non-Limber) C_L^phiphi for sum m_nu = 0.06/0.12/0.18 eV (three degenerate states) at fixed theta_*,
    omega_b, omega_c, A_s, n_s, tau: the lensing amplitude's slope; the chain's lensing change as an equivalent sum m_nu.
    Against DESI DR2 + CMB: sum m_nu < 0.0642 eV (95%), sigma = 0.020 eV; sigma(sum m_nu,eff) = 0.053 eV, 3 sigma below
    the oscillation floor (Elbers+25).  The conversion leaves the expansion history alone (daughters: w ~ sigma_d^2/c^2 ~
    1e-7), so the BAO/geometry part of DESI's constraint is untouched: only the lensing channel moves.
PRE-DECLARED (written 2026-09-27T14:01Z, before any full run)
  H3a [load-bearing; MUTATE must fail] the conversion lowers the CMB-lensing amplitude over L = 40-763 (A < 1).
  H3b CMB lensing stays Planck-like: |A - 1| <= 0.023 (ACT DR6 1 sigma) under an S/N-like weighting.
  H3c no phantom: the cluster-count-equivalent S8 is below Planck's for both selections (recapture does not fully
      preserve the counts).
  H3d the chain's fsigma8-implied sigma8 lies within 2 sigma of DESI DR1 full-shape (0.842 +- 0.034).
  H3e the conversion acts as a positive lensing-equivalent sum m_nu >= 0.02 eV (worsens DESI's low-mass preference in the
      lensing channel).
CHECKS (load-bearing unless marked)
  C1 CONTROL: this lane's Limber C_L^kappakappa (LCDM) against CAMB's own lensing potential within 2% at L = 40-763.
  C2 CONTROL: no conversion gives A = 1 exactly and the LCDM count exactly (count-equivalent S8 = Planck's).
  C3 CONTROL: the count-equivalent inversion returns a known sigma8 (LCDM at sigma8 = 0.78) to 1e-4.
  C4 (reported) the CAMB lensing slope per 0.1 eV of sum m_nu.
  H3a-H3e as above (nominal cell, primary reading, no phantom, unless stated); robustness across delta_t0 5.31-25, the
  readings, the halo populations, both footings and the phantom bracket reported.
MUTATE=1: the conversion switched off: A = 1, counts and f sigma8 return to LCDM, the equivalent sum m_nu to 0.06 eV;
  H3a must FAIL (rc = 1).
HISTORY (disclosed): the unit tests and smoke runs listed in XR32_matter_power.py's and XR32_survey_s8.py's docstrings.  One
  smoke run of this script (scratch, not for the record) completed with the code as it stands (7/9: H3b and H3d falling);
  its outcomes were seen before the recorded runs and no hypothesis was changed.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR32_consistency.py   (MUTATE=1 first)
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import XR32_common as X
import numpy as np
import camb
from scipy import special, optimize

MUTATE = os.environ.get("MUTATE", "0") == "1"
OUTD = os.environ.get("XR32_OUTDIR", HERE)                              # smoke tests write to scratch, never the record
SLUG = "XR32_consistency"; SUF = "_MUTATE" if MUTATE else ""
P = X.Log(os.path.join(OUTD, SLUG + SUF + ".out"))
T0 = time.time(); CH = []; OUT = {"lane": "XR32", "part": "3/3 consistency", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)
def el(): return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("PRE-DECLARED")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: conversion switched off; H3a must FAIL ***")
base = X.ChainBase(); C = base.C; hm = base.hm
S8P = float(base.res.get_sigma8_0()) * math.sqrt(C.Om / 0.3); s8P = float(base.res.get_sigma8_0())
NAMES = [n for n, _, _ in X.HISTORIES]
R = X.record(); LC = R["LC"]
if MUTATE:
    comp0 = dict(dc=LC.copy(), dd=np.zeros_like(LC), rc=np.ones(LC.shape[1]), rd=np.zeros(LC.shape[1]), tot=LC.copy())
    H = {n: dict(Fz=X.history(k, True), vk=v, comp=comp0, T=X.Transfer(comp0, LC)) for n, k, v in X.HISTORIES}
else:
    H = X.solve_histories(NAMES)
P(f"  base and {len(H)} histories ready; Planck-2018 sigma8 {s8P:.4f}, S8 {S8P:.4f}   {el()}")
PH = {"none": None, "L1.7 canonical": ("canonical", X.L_STANDIN, "sharp"), "L1.7 alt": ("alt", X.L_STANDIN, "sharp"),
      "running L canonical (sensitivity)": ("canonical", "running", "sharp")}
NOM = "nominal (dt0 5.31)"; PRIM = X.READINGS[0]

# ================================================================================================ CMB lensing
banner("CMB LENSING: C_L^kappakappa (Limber) of the chain against LCDM; the amplitude over ACT DR6's L = 40-763")
zstar = float(base.res.get_derived_params()["zstar"]); chis = float(C.chi(zstar))
chi = np.linspace(1.0, chis * 0.999, 1400)
zi = np.linspace(0.0, zstar, 200000); zc_ = np.interp(chi, C.chi(zi[::100]), zi[::100])
aW = 1 / (1 + zc_); Wk = 1.5 * C.Om / 2997.92458 ** 2 * chi / aW * (chis - chi) / chis
LL = np.unique(np.round(np.geomspace(20, 2000, 120)).astype(int)).astype(float)


def Pcmb(k, z, Rf=None, T=None):
    if z <= 10.0:
        p = C.P(k, z)
    else:
        p = C.P(k, 10.0, lin=True) * (11.0 / (1 + z)) ** 2
    if Rf is None: return p
    if z <= X.ZR[-1]: return p * Rf(k, z)
    return p * (T(k, min(z, 60.0), "tot") if T is not None else 1.0)


def clkk(Rf=None, T=None):
    out = np.zeros(len(LL))
    w = np.gradient(chi) * Wk ** 2 / chi ** 2
    for j, (x, z) in enumerate(zip(chi, zc_)):
        out += w[j] * Pcmb((LL + 0.5) / x, z, Rf, T)
    return out


CL0 = clkk()
pl = X.camb_setup(zs=None, nl="mead2020", lensing=True); pl.set_for_lmax(2500, lens_potential_accuracy=4)
rl = camb.get_results(pl); cpp = rl.get_lens_potential_cls(lmax=2000, raw_cl=True)[:, 0]
Lc = np.arange(len(cpp)); ckk_camb = (Lc * (Lc + 1.0)) ** 2 / 4 * cpp
sel = (LL >= 40) & (LL <= 763)
dev = float(np.max(np.abs(CL0[sel] / np.interp(LL[sel], Lc, ckk_camb) - 1)))
check("C1 CONTROL: this lane's Limber C_L^kappakappa (Planck 2018, HMcode-2020) against CAMB's own lensing potential (non-Limber) at L = 40-763",
      f"max |ratio - 1| = {dev:.4f}", dev <= 0.02)
edges = np.geomspace(40, 763, 11)


def amp(ratio):
    rb = [np.mean(ratio[(LL >= a) & (LL < b)]) for a, b in zip(edges[:-1], edges[1:])]
    cv = (2 * LL[sel] + 1); return float(np.mean(rb)), float(np.sum(cv * ratio[sel]) / np.sum(cv))


CMB = {}
cfg_cmb = [(NOM, PRIM, "lcdm", pn) for pn in PH] + [(NOM, rd, "lcdm", "none") for rd in X.READINGS[1:]] + \
          [(n, PRIM, "lcdm", "none") for n in NAMES if n != NOM] + [(n, PRIM, "lcdm", f"L1.7 {f}") for n, f in (("dt0 14.6 (canonical top)", "canonical"), ("dt0 22.8 (alt top)", "alt"))]
Rcache = {}
for (n, rd, sm, pn) in cfg_cmb:
    h_ = H[n]; key = f"{n} | {rd} | pop {sm} | phantom {pn}"
    Rg = base.response(h_["T"], h_["Fz"], h_["vk"], rd, PH[pn], sm, MUTATE); Rcache[key] = Rg
    ratio = clkk(X.R_fun(Rg), h_["T"]) / CL0
    A_band, A_cv = amp(ratio)
    CMB[key] = dict(A_band=A_band, A_cv=A_cv, ratio_at={int(L): float(np.interp(L, LL, ratio)) for L in (40, 100, 300, 763, 1000, 2000)},
                    sigma8_cmbl=s8P * math.sqrt(A_band))
    P(f"    {key}: C_L ratio L=40/100/300/763/1000/2000 " + "/".join(f"{v:.3f}" for v in CMB[key]["ratio_at"].values())
      + f"; A(40-763) band {A_band:.4f}, CV {A_cv:.4f}; sigma8_CMBL {CMB[key]['sigma8_cmbl']:.4f}   {el()}")
OUT["numbers"]["cmb_lensing"] = CMB
kN = f"{NOM} | {PRIM} | pop lcdm | phantom none"
LCt = X.Transfer(dict(dc=LC.copy(), dd=np.zeros_like(LC), rc=np.ones(LC.shape[1]), rd=np.zeros(LC.shape[1]), tot=LC.copy()), LC)
Rid = base.response(LCt, (np.array([0.0, 20.0]), np.array([0.0, 0.0])), 600.0, PRIM, None, "lcdm", mutate=True)
A_id = amp(clkk(X.R_fun(Rid), LCt) / CL0)

# ================================================================================================ sum m_nu
banner("SUM m_nu: CAMB's lensing slope, and the conversion as an equivalent neutrino mass (lensing channel only)")
theta = float(base.res.cosmomc_theta()) if hasattr(base.res, "cosmomc_theta") else None
if theta is None: theta = float(base.res.get_derived_params()["thetastar"]) / 100
AM = {}
for mnu in (0.06, 0.12, 0.18):
    pn_ = X.camb_setup(zs=None, nl="mead2020", lensing=True, mnu=mnu, nmass=3, theta=theta); pn_.set_for_lmax(2500, lens_potential_accuracy=4)
    cp = camb.get_results(pn_).get_lens_potential_cls(lmax=2000, raw_cl=True)[:, 0]; AM[mnu] = cp
rat12 = np.interp(LL, Lc, AM[0.12] / AM[0.06]); rat18 = np.interp(LL, Lc, AM[0.18] / AM[0.06])
s12, s18 = amp(rat12)[0] - 1, amp(rat18)[0] - 1
slope = s12 / 0.06
check("C4 (reported) CAMB's C_L^phiphi response to sum m_nu at fixed theta_* (three degenerate states; band-weighted over L = 40-763)",
      f"dA = {s12:+.4f} per +0.06 eV, {s18:+.4f} per +0.12 eV (slope {slope:+.3f} per eV)", True, load_bearing=False)
MNU = {k: dict(dA=v["A_band"] - 1, mnu_eq=0.06 + (v["A_band"] - 1) / slope) for k, v in CMB.items()}
for k in (kN, f"{NOM} | {PRIM} | pop lcdm | phantom L1.7 canonical"):
    P(f"    {k}: dA {MNU[k]['dA']:+.4f} -> lensing-equivalent sum m_nu {MNU[k]['mnu_eq']:.3f} eV (+{MNU[k]['mnu_eq'] - 0.06:.3f} over the 0.06 eV baseline)")
OUT["numbers"]["mnu"] = dict(slope_per_eV=slope, dA_012=s12, dA_018=s18, configs=MNU)

# ================================================================================================ cluster counts
banner("CLUSTER COUNTS: count-equivalent S8 for eRASS1-like and SPT-like selections")
SELS = {"eRASS1-like (z 0.1-0.8, M500c > 1.5e14)": (0.1, 0.8, 1.5e14), "eRASS1-like (z 0.1-0.8, M500c > 3e14)": (0.1, 0.8, 3e14),
        "SPT-like (z 0.25-1.78, M500c > 3.5e14)": (0.25, 1.78, 3.5e14), "SPT-like (z 0.25-1.78, M500c > 5e14)": (0.25, 1.78, 5e14)}
SIGLN = 0.2


def m500_of(z):
    """M500c (Msun/h) and R500 (physical Mpc/h) of every halo of hm at z from its NFW (Duffy c_vir)."""
    rvir, cv, Dvm = hm.profiles(z); a = 1 / (1 + z)
    rv = rvir * a; rs = rv / cv; mc = np.log1p(cv) - cv / (1 + cv)
    rhoc = 2.775e11 * (C.Om * (1 + z) ** 3 + 1 - C.Om)
    x = np.geomspace(0.05, 1.5, 400)
    Mx = hm.M[:, None] * (np.log1p(cv[:, None] * x) - cv[:, None] * x / (1 + cv[:, None] * x)) / mc[:, None]
    mean = Mx / (4 / 3 * math.pi * (x[None, :] * rv[:, None]) ** 3)
    j = np.argmin(np.abs(np.log(mean / (500 * rhoc))), axis=1)
    return Mx[np.arange(len(hm.M)), j], x[j] * rv


_M5 = {}


def M5(z):
    key = round(float(z), 6)
    if key not in _M5: _M5[key] = m500_of(float(z))
    return _M5[key]


def ph_r500(z, foot, M500, R500):
    g = X.gp0(); Mb = np.asarray(g.M_bound(hm.M / hm.h, z, "observed"), float)          # Msun
    Rp = R500 / hm.h * X.MPC_M
    y = X.G_SI * Mb * X.MSUN / Rp ** 2 / X.A0[foot]
    on = (hm.M / hm.h >= X.PH_MRANGE_MSUN[0]) & (hm.M / hm.h <= X.PH_MRANGE_MSUN[1])
    return np.where(on, (X.nu_mono(y) - 1) * Mb * hm.h, 0.0)                              # Msun/h


def counts(z_lo, z_hi, Mthr_msun, frac_fn=None, ph=None, sig8_scale=1.0, pop=None):
    tot = 0.0; zz = np.linspace(z_lo, z_hi, 12)
    for z in zz:
        Pkk = C.P(hm.kk, z, lin=True) * sig8_scale ** 2
        if pop is not None: Pkk = Pkk * pop(hm.kk, z)
        n, _ = hm.mf(hm.sigma(Pkk))
        M500, R500 = M5(z)
        Mobs = M500 * (1 - hm.fnu if frac_fn is None else frac_fn(z))
        if ph is not None: Mobs = Mobs + ph_r500(z, ph, M500, R500)
        pdet = 0.5 * special.erfc((math.log(Mthr_msun * hm.h) - np.log(np.maximum(Mobs, 1e-30))) / (math.sqrt(2) * SIGLN))
        dV = float(C.chi(z)) ** 2 / float(C.Hh(z))
        tot += dV * float(np.sum(n * pdet) * hm.dlnM)
    return tot * (zz[1] - zz[0])


def s8_equiv(Ntarget, sel):
    f = lambda s: math.log(counts(*sel, sig8_scale=s)) - math.log(Ntarget)
    s = optimize.brentq(f, 0.6, 1.5, xtol=1e-7)
    return S8P * s


N0 = {k: counts(*v) for k, v in SELS.items()}
s_test = 0.78 / s8P
got = s8_equiv(counts(*SELS["SPT-like (z 0.25-1.78, M500c > 3.5e14)"], sig8_scale=s_test), SELS["SPT-like (z 0.25-1.78, M500c > 3.5e14)"]) / S8P * s8P
check("C3 CONTROL: the count-equivalent inversion returns a known sigma8 (LCDM counts at sigma8 = 0.78, SPT-like selection)",
      f"{got:.6f}", abs(got - 0.78) <= 1e-4)
CL = {}
cfg_cl = [(NOM, rd, sm, pn) for rd in X.READINGS for sm in ("lcdm", "cold") for pn in ("none", "L1.7 canonical")] + \
         [(NOM, PRIM, "lcdm", "L1.7 alt")] + [(n, PRIM, "lcdm", "none") for n in NAMES if n != NOM]
for (n, rd, sm, pn) in cfg_cl:
    h_ = H[n]; key = f"{n} | {rd} | pop {sm} | phantom {pn}"
    Fe = lambda z, h_=h_: 0.0 if MUTATE else float(np.interp(z, h_["Fz"][0], h_["Fz"][1]))
    def frac_fn(z, h_=h_, rd=rd):
        B = hm.base(z, C.P(hm.kk, z, lin=True), None)
        return X.content(rd, hm.M, z, Fe(z), X.sigma_d(h_["Fz"], h_["vk"], z), h_["vk"], hm, B["rvir"], B["cv"], mutate=MUTATE)[1]
    pop = (lambda k, z, h_=h_: h_["T"](k, z, "cc")) if (sm == "cold" and not MUTATE) else None
    foot = PH[pn][0] if PH[pn] is not None else None
    row = {}
    for sname, sv in SELS.items():
        Nc = counts(*sv, frac_fn=frac_fn, ph=foot, pop=pop)
        row[sname] = dict(N_ratio=Nc / N0[sname], S8_eq=s8_equiv(Nc, sv))
    CL[key] = row
    P(f"    {key}: " + "; ".join(f"{s.split(' (')[0]} {s.split('> ')[1][:-1]}: N/N_LCDM {v['N_ratio']:.3f}, S8_eq {v['S8_eq']:.3f}" for s, v in row.items()) + f"   {el()}")
OUT["numbers"]["clusters"] = CL
hid = dict(Fz=(np.array([0.0, 20.0]), np.array([0.0, 0.0])), vk=600.0)
def frac_id(z):
    B = hm.base(z, C.P(hm.kk, z, lin=True), None)
    return X.content(PRIM, hm.M, z, 0.0, X.sigma_d(hid["Fz"], 600.0, z), 600.0, hm, B["rvir"], B["cv"], mutate=True)[1]
nid = max(abs(counts(*sv, frac_fn=frac_id) / N0[s_] - 1) for s_, sv in SELS.items())
check("C2 CONTROL: no conversion gives the LCDM CMB-lensing amplitude and the LCDM cluster counts exactly",
      f"|A - 1| = {abs(A_id[0] - 1):.1e} (band), {abs(A_id[1] - 1):.1e} (CV); max |N/N_LCDM - 1| = {nid:.1e}",
      abs(A_id[0] - 1) < 1e-12 and abs(A_id[1] - 1) < 1e-12 and nid < 1e-12)

# ================================================================================================ RSD
banner("RSD: f sigma8 of the chain against LCDM at DESI DR1's effective redshifts")
ZD = (0.295, 0.510, 0.706, 0.930, 1.317, 1.491)
kk = np.geomspace(1e-4, 50.0, 6000); x8 = kk * 8.0; W8 = 3 * (np.sin(x8) - x8 * np.cos(x8)) / x8 ** 3
RSD = {}
for n in NAMES:
    T = H[n]["T"]; row = {}
    for z in ZD:
        Pl = C.P(kk, z, lin=True)
        sr = math.sqrt(X._trap(kk ** 2 * Pl * W8 ** 2 * T(kk, z, "tot"), kk) / X._trap(kk ** 2 * Pl * W8 ** 2, kk))
        fr = {}
        for kq in (0.05, 0.1, 0.2):
            fc, ku = T.growth_rate(kq, z, "tot"); fl, _ = T.growth_rate(kq, z, "lc"); fr[kq] = fc / fl
        row[z] = dict(sigma8_ratio=sr, f_ratio=fr, fs8_ratio=sr * fr[0.1])
    imp = s8P * float(np.mean([row[z]["fs8_ratio"] for z in ZD]))
    RSD[n] = dict(bins={str(z): v for z, v in row.items()}, sigma8_implied=imp)
    P(f"    {n:26s}: f sigma8 ratio at z_eff " + "/".join(f"{row[z]['fs8_ratio']:.4f}" for z in ZD) + f"; f ratio k=0.05/0.1/0.2 at z=0.51 "
      + "/".join(f"{row[0.510]['f_ratio'][k]:.4f}" for k in (0.05, 0.1, 0.2)) + f"; implied sigma8 {imp:.4f}")
OUT["numbers"]["rsd"] = RSD

# ================================================================================================ H3a-H3e
banner("H3a-H3e")
A0b = CMB[kN]["A_band"]; A0c = CMB[kN]["A_cv"]
check("H3a the conversion lowers the CMB-lensing amplitude over ACT DR6's L = 40-763 (A < 1; nominal, primary, no phantom)",
      f"A = {A0b:.4f} (band-weighted), {A0c:.4f} (cosmic-variance-weighted)", A0b < 1.0 - 1e-6 and A0c < 1.0 - 1e-6)
check("H3b CMB lensing stays Planck-like: |A - 1| <= 0.023 (ACT DR6's 1 sigma) under the S/N-like (band) weighting",
      f"A - 1 = {A0b - 1:+.4f} (band); {A0c - 1:+.4f} (CV); against ACT DR6 A_lens = 1.013 +- 0.023: {(A0b - 1.013) / 0.023:+.2f} sigma; sigma8_CMBL "
      f"{CMB[kN]['sigma8_cmbl']:.4f} vs ACT+Planck 0.812 +- 0.013: {(CMB[kN]['sigma8_cmbl'] - 0.812) / 0.013:+.2f} sigma", abs(A0b - 1) <= 0.023)
cn = CL[kN]
check("H3c without the phantom the cluster-count-equivalent S8 is below Planck's for both selections (nominal, primary, LCDM population)",
      "; ".join(f"{s}: {v['S8_eq']:.3f}" for s, v in cn.items()) + f" (Planck {S8P:.3f}; eRASS1 0.86 +- 0.01; SPT 0.795 +- 0.029)",
      all(v["S8_eq"] < S8P for v in cn.values()))
sd_ = RSD[NOM]["sigma8_implied"]
check("H3d the chain's f sigma8-implied sigma8 lies within 2 sigma of DESI DR1 full shape + BAO (0.842 +- 0.034)",
      f"{sd_:.4f}: {(sd_ - 0.842) / 0.034:+.2f} sigma (Planck-2018 LCDM {s8P:.4f}: {(s8P - 0.842) / 0.034:+.2f} sigma)", abs(sd_ - 0.842) <= 2 * 0.034)
me = MNU[kN]["mnu_eq"] - 0.06
check("H3e the conversion acts as a positive lensing-equivalent sum m_nu of >= 0.02 eV (lensing channel)",
      f"+{me:.3f} eV (= {me / 0.020:.1f} x DESI DR2's sigma(sum m_nu) = 0.020 eV if lensing carried the whole constraint; the BAO/"
      f"geometry part is untouched)", me >= 0.02)

# ================================================================================================ summary
banner("SUMMARY")
rngA = [v["A_band"] for k, v in CMB.items() if k.endswith("phantom none")]
P(f"""  CMB lensing (L = 40-763): A = {A0b:.4f} at the nominal cell without the phantom; {min(rngA):.4f}-{max(rngA):.4f} over every history and
  reading; ACT DR6 measures 1.013 +- 0.023.  Equivalent sum m_nu (lensing channel): {MNU[kN]['mnu_eq']:.3f} eV.
  Clusters (nominal, primary, no phantom): count-equivalent S8 {min(v['S8_eq'] for v in cn.values()):.3f}-{max(v['S8_eq'] for v in cn.values()):.3f} (eRASS1 0.86 +- 0.01, SPT 0.795 +- 0.029).
  RSD: implied sigma8 {sd_:.4f} (DESI DR1 0.842 +- 0.034).""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(n_checks=len(CH), load_bearing_failed=n_fail, runtime_s=round(time.time() - T0, 1))
json.dump(OUT, open(os.path.join(OUTD, f"{SLUG}_results{SUF}.json"), "w"), indent=1,
          default=lambda o: (o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, np.floating) else str(o))))
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   {el()}")
sys.exit(1 if n_fail else 0)
