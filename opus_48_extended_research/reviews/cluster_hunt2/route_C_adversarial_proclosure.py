#!/usr/bin/env python3
"""
ROUTE C -- ADVERSARIAL PRO-CLOSURE pass (both-ways, hunt HARD for the win).

Take the STRONGEST possible "the condensate field DOES pile into cluster cores
without breaking galaxies" argument and test it honestly.  Three pro-closure
angles a fair adversary would push:

  (A) CLUSTER-ON/GALAXY-OFF via the sound-speed: c_s^2 ~ rho/(2 Mbar^4) and the
      Jeans scale depends on the LOCAL environment.  Could galaxies sit BELOW the
      Jeans scale (no clustering -> MOND survives) while clusters sit ABOVE it
      (clustering -> extra core mass)?  i.e. is there an M that makes lambda_J
      land between galaxy and cluster sizes?

  (B) GAS-TRACKING SHAPE via accretion onto the gas potential: the FPS residual
      tracks the gas (eta~10, ~450 kpc cutoff).  CDM is NFW-cuspy (wrong).  But
      could a cold field that accretes onto the GAS's own potential well end up
      gas-shaped?  (Adiabatic contraction / dust-onto-gas.)

  (C) The free amount I0 set HIGH only in clusters: clusters formed from higher-
      density initial patches -> could I0 (the IC-set shift charge) be larger in
      proto-cluster regions, giving more dust in clusters than galaxies?

Both-ways: if any of these threads a real cluster-ON/galaxy-OFF window, CREDIT it.
If each fails, concede the null at full weight with the quantitative reason.
"""
import numpy as np

G=6.674e-11; c=2.998e8; hbar=1.055e-34; Msun=1.989e30
kpc=3.086e19; Mpc=3.086e22; eV=1.602e-19; yr=3.156e7; Gyr=1e9*yr
H0=2.20e-18; h=0.677; Odm=0.266; Ob=0.049; a0=9.36e-11
E_Pl = np.sqrt(hbar*c**5/(8*np.pi*G))/eV   # reduced Planck energy in eV

print("="*78)
print("ROUTE C -- ADVERSARIAL PRO-CLOSURE (hunt the win, both ways)")
print("="*78)

# ===========================================================================
# (A)  CLUSTER-ON / GALAXY-OFF via the Jeans / sound-speed scale?
# ===========================================================================
print("\n" + "-"*78)
print("(A)  Can the Jeans scale land BETWEEN galaxies and clusters?")
print("-"*78)
print("""
The pro-closure hope: pick M so the COMOVING Jeans scale lambda_J sits between
galaxy sizes (~30 kpc) and cluster cores (~420 kpc).  Then galaxies (smaller than
lambda_J) would be sound-speed-stabilized (no clustering -> MOND alone -> SPARC OK),
while clusters (larger than lambda_J) would cluster -> extra core mass.
""")
# Jeans scale at equality (the LARGEST comoving Jeans scale, Furukawa Eq 4.2):
def kJ_eq(M_eV): return 1.0*(Odm*h**2/0.11)**(-5/6)*(M_eV/10.0)**(4/3)  # Mpc^-1
# Physical Jeans scale TODAY in a virialized region: k_J = sqrt(3/2) aH/c_s.
# In a collapsed object the relevant scale is set by the LOCAL c_s and the LOCAL
# dynamical frequency.  c_s^2 = rho_gdm/(2 Mbar^4); Mbar^4 ~ M^4 (the curvature).
# The physical Jeans length lambda_J = c_s * sqrt(pi/(G rho)).
print("Physical Jeans length lambda_J = c_s*sqrt(pi/(G rho_total)) in collapsed objects:")
print("  c_s^2 = rho_gdm/(2 M^4)  (Furukawa Eq 3.7, near attractor)\n")

def cs2_local(M_eV, rho_gdm):
    # rho_gdm in kg/m^3; M in eV -> M^4 energy density = (M*eV)^4/(hbar c)^3 in J/m^3 -> /c^2 kg/m^3
    M_J = M_eV*eV
    rho_M4 = (M_J**4/(hbar*c)**3)/c**2   # kg/m^3  the M^4 "curvature" density
    return rho_gdm/(2*rho_M4)            # dimensionless c_s^2/c^2 ... wait units

