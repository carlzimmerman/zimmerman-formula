# HOSTILE REGRADE — SWEEP 2 [galaxy_box] (Opus 4.8 [1m], 2026-06-15)

*Skeptic re-audit of the galaxy-sector viable region. Re-ran `galaxy_box_viability_scan.py` +
`galaxy_box_robustness.py` (reproduced exactly) and added `HOSTILE_galaxy_box_regrade.py` with five
independent cross-checks: (Q1) 2D volume vs the 1D-marginal headline; (Q2) edge-vs-interior; (Q3)
RAR-penalty robustness to the scatter METRIC; (Q4) BTFR dispreference magnitude; (Q5) threshold
robustness. 175 gal / 2807 RAR pts, 123 gal BTFR. The fine-tuning-trap question answered both ways.*

## Verdict: the sweep's headline SURVIVES — galaxy box is genuinely broad, framework comfortably inside, low fine-tuning. Two framing tightenings, no flips.

The original sweep's core claims reproduce and hold up to hostile probing. The "broad ~49% region,
framework interior, low fine-tuning" verdict is **correct and not manufactured**. I tightened two
framings and chased one number that *looked* damning until it dissolved as an artifact (the honest
both-ways result).

## What I verified holds (CREDIT, at full weight)

- **49% cell fraction reproduces exactly** (172/351 dS-Unruh). Confirmed independently.
- **RAR floor: dS-Unruh is co-best** (0.1440) vs standard-μ 0.1439 / McGaugh 0.1444 / simple 0.1459.
  No unfair pass to the framework's own ν.
- **Framework point passes all three computed fronts**: RAR pen +0.51% (unweighted), BTFR ODR slope
  3.871 = Lelli+2019 3.85±0.09 on the nose, EFE cap physical.
- **9.36e-11 survives the tightest RAR tolerance** (0.001 dex window [9.23e-11, 1.14e-10]).
- **The shape is the well-known RAR a0–Υ degeneracy ridge** clipped by BTFR at low Υ — a real
  diagonal band, not a tuned point.
- **Of the 5 fronts, only 2 are binding** (RAR ridge + BTFR low-Υ clip). I verified the EFE/WB cap
  NEVER exits (1.0,1.65) anywhere in the box (range [1.063, 1.435]) → it carves nothing, and dwarfs
  don't carve a region either. The ledger says exactly this. The "49%" is genuinely RAR∩BTFR.

## Two FRAMING tightenings (own them; neither flips the verdict)

**T1 — "96% of a0 prior / 75% of Upsilon prior" is a 1D MARGINAL, not the volume.** The honest
volume is the 2D cell fraction (~49%), which the ledger DOES lead with. The "96%" is the a0 span
that is viable at *some* Upsilon; you cannot simultaneously sit at the a0-extreme AND the Υ-extreme.
(Caveat-of-the-caveat, both ways: at the framework's OWN Υ=0.70 the *conditional* a0 window is also
[8.0e-11, 1.30e-10] = 96% — so here the marginal happens to equal the conditional, and the band
really is that wide at max-disk. The "96%" is not inflated, just stated as a marginal.) **Use the
49% as THE volume number; quote 96%/75% as conditional/marginal spans, not "the box."**

**T2 — the framework point is interior in a GENEROUS sense, edge-ish in a STRICT sense.** At Υ=0.70,
9.36e-11 sits only 27% of the way up from the low RAR edge (1.34e-11 above it) and 8.9% below the
optimum. More importantly it lands on the ridge ONLY for **Upsilon ≳ 0.625–0.65 (near-max-disk)**;
at population-synthesis Υ~0.5 the RAR+BTFR want a0 ~1.4–1.5e-10 and 9.36e-11 is dispreferred. The
ledger states this ("9.36e-11 lands on the ridge for Υ ≳ 0.65") but calling the point "interior on
every front" slightly oversells. **Honest phrasing: the framework needs BOTH knobs set together
(a0=9.36e-11 AND near-max-disk Υ≥~0.65) — a self-consistent diagonal slice, not free interiority.**

## The one number that LOOKED damning — and dissolved (Q3, the load-bearing both-ways check)

Per the MEMORY rule (optimal a0 depends on the weighting), I re-ran the RAR penalty under four metrics:

| metric | opt a0 | 9.36e-11 penalty |
|---|---|---|
| unweighted RMS (sweep's) | 1.03e-10 | **+0.51%** |
| pure inverse-variance (formal vobs err only) | 1.21e-10 | **+6.68%** |
| 5–95% trimmed RMS | 1.24e-10 | +1.15% |
| L1 median&#124;resid&#124; | 1.06e-10 | +2.19% |

The pure inverse-variance 6.68% looked like a real deficit. **It is an artifact**: weighting by formal
vobs errors alone massively over-weights the flat outer points (tiny errors, gobs≈gbar·ν with ν≈1)
where the interpolation barely matters, pulling the optimum up to 1.21e-10. The moment you add the
**standard Lelli+2016 RAR error floor** (~0.1 dex from M/L + distance + inclination systematics — the
physically correct error budget, which dominates over formal vobs), the penalty collapses:

| added systematic floor | opt a0 | 9.36e-11 penalty |
|---|---|---|
| 0.00 dex (pure formal) | 1.21e-10 | 6.68% |
| 0.05 dex | 1.06e-10 | 1.13% |
| 0.10 dex (Lelli standard) | 1.04e-10 | **0.75%** |
| 0.13 dex | 1.04e-10 | 0.66% |

**So the +0.51% (unweighted) and ~0.7% (correctly error-floored) agree; only the unphysical
pure-formal-error weighting gives 6.7%. The "interior on RAR" claim is metric-robust.** Verified as
rigorously as a win — the apparent deficit was a weighting artifact, not a real one.

## Q4 — BTFR dispreference, honestly sized

The BTFR-implied a0 (the median per-galaxy V⁴/GM) is 1.26e-10 at Υ=0.70 — **higher** than 9.36e-11
by +0.130 dex. As "σ of the mean" that's ~6σ (N=123-inflated); on the **fair scale (population
scatter 0.24 dex)** it is **~0.5σ**. So the BTFR mildly *disprefers* 9.36e-11 (wants higher a0) but
well inside the per-galaxy spread — consistent-but-non-diagnostic, matching the banked verdict and
the MEMORY ledger ("BTFR disprefers 9.36e-11"). The sweep's "BTFR slope 3.87 = Lelli" PASS is about
the *slope* (IF-free, correct); the *zero-point a0* mildly leans high — both true, both owned.

