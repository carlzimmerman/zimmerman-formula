# CFG201 — CFG198's mass-route drift in a prior-anchored sample (Price+2021 RC41)

- **Criteria:** `FROZEN_CRITERIA.md` (8a15e7e48), committed before any number. **κ = ½ FITTED, NOT DERIVED.**
- **Run:** `python3 campaign_fresh_gravity/CFG201_rc41_mass_route/cfg201_rc41_mass_route.py`, about 4 s.
- **Checks:** 2/2 pass. The MUTATE run (a −0.5 dex per unit z drift injected) passes 3/3; its slope moves by exactly −0.500.

## Bottom line

- **No significant drift.** The fitted log M_bar minus log(M*_SED + M_gas) has a slope of **−0.036 dex per unit z (95% CI −0.133 to +0.067)** over 41 discs at z = 0.66–2.45. Spearman ρ = −0.11 (p = 0.49).
- **D2:** that is smaller than MUSE-DARK's −0.72 at 95%.
- **Reading.** With M_bar anchored by a 0.2-dex prior on SED + gas, the fitted masses stay at the prior centre at every z. The drift that carries MUSE-DARK III's rise (CFG198) appears in prior-free fits (DC14, no SED prior), not in this prior-anchored one.
- **Not shown.** This cannot say whether RC41's data would drift without the prior: a 0.2-dex prior per galaxy can hold a slope of this size in place.
- **Descriptive (not graded):** the slope of f_DM(R_e) against z is −0.048 per unit z [−0.159, +0.087], so no trend.
- **Caveat:** the gas mixes measured values (PHIBSS CO) with scaling-relation values, with no per-galaxy flag.
