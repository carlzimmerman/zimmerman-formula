# AG4f FROZEN CRITERIA (2026-10-20): is the footing–law pairing physics or a fitting artefact?

Committed alone, before any AG4f script or number. Owner's go (2026-10-20, in chat, "swing it") on the proposal to freeze a
test of the pairing n=1 ↔ canonical footing (ρ_Λ) and n=2 ↔ alt footing (ρ_total).

## What prompted it (seen before this file, disclosed)
AG4b's S3 diagnostic (not graded), with a₀ free and per-galaxy MAP Υ: n=1's best a₀ = 9.333e-11; n=2's best a₀ = 1.148e-10.
Their ratio is R ≈ 1.23. The footing ratio is T = a₀_alt/a₀_canonical = √(ρ_total/ρ_Λ) = 1/√Ω_Λ ≈ 1.2085.

**T is an identity by construction** (both footings are κ = ½ applied to different densities; feedback 10-16). The question
here is only whether SPARC's cross-law ratio R carries information. R is expected to be set mostly by how one law compensates
when fitted to data the other describes, so any world gives a similar R, and it should shrink toward 1 where galaxies sit in
the deep regime, because the two laws share the deep limit √(a₀g_N).

## Pipeline (AG4b's, unchanged)
- Data: CFG4_common.load_sparc(), with AG4b's point and galaxy cuts (170 galaxies).
- Υ_disk per galaxy: MAP under the prior log₁₀Υ ~ N(log₁₀0.50, 0.10); bulge 1.4Υ; s₀ = 0.05 dex; kernels ν₁, ν₂ as AG4b.
- Per law and per galaxy, χ²_min,g(a₀) on a fine grid, log₁₀a₀ ∈ [−10.30, −9.70] in 301 steps (0.002 dex).
  - Sample best a₀ = argmin of Σ_g χ²_min,g; R = a₀,best(n=2)/a₀,best(n=1).
  - σ_R from 1,000 galaxy bootstraps of the summed curves (seed 20261020).

## Worlds and mocks (the by-construction check)
- W1 = (n=1, a₀_canonical) and W2 = (n=2, a₀_alt). For each, 20 mock SPARC sets from AG4b's mock generator (seeds 101–120 for
  W1, 121–140 for W2), refitted with both laws exactly as the data.
- Each world gives μ_W and s_W (mean and SD of the mock R), plus the mock best a₀ per law.
- R_obs is consistent with W when |R_obs − μ_W| ≤ 2√(s_W² + σ_R²).

## Mix dependence
Three splits at the sample median, each declared now:
- (a) deep fraction: the share of a galaxy's points with g_bar(Υ = 0.5)/a₀_canonical < 0.3;
- (b) disk central surface brightness SBdisk (master table);
- (c) gas fraction at the last point, V_gas²/V_bar² at Υ = 0.5.

Each half gets its own R and bootstrap σ. Δ = R(high half) − R(low half), with σ_Δ = √(σ_hi² + σ_lo²).

## Readings
- **NOT DIAGNOSTIC:** σ_R > 0.04, or s_W > 0.04 for either world.
- **PAIRS DEGENERATE (by construction):** R_obs is consistent with both W1 and W2. SPARC cannot tell "n=1 with ρ_Λ" from
  "n=2 with ρ_total": choosing the law fixes the footing on SPARC, but SPARC cannot make the choice.
- **W1 FAVOURED / W2 FAVOURED:** R_obs is consistent with exactly one world.
- **NEITHER:** R_obs is consistent with neither world; the ratio is anomalous and is reported as such.
- **MIX-DEPENDENT** (an addendum to any of the above): any split gives |Δ| > 3σ_Δ. The ratio is then a property of SPARC's
  acceleration mix, and R ≈ T is a numerical coincidence of this sample, not a law of nature.
- **Also reported:** |R_obs − T|/σ_R, and whether each law's best a₀ sits within 2σ of its paired footing (n=1 with canonical,
  n=2 with alt). Bootstrap σ of each a₀ is computed the same way.

## Controls
- K1: on the data, AG4b's S3 values are reproduced to one coarse grid step (0.01 dex): n=1 9.333e-11, n=2 1.148e-10.
- K2: on a W1 mock fitted with n=1, the best a₀ is within 0.02 dex of a₀_canonical (the fitter recovers its truth).

## MUTATE
`AG4F_MUTATE=1` replaces ν₂ with ν₁ in every fit. R must then be exactly 1 on the data and on every mock, and the script exits 1
(the control bites). If it does not, that is recorded.

## Settings
κ = ½ fitted; footings never pooled in any verdict; not theory closed. Runs only after CFG654 NC2x (live at freeze time) ends.
Single thread, nice 10. Outputs: `ag4f.py` → `ag4f.out`, `ag4f_results.json`; MUTATE → `_MUTATE`.
