# CFG187 — AeST with a Henneaux–Teitelboim Λ-tie: the time-flow reading as one candidate, and its scorecard

- **Frozen question:** `FROZEN_QUESTION.md`, written before any script. Its sha256 and UTC time (21:21:28Z) are in `FROZEN_QUESTION_SHA256.txt`. §0 of that file discloses what I had already read. The scorecard is therefore an assembly of numbers I knew, not a blind test.
- **Script:** `CFG187_aest_tie.py`, about 5 s (MUTATE=2 about 11 s). It imports `CFG4_common` read-only for the constants and kernels, and writes nothing outside this directory.
- **Runs:**

| mode | checks | rc | what it does |
|---|---|---|---|
| main | 18/18 | 0 | the construction (L1–L8), controls C1–C6, reported rows, the scorecard |
| `MUTATE=1` | 16/18 | 1 | unties a₀ from Λ. **L1 and L7 fail, as required.** Only the scorecard rows 3.11 and 5.13 change. |
| `MUTATE=2` | 14/18 | 1 | ties a₀ to the flow's expansion θ = ∇·A. **L1 and L5 fail, as required** (L3 and L7 also fail). a₀(z)/a₀(0) = 1.322, 1.791, 3.769, 8.294 (+0.576 dex at z = 2.5), the rival law. Rows 3.10, 3.11 and 5.13 change. |

κ = ½ is FITTED and the tie is POSTULATED. Nothing here says the theory is closed, that the data favour the framework, or that a dark-matter particle exists. In this candidate the dark mass is a state of the scalar field, and that mass is still required.

## Bottom line

**The Λ-tie can be written into AeST cleanly, but it is bookkeeping.**
- Λ stays one global constant, so a₀(z) is exactly flat.
- The tie adds no local degree of freedom.
- On shell the theory *is* AeST with a₀ = ½c√(Gρ_Λ).
- Untying it changes no data row (MUTATE=1).

**On the record's own committed numbers, this candidate does worse than candidate B on most rows where the two differ.**
- Better on 2 rows: Chae's external-field signal, and having an action at all.
- Worse on 13 rows. Two things drive this:
  - **The external-field effect (EFE) applies everywhere:** the satellites, the Coma UDGs, DF2, and the Sun's own phantom.
  - **AeST's dust adds to MOND rather than replacing it:** X-COP and KiDS.
- Same status on 11 rows.

The binding failures are:
- the Solar System: the EFE quadrupole is 3.99–5.69× the Q₂ ceiling, and α₁ ≈ −4 is carried from the record's v9 kill;
- X-COP, which fails on both readings of where the dust sits;
- the record's own KiDS closure of AeST (Δχ² ≥ +106).

**Gaia DR4 on 2 Dec 2026 separates this candidate from B.** This candidate predicts Arm A (1.16–1.18); B predicts Arm C (1.000).

**Relation to the record.**
- This agrees with `STANDING_2026-09-28.md`, which lists the AeST-type route among the excluded relativistic completions.
- It fills the gap CFG172 left: that lane scored Einstein-aether and khronon variants of door 11C but put AeST-type vector–scalar models out of scope.
- The tie construction is XR20 T1 / CFG43, applied to AeST's 𝒥.

## For the owner, in plain words

AeST is the best-developed published theory built like your time-direction picture. It has two fields:
- a field that marks the flow of cosmic time (the "aether", with no rest mass and no particle);
- a scalar field.

The scalar field does two jobs:
- **its change in time** behaves like dark matter on cosmic scales (a state of the field, not a particle);
- **its slope in space** gives MOND's extra pull in galaxies.

I wrote your rule a₀ = ½c√(Gρ_Λ) into it using the record's unimodular trick. That works and costs nothing: Λ becomes a single constant fixed once for the whole universe, a₀ cannot drift with time, and nothing new propagates. But the data cannot tell the tied version from the untied one. The tie explains nothing yet; it only records the coincidence inside the equations. κ = ½ is still fitted.

Two points bear on your picture directly:
- **The "compaction" does no work in AeST.** The flow's expansion rate (how fast the time-flow spreads out) does not appear in AeST's equations at the cosmic level. If a₀ is tied to that expansion rate instead, a₀ follows H(z): the rival law, not your flat one.
- **The whole theory, scored against the record's gate list, fails more than it passes where it differs from B.** The main reason is that AeST has the "external field effect": a system inside a bigger one (a satellite inside the Milky Way, the Sun inside the Galaxy) gets less boost. The record's data say B's rule, which ignores the host, fits the satellites, the Coma dwarfs and the Solar System better. AeST's dark matter also piles on top of MOND in clusters and around galaxies, where the data want one or the other, not both.

