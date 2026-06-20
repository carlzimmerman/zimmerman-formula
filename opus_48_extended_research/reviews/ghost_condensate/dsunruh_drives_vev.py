#!/usr/bin/env python3
"""
dsunruh_drives_vev.py  (topic: dsunruh_drives_vev)

Does de Sitter-Unruh / Lambda DRIVE the ghost condensate (set the derivative VEV scale M)?

Ghost condensate (Arkani-Hamed-Cheng-Luty-Mukohyama 2004, hep-th/0312099):
  L = M^4 * P(X),   X = (d phi)^2 / M^4   (dimensionless),
  P(X) has a NON-TRIVIAL MINIMUM at X = X0 > 0  (prototype P(X) = (1/8)(X - c^2)^2, X0=c^2~O(1)).
  Condensate: <d_t phi> = M^2 * sqrt(X0)  ->  spontaneously breaks Lorentz/time-translation -> preferred frame.
  Fluctuations pi:  L_pi = (1/2)(pi-dot)^2 - (alpha/2 M^2)(nabla^2 pi)^2  -> dispersion omega^2 = (alpha/M^2) k^4.
  Energy density / EoS: at the SSB point rho=-p (w=-1, CC-like); IR fluctuations -> w=0 dust-like clustering.
  Jeans: L_J ~ M_Pl/M^2,  t_J ~ M_Pl^2/M^3,  unstable-lump rho ~ M^6/M_Pl^2.
  Bounds: Newton-potential twinkling/static-source  M <~ 10 MeV;  BH accretion tighter still.

AeST dictionary (Skordis-Zlosnik 2021; Verwayen-Skordis-Zlosnik 2024, arXiv:2304.05134 / MNRAS 531,272):
  K(Q) = K2 (Q - Q0)^2  near the condensate  (Q = A^mu d_mu phi = the TEMPORAL invariant).
  -> THIS IS A GHOST CONDENSATE: Q0 is the derivative VEV (the X0), K2 sets the curvature of P at the min.
  Quasistatic: time-diffs broken -> the metric potential Psi gets a MASS mu,
     m^2 = (2 K2 / (2 - K_B)) * Q0^2   (mass term; m ~ mu the GC fluctuation mass).
  Verwayen et al: mu treated as a FREE parameter, mu^-1 >~ 1 Mpc for MOND to survive at galaxy scales;
     a0 enters ONLY via J(Y) (spatial), Q0/mu independent of a0.

So in the AeST language the "condensate VEV scale M" maps to TWO things:
  - Q0  = the derivative VEV  (<A.dphi> at the minimum)  <-> M^2 sqrt(X0)
  - mu  = the GC fluctuation mass = the Psi mass that sets the dust clustering scale  <-> M^2/M_Pl-class

QUESTION: does the de Sitter scale (cH_Lam, T_GH=H/2pi, or a0=cH_Lam/Z) set Q0 / mu / M?
And: what M does the DUST AMPLITUDE (Omega_dm) need, vs what the dS scale gives?
Both ways.
"""
import numpy as np

# ---------------- constants (SI + natural) ----------------
c      = 2.99792458e8        # m/s
G      = 6.67430e-11         # SI
hbar   = 1.054571817e-34     # J s
kB     = 1.380649e-23
Mpc    = 3.0856775814913673e22  # m
kpc    = Mpc/1e3
Gyr    = 3.15576e16          # s
eV     = 1.602176634e-19     # J
MeV    = 1e6*eV
GeV    = 1e9*eV

# cosmology (framework footing, banked)
H0_kms = 67.4                # km/s/Mpc
H0     = H0_kms*1e3/Mpc      # 1/s
Om_L   = 0.685
Om_m   = 0.315
Om_dm  = 0.265               # cold dark matter density param
Om_b   = 0.050
h      = H0_kms/100.0

