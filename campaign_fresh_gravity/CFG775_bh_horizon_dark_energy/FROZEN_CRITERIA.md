# CFG775 FROZEN CRITERIA: black holes, cold energy, dark energy and the horizon

Committed alone, before any script or number. 2026-10-14. Block CFG770–779.
Owner: "i think there is something going on between the black holes, the cold energy, dark energy and the horizon... figure
out the geometric correlation or connection".

Record checked first:
- The a0 ↔ de Sitter horizon link is worked (equation book; 32π campaign: no derivation; dS entropy route gives the form
  a0 ∝ cH, not κ).
- The BH*/LRD coincidence was audited as NOT a framework result (09-22).
- No lane has tested black holes as dark energy's source.

## Part A: geometry (reported, no verdict)
Express every BH / horizon / a0 / tether relation in the framework through the single number q ≡ a0/(cH∞) = κ√(3/8π)
(= 0.1727 at κ = ½):
- r_M = √(GM/a0) vs √(r_s R_H);
- the tether capacity a0/(πG) vs the horizon's mean surface density;
- the black-hole mass whose horizon surface gravity equals a0, vs the horizon mass c³/(2GH∞);
- the Nariai mass.

Gate K1: every relation is reproduced numerically from q alone to 1e-12, i.e. none carries an independent constant.
Class: **ONE COINCIDENCE** if K1 passes.

## Part B: are black holes dark energy's source? (cosmologically coupled BHs, k = 3)
- In the k = 3 hypothesis (Farrah et al. 2023; Croker et al. 2024) a black hole's mass grows as a³. A population formed at
  z_f then has a constant physical density, equal to its density at formation. So
  ρ_DE(z) = ε ∫_z^∞ ψ(z′)(1 + z′)³ |dt/dz′| dz′,
  with ψ the cosmic star-formation-rate density and ε the remnant-BH mass fraction.
- ψ: the Madau & Dickinson (2014) fit to the observed UV + IR luminosity densities (Salpeter mass units), extrapolated to
  z_max ∈ {8 (primary), 15, 30}.
- dt/dz: flat, Ω_m = 0.308 (the framework's flat-a0 value), h = 0.70 (MD14's h).
- ρ_DE0 = 0.692 ρ_crit.
- **B1, amount.** ε_req = ρ_DE0 / ∫…
  - EXCLUDED (stellar remnants alone cannot be the source) if ε_req > 0.05 at every z_max. 0.05 is a generous ceiling: a
    Salpeter-to-top-heavy IMF puts ≲ 1–3% of the formed mass into BH remnants.
  - Pop III bracket (reported): add ψ_III = 1e-3 M☉ yr⁻¹ Mpc⁻³ over z = 10–30 with ε_III = 0.5.
- **B2, shape.** F(z) = ρ_DE(z)/ρ_DE0 (independent of ε). Framework: a0(z)/a0(0) = √F(z).
  - Compare with the F-DESI branch already on the record (DESI CPL w0 = −0.838, wa = −0.62; CFG571's r_desi) over
    z = 0–2.5.
  - MATCHES DESI if max |Δlog10 r| ≤ 0.02, else DIFFERS (reported with the sign).
- **B3, sealed ALMA.** Required gas for GS4_24110 (z 1.997, public 2026-11-28) and U4_27928 (z 1.419, public 2026-11-06)
  under the BH branch, both footings.
  - Computed with CFG571's own `predict` machinery: a0 × r_BH(z), all else identical.
  - Written to `SEALED_BH_BRANCH.json` with its sha256 in the README, before either release.

## MUTATE (CFG775_MUTATE=1)
- M1: k = 0 (no coupling; weighting (1 + z)⁰). F(z) must change, and ε_req rises.
- M2: ε × 10. F(z) unchanged to 1e-12 (the shape is ε-free).

## Hand estimates (before any script)
- A: ONE COINCIDENCE. r_M ≈ 1.70 √(r_s R_H); capacity ≈ 1.4 × the horizon's 4πR² surface density; the a0-surface-gravity BH
  ≈ 2.9 × the horizon mass.
- B1: the (1 + z)³-weighted formed mass is ~1e10 M☉ Mpc⁻³, against ρ_DE0 ~ 8e10 ⇒ ε_req of order a few, i.e.
  **EXCLUDED** for stellar remnants. Pop III with ε = 0.5 may close it.
- B2: F(z) falls toward the past (DE grows with BH production). Probably near DESI's 0.76 at z = 2, but the shape is
  uncertain: hand guess F(2) ~ 0.5–0.8.

## Disclosures fixed now
- Measured BH masses are taken as the coupled masses, as in the k = 3 literature.
- The MD14 fit assumes a luminosity-distance cosmology (mild). The high-z extrapolation is bracketed.
- No ΛCDM mass function or halo model enters.
- κ fitted; cold energy mass required; not theory closed.
