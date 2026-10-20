# AG4b FROZEN CRITERIA (2026-10-20): SPARC law-form comparison, n=1 vs n=2, with stellar-population Υ, both footings

Committed alone, before any AG4b script or number exists. Owner's go (2026-10-20, in chat): run AG4b and AG4c after the
CFG654 NC2x 1024³ job ends, and seal n=2's ALMA predictions before 2026-11-06 if n=2 survives.

## Question
AG4 (argon_push/AG4_law_from_action, HANDOFF spawn proposal AG4b) showed the frozen action's rest state is the n=1 law, and the
quadratic a₀-line is the n=2 member of the capacity family K W_rem′ = u²/(a₀ − n u). AG3's paired diagnostic, with Υ held fixed,
preferred n=2 by 0.042 dex. Is that preference real once each galaxy's stellar mass-to-light ratio is fitted under a
stellar-population prior instead of being fixed?

## Laws (same a₀ for both; footings never pooled)
- n=1 (canonical; frozen S2; PAPER49): ν₁(y) = (1 + √(1 + 4/y))/2.
- n=2 (quadratic a₀-line, g² − g_bar² = a₀ g_bar): ν₂(y) = √(1 + 1/y).
- y = g_bar/a₀. a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), from CFG4_common.A0 (FP0).

## Data
`campaign_fresh_gravity/CFG4_common.load_sparc()`: the 175 rotmod files and the Lelli+2016 master table, no quality cut
(as in CFG4 and CFG695). A point enters a galaxy's fit only if V_obs > 0, g_obs > 0 and g_bar > 0 at every Υ on the grid.
Galaxies with fewer than 5 such points are dropped (count reported).

## Υ model
- Υ_disk per galaxy, log₁₀Υ_disk ~ N(log₁₀0.50, 0.10): the stellar-population value at 3.6 μm (Schombert & McGaugh 2014;
  Lelli+2016 convention), with CFG4's declared population scatter of 0.10 dex. The prior is NOT taken from any rotation curve.
- Υ_bul = 1.4 Υ_disk (CFG4 convention).
- Grid: log₁₀Υ_disk = log₁₀0.5 ± 0.5 in 201 steps.

## Per-galaxy fit (MAP)
χ²_g(Υ) = Σ_i r_i²/(σ_i² + s₀²) + ((log₁₀Υ − log₁₀0.5)/0.10)², with
r_i = log₁₀g_obs,i − log₁₀[ν(g_bar,i/a₀) g_bar,i], σ_i = (2/ln10)·max(eV,1)/max(V_obs,1) (CFG4), s₀ = 0.05 dex (declared floor
for unmodelled scatter, identical for both laws). Distance and inclination fixed at SPARC values (variant V2 adds them).

## Primary statistic (AG4's "paired law comparison", AG3's form)
- Per galaxy, the velocity-space rms at its MAP Υ: rms_g = √(mean_i (r_i/2)²) dex, for each law.
- d_g = rms_g(n=2) − rms_g(n=1). D = median over galaxies of d_g.
- σ_D from 10,000 bootstrap resamples over galaxies (seed 20261020). z = −D/σ_D (z > 0: n=2 fits better).

## Readings, per footing (AG4 HANDOFF wording, made numeric here)
- z ≥ 3: **n=2 PREFERRED** at ≥ 3σ, so the law form goes back to the owner.
- 2 ≤ z < 3: **LEAN n=2** (tension; canonical not excluded).
- |z| < 2: **NOT SIGNIFICANT**: canonical survives and n=2 is not excluded.
- z ≤ −2: **FLIPS**: n=1 preferred at ≥ 2σ; n=2 disfavoured.
- **Input to the ALMA step:** "n=2 survives AG4b" iff z > −2 on both footings, or the footing is NOT DIAGNOSTIC (power rule).

## Power (decided before the data reading is used)
Mock SPARC sets on the real radii, errors and baryonic components: per galaxy, Υ_true drawn from the prior, a coherent log offset
N(0, 0.05 dex), per-point scatter N(0, √(σ_i² + 0.05²)) in log g; g_obs,mock = ν_true(g_bar(Υ_true)/a₀)·g_bar(Υ_true)·noise.
20 mocks with truth n=1 (seeds 1–20) and 20 with truth n=2 (seeds 21–40), per footing, through the identical pipeline.
- A footing is **DIAGNOSTIC** only if ≥ 80% of n=1 mocks give z ≤ −2 AND ≥ 80% of n=2 mocks give z ≥ +2.
- Otherwise that footing is **NOT DIAGNOSTIC**. Its real-data z is still reported, but it carries no verdict, and n=2 survives
  AG4b on that footing by default.

## Secondary (reported, not graded)
- S1: Σ_g Δχ²_g,min (n=2 − n=1) with its bootstrap z.
- S2: the MAP Υ distribution per law (median; fraction at ≥ 3σ from the prior centre).
- S3: the best global a₀ per law at the per-galaxy MAP Υ (a₀ grid 10^−10.4..10^−9.6), with κ = a₀/a₀(κ=1): does n=2 want a
  different κ?
- S4: the primary statistic restricted to the transition regime 0.3 ≤ y ≤ 3.

## Variants (reported; a changed reading under any variant is disclosed, the primary stands)
V1 σ_Υ = 0.15 dex; V2 CFG4's coherent distance + inclination term added in quadrature to s₀ per galaxy; V3 Q ≤ 2 only;
V4 s₀ = 0.03 and 0.08 dex.

## Controls
- K1: CFG695's global-Υ scan for n=1 is reproduced on the same loader: rms 0.10091 @ Υ 0.60 (canonical), 0.09943 @ 0.55 (alt),
  to 1e-5 (data pipeline identical).
- K2: ν₁(1e-4) = 100.50125 and ν₂(1e-4) = 100.00500; both laws satisfy their algebraic forms to 1e-12 for y ∈ [1e-6, 1e4].
- K3: deep limits agree: |ν₁/ν₂ − 1| ≤ 1e-3 at y = 1e-6.

## MUTATE
`AG4B_MUTATE=1` runs the identical pipeline on the n=1-truth mock with seed 1 in place of the data. It must return FLIPS
(z ≤ −2) on both footings; the script then exits 1 (the control bites). If it does not, that is recorded as a failed control.

## Seen before this file (disclosed)
AG3's fixed-Υ diagnostic (paired −0.0422 dex, corpus v7, a₀ 9.3619e-11); CFG695's n=1 rms 0.1009 @ 0.60 / 0.0994 @ 0.55;
AG4's remark that a 16–25% Υ_disk overestimate absorbs the n=2 preference. No AG4b number at any setting.

## Settings
κ = ½ fitted; footings never pooled; cold-energy mass required; not theory closed. Runs only after NC2x ends (no computation
beside a 1024³ job), single thread, nice 10. Outputs: `ag4b.py` → `ag4b.out`, `ag4b_results.json`; MUTATE →
`ag4b_MUTATE.out`, `ag4b_results_MUTATE.json`.
