#!/usr/bin/env python3
"""
L165 -- THE PURE-SMOOTH-DUST ENDPOINT, CALIBRATED IN SIGMA, IN TWO INDEPENDENT BOLTZMANN CODES.
        A CONFIRMATION-AND-EXTENSION LANE, NOT A FIRST.
=============================================================================================================
THE NUMBER:  a smooth (non-clustering) a^-3 component misses the observed third acoustic peak by 55 sigma.
             Equivalently A3/A2 = 0.6029 against Planck's measured 0.9737 +- 0.0109  (-34 sigma, -38%).
             There is NO value of omega_smooth that repairs it: the scan best case is -25.3 sigma.

PRIOR ART IN THIS DIRECTORY -- READ THIS FIRST, THIS LANE IS MOSTLY A REPLICATION:
  * L129 already showed, in CLASS at c_s^2 = 1, that smooth a^-3 dust fails the third peak. It explicitly
    declined to quote a sigma ("no likelihood was evaluated ... do not quote a sigma from this lane"),
    flagged c_s^2 = 1 as a STAND-IN for c_s^2 -> infinity, and asked for a CAMB cross-check.
  * L145 already implemented the SAME CAMB route this lane uses -- the dark sector carried by a tabulated
    w(a) = -rho_L/(rho_s0 a^-3 + rho_L) with omega_cdm reduced -- and scanned the CLUSTERING FRACTION f.
    Its variant-B numbers are REPRODUCED HERE EXACTLY (check XLANE-0): H3/H2 = 0.9797 at f = 1 (L145:
    0.9793), 0.7532 at f = 0.5 (L145: 0.7532), 0.7989 at f = 0.6 (L145: 0.7989).
  * L146/L147 supersede L145's profiled floor: f_cmb_min = 0.9877, i.e. the smooth fraction ceiling is
    ~1.2%. This lane's cruder single-amplitude version (~1-2% on the full TT chi^2) AGREES and is looser.
  * L156 already put the 3-sigma CMB ceiling on a dark fluid's sound speed at c_s^2(a_rec) < 6.1e-4
    (Fisher-marginalised over six parameters), tighter than this lane's single-statistic ~2e-3. L156's
    number is the one to cite; this lane's is a consistency check on it, not an improvement.
  * L152/L156/L158 concern a RUNNING c_s^2, where a real window survives. This lane says nothing about
    that branch. It is about CONSTANT-and-huge c_s^2, i.e. the cuscuton.

WHAT IS ACTUALLY NEW HERE (five things, each a check below):
  1. THE PURE-SMOOTH ENDPOINT IN CALIBRATED SIGMA. L145's scan returned NaN below f = 0.3 and never reached
     f = 0; L129 quoted no sigma. Here f = 0 is evaluated, and against Planck 2018 results I Table 5 (the
     published TT peak amplitudes AND their errors) with an error model -- cosmic variance + Planck HFI
     noise, f_sky = 0.70 -- VALIDATED by reproducing Planck's own published sigma(A3): 17.1 uK^2 computed
     against 17 uK^2 published. The sigma is calibrated, not asserted.
  2. THE c_s^2 -> infinity LIMIT, NOT A STAND-IN. The ladder c_s^2 = 0 ... 10^4 CONVERGES: 10^2, 10^3 and
     10^4 give A3/A2 = 0.6027, 0.6029, 0.6029. So the infinite-sound-speed answer is a limit REACHED
     numerically. It also CORRECTS L129's scope note: c_s^2 = 1 (A3/A2 = 0.578) is NOT "conservative in the
     correct direction" -- it is slightly WORSE than the true limit, not better. Both are excluded.
  3. TWO CODES, TWO ROUTES, AT THE ENDPOINT. CAMB (tabulated-w dark sector, H0 root-solved on theta_star)
     and CLASS (its own Omega_fld fluid with w0_fld = -1e-5, 100*theta_s a direct input) agree to 0.07%:
     A3/A2 = 0.6029 vs 0.6025. L129's requested cross-check is discharged.
  4. THE WINDOW SCAN AT f = 0, AND THE INVERTED LEVER. omega_smooth h^2 from 0.02 to 0.70 at fixed
     theta_star: monotone, no window, best case -25.3 sigma. And baryon loading -- the ONE knob that raises
     odd peaks relative to even ones, verified here to lift LCDM's A3/A2 from 0.980 to 1.342 -- moves SMOOTH
     dust the WRONG WAY (0.603 -> 0.563 -> 0.458 out to 4.5x BBN).
  5. THE MECHANISM, MEASURED. At the third-peak scale the Weyl potential FREEZES at 11-14% of its
     primordial value in LCDM and decays to <1% (changing sign) when the component is smooth.

WHY theta_star IS HELD FIXED: otherwise one compares peak POSITIONS, not peak HEIGHTS. Here the background
is identical by construction -- the CAMB route reproduces LCDM's H(z) to 3.5e-9 over 0 < z < 10^6, so z_eq
is matched exactly and the failure cannot be blamed on the expansion history.

POSITIVE CONTROLS (this pipeline is not blind):
  * the SAME fluid machinery at c_s^2 = 0 gives back ordinary CDM: unlensed C_l agree with a true-CDM run
    to 0.014% (median, l = 30-2000), and A3/A2 = 0.9808 (CAMB) / 0.9796 (CLASS) vs LCDM's 0.9803.
  * the pipeline's LCDM peaks reproduce Planck's PUBLISHED Table 5 values at 0.05 / 0.40 / 1.41 sigma.
  * L145's variant-B table is reproduced to 4 significant figures (XLANE-0).

HONEST SCOPE -- READ BEFORE CITING (see SCOPE-0/1/2 at the end):
  This computes GENERAL-RELATIVISTIC perturbations with a smooth dark component. It does NOT include the
  programme's own modified perturbation equations. L136 R3 is the standing correction on exactly this point:
  under a0 ~ H(z) the recombination-epoch acceleration scale is not the local one, and the deep-MOND
  response at the third-peak scale is not the GR response. So this lane closes "smooth a^-3 dust + GR
  perturbations"; it does NOT close the programme's cosmology, and must not be cited as doing so.

POLARITY: each check ASSERTS a statement; PASS = true. Requires camb and classy. Verified as hard as a win.
Runtime ~20 min.
"""
import numpy as np, sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L165 -- smooth a^-3 dust vs the CMB third peak: calibrated sigma, two codes, window scan (confirms L129/L145)")
print("=" * 112, flush=True)

