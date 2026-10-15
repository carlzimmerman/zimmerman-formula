# A dynamical critical-charge stiff pair: exact Maxwell base and a positive-radial-energy nonlinear Newtonian branch

VC3-CRITICAL-STIFF-001, 15 October 2026. This is a genuinely critical-charge counterroute after the soft co-Plummer instability. Both gravitating populations are dynamical: an ordinary neutral baryonic fluid b and a charged cold fluid c with q_c/m_c=sqrt(4 pi G). There is no held central source and no added neutral support stock. The **chosen** equations of state are P_b=K_b rho_b^2 and P_c=K_c rho_c^2. Their normalization relation below is a continuum input, not derived baryon microphysics or a predicted abundance.

The exact Maxwell auxiliary model has a compact two-fluid equilibrium and strictly positive coupled radial density/Gauss energy. A genuinely finite-D0 branch also exists and has positive radial energy in the explicitly defined **Newtonian instantaneous nonlinear-electric model** below. Its global nonrelativistic electric energy is an assigned spatial constitutive functional. It is not a derivation of the relativistic material-frame vacuum phase. Attempting the unchanged RTM finite-density causal response at the outer cold edge fails its gate. Thus this result repairs the moving-core radial-energy problem in a critical-charge Newtonian comparison; it does not close the original theory.

## 1. Conserved species and the declared Newtonian energy

Each rest-mass density has its own conserved fluid velocity. Newtonian gravity is sourced by rho_b+rho_c. Only c carries the critical charge. The potential energy is

\[
 E=\int(K_b\rho_b^2+K_c\rho_c^2)d^3x
 -{G\over2}\iint{(\rho_b+\rho_c)(x)(\rho_b+\rho_c)(y)\over|x-y|}dxdy
 +\int H(|\mathbf D|)d^3x,\qquad
 \nabla\cdot\mathbf D=\sqrt{4\pi G}\,\rho_c .          \tag{1}
\]

At the Maxwell base H=D^2/2. For the nonlinear Newtonian continuation **define the same instantaneous spatial functional on all of space**, including the empty exterior,

\[
 H(D)=D_0^2[-x-\log(1-x)],\quad x=D/D_0<1,\quad
 E(D)=H'(D)={D\over1-D/D_0},\quad D_0={a_0\over\sqrt{4\pi G}}.
                                                               \tag{2}
\]

This is a well-defined spherical nonrelativistic field-energy model. It does not require a material U in empty space, because it is stipulated in the preferred Newtonian time/spatial description; no Lorentz-invariant or RTM vacuum action is inferred from it. It is not a switch to Maxwell outside a material phase: there is no Hamiltonian jump and no artificial uncounted surface traction in this model. A relativistic embedding is a separate obligation.

Ordinary Newtonian fluid kinetic energy is sum integral rho_a v_a^2/2. No propagating-cone conclusion is drawn from this convention. With spherical density and positive cold charge, Gauss fixes D=sqrt(4 pi G)M_c(<r)/(4 pi r^2); the curl equation for E is automatic. Static force balance is

\[
 P_b'=-\rho_b{G(M_b+M_c)\over r^2},\qquad
 P_c'=-\rho_c{G\over r^2}
                  \left[M_b+M_c-{M_c\over1-x}\right]. \tag{3}
\]

These equations count actual charge separately from actual mass. The nonlinear self-electric correction is outward; it has not been replaced by a neutral gravitational source.

## 2. Exact critical-charge Maxwell equilibrium

Choose f>0 and

\[
 K_c={K_b\over f(1+f)},\quad
 k^2={2\pi G(1+f)\over K_b},\quad R_0={\pi\over k}.
\]

For any rho_*>0, let

\[
 \rho_b=\rho_*{\sin(kr)\over kr},\qquad
 \rho_c=f\rho_b\quad(0\le r\le R_0),\qquad
 \rho_b=\rho_c=0\quad(r>R_0).                          \tag{4}
\]

The profiles are positive inside, regular at zero, and vanish linearly at the common free edge. Their enclosed masses satisfy M_c=fM_b and M_b'=4pi r^2rho_b. At Maxwell critical charge, the cold self-gravity cancels its own electric repulsion exactly, so b feels G(M_b+M_c) while c feels GM_b. Substitution of the EOS normalization verifies both equations (3) at x=0. The radius obeys

