# FGF-019 finite SZ pressure-gradient identifiability

Setup started 2026-09-27T20:29:05Z, Astra agent /root/catalogue_audit.
The physical task is open; no detector covariance or pressure-gradient
measurement is assumed. This is one explicitly finite spherical pressure
model using the actual cached map, mask and beam.

## Projection and target

For electron pressure Pe, y(theta)=C integral Pe(sqrt(R²+l²)) dl,
C=sigma_T/(m_e c²), R=DA theta. Fix target Rt=1252 kpc for ZW1215 and define
x=r/Rt and dimensionless pressure p(x)=C Rt Pe(Rt x). Then
 y(t)=2 integral_t^5 p(x) x/sqrt(x²-t²) dx, t=theta/theta_t.
Thus dp/dx/(C Rt²) is the physical electron-pressure derivative. Total
thermal pressure requires composition/electron-to-total conversion. The
electron pressure inference is not independently a gravitational-force test.

Use continuous piecewise-linear pressure through the nodes
 0,.18,.36,.54,.72,.90,1.10,1.28,1.46,1.64,1.82,2,2.5,3,4,5.
The pressure at 5 is fixed to zero; the other 15 nodal amplitudes are free.
The target is the exact derivative on (.90,1.10):
 g=(p(1.10)-p(.90))/.20.
In this finite model it is constant on that interval and defined at x=1;
it is not the derivative of a piecewise-constant shell or at a pressure knot.

For one radial segment p=A+B x between a and b, Abel projection is obtained
from primitive terms J0(s,t)=sqrt(s²-t²) and
 J1(s,t)=[s sqrt(s²-t²)+t² asinh(sqrt(s²-t²)/t)]/2.
At t=0 use J1=s²/2. Integrate 2[A Delta J0+B Delta J1], from max(a,t) to b,
only for t<b. This provides an analytic shell projection, avoiding a fit to
an assumed universal pressure law.

## Explicit observation operator

Adopt DA from flat matter/vacuum distance with H0=70 km/s/Mpc, Omega_m=.315,
Omega_Lambda=.685 and X-COP z=.0766. This is an added fiducial conversion,
not authenticated catalog cosmology. Actual positions and masks come from the
pinned catalogs/FITS. Report the resulting angular aperture and physical
support separately; redshift agreement does not authenticate distance.

Use twelve equal-width angular annuli between 0 and 2 theta_t. For each,
retain finite map pixels with mask>0 and calculate a mask-weighted mean.
Record all pixel counts, unweighted usable fractions, mask means, mask minima/
maxima and weighted y sums; center coverage alone is insufficient. Inspect
further annuli 2–3,3–4,4–5 theta_t as coverage diagnostics. Repeat coverage for
A644, whose center is masked, without silently promoting it to a usable target.
No annular scatter or map-pixel count is interpreted as independent noise.

Build A by projecting each pressure basis onto the actual local pixel centers,
applying the cached isotropic harmonic beam through an explicit tangent-plane
FFT, and then applying exactly the same masks and bin weights. The finite
flat-sky pixel model uses the local CAR longitude spacing times cos(dec) and
latitude spacing, a 512-square source patch zero-padded to 1024 before FFT,
and T(ell)=cached b_ell for ell<=17000, zero above. The cutoff is conditional
on the local PROVENANCE.md description, not an authenticated full response.
Spherical angular separations set projection radii; FFT convolution is a local
flat-sky approximation. Radial pressure vanishes outside 5 Rt; no hidden outer
profile is extrapolated. Include an additive constant map-background mode.

The finite binned observation vector is d=A p+b 1: 12 rows and 16 columns.
It is a deliberate annular compression, not all available map pixels. A
null mode for this model is not automatically a null mode of the full map,
finer bins, other support choices or a coupled X-ray/SZ response.

## Decisive identifiability test and controls

Write inner columns as the first twelve pressure nodes (through x=2), and
nuisance columns as the outer nodes 2.5,3,4 plus constant background. If the
12x12 inner matrix is nonsingular, fixing all nuisance amplitudes makes the
finite derivative identifiable, with exact noiseless synthetic recovery.
When nuisance modes are free, each column a_j generates v_j with inner part
 -A_inner^(-1) a_j and nuisance unit coordinate j. Thus A v_j=0. If the target
functional L v_j is nonzero for any j, g is not identifiable from these bins.
SVD singular values and row-space target residual supply an independent
linear-algebra diagnostic. Numerical tolerance is relative to matrix/vector
norms, not a claim of statistical significance.

Choose a positive decreasing synthetic baseline p_i=1e-5 exp(-x_i), final
node zero. Normalize one gradient-changing null vector and choose a finite
step small enough that both p_plus and p_minus remain positive at every free
node and decreasing to the fixed outer boundary. Verify identical model bins
and distinct gradients. This is a synthetic pressure witness on the measured
geometry, not a fit of the actual map. It is sufficient to disprove global
identifiability on this admissible finite pressure family. The actual map bins
remain descriptive observations without a resolved pressure estimate.

Controls: analytic constant-sphere line-of-sight chord; constant-background
preservation; exact same masking of data and basis; full-annulus coverage;
rank and synthetic recovery when outer/background parameters are frozen;
positive monotone null witnesses when released. Failure of the closed model
rank or coverage gate is reported, not hidden. No large grid or model sweep.

## Gravity and bounds

The user's scale remains a=kappa c sqrt(G rho_Lambda), kappa adopted, with
both a0=9.3619e-11 and 1.1279e-10 m/s². Constant-vacuum history and separate
H history a=a0 sqrt[.315(1+z)^3+.685] remain distinct. Q=sqrt(B²+aB),
R=B/[1-exp(-sqrt(B/a))], and registered M remain distinct. This task computes
no gravitational force or missing mass: its projection identifiability
statement is independent of all those choices. A later force test would
require density/composition plus an identifiable independent pressure gradient
for each branch; none is fabricated here.

Float64, deterministic finite matrices and map reductions, no random sampling.
Each process: <=120 s wall, 110 s CPU, cooperative one-library-thread cap,
1 MiB logs. No memory/affinity limit claimed. Source hashes precede execution;
actual HEAD is execution provenance and is distinct from scientific parentage.
