# CFG912: is the red/spheroidal isolated-lens excess partly the framework's own catalogue two-halo term? NOT ENVIRONMENT on both footings: the red − blue difference in the term explains 6–7% of the split, robust to every bracket

**What was done.**
- CFG903's catalogue two-halo machinery was rerun per colour class: observed KiDS-bright neighbours, each with its baryons +
  catchment cold energy, random-clone subtracted, smaller neighbours excluded inside the lens's own edge, no free amplitude.
- The term is mapped onto **B21's RAR g_bar bins**. Lens–source pairs of lens l fall in bin k at
  R ∈ [√(GM_l/g_{k+1}), √(GM_l/g_k)]. Each lens is weighted by W_l × annulus area, ΔΣ is area-averaged over the annulus, and
  Δg = 4GΔΣ.
- The term is then subtracted from B21's published colour-bin g_obs inside CFG850's window, 10^−13.3 ≤ g_bar < 10^−11.9.
- The re-fitted red and blue amplitudes are compared with CFG850's.
- Statistic: **f_env = (δA_red − δA_blue)/(A_red − A_blue)**, the share of the split the environment explains, and z_corr,
  the corrected split in σ.

Criteria: `FROZEN_CRITERIA.md` (96de8091f, committed alone before any script). `AMENDMENT_A1.md` (e5a9fc4c9) is **post hoc**,
written after the frozen MUTATE failed; it adds MUTATE-B. See Controls.

## Result (primary: I0, u−r 2.0, M★ shift +0.123 dex on red, W 500, P1, E1, C1′)

| footing | A_red | A_blue | split | δA_red (two-halo) | δA_blue | A_red^corr | A_blue^corr | **f_env** | **z_corr** | σ_jk(f_env) | class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| canonical (9.3603e-11) | 1.451 ± 0.067 | 1.016 ± 0.086 | 0.435 (3.98σ) | +0.061 | +0.033 | 1.390 | 0.983 | **+0.064** | **3.73** | 0.004 | **NOT ENVIRONMENT** |
| alt (1.1312e-10) | 1.324 ± 0.061 | 0.928 ± 0.078 | 0.396 (3.98σ) | +0.059 | +0.033 | 1.264 | 0.895 | **+0.067** | **3.71** | 0.005 | **NOT ENVIRONMENT** |

- Footings are never pooled. No class boundary is within 2σ_jk. Adding the jackknife variance of δA_red − δA_blue leaves
  z_corr at 3.73 / 3.71.
- The term lifts **both** colours: about 4% of A for red and 3% for blue. Their difference, about 0.028 in A, is
  **1/16 of the split**.
  - Closing the split needs **15.7× / 14.9×** the catalogue red − blue difference.
  - Bringing z_corr down to 2 needs 7.8× / 7.4×.
  - Arithmetic, not a run: even at the ≈3.5× amplitude CFG903's outer-halo data want, f_env would be ≈0.22.
- After the term the blue lenses stay on the law: (A_blue^corr − 1)/σ = −0.20 canonical, −1.34 alt.
- Sérsic split, reported only, using the colour-proxy vectors (red → spheroid, blue → disc): f_env +0.066 / +0.069, z
  3.81 → 3.56 / 3.81 → 3.54.

### Per bin, canonical (alt in `cfg912_score.out`, same pattern)

R/B = in the red / blue window. ΔΣ_2h is in Msun/pc². "Host share" is the part from neighbours more massive than the lens.

| file g_bar | window | ΔΣ_2h red / blue | Δg/g_law red / blue | data g_obs/g_law − 1, red / blue | host share red / blue |
|---|---|---|---|---|---|
| 4.17e-14 | R | 0.41 / 0.28 | +0.099 / +0.077 | +0.77 / +0.49 | 1.23 / 1.15 |
| 7.36e-14 | RB | 0.46 / 0.31 | +0.084 / +0.065 | +0.61 / −0.08 | 1.09 / 1.06 |
| 1.30e-13 | RB | 0.50 / 0.31 | +0.067 / +0.049 | +0.46 / +0.41 | 1.04 / 1.03 |
| 2.29e-13 | RB | 0.53 / 0.30 | +0.053 / +0.035 | +0.27 / +0.25 | 1.02 / 1.02 |
| 4.04e-13 | RB | 0.54 / 0.29 | +0.041 / +0.026 | +0.34 / +0.09 | 1.01 / 1.01 |
| 7.13e-13 | RB | 0.56 / 0.29 | +0.031 / +0.019 | +0.32 / −0.25 | 1.01 / 1.01 |
| 1.26e-12 | B | 0.55 / 0.27 | +0.023 / +0.013 | +0.27 / −0.27 | 1.00 / 1.00 |

