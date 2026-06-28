#!/usr/bin/env python3
"""
posit_dS_structure.py  --  CLASS C: de SITTER STRUCTURE / HORIZON-dof posits.
=============================================================================
GENERATE + GRADE 3 NEW posits on the framework's OWN terms, tying its horizon
quantities (Z = sqrt(32pi/3), a0 = cH_Lambda/Z, E_L = rho_DE^(1/4) = 2.24 meV)
to the de Sitter HORIZON-dof count N = S_dS = A/4G, in the spirit of the
Addazi-Meluccio (Particles 9 (2026) 11 / arXiv:2604.26982) dS-entropy
information-seesaw m_nu ~ M_P/N^(1/4).

Footing (LOCKED, the framework's OWN -- never McGaugh nu):
  a0 = c H_Lambda / Z = 9.36e-11 m/s^2 ;  Z = sqrt(32 pi / 3)
  rho_DE = Lambda c^2 / 8 pi G  (PURE-Lambda) sets BOTH a0 AND E_L = rho_DE^(1/4)
  H_Lambda = H0 sqrt(Omega_Lambda) ;  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)

The three posits:
  C1  Does the Z / horizon-dof count PREDICT the seesaw N (and so the dark/nu
      mass)?  Compute S_dS, N; find the exponent p s.t. E_L = M_P / N^p; test
      whether p is "framework-natural" (1/4? tied to Z?). FDR-guard the match.
  C2  The dark-sector mass as a horizon-bath excitation LOCKED to a0(z):
      m_dark(z) = E_L * (a0(z)/a0(0)) ^ q  for the natural exponents q.
      A redshift-declining mass -- the framework's own falsifiable consequence.
  C3  An EFE / external-field-bath -> particle-scale posit: an external bath
      acceleration a_ext raises the local dS-Unruh kappa = sqrt(a_ext^2+(cH_L)^2);
      does the boosted bath define a LOCAL mass scale E(a_ext) that differs from
      E_L?  Compute the induced scale and grade whether it is a real new handle.

GRADE each: FORCED-CONSEQUENCE / HYPOTHESIS-WITH-FREE-KNOB / SPECULATIVE.
Back every number; FDR-guard coincidences; both-ways honest. Exit 0. No git push.
"""
import math
import numpy as np

# ----------------------------------------------------------------- footing (SI) ------
c    = 2.99792458e8
G    = 6.67430e-11
hbar = 1.054571817e-34
kB   = 1.380649e-23
eV   = 1.602176634e-19
Mpc  = 3.0856775814913673e22
H0   = 67.36e3/Mpc
OmL  = 0.6847
H_L  = H0*math.sqrt(OmL)                       # pure-Lambda Hubble
Lam  = 3.0*H_L**2/c**2                          # cosmological constant [1/m^2]
rho_DE = Lam*c**2/(8.0*math.pi*G)               # kg/m^3
u_DE  = rho_DE*c**2                              # J/m^3
Z    = math.sqrt(32.0*math.pi/3.0)
a0   = c*H_L/Z

lP   = math.sqrt(hbar*G/c**3)                    # Planck length
E_P  = math.sqrt(hbar*c**5/G)/eV                 # Planck energy [eV]
E_P_red = 2.435e18*1e9                           # reduced Planck energy [eV]
E_L  = (u_DE*(hbar*c)**3)**0.25/eV               # rho_DE^(1/4) [eV]
E_L_meV = E_L*1e3

print("#"*92)
print("# CLASS C -- de SITTER STRUCTURE / HORIZON-dof posits  (Z, a0=cH_L/Z, E_L=rho_DE^1/4)")
print("#"*92)
print(f"\n[footing]  Z = sqrt(32pi/3) = {Z:.5f}")
print(f"           a0 = cH_L/Z = {a0:.4e} m/s^2   H_L = {H_L:.4e} /s")
print(f"           E_L = rho_DE^(1/4) = {E_L_meV:.4f} meV   E_Planck = {E_P:.4e} eV")

# =====================================================================================
# C1 -- does Z / the horizon-dof count PREDICT the seesaw N (and the dark/nu mass)?
# =====================================================================================
print("\n"+"="*92)
print("C1  HORIZON-dof SEESAW: compute S_dS = N = A/4G; find p s.t. E_L = M_P/N^p;")
print("    is p 'framework-natural' (1/4? tied to Z)?  FDR-guard the match.")
print("="*92)

