# An exact finite-mass neutral atmosphere around a fixed regular core

AS2-CORE-001. Conditional construction in Newtonian rest-mass gravity, with the local constitutive gate checked separately. The central mass and charge profiles, neutral species, polytropic EOS and constitutive response are specified inputs. This is not a solution for the original charged carrier/core or the full Einstein equations.

## Exact occupied equilibrium without an inner wall

Fix a central gravitating density with total mass M0>0 and scale b>0,

\[
 \rho_0(r)={3M_0b^2\over4\pi(r^2+b^2)^{5/2}},\qquad
 \Phi_0=-{GM_0\over\sqrt{r^2+b^2}}.
\]

The central source is held fixed during this comparison. Give the neutral support species a rest density and EOS

\[
 \rho_s(r)={3fM_0b^2\over4\pi(r^2+b^2)^{5/2}},\qquad
 P=K\rho_s^{6/5},\qquad f>0.
\]

Its total rest mass is exactly fM0. It is positive at every finite radius, finite at the center and decays as r^-5, so it requires no finite-density-to-vacuum interface or reflecting inner wall. Its self-potential is \(\Phi_s=f\Phi_0\). Put \(\Psi=-(\Phi_0+\Phi_s)\). The isentropic specific enthalpy is \(w=6K\rho_s^{1/5}\). The choice

\[
 6K\left({3fM_0\over4\pi b^3}\right)^{1/5}
 ={GM_0(1+f)\over b}                                      \tag{1}
\]

gives w=Psi, and differentiation yields the exact Euler-Poisson equilibrium

\[
 P'=-\rho_s{GM_0(1+f)r\over(r^2+b^2)^{3/2}}.
\]

This includes support rest-mass self-gravity. It does not include the gravitational stress/energy of the gauge field, pressure corrections to the metric, or the central body's response. In a weak-field interpretation those are additional relativistic corrections, not terms silently included here.

For fixed K,M0,b define

\[
 \mu={4\pi b^3\over3M_0}\left({GM_0\over6Kb}\right)^5.
\]

Equation (1) is \(\mu=f/(1+f)^5\). Its derivative is \((1-4f)/(1+f)^6\), so it has a unique weak branch 0<f<1/4 for 0<mu<256/3125, a turning point f=1/4, and a second larger branch. This does not select K or the atmospheric mass. Choosing an example f means specifying the corresponding EOS normalization, not deriving an abundance.

## Positive density-energy Hessian on the weak branch

Keep the central source fixed. The neutral Euler-Poisson energy is

\[
 {\cal E}=\int 5K\rho^{6/5}\,d^3x
       +\int\rho\Phi_0\,d^3x
       -{G\over2}\iint {\rho(x)\rho(y)\over|x-y|}\,d^3x\,d^3y.
\]

The equilibrium first variation vanishes because w+Phi0+Phis=0. For a density perturbation eta in the finite quadratic-form domain,

\[
 Q[\eta]=\int a(x)\eta(x)^2\,d^3x
       -G\iint{\eta(x)\eta(y)\over|x-y|}\,d^3x\,d^3y,
 \qquad a={c_{s,N}^2\over\rho_s},\quad c_{s,N}^2={\Psi\over5}.
\]

Here c_s,N is the Newtonian barotropic sound speed. Use the positive profile rho_s in

\[
 2|\eta(x)\eta(y)|\le
 \eta(x)^2{\rho_s(y)\over\rho_s(x)}
 +\eta(y)^2{\rho_s(x)\over\rho_s(y)}.
\]

Integration against G/|x-y| gives the weighted Schur bound

\[
 \left|G\iint{\eta(x)\eta(y)\over|x-y|}\right|
 \le\int{\eta^2\over\rho_s}(-\Phi_s)
 ={5f\over1+f}\int a\eta^2.
\]

Therefore

\[
 \boxed{\quad Q[\eta]\ge
 \left(1-{5f\over1+f}\right)\int a\eta^2>0
 \quad\text{for }0<f<1/4,\ \eta\ne0.\quad}              \tag{2}
\]

