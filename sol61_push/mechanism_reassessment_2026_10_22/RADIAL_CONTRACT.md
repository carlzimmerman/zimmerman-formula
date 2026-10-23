# Radial preservation calculation: pre-run contract

Checkpoint c6a0b6f3c74c623eacce284ab3765f480049aee7. The two newer commits concern separate D7b/D8b preregistrations; the audited action is unchanged. Previous turn: progress (general bracket, exact obstruction, corrected linear reduction).

Target: derive the lapse equation obtained by preserving the regular-centre spherical momentum relation. Keep both radial metric fields ell(r), R(r) until after variation; do not impose areal gauge inside the action. Normalize the angular integral out consistently. Use canonical pairs (ell,p_ell), (R,p_R), (P_r,Pi).

Checks: derive the radial Hamiltonian; independently compare its canonical lapse bracket with the spherical restriction of the previously derived full formula. At zero momenta derive dot A^r by applying Hamilton's equations, including derivatives of the momenta. Extract the highest lapse derivative. Then specialize only AFTER variation to ell=1, R=r, P=0, Lambda=0, W(0)=W'(0)=0. Recover the flat-vacuum lapse operator; prove uniqueness of a bounded regular lapse with fixed asymptotic value using its factorized elliptic equation. This is a formal flat limit, not the actual positive-Lambda cosmology.

Success means a correctly derived necessary lapse equation and an explicitly scoped regular limit. It does not mean a polarized galaxy solution or nonlinear well-posedness. If actual static galaxy backgrounds are required for further conclusions, leave those conclusions open. No parameter fitting, no new observational claim. Exact symbolic calculation, bounded runs, single-threaded numerical libraries.
