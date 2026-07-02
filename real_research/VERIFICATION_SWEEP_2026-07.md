# Repo Self-Verification Sweep — 2026-07-02
**Every committed `.py` under `real_research/` + `opus_48_extended_research/` executed** (timeout 120 s, MPLBACKEND=Agg, direct background run — deterministic, no agents).
| metric | count |
|---|---|
| scripts executed | **1257** |
| exit 0 | **1198** (95.3%) |
| timeout >120 s (long compute, not failure) | 28 |
| data/dependency-missing failures | 22 |
| hard failures | **9** |
| hard failures in LOAD-BEARING scripts (cited in README/papers) | **1** |
## Hard failures in load-bearing scripts (priority)
| script | last error |
|---|---|
| `real_research/reviews/lensing_rar/agentZ_second_variable.py` | `agentZ_second_variable.py: error: the following arguments are required: --stage` |

## All hard failures
| script | last error |
|---|---|
| `opus_48_extended_research/papers/zenodo_newversion_skordis.py` | `IndexError: list index out of range` |
| `opus_48_extended_research/reviews/rc_diversity_renzo.py` | `ValueError: n must be an integer not less than 1` |
| `opus_48_extended_research/reviews/unitarity_anticirc/anticircularity_crux.py` | `SyntaxError: invalid syntax` |
| `real_research/papers/zenodo_newversion_dwarf.py` | `usage: python zenodo_newversion_dwarf.py <existing_record_id>` |
| `real_research/papers/zenodo_newversion_nogo.py` | `usage: python zenodo_newversion_nogo.py <existing_record_id>` |
| `real_research/reviews/toe_law/agentHH_3d4_row.py` | `IndexError: list index out of range` |
| `real_research/reviews/toe_law/agentHH_fit_extract.py` | `IndexError: list index out of range` |
| `real_research/reviews/lensing_rar/agentZ_second_variable.py` | `agentZ_second_variable.py: error: the following arguments are required: --stage` |
| `real_research/reviews/lensing_rar/lr_esd_remeasure.py` | `lr_esd_remeasure.py: error: the following arguments are required: --stage` |

## Timeouts (>120 s — long compute, rerun individually to verify)
- `opus_48_extended_research/reviews/aest_collapse/aest_collapse_run.py`
- `opus_48_extended_research/reviews/aest_phi_cluster/aest_phi_cluster_ADVERSARIAL.py`
- `opus_48_extended_research/reviews/aest_rigorous_collapse/aest_rig_run.py`
- `opus_48_extended_research/reviews/cluster_aest_shooting_solver.py`
- `opus_48_extended_research/reviews/derivation_chain/gap2_mechanism_independence.py`
- `opus_48_extended_research/reviews/derivation_chain/gap3_conservative_kernel_dissolves_antimond.py`
- `opus_48_extended_research/reviews/koide_dsunruh/route1_minimize.py`
- `opus_48_extended_research/reviews/koide_dsunruh/route2_qcd_scheme_running.py`
- `real_research/reviews/door2_dssyk_wE_center_vs_edge_DIRECT.py`
- `real_research/reviews/door_part3.py`
- `real_research/reviews/member_MI_adversarial_check.py`
- `real_research/reviews/toe_law/agentE_solar_reflex.py`
- `real_research/reviews/toe_law/agentHH_3a1f.py`
- `real_research/reviews/toe_law/agentHH_3dK.py`
- `real_research/reviews/toe_law/agentHH_leftovers.py`
- `real_research/reviews/toe_law/agentJJ_transient_fingerprint.py`
- `real_research/reviews/toe_law/agentN5_freq_vs_accel.py`
- `real_research/reviews/toe_law/agentOO_c11_converge.py`
- `real_research/reviews/toe_law/agentOO_c1_bubble.py`
- `real_research/reviews/toe_law/agentOO_c2_analytic.py`
- `real_research/reviews/toe_law/agentOO_c3_robust.py`
- `real_research/reviews/toe_law/agentOO_c4_moments.py`
- `real_research/reviews/toe_law/agentOO_c5_forced.py`
- `real_research/reviews/toe_law/agentOO_c6_htl.py`
- `real_research/reviews/toe_law/agentOO_c7_fast.py`
- `real_research/reviews/toe_law/agentOO_c9_pv.py`
- `real_research/reviews/toe_law/agentSS_verify_p3_kstruct_edge.py`
- `real_research/reviews/toe_law/agentS_edge_qnm.py`

