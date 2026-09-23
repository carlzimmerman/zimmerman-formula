# Closure assessment after the constructive search

**The novel theory is not closed.** This continuation found constructive possibilities, corrected an overinterpretation in the preceding report, and isolated two central obligations. It has not produced one action that simultaneously derives the normalization, has controlled physical evolution, and yields the required galactic and cluster solutions. This verdict concerns the candidate's own equations; agreement with another cosmological model is not a premise.

The meaningful closure target is one declared action and domain, its consistent background and constraints, a controlled evolution of its physical perturbations, and its force and density predictions. If the coefficient in `a0 = kappa sqrt(G rho_vac)` is claimed as a prediction, the action must also determine it. Stating that coefficient as a postulate would remove that particular derivation obligation; it would not settle the dynamics.

## What can now be stated positively

1. **A nontrivial part of the consistency problem is solved.** The corrected expanding action has an exact homogeneous solution and a positive two-scalar kinetic matrix for every point in the stated positive-parameter domain. The previous `PositiveKinetic.lean` certifies the matrix identity and positivity, with an independent analytic sum-of-squares derivation. This is absence of quadratic scalar kinetic ghosts, conditional on the symbolic variational derivation. It is not a stability theorem.
2. **Environmental response is a constructive option.** Explicit functions of the clock acceleration have positive longitudinal and transverse principal coefficients, the intended low-acceleration MOND cancellation, and a bounded extra force in the declared Newtonian regime. A further explicit smooth profile also has a finite positive vacuum contribution under an empty-high-acceleration boundary prescription. These constructions refute a blanket claim that this type of screening or vacuum generation is impossible. Their complete cosmological and nonlinear dynamics are not certified.
3. **The same-field fluid repair is mathematically well defined.** Replacing the density well `-F(Q)` by `-F(sqrt(Q^2-Y))` preserves its homogeneous solution and the full FRW kinetic matrix. It gives the isolated well a convex fluid interpretation and intrinsic sound speed squared `epsilon/s`, where `s=sqrt(Q^2-Y)>0`. The tested physical transfer is substantially different. This exact replacement also changes the static MOND equation, so it cannot inherit the old galaxy certificate unchanged.

These are constructive results with explicit limits. Counting successful scripts or Lean declarations would not turn them into full closure.

## Obligation 1: a real normalization equation

The simplest decisive counterpair uses the actual static kernel and its primitive. With

```text
L_static = -s0^2 F(z)/(8 pi G) - rho_b Phi,
z = |grad Phi|^2/s0^2,
F'(z) = 1-(1+sqrt(z))^(-2),
```

the deep MOND scale is `a0=s0/2`. In the explicitly declared lapse completion used in this test,

```text
rho_vac = s0^2 F(0)/(8 pi G),
kappa^2 = 2 pi/F(0).
```

`F(0)=8 pi` and `F(0)=2 pi` therefore give the same force law but respectively `kappa=1/2` and `kappa=1`, both with positive vacuum. This is a counterexample to deriving one half from that force law and shared-function assumption alone. It is not a no-go theorem for new actions.

The tested attempts to remove that freedom yield specific information:

- The empty Newtonian vacuum prescription diverges logarithmically for the preferred index two. Its finite-part version retains a free subtraction scale.
- A quadratic four-form mechanism cancels the flux amplitude and obtains the square-root scaling, but leaves the invariant coupling ratio `Z/beta^2` free.
- Allowing a variable pure-cuscuton coefficient does not supply the missing vacuum equation: the apparent extra derivative terms cancel in its Euler–Lagrange equation.

There is a more constructive alternative. For the clock sector `+f(X)`, let `alpha=f_X`, `a=alpha_lo>0`, and prescribe `f(X)-aX -> 0` at high acceleration. If

```text
I = integral_0^infinity [alpha(X)-a] dX
```

is positive and finite, lapse variation gives `Lambda_eff=I/2`, with positive vacuum energy. Using the measured Newton constant gives

```text
kappa^2 = 8 pi (2-a) a0^2/I.
```

We constructed a smooth finite profile with strictly positive clock principal coefficients. Health and monotonicity also impose a useful sharp bound. If `alpha(g0^2)=A>a`, `alpha>=a`, and `alpha` is nonincreasing, then

```text
I >= g0^2 A(A-a)/a.
```

