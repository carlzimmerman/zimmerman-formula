# GH2_cgm_extent_discriminator

**Question.** X78 found that the lensing preference between the isolated law (L) and route E fair-share halos (H)
reverses with the hot-CGM extent. Is the hot gas at 1–3 R_vir a clean, measurable discriminator between the two
theories?
- **Method:** map Δχ²(H − L) against the CGM cut k (Zhang+24's MW-mass profile to k R_vir), with identical baryons in
  both models.
- **Samples:** KiDS isolated lenses (X53 harness) and GAMA G09 centrals (GH1's stacks), bins 3–4 (log M★ 10.6–11.0).
- Criteria were frozen first (48468b5bd8).

## Verdict

**PRIMARY (k = 1, measured gas only):**
- KiDS isolated: **LAW**.
- G09 centrals: NOT DIAGNOSTIC.

**Discriminator:** NOT A CLEAN DISCRIMINATOR. KiDS flips cleanly; G09 never flips.

Δχ²(H − L) and χ² for bins 3–4, canonical (alt in the JSON; same pattern):

| CGM cut k (R_vir) | KiDS H / L | KiDS Δ | G09 H / L (10 pts) | G09 Δ |
|---|---|---|---|---|
| 0 (F2's 0.5 M★ hot) | 600.7 / 95.0 | +505.7 LAW | 23.0 / 12.3 | +10.8 LAW |
| **1 (measured only)** | 437.9 / **66.2** | **+371.7 LAW** | 17.7 / 10.1 | +7.5 |
| 1.5 | 302.2 / 136.3 | +165.9 LAW | 14.0 / 10.5 | +3.5 |
| 2 | 203.3 / 298.3 | −94.9 HALOS | 11.8 / 10.8 | +1.0 |
| 3 (Zhang closure) | **140.6** / 757.8 | −617.3 HALOS | 11.2 / 11.0 | +0.2 |
| 5 | 675.7 / 1913.7 | −1238 HALOS | 24.2 / 11.0 | +13.2 LAW |

**Crossover k\*** on KiDS: **1.82 R_vir** canonical, 1.66 alt. On G09, none.

## What it shows

1. **On KiDS isolated lenses, the hot gas beyond R_vir decides which theory the lensing prefers.**
   - Below about 1.7–1.8 R_vir of gas, the law wins by hundreds in χ².
   - Above it, route E wins by hundreds.
   - That is a sharp, measurable target: the hot-gas mass at 1–2 R_vir (≈ 200–400 kpc) around MW-mass isolated
     centrals. Deeper eROSITA stacks or tSZ cross-correlations can measure it.
2. **G09 50–300 kpc lensing cannot see it.** Gas beyond R_vir (~200 kpc) hardly changes ΔΣ inside 300 kpc. The law fits
   G09 at every k (χ² 10–12 on 10 points). Route E fits only when the gas extends to 2–3 R_vir.
3. **Reported, not graded: each model's best KiDS fit over k.**
   - The law's best is χ² 66.2 at k = 1, which is the measured gas.
   - Route E's best is 140.6 at k = 3, the extrapolated gas to Zhang's closure radius.
   - On this grid, the law with the measured CGM fits KiDS bins 3–4 better than route E with any CGM extent, by ~75.
   - Absolute fits are poor for both (30 points), as in X53.
4. **For the route E flagship:** route E needs hot gas extending well past what is detected, to at least ~1.8 R_vir,
   to beat the law on KiDS, and even then fits worse than the law at its measured-gas best. The CGM extent stays
   untested, and it is now the single decisive measurement.
- κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
  not theory closed; nothing here says the data favour the framework.

## Checks (5/5)

- **K1:** at k = 0, the KiDS numbers reproduce X76 (H 600.741) and X53 (L 95.015) exactly.
- **K2:** at k = 3, they reproduce X78's committed central_k3 on both footings.
- **K3:** the G09 data vector equals GH1's committed ΔΣ.
- **MUTATE:** removing all hot gas lowers both models' ΔΣ at 100 kpc.
- Runtime ~3 min, one thread.

## Limits

- The KiDS 2h term is fitted per bin, as in X53. KiDS isolation leakage (X53's caveat) could mimic outer mass, which
  would help both models' outer fits differently.
- Zhang's R_vir and M★ are taken as published.
- k is a coarse grid, so k\* is interpolated linearly.
- Bins 1–2 are not graded: Zhang has no CGM detection there.

## Files

- `FROZEN_CRITERIA.md`
- `gh2_discriminator.py` with `gh2.out` and `gh2_results.json`
- Inputs: X78's code (read-only); GH1's stacks in `_external_data/gh1_work/gh1_esd.npz`

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh2_discriminator.py