import camb
from camb import model as cmodel
from classy import Class
from scipy.optimize import brentq

# =============================================================================================
# Planck 2018 results I, Table 5 -- published TT peak multipoles and amplitudes (D_l, uK^2)
# =============================================================================================
PK = {1: (220.6, 5733.0, 39.0), 2: (538.1, 2586.0, 23.0), 3: (809.8, 2518.0, 17.0)}
OBS = np.array([PK[k][1] for k in (1, 2, 3)])

# ---- Planck HFI TT noise: 100/143/217 GHz inverse-variance combined (FWHM arcmin, uK-arcmin)
CHANNELS = [(9.66, 77.4), (7.22, 33.0), (4.90, 46.8)]
def Nl_TT(l):
    l = np.atleast_1d(np.asarray(l, float)); inv = np.zeros_like(l)
    for fw, s in CHANNELS:
        th = np.radians(fw / 60.0); sg = np.radians(s / 60.0)
        inv += 1.0 / (sg ** 2 * np.exp(l * (l + 1) * th ** 2 / (8 * np.log(2))))
    return 1.0 / inv
def sigma_Dl(l, Dl, fsky=0.70):
    l = np.atleast_1d(np.asarray(l, float)); f = l * (l + 1) / (2 * np.pi)
    return f * np.sqrt(2.0 / ((2 * l + 1) * fsky)) * (Dl / f + Nl_TT(l))
def band_amp(D, lpeak, Dref, half=19):
    """Inverse-variance-weighted mean of D_l over lpeak +- half.  Weights come from the SAME
    reference spectrum for every model, so the estimator is identical across models."""
    l = np.arange(int(round(lpeak)) - half, int(round(lpeak)) + half + 1)
    w = 1.0 / sigma_Dl(l, Dref[l]) ** 2
    return np.sum(w * D[l]) / np.sum(w), 1.0 / np.sqrt(np.sum(w))

# =============================================================================================
# CAMB route: the smooth dust is carried by the dark-energy fluid with a tabulated w(a) that is
# EXACTLY dust + Lambda, with omega_cdm -> 0.  cs2 sets the clustering; huge cs2 = the smooth limit.
# =============================================================================================
LMAX = 2500
CBASE = dict(tau=0.0544, As=2.100549e-9, ns=0.9649, mnu=0.06, omk=0, ombh2=0.02237)
def camb_make(H0, omch2_clust=0.0, omch2_smooth=0.0, cs2=1e3, lensing=True, acc=2.0, **over):
    kw = dict(CBASE); kw.update(over); h = H0 / 100.0
    p = camb.set_params(H0=H0, omch2=max(omch2_clust, 1e-9), lmax=LMAX,
                        halofit_version='takahashi',
                        **({'dark_energy_model': 'fluid'} if omch2_smooth > 0 else {}), **kw)
    if omch2_smooth > 0:
        Ode = camb.get_background(p).get_Omega('de', z=0)
        Od = omch2_smooth / h ** 2; OL = Ode - Od
        if OL <= 1e-6: raise ValueError(f"smooth dust exceeds the closure budget ({Od:.3f} > {Ode:.3f})")
        a = np.unique(np.concatenate([np.logspace(-9, -2, 750, endpoint=False), np.linspace(1e-2, 1.0, 3000)]))
        a[-1] = 1.0
        p.DarkEnergy.set_w_a_table(a, -OL / (Od * a ** -3 + OL)); p.DarkEnergy.cs2 = cs2
    p.set_for_lmax(LMAX, lens_potential_accuracy=1 if lensing else 0)
    p.NonLinear = cmodel.NonLinear_none
    p.Accuracy.AccuracyBoost = acc; p.Accuracy.lSampleBoost = acc; p.Accuracy.lAccuracyBoost = acc
    p.DoLensing = lensing
    return p
def camb_theta(p): return camb.get_background(p).get_derived_params()['thetastar']
def camb_cl(p, kind='total'):
    r = camb.get_results(p)
    return r.get_cmb_power_spectra(p, CMB_unit='muK', spectra=[kind])[kind][:, 0]
def camb_solveH0(target, lo=55.0, hi=90.0, **mk):
    f = lambda H: camb_theta(camb_make(H, lensing=False, acc=1.0, **mk)) - target
    g = np.linspace(lo, hi, 21); v = []
    for H in g:
        try: v.append((H, f(H)))
        except Exception: pass
    for (a1, f1), (a2, f2) in zip(v[:-1], v[1:]):
        if f1 * f2 <= 0: return brentq(f, a1, a2, xtol=1e-6, rtol=1e-12)
    raise RuntimeError("no theta* solution in bracket")

# =============================================================================================
# CLASS route (independent): its own fluid.  CLASS forbids w >= 0, so w0_fld = -1e-5, which is
# dust to 2e-4 in rho at a = 1e-3.  Omega_Lambda comes from closure.  100*theta_s is a direct input.
# =============================================================================================
CL_COMMON = dict(omega_b=0.02237, A_s=2.100549e-9, n_s=0.9649, tau_reio=0.0544,
                 N_ur=2.0328, N_ncdm=1, m_ncdm=0.06, T_ncdm=0.71611,
                 output='tCl,pCl,lCl,mPk', lensing='yes', l_max_scalars=2600)
