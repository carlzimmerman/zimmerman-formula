# Self-review and verification

Primary bounded runs: AQUAL and selective coupling completed; deliberate schema mutation failed as intended. All three v2 manifests validate against current input and result hashes. Normal controls cover error semantics, source derivatives, PSD correlation extremizer, coherent cancellation, interval feasibility, minimal repair brackets and hydrostatic witness consistency. The primary reproduces all previous central AQUAL source masses. The selective calculation checks an independent acceleration-form expression and its baryonic derivative.

Independent verify.py:
- Enumerated 26,880 endpoint corners across both couplings, both footings, all clusters/shells and t=1/2/3. Maximum discrepancy from the analytic rectangular extrema was 8.84e-14 relative (recorded exact value in verification.json).
- Used scipy HiGHS linear programming, independent of the production greedy method, for 98 feasibility checks immediately above/below the minimum-width boundaries. All agree.
- Symbolically verified the derived AQUAL source-positivity slope identity.

Scientific audit:
- The actual joint posterior was not obtained. Neither normality nor a chosen correlation matrix was presented as observed data. The reported width ratios are not significance levels.
- A marginal box includes all correlations inside its coordinate limits but is not a joint confidence region.
- Component error semantics differ. The mutation intentionally swaps the stellar bound for a width and is caught before any shell result.
- Full-box repair is an optimistic feasibility relaxation; the hydro-only witness additionally verifies physical monotonicity of H. Neither witness is a forward dynamical prediction.
- Differences between released mass models represent reconstruction sensitivity, not independent statistical confirmation or posterior weighting.
- The old AQUAL inversion and new CCT selective coupling remain distinct. Native hold caps are not asserted for the CCT wave.
- The wave stress estimate concerns smooth gradients on the cluster radius. It does not bound excited modes, nodes or velocity dispersion. The coherent self-gravity length is a scaling estimate, not an exact ground-state radius.
- Fixed-eta wave scaling holds in the isolated self-gravitating limit; baryons break that exact scaling. Norm conservation still requires supply/initial data. No general microscopic no-go is claimed.

The canonical primary sensitivity plot was visually inspected for legible labels and explicit non-confidence-interval labeling. No new cold-physics parameters were fitted. Original goal remains open: full observational covariance and a predictive state-selection dynamics are both missing, for different reasons.
