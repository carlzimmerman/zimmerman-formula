# Review correction: slopes and interference-safe inclusive collision bound

The original run_four_fermion is preserved unchanged. Its individual
graph-class bounds are valid, but summing their rates does not, by itself,
bound interference when classes have the same final state. Its phrase
summed upper bound is therefore superseded by this correction and
run_four_fermion_v2. The separate phase-radiation bound already used
Cauchy--Schwarz correctly.

Use the same five cross-section envelopes from FOUR_FERMION_COLLISIONS.md.
A uniform inclusive upper bound, allowing all of them to overlap, is

    sigma_v_inclusive <= (sum_i sqrt(sigma_v_i_bound))².

Equivalently the local rate is bounded by the square of the sum of square
roots of the class rates. This is conservative even for orthogonal final
states. The earlier sum remains an informative arithmetic diagnostic and
is not used as the final upper bound. No class is subtracted or double
counted destructively.

The earlier radial/gaugino argument invoked |kappa_i|<1 but the current
e=.003 slopes of SU3 and SU2 were not yet pinned; values from nearby
couplings/vacua were insufficient provenance. The v2 runner now computes
all three finite-F mass slopes directly at the same declared reference
vacuum X=z0/sqrt(31e), with two independent five-point log-field stencils
h=.001,.0005. It records actual thresholds and checks |kappa_i|<1,
convergence, and the scalar/phase denominator hierarchy. This supplies
the missing local input to the already loose100 m²/(pi a^4) envelope.

All other norm/topology inputs and scope remain those of the frozen
four-fermion proof. This is a review correction under its authorization,
not a new research lane. The v2 contract precedes execution, hashes the
additional frozen threshold/model sources, and keeps one thread,
30s wall/25s CPU and measured RSS<1GB. No earlier outputs are overwritten.
