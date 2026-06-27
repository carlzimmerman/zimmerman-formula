#!/usr/bin/env python3
"""
posit_horizon.py  --  CLASS 1: HORIZON / MACH routes to particle physics.
=========================================================================
Enumerate EVERY variant where the REST MASS (inertia's high-acceleration limit)
is SOURCED by the de Sitter horizon rather than input, and grade each against:

  WALL 1  flavor-blindness : the dS-Unruh response couples to |a| only (EP); it
          multiplies e, mu, tau, top, nu IDENTICALLY -> cannot supply 9 flavorful
          Yukawas.
  WALL 3  30-order scale gap: a0 ~ 1e-10 m/s^2 (horizon IR scale, E_dS ~ 2.24 meV)
          vs SM masses ~ MeV-TeV. ~30 orders for charged leptons; CLOSES only for nu.

Footing (framework's OWN, never McGaugh nu): a0 = cH_L/Z = 9.36e-11; Z = sqrt(32pi/3);
dS-Unruh T_eff = (hbar/2pi c kB) sqrt(a^2 + (cH_L)^2) (Deser-Levin gr-qc/9706018).

The variants (this script GRADES each + computes the feasibility of the ONE
genuinely-untried angle the parent flagged: does the dS-Unruh / SO(4,1) response
have a DISCRETE INTERNAL SPECTRUM nobody computed -- discrete series + static-patch
quasinormal ladder -- and could it pattern masses?):

  1a FULL-MACH (rest mass = horizon coupling)            -> TRIED-WALLED (FULL_MACH doc)
  1b HOLOGRAPHIC / area equipartition (mass from S_dS)   -> TRIED-WALLED (area is mass-blind)
  1c dS static-patch ENTROPY -> mass                     -> TRIED-WALLED (S=A/4, dS/dm=0)
  1d dS-Unruh TEMPERATURE LADDER -> mass spectrum        -> TRIED-WALLED (Matsubara=1 scale)
  1e memory-kernel theta(y) internal scale               -> TRIED-WALLED (single IR scale)
  1f principal/complementary-series boundary -> mass     -> TRIED-WALLED (cosmological mass)
  1g propagator-pole "tower"                             -> TRIED-WALLED (tachyonic, attack6)
  --- the parent's FLAGGED untried variant: --------------------------------------------
  1h dS DISCRETE-SERIES of SO(4,1) -> discrete m^2 ladder?   <-- COMPUTE feasibility here
  1i dS static-patch QUASINORMAL-MODE ladder -> spectrum?    <-- COMPUTE feasibility here
  --- the ONE partial-open (published): -------------------------------------------------
  1j NEUTRINO: E_dS = rho_DE^(1/4) ~ 2.24 meV closes WALL 3 for nu only -> PARTIAL-OPEN

Run: python3 posit_horizon.py   (exit 0; sympy/mpmath exact where possible)
"""
import sympy as sp
import mpmath as mp
import math

mp.mp.dps = 40
print("#"*92)
print("# CLASS 1 -- HORIZON/MACH routes: can the dS horizon SOURCE the rest mass?")
print("#"*92)

# ------------------------------------------------------------------ footing (SI) ------
c    = 2.99792458e8
G    = 6.67430e-11
hbar = 1.054571817e-34
kB   = 1.380649e-23
eV   = 1.602176634e-19
Mpc  = 3.0856775814913673e22
H0   = 67.4e3/Mpc
OmL  = 0.685
H_L  = H0*math.sqrt(OmL)                 # pure-Lambda Hubble (declining-sqrt-rho footing)
Lam  = 3*(H0**2*OmL)/c**2
rho_DE = Lam*c**2/(8*math.pi*G)
Z    = math.sqrt(32*math.pi/3)
a0   = c**2*math.sqrt(Lam/(32*math.pi))  # = cH_L/Z
lP   = math.sqrt(hbar*G/c**3)
EPl  = math.sqrt(hbar*c**5/G)/eV         # Planck energy eV
E_dS = (rho_DE*c**2*(hbar*c)**3)**0.25/eV  # rho_DE^(1/4) in eV
m_floor_eV = hbar*H_L/eV                  # IR floor hbar*H_L quoted as energy (eV)

print(f"\n  a0 = {a0:.4e} m/s^2 (= cH_L/Z={c*H_L/Z:.4e})  Z={Z:.5f}")
print(f"  E_dS = rho_DE^(1/4) = {E_dS*1e3:.4f} meV   IR floor hbar*H_L = {m_floor_eV:.3e} eV")
print(f"  SM charged-lepton scales: m_e=5.11e5 eV, m_mu=1.057e8, m_tau=1.777e9 eV")

