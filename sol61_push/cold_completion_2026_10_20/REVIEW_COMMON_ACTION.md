# Independent reconstruction review of the common matter action

20 October 2026. **Verdict: correct under the stated classical and finite-computation restrictions.** The exact flat-space energy/charge floor is supported by a complete algebraic certificate. The stationary fragments and uniform zero-pressure phase are numerical candidate branches, not proved ground states, stable dynamical objects, cooling mechanisms or empirical fits. This review does not rerun a collocation solve, root search, PDE or collision experiment. Exact bytes reviewed are pinned in `sources_review_action.json`.

## Claim and conventions

The audited matter potential is

    V = I + MX^2 |X|^2 + g(X* Psi^2+X Psi*^2)
           + lambda I^2 + a chi I + U(chi), I=|Psi|^2,
    U(chi)=M^2 chi^2/2-M chi^3/8+chi^4/4,
    MX^2=4.0016, g=.002168, lambda=1.99+g^2/MX^2,
    M=100, a=200.

Psi and X are complex, with U(1) charges 1 and 2; chi is real and neutral. Flat matter time derivatives use Box_+=dt^2-laplacian. The report's separate minimal GR embedding uses (-+++) and fixes the curvature sign through the displayed Einstein equation. These conventions are compatible; the flat Box symbol is explicitly distinguished.

## Exact uniform classical floor: passed

For mu=17/20, alpha=1-mu^2 and D_mu=MX^2-4mu^2,

    V-mu^2(I+4|X|^2)
       = D_mu |X+g Psi^2/D_mu|^2
            + ell I^2 +(alpha+a chi)I+U(chi),
    ell=lambda-g^2/D_mu>0.

This square has the correct complex conjugation and coefficient. The rational constants independently reconstruct as

    D_mu=2779/2500,
    ell=13831033985551/6950279000000,
    alpha=111/400,
    t0=alpha/a=111/80000.

U is nonnegative for every real chi, because

    U(chi)=chi^2[(chi-M/4)^2/4+31M^2/64].

When alpha+a chi>=0, the reduced potential is nonnegative for I>=0. Otherwise write chi=-t and minimize the quadratic in I. The necessary remaining polynomial is

    F(t)=ell t^4+50ell t^3+(20000ell-40000)t^2
                         +111t-12321/160000,
    t>=t0.

Independent exact-rational Sturm reconstruction gives F(t0)>0 and zero roots on [t0,infinity). The sign sequences are (+,+,+,-,-) and (+,+,+,+,-), each with one variation. This certifies the entire amplitude domain rather than sampling it. The code and run_001 reproduce these exact coefficients and signs.

The positive-charge convention Q=integral[2 Im(Psi*Psi_t)+4 Im(X*X_t)] is positive on exp(+i omega t). Completing |Psi_t-i mu Psi|^2 and |X_t-2i mu X|^2, with all gradients and the neutral kinetic terms retained, gives E-mu Q>=0; opposite signs give E+mu Q>=0. Thus **E>=.85|Q|** for the stated flat finite-energy/periodic classical configurations. This does not prove a quantum inequality or a global energy bound for a gravitating spacetime. It replaces, rather than preserves, the protected carrier's stronger E>=|Q| floor.

## Stationary Euler-Lagrange equations, charge and energy: passed

Writing Psi=f(r)exp(i omega t), X=b(r)exp(2i omega t), chi=h(r), with real profiles, direct variation gives

    f''+2f'/r=(1-omega^2+2lambda f^2+a h+2g b)f,
    b''+2b'/r=(MX^2-4omega^2)b+g f^2,
    h''+2h'/r=M^2h-3M h^2/8+h^3+a f^2.

