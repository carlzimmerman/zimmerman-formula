# PF08 exact cancellation before discretization

Gradient-coordinate constraints remove the n1023 initial Newton floor without
relaxing tolerance. At larger grids the adapted RHS still subtracts separate
second spatial derivatives of lapse and beta_t. These terms cancel in the
continuum using the momentum and uniform-lambda gauge constraints; evaluating
them separately amplifies roundoff and collocation product-rule errors.

Derive the adapted r_mom rate symbolically, substituting p_lambda,x=beta_x*p_beta
and its derivative, and w_x=lambda_t-N(p_lambda-p_beta)/(2Mpl²V3).
Verify exact vanishing of N_xx, beta_xxx, w_xx and p_lambda,xx coefficients after
substitution. Generate the algebraic RHS and compare with the original on
resolved constrained states. Only after equivalence checks may it be used for
refinement. No viscosity, filtering, tolerance relaxation or physical term
removal is authorized by this numerical change.
