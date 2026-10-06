# Conserved radiation changes the clock connection and its early mode threshold

The logKGB clock admits a unique tuned analytic expanding connection from an early ordinary-radiation GR background to its selected late rolling vacuum, with both ordinary dust and radiation minimally coupled and conserved. Radiation modifies the critical conserved charge and the late dust enhancement. It also changes the early fixed-comoving kinetic limit: sufficiently small comoving modes can retain a negative clock kinetic coefficient toward the radiation limit. This result extends the background theorem; it does not solve radiation perturbation transfer, atomic recombination, CMB observables, cold-mass assembly or the 32pi selector.

## Exact same-action background

Work in four spacetime dimensions with Einstein coefficient M/2, M>0, c>0, H*>0, eta=c/(3M H*²)>0. The scalar has K=-c ln(X/Xref), G=-sqrt(2)c/(3H*) X^(-1/2), L3=-G Box(phi), positive q=phidot, X=q²/2, and constant vacuum rho_v. Its actual current and stresses are

`J=2c(h-1)/q`, `a_FRW³ J=J0`,

`rho_phi=c ln(q²/(2Xref))+2c(h-1)`,

`p_phi=-c ln(q²/(2Xref))-[2c/(3H*)] qdot/q`,

where h=H/H*. Add independently conserved ordinary dust and radiation,

`rho_d=rho_d0 a_FRW^-3`, `rho_r=rho_r0 a_FRW^-4`, `p_r=rho_r/3`.

Use the same selected-vacuum q* as in the parent theorem. Define D=rho_d0/(2c)>0, R=rho_r0/(2c)>0, j=J0 q*/(2c)>0. Current conservation gives q/q*=a_FRW³(h-1)/j. Vacuum-subtracted Friedmann is exactly

`f(h)=D a_FRW^-3+R a_FRW^-4+3 ln(a_FRW)-ln(j)`,

`f(h)=(h²-1)/(2eta)-(h-1)-ln(h-1)`, h>1.

There is no extra independently conserved clock dust term on the right. All scalar pressure and charge effects are retained on the left through f and the q relation. The clock congruence is homogeneous and geodesic. A finite-A response M[kappa a_mu a^mu-2W(|a|;A)], W=O(|a|³/A), still vanishes with its first variation; neither the background history nor its quadratic coefficients select A.

## A unique source fold and critical charge

Set t=ln(a_FRW). The source derivative is `3-3D exp(-3t)-4R exp(-4t)`, strictly increasing from minus infinity to 3. It has exactly one zero at a_f>0, characterized by

`d_f=D/a_f³`, `r_f=R/a_f⁴`, `d_f+(4/3)r_f=1`.

Both densities are positive, so `0<r_f<3/4` and `d_f=1-4r_f/3>0`. The source tends to infinity at both scale-factor endpoints and has second t derivative `9d_f+16r_f=9+4r_f>0` at the fold. The scalar-side unique minimum is unchanged: h_f=1+eta and f_min=1-eta/2-ln eta.

Matching the two minima gives the necessary charge

`j_crit=eta a_f³ exp(eta/2-r_f/3)`.

If the source minimum is lower there is a missing-real-root interval. If higher, the upper and lower h roots never meet. Thus a globally continuous early-GR upper-root to late-H* lower-root connection requires precisely this tuning. Arbitrary conserved J0 does not relax into it.

For sufficiency write x=a_FRW/a_f, u=(h-1)/eta, and L(y)=y-ln(y)-1. At the tuned charge the exact normalized equation is

`L(u)+(eta/2)(u-1)² = d_f(x^-3-1)+r_f(x^-4-1)+3 ln x`.

The right side has a unique nondegenerate zero at x=1 and is positive elsewhere. On x<1 select u>1; on x>1 select 0<u<1. Both sides are strictly monotone on their corresponding halves, giving a unique decreasing h(a_FRW) throughout the positive scale factors. The signed square root at their quadratic zeros supplies a local analytic crossing, with

`dh/d ln(a_FRW)|_f = -eta sqrt(9+4r_f)/sqrt(1+eta)`.

The pure-dust limit r_f=0 reproduces the parent slope. For each finite positive a_FRW, h and q are finite and positive. The analytic local crossing plus the smooth simple-root branches supply the global finite-a background connection.

## Homogeneous on-shell check and predictions

Set q by the conserved current and integrate d ln(a_FRW)/dt=H. The unchanged scalar current gives `qdot/q=3H+Hdot/(H-H*)`, which implies `rhodot_phi+3H(rho_phi+p_phi)=0` with the actual pressure. The matter continuities are `rhodot_d=-3Hrho_d` and `rhodot_r=-4Hrho_r`. Differentiated Friedmann therefore yields the actual spatial equation

`2M Hdot=-(rho_d+4rho_r/3+rho_phi+p_phi)`.

No pressureless substitution for the scalar or radiation has been made. The Big Bang endpoint and perturbative health are separate obligations.

For any R>0, the early asymptotics are

`h ~ alpha a_FRW^-2`, `alpha=sqrt(2eta R)`,

`3M H² ~ rho_r`, `q/q* ~ (alpha/j) a_FRW`.

The ordinary dust correction is subleading. Thus q remains positive at every finite early scale factor but tends to zero at the excluded singular endpoint. More precisely,

`h=alpha a_FRW^-2+beta a_FRW^-1+gamma+o(1)`,

`beta=eta D/alpha>0`, `gamma=eta-beta²/(2alpha)`.

Terms involving logarithms first enter lower orders and do not alter these coefficients. The R->0 and a_FRW->0 limits are nonuniform: however small positive R is, sufficiently early expansion is radiation dominated.

