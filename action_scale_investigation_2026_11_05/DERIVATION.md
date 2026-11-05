# Scale selection: three structural checks

Kappa=1/2 FITTED. Original target not reached. These are internal analytic
results, self-reviewed and corroborated by checks.py, not external novelty
claims. Sources are CONTRACT.md and the pinned local AZ40/AC2 definitions.

## 1. Varying the actual fields does not vary a coupling

Let a=a0/c^2 and q=sqrt(Y). The adopted kernel is

    J = Lambda - 2 a^2 [q/a - log(1+q/a)].

The field Euler-Lagrange equations vary the metric, clock and auxiliary
fields at fixed a. They contain no equation obtained by varying a coupling.
On a homogeneous zero-acceleration background q=0, J=Lambda for every a>0.
The action and all first field variations on that branch are unchanged when
a changes; the kernel starts at -Y, with its first a-dependent term
2 Y^(3/2)/(3a). Thus neither that background nor its quadratic perturbations
can determine a. This is a degeneracy of this branch, not a demonstration
that every value fits observations or gives a globally healthy theory.

Promoting a to an auxiliary field is a new action. If no other term depends
on it, define s=q/a and

    h(s)=s+s/(1+s)-2 log(1+s),
    h(0)=0, h'(s)=s^2/(1+s)^2.

Then J_a=-2 a h(s)<0 for every finite a,q>0. The new algebraic equation
J_a=0 has no such solution; at q=0 it holds for every a. This minimal
promotion therefore gives neither a finite nonzero acceleration-sector
solution nor a selected vacuum scale. Kinetic terms, new potentials,
boundary prescriptions, or a-dependence of stiffness change this statement
and must be supplied and varied explicitly. This is not a no-go for them.

## 2. AC2's linear cosmological health cannot select xi

For K=4 pi G and p=K sqrt(P.P), AC2 has

    W(p,a)=p^2/(2K)+p^3/(3Ka)+p^4/(4Ka^2)+O(p^5).

Around P=0, a_bar>0, the full quadratic action is independent of a_bar and
its perturbations. The |P|^3 term is C2 at zero and has zero second
variation. Dependence of p on metric perturbations does not change the
degree counting. P.A is independent of a. AC2's stiffness has no xi
dependence. Canonical scalar, Einstein and minimally coupled matter actions
also have no xi. Consequently, adding their coupled matter perturbations
cannot make this quadratic action determine xi. It may reveal instabilities
or additional constraints, but these would be shared across xi on that same
background. Nonlinear physics can depend on xi; it is not excluded here.

The same statement holds for the density portal a^2=b rho(X,phi) near this
zero-polarization background, provided rho>0 and the portal is smooth there.
This does NOT prove the charged-background action healthy or protect xi
quantum mechanically. It identifies the first order where xi can matter.

## 3. A general k-essence exact-density portal

Take the two-independent-field clock/scalar class in CONTRACT.md. At a fixed
timelike scalar state let F be C3, X>0, rho=2X F_X-F>0,
r=rho_X=F_X+2X F_XX>0, t=rho_XX finite. Set a^2=b rho with b>0.
Write epsilon=b/(2K). At fixed p, p=a*s/(1+s), direct derivatives give

    W_rho = -epsilon h(s),
    W_rhorho = epsilon s^3/[2 rho (1+s)].

The coefficient of (delta phi_dot)^2 in the Hessian of F-W is

    T = r + epsilon h(s)(r+2Xt)
          - epsilon X r^2/rho * s^3/(1+s).

For each fixed admissible scalar state,

    lim[s->infinity] T/s^2 = -epsilon X r^2/rho < 0.

The proof uses h(s)=O(s), finite t, and s^3/(1+s)~s^2. No power-law
ansatz for F is needed. Therefore every such choice has sufficiently large
s with a negative fixed-p scalar velocity coefficient. There is no uniform
positive choice of the imposed b that cures the whole s>=0 domain.
Shrinking b moves a threshold; it does not single out a positive value.

### Why integrating out polarization alone can mislead

At fixed conjugate acceleration A, extremizing A*p/K-W gives
p=a*A/(a+A). The reduced Lagrangian contribution is

    Lpol(A,rho)=a^2/K [A/a-log(1+A/a)].

Let s=A/a, and retain the independent clock perturbation through
delta A=-k delta sigma_dot in a fixed-metric parallel local mode, k>0.
With v^2=2X, the velocity Hessian for (delta phi,delta sigma) is

    H11 = r+L_rho(r+2Xt)+2X r^2 L_rhorho,
    H12 = -k v r L_Arho,
    H22 = k^2 L_AA > 0.

Direct differentiation gives exactly

    H11-H12^2/H22 = T.

In particular the omitted correction is

    2X r^2 L_Arho^2/L_AA
       = epsilon X r^2/rho * s^4/(1+s)^2 > 0.

Thus the fixed-metric two-field kinetic matrix is indefinite once T<0.
Setting the clock velocity to zero before evaluating health removes the
term which exposes the negative direction. This generalizes the canonical
CT14/AZ40 algebra in the explicitly stated local class.

### Metric constraints and the physical scope

For the generic parallel PN constraint density

    L2 = T u^2/2 - k^2 Phi^2/2 + k P Phi - D P^2/2
             - ell Phi u - B P u - k P w,

u,w are scalar and clock velocities, Phi,P are constraints, D>1. Exact
elimination yields

    H22=k^2/(D-1), det H=(k^2 T+ell^2)/(D-1).

The polarization velocity mixing B cancels from this determinant. For a
fixed background with finite ell and T<0, this block is indefinite when
k^2>ell^2/(-T). This is a conditional local high-frequency extension;
the complete action's coefficients, other lapse terms, allowed wavelengths,
stiffness switch and solved background must be matched before applying it.
In particular a finite EFT cutoff might exclude the requisite k. No
physical solar or galaxy instability is newly certified by these fixtures.

### Escape conditions are specific

The argument does not cover X=0, rho_X=0 constrained scalars, a bounded
accessible s domain, additional derivative operators, or identification of
phi with the clock. An exactly potential-only portal evades the derivative
terms but does not track the density on arbitrary scalar histories. A
single-clock density portal changes the constraint structure and is the
next candidate to check; it is not excluded by this two-field determinant.

## Evidence and review status

checks.py verifies the exact identities and 54 direct-derivative fixtures
at 40/80 digits. The mutation deliberately omits clock mixing and must fail
the Schur identity. Finite fixtures are diagnostics, not background solutions.
Self-review: domains, signs, fixed-p versus fixed-A derivatives, finite
jet coefficients, field-order counting, clock retention and large-s limit
checked. Primary proof-audit verdict: proved as written for the scoped
algebraic statements, with the full-action application explicitly conditional.
No independent review and no complete physical theory are claimed.
