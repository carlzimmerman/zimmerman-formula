# Observed command ledger

Unless noted otherwise, commands were run from the repository root on
2026-09-01. Status 0 means the program reproduced its own stated diagnostic;
it does not mean the candidate theory passed.

## Live-tree inspection

| Exact command | Status |
|---|---:|
| `git status --short --branch` | 0 |
| `git log --oneline -12` | 0 |
| `rg --files qwen_claude_field_theory/closure_2026/one_shot_final qwen_claude_field_theory/closure_2026/fried_chicken_2026 qwen_claude_field_theory/closure_2026/generalized_aest_2026` | 0 |

## Candidate-B and comparison tests

| Exact command | Status | Observed result |
|---|---:|---|
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_curvature_qumond_action_gate_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_curvature_qumond_adm_dirac_gate_2026.py` | 0 | 6 tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_curvature_qumond_clock_stueckelberg_gate_2026.py` | 0 | 3 tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_curvature_qumond_full_tf_gate_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_curvature_qumond_luminality_no_go_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_luminality_no_go_observational_strengthening_2026.py` | 0 | 4 tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_fable_5_1_comparison_gate_2026.py` | 0 | 3 tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_action_gate_2026.py` | 0 | 8/8 diagnostics |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_adm_dirac_gate_2026.py` | 0 | 8/8 diagnostics |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_clock_stueckelberg_gate_2026.py` | 0 | 6/6 diagnostics |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_full_tf_gate_2026.py` | 0 | 5/5 diagnostics |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_luminality_no_go_2026.py` | 0 | 6/6 diagnostics |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/luminality_no_go_observational_strengthening_2026.py` | 0 | 11/11 finite-shell diagnostics |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/fable_5_1_comparison_gate_2026.py` | 0 | Expected strict theory failures generated; 4/6 proposal gates pass |

## TDD failure history

These failures were retained as provenance rather than hidden:

| Exact command and working directory | Status | Reason |
|---|---:|---|
| `python3 test_fable_5_1_comparison_gate_2026.py` in `one_shot_final/` | 1 | Expected red: implementation module absent |
| `python3 test_fable_5_1_comparison_gate_2026.py` in `one_shot_final/` after first implementation | 1 | Exposed an invalid positive-domain assumption at the boundary \(c_{14}=0\) |
| `python3 test_luminality_no_go_observational_strengthening_2026.py` in `one_shot_final/` before refactor | 0 but invalid | Imported production module called `sys.exit` before any tests ran; treated as a false green and fixed with a main guard |
| `python3 test_luminality_no_go_observational_strengthening_2026.py` in `one_shot_final/` before the additive-constant bound | 1 | Expected red: new bound function absent |

## Existing closure regressions

| Exact command | Status | Observed result |
|---|---:|---|
| `python3 qwen_claude_field_theory/closure_2026/elliptic_phantom_action_gate_2026/test_elliptic_phantom_action_gate_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_ctp_auxiliary_dirac_gate_2026.py` | 0 | 4 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_ctp_matching_multiplier_no_go_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_field_dependent_spin2_bianchi_gate_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_spin2_no_slip_linearity_gate_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_tensor_nonlocal_localization_gate_2026.py` | 0 | 2 tests |
| `python3 qwen_claude_field_theory/closure_2026/elliptic_phantom_action_gate_2026/elliptic_phantom_action_gate_2026.py` | 0 | 7/7 diagnostics; Candidate A dead |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/ctp_auxiliary_dirac_gate_2026.py` | 0 | Standard CTP matching not second class |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/ctp_matching_multiplier_no_go_2026.py` | 0 | Direct multiplier erases physical response equation |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/field_dependent_spin2_bianchi_gate_2026.py` | 0 | Scalar-curvature completion carries a scalar/slip source |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/spin2_no_slip_linearity_gate_2026.py` | 0 | Fixed kernel too linear for deep MOND |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/tensor_nonlocal_localization_gate_2026.py` | 0 | Finite localization has opposite-sign TT pair |
| `python3 qwen_claude_field_theory/closure_2026/sf60_rotated_mmg_complete_field_theory_master.py` | 0 | Reproduced the older claimed synthesis only; no independent certification |
| `python3 qwen_claude_field_theory/closure_2026/sf61_honest_canonical_adm_closure.py` | 0 | Reproduced DBI-clock and FLRW overconstraint diagnosis |
| `python3 qwen_claude_field_theory/closure_2026/sf62_lapse_curvature_trilemma_proof.py` | 0 | Reproduced scoped pure-metric auxiliary trilemma |
| `python3 qwen_claude_field_theory/closure_2026/aest_j10/wf4_skeptic1_alpha1_anchor_lens.py` | 0 | Reproduced AeST preferred-frame anchor |

## Live Fable 5.1 scripts

These source files were untracked user/Fable work and were not silently added
to this commit.

| Exact command and working directory | Status | Observed result |
|---|---:|---|
| `python3 clock_current_nonlocal_mond_gate_2026.py` in `fried_chicken_2026/` | 0 | 40/40 diagnostics; metric response remains non-MOND |
| `python3 clock_current_localization_dof_gate_2026.py` in `fried_chicken_2026/` | 0 | 14/14 diagnostics; healthy localization adds two vector modes |
| `python3 gaest_setup_fj_anchors_stability_2026.py` in `generalized_aest_2026/` | 0 | FJ anchors; flags `c2` convention mismatch |
| `python3 gaest_setup_quadratic_modes_2026.py` in `generalized_aest_2026/` | 1 | After 1716 s it derived the two-polarization tensor block, then failed because the pole null space had dimension 2 while its residue helper asserted dimension 1 |
| `python3.13 sector2_conserved_charge_dust_2026.py` in `field_equations_2026/` | 1 | Crashes differentiating with respect to `Derivative(phi(t),t)/N(t)` before its advertised checks |
| `python3.13 dw_localized_noether_identity_2026.py` in `fried_chicken_2026/` | 1 | 18/26; all four metric-variation and both Noether-identity checks fail despite printed prose claiming solidity |
| `python3.13 dw_localized_dirac_count_2026.py` in `fried_chicken_2026/` | 1 | SymPy rank calculation crashes on an invalid NaN comparison |
| `python3 fc_operator_basis_scalar_sector_2026.py` in `fried_chicken_2026/` | 130 | Baseline checks passed; generic operator-basis scan remained in symbolic polynomial cancellation and was manually interrupted without a classification result |

## Public-record check

| Exact command | Status | Observed result |
|---|---:|---|
| `curl -sS https://zenodo.org/api/records/22033942` | 6 in sandbox, then 0 with approved network access | Public stats: 1 unique download, 0 unique views |