The code implements these equations with the correct factor of two for the complex-field conversion term. The fixed-charge state and Hamiltonian are

    Q=8pi omega integral r^2(f^2+4b^2)dr,
    E=4pi integral r^2[omega^2(f^2+4b^2)
                          +f'^2+b'^2+h'^2/2+V]dr.

The integrated charge in X is 8omega integral b^2 d^3x. The real mediator contributes half its kinetic/gradient square and no charge. Scaling E-omega Q gives T_grad+3V_int-3T_rotation=0, as used. The finite-difference dE/dQ=omega check uses the same chemical-potential normalization.

Independent arithmetic from saved results reproduces

    E(80000)=76151.17723365594,
    E(160000)=149323.62958635326,
    gap=2978.7248809586163,
    gap/[2E(80000)]=0.019557970008913617,
    [E(80800)-E(79200)]/1600=0.9217888800430319.

The last value agrees with omega(80000)=.9217883882751382 at the reported finite-difference accuracy. The largest L=40/tol=1e-5 to L=60/tol=1e-7 relative energy change is 1.215e-11. run_001 records 43 passed controls. These are resolved finite-profile observations; collocation residuals and orthogonal identities are not a rigorous continuum error bound, uniqueness theorem, nonradial spectrum or ground-state proof. The two-field ARGON gap is not silently reused.

## Corrected homogeneous phase: passed as a local numerical candidate

At fixed omega, eliminate only the homogeneous X amplitude:

    D=MX^2-4omega^2,
    b=-g I/D,
    A(omega)=lambda-g^2/D,
    Omega=(1-omega^2)I+A I^2+a h I+U(h).

The equations Omega_I=0, Omega_h=0 are precisely the uniform field equations. The a h I term is essential. It appears in both corrected `liquid_phase_v2.py` and the report. The original omitted-term run is retained with failed runner status; it is not counted as successful evidence.

Pressure, charge and energy follow independently:

    P=-Omega,
    q=-dOmega_on-shell/domega=2omega(I+4b^2),
    e=omega q-P.

In particular A'=-8g^2 omega/D^2, so eliminating the charged source preserves its contribution to q; treating X as neutral would miss it. The reduced amplitude Hessian is [[2A,a],[a,U'']], the Schur complement of the positive 2D block of the full (I,b,h) Hessian. Its two positive eigenvalues are a meaningful local amplitude check, not the full dynamical perturbation spectrum.

The saved coexistence root reconstructs with direct full-potential residuals at approximately 1e-12 or less:

    I=49.00650744444027, h=-.976461506496568,
    b=-.10747017781677803, omega=.8678983025671659,
    q=85.14552193768695, e=73.897653960913,
    P approximately 0, e/q=omega,
    dq/domega=395.709175815124,
    cs^2=q/(omega dq/domega)=.24792301922176127.

The report correctly calls this a zero-pressure local stationary phase candidate. Positive compressibility does not certify a global phase diagram, successful formation, a collision rate or stability against every mode. The rather large sound speed is explicitly distinguished from a cosmological dilute cold-gas sound speed. run_003 has 19 passed controls; run_002 remains failed.

## Model limits and wording corrections

Two ambiguities raised during review have been corrected in the pinned report:

1. Exact ARGON is recovered only along the parameter family **g->0 with lambda(g)=1.99+g^2/MX^2**. Holding the performed numerical lambda fixed produces a slightly different ARGON quartic. The current report says so explicitly.
2. The **three-field matter sector** has no massless vacuum carrier. Its GR embedding does have massless metric/gravitational-wave modes, whose emission is a separate uncomputed channel. The current report distinguishes these statements.

Setting a=0 consistently decouples the neutral field and recovers a protected-family member, with a strongly changed lambda_rep. Merely imposing chi=0 at a!=0 fails its sourced equation. Original pressure, scattering, nonlinear yield and abundance results therefore do not transfer; the report maintains that restriction. The displayed narrow linear daughter-production band is compatible with the same new action, because chi and source backreaction first enter at quadratic order in daughter amplitude. It is not a nonlinear or vacuum-seeded production calculation.

The empirical/noncompletion language is appropriate. No mass scale, abundance, original-to-ARGON physical bridge, microscopic galactic viscosity, useful exported E/Q/vector J, gravity-law normalization, lensing profile, cosmological transfer function or four-dwarf likelihood is supplied by the floor or the stationary roots. Sextans' conditional global-profile stock ceiling, actual stellar selection, and Fornax/Leo I heating/profile constraints remain open. New stationary binding cannot repair them by assertion.

The outgoing energy/charge/spin formulas, gravity action audit and observed-data claims are referenced scope boundaries, not independently revalidated in every detail by this focused matter-action review. In particular, no scalar emission threshold is promoted into a theorem excluding every radiative or gravitational channel.

## Review record and next obligation

The exact floor and local equations are reconstructed algebraically; saved finite results and runner statuses are checked independently without executing the authors' scripts. Review was not blind: the candidate and earlier carrier-audit result were known. No source code/report was edited by this reviewer. Only this review and its hash receipt were written.

**First unresolved physical implication:** establish stability and actual escaped branching of these same-action fragments. Compute the full coupled perturbations and then matched pair E,Q,p,orbital J,intrinsic J and radiation/matter flux with phase/impact averaging. A positive stationary gap is an available endpoint difference only if the process reaches that state and actually exports the difference. It is not the completed theory.
