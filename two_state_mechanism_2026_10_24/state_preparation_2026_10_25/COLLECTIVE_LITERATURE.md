# Emergent-fermion alternative: checked bridges and missing operators

Checked 2026-10-25. Source question: can a known interacting spin liquid supply
our field-linear dipole mass and critical response while avoiding identification
of quasiparticle mass with the gravitating constituent mass? No novelty claim.
Sources were read through the web tool; full texts are not copied into the repo
or cached here, so no retained-source hash is claimed. This is a focused source
check, not a reproduction of those papers' many-body calculations.

## Physical probe versus gapless spectrum

Smith et al., *Neutron scattering signatures of the 3D hyperhoneycomb Kitaev
quantum spin liquid*, PRB 92, 180408(R) (2015), published abstract checked:
https://doi.org/10.1103/PhysRevB.92.180408 . It explicitly reports a spin-response
gap despite a gapless spin-liquid phase. This is a magnetic probe result; its
transfer to an electric dipole operator is unverified.

Bolens et al., *Mechanism for subgap optical conductivity in honeycomb Kitaev
materials*, arXiv:1711.00308v4 (14 April 2018), PRB 97, 161108 (2018):
https://arxiv.org/html/1711.00308v4 . Full operator/flux argument checked at
Eqs.7--16. The derived electric polarization is an antisymmetric bond-spin
bilinear. It changes the flux sector, so its matrix elements cannot be replaced
by the density of gapless matter Majoranas alone. The microscopic amplitude
also requires hopping, Hund coupling, spin-orbit coupling and crystal-field
inputs. **Verdict:** the shortcut from nodal DOS to our dipole spectrum is
inapplicable to this specified operator. This does not exclude other operators
or three-dimensional spin liquids. The abstract's revision date, not a later
HTML rendering date, identifies the version.

## Static electric-field perturbation

Chari, Moessner and Rau, *Magnetoelectric generation of a Majorana-Fermi surface
in Kitaev's honeycomb model*, arXiv:2010.11200v1:
https://arxiv.org/html/2010.11200v1 . Secs.VI and IV.3, especially Eqs.53--56,
were checked. At the stated weak-field order, electric-only terms shift the
Dirac nodes rather than opening our proposed linear mass. Crossed electric and
magnetic fields induce a chemical-potential-like term proportional to
n dot (E cross B). **Verdict:** adjacent mechanism, not the required mass.
Our sign check for a pocket with DOS C*epsilon is
Delta F=-integral_0^|mu| C*epsilon*(|mu|-epsilon)d epsilon=-C*|mu|^3/6.
Degeneracy/Majorana counting changes the positive prefactor, not the sign.
For mu proportional to E at fixed B, this gives the opposite cubic sign from
our saturating polarization. It is only this pocket contribution, not a claim
about every term in the full material's free energy.

Noh, Hwang and Moon, *Manipulating Topological Quantum Phase Transitions of
Kitaev's Quantum Spin Liquids with Electric Fields*, arXiv:2308.00760v1 (1 August
2023), later PRB 109, L201105 (2024): https://arxiv.org/pdf/2308.00760v1 .
Table I and the symmetry discussion were checked in the preprint; the
publisher's abstract authenticates title/authors, not equality of all revisions.
The mass is even under E reversal, with allowed h*E^2 contributions, while the
chemical-potential function is E-odd. **Verdict:** electric control of mass is
real in the stated model, but a linear mass at zero electric field does not
follow. At a zero-mass point with m proportional to E^2, our +|m|^3 term would
be proportional to E^6, not |E|^3. A nonzero initial mass cuts off the singularity.

## Route disposition

Emergent fermions evade the fundamental-particle packing identification, but
these sources do not supply the missing dark-medium construction. A promising
continuation must derive a physical flux-preserving electric operator with the
right symmetry, field order and sign in a specified 3D phase, then account for
its actual constituent mass, countercharges and preparation. That route is open;
no lattice, cooling law, angular-velocity dependence or galaxy selector has been
derived here. Do not equate a magnetic field in these papers with galaxy rotation
without deriving the coupling.
