# CFG665 FROZEN CRITERIA: is thermal equilibrium the selector? (isothermal settled cold energy with a universal edge)

Date: 2026-10-12. Written and committed ALONE, before any CFG665 code or score. Block CFG660–669 (CFG662 and CFG664 were declared
moot in MECHANISM_JOINT §5 and are not used). Nothing below may be edited after this commit.

κ = ½ is fitted. Footings (9.3603e-11 canonical, 1.1312e-10 alt) judged separately, never pooled. The cold energy's mass is
required. No particle species. Not "theory closed". Nothing will be phrased as "the data favour the framework". Raw SPARC
rotmod only (the record's CFG4 harness, Υ = 0.61). The law's kernel ν is NOT used in the prediction.

## 0. What has been seen (stated before any choice below)

- CFG461: no c-free mechanism can set σ⁴ = G M_b a₀/4 (Buckingham c-test); max entropy alone picks cored states, not the SIS;
  C3b (edge pressure a₀²/8πG) leaves σ free; R0 control (cosmic share inside the law's r_edge) gets the amplitude within 0.07 dex.
- CFG462: σ⁴ is exact if settling stops where the law's boost equals Ω_m/Ω_b (edge 5.85 r_M). CFG488: co-settling of the present
  baryons' share supplies that edge only as a restatement.
- cm08 (record): galaxies retain about 0.13 of the cosmic cold share, groups about 0.6, close to their baryon retention.
- This author's derivation (no data seen): for an isothermal sphere M_tot(<r_e) = 4σ⁴/(G g_e); with M_tot = M_b/f_b (co-retained
  cosmic share) and g_e = f_b a₀ this gives σ⁴ = G M_b a₀/4 exactly, f_b cancelling. The edge condition equals the deep law
  evaluated at one radius (g·M_tot = a₀·M_b): the law is reduced to one boundary number, not removed. For a singular isothermal
  sphere the edge pressure is P_e = g_e²/8πG = (f_b κ)² ρ_DE c²/8π.
- **Author's expectation, before any score:** an isothermal (Boltzmann) halo concentrates cold energy as e^(−Φ_b/σ²) in deep
  baryonic centres, so high-surface-brightness inner regions are likely to fail; low-surface-brightness discs may pass.

## 1. Model S* (no fitted constant; inputs κ through a₀, f_b = 0.02237/0.14237, the cosmic ratio 5.364)

Per galaxy, spherical: M_b(<R) = g_bar R²/G at the harness's good points (g_bar > 0), linear in R between points,
M_b(<r) = M_b(R₁)(r/R₁)² inside the first point, constant beyond the last; M_b ≡ M_b(<R_last).
Settled cold energy is isothermal in the total potential: dρ_c/dr = −ρ_c G[M_b(<r) + M_c(<r)]/(r²σ²), dM_c/dr = 4πr²ρ_c.
Three conditions fix (σ, ρ_e, r_e):
1. supply: M_c(<r_e) = 5.364 M_b;
2. edge acceleration: G[M_b(<r_e) + M_c(<r_e)]/r_e² = g_e ≡ f_b a₀;
3. edge pressure: ρ_c(r_e) σ² = P_e ≡ g_e²/(8πG).
Conditions 1–2 give r_e; condition 3 gives ρ_e for each σ; σ is the root of M_c(r → r_min) = 0 when integrating inward from r_e
(regularity at the centre, r_min = 1e-3 R₁). If no root exists in σ ∈ [5, 2000] km/s the galaxy is UNSOLVABLE.

Prediction at each good point: g_pred = G[M_b(<R) + M_c(<R)]/R².

## 2. Checks

- **K1 (deep control):** a Hernquist sphere with a = 0.01 r_M: σ⁴/(G M_b a₀/4) within 0.05 dex.
- **D1 (DATA):** the harness's weighted rms of log g_obs − log g_pred over all good points of solvable galaxies, per footing,
  against the law's rms on the same points.
  - **S\* VIABLE** if rms_S* ≤ rms_law + 0.02 on both footings, |mean residual| ≤ 0.05 dex and ≤ 10% of galaxies UNSOLVABLE;
  - **S\* TENSION** if rms_S* ≤ rms_law + 0.05 on both footings;
  - **S\* FAIL** otherwise.
- Reported, no verdict weight: rms in bins of g_bar (inner high-g vs outer low-g); rms for the half of galaxies with the lowest
  central surface brightness proxy (g_bar at the first point) vs the highest half; the BTFR slope of predicted V at R_last.
- **MUTATE (`CFG665_MUTATE=1`, exit 1 iff both bite):** M1, g_e = a₀ (f_b dropped): D1 rms must rise by ≥ 0.05 dex on the canonical
  footing; M2, supply × 2: σ⁴ in K1 must move by ≥ 0.1 dex.

## 3. Machine rules

Light: one process, `nice -n 10`; allowed while the 1024³ run is live.
