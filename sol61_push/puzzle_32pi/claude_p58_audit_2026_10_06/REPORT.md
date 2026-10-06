# Claude p58: verified QUMOND bound, exact tail discriminator, restricted operator bridge

The raw p58 quadrupole is reproduced independently: Q2=2.19473223e-26 s^-2 at a0=9.3603e-11 m/s² and observed external field ge=2.146e-10 m/s². Its historical standardized residual is6.316 using the 2014 fit. Its kappa limits are accurate coarse interpolations for the stated UNCUT QUMOND kernel. Neither the number nor the inference transfers automatically to every modified-potential action. In particular, p58 does not evaluate our nonlinear projected-star operator or the nonminimal scalar calibration.

Two exact additional discriminants are derived here. First, the projected operator agrees with QUMOND at first order in a declared weak-modification expansion, but has an explicit nonzero second-order angular response difference. Second, at fixed physical external field, uncut QUMOND has Q2 proportional to a0 as a0 tends to zero, while the same finite-T QUMOND cutoff has Q2 proportional to a0³. Both coefficients follow from exact Mellin moments, not a numerical tail fit. These are operator tests; no coefficient32pi is selected.

## Authenticated ancestry and source scope

The requested Claude commits are3df87c31a0ab35b1485b125e14993909601d582c (p58) and536e8d160573ad2c40a4de519369642a9ab20344 (master action). Current bytes and actual concurrent HEAD are pinned in provenance.json. The p58 raw script imports qumond_efe_multipole.Field and supplies nu−1=1/[y(sqrt(1+1/y)+1)]. It does NOT include the T=128.915 cutoff. It fixes observed ge, solves e nu(e)=ge/a0, evaluates ten a0 values, and log-interpolates three Q2 thresholds. Its monotonicity assertion is ten-point evidence, not an all-a0 theorem. Its kappa convention is a0/(2*9.3603e-11), with the vacuum-density denominator held fixed. Those data and conventions are conditional inputs, not a new vacuum/source derivation.

The nearest p57 script explicitly distinguishes uncut and finite-cutoff kernels and reports almost equal Q2 at the reference a0. Its orbit integration is not rerun here. The master-action commit changes a tidal switch; this audit does not assume that switch implements p58's QUMOND equation. Only the named p58/p57/solver/README source scope and our relevant projected/nonminimal reports were examined; this is not a survey of all Claude activity.

Primary observations were reopened at exact versions: Hees et al., arXiv1402.6950v2, footer29April2014, eqs(2),(3),(6),(12); and Park et al., arXiv2602.17884v2, manuscriptdated29July2026, SecIII recommended fit. The first gives Q2=(3±3)e-27 s^-2; the latter gives(1.6±1.8)e-27 s^-2, both one-sigma estimates. The first explicitly separates nonlinear Poisson and QUMOND away from spherical symmetry. Its fitted quadrupole is a physical metric/planetary template, not an interpolation-kernel theorem. Exact source URLs and checked locators are in sources.json. No full paper copy is redistributed or claimed locally hashed.

## Independent coefficient reconstruction

Use Claude's force and potential conventions: Newtonian force G=−GM rhat/r²+a0 e zhat; psi=−Phi_phantom; Phi_Q=−Q2 r²P2/3. Set rM=sqrt(GM/a0), f(y)=nu(y)−1. The exact point-source uniform-field QUMOND Green coefficient is

Q2=−9a0/(4rM) integral f(y)sqrt(y)F(e/y)dy
  =−9a0 e^(3/2)/(4rM) integral f(e/q)q^(−5/2)F(q)dq,

F(q)=−2/(35q³){P(q)/sqrt(1+q)−sgn(1−q)R(q)/sqrt(|1−q|)},
P=2q³+q²+6q+12, R=−2q³+q²−6q+12.

This is the previously audited full Green weight, not an extrapolation of the q<1 expression. F~q²/10 at zero, F~−q^(−7/2) at infinity; its two shell singularities at1 are integrable inverse square roots. Thus K(s)=integral q^(s−1)F(q)dq is absolutely convergent for−2<s<7/2.

