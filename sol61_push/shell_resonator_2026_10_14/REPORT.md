# Paraxial optical cavity through the proposed silica shell

Parent: cb832d22917df2515ae708ebad4b2ff2d6152f1c.
A stable scalar paraxial mode can have the previously prescribed 2 mm central
waist while traversing the curved shell. This supplies a missing geometrical
condition. It does not establish high-power feasibility, a complete Maxwell
solution, or the hypothetical particle physics.

## Construct the Gaussian mode

Use inner shell radius a=2 cm, outer radius b=2.5 cm, silica index
n=1.447598098 and vacuum wavelength 1.239841984 micrometres, inherited from
the silica material package. The central vacuum waist w0=2 mm has
zR=pi w0^2/lambda=10.13546 m. Start q0=i zR.

In physical ray coordinates (height, angle), propagation and refraction are

    P(d)=[[1,d],[0,1]],
    S(n1,n2,R)=[[1,0],[(n1-n2)/(n2 R),n1/n2]],
    q'=(Aq+B)/(Cq+D).

For motion from the center toward the right mirror, both shell surface
curvature radii are negative: their centers of curvature lie behind the
surface. The shell matrix is

    S(n,1,-b) P(b-a) S(1,n,-a)
      = [[1.07730013,0.00345400],[3.09200529,0.93815989]].

Its nonzero focusing element shows why free-space cavity parameters cannot
simply be reused. The half-cavity matrix to a mirror at distance d is
M=P(d-b) shell P(a). At that mirror, choose curvature radius
Rmirror=1/Re(1/qmirror) to match the Gaussian wavefront. Reflection has matrix
[[1,0],[-2/Rmirror,1]]. The reverse optical path has matrix [[D,B],[C,A]],
because the full forward path begins and ends in vacuum with determinant one.
The roundtrip fixed point is checked directly and by solving its quadratic.

| Full cavity length | Mirror curvature radius | Mirror beam radius | Clear mirror radius for 1 ppm Gaussian clipping |
|---|---:|---:|---:|
| 0.2 m | 0.423337 m | 2.61848 mm | 6.88204 mm |
| 0.5 m | 0.573271 m | 3.54635 mm | 9.32072 mm |
| 1.0 m | 0.823215 m | 5.09296 mm | 13.3856 mm |

The last column follows exp(-2 aperture^2/w^2)=1e-6 for a centered ideal
Gaussian beam, not a complete diffraction/alignment loss budget. The beam
radius at the inner surface is 2.000004 mm and at the outer surface 2.154606 mm.
Inside the vacuum sphere, on-axis intensity varies only 3.89e-6 fractionally
between waist and inner surface. Reciprocal counterpropagating modes can
therefore approximate the spatial pump profile previously assigned inside
the cavity, at scalar paraxial order.

The 1 m design's half roundtrip trace is 0.996999, within the stable range
but near its edge. With geometry and index fixed and both mirror radii varied
together, the upper curvature stability boundary is 0.8234147 m, only
0.00019984 m above the chosen radius. This is a parameter-space margin,
not a manufacturing tolerance or a bound on thermal lensing. Waist accuracy
can require tighter control than mere stability. Other lengths are similarly
near a boundary.

## Power and interfaces remain serious requirements

The assigned peak intensity requires

    Pwave=Ipeak pi w0^2/2=6.28319 MW

in EACH traveling wave at the center. This is circulating power, not an
asserted achievable buildup or an external laser specification.

At normal incidence the inherited uncoated Fresnel reflectance is 0.0334423
per interface. If every reflected branch is discarded, the direct intensity
transmission through all four interfaces in one traversal is
T4=(1-R)^4=0.872793; eight encounters per roundtrip give a rejected fraction
1-T4^2=0.238233. Those are bookkeeping diagnostics, not absorption.

For a single optimally coupled input and an otherwise lossless end mirror,
maintaining 6.283 MW in the forward wave at the CENTER would require about
1.602 MW input in this discarded-branch model. The reference-plane factor
1/(1-R)^2 is included between the input mirror and center. The reverse
center wave would be weaker; this single-input calculation does not maintain
the equal counterpropagating intensities assumed in pair preparation.

If both center waves instead have equal power P, the same discarded-branch
energy balance is 2P[1-T4]/(1-R)^2, about 1.71 MW removed from the main
optical branches. Balanced coherent inputs would require a separate coupling
solution. These numbers are not universal lower bounds: reflected light can
interfere and recouple, and antireflection coatings change the result.
Conversely real absorption, scatter, and mirror losses add requirements.
A multi-interface coherent transfer calculation is needed before specifying
input power. No coating or thermal performance has been assumed measured.

## Evidence and remaining physics

Twelve bounded checks cover determinant conservation, physical beam-radius
continuity at each refractive interface, and roundtrip fixed points by two
methods. The command, parameters, input hashes and output hashes validate in
the run manifest. This is an analytic/numerical self-review, not a new Lean
certificate or an experimental demonstration.

The calculation uses standard scalar Gaussian ray-transfer propagation,
consistent with the paraxial formalism already checked in the earlier
paraxial_optical_source package. The refractive-index evidence remains in
the silica_shell_retention report. No new measured optical properties are
introduced here.

Spherical aberration is not bounded merely because a paraxial fixed point
exists. The inner-surface ratio w/a=0.1 also makes an aberration calculation
worth doing before adopting this large-waist solution. Coating phase, finite
apertures, coherent shell reflections, vector-field corrections and thermal
deformation remain missing. The source inside the shell material is still
omitted from the particle preparation calculation. These gaps prevent calling
this a full optical creation apparatus.

This advances the cavity-geometry obligation: the shell does not prevent a
Gaussian mode at leading paraxial order. The next discriminating optical
check is aberration of the concentric shell at the assigned beam waist,
followed by coherent interface losses. The broader goal remains open, including
particle admissibility, complete material response, and stimulated losses.
