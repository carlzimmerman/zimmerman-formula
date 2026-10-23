# Direct orbit folds admit a regular local coordinate change

The fifth- and sixth-harmonic turning points flagged by the stored samples persist under direct orbit integration. At both selected points the angular-momentum derivative of frequency is nonzero. Thus the apparent singularity of the energy-root formula can be removed locally by solving for angular momentum at fixed energy. This is a numerical-method advance toward the continued response, not a new physical damping mechanism.

## Direct calculation

We reconstruct the A10000, gamma=.01, unit-mass spherical equilibrium from its stored central potential using the same differential equations and tight integration tolerances. For each fixed u=L² we bracket radial turning radii and integrate the radial period after r=rp+(ra-rp)sin²(theta). Independent Gauss–Legendre orders64,128,256 evaluate the periods. A65-point energy scan brackets an interior minimum, bounded minimization refines it, and an outer root solve locates n Omega_min(u)=.8228. The chosen u brackets correspond to the earlier fifth/sixth-harmonic candidates, not an exhaustive search.

| harmonic n | u at crossing | minimum Omega | energy near minimum | partial Omega/partial u |
|---|---:|---:|---:|---:|
|5|.001071871601|.1645600000|-.02852089|-10.84331|
|6|.003386016149|.1371333333|-.02823668|-12.82441|

The u estimates change by less than1.5e-13 across quadrature orders in this test; that is agreement, not a certified absolute error. Resonance residuals are below1.9e-11. Energy curvatures are positive, approximately1.9861e4 and4.0611e4. Curvatures agree within.05% under halving the finite-difference step. The minimized energies themselves vary by several1e-9 across orders, and centered energy slopes retain finite-step error; no exact stationary-point certification is claimed.

The derivative along the minimum curve and the independently evaluated fixed-energy u derivative agree within3.06e-6 relatively. This is consistent with Omega_E=0 at a minimum and confirms that the coordinate swap is numerically well conditioned at these selected points. This cross-check uses steps .001u and .0005u, and does not establish global monotonicity in u.

## Coordinate-invariant expression and local remedy

The spectral density introduced in LITERATURE_CONTINUATION_RESULT.md can be written, for positive s, as

    W_n(s) = 2 pi² F n integral dE du C_n C_n^T delta(s-n Omega(E,u)).

Integrating over energy yields the earlier formula with 1/|Omega_E|. Integrating over u instead gives

    W_n(s) = 2 pi² F integral dE
                 sum_{u: n Omega(E,u)=s} C_n C_n^T / |Omega_u|.

The factors of n cancel in either representation. The latter formula is regular locally at the two measured energy minima because Omega_u is nonzero. Equivalently, the full gradient of the resonance function does not vanish there: an energy fold is not necessarily a singularity of the two-dimensional resonance curve. This prevents the incorrect inference that every energy turning point forces a branch singularity of the integrated spectral response.

The next response calculation can cover resonance curves with local coordinate patches: use energy roots where |Omega_E| is well conditioned and u roots near energy folds. Patches must cover each curve once; naive addition of both representations would double count. Physical support boundaries and points where both derivatives vanish still require separate treatment. Regularity of these two patches does not establish an analytic extension of the entire W(s).

## Evidence and scientific scope

direct_folds.py/direct_folds_run preserve the first direct minimum calculation. direct_folds_v2.py/direct_folds_v2_run add the fixed-energy derivative check without overwriting earlier evidence. Both executions completed; the v2 manifest validates with six passing checks. Exact argv, software versions, input/output hashes and timing are in direct_folds_v2_run/manifest.json. The only external numerical input is cold_limit_run/results.json; the script contains its own background and orbit routines. This is self-reviewed floating-point evidence on two selected crossings, not interval certification or an independent physical-model validation.

No continued matrix pole has yet been solved, and the provisional slow-decay estimate remains conditional. Formation, occupation selection, parameter derivation, full parent dynamics and novelty remain open.
