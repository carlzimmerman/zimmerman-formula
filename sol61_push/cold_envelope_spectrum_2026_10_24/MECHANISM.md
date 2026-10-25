# CCT-008: a supported envelope instead of runaway condensation

This is a conditional extension of the new CCT selective-coupling candidate. It is not current Khronon/AeST theory, retired SCT-M, a cosmological derivation, or an established description of dark matter. The benchmark profiles are inherited from CCT-006; matching them retains their calibration and limitations.

## 1. A sharp correction to the previous wave scale

For a coherent field psi=sqrt(rho) exp(i S),

    T = eta²/2 integral |grad psi|² dV
      = eta²/2 integral |grad sqrt(rho)|² dV
        + eta²/2 integral rho |grad S|² dV
      >= T_Q.

The same lower bound holds for a sum of positive orbital densities by Cauchy–Schwarz. For a Plummer density of mass M and scale b, direct integration gives

    T_Q/M = 15 eta²/(28 b²).

A stationary isolated configuration with vanishing surface stress requires

    2T = integral rho r (dPhi_c/dr + dPhi_b,N/dr) dV,
    integral rho r dPhi_c/dr dV = 3 pi G M²/(32 b).

Thus eta has an upper ceiling for EACH chosen target profile. The old eta=3000 pc km/s violates this necessary condition for the chosen Draco and Leo I profiles. More cooling cannot fix that incompatibility while preserving these density targets. The ceilings from the present stellar potentials are approximately 2763 (Draco), 29380 (Sextans), 7544 (Fornax), and 2483 (Leo I), all in pc km/s. These are conditional profile constraints, not measured particle masses or universal data bounds.

The tested common value eta=1500 is below all four ceilings. This value was selected after the 3000 and 2000 failures; it is a disclosed parameter adjustment, not predicted from Lambda or a0.

## 2. Retain orbital support in an extended envelope

A single coherent collapse can dump too much mass into the centre. A possible endpoint is instead a field with a spread of bound mode occupations. Introduce a positive density matrix Gamma, with mass normalization Tr Gamma=M:

    i eta partial_t Gamma = [H[Gamma], Gamma],
    H = -eta² lap/2 + Phi_c + Phi_b,N,
    rho_c(x)=Gamma(x,x),   lap Phi_c=4 pi G rho_c.

Rank-one Gamma recovers the coherent wave equation. Higher rank is an additional statistical/random-phase closure. It is NOT obtained merely by relabeling one pure wave; the interference and gravitational fluctuation terms must be justified if a coherent parent is retained.

For radial eigenfunctions u_nl, normalized integral |u_nl|² dr=1,

    [-eta² d²/dr²/2 + eta² l(l+1)/(2r²) + Phi_c+Phi_b,N] u_nl = E_nl u_nl,
    Gamma = sum_nlm N_nlm |nlm><nlm|,  N_nlm>=0,
    rho_c = sum_nlm N_nlm |u_nl(r)|² |Y_lm|²/r².

Equal m occupations at fixed n,l produce a spherical density. Nonnegative bound-state weights can reconstruct all four chosen profiles at eta=1500. The Sextans construction uses substantial high-l support: the finite L<=4 library fails badly even with many radial excitations, whereas the larger library succeeds. The weights are nonunique and were fitted to the target density. Neither their initial production nor their selection by galaxy history has been derived.

## 3. Net spin can be stored without increasing the density

Because |Y_l,m|²=|Y_l,-m|², transferring occupation from -m to +m at fixed pair sum changes Jz but leaves rho and its gravitational potential unchanged. Starting with equal m weights, complete polarization of all pairs gives the constructive capacity

    Jz_max/M = eta sum_nl f_nl l(l+1)/(2l+1),

where f_nl is that radial shell's total occupation divided by M. Any smaller aligned Jz is reached by partial polarization. This is net angular momentum storage, not an identification of net spin with its dispersion. It adds no extra mass or extra gravity.

For the refined Sextans reconstruction, capacity is ~7277 pc km/s per retained unit mass. The old CCT-007 angular shape has mean m~0.7856, hence at eta=1500 its initial j~1178 pc km/s. Even retaining the full benchmark source J in the 425-million-Msun final envelope would require only ~2521 pc km/s: the constructed envelope has capacity. This is a kinematic storage result; it does not demonstrate torque-mediated delivery to these modes.

Draco, Fornax and Leo I remain different: with the old common 200-times-formed baryon source and the present fitted occupations, at least ~98.4%, 99.65%, and 99.91% of that source spin must leave, respectively. These are conditional on THIS fit and oversized source prescription, not universal no-go bounds. A much smaller captured supply or a different permitted outer envelope changes them. Thus fixing Sextans' storage does not automatically solve supply/selection in the controls.

## 4. Energy transport and stellar gravity

The Hamiltonian is

    E = sum_nlm N_nlm integral [eta² |grad phi_nlm|²/2 + Phi_b,N |phi_nlm|²] dV
        + (1/2) integral rho_c Phi_c dV.

Cold mass sources Phi_c once. Stars feel the previously stated selective action's baryon-only law plus this Newtonian cold contribution. Cold modes feel baryonic Newtonian gravity, not an added baryonic Xi charge. No wave energy is counted a second time as extra gravitating mass in these Newtonian tests.

The occupation evolution above is conservative and does not itself cool. Formation must include actual outgoing positive-energy field flux, with mass/E/vector-J accounting. Earlier CCT-007 runs demonstrate finite-mode emission but form the wrong profile. The present construction supplies a possible supported endpoint, not the missing connecting trajectory. Unequal +/-m weights alone cannot manufacture angular momentum or shed energy.

Static mass-profile compatibility prevents the previous overboost in the calibrated stellar moments. It is not a stellar-heating result. Pure-field interference, nonspherical instabilities, live stellar distribution functions, tides and the origin of the retained mass still require separate tests.

## 5. A specific formation route to test

Project the coherent parent into spatial modes phi_alpha. Its self-gravity gives a conservative four-wave interaction,

    i eta dot a_alpha = sum_beta H_b,alpha,beta a_beta
                       + sum_beta,gamma,delta U_alpha,beta,gamma,delta
                         a_beta a_gamma a_delta*,
    U = -G integral d³x d³y phi_alpha*(x) phi_beta(x)
                             phi_gamma(y) phi_delta*(y) / |x-y|.

Azimuthal symmetry gives m_alpha+m_delta=m_beta+m_gamma. This allows opposite-sign angular mode population while conserving total Jz. The physical candidate is collapse-driven gravitational mode mixing into a supported envelope, with positive-energy waves exporting the excess binding energy and residual spin. It requires neither a binary collision term nor new dissipative drag. The matrix-density calculation only tests the endpoint and radial response; it does not measure these nonlinear transfer rates.

Exact seed symmetries matter. The old initial l=0,2 state is inversion even and has only even m. Its exact coherent evolution preserves those symmetries. Repeating the endpoint reconstruction with EVEN l only still meets the stated 5% aperture/potential criterion, including an excellent Sextans fit, but that does not remove the separate even-m restriction. An all-m spherical ensemble cannot be declared reachable from that exact seed. A physically justified nonsymmetric perturbation, or a nonspherical endpoint respecting the seed, must be specified and evolved. Do not erase this issue by calling arbitrary mode occupations 'virialization'.
