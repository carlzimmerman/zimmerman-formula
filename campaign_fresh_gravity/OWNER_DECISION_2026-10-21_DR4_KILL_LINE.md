# Owner decision, 2026-10-21: the Gaia DR4 kill line, restated to match what the registered test can detect

Dated note. No frozen file is edited: not the DR4 pre-registration or its 22 amendments, not CFG740, CFG800, CFG825 or
THEORY_CANONICAL_2026-10-14. The governing rule is unchanged. Only the prose that summarises it is corrected. Basis: CFG943's MOCK
dry run (`CFG943_dr4_readiness/README.md` §3, §4, §7 N1–N3, N10). Every number below is a MOCK forecast, not a measurement. It was
written before any DR4 data exist.

## 1. The restated line (replaces "an MOND-size wide-binary boost" wherever the kill line is quoted)

> **Gaia DR4 kills the sealed wide-binary prediction (CFG740) if and only if R − 1 ≥ max(0.01, 3σ_R),** where R is CFG825's
> statistic and σ_R is computed from the pairs that enter R (N_R), never from the γ̂ catalogue's N. A smaller excess reads
> UNDECIDED, which is neither a kill nor a survival. DR4 cannot return CONSISTENT for CFG740: that needs 2σ_R ≤ 0.01, and σ_R
> is at least 0.02.

**What this can detect** (MOCK, the frozen population generator, K = 100 per cell):

| pairs entering R (catalogue N) | σ_R | a kill needs | full MOND benchmark (R ≈ 1.22) killed | MOND step ×1.15 killed | AQUAL-EFE floor (R ≈ 1.11) killed |
|---|---|---|---|---|---|
| ~2,100 (30,000, the prereg's assumed DR4 N) | 0.075 | R ≥ 1.22 | 44–47% | 2–6% | 1% |
| ~7,000 (100,000) | 0.044 | R ≥ 1.13 | 100% | 90% | 23% |
| ~21,000 (300,000) | 0.030 | R ≥ 1.09 | 100% | 100% | 98% |

In plain words, at the sample size the plan assumes:
- A full MOND-size boost kills CFG740 only about half the time.
- A Chae & Yoon-size boost (1.15–1.20) almost always reads UNDECIDED.
- A Newtonian DR4 sky cannot exclude standard MOND at 3σ_R (z = −1.96 to R = 1.15, −2.63 to R = 1.20).

Reliable discrimination at MOND size needs about 7,000 pairs in R. The real N_R is known only when the catalogue is built. The
report states the σ_R it got and the size it could detect.

## 2. Companion readings (same basis; no frozen file changed)
- **σ_R (CFG943 N1).** The CFG800 addendum's "expected DR4 σ_R = 0.0276 at the prereg's frozen N = 30,000"
  (`CFG800_wb_2026_scoring/ADDENDUM_BEG_RIVAL_2026-10-18.md` §4) used the catalogue N. It is not the operative value. At that
  catalogue N the operative σ_R is 0.075–0.083. The addendum's ordering and its "cannot separate BEG at any N" conclusion are
  unaffected.
- **γ̂ guard zone (N3).** γ̂ > 1.23 is "no verdict" for every arm, Arm C and the settling model included, whatever R says. It is
  never read as survival. The no-EFE MOND benchmark (1.33) lands there in 100% of MOCK repeats, so γ̂ kills nothing for that sky.
- **Split outcomes (N6).** CFG740 is scored by R. Arm C and the settling model are scored by γ̂ rows. Arm A is falsified by any
  Newtonian sky. They are reported separately, and a split is reported as a split, never merged into one framework verdict.
- **Correction C8.** THEORY_CANONICAL_2026-10-14_CORRECTIONS item C8 said the quantitative rule is "much stricter than the prose".
  After Amendment 22 that no longer holds. At the expected N the rule kills less than the prose promised, because it needs R ≳ 1.22.
  This note supersedes that sentence.

## 3. What is NOT decided here (still open, CFG943 §7)
- N4: the NSS-off rung and the ladder false-failure rate.
- N5: which catalogue feeds R.
- N7: CFG740's falsifiers beyond ~37 kAU, and its log-slope, which no registered statistic covers.
- N9: tooling defaults.
- Whether to register a better-powered statistic. That would have to happen before DR4, with its own criteria committed alone.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
