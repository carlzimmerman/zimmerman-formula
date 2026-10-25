# CCT-009: coherent mode mixing, cooling, and the assembly-energy selector

Scope: this is the new CCT nonrelativistic selective-coupling candidate. It is not a result for current v3/AeST or retired SCT-M. Eta=1500 pc km/s remains an imposed universal parameter. The cold inventory 5.364*200*Mformed remains an assumed catchment, not an observed total dwarf mass or a cosmological prediction. The earlier CCT-008 supported occupations are targets, never reset into these collapses.

## Field dynamics without a binary collision term

    i eta partial_t psi = -eta² lap psi/2 + (Phi_c+Phi_g) psi,
    lap Phi_c = 4 pi G |psi|².

Writing psi=sqrt(rho) exp(i S/eta), where S is a velocity potential,

    partial_t rho + div(rho grad S) = 0,
    partial_t S + |grad S|²/2 + Phi_c+Phi_g
        - (eta²/2) lap sqrt(rho)/sqrt(rho) = 0.

The last term is dispersive gradient stress. It can oppose concentration but does not supply dissipation. Nonspherical self-gravity mixes angular/radial waves. Outgoing waves carry mass, energy and angular momentum; a retained supported envelope must be generated dynamically rather than assigned an occupation after collapse.

The total field Hamiltonian is

    E = eta²/2 integral |grad psi|² dV
        + (1/2) integral rho Phi_c dV + integral rho Phi_g dV.

The self-potential is sourced once, and its interaction energy has the factor 1/2. The force uses the full Phi_c. No Newtonian correction is added after solving it. Prescribed gas contributes work W_g=integral dt dV rho partial_t Phi_g. Stars in the diagnostics feel the previously specified baryon-only law plus the Newtonian cold field once. Cold is not assigned an extra Xi charge.

## Angular support is different from spin removal

For psi=sum a_lm(r) Y_lm, kinetic support depends on eta² l(l+1)/(2r²), while aligned spin is

    Jz = eta sum_lm m integral |u_lm|² dr.

High l can give tangential support at small m. It is not evidence that large net spin has escaped. Projection of self-gravity gives four-wave terms obeying m_alpha+m_delta=m_beta+m_gamma. The explicit nonspherical control generates modes above l=4; the matched spherical-only control cannot do so because each l,m evolves under its own radial Hamiltonian.

The source starts with m=0,+-2 and a 1% amplitude l=3,m=0 seed. The seed breaks the old exact inversion symmetry. Pi-rotation symmetry remains: odd m are absent and Jx=Jy=0 exactly. Results concern aligned spin in this symmetry class, not arbitrary tilted assembly. Finite |m| cutoffs materially change mode populations, so late spin-export percentages remain finite-run diagnostics.

For a free outgoing mode exp(-i omega t+i m phi), specific energy is eta omega and specific aligned angular momentum is eta m. Emitting predominantly small-m waves can remove energy and mass while leaving MORE specific spin in the remnant. That is what the tested deeply bound history does. A successful formation mechanism needs the right azimuthal spectrum, not simply more high-l power.

## A necessary energy condition on any proposed assembly

With final target energy E_target, additional discarded energy E_out, and no other remnants,

    E_initial + W_external = E_target + E_out.

If outflow is diffuse and asymptotically nonnegative-energy, E_out>=0, hence E_initial+W_external>=E_target. A very tightly bound oversized cloud cannot become the chosen weakly bound small inventory merely by emitting positive-energy waves: that makes the remnant energy more negative. The actual remaining Hamiltonian and already removed sink energy sharpen the additional-work requirement after gas removal.

This is conditional on the target and receiver assumptions. A self-bound escaping fragment can carry negative internal energy while its centre of mass escapes; tides, gas, or another bound companion can also be receivers. A negative sink-energy entry alone does not determine its orbital status. No universal no-go is inferred here.

## Three explicit assembly tests

