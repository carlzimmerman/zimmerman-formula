# CFG265 -- hostile, fair referee of the PAPER39 draft (closure map; NOT deposited): phase 2 report

**kappa = 1/2 is FITTED, NOT DERIVED.** Nothing here says the data favour any law; a lean is not a detection; nothing is called closed. Frozen criteria: `CFG265_FROZEN_CRITERIA.md` in this directory, written before any source was opened (sha256 ba8369fa..., recorded with a UTC time in `CFG265_frozen_hash.out`; the file is unchanged since). Subject: `qwen_claude_field_theory/papers_2026/PAPER39_closure_map_2026.tex` as committed in 53f374ae2 (sha256 cfafe712...; unchanged at the current HEAD; the later commit d47f2d292 adds only a deposit script, gated on this referee). Every source is read at 53f374ae2 with `git show`. One reader classified every claim by hand; the flagger is a hint generator, not the verdict. Failed controls, harness bugs and wrong estimates are kept below. No repository file outside this directory was edited; nothing was committed or pushed.

## 1. Bottom line

- **1 CRITICAL, 3 MAJOR, 19 MINOR, 7 NIT** (30 findings; `CFG265_findings.json`).
- **Revision before deposit: WARRANTED** by the frozen v1.1 rule (any CRITICAL, or two or more MAJOR). Every finding is a wording fix; no physics result in the draft changes. The owner decides.
- **What holds:** every audited number traced reproduces from its lane (the audit re-runs 141/141 and both mutation modes exit 1, `CFG265_paper39_audit_rerun.out`); the Lean counts (331; 47 -> 219, 62 -> 281, 50 -> 331), the theorem statements and their premises match the committed `.lean` files; the dimension theorem, the AQUAL-to-P2 step, the 32pi algebra, the DR4 constants, the satellite significance and 22 internal arithmetic relations all re-derive (`CFG265_physics.out`); the gemini-note wording matches the status page; no withdrawn number crept back; the two frozen reference spot-checks (HFB17, MC10) agree with their arXiv pages.
- **What fails:** the draft's statement of its own preregistration discipline (F-01), the DR4 paragraph's "bare law" (F-02), the promotion of a labelled reading to "what a mechanism must do" (F-03), and a P38 gloss that P38 v1.2 itself withdrew (F-04).

## 2. Route-count verdict (task item 1)

- **The recount reproduces.** The table has 25 rows; class labels give 22 no-go / 2 no mechanism (hand-check) / 1 realisable only, equal to the prose (`CFG265_route_recount.out`; checker relations R01, R02). Each of the 22 "no-go" rows carries a binding FAIL in its own lane or in TEN_DOORS_RESULT / DOOR11_RESULT, and DOOR11_RESULT Addendum 1 itself calls every door-11 variant "a scoped no-go on its frozen class", so "no-go (restatement)" for 11A and 11C-a is the lanes' own reading. **No row's label is stronger than its lane's verdict.** Every commit hash exists and touches its lane.
- **Judgment call (F-16):** CFG253 asks where the cosmic cold amount comes from, not how C(r) arises (the "missing object" of TEN_DOORS_GATES), which is also the reason the draft gives for excluding CFG252/CFG254. Without it the count is 24 (22 / 1 / 1). The "phase-1 hand-check" label for CFG253 is the draft's (the lane ran a 26-check background script).
- **What does not hold:** "Each route below was given frozen criteria committed before its scripts" (F-01, CRITICAL): 5 of 25 rows (doors 5, 8, 11A, 11D, CFG253) committed the frozen file in the same commit as the first script, and TEN_DOORS_RESULT:29 says so for doors 5 and 8. "Scored against the shared gates of TEN_DOORS_GATES" holds for 12 of 25 rows (F-17).

## 3. Commands, files, coverage

Re-run (about 2.5 minutes, no network): `ZF_REPO=<repo root> bash CFG265_run_all.sh`. Expected and observed exit codes (`CFG265_run_all.out`): extract 0; route_recount 0; lean_read 0; physics 0; physics --mutate 1; audit_anchor 0; refs 0; check 0; plant (frozen set) 0; plant --fresh 1 (two misses, kept); self-disable 1.