- Red lenses do get a larger term: ΔΣ_2h 0.41–0.56 against blue's 0.27–0.31 Msun/pc², rising toward high g_bar where blue's
  does not.
- But the term is 1–10% of g_law in both classes, while the red excess is +27% to +77%.
- **Hosts supply all of it** (host share 1.00–1.23):
  - the window annuli lie inside the lens's own edge (x_x = r_x/ρ_l ≈ 3.0 canonical, 2.75 alt; ×1.15 for shifted red);
  - so smaller neighbours act only from outside, and net slightly negative after the random subtraction.

## Brackets (one at a time; frozen class by f_env / z_corr)

| bracket | canonical f_env (z_corr) | alt f_env (z_corr) | class |
|---|---|---|---|
| primary | +0.064 (3.73) | +0.067 (3.71) | NOT ENVIRONMENT |
| ISO-f30 (I1, 57,261 lenses) | +0.073 (3.69) | +0.081 (3.66) | NOT ENVIRONMENT |
| ISO-B21n (I5, count-matched to B21) | +0.067 (3.72) | +0.069 (3.70) | NOT ENVIRONMENT |
| P0, neighbour cold energy as a point (δA 0.176 / 0.146) | +0.070 (3.70) | +0.065 (3.72) | NOT ENVIRONMENT |
| P2, diffuse cold energy | +0.034 (3.85) | +0.035 (3.84) | NOT ENVIRONMENT |
| W300 / W1000 | +0.070 / +0.059 | +0.073 / +0.062 | NOT ENVIRONMENT |
| CUT-2.5 (see disclosure) | −0.021 (4.07) | −0.024 (4.07) | NOT ENVIRONMENT (opposite-sign label) |
| MSTAR-0, no M★ shift (A_red 1.587 / 1.448) | +0.040 (4.77) | +0.043 (4.75) | NOT ENVIRONMENT |

**Robust:** no bracket changes the class on either footing. The largest f_env in any frozen bracket is 0.081.

**Reported only:**
- shift (+0.20, 0): +0.073 / +0.076, z_corr 2.70 / 2.69.
- shift (+0.123, +0.05): +0.058 / +0.061.
- **E0** (no exclusion; double counts the lens's own satellites): +0.191 canonical, **+0.206 alt**. Alt would read PARTIAL by
  the numbers, but this variant has no class weight because it double counts.
- E2 (hosts inside r_x dropped too): −0.017 / −0.022. Removing the hosts removes the term.
- Annulus edges centred on the file's g_bar values: +0.065 / +0.068.

## Reading

1. **The red/blue split is not the framework's catalogue environment.**
   - The neighbours KiDS sees, with their baryons and catchment cold energy, do lens more around red isolated lenses than
     around blue ones in the RAR window.
   - The difference is 6–7% of the 0.4-in-A split (4σ), with a jackknife spread of 0.004.
   - It holds for stricter and looser isolation, every cold-energy profile, every photo-z window, both M★ treatments and both
     footings.
2. **The term itself is not negligible.** It raises both colours by 3–4% in A, mostly through hosts of satellites that leak
   through the photo-z isolation, as in CFG903. It does not discriminate by colour nearly enough.
3. **What it would take.** About 15× the red − blue catalogue difference to close the split. That is not attached to
   catalogued galaxies' catchments at any amplitude the record has seen (CFG903's outer data want ×3.5 overall).