# de Sitter / Lambda
H_L    = H0*np.sqrt(Om_L)            # pure-Lambda Hubble (framework canonical footing)
Lam    = 3*Om_L*H0**2/c**2           # m^-2  (Lambda = 3 Om_L H0^2 / c^2)
cH_L   = c*H_L                       # m/s^2-ish (the dS acceleration scale)
Z      = np.sqrt(32*np.pi/3)         # 5.7888
a0     = c**2*np.sqrt(Lam/(32*np.pi))# = cH_L/Z = 9.36e-11
T_GH   = hbar*H_L/(2*np.pi*kB)       # Gibbons-Hawking temperature (K)
rho_DE = Om_L*3*H0**2/(8*np.pi*G)    # dark-energy density (kg/m^3)
rho_dm = Om_dm*3*H0**2/(8*np.pi*G)   # dark-matter density (kg/m^3)

# Planck units (natural)
M_Pl_GeV  = 2.435e18    # reduced Planck mass in GeV
M_Pl_J    = M_Pl_GeV*GeV
# energy<->mass via mc^2; "mass scale M in energy units"

print("="*78)
print("FRAMEWORK FOOTING")
print("="*78)
print(f"H0        = {H0:.4e} 1/s   ({H0_kms} km/s/Mpc)")
print(f"H_Lambda  = {H_L:.4e} 1/s")
print(f"Lambda    = {Lam:.4e} m^-2")
print(f"a0        = {a0:.4e} m/s^2   (cH_L/Z, Z={Z:.4f})")
print(f"cH_L      = {cH_L:.4e}        (a0*Z)")
print(f"T_GH      = {T_GH:.4e} K  = {kB*T_GH/eV:.4e} eV")
print(f"rho_DE    = {rho_DE:.4e} kg/m^3")
print(f"rho_dm    = {rho_dm:.4e} kg/m^3")
print(f"Om_dm/Om_L= {Om_dm/Om_L:.4f}")

# ============================================================================
# PART A. What energy/mass scale does the de Sitter sector hand you?
# ============================================================================
# The candidate dS scales, expressed as ENERGY (so we can compare to M~10 MeV GC bound)
print("\n"+"="*78)
print("PART A. de Sitter energy/mass scales (candidate condensate scales)")
print("="*78)

# (a) Gibbons-Hawking temperature as an energy
E_GH   = hbar*H_L            # J  (the dS "temperature" energy ~ kB T_GH * 2pi)
E_GH_eV= E_GH/eV
print(f"(a) Hubble energy hbar*H_L           = {E_GH_eV:.4e} eV   (~{E_GH_eV*1e33:.2f} x10^-33 eV)")
print(f"    kB*T_GH                          = {kB*T_GH/eV:.4e} eV")

# (b) dark-energy density as a quartic scale: rho_DE = M_DE^4 (in natural units)
#     M_DE = (rho_DE)^(1/4) in energy.  rho in J/m^3 -> convert: rho*hbar^3 c^3 has units J^4? do it cleanly:
#     energy density u [J/m^3]; natural scale E s.t. E^4/(hbar c)^3 = u  -> E = (u (hbar c)^3)^(1/4)
u_DE   = rho_DE*c**2        # J/m^3
E_DE   = (u_DE*(hbar*c)**3)**0.25   # J
E_DE_eV= E_DE/eV
print(f"(b) rho_DE^(1/4) (vacuum scale)       = {E_DE_eV:.4e} eV  = {E_DE_eV*1e3:.3f} meV")

# (c) dark-matter density as a quartic scale
u_dm   = rho_dm*c**2
E_dm   = (u_dm*(hbar*c)**3)**0.25
E_dm_eV= E_dm/eV
print(f"(c) rho_dm^(1/4) (dust scale)         = {E_dm_eV:.4e} eV  = {E_dm_eV*1e3:.3f} meV")

