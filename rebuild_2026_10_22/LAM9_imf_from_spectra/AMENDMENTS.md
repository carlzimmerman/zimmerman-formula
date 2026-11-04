# LAM9 amendments, dated

`FROZEN_CRITERIA.md` (9c1f411110) is unedited. κ = ½ FITTED; not theory closed. Footings are never pooled. Nothing here
says the data favour the framework.

## 2026-11-04, A1: download, templates and run details, written before any fit

### The download
- The owner approved the download on 2026-11-04 ("Yes, 1.41 GB set"), for exactly the five files in the criteria's table.
  Nothing else was fetched.
- The files were fetched with curl and resume from the MILES share named in the criteria into a new, empty
  `_external_data/lam9_emiles_bi_basti/`.
- All five sizes match the table: 1,409,001,566 B in all. Sizes and SHA-256 sums are in `lam9_download.json`. The tarball's
  SHA-256 is 4a730867e6805d4a54c828f42c31f296df8b8bf5c099b1bb95e0418a5c473d09.

### The tarball
- It has 8904 members. All are regular files with flat names, and none has an absolute path or "..".
- It holds 14 bimodal slopes, not the 13 the MILES page lists: Γb 1.00 is there too (8904 = 14 x 53 x 12). The frozen
  13-slope grid is kept, so Γb 1.00 is not used.
- The 1092 frozen spectra were extracted by explicit member list into a new, empty `fits/` folder. Their names, sizes and
  SHA-256 sums are in `lam9_template_manifest.txt`, in reg_dim order (age, [M/H], Γb).
- Each file has 53,689 float32 pixels at 1680.2 + 0.9 i Å (air wavelengths), in L_λ per M_sun formed.
- The FITS headers say nothing about the library joins, so m7 stays as frozen.

### The templates (`lam9_templates.py`, `.out`, `.json`; no galaxy data)
- 3500-9399.5 Å is kept.
- **C4 PASSES.** For all five frozen templates the synthetic M(*+remn)/L_V is 0.7 % below the MILES table (ratio 0.9927-0.9929).
- Reference ratios at 12 Gyr and [M/H] +0.06: Υ_V(BI 1.3) / Υ_V(CH) = 1.0835 and Υ_V(BI 1.3) / Υ_V(KU) = 1.0051.
- Single-template α at 12 Gyr and +0.06:

  | Γb | 0.3 | 0.5 | 0.8 | 1.3 | 2.3 | 3.0 | 3.5 |
  |---|---|---|---|---|---|---|---|
  | α | 4.70 | 2.55 | 1.36 | 1.00 | 1.40 | 2.03 | 2.66 |

  α is U-shaped in Γb because top-light IMFs leave heavy remnants. The largest bottom-heavy α on the grid, 2.66, is below
  the α of 4.5-6.2 that Q1 needs (criteria, "Known before the fit").

### Step 5 and the K donors (`lam9_fit.py --prepare`: `lam9_prepare.json`, `lam9_k_donors.csv`; no fit)
- The stack rebuild matches stage 0 exactly (largest difference 0).
- Of the 2526 candidates, 1586 pass step 5 and 940 fail it. C1 (N ≥ 1000) passes.
- The failures come from the Na I feature landing on OH sky lines. In 200 sampled failures, 48 % of the Na I feature pixels
  sit on dilated OH spikes (m4) and 27 % on the coherent mask (m5).
- The pass rate is 0.99 at z 0.04-0.063 and 0.37-0.55 elsewhere, so the graded sample leans to that redshift window.

### Changes and additions, all before any fit
1. **K1's thirds.** The criteria cut them on the χ²_a-scaled Na I S/N, which exists only after the fits. They are cut on
   stage 0's χ²_kin-scaled Na I S/N instead (edges 62.5 and 80.1 over the 1586). The synthetic noise still uses each donor's
   own χ²_a.
2. **K1's donors.** Each third gets a permutation with seed 20261105, written to `lam9_k_donors.csv`.
   - The first 110 of each third are fitted first (`--phase donors`).
   - The K1 donors are the first 100 successful variant-A fits in that order.
   - These are the real fits of those sums, and they are not repeated later.
3. **Order.** The donors are fitted first, then K1 and K2. If K1 fails, every label is NOT MEASURABLE, as frozen, and the
   remaining fits are not run.
4. **K2's IQR.** Until the full fits exist, IQR(h4_int) is taken over the 1586 step-5 galaxies. The graded sample is the
   same galaxies minus fit failures.
5. **K rows (reported, not graded).** Step a's unregularised Γb and α are also recorded for every synthetic.
6. **Q2's harness.** RQ3's `acceptance.py` is loaded with this lane's folder as its working folder. CRG1's cache folders are
   therefore made here (untracked), and nothing is written in HX1's folder. This meets the frozen "temporary copy" rule.
   HX1's output handle goes to memory, as frozen.
7. **Execution.**
   - The fits run as four single-thread shards, split by index mod 4, so each sum is fitted once. Merged outputs are sorted by
     plateifu.
   - `compute_queue/heavyq.py` is blocked at its head of line. Another process, a 6.1 GB virtual machine, is above the
     queue's 4 GB limit, and 35 GB jobs are waiting.
   - Each shard is under 1 GB, which the standing rule lets run beside other jobs. So the shards run directly with
     `nice -n 10`.
   - They still meet the job contract: SIGTERM or `compute_queue/YIELD` gives exit 75 at a sum boundary, and `--resume`
     continues.
8. **Colour row (reported, not graded).** α_KU2 is split by NSA elpetro u - r (absolute magnitudes as stored; the h units
   cancel in a colour) at SI2's boundary, with red meaning u - r > 2.0. This is done for both variants.
   - Reported per colour and footing: the median α_KU2 with its 95 % bootstrap interval, and R1 - R0.
   - It is to be read beside the record's red-versus-blue lens split (BL1, SI2). It grades nothing.
   - The graded sample is gas-poor, so the blue side will be small. Its count is printed.

### A code test, disclosed (no real flux was fitted)
- **Setup.** Three single-template synthetics (10 Gyr, [M/H] +0.06, Γb 1.3, 2.3 and 3.0) on one sum's grid, masks and LSF,
  with that sum's noise x 1.5.
- **Without noise,** both steps return the input exactly.
- **With one noise draw,** step a's Γb is within 0.1 of the input. Step b's Γb (regul 100) is 0.4-0.6 low, and its α is
  1.1-3.0 times the input, because the smoothed weights reach the remnant-heavy Γb 0.3-0.5 end.
- Nothing is changed for this. K1 is the frozen test of exactly this, and it runs first.
- **Timing.** About 7 s per fit with noise, so about 14 s per sum for both variants.

κ = ½ FITTED; not theory closed.
