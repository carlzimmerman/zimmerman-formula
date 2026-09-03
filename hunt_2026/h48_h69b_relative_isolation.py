#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h48_h69b_relative_isolation.py -- HUNT ITEMS 48 and 69, the systematic that h48_h69_binary_galaxies.py identified
but could not close.
=================================================================================================================
WHY THIS SCRIPT EXISTS.  h48_h69_binary_galaxies.py measured the velocity dispersion of isolated 2MRS galaxy pairs
and found the framework's best case -- Milgrom's isolated deep-MOND two-body law -- to be a factor A = 1.74 +/- 0.06
BELOW the data, i.e. the framework would need 7.7x the K-band baryonic mass.  It flagged the leading systematic
itself: residual group contamination, and showed that the excess shrinks as the isolation reaches further down the
luminosity function (A = 1.99 in the far velocity shell, 1.51 in the near one).  But its isolation scan varied only
an ABSOLUTE veto radius (800, 1500, 2500 kpc) and found no movement at all.

The dwarf-pair work in h47_dwarf_pairs.py found the missing lever: what matters is the veto radius RELATIVE TO THE
PAIR'S OWN SEPARATION.  A fixed 1500 kpc veto is a 30x margin around a 50 kpc pair and a 1.5x margin around a
1000 kpc pair, so it barely isolates the wide pairs -- which dominate the sample by number.  On ALFALFA dwarf pairs,
tightening d_third > 2 r_p to d_third > 5 r_p moved the framework's amplitude from 1.79 +/- 0.20 to 1.12 +/- 0.29,
and moved LambdaCDM's from 1.37 to 1.04 with it.  This script applies the same criterion to the massive pairs, on
the same catalogue and with the same estimator, and asks whether the A = 1.74 headline survives it.

REPORTED WHICHEVER WAY IT LANDS.  If A stays at 1.74 under a five-fold tighter relative criterion, the offset is
real and item 48/69's liability stands as written.  If it falls toward 1, the published number is an upper limit
and the liability must be softened.

THE ANSWER, UP FRONT, AND IT IS NOT THE ONE THIS SCRIPT WAS WRITTEN EXPECTING.  The amplitude does NOT fall.  Across
relative criteria from 2 to 8 pair separations -- a four-fold tightening that cuts the sample from 4294 pairs to
1196 and the median separation from 270 to 104 kpc -- it sits at 1.76 to 1.99 and does not trend.  h48_h69's
A = 1.74 +/- 0.06 is CONFIRMED, not retired, and item 48/69's liability stands as written: the framework's own best
case under-predicts the velocity dispersion of well-isolated L* galaxy pairs by about 0.27 dex, which is a factor of
twelve in baryonic mass.  Over the same scan LambdaCDM's abundance-matched halos sit at 0.90 to 1.06, i.e. on their
own parameter-free prediction.  The dwarf-pair sample of item 47 behaved differently (its amplitude did fall toward
1 under the same criterion), and the tension between the two is recorded rather than explained away: at 2.6 sigma
it is as likely to be the dwarf sample's 53 pairs as a real mass dependence.

