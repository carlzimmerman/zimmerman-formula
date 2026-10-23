# S3_v3_mw_seals — batch R3 of N0 for v3 (AQUAL discs, μ = x/(1+x), EFE solved, screening)

## Verdict: CRISP FINDING

1. **Milky Way outer slope (tile 25): v3 is SHAPE EXCLUDED on both footings, robustly.** v3's 15–27.5 kpc slope is −0.126
   (canonical) / −0.114 (alt) on Ou+24. The data slope is −0.325 there, and the primary Ou+Jiao test gives Z −4.37 / −4.62.
   This is v3's own failure. The record's round rule RM-v gave Z −3.63 / −3.90, so v3 does slightly worse. No ingredient
   cures it. The cause is the steep Gaia DR3 decline (RGB/LIM, ~−0.32), not the law's amplitude.
2. **κ (tile 47): AQUAL in discs moves κ up by +0.045 dex.** v3's κ_Λ = **0.499 ± 0.116** (½ at 0.01σ) and κ_crit =
   **0.413 ± 0.096** (½ at 0.82σ). Both footings are CONSISTENT BUT NOT DISCRIMINATING. The record had 0.417 ± 0.095 and
   0.345 ± 0.078. The kernel swap alone moves κ by −0.0002 dex. The full shift comes from two places:
   - **Record error, +0.033 dex.** CFG493's P3 gas velocities are numerically noisy, and fixing them gives +0.033 dex. See
     "Record errors" below.
   - **AQUAL disc geometry, +0.045 dex.** At the gas-dominated points, AQUAL's in-plane pull is a median 0.95 of the
     algebraic ν₁ value.
3. **Sealed Gaia DR4 file for v3 (tile 45):** `SEALED_V3_MW_DR4.json`, sha256
   **15b7e6ffb0a340248e111d83a4dd214492f0f2e3b2294e5ff23d6542da3b6160**. It is a new file and is labelled v3. CFG553 is
   untouched.
   - An independent rerun from an empty cache reproduces the file byte for byte (C1).
   - New observable P6: the in-plane azimuthal asymmetry that the external field creates. It is
     A(R) = 1.8 / 3.0 / 4.1 / 5.2 / 8.2 % at R = 15 / 20 / 25 / 30 / 60 kpc, with V_min toward Galactic l ≈ 270°.
   - The isolated v3 predicts A = 0.
4. **ALMA (tile 43): v3 NEEDS ADDENDUM F.** v3's AQUAL-disc reading is sealed as `SEALED_V3_ALMA_AQUAL.json`, sha256
   **b5d65a5e17bbce21c3ca2f3cd748169fe736e9b86281ff1329449176e1a8c11d**. The draft is `ADDENDUM_F_DRAFT.md`, in this lane
   only.
   - **GS4 (28 Nov).** At R_e, AQUAL's pull is 0.92–0.95 of AG4e's algebraic ν₁. v3 therefore needs +0.03 to +0.05 dex more
     V²_bar, which is +0.09 to +0.47 dex more gas. Four FLOOR cells flip to finite requirements.
   - **U4 (6 Nov).** At U4's radius AQUAL and the algebraic rule agree on V²_bar (≤ 0.001 dex). The gas requirement still
     moves by up to 0.055 dex near FLOOR.

κ = ½ is FITTED. Footings are never pooled. No dark-matter particle. Not theory closed. Nothing here says the data favour
the framework.

**Lane checker:** 28/31 checks PASS. The three FAILs are frozen checks that were mis-specified (amendments A3, A5, A6), and
each is kept in the output. `--mutate` sets μ ≡ 1, which breaks A7 (V(20 kpc) 124 against ≥ 170) and the frozen D6.

## Part A — Milky Way outer slope, one ingredient at a time (census McMillan17 held; CFG532/532b frozen labels)

