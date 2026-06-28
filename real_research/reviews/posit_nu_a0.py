#!/usr/bin/env python3
"""
posit_nu_a0.py  -- CLASS A: neutrino <-> a0 SHARED-ORIGIN posits, on the framework's OWN terms.

Framework premises (NOT a TOE -- Carl retracted the TOE; gravity result is a0=sqrt(Lambda) only):
  * inertia = response to the de Sitter-Unruh horizon bath.
  * a0 = c*H_Lambda / Z = c^2*sqrt(Lambda/32pi) = 9.36e-11 m/s^2, Z = sqrt(32pi/3).
  * the SAME rho_DE that sets a0 sets a meV vacuum-energy scale E_L = rho_DE^(1/4) = 2.2395 meV.
  * cosmic evolution: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0))  [FORCED -- only w0,wa enter].

This script TESTS the Class-A posits both-ways, FDR-guarding every numeric coincidence, and
propagates the co-evolution through the REAL public DESI DR1 w0waCDM MCMC chains when present
(else analytic CPL central values). Each posit is graded:
  FORCED-CONSEQUENCE / HYPOTHESIS-WITH-FREE-KNOB / SPECULATIVE.

Exit 0. Both-ways honest. No git push.
"""
import os, math
import numpy as np

# ----------------------------- footing (LOCKED) -----------------------------
c     = 2.99792458e8        # m/s
G     = 6.67430e-11         # SI
hbar  = 1.054571817e-34     # J s
eV    = 1.602176634e-19     # J
H0    = 67.36e3/3.0856775814913673e22   # s^-1 (Planck-ish)
Om0   = 0.3153
ODE0  = 1.0 - Om0
Lambda= 1.0891e-52          # m^-2 (banked, H0=67.36, OmL=0.6847)
rho_DE= 5.8355e-27          # kg/m^3 (banked)
Z     = math.sqrt(32*math.pi/3)

# de Sitter horizon Hubble (pure-Lambda): H_L = c*sqrt(Lambda/3)
H_L   = c*math.sqrt(Lambda/3.0)
a0    = c*H_L/Z
E_L_J = (rho_DE*c**2 * (hbar*c)**3)**0.25      # J
E_L   = E_L_J/eV*1e3                            # meV

print("="*94)
print("CLASS A -- neutrino <-> a0 shared-origin posits (framework's own premises)")
print("="*94)
print(f"  a0 = c*H_L/Z               = {a0:.4e} m/s^2   (target 9.36e-11)")
print(f"  E_L = rho_DE^(1/4)         = {E_L:.4f} meV     (target 2.2395)")
print(f"  Z = sqrt(32 pi/3)          = {Z:.5f}")
print(f"  H_L = c*sqrt(Lambda/3)     = {H_L:.4e} /s")

# ----------------------------- CPL rho_DE(z) -----------------------------
def rho_de_ratio(z, w0, wa):
    z = np.asarray(z, float)
    return (1.0+z)**(3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*z/(1.0+z))

def wz(z, w0, wa):
    z = np.asarray(z, float)
    return w0 + wa*z/(1.0+z)

def Om_DE(z, w0, wa):
    de = ODE0*rho_de_ratio(z, w0, wa); m = Om0*(1.0+z)**3
    return de/(de+m)

def dphi(zmax, w0, wa, nz=4000):
    """quintessence field excursion Delta_phi (in M_Pl) = int sqrt(3|1+w| Om_DE) dln(1+z)."""
    zs = np.linspace(0.0, zmax, nz)
    integ = np.sqrt(3.0*np.abs(1.0+wz(zs, w0, wa))*Om_DE(zs, w0, wa))
    return np.trapz(integ, np.log(1.0+zs))

# ----------------------------- load real DESI DR1 chains if present -----------------------------
CH_DIR = os.environ.get("DESI_CHAINS_DIR",
    "/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
    "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")
W0_COL, WA_COL, WCOL = 8, 9, 0
BURNIN = 0.3
COMBOS = {"DESI+CMB+DESY5":"desy5sn", "DESI+CMB+Union3":"union3", "DESI+CMB+Pantheon+":"pantheonplus"}
# analytic fallback central values (DESI DR1, banked) if chains absent
FALLBACK = {"DESI+CMB+DESY5":(-0.726,-1.06), "DESI+CMB+Union3":(-0.642,-1.31),
            "DESI+CMB+Pantheon+":(-0.828,-0.74)}

def load_chain(tag):
    ws=[]; w0=[]; wa=[]
    for n in (1,2,3,4):
        p = os.path.join(CH_DIR, f"{tag}.chain.{n}.txt")
        if not (os.path.exists(p) and os.path.getsize(p)>0): return None
        d = np.loadtxt(p); k=int(BURNIN*len(d)); d=d[k:]
        ws.append(d[:,WCOL]); w0.append(d[:,W0_COL]); wa.append(d[:,WA_COL])
    return np.concatenate(ws), np.concatenate(w0), np.concatenate(wa)

