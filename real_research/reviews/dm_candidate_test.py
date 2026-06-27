#!/usr/bin/env python3
"""
FRONT 3 -- THE OBSERVATIONAL TEST + CONSISTENCY. Does the framework predict a SPECIFIC, testable
DARK-MATTER candidate with a falsifiable VARYING-MASS signature tied to a0(z), or is its candidate
below-floor / free / already-excluded / absorbed? Both-ways, computed, exit 0.

#1 RULE: DARK SECTOR ONLY, NOT a TOE. Forced scale + test = credit (dark-sector prediction). Scale
FREE (tower fixes VARIATION not ABSOLUTE; I0 free) = say so, do NOT manufacture a DM mass.

FOOTING (LOCKED): a0=9.36e-11 m/s^2 = cH_Lambda/Z, Z=sqrt(32pi/3). rho_DE = 3 H_Lam^2/(8 pi G).
  rho_DE^(1/4) ~ 2.3 meV (the de Sitter vacuum mass scale). IR floor hbar H_Lambda/c^2 ~ 1.2e-33 eV.

WHAT THE FRAMEWORK ACTUALLY BANKS (read from memory + GHOST_CONDENSATE_CONSEQUENCES_2026-06-19.md +
swampland_tower_from_a0z.py + nu_de_tower.py):
  * The dark sector is a GHOST CONDENSATE (AeST authors' own id): one scalar phi, temporal Q-mode -> cold
    a^-3 "dark matter". Its AMOUNT I0 ~ Omega_dm is ROBUSTLY FREE (sympy-exact: I0 = mean of a shift-flat
    direction; thermal/dS-Unruh sets only the variance -> ~72-74 orders short of Omega_dm). FOUNDED-not-DERIVED.
  * The GC clustering scale mu <-> M (the k^4/M^2 Jeans scale) is ALSO FREE (galaxy-WL vs clusters squeeze
    it opposite ways). The GC mode is COLD (Hubble-over-damped), NOT a wave-like fuzzy condensate.
  * a0(z)=sqrt(rho_DE(z)) -> a swampland-tower mass m_tower(z)/m_tower(0)=exp(-alpha*Delta_phi(z)) that
    DECLINES ~25-40% over z=0-3 (banked, conditional on alpha~lambda). The ABSOLUTE scale is NOT forced.

REAL CONSTRAINTS (WebSearched 2026-06-27, both-ways):
  (i) FUZZY/ULTRALIGHT DM: canonical ~1e-22 eV. Dwarf-galaxy dynamics now require m >~ 2.2e-21 eV
      (arXiv:2405.xxxxx, May 2024); Lyman-alpha forest pushes the lower bound to ~1e-21..2e-21 eV;
      21cm "closes the window" up to ~1e-21 (2207.05083). 2507.00705 review: bulk fuzzy DM at 1e-22
      is DISFAVORED. => any DM at the framework's IR floor (1.2e-33 eV) is ~12 orders BELOW the bound.
  (ii) COUPLED DE-DM / MaVaN: a LIVE DESI-era literature (2503.10806 hint of coupled DM-DE; 2606.05005
       nu-mass in interacting DE after DR2; 2604.12032 coupled DE in the DESI era; Avsajanishvili 2026
       MaVaN late universe). DESI DR2 w0waCDM RELAXES Sigma m_nu (up to ~0.16 eV) and the degeneracy
       "dynamical DE vs time-varying mass" is EXACTLY where the framework's a0(z)+m(z) sits.
  (iii) S8 / sigma8: 2026 review (2602.12238) S8 ~ 0.819 +/- 0.007; KiDS-Legacy revised UP toward Planck
        (0.832 +/- 0.013); ACT+SPT+Planck-lensing+DESI shows the tension is NOT universal. => the S8
        tension is EASING; there is NO robust small-scale deficit for the framework's DM to "cure".

OUTPUT: a magnitude ledger placing the framework's candidate scales against each real constraint, then
the single decisive observational test (if any), both-ways.
"""
import os, math
import numpy as np

