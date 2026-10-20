# Actual-action cooling and angular-momentum flux audit

20 October 2026. Requested base checkpoint: `dce2a2e3d`. **The ARGON stationary merger gap is not blocked by total energy availability, but the isolated vacuum has no neutral massless cooling channel. Low-frequency escaping charged-field radiation generally changes remnant charge. Internal sound or vortex storage does not itself establish galactic angular-momentum export.** The added charged-X alternative preserves those distinctions.

This audit derives continuum thresholds and flux bookkeeping from the action. It executes no field evolution and changes no source, frozen criterion or completed record. Exact current input hashes and the small arithmetic checks are in `sources_flux.json`.

## 1. Vacuum channels of the actual ARGON action

The source is `ARGON11/frag3d.c`, revision `07546091c`, in units m_h=hbar=c=1:

    V = I + Lq I^2 + a chi I + U(chi),  I=|Psi|^2,
    U = M^2 chi^2/2 - M chi^3/8 + chi^4/4,
    M=100, Lq=1.99, a=200.

Linearization about Psi=chi=0 gives uncoupled massive fields:

    nu_Psi^2 = k^2 + 1,
    nu_chi^2 = k^2 + 10000.

The interaction is cubic or higher about vacuum, so there is no vacuum linear mixing that creates a massless mode. Psi carries the conserved charge; chi is neutral. A real propagating chi wave requires |nu|>=100. An off-shell mediator field or its quasistatic deformation transfers force and stores energy but is not an outgoing radiation channel. This is a flat matter-field test; no gravitational-wave sector is included.

For the source convention Q=2 Im(Psi* Psi_t), take an outgoing charged harmonic proportional to exp(i nu t - i k r - i m phi), with nu*k>0. Its asymptotic fluxes obey

    E_dot = nu Q_dot,       Jz_dot = m Q_dot,
    Jz_dot/E_dot = m/nu.

The sign of Q_dot distinguishes positive and negative frequency branches. In a particle interpretation, E=|nu|N, Q=sign(nu)N, so E>=|Q| for vacuum Psi quanta. This is a bound on asymptotic quanta, not the already-bound soliton energy. For a neutral real chi harmonic the consistent positive-energy convention gives Jz_dot/E_dot=m/|nu| and Q_dot=0.

These are thresholds for small-amplitude radiation around vacuum. They do **not** prohibit nonlinear outgoing solitons with E/Q<1. The desired cold outflow could contain intact fragments or new bound daughters; their full E, Q, P and J must be measured rather than applying a free-Psi-quantum E>=|Q| bound to them.

An angular harmonic's J is about the chosen origin. For a localized fragment, the galaxy-centred flux decomposes into R_fragment cross P_escape plus intrinsic/multipole J about that fragment. Exporting fragment winding is not automatically exporting the galaxy's orbital J.

## 2. Perturbations about a charged rotating fragment

For Psi=exp(i omega t)[f+u+i v], chi=h+xi, define radial/angular operators L_u=-Laplacian+1-omega^2+6 Lq f^2+a h, L_v=-Laplacian+1-omega^2+2 Lq f^2+a h, and L_chi=-Laplacian+M^2-3 M h/4+3 h^2. Linearization gives

    u_tt - 2 omega v_t = -L_u u - a f xi,
    v_tt + 2 omega u_t = -L_v v,
    xi_tt = -L_chi xi - 2 a f u.

The factors of two follow from the complex Psi and real chi kinetic normalizations. Rescaling the real Psi components by sqrt(2) makes the static Hessian symmetric.

A rotating-frame frequency Omega produces charged lab-frequency sidebands omega+Omega and omega-Omega. At infinity their wavenumbers satisfy

    k_plus^2  = (omega+Omega)^2 - 1,
    k_minus^2 = (omega-Omega)^2 - 1,
    k_chi^2   = Omega^2 - 10000.

For Omega>=0 and 0<omega<1, the positive-charge sideband opens at Omega=1-omega; the negative-charge sideband opens at Omega=1+omega. The neutral chi threshold is Omega=100. Proper nonradial Bogoliubov modes have conjugate sidebands; each outgoing sideband's frequency and angular index must be measured separately when calculating flux.

| Isolated stationary charge | omega | First positive-Q threshold | Negative-Q threshold | Neutral chi threshold |
|---:|---:|---:|---:|---:|
| 80,000 | 0.9218835527 | 0.0781164473 | 1.9218835527 | 100 |
| 160,000 | 0.9096140574 | 0.0903859426 | 1.9096140574 | 100 |