## Q5 — threshold robustness (not a loose-tolerance artifact)

| TOL_DEX | viable cells | framework in? |
|---|---|---|
| 0.005 (sweep) | 49.0% | YES |
| 0.003 | 38.7% | YES |
| 0.002 | 31.3% | YES |
| 0.001 | 23.1% | YES |

Tightening 5× shrinks the box from 49%→23% but it stays BROAD and the framework stays inside. Not a
loose-threshold artifact.

## The fine-tuning, re-quantified (both ways, no hiding)

- **Volume: ~49% of the prior box** on dS-Unruh (the honest 2D number; 23% at 5× tighter RAR; 32% on
  standard-μ; ν-robust across the four). LOW fine-tuning. This is ΛCDM-grade broadness for a
  galaxy-sector fit — comparable to ΛCDM's broad galaxy posteriors.
- **Sigma allowed**: RAR flat-bottomed (≤~2% across metrics at the framework footing, 0.5–0.75% on
  the correct error budget); BTFR slope within its 0.094 σ of Lelli; BTFR zero-point ~0.5 pop-σ high.
- **The cost the box does NOT pay (must be stated)**: it does not *select* 9.36e-11 — the cross-ν a0
  optimum spans ~7.5e-11–1.5e-10 (a ~50% swing) and swamps the framework's ~9% offset. The framework
  point is viable because BOTH knobs are set consistently (a0=9.36e-11 AND Υ≥~0.65); at Υ~0.5 it is
  dispreferred. And the box shares — does not cure — MOND's dwarf failure (3/8 over-dispersed, −3.7
  to −4.2σ, WORSE at framework-leaning conventions) and the Chae EFE pull (the framework's dS-Unruh
  cap 1.137/1.20 is the LOWEST IF, so it sits FURTHEST from Chae 1.49–1.60 — owned).

## Scope flag (the fine-tuning-trap guard the prompt demanded)

**This sweep is the GALAXY SECTOR ONLY (fronts 1–6). It does NOT, and does not claim to, establish a
non-empty NINE-front intersection.** The cluster+CMB+galaxy-WL crux is SWEEP 3/4, which concluded the
9-front intersection is **EMPTY for the cluster cure** (Mistele μ-squeeze: galaxy-WL caps μ≤1.0 Mpc⁻¹,
clusters need μ≥1.58; cs²→0 unified-dust over-clusters galaxies — 0/5100 unified cells). So there is
**no manufactured global viable corner** here: the galaxy box is broad (8 of 9 fronts share it), the
hole is at clusters, and SWEEP 3/4 own that hole. The galaxy_box sweep is correctly scoped — it would
be a fine-tuning-trap error to read its "49% broad" as "the framework is jointly viable everywhere."
It isn't; it's galaxy-sector viable, cluster-cure empty.

## NET (regrade)

**Sweep 2's verdict stands: the galaxy box is REAL, broad (~49% of prior, ν-robust), and the framework
sits inside it at low fine-tuning — credited, not manufactured.** Two framing tightenings: report 49%
as THE volume (not the 96% marginal), and call the framework point a self-consistent (a0, Υ≥0.65)
diagonal slice (needs near-max-disk M/L) rather than freely "interior." The one scary number (6.7%
error-weighted RAR penalty) is a pure-formal-error artifact that dissolves to ~0.7% under the standard
Lelli error floor — verified both ways. The honest liabilities (BTFR zero-point ~0.5σ high, dwarfs
shared & worse at framework conventions, framework EFE cap furthest from Chae) are all already owned
in the ledger at full weight. No flip, no manufactured corner, no high-priest dismissal. Quarantine
held: a0/Z never asserted derived; ν=√(1+1/y) treated as the stated empirical interpolation.

## Sources / scripts
- `galaxy_box_viability_scan.py`, `galaxy_box_robustness.py` (reproduced), `HOSTILE_galaxy_box_regrade.py` (new).
- SWEEP3_CLUSTER_CMB_JOINT_GRID / SWEEP4_GLOBAL_INTERSECTION (the 9-front EMPTY-at-clusters context).
- Lelli, McGaugh, Schombert 2016 (SPARC, 0.1-dex RAR error budget); Lelli+2019 (BTFR 3.85±0.09);
  Chae 2024 (wide-binary 1.49–1.60, contested); Banik+2024 (no-evidence); Mistele+2023 (μ squeeze).
