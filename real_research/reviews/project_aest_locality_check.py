#!/usr/bin/env python3
"""
The locality 'make-or-break' for the AeST construction, checked: a0 stays UNIVERSAL -> BENIGN (much less severe).
================================================================================================================
The construction (project_aest_darkenergy_construction.py) sets a0 = a0(0) sqrt(rho_DE(Q)/rho0) via a coupling C(Q).
Flagged worry: C depends on the LOCAL aether invariant Q, so does a0 vary between galaxies and break the universal
RAR? Checked here -- and it is benign, for a reason that is the whole point of the rho_DE (not rho_total) reading.

THE KEY: Q is the COSMOLOGICAL / TIME-sector invariant (Q ~ A^mu d_mu phi ~ phi-dot). Galaxies source the SPATIAL-
gradient invariant Y -- that IS the MOND potential -- but they barely touch Q. Inside a quasi-static galaxy the
scalar's time-derivative is ~ the cosmological phi-dot, so Q ~ Q_cosmo, perturbed only at the gravitational-potential
(Phi) / aether-tilt (sqrt Phi) level: delta a0/a0 ~ 1e-6 to 1e-3 for real galaxies (V_flat=100-300 km/s) -- FAR below
the observed RAR scatter (~0.11 dex ~ 29%). So a0 is universal to ~1e-3 or better. The construction survives.

CONTRAST: had a0 tracked the LOCAL TOTAL density (the rejected sqrt rho_total reading), rho_gal/rho_cosmic ~ 1e5
would make a0 vary ~300x between galaxies -- catastrophic. Coupling a0 to rho_DE via the uniform cosmological Q is
exactly what makes a0 universal by construction. Needs numpy.

------------------------------------------------------------------------------------------------------------------
CROSS-REFERENCE (resolved 2026-06-09): the disagreement between THIS file ("Q ~ Q_cosmo, benign") and
project_aest_crosscoupling.py Part 4 ("Q_local environment-dependent, not pinned to Q0") is RESOLVED -- in favor of
this file -- by aest_locality_theta_profile.py. Via the static-aether theorem (Eling & Jacobson 2006, gr-qc/0603058)
a virialized (time-independent-potential) galaxy forces the unit aether purely timelike, A^i = 0, so BOTH
theta = nabla.A and Q = A^mu d_mu phi are pinned to their cosmological values to O(|Phi|) ~ 1e-6 (tighter than the
~1e-3 bound here). crosscoupling Part 4's "environment-dependent" cross term v*dphi' VANISHES for the correct static
aether -- it was implicitly a non-static (A^i != 0) artifact. Contingent on staticity: relaxed galaxies pinned; only
actively merging/collapsing systems (dPhi/dt != 0) get a small transient wobble (see that script's Part D).
"""
import numpy as np

c=2.998e8


def main():
    print("#"*98); print("# Locality check: is a0 = a0(0) sqrt(rho_DE(Q)/rho0) universal across galaxies?  -> BENIGN"); print("#"*98+"\n")

    print("="*98); print("(1) Q is the cosmological/time-sector invariant; galaxies perturb it only at the potential level"); print("="*98)
    print(f"   {'V_flat':>12}{'Phi=(V/c)^2':>14}{'tilt~sqrt(Phi)':>16}{'delta a0/a0':>16}")
    for V in (100e3,150e3,300e3):
        Phi=(V/c)**2
        print(f"   {V/1e3:>8.0f} km/s{Phi:>14.1e}{np.sqrt(Phi):>16.1e}{f'1e-6..{np.sqrt(Phi):.0e}':>16}")
    rar=10**0.11-1
    print(f"\n   observed RAR scatter ~0.11 dex = {100*rar:.0f}% (the universality bound)")
    print(f"   => delta a0/a0 ~ 1e-6 to 1e-3  <<  {100*rar:.0f}%   -> a0 UNIVERSAL. Locality benign.\n")

    print("="*98); print("(2) why the rho_DE (cosmological-Q) coupling is what makes it universal"); print("="*98)
    r=1e5
    print(f"   rejected sqrt(rho_total) reading: rho_galaxy/rho_cosmic ~ {r:.0e} -> a0 would vary ~sqrt = {np.sqrt(r):.0e}x. CATASTROPHIC.")
    print(f"   adopted  sqrt(rho_DE) reading:    rho_DE is the UNIFORM vacuum energy, read via the cosmological Q -> a0 universal.\n")

    print("="*98); print("VERDICT"); print("="*98)
    print("""  The locality problem flagged as the construction's make-or-break is much LESS severe than feared: a0 is
  universal to ~1e-3 or better, because the coupling C(Q) is to the cosmological/time-sector invariant Q -- which
  galaxies perturb only at the gravitational-potential level (~1e-6) -- not the local matter density. This is the
  same fact that resolved the rho_DE-vs-rho_total fork: tying a0 to the uniform dark energy (rho_DE), not the
  clustered total density, makes it universal by construction. So the concrete AeST realization now passes
  ghost-freedom, c_GW=c, CMB-safety, AND universality. Honest caveat: this is an order-of-magnitude argument; a full
  check needs the quasi-static AeST Q-profile inside a galaxy and confirmation that the standard-AeST aether
  stiffness (already CMB-fit by Skordis-Zlosnik) is unchanged by the C(Q) coupling. Downgrade locality from
  'make-or-break' to 'likely benign, pending the full quasi-static solution'.""")
    print("#"*98)


if __name__=="__main__":
    main()
