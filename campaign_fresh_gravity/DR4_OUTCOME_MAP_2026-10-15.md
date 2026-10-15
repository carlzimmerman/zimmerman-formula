# Gaia DR4 wide binaries: outcome map and one gap in the frozen rule (2026-10-15)

**Status: a reading aid, written 2026-10-15, before DR4 (ESA's planned date 2026-12-02, not fixed).** It changes no frozen number, cut,
threshold or sealed file. It is NOT an amendment: the owner decides whether any of it is filed into
`prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` (inline, hash-stamped, as Amendments 1-21 were). Sources are named per line.
κ = ½ is fitted, not derived. The cold mass is still required. Nothing here says the data favour the framework.

## 1. What is registered, and on which statistic

| item | where | prediction | its own kill |
|---|---|---|---|
| Arm A (boost) | prereg Amendment 12/13 table | γ_v 1.1614-1.1814 canonical / 1.1917-1.2267 alt | falsified well below its floor (see 3) |
| Arm B | prereg (f) | 1.0000 ± 0.0025, "not a testable arm" | killed from above at 1.084 |
| Arm C (ownership) | prereg Amendment 12(d) | γ_v = 1.000, exactly Newtonian | falsified at γ̂ 1.084-1.23 if the stability requirements pass |
| settling model | prereg Amendment 21 | the same number as Arm C | scored by Arm C's rows |
| CFG740 (stiffness) | `CFG740_sealed_wb_slope2`, sealed 10-13 | essentially no boost, log-slope 2 (γ_v-1 = 8.9e-4 at 50 kAU) | γ_v ≥ 1.01 at s ≤ 50 kAU |
| CFG800 rule | `CFG800_wb_2026_scoring/FROZEN_CRITERIA.md`, 10-15 | R-1 < 0.01 | "FRAMEWORK KILLED" if R-1 ≥ 0.01 at ≥ 3σ |

Statistics differ. The prereg scores the pooled γ̂ over 3-30 kAU, with σ_tot = 0.028 at the frozen N = 30,000, of which σ_sys = 0.02
is irreducible (Amendment 7: 3σ is unreachable at any N). CFG800 scores R, the median ṽ beyond the MOND radius (s ≤ 50 kAU) over the
Newtonian-regime normalization, with Cookson's quality checklist.

## 2. Outcome map for the prereg statistic (rows quoted from Amendment 12(d), σ_tot = 0.028)

| γ̂ lands in | Arm C / settling model | Arm A | MOND (R ≈ 1.15-1.20) |
|---|---|---|---|
| ≤ 0.916 | disfavoured | every registered arm disfavoured | disfavoured |
| 0.916-0.944 | 2-3σ below, not a kill | not stated in the row | disfavoured |
| 0.944-1.056 | **consistent** | **falsified** (≥ 3.8σ below its canonical floor); the arm question is decided for C over A | disfavoured |
| 1.056-1.084 | disfavoured at 2-3σ, not a kill | "no arm verdict" per the row | disfavoured |
| 1.084-1.23 | **falsified** if the stability requirements pass | see Arm A's own rows | the frozen guard zone starts at 1.20 (contamination only raises γ̂) |
| > 1.23 | no verdict | no verdict | no verdict |

"Disfavoured" for MOND is my arithmetic: (1.15-1.00)/0.028 = 5.4σ. A Newtonian result is never confirmation over Newton or over
Arm B (same number), and must not be described as evidence for the framework over general relativity (Amendment 12(e)).

## 3. The gap: CFG800 does not define σ

CFG800's rule says "at ≥ 3σ" and "at 2σ" and defines no error model. The outcome depends entirely on which σ is used.

- With the prereg's σ_tot = 0.028: **KILLED** needs R-1 ≥ 3σ = 0.084, so R ≥ 1.084. That is exactly the prereg's own 1.084 edge for Arm C.
  The "0.01" in the rule then does nothing.
- With the same σ_tot, **CONSISTENT** ("|R-1| < 0.01 at 2σ") cannot be reached: a 2σ interval is ±0.056, far wider than 0.01. Every
  result then falls in UNDECIDED or KILLED. "MOND excluded" is still reachable through the z-rule (5.4σ above), not through the
  CONSISTENT class.
- CFG800's 0.01 thresholds are meaningful only if σ_R ≤ ~0.003 (kill) or ~0.005 (consistent). That would need a statistical-only
  error budget, which is not the prereg's.
- Scope: CFG800's "FRAMEWORK KILLED" is stronger than the rows of Arm C, which stays alive until 1.084. CFG740's own falsifier
  (γ_v ≥ 1.01 at s ≤ 50 kAU) kills the stiffness construction CFG740, not the Arm C ownership rule. A result with γ̂ in 1.01-1.084 would
  read "CFG740 killed, Arm C alive, Arm A falsified or no-verdict (row dependent)".

**FILED 2026-10-15 as Amendment 22** (`prep_2026/gaia_dr4_prep/AMENDMENT22_HASH.txt`): sigma_R = max(sigma_tot, R's own error); KILLED needs R-1 >= 0.01 and >= 3 sigma_R; CONSISTENT needs 2 sigma_R <= 0.01 (unavailable at sigma_tot); "FRAMEWORK KILLED" means CFG740's stiffness construction; Arms A, B, C and the settling model keep their own rows. The three decisions below were settled that way under the owner's instruction to file.

**Decisions that were open before filing:**
1. Which σ governs the CFG800 rule (σ_tot of the prereg, or a stated alternative). Record it in a dated file.
2. Whether "FRAMEWORK KILLED" in CFG800 is re-worded to "CFG740 killed".
3. Whether this note, or part of it, is filed as Amendment 22 into the prereg (with the SHA-256 stamp).

## 4. Required reporting at scoring time (already in the record)

Report raw γ̂ with its distance to every arm (Amendment 7(c), "label trap"); never a single verdict word. Apply the frozen cuts, the
NSS screen and the stability requirements as written; add no new cuts after DR4 (CFG800).

## 5. Not verified here

No script was run. Arm A's rows above the table and the in-force edges inside `wide_binary_pipeline.py` were not re-read; the pipeline's
in-force constants govern (Amendment 14/19). CFG800's σ may be defined in a file I did not open (only `FROZEN_CRITERIA.md` and the README).