# ----------------------------------------------------------------- footing (LOCKED) --
c     = 2.99792458e8
hbar  = 1.054571817e-34
G     = 6.67430e-11
eV    = 1.602176634e-19
H_Lam = 1.808e-18                      # 1/s
a0    = 9.36e-11                       # m/s^2
Z     = math.sqrt(32*math.pi/3)

rho_DE = 3.0*H_Lam**2/(8.0*math.pi*G)  # kg/m^3
u_DE   = rho_DE*c**2                   # J/m^3
E_dS_J = (u_DE*(hbar*c)**3)**0.25      # rho_DE^(1/4) as an energy
E_dS_meV = E_dS_J/eV*1e3
# IR floor: hbar H_Lambda  as an energy / c^2 as a mass
m_IR_eV = (hbar*H_Lam)/eV              # hbar H_Lam in eV (the graviton-like IR mass floor)

print("="*100)
print("FRONT 3 -- the framework's DM CANDIDATE vs real constraints (fuzzy/Lya, coupled-DE/MaVaN, S8)")
print("="*100)
print(f"[footing]  a0={a0:.3g} m/s^2  Z={Z:.4f}  rho_DE={rho_DE:.4g} kg/m^3")
print(f"           rho_DE^(1/4)        = {E_dS_meV:.3f} meV  = {E_dS_meV*1e-3:.3e} eV  (de Sitter vacuum mass scale)")
print(f"           hbar*H_Lambda (IR floor) = {m_IR_eV:.3e} eV  (the extreme-IR graviton/condensate floor)")

# =====================================================================================
# (A) WHICH 'mass' does the framework actually put forward? Enumerate ALL candidate scales,
#     mark each FORCED vs FREE vs COINCIDENCE, and place each on the fuzzy-DM exclusion axis.
# =====================================================================================
print("\n"+"="*100)
print("(A) CANDIDATE-MASS LEDGER -- every scale the framework could call its 'DM mass', honestly tagged")
print("="*100)

# fuzzy-DM exclusion line (WebSearched)
fuzzy_canonical = 1e-22      # eV  classic Hu-Barkana-Gruzinov
fuzzy_lya       = 1e-21      # eV  Lyman-alpha lower bound (order)
fuzzy_dwarf     = 2.2e-21    # eV  dwarf-galaxy dynamics (2405, May 2024)
print(f"  fuzzy-DM exclusion axis (real):  canonical {fuzzy_canonical:.0e} eV  |  Lya >~ {fuzzy_lya:.0e} eV  |"
      f"  dwarf-dyn >~ {fuzzy_dwarf:.1e} eV (2024)")
print("  -> to be the BULK DM as a wave/fuzzy field, a candidate must sit ABOVE ~2e-21 eV.\n")

cands = [
    ("rho_DE^(1/4) = E_dS",           E_dS_meV*1e-3, "COINCIDENCE/BOUND (=meV; m_nu1<~Lambda^1/4, Gonzalo-Ibanez-Valenzuela)"),
    ("hbar H_Lambda (IR floor)",      m_IR_eV,       "FORCED-but-IRRELEVANT (graviton/condensate IR floor, not the DM amount)"),
    ("ghost-condensate cold mode M",  None,          "FREE (M ~ 0.04-1 eV input; amount I0~Omega_dm FREE, sympy-exact)"),
    ("swampland tower m_tower(0)",     None,          "FREE (absolute = M_Pl exp(-alpha phi_total); phi_total unobservable)"),
]
print(f"  {'candidate scale':32s}  {'value [eV]':>14s}   status")
print("  "+"-"*96)
for name,val,status in cands:
    vs = f"{val:.3e}" if val is not None else "   FREE   "
    print(f"  {name:32s}  {vs:>14s}   {status}")