This is a scoped result about one published theory with one added tie. It is not a verdict on your picture as a whole.

## 1. The action (declared in the frozen question)

This is the record's transcription of Skordis & Złośnik 2021, eq. 5 (`real_research/bridge1_aest_equations.md`), with the tie and the HT field added. The units are c = 1 and 16πG̃ = 1.

    S = ∫d⁴x { √−g [ R − (K_B/2)F² + 2(2−K_B)J^μ∇_μφ − (2−K_B)𝒴 − 𝓕(𝒴,𝒬;Λ) − 2Λ − λ(A² + 1) ] + 2Λ ∂_μT^μ } + S_m[g]
    𝓕 = (2−K_B) α(Λ)² j(𝒴/α(Λ)²) + 𝒦(𝒬),     α(Λ) = κ√(Λ/8π)  ⇔  a₀ = κ c √(G ρ_Λ)

- 𝒬 = A·∇φ is the time-derivative part, and 𝒴 = (g + AA)∇φ∇φ is the spatial-gradient part.
- In deep MOND, j(s) → [2λ_s/(3(1+λ_s))] s^{3/2}. This reproduces the transcription's 𝒥 ∝ 𝒴^{3/2}/a₀.
- AeST's constant term in 𝒦 is replaced by the HT field Λ(x) and its multiplier T^μ, so the theory has one cosmological constant.
- **Status of the parts:**
  - **POSTULATED:** the tie α(Λ).
  - **FITTED:** κ = ½. The alt footing needs κ = 0.6043 on ρ_Λ.
  - **AeST's own parameters, declared and not fitted:** K_B, λ_s, 𝒦₂, 𝒬₀, and the dust amount.

## 2. Part A — the construction (load-bearing, sympy)

| check | result |
|---|---|
| L1 tie | α = κ√(Λ/8π), with ∂α/∂Λ ≠ 0. It gives a₀ = 9.360325e-11 from FP0's ρ_Λ (ratio − 1 = 0). |
| L2 global | δT gives −2∂_tΛ = −2∂_xΛ = 0, and no AeST field appears in those equations. δΛ fixes only ∂_μT^μ, the unimodular clock. T appears in no other equation. This agrees with CFG177 E1, where the HT current is pure gauge. |
| L3 same as AeST | With Λ = Λ₀, the φ, A^t, A^x and λ equations equal plain AeST's at a₀ = α(Λ₀). This holds for a generic j and 𝒦; the difference is exactly 0. |
| L4 no local dof | On a periodic lattice (N = 5): the constraints Λ_{n+1} − Λ_n have rank 4, every bracket with H vanishes, and they are first class. The HT sector reduces to 2N − 2(N−1) = 2, one global pair. The local sector is unchanged. |
| L5 flat | a₀(z)/a₀(0) = 1 at z = 0.5, 1, 2.5, 5 and 1100. |
| L6 FRW, linear | 𝒴̄ = 0 on FRW. For a general linear perturbation (metric, aether with its unit constraint, scalar), δ𝒴 = 0. The a₀-sector is therefore O(ε³): absent from the background and from the linear equations. This re-derives bridge1's order counting with the metric and aether included. |
| L7 count | Beyond AeST's own parameters, the tie adds one dimensionless coupling κ and removes a₀ as an independent constant. |
| L8 metric-free | The HT term has zero metric variation, so c_T and the PPN metric are untouched by the tie. |
| R-θ (reported) | On FRW the aether has θ = 3H, but F_{μν} = 0 and J^μ = 0. AeST's vector sector is blind to the flow's expansion at the background level. |

## 3. Controls (all pass in every mode)