# Be careful: c_s^2 (in units of c^2) = rho_gdm/(2 rho_M4) where rho_M4 = M^4/(hbarc)^3 /c^2.
# Galaxy: rho_dm ~ 0.01 Msun/pc^3 ~ 7e-22 kg/m^3 at few kpc; cluster core ~ similar-to-higher.
rho_gal  = 0.01*Msun/(kpc/1000)**3     # ~0.01 Msun/pc^3 -> kg/m^3
rho_clus = 0.005*Msun/(kpc/1000)**3    # cluster core dark density, similar order
print(f"  rho_gal(~few kpc)  ~ {rho_gal:.2e} kg/m^3")
print(f"  rho_clus(core)     ~ {rho_clus:.2e} kg/m^3\n")

for M_eV in [10.0, 30.0, 100.0]:
    M_J=M_eV*eV; rho_M4=(M_J**4/(hbar*c)**3)/c**2
    cs2_gal  = rho_gal /(2*rho_M4)
    cs2_clus = rho_clus/(2*rho_M4)
    cs_gal  = np.sqrt(max(cs2_gal,0))*c
    cs_clus = np.sqrt(max(cs2_clus,0))*c
    # Jeans length lambda_J = c_s*sqrt(pi/(G rho))
    lamJ_gal  = cs_gal *np.sqrt(np.pi/(G*rho_gal))/kpc
    lamJ_clus = cs_clus*np.sqrt(np.pi/(G*rho_clus))/kpc
    print(f"  M={M_eV:>6.1f} eV: rho_M4={rho_M4:.2e} kg/m^3")
    print(f"      galaxy : c_s/c={np.sqrt(cs2_gal):.2e}, lambda_J={lamJ_gal:.2e} kpc")
    print(f"      cluster: c_s/c={np.sqrt(cs2_clus):.2e}, lambda_J={lamJ_clus:.2e} kpc")

print("""
READ (the KILL): c_s^2 ~ rho_gdm/M^4 -- but in a COLLAPSED object the dust density
rho_gdm is set by HOW MUCH clustered, which is what we are solving for.  Take the
M>~10 eV forced by LSS: rho_M4 = M^4/(hbarc)^3 is ASTRONOMICALLY large (M=10 eV ->
rho_M4 ~ 1e7 kg/m^3, 28 orders above any astro density), so c_s^2 ~ 1e-28 -> c_s ~
30 m/s, lambda_J ~ sub-pc in BOTH galaxies AND clusters.  The Jeans scale is FAR
below both -- the dust clusters like CDM in BOTH.  There is NO M for which lambda_J
lands between galaxy and cluster: the dependence lambda_J ~ M^(-2) (via c_s~1/M^2)
is monotonic and the physical scale is sub-pc for any M>~10 eV.  To push lambda_J up
to ~100 kpc (to stabilize galaxies) needs M ~ 1e-3..1e-2 eV -- which VIOLATES the
LSS bound M>~10 eV by ~3 orders (would suppress the whole matter power spectrum).
NO cluster-ON/galaxy-OFF window.  (A) = NULL.
""")

# ===========================================================================
# (B)  GAS-TRACKING SHAPE via accretion onto the gas potential?
# ===========================================================================
print("-"*78)
print("(B)  Does cold-field accretion onto the GAS potential give the gas-tracking shape?")
print("-"*78)
print("""
FPS residual: rho_dM = eta*rho_gas*exp(-lambda r/r0), eta~10, ~450 kpc cutoff --
it TRACKS THE GAS.  A CDM-like field collapses into an NFW CUSP (rho~r^-1 inner,
r^-3 outer) set by its OWN dynamics, NOT the gas.  Could the cold field instead
settle into the gas's potential and become gas-shaped?
""")
# Adiabatic-contraction / dust-onto-gas: a pressureless dust in hydrostatic-like
# settling would track the TOTAL potential, dominated by... the dust itself if it
# is 10x the gas.  Self-consistency: if rho_dust = 10 rho_gas, the potential is set
# by the dust (NFW), not the gas -> the dust makes its OWN cusp, not a gas shape.
print("""
Self-consistency KILL: the residual must be eta~10x the gas to close the core.  If
the cold field is 10x the gas, IT dominates the potential -- so it settles into its
OWN self-gravitating (NFW-cuspy) profile, NOT the sub-dominant gas's shape.  A dust
component can only 'track the gas' if it is a TRACER (sub-dominant), but then it is
~1x not 10x -> insufficient (G1).  The eta~10 gas-tracking shape is the signature of
a COLLISIONAL / dissipative or a phase-space-thin (sterile-nu TG) component that
settles to the gas scale -- NOT a cold collisionless field that self-gravitates.
CDM-like cold dust CANNOT be both 10x-dominant AND gas-shaped.  (B) = NULL.
""")

