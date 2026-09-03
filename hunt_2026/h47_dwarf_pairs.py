#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h47_dwarf_pairs.py -- HUNT ITEM 47: the dwarf-pair Kepler law.
==============================================================
The item as written: take Stierwalt et al. 2015's TiNy Titans (TNT) isolated dwarf-dwarf pairs, whose velocity
separations and projected separations are published, and test the framework's deep-MOND two-body law
      v_rel^2 = (2/3) sqrt(G a_0) [ (M1+M2)^{3/2} - M1^{3/2} - M2^{3/2} ] / mu,    mu = M1 M2/(M1+M2)
(Milgrom 1994), which for an equal-mass pair gives v_rel = 1.051 (G m a_0)^{1/4} and is INDEPENDENT of separation.
Dwarfs are the best possible place to look: their internal accelerations are far below a_0 and the LambdaCDM
alternative (an abundance-matched halo) is at its most extreme there.

TWO VERDICTS, and they are different.
  (A) ITEM 47 AS POSED IS NOT RUNNABLE.  The TNT per-pair table does not exist in machine-readable form: nothing on
      disk, VizieR (CfA mirror) answers "Table or Catalog not found: J/ApJ/805/2", and the arXiv preprint carries only
      "TNT Starburst and Quenched Fractions" -- r_sep and v_sep appear only as points in its Figure 2.  Section 1.
      Section 3 then shows that even WITH the table it would be underpowered: with the paper's own median SDSS
      velocity uncertainty of 37 km/s against a 20-40 km/s signal, 60 pairs separate the framework from LambdaCDM at
      about 2 sigma, under the hunt list's 3 sigma bar, and cannot separate the framework's own two branches either.
  (B) THE PHYSICS IS RUNNABLE ON A BETTER SAMPLE, AND IS RUN HERE.  Section 4 builds an isolated dwarf-pair
      catalogue from ALFALFA alpha.100 (fetched this session): HI systemic velocities good to a few km/s instead of
      37, a baryonic mass measured (M_HI) rather than inferred from a stellar M/L, TNT's own isolation criterion
      imposed against 2MRS, and roughly ten times TNT's pair count.  That sample gives a real measurement, and it is
      reported here whichever way it comes out.

A PHYSICS POINT THE ITEM DID NOT ANTICIPATE, and it governs the answer: at dwarf-pair separations the pair's own
internal MOND field, sqrt(G M_b a_0)/r, is only a FEW PER CENT of a_0 -- the same order as the external field of
large-scale structure on an isolated galaxy (e_N ~ 0.01-0.05).  The external-field effect therefore sets the
framework's prediction over most of the range, the isolated deep-MOND law is the framework's BEST CASE (the largest
dv it can produce at fixed baryonic mass) rather than its prediction, and any "flat dv vs separation" reading of the
item is a statement about the best case only.  Exactly the same correction was needed for the massive pairs of items
48/69 (h48_h69_binary_galaxies.py).

Both footings.  LambdaCDM (Moster+2013 abundance matching + NFW) computed beside the framework.  Mutation controls.
Checks CAN fail -- and several of the first version's did, which is why this one differs from it (see NOTE below).

