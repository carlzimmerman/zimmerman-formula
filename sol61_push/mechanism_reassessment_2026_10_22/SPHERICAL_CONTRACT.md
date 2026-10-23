# Finite-stiffness spherical background, pre-computation

Solve the previously derived weak-field fixed-baryon stationary equation, not the full ADM/cold system. Set s=r/R, q=K P/a0, epsilon²=gamma/(K R²), and Plummer gN/a0=A s/(1+s²)^(3/2). Then

 epsilon²(q''+2q'/s-2q/s²)=q²/(1-q)-A s/(1+s²)^(3/2).

Take A=1, epsilon=0.03,0.1,0.3; domain [1e-5,100]. Impose regular inner q'=q/s and outer q'=-q/s (leading isolated asymptotic). Compare tolerance 1e-6 and 2e-8, and outer endpoint 200. Require converged solver, 0<q<1, max profile change below 1e-4, independently evaluated differential residual below 1e-4 on common interior samples. Report actual values even on failure. Retain domain and boundary errors separately. Mutation removes radial vector curvature -2q/s² and must fail the original-equation residual. No guarantee of relativistic background validity or dynamical settling.

Near a smooth baryonic centre gN/a0~A s, the algebraic limit q~sqrt(A s) is not a smooth vector at the origin. Balancing its gradient correction with the source predicts a transition scaling s_core~epsilon^(4/5) A^(-1/5), up to a coefficient; test regularity numerically, not a universal fitted core law.