The proof follows from `(g alpha(g^2))' > 0`, not a numerical scan. At `A=1/2`, `a=10^-7`, and `g0=a0`, it forces `kappa<0.004484`. The explicit finite profile predicts `kappa≈0.002530` if its core scale `B=a0`; obtaining one half requires `B/a0≈0.00505965`. That is the precise additional relation a new principle would need to derive. A small undershoot of the asymptotic coefficient can evade the bound while retaining principal positivity, but its location then tunes the vacuum area. It supplies an escape from a universal no-go, not a derived coefficient.

The calculation of the area and the analytic bound are documented in [the environmental vacuum report](normalization/environment_vacuum/REPORT.md). The [normalization audit](normalization/REPORT.md) records the counterpair and the other mechanisms. No external empirical cosmology is used in these arguments.

## Obligation 2: control the same action's physical modes and local solutions

An important correction to the preceding report is needed. The variables `Phi` and `P` there are in unitary clock gauge. Their short-interval growth does not, by itself, measure growth of the observable gravitational potentials. The independent reconstruction gives

```text
Phi_Newtonian = Phi - H a B,
Psi_Newtonian = psi + d(a B)/dt,
Phi_Newtonian = Psi_Newtonian.
```

Here `psi` and `B` are the solved lapse and shift perturbations. The equality follows exactly from the corrected equations. The scalar's conserved canonical-charge perturbation

```text
w = (Pdot-Q psi)/epsilon - 3 Phi
```

gives an invertible change of state that avoids the badly scaled original velocity variables. Both physical scalar modes remain present.

For the earlier short constant-coefficient witness, unitary `Phi` grew by about 22.4 while the Bardeen potential grew only by 1.00054. For the earlier short response witness, unitary `Phi` grew by about 17.8 while the Bardeen potential changed by a factor 0.99343. The short response witness therefore did not establish gravitational runaway. This correction supersedes the stronger interpretation in the original checkpoint; its numerical records are preserved.

Longer evolution is discriminating. For the original constant coefficients at `a=.1`, `k=.1/Mpc`, over `Delta log(a)=.1`, the previously selected initial direction produces Bardeen amplification about `1.73325e7` and Newtonian density amplification about `2.97007e8`. Independent 50-digit fixed-step integration confirms this bounded physical-growth witness. No reference growth curve is needed to detect it.

The response family at `a=.5`, `k=.001/Mpc` has a quite different result: the same longer interval gives Bardeen amplification about `1.05968`. That particular local episode is a transient, not the claimed fast gravitational runaway. At `a=.1`, `k=.001/Mpc`, over `Delta log(a)=.5`, however, the explicit initial state `z=(1,0,0,0)` produces Bardeen amplification about `6.35004e14`. Independent 50-digit RK4 at 2000/4000 steps agrees within `1.4e-7` in relative final-state norm; independently stepped adaptive integration agrees with the finer run within `9.4e-9`. The two statements concern different epochs and intervals and must not be conflated. These are bounded linear witnesses, not extrapolations through nonlinear saturation.

The archived fundamental matrices use the dimensionless state

```text
z = (Phi, dPhi/dlog(a), H P/Q, w).
```

Their reported observable operator norms refer to a unit Euclidean norm of this declared initial state. They are neither an energy norm nor a predicted primordial distribution. Initial amplitudes can be rescaled arbitrarily within the linear calculation. No finite collection of quiet intervals is a universal stability proof.

### Why the Lorentz-well repair is progress but not closure

For `s=sqrt(Q^2-Y)>0`, `F(s)=-A exp((s-Q0)/epsilon)` and `n=-F_s>0`, the isolated fluid satisfies

```text
p=epsilon n, rho=(s-epsilon)n,
U(n)=n[Q0+epsilon log(epsilon n/A)-epsilon], U''(n)=epsilon/n>0,
c_s^2=epsilon/s.
```

At quadratic order the replacement adds `a F_Q (P_x)^2/(2Q)` to the FRW Lagrangian. The lapse and shift constraints and the kinetic matrix are unchanged. The observable reconstruction was checked with the new accelerations. For the constant-parameter case `a=.1`, `k=.1/Mpc`, `Delta log(a)=.1`, the final Bardeen-potential operator norm falls from approximately `1.58277e7` to `0.225054` with the replacement, using the same declared initial-state norm. This is a substantial bounded improvement. It does not give a coercive energy bound: other state components and clock observables can still be large, and an individual potential gain can be large when its initial value is small. The result does not establish global stability.

