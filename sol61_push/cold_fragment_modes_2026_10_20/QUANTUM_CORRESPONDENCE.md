# Conditional quantum correspondence of the chiral mode's classical loss

20 October 2026. Bounded analytic derivation from the existing no-half, unit-K classical mode and its action-derived second-harmonic outgoing calculation. Reviewed bytes are pinned in `sources_quantum.json`. No quantum scattering calculation, new evolution, or numerical experiment is performed here.

**Status: conditional correspondence, not a completed quantum calculation.** If a positive-energy fragment shape mode can be canonically quantized as one oscillator, and its emitted Psi continuum can be eliminated in a weak-coupling, vacuum, rotating-wave, Markov approximation with the same normalization, the classical coefficient matches a two-quantum loss operator. In units hbar=1 the standard coefficient is `kappa=gamma Omega/2`. The classical PDE calculation alone does not establish that master equation, its microscopic matrix element, or its validity down to one excitation.

## 1. Classical input and what is being quantized

The existing normalized real perturbation is

    z=A[Z(r)Y_22 exp(+i Omega t)/r+c.c.],
    K_mode=A^2, J_mode=(2/Omega)K_mode,

with `partial_phi Y=-2iY`, the established physical positive-chirality convention. K means E-omega Q, not laboratory energy E. The five real components are canonical, but the rotating background introduces gyroscopic terms. Their symplectic normalization must be retained in quantization; treating the components as five independent oscillators would be incorrect.

For the selected finite modes, the action generates a quadratic source at frequency 2Omega and physical angular labels ell=4,m=4. The outgoing calculation defines gamma by

    P_K,out=gamma A^4=gamma K_mode^2,
    dK_mode/dt=-gamma K_mode^2

to leading weak-amplitude, slowly varying-background order. The reviewed deterministic-cache finest-grid coefficients are gamma=3.8003453684523445e-6 at Q80000 and gamma=1.6773340732409204e-7 at Q160000, in the stated dimensionless classical normalization. These are classical response coefficients, not already quantum transition rates or physical dwarf times.

Suppose a properly normalized positive-energy mode has oscillator action I=K/Omega. Quantization would give

    K_hat=hbar Omega N_hat, N_hat=a_dagger a, [a,a_dagger]=1,
    J_hat=2 hbar N_hat.

K here is excitation energy above the renormalized reference fragment. A zero-point term must not be inserted into the classical loss formula and interpreted as vacuum radiation. The positive-time complex phasor convention must also be reconciled with creation/annihilation operators; a coefficient of exp(+i Omega t) is not automatically an annihilation operator.

The overall physical normalization of the action is a separate input. If S_phys=S0 S_dimensionless, then hbar_eff=hbar/S0 enters the dimensionless oscillator relation K=hbar_eff Omega N. Classical Euler-Lagrange equations and classical gamma do not fix S0. Thus the dimensionless mode normalization does not by itself determine the number of quanta in a real fragment.

## 2. Two-mode selection rules

Call a quantum of this localized shape mode a quasiparticle or phonon; this does not assert a bulk acoustic dispersion or conserved phonon number.

Two identical chiral ell=2,m=2 excitations have M=4. The product of two ell=2 harmonics has L<=4; M=4 therefore forces L=4. Equivalently,

    Y_22^2=sqrt(5/(14pi)) Y_44

in the matched chirality convention. This is the highest-weight symmetric two-boson channel. For a general pair of quadrupole polarizations, identical-boson angular addition also permits symmetric L=0,2,4 channels with their appropriate M and radial overlaps; the single chiral preparation is essential to the L=4-only statement.

The candidate elementary channel is therefore

    two internal mode quanta -> one outgoing Psi+ quantum,

while the remnant supplies the charge and chemical-potential contribution consistently. The emitted scalar has no intrinsic particle spin; its angular momentum about the fragment is its ell=4,m=4 partial wave. Each event removes leading rotating energy 2hbar Omega and internal angular momentum 4hbar. Its positive Psi charge is one quantum of the source U(1), and its leading laboratory frequency is

    nu=omega+2Omega.