1. **Old bound history:** 10 km/s inward radial phase with the CCT-007 gas contraction/removal. Same inventory/geometry, lower eta and higher angular support. Gas work is recorded, not supplied for free in the interpretation.
2. **Near-marginal bound history:** no gas; choose the FIRST radial-phase root giving E_initial=-0.001 |W_self|, independently of the target profile. This relaxes the energy obstruction for Draco/Sextans but remains too bound for the chosen compact Fornax/Leo I inventories. Fornax/Leo I were checked by energy preflight rather than unnecessary long evolutions.
3. **Local escape-speed incoming pulse:** no gas; at the initial snapshot set

       v_r(r) = -sqrt(v_ref² - 2 min_angles Phi_c(r,angles)),
       S(r) = integral v_r dr,  v_ref=10 km/s.

   This radial WKB prescription exceeds the instantaneous classical escape speed in every sampled direction. It has positive total initial Hamiltonian. It does NOT prove the full wave lies in the positive spectral subspace, nor does it derive a cosmological incoming stream.

**Important self-gravity bookkeeping:** the code's argument `--vinfinity` and raw key `initial_classical_vinfinity_kms` name the LOCAL test-potential reference v_ref above. They are NOT a common total-system speed at infinity. For self-gravitating material, summing rho Phi counts interactions twice; the Hamiltonian uses half that term. Consequently this prescription supplies E_initial/M substantially larger than v_ref²/2. The correct equivalent collective energy speed is sqrt(2 E_initial/M), recorded by analysis. Do not transfer CCT-006's common 10 km/s infinity-energy budget to this pulse. A physical assembly must provide its measured positive total energy, for example through an independently specified orbital/merger history.

The initial negative spectral weight is also measured for the MONOPOLE Hamiltonian. A complete monopole bound-state sum is not a spectral certificate for the nonspherical Hamiltonian. An incomplete sum is only a lower bound on that monopole weight. No pure-continuum capture claim is made from the WKB construction.

## What a successful continuation must establish

Populate a supported envelope from a specified incoming state, with correct source mass and initial TOTAL energy, while retaining an acceptable radial profile and paying all outgoing M/E/vector-J. Demonstrate l, m, radial, time and boundary convergence. Preserve failures of previously fixed endpoint/profile gates. A newly compatible global stellar moment is an exploratory clue, not a posthoc pass of a failed profile criterion. Any extended alternative halo requires radial-data and tidal/inventory checks. Only a settled, acceptable profile warrants a live nonspherical stellar DF heating test; delayed star birth by itself supplies no protection.

## An additional continuum mass–energy bound

For an isolated star-free field of mass M=integral |psi|², put A=||grad psi||_2. For any centre x, complete the square with the radial unit vector around x:

    0 <= integral |grad psi + a rhat_x psi|²
       = A² + a² M - 2a integral rho(y)/|y-x| d³y.

Optimizing the real parameter a gives integral rho(y)/|y-x| d³y <= sqrt(M) A. Integrate this inequality against rho(x) and retain the self-energy factor 1/2:

    W_self >= -(G/2) M^(3/2) A,
    E >= eta² A²/2 -(G/2) M^(3/2) A
      >= -G² M³/(8 eta²).

Thus any isolated negative-energy cold state obeys

    M >= [8 eta² |E|/G²]^(1/3).

This non-sharp necessary bound is a continuum inequality, not a fit to the numerical runs. It also extends to positive mode mixtures by Cauchy–Schwarz on their gradient norms. Applying it to a finite-run measured energy is conditional on a consistent continuum energy approximation; finite ledger conservation alone does not establish that approximation. It constrains a cold star-free remnant, not an arbitrary baryon-coupled system. A fixed bounded stellar potential adds its known negative lower-bound term; future positive work or negative-energy bound ejecta must be included explicitly before extrapolating.

This makes the required correction concrete: after positive-energy radiation has made a remnant very tightly bound, one cannot independently choose a tiny retained mass by relabeling its angular occupations. The energy, mass, gradient stress and receiver must agree.

## Coherence is a separate, exact bridge obligation

For the coherent parent Gamma=|psi><psi|,

    i eta dot Gamma=[H[Gamma],Gamma].

The commutator preserves Tr Gamma^n and the spectrum of Gamma. In particular a pure rank-one state stays rank one. A deterministic absorber changes the norm but still maps a single wave to a single wave; it does not produce a high-rank statistical mixture. Populating many angular or radial coefficients is not the same as destroying their mutual coherences.

Therefore the literal high-rank CCT-008 occupation matrix is NOT dynamically manufactured from a pure wave by this closed commutator equation. This does not forbid a different coherent stationary density with the right observables. It also does not forbid a time/ensemble-averaged effective description, but its validity for the stars must be derived.