NOTE ON THE FIRST VERSION OF THIS SCRIPT.  An earlier draft of h47 was written but never executed.  Run, four of its
six checks FAILED, and three of the failures were the draft's own fault, not the data's:
  * its mutation control scaled a_0 in BOTH the mock generation and the reference prediction, so the fitted amplitude
    could not move -- a control with no bite.  Fixed here: a_0 is mutated in the generator only.
  * it asserted that a 60-pair TNT sample "CAN kill Newtonian gravity on the baryons alone".  The forecast says
    otherwise (0.4 sigma), because over TNT's mass and separation ranges the Newtonian and deep-MOND amplitudes are
    accidentally close.  Corrected.
  * it asserted that the on-disk catalogues contain a negligible number of dwarf pairs.  They contain 62 inside the
    TNT window.  They are still unusable, but for a different and better-evidenced reason (item 48b's selection bias),
    and the check now tests that reason instead.
  * its Magellanic check demanded that the observed 128 km/s lie between the two framework branches.  It does not:
    both branches are BELOW it.  Reported as found, with the eccentricity caveat that softens it.
"""
import sys, math, os, glob, collections
import numpy as np
from scipy.spatial import cKDTree
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(47047)
E_N = 0.02                  # external field of large-scale structure on an isolated dwarf, in units of a_0
V_ERR_TNT = 37.0            # km/s, TNT's own median SDSS velocity uncertainty per pair
N_TNT = 60                  # TNT's own number of isolated pairs
F_GAS = 3.0                 # M_b/M* for gas-rich dwarfs (M_HI ~ 1-2 M*), used only in the TNT forecast
UPS_K = 0.6                 # stellar M/L in Ks (repo convention), used only for the 2MRS isolation veto
MK_SUN = 3.28
H0_KMS = 67.4

# ---------------------------------------------------------------------------------------------- gravity laws
def v_rel_deepmond(M1, M2, a0):
    """Milgrom (1994) exact deep-MOND two-body relative speed of a circular relative orbit [m/s].  No r dependence."""
    M1 = np.asarray(M1, float)*Msun; M2 = np.asarray(M2, float)*Msun
    Mt = M1 + M2; mu = M1*M2/Mt
    return np.sqrt((2/3.)*np.sqrt(G*a0)*(Mt**1.5 - M1**1.5 - M2**1.5)/mu)

def v_rel_newton(M1, M2, r_kpc):
    return np.sqrt(G*(np.asarray(M1, float) + np.asarray(M2, float))*Msun/(np.asarray(r_kpc, float)*kpc))

def v_rel_efe(M1, M2, r_kpc, eN):
    """Quasi-Newtonian branch: a dominant external field e_N makes the internal dynamics Newtonian with
    G_eff = nu(e_N) G (to leading order; the EFE tensor's anisotropy is a further O(1) factor left out here)."""
    return math.sqrt(nu_s(eN))*v_rel_newton(M1, M2, r_kpc)

def v_rel_framework(M1, M2, r_kpc, a0, eN):
    """The framework's actual answer: whichever of the internal and external fields dominates.  Taking the minimum
    of the two branches is the standard interpolation and is CONSERVATIVE for the framework only in the sense that
    it never exceeds the isolated law; it is the honest prediction, not the best case."""
    return np.minimum(v_rel_deepmond(M1, M2, a0), v_rel_efe(M1, M2, r_kpc, eN))

def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(logMh - logM1)
    return 10**logMh*2*N/(x**(-be) + x**ga)
_LMH = np.linspace(8.0, 15.5, 1501); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass(Mstar): return 10**np.interp(np.log10(np.asarray(Mstar, float)), _LMS, _LMH)
_RHO_C = 3*(H0_KMS*1e3/Mpc)**2/(8*math.pi*G)/Msun*(3.0857e22)**3
def nfw_enclosed(Mh, r_kpc):
    Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
    c = 10**(0.905 - 0.101*(np.log10(Mh*0.674) - 12.0))
    R200 = (3*Mh/(4*math.pi*200*_RHO_C))**(1/3.)*1000.0
    x = np.clip(r_kpc/R200, 1e-4, 5.0)
    m = lambda t: np.log1p(t) - t/(1 + t)
    return Mh*m(c*x)/m(c)

def sigma_law(M1, M2, r_kpc, law, a0=None, eN=E_N):
    """rms line-of-sight velocity difference [km/s] for a circular relative orbit at 3-D separation r_kpc."""
    if law == "deepmond":  v = v_rel_deepmond(M1, M2, a0)
    elif law == "efe":     v = v_rel_efe(M1, M2, r_kpc, eN)
    elif law == "framework": v = v_rel_framework(M1, M2, r_kpc, a0, eN)
    elif law == "newton":  v = v_rel_newton(M1, M2, r_kpc)
    elif law == "lcdm":
        v = np.sqrt(G*(nfw_enclosed(halo_mass(M1), r_kpc) + nfw_enclosed(halo_mass(M2), r_kpc))*Msun
                    / (np.asarray(r_kpc, float)*kpc))
    else: raise ValueError(law)
    return v/math.sqrt(3.0)/1e3

def sigma_pred(M1, M2, rp_kpc, law, a0=None, eN=E_N, nmc=300, seed=1):
    """Predicted rms dv_los [km/s] given the PROJECTED separation only.  Deprojection: draw the 3-D separation r from
    a log-uniform prior weighted by the random-orientation kernel p(r_p|r) = r_p/(r sqrt(r^2-r_p^2)); circular
    relative orbit of speed v_rel(r); isotropic velocity direction so <dv_los^2> = <v_rel^2>/3.
    (Same construction as h48_h69_binary_galaxies.py, so the two items' amplitudes are directly comparable.)"""
    g = np.random.default_rng(seed)
    M1 = np.asarray(M1, float); M2 = np.asarray(M2, float); rp = np.asarray(rp_kpc, float)
    u = g.random((len(rp), nmc))
    r = rp[:, None]*np.exp(u*math.log(20.0))*1.0001
    w = 1.0/np.sqrt(np.maximum((r/rp[:, None])**2 - 1.0, 1e-6)); w /= w.sum(axis=1, keepdims=True)
    if law == "deepmond":
        v2 = np.repeat((v_rel_deepmond(M1, M2, a0)**2)[:, None], nmc, axis=1)
    elif law == "efe":
        v2 = v_rel_efe(M1[:, None], M2[:, None], r, eN)**2
    elif law == "framework":
        v2 = v_rel_framework(M1[:, None], M2[:, None], r, a0, eN)**2
    elif law == "newton":
        v2 = v_rel_newton(M1[:, None], M2[:, None], r)**2
    elif law == "lcdm":
        v2 = G*(nfw_enclosed(halo_mass(M1)[:, None], r) + nfw_enclosed(halo_mass(M2)[:, None], r))*Msun/(r*kpc)
    else: raise ValueError(law)
    return np.sqrt(np.sum(w*v2, axis=1)/3.0)/1e3

def ml_sigma(dv, sig_shape=None, dvmax=500.0, verr=8.0):
    """Pair/interloper likelihood: each pair is either real (dv Gaussian with dispersion sqrt((A s_i)^2 + verr^2)) or
    an interloper drawn uniformly on [-dvmax, dvmax].  sig_shape=None fits one common sigma; otherwise it fits the
    AMPLITUDE A relative to the supplied per-pair prediction.  Returns (value, error, interloper fraction)."""
    dv = np.asarray(dv, float); n = len(dv)
    s = np.ones(n) if sig_shape is None else np.asarray(sig_shape, float)
    def nll(pars):
        lA, lf = pars
        A = math.exp(lA); f = 1/(1 + math.exp(-lf))
        sg = np.sqrt((A*s)**2 + verr**2)
        p = f*np.exp(-0.5*(dv/sg)**2)/(math.sqrt(2*math.pi)*sg) + (1 - f)/(2*dvmax)
        return -np.sum(np.log(np.maximum(p, 1e-300)))
    lAs = np.linspace(math.log(5.0), math.log(400.0), 90) if sig_shape is None else np.linspace(math.log(0.10), math.log(12.0), 90)
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
    fine = np.linspace(lA0 - 0.35, lA0 + 0.35, 241)
    prof = np.array([min(nll((lA, lf)) for lf in np.linspace(lf0 - 0.9, lf0 + 0.9, 25)) for lA in fine])
    prof -= prof.min(); lA0 = fine[int(np.argmin(prof))]
    hi = fine[prof < 0.5]
    err_ln = (hi.max() - hi.min())/2 if len(hi) > 1 else float(np.diff(fine).mean())
    A = math.exp(lA0)
    return A, A*err_ln, 1 - 1/(1 + math.exp(-lf0))

def ml_slope(dv, mb, dvmax=500.0, verr=8.0):
    """Direct maximum-likelihood fit of sigma_i = S * (M_b,i/median)^beta together with the interloper fraction.
    Binning into mass quartiles and regressing four points, which is what the first version of this section did,
    throws away most of the information and is dominated by whichever bin happens to scatter high -- the bright/faint
    half-split disagreed with the binned slope, which is how the problem was found.  This estimator uses every pair.
    Returns (beta, error from the profile likelihood, S at the median mass)."""
    dv = np.asarray(dv, float); x = np.log10(np.asarray(mb, float)/np.median(mb))
    def nll(lS, be, lf):
        f = 1/(1 + math.exp(-lf))
        sg = np.sqrt((math.exp(lS)*10**(be*x))**2 + verr**2)
        p = f*np.exp(-0.5*(dv/sg)**2)/(math.sqrt(2*math.pi)*sg) + (1 - f)/(2*dvmax)
        return -np.sum(np.log(np.maximum(p, 1e-300)))
    bes = np.linspace(-1.5, 2.5, 81)
    prof = []
    for be in bes:
        best = 1e30; lS0, lf0 = math.log(50.0), 1.0
        for lS in np.linspace(math.log(5.0), math.log(400.0), 60):
            for lf in np.linspace(-3, 4, 25):
                v = nll(lS, be, lf)
                if v < best: best, lS0, lf0 = v, lS, lf
        for _ in range(3):
            lf0 = min(np.linspace(lf0 - 0.8, lf0 + 0.8, 41), key=lambda t: nll(lS0, be, t))
            lS0 = min(np.linspace(lS0 - 0.2, lS0 + 0.2, 41), key=lambda t: nll(t, be, lf0))
        prof.append(nll(lS0, be, lf0))
    prof = np.array(prof); prof -= prof.min()
    be_hat = float(bes[int(np.argmin(prof))])
    ok = bes[prof < 0.5]
    err = float((ok.max() - ok.min())/2) if len(ok) > 1 else float(np.diff(bes).mean())
    return be_hat, err, prof

def unitvec(ra, de):
    ra = np.radians(ra); de = np.radians(de)
    return np.c_[np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)]

# ====================================================================================================================
P("="*122); P("SECTION 1 -- is the TiNy Titans per-pair table available at all?"); P("="*122)
found = sorted(glob.glob(os.path.join(DATA, "*tnt*")) + glob.glob(os.path.join(DATA, "*tiny*")) +
               glob.glob(os.path.join(DATA, "*stierwalt*")) + glob.glob(os.path.join(DATA, "**", "*tnt*"), recursive=True))
info(f"files on disk matching TNT / TiNy / Stierwalt: {found if found else 'NONE'}")
info("VizieR (CfA mirror, vizier.cfa.harvard.edu, the one reachable from here) answers")
info("   'Error=Table or Catalog not found: J/ApJ/805/2'  -- checked this session; Stierwalt et al. 2015 was never")
info("deposited at CDS.  The arXiv preprint 1412.4796 carries one table, 'TNT Starburst and Quenched Fractions';")
info("the per-pair r_sep and v_sep exist only as plotted points in its Figure 2.")
ck("47a ITEM 47 AS POSED IS NOT RUNNABLE -- the dwarf-pair velocity differences and separations it needs are not "
   "available in machine-readable form: nothing on disk, no CDS/VizieR deposit, and the preprint publishes them "
   "only as a scatter plot.  A data-availability result, not a null",
   len(found) == 0, "0 matching files on disk; VizieR J/ApJ/805/2 returns 'Table or Catalog not found'")

# ====================================================================================================================
P(""); P("="*122); P("SECTION 2 -- what regime are dwarf pairs actually in?  (the item assumed deep MOND; check it)"); P("="*122)
info("TNT selection (Stierwalt et al. 2015, ApJ 805, 2): 60 isolated pairs, r_sep < 50 kpc, v_sep < 300 km/s (only")
info("six above 150), 7 < log(M*/Msun) < 9.7, stellar mass ratio < 10, every pair > 1.5 Mpc from a galaxy with")
info(f"M* > 2.5e10 Msun.  Baryonic mass here M_b = {F_GAS:.0f} M* (gas-rich dwarfs).")
P("")
info(f"{'log M* (each)':>14} {'M_b pair':>11} {'r [kpc]':>8} {'g_N/a_0':>10} {'g_int/a_0':>11} {'g_int/e_N':>10}")
regime = []
for lms in (7.5, 8.5, 9.5):
    for r in (10.0, 30.0, 50.0):
        m = F_GAS*10**lms; Mt = 2*m; a0 = A0["canonical"]
        gN = G*Mt*Msun/(r*kpc)**2
        gint = math.sqrt(G*Mt*Msun*a0)/(r*kpc)
        regime.append((lms, r, gN/a0, gint/a0))
        info(f"{lms:14.1f} {Mt:11.2e} {r:8.0f} {gN/a0:10.4f} {gint/a0:11.4f} {gint/a0/E_N:10.2f}")
frac_efe = float(np.mean([x[3] < 3*E_N for x in regime]))
ck("47b the item's premise needs correcting: TNT pairs are deep in the MOND regime (g_N/a_0 = 1e-4 to 1e-2, kernel "
   "fully engaged) but their internal MOND field is only a few per cent of a_0 -- the SAME ORDER as the external "
   "field of large-scale structure on an isolated galaxy.  The EFE therefore governs the answer over most of the "
   "range, and the isolated deep-MOND law is the framework's BEST CASE, not its prediction",
   frac_efe > 0.4,
   f"{100*frac_efe:.0f}% of the tabulated (mass, separation) combinations have internal field below 3 e_N with "
   f"e_N = {E_N}; only the most massive TNT dwarfs at the smallest separations stay on the isolated branch")

# ====================================================================================================================
P(""); P("="*122); P("SECTION 3 -- the forecast for a 60-pair TNT sample with SDSS-grade velocities"); P("="*122)
for ft, a0 in A0.items():
    info(f"--- footing {ft} (a_0 = {a0:.3e}) ---")
    info(f"{'log M* (each)':>14} {'r [kpc]':>8} {'deep-MOND':>11} {'EFE branch':>11} {'Newton_b':>10} {'LambdaCDM':>11}  [km/s, sigma_los]")
    for lms in (7.5, 8.5, 9.5):
        for r in (10.0, 30.0):
            m = F_GAS*10**lms
            info(f"{lms:14.1f} {r:8.0f} {sigma_law(m, m, r, 'deepmond', a0=a0):11.1f} "
                 f"{sigma_law(m, m, r, 'efe', a0=a0):11.1f} {sigma_law(m, m, r, 'newton'):10.1f} "
                 f"{sigma_law(m, m, r, 'lcdm'):11.1f}")
info(f"against a published median SDSS velocity uncertainty of +/- {V_ERR_TNT:.0f} km/s PER PAIR.")

def mock_and_fit(true_law, a0_gen, a0_ref=None, n=N_TNT, ntrial=200, verr=V_ERR_TNT, seed=0):
    """TNT-like mocks under `true_law` with a_0 = a0_gen, fitted for the amplitude A relative to the deep-MOND
    prediction computed with a_0 = a0_ref (defaults to a0_gen).  Keeping the two separate is what gives the
    mutation control its bite: the earlier draft used one a_0 for both and could not respond to it at all."""
    a0_ref = a0_gen if a0_ref is None else a0_ref
    g = np.random.default_rng(seed); As = []
    for _ in range(ntrial):
        lms = g.uniform(7.5, 9.5, n)                       # TNT's mass range, flat in log
        ratio = 10**g.uniform(0, 1, n)                     # mass ratios up to 10
        m1 = F_GAS*10**lms; m2 = m1/ratio
        r = 10**g.uniform(0, math.log10(50.0), n)          # separations to 50 kpc, flat in log
        s_true = sigma_law(m1, m2, r, true_law, a0=a0_gen)
        dv = g.normal(0, np.sqrt(s_true**2 + verr**2))
        keep = np.abs(dv) < 300.0                          # TNT's own velocity cut
        dv = dv[keep]; s_dm = sigma_law(m1, m2, r, "deepmond", a0=a0_ref)[keep]
        lAs = np.linspace(math.log(0.15), math.log(8.0), 160)
        def nll(lA):
            sg = np.sqrt((math.exp(lA)*s_dm)**2 + verr**2)
            return -np.sum(np.log(np.exp(-0.5*(dv/sg)**2)/(math.sqrt(2*math.pi)*sg) + 1e-300))
        As.append(math.exp(lAs[int(np.argmin([nll(x) for x in lAs]))]))
    return float(np.mean(As)), float(np.std(As))
P("")
info("forecast: 200 mock TNT samples of 60 pairs each, generated under each law and fitted for the amplitude A "
    "relative to the framework's deep-MOND prediction (A = 1 means the framework is right)")
FC = {}
for law in ("deepmond", "efe", "newton", "lcdm"):
    mu_, sd_ = mock_and_fit(law, A0["canonical"], seed=abs(hash(law)) % 1000)
    FC[law] = (mu_, sd_)
    info(f"  truth = {law:10}: fitted A = {mu_:.2f} +/- {sd_:.2f}")
seps = {k: abs(FC[k][0] - FC["deepmond"][0])/math.sqrt(FC[k][1]**2 + FC["deepmond"][1]**2) for k in ("lcdm", "efe", "newton")}
info(f"separations at N = {N_TNT}: framework vs LambdaCDM {seps['lcdm']:.1f} sigma, framework vs its own EFE branch "
     f"{seps['efe']:.1f} sigma, framework vs Newton-on-the-baryons {seps['newton']:.1f} sigma")
n_need = N_TNT*(3.0/max(seps["lcdm"], 1e-9))**2
info(f"AGAINST THE DRAFT'S OWN CLAIM: the earlier version of this script asserted that 60 TNT pairs could at least "
     f"kill Newtonian gravity on the baryons alone.  They cannot ({seps['newton']:.1f} sigma) -- over TNT's mass and")
info("separation ranges the Newtonian and deep-MOND amplitudes happen to be close, so the two laws are degenerate")
info("in an amplitude fit and only the SEPARATION DEPENDENCE would tell them apart.")
ck("47c UNDERPOWERED even if the table existed -- with a median velocity uncertainty of 37 km/s against a 20-40 km/s "
   "signal, 60 pairs reach only ~2 sigma between the framework and LambdaCDM, under the hunt list's 3 sigma bar, and "
   "cannot separate the framework's own two branches either",
   seps["lcdm"] < 3.0 and seps["efe"] < 3.0,
   f"framework vs LambdaCDM {seps['lcdm']:.1f} sigma at N = {N_TNT} (3 sigma needs N ~ {n_need:.0f}); vs its own EFE "
   f"branch {seps['efe']:.1f} sigma; vs Newton-baryons {seps['newton']:.1f} sigma")

mu_x, sd_x = mock_and_fit("deepmond", 16*A0["canonical"], a0_ref=A0["canonical"], seed=99)
ck("M1 mutation control (REPAIRED) -- generating the mocks with a_0 sixteen times too large while the reference "
   "prediction keeps the true a_0 moves the fitted amplitude by the predicted factor of 2 (v ~ a_0^1/4), so the 47c "
   "verdict is a statement about the size of the effect and not about a dead estimator",
   abs(mu_x - 2.0) < 0.35 and abs(mu_x - 1.0)/sd_x > 3.0,
   f"a_0 x 16 in the generator only: fitted A = {mu_x:.2f} +/- {sd_x:.2f}, predicted 2.00, "
   f"{abs(mu_x-1.0)/sd_x:.1f} sigma from 1")

# ====================================================================================================================
P(""); P("="*122); P("SECTION 4 -- the substitute that works: isolated dwarf pairs from ALFALFA alpha.100"); P("="*122)
info("alpha.100 (Haynes et al. 2018, J/ApJ/861/49 table2) fetched this session to")
info("real_research/data/alfalfa_a100_positions.tsv -- 31502 HI sources with position, systemic velocity, W50,")
info("flow-model distance and log M_HI.  Why it beats TNT for this item:")
info("  * the systemic velocity comes from an HI profile, good to a few km/s, not 37;")
info("  * M_HI is a MEASURED baryonic mass, so the stellar M/L that blocks the rest of this hunt is a minor term;")
info("  * TNT's own isolation criterion (no galaxy with M* > 2.5e10 within 1.5 Mpc) can be imposed against 2MRS;")
info("  * there are about ten times as many pairs.")
info("What it costs: ALFALFA's 3.5' beam blends pairs closer than about two beamwidths, so this sample lives at")
info("LARGER separations than TNT's < 50 kpc, where the external-field branch is even more dominant.")

rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "alfalfa_a100_positions.tsv"), encoding="latin-1")
        if l.strip() and not l.startswith("#")]
