# Independently frozen FGF041 packet, residual and defect derivation

Derived before new author/root proofs or previews. Proof-only, one analytic packet and one amplitude control, no numerical scan. Retain one fixed-reference Q crossing on I=(-d,d), fixed positive physical C,tau,sigma,J,cs²,S0 and field walls. Backgrounds n=rho, j=0, phi0,chi0 solve the actual static equations. The packet stays strictly within a compact regular-side segment of (0,d).

## Packet and geometry

Set v=1/sqrt(tau), the actual diagnostic potential wave speed. Choose x_star,T>0 such that X(t)=x_star+vt, 0<=t<=T, stays a positive distance from both the crossing and right wall. Fix physical length L>0, potential amplitude P0>0, and one nonzero smooth f compactly supported in (-1,1). For dimensionless epsilon small enough that L epsilon is below the support margin, put

 psi_epsilon=P0 sqrt(epsilon) f((x-X(t))/(L epsilon)),
 h=partial_x psi=P0/(L sqrt(epsilon)) f'((x-X)/(L epsilon)),
 phi=phi0+psi, phi_t=-v h,
 n=rho, j=0, chi=chi0, chi_t=0.

The perturbation is zero near both physical walls throughout the slab. Density, mass and scale are EXACTLY fixed. At each time int h²=K_h=P0² int f'²/L>0, int abs(h)=O(sqrt(epsilon)), and ||psi||infinity=O(sqrt(epsilon)). The packet's space/time derivatives have bounded L2 norms but do not tend strongly to zero. tau psi_tt=psi_xx follows exactly from tau v²=1; this choice does not import any physical photon/light speed.

## Exact Q high-gradient controls

For signed G, B(G,a)=sgn(G)b(abs(G),a), and s=abs(G):

 abs(B-G)<=a/2,
 abs(W(s,a)-s²/2)<=a s/2,
 H(s,a)=s b-W satisfies 0<=H<=s²/2 and
 abs(H-s²/2)<=a s/2,
 T_s=q=a b/(2b+a)<=a/2.

The W bounds follow directly from s-a/2<=b<=s. The upper H bound follows by integrating H_s=s A<=s; the lower quadratic bound follows from b>=s-a/2 and W<=s²/2. Thus T(abs(G),a) is globally Lipschitz in signed G with constant a/2. All a bounds are uniform on the fixed compact background; no deep-MOND expansion is applied to the large new gradient.

Let g0=phi0', B0=B(g0,a), and define exact source-flux error

 D_epsilon=B(g0+h,a)-B0-h.

It vanishes off the moving packet strip and abs(D_epsilon)<=a_max, hence ||D||_1=O(epsilon), ||D||_2=O(sqrt(epsilon)), uniformly in time. Source flux equals B0+h+D. It converges to B0 weakly in L2 and strongly in every Lp, p<2. psi converges uniformly to zero, and its derivatives weakly in L2; the weak convergence follows from bounded norms and the shrinking strip against L2 tests.

## Every actual equation residual

Use residual signs consistent with the original equations:

 R_mass=n_t+j_x=0,
 R_phi=tau phi_tt-B_x+C n=-partial_x D_epsilon,
 R_chi=sigma chi_tt-J chi_xx+U'-T= T(g0,a)-T(g0+h,a),
 R_matter=j_t+(j²/n+cs²n)_x+n phi_x=rho h.

Thus uniformly for time in [0,T], R_phi is O(sqrt(epsilon)) in spatial H^-1 (tested against H1_0), and O(epsilon) in the dual norm of W1,infinity test functions. R_chi and R_matter are O(sqrt(epsilon)) in spatial L1, hence also in spacetime L1 on this fixed slab. They are not asserted to vanish in L2; bounded L2 residuals can retain concentration. All these are residual statements for actual equations, not an assertion that the packet solves them exactly.

For the combined momentum, let P and Pi be the full quantities from FGF040. The background has P0=0 and Pi0 spatially constant. With

 E_H=H(abs(g0+h),a)-H(abs(g0),a)
                        -[(g0+h)²-g0²]/2,

one has ||E_H||_1=O(sqrt(epsilon)) uniformly in time and exactly

 P-P0=(tau v/C)(h²+g0 h),
 Pi-Pi0=(h²+g0 h+E_H)/C.

