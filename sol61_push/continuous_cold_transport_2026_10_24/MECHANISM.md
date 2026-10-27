# A continuous cold field that clumps: what the equations must supply

Status: conditional candidate and derived diagnostics, not a completed physical theory. Classical-field language does not establish the absence of a particle interpretation or non-gravitational interactions. Here “collisionless” means no binary collision term is assumed; gravitational interactions and wave transport remain present. “Cold” means small pressure relative to rest energy, not zero motion or zero stress after collapse.

## 1. The three descriptions and their first failures

Pressureless Euler–Poisson has

    partial_t rho + div(rho u) = 0,
    (partial_t + u.grad)u = -grad Phi,
    lap Phi = 4 pi G (rho + rho_b).

Even without gravity, u(q,0) = -a q gives x(q,t) = q(1-at), rho = rho0/(1-at) in one dimension before crossing. The velocity description fails at t=1/a. This is not core formation or cooling.

A collisionless phase-space continuum instead evolves

    partial_t f + v.grad_x f - grad Phi.grad_v f = 0.
    rho = integral f dv; rho u = integral v f dv.
    partial_t(rho u_i) + partial_j(rho u_i u_j + Pi_ij) = -rho partial_i Phi,
    Pi_ij = integral (v_i-u_i)(v_j-u_j) f dv.

Two equal counterstreams have u=0 but Pi_xx=rho v0^2. Dropping Pi after streams meet removes real support. This continuum can describe a classical field's kinetic limit only after deriving that limit; calling f a field does not derive a new dark sector or solve the galaxy-law double count. Phase mixing can relax coarse observables without collisions; fine-grained evolution remains reversible.

The third route supplies a finite dispersive stress explicitly. It is the candidate developed below.

## 2. An explicit wave candidate, with its new scale disclosed

Take rho=|psi|^2 as a mass density; eta has units length^2/time. With Newtonian potential zero at infinity, use

    S = integral dt d^3x { (i eta/2)(psi* psi_t - psi psi*_t)
        - eta^2 |grad psi|^2/2 - U(rho) - Phi(rho+rho_b)
        - |grad Phi|^2/(8 pi G) }.