Scripts: `CFG265_common.py`, `CFG265_extract.py`, `CFG265_route_recount.py`, `CFG265_lean_read.py`, `CFG265_physics.py`, `CFG265_audit_anchor.py`, `CFG265_refs.py`, `CFG265_check.py`, `CFG265_run_all.sh`. Hand inputs: `CFG265_classification.csv`, `CFG265_findings.json`, `CFG265_refs_webfetch.json` (transcription of five arXiv pages fetched by the referee), `CFG265_withdrawn_lexicon.json`. Outputs: `CFG265_*.out`, `CFG265_claims.csv`, `CFG265_worksheet.csv/.json`, `CFG265_route_recount.json`, `CFG265_physics_results.json`, `CFG265_physics_MUTATE_results.json`. Kept first runs: `CFG265_flags_firstrun.out`, `CFG265_route_recount_v1_buggy.out`, `CFG265_plant_v1.out`.

- **Extraction:** the committed extractor reproduces the frozen throwaway count exactly: 115 prose sentences, all 115 claim sentences, 25 table rows, **140 claim units, all classified (100%)**.
- **Classes:** FAITHFUL 111 (79%), MISSING-CAVEAT 20, CONTRADICTED 5, OVERSTATED 3, WITHDRAWN-CLAIM-CREPT-BACK 1, UNVERIFIABLE-OFFLINE 0 (target <= 10%). Five FAITHFUL or flagged rows carry an offline note (Lean build not re-run; HFB17 checked against arXiv only; the BBN-only 0.98 +- 0.06 of [A20] is not on disk; G26/AP26/M13/D08 content not checked against the journals).
- **Number tokens:** every number of the abstract, the 25 table rows, S1-S6 and Section 7 was matched to a lane file or a recomputation (NUM family plus reading).
- **Lane level:** all 25 rows were opened at their lane README and a committed `.out` or results JSON / result-table row.

## 4. CRITICAL and MAJOR findings (full text)

### F-01 CRITICAL (CONTRADICTED), tex line 70, claim C041
- **Sources:** `campaign_fresh_gravity/closure_map/TEN_DOORS_RESULT_2026-09-29.md:29`; `campaign_fresh_gravity/CFG131_door8_interacting_vacuum/README.md:3`; `CFG265_route_recount.out`.
- **Evidence:** The draft says "Each route below was given frozen criteria committed before its scripts". TEN_DOORS_RESULT:29 says "Doors 5 and 8: the frozen question preceded the scripts by file times but was not committed first." The CFG131 README says its frozen question was "NOT committed, per the run's instruction". At 53f374ae2, 5 of the 25 rows added the frozen file in the same commit as the first script: door 5 (CFG130, c1d719fbf), door 8 (CFG131, aa0d95aef), 11A (CFG171, 1c91164e9), 11D (CFG251, eff33f041) and CFG253 (c89139c1b). The other 20 rows have the frozen file in an earlier commit. For all five, the lanes record that the criteria were written before any script (by file time, or with a sha256 recorded before the script existed for CFG251 and CFG253), so no verdict depends on this. But the sentence is false, and it is the draft's statement of its own preregistration discipline.
- **Two supports:** an explicit source statement plus an independent git-history recomputation.
- **Fix:** "Each route below has frozen criteria written before its scripts. For 20 of the 25 they were committed in an earlier commit; for doors 5, 8, 11A, 11D and CFG253 they were written first (by file time, or with a recorded hash) and committed together with the scripts, as TEN_DOORS_RESULT and those lanes disclose."

