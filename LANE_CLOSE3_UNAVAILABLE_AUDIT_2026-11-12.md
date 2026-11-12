# CLOSE-3 (B): every lane under fable52_push/, closure_2026_11_10/, closure_2026_11_11/ and hy4_preview_push/ with no RESULT.md, or with a NO VERDICT label

Audit lane, 2026-11-12. Read-only. Adopts nothing, relabels nothing, registers nothing.
Footings never pooled. kappa = 1/2 FITTED; not theory closed. Cold dark energy is a gravitating
field component, never a particle.

**Method.** Walked all 93 lane directories under the four roots. A lane is listed if
`RESULT.md` is absent, or if the label printed in its `RESULT.md` is NO VERDICT (as frozen; where a
post hoc amendment changed the label, the amendment's label is printed beside it and the lane is
still listed, because the frozen label is the one on the record). Reasons quoted are the lanes' own
words. Nothing here is recomputed.

**Counts.** 93 lane directories. 19 have no `RESULT.md`. 15 carry a NO VERDICT label (13 as the
final label, 1 — DCN1 — as the label of every pre-registered reading with a post hoc A6 label
beside it, 1 — FINAL4 — on one graded row). Of the 19 missing, 6 are graded lanes with frozen
criteria and 13 declare themselves notes, forecasts, audits or scratch.

`hy4_preview_push/CLOSE-1_DT2` was created during this walk (a sibling lane of this audit); it is
listed as in-flight, not as a gap.

---

## B1. NO `RESULT.md`, graded lane (criteria were frozen, scripts ran, the label file was never written)

These are the cheapest closes in the whole set: in every case the compute is already done and only
the label is missing.

| Lane | Artifacts present | The untested question (one line) | Cheapest pre-registered test that settles it |
|---|---|---|---|
| `closure_2026_11_10/GRW2_required_growth_history` | FROZEN_CRITERIA, AMENDMENT_A1, `grw2.py/.json/.out`, `grw2_gates.py/.json/.out`, `grw2_rows.out` | The inverse of SRH1: what growth history `R_set(z, M_b)` do the four gates *require*, graded against the independent rows? | `grw2_gates.py` has already run (`grw2_gates.out` exists). Read it against the frozen gate table and write `RESULT.md` in the frozen label vocabulary. **No new compute.** |
| `closure_2026_11_11/DW1_desi_dr2_mw_mass` | FROZEN_CRITERIA, README, `dw1.py`, `dw1.out`, `dw1_results.json` | Does DESI DR2 III's Milky Way mass — `M(<80 kpc) = 6.36 (+0.53/-0.48)e11 Msun`, `M200c = 1.19 (+0.14/-0.12)e12`, and the 13-radius enclosed-mass profile at 20-80 kpc — sit inside or outside the framework's prediction? | `dw1.out` and `dw1_results.json` exist. Read the 13 points against the frozen gates and write the label. **No new compute.** |
| `hy4_preview_push/FINAL-7_what_it_is` | FROZEN_CRITERIA, `fin7.json/.out`, five `fin7_MUTATE_M*.json/.out` | What the medium *is* — the M5 hypothesis triage (criteria §0). | `fin7.out` plus five MUTATE outputs exist. Read the exit row and the five arms against the frozen gates and write the label. **No new compute.** |
| `fable52_push/HIS1R_history_regrade` | COMPARISON, READING, **`RESULT_BLIND.md`**, `his1r.json/.out`, `his1r_MUTATE.*`, `his1r_compare.out` | Does a blind regrade reproduce HIS1's per-class history offsets? | The label already exists in `RESULT_BLIND.md`. Promote it to `RESULT.md` (or state in one line why it is withheld). **No new compute.** |
| `fable52_push/FINAL-9_lean_static`; `fable52_push/FINAL-11_lean_budget`; `hy4_preview_push/FINAL-10_lean_stress`; `hy4_preview_push/FINAL-11_lean_budget` | `FINAL9_StaticHalo.out`, `Final11Budget.out`, `build1.out`, `lane_result.json`, `verify*.out` | Does the Lean certification of the static halo / the amount budget / the stress tensor compile with zero `sorry` and only the allowed axioms? | The Lean runs are done (`.out` files present). Read each exit code and the axiom line and write a one-page `RESULT.md` per lane. **No new compute.** |

## B2. NO `RESULT.md`, but the lane declares itself a note / forecast / audit / scratch

Listed so they are not mistaken for gaps. Each states in its own header that it has no criteria and
no label. Their unanswered questions are real but were never pre-registered.