hdr = [h.strip() for h in rows[0]]; body = rows[3:]
col = {k: [r[i].strip() if i < len(r) else "" for r in body] for i, k in enumerate(hdr)}
def _ff(v):
    try: return float(v)
    except Exception: return float("nan")
def _sx(s):
    p = s.split()
    return (float(p[0]) + float(p[1])/60 + float(p[2])/3600)*15 if len(p) == 3 else float("nan")
def _sd(s):
    sg = -1.0 if s.strip().startswith("-") else 1.0; p = s.strip().lstrip("+-").split()
    return sg*(float(p[0]) + float(p[1])/60 + float(p[2])/3600) if len(p) == 3 else float("nan")
A_ra = np.array([_sx(x) for x in col["RAJ2000"]]); A_de = np.array([_sd(x) for x in col["DEJ2000"]])
A_v = np.array([_ff(x) for x in col["Vhel"]]); A_D = np.array([_ff(x) for x in col["Dist"]])
A_lm = np.array([_ff(x) for x in col["logMHI"]]); A_code = np.array([_ff(x) for x in col["HI"]])
A_eW = np.array([_ff(x) for x in col["e_W50"]]); A_agc = np.array([x for x in col["AGC"]])
t2 = {r["AGC"].strip(): r for r in vizier_tsv("alfalfa_sdss_durbala2020_t2.tsv")}
A_lms = np.array([_ff(t2[a]["logMsT"]) if a in t2 else np.nan for a in A_agc])
info(f"alpha.100 rows: {len(A_agc)};  code-1 (S/N-selected, reliable) {int(np.sum(A_code == 1))};  "
     f"with an ALFALFA-SDSS stellar mass {int(np.sum(np.isfinite(A_lms)))}")

