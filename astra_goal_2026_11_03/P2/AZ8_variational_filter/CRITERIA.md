# AZ8 — field-dependent filter variation

κ = ½ FITTED; not theory closed

Pre-result. Record: ls AZ1/AZ2 and KT26–28; git log filter/AZ; rg D(u)/field-dependent-filter/density-dependent-filter in KT records. AZ2 explicitly leaves coefficient variation open. Here test that missing term, not another width scan.

For J[u]=integral [u²/2 + D(u)u_x²/2-rho*u] dx on a periodic line, derive delta J/delta u=u-d_x(D u_x)+D'(u)u_x²/2-rho. The proposed shortcut is to use the conservative AZ2 equation with D(u) inserted after variation. Hypothesis: it remains both the Euler equation and mass preserving. For monotone D and positive nonuniform u these demands need not agree.

Synthetic manufactured field u=1+0.5 cos x on [0,2pi], D=0.01(1+u²), perturbation v=1+0.25 cos(2x). rho is generated from the conservative shortcut, not from data. Compute derivative of J[u+epsilon v] at epsilon=0 by central differences h=1e-5, compare to integral D' u_x² v/2 with absolute tolerance 1e-8. Known constant-D control derivative must vanish within 1e-8. Integrated true Euler source must differ from integral u by the analytic integral 0.01 integral u u_x², quadrature agreement <=1e-10. MUTATE drop the D' term in the derivative oracle; mismatch must exceed 1e-4. Both footing identities the same; no empirical data or a0 used. Output results.json predeclared.

If shortcut fails, label FAIL only for the plug-in variational claim. A separate coefficient field with its own equation, or a constrained nonlocal construction, is not excluded. Physical D function, normalization and scales are unspecified and FITTED if chosen; synthetic 0.01 and amplitudes are test coordinates. κ=1/2 FITTED. No row 12/E1 credit for a toy functional.
