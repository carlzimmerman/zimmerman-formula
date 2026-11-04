# Cassini: full generalized-action response

All six tested physical lengths pass the inherited Cassini quadrupole cut
on both frozen acceleration footings. The calculation includes **both**
div A and -double_div B from the action. The Hessian-dependent B term
dominates the resulting quadrupole; omitting it would give a substantially
incorrect prediction.

| Universal length (kpc) | Canonical | Alternate |
|---:|---:|---:|
| 0.03 | 0.00372940884 | 0.00425233111 |
| 0.1 | 0.00111883524 | 0.00127571363 |
| 0.3 | 0.000372945892 | 0.000425238799 |
| 1 | 0.000111883826 | 0.000127571706 |
| 3 | 0.0000372946124 | 0.0000425239063 |
| 10 | 0.0000111883840 | 0.0000127571722 |

Entries are abs(Q2)/(5.2e-27 s^-2). The signed quadrupole is negative in
every listed case. At 3 kpc it is -1.93931985e-31 s^-2 canonical and
-2.21124313e-31 s^-2 alternate. These are finite, converged numerical
values for the stated constant-external-field diagnostic, not a uniform
theorem over every length, a full ephemeris fit, or a transferred KT36 bound.

## Exact law and full variation

The parent PLAN specifies the known generalized-QUMOND action with
P=xQ(z)/z, x=|grad psi|^2/a0^2, and
z=x+ell^2||Hess psi||_F^2/a0^2. Here psi is the ordinary unfiltered Newtonian
potential. Q'=simple nu(sqrt z) and Q(0)=0. There is no Gaussian outer
filter; a Gaussian Solar source is used only as an explicit point-source
regularization check.

DERIVATION.md gives the angular Green integrals, differential-source
comparison, origin contacts, and normalization. With C=R-1+xR',
D=lambda^2 xR', and lambda=ell/rM, the point-field integrals are

```
q_A=(3/2) integral b/r d(log r),
q_B=-18 integral d/r^5 d(log r),
Q2_signed=(3/2)(a0/rM)(q_A+q_B).
```

The angular moments b and d are defined there. At canonical ell=3 kpc,
q_A=-3.74293e-14 and q_B=-1.644883105e-6. Their total is
-1.644883143e-6. The B term is a mandatory variation of the Hessian
dependence, rather than a numerical correction that can be discarded.

The parent independently reconstructed the sign and coefficient of q_B
and both finite-core contact terms. REGULARIZATION_PROOF.md additionally
establishes the Gaussian-source limit for fixed eta>0 and lambda>0, using
uniform small-core bounds and dominated convergence outside the core.
It makes no assertion about every possible regulator or a simultaneous
lambda-to-zero limit.

## Controls and numerical evidence

`run_002/manifest.json` completed in 12.02 seconds and validates against
unchanged input hashes. The main checks include:

- Ell=0 reproduces the inherited plain QUMOND Green result to the stated
  1e-9 absolute-q tolerance, using identical nodes and domain. The signed
  controls are -0.3476007075 canonical and -0.3006614873 alternate.
- A finite Gaussian source at ell=0 reproduces the inherited corrected
  source-only result, including its nonzero origin contact.
- Q=z gives exactly zero anomalous quadrupole. Eta=0 likewise gives zero
  STF quadrupole.
- Base integrations use 8,000 radial by 160 angular nodes. Fine integrations
  use 16,000 by 320 and expand the domain from [1e-8,1e6] to [1e-10,1e7]
  in rM units. The largest relative change among the twelve nonzero-length
  point calculations is 2.843e-10.
- Analytically differentiated angular moments independently form the full
  differential source div A-double_div B. Its density integral agrees with
  the Green formula within 4.736e-16 absolute q, or 9.60e-10 relative in
  the smallest result. This is a differential identity check, not an
  independent three-dimensional field solver.
- At ell=.03 kpc, source widths sigma=.5,.1,.01,.001,5e-7 rM are evaluated
  with both origin contacts. The three smallest widths agree with the point
  result within 3.67e-13 relative. The larger .5 core differs by 3.64e-4
  canonical and 2.19e-4 alternate, as a resolved finite-source effect.

The fixed Newtonian Solar term remains excluded from the anomaly, and all
original Solar constants, external field, acceleration footings, and the
5.2e-27 s^-2 ceiling remain unchanged.

## Preserved numerical failure and correction

The first run (`run_001/`) deliberately remains recorded as failed. Its
point-source, zero-length, Newtonian, and tiny-core checks passed, but the
differential-density comparison failed for broad Gaussian cores sigma=.5
and .1 when their inner radius was forced down to 1e-10 rM. At such tiny
r/sigma, angular roundoff in a nominal O(r^2) tensor moment is amplified by
r^-2 in the boundary/density expression. An apparent inner B surface of
order unity contradicted its analytic contact of order 1e-9; this identified
the numerical cancellation rather than a physical origin contribution.

The unchanged quadrupole implementation was then tested at inner radii
sigma times .001, .0005, and .00025. The analytic origin contacts remain
included. `core_debug_001/` completed: density discrepancies were at most
3.02e-14 q, and changing those radii moved q by at most 1.05e-15. The broad
core issue therefore received a resolved-core convergence test, rather than
a relaxed acceptance threshold or removal of the failed control.

The final wrapper uses rmin=max(1e-10,.001 sigma) for positive-width core
checks. It preserves `calculate.py`, the first failed run, and the successful
core diagnostic unchanged. `calculate_v2.py` changes the run prescription
and adds the explicitly authorized 3 and 10 kpc points. All original
accuracy gates remain enforced. Both the core diagnostic and final manifest
validate against their pinned inputs.

## Scope and reproduction

The specified external field is constant and has zero Newtonian Hessian.
A real Galactic background supplies derivatives too; evaluating that
embedding and its tracking-data conventions remains separate. There is no
claim here of relativistic health, lensing viability, a dwarf pass, or a
general exclusion/acceptance of all generalized-QUMOND actions.

To repeat the complete calculation from the repository root, choose a fresh
run directory and invoke the installed computation-audit runner with
`contract_v2.json`, its exact `execution_artifacts` list, a declared
`results.json` below the new directory, and `calculate_v2.py --output` that
same result path. The original argv arrays, 300-second wall and 280-second
CPU caps, one numerical thread, 1 MiB log cap, software versions, and input
and output hashes are retained in each manifest. No randomness is used.

This new prose and the displayed derivations received mathematical
self-proofreading. Source artifacts from KT33 and the shared analytic law
were read and hash-pinned, not edited by this lane.