### F-02 MAJOR (OVERSTATED), tex lines 180 and 33, claims C092, C093, C094 (and C012)
- **Sources:** `closure_map/DOOR11_RESULT_2026-09-29.md:36-39,41-44,50`; `CFG200_dr4_merge_band_forecast/README.md:12-20,27`; `prep_2026/gaia_dr4_prep/dr4_ready_1/edge_table_dr4.json` (hard edges: Arm A falsified below 1.056; B killed at >= 1.084); `PREREGISTRATION_DR4.md` (Amdt 11 table row 1.056-1.084; Amdt 13(d) table); `CFG63_discrimination_forecast/README.md:46-47`; `CFG265_physics.out` P7.
- **Evidence:**
  - **Kernel label.** "The bare law's floor is 1.161 (alt 1.192)" is Arm A, the merged law with the nu_RAR kernel (DOOR11_RESULT:36 says Arm A's band "uses the nu_RAR kernel ... not P2"). The same paragraph then gives the P2 merge, 1.063-1.127, without saying that the two numbers are two kernels of the same bare law.
  - **"γ ≤ 1.077 kills the bare law".** This is Arm A's floor minus 3 x 0.028 (CFG63's "frozen-rounded" value). The preregistration falsifies Arm A only below 1.056 and reads 1.056-1.084 as "disfavored (2.8-3.8 sigma_tot)". And 1.077 is the top of the P2 merge at the variant field, so for the P2 law it cannot be a kill line.
  - **Cap and pairs.** "Cap 8.1 sigma" and "3 sigma needs about 4,300 pairs" are Arm A numbers. For the P2 merge, CFG200 gives 2.3-3.7 sigma at N = 30,000 and 14,000-264,000 pairs for 3 sigma, and no separation from the derivation chain's ceiling (0.2-1.1 sigma, never 3).
  - **B's kill line.** "γ ≥ 1.084 kills B" holds only if the frozen stability checks pass.
  - **What a reader concludes.** DR4 separates B from "the bare law" at 5.8 sigma with about 4,300 pairs. With the programme's primary P2 kernel the separation is 2.3-3.7 sigma, and there is none against the chain's law.
- **Fix:** "Gaia DR4 wide binaries, 2 December 2026. B predicts γ = 1.000. Arm A, the merged law with the nu_RAR kernel, has its floor at 1.161 (alt 1.192): with the frozen sigma_sys = 0.02 its cap is 8.1 sigma, and 3 sigma needs about 4,300 pairs of the ~30,000 expected; the preregistration falsifies Arm A below 1.056 and reads 1.056-1.084 as disfavored. With the P2 kernel the merged law gives 1.063-1.102 (canonical; 1.079-1.127 alt). That is 2.3-3.7 sigma from ownership at N = 30,000 (canonical), and it cannot be separated from the derivation chain's ceiling (0.2-1.1 sigma). γ ≥ 1.084 kills B if the frozen stability checks pass. B, LCDM and Newton all predict 1.000, so for B this is a survival test, never a confirmation." Abstract (vii): "... a survival test of B against the merged (no-ownership) law: decisive against Arm A's nu_RAR kernel, 2.3-3.7 sigma against the P2 kernel."

### F-03 MAJOR (OVERSTATED), tex lines 23 (title), 33 (abstract iv), 140-155, claims C009, C070
- **Sources:** `closure_map/TEN_DOORS_RESULT_2026-09-29.md:23-24`; `STANDING_2026-09-29.md:284,294`; `CFG242_closure_swing/README.md:3`; `CFG230_requirements_synthesis/CFG230_README.md:3` and its section 3 header.
- **Evidence:** The title says "What a Complete Mechanism ... Must Do", abstract (iv) says "The failures sharpen the target into a specification", and line 155 says "the target is ...". The sources label the core of S1-S3 a reading:
  - TEN_DOORS_RESULT:23: "Cross-door pattern (a READING, not a theorem) ... One reading: the missing object must itself carry an acceleration scale".
  - STANDING:284: "The common thread across the doors (a reading, not a theorem): ownership must remember boundness".
  - STANDING:294 (CFG243): "Reading: the mechanism needs (1) an early cold fluid ... (2) a separate, perfectly remembering ownership assignment".
  - The CFG242 README: "nothing is a theorem".
  - CFG230 states its requirements "inside the stated hypotheses" of the scored classes.

  The draft itself labels the same content "a reading and not a theorem" at line 136, then promotes it to what a mechanism "must do" in the title, the abstract and the one-sentence summary. Only two items rest on more than the failure of one to three scored classes each: S3's "an acceleration scale must enter" (the dimension theorem, for monomials) and S1's "cosmic amount at recombination" (the inherited CMB gate).
- **Two supports:** two source lines, plus the draft's own line 136.
- **Fix:**
  - Abstract (iv): "The failures suggest a specification (a reading of the scored classes, not a theorem; only the acceleration-scale item rests on a theorem, for monomials): ...".
  - Section 4 opener: "Each item is a reading of the failures of scored classes: a necessary condition only inside those classes' hypotheses (CFG230)."
  - Line 155: "In one sentence, the reading is: ...".
  - Title: either "What the Scored Routes Suggest a Complete Mechanism Must Do", or keep it and say "suggest" at the abstract's first use.