# =====================================================================================
# WALL CHECKS (the two the parent named) -- made quantitative once, used by all variants
# =====================================================================================
print("\n"+"="*92)
print("WALL 1 (flavor-blindness) and WALL 3 (scale gap), quantified")
print("="*92)
# WALL 1: mu_fw(a/a0) is the framework's interpolation; at any fixed a it is ONE number
# multiplying every species. Show it is flavor-blind: d mu / d(flavor) = 0 trivially,
# and at a=a0 it equals the golden value, identical for all masses.
x = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
mu_at_a0 = sp.nsimplify(mu_fw.subs(x,1))
print(f"\n  mu_fw(a=a0) = {mu_fw.subs(x,1)} = {float(mu_fw.subs(x,1)):.6f} = 1/phi (golden).")
print("  It multiplies e, mu, tau, top, nu IDENTICALLY -> 0 flavor information. WALL 1 stands.")
# WALL 3: gap in dex between E_dS and each lepton
for nm,mE in [("electron",5.11e5),("muon",1.057e8),("tau",1.777e9)]:
    print(f"  scale gap E_dS->{nm}: {math.log10(mE)-math.log10(E_dS):.1f} dex")
print(f"  scale gap E_dS->neutrino(~50 meV): {math.log10(0.05)-math.log10(E_dS):.2f} dex  <-- CLOSES")

# =====================================================================================
# 1h  THE FLAGGED UNTRIED ANGLE #1:  dS DISCRETE SERIES of SO(4,1)
# =====================================================================================
print("\n"+"="*92)
print("1h  dS DISCRETE-SERIES of SO(4,1): is there a DISCRETE internal m^2 ladder?")
print("="*92)
print("""
  attack6 tested the PRINCIPAL series (heavy, m^2/H^2>9/4, nu imaginary) and the
  propagator poles (tachyonic). It did NOT separately test the DISCRETE SERIES of
  SO(4,1)=dS_4 isometry. UIRs of SO(4,1) (Basile-Joung-Oh 1611.xxxxx, Sun 2111.04591,
  Anninos et al): the strictly-normalizable DISCRETE series D(p) in d=4 exists ONLY
  for fields of SPIN s>=1; for SCALARS (s=0) there is NO discrete series at all.
  The discrete-series 'masses' are LABELLED by integers but are SPIN labels, with
  Delta = s+1 (exceptional points), NOT a tower of distinct scalar rest masses.
""")
# Feasibility computation: enumerate the dS_4 (SO(4,1)) UIR families and their mass^2/H^2.
# Scalar principal: Delta = 3/2 + i*lambda, m^2/H^2 = Delta(3-Delta) = 9/4 + lambda^2 (continuous).
# Scalar complementary: Delta in (0,3), m^2/H^2 in (0,9/4) (continuous, NOT discrete).
# Discrete series (spin s>=1, integer t): Delta = s+1, m^2/H^2 = (s+1)(2-s) (FINITE set, spin-labelled).
print("  enumerate SO(4,1) UIR families and their dimensionless m^2/H^2 (H=cH_L):")
s, lam, Delta = sp.symbols('s lambda Delta', real=True)
m2_of_Delta = sp.expand(Delta*(3-Delta))   # d=4: m^2/H^2 = Delta(d-1-Delta) with d-1=3
print(f"    m^2/H^2 = Delta*(3-Delta).")
print("    PRINCIPAL (scalar): Delta=3/2+i*lambda -> m^2/H^2 = 9/4+lambda^2  (CONTINUOUS, lambda in R).")
print("    COMPLEMENTARY     : Delta in (0,3)     -> m^2/H^2 in (0,9/4]      (CONTINUOUS).")
print("    DISCRETE (spin s>=1, the only discrete family): Delta=s+1 ->")
for sv in [1,2,3,4]:
    m2 = (sv+1)*(3-(sv+1))   # = m^2/H^2 at Delta=s+1
    print(f"        s={sv}: Delta={sv+1}, m^2/H^2={m2}  ({'tachyonic/zero' if m2<=0 else 'ok'})")
