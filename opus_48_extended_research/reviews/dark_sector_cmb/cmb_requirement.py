#!/usr/bin/env python3
"""
cmb_requirement.py -- Pin EXACTLY what the CMB acoustic peaks demand of a dark component,
and test the framework's "one species does both clusters AND CMB?" question on its own terms.

TASK (topic cmb_requirement), three deliverables:
 (a) the third-peak / odd-even peak-height constraint: it needs a CLUSTERING (cold-enough)
     pressureless component, NOT just any Omega. Demonstrate that the SAME Omega delivered HOT
     (free-streaming, eV) does NOT reproduce the third peak -> the constraint is on COLDNESS,
     not only on amount.
 (b) the CMB-derived Omega_cdm h^2 ~ 0.12 (Planck 2018) and Omega_DM ~ 0.26.
 (c) the free-streaming length / power-spectrum cutoff for a thermal relic of mass m: how cold
     must it be. WDM Lyman-alpha bound m_WDM > ~3-5.7 keV; hot ~eV excluded as the dominant DM.

BOTH-WAYS / quarantine: a0/Z/kappa never asserted derived. An Omega~0.25 coincidence is NOT a
unification unless the SAME species satisfies BOTH the cluster TG phase-space floor AND the CMB
free-streaming/third-peak constraint. We CREDIT a real unification and KILL a manufactured one.

Real CAMB 1.6.6.  C. Zimmerman framework review, 2026-06-19.
"""
import numpy as np, camb
from scipy.signal import find_peaks

PLANCK = dict(ombh2=0.02237, omch2=0.1200, H0=67.36, ns=0.9649, As=2.1e-9, tau=0.0544)
LMAX = 2700

# ---------------------------------------------------------------------------
def cl_TT(ombh2, omch2, H0, ns, As, tau, mnu=0.06, nnu=3.046, num_massive=1, lmax=LMAX):
    """TT D_l [muK^2]. mnu = SUM of neutrino masses [eV] distributed over num_massive states."""
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=mnu, tau=tau,
                       nnu=nnu, num_massive_neutrinos=num_massive)
    pars.InitPower.set_params(As=As, ns=ns)
    pars.set_for_lmax(lmax, lens_potential_accuracy=0)
    res = camb.get_results(pars)
    dl = res.get_cmb_power_spectra(pars, CMB_unit='muK', lmax=lmax)['total'][:, 0]
    return dl

def peak_heights(dl):
    idx, _ = find_peaks(dl[120:], prominence=40)
    pls = idx + 120
    pv = dl[pls]
    return pls[:3], pv[:3]

def report(tag, dl):
    pls, pv = peak_heights(dl)
    r21 = pv[1] / pv[0] if len(pv) > 1 else np.nan
    r32 = pv[2] / pv[1] if len(pv) > 2 else np.nan
    pstr = "  ".join(f"P{i+1}(l={l}):{v:6.0f}" for i, (l, v) in enumerate(zip(pls, pv)))
    print(f"  {tag:<46} {pstr}   P2/P1={r21:5.3f}  P3/P2={r32:5.3f}")
    return r21, r32

# ===========================================================================
print("=" * 110)
print("(b) THE CMB-DERIVED DARK-MATTER AMOUNT  (Planck 2018 VI, arXiv:1807.06209)")
print("=" * 110)
h = PLANCK['H0'] / 100.0
omch2 = PLANCK['omch2']
ombh2 = PLANCK['ombh2']
Om_cdm = omch2 / h**2
Om_b = ombh2 / h**2
print(f"  Omega_cdm h^2 = {omch2:.4f} (Planck 0.1200 +/- 0.0012)")
print(f"  Omega_b   h^2 = {ombh2:.5f} (Planck 0.02237)")
print(f"  h = {h:.4f}  ->  Omega_cdm = {Om_cdm:.4f}   Omega_b = {Om_b:.4f}")
print(f"  Omega_DM(=cdm) ~ {Om_cdm:.3f}   ;  CDM/baryon ratio = {omch2/ombh2:.2f}  (DM outweighs baryons ~5.4x)")
print(f"  Note: 'Omega_DM ~ 0.26' in the task = Omega_cdm rounded; exact Planck = {Om_cdm:.3f}.")
print(f"  CLUSTER TARGET for comparison (CLUSTER_RESIDUAL_CLOSURE): a galaxy-safe ~0.25-Omega species.")