These values use the completed, pinned isolated-profile run, not fragmentation medians. A small perturbation below the first threshold has no linear propagating vacuum channel. It may remain trapped, mix with other internal modes, or leak through nonlinear harmonics. An internal U(1) phase/Goldstone mode does not stay gapless on entering the symmetric vacuum outside the fragment.

The large total gap 2977.827663 does not imply a wave of frequency 2977.8. Frequencies, amplitudes and their nonlinear conversion determine which channels propagate. In particular, slow chi following the charge density does not emit on-shell chi merely because the total excitation energy exceeds its mass. Conversely, sufficiently high-frequency nonlinear motion can emit chi: the mass threshold is not a universal prohibition.

## 3. Charge bookkeeping limits the meaning of cooling

Let E_i=2 E_stat(Q), final bound charge Q_r=2Q-q, and escaping energy E_out. Even if the remnant reaches the tested stationary branch, conservation requires

    E_out = E_i - E_stat(2Q-q),
    Q_out = q,

plus any surviving internal excitation, rotation, other fragments and their energies. If the escaping channel is positive-Q Psi radiation, E_out>=q. For small q, using dE_stat/dQ=omega_f,

    E_out approximately Delta E_stat + omega_f q,
    Delta E_stat >= (1-omega_f) q

is the leading threshold cost for near-rest charged evaporation. Finite q needs the full E_stat curve and a dynamically accessible final branch; the tangent expression is not a finite-q exclusion bound.

An unexcited stable fragment cannot emit a small positive charge at zero cost: removing q releases only approximately omega q<q while a free outgoing Psi quantum costs at least q. Merger excitation can supply that deficit. Thus omega<1 protects the ground branch from spontaneous evaporation; it does not prevent an excited merger from cooling by losing charge.

If remnant charge must remain exactly 2Q, net-charge-free cooling needs a neutral channel, both charge signs of Psi radiation, energy transfer to other already-existing fragments, or another explicitly constructed recipient. A single low-frequency sector with only the positive-Q sideband open does not accomplish that. General particle-antiparticle emission can be charge neutral; a single coupled-frequency sector and a multiharmonic merger need not have the same threshold bookkeeping.

The root's processed-mass estimate from the stationary gap therefore remains conditional: it must not count the gap as available wind power while silently keeping all remnant Q, internal energy and mass allocation unchanged. Energy transfer through a virtual mediator to a third body is possible without on-shell chi emission, but requires that body and an actual momentum/energy exchange calculation. An isolated pair cannot assume such a recipient.

## 4. Coherent angular modes and the centrifugal barrier

An outgoing scalar partial wave satisfies at large r

    u_l'' + [k^2 - l(l+1)/r^2] u_l = 0.

It can carry J/E=m/nu. This is why the packet estimate J<=r E/c is not a universal theorem about a compact coherent emitter. High angular indices can have an extended evanescent near field and tunnel to a propagating far field.

That loophole has a calculable coupling cost. The centrifugal turning radius is approximately sqrt[l(l+1)]/|k|. For an emitter of radius a_f, partial waves with l much greater than |k|a_f encounter a barrier between the source and the outgoing region. Efficient emission of a huge m cannot simply be inferred from a formal m/nu ratio. One must calculate the partial-wave transmission and source amplitude. This is a suppression criterion, not an exact zero-flux bound.

Likewise, isotropic emission with zero net momentum and zero intrinsic J in the emitter COM frame exports only advected orbital J after boosting. Coherent multipole emission or an escaping-subset bias can evade that special case, but their global orbital direction must be correlated with the parent galaxy's angular momentum. Arbitrary local phases or fragment spin labels do not supply that correlation.

## 5. Could an ambient charged phase provide a gapless receiver?

A nonzero homogeneous background differs from vacuum. For Psi=sqrt(I) exp(i omega t), chi=h, stationarity gives

    omega^2 = 1 + 2 Lq I + a h,
    U'(h) + a I = 0.

With B=U''(h), define D=4 Lq I-2 a^2 I/B. Eliminating the heavy neutral response in the small-k limit of the full linear system gives

    c_s^2 = D / (D + 4 omega^2).

The exact fluctuation determinant before that limit is

    [(k^2+4 Lq I-Omega^2)(k^2+B-Omega^2)-2 a^2 I]
        (k^2-Omega^2) - 4 omega^2 Omega^2 (k^2+B-Omega^2) = 0.