- **C1.** a₀ = 9.3603e-11, and Λ/α² = 32π = 100.530965 (XR20 C3).
- **C2.** Without the multiplier, Λ's own equation is local and algebraic. For the deep-MOND j it gives Λ ∝ 𝒴, so a₀ would vary in space, and it pins 𝒴/α² to a constant. The multiplier is what makes the tie global; this is the FP5 D3 / XR20 T1b point.
- **C3.** The record's overshoot for a CDM-clustering dust is 2.06–4.42× (Route A kernel, `mi_aest_jeans_nonlinear_verdict_2026.py` E1). It is reproduced as 2.062–4.419.
- **C4.** For P2, h → ½ − 1/(8y). The RAR kernel's h decays above Y_P. H_P = 0.6476. CFG185's Earth and Mars ratios are reproduced to 2.9e-4.
- **C5.** E(z) reproduces FP0's committed `a0z_rival_E` exactly.
- **C6.** All 41 anchors are present in their cited committed files, and CFG7 H0's 14 gates are parsed on both footings.

## 4. The scorecard (reported; row ids from `closure_map/GATES.md`)

**How to read it.**
- **Horn N** means the dust stays out of galaxies. This is the published AeST phenomenology, and the record says it needs a per-galaxy boundary constant (MMH23).
- **Horn D** means the dust clusters like CDM, which is the record's linear verdict.
- Galaxy rows are scored on horn N, the reading most favourable to AeST's MOND. The two horns are never pooled.
- The physics codes:
  - **SAME:** a committed computation of the same equations. CFG7's "law with the external field" column is AeST's quasi-static MOND limit with its EFE.
  - **CARRIED:** the same class of model with a different base, named in the row.
  - **LIT:** literature as the record quotes it, UNVERIFIED.
  - **HERE:** computed in this lane.
- **σ values** are canonical / alt.