The reviewed modes obey omega+Omega<1 but omega+2Omega>1, so the fundamental is below the first matter threshold and the second harmonic opens Psi+. The X+ and chi channels are closed at this second harmonic. Angular and threshold selection rules permit the process; the nonzero classical outgoing overlap supports a corresponding leading semiclassical channel, conditional on the quantization and continuum hypotheses. Selection rules alone would not determine its rate.

## 3. Charge bookkeeping and the missing DC response

The mode's vanishing *linear* global charge does not make its quadratic charge vanish. Write the full canonical fields as

    Psi=e^(i omega t)(F+u+i v)/sqrt(2),
    X=e^(2i omega t)(B+s+i t_X)/sqrt(2),
    chi=h+xi, F=sqrt(2)f, B=sqrt(2)b.

The positive-charge convention gives exactly

    Q=integral {omega[(F+u)^2+v^2]+(F+u)v_t-v u_t
               +4omega[(B+s)^2+t_X^2]
               +2[(B+s)t_X,t-t_X s_t]} d^3x.

Consequently the bare first-order mode contributes at quadratic order

    Q_bare,2=integral {omega(u^2+v^2)+u v_t-v u_t
                      +4omega(s^2+t_X^2)
                      +2(s t_X,t-t_X s_t)} d^3x.

For the no-half chiral phasor, using reduced components Z=(Z_u,Z_s,Z_xi,Z_v,Z_t), the time/angular-averaged coefficient is

    Q_bare,2/A^2=integral dr {
       2omega(|Z_u|^2+|Z_v|^2)-4Omega Im(Z_u* Z_v)
       +8omega(|Z_s|^2+|Z_t|^2)-8Omega Im(Z_s* Z_t)}.

The star in the last display denotes complex conjugation. This bare quantity is not the charge of a completed fixed-total-Q quasiparticle state. The quadratic source also has a zero-frequency sector from Y_22 Y_22*, with ell=0,2,4. Its ell=0 deformation changes the background charge through the *linear* charge functional evaluated on that second-order correction. A frequency/family shift adds `(dQ_bg/domega)delta_omega`. A consistent fixed-Q preparation must solve the forced static response, remove phase/collective-coordinate ambiguities, and choose the family shift so that bare mode charge plus DC/family charge has the prescribed total. Nonzero dQ_bg/domega and control of the static inverse are additional hypotheses. These calculations have not been supplied by the second-harmonic radiation solve.

A number-conserving quantum treatment can label initial and final fragment states by exact total U(1) charge. Then a pair-loss event has, schematically in hbar=1 charge units,

    |Q,N> -> |Q-1,N-2> + Psi+(ell4,m4),
    E_bg(Q)+Omega_Q N
      =E_bg(Q-1)+Omega_(Q-1)(N-2)+nu.

For a large slowly varying remnant, dE_bg/dQ=omega gives nu approximately omega+2Omega. Finite-charge recoil/frequency shifts and the DC dressing correct this relation. In a grand-canonical treatment a remnant charge-shift operator or an equivalent collective coordinate is implicit; replacing the rotating background by a c-number does not prove exact charge conservation in the reduced oscillator Hilbert space.

Per leading event, Delta K_mode=-2hbar Omega, Q_out=hbar in the classical Noether-charge normalization, E_out=hbar(omega+2Omega), and J_out=4hbar. The remnant loses Q_out and the corresponding laboratory energy. There is no free omega contribution: its background energy pays that chemical-potential debit. If integer charge is defined as Q/hbar, the emitted integer charge is one. A different quasiparticle-charge convention must give the same total ledger after its background/DC contribution is included.

## 4. Master-equation coefficient: the factor of two

Assume a single oscillator and an initially empty irreversible outgoing continuum admit the rotating-wave interaction, schematically,

    H_int/hbar=integral dk [g_k b_k_dagger a^2 C_bg+h.c.],

where C_bg represents the charge-consistent remnant transition, and the on-shell emitted rotating frequency is 2Omega. The normalization of g_k includes any identical-particle factorial convention. An actual microscopic derivation would normalize the continuum, establish its spectral density, compute these matrix elements and justify eliminating it. None is supplied merely by naming a jump operator.

In the oscillator interaction picture, use the standard dissipator convention

    D[L]rho=L rho L_dagger-{L_dagger L,rho}/2,
    rho_t=kappa D[a^2]rho,

