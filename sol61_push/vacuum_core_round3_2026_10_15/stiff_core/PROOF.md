# A fixed-EOS subcritical stiff core has a self-consistent small-neutral branch with positive radial energy

VC3-STIFF-001, 15 October 2026. This changes the charged-core candidate after the critical co-Plummer counterexample. The charged EOS is now fixed before solving, P_c=K rho_c^2 with K>0; the charge ratio is **subcritical**, q_c/m_c=b_q sqrt(4 pi G), 0<alpha=b_q^2<1. A neutral n=5 atmosphere has its own fixed EOS normalization. These are new continuum inputs; this result does not recover the original critical-charge galaxy law or derive a microscopic species/abundance.

The result is qualitative but mathematical: for every fixed alpha in (0,1), an open sufficiently small positive range of the neutral-amplitude and nonlinear-field parameters admits an actual finite-mass two-fluid Newtonian equilibrium, with positive coupled **radial** density/Gauss quadratic energy. The proof constructs the finite-mass exterior and a scalar interior/exterior matching map. It does not infer equilibrium from positivity alone. A bounded shooting calculation below is a separate numerical illustration; no numerical sample supplies the existence theorem.

## 1. Equations and physical inputs

Use the same two conserved currents, varied total rest-mass-current frame, positive Gauss convention and pure-electric law as `../core/PROOF.md`. The source of Newtonian gravity is rho_c+rho_s, with no held source. The charged EOS is P_c=K rho_c^2 and its material energy is rho_c c^2+P_c. The neutral EOS is P_s=K_s rho_s^(6/5), material energy rho_s c^2+5P_s. Neutral chemical equilibrium with pressure vanishing at infinity gives w_s=6K_s rho_s^(1/5)=-Phi. The first constitutive frame variation still vanishes on this static electric state; it is not held fixed before variation.

Fix central core density rho_*>0 and set

\[
 \ell^2={K\over2\pi G},\quad r=\ell t,\quad
 \rho_c=\rho_*\theta,\quad
 -\Phi=2K\rho_*\psi,\quad
 M_a=4\pi\rho_*\ell^3 m_a,
\]

\[
 \delta={1\over\rho_*}\left({2K\rho_*\over6K_s}\right)^5,
 \quad \eta={b_q4\pi G\rho_*\ell\over a_0},\quad
 x={D\over D_0}={\eta m_c\over t^2}.
\]

Thus rho_s=delta rho_* psi^5. In the charged core, theta>0, the exact Newtonian comparison equations are

\[
 \theta'=-{m_c+m_s-\alpha m_c/(1-\eta m_c/t^2)\over t^2},
 \quad m_c'=t^2\theta,\quad m_s'=\delta t^2\psi^5,
 \quad \psi'=-{m_c+m_s\over t^2}.                       \tag{1}
\]

At the center theta(0)=1, m_c(0)=m_s(0)=0. The value psi(0) is determined by matching to the finite-mass exterior, rather than freely assigned. The first zero R of theta is the charged free boundary. Outside R, m_c is constant and theta=0; the neutral equations continue. There is no reflecting wall, imposed surface pressure or surface charge. The electric displacement remains continuous. Since the neutral density is positive at every finite t, the total-current frame does not vanish at the charged edge. This does not prove regularity of the disappearing charged current or a vacuum extension at infinity.

## 2. Exact base solution and a genuine finite-mass exterior map

At delta=eta=0 put k=sqrt(1-alpha). The exact charged solution is

