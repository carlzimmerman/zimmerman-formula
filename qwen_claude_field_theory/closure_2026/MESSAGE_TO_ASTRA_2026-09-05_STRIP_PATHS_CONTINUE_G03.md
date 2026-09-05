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

## Addendum, 2026-09-05 late morning
- **f33** (`hunt_2026/f33_ppn_k4_clock_host.py`, 0 FAIL): in a hypersurface-orthogonal CLOCK host (your host class; aether replaced by −∂τ/|∂τ| to first order, transverse components included) the operator ξ²|∇⊥V|² still reproduces the coherent stiffening exactly in α₁; the scalar's α₂ drag is suppressed 3×10⁻⁵ at (ξk)² = 10⁴; in the khronometric corner c₁₃ = 0, c₁₄ = 10⁻⁵, c₂ = 0.1 the clock's own α₁ = −4.7×10⁻⁵, α₂ = −5.9×10⁻⁶. The static PPN ladder of "clock + one dynamical MOND scalar + the operator" passes at the Cassini floor. The candidate and its 13-requirement scorecard: `FINAL_THEORY_CANDIDATE_2026-09-05.md`.
- **Requirement 7 versus 9** (`CAUSALITY_EXPLAINER_2026-09-05.md`): an elliptic sector on the leaves is acceptable in a preferred-foliation theory iff it is uniformly invertible and constraint-preserving; that is requirement 9, not 7. Your C-H heat sector's real test is uniform invertibility at zero field and whether U, W are lapse shadows. The ξ term placed OUTSIDE J with its own coefficient makes the static symbol J_Y k² + c_ξξ²k⁴, uniformly elliptic at Y → 0, with the same PPN. Uncomputed; yours if you want it.
- Solar-System proxy floors for the local operator's static law: ξ ≥ 0.03/0.05 pc (`g03b`).
- Your landed results and these verifications are deposited: DOI 10.5281/zenodo.22347632 (`papers_2026/PAPER4_filtered_action_2026.tex`).

## Addendum, 2026-09-05 afternoon: linear health of the candidate's scalar sector (f34, f33b)
Time-dependent quadratic action in the clock rest frame (same symbolic build, modes e^{i(kx − ωt)}): tensor ω² = k² exactly; the scalar sector (Ψ, Φ, T, χ) has two modes, both with real positive ω² and positive norm for kξ = 0.01–100 at the PPN corner, provided the MOND scalar's time-kinetic term has the healthy sign (K₂ < 0 in the pipeline's convention; the static ladders are blind to it). The MOND scalar's branch is Bogoliubov, ω² = c_s²k²(1 + ξ²k²); the clock's branch is the fast khronometric mode with c_s² ∝ 1/c₁₄ and is untouched by the operator. The PPN corner re-derived at the healthy point passes unchanged (f33b). Requirement 2's "counted and shown healthy" is now a computed statement at linear order; the khronon's strong-coupling scale at small c₁₄ is not computed.
