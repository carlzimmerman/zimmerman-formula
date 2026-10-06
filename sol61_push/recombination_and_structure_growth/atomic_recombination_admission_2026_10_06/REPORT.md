# Atomic admission requires a calibrated number and temperature current

A comparison between recombination's physical scale factor and the model's uncalibrated coordinate gave an unjustified exclusion. That inference is withdrawn. The actual charged background uses a=1 as a chosen initial slice, not an established present-day slice. Matching its ordinary dust/radiation normalization to a physical hydrogen/photon current yields an explicit admission inequality and positive-F examples. This still does not establish nonequilibrium recombination or last scattering.

Initial actual HEAD: `83b519c1251be83ef6fe6b83b9746e28e658ad08`. All new writes are confined to this folder. Existing atomic_recombination/REPORT.md already derives Saha equilibrium, authenticates Peebles/RECFAST/HyRec sources and supplies a kinetic laboratory. Those source leaves and limitations are reused; its kinetic solver is not rerun. The new result is joint current/temperature calibration against the audited **actual** nonminimal charged background, rather than another imposed ΛCDM/EdS history.

## 1. Exact equilibrium and tracking requirement

Assume homogeneous nonrelativistic, nondegenerate, charge-neutral, ground-state hydrogen, no helium, Planck photons, a common matter/photon temperature T, and chemical equilibrium H↔p+e. Maxwell–Boltzmann chemical potentials, including the ground-state electron spin cancellation, give

    x_e²/(1−x_e)=S(T),
    S=(2πm_e k_B T/h²)^(3/2) exp[−χ/(k_B T)]/n_H,
    n_H=η_H nγ(T), nγ=16πζ(3)(k_B T/hc)³.

In this hydrogen-only screen η_H=η_b. Supply η_b=6.1e−10 and present-reference T0=2.7255 K as independent declared inputs, not values derived from the cold/vacuum action. Use CODATA2022 SI constants. The binding χ=hcR∞/(1+m_e/m_p)=13.5982873 eV is a declared leading reduced-mass Coulomb approximation; relativistic/level/finite-size corrections and the reduced-mass correction to the translational prefactor are omitted. Extra decimals in computed roots do not imply atomic-model accuracy.

The equilibrium milestones are

| x_e | T (K) | physical a=T0/T | χ/(k_BT) |
|---|---:|---:|---:|
| .9 | 4037.82 | .000674993 | 39.0809 |
| .5 | 3759.60 | .000724944 | 41.9730 |
| .1 | 3436.87 | .000793017 | 45.9143 |

The large dilute-gas entropy, rather than k_BT≈13.6 eV, accounts for neutralization far below the binding energy. These are equilibrium milestones, not observed redshifts, photon last-scattering times or outputs of the candidate action.

A minimal kinetic reduction makes the missing timescale explicit. In the conventional effective hydrogen shell approximation,

    xdot=−C[α_B n_H x²−β_eff(1−x)],
    β_eff=β_2 exp[−E21/(k_BT)], β_2=α_B(2πm_e k_BT/h²)^(3/2)exp[−E2/(k_BT)],
    E2=χ/4, E21=3χ/4,
    C=(Λ_2s+R_esc)/(Λ_2s+R_esc+β_2),
    R_esc=8πH/[λ_Lyα³ n_H(1−x)]

under optically thick Case-B/quasi-static excited-state and expanding Sobolev assumptions. The shell convention is pinned to the existing RECFAST primary; statistical factors cannot be transplanted from another shell convention. The exact Sobolev probability is (1−exp(−τS))/τS with τS∝n_lower/H. Thus H controls photon escape as well as temperature/time conversion. This rate formula is a conditional reduction, not a completed multilevel transport model on the carrier action.

Linearizing the kinetic equation about its instantaneous equilibrium, the derivative of C multiplies a vanishing net rate. Therefore the relaxation rate is

    Γ_rel=C α_B n_H [2x_S+S].

For conserved η_H and T∝a⁻¹,

    dx_S/dln a = x_S(1−x_S)/(2−x_S) [3/2−χ/(k_BT)].

Writing x=x_S+δ gives δdot≈−Γ_rel δ−xdot_S. Small *relative* tracking error requires Γ_rel/H≫|dln x_S/dln a|, not merely Γ_rel/H≫1. At the .9,.5,.1 milestones the right-hand side is 3.4164,13.4910,21.0383. This is a concrete necessary local tracking screen, not a computation of Γ_rel on the candidate, whose atomic rates and physical H clock are not yet specified. When photoionization is negligible, the conditional equation instead gives 1/x(a)=1/x(a_i)+∫ Cα_B n_H/H dln a, exhibiting the freezeout dependence on both physical rates and expansion.

## 2. The calibration theorem