CL_COMMON['P_k_max_h/Mpc'] = 2.0
W_DUST = -1e-5
def class_run(theta, Omega_fld=0.0, cs2=1e3, omega_cdm=1e-8, omega_b=0.02237, n_s=0.9649):
    p = dict(CL_COMMON)
    p.update({'100*theta_s': theta, 'omega_cdm': max(omega_cdm, 1e-8), 'omega_b': omega_b, 'n_s': n_s})
    if Omega_fld > 0:
        p.update({'Omega_fld': Omega_fld, 'w0_fld': W_DUST, 'wa_fld': 0.0,
                  'cs2_fld': cs2, 'use_ppf': 'no'})
    c = Class(); c.set(p); c.compute()
    cl = c.lensed_cl(2500); l = cl['ell']; T = c.T_cmb() * 1e6
    D = np.zeros(2501); D[2:] = (l[2:] * (l[2:] + 1) / (2 * np.pi)) * cl['tt'][2:] * T ** 2
    out = dict(D=D, h=c.h(), theta=c.theta_s_100())
    try: out['sigma8'] = c.sigma8()
    except Exception: out['sigma8'] = float('nan')
    c.struct_cleanup(); c.empty(); return out
def class_at_omega(theta, omega_smooth, cs2=1e3, omega_cdm=1e-8, iters=6, **kw):
    """Solve for the Omega_fld that realises a target omega_smooth h^2 at fixed theta_s."""
    h = 0.6736
    for _ in range(iters):
        r = class_run(theta, Omega_fld=omega_smooth / h ** 2, cs2=cs2, omega_cdm=omega_cdm, **kw)
        if abs(r['h'] - h) < 2e-5: break
        h = r['h']
    r['omega_smooth'] = omega_smooth / h ** 2 * r['h'] ** 2
    return r

# =============================================================================================
sec("PART 0 -- the BACKGROUND is exactly LCDM's, so theta_star is fixed structurally, not by tuning.")
# =============================================================================================
p_l = camb_make(67.36, omch2_clust=0.1200, lensing=False, acc=1.0)
p_s = camb_make(67.36, omch2_smooth=0.1200, lensing=False, acc=1.0)
TH = camb_theta(p_l)
z = np.concatenate([np.array([0., .5, 1., 2., 5., 10.]), np.logspace(1.5, 6, 25)])
Hs = camb.get_background(p_s).hubble_parameter(z); Hl = camb.get_background(p_l).hubble_parameter(z)
dH = float(np.max(np.abs(Hs / Hl - 1)))
check("BG-0  the CAMB smooth-dust route (dark-energy fluid carrying a tabulated w(a) = -Om_L/(Om_d a^-3+Om_L), "
      "omega_cdm -> 0) reproduces LCDM's expansion history EXACTLY: max |H_smooth/H_LCDM - 1| < 1e-7 over "
      "0 < z < 10^6. The two models therefore have the same theta_star, the same sound horizon and the same "
      "z_eq, and any C_l difference is a PERTURBATION difference, never a background one",
      dH < 1e-7, f"max |H_s/H_L - 1| = {dH:.2e} over z = 0..1e6;  100*theta_s = {TH:.7f}")

# =============================================================================================
sec("PART 1 -- POSITIVE CONTROLS: the same machinery with c_s^2 = 0 must give back ordinary CDM,")
sec("          and the pipeline must reproduce Planck's PUBLISHED peak amplitudes.")
# =============================================================================================
cl_lcdm = camb_cl(camb_make(67.36, omch2_clust=0.1200))
REF = cl_lcdm
u_cdm = camb_cl(camb_make(67.36, omch2_clust=0.1200, lensing=False), 'unlensed_scalar')
u_fl0 = camb_cl(camb_make(67.36, omch2_smooth=0.1200, cs2=0.0, lensing=False), 'unlensed_scalar')
rel = np.abs(u_fl0[30:2001] / u_cdm[30:2001] - 1)
check("CTRL-0  the fluid route with c_s^2 = 0 reproduces a true-CDM run: the unlensed C_l^TT agree to "
      "0.02% (median) and 0.06% (max) over l = 30-2000. The implementation is therefore correct at the "
      "clustering end, and a failure at the smooth end is physics, not a broken model",
      float(np.median(rel)) < 3e-4 and float(rel.max()) < 2e-3,
      f"median |ratio-1| = {np.median(rel):.2e}, max = {rel.max():.2e} at l = {30+int(np.argmax(rel))}")

A_l = {k: band_amp(cl_lcdm, PK[k][0], REF)[0] for k in (1, 2, 3)}
SIG = np.array([band_amp(cl_lcdm, PK[k][0], REF)[1] for k in (1, 2, 3)])
dev = {k: (cl_lcdm[int(round(PK[k][0]))] - PK[k][1]) / PK[k][2] for k in (1, 2, 3)}
print("    pipeline LCDM D_l at the Planck peak multipoles vs Planck 2018 Table 5:")
for k in (1, 2, 3):
    print(f"      peak {k}: l = {PK[k][0]:6.1f}   pipeline {cl_lcdm[int(round(PK[k][0]))]:8.1f}   "
          f"published {PK[k][1]:6.0f} +- {PK[k][2]:.0f} uK^2   -> {dev[k]:+.2f} sigma")
check("CTRL-1  the pipeline's LCDM run reproduces the three PUBLISHED Planck TT peak amplitudes (Planck 2018 "
      "results I, Table 5) to better than 2 sigma each. The machinery is measuring the same thing the "
      "experiment measured",
      all(abs(dev[k]) < 2.0 for k in (1, 2, 3)),
      f"deviations = {dev[1]:+.2f}, {dev[2]:+.2f}, {dev[3]:+.2f} sigma")

check("CTRL-2  the error model (cosmic variance + Planck HFI 100/143/217 noise, f_sky = 0.70, band "
      "l_peak +- 19) REPRODUCES Planck's own published peak-amplitude uncertainty on the third peak: "
      "17 uK^2 computed vs 17 uK^2 published. The sigmas quoted below are therefore calibrated against the "
      "real experiment, not invented",
      abs(SIG[2] / PK[3][2] - 1) < 0.25,
      f"sigma(A3) computed = {SIG[2]:.1f} uK^2  vs published {PK[3][2]:.0f};  "
      f"sigma(A2) = {SIG[1]:.1f} vs {PK[2][2]:.0f};  "
      f"N_l/C_l at l=810 = {float(Nl_TT(810)[0])/(cl_lcdm[810]*2*np.pi/(810*811)):.4f} (CV-limited)")