Both footings.  LambdaCDM (Moster+2013 + NFW) computed beside the framework.  Mutation controls.  Checks CAN fail.
Estimator, gravity laws and sample construction are lifted verbatim from h48_h69_binary_galaxies.py so that the two
scripts' amplitudes are directly comparable; only the isolation criterion differs.
"""
import sys, math, os
import numpy as np
from scipy.spatial import cKDTree
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(48690)
UPS_K = 0.6; MK_SUN = 3.28; H0_KMS = 67.4
CZ_LO, CZ_HI = 3000.0, 12000.0
RP_MAX = 1000.0
DV_MAX = 2000.0
V_ERR = 40.0
DV_ISO = 1000.0
E_N = 0.03
SEARCH_KPC = 4000.0          # how far out the nearest third galaxy is looked for
D3_FLOOR = 300.0             # kpc, the veto radius never drops below this however close the pair is

def unitvec(ra, de):
    ra = np.radians(ra); de = np.radians(de)
    return np.c_[np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)]
def ang_sep_deg(u, v):
    return np.degrees(2*np.arcsin(np.clip(np.linalg.norm(u - v, axis=-1)/2, 0, 1)))
def cmb_frame(ra, de, vhel):
    ra_r, de_r = np.radians(ra), np.radians(de)
    ra_gp, de_gp, l_ncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    sb = np.sin(de_r)*math.sin(de_gp) + np.cos(de_r)*math.cos(de_gp)*np.cos(ra_r - ra_gp)
    b = np.arcsin(np.clip(sb, -1, 1))
    y = np.cos(de_r)*np.sin(ra_r - ra_gp)
    x = np.sin(de_r)*math.cos(de_gp) - np.cos(de_r)*math.sin(de_gp)*np.cos(ra_r - ra_gp)
    l = l_ncp - np.arctan2(y, x)
    la, ba, amp = math.radians(264.021), math.radians(48.253), 369.82
    return vhel + amp*(np.sin(b)*math.sin(ba) + np.cos(b)*math.cos(ba)*np.cos(l - la))
def LK_from_mag(K, D_Mpc):
    return 10**(0.4*(MK_SUN - (K - 5*np.log10(D_Mpc*1e6) + 5)))

def v_rel_deepmond(M1, M2, a0):
    M1 = np.asarray(M1, float)*Msun; M2 = np.asarray(M2, float)*Msun
    Mt = M1 + M2; mu = M1*M2/Mt
    return np.sqrt((2/3.)*np.sqrt(G*a0)*(Mt**1.5 - M1**1.5 - M2**1.5)/mu)
def v_rel_newton(M1, M2, r_kpc):
    return np.sqrt(G*(np.asarray(M1, float) + np.asarray(M2, float))*Msun/(np.asarray(r_kpc, float)*kpc))
def v_rel_efe(M1, M2, r_kpc, eN):
    return math.sqrt(nu_s(eN))*v_rel_newton(M1, M2, r_kpc)
def v_rel_framework(M1, M2, r_kpc, a0, eN):
    return np.minimum(v_rel_deepmond(M1, M2, a0), v_rel_efe(M1, M2, r_kpc, eN))
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(logMh - logM1)
    return 10**logMh*2*N/(x**(-be) + x**ga)
_LMH = np.linspace(9.0, 15.5, 1301); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass(Mstar): return 10**np.interp(np.log10(np.asarray(Mstar, float)), _LMS, _LMH)
_RHO_C = 3*(H0_KMS*1e3/Mpc)**2/(8*math.pi*G)/Msun*(3.0857e22)**3
def nfw_enclosed(Mh, r_kpc):
    Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
    c = 10**(0.905 - 0.101*(np.log10(Mh*0.674) - 12.0))
    R200 = (3*Mh/(4*math.pi*200*_RHO_C))**(1/3.)*1000.0
    x = np.clip(r_kpc/R200, 1e-4, 5.0)
    m = lambda t: np.log1p(t) - t/(1 + t)
    return Mh*m(c*x)/m(c)
def sigma_pred(M1, M2, rp_kpc, law, a0=None, eN=E_N, nmc=400, seed=1):
    g = np.random.default_rng(seed)
    M1 = np.asarray(M1, float); M2 = np.asarray(M2, float); rp = np.asarray(rp_kpc, float)
    u = g.random((len(rp), nmc))
    r = rp[:, None]*np.exp(u*math.log(20.0))*1.0001
    w = 1.0/np.sqrt(np.maximum((r/rp[:, None])**2 - 1.0, 1e-6)); w /= w.sum(axis=1, keepdims=True)
    if law == "deepmond":   v2 = np.repeat((v_rel_deepmond(M1, M2, a0)**2)[:, None], nmc, axis=1)
    elif law == "efe":      v2 = v_rel_efe(M1[:, None], M2[:, None], r, eN)**2
    elif law == "framework": v2 = v_rel_framework(M1[:, None], M2[:, None], r, a0, eN)**2
    elif law == "newton":   v2 = v_rel_newton(M1[:, None], M2[:, None], r)**2
    elif law == "lcdm":
        v2 = G*(nfw_enclosed(halo_mass(M1)[:, None], r) + nfw_enclosed(halo_mass(M2)[:, None], r))*Msun/(r*kpc)
    else: raise ValueError(law)
    return np.sqrt(np.sum(w*v2, axis=1)/3.0)/1e3
def ml_sigma(dv, sig_shape=None, dvmax=DV_MAX, verr=V_ERR):
    dv = np.asarray(dv, float); n = len(dv)
    s = np.ones(n) if sig_shape is None else np.asarray(sig_shape, float)
    def nll(pars):
        lA, lf = pars
        A = math.exp(lA); f = 1/(1 + math.exp(-lf))
        sg = np.sqrt((A*s)**2 + verr**2)
        p = f*np.exp(-0.5*(dv/sg)**2)/(math.sqrt(2*math.pi)*sg) + (1 - f)/(2*dvmax)
        return -np.sum(np.log(np.maximum(p, 1e-300)))
    lAs = np.linspace(math.log(10.0), math.log(2000.0), 90) if sig_shape is None else np.linspace(math.log(0.15), math.log(8.0), 90)
    lfs = np.linspace(-4, 4, 41)
    best = (1e30, None)
    for lA in lAs:
        for lf in lfs:
            v = nll((lA, lf))
            if v < best[0]: best = (v, (lA, lf))
    lA0, lf0 = best[1]
    for _ in range(3):
        lf0 = min(np.linspace(lf0 - 1.0, lf0 + 1.0, 81), key=lambda x: nll((lA0, x)))
        lA0 = min(np.linspace(lA0 - 0.15, lA0 + 0.15, 81), key=lambda x: nll((x, lf0)))
    fine = np.linspace(lA0 - 0.30, lA0 + 0.30, 241)
    prof = np.array([min(nll((lA, lf)) for lf in np.linspace(lf0 - 0.8, lf0 + 0.8, 25)) for lA in fine])
    prof -= prof.min(); lA0 = fine[int(np.argmin(prof))]
    hi = fine[prof < 0.5]
    err_ln = (hi.max() - hi.min())/2 if len(hi) > 1 else float(np.diff(fine).mean())
    A = math.exp(lA0)
    return A, A*err_ln, 1 - 1/(1 + math.exp(-lf0))

# ====================================================================================================================
P("="*122); P("PART 1 -- rebuild the 2MRS isolated-pair sample of item 69, then re-isolate it RELATIVELY"); P("="*122)
d = np.genfromtxt(os.path.join(DATA, "2mrs_catalog.csv"), delimiter=",", names=True)
ok = np.isfinite(d["RAJ2000"]) & np.isfinite(d["Ktmag"]) & np.isfinite(d["cz"])
m_ra, m_de, m_K, m_cz = d["RAJ2000"][ok], d["DEJ2000"][ok], d["Ktmag"][ok], d["cz"][ok]
MX = unitvec(m_ra, m_de); MT = cKDTree(MX)
cz_cmb = cmb_frame(m_ra, m_de, m_cz)
info(f"2MRS galaxies with a cz and a Ks magnitude: {len(m_ra)}")

ang_max = math.degrees(RP_MAX/1000.0/(CZ_LO/H0_KMS))
cand = MT.query_pairs(2*math.sin(math.radians(ang_max)/2), output_type="ndarray")
ii, jj = cand[:, 0], cand[:, 1]
czm = (cz_cmb[ii] + cz_cmb[jj])/2; Dm = czm/H0_KMS
rp = np.radians(ang_sep_deg(MX[ii], MX[jj]))*Dm*1000.0
dv = cz_cmb[ii] - cz_cmb[jj]
sel = (np.abs(dv) < DV_MAX) & (czm > CZ_LO) & (czm < CZ_HI) & (rp < RP_MAX) & (rp > 10.0)
ii, jj, rp, dv, czm, Dm = ii[sel], jj[sel], rp[sel], dv[sel], czm[sel], Dm[sel]
L1 = LK_from_mag(m_K[ii], Dm); L2 = LK_from_mag(m_K[jj], Dm)
rok = (np.maximum(L1, L2)/np.minimum(L1, L2)) < 6.0
ii, jj, rp, dv, czm, Dm, L1, L2 = (a[rok] for a in (ii, jj, rp, dv, czm, Dm, L1, L2))
M1, M2 = UPS_K*L1, UPS_K*L2
info(f"candidate MAJOR close pairs before any isolation: {len(ii)}")

mid = MX[ii] + MX[jj]; mid /= np.linalg.norm(mid, axis=1)[:, None]
d3 = np.full(len(ii), np.inf)
for k in range(len(ii)):
    ang = min((SEARCH_KPC/1000.0)/max(Dm[k], 1e-6), 1.0)
    nb = MT.query_ball_point(mid[k], 2*math.sin(0.5*ang))
    best = np.inf
    for t in nb:
        if t == ii[k] or t == jj[k]: continue
        if abs(cz_cmb[t] - czm[k]) >= DV_ISO: continue
        s = 2*math.asin(min(np.linalg.norm(MX[t] - mid[k])/2, 1.0))*Dm[k]*1000.0
        if s < best: best = s
    d3[k] = best
info(f"nearest third 2MRS galaxy to the pair midpoint (|dv| < {DV_ISO:.0f} km/s), searched to {SEARCH_KPC:.0f} kpc:")
info(f"  median {np.median(np.minimum(d3, SEARCH_KPC)):.0f} kpc; "
     f"{100*np.mean(d3 > 1500):.0f}% of pairs have none inside 1500 kpc (item 69's own absolute criterion)")
info(f"  median of d3/r_p = {np.median(np.minimum(d3, SEARCH_KPC)/rp):.1f}; item 69's absolute 1500 kpc veto "
     f"corresponds to a RELATIVE margin of only {np.median(1500.0/rp):.1f} r_p at the median separation")

def mask_rel(f):
    return d3 > np.maximum(f*rp, D3_FLOOR)

P(""); P("-"*122)
info("THE SCAN.  Same catalogue, same estimator, same predictions; only the isolation criterion changes.")
info(f"{'F (d3 > F r_p)':>16} {'N':>6} {'med r_p':>9} {'log Mb':>8} {'sigma [km/s]':>16} {'A(deepMOND)':>15} "
     f"{'A(framework)':>15} {'A(LambdaCDM)':>15}")
SCAN = []
for f_ in (0.0, 1.0, 2.0, 3.0, 5.0, 8.0):
    m_ = mask_rel(f_) if f_ > 0 else np.ones(len(ii), bool)
    if m_.sum() < 60: continue
    rpx, dvx, m1x, m2x = rp[m_], dv[m_], M1[m_], M2[m_]
    s_, e_, f0 = ml_sigma(dvx)
    A_, eA_, _ = ml_sigma(dvx, sig_shape=sigma_pred(m1x, m2x, rpx, "deepmond", a0=A0["canonical"]))
    F_, eF_, _ = ml_sigma(dvx, sig_shape=sigma_pred(m1x, m2x, rpx, "framework", a0=A0["canonical"]))
    L_, eL_, _ = ml_sigma(dvx, sig_shape=sigma_pred(m1x, m2x, rpx, "lcdm"))
    SCAN.append(dict(f=f_, n=int(m_.sum()), rp=float(np.median(rpx)), s=s_, A=A_, eA=eA_, F=F_, eF=eF_,
                     L=L_, eL=eL_, mask=m_))
    lab = "none" if f_ == 0 else f"{f_:.0f}"
    info(f"{lab:>16} {int(m_.sum()):6d} {np.median(rpx):9.0f} {np.median(np.log10(m1x+m2x)):8.2f} "
         f"{s_:11.1f} +/-{e_:4.1f} {A_:10.2f} +/-{eA_:4.2f} {F_:10.2f} +/-{eF_:4.2f} {L_:10.2f} +/-{eL_:4.2f}")

first = SCAN[0]; last = SCAN[-1]
strict = [s for s in SCAN if s["f"] >= 5.0]
S5 = strict[0] if strict else last
iso = [s for s in SCAN if s["f"] >= 2.0]          # every genuinely isolated sample
As = [s["A"] for s in iso]; Ls = [s["L"] for s in iso]
A_PUB = 1.74                                       # h48_h69's published value on the absolute criterion
ck("48c 🔴 AGAINST THE HYPOTHESIS THIS SCRIPT WAS WRITTEN TO TEST -- the published headline of items 48/69 is NOT a "
   "selection effect.  Re-isolating relatively, with no third 2MRS galaxy inside 2 to 8 times the pair's own "
   "separation, does not move the amplitude: it sits at 1.8-2.0 with no trend while the sample shrinks four-fold "
   "and the median separation falls from 270 to 104 kpc.  A = 1.74 is CONFIRMED and the liability stands.  (For "
   "the ALFALFA dwarf pairs of item 47 the same criterion DID move it, from 1.79 to 1.12 +/- 0.29 -- a 2.6 sigma "
   "difference from this sample, recorded as unresolved)",
   max(As) - min(As) < 0.35 and abs(S5["A"] - A_PUB) < 5*S5["eA"] + 0.10,
   f"A(isolated deep-MOND) across F = 2, 3, 5, 8: " + ", ".join(f"{a:.2f}" for a in As) +
   f"; at F = 5 (N = {S5['n']}, median r_p = {S5['rp']:.0f} kpc) A = {S5['A']:.2f} +/- {S5['eA']:.2f}, "
   f"{abs(S5['A']-1)/S5['eA']:.0f} sigma above 1 and {(S5['A']/A_PUB-1)*100:+.0f}% from the published 1.74.  "
   f"The framework would need {S5['A']**4:.0f}x the K-band baryonic mass")
ck("48d AND LambdaCDM LANDS ON ITS OWN PREDICTION over the same scan, which is what makes 48c a statement about the "
   "framework rather than about the sample.  Abundance-matched NFW halos give A = 0.90-1.06 with no free parameter "
   "once the pairs are properly isolated, while the framework's best case needs a factor of two in velocity",
   all(abs(l - 1) < 0.20 for l in Ls),
   f"LambdaCDM A across F = 2, 3, 5, 8: " + ", ".join(f"{l:.2f}" for l in Ls) +
   f"; at F = 5, {S5['L']:.2f} +/- {S5['eL']:.2f} ({abs(S5['L']-1)/S5['eL']:.1f} sigma from 1) against the "
   f"framework's {S5['A']:.2f} +/- {S5['eA']:.2f}")
info("")
info(f"what would close the framework's gap at F = 5?  A = {S5['A']:.2f} means {S5['A']**4:.0f}x the assumed "
     f"baryonic mass (v ~ M_b^1/4), i.e. Upsilon_K = {UPS_K*S5['A']**4:.1f} instead of {UPS_K}, which no stellar "
     f"population reaches; or gas {S5['A']**4 - 1:.0f} times the stellar mass, which L* early types do not have in "
     f"cold form; or a hot intra-pair medium, which is the one baryonic reservoir 2MRS cannot see and the one the "
     f"framework is entitled to ask for -- but a 1e12 Msun pair does not carry 1e13 Msun of hot gas either.")
info(f"the no-isolation row is printed for scale only -- it is a sample of group members, not of pairs, and its "
     f"A = {first['A']:.2f} is what an unfiltered catalogue gives.")
ck("48e 🔴 WHAT DOES NOT MOVE: the framework's own external-field branch.  Whatever the isolation, the "
   "quasi-Newtonian G_eff = nu(e_N)G prediction is far below the measured dispersion, so the framework needs these "
   "pairs to be on the ISOLATED deep-MOND branch -- which for L* pairs at hundreds of kpc means an external field "
   "far smaller than the large-scale-structure value.  This is the same finding as item 47's 47g, on a mass scale "
   "two decades higher",
   (S5["F"] - 1)/S5["eF"] > 3.0,
   f"framework with e_N = {E_N}: A = {first['F']:.2f} at no isolation and {S5['F']:.2f} +/- {S5['eF']:.2f} at "
   f"d3 > 5 r_p, {(S5['F']-1)/S5['eF']:.1f} sigma above 1")

# ---- both footings on the strict sample
P("")
mS = S5["mask"]
info(f"both footings on the d3 > {S5['f']:.0f} r_p sample (N = {S5['n']}, median r_p = {S5['rp']:.0f} kpc):")
FOOT = {}
for ft, a0 in A0.items():
    A_, eA_, fi_ = ml_sigma(dv[mS], sig_shape=sigma_pred(M1[mS], M2[mS], rp[mS], "deepmond", a0=a0))
    FOOT[ft] = (A_, eA_)
    info(f"  {ft:10}: A(isolated deep-MOND) = {A_:.2f} +/- {eA_:.2f} ({math.log10(A_):+.3f} dex), "
         f"interloper fraction {fi_:.2f}")
info("gas is still not counted in M_b (2MRS is K-band only).  Adding 20% of M* in gas raises the framework's "
     "prediction by 0.02 dex in velocity and moves A down by 5%; it cannot be the whole story either way.")

# ---- MUTATION CONTROLS
P(""); P("-"*122); P("MUTATION CONTROLS"); P("-"*122)
sc = rng.permutation(int(mS.sum()))
dv_scr = cz_cmb[ii[mS]] - cz_cmb[jj[mS]][sc]
keep_s = np.abs(dv_scr) < DV_MAX
s_r, _, f_r = ml_sigma(dv[mS])
s_s, _, f_s = ml_sigma(dv_scr[keep_s])
ck("M1 mutation control: scrambling which galaxy each pair member is paired with must drive the fitted PAIR "
   "fraction to the floor on the strict sample too, or the strict sample has no pairs left in it",
   (1 - f_s) < 0.6*(1 - f_r),
   f"pair fraction 1-f on the strict sample: real {1-f_r:.2f} (sigma {s_r:.0f} km/s) -> scrambled {1-f_s:.2f} "
   f"(sigma {s_s:.0f} km/s)")
A_t = ml_sigma(dv[mS], sig_shape=sigma_pred(M1[mS], M2[mS], rp[mS], "deepmond", a0=A0["canonical"]))[0]
A_x = ml_sigma(dv[mS], sig_shape=sigma_pred(M1[mS], M2[mS], rp[mS], "deepmond", a0=100*A0["canonical"]))[0]
ck("M2 mutation control: a_0 x 100 must move the required amplitude by exactly 0.5 dex on the strict sample, or "
   "the amplitudes above are insensitive to the physics they claim to test",
   abs(math.log10(A_t/A_x) - 0.5) < 0.05,
   f"log10(A_true/A_x100) = {math.log10(A_t/A_x):+.3f}, predicted +0.500")
A_INJ, F_INJ = 1.50, 0.20
sp = sigma_pred(M1[mS], M2[mS], rp[mS], "deepmond", a0=A0["canonical"])
n_i = int(mS.sum()); is_int = rng.random(n_i) < F_INJ
dv_i = np.where(is_int, rng.uniform(-DV_MAX, DV_MAX, n_i), rng.normal(0, np.sqrt((A_INJ*sp)**2 + V_ERR**2)))
A_r, eA_r, f_i = ml_sigma(dv_i, sig_shape=sp)
ck("M3 injection-recovery control: mock velocity differences built from the same per-pair predictions with a known "
   "amplitude must come back with it.  A biased estimator would make the whole scan meaningless",
   abs(A_r - A_INJ) < 3*eA_r and abs(f_i - F_INJ) < 0.20,
   f"injected A = {A_INJ:.2f}, f_int = {F_INJ:.2f}; recovered A = {A_r:.2f} +/- {eA_r:.2f}, f_int = {f_i:.2f}")
# does the strict criterion just select LOW-dv pairs?  (it must not: it never looks at dv of the pair itself)
info("")
info("the relative criterion is blind to the pair's own dv by construction -- it looks only at THIRD galaxies -- "
     "but the check is worth making explicitly:")
for f_ in (0.0, 5.0):
    m_ = mask_rel(f_) if f_ > 0 else np.ones(len(ii), bool)
    info(f"  F = {f_:.0f}: median |dv| = {np.median(np.abs(dv[m_])):.0f} km/s, median r_p = {np.median(rp[m_]):.0f} "
         f"kpc, median log M_b = {np.median(np.log10(M1[m_]+M2[m_])):.2f}")
ck("M4 control: the strict sample must differ from the loose one in SEPARATION and not in baryonic mass, or the "
   "amplitude change is a mass effect rather than an isolation effect",
   abs(np.median(np.log10(M1[mS] + M2[mS])) - np.median(np.log10(M1 + M2))) < 0.15,
   f"median log M_b(pair): all {np.median(np.log10(M1+M2)):.2f} -> strict "
   f"{np.median(np.log10(M1[mS]+M2[mS])):.2f}; median r_p {np.median(rp):.0f} -> {np.median(rp[mS]):.0f} kpc")

P(""); P("-"*122)
info("WHAT THIS DOES AND DOES NOT SETTLE:")
info(" * it does NOT retire items 48/69's liability, which is what it set out to test.  The amplitude is stable")
info("   under a four-fold tightening of the isolation on the axis that matters, so the offset is not the loose")
info("   absolute veto's doing.  h48_h69's number stands and this script strengthens it.")
info(" * the SEPARATION between the two laws is the result: on well-isolated major pairs LambdaCDM's")
info("   abundance-matched halos need no adjustment and the framework's best case needs a factor of two in")
info("   velocity.  That is the sharpest negative these pair samples produce.")
info(" * it does NOT touch item 48b's other finding, that the KT2017 catalogue cannot be used at all because its")
info("   group-finder selects on the velocity difference being measured.  That stands.")
info(" * the framework's external-field branch remains excluded at both mass scales (item 47's 47g and 48e here).")
info("   That is a statement AGAINST the framework's own honest prediction, not for it: it forces the isolated")
info("   deep-MOND branch on pairs whose internal field is well below the large-scale-structure external field.")
info(" * THE UNRESOLVED CROSS-ITEM TENSION: item 47's ALFALFA dwarf pairs give A = 1.12 +/- 0.29 under the same")
info("   relative criterion where these major pairs give 1.89 +/- 0.05.  Either the dwarf sample's 53 pairs are")
info("   noise, or the offset grows with mass -- which would point at the baryons 2MRS cannot see (hot gas around")
info("   L* early types) rather than at gravity.  Deciding it needs an HI-complete major-pair sample.")
info(" * remaining systematics unchanged from h48_h69: 2MRS's depth (fainter companions are not vetoed), cz/H0")
info("   distances, Upsilon_K = 0.6 assumed, no gas in M_b, circular orbits assumed.  Every one of these except")
info("   the gas pushes the framework's requirement UP, not down.")
sys.exit(ck.done())
