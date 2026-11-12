# Audit of the Codex session's uncommitted correction notices (2026-11-12)

The owner asked for these notices to be checked before PAPER72 version 1.2 relies on them. Four independent auditors
each took one slice; each redid the deciding step with its own derivation or script and was read-only on every lane,
research and PAPER72 file. The lead session re-checked the items marked (lead) below by hand or from git. The notices
and the research folder they cite (`research_closure_2026_11_12/`) were UNCOMMITTED when audited, so this folder grades
working-tree text as it stood on 2026-11-12; it adopts none of it.

| slice | file | bottom line |
|---|---|---|
| C1 dust threshold and growth | `C1_dust_and_growth.md` | Notices CORRECT WITH LIMITS. With the polarization response on, the cold dark energy's self-gravity factor is mu^2/(mu^2 + k^2), valid only while the clock's gradient is well below a0 (a condition the notices do not state). MK1 stays NO VALUE / NO VALUE; only its 2.51e4 per Mpc line is touched, and "withdrawn" overstates: no replacement likelihood was run and the two factors agree to first order near 2.5e4. FINAL4's notice CORRECT (its 0.880 growth ratio is a 12.0 % suppression, not 3.6 %) (lead: arithmetic). |
| C2 PIK1 and FRM1 | `C2_pik1_and_frm1.md` | Corrections CORRECT on substance. PIK1's linear-invisibility step fails except for gates flat at the origin, so its NO VALUE is not established; PIK1's criteria, result and scripts were one commit, one committed script does not compile and no output exists (lead: confirmed in git). FRM1's frozen line is FAILS / FAILS and its class bands are retrospective (lead: commit order and the "before the table was read" sentence confirmed). |
| C3 kappa lanes and CLOSE-1 | `C3_kappa_and_dt2.md` | Every notice's physics CORRECT. CLOSE-1's label FOLDS / FOLDS is unchanged; its linear gate moves from pass 0.551 to fail 0.491 and its derived settled radius is withdrawn. No file says kappa or 5.41 is derived. Three edits should not be committed as they stand (below). |
| C4 gas signal and the research folders | `C4_gas_signal_and_combined_route.md` | FINAL5's correction CORRECT (flat-sheet projection, beam, an X-ray flux 1e4 too large; the forecast is rightly withdrawn) (lead: projection factors 2.85 / 1.61 / 0.76 re-computed). Both research folders conclude the theory is not closed and claim no derivation, joint, medium or rescued row. |

## What should change before any of it is committed

1. **Lane scripts were rewritten in place.** A forward correction adds; it does not replace. Restore from HEAD and add
   the corrected code under new names: `hy4_preview_push/FINAL5_measurement/final5_signal.py` (552 lines replaced by a
   wrapper around an untracked file), `fable52_push/PIK1_pi_gated_dust/pik1.py` and `pik1_var.py` (both now dispatch to
   one untracked checker), the four `hy4_preview_push/CLOSE-1_DT2/dt2_*.py` (the committed `.out` files no longer
   follow from them), `hy4_push/H062_exponent_gap.py` (committed `.out` stale).
2. **`hy4_preview_push/FINAL-17_kappa_A/final17_kappa_A.py`**: the edit replaces a pre-registered label in the
   else-branch with an unregistered one, so the mutation twin no longer prints the label its amendment names. Revert
   that line.
3. **`hy4_preview_push/OUT-3_kappa_equality_fixed/FROZEN_CRITERIA.md`**: the notice is right but sits in a frozen
   file. Move it to a new correction file.
4. **`closure_2026_11_12/CLOSE2_par1_branch_union/close2_grade.json`**: a re-run artefact naming a temp copy that no
   longer exists. Restore from HEAD.
5. **`fable_independent_2026/lean_2026/lakefile.toml`**: registers a library whose root files are untracked. Commit it
   with those files or not at all.
6. **PIK1's two notices contradict each other** (one says an instability is established, the other that the full
   constrained system is not shown to have a ghost). Reconcile them.
7. **Wording**: "cold dark self-gravity factor" should read "cold dark energy's"; MK1's "cannot be transferred
   unchanged" should add the validity condition and say no replacement likelihood exists.
8. **Home paths** appear in run records under `research_closure_2026_11_12/` (run_commands and stderr files). Strip
   them before committing.
9. **The research folders are untracked**, so "criteria frozen before numbers" cannot be shown from git; one contract
   file was last modified after its own early results. Their "independent reviews" are agents of the same session, not
   an independent re-grade.

Also found, not part of the notices: about 22 of the 53 modified tracked files are older uncommitted outputs (11-05 to
11-09), and the working copy of `closure_2026_11_07/ARGON_RESPONSE_ASSESSMENT_2026_11_07.md` is an older committed
version that lacks a section HEAD has.

## Not checked by anyone

The instability formula and the roughly 450 per Mpc galaxy pressure ceiling in `closure_push_02`; the 1.44212 baryon
growth in `combined_route`; a corrected CMB lensing-shape likelihood for the dust term; any coupled-gravity spectrum of
the gated dust term; the corrected `dt2_reach.py` output.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
