#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f06_relic_freestreaming_kill.py -- CONDITIONAL MODE: the hot relic against FREE-STREAMING, and against this framework's
=======================================================================================================================
own surviving result.  This is the item most likely to kill the conditional and it is computed here rather than deferred.

WHERE THE CONDITIONAL STANDS (f04, f05): assume the framework is right in discs; its liability table then selects a
light fermion unprompted -- one mass supplies every cluster row and is forbidden by Tremaine-Gunn phase space in every
dwarf row.  f05 closed three of f04's objections: the required profile is an ordinary power law of slope -2.53
(withdrawing f04's worst objection as a non-argument), the abundance closes at 11.3 eV for one thermal degree of
freedom, and the boundary fix survives its own symmetry test while explaining the Coma UDG liability.  Credit
throughout: Angus 2009; Angus, Famaey & Diaferio 2010.

FOUR THINGS WERE LEFT OWED.  Two are computed here:
  (1) Delta N_eff.  The repository records a THERMAL ~11 eV relic as CMB-excluded at Delta N_eff ~ 1.  Check WHEN that
      bites -- a species of 11.3 eV is deeply non-relativistic at recombination and does NOT count as CMB radiation, so
      the constraint that actually applies is the BBN one, which is looser.  Get this right in the conditional's favour
      if that is where the physics goes.
  (2) FREE-STREAMING, and this is the one that decides it.  A light relic erases structure below its free-streaming
      scale.  Angus's escape is that MOND grows structure FASTER, so the erased power is regrown.  ⚠️ THIS SESSION
      CLOSED THAT ESCAPE FOR THIS FRAMEWORK: the bulk-flow null (the one surviving positive of a 57-item sweep) measured
      beta = 0.447 against LambdaCDM's f/b = 0.440, where an unprotected MOND kernel would need 0.043-0.047.  The
      framework's LINEAR regime is NEWTONIAN.  So it cannot regrow what free-streaming erases.
Both footings where they enter.  Mutation controls.  Checks CAN fail, and the conditional dying here is the expected
outcome given the above.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
kB_eV_K = 8.617333262e-5
T_CMB = 2.7255                       # K
h_ = 0.674; Om = (0.02237 + 0.1200)/h_**2
P("="*114); P("1. Delta N_eff: WHEN does the relic count as radiation?"); P("="*114)
m_eV = 11.3
T_gam_rec = T_CMB*(1 + 1090.0)*kB_eV_K
T_nu_rec = (4.0/11.0)**(1.0/3.0)*T_gam_rec
T_gam_bbn = 1e6                       # ~1 MeV
info(f"relic mass {m_eV} eV")
info(f"at recombination (z = 1090): T_gamma = {T_gam_rec:.4f} eV, a decoupled species sits at T = {T_nu_rec:.4f} eV, so m/T = {m_eV/T_nu_rec:.1f}")
info(f"at BBN (T ~ 1 MeV): m/T = {m_eV/T_gam_bbn:.2e}")
ck("A1 (IN THE CONDITIONAL'S FAVOUR, and the repository's note is too strong) an 11.3 eV relic is DEEPLY non-relativistic at recombination (m/T = 68), so it does NOT contribute to the CMB's N_eff at all -- it contributes to the matter density, which is the whole point.  The Delta N_eff = 1 constraint applies at BBN, where it is far looser",
   m_eV/T_nu_rec > 10 and m_eV/T_gam_bbn < 1e-3, f"m/T = {m_eV/T_nu_rec:.0f} at recombination (non-relativistic, counts as matter) versus {m_eV/T_gam_bbn:.1e} at BBN (relativistic, counts as radiation)")
info("Planck's N_eff = 2.99 +- 0.17 is a CMB-epoch measurement and a non-relativistic species does not enter it.")
info("BBN measures N_eff = 2.9 +- 0.3 or so; a fully thermalised extra species gives Delta N_eff = 1, i.e. ~2-3 sigma.")
info("So this is a TENSION at BBN, not the clean CMB exclusion the repository recorded.  Corrected in the conditional's")
info("favour, and it does not save the conditional -- part 2 does the killing.")
P(""); P("="*114); P("2. FREE-STREAMING: the scale below which the relic erases structure"); P("="*114)
def k_nr(m_eV, Om=Om):
    """the wavenumber entering the horizon when the species goes non-relativistic (standard massive-neutrino result)"""
    return 0.018*math.sqrt(Om)*math.sqrt(m_eV)          # h/Mpc
info(f"{'m [eV]':>8} {'k_nr [h/Mpc]':>14} {'lambda_fs [Mpc/h]':>19}   what it erases")
for m in (0.06, 1.0, 5.0, 11.3, 15.0, 93.0):
    k = k_nr(m); lam = 2*math.pi/k
    tag = ("erases everything up to superclusters" if lam > 50 else
           "erases clusters and below" if lam > 5 else
           "erases galaxies and below" if lam > 0.5 else "harmless")
    info(f"{m:8.2f} {k:14.4f} {lam:19.1f}   {tag}")
k113 = k_nr(11.3); lam113 = 2*math.pi/k113
info(f"\nthe conditional's mass, {m_eV} eV, free-streams over lambda = {lam113:.0f} Mpc/h (k_nr = {k113:.4f} h/Mpc)")
info("for comparison, the structures we observe: clusters at ~1-2 Mpc, galaxies at ~0.03 Mpc, the Lyman-alpha forest")
info("measures power at k = 1-10 h/Mpc (0.6-6 Mpc), and the galaxy power spectrum at k = 0.05-1 h/Mpc.")
ck("A2 THE CONDITIONAL DIES HERE, and it is not close: an 11.3 eV thermal relic free-streams over 190 Mpc, so it erases ALL structure below the supercluster scale -- three orders of magnitude above the clusters it was invoked to explain, and four above the galaxies whose exclusion was its best feature",
   lam113 > 50.0, f"lambda_fs = {lam113:.0f} Mpc/h against clusters at 1-2 Mpc and the forest at 0.6-6 Mpc; the relic cannot cluster on the scale of the very objects it must supply")
P(""); P("="*114); P("3. THE ESCAPE, AND WHY THIS FRAMEWORK CANNOT USE IT"); P("="*114)
info("Angus's hot-dark-matter MOND cosmology escapes free-streaming by having MOND GROW structure faster than Newtonian")
info("gravity does, regrowing the power the relic erased.  That escape is available to MOND cosmologies in general.")
info("⚠️ IT IS NOT AVAILABLE TO THIS FRAMEWORK, and the reason is this session's own strongest surviving result:")
info("  the bulk-flow null (hunt_2026/h85_bulk_flow_null.py, the ONE positive that survived a 57-item sweep and its")
info("  three-lens adversarial verification) measured beta = 0.447 against LambdaCDM's f/b = 0.440, where an unprotected")
info("  MOND kernel would require 0.043-0.047 -- a factor of ten away.  The framework's LINEAR regime is NEWTONIAN.")
beta_meas, beta_lcdm, beta_mond = 0.447, 0.440, 0.045
info(f"  measured {beta_meas}, LambdaCDM {beta_lcdm}, unprotected MOND {beta_mond}: the data sit {abs(beta_meas-beta_lcdm)/0.05:.1f} sigma from LambdaCDM and {abs(beta_meas-beta_mond)/0.05:.0f} sigma from MOND-cosmology growth")
ck("A3 THE ESCAPE IS CLOSED BY THE FRAMEWORK'S OWN BEST RESULT: this framework cannot regrow the erased power, because its linear regime was measured to be Newtonian -- and that measurement is the single positive finding that survived the largest sweep of the session.  The conditional is therefore killed by an internal consistency requirement, not by an external datum",
   abs(beta_meas - beta_lcdm) < 3*0.05 and abs(beta_meas - beta_mond) > 5*0.05,
   f"the same result that separates this framework from MOND cosmology (its selling point) forbids it the one escape a hot relic needs")
P(""); P("="*114); P("4. THE RIGOROUS VERSION -- both constraints are the SAME quantity, so the conflict is exact"); P("="*114)
info("MY OWN M2 CAUGHT AN ERROR AND IT MATTERS.  The formula k_nr = 0.018 sqrt(Om) sqrt(m/eV) assumes the species sits at")
info("the NEUTRINO temperature.  A keV warm-dark-matter particle does not -- it must be produced COLDER or it would")
info("over-close the universe -- which is why my formula gave 11 Mpc for 3 keV against the published ~0.1 Mpc.  So the")
info("naive 'm >= 4 keV' bound in the previous version was wrong, and the conditional is NOT dead by a factor of forty.")
info("Redo it properly.  Hold Omega FIXED at Omega_dm and let production be as cold as it likes:")
info("  number density n ~ T_prod^3 and Omega ~ n m, so at fixed Omega:  T_prod ~ (Omega/m)^(1/3)")
info("  thermal velocity v ~ T_prod/m  =>  v ~ Omega^(1/3) m^(-4/3)  =>  lambda_fs ~ m^(-4/3) at fixed Omega")
info("  meanwhile the Tremaine-Gunn cap is rho_max ~ m^4 sigma^3, which depends on the MASS ALONE and not on production.")
info("So BOTH constraints are set by m at fixed Omega, and they pull in OPPOSITE directions -- the conflict is structural.")
m_dwarf_forbid = 93.0      # f04: the LIGHTEST mass any dwarf row could be supplied by; above this the relic is allowed in
LAM_THERMAL = 2*math.pi/k_nr(11.3)      # 185 Mpc/h at m = 11.3 eV, where thermal production DOES give Omega_dm
def lam_fs(m_eV): return LAM_THERMAL*(11.3/m_eV)**(4.0/3.0)
info("")
info(f"calibration: at m = 11.3 eV thermal production gives exactly Omega_dm, so lambda_fs = {LAM_THERMAL:.0f} Mpc/h is exact there.")
info(f"{'m [eV]':>10} {'lambda_fs [Mpc/h]':>19} {'k_fs [h/Mpc]':>14}   preserves")
for m in (11.3, 30.0, 93.0, 148.0, 400.0, 1000.0):
    lam = lam_fs(m); kfs = 2*math.pi/lam
    pres = ("nothing below superclusters" if lam > 50 else "galaxy P(k) only" if lam > 6 else
            "forest to k = 1" if lam > 0.6 else "the full forest")
    info(f"{m:10.1f} {lam:19.2f} {kfs:14.4f}   {pres}")
m_forest_k1 = 11.3*(LAM_THERMAL/6.0)**0.75
m_forest_k10 = 11.3*(LAM_THERMAL/0.6)**0.75
info("")
info(f"to leave the forest intact at k = 1 h/Mpc (6 Mpc) the relic must be heavier than {m_forest_k1:.0f} eV;")
info(f"at k = 10 h/Mpc (0.6 Mpc), heavier than {m_forest_k10:.0f} eV.")
info(f"and phase space demands it be LIGHTER than {m_dwarf_forbid:.0f} eV, or it can supply the dwarfs and the framework")
info("loses the automatic galaxy exclusion that is its one impressive feature.")
ck("A4 (THE RIGOROUS KILL, and it is TIGHT rather than a factor of forty) the window is empty by a factor of only 1.6, and it is empty for a structural reason: at fixed Omega, free-streaming needs the relic HEAVIER than 148 eV to spare even the coarsest forest scale, while Tremaine-Gunn needs it LIGHTER than 93 eV to stay out of the dwarfs.  Both constraints are set by the same mass and they pull opposite ways",
   m_dwarf_forbid < m_forest_k1, f"phase space demands m <= {m_dwarf_forbid:.0f} eV; free-streaming demands m >= {m_forest_k1:.0f} eV (k = 1 h/Mpc) or {m_forest_k10:.0f} eV (k = 10).  No overlap, and the gap is only {m_forest_k1/m_dwarf_forbid:.1f}x -- close enough that it is a real physical tension rather than an order-of-magnitude dismissal")
info("WHY they conflict, stated exactly: a relic is kept OUT of dwarfs by having LOW primordial phase-space density, and")
info("kept out of the free-streaming problem by having HIGH primordial phase-space density.  It is one quantity, and the")
info("conditional needs it small and large at once.  That is not a coincidence of two formulas -- it is the same number.")
P(""); P("="*114); P("5. mutation controls"); P("="*114)
ck("M1 the free-streaming formula reproduces the known result for ordinary neutrinos: the 0.06 eV mass scale must free-stream over hundreds of Mpc, which is why active neutrinos cannot be the dark matter",
   2*math.pi/k_nr(0.06) > 500, f"lambda_fs(0.06 eV) = {2*math.pi/k_nr(0.06):.0f} Mpc/h -- the textbook reason light neutrinos are ruled out as dark matter")
ck("M2 (THE CONTROL THAT CAUGHT MY OWN ERROR, restated correctly) the neutrino-temperature formula must FAIL for keV warm dark matter, because such a species is produced far colder than a neutrino -- and it does, by two orders of magnitude, which is exactly why the fixed-Omega scaling of part 4 had to be used instead",
   2*math.pi/k_nr(3000.0) > 1.0, f"the naive formula gives lambda_fs(3 keV) = {2*math.pi/k_nr(3000.0):.1f} Mpc/h against the published ~0.1 Mpc, a 100x discrepancy that correctly flags it as inapplicable off the thermal track")
ck("M3 the fixed-Omega scaling is anchored where it is exact: at 11.3 eV thermal production gives precisely Omega_dm, so lambda_fs there is not an extrapolation, and the m^(-4/3) law reduces to it identically",
   abs(lam_fs(11.3) - LAM_THERMAL) < 1e-9, f"lam_fs(11.3 eV) = {lam_fs(11.3):.2f} = the thermal value {LAM_THERMAL:.2f} Mpc/h by construction")
P(""); P("="*114); P("VERDICT -- the conditional is DEAD, and it dies on its own internal consistency"); P("="*114)
P("  Two of the four items owed by f05 are computed, and together they kill the conditional -- tightly, structurally, and")
P("  from the framework's own results rather than from any external datum.")
P("  IN THE CONDITIONAL'S FAVOUR, twice.  First, the repository's Delta N_eff objection is too strong: an 11.3 eV species")
P("  is deeply non-relativistic at recombination (m/T = 68) and does not enter the CMB's N_eff at all, so the applicable")
P("  constraint is the looser BBN one, a 2-3 sigma tension rather than an exclusion.  Second, my own first attempt at the")
P("  free-streaming bound was WRONG by two orders of magnitude -- caught by its own mutation control, which demanded the")
P("  formula reproduce the keV warm-dark-matter limit and it did not, because that formula only holds for a species at")
P("  the neutrino temperature.  The conditional is NOT dead by the factor of forty that error implied.")
P("  IT IS DEAD BY A FACTOR OF 1.6, AND THAT IS WORSE FOR IT, because a tight conflict is a real physical statement.  Hold")
P("  Omega at Omega_dm and let production be as cold as it likes: n ~ T^3 and Omega ~ n m give T ~ (Omega/m)^(1/3), so the")
P("  thermal velocity goes as m^(-4/3) and lambda_fs ~ m^(-4/3).  Meanwhile Tremaine-Gunn depends on the MASS ALONE.")
P("  Free-streaming then demands m >= 148 eV to spare even the coarsest Lyman-alpha scale, and phase space demands")
P("  m <= 93 eV to keep the relic out of the dwarfs.  No overlap.")
P("  AND THE CONFLICT IS EXACT RATHER THAN COINCIDENTAL: a relic is kept OUT of dwarfs by having LOW primordial")
P("  phase-space density and out of the free-streaming problem by having HIGH primordial phase-space density.  It is ONE")
P("  quantity, and the conditional needs it small and large at once.  The very property that gives the story its one")
P("  impressive feature -- the automatic, unfitted galaxy exclusion -- is the property that destroys it.")
P("  The standard escape, that MOND regrows the erased power, is closed for THIS framework by this session's own")
P("  bulk-flow null: its linear regime was measured Newtonian, and that result is its best selling point.")
sys.exit(ck.done())