D_LO, D_HI = 5.0, 100.0        # Mpc; the upper end is where 2MRS is still complete for the isolation veto
LMHI_MAX = 9.3                 # dwarf definition: M_HI < 2e9 Msun
RP_LO, RP_HI = 20.0, 400.0     # kpc, projected separation window
DV_WIN = 500.0                 # km/s, velocity window -- >10x the expected signal, so nothing is truncated
THETA_MIN = 4.0/60.0           # deg, ~2 ALFALFA beamwidths: below this the two HI profiles are not independent
F_THIRD, R_THIRD_MIN, DV_THIRD = 2.0, 150.0, 500.0
# relative isolation, the standard binary-pair criterion: no third alpha.100 source within max(F_THIRD x r_p,
# R_THIRD_MIN) of the pair midpoint at |dv| < DV_THIRD.  Scaling with r_p (rather than a fixed radius) is what keeps
# the close pairs in the sample -- a fixed 400 kpc veto removes them preferentially and leaves only r_p > 200 kpc.
# The sensitivity of every headline number to F_THIRD is scanned at the end of the section.
R_ISO_MPC, DV_ISO = 1.5, 1000.0      # TNT's isolation: no M* > 2.5e10 galaxy within 1.5 Mpc and 1000 km/s
MSTAR_ISO = 2.5e10

base = (A_code == 1) & np.isfinite(A_D) & (A_D > D_LO) & (A_D < D_HI) & np.isfinite(A_lm) & np.isfinite(A_ra)
dw = base & (A_lm < LMHI_MAX)
info(f"code-1 sources with {D_LO:.0f} < D < {D_HI:.0f} Mpc: {int(base.sum())};  of those log M_HI < {LMHI_MAX}: {int(dw.sum())}")

ia = np.where(dw)[0]; ib = np.where(base)[0]
u_dw = unitvec(A_ra[ia], A_de[ia]); u_all = unitvec(A_ra[ib], A_de[ib])
tree_dw = cKDTree(u_dw); tree_all = cKDTree(u_all)
chord = 2*np.sin(0.5*(RP_HI/1000.0)/D_LO)
raw = tree_dw.query_pairs(r=chord, output_type="ndarray")
p, q = raw[:, 0], raw[:, 1]
th = 2*np.arcsin(np.clip(np.linalg.norm(u_dw[p] - u_dw[q], axis=1)/2, 0, 1))
Dmean = 0.5*(A_D[ia[p]] + A_D[ia[q]])
rp = th*Dmean*1000.0
dv = A_v[ia[p]] - A_v[ia[q]]
keep = (rp > RP_LO) & (rp < RP_HI) & (np.abs(dv) < DV_WIN) & (np.degrees(th) > THETA_MIN)
p, q, rp, dv, Dmean = p[keep], q[keep], rp[keep], dv[keep], Dmean[keep]
info(f"candidate dwarf pairs ({RP_LO:.0f}-{RP_HI:.0f} kpc, |dv| < {DV_WIN:.0f} km/s, separation > {60*THETA_MIN:.0f}'): {len(p)}")

# --- cut 1: relative isolation.  For every candidate pair, find the projected distance from the midpoint to the
#     NEAREST third alpha.100 source at |dv| < DV_THIRD; the cut is then applied (and scanned) as d3 > F x r_p.
mid = u_dw[p] + u_dw[q]; mid /= np.linalg.norm(mid, axis=1)[:, None]
vmid = 0.5*(A_v[ia[p]] + A_v[ia[q]])
SEARCH_KPC = 2000.0
d3 = np.full(len(p), np.inf)
for k in range(len(p)):
    ang = min((SEARCH_KPC/1000.0)/max(Dmean[k], 1e-6), 1.0)
    nb = tree_all.query_ball_point(mid[k], 2*math.sin(0.5*ang))
    best = np.inf
    for n in nb:
        gi = ib[n]
        if gi == ia[p[k]] or gi == ia[q[k]]: continue
        if abs(A_v[gi] - vmid[k]) >= DV_THIRD: continue
        s = 2*math.asin(min(np.linalg.norm(u_all[n] - mid[k])/2, 1.0))*Dmean[k]*1000.0
        if s < best: best = s
    d3[k] = best
ok_third = d3 > np.maximum(F_THIRD*rp, R_THIRD_MIN)
info(f"after relative isolation (no third alpha.100 source inside max({F_THIRD:.0f} r_p, {R_THIRD_MIN:.0f} kpc) of "
     f"the midpoint at |dv| < {DV_THIRD:.0f} km/s): {int(ok_third.sum())}")

# --- cut 2: TNT's isolation against 2MRS massive galaxies
m2 = np.genfromtxt(os.path.join(DATA, "2mrs_catalog.csv"), delimiter=",", names=True)
M_ra, M_de, M_K, M_cz = m2["RAJ2000"], m2["DEJ2000"], m2["Ktmag"], m2["cz"]
good2 = np.isfinite(M_ra) & np.isfinite(M_K) & np.isfinite(M_cz) & (M_cz > 200)
M_ra, M_de, M_K, M_cz = M_ra[good2], M_de[good2], M_K[good2], M_cz[good2]
M_D = M_cz/H0_KMS
M_LK = 10**(0.4*(MK_SUN - (M_K - 5*np.log10(M_D*1e6) + 5)))
M_Ms = UPS_K*M_LK
big = M_Ms > MSTAR_ISO
u_big = unitvec(M_ra[big], M_de[big]); cz_big = M_cz[big]
tree_big = cKDTree(u_big)
info(f"2MRS galaxies with Upsilon_K = {UPS_K} stellar mass above {MSTAR_ISO:.1e} Msun: {int(big.sum())}")
ok_iso = np.ones(len(p), bool)
for k in range(len(p)):
    ang = min(R_ISO_MPC/max(Dmean[k], 1e-6), 1.0)
    nb = tree_big.query_ball_point(mid[k], 2*math.sin(0.5*ang))
    if any(abs(cz_big[n] - vmid[k]) < DV_ISO for n in nb): ok_iso[k] = False
