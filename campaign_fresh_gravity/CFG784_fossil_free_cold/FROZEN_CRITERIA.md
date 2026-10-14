# CFG784 FROZEN CRITERIA: fossil free cold energy in dwarfs, with CFG782's derived selector

Committed alone, before any script or number. 2026-10-14. Block CFG780–789.
Source: agent A's draft (`THEORY_PUSH_2026-10-14/A_ufd.md` §7), with one change: the selector is CFG782's, frozen first.

## Conditional
Run ONLY if CFG782's verdict is SELECTOR VIABLE or BORDERLINE. If CFG782 is DEAD, CFG784 is not run and is recorded as
"not run: selector dead".

## Question
- Systems flagged SUDDEN by CFG782 (photo-evaporated at reionization) keep their original baryons' cold energy as free,
  untethered, collisionless mass: M_free = 5.364 (R_ind − 1) M_b,now.
- RETAINED systems carry none.
- Does this close the MW UFDs (+0.325 dex) without breaking the MW classicals, M31 dSphs or LV field dwarfs?

## Declared calculation (no new constant)
- **R_ind:** CFG317 per object (nominal yield −0.2; ends −0.5 / +0.1 reported).
- **Selector:** CFG782 at its primary setting (canonical, T_IGM 1.5e4 K); the bracket ends are reported.
- **Free profile (P1):** isothermal, truncated at the top-hat radius r_f of the collapse mass M_coll = R_ind M_b,now / f_b
  (f_b = 0.157) at z_f = 8 (CFG336; z_f = 6 / 10 reported).
  - r_f = (3 M_coll / (4π · 18π² · ρ̄_m(z_f)))^{1/3}, with ρ̄_m from Ω_m 0.308, h 0.70.
  - Inside r_f, M_free(<r) = M_free r/r_f, so σ_free² = G M_free/(3 r_f) at r ≤ r_f.
- **Dispersion.** σ_pred² = σ_law² + G M_free(<r)/(3r) at r = (4/3) r_half (the AUDIT_UFD estimator: σ² = g r/3).
  - σ_law from the AUDIT_UFD harness (isolated law, Υ_V 2, condensed source).
  - The free term is Newtonian and does not feed the tether.
- **Statistic.** AUDIT_UFD's KM median of log(σ_obs/σ_pred) with upper limits, bootstrap 1000 seed 42, Υ_V 1–4 floor.
  Classicals: CFG336/AUDIT stars-only harness.

## Pass / fail (canonical decides; alt reported)
- **P-UFD:** |z| < 2 for the MW UFD KM median at the nominal yield.
- **P-SAT:** MW classicals |z| < 2.
- **P-FIELD:** LV field |z| < 2 (from CFG317 objects with σ in the LVD local-field table).
- **SOLVES** = all three pass. **PARTIAL** = P-UFD passes and one other fails. **FAIL** otherwise.
- SPARC is untouched by construction if CFG782 S2 passed; reported.

## Controls
- K1: M_free ≡ 0 reproduces AUDIT_UFD's +0.3245 (canonical) to 1e-3.
- K2: r_f for M_coll = 10⁷ M☉ at z_f = 8 is checked analytically (printed).
- MUTATE M1: shuffle R_ind across UFDs (seed 784). The UFD median must change by ≥ 0.02 dex, or the per-object
  correlation must vanish.
- MUTATE M2: selector off (every system gets fossil cold energy). P-SAT or P-FIELD must fail, which reproduces agent A's
  trade.

## Hand estimate (agent A)
- UFD +0.325 → about −0.04 (P-UFD PASS).
- With the selector sparing the classicals and the field, those stay at +0.10 / −0.04 (pass).
- **Expected: SOLVES if CFG782 is VIABLE; PARTIAL if borderline classicals are flagged.**

## Disclosures
- In UFDs this is behaviourally a cold halo of native mass, and is reported as such.
- The two-population postulate is not derived.
- κ fitted; not theory closed.
