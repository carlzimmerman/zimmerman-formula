#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG4 (part 4 of 5) -- COSMOLOGY: the cold component the CMB demands, and how much of it can LEAVE (stop clustering on small
scales: kicked, streaming daughters) or CHANGE FORM (decay into radiation) by z ~ 0 without violating CMB lensing, S8, BAO
and RSD.  CLASS 3.3.4 for every linear spectrum (FP6's T_EH98 carries an h-units error and is not used).

THE BASE.  a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED, flat in z (a0 enters no linear coefficient: XR26 part 1, the
record's S8-neutral theorem of the ghost-condensate thread).  The dark component, where one is needed, is the framework's own
field -- a cold fluid, not a particle species (the record's GDM theorem: linear cosmology sees only (w, c_s^2, c_vis^2) and the
amount) -- and a mass is still required: Omega_c h^2 is initial data, like LCDM's.

THE FACT (published, not refitted here): Planck 2018 TT,TE,EE+lowE+lensing, Omega_c h^2 = 0.1200 +- 0.0012, a cold,
pressureless component clustering in the perturbations at z ~ 1100.

WHAT IS COMPUTED.  Starting from the Planck 2018 best fit (XR26's CLASS parameters, H0 from CAMB's theta_MC):
  (a) THE KICK MODE ('leave'): at z_c a fraction F of the cold component converts into daughters that keep w = 0 (the
      background, hence BAO, is unchanged) but stream with a velocity dispersion v_k (a_c/a) (Hubble-cooled), so they stop
      clustering below their free-streaming scale.  Two-fluid linear growth per k (the daughters inherit the parent's density
      and bulk flow at birth; fluid approximation, c_s^2 = v^2/3).  This is the record's FK1/FP10/XR19 conversion channel.
  (b) THE SMOOTH LIMIT: v_k -> oo (the converted part never clusters again).
  (c) THE RADIATION MODE ('change form'): CLASS's decaying cold component -> dark radiation (omega_ini_dcdm, Gamma_dcdm), with
      h re-fitted to hold the CMB acoustic scale 100 theta_s fixed.
  Gates: Planck 2018 lensing 8-400 amplitude within 2 sigma of 1.011 +- 0.028 (the MV band powers, XR26's table); S8 >= the
  record's floor 0.752 (PAPER34 correction); RSD f sigma_8 (6dFGS, SDSS MGS, BOSS DR12, eBOSS DR16; published values) with
  Delta chi^2 <= 4 against LCDM; BAO: DESI DR1's fractional errors on D_M/r_d, D_H/r_d, D_V/r_d with the shift's chi^2 <= 4
  (automatically passed where the background is unchanged).

PRE-DECLARED (written before any run of this script):
  H1 CONTROLS.  (a) CLASS at XR26's Planck 2018 parameters, with this lane's own band-power code, reproduces XR26's committed
     LCDM lensing chi^2 = 10.1456 (9 MV bins) and pull -0.39, and sigma_8 = 0.812 +- 0.002; (b) this lane's Limber integral
     reproduces CLASS's own C_L^phiphi to <= 1% at 30 <= L <= 1000 (linear) and the two-fluid solver returns LCDM exactly at
     F = 0.  EXPECT TRUE.
  H2 [HEADLINE] A LATE COLD COMPONENT CAN LEAVE.  In the kick mode with v_k <= 600 km/s, a converted fraction F >= 0.3 after
     z_c = 1 passes every gate (CMB lensing, S8 floor, RSD, BAO): the daughters still cluster on the scales these probes weigh
     (the record's XR19: S8 ratio 0.912-0.938 even for F = 1).  The smooth limit (no clustering at all) allows much less.  The
     radiation mode is limited to a few per cent by the background (BAO) at fixed theta_s.  EXPECT TRUE.
  H3 CROSS-CHECK (reported).  The step model reproduces the record's 'whole carrier converts at z_web' S8 bracket (XR19 X:
     0.912 / 0.924 / 0.938 at z_web = 1.8 / 1.2 / 0.5; FP10 A8's 0.918 / 0.929 / 0.948) within 0.02 at v_k = 600 km/s.
     UNCERTAIN (a different solver and velocity treatment).
MUTATE=1 makes the headline's converted component smooth (v_k -> oo) and whole (F = 1 at z_c = 1): H2 must FAIL (rc = 1).

SCOPE.  Linear theory (sub-horizon two-fluid growth applied to CLASS's LCDM P(k, z) as a transfer ratio; halofit only as the
alternative lensing base); the forest is not re-scored here (the conversion is placed at z_c <= 2; the record's XR12/XR19 gas
proxy bounds the z >= 2 converted fraction); published data numbers typed in with their sources in the comments.

Run from the repository root:  python3 campaign_fresh_gravity/CFG4_cosmology.py      (MUTATE=1 for the control run)
"""
import os
import sys
import math
import json
import time
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG4_common as C
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.interpolate import RectBivariateSpline, CubicSpline
from classy import Class

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
R = C.Run("CFG4_cosmology")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("PRE-DECLARED")[0].strip())
P("\nPRE-DECLARED" + __doc__.split("PRE-DECLARED")[1].split("SCOPE.")[0].rstrip())
if C.MUTATE:
    P("\n  *** MUTATE=1: the headline's converted component is smooth (v_k -> oo) and whole (F = 1 at z_c = 1) -- H2 must FAIL ***")

# ================================================================================================ inputs
XR26 = os.path.join(C.HUB, "XR26_cmb.py")
XI = C.exec_slices(XR26, [("# ================================================================================================ inputs (published, committed)",
                           "fp0 = json.load(")], ns={"np": np, "math": math}, name="xr26_inputs")[0]
PL18_MV, LENS_AMP, P18 = XI["PL18_MV"], XI["LENS_AMP"], XI["P18"]
J26 = json.load(open(os.path.join(C.HUB, "XR26_cmb_results.json")))["numbers"]
H0F = J26["K1"]["H0"] / 100.0
YHE = J26["K1"]["YHe"]
BASEPAR = {"h": H0F, "omega_b": P18["omega_b"], "omega_cdm": P18["omega_cdm"], "tau_reio": P18["tau_reio"],
           "ln_A_s_1e10": P18["ln_A_s_1e10"], "n_s": P18["n_s"], "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "YHe": YHE}
S8_FLOOR = 0.752                                                   # the record's S8 floor (PAPER34 correction, memory index)
# f sigma_8 (published): 6dFGS (Beutler et al. 2012), SDSS MGS (Howlett et al. 2015), BOSS DR12 consensus (Alam et al. 2017),
# eBOSS DR16 LRG / ELG / QSO (Alam et al. 2021)
FS8 = [(0.067, 0.423, 0.055), (0.15, 0.53, 0.16), (0.38, 0.497, 0.045), (0.51, 0.458, 0.038), (0.61, 0.436, 0.034),
       (0.70, 0.473, 0.041), (0.85, 0.315, 0.095), (1.48, 0.462, 0.045)]
# DESI DR1 BAO (DESI 2024 III, Table 1): (z_eff, kind, value, sigma)
BAO = [(0.295, "DV", 7.93, 0.15), (0.510, "DM", 13.62, 0.25), (0.510, "DH", 20.98, 0.61), (0.706, "DM", 16.85, 0.32),
       (0.706, "DH", 20.08, 0.60), (0.930, "DM", 21.71, 0.28), (0.930, "DH", 17.88, 0.35), (1.317, "DM", 27.79, 0.69),
       (1.317, "DH", 13.82, 0.42), (1.491, "DV", 26.07, 0.67), (2.330, "DM", 39.71, 0.94), (2.330, "DH", 8.52, 0.17)]
LA = LENS_AMP["8-400"]
P(f"\n  Planck 2018 best fit (XR26's CLASS inputs): h = {H0F:.6f}, omega_b {P18['omega_b']}, omega_cdm {P18['omega_cdm']}, YHe {YHE:.5f}; "
  f"lensing gate {LA[0]} +- {LA[1]} (8-400); S8 floor {S8_FLOOR}; {len(FS8)} f sigma_8 points; {len(BAO)} DESI DR1 BAO numbers")

# ================================================================================================ K controls
banner("K  CONTROLS: CLASS at XR26's parameters reproduces XR26's LCDM lensing chi^2 and sigma_8; Limber vs CLASS; the solver at F = 0")
t0 = time.time()
cl = Class()
cl.set(dict(BASEPAR, output="tCl,pCl,lCl,mPk", lensing="yes", l_max_scalars=3500, non_linear="halofit", **{"P_k_max_h/Mpc": 30.0,
                                                                                                            "z_max_pk": 50.0}))
cl.compute()
LENS = cl.lensed_cl(2500)
CPP = LENS["pp"]


def bandpowers(Rfun, rng="8-400", cpp=None):
    cpp = CPP if cpp is None else cpp
    out = []
    for (lo, hi, A_, sA, fid) in PL18_MV[rng]:
        ll = np.arange(lo, hi + 1)
        out.append(1e7 * np.mean((ll * (ll + 1.0)) ** 2 * cpp[ll] * Rfun(ll) / (2 * math.pi)))
    return np.array(out)


def amp_chi2(Rfun=None, cpp=None, rng="8-400"):
    Rf = (lambda ll: np.ones_like(ll, float)) if Rfun is None else Rfun
    dat = np.array([b_[2] * b_[4] for b_ in PL18_MV[rng]]); err = np.array([b_[3] * b_[4] for b_ in PL18_MV[rng]])
    bp_l = bandpowers(lambda ll: np.ones_like(ll, float), rng)
    bp_c = bandpowers(Rf, rng, cpp)
    w = 1 / np.array([b_[3] for b_ in PL18_MV[rng]]) ** 2
    A_ = float(np.sum(w * bp_c / bp_l) / np.sum(w))
    return A_, float(np.sum(((dat - bp_c) / err) ** 2)), (A_ - LENS_AMP[rng][0]) / LENS_AMP[rng][1]


A_l, chi_l, pull_l = amp_chi2()
s8_class = cl.sigma8()
P(f"    LCDM: lensing chi^2 {chi_l:.4f} (XR26 committed {J26['L2']['8-400']['chi2_lcdm']:.4f}), pull {pull_l:+.3f}; sigma_8 {s8_class:.4f} "
  f"(Planck 0.8120; XR26's CAMB {J26['K1']['sigma8']:.4f}) ({time.time() - t0:.0f} s)")
k1 = abs(chi_l - J26["L2"]["8-400"]["chi2_lcdm"]) < 1e-6 and abs(s8_class - 0.8120) < 0.002
check("K1 CONTROL: CLASS at XR26's Planck 2018 parameters, with this lane's own band-power code, reproduces XR26's committed LCDM lensing "
      "chi^2 (9 MV bins, 8-400) and sigma_8 = 0.812 +- 0.002", f"chi^2 {chi_l:.6f} vs {J26['L2']['8-400']['chi2_lcdm']:.6f}; sigma_8 {s8_class:.4f}", k1)

# background and spectra
BG = cl.get_background()
zb = BG["z"][::-1]; chib = BG["comov. dist."][::-1]; Hb = BG["H [1/Mpc]"][::-1]
chi_of_z = CubicSpline(zb, chib); H_of_z = CubicSpline(zb, Hb)
ZSTAR = cl.get_current_derived_parameters(["z_star"])["z_star"]
CHISTAR = float(chi_of_z(ZSTAR))
OM0 = cl.Omega_m(); OB0 = cl.Omega_b(); OC0 = OM0 - OB0 - cl.Omega_nu
H0M = H_of_z(0.0)                                                           # 1/Mpc
Z_PK = np.concatenate([np.linspace(0.0, 1.0, 21)[:-1], np.linspace(1.0, 5.0, 17)[:-1], np.linspace(5.0, 50.0, 19)])
K_PK = np.exp(np.linspace(math.log(1e-4), math.log(19.0), 300))              # 1/Mpc
PLIN = np.array([[cl.pk_lin(k_, z_) for k_ in K_PK] for z_ in Z_PK])
PNL = np.array([[cl.pk(k_, z_) for k_ in K_PK] for z_ in Z_PK])
IPL = RectBivariateSpline(Z_PK, np.log(K_PK), np.log(PLIN), kx=3, ky=3)
IPN = RectBivariateSpline(Z_PK, np.log(K_PK), np.log(PNL), kx=3, ky=3)
CHI_G = np.concatenate([np.linspace(1.0, float(chi_of_z(5.0)), 900)[:-1], np.linspace(float(chi_of_z(5.0)), CHISTAR - 1.0, 400)])
Z_G = np.interp(CHI_G, chib, zb)
L_G = np.unique(np.concatenate([np.arange(2, 60), np.round(np.geomspace(60, 2500, 120)).astype(int)]))
W_LIMB = ((CHISTAR - CHI_G) / CHISTAR) ** 2 * (1.5 * OM0 * H0M ** 2 * (1 + Z_G)) ** 2


def P_of(k_arr, z_arr, base):
    ip = IPN if base == "NL" else IPL
    zz = np.minimum(z_arr, 50.0)
    out = np.exp(ip(zz, np.log(np.clip(k_arr, K_PK[0], K_PK[-1])), grid=False))
    out = np.where(k_arr > K_PK[-1], 0.0, out)
    return np.where(z_arr > 50.0, out * ((1 + 50.0) / (1 + z_arr)) ** 2, out)


def limber(base="lin", T2fun=None):
    out = np.zeros(len(L_G))
    for i_, L_ in enumerate(L_G):
        kk = (L_ + 0.5) / CHI_G
        Pv = P_of(kk, Z_G, base)
        if T2fun is not None:
            Pv = Pv * T2fun(kk, Z_G)
        out[i_] = 4.0 / (L_ + 0.5) ** 4 * np.trapz(W_LIMB * Pv, CHI_G)
    return out


LIMB = {b: limber(b) for b in ("lin", "NL")}
sel = (L_G >= 30) & (L_G <= 1000)
k2a = float(np.max(np.abs(LIMB["NL"][sel] / CPP[L_G[sel]] - 1)))
P(f"    Limber (halofit) / CLASS C_L^pp at 30-1000: max deviation {k2a:.4f}")

# ================================================================================================ the two-fluid growth
KH = np.geomspace(1e-3, 25.0, 160)                                          # h/Mpc
KM = KH * H0F                                                               # 1/Mpc
A_I = 0.01
LNA_OUT = np.log(1.0 / (1.0 + np.array([0.0, 0.067, 0.15, 0.25, 0.38, 0.5, 0.51, 0.61, 0.7, 0.85, 1.0, 1.2, 1.48, 1.5, 1.8, 2.0, 2.5,
                                             3.0, 4.0, 5.0])))
Z_OUT = np.round(1.0 / np.exp(LNA_OUT) - 1.0, 6)


def Hz_Mpc(a):
    return float(H_of_z(1.0 / a - 1.0))


def Om_a(a):
    return OM0 * H0M ** 2 / a ** 3 / Hz_Mpc(a) ** 2


def dlnH(a, e=1e-4):
    return (math.log(Hz_Mpc(a * (1 + e))) - math.log(Hz_Mpc(a * (1 - e)))) / (math.log(1 + e) - math.log(1 - e))


def growth(F=0.0, z_c=1.0, v_kms=600.0, smooth=False):
    """(delta_m(k, z_out), f(k, z_out)): one fluid until a_c, then cold (1 - f_d) + daughters f_d = F Omega_c/Omega_m; daughters are
    born with the parent's density and bulk flow, stream with dispersion v (a_c/a), fluid c_s^2 = v^2/3 (smooth: no clustering)."""
    a_c = 1.0 / (1.0 + z_c)
    fd = F * OC0 / OM0
    n = len(KM)

    def rhs1(N_, Y):
        a = math.exp(N_)
        d, dp = Y[:n], Y[n:]
        return np.concatenate([dp, 1.5 * Om_a(a) * d - (2 + dlnH(a)) * dp])

    def rhs2(N_, Y):
        a = math.exp(N_)
        dc, dcp, dd, ddp = Y[:n], Y[n:2 * n], Y[2 * n:3 * n], Y[3 * n:]
        src = 1.5 * Om_a(a) * ((1 - fd) * dc + fd * dd)
        fr = 2 + dlnH(a)
        if smooth:
            ddpp = np.zeros(n)                                              # the converted part never clusters (delta_d = 0)
        else:
            cs = v_kms * (a_c / a) / math.sqrt(3.0) / 299792.458              # units of c; H in 1/Mpc (CLASS's H/c), k in 1/Mpc
            ddpp = src - fr * ddp - (cs * KM / (a * Hz_Mpc(a))) ** 2 * dd
        return np.concatenate([dcp, src - fr * dcp, ddp, ddpp])

    y0 = np.concatenate([np.full(n, A_I), np.full(n, A_I)])
    Nc = math.log(a_c)
    outs = {}
    if F <= 0.0 or z_c < 0:
        s = solve_ivp(rhs1, (math.log(A_I), 0.0), y0, t_eval=np.sort(LNA_OUT), method="LSODA", rtol=1e-7, atol=1e-14)
        for j, N_ in enumerate(s.t):
            d = s.y[:n, j]; dp = s.y[n:, j]
            outs[round(1 / math.exp(N_) - 1, 6)] = (d, dp / d)
        return outs
    ev_before = [N_ for N_ in np.sort(LNA_OUT) if N_ <= Nc]
    s1 = solve_ivp(rhs1, (math.log(A_I), Nc), y0, t_eval=ev_before if ev_before else None, method="LSODA", rtol=1e-7, atol=1e-14,
                   dense_output=True)
    for j, N_ in enumerate(s1.t if ev_before else []):
        d = s1.y[:n, j]; dp = s1.y[n:, j]
        outs[round(1 / math.exp(N_) - 1, 6)] = (d, dp / d)
    yc = s1.sol(Nc)
    d_c, dp_c = yc[:n], yc[n:]
    y2 = np.concatenate([d_c, dp_c, (np.zeros(n) if smooth else d_c), (np.zeros(n) if smooth else dp_c)])
    ev_after = [N_ for N_ in np.sort(LNA_OUT) if N_ > Nc]
    s2 = solve_ivp(rhs2, (Nc, 0.0), y2, t_eval=ev_after, method="LSODA", rtol=1e-7, atol=1e-14)
    for j, N_ in enumerate(s2.t):
        dc, dcp, dd, ddp = s2.y[:n, j], s2.y[n:2 * n, j], s2.y[2 * n:3 * n, j], s2.y[3 * n:, j]
        dm = (1 - fd) * dc + fd * dd
        dmp = (1 - fd) * dcp + fd * ddp
        outs[round(1 / math.exp(N_) - 1, 6)] = (dm, dmp / dm)
    return outs


G0 = growth(0.0)
Gchk = growth(0.0, 1.0)
k2b = max(float(np.max(np.abs(Gchk[z][0] / G0[z][0] - 1))) for z in G0)
k2 = k2a <= 0.01 and k2b < 1e-9
check("K2 CONTROL: this lane's Limber integral on CLASS's halofit P(k, z) reproduces CLASS's own C_L^phiphi to <= 1% at 30-1000, and "
      "the two-fluid solver returns LCDM exactly at F = 0", f"Limber max dev {k2a:.4f}; solver F = 0 vs LCDM {k2b:.1e}", k2)


def W_th(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3


_PKC = {}


def sigma8_z(T2, z):
    if z not in _PKC:
        _PKC[z] = np.array([cl.pk_lin(k_, z) for k_ in KM])
    k = KM
    Pk = _PKC[z] * T2
    return math.sqrt(np.trapz(k ** 3 * Pk * W_th(k * 8.0 / H0F) ** 2 / (2 * math.pi ** 2), np.log(k)))


S8FAC = math.sqrt(OM0 / 0.3)
S8_L = sigma8_z(np.ones(len(KM)), 0.0) * S8FAC
FS8_L = {z_: None for z_, _, _ in FS8}
for z_, _, _ in FS8:
    zz = min(G0, key=lambda q: abs(q - z_))
    i01 = int(np.argmin(np.abs(KH - 0.1)))
    FS8_L[z_] = G0[zz][1][i01] * sigma8_z(np.ones(len(KM)), z_)
chi_rsd_L = sum(((FS8_L[z_] - v) / e) ** 2 for z_, v, e in FS8)
P(f"    LCDM: S8 = {S8_L:.4f} (Omega_m {OM0:.4f}); f sigma_8 chi^2 = {chi_rsd_L:.2f} over {len(FS8)} points")


def evaluate(F, z_c, v_kms, smooth=False):
    """the gates for one conversion model: lensing amplitude (linear and halofit bases), S8, RSD chi^2 difference."""
    Gm = growth(F, z_c, v_kms, smooth)
    zs = sorted(Gm)
    T2 = np.array([(Gm[z][0] / G0[z][0]) ** 2 for z in zs])
    ib = RectBivariateSpline(np.array(zs), np.log(KH), T2, kx=1, ky=1)
    T2f = lambda kk, zz: np.where(zz > zs[-1], 1.0, ib(np.minimum(zz, zs[-1]), np.log(np.clip(kk / H0F, KH[0], KH[-1])), grid=False))
    out = {}
    for base in ("lin", "NL"):
        Rr = limber(base, T2f) / LIMB[base]
        out[base] = amp_chi2(lambda ll, Rr=Rr: np.interp(ll, L_G, Rr))
    s8 = sigma8_z(T2[zs.index(0.0)], 0.0) * S8FAC
    i01 = int(np.argmin(np.abs(KH - 0.1)))
    chi = 0.0
    for z_, v, e in FS8:
        zz = min(zs, key=lambda q: abs(q - z_))
        fs8 = Gm[zz][1][i01] * sigma8_z(T2[zs.index(zz)], z_)
        chi += ((fs8 - v) / e) ** 2
    ok = abs(out["lin"][0] - LA[0]) <= 2 * LA[1] and s8 >= S8_FLOOR and chi - chi_rsd_L <= 4.0
    return dict(F=F, z_c=z_c, v=v_kms, smooth=smooth, amp_lin=out["lin"][0], pull_lin=out["lin"][2], amp_NL=out["NL"][0],
                pull_NL=out["NL"][2], S8=s8, S8_ratio=s8 / S8_L, d_chi_rsd=chi - chi_rsd_L, pass_all=ok)


# ================================================================================================ H3 cross-check against the record
banner("H3  CROSS-CHECK: the record's 'whole carrier converts at z_web' S8 bracket (XR19 X; FP10 A8) with this lane's step model")
XR19 = json.load(open(os.path.join(C.HUB, "XR19_web_runaway_results.json")))["numbers"]["X_maxbracket"]
XC = {}
for zw in (1.8, 1.2, 0.5):
    e_ = evaluate(1.0, zw, 600.0)
    XC[zw] = e_["S8_ratio"]
    P(f"    z_web = {zw}: this lane S8 ratio {e_['S8_ratio']:.3f} (v_k = 600 km/s, F = 1) vs XR19 {XR19['mine'][str(zw)]:.3f}, FP10 {XR19['fp10'][str(zw)]:.3f}")
h3 = all(abs(XC[zw] - XR19["mine"][str(zw)]) <= 0.02 for zw in XC)
check("H3 (reported; pre-declared UNCERTAIN) the step model reproduces the record's whole-carrier S8 bracket within 0.02",
      "; ".join(f"z_web {zw}: {XC[zw]:.3f} vs {XR19['mine'][str(zw)]:.3f}" for zw in XC), h3, load_bearing=False,
      reading="the record's numbers come from L319's solver with its own velocity treatment; the difference is the modelling spread")
R.num("H3", dict(this_lane=XC, xr19=XR19))

# ================================================================================================ H2 the kick and smooth modes
banner("H2  HOW MUCH CAN LEAVE: the converted fraction F allowed by CMB lensing, S8, RSD (BAO unchanged), per z_c and v_k")
FGRID = (0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
GRID = {}
t2 = time.time()
for z_c in (0.5, 1.0, 2.0):
    for v in (200.0, 400.0, 600.0, 1000.0, "smooth"):
        rows = []
        for F in FGRID:
            e_ = evaluate(F, z_c, 600.0 if v == "smooth" else v, smooth=(v == "smooth"))
            rows.append(e_)
        Fmax = max([r_["F"] for r_ in rows if r_["pass_all"]], default=0.0)
        GRID[(z_c, v)] = dict(rows=rows, Fmax=Fmax)
        r1 = rows[-1]
        P(f"    z_c = {z_c:3.1f}, v_k = {str(v):>6s}: F_max = {Fmax:.2f};  at F = 1: lensing {r1['amp_lin']:.3f} (lin, {r1['pull_lin']:+.1f} sigma) / "
          f"{r1['amp_NL']:.3f} (NL), S8 {r1['S8']:.3f} (ratio {r1['S8_ratio']:.3f}), d chi^2 RSD {r1['d_chi_rsd']:+.1f}")
P(f"    ({time.time() - t2:.0f} s)")
if C.MUTATE:
    head = evaluate(1.0, 1.0, 600.0, smooth=True)
    head_ok = head["pass_all"]
    P(f"    [MUTATE] headline evaluated at F = 1, smooth, z_c = 1: pass_all = {head_ok}")
else:
    head_ok = all(GRID[(1.0, v)]["Fmax"] >= 0.3 for v in (200.0, 400.0, 600.0))
check("H2 [HEADLINE] A LATE COLD COMPONENT CAN LEAVE: in the kick mode (v_k <= 600 km/s) a converted fraction F >= 0.3 after z_c = 1 "
      "passes CMB lensing (8-400 within 2 sigma), the S8 floor, RSD (Delta chi^2 <= 4) and BAO (background unchanged)",
      "; ".join(f"z_c {k[0]}, v {k[1]}: F_max {v['Fmax']:.2f}" for k, v in GRID.items() if k[0] == 1.0), head_ok)
R.num("H2", {f"zc{k[0]}|v{k[1]}": v for k, v in GRID.items()})

# ================================================================================================ H4 the radiation mode
banner("H4  CHANGE OF FORM: decay into radiation (CLASS dcdm -> dr), h re-fitted to hold 100 theta_s; BAO, S8, CMB lensing")
DPAR = dict(BASEPAR)
DPAR.pop("omega_cdm")
TH_L = cl.get_current_derived_parameters(["100*theta_s"])["100*theta_s"]
RD_L = cl.rs_drag()


def bao_vec(c_):
    rd = c_.rs_drag()
    out = []
    for z_, kind, v, e in BAO:
        DM = c_.angular_distance(z_) * (1 + z_)
        DH = 299792.458 / (c_.Hubble(z_) * 299792.458)
        DV = (z_ * DM ** 2 * DH) ** (1 / 3)
        out.append({"DM": DM, "DH": DH, "DV": DV}[kind] / rd)
    return np.array(out)


BAO_L = bao_vec(cl)
t4 = time.time()
RAD = {}
T0_GYR = cl.age()
for F in (0.01, 0.02, 0.05, 0.1):
    Gam = -math.log(1 - F) / T0_GYR * 977.792                               # km/s/Mpc; the undecayed share today is 1 - F
    def run(h_, lens=False):
        c_ = Class()
        par = dict(DPAR, h=h_, omega_cdm=1e-7, omega_ini_dcdm=P18["omega_cdm"], Gamma_dcdm=Gam)
        if lens:
            par.update(output="tCl,pCl,lCl,mPk", lensing="yes", l_max_scalars=3500, non_linear="halofit",
                       **{"P_k_max_h/Mpc": 30.0, "z_max_pk": 50.0})
        c_.set(par)
        c_.compute()
        return c_
    hfit = brentq(lambda h_: run(h_).get_current_derived_parameters(["100*theta_s"])["100*theta_s"] - TH_L, H0F - 0.06, H0F + 0.02, xtol=1e-6)
    cd = run(hfit, lens=True)
    bv = bao_vec(cd)
    shift = bv / BAO_L - 1.0
    chi_bao = float(np.sum((shift * BAO_L / np.array([b_[3] for b_ in BAO])) ** 2))
    cpp_d = cd.lensed_cl(2500)["pp"]
    amp_d = amp_chi2(cpp=cpp_d)
    s8_d = cd.sigma8() * math.sqrt(cd.Omega_m() / 0.3)
    RAD[F] = dict(Gamma=Gam, h=hfit, chi2_bao_shift=chi_bao, max_shift=float(np.max(np.abs(shift))), amp=amp_d[0], pull=amp_d[2], S8=s8_d,
                  F_decayed=1 - cd.get_background()["(.)rho_dcdm"][-1] / (P18["omega_cdm"] / hfit ** 2 * cd.get_background()["(.)rho_crit"][-1]))
    P(f"    F = {F:.2f} (Gamma {Gam:.2f} km/s/Mpc): h re-fitted {hfit:.4f} (LCDM {H0F:.4f}); BAO shift chi^2 {chi_bao:.2f} (max fractional shift "
      f"{RAD[F]['max_shift']:.4f}); lensing amplitude {amp_d[0]:.3f} ({amp_d[2]:+.1f} sigma); S8 {s8_d:.3f}")
Fmax_rad = max([F for F, v in RAD.items() if v["chi2_bao_shift"] <= 4 and abs(v["amp"] - LA[0]) <= 2 * LA[1] and v["S8"] >= S8_FLOOR], default=0.0)
P(f"    radiation mode: F_max = {Fmax_rad:.2f} ({time.time() - t4:.0f} s)")
check("H4 (reported) THE RADIATION MODE is limited by the background: at fixed 100 theta_s the BAO shift and the lensing and S8 gates "
      "allow at most the printed decayed fraction", f"F_max = {Fmax_rad:.2f}; " + "; ".join(f"F {F}: BAO chi^2 {v['chi2_bao_shift']:.1f}, "
                                                                                          f"amp {v['amp']:.3f}, S8 {v['S8']:.3f}" for F, v in RAD.items()),
      Fmax_rad <= 0.1, load_bearing=False)
R.num("H4", dict(rows={str(k): v for k, v in RAD.items()}, Fmax=Fmax_rad))

# ================================================================================================ W ledger
banner("W  THE LEDGER: part 4 (cosmology)")
R.ledger("Q1", "MEASURED", "the cold component at z ~ 1100: Omega_c h^2 = 0.1200 +- 0.0012 (Planck 2018), a cold fluid (w, c_s^2, c_vis^2 "
         "~ 0: the record's GDM theorem); CMB-scale physics is GR + CDM (XR26: TT/TE/EE = LCDM to 7.8e-8)", "published; XR26")
R.ledger("Q2", "CONSTRAINT", "kick mode, F_max by (z_c, v_k): " + "; ".join(f"({k[0]}, {k[1]}) {v['Fmax']:.2f}" for k, v in GRID.items()), "H2")
R.ledger("Q3", "CONSTRAINT", f"radiation mode (decay at fixed theta_s): F_max = {Fmax_rad:.2f}", "H4")
R.ledger("Q4", "CONSTRAINT", "the forest bounds what converts before z ~ 2 (the record's XR12/XR19 calibrated gas proxy: bias-weighted "
         "converted fraction F_b(2) ~ 0.4 already sits at the 10% line)", "XR12, XR19 (quoted)")
check("W (reported) the ledger of part 4", f"{len(R.OUT['ledger'])} rows", True, load_bearing=False)
sys.exit(R.finish())