## Data/dependency-missing (need a local file, network, or module)
- `opus_48_extended_research/papers/build_cluster_nogo_pdf.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'CLUSTER_RESIDUAL_DENSITY_NOGO.md'`
- `opus_48_extended_research/papers/build_skordis_pdf.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'WHY_SKORDIS_AND_ZLOSNIK_WERE_RIGHT.md'`
- `opus_48_extended_research/papers/zenodo_publish_cluster_nogo.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'CLUSTER_RESIDUAL_DENSITY_NOGO.zenodo.json'`
- `opus_48_extended_research/papers/zenodo_publish_skordis.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'WHY_SKORDIS_AND_ZLOSNIK_WERE_RIGHT.zenodo.j`
- `opus_48_extended_research/reviews/btfr_slope_odr_bothways.py` — `FileNotFoundError: [Errno 2] No such file or directory: '/Users/carlzimmerman/new_physics/zimmerman-`
- `opus_48_extended_research/reviews/toe_law/agentZZ_gate.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'agentY_eqs.pkl'`
- `real_research/data/widebinaries/find_binaries_edr3.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'edr3_parallax_snr5_goodG.fits.gz'`
- `real_research/data/widebinaries/num_neighbors_edr3.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'edr3_parallax_snr5_goodG.fits.gz'`
- `real_research/papers/zenodo_publish_a0z_discriminant.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'A0Z_NONMONOTONIC_DISCRIMINANT_2026.zenodo.j`
- `real_research/papers/zenodo_publish_cluster_anisotropy.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'CLUSTER_ANISOTROPY_MI_TEST_2026.zenodo.json`
- `real_research/papers/zenodo_publish_desitter.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'DESITTER_UNRUH_A0_NOGO_2026.zenodo.json'`
- `real_research/papers/zenodo_publish_dwarf.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'DWARF_ORBITAL_HISTORY_PREDICTION_2026.zenod`
- `real_research/papers/zenodo_publish_growing_nu.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'GROWING_NEUTRINO_MASS_2026.zenodo.json'`
- `real_research/papers/zenodo_publish_growth_tomography.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'GROWING_NU_GROWTH_TOMOGRAPHY_2026.zenodo.js`
- `real_research/papers/zenodo_publish_inverted_bh.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'INVERTED_BH_DUALITY_2026.zenodo.json'`
- `real_research/papers/zenodo_publish_kappa.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'KAPPA_ONE_FREE_NUMBER_2026.zenodo.json'`
- `real_research/papers/zenodo_publish_scale_without_law.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'SCALE_WITHOUT_LAW_2026.zenodo.json'`
- `real_research/papers/zenodo_publish_stx.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'STX_PREDICTION_FOR_EPHEMERIS_TEAMS_2026.zen`
- `real_research/papers/zenodo_publish_theory.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'DSUNRUH_MI_THEORY_2026.zenodo.json'`
- `real_research/reviews/gamma_th_blind/FINAL_band_summary_FRESH.py` — `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/gamma_th_blind/cosmo_desi.py'`
- `real_research/reviews/gamma_th_blind/audit_partC_cancellation.py` — `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/gamma_th_blind/audit_eps_table.json'`
- `real_research/reviews/toe_law/agentY_gates.py` — `FileNotFoundError: [Errno 2] No such file or directory: 'agentY_eqs.pkl'`
