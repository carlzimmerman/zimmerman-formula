# CFG477: ΛCDM with the DC14 feedback-core recipe nearly reproduces SPARC's RAR. MARGINAL: scatter 0.120 vs 0.099 dex, emergent a₀ 9.7e-11 (on the canonical footing); the low-acceleration slope is too steep

Criteria ba1d89b8f (committed before the script). Script `cfg477_dc14.py` (~15 s). Reuses CFG476's data, abundance matching, noise and statistic. κ = ½ fitted.

| | RAR rms (a₀ free) | emergent a₀ | low-g slope |
|---|---|---|---|
| SPARC data | 0.099 | 1.37e-10 | 0.605 |
| CFG476: dark-matter-only ΛCDM | 0.205 | 3.9e-10 | 0.40 |
| **CFG477: ΛCDM + DC14 cores** | **0.120** (16–84%: 0.108–0.140) | **9.7e-11** (8.6–11.2e-11) | 0.754 |

**Verdict: MARGINAL.** The median 0.1202 exceeds data + 0.02 = 0.1194 by 0.001. Only 9% of mocks are ≥ data + 0.05.

**Reading (stated plainly, against the framework's interest).**
- A standard, published feedback prescription closes most of the gap: the scatter falls from 0.205 to 0.120 dex.
- The emergent acceleration scale lands at 9.7e-11, between the two footings and close to the canonical one. So ΛCDM with feedback produces an a₀-like scale of the right size without any tie to Λ.
- What DC14 does NOT match is the low-acceleration slope (0.75 vs 0.61 observed; deep MOND is 0.5). That is the most specific remaining discriminator in this comparison.
- This weakens any claim that the RAR's existence or its acceleration scale requires the framework. The framework's distinctive content narrows to: (i) the exact low-acceleration shape, (ii) a₀ tracking ρ_DE in redshift, (iii) the cases in the record where ΛCDM is under strain.

**Controls.**
- K1: forced NFW with the generic integrator reproduces CFG476's 0.2052 exactly.
- K2: M(<R₂₀₀) = M_h to 1e-4.
- MUTATE (feedback inverted, X − 3): rms 0.120 → 0.208, detected (exit 1).
- 4% of draws had X clipped to DC14's calibrated range.

**Scope.**
- One prescription (DC14), r_s convention approximated, no adiabatic contraction, Moster+13 SHMR.
- Other feedback models or SHMRs would shift these numbers, and none are scanned.
