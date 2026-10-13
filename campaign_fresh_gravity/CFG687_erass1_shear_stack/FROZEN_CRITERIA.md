# CFG687 — hundreds of eROSITA clusters: raw KiDS shear vs the law from their X-ray gas (FROZEN, before any shear is measured)

Block CFG680–689. Owner "yes" (2026-10-13) to scaling up CFG686 (8 ACCEPT clusters: OUTER A = 1.02 ± 0.24, MID 1.70 ± 0.35 at 1.97σ,
INNER failed nulls). Same estimator, distances and law as CFG686 (verbatim code paths); new: sample, gas profile, mass scaling test.

## Data
- Clusters: eRASS1 main cluster catalogue (Bulbul+2024, VizieR J/A+A/685/A106/emain; `_external_data/cfg687_inputs/erass1_main.tsv`,
  sha256 f098f046…): X-ray positions, zBest 0.05–0.50, Mgas500 (X-ray gas mass, 1e11 M☉) and R500 (kpc). R500 comes from eROSITA's
  ΛCDM-calibrated scaling; it is used ONLY as the aperture radius of the measured gas mass, never as a mass (disclosed).
- Shear: KiDS-1000 SOM-gold, CFG686 estimator (sign, weights, m = −0.01, Z_B > z_l + 0.2, ≤ 1.2); source-density and random checks
  as CFG686 (≥ 200 sources, ≥ 5 good randoms per cluster; randoms 1–3° away, same z_l).
## Gas and the law
Gas ρ ∝ [1 + (r/r_c)²]^(−3β/2), normalised to M_gas(<R500) = Mgas500, truncated at 3 Mpc; primary β = 2/3, r_c = 0.15 R500;
brackets β ∈ {0.6, 0.8}, r_c ∈ {0.10, 0.20} R500. Stars f* ∈ {0.10, 0.20, 0.30} (primary 0.20). Law, lensing mass, projection:
CFG686 RUN3 code (ν_mono, both footings, SIS self-test must pass to < 1%).
## Statistics
Stack weighted by shape noise; errors by jackknife over 30 equal-count sky patches (CFG686 showed shape-noise errors ~1.6× low).
A = ΔΣ_obs/ΔΣ_law in MID 0.5–1.2 and OUTER 1.2–3 Mpc; INNER 0.15–0.5 reported, NOT used (failed nulls in CFG686).
T2 mass scaling: stack in Mgas500 terciles; fit ΔΣ_OUTER ∝ Mgas500^s. Compare s with the law's own predicted s (same pipeline on
the predictions) and with Newtonian baryons (s_N from the same pipeline, ≈ 1).
## Decision rules (primary bracket, both footings must agree)
- T1 as CFG686 on MID/OUTER: LAW SUFFICES / CORE EXCESS (MID ≥ 2σ) / EXTENDED EXCESS (OUTER ≥ 2σ) / LAW OVERPREDICTS (≤ −2σ).
- T2: MASS SCALING FOLLOWS THE LAW if |s − s_law| < 2σ AND |s − s_N| ≥ 2σ; FOLLOWS NEWTON if the reverse; NOT DECIDED otherwise.
- Consistency with CFG686: the 8-cluster OUTER A must lie within 2σ of this stack's.
MUTATE: M1 cross-shear consistent with 0 in MID/OUTER (jackknife); M2 random-minus-random ≈ 0; M3 a0 → 0 raises A.
κ fitted; cold energy mass required; not theory closed.