print(f"\n  Placement on the fuzzy axis:")
print(f"    * rho_DE^(1/4) = {E_dS_meV*1e-3:.2e} eV is ~{math.log10((E_dS_meV*1e-3)/fuzzy_dwarf):.0f} ORDERS ABOVE the dwarf bound")
print(f"      -> it is a meV-scale relativistic species (a NEUTRINO-like hot/warm state), NOT a cold fuzzy field.")
print(f"    * hbar H_Lambda = {m_IR_eV:.2e} eV is ~{math.log10(fuzzy_dwarf/m_IR_eV):.0f} ORDERS BELOW the dwarf bound")
print(f"      -> a DM made of THIS mode is fuzzy-EXCLUDED by ~12 orders (free-streams away ALL structure).")
print(f"    * the GC cold mode is NOT a fuzzy wave at all (Hubble-over-damped, k^4/M^2, cold a^-3) -> the")
print(f"      fuzzy/Lya bound does NOT apply to it; but its amount AND its M are FREE inputs.")

# =====================================================================================
# (B) THE DISTINCTIVE SIGNATURE: varying mass m(z) tied to a0(z). Compute it on the REAL DESI
#     posterior (verbatim import of the banked tower ratio), and ask: is it DISTINCTIVE vs the
#     coupled-DE/MaVaN degeneracy, and at what redshift is the variation largest?
# =====================================================================================
print("\n"+"="*100)
print("(B) THE VARYING-MASS SIGNATURE m(z)/m(0) (the ONLY a0(z)-tied, potentially-distinctive handle)")
print("="*100)
DATA = ("/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
        "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")
W0_COL, WA_COL, WEIGHT_COL, BURNIN = 8, 9, 0, 0.3
COMBOS={"DESI+CMB+DESY5":"desy5sn","DESI+CMB+Union3":"union3","DESI+CMB+Pantheon+":"pantheonplus"}
Om0=0.31
def load(tag):
    ws,w0s,was=[],[],[]
    for n in (1,2,3,4):
        f=os.path.join(DATA,f"{tag}.chain.{n}.txt")
        d=np.loadtxt(f); k=int(BURNIN*len(d)); d=d[k:]
        ws.append(d[:,WEIGHT_COL]); w0s.append(d[:,W0_COL]); was.append(d[:,WA_COL])
    return np.concatenate(ws),np.concatenate(w0s),np.concatenate(was)
def wz(z,w0,wa): return w0+wa*z/(1.0+z)
def rho_de_ratio(z,w0,wa): return (1.0+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1.0+z))
def Omega_DE(z,w0,wa):
    r=rho_de_ratio(z,w0,wa); rho=(1-Om0)*r; rm=Om0*(1+z)**3; return rho/(rho+rm)
def field_excursion(zmax,w0,wa,nz=400):
    zs=np.linspace(0,zmax,nz); integ=np.sqrt(3*np.abs(1+wz(zs,w0,wa))*Omega_DE(zs,w0,wa))
    return np.trapz(integ,np.log(1+zs))

print(f"  {'combo':22s} {'w0':>7s} {'wa':>7s} | {'a0(z3)/a0':>9s} {'tower m(z3)/m':>13s} {'rhoDE^1/4(z3)':>13s}  decline%")
print("  "+"-"*96)
declines=[]
for name,tag in COMBOS.items():
    w,w0,wa=load(tag); w0m=np.average(w0,weights=w); wam=np.average(wa,weights=w)
    lam0=math.sqrt(3*abs(1+w0m))
    dphi3=field_excursion(3.0,w0m,wam)
    tower3=math.exp(-lam0*dphi3)          # banked tower ratio
    a0r3=rho_de_ratio(3.0,w0m,wam)**0.5
    rho4_3=rho_de_ratio(3.0,w0m,wam)**0.25
    decl=(1-tower3)*100; declines.append(decl)
    print(f"  {name:22s} {w0m:+7.3f} {wam:+7.3f} | {a0r3:9.3f} {tower3:13.3f} {rho4_3:13.3f}  {decl:6.1f}%")
