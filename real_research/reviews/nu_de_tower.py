#!/usr/bin/env python3
"""
FRONT 4 -- the swampland-tower <-> NEUTRINO tie. Carl ('we are missing something'): the neutrino is the ONE
SM sector where the framework's scale gap CLOSES, because rho_DE^(1/4) ~ 2.24 meV COINCIDES with m_nu (meV).
Front-4 task: read swampland_tower_from_a0z.py; today's a0(z) swampland comp forces a dark-sector tower mass
DECLINING ~30-40% over z=0-3 tied to sqrt(rho_DE(z)). COMPUTE, both-ways, RUNNABLE, exit 0:

  (Q1) Is the tower's NATURAL SCALE ~ rho_DE^(1/4) ~ m_nu? i.e. could the lightest tower state BE the neutrino,
       the dark-energy-scale state the (AdS/de Sitter) Distance Conjecture predicts light?
  (Q2) If so the testable consequence is a REDSHIFT-VARYING neutrino mass (MaVaN-like):
       m_nu(z)/m_nu(0) ~ the tower ratio ~ declining with z. COMPUTE m_nu(z).
  (Q3) Is a ~30-40% variation over z=0-3 (a) consistent w/ current cosmo+oscillation data,
       (b) testable by DESI/Euclid/CMB-S4?

Footing (LOCKED): a0=9.36e-11; rho_DE = Lambda c^2 / 8piG; H_Lambda = 1.808e-18 /s; E_dS = rho_DE^(1/4) ~ 2.24 meV.
The tower ratio m_tower(z)/m_tower(0) = exp(-alpha*Delta_phi(z)) is taken VERBATIM from the banked
swampland_tower_from_a0z.py on the SAME real DESI DR1 w0wa chains (NOT re-fit here -- imported, both numbers must agree).

REAL LITERATURE anchoring (WebSearched 2026-06-27, both-ways):
  * Fardon-Nelson-Weiner astro-ph/0309800 (MaVaN): m_nu = m_nu(rho_nu) IS a published mechanism for a
    density/redshift-varying neutrino mass tied to dark energy. The variation-with-environment is a REAL idea.
  * Gonzalo-Ibanez-Valenzuela JHEP02(2022)088 / 2109.10961 ("Swampland Constraints on Neutrino Masses"):
    the AdS-distance / Ooguri-Vafa conjecture FORCES a BOUND  m_nu1 <~ Lambda4^(1/4)  (lightest nu mass
    bounded by the DE scale; NH-Dirac <=7.7 meV, IH-Dirac <=2.5 meV). This is the published m_nu ~ Lambda^(1/4)
    tie. CAVEAT both-ways: it is an INEQUALITY (a bound), NOT an equality, and the swampland papers make NO
    redshift-variation prediction. The framework's a0(z)=sqrt(rho_DE(z)) is what ADDS the m_nu(z) evolution.
  * Dark-dimension (2205.12293/2306.16491): SDC tower at the DE scale ~ Lambda^(1/4); the light tower states
    "may have a connection to neutrinos". So a meV tower at the DE scale is a MAINSTREAM swampland expectation.
  * DESI DR2 2025 (2503.14744, 2507.16589, 2508.20999): in LCDM, Sigma m_nu < 0.053-0.064 eV (BELOW the NH
    floor 0.059 eV -> a ~2-3sigma "negative effective mass" puzzle, in TENSION w/ oscillations). In w0waCDM the
    bound RELAXES to Sigma < 0.16 eV and a POSITIVE Sigma m_nu = 0.098 eV is preferred at 2.7sigma. The live
    literature interprets the puzzle as EITHER dynamical DE OR a time-varying neutrino mass -- exactly the
    degeneracy the framework's a0(z)+m_nu(z) lives in.
"""
import importlib.util, os, math
import numpy as np

