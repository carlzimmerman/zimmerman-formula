# AZ48 I6 Bullet3D — frozen before numerical implementation

This completes the missing three-dimensional nonlinear calculation for the
inherited I6 model. It does not reopen its SPARC or force failures, restore
the retired sector, or establish a healthy action. Retired sector, adopts
nothing; kappa=1/2 FITTED; not theory closed. Both a0 footings9.3603e-11 and
1.1312e-10m/s2 are separate. No data download or old-folder edit.

## Source and scope

Use the exact six Plummer components in FA1/fa1_zeta.py, in Msun and kpc,
with every centre at z=0. Preserve the signed gas correction:

| component | M | a | x | y |
|---|---:|---:|---:|---:|
| gas1 | 2.0e14 | 565 | 190 | 90 |
| gas2 | 1.5e13 | 505 | 525 | 120 |
| gas3 | 1.5e13 | 90 | 670 | 170 |
| gas correction | -6.8e12 | 70 | 670 | 170 |
| galaxy1 | 1.196e13 | 470 | 0 | 0 |
| galaxy3 | 4.0e12 | 245 | 820 | 220 |

rho_j=3 M_j/(4 pi a_j^3)*(1+|r-r_j|^2/a_j^2)^(-5/2).
First prove/check positivity of the combined source, including the signed
pair, and verify its mass normalization. Do not delete a component or clip
the density. These masses, scales and positions are the inherited
phenomenological source prescription, not a new native reconstruction of
the observed Bullet. The result must keep that conditional scope visible.

Evaluate the field at BCG1=(0,0,0), BCG3=(820,220,0), main gas=(190,90,0)
and bullet gas=(670,170,0). Also report area-averaged selector and on-fraction
in100kpc discs in the z=0 plane around each point, as numerical diagnostics.
No claim to reconstruct the observed lensing map or determine dust motion.

## Physical equation and normalization

Solve the single combined-source equation, never superpose nonlinear
single-source fields:

    lap(pi)+k[(lap(pi))^2-pi_ij*pi_ij]=8*pi*G*rho,
    k=c^2/(3*a0^2).

Use I6's declared constants G=6.674e-11 SI, Msun=1.989e30kg,
kpc=3.0857e19m and c=299792458m/s. Let L0=1000kpc and choose the arbitrary
unit density rho_ref=1e5Msun/kpc^3. With x=L0*q and
pi=L0^2*sqrt(8*pi*G*rho_ref/k)*phi,

    epsilon*lap(phi)+(lap(phi))^2-H_ij*H_ij=S,
    epsilon=1/sqrt(8*pi*G*rho_ref*k), S=rho/rho_ref.

Keep this physical epsilon per footing; do not replace it by a regulator
and claim an exact physical solution. A larger-epsilon homotopy may
initialize the solve but the final residual uses physical epsilon. Allowed
homotopy multipliers are100,10,1, fixed before results. The selector is
s=3*sqrt(3)*det(H)/(tr(H^2))^(3/2), zero only at a zero Hessian; report any
sample where the Hessian norm is too small for a stable numerical ratio.
Changing rho_ref by4 must scale phi and epsilon by1/2 and leave physical
pi and s unchanged. This unit choice is not a fitted physical parameter.

## Domain, branch and solver bounds

Use a full3D Cartesian box centred on the signed source's mass centroid.
Each axis has N intervals and mapping x=x_c+L*sinh(3u)/sinh(3), u in[-1,1].
Primary half-width L=4000kpc; ladder N=64,128,256. The128/256 pair determines
numerical eligibility. The64 rung is a diagnostic, not an alternate grade.
Use centred second-order derivatives, including mixed Hessian components.
No axisymmetric approximation is eligible for the Bullet source.

Boundary and initial values come from a declared spherical approximation,
not superposition of potentials: replace each source centre by the box
centre, preserve its M and a, sum its analytic enclosed mass, and solve
epsilon*r^2*phi'+2*r*(phi')^2=Q(r) on the positive branch, where
Q=M_spherical(<L0*r)/(4*pi*rho_ref*L0^3). Rationalize the quadratic root
to avoid cancellation. Integrate that derivative to obtain boundary phi;
an arbitrary additive constant is immaterial. Compare4096/8192 logarithmic
radial quadrature points from1e-6 to1.1 times the dimensionless box diagonal:
boundary potential differences relative to its centre-to-corner amplitude
must be<=1e-6. Use the finer table for production.

