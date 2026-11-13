# Joint obstruction: the repaired clock cannot meet both declared targets

**The tested perspective/Q-Gamma repair has no common clock coefficient satisfying the stated galaxy target and unchanged early-universe history.** This conclusion uses the corrected equations. It does not use the inherited, inapplicable 25120/Mpc growth threshold.

The result is conditional on a precise action class and the program's declared requirements. It is not a new primordial-abundance likelihood or a theorem excluding every possible realization of the Zimmerman relation.

## Common hypotheses

1. The same conserved clock supplies the canonical present dust coefficient and has `H(Q,0)=F(Q)=mu²(Q-1)²/(2K)`, `K=4piG`, throughout the specified homogeneous early history. There is no later source of net homogeneous clock charge.
2. The repair is the perspective bounded-piece construction `H=F-B+B S-Q Gamma`, with the original W and optional nonnegative original stiffness. Its Pi dependence is concave on the independently admissible rectangular domain `1<=Q<=Qmax`, `Pi>=0`; the compensator and its first derivative vanish at Pi=0. This already weakens the original unrestricted-Q requirement.
3. The galaxy target is the canonical `10^11 Msun` weak-field annulus from approximately 12.2 to 732 kpc, with the stated Q/force profile and weak spatial geometry. Clock energy is suppressed by at least the declared fraction `delta=(1 Mpc^-1/mu)^2`. No extra negative-active-energy compensating sector is added. Polarization deformation is allowed in the necessary pressure bound.
4. The early radiation comparison uses the frozen KD1 temperature convention at 0.1 MeV and its budget 0.067. This is a declared test, not a newly inferred observational confidence limit. The weaker alternative budget 1 is also evaluated.

The non-overlap below follows even with the illustrated positive cosmological constant, up to `Lambda=1.1e-7 Mpc^-2`. The numerical target is not being refitted.

## Exact early-history requirement

Homogeneous current conservation gives `n=n0 a^-3`. Directly from F,

    rho_clock = n0 a^-3 + K n0²/(2mu²) a^-6.

With `n0=Omega_d rho_crit0`, `I0=3H0² Omega_d`, and the specified radiation scaling,

    rho_stiff/rho_r = Omega_d I0/(4mu² Omega_r a²).

Both proposed repairs leave the homogeneous F branch unchanged, so they retain this result. The [growth/background audit](../growth_gate_audit/RESULT.md) and [independent reconstruction](../growth_derivation/BBN_STATIC_AUDIT.md) reproduce the frozen criterion:

    mu >= 8,890,113.535 Mpc^-1.

This equation is exact for that clock branch and declared radiation history even when the clock is far from cold. Precision nucleosynthesis would require a thermal history and reaction network; a stiff component cannot be identified with a constant extra-neutrino contribution across all epochs.

## Independent galaxy requirement

Concavity on the rectangular Q band already forces a minimum compensator curvature. Its finite-Pi pressure moment cannot be removed by a QPi boundary term. Including the full on-shell spatial stress, W and the original positive stiffness gives a positive mean-pressure floor. The energy-suppression requirement itself forces `S<=delta`, so this floor does not assume that the actual polarization equals the unperturbed AQUAL profile.

The static Einstein equation is

    D²N = N[K(rho+3 mean(p))-Lambda].

Normal density is nonnegative on the stated branch. Integrating this equation across the specified annulus bounds the increase in lapse flux from below. Its independently reproduced necessary coefficient ceilings are:

| Lambda [Mpc^-2] | Necessary mu ceiling [Mpc^-1] |
|---:|---:|
| 0 | 435.3271 |
| 1e-7 | 445.3183 |
| 1.1e-7 | 446.3052 |

See the [static pressure proof](../static_gate/polarized_pressure/RESULT.md) and [independent audit](../growth_derivation/BBN_STATIC_AUDIT.md). These are necessary ceilings; no viable solution below them is asserted. The weak-geometry approximation and prescribed target remain explicit hypotheses. Rounding the largest ceiling upward to **450/Mpc** leaves margin far larger than the displayed weak-field corrections.

## No parameter interval remains

| Requirement | Conservative bound on the same mu |
|---|---:|
| Specified galaxy target | mu <= 450/Mpc |
| Frozen early-radiation budget 0.067 | mu >= 8.89e6/Mpc |
| Much weaker early budget: stiff energy <= radiation | mu >= 2.30e6/Mpc |

The frozen lower bound exceeds the rounded galaxy ceiling by a factor **19,756**. Even allowing stiff energy as large as all radiation leaves a factor **5,114**. At the rounded galaxy ceiling, the specified early stiff/radiation ratio is about **26.1 million**. Thus the contradiction does not depend on interpreting the historical 0.067 as a precision empirical limit.

Meeting the frozen budget at the galaxy ceiling would require the early homogeneous comoving charge to be at most about `5.06e-5` of its present value. The unchanged source-free conservation law cannot produce that later increase. Local mass retention and an external-field boundary redistribute or affect response; they do not supply a missing source in this homogeneous current.

The separate quiet-polarization test is stronger than the raw lapse bound at low mu: the explicit minimum-moment repair needs roughly 13.21 extra baryon masses in the polarization-subtracted field equation at mu=198.25. That rejects the quiet branch. The general parameter contradiction above does not rely on that stronger branch-specific assumption.

## What this closes

The original unrestricted flat multiplicative gate already fails the constrained scalar health test. The nonmultiplicative construction genuinely repairs the identified curvature problem; claiming it mathematically impossible would be wrong. Its Q-independent version changes the force law, while its Q-dependent version fails the joint pressure/background requirements above, even after the tested rectangular clock-band restriction.

This closes these specified implementations as completions of the declared combined retention/external-field program. A changed early-time kinetic term or history, an actual charge-production mechanism, a derived correlated state domain, a changed galaxy target or an additional jointly varied stress sector would alter the hypotheses. Those are new constructions, not solutions supplied by this action. No universal all-theory impossibility or derivation of kappa is claimed.

`run_001/manifest.json` records the bounded arithmetic combination of two pinned audited results. The independent audit separately reconstructs both the homogeneous bound and the static scalar root. Historical incorrect growth claims were corrected forward while preserving their original bodies and source snapshots.
