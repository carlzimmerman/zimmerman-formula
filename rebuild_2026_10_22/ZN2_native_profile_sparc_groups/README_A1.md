# ZN2 AMENDMENT A1 read: BOTH FAIL on the frozen mapping, 18 low-mass zooms now in, no clamp above 1e10. FC1's normalisation passes, so [NORMALISATION-DEPENDENT]

Criteria: `FROZEN_CRITERIA.md` (c3fd993dcc), `AMENDMENT_A1.md` (0a5057caff). `zn2_a1.sh`, `zn2_a1.out`, `zn2_low_shapes.json`. Native z = 0 shapes tagged 1e10–1e14. κ = ½ FITTED; not theory closed.

- 1e10, 1e11: nine seeds each. M₂₀₀/nominal 0.81, 0.78; c₂₀₀ 11.21, 10.26.
- **Frozen mapping (M_t = M₂₀₀/f_c):** SPARC rms 0.0829, median Υ 0.84 and rms 0.0800, Υ 0.81, line FAIL (Υ above 0.80); groups +2.08 ABOVE LAW. 60 of 700 evaluations still clamp below the lowest tag's range.
- **FC1's normalisation (M₂₀₀, R₂₀₀):** rms 0.0777, Υ 0.75 and rms 0.0751, Υ 0.69, line PASS; groups +1.91.
- By V_flat at the FC1 reading, Υ: 20–60 km/s 1.20 (the cap, n 13), 60–100 0.96, 100–150 0.92, 150–200 0.52, 200–250 0.62, 250–400 0.75. So the dwarfs want little or no stars with this much cold mass, and Υ runs against V_flat. A median pass hides that.
- HS1 slope with these shapes: −0.105 ± 0.057 and −0.116 ± 0.059. Weaker than route E's −0.227, not flat.
- Other masses: fair rms 0.134, Υ 1.20; AM1's rms 0.233–0.253, Υ 0.30. AM1 doesn't fit on these shapes.
- MUTATE moves median Υ by +0.36, BITES.

Before these zooms, the clamped read gave Υ 1.01, 0.97. Real low-mass shapes bring that down, and the frozen read still fails.
