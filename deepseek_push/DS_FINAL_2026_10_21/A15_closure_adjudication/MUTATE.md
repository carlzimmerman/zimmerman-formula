# A15 — mutation controls

Two mutations, both in `a15_checks.py`, both must break declared checks. Each run is captured in full;
the excerpts below are verbatim from the captured output.

| run | flag | exit | result | checks that must fire |
|---|---|---|---|---|
| main | — | 0 | `A15 COMPLETE: 15/15 checks PASS.` | — |
| M1 | `--mutate` | 1 | `A15 COMPLETE: 12/15 checks PASS.` | K7, K9, K12 |
| M2 | `--mutate-gamma` | 1 | `A15 COMPLETE: 12/15 checks PASS.` | K1, K6, K7 |

Files: `a15.out` (main), `a15_MUTATE.out` (M1), `a15_MUTATE_gamma.out` (M2),
`a15_results.json`, `a15_results_MUTATE.json`.

## M1 — `--mutate`: assert the identity by hand

**What it changes.** The lane's finding is that the chain's output is *not* the law's κ. M1 asserts the
opposite: it hard-wires the chain's output to be the law's κ (`out_mut = κ_law`), i.e. it simulates a
world in which GF2's claim is true and the two numbers are one object.

**Why the checks must fire.** K7, K9 and K12 are the three checks that assert the two quantities are
*distinct objects*. If the mutation cannot make them fail, they are decoration.

Verbatim:

```
K7  RENAMING TEST (CFG908 T1b): move the law's kappa; the chain's 1/2 does not move
      law's kappa 1/2 -> 2/5:  chain output = 1/2 (main) / 2/5 (mutate)
      |chain output - renamed law kappa| = 1/10 in the main run:
  [FAIL] K7   chain output 1/2 vs law kappa 2/5: difference 1/10  |  THRESHOLD: main: output = 1/2 and != the renamed law kappa; mutate: must FAIL

K9  SCALING SYMMETRY (the proof): kappa_dyn is mu-invariant, kappa_law scales as mu
      chain equations after the substitution: sigma^2-C/2 -> 0 (x sqrt(mu)); v^2-C -> 0
      kappa_dyn before/after: 1/2 / 1/2   (invariant)
  [FAIL] K9   symmetry residuals 0,0; kappa_dyn invariant = True; kappa_law weight = mu  |  THRESHOLD: exact invariance of the chain and unit weight of kappa_law

K12 THE DILEMMA: tie a0 = k_tie c sqrt(G rho_DE) and there are only two horns
      horn A (chain does not use the tie):  d kappa_dyn / d k_tie = 0
      horn B (tie substituted):             kappa_law = k_tie  (returns the input)
  [FAIL] K12  d kappa_dyn/d k_tie = 0; kappa_law(tie) = k_tie  |  THRESHOLD: 0 and k_tie respectively -- no informative horn
```

**Reading.** With the identity forced, the chain output moves with the rename (2/5) — which is precisely
the behaviour K7 declares a *failure of the finding*. The three checks are live: they detect the
identity-assertion and reject it. Under M1 the lane's verdict would be `DERIVED`, and the script refuses
to print it.

## M2 — `--mutate-gamma`: γ = 2.1 (GF2's own registered mutation)

**What it changes.** The chain's density exponent is set to γ = 21/10 instead of 2, keeping Φ = C ln r.
This is GF2's own MUTATE (`GF2_MUTATE=1`, κ_dyn = 10/21 = 0.476). It is the honest test that the chain's
numbers are not algebraically insensitive to their input.

Verbatim:

```
K1  THE GF2 CHAIN REBUILT  --  where sigma^2 = C/2 comes from
      P1  Phi = C ln r  (the committed static branch)
      P2  Lap Phi = 4 pi G rho   ->   rho = C/(4 pi G) r^-gamma
          with gamma = 2: gamma = 2 FORCED;  chain gamma used here = 21/10
          Poisson residual at gamma = 21/10: C/r**2 - C/r**(21/10)
          sigma^2 (gamma-2)/r = -C r^(-1)  ->  sigma^2 = 10*C/21
          v_c^2 = r Phi' = C;   kappa_dyn := sigma^2/v_c^2 = 10/21
  [FAIL] K1   Poisson residual C/r**2 - C/r**(21/10); sigma^2=10*C/21; v_c^2=C; kappa_dyn=10/21

  [FAIL] K6   kappa_dyn(beta) = -10/(20*beta - 21); range [0.323,0.909]
  [FAIL] K7   chain output 10/21 vs law kappa 2/5: difference 8/105
```

**Reading.** γ = 2.1 leaves a *residual* `C/r² − C/r^2.1` — the log potential does not source a
γ ≠ 2 power law, and κ_dyn falls to 10/21 = 0.4762, exactly GF2's registered MUTATE value (cross-lane
agreement). K1 and K6 fire as declared. K7 also fires because the mutated chain no longer returns ½; that
is incidental to M2 but correct: the check pins the value as well as the invariance.

**What M2 does not show.** It does not rescue or damage the verdict. κ_dyn = 10/21 under γ = 2.1 is still
a ratio with no a₀ in it; the K8 symbol audit and the K9 symmetry are untouched by the mutation. The
verdict `DIFFERENT-QUANTITY` survives every value of γ.

## Why these two and not more

The claim under test has exactly two load-bearing parts: (1) the chain's output is the SIS ratio (algebra,
tested by K1/K2/K3/K4 and broken by M2's γ), and (2) that ratio is not the law's κ (identity, tested by
K7/K8/K9/K12/K14 and broken by M1's forced identity). Each part now has a mutation that makes its checks
fail, so neither is a slogan.
