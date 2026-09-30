# 32pi investigation: coefficient and orientation constraints

**Not solved.** None of the constructions below derives 32pi. The strongest additional result is an exact lower bound on the oriented dipole amplitude product, together with a three-dimensional orientation obstruction for a simple passing stream. These make the proposed internal-response route more falsifiable. They do not establish that no theory can produce the coefficient.

Base checkpoint and success criteria are in `PUZZLE_32PI_CONTRACT.md`. The existing puzzle campaign's latest README, corrections, evidence lane, K, X1/X2/X3, W, Y and memory-referee summaries were reviewed. Most existing routes already establish that locating 32pi in another formula is insufficient. No global literature novelty claim is made; existing lanes were not all independently rerun here.

## The actual unknown

In units c = 1,

    Lambda = 32 pi a0²  <=>  G rho_Lambda = 4 a0².

Restoring units, a0 = (c/2) sqrt(G rho_Lambda) for vacuum mass density. The Einstein conversion Lambda = 8piG rho_Lambda/c² accounts for the 8pi; the unresolved physical coefficient is 4. An action must connect the **absolute** vacuum energy and the **measured response** acceleration. Neither an Euler number nor a chosen horizon area identifies that connection.

Exactness is a conjecture, not an observational conclusion. The repository's current coefficient-evidence lane finds nearby alternatives indistinguishable at present systematic precision. This session did not refit those data. Total-density and vacuum-density footings must remain separate.

## Route 1: reconstruct the exact P2 action

For the spherical target g² = b² + a0 b, put x = g/a0. Its AQUAL inverse is

    mu(x) = [sqrt(1+4x²)-1]/(2x).

For L = -a0² F(y)/(8piG), y = x², an exact primitive with the chosen reference F(0) = 0 is

    F(x²) = (x/2)sqrt(1+4x²) + asinh(2x)/4 - x.

It has F(x²) = (2/3)x³ + higher powers near zero, and

    F(x²)-x² = -x + log(4x)/4 + 1/8 + o(1)

at large x. Thus a condition that the Newtonian-subtracted action approach a finite constant cannot normalize this exact P2 action. Adding an arbitrary C leaves the force equation unchanged. If a completion interprets that constant as vacuum energy, rho_v = a0² C/(8piG), it requires C = 32pi as an additional condition.

This is not a new offset no-go: lane K already analyzes the same inverse interpolation and its divergent tail. The contribution here is the closed primitive tied explicitly to the target used in our support/assembly work. AQUAL realizes the algebraic relation in spherical symmetry; this is not a proof of its full nonspherical or covariant realization.

## Route 2: the dipole model gives a quantitative selection obligation