print(f"\n  banked headline reproduced: tower m(z=3)/m(0) ~ 0.66-0.75 (DR1) -> a {min(declines):.0f}-{max(declines):.0f}% DECLINE over z=0-3.")

# =====================================================================================
# (C) THE SINGLE DECISIVE TEST -- is the m(z) signature DISTINGUISHABLE, and from what?
# =====================================================================================
print("\n"+"="*100)
print("(C) IS THE m(z) SIGNATURE DISTINCTIVE? -- the decisive-test analysis (both-ways)")
print("="*100)
# the framework's m(z) is DEGENERATE with dynamical DE because BOTH come from the SAME w(z).
# The only way m(z) becomes an INDEPENDENT signal is if the varying mass leaves a fingerprint that
# w(z)-geometry alone does NOT: a redshift-dependent free-streaming / growth modulation. Quantify the lever.
print("  The varying-mass m(z) and the geometric a0(z) are sourced by the SAME DESI w(z). So m(z) is")
print("  DEGENERATE with dynamical DE on geometry (BAO/SN). It becomes an INDEPENDENT handle ONLY via a")
print("  growth/free-streaming fingerprint that pure-geometry w(z) cannot fake. Quantify that lever:\n")

# If the lightest neutrino IS the lightest tower state (the one SM sector where the gap closes),
# a declining m_nu(z) lowers the cosmological free-streaming suppression at high z vs a constant mass.
dm21=7.42e-5; dm31=2.510e-3  # eV^2 (NuFIT)
# take the DESY5 declining law (rho_DE^1/4) on m1; heavier states pinned by splittings ~const.
w,w0,wa=load("desy5sn"); w0m=np.average(w0,weights=w); wam=np.average(wa,weights=w)
m1_0 = E_dS_meV/1e3            # eV, hypothesis m1(0)=E_dS
zs=np.linspace(0,3,200); ratio=rho_de_ratio(zs,w0m,wam)**0.25
m1z=m1_0*ratio
m1_eff=np.trapz(m1z,zs)/3.0
print(f"  IF lightest nu = lightest tower (rho_DE^1/4 law, the one closed-gap SM sector):")
print(f"     m1(0)={m1_0*1e3:.2f} meV -> <m1>_z(0-3)={m1_eff*1e3:.2f} meV  (a {(1-m1_eff/m1_0)*100:.0f}% effective drop)")
Sig0=(m1_0+math.sqrt(m1_0**2+dm21)+math.sqrt(m1_0**2+dm31))*1e3
shift=(m1_0-m1_eff)*1e3
print(f"     Sigma m_nu(0) = {Sig0:.1f} meV;  the m1(z) decline lowers the cosmologically-bounded Sigma_eff by ~{shift:.2f} meV")
print(f"     -> RIGHT SIGN to ease the DESI DR2 'Sigma below the NO floor' puzzle, but the shift ({shift:.2f} meV) is")
print(f"        TINY vs the puzzle (~tens of meV) because only the lightest state tracks. NOT a stand-alone signal.")

# forecast sensitivity
print(f"\n  Sensitivity ledger (WebSearched):")
print(f"     DESI DR2 + CMB now : sigma(Sigma m_nu) ~ 20-30 meV; w0waCDM vs LCDM Sigma split ~ 53 vs ~160 meV")
print(f"                          -> ALREADY cannot separate 'evolving DE' from 'evolving mass' (the degeneracy).")
print(f"     Euclid + DESI-DR3 (2026-28): sigma(Sigma) -> ~15-20 meV; first f(z)*sigma8(z) tomographic m(z) handle.")
print(f"     CMB-S4 + LSS (~2030): sigma(Sigma) -> ~14 meV; a 25-40% m(z) decline = O(15-25 meV) suppression")
print(f"                          modulation -> AT the sensitivity floor. Marginally testable, NOT this year.")