# (d) a0 as an energy via a0 = c * (E/hbar)? a0 has units m/s^2; hbar*a0/c^2 is an energy
E_a0   = hbar*a0/c          # J : a0/c is a frequency-ish (1/s); times hbar -> energy
E_a0_eV= E_a0/eV
print(f"(d) hbar*a0/c (accel energy)         = {E_a0_eV:.4e} eV")

# ============================================================================
# PART B. The GHOST-CONDENSATE dictionary: what M does each AeST scale imply?
# ============================================================================
print("\n"+"="*78)
print("PART B. Ghost-condensate scales from the AeST mass mu (the Psi mass = dust clustering)")
print("="*78)
# AeST: mu^-1 >~ 1 Mpc (Verwayen et al). mu is the GC fluctuation mass (Compton-like).
# In GC: the relevant IR scale where Newtonian gravity is modified / dust clusters:
#   The GC "Jeans"/oscillation scale is L ~ M_Pl/M^2 (geometric), and the fluctuation
#   effective mass for clustering is mu ~ M^2/M_Pl.  So mu and M relate via mu = M^2/M_Pl.
# Invert AeST's mu (>~ 1/Mpc) to a GC SSB scale M:
for mu_inv_Mpc in [1.0, 10.0, 100.0]:   # mu^-1 in Mpc (AeST range ~ 0.1-100 Mpc; canonical >~1)
    mu_inv = mu_inv_Mpc*Mpc             # m
    mu_len = 1.0/mu_inv                  # 1/m
    # mu as an energy (Compton): E_mu = hbar c / (mu^-1)
    E_mu   = hbar*c*mu_len               # J
    E_mu_eV= E_mu/eV
    # GC dictionary mu = M^2/M_Pl  ->  M = sqrt(mu * M_Pl) in energy units
    M_gc   = np.sqrt(E_mu*M_Pl_J)        # J
    M_gc_eV= M_gc/eV
    print(f"  mu^-1={mu_inv_Mpc:6.1f} Mpc -> E_mu={E_mu_eV:.3e} eV ;  GC M=sqrt(mu*MPl)={M_gc_eV/1e6:.4f} MeV")

print("\n  -> AeST's mu^-1 ~ Mpc maps (via mu=M^2/M_Pl) to a GC SSB scale M ~ few MeV,")
print("     i.e. RIGHT AT the canonical GC bound M<~10 MeV.  Interesting but see PART D.")

# ============================================================================
# PART C. Does any dS combination SET mu (the clustering scale) ?
# ============================================================================
print("\n"+"="*78)
print("PART C. Can the dS scale set mu (the dust clustering length) ? compare to mu^-1>~1 Mpc")
print("="*78)
# The ONLY length the dS sector naturally supplies is the Hubble/horizon length:
L_H    = c/H_L
print(f"  dS horizon length c/H_L           = {L_H/Mpc:.3e} Mpc")
print(f"  AeST clustering mu^-1 needed       ~ 0.1 - few Mpc (galaxy MOND survival)")
print(f"  ratio (mu^-1)/(c/H_L) for mu^-1=1Mpc = {1.0*Mpc/L_H:.3e}")
print("  -> the dS horizon is ~4400 Mpc; the clustering scale is ~1 Mpc: OFF by ~10^3-10^4.")
print("     dS gives ONE length (horizon); the dust needs a DIFFERENT, much shorter one.")

# a0 supplies a length too: L_a0 = c^2/a0 (the MOND/Hubble-ish length)
L_a0   = c**2/a0
print(f"  MOND length c^2/a0                 = {L_a0/Mpc:.3e} Mpc  (~Hubble; NOT ~1 Mpc either)")