Use a_m for the background coordinate. Its separately conserved ordinary densities are ρd=ρd,ref a_m⁻³ and ρr=ρr,ref a_m⁻⁴ with ρd,ref/ρr,ref=100. Ratios use common energy units. Let f_b∈(0,1] be the hydrogen rest-energy fraction of ordinary dust and fγ∈(0,1] the thermal-photon energy fraction of ordinary radiation. Remaining dust is atomically inert in this declared screen; its microscopic identity is not inferred. Remaining radiation has the same ideal equation of state; a thermal photon component is an additional premise, not a consequence of p=ρ/3.

Conserved number and Planck temperature imply

    Tγ=T_ref/a_m, n_H=η_b nγ(T_ref)a_m⁻³,
    ργ(T)=8π⁵(k_BT)⁴/(15h³c³),
    mean photon energy = [π⁴/(30ζ(3))] k_BT ≡ μγ k_BT.

Matching f_bρd=m_pc²n_H and fγρr=ργ gives exactly

    f_b = fγ η_b m_pc²/[100 μγ k_BT_ref],
    T_ref = T_* fγ/f_b, T_*=24.5885282 K.

Thus model a_m=1 corresponds to physical a_ref=T0/T_ref, with a_phys=a_ref a_m. These are necessary simultaneous number/energy calibration equations. They do not establish that the chosen scalar branch, fractions, thermal spectrum or present epoch are a complete observationally calibrated cosmology. The ionization binding-energy fraction is negligible for this rest-energy matching approximation.

Setting T_ref=T0 and fγ=1 would require f_b=9.02166>1, exceeding the total ordinary dust. Thus the particularly simple present-day/all-photon identification is inconsistent with the supplied η_b and model ratio; changing the fractions or the reference slice changes that premise. This does not exclude calibrated models.

Let a_g be the inspected positive-F guard endpoint and [T_min,T_max] a specified equilibrium interval. It lies wholly inside the inspected past coordinate interval (a_g,1] precisely when

    a_g < T_ref/T_max and T_ref/T_min ≤ 1,
    a_g T_max/T_* < fγ/f_b ≤ T_min/T_*.

This exact reparameterization criterion is conditional on the background remaining admitted on the intervening interval. The parent's numerical F=1e−8 guard is an inspected endpoint, not an analytically certified all-history singularity. It must not be assigned a physical redshift before temperature calibration.

For the .9→.1 Saha interval the common upper ratio is approximately 139.78, and the lower threshold ratios are 1.569886 (ξ100) and .3072352 (ξ1000). Here a_g≈.0095599065 and .0018709253 respectively, read from the tighter DOP853 parent record. The bare coordinate comparison to a≈.0009 has no calibration-independent force.

## 3. Constructive bounded admission screens

Two declared calibrations supply useful controls:

| (f_b,fγ) | T_ref (K) | a_ref | ξ100 all milestones? | ξ1000 all milestones? |
|---|---:|---:|---|---|
| (1,1) |24.5885|.110844|no|yes|
| (.16,.6)|92.2070|.0295585|yes|yes|

For each admitted case only, integrate the actual parent background with DOP853 to the three remapped atomic milestones (rtol3e−10,atol3e−15,nfev bound15000). The unchanged Friedmann root, full nonminimal trace and conserved charge are used. No prescribed radiation R=0 or equilibrium recombination stress is inserted into its dynamics. The sampled F values over these milestones are .79965–.84090 for ξ1000/(1,1), .71570–.77572 for ξ100/(.16,.6), and .97113–.97731 for ξ1000/(.16,.6). Charge and actual Friedmann constraints are checked. These are bounded numerical admissions, not interval positivity certificates or full perturbative health.

This gives an explicit candidate with enough coordinate/temperature domain to pose the atomic problem, rather than falsely excluding both histories by a scale-factor label. It does not prove that either arbitrary fraction choice evolves to the present universe, or that F can be crossed healthily. The carrier's effective Jordan-frame carrier density on the fixed-M Einstein-equation right-hand side at these nodes is negative in the tested examples; it is not added to the hydrogen number current.

## 4. Two distinct remaining arrows

First, history admission requires a physical thermal-photon component, conserved atomic baryon number, temperature/energy calibration, dimensional expansion clock and a healthy actual background spanning the relevant interval. The inequalities and finite examples address part of this arrow; positive F alone is not full health. The earlier proposed uncalibrated no-recombination inference has been withdrawn.

Second, the admitted history must supply atomic reactions and photon transport: nonequilibrium level populations, line/two-photon escape, matter-temperature exchange and Thomson opacity. Optical depth τ=∫ cσ_T n_H x_e/H dln a depends on H and a complete x_e history; an equilibrium x_e=.5 milestone is not its visibility peak. A pressureless dust current plus p=ρ/3 radiation in the action does not itself supply those operators or establish photon microphysics. The existing atomic laboratory demonstrates the distinction on its own declared cosmological background, not on this carrier action.

No cold-particle identity, 32π selector, observed last-scattering redshift, CMB likelihood or full recombination completion is claimed. The novelty here is only the project-specific exact calibration/admission condition and its remapped actual-background witnesses. Current bounded checks, controls and hashes are recorded separately in RUNS.md; REPORT is outside executable inputs.
