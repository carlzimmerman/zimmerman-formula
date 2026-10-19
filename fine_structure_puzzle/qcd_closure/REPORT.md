# Deeper QCD closure: actual bounds, boundary matching and finite-charge response

FSP-005. **Physical alpha and R(alpha)=A_rho/mp^3 remain uncalculated.**
This continuation closes several specific mathematical and field-theory
gaps from the previous phase. No measured alpha, cosmic coefficient or
unknown matching parameter was fitted. Earlier scientific inputs remain
frozen.

The most consequential new test concerns an apparent electromagnetic
linear-curvature term. We constructed a precise model in which the first
charge correction really has that term, then summed the full Gaussian
response at fixed charge. The term cancels. This identifies a concrete
failure of an attractive shortcut and a stronger requirement for any
future physical candidate; it is not evidence that every QCD mechanism
has the same outcome.

## The angular calculation now has a quantitative connection bound

The [actual Hessian calculation](angular_connection/REPORT.md) goes beyond
a no-zero-mode argument. For J>=6 it derives the universal Cartesian
angular form, an explicit centrifugal lower bound, and the regular
Dirichlet-to-Neumann map P_J. In its natural charged/neutral boundary scale,

    (tanh(1)/4) Z_J <= P_J <= (5/3) Z_J,
    Z_J=(J/R)I+Q,       R>=4.

Q projects onto the charged angular subspace. The actual relative wall has
a bounded inverse in this scale; its neutral Robin Schur coefficient lies
between tanh(1)/4 and 11/6. A noncommuting Riccati comparison to the exact
far Coulomb operator supplies an explicit remainder, uniformly negligible
for J of order sqrt(R) or larger. With both regular matrices normalized
to identity at r=2, the determinant connection has |c_J|<38.

The [fresh independent audit](reviews/angular_connection/REVIEW.md) checks
the exact operator, coercivity, variational domain, wall, Schur complement
and ordered Riccati estimates. This closes the normalized DN/Schur and
fixed-core determinant obligations. It does not bound every singular value
of an arbitrarily normalized growing map. Original Frobenius normalization
factors and the commonly subtracted infinite angular product remain open.
No physical finite part is assigned to the old divergent coefficient sum.

## The actual boundary term and its common-regulator match

The [relative-wall calculation](boundary_heat/REPORT.md) derives, for one
constant-gapped charged frequency pair with mass m, the boundary heat and
large-mR determinant terms

    A4=-128pi/(315R),
    Gamma_boundary|inverse=16/(315mR).

The normal/tangential projector moves on the sphere. Its derivatives are
essential; freezing it or imposing all-vector Dirichlet gives a different
problem. An independent TE/TM decomposition reproduces the coefficient.
The [fresh boundary review](reviews/boundary/REVIEW_FSP005.md) verifies the
constant benchmark, the local scalar-collar jets, and the heavy-PV
Riemann-sum limit under their specified conventions.

The profile h=v-a/r introduces same-order terms from lower wall functions.
Keeping the common four-dimensional PV fields through the frequency sum
produces +4La^2/(3piR) in the integrated-Duhamel wall representative at
center holonomy. A geometric cubic-wall counterterm is needed for the
absolute frequency sum; it cancels in a same-wall, same-holonomy comparison.
This does not fix arbitrary finite physical wall functions.

The [combined local matching](common_regulator_match/REPORT.md)
finds a further necessary distinction. The integrated Duhamel collar matches
the fully integrated-by-parts bulk. To pair it with the unintegrated
diagonal bulk, its compensating surface is

    Gamma_collar,diag-Gamma_collar,IBP
       =-integral_outer partial_out F0(h)/(12pi).

Its inverse-radius coefficient is -La^2/(3pi). This is invisible at that
order in a strict physical single-frequency calculation but survives the
common regulator sum. Mixing the diagonal bulk with the IBP collar would
therefore give a wrong coefficient even though each separate calculation
had correct arithmetic.

For v=pi/L, B=n_mag rhat/r^2 and the declared magnetic harmonic subtraction,
the matched **local bulk plus collar** one-loop coefficient is

    Gamma_local|inverse=C_local/R,
    C_local=(L/pi)[(11log(2)/3)(a^2+n_mag^2)+7a^2/6-a^4/3].

The a^4 term is the periodic potential, the a^2 terms include the electric
and wall response, and the n_mag^2 term is magnetic. Logweight has the
opposite sign. This result is conditional on the declared local expansion
and wall matching. It omits core/global and neutral contributions, lifted
modes, physical collective-coordinate conversion, deformation and the
stable screened saddle. It is not the complete monopole action or metric
vacuum stress.

The [second independent boundary audit](reviews/boundary/MATCHING_CONVENTION_REVIEW.md)
reconstructed the representative conversion before reading the new match.
It verifies the coefficient and the pure geometric reference cancellation,
while retaining the same local-expansion and finite-wall matching limits.

