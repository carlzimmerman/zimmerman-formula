# M6N1_minimum_patch_need: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** What is the **minimum** fraction of cosmic baryons, F_need, that must start in M6's depleted patches for the
galaxies that need M6 to be cold-dark-energy-poor today? Is that minimum above or below the M6 patch budget that X57
allows (F_allowed)? If even the minimum exceeds the budget, the forest-derived budget decides M6. If the minimum sits far
below it, the forest bound cannot bite unless retention is low.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. The new piece: a minimum patch-born fraction x_min (derived, not assumed)

- **The patch.** An M6 patch has cold-to-baryon ratio (1 + δ_c,in)/(1 + δ_b,in) × (Ω_c/Ω_b). Here 1 + δ_c,in = f_max
  (X22's allowed cold share) and δ_b,in = (Ω_c/Ω_b)(1 − f_max), so the patch is compensated.
- **Outside material** carries the fair ratio Ω_c/Ω_b.
- **The mixture.** A galaxy whose baryons are a fraction x patch-born and (1 − x) outside-born has cold share, relative to
  fair,

  r(x) = (1 − x) + x f_max / (1 + δ_b,in).

  This assumes cold material accompanies its baryons in the same proportion it had initially. That is the no-exchange
  result of X54 (ξ consistent with 0) together with collisionless co-infall.
- **The cap.** The galaxy must satisfy r ≤ f_max (X22's capture cap), which gives

  **x_min = (1 − f_max) / (1 − f_max/(1 + δ_b,in))**.

- **Where the numbers come from.** f_max per footing is read from X22's committed JSON; δ_b,in comes from P1D1's native
  background (committed JSON).

## 2. Requirement

F_need(q, ε) = x_min · q · F_inv / ε.

| symbol | meaning |
|---|---|
| F_inv | the galaxy baryon inventory as a fraction of cosmic baryons |
| q | the mass share of that inventory in galaxies that need M6 |
| ε ∈ (0, 1] | retained galaxy baryons over initial patch baryons |

- **Minimum (ε = 1).** The whole patch ends up in the galaxy, so F_need,min = x_min q F_inv.
- **Reference retention (record-native).** ε_ref = 1/(1 + δ_b,in). This is X22's Lagrangian mapping: a galaxy of law mass
  M_b is assigned the Lagrangian volume of total mass (Ω_m/Ω_b) M_b. In a compensated patch that volume holds
  (1 + δ_b,in) M_b of baryons.
- **Critical retention.** ε_crit = F_need,min / F_allowed. The budget is violated whenever ε < ε_crit.

## 3. Inputs

Read at run time from the closure program's population run, with a sha256 check:
`closure_program_2026_10_27/population/run/results.json`, sha256 0131d5da47e442c92dfd716fda8b5d036b0808940079fc8e0dd62d2445746323.
That run's sources are Driver et al. 2022, Jones et al. 2018 and Fletcher et al. 2020, on the native h.

| input | value |
|---|---|
| F_inv, stellar only (lower) | `census/F_star` = 0.046987 |
| F_inv, stars + cold gas (central) | `census/F_cold_baseline` = 0.059787 |
| q_lo | **0.30**: Alpaslan et al. 2015's ungrouped stellar-mass fraction. Ungrouped galaxies are isolated and below the crossover, so they follow the law and need M6. This is a published marginal and not an isolation-selected measurement |
| q_hi | `gsmf/mass_ranges/1e9_to_1e11/fraction_of_fitted_stellar_mass` = 0.69145. All galaxies at 1e9–1e11 M☉, the range where the law is tested and passes. This includes satellites, so it is an upper bracket |
| F_allowed | P1D1 native `backgrounds/native/m6/<foot>/Fb_max_z3` (0.06132 / 0.04895). X57's provisional variance budget, **not** a measured forest limit; P1D1–P1D3 are all NOT DIAGNOSTIC |

**Step 0 (stop rule).** The sha256 matches. Every input above is reproduced to 4 decimals. f_max is read from X22 and
δ_b,in from P1D1.

## 4. Verdict per footing (frozen)

Four corners are evaluated: q ∈ {q_lo, q_hi} × F_inv ∈ {stellar, stars + cold gas}.

| verdict | condition |
|---|---|
| **M6 OVER BUDGET EVEN AT FULL RETENTION** | F_need,min > F_allowed at all four corners |
| **BUDGET BINDS AT RECORD RETENTION** | F_need,min ≤ F_allowed at all four corners, but F_need(ε_ref) > F_allowed at all four corners |
| **BUDGET DOES NOT BIND** | F_need(ε_ref) ≤ F_allowed at all four corners |
| **MIXED** | anything else. The corners that flip are named |

Reported for every case:
- ε_crit at each corner, against ε_ref;
- the ε at which F_need = F_allowed;
- the q at which F_need,min = F_allowed.

## 5. Checks and twin

- **K1. x_min.** The closed form equals a brute-force root of r(x) = f_max on a 1e-7 grid, within 1e-6.
- **K2. Accounting identity.** At ε = ε_ref, x = 1, q = 1 and F_inv = 1/(1 + δ_b,in), F_need = 1. Any baryon in a galaxy
  of Lagrangian origin then fills the patch.
- **K3. Limits.** f_max → 1 gives x_min → 0, because no exclusion is needed. f_max → 0 gives x_min → 1.
- **K4.** Peak RSS < 1 GB.
- **MUTATE (`M6N1_MUTATE=1`, separate outputs).**
  - m1: the cap is r ≤ 1, a wrong cap that gives x_min = 0.
  - m2: the sha256 target is altered.
  - The twin must fail Step 0 and K1.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I m6n1_need.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.