In a static local environment the same replacement adds a density-dependent flux floor,

```text
beta_eff = beta + n/(2 d s), d=2-K_B.
```

At nonzero local density this spoils the old zero-gradient MOND cancellation. A counterterm that cancels this floor also cancels the proposed quadratic repair. At finite gradient the well charge can become exponentially suppressed, but the longitudinal stationary coefficient crosses its sonic condition. We obtained an exact timelike local configuration where the old static determinant is positive and the repaired determinant is `-16.7339586585`, while the temporal well Hessian remains positive. This is a counterexample to inheriting stationary ellipticity everywhere; it is not a global halo solution or a temporal-ghost claim.

Consequently the next meaningful local calculation would have to solve for the lapse, scalar gradient and charge together, rather than choose a local charge after fixing the force law. The [Lorentz-well audit](dynamic_audit/lorentz_well/REPORT.md) gives the exact action variation, counterexample and domain.

This architecture also has prior versions in the repository's `clock_response_repair_2026/nonlinear_transport` work. The same-field exponential implementation was not found in the bounded search, but the general `P(Q^2-Y)` reframing is not new to the project. L289's separate-carrier implementation has a kinetic-sign error for its chosen positive coefficients; its positive sound-speed ratio does not certify positive kinetic energy. That existing result cannot close this gap.

## What this changes about the research direction

The useful reframing is to treat the cosmological conserved charge, the MOND derivative response, and the vacuum value as three quantities that must be linked by one specified action. The Lorentz-well calculation makes a tradeoff explicit: the gradient term that helps the charge behave as a fluid also contributes to the galactic flux. The environmental calculation similarly ties vacuum energy to an integral over the screening profile. Those relations are productive constraints for a new theory because they expose exactly what a proposed mechanism must accomplish.

The next advance must supply one of the missing physical relations and survive both sides of its tradeoff. Another selected kernel, background fit, or algebraic certificate with the desired number assumed does not do that. The work here has not identified a principle that fixes the remaining scale ratio, nor a complete action with certified cosmological evolution and local solutions. The stronger target requested by the user remains open.

## Evidence and reproducibility

All new files are confined to this review directory. Existing user research was not edited. Manifests pin actual source hashes in the shared dirty workspace; a Git commit alone does not identify the run inputs.

| Evidence | Scope |
| --- | --- |
| `normalization/run/manifest.json` | 24 exact normalization and loophole checks |
| `normalization/environment_vacuum/run/manifest.json` | 31 exact finite-profile, integral, bound and undershoot ingredients |
| `environment/run/manifest.json` | 38 exact static flux and principal-matrix checks |
| `dynamic_audit/run_verified_dynamic/manifest.json` | Original-equation residuals, gauge reconstruction, Helmholtz identities and independent high-precision transfers |
| `dynamic_audit/lorentz_well/` | Exact covariant-well variation, fluid/Legendre identities and static counterexample |
| `cosmology/run_verified/manifest.json` | Exact canonical-charge transformation, original and repaired full transfers, two explicit 50-digit witnesses |

The fresh cosmology run completed and its manifest passed input-freshness and output-hash validation. Six further theorems in [NormalizationConsequences.lean](normalization/environment_vacuum/NormalizationConsequences.lean) certify the primitive-shift ambiguity, the conditional area-to-coefficient bound, its same-scale exclusion, and a positive health margin. The area bound itself is an explicit hypothesis in Lean; its analytic derivation is in the report. [StaticWitness.lean](dynamic_audit/lorentz_well/StaticWitness.lean) certifies the exact old/new determinant signs and the timelike, supersonic local configuration. Both compiled successfully, with bounded validated manifests in their respective directories. Their printed axiom dependencies contain only `propext`, `Classical.choice` and `Quot.sound`.

The contracts specify parameters, domains, precision and non-claims. Symbolic identities, Lean proofs of the declared algebra, and bounded floating-point evidence are kept distinct. `cosmology/constant_response.py` and `dust_IR.json` are exploratory diagnostics and do not enter the conclusion or the verified cosmology bundle. The 1000/2000-step development attempt for the longer response witness narrowly failed its fixed `2e-6` tolerance; doubling both resolutions passed without relaxing the tolerance, as recorded in the final contract.
