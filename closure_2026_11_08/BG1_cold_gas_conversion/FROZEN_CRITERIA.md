# BG1: cold-gas conversion key for the K(Q) dust component. FROZEN CRITERIA (committed alone, before any number)

Lane class: TEST (owner decision closure_2026_11_08/OWNER_DECISION_2026-11-08_BG1_LAUNCH.md). Adopts nothing.

## Mechanism under test
The K(Q) sector has two phases: dust (clusters, carries the CMB need of 5.41 x baryons at z 1100, F1A) and smooth fluid
(non-clustering today, carries the expansion term omega_X 0.108, CMB1). Dust converts to the smooth phase at a rate
  Gamma(x,t) = alpha * rho_cold(x,t),
where rho_cold is the local density of baryons with T < 1e4 K (neutral + molecular gas). Ionized gas (IGM, ICM, z > 1100
plasma) and stars do not convert. The retained dust fraction of a parcel is f = exp(-alpha * E), E = integral of rho_cold
along its orbit over cosmic time. alpha is the lane's ONE declared parameter, scanned over [1e-3, 1e3] in units of
(M_sun pc^-3 Gyr)^-1 on a log grid of 61 points; the verdict is whether any alpha passes every gate on a footing.
Both footings graded separately (a0 1.2e-10 canonical, 1.1e-10 alt), never pooled.

## Exposure model (frozen)
- Disc galaxies: component on an isotropic halo distribution crosses the disc; E(r) = N_cross(r) * Sigma_cold(r) * 2 / v_z(r),
  N_cross = t_exposed / T_orbit(r). Sigma_cold today from the SPARC HI profiles (helium factor 1.33) plus H2 from the frozen
  SPARC bulge/disc H2 rule already used by the record (cite the file). Past gas: Sigma_cold(t) = Sigma_cold(0) * G(t) with
  G(t) the frozen rule M_gas(t)/M_gas(0) = 1 + (M_*(0) - M_*(t))/M_gas(0) (gas consumed into stars), M_*(t) from the
  system's star-formation history class (early-type: formed by z 2; late-type: constant SFR). t_exposed = age of the disc.
- Quenched systems (ellipticals, dSph, Coma UDGs): exposure accumulated only during their gas-rich phase, length from the
  frozen class rule (ellipticals 2 Gyr ending at z 2; LG field dSph 3 Gyr ending at z 2; M31 bright dSph 4 Gyr; Coma UDG
  4 Gyr ending at infall z 1). Each class length is a frozen number; it is NOT a fitted quantity.
- Clusters and groups: ICM is hot (no conversion); member galaxies convert their own halos only; the cluster's retained
  share is 1 - (member halo share converted), with the member halo share from the record's MB1 member-mass sums.
- Cosmic: converted fraction history f_conv(z) from the cold-gas density history Omega_HI(z) (DLA raw data) + H2 (raw
  CO-based) applied to the halo exposure model summed over the raw stellar-mass function; dark ages z 20-1100: mean-density
  neutral gas, E_dark = integral rho_b(z) dt over z 20-1100.

## Gates (each gate reported on both footings; FAIL if any gate fails at every alpha)
- G1 SPARC rotation curves: law + retained component. rms over the lane's frozen SPARC set must not exceed the law-only
  rms by more than 0.01 dex and the mean residual must stay within |0.05| dex. Sub-gate G1b: gas-rich low-density discs
  (Sigma_cold(2.2 h) < 10 M_sun pc^-2) alone, same bounds.
- G2 KiDS isolated-lens lensing (Brouwer 2021, 59 points, the record's gate in QX7 iter_4 FROZEN_CRITERIA.md:26):
  |shift| <= 0.05 dex.
- G3 X-COP (record gate: |mean| <= 0.05, rms <= 0.10 in log M over 50 kpc to r500): retained component at f_ret x
  (omega_X/omega_b) x M_b with a cold-collapse profile whose concentration is a reported nuisance in [2, 10]; FAIL if no
  concentration passes. No LambdaCDM-fitted concentration enters.
- G4 Groups (Lovisari 20 groups, the record's gate in QX7): >= 16/20 within the need band.
- G5 Coma UDGs (EV1 gate): residual within 2 sigma of the need.
- G6 LG field dSph (DX1 gate): |mean| <= 0.10 dex; M31 bright dSph (ST1 gate): within 2 sigma of +0.214.
- G7 Ellipticals: graded under BOTH readings on record (ST1 IMF reading: need ~ 0 -> f_ret <= 0.1; HX1 reading: need
  B 4.2 -> f_ret >= 0.9); PASS if either reading is met; the lane reports which.
- G8 Forest (DESI P1D gate of NC2): converted fraction by z 2 <= 0.03.
- G9 Dark ages and primary CMB: converted fraction by z 20 <= 0.01; zero conversion at z >= 1100 by construction, so the
  F1A need (5.41) is carried unchanged.
- G10 Growth: CMB-lensing growth gate (QX3 ODE on raw Planck PR4 bandpowers, Delta chi^2 <= 4, as QX7 iter_3
  FROZEN_CRITERIA.md:24) and raw fsigma8 points within 2 sigma, with the cosmic converted fraction f_conv(z) removed from
  the clustering component.

## Label rule
PASS on a footing iff one alpha passes G1-G10 on that footing. FAIL iff every alpha fails at least one gate. NO VERDICT
only if a gate is NOT EVALUABLE for lack of a framework-native input (name it; do not import).

## MUTATE (must bite; each run writes separate outputs *_MUTATE.json)
- M1 catalyst swapped to hot gas (T > 1e6 K): must FAIL G3 (over-clears clusters) at every alpha.
- M2 alpha -> 0: must FAIL G1 and G2 (full component in galaxies).
- M3 alpha -> 10 alpha at the best alpha: must flip at least one of G5, G6.
- KA replay: criteria hash in every output; replaying with a wrong exposure scale (x10) must flip a gate.

## Operational
Heavy compute preemptible (SIGTERM checkpoint), RSS < 1 GB, no edits to other lanes' files, outputs under this directory,
commit with explicit paths, push via temp worktree. Message the "Theory completion" session:
"BG1 RESULT: <label can / alt> (criteria <hash>, result <origin hash>)".
