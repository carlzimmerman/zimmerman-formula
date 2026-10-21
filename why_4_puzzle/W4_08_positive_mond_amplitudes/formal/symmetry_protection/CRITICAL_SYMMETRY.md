# P3: interacting critical points, protected data and dual response

2026-10-20. Analytic packet under criteria-only checkpoint `1d58a0851`,
base `b37b50b1c`. No scripts, scans, downloads, builds or Lean runs.
Primary source/version cards are in `SOURCES_CRITICAL.md`.

**Verdict.** No amplitude selector is obtained in the tested classes. A
concrete interacting four-dimensional SCFT has exactly the protected
dimension needed by the simplest critical-source proposal, but its bottom
component source runs away on the full Coulomb branch. A stable affine
ground-state-source replacement has the wrong sign for a leading positive
cubic after the linear stiffness is removed. Genuine supersymmetric
deformations have different dimensions. Large-charge CFTs give a genuine
positive nonanalytic energy and a scalar/gauge dual description, but in a
finite-density ensemble and with theory-dependent leading amplitude. The
protected four-dimensional dilaton anomaly fixes a different observable.
These are restricted tests, not a theorem excluding every interacting CFT,
clock completion or duality-based construction.

## 1. Which response must be protected

Use four spacetime dimensions, signature `(-+++)`, a dimensionless physical
potential `Phi`, `h=|grad Phi|` and `z=h^2`. The required static energy is

    E(h)=epsilon+C3 h^3+o(h^3)       (IR),
    E(h)=C2 h^2+o(h^2)+constant     (actual UV force regime),
    C2>0, C3>0, epsilon>0,
    [C2]=2, [C3]=1, [epsilon]=4.

The UV line is a separate physical regime, not a quadratic coefficient in
an expansion about a finite-density IR state. A scalar-source diagnostic
with energy `integral[E(h)+q rho Phi]`, `q>0`, gives

    div[(E_h/h) grad Phi]=q rho,
    4pi r^2 E_h=q m,
    a_phi=q h,
    Gs=q^2/(8pi C2),
    a_phi^2=Gs m a_s/r^2,       a_s=2q C2/(3C3).

These follow directly by varying Phi and integrating Gauss' equation for
a spherical positive source of mass m. Boundary variations of Phi vanish;
the flux at infinity carries the source. They assume a universal physical
matter coupling giving the displayed charge and force. A tensor channel,
disformal metric, screening or other matter coupling requires a new
physical-force calculation. In the single-mediator convention only,

    R=epsilon C3^2/C2^3,       xi=32pi/(9R).

The requested value `R=128pi/9` is a target, not an input below. Neither a
CFT operator normalization nor a dual flux convention supplies q.

For the minimal Lorentz-scalar static continuation `L=-E(Z)`,
`Z=g^{mu nu}partial_mu Phi partial_nu Phi`, direct metric variation gives

    T_mu nu=2 E_Z partial_mu Phi partial_nu Phi-E g_mu nu,
    rho=E,   p_perp=-E,   p_parallel=-E+2z E_z.

Thus the cubic gradient stress is anisotropic. Only the `h=0` constant
epsilon has vacuum form. This formula is not a stress calculation for an
unspecified clock-projected completion, and no healthy continuation
through both timelike and spacelike Z is assumed.

## 2. An actual exponent-matching interacting SCFT

