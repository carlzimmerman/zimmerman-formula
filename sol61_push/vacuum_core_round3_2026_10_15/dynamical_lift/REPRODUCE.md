# Counted lift: evidence and reproduction

The lift's authoritative successful run is `run_v2/manifest.json`, using
`check_lift_v2.py` and `contract_v2.json`. It records 25 exact symbolic checks and
2 deterministic 55-digit quadrature cases of the exact KKT energy decomposition.
The cases retain positive actual density and the same finite inventory by a
5 percent convex mixture with a Plummer density of scale equal to the original
edge. Both measured energy differences are positive; each decomposition has
absolute residual about 7.97e-59 against the declared 1e-40 threshold. These are
implementation controls; the analytic supporting-plane proof carries the
universal angular/support quantifiers.

The preserved `run_v1` is a failed symbolic check, with its original
`check_lift.py` and contract unchanged. SymPy left
sqrt(1+4s(s+1)) unsimplified despite s>0. The v2 script adds the exact radicand
identity 1+4s(s+1)=(2s+1)^2 and explicitly checks that 2s+1 is positive before
using this positive root. It changes neither the constitutive function nor any
profile, parameter or physical condition. Both run manifests validate with
their respective failed/completed statuses.

To rerun, use the installed computation-audit bounded runner with a new output
directory and `contract_v2.json`, passing every `execution_artifacts` path as a
separate `--input`. Declare NEW_OUTPUT_DIRECTORY/results.json with `--result`
and use NEW_OUTPUT_DIRECTORY with `--output`. Limits:

    --timeout 45 --max-output-bytes 65536 --max-cpu-seconds 35 --max-threads 1

Child command:

    python3 sol61_push/vacuum_core_round3_2026_10_15/dynamical_lift/check_lift_v2.py NEW_OUTPUT_DIRECTORY/results.json

The installed runner is
`/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py`.
Its companion validator checks a manifest with
`--root /Users/carlzimmerman/new_physics/zimmerman-formula`.

The companion independent audit of the finite-gamma root construction uses
`check_stiff_halo_audit_v2.py`, `stiff_halo_audit_contract_v2.json` and
`stiff_halo_audit_run_v2/manifest.json`. It independently integrates the matter
profile, derives the inverse source from the full force equation, reconstructs
the entire exact source polynomial from the stored Bernstein basis coefficients,
and checks edge/Hodge and chemical-force conditions. The narrative review and
exact byte hashes are in `../stiff_halo/AUDIT.md`.

Self-review kept explicit distinctions between actual j and P_t, the gamma-zero
profile and a finite-gamma equilibrium, the mechanical vacuum convention and a
relativistic vacuum, and fixed source inputs versus derived predictions. The
stiffness energy is counted once and no extra dark EOS is inserted. No global
smooth evolution, new fit, microscopic substance or full-theory closure is
asserted by these recorded runs.

The initial stiff-halo independent audit run is also preserved. It caught the
auditor's omitted factor of three in the central baryon density: differentiating
Mb~k r^3/5 gives rho_b(0)=3k/(20pi), not k/(20pi). The root proof and certificate
were correct. The original audit draft is preserved byte-for-byte in
`inputs/STIFF_HALO_AUDIT_DRAFT.md`; the current `../stiff_halo/AUDIT.md` corrects
that transcription and points to the v2 checker. As a result, the old audit-run
v1 manifest has an intentionally changed audit-text input at its original
path; its recorded historical hash matches the preserved draft. It is not
authoritative successful evidence. The v2 run pins the corrected current audit
and must validate normally.
