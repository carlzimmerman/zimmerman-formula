# Independent audit of the finite-regularity local construction

**Verdict: proved in the stated local periodic Lipschitz strong-solution
class, with the operator-neighborhood and constraint-trace details made
explicit below.** I find no remaining derivative-loss or cusp obstruction
to this local argument. This is not a smooth all-orders theorem, a global
existence result, or a singular-continuation result.

Reviewed candidate: LOCAL_EVOLUTION.md, SHA-256
05217ebf0e188ce365aa34d69920ed5dee1ade17aaddb62915b1f1f9d1c12c6b.
The source is an internal construction, not a direct application of the
external smooth symmetric-hyperbolic theorem mentioned for comparison.
The audit below verifies the extra nonlocal and Lipschitz steps rather
than relying on that citation.

## Precise local statement

Take periodic spatial W1,infinity initial U=(r,A,P,beta,B,E,a,K), ell>0,
with the declared strict on-branch/hyperbolic/cap margins and an invertible
initial periodic auxiliary operator. The datum need not satisfy constraints
for the expanded-system construction. Restrict the lower fields and ell
to a sufficiently small C0 operator neighborhood, and all fields to a
bounded state set. There is a positive time and a unique jointly Lipschitz
U solving the exact expanded system almost everywhere, with the specified
initial continuous trace, and the exact periodic inverse at each time.
The scalar ell solves its ordinary differential equation. Continuous
dependence is in C(time;L2), uniformly within bounded Lipschitz classes.

This does not assert strong continuity in the W1,infinity norm at the
initial time. Spatial derivatives have their weak initial trace, which
is sufficient for the residual argument.

## 1. Gauge and inverse neighborhood

The mean-zero shift satisfying
w_x=mean(K/r)-K/r and ell'/ell=mean(K/r) gives the actual commutator
[n,e]=-e(log r)n-Ke, including off constraint. The shift map gains one
spatial derivative and is locally Lipschitz from L2 state differences to
H1 shift differences. In one dimension this also controls shift differences
in the supremum norm, as needed in the hyperbolic energy estimate.

The auxiliary first-order matrix depends on the lower fields, not on
spatial derivatives or the forcing variables a,K. Given an initial inverse
Lp->W1,p, perturb its multiplication coefficient in the supremum norm.
The resulting bounded operator perturbation on W1,p is small, so a Neumann
inverse supplies a common neighborhood and uniform estimates. In particular
the L-infinity inverse controls z=(u,v) and z_x by bounded state values.

The explicit off-constraint energy from RESIDUAL_PROPAGATION.md is an
alternative when Cbeta is small in L-infinity. It does not replace the
C0 operator argument for arbitrary iterates: C0 closeness alone need not
make beta_x-E small.

For two states the exact difference equation is

    T1(z1-z2)=(M1-M2)z2+f1-f2.

Pointwise Lipschitz dependence, bounded z2 and the uniform L2->H1 inverse
therefore prove the claimed L2-state-to-H1-inverse Lipschitz estimate.
The same statement includes ell differences. Uniform errors in proof-
approximant coefficients add an ordinary uniform-error term to this bound.

## 2. Smooth proof approximants: the tame estimate needed for continuation

Mollify the native locally Lipschitz source/inverse coefficient functions
inside the fixed compact state neighborhood, preserving uniform Lipschitz
constants and convergence. Strict initial margins and sufficiently small
coefficient errors preserve the inverse neighborhood. Smooth initial data
can approximate the W1,infinity datum with uniform first-derivative bounds.
No assertion of constraint preservation is needed for these approximants.

For each fixed approximation, the source/inverse maps are smooth. The
standard frozen-coefficient iteration closes here because the inverse has
the following tame bound, which makes the candidate's smooth construction
step explicit. From z_x=M(U)z+f(U), for integer s>=2,

    ||z||H^s <= C_s[||z||L2+||M||H^(s-1)||z||infinity
                    +||f||H^(s-1)].

The lower ||z||H^(s-1) term from multiplication by bounded M is absorbed
by interpolation. Smooth composition on a compact set gives a bound
linear in 1+||U||H^(s-1), with constants allowed to depend on the fixed
smoothing index. Thus the nonlocal source costs no derivative in the
hyperbolic high-norm estimate. The shift has the analogous derivative gain.
This verifies the key property needed in a smooth Picard/energy construction;
it is not an unproved smoothing assertion about an arbitrary nonlocal map.

Once first derivatives are bounded, fixed-index high-Sobolev energy obeys
a linear Gronwall bound with finite fixed-index constants. Consequently
each smooth approximant extends over the uniform first-derivative interval.
Higher constants need not be uniform in the smoothing index.

## 3. Uniform first derivatives and the repeated-speed block

