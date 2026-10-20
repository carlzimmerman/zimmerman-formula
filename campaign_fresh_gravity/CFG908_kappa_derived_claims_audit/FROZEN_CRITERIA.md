# CFG908: audit of the record's unaudited "κ derived" claims (frozen criteria, committed alone, before any script)

Block 900–909 (reserved in LEDGER.md, 485e8d85b). This is CFG894 prerequisite **P5** (KAPPA_DOORS.md): one audit note covering
Q010, G031, glm53's README and the gemini38 chain, citing AUDIT_GF2 (a755b66ca) and H061 (763086b23). It is an audit lane, not
a κ attempt: it derives nothing and adds no trial to the look-elsewhere count.

Standing facts restated (KAPPA_CAMPAIGN_RULES §0):
- **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095 on ρ_DE, κ_crit = 0.345 ± 0.078 on ρ_crit). The footings are never pooled.
- Z ≡ κ. No de Sitter–Unruh argument is cited for ½. Never "theory closed".
- GF2's "κ derived" is the singular-isothermal-sphere ratio σ²/v² = ½, not the law's κ (AUDIT_GF2, a755b66ca).

Disclosure (what was done before this file was written):
- I read the claim files listed in §1, CFG894's README / rules / doors / ledger intro / register, AUDIT_GF2, H061, CFG891's
  and CFG904's READMEs.
- I ran two sizing greps into a scratch directory (not committed) to choose a review filter that one reader can finish. The
  first (§6 pattern S1) returned 9,140 tracked-file lines. A negation-word filter of the kind frozen in §6 left 344 for manual
  review. The second (a slow tie-form regex) was stopped part way and is replaced in §6 by fixed-string anchors.
- No line was classified and no chain was computed before this commit.

## 1. The claims under audit (blobs pinned at HEAD when this file was written)

**Primary claims** (CFG894 ledger_intro "Record conflicts" items 1 and 3):

| id | claim | where (tracked) | blob |
|---|---|---|---|
| C1 | **Q010**: "κ=½: DERIVED as the closure coefficient of the dynamical face" (routes GF2 closure, Q001, Q007); "germ face tied by exact κ=1/n web" (GF1 R1e); cross-face junction = "rung 5" (carried postulate); "value anchored empirically" n_germ = 2.000102 ± 0.017 with three channels (germ tie, SPARC slope, BTFR slope b = 1.004 ± 0.011) | `qwen38_push/Q010_kappa_referee/FROZEN_CRITERIA.md` (pre-registered register-line text, line 88ff) | e982efcf2e29 |
| C2 | **G031**: "ρ_Λ = 4a₀²/(Gc²) ⟺ Λ_geom = 32πa₀²/c⁴: DERIVED (action level, sympy-exact 9/9)"; and its relatives G058 `one_constant_closure` / G052 "Ω_Λ = 32πa₀²/(3H₀²c²) … a Lean theorem, not a fit" (the tie used as a premise) | `glm53_push/G031_gr_fluid_action.py` (V1 at :73–77), `.out`, `lean/G031_fluid_action.lean`, `STATE.md:33`; `lean/G058_omega_from_a0.lean:185–190` | ff422718b3a0, 8cd9e76f74c9, 9cb61a653bfd, 6c4f46703e63, 5687df50bc6b |
| C3 | **glm53 README**: "κ = 1/2 is DERIVED (the reciprocal of the SPARC-measured mode count), a_0 = s/2" (`README.md:102`, also :43, :19); its source G002 (`kappa_pred = sy.Rational(1, 2)` at :231; "n = 2 -- the mode count SPARC selected ... NOTHING fitted (L232: mu_n(g/s) g = g_bar, integer by integer" at :14–16); `STATE.md:35` "κ = ½ = 1/n from SPARC (n = 2): DERIVED from data" | `glm53_push/README.md`, `G002_onefunction_construction.py`, `STATE.md` | 798f1173e7cc, 0dedd4d4727d, 6c4f46703e63 |
| C4 | **gemini38 chain**, Link 1: photocount μ_n(Y) = 1 − (1+Y)⁻ⁿ with n = (d+1)(d−2)/2 = 2 TT polarisations, Y = g/s_DE, so "a₀ = s_DE/2 … ⟹ κ = ½ with zero free parameters" | `gemini38_flash_push/FIRST_PRINCIPLES_DERIVATION_CHAIN_REPORT.md:43–54`, `first_principles_derivation_chain.py` (:31–32, :33–72), `FirstPrinciplesChainProof.lean` (link1 at :24–28) | d7e10a4f2835, 651ba85612d8, 086def3657f3 |

