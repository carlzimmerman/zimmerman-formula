# AC2: one canonical scalar supplies dark energy and the preferred clock

Candidate only. The scalar-only FRW quadratic test is healthy in its stated
regime; the full sourced theory has not been established. Kappa=1/2 FITTED.
No v3s observational gate is inherited. This is a different action.

## Definition and changed premises

Signature (-,+,+,+), X=-grad(phi).grad(phi)/2>0, K=4pi G,
Mpl²=1/(8pi G), n_mu=-grad_mu(phi)/sqrt(2X), h=g+n n,
A_mu=n^nu nabla_nu n_mu, and D the intrinsic spatial derivative.
P is spatial, n.P=0; p=K sqrt(P.P), 0<=p<a0(phi).

 S=integral sqrt(-g) [Mpl² R/2+X-V(phi)+P.A-W(p,a0)
            -gamma/2*(D.P)²+lambda_P*n.P] + S_b[g],
 W=a0²/K*[-p/a0-log(1-p/a0)],
 a0²=xi G V(phi), gamma=K Lstar²/2.

There is no independent tau, no separate clock norm penalty, and no bare Lambda.
The independent canonical scalar is itself the preferred foliation while X>0.
The squared divergence is smooth and unswitched: negative-divergence regions
are changed relative to v3s. The old static screen or data-window labels must
therefore be recalculated. Merely replacing tau by phi inside the old equations
would be wrong; the displayed action is varied with n defined by phi.

The AZ40 sinh potential and xi=2*kappa²/(1+beta) still give their selected
constant-w homogeneous scalar/dust solution: on comoving FRW, P=0,A=0,
and all first variations of the added polarization terms vanish. The same
background density relation follows on that branch. General histories do not
obey it identically, and xi still sets kappa by hand. Independent-clock initial
data from AC1 are no longer a freely variable branch: tilting the clock now
changes phi and its stress/field equation. This removes that specific argument,
not every possible caustic or loss of timelike scalar gradient.

## Explicit ADM quadratic calculation

For this calculation only, take a scalar-dominated homogeneous rolling solution
with epsilon=-Hdot/H²=phidot²/(2 Mpl² H²)>0. No matter perturbation is included.
Unitary gauge uses phi=phi_bar(t), h_ij=a_FRW² exp(2zeta)delta_ij,
N=1+alpha, N_i=partial_i beta_shift. Here A_i=partial_i log N;
the acceleration contains spatial lapse derivatives and no lapse time derivative.
All projections in the stiffness are onto these same phi leaves.

At P=0, W=K P²/2+O(|P|³/a0). Integrating the longitudinal P mode by
completing the square gives the positive term Mpl² cY(k) k_phys² alpha²,

    cY(k)=1/[1+Lstar² k_phys²/2].

The transverse P components have positive algebraic cost and no linear scalar
source. The scalar potential's a0-dependence first enters W at cubic order
about P=0; the linear test does not determine its nonlinear effects.

run_v2.py reconstructs the planar ADM quadratic density from the intrinsic
curvature, extrinsic-curvature trace combination and canonical scalar term.
It solves both lapse and shift constraints. The shift gives alpha=zetadot/H.
The remaining zeta*zetadot coefficient is integrated by parts with the evolving
a_FRW/H, using Hdot=-epsilon H². Omitting that derivative gives the wrong
spatial-gradient sign. For one Fourier mode the result, up to its averaging
normalization, is

 S2=Mpl² integral dt a_FRW³ {
       [epsilon+cY*k_phys²/H²]*zetadot²
       -epsilon*k_phys²*zeta² }.

Both coefficients have the required sign for epsilon>0 and Lstar²>=0.
Turning off the P.A coupling recovers the canonical curvature action exactly.
This establishes the specified scalar-only FRW quadratic block, not a theorem
about all matter backgrounds or all constraints.

## Frozen-background dispersion and its limits

Let x=k_phys/H, ell=H Lstar/sqrt(2), E=epsilon. The instantaneous frequency is

 (omega/H)²=E*x²*(1+ell²*x²)/[E+(1+E*ell²)*x²].

Write D=E+(1+E ell²)x². The phase speed satisfies
c_phase²=E(1+ell²*x²)/D, strictly positive and <=1. Its derivative is
-2E*x/D². Therefore

 c_group=c_phase-E*x²/(c_phase*D²),

which is <=c_phase. It is positive because the numerator after multiplication
by c_phase*D² is E*[E+2E ell² x²+ell²(1+E ell²)x⁴]>0.
At finite Lstar>0 the ultraviolet phase speed tends to
sqrt[E ell²/(1+E ell²)]; at Lstar=0 it tends to zero. A small positive sound
speed does not establish weak coupling or prevent nonlinear shocks.

These are instantaneous constant-coefficient speeds. For k_phys comparable to
H, background time evolution cannot be ignored to infer a propagating mode.
Even in the short-wave regime, subluminal phase/group speeds alone are not a
proof of causal support for the full constrained theory. The lapse and P are
spatial constraints; retarded gauge-invariant observables need their own test.

The FRW transverse-traceless metric perturbation has no linear lapse acceleration
or polarization source. The added terms therefore do not alter its quadratic
GR kinetic/gradient terms on this background; its leading FRW tensor cone is
unchanged. This is not a nonhomogeneous gravitational-wave propagation audit.

## Evidence and retained failure

36 fixtures (3 epsilon * 3 ell * 4 x) pass positive kinetic/speed checks and
independent 40/80-digit differentiation. Reversing the induced lapse-gradient
term makes the kinetic coefficient negative on fixtures, as intended.
The criteria's stated total 48 was an arithmetic error: the first script
failed only that count check. initial/ and run.py retain it; COUNT_ERRATUM.md
and run_v2.py correct the count without changing any case, threshold or formula.

## What must happen before calling this a healthy action

1. Derive the coupled matter perturbations and constraint rank on relevant
   cosmological backgrounds; the scalar-only block is insufficient.
2. Solve the single-clock sourced inhomogeneous system and match its clock to
   cosmological initial/boundary data. AC1's two-field radial solves do not
   transfer automatically.
3. Check X>0 preservation, nonlinear evolution, strong coupling and whether
   the low sound speed simply reintroduces a different focusing problem.
4. Recompute own-equation Solar-System, galaxy, lensing and tensor tests after
   the unswitched stiffness change. No FN6 Gaussian-filter pass transfers.
5. Separate the selected density-tie history from a universal relation;
   derive rather than posit xi if the objective includes a kappa derivation.

Self-review only. The exact ADM algebra and finite tests support this restricted
quadratic claim. No independent audit, external theorem certification, complete
DOF theorem, new empirical success or kappa derivation is claimed.