Repeat the N256 solve at L=8000kpc, choosing the mapping alpha by the unique
positive solution of L*alpha/sinh(alpha)=4000*3/sinh(3), so the central
physical spacing stays fixed. This is the boundary/domain error check.
No changed source parameters. Newton updates use the exact linearization
epsilon*lap(dphi)+2*tr(H)*lap(dphi)-2*H_ij*dphi_ij.
Use a matrix-free linear solve, with at most400 matrix-vector applications
per Newton update and60 Newton updates per homotopy level. A line search
must reduce the residual and retain positive principal-matrix eigenvalues
epsilon*I+2*(tr(H)*I-H). Never accept a non-elliptic step merely because
its residual is smaller. A bound reached without convergence is UNDECIDED,
not a fitted solution. Checkpoint every accepted Newton step.

## Numerical gates, known answers and mutation

At an accepted final field require max|residual|/max(1,max|S|)<=1e-8,
finite fields and positive principal-matrix eigenvalues on every interior
cell. Record minimum eigenvalue and residual histories. Graded point s must
change<=0.02 between128/256, and between primary/expanded boxes; disc-average
s and disc on-fractions must change<=0.03. All conditional threshold flags
must agree. Disc quadratures use32/64 radial and64/128 angular samples with
area weights; changes<=0.01 and same flags. Failed lines mean UNDECIDED.
These selector-resolution lines retain I6's0.02/0.03 accuracy scale; they
are numerical eligibility tolerances, not observational error bars.

Known answers before production:
- A constant quadratic potential reproduces the discrete full3D Hessian,
  nonlinear residual and analytic principal matrix to1e-10 relative; include
  a rotated Hessian with mixed terms. A uniform positive isotropic Hessian
  gives s=1, planar and rank-two Hessians give s=0, and the deep point-source
  eigenvalue ratio(-1/2,1,1) gives s=-0.769800358919501 to1e-12.
- A centred Plummer source has an independent spherical positive-root
  solution. Solve it in3D at32/64/128 and physical epsilon on both footings.
  Compare selector s at r/a=0.3,0.5,1,2,5 along axes and diagonals: finest
  absolute error<=0.02,64/128 change<=0.02, same threshold flags, and final
  residual/ellipticity gates above. Do not reuse the3D solver as the oracle.
- Check analytic Jacobian products against independent centred differences
  of the nonlinear residual on a small grid, relative error<=1e-8.
- Source parsing, Plummer mass integral and normalization rescaling checks
  must pass before any Bullet physical grade. Scalar algebra checks use
 1e-12 relative; mass quadrature uses paired tolerances1e-6.

MUTATE uses s->-s on independently written output, preserving the same
converged field. It must fail the isotropic positive-Hessian known answer;
report whether it also changes Bullet conditional classifications, without
requiring the source to have a particular unobserved response. Do not change
a threshold to make a physical flag flip.

## Reporting and execution

Primary output is the3D field's point/disc selectors and numerical status.
Report the threshold interval allowing both BCG points, s_c<=min(s_BCG1,
s_BCG3), and intervals producing gas-on/galaxy-off in each subcluster.
These intervals are derived diagnostics, not a search for a new selector.
Also compare with the old I6 per-footing s_c as an explicitly inherited,
data-calibrated threshold; do not represent that threshold as derived from
the action or newly authenticated native data. WEIGHT ALLOWED AT GALAXIES,
WRONG SIGN or NO SIGN is conditional on that inherited threshold and source.
Numerical failure overrides these readings with UNDECIDED. Even a stable
field reading is not an observational lensing PASS or a healthy-action result.

All production and convergence solves require heavyq after light work.
Only bounded N<=16 implementation pilots may run unqueued. Use one thread,
atomic outputs, flag-only SIGTERM handlers, safe-step checkpoint/exit75,
source/criteria identities and idempotent --resume. Test an actual live
interrupt/resume against uninterrupted output on a small pilot before queue
submission; scientific output must be byte-identical. Measure the pilot's
physical footprint and conservatively scale the queue estimate. Do not
declare pending jobs complete. Raw field arrays may remain reproducible
runtime artifacts with committed hashes; commit compact evidence and labels.
