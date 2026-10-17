# Corrections and status updates to THEORY_CANONICAL_2026-10-14 (dated 2026-10-16) — DRAFT

**Status: draft for the owner's review. Committed; it reached `origin/main` through another session's push, not this note's author's.** The frozen file `THEORY_CANONICAL_2026-10-14.md` is not edited.

**Written against the 10-14 file.** A dated v2 (`THEORY_CANONICAL_2026-10-16.md`) landed on 2026-10-16 while this note was being drafted. The section "Status against v2" below says which items v2 already resolves and which still apply.

## What this note is, and is not

- It records places where the frozen text misdescribes the record, or where the record has moved since the freeze.
- It does **not** change S1–S5, any sealed prediction, any seal hash, or any kill condition in §2 of the frozen file.
- It adds no parameter, no knob and no new prediction. It does not say the theory is closed or failed.
- κ = ½ is FITTED. The two a₀ footings are never pooled.

## Admission rule (what keeps this from being circular)

An item is included only if all five hold:

1. The frozen sentence is quoted and line-cited.
2. The contradicting or limiting statement sits in a **primary source the frozen text does not itself derive from** (a ledger row, a lane README or criteria file, a results JSON), cited by id and path.
3. The correction changes what a reader would conclude. A restatement of something the frozen text already says is not a correction.
4. The orchestrator re-read the primary source. An audit lane's summary was not accepted as evidence.
5. No output of the 10-16 parameter-reduction workflow (CFG830–834) is used as evidence, except item C9, which is labelled as a new result.

Classes: **E** = the frozen text overstated or mis-scoped the record when written. **S** = stale, a result committed after the 10-14 freeze. **U** = update from a new result.

## The corrections

