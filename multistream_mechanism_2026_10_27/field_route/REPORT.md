# Field route: reciprocal gate terms and a conditional mediator

2026-10-27. Bounded investigation from HEAD e6d278b74755885d9f62106becef5d7b753c512c, with concurrent work elsewhere.
Only this directory was written. No halo simulation, cosmological refit, or live lane was modified.

**Result:** a positive-energy local mediator can be written and can acquire a stable nonzero value above a kinetic-stress threshold. This does not derive the required Lambda normalization, make the threshold a stable halo endpoint, or supply the cold-field kinetic limit. A direct gate multiplying an internal-energy density has unavoidable reciprocal momentum and pressure terms. In the logotropic example these terms can reverse the pressure sign or make the local kinetic coefficient negative. Treating the gate as a multiplier on the force alone is not a conserving realization of that energy.

## 1. A conditional kinetic parent with a healthy local scalar branch

Use a continuum of cold-stream characteristics, not an assertion about particle ontology. Densities rho_s obey continuity, vbar is their density-weighted velocity, and K_v = sum_s rho_s |v_s-vbar|^2/2. At fixed densities consider the nonrelativistic Lagrangian density

    L = rho |vbar|^2/2 + Achi(chi) K_v - rho Phi
        + (chidot^2 - cchi^2 |grad chi|^2)/2 - U(chi),
    Achi = 1 + beta chi^2/(3 M^2),
    U = V0 + m^2 chi^2/2 + lambda chi^4/4,
    beta, m^2, M^2, lambda > 0.

The relative canonical momenta are p_s-vbar = Achi(v_s-vbar). The exact local Legendre transform is

    H = rho |vbar|^2/2 + K_p/Achi + pi_chi^2/2
        + cchi^2 |grad chi|^2/2 + U(chi) + gravitational terms.

The kinetic metric is positive because Achi>0. This statement concerns the local kinetic and mediator sectors, not positivity of self-gravitating total energy or general relativistic health. It is Galilean invariant because only relative velocities enter Achi K_v. Conservation follows from varying the same action, including both cold and chi equations.

At prescribed K_p, the scalar effective potential is W=K_p/Achi+U. Its mass at chi=0 is

    m_eff^2 = m^2 - 2 beta K_p/(3 M^2).

Writing I0=2K_p/3 at chi=0 gives the activation threshold

    Istar = m^2 M^2/beta.

For K_p above threshold, y=chi^2>0 is uniquely determined by

    m^2 + lambda y = 2 a K_p/(1+a y)^2,    a=beta/(3 M^2).

The left-minus-right side has derivative lambda+4a^2 K_p/(1+a y)^3>0. At that root W_chichi=2y times this derivative is positive. Thus this is a locally stable scalar branch, conditional on the prescribed kinetic state. It does not prove stability of the coupled cold distribution or a halo.

The conjugate isotropic kinetic stress on this branch is 2K_p/(3 Achi), which equals

    (M^2/beta) (m^2+lambda y)(1+a y) >= Istar.

It is not clamped to Istar. Above activation, physical velocity moments and canonical momentum moments also cease to coincide. A halo calculation must use the stress obtained by variation of the complete action, not keep using the bare Jeans moment unchanged.

This parent reads the trace of random motion: sheets and filaments can activate it. Replacing it by a determinant/full-rank coupling is an additional construction whose Legendre positivity must be checked, not inherited from this example. A covariant stream-current completion and a derivation of these streams from the owner's cold field remain absent.

**An unsafe shortcut:** writing the Hamiltonian interaction as -beta chi^2 I/(2M^2), while retaining an unchanged bare kinetic energy 3I/2, gives after scalar minimization

    H_eff = 3I/2 + V0 - (beta I/M^2-m^2)^2/(4 lambda)

on the active branch. This goes to minus infinity as I increases. The exact Legendre transform above avoids that particular instability; simply reading a velocity-dependent Lagrangian coupling as a potential does not.

## 2. The Lambda coefficient is still an input

The threshold m^2 M^2/beta is independent of the additive vacuum energy V0. Shifting V0 changes gravitation but not the local scalar field equation or this threshold. Therefore this class of minimally coupled additive-vacuum parents does not explain Istar proportional to the measured vacuum density.

One may prescribe m^2=alpha Lambda and M^2=M_Pl^2, with reduced M_Pl^2=1/(8 pi G), in c=1 units. Then Istar=(alpha/beta) rho_Lambda. But alpha/beta is free. Matching the canonical Burkert stress target requires

    alpha/beta = C/(16 pi^2) = 0.005231383918936,
    C = 0.826107036001911.

That matching is target calibration unless the ratio and profile follow from an independent parent. C is a shape-dependent Jeans coefficient, not an available universal constant of the action. The alternative acceleration footing must not be assigned the same ratio by an identity.