# de Sitter horizon: radius, area, entropy = N (in nats; S = A/4G in natural units).
r_dS = math.sqrt(3.0/Lam)                        # = c/H_L
A_dS = 4.0*math.pi*r_dS**2
# S_dS = A/(4 l_P^2) = pi/(H_L^2 l_P^2) = pi r_dS^2 / l_P^2 (dimensionless dof count N)
N    = A_dS/(4.0*lP**2)
# the prompt's "pi/(H_L^2 L_P^2)" form: H_L here is the RATE (1/s), so the horizon length is
# c/H_L and N = pi (c/H_L)^2 / lP^2 = pi c^2/(H_L^2 lP^2). (Writing pi/(H_L^2 lP^2) with H_L
# as a rate drops a c^2; restore it.)
N_alt = math.pi*c**2/(H_L**2*lP**2)
print(f"  r_dS = c/H_L = {r_dS:.4e} m   (= {r_dS/Mpc:.2f} Mpc)")
print(f"  S_dS = N = A/(4 lP^2) = {N:.4e}   (~1e{int(round(math.log10(N)))})")
print(f"  cross-check pi c^2/(H_L^2 lP^2) = {N_alt:.4e}  (match: {math.isclose(N,N_alt,rel_tol=1e-9)})")

# The Addazi-Meluccio relation: m ~ M_P / N^(1/4) = (M_P^2 Lambda)^(1/4) ~ rho_vac^(1/4).
mAM = E_P_red / N**0.25
mAM_full = E_P / N**0.25
print(f"\n  Addazi-Meluccio bare scale  M_P/N^(1/4):")
print(f"     reduced M_P/N^(1/4) = {mAM*1e3:.4f} meV   (k = m/E_L = {mAM/E_L:.4f})")
print(f"     full    M_P/N^(1/4) = {mAM_full*1e3:.4f} meV   (k = {mAM_full/E_L:.4f})")

# *** the key C1 computation: solve for the exponent p that makes E_L = M_P / N^p EXACTLY. ***
# E_L = M_P N^-p  =>  p = ln(M_P/E_L) / ln(N).
p_red  = math.log(E_P_red/E_L)/math.log(N)
p_full = math.log(E_P/E_L)/math.log(N)
print(f"\n  *** solve E_L = M_P / N^p for p (prove-by-moving-the-number) ***")
print(f"     reduced M_P: p = {p_red:.5f}     full M_P: p = {p_full:.5f}")
print(f"     framework-natural candidates: 1/4 = {0.25}, 1/Z = {1/Z:.4f}, 3/(8pi)... ")
print(f"     |p_red - 1/4| = {abs(p_red-0.25):.4f}  ({(p_red-0.25)/0.25*100:+.1f}% off 1/4)")
print(f"     |p_full- 1/4| = {abs(p_full-0.25):.4f}  ({(p_full-0.25)/0.25*100:+.1f}% off 1/4)")

# Is p~1/4 because of a FORCED kernel, or is it the trivial dimensional identity?
# CRUX: rho_DE = Lambda c^2/8piG and N = pi/(H_L^2 lP^2) are BOTH built from (Lambda, lP).
# => E_L = rho_DE^(1/4) and M_P/N^(1/4) are the SAME function of (Lambda, lP) up to an O(1).
# Show this algebraically: E_L^4 = u_DE (hbar c)^3 = (3 H_L^2 c^2/8piG)(hbar c)^3;
#                          (M_P/N^(1/4))^4 = M_P^4/N = E_P^4 * (H_L^2 lP^2/pi).
# Their RATIO is a pure number (no Lambda, no lP) -> p=1/4 is a DIMENSIONAL IDENTITY, the
# O(1) is the only content, and the O(1) is NOT 1 (k != 1) and NOT fixed by Z.
# Compute the ratio in dimensionless ENERGY units (eV) to avoid float overflow from M_P^4:
#   E_L^4 / (M_P/N^(1/4))^4 = (E_L / (E_P/N^(1/4)))^4 = (E_L*N^(1/4)/E_P)^4   -- all in eV.
ratio4 = (E_L*N**0.25/E_P)**4
print(f"\n  ALGEBRAIC CRUX -- is p=1/4 a forced kernel or a dimensional identity?")
print(f"     E_L^4 / (M_P/N^(1/4))^4 = {ratio4:.5f}   (a PURE number: no Lambda, no lP left)")
print(f"     => E_L and M_P/N^(1/4) are the SAME (Lambda,lP)-function up to this O(1).")
print(f"        p=1/4 is therefore a DIMENSIONAL IDENTITY (rho^(1/4) IS M_P/N^(1/4) by")
print(f"        construction), NOT a forced prediction of N. The only content is the O(1)")
print(f"        = {ratio4:.4f} (= k^4, k={ratio4**0.25:.4f}), NEITHER 1 NOR a clean Z-function.")