4. **The open sector stands as before:**
   - CFG850: the split survives the known M★ bias;
   - CFG885: and native distances;
   - CFG912: and the framework's own two-halo term.

   With the term the split is A_red^corr − A_blue^corr = 0.41 / 0.37 (3.7σ). Its cause remains open. Nothing here says the data
   favour the framework.

## Controls

| control | result |
|---|---|
| K0a: table I0 lenses = lr_lenses; reconstructed u−r > 2.0 = lr_lenses `typ` | 181,431 identical (ra, dec, z, Mgal); red 88,079 / blue 93,352 exact; I1 ⊂ I0 ⊂ I5 |
| K0b: this lane's pair loop = CFG903's committed-run v0 histograms (lens + random, 4 bins) | max \|Δ\| = 0; pair counts identical (35.6M / 17.0M / 13.4M / 10.7M lens) |
| K1: two-halo ≡ 0 reproduces CFG850's committed rows (10 rows × 6 quantities) | max \|Δ\| = 0 |
| K2a-i: annulus integral (Simpson in ln X) vs adaptive quadrature of CFG903's F2 | 7.7e-7 (tolerance 2e-3) |
| K2a-ii: annulus kernel vs CFG903's independent brute-force polar F + Gauss–Legendre | 2.9e-4 (tolerance 3e-3) |
| K2c: uniform neighbour field gives ΔΣ = 0 | point 1e-16, cold 1.6e-4 of Σ₀ (tolerance 2e-3) |
| K3: random halves A − B, window mean | canonical red +0.2σ, blue −0.7σ; alt +0.2σ, −0.8σ |
| Jackknife coarse cells vs fine (full sample) | f_env +0.065 vs +0.064 canonical; +0.068 vs +0.067 alt |
| **MUTATE (frozen): FAILED**, see below | blue P1 Δ 5e-29; two of four bins miss 1%; f_env fell |
| MUTATE-B (A1, post hoc): host at 0.01 Mpc around every 10th I0 red lens | **recovered**: P0 red change = direct per-lens computation in all 9 bins (to the printed 4 digits); blue unchanged (P0 exactly, P1 3e-16 relative); f_env 0.070 → 1.37 (P0), 0.064 → 0.44 (P1, PARTIAL) canonical; alt 0.065 → 1.37, 0.067 → 0.48 |

**The frozen MUTATE failed, and why.** It injected 8,808 hosts (log M_b 11.325) at d = 0.4 Mpc.
- **The expectation was wrong physics.** At 0.4 Mpc the host sits inside the window annuli for most lenses. A point mass in
  the outer ≈40% of an annulus gives a *negative* annulus-averaged ΔΣ. So the injection lowered the red term in the window, and
  f_env fell: P0 0.070 → 0.004 canonical.
- **The pipeline transmitted it faithfully.** f_env recomputed with the *direct* expected injection gives +0.0043, against the
  pipeline's +0.0041 (alt −0.0010 vs −0.0012).
- **Per bin:** the two bins carrying most of the signal match to 0.05% and 0.4%. Bin k = 6 is a near-cancellation (miss 0.8% of
  the gross). Bin k = 8 holds 183 lenses packed into one x bin, where the frozen area-uniform within-bin average is not exact
  for a delta-like separation (miss 3.5% of the gross).
- **Blue:** P1 canonical differs by 2.9e-16 relative (A1 quoted ≈ 4e-16), from kernel-cache order.
- The real neighbour distribution is smooth across bins, so this averaging does not bias the result (K2c, K3 and the
  coarse/fine agreement). The frozen MUTATE is nonetheless recorded as FAILED.
- MUTATE-B was added post hoc, with the host interior to every annulus, and recovers the injection.

## Disclosures

- **Proxy sample.**
  - The amplitudes are B21's published colour bins: B21's sample, isolation, and u−r 2.5 cut in B21's photometry.
  - The term is computed for the record's reconstruction: I0, LePhare MAG_ABS u−r 2.0.
  - ISO-B21n brackets the sample count. Nothing more is possible with stacked public files.
- **CUT-2.5 is not a usable proxy.** On the LePhare MAG_ABS system only 1,432 I0 lenses (0.8%) have u−r > 2.5. So that bracket
  compares an extreme-red handful with nearly everything; it is reported as frozen.