| step | law slope Ou (can / alt) | primary Ou+Jiao Z (can / alt) | ρ 0.5 | all pairs (can) |
|---|---|---|---|---|
| 0 OLD RM-v, ν_mono (CFG532b) | −0.160 / −0.148 | −3.63 / −3.90 | −3.00 / −3.23 | −4.20 … −2.05 |
| 0 OLD RM-φ, ν_mono (CFG532b) | −0.119 / −0.107 | −4.53 / −4.79 | −3.75 / −3.96 | |
| 1 ALG ν_mono (my field; reproduces CFG532b to ≤ 0.0009 in slope) | −0.120 / −0.110 | −4.51 / −4.73 | −3.73 / −3.92 | −5.02 … −2.82 |
| 2 kernel: ALG ν₁ | −0.128 / −0.116 | −4.34 / −4.59 | −3.59 / −3.80 | −4.86 … −2.68 |
| 3 geometry: AQUAL disc, isolated | −0.122 / −0.111 | −4.46 / −4.71 | −3.69 / −3.90 | −4.98 … −2.78 |
| **4 EFE: AQUAL + h81 field (exact γ = 0 solve; the v3 cell)** | **−0.126 / −0.114** | **−4.37 / −4.62** | −3.62 / −3.82 | −4.87 … −2.70 |
| 4′ EFE 2 × h81 | −0.132 / −0.121 | −4.21 / −4.45 | −3.48 / −3.68 | |
| 4″ γ = 57° 3-D, anticentre wedge (reported; A5iii failed) | −0.126 / −0.115 | −4.37 / −4.61 | | |

- **Step 5, screening:** l_g = L★²/(2 r_M) is 0.024–0.45 pc for L★ = 21.7–90 pc. The galaxy is unscreened at every radius
  used.
- **Step 6, the μ_K² term:** first-order bound only, at μ_K = 14.8 h/Mpc with the EFE zero point; batch R6 owns this term.
  - It adds 2.4e9 / 1.1e10 M☉ inside 15 / 27.5 kpc.
  - V² rises by +2.3 % / +9.3 %.
  - The slope becomes **shallower** by +0.055 / +0.059, so it worsens the tension.
- **Amplitude at census (v3 cell):**
  - χ²: Ou 167 / 67 of 37, Eilers 122 / 43 of 38 (canonical / alt).
  - M★ needed: 6.5–6.8e10 canonical (z +1.9 to +2.3) and 6.0–6.2e10 alt (z +0.9 to +1.3).
- **Labels:** every RGB/LIM curve is EXCLUDED or NEEDS-HEAVY-DISC.
- **Cepheids (Feng+26):** SHAPE CONSISTENT (Z +1.45 / +1.25).
- **Detection power:** a Keplerian tail injected into the data gives Z −7.9 / −8.2.
- **Reading:** SHAPE EXCLUDED on both footings. It is ROBUST across ρ 0.5, isolated, 2 × h81, and the 3-D cells.

## Part B — κ under v3 (CFG493's routes, GLS and error model; log₁₀ a₀ ± total)

| step | P1 SPARC (12) | P2 MIGHTEE | P3 WALLABY | combined | κ_Λ | κ_crit |
|---|---|---|---|---|---|---|
| record ν_mono (CFG493) | −10.015 ± 0.141 | −10.081 ± 0.151 | −10.302 ± 0.171 | −10.107 ± 0.098 | 0.417 ± 0.095 | 0.345 ± 0.078 |
| K: ν₁, record P3 | −10.016 | −10.082 | −10.304 | −10.108 ± 0.098 | 0.417 ± 0.094 | 0.345 ± 0.078 |
| K: ν₁, P3 rebuilt (44 galaxies) | −10.016 | −10.082 | −10.167 ± 0.174 | −10.074 ± 0.098 | 0.450 ± 0.102 | 0.372 ± 0.084 |
| **A: AQUAL disc (v3)** | **−9.980 ± 0.149** | **−10.036 ± 0.153** | **−10.098 ± 0.178** | **−10.030 ± 0.101** | **0.499 ± 0.116** | **0.413 ± 0.096** |
| A, razor-thin variant | −9.976 | −10.036 | −10.096 | −10.027 ± 0.101 | 0.502 | 0.415 |
| E: EFE noclu (reported) | −9.981 | −10.036 | −10.098 | −10.030 | 0.498 | 0.412 |
| E: EFE maxclu (reported) | −9.966 | −10.036 | −10.049 | −10.012 | 0.520 | 0.430 |

- **Pulls of the other candidates (canonical):** 1/√π 0.53σ, 0.6 0.79σ, Milgrom cH₀/2π 0.47σ, cH_Λ/2π 0.34σ. None is
  excluded.