def wq(x, w, q):
    i=np.argsort(x); x=x[i]; w=w[i]; cw=np.cumsum(w); cw/=cw[-1]
    return np.interp(q, cw, x)

chains = {name: load_chain(tag) for name,tag in COMBOS.items()}
HAVE = all(v is not None for v in chains.values())
print(f"\n  real DESI DR1 chains loaded: {HAVE}  (dir={CH_DIR})")

# ============================================================================
# POSIT A1 -- a0(z) and m_nu(z) CO-EVOLVE; is the RATIO a forced consequence?
# ============================================================================
print("\n"+"="*94)
print("POSIT A1 -- a0(z)/a0(0) vs m_nu(z)/m_nu(0): co-evolution of the two rho_DE-children")
print("="*94)
print("""
  FRAMEWORK CONTENT (forced):  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) = rho_DE(z)^(1/2)-tracker.
  The neutrino mass evolution m_nu(z) has TWO candidate laws -- they give DIFFERENT ratios:

    LAW (i)  MaVaN/swampland 'tracker':  m_nu(z) ∝ rho_DE(z)^p  (p free).
             => m_nu(z)/m_nu(0) = [a0(z)/a0(0)]^(2p).  The ratio m_nu/a0-scaling is forced ONLY
             if p is fixed.  p=1/2 is the SPECIAL value where m_nu and a0 share the EXACT same
             rho_DE^(1/2) scaling, i.e. m_nu(z)/m_nu(0) == a0(z)/a0(0) identically.
             p is NOT forced by the framework -> this is the FREE KNOB.

    LAW (ii) growing-nu (door3): m_nu(z)=m_nu(0)*exp(-alpha*Delta_phi[w(z)]), alpha~lambda0
             a swampland conjecture (free knob). Heavier today, freezes by z~10.

  TEST: compute BOTH ratios on the REAL DESI posterior; show whether 'p=1/2 ties m_nu to a0
  one-to-one' is a distinctive prediction or just one knob-setting among many (FDR view).
""")
ZTEST = [0.4, 1.0, 3.0]
print(f"  {'combo':20s} {'z':>4s}  a0(z)/a0(0)   m_nu/m0 (p=1/2)  m_nu/m0 (p=1)   m_nu/m0 (door3 growing-nu)")
A1ROWS=[]
for name in COMBOS:
    if HAVE:
        w,w0s,was = chains[name]
        w0 = wq(w0s,w,0.5); wa = wq(was,w,0.5)
    else:
        w0,wa = FALLBACK[name]
    lam0 = math.sqrt(3.0*abs(1.0+w0))
    for z in ZTEST:
        r_a0 = float(np.sqrt(rho_de_ratio(z,w0,wa)))       # = m_nu ratio for p=1/2 (LAW i)
        r_p1 = float(rho_de_ratio(z,w0,wa))                # p=1     (LAW i)
        r_gn = math.exp(-lam0*dphi(z,w0,wa))               # door3 growing-nu (LAW ii)
        A1ROWS.append((name,z,r_a0,r_p1,r_gn))
        print(f"  {name:20s} {z:4.1f}  {r_a0:11.4f}   {r_a0:13.4f}   {r_p1:11.4f}   {r_gn:.4f}  (lam0={lam0:.2f})")

print("""
  READ:
   * For p=1/2, m_nu(z)/m_nu(0) is IDENTICAL to a0(z)/a0(0) by construction (same column) --
     a TRUE one-to-one co-evolution, but ONLY because p was SET to 1/2; nothing forces p.
   * The door3 growing-nu law gives the OPPOSITE near-field SIGN at low z (m_nu heavier today,
     ratio<1 in past) AND a much larger excursion -- so the two 'shared-origin' readings are
     PHYSICALLY DISTINCT, not the same prediction. They cannot both be the framework's law.
   * Therefore A1's clean statement 'a0 and m_nu both go as rho_DE^(1/2)' is a HYPOTHESIS: it is
     forced ONLY under MaVaN-with-p=1/2, which is itself a free choice.
  GRADE A1 = HYPOTHESIS-WITH-FREE-KNOB (the knob is p, or equivalently alpha).
  The FORCED kernel underneath it -- a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)) -- stays forced and is
  the SAME w(z) that the m_nu(z) law would have to share. THAT shared-w(z) is the testable hook.
""")

