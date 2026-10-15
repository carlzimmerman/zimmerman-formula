# AG3 — SPARC phantom-annulus widths vs the AG1 ladders (observational kill test)

**Open item addressed:** AG1's queued observational kill test (AG1 IDEA.md "Kill test",
HANDOFF_TO_CONDUCTOR spawn proposal AG3). **Question:** AG1 showed a conservative
isothermal A/r² phantom annulus destabilizes above width w₁ = 7.4403 (DF) / 10.7491
(DD/FF). Observed law-obeying galaxies persist Gyr. How wide are the annuli real
galaxies settle into? Pre-registered branches S (narrow ⇒ conservative reading survives)
/ F (wide ⇒ dissipation or non-conservative medium mandatory).

## Idea

Zero new framework constants. The law line g² − ḡ² = a₀ḡ plus the AG1 closure identity
C = √(a₀GM_b) fix the phantom-force ratio ρ(r) ≡ r·g_ph/C exactly:

    ρ = √(M(r)/M_b) / (√(u+1) + √u),   u = ḡ/a₀,   M(r) = r²ḡ/G  (measured per point)

(Amendment A, frozen pre-run: the enclosed-mass factor matters — the point-mass corollary
r_lo = (4/3)r_M alone overestimates dwarf widths several-fold.) The A/r² reading holds
within factor f iff ρ ≥ 1/f. Annulus = maximal contiguous in-band run reaching the curve
edge; w = r_hi/r_lo. f = 2 primary (√2, 3 robustness); a₀ and α_break read at runtime
from G081_results.json; pipeline conventions are G071/G044's (corpus v7, m2l_disk, sign-
convention gas).

## Results (175 SPARC → 165 cleaned → 78 eligible; 87 curves never robustly reach the
factor-2 A/r² regime inside the data — itself a finding: half the sample is haze-only
over its observed range)

- **K3 — THE decision: VERDICT S.** median w = **1.843** [IQR 1.403–3.180], max 8.98;
  frac(w > 7.4403) = 0.038 (3 galaxies: UGC 06787 w=8.98, UGC 02953 w=8.67, UGC 09133
  w=7.63, all quality tier 1 — named dissipative/non-settled follow-up candidates);
  frac(w > 10.7491) = 0. Stable under every pre-registered cut: censored-excluded
  (1.810), G071 isolated/low-EFE subset (1.875), f=√2 (1.758), f=3 (2.754),
  a₀_alt=1.1279e-10 (1.914) — all S. **4× margin to the binding rung.**
- **K4 — interior discriminator: static ball decisively excluded.** X_ball = median
  ρ(r ≤ 0.62 r_M) = **0.0025** over 128 galaxies vs static-ball prediction 1 (>>10×
  every noise/systematic scale: σ_ρ = 0.059, 20%-Υ proxy = 0.167). Haze-vs-Newtonian
  interior is NOT decidable at SPARC precision (haze signal 0.13 ≤ Υ systematics).
  Load-bearing statement: **the cap interior of real galaxies is not an A/r² static
  ball** — GF2's closure device is not the realized galactic interior state; AG1's
  violently-unstable ball configuration was never what galaxies are made of.
- **B2 — baryon-inclusive refinement (exploratory, non-gated): 0/78 unstable.** The
  baryon/phantom force ratio inside the observed annuli is non-negligible (median
  r_M/r = 0.464), so AG1's phantom-only ladder is an idealization; solving the general
  q-ODE with Φ₀′ = GM_b/r² + C/r and local-hydrostatic σ²(r) = (GM_b/r + C)/2
  (drift −GM_b/(2r²), assembled symbolically from primitives) gives lowest eigenvalues
  ω₀²/(C/r_lo²) = +3.43 median [+0.61, +15.06] — **all positive**. Including baryon
  gravity strengthens stability; verdict S is conservative in the right direction.
- **K1/K2a:** law-ratio residual rms 0.556 dex (full) / 0.502 (deep, u≤1) — consistent
  with precedent: G071's registered 0.145 dex benchmark is velocity-space; the
  difference quantity (g²−ḡ²)/(a₀ḡ) amplifies it (in-band ρ-space scatter: std ≈ 1.0).
  K2a median ln(ρ_meas/ρ_pred) = −0.198 (quiet band).