### F-04 MAJOR (WITHDRAWN-CLAIM-CREPT-BACK), tex line 183, claim C097
- **Sources:** `campaign_fresh_gravity/CFG241_paper38_referee/README.md:32-36` (F-01); `qwen_claude_field_theory/papers_2026/PAPER38_a0z_calibration_wall_2026.tex:33,204` (v1.2).
- **Evidence:** The draft says "The flat law against a0 prop H(z) is limited by the baryon calibration, not by sample size [P38]." CFG241 F-01 (MAJOR) found PAPER38 v1.1's version of this claim true only as N -> infinity, with three lanes currently limited by statistics or the Newtonian regime. PAPER38 v1.2, the version [P38] cites, replaced it with "the limit that survives an unlimited sample is the absolute calibration ...; at present sizes ... also limited by statistical power or by the Newtonian regime". The draft restates the corrected gloss and attributes it to the version that withdrew it. It is graded MAJOR, not CRITICAL, by the tie rule: the correction rescoped a sentence and did not retract a number.
- **Fix:** "The flat law against a0 prop H(z): the limit that survives an unlimited sample is the absolute baryon calibration; at present sizes several lanes are also limited by statistical power or by the Newtonian regime [P38]."

## 5. MINOR findings (wording in `CFG265_findings.json`)

| id | tex line(s) | class | one-line evidence |
|---|---|---|---|
| F-05 | 180 | CONTRADICTED | "1.063-1.127 ... 2.3-3.7 sigma": 2.3-3.7 is the canonical footing (1.063-1.102); the alt top 1.127 is 4.6 sigma (CFG200, P7). Literally a CRITICAL-class numeric mismatch, graded MINOR by the tie rule (CFG241 F-14 precedent). The P2-merge vs chain-ceiling non-separation is dropped. |
| F-06 | 175 | MISSING-CAVEAT | The BBN 0.98 +- 0.06 is a 95.4% BBN-only interval (status page). As 1 sigma it gives only 2.6 sigma, and "excluded" would not follow. The transfer assumptions (constant couplings, etc.) are unnamed, and the untested evolving couplings are dropped. |
| F-07 | 33, 172 | MISSING-CAVEAT (fairness to MOND) | Delta chi2 vs the free best fit: Milgrom 5.34 < framework alt 7.04 < framework canonical 63.90. "As well as" compares only with alt. |
| F-08 | 172 | MISSING-CAVEAT | Footing.lean uses rho = 3H^2/(8 pi G) (critical); in the draft's rho_Lambda convention Milgrom's kappa is 0.557, not 0.461. |
| F-09 | 33, 144, 148 | MISSING-CAVEAT | Lean's "field data" are two scalars (g_N, g_ext) at a point, and the result follows from the postulated rule. The abstract drops this, and S2 uses it as support; the abstract also drops "monomials". |
| F-10 | 33, 165, 186 | MISSING-CAVEAT | "Is preferred" (abstract, Section 5) contradicts Section 7's "before it could be called a preference". The abstract omits power 0.28 and that the ultra-faints carry it all. |
| F-11 | 186 | MISSING-CAVEAT | The 2.5 sigma cap is on the bare-law vs derived-rule test, not on B's 3.5-3.9 sigma failure. "Data can shrink" inverts the source's "cannot" (ambiguous source). |
| F-12 | 131, 193 | MISSING-CAVEAT | "Ten doors' headlines re-derived" by nine lanes. Six of them are "reported by the calc chat ... not re-verified". Doors 11A, 11B', 11D, 12, 13 and CFG253 have no independent re-derivation. |
| F-13 | 194 | CONTRADICTED | "Hossenfelder's covariant Lagrangian" is listed as untested, but door 12 (CFG231, the draft's own row 12) scored a class-V reconstruction of it. No reference is given. |
| F-14 | 42 | CONTRADICTED | "Not a particle species in any lane": doors 4 and 7 model particle species (CFG122, CFG119). |
| F-15 | 202 | CONTRADICTED | The audit reads no CFG29/CFG118/CFG131/CFG253 README and no kappa note file. It reads CFG0_README (not listed). 67 of 141 rows check the status page. |
| F-16 | 125, 70, 33 | MISSING-CAVEAT | CFG253's "at most about 3%" is its declared tolerance (CFG131's line allows 0.5-1.6%). Its route status and "phase-1 hand-check" label are the drafter's (count 24 without it). |
| F-17 | 70 | OVERSTATED | Only 12 of 25 rows use the TEN_DOORS gates. Door 11 uses DOOR11's G1-G8; CFG242-245, 251 and 253 use their own gates. |
| F-18 | 150 | MISSING-CAVEAT | S5's f(30) = 24.8 is CFG48's r_ta. In B's r_ta it is 0.30-1.65 (3 of 4 masses <= 1). The FAIL stands via the a0-shift line. The ledger is post hoc. |
| F-19 | 51 | MISSING-CAVEAT | The cap window is given without "against the 1e4 the BTFR needs" and without the new constant nu* that the saturating cap needs. |
| F-20 | 152, 61 | MISSING-CAVEAT | "Ownership, or an EFE" repeats the dichotomy that DOOR11_RESULT Addendum 2 corrected ("Only B escapes fails as worded"). |
| F-21 | 168 | MISSING-CAVEAT (fairness to LCDM) | It drops CFG244's "a bound-core reading that matches LCDM at satellites is LCDM there" and Gate D. |
| F-22 | 80-96, 194 | MISSING-CAVEAT (fairness to named authors) | Mashhoon, Deser-Woodard / RR, mimetic, superfluid, dipolar, fuzzy-DM and Hossenfelder are uncited. Nothing says the note is not a literature review or that each lane scores its own frozen version. |
| F-23 | 206-214 | MISSING-CAVEAT | [M13] lacks the volume that REFERENCES.bib has (MNRAS 428, 3121). [AP26] "accepted" vs the status page's A&A 708, A287. [A20] has no volume. Nothing is contradicted. |