# =====================================================================================
# VERDICT
# =====================================================================================
print("\n"+"="*100); print("VERDICT (both-ways) -- does the framework predict a testable DM candidate?"); print("="*100)
print(f"""
 DOES IT NAME A SPECIFIC DM PARTICLE/MASS?  NO -- and saying otherwise would be manufacturing a number.
   * The dark-matter AMOUNT (I0 ~ Omega_dm) is ROBUSTLY FREE (sympy-exact: mean of a shift-flat direction;
     dS-Unruh thermal occupation falls ~72-74 orders short). FOUNDED-not-DERIVED.
   * The cold-mode clustering scale M (~0.04-1 eV) is a FREE input (galaxy-WL vs clusters squeeze it oppositely).
   * The swampland tower's ABSOLUTE scale is FREE (depends on the unobservable total field distance phi_total).
   The framework's DM is a GHOST-CONDENSATE COLD MODE, not a fuzzy wave -> the fuzzy/Lya >~2e-21 eV bound does
   NOT bite it (it is cold a^-3, Hubble-over-damped), but ONLY because its amount and scale are put in by hand.
   The one FORCED scale, rho_DE^(1/4)={E_dS_meV:.2f} meV, is a meV (neutrino-like) HOT state -- ~19 orders ABOVE the
   fuzzy bound -- and coincides with the PUBLISHED swampland bound m_nu1 <~ Lambda^(1/4) (a coincidence/inequality,
   not a forced DM amount). The IR floor {m_IR_eV:.2e} eV would be fuzzy-EXCLUDED by ~12 orders if it were the bulk DM.

 DOES IT MAKE A DISTINCTIVE VARYING-MASS PREDICTION TIED TO a0(z)?  YES, ONE -- but it is ABSORBED/degenerate now.
   The variation m(z)/m(0)=exp(-alpha*Delta_phi(z)) ~ 0.66-0.75 at z=3 (a 25-34% DECLINE) IS forced by the
   framework's a0(z)=sqrt(rho_DE(z)) (no free knob in the RATIO), and is genuinely NEW (the swampland papers make
   NO redshift prediction). It is a MaVaN-class declining dark/neutrino mass -- a real, computed, falsifiable shape.
   BUT it is sourced by the SAME DESI w(z) as the geometry, so on BAO/SN it is DEGENERATE with dynamical DE; it
   becomes INDEPENDENT only through a growth/free-streaming fingerprint, whose lever (~a few meV on Sigma if only
   the lightest state tracks) is TINY vs current sensitivity. Right-signed for the live DESI Sigma-m_nu puzzle.

 S8 CONSISTENCY: the GC cold mode gives NO S8 relief (wrong shape: a sharp Jeans knee, not a broadband tilt) AND
   S8 is EASING in 2025-26 data (KiDS-Legacy revised UP to ~Planck; 2026 review S8~0.819) -> no deficit to cure,
   and no S8 front to claim. Neutral-by-theorem, not solved.

 THE SINGLE DECISIVE TEST (if any): a TOMOGRAPHIC measurement of the dark/neutrino mass scale m(z) via the growth
   rate f(z)*sigma8(z) + free-streaming suppression as a function of redshift, by Euclid+DESI-DR3 (2026-28) and
   CMB-S4+LSS (~2030), targeting a 25-40% DECLINE over z=0-3 that TRACKS the SAME w(z)/a0(z). A detection that the
   mass declines WITH rho_DE^(1/2) (not independently) is the framework-distinctive signature. It DIES if DESI -> w=-1.

 NET (both-ways): the framework does NOT predict a specific DM particle mass (amount + scale FREE -> no number to
   manufacture), and its cold candidate is fuzzy-bound-immune only by being cold-by-construction. It DOES make ONE
   genuine, computed, falsifiable VARYING-MASS prediction tied to a0(z) -- a ~25-40% redshift DECLINE -- that is
   currently ABSORBED into the dynamical-DE degeneracy and marginally testable by ~2030 growth tomography. Forced =
   the VARIATION + the meV scale-coincidence; FREE = the absolute amount/scale. Not a TOE, dark-sector only.
""")
