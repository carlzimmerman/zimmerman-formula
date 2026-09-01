# One-shot commands and observed status

| Command | Exit status | Purpose |
|---|---:|---|
| `python3 sf60_rotated_mmg_complete_field_theory_master.py` | 0 | Reproduced the older claimed MMG synthesis |
| `python3 sf61_honest_canonical_adm_closure.py` | 0 | Reproduced the DBI-clock and FLRW over-constraint diagnosis |
| `python3 sf62_lapse_curvature_trilemma_proof.py` | 0 | Reproduced the no-slip/FLRW trilemma |
| `python3 wf4_skeptic1_alpha1_anchor_lens.py` | 0 | Reproduced the AeST preferred-frame anchor |
| `python3 test_curvature_qumond_action_gate_2026.py` | 0 | Ran two Candidate B regressions |
| `python3 curvature_qumond_action_gate_2026.py` | 0 | Ran Candidate B variation and falsification gate |
| `python3 test_curvature_qumond_adm_dirac_gate_2026.py` | 0 | Ran five ADM/Dirac regressions, including restored-gauge scalar and vector/static checks |
| `python3 curvature_qumond_adm_dirac_gate_2026.py` | 0 | Ran the action-derived ADM Hessian, exact finite-`k` constraint matrix/closure, separate `k=0`/`y=0`, tensor/vector, spherical, and BTFR report (8/8 checks) |
| `python3 test_curvature_qumond_action_gate_2026.py` | 0 | Fresh final Candidate B regression pass (2 tests) |
| `python3 test_elliptic_phantom_action_gate_2026.py` | 0 | Fresh Candidate A regression pass (2 tests) |
| `python3 test_{spin2,field_dependent_spin2,tensor_nonlocal_localization,ctp_auxiliary_dirac,ctp_matching_multiplier_no_go}_gate_2026.py` | 0 | Fresh nonlocal-gate regression pass (12 tests total) |
| `python3 curvature_qumond_action_gate_2026.py` | 0 | Fresh full Candidate B symbolic/numerical report |
| `python3 elliptic_phantom_action_gate_2026.py` | 0 | Fresh full Candidate A symbolic/numerical report |
| `python3 {spin2_no_slip_linearity,field_dependent_spin2_bianchi,tensor_nonlocal_localization,ctp_auxiliary_dirac,ctp_matching_multiplier_no_go}_gate_2026.py` | 0 | Fresh full nonlocal-gate reports |
| `python3 qwen_claude_field_theory/closure_2026/sf62_lapse_curvature_trilemma_proof.py` | 0 | Fresh existing no-slip/FLRW trilemma check |
| `python3 sf{13a_shift_redefinition,13b_quasistatic_reduction,13c_normalisations,13d_sign_chain,13e_the_function,18_step4_structure,19_the_bracket,21_weak_zero_test,22_finishing,23_lattice_artifact}_2026.py` | 0 | Fresh rerun of all ten khronon-split bimetric construction/constraint files; they retain the conditional `7=2+5` target mismatch |

The brace notation records the individually executed commands named in each
grouped row; it is not itself a shell command.

The final verification rerun and manifest-validation commands are appended only
after they have actually been executed; this file is an observed-command
ledger, not a proposed checklist.