**NITs:**
- **N-01:** "hence": law_not_efeFreeRay is proved without continuity.
- **N-02:** T4's Fisher / independent-error premise is missing.
- **N-03:** "nearly meet": the window overlaps in the generous bracket only (post hoc).
- **N-04:** "About -1.3" vs -1.3 to -1.8.
- **N-05:** The cross-door reading drops "doors 1, 3, 4 and 9 are not covered".
- **N-06:** CFG259's "reported row, not a verdict" is dropped.
- **N-07:** The R09 tail premise is dropped.

## 6. Specification S1-S6 (task item 2)

| item | what the cited lanes establish | grade |
|---|---|---|
| S1 early cold fluid | cosmic amount at recombination: the inherited CMB gate (G2); the turnaround dust class fails COSMIC by 10^-1376.8 (CFG243); continuous transfer makes a few per cent (CFG253) | the CMB part is established; "a turnaround source can at most add to or relabel" is the status page's **reading** |
| S2 memory-carrying ownership | one latch class forgets (CFG242, 0.791 vs 0.99); first-crossing rule post hoc (CFG243); "not field-local" is the near-definitional Lean result | **reading** (STANDING:284 "a reading, not a theorem") |
| S3 distribution carries the M^1/2 scale | the dimension theorem (monomials) forces an acceleration scale; passive infall M^0.33 (CFG118, CFG244 not independent), vacuum-rate relaxation too slow (CFG245) | the acceleration scale is a **theorem**; "carried by the distribution itself" is the ten-door **reading** |
| S4 field-local but bound-labelled | CFG245 G0.2 (R_loc up to 2.33, reproduced in order by P13: 1.0-2.45 on generic spheres) and G0.5 (3.16 = sqrt 10, re-derived) | scoped numerical, one class |
| S5 no created rest mass | post hoc ledgers in CFG243 / CFG131 / CFG242; convention-dependent (F-18) | post hoc, scoped |
| S6 inherited gates | CFG230 R05 (scoped), R09 (theorem inside the aether class), G3/G4 | as labelled in CFG230 |

The section's opening sentence ("a necessary condition read off the failures of scored classes; none is shown sufficient, ...") is CFG230's own wording and FAITHFUL. The overreach is in the title, the abstract and line 155 (F-03).

## 7. Lean (task item 3)