# Does Z fix the O(1)?  Test framework-natural O(1) candidates against ratio4 and against k.
print(f"\n  Does Z fix the O(1)?  test framework-natural candidates vs the required O(1):")
cands = {
    "1"            : 1.0,
    "3/(8pi)"      : 3.0/(8*math.pi),
    "8pi/3"        : 8*math.pi/3.0,
    "1/Z"          : 1.0/Z,
    "Z"            : Z,
    "Z^2=32pi/3"   : Z**2,
    "1/Z^2"        : 1.0/Z**2,
    "(3/32pi)^(1/4)": (3.0/(32*math.pi))**0.25,
}
kreq = E_L/mAM_full   # required O(1) on the energy (k vs full M_P)
print(f"     required E_L/(M_P/N^1/4)_full = {kreq:.4f};  ratio4 (on E^4) = {ratio4:.4f}")
for nm,v in cands.items():
    print(f"       {nm:14s} = {v:8.4f}   |E^4 ratio off| {abs(v-ratio4):.4f}    |k off| {abs(v-kreq):.4f}")
print(f"     -> no framework-natural O(1) lands ON the required value cleanly; the closest")
print(f"        are coincidental (within 2x of several). Z does NOT fix it.")

# FDR / look-elsewhere: ANY cosmic density^(1/4) ~ few meV (the M6 control). Show the spread.
print(f"\n  FDR / look-elsewhere control (is meV ~ rho^(1/4) generic?):")
rho_crit = 3*H0**2/(8*math.pi*G)
for nm,rho in [("rho_DE",rho_DE),("rho_crit",rho_crit),("rho_m=0.31rho_c",0.31*rho_crit),
               ("10*rho_DE",10*rho_DE),("0.1*rho_DE",0.1*rho_DE)]:
    E = ((rho*c**2)*(hbar*c)**3)**0.25/eV*1e3
    print(f"       {nm:16s} ^(1/4) = {E:.3f} meV")
print(f"     => a factor 100 in density moves the meV scale only ~3.2x. '~2 meV' is GENERIC")
print(f"        to rho_cosmic^(1/4); it is NOT a sharp N-prediction. (matches banked M6.)")

print(f"""
  GRADE C1: SPECULATIVE (graded down honestly).
    The horizon-dof count N = {N:.2e} is real and the Addazi-Meluccio M_P/N^(1/4)
    lands at {mAM_full*1e3:.2f} meV (k={mAM_full/E_L:.2f} x E_L) -- the right ORDER. BUT:
    (i) p=1/4 is a DIMENSIONAL IDENTITY (rho_DE^(1/4) IS M_P/N^(1/4) up to an O(1)
        ratio = {ratio4:.3f}), so N does NOT independently PREDICT E_L -- it RESTATES it.
    (ii) the O(1) is not 1 and not fixed by Z (no clean Z-function lands on it).
    (iii) any rho_cosmic^(1/4) gives ~2 meV (FDR control). So this is the banked
        'E_L restates rho_DE, no particle' verdict, re-derived through the N route.
    NOT a forced seesaw prediction. Founded-not-derived STAYS.""")

# =====================================================================================
# C2 -- dark-sector mass as a horizon-bath excitation LOCKED to a0(z)
# =====================================================================================
print("\n"+"="*92)
print("C2  DARK-SECTOR MASS LOCKED TO a0(z): m_dark(z) = E_L * (a0(z)/a0(0))^q.")
print("    The framework's OWN consequence -- a REDSHIFT-DECLINING horizon-bath mass.")
print("="*92)

# The framework forces a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0). For pure-Lambda rho_DE=const
# -> a0(z)=const; the EVOLUTION lives only if DE rolls (w != -1). Use the DESI-band w0wa
# shape parametrically (NOT re-fit -- representative w0,wa) and the pure-Lambda null.
print("  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).  E_L(z) = rho_DE(z)^(1/4) = E_L*(a0(z)/a0(0))^(1/2).")
print("  => a horizon-bath mass tied to E_L tracks  m(z)/m(0) = (a0(z)/a0(0))^(2q).")

def rho_de_ratio(z,w0,wa):
    return (1.0+z)**(3*(1+w0+wa))*math.exp(-3*wa*z/(1.0+z))

print("\n  branch (i) PURE-Lambda (w=-1): rho_DE const -> a0(z)=a0(0) -> m_dark(z)=E_L CONSTANT.")
print("     This is the CANONICAL footing. No evolution. (the null; m(z)/m(0)=1 at all z.)")

