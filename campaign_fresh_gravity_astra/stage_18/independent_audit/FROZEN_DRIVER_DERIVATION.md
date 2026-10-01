# Independent FGF033 driver and Schur derivation, frozen before new proofs

Auditor /root/metric_intake. Inputs are only task FGF033 and pinned FGF023/032 parent derivations. No FGF033 author or stage18 root proof read. Fix C=4piG, tau=K/c², sigma=J/vchi² and a=a_c exp(chi+lambda). Add the single global coordinate with Ldrv=I lambda_dot²/2-V(lambda) per transverse area. I>0 has energy times time² per area units, and V energy per area. The coordinate is neither a gauge redundancy nor a local field.

## Equation, conservation and equilibrium

At fixed chi, the action derivative with respect to lambda is integral T/C, T=-aW_a. Thus

 I lambda_ddot+V'(lambda)=integral_0^d T/C dx.

The old physical matter/field balance is dE_old/dt=-[S]_0^d-lambda_dot integral T/C. Driver energy has derivative lambda_dot(I lambda_ddot+V')=lambda_dot integral T/C, so d(E_old+I lambda_dot²/2+V)/dt=-[S]_0^d. Original fixed phi,chi walls and impermeable matter set this boundary flux to zero. This is global conservation for a deliberately nonlocal mechanical coordinate, not a new local covariant driver-energy density.

At an actual static equilibrium lambda=lambda0, the inherited static Q fluid/field equations must hold with reference a_c exp(lambda0), AND V'(lambda0)=integral T0/C. For Q, T>0 where g>0, so V constant cannot support any regular static slab with a nonzero field on positive measure. No subtraction of the mean T or support term is authorized. A chosen V cannot be replaced separately for each target equilibrium; an old fixed-reference background is a candidate only if this additional condition holds.

## Full second variation in original coordinates

Use fluid displacement xi, psi=delta phi, eta=delta chi in H1_0(0,d), and l=delta lambda in R. Let r=delta rho=-(rho xi)', A=b_g, q=T_g, s=T_chi=2T-gq, m=U''-s. Fixed-mass hydrostatic balance makes e'(rho)+phi constant, so density second-order terms vanish against the mass constraint exactly as FGF023. No direct fluid-lambda term is added: material coupling is rho phi and the lambda dependence is in W.

With Q0 the inherited fixed-lambda second-variation form,

 Q0(u)=integral[cs²((rho xi)')²/rho-2(rho xi)'psi+(A psi'²-2q eta psi'+J eta'²+m eta²)/C]dx,

full Q=delta² potential=2V2 is

 Q(u,l)=integral[cs²((rho xi)')²/rho-2(rho xi)'psi
   +(A psi'²-2q(eta+l)psi'+J eta'²+U'' eta²-s(eta+l)²)/C]dx+V''(lambda0)l²
 =Q0(u)+2l ell(u)+k l²,
 ell(u)=-(1/C) integral[q psi'+s eta]dx,
 k=V''(lambda0)-(1/C) integral s dx.

The negative signs follow W_gchi=-q and W_chichi=-s. The full positive kinetic form is N=integral[rho xi_dot²+(tau psi_dot²+sigma eta_dot²)/C]dx+I l_dot². I>0 makes velocities nondegenerate but says nothing about Q. Coefficients and rho are smooth positive regular-background quantities; reference scales can be used to compare norms of different physical components.

## Exact Schur condition with fixed-lambda coercivity

Assume Q0 extends to a continuous coercive symmetric form a0 on H=H1_0(0,d)^3, with the actual inherited boundary, action and parameters unchanged. This is stronger than merely pointwise strict positivity without a gap; use the proved finite-slab estimate where applicable. Smooth bounded coefficients make ell a continuous linear functional. There is a unique z in H with a0(z,u)=ell(u) for all u. Then

 Q(u,l)=a0(u+l z,u+l z)+Delta l²,
 Delta=k-ell(z)=V''-(integral s/C)-ell(A0^-1 ell).

Hence Delta>0 iff the full form is coercive positive on H plus R, Delta=0 gives one null direction (-z,1) with no negative direction, and Delta<0 gives precisely one negative direction index relative to the positive fixed-lambda block. Under the compact finite-domain positive-inertia self-adjoint linearization, Delta<0 yields a negative generalized eigenvalue and exponential linear instability. Delta=0 is a zero-frequency/marginal quadratic mode, not a nonlinear stability theorem; initial velocity along a zero mode can drift linearly. Conservation and I>0 do not decide Delta. The inequality V''>integral s/C+ell(A0^-1 ell) is conditional at an equilibrium; it neither constructs V nor establishes its admissibility.

No static field was eliminated. If psi alone were minimized, h=C rho xi-q(eta+l) and Dirichlet compatibility integral psi'=0 would retain the positive contribution (integral h/A)^2/[C integral 1/A], alongside the other terms. Setting the completed square to zero everywhere is not the same boundary problem.

## Exact autonomous coordinate transformation and boundary subtlety

Now lambda is dynamical: theta=chi+lambda is a time-independent transformation on the EXTENDED configuration space. The exact scale kinetic term is integral sigma(theta_dot-lambda_dot)²/(2C) plus I lambda_dot²/2, spatial gradient is theta_x and potential is U(theta-lambda). Momenta obey

 pi_theta=sigma(theta_dot-lambda_dot)/C,
 P_lambda=I lambda_dot-integral pi_theta dx.

The transformed kinetic Hamiltonian is integral C pi_theta²/(2sigma) dx+(P_lambda+integral pi_theta dx)²/(2I), plus unchanged fluid/phi kinetics. It is positive and has the same rank. The total canonical Hamiltonian equals physical total energy: the field contribution lambda_dot integral pi_theta is canceled by the global momentum change. There remains exactly one added global canonical pair. No prescribed-time-coordinate energy correction can be used to hide it.

In perturbations h=delta theta=eta+l, the domain is xi,psi in H1_0 with h-l in H1_0 and l in R. In particular h(0)=h(d)=l; h cannot be forced to zero independently. The transformed Hessian is the same expression above with eta=h-l, eta+l=h and eta'=h'. Its positivity and inertia are identical under this bounded invertible domain map.

There is a further variation check when deriving the transformed global equation. Fixed original chi walls give theta_b=chi_b+lambda, so delta theta_b=delta lambda. The naive fixed-theta bulk expression for the lambda variation is incomplete: varying -J theta_x²/(2C) supplies the boundary term -J[theta_x] delta lambda/C. Thus its on-shell global equation is

 dP_lambda/dt=integral U'(theta-lambda)/C dx-V'(lambda)-J[theta_x]_0^d/C.

Together with pi_theta,t=J theta_xx/C-U'/C+T/C this yields exactly I lambda_ddot+V'=integral T/C. Dropping this linked-trace boundary term would falsely leave a J[theta_x]/C force. This equation uses original fixed walls, not independently fixed theta values. It is a bookkeeping check, not a new boundary force.

Both a0 normalizations remain separate hypotheses with lambda0 bookkeeping. Static vacuum and actual H trajectories are distinct; no trajectory or potential V is selected. The old actual-scale/vacuum incompatibility remains. This is Q diagnostic global-coordinate conservation and conditional linear stability only, not RAR or M dynamics, filtered-MONO transfer, metric/photon construction, a local covariant reservoir, nonlinear stability, observational evidence, or theory closure. No mathematical computation executed.