| # | Frozen text (line) | What the primary source says | Source | Class |
|---|---|---|---|---|
| C1 | S4: "The selector is CFG782" (l. 36–37); UFDs "S4 + CFG782/784 address this; the result is pending" (l. 61) | CFG782 is **DEAD**. S1 passes (100% of MW ultra-faints flagged SUDDEN) but S2 fails: about 50% of M31 satellites are flagged too, against a 10% ceiling. CFG784 was **NOT RUN** (frozen conditional on CFG782). Committed 2026-10-15, one day after the freeze. | `CFG782_unbinding_selector/README.md:3`; ledger rows CFG782, CFG784 | S |
| C2 | "early-type cores: +0.28 dex, pending; eRASS1 cluster cores: ×1.8, pending" (l. 62–63) | Not pending: tested, none passing. Early types: CFG721 H-OF FAILS; CFG811 SHORT (predicts +0.013 vs +0.280, Z +3.2); CFG726 merger memory reaches only the 2σ line. Clusters: CFG815 FAIL on both profiles (middle tercile ×1.64, Z +4.6); CFG818 NULL; CFG819 thread PAUSED, "middle-mass shortfall ~1.6 real and unexplained". UFDs: blocked by C1. | ledger rows CFG721, 726, 811, 815, 818, 819 | E/S |
| C3 | "κ = ½ (measured, not derived)" (l. 10) | The measurement is CFG493's combined interval: κ = 0.417 ± 0.095 (canonical footing), 0.345 ± 0.078 (alt). ½ is an adopted round value inside it: 0.80σ away (canonical), 1.63σ (alt). The frozen file's own footer says "κ fitted". Wording only. | `CFG493_kappa_combined/cfg493_kappa_combined_results.json`, key `combined` (not the `_MUTATE` twin). No CFG493 ledger row exists. | E |
| C4 | "environment slope is −0.010 ± 0.015 (record)" (l. 13–14) | The −0.010 ± 0.015 is a **SPARC-internal kNN slope**. CFG252's criteria say it "is not mapped, because a kNN density among SPARC galaxies is not 1 + δ of the matter and the record has no calibration". The mapped limit (2M++ real-space, N = 52) is **−0.083 ± 0.135**, "CONSISTENT, UNDERPOWERED" (z = −0.46), about 9× weaker. The separate +0.5 local-density exclusion (13σ SBeff, ~34σ kNN) is the same kind of proxy test and is not re-evaluated here. | `CFG252_FROZEN_CRITERIA.md:117–118`; `CFG252_timescape_between_the_bands/README.md:107` | E |
| C5 | "The law is a two-sided attractor: deficits fill in (CFG747/748) and surpluses are expelled (CFG776)" (l. 29) | Shown only for spherical **radial** collisionless shells, with angular momentum listed as "next" and not done. CFG747: inner halo (2, 5 r_M) lands on the law within 0.2–1.7%, outer (10, 20 r_M) short at 0.62–0.96; R1 and K1 FAIL as frozen. CFG748: C1 FAIL, C2 STALLED, K2 FAIL on the uniform run, MUTATE did not bite; the outer halo fills only with the law's full mass and time (0.945 at 50 r_M; mass-starved 0.813). CFG776: the surplus is expelled within ~50–100 t₀ but **overshoots into a deficit** (m/r 0.30–0.50 at 5–11 r_M, still 0.44–0.77 at 3000 t₀); the row itself concludes surplus tethered cold energy is "dynamically unstable". "Attractor" is not demonstrated for surpluses within the simulated time. | ledger rows CFG747, 748, 776 | E |
| C6 | "condensed baryons source the settled profile (T12; raw KiDS Δχ² = +2.03)" (l. 30) | The number checks, but the context is missing. T12 is a **POST-PREVIEW selection** (addendum A1); T1x is the primary pre-declared run. It is scored on the canonical footing only (alt: PENDING). It inherits ΛCDM initial conditions (native rerun pending). Δχ² = +2.03 is **worse** than the same-pipeline control (χ² 146.29 vs 144.26; both marginal in absolute terms, p 0.011 vs 0.014); the class is CONSISTENT, not an improvement. With the PAPER50 cold-to-dark-energy conversion applied, T12 becomes **TENSION (+8.30)** (CFG780). | `CFG650_theory_v2_combined_pm/README.md:91–101`; `FROZEN_CRITERIA_ADDENDUM_T12.md:5`; ledger row CFG780 | E |
| C7 | "FRBs exclude baryon consumption at 7.8σ (CFG779)" (l. 41–42) | 7.8σ is one case: the Croker-like 30%-eaten model (P2), 5.6σ with a 5% systematic. The 57%-eaten model (P1) is excluded at 16.6σ. These are tested fractions, not a general bound. The "cold-energy-only conversion consistent at 0.9σ" is labelled post-hoc, mechanism not derived; CFG780 shows that conversion worsens KiDS (T1x +4.66). | ledger rows CFG779, CFG780 | E |
| C8 | Gaia DR4 row, kills it = "an MOND-size wide-binary boost" (l. 51) | The frozen quantitative rule is much stricter than the prose: **R − 1 ≥ 0.01 at 3σ kills; \|R − 1\| < 0.01 at 2σ is CONSISTENT**. CFG740's own falsifiers: γ_v ≥ 1.01 at s ≤ 50 kAU, or an excess with slope ≠ 2. The quantitative rule governs. CFG800 also records a 2026 analysis reporting a boost of 1.15–1.20 (unreplicated), which would kill CFG740 if confirmed. | ledger rows CFG740, CFG800 | E/S |
| C9 | "L* ∈ [5.75 pc, ≳ 1 kpc] (bounded, not derived)" (l. 19) | CFG691 shows "raw SPARC unaffected to ≥ 1000 pc (grid edge)": 1 kpc is the end of the scan, so the upper end was never a bound. **New result, provisional (CFG832):** lower edge 5.650 pc (the Saturn gate; 5.754 was the next grid point), upper edge ≈ 2.04 kpc canonical / 2.14 kpc alt at the CFG4 rms 0.110 line, soft (1.4–2.6 kpc across the 0.105/0.115 lines and two mass rules). It depends on point-mass screening of extended systems, a single lane and a campaign-defined threshold. L* is still not derived. The lower edge was raised later the same day by CFG820 (see "Status against v2"). | ledger rows CFG691, CFG832, CFG820 | E (bound) + U (edge) |
| C10 | §4: CONFIRMED needs "the pending lanes on S4 pass their frozen gates" (l. 68–69) | Consequence of C1, not a rule change. The only quantified S4 gate (CFG782) has failed and its dependent (CFG784) was never run, so **no S4 gate is currently available to pass**. This note does not rewrite §4. Whether S4 gets a new gate frozen before the data, or §4 is read as unreachable as written, is the owner's decision in a new dated version. The §2 kill conditions are unaffected. | C1 | S |