# ============================================================================
# POSIT A2 -- IF m1=E_L, Sigma m_nu = 61.3 meV ; JUNO(2026)+DESI DR3 test
# ============================================================================
print("="*94)
print("POSIT A2 -- IF m_lightest = E_L (NOT forced): Sigma m_nu = 61.3 meV, a JUNO+DESI target")
print("="*94)
# NuFIT 5.3 / PDG 2024
dm21 = 7.42e-5   # eV^2
dm31 = 2.510e-3  # eV^2 (NO)
dm32_IO = 2.490e-3
sin2_12, sin2_13 = 0.303, 0.02203
Ue1sq = (1-sin2_13)*(1-sin2_12); Ue2sq=(1-sin2_13)*sin2_12; Ue3sq=sin2_13
m1 = E_L*1e-3   # eV (E_L in meV -> eV)
m2 = math.sqrt(m1**2 + dm21)
m3 = math.sqrt(m1**2 + dm31)
Sig = (m1+m2+m3)*1e3   # meV
Sig_floor = (0 + math.sqrt(dm21) + math.sqrt(dm31))*1e3
mbeta = math.sqrt(Ue1sq*m1**2+Ue2sq*m2**2+Ue3sq*m3**2)*1e3
# IO control
m3_IO=m1; m1_IO=math.sqrt(m3_IO**2+dm32_IO); m2_IO=math.sqrt(m1_IO**2+dm21)
Sig_IO=(m1_IO+m2_IO+m3_IO)*1e3
print(f"  m1=E_L={E_L:.4f} meV  m2={m2*1e3:.3f} meV  m3={m3*1e3:.3f} meV")
print(f"  Sigma m_nu (NO, m1=E_L) = {Sig:.2f} meV   (minimal-NO floor = {Sig_floor:.2f} meV; +{Sig-Sig_floor:.2f} meV above)")
print(f"  m_beta (KATRIN-type)    = {mbeta:.3f} meV")
print(f"  Sigma m_nu (IO control) = {Sig_IO:.2f} meV  -> ABOVE Planck+DESI ceiling ~72 meV (disfavored ordering)")
print(f"""
  TESTS (near-term, 2026-2028):
   * DESI DR3 + CMB Sigma m_nu 95% bound: if it drops BELOW the NO floor ~59 meV -> kills m1=E_L
     (and clashes with oscillations). Current ~<72 meV -> ~10 meV headroom; A2 lives but cornered.
   * JUNO (data 2026, ordering ~2027-2029): determines NO vs IO at ~3sigma. IO reading of A2
     (Sigma=101 meV) already in cosmic tension; a firm IO would kill the only viable (NO) version.
  GRADE A2 = HYPOTHESIS-WITH-FREE-KNOB: E_L is FORCED, but 'm1 = E_L' sets the O(1) coefficient
  to exactly 1 by inversion (no geometric factor). Falsifiable 2026-2028; FDR-flagged below.
""")

# FDR guard on A2: is ~2 meV special to rho_DE, or generic to any cosmic density^(1/4)?
print("  FDR GUARD (A2): meV scale from cosmic-density^(1/4) -- is rho_DE special?")
rho_crit = 3*H0**2*c**2/(8*math.pi*G)   # kg/m^3 (mass density)
for nm, rho in [("rho_DE", rho_DE), ("rho_crit", rho_crit), ("rho_m=Om0*rho_crit", Om0*rho_crit),
                ("10*rho_DE", 10*rho_DE), ("rho_DE/10", rho_DE/10)]:
    E = (rho*c**2*(hbar*c)**3)**0.25/eV*1e3
    print(f"     {nm:22s} -> E^(1/4) = {E:.3f} meV")
print("     => a factor 10 in density moves the meV scale only ~1.8x. '~2 meV ~ m_nu' is GENERIC")
print("        to any cosmic density. rho_DE is NOT uniquely picked by the meV match alone. (both-ways)")

# ============================================================================
# POSIT A3 -- the neutrino as lightest excitation of the dS bath (floor T0)
# ============================================================================
print("\n"+"="*94)
print("POSIT A3 -- neutrino as the lightest excitation tied to the de Sitter bath temperature floor")
print("="*94)
T_dS = H_L*hbar/(2*math.pi*1.380649e-23)   # Gibbons-Hawking dS temperature (K)
E_dS_thermal = (1.380649e-23*T_dS)/eV*1e3  # meV
print(f"  Gibbons-Hawking dS temperature   T_dS = {T_dS:.3e} K")
print(f"  thermal energy kT_dS             = {E_dS_thermal:.3e} meV")
print(f"  E_L = rho_DE^(1/4)               = {E_L:.4f} meV")
print(f"  ratio E_L / kT_dS                = {E_L/E_dS_thermal:.3e}")
print(f"""
  HONEST READ: the bath's THERMAL quantum kT_dS ~ {E_dS_thermal:.1e} meV is ~31 ORDERS too small to
  be a neutrino mass (this is the known dS-Unruh thermal-mass failure, M5 in nu_de_mechanism.py).
  So 'm_nu = the bath thermal floor' is FALSE by ~10^31. What IS true: E_L is the VACUUM-ENERGY
  (condensate) scale rho_DE^(1/4), NOT the thermal scale -- a meV CONDENSATE floor, not a thermal one.
  Calling the neutrino 'the lightest dS-bath excitation' only works if 'excitation' means the
  vacuum-energy-density scale (E_L), which restates rho_DE -> no particle, no mechanism (M0).
  GRADE A3 = SPECULATIVE: the thermal-floor reading is killed by 10^31; the vacuum-floor reading
  is just E_L relabelled. No forced bridge to a neutrino. Keep as imagery, not a test.
""")