This bound applies to arbitrary spatial density perturbations in the stated form domain, not just radial trials. Its constant is sharp on the unconstrained density space: eta proportional to rho_s saturates the inequality. Such a direction need not preserve total support mass. Thus failure of the sufficient bound above f=1/4 is not by itself a mass-conserving instability theorem.

Positive fluid kinetic energy plus (2) gives a positive conserved quadratic energy for the fixed-source linear Euler-Poisson comparison, subject to existing finite-energy solutions and no flux at infinity. It supplies no uniform frequency gap, nonlinear existence theorem, moving-core stability or full gauge/Einstein stability by itself. The distinct fixed-inner-boundary atmosphere and its moving-boundary counterexample are treated in `../stability/REPORT.md`.

## Finite charge field and the local constitutive gate

For one explicit regular source comparison, fix the enclosed charge in critical-chi-mass units to

\[
 M_Q(<r)=M_Q{r^3\over(r^2+b^2)^{3/2}},\quad
 t=r/b,\quad q_0={GM_Q\over a_0b^2},\quad
 x={D\over D_0}=q_0{t\over(1+t^2)^{3/2}}.
\]

D0=a0/sqrt(4 pi G), as in the parent constitutive model. The neutral atmosphere adds no minimal gauge charge. The charge profile is held fixed, not inferred from the neutral density or proved to be the original carrier's equilibrium. Its maximum is x_max=2q0/(3sqrt(3)); require q0<3sqrt(3)/2 to avoid the constitutive pole.

For the support EOS epsilon_mat=rho_s c²+5P,

\[
 h_s(1-s_s^2)=\rho_sc^2+{24\over5}P\ge\rho_sc^2,
 \qquad s_s^2={\Psi\over5(c^2+\Psi)}<1/5.
\]

This s_s is the relativistic EOS sound fraction used in the local mode gate; it is distinct from the Newtonian c_s,N. Put epsilon0=GM0/(bc²), gamma_Q=M_Q/M0. Exact substitution gives

\[
 {h_{\rm crit}\over\rho_sc^2}
 ={\epsilon_0\gamma_Q^2 q_0\over3f}
 {t^3\over(1+t^2)^2(1-x)^2}.
\]

Since t³/(1+t²)²<=3sqrt(3)/16 and x<=x_max, a sufficient all-finite-radius gate is

\[
 f>{\epsilon_0\gamma_Q^2q_0\sqrt3
       \over16(1-x_{\max})^2}.                            \tag{3}
\]

A simple rational witness uses q0=gamma_Q=1/2, epsilon0=10^-6 and f=10^-3. Then x<1/5, t³/(1+t²)²<1/2, and

\[
 {h_{\rm crit}\over\rho_sc^2}<\frac{25}{768000},\qquad
 \frac{h_s(1-s_s^2)}{h_{\rm crit}}>30720
 \quad(r>0),\qquad {5f\over1+f}={5\over1001}<1.
\]

The largest gravitational potential is only epsilon0(1+f)c². This assigned hierarchy puts support rest-mass self-gravity above the omitted relativistic corrections in order of magnitude; it does not constitute a controlled full Einstein solution or a parameter fit.

At the origin D=0 and hcrit=0. The parent pure-electric mode theorem is stated for 0<x<1; its Maxwell-like limiting coefficients do not by themselves prove differentiability/well-posedness of the nonlinear constitutive action for every nearby magnetic configuration at E=0. That regularity remains an action-level obligation. At infinity the support and electric field both decay, with support density falling more slowly than hcrit. No finite empty-vacuum boundary is crossed, but uniform hyperbolicity, asymptotic field phase and microscopic realization remain unproved.

## Exact checks and nonclaims

The accompanying code checks density/enclosed mass, Poisson and hydrostatic equations, EOS normalization, branch derivative/turning point, the exact Schur constant, charge-field bounds and the rational weak-field/gate witness. Independent shell quadrature verifies the support potential at fixed radii. The analytic equations and inequalities, not the finite samples, establish the stated uniform claims.

This is a regular, finite-mass, occupied **neutral support** construction around prescribed regular central mass/charge sources. It is not an action-derived charged galaxy/core, a generated cosmic abundance, a conversion/settling history, or a new empirical pass. Joining the dynamical gauge/current energy to (2) must be independently derived rather than assumed from separate positivity statements.
