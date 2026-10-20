# CFG908 — audit of the record's unaudited "κ derived" claims (CFG894 P5)

Block 900–909. Criteria `FROZEN_CRITERIA.md`, committed alone first (122af8ada). Audit lane: it derives nothing and adds no
trial to the look-elsewhere count. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095 on ρ_DE). Not theory closed.

## Verdict: none of the four claims derives the law's κ

The algebra in every chain reproduces; no algebra error was found. Each claim fails because of what its ½ is taken to mean.

| claim | what it says | headline class | where the ½ for the law's κ enters |
|---|---|---|---|
| **C1 Q010** | "κ = ½: DERIVED as the closure coefficient of the dynamical face" | **DIFFERENT QUANTITY** | The ½ is σ²/v_c² of the singular isothermal sphere. The step to the law's κ is a posited junction ("rung 5"), plus a germ face that is a definition, plus a footing-circular anchor |
| **C2 G031** | "ρ_Λ = 4a₀²/(Gc²) ⟺ Λ = 32πa₀²/c⁴: DERIVED (action level)" | **IDENTITY / INSERTION (I-W)** | V1 substitutes the tie and then checks it. The same check passes for every κ |
| **C3 glm53 README / G002** | "κ = 1/2 is DERIVED (the reciprocal of the SPARC-measured mode count)" | **IDENTITY / INSERTION (I-M)** | n = 2 is the integer that SPARC fits of μ_n(g/s) select with s held fixed. That is a measurement of 1/κ, rounded to an integer |
| **C4 gemini38 chain** | photocount μ₂, n = 2 TT polarisations, Y = g/s ⟹ "κ = ½ with zero free parameters" | **IDENTITY / INSERTION (I-A)** | The occupancy Y = g/s_DE posits the unit c√(Gρ_DE) with coefficient 1 (premise A). Any other unit in the record gives a different, π-odd value |

`cfg908_audit.py` (sympy and stdlib, about 1 s): 20/20 tests and 6/6 identity checks pass (exit 0). MUTATE: 6/6 controls bite
(exit 1).

## C1 — Q010 (DIFFERENT QUANTITY; the junction is posited)

- **T1a.** GF2's chain reproduces: ∇²(C ln r) = C/r², ρ = C/(4πGr²), and hydrostatics give σ² = C/γ. The two-point argument
  2^−γ = ¼ gives γ = 2, so κ_dyn = σ²/v_c² = ½. Q001 (c_s² = σ²) and Q007 (v_c² = 2σ²) reduce to the same ratio.
- **T1b–c.** κ_dyn has no free symbols at all: no c, no ρ_DE, no a₀. With the law's κ renamed to 2/5, κ_dyn stays ½. It is the
  isothermal ratio, as AUDIT_GF2 (a755b66ca) found. Q010's README never cites AUDIT_GF2 or a755b66ca (checked by text).
- **T1f.** None of the chain's equations (log branch, Poisson, hydrostatics, C = √(GM_b a₀)) contains ρ_DE. So nothing links
  σ²/v² to a₀/s. Q010 itself labels this junction POSTULATED-CARRIED.
- **T1d.** The germ face is a definition: κ_germ := a₀/s with s := n a₀, so κ_germ − 1/n ≡ 0. The "empirical anchor"
  n_germ = s/a₀_reg uses a footing a₀, which is itself a κ = ½ statement, so n_germ = (1/κ_law)√(ρ/ρ′). It is 2 by construction
  and becomes 5/2 under the rename. GF1's registers reproduce 2.0001015. The 1e-4 offset is a ρ_Λ input drift (ρ/ρ′ = 1.000102),
  not physics. This is exactly the forbidden input A₀ = c√(Gρ)/2 (rules §2). p62, registered and unrun, remains the formal GF1
  audit and is not duplicated here.