For s=−1/2 the substitutions z=sqrt(1+1/q), sqrt(1/q−1), sqrt(1−1/q) give respectively the plus, lower and upper transformed primitives

Splus=Shigh=−24z^7/7+12z^5−50z³/3+10z,
Slow=−24z^7/7−12z^5−50z³/3−10z.

For s=3/2 they instead give

Splus=Shigh=−8z³+12z+2z/(z²−1),
Slow=−8z³−12z+2z/(z²+1).

For each s, keep the COMMON finite cutoffs epsilon and Rcut before adding terms. The combined bracket is

Splus(sqrt(1+1/Rcut))+Shigh(sqrt(1−1/Rcut))
 +Slow(sqrt(1/epsilon−1))−Splus(sqrt(1/epsilon+1)).

It tends to80/21 and10 respectively. Multiplication by−2/35 gives exactly

K(−1/2)=−32/147, K(3/2)=−4/7.

The script differentiates all six primitives and evaluates both combined limits independently. No divergent beta pieces are split or assigned unrelated regulators.

## All-parameter asymptotic tail test within QUMOND

Let b(y)=sqrt(1+1/y)−1, so0<b(y)≤1/(2y) and yb(y) tends to1/2 at infinity. For the uncut kernel, observed ge fixes eta=ge/a0 and e=(sqrt(1+4eta²)−1)/2, hence e/eta tends to1. Pointwise e b(e/q) tends to q/2 and is bounded by q/2. The dominating integral q^(−3/2)|F(q)| is finite. Dominated convergence therefore yields

Q2_uncut ~ (12/49) a0 sqrt(ge/GM), a0→0 at FIXED ge>0.

For finite T>0, f_T(y)=b(y)/[1+(y/T)²]. The external solve remains e nu_T(e)=eta; e/eta tends to1 on its admitted high-field branch. Pointwise e³f_T(e/q) tends to T²q³/2, and is bounded by that same expression because1/[1+(y/T)²]≤T²/y². The dominating integral q^(1/2)|F(q)| is finite. Consequently

Q2_cut ~ (9/14) T² a0³/[sqrt(GM) ge^(3/2)].

This is a fixed-T mathematical limit, not an assertion that a dynamical cutoff stays fixed as an action parameter is changed. It includes the QUMOND cancellation shell through the absolutely integrable exact weight. It is NOT obtained by a uniform pointwise expansion at the physical Newtonian saddle. Nor does it prove the same limit for the nonlinear projected operator. The two limits a0→0 and T→infinity do not commute at the level of Q2/a0.

At the reference a0, the independent finite-T integral gives2.19859190e-26 s^-2, agreeing with p57's cutoff comparison. Thus the cutoff scarcely changes that particular QUMOND point even though it changes the fixed-T asymptotic scaling. A finite moment in the cutoff model does not make p58's uncut kernel itself have a finite vacuum moment.

## Actual projected operator: exact comparison, not blanket escape

At the frozen leading pressureless weak-static source order, our projected and shared-leaf actions vary to

Delta Phi_plus=4pi Gt rho,
div[mu_star(x)grad Phi_star]=4pi Gt rho,
Phi_visible=(Phi_plus+Phi_star)/2,
x=(2nu(y)−1)y, mu_star(x)=y/x.

These equations are spherical-kernel matched but generally not QUMOND. With a uniform aligned background, the visible external field is ge=(gNe+gstar,e)/2 and gstar,e=a0 x_e. The exact inner projected quadrupole is HALF the AQUAL-star quadrupole computed with this mu_star and that star external field. Since mu_star~x/4 at zero, one can equivalently use ordinary AQUAL normalization a_star=4a0 and mu_bar(z)=mu_star(4z). This is an exact change of units/function for the frozen NR BVP; it does not assign its unknown quadrupole from nu alone.