All four certified statements in the abstract, and the CalibrationWall and Footing items, were printed from the `.lean` files at 53f374ae2 (`CFG265_lean_read.out`). The theorem counts reproduce: 331 in total, 0 non-standard axioms and 0 `sorry` per `verify_chain.out` and `Axioms.out` (331 axiom lines, all standard); the module sums are 47 / 62 / 50; `verify_chain_MUTATE.out` FAILS as required. No Lean build was run (it would write into the repo).

| statement | verdict |
|---|---|
| (a) ownership non-local (`ownership_distinguishes`, `ownership_not_field_local`, `CandidateB.ownership_nonlocal`) | Faithful, given its premises: a hierarchy with one top-level and one owned system, g_N != 0, nu != 1. "Field data" means F(g_N, g_ext) at a point, and the result is close to definitional given the postulated rule (F-09). |
| (b) no EFE forces linearity (`noEFE_continuousLinear`, `law_not_efeFreeRay`, `vecLaw_not_efeFree`) | Faithful. The draft's "pointwise laws only" caveat matches. The deep-limit results need no continuity (N-01). |
| (c) dimension theorem (`no_sqrtM_length_GMc`, `sqrtM_length_iff`, `acc_from_GcX_iff`, `hbar_admissible`) | Faithful in Section 2. The iff is re-derived for 10 choices of X (P2). |
| (d) AQUAL to kernel (`gauss_form`, `gauss_iff_kernel`, `spherical_kernel`, `nuP2_of_action`) | Faithful. The premises (the reduced Euler-Lagrange equation, regularity, spherical symmetry) are stated. P2 is re-derived (P3). |
| CalibrationWall T1 / T2a / T4 | Faithful. T4's slope premise is stated; the Fisher / det F premise is not (N-02). |
| Footing `footing_kappaM_iff` | Faithful for rho = rho_crit, which the draft does not say (F-08). |

Observation outside the draft (not a finding): ChainCert's `nuMono` is defined as 1/(1 - exp(-sqrt y)), the nu_RAR kernel, while `CFG4_common.py` describes nu_mono as "the chain's monotone repair of nu_RAR". The two names differ across the record.

## 8. Satellites, kappa, 32pi, DR4, withdrawn claims (task items 4-7)

- **Satellites.**
  - Faithful: 3.77 sigma re-derives as 0.3245/sqrt(0.038^2 + 0.077^2); "<= 0.005 dex", "3.5-3.9 sigma", "8 of 40", "a fifth to a third", "+13.58/+11.32", "+8.60", "0.24 above 9", power 0.28, "33 of 40", H4 -> H2 under every variant with both kernels, and the Boo I conflict.
  - Caveats, task item 4: in Section 5 the lean is worded with power 0.28, the H4 -> H2 movement, the ultra-faints carrying it, and small margins. The abstract lacks the power and the UFD-only point, and the "preferred" / "preference" wording clashes (F-10). "Fractions of a chi2" (CFG259) is not quoted, but "the margins are small" with "0.24 above 9" carries it.
  - The weak-binary label is CFG259's own (my memory note "pred >= 1.5 row" is the same row; not a finding).
- **kappa.**
  - Faithful: 0.465 +- 0.076, 0.547 +- 0.175, and 12.9 sigma for n = 2.
  - The Milgrom footing is footing-conditional as worded, but understated against the canonical footing (F-07). The convention for sqrt(2/(3pi)) is undeclared (F-08).
- **32pi.**
  - The gemini-note paragraph matches STANDING:332-337 ("interpretation, not a derivation"; "coherent physical reading ... not a derivation of kappa = 1/2").
  - Algebra re-derived: R*^2 Lambda = 8pi, kappa = 1/2, C = 32pi, the rational 4. R* = 2.89 times the de Sitter horizon radius, so R* is not a horizon.
  - The BBN exclusion is scoped only as "conditionally on its transfer assumptions": the constant couplings and the 95.4% level are dropped (F-06).
- **DR4** (against `PREREGISTRATION_DR4.md` and `edge_table_dr4.json`, read only).
  - Faithful: B = 1.000; floors 1.161/1.192; sigma_sys 0.02; the cap 8.07; 4,342 and 2,941 pairs re-derived (c = 3.291); the B kill line at 1.084; "survival test, never a confirmation".
  - Wrong: the "bare law" labelling, the 1.077 "kill", and the P2 power (F-02, F-05).
  - **The 1.063-1.127 band the drafter chose is the record's corrected value.** DOOR11_RESULT's own "1.16-1.18" was relabelled by Addendum 2 as Arm A's nu_RAR band, and the status page gives "1.063-1.127 over footings and fields". So the choice is right. Paired with "2.3-3.7 sigma" (canonical only), it is not (F-05).
