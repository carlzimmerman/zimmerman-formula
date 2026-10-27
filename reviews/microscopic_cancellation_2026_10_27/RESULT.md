# Unequal-spectrum cancellation and an explicit spectator model

The requested joint microscopic model has not been found. There is a new
algebraic opening: exact pairing is not necessary to cancel the unwanted loop
terms while retaining a positive cubic contribution. But the constructed
spectrum is unprotected and does not fix a gravitating vacuum. A concrete
local two-field detailed-balance action was also tested; its relaxed response
is not MOND and its positive auxiliary energy breaks spectral pairing.

Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and
kappa_crit=0.345 +/- 0.078 are separate, unused measurements. No kappa is
computed. These are two audit routes, not successful normalization candidates.

## What was already tried and what is different

The direct predecessor is [K796](../microscopic_ir_matching_2026_10_26/RESULT.md),
which found a formal positive s^(5/2) term for s=|grad phi|. The older
[SUSY audit](../susy_lifshitz_matching_2026_10_24/RESULT.md) already covered
identical spectra, elementary splitting, and the vanishing affine response
of a single derivative-only detailed-balance superpotential. W4-08's
protected_auxiliaries tested a different relativistic chiral auxiliary fold,
its branch instabilities, and FI/Born-Infeld matching. These are not repeated.

Here the new steps are (A) unequal signed spectral moments and their minimal
support obstruction; (B) an explicit undifferentiated spectator coupled to
the gradient, outside the old single-field argument. Targeted searches of
these predecessors and the local reviews found no identical construction.
This is a scoped local-record comparison, not global novelty certification.

## A. Cancellation without complete pairing is algebraically possible

Assume actual physical modes, if they can be constructed, have the common form

    omega_i = v_i k sqrt(k^2+t_i s(1+mu^2)),   v_i,t_i>0,
    w_i = sigma_i d_i v_i,    M_p=sum_i w_i t_i^p,

where d_i is physical degeneracy and sigma_i is + for bosons and - for
fermions. The angular structure and common momentum cutoff L are explicit
assumptions. In n dimensions the infrared nonanalytic moment is (n+2)/2,
with possible logarithms at integer powers. In n=3, K796 gives

    Delta E = hbar/(4pi^2) [L^5 M0/5
            + L^3 s <a> M1/6 - L s^2 <a^2> M2/8
            + 2s^(5/2)<a^(5/2)> M(5/2)/15
            - s^3<a^3> M3/(16L) + O(s^4/L^3)],
    a=1+mu^2,  <a^3>=96/35.

Thus suppressing the displayed s, s^2 and s^(5/2) terms requires
M1=M2=M(5/2)=0. These equations do NOT require M0 or M3 to vanish.

### A useful minimal-support obstruction

Suppose one statistics side has only one distinct positive t=t0, with any
positive total weight; the other side can have arbitrarily many positive
weights. Equality of M1 sets a common positive normalization S. On the
multi-node side define probabilities p_i=w_i t_i/S using unsigned weights.
M2=0 says sum p_i t_i=t0. M(5/2)=0 says
sum p_i t_i^(3/2)=t0^(3/2). Strict convexity of t^(3/2) forces all t_i=t0.
Then M1 also forces equal total weights, and every moment, including M0,
vanishes. The argument works with the statistics reversed.

Therefore a non-paired solution needs at least two distinct positive response
parameters on EACH statistics side. Response-blind t=0 modes evade this
statement but merely add an independent vacuum sector unless further tied.
This is a theorem about this spectral ansatz, not all microscopic theories.

### An exact four-node fixture

The nodes t_i=t0*(1,4,9,16) were declared before computation. Their moment
nullspace has signed weights proportional to

    w_i=v0*(1248,-684,224,-33),  v0>0.

Both overall signs are mathematical solutions; the displayed orientation is
chosen to show positive M0, not predicted statistics. Exactly,

    M1=M2=M(5/2)=0,
    M0=755 v0,       M3=-14400 v0 t0^3.

Consequently the formal determinant leaves

    epsilon_cut = 151 hbar v0 L^5/(4pi^2) > 0,
    C3_cut = 4320 hbar v0 t0^3/(7pi^2 L) > 0.

It is possible algebraically to remove the new fractional term and the two
lower powers while leaving a positive cubic and positive regulated constant.
The fixture is a counterexample to the claim that these cancellations always
force a zero vacuum or erase the cubic. It is not a proposal for hundreds of
particles: weights can also involve velocity factors, and neither degeneracies
nor velocities have been derived from an action or a symmetry here.

### Why this does not solve the microscopic problem

1. The spectrum itself assumes a nonanalytic background dependence proportional
   to s=|grad phi|, inherited from a presumed cubic response. This calculation
   cannot be presented as deriving that operator from a regular microscopic
   Lagrangian. Arbitrary bosonic and fermionic frequencies need not coexist in
   a local interacting, source-compatible model.
2. Perturbing one weight destroys cancellation. No Ward identity protects the
   three moment equations; imposing them is a tuning. A common rescaling of
   all t_i preserves the cancellations and changes C3_cut by its cube while
   leaving epsilon_cut unchanged. Thus even exact cancellation and positive
   constant energy do not select the force amplitude.