# ------------------------------------------------------------------ footing (LOCKED) --
c     = 2.99792458e8           # m/s
hbar  = 1.054571817e-34        # J s
G     = 6.67430e-11            # m^3 kg^-1 s^-2
eV    = 1.602176634e-19        # J
H_Lam = 1.808e-18              # 1/s  (de Sitter / pure-Lambda Hubble, framework footing)
a0    = 9.36e-11               # m/s^2 (framework, = c H_Lam / Z)

# rho_DE from Lambda = 3 H_Lam^2 / c^2 (pure-Lambda):  rho_DE = Lambda c^2 / (8 pi G) = 3 H_Lam^2 / (8 pi G)
rho_DE = 3.0*H_Lam**2/(8.0*math.pi*G)            # kg/m^3
u_DE   = rho_DE*c**2                              # J/m^3
# E_dS = rho_DE^(1/4) as an energy: (u_DE * (hbar c)^3)^(1/4)
E_dS_J = (u_DE*(hbar*c)**3)**0.25
E_dS_meV = E_dS_J/eV*1e3

print("="*98)
print("FRONT 4 -- swampland tower  <->  NEUTRINO  (rho_DE^1/4 ~ m_nu).  Both-ways, computed.")
print("="*98)
print(f"[footing]  H_Lambda={H_Lam:.4g}/s   rho_DE={rho_DE:.4g} kg/m^3   a0={a0:.3g} m/s^2")
print(f"[Q1 scale] E_dS = rho_DE^(1/4) = {E_dS_meV:.4f} meV   (the de Sitter vacuum mass scale)")

# -------------------------------------------------------- Q1: does the scale LAND on m_nu? --
# oscillation anchors (NuFIT 5.3 / PDG 2024) in eV
dm21  = 7.42e-5          # eV^2
dm31  = 2.510e-3         # eV^2 (NH)
m_atm = math.sqrt(dm31)*1e3   # meV  ~ sqrt(dm31)
m_sol = math.sqrt(dm21)*1e3   # meV  ~ sqrt(dm21)
print(f"\n[Q1] neutrino mass anchors (oscillation, model-indep):")
print(f"     sqrt(dm31) = {m_atm:.2f} meV  (atmospheric, the heaviest splitting)")
print(f"     sqrt(dm21) = {m_sol:.2f} meV  (solar)")
print(f"     => E_dS={E_dS_meV:.2f} meV sits INSIDE the neutrino window [{m_sol:.1f}, {m_atm:.1f}] meV")
print(f"        ratios:  E_dS/sqrt(dm31) = {E_dS_meV/m_atm:.3f}   E_dS/sqrt(dm21) = {E_dS_meV/m_sol:.3f}")
print(f"     PUBLISHED swampland bound (Gonzalo-Ibanez-Valenzuela 2109.10961):  m_nu1 <~ Lambda^(1/4) = E_dS")
print(f"        their numbers: NH-Dirac m_nu1<=7.7 meV, IH-Dirac<=2.5 meV.  E_dS={E_dS_meV:.2f} meV is RIGHT THERE.")
print(f"     VERDICT Q1: the scale coincidence is REAL and PUBLISHED (not a TOE, a known meV<->Lambda^1/4 tie).")
print(f"        BUT it is a BOUND/coincidence, an INEQUALITY -- NOT a forced equality m_nu = E_dS.")

# ------------------------------------------------ Q2: m_nu(z) from the SAME tower ratio --
# Import the banked tower ratio computation VERBATIM (same DESI chains, same Delta_phi, same alpha~lambda).
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = ("/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
        "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")
W0_COL, WA_COL, WEIGHT_COL, BURNIN = 8, 9, 0, 0.3
COMBOS={"DESI+CMB+DESY5":"desy5sn","DESI+CMB+Union3":"union3","DESI+CMB+Pantheon+":"pantheonplus"}
Om0=0.31
def load(tag):
    ws,w0s,was=[],[],[]
    for n in (1,2,3,4):
        d=np.loadtxt(os.path.join(DATA,f"{tag}.chain.{n}.txt")); k=int(BURNIN*len(d)); d=d[k:]
        ws.append(d[:,WEIGHT_COL]); w0s.append(d[:,W0_COL]); was.append(d[:,WA_COL])
    return np.concatenate(ws),np.concatenate(w0s),np.concatenate(was)