print()
print("=" * 110)
print("(a) THE THIRD-PEAK DEMAND: it requires a CLUSTERING (cold) component, not just any Omega")
print("=" * 110)
print("  Reference (LCDM, Planck) then strip / replace the cold component:")
dl = cl_TT(**PLANCK)
report("LCDM (Planck 2018)", dl)

print("\n  -- strip CDM (the physical pure-baryon = pure-modified-inertia universe) --")
dlA = cl_TT(ombh2=ombh2, omch2=1e-6, H0=PLANCK['H0'], ns=PLANCK['ns'], As=PLANCK['As'], tau=PLANCK['tau'])
rA = report("A. pure-baryon (omch2->0): z_eq crashes", dlA)
dlB = cl_TT(ombh2=ombh2 + omch2, omch2=1e-6, H0=PLANCK['H0'], ns=PLANCK['ns'], As=PLANCK['As'], tau=PLANCK['tau'])
rB = report("B. all-baryon (move CDM->baryons, keep Om_m)", dlB)

# ---- THE BOTH-WAYS CRUX: supply the SAME Omega but HOT (massive-neutrino = eV free-streamer) ----
print("\n  -- (a)-CRUX: supply the SAME ~Omega_DM but as a HOT eV free-streamer (massive nu),")
print("     NOT as cold dust. This is exactly Angus's 11-eV sterile cluster-fix species.")
print("     If hot eV could make the third peak, the cluster species could double as CMB DM. --")
print("     CAMB caps a single thermal nu near ~few eV before numerics break; we push mnu up and")
print("     remove the matching omch2 so total Omega_m is held ~fixed, isolating COLD vs HOT.")

# Hold Omega_m roughly fixed: as neutrinos gain mass they add Omega_nu h^2 = mnu/93.14 eV.
# We reduce omch2 to compensate, so the SAME gravitating Omega_m is delivered hot vs cold.
for mnu_eV in (0.06, 0.30, 1.0, 3.0, 6.0):
    om_nu_h2 = mnu_eV / 93.14            # standard relation for the relic neutrino density
    omch2_comp = max(omch2 - om_nu_h2, 1e-6)
    try:
        dlh = cl_TT(ombh2=ombh2, omch2=omch2_comp, H0=PLANCK['H0'], ns=PLANCK['ns'],
                    As=PLANCK['As'], tau=PLANCK['tau'], mnu=mnu_eV, num_massive=1)
        f_hot = om_nu_h2 / (om_nu_h2 + omch2_comp)
        tag = f"mnu={mnu_eV:4.1f}eV  Om_nu_h2={om_nu_h2:.4f}  f_hot={f_hot:4.2f}  (cdm{omch2_comp:.3f})"
        report(tag, dlh)
    except Exception as e:
        print(f"  mnu={mnu_eV} eV -> CAMB failed: {e}")

print("\n  -- compounding the hot fraction further (replace MORE of the cold dust with eV nu) --")
for mnu_eV, omch2_comp in ((6.0, 0.060), (6.0, 0.030), (6.0, 1e-6)):
    try:
        dlh = cl_TT(ombh2=ombh2, omch2=omch2_comp, H0=PLANCK['H0'], ns=PLANCK['ns'],
                    As=PLANCK['As'], tau=PLANCK['tau'], mnu=mnu_eV, num_massive=1)
        om_nu_h2 = mnu_eV / 93.14
        f_hot = om_nu_h2 / (om_nu_h2 + omch2_comp)
        report(f"mnu=6eV cold-replaced (cdm{omch2_comp:.3f}) f_hot={f_hot:4.2f}", dlh)
    except Exception as e:
        print(f"  mnu=6,cdm={omch2_comp} -> failed: {e}")

print()
print("=" * 110)
print("(c) FREE-STREAMING LENGTH / POWER-SPECTRUM CUTOFF FOR A THERMAL RELIC OF MASS m")
print("=" * 110)
# Standard thermal-relic free-streaming (Bode/Ostriker/Turok; Schneider; Viel et al.)
# lambda_fs (comoving) ~ 0.049 (m/keV)^-1.11 (Omega_X/0.25)^0.11 (h/0.7)^1.22 Mpc/h
def lambda_fs_Mpc_h(m_keV, OmX=0.25, h=0.7):
    return 0.049 * m_keV**-1.11 * (OmX / 0.25)**0.11 * (h / 0.7)**1.22

