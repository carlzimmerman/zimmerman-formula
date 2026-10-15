# CFG789 FROZEN CRITERIA: how fast can cold energy turn into light, and what would a light drive need?

Committed alone, before any script. 2026-10-15. Block CFG780–789 (last ID). Owner: "lets figure it out" (propulsion that
emits only soft white light, powered by cold energy).

## Question
- Any channel turning cold energy into optical photons would act on all cosmic cold energy, so the sky would glow.
- The measured cosmic optical background (COB) therefore caps the spontaneous conversion rate Γ.
- From that cap, compute:
  - (i) the ceiling on light power from ambient cold energy in a craft-sized volume;
  - (ii) the stimulation factor S a device would need to give 1 N of thrust (300 MW of light).

## Declared inputs (PROVISIONAL, from memory)
- COB excess allowed above integrated galaxy light: I_ex ≤ 8 nW m⁻² sr⁻¹ (New Horizons LORRI-era range).
  Brackets: 2 and 16.
- Cosmic cold energy ρ_c = 0.26 × ρ_crit (h = 0.70).
- Local cold energy near the Sun ρ_loc = 0.01 M☉ pc⁻³. Brackets: 0.005 and 0.02.
- Production over the age t_H = 13.8 Gyr. Redshift dilution factor f_z = 0.5 (order of magnitude; brackets 0.2 and 1).

## Calculation
- u_ex = 4π I_ex / c.
- Γ_max = u_ex / (ρ_c c² t_H f_z); τ_min = 1/Γ_max.
- Ambient power ceiling P(V) = ρ_loc c² V Γ_max, for V = 1 m³, 1 km³ and a 1 km-radius sphere.
- Required S = 300 MW / P(1 km³).
- Eye-safe hull area for 300 MW at radiance 100 W m⁻² sr⁻¹: A = P/(π L).

## Classes
- **DATA-CLOSED for ambient fuel** if P(1 km³) < 1 W. A device would then need stimulated conversion by the reported S;
  that is new physics with no mechanism in the record.
- **OPEN** otherwise.

## Controls
- K1: the arithmetic of u_ex and the τ_min units is checked against a hand value (u_ex ≈ 3.4e-16 J m⁻³ at 8 nW).
- MUTATE (CFG789_MUTATE=1): I_ex × 10⁸ (a hypothetical glowing sky). P(1 km³) must scale by 10⁸.

## Hand estimate
τ_min ~ 10¹⁵–10¹⁶ yr; P(1 km³) ~ 10⁻¹⁹ W; S ~ 10²⁷; A ~ 1 km². **DATA-CLOSED for ambient fuel.**

κ fitted; not theory closed. This bounds spontaneous conversion only. A stimulated channel would be new physics.
