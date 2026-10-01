# FGF043 independently frozen residual and local-energy audit

No new author/root proof or preview read. This changes the already-known static velocity concentration into an audit of actual coupled residuals, local energy balance and traces. Proof-only, no scan. Work on a fixed finite interval I and finite slab [0,T] with the reviewed fixed-reference Q equilibrium rho,phi0,chi0. Keep C,tau,sigma,J,u=cs² and all physical units fixed. Choose x* on one regular side, L>0 fixed physical length, v0>0 physical velocity, and nonnegative nonzero smooth f compactly supported in (-1,1). For N sufficiently large, support is strictly interior away from crossing and walls.

## Same recorded family; no new moment-example claim

 n_N=rho, phi_N=phi0, chi_N=chi0,
 field velocities=0,
 v_N(x)=v0 N f(N³(x-x*)/L), j_N=rho v_N,

all time-independent. Full equilibrium density and scale caps are retained exactly. Let F_k=integral f^k and rho*=rho(x*). For k=1,2,3, direct fixed-profile substitution yields

 integral rho v_N^k dx=v0^k L N^(k-3)
                 integral rho(x*+L y/N³) f(y)^k dy.

Thus ||j_N||1=O(N^-2), integral rho v_N²=O(N^-1), and cubic flux measure rho v_N³ dx/2 -> A_* delta_x*, where

 A_*=rho* v0³ L F_3/2>0.

This static moment fact was already frozen in FGF042. The NEW work below tests its actual equations and local energy current, rather than re-promoting that bare mismatch.

## Every actual equation residual and its declared topology

Use conservative residual signs

 R_mass=n_t+j_x,
 R_phi=tau phi_tt-B_x+C n,
 R_chi=sigma chi_tt-J chi_xx+U'-T,
 R_m=j_t+(j²/n+u n)_x+n phi_x,
 R_comb=P_t+Pi_x.

All static background relations are the actual signed Q equations; no Newtonian source or positive-gradient-only substitution is made. Since fields and density remain the equilibrium,

 R_phi=0, R_chi=0 exactly,
 R_mass=partial_x j_N,
 R_m=partial_x(rho v_N²).

The force and pressure cancel by u rho'+rho phi0'=0. Separate force is well-defined since rho and phi0' are bounded. Define a spatial test seminorm dual by taking smooth compact tests zeta with ||zeta||infinity+||zeta_x||infinity<=1 after fixed reference units. A derivative of an L1 coefficient has dual norm no greater than that coefficient's L1 norm. Thus R_mass=O(N^-2), R_m=O(N^-1), uniformly in time, in this declared weak test norm. Both vanish in spacetime distributions against fixed compact C1 tests. Additionally ||j_N||2=O(N^-1/2), so R_mass vanishes in H^-1. No H^-1-small claim is made for R_m; its flux coefficient has L2 norm O(N^(1/2)), so this family is not licensed under an undeclared stronger residual criterion.

Full P and Pi are inherited, including both field kinetic stresses, signed B g-W, Jchi_x²/2-U and matter pressure. Here

 P_N=j_N,
 Pi_N=Pi0+rho v_N²,

and equilibrium Pi0 is constant. Therefore R_comb=partial_x(rho v_N²), exactly the same residual and weak bound. These expressions follow by direct substitution into FULL currents, not multiplication of weak residual equations. No scale/matter field term is dropped. This family consequently has vanishing mass/source/scale/separate and combined momentum residuals in the named weak spaces; finite-N equations are not exact.

## Full energy and the local defect

Let e(n)=u n[log(n/rho_ref)-1], p=u n. Every full energy term except fluid kinetic energy is unchanged. Thus

 e_total,N=e_total,0+rho v_N²/2,
 Erel_N=integral rho v_N²/2=O(N^-1)>0.

It is constant in time exactly. Hence it obeys the stipulated global inequality Erel_N(t)<=Erel_N(0), indeed equality, although it is not a solution. Initial FULL excess tends to zero and energy density converges strongly L1 uniformly in time. Initial field derivatives/velocities are exactly the background/zero; fluid momentum tends to zero L1 and density-weighted kinetic velocity tends to zero L2. No hidden initial energy concentration is present.

The inherited fixed-reference local energy current is

 S=[rho v²/2+e(rho)+u rho+rho phi0]v
                     -[phi_t B+J chi_t chi_x]/C.

The field parts vanish, but all matter terms remain. Hydrostatic equilibrium supplies a constant h0=u log(rho/rho_ref)+phi0. Hence exactly

 S_N=rho v_N³/2+h0 j_N,
 R_energy=partial_t e_total,N+partial_x S_N=partial_x S_N.

The enthalpy-plus-potential piece is O(N^-2) in L1. The cubic flux converges to A_* delta_x* as finite spatial measures, and to A_* delta_x* dt on the slab. Therefore for every fixed compact smooth spacetime test zeta,

 <R_energy,N,zeta> -> -A_* integral_0^T zeta_x(t,x*)dt.