## The first interaction of the closed neutral ensemble is calculated

The [complete leading quartic diagram](neutral_interactions/REPORT.md)
retains all field modes of the compact cosine theory on S3. Its value is
W_2=lambda V G_R^2/8, with lambda=-m^2/kappa and the common finite-part
coincident propagator. The isolated compact zero-mode correction is already
included in that square and cannot be added a second time.

At fixed Lagrangian mass, its flat-subtracted spatial stress starts at
m^2/(384pi^2 kappa L R^2). At fixed flat pole mass the required tadpole
mass retuning completes a square in G_R-G_infinity, and the **two-loop
correction** starts instead at 1/(1536pi^2 kappa L R^4). The Gaussian
one-loop stress still starts at R^-2. Both paths have zero R^-1 coefficient
for this explicitly computed diagram.

The [independent derivation/review](reviews/neutral_interactions/REVIEW.md)
confirms the Wick coefficient, mass-retuning sign, exact metric derivatives,
zero mode and asymptotic powers. Unknown hard curvature terms, higher
interactions and absolute vacuum matching are not fixed. A numerical-tail
precision failure was isolated and preserved; its corrected implementation
uses explicit analytic spectral-tail bounds. This is a field-theory loop
calculation with a declared action and matching path, not a number search.

## Electromagnetism now enters through the actual curved current insertion

The [QED route](qed_infrared/REPORT.md) uses the physical order-e^2
current-current insertion on closed S4, the transverse photon domain,
canonical global U1 quotient, and the actual metric derivative of W/V.
Its exact spectral diagnostics are zeta_T(0)=19/30,
zeta_T(-1)=5/63, and the Maxwell scale coefficient 31/45 after retaining
the constant gauge-group volume. A massless photon anomaly gives H^4,
not the desired linear H term.

In a specified photon EFT, the calculated dimension-six trace is

    delta rho_gamma,6=-e^2 H^6/(4Omega4)
                      [(19/30)c_R+(5/63)c_lambda],
    c_lambda=-integral ds rho_J(s)/s^2, Omega4=8pi^2/3.

Flat current data can fix c_lambda in principle. c_R requires curved TJJ
matching, and independent pure-gravity/parameter matching also contributes.
The displayed trace is a scheme-defined EFT contribution, not a universal
total vacuum coefficient.

Under explicitly uniform mixed T...TJJ clustering, local matching, global
state and differentiated-remainder assumptions, the linear-H insertion
vanishes. A flat hadron spectral gap alone does not prove those assumptions.
The route constructs a transverse low-mode kernel that disappears in the
pointwise flat limit yet gives a nonzero linear-H first insertion. It then
resums that finite-mode model at fixed charge and obtains H^4 log H instead.
The missing uniformity is a demonstrated order-of-limits problem, not just
a verbal caution about perturbation theory.

## The full singular polarization also loses the apparent linear term

The [coordinator resummation](qed_resummation/REPORT.md) extends
that check to infinitely many modes. Define the positive but nonlocal
Gaussian test operator

    P_eff=Delta_T[1+M^3 Delta_T^(-3/2)], t=(M/H)^3.

This deliberately supplies an infrared singularity strong enough to make
the first perturbative density proportional to M^3 H. It is not a gapped
QCD current kernel. In one common spectral subtraction, an exact Mellin
representation gives

    delta W=-pi t^(4/3)/(4sqrt(3))-pi t^(2/3)/sqrt(3)
               +(19/60)log t+C+O(t^(-sigma)), 0<sigma<1.

The pole at s=1 cancels the explicitly retained first-order trace. Thus
the fixed-M density has only the displayed constant, H^2 and H^4 log H
terms through this order, with a differentiated remainder too small to
hide H. Its full linear-H stress coefficient is zero. Even manufacturing
the proposed singular polarization at first order is insufficient to
obtain the desired finite-charge response.

The [fresh QED/resummation review](reviews/qed_response/REVIEW.md) independently
derives the spectral values and Mellin cancellation, verifies the common
subtraction and differentiated remainder, and proves the first-order
coefficient is strictly nonzero. It separately checks the primary-source
global gauge normalization. The QCD insertion exclusion remains conditional
on the explicitly unproved uniform locality/global-state hypotheses.

These are rigorous statements for defined models and normalized operator
claims. They do not establish global novelty or solve alpha. The unresolved
physical requirement is the full, commonly regulated neutral QCD+QED metric
functional at fixed nonzero charge, with independently matched proton
response and control of its global/state sector. Neither a local charged
wall coefficient nor a first derivative at zero charge supplies it.

The phase assessment selects the completed computation records and pins
these separate hand/source reviews. All assigned work is saved. The original
fine-structure goal remains open; no global novelty claim or automatic
worker continuation is implied.