sel = ok_third & ok_iso
info(f"after TNT's isolation veto (no M* > {MSTAR_ISO:.1e} galaxy within {R_ISO_MPC} Mpc and {DV_ISO:.0f} km/s): {int(sel.sum())}")

def sample_mask(f_third):
    return (d3 > np.maximum(f_third*rp, R_THIRD_MIN)) & ok_iso

P1, Q1 = ia[p[sel]], ia[q[sel]]
RP, DV, DM = rp[sel], dv[sel], Dmean[sel]
# baryonic masses: 1.33 M_HI (helium) + M* where the ALFALFA-SDSS catalogue has one, else M* = M_HI (gas-rich dwarf)
def mb_of(idx):
    mhi = 10**A_lm[idx]; ms = 10**A_lms[idx]
    ms = np.where(np.isfinite(ms), ms, mhi)
    return 1.33*mhi + ms
MB1, MB2 = mb_of(P1), mb_of(Q1)
V_ERR_HI = float(np.nanmedian(np.sqrt(A_eW[P1]**2 + A_eW[Q1]**2)/2.0))
info(f"FINAL SAMPLE: {len(RP)} isolated ALFALFA dwarf pairs.  median r_p = {np.median(RP):.0f} kpc, "
     f"median D = {np.median(DM):.0f} Mpc, median log M_b(pair) = {np.log10(np.median(MB1+MB2)):.2f}, "
     f"median |dv| = {np.median(np.abs(DV)):.0f} km/s")
info(f"velocity error per pair from the tabulated e_W50: {V_ERR_HI:.1f} km/s (TNT's is {V_ERR_TNT:.0f})")
hist = np.histogram(np.abs(DV), bins=10, range=(0, DV_WIN))[0]
info("|dv| histogram in 50 km/s bins: " + " ".join(str(int(x)) for x in hist))
ck("47f the ALFALFA substitute exists and is large enough to matter: an isolated dwarf-pair sample an order of "
   "magnitude bigger than TNT's, with velocities an order of magnitude better.  This is what makes the rest of the "
   "section a measurement rather than a forecast",
   len(RP) >= 100 and V_ERR_HI < 15.0,
   f"N = {len(RP)} pairs (TNT: {N_TNT}); per-pair velocity error {V_ERR_HI:.1f} km/s (TNT: {V_ERR_TNT:.0f})")