## Nonlocal-theorem correction

| Exact command | Status | Observed result |
|---|---:|---|
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door_2026/test_nonlocal_universal_claim_audit_2026.py` | 0 | 6 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door_2026/nonlocal_universal_claim_audit_2026.py` | 0 | 10/10 derived checks; universal theorem refuted and narrower localization obstruction established |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door_2026/nonlocal_alpha3_escape_and_darkfield.py` | 1 | Intentional compatibility failure: four withdrawn implications are no longer accepted |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2026/gateA/cde_l4c_ppn_alpha3.py` | 0 | 4/4 provenance checks; denominator mismatch reproduced, `alpha_3` remains uncomputed |

## Latest published cluster-paper audit

| Exact command | Status | Observed result |
|---|---:|---|
| `python3 test_itemC_phase_pinning_conservative_audit_2026.py` in `cluster_phase_2026/` before implementation | 1 | Expected TDD red: implementation module absent |
| `python3 qwen_claude_field_theory/closure_2026/cluster_phase_2026/test_itemC_phase_pinning_conservative_audit_2026.py` | 0 | 4 tests |
| `python3 qwen_claude_field_theory/closure_2026/cluster_phase_2026/itemC_phase_pinning_conservative_audit_2026.py` | 0 | 6/6 checks; exact EOS and conservative-flow qualification derived |
| `python3 qwen_claude_field_theory/closure_2026/cluster_phase_2026/itemC_phase_pinning_dynamics_2026.py` | 0 | Original published calculation reproduced: 27 checks, 0 failures |
| `python3 build_cluster_phase_pinning_pdf.py` in `opus_48_extended_research/papers/` | 0 | Rebuilt corrected 8-page PDF, 88,099 bytes |
| `pdfinfo opus_48_extended_research/papers/pdf/CLUSTER_PHASE_PINNING_POLYTROPE.pdf` | 0 | 8 Letter pages, PDF 1.5, no form |
| `pdftoppm -png -r 120 opus_48_extended_research/papers/pdf/CLUSTER_PHASE_PINNING_POLYTROPE.pdf tmp/pdfs/cluster_phase_qa/page` | 0 | Rendered all pages for visual inspection |
| `montage tmp/pdfs/cluster_phase_qa/page-1.png tmp/pdfs/cluster_phase_qa/page-2.png tmp/pdfs/cluster_phase_qa/page-3.png tmp/pdfs/cluster_phase_qa/page-4.png tmp/pdfs/cluster_phase_qa/page-5.png tmp/pdfs/cluster_phase_qa/page-6.png tmp/pdfs/cluster_phase_qa/page-7.png tmp/pdfs/cluster_phase_qa/page-8.png -thumbnail 420x -tile 2x4 -geometry +12+12 tmp/pdfs/cluster_phase_qa/contact.png` | 0 | Contact-sheet inspection found no clipping, overlap, or overflow |

## CCNL candidate audit

