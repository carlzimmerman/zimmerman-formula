# A78 — MUTATIONS

Eleven dials. Each changes **exactly one input** of the action or of one formula, is invoked as

```bash
A78_MUTATE=<name> python3 a78_checks.py ; echo $?
```

and every run exits **1**. Baseline (`A78_MUTATE` unset) is **30/30 PASS, exit 0**. Each mutation writes
`a78_MUTATE_<name>.out`; the `SUMMARY: n/30` line and the failing check names are recorded below from those files.

---

## 1. The dials

| name | the one input it changes | theory value | mutated value |
|---|---|---|---|
| `beta_sign` | sign of β in the θ² coefficient `c = 1 ± β` | `c = 1+β` | `c = 1−β` |
| `no_theta2` | the θ² coefficient itself | `c = 1+β` | `c = 0` (term deleted) |
| `clock_xi` | the clock coefficient ξ of `P^iD_i ln N` | `ξ = 1` | `ξ = 2` |
| `Z_eta` | the ηp² piece of the fifth mode's kinetic coefficient | `Z = B+ηp²` | `Z = B` |
| `tt_beta` | a spurious β in the TT kinetic coefficient | `1` | `1+β` |
| `G_factor` | the Friedmann normalisation `n` in `n(2+3β)H² = 2Λ+4Kρ` | `n = 3` | `n = 2` |
| `static_shift` | the shift field in the "static" ansatz `N^i = c r r̂` | `c = 0` | `c = 0.05` |
| `frw_ansatz` | the denominator of the hand-written reduced FRW Lagrangian | `4K` | `8K` (a factor 2) |
| `gamma_factor2` | the gradient stiffness γ | `γ = KL*²/2` | `2γ` |
| `W_quad` | the functional form of `W(u)` (hence the interpolation `u(g)`) | log, `u = a₀g/(g+a₀)` | quadratic, `KW'=u` ⟹ `u = g` |
| `tt_trace` | the mode used for the tensor check | `diag(h₊,−h₊,0)` | `diag(h₊,h₊,h₊)` (a scalar) |

## 2. Results — exit code, pass count, failing checks

| mutation | exit | SUMMARY | checks that FAIL |
|---|---|---|---|
| `beta_sign` | **1** | 19/30 | C02_FRW2, C04_K16, C06_STAB, C09_SHARP, C17_B, C18_Z_b1, C18_Z_b3, C19_ZSIGN, C20_RATIO, C29_BBN, C30_BARE |
| `no_theta2` | **1** | 15/29 | C01_FRW, C02_FRW2, C03_GEFF, C03b_GEFF, C04b_ROOT, C05_LAM0, C06_STAB, C09_SHARP, C17_B, C18_Z_b1, C18_Z_b3, C19_ZSIGN, C20_RATIO, C29_BBN |
| `clock_xi` | **1** | 26/30 | C11_LAW, C12_AQUAL, C24_IDENT, C27_XI |
| `Z_eta` | **1** | 29/30 | C22_UVSPEED |
| `tt_beta` | **1** | 28/30 | C15_CT2, C16_TTBETA |
| `G_factor` | **1** | 25/30 | C02_FRW2, C03_GEFF, C03b_GEFF, C05_LAM0, C30_BARE |
| `static_shift` | **1** | 26/30 | C07_THETA, C08_BTERM, C09_SHARP, C10_DSDB |
| `frw_ansatz` | **1** | 29/30 | C01_FRW |
| `gamma_factor2` | **1** | 28/30 | C13_ALPHA1, C22_UVSPEED |
| `W_quad` | **1** | 28/30 | C11_LAW, C12_AQUAL |
| `tt_trace` | **1** | 29/30 | C14_TTTHETA |

(`no_theta2` reports 29 checks rather than 30 because the root-find branch of C04 is replaced by the
`C04b_ROOT` failure record — the mutated background has no real `H²` solution at all.)

## 3. Coverage, per check

| check | broken by |
|---|---|
| C01_FRW | `frw_ansatz`, `no_theta2` |
| C02_FRW2 | `beta_sign`, `no_theta2`, `G_factor` |
| C03_GEFF, C03b_GEFF | `no_theta2`, `G_factor` |
| C04_K16 | `beta_sign` (`no_theta2` → `C04b_ROOT`) |
| C05_LAM0 | `no_theta2`, `G_factor` |
| C06_STAB | `beta_sign`, `no_theta2` |
| C07_THETA, C08_BTERM | `static_shift` |
| C09_SHARP | `beta_sign`, `no_theta2`, `static_shift` |
| C10_DSDB | `static_shift` |
| C11_LAW, C12_AQUAL | `clock_xi`, `W_quad` |
| C13_ALPHA1 | `gamma_factor2` |
| C14_TTTHETA | `tt_trace` |
| C15_CT2, C16_TTBETA | `tt_beta` |
| C17_B, C18_Z_b1, C18_Z_b3, C19_ZSIGN, C20_RATIO | `beta_sign`, `no_theta2` |
| C22_UVSPEED | `Z_eta`, `gamma_factor2` |
| C24_IDENT | `clock_xi` |
| C27_XI | `clock_xi` |
| C29_BBN | `beta_sign`, `no_theta2`, `G_factor` |
| C30_BARE | `beta_sign`, `G_factor` |

## 4. The three checks no single-input mutation breaks, and why they are kept

`C23_DET` (det M = 4, symbolic vs numerical), `C26_SHIFT2` (the `O(ε²)` ratio 4.000) and `C28_SMAT` (`ω²` invariance
under `σ → λσ`) are **identity checks**: both sides are computed from the same action by different routes, so a dial
that changes the action moves both sides identically and cannot separate them. They are not assertions and no dial was
constructed to fake a failure. They are kept because each one *is* a step of the Task-2 argument:

* `C23_DET` is the non-degeneracy certificate of the redundancy system (its content is that `R₃` and `K_ijK^ij` carry
  different Weyl weights, which is why `G_N` and `c_T` are independent measurements). Their ratio is definitional, so
  the only "mutation" would be to change a Weyl weight — a change of mathematics, not of an input.
* `C26_SHIFT2` is the proof that a shift redefinition is on-shell trivial (it *is* the second-order structure of the
  eliminated action).
* `C28_SMAT` is the proof that a uniform field rescaling cannot move `ω²` (every quadratic term scales by λ²).

Checks that could not be made to fail and asserted nothing beyond a definition were **deleted**, with what replaced
them:

| deleted | why |
|---|---|
| `C21_PSC` (`η p_sc²/B < 1e−80`) | a derived number, not a check. Now printed in `a78.out` and quoted in the report (`1.1328e−89`). |
| `C05b_LAM` (plug the closed form back into the exact equation) | pure algebra: the residual is 5.6e−17 by construction. Now printed. |
| `C23b_FULL` (`det ≠ 0`) | implied by `C23_DET` (`det = 4`). |
| `C25_SHIFT` (`dL/dY = 0` at `Y*`) | a tautology: `Y*` is *defined* as the stationary point. `C26_SHIFT2` carries the content. |

## 5. What the mutations demonstrate

The four dials that touch the β-sector (`beta_sign`, `no_theta2`, `clock_xi`, `G_factor`) each break between 3 and 14
checks, and they break **different** ones: the sign of β is caught by the ghost/sign and Λ-slope checks; deleting θ² is
caught by the Legendre/background checks; the clock coefficient is caught by the law; the Friedmann normalisation is
caught by `G_eff/G_N` and the BBN bound. No single dial breaks everything, which is the point: β's four channels
(algebra sign, fifth-mode kinetic term, law normalisation, background normalisation) are independently instrumented.