At late a_FRW,

`h-1~j_crit a_FRW^-3`, `q/q*->1`,

`3M(H²-H*²) ~ E rho_d`,

`E=j_crit/(eta D)=exp(eta/2-r_f/3)/(1-4r_f/3)`.

E increases strictly with r_f, since `d ln E/d r_f=-1/3+4/[3(1-4r_f/3)]>0`. It reduces to exp(eta/2) for dust-only histories but can grow without bound in the parameter limit r_f->3/4 with D remaining positive and tending to zero relative to the fold scale. Consequently the inherited dust-only sqrt(e) cap for 0<eta<1 is not a bound on these radiation histories. For example eta=1/2,r_f=0.7 gives E about 15.25. This is a parameter-limit fact and a background prediction. For specified observed rho_d0/rho_r0 and action parameters, a_f and r_f are fixed by the minimum equation; E is not a freely adjustable fit parameter. Nor is E an independently conserved cold abundance or a measurement of laboratory Newton's constant.

Scale-factor normalization is harmless: under a_FRW->s a_FRW, D->s³D, R->s⁴R, j->s³j, a_f->s a_f. The invariant quantities d_f,r_f,E and j/D do not change. Under the exact constant-vacuum rescaling, q* and J0 transform inversely, preserving J0 q* and the critical condition as in the parent theorem.

## Matter constraints and the radiation-era comoving kinetic limit

For the health statement restrict 0<eta<1, kappa>0 and a nonzero Fourier mode, so Theta=M H*(h-eta) never vanishes. The actual scalar coefficients remain

`Sigma=3M H*²[eta(1+h)-h²]`,

`K_c/M=[3eta(1+eta-h)+kappa(p/H*)²]/(h-eta)²`, `p=k/a_FRW`.

These are actual-H coefficients, not transplanted vacuum coefficients. Radiation is represented by a minimally coupled P(Y)=C Y² field with positive enthalpy and c_r²=1/3. With one or more regular perfect-fluid velocities v_i, the shift relation is `nu=(M zetadot+sum_i (rho_i+p_i)v_i/2)/Theta`. Each fluid adds a positive square `C_i(vdot_i-d zetadot)^2` to the velocity form, with d=M/Theta and C_i=(rho_i+p_i)/(2c_i²)>0. The three-velocity determinant for a dust regulator plus radiation is `K_c C_d C_r`. Taking the exact dust action instead, its canonical change w_d=v_d-d zeta cancels the density-momentum/zetadot term exactly. The regular radiation square remains, so its velocity Schur complement is still K_c. Ordinary radiation mixing does not remove the stated unitary-configuration negative direction. These kinetic statements do not classify the full coupled infrared mode dynamics.

In the early radiation limit a fixed comoving k gives

`K_c/[M a_FRW²] -> [kappa(k/H*)²-3eta alpha]/alpha²`.

Thus modes strictly below `k²/H*²=3eta sqrt(2eta R)/kappa` have negative K_c sufficiently early; modes strictly above have positive K_c sufficiently early. At exact threshold the dust term gives `K_c/[M a_FRW³] -> -3eta beta/alpha²<0`, so equality is also early-negative when D>0. Using the invariant normalized wave number k_bar=k/(H* a_f), the threshold is `k_bar_crit²=3eta sqrt(2eta r_f)/kappa`.

This differs substantively from pure dust: there the response p² grows faster than h, making every fixed nonzero k eventually positive toward the early limit. Here radiation makes both compete as a_FRW^-2. The difference disappears at fixed finite a_FRW as R approaches zero, but the order of the two limiting operations matters.

The instantaneous negative band remains `p_crit²=3eta H*²(h-1-eta)/kappa`. Its maximum ratio to H² is still `3eta/[4kappa(1+eta)]`, below 3/8 for kappa=1, 0<eta<1. In the far radiation limit p/H tends to zero for fixed k. Hence an early-negative fixed-comoving coefficient is still not a high-frequency instability or quantum vacuum-decay theorem. The dust-only canonical-crossing proof cannot simply be transplanted into the additional-radiation system: its larger constrained state space, potentials and regularity conditions require a fresh analysis. This report does not claim radiation-mode logarithmic poles or a completed health result.

## Exact remaining implication and evidence

The construction now includes ordinary radiation at background level and predicts its charge-dependent connection to late vacuum. It introduces neither the microphysics of recombination nor a pre-recombination cold source. Its next physical obligations are coupled dust/radiation/clock perturbation transfer and crossing regularity, radiation acoustic propagation and photon/baryon reactions, and a matched nonlinear source branch. Even a healthy completion of those arrows would leave the finite positive response scale A unchanged by these homogeneous equations, so the original 32pi selection remains open.

checks.py verifies the minimum, critical charge, signed-root identity, slope, early expansion coefficients, matter kinetic squares, late enhancement and bounded monotone backgrounds at eta=1/2 and r_f=0,0.25,0.7. Three controls incorrectly reuse the dust charge, reuse dust early positivity, or enforce the dust enhancement cap. Exact global assertions follow from the derivation, not sampled roots. SOURCES.md records the primary source dependencies and their scopes. REPORT.md is not an execution input; report clarification cannot silently stale the calculation. No frozen parent inputs were edited.


Authoritative evidence: runs/main_a passes 31 checks; control_charge_a, control_early_a and control_enhancement_a each fail their intended assertion. All four manifests independently validate against current input and output hashes. No unsupported address-space limit was requested on this host; the recorded wall-time, CPU-time and numerical thread limits bound the runs. The preflight result is a development artifact, not the authoritative run.
