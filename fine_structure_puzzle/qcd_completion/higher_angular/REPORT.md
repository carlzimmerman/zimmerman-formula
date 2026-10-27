# Static higher angular family: fixed-J result and summation boundary

For every fixed integer J>=2, the specified static BPS/unbroken auxiliary
comparison has

\[
\boxed{\log Z_J=(2J+1)\left[-2x+(2J+3)\log x+c_J
                  +\frac{J(J+1)-1}{x}+O_J(x^{-2})\right].}
\]

Here x=m_W R is varied at fixed small circle and fixed asymptotic m_W.
The vector wall is the actual relative mixed wall, with nine Dirichlet and
three reduced normal Robin conditions u'+u/x=0. The ghost wall is framed
Dirichlet. The comparison saddle is K=1,h=0. It has different holonomy from
the BPS saddle and is an auxiliary reference; the result is not a physical
same-holonomy QCD subtraction or an electromagnetic coefficient.

## Derivation and hypotheses

The generic vector centrifugals were derived from the actual self-dual
four-vector Pauli block, rather than inferred from scalar intertwiners.
For charge q=+/-1, let L be monopole angular momentum, w=sigma dot n,
kappa=sigma dot L+1, and lambda=k+1/2. The Cartesian curvature term gives

\[
A=L^2-2qw=\lambda^2-(\kappa+2qw),\qquad
\kappa^2=\lambda^2,\quad \{\kappa,w\}=-2q,\quad w^2=1.
\]

Hence (kappa+2qw)^2=lambda^2 and the active-spinor eigenvalues are
lambda(lambda-1),lambda(lambda+1). Coupling the spectator spin 1/2 to
grand spin J gives, per charge,

\[
J(J-1),\quad J(J+1),\quad J(J+1),\quad (J+1)(J+2).
\]

The monopole harmonic restriction L>=|q| can be seen directly by realizing
the charged angular sections as functions on SU(2) with fixed right U(1)
weight q: a spin-L representation contains that weight exactly once for
L=|q|,|q|+1,... . At J1 the lowest active-spinor space has only one branch;
the absent centrifugal is C1=2. This explains the exceptional six, rather
than eight, charged vector channels there and reproduces the supplied J1
Cartesian spectrum without assuming its continuation to higher J.

At J>=2 there are eight charged and four neutral vector channels. The
neutral centrifugal list is the same four-entry list, with each entry
appearing once. The free origin orbital multiplicities across
l=J-2,...,J+2 are (1,3,4,3,1), giving twelve channels and reference boundary
power 12J+9. Charge separation preserves the normal wall projection: its
rank is two in the charged space and one in the neutral space.

For a charged growing zero-energy mode of centrifugal c,

\[
g_c=\frac{e^x}{x}\left[1+\frac{2-c}{2x}+O(x^{-2})\right],
\qquad
g_c'+g_c/x=\frac{e^x}{x}\left[1+\frac{2-c}{2x}+O(x^{-2})\right].
\]

The charged vector sum of these first coefficients is 6-4J(J+1). The
actual neutral radial/electric wall determinant has nonzero leading
constant -(J+1)(2J+3)/(2J+1), and the four neutral wall powers give 4J+3.

The global input is the whole-space kernel proof in
`../reviews/kernel_rank/RAW_DERIVATION_v1.md`: phase J0 and translations J1
exhaust the L2 kernel. All neutral decays are L2 at J>=2, since their
smallest orbital number is J-1>=1. Therefore the regular-origin and
no-growing Lagrangians intersect trivially, and the full growing connection
map is invertible. Its charged part has rank eight, leaving four independent
neutral growing directions. Neutral scattering changes the wall determinant
only at relative x^{-(2J-1)}, starting at x^-3.

For each fixed J the exact coefficient remainder is exponential times
polynomial/logarithmic factors after the charged/neutral far operator is
removed. This follows from the BPS profiles and finite-dimensional angular
matrices. Charged growing solutions can induce polynomial neutral tails;
the proof uses the actual mixed-wall Schur complement to remove their
effect on algebraic determinant coefficients. It does not simply discard
these tails. The charged block inverse is O_J(x e^-x), the charged trace
of growing-free companions is exponential, and the remaining neutral block
has a polynomially bounded inverse. This is the fixed-J extension of the
explicit J1 remainder argument, not a J-uniform estimate.

Writing C_J=J(J+1), the separate determinants per magnetic component are

\[
\log D_{\rm vec,J}=8x-(8J+14)\log x+c_{\rm vec,J}
                     +(6-4C_J)/x+O_J(x^{-2}),
\]
\[
\log D_{\rm gh,J}=2x-(2J+4)\log x+c_{\rm gh,J}
                     +(2-C_J)/x+O_J(x^{-2}).
\]

