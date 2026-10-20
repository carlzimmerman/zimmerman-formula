# κ attempts ledger (CFG894, 2026-10-20)

This file lists every κ derivation or selection attempt found in the record. The law is a₀ = κ c √(G ρ_DE), and **κ = ½ is
FITTED**. Equivalent forms: Λ = 32π a₀²/c⁴, G ρ_Λ = 4 a₀²/c², Z = cH_Λ/a₀ = √(32π/3) = 5.7888 (Z is never ~21). Deriving Z,
the "32π", the "4" or the "¼" is the same problem as deriving κ.

**How this file is made.** The tables below are rendered by `kappa_campaign_lee.py` from `kappa_attempts_register.csv`. That
CSV is the source: one row per attempt, append-only, ids K001… The same script prints the counts and the look-elsewhere
numbers into `kappa_campaign_lee.out`. If you edit the CSV, rerun the script; never hand-edit the tables.

**Where the rows come from.** Five read-only sweeps on 2026-10-20 covered sonnet55_push/puzzle_32pi (p01–p63, agents A–Z,
EXT01–04), sol61_push (top level, puzzle_32pi, puzzle_32pi_*_2026_10_14/15 and later lanes), real_research and its reviews,
reviews/, kappa_closure, nbody_2026, fable_independent_2026 (kappa_slot_2026, lean_2026, L-lanes), opus_48/49,
qwen_claude_field_theory, campaign_fresh_gravity, campaign_fresh_gravity_astra, argon_push, deepseek_push, qwen*,
the other model pushes, hunt_2026, project_atomos, predictions_2026, RETRACTIONS.md and STANDING.md. Rows that repeat the same
mechanism in another file were merged into one; pure re-runs are marked `audit`. Every commit hash was checked to exist.
Rows marked `untracked` are files on disk that are not committed (31 sol61 Oct-14/15 directories, the p62/p63 scripts, the
10-20 KAPPA_LOGIC Lean file, and the gated brute-force verdict, which `.gitignore` hides through its `*brute*` pattern).

## Totals ({{N_ROWS}} rows)

- **{{N_DERIV}} derivation or selection attempts.** That excludes observational, audit, Lean and κ-blind rows.
- **None derives κ = ½.**
- **{{N_TRIALS}} produced a number.** {{N_DET}} produced one determinate value; {{N_MENU}} are menus of several values from
  admissible variants. Every other attempt ended in one of four ways:
  - a condition equal to the target,
  - a free ratio, or a trade for a new constant,
  - a bound,
  - a closure.
- {{N_OBS}} rows are measurements (κ determinations, not derivations), and {{N_PEND}} are registered but unrun.

**{{N_DET_IN}} of the {{N_DET}} determinate values land inside today's 2σ data window {{WINDOW}}.** That window is CFG493's
κ_Λ = 0.417 ± 0.095.
- Every landing is an O(1) number that the window cannot separate from ½.
- They are mostly the same few values, recurring: 0.461 (Z = 2π), 0.482 (Z = 6, Verlinde), 0.55–0.557 (particle horizon,
  Nariai).
- The rate (about 33%) is what a random draw from the record-natural number set gives (27–28%; see
  `kappa_campaign_lee.out`). So the landings are no evidence that any route knows κ.

**{{N_HALF}} attempts output exactly ½, and every one was voided or left conditional.** That is about one attempt in seven.
The ½ got in by one of these routes:
- inserted or written in (CFG43, CFG187, G031);
- posited (the free-fall surface gravity c²/2R*, i.e. J = Gρr²/c² = 1);
- tuned (p20c, AS651.C01, lens q = 4, cosmic-string Gμ = 3/16);
- by naming, where a different quantity was called κ (the SIS ratio σ²/v² in GF2, Q001, Q007, Q010 and deepseek_moa; I14's
  lattice coupling);
- by a channel or polarisation count (PD07, H017, kimik3, gemini38: a retracted class);
- by circularity (GF1's n = 2 and the Ω_Λ selectors);
- by a gauge or algebra error (graviton normalisation A; EXT02).

**Historically, then, P(flawed | the output is ½) = 1.** The campaign rules (`KAPPA_CAMPAIGN_RULES.md`) are built around that
fact.

## What each family showed (one paragraph each; the tables give the rows)

- **HT, horizon/thermal.** Every identification uses a₀ and H only.
  - The π-parity obstruction applies (L4, LN5, CFG263). The outputs are rational × π^k with k odd, so never ½. The values
    cluster on Z ∈ {1, 2, 2π, 6, ½}.
  - The 2π landing (κ = 0.461) is data-consistent and recurs, but it is one input (T_GH = ħH/2π) wearing several hats.
  - The KMS "derivation" of 0.4607 (RT-17) was later withdrawn by RT-19 (a 4π error, giving 2cH_Λ). PAPER6 and some notes still
    present 0.4607 as coefficient-free. **Record conflict, listed below.**
- **HE, holographic/entropic.** The Bekenstein–Hawking ¼ carries ħ⁻¹, while a₀ is ħ-free (RT-18, CFG264).
  - CKN and the seesaw are identities (FL12, RR-24/25).
  - Verlinde's 6 (0.482) lands in the window, but its local term fails SPARC (p34) and its shape test fails 0/16 (CFG117).
- **VM, vacuum matching.**
  - The a₀ sector's vacuum constant is a zero mode in every local action (k01, AS067, AS069, ARGON01, sol61 non-selection
    Lean).
  - Natural kernel vacua give κ ≈ 1, which is excluded.
  - Tail and cutoff versions trade κ for a turn-off y_t ≈ 129. Detached TNOs likely exclude that turn-off (p56), and Cassini
    rejects the whole QUMOND/BIMOND class (p58).