print("""
  RESULT (feasibility): the discrete series is (i) SPIN>=1 only (no scalar tower -> cannot
  host the spin-0 Higgs-Yukawa rest masses), (ii) its integer label is the SPIN, not a
  generation/mass index, and (iii) the implied m^2/H^2=(s+1)(2-s) goes NEGATIVE for s>=2.
  Even the s=1 member sits at m^2/H^2=2 -> m = sqrt(2)*hbar*H_L/c^2 ~ {0} eV, a COSMOLOGICAL
  mass ~33 dex below m_e. So a 'discrete internal spectrum nobody computed' DOES exist as a
  labelled set, but it is SPIN-labelled, partly tachyonic, and pinned to the cH_L scale.""".format("%.2e"%(math.sqrt(2)*m_floor_eV)))
print("  Coleman-Mandula seals it: SO(4,1) is the SPACETIME isometry; its Casimir labels")
print("  spin & a cosmological mass, and is BLIND to the internal generation/flavor index.")
print("  GRADE 1h: TRIED-on-its-merits-now -> WALLED (spin-only, tachyonic, cH_L-scaled, CM-blind).")

# =====================================================================================
# 1i  THE FLAGGED UNTRIED ANGLE #2:  dS static-patch QUASINORMAL-MODE ladder
# =====================================================================================
print("\n"+"="*92)
print("1i  dS static-patch QUASINORMAL-MODE ladder: a discrete (complex) spectrum -- masses?")
print("="*92)
print("""
  The dS_4 static patch HAS a genuine discrete spectrum nobody in this corpus computed:
  the QUASINORMAL modes (QNMs) of a scalar. Lopez-Ortega (gr-qc/0605027, 0706.2933) gives,
  for dS_4 with Hubble H, the EXACT QNM frequencies:
        omega_{n,l} / H = -i ( l + 2n + Delta_+ ),   n=0,1,2,...  l=0,1,2,...
  with Delta_+ = 3/2 + sqrt(9/4 - m^2/H^2). These ARE an evenly-spaced (arithmetic)
  discrete ladder -> the 'discrete internal spectrum' the parent asked about.
""")
# Feasibility: build the QNM ladder for a light scalar (m->0 => Delta_+ = 3) and show its
# spacing/scale. Then test whether the ladder of imaginary frequencies can be read as a
# REAL mass spectrum (it cannot: they are decay rates, purely imaginary, ~H_L).
n, l = sp.symbols('n l', integer=True, nonnegative=True)
Delta_p = 3  # massless scalar in dS4
omega_over_H = -sp.I*(l + 2*n + Delta_p)
print(f"  massless scalar (Delta_+={Delta_p}): omega_{{n,l}}/H = {omega_over_H}")
print("  ladder (n,l) first few |omega|/H:")
vals=[]
for nn in range(3):
    for ll in range(3):
        vals.append((nn,ll, ll+2*nn+Delta_p))
for nn,ll,v in vals[:6]:
    print(f"     n={nn} l={ll}: |omega|/H = {v}  -> |omega| = {v*H_L:.3e} 1/s, "
          f"energy hbar|omega| = {v*hbar*H_L/eV:.3e} eV")
print("""
  RESULT (feasibility): the QNM ladder is REAL, DISCRETE, and ARITHMETIC (spacing = H_L) --
  this is the genuine 'spectrum nobody computed' -- BUT every level is:
    (1) PURELY IMAGINARY (a decay rate / inverse relaxation time, not a rest mass);
    (2) spaced and scaled by H_L -> energies ~1e-33 eV, ~38 dex below m_e (WALL 3, hard);
    (3) flavor-blind & generation-blind: (n,l) are radial+angular overtone numbers of the
        STATIC PATCH geometry, carry no internal/family quantum number (WALL 1);
    (4) the ladder is INFINITE & equally spaced -> no selection of '3 generations', no
        Yukawa hierarchy (an arithmetic decay ladder cannot make m_tau/m_e ~ 3477).
  So a discrete internal dS spectrum EXISTS (QNMs), is computed here, and is decisively the
  WRONG OBJECT for masses (imaginary, H_L-scaled, structureless).
  GRADE 1i: NOW-COMPUTED -> WALLED (decay ladder, imaginary, H_L scale, no flavor index).""")

# =====================================================================================
# 1d (re-confirm) dS-Unruh Matsubara ladder = ONE scale (kappa), not a spectrum
# =====================================================================================
print("\n"+"="*92)
print("1d  dS-Unruh temperature ladder (re-confirm attack6): Matsubara = single scale")
print("="*92)
a, H = sp.symbols('a H', positive=True)
kappa = sp.sqrt(a**2 + H**2)
print(f"  2*pi*T_eff = sqrt(a^2+H^2)=kappa; KMS poles at omega=i*kappa*k (k in Z): spacing = kappa.")
print("  ONE scale set by CURRENT a (floor H). No eigenvalue selection. WALLED (confirmed).")