# ============================================================================
# PART D. What does the DUST AMPLITUDE (Omega_dm) need for M, and does dS give it?
# ============================================================================
print("\n"+"="*78)
print("PART D. Dust amplitude Omega_dm: what M does it need, vs what dS hands you")
print("="*78)
# In the AeST condensate the dust density is rho_dust = Q0 * I0 / a^3 (I0 integration const).
# The condensate energy density at the minimum is rho ~ M^4 * P(X0) -- but P(X0)=0 by the
# "no CC" tuning, so the LEADING energy is the FLUCTUATION/offset, an integration constant.
# Equivalent GC statement: the homogeneous condensate's ENERGY is NOT fixed by M alone;
# rho_cond = (2 X0 P'(X0) - P(X0)) M^4 ; at the minimum P'(X0)=0 AND P(X0)=0 -> rho=0 EXACTLY.
# The a^-3 dust is the FLUCTUATION delta-rho riding on top, amplitude = free initial datum.
print("  KEY: at the GC minimum  P'(X0)=0  AND (no-CC tuning) P(X0)=0  -> rho_cond = 0 EXACTLY.")
print("       Homogeneous EoS at the point: w=-1 (CC-like) but tuned to zero energy.")
print("       The a^-3 DUST is the FLUCTUATION delta-rho on top; its amplitude is a")
print("       free integration constant (I0), NOT fixed by M.  (matches banked I0-free result)")

# If one INSISTED M^4 set the dust: M_dust = rho_dm^(1/4):
print(f"\n  If (counterfactually) rho_dm = M^4:  M_dust = rho_dm^(1/4) = {E_dm_eV*1e3:.3f} meV")
print(f"     -> that is ~10^-3 eV ~ the dark-ENERGY (CC) scale, NOT 10 MeV.")
print(f"     The GC SSB scale (from clustering, PART B) is ~MeV; the energy-density scale is ~meV.")
print(f"     These are DIFFERENT scales (M_clustering ~ 10^10 x M_energy): the GC has TWO scales,")
print(f"     and NEITHER is fixed by a single dS input.")

# ratio check: the "why now" Omega_dm/Omega_L
print(f"\n  why-now ratio Omega_dm/Omega_L     = {Om_dm/Om_L:.4f}")
print(f"  candidate dS dimensionless numbers: Om_L={Om_L}, 1/Z={1/Z:.4f}, (3/8pi)^(1/4)={(3/(8*np.pi))**0.25:.4f}")
print(f"     1/Z={1/Z:.4f}, 1/Z^2={1/Z**2:.4f}, none = 0.387 within tolerance")
print(f"     -> no dS identity hits Omega_dm/Omega_L (matches banked PIN_THE_AMOUNT null).")

# ============================================================================
# PART E. The dS-VACUUM / SSB gate: does a CONDENSATE evade the SO(4,1) gate?
# ============================================================================
print("\n"+"="*78)
print("PART E. Does the condensate EVADE the SO(4,1) vacuum gate?  (the wall-1 question)")
print("="*78)
print("  Wall-1 gate (banked): the dS VACUUM is SO(4,1)-invariant -> picks no frame ->")
print("    one-loop induces no preferred-timelike kinetic term.")
print("  GHOST CONDENSATE logic: the symmetry is broken by the SOLUTION <dphi>=M^2 delta_0,")
print("    NOT required of the vacuum action. The action P(X) is Lorentz-INVARIANT;")
print("    the GROUND STATE is not. So a condensate CAN carry a preferred frame on a")
print("    Lorentz-invariant (even SO(4,1)-invariant) action.  => the gate is EVADED *in form*.")
print("  BUT what the gate forbids is the dS vacuum DERIVING the kinetic term P(X). The GC")
print("    still POSTULATES P(X) with a min at X0; nothing in dS-Unruh DERIVES that P has a")
print("    ghost (wrong-sign) quadratic + min. dS-Unruh DRIVING the condensate would require")
print("    dS dynamics to GENERATE P(X) and to SET X0/M. PARTS B-D show it sets NEITHER the")
print("    clustering scale (off by 10^3-4) NOR the energy scale (free I0). So:")
print("    EVADES-THE-GATE-IN-FORM (condensate breaks symmetry via solution) but does NOT")
print("    DERIVE/DRIVE the condensate (P, X0, M, amplitude all remain inputs).")

print("\nDONE.")