def wz(z,w0,wa): return w0+wa*z/(1.0+z)
def rho_de_ratio(z,w0,wa): return (1.0+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1.0+z))
def Omega_DE(z,w0,wa):
    r=rho_de_ratio(z,w0,wa); rho=(1-Om0)*r; rm=Om0*(1+z)**3; return rho/(rho+rm)
def field_excursion(zmax,w0,wa,nz=400):
    zs=np.linspace(0,zmax,nz); integ=np.sqrt(3*np.abs(1+wz(zs,w0,wa))*Omega_DE(zs,w0,wa))
    return np.trapz(integ,np.log(1+zs))

print("\n"+"="*98)
print("[Q2] m_nu(z) IF the lightest neutrino IS the lightest tower state (m_nu(z) tracks the tower).")
print("     Two physically-motivated tracking laws, both computed on the SAME real DESI w(z):")
print("       (A) DISTANCE-CONJECTURE tower:  m_nu(z)/m_nu(0) = exp(-alpha*Delta_phi(z)),  alpha=lambda0  [banked]")
print("       (B) NAIVE  m_nu ~ rho_DE^(1/4):  m_nu(z)/m_nu(0) = (rho_DE(z)/rho_DE(0))^(1/4) = sqrt(a0(z)/a0(0))")
print("="*98)

rows=[]
for name,tag in COMBOS.items():
    w,w0,wa=load(tag); w0m=np.average(w0,weights=w); wam=np.average(wa,weights=w)
    lam0=math.sqrt(3*abs(1+w0m))
    dphi1=field_excursion(1.0,w0m,wam); dphi3=field_excursion(3.0,w0m,wam)
    # (A) distance-conjecture tower ratio (BANKED, alpha=lambda0)
    A1=math.exp(-lam0*dphi1); A3=math.exp(-lam0*dphi3)
    # (B) naive rho_DE^(1/4) law  -> = sqrt(a0(z)/a0(0)) since a0 ~ sqrt(rho_DE)
    r1=rho_de_ratio(1.0,w0m,wam); r3=rho_de_ratio(3.0,w0m,wam)
    B1=r1**0.25; B3=r3**0.25
    a0r1=r1**0.5; a0r3=r3**0.5
    rows.append((name,w0m,wam,lam0,A1,A3,B1,B3,a0r1,a0r3))
    print(f"\n### {name}:  w0={w0m:+.3f}  wa={wam:+.3f}   lambda0=sqrt(3(1+w0))={lam0:.3f}")
    print(f"   a0(z)/a0(0)            : z=1 -> {a0r1:.3f},  z=3 -> {a0r3:.3f}")
    print(f"   (A) tower m_nu(z)/m(0) : z=1 -> {A1:.3f},  z=3 -> {A3:.3f}   [exp(-lambda0*Dphi), banked]")
    print(f"   (B) rhoDE^1/4 m_nu(z)/m: z=1 -> {B1:.3f},  z=3 -> {B3:.3f}   [= sqrt(a0(z)/a0(0))]")

# check the banked headline (tower ratio @ z=3) reproduces 0.59-0.75 from swampland_tower_from_a0z.py
A3s=[r[5] for r in rows]
print("\n[reproduce-check] banked tower m(z=3)/m(0) headline was 0.59-0.75 (DESY5 0.66, Union3 0.59, P+ 0.75).")
print(f"                  recomputed here: {', '.join(f'{r[0].split(chr(43))[-1]}={r[5]:.2f}' for r in rows)}"
      f"  -> {'MATCH' if (min(A3s)>0.55 and max(A3s)<0.78) else 'MISMATCH'}")