A multiplicative potential V=u_Lambda U(chi/M) can put a vacuum amplitude into the scalar mass, but an independently allowed additive vacuum term changes the gravitationally measured Lambda without changing the threshold. A symmetry or renormalization condition tying all these coefficients is a new obligation. A curvature mass xi R chi^2 instead senses R=(rho-3p+4u_Lambda)/M_Pl^2 in GR: the cold rest density and baryonic trace enter, so it is not a pure multistream/vacuum trigger. Cancelling their contribution needs further couplings.

## 3. A stress-gated logotropic energy has reciprocal terms

This section supplies the precise obstacle to multiplying the root agent's logotropic force by a gate. Let f(x,p) be a mass distribution in canonical specific momentum. Define

    rho = integral f dp,  pbar = integral p f dp/rho,
    Pi = integral f (p-pbar)(p-pbar)^T dp,  I=(det Pi)^(1/3),
    u(rho)=-A[ln(rho/rho_ref)+1],   e_int=u(rho) g(I).

For positive-definite Pi, varying f gives

    delta Pi/delta f = (p-pbar)(p-pbar)^T,
    delta I/delta f = (I/3)(p-pbar)^T Pi^-1(p-pbar).

Therefore a Vlasov Hamiltonian containing integral e_int dx must use

    h_int = g u'(rho)
            + u g'(I) (I/3)(p-pbar)^T Pi^-1(p-pbar).

The second term is compulsory. It is the reciprocal response to the state-dependent gate. A force from the first term alone is not generated by that Hamiltonian. For an isotropic state Pi=I Identity, its momentum-dependent contribution changes the characteristic velocity coefficient to

    1 + 2 u g'(I)/3.

If that coefficient is negative, this simple local kinetic sector has lost convexity. This is a necessary-health diagnostic, not a complete dispersion or ghost analysis. On the active plateau g=1,g'=0 the extra term vanishes; the issue is specifically the transition and the energy reference it carries.

For an isotropic adiabatic affine dilation x->a x, p->p/a, rho->rho/a^3, Pi->Pi/a^5. The interaction pressure derived from total energy variation is

    P_int = g P_log + (5/3) I g'(I) u,
    P_log = A ln(rho/rho_ref).

With g=I^3/(Istar^3+I^3), g'(Istar)=3/(4 Istar). Thus, at the threshold, the velocity coefficient is 1+u/(2Istar). A constant additive shift of u now affects forces and kinetic convexity. For rho=I=Istar=1 and A=0.4, choosing ln rho_ref=-10,0,10 gives this coefficient -1.2,0.8,2.8. These are alternative interacting models, not gauge-equivalent choices.

In the ungated theory, rho_ref->exp(k)rho_ref shifts u by Ak and can be compensated by V0->V0-Ak. Once gated, the same compensation leaves Ak(g-1), a state-dependent interaction. In a mediator gate g(chi), an additional counterterm -Ak g(chi) in its potential is required to preserve the theory; it cannot be dropped as a harmless energy reference. The background-vacuum/active-logotrope matching has to specify this term and the phase free-energy offset.

The matrix formula need not be used at rank deficiency: for this particular determinant gate, the derivative can be written with the adjugate and denominator (Istar^3+det Pi)^2. Whether the kinetic branch remains healthy through such states is still a separate test.

## 4. Exact vacuum exchange is more restrictive than mediator radiation

X54's specified stress is T_vac^{mu nu}=-V g^{mu nu}; its exchange is geodesic, Q_c^nu=Q u_c^nu, with no momentum transfer in the cold frame. Conservation then requires Q_c^nu=grad^nu V. Consequently h^mu_nu grad^nu V=0. A spatially varying halo stress gate cannot be independently inserted into Q while keeping that vacuum stress and zero momentum transfer.

In differential-form language, dV=Q u_flat implies d(Q u_flat)=0. Wedge with u_flat gives Q u_flat wedge du_flat=0. Where Q is nonzero, the chosen cold flow must be hypersurface orthogonal; a generic vortical multistream mean flow does not satisfy this. This is a consistency condition on that exact-vacuum/geodesic ansatz, not a ban on a general mediator.

A propagating chi can exchange energy conservingly because it also carries kinetic, gradient, and momentum stresses. It is not exactly w=-1 during the exchange. X54's homogeneous Q=xi H rho_c and Q=xi H rho_DE constraints do not by themselves grade such a post-collapse, momentum-carrying mechanism. Conversely, X54 is not evidence that arbitrary local halo heating is allowed.

## 5. Primordial pressure and transport direction

For a nonrelativistic freely redshifting primordial dispersion, sigma=sigma_today/a and rho=rho_today/a^3, so an isotropic stress amplitude grows as a^-5. An amplitude threshold proportional to constant Lambda is crossed sufficiently early for every nonzero present dispersion if the same cold phase persists far enough backward. The exact-cold limit avoids this, but is not robust under adding a finite thermal width.

