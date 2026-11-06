# Momentum projection in adapted variables

The unprojected adapted run passes homogeneous/Jacobian controls but reaches
momentum residual tolerance at t=.07, before a physical domain boundary.
This distinguishes numerical constraint drift from breakdown.

Next test keeps r fixed and solves p_lambda,x=beta_x(r+C S), retaining the
mean p_lambda. This differs from projecting canonical p_beta fixed. Newton
solves the odd-grid derivative equation augmented by a mean constraint;
check the unaugmented residual and compatibility explicitly. Apply each RK
stage and complete step, with unchanged physical action and stopping bounds.
Compare n31/63 and dt refinement at a common resolved time. This is constraint
elimination, not a dissipative postfold prescription or proof of uniqueness.
