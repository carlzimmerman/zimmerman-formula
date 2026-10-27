# Self-review

Same-agent audit; no external review or novelty claim. Four completed runs:
run_spectrum, run_chemistry, run_extend, run_check. Exact inputs, imports and
result dependencies are pinned in each contract/manifest.

## Physical model boundaries

This is a Coulomb parent completion, not a deduction of a global molecular
potential from the prior harmonic Hamiltonian. The Morse-family example proves
why local curvature alone is insufficient. The old phenomenological band and
molecular assembly have NOT been derived simultaneously from this parent.
The positively charged molecule escapes the neutral-atom charge objection,
but free X also has+Q, and molecular Q/m is about half that of X at mass ratio100.
Repulsive gauge charge is not a demonstration of tethered galactic orbits.

The two-center electronic curve is variational within a minimal basis. It
omits long-range induced polarization and richer electronic states. Radial grid
convergence cannot establish convergence to the exact Coulomb spectrum. Finite
mass and diagonal BO corrections are omitted. Nuclear rotational weights are
explicit simplified statistics, not spin-projected identical-particle states.
The photo coefficient is a selected J0->J1 channel; nuclear exchange/statistical
weights, other continua, higher multipoles and radiative branching are omitted.

## Numerical and analytical checks

- Ground potential includes nucleus-nucleus repulsion; separated threshold is
  -.5, so radial potential is U+.5 and E<0 is the bound-state criterion.
- Binding energies from two meshes agree within2.04e-6 E_H at mass ratio100.
  Same15(v,J) levels, total rotational weight83. The termination test min(V_J)>=0
  excludes bound levels at all larger J for this discretized positive-kinetic
  Hamiltonian. Near-threshold/continuum errors of the approximate potential remain.
- Continuum initial wavepacket is explicitly projected off bound eigenvectors.
  Its zero capture is supported by the exact projector commutation argument;
  it is not independent evidence against radiation-assisted capture. Core
  probability is reported separately to prevent relabeling transient dwell as
  formation. Direct tridiagonal energy evaluation is independent of phase sums.
- Radial continuum matrix elements use normalized box vectors. Strength density
  divides by energy spacing for cross sections; summed blackbody coefficients
  use raw box strengths with no extra density factor. Box and cutoff checks are
  separate. Inverse thermal coefficient is defined by derived detailed balance;
  its agreement with that relation must NOT be counted as an independent test.
- All microscopic photonic events obey photon energy E_cont+D_bound. No actual
  photon-coupled reaction trajectory is simulated. Equilibrium endpoint energy
  conservation is distinguished from radiative kinetic evolution.
- Chemical equations retain C countercharges: c=x+t and x+a+2t=1. Hence molecular
  formation cannot silently discard released negative charge. Molecular energy
  uses the thermal mean of computed bound-level energies, not only the deepest
  level. Independent free-energy/chemical-potential checks in run_check verify
  this accounting in9 interior cases.
- Uniform bound follows algebraically from t(x+t)=a²/r, a=1-x-2t, and r>=A_mu/W.
  It applies only to the specified spectrum and four-species model. Additional
  bound states/statistical weights alter W; other species change the constraints.
- The525-point scan has ZERO common applicability-passing points and is not an
  astrophysical exclusion sample. The42-point extension has29 closed-matter and
 30 fixed-T common applicable points. Both sets are retained separately. Summing
  every raw point as567 physically tested successful approximations would be wrong.
- Molecular abundance cap and conditional population results do not validate
  finite-age equilibration. Very dilute environments may not reach equilibrium.
  Reference rotation is absent; common-boost invariance only rejects a spurious
  direct local rotation multiplier, not effects through real assembly history.

## Source scope

NIST E1 parity/DeltaJ rules were directly opened and checked. No molecular
potential was copied from a source; explicit normalized orbital integrals were
used. Search results from unofficial teaching sites were not relied on for
numerical evidence. No assertion of an exact molecular dissociation energy.

## Remaining scientific risk

This restricted gas may omit dominant neutral-molecule chemistry, screening,
correlations, or a condensed phase. It has not reproduced the critical dipole
spectrum, isotropy, acceleration scale, physical mass inventory or live gravity.
Nonequilibrium assembly could exceed the equilibrium bound; no rate integration
has tested that possibility. Do not call this an all-mechanism no-go.