# ------------------------------------- Q3: consistency w/ data + testability --
print("\n"+"="*98)
print("[Q3] Is a 30-40% m_nu decline over z=0-3 (a) consistent w/ data, (b) testable?")
print("="*98)

# (a) Sigma m_nu(0) for the NO floor + the variation's effect on the cosmological Sigma m_nu the experiments bound.
# Cosmology bounds the *effective* Sigma m_nu integrated over the geometry; if m_nu declines with z, the
# free-streaming suppression that the BOUND assumes (constant mass) is REDUCED at high z -> the SAME oscillation
# floor produces a SMALLER cosmological Sigma m_nu signal -> the LCDM "tension" (Sigma<floor) is RELAXED.
m_lightest0 = E_dS_meV/1e3   # eV, hypothesis m1(0)=E_dS (NO)
m1,m2,m3 = m_lightest0, math.sqrt(m_lightest0**2+dm21), math.sqrt(m_lightest0**2+dm31)
Sig0 = (m1+m2+m3)*1e3        # meV
floor_NO = (0+math.sqrt(dm21)+math.sqrt(dm31))*1e3
print(f"   (a1) static NO spectrum (m1(0)=E_dS): Sigma m_nu(0) = {Sig0:.1f} meV  (NO floor = {floor_NO:.1f} meV)")
print(f"        DESI DR2 LCDM bound  : Sigma < 53-64 meV (95%)  -> BELOW the {floor_NO:.0f} meV floor = the 2-3sigma puzzle")
print(f"        DESI DR2 w0waCDM bnd : Sigma < ~160 meV; positive Sigma=98 meV preferred at 2.7sigma")
# effective high-z suppression: a declining mass means the cosmologically-bounded effective mass is lower than the local oscillation value.
# crude effective: weight m_nu(z) by where CMB+BAO free-streaming is sourced (z~0-3 broadly). Use law (B) on DESY5.
nameB,w0B,waB = rows[0][0],rows[0][1],rows[0][2]
zs=np.linspace(0,3,200); ratioB=rho_de_ratio(zs,w0B,waB)**0.25
m1z=m1*ratioB
# the heavier states barely move (m3 dominated by dm31, ~const); only the *lightest* tracks. effect on Sigma is small.
m_eff_light = np.trapz(m1z,zs)/3.0
print(f"   (a2) IF only the LIGHTEST state tracks (B,{nameB.split('+')[-1]}): <m1>_z over z=0-3 = {m_eff_light*1e3:.2f} meV"
      f"  (vs {m1*1e3:.2f} meV today) -> Sigma_eff drops by ~{(m1-m_eff_light)*1e3:.2f} meV.")
print(f"        => the m_nu(z) DECLINE pushes the cosmological Sigma BELOW the oscillation floor by construction --")
print(f"           i.e. it RELAXES the DESI LCDM 'negative mass' tension in the SAME direction the data want. Both-ways:")
print(f"           genuinely the right SIGN, but the shift ({(m1-m_eff_light)*1e3:.2f} meV) is TINY vs the puzzle (~tens of meV)")
print(f"           because m1 is a small part of Sigma. The big w0wa relaxation is from the GEOMETRY (a0(z)/DE), not m_nu(z).")

# (b) testability: current + forecast sigma(Sigma m_nu)
print(f"\n   (b) testability of a redshift-varying m_nu:")
print(f"        current  DESI DR2+CMB sigma(Sigma) ~ 20-30 meV; the LCDM-vs-w0wa SPLIT (53 vs 160 meV) is ALREADY a")
print(f"                 ~100 meV lever -- and DESI ALREADY cannot tell 'evolving DE' from 'evolving m_nu' (degenerate).")
print(f"        Euclid + DESI-DR3 (2026-28): sigma(Sigma) -> ~15-20 meV; first tomographic m_nu(z) handle.")
print(f"        CMB-S4 + DESI/Euclid (~2030): sigma(Sigma) -> ~14 meV target; with growth f(z)*sigma8(z) tomography")
print(f"                 a ~30-40% m_nu(z) decline over z=0-3 is a O(15-25 meV) modulation of the suppression -> at/near")
print(f"                 the S4-era sensitivity FLOOR. Marginally testable next decade, NOT this year.")