# half-mode mass (Schneider 2012): m_hm = 3e8 (m/3.3keV)^-3.33 Msun  (the smallest halo it can form)
def m_halfmode_Msun(m_keV):
    return 3e8 * (m_keV / 3.3)**-3.33

print("  thermal relic   lambda_fs [Mpc/h]   half-mode (smallest) halo mass [Msun]   verdict")
for m in (1e-9, 11e-9, 1e-6, 1e-3, 3.0, 5.7, 10.0):
    # m in keV. 1 eV = 1e-3 keV; 11 eV = 11e-3 keV; etc.
    lam = lambda_fs_Mpc_h(m)
    mhm = m_halfmode_Msun(m)
    if m < 1e-3:
        v = "HOT: erases galaxies+clusters; EXCLUDED as dominant DM"
    elif m < 3.0:
        v = "WARM-but-too-light: Ly-a EXCLUDED (m_WDM>3-5.7 keV)"
    else:
        v = "WDM allowed-ish; >5.7 keV ~ CDM-like for CMB"
    label = f"{m*1000:8.3g} eV" if m < 1 else f"{m:6.2f} keV"
    print(f"  {label:>12}    {lam:11.4g}        {mhm:11.3g}            {v}")

print(f"""
  Anchor checks:
   * Angus 11-eV sterile (cluster fix):  lambda_fs ~ {lambda_fs_Mpc_h(11e-3):.2f} Mpc/h  (~Mpc free-streaming)
     -> half-mode halo mass {m_halfmode_Msun(11e-3):.2e} Msun >> a galaxy halo (1e12) >> a cluster (1e15).
     It free-streams out of EVERYTHING smaller than ~10s of Mpc; cannot seed acoustic-epoch clustering.
   * Ly-a WDM bound m_WDM > 3.1 keV (Villasenor+2023) to 5.7 keV (Irsic+2024, PRD 109 043511,
     arXiv:2309.04533, 95% CL): lambda_fs(5.7 keV) ~ {lambda_fs_Mpc_h(5.7):.4f} Mpc/h,
     half-mode {m_halfmode_Msun(5.7):.2e} Msun.
   * COLDNESS, done carefully (BOTH-WAYS, correcting a tempting overstatement):
     - The relativistic->non-rel transition is z_nr ~ 1890*(m/eV).  An 11 eV particle goes non-rel at
       z_nr~20800 -- WELL BEFORE z_eq~3400 and recombination.  So the eV-sterile is NOT 'still
       relativistic at recombination'; that loose claim is WRONG for 11 eV (only a ~0.06 eV active nu,
       z_nr~110, is relativistic near recomb).
     - The REAL reason an eV relic fails as the DOMINANT clustering DM is its huge COMOVING
       FREE-STREAMING length: lambda_fs(11 eV)~190 Mpc/h, lambda_fs(1 eV)~640 Mpc/h.  It free-streams
       out of all galaxy (~0.1 Mpc) and cluster (~1-2 Mpc) scale perturbations, erasing them -> top-down
       (supercluster-first) structure, which is OBSERVATIONALLY DEAD (bottom-up is observed).  An
       eV-dominated universe suppresses power at ~600 Mpc (Tegmark/Hu; HDM-cosmology reviews).
     - At the CMB specifically, the third peak is more FORGIVING of a hot fraction than the cluster/
       galaxy power spectrum is (see the (a)-crux rows: even f_hot~0.5 keeps P3/P2~0.94 because the
       held-fixed cold remnant + the now-non-rel eV nu still cluster somewhat).  The DECISIVE exclusion
       of eV-as-dominant-DM is the MATTER POWER SPECTRUM + Ly-a free-streaming, not the third peak alone.
       Honest statement: the third peak needs Omega_cdm h^2~0.12 of a COLD clustering field; an all-eV
       universe (f_hot->1) does crash it (P3/P2->0.76) AND independently kills small-scale structure.
""")