| Lane | What it is (its own words) | The question it leaves open | Cheapest test, if the record wants one |
|---|---|---|---|
| `fable52_push/DT1_dust_term_design` | "A design note, not a graded lane: no criteria, no label" | What the clock's dust term has to do. Its candidate was graded by MK2 and returned NO VALUE / NO VALUE. | Already settled negatively by MK2; close as **SUPERSEDED BY MK2 (NO VALUE)** rather than run. |
| `fable52_push/EQ1_cold_dark_energy_equations` | "A reference sheet, not a lane and not a new result" | Which equations are certified [C], hand-checked [H], measured [M], or not given [X]. | None needed; mark **[X]** items as the open list. The **[X]** tags *are* the open-question register. |
| `fable52_push/FB1_form_b_from_the_action` | "A note with one check, not a graded lane" | Completeness of form B against the owner's decision file. | Its four parts: one answered by the record, three not. Freeze one lane per unanswered part (the external-field disc stability went to SCS3 → still NO VERDICT). |
| `fable52_push/KO3F_spec_veto_power_forecast` | "A forecast, not a graded lane" | Would spectroscopy sharpen KO1's host veto? Answer given: **"Not on the data that exist today"** — DESI DR1 redshifts shrink the late-type outer error from 0.68/0.62 to 0.57/0.52 of the law; a 3-sigma call needs ~0.47. | None. It answers its own question: **NO POWER**. Freeze that as the label. |
| `fable52_push/SHAPE_search` | "Notes, not lanes: no criteria, no labels" | Why the cold component's pull is `g_c = a0 g/(g + a0)`. Route A: RE-DESCRIPTION ONLY; Route B: DOES NOT GO THROUGH. | Freeze a lane on Route C/D (the two the README does not summarise as failed) with the same verdict vocabulary. |
| `closure_2026_11_10/AMT1_amount_budget` | "Arithmetic only" | How much cold charge there is to spend against the 59.5 M_b form B needs. | This is the same question FINAL-3 was chartered to answer and did not. Fold AMT1's three contending amounts into the FINAL-3 re-run. |
| `closure_2026_11_10/R541_why_the_cold_share` | "This is a note, not a graded lane" | Why is the cold share 5.41? Its answer: **"5.41 is what the acoustic peaks of the CMB need. It is fitted (lane F1A)… NOT DERIVED. In the adopted action it is FREE (an integration constant)."** | This is FINAL-3's question, asked earlier and answered "free". FINAL-3's D1 now says it is *not* free — it is pinned to `R` by charge conservation, and that value fails KiDS at +4.85 / +4.93 sigma. The two notes must be reconciled. |
| `closure_2026_11_10/_fzs1_scan_tmp` | scratch (scan outputs for FZS1) | — | Delete or move under FZS1; not a lane. |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT` | "Lean certification bookkeeping… No new physics" | sha256-level bookkeeping of `fable_independent_2026/lean_2026/`. | None; the audit is complete and self-hashing. |
| `hy4_preview_push/FINAL-20_kappa_audit` | "Auditing lane. Nothing committed by this lane" | Audit of FINAL-16..FINAL-19 (the kappa lanes). | None; it is an audit. Its conclusion stands: **kappa = 1/2 stays FITTED unless a lane outputs it.** |
| `hy4_preview_push/CLOSE-1_DT2` | created during this walk | sibling of this audit | In flight, 2026-11-12. Not a gap. |

## B3. `RESULT.md` present, label NO VERDICT (as frozen)

Every reason below is the lane's own.

| Lane | Frozen label | The untested question (one line) | Cheapest pre-registered test that settles it |
|---|---|---|---|
| `closure_2026_11_10/BX1_fixed_amplitude_reference` | NO VERDICT / NO VERDICT. "KA3 fails and MUTATE MB2 does not bite." | Is the fixed-amplitude reference a real comparator? | Two pre-existing criteria items, both cheap: (i) repair or replace **KA3**; (ii) redesign **MB2** so it bites — as frozen it reads 1.8 / 1.5 / 1.2 against a `>= 1.5` single/pair line. Neither needs a new run of the pair pipeline. |
| `closure_2026_11_10/EFN1_external_field_nonlinear` | NO VERDICT / NO VERDICT, "in every reading (frozen, A1, A2-A4). Neither route decides." | What is the nonlinear outcome of SCS3's external-field instability? | The lane lists *why each reading is NO VERDICT* (line 71). Pick the single blocker common to all four readings and freeze one amendment that removes it; four post hoc amendments have already failed to find it, so the cheap move is a scope cut to the one route whose blocker is removable. |
| `closure_2026_11_10/HLF1_own_halo_list_forest` | NO VERDICT / NO VERDICT. Part A: MA1 "DOES NOT BITE" (160 of 455 above 1e13 in the cell-permuted grid). Part B: the forest row. | Does CO1's redistribution survive the record's *own* halo list, and does it survive at forest redshifts? | Part B is the binding one and it is a single number: CO1's z=0 redistribution held to the forest gives `Delta chi^2` 160.74 / 1025.57 against a gate of 4; under the record's fade it gives 0. **The row turns entirely on how the redistribution evolves from z 0 to z 3.** Cheapest test: freeze one `R_cold(z)` law (a two-parameter fade is enough), re-run the single forest row, and the row decides. |
| `closure_2026_11_10/KL1_lensing_amplitude_survey_assumptions` | Part A: NO VERDICT / NO VERDICT as frozen ("the MUTATE arm MC1 does not bite"; TENSION / TENSION under A1). | Does the lensing amplitude move when the survey's own assumptions are swapped for the newest release? | Replace **MC1** with an arm that moves the quantity the stack is actually sensitive to — moving the gas with `f = 0.2` barely changes `R_tot`. One re-run of the existing `MC1` variant at a larger `f` settles whether the arm is vacuous or the gate is. |
| `closure_2026_11_10/KL1R_blind_legacy_regrade` | NO VERDICT / NO VERDICT. "MA2 cannot bite on DES Y3. With every density halved, only 4/4 DES points are signal-dominated." Also "MB2 does not bite." | Is the KiDS-Legacy regrade decided by the data or by the survey's priors? | **Scope cut, pre-registered:** drop the DES Y3 rows from the graded set and re-label on KiDS-Legacy alone, where the mutant can act. The lane's own finding is that the DES Y3 rows have no power to be moved; grading them cannot produce anything but NO VERDICT. |
| `closure_2026_11_10/NH2_ngc1052_host_mass` | NO VERDICT / NO VERDICT. "Two known answers fail: KA2 (KT2017's R_g) and KA4c (mock-group estimators biased high). The criteria say grading is read only after every known answer passes." | Is NGC 1052's measured mass enough for its tides to reach DF2 / DF4 under form B? | The blocker is the two known answers, not the measurement. Recompute **KA2** and **KA4c** from the same two tables (group 9843 in KT2017; the GC table) with the bias correction, re-run the unchanged grading script, and read the label. Under A1 the lane already reports both failures make the group ceiling *looser, never tighter*. |
| `closure_2026_11_10/PAR1_parent_action_spec` | NO VERDICT / NO VERDICT, as frozen, under A1 and under A2. "Every known answer passes, every MUTATE arm bites, and the Lean file compiles. The label is NO VERDICT because **two branches stay open and no member of them was written and graded here.**" | Find the parent action whose static galaxy limit is action (A)'s law and which works for CMB, growth, lensing, clusters, galaxies and the Solar System — or prove none exists. | This is the one NO VERDICT that is not a defect: the lane did everything asked and the label is honest. The cheap decisive step is to **write and grade one member of each open branch** (one candidate action, one non-existence argument) and let the frozen gates read them. The gates are already written. |
| `closure_2026_11_10/VSH1_viscous_shock_settling` | NO VERDICT / NO VERDICT as frozen. (A1, post hoc: SETTLES BY SHOCK / SETTLES BY SHOCK.) | Does AKS1's estimate T7 hold — does a halo settle to CFG461's edge by today for `nu >= nu_S = r_e*^2/t0`? | The blocker is one known answer: **KA3 as frozen FAILS (57.9 against 88 at log M_b 9; the 11.5 run had not reached z = 0)**, while **KA3' under A1 PASSES (87.7 / 597.0)**. Cheapest test: finish the two `log M_b 11.5` runs to z = 0, re-run `vsh1.py ka && grade && mutate`, and promote A1 to a pre-registered amendment so the SETTLES BY SHOCK label rests on a frozen rule. |
| `closure_2026_11_10/XCV1_xcop_nonhydrostatic_mass` | NO VERDICT / NO VERDICT (KA-3 failed: HeCS centres A85 0.6 Mpc from X-COP). A1, post hoc: AT THE CEILING / AT THE CEILING. | Do X-COP's non-hydrostatic mass corrections sit at the ceiling form B allows? | The blocker is a single centre convention. Freeze an amendment adopting **A1's** centre handling (which already produced AT THE CEILING, with A85 tagged CENTRE OFFSET 9.5') and re-grade under a frozen rule. One re-run. |
| `fable52_push/SCS2_static_clock_stability_discs` | External-field family: NO VERDICT / NO VERDICT. "a known answer fails: KA4's two-resolution clause fails." | Is the static clock stable around an isolated disc in an external field? | Repair **KA4's two-resolution clause** (it is a convergence check, not a physics row): run the third resolution the clause asks for, and the family reads. SCS3 took this family on and is still NO VERDICT, so do this in SCS2 first where the clause is the only blocker. |
| `fable52_push/SCS3_external_field_stability` | NO VERDICT / NO VERDICT on every family and under A1, A2 and A4. Rule alone: UNSTABLE on 11 of 16 / 10 of 16 backgrounds (axial, 2D); 4 of 8 / 4 of 8 (3D); RATE UNBOUNDED on 1 / 1 for the thick-disc twin. | Does SCS2's external-field instability have a converged magnitude, and is it a verdict? | The instability itself is established (11 of 16 / 10 of 16). What is missing is **convergence of the rate**. Cheapest test: one resolution doubling on the *worst* background only, graded against a frozen convergence line. If the rate converges, the label becomes UNSTABLE; if not, it stays NO VERDICT for a stated reason. |
| `closure_2026_11_10/WV1_wave_dust_split_charge` | V1 as frozen: NO VERDICT (known answer KA4(ii) fails as frozen). V1 under A1: STRUCTURE FAILS. Also "**M4 (A -> dPhi/dr) DOES NOT BITE**". | Does the wave/dust split of the charge survive? | Repair **KA4(ii)** and redesign **M4** (as frozen it gives 0.264-0.272 against a 0.01 line — the arm is vacuous, so it cannot bite). Both are criteria edits, not new physics runs. |
| `fable52_push/GRW1_late_growth_baryons_and_law` | "As frozen: NO VERDICT / NO VERDICT" (T-A FALLS SHORT / FALLS SHORT; T-S FALLS SHORT AND OVERSHOOTS). | Do baryons under the a0 law build late structure when the cold component is warm late? | The blockers are two mutants that **do not bite as frozen**: M-COLD (0 of 4) and M-2A0 (does not bite on alt at 1000 km/s: the top forest bin at z 3 falls 1.6 %). Cheapest test: raise the mutant's lever until the *reference* quantity it is supposed to move moves by more than the line — a one-parameter scan, no new pipeline. |
| `fable52_push/DCN1_disc_centre_null` | "**Every reading frozen before the outcome was seen is NO VERDICT**, each on a known-answer gate. A6 is the only reading in which every known answer passes." Final label under post hoc A6: ARTEFACT / ARTEFACT. | Is the disc-centre null a physical prediction or an artefact of the reading? | The lane answers it under A6 (ARTEFACT) but A6 is post hoc. Cheapest test: re-freeze A6 as a *pre-registered* reading and re-run the six known answers unchanged. If they pass under a frozen A6, the NO VERDICT chain breaks. Also noted: "M3's numerical half does not bite (2.1 % < 5 %)" — repair that arm too. |
| `closure_2026_11_11/FINAL4_growth_history` | Lane label is not NO VERDICT, but **the absolute C3 row is**: "a known answer that fails gives NO VERDICT… it gives `chi2_ref = 76.692 / 76.692` where CO1 reports `2.23 / 2.20`." Also "MUTATE (partial; one arm does not bite)." | Does form B's growth history reproduce CO1's DESI DR1 `f sigma8` rows in absolute terms? | The mismatch is a factor ~34 in `chi2_ref` against CO1's. Cheapest test: **reproduce CO1's C3 row in this lane's own pipeline before grading anything** — it is a known-answer reconciliation, one script, and if it lands the absolute row can be graded. The multiplicative-shift result the lane reports stands either way. |

---

## B4. What the table says

- **The dominant failure mode is not physics, it is a vacuous mutation arm or one broken known
  answer.** Of the 15 NO VERDICT lanes, 10 name a specific mutant that does not bite or a specific
  KA that fails. In each of those the fix is a criteria edit plus one re-run, not new theory.
- **Three NO VERDICTs are structural and will not close cheaply:** PAR1 (two branches left open by
  design — an honest NO VERDICT), SCS3 (the rate will not converge), EFN1 (four readings, no route
  decides). These should be recorded as *the record cannot say*, not pushed again.
- **Six of the 19 missing `RESULT.md` files need no compute at all** — the scripts already ran and
  the outputs are in the folders. Only the label file is missing. That is the cheapest closure
  available anywhere in this audit.
- **Two separate lanes ask FINAL-3's question** — `R541_why_the_cold_share` ("5.41 is fitted, NOT
  DERIVED, in the adopted action it is FREE") and `AMT1_amount_budget`. FINAL-3 was chartered to
  close it and did not run. Part (A) of this audit derives the share in closed form and finds it is
  *not* free — conservation pins it to `R` — and that this pinned value fails KiDS by 4.9 sigma.
  R541's "FREE" and that result are in direct contradiction and one of them must fall.