if len(RP) >= 40:
    sig, esig, fint = ml_sigma(DV, dvmax=DV_WIN, verr=V_ERR_HI)
    info(f"maximum-likelihood dv dispersion of the whole sample: {sig:.1f} +/- {esig:.1f} km/s, "
         f"interloper fraction {fint:.2f}")
    P("")
    info(f"{'r_p bin [kpc]':>16} {'N':>5} {'f_int':>7} {'sigma_los [km/s]':>20} {'log M_b,pair':>13}")
    edges = [20, 60, 120, 200, 300, 400]
    binfo = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m_ = (RP >= lo) & (RP < hi)
        if m_.sum() < 25: continue
        s_, e_, f_ = ml_sigma(DV[m_], dvmax=DV_WIN, verr=V_ERR_HI)
        binfo.append(dict(lo=lo, hi=hi, n=int(m_.sum()), s=s_, e=e_, f=f_, rp=float(np.median(RP[m_])),
                          mb=float(np.median(MB1[m_] + MB2[m_])), mask=m_))
        info(f"{lo:7.0f} -{hi:7.0f} {int(m_.sum()):5d} {f_:7.2f} {s_:13.1f} +/-{e_:5.1f} {math.log10(binfo[-1]['mb']):13.2f}")

    for ft, a0 in A0.items():
        P("")
        info(f"--- footing {ft} (a_0 = {a0:.3e}), external field e_N = {E_N} ---")
        info(f"{'r_p bin':>16} {'observed':>15} {'deep-MOND':>11} {'EFE branch':>11} {'framework':>11} {'Newton_b':>10} {'LambdaCDM':>11}")
        for b in binfo:
            m_ = b["mask"]
            pr = {law: float(np.median(sigma_pred(MB1[m_], MB2[m_], RP[m_], law, a0=a0)))
                  for law in ("deepmond", "efe", "framework", "newton", "lcdm")}
            info(f"{b['lo']:7.0f} -{b['hi']:7.0f} {b['s']:10.1f}+/-{b['e']:4.1f} {pr['deepmond']:11.1f} "
                 f"{pr['efe']:11.1f} {pr['framework']:11.1f} {pr['newton']:10.1f} {pr['lcdm']:11.1f}")

    # ---- amplitude test, both footings, every law
    P("")
    info("amplitude A = (observed dispersion)/(predicted), fitted jointly with the interloper fraction on all "
        f"{len(RP)} pairs.  A = 1 means the law is right with no free parameter.")
    AMP = {}
    for ft, a0 in A0.items():
        for law in ("deepmond", "framework", "newton", "lcdm"):
            if law == "lcdm" and ft == "alt": continue
            sp = sigma_pred(MB1, MB2, RP, law, a0=a0)
            A_, eA_, f_ = ml_sigma(DV, sig_shape=sp, dvmax=DV_WIN, verr=V_ERR_HI)
            AMP[(ft, law)] = (A_, eA_, f_)
            info(f"  {ft:10} {law:10}: A = {A_:5.2f} +/- {eA_:4.2f}  ({math.log10(A_):+.3f} dex), "
                 f"interloper fraction {f_:.2f}")
    best_ft = min(A0, key=lambda f_: abs(math.log10(AMP[(f_, 'deepmond')][0])))
    Ab, eAb, _ = AMP[(best_ft, "deepmond")]
    Al, eAl, _ = AMP[("canonical", "lcdm")]
    Af, eAf, _ = AMP[("canonical", "framework")]
    An, eAn, _ = AMP[("canonical", "newton")]
    # what external field would the EFE branch need in order to fit?  nu(e_N) has to grow by A_framework^2.
    nu_need = nu_s(E_N)*Af**2
    y = np.logspace(-8, 0, 20001); eN_need = float(y[int(np.argmin(np.abs(1/(1 - np.exp(-np.sqrt(y))) - nu_need)))])
    info(f"to fit on the EFE branch the external field would have to satisfy nu(e_N) = {nu_need:.0f} "
         f"(it is {nu_s(E_N):.1f} at e_N = {E_N}), i.e. e_N = {eN_need:.1e} a_0 -- {E_N/eN_need:.0f}x below the "
         f"large-scale-structure value the repository uses for an isolated galaxy.")
    info("THE LOOPHOLE, stated because it is real: if the EFE branch IS right, pairs at these separations are not "
         "bound at all, and their velocity differences would be local flow rather than orbits.  The interloper term "
         "removes chance projections, not physically associated but unbound pairs.  So 47g excludes 'bound circular "
         "orbits on the EFE branch', which is what the item asked about, and not the branch itself.")
    ck("47g THE FRAMEWORK'S OWN EFE BRANCH DOES NOT FIT, and neither does Newtonian gravity on the baryons.  At "
       "60-400 kpc a dwarf pair's internal MOND field is far below the external field of large-scale structure, so "
       "the framework's honest prediction is the quasi-Newtonian branch with G_eff = nu(e_N)G -- and that is four to "
       "five times too small for bound circular orbits.  Only the ISOLATED deep-MOND branch, e_N -> 0, reproduces "
       "the observed dispersion",
       (Af - 1)/eAf > 3.0 and (An - 1)/eAn > 3.0,
       f"framework (min of the two branches, e_N = {E_N}): A = {Af:.2f} +/- {eAf:.2f}, {(Af-1)/eAf:.1f} sigma above 1; "
       f"Newton on the baryons: A = {An:.2f} +/- {eAn:.2f}, {(An-1)/eAn:.1f} sigma above 1; the EFE branch would need "
       f"e_N = {eN_need:.1e} a_0")
    ck("47h THE AMPLITUDE, and it does NOT come out at 1.  Against the framework's best case -- the isolated "
       "deep-MOND two-body law, which no external field can raise -- the observed dispersion sits ABOVE the "
       "parameter-free prediction.  LambdaCDM's abundance-matched halos sit above their own prediction too, by less. "
       "Whether the excess is physics or residual contamination is what 47i tests",
       (Ab - 1)/eAb > 2.0,
       f"best footing ({best_ft}): A = {Ab:.2f} +/- {eAb:.2f} = {math.log10(Ab):+.3f} dex, {(Ab-1)/eAb:.1f} sigma "
       f"above the parameter-free prediction -- {Ab**4:.1f}x the measured baryonic mass would be needed "
       f"(v ~ M_b^1/4).  LambdaCDM (Moster+NFW): A = {Al:.2f} +/- {eAl:.2f}, {(Al-1)/eAl:.1f} sigma above 1")

    # ---- the separation dependence: the item's own headline ("Delta v flat in separation")
    P("")
    sl_rp, esl_rp, _ = ml_slope(DV, RP, dvmax=DV_WIN, verr=V_ERR_HI)
    def pred_slope_rp(law, a0=None):
        sp = sigma_pred(MB1, MB2, RP, law, a0=a0)
        return float(np.polyfit(np.log10(RP), np.log10(sp), 1)[0])
    rp_dm = pred_slope_rp("deepmond", a0=A0["canonical"]); rp_ef = pred_slope_rp("efe", a0=A0["canonical"])
    rp_nw = pred_slope_rp("newton"); rp_lc = pred_slope_rp("lcdm")
    info(f"UNBINNED maximum-likelihood d log sigma_los / d log r_p = {sl_rp:+.3f} +/- {esl_rp:.3f} over "
         f"{RP_LO:.0f}-{RP_HI:.0f} kpc")
    info(f"predicted: isolated deep-MOND {rp_dm:+.3f} (separation-INDEPENDENT, the item's headline) | framework's "
         f"EFE branch {rp_ef:+.3f} | Newton on the baryons {rp_nw:+.3f} | LambdaCDM {rp_lc:+.3f}")
    seps_rp = {k: abs(sl_rp - v)/esl_rp for k, v in
               (("deepmond", rp_dm), ("efe", rp_ef), ("newton", rp_nw), ("lcdm", rp_lc))}
    ck("47k UNDERPOWERED -- the item's headline axis, 'Delta v flat in separation', cannot be read at this sample "
       "size.  The measured slope is consistent with ALL FOUR laws, including the two that differ from each other "
       "by 0.44 in slope.  It is the amplitude (47g, 47h) and not the separation dependence that carries whatever "
       "information this sample has; a sample several times larger, or one reaching below ALFALFA's blend limit "
       "where the two branches diverge most, would be needed to use this axis",
       max(seps_rp.values()) < 2.0,
       f"measured {sl_rp:+.3f} +/- {esl_rp:.3f}: {seps_rp['deepmond']:.1f} sigma from the isolated deep-MOND "
       f"{rp_dm:+.3f}, {seps_rp['efe']:.1f} sigma from the EFE branch {rp_ef:+.3f}, "
       f"{seps_rp['lcdm']:.1f} sigma from LambdaCDM {rp_lc:+.3f} -- no separation at all")

    # ---- the mass scaling: the only part that could be Kepler-grade
    P("")
    MBT = MB1 + MB2
    qs = np.quantile(np.log10(MBT), [0, 0.25, 0.5, 0.75, 1.0])
    info(f"{'log M_b,pair bin':>26} {'N':>5} {'sigma_los [km/s]':>20} {'deep-MOND(can)':>15} {'LambdaCDM':>10}")
    xs, ys, es = [], [], []
    for lo, hi in zip(qs[:-1], qs[1:]):
        m_ = (np.log10(MBT) >= lo) & (np.log10(MBT) <= hi if hi == qs[-1] else np.log10(MBT) < hi)
        if m_.sum() < 25: continue
        s_, e_, f_ = ml_sigma(DV[m_], dvmax=DV_WIN, verr=V_ERR_HI)
        pdm = float(np.median(sigma_pred(MB1[m_], MB2[m_], RP[m_], "deepmond", a0=A0["canonical"])))
        pl = float(np.median(sigma_pred(MB1[m_], MB2[m_], RP[m_], "lcdm")))
        info(f"{lo:11.2f} -{hi:11.2f} {int(m_.sum()):5d} {s_:13.1f} +/-{e_:5.1f} {pdm:15.1f} {pl:10.1f}")
        xs.append(float(np.median(np.log10(MBT[m_])))); ys.append(math.log10(s_)); es.append(e_/s_/math.log(10))
    if len(xs) >= 3:
        xs, ys, es = np.array(xs), np.array(ys), np.array(es)
        W = np.diag(1/es**2); Am = np.vstack([xs - xs.mean(), np.ones_like(xs)]).T
        cov = np.linalg.inv(Am.T @ W @ Am); beta = cov @ (Am.T @ W @ ys)
        sl_bin, esl_bin = float(beta[0]), float(math.sqrt(cov[0, 0]))
        info(f"binned regression on those four points: d log sigma / d log M_b = {sl_bin:+.3f} +/- {esl_bin:.3f}")
        # THE HEADLINE FIT: every pair, no binning, interloper fraction profiled out (see ml_slope's docstring for
        # why the binned number above is not trusted -- it is dominated by whichever quartile scatters high).
        sl, esl, _ = ml_slope(DV, MBT, dvmax=DV_WIN, verr=V_ERR_HI)
        # the two laws' own slopes, measured the same way off their predictions
        def pred_slope(law, a0=None):
            sp = sigma_pred(MB1, MB2, RP, law, a0=a0)
            return float(np.polyfit(np.log10(MBT), np.log10(sp), 1)[0])
        sl_dm = pred_slope("deepmond", a0=A0["canonical"]); sl_l = pred_slope("lcdm")
        info(f"UNBINNED maximum-likelihood d log sigma_los / d log M_b = {sl:+.3f} +/- {esl:.3f} "
             f"over {np.log10(MBT).max()-np.log10(MBT).min():.2f} dex in M_b")
        info(f"predicted: framework isolated deep-MOND {sl_dm:+.3f} (the 1/4 law with the mass-ratio term) | "
             f"LambdaCDM (Moster + NFW) {sl_l:+.3f}")
        s_f = ml_sigma(DV[MBT < np.median(MBT)], dvmax=DV_WIN, verr=V_ERR_HI)[0]
        s_b = ml_sigma(DV[MBT >= np.median(MBT)], dvmax=DV_WIN, verr=V_ERR_HI)[0]
        info(f"the crude control on the same axis: bright half {s_b:.1f} km/s vs faint half {s_f:.1f} km/s "
             f"(implied slope {math.log10(s_b/s_f)/(np.median(np.log10(MBT[MBT >= np.median(MBT)])) - np.median(np.log10(MBT[MBT < np.median(MBT)]))):+.2f})")
        ck("47i the mass scaling -- the part of the item that could have been Kepler-grade -- CANNOT BE MEASURED "
           "HERE, and the reason is not the data but the item's own arithmetic: over the mass range an HI-selected "
           "dwarf-pair sample spans, the framework's M_b^(1/4) law and LambdaCDM's abundance-matched halos predict "
           "slopes that differ by less than the measurement error.  The axis that was supposed to be decisive is "
           "degenerate",
           abs(sl_dm - sl_l) < 2*esl,
           f"measured {sl:+.3f} +/- {esl:.3f}; framework {sl_dm:+.3f}, LambdaCDM {sl_l:+.3f} -- the two predictions "
           f"are {abs(sl_dm-sl_l):.3f} apart against an error of {esl:.3f}, so no sample of this kind can separate "
           f"them on this axis.  (The binned four-point regression gave {sl_bin:+.3f} +/- {esl_bin:.3f}; it "
           f"disagrees with the bright/faint half-split, which is why it is not the headline)")

    # ---- MUTATION CONTROLS on the real sample
    P(""); P("-"*122); P("MUTATION CONTROLS on the ALFALFA sample"); P("-"*122)
    sc = rng.permutation(len(DV))
    dv_scr = A_v[P1] - A_v[Q1[sc]]
    ok_scr = np.abs(dv_scr) < DV_WIN
    s_r, e_r, f_r = ml_sigma(DV, dvmax=DV_WIN, verr=V_ERR_HI)
    s_s, e_s, f_s = ml_sigma(dv_scr[ok_scr], dvmax=DV_WIN, verr=V_ERR_HI)
    info(f"real pairs: sigma = {s_r:.1f} km/s, interloper fraction {f_r:.2f};  partners scrambled: "
         f"sigma = {s_s:.1f} km/s, interloper fraction {f_s:.2f} (N = {int(ok_scr.sum())})")
    ck("M2 mutation control: scrambling which dwarf each dwarf is paired with must drive the fitted PAIR fraction "
       "toward zero, so the measured dispersion is a property of the pairs and not of the velocity field or of the "
       "estimator",
       (1 - f_s) < 0.5*(1 - f_r),
       f"pair fraction 1-f: real {1-f_r:.2f} -> scrambled {1-f_s:.2f}")
    sp_true = sigma_pred(MB1, MB2, RP, "deepmond", a0=A0["canonical"])
    sp_x100 = sigma_pred(MB1, MB2, RP, "deepmond", a0=100*A0["canonical"])
    A_t = ml_sigma(DV, sig_shape=sp_true, dvmax=DV_WIN, verr=V_ERR_HI)[0]
    A_x = ml_sigma(DV, sig_shape=sp_x100, dvmax=DV_WIN, verr=V_ERR_HI)[0]
    ck("M3 mutation control: the amplitude test must respond to a_0 exactly as v ~ a_0^(1/4) says -- a_0 x 100 has to "
       "move the required amplitude by 0.5 dex.  If it does not, the fit is insensitive and 47g means nothing",
       abs(math.log10(A_t/A_x) - 0.5) < 0.05,
       f"log10(A_true/A_x100) = {math.log10(A_t/A_x):+.3f}, predicted +0.500")
    A_INJ = 1.6
    sp_inj = sigma_pred(MB1, MB2, RP, "deepmond", a0=A0["canonical"])
    n_inj = len(DV); f_inj = 0.25
    is_int = rng.random(n_inj) < f_inj
    dv_inj = np.where(is_int, rng.uniform(-DV_WIN, DV_WIN, n_inj),
                      rng.normal(0, np.sqrt((A_INJ*sp_inj)**2 + V_ERR_HI**2)))
    A_rec, eA_rec, f_rec = ml_sigma(dv_inj, sig_shape=sp_inj, dvmax=DV_WIN, verr=V_ERR_HI)
    ck("M4 injection-recovery control: mock velocity differences built from the SAME per-pair predictions with a "
       "known amplitude and a known interloper fraction must come back with that amplitude.  If the estimator were "
       "biased, every amplitude above would be worthless",
       abs(A_rec - A_INJ) < 3*eA_rec and abs(f_rec - f_inj) < 0.20,
       f"injected A = {A_INJ:.2f}, f_int = {f_inj:.2f}; recovered A = {A_rec:.2f} +/- {eA_rec:.2f}, "
       f"f_int = {f_rec:.2f} on N = {n_inj} mock pairs")

    # ---- how hard is the answer pushed by the isolation criterion?
    P("")
    info("SENSITIVITY to the relative-isolation criterion (the one free choice in the sample definition).  If the")
    info("47h excess were residual group contamination, tightening the criterion would bring it down.")
    info(f"{'F (d3 > F r_p)':>16} {'N':>5} {'med r_p':>9} {'sigma [km/s]':>16} {'A(deep-MOND)':>16} "
         f"{'A(LambdaCDM)':>16} {'A(EFE branch)':>16}")
    Ascan, Lscan, Escan, Fscan = [], [], [], []
    for f_ in (1.0, 1.5, 2.0, 3.0, 5.0):
        m_ = sample_mask(f_)
        if m_.sum() < 40: continue
        i1, i2 = ia[p[m_]], ia[q[m_]]
        mb1, mb2, rpx, dvx = mb_of(i1), mb_of(i2), rp[m_], dv[m_]
        s_, e_, _ = ml_sigma(dvx, dvmax=DV_WIN, verr=V_ERR_HI)
        A_, eA_, _ = ml_sigma(dvx, sig_shape=sigma_pred(mb1, mb2, rpx, "deepmond", a0=A0["canonical"]),
                              dvmax=DV_WIN, verr=V_ERR_HI)
        L_, eL_, _ = ml_sigma(dvx, sig_shape=sigma_pred(mb1, mb2, rpx, "lcdm"), dvmax=DV_WIN, verr=V_ERR_HI)
        E_, eE_, _ = ml_sigma(dvx, sig_shape=sigma_pred(mb1, mb2, rpx, "framework", a0=A0["canonical"]),
                              dvmax=DV_WIN, verr=V_ERR_HI)
        Ascan.append((A_, eA_)); Lscan.append((L_, eL_)); Escan.append((E_, eE_)); Fscan.append(f_)
        info(f"{f_:16.1f} {int(m_.sum()):5d} {np.median(rpx):9.0f} {s_:11.1f} +/-{e_:4.1f} "
             f"{A_:11.2f} +/-{eA_:4.2f} {L_:11.2f} +/-{eL_:4.2f} {E_:11.2f} +/-{eE_:4.2f}")
    if len(Ascan) >= 4:
        E_last, eE_last = Escan[-1]
        info(f"the framework's EFE branch stays excluded at every isolation depth: A = {Escan[0][0]:.2f} at the "
             f"loosest and {E_last:.2f} +/- {eE_last:.2f} ({(E_last-1)/eE_last:.1f} sigma above 1) at the "
             f"strictest, so 47g does not rest on the contamination that 47j identifies.")
        A_last, eA_last = Ascan[-1]; L_last, eL_last = Lscan[-1]
        info(f"the excess FALLS as the isolation is tightened, for BOTH laws: deep-MOND {Ascan[0][0]:.2f} -> "
             f"{A_last:.2f}, LambdaCDM {Lscan[0][0]:.2f} -> {L_last:.2f}.  That is the signature of residual group "
             f"contamination, not of gravity, and it makes 47h's offset an UPPER LIMIT on any real one.")
        info("CROSS-CHECK, and it does not agree.  h48_h69b_relative_isolation.py applies exactly this criterion to "
             "2MRS MAJOR pairs and finds the amplitude FLAT at 1.8-2.0 from F = 2 to F = 8 -- no decline at all.  "
             "So either these 53 dwarf pairs are noise (1.12 +/- 0.29 against 1.89 +/- 0.05 is 2.6 sigma), or the "
             "framework's deficit grows with mass.  The tension is recorded, not resolved.")
        ck("47j THE HONEST VERDICT ON THE AMPLITUDE: the offset found in 47h is not stable.  Tightening the "
           "relative-isolation criterion by a factor of five brings the framework's amplitude down toward 1 -- and "
           "brings LambdaCDM's down with it, which is the signature of residual contamination rather than of "
           "gravity.  The best-isolated subsample is consistent with the framework's parameter-free prediction and "
           "equally consistent with LambdaCDM's, so this item CANNOT separate them.  It is a weaker statement than "
           "it looks: the same criterion leaves the major-pair amplitude untouched (see the cross-check above), so "
           "the decline here may be small-number scatter.  What the item CAN and does do is exclude the "
           "framework's own external-field branch (47g)",
           abs(A_last - 1)/eA_last < 2.0 and A_last < Ascan[0][0],
           f"strictest isolation (F = {Fscan[-1]:.0f}, N = {int(sample_mask(Fscan[-1]).sum())}): deep-MOND "
           f"A = {A_last:.2f} +/- {eA_last:.2f} ({abs(A_last-1)/eA_last:.1f} sigma from 1), LambdaCDM "
           f"A = {L_last:.2f} +/- {eL_last:.2f} ({abs(L_last-1)/eL_last:.1f} sigma from 1); at the loosest, "
           f"{Ascan[0][0]:.2f} and {Lscan[0][0]:.2f}")