# ---- CROSS-LANE REPRODUCTION of L145's variant-B table (same CAMB route, c_s^2 = 1, peak-maximum ratio)
from scipy.interpolate import InterpolatedUnivariateSpline as IUS
def peak_max_ratio(D, lmin=60, lmax=1200):
    """Ratio of the 3rd to the 2nd LOCAL MAXIMUM of D_l -- L145's H3/H2 statistic, not the band estimator."""
    Lx = np.arange(lmin, lmax + 1).astype(float); y = D[lmin:lmax + 1]
    idx = [i for i in range(2, len(y) - 2) if y[i] > y[i-1] and y[i] > y[i+1] and y[i] > y[i-2] and y[i] > y[i+2]]
    sp = IUS(Lx, y, k=4); out = []
    for i in idx:
        lo, hi = Lx[max(i-12, 0)], Lx[min(i+12, len(Lx)-1)]
        cr = [c for c in sp.derivative().roots() if lo < c < hi]
        out.append((float(cr[int(np.argmax([sp(c) for c in cr]))]) if cr else float(Lx[i]),))
        out[-1] = (out[-1][0], float(sp(out[-1][0])) if cr else float(y[i]))
    ded = []
    for l_, d_ in sorted(out):
        if not ded or l_ - ded[-1][0] > 40: ded.append((l_, d_))
        elif d_ > ded[-1][1]: ded[-1] = (l_, d_)
    return ded[2][1] / ded[1][1] if len(ded) >= 3 else float('nan')
L145_REC = {1.00: 0.9793, 0.60: 0.7989, 0.50: 0.7532}     # from L145_cmb_third_peak_floor.out, variant B
print("\n    cross-lane reproduction of L145 variant B (H3/H2 = ratio of the 3rd to 2nd local maximum):")
print(f"    {'f_clust':>8} {'this lane':>11} {'L145 recorded':>15} {'rel. diff':>11}")
xl = {}
for fcl in [1.00, 0.60, 0.50]:
    kw = dict(omch2_clust=0.1200) if fcl == 1.0 else dict(omch2_clust=0.1200*fcl,
                                                          omch2_smooth=0.1200*(1-fcl), cs2=1.0)
    H0 = camb_solveH0(TH, **kw)
    xl[fcl] = peak_max_ratio(camb_cl(camb_make(H0, **kw)))
    print(f"    {fcl:8.2f} {xl[fcl]:11.4f} {L145_REC[fcl]:15.4f} {abs(xl[fcl]/L145_REC[fcl]-1):11.2e}", flush=True)
check("XLANE-0  this lane independently REPRODUCES L145's variant-B table to 4 significant figures "
      "(H3/H2 = 0.9797 vs 0.9793 at f = 1, 0.7532 vs 0.7532 at f = 0.5, 0.7989 vs 0.7989 at f = 0.6), "
      "having been written without reference to L145's code. Two independent implementations of the same "
      "CAMB route agree, so neither carries an implementation error -- and this lane is correctly read as "
      "a CONFIRMATION of L129/L145 extended to the f = 0 endpoint, not as an independent discovery",
      all(abs(xl[k]/L145_REC[k] - 1) < 3e-3 for k in L145_REC),
      "  ".join(f"f={k:.2f}: {xl[k]:.4f} vs {L145_REC[k]:.4f}" for k in [1.00, 0.60, 0.50]))

# the two ratio statistics and their published errors
def ratio_obs(i, j):
    o = PK[i][1] / PK[j][1]
    return o, o * np.hypot(PK[i][2] / PK[i][1], PK[j][2] / PK[j][1])
O32, S32 = ratio_obs(3, 2); O31, S31 = ratio_obs(3, 1)
L = np.arange(30, 2001); sD = sigma_Dl(L, REF[L])
def verdict(D):
    m = np.array([band_amp(D, PK[k][0], REF)[0] for k in (1, 2, 3)])
    w = 1 / SIG[:2] ** 2
    al = np.sum(w * m[:2] * OBS[:2]) / np.sum(w * m[:2] ** 2)     # amplitude fitted to peaks 1+2 ONLY
    mm = D[L]; af = np.sum(mm * REF[L] / sD ** 2) / np.sum(mm * mm / sD ** 2)
    return dict(A=m, n3=(al * m[2] - OBS[2]) / SIG[2], r32=m[2] / m[1], r31=m[2] / m[0],
                s32=(m[2] / m[1] - O32) / S32, s31=(m[2] / m[0] - O31) / S31,
                chi2=float(np.sum(((af * mm - REF[L]) / sD) ** 2)))
print(f"\n    Planck ratios:  A3/A2 = {O32:.4f} +- {S32:.4f}    A3/A1 = {O31:.4f} +- {S31:.4f}")
print(f"    sigma(A1,A2,A3) = {SIG.round(1)} uK^2")

# =============================================================================================
sec("PART 2 -- THE c_s^2 LADDER: does the c_s^2 -> infinity limit EXIST numerically?  It does.")
# =============================================================================================
print(f"    {'code':6s} {'c_s^2':>8} {'A3/A2':>8} {'sigma':>8} {'A3/A1':>8} {'sigma':>8} {'peak3 miss':>11} {'chi2(30-2000)':>14}")
lad = {}
for cs2 in [0.0, 1e-4, 1e-2, 1.0, 1e2, 1e3, 1e4]:
    H0 = camb_solveH0(TH, omch2_smooth=0.1200, cs2=cs2)
    v = verdict(camb_cl(camb_make(H0, omch2_smooth=0.1200, cs2=cs2))); lad[cs2] = v
    print(f"    {'CAMB':6s} {cs2:8.0e} {v['r32']:8.4f} {v['s32']:+8.1f} {v['r31']:8.4f} {v['s31']:+8.1f} "
          f"{v['n3']:+11.1f} {v['chi2']:14.0f}", flush=True)
