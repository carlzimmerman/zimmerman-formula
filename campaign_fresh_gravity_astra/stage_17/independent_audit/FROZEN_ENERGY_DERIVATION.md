# Independent protocol-energy derivation, before new worker/root inspection

Auditor /root/metric_intake. Derived only from task FGF032 and the original stage04 action; new FGF032 worker and root proof not read. Let C=4piG, tau=K/c² and sigma=J/vchi², all fixed physical coefficients. Let lambda(t) be a prescribed spatially uniform smooth function, and a=a_c exp[chi+lambda(t)]. The original Lagrangian density is

L=L_m-rho phi+[tau phi_t²/2-W(|grad phi|,a)+sigma chi_t²/2-J|grad chi|²/2-U(chi)]/C.

Use Bvec=W_gradphi=mu gradphi and T=-aW_a=-W_chi. For the Q branch b=F_Q^-1(g;a), F_Q=sqrt(B²+aB), so Bvec=b gradphi/g and all source work is computed with this MOND flux. The signed scalar equation is tau phi_tt-div Bvec=-C rho, while sigma chi_tt-J Delta chi+U'=T. Lambda dependence changes the parameter a, not these partial variations at fixed protocol.

For a smooth ideal barotropic fluid take internal energy density epsilon(rho), p=rho epsilon'(rho)-epsilon, continuity rho_t+div(rho v)=0 and material acceleration Dv/Dt=-grad phi-grad p/rho. Matter kinetic-plus-internal energy e0=rho|v|²/2+epsilon satisfies e0_t+div[(e0+p)v]=-rho v dot grad phi. The interaction rho phi contributes (rho phi)_t+div(rho phi v)=rho phi_t+rho v dot grad phi. Thus e_m=e0+rho phi and F_m=(e0+p+rho phi)v satisfy e_m,t+div F_m=rho phi_t. In enthalpy notation epsilon+p=rho h. The interaction is counted once, and the pressure/enthalpy flux cannot be dropped.

The field energy e_phi=[tau phi_t²/2+W]/C and F_phi=-phi_t Bvec/C obey

 e_phi,t+div F_phi=-rho phi_t-T(chi_t+lambda_dot)/C.

The scale energy e_chi=[sigma chi_t²/2+J|grad chi|²/2+U]/C and F_chi=-J chi_t grad chi/C obey

 e_chi,t+div F_chi=T chi_t/C.

Therefore the physical energy E=e_m+e_phi+e_chi and physical flux F=F_m+F_phi+F_chi satisfy

 E_t+div F=-lambda_dot T/C,
 d/dt integral_Omega E=-integral_boundary F dot n-lambda_dot integral_Omega T/C.

This is for a fixed spatial domain. A moving boundary needs the corresponding transport term. Zero material normal flux and stationary field Dirichlet traces set the physical flux to zero; arbitrary or time-dependent traces need not. Increasing lambda extracts physical energy at g>0 where Q has T>0. The external protocol source must account for the opposite work if a larger closed system is wanted.

## Time-dependent coordinate change

Define theta=chi+lambda(t). Then chi_t=theta_t-lambda_dot, grad chi=grad theta and U becomes U(theta-lambda). The EXACT transformed Lagrangian is

 L'=L_m-rho phi+[tau phi_t²/2-W(g,a_c exp theta)+sigma(theta_t-lambda_dot)²/2-J|grad theta|²/2-U(theta-lambda)]/C.

Its scale equation is sigma(theta_tt-lambda_ddot)-J Delta theta+U'(theta-lambda)=T(g,a_c exp theta), exactly the original equation in new variables. Replacing this shifted kinetic/potential action with an autonomous theta action removes terms and changes the model.

The canonical momentum density is P_theta=sigma(theta_t-lambda_dot)/C=P_chi. The transformed canonical Hamiltonian density is H'=E+lambda_dot P_theta, where E is the original physical energy expressed with theta_t-lambda_dot and U(theta-lambda). The transformed canonical energy flux is

 F'=F_m-phi_t Bvec/C-J theta_t grad theta/C
   =F-lambda_dot J grad theta/C.

The exact transformed canonical identity is

 H'_t+div F'=lambda_ddot P_theta-lambda_dot U'(theta-lambda)/C=-partial_t L'|fields,velocities.

To check: add lambda_ddot P_theta+lambda_dot P_theta,t to the physical identity, then subtract lambda_dot J Delta theta/C from the flux divergence. The scale equation P_theta,t-J Delta theta/C=(T-U')/C cancels the original -lambda_dot T/C, leaving precisely the displayed canonical source. This cancellation uses the equation of motion; the identities should not be treated as on-shell checks for arbitrary manufactured field functions.

The integrated H' relation includes the corresponding F' boundary flux. For originally fixed chi boundary data, theta_t=lambda_dot there, so the canonical scale boundary flux generally is nonzero even where the physical scale flux is zero. A time-dependent Hamiltonian is not automatically the physical energy.

Constant lambda: lambda_dot=lambda_ddot=0 gives H'=E and F'=F and conservation subject to boundary flux, but the correct potential is still U(theta-lambda). At an instant with lambda_dot=0 and lambda_ddot nonzero, physical protocol power is zero and H'=E instantaneously, yet H'_t can differ from E_t by lambda_ddot P_theta. Zero rate alone at one instant is not an autonomous protocol.

The old prescribed-H obstruction remains: this coordinate change does not supply an autonomous source equation for lambda or make the old unforced chi_H history a solution. The two a0 normalizations can be represented by separate constant offsets of lambda, with common fixed units; varying H histories remain distinct driven protocols. This is a conditional Q diagnostic calculation, not an M action, filtered-MONO transfer, metric theory, cosmological evolution mechanism or empirical result. No computation was executed.
