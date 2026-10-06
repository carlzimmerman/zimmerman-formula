# Generic linear clock perturbations diverge at an analytic simple kinetic zero

This result uses the exact finite-mode dust action in the parent fold-health report. It distinguishes the actual crossing problem from an instantaneous infrared kinetic sign. Assume the tuned background is analytic at a finite time t0, q>0, M>0, rho>0, Theta!=0, nonzero comoving Fourier mode, and A=Kclock has a **simple** zero: A=alpha(t-t0)+O((t-t0)^2), alpha!=0. Double zeros, the homogeneous k=0 sector and nonanalytic backgrounds are excluded.

Let d=M/Theta, e=rho/(2Theta), S=Sigma+kappa M p², T=2M p²+3rho. Use the per-volume canonical clock momentum P (the actual canonical momentum is a_FRW³ P). The exact momentum identity and equations are

`P=2A zetadot+(rho A/M)v+dT zeta-d pi`,

`nu=d zetadot+e v`,

`pidot=e[2S nu+6Theta zetadot+T zeta-pi]-rho p²v-3H pi`,

`Pdot=T nu+2M p²zeta-3H P`.

These retain all dust tadpoles, expansion and one-derivative terms. The coefficient of zetadot in pidot is rho A/M, so that equation has no pole after substituting the momentum identity. For the state y=(zeta,v,pi,P), the exact first-order system near tau=t-t0 has the form

`ydot=[N/tau+B(tau)]y`,

with B analytic and

`N=c r/(2alpha)`, `c=(1,d,0,Td)^T`, `r=(-dT,0,d,1)`,

where d,T in this residue are evaluated at t0. Direct multiplication gives r c=0, N²=0, rank N=1. No divergent coefficient was introduced by eliminating dust at this zero: its algebraic coefficient is B_dust=-3rho²/(4M)-rho p²/2<0. The lapse and shift constraints also have nonzero Theta there.

## Local solution and physical invariant

The analytic regular-singular system admits an invertible analytic matrix U(tau), U(0)=I, reducing it to z'=N z/tau. One can prove this directly by the series recurrence: at order n>=1 its operator is nI-ad_N, invertible because ad_N is nilpotent. Consequently a fundamental solution is

`y=U(tau)[I+N ln|tau|]b`.

Generic amplitudes have r b!=0. Since the zeta component of c is one, zeta then has a logarithmic term with coefficient (r b)/(2alpha). Its derivative has that coefficient divided by tau. The v term in nu is at most logarithmic, so

`nu=d(r b)/(2alpha tau)+O(ln|tau|)`.

The divergent lapse has a direct scalar invariant: the perturbation of X on surfaces of constant clock is

`delta X_clock=delta X-(Xdot/q)delta phi`.

This combination is invariant under a linear time coordinate change. In unitary clock gauge delta phi=0 and X=q²/(2N_lapse²), so delta X_clock=-q²nu. Its generic pole cannot be removed by a smooth gauge change. It establishes a breakdown of finite linear clock perturbations near the simple crossing. It does not establish quantum vacuum decay or describe the nonlinear continuation once perturbations become large.

Regular local amplitudes obey the one independent condition r b=0 and form a codimension-one subspace per Fourier mode. No dynamical selection of that subspace or continuation of arbitrary initial data is provided. A spectrum whose comoving modes never cross a zero is outside this obstruction. The comoving-envelope calculation determines which modes encounter such zeros; an instantaneous negative-band argument alone does not.

## Review and checks

Root derived the residue from the full equations; the main-theory agent independently reconstructed its four components and the analytic-series argument. The symbolic checks verify the residue, nilpotent rank, absence of a dust-density pole, regular dust elimination, mixing coefficient, and invariant lapse pole. A deleted clock-density component is an expected-failing control. A first development invocation substituted before rational cancellation and failed four residue checks; it is superseded by cancellation before taking A=0, rather than treated as scientific evidence.

This is a conditional local theorem, not a complete mode-transfer calculation, a radiation/recombination solution, or a 32pi selector. It gives a concrete perturbative obstruction to promoting the smooth dust background to a generic regular cosmology.