| row | observable | this candidate | B (GATES_STATUS 09-29) | physics; source |
|---|---|---|---|---|
| 1.01 | SPARC RAR | **CONDITIONAL.** Horn N: the same law and numbers, ν_mono 0.1003/0.0991, P2 0.1083/0.1035 dex (no EFE in that rms). Horn D: overshoot P2 1.81–4.89×, ν_mono 2.06–4.49×. N9 says horn N costs the forest. | PASS | SAME / HERE; CFG4_galaxy_law.out; C3 |
| 1.07 | MW classical dSphs | **FAIL** 3.53 / 3.34σ | PASS 1.06/0.74 | SAME; CFG7_hierarchy_fg001.out H0 |
| 1.08 | M31 dSphs | **FAIL**: LVD 5.96 / 5.70σ, Collins 5.80 / 5.58σ | MARGINAL | SAME; CFG7 H0 |
| 1.09 | MW ultra-faints | **FAIL** 13.19 / 12.82σ (harness, statistical only) | FAIL (refereed 3.8/3.5σ) | SAME; CFG7 H0 |
| 1.10 | LV dwarfs, host statistic | **FAIL** 3.92 / 3.96σ | PASS 1.71σ | SAME; CFG7 H0 |
| 1.11 | cluster-infall BTFR | **FAIL** on the slope, 2.35 / 2.38σ; the zero point passes at 0.77 / 0.79σ | PASS | SAME; CFG7 H0 |
| 1.12 | tidal dwarfs | PASS 0.86 / 1.24σ | PASS | SAME; CFG7 H0 |
| 1.13 | outer-halo GCs | PASS: needs M/L_V 1.04 / 0.99 (does not discriminate) | PASS | SAME; CFG7 H2 |
| 1.14 | DF2 / DF4 at 20 Mpc | **FAIL**: DF2 2.95 / 3.12σ; DF4 passes at 1.45 / 1.49σ (distance contested) | PASS | SAME; CFG7 H0 (XR27) |
| 1.15 | Chae EFE signal | **PASS**: D1 0.76σ, D2 0.00σ. CFG8's median e > 0 (1.7–3.0σ) is what an EFE theory expects. The slope 0.55–0.87 ± 0.25 lies 0.5–1.8σ from 1, but there is no rank correlation (p 0.57–0.87). | FAIL | SAME; CFG7 H0; CFG8_README.md |
| 1.16 | Coma UDGs | **FAIL**: +1.159 / +1.112 dex = 4.9 / 4.7σ | PASS 1.33/1.11σ | SAME; CFG31 .out (L23) |
| 1.17 | binary galaxies | UNSCORED | UNDECIDED | — |
| 1.18 | X-ray ellipticals | MARGINAL: 1.70 / 1.58σ (bare law; EFE omitted) | MARGINAL/FAIL | CARRIED; GATES.md |
| 1.19 | SLACS | MARGINAL: 1.5–1.7σ | MARGINAL | CARRIED; GATES.md |
| 1.20 | SLUGGS | **FAIL**: +0.097 (4.0σ, JAM masses); 3.6σ with published slopes | FAIL | CARRIED; GATES_STATUS + addenda |
| 1.21 | passive disks | PASS +0.026 | PASS | CARRIED |
| 1.24 | environmental null | PASS: a₀ is global (L2) | consistent | HERE |
| 1.25 | super spirals | MARGINAL: 1.67σ (the nine fastest at 2.34σ, shared with ΛCDM) | MARGINAL/FAIL | CARRIED |
| 1.26 | massive HI disks | PASS, −0.028 ± 0.066 | PASS | CARRIED |
| 2.01 | X-COP | **FAIL on both horns.** Horn D: the additive reading gives ≥ 1.27–1.37 (8.4–10.6σ), a lower bound because AeST's phantom is also sourced by the dust. Horn N: the law alone falls short, η 1.68–2.03 (13–17σ). The middle ground needs λ_J ≈ 2.7 Mpc, 22 orders from AeST's natural condensate scale. | PASS 0.946 | CARRIED; CFG4_README.md, CFG4_clusters.out, jeans verdict C1 |
| 2.02 | Bullet | CONDITIONAL. Horn D: collisionless dust at the cosmic share, as B has (4.6× / 4.9× needed). Horn N: not scored (literature says MOND alone fails; UNVERIFIED). | PASS | CARRIED; CFG4_clusters.out H5 |
| 2.03, 2.04 | X-ray groups, LG R0 | UNSCORED | R2500 FAIL; FAIL (shared) | — |
| 3.01 | CMB | CONDITIONAL. AeST's fit is LIT (UNVERIFIED). The tie is invisible at linear order (L6). The record reads SZ21 as: only the "Exp" K meets the galactic μ bound. N9: a charge dust cannot be both cold for the CMB and forest and absent from galaxies. | met by construction | LIT + HERE; AEST_BOUNDARY_CONDITION_CLOSURE.md, CONDENSATE_NOGO_THEOREM.md |
| 3.02, 3.03 | CMB lensing; growth, S8 | UNSCORED (AeST's P(k) fit is LIT, UNVERIFIED) | PASS; met by allowance | — |
| 3.04 | BAO, background | PASS: the background is AeST's FRW with constant Λ | unchanged | HERE + LIT |
| 3.05 | KiDS isolated lenses | **FAIL** on the record's AeST closure: a charge-fixed boundary gives Δχ² ≥ +106 for every m², on both footings. It passes (−0.5 to −4.9) only with a free per-galaxy constant (MMH23's regime). A kernel that sees the web's total field gives +404 / +415 (+47 / +52 inside 0.3 Mpc; BS3, base model C-H/K). | PASS at x_e = 0.4 | SAME / CARRIED; aest_boundary_condition_closure_2026.out; BS3 .out |
| KiDS split | CFG61/67/110 | UNSCORED: an EFE theory predicts an environment-correlated difference, not computed | FAIL ~3.7σ | — |
| 3.06–3.09 | budget, edge | N/A (B's constructs) | mixed | — |
| 3.10 | a₀(z) at z ≈ 2.5 | NS: the prediction is flat exactly (L5) | NS (flat, TIED) | HERE |
| 3.11 | a₀ = κc√(Gρ_Λ) | PASS: TIED in the action, κ FITTED, consistent at 0.46 / 0.29σ | consistent, FITTED | HERE; GATES.md 3.11 |
| 3.12 | Lyman-α forest | CONDITIONAL. Horn N fails by N9 F1: a dust that shields galaxies is ≥ 20 km/s at z = 3 (minimum 23 km/s). Horn D is cold, like CDM (not scored). | PASS 0.00 | SAME (N9); condensate_mu_pincer_2026.out |
| 4.01 | Cassini, ephemeris | **FAIL.** The Sun owns its phantom. The EFE quadrupole is 3.99–5.69× the Q₂ ceiling (strict P2 law). The monopole is 3011 / 3620× the Earth bound for ν_mono and 1279 / 1545× for P2. The RAR kernel removes the monopole but not the quadrupole. | PASS via ownership | SAME + HERE; CFG1_evidence_audit.out A01; CFG185; C4 |
| 4.02 | GW170817 | PASS: c_T = c by AeST's construction (LIT, UNVERIFIED); the tie is metric-free (L8) | NS (no action) | LIT + HERE |
| 4.03 | γ = 1 | PASS: Φ = Ψ in the quasi-static limit (the record's completion script C1–C2) | NS | LIT |
| 4.04 | α₁, α₂ | **FAIL.** α₁ = −2(K_B+2) (the v9 kill, which attributes it to AeST's J·∇φ term; this candidate shares that term). Named residual: the Sun's own background, unresolved (CFG172 §3). If J_Y ≤ 1 on every background, then \|α₁\| ≥ 4 everywhere (R-α₁, conditional). α₂ is UNSCORED. | NS | CARRIED; V9_PPN_KILL_VERDICT.md |
| 4.05 | DR3 wide binaries | CONT | CONT | — |
| 4.06 | DR4 (2 Dec 2026) | NS. The prediction is **Arm A**: 1.1614–1.1814 (can) / 1.1917–1.2267 (alt); it dies if the result is Newtonian. | NS; **Arm C 1.000** | SAME; PREREGISTRATION_DR4.md |
| 4.07 | EFE | MIXED: Chae supports it; the satellites, Coma and DF2 go against it | absent by ownership | rows 1.07–1.16 |
| 4.08 | preferred frame (KM1) | UNSCORED. a₀ is frame-independent. The kinematic 𝒴 shift is ≤ 4.0e-6 at 600 km/s. The aether-drag response was not computed. CFG186 is pending. | NS | HERE (kinematic) |
| 5.01 | one action | PASS: AeST + HT, though not an action for B | FAIL/OPEN | HERE |
| 5.02 | stability | UNSCORED | FAIL as varied | — |
| 5.05, 5.10 | dof; FLRW | PASS: 0 local dof from the tie (L4); the background is AeST's (L6) | orphaned; partial | HERE |
| 5.11 | dark mass as a field state | CONDITIONAL: yes structurally (the scalar's 𝒬-sector), but N9 excludes the version absent from galaxies | OPEN | SAME (N9) |
| 5.13 | a₀–Λ | PASS: TIED (postulated), κ FITTED | declared input | HERE |

**Tally** (the rows are not equally weighted): PASS 14, FAIL 12, CONDITIONAL 5, MARGINAL 3, NS 3, UNSCORED 8, MIXED 1, CONT 1, N/A 1.

**Head-to-head with B**, on rows where both have a data status:
- **Better (2):** 1.15 and 5.01.
- **Worse (13):** 1.01, 1.07, 1.08, 1.10, 1.11, 1.14, 1.16, 2.01, 2.02, 3.01, 3.05, 3.12 and 4.01.
- **Same (11):** 1.09, 1.12, 1.13, 1.18–1.21, 1.24–1.26 and 3.11.
- **Not compared, because B has no action:** the candidate passes 4.02 and 4.03 (c_T, γ) where B is NS.

## 5. How it differs from candidate B

| | this candidate (AeST + HT tie) | candidate B |
|---|---|---|
| what it is | one covariant action | an effective law plus bookkeeping rules; no action (5.01) |
| external field | **present everywhere** (AQUAL-type, nonlinear) | **absent by ownership**: a system obeys the isolated law of its own infall baryons, and the Sun owns no phantom |
| dark mass | the scalar's 𝒬-sector (dust), **added to** the MOND phantom | cold mass at the cosmic share, **max(phantom, cosmic share)**; the two never add |
| where the phantom stops | nowhere (up to AeST's μ² term) | a declared edge at 0.4 r_ta, with a bound-only switch |
| a₀–Λ | tied in the action (HT); κ fitted | tied by the same HT construction (XR20 T1); κ fitted |
| wide binaries (DR4) | Arm A 1.16–1.18 | Arm C 1.000 |

- **Where it is better:**
  - Chae's EFE signal is predicted, not a cost.
  - It is an action.
  - Its c_T and γ follow from AeST (LIT).
  - Its dark mass is a state of the same field, not an extra species.
- **Where it is worse:**
  - Every EFE-sensitive population the record scored: the classical and M31 satellites, the LV host statistic, the cluster-infall slope, DF2 and the Coma UDGs.
  - The Solar System: the quadrupole, the monopole with the framework's kernels, and α₁.
  - X-COP.
  - KiDS, on the record's AeST closure.
  - The CMB and forest pincer on the dust (N9).

## 6. What stays unexplained

- **κ = ½:** fitted, as in every lane. The Unruh route was retired (CFG47).
- **The tie's origin:** α(Λ) is a coupling function written in by hand. XR20 T1 shows any α(Λ) can be written this way. The √Λ power is dimensional; the ½ is not derived.
- **Where the dust sits:** the published phenomenology needs a per-galaxy boundary constant (MMH23: "no known mechanism"). The record's charge-conservation closure and the N9 theorem say it cannot be kept out of galaxies. The rests-on list: an accretion estimate, and the fact that no AeST N-body run exists.
- **AeST's own free function and parameters** (K_B, λ_s, 𝒦₂, 𝒬₀): declared, not derived.
- **The Solar System:** the EFE quadrupole fails for every kernel on record, and α₁ is carried from the v9 kill with its named residual.

## 7. MUTATE results

- **MUTATE=1** (untie; a₀ is an independent constant):
  - L1 and L7 fail.
  - L5 still passes: plain AeST's a₀ is also constant, so **flatness is not unique to the tie**.
  - R-DIFF: only rows 3.11 and 5.13 change. **No data row changes.**
- **MUTATE=2** (a₀ ∝ θ, the owner's compaction used as the tie variable):
  - L1, L3, L5 and L7 fail.
  - a₀(z) = E(z), +0.576 dex at z = 2.5: the rival law.
  - Rows 3.10, 3.11 and 5.13 change.
  - CFG172 (11C-b) already found the local pincer this reading meets.

## 8. Disclosures

- **Edits before the first run** (made after the script was written):
  - The P2 tail check uses limits, not a truncated-series equality (the CFG185 pitfall).
  - An overflow guard was added to the RAR tail.
  - A malformed anchor expression was removed.
  - L7 is now computed from the expression, not from the mode.
  - The Λ function was renamed.
  - L3 compares against a constant a₀ when α reads a field (mode 2).
- **Debug run 1 (main):** 18/18, rc 0. After it, cosmetic edits only: the Chae row's wording, a printed symbol list, the C2 root print, and the note "(no EFE in the carried rms)". No number changed.
- **Ordered run 1 (MUTATE=1, MUTATE=2, main):** the verdict line wrongly printed "required failures … MISSING". The cause was a list-membership test on names truncated at ':'. The checks themselves failed as required.
  - Fixed, and ordered run 2 (MUTATE=1, MUTATE=2, main) is kept.
  - A further re-run of main is identical apart from the timing line.
- **The scorecard is not blind** (see the frozen question, §0). Its statuses are assembled from committed numbers. Rows whose content depends on Part A (3.10, 3.11, 4.02, 5.05, 5.10, 5.13) are computed from the checks.
- **Literature items are UNVERIFIED** (no network; as the record quotes them or from memory): AeST's CMB and P(k) fits; c_T = c; its quasi-static MOND limit with an EFE; ghost-freedom; MMH23; "MOND alone fails the Bullet".
- **The EFE rows carry a caveat.** They use the strict law with the host's field (CFG7). AeST's quasi-static limit is a two-field (Newtonian plus scalar) form per the literature, which could move EFE coefficients at O(1). This was not computed.
- **The v9 α₁ number comes from an embedding with a DBI 𝒦 and its own a₀(𝒬) tie.** The verdict attributes α₁ to the base J·∇φ term and says the 𝒦 channel does not move it; the transfer to this candidate is carried, not re-derived. The verdict file's own "Layer A" wording (Z ≈ 21; a₀ ∝ H(z) as the prediction) is superseded in the record and is not used here.
- The existing `campaign_fresh_gravity/__pycache__` (16:18) predates this lane. It is gitignored and was left as found.

## Reproduction

From the repository root:
```
MUTATE=1 python3 campaign_fresh_gravity/CFG187_aest_lambda_tie_candidate/CFG187_aest_tie.py   # rc 1 (L1, L7)
MUTATE=2 python3 campaign_fresh_gravity/CFG187_aest_lambda_tie_candidate/CFG187_aest_tie.py   # rc 1 (L1, L5; also L3, L7)
python3 campaign_fresh_gravity/CFG187_aest_lambda_tie_candidate/CFG187_aest_tie.py            # rc 0, 18/18
```
It reads FP0's committed JSON (through `CFG4_common`), `CFG7_hierarchy_fg001.out`, and the files named in C6. All of these are read-only.
