# IC31 executed constrained-exterior checkpoint

Base90489d78165de9252ae984e5728f111373ae9640. Full theory **OPEN**.
Both jobs are terminal and both v2 manifests validated against their input
and output hashes. No source changed during either run.

## Actual commands and exits

Exact argv and runner invocations are in run_index.json and the manifests.

- Closure suite:402 tests in218.624s, child0/runner0.
  Recorded runner runtime219.195234s. Validator0.
- Nonlinear exterior scientific run:all ten scoped checks true;
  strict child2/runner1, runtime14.220166s. Validator0.

Strict2 preserves the full-theory OPEN verdict, and the runner's failed
status is retained honestly. It is not a failed scoped residual test.
Each job had300s wall and2MiB log caps, cooperative1numericalthread, and no
hard memory/affinity cap. No resource limit was reached.

## Strongest new same-action result

The formerly unsolved lapse and multiplier equations are now solved
numerically on a finite pinned exterior of the IC29 action, along with the
z, momentum and pin constraints. The shift equation uses the actual
variable t(S), and the q Euler equation determines the initial Qdot.
No action coefficient is reconstructed as shear is changed.

The fixed41/81-node D approximations both solve amplitudes0,.5,1,2 on r2..8.
The81-node action also solves amplitude1 on r2..12. All coefficient iterates
remain inside the declared domain, about[.1,.104953195]. Every solution has
positive D, B and initial physical normal expansion, and remains on eta=1.

For the refined amplitude1 case:

    q=-2.755868541549812, Q=.1,
    Sbar=.10097996320944924,
    max S=.1014786050412294,
    max |S-Sbar|=.0004986418317801528,
    inner z=.9061388157623438,
    inner ell=13.333977494545566,
    min H_normal=.9476668838998314.

All numbers are model units and constructed data, NOT galaxy observations.
At amplitude2 the refined maximum S is .102791103134686 and the inner ell
is about9.9664, still finite. The zero-shear control reproduces the actual
homogeneous constraint root with zero reported lapse displacement.

The largest lapse residual across all nine solves is below4.71e-9. Cubic
z residuals are below2e-16, and the derived multiplier back-substitution
residuals are below2e-15. Shift residuals are tested between quadrature nodes,
not merely where the integrand was interpolated; all pass1e-7.
The represented S is the integral of the represented slope, so its first
and second derivatives used in these residuals belong to ONE function.

Refined128/256-cell radial constraint largest eigenvalues:

    amplitude0:  -1000.1586888609747, -1000.1586894613766
    amplitude.5: -1000.4241121246218, -1000.4241235839085
    amplitude1:  -1000.6398492372532, -1000.639871371235
    amplitude2:  -1001.0954447966469, -1001.0954987810095

These are calculated eigenvalues of the linearized auxiliary boundary
operator, not assigned determinants, propagating frequencies or DOF counts.
The R12 control gives -1000.1778070473745,-1000.1778124096916; the larger
domain changes the spectrum, while its inner peak S differs from R8 by
about3e-17. This is a finite boundary-sensitivity check, not proof of an
infinite-radius matched solution.

## Adversarial self-audit

Primary verdict: **computationally verified only in the stated range**.

Dependency chain: IC29 fixed action and matter -> IC30 off-pin variation ->
IC31 exact radial reduction/linearization -> fixed approximate D tables ->
nonlinear BVP -> differentiated represented-field residuals and operator grids.

- Action variation: exact checks pass; pinning occurs AFTER variation.
- Coefficient variation: functions stay fixed functions of S; their jets are
  differentiated and their tables are not reconstructed from each source.
- Matter trace: the off-pin w derivative of each same-action fluid is retained.
- Initial constraints: numerical residuals pass in the tested domains. The
  multiplier residual is algebraic back-substitution, not an independent
  evolution test; its coefficient and finite value are separately recorded.
- Radial no-kernel argument: conditional on a>0 and V_L<=-epsilon everywhere,
  the stated integration-by-parts identity excludes a homogeneous kernel.
  Sampled signs and discrete spectra do NOT establish those uniform bounds.
- Physical stability, full functional Poisson brackets, exact k0 handling,
  global regularity and pin-off matching: NOT established here.
- Mathematical proofreading covered the new code and IC31 note. The wording
  was clarified before freezing inputs: action functions are not new varied
  fields. No independent referee review or Lean certificate is claimed.

## Next calculation: preserve these constraints, then cross the pin boundary

Use the actual IC30 Q Euler equation to calculate qdot on these inhomogeneous
data, rather than reuse the homogeneous qdot. Differentiate the spatial
momentum constraint to obtain the shear evolution with explicit boundary data.
Include the matter evolution: initially zero spatial fluid gradients do not
mean their time derivatives vanish under a nonuniform lapse. Preserve the
lapse and z constraints to solve their time multipliers with the same fixed
coefficient functions. Check the resulting physical metric evolution.

Then solve the mixed pinned/unpinned inner boundary problem. The diagnostic
S'(2)=0 boundary here is NOT a derived galactic boundary condition. eta=1
throughout this package; it does not test the delicate eta->0 multiplier
compatibility or the changed constraint stratum. The radial lapse profile
alone is not a prediction of galactic attraction, no-slip, or lensing.

Finally retain the full original scope: one controlled global action,
nonlinear constraint closure, healthy counted modes, PPN, causal/interaction
scales, zero-field and zero-mode control, realistic cosmology and empirical
galaxy/cluster/CMB tests. The a0–Lambda coefficient remains input. The
construction is progressing, but none of these obligations is waived.