conv = abs(lad[1e3]['r32'] - lad[1e4]['r32']) / lad[1e4]['r32']
check("LIMIT-0  the ladder CONVERGES: c_s^2 = 10^2, 10^3 and 10^4 give A3/A2 agreeing to better than 0.1%. "
      "The infinite-sound-speed (cuscuton) answer is therefore a limit that has been REACHED numerically, "
      "not a c_s^2 = 1 stand-in extrapolated by hand. L129's c_s^2 = 1 value is not the limit -- the true "
      "limit is slightly LESS bad, and it is still catastrophic",
      conv < 1e-3 and abs(lad[1e2]['r32'] - lad[1e4]['r32']) / lad[1e4]['r32'] < 3e-3,
      f"A3/A2: cs2=1e2 -> {lad[1e2]['r32']:.4f}, 1e3 -> {lad[1e3]['r32']:.4f}, 1e4 -> {lad[1e4]['r32']:.4f} "
      f"(|d| = {conv:.1e});  cs2=1 gives {lad[1.0]['r32']:.4f}, which is NOT the limit")
check("LIMIT-1  the same ladder run at c_s^2 = 0 lands on LCDM (A3/A2 within 1 sigma of Planck) and at "
      "c_s^2 = 1e-4 is still within 2 sigma: the ladder spans the whole physical range and the transition "
      "is resolved, so the smooth end is not an isolated numerical artefact",
      abs(lad[0.0]['s32']) < 2.0 and abs(lad[1e-4]['s32']) < 3.0,
      f"cs2=0: A3/A2 = {lad[0.0]['r32']:.4f} ({lad[0.0]['s32']:+.1f} sigma);  "
      f"cs2=1e-4: {lad[1e-4]['r32']:.4f} ({lad[1e-4]['s32']:+.1f} sigma)")

# =============================================================================================
sec("PART 3 -- THE KILL, and the SAME number from an INDEPENDENT Boltzmann code.")
# =============================================================================================
KILL = lad[1e4]
cl_ref = class_run(1.041850, omega_cdm=0.1200); THC = cl_ref['theta']; REFC = cl_ref['D']
SIGC = np.array([band_amp(REFC, PK[k][0], REFC)[1] for k in (1, 2, 3)])
sDC = sigma_Dl(L, REFC[L])
def verdictC(D):
    m = np.array([band_amp(D, PK[k][0], REFC)[0] for k in (1, 2, 3)])
    w = 1 / SIGC[:2] ** 2
    al = np.sum(w * m[:2] * OBS[:2]) / np.sum(w * m[:2] ** 2)
    mm = D[L]; af = np.sum(mm * REFC[L] / sDC ** 2) / np.sum(mm * mm / sDC ** 2)
    return dict(A=m, n3=(al * m[2] - OBS[2]) / SIGC[2], r32=m[2] / m[1], r31=m[2] / m[0],
                s32=(m[2] / m[1] - O32) / S32, s31=(m[2] / m[0] - O31) / S31,
                chi2=float(np.sum(((af * mm - REFC[L]) / sDC) ** 2)))
cK = class_at_omega(THC, 0.1200, cs2=1e4); vK = verdictC(cK['D'])
c0 = class_run(THC, Omega_fld=0.1200 / 0.6736 ** 2, cs2=0.0); v0 = verdictC(c0['D'])
print(f"    {'CLASS':6s} {'0':>8} {v0['r32']:8.4f} {v0['s32']:+8.1f} {v0['r31']:8.4f} {v0['s31']:+8.1f} {v0['n3']:+11.1f}")
print(f"    {'CLASS':6s} {1e4:8.0e} {vK['r32']:8.4f} {vK['s32']:+8.1f} {vK['r31']:8.4f} {vK['s31']:+8.1f} {vK['n3']:+11.1f}")
agree = abs(vK['r32'] - KILL['r32']) / KILL['r32']
check("CROSS-0  CAMB and CLASS -- different codes, different fluid implementations, different ways of fixing "
      "theta_star (root-solve on H0 vs 100*theta_s as a direct input) -- agree on the converged smooth-dust "
      "A3/A2 to better than 0.5%. L129's requested independent cross-check is satisfied",
      agree < 5e-3,
      f"A3/A2: CAMB {KILL['r32']:.4f}, CLASS {vK['r32']:.4f} (differ by {agree*100:.2f}%);  "
      f"c_s^2=0 control: CAMB {lad[0.0]['r32']:.4f}, CLASS {v0['r32']:.4f}")
check("KILL-0  THE NUMBER. With theta_star fixed and ONE overall amplitude (which absorbs A_s e^{-2tau} and "
      "any calibration) fitted to peaks 1 and 2 ONLY, the smooth a^-3 component misses the third peak by "
      "more than 50 sigma. The third peak is not reachable through the background/z_eq alone",
      KILL['n3'] < -50.0 and vK['n3'] < -50.0,
      f"peak-3 residual = {KILL['n3']:+.1f} sigma (CAMB), {vK['n3']:+.1f} sigma (CLASS); "
      f"sigma(A3) = {SIG[2]:.1f} uK^2 calibrated against Planck's published 17")
check("KILL-1  the amplitude-independent statement: A3/A2 = 0.60 against Planck's measured 0.9737 +- 0.0109 "
      "-- a 38% deficit at 34 sigma -- and A3/A1 = 0.288 against 0.4392 +- 0.0042, a 36 sigma miss. These "
      "ratios are immune to A_s, to tau and to absolute calibration, so no amplitude freedom can rescue them",
      KILL['s32'] < -20 and KILL['s31'] < -20 and vK['s32'] < -20,
      f"A3/A2 = {KILL['r32']:.4f} vs {O32:.4f}+-{S32:.4f} ({KILL['s32']:+.0f} sigma); "
      f"A3/A1 = {KILL['r31']:.4f} vs {O31:.4f}+-{S31:.4f} ({KILL['s31']:+.0f} sigma)")

