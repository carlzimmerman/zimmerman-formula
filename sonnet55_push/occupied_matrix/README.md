# sonnet55_push/occupied_matrix -- CA5-GNC-R occupied finite-wavelength matrix (2026-09-28)

Target (CD26-5's named next calculation): the occupied finite-wavelength spatial/potential matrix of CA5-GNC-R after all
constraints. Linear scalar sector, homogeneous occupied expanding background, inactive gate, U = Z = 0 for nonzero modes,
no ordinary matter, actual five-field potential V = m_H^2|phi|^2/2 + m_L^2|chi + gamma s phi|^2/2 + mu^2 s^2/2, M_P^2 = 1, V0 = 3.
NOT covered: Dirac count, PPN, nonlinear inhomogeneous evolution, observational gates. **No verdict on the candidate yet.**

## Established (committed scripts)
- `occ01_vector_form_check.py` (output committed): the N-carrier VECTOR form of the boxed reduced action -- J, F_d, the
  lapse-eliminated L_red -- follows from the same primitives check.py uses for one field (5/5 exact identities, N = 2).
  Before this, check.py only verified one carrier field.
- Detector controls (occ02 run of 2026-09-28): a tachyonic psi gradient and an indefinite velocity matrix are both
  flagged by the frozen-coefficient detector. (My first two mutations did not create an instability; they were rebuilt.)
- `occ03` R1 (18,000 sub-horizon points, 300 random parameter sets in the record's window x 4 snapshots): velocity block
  positive definite and D_R > 0 everywhere; NO frozen growing mode at x/H^2 >= 10 (max Re lambda/H = -1.15).
  The earlier frozen "growing modes" at x/H^2 ~ 1e-4 are artefacts of the frozen approximation there (it drops the time
  dependence of x; P + bdot cancels at leading order -- see ../equations/eq02_vacuum_psi_mode.py).

## Preliminary, NOT final (scripts committed, final outputs pending)
- Exact time-dependent evolution (Gdot, Bdot along the background): on the baseline case the growth is polynomial
  (late log-slope 0.05 and falling), not exponential. The growing direction is a carrier (s) perturbation driving psi.
  An earlier "EXPONENTIAL" label came from a threshold that also flags t^1.3 growth; occ03's two-window classifier
  replaces it and passes its known-answer controls (t^2, exp(0.3 t), decaying oscillator).
- Not yet resolved: whether the secular psi drift is a physical super-horizon non-conservation or a separate-universe
  effect; heavy-s and random-parameter cases; some random cases are stiff and are recorded as TIMEOUT, not classified.
- occ02/occ03 were re-running when this was committed; their .out files are deliberately NOT committed until a complete run exists.
