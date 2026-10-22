# A61 — mutations

Five mutations, each is a copy of the *wrong* convention or the *wrong* identity, and each breaks a
different check. Run:

```bash
python3 a61_checks.py --mutate <name>      # exit 1, at least one FAIL
```

The base run is 19/19 PASS, exit 0. The mutated stdout is saved as `a61_MUTATE_<name>.out`.

| # | mutation | what it changes | checks that fail | base → mutated |
|---|---|---|---|---|
| M1 | `eh8pi` | `K_EH = 8πG` in the EH / Poisson / Friedmann chain (i.e. the BRIEF's convention taken literally) | **K1, K2b, K3** | K1 residual 0 → −1.5e8 (`K_EH = 1.6774e-9`); `∇²Φ` coefficient 8.3872e-10 → 1.6774e-9 ; `H²` ρ-coefficient 1.6774e-9 → 3.3549e-9 |
| M2 | `wquad_a0` | `W`'s quadratic term read as `u²/(2a₀)` instead of `u²/(2K)` | **K5** | coefficient 5.9615e8 → 5.3419e9 ; and the dimension check fails independently (acceleration vs Pa) |
| M3 | `eta2gamma` | `η = 2γ` in `m² = K/η` (drops the "one stiffness" premise) | **K11** | `L*/λ_P` 1.4142 → 1.0000 ; the identity becomes `L*(2K) = c_sλ_P(K)` with `c_s² = ½` |
| M4 | `gamma8pi` | `γ = (8πG)L*²/2` with L* held at 24.02 pc, i.e. the record's bookkeeping under the BRIEF's K | **K8, K12** | `γ(8πG)/γ_phys` 2.0 → 1.0 (the check asserts the 2); the table moves to `R_core` 53.37 → 75.48 pc, `r_switch` 3.73/18.43 → 5.27/26.06 pc, `λ_J` 106.7 → 151.0 pc |
| M5 | `identity_swap` | asserts `L*(K) = λ_P(2K)` — the prompt's stated direction of the coincidence — instead of `L*(2K) = λ_P(K)` | **K10** | residual 0 → non-zero, symbolic γ and K |

## What each mutation proves

- **M1** is the important one: the BRIEF's `K = 8πG` is not a harmless relabelling. Taken into the action's
  own normalisation it changes the Poisson coefficient by a factor 2, i.e. `G_eff = 2G`. K1, K2b and K3 are
  three independent places where the same wrong number must break, and all three do.
- **M2** shows K5 is not a tautology: the coefficient and the dimension are two separate assertions, and the
  `u²/(2a₀)` form fails both. (It fails the dimension test even when the numeric coefficient is forced.)
- **M3** shows the identity `L*(2K) = λ_P(K)` has content: it requires `η = γ`. If the two stiffnesses differ,
  the coincidence degrades to `L*(2K) = c_sλ_P(K)` and there is no √2.
- **M4** is the record's actual failure mode — L* anchored at 24 pc, then γ recomputed from `KL*²/2` with the
  wrong K. The result is a 2× γ and a 1.41× core; K8 catches the 2 in γ, K12 catches the √2 in `R_core`.
- **M5** is a *sign of the arrow* test. `L*(2K) = λ_P(K)` is true and `L*(K) = λ_P(2K)` is false; both are
  "the same formula" if one does not track which coupling each side is evaluated at. This is exactly the
  symbol swap the lane is about, so the check tests the direction rather than the existence of a relation.

## Not mutated

The numerical core of the lane — `L* = 24.025 pc`, `λ_P = 16.988 pc`, `R_core = 53.370 pc`, the window
`[24.03, 90.03] pc` — is computed from BRIEF §4 constants and σ_c = 8.33 km/s. A mutation of those constants
would test arithmetic, not structure; the structure is what M1–M5 attack.