For an ensemble, write Gamma=Gamma_bar+delta_Gamma and Phi=Phi_bar+delta_Phi. The exact averaging equation contains the correlation term

    i eta dot Gamma_bar = [H[Gamma_bar],Gamma_bar]
                         + average([delta_Phi,delta_Gamma]).

Dropping that term is an additional closure. A moving finite-time average also has window/flux terms. Its dynamics is not certified merely by finding positive occupations in a fixed potential.

The energy bridge has a corresponding term:

    average(E) = eta²/2 Tr(-lap Gamma_bar)
                 + (1/2) integral rho_bar Phi_bar dV
                 + (1/2) average(integral delta_rho delta_Phi dV)
                 + average(external potential energy),
    (1/2) average(integral delta_rho delta_Phi dV)
       = -1/(8 pi G) average(integral |grad delta_Phi|² dV) <= 0,

for isolated matching boundaries. A smooth mean density therefore omits negative fluctuation binding energy unless it is explicitly retained. Calling that omission 'energy shed' would be false cooling. No second cold gravitational source is introduced to repair it. `fluctuations.json` measures the monopole part of this exact finite-window identity from saved profiles; nonspherical and stellar-force response obligations remain.

## External-host consistency of the selective coupling

The stated CCT action gives stars an extra Xi acceleration and gives cold mass no Xi charge. An external host can therefore accelerate their centres differently. This is a physical effect, not removed by a shared accelerating coordinate system. Under the approximation of a slowly varying host field and translating unchanged components, the internal Newtonian restoring force must satisfy the necessary condition

    |g_X,host| <= (1+Mstar/Mcold) max_r |g_cold(r)|.

The extended stellar COM's restoring acceleration is bounded above by the maximum point acceleration, so this is a conservative necessary test, not sufficient survival. For a Plummer cold profile max g_c=2 G Mc/(3 sqrt(3) b²). In a spherical baryonic host, the candidate's own action gives

    g_N,host = g_X,host²/(a0-g_X,host).

`host_threshold.json` therefore reports the host baryonic SOURCE MASS at which the conservative condition fails, using the catalogue's Galactocentric distances rather than heliocentric distances. It assumes no actual Milky Way source mass and issues no observational exclusion. A full host solution, external-field/basin prescription and live stellar/cold response are required before claiming satellite survival. Making the cold Xi charge universal would change both its force and its source in the action; it cannot be added as a force-only patch without rescoring the model and avoiding duplicate gravity.

## Fragments and reference frames must be tracked

A high-l expansion around the original origin can represent a displaced localized object. It is not, by itself, intrinsic orbital support of one galaxy. The Draco incoming-pulse state develops two symmetry-related off-axis potential wells, so the original origin is not automatically the centre of either potential fragment.

For a selected material core,

    J_internal = J_about_origin - R_core_COM cross P_core.

A window's Jz about the old cloud axis is not the internal spin of an off-axis fragment. In a moving stellar/core frame r'=r-c(t),

    d²r'/dt² = -grad Phi(c(t)+r',t) - grad Xi_b(c(t)+r',t) - c_ddot(t).

A uniform centre acceleration must not be turned into stellar heating by fixing the stars at the old cloud origin. Conversely an instantaneous potential minimum is not automatically a material core trajectory. Future runs need a fragment finder, mass currents, core COM/bulk velocity, linear-momentum/outflow recoil ledgers, and a live baryonic response.

`centering.json` re-scores instantaneous radial monopoles around cold-potential wells without changing the saved dynamics or original gate. Its off-centre mass integral is exact in ANGLE for the finite density harmonics. If c is the new centre, d=|c|, and A the aperture radius,

    u(r)=(r²+d²-A²)/(2rd), clipped to [-1,1],
    M_c(A)=2 pi sum_radial w r² sum_lm rho_lm(r) Y_lm(c_hat) I_l(u),
    I_0(u)=1-u,
    I_l(u)=[P_(l-1)(u)-P_(l+1)(u)]/(2l+1), l>=1.

Radial shell quadrature, finite field resolution and the provisional well-centre definition remain limitations. The spherical-shell limit and whole-domain M/Jz normalization are checked. `free_translation_check.json` compares the representation with an analytically translating and spreading free Gaussian; it does not replace a nonlinear recoil test.