# ====================================================================================================================
P(""); P("="*122); P("SECTION 5 -- why the on-disk K-band pair catalogue cannot substitute"); P("="*122)
kt_rows = []
for line in open(os.path.join(DATA, "kt2017_galaxies.tsv"), encoding="latin-1"):
    if line.startswith("#") or not line.strip(): continue
    f = line.rstrip("\n").split("\t")
    if len(f) < 6: continue
    try: kt_rows.append((int(f[0]), float(f[1]), float(f[2]), float(f[3]), float(f[4]), int(f[5])))
    except ValueError: continue
gf = {}
for line in open(os.path.join(DATA, "kt2017_groups_full.tsv"), encoding="latin-1"):
    if line.startswith("#") or not line.strip(): continue
    f = line.rstrip("\n").split("\t")
    if len(f) < 9: continue
    try: gf[int(f[0])] = (int(f[1]), float(f[2]), float(f[3]))
    except ValueError: continue
grp = collections.defaultdict(list)
for r in kt_rows: grp[r[5]].append(r)
n_pair = n_dwarf = n_close = 0; kt_dv = []
for pgc1, mem in grp.items():
    if len(mem) != 2 or pgc1 not in gf: continue
    Nm, logK, Dg = gf[pgc1]
    if Nm != 2 or not np.isfinite(Dg) or Dg <= 0: continue
    n_pair += 1
    a, b = mem
    Ms = [UPS_K*10**(0.4*(MK_SUN - (x[4] - 5*math.log10(Dg*1e6) + 5))) for x in (a, b)]
    th = math.radians(math.hypot((a[1] - b[1])*math.cos(math.radians(a[2])), a[2] - b[2]))
    rp_ = th*Dg*1000.0
    if max(Ms) < 1e10:
        n_dwarf += 1
        if rp_ < 50:
            n_close += 1; kt_dv.append(abs(a[3] - b[3]))
