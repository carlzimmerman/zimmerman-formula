# MUTATE — A42 proof that the checks have teeth

Each mutation changes **one input or one equation** of the lane and must break at least one check.
All six do; each run exits 1. Captured output: `a42_MUTATE_<name>.out`.

```
python3 a42_checks.py --mutate <name>
```

| mutation | what it changes | checks that break | captured output |
|---|---|---|---|
| `beta0` | forces **β = 0** in the matter-filled branch (i.e. takes the lane's own premise literally) | **K11, K18, K19, K20, K23** | `a42_MUTATE_beta0.out` |
| `kappa1` | κ = 1 instead of ½ (the a₀ normalisation) | **K4, K5, K7, K9** | `a42_MUTATE_kappa1.out` |
| `h0_73` | H₀ = 73 km/s/Mpc instead of 67.4 | **K4, K5, K9, K16, K24** | `a42_MUTATE_h0_73.out` |
| `no_c2` | drops the `c²` in `Λ_bare = 3H₀²/c²` | **K3, K4, K5, K9, K10, K11, …** (8) | `a42_MUTATE_no_c2.out` |
| `lam_obs` | sets `Λ_bare = Λ_obs` (the observed-Λ footing) | **K3, K4, K5, K23, K24** | `a42_MUTATE_lam_obs.out` |
| `theta_gr` | replaces the branch's `E² = 2[1+Ω_m(1+z)³]/(2+3β)` by the naive `Ω_m(1+z)³ + (1−Ω_m)` | **K19, K20** | `a42_MUTATE_theta_gr.out` |

## Measured failures (from the captured files)

```
beta0    K18  FAIL  [2*Omega_m/3] (used: 0.000000)      K19 FAIL max|dE| = 1.1e+00
         K20  FAIL  dC -8.65%/-6.61% (sign flips)        K23 FAIL (rho_bare+rho_beta)/rho_DE = 1.4626
kappa1   K4   FAIL  2.262407e-10  (+99.86%)              K5 FAIL +99.77%
         K7   FAIL  ratio 1.000000 (not 2)               K9 FAIL bound = 3.4752e-18
h0_73    K4   FAIL  1.225191e-10  (+8.23%)               K5 FAIL +8.18%
         K16  FAIL  Lam_needed = 1.2773e-52              K24 FAIL Lam_bare/Lam_obs = 1.7155
no_c2    K3   FAIL  rho_bare/rho_crit = 8.99e+16          K4 FAIL a0 = 3.39e-02 m/s^2
lam_obs  K3   FAIL  rho_bare/rho_crit = 0.6838            K24 FAIL ratio 1.00000 vs 1.46263
theta_gr K19  FAIL  max|dE| = 1.0e+00                     K20 FAIL dC +0.00%/+0.00%
```

Each exits 1 and prints `A42 COMPLETE: n/27 checks PASS.` with `n < 27`.

## Why `beta0` is the mutation that matters

It is not a perturbation of the lane — it is the lane's **premise**, executed. With β = 0 the branch's
Friedmann equation is `H² = H₀²[1 + Ω_m(1+z)³]`, so `H(z=0) = 1.147 H₀ ≠ H₀`: the model no longer has the
observed expansion rate, its distance ratios flip sign against Planck, and the dark-energy closure
`ρ_bare + ρ_β = ρ_DE` fails by exactly `Ω_mρ_crit` (1.4626 instead of 1). That is the whole content of
§3–§4 of the report, made executable: **β = 0 and a matter-filled universe at H₀ are mutually exclusive.**

## Why `theta_gr` is the second one that matters

It reproduces the arithmetic the task's item (3b) invites — put `Ω_c = 0.2666` and `Ω_b = 0.0497` in,
set `Ω_Λ = 1 − Ω_m`, and use the standard ΛCDM `E(z)`. That is a perfectly good model; it is just **not
this action's model**, because this action has `Λ_bare = ρ_crit` and a `(2+3β)` in front of the matter
term. Under the mutation the branch becomes indistinguishable from case (b) (`dC` difference 0.00 %) and
K19/K20 fail. The mutation is the sentence "the theory predicts ΛCDM at Ω_m = 0.3163", and the checks
refuse to let it pass.

## What the mutations do *not* touch

The mutation flag never touches the inputs of §1 (Λ_obs, the census, L_*, the Planck comparison values).
It only changes one coupling, one constant, or one equation at a time — the point is that the results
depend on the *structure*, not that arithmetic can be broken by changing an input. `no_c2` is the one
exception, included precisely because dimensional errors of that kind are the classic failure mode of a
`c = 1` action and it is worth seeing how loudly the checks shout (a factor 9×10¹⁶ on `ρ_bare/ρ_crit`).