- **Withdrawn claims.**
  - Seeds plus phase-2 patterns from STANDING, CLAIMS_AUDIT and DOOR11 Addendum 2 (`CFG265_withdrawn_lexicon.json`, 29 patterns): no hit on the real tex. No 5.09 keV, BH*, "theory closed", kappa derived, unqualified "beats 1/2pi", 1.16-1.18 as a P2 value, "1.08 MI", "only B escapes", 9/14, "cap excluded", "about one decade", or "largest standing failure".
  - The one creep found is a rescoped gloss rather than a lexicon item (F-04). The "ownership or an EFE" dichotomy echoes a corrected wording (F-20).

## 9. Controls (kept, in order)

- **Frozen plants M1-M14 and paraphrases P-a to P-c, first run (`CFG265_plant_v1.out`): 14 of 14 caught, 3 of 3 paraphrases not flagged, exit 0.** The re-run in `CFG265_plant.out` is identical.
  - **Caveat:** the plants were frozen before any code, but the new flag families (LANE, CLASS, KEYTOPIC, ARITH-COUNT, the withdrawn lexicon) were written knowing them, so 14/14 is partly by construction.
- **Fresh plants X1-X8,** written after the code and after the frozen-set run, and never used to tune a rule (`CFG265_plant_fresh.out`, exit 1):
  - caught: X1 (range), X3 (verb), X4 (withdrawn 1.16-1.18), X6 (scope), X8 (lane);
  - **MISSED: X2,** the dropped "conditionally on its transfer assumptions". The word "conditional" survives elsewhere in the same paragraph, so the paragraph-level CAVEAT rule cannot see the drop;
  - **MISSED: X5,** a single-digit change "n=2 -> n=3". Single-digit integers are not tracked: the same blind spot as CFG241's Y3;
  - X7 paraphrase: not flagged.
- **Self-disable** (M1 with NUM disabled): exit 1, as required. **Physics `--mutate`** (P2 exponent 0.45): exit 1 (2 of 7 self-controls fail), as required.
- **Harness defects, kept:**
  - Two ARITH regexes failed on the first main run (R12, R20, tex dollar placement; `CFG265_flags_firstrun.out`). They were fixed before any plant run and are marked v1.1 in the code.
  - The route recount's first version compared abbreviated hashes of different length and reported "frozen first" for same-commit lanes (`CFG265_route_recount_v1_buggy.out`). It was fixed to full hashes; this is what exposed F-01.
- **Flagger versus hand** (`CFG265_flags.out`):
  - 98 of 140 claims carry some flag. Precision is low (CAVEAT 15 of 80 flagged claims hand-non-FAITHFUL; CLASS 0 of 21; CITE 0 of 4; NUM 5 of 13; ARITH 2 of 2).
  - Recall: 17 of 29 hand-non-FAITHFUL claims carry a flag. **The flagger missed the CRITICAL (C041) and the claims behind all three MAJORs (C092-C094 and C097 carry no flag; C009 and C070 carry only unrelated NUM/CAVEAT noise)**, plus C010, C024, C068, C079, C086, C099 and C104. The gloss-level problems were found by reading, not by the pipeline.

## 10. Fairness checklist (F1-F12 of the criteria)

| item | score |
|---|---|
| F1 B's UFD failure attributed to B | FAIR |
| F2 LCDM comparator described as the record's | FAIR, with its extrapolation in Section 5 |
| F3 named theories | UNFAIR-TO-NAMED-AUTHORS in part (uncited, F-22; Hossenfelder, F-13) |
| F4 32pi exclusion scope | UNDECLARED (F-06) |
| F5 Milgrom footing | UNFAIR-TO-MOND, mild (F-07) |
| F6 the gemini note | FAIR |
| F7 DR4 | OVERSTATED (F-02) |
| F8 non-blindness | FAIR (Limitations; not in the abstract) |
| F9 owner-directed credit | FAIR |
| F10 literature scope | UNDECLARED (F-22) |
| F11 undeclared choices | UNDECLARED: kernel per number, r_ta convention, rho in Footing (F-02, F-08, F-18) |
| F12 AI-assisted / not peer reviewed | FAIR (title block and `.zenodo.json`; the PDF text agrees with the tex on every decimal token, and the three tex-only tokens are layout widths) |

