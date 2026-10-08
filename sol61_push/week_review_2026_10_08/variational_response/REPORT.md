# A variational near match to the quadrature law

The exact fluctuation state representing the quadrature law uses **28/27 of the minimum gradient energy at fixed deep-MOND response**. An independently specified minimum-gradient principle selects an exponential amplitude and a different, explicit interpolation law. It shares the quadrature law's deep limit and high-acceleration offset. In a bounded numerical comparison their accelerations differ by at most about **1.2207 percent**.

This is a constructive mathematical result under a stated averaging rule, not a derivation of that rule from microscopic physics. The same analysis gives two sharper restrictions: a state-independent upper bound on the coefficient under the earlier operator-based vacuum dictionary, and an obstruction to obtaining MOND by using the averaged magnitude directly as field energy. The physical \(32\pi^2\) target remains open.

Base: commit 2efa706de5ba0a138276bd07fc07ebc5c55ff95a, continuing the [halo and vacuum review](../REPORT.md). The prior [inverse construction](../../TONIGHT_32PI_RESULTS.md) and its script fluctuation_response_inverse.py supply the target distribution being compared. The present calculations do not import their numerical outputs. No claim of literature-wide novelty is made.

## The declared response and state class

Work in three-dimensional acceleration configuration space, in units \(c=1\). The radial variable \(R=|\boldsymbol\xi|\) is a fluctuation acceleration magnitude, not a physical galactic radius. Let \(\psi\in H^1(\mathbb R^3)\) be normalized and isotropic, and define

\[
p(R)=4\pi R^2|\psi(R)|^2,\qquad
q=\mathbb E(R^{-1}),\qquad
K=\int_{\mathbb R^3}|\nabla_\xi\psi|^2\,d^3\xi.
\]

Require \(\mathbb E R<\infty\) to define the separate mean magnitudes. The hypothetical inverse response is

\[
b(g)=\mathbb E|\boldsymbol\xi+g\mathbf e|-\mathbb E R.
\]

Here \(b\) denotes the baryonic acceleration and \(g\) the response acceleration only when this prescription is adopted. It is not the mean-vector equation of an additive random force.

Angular integration gives

\[
\mathbb E_{\rm angle}|\boldsymbol\xi+g\mathbf e|=
\begin{cases}
R+g^2/(3R),&R\ge g,\\
g+R^2/(3g),&R\le g.
\end{cases}
\]

Consequently \(b(g)\sim qg^2/3=g^2/a_0\), with \(a_0=3/q\). Minimizing gradient energy at fixed \(q\) is therefore a precise variational proposal at fixed deep response. It does not fix the value of \(q\) relative to cosmology.

## An exact minimum and its unique state

For a normalized smooth state and any real \(\alpha\), integration by parts with \(\nabla\cdot\widehat{\boldsymbol\xi}=2/R\) gives

\[
\int|\nabla\psi+\alpha\widehat{\boldsymbol\xi}\psi|^2
=K+\alpha^2-2\alpha q.
\]

At \(\alpha=q\),

\[
\boxed{K-q^2=
\int|\nabla\psi+q\widehat{\boldsymbol\xi}\psi|^2\ge0.}
\]

The identity extends to \(H^1\) by smooth approximation and the Coulomb form bound that the same inequality supplies. More explicitly, first establish the unnormalized bound \(\int |f|^2/R\le\|f\|_2\|\nabla f\|_2\) on smooth functions; weighted Cauchy-Schwarz then makes that quadratic form continuous in the \(H^1\) norm.

Equality requires \(\nabla\psi=-q\widehat{\boldsymbol\xi}\psi\). Up to a constant phase, normalization gives the unique optimizer

\[
\boxed{\psi_q(R)=\sqrt{\frac{q^3}{\pi}}e^{-qR}.}
\]