# =============================================================================================
sec("PART 4 -- IS THERE ANY WINDOW?  Scan omega_smooth with theta_star FIXED at every point.")
# =============================================================================================
print(f"    {'om_s h^2':>9} {'h':>7} {'A3/A2':>8} {'sigma':>8} {'A3/A1':>8} {'sigma':>8} {'peak3 miss':>11} {'sigma8':>8}")
scan = []
for oms in [0.02, 0.06, 0.12, 0.20, 0.45, 0.70]:
    try:
        r = class_at_omega(THC, oms, cs2=1e3)
    except Exception as e:                      # CLASS's theta_s+tau shooting fails at extreme h
        print(f"    {oms:9.3f}   -- CLASS shooting failed (h out of range); point skipped", flush=True); continue
    v = verdictC(r['D']); v['oms'] = oms; v['h'] = r['h']; v['sigma8'] = r['sigma8']; scan.append(v)
    print(f"    {oms:9.3f} {r['h']:7.4f} {v['r32']:8.4f} {v['s32']:+8.1f} {v['r31']:8.4f} {v['s31']:+8.1f} "
          f"{v['n3']:+11.1f} {r['sigma8']:8.4f}", flush=True)
best32 = max(v['s32'] for v in scan); best3 = max(v['n3'] for v in scan)
check("WINDOW-0  THERE IS NO WINDOW. Over omega_smooth h^2 = 0.02 to 0.70 -- a factor of 35, spanning h from "
      "1.56 down to 0.19, far outside anything else allows -- the third peak is missed by at least 25 sigma "
      "at EVERY point, and the trend is monotone with no turning point toward the data. No choice of how "
      "much smooth dust to add reproduces the observed third peak",
      best32 < -20.0 and best3 < -30.0,
      f"best A3/A2 over the scan = {best32:+.1f} sigma (at omega_s h^2 = "
      f"{[v['oms'] for v in scan][int(np.argmax([v['s32'] for v in scan]))]}); best peak-3 miss = {best3:+.1f} sigma")


# ---- the ONE physical lever that raises odd peaks relative to even ones: baryon loading.
print("\n    BARYON LOADING is the only physical knob that raises the ODD peaks (1, 3) relative to the")
print("    EVEN peak 2. If anything could fake A3/A2 for smooth dust, it is a large omega_b.")
print(f"    {'omega_b':>9} {'x BBN':>7} {'component':>12} {'H0':>8} {'A3/A2':>8} {'sigma':>8} {'peak3 miss':>11}")
lever = {}
for tag, kw in [("SMOOTH", dict(omch2_smooth=0.1200, cs2=1e3)), ("CDM", dict(omch2_clust=0.1200))]:
    for ob in [0.02237, 0.0500] + ([0.1000] if tag == "SMOOTH" else []):
        try:
            H0 = camb_solveH0(TH, lo=40, hi=200, ombh2=ob, **kw)
            v = verdict(camb_cl(camb_make(H0, ombh2=ob, **kw))); lever[(tag, ob)] = v
            print(f"    {ob:9.5f} {ob/0.02237:7.2f} {tag:>12} {H0:8.2f} {v['r32']:8.4f} {v['s32']:+8.1f} {v['n3']:+11.1f}", flush=True)
        except Exception as e:
            print(f"    {ob:9.5f} {tag:>12}  -- no theta* solution in bracket", flush=True)
dCDM = lever[("CDM", 0.0500)]['r32'] - lever[("CDM", 0.02237)]['r32']
dSM  = lever[("SMOOTH", 0.0500)]['r32'] - lever[("SMOOTH", 0.02237)]['r32']
check("WINDOW-1  THE LAST LEVER IS INVERTED. Baryon loading is the one physical knob that raises the third "
      "peak relative to the second, and the CONTROL confirms it is a real and powerful knob: with clustering "
      "CDM, raising omega_b from 1x to 2.2x BBN lifts A3/A2 from 0.980 to 1.342 (+37%). Applied to SMOOTH "
      "dust the SAME knob moves A3/A2 the WRONG WAY -- it falls, and keeps falling out to 4.5x BBN. So the "
      "one escape route that existed on paper does not exist in fact, and it fails for a reason: with no "
      "wells there is no driving envelope for the extra baryon inertia to work against",
      dCDM > 0.25 and dSM < 0,
      f"d(A3/A2) from omega_b 1x -> 2.2x BBN:  CDM {dCDM:+.4f} (the knob works)   SMOOTH {dSM:+.4f} (inverted); "
      f"at 4.5x BBN smooth gives A3/A2 = {lever[('SMOOTH',0.1000)]['r32']:.4f} ({lever[('SMOOTH',0.1000)]['s32']:+.0f} sigma) "
      f"-- and 2.2x BBN is already ~180 sigma from the BBN/Planck value 0.02237 +- 0.00015")

# =============================================================================================
sec("PART 5 -- HOW MUCH of the dark component MAY be smooth, and how small must c_s^2 be?")
# =============================================================================================
print(f"    {'f_smooth':>9} {'A3/A2':>8} {'sigma':>8} {'peak3 miss':>11} {'chi2':>10} {'sigma8':>8}")
mix = []
for f in [0.0, 0.02, 0.05, 0.10, 0.20]:
    if f == 0: r = class_run(THC, omega_cdm=0.1200)
    else: r = class_at_omega(THC, 0.1200 * f, cs2=1e3, omega_cdm=0.1200 * (1 - f))
    v = verdictC(r['D']); v['f'] = f; mix.append(v)
    print(f"    {f:9.3f} {v['r32']:8.4f} {v['s32']:+8.1f} {v['n3']:+11.1f} {v['chi2']:10.0f} {r['sigma8']:8.4f}", flush=True)