so the jump operator is sqrt(kappa) a^2. Since a^2|N>=sqrt(N(N-1))|N-2>,

    R_events=kappa <N(N-1)>,
    d<N>/dt=-2kappa <N(N-1)>,
    d<K>/dt=-2hbar Omega kappa <N(N-1)>.

There is no further factor of two hidden in the event count: one event removes two mode quanta. A convention writing `2LrhoL_dagger-{L_dagger L,rho}` uses a different named coefficient.

For a charge-tracking remnant the jump is instead schematically `L=sum_Q sqrt(kappa_Q)|Q-1><Q| tensor a^2`, with compatible mode bases and transition frequencies. Replacing it by the oscillator-only jump requires a slowly changing remnant and a justified reduction; it is not an exact charge-complete dynamics for the fragment. Emitted-particle states must carry the opposite charge change in the full system.

For a coherent large-occupation oscillator, <N(N-1)>=|alpha|^4 and K_class=hbar Omega |alpha|^2. Matching the same classical on-shell continuum normalization therefore requires

    2hbar Omega kappa=gamma(hbar Omega)^2,
    kappa=gamma hbar Omega/2.

Thus **kappa=gamma Omega/2** follows in hbar=1 units, conditionally. In the dimensionless action normalization it is `gamma hbar_eff Omega/2`. This is a correspondence requirement, not an independently computed quantum rate. A canonical symplectic mode normalization, the vacuum state, the continuum normalization/density, the same no-half source convention, and a valid weak-coupling/rotating-wave/Markov reduction are all needed to turn it into a physical prediction. Bath memory near thresholds or bound-state resonances can invalidate a time-local Lindblad description even when a monochromatic classical outgoing solution exists.

The closure `<N(N-1)> approximately <N>^2` is not generally preserved by two-particle loss. Even if the initial state is coherent, its later state need not remain coherent. The classical law for the mean is therefore a large-occupation approximation, not an exact quantum equation for every state. Its adiabatic condition includes gamma K/Omega much less than one, alongside small field deformation and no important multimode resonance. Large occupation and weak amplitude must have a common validity window.

## 5. Single-excitation residue and omitted channels

The pair-only jump annihilates |0> and |1>. It preserves oscillator-number parity. A number state with even N can reach zero through this channel; an odd N state stops at one. For a general initial state the dark subspace spans |0>,|1>, so residual mean occupation depends on its parity weights and coherences. A coherent initial state of mean N0 has initial odd-parity probability `(1-exp(-2N0))/2`; the simple pair-only loss model would leave that mean population in |1>. These are exact statements about the conditional jump model, not predictions for a real fragment.

Thus classical decay toward arbitrarily small continuous K cannot be extrapolated through the one-quantum regime. The vacuum's zero-point fluctuations do not become a source with N^2=1/4: the normal-ordered pair factor is N(N-1), which vanishes for zero and one excitation.

The apparent one-excitation residue is not a universal stability theorem. Other processes may remove or redistribute it:

- A permitted one-quantum continuum channel would yield a linear loss operator, but the computed matter thresholds close that direct channel for the selected isolated frequencies.
- Decay or conversion into other discrete/continuum excitations requires their actual spectrum, angular couplings and energy conservation; three targeted Arnoldi shifts do not exhaust those possibilities.
- Higher harmonics, multimode scattering, collisions with other fragments, thermal/stimulated absorption and emission, and changes of the remnant can open channels absent from the single-mode vacuum calculation. Reverse pair excitation in a populated bath also changes the loss-only model.
- Metric/gravitational-wave radiation or additional massless sectors could permit fundamental-frequency quadrupole emission. They are absent from the flat-space matter calculation and require a consistent gravitational completion.
- Quantum tunneling, loop corrections, ultraviolet/renormalization consistency, and finite-Q transitions are uncomputed. Classical lower bounds and finite spectra do not supply those quantum results.

Emission of the second harmonic concerns internal fragment energy and spin. It still gives no amount of mode excitation in an actual merger, conversion of galactic orbital angular momentum into the mode, selective early density histories, surviving dwarf cold-mass inventory, or avoidance of Fornax/Leo I overboost. The useful conclusion is a constrained semiclassical interpretation of an existing classical channel, with its low-occupation and charge-response limits exposed.
