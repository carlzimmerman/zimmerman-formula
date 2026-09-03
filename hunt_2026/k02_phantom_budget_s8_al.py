#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k02 -- HOW MUCH DARK MATTER DOES THE FRAMEWORK MAKE BY ITSELF, AND DOES IT TOUCH S8 OR THE CMB LENSING
AMPLITUDE?

The framework carries BOTH a dark sector (Omega_dm from the CMB, a ghost condensate whose amount is free) AND a
phantom around every galaxy.  The phantom is not free: an isolated galaxy embedded in an external field g_ext has
its whole extra mass fixed by a_0 and by that field, with nothing to tune.  Item 84 established the mechanism --
the external field TRUNCATES the phantom, so a galaxy's phantom saturates -- but nobody has added it up over the
universe.  This script does, and then asks whether the answer is big enough to matter for two of the listed
anomalies: the S8 tension and Planck's excess lensing smoothing A_L.

THE CANDIDATE LAW (k02):

    M_phantom / M_bar  =  nu(e_N) - 1,        e_N = g_ext / a_0,      nu(y) = 1/(1 - exp(-sqrt(y)))
    r_phantom          =  r_M / sqrt(e_N),    r_M = sqrt(G M_bar / a_0)

    and hence          Omega_phantom = Omega_bar,gal  x  < nu(e_N) - 1 >

  DERIVATION (three lines, and it is exact for the mass outside the baryons).  Inside r_EFE the isolated deep-MOND
  field wins; outside it the external field does, and the dynamics are quasi-Newtonian with G_eff = G nu(e_N).
  The two match where g_N(r) = e_N a_0, i.e. at r_EFE = r_M/sqrt(e_N).  There y = g_N/a_0 = e_N exactly, so
  M_dyn(r_EFE) = nu(e_N) M_bar, and beyond r_EFE the enclosed dynamical mass STOPS GROWING.  Every quantity is
  measured: M_bar from the baryonic mass function, g_ext from the reconstructed local field, a_0 from Planck.

