# CFG367 FROZEN CRITERIA: black-hole superradiance against the cold-fluid wave field's mass window (CFG288 road W)
(owner 2026-10-06: "yeah", to reading the field's frequency through black-hole spins; committed before any script)

**Field.** CFG288 road W: a free complex scalar, V = ρ_Λ + m²|Φ|², with no self-interaction. So there is no bosenova escape, and superradiance bounds apply in full.
- Mass window from the record: 2e-20 eV to 37 eV. The L383 floor at 2e-19 eV is reported.
- The field's oscillation frequency is f = m c²/h. A boson cloud radiates gravitational waves at f_GW = 2 m c²/h.

**Data.** Reynolds 2021 (ARAA 59, 117; arXiv 2011.08948), read from the PDF text and transcribed by position into `bh_spins_reynolds2021.csv`.
- **Primary: Table 1, the supermassive holes (X-ray reflection).**
  - Masses are 1σ. I use ±2σ, floored at 0.3× the central value.
  - "~" masses get ±50%, as in Reynolds' Fig. 6.
  - Objects with no mass are dropped.
  - Spin: the lower edge of the 90% range, or the quoted lower limit.
- **Secondary, PROVISIONAL-MASS: Table 2, the stellar holes in X-ray binaries.**
  - This table gives spins only. Every system takes the conservative bracket M ∈ [5, 20] Msun.
  - Spin: the lower edge of the 90% range, using reflection or CF, whichever is lower.

**Physics (units G = c = ħ = 1 per hole).**
- α = G M m/(ħ c) = 7.49e9 (M/Msun)(m/eV). Ω_H = a/(2 r_+), with r_+ = 1 + √(1−a²). Mode (n = l+1, m_az = l) with ω ≈ α(1 − α²/2n²).
- Superradiance condition: ω < l Ω_H.
- Growth rate: Detweiler's formula with its factor-2 correction (l = 1 gives Γ ≈ a α⁹/24):
  - Γ = 2 · 2 r_+ C_nl g_l (l Ω_H − ω) α^{4l+5};
  - C_nl = 2^{4l+1}(n+l)!/(n^{2l+4}(n−l−1)!) · [l!/((2l)!(2l+1)!)]²;
  - g_l = ∏_{j=1..l} [j²(1−a²) + (a l − 2 r_+ ω)²].
- Exclusion: a mass m is excluded by a hole if, for EVERY M on a 9-point log grid across its mass range, some l ∈ {1, 2, 3} satisfies the condition with Γ τ ≥ 200 e-folds.
- τ = 4.5e7 yr (Salpeter) for supermassive holes, and 1e6 yr for stellar holes.

**Output (descriptive verdict).**
- The union of excluded intervals inside the window, per set.
- The surviving window pieces.
- f and f_GW at the edges of each surviving piece, with the detector band: PTA nHz, μHz gap, LISA 1e-4–1e-1, LIGO 10–1e3 Hz.

**Verdict.**
- NARROWS: any part of the window is excluded.
- NO CONSTRAINT: nothing is excluded.
- These are reported separately for the primary set and for primary plus secondary.

**Controls.**
- C1: l = 1 at small α reproduces a α⁹/24 to 1%.
- C2: a = 0 gives no superradiance.
- **MUTATE** (CFG367_MUTATE=1): all spins set to 0. The union must be empty. MUTATE writes separate outputs.

**Scope.** A gravity-only test. The field must exist, but no ambient cold-fluid density is needed. This bounds or locates m; it does not detect it. The cold-fluid amount stays free. κ = ½ is fitted.