**Untracked / uncommitted Q010 material** (read by explicit path only; never by an untracked grep). Q010's README, results and
Lean are untracked: `qwen38_push/Q010_kappa_referee/README.md` (hash-object f4b2400c774f), `q010_referee.py` (759204ca46e9),
`q010_referee.out` (8d39b5cb1b4c), `q010_results.json` (95231732e809), `qwen38_push/lean/Q010_kappa_closure.lean`
(a6664fbfeab3). The "derived" lines that CFG894 found in qwen38 PREDICTIONS and STATUS are **uncommitted working-tree
additions** to `qwen38_push/PREDICTIONS.md` and `qwen38_push/STATUS_2026-09-15.md` (`git diff`), not committed text. These are
reported in a separate list, not in the tracked list.

**Secondary rows** (register rows whose chain is a sub-chain of a primary claim; classified through it, and their files enter
the §6 list if they still state "derived"): GF2 K520 and its README title, Q001 K549, Q007 K550, deepseek_moa K583 (all the
SIS ratio = C1's first step); GF1 K519 (= C1's germ step); G002 K578 (= C3); H017 K568 and PD07 K521 (polarisation count =
C4's class, H061); G052 K581 (= C2's tie-as-premise); R15 K591 (already retracted; list only).

## 2. Inputs and conventions

- Law: a₀ = κ_law c √(G ρ_DE), with κ_law a symbol (value ½ in the normal run). The record's "dark-energy unit" is
  s ≡ c√(Gρ_DE) (G002, GF1, gemini38). Friedmann: H_Λ² = 8πGρ_DE/3. All tests are symbolic in G, c, ρ_DE, a₀, σ, C, M, r.
- **Footing:** ρ_DE. Every κ statement here is a symbolic statement about a₀/(c√(Gρ_DE)), so no footing number is needed.
- **One report-only exception.** To reproduce GF1's printed n_germ = 2.000102, the script reads GF1's own registers from
  `deepseek_push/GF1_germ_flip/GF1_results.json` at run time, read only. They are the record's inputs under audit, not inputs to
  any derivation. The script itself contains no §2 forbidden literal (K1).
- No measured number enters any classification. W_data = [0.227, 0.607] (ρ_DE, width 0.380) is used only as the MENU spread
  threshold (KAPPA_CAMPAIGN_RULES §4) and in report-only lines.

## 3. Classification rules (frozen)

Each claim is reduced to its chain, and the step at which the value ½ for **the law's κ** enters is located.

- **VALID DERIVATION.** All of:
  - the output is the law's κ (a₀/(c√(Gρ_DE))) and equals ½ symbolically;
  - no ½ and no §2 target premise is put in upstream: Λ = 32πa₀²/c⁴, Gρ_Λ = 4a₀²/c², J = 1, W_v = 4, "premise A" (the unit
    c√(Gρ) with coefficient 1 posited), or a footing value (incl. A₀ = c√(Gρ)/2);
  - it survives the rename test (κ_law → 2/5: the output does not move, and the comparison with the law then fails);
  - it is not an identity (S2: it would give a different number if κ were different);
  - no forbidden input (§2 of the rules, incl. a measured value of the result upstream);
  - it is determinate over the chain's own unforced choices (spread < 0.380).
- **IDENTITY / INSERTION.** The target is written in. Subtypes:
  - **I-W** (written in): the tie or a literal ½ is substituted and then "verified", or the asserted relation holds identically
    once its premise is substituted (it holds for every κ).
  - **I-A** (premise A): the unit c√(Gρ_DE) is posited with coefficient 1 (or J = 1), so that κ = 1/(an integer) follows only
    from that choice of unit.
  - **I-M** (measured, relabelled): a measured or footing value of the result is used upstream. The output follows the data or
    the law (rename test: it moves with κ_law or with κ_true of the data).
