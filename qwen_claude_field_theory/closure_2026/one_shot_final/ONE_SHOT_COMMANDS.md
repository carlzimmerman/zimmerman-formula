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

### Projector/CDE checkpoint publication

| Exact command | Status | Observed result |
|---|---:|---|
| `git commit -m "Correct projector and CDE constraint certificates"` | 0 | Created `d535b8ee1`; 24 intended files, unrelated live-tree work excluded |
| `git push origin main` | 0 | Published `dadab0384..d535b8ee1` to `origin/main` |

## Exact-kernel, CDE-L4C-2Delta, FLRW, and Cassini attack (2026-09-03)

Status 0 means the stated derivation or exclusion certificate reproduced. It
does not mean the full relativistic theory passed.

| Exact command | Status | Observed result |
|---|---:|---|
| `python3 hunt_2026/test_exact_exponential_mu_2026.py` | 0 | 13 tests; exact inverse, input guards, dependency graph, nonlinear-BVP scoping, and executable channel identities |
| `python3 hunt_2026/exact_exponential_mu_2026.py` | 0 | 11/11 checks; Route A distinguished from exact target; twelve scoped channels, not twelve independent laws |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/test_cde_l4c_2delta_action_gate_2026.py` | 0 | 12 tests; finite-k static variation, explicit ADM generation, and zero/nonzero-field Dirac chains |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_action_gate_2026.py` | 0 | 21/21 checks; corrected ADM normalization gives `det=A^8 k^32`, one scalar pair, `omega^2=lambda_parallel*k^2/3` |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/test_cde_l4c_2delta_flrw_gate_2026.py` | 0 | 8 tests; background equations, exact expanding witness, and FLRW principal family |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_flrw_gate_2026.py` | 0 | 10/10 checks; FLRW exists; promoted principal family retains the pair, while the direct `k=0` chain differs |
| `PYTHONWARNINGS=error python3 hunt_2026/exact_mu_cassini_2026/test_exact_mu_qumond_cassini.py` | 0 | 6 tests; inverse, independent quadratures, domain/tail controls, mutations, physical conversion |
| `PYTHONWARNINGS=error python3 hunt_2026/exact_mu_cassini_2026/exact_mu_qumond_cassini.py` | 0 | Exact-target standard QUMOND gives 3.761895912 and 4.961976265 times the adopted ceiling for the canonical and alternate `a0` footings |
| each of the four main programs piped to `diff -` against its `.out` | 0 | All recorded outputs match fresh stdout |
| Mathbox `validate_manifest.py` on the exact-kernel, CDE-L4C-2Delta, and Cassini manifests | 0 | All three computation manifests valid |
| `python3 qwen_claude_field_theory/closure_2026/door_a_2026/doorA_alpha1_generality_theorem.py` | 0 | 12 reported checks; only the AeST/vector algebra is computed. T3b, T4, and M2 are literal `True` assertions, so the universal local-class verdict is not accepted |

### Publication

| Exact command | Status | Observed result |
|---|---:|---|
| `git commit -m "Audit exact MOND action and zero-field obstruction"` | 0 | Created `92257aa65`; 21 intended files, unrelated live-tree work excluded |
| `git push origin main` | 0 | Published `1cdc25ea5..92257aa65` to `origin/main` |

### TDD and audit-hardening failures retained

| Exact command and state | Status | Reason |
|---|---:|---|
| `python3 test_exact_exponential_mu_2026.py` before implementation | 1 | Expected red: implementation module absent |
| the same inverse test after first implementation | 1 | Deep-`x` stopping tolerance scaled to one and lost relative accuracy |
| the same report before the analytic branch correction | 1 | Exposed the false claim that `lambda_parallel` grows for every `y>0` |
| the same test before stable logarithmic-slope evaluation | 1 | `expm1(1e5)` overflowed under strict floating-point errors |
| `python3 test_cde_l4c_2delta_action_gate_2026.py` before implementation | 1 | Expected red: action module absent |
| the same test before the zero-field extension | 1 | Expected red: `zero_field_dirac` result absent |
| the same test after first count comparison | 1 | Exact rational degree count was compared to a Python float |
| the same test after updating the next calculation | 1 | Stale string expected the superseded full-Dirac wording |
| the same test before the positive-gradient extension | 1 | Expected red: `nonzero_field_dirac` result absent |
| the same test after the extension | 1 | Algebraically opposite bracket factorizations needed entrywise simplification before antisymmetry comparison |
| `python3 test_cde_l4c_2delta_flrw_gate_2026.py` before implementation | 1 | Expected red: FLRW module absent |
| the same test before the exact expanding witness | 1 | Expected red: simultaneous three-equation FLRW witness absent |
| `PYTHONWARNINGS=error python3 test_exact_mu_qumond_cassini.py` before implementation | 1 | Expected red: hardened Cassini module absent |
| the Cassini test after requiring both `a0` footings | 1 | Expected red: alternate footing constant was not yet implemented |
| the action test after requiring ADM provenance | 1 | Expected red: manually entered Dirac block had no `adm_principal_derivation` |
| the FLRW test after requiring a direct `k=0` restart | 1 | Expected red: promoted finite-k family had no independent homogeneous chain |
| `python3 -m py_compile` without a local cache prefix | 1 | macOS denied the external system Python cache; no syntax failure was emitted |