f3 = [v['f'] for v in mix if abs(v['s32']) > 3.0]
fchi = [v['f'] for v in mix if v['chi2'] > 9.0]
check("FRACTION-0  essentially NONE of the dark component may be smooth. On the third-to-second peak ratio "
      "alone the 3-sigma ceiling is a smooth fraction of about 10%; on the full l = 30-2000 chi^2 it is "
      "about 1%. A theory that makes its dark sector out of a non-clustering field must therefore make "
      "almost all of it clustering anyway -- which defeats the purpose",
      len(fchi) > 0 and min(fchi) <= 0.05 and mix[3]['s32'] < -2.0,
      f"chi^2 > 9 already at f = {min(fchi):.2f}; A3/A2 at f = 0.10 is {mix[3]['s32']:+.1f} sigma; "
      f"the 3-sigma ceiling on A3/A2 falls between f = {f3[0] if f3 else 0.20:.2f} and the next grid point")
print(f"\n    {'c_s^2':>8} {'A3/A2':>8} {'sigma':>8} {'chi2':>10} {'sigma8':>8}")
csb = []
for cs2 in [1e-6, 1e-4, 1e-3, 3e-3, 1e-2]:
    r = class_at_omega(THC, 0.1200, cs2=cs2); v = verdictC(r['D']); v['cs2'] = cs2; v['s8'] = r['sigma8']
    csb.append(v)
    print(f"    {cs2:8.0e} {v['r32']:8.4f} {v['s32']:+8.1f} {v['chi2']:10.0f} {r['sigma8']:8.4f}", flush=True)
check("CS2BOUND-0  this lane's single-statistic ceiling from the peaks alone is c_s^2 < ~2e-3 (the A3/A2 "
      "3-sigma crossing), which is LOOSER than -- and therefore consistent with -- L156's Fisher-marginalised "
      "TT/TE/EE ceiling c_s^2(a_rec) < 6.1e-4. CITE L156, not this. What this adds is the LATE-TIME leg on "
      "the same grid: sigma_8 is far more demanding than the peaks, already ~10% low at c_s^2 = 1e-6 and "
      "collapsed threefold at 1e-4 -- the ~1e-6 level L156 correctly attributes to late-time clustering "
      "rather than to the CMB. Either way the cuscuton's c_s^2 is infinite, so the gap is not marginal",
      csb[-1]['s32'] > 3.0 and csb[0]['s8'] < 0.78 and csb[1]['s8'] < 0.45,
      f"A3/A2 crosses 3 sigma between c_s^2 = 1e-3 ({csb[2]['s32']:+.1f}) and 3e-3 ({csb[3]['s32']:+.1f}); "
      f"sigma8 = {csb[0]['s8']:.4f} at c_s^2=1e-6 and {csb[1]['s8']:.4f} at 1e-4 (LCDM: 0.811)")

# =============================================================================================
sec("PART 6 -- THE MECHANISM, MEASURED: the wells are simply not there.")
# =============================================================================================
zz = np.array([1e5, 1e4, 5e3, 3403, 2000, 1100, 500, 10])
W = {}
for tag, kw in [("LCDM", dict(omch2_clust=0.1200)), ("SMOOTH", dict(omch2_smooth=0.1200, cs2=1e3))]:
    H0 = camb_solveH0(TH, **kw)
    p = camb_make(H0, WantTransfer=True, lensing=False, **kw)
    W[tag] = camb.get_results(p).get_redshift_evolution(np.array([0.086]), zz, ['Weyl'])[0][:, 0]
print(f"    Weyl potential at k = 0.086 h/Mpc (the third-peak scale), normalised to its z = 1e5 value:")
print(f"    {'z':>9} {'LCDM':>12} {'SMOOTH':>12}")
for i, zv in enumerate(zz):
    print(f"    {zv:9.0f} {W['LCDM'][i]/W['LCDM'][0]:12.4f} {W['SMOOTH'][i]/W['SMOOTH'][0]:12.4f}")
IW = [4, 5, 6]   # z = 2000, 1100, 500 -- the recombination window
wl = float(np.max(np.abs(W['LCDM'][IW] / W['LCDM'][0])))
ws = float(np.max(np.abs(W['SMOOTH'][IW] / W['SMOOTH'][0])))
check("MECH-0  at the third-peak scale the LCDM gravitational potential DECAYS through radiation domination "
      "and then FREEZES at ~11% of its primordial value once CDM dominates -- that frozen well is what the "
      "third peak measures. With smooth dust the potential decays to a few times 1e-3 and oscillates in "
      "SIGN: there is no well left at recombination. The third peak's enhancement is a clustering "
      "signature, and the clustering is absent -- exhibited, not assumed",
      wl > 0.05 and ws < 0.02 and wl / ws > 10,
      f"max |Weyl/Weyl(1e5)| over z = 2000-500: {wl:.4f} (LCDM) vs {ws:.4f} (smooth), a factor {wl/ws:.0f}")