# =====================================================================================
# 1j  THE PARTIAL-OPEN: the NEUTRINO -- E_dS closes WALL 3 for nu ONLY
# =====================================================================================
print("\n"+"="*92)
print("1j  PARTIAL-OPEN: the NEUTRINO. E_dS = rho_DE^(1/4) ~ 2.24 meV closes the scale gap")
print("="*92)
print(f"  E_dS = {E_dS*1e3:.4f} meV. Lightest-nu / minimal-NO scale ~ few-50 meV: WALL 3 CLOSED.")
print("  Published anchor: Gonzalo-Ibanez-Valenzuela (2109.10961) AdS-distance bound m_nu1 <~ Lambda4^(1/4).")
print("  Framework adds a0(z)=sqrt(rho_DE(z)) -> a REDSHIFT-DECLINING nu/dark mass (MaVaN-class),")
print("  computed elsewhere (swampland_tower_from_a0z.py / nu_de_tower.py): m(z=3)/m(0)=0.59-0.75.")
print("  HONEST: this is FOUNDED-NOT-DERIVED -- (i) it is a BOUND (inequality), not an equality;")
print("  (ii) coefficient=1 in m_nu=E_dS is fit-by-inversion (no forced factor); (iii) WALL 1 still")
print("  bites (flavor-blind: does NOT explain the OTHER two nu masses or the PMNS angles).")
print("  GRADE 1j: PARTIAL-OPEN (the lone Class-1 partial: scale gap closes for nu; bound-not-equality).")

# =====================================================================================
# SYNTHESIS + the BEST genuinely-untried long-shot feasibility number
# =====================================================================================
print("\n"+"#"*92)
print("# SYNTHESIS -- Class 1 grades")
print("#"*92)
grades = [
 ("1a full-Mach (rest mass = horizon coupling)", "TRIED-WALLED", "orthogonality: v->0 vs Lambda->0 independent"),
 ("1b holographic/area equipartition",           "TRIED-WALLED", "S_dS=A/4 -> dS_dS/dm_i=0, mass-blind"),
 ("1c static-patch entropy -> mass",             "TRIED-WALLED", "entropy is AREA(Lambda,lP), sees no mass"),
 ("1d dS-Unruh temperature ladder",              "TRIED-WALLED", "Matsubara = ONE scale kappa(a), no eigenvalues"),
 ("1e memory-kernel theta(y) internal scale",    "TRIED-WALLED", "single IR scale a0, flavor-blind"),
 ("1f principal/complementary-series boundary",  "TRIED-WALLED", "m_break=1.5 cH_L, cosmological, ~33 dex low"),
 ("1g propagator-pole tower",                    "TRIED-WALLED", "m^2/H^2=-n^2-3n<0, tachyonic (attack6)"),
 ("1h dS DISCRETE-SERIES SO(4,1)",               "TRIED-WALLED", "spin>=1 only, tachyonic s>=2, CM-blind (NEW here)"),
 ("1i dS static-patch QNM ladder",               "TRIED-WALLED", "imaginary decay ladder, H_L scale, no flavor (NEW here)"),
 ("1j NEUTRINO E_dS=rho_DE^(1/4)~2.24 meV",       "PARTIAL-OPEN", "scale gap CLOSES for nu; bound-not-equality"),
]
for nm,g,why in grades:
    print(f"  [{g:13s}] {nm:42s} : {why}")

print("""
  BEST GENUINELY-UNTRIED-IN-CLASS long-shot (now actually computed -> demoted to WALLED, honestly):
    The dS static-patch QUASINORMAL ladder (1i) was the one object in Class 1 that is genuinely
    DISCRETE and that nobody in the corpus had computed. Feasibility verdict (computed above):
    it IS a real discrete arithmetic spectrum, spacing H_L -- but the levels are PURELY IMAGINARY
    (decay rates), scaled by H_L (~1e-33 eV, ~38 dex below m_e), and carry only (n,l) overtone
    labels, NO internal/flavor index. It cannot be a rest-mass spectrum. So Class 1's last untried
    door, once computed, WALLS on the SAME two walls -- scale (WALL 3) + flavor-blindness (WALL 1).
  => Within Class 1, NO genuinely-untried route survives computation; the lone PARTIAL-OPEN is the
     NEUTRINO (1j), and it is FOUNDED-NOT-DERIVED (a published bound, not a derivation).
""")
print("posit_horizon.py: done (exit 0).")
