# CCT018 complete-envelope data test

Read RESULT.md first, then SOURCES.md and NEXT.md. Canonical outputs are fit_002, core_001, core_fraction_001, response_002 and hst_002. The registered contracts state all limitations. Each raw producer records input hashes; the bounded runner adds exact execution revision/status/environment and result pins. No source masses are renormalized and no frozen prior criterion was changed.

For independent controls (repository root):

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /usr/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/test_physics.py
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /usr/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/test_likelihood_v2.py
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /usr/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/test_response.py

For a new bounded repeat, select a NEW output tag. This reads the same pinned canonical inputs; it does not automatically substitute a freshly repeated upstream fit into downstream tests:

    PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/run_registered.py fit fresh_fit_003
    PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/run_registered.py core fresh_core_002
    PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/run_registered.py fraction fresh_fraction_002
    PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/run_registered.py response fresh_response_003
    PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/run_registered.py hst fresh_hst_003
    PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 sol61_push/cold_full_envelope_data_2026_10_25/run_registered.py verify fresh_verify_002

Each supplied tag must not exist; canonical outputs are never overwritten. run_registered is a convenience CLI for these authored scripts, not an automation or an interpreter for commands from evidence records. It uses the installed computation-audit runner. One numerical thread, measured memory guard below750MB, all experiments below1GB. These are measured RSS/headroom checks; no unsupported hard macOS memory cap is claimed. See verification_001/result.json for observed maximum.

plot.py regenerates envelope_data.png from the canonical data, actual-position binned velocities and full CCT profiles. Error bars are conditional Gaussian bin profile intervals, not membership/foreground-marginalized uncertainties. The figure was visually inspected. Gray mass panels mark90% spectral coverage, not a sharp physical boundary.

History:fit_001 preserves the initially incorrect component-window mixture normalization and is SUPERSEDED by fit_002; REVIEW_CORRECTIONS.md documents the repair/control. response_001 and response_002 have identical physical summary numbers; the latter additionally stores all worst-star work witnesses promised by the contract. hst_001 and hst_002 have identical predictions; the latter also pins unused initial-profile dependencies traversed by the helper import path. Neither a completed manifest nor a finite evidence count is a theory-completion certificate.