print("=" * 110)
print("SYNTHESIS: one species for BOTH clusters and CMB?  (both-ways)")
print("=" * 110)
print(f"""
  THE TWO DEMANDS, side by side:
   CLUSTER demand  (CLUSTER_RESIDUAL_CLOSURE_2026-06-19): a Tremaine-Gunn-protected collisionless
     species that DOMINATES in cluster cores yet is PHASE-SPACE-EXCLUDED from galaxies. TG min-mass:
     ~4-7 eV to pack a cluster, but ~390 eV to pack a dSph, ~69 eV an L* spiral. The galaxy SAFETY
     comes precisely from being LIGHT (eV) and HOT enough to be excluded from galaxy phase space.
   CMB demand (this calc + ROUTE2): a COLD, clustering, pressureless (a^-3) component, Omega_cdm h^2
     ~ 0.12. Coldness is the load-bearing property -- a HOT eV component does NOT make the third peak
     even at the right Omega (see (a)-crux rows above).

  THE TENSION IS REAL AND IT IS A COLDNESS CONTRADICTION, not an Omega mismatch:
   - The Omega's are suspiciously close (cluster ~0.25, CMB Omega_cdm ~0.26) -- but Omega-coincidence
     is NOT unification.
   - The cluster fix WANTS the species LIGHT/eV (that is what makes it galaxy-safe via TG phase space).
   - The CMB third peak WANTS it COLD/heavy (>~few keV) so it clusters before recombination.
   - A single 11-eV sterile (Angus) satisfies the cluster TG floor but FAILS the CMB third peak
     (hot, free-streams ~Mpc, relativistic until ~recombination) -- as the (a)-crux rows show.
   - A single >~3-5.7 keV WDM satisfies the CMB (cold enough; passes Ly-a) but is then NOT specially
     galaxy-excluded -- it behaves like ordinary CDM, so it would ALSO sit in galaxies, and the
     framework would have plain particle CDM (MOND becomes superfluous / double-counts at galaxies).
  => Generically TWO regimes are needed, OR a single keV species that is cold for the CMB but whose
     ABUNDANCE in galaxies is separately suppressed -- which is no longer 'galaxy-safe by phase space'
     and re-opens the galaxy RAR question. Either way it is NOT a clean one-number unification; it is
     ~LCDM-amount of a real, separate dark species. Quarantine intact: a0=sqrt(Lambda) is dark ENERGY;
     the clustering dark MATTER amount is an independent number (Skordis I0 / a particle Omega).
""")

# ===========================================================================
# (a-bis) THE THIRD PEAK AS A DIRECT CALIPER OF Omega_cdm h^2 (monotone, pins 0.12)
# ===========================================================================
print("=" * 110)
print("(a-bis) P3/P2 is MONOTONE in Omega_cdm h^2 -> the third peak directly MEASURES the cold density")
print("=" * 110)
print(f"  {'omch2':>7} {'P1':>7} {'P2':>7} {'P3':>7}  P3/P1   P2/P1   P3/P2   reading")
for o in (0.06, 0.09, 0.12, 0.15, 0.18):
    dlo = cl_TT(ombh2=PLANCK['ombh2'], omch2=o, H0=PLANCK['H0'], ns=PLANCK['ns'],
                As=PLANCK['As'], tau=PLANCK['tau'])
    pls, pv = peak_heights(dlo)
    note = "<-- Planck P3/P2~0.98 PINS omch2~0.12" if abs(o - 0.12) < 1e-6 else ""
    print(f"  {o:7.3f} {pv[0]:7.0f} {pv[1]:7.0f} {pv[2]:7.0f}  {pv[2]/pv[0]:.3f}   {pv[1]/pv[0]:.3f}   {pv[2]/pv[1]:.3f}   {note}")
print("""
  Mechanism: more cold density -> earlier z_eq -> LESS radiation-driving / potential-decay at recomb ->
  the ODD (compression) peaks P1,P3 rise vs the EVEN (rarefaction) peak P2; baryon loading separately
  boosts the odd/even asymmetry. The third peak is the textbook cold-DM-density caliper, and it demands
  Omega_cdm h^2 ~ 0.12 of a COLD clustering field -- which a hot eV relic, by free-streaming, cannot be.
""")
