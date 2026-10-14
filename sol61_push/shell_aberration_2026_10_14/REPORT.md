# Exact-ray check exposes a limitation of the paraxial shell cavity

Parent: a5d5d55df5bfda9016ed2912f57e55e910e3c6a8.
For the preceding 1 m cavity, exact geometric ray tracing gives a weighted
wavefront residual of 30.98 nm RMS after piston and defocus removal. The
associated phase-only Gaussian overlap is 0.982141 for a center-to-mirror-
to-center excursion through one shell side. This is an optical limitation
that must be addressed; the preceding paraxial fixed point is not a
certificate of a high-finesse Gaussian mode.

## Calculation

Start meridional rays at (r,z=0) with direction (0,1), corresponding to a
flat central input wavefront. Intersect the inner and outer spherical shell
surfaces exactly, refract by vector Snell's law, intersect the spherical
mirror, reflect specularly, traverse the shell in reverse, and return to
z=0. Accumulate each segment's optical length n times geometric distance.

Use the inherited a=2 cm, b=2.5 cm, n=1.447598098, mirror vertex z=0.5 m,
and mirror curvature radius 0.823214875 m. Its center of curvature is
z=0.5-R. No thin-shell or paraxial refraction approximation is used in the
ray propagation. Reflected interface branches, polarization and absorption
are excluded.

For a forward-pointing unit normal N, the refracted direction is

    tangent = d-(d.N)N,
    d_out=(n1/n2)tangent
          +sqrt[1-(n1/n2)^2 |tangent|^2] N.

The trace verifies that no sampled ray undergoes total internal reflection.
At the returning central plane, retain output radius r_out(r), final
transverse direction and optical length S(r). Fermat's endpoint relation

    dS/dr_out = d_out,transverse

is checked by an independent finite difference at four nonzero radii.
Small-height ray limits reproduce the preceding ABCD half-map. This checks
curvature signs, reverse propagation and optical-length accumulation.

Weight input rays by r exp(-2 r^2/w0^2) with w0=2 mm and 0<=r<=3w0.
Fit S(r) with A+B[r_out(r)/w0]^2 using weighted least squares. Subtract this
piston and defocus to obtain W(r). Define the two diagnostics

    RMS = sqrt[weighted_mean(W^2)],
    overlap = |weighted_mean(exp(2 pi i W/lambda))|^2.

The fit minimizes mean squared wavefront error; it is not a nonlinear search
for the defocus maximizing overlap. The weight is input Gaussian power,
not a solved output intensity distribution. Rays are traced geometrically
from a flat wavefront, not propagated as a diffracting Gaussian field.
These distinctions are essential to interpreting the result.

## Result and its meaning

96 and 192 radial quadrature nodes agree:

    RMS=3.09805559e-8 m = 0.0249875 wavelengths,
    phase-only overlap=0.9821409998,
    phase-only mismatch=0.0178590002.

The Gaussian power beyond 3w0 is exp(-18), about 1.52e-8; this truncation
is small for the sampled phase diagnostic but is not an aperture-loss model.
The largest sampled ray-height departure from the paraxial map is about
0.621 mm near the low-weight outer edge. It must not be represented as a
power-weighted average beam distortion.

The 1.8% diagnostic mismatch is not a measured loss or a calculated cavity
roundtrip loss. A real resonator can adopt a non-Gaussian eigenmode, and phase
can redistribute rather than remove energy. Diffraction, amplitude mapping,
coherent reflections and the other cavity half must be included to obtain
an eigenmode and its roundtrip eigenvalue. It would be incorrect to turn this
number directly into a finesse or an input-power requirement.

Nevertheless, a nominally stable ABCD solution cannot by itself justify
assuming the assigned Gaussian profile at high buildup. This result changes
the next optical task: solve the wave-optical mode or compensate the shell's
aberration, rather than treating the paraxial construction as complete.
A candidate compensation is an aspheric mirror surface chosen from the
optical-path residual, but that surface and its self-consistent mode have
not been designed here. Reducing the waist is another possible route and
would require recalculating the particle-source overlap, not reusing it.

## Verification and reproducibility

Eleven checks pass: small-ray agreement with ABCD, on-axis optical length,
four endpoint-eikonal derivative checks, quadrature refinement, Snell
transverse-momentum continuity and direction normalization. The first
preflight failed an overly strict Snell residual because computed sphere
intersection normals departed from unit length by up to 6.86e-13. Diagnostic
instrumentation linked that to the 6.27e-13 momentum residual. Normalizing
the normals explicitly before refraction/reflection fixes this numerical
implementation issue without loosening the Snell tolerance. The authoritative
run uses the corrected implementation and its manifest validates the hashes.

This is a self-reviewed geometric calculation, not a Lean-certified optics
theorem or experimental evidence for the hypothetical carriers. The creation
goal remains open. The pending optical correction is added to the existing
particle-admission, material-response, stimulated-loss and thermal obligations;
it is not evidence that the wider mechanism is impossible.