\[
 R_0^2={\pi K_b\over2G(1+f)}.
\]

All masses and field energy are finite. The electric Maxwell field and its stress are continuous through the zero-density free edge and are globally defined in the exterior. Both material pressures vanish there; there is no imposed wall or external pressure. The ratio f is assigned, not generated.

## 3. Exact two-channel radial energy at the Maxwell base

Let u=delta M_b and v=delta M_c be separately conserved enclosed-mass perturbations, each zero at the center and at its free edge. Eliminating Poisson and Gauss gives the full coupled radial potential Hessian

\[
 Q=\int_0^{R_0}\left[{K_b\over2\pi}u'^2
                         +{K_c\over2\pi}v'^2\right]{dr\over r^2}
       -G\int_0^{R_0}{u^2+2uv\over r^2}dr .           \tag{5}
\]

The cold v^2 gravity is canceled by actual critical Coulomb energy, not discarded. The gravity cross term is retained. Write A=K_b/(2pi) and make the invertible constant change

\[
 u=a+b,\qquad v=f a-(1+f)b.
\]

Direct congruence diagonalizes both derivative and potential terms:

\[
 Q=(1+2f)\int_0^{R_0}\left\{
 {A\over1+f}a'^2-Ga^2+{A\over f}b'^2+Gb^2\right\}{dr\over r^2}.
                                                               \tag{6}
\]

The a channel has the actual equilibrium mass ratio; the independent b channel is repulsive. For any regular mass variable z zero at both endpoints,

\[
 \int_0^L{z'^2\over r^2}dr
 =\int_0^L\left[((z/r)')^2+2{(z/r)^2\over r^2}\right]dr
 \ge{\pi^2+2\over L^2}\int_0^L{z^2\over r^2}dr.       \tag{7}
\]

The last inequality is the elementary Dirichlet sine ground-state identity plus r^-2>=L^-2, first on regular compact approximants and then on the form closure. Since R0^2=pi^2A/[G(1+f)], (6)--(7) give

\[
 Q\ge(1+2f)G\left[{2\over\pi^2}\int{a^2\over r^2}dr
                              +\int{b^2\over r^2}dr\right]>0.
                                                               \tag{8}
\]

This is a bound for every nonzero admissible pair, not a finite mode test. It proves a positive radial density/Gauss energy; positive fluid kinetic energy then gives a conserved radial quadratic comparison energy for suitable linear solutions. It is not an angular or nonlinear free-boundary theorem. Separate chemical constants are handled by the separately conserved masses in the Hessian; pressure and density both vanish at either free edge, so no extra quadratic wall energy is present.

## 4. Actual finite-D0 Newtonian bulk and exterior continuation

The nonlinear Newtonian model (1)--(2) has an actual compact branch without fitting inverse EOSs. Let ell^2=K_b/(2piG), scale r=ell t and rho_a=rho_* theta_a, M_a=4pi rho_* ell^3 m_a, and set

\[
 \lambda={K_b\over K_c}=f(1+f),\qquad
 \eta={4\pi G\rho_*\ell\over a_0},\qquad
 x={\eta m_c\over t^2}.
\]

Introduce continued enthalpy variables theta_a with actual densities (theta_a)_+=max(theta_a,0). The ordinary differential equations are

\[
 \theta_b'=-{m_b+m_c\over t^2},\quad
 \theta_c'=-{\lambda\over t^2}
                         \left[m_b-{m_c x\over1-x}\right],
 \quad m_b'=t^2(\theta_b)_+,\quad m_c'=t^2(\theta_c)_+,
\]

\[
 \theta_b(0)=1,\quad\theta_c(0)=f,\quad m_b(0)=m_c(0)=0. \tag{9}
\]

The continued negative enthalpy is only an ODE device outside a fluid; it is not a negative physical density. At eta=0, (9) is exactly the scaled solution (4), whose two zeros are transverse. On a fixed interval containing those zeros, the integral form has locally Lipschitz positive-part sources and denominators uniformly separated from the pole. Ordinary contraction/continuation therefore gives unique solutions continuous in eta, including the regular-center limits m_a=O(t^3), x=O(eta t). Each transverse zero persists and tends to the base radius. Beyond each first zero that fluid density is set to zero by (9). At the outer cold zero require m_b(R_c)>m_c(R_c)x(R_c)/(1-x(R_c)); this strict inequality holds by continuity from its positive Maxwell-base value. Beyond that zero m_c is constant, x decreases as t^-2 and m_b cannot decrease, so the cold enthalpy remains decreasing and cannot reenter the occupied phase. Baryonic enthalpy is always decreasing. The two masses freeze outside the outer zero and the exterior nonlinear field has finite energy. This constructs an actual finite-mass solution of the declared global Newtonian model.

The supports split at positive eta. While both fluids are occupied, put z=theta_c-f theta_b and n=m_c-fm_b. Then

\[
 z'={f n+\lambda m_c x/(1-x)\over t^2},\qquad n'=t^2z,
 \quad z(0)=n(0)=0.
\]

The cooperative integral equations imply z,n>0 for t>0 and eta>0. Hence at the baryon zero, cold density is still positive: R_b<R_c. The mass ratio at finite eta is no longer fixed to f and is not silently reset. No EOS constant has been retuned after seeing the profile.

## 5. The finite-D0 branch retains positive full radial energy

Let L be the outer support radius in physical units. Extend each separately conserved mass perturbation by zero past its own edge to [0,L]. These extensions are admissible Dirichlet form variables. The radial electric Hessian is H''(D)=(1-x)^-2>=1, so the full nonlinear field adds a nonnegative quadratic term to the critical Maxwell Hessian (5), while the fixed Gamma2 internal coefficients are unchanged. Consequently the same constant congruence and (7) give

\[
 Q_{\rm NL}\ge(1+2f)G\left[\kappa_L\int{a^2\over r^2}dr
                                   +\int{b^2\over r^2}dr\right],
 \qquad \kappa_L=\left(1+{2\over\pi^2}\right){R_0^2\over L^2}-1.
                                                               \tag{10}
\]

Because L tends to R0 as eta tends to zero, kappa_L>0 on a sufficiently small positive branch. Thus there is no held-core stability inference: both fluids and their gravity cross term are varied, and (10) controls the entire radial comparison form. The proof gives a qualitative open parameter range; the finite numerical example is not an interval certification or an explicit universal threshold.

## 6. Exact obstruction to importing this result as RTM closure

At the outer cold edge R_c, the total cold charge is positive and finite, so D(R_c)>0. Both actual densities vanish there. For either a cold-only material frame or a frame including both fluids, the effective inertia tends to zero. The retained finite-D0 RTM gate requires

\[
 h_*>h_{\rm crit}=D_0^2{x^3\over(1-x)^2}>0.
\]

It therefore fails **inside** the positive-density taper near R_c for every finite D0 in this compact branch. The Newtonian radial energy result cannot override that local principal obstruction. The Maxwell base evades it only because D0 tends to infinity, not because a physical finite-D0 carrier was produced.

Likewise, replacing the assigned global Newtonian nonlinear exterior by Maxwell vacuum at the zero-pressure edge would create the positive electric Hamiltonian jump Delta H=D0^2[-x-log(1-x)-x^2/2]. Zero fluid pressure and no counted surface carrier cannot balance that jump. A new phase/interface mechanism is needed; the separate fixed-core interface control does not automatically apply to this dynamical pair.

The scalar global functional (2) is useful as an explicitly chosen Newtonian counterroute. It supplies neither the missing relativistic vacuum action, a healthy RTM taper, nor the original critical-charge galaxy law for real baryonic EOSs. Positive radial energy and actual charged-core force balance are real advances within that model, with the remaining obstruction now isolated at finite-density/vacuum health and physical EOS selection.

## 7. EOS dictionary and verification

Under the optional S2 radial Hodge identification rho_c=div bold-P, curl bold-P=0 and vanishing boundary term, gamma integral |grad bold-P|^2/2=integral K_c rho_c^2 with K_c=gamma/2. This is the same energy, not an additional term. The exact Maxwell matching then requires K_b=f(1+f)gamma/2. The ordinary baryonic pressure law and this normalization are chosen inputs; no universal real-galaxy baryonic EOS is deduced.

`check_critical_stiff.py` verifies the exact Maxwell solution, both force balances, constant congruence, uniform radial margin, Gauss/nonlinear normalization and positive support-splitting identity. A bounded finite-D0 integration gives an implementation illustration with positive densities, separate free edges and a strict radius-based radial margin. The code and contract explicitly distinguish that finite floating run from the qualitative existence proof and the RTM obstruction.