LCDM fairness: the satellites' implication paragraph is mildly UNFAIR-TO-LCDM (F-21).

## 11. References (task item 9) and offline limits

- **Frozen WebFetch pair:**
  - [HFB17] (arXiv:1702.04358): title, authors and Phys. Rev. D 95, 064019 all agree. Its abstract carries "discrepant with the data by seven orders of magnitude", so row 2's attribution is HFB17's own.
  - [MC10] (arXiv:1009.4205): title and authors agree; the DOI resolves to ApJL 722(2) L209.
- **Labelled extras:**
  - [A20]: title and authors agree. The abstract's value is the BBN+CMB 0.99 +0.06/-0.05 at 2 sigma; the BBN-only 0.98 +- 0.06 (eq. 9) is not checkable here.
  - [M09]: agrees, PRD 80, 123536.
  - [O26]: exists, submitted to ApJ.
- **Offline:** D08, M09, M13, O26 and V17 match `citations/REFERENCES.bib`. [P36] and [P38] match the repo's deposit table.
- **Not checked:** journal-side pagination; the 2026 papers beyond their abstract pages. Each entry is reported as "agrees with arXiv / repo record, not checked against the journal".

## 12. Hand estimates graded (made after reading the tex, before any source)

| estimate | outcome |
|---|---|
| CRITICAL: P(0) = 0.50, P(1) = 0.30 | 1 |
| MAJOR median 2 | 3 |
| all findings: median 20, 80% interval 10-32 | 30, inside the interval |
| FAITHFUL about 80% | 111 of 140 = 79% |
| revision warranted, 0.55 | yes |
| recount reproduces, 0.60 | yes |
| a row label stronger than its lane, 0.55 | **no (wrong)** |
| "1.063-1.127 ... 2.3-3.7 sigma" reproduces, 0.35 | no |
| Footing uses rho_crit, 0.60 | yes |
| every route frozen-and-committed first, 0.45 | no (5 of 25) |
| all 14 plants caught first run, 0.30 | **yes (wrong side, partly by construction)** |
| paraphrases unflagged, 0.50 | yes |
| coverage met first run, 0.75 | yes |
| bib contradiction, 0.10 | none |

Attention list:
- **Became findings:** W1 (F-02, F-05); W3 (F-01); W4 (F-09); W6 (F-08); W7 (F-07); W8 (F-06); W9 (F-10); W10 (F-11); W14 (F-13, F-22); W15 (F-15); W17 (F-03, F-18); W23 (F-03).
- **Not findings:** W2 (restatement rows are the lanes' own no-gos); W5; W11 (the label is CFG259's); W12 (every variant H2 holds); W13 (HFB17's own words); W16 (the status page dates the swings 10-01); W18; W19 (P38 v1.2 exists, DOI matches); W20 (0.10 dex is P38 v1.2's); W21; W22 (FAIR).

## 13. Could not verify (from memory, unverified; none of these supports a finding)

- The original references for the named classes in F-22.
- Whether A&A 708, A287 is [AP26]'s final record.
- [A20]'s eq. 9 value and its constancy assumptions beyond the abstract.
- Whether the Lean proofs compile today (the build was not run).
- Whether a second reader would reproduce this classification.

## 14. Revision statement (frozen v1.1 rule)

There is one CRITICAL (F-01) and there are three MAJOR findings (F-02, F-03, F-04), all on text the draft itself states, so **a revision (v1.1 of the draft) is warranted before deposit.** Minimal content:

- F-01: one clause on how the routes were frozen.
- F-02: the DR4 paragraph and abstract (vii) rewritten to name the kernels and the preregistered verdict words.
- F-03: "reading" and "suggest" in the title or abstract, the Section 4 opener and line 155.
- F-04: P38 v1.2's own wording.

The MINOR fixes are optional but cheap. No result changes, no number in the table changes, and the audit stays valid; F-05, F-15 and F-16 change a few numbers in prose. The owner decides.