The limit is A_* delta'_x* tensor dt, nonzero. A test zeta=a(t)b(x) with nonzero integral a and b'(x*)!=0 explicitly detects it. Thus local energy residual DOES NOT vanish, despite all the earlier declared weak equation residuals and the small constant global full energy. Each finite-N flux and residual is classically defined on its smooth support and integrable/distributional elsewhere; this is failure of local balance, not undefined flux.

The defect derivative has either sign on nonnegative tests: choose b>=0 supported near x* with b'(x*) positive or negative. Consequently it cannot meet either sign-definite local dissipative inequality in the limit. Requiring actual local energy residual to vanish against every compact spacetime test, or an appropriate one-sided local energy inequality with controlled errors, excludes this family. A scalar global energy inequality tests too little: the derivative integrates to zero spatially, so it is compatible with the global budget and cannot imply local balance. Do not infer energy creation, exact-solution instability, or failure of a stronger scheme.

## Walls and initial traces

Velocity and j vanish in neighborhoods of both walls for every N; fixed field walls and field velocities are unchanged. Thus mass/energy boundary fluxes are exactly zero. Momentum traction is the equilibrium Pi0, not zero by declaration; its two endpoint values agree for this actual static background. Perturbation traction is zero at both walls. Static time dependence supplies ordinary initial traces for each member. On tests reaching t=0, actual energy trace tends strongly L1 to the background, so there is no initial defect that cancels A_* delta'_x*. The same holds for the vanishing initial momentum perturbation. The local residual survives already on interior-time tests and cannot be blamed on wall/initial traces.

## One amplitude control

Keep the same width, background and support, but multiply v_N by N^-1/2. Then v_N^ctl=v0 sqrt(N) f(N³(x-x*)/L). Kinetic energy is O(N^-2), mass-current L1 O(N^-5/2), momentum flux L1 O(N^-2), and cubic energy-flux L1 O(N^-3/2). The field residuals stay exactly zero; mass, separate/combined momentum AND local energy residuals now vanish in the declared weak test spaces. Initial/wall properties remain as above. Peak velocity still diverges, so this control isolates moment magnitude rather than imposing a cutoff. It is one fixed control, not an exponent scan or an exact-solution construction.

## Extra bounded-velocity sufficient condition in the FGF042 class

Now consider general FGF042 zero-excess states, without density caps. They already obey n->rho L1, D(n|rho)->0, integral n v²->0, ||j||1->0, Phi->phi0 uniformly, and the field products converge in L1. Impose the ADDITIONAL condition |v|<=V with one fixed finite physical V on n>0, choosing v=0 on vacuum for formulas. This is not supplied by energy and is not a physical cutoff or a change of action.

Cubic kinetic transport obeys

 integral |n v³|/2 <= V integral n v²/2 ->0.

Potential advection obeys ||j Phi||1<=||Phi||infinity||j||1->0. For enthalpy, handle the logarithm without a lower density bound. The pointwise nonnegative entropy integrand h=n log(n/rho)-n+rho gives

 |n log(n/rho)|<=h+|n-rho|,
 integral |v n log(n/rho)|<=V[D(n|rho)+||n-rho||1] ->0.

Also ||j log(rho/rho_ref)||1<=||log(rho/rho_ref)||infinity||j||1->0. Splitting log(n/rho_ref)=log(n/rho)+log(rho/rho_ref) now proves the COMPLETE enthalpy current j u log(n/rho_ref) tends strongly L1 to zero. At n=0 the expressions nlogn and jlogn are interpreted by this bounded-velocity conservative extension as0; no undefined0 times infinity is used. Huge or tiny positive densities are allowed.

Therefore under this extra velocity cap every matter energy-flux term converges strongly L1, and with the established field flux the full energy current is identified. For the uniform-in-time zero-excess setting these are uniform spatial L1 bounds, hence spacetime L1 on each fixed slab. Merely slice-wise convergence without a time bound would not by itself justify spacetime passage. This sufficient condition does not derive any actual PDE, initial/wall trace, local balance or existence theorem. It removes the identified flux concentration obstruction; a genuine approximation must still satisfy the selected local-energy residual/admissibility requirement.

## Scope

This is an exact analytic counterexample to deriving LOCAL energy balance from the listed weak mass/field/momentum residuals plus global small-energy inequality alone. The bare static moment example is inherited, not new evidence; its full residual/trace audit and nonzero local-energy derivative are the changed conclusion. Strong energy DENSITY and combined momentum/stress convergence from FGF042 survive. No exact trajectory, uniqueness, nonlinear instability, general existence or physical exclusion follows.

Both a0 normalizations are separate and actual signed MOND Q is retained. Fixed vacuum and frozen-H references are distinct from evolving-H work/reservoir accounting. Responsive scale/inertias remain added diagnostic hypotheses. No RAR/M/filtered-MONO, metric/photon/DOF, physical reservoir, calibrated observations, historical novelty or theory closure is promoted.