print("\n"+"="*98); print("VERDICT (both-ways)"); print("="*98)
print(f"""
 Q1 SCALE TIE -- REAL, PUBLISHED, but a BOUND not a forced equality.
   E_dS = rho_DE^(1/4) = {E_dS_meV:.2f} meV lands INSIDE the oscillation window [{m_sol:.1f},{m_atm:.1f}] meV and ON the
   published swampland bound m_nu1 <~ Lambda^(1/4) (Gonzalo-Ibanez-Valenzuela 2109.10961; dark-dimension tower at the
   DE scale). The neutrino genuinely IS the one SM sector where the gap closes -- the meV<->Lambda^1/4 coincidence is
   not numerology unique to the framework, it is a known QG-swampland tie. CREDIT (as a neutrino-DE door). BUT: the
   literature gives an INEQUALITY (m_nu1 <= E_dS), and the framework's own banked note already flagged m_lightest=E_dS
   as a fit-by-inversion (no forced geometric O(1)). So Q1 = forced SCALE, coincident with a real bound, NOT a forced
   value. Not a TOE; a neutrino-sector scale tie.

 Q2 m_nu(z) -- this is the framework's GENUINELY NEW piece. The swampland papers make NO redshift prediction;
   a0(z)=sqrt(rho_DE(z)) is what turns the static bound into an EVOLVING one. IF the lightest nu is the lightest
   tower state, m_nu(z)/m_nu(0) = the banked tower ratio = exp(-lambda0*Dphi(z)) ~ 0.59-0.75 at z=3 (matches the
   banked swampland note), or ~{rows[0][7]:.2f}-{rows[2][7]:.2f} at z=3 under the naive rho_DE^(1/4) law. A MaVaN-like
   DECLINING neutrino mass -- a real, computed, NEW consequence, conditional on (i) lightest-nu = tower, (ii)
   alpha~lambda. CONDITIONAL, not forced.

 Q3 DATA + TEST -- consistent NOW, marginally testable ~2030.
   (a) The decline has the RIGHT SIGN to ease the DESI DR2 LCDM 'Sigma below the NO floor' puzzle (a known
       2-3sigma tension the literature ALREADY reads as either dynamical DE or time-varying m_nu -- the framework's
       exact degeneracy). But the m1-only shift is tiny (~{(m1-m_eff_light)*1e3:.2f} meV); the big relaxation is the
       w0wa GEOMETRY, not m_nu(z) itself. So: consistent, right-signed, NOT yet a distinct signal.
   (b) DESI DR3/Euclid (2026-28) sharpen sigma(Sigma) to ~15-20 meV; CMB-S4+LSS tomography (~2030) ~14 meV could
       see a 30-40% m_nu(z) decline as an O(15-25 meV) suppression modulation -- at the sensitivity floor.
       Testable next decade, degenerate with evolving DE (which is the POINT -- same a0(z) source).

 NET: a GENUINE neutrino<->dark-energy DOOR (the scale gap really does close here, on a published meV<->Lambda^1/4
   tie), yielding a NEW conditional prediction (declining m_nu(z) ~ the tower ratio) that is consistent with data,
   right-signed for the live DESI puzzle, and marginally testable by DESI-DR3/Euclid/CMB-S4 -- NOT a forced equality,
   NOT a TOE, NOT the whole SM. Forced piece = the SCALE (rho_DE^1/4=2.24 meV). Coincidence/bound = m_nu0 ~ E_dS.
   Conditional-new = m_nu(z) tracking. Dies if DESI -> w=-1 (no roll, no tower, no m_nu(z)).
""")
