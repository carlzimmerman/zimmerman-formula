# AM1_native_abundance_match: AM HIGH, and SPARC BREAKS with the native relation. EM1's fitted halos are about 3–4 times too common for the galaxies they host, or 0.5–0.7 dex too light for their number

Criteria: `FROZEN_CRITERIA.md` (56c2016c2e), committed alone before any script or number. `am1_bmf.py` → `am1_bmf.out`, `am1_bmf.json`; `am1_match.py` → `am1.out`, `am1_results.json`, `am1_sigma.json`; MUTATE `am1_MUTATE.out`. Post-result, reported only: `am1_generous.py`, `am1_generous.out`. κ = ½ FITTED; footings never pooled; not theory closed.

## Frozen grade
**A. Press–Schechter on the native σ(M) against GAMA's measured baryons, centrals, z 0.02–0.30:** cold M200 at lg M_b 10 = **11.88**, total M_t 11.96, against EM1's 11.18: **Δ +0.70 dex.** Slope over 9.5–10.5: 0.79 (EM1 0.90). **AM HIGH** in both mass conventions; Argon's fail line was 11.45.

| lg M_b | native cold M200 | EM1 |
|---|---|---|
| 9.0 | 10.81 | 10.28 |
| 10.0 | 11.88 | 11.18 |
| 11.0 | 13.30 | 12.08 |
| 11.5 | 14.58 | 12.53 |

**B. The SPARC line with this relation in place of EM1's:**
| Rule | SPARC rms (A/B) | median Υ (A/B) | line | groups Z |
|---|---|---|---|---|
| F, EM1 (K3) | 0.0687 / 0.0700 | 0.51 / 0.50 | pass | +1.62 |
| N1, EM1 | 0.0670 / 0.0681 | 0.55 / 0.56 | pass | +1.62 |
| **F, native match** | **0.168 / 0.165** | 0.55 / 0.56 | **FAIL, rms** | **−16.1** |
| **N1, native match** | **0.169 / 0.165** | 0.55 / 0.55 | **FAIL, rms** | **−16.1** |

**SPARC BREAKS (rms)** on F (both footings) and N1. The halos are too massive, so V runs high at fixed baryons, and Υ can't fix that. The group path takes the same relation and goes far BELOW LAW's estimator. Argon's expected failure was Υ below 0.42. It breaks on rms instead, at Υ 0.55.

## How firm is it
| Choice | cold M200 at 10¹⁰ | Δ from EM1 |
|---|---|---|
| frozen: centrals, PS | 11.88 | +0.70 |
| 0.15 dex scatter | 11.90 | +0.72 |
| z below 0.15 | 11.91 | +0.73 |
| M★ − 0.2 dex | 12.02 | +0.84 |
| M★ + 0.2 dex | 11.73 | +0.55 |
| all galaxies | 11.67 | +0.49 |
| Sheth–Tormen [BORROWED FIT] | 11.69 | +0.51 |
| n_b × 2 (MUTATE) | 11.54 | +0.36 |
| all galaxies, M★ + 0.2 (approx), PS | 11.52 | +0.34 |
| the same with Sheth–Tormen [BORROWED FIT] | 11.34 | +0.16 |

No single choice reaches EM1's band, and neither does every generous choice stacked together, though the last comes close. **In counting terms:** EM1 puts M_b 10¹⁰ at M_t 10¹¹·²⁶. There Press–Schechter has 1.26e-2 halos per Mpc³ above that mass, against 3.1e-3 central galaxies above M_b 10¹⁰ (4.7e-3 for all): **4.1 and 2.7 halos per galaxy.**

## Limits, and they matter
- **The bright end of this mass function isn't trustworthy.** Above lg M_b 10.5 the count depends strongly on redshift: n_b(>10¹¹) 1.2e-4 at z below 0.30, 6.5e-6 at z below 0.15. P2 uses LePhare's MASS_MED + 0.15, and I suspect aperture losses at low z, not checked here. So the 13.3 at lg M_b 11 is weak, and lg M_b 10 is what's graded. At lg M_b 10, z below 0.15 agrees within 7 %.
- **All centrals share one relation here.** Red galaxies take the massive halos at fixed baryons, so spirals may sit in lighter ones than this match gives. That's a known way to reduce the gap at the bright end. It does less at lg M_b 10, and it needs a colour-split count that isn't built.
- **Press–Schechter isn't measured for this cosmology,** and its mass isn't M₂₀₀. A conversion would lower M_t by roughly 0.1 dex once ZN1 gives its M₂₀₀/M nominal.
- **The count is for host halos, with no scatter treatment beyond line 6.** Halos with no galaxy above M_b 10¹⁰ are allowed in this reading only if most halos of 2 × 10¹¹ fall short of that, which is exactly the excess it's measuring.
- It says nothing against the a₀ law, which has no galaxy halo to count. It doesn't say where the rest of those halos are, either. The record's picture of the cold fluid at galaxy scale is not settled.

## How this reads
EM1's relation is what lets route E pass SPARC, and it's fitted. A native count doesn't give it. The relation that the count gives breaks the SPARC line. So gate G13 stays open and got harder: route E's SPARC pass depends on galaxies sitting in halos about 3–4 times more common than the galaxies are.

## Checks
K1 PS mass integral against erfc: 1.6e-5 of ρ_m. K2 P2's formula reproduces its ρ_b,gal 2.959e8: 2.9594e8. K3 EM1's relation through this path against FC1's JSON: |d| 0 on SPARC rms, Υ and group Z; N1 against NF1's JSON: |d| 0. MUTATE n_b × 2: −0.342 dex.