\[
 \theta_0={\sin(kt)\over kt},\quad R_0={\pi\over k},\quad
 m_{c,0}=-{t^2\theta_0'\over k^2},\quad
 m_{c,0}(R_0)={\pi\over k^3},\quad
 \psi_0(t)={1+\theta_0(t)\over k^2}\quad(t\le R_0).
\]

Outside R0, psi0=m_c,0(R0)/t. The core zero is transverse: theta0'(R0)=-k/pi. It is therefore a free boundary that persists under small perturbations, not an assumed fixed profile.

For any R>0 and enclosed total mass m_R>0 near their base values, the neutral exterior solves

\[
 \psi(t)={m_R\over t}
 +\delta\int_t^\infty {ds\over s^2}
                    \int_R^s u^2\psi(u)^5du.           \tag{2}
\]

Normalize z=t/R, psi=(m_R/R)Z(z), and

\[
 \mu={\delta m_R^4\over2R^2}.
\]

The map becomes Z=1/z+2 mu integral_z^infinity s^-2 integral_1^s u^2 Z(u)^5 du ds. In the weighted norm ||Z||=sup_(z>=1) z|Z(z)|, it preserves 1/z<=Z<=C/z if 1+mu C^5<=C, and has Lipschitz constant q_ext=5mu C^4. For example C=2 works whenever mu<=1/32 and mu<1/80. This is a strict contraction, hence a unique occupied exterior in that interval. Its total mass is finite and lies between m_R(1+mu) and m_R(1+mu C^5). Its potential tends to zero, so it fixes an actual exterior gravitational boundary condition.

The boundary value B(R,m_R,delta)=psi(R) is C1 in parameters near the base. To see this rather than assume it, scale to z>=1 as above; all parameter dependence of the normalized map is polynomial in mu. Its derivative on the order interval is a uniformly bounded integral operator with norm at most q_ext<1. Difference quotients satisfy a linear equation with inverse (I-DT)^-1=sum_(j>=0)(DT)^j; the series converges uniformly. The second-order remainder is bounded by the same integrable z^-5 majorant. Thus derivatives exist and are continuous. Restoring the smooth factors m_R/R and mu proves the claim for B, including its one-sided positive-delta continuation. At delta=0, B=m_R/R.

## 3. Interior/exterior matching establishes a coupled branch

For parameters (psi_c,delta,eta) near (2/k^2,0,0), solve the regular-center interior initial-value problem (1) until its first theta zero. The apparent t^-2 singularity is removable by the integral form and m_a=O(t^3); in particular x=O(eta t), and the constitutive pole has a strict margin on a fixed bounded neighborhood. Standard local Picard contraction on the integral equations, followed by ordinary continuation away from zero, gives C1 dependence on these parameters. The transverse zero gives C1 functions R and m_R=m_c(R)+m_s(R). These assertions can alternatively be obtained by differentiating the bounded integral equations and their nonvanishing zero condition; no source profile is frozen.

Define the scalar mismatch

\[
 F(\psi_c,\delta,\eta)=\psi_{\rm int}(R)
             -B(R,m_R,\delta).                         \tag{3}
\]

At delta=eta=0, the interior theta and masses do not depend on psi_c. The potential is psi_int=psi_c+(theta0-1)/k^2. Hence

\[
 F(\psi_c,0,0)=\psi_c-{2\over k^2},\qquad
 \partial_{\psi_c}F=1.                               \tag{4}
\]

For completeness, the local scalar implicit step is elementary: write F=psi_c-2/k^2+H; C1 continuity makes |partial H/partial psi_c|<1/2 in a small closed interval. For sufficiently small delta,eta the map psi_c -> 2/k^2-H maps that interval into itself and contracts. Its unique fixed point gives F=0. Combining it with (2) produces an actual self-gravitating two-fluid solution with no external mass/charge and finite total mass. The core stays positive until its simple first zero; psi stays positive, and the exterior neutral tail is t^-5. Both actual static currents are separately conserved.

The first zero, masses, potentials and enclosed-field maximum tend continuously to their base values. The statement is an existence theorem for **some sufficiently small positive** delta and eta; no explicit universal numerical threshold is inferred from the shooting sample.

## 4. Positive full radial density/Gauss energy on a smaller open branch

Use physical radii in this section. For mass perturbations u=delta M_c and v=delta M_s, the exact same radial reduction as in `../core/PROOF.md` gives

\[
 Q={K\over2\pi}\int_0^{R\ell}{u'^2\over r^2}dr
 +U_s-G\int_0^\infty{(u+v)^2\over r^2}dr
 +G\alpha\int_0^{R\ell}{u^2\over r^2(1-x)^2}dr,
\]

where u=0 outside the charged body and

\[
 U_s=\int {c_{s,N}^2\over4\pi\rho_s r^2}v'^2dr,
 \quad c_{s,N}^2={-\Phi\over5},\quad
 I_u=\int_0^{R\ell}{u^2\over r^2}dr.                  \tag{5}
\]

The electric Hessian is at least its Maxwell value. Thus it cancels alpha of the core's own gravity and leaves G_eff=G(1-alpha)>0. The charged free-boundary finite-inertia domain has u(0)=u(R ell)=0; core mass is conserved. Put u=rv. Integration by parts gives

\[
 \int_0^L{u'^2\over r^2}dr
 =\int_0^L\left(v'^2+{2v^2\over r^2}\right)dr
 \ge{\pi^2+2\over L^2}\int_0^L v^2dr.               \tag{6}
\]

The Dirichlet inequality used here follows directly by expanding the nonnegative integral integral[v'-(pi/L)cot(pi r/L)v]^2 and taking compact approximants, giving integral v'^2 >=pi^2/L^2 integral v^2. Thus no numerical eigenvalue establishes (6).

Consequently the isolated charged-core part is at least kappa G_eff I_u, with

\[
 \kappa={K(\pi^2+2)\over2\pi L^2G_{\rm eff}}-1,
 \quad L=R\ell.                                      \tag{7}
\]

At the exact base radius L0^2=pi K/(2G_eff), kappa=2/pi^2>0. This margin persists by continuity of the actual equilibrium radius.

The neutral weighted Schur bound, now applied to its actual self-potential, gives

\[
 G\int_0^\infty{v^2\over r^2}dr\le q_s U_s,
 \quad q_s=5\sup_r{(-\Phi_s)\over(-\Phi)}.
\]

The neutral potential is O(delta) relative to the core potential uniformly on the branch: inside the body this follows from the bounded interior solution and positive core potential; outside it follows from the weighted exterior contraction and finite mass. Hence q_s tends to zero as delta tends to zero. Cauchy-Schwarz bounds the cross term by 2sqrt(G q_s I_u U_s). Therefore

\[
 Q\ge\kappa G_{\rm eff}I_u+(1-q_s)U_s
                    -2\sqrt{Gq_s I_uU_s}>0              \tag{8}
\]

for nonzero density perturbations whenever

\[
 q_s<1,\quad \kappa>0,\quad
 \kappa G_{\rm eff}(1-q_s)>Gq_s.                       \tag{9}
\]

These strict inequalities hold on a sufficiently small positive subbranch because their base limits are (q_s,kappa)=(0,2/pi^2). This establishes a coercive radial density/Gauss quadratic form, not just one trial direction or a fixed-core neutral estimate. Positive radial kinetic energy supplies a positive conserved quadratic comparison energy for suitable finite-energy linear solutions. This does not prove nonlinear PDE existence, all angular sectors, strong hyperbolicity, or metric/gauge health in the full covariant theory.

## 5. Local principal gate can be included without assuming a fixed neutral inventory

The chosen EOSs have h_c(1-s_c^2)=rho_c c^2 and h_s(1-s_s^2)>=rho_s c^2. With the actual mass weights in the varied two-current frame, h_*>= (rho_c+rho_s)c^2. Define epsilon=2K rho_*/c^2. Exact normalization gives D0^2/(rho_*c^2)=alpha epsilon/eta^2, hence

\[
 {h_{\rm crit}\over h_*}\le
 {\alpha\epsilon\eta\,m_c(t)^3
 \over t^6[\theta(t)+\delta\psi(t)^5](1-x)^2}.        \tag{10}
\]

For each positive-delta equilibrium already constructed, the right-hand coefficient of epsilon is bounded: it vanishes at the center as t^3, has a finite charged-edge limit because the neutral density is positive, and decays as t^-1 at infinity. Therefore a sufficiently small positive epsilon supplies a strict all-finite-radius gate margin. K and rho_* can realize epsilon and eta independently by setting ell=b_q c^2 epsilon/(a0 eta), then K=2pi G ell^2 and rho_*=epsilon c^2/(2K); K_s sets delta. This is parameter choice, not a derived abundance or fitted prediction. Weak gravitational and pressure potentials also follow as epsilon tends to zero.

At the charged edge the two-current mode formula is understood on either occupied side and by the reduced neutral limit; this is not a theorem about charged-fluid free-boundary hyperbolicity. At zero electric field an explicitly specified occupied-phase response patch is still needed. The noncompact neutral stock prevents a finite empty-vacuum crossing but does not derive the asymptotic frame or vacuum phase.

## 6. Scope and checks

The exact checks and bounded shooting example are in `check_stiff_core.py`; its contract separates algebra, finite integration, and the qualitative existence proof. Numerical shooting uses a finite outer match with an analytic first-Picard tail and records its contraction error, tolerances and truncation. It is evidence about that implementation and sample, not a certified interval ODE proof or a quantitative replacement for the sufficiently-small theorem.

This construction addresses a genuine failure of the soft critical co-Plummer family by changing to a fixed stiffer core EOS and a subcritical charge ratio. The critical original model, microscopic selection, abundance, full angular stability, conversion, cosmology, empirical tests and full Einstein/current well-posedness remain open. A subcritical branch must not be substituted into the old critical-charge algebraic galaxy law.