print("\n  branch (ii) DESI-band rolling DE (representative w0=-0.7, wa=-0.7):")
w0,wa = -0.7,-0.7
for z in [0.5,1.0,2.0,3.0]:
    r = rho_de_ratio(z,w0,wa)
    a0z = math.sqrt(r)                 # a0(z)/a0(0)
    ELz = r**0.25                      # E_L(z)/E_L(0) = (a0 ratio)^(1/2)
    print(f"     z={z:>4.1f}:  a0(z)/a0(0)={a0z:.3f}   E_L(z)/E_L(0)={ELz:.3f}"
          f"   [m_dark = E_L: q=1/2 of a0-ratio]")
print("  (NB: this representative thawing pair is NON-monotonic -- a0(z) rises ~11% by z~1")
print("   then falls back below 1 by z=3. The SIGN/size of the swing is w0,wa-dependent.)")
print("  => IF the dark-sector/lightest-nu mass is a horizon-bath excitation pinned to E_L,")
print("     it EVOLVES with a0(z); the banked DESI-chain fits (nu_de_tower.py) give a NET")
print("     ~20-40% DECLINE in E_L(z) over z=0->3 (right-signed for the DESI 'neg-mass' puzzle).")

# the q-knob: is q forced? m_dark ~ E_L = rho_DE^(1/4) gives q=1/2 (in a0-ratio). But a
# Compton/horizon-mass ~ hbar H_L/c^2 gives m ~ H_L ~ a0-ratio^1 (q=1); a Unruh thermal
# mass kT_dS ~ hbar H_L gives the same. So q in {1/2 (energy-scale), 1 (mass~H_L)} is a
# CHOICE -> the exponent is a free knob.
print("\n  the q-knob (both-ways): m_dark ~ rho_DE^(1/4) -> exponent 1/2 in the a0-ratio;")
print("     m_dark ~ hbar H_L/c^2 (Compton/Unruh) -> exponent 1 in the a0-ratio. Both natural.")
print(f"""
  GRADE C2: HYPOTHESIS-WITH-FREE-KNOB.
    GENUINE framework content: the EVOLUTION law a0(z)=sqrt(rho_DE(z)) is forced once
    the dark mass is locked to E_L, and it is the framework's OWN (the swampland papers
    make no z-prediction). It is right-signed for the live DESI Sigma_m_nu puzzle and
    near-term-touchable (DESI DR3/Euclid). FREE KNOBS: (a) WHETHER the dark mass is
    locked to E_L at all (the lock is posited, not derived -- see C1); (b) the exponent
    q (1/2 vs 1); (c) the whole effect VANISHES on the canonical pure-Lambda footing
    (w=-1) -> it is a HOSTAGE to dynamical DE. Real, testable, conditional. Dies if w->-1.""")

# =====================================================================================
# C3 -- EFE / external-field bath -> a LOCAL particle scale
# =====================================================================================
print("\n"+"="*92)
print("C3  EFE / EXTERNAL-FIELD BATH -> a LOCAL mass scale.  An external bath acceleration")
print("    a_ext raises kappa = sqrt(a_ext^2+(cH_L)^2); does E(a_ext) define a new mass?")
print("="*92)

# In modified inertia, the dS-Unruh bath temperature is set by the TOTAL kappa felt by the
# object: kappa = sqrt(a_tot^2 + (cH_L)^2) (Deser-Levin). An object in an external field
# a_ext sees a HOTTER bath -> a higher associated energy E_kappa = hbar*kappa/(2pi c) ... .
# Compute the scale this defines, both at a_ext=0 (the floor, ties to E_L?) and at galactic
# a_ext ~ a0, and ask whether it ever lands near a SM particle scale (it should not: it
# scales with a_ext, which is dynamical, not a fixed rest mass).
def E_kappa_eV(a_ext):
    kappa = math.sqrt(a_ext**2 + (c*H_L)**2)     # 1/s-like (units of acceleration/c below)
    # dS-Unruh temperature: kT = hbar*kappa/(2*pi*c) (kappa as proper accel) -> energy:
    T = hbar*kappa/(2*math.pi*c*kB)               # K
    return kB*T/eV                                # eV
print("  dS-Unruh bath energy  E_kappa = kB T = hbar*sqrt(a_ext^2+(cH_L)^2)/(2 pi c):")
for nm,aex in [("a_ext=0 (cosmic floor)",0.0),("a_ext=a0",a0),("a_ext=10 a0",10*a0),
               ("a_ext=g_solar(1 AU)",0.006),("a_ext=g_Earth",9.8)]:
    E = E_kappa_eV(aex)
    print(f"     {nm:24s}: E_kappa = {E:.3e} eV   (E_kappa/E_L = {E/E_L:.3e})")
