# Verifier report A (export of HEAD 4fa9f54e3; all runs from campaign_fresh_gravity/)

| lane | script | mode | exit | expected exit (source) | tally | equals committed .out? |
|---|---|---|---|---|---|---|
| CFG75 | CFG75_phi_acceptance.py | main | 0 | 0 (README) | checks: all pass | yes (0 diff lines) |
| CFG75 | CFG75_phi_acceptance.py | MUTATE=1 | 1 | 1 (README; H1 must fail) | checks: load-bearing failure(s); H1 FAIL | yes (0 diff) |
| CFG57 | CFG57_sluggs_hot_gas.py | main | 0 | 0 (README) | 15/15, 0 load-bearing failures | yes (ignoring "(6 s)") |
| CFG57 | CFG57_sluggs_hot_gas.py | MUTATE=1 | 1 | 1 (README; H1,H2 fail) | 12/15, 2 load-bearing failures (H1,H2) | yes |
| CFG55 helper | CFG55_h50_keyfix.py | main only (no control) | 1 | 1 (CFG55_README: C1,C3 fail by construction; H1,H2 also fail) | 6/10, 4 load-bearing failures (C1,C3,H1,H2) | yes (only diff: a header line printed by the script, absent from the committed .out) |
| CFG55 helper | CFG55_salpeter_definition_check.py | main only (no control) | 0 | 0 (script: ok) | "reproduces ... YES" | yes |
| CFG79 | CFG79_lcdm_xray_ellipticals.py | main | 1 | 1 (README: both runs exit 1, C4 fails) | 15/16, 1 load-bearing failure (C4) | yes |
| CFG79 | CFG79_lcdm_xray_ellipticals.py | MUTATE=1 | 1 | 1 (README/FROZEN) | 13/16, 3 load-bearing failures (C4,H1b,M1) | yes |
| CFG80 | CFG80_lcdm_slacs.py | main | 0 | 0 (README) | 14/14, 0 failures | yes |
| CFG80 | CFG80_lcdm_slacs.py | MUTATE=1 | 1 | 1 (README; failing set {C5,H1}) | 12/14, 2 failures (C5,H1) | yes |
| CFG81 | CFG81_lcdm_xray_groups.py | main | 0 | 0 (README) | 15/15, 0 failures | yes |
| CFG81 | CFG81_lcdm_xray_groups.py | MUTATE=1 | 1 | 1 (README; C5,H1 fail) | 14/16, 2 failures (C5,H1) | yes |

Runs: 12. Mismatches: 0. Tracebacks: 0. Timeouts: 0. Logs in rerun5/logsA/.

## Findings
- No exit-code or tally mismatch; every .out reproduces line for line (timing fields ignored). No missing files.
- No dependence on git-ignored data: CFG57 reads the tracked tables in real_research/data/cfg57_gas_sources (its raw sources are git-ignored but not read).
- CFG79: the main run exits 1 (declared in README) because of a declared control C4 that FAILS in both runs and is kept as a failure. Its exit code cannot discriminate main from MUTATE. The failure sets do differ (MUTATE adds H1b and M1), and H1c passes, so the README says the class does change.
- CFG80, CFG81: the MUTATE exit 1 is guaranteed by a construction detector (C5). The exit code carries no information about the science, as the frozen files state. CFG80's C6 passes and CFG81's H1 flips (+3.30 sigma), so both are informative for the headline.
- CFG57: the MUTATE run also shows H3 failing, but H3 is a reported check there, not load-bearing. The main run's 15/15 pass is an extrapolation artefact per the README (frozen H1/H2/H3 pass spuriously; D1 fails). The rerun reproduces this.
- CFG55 helper scripts have no committed MUTATE control. h50_keyfix exits 1 by design.
- CFG75: the MUTATE control discriminates (main passes, MUTATE fails H1).
- Caveat: CFG57 main and MUTATE ran in parallel; both outputs matched the committed ones, so there was no race effect.