## Status against v2 (`THEORY_CANONICAL_2026-10-16.md`, commit b7b3ba9a7)

v2 supersedes the 10-14 text "only where stated" and leaves S1, S2, S5, §2 and §4 unchanged. I read v2 in full. I re-read only the primary sources named in the table above, not the lanes v2 itself cites (CFG801–806, 809, 814), so I take v2's statements about those as v2's.

| # | Against v2 |
|---|---|
| C1 | **RESOLVED.** v2 removes the CFG782 selector and says the UFDs are "now without a selector". |
| C2 | **LARGELY RESOLVED.** v2's "does NOT do" list names the failures (early-type +0.013 vs +0.280; middle-mass eRASS1 short ×~1.6, Z ≈ +4; UFDs without a selector) instead of "pending". |
| C3 | **STILL APPLIES.** S1 is unchanged, so "κ = ½ (measured, not derived)" stands. |
| C4 | **STILL APPLIES.** S1 is unchanged. |
| C5 | **STILL APPLIES** to the attractor sentence (v2 revises only the supply rule). v2 adds "collisionless infall fills onto the law out to 20–50 r_M (CFG748, CFG803)". I re-read CFG748 only: it reaches 0.945 at 50 r_M when given the law's full mass, with C1 FAIL / C2 STALLED as frozen. I did not re-read CFG803. |
| C6 | **STILL APPLIES, plus a tension to check (not asserted).** v2 removes "each halo settles only its own supply" (citing CFG801), while T12 was run with per-host supply (M1; `CFG650_theory_v2_combined_pm/README.md:91`). How T12 and T1x score under v2's catchment rule is not on the record. |
| C7 | **STILL APPLIES.** S5 is unchanged. |
| C8 | **PARTLY ADDRESSED.** v2 names "CFG800's decision rule and Amendment 22" for DR4, but the "MOND-size" wording in the 10-14 table is not itself edited. Read the DR4 row through CFG800. |
| C9 | **UPDATED.** CFG820 (landed 2026-10-16 17:33, after v2) reports **L\* ≥ 24.0 pc (95%, canonical; 24.7 alt; ≥ 13.8 pc if all four globulars including Pal 3 are used)** from outer-halo globulars (CFG332 data × CFG691 screening). That is consistent with a DR4 envelope smaller by (24/5.754)² ≈ 17, as it states. Its upper end still reads ">~1 kpc" (the grid-edge wording); CFG832's soft ≈ 2 kpc edge is a separate lane. If both hold the window is [24 pc, ≈ 2 kpc soft]. Both are single-lane results, and for CFG820 I read the ledger row only (the id CFG820 is also used on a DR4-scoring row; the one meant here is titled "Stiffness length lower bound from outer-halo globulars"). **CFG821 (landed 2026-10-17, after this note was first drafted) conflicts with it:** 11 MW classical dSphs want L\* ≤ 22 pc (95%, floor-preferring) against the globulars' ≥ 24 pc, and the row marks this INCONSISTENT (CONDITIONAL). Its own reading is that the unscreened isolated law already fits the dSphs badly (χ² 58 for 10), so a gravity-only stiffness cannot serve both and the dwarfs need real bound cold mass; on that reading L\* ≥ 24 pc stands. Taken at face value as a bound, ≤ 22 pc would leave no L\* satisfying both, and it is a stricter upper bound than CFG832's ≈ 2 kpc, from different data. The [24 pc, ≈ 2 kpc soft] window above therefore holds only on CFG821's own reading (the dSph preference is a missing-mass signal, not an L\* bound). I read the CFG821 ledger row only. |
| C10 | **NARROWED to the 10-14 file.** v2 replaces the dead selector by H-EX and leaves §4 "unchanged". Under v2, S4 has a recorded failure on the full 318 clusters (CFG815) and the early-type miss (CFG811). Whether "the pending lanes on S4 pass their frozen gates" can still be met is the owner's reading; this note does not decide it. **CFG821 adds a second pointer on the dwarf side of S4:** its row concludes the classical dSphs need real bound cold mass (its words: a two-population S4), so the dwarf arm has no quantified rule under v2 either (v2 already lists the UFDs as still open). That is a status fact from one ledger row, not a decision on §4. |