It is bounded and has finite gradient energy. It has a cusp at the origin as a Cartesian function, so it is an \(H^1\) optimizer, not a globally smooth amplitude. If smoothness is additionally required, smooth approximations approach the same infimum. Its radial flux \(R^2\psi'\) vanishes at zero: there is no point delta in its Laplacian.

This optimizer was obtained without inserting the quadrature response. Its Coulomb equation
\[
(-\Delta-2q/R)\psi_q=-q^2\psi_q
\]
is a consequence of the variational constraint. Calling that equation a fundamental vacuum Hamiltonian would be an additional physical assumption.

## The quadrature state lies close to this minimum

The earlier exact representation of \(b_{\rm P2}(g)=\sqrt{g^2+h^2}-h\), with \(a_0=2h\), is

\[
|\psi_{\rm P2}(R)|^2=\frac{15h^4}{8\pi(R^2+h^2)^{7/2}}.
\]

Independent beta-integral calculations give

\[
q_{\rm P2}=\frac{3}{2h},\qquad K_{\rm P2}=\frac{7}{3h^2},\qquad
\boxed{\frac{K_{\rm P2}}{q_{\rm P2}^2}=\frac{28}{27}.}
\]

Thus its energy exceeds the exact minimum by \(1/27\), or 3.7037 percent. The fraction \(q^2/K\) is \(27/28\). These statements use the same fixed deep-response constraint for both states.

At \(q=1\), direct radial quadrature gives an amplitude overlap of 0.9953218631, squared overlap 0.9906656111. This is an ordinary normalized function-space comparison, not a quantum fidelity measured in nature or a guarantee that the response laws are uniformly close.

## The law selected by the minimum

Write \(\beta=q\), \(z=\beta g\). The optimizer's radial density is \(p(R)=4\beta^3R^2e^{-2\beta R}\). Exact integration of the angular formula yields

\[
\boxed{
b_{\rm opt}(g)=\frac1\beta
\left[z-\frac32+\frac1z-
\left(\frac12+\frac1z\right)e^{-2z}\right],
\qquad a_0=\frac3\beta.}
\]

The expression has a removable singularity at \(z=0\). Its limiting expansions are

\[
b_{\rm opt}(g)=\frac{g^2}{a_0}
-\frac95\frac{g^4}{a_0^3}
O(g^5/a_0^4),
\]
\[
b_{\rm opt}(g)=g-\frac{a_0}{2}+\frac{a_0^2}{9g}
\text{exponentially small terms}\quad(g\to\infty).
\]

P2 instead has
\[
b_{\rm P2}(g)=\frac{g^2}{a_0}-\frac{g^4}{a_0^3}
O(g^6/a_0^5),\qquad
b_{\rm P2}(g)=g-\frac{a_0}{2}+\frac{a_0^2}{8g}
O(g^{-3}).
\]

The common deep coefficient and high-field offset are exact; the laws are not identical. The offset \(a_0/2\) follows here from \(\mathbb E R=3/(2\beta)\). It does not identify this half with the vacuum coefficient.

For equal \(a_0=1\), direct inversion on 161 log-spaced baryonic accelerations \(10^{-8}\le b\le10^8\), followed by a local numerical refinement, finds the largest relative excess near \(b/a_0=0.2162118\):

\[
g_{\rm P2}/a_0=0.5127956,\quad
g_{\rm opt}/a_0=0.5190552,\quad
g_{\rm opt}/g_{\rm P2}-1=0.0122068324.
\]

That is 0.0052693 dex in acceleration, or 0.0026346 dex in circular speed at fixed radius. It is the maximum found in this bounded numerical comparison, not a rigorously certified global maximum. No galaxy data have been fit. The alternative retains the high-field acceleration offset, so the existing need to test or screen that behavior is not removed.

The angular expression has a strictly positive first derivative for \(g>0\). Hence \(b_{\rm opt}>0\) and \(b_{\rm opt}'>0\). Defining a static field energy by \(W'(g)=b_{\rm opt}(g)\) gives the usual positive radial and tangential ellipticity eigenvalues \(b_{\rm opt}'\) and \(b_{\rm opt}/g\) away from zero field. This supplies a static constitutive construction; the integration rule itself remains an added physical prescription.

## A sharp conditional vacuum bound

Consider specifically the earlier operator dictionary

\[
a_*^2K=1,\qquad \Lambda=\lambda a_*^2,\qquad \lambda>0.
\]

These are assumptions to test, not statements established about quantum gravity. Combining them with the response rule and the sharp inequality gives

\[
\boxed{\frac{\Lambda}{a_0^2}
=\frac{\lambda q^2}{9K}\le\frac{\lambda}{9}.}
\]

This applies to every normalized isotropic \(H^1\) state in the declared response class, not just the gamma family or the two states above. It is sharp: the exponential amplitude saturates it.

For the inherited illustrative \(\lambda=3\), the upper bound is \(1/3\); the desired \(32\pi\) is larger by \(96\pi\), about 301.59. Reaching the target under this dictionary requires at least \(\lambda=288\pi\). Selecting that value would reintroduce the coefficient as an input. The exact P2 state gives \(3\lambda/28\), slightly below the maximum.

The different variance dictionary \(a_*^2=2\mathbb E R^2\) gives \(2\lambda/3\) for the optimizer and \(3\lambda/4\) for P2. The sharp operator bound does not apply to that dictionary. Keeping this distinction explicit prevents a change of vacuum normalization from being mistaken for a physical derivation.

## Why the averaged magnitude cannot simply be the field energy

There is a further exact obstruction for the declared fixed state class. Define the inverse-moment quadratic term and its remainder using the angular formula:

\[
b(g)=\frac{qg^2}{3}-D(g),\qquad
D(g)=\frac1{3g}\int_0^g\frac{(g-R)^3}{R}p(R)\,dR\ge0.
\]

For every \(H^1(\mathbb R^3)\) state,
\[
J=\mathbb E(R^{-2})\le4K<\infty.
\]
This follows by completing the second square
\[
\int\left|\nabla\psi+\frac{\widehat{\boldsymbol\xi}}{2R}\psi\right|^2
=K-\frac14J.
\]
The identity is established first on smooth functions away from the origin and extended by approximation. The divergence needed is \(\nabla\cdot(\widehat{\boldsymbol\xi}/R)=1/R^2\).

Since \(0<R<g\),
\[
0\le\frac{D(g)}{g^3}
\le\frac13\int_0^g\frac{p(R)}{R^2}\,dR\longrightarrow0.
\]

Also
\[
\partial_g\frac{(g-R)^3}{3gR}
=\frac{(g-R)^2(2g+R)}{3g^2R}
\le\frac gR,
\]
so \(D'(g)/g^2\to0\). Therefore
\[
\boxed{
b(g)=\frac{qg^2}{3}+o(g^3),\qquad
b'(g)=\frac{2qg}{3}+o(g^2).}
\]

Suppose a positive fixed dimensional normalization \(\eta\) is used to turn this average into field energy directly, \(W(g)=\eta b(g)\). Its field-equation flux is \(W'(g)\), which is linear at small \(g\), not the MOND flux proportional to \(g^2\). Canceling its leading quadratic energy term leaves a flux \(o(g^2)\), again without a nonzero MOND coefficient. In contrast, the imposed primitive \(W=\int b\,dg\) has the desired cubic leading energy. These are different actions.

The borderline escape makes the restriction sharp. If \(|\psi|^2\sim A^2/R\) at the origin, then
\[
D(g)\sim\frac{\pi A^2}{3}g^3,
\qquad
4\pi R^2|\psi'|^2\sim\frac{\pi A^2}{R}.
\]
The desired power appears only outside this finite-gradient class, with logarithmically divergent gradient energy in this example. After subtracting the quadratic term, the direct energy's cubic coefficient is also negative for positive \(\eta\). This is not a universal exclusion of singular states with a different operator or measure.

The theorem concerns a fixed isotropic state and this direct mean-norm energy. It does not cover source-dependent state changes, additional derivative operators, nonlocal inertia, or an independently justified primitive response action.

## Research decision and evidence

The work executed three distinct tests: a sharp variational inequality, construction and comparison of its selected interpolation law, and a direct-action interpretation of the same statistical quantity. The first two yield exact mathematics and a close conditional alternative to P2. The third rules out the simplest direct-energy interpretation for the stated regular state class. None selects the vacuum normalization.

The remaining physical obligation is narrower: derive the response functional and vacuum stress from the same source-coupled dynamics. A new proposal must specify why the action uses the primitive response, or demonstrate how source-dependent states evade the direct-energy theorem. Merely changing a radial distribution within the fixed finite-gradient/operator dictionary cannot reach the target at the inherited small \(\lambda\). That route is closed under its stated hypotheses. Source-dependent dynamics and different vacuum dictionaries remain open, pending a specified physical action rather than a target-fitted operator.

The main calculation passed all 35 checks: symbolic moments and expansions, independent radial response quadratures, gamma-family square identities, and the bounded force comparison. Its mutation asserts the false strengthened bound \(q^2\le0.99K\), which must fail on the optimizer. The action calculation passed all 16 constituent checks; its mutation wrongly asserts a positive borderline cubic coefficient. The universal arguments are the proofs above, not the check counts.

Both deliberately false controls failed exactly their intended assertion (34/35 and 15/16, exit 1). All four execution manifests validated with input and output hashes. Execution commands, software versions, input and result hashes, numerical bounds and exit codes are stored in the four sibling run directories and their manifests. The contract explicitly records that the formula and approximate numerical peak were explored before execution; this was not a blind or preregistered discovery. Review is adversarial self-review, not an independent-agent certificate. Earlier files and results were preserved.

The saved [response comparison plot](response_comparison.png) displays the computed acceleration difference. It is generated from the retained main results, not an additional empirical test.