- **T1e.** The third anchoring channel, the BTFR slope b = 1.004 ± 0.011, cannot see n. On the deep branch v⁴ = GM s/n, so
  d ln v⁴/d ln M = 1 for every n and every κ (H061's measurement rule I7). The second channel, the SPARC slope, is G002's
  integer (C3).
- **Reading.** Q010's "UPHELD-QUALIFIED: DERIVED (dynamical face)" restates AUDIT_GF2. GF2's ½ is real, but it is the SIS ratio,
  and the bridge to a₀ = κc√(Gρ_DE) is a posit plus a circular anchor.
- **Secondary rows** (same class, inherited): Q001 K549, Q007 K550, deepseek_moa K583, and the "triad" lines in G205, g03g and
  G152.

## C2 — G031, with G058 and G052 (IDENTITY / INSERTION, I-W)

- **T2a.** V1 reproduces. G031.py:73–74 sets `rhoL_of_a0 = 4*a0**2/(G*c**2)` and then checks
  `sqrt(G*rhoL_of_a0)*c/2 - a0 == 0`.
- **T2b.** With ρ_Λ = a₀²/(k²Gc²), the residual k c√(Gρ_Λ) − a₀ vanishes for every k > 0. The check cannot fail, whatever κ is
  (S2).
- **T2c.** Against a law with κ = 2/5, G031's tie returns −a₀/5. The "derivation at the action level" is its own premise.
- **T2d.** V2, Λ = 32πa₀²/c⁴, follows from the substituted tie.
- **T2e.** G058's `one_constant_closure` is witnessed by the tie itself
  (lean:190 `refine ⟨4 * a0 ^ 2 / (G * c ^ 2), ⟨rfl, ?_⟩, ?_⟩`). Ω_Λ = 32πa₀²/(3H₀²c²) is the tie rewritten through Friedmann.
  The "+0.07% of Planck" uses a footing a₀ built from Planck's Ω_Λ, which is circular, as the register already says for G052
  (K581) and Q002 (K551).

## C3 — glm53 README / G002 (IDENTITY / INSERTION, I-M; also I-A and a literal ½)

- **T3a.** The deep slope of μ_n is n. With Y = g/u, the deep law gives a₀ = u/n, so κ = (u/s)/n.
  - κ = 1/n only because G002 writes X = (g/s)², i.e. the unit s = c√(Gρ_Λ) with coefficient 1 (I-A).
  - With u = cH_Λ the same family gives √(8π/3)/n.
- **T3b, synthetic test** (units of s, no constants, McGaugh RAR shape):
  - data at κ_true = ½ select n_best = 2 (continuous n = 1.835);
  - data at κ_true = ⅓ select n_best = 3;
  - data at κ_true = 2/5 move the continuous n to 2.23 (T3d) and still select n = 2.

  So "the SPARC-measured mode count" is the measured κ, coarse-grained to reciprocals of integers. G002's own docstring
  (:14–16) says the integer was chosen by fitting μ_n(g/s) g = g_bar with s fixed, "integer by integer".
- **T3c.** G002.py:231 sets `kappa_pred = sy.Rational(1, 2)` and compares it with the fitted ½.

## C4 — gemini38 Link 1 (IDENTITY / INSERTION, I-A; MENU over the unit; retracted class)

- **T4a–b.** The slope of μ₂ at the origin is 2, and N_pol(3) = 2, so κ = 1/N_pol(d) at u = s: ½ at d = 3, 1/5 at d = 4, 1/9 at
  d = 5. The ½ is the d = 3 value only (S3).
- **T4c.** Over the record's de Sitter units at d = 3, the same chain gives:
  - 0.5 for s (premise A, π-weight 0);
  - 1.447 for cH_Λ;
  - 2.507 for c√(8πGρ);
  - 1.772 for c√(4πGρ).

  The last three are π-weight 1. The spread is 2.0, against a window width of 0.380. The ½ belongs to the one unit that is
  premise A.
- **T4d.** The output stays ½ whatever the law says. It is a value fixed by its posits: the unit, the occupancy n̄ = g/u
  (asserted, not derived), and κ = 1/(polarisation count). The last is the retracted class X5 (H061; H017 K568, PD07 K521).
- **T4e, script hygiene.**
  - `a0_canonical = s_de / 2.0` is set at line 32, before Link 1 (line 34).
  - The conclusion "a0 = s / 2 ==> kappa = 1/2" is a printed string (line 70); nothing in the script assigns a₀ or κ from the
    computed slope.
  - The Lean `link1_graviton_modes_and_kappa` proves `(1 : ℝ) / 2 = 1 / 2` for its κ part (line 27).
- **The deepseek PD01–PD22 series** (STANDING: do not cite) uses the same family. Its μ = 1 − (1−p)² with p = Y/(1+Y) is μ₂
  with Y = g/s, and its "s fixed independently of a₀" is premise A. So the same I-A finding applies to it. This is inherited,
  not recomputed separately.

## Mutation control (`cfg908_audit_MUTATE.out`, exit 1, 6/6 bite)

| control | change | result |
|---|---|---|
| M1 | law κ ½ → 2/5 | n_germ → 5/2; G031 V1 → −a₀/5; κ_dyn stays ½; the gemini38 output stays ½ |
| M2 | γ 2 → 2.1 | κ_dyn → 10/21 = 0.476 (GF2's own MUTATE value) |
| M3 | d 3 → 4 | gemini38 κ → 1/5 |
| M4 | unit s → cH_Λ | κ → √(8π/3)/2 = 1.447, π-weight 1 |
| M5 | synthetic κ_true ½ → ⅓ | n_best 2 → 3 |
| classes | — | all four headlines unchanged |

## The file list: tracked files that still state κ is derived (read only; nothing listed was edited)

**How it was built** (FROZEN_CRITERIA §6):
- Search: `git grep` at the pinned tree 122af8ada, over tracked text files.
  - S1 found 9,162 κ + derive lines.
  - S2 found 45,067 anchor lines, of which 4,267 carry a tie form.
- The pre-filter left **973 candidates in 704 files. All 973 were read by hand**: 200 are class A, 677 B and 96 C.
- Class A totals **200 lines in 142 files**. Of these, 47 lines are generated copies (`.out` / `_results.json` / snapshots of a
  listed source).
- Full table: `cfg908_filelist_A.csv`. Every hand class is in `cfg908_manual_review.csv`. Quoted text in the CSVs is redacted
  for names; paths are kept as identifiers.

**Recall checks.**
- **Miss-rate.** In a seeded sample of 40 non-selected lines, 1 is A-like (m31): a step line in an AS066 snapshot of PD08, inside
  a file that is already listed.
- **A recall hole in the frozen search, disclosed.** S1's `[^|]` means a markdown table row with κ and DERIVED in different cells
  is never seen. I found this because glm53 STATE.md:35, a claim line already verified by K6, was missing from the list.
  - A post-freeze supplementary scan (`cfg908_filelist.py supplement`, `cfg908_supplement*.csv`; the frozen list is unchanged)
    found 4 candidates, 2 of them A: `glm53_push/STATE.md:35` and `deepseek_push/G152_inventory_revision.md:112` (the SIS
    triad called κ, DERIVED).
- **Known claim lines that no keyword search sees.** The claim audit itself located these lines. They are written as LaTeX,
  sit in table cells, or have no derive word on the line:
  - `glm53_push/STATE.md:42` (Ω_Λ "DERIVED + Lean CERTIFIED").
  - `glm53_push/README.md:26–27` (Ω_Λ "a Lean theorem (G058), not a fit").
  - `glm53_push/lean/G058_omega_from_a0.lean:183–184` ("the parameter count of the dark-energy sector is ZERO").
  - `glm53_push/G002_onefunction_construction.py:54, 56, 231, 256` (OUTPUTS "all derived"; κ = 1/n = 1/2; the literal; "is now
    the DERIVED output"), and its copy in `.out:102`.
  - `gemini38_flash_push/FIRST_PRINCIPLES_DERIVATION_CHAIN_REPORT.md:53–54`.
  - `gemini38_flash_push/first_principles_derivation_chain.py:32, 69, 70`.
  - `gemini38_flash_push/FirstPrinciplesChainProof.lean:25, 27`.
  - `qwen38_push/Q010_kappa_referee/FROZEN_CRITERIA.md:88–92`. This is the pre-registered conditional register-line text, so the
    frozen rule puts it in class B. It is the only committed copy of Q010's "DERIVED" wording.

### Class A, sources (the record outside the `ai_slop/` archive; 42 source files)

The audited claims and their direct relatives:
- `glm53_push/README.md`: 19, 43, 102 — the tie "with zero free parameters"; "kappa = 1/2 derived, Lean 4"; "κ = 1/2 is DERIVED (the reciprocal of the SPARC-measured mode count)"
- `glm53_push/STATE.md`: 33, 35 (supplement), 42 (known line) — rung 0 (G031), rung 2 (G002), rung 9 (G052/G058)
- `glm53_push/G031_gr_fluid_action.py`: 75 — V1 (claim C2)
- `glm53_push/G002_onefunction_construction.py`: 471 (+ known lines 54, 56, 231, 256) — derived = ["a_0 = s/2", "kappa = 1/n = 1/2", …]
- `glm53_push/G005_derived_length_cassini.py`: 8; `glm53_push/G007_bimetric_door.py`: 140; `glm53_push/G015_the_equilibrium_board.py`: 72, 88, 150 — "a_0 = s/2 DERIVED"
- `glm53_push/REFEREE_ATTACKS.md`: 128 — "kappa = 1/2 = 1/n is DERIVED"
- `glm53_push/THE_EQUILIBRIUM_THEORY.md`: 110 — "κ=½ derived as 1/n from the SPARC integer"
- `qwen38_push/STATUS_2026-09-15.md`: 21 — "G002 derives kappa = 1/2"
- `hy4_push/H001_zimmerman_aest_action.py`: 121, 389 — "kappa = 1/2 derived as the reciprocal of the measured mode count n = 2 -- not fitted"
- `deepseek_push/THEORY.md`: 14 — "a₀ = s/2 … DERIVED from a measurement"
- `gemini38_flash_push/grand_synthesis_derivation.py`: 11 — "derives kappa = 1/n = 1/2 from pure spatial dimensionality"
- `deepseek_push/GF2_closure_half/GF2_closure_half.py`: 3, 43, 357, 384; `README.md`: 1; `STATE.md`: 45 — GF2's "κ = ½ derived" (none of these files references AUDIT_GF2 or a755b66ca; checked)
- `deepseek_push/G205_results.json`: 16, 37; `deepseek_push/g03g_flatness_n2.py`: 22; `deepseek_push/G152_inventory_revision.md`: 112 (supplement) — the SIS triad called κ and derived
- `deepseek_push/GRAVITY_EVERYWHERE.md`: 49 — cites G031 V1/V2 as making Λ and a₀ one number
- `deepseek_push/G163_cosmic_noon.py`: 253, 336, 449, 520 — the tie "closes the measured DE density … zero cosmological input" (circular: the footing a₀ is a κ = ½ value)

The polarisation-count series (PD; STANDING: do not cite):
- `deepseek_push/PD01_polarization_count.py`: 2; `PD03_two_halves.py`: 41, 181, 182, 183; `PD08_particle_free_derivation.py`: 2; `PD19_referee_report.md`: 5
- `deepseek_push/STATE.md`: 111, 129; `deepseek_push/FALSIFIER_MATRIX.md`: 34; `deepseek_push/ZD01_phantom_ceiling.py`: 13, 56; `deepseek_push/ZD_README.md`: 14, 39; `fable_independent_2026/lean_2026/ZD01_phantom_ceiling.lean`: 19 — "the framework's DERIVED constant (PD01–PD13)"
- `real_research/clock_2026/L311_phantom_law.py`: 6 — "kappa = 1/2 (PD08-derived: a0 is NOT a fit)"
- `real_research/reviews/OPUS49_BRIDGE_CLOSURE_2026-09-22.md`: 46 — "kappa = 1/2 remains derived by the PD08/PD22 composition route"

Other:
- `deepseek_push/TOE_STATUS.md`: 77 — "32 = the kernel's 2² × Einstein's 2³" (the 32π "explained")
- `gemini_pi_puzzle/SPIN2_PROJECTION_DERIVATION.md`: 1; `gemini_pi_puzzle/test_spin2_projection.py`: 4 — "microscopic derivation of κ = 1/2 and 32π" (register K575, VOID)
- `gemini_pi_puzzle/THEORY_AND_DERIVATION.md`: 1, 133 — "Deriving a₀ = c²√(Λ/32π)" (register K574, VOID)
- `fable_independent_2026/L169_single_metric_action.py`: 47; `fable_independent_2026/SINGLE_METRIC_ACTION.md`: 42 — "derived κ" said in passing
- `opus_48_extended_research/THE_HONEST_LCDM_STRESS_BRIEF.md`: 135 — a suggested verbatim pitch: "a specific, derived acceleration scale a₀ = c²√(Λ/32π)"
- `prep_2026/mi_fingerprint/PRIOR_ART.md`: 42 — "Z = sqrt(32pi/3) derived from the horizon footing"
- `qwen_claude_field_theory/closure_2026/HANDOFF_2026-08-31.md`: 16 — "horizon-derived a₀ = ½c·H_Λ/Z"
- `real_research/WHITEPAPER_geometric_gravity.md`: 228 — "c²√(Λ/32π) (derived from Λ)"
- `real_research/msa3d_a0z_confrontation.py`: 16 — "horizon-derived a0"

**Copies.** These clear when their source is fixed:
- `glm53_push/`: G031 .out:50, _results.json:6; G002 .out:106, _results.json:60; G005 .out:7; G015 .out:42, :78, _results.json:7, :43
- `hy4_push/H001_results.out`: 22, 165
- `fable_independent_2026/L169_single_metric_action.out`: 11
- `deepseek_push/`:
  - GF2 .out:75, _MUTATE.out:75, the four results JSONs (156/161)
  - PD01 .out:1; PD03 .out:40, :80, :82 and results.json:43, :48; PD08 .out:1, :94 and results.json:37
  - ZD01_results.json:12; G163 .out:33, :54 and results.json:148, :188
  - THE_EQUILIBRIUM_THEORY.md:110 (copy of glm53's)
  - lanes/G031_gr_fluid_action.py:75 and .out:50
  - the AS060/AS066 snapshots of PD01/PD08 (7 lines)

### Class A, the `ai_slop/` archive (97 lines in 68 files, 5 of them copies)

These are the archived Z² = 32π/3 framework's claims that "Z² = 32π/3 is derived": from 8D compactification, T³/Z₂ orbifold
singularity resolution, Friedmann × Bekenstein–Hawking, or cube × sphere. Since Z ≡ κ, each one is a "κ derived" claim. Two
need attention first:
- `ai_slop/.zenodo.json:3` lists "MOND acceleration a₀ = cH₀/Z where Z = 2√(8π/3)" among what the framework "derives". This
  is deposited metadata.
- `ai_slop/website/public/LAGRANGIAN_FROM_GEOMETRY_v5.4.0.tex`:267, 306 is a public website copy.

The other lines:
- `papers/GN_Z11_Z2MOND_PAPER.md`:35 ("Z = √(32π/3) … derived from the geometry of a T³/Z₂ orbifold")
- the five `manuscript/v8.2.0/` files zimmerman_formula_v8.5.0, v8.6.0, v8.7.0, v8.8.0 and v8.8.8 `.tex` ("Z² = 32π/3 … fully derived"; 24 lines)
- `papers/` (LAGRANGIAN_FROM_GEOMETRY, Z2_UNIFIED_ACTION*, ALPHA_FIRST_PRINCIPLES_DERIVATION, PARTICLE_MASSES_FROM_GEOMETRY,
  generate_complete_pdf.py)
- 42 `research/` files (49 lines)
- `examples/18_cosmological_constant/run.py`:159 ("Λ(derived) = 32πa₀²/c⁴")
- `research/quantum_implications/quantum_data_evidence.py`:104 (`rho_Lambda_derived = 4*a0**2/(G*c**2)`)

Every file:line is in `cfg908_filelist_A.csv` and `cfg908_filelist.out`.

### Separate list: untracked and uncommitted Q010 material (read by explicit path; not in the tracked list)

**Untracked:**
- `qwen38_push/Q010_kappa_referee/README.md`: 7, 15, 18, 66, 71. Line 71 proposes replacing the canonical "MEASURED, not derived"
  register line (S1 L13) with the DERIVED reading.
- `q010_referee.py`: 248, 280, 281; `q010_referee.out`: 49, 101, 103; `q010_referee_MUTATE.out`: 54, 106, 108.
- `q010_results.json`: 55 ("POSTULATED->DERIVED-STATIC (GF2/Q001/Q007)").
- `qwen38_push/lean/Q010_kappa_closure.lean`: 4, "the kappa = 1/2 closure chain". Its own line 30 calls the junction a carried
  postulate.

**Uncommitted working-tree additions** (`git diff`, author not this lane):
- `qwen38_push/PREDICTIONS.md`: 78, 80 ("VERDICT: kappa = 1/2 is DERIVED as the closure coefficient").
- `qwen38_push/STATUS_2026-09-15.md`: 52 ("UPHELD-QUALIFIED").

**Allowed replacement** for any listed line (KAPPA_CAMPAIGN_RULES §10): "κ = ½ is FITTED (CFG493). <Route> gives <its quantity>:
the SIS ratio σ²/v² = ½ (GF2, Q001, Q007); a definition or substitution of the tie (G031, G058); the SPARC integer n = 2, a
measurement of 1/κ (G002); or ½ under the posited unit c√(Gρ_DE) (gemini38, PD). None of these derives the coefficient of
a₀ = κc√(Gρ_DE)."

## Consequences for CFG894 (not applied here; that lane's files are not this lane's)

- **Record conflict 1 (Q010 versus AUDIT_GF2): resolved in AUDIT_GF2's favour.** K548's "UNRESOLVED CONFLICT" can read "audited
  CFG908: DIFFERENT QUANTITY (SIS ratio); junction posited; n_germ footing-circular; BTFR anchor blind to n".
- **Record conflict 3 (G031, glm53 README, gemini38): audited.**
  - G031 (K580): I-W, as registered.
  - G002 / glm53 README (K578): I-M, a measurement relabelled.
  - gemini38 (K573): I-A inside the retracted class, as registered.
- Proposed register row (the next free id after K600; append-only; for CFG894 to add):
  `K601,CFG908,AU,campaign_fresh_gravity/CFG908_kappa_derived_claims_audit,"audit of the four unaudited 'kappa derived' claims (Q010, G031, glm53 README/G002, gemini38) in sympy with rename and mutation controls",,,audit,0,"none derives the law's kappa: Q010 DIFFERENT QUANTITY (SIS ratio; rung-5 junction posited; n_germ footing-circular; BTFR anchor blind to n); G031 IDENTITY (tie substituted then verified; holds for every kappa); G002 MEASUREMENT RELABELLED (SPARC integer with s fixed; literal 1/2); gemini38 PREMISE-A INSERTION (menu 0.5-2.5 over units; d = 3 only); 200 class-A lines in 142 tracked files still say derived",<this lane's result commit>`

## What this lane does not claim

- It does not claim κ is underivable in general. It says these four routes do not derive it.
- It does not discredit the reproduced algebra: the SIS ratio (GF2), the deep slope of μ_n, and the tie identities are all
  correct as algebra.
- It does not test G002's SPARC fit itself. The synthetic test shows only that such an integer tracks κ_true.

## Files

- `FROZEN_CRITERIA.md`
- `cfg908_audit.py`, with `.out`/`.json` (normal run, exit 0) and `_MUTATE.out`/`_MUTATE.json` (exit 1)
- `cfg908_filelist.py` (`extract`, `supplement`, `merge`):
  - `cfg908_extract.out`, `cfg908_filelist_candidates.csv`, `cfg908_missrate_sample.csv`
  - `cfg908_manual_review.csv`, `cfg908_missrate_review.csv`
  - `cfg908_supplement.out`, `cfg908_supplement_candidates.csv`, `cfg908_supplement_review.csv`
  - `cfg908_filelist_A.csv`, `cfg908_filelist.out`

**Rerun** from the repo root:

    OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_audit.py
    MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_audit.py

Each `git grep` pass takes about a minute and uses one thread:

    nice -n 10 python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_filelist.py extract
    nice -n 10 python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_filelist.py supplement
    python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_filelist.py merge > campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_filelist.out
