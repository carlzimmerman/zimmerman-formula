# CFG744: radiative relaxation reaches galaxy scales only for an independent light field

**Label: (a) cold-medium identification FAIL; (b) independent light field (c_P = c) PASS.** N1 scaling PASS as frozen, with a
caveat. This corrects CFG743's reading: short oscillation periods are not settling. Settling needs damping, and the only
damping in the construction is radiation, which at galaxy scales is far too slow when the polarization is the cold medium.

- **Criteria:** `FROZEN_CRITERIA.md` (3cfc8fd02), committed alone first.
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg744.py` (about 10 s) → `cfg744.out`, `cfg744_results.json`.
  `CFG744_MUTATE=1` exits 1: with a reflecting boundary s₀ = 80 never relaxes.
- **Settings:** κ = ½ FITTED; L* = 5.754 pc; simple μ; the cold energy's mass is required; no particle species; not "theory
  closed".

## Results
- **N1.** t_1% = 24 / 897 / 972 / 1048 at s₀ = 10 / 20 / 40 / 80. Log-log slope **1.65**, inside [1.2, 1.8]: PASS as frozen.
  - **Caveat:** the s₀ = 20–80 times cluster near 900–1050. That looks like a wave reflected from the outer boundary
    (round trip about 2S = 800) setting the last >1% excursion, so N1 does **not** cleanly confirm s^{3/2}.
  - The verdicts below do not depend on the exponent.
- **N2**, t_relax = A s₀^{3/2} ℓ_γ/c_P with A = 2.56 from N1:

| M_b, y | s₀ | (a) medium c_P | (a) t_relax | (a) one crossing r/c_P (reported) | (b) c_P = c |
|---|---|---|---|---|---|
| 10⁹, 1 | 7–9e4 | 187–216 m/s | 3.5–4.9e3 Gyr | **5.0–?** Gyr | 0.003 Gyr |
| 10¹⁰, 0.1 | 2.4–2.8e6 | 35–40 m/s | ~1e6 Gyr | 159–202 Gyr | 0.14–0.17 Gyr |
| 10¹¹, 0.1 | 2.4–2.8e7 | 20–23 m/s | ~2e7 Gyr | up to 1.9e3 Gyr | 1.4–1.7 Gyr |

The minimum over every case of the exponent-free one-crossing bound is **5.0 Gyr** (alt, 10⁹ M☉, y = 1). It is above the bar
everywhere: the cold medium fails even if relaxation needed only one crossing at its wave speed.

## Reading
1. **The cold medium cannot be the polarization field.** With c_P² = 2πG L*² ρ_c, its waves move at 20–220 m/s and cannot carry
   energy out of a galaxy in a Hubble time. Candidate B with a mechanism (CFG698 / CFG743) has **no relaxation channel**, unless
   collisionless relaxation provides one (not on the record). CFG743's post-hoc C3 note is moot for the medium.
2. **The radiative mechanism stands only for an independent, light polarization field** (c_P ~ c): relaxation in 0.003–1.7 Gyr.
3. **Where that leaves the cold energy.** It must be a separate component, and both kinematic and energetic selectors that would
   keep it out of galaxies are closed (CFG741, CFG742). What remains open is a **baryon-state dependence**.