- **New error terms:**
  - AQUAL geometry: 0.0023 / 0.0002 / 0.0011 dex (P1 / P2 / P3).
  - Outer gas extent (A4): 0.0015 / 0.0007 dex (P1 / P3).
  - P2 kernel bound: 0.0013 dex.
  - P2 AQUAL reference disc: 0.026 dex.
- **P2's kernel shift:** my bound is −0.0013 ± 0.0013 dex. Lane P4's direct REST ν₁ refit gives −0.0009 dex.
- **The AQUAL correction C at the gas points:** median 0.954 (P1) and 0.959 (P3).

## Part C — sealed DR4 predictions (census s = 1; band = the census stellar ±1σ; full tables in `PREDICTIONS_V3.md`)

| quantity | v3 canonical | v3 alt | v3 isolated (can) | NFW fitted to Ou+24 |
|---|---|---|---|---|
| V_c(20 kpc), anticentre wedge | 196.0 (190.4–201.3) | 203.2 | 196.1 | 207.2 |
| slope 15–27.5 kpc (even grid) | −0.120 (−0.129 to −0.111) | −0.110 | −0.115 | −0.174 |
| K_z(R0, 1.1)/2πG [M☉ pc⁻²] | 92.3 (86.5–98.0) | 96.8 | 92.5 | 76.3 |
| local "phantom" density (R0, 0) | 2.22 GeV cm⁻³ (shell 0.25) | 2.55 | — | 0.34 (NFW) |
| V_c(60 kpc) wedge / azimuthal mean | 170.9 / 169.9 | 178.4 / 177.3 | 178.2 | 166.6 |
| P6 asymmetry A(20 / 30 / 60 kpc) | 3.0 / 5.2 / 8.2 % | 3.1 / 5.4 / 8.2 % | 0 | 0 |

- **Required DR4 precision for v3 vs the NFW (3σ):**
  - slope: 0.012–0.019;
  - K_z(R0, 1.1): 3.4–5.7 M☉ pc⁻²;
  - V(60 kpc) and the 30–60 kpc mean: NOT SEPARABLE on the canonical footing.
- **Cross-lane check:** lane P4's independent AQUAL MW gives K_z(R0, 1.1)/2πG 92.3 / 96.9 and V_c(R0) 215.2 / 220.4. Here
  they are 92.3 / 96.8 and 215.3 / 220.6.
- **v3 is in tension with Bovy & Rix K_z:** P4 found 92 against the measured 66.4 ± 2.2. That score belongs to P4. The seal
  records the prediction only.

## Part D — ALMA (razor-thin Freeman stars + exponential gas; same radii, V_c and a₀(z) branches as AG4e)

AG4e is reproduced exactly: 126 cells, |Δ| = 0.

| release | max \|Δ log V²_bar,req\| | max \|Δ log M_gas,req\| | FLOOR flips | frozen reading |
|---|---|---|---|---|
| U4_27928 (2026-11-06) | 0.0009 | 0.055 | 0 | needs F (gas clause only) |
| GS4_24110, log M★ 10.89 (2026-11-28) | 0.029 | 0.45 | 4 | needs F |
| GS4_24110, log M★ 10.76 | 0.046 | 0.47 | 0 | needs F |

**Thick-disc variant (z₀ = 0.15 R_d):** reported in `s3_partD_alma.out`.

**What to file:** `ADDENDUM_F_DRAFT.md` scores v3's sealed AQUAL-disc requirement as a labelled parallel reading under
addendum E's rules. The owner must approve it, and it must be filed before 2026-11-06. The coordinator files it.

## Other crisp findings

- **AQUAL is not the algebraic law in thin discs.** On the exact Kuzmin solution, the in-plane AQUAL pull is ν₁ evaluated at
  the full off-plane |g_N|, not at the in-plane g_N. At R = 0.3a it is 11.7 % below the algebraic in-plane law (A1).
- **The MW external field's in-plane m = 1 pattern is physical and large in AQUAL.**
  - Exact tilted-field Plummer reference: peak-to-peak F_R of 4.3 / 9.7 / 15.8 % at 15 / 27.5 / 60 kpc.
  - The 3-D solver reproduces this to ≤ 0.5 % (C5).
  - The record's QUMOND linear-response estimate (hunt h81, |A| 0.3–1.4 %) is several times smaller.

