# Route C bounded result and reproducibility

The changed kernel mu=1-1/sqrt(1+2x) supplies a sufficient K_lock>=1 theorem
for every x when 0<=eta<=50/81. The constrained two-field kinetic matrix is
positive at every angle in the explicitly truncated frozen leading-derivative
PN block. This preserves a^2=xi G rho_DE on aligned homogeneous FRW while
avoiding the particular CT14 simple-kernel kinetic failure on the declared
background class. It is partial progress, not a completed theory or a data fit.

## Exact result versus finite corroboration

THEORY_CHECKPOINT.md gives the action, Legendre representation, exact ratio
minimum, conditional fast-tail obstruction, general power-tail tradeoff and
remaining assumptions. The sufficient 50/81 inequality is not a sharp bound
on K_lock>0 at finite epsilon. Local eta is not automatically its cosmological
value. E=X+V is the scalar rest energy on the timelike branch; the density
identification is exact on aligned homogeneous FRW, not arbitrary T_nn.

Run 003 performs exact SymPy differentiation before 1080 deterministic matrix
fixtures at 80 decimal digits. The inputs span x=.001 through 1e22, five eta
values through 50/81, parallel/45-degree/transverse propagation, gamma=0 or1000,
k=100 or1e6, and the canonical lapse/phi_dot mixing omitted or included.
Every raw constraint matrix is negative definite, every reduced 2x2 kinetic
matrix positive definite, and minimum sampled K_lock=1. The independent explicit
Schur formula agrees with direct inversion to relative error below4.76e-72.
The maximum raw relative anti-Hermitian defect is1.78e-82; this is checked below
1e-60 before projecting floating roundoff onto the exact Hermitian identity.
This projection is numerical bookkeeping, not a remedy for a physical sign.

Known-failure controls:
- Old simple kernel: x108.9, eta.05 gives K_lock=-.9226988 while the incorrect
  scalar-only K_free=+1.9730194. The check is sensitive to the missing mixing.
- Exponential tail: x2 gives negative unscreened clock curvature -.1192029.
- New slow kernel outside the sufficient class: eta2/3 at x1e6 gives
  K_lock=-1.3379487. No all-background pass is asserted.

## Local scalar-response experiment: specified frozen toy only

Let chi=delta phi/Mpl and retain a prescribed static acceleration g(r), not a
coupled metric/khronon/polarization solution. At fixed g and a rolling FRW
background, the exact scalar equation is

  nabla_mu[(1+epsilon h) nabla^mu phi] - (1-epsilon h)V'=0.

Subtracting the homogeneous canonical equation, dropping metric/lapse response
and local delta-phi time derivatives, yields

  div[Z grad chi]= -2 epsilon(V'/Mpl) h
                         +epsilon(q/Mpl) h_dot, Z=1+epsilon h,
  h_dot=(3/2)H eta x h',
  V'=-lambda V/Mpl, q/Mpl=a sqrt(eta/epsilon).

For lambda1 this equals the code's

  S_chi=2(1-eta/2)a^2 h
          +(3/2)H a sqrt(epsilon) eta^(3/2) x h'.

Acceleration a is restored as a_SI/c^2 in this geometric-length equation.
The frozen g(r) is obtained from the unscreened spherical algebraic relation
mu(g/a)g=g_bar for a uniform baryon core and exterior point mass. The PDE has
regular inner flux and chi=0 at the declared outer radius. The reported
source-only |delta ln a|=(1-eta/2)|chi|/2 assumes fixed q and lambda1.
It excludes lapse-driven delta X, coupled g response, screened W(P) backgrounds,
external-field environment and time-dependent boundary data.

Twenty-four solves use Sun, Earth, toy Milky Way and toy cluster fixtures,
eta.1 or1/3 and three grids/outer radii. Largest source-only |delta ln a| is
1.23651e-10 at the toy cluster observation radius; the Sun at1AU gives
3.99681e-23 for eta.1. Largest spatial-gradient/background-q ratio is2.08247e-4.
Maximum grid relative change is5.96e-6 and outer-boundary change5.43e-4. These
are sensitivity and discretization checks for this PDE. They are not a proof
of local constancy in the full action. A separate bare baryonic lapse estimate,
eta GM/(2rc^2), is recorded only as an omitted-effect scale, not a total metric.

The new unscreened Solar force correction is5.27e-7 m/s^2 at1AU. That branch
has a serious local-gravity obligation. It does not reject or validate a
stiffness-screened branch: its khronon acceleration and physical acceleration
differ and must be solved together. The old screened v3s pass cannot transfer.

## Failure history and provenance

run_001 failed on a structurally unequal SymPy expression whose exact difference
is zero. run_002 failed because mpmath's absolute Hermitian tolerance rejected
a tiny imaginary diagonal; a diagnostic captured relative defect2.06e-85.
Their original manifests and logs remain unchanged. Exact source reconstructions
match both original SHA256 values, recorded in failed_source_reconstruction.json.
Run003 succeeds with a raw relative adjoint check preceding roundoff projection.
Its source snapshot is also retained. No failure has been silently overwritten.

The standard computation-audit manifest validator reports run003 valid. It does
not certify the mathematical interpretation. inputs.json pins the13 actual repo
source byte hashes and parent-supplied revision context. The check rehashes those
inputs and confirms all unchanged. This route made no repository edits or Git
operations. Independent verify_archive reviewed the analytic identity,50/81
bound and negative-C argument and required the explicit frozen-system scope.

## Remaining gates

Finite mu_K and omitted metric/shift constraints, mass/time/curvature terms,
full finite-wavelength poles, misaligned or spacelike scalar gradients, the
x=0 homogeneous strong-coupling limit, sign interfaces and negative-rho_tau
backgrounds remain unresolved. The fast parallel principal mode is generally
superluminal relative to the metric; energy positivity is not metric-cone
causality. No kappa derivation, phantom crossing, abundance/growth closure,
SPARC/lensing fit or screened Solar/galaxy background is established.

The next constructive gate is the coupled screened static background for the
new W(P), followed by local eta and the full constraint symbol evaluated on it.
The force-law and distance-invariance experiments elsewhere use different
algebraic kernels; neither their numerical success nor their scale homogeneity
can transfer to this action. A physical stiffness length may break the latter.
