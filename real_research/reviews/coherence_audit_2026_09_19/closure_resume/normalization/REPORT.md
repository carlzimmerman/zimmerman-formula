# Normalization closure: action-level audit and exact discriminator

Base: `23d3890790291c0ec44b4ca7da784a806d7094d2`, with pre-existing dirty workspace. This is a new independent audit of the supplied raw sources, not an edit to their conclusions. All writes are below this directory. The version-2 computation manifest pins the actual source hashes before and after execution, records dirty state, and hashes the results.

**Target:** derive the dimensionless relation `a0 = kappa sqrt(G rho_vac)` in units `c=1`, with vacuum energy and the MOND acceleration initially independent, using a physical principle already present in the source action. Neither fitting `kappa`, selecting a response with the desired slope in prescribed vacuum units, nor comparison with a reference cosmology counts.

**Primary verdict: incomplete, with the smallest missing implication identified.** None of the examined source principles fixes the ratio of the zero-gradient action value to the deep-MOND coefficient. The shared-function route still needs that implication even after removing a separate potential. The exact calculation below excludes its most direct boundary-normalization repair for the preferred `n=2` kernel. This is not a universal obstruction to gravitational theories or all global constraints.

## 1. The missing coefficient survives in a single function

The raw implementation `fable_independent_2026/L230_one_number.py:53` explicitly postulates the gradient argument in vacuum units, and line 56 sets `Yv = gradPhi/sqrt(G*rho)`. Its subsequent `kappa=1/n` is correct conditional on that identification; it does not vary an action that derives it.

Write the actual standard static AQUAL normalization with an initially independent acceleration `s`:

```text
L_static = -s^2 F(z)/(8 pi G) - rho_b Phi,
z = |grad Phi|^2/s^2,
F'(z) = mu_n(sqrt(z)) = 1-(1+sqrt(z))^(-n).
```

Variation in `Phi` gives `div(mu_n grad Phi)=4 pi G rho_b`. The deep limit `mu_n(y)=n y+O(y^2)` therefore yields `a0=s/n`. Newton's constant is already fixed by `mu_n(infinity)=1`.

To test the proposed shared-function vacuum reading, retain a lapse in the explicitly declared homogeneous completion:

```text
L_hom = -N a^3 s^2 F(0)/(8 pi G).
rho_vac = -(1/a^3) dL_hom/dN = s^2 F(0)/(8 pi G).
kappa^2 = 8 pi/[n^2 F(0)].
```

This completion is a stated hypothesis of this normalization calculation, **not** a complete covariant action. Another lapse coupling must be varied in its own terms; its energy cannot be identified from a static primitive by assertion.

At `n=2` the exact primitive is

```text
F(z) = F0 + z - 2 log(1+sqrt(z)) + 2 - 2/(1+sqrt(z)).
```

Both `F0=8 pi` and `F0=2 pi` give exactly the same static response and the same `a0=s/2`, but their gravitational vacuum densities give respectively `kappa=1/2` and `kappa=1`. Both have positive vacuum energy. Thus fixing `n=2` and using one function does not remove the zero mode. In these action conventions, the identification made by L230 requires the additional physical condition `F0=8 pi`. Defining units so that this holds relocates the missing ratio into the gradient argument; it does not derive it.

## 2. Executed discriminator: empty Newtonian vacuum and the marginal index

The repository already considers fixing the primitive by an empty Newtonian vacuum in `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py`. L234/L235 separately identify `n=2` as the convergence boundary of the primitive residual. The discriminating calculation combines those proposed ideas in the single-function AQUAL sector, with its own sign and normalization rather than importing the different scalar-carrier sign from k01.

Demand `F(z)-z -> 0` as `z -> infinity`. Since `F'(z)-1=-(1+sqrt(z))^(-n)`, this would imply

```text
F0 = integral_0^infinity [1-mu_n(sqrt(z))] dz
   = 2 integral_0^infinity y/(1+y)^n dy.
```

For the preferred `n=2`, the exact cutoff integral is

```text
I2(R) = 2 log(1+R) + 2/(1+R) - 2 -> infinity.
```

No finite `F0` satisfies that boundary condition. A logarithmic finite-part prescription does not fix the problem without extra physical information:

```text
lim_R->infinity [I2(R)-2 log(R/ell)] = 2 log(ell)-2.
d/d log(ell) [finite part] = 2.
```

The subtraction scale is exactly a surviving dimensionless normalization datum. A quantum anomaly or ultraviolet completion might in principle determine such a scale, but none is supplied by this calculation or by the inspected source route. Calling the marginal index a criticality principle alone supplies no finite matching condition.

For every real `n>2`, by contrast, the integral converges and the same boundary prescription gives

```text
F0 = 2/[(n-1)(n-2)],
kappa^2 = 4 pi (n-1)(n-2)/n^2.
```

The elementary antiderivative is verified symbolically; its upper endpoint vanishes because the powers `2-n` and `1-n` are negative. For integer `n>=3`, the derivative of `kappa^2` with respect to real `n` is `4 pi (3n-4)/n^3 > 0`, so `kappa^2 >= 8 pi/9 > 1/4`. Thus **no positive integer member of this family produces `kappa=1/2` under this particular empty-Newtonian-vacuum prescription**: `n<=2` diverges, while `n>=3` has the wrong coefficient. For `0<n<2`, divergence follows directly from the asymptotic integrand `2 y^(1-n)`; no numerical sampling is used.

This is a conditional exact result about one explicit prescription, not a rejection of the empirical shape or every possible normalization mechanism.

## 3. L236's variable-coefficient loophole closes exactly

L236's final paragraph explicitly leaves open whether `U(tau)` supplies an extra term that can replace a cuscuton potential. For