Since h_t=-v h_x and tau v²=1,

 R_combined=partial_t P+partial_x Pi
          =[g0' h+partial_x E_H]/C.

The regular-side g0' is bounded on the packet support. Hence R_combined is O(sqrt(epsilon)) in the spatial dual W1,infinity norm uniformly in time, and in the corresponding compact spacetime C1 test norm. This calculation keeps every background matter/scale stress; only their exact equilibrium residual is zero. It does not multiply vanishing weak residuals by a diverging derivative.

## Measure limits of momentum, stress and energy

For each continuous test, changing x=X(t)+L epsilon y gives

 h² dx -> K_h delta_X(t),
 h² dx dt -> K_h delta_(x=X(t)) dt.

The convergence is weak as finite Radon measures, uniformly in time against a uniformly continuous test family. Cross terms g0 h are L1-small. Consequently

 P -> P0 dx + (sqrt(tau)K_h/C)delta_X(t),
 Pi -> Pi0 dx + (K_h/C)delta_X(t).

The extra stress equals v times the extra momentum, so its moving measure satisfies the interior transport conservation identity; X'=v. The nonlinear currents are NOT the currents evaluated at the weakly limiting fields, which are just the background. In particular there is no ordinary weak-L1 compactness for the concentrated quadratic terms: their mass stays nonzero on shrinking sets.

Let the exact total energy density include fluid kinetic/internal/interaction and both field kinetic/gradient/potential pieces. Only the potential packet changes. Its density difference is

 E_epsilon-E0= rho psi +(1/C)[tau phi_t²/2
                  +W(abs(g0+h),a)-W(abs(g0),a)]
            =h²/C + g0 h/C + E_W/C +rho psi,
 E_W=W(abs(g0+h),a)-W(abs(g0),a)
                       -[(g0+h)²-g0²]/2.

The exact Q bound gives ||E_W||_1=O(sqrt(epsilon)); rho psi is O(epsilon^(3/2)) in L1. Hence total energy measures converge to E0 dx+(K_h/C)delta_X(t). One half of this defect comes from potential field kinetic energy and one half from Q gradient energy. No density/internal/scale energy defect is hidden.

For completeness, the full energy flux on this ansatz is -phi_t B/C (fluid velocity and chi_t vanish). It equals v h²/C plus L1 errors O(sqrt(epsilon)), so its defect is v K_h delta_X(t)/C. Thus the total energy residual also tends to zero on compact spacetime C1 tests by cancellation of the leading transported measure. No exact finite-epsilon energy conservation is asserted.

At t=0 the same positive energy defect K_h/C is ALREADY PRESENT, and initial combined momentum has defect sqrt(tau)K_h/C. The field values tend uniformly to their background values and field velocities/gradients only weakly, not strongly, in L2. This is not creation from zero initial energy, not strong energy-norm initial convergence, and not a counterexample to exact solutions or uniqueness. Tests that incorporate initial energy/momentum must retain these initial defect measures rather than substitute background initial currents.

## Explicit vanishing-energy control and sufficient compactness

Multiply the same packet amplitude by epsilon^(1/4), changing P0 sqrt(epsilon) to P0 epsilon^(3/4). Then int h_control²=K_h epsilon^(1/2)->0, with the same speed/path/support and exact tau psi_tt=psi_xx. The derivative amplitude still grows like epsilon^(-1/4), but its energy disappears. All momentum/stress/energy differences now tend strongly to zero in L1, and every residual estimate still vanishes. This is one fixed amplitude control, not an exponent scan.

For the present fixed-density/fixed-scale ansatz, strong L2 convergence of phi_x and phi_t is sufficient to identify every nonlinear momentum and energy term: products and squares converge in L1, B is 1-Lipschitz in the signed gradient, and W and H have derivative bounds linear in abs(g). The interaction converges by uniform/L2 potential convergence and bounded fixed rho. Alternatively, convergence in measure plus uniform integrability of the quadratic products identifies their L1 limits: split into a small exceptional set and its complement, use uniform integrability on the former and uniform small differences on the latter. The packet violates precisely uniform integrability of its quadratic energy/current pieces.

If matter or scale are allowed to vary, corresponding convergence is additionally needed for their actual kinetic densities j²/n, pressure n, scale derivative/time products, U and scale-dependent constitutive factors; the fixed-ansatz argument does not prove those general conditions. No PDE estimate supplying the required strong compactness or defect-free approximation class is established.

## Exact scope

This sequence consists of admissible bounded-energy approximants with weakly vanishing residuals in the DECLARED weak spaces. The defect disproves the particular implication that these bounds/residuals alone identify all nonlinear currents under weak field convergence. It is not a sequence of exact solutions and not a criticism of every approximation scheme. The limiting background itself remains a solution; the nonzero residual limit is not the mechanism, the nonlinear measure defect is.

Both positive a0 hypotheses and distinct vacuum/frozen-H/evolving-H interpretations remain. All Q source calculations use signed B and the actual positive potential inertia tau. No RAR/M, photon/light-speed, physical metric/DOF, reservoir, calibration or theory closure is claimed. Fixed reference and fixed walls are essential declared premises; no numerical astrophysical size or historical novelty claim is made.
