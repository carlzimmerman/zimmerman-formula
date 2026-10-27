# X61_switch_at_high_z: at z ≥ 1 the crossover falls below every disc in the record. The split test is NOT DIAGNOSTIC.

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (0b35616410, committed alone, before any script or number). No
amendment.
- **One loader fix after run 1.** Run 1 stopped at step 0 (d) (`x61_switch_high_z_run1_STOPPED.out`, kept). The cause was
  that CFG280's points file prefixes object names with "SINS ", so the join found nothing. This was my join, not a record
  number. No graded number had been computed when the run stopped. The fix is one line, marked in the script.
- κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter. Not "theory closed". Nothing here says the data
  favour the framework.

## The switch at redshift z

The switch is X58's hypothesis SW; only X58's committed criteria are used.
- **Above M_×:** route E, Newtonian, with an X43 collapse-cored Burkert halo.
- **Below M_×:** the law on the baryons alone, with no halo.
- Each object stays on one branch at all radii.

The crossover M_×(z) is the mass where η Σ_coll(M, z) = a₀ F(z)/(2πG):
- η = 14.83 and c_f = 4 is EXTERNAL.
- Σ_coll comes from X41's Lacey–Cole EPS on EM1's CLASS P(k), generalised to the observation epoch:
  δ_c/D(z_f) = δ_c/D(z_obs) + ω̃ S^{1/2}.

## M_×(z), log₁₀ M200 [M☉] (bg A; bg B within +0.03 to +0.05)

| z | 0 | 1 | 1.5 | 2 | 2.5 |
|---|---|---|---|---|---|
| canonical, M-DEC (primary) | 12.09 | 10.91 | 10.38 | 9.91 | 9.50 |
| alt, M-DEC (primary) | 12.43 | 11.21 | 10.66 | 10.19 | 9.77 |
| canonical, flat a₀ | 12.09 | 10.93 | 10.48 | 10.11 | 9.78 |
| alt, flat a₀ | 12.43 | 11.22 | 10.77 | 10.39 | 10.05 |
| F_MDEC(z) | 1.000 | 0.989 | 0.931 | 0.874 | 0.822 |

