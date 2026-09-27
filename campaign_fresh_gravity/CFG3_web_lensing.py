#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG3_web_lensing -- THE EXPANDING LINEAR WEB UNDER THE PRINCIPLE: growth and the CMB lensing amplitude (Planck 2018 VIII).

WHAT THE PRINCIPLE SAYS ABOUT THE WEB.  The linear web is never behind the vacuum (CFG3_principle D5: H^2 - H_Lambda^2 =
8 pi G rho_m/3 > 0, and theta/3 < H_Lambda needs delta > 0.98 at every z <= 1100), so at first order in delta the vacuum's
answer is identically absent: the linear equations are GR + the dark field, growth is LCDM's, and the lensing boost B(k, z) = 1
on every linear mode.  The answer lives only in gated regions (collapsing patches and their infall zones), where each region's
phantom is COMPENSATED (D6: zero net mass), so it can reach the lensing power only through the change of mass profiles on the
regions' own scales.

MACHINERY (read-only).  XR26_cmb.py's lensing pipeline is exec'd from its committed source (the slices that set up CAMB/CLASS at the
Planck 2018 best fit, FP13's growth yardstick, the Limber integral, Planck 2018 VIII's MV band powers and amplitude estimator); its
patched-CLASS build, its C section and its L3-L5 are not run.  CLASS 3.3.4 supplies P_lin and halofit P(k, z).  The halo-model
estimate uses the Sheth-Tormen mass function and bias on CLASS's linear spectrum, NFW halos with Duffy+08 concentrations,
Moster+13 stellar masses, and this lane's gate radius (CFG3_common.gate_radius).

CHECKS
  K1 CONTROL: XR26's committed lensing numbers are reproduced by its own code: LCDM chi^2 = 10.1456 and pull -0.393 (8-400), the
     chain's headline amplitude 1.149178 (linear base) / 2.134361 (halofit), the phantom budget f* = 0.6182 / 0.1776.
  S1 [HEADLINE; load-bearing; MUTATE must fail] THE LINEAR WEB: with B = 1 on every linear mode (derived), Planck 2018's 8-400
     amplitude relative to its best fit is 1.0000, within 2 sigma of 1.011 +- 0.028; chi^2 as LCDM's.
  S2 (reported) GROWTH: the linear growth, f sigma_8(z) and S8 are LCDM's (CLASS's sigma_8 = XR26 K1's 0.8120): neutral on the mild
     S8 tension, not a solution.
  S3 (reported; an ESTIMATE) THE GATED REGIONS' NONLINEAR IMPRINT: halos of 1e10-1e13 Msun carry their galaxy's isolated Bose
     phantom out to the gate radius r_g(M, z), compensated there (no EFE: an upper bound), (a) added to LCDM's halo, or (b) with the
     halo's own dark mass displaced to r_g (mass conserved: the dark field must not sit in galaxies, CFG3_sparc S5).  Halo-model
     Delta P(k, z) -> R(L) on both bases -> the 8-400 amplitude.  Groups and clusters (M > 1e13) are taken at LCDM's totals (their
     required dark mass fills the answer's deficit: stated, not computed).
  S4 (reported; an estimate) COSMIC SHEAR: the same halo-model imprint (bracket b) on a KiDS-like source sample (n(z) ~ z^2
     exp[-(z/0.6)^1.5]), halofit base, with no EFE and with a representative in-region external field e = 0.01 / 0.03 a0 capping
     each phantom at r_e = v_f^2/e; the implied S8 read-off shift (C_l ~ S8^2.5 at l ~ 300).