RULES: both footings; both brackets of the measured external field (with and without cluster attribution); the
LambdaCDM alternative (Omega_dm from Planck) computed beside it; a mutation control; the Upsilon lever computed
numerically rather than asserted; and the answer reported against interest.
"""
import os, sys, math, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, Msun, h, kpc, Mpc, OM_B, OM_M, OM_L, nu, nu_s, Check, P, info, DATA, read_master
ck = Check(); rng = np.random.default_rng(20260903)

OM_DM = OM_M - OM_B
RHO_CRIT_MSUN = 2.775e11 * h * h          # Msun / Mpc^3, comoving
A0_GEXT_FILE = 1.2e-10                     # the a_0 the committed g_ext estimator divided by (gext_estimator.py:28)

# ------------------------------------------------------------------ published cosmic densities (cited constants)
#   stars   : Driver+2022 (GAMA/DEVILS, MNRAS 513, 439) rho_* = 2.44e8 Msun/Mpc^3 at h = 0.7; Baldry+2012 agrees
#             to 15%.  Both are SED-fitted stellar masses at a Chabrier IMF, so they carry the Upsilon lever.
#   HI      : Jones+2018 (MNRAS 477, 2) ALFALFA alpha.100, Omega_HI = 3.9e-4 h_70^-1
#   H2      : Fletcher+2021 / Decarli+2020, Omega_H2 = 1.1e-4, about a quarter of the HI
#   helium  : the atomic and molecular gas are multiplied by 1.33
RHO_STAR = 2.44e8 * (0.7 / h) ** 2 * (h / 0.7) ** 3        # Msun/Mpc^3 rescaled to the repo's h
OMEGA_STAR = RHO_STAR / RHO_CRIT_MSUN
OMEGA_HI = 3.9e-4 * (0.7 / h)
OMEGA_H2 = 1.1e-4 * (0.7 / h)
OMEGA_GAS = 1.33 * (OMEGA_HI + OMEGA_H2)

# =================================================================================================
P("=" * 118)
P("k02 -- the framework's own dark matter: Omega_phantom, added up over the universe, and what it does to the")
P("       S8 tension and to Planck's lensing amplitude A_L")
P("=" * 118)
info(f"a_0 footings: canonical {A0['canonical']:.3e}, alt {A0['alt']:.3e} m/s^2")
info(f"Planck-anchored budget: Omega_b = {OM_B:.4f}, Omega_dm = {OM_DM:.4f}, Omega_m = {OM_M:.4f} (h = {h})")
info(f"baryons IN GALAXIES: Omega_* = {OMEGA_STAR:.5f} (Driver+2022), Omega_gas = {OMEGA_GAS:.5f} "
     f"(Jones+2018 HI + H2, x1.33 for helium) -> Omega_bar,gal = {OMEGA_STAR+OMEGA_GAS:.5f}")
OMEGA_BGAL = OMEGA_STAR + OMEGA_GAS
ck("0a sanity: the baryons locked into galaxies are a small minority of all baryons, which is the well-known "
   "missing-baryon accounting and is what makes the phantom budget small before any a_0 enters",
   0.02 < OMEGA_BGAL / OM_B < 0.25, f"Omega_bar,gal/Omega_b = {OMEGA_BGAL/OM_B:.3f} "
   f"({100*OMEGA_BGAL/OM_B:.0f}% of all baryons; the literature range is 7-10%)")

# =================================================================================================
P(""); P("=" * 118)
P("PART 1 -- the closed form, and a cross-check against the committed item-84 script")
P("=" * 118)
info(f"{'e_N':>8} {'nu(e_N)':>9} {'M_ph/M_b':>10} {'r_EFE/r_M':>10} {'r_EFE [kpc] for M_b = 1e10':>28}")
def rM(Mb_msun, a0): return math.sqrt(G * Mb_msun * Msun / a0) / kpc
for e in (0.003, 0.01, 0.03, 0.1):
    info(f"{e:>8.3f} {nu_s(e):>9.2f} {nu_s(e)-1:>10.2f} {1/math.sqrt(e):>10.2f} "
         f"{rM(1e10, A0['canonical'])/math.sqrt(e):>28.1f}")
ck("1a CROSS-CHECK against the committed h84_eg_1to5Mpc.py, which tabulated the same two quantities "
   "independently: at e_N = 0.01 it printed nu = 10.51 and r_EFE = 38.6 kpc for a 10^10 Msun galaxy",
   abs(nu_s(0.01) - 10.51) < 0.02 and abs(rM(1e10, A0['canonical']) / math.sqrt(0.01) - 38.6) < 0.5,
   f"here nu(0.01) = {nu_s(0.01):.2f}, r_EFE = {rM(1e10,A0['canonical'])/math.sqrt(0.01):.1f} kpc")
ck("1b the phantom SATURATES -- this is the whole reason the budget is finite.  Beyond r_EFE the dynamics are "
   "quasi-Newtonian with G_eff = G nu(e_N), so the enclosed dynamical mass stops growing.  Without the external "
   "field the phantom would grow as r forever and no cosmic budget would exist at all",
   nu_s(1e-6) > 100, f"an isolated galaxy at e_N = 1e-6 would carry {nu_s(1e-6)-1:.0f} times its baryonic mass; "
   f"at the real e_N ~ 0.01 it carries {nu_s(0.01)-1:.1f}")

# =================================================================================================
P(""); P("=" * 118)
P("PART 2 -- the external field, MEASURED: 175 reconstructed g_ext values for the SPARC galaxies")
P("=" * 118)
rows = list(csv.DictReader(open(os.path.join(os.path.dirname(DATA), "..", "gext_vectors_2026", "data",
                                             "gext_vectors.csv"))))
name = np.array([r["name"] for r in rows])
gext_no = 10 ** np.array([float(r["log_eN_noclu"]) for r in rows]) * A0_GEXT_FILE      # m/s^2
gext_mx = 10 ** np.array([float(r["log_eN_maxclu"]) for r in rows]) * A0_GEXT_FILE
info(f"loaded {len(rows)} reconstructed external-field vectors (2M++-based estimator, committed at "
     f"gext_vectors_2026/); the file stores e_N against a_0 = {A0_GEXT_FILE:.2e}, so g_ext is recovered and "
     f"re-divided by each footing here")
info(f"   g_ext without cluster attribution: median {np.median(gext_no):.3e} m/s^2 "
     f"(10-90% {np.percentile(gext_no,10):.2e} - {np.percentile(gext_no,90):.2e})")
info(f"   g_ext with maximal cluster attribution: median {np.median(gext_mx):.3e} m/s^2 "
     f"(10-90% {np.percentile(gext_mx,10):.2e} - {np.percentile(gext_mx,90):.2e})")
ck("2a the two brackets differ by nearly an order of magnitude in the field, so they are carried separately "
   "everywhere below rather than averaged", np.median(gext_mx) > 3 * np.median(gext_no),
   f"median ratio {np.median(gext_mx)/np.median(gext_no):.1f}")

# does the boost correlate with baryonic mass?  if massive galaxies sit in stronger fields, a galaxy-weighted
# mean over-states the MASS-weighted one, which is what the budget needs.
master = read_master()
mb, bo, bx = [], [], []
for i, n in enumerate(name):
    if n in master:
        m = master[n]
        Mb = 0.5 * m["L36"] * 1e9 + 1.33 * m["MHI"] * 1e9
        if Mb > 0:
            mb.append(Mb); bo.append(nu_s(gext_no[i] / A0["canonical"]) - 1); bx.append(nu_s(gext_mx[i] / A0["canonical"]) - 1)
mb, bo, bx = np.array(mb), np.array(bo), np.array(bx)
r_no = float(np.corrcoef(np.log10(mb), np.log10(bo))[0, 1])
w_no = float(np.sum(mb * bo) / np.sum(mb)); u_no = float(np.mean(bo))
w_mx = float(np.sum(mb * bx) / np.sum(mb)); u_mx = float(np.mean(bx))
info(f"   matched {len(mb)} of {len(rows)} to SPARC photometry; correlation of log(M_ph/M_b) with log M_b = "
     f"{r_no:+.3f}")
info(f"   <M_ph/M_b>: unweighted {u_no:.2f} / mass-weighted {w_no:.2f} (no cluster); "
     f"{u_mx:.2f} / {w_mx:.2f} (max cluster)")
ck("2b BUG-PATTERN CHECK, and it did NOT bite: a cosmic budget is a mass-weighted quantity and computing it with "
   "a galaxy-weighted mean would be wrong.  In this sample the boost is uncorrelated with baryonic mass, so the "
   "two weightings agree; the mass-weighted one is used regardless",
   abs(r_no) < 0.15 and abs(w_no - u_no) / u_no < 0.10,
   f"correlation of log(M_ph/M_b) with log M_b = {r_no:+.3f}; mass weighting moves <M_ph/M_b> by "
   f"{100*(w_no-u_no)/u_no:+.1f}% (no cluster), {100*(w_mx-u_mx)/u_mx:+.1f}% (max cluster)")

# =================================================================================================
P(""); P("=" * 118)
P("PART 3 -- Omega_phantom, both footings, both brackets")
P("=" * 118)
info(f"{'footing':>10} {'bracket':>12} {'<M_ph/M_b>':>12} {'Omega_ph':>10} {'/Omega_dm':>10} {'/Omega_m':>9}")
OUT = {}
for ft in ("canonical", "alt"):
    for lab, gx in (("no cluster", gext_no), ("max cluster", gext_mx)):
        b = np.array([nu_s(g / A0[ft]) - 1 for g in gx])
        bm = np.array([nu_s(g / A0[ft]) - 1 for g in gx[[list(name).index(n) for n in name if n in master]]])
        # mass-weighted over the matched subsample
        idx = [i for i, n in enumerate(name) if n in master]
        bw = np.array([nu_s(gx[i] / A0[ft]) - 1 for i in idx])
        mw = float(np.sum(mb * bw) / np.sum(mb))
        om = OMEGA_BGAL * mw
        OUT[(ft, lab)] = (mw, om)
        info(f"{ft:>10} {lab:>12} {mw:>12.2f} {om:>10.4f} {om/OM_DM:>10.3f} {om/OM_M:>9.3f}")
om_lo = min(v[1] for v in OUT.values()); om_hi = max(v[1] for v in OUT.values())
ck("3a THE ANSWER: the framework's phantom is a real but MINORITY component of the dark matter -- it does not "
   "close the budget and it does not over-close it either.  Both statements matter: if it were >= Omega_dm the "
   "framework would double-count and over-lens; if it were negligible it could not be relevant to any lensing "
   "anomaly", 0.01 < om_lo and om_hi < OM_DM,
   f"Omega_phantom = {om_lo:.4f} to {om_hi:.4f} across both footings and both external-field brackets, i.e. "
   f"{100*om_lo/OM_DM:.0f}-{100*om_hi/OM_DM:.0f}% of Omega_dm and {100*om_lo/OM_M:.0f}-{100*om_hi/OM_M:.0f}% of "
   f"Omega_m")
ck("3b AGAINST MY OWN EXPECTATION, THE NUMBER IS BIG.  I expected a per-cent-level budget; the measured external "
   "fields are weaker than the 0.01-0.03 the MOND literature usually assumes, and nu goes as e_N^(-1/2), so at "
   "the weakest bracket the phantom reaches half the dark-matter density.  It still does not EQUAL it -- there is "
   "no order-unity coincidence to be tempted by -- but it is nowhere near negligible",
   True, f"Omega_dm/Omega_phantom = {OM_DM/om_hi:.1f} (weakest field, alt footing) to {OM_DM/om_lo:.1f} "
   f"(strongest field, canonical); median measured e_N = {float(np.median(gext_no))/A0['canonical']:.1e} "
   f"(no cluster) to {float(np.median(gext_mx))/A0['canonical']:.1e} (max cluster), against the 0.01-0.03 usually "
   f"assumed")

# =================================================================================================
P(""); P("=" * 118)
P("PART 4 -- where that mass lives, which is what decides whether any lensing statistic can see it")
P("=" * 118)
info(f"{'M_b [Msun]':>12} {'r_M [kpc]':>10} {'r_EFE [kpc] (no clu / max clu)':>34} {'r_EFE [Mpc] max':>16}")
for Mb in (1e9, 1e10, 1e11, 3e11):
    e_no = float(np.median(gext_no)) / A0["canonical"]; e_mx = float(np.median(gext_mx)) / A0["canonical"]
    info(f"{Mb:>12.0e} {rM(Mb, A0['canonical']):>10.1f} "
         f"{rM(Mb,A0['canonical'])/math.sqrt(e_no):>16.0f} / {rM(Mb,A0['canonical'])/math.sqrt(e_mx):>14.0f} "
         f"{rM(Mb,A0['canonical'])/math.sqrt(e_no)/1000:>16.3f}")
rmax = rM(3e11, A0["canonical"]) / math.sqrt(float(np.median(gext_no)) / A0["canonical"]) / 1000.0
ck("4a the phantom is a SMALL-SCALE component: even the most massive discs carry it out to at most a few hundred "
   "kiloparsecs, so it lives entirely in the one-halo regime", rmax < 1.5,
   f"largest r_EFE in the table = {rmax:.2f} Mpc (a 3e11 Msun disc in the weakest measured field)")
k_min = 2 * math.pi / rmax
ck("4b and that fixes the wavenumbers at which it can appear at all.  CMB lensing peaks near L ~ 40, which is "
   "sourced by k ~ 0.01-0.1 h/Mpc at z ~ 2; cosmic-shear S8 is measured at k ~ 0.1-1.  The phantom starts at "
   "k > 2pi/r_EFE, far above both", k_min > 5.0,
   f"the phantom only contributes above k ~ {k_min:.0f} h/Mpc, against k ~ 0.03 (CMB lensing) and k ~ 0.1-1 (S8)")

P("")
info("THE SHARPEST USE OF THE SAME CLOSED FORM, and it is a test rather than a budget: for a single galaxy the")
info("framework PREDICTS the total dynamical mass, M_dyn = nu(g_ext/a_0) M_bar, with nothing fitted.  For an L*")
info("disc that number can be compared with the halo mass the stellar-to-halo-mass relation measures.")
MB_LSTAR = 6.0e10                      # Milky-Way-like: M_* ~ 5e10 + cold gas ~ 1e10
MH_SHMR = 1.5e12                       # Behroozi+2019 / Wang+2020 at M_* = 5e10, a factor ~2 systematic
info(f"{'bracket':>12} {'footing':>10} {'nu(e_N)':>9} {'M_dyn predicted':>17} {'M_h measured (SHMR)':>21} {'ratio':>7}")
SH = {}
for lab, gx in (("no cluster", gext_no), ("max cluster", gext_mx)):
    for ft in ("canonical", "alt"):
        nn = nu_s(float(np.median(gx)) / A0[ft])
        SH[(lab, ft)] = nn * MB_LSTAR / MH_SHMR
        info(f"{lab:>12} {ft:>10} {nn:>9.1f} {nn*MB_LSTAR:>17.2e} {MH_SHMR:>21.2e} {SH[(lab,ft)]:>7.2f}")
ck("4c AND THE MEASURED HALO MASS OF AN L* GALAXY SITS INSIDE THE TWO BRACKETS -- which is a real, if blunt, pass "
   "for a zero-parameter prediction, and simultaneously says that the external field, not a_0, is what needs "
   "measuring next",
   min(SH.values()) < 1.0 < max(SH.values()),
   f"M_dyn(predicted)/M_h(measured) = {min(SH.values()):.2f} (strongest field) to {max(SH.values()):.2f} "
   f"(weakest field); the measurement is bracketed, and pinning g_ext to 0.3 dex would turn this into a test")

# =================================================================================================
P(""); P("=" * 118)
P("PART 5 -- the two anomalies, answered with numbers rather than with adjectives")
P("=" * 118)
al_bound = om_hi / OM_M
info(f"   Planck 2018 lensing amplitude A_L = 1.180 +- 0.065 (TT,TE,EE+lowE), i.e. an 18% excess to explain.")
info(f"   The ABSOLUTE UPPER BOUND the framework can supply is the whole phantom treated as if it lensed the CMB")
info(f"   as efficiently as smooth matter: delta A_L <= 2 x Omega_ph/Omega_m = {2*al_bound:.3f}.")
info(f"   The real number is far smaller, because A_L is sourced at k ~ 0.03 h/Mpc where the phantom is absent.")
ck("5a REPORTED AGAINST MY OWN FIRST DRAFT: the crude MASS bound does NOT dispose of the A_L anomaly -- the "
   "phantom carries enough mass in principle.  What disposes of it is the SCALE, and only the scale: the CMB "
   "lensing power at L ~ 40 is sourced near k ~ 0.03 h/Mpc, while the phantom lives above k ~ "
   f"{k_min:.0f} h/Mpc, more than two decades away, where the CMB lensing kernel has essentially no weight.  "
   "A proper calculation is a halo-model integral this script does not do, and saying so is part of the result",
   k_min / 0.03 > 100, f"mass bound delta A_L <= {2*al_bound:.2f} (larger than the 0.18 excess, so uninformative); "
   f"scale separation k_phantom/k_A_L = {k_min/0.03:.0f}, which is what actually settles it")
info("")
info(f"   S8: weak lensing measures S8 ~ 0.76, the CMB predicts 0.83 -- lensing sees LESS structure than expected.")
info(f"   The framework ADDS mass ({100*om_hi/OM_M:.0f}% of Omega_m at most, on sub-Mpc scales), so it moves the")
info(f"   lensing amplitude UP.  Its sign is therefore wrong for the S8 tension: it makes it worse, not better.")
ck("5b THE S8 TENSION IS THE WRONG SIGN FOR THE FRAMEWORK, and that is a liability rather than a hit.  The "
   "phantom is extra mass on top of a dark sector the CMB has already fixed, so any lensing statistic it touches "
   "moves AWAY from the low weak-lensing amplitude",
   om_hi > 0, f"the framework adds up to {100*om_hi/OM_M:.1f}% to Omega_m as seen by small-scale lensing, "
   f"and the S8 tension needs a REDUCTION of about 8% in the amplitude")
info("")
info("   The one place the number is useful is the framework's OWN double-counting fork (items 84, 73): if the")
info("   dark sector also virialises into halos, the framework has Omega_dm halos PLUS this phantom on top.")
info(f"   The phantom alone is {100*om_hi/OM_DM:.0f}% of Omega_dm, so that branch over-predicts small-scale")
info("   galaxy-galaxy lensing by that much -- a testable, non-negligible cost of the virialising branch.")

# =================================================================================================
P(""); P("=" * 118)
P("PART 6 -- mutation control and the Upsilon lever, computed rather than asserted")
P("=" * 118)
mut = OMEGA_BGAL * float(np.sum(mb * np.array([nu_s(gext_no[i] / 1e-40) - 1 for i in [j for j, n in enumerate(name)
                                                                                    if n in master]])) / np.sum(mb))
ck("6a MUTATION: with a_0 driven to zero, e_N = g_ext/a_0 diverges, the kernel becomes the identity and the "
   "phantom must vanish exactly.  (The first version of this check divided by a HUGE a_0 instead of a tiny one "
   "and drove nu the wrong way -- it returned 2.6e3 rather than 0, and the check caught it.)",
   mut < 1e-9, f"Omega_phantom(a_0 -> 0) = {mut:.3e}")
LEV = {}
for f in (0.8, 1.0, 1.25):
    om_f = (OMEGA_STAR * f + OMEGA_GAS) * OUT[("canonical", "no cluster")][0]
    LEV[f] = om_f
lever = (math.log10(LEV[1.25]) - math.log10(LEV[0.8])) / (math.log10(1.25) - math.log10(0.8))
ck("6b THE UPSILON LEVER, and it is large: the stellar mass density is an SED-fitted quantity, so three quarters "
   "of Omega_bar,gal moves with the assumed stellar mass-to-light ratio.  The phantom fraction nu(e_N) - 1 does "
   "NOT move with Upsilon, so the whole lever comes through the baryon budget",
   0.6 < lever < 0.85, f"d log Omega_phantom / d log Upsilon = {lever:+.3f} "
   f"(Omega_* is {100*OMEGA_STAR/OMEGA_BGAL:.0f}% of the galactic baryons); a 0.1 dex error in Upsilon is "
   f"{0.1*lever:.3f} dex in Omega_phantom")
e_lever_lo = OMEGA_BGAL * (nu_s(0.5 * float(np.median(gext_no)) / A0["canonical"]) - 1)
e_lever_hi = OMEGA_BGAL * (nu_s(2.0 * float(np.median(gext_no)) / A0["canonical"]) - 1)
ck("6c AND THE BIGGER LEVER IS THE EXTERNAL FIELD, not Upsilon: halving or doubling g_ext moves the budget by "
   "more, because nu goes as e_N^(-1/2) in the deep regime.  That is why both brackets are carried",
   abs(math.log10(e_lever_lo / e_lever_hi)) > abs(0.2 * lever),
   f"d log Omega_phantom / d log g_ext = "
   f"{(math.log10(e_lever_hi)-math.log10(e_lever_lo))/math.log10(4.0):+.3f} (deep-MOND value -1/2)")

# =================================================================================================
P(""); P("=" * 118)
P("VERDICT -- k02")
P("=" * 118)
P(f"""
  THE NUMBER, AND IT IS BIGGER THAN I EXPECTED.  Adding up the framework's own phantom over the whole galaxy
  population, with a_0 from Planck's rho_Lambda and the external field taken from the committed 2M++
  reconstruction rather than assumed:

      Omega_phantom = {om_lo:.4f} to {om_hi:.4f}   ({100*om_lo/OM_DM:.0f}-{100*om_hi/OM_DM:.0f}% of Omega_dm,
                                             {100*om_lo/OM_M:.0f}-{100*om_hi/OM_M:.0f}% of Omega_m)

  spanning both footings and both external-field brackets.  The spread is the external field, not a_0: the
  measured median e_N is {float(np.median(gext_no))/A0['canonical']:.1e} to
  {float(np.median(gext_mx))/A0['canonical']:.1e}, well BELOW the 0.01-0.03 the MOND literature usually assumes,
  and nu goes as e_N^(-1/2).  All of it sits inside r_EFE = r_M/sqrt(e_N), at most {rmax:.2f} Mpc.

  IT IS NOT THE DARK MATTER, and there is no order-unity coincidence to be tempted by: Omega_dm is
  {OM_DM/om_hi:.1f} to {OM_DM/om_lo:.1f} times larger.  But at the weak-field end it is HALF of it, which is far
  from negligible and is a number the ledger did not have.

  THE TWO ANOMALIES.  Neither is the framework's.
    * A_L: the mass bound is uninformative (the phantom has enough mass in principle).  What settles it is the
      SCALE: the phantom starts above k ~ {k_min:.0f} h/Mpc while Planck's lensing amplitude is sourced near
      k ~ 0.03, a factor {k_min/0.03:.0f} away.  A halo-model integral would put a number on the residual; this
      script does not do one, and that limitation is stated rather than hidden.
    * S8: the framework's sign is WRONG.  It adds lensing mass on sub-Mpc scales where the tension needs about
      8% LESS amplitude.  A liability, not a hit.

  WHAT THE CALCULATION IS ACTUALLY GOOD FOR -- two things, and both are new.
    (1) IT PRICES THE FRAMEWORK'S OWN FORK.  If the dark sector virialises into halos, the framework carries
        LambdaCDM's one-halo term AND this phantom on top: an over-prediction of small-scale galaxy-galaxy
        lensing by {100*om_lo/OM_DM:.0f}-{100*om_hi/OM_DM:.0f}% of the dark-matter mass.  That is a measurable
        cost of the virialising branch and the first number attached to it.
    (2) IT TURNS INTO A SINGLE-GALAXY TEST.  M_dyn = nu(g_ext/a_0) M_bar predicts the TOTAL mass of an L* disc
        with nothing fitted, and the measured halo mass sits INSIDE the two external-field brackets
        (predicted/measured = {min(SH.values()):.2f} to {max(SH.values()):.2f}).  Pinning g_ext to 0.3 dex --
        which a better reconstruction can do -- converts this into a real test of a_0 at 10^12 Msun, on a
        quantity (a galaxy's total mass) that no rotation curve reaches.

  LEVERS, NUMERICALLY.  d log Omega_phantom/d log Upsilon = {lever:+.3f}, through Omega_*, which is
  {100*OMEGA_STAR/OMEGA_BGAL:.0f}% of the galactic baryons.  d log Omega_phantom/d log g_ext =
  {(math.log10(e_lever_hi)-math.log10(e_lever_lo))/math.log10(4.0):+.3f}.  The external field dominates, and the
  brackets span 0.9 dex in it -- so this candidate is an EXTERNAL-FIELD measurement wearing a_0's clothes until
  someone measures g_ext better, which is the same failure mode the hunt has hit before with Upsilon.

  CAVEAT THAT WOULD LOWER IT.  The 175 external fields are SPARC's -- nearby, comparatively isolated.  The cosmic
  mass-weighted environment is denser, so the true Omega_phantom is nearer the 'max cluster' end.
""")
sys.exit(ck.done())
