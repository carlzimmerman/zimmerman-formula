# X36: does X33's e_ext trend tell "law fundamental" from "law emergent from cold dark energy"? As frozen: NOT DIAGNOSTIC (power P < 2), both footings

Criteria and ledger were committed alone first (**d8651cafc3**). **AMENDMENT A1** (667b97260b) was written after step 0 fired
the stop rule and before any slope existed: S0c's 1e-9 tolerance could not pass against the atlas's 6-digit CSV, so it now
uses the 6th significant digit. That is a check-definition change only. Script: `x36_efe.py` (196 s, one thread, 0.63 GB).
`X36_MUTATE=1` fails K_efe and K_repro as it should (exit 1). κ = ½ FITTED. Footings never pooled. No dark-matter particle.
Not "theory closed". Nothing here says the data favour the framework. "Cold dark energy" is the cold w ≈ 0 clumping
component: a field paired with dark energy, not matter and not a particle.

Every number below comes from `x36_efe.out`, `x36_efe_results.json` or `x36_per_galaxy.csv`.

## The question

X33 found that the residual of large SPARC galaxies against the isolated law falls with log e_ext (ρ −0.455 / −0.437, N 68).
- **(a) The law with the exact AQUAL EFE** (v3s; P4's solver at L★ = 0, Chae+21 e_N) predicts that galaxies in stronger fields sit lower.
- **(b) Route E** (EM1's emergent model: dust-like cold-dark-energy halos, NFW + Bullock c(M), one global M200(M_b) relation)
  has no EFE term.

Which of them reproduces the measured slope, and can the slope separate them?

## Step 0 (all PASS)

| check | result |
|---|---|
| S0a EM1 rerun (scratch copy in `step0_em1/`; only two path constants patched; EM1's folder not written) | every quoted number identical: R1 rms 0.06557 / 0.06546, median Υ 0.36 / 0.35, (a, b) (11.18, 0.90) / (11.20, 0.90); UPS05 dust 0.1020, law 0.11243 / 0.10288; R3 g† 1.183e-10 / 1.227e-10; EM1's own checks all pass |
| S0b X33 trend from `x33_atlas.csv` | ρ −0.4547 / −0.4367 (large, N 68), −0.2213 / −0.2309 (all, N 109), equal to X33 to 1e-9 |
| S0c residual identity (A1) | 175 / 175 galaxies; max \|d\| 4.8e-7 / 4.9e-7 (atlas rounding) |
| S0d P4 L★ = 0 with the EFE solved | 0.053986 @ 0.52 / 0.053509 @ 0.44, against P4's 0.053986 @ 0.52 / 0.053510 @ 0.44 |
| S0e route-E relation by EM1's grid fit | (11.18, 0.90), (11.24, 0.90), (11.20, 0.90), (11.24, 0.90): EM1's R1 and UPS05 values on backgrounds A and B, exactly |

## Slopes: S_L (large, N 68), paired bootstrap B 2000, dex of residual per dex of e_ext

| footing, Υ convention | measured s (ρ) | (a) law + EFE: s, z | (b) route E (bg A): s, z | power P |
|---|---|---|---|---|
| canonical, C_U0 (X33's global Υ 0.60) | **−0.561 ± 0.175** (−0.455) | +0.0000, **z −3.21** | −0.125, z −2.26 | **0.71** |
| canonical, C_05 (Υ 0.50) | −0.522 ± 0.177 (−0.428) | −0.0000, z −2.97 | −0.143, z −1.87 | 0.81 |
| canonical, C_EM1 (route E's per-galaxy Υ) | −0.099 ± 0.122 (+0.038) | −0.0015, z −0.80 | +0.028, z −0.76 | 0.24 |
| alt, C_U0 (Υ 0.55) | **−0.525 ± 0.176** (−0.437) | −0.0000, **z −2.99** | −0.123, z −2.06 | **0.70** |
| alt, C_05 | −0.506 ± 0.177 (−0.417) | −0.0001, z −2.86 | −0.135, z −1.84 | 0.76 |
| alt, C_EM1 | −0.099 ± 0.123 (+0.039) | −0.0017, z −0.80 | +0.025, z −0.75 | 0.22 |

- **The law's own EFE predicts almost nothing here.** Large SPARC galaxies sit in fields of e ≈ 10^−1.49 to 10^−1.24 (10–90 %).
  At those fields the exact solve moves their median residual by at most 0.005 dex, and in all SPARC by at most 0.015 / 0.016.
  So the predicted slope is 0.000. Variants do not change this: Chae's max-clustering bracket gives −0.0004 / −0.0005, the ring
  orientation +0.0002, and L★ = 24 pc 0.0000. The measured slope is about 3σ steeper than the law predicts: z −3.21 canonical,
  −2.99 alt.
- **Route E gets part of the way, for an indirect reason.** Its halo relation gives a residual against the law that varies with
  galaxy properties correlated with e_ext. Its slope is −0.12 to −0.14 at the global-Υ conventions:
  - tension at C_U0 (z −2.26 / −2.06);
  - inside 2σ at C_05 (−1.87 / −1.84) and C_EM1 (−0.76 / −0.75).

  Background B gives the same (−0.124 / −0.127 at C_U0).
- **Neither model gives the measured −0.5.** The two predictions differ by only about 0.12, which is 0.7 of the measurement's
  σ (P 0.71 / 0.70). The frozen rule therefore returns NOT DIAGNOSTIC on power, before reaching the "LAW" or "ROUTE E" rows.
- **The trend is a normalization, not an outer-curve shape.** With each galaxy at its own Υ (C_EM1), the measured trend
  disappears (ρ +0.038, s −0.099 ± 0.122). A per-galaxy Υ absorbs it: galaxies in stronger fields prefer a lower mass-to-light
  ratio at fixed law, or a whole-curve offset that acts like one. The EFE would bend the outer curve instead, and the law
  predicts only ~0.005 dex of that.
- **All SPARC with an environment (S_A, N 109).** Measured −0.256 ± 0.153 (ρ −0.221); (a) −0.008 (z −1.63); (b) −0.194
  (z −0.38); P 1.21 (canonical). Alt: −0.258, (a) z −1.62, (b) z −0.34, P 1.25.

## Confounds (S_L, C_U0): the gate does not fire on either footing

- **The trend survives every control.**
  - Raw ρ −0.455 (p 9.8e-5).
  - All nine gated controls jointly: partial ρ −0.428 (p 7.2e-4); alt −0.437 → −0.410 (p 1.3e-3).
  - No single control moves |ρ| by more than 0.04: log D −0.454, inclination −0.469, Q −0.456, T −0.452, log Σ₀ −0.463,
    log L36 −0.450, log M_b −0.453, Hubble-flow distance −0.433, UMa −0.419.
  - Mechanism-adjacent, reported only: log R_last −0.449, log x −0.438.
- **e_ext does correlate with distance.** Spearman(e, log D) is −0.360 (p 2.6e-3) and with Hubble-flow distances −0.307
  (p 0.011), because the strong-field galaxies are the nearby ones. Yet the trend is stronger, not weaker, among
  galaxies with non-Hubble-flow distances: s −0.971, ρ −0.670 (N 33), against −0.485, ρ −0.268 for Hubble flow (N 35;
  canonical). A Virgo-infall distance error is therefore not the cause.
- **How e_ext was built.** X33 and P4 take Chae+21 Table 3 log e_N (mean of the max- and no-clustering brackets) and pass it
  through the v3 law at the canonical a₀. The axis is a catalogue quantity from 2M++/MCXC/NSA, independent of the rotation curves.
- **What is not controlled:** Υ★ itself. The C_EM1 result shows that a Υ that correlates with environment would produce the trend.

## Verdict (frozen precedence)

- canonical: **NOT DIAGNOSTIC (power P < 2)**;
- alt: **NOT DIAGNOSTIC (power P < 2)**.

**Lane: NOT DIAGNOSTIC.** The X33 e_ext trend cannot separate "law fundamental" from "law emergent from cold dark energy".
At SPARC's field strengths the law's exact EFE is about 0.005 dex, far too small to drive a slope. Route E's indirect slope is
only 0.7σ different from the law's. Reported only: the law's EFE does not reproduce the trend (z −3.21 / −2.99). Route E does
not reproduce it at X33's own convention either (z −2.26 / −2.06), though it does at Υ 0.5 and at its own per-galaxy Υ. The
trend is not one of the listed confounds. It is absorbed by a per-galaxy Υ, so it behaves like an environment-correlated
normalization. This changes no verdict of X33, EM1 or P4.

## Gaia DR4 wide binaries for the same question (reported)

- **The DR4 volume has no lever arm in e.** The MW field at R₀ = 8.122 kpc is e = g/a₀ = 1.98 / 1.72 (sealed v3 V_c(R₀)
  215.4 / 220.6 km/s). Across ±200 pc, e changes by only 0.023 / 0.022 dex, against the 0.25 dex spread (10–90 %) of large
  SPARC galaxies. DR4 cannot measure a slope in e_ext.
- **Both readings predict Newton.** v3s is screened at L★ = 24 / 50 / 90 pc, with γ_v − 1 at 20 kAU of 8.12e-6 / 1.88e-6 /
  5.80e-7 (C6). Route E is Newtonian by construction.
- **So DR4 does not separate the law-fundamental v3s from route E.** It can only test the unscreened law-first AQUAL arm. The
  frozen CFG800 / Amendment 22 rule (`campaign_fresh_gravity/DR4_OUTCOME_MAP_2026-10-15.md`) is quoted, not edited.
  `SEALED_V3_MW_DR4.json` was only read.
- **Directional EFE record** (a different observable: aligned rotation-curve asymmetry). The n = 16 first firing gave
  Â = +2.95 (Z +0.94). WALLABY (n 25) gave Â = −1.70 ± 2.12 (Z −0.57; an amplitude, AQUAL = +1). Neither can decide.

## Other reported rows

**Tidal bound on route E's halos** (S_L, canonical U₀ relation; host distance not on disk, declared 1 / 3 Mpc): the tidal
radius is r_t / R_last = 8.6 / 12.3 at the median, and at least 3.4 / 4.9. So in route E the external field cannot truncate
halos inside the measured curve, and route E has no environment term at the radii observed.

## Checks

| check | normal | MUTATE (e_ext shuffled within T bins + EFE off) |
|---|---|---|
| S0a–S0e | PASS | PASS (step 0 is unmutated) |
| K_efe (r_a ≤ 1e-6 everywhere, max \|r_a\| > 1e-3) | PASS (max r_a −2.3e-6 / −3.6e-6; max \|r_a\| 0.0151 / 0.0161) | **FAIL** (r_a ≡ 0) |
| K_repro (ρ equal to X33's) | PASS (−0.454675 / −0.436714) | **FAIL** (+0.0776 / +0.0683) |
| K_plant (−0.10 slope plant recovered within 2σ) | PASS | PASS |
| K_rss | PASS 0.63 GB | PASS 0.59 GB |

## Limits

- **EFE geometry.** The EFE uses the spherical-mass approximation and the sphere-averaged field ("mono"). The ring orientation
  and the e_N brackets give the same ~0 slope. A full thin-disc EFE solve is not run.
- **Route E is EM1's model:** no scatter in c or M200, no feedback (DC14 not rerun) and no assembly bias. Environment-dependent
  halo concentration is a ΛCDM-machinery effect that EM1 does not have.
- **The trend's existence is X33's result (post-hoc, disclosed).** X36 tests only what explains it.

## Reproduce

```
# step 0a (scratch EM1 rerun; outputs stay in step0_em1/)
cd step0_em1 && PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 em1_emergent.py && PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 em1_emergent.py --ups05
cd .. && PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x36_efe.py           # x36_efe.out, x36_efe_results.json, x36_per_galaxy.csv
X36_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x36_efe.py      # *_MUTATE; exit 1 by design
```
