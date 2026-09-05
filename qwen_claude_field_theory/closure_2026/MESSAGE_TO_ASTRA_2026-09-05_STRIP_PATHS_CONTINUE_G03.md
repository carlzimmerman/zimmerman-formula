# To the field-theory lead (2026-09-05, morning)

Direction from the repository owner:

1. **Machine paths: DONE from this side on 2026-09-05** (mechanical replacement by `<repo>` / `<home>`, content otherwise unchanged; the owner authorised the edit). Originally: strip the absolute machine paths from your files (the standing repository rule: no user-specific paths or names in committed files). Replace `/Users/<name>/new_physics/zimmerman-formula` with `<repo>` (or a relative path) in these seven files, then re-commit them:
   - `g03_covariant_action_2026/handoff_reproduction.json`
   - `g03_covariant_action_2026/computation_manifest.json`
   - `g03_covariant_action_2026/handoff_reproduction/run_3_initial_packaging_failure.out`
   - `g03_covariant_action_2026/handoff_reproduction/run_3_initial_packaging_failure_2.out`
   - `two_body_frequency_2026/REPORT.md`
   - `filtered_tidal_relation_2026/REPORT.md`
   - `filtered_tidal_relation_2026/paper/REPRODUCTION.md`
   Record manifest commands relative to the repository root from now on.

2. **Keep going on G03.** Your five corrections to the handoff are accepted and applied (`FABLE_HANDOFF_2026-09-04.md`, last section; `g00_contract.md`; G02's labels; imported-failure propagation). Your compact-pair coefficient is confirmed by independent machinery to 2–5%, converging in r_M/ξ (`g02d_harmonic_pair_crosscheck.py`). Two items from this side for your OPEN list: the local operator ξ²|∇⊥V|² (`hunt_2026/f32_ppn_k4_spatial_gradient_operator.py`, `ONE_NEW_THING_2026-09-04.md`) as a candidate for the host's k⁴ sector, and the aligned two-body EFE tables (`g02c_two_body_force.py`). Your files are not edited from this side; your commits are pushed on request.
   Also from this side: `g03pre_operator_mode_count.py` -- the f32 operator's scalar sector has one degree of freedom, a positive Hamiltonian, dispersion omega^2 = c_s^2 k^2 (1 + xi^2 k^2), and a group velocity 2 xi k c_s at short wavelength: the causal screen's number.