- **Implementation differs from the frozen text in one place.**
  - The criteria said the extended kernels would come from tabulated F(u, v) and G(u, v).
  - Instead, F is evaluated directly with CFG903's F2 at every node: Simpson in ln X over each annulus, 4-node area-uniform
    Gauss–Legendre per x bin. No table and no interpolation.
  - The table half of K2a was therefore replaced by Simpson vs adaptive quadrature (K2a-i). The brute-force half is as frozen.
- **Frozen bin step.** The frozen edges use a step of 0.246606 dex. The exact (log 5e-12 + 15)/15 is 0.246598, a 1.2e-4 dex
  difference at the top edge. File-centred edges move f_env by ≤ 0.001.
- **Development runs, all disclosed.** The criteria, classes, brackets and all numerics are unchanged across them.
  - **Score run 1** was stopped by this lane's RSS watchdog (1.2 GB) before any amplitude was computed.
  - **Score run 2** printed the canonical primary, the brackets and two reported rows, then was stopped by the watchdog. Those
    numbers are identical to the reported run.
  - Fix: kernels are now computed before the histograms are loaded, histograms are streamed from the zip members, and F2 calls
    are chunked to 100 nodes.
  - **The frozen MUTATE score was rerun** after the A1 code edits so the committed output matches the committed script:
    identical numbers (max |Δ| 0); only a check label changed. A1 did not change the pair stage's main or MUTATE code paths,
    so those pair outputs were not rerun.
- **Exclusion uses catalogue lens masses** (no profiled one-halo fit in this lane); N_l is taken at the 0.1-dex lens-cell
  centre. In shifted variants, r_x uses the shifted mass while the less-massive flag stays on catalogue masses.
- **Not modelled** (as CFG903): B21's radial limits on RAR pairs, if any; neighbours' photo-z mass errors; true-z lensing
  efficiency; catchment sharing, which can only lower the term; faint neighbours beyond C1′; the lens's own share of a host's
  catchment.
- **The split σ ignores cross-covariance** between the two colour bins (as CFG850). The term's own noise enters only through
  the jackknife (σ_jk(δA_red − δA_blue) = 0.0019).

**Compute.** One core, nice 10, watchdog 1.2 GB / 20 min.
- Colour stage: 1 s, 458 MB.
- Pairs: 6–16 s per bin, peak 966 MB.
- Score: 151 s, peak 1131 MB.
- MUTATE / MUTATE-B: 6–15 s per bin; score about 55 s, ≤ 883 MB.

## Files and rerun

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`
- `cfg912_lib.py`: binning, classes and injection; imports CFG903's `cfg903_lib.py` read-only.
- `cfg912_colour.py`: u−r per table lens, K0a. Output → `cfg912_colour.{out,json}`.
- `cfg912_pairs.py BIN`: histograms, K0b accumulators. Output → `cfg912_pairs_bin{1-4}[_MUTATE|_MUTATE_B].{out,json}`.
- `cfg912_score.py`: kernels, amplitudes, brackets, jackknife, K1–K3, MUTATE.
  - Main → `cfg912_score.out`, `cfg912_results.json`.
  - `CFG912_MUTATE=1` → `*_MUTATE*`.
  - `CFG912_MUTATE=B` → `*_MUTATE_B*`.
  - Exec's read-only: cfg850.py's definitions (through cfg829's `load`/`amp`) and cfg903_score.py's profile/F2/brute
    definitions.
- Large arrays go to `../../../_external_data/cfg912_work/` (not committed). Inputs read: CFG903's stage arrays and
  committed-run histograms.
- Rerun from this directory, with `OMP_NUM_THREADS=1 nice -n 10 python3`, in this order:
  1. `cfg912_colour.py`
  2. `cfg912_pairs.py 1..4`
  3. `cfg912_score.py`
  4. then the same pairs + score with `CFG912_MUTATE=1`, and then with `CFG912_MUTATE=B`.

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw KiDS data, framework-native neighbours (no ΛCDM halo-model
two-halo term); not theory closed.
