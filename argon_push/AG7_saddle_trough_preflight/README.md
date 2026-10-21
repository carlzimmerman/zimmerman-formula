# AG7: power pre-flight of the saddle test against published stacked pair lensing (2026-10-21)

Owner's go (2026-10-21): "freeze and run a power pre-flight of the saddle no-trough prediction against published stacked
pair-lensing measurements (verify the papers first; no data download without my OK)". The criteria (`FROZEN_CRITERIA.md`)
were committed alone, before any script or number. No data were downloaded; only published numbers are used. κ = ½ fitted;
not theory closed. A pre-flight decides only whether a test is possible, never which prediction is right.

## Result: MARGINAL by the frozen rule. In practice the published data cannot decide it.
- Data: Epps & Hudson 2017 (arXiv:1702.08485), CFHTLenS × BOSS LRG pairs. Numbers verified from the paper text: ~23,000 pairs,
  6–10 h⁻¹ Mpc, filament box 7.1 × 2.5 h⁻¹ Mpc, M = (1.6 ± 0.3)×10¹³ M☉.
- **K1 passes:** AG6C's F1 column is reproduced (1.9648 vs 1.9647 M☉/pc²).
- **K2:** the box gives 0.442 ± 0.083 M☉/pc², i.e. 5.3σ, matching the paper's ~5σ.
- **Primary** (canonical, M_b = 10^11.3 M☉, d = 8.23 h⁻¹ Mpc): the dip column is 0.21 M☉/pc².
  - Box S/N 0.30.
  - Optimal-strip S/N 0.87, with every choice favouring detection.
- **Brackets:**
  - M_b ×10 alone gives a strip S/N of 2.77.
  - Only the corner with both brackets (M_b = 2×10¹² M☉ and d = 6 h⁻¹ Mpc) reaches 3.24. The alt footing gives 3.56.
  - That corner keeps all 23,000 pairs at the closest separation, which the sample does not have. It also ignores every item
    in the list below.
- **Forecast (labelled; optimistic):**
  - 3σ at the primary values needs ~2.7×10⁵ CFHTLenS-like pairs (×12).
  - A ~100× pair sample with ~2× source density (DESI × LSST/Euclid-like) would give S/N ~ 12.
  - Both before the losses listed below.
- **MUTATE** (trough ×100) reads DIAGNOSTIC and exits 1: the control bites.

## Finding: in AQUAL the column through the saddle is net positive
This comes from AG6C's own committed output (`ag6c_s0_saddle.out`, the line "mid-plane column through the saddle"):
- **The numbers:** along the mid-plane line of sight through the saddle, the negative part is −0.2064, but the net is +0.0160
  (dimensionless). At the primary values these are −0.203 and +0.016 M☉/pc².
- **So neither model predicts negative convergence there.** AQUAL predicts a narrow dip, nearly to zero, inside the positive
  phantom bridge. A medium that cannot go below zero has no dip, if it keeps the positive part. Its actual departure from the
  law is not computed.
- **AG7 is unaffected:** its statistics size exactly that difference, a dip of depth ≤ Σ_line in a 0.1d strip.
- **PAPER49 v1.1 needs a fix:** its wording "no negative lensing trough through the saddle" is imprecise. The separating
  prediction is "no dip of ~0.2–2 M☉/pc² in the column through the saddle". The paper was not changed here. A wording
  correction needs the owner's go.

## Not included (each weakens the test further)
- An external field. The field near the saddle is only ~2×10⁻³ a₀ (deep-MOND estimate at R = 0.2d), so a larger external
  field fills the null point. Not modelled.
- The dip's real profile: thinner than the strip, and smeared for pairs not seen edge-on.
- Correlated Kaiser–Squires noise. Shape noise was taken as white.
- Modelling the positive filament and the medium's own departure from the law, which is needed to isolate the dip.

## Prior art
The negative phantom density, and the negative convergence it gives for single galaxies in an external field, is not new:
- Oria et al. 2021 (arXiv:2109.10160), QUMOND, κ ~ −10⁻³. It is degenerate with ΛCDM underdensities and sensitive to the
  external field.
- The Famaey & McGaugh review (arXiv:1112.3960).

What is specific here is that a real positive-mass medium cannot supply it.

## Files
- `ag7.py` writes `ag7.out` and `ag7_results.json`. The `AG7_MUTATE=1` run writes `ag7_MUTATE.out` and
  `ag7_results_MUTATE.json`.
- Each run is a small job: single thread, under a second.
- **Disclosed:** after the first run, two REPORTED blocks were added: AG6C's net column and the saddle-field estimate. The
  caveat text was also made precise. No criterion, number or reading changed.

## Provenance note (disclosed)
- The criteria were committed alone first: local 3e77d0047, author time 07:06:18. The script and results followed at 07:10:52.
- On origin the order is inverted. The results commit (f55d65c04) landed before the criteria commit (519634f29), because a
  cherry-pick abort in the push worktree dropped the criteria the first time.
- The author dates keep the freeze-first order. The results commit message cites the local hash 3e77d0047. Its origin copy is
  519634f29, with the same content.