Varying psi* and Phi gives

    i eta psi_t = -eta^2 lap psi/2 + [Phi + U'(rho)] psi,
    lap Phi = 4 pi G (rho+rho_b).

For psi=sqrt(rho) exp(i S_phase/eta), wherever rho>0,

    u = grad S_phase,
    rho_t + div(rho u)=0,
    (partial_t+u.grad)u = -grad[Phi + U'(rho) + Q],
    Q = -(eta^2/2) lap sqrt(rho)/sqrt(rho),
    p = rho U'(rho)-U(rho).

Q is dispersive stress, not an inserted cooling force. The wave equation remains the primary description at density nodes, where these fluid variables break down. Vortices and multiple spatial modes are needed for generic angular momentum. This is a Newtonian candidate; a stable covariant completion, cosmological history and the original acceleration law are unproved.

eta is NEW unless derived from the existing action. Writing eta=hbar/m produces the usual wave-dark-matter parameterisation; leaving eta classical does not remove the scale or prove a nonparticle ontology. U is also new microphysics unless specified/derived. Set U=0 for the following limited control.

Linearising the corresponding nonrelativistic cosmological fluid about a homogeneous background gives the local subhorizon diagnostic

    delta_tt + 2 H delta_t + [c_s^2 k^2/a^2 + eta^2 k^4/(4 a^4) - 4 pi G rho_bar] delta = 0,
    c_s^2 = rho_bar U''(rho_bar).

Here k is comoving and rho_bar is the self-gravitating wave component; baryon perturbations would supply a coupled source, not disappear into rho_bar. For U=0 the instantaneous physical Jeans wavenumber is (16 pi G rho_bar/eta^2)^(1/4). Gravity can amplify sufficiently long wavelengths while dispersion opposes short wavelengths. Thus the same eta that supports cores must also pass early-growth tests; core support is not permission to ignore cosmology. This diagnostic is not a derivation of a consistent cosmological background from the Newtonian action above.

## 3. Support is possible, but formation is a separate question

For an isolated, nonrotating Gaussian rho=M exp(-r^2/R^2)/(pi^(3/2) R^3), the exact energy of this trial family at U=0 is

    E(R) = 3 eta^2 M/(4 R^2) - G M^2/(sqrt(2 pi) R).
    R_star = 3 sqrt(2 pi) eta^2/(2 G M).

E'(R_star)=0, E''(R_star)>0 and E(R_star)<0. Thus a stable radius exists within this trial family; it is not a proof of dynamical formation, a full stability theorem or an exact soliton profile. For a universal eta the family obeys M R_star=constant, so four radii and masses cannot be independently chosen.

Alternative pressure support U=g rho^2/2, g>0 gives p=g rho^2/2. In the spherical pressure-dominated limit the n=1 polytrope has R=pi sqrt(g/(4 pi G)), independent of mass. It supplies support but introduces g, and does not by itself export energy. Neither pressure nor dispersion may be substituted into the original frozen action without a new derivation and new tests.

## 4. How a collisionless core can cool: export, not disappearance

For isolated self-gravity and U=0,

    E_total = integral [eta^2 |grad psi|^2/2 + rho Phi_self/2] d^3x

is conserved. A forming core can become more bound while an outer envelope or outgoing waves gain energy. This is a conservative redistribution. A prescribed damping term silently removes that ledger unless its receiver is evolved. With live baryons include their energy, recoil and heating; with prescribed time-dependent Phi_b include integral rho partial_t Phi_b d^3x as external work.

Gravitational cooling exists in other scalar-field systems (Seidel & Suen, PRL 72, 2516, 1994; https://arxiv.org/abs/gr-qc/9309015). That is evidence for the possibility of collisionless scalar cooling, not evidence for its rate, abundance or four-dwarf selectivity in this candidate or v3s. Previous local weak-radiation calculations found inadequate cooling within their tested regime and cannot be overwritten by that analogy.

In the dilute free far zone, an outgoing mode psi proportional to exp(i k r-i omega t+i m phi)/r has

    omega=eta k^2/2; epsilon=eta omega;
    mass flux F_M=eta Im(psi* partial_r psi),
    F_E=epsilon F_M; F_Jz=m eta F_M; F_Jz/F_E=m/omega.

These are time-averaged asymptotic mode relations with energy measured above escape, not the rest-energy flux. At finite radius gravitational binding and stress fluxes must be retained. Integrated orthogonal outgoing modes add their fluxes.

Consequences:

* Spherical (m=0) cooling exports no Jz. A spherically symmetric calculation cannot demonstrate spin shedding.
* If only modes |m|<=m_max are excited, |Delta Jz|<=eta m_max M_out. If their epsilon<=epsilon_max, E_out<=epsilon_max M_out. A finite available outgoing mass therefore constrains both budgets. These bounds do not apply to a separate massless radiation channel.
* For a purely ballistic advected envelope crossing radius <=R, Cauchy–Schwarz gives J_out^2 <= 2 M_out R^2 K_out, where K_out is kinetic energy AT that surface, not energy at infinity. Tangential stress/wave transport requires its own flux ledger and is not covered by this ballistic bound.
* A low-frequency mode may have large m/omega, but its excitation amplitude, propagation and escape must be derived. A favourable ratio alone proves no transport rate.

## 5. The missing phase equation

A two-phase phenomenology would need rho_s,t+div j_s=-Gamma and rho_n,t+div j_n=+Gamma, along with momentum and energy exchange that cancel in the total. A Landau condition v>min(omega/k) identifies an energetically accessible excitation channel under its assumptions; it determines neither Gamma nor complete conversion of the condensate. PH1's A6 explicitly marks its transition POSITED. Its failed growth and isolated-galaxy double-count controls remain failures. Merely adding Gamma or choosing different phase fractions per dwarf is a fit, not a mechanism.

## 6. The discriminating next experiment

Use one explicitly chosen action and common parameters, and a nonspherical rotating initial cloud with a live envelope. First compare no-spin, opposite-spin and finite-spin controls. Track core, bound envelope and escaping M,E,J, plus field/gravitational stress and any baryonic work. Require convergence under resolution, time step, box size and boundary placement; an absorber must report everything it removes. Compare core contraction against directly measured outgoing nonzero-m modes. No cold mass may disappear merely to satisfy a desired profile.

Then inherit Draco, Sextans, Fornax and Leo I inputs and frozen target intervals from one pinned data/normalisation model. Derive initial supply/spin/history from shared physics; do not choose four unconstrained core fractions. A pass requires simultaneous central masses/profiles, total supply, stellar heating, conserved transport and acceptable isolated-galaxy/cosmological controls. If selecting eta from one dwarf, label it calibration and hold out the others. If it fails, the result rejects that action/parameter/history class, not all classical fields.

There is a further coupling gate. Simply sourcing an unchanged spherical AQUAL law with both components yields g mu(g/a0)=G(M_b+M_c)/r^2, not the original baryon-only relation. A cold halo then boosts the law as well as supplying mass. Before interpreting any four-dwarf contraction as a success, derive from one action whether and how that extra response is avoided in isolated galaxies. This is precisely the double-counting problem PH1 exposed; writing a Schrödinger equation alone does not cure it.

Open continuation: derive eta and the coupling to the acceleration-law sector from an action, or explicitly accept a new scale and test it. No heavy experiment was launched in this packet; existing shared L1 work is not duplicated.
