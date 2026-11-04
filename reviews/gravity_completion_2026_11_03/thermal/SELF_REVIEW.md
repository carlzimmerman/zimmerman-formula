# TH07 finite computation self-review

Review outcome: implementation and finite assertions checked within the
recorded grids, conditional on float quadrature/interpolation and the stated
one-loop equilibrium action. No all-history thermal producer is certified.

Controls executed in run_diagnostic_001: GL128/GL256 thermal integrals against
adaptive scalar integrals at y=0,1e-6,.001,.1,1,25,400 for both statistics;
physical boson/fermion146/146 accounting; twelve extra massless Weyls at X=0;
independent TP01 representation-matrix eigenvalues at four fields; independent
CW function comparison; occupation-integral force against five-point thermal
potential derivatives. Maximum force-control relative difference6.3e-11.
The local finite action reproduces canonical/protected radial masses to
2.7e-8/4.7e-8 fraction, respectively.

run_static_001: all four unresummed numerical spinodals solve the interpolated
stationary/zero-curvature equations. Direct high-precision T0 forces differ
by at most4.8e-17 mu^3 at origin loss and3.2e-20 at outer loss. Direct origin
curvature differs at about1e-4 relative of its cancelling pieces; spinodal
values are numerical estimates, not precision errors or screened predictions.
The threshold for the direct-force audit is2e-15 mu^3 and is recorded rather
than inferred from a success flag. Far-field seesaw derivatives use stable
constant-determinant eigenvalues; wide coverage is60 fields at six temperatures
per gravity point. No continuous sign proof is inferred.

Important exclusions: the flat direction's finite quantum pole/current action
and the protected neutral super-Higgs matching remain incomplete. Global
finite two-loop sources are unavailable outside the published coefficient
fit, so the global thermal profile uses exact neutral tree+full rigid CW.
Thermal self-energies, ring resummation and the corresponding all-field heavy
normal shifts are not solved. Varying a heavy normal off the stationary
background can produce off-shell Goldstone/flat Hessian eigenvalues; this
work does not call those physical thermal tachyons or silently take their
absolute values. At least a resummed background treatment is needed for a
complete all-field thermal minimum.

A thermal phase-space state is an initial input. Chemical equilibrium across
all species is not implied by an ideal-gas free energy. Charged occupation
conservation, neutral scalar inverse decays, companion relics, entropy release
and momentum-dependent photino production are separate dynamical obligations.
An equilibrium outward force is not a dynamical no-go theorem. A cold vacuum
may support a very low reheating/Boltzmann-tail source, whose actual leading
vertices and stable charged companion budget must be checked separately.

Both v2 manifests validated against current dependency and output hashes;
run.status=completed. No prior failed run or source was overwritten. No Git
mutation, install, queue action, or earlier sibling edit was performed.

TH07C final audit: direct tensor rotation preserves external U1 normalization;
physical Goldstone projector residual<1.1e-12;86 real physical scalars;
actual squared vertex norm 1.9575e-5 below the independent all-field charge-trace
bound 2.61e-5. Distinct Majorana spin-trace factors and source spin counts are
stated in DERIVATION. The second run independently checks the 3pi/2 Bessel
normalization and records initial thermal parent yields to avoid interpreting
an equilibrium source integral as a bound on all frozen late decays. Fixed
cold heavy spectra and constant xi are explicit approximations. The high
charged masses make the computed tail exponentially tiny, but no vector,
loop-induced neutral-heavy or all-orders inclusive rate is claimed. Both new
v2 records validate current hashes and completed status. Phase frozen after
this check; real-time roll/depletion remains the kinetic sibling's obligation.

Final math proofreading: DERIVATION.md, STATUS.md and this self-review only.
Routine edits: number/unit spacing, one ambiguous description of the fermion
free-energy sign, and the live continuation wording after the tail calculation.
Mathematical-token changes: “positive physical tree spectra” changed to
“nonnegative physical tree spectra,” uniquely forced by the explicitly retained
massless modes. Equations and numerical values unchanged. No unresolved local
notation or reference issue found. Numerical validation is the four v2 records;
there is no manuscript build for these Markdown research notes.
