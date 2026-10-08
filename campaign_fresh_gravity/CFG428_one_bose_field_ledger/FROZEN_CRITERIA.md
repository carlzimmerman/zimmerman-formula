# CFG428 FROZEN CRITERIA: can ONE Bose field satisfy every mass constraint on the record? (door 2 of the 10-07 list)
(owner relayed a ten-door list on 2026-10-07. Committed before the script was run.)

**Constraints, read from the record:**
- CFG383: clusters half-unsettled at R500 as an ideal Bose gas gives m = 0.62–1.04 eV.
- CFG474: the surviving windows are 3.0–3.9e-19 and 5.3e-17–37 eV. The light end is closed by UFD heating.
- CFG479: a depletion-driven normal fraction ν = 0.05–0.3 needs a scattering length a = n^{-1/3}(3√π ν/8)^{2/3}.
- Bullet Cluster: σ/m < 1 cm²/g, with σ = 8πa² for identical bosons.

**Densities.** Cluster R500 local density ρ = 1.55e-24 kg/m³ (CFG382/T15), with the cold share (1 − f_b). σ_v = 1000 km/s.

**Tests.**
1. **Window:** CFG383's m lies inside a CFG474 window.
2. **Depletion route:** at m in CFG383's window, the CFG479 a gives σ/m. The route is DEAD if this exceeds the Bullet limit by > 10×.
3. **Thermal route:** the largest Bullet-allowed a gives a relaxation time with Bose enhancement, t = 1/(n σ v (1 + 𝒻)), where 𝒻 = n(2πħ)³/(m³(2πσ_v²)^{3/2}) is the phase-space occupation. It is ALLOWED if t ≤ t_H = 13.8 Gyr for some m in the window, and STARVED otherwise.
4. **Production (reported):** a 0.8 eV boson in thermal equilibrium would be hot dark matter. It must be produced non-thermally. This is stated, not computed.

**Verdict.**
- **ONE FIELD VIABLE:** tests 1 and 3 pass. Report the depletion verdict as well.
- **ONE FIELD DEAD:** test 1 fails, or test 3 is STARVED across the whole window.

**MUTATE.** σ/m limit × 1e40. This makes the depletion route Bullet-safe, so test 2 must flip.
