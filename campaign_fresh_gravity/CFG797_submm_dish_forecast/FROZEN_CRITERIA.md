# CFG797 FROZEN CRITERIA: forecast for a sub-mm dish-antenna search at the framework-native mass (committed before any script)

**Purpose.** Supply the numbers for a proposal. This is a forecast, not a test.

**Target frequencies.** The ARGON03 native mass is m = (ρ_DE ħ³/c³)^{1/4}, with ρ_DE = 4a₀²/(Gc²). That identification is
equivalent to κ = ½ (fitted, not derived). Report m and ν for both footings: canonical 9.3603e-11 and alt 1.1312e-10.

**Signal.** Dish-antenna power P = (2/3) ε² ρc² · c · A, with ρ = 0.01 M☉ pc⁻³, A = 1 and 10 m², ε = 1e-12.
- Without the 2/3 random-polarization factor, P must reproduce ARGON03's 4.4e7 photons per day per 10 m² (K1).
- Line width Δν = ν σ²/c², with σ = 230 km/s.

**Noise.** Radiometer equation σ_P = k T_sys √(Δν/t), with T_sys = 100, 300 and 1000 K (heterodyne SIS to warm receivers;
provisional) and t = 1 h, 1 day, 30 days.

**Report:**
- SNR at ε = 1e-12;
- 5σ reach ε_min for each setup;
- comparison with the nearest published limit (χ ≲ 1e-8 at 0.67–0.92 meV, JCAP 2018);
- the CFG795 window (ε ≈ 4–6e-9) and the ARGON03 kill sensitivity (1e-12).

**Controls.** K1 as above. K2: the radiometer formula reproduces σ_P = 1.38e-21 W for T = 100 K, Δν = 1 Hz... check units
(kT√(Δν/t) at Δν/t = 1 gives kT = 1.38e-21 W). MUTATE (separate output): ρ → 0 gives SNR 0.

κ fitted; not theory closed.
