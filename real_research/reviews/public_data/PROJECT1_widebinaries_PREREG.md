# Project 1 — Gaia wide binaries: PRE-REGISTERED analysis plan

*Committed 2026-06-09, BEFORE the catalog is processed (download `bi2zcrwcj` still running). This fixes the sample, estimator, null, and decision rule in advance — the discipline Fable required for the most methodologically treacherous item on the board. The goal is NOT "run the test" — it is to **replicate Chae (~5σ low-acceleration boost) and Banik (~16σ Newtonian null) on the same public data and locate the methodological fork that flips the answer.***

## Data (provenance-pinned)
- **El-Badry, Rix & Heintz 2021**, "Wide binaries from Gaia eDR3", Zenodo record **4435257** (DOI 10.5281/zenodo.4435257). Files: `all_columns_catalog.fits.gz` (1.42 GB, the science catalog), `all_columns_catalog_shift.fits.gz` (354 MB, the chance-alignment control), `find_binaries_edr3.py` + `num_neighbors_edr3.py` (the published selection method — fetched, method fidelity).
- Pin: record 4435257; checksums logged on download; no other catalog substituted.

## Observable
The relative projected velocity between the two components vs projected separation s, in the **low-acceleration (deep-MOND) regime** g_N ≲ a₀ (separations s ≳ ~3–7 kAU for ~1 M_⊙ pairs). MOND/the framework predicts a velocity *boost* (≈√(g_obs/g_N) → up to ~1.15–1.2× the Newtonian circular value as a→0); Newton predicts none. The framework a₀ = 9.36×10⁻¹¹ (NOT the canonical 1.2×10⁻¹⁰) is the value tested — that 22% difference shifts the transition separation and must be carried.

## Sample cuts (published-method fidelity FIRST; each later deviation logged)
1. **Single-star astrometry:** RUWE < 1.4 on both components (reject unresolved subsystems).
2. **Parallax quality:** parallax_over_error > ~20 (both); consistent parallaxes (the El-Badry pair criterion).
3. **Distance:** d ≲ 200 pc (where projected separation → physical is clean and the sample is volume-complete-ish).
4. **Magnitude / main-sequence:** restrict to MS pairs; apply the El-Badry mass estimates (M_G → mass).
5. **Chance-alignment rejection:** use the `shift` control catalog to estimate and subtract the contamination fraction per (s) bin — the standard El-Badry R-statistic.
6. **Hidden-triple rejection:** the dominant systematic. Apply the published triple-flagging (over-luminosity / RUWE / the v-excess tail). **This is a candidate fork variable — vary the stringency and record the effect.**

## The fork map (re-registered 2026-06-09 per WB-1 — split hidden triples out of contamination)
The Chae-vs-Banik disagreement on identical data traces to:
- **F1 — chance alignments (line-of-sight interlopers): [CLOSED].** First pass: the deep-MOND boost survives a 500× tighter `R_chance_align` cut → not chance-alignment-driven.
- **F4 — hidden triples (bound binary + unresolved close companion): [OPEN, PRIMARY].** Banik's actual mechanism, and **invisible to `R_chance_align` by construction** (the system is a real binary on the sky). They inflate v/v_N *twice*: photocenter wobble adds spurious velocity to the numerator, the unseen mass makes v_N too small in the denominator. RUWE screens some, not all; the surviving fraction is the contested number. **This is the main event.**
- **F2 — eccentricity distribution: [OPEN].** Sky-plane → 3D deprojection depends on f(e); Hwang+2022 superthermal α(s) (e rises with separation) is the teeth.
- **F3 — projection/phase statistics: [OPEN].** Phase sampled uniformly in *mean* anomaly (Kepler), random orientation — Chae's MCMC vs Banik's binned estimator weight the tails differently.
- *(noise inflation — D1 — is the other open systematic, not a "fork" but a floor; see WB-2.)*
The deliverable is the **fork table** (each variable × its effect on the inferred boost/null), and the twin-resampling Monte-Carlo (WB-3/WB-4) that adjudicates it.

## Null & decision rule (pre-registered)
- H0 (Newton): the deprojected relative-velocity distribution matches the Newtonian Monte-Carlo at the measured (M, s, e-prior) with no excess.
- The framework predicts a boost factor b(s) = √(ν(g_N/a₀)) rising toward small g_N; report b in the deepest-MOND separation bin with its full error.
- **Decision:** we do NOT declare for Chae or Banik. We report (a) our own b ± σ under published-fidelity cuts, (b) the fork table, (c) which methodological choice is decisive. A result agreeing with *either* team is reported only with the hostile verification tier; a result contradicting *both* is held pending a third independent computation.

## Honesty fence
This is **C1/C2 (static-acceleration KILL-class), not C3.** It tests *whether* the low-acceleration boost exists at the framework a₀ — it says nothing about a₀(z) evolution. Positions us for **Gaia DR4 (late 2026)**, which may settle the dispute.

## Status
Catalog downloading (`bi2zcrwcj`); selection scripts fetched. First real-data pass (load → cuts → deep-MOND velocity relation → fork table) begins once the FITS lands. No numbers exist yet — this file is the pre-commitment.
