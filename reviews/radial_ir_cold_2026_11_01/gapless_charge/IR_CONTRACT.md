# Logarithmic gauge threshold, anomaly and charge-response contract

Frozen before execution. Inputs are the immutable TP03 full model, the frozen
one-loop gaugino implementation and completed run_003. Compute scalar/Weyl
Dynkin weights by rotating actual raw generators into mass bases. The physical
massive vector weight is −7 T_X/2 (Goldstone already included); physical real
scalars contribute T/6 and Weyl fermions2T/3. DR matching has only mass logs:
the MS vector constant cancels the MS-to-DR conversion difference. Assert the
sum of heavy weights is (4,1,−5), and raw R-anomaly traces are5 for each
embedded subgroup. Use couplings at the TP03 fixed Q0²=e(1+z0²)/31.

Evaluate e=.01,.03,.0001 at z0. Run below heavy thresholds with b=−3C,
decouple the radiative gaugino at its leading mass, and define the formal
one-loop pure-YM scale below it using b=−11C/3. Output log10(Lambda/mu), never
exponentiate underflowing numbers. This is a leading matched scale, not a
calculated confinement gap/prefactor or high-precision scale prediction.
Higher-loop running produces logarithmic corrections to the large exponent.

Compute the residual-U1 rolling-phase dispersion from the unambiguous K1=5
Wess-Zumino coefficient; test its extremum against direct numerical maximization
and finite conductivity quadratic equation. No thermal sphaleron expression
is evaluated at T=0. Thermal drift is only a conditional linear-response
formula in the pure-YM window Lambda≪T≪m_lambda, with unknown dimensionless
diffusion coefficient. No cosmological patch, plasma or seed is selected.

One thread,120s wall,110s CPU, expected below1GB RSS. No new scans over
theory parameters or nonperturbative simulations.