# ============================================================================
# POSIT A4 (own) -- the LOCKED CMB-vs-late SPLIT as the JOINT a0(z)+m_nu(z) discriminator
# ============================================================================
print("="*94)
print("POSIT A4 (own) -- the SHARED w(z) lock: a0(z) and m_nu(z) must use the SAME rho_DE(z)")
print("="*94)
print("""
  CONTENT: a0(z)=sqrt(rho_DE(z)) is FORCED; IF m_nu also tracks rho_DE (A1, any law), then the
  SAME measured w(z) drives BOTH. That gives a falsifiable CONSISTENCY: the redshift where a0(z)
  peaks/declines and the redshift where m_nu(z) peaks/declines must COINCIDE (set by one w(z)).
  This is distinctive because generic MaVaN/quintessence rivals do NOT tie their m_nu evolution
  to the SAME rho_DE(z) that any gravity-side a0(z) test sees -- the framework does, by shared origin.
""")
# CMB-imprinted Sigma_eff under door3 growing-nu, today at NO floor -- the split size:
print(f"  {'combo':20s}  a0(z=3)/a0(0)   Sigma_eff(CMB)/Sigma(today)   Delta_Sigma split (today@59meV)")
for name in COMBOS:
    if HAVE:
        w,w0s,was=chains[name]; w0=wq(w0s,w,0.5); wa=wq(was,w,0.5)
    else:
        w0,wa=FALLBACK[name]
    lam0=math.sqrt(3.0*abs(1.0+w0))
    r_a0_z3=float(np.sqrt(rho_de_ratio(3.0,w0,wa)))
    r_cmb=math.exp(-lam0*dphi(1100.0,w0,wa))     # frozen-early m_nu ratio
    dSig=(1-r_cmb)*Sig_floor                      # meV
    print(f"  {name:20s}  {r_a0_z3:11.4f}   {r_cmb:24.4f}   {dSig:.1f} meV")
print("""
  TEST (2027-2030): joint fit imposing m_nu(z)=m_nu(0)*f(rho_DE[w(z)]) with w(z) SHARED between
  (a) the BAO/SN w0wa fit, (b) any a0(z) gravity probe (BTFR/cluster zero-point), (c) the CMB-vs-LSS
  Sigma m_nu split. One extra dof (the m_nu-rho_DE coupling). CMB-S4 sigma(Sigma)~16-32 meV makes the
  ~15-25 meV split a ~1-2sigma target. DIES gracefully if DESI DR3 -> w=-1 (split->0, no signal).
  GRADE A4 = FORCED-CONSEQUENCE *conditional on A1*: GIVEN that m_nu tracks rho_DE at all, the
  shared-w(z) coincidence is forced (not a new knob). Unconditionally it inherits A1's knob.
  Honest label: FORCED-CONSEQUENCE-IF-A1, i.e. a forced consistency test of the shared-origin claim.
""")

# ============================================================================
# SUMMARY
# ============================================================================
print("="*94)
print("SUMMARY -- Class A posit grades (both-ways, no manufacture)")
print("="*94)
print("""  A1  m_nu(z)/a0(z) co-evolution ratio        HYPOTHESIS-WITH-FREE-KNOB  (knob=p / alpha; forced kernel=a0(z))
  A2  m1=E_L => Sigma=61.3 meV                 HYPOTHESIS-WITH-FREE-KNOB  (E_L forced; '=m1' fit; JUNO+DESI 2026-28)
  A3  neutrino = lightest dS-bath excitation   SPECULATIVE                (thermal floor off by 10^31; vacuum floor = E_L relabel)
  A4  shared-w(z) lock / CMB-vs-late split     FORCED-CONSEQUENCE-IF-A1   (forced GIVEN A1; the genuine joint discriminator)

  BEST-IN-CLASS: A4 -- it is the only one whose distinctive content is a FORCED consistency
  (shared rho_DE(z) drives both children) rather than a free-knob coincidence, and it is the one
  near-term JOINT test (a0(z) gravity probe + m_nu(z) cosmology share ONE w(z)). A2 is the cleanest
  falsifiable NUMBER (61.3 meV, dead by ~2028 if Sigma drops below the NO floor).""")
print("\nposit_nu_a0: OK")
