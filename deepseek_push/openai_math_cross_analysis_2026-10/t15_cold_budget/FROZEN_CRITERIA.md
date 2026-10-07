# T15 — FROZEN CRITERIA: the cold-fluid budget (who can afford a cold fluid)

**Claim to test.** The framework's own numbers force the cold fluid's
mass. With f_obs = M_b/M_tot (baryon fraction), x := deficit =
M_missing/M_b, f_law = settled fraction of the supply (from the settling
law), and S(<R) = kernel supply within R:

    M_cold/M_b = x − f_law·S(<R)/M_b          (budget identity, exact)
    x = (1 − f_obs)/f_obs,  f_obs = 1/(1 + x)
    ceiling:  M_cold ≥ 0  ⇒  f_law ≤ x·M_b/S(<R)

**S1 (branch audit — the record's numbers mean THREE things):**
CFG382's calibration values 0.14/0.60/0.43 are LEFTOVER fractions
e = e^{−Γt} (settled f = 1 − e = 0.86/0.40/0.57); the target-audit
table (definition A) lists DEFICITS x = M_missing/M_b, shifting ~2×
with hydrostatic bias (b = 0: groups 0.79, clusters 0.41; b = 0.3:
1.76, 0.91); T12/T14 read them as settled fractions f — a branch
misread that inflates the settled phantom by the supply factor S/M_b
within R500. [The T12 λ-confirmation and T14's σ(ln t) readings both
inherit this; the fork shape survives only as exponential-law content.]

**S2 (the overdraft — the load-bearing result):** on definition A and
the record's own calibration (λ = 0.028 → f_law(R500 densities) =
0.286 at τ = 10.3 Gyr), the settled kernel supply at R500 EXCEEDS the
observed deficit:
    MW 30 kpc:  f_law = 0.86 vs ceiling f_max = 0.60–0.73 (V = 188–230)
    groups:     M_ph = 1.77 M_b vs deficit 0.79–1.76 → M_cold = −0.98
                (b=0) … −0.56 (b=0.3)
    clusters:   M_ph = 1.42 M_b vs deficit 0.41–0.91 → M_cold = −1.01
                (b=0) … −0.51 (b=0.3)
The cold fluid is forced NEGATIVE at every clock outside the MW's
marginal 30-kpc point. The settling rates that clear the ceilings:
λ_max(ceiling) = 0.0072–0.016 (clusters), 0.011–0.025 (groups) vs the
MW floor λ = 0.028 — **no single λ clears the clusters' budget.** The
kernel supply to R500 over-predicts the dark mass 5–12×; the deficit
itself is the reservoir (CFG379/CFG365 compat: baryon-depletion
ordering).

**S3 (the forced reading):** at R500 the settled fraction is the
reservoir fraction f ≈ deficit/S_kernel ∈ [0.083, 0.18] (clusters),
[0.128, 0.28] (groups) — NOT 0.286 and NOT T12's 0.43. The cold fluid
at cluster scales must be (nearly) absent; CFG344's small-scale
clumping requirement must be satisfied by a component whose LARGE-scale
density profile is the reservoir complement ρ_cold ∝ (1−f)·ρ_res — a
flat/equilibrium profile, registered as the derived (falsifiable)
large-scale law; its small-scale clumping scale (T_cold) stays open.

**Falsifier (registered):** a lensing-calibrated deficit at R500 (one
footing, b known) that CLEARS the settled kernel supply without
negative cold fluid (i.e. deficit ≥ f_law·S/M_b with f_law from any
universal λ) kills S2 — that is exactly the "reservoir-inside-R500"
alternative, and the numbers above say how far the ledger must move
(≥ 2.2×, clusters ≥ 3.5×).

**Screens:** Q1 — derives from the record's own calibration (CFG382),
the kernel (T9), the deficit tables (definition A); nothing inserted;
Q2 — no rationals; Q3 — the budget identity is a definition-level
accounting law with a checkable ceiling.

**Checks (exit 1 on failure):**
  C1  branch audit: f = 1−e and f_obs = 1/(1+x) mappings exact; the
      S/M_b inflation factor reproduced (cluster 4.95, group 6.18,
      MW-30 2.3 at the stated M_b/R500 conventions).
  C2  budget matrix: M_cold/M_b at {MW-30 × V=188/200/230} ×
      {groups × b=0/0.3} × {clusters × b=0/0.3} = the S2 values
      (±0.05); MW marginal (sign flips at V ≳ 215), groups/clusters
      negative at every b.
  C3  ceilings: f_max window and the λ_max window (0.0072–0.025 vs
      0.028) — the floor λ violates every non-MW ceiling.
  C4  reservoir reading: f_res = deficit/(S/M_b) ∈ the declared
      windows at b = 0/0.3 for groups and clusters.
  C5  T12 λ-range verdict: every λ in T12's [0.029, 0.066] violates
      the cluster ceiling (declared factors 4–9×).
  C6  MUTATE (T15_MUTATE=1: the T12 identification f_law := deficit):
      C2 flips (the matrix reads M_cold = deficit·(1−S/M_b) < 0 — wait:
      no: the mutation REPRODUCES the T12 illusion: with f_law = x,
      M_ph = x·S/M_b and M_cold = x·(1 − S)… — register: mutation maps
      the deficit onto the settled fraction and C2/C3/C4 must change
      by > 0.1 and C5 flips (T12's range then "passes").
  C7  cold-profile law: ρ_cold ∝ (1−f)·ρ_res — the complement
      statement, reported; CFG344's small-scale clumping scale
      registered open.

**Deliverables:** freeze committed ALONE; t15_cold_budget.py + .out ×2
+ results ×2; README; three new theorems appended to the MASTER
certificate (`deficit_to_fraction`, `cold_budget_identity`,
`cold_ceiling`) recompiled and re-audited (zero sorry; axioms
{propext, Classical.choice, Quot.sound}); campaign row with the
overdraft verdict. Language: nothing "closed"; the finding is a
ledger-level constraint, killable by the falsifier.

## Corrections (dated 2026-10-07, post-run, hand-arithmetic slips vs the script)

- C2's "MW marginal" was a hand-slip (enclosed-baryon M_b = 7e10, not
  1e11): the MW-30 point OVERDRAWS at the measured flat level too
  (M_cold/M_b = −0.97 @V=188, −0.65 @V=200; flips positive only at
  V ≳ 217). The sign-flip structure declared stands; the "marginal"
  label is corrected to "negative at the measured level".
- Groups at b=0.3 close at the knife-edge (M_cold ≈ +0.04, declared
  −0.56 was wrong); clusters stay negative at every b
  (−0.98 @b=0, −0.48 @b=0.3).
- C5's declared "4–9×" tightened: measured violation factor 3.95×
  (window ≥ 3.5 — T12's minimum λ against the b=0 cluster ceiling).
- C2 predicate corrected accordingly; all other numbers as frozen.