3. The constant scales as L^5; the cubic as 1/L. The latter here comes from the
   upper-end analytic expansion after the infrared term cancels. They are
   regulator/matching-dependent quantities, not universal predictions. An
   independent cosmological counterterm is still permitted absent a named
   gravitational normalization principle.
4. There is no high-field Newtonian matching, physical baryon charge, covariant
   stress, or controlled all-orders infrared branch. The original K796
   strong-fluctuation caveat is not removed by a one-loop signed sum.

The target invariant epsilon C3^2/C2^3 is therefore unselected. Varying t0
already disproves selection with epsilon and an independent C2 held fixed.

## B. Concrete local spectator extension

Use canonical time kinetic terms and real time-domain detailed balance:

    E = (F_phi^2+F_chi^2)/2,  F_A=delta W/delta field_A,
    W=integral [a|grad phi|^2/2+b|grad chi|^2/2
                +f chi+g chi^3/3+lambda chi|grad phi|^2],
    a,b,f,g,lambda > 0.

The fermion bilinear is the functional Hessian of W. This action class is
motivated by [1908.03220v1, section 2.1, Eq.5](https://arxiv.org/html/1908.03220v1).
That source gives the real-field detailed-balance construction and time-domain
supercharge algebra; it does not claim our multifield example, MOND matching,
or positive cosmological vacuum selection. The extension and analysis below
are explicit classical calculations, not imported results.

In any spatial dimension,

    F_phi=-a Delta phi-2lambda div(chi grad phi),
    F_chi=-b Delta chi+f+g chi^2+lambda|grad phi|^2.

At fixed affine phi with gradient magnitude s, chi=0 gives

    E_rel(s)=(f+lambda s^2)^2/2
            =f^2/2+f lambda s^2+lambda^2 s^4/2.

This is not just a homogeneous stationary guess. In a finite periodic cell,
allow arbitrary periodic chi and phi=v.x+periodic fluctuation, with fixed v.
The average Laplacian of chi vanishes and average |grad phi|^2>=|v|^2.
Thus average F_chi>=f+lambda s^2. Cauchy-Schwarz and E>=F_chi^2/2 imply
average E>=(f+lambda s^2)^2/2, attained by chi=0 and affine phi.
The exact classical relaxed energy in this boundary class has no cubic.
This argument is dimension-independent and includes spectator gradients.

At zero momentum about this background the spectator boson has

    m_chi,B^2=2g(f+lambda s^2)>0,

whereas W_chi,chi=2g chi=0 and all mixed Hessian terms at k=0 vanish.
Both fermionic zero-momentum Hessian eigenvalues vanish. The positive auxiliary
background therefore fails full boson/fermion pairing already at k=0.
No full determinant cancellation is inferred from the action's supersymmetry.
This does not by itself exclude accidental cancellation of a particular term;
the decisive force failure is the exact relaxed polynomial above.

The response current is 2f lambda h+2lambda^2 h^3. Conditional on a scalar
source q rho_b, Gauss law gives r^(n-1) times this current proportional to
mass. In n=3 the low-gradient branch scales h~M/r^2; the quartic-dominated
branch scales h~M^(1/3)r^(-2/3). Neither is MOND's sqrt(M)/r. The latter is
only the homogeneous/local response diagnostic; higher derivatives matter
where the corresponding gradient hierarchy fails.

Removing lambda removes the response. Taking f->0 removes the positive
classical vacuum and leaves a quartic, not a cubic. Replacing g chi^3/3 in W
by m chi^2/2 instead allows homogeneous chi=-(f+lambda s^2)/m, making both
auxiliary variations vanish and erasing all homogeneous energy, including
vacuum and response. This explicitly tests the spectator-relaxation escape.

Although the original branch has a fixed algebraic energy f^2/2 for a GIVEN
f, f is a free input. This is a classical energy density, not the exact quantum
vacuum or a demonstrated rho_DE c^2. Coupling baryons and gravity without
losing the relevant identities remains absent. No complete quantum stability
or generally covariant theory is claimed.

## Status, verification and continuation

Frozen at 55a75b0759 before executable; baseline check.out passes 16/16.
Changing the final spectral weight by one gives the separately stored mutation
failure. Exact nullspace identities, spectator Hessian, relaxation and source
current are checked symbolically. The Jensen and periodic-cell arguments were
self-reviewed analytically; no independent reviewer or formal proof checker.
No empirical target, downloads, scan or cosmological substitution was used.
I1-I8 inputs/scaling/footing/hbar/pi checks are as frozen; the absent relativistic
and vacuum normalization bridges remain absent, not passed.

Route A remains open as a physical construction problem: derive non-paired
spectral identities from a local interacting symmetry and match baryons,
gravity and absolute vacuum in that SAME theory. The four-node fixture cannot
be promoted by choosing its parameters. Route B closes only the two explicit
spectator potentials tested here. More general constrained multiplets or
nonanalytic critical branches remain untested; the old auxiliary-fold record
shows why merely inserting such a branch is insufficient.

No published action supplying the missing identities has been identified in
the inspected sources. A further numerical moment search would only generate
more tuned fixtures and is not a justified continuation. The next substantive
input must be an actual action with a protective identity, rather than another
choice of frequencies. The original joint-model goal remains unresolved.
