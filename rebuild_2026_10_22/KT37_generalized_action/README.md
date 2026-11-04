# KT37: curvature action with a two-check witness and a dwarf deficit

The fully varied generalized-QUMOND response has **22 canonical and 50
alternate Milky Way four-cut passes at ell=3 kpc** on the production grid.
The strongest selected witnesses survive refinement through level 5 and
inner/outer-domain changes. The same law passes Cassini. It retains **12/24
isolated dwarf virial-screen passes on each footing**, versus 19/24 for
plain QUMOND. Both MW witnesses fail the separate strict vertical scale-length
cut. This is a two-check candidate, not a broadly validated gravity theory.

## Specified action and accepted results

This is the construction in [Milgrom 2023, Eq.16](https://arxiv.org/html/2305.01589v2),
with the original simple nu, Q(0)=0, unfiltered Newtonian potential psi,
and one physical length ell shared by all matter:

    x=|grad psi|^2/a0^2, s=ell^2 ||Hess psi||_F^2/a0^2,
    z=x+s, P=x Q(z)/z, Q'(z)=nu_simple(sqrt(z)), R=Q/z.
    A=[R-1+xR'] grad psi, B=ell^2 xR' Hess psi,
    Delta Phi_ph=div A-double_div B.

The Hessian term is mandatory and dominates the Solar quadrupole here.
The framework is known; empirical success and a healthy relativistic
completion do not follow from that source.
[Full variation and limits](analytic/DERIVATION.md)

The accepted MW scan contains all original 1,375 cells per footing at
ell=.03,.1,.3,1,3,10 kpc: 16,500 evaluations. Only the sampled 3 kpc length
has four-cut passes. At refinement 5:

| Observable | Canonical, cell 1317 | Alternate, cell 1206 |
|---|---:|---:|
| Local speed (km/s) | 225.98697 | 227.60603 |
| Local vertical force equivalent (Msun/pc^2) | 69.77896 | 69.86582 |
| Vertical chi-squared | 51.34899 | 53.67615 |
| Rotation chi-squared | 36.79297 | 22.21636 |
| Vertical scale length (kpc) | 3.37421 | 3.39970 |

The first four meet the original primary cuts; both scale lengths exceed
the separate strict 3.02 kpc ceiling. Selected refinement is not an exhaustive
fine-grid population count or a continuum-length scan.

**The first angular implementation's empirical grades are withdrawn.** A
spherical covariance test found an artificial polar force. The corrected
factored finite-volume Hessian preserves weighted angular symmetry and radial
stress cancellation. Fresh controls precede the accepted `full_002` and
`refine_002`; no old grade transfers. The alternate count changed from the
withdrawn 51 to 50. The half-domain axial-linear manufactured scalar is
inadmissible; its separate full-sphere control passes. Pointwise quadratic
Hessian convergence at the first/last radial rows is not claimed, although
moving both boundaries changes the selected observables very little.

[MW report](mw/README.md) · [Accepted scan](mw/full_002/results.json) ·
[Accepted refinements](mw/refine_002/results.json)

All six lengths pass the frozen constant-external-field Cassini calculation
on both footings. At 3 kpc, ceiling ratios are **3.72946e-5 canonical** and
**4.25239e-5 alternate**. Both full-response terms, origin contacts, surfaces,
independent density/flux forms and refinement are included. The point source
is a specified Gaussian shrink limit with independent proof review, not an
assertion that a nonlinear function acts on a distributional Hessian. The
failed broad-core cancellation run remains preserved; a tested core-scaled
inner cutoff resolves it without relaxing the accuracy criterion.

[Solar results](cassini/README.md) ·
[Point-limit proof](cassini/REGULARIZATION_PROOF.md) ·
[Independent limit review](analytic/GAUSSIAN_LIMIT_REVIEW.md)

## Dwarf and static-response limitations

At ell=.03,.1,.3,1,3,10 kpc the canonical/alternate isolated dwarf counts are
19/19, 19/19, 16/18, 13/13, 12/12 and 5/7. The original sample, Plummer
baryons, 41 Upsilon values in [1,3] and dispersion cuts are retained. Three
independent virial representations and refinements agree. At 3 kpc Fornax
and Leo I retain narrow sampled passes, while Sculptor fails on both
footings. Seven plain-model passes are lost. These are isolated virial
diagnostics, not full satellite external-field or equilibrium grades.
[Dwarf results](dwarfs/README.md)

The static uniform-background transfer is

    delta Phi_hat/delta psi_hat
      =nu(eta)+eta nu'(eta) cos^2(alpha)
       -[R(eta^2)-nu(eta)](k ell)^2.

The final coefficient is negative. In the prescribed Solar external-field
footings its sign change occurs at wavelengths about 2.34--2.74 times ell.
This establishes a short-wavelength repulsive linear density contribution,
not a ghost or dynamical-instability proof. Matter dynamics, finite amplitude
and coarse-graining require separate analysis.
[Independent static-response audit](analytic/LINEAR_RESPONSE.md)

## Continuing experiment

KT38 tests P=xR(x+s^2) to suppress curvature corrections in weak-amplitude
fields and remove this extra linear term around a nonzero uniform background.
It is a new phenomenological choice, not an established solution. All KT37
inputs and failed or withdrawn evidence remain preserved. No baryon or cut
change was used in this phase.
