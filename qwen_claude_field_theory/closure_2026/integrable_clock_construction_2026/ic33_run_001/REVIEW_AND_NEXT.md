# IC33 terminal review and next calculation

Base: 42716b2a63d10f8bcdd5bbbd4c7c49647bedbd73.
Full theory **OPEN**. Self-review, not independent review or formal certification.

## Important correction

IC32's nonzero-tail time tangents obeyed the tested constraints but not the
independent tracefree spatial-metric evolution equation. At r=2 its selected
shdot=0 disagrees with the action's -1.872218775243549 for amplitude 1 and
-3.791723047519155 for amplitude 2 (model units). The homogeneous zero-tail
control agrees to about 1.7e-14.

This does not invalidate the existence of the IC31 constrained initial slice or
the narrower IC32 constraint-tangency result. It rules out promoting that particular
boundary choice to a solution of all metric evolution equations. No construction
or adverse evidence was deleted.

## Structural reason and constructive resolution

On the initial Q'=q'=sigma'=0 slice, two shear rates preserving the same momentum
constraint differ by delta satisfying delta'+3 delta/r=0. Multiplication by r^3
gives (r^3 delta)'=0, so a connected exterior r>0 leaves delta=C/r^3.
Constraint preservation alone cannot choose C.

Varying independent radial and angular metrics determines the missing rate.
The same action therefore fixes the inner integration datum. The corrected
momentum integral carries that datum through the exterior; lapse, z, ell and
shift preservation are then solved again without changing the coefficient
function or fitting any source.

For clarity, section 1 of IC33_FULL_METRIC_EVOLUTION.md displays the gravitational
radial density. For each ordinary fluid the total first-order action additionally
contains Pi sigma_dot - beta Pi sigma' - J H(Pi/J,exp(-2a) sigma'^2).
Its independently varied metric stresses are given in that document's section 3.

## Executed checks and actual outcomes

| Job | Child exit | Runner exit | Wall seconds | Result |
|---|---:|---:|---:|---|
| tests | 0 | 0 | 255.525855 | 410 tests; unittest elapsed 254.931 seconds |
| metric | 2 | 1 | 54.171692 | Nine scoped checks true; strict mode retains full-theory OPEN |

Both manifests validate with exit 0 using the repository root. All pinned inputs
and recorded output hashes match. This is provenance validation, not physics
certification. Exact child and bounded-runner commands are in run_index.json.
Caps: 420 seconds wall, 2 MiB logs, one cooperative numerical-library thread;
no hard memory/affinity limit. Both jobs are terminal.

Seven symbolic checks include the explicit action boundary relation, trace and
tracefree Euler equations, matter variation, and independently constructed Ricci
curvature. The simplified trace equation uses the shear-gauge constraint:
without that stated hypothesis the residual is
-2 sh(beta'-beta/r+t sh), not zero. The development test caught this.

| Repaired case | Representation nodes | BVP nodes | Maximum full shear Euler defect | Maximum lapse-preservation defect |
|---|---:|---:|---:|---:|
| amplitude 1 | 3201 | 3532 | 9.160284086817683e-9 | 2.3947066551954777e-11 |
| amplitude 2 | 3201 | 3903 | 4.8540603092561696e-8 | 2.474642712968489e-11 |
| amplitude 2 refined | 6401 | 6859 | 3.1294522528924062e-9 | 2.12825312928544e-11 |

These are maxima over the stated nodes/midpoints, not continuum enclosures.
The amplitude-1 1601-node control missed the 1e-7 shear tolerance:
1.3735771631218086e-7. It remains in the output, and the threshold was not relaxed.
Both tested refinements reduced the full-shear defect by more than a factor of 8.

All selected finite-kick constraint-error ratios exceed 3.2 at BOTH successive
halvings; they are near 4. For amplitude 2 at 6401 nodes, the lapse errors at
dt=.001,.0005,.00025 are 3.442541021457681e-5, 8.608073244684279e-6,
2.151973801902408e-6. These absolute errors are not the much smaller
first-preservation residuals. No gravitational constraints were re-solved
after the kicks. Generated fluid gradients enter the same full Legendre map.

Development runs also retained these meaningful failures before correction:
missing module/function tests; the unstated shear-gauge hypothesis in the trace
comparison; and the coarse-grid 1e-7 tolerance miss. The final scientific run
reproduces both the old boundary mismatch and the repaired coarse-grid control.

## Strongest defensible result

The active-pin spherical action now has independently derived trace AND
tracefree metric evolution equations with general radial metric/momentum jets
and varied matter stress. Using the tracefree equation to fix the previously
free shear-rate datum yields a numerically checked first-order tangent in the
selected exterior examples. This repairs evolution data within the same
candidate, rather than replacing the exponential law or designing another fit.

No many-step spacetime, full functional Dirac algebra, homogeneous/zero-field
stratum closure, pin-off matching, general health/causality, PPN, empirical
galaxy/cluster/CMB prediction, or priority claim follows from these tests.
Lean/lake were not found on PATH; no formal certificate exists.

## Next unavoidable calculation

Use the general trace and tracefree equations together with the generated
matter momentum/stress to evolve genuinely inhomogeneous data over many time
steps. Derive full matter canonical transport and auxiliary preservation on
those general slices; do not reuse the initial simplifications. Check both
metric evolution residuals as well as all constraints and boundary fluxes.
Then construct the active-pin to unpinned MOND connection with physical
matching data. The remaining original full-theory requirements stay intact.

Mathbox computation-audit controlled the finite-evidence contract and provenance;
proof-audit exposed the gap between constraint tangency and the missing equation.
Proofreading self-review covered the new document and equations: no additional
mathematical-token edits; the gravitational-versus-total density scope is
clarified above. No third-party independent review was performed.
