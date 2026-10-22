# A57 — mutations

Five mutations, each invoked as `python3 a57_checks.py --mutate NAME`, each writing
`a57_MUTATE_<NAME>.out` / `a57_results_MUTATE_<NAME>.json`. **Every one exits 1.** The base run is
`a57.out` (20/20 PASS, exit 0). All mutations are switches inside the script; no file is edited.

## Summary

| mutation | what it changes | checks broken | exit |
|---|---|---|---|
| `kappa1` | κ = 0.5 → 1.0 (the "no factor ½" reading) | K5, K7, K17 | 1 |
| `no_turnoff` | y_t → ∞ (the closure with no turn-off) | K1 | 1 |
| `capacity2` | capacity 2a₀ instead of a₀ (a medium that over-responds) | K1, K3, K4, K5, K7, K20 | 1 |
| `q3` | the q = 3 ladder instead of q = 2 | K10 | 1 |
| `xi_ell1` | turn-off at the cell acceleration c²/ℓ₁ = a₀/κ (ξ = ℓ₁) | K1 | 1 |

## The five, in detail

### `kappa1` — κ = 1

The mutation a reader would try first: if κ were 1 instead of ½, `8π/κ²` falls from 100.531 to 25.133, the
cell ratio `Y = 1/κ` from 2 to 1, and the identity curve (14) moves.

```
FAIL K5 0.464585 | 0.465 < 25.133 ; shortfall>80 | xi=ell_1 => Y=1/kappa=2
FAIL K7 Y*=28.0345 kappa_req=0.035670 a0_req=6.6733e-12 | Y*>100, kappa_req<0.02, a0_req<0.05 a0
FAIL K17 L*(8.33km/s)=12.02 pc ; sigma(24pc)=11.771 ; sigma(90pc)=22.794 km/s | 24.04+-0.1
A57 COMPLETE: 17/20 checks PASS.
```

Teeth: K5's shortfall drops to 25.13/0.4646 = 54.1 (< 80), K7's required a₀ rises to 6.67×10⁻¹² (still 14× low,
but outside the frozen 5 % band), and K17's identity value halves to 12.02 pc. So the numbers in §3 are pinned to
κ = ½ and to no other value.

### `no_turnoff` — the closure integral with no IR cut-off

`y_t → ∞` removes the `1/(1+(y/y_t)²)` weight. This is the sharpest single mutation because it tests whether the
lane's central claim — that convergence is supplied by the turn-off and not by the medium — is actually being
computed rather than asserted.

```
FAIL K1 999986.684488 | |F-100.405845|<1e-6 | MUTATION no_turnoff: integral runs to 1e6
A57 COMPLETE: 19/20 checks PASS.
```

The integral diverges linearly (F(10⁶) = 9.99987×10⁵). K1 fails by four orders of magnitude, which is the
numerical content of §2.2: **a finite-capacity medium alone has no finite vacuum closure**.

### `capacity2` — capacity = 2a₀

Every response is multiplied by 2, i.e. the medium stores twice the field it should. This is the mutation that
tests the capacity = affinity constraint of §1.2 and the bound (7)–(8).

```
FAIL K1 200.81169 | |F-100.405845|<1e-6
FAIL K3 min=2.000e-04 max=1.999999980 | 0<=h<1 on 4001 points; exact identity
FAIL K4 1.977126 | <1
FAIL K5 2.293465 | 2.293 < 100.531 ; shortfall>80
FAIL K7 Y*=53.7869 kappa_req=0.018592 a0_req=3.4782e-12
FAIL K20 F(Y)/Y at 1e5 = 1.99978 ; F_inf = 200.8117 ; F(50) ratio=0.851
A57 COMPLETE: 14/20 checks PASS.
```

Six checks break. Note the shape: `h ≤ 1` (K3) and `F ≤ Y` (K4) both fail *because* the capacity is not a₀ — the
bound (8) is not an independent assumption but a restatement of capacity = a₀.

### `q3` — three states per site

The ladder is run with q = 3, which is the alternative a "finite number of states" model-builder would pick.

```
FAIL K10 gN3/a0(x=.5)=-0.0714 ; law residual=0 | q=2 only; q=3 -> gN<0
A57 COMPLETE: 19/20 checks PASS.
```

K10 is the only check with a q-switch, and it fails exactly on the statement §1.2 makes: at x = ½ the q = 3 medium
gives g_N/a₀ = −0.0714 < 0. Nothing else moves, which is correct — the q = 3 ladder still has the same closure
integrand shape at large y, so the closure checks are blind to q. That blindness is itself the point of the lane:
q is fixed by the law, not by the closure.

### `xi_ell1` — the turn-off at the cell acceleration

The one-structure hypothesis of §3a: the medium's correlation length *is* the vacuum cell, so the response cuts off
at a_max = c²/ℓ₁ = a₀/κ, i.e. y_t = 1/κ = 2.

```
FAIL K1 2.203666 | |F-100.405845|<1e-6 | xi=ell_1 => Y=1/kappa=2
A57 COMPLETE: 19/20 checks PASS.
```

F(2) = 2.204 (the tanh-substituted quadrature of the full turn-off at y_t = 2) — 45.6× short of 100.406. The
sharp-cutoff value quoted in the report is 1.147 (integration to Y = 2 with the turn-off of 66.3); both are far
below the requirement, and both trigger K1. The mutation is recorded to show that the identification ξ = ℓ₁ is not
merely disfavoured by a factor of order unity: **it removes 98 % of the integral.**

## The Lean mutation

`A57_uv_completion_MUTATE.lean` relaxes the truncation hypothesis of `kappa_ge_eight_pi` from `F ≤ Y` to
`F ≤ 3·Y` (everything else identical, namespace `A57mut`). Compiled with the same command:

```
A57_uv_completion_MUTATE.lean:129:11: error: Tactic `rewrite` failed: Did not find an occurrence of the pattern
  1 / κ * κ ^ 2
in the target expression
  8 * Real.pi ≤ 3 * (1 / κ) * κ ^ 2
...
'A57mut.kappa_ge_eight_pi' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
```

Exit 1. The other eight theorems still print the clean footprint, so the failure is localised to the bound: **the
proof of κ ≥ 8π genuinely uses F ≤ Y**, and the relaxation leaves `8π ≤ 3κ`, from which `8π ≤ κ` does not follow.
Recorded in `A57_uv_completion_MUTATE.out`. (The `sorryAx` is Lean's error-recovery marker for the failed proof, not
an axiom of the certificate.)

## What the mutations do not do

They do not re-run the symbolic checks under altered symbols (K2, K11, K12, K13 are identities and are either true or
false independent of the switches). They do establish that each numerical claim in the report is computed from the
stated inputs and not hard-coded: five independent switches, each breaking at least one check, with the union
covering K1, K3, K4, K5, K7, K10, K17, K20; and the Lean mutation shows the algebraic bound is not vacuous.