## Record errors found

- **CFG493's `v2_disc` is noisy.** In `campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined.py:126-142` the
  gas V² comes from a ring-potential finite difference, which has log-singularity noise.
  - Point to point, V² flips sign on smooth Σ profiles: 2948, −2639, −1065 (km/s)².
  - CFG493's P3 gas-point mask and its g_bar inherit this. P3 moves from −10.302 to −10.167 once rebuilt on a smooth solve.
- **The QUMOND anisotropy in hunt h81 understates AQUAL's MW asymmetry.** See above.

## Input ledger

The full ledger is `ASSUMPTION_LEDGER.md`. The contaminated inputs and their sensitivities:
- **MW external field (h81, ΛCDM-processed 2M++):** e_N = 0 / h81 / 2 × h81 all give SHAPE EXCLUDED. The label does not
  depend on it.
- **McMillan17 discs (normalised in a fit with an NFW halo):** the census ±1σ band and the B2 / B2b / B3 envelope, with V20
  and slopes in `PREDICTIONS_V3.md`. The slope moves by ≤ 0.02.
- **SPARC / WALLABY e_N (catalogue sum):** step E only, at +0.000 / +0.018 dex in log a₀.
- **ALMA D_A (ΛCDM) and RC100 V_c:** inherited unchanged from AG4e.

## What this does not show

- **No vertical-force score against Bovy & Rix.** That belongs to P4.
- **No SPARC RAR refit.** That belongs to P4.
- **The μ_K² term is not solved.** That belongs to R6. Its first-order bound worsens the MW slope.
- **The EFE in κ uses the disc-axis geometry (γ = 0)** and catalogue e_N. P2 has no e_N on disk.
- **The high-z ALMA discs are treated as isolated.** No external-field estimate for them is on disk.
- **Every model is static, axisymmetric (except the 3-D EFE ratio) and in equilibrium.** None of the parts addresses
  non-equilibrium MW effects (bending waves, the LMC).

## Disclosures

**Amendments.** A1–A7 are in `FROZEN_CRITERIA.md`:
- A1, A2, A4, A6 and A7 were written pre-result for the numbers they govern. A6 is post-result for B3 only.
- A3 is post-result for Part A, and A5 is post-result for Part D. Each lists what had been seen before it was written.

**Frozen FAILs kept in the output:**
- A5iii: the 3-D γ = 0 grid anisotropy is 0.63 %.
- B3: its reference is the noisy `v2_disc`.
- D6: the gas clause fires near FLOOR.

**The A5 restatement D6′ does not bite under the mutate:** Newton's shift is 0.277 dex, under the 0.3 line. A7 and the frozen
D6 do bite.

**Memory:**
- Two development runs of Part A peaked at 1.74 GB and 1.68 GB RSS, above the 1 GB rule. Fine-grid and control solves ran
  in-process because SuperLU's heap fragments.
- Every AQUAL solve now runs in a short-lived child process. The committed runs peak at 0.32 GB in the parent and ≤ 0.90 GB
  in the children (`child_rss_MB` in each results JSON).

**Superseded runs:**
- One Part B run that used the old inversion was killed after amendment A6. Its κ lines were never read.
- Earlier development caches are left untracked: `_cache`, `_cache_r3` and `_cache_final`. They are not committed and can be
  deleted.

## Files

- **Solver:** `s3_aqual.py` (axisymmetric AQUAL with Kačanov + Anderson, the EFE along the axis, and the 3-D FFT ratio).
- **MW model:** `s3_mw.py`.
- **Parts:** `s3_partA_mw.py`, `s3_partB_kappa.py` with `s3_kappa_lib.py`, `s3_partC_seal.py`, and `s3_partD_alma.py` with
  `s3_alma.py`. Each has `.out`, `_results.json`, and `_MUTATE` files for A and D.
- **Lane checker:** `s3_v3_mw_seals.py`.
- **Writers:** `s3_write_md.py` and `s3_write_addendum_f.py`.

**Run order** (each `OMP_NUM_THREADS=1 nice -n 15`):
1. A
2. D
3. B
4. C, then `s3_write_md.py`
5. the checker

A rerun never overwrites a seal. It recomputes it and compares the hash.
