# D2_wide_binary_fork — law-first vs medium-first

**Verdict: CRISP FINDING** (three corrections to the record). The fork itself stays **DATA-GATED**:
it is open on current data. Gaia DR4 can decide it only through the global γ̂, not through one bin, and only if the
contamination systematic is below 0.054.

Criteria were frozen first (`FROZEN_CRITERIA.md`, commit c8960e6424). Script `d2_wide_binary_fork.py` uses the
solver `qumond_fft.py`. It passes 7/7 checks and exits 0. Every number below is in
`d2_wide_binary_fork_results.json`. The `--mutate` run drops the curl-free projection, C1 fails, and the score is
6/7 (`*_MUTATE.*`). κ = ½ is FITTED. Both footings are reported. Nothing here says the data favour the framework.

## Numbers

**Q1. Is 1.18 the law's number?** Yes, within the spread of the record's own inputs. The check uses a 3-D FFT
QUMOND solve that is independent of A24's quadrature. It is validated against linear EFE theory to 0.2 % (C1) and
converges to 0.0007 (C2, C3). Setup: 1+1 M☉, circular orbit, 20 kAU.
- A24's own case (θ = 0, x_ext = 1.8): **1.1971** against A24's 1.1933. A24 is reproduced (diff +0.004).
- Orientation-averaged, at the PREREG primary g_ext = 1.778e-10: **1.175 canonical / 1.210 alt**.
- At the PREREG alternative g_ext = 2.078e-10 (v_c²/R₀): 1.151 / 1.182.
- Canonical spread over the record's three g_ext values and three orientations: 1.140–1.197.
- A24's "standard" x_ext = 1.8 a₀ (1.685e-10 m/s²) is below both frozen PREREG values.

**κ leverage (A71's "halves the κ error") is OVERSTATED.**
- dγ_v/dκ = **0.41** (A71's convention, 20–30 kAU) against A71's 0.51. A71 rescaled 1.1811 by √ν(y_ext) instead of
  solving.
- A71 divided the shared σ_sys = 0.020 by √7 and gave every bin the 20 kAU slope (`a71_checks.py:1178`). The script
  reproduces its 0.040 (C5) to show the arithmetic is read right.
- With σ_sys shared and every pair placed at the best slope (optimistic), σ(κ) = 0.066.
- The infinite-N floor from σ_sys alone is 0.048.
- γ_v depends almost only on g_ext/a₀ (∂γ/∂ln g_ext = −0.957 × ∂γ/∂ln a₀). The two frozen g_ext values differ by
  16 %, which adds σ(κ) = 0.031. A wide-binary κ is therefore tied to the Galactic R₀ and v_c, so it is not free of a
  distance ladder.
- Total **σ(κ) = 0.073**, so the joint error goes **0.1207 → 0.077, not 0.0605**.

**Q2. Bin occupancy and current data.**
- The DR3 frozen-cut catalogue on disk has **43 of 6,210 pairs (0.69 %) in 18–22 kAU**. A24 assumed 7.41 %
  (log-uniform), which is **10.7× too many**. The pipeline's own a^−1.6 mock gives 3.73 %.
- At N = 30,000 the bin alone separates 1.18 from 1.0 at only **0.8–2.6σ** at DR3 occupancy (1.7–5.1σ at mock
  occupancy). The range depends on the per-pair σ convention. So "one DR4 bin decides" does not hold. Note that A24's
  4.5σ was for 1.51 vs 1.18, not for the fork.
- The registered **global** γ̂ does separate Arm A's floor from 1.000: **5.0–5.9σ canonical, 6.0–7.0σ alt**, at the
  frozen σ_sys = 0.02.
- The current data are **OPEN**. Cookson+26 finds Newton p 0.78–0.92 and disfavours a ~20 % step at p 0.007–0.011.
  Chae & Yoon 26 finds 1.15–1.20 (provisional record). The record shows a 0.174 inter-group spread on one catalogue.
  CFG825's DR3 R = 0.973 ± 0.178 is UNDECIDED. The DR3 dry run γ̂ = 1.075 ± 0.055 is non-scoring and lies 1.4σ / 1.6σ
  from the two readings.

**Q3. Ultra-faints.** A26 tested the law **without** the host's external field. That is the EFE-blind reading, whose
wide-binary value is 1.40–1.53, not 1.18.
- Putting the MW/M31 field into the same law, as A24 does for binaries, lowers the predicted boost of the 45
  sub-threshold systems by 0.75 dex.
- The data then sit **+1.25 dex above the EFE-present law** (5/45 within 0.5 dex; variants +1.16 to +1.39) and
  +2.15 dex above Newton.
- **Both readings fail on satellites.** FINAL_THEORY §5b ("resolved: law-first") and §6 P5 (γ_v = 1.18) rest on
  two different readings of the law.
- Isolated sub-threshold systems with σ on disk: **1 (Leo T)**.

**Q4. What DR4 needs.**
- For 3σ between law-first's global γ̂ and 1.000, canonical needs N = 4,300–7,500 at σ_sys = 0.02 and 8,400–14,500
  at 0.04. 3σ is impossible at any N if σ_sys > **0.054** (alt: 0.064). The record's demonstrated inter-group
  disagreement (0.174) is 3.2× that ceiling. DR4's NSS/RV screening of triples is therefore what decides the fork,
  not N.
- The 18–22 kAU bin alone would need 42,000–520,000 catalogue pairs at DR3 occupancy.
- Runnable before DR4: only this power calculus and the frozen pipeline's dry runs (already done, non-scoring).
  Nothing on disk can decide the fork.

## Record errors found
- `deepseek_push/DS_FINAL_2026_10_21/A71_global_fit/a71_checks.py:1178` (and report.md:279, VERDICT.md:14,
  STATUS_BOARD.html "Open item 0"): σ(κ) = 0.040 and 0.1207 → 0.0605 should read ≈ 0.073 and → 0.077.
- `A24_wide_binaries/report.md:183` and `FINAL_THEORY.md:527` (P5 recipe): the 18–22 kAU bin holds ~208 pairs at
  N = 30k on DR3 occupancy, not 2,223.
- `FINAL_THEORY.md:489–498` §5b and `CANDIDATE_LAWS_REGISTER.md:707` ("one DR4 bin decides"): A26's law-first verdict
  is EFE-free. With the EFE that P5 uses, satellites miss the law by +1.25 dex. The dwarf leg excludes medium-first
  but does not certify the law-first reading that predicts 1.18.

## What this does not show
- No DR3/DR4 γ̂ is scored here, and nothing is downloaded.
- The configuration is a single 1+1 M☉ circular binary, not the registered population and estimator.
- The UFD EFE is the 1-D QUMOND estimate. It is not a full solve and does not model tides.
- The +1.25 dex may come from binaries, tides or cold energy. This lane does not say which.
- Field ultra-faints from Rubin are the clean dwarf test. DR4 with a contamination systematic below 0.054 is the
  clean binary test.
