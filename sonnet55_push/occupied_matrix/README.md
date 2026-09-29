# sonnet55_push/occupied_matrix -- CA5-GNC-R occupied finite-wavelength matrix (2026-09-28)

Target (CD26-5's named next calculation): the occupied finite-wavelength spatial/potential matrix of CA5-GNC-R after all
constraints. Scope: linear scalar sector, homogeneous occupied expanding background, inactive gate, U = Z = 0 for nonzero
modes, no ordinary matter, the ACTUAL five-field potential V = m_H^2|phi|^2/2 + m_L^2|chi + gamma s phi|^2/2 + mu^2 s^2/2,
M_P^2 = 1, V0 = 3. NOT covered: Dirac count, PPN, nonlinear inhomogeneous evolution, observational gates, the full
parameter space (300 random parameter sets and 5 long-run cases below).

## Result (all three scripts exit 0; outputs committed)
**Within the scanned window no linear instability of the occupied scalar sector was found.** That is an absence of a failure
in a sampled region, not a proof, and it does not close the theory.

- `occ01_vector_form_check.py` (5/5): the N-carrier vector form of the boxed reduced action follows from the same primitives
  check.py uses for one field (verified at N = 2).
- `occ02_finite_k_matrix.py` (5/5): 300 random parameter sets in the record's window (alpha, c2, ell, xi, masses, gamma) x
  4 occupied snapshots x 36 wavenumbers. Velocity block G positive definite and D_R > 0 at every point (min eig G 3.6e-2,
  min D_R 8.6e-5). Frozen-coefficient test, valid only at x/H^2 >= 10: no growing mode (max Re lambda/H = -1.15). The 1438
  frozen flags at x/H^2 < 10 are NOT evaluated as instabilities: the frozen approximation drops the time dependence of x there.
  Two detector controls (tachyonic psi gradient; indefinite velocity block) are flagged.
- `occ03_refined_classification.py` (6/6): exact time-dependent linear evolution (Gdot, Bdot along the background) of the full
  12-dimensional propagator for 5 cases x 3 wavenumbers (k/aH = 0.1, 1, 5), T = 24 e-folds. **0 of 15 runs exponential**
  (sustained or transient). Light-carrier cases (mu = 0.6, 0.12, 0.20) show slow polynomial growth of psi driven by an s
  perturbation (late log-slope 0.05-0.09; sigma_max up to 9.3e2 for mu = 0.12); heavy-carrier cases (mu = 2.5, 2.56) are bounded
  (sigma_max <= 32). The growth vanishes for a heavy s, consistent with a light spectator field sourcing psi. Whether that
  secular drift is physical super-horizon non-conservation or a separate-universe/gauge effect is NOT resolved.
- `../equations/eq02_vacuum_psi_mode.py`: on empty de Sitter the psi mode is healthy at every wavenumber (closed form, N > 0).

## Numerics and what I changed after failures (disclosed)
- First runs used an explicit solver on a-cubed-weighted matrices; heavy cases hung. Causes found: (i) entries ~ e^{3N}
  ruined the finite-difference derivatives; (ii) G_psipsi = MK - (MKH)^2/(M F_d) is a catastrophic cancellation (it is ~ x,
  down to 1e-12): replaced by the identical MK Delta / F_d; (iii) the system is stiff: now an implicit Radau solve with the
  exact Jacobian. The baseline result is unchanged to 4 digits (sigma_max = 80.16) across all these changes.
- My first tachyonic-mutation control was run at k = 2H and looked "bounded": the mode redshifts out of the sub-horizon
  regime before it grows (the mutated psi mode does grow x128 at k = 10H, x2e8 at k = 30H). The control now uses k = 30H.
- The growth classifier was changed twice after controls failed: (1) a transient-burst criterion added after the tachyonic
  mutation was called "polynomial" (its rate falls as the mode redshifts); (2) made per-sample after a synthetic burst
  exp(8(1-e^-t)) over a T = 24 run was diluted by a 6-unit window. The threshold (2.0 per unit t) is above the fastest
  adjacent-sample slope of the t^3 control (1.5) and was not tuned on the case tables; both changes can only flag MORE cases.
  Known-answer controls: t^2, t^3 (polynomial), exp(0.3 t) and the burst (exponential), a decaying oscillator (bounded).
- Early "growing modes" at x/H^2 ~ 1e-4 and "EXPONENTIAL" labels from a 0.15 slope threshold were artefacts of the frozen
  approximation and of a threshold a t^1.3 power law also crosses; both are superseded above.