Using only X54's own xi=0 DES-SN5YR refit (h=0.6847, omega_c=0.11859, Omega_m=0.3009) gives rho_c0/rho_DE0=0.361833. For the canonical target Istar/u_Lambda=0.00523138, demanding primordial pressure below threshold gives

    sigma_today < c sqrt[0.00523138/(0.361833(1+z)^5)].

At z=1090 this is 0.917 m/s today, or 1.00 km/s at recombination. At z=50000 it is 6.45e-5 m/s today, or 3.22 m/s then. These are illustrative necessary off-state bounds for this amplitude criterion, not observational measurements or a refit. A finite onset of the cold phase changes the interval where this scaling applies.

A passive radiative sink does not automatically create the desired core. For a fixed-mass homologous virial core, E proportional to -1/R and P proportional to R^-4 imply Pdot/P=4 Edot/E. Exporting binding energy raises pressure, so high-pressure cusp expansion requires energy delivered to the core or a different conservative structural response. This does not obstruct damping of positive-energy perturbations about an already stable core: the root agent's reciprocal wave outlet addresses that distinct question.

## 6. Check of the root agent's reciprocal mode outlet

For the supplied coupling L_int=g zeta n^2 Dchi, an advected material phase label satisfies Dzeta=0. Let the displacement be q(t) xi(x). Then delta n=-q div(n0 xi), v=qdot xi, and delta zeta=-q xi dot grad zeta. Expanding to quadratic order and integrating the chi time derivative by parts gives the spatial coefficient

    2 zeta n0 div(n0 xi) - div(zeta n0^2 xi)
        + n0^2 xi dot grad zeta = zeta n0^2 div xi.

Thus J=g zeta n0^2 div xi is correct under those assumptions. A fixed spatial zeta instead retains the extra term -g n0^2 xi dot grad zeta. Sharp interfaces should be understood as a consistent smooth-interface limit, including any density jump; this avoids undefined products of distributions.

For the projected Lagrangian

    L2 = mu(qdot^2-omega^2 q^2)/2
         + integral(chidot^2-cchi^2|grad chi|^2)/2 + qdot integral J chi,

the momenta are p_q=mu qdot+integral J chi and pi_chi=chidot. Hence

    H2 = (p_q-integral J chi)^2/(2mu) + mu omega^2 q^2/2
         + integral(pi_chi^2+cchi^2|grad chi|^2)/2.

This is nonnegative for mu>0, omega^2>0; zero-mode/boundary conventions determine strict positivity. Variation yields chi_tt-cchi^2 lap chi=J qdot and mu qddot+mu omega^2 q=-integral J chidot. The reciprocal source cancels in the total-energy derivative, leaving the wave flux at the boundary. Outgoing radiation can therefore remove positive perturbation energy while conserving total energy. This check does not derive the equilibrium, phase formation, J's coefficient, or the full spectrum after mode truncation. No new numerical run of this outlet was performed by this subagent.

## Checks, source scope, and remaining obligation

The bounded run in run/ completed in under one second; its manifest validates. Eight independent finite weight perturbations reproduce h_int with maximum absolute error 1.18e-10. An independent affine energy derivative gives P_int=-0.607963383729 against the formula -0.607963383761. The omitted reciprocal term is -0.678166775676; the gate-times-log-pressure term alone has the opposite sign in this example. Symbolic checks establish the scalar linear threshold, its V0 independence, and the unsafe shortcut's negative large-I quadratic coefficient. The primordial bounds are also saved. These finite checks support the displayed algebra; none evolves a halo.

Primary sources checked on 2026-10-27:

- De-Santiago, Wands and Wang, arXiv:1209.0563v1, equations 1–6: exact-vacuum stress and gradient exchange. Their Q labels vacuum gain; Q_c here is its negative. https://arxiv.org/pdf/1209.0563v1
- Morrison, *Hamiltonian Description of Vlasov Dynamics*, Transport Theory and Statistical Physics 29, 397–414 (2000), section 3, equation 18: noncanonical Vlasov bracket with functional Hamiltonian. This supports the conservative kinetic framework, not the proposed field-to-kinetic completion. https://web2.ph.utexas.edu/~morrison/00TTSP_morrison.pdf
- Hinterbichler and Khoury, arXiv:1001.4525v3: adjacent symmetry-breaking screening idea only. The pressure-coupled kinetic parent above is a construction in this investigation, not a result of that paper. https://arxiv.org/abs/1001.4525v3

No external source was downloaded or cached. Local source hashes are in INPUT_HASHES.txt; execution input hashes are also in run/manifest.json.

**Next decisive obligation:** join a healthy kinetic/multistream field limit to the stable active-phase core and its reciprocal outlet, specifying the entire transition energy (including reference-dependent terms). Derive the coefficient linking its phase energy to the total gravitating vacuum energy. Until that is done, the construction has conserving conditional ingredients, but its core surface density remains a calibrated target.