The six advected fields have coordinate eigenvectors. The two other left
eigenvectors depend smoothly only on r,A, and their inverse remains bounded
on the strict hyperbolic neighborhood. Repetition of the advective speed
does not create a Jordan block or require differentiating an arbitrary
eigenbasis.

For V=U_x the differentiated smooth system has sources
-(C_x)V+F_x. The actual inverse equation gives z_x bounded solely by
state bounds. Source approximants have uniformly bounded first state
derivatives, including the mollified cusp coefficient. Thus

    ||F_x||infinity<=C_R(1+||V||infinity).

The principal coefficient and eigenvector derivatives have at most linear
dependence on V. Along the diagonal characteristics this gives
m'<=C_R(1+m)^2 for the maximum eigencomponent of V. The state time
derivative has the corresponding bound. These yield a positive uniform
time, maintain the operator/domain neighborhood and keep ell positive.
No W_PPP or second derivative of the native source is required.

## 4. Convergence, native cusp, and uniqueness

Subtracting two approximate systems and using one symmetrizer gives an
L2 inequality for the state and ell differences. The term involving a
principal-coefficient difference multiplies the uniformly bounded U2_x.
Pointwise coefficient Lipschitz bounds and the shift H1 bound control it.
The source difference is controlled by the inverse H1 estimate in section 1.
Symmetrizer first derivatives are uniformly bounded. Uniform approximation
errors enter additively and tend to zero. Gronwall therefore makes the
sequence Cauchy in C(time;L2).

Uniform spatial/time Lipschitz bounds give uniform convergence on the
compact time-space cylinder (and weak-* convergence of first derivatives).
The exact inverse depends continuously on the uniformly converging state,
so there is no unresolved nonlinear inverse defect. Principal coefficients
converge uniformly and multiply bounded weakly converging derivatives;
the limit solves the exact native expanded equations distributionally
and almost everywhere. The same energy inequality proves uniqueness in
the bounded Lipschitz class. No mollification remains in the equations.

This is the step that resolves the earlier W_PP cusp concern. Native
W_PP is locally Lipschitz inside the cap; its bounded almost-everywhere
derivative is sufficient. All-orders smooth/high-Sobolev regularity at a
generic P zero is neither used nor obtained.

## 5. Native constraints and initial trace

RESIDUAL_PROPAGATION.md directly derives the complete homogeneous normal-
transport residual system for exactly this off-constraint extension.
Joint Lipschitz fields permit its commutator/product calculation in
divergence form in distributions; only first derivatives of the native
constitutive functions appearing there are needed.

At tau=0 the continuous initial trace U0 determines the weak spatial-
derivative trace: pairing with a smooth periodic spatial test function
and integrating by parts passes to U0. Thus compatible initial data
give zero initial residual trace even though the proof approximants were
not exactly constrained. After dividing by positive r, the residual
system has common spatially Lipschitz transport velocity -w and bounded
homogeneous coefficient matrix. Characteristic transport uniqueness
preserves zero. No assumed Bianchi cancellation replaces this check.

On zero residuals the promoted equations recover the native matter and
all planar Einstein components, not merely the truncated a,K block.

## 6. Continuation estimate

On constraint, all six lower-field spatial derivatives are algebraically
bounded by compact state values. Shift derivatives and the time/space
derivatives of the principal eigenvectors are therefore controlled
independently of a_x,K_x. The inverse still gives bounded z_x from bounded
state values.

The differentiated a,K source has only linear dependence on a_x,K_x.
For the native Lipschitz source this follows by spatial difference
quotients or the weak chain-rule bound, not by assuming differentiability
of W_PP at zero. Diagonal characteristic transport then gives

    m'<=C_R(1+m)

for the a_x,K_x eigencomponents. The characteristic velocities are
spatially Lipschitz with bounds independent of these high derivatives.
Thus a finite-time endpoint with compact domain/length/state bounds and
bounded a,K has bounded full W1,infinity norm. Time Lipschitz control
gives a continuous limiting datum with the same weak derivative bounds;
the constrained coercive inverse remains uniformly available. Restarting
the local construction extends the solution. This is the required
continuation criterion, not a circular assumption of bounded derivatives.

## Consequence boundary

This audit supplies the local/continuation input previously conditional
in PF08 for this finite-regularity, constant-potential, periodic planar,
on-branch class. A formation theorem additionally needs the independently
audited uniform compact packet bootstrap and gradient comparison; it
does not follow just by naming a local theory. Neither result supplies
postbreak existence, uniqueness, or admissibility.

Independent delegated proof audit, 2026-11-06. No local-existence theorem
was imported for the nonsmooth/nonlocal native source; the required tame,
first-derivative, difference and residual estimates are checked above.