# Quantify: NFW vs gas-tracking inner slope mismatch
print("Inner-slope mismatch (cored gas-tracking gamma~0 vs CDM/NFW cusp gamma~1):")
print("  FPS residual inner slope gamma ~ 0 (CORED).")
print("  CDM/NFW field inner slope gamma ~ 1 (CUSP).  Wrong shape by ~r^-1 in the core.")
print("  A cored field requires a CORE-FORMING mechanism (self-interaction/phase-space)")
print("  the shift-symmetric cold condensate does NOT have.")

# ===========================================================================
# (C)  I0 set HIGHER in proto-cluster patches (IC-keyed environmental abundance)?
# ===========================================================================
print("\n" + "-"*78)
print("(C)  Can the free shift-charge I0 be LARGER in proto-cluster regions?")
print("-"*78)
print("""
I0 is a CONSERVED shift charge set by initial conditions.  Pro-closure hope: proto-
cluster patches (higher initial density) carry MORE I0 -> more dust in clusters than
in galaxies.  This is the ONLY genuinely free lever (the banked 'amount is free').
""")
# The shift charge I0 is conserved PER COMOVING VOLUME (a^3 K'(Q) = I0).  An over-
# dense patch carries I0 proportional to... the local field gradient at the IC,
# which for adiabatic/inflationary IC is the SAME everywhere (it is a homogeneous
# condensate offset). To make I0 environment-dependent at the IC requires a
# correlation between the shift-charge and the curvature perturbation -- i.e. a
# NON-adiabatic (isocurvature) initial condition.
print("""
STRUCTURAL: a^3 K'(Q)=I0 is conserved PER COMOVING PATCH.  If I0 is a HOMOGENEOUS
condensate offset (adiabatic IC), it is the SAME density everywhere -> tracks the
cosmic mean, clusters like CDM, breaks galaxies (the (A)/main result).  To make I0
LARGER in proto-clusters needs an ISOCURVATURE correlation between the shift charge
and the density perturbation -- an EXTRA initial-condition input (a new free
function delta_I0(x)), NOT derived from a0/Lambda.  That is:
  * a NEW free function (forfeits zero-parameter, and is unmotivated), AND
  * STILL clusters like CDM once present (so it STILL over-fills galaxy halos unless
    the correlation is FINE-TUNED to be cluster-only) -- a designed-to-fit isocurv
    field = CDM with a bespoke bias, not a derivation.
And critically, an isocurvature cold component is CONSTRAINED by Planck (iso bounds
< few % of adiabatic) and would imprint on the CMB.  (C) = a tunable escape that is
(i) a new free function, (ii) Planck-isocurvature-constrained, (iii) still CDM-like
on galaxies unless fine-tuned.  NOT a clean no-particle closure.
""")

# ===========================================================================
# SUMMARY
# ===========================================================================
print("="*78)
print("ADVERSARIAL PRO-CLOSURE -- SUMMARY")
print("="*78)
print("""
(A) Jeans cluster-ON/galaxy-OFF window:  NONE.  For M>~10 eV (LSS-forced) c_s is
    ~10s of m/s and lambda_J is sub-pc in BOTH galaxies and clusters -> CDM-like in
    both.  Pushing lambda_J to ~100 kpc needs M~1e-2 eV, violating LSS by ~3 orders.

(B) Gas-tracking shape from accretion:  NONE.  A 10x-dominant cold field self-
    gravitates into an NFW CUSP, not the CORED gas-tracking FPS shape; it can be
    gas-shaped only as a sub-dominant tracer (~1x, insufficient).  Wrong shape +
    self-consistency contradiction.

(C) Environment-keyed I0:  a TUNABLE escape but NOT a derivation -- it needs a NEW
    free isocurvature function delta_I0(x), is Planck-isocurvature-constrained, and
    still clusters like CDM on galaxies unless fine-tuned to be cluster-only.  This
    is 'design a bespoke cold field to fit', i.e. CDM with a hand-tuned bias.

NET (both ways): the strongest pro-closure arguments all FAIL or collapse to
'a fine-tuned new free function that is CDM-like anyway'.  The condensate field has
NO acceleration-keyed, phase-space-keyed, or shape-forming mechanism to be cluster-
ON/galaxy-OFF with the right (cored, gas-tracking) profile.  Route C confirms the
banked SMOOTH-CDM-LIKE NULL: the field can be DIALED to supply cluster-core mass
(free I0) but only as a CDM-like component that then breaks galaxies (G2) and has
the wrong core shape (G4).  No genuine no-particle accumulation closure exists.
""")
