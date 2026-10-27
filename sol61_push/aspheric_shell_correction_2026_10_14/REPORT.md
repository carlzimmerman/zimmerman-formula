# Candidate aspheric correction for the shell-induced aberration

Parent checkpoint: 0bef1df926e480f9473d3004a625a030faa7c1e2.
An ideal quartic-plus-sextic mirror sag reduces the preceding one-sided
geometric wavefront RMS from 30.98 nm to about 3.35 pm while retaining the
same paraxial mirror curvature and assigned central waist. This resolves
neither the diffractive cavity eigenmode nor high-power manufacturing and
thermal feasibility. It supplies a concrete correction candidate for the
optical part of the hypothetical preparation apparatus.

## Surface and optimization

For mirror transverse coordinate rho, set

    z(rho)=L-R+sqrt(R^2-rho^2)
           +A4 (rho/wm)^4+A6 (rho/wm)^6,

with L=0.5 m, R=0.823214874898129 m and wm=0.005092961062765224 m.
The fitted coefficients, in metres, are

    A4=-2.720233553e-8,
    A6= 1.412126879e-10.

At rho=wm, the added sag is approximately -27.06 nm. The correction has
no quadratic term, so it preserves on-axis curvature and the preceding
ABCD map. These coefficients use the displayed normalized radius, not
unscaled powers of metres. Extrapolation beyond the traced/usable aperture
has not been validated as a manufacturable surface.

Rays are intersected with the actual modified surface by a bracketed root
solve. Reflection uses its analytic surface normal, including derivatives
of both correction terms. The whole outward and return path through the
shell is retraced for every coefficient pair; the calculation does not
simply subtract a guessed phase from the earlier result.

The optimization minimizes Gaussian-power-weighted optical-path residuals
after removal of piston and defocus, using 64 radial quadrature nodes over
0<=r<=3w0, w0=2 mm. An explicit central-difference coefficient Jacobian is
used, with 1 nm coefficient steps. The fit terminates after 14 evaluations.
96 and 192 nodes independently evaluate the fitted surface. This is a local
least-squares solution, not a claim of global optimality.

## Results

At 192 validation nodes:

    geometric wavefront RMS = 3.35264e-12 m,
    phase-only mismatch = 2.88669e-10,
    maximum sampled ray-height deviation from ABCD = 2.50 micrometres.

The last quantity occurs near the low-weight outer edge and is not a
power-weighted beam distortion. The same implementation with zero correction
reproduces the earlier 30.98 nm and 0.017859 phase-only mismatch.

Sensitivity to an error in A4, holding A6 fixed and refitting only diagnostic
piston/defocus, is

| A4 error | Wavefront RMS | Phase-only mismatch |
|---|---:|---:|
| -1 nm | 1.100 nm | 3.102e-5 |
| -0.1 nm | 0.1102 nm | 3.121e-7 |
| +0.1 nm | 0.1103 nm | 3.124e-7 |
| +1 nm | 1.105 nm | 3.131e-5 |

These are coefficient sensitivity calculations, not general surface-error
or manufacturing tolerances. Coating phase, roughness, alignment, changes to
shell radius/index and thermal deformation are different perturbations.
The tiny ideal residual is not an achieved physical optical specification.

## Scope of the correction

The preserved paraxial curvature makes the candidate compatible with the
previous central Gaussian waist at ABCD order. It does NOT prove that the
corrected cavity has that eigenmode. The rays start with a flat geometric
central wavefront; diffraction, amplitude redistribution and all coherent
interface reflections remain absent. The residual is measured after fitted
piston/defocus, and the overlap uses prescribed input Gaussian power weights.
It is not a full roundtrip loss or finesse. The measured optical-path error
on one side cannot simply be squared or doubled to obtain a cavity loss.

A symmetric implementation would use corresponding corrected mirrors at both
ends. That full cavity still needs a wave-optical mode calculation. Neither
the required 6.28 MW circulating power in each direction nor material/particle
assumptions are validated by improving geometric phase matching.

## Evidence and next task

Sixteen numerical checks pass, including paraxial limits, on-axis optical
length, endpoint-eikonal derivative checks before and after correction,
Snell continuity, unit directions and quadrature refinement. The fitted
result meets the explicitly assigned 1e-6 phase-only mismatch target in this
model. The bounded-run manifest validates the input and output hashes.
The source is a scoped adaptation of the preceding ray tracer with an
implicit aspheric mirror intersection and coefficient fit. No Lean proof
or empirical apparatus certification is claimed.

The exact spherical surfaces were an optical obstacle to simply adopting the
Gaussian assumption. An aspheric correction now addresses that obstacle in
geometric optics without changing the assumed central beam size. The next
step is a wave-optical propagation/eigenmode check that includes the corrected
surface and coherent shell interfaces. Stimulated losses, physical material
response and empirical admission of the proposed particles remain independent
open requirements. The overall creation goal remains open.
