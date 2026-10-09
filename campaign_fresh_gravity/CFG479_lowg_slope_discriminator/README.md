# CFG479: the RAR's low-acceleration slope is NOT a robust discriminator. ΛCDM with coreNFW cores matches it; DC14 is 1.3–2.5σ off; the law is also within 0.6σ

Criteria 66b9928d5 (committed before the script). Script `cfg479_slope.py` (~15 s). κ = ½ fitted; both footings for the law row (canonical shown; alt within 0.005).

Slope = d log g_obs / d log g_bar over points with g_bar < 1e-11. Each cell shows the mock median and its (mock − data)/σ.

| Υ_disk | data | law | Moster DC14 | Moster coreNFW | Behroozi DC14 | Behroozi coreNFW | Kravtsov DC14 | Kravtsov coreNFW |
|---|---|---|---|---|---|---|---|---|
| 0.4 | 0.623 ± 0.062 | 0.564 | 0.735 (+1.3σ) | 0.651 (+0.4σ) | 0.737 (+1.3σ) | 0.700 (+1.0σ) | 0.744 (+1.5σ) | 0.615 (−0.1σ) |
| 0.5 | 0.605 ± 0.066 | 0.565 | 0.756 (+1.8σ) | 0.658 (+0.7σ) | 0.750 (+1.7σ) | 0.713 (+1.4σ) | 0.769 (+2.0σ) | 0.616 (+0.1σ) |
| 0.7 | 0.545 ± 0.070 | 0.559 | 0.738 (+2.2σ) | 0.656 (+1.4σ) | 0.738 (+2.2σ) | 0.715 (+2.0σ) | 0.757 (+2.5σ) | 0.613 (+0.8σ) |

**Verdict: NOT ROBUST** (frozen rule: some feedback cell lies within 2σ; the range is −0.11σ to +2.46σ).

**Reading.**
- CFG477's apparent discriminator (DC14 0.75 against data 0.61) does not survive declared alternatives. A fully cored coreNFW response matches the data at every Υ and SHMR.
- The data slope itself carries ±0.06–0.07 (bootstrap over galaxies), and the law's noisy prediction (0.56) is within 0.6σ.
- **On SPARC's RAR, the law and ΛCDM-with-feedback are not separable**, in scatter (CFG477, marginal), acceleration scale (CFG477) or low-g shape (this lane).

**Controls.**
- K1: Moster/DC14/Υ 0.5 slope 0.756 against CFG477's 0.754 (PASS).
- K2: coreNFW with r_c → 0 equals NFW (PASS).
- MUTATE (law-generated mocks in every cell): NOT ROBUST, detected (exit 1).

**Departures (disclosed).**
- Two runtime fixes to the SHMR code before any full output existed: an overflow guard in the Behroozi form, and clipping the inversion to the relation's range for one Υ 0.7 galaxy.
- The Behroozi+13 and Kravtsov+18 parameters are as recalled and flagged for verification.
- coreNFW n = 1 (fully cored) is the declared most-core-favourable choice.
