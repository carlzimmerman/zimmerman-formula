# Evidence audit

Scope: bounded numerical evidence, self-audited; no independent reviewer.

1. **Executable success versus physical validity.**22 archived run manifests
   pass schema and hash validation. Order8 integral runs are nevertheless rejected
   because their inner spectra are grossly unphysical. `audit.py` enforces this
   classification; its−2 screen is a gross plausibility test, not an exact Coulomb
   lower bound or a sufficient acceptance test.
2. **Independent Hamiltonian check.**Gaussian-only neutral singlet eigenvalues
   from stored UKRmol integrals reproduce PySCF at R2:−1.1325883966,−0.7097342170,
   −0.4909996520,−0.3738042836. The first ionic target energy is−0.6012477382.
   Raw diagnostic output is retained. This isolates the continuum mixed-integral
   failure but does not benchmark every angular sector or continuum observable.
3. **K convention.**Read the upper triangle by columns, divide Rydberg energies
   by2, form S=(I+iK)/(I−iK). Compare UKRmol eigenphase sums modulo pi. The independent
   phase printout agrees to its output precision. Symmetry/unitarity are necessary
   consistency checks, but follow algebraically from real symmetric K and cannot
   detect the bad inner Hamiltonian. No unitarity loss is promoted into chemistry.
4. **Corrected numerical scope.**Order15→20, radial20→25 and lmax2→4 comparisons
   are reported separately; one stable S00 cannot certify a whole matrix.
   The resonance's0.199 grid location is a candidate, with no sub-grid uncertainty
   estimate. No accepted width, nuclear branching fraction or chemical cross section.
   Corrected outer80→160 propagation is stable for the reported low-energy point.
   No full target-basis, inner-radius, threshold or nuclear-grid convergence.
5. **Nuclear derivatives.**Cross-geometry AO overlaps include moving centers;
   equal-geometry overlap identity, sign alignment, antisymmetry and step halving
   are checked. Near-degenerate subspaces may require a matrix gauge alignment,
   not only signs, in future wider scans. Four-state missing derivative norm is
   not a rate uncertainty. The reported DBOC field is radial only. S_R was taken
   at fixed incident kinetic energy, not fixed total energy, and has only one
   corrected finite-difference step. Rejected order8 half-step tests do not validate it.
6. **Missing physical dependencies.**No continuum-normalized neutral nuclear
   dissociation states, electronic-to-nuclear frame transformation, complete
   spin/rotational symmetry treatment, excited-product network, or finite-mass
   threshold reconciliation. Ordinary-hydrogen rates cannot be transferred to
   nuclear mass ratio100 without recalculation.
7. **Conservation claim.**The clamped Hamiltonian conserves charge and energy;
   unitary elastic scattering is computed. No new chemical source enters photon
   recycling, so no new coupled energy-conservation test or galaxy separation
   claim is made. Earlier manufactured-rate tests remain only software tests.
8. **Resources and provenance.**External source/binary hashes are recorded.
   Upstream full integral test timed out at240s. The point driver uses two OpenMP
   threads even though its runner environment requested one; that setting was
   not a hard cap. Some initial parsing/configuration failures occurred before
   recorded runs; documented fixes did not change the physical source code.
   The release page's inconsistent GBTOlib version is not used as provenance.

The strongest conclusion is that a usable, partially checked continuum route
now exists and a severe numerical artifact was identified. It is neither a
successful galaxy mechanism nor a no-go theorem against all collective media.