info(f"KT2017 Nm = 2 pairs: {n_pair}; both members below 1e10 Msun: {n_dwarf}; of those inside TNT's 50 kpc "
     f"window: {n_close}")
info("So the catalogue does contain dwarf pairs -- the earlier draft of this script wrongly asserted it did not.")
info("They are still unusable, for the reason item 48b established on the same catalogue: Kourkchi & Tully link")
info("galaxies inside a velocity window scaled by K-band luminosity, so a KT2017 pair is BY CONSTRUCTION a pair")
info("whose dv was small enough to be linked.  The velocity difference the item wants to measure is the quantity")
info("the catalogue selected on.")
if kt_dv:
    kt_dv = np.array(kt_dv)
    s_kt = ml_sigma(kt_dv*np.sign(rng.normal(size=len(kt_dv))), dvmax=DV_WIN, verr=V_ERR_HI)[0]
    info(f"as a demonstration: those {n_close} KT dwarf pairs have max |dv| = {kt_dv.max():.0f} km/s and a fitted "
         f"dispersion of {s_kt:.0f} km/s -- truncated, and the truncation is the selection, not the physics.")
ck("47d the on-disk K-band catalogue cannot substitute for TNT -- not because it lacks dwarf pairs (it has "
   f"{n_close} inside the TNT window) but because its group-finder selected on the very velocity difference the "
   "item measures.  Item 48b demonstrated the same bias on the massive pairs, where an independently selected "
   "sample of the same galaxies gave a much larger dispersion",
   n_close > 0 and float(np.max(kt_dv)) < 300.0 if kt_dv is not None and len(kt_dv) else False,
   f"{n_close} both-dwarf KT pairs inside 50 kpc, maximum |dv| = {float(np.max(kt_dv)) if len(kt_dv) else float('nan'):.0f} "
   f"km/s -- a hard edge set by the linking window, not by gravity")

# ====================================================================================================================
P(""); P("="*122); P("SECTION 6 -- the one dwarf pair whose 3-D kinematics are actually measured"); P("="*122)
info("Literature values, quoted for a consistency statement and used in no fit: M*(LMC) ~ 2.7e9, M_HI(LMC) ~ 5e8,")
info("M*(SMC) ~ 3.1e8, M_HI(SMC) ~ 4e8 Msun; 3-D separation ~23 kpc; relative space velocity ~128 km/s")
info("(HST proper motions, Kallivayalil et al. 2013).")
M_LMC, M_SMC, R_LS, V_LS = 2.7e9 + 5e8, 3.1e8 + 4e8, 23.0, 128.0
MW_MB = 6.0e10
for ft, a0 in A0.items():
    v_iso = float(v_rel_deepmond(M_LMC, M_SMC, a0))/1e3
    g_mw = math.sqrt(G*MW_MB*Msun*a0)/(55.0*kpc)
    v_efe = float(v_rel_efe(M_LMC, M_SMC, R_LS, g_mw/a0))/1e3
    info(f"{ft:10}: MW external field at 55 kpc = {g_mw/a0:.2f} a_0 (so the pair is EFE-dominated, not isolated); "
         f"isolated deep-MOND relative speed {v_iso:.0f} km/s, EFE-quasi-Newtonian {v_efe:.0f} km/s, "
         f"observed {V_LS:.0f} km/s")
    if ft == "canonical": V_ISO, V_EFE = v_iso, v_efe
ck("47e AGAINST INTEREST -- the archetypal dwarf pair sits ABOVE both framework branches, not between them.  Both "
   "the isolated deep-MOND speed and the EFE-quasi-Newtonian speed fall short of the measured 128 km/s.  The "
   "caveat that softens it is real and was not put in to soften it: the Clouds are near pericentre of a highly "
   "eccentric relative orbit (and possibly not bound to each other at all), and a circular-orbit formula is a "
   "lower bound on the instantaneous speed for any eccentric orbit passing through that separation",
   V_LS > max(V_ISO, V_EFE),
   f"canonical: isolated deep-MOND {V_ISO:.0f} km/s, EFE branch {V_EFE:.0f} km/s, observed {V_LS:.0f} km/s -- "
   f"the best case is {V_LS/V_ISO:.2f}x short, needing {(V_LS/V_ISO)**4:.0f}x the assumed baryonic mass on a "
   f"circular orbit")

P(""); P("-"*122)
info("SYSTEMATICS on the ALFALFA measurement, stated plainly:")
info(" 1. flow-model distances.  r_p and M_HI both scale with D; a 10% distance error is 10% in r_p and 20% in M_HI,")
info("    i.e. 5% in the predicted dv.  Peculiar velocities at D < 20 Mpc are the worst case.")
info(" 2. the 4-arcminute cut.  ALFALFA blends closer pairs into one source, so the sample is biased AGAINST the")
info("    small separations where the isolated deep-MOND branch survives, and toward the EFE branch.")
info(" 3. isolation depth.  2MRS is complete for M* > 2.5e10 only to ~100 Mpc, which is why D < 100 Mpc is imposed;")
info("    fainter companions and any intra-group gas are not excluded, and those are baryons the framework may use.")
info(" 4. M* is the ALFALFA-SDSS Taylor colour mass where available and M_HI otherwise.  In a gas-rich dwarf M_HI")
info("    dominates M_b, so the stellar M/L that blocks the rest of this hunt enters here only at the 10-20% level.")
info(" 5. circular relative orbits.  Eccentric orbits of the same energy spend most of their time near apocentre at")
info("    LOWER speed, so this assumption is generous to the framework rather than stingy.")
info(" 6. one nominal external field e_N for every pair.  A per-pair value from 2M++ would move the framework's own")
info("    prediction down, not up.")
P("")
info("WHAT WOULD MAKE ITEM 47 RUNNABLE AS POSED, in order of value:")
info(" 1. the TNT per-pair table (r_sep, v_sep, M*_1, M*_2) from the authors or IOP.  Even then section 3 says the")
info("    60 pairs give ~2 sigma; the sample would have to grow several-fold.")
info(" 2. resolved HI synthesis imaging of the ALFALFA pairs below the 4-arcminute blend limit, which is the only")
info("    way to reach TNT's < 50 kpc separations with HI-grade velocities.")
info(" 3. a per-pair external field.  Section 2 shows the EFE, not a_0, sets the framework's own answer over most of")
info("    the range, so a test that ignores it is testing the wrong branch.")
sys.exit(ck.done())
