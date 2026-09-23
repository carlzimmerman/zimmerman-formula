# September 13–20: an explicit constructive route and the claims that need repair

**Updated user constraint: no dark-matter particle.** The carrier recommendation
below is withdrawn as an answer to that closure request. Its bounded mathematical
results remain recorded, but they do not supply the requested particle-free
closure. The current answer and nine freshly compiled static-response theorems
are in [Particle-free result and exact closure gap](no_particle/ANSWER.md).

**The strongest new route found in this review is an action whose conserved cosmological background stays free of the environmental switch at quadratic order throughout its evolution.** We constructed such a carrier and checked exact identities, positive kinetic algebra and its first nonlinear limitation. This is a coherent partial advance, not full closure. The finite-gradient coupled theory, halo solutions and the normalization coefficient remain unresolved.

The review follows the previous September 19 checkpoint, using base commit `3aaed026d55f65b38733316cb63c432290a339e1`. The September 13–20 history contains 645 commits; twelve landed after the prior audited base. I reviewed that history and selected critical source chains, rather than reading every changed file. Detailed new work covers PD01–03, L290–293, the cluster-shape dependency in L41, and eight Navier–Stokes scripts, with a bounded RH/Yang–Mills source survey. The earlier BH* work was identified in the history but not independently re-audited here. Exact input hashes accompany every executed result. Existing research sources were left unchanged.

## 1. The useful reframing: protect a trajectory, then derive the constitutive law

The L290 carrier is specified near one velocity, `X=X0`, by

```text
p(X,Y)=p1(X-X0)+g(Y)(X-X0)^2/2.
```

Here `X=-grad(chi)^2>0` is the carrier's timelike kinetic invariant and `Y` is the MOND scalar's squared spatial gradient. Its switch vanishes to the desired order at `X=X0`. But conserved charge in an expanding universe requires `a³ p_X sqrt(X)=constant`, so X must evolve for fixed action coefficients. Inserting coefficients proportional to `a^-3` after varying the action does not solve that problem. The original square-root switch also becomes nondifferentiable at zero MOND gradient once X moves away from X0.

An explicit candidate replacement uses the original positive scales and normalizations:

\[
\mathcal B(Y)=\left[1+(Y/Y_d)^2\right]^{1/4},\qquad
m(Y)=1+\frac{A-1}{2\mathcal B(Y)},\qquad
p_\star(X,Y)=\frac{\rho_0}{2m(Y)}
\left[\left(\frac X{X_0}\right)^{m(Y)}-1\right].
\]

Assume `A>1`, `rho0,X0,Yd>0`, `X>0` and `Y>=0`. The key identities hold for **every** positive homogeneous X:

\[
p_{\star Y}(X,0)=p_{\star XY}(X,0)=0,
\qquad p_{\star X}+2Xp_{\star XX}=(2m-1)p_{\star X}>0.
\]

Since spatial-gradient invariant Y starts at second perturbative order, this switch starts at fourth order around the whole homogeneous trajectory. It contributes no new quadratic MOND-gradient term there. The carrier still couples to the metric.

At Y=0, exact conserved evolution normalized by `X(1)=X0` is

\[
X(a)=X_0a^{-6/A},\qquad
\rho(a)=\frac{\rho_0}{A+1}\left[Aa^{-3(1+1/A)}+1\right],\qquad
p(a)=\frac{\rho_0}{A+1}\left[a^{-3(1+1/A)}-1\right].
\]

The isolated carrier has `c_chi²=1/A` throughout that homogeneous solution. At fixed nonzero Y its speed is `1/[1+(A-1)/B(Y)]`, recovering the intended large-gradient scaling. These are action-derived properties; no inserted time dependence is needed. For the illustrative `A=10^10`, the density differs from exact dust by about two parts in a billion at `a=10^-3`. That fact alone is not a CMB or structure-formation prediction.

We also checked the positive kinetic Schur complement appropriate to the clock and carrier after the auxiliary scalar is eliminated. Its determinant is `4 Akin Bkin E/(Akin H²+Bkin C²+E)>0` under the stated positive-domain assumptions. Lean certifies the matrix algebra; the mapping from the action uses the independently reconstructed scalar constraint and the prior ADM velocity derivation. Healing must be absent or explicitly intrinsic spatial healing for this mapping.

**The limit found by testing the construction:** at finite Y the carrier can reduce the scalar's longitudinal spatial stiffness. An exact local example and an asymptotic argument show that a fixed J(Y) cannot guarantee that particular spatial block's positivity for arbitrarily large X. A viable construction must control the physically reached X,Y domain or alter the finite-gradient coupling. We have not established that control. Positive kinetic energy and homogeneous decoupling are separate from this question.

The fixed-Y power-law/affine-EOS ingredient is known in the literature; [the attribution check](LITERATURE.md) gives the exact source and dictionary. No global novelty claim is made for the combined construction. Its value here is repairing a specific missing implication in the current action.

Details: [carrier action and conserved completion](carrier_action/REPORT.md), [kinetic certificate and finite-gradient gate](carrier_bounds/REPORT.md), [independent review](completion_review.md).

## 2. The cluster route was closed prematurely

L293 does not derive its claimed cluster exclusion:

- For its own assumption `P=rho*C(r)`, hydrostatic balance gives `d log rho/d log r=-v²/C-rC'/C`. The code uses the opposite sign on the derivative term.
- The inward density integral has its sign reversed. The mass calculation also changes the outer density boundary from 5 Mpc to 1.4 Mpc, and its required normalization uses 0.32 where the prose says 2.2.
- Most fundamentally, the carrier's characteristic speed is not its equilibrium pressure divided by density. At its reference point the actual action has `p=0`, `rho>0`, and `c_chi²>0`. Away from it, Y introduces exchange and anisotropic stress.
- The stated point-source deep-MOND potential is outside its deep-MOND domain in the 75–420 kpc band. The older L41 work had also already shown that a finite-band slope near −1.5 can come from a cored profile.

Correcting the declared surrogate changes its mean band slope from −4.3005 to −2.3005. With its original cosmic outer-density boundary, the corrected atmosphere becomes overwhelmingly self-gravitating, invalidating the assumed fixed potential. This **does not** establish a viable halo; it establishes that the published exclusion and its opposite are both unsupported by that surrogate.

The action itself gives a cleaner reduction for a stationary carrier:

```text
X(r)=mu_infinity²/N(r)²,
rho=2X p_X-p,
p_radial=p-2Y p_Y,   p_tangential=p.
```

Those quantities, the scalar equation and gravity must be solved together. This replaces an assumed isothermal atmosphere with a definite boundary-value problem. [Exact hydrostatic correction and inverse-pressure theorem](cluster_equilibrium/REPORT.md).

## 3. The channel-count work supplies a conditional theorem, not the missing coefficient

The correct static two-potential Einstein symbol has rank two in every spatial dimension d>=2 at nonzero frequency. The OR-response algebra also survives and now compiles in the audited Lean reconstruction. Its general consequence is

\[
\kappa=\frac1{n\lambda},
\]

where lambda is the single-channel slope in the chosen physical vacuum units. Setting n=2 does not determine lambda.

An exact positive family makes the remaining freedom explicit:

\[
p_\lambda(y)=\frac{\lambda y}{1+\lambda y},\qquad
\mu_\lambda(y)=1-(1+\lambda y)^{-2},\qquad \lambda>0.
\]

It preserves two identical OR channels, normalized saturation, monotonicity, a quasistatic variational action and ellipticity away from zero field, while giving `kappa=1/(2lambda)`. Rank and parity do not supply an energy weighting or unit susceptibility. PD03's quarter-energy matching is equivalent to the desired coefficient once its scale definition is assumed; its numerical check inserts `a0=s/2` first. PD03 itself identifies matching as a premise, and that qualification matters.

One may choose matching as a physical postulate and test it. Calling it independently derived requires an action calculation that fixes lambda or the equivalent energy coefficient. [Exact counterfamily, general slope theorem and Lean reconstruction](pd_normalization/REPORT.md).

## 4. A major mathematical evidence problem: the NS code removes advection

Eight examined Navier–Stokes scripts contract derivative indices in the wrong order. Six compute `grad(|u|²/2)`, which the correct incompressibility projector removes. N05 additionally differentiates a captured initial field instead of the current field; N12 additionally has a defective projector on the k_x=0 plane.

For the resolved divergence-free field `u=(sin y,0,sin x)`, true projected advection has RMS exactly 1/2; the six affected implementations produce essentially zero. An isolated corrected N04c run differs from the original by about 0.124 RMS, whereas the original agrees with exact forced Stokes to `2.74e-15` in that bounded test.

The useful Lean-certified explanation is that energy tests cannot catch this particular transpose:

\[
u\cdot(Du)=u\cdot(D^Tu)
\]

for every real matrix D. The original and corrected evolutions can both pass energy checks while being different PDEs. A runnable corrected solver and source-faithful discriminating tests are archived. These bounded results require rebuilding the affected numerical evidence; they neither settle Navier–Stokes regularity nor invalidate separate correctly stated conditional theorems. [Operator audit, repaired solver and exact certificates](major_questions/REPORT.md).

The bounded RH survey still lacks control of every zero of the actual completed zeta, beyond its symmetry/factor identities. The examined YM06 certificate still needs the physical fluctuation operator, its domain and boundary matching before an assigned positive frequency becomes a spectral gap. Neither branch produced a major-problem solution in this review.

## What is proved and what would actually move closure forward

The new carrier closes two concrete algebraic obligations: a conserved rolling background and absence of direct switch-induced quadratic scalar coupling along that background. The kinetic certificate closes a conditional velocity-sign obligation. The corrected hydrostatic identity, susceptibility counterfamily and NS operator witness are also exact results with compiled Lean portions.

The immediate physics target is now specific: derive the complete finite-gradient principal matrix of this one action on an action-consistent static solution, including the X,Y exchange and anisotropic pressure. Its characteristic speeds and kinetic signs must hold on the same accessible field domain used to compute the halo. The full FRW equations must then be reduced using the actual scalar constraint and an action-consistent background. The existing L291 result cannot substitute for that calculation. A coefficient derivation remains a separate action-normalization obligation.

This is the research direction I would prioritize. The broad theory and the major mathematical questions remain open. The value of this checkpoint is that it supplies a concrete candidate, precise theorems it satisfies, a detected limitation, and corrected computations that can decide the next step.

All successful final computation and Lean runs have adjacent version-2 manifests. `checkpoint.json` records the base and route ownership; `evidence_index.json` records final validation. Earlier failed/preflight runs are retained as such and are not substituted for final evidence. No tests assert that a bounded numerical run proves universal stability or a major open theorem.