## Considered and NOT included (so they are not re-flagged)

- **C = 16π, "equivalently" ρ_DE c² = 4a₀²/G (l. 11).** This is a restatement of κ = ½, but the frozen text already says "equivalently". Nothing is misdescribed.
- **"The frozen file quotes κ = 0.42 ± 0.10."** It does not. That is in `STANDING_2026-10-09_law.md`. C3 is the real κ wording issue.
- **"The frozen file cites CFG720 for supply overflow."** It does not. CFG720 appears only in `THEORY_v3_DRAFT_2026-10-13.md` (lines 5, 14, 56, 106, 121), where the overflow lane is actually dir `CFG721_supply_overflow` and it fails. Fix the draft directly. The ledger also carries each of the ids 721, 722 and 723 twice.
- **Not verified, so not asserted:** the sealed ALMA gas ranges, the seal hashes, the "a₀(z≈2)/a₀(0) ≈ 0.85" figure's coupling case, the claim that the c_P floor conflicts with the medium identification, and the R_ind / EFE-basin-rule leads (inferences, not scored results).

## Errata to this workflow's own ledger rows (CFG830–834)

- **CFG830** says "canonical and v3 cite CFG720". Only v3 does (see above).
- **CFG833** presents a₀_alt / a₀_canonical = 1/√Ω_Λ (to 2.2 × 10⁻⁴) as a structural finding. It holds **by construction**: the footings are κ = ½ applied to ρ_crit and to ρ_Λ. Check: (canonical/alt)² = 0.68470, the Planck Ω_Λ the canonical value was built from, and the 2.2 × 10⁻⁴ is only 0.685 versus 0.6847 rounding. The same row's "footing = nuisance rejected" refuted a position no one held. What stands from CFG833 is non-circular: the CFG493 interval and pulls, the footing likelihood ratio (2.76, weak), and the pin-threshold analysis (no sealed test pins κ).
- Applied: ledger row **CFG835** records both errata. It also notes that CFG832's lower edge (5.650 pc) is superseded by CFG820.

## Reproduce

```bash
cd campaign_fresh_gravity
grep -n -E "^\| CFG(782|784|747|748|776|779|780|740|800|691|820|821|832) " LEDGER.md | cut -c1-400
sed -n 3p CFG782_unbinding_selector/README.md
sed -n 117,118p CFG252_FROZEN_CRITERIA.md; sed -n 107p CFG252_timescape_between_the_bands/README.md
sed -n 91,101p CFG650_theory_v2_combined_pm/README.md
python3 -I -c "import json;d=json.load(open('CFG493_kappa_combined/cfg493_kappa_combined_results.json'))['combined'];print(d['canonical']['kappa'],d['canonical']['sigma'],d['alt']['kappa'],d['alt']['sigma'])"
```