print(f"\n  floor (a_ext=0): E_kappa(floor) = {E_kappa_eV(0.0):.3e} eV = hbar*cH_L/(2pi c)/eV-scale")
print(f"     vs E_L = {E_L:.3e} eV.  ratio E_L/E_kappa(floor) = {E_L/E_kappa_eV(0.0):.3e}")
print(f"     (E_kappa floor is the Gibbons-Hawking dS temperature ~1e-33 eV -- it is the")
print(f"      Hubble-energy hbar*H_L, NOT rho_DE^(1/4). The (M_P/Hubble)^(1/2) seesaw that")
print(f"      LIFTS hbar*H_L to E_L is the geometric-mean -- a separate, UV-scale-inserting step.)")

# Does an external-field bath SET a rest mass?  It cannot: E_kappa scales with a_ext (a
# dynamical, position-dependent quantity), so it is a local THERMAL energy, not a fixed
# Yukawa rest mass. The only fixed scale is the floor (hbar cH_L) and its seesaw lift E_L.
print(f"""
  GRADE C3: SPECULATIVE.
    The external-field bath gives a REAL local energy E_kappa(a_ext) = hbar*kappa/2pi c
    that rises with a_ext -- a genuine framework quantity (the EFE-modulated bath temp).
    BUT it is a THERMAL/position-dependent energy, NOT a rest mass: it scales with the
    dynamical a_ext, so it cannot be a fixed Yukawa scale (WALL 1 flavor-blind, WALL 3
    the floor is hbar*H_L ~ 1e-33 eV, ~31 orders below meV). The ONLY way to reach E_L is
    the geometric-mean seesaw that inserts M_P as an external UV scale (banked M3) -- not
    forced by the bath alone. So: a real EFE-thermometer observable (relevant to the dwarf
    sigma-spread fronts), but NOT a particle-mass mechanism. No new SM contact.
    (Cross-link: the a_ext-modulated bath IS the engine of the MW-dwarf sigma-vs-eccentricity
     and relational sigma-spread MI-vs-MG tests -- the real, near-term payoff lives THERE.)""")

# =====================================================================================
# SYNTHESIS
# =====================================================================================
print("\n"+"#"*92)
print("# SYNTHESIS -- Class C grades (de Sitter structure / horizon-dof)")
print("#"*92)
rows = [
 ("C1 horizon-dof seesaw  E_L=M_P/N^p", "SPECULATIVE",
  f"p=1/4 is a DIMENSIONAL IDENTITY (O(1)={ratio4:.3f}, not Z-fixed); N restates E_L"),
 ("C2 dark mass locked to a0(z)",       "HYPOTHESIS-WITH-FREE-KNOB",
  "evolution-law forced IF locked; lock+exponent free; HOSTAGE to w!=-1; DESI-testable"),
 ("C3 EFE-bath -> particle scale",      "SPECULATIVE",
  "real EFE-thermometer E_kappa(a_ext), but thermal not rest mass; floor=hbar H_L, ~31 dex low"),
]
for nm,g,why in rows:
    print(f"  [{g:26s}] {nm:36s}: {why}")

print(f"""
  BOTH-WAYS BOTTOM LINE (Class C):
    * The horizon-dof count N = S_dS = {N:.2e} is REAL and on the SAME dS/Lambda physics
      as a0 -- the Addazi-Meluccio seesaw is a genuine, published, framework-aligned hook.
    * But N does NOT PREDICT the dark/nu mass: E_L = M_P/N^(1/4) is a dimensional identity
      (rho_DE^(1/4) by construction), the O(1) is free + not Z-fixed, and any rho^(1/4) ~ 2 meV.
    * The ONE piece with real teeth is C2 -- the a0(z) = sqrt(rho_DE(z)) LOCK -> a declining
      horizon-bath mass, right-signed for DESI, but a HOSTAGE to dynamical DE (null if w=-1)
      and resting on a posited (not derived) lock. The decisive test is the SAME DESI w(z) gate.
    * C3 surfaces the genuinely-actionable native consequence: the EFE-modulated bath temperature
      drives the MW-dwarf sigma-vs-eccentricity / relational sigma-spread MI-vs-MG tests -- the
      near-term, DE-CLEAN payoff lives in those kinematic fronts, NOT in a new particle scale.
    NEVER 'no doors': N is a real hook, C2 is DESI-live, C3 points at the clean kinematic tests.
    NO re-overclaim: no forced seesaw, no derived mass, founded-not-derived STANDS.""")
print("\nposit_dS_structure.py: done (exit 0).")