- **K2b — FAILED as frozen, verdict CONDITIONAL on record.** median |ln(r_lo
  meas/pred)| = 0.326 > 0.15 tolerance, but signed median = +0.0000 (unbiased) and the
  scatter is quantitatively the framework's own registered law precision: band-region
  ρ-space residual std 1.0 / local slope 0.671 ⇒ expected crossing scatter ≥ 0.33
  (errV-only MC budget: 0.08; observed 0.326 sits between, law-residual dominated).
  The frozen 0.15 tolerance was miscalibrated at freeze time (tighter than the law's
  0.15-dex velocity-space benchmark propagates through the difference estimator).
  Gate kept FAILED per discipline — not retro-passed. Lesson registered: calibrate
  difference-quantity tolerances against the law's registered precision, not against
  exactness.
- **Mutations (all as designed):** M1 M_b-shuffle degrades K2b (0.3045 > 0.3 — thin
  margin, honest note: the metric is law-residual-dominated, so M_b sensitivity is
  weak by construction); M2 baryonic-band: median r_lo shift ×5 (frozen arm 2 fires;
  arm 1 flips 20% only); M3 role-swap: zero eligible edge-runs; the 20 galaxies with
  any negative-g_ph points are a real data fact (inner velocity deficits vs the baryon
  model), reported not gated.

## Kill test (of this lane's conclusion)

A SPARC galaxy with a robustly measured settled A/r² annulus of width > 7.44 and
demonstrably quiescent/settled kinematics would falsify branch S's conservative reading
for that system. Three named candidates exist in-sample (UGC 06787, UGC 02953,
UGC 09133): pre-registered follow-up AG3b = kinematic-disturbance literature/data check
on exactly these three (if they show non-circular motions / interactions, the conservative
picture is strengthened; if pristine and settled, they are the falsifiers). Conversely,
a re-analysis band f with median w > 7.44 would flip to F — checked at f=√2, 3: no flip.

## Two strongest objections

1. **"Eligibility throws away half the sample (87/165) — selection effect."** The
   excluded curves never robustly enter the factor-2 A/r² regime within their measured
   range: for them no observed A/r² annulus exists, so AG1's annulus verdict simply has
   no observational purchase — including them requires extrapolating the phantom beyond
   the data, which is exactly the theatre this lane refuses. The 78 eligible are the
   complete set where the question is data-answerable; f=3 (looser band) adds no
   galaxies (78) and keeps S.
2. **"M_b from truncated curves underestimates; ρ-band depends on C(M_b)."** Frozen
   bias ledger: M_b low ⇒ C low ⇒ ρ_meas high ⇒ r_lo biased inward ⇒ w biased UP ⇒
   branch F favored. Verdict is S — against the bias. Left-censoring (4 galaxies)
   biases w down; excluded-robustness keeps S. Both directions were frozen pre-run and
   both come out the same way.

## Consequences (register proposals in HANDOFF_TO_CONDUCTOR.md)

1. **AG1's observational kill test RESOLVED in favor of the branch:** observed A/r²
   annuli are narrow (median 1.84); conservative-fluid stability is NOT falsified at
   observed scales; the data-implied inner cutoff (law algebra: r_lo ≥ (4/3)r_M·mass-
   correction) sits ~16× above AG1's r_crit = 0.083 r_M.
2. **GF2 P1 acceptance sharpened again:** the static A/r² ball is excluded as the
   realized interior state (K4); the branch's physical realization is haze-interior +
   narrow outer A/r² annulus. The κ=½ algebra is untouched (it is a closure identity,
   not a galactic-structure claim).
3. **Framework-facing finding (flagged, non-gated):** the quadratic law line's interior
   residual (g_ph → a₀/2 haze) is NOT visible in SPARC interiors (X_ball ≈ 0), but the
   deficit is within Υ systematics — a law-interpolation interior refinement question
   for the conductor (proposed: G071-follow-up re-audit at the inner points; evidence
   re-audit on a named pain point).

**Files:** FROZEN_CRITERIA.md (4560f945c) + AMENDMENT_A (7527066a6), both pre-run ·
ag3_sparc_widths.py/.out/_results.json (MAIN; exit 1 = K2b CONDITIONAL on record) ·
_MUTATE.out/_results.json (M1–M3 as designed) · IDEA.md · README.md ·
HANDOFF_TO_CONDUCTOR.md.