- **The baryonic mass at the crossover** (EM1's line inverted, M-DEC): log M_b,× = 11.01 / 9.70 / 9.11 / 8.59 / 8.13
  (canonical) and 11.39 / 10.03 / 9.42 / 8.90 / 8.43 (alt).
- **Why it drops.** At fixed M, Σ_coll at z = 2.5 is 4.0–4.9× its z = 0 value for M = 10^10–10^12 (z_f 3.3–3.6 against
  0.9–1.3), and a₀(z) under M-DEC falls slightly as well.
- The hand estimate HE1 (10^10–10^10.5 at z ≈ 1.5) was right: 10.38 (canonical) and 10.66 (alt).

## Counts on each side of M_×(z_gal) (M-DEC, bg A; above / below)

| sample | canonical | alt |
|---|---|---|
| **KURVS** (CFG140/141, z 1.33–1.61, μ = 0.67) | **10 / 0** | **10 / 0** |
| KMOS3D clean HIGH, z ≥ 1.9 (CFG99) | 74 / 0 | 74 / 0 |
| KMOS3D clean MID, 1.1–1.9 | 74 / 0 | 74 / 0 |
| KMOS3D clean LOW, 0.6–1.1 | 101 / 13 | 84 / 30 |
| SINS-AO T0 / T2 (CFG280, stars only, a lower bound on M200) | 38 / 0; 18 / 0 | 38 / 0; 18 / 0 |
| RC100 z ≥ 2 (CFG227 S4, class D) | 41 / 0 | 41 / 0 |
| RC100, all z (class D) | 99 / 1 | 93 / 7 |

The flat-a₀ variant gives the same counts for KURVS, KMOS3D and SINS-AO (it was not run for RC100). Halo masses all come from EM1's z = 0 relation, log M200 = 11.18 + 0.90 (log M_b − 10),
and are APPROXIMATE (ledger A5). That relation was fitted with a ΛCDM c(M) (ledger A6).

## Verdict (frozen): **NOT DIAGNOSTIC**, both footings

The graded statistic is KURVS's outer Δ' (P2, μ 0.67, δ 0, M-DEC). Its power:

| | N_A | N_B | expected separation S |
|---|---|---|---|
| canonical | 10 | 0 | 0 (σ_B undefined; ⟨Δ_pred⟩_A +0.076) |
| alt | 10 | 0 | 0 (⟨Δ_pred⟩_A +0.044) |

The rule needs N_A ≥ 3, N_B ≥ 3 and S ≥ 2.
- **No disc in the record at z ≥ 1.1 sits below M_×.** The below-M_× subgroup is empty, so the switch's high-z split
  cannot be tested on this record.
- This is a statement about the samples. It does not grade the switch.

**R4 flag robustness (KURVS).** Across μ 0.25–4, δM★ ±0.2 dex and M200 ±0.3 dex, at least 8 of 10 discs (canonical) and
7 of 10 (alt) stay above. At the most adverse corner the smallest margin is −0.15 dex (canonical) and −0.43 dex (alt). With
bg B or flat a₀, all 10 are above.

## Reported only: the above-only reading (R1, KURVS; no grade)

Every KURVS disc is on the route-E branch, so the record can still ask whether route E's predicted excess at R_max
(4–7 R_d) matches the observed one. Central cell, M-DEC:

| pressure model | Δ'_A observed (the law alone) | ⟨Δ_pred⟩ route E | residual vs route E |
|---|---|---|---|
| P2 (measured σ) canonical / alt | +0.402 ± 0.065 / +0.405 ± 0.064 | +0.076 / +0.044 | **+0.327 ± 0.067 / +0.361 ± 0.067** |
| P1 canonical / alt | +0.410 ± 0.070 / +0.412 ± 0.069 | +0.076 / +0.044 | +0.335 ± 0.073 / +0.369 ± 0.073 |
| P0 (no pressure) canonical / alt | −0.118 ± 0.057 / −0.114 ± 0.057 | +0.076 / +0.044 | −0.196 ± 0.060 / −0.160 ± 0.060 |

**Over the 12 μ × δ cells, route E is within 2σ in:**

| | P0 | P1 | P2 |
|---|---|---|---|
| canonical | 1 | 3 | 3 |
| alt | 3 | 2 | 2 |

**What this reading shows:**
- The X43 collapse core at these masses (M200 ≈ 10^11.0–10^12.0, z ≈ 1.5) adds only 0.01–0.10 dex over the law at R_max.
- Under P1/P2 the observed excess is five to nine times larger. Under P0 it has the opposite sign.
- So the size of the predicted halo excess is far below the walls CFG140/141 name: pressure support and unmeasured gas
  (about 0.3 dex each).
- Even with a populated below subgroup, the KURVS-type observable could not separate the branches at this precision.
  CFG141's +0.39 excess is not evidence for the switch.

**Descriptive (R3, class D / stars only; no grade):**
- SINS-AO δ_FLAT median: +0.243 (T0) and +0.319 (T2). All rows are above, so there is no comparison group.
- RC100 all-z f_DM(< R_e) median: 0.28 above against 0.79 for the single canonical below-M_× disc (0.70 for the 7 on alt).
  That one disc runs opposite to the switch's direction. It is a single class-D object.

## What a future sample would need (R5)

- **Below-M_× discs at the test redshift.** M_b below ≈ 10^9.1 (canonical) / 10^9.4 (alt) at z ≈ 1.5, and below
  10^8.6 / 10^8.9 at z ≈ 2: dwarf-mass discs at z ≳ 1.
  - None of KURVS, KMOS3D, SINS-AO or RC100 reaches that mass.
  - JWST/NIRSpec IFU kinematics of low-mass lensed discs is the only route the record knows of.
  - The ALMA windows of CFG806 / CFG809 target massive gas-rich discs, which are on the route-E side.
- **The predicted signal is small.** Above-M_× discs are expected at only ≈ +0.04 to +0.08 dex over the law at R_max. A
  2σ split needs σ_diff ≲ 0.02–0.04 dex. That means CFG385's specification: per-galaxy curves spanning y ≳ 3 to ≲ 0.3 at
  about 5 % in velocity, with measured gas and outer dispersion, and ≥ 10–20 discs per side.
- **The low-z lever.** The only populated below subgroup is KMOS3D LOW (13 / 30 at z 0.6–1.1). Its velocities fail CFG99's
  C1c (28 % slow at r_out), so it carries no g_obs without a beam-smearing forward model.

## Checks

**Normal run: 7/7, exit 0.**
- **K0 (step 0).** The record's headline numbers reproduce:
  - CFG140 per-galaxy Δ_flat to 0.0028; central df 0.398302 exact;
  - CFG141 P2 central df 0.389889 exact; per-galaxy to 0.0049;
  - CFG99: 74 clean HIGH discs, 2 / 3 below a₀;
  - CFG280: 38 rows, T2 = 18;
  - RC100: 41 at z ≥ 2;
  - X43's crossover: 10^12.093 / 10^12.429, and Σ_coll(10^12) = 6.837.
- **K1:** the switch property, on both footings.
- **K2:** the generalised EPS residual is ≤ 4e-16.
- **K3:** the Burkert mass at z 1.5 is exact to 1e-14.
- **K4:** F(0) = 1, and the flat law branch equals CFG140 exactly.
- **K5:** RSS 0.23 GB.
- No halo saturated.

**MUTATE (`X61_MUTATE=1`, every flag inverted): K1 fails on both footings (0/10 flags agree), 5/7, exit 1.**

## Files

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `x61_switch_high_z.py`, `.out` / `_results.json`, `_MUTATE`,
`x61_switch_high_z_run1_STOPPED.out`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x61_switch_high_z.py                # exit 0, 7/7 (about 6 s)
    X61_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x61_switch_high_z.py   # exit 1, K1 fails
