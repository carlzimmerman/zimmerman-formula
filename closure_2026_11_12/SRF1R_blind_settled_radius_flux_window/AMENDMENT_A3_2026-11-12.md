# SRF1R AMENDMENT A3 (2026-11-12): compute budget, third cut

Committed alone, after A2 (23c3b8956a), while the first primary parts run and before any flux-level statistic of this lane
has been computed or read (only the run log's wall time, A and the mean-flux error were seen). The first seed-0 anchor part
took 1196 s (machine shared with another heavy lane; load average about 19), three times the A2 timing. The A2 queue would
take about 9 hours.

Changes (stated before any flux statistic):

1. **Bins.** Flux is computed at the three anchor bins only (z 2.2, 3.0, 4.4). The nine other bins are not computed.
   The twelve-bin flux Delta chi^2 at each f is estimated as the anchor-block flux Delta chi^2 (joint covariance of the
   three anchor bins) times the ratio twelve-bin / anchor-block of this construction's matter-level Delta chi^2 at the
   same f. The graded Delta chi^2_G(f) is then this estimate times K(f) (unchanged definition). Labelled an estimate
   everywhere. The anchor-block values themselves are reported as the direct numbers.
2. **f grid per part.** z 2.2 seed 0 (both footings) keeps the full grid including 4, 6 and inf (already running). z 3.0
   and 4.4 seed 0: f < 4 only. For f = 4, 6, inf the twelve-bin estimate uses z 2.2 alone, scaled by the matter-level ratio
   twelve-bin / z 2.2 bin. This also serves known answer (b), labelled an estimate.
3. **Seeds.** Seed 0 at every anchor. Known answer (e) uses seeds 0 and 1 at z 2.2 only (the bin that carries the effect),
   on f = 0, 0.70, 1.00, 1.25, 1.60, 2.00, 3.00, with S the standard error of the two-seed mean; z 3.0 and 4.4 are not
   checked for scatter (stated).
4. **Mutations** M1 and M2 at z 2.2 only (seed 0); bite rules unchanged, applied to the z 2.2 bin.
5. **Brackets** at z 2.2 only (seed 0), value = Delta chi^2_G(primary) x ratio of the z 2.2-bin flux Delta chi^2, in
   this order as time allows: B2 (lambda_P x 2), B3 (100 proper kpc), B8 (clustered), B1, B4, B5, B6, B7, B9, B10.
   Brackets not run are reported as not computed; the FRAGILE rule is applied to those computed, and the result says the
   bracket set is incomplete.
6. Queue order: the running z 2.2 parts; z 3.0, 4.4 (f < 4); M1, M2; seed 1 at z 2.2; brackets.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
