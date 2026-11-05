# Exact planar reduction and constrained evolution

Use clock-adapted time tau=t, with

 ds^2=-N^2dt^2+e^(2A)(dx+w dt)^2+e^(2B)(dy^2+dz^2).

All fields depend on(t,x). The scalar field phi and physical longitudinal
polarization P are retained. External matter is absent. Define v=e^(A+2B),

 kx=(A_dot-w A_x-w_x)/N, ky=(B_dot-w B_x)/N,
 Theta=kx+2ky, u_phi=(phi_dot-w phi_x)/N,
 Dp=e^(-A)(P_x+2B_x P), acceleration=e^(-A)N_x/N,
 R3=e^(-2A)(-4B_xx-6B_x^2+4A_x B_x).

Here kx,ky are extrinsic-curvature eigenvalues, not wave numbers. The action
per unit transverse coordinate area is exactly

 L=N v { M^2[R3/2-2kx ky-ky^2]+u_phi^2/2
          -e^(-2A)phi_x^2/2-V+P e^(-A)N_x/N-W
          -gamma Dp^2/2
          +M^2[-lambda(Theta-Theta_star)+U(lambda)] },
 U=T sqrt(lambda^2+b^2 T^2)-b T^2.

This is the full stated action in this symmetry sector, not a PN truncation.
The orthogonality multiplier is eliminated by using spatial P. The lapse and
shift are varied before choosing zero shift. The clock equation follows from
the diffeomorphism identity when the remaining equations and constraints hold;
fixing tau as a coordinate is not permission to omit the lapse constraint.

Canonical momentum densities are

 pi_A=M^2 v(-2ky-lambda),
 pi_B=M^2 v[-2(kx+ky)-2lambda], pi_phi=v u_phi.

Let rA=pi_A/(M^2 v),rB=pi_B/(M^2 v). Then

 ky=-(rA+lambda)/2, kx=(rA-rB-lambda)/2,
 Theta=-(rA+rB+3lambda)/2,
 (3lambda+rA+rB+2Theta_star)/2
       +T lambda/sqrt(lambda^2+b^2 T^2)=0.

The last equation has derivative at least3/2 and a unique finite solution
for finite canonical data. Its small denominator is not itself a branch
ambiguity. The cap can nevertheless drive lambda large if momenta/volume grow.
For the uncapped control, lambda=U=0.

After integrating the polarization/lapse coupling by parts periodically, the
Hamiltonian is integral[N Hdens+w Cmom], where

 Hdens=v { M^2[-2kx ky-ky^2-lambda Theta_star-U-R3/2]
             +pi_phi^2/(2v^2)+e^(-2A)phi_x^2/2+V+W
             +gamma Dp^2/2+Dp },
 Cmom=pi_A A_x+pi_B B_x+pi_phi phi_x-(pi_A)_x.

The auxiliary lambda derivative of Hdens vanishes on its equation. Hence it
may be held fixed when taking first Hamiltonian derivatives (envelope identity),
but its actual solution is recomputed at each state. Polarization stationarity
is equivalently

 (1+gamma Dp) e^(-A)N_x/N=W_P-gamma e^(-A)(Dp)_x.

The factor1+gamma Dp is a genuine potential degeneracy of this coupled system.
It and the independent polarization domain|K P|<a must be monitored. The cap
only controls Theta-Theta_star, not either of these quantities.

## Periodic global constraint and normalization

N is normalized by mean(N)=1 to fix the remaining global clock parametrization.
Do not set N=1 locally. Solve the nonconstant parts of Hdens=0 for the odd P
profile. The remaining constant E=mean(Hdens) is the global Hamiltonian
constraint. The even lapse is the normalized left null vector of the
polarization constraint Jacobian. Then polarization stationarity holds.
The reduced Hamiltonian is2pi*E; initial E=0 is preserved by the exact reduced
Hamiltonian evolution. Numerical E drift is monitored, not projected away.

This can be verified without appealing to continuum chain rules. In a finite
odd-node reflection-symmetric discretization, write P=S p (sine basis),
G_j=2 mean(cos(jx) Hdens), h0=mean(Hdens), J=partial G/partial p.
Solve G=0 and set the lapse cosine coefficients to

 n=-2 J^(-T) grad_p h0, N=1+sum_j n_j cos(jx).

Then grad_p mean(N Hdens)=0 and differentiating the reduced h0 gives exactly
the canonical Hamiltonian derivatives at fixed N,P,lambda. This is why
constraint solving at every step does not arbitrarily reset the energy.
The lapse must stay positive; otherwise this clock chart/branch fails.

Zero shift is used for evolution. Momentum-constraint conservation is a
continuum consequence of the spatial diffeomorphism identity. Collocation
breaks its exact continuum product rules, so its residual and refinement are
essential checks, not optional diagnostics.

The initial homogeneous metric/scalar, constant pi_A, varying pi_B and solved
positive pi_phi obey Cmom=0 and Hdens=0 with P=0,N=1. They describe actual
inhomogeneous expansion and shear, not a coordinate relabeling of Bianchi I.
This collapse test may involve physical spacetime curvature as well as the
clock foliation. It is not the old geodesic-clock fold on a fixed regular FRW
metric; comparison with the uncapped theory uses separately constrained data.