The published local coefficient is a0 = -8c² eta_1 eta_2 eta_3/(3 alpha k_2 k_3 sin(theta)). Its linear cancellation assumes sum eta_a^-2 approximately one; its vacuum scale is only an order-of-magnitude statement. Source: [Blanchet and Seraille, arXiv:2502.14686v2, Eqs. (2.9), (3.26), (3.35)](https://arxiv.org/pdf/2502.14686). Initial-state universality is left unresolved there.

For an exact calculation, impose sum eta_a^-2 = 1 and introduce the **extra, unproved** premise Lambda = q/alpha². Define K = |k_2 k_3 sin(theta)| and E = |eta_1 eta_2 eta_3|. Eliminating alpha gives

    c⁴ Lambda/a0² = 9 q K²/(64 E²).

The cancellation constraint itself limits E. Set u_a = eta_a^-2 > 0. Since sum u_a = 1, AM-GM gives product u_a <= 1/27, hence E² >= 27. Therefore

    c⁴ Lambda/a0² <= q K²/192.

To obtain 32pi one necessarily needs

    K² >= 6144 pi/q,

with equality only for equal absolute charge ratios. At q = 1 this means K >= 138.93144. If |sin(theta)| = 1 and k_2 = k_3 in magnitude, each must be at least 11.78692. Conversely q = 1 and both |k_a| <= 1 give a coefficient at most 1/192, a factor 19301.95 below 32pi. Choosing q or the amplitudes to meet the bound is a fit, not a derivation.

This does not prove that large amplitudes are inconsistent. The k_a are relative amplitudes; sufficiently small g can keep physical fields perturbative. A full EFT consistency check at the selected state remains open. Nor must q be one: its value is another unclosed obligation. Unequal charge ratios only strengthen the bound. For approximate cancellation S = sum eta_a^-2, the corresponding bound is K² >= 6144pi/(q S³); near S = 1 it changes little, while a large S restores a large unwanted linear response.

Independent phase averaging does not select the coefficient. For uniform relative phase, mean sin(theta) = 0, half the phases have the wrong sign, and mean 1/|sin(theta)| diverges. Averaging sin² yields 1/2 but has relative standard deviation 1/sqrt(2); it averages a squared coefficient, not the physical induction. For a0 = A/|sin(theta)|, optimizing A to maximize the fraction within a relative window epsilon gives

    fraction_max = 1 - (2/pi) asin[(1-epsilon)/(1+epsilon)]

conditional on the attractive sign. The maximum is attained at A/a0_target = 1-epsilon: below this point both sine bounds grow and the probability increases; above it the upper bound is clipped to one and the probability decreases. Even at epsilon = 0.13 the maximum is 44.06%, or 22.03% without conditioning the sign. This is a diagnostic for the specified random-phase hypothesis, not an observational likelihood or exclusion of the dipole model.

## Route 3: a simple same-field vacuum extremum loses its kinetic term

To test whether a field could set both vacuum energy and response without prescribing their ratio, consider the restricted classical gauge action L = -V(X), X = sum F_a^{mu nu} F_{a mu nu}/4. Take an isotropic purely magnetic background (for example, three equal orthogonal Abelian magnetic fields), so X = sum B_a²/2. Metric variation gives

    rho = V(X),  p = -V(X) + (4/3) X V'(X).

The pressure identity is consistent with [Benaoum et al., EPJC 83, 367 (2023), Eqs. (7)-(9)](https://link.springer.com/article/10.1140/epjc/s10052-023-11481-3). We independently differentiate the metric-dependent action for an explicit magnetic triad and a quadratic V, rather than relying on that paper's perturbative-health conclusions.

At nonzero finite X, exact rho+p = 0 requires V'(X) = 0. Electric perturbations have X = X_B - sum E_a²/2, so

    L = -V(X_B) + V'(X_B) sum E_a²/2 + higher terms.

The electric Hessian is V'(X_B) times the identity. At the purported magnetic vacuum it vanishes. This is loss of the ordinary quadratic electric kinetic term, not a complete proof of instability or strong coupling: constraints, higher derivatives and additional operators require their own analysis. It prevents this minimal magnetic extremum from being accepted as a healthy response mechanism on the calculation alone.

Moreover V -> V+C shifts the vacuum height without changing the stationary point or this Hessian. A vacuum extremum therefore does not fix 4. The result excludes neither electric condensates, ghost condensates, extra invariants, derivative operators nor the full non-Abelian dipole action. Magnetic background evolution and Bianchi identities would be additional obligations even if the algebraic test passed.

## Route 4: extending a single stream to an entire galaxy

A planar calculation with g in one fixed positive direction does not ensure an attractive response in all spatial directions. Consider the most general rotation-covariant **linear** response matrix built from one incident velocity v and scalar coefficients:

    xi_a = A_a g + B_a v(v dot g) + C_a (v cross g).

For g = (g,0,0), direct calculation gives

    (xi_2 cross xi_3)_x = g² v_x(v_y²+v_z²)(B_3 C_2 - B_2 C_3).

The longitudinal contribution vanishes for g parallel or perpendicular to v, reverses under v -> -v, and cancels in a symmetric counter-stream ensemble with fixed coefficients. If the physical dipoles are polar and there is no pseudoscalar response coefficient, parity requires C_a = 0 and the longitudinal cross term vanishes everywhere in this linear subclass.

More generally cross(M_2 g, M_3 g) is even under g -> -g for fixed matrices M_a. The isotropic deep-MOND induction |g|g/a0 is odd. They cannot agree globally at nonzero response with fixed coefficients. The state must rotate/reselect its orientation with g, or the constitutive relation must involve a nonlinear branch or spatial dynamics. This is an exact local obstruction under the declared assumptions, not an exclusion of a physical stream. It exposes the additional selection obligation concealed by a one-dimensional favorable initial state.

## Current decision and executable continuation

The puzzle remains OPEN. The meaningful additional outputs are the charge-constrained amplitude bound, a random-phase discriminator, the minimal magnetic kinetic degeneracy, and the stream orientation obstruction. The primitive/offset result reproduces a known restriction in the prior campaign.

For the active-medium direction to become a coefficient derivation, it needs all of: a predicted vacuum height q; a dynamical value of the oriented amplitude product K; coherence maintenance; and a spatial orientation rule that produces the same attractive response around a galaxy. Their selected values must yield 9qK²/(64E²) = 32pi without setting that equality as an input. Extra degrees of freedom might solve these obligations, but adding them without a selection principle does not constitute progress on the number.

Next executable package, once a specific transport action is supplied or independently constructed: evolve its correlation tensor with the stream in a nonuniform gravitational field, track the energy exchanged with baryons, and test invariance under reversal/rotation of the incident stream. Do not choose a driving amplitude, phase or vacuum offset from the desired coefficient. A failed spatial test should be kept even if a local fit works. This continuation is **open**, not exhausted; it needs a defined action and pump, neither of which this session has derived. Quantum/RG selection is deferred for the same reason: no specified new beta functions to calculate beyond the existing Q/U lanes.

## Verification

`coefficient_constraints.py` supplies 32 deterministic symbolic/finite checks, including independent metric variation and a direct full-Lagrangian Hessian. A control halves the required amplitude product squared and must fail the target check. The exact AM-GM inequality and physical interpretation are the prose arguments above; finite success counts are not proofs of 32pi. Bounded runs, actual versions, input/output hashes and exit statuses are recorded in `runs/coefficient/` and `runs/coefficient_mutation/` and validated with the computation-audit manifest validator. Source PDFs/article pages were verified online; no local copies were downloaded.