- **DIFFERENT QUANTITY.** The ½ is a ratio that contains no a₀ normalisation against ρ_DE (e.g. σ²/v²). Test: its free symbols
  exclude {c, ρ_DE} or the a₀/ρ_DE combination, and the rename test leaves it at ½ while the law's κ moves.
- **MENU.** The chain's own unforced choices (unit, identification, count) give κ values spread by more than 0.380, ½ being one
  entry.
- **ERROR.** A recomputed algebra or logic step fails. The step is located.

**Headline rule.** The headline class is the class of the step at which ½ for the law's κ enters. Precedence when several apply
to that step: ERROR > DIFFERENT QUANTITY > IDENTITY/INSERTION > MENU > VALID DERIVATION. Every other class that applies anywhere
in the chain is listed as a secondary finding. A claim whose junction to the law's κ is a posit is never VALID.

**Expectation, disclosed (not a result).** From reading the files: C1 DIFFERENT QUANTITY (the SIS ratio) with the bridge = a
posit plus I-M (footing circularity, p62's subject); C2 I-W; C3 I-M plus I-A plus a literal ½ in G002; C4 I-A inside the
retracted polarisation-count class (H061, X5), MENU over the unit. The tests decide.

## 4. Tests (each printed PASS/FAIL with evidence; `cfg908_audit.py`, sympy + stdlib)

**C1 (Q010).**
- T1a SIS chain reproduced: ∇²(C ln r) = C/r²; Poisson ρ = C/(4πG r²); hydrostatics at constant σ² for ρ ∝ r^−γ gives
  σ² = C/γ, and γ = 2 is the unique self-sourced power law, so σ² = C/2; with v_c² = C, κ_dyn := σ²/v_c² = ½. Q001
  (c_s² = σ² = C/2) and Q007 (v_c² = 2σ²) reduce to the same ratio. PASS iff all three give ½ exactly.
- T1b symbol content: κ_dyn after substitution has no free symbols, and in particular carries no c and no ρ_DE.
- T1c rename (κ_law → 2/5): κ_dyn stays ½ while the law's κ is 2/5.
- T1d germ face (GF1 R1e): κ_germ := a₀/s with s := n a₀ minus 1/n is identically 0 (definition). n_germ := s/a₀_reg with
  a₀_reg = κ_law c√(Gρ′) gives n_germ = (1/κ_law)√(ρ/ρ′) symbolically, so it follows the law (1/κ_law = 5/2 under the rename).
  Report only: GF1's registers reproduce 2.000102, and the implied ρ/ρ′ is printed.
- T1e BTFR-slope channel: on the deep branch of μ_n(g/s), v⁴ = G M s/n, so d ln v⁴/d ln M = 1 for every n and every κ. PASS
  (channel uninformative on n and on κ) iff the slope is n- and κ-free. This is H061's I7 measurement rule.
- T1f junction: no equation in the chain's own set (log branch, Poisson, hydrostatics, C = √(G M a₀)) contains ρ_DE, so no
  equation links σ²/v² to a₀/s. Q010 itself labels the junction POSTULATED-CARRIED.

**C2 (G031, G058/G052).**
- T2a G031 V1 reproduced: with ρ_Λ = 4a₀²/(Gc²), (c/2)√(Gρ_Λ) − a₀ = 0.
- T2b generalised: with ρ_Λ = a₀²/(k²Gc²), k c√(Gρ_Λ) − a₀ = 0 for every k > 0. The check holds for every κ (S2 fails).
- T2c rename: κ_law = 2/5 against G031's tie (½ kept): κ_law c√(Gρ_Λ) − a₀ = −a₀/5 ≠ 0. The "derivation" returns its premise.
- T2d G031 V2: Λ = 8πGρ_Λ/c² = 32πa₀²/c⁴ follows from the substituted tie (identity given it).
- T2e G058: ρ_Λ/ρ_crit with the tie and Friedmann gives 32πa₀²/(3H₀²c²) identically; text check that the Lean
  `one_constant_closure` is witnessed by the tie itself (`refine ⟨4 * a0 ^ 2 / (G * c ^ 2), ⟨rfl, ?_⟩, ?_⟩`).

**C3 (glm53 README / G002).**
- T3a deep slope of μ_n is n; with Y = g/u the deep law gives a₀ = u/n, so κ = (u/s)/n. With u = s (G002's X = (g/s)²),
  κ = 1/n; with u = cH_Λ, κ = √(8π/3)/n.
- T3b n is measured: synthetic rotation-curve data in units of s (no constants), generated from the McGaugh RAR form
  g = g_bar/(1 − exp(−√(g_bar/a₀))) at a₀ = κ_true s, 60 log-spaced g_bar/s in [0.005, 5]. Fit μ_n(g/s) g = g_bar for
  n ∈ {1, …, 6} (best integer) and for continuous n (golden-section on [0.5, 8]), minimising the rms of log₁₀ g. Report n_best
  and n_cont at κ_true = ½ and 1/3. PASS (the integer is a measurement of κ) iff n_best = 2 at κ_true = ½ and n_best = 3 at
  κ_true = 1/3.
- T3c text check: G002 contains `kappa_pred = sy.Rational(1, 2)` and the L232 "integer by integer" selection line.
- T3d rename: at κ_true = 2/5, n_cont moves by more than 0.25 from its κ_true = ½ value.

**C4 (gemini38).**
- T4a deep slope of μ_2 is 2; N_pol(d) = (d+1)(d−2)/2 = 2 at d = 3.
- T4b κ(d, u) = (u/s)/N_pol(d): d = 3 → ½, d = 4 → 1/5, d = 5 → 1/9 at u = s (S3: the ½ is the d = 3 value only).
- T4c unit menu over the record's dS units u ∈ {s (premise A), cH_Λ = c√(8πGρ/3), c√(8πGρ) (= c²√Λ), c√(4πGρ)} at d = 3:
  κ ∈ {0.5, 1.447, 2.507, 1.772}. Print the π-weight of each κ². PASS (MENU) iff the spread exceeds 0.380, and record that the
  only π-free entry is the premise-A unit.
- T4d rename: κ_law → 2/5 leaves the output at ½ (it does not follow the law), so it is a value fixed by its posits.
- T4e text checks: `a0_canonical = s_de / 2.0` precedes Link 1; Link 1's "a0 = s / 2" is a printed string, not computed from
  the slope; the Lean `link1_graviton_modes_and_kappa` proves `(1 : ℝ) / 2 = 1 / 2` for its κ part.

**Identity checks (all claims).**
- K1 forbidden-literal grep of the script: none of 9.36e-11, 9.3603e-11, 9.3619e-11, 1.13e-10, 1.1312e-10, 1.1279e-10,
  1.2e-10, 5.7888, 0.1727, 0.417, 0.551, 0.465.
- K2 every κ expression printed symbolically with its free symbols.
- K3 scaling G → λG, ρ → μρ, c → νc (a₀ → ν√(λμ) a₀): every chain's κ output invariant.
- K4 rename test per chain, as in T1c, T1d, T2c, T3d, T4d.
- K5 π-weight of κ² per chain output.
- K6 every quoted record line is present at the pinned blob (git show, read only). A missing line fails that test.

## 5. Mutation control (`MUTATE=1`, separate `_MUTATE` outputs)

| control | change | expected |
|---|---|---|
| M1 | κ_law ½ → 2/5 for the whole run | n_germ → 5/2; the G031 V1-against-law residual → −a₀/5; κ_dyn stays ½; gemini38 stays ½ |
| M2 | SIS exponent γ = 2 → 2.1 | κ_dyn → 1/2.1 = 0.476 (GF2's own MUTATE value) |
| M3 | d = 3 → 4 in C4 | κ → 1/5 |
| M4 | unit u = s → cH_Λ in C3/C4 | κ → √(8π/3)/2 = 1.447; κ² gains π¹ |
| M5 | synthetic κ_true ½ → 1/3 in C3 | n_best 2 → 3 |

Classifications must not change under the mutations (an identity stays an identity). Exit codes (chain6 convention): the
normal run exits 0 when every test was evaluated and every reproduction check held, 2 on an internal failure; the MUTATE run
exits **1** when every control bites as expected, **3** if any fails to bite (the normal-mode verdicts are then void).

## 6. The file list: every tracked file that still states κ is derived

- **Pinned tree:** this file's own commit. Read only; nothing listed is edited.
- **Search** (`git grep -I -n` at the pinned commit, single thread, `nice -n 10`, over `*.md *.py *.tex *.txt *.lean *.out
  *.json`, `_external_data` excluded):
  - **S1** (κ with a derive word, case-insensitive): `(kappa|κ|\kappa)[^|]{0,60}deriv|deriv[^|]{0,60}(kappa|κ|\kappa)`.
  - **S2** (the tie and the coefficient in other forms): fixed-string anchors `a0^2`, `a0**2`, `a_0^2`, `a₀²`, `a_{0}^2`,
    `s/2`, `s / 2`, `32 pi`, `32pi`, `32π`, `32\pi`, `32*pi`, `32*np.pi`, `32*math.pi`, `32*sp.pi`; then, in Python, keep a line
    only if it matches a tie form (4a₀²/(Gc²) in any of these spellings, ρ_Λ/ρ_DE = 4…, 32π a₀²/c⁴, a₀ = s/2 or s_DE/2,
    (1/2)c√(Gρ) / c√(Gρ)/2, or "32π" with derive/explain within 40 characters) **and** a claim word on the line: deriv,
    theorem, certif, closes/closure, forced, first-principles/first principles, zero free, no free, not a fit, parameter-free,
    one constant, one number, not fitted.
- **Pre-filter (scripted).**
  - S1 lines are review candidates iff an assertive form matches: κ (optionally "= ½") followed within 50 characters by
    derived/DERIVED/derivable/derives, or derive(s)/derived/derivation of followed by κ.
  - Candidates from S1 or S2 are dropped iff the line itself carries an explicit negation or withdrawal: not derived / not
    derivable / not a derivation, underiv, non-deriv, never … deriv, no derivation, cannot … deriv, n't, fitted, void,
    withdrawn, retract, do not cite, never cite, circular, tautolog, naming, unmet, obligation, no-go, nothing, neither, nor,
    not, must not, non_claims, NOT_derived, adopted, quarantine, impossible. Before this test the booster phrases "not fitted",
    "no longer fitted", "not a fit" and "not measured" are removed from the line, so a strong claim of the form "derived, not
    fitted" is not dropped.
- **Manual review.** Every remaining candidate is read with ±2 lines of context and classed:
  - **A (correction candidate):** in its own voice, states that κ (or "the ½", a₀ = s/2, or the tie ρ_Λ = 4a₀²/(Gc²) /
    Λ = 32πa₀²/c⁴ / "the 32π") is derived, a theorem, forced, or a zero-free-parameter output, with no fitted / void /
    withdrawn / conditional caveat in the same passage (±3 lines).
  - **B (compliant or related):** caveated, conditional, a quotation that is refuted, a demand or plan ("derive κ"), or
    "derived" said of a different quantity that carries the name κ.
  - **C (unrelated):** another κ (Einstein κ = 8πG, epicyclic κ, curvature, κ(r), κ_t, κ_c …).
  Generated copies (an `.out` or `_results.json` of a listed `.py`, snapshots) are listed under their source and marked as copies.
- **Miss-rate check.** A seeded random sample (seed 908) of 40 lines from S1 ∪ S2 that the pre-filter did not select is read
  by hand. The number found to be class A is reported.
- **Separate list.** The untracked Q010 files and the uncommitted PREDICTIONS / STATUS additions (§1) are read by explicit path
  and reported apart from the tracked list.
- The list is report-only. No listed file is edited by this lane. The CFG894 register row and the LEDGER row are proposed in
  the README, not appended.

## 7. Verdict vocabulary (per claim, frozen)

Headline ∈ {VALID DERIVATION, IDENTITY/INSERTION (I-W | I-A | I-M), DIFFERENT QUANTITY, MENU, ERROR}, plus the secondary
classes found, plus the located step. Any K-check failure, or any mutation control that does not bite, voids the verdict for
the claims it touches (reported as VOID with the failing check).

## 8. Second prediction (S4)

Not applicable: an audit lane, not a derivation attempt. P_LEE is unchanged.

## 9. Resources and hygiene

Single core, `nice -n 10`, `OMP_NUM_THREADS=1`, under 1 GB, seconds per script (the git grep runs take about a minute each).
Tracked-file searches only; no untracked grep; no downloads. Only this lane's directory is written and committed; no push. No
personal names or home paths.
