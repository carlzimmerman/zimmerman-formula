# Nuclear outgoing flux continuation

Base checkpoint0343483bcb63d46da0b1fd4fde2f1509d0bdbb3c.
Target: state-resolved T_b+C -> A_n+A_m rates, coupled to radiation with energy,
charge and constituent conservation, same microscopic parameters for all profiles.
Success requires converged entrance-to-product flux, not an arbitrary source.

Route1 (execute): replace four-state nuclear projection with the complete singlet
Ag sector of the chosen Gaussian electronic space. Construct the projected radial
Hamiltonian with exact cross-geometry overlaps; solve its multichannel outgoing
boundary problem. Test asymptotic product channels, flux balance, reciprocity,
grid/domain/electronic truncation. This supplies neutral nuclear scattering only
until electron entrance/autoionization coupling is calculated.
Route2 (investigate): Feshbach/nonlocal optical potential or energy-dependent MQDT
from the corrected electronic R matrix. Identify exactly what archived outputs
provide and which channel-resolved kernels are missing; do not identify physical
open K with short-range quantum defects or diagonal widths with a full kernel.
Route3 (execute independent conservation work if needed): branch-resolved chemical
and photon energy bookkeeping and threshold test, with no manufactured rates
labeled physical. Products may include excited atoms, ion pairs and ionization.

Chosen discretization: symmetric radial second difference projected between
actual normalized electronic states. Diagonal kinetic1/(mu*h²), neighboring
block−O(R,R+h)/(2mu*h²), its transpose on reverse link. This retains the moving-
basis metric through the overlap, without assuming four-state completeness.
Nuclear reduced mass50 and J=0 are a restricted radial convention, not full
rovibrational/spin-averaged physical rates. Lead matching uses the exact discrete
lattice dispersion for numerical flux accounting; continuum convergence is a
separate test. No arbitrary absorbing strength is used.

Do not alter previous pinned inputs. New runs and contracts live here. Published
H2/HD rate coefficients cannot be copied to M/m100. A failed numerical approach
is not a no-go theorem. Full astrophysical goal remains unchanged.
