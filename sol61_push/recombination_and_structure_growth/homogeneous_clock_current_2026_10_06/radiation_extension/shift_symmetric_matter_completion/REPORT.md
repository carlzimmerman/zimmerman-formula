# Dust-density stealth square fails the short-wavelength matter test

For the pure positive square

    Delta L=Z(rho_d;rho_v)/2 [X-B(rho_d;rho_v)]^2,
    X=-grad(phi)^2/2, rho_d=m n, B=Xbar_d,

a finite smooth epoch with Z>0, rho_d>0, b=B'(rho_d)!=0, M>0, Theta!=0 and finite kappa>0 has a constrained dust branch

    omega_d^2/p^2 -> -rho_d Z b^2 < 0,  p -> infinity.

The full clock–dust–radiation characteristic establishes this result after lapse, shift and dust-density elimination. Clock mixing does not cancel the negative dust compressibility. This is a scoped no-go for the declared pure dust-density square as a healthy arbitrarily-short-wavelength repair; it is not a no-go for other operators or a claim that an unstable mode necessarily lies below an unspecified EFT cutoff.

## Background and family map

The parent logKGB + finite-A acceleration response is unchanged. In unitary clock gauge, its quadratic acceleration term is kappa M(grad nu)^2; W=O(|a|^3/A) has no quadratic contribution. Set q=phidot>0. On the chosen conserved FRW history, dust rho_d decreases monotonically, so one may define B(rho_d)=X_background along that history. Delta L and its X and density first derivatives vanish on X=B. The background matter and scalar equations are unchanged, including the extra shift current, which is zero there. This is a designer background construction, not an explanation of the history or current boundary data.

There is no explicit phi dependence, so the exact scalar shift current remains conserved. If B=q_star(rho_v)^2 F(rho_d) and Z=q_star(rho_v)^(-4) Znorm(rho_d), the algebraic action-family transformation phi->s phi, rho_v->rho_v-2c ln s sends B->s^2 B and Z->s^(-4)Z, leaving this square invariant. This transformation changes the explicitly rho_v-dependent interaction functions along with the action parameter. It is not automatic physical self-adjustment to new independent matter vacuum energy at fixed couplings.

## Covariant dust variation and the conservation dictionary

Use an irrotational Schutz current with the potential sign chosen to match the parent's positive pi dot(v_d) convention:

    S_d+square=integral[-sqrt(-g)m n+J^mu partial_mu ell
                                +sqrt(-g)Delta L],
    J^mu=sqrt(-g)n u^mu, u^mu u_mu=-1.

This ell is minus the potential in the source convention cited below. At fixed metric, partial n/partial J^mu=-u_mu/sqrt(-g). Varying ell gives partial_mu J^mu=0 exactly. Varying J gives

    partial_mu ell=-(m-Delta L_n)u_mu.

The effective chemical potential is m-Delta L_n. The square therefore changes the dust force law away from the chosen trajectory. Particle number remains conserved; dust is not a separately conserved minimally coupled stress tensor once the interaction is added. Total covariant stress and scalar shift current remain conserved. Radiation retains its independent minimal P(Y)=lambda Y^2 action.

At the trajectory, Delta L_X=Z(X-B), Delta L_rho=-Z b(X-B)+O((X-B)^2). At first order put delta Y=delta X-b delta rho_d. Then

    delta[(m-Delta L_n)/m]=Z b delta Y,
    delta p_effective=rho_d Z b delta Y.

This density response has the sign of negative compressibility when the clock norm is held fixed: delta p=-rho_d Z b^2 delta rho_d. These equations alone do not prove the coupled instability; the full constraint calculation below does.

For the covariant density current at a comoving background, first-order n is J^0/sqrt(gamma). Lapse and shift cancel out of this expression; matter spatial current enters only at second order. With N=1+nu, gamma_ij=a_FRW^2 e^(2zeta)delta_ij, coordinate-density momentum pi=m delta J^0/a_FRW^3,

    delta rho_d=pi-3rho_d zeta,
    delta X=-q^2 nu,
    Delta L_2=Z/2 [q^2 nu+b(pi-3rho_d zeta)]^2.

Neither delta Y nor its square contains a matter velocity or the shift at this order. delta Y is gauge invariant because Xdot=b rhodot on the background. Z' does not contribute quadratically because the background square and first variations vanish.

## Actual reduced three-pair action

Freeze smooth coefficients at a finite epoch to form the local high-frequency characteristic. Keep the raw parent coefficients Sigma,Theta, with S=Sigma+kappa M p^2. The retained scalar action per a_FRW^3 is

    -3M zetadot^2+S nu^2+6Theta nu zetadot
       -2Theta nu t+2M zetadot t+M p^2zeta^2+2M p^2nu zeta
       +3rho_d zeta nu+pi(v_d_dot-nu)-rho_d p^2v_d^2/2+rho_d v_d t
       +C_r(v_r_dot-Hv_r-nu)^2+3R_r zeta(v_r_dot-Hv_r)
       -R_r p^2v_r^2/2+R_r v_r t
       +Z/2[q^2nu+b(pi-3rho_d zeta)]^2.