For the original ARGON parameters, the nonzero-density sound-sign change is at I=32.7294523, h=-0.65296236. The coexistence scale is I_star=48.9893097. Evaluating the exact six-component fluctuation matrix at k=0.001 reproduces the low-k expression to within 7e-6 relative in four illustrative cases:

| I/I_star | c_s^2 |
|---:|---:|
| 0.10 | -0.04815088 |
| 0.50 | -0.09923705 |
| 0.85 | +0.14286266 |
| 1.00 | +0.24898158 |

The dilute homogeneous charged states used in these two source branches are modulationally unstable, not an already-established stable gapless transport bath. The dense branch can support local collective sound, but its physical density, spatial extent, boundaries and coupling to an escaping receiver remain to be supplied. These dimensionless internal sound speeds are not dwarf velocity dispersions. This does not exclude a discrete fragment bath, a different stable ambient phase or gravitational transport.

## 6. Addendum: the root's explicit charged-X alternative

The new common_action.py introduces charge-2 X, mass-squared 4.0016, coupling g(X*Psi^2+X Psi*^2), g=0.002168, lambda=1.99+g^2/M_X^2, retaining the neutral field. This is a declared alternative common matter action, not a reinterpretation of the unchanged ARGON source.

For X=b exp(2 i omega t), its source and charge factors are correct:

    (-Laplacian + M_X^2 - 4 omega^2)b + g f^2 = 0,
    Q = 2 omega integral [f^2 + 4 b^2] d^3x,
    T_rotation = omega^2 integral [f^2 + 4 b^2] d^3x.

The vacuum fields still decouple linearly. X has |nu_X|>=M_X approximately 2.000400, charge magnitude 2, hence E/|Q|>=M_X/2 approximately 1.000200 for free X waves. Its rotating-frame sideband thresholds are M_X-2omega and M_X+2omega. A stationary b at 2omega<M_X is evanescent, not an escaping neutral coolant. Near-threshold conversion X to two Psi quanta preserves charge; it is not a new neutral massless branch.

For homogeneous amplitudes, integrating out stationary b gives A(omega)=lambda-g^2/(M_X^2-4omega^2) and

    grand = (1-omega^2)I + A(omega)I^2 + a h I + U(h),
    q = 2omega[I+4b^2],  P=-grand,  rho=omega q-P,
    c_s^2 = q / [omega (dq/domega)].

The restored a h I term in liquid_phase_v2.py is essential. The earlier liquid_phase.py omitted it in the grand potential while retaining it in the field equation; its failed controls are not evidence. The corrected script checks the direct full potential, the I derivative, dP/domega=q and implicit derivatives. Its run_003 gives omega=0.8678983 and local c_s^2=0.247923 at zero pressure. This supports a local compressible charged phase, not a relaxation rate, full nonradial stability, or escape into vacuum. The neutral-only low-density expansion -a^2 I^2/(2M^2)+a^3 I^3/(8M^5) is correctly normalized; near-resonant X retains its frequency dependence.

## 7. Cheapest decisive next calculation

For an intact-fragment outflow, first extend the stationary branch to the proposed remnant and daughter charges, including the minimum supported daughter charge. Test the declared branch's energy balance against E_stat(Q_remnant)+E_stat(Q_daughter)+K_orbital and its J allocation. The existing two charges do not establish arbitrary fragment mass loading. This is a cheap static compatibility gate, not a fission or merger rate and not a ground-state bound.

Use the saved stationary profiles to compute the coupled outgoing radial fluctuation/scattering problem, separately for several l,m sectors. Locate internal poles and determine whether their frequencies lie below or above the positive-Psi, negative-Psi, X and chi thresholds. Measure channel-resolved E_dot, Q_dot and J_dot, with the far-field flux identities checked. Test zero-frequency phase/translation modes and a no-coupling vacuum limit as controls.

This costs much less than another 3D formation run and directly distinguishes trapped excitation, charged evaporation and neutral radiation. It does not determine how strongly a merger excites each sector or whether it ejects whole nonlinear fragments; the next matched pair experiment must supply that source spectrum, outgoing-fragment census and phase/impact distribution. Galaxy-scale orbital export still requires the correct origin, angular bias and a dynamically connected outer receiver. Neither a thermodynamic sound speed nor a stationary energy gap completes that transport mechanism.