There is nevertheless a constructive perturbative comparison. Write nu=1+epsilon f at fixed a0. Then mu_star=1−2epsilon f+O(epsilon²). For an admitted differentiable source solution Phi_star=Phi_N+epsilon phi1+..., away from degenerate field zeros, variation gives

Delta phi1=2 div[f(|grad Phi_N|/a0)grad Phi_N].

Visible half cancels the factor2, exactly reproducing QUMOND's first-order potential equation and its boundary data at that order. This Born comparison is conditional on perturbative source admission; it is not a global nonlinear existence/differentiability theorem across a Newtonian saddle. It supplies a reason the operators can agree to leading weak modification without being identical.

An exact local external-field Fourier comparison exposes the next order. Let a=2nu_e−1, d=2y_e nu'_e, t=(khat·ehat)², with a>0,a+d>0. The actual visible projected response multiplier relative to the Newton potential is

P_proj(t)=1/2+a(a+d)/[2(a+d−dt)],
P_QUMOND(t)=(a+1+dt)/2,
P_proj−P_QUMOND=−d²t(1−t)/[2(a+d−dt)].

They agree at parallel/perpendicular wave vectors and at first order in d; they disagree strictly at oblique directions whenever d!=0. The witness a3,d−1,t1/2 gives−1/20. This comparison is derived from the inverse star constitutive Jacobian, including its longitudinal eigenvalue, rather than declaring every modified-potential theory equivalent. It is a far/external-dominated diagnostic; it does not determine the inner Solar Q2.

The already peer-reviewed projected Solar BVP estimated Q2≈2.83e-26 at this same cutoff/reference normalization, with source-radius/domain/refinement tests but no certified continuum or full covariant admission. This independent operator calculation offers no apparent numerical suppression at that reference point; the action is not exempt simply because QUMOND is inapplicable. Its empirical uncertainty/model scope still forbids turning that estimate into a precise significance or a universal exclusion.

For the nonminimal action, freezing u additionally requires the declared source hierarchy. Its ordinary-only light scalar changes Newton calibration, a0obs=a0J/(1+s),0<s<1/6 in d4, and adds a conformal force. Cutoff feedback, calibrated Galactic boundary fields and source-metric/light-propagation matching must be derived before p58's kappa bound can be applied. A quadratic scalar source response is not a new screening proof. The full shared-leaf and foliation constraints remain separate from force-PDE ellipticity.

## Numerical audit and statistical limits

The independent42-digit weight quadrature reproduces the ten-point monotonic trend. Direct root solving gives historical upper thresholds kappa0.109616,0.170220,0.235562 instead of p58's coarse log-interpolated0.110,0.171,0.236. Using the updated2026 CENTRAL VALUE PLUS1 OR2quoted sigmas gives conditional uncut-QUMOND thresholds0.060386 and0.094163. The reference standardized residual is11.304 under that newer fit, compared with historical6.316. These are fixed-model scalar pulls and central-plus-sigma thresholds, NOT complete hypothesis-test probabilities, marginalized Galactic-field constraints, or one-sided confidence limits. No experimental likelihood is rerun and the physical nonminimal/projected model is not claimed to have these numbers.

checks.py uses exact primitives/operator identities, independent bounded quadrature/root solving, and a small-a0 corroboration. A preliminary development run24/24 preceded adding two exact angular comparisons; final scientific checks/current manifests supersede it. Controls falsely equate the distinct operator multiplier, transfer the uncut linear tail to fixed T, or replace the updated fit by the historical pull. Each tests a computed nonzero quantity. No original Claude solver or astronomical integration is executed, and no source files outside this folder are changed.

The surviving result is strong conditional tension for the specified QUMOND kernel plus exact operator/tail comparisons. The overreach is treating a single spherical kernel or the words modified potential as proof of its nonspherical Solar coefficient and claiming every vacuum integral is therefore ruled out. A theory with a new screened field operator needs its own conserved sourced metric and quadrupole calculation. A successful repair would still need an independently selected vacuum normalization; none is supplied here.