Here t=Delta beta/a_FRW^2, physical p=k/a_FRW, R_r=rho_r+p_r>0, C_r=R_r/(2c_r^2), c_r^2=1/3. The H v_r term is retained rather than freezing radiation's field-normalization dictionary. Volume redshifting and time derivatives of smooth coefficients affect lower WKB orders, not the leading characteristic derived here.

The unchanged exact shift equation is

    nu=(M/Theta)zetadot+rho_d v_d/(2Theta)+R_r v_r/(2Theta).

The lapse equation still solves t with nonzero coefficient -2Theta; no omitted lapse constraint removes a scalar pair. Since b and Z are nonzero, pi now has an algebraic equation

    pi=3rho_d zeta-(v_d_dot-nu)/(Z b^2)-q^2nu/b.

Its elimination is invertible and leaves three second-order scalar coordinates (zeta,v_d,v_r). The exact resulting dust terms, including cancellation against the gravity+dust tadpole, are

    3rho_d zeta v_d_dot-(v_d_dot-nu)^2/(2Z b^2)
       -(q^2/b)nu(v_d_dot-nu)-rho_d p^2v_d^2/2.

The negative velocity-square sign in this representation is suggestive, but the following high-p imaginary-frequency root, rather than an isolated canonical sign, establishes the classical gradient instability.

## Exact high-p determinant and physical root

For the reduced L, define velocity Hessian K_ij=L_(dot u_i dot u_j), field Hessian V_ij=L_(u_i u_j), and antisymmetric one-derivative matrix G_ij=L_(dot u_i u_j)-L_(u_i dot u_j), where u=(zeta,v_d,v_r). With Fourier convention exp(-i omega t), the frozen Euler matrix is

    E=-omega^2 K-i omega G-V.

Set omega=p x. Direct exact algebra gives the leading full characteristic

    det E = p^8 [2 kappa M^3/(Theta^2 Z b^2)]
                  x^2(2C_r x^2-R_r)(x^2+rho_d Z b^2)+O(p^6).

The script derives this from the unreduced action rather than postulating a dust sound speed. In particular all apparent kappa p^2 matter-potential terms and the large shift/velocity mixing cancel correctly in the determinant. The H-dependent radiation normalization drops out of this leading coefficient.

The two nonzero principal branches are therefore

    x_r^2=R_r/(2C_r)=1/3,
    x_d^2=-rho_d Z b^2.

The x=0 factor represents the differently scaled clock branch and does not annul either simple nonzero dust root. For positive finite Z,rho_d and nonzero b, x_d=+/- i sqrt(rho_d Z)|b| are simple roots of the leading polynomial; the implicit-function theorem gives actual frozen large-p roots approaching them. Smooth finite background time dependence supplies subleading WKB corrections, so the leading negative omega^2/p^2 is unchanged. The frozen characteristic has even powers in p, hence omega_d^2=-rho_d Z b^2 p^2+O(p^0) there; the time-dependent statement is the principal asymptotic limit, not that exact frozen subleading remainder.

This branch carries a genuine dust density perturbation. At high p the clock constraint/clock equation enforce a suppressed lapse for that branch; pi dynamics then has pi_dot approximately -rho_d p^2 v_d and v_d_dot approximately -Z b^2 pi. Combining gives pi_ddot approximately +rho_d Z b^2 p^2 pi. Gauge-invariant delta Y and the constrained characteristic make this a physical short-wavelength instability, not merely an IR canonical ghost diagnosis. No quantum vacuum-decay conclusion is drawn.

## Exact scope and next door

The result assumes the declared operator is valid in the short-wavelength regime. With an EFT cutoff one must separately show a range H, other background rates << p < cutoff in which the asymptotic branch is admitted; this report provides no cutoff or observational growth rate. b=0, Z=0, kappa=0, Theta=0, extra pressure or extra operators are outside the theorem's hypotheses. The theorem excludes the pure positive density square as a universally stable UV repair, not all shift-symmetric completions. A negative Z reverses the density response but is not the proposed positive clock-kinetic repair.

A square using a radiation scalar density instead of dust's current density is a separate possible route: its density perturbation includes a radiation time derivative, so it changes the velocity matrix rather than introducing this positive pi^2 term. Its full mixed gradient and sourced dynamics have not been checked here. It remains a new door, not a successful completion. No statement about a0/H or 32pi follows from this calculation.

## Evidence and primary source

checks.py verifies background stealth, family rescaling, the density dictionary, exact shift and density elimination, the full three-pair determinant and its roots. Bounded numerical frozen-coefficient matrices illustrate convergence to the imaginary root; these coefficient samples are algebra controls, not fitted on-background cosmologies. The universal sign follows from the exact determinant and stated hypotheses, not the sample count. Three controls assert a stable dust root, discard the density perturbation, or omit matter momentum in the shift equation.

The dust current conventions were checked directly against De Felice–Frusciante–Papadomanolakis, arXiv:1609.03599v2 (13 March 2017), equations III.1–III.12, https://arxiv.org/pdf/1609.03599v2 . That primary source treats minimal fluids; our new interaction, effective chemical potential and characteristic are derived here and are not attributed to its minimal-fluid stability theorem. The versioned HTML fetch failed; the full PDF was successfully read. Parent raw action/source inputs and actual hashes are recorded in provenance.json, sources.json and the standard fresh manifests. No frozen parent evidence was modified.