```text
S_clock = integral sqrt(-g) [U(tau) sqrt(X)-V(tau)],
X = -g^(mu nu) tau_mu tau_nu > 0,
```

on a future monotone homogeneous branch (`dot(tau)>0`, `N>0`),

```text
L_clock = a^3 U(tau) dot(tau) - N a^3 V(tau).
d/dt [dL/d dot(tau)] - dL/dtau
    = 3 a^2 dot(a) U + N a^3 V_tau.
```

The two `U_tau dot(tau)` terms cancel exactly. With `H=dot(a)/(Na)`, the result is `3 H U+V_tau=0`; the lapse energy is `rho_clock=V`. Therefore allowing `U` to depend on `tau` does **not** reopen the no-potential branch: where `U != 0`, setting `V_tau=0` still forces `H=0`.

Covariantly the same cancellation follows from `d_mu[U(tau)n^mu]=U theta+U_tau sqrt(X)` in the Euler-Lagrange equation. The corresponding local field redefinition `d chi=U(tau)d tau` also makes the pure cuscuton coefficient constant wherever `U` has fixed nonzero sign. These are orthogonal checks of the minisuperspace result. The conclusion does not cover an additional `P(X)` sector, derivative couplings, or the degenerate branch `U=0`.

A required potential is not itself proof that its additive constant must remain arbitrary in *every* possible theory. L236's broader architectural language must remain conditional on the absence of another equation, symmetry, or boundary condition fixing it. For its displayed sector the clock equation only fixes `V_tau`, leaving the constant untouched.

## 4. Four-form route: a structural scaling, one invariant free ratio

The calculation independently varies k04's homogeneous four-form term, using flux `f=N a^3 q`:

```text
L4 = N a^3 P(f/(N a^3)),
P(q) = Z q^2/2 + b beta^2 q^2,
rho4 = -(1/a^3) dL4/dN = q P_q-P,
a0^2/G = beta^2 q^2.
```

It reproduces exactly

```text
kappa^2 = 2 beta^2/(Z+2 b beta^2),
kappa=1/2 iff Z/beta^2 = 8-2b.
```

The flux amplitude cancels, which is real progress toward the square-root scaling. The remaining ratio cannot be removed by canonically rescaling the four-form: that rescaling changes `Z` and `beta^2` together and preserves `Z/beta^2`. The source provides no equation selecting this ratio. This audit derives its needed energy identity directly and does not rely on k04's external citations or local numerical feedback claims.

## 5. Dependency and obligation record

| Implication | Status | Decisive evidence |
| --- | --- | --- |
| Static kernel fixes derivative but not primitive | Passed | Exact primitive and positive-vacuum counterpair |
| One shared function alone implies `kappa=1/n` | Failed | Depends on independently fixing `F0=8 pi` in the declared convention |
| Marginality plus empty Newtonian vacuum fixes preferred `n=2` primitive | Failed | Exact logarithmic divergence; finite subtraction retains `ell` |
| Same empty-vacuum boundary gives half for another integer `n` | Failed | General convergent integral and monotonicity for `n>=3` |
| Variable `U(tau)` rescues the pure potential-free cuscuton | Failed | Exact Euler-Lagrange cancellation with lapse retained |
| Four-form fixes square-root scaling | Passed in stated quadratic sector | Flux amplitude cancels exactly |
| Four-form fixes its coefficient | Incomplete | `Z/beta^2` remains free |
| Global-constraint classes are exhausted by k02 | Not established | k02 is a specified numerical cosmic-average model, not a universal action theorem |
| Complete healthy relativistic theory follows | Not addressed | Requires full action and independent constraint/stress/perturbation analysis |

The raw-source dependency chain is: k01 establishes the original primitive zero mode; L226 isolates the ratio that a shape-fixing principle must determine; L230 supplies a vacuum-unit argument by assumption; L231 supplies `mu_n`; L234/L235 supply the marginal-index suggestion; L236 states the cuscuton loophole; k04 supplies the four-form mechanism. THE_ACTION and CLOSURE_THEOREM are context and claim locators, not substitutes for those implementations. All are hashed in `run/manifest.json`.

## 6. Exact remaining implication and next executable mechanism

The missing implication is a physical condition fixing the relation between the zero-gradient action value and its deep-MOND derivative coefficient **in the same lapse-varied covariant action**, without an independent vacuum term, a free subtraction scale, or a free coupling ratio.

The cheapest discriminating gate for a new candidate is now explicit: derive its homogeneous lapse energy, deep static flux, and the change under a constant shift or field rescaling before fitting anything. For the four-form branch the input needed is an actual action-level relation selecting `Z/beta^2`; then derive whether it survives integrating out the constrained fields. For the marginal `n=2` branch the input needed is a dynamical or ultraviolet matching condition fixing the finite subtraction scale. Neither input appears in the inspected source artifacts. There is no presently specified executable mechanism here that honestly completes the coefficient derivation; another number fit would not advance it.

## Reproduction and provenance

`run/results.json` contains all 24 exact checks; the process exited zero. `run/stdout.txt` contains the compact results and `run/stderr.txt` is empty. The version-2 manifest passed validation with the repository root supplied, including input freshness and result hashes. It records the full argv needed to reproduce the run in a fresh output directory. Environment: Python 3.9.6, SymPy 1.14.0; no randomness, observational data, external downloads, or reference-cosmology fitting. Wall limit 30 seconds and combined-log cap 1 MiB; the run completed in under a second. Thread limiting is cooperative, as recorded by the runner.

Interpretation was separately self-reviewed against the equations above. The computation verifies formulas and limits in the stated family; the proof of the integer-family exclusion also uses the written asymptotic and monotonicity reductions. Agreement of exact algebra alone does not establish the missing physical input.