Commit and push commands are appended only after they have actually completed.

## Projector and CDE certificate correction (2026-09-03)

Status 0 below means that the scoped diagnostic reproduced; it is not a
fried-chicken theory PASS.

| Exact command | Status | Observed result |
|---|---:|---|
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_metric_only_elliptic_projector_gate_2026.py` | 0 | 13 tests; smooth rank-changing counterexample, sector split, and provenance guards |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/metric_only_elliptic_projector_gate_2026.py` | 0 | 12/12 checks; broad regular-projector no-go withdrawn, singular zero-field response exposed |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/test_ricci_polynomial_projector_gate_2026.py` | 0 | 6 tests |
| `python3 qwen_claude_field_theory/closure_2026/nonlocal_door/ricci_polynomial_projector_gate_2026.py` | 0 | 5/5 checks; explicit Ricci-polynomial realization fails anisotropic/Ostrogradsky gate |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2026/test_cde_l4c_cuscuton_legendre_audit_2026.py` | 0 | 7 tests |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2026/cde_l4c_cuscuton_legendre_audit_2026.py` | 0 | 8/8 checks; old full-action DOF certificate refuted, architecture remains open |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2026/cde_l4c_structural_gate.py` | 0 | Corrected structural diagnostics reproduced; full DOF certificate explicitly open |
| `python3 qwen_claude_field_theory/closure_2026/cde_l4c_2026/gateA/cde_l4c_covariant_dirac_rank.py` | 0 | Generic truncated rank 4, derived rank-2 cancellation surface, non-closed momentum brackets |
| `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.1.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/nonlocal_door/metric_projector_rank_change_audit_manifest_2026.json` | 0 | Valid computation manifest |
| `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.1.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/cde_l4c_2026/cde_l4c_certificate_correction_manifest_2026.json` | 0 | Valid computation manifest |

### TDD and audit-hardening failures retained

| Exact command and state | Status | Reason |
|---|---:|---|
| `python3 test_metric_only_elliptic_projector_gate_2026.py` before the smooth-vector branch | 1 | Expected red: counterexample result absent |
| `python3 metric_only_elliptic_projector_gate_2026.py` after adding the branch | 1 | Expected red: report referenced a not-yet-bound result |
| `python3 test_metric_only_elliptic_projector_gate_2026.py` before the covariant FLRW correction | 1 | Expected red: homogeneous connection-term result absent |
| `python3 test_metric_only_elliptic_projector_gate_2026.py` before the momentum-projector guard | 1 | Expected red: contraction result absent |
| `python3 test_metric_only_elliptic_projector_gate_2026.py` before provenance fields | 1 | Expected red: action/provenance scope fields absent |
| `python3 test_ricci_polynomial_projector_gate_2026.py` before implementation | 1 | Expected red: module absent |
| `python3 test_ricci_polynomial_projector_gate_2026.py` after first implementation | 1 | Exact DOF expectation exposed a float instead of rational count |
| `python3 test_cde_l4c_cuscuton_legendre_audit_2026.py` before full ADM normalization | 1 | Expected red: `sqrt_gamma` result absent |
| `python3 cde_l4c_cuscuton_legendre_audit_2026.py` after extending the derivation | 1 | Expected red: report still asserted the old bounded-momentum statement |

### Fresh pre-commit verification

| Exact command | Status | Observed result |
|---|---:|---|
| each of the eight test/main commands in the table above, rerun individually on the final tree | 0 | 8/8 programs exited 0; 26 individual tests and 25 scoped main checks |
| `python3 <each gate> | diff - <its .out>` for the metric-projector, Ricci-projector, and cuscuton audit | 0 | All three observed-output artifacts exactly match fresh stdout |
| `env PYTHONPYCACHEPREFIX=/tmp/zimmerman_projector_cde_pycache python3 -m compileall -q` on the eight changed Python files | 0 | Syntax compilation passed |
| output-hash check across both new computation manifests | 0 | 16 outputs, 0 hash mismatches |
| `git diff --check` | 0 | No whitespace errors |
