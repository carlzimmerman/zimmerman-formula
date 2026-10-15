# The old finite boundary fails; a different constrained source is now explicit

2026-10-15. This follows checkpoint c7ae2193db908e9181888dbbff190a514f05cf07. The first local run observed shared repository HEAD 7ababab3ece1cdd36786736e7ea1cdd049ba48d0. The original physical cold-energy propulsion goal is **not achieved**. The main unresolved stability claim of the old model is now decided negatively, rather than left behind a finite-grid success.

## Decisive result

The [harmonic boundary proof](NO_GO.md) constructs a physical negative kinetic-energy direction for **every finite derivative-elastic strength** in the old finite clock-mass model, even at rest. A compact gradient shift can be harmonic throughout the material, making the expansion penalty zero while its Hessian grows with transverse wavenumber. The Einstein shift energy cancels globally in the vacuum outside. The old material term controls the shift's magnitude but not that harmonic shear.

A sufficient bad-wavenumber threshold is k²>4(1+κmax)hmax/M². For κmax=64, M=hmax=1, an explicit smooth witness at k=17 has reduced kinetic energy ≤−29 I/130<0. The capture estimate is rational and analytic; it is not a numerical extrapolation. The previous weighted continuum comparison constant C* is infinite for this old class. Increasing κ to 400 or another finite value cannot fix it.

This supersedes the earlier suggestion that stronger κ might complete that boundary. It does not invalidate the old unconfined theorem, the globally massless cap theorem, or the decaying purely planar theorem, each of which has different hypotheses. It does not rule out every finite gravitational medium. A physical ultraviolet cutoff would require a specified completion; none is currently part of this model.

## What was constructed instead

[REPLACEMENTS.md](REPLACEMENTS.md) proves a full R³ **quadratic rest-state** result for a different finite body: retain nonnegative compact spatial/shift masses, but keep the lapse as a global multiplier by removing the clock mass and lapse-gradient term everywhere. Its constrained reduced energy is nonnegative for every direction and wavelength. This is a continuum theorem, not the result of another passing grid.

The same file specifies a separate shear-gradient operator that directly blocks the harmonic witness. That operator has a completed-square bound for core-supported velocities and passes the selected finite tests. Its all-mode curved theorem remains open.

Deleting a quadratic clock mass alone does not guarantee nonlinear lapse degeneracy. The old inverse-metric strain potential still has generic nonlinear lapse dependence. [SOURCE.md](SOURCE.md) therefore reconstructs the source using **proper material normal velocity B=−β/N and spatial strain C=γinverse−I**, rather than carrying forward that potential.

For this new algebraic F(Φ,B,C) candidate:

- Ten explicit constitutive coefficients match the prescribed stationary Einstein source, including energy, momentum and all spatial stresses.
- Compact source coefficients give a pure Einstein gravitational/material exterior.
- Its canonical Hamiltonian factors as N times a function of the shift ratio s=β/N. Solving s where its constitutive Hessian is invertible leaves N enforcing a nonlinear Hamiltonian constraint. Vacuum constraints are retained without dividing by zero.
- A new, explicitly derived transverse controller current cancels the constant-speed controller source, placing the stationary family in one fixed covariant action. A canonical controller retains the lapse factorization, while adding a scalar to the exterior theory.

These statements close background matching and one nonlinear constraint step. They do **not** establish the full Poisson/Dirac constraint algebra, a healthy nonlinear mode count, positive curved-wall energy, a powered launch, or a physical source material. The explicit reduced Hamiltonian is given so the next missing implication can be audited directly. No old unconfined stability or energy-cost number is silently transferred to this new action.

## Verification and failed runs

- [Harmonic v2](run_v2/calculation/results.json): 16 exact identities and rational checks supporting the analytic counterexample and shear completion.
- [Replacement v2](replacement_run_v2/calculation/results.json): 29 finite implementation/benchmark assertions across nine constrained cases. The original negative control is reproduced. The globally constrained model matches independent TT kinetic bounds and static identities. Near-zero numerical residuals remain; the analytic theorem supplies the scoped conclusion.
- [Source v5](source_run_v5/calculation/results.json): 27 exact identities, including all ten source variations, old/new potential degeneracy, ADM source signs, controller cancellation and the explicit reduced Hamiltonian.

Counts contain different kinds of checks and are not independent proof votes. Earlier completed versions and two failures are frozen. Harmonic v1 failed because its symbol declaration admitted k=0 while its derived formula assumed k>0; v2 aligns the declaration with the contract. Source v1 failed a hand-entered potential-Schur benchmark; v2 corrects that benchmark without changing the differentiated potential. [The self-review](REVIEW.md) states remaining risks. No independent reviewer or novelty search is claimed.

## What remains before a propulsion claim

The exact next mathematical task for the new source is constraint preservation for its explicit reduced Hamiltonian, including the constitutive/vacuum interface, followed by curved-background reduced energy. A lapse multiplier alone does not settle those questions. The optional controller requires a coupled audit as well.

The separate physical gap is still substantial: the stress functions are assigned to reproduce a metric; no identified cold carrier or known material produces them. The background still requires negative normal stress energy. A finite powered evolution with the apparatus, payload and conserved full energy/momentum has not been solved. Nothing here establishes a black-hole/horizon fuel process or conversion of dark energy into baryons.

The outcome is therefore a rigorous rejection of the old finite construction and a more structurally constrained replacement action—not a completed or demonstrated cold-energy drive.