The net Gaussian is det M/det H^(1/2). Exact Dirichlet-ghost/relative-vector
longitudinal pairing retains every positive finite-wall mode and introduces
no further scalar subtraction. This yields the boxed formula above.

The external whole-space index argument was source-audited in the kernel
lane; it was read and applied here, not independently source-audited again.
The local generic angular and wall derivation is given in
`RAW_DERIVATION_v1.md`.

## What can actually be summed

For every fixed finite N>=2, the full finite angular product has inverse
coefficient

\[
\boxed{A_N=\sum_{J=2}^N(2J+1)(C_J-1)
       =\frac{(N+1)^4-3(N+1)^2}{2}-2.}
\]

It diverges quartically as N grows. The nominal charged solution correction
is order J^2/x, so its unresummed series ceases to be a small-correction
series at J~sqrt(x), earlier than the centrifugal transition J~x.

There is a useful stronger statement at the first scale. For every integer
l>=1 the uncoupled charged growing solution is exactly e^x f_l(x)/x, where
f_l is a terminating polynomial in 1/x. If d=l(l+1)-2>0 and s=d/(2x), then

\[
\left|f_l(x)-e^{-s}\right|
\le \frac{e^s(s^3+6s^2)}{3d}.
\]

This explicit inequality proves uniformly for bounded s that
log f_l=-d/(2x)+O(d/x^2), together with the derivative bound needed by the
actual charged normal wall. Thus at J~sqrt(x) the solution can be resummed;
the logarithm is more controlled than the unresummed solution series alone
suggests. After ghost/vector cancellation, the exact finite-cutoff product
of these charged exterior growing factors obeys

\[
\sum_{J=2}^N(2J+1)E_J(x)=A_N/x+O_\kappa(N^4/x^2),
\qquad N\le\kappa\sqrt{x}.
\]

For N=floor(kappa sqrt(x)), this is A_N/x+O_kappa(1), and A_N/x grows as
kappa^4 x/2. The proof, exact factor definition and explicit constants are
in `UNIFORM_EXTERIOR_v1.md`. It controls the exterior factor, not the
complete regular-origin connection or the full neutral Schur complement
uniformly in J.

An angular heat regulator gives the convergent coefficient diagnostic

\[
\sum_{J\ge2}(2J+1)(C_J-1)e^{-\epsilon C_J}
 =\epsilon^{-2}-\epsilon^{-1}-12/5+O(\epsilon).
\]

The finite part -12/5 belongs to this chosen coefficient regulator. It is
not a finite physical coefficient, and no zeta assignment is used. A common
radial/angular regulator of the complete elliptic problem, its local bulk
and boundary heat subtractions, and physical vacuum matching remain
separate tasks. The next mathematical discriminator is a quantitative
J-uniform bound on the inverse regular-to-exterior growing connection map.

## Exact computations and provenance

`check_general_j_v1.py` and `COMPUTATION_CONTRACT_v1.json` define the first
bounded run. It checks the actual four-vector quaternion algebra, generic
charged characteristic polynomial, neutral mixed-wall determinant,
reference/log powers, and explicit Clebsch-Gordan counts for J2..20. It
also checks the frozen J1 Cartesian operator's far-field charged/neutral
characteristic polynomials and charge/normal wall commutation. The copied
operator input is immutable in `inputs_v1/j1_operator.json`.

Run `runs/general-j-001/manifest.json` has status `completed`, with 96 exact
checks passed. Its manifest validates against the current input bytes.

`check_exterior_v1.py` and `EXTERIOR_CONTRACT_v1.json` define the second
bounded run. It verifies exact charged Coulomb growing polynomials for
l1..30, factorial coefficients, the product-subtraction and Poisson-moment
identities used in the uniform bound, and exact angular partial sums.

Run `runs/exterior-001/manifest.json` has status `completed`, with 588 exact
checks passed. Its manifest also validates. Both runs used Python 3.9.6 and
SymPy 1.14.0, a 45-second wall cap and a 1-MiB log cap; no numerical fit,
floating ODE, stochastic sample or target coefficient entered. Execution
commands, Git state, software, runtime and hashes are recorded in the
manifests. The structural derivations, rather than finite checks alone,
supply the universal J statements.

The initial J1 operator read also exposed its coefficient, so this lane is
not coefficient-blind. The generic Pauli calculation was saved before
reading the coordinator's independently saved generic candidate; that
candidate was then checked and all counts, powers and coefficients agreed.

Final proofreading self-review covered the three newly authored derivation
and report files, including notation, charge multiplicities, origin powers,
wall ranks, asymptotic orders, and fixed versus uniform limits. No routine
typographical or mathematical-token corrections were required. This
proofreading receipt is not an independent correctness audit.