PRE-DECLARED HYPOTHESES (written before the first run of this script):
  H1 K1 reproduces XR26 exactly (the same code).  EXPECT TRUE.
  H2 S1: amplitude 1.0000, pull -0.39 sigma, chi^2 10.15.  EXPECT TRUE (it is LCDM's by derivation).
  H3 S3: compensation keeps the gated regions' imprint on the 8-400 amplitude below Planck's 2 sigma in bracket (b) and below
     XR26's linear-base excess (+4.9 sigma) in bracket (a).  UNCERTAIN: the isolated phantom is large at Mpc radii (M_ph(<r) ~ r
     v_f^2/G) and z < 0.5 gated regions are big (r_g ~ 2-3 r_ta).
  H4 [added after the first development run showed B(z = 0, k = 1/Mpc) ~ 2 on the halofit base; disclosed] S4: with the
     in-region EFE the S8 shift stays below +5%; with none it exceeds it.  UNCERTAIN.
MUTATE=1: the vacuum answers all matter, including the expanding web (the gate removed): the web's MOND boost is XR26's own
headline B(k, z) (FP13's yardstick, the chain's web MOND) -- S1 must FAIL (1.149, +4.9 sigma), rc = 1.
Run from the repository root (MUTATE first):  MUTATE=1 python3 campaign_fresh_gravity/CFG3_web_lensing.py; python3 campaign_fresh_gravity/CFG3_web_lensing.py
"""
import os, sys, math, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG3_common as C
import numpy as np
from scipy.special import sici

R = C.Run("CFG3_web_lensing", __doc__)
P, check = R.P, R.check
if C.MUTATE:
    P("\n  *** MUTATE=1: the vacuum answers the expanding web too (no gate): B(k, z) = XR26's headline web MOND -- S1 must FAIL ***")

# ================================================================================================ K1
R.banner("K1  CONTROL: XR26's lensing pipeline (exec'd read-only) reproduces its committed numbers")
t1 = time.time()
XR26 = os.path.join(C.HUB, "XR26_cmb.py")
X, _ = C.exec_slices(XR26, [(None, "class _Tee:"),
                            ('OUT = {"lane": "XR26"', "P(__doc__.strip())"),
                            ("# ================================================================================================ inputs (published, committed)",
                             "# ================================================================================================ the patched CLASS"),
                            ('banner("K  CONTROLS', "cam = cres.get_cmb_power_spectra"),
                            ("# ---- FP13's (H_S) growth yardstick", "# ---- re-lensing with CAMB"),
                            ("# ================================================================================================ L late-time lensing",
                             "# L3/L4 the lensed spectra")], name="xr26_ro")
J26 = json.load(open(os.path.join(C.HUB, "XR26_cmb_results.json")))["numbers"]
HEAD = X["HEAD"]
L2x = X["L2"]["8-400"]
rows_c = J26["L2"]["8-400"]["rows"]
lin_now, nl_now = L2x["rows"][(HEAD, "lin")], L2x["rows"][(HEAD, "NL")]
lin_ref, nl_ref = rows_c[f"{HEAD} || lin"], rows_c[f"{HEAD} || NL"]
d_amp = max(abs(lin_now["amp"] - lin_ref["amp"]), abs(nl_now["amp"] - nl_ref["amp"]))
d_chi = max(abs(L2x["chi2_lcdm"] - J26["L2"]["8-400"]["chi2_lcdm"]), abs(lin_now["chi2"] - lin_ref["chi2"]))
d_f = max(abs(X["FSTAR"][b] - J26["L2b"]["f_star"][b]) for b in ("lin", "NL"))
P(f"    reproduced ({time.time() - t1:.0f} s): LCDM chi^2 {L2x['chi2_lcdm']:.4f} (committed {J26['L2']['8-400']['chi2_lcdm']:.4f}), pull "
  f"{L2x['pull_lcdm']:+.3f}; chain amplitude linear {lin_now['amp']:.6f} (committed {lin_ref['amp']:.6f}), halofit {nl_now['amp']:.6f} "
  f"(committed {nl_ref['amp']:.6f}); f* {X['FSTAR']['lin']:.4f} / {X['FSTAR']['NL']:.4f}")
check("K1 CONTROL: XR26's committed lensing numbers are reproduced by its own code (exec'd read-only): LCDM chi^2 and pull, the chain's "
      "headline amplitude on both bases, the phantom budget f*", f"max |d amp| {d_amp:.1e}, |d chi^2| {d_chi:.1e}, |d f*| {d_f:.1e}",
      d_amp < 1e-9 and d_chi < 1e-6 and d_f < 1e-9)
R.num("K1", dict(chi2_lcdm=L2x["chi2_lcdm"], pull_lcdm=L2x["pull_lcdm"], amp_chain_lin=lin_now["amp"], amp_chain_NL=nl_now["amp"]))

limber_pp, LIMB_FID, bandpowers, PL18_MV, LENS_AMP = X["limber_pp"], X["LIMB_FID"], X["bandpowers"], X["PL18_MV"], X["LENS_AMP"]
L_G, H_FID, IPLIN, IPNL, cl_fid = X["L_G"], X["H_FID"], X["IPLIN"], X["IPNL"], X["cl_fid"]


def amp_chi2(Rfun, rng="8-400"):
    dat = np.array([b_[2] * b_[4] for b_ in PL18_MV[rng]]); err = np.array([b_[3] * b_[4] for b_ in PL18_MV[rng]])
    bp_l = bandpowers(lambda ll: np.ones_like(ll, float), rng)
    bp_c = bandpowers(Rfun, rng)
    w = 1 / np.array([b_[3] for b_ in PL18_MV[rng]]) ** 2
    A = float(np.sum(w * bp_c / bp_l) / np.sum(w))
    return A, (A - LENS_AMP[rng][0]) / LENS_AMP[rng][1], float(np.sum(((dat - bp_c) / err) ** 2))


# ================================================================================================ S1
R.banner("S1  THE LINEAR WEB UNDER THE PRINCIPLE: the gate is closed on every linear mode (CFG3_principle D5), so B(k, z) = 1")
if C.MUTATE:
    Bweb = X["BFUN"][HEAD]
    Rw = {b: limber_pp(b, Bweb) / LIMB_FID[b] for b in ("lin", "NL")}
else:
    Rw = {b: np.ones_like(L_G, float) for b in ("lin", "NL")}
S1 = {}
for b in ("lin", "NL"):
    for rng in ("8-400", "8-2048"):
        A, pull, chi2 = amp_chi2(lambda ll, b=b: np.interp(ll, L_G, Rw[b]), rng)
        S1[f"{b}|{rng}"] = dict(amp=A, pull=pull, chi2=chi2)
        P(f"    {b:3s} base, {rng:7s}: amplitude {A:.4f} vs {LENS_AMP[rng][0]} +- {LENS_AMP[rng][1]} (pull {pull:+.2f} sigma), chi^2 {chi2:.2f} "
          f"({len(PL18_MV[rng])} bins)")
g1 = all(abs(S1[f"{b}|8-400"]["amp"] - LENS_AMP["8-400"][0]) <= 2 * LENS_AMP["8-400"][1] for b in ("lin", "NL"))
check("S1 [HEADLINE; MUTATE must fail] THE LINEAR WEB IS GR BY DERIVATION: the vacuum does not answer matter that expands faster than it "
      "(H > H_Lambda at every z), so B(k, z) = 1 on every linear mode and Planck 2018's conservative 8-400 lensing amplitude is LCDM's -- "
      "within 2 sigma of 1.011 +- 0.028 on both bases", "; ".join(f"{k}: {v['amp']:.4f} ({v['pull']:+.2f} sigma)" for k, v in S1.items()), g1)
R.num("S1", S1)

# ================================================================================================ S2
R.banner("S2  GROWTH")
s8 = float(cl_fid.sigma8()); om = float(cl_fid.Omega_m())
S8 = s8 * math.sqrt(om / 0.3)
fs8 = {}
for zz in (0.3, 0.5, 0.8, 1.0, 1.5):
    fs8[str(zz)] = float(cl_fid.scale_independent_growth_factor_f(zz) * cl_fid.sigma(8 / H_FID, zz))
P(f"    sigma_8 = {s8:.4f} (XR26 K1: CAMB 0.8120), S8 = {S8:.4f}; f sigma_8(z) = " + ", ".join(f"{k}: {v:.4f}" for k, v in fs8.items())
  + "  -- all LCDM's: the gate is closed on the linear web")
check("S2 (reported) GROWTH IS LCDM's: the linear growth equations are GR + the dark field, so sigma_8, S8 and f sigma_8(z) equal LCDM's at "
      "the Planck best fit -- neutral on the survey-S8 question (not a solution)", f"sigma_8 {s8:.4f}, S8 {S8:.4f}",
      abs(s8 - 0.8120) < 0.003, load_bearing=False)
R.num("S2", dict(sigma8=s8, S8=S8, fsigma8=fs8))

# ================================================================================================ S3
R.banner("S3  (reported; an estimate) THE GATED REGIONS' NONLINEAR IMPRINT, compensated phantoms in a halo model")
t3 = time.time()
RHOM = float(cl_fid.Omega_m()) * 2.775e11 * H_FID ** 2                   # Msun / Mpc^3 (comoving), P18
DC = 1.686
LMH = np.linspace(9.0, 16.0, 141)
MH = 10 ** LMH
KMOD = np.geomspace(1e-3, 8.0, 160)                                     # 1/Mpc
ZMOD = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
Rl = (3 * MH / (4 * math.pi * RHOM)) ** (1 / 3)
KI = np.geomspace(1e-4, 50.0, 3000)


def sigma_M(z):
    Pk = np.exp(IPLIN(min(z, 50.0), np.log(np.clip(KI, 1e-4, 19.0)), grid=False)) * (KI <= 19.0)
    x = KI[None, :] * Rl[:, None]
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return np.sqrt(C._trap(Pk[None, :] * W ** 2 * KI[None, :] ** 2, KI, axis=1) / (2 * math.pi ** 2))


def st_mf(z):
    s = sigma_M(z)
    nu = DC / s
    a_, p_, A_ = 0.707, 0.3, 0.3222
    f = A_ * math.sqrt(2 * a_ / math.pi) * (1 + (a_ * nu ** 2) ** (-p_)) * nu * np.exp(-a_ * nu ** 2 / 2)
    dlnnu = np.gradient(np.log(nu), np.log(MH))
    dndlnM = RHOM / MH * f * np.abs(dlnnu)
    b = 1 + (a_ * nu ** 2 - 1) / DC + 2 * p_ / (DC * (1 + (a_ * nu ** 2) ** p_))
    return dndlnM, b


def u_nfw(k, M, z):
    c200 = 5.71 * (M / (2e12 / H_FID)) ** (-0.084) * (1 + z) ** (-0.47)
    r200 = (3 * M / (4 * math.pi * 200 * RHOM)) ** (1 / 3)                   # comoving, 200 x mean
    rs = r200 / c200
    x = np.outer(k, rs)
    si1, ci1 = sici(x * (1 + c200)); si0, ci0 = sici(x)
    mc = np.log(1 + c200) - c200 / (1 + c200)
    return (np.sin(x) * (si1 - si0) - np.sin(c200 * x) / ((1 + c200) * x) + np.cos(x) * (ci1 - ci0)) / mc


# the gate-radius table (physical Mpc at z) on the halo grid used for the gated phantoms
GM_LM = np.arange(10.0, 13.01, 0.5)
RGT = np.zeros((len(ZMOD), len(GM_LM)))
for iz, zz in enumerate(ZMOD):
    for im, lm in enumerate(GM_LM):
        RGT[iz, im] = C.gate_radius(10 ** lm, zz)["r_g"]
P(f"    gate radius r_g [physical Mpc] (rows z = {ZMOD}; columns log M = {list(GM_LM)}):")
for iz, zz in enumerate(ZMOD):
    P(f"      z = {zz:4.2f}: " + " ".join(f"{v:6.3f}" for v in RGT[iz]))
P(f"    ({time.time() - t3:.0f} s)")


def phantom_ft(k, Mb, rg_c, z, a0, e_in=0.0):
    """compensated Bose phantom of baryonic mass Mb [Msun], gated out to comoving r_g: Fourier transform [Msun].  e_in > 0: an
    in-region external field e_in a0 (neighbours inside the same region) caps the phantom at r_e = v_f^2/(e_in a0) (the deep-MOND
    EFE radius; beyond it the enclosed phantom is held constant up to r_g -- an approximation of QUMOND's EFE fall-off)."""
    rr = np.geomspace(1e-5, 1.0, 400)[:, None] * rg_c[None, :]        # comoving Mpc
    rphys = rr / (1 + z) * C.MPC
    y = C.G_SI * Mb[None, :] * C.MSUN / rphys ** 2 / a0
    Mph = Mb[None, :] * (C.nu_bose(y) - 1)
    if e_in > 0:
        re = (C.G_SI * Mb * C.MSUN * a0) ** 0.5 / (e_in * a0)             # physical m
        Mcap = Mb * (C.nu_bose(C.G_SI * Mb * C.MSUN / re ** 2 / a0) - 1)
        Mph = np.where(rphys > re[None, :], Mcap[None, :], Mph)
    dM = np.diff(Mph, axis=0)
    rm = 0.5 * (rr[1:] + rr[:-1])
    kr = k[:, None, None] * rm[None, :, :]
    j0 = np.sinc(kr / math.pi)
    j0g = np.sinc(k[:, None] * rg_c[None, :] / math.pi)
    inner = np.einsum("krm,rm->km", j0, dM) + Mph[0][None, :] * 1.0      # the core below the first node (j0 ~ 1)
    return inner - Mph[-1][None, :] * j0g                              # minus the compensating shell at r_g


def delta_P(z, a0, mode, mb_fac=1.4, e_in=0.0):
    dndlnM, b = st_mf(z)
    sel = (LMH >= 10.0) & (LMH <= 13.0)
    Ms, dn, bb = MH[sel], dndlnM[sel], b[sel]
    lm = LMH[sel]
    Mb = mb_fac * C.mstar_of_mh(Ms, z)
    rg_phys = np.array([np.interp(l_, GM_LM, np.array([np.interp(z, ZMOD, RGT[:, j]) for j in range(len(GM_LM))])) for l_ in lm])
    rg_c = rg_phys * (1 + z)
    ph = phantom_ft(KMOD, Mb, rg_c, z, a0, e_in)                       # (k, M)
    dlnM = np.gradient(np.log(Ms))
    un = u_nfw(KMOD, Ms, z)
    if mode == "b":
        Md = Ms * (1 - C.OB_K / C.OM_K)
        ph = ph + Md[None, :] * (np.sinc(KMOD[:, None] * rg_c[None, :] / math.pi) - un)
    Bx = np.sum(dn[None, :] * bb[None, :] * ph / RHOM * dlnM[None, :], axis=1)
    P1 = np.sum(dn[None, :] * (2 * Ms[None, :] * un * ph + ph ** 2) / RHOM ** 2 * dlnM[None, :], axis=1)
    Plin = np.exp(IPLIN(z, np.log(KMOD), grid=False))
    return Plin * (2 * Bx + Bx ** 2) + P1, Bx


S3 = {}
for foot in C.FOOTS:
    for mode in ("a", "b"):
        DPt = np.array([delta_P(zz, C.A0[foot], mode)[0] for zz in ZMOD])        # (z, k)
        for base, ip in (("lin", IPLIN), ("NL", IPNL)):
            Pb = np.array([np.exp(ip(zz, np.log(KMOD), grid=False)) for zz in ZMOD])
            ratio = 1.0 + DPt / Pb
            from scipy.interpolate import RectBivariateSpline as _RBS
            ib = _RBS(np.array(ZMOD), np.log(KMOD), ratio, kx=1, ky=1)
            Bf = (lambda ib_: (lambda k_h, z_: np.where(z_ > ZMOD[-1], 1.0, ib_(np.minimum(z_, ZMOD[-1]),
                                                                              np.log(np.clip(k_h * H_FID, KMOD[0], KMOD[-1])), grid=False))))(ib)
            Rb = limber_pp(base, Bf) / LIMB_FID[base]
            A, pull, chi2 = amp_chi2(lambda ll, Rb=Rb: np.interp(ll, L_G, Rb))
            S3[f"{foot}|{mode}|{base}"] = dict(amp=A, pull=pull, chi2=chi2, R={str(L_): float(np.interp(L_, L_G, Rb)) for L_ in (100, 200, 400, 1000)},
                                               B_z0={str(kk): float(np.interp(math.log(kk), np.log(KMOD), ratio[0])) for kk in (0.1, 0.3, 1.0)})
            P(f"    {foot:9s} bracket ({mode}) {base:3s} base: amplitude {A:.4f} (pull {pull:+.2f} sigma), chi^2 {chi2:.2f}; R(100/400/1000) = "
              f"{S3[f'{foot}|{mode}|{base}']['R']['100']:.4f}/{S3[f'{foot}|{mode}|{base}']['R']['400']:.4f}/{S3[f'{foot}|{mode}|{base}']['R']['1000']:.4f}; "
              f"B(z=0; k = 0.1/0.3/1 /Mpc) = " + "/".join(f"{v:.3f}" for v in S3[f'{foot}|{mode}|{base}']['B_z0'].values()))
P(f"    ({time.time() - t3:.0f} s)")
ok_b = all(abs(S3[f"{f}|b|{b}"]["amp"] - LENS_AMP["8-400"][0]) <= 2 * LENS_AMP["8-400"][1] for f in C.FOOTS for b in ("lin", "NL"))
ok_a = all(S3[f"{f}|a|lin"]["amp"] < lin_ref["amp"] for f in C.FOOTS)
check("S3 (H3, reported; an estimate) THE GATED REGIONS' IMPRINT: compensated phantoms keep Planck's 8-400 amplitude within 2 sigma when the "
      "galaxy halos' dark mass is displaced (bracket b), and below XR26's linear-base excess when it is added (bracket a)",
      "; ".join(f"{k}: {v['amp']:.4f} ({v['pull']:+.2f})" for k, v in S3.items()), ok_b and ok_a, load_bearing=False)
R.num("S3", S3)

R.banner("S4  (reported; an estimate) THE SAME IMPRINT IN COSMIC SHEAR: a KiDS-like source sample, halofit base")
t4 = time.time()
ZS = np.linspace(0.01, 3.0, 300)
nz = ZS ** 2 * np.exp(-(ZS / 0.6) ** 1.5); nz /= C._trap(nz, ZS)
bgF = cl_fid.get_background()
_zb, _chib = bgF["z"][::-1], bgF["comov. dist."][::-1]
chiS = np.interp(ZS, _zb, _chib)
OMF = float(cl_fid.Omega_m()); H0M = 100 * H_FID / 299792.458
CHIQ = np.linspace(1.0, float(np.interp(2.9, _zb, _chib)), 900)
ZQ = np.interp(CHIQ, _chib, _zb)
Wq = np.array([C._trap(np.where(chiS > cq, nz * (chiS - cq) / chiS, 0.0), ZS) for cq in CHIQ]) * 1.5 * OMF * H0M ** 2 * CHIQ * (1 + ZQ)
ELL = np.array([100, 200, 300, 500, 1000, 2000])


def shear_cl(Bf=None):
    out = []
    for l_ in ELL:
        kk = (l_ + 0.5) / CHIQ
        Pv = np.exp(IPNL(ZQ, np.log(np.clip(kk, 1e-4, 19.0)), grid=False)) * (kk <= 19.0)
        if Bf is not None:
            Pv = Pv * Bf(kk, ZQ)
        out.append(C._trap(Wq ** 2 / CHIQ ** 2 * Pv, CHIQ))
    return np.array(out)


CL0 = shear_cl()
S4 = {}
for foot in C.FOOTS:
    for e_in in (0.0, 0.01, 0.03):
        DPt = np.array([delta_P(zz, C.A0[foot], "b", e_in=e_in)[0] for zz in ZMOD])
        Pb = np.array([np.exp(IPNL(zz, np.log(KMOD), grid=False)) for zz in ZMOD])
        from scipy.interpolate import RectBivariateSpline as _RBS
        ib = _RBS(np.array(ZMOD), np.log(KMOD), 1.0 + DPt / Pb, kx=1, ky=1)
        Bf = (lambda ib_: (lambda kk, zq: np.where(zq > ZMOD[-1], 1.0, ib_(np.minimum(zq, ZMOD[-1]), np.log(np.clip(kk, KMOD[0], KMOD[-1])), grid=False))))(ib)
        rat = shear_cl(Bf) / CL0
        dS8 = (float(np.interp(math.log(300), np.log(ELL), rat)) ** (1 / 2.5) - 1.0)     # C_l ~ S8^2.5 near l = 300
        S4[f"{foot}|e_in={e_in}"] = dict(ratio={str(int(l_)): float(r_) for l_, r_ in zip(ELL, rat)}, dS8_frac=dS8)
        P(f"    {foot:9s} bracket (b), in-region EFE e = {e_in:.2f} a0: C_l ratio at l = " + ", ".join(f"{int(l_)}: {r_:.3f}" for l_, r_ in zip(ELL, rat))
          + f"  -> an S8 read off at l = 300 would move by {100 * dS8:+.1f}%")
P(f"    ({time.time() - t4:.0f} s)")
check("S4 (reported; an estimate) COSMIC SHEAR: with a representative in-region external field (e = 0.01-0.03 a0, the neighbours inside the "
      "same region) the gated phantoms move a KiDS-like S8 read-off by less than +5%; with no EFE at all (the upper bound) the shift is printed",
      "; ".join(f"{k}: {100 * v['dS8_frac']:+.1f}%" for k, v in S4.items()),
      all(v["dS8_frac"] < 0.05 for k, v in S4.items() if not k.endswith("e_in=0.0")), load_bearing=False)
R.num("S4", S4)

R.banner("W  THE LEDGER")
R.ledger("WL1", "DERIVED", "the linear web is not answered (H > H_Lambda): B = 1 on every linear mode; Planck 8-400 amplitude " +
         f"{S1['lin|8-400']['amp']:.4f} (pull {S1['lin|8-400']['pull']:+.2f})", "S1")
R.ledger("WL2", "NEUTRAL", f"growth, sigma_8 = {s8:.4f}, S8 = {S8:.4f}: LCDM's", "S2")
R.ledger("WL3", "ESTIMATE", "compensated gated phantoms (no EFE, upper bound): amplitude " + "; ".join(
    f"{k} {v['amp']:.3f}" for k, v in S3.items()), "S3")
R.ledger("WL4", "AT RISK", "cosmic shear: the gated phantoms' small-scale imprint moves a KiDS-like S8 read-off by " + "; ".join(
    f"{k} {100 * v['dS8_frac']:+.1f}%" for k, v in S4.items()) + " (needs the in-region EFE computed, not assumed)", "S4")
sys.exit(R.finish())