- **FN, normalisation of W and the action.**
  - The four-form gives a free ratio Z/β² (k04, AS651–658).
  - Spectral functionals obey the reparametrisation theorem: a probe, never a derivation (RT-12).
  - The gated brute force (six action classes) found no survivor.
  - a₀-as-field (p63) is registered but unrun.
- **PS, π-counting and geometry.**
  - 32π is 8π × 4 and carries no geometric meaning (k05). About 60 horizon/vacuum principles give q·π^±1 (L4).
  - Nariai (0.557) evaluates outside its own static patch.
  - The free-fall surface gravity gives ½ only by positing J = 1. No physical object has radius c/√(Gρ) (RV-25).
- **GB, graviton bath.**
  - The ε_tot = 1/(32π) slot is not live: it double-counts S_dS (KS01).
  - Mode counting spans 161× (RV-40).
  - The polarisation-count class is retracted (H061).
- **TA, topological.** η = 0 on the round dS S³ (theorem-grade). Forced halves sit in the wrong slot; anomalies give integers
  or need inserted constants.
- **QG.** Asymptotic-safety exponents are type-mismatched; DSSYK was computed to fail; the RG, dilaton and large-N ratios give
  the wrong numbers.
- **KS, kinetic and cold-energy dynamics.**
  - SIS σ²/v² = ½ is a different quantity (AUDIT_GF2).
  - CFG893 (131bedf33): the c-free cold-energy system is invariant under S_λ (x→λx, M→λ³M, a₀→λa₀). Any c-free balance
    therefore makes a₀ depend on galaxy mass or holds for every a₀, and κ needs c. **This is now a campaign rule.**
- **CC, cosmological ties.**
  - Unimodular (XR20), the clocks and the horizons tie a₀ to Λ without fixing κ.
  - The particle horizon (0.55) is an epoch coincidence that fails the flat a₀(z) record.
  - Ω_Λ-from-a₀ "selectors" are circular (CFG835).
- **NU, numerology.** Base rates:
  - ½ appears in 0.94% of an 852-form principle grammar (p60);
  - 10.8% of ≤3-operation numbers fall in a 2σ band (KS04);
  - 596 closed forms lie within 1% of Z (RT-22).
- **OB, measurements, not derivations.** The primary is CFG493. Never quote 0.551 ± 0.043, 0.465 ± 0.076 (use 0.450 ± 0.073),
  SPARC 1.0766e-10 or the p48 pool.
- **AU/LN, audits and Lean.** κ is independent of every committed premise set (L3, sol61-104).
- **EX, pasted derivations.** All circular or erroneous.

## Record conflicts and hygiene items found by this sweep (not fixed here; read-only lane)

1. **Q010 versus AUDIT_GF2.**
   - qwen38_push/Q010_kappa_referee calls GF2 "UPHELD-QUALIFIED: DERIVED (dynamical face)" and never engages AUDIT_GF2
     (a755b66ca).
   - Only Q010's criteria are committed (0eb0b4d07); its README, results and Lean are untracked.
   - qwen38 PREDICTIONS and STATUS repeat "derived".
   - **AUDIT_GF2 stands: GF2's ½ is the SIS ratio, and changing the law's κ leaves it at ½.** Q010 must not be cited.
2. **RT-17 versus RT-19.** The KMS 0.4607 "first predicted κ" was withdrawn by RT-19 (4π error → a₀ = 2cH_Λ). PAPER6
   (F04 in the sweep) and AS066 still present 0.4607 as a coefficient-free horizon value. Which one stands should be settled
   before anyone cites "the dS tie gives 0.461".
3. **Never separately audited:**
   - G031's "ρ_L = 4a₀²/(Gc²) DERIVED (action level)": same tie-written-in class as CFG43;
   - glm53's README "κ = ½ DERIVED";
   - the gemini38 photocount chain: retracted class.
4. **Stale index.** fable_independent_2026/kappa_slot_2026/KS00_INDEX.md lists KS01 only (KS02–KS08 exist).
5. **Unreproducible from the repo.** opus_48 review memos cite /tmp scripts that are not in the repo (ROUTE2, ROUTE4, ROUTE5,
   AEST-joint, FRONTIER1, CLASS3, CLASS6, MECH4, ETA).
6. **Untracked:** KAPPA_GATED_ACTION_BRUTEFORCE_VERDICT_2026-06.md (hidden by the `*brute*` .gitignore pattern) and the 31
   sol61 Oct-14/15 directories.

## Registered, unrun (run these before launching anything that overlaps them)

- p62 (GF1 pin audit).
- p63-C1, C1b, C2 and C3 (a₀ as a field: cosmic bound charge, patch bootstrap, flux lattice, Kaloper–Sorbo ħ audit). Criteria
  2a36f4ae5, errata 5e5a10e33 and a1e430de1.
- KAPPA_LOGIC_2026_10_20.lean (the 32π chat; compile in lean_2026).
- Nine deepseek AS proposals that were never executed.

## Active parallel efforts (do not duplicate)

- **The "32pi squared puzzle" chat.** It is auditing the empirical provenance of the measured κ values and doing the logic/Lean
  argument (KAPPA_LOGIC).
- **CFG893.** κ from the new cold-energy structures. DONE 2026-10-20: NOT SELECTED (131bedf33).
- **CFG895.** The α (fine-structure) ledger: a separate constant and a separate lane.
