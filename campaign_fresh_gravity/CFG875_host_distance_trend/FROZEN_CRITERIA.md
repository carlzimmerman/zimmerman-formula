# CFG875 — FROZEN CRITERIA: does the dwarf excess fade with distance from the host at fixed g_bar?

Frozen before any script (owner block 870–879; owner asked for this test in chat). κ = ½ fitted; not theory closed.

## Why, and an honest label
The two readings of the dwarf excess make opposite predictions:
- **Environmental** (something a host does): the excess fades from ~+0.4 dex inside ~300 kpc to ~0 beyond ~1 Mpc, a slope of
  about −0.4 dex per dex of host distance at fixed g_bar.
- **Universal small-system component** (CFG870's cored cold component, σ ≈ 7.5 km/s, r_c ≈ 100 pc, in every dwarf): no trend.

CFG874 found the isolated dwarfs 0.10 ± 0.09 below satellites (undecided). **Post-hoc motivation, disclosed:** this test was
suggested by a CFG874 variant (the ≥ 500 kpc dwarfs sit near the law). It uses the same dwarfs, so it is weaker evidence than
a test on new objects. Its added value is that it uses the full continuous range of host distance (≈ 20 kpc–1.35 Mpc),
including the distance spread inside the satellite population, rather than a 300 kpc split.

## Sample and estimators (identical to CFG874's primary, so per-dwarf Δ are the same numbers)
- LVD MW + M31 + local-field dwarfs with measured stellar σ (no upper limit), r_h, M_V, MW and M31 distances; CFG852's
  rotating / gas-rich set excluded. All groups used: satellites with or without HI (S, SG) and isolated (I).
- Υ_V = 2; gas inside r12 counted for every HI-detected dwarf (Wang+16 exponential disc, extended root; fallback R_HI/2).
- r12 = (4/3) r_h; g_obs = 3σ²/r12; g_bar = G (M*/2 + M_gas,in)/r12²; Δ = log10(g_obs/(g_bar ν_e(g_bar/a0))); footings
  9.3603e-11 (primary) and 1.1312e-10, never pooled.
- d_host = min(distance_gc, distance_m31) in kpc.
- g_bar window: CFG874's, [min_I − 0.5, max_I + 0.5] in log g_bar (it removes the lowest-g ultra-faints, which are all close to
  the MW and most exposed to binary inflation).

## Statistic
Unweighted least squares: Δ = a + b (log g_bar + 12.5) + k (log10 d_host − 2.5). **k** = change in excess per dex of host
distance at fixed g_bar. Errors: bootstrap over dwarfs, 4000 draws, seed 875. Also reported: the partial Spearman ρ between Δ
and log d_host after removing the linear g_bar trend from both.

## Classes (canonical primary; the alternative footing must agree, else UNDECIDED)
- NOT DIAGNOSTIC: se_k > 0.20 (cannot separate 0 from −0.4 at 2σ).
- ENVIRONMENTAL: k/se_k ≤ −3.
- WEAK TREND: −3 < k/se_k ≤ −2.
- NO TREND: |k|/se_k < 2 AND k − 2 se_k > −0.20 (a trend half as steep as the environmental reading is excluded at 2σ).
- OPPOSITE: k/se_k ≥ +2.
- UNDECIDED: anything else.

## Reported variants (not graded)
Satellites only (d_host < 300 kpc; the CFG838 question with distance); M_V ≤ −6 only; MW satellites + isolated; M31 satellites +
isolated; Υ_SFH where available; no gas; full g_bar range; step model (k replaced by an indicator for d_host ≥ 300 kpc, which
reproduces CFG874's set-up with SG added).

## Controls
- K1 (code identity): per-dwarf Δ for the 11 isolated dwarfs equal CFG874's primary canonical values (cfg874_results.json) to
  < 1e-9. FAIL ⇒ INVALID.
- MUTATE (`CFG875_MUTATE=inject|shuffle`, outputs separate): inject adds −0.4 (log10 d_host − 2.5) to every Δ (must give
  ENVIRONMENTAL); shuffle permutes d_host across dwarfs (seed 875; must not give ENVIRONMENTAL or WEAK TREND).

## Disclosed limits (fixed now)
Present-day distance is not orbital history (backsplash dwarfs now far may have passed a host). M31-system distances carry
larger errors. Binary inflation is untreated except via the M_V ≤ −6 variant. Stellar rotation untreated.