| Exact command and working directory | Status | Observed result |
|---|---:|---|
| `python3 qwen_claude_field_theory/closure_2026/candidate_ccnl_2026/ccnl_mond_gates_2026.py` | 130 | Proposal produced two numerical failures, then remained inside SymPy's higher-derivative Euler calculation until manually interrupted; no final advertised verdict was reached |
| `python3 qwen_claude_field_theory/closure_2026/candidate_ccnl_2026/ccnl_mond_gates_2026.py` after the committed rewrite | 0 | 29/29 after 544 s; the output itself leaves the in-in phase space owed, and is superseded on that gate by the later instability and Dirac audits |
| `python3 test_ccnl_action_dirac_audit_2026.py` in `candidate_ccnl_2026/` before implementation | 1 | Expected TDD red: audit module absent |
| `python3 test_ccnl_action_dirac_audit_2026.py` after the first report implementation | 1 | Expected regression red: unsimplified eigenvalue product exposed a symbolic comparison bug |
| `python3 qwen_claude_field_theory/closure_2026/candidate_ccnl_2026/test_ccnl_action_dirac_audit_2026.py` | 0 | 8 tests |
| `python3 qwen_claude_field_theory/closure_2026/candidate_ccnl_2026/ccnl_action_dirac_audit_2026.py` | 0 | 14/14 derived checks; exact kernel survives, ordinary localized action fails the auxiliary Dirac/ghost gate |
| `python3 qwen_claude_field_theory/closure_2026/candidate_ccnl_2026/ccnl_inin_linear_scalar_2026.py` | 0 | 12/12 findings reproduced; complex longitudinal modes at `y>=0.5`, negative residue in the tested deep-MOND window |

## Nonlocal spin-2 residual

| Exact command and working directory | Status | Observed result |
|---|---:|---|
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_spectral_state_space_gate_2026.py` before implementation | 1 | Expected TDD red: audit module absent |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_spectral_state_space_gate_2026.py` | 0 | 6 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/spectral_state_space_gate_2026.py` | 0 | 7/7 derived checks; positive spectral memory requires extra states |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_field_dependent_spin2_zero_field_gate_2026.py` before implementation | 1 | Expected TDD red: audit module absent |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_field_dependent_spin2_zero_field_gate_2026.py` after the first implementation | 1 | Expected regression red: symbolic positivity was not yet represented as a Boolean proof object |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_field_dependent_spin2_zero_field_gate_2026.py` after adding the projector test | 1 | Expected regression red: general projector result absent |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_field_dependent_spin2_zero_field_gate_2026.py` | 0 | 7 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/field_dependent_spin2_zero_field_gate_2026.py` | 0 | 7/7 derived checks; no slip forces `a=c`, then exact `mu(0)=0` zeros the TT Hessian |
| `python3 -m pytest -q` on the nine aligned regression files | 1 | Environment limitation: `pytest` is not installed; all nine files were then run through their self-running entry points and exited 0 |
| `python3 -m compileall -q` on the six changed Python files | 1 | macOS denied writes to its external Python cache directory; no syntax diagnostic was emitted |
| `env PYTHONPYCACHEPREFIX=/tmp/zimmerman_formula_pycache python3 -m compileall -q` on the same six files | 0 | Syntax compilation completed using a task-specific writable cache |
| `python3 .../mathbox/.../validate_manifest.py` on the first spin-2 manifest draft | 1 | Expected audit hardening: four required provenance blocks were missing |
| `python3 .../mathbox/.../validate_manifest.py` on all final aligned manifests | 0 | New spin-2, CCNL Dirac, and one-shot manifests valid; all recorded output hashes matched |

## Final verification

| Exact command | Status | Observed result |
|---|---:|---|
| `PYTHONPYCACHEPREFIX=/tmp/zimmerman_pycache python3 -m compileall -q qwen_claude_field_theory/closure_2026/one_shot_final` | 0 | Syntax compilation passed |
| all 15 exact aligned test commands listed above, rerun on the final pre-commit tree | 0 | 15/15 programs, 46/46 individual tests |
| `python3 qwen_claude_field_theory/closure_2026/one_shot_final/test_curvature_qumond_luminality_no_go_2026.py && python3 qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_luminality_no_go_2026.py` | 0 | Manifest load-bearing command; 2 tests and 6/6 theorem checks |
| `python3 -c "import json,hashlib,pathlib,sys; m=json.load(open('qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_audit_manifest_2026.json')); bad=[o['path'] for o in m['outputs'] if hashlib.sha256(pathlib.Path(o['path']).read_bytes()).hexdigest()!=o['sha256']]; print('outputs=%d hash_mismatches=%d'%(len(m['outputs']),len(bad))); sys.exit(bool(bad))"` | 0 | 18 outputs, 0 hash mismatches |
| `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/one_shot_final/curvature_qumond_audit_manifest_2026.json` | 0 | Valid computation manifest |
| `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/nonlocal_door_2026/nonlocal_universal_claim_audit_manifest_2026.json` | 0 | Valid computation manifest |
| `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/cluster_phase_2026/itemC_phase_pinning_conservative_audit_manifest_2026.json` | 0 | Valid computation manifest |
| `python3 -c "...verify all output hashes from the three computation manifests..."` | 0 | 25 outputs, 0 hash mismatches |
| `git diff --check` | 0 | No whitespace errors |

Commit and push commands are appended only after they have actually completed.