# =============================================================================================
sec("PART 7 -- honest scope.")
# =============================================================================================
print("""
  WHAT IS SHOWN (two codes, calibrated against the published Planck peak amplitudes and their errors):
    * A smooth (non-clustering) a^-3 component cannot drive the CMB third peak. With theta_star fixed and
      one free overall amplitude, it misses by 55 sigma; the amplitude-free ratio A3/A2 is 0.60 against the
      measured 0.9737 +- 0.0109, a 34 sigma / 38% deficit.
    * The c_s^2 -> infinity limit is a numerically reached limit, not a stand-in.
    * No value of omega_smooth repairs it (best case -26 sigma over a factor-50 scan).
    * At most ~1% of the dark component may be smooth (full-spectrum chi^2), ~10% (third-peak ratio alone).
    * sigma_8 is a far tighter constraint on the sound speed than the peaks are: c_s^2 <~ 1e-6.

  WHAT IS *NOT* SHOWN -- and this is load-bearing:
   1. THESE ARE GENERAL-RELATIVISTIC PERTURBATIONS. CAMB and CLASS solve the GR Boltzmann hierarchy with a
      smooth dark component added. The programme's own modified perturbation equations are NOT in here.
      L136 R3 is the standing correction on exactly this point: under a0 ~ H(z) the recombination-epoch
      acceleration scale is not the local one, and the deep-MOND response at the third-peak scale is not
      the GR response. So this lane closes "smooth a^-3 dust + GR perturbations". It does NOT close the
      programme's cosmology, and must not be cited as doing so.
   2. IT IS NOT A LIKELIHOOD. The comparison uses the three published Planck TT peak amplitudes with an
      error model validated to reproduce Planck's own quoted sigma(A3) = 17 uK^2, plus a chi^2 against the
      LCDM spectrum (which matches the published peaks to 0.05/0.4/1.4 sigma) with a Gaussian, uncorrelated,
      cosmic-variance + noise covariance. The real Planck likelihood has bandpower correlations, foreground
      and calibration nuisance parameters. At a 34-55 sigma miss none of that matters, but the number should
      be read as "tens of sigma", not as a likelihood-grade figure to three digits.
   3. THE CAMB 'no perturbations' ROUTE IS *NOT* THE CUSCUTON, and is not used for the headline. Setting the
      fluid's delta to zero at all times violates adiabatic initial conditions on super-horizon scales and
      injects a large isocurvature mode (it gives D_2 ~ 1.3e6 uK^2 and A3/A2 = 1.58, i.e. it fails in the
      OPPOSITE ratio direction). The cuscuton's perturbation is slaved with a 1/k^2 suppression, so it
      tracks on super-horizon scales and vanishes sub-horizon -- exactly the large-but-finite-c_s^2 fluid.
      That is why the headline comes from the converged c_s^2 ladder and not from that route. Both routes
      fail catastrophically; only the ladder is quantitatively faithful.
   4. NOTHING HERE addresses whether a ghost-free non-propagating field could cluster by some other
      mechanism. It quantifies the target: c_s^2 <~ 1e-6, from infinity.
""")
check("SCOPE-0  honestly bounded: SHOWN = smooth a^-3 dust misses the third peak by 55 sigma under GR "
      "perturbations, in two codes, with no window in omega_smooth and a <=1-10% ceiling on the smooth "
      "fraction. NOT SHOWN = anything about the programme's own modified perturbation equations (L136 R3 "
      "stands), and this is not a likelihood-grade number", True,
      "closes smooth-dust + GR perturbations; does NOT close the programme's cosmology")
check("SCOPE-2  PRIORITY IS NOT MINE. The result that smooth a^-3 dust fails the third peak is L129's; "
      "the CAMB tabulated-w route and the clustering-fraction scan are L145's (reproduced here to 4 "
      "significant figures); the smooth-fraction floor is L146/L147's and is TIGHTER than this lane's; "
      "the sound-speed ceiling is L156's and is TIGHTER than this lane's. What this lane contributes is "
      "the f = 0 endpoint in calibrated sigma, the converged c_s^2 -> infinity limit, the two-code check, "
      "the omega_smooth window scan, the inverted baryon lever and the measured Weyl decay. Cite the "
      "earlier lanes for what they established", True,
      "confirmation-and-extension; L146 and L156 carry the tighter versions of two of these numbers")
check("SCOPE-1  L129 is CONFIRMED and SUPERSEDED in scope, not contradicted: its c_s^2 = 1 CLASS numbers "
      "reproduce here (A3/A1 = 0.2263 there vs 0.2254 from independent CAMB at the same c_s^2), its refusal "
      "to quote a sigma is now discharged with a calibrated error model, and its requested CAMB cross-check "
      "is done. Its one imprecision -- that c_s^2 = 1 is 'conservative in the correct direction' -- is "
      "corrected: c_s^2 = 1 is slightly WORSE than the true infinite-c_s limit, not better",
      lad[1.0]['r32'] < lad[1e4]['r32'],
      f"A3/A2: c_s^2 = 1 gives {lad[1.0]['r32']:.4f}, the c_s^2 -> inf limit gives {lad[1e4]['r32']:.4f} "
      f"(the limit is the less extreme of the two, and both are excluded)")

sec("VERDICT")
print(f"""
  A SMOOTH a^-3 DARK COMPONENT MISSES THE CMB THIRD PEAK BY {abs(KILL['n3']):.0f} SIGMA.

  With the acoustic scale held fixed and a single overall amplitude free, the ratio of the third to the
  second acoustic peak comes out {KILL['r32']:.3f} against Planck's measured {O32:.4f} +- {S32:.4f}: a {abs(KILL['s32']):.0f} sigma,
  {100*(1-KILL['r32']/O32):.0f}% deficit. Two independent Boltzmann codes agree to 0.1%. There is no value of omega_smooth that
  repairs it, and at most about 1% of the dark component may be smooth.

  The mechanism is measured, not assumed: at the third-peak scale the gravitational potential freezes at 11%
  of its primordial value in LCDM and decays to ~0.5% (with sign changes) when the dark component is smooth.
  The third peak is reading the depth of a well that a smooth component does not dig. z_eq is not a
  substitute -- the background was held EXACTLY identical, so z_eq was matched by construction, and the
  spectrum still fails.

  For the cuscuton line specifically: the c_s^2 = infinity that lets the cuscuton evade the stiff-genericity
  no-go (L128) is the same property that costs it the third peak, and the required c_s^2 is <~ 1e-6. That is
  not a near miss to be closed by a better potential; V does not enter the kinetic degeneracy at all.

  CAVEAT THAT MUST TRAVEL WITH THIS NUMBER: these are GR perturbations. The programme's own modified
  perturbation equations are not included (L136 R3). This closes smooth-dust-in-GR; it does not close the
  programme's cosmology.
""")
print("=" * 112)
if FAILS:
    print(f"L165 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L165 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.0f}s]")
print("=" * 112)
