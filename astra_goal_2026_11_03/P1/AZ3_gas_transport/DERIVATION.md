# AZ3 derivation and result

κ = ½ FITTED; not theory closed

**FAIL: synthetic centred-transport peak hypothesis, both footings. P1 observations NOT EVALUABLE.**

For rho_f(x)=integral K(x-y)rho(y)dy with integral K=1 and finite first moments, set z=x-y. Then integral x rho_f(x)dx = integral y rho(y)dy + M integral z K(z)dz. An even kernel has zero first moment. Its spatial smoothing cannot displace the overall source centroid. This is not a theorem about peaks: a multi-clump density can move its peaks while preserving its centroid.

For the more restricted single Gaussian source and Gaussian kernel, complete the square: convolution of widths s and l is a Gaussian of width sqrt(s²+l²) with the same centre. Its derivative is -x/(s²+l²) times the density, so its unique peak is at zero for all positive widths. Positive amplitude cannot change that location. This conclusion is independent of a0 and is therefore identical on both footings.

results.json: analytic-convolution error 5.55e-17, normalization error 4.44e-16, centroid 0. MUTATE shifts the kernel centre to 3 and obtains 3.0000000000000004, breaking the zero-shift invariant. The synthetic required peak is 3; mismatch 3, margin -3. These are dimensionless identity checks, not measured Bullet errors. No 15-key or X-COP score was run.

A radial nonlocal response may change a relaxed cluster profile, but it does not by itself explain an offset single clump. A viable continuation needs anisotropic transport, a signed response, or a dynamically carried field with initial data. TM2 already explores several time-memory choices; those are not renamed here. Source histories in TM2 are halo-simulation kinematics and provisional; they are not raw admissible input for a new causal field calculation under this goal.
