# CFG330 FROZEN CRITERIA: are the four cluster-centre ellipticals' excesses intracluster-GC contamination?

**Lane:** orchestrator. The owner said "yeah run it boss".

**Hypothesis.** The surviving elliptical tension comes from the four group/cluster centrals: M87 = NGC 4486, NGC 4365, NGC 4374 and NGC 5846, at +0.18 dex (CFG323). Their outer GC samples may contain intracluster GCs, which belong to the cluster potential and have a larger velocity dispersion. Those would inflate the measured σ.

**Test.** Remove kinematic outliers locally, per radial bin, and re-measure.

## Method
- **Base.** A copy of AUDIT_SLUGGS's independent recompute (raw Forbes+17 GC velocities, ATLAS3D JAM calibration, γ = 3, isotropic, outer bins, ν_mono, both footings). Unchanged except for one extra step inside each radial bin.
- **The extra step.** After the existing global 3σ clip, each equal-number bin is iteratively clipped at k × σ_bin about its own ML mean. The bin σ is then divided by the truncated-Gaussian factor c(k) = sqrt(1 − 2kφ(k)/(2Φ(k) − 1)), so that an uncontaminated Gaussian bin is unbiased.
- **Modes:**
  - K0: no local clip, the audit baseline (control);
  - K25: k = 2.5, the primary;
  - K20: k = 2.0, reported as an aggressive bound.
- **Reported:**
  - the per-galaxy offset change Δ for the four centrals and the twelve others;
  - the mean offset of the four centrals, the twelve others and all 16 (the audit statistic: mean with the galaxy-scatter error).

## Decision (K25, both footings)
- **CONTAMINATION EXPLAINS:** the centrals' mean offset falls below 2σ (its own scatter error) and to within 0.05 dex of the twelve others' mean.
- **PARTIAL:** the centrals' excess over the twelve others drops by ≥ 50%.
- **NOT SUPPORTED:** otherwise.

## Controls
- **C1:** K0 reproduces AUDIT_SLUGGS's all-16 canonical offset (+0.0977) to 0.001 dex.
- **C2:** a synthetic pure-Gaussian bin (N = 40, σ = 200 km/s, 15 km/s errors; 2000 draws) recovers σ to within 3% after the K25 clip and correction.
- **C3:** an injection test. A Gaussian bin with 25% contaminants (σ ×2.5) is pulled back by more than half by K25.
- **MUTATE** (CFG330_MUTATE=1): the clip is applied only to the twelve non-centrals. The centrals' Δ must then be exactly 0.

## Scope
This is a tracer test, not a change to the law or the frozen CFG323 verdict, which stands. A positive result would motivate a frozen re-score of CFG323.

## Pre-freeze disclosure
- Known before freezing: the audit's "drop the 4 centrals" row (2.76σ), and CFG323's centrals at +0.18.
- No clipped value had been computed.
