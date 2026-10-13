# CFG686 — does each cluster's measured shear match the law from its own baryons? (FROZEN, before any shear is measured)

Block CFG680–689. Owner "keep going" (2026-10-12) after "so clusters solved?" — no. The framework needs cold-energy mass in
clusters (κ fitted, mechanism missing); CFG663 says the extra sector lenses like mass. Never tested: WHERE, relative to each
cluster's own gas, the lensing mass sits, on raw shear. No NFW, no ΛCDM halo, no mass function.

## Data (all raw; local)
- Shear: KiDS-1000 SOM-gold (`_external_data/kids_lensing_zsplit/`, sha256 dcc2bf03…), e1/e2/weight/Z_B; tangential-shear sign
  convention exactly as the record's validated estimator (real_research/reviews/lensing_rar/lr_esd_remeasure.py v3: e2-flipped);
  multiplicative bias m = −0.01 applied as ΔΣ/(1+m) (KiDS-1000 bins span −0.015..+0.007; disclosed). Sources Z_B > z_l + 0.2, Z_B ≤ 1.2.
- Gas: ACCEPT deprojected Chandra n_e(r) (Cavagnolo+2009; `all_profiles.dat` via the Wayback Machine, sha256 bb762dff…),
  clusters in KiDS-1000 with z ≥ 0.05 and a source-density check (≥ 50% of the blank median within 30').
- Distances: raw DESI DR2 BAO D_M/r_d (CFG681 interpolation) × r_d, with h·r_d = 101.54 Mpc (DESI BAO) and h = 0.70 (ACCEPT's h).
  ACCEPT radii/densities rescaled from their h70 Ω_m 0.3 distances to these (≤ 2% at z < 0.35; disclosed).

## Baryons and the law's prediction
ρ_gas = 1.17 m_p n_e. Beyond ACCEPT's last bin, n_e ∝ r^−β_out with β_out from the last 3 bins (record CFG656 convention), to 3 Mpc;
bracket β_out ± 0.5. Stars (BCG + ICL + members) M* = f* M_gas(<r), f* ∈ {0.10, 0.20, 0.30} (primary 0.20; disclosed literature range).
Law: g = ν_mono(g_bar/a0) g_bar (CFG4_common's committed kernel), both footings (a0 = 9.36e-11 canonical, 1.13e-10 alt).
Lensing mass M_L(<r) = r² g / G (lensing = dynamics, CFG663). ΔΣ_law(R) by numerical projection of ρ_L = (4π r²)^−1 dM_L/dr.
Reference: Newtonian baryons only (a0 → 0).

## Measurement
Per cluster and stacked (inverse-variance by shape noise): ΔΣ_obs(R) in 8 log bins 0.15–3 Mpc, minus the same estimator around
random points (≥ 20 per cluster, same footprint). Errors: bootstrap over clusters for the stack, shape noise per cluster.
Ratio A = ΔΣ_obs / ΔΣ_law in bands INNER 0.15–0.5, MID 0.5–1.2, OUTER 1.2–3 Mpc (stack; also per cluster where S/N ≥ 3).

## Decision rules (stack, primary bracket, both footings must agree; else FOOTING-DEPENDENT)
- LAW SUFFICES: A consistent with 1 (|A − 1| < 2σ) in all three bands.
- CORE EXCESS: A > 1 at ≥ 2σ in INNER and/or MID, OUTER consistent with 1 → the required cold energy sits where the gas is.
- EXTENDED EXCESS: A > 1 at ≥ 2σ in OUTER → mass beyond the law's halo at 1.2–3 Mpc.
- LAW OVERPREDICTS: A < 1 at ≥ 2σ in any band (e.g. the phantom halo too extended for the data).
Reported always: M_extra/M_b(<1 Mpc) implied by A; the β_out/f* brackets; ACCEPT hydrostatic Mgrav vs the law's dynamical mass.
MUTATE: (M1) 45°-rotated (cross) shear must be consistent with 0; (M2) random lens positions give ΔΣ ≈ 0; (M3) a0 → 0 must raise A.
κ fitted; cold energy mass required; not theory closed.
