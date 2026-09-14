# G049 PRE-REGISTRATION — THE SAG DECOMPOSITION
## FROZEN 2026-09-14 (EDT) BEFORE ANY G049 RESIDUAL OR SAG SLOPE WAS COMPUTED

G036/G044 established the RAR residual decomposition: per-galaxy offset +
white per-point noise (0.045–0.052 dex within-galaxy) + a small ONE-SIGN
outer sag (per-galaxy deep-regime slope mean −0.13 to −0.15 dex/dex,
population-coherent binomial p ≈ 1e-3..8e-5, t ≈ −4σ) in r/r_M. G040 killed
the physics-variable reading of the OFFSET. The sag is the remaining
UNEXPLAINED coherent structure. This lane decomposes it.

## The sag observable (fixed by G036's instrument, not re-tuned)
Per galaxy: deep-regime points r/r_M > 2, residual δ = log10(g_obs/g_th)
against the mu2 bisection (s = 2a0, G010/G013 certified), M_b from the
curve's own enclosed baryons at the standing 0.5/0.7 M/L convention,
per-galaxy slope of δ vs log10(r/r_M) by least squares (≥3 points, x-span
> 0.05). The SAG = population mean of those slopes (128–151 galaxies,
G036's counts; G044's extended Tier-1 repeats 94–100/145–151 negative).
Dual corpus: SPARC-175 (bit-identical to G036's ingest) and the G044 v7
corpus Tier-1. Both a0 footings (9.3619e-11 canonical, 1.1279e-10 alt).

## Candidates and pre-registered verdict criteria
**(a) radial M/L gradient — THE STRONGEST, tested FIRST.**
Model: ups(r) = ups0 + ups1·(r/Rd), Rd = 3.2·Rd_disk (SPARC's standard
stellar-disc scale length, read from the header of every rotmod file;
galaxies without a parsable header are excluded from (a) and counted).
d ln g_bar = d ln ups pointwise (exact per-point for a multiplicative
M/L change at fixed components). Two-parameter per-galaxy fit
(minimize, bounds pre-set: ups0 ∈ [0.2, 1.2] — G013/G040's registered
Lelli+16 population range; ups1 ∈ [−0.5, +0.5] per scale length — the
pre-set physical-plausibility band, |ups1| > 0.5 is a FAIL of the
candidate's plausibility clause regardless of the sag outcome).
Objective: pooled dex residual over the WHOLE curve (same weighting as
G013/G040's per-galaxy rms fit), NOT a deep-regime-only fit.
  V-G (a) verdict — gradient KILLS the sag iff, with the gradient fitted:
    (i)   population-mean deep-regime slope |mean| < 0.05 dex/dex
          (from −0.13/−0.15 registered), AND
    (ii)  the within-galaxy white-noise floor does NOT degrade: pooled
          deep-regime per-point residual-about-the-galaxy-mean rms stays
          ≤ the fixed-M/L value + 0.005 dex (the 0.045–0.052 registered
          floor is the thing a gradient must not eat), AND
    (iii) > 80% of fitted gradients are interior to [−0.5, +0.5]
          (not pinned at the plausibility bound).
    Kill-also condition: if the gradient fit hits (i) only by pinned
    bounds or by inflating the noise floor, (a) does NOT own the sag.
  HEADLINE (pre-registered): if (a) satisfies (i)+(ii)+(iii), the sag was
  the radial M/L gradient all along; the RAR residual then prices as
  per-galaxy M/L surface + gradient + white noise, and the RAR's TRUE
  precision at priced baryons is the gradient-fit white-noise floor —
  reported as the headline number against the registered 0.150/0.174 dex
  deep-regime totals (G036) and the 0.045–0.052 dex within-galaxy floor.

**(b) matched law at Y ≠ 0.**
Refit with the G031-matched-law deep branch implemented at finite Y:
g^2 = a0·C(Y)·g_N with C(Y) = 2(1+Y)²/(2+Y). C(Y→0)=1 (G031 V7, exact),
C(1) = 8/3 (corrected below): at Y = g_bar/(2a0) ~ O(1) the matched law sits well
above bare-mu2 deep-MOND asymptotics, i.e. it is a POSITIVE, r-dependent
relative shift. ARITHMETIC CORRECTION (logged 2026-09-14, still before any
galaxy residual was computed): the first draft mis-evaluated C(1) as 3/2;
the exact value is C(1) = 2*(1+1)^2/(2+1) = 8/3 = 2.667. The direction of
the shift and the verdict criteria are unchanged; the lane measures the
actual bare-C-vs-mu2 offset profile numerically rather than relying on
any hand value. Fit the same two-parameter M/L models (constant and
gradient) under this law. Verdict: (b) absorbs a MATERIAL share of the
sag iff the mean deep-regime slope moves from −0.13/−0.15 toward 0 by
more than half (|mean| < 0.075) with the white-noise floor intact.
Mechanistic expectation (stated in advance): a positive r-dependent
g_th shift SLOWS the fall of δ with r but does not flip it unless it
grows faster than log r — the sag's fate under (b) is measured, not assumed.

**(c) HI truncation / outermost-point artifacts.**
Drop the outermost 2 points of every curve, refit slopes on the same
deep-regime definition. Verdict: truncation owns a material share iff
the mean slope shrinks by more than half (|mean| < 0.075, binomial
sign coherence p > 0.01). Also run the errV/V < 10% quality cut variant
(G013 selection) as the error-bar-artifact control.

**(d) the EFE at the sample's high-eN tail** is NOT re-run here:
G036 V4e and G044 V2E already measured it (regression slopes consistent
with zero at SPARC amplitudes; predicted shift ~1e-3–1e-2 dex, 10× below
the sag) — re-running a closed null would be theatre. G049 reads the
e_N column onto the sag-slope population only as a consistency column
in the results JSON; no verdict is claimed on (d).

## THE FINAL VERDICT (pre-registered decision rule)
- If (a) kills the sag (i+ii+iii): the sag IS the radial M/L gradient;
  the true RAR precision floor at priced baryons is the headline number;
  the sag leaves the unexplained-structure ledger.
- If (a) fails and (b) or (c) absorbs ≥ half: that candidate owns the
  sag; state the residual unexplained share honestly.
- If NO candidate (alone or the measured combination) reduces the
  population-mean |slope| below 0.05 dex/dex with the noise floor
  intact: the sag is UNEXPLAINED residual structure — the theory's
  sharpest open anomaly, ESCALATED in the results JSON and STATE.md.
Both outcomes are findings. No threshold is tuned after the run.

## Honest-scope notes (frozen)
- SPARC headers supply Rd (3.2·Rd_disk). Where the header is absent the
  galaxy is excluded from candidate (a) with the count reported.
- The M/L gradient model is a NUISANCE hypothesis test, not a claim that
  SPARC galaxies have measured gradients; the fitted ups1 distribution is
  itself part of the verdict (a real population effect should centre near
  small negative-to-zero values for old populations, but ANY value inside
  the plausibility band counts as physically possible; values pinned at
  the bounds count AGAINST the candidate).
- G044's Tier-1 extended corpus repeats both candidates' headline fits;
  crossmatched curves inherit their SPARC model (G044's registered rule).