The rank-one Argyres-Douglas theory `H1=(A1,A3)` has a Coulomb primary O of
dimension `Delta=4/3`, with a freely generated Coulomb ring. This is the
specific interacting candidate, rather than a continuously adjustable
postulated scaling dimension. See Banerjee--Buican, v2, section 4.3,
particularly the paragraph before (4.4) and the paragraph about
`alpha_0^k` after (4.9).
[Primary text](https://arxiv.org/html/2306.12521v2).

Consider the **bottom-component Hamiltonian portal**

    H(z)=H_CFT+J(z) O_R,       O_R=Re O,       J(z)=lambda z.

An operator rescaling may be removed by fixing its two-point
normalization; lambda then remains a physical portal coupling. Since
`[J]=4-Delta=8/3`, `[lambda]=2/3`. If a stable one-scale deformation obeyed
hyperscaling, its singular vacuum energy density would have the form

    E_sing(J)=A_+ J^(4/(4-Delta))=A_+ J^(3/2),    J>0,
    C3=A_+ lambda^(3/2).

The scaling equation fixes the exponent, not A_+ or lambda. This is a
conditional dimensional calculation, not a claim that the displayed H1
source actually has a stable vacuum, a gap, locality, or this equation of
state.

There is a direct problem with that source. Let `u=<O>` label the
homogeneous supersymmetric Coulomb vacua. Their vacuum energy is zero in
the rigid supersymmetry normalization. If the full noncompact branch is
admissible in the global minimization, those vacua are trial states with

    <H_CFT>/volume=0,       <H(J)>/volume=J Re u.

The branch has arbitrary complex u; taking `Re u -> -infinity` for J>0
makes the infimum `-infinity`. This variational runaway uses a bottom
operator source and the full branch. Holding a particular boundary sector
at spatial infinity, introducing a stabilizing potential, or replacing the
source by a supersymmetric descendant changes the problem. It does not
prove runaway for every deformation of H1. Spatially varying compact
sources also require their own gradient and boundary analysis.

### Genuine F-terms are different sources

For a chiral primary of dimension Delta, a four-dimensional N1 F-term
contains two Q's and has operator dimension `Delta+1`. An N2 Coulomb
F-term contains four Q's and has dimension `Delta+2`. This distinction is
explicit in Córdova--Dumitrescu--Intriligator, Eq. (1.10), sections 3.2.1--2,
Tables 20 and 22.
[Primary text](https://arxiv.org/html/1602.01217v1).

In superspace notation when available, these are respectively

    delta L_N1=integral d^2theta lambda_1 O+h.c.,
    [lambda_1]=3-Delta=5/3,
    delta L_N2=integral d^4theta_chiral lambda_2 O+h.c.,
    [lambda_2]=2-Delta=2/3.

The half-superspace N2 measure is not the full eight-theta measure. A
one-scale dimensional vacuum-energy power would consequently be
`|lambda_1|^(12/5)` or `|lambda_2|^6`, not the bottom-source `J^(3/2)`.
These are possible scaling powers, not nonzero SUSY vacuum energies:
an unbroken rigid supersymmetric vacuum has zero energy. Promoting either
lambda to a gradient-dependent spurion requires its supermultiplet and
Ward identities, and cannot be identified with `J=lambda z` by notation.

## 3. Restricted sign test and analytic portal discriminator

The concavity principle is inherited from `../NEUTRAL_CURRENT_TEST.md`
and `../protected_normalization/QUANTUM_STATE.md`; it is not a new general
theorem here. Its Hamiltonian form applies to interacting fermions too.
Assume a common Hilbert space and z-independent admissible normalized
states/common quadratic-form domain, a Hermitian affine family
`H(z)=H0+z V`, a finite stable ground infimum, and a thermodynamic limit of
the ground energy density. The same ensemble, gauge constraints and
boundary conditions must be used for every z. Then

    E(tz1+(1-t)z2)
      =inf_psi[t <H(z1)>_psi+(1-t)<H(z2)>_psi]
      >=t E(z1)+(1-t)E(z2),          0<=t<=1.

No positive Euclidean path-integral measure or bosonic determinant is
needed. If the right tangent `ell=E'_+(0)` is finite, concavity gives

    E(z)-E(0)-ell z<=0,             z>0.

Consequently a leading `+C z^(3/2)`, C>0, after removing the constant and
linear term is impossible in this class. Adding a twice continuously
differentiable local counterterm with its affine Taylor part subtracted
contributes `O(z^2)` and cannot
reverse the conclusion. A positive uncancelled linear term instead
restores quadratic IR stiffness. Singular nonanalytic source counterterms
can insert a cubic but constitute precisely an additional amplitude.

Where isolated eigenvalue perturbation theory is valid, the same sign is
visible as `E''=-2 sum_{n>0}|<n|V|0>|^2/(E_n-E_0)<=0`. For the dimension
4/3 critical operator, the undeformed two-point integral has short-distance
radial power `r^(3-8/3)=r^(1/3)`: it is UV-integrable and IR-divergent.
Thus an IR singular susceptibility is compatible with this sign; it is
not evidence for a positive cubic. The spectral formula is not assumed
at an actually degenerate or gapless point; the variational inequality is
the load-bearing statement.

Excluded from this test are temporal Gauss extrema, a source-dependent
constraint/domain, fixed-charge states, canonical Hamiltonians nonlinear
in z after elimination, and a nonlocal functional substituted for E(z).
A critical theory need not produce a local action at h=0. If a stable
source opens a gap m(J), a local-density approximation additionally needs
`|partial J|/|J| << m(J)`; no automatic failure or success of that condition
is inferred just from criticality.

### A small conditional classification of one-source portals

Take a four-dimensional Lorentz-invariant unitary CFT, a gauge-invariant
primary, a constant-gradient external Phi, one source-generated scale,
no pre-existing density/clock scale, and a leading analytic local portal.
For a scalar portal `J=lambda z^p`, p a positive integer, hyperscaling
requires

    E_sing proportional h^[8p/(4-Delta)],
    h^3 requires Delta=4-8p/3.

Scalar unitarity `Delta>=1` permits only p=1, Delta=4/3. For p>=2 the
required dimension is negative. The identity is a separate local source
counterterm, not an interacting response. For the other two simplest
primary portals:

    partial_mu Phi O^mu:             Delta_required=8/3 < 3,
    partial_mu Phi partial_nu Phi
       O_ST^{mu nu}:                 Delta_required=4/3 < 4.

The bounds 3 for a vector and 4 for a symmetric traceless rank-two primary
are the four-dimensional unitary representation bounds; the operator
must be gauge invariant. A vector descendant `O_mu=partial_mu O` evades
the primary vector bound, but this portal integrates by parts to
`-Box Phi O` and has no bulk constant-gradient response. Boundary terms
or inhomogeneous responses cannot then be relabeled local E(h).
[Primary bound and qualifications, Eq. (1.3), footnotes 3--4](https://arxiv.org/pdf/0801.1140).

This classification is limited to these portals and its one-scale
hypotheses. Multiple competing relevant operators, nonanalytic portals,
nonlocal response, background clocks/densities, crossover scales and
Lorentz-breaking fixed points are not classified. It identifies an actual
remaining scalar candidate rather than excluding all CFT constructions.

## 4. A genuinely protected amplitude: the dilaton anomaly

Komargodski--Schwimmer fix the coefficient of the anomaly functional and
the associated low-energy four-dilaton scattering term. Their general
action also contains the independent two-derivative decay constant f
and Weyl-invariant higher-derivative coefficients. For a genuine
spontaneously broken conformal moduli vacuum, their cosmological
potential vanishes. See v2, Eqs. (2.2), (2.9), (2.13)--(2.14), (3.1).
[Primary PDF](https://arxiv.org/pdf/1107.3987v2).

In their anomaly normalization, writing `Delta a` for the matched
coefficient and suppressing curvature terms, the off-shell flat-space
functional includes

    S_WZ=Delta a integral[4 (partial tau)^2 Box tau
                         -2 ((partial tau)^2)^2].

The EOM-reduced scattering representative is
`+2 Delta a integral((partial tau)^2)^2`. Those expressions agree for the
specified on-shell observable. They cannot be interchanged inside a
static source calculation without also transforming sources and the other
operators. In particular a constant nonzero gradient of tau does not obey
the leading source-free equation `Box tau=(partial tau)^2`.

This protected term has four derivatives, rather than a first-gradient
cubic. Around a nonzero compensator vacuum the two-derivative term gives
ordinary quadratic stiffness. In flat space the allowed Weyl invariant
`integral sqrt(-g_hat) R_hat^2` becomes
`36 integral[Box tau-(partial tau)^2]^2`; its coefficient is independent
of the anomaly and it matters off shell. Thus even the static quartic
cannot be read uniquely from the protected scattering number.

Independently, an exactly scale invariant compensator potential in four
dimensions has `V(chi)=k chi^4`. A stationary nonzero chi requires k=0,
so that vacuum energy is zero. A positive constant gravitating vacuum
requires an additional breaking/state/gravity construction. Anomaly data
do not fix f, a massive-matter source coupling, or that construction.
This tests actual protected data; it does not repeat the old pure-electric
D3/DBI tension or endpoint-normalization calculation.

## 5. Constructive alternative: positive large-charge energy and its dual

The interacting three-dimensional critical O(2) model and supersymmetric
`W=Phi^3` example have a controlled large-charge Goldstone description.
The leading coefficient is CFT data; the common symmetry and universal
subleading Casimir term do not fix it. The primary explicitly warns that
the Goldstone expansion is not an expansion about its zero-density
origin. See Hellerman--Orlando--Reffert--Watanabe v4, introduction,
sections 3.3, 5.1 and 6.2.
[Primary text](https://arxiv.org/html/1505.01537v4).

Here is the direct stress/ensemble calculation, with D the spacetime
dimension and theta a phase, not the gravitational Phi:

    X=-g^{mu nu}partial_mu theta partial_nu theta>0,
    P(X)=c X^(D/2),      c>0,
    theta=mu t,
    n=partial P/partial mu=D c mu^(D-1),
    epsilon_charge=mu n-P=(D-1)c mu^D,
    p=P,    epsilon_charge+p=D c mu^D,
    epsilon_charge(n)=(D-1)c[n/(D c)]^[D/(D-1)].

Thus D=3 has a positive fixed-charge `n^(3/2)` energy, while its pressure
is proportional to `mu^3`. D=4 instead has quartic pressure and a
`n^(4/3)` fixed-charge energy. The finite-density stress is traceless
perfect-fluid stress with `p=epsilon_charge/(D-1)`, not positive vacuum
stress. Adding a constant vacuum term breaks this equation and does not
tie that term to c.

For `theta=mu t+pi`, direct expansion at mu>0 gives

    L2=(D(D-1)/2)c mu^(D-2) pi_dot^2
                         -(D/2)c mu^(D-2)|grad pi|^2,
    cs^2=1/(D-1).

The static perturbation energy at fixed homogeneous charge has the same
leading positive quadratic spatial stiffness, by the Legendre envelope
identity `partial_z H|n=-partial_z L|mu`. A strictly time-independent
theta has X<0 and lies outside this real timelike Goldstone branch. Thus
the pressure cannot be substituted for `+C3|grad Phi|^3` in section 1.
If such a static cubic were independently installed in two spatial
dimensions, Gauss' law would give `h proportional r^(-1/2)`, rather than
the three-spatial-dimensional `r^(-1)` MOND field.

Duality is constructive but does not remove the amplitude. In three
dimensions identify the conserved current with the Hodge dual of a gauge
field strength, with a **specified** flux convention `n=sigma B`. Then
the same homogeneous energy is

    epsilon_charge(B)=2 sigma^(3/2)/(3^(3/2) sqrt(c)) |B|^(3/2).

For example `sigma=1/(2pi)` is the convention in which a 2pi magnetic
flux carries one unit of the chosen integer charge. This convention is
not inferred from an unidentified topological integer or used to set a
gravitational amplitude. The dual exponent and coefficient follow from
the fixed-charge Legendre transform above. A rescaled F changes the
displayed coefficient; source and charge normalizations must follow it.
The cited source's rescaled dual variables are not imported to fix q.

More generally, the desired convex *static* scalar energy itself has a
dual variational representation for every C>0:

    E(h)=C |h|^3,
    D=partial E/partial h=3C |h| h,
    E_star(D)=2/(3 sqrt(3C)) |D|^(3/2),
    E(grad Phi)=sup_D[D dot grad Phi-E_star(D)].

Varying Phi in the first-order sourced functional gives
`div D=q rho`, with the same boundary flux as section 1. Away from
sources the spatial Hodge dual of D is a closed two-form in three
space dimensions. This is a bounded static Legendre/closure statement,
not a constructed Lorentzian healthy two-form theory. The transform and
inverse work for every C, and for every strictly convex interpolating
E. Hence ordinary scalar/form dualization supplies no equation selecting
C, epsilon or the UV interpolation. Extra self-duality, microscopic
symmetry and matter matching would be additional physical hypotheses.

## 6. Counterterms, same-state vacuum and remaining implication

An isolated exact flat CFT in its Lorentz-invariant vacuum has a
traceless stress tensor; `T_mu nu=-epsilon g_mu nu` then requires
epsilon=0. A finite-density state evades the vacuum assumption but has
the non-vacuum stress above. Curved-space trace anomalies are another
problem, requiring the curved state and gravitational backreaction;
they do not identify a source coefficient with an independently added
flat vacuum term.

After coupling a Phi portal, Einstein gravity and arbitrary massive
matter, diffeomorphism invariance and Phi shift symmetry alone allow
independent local matching terms, for example

    integral sqrt(-g)[-delta epsilon+delta Mpl^2 R/2
                      -delta C2 Z+c4 Z^2+cR R Z+cBox(Box Phi)^2+...].

With a clock, its additional invariants must also be included. The exact
flat-CFT Ward identity forbids an arbitrary constant identity term if
that identity is demanded of the entire system; it does not at the same
time furnish positive epsilon. A compensator can organize the allowed
terms covariantly but does not itself fix their finite coefficients.
For the dimension-4/3 bottom source, `[lambda]=2/3` already introduces a
physical matching scale. Fixing O's normalization does not fix lambda,
the physical matter map, C2 or positive epsilon.

The smallest missing implication is an actual microscopic Ward identity
or quantization relation tying **all three physically matched** quantities
`epsilon, C3, C2` in a stable, sourced, same-state branch, while excluding
every symmetry-allowed deformation and preserving the needed crossover.
None of the authenticated protected dimensions, anomaly coefficient,
large-charge Ward identities or ordinary dualization supplies that
implication. A future interacting construction with non-affine dynamical
sources, a different ensemble or additional exact symmetry remains open;
it must supply its action, stress, source force and health checks rather
than just a protected exponent. No full microscopic/quantum completion,
amplitude selection or target match is claimed.
