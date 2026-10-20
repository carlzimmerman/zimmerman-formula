# CFG892: can undetected binaries make the classical dSphs' excess?

**Label: PARTIAL (reached: Carina), canonical, graded, by the frozen rule. The alt footing gives the same class.**
Undetected binaries cannot make the excess in Draco, Ursa Minor or Sextans. The binaries that pass CFG861's cleaning add at most
3.3–3.5 km/s over the law at the 95th percentile, in the most generous allowed cell. Those three dwarfs need 4.9–7.8 km/s. Not one
of the 15,000 graded realizations per dwarf reached their observed cleaned dispersion. Carina, the graded dwarf with the smallest
excess, is reached only at the edge of the bracket: Q95 3.21 against a need of 3.195 km/s, in only 1–2 of the 15 cells (the
short-period-heavy P3/P4 at f = 0.7), at P ≈ 0.05. Crater II sits below the law. PARTIAL comes from Carina alone.

- **Criteria:** `FROZEN_CRITERIA.md` (5b5da1665), committed alone before any script. Block CFG890–899 (orchestrator reservation).
- **Script:** `cfg892.py` → `cfg892.out`, `cfg892_results.json`. `CFG892_MUTATE=1` → `cfg892_MUTATE.out`, `cfg892_results_MUTATE.json`.
  `cfg892_post.py` → `cfg892_post.out`, `cfg892_post.json` (POST HOC, not graded). One process, single thread, nice 10. Main run
  389 s at about 1.0 GB maximum RSS; MUTATE 5 s; post hoc 79 s. numpy/scipy only, nothing downloaded. A 1024³ run was live and
  was not touched.
- **Reuse:** CFG51's `reduce_walker.py` is imported unchanged. The data path is CFG861's: three Walker+2023 files, `build_stars`,
  `membership`, classical = LVD-matched with M_V ≤ −7.7, M = members with ≥ 2 quality epochs. CFG852's `delta_ups2` is extracted
  with `ast` (Υ_V = 2, Wolf at r_1/2 = 4/3 r_h, kernel ν_e). σ_law² = law(g_bar)·r_1/2/3.
- **Settings:** κ = ½ FITTED. Canonical a0 = 9.3603e-11 (graded), alt 1.1312e-10 (reported, same grid). Footings never pooled.

## The question

CFG861 found that detected binaries move the classical dSphs' excess very little (mean δ −0.045 dex). It left three caveats. (1) δ is a lower
bound: most M stars have 2 epochs, so long-period binaries escape the χ² test. (2) Instrument zero points were not modelled, and Sextans
pools three files. (3) The ~4.5 km/s single-epoch bound (McConnachie & Côté 2010) was not re-checked. This lane forward-models the
binaries that pass the cleaning. Each member keeps its real epochs and quoted errors.

The model per realization is v_ij = u_i + b_i(t_ij) + z_k + e_ij·n_ij, with u ~ N(0, σ_law) (H0 = law + binaries). b is a Keplerian RV
with probability f. The simulated data then go through CFG51's own steps: the two-pass velocity window, χ² p < 0.01 cleaning, and the
Gaussian MLE on first epochs (single) and on cleaned all-epoch means (clean). A paired no-binary twin is run alongside. R = 1000 per cell.

**Populations** (from the repo, or stated as brackets):
- P1: log-normal log P 5.03/2.28 (CFG93's values, which are the Raghavan+2010 numbers).
- P2: Duquennoy & Mayor 1991, 4.8/2.3 (CFG334).
- P3: mean 4.0 (CFG93's short-period-heavy variant).
- P4: flat in log P on 0.5–8 (CFG93).
- P5: P1 with thermal e (a bracket).
- All share q ~ U[0.1, 1], M1 = 0.8 M_⊙, e ~ U[0, 0.8] above 10 d, and periastron ≥ 3 × 10 R_⊙ (more generous than CFG93's 15 R_⊙),
  with failed draws redrawn.
- Graded f ∈ {0.3, 0.5, 0.7}.

**Graded statistic.**
- Q95 = the maximum over the 15 cells of the 95th percentile of σ_ex = √(σ_clean,sim² − σ_law²).
- σ_need = √(σ_obs² − σ_law²), where σ_obs = min(Walker σ_clean(M), σ_LVD·σ_clean(M)/σ_single(M)).
- A dwarf is "reached" if Q95 ≥ σ_need.

## Result (canonical, graded)

σ in km/s. Q95 is the most generous cell's 95th-percentile excess. P_max is the largest P(σ_clean,sim ≥ σ_obs) over the 15 cells.
I2 is the paired binary inflation of σ_clean (median / 95th) in the primary cell P1, f = 0.5.

| dwarf | \|M\| | Δ_LVD | σ_law | σ_obs (W / L → used) | σ_need | Q95 (cell) | P_max | reached | I2 P1 f0.5 | catch P1 f0.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| Crater II | 39 | −0.436 | 3.87 | 2.49 / 2.37 → 2.37 | 0 | 2.77 (P3, 0.7) | 1.00 | nothing to explain | 0.88 / 2.05 | 0.105 |
| Sextans | 192 | +0.509 | 4.40 | 7.95 / 6.57 → 6.57 | 4.88 | 3.27 (P3, 0.7) | 0.000 | no | 1.21 / 2.20 | 0.128 |
| Ursa Minor | 135 | +0.573 | 4.58 | 9.37 / 8.71 → 8.71 | 7.40 | 3.48 (P3, 0.7) | 0.000 | no | 1.18 / 2.29 | 0.136 |
| Draco | 263 | +0.632 | 4.61 | 9.07 / 9.21 → 9.07 | 7.81 | 3.41 (P3, 0.7) | 0.000 | no | 1.49 / 2.40 | 0.113 |
| Carina | 396 | +0.199 | 5.25 | 6.14 / 6.39 → 6.14 | 3.195 | 3.208 (P4, 0.7) | 0.053 | **yes (edge)** | 1.50 / 2.12 | 0.090 |

**CLASS: PARTIAL (reached: Carina).** Four dwarfs have σ_need > 0. One is reached and three are not.

- **Alt footing:** PARTIAL (reached: Carina). Sextans, Ursa Minor and Draco need 4.68 / 7.27 / 7.68 against Q95 3.31 / 3.51 / 3.48.
  Carina's alt need is 2.75 against Q95 3.22, so its margin is larger (P_max 0.23).
- **The undetected remainder is small.** The cleaning catches only 8–20% of injected binaries at these cadences, across all cells. That
  confirms CFG861's "δ is a lower bound" and matches CFG93's 9–13%. But the binaries it misses add only about 1.2–1.5 km/s in quadrature
  (median), or about 2.1–2.4 km/s at the 95th percentile (P1, f 0.5). The most generous cells give 3.2–3.5 km/s including sampling noise.

## Carina: how solid is "reached"? (POST HOC, `cfg892_post.py`, not graded)

Carina's margin was 0.013 km/s. The development runs at small R (below) had shown it flipping either way, so a seed check was added
after the graded run:
- Re-running the main-run seed reproduces the committed cell exactly (3.207657433723).
- Four new seed sets give a max-over-cells Q95 of 3.217, 3.270, 3.224 and 3.228. Over all five: mean 3.229, sd 0.024. **Reached in 5 of 5.**
- Only 1–2 of the 15 cells reach the need in each seed set. Pooled at R = 5000, the 95th percentile is 3.226 ± 0.019 for P4 f0.7 and
  3.199 ± 0.015 for P3 f0.7, with P(σ_clean,sim ≥ 6.144) = 0.055 and 0.051.
- None of P1, P2, P5 or f ≤ 0.5 reaches the need. The main-run values are 2.16–2.89 in those cells.

So "reached" is not seed noise under the frozen statistic. It holds only at the boundary of the allowed bracket: the most
short-period-rich populations, at the highest graded binary fraction, at the 5% level.

## Reported variants (not graded)

| variant | canonical | alt |
|---|---|---|
| σ_obs = Walker σ_clean(M) only | PARTIAL (Carina) | PARTIAL (Carina) |
| σ_obs = LVD-scaled only (Carina need 3.65 / 3.27) | **CANNOT EXPLAIN** | **CANNOT EXPLAIN** |
| bracket + f = 1.0 | PARTIAL (Carina) | PARTIAL (Carina) |
| bracket + P6 no periastron cut (unphysical) | PARTIAL (Carina) | PARTIAL (Carina) |
| P1 with R1 = 15 R_⊙, f 0.5 alone (CFG93 setting) | CANNOT EXPLAIN | CANNOT EXPLAIN |
| single epoch, no cleaning: Q95 vs CFG861 σ_bin | PARTIAL (Carina) | PARTIAL (Carina) |

Per-dwarf Q95 under the extensions (canonical; need / graded / + f 1.0 / + no-cut / R15):
- Sextans 4.88 / 3.27 / 3.70 / 3.43 / 2.44
- Ursa Minor 7.40 / 3.48 / 3.96 / 3.76 / 2.61
- Draco 7.81 / 3.41 / 4.00 / 3.58 / 2.49
- Carina 3.19 / 3.21 / 3.69 / 3.37 / 2.48

Even with every star a binary, or with unphysical sub-giant-radius orbits, Draco, Ursa Minor and Sextans stay short by 1.2–3.8 km/s.

**The 4.5 km/s bound, replaced by the forward model.** With no cleaning at all, the single-epoch 95th-percentile excess is
5.0–5.4 km/s for Draco, Ursa Minor and Sextans. CFG861's σ_bin = σ_LVD√(1 − 10^(−Δ_LVD)) for them is 6.6–8.4 km/s (6.4–8.2 alt),
so they are not reached even before cleaning. Carina is reached (4.57 vs 4.00), as CFG861 already noted (4.0 within 4.5).

The binary-only single-epoch dispersion (σ_true = 0.2 km/s, f 0.7, each dwarf's own M epochs and errors) has medians of 1.8–3.9 km/s
and 95th percentiles of 3.1–5.2 km/s across P1–P5. That is the same size as the ~4.5 km/s figure in McConnachie & Côté 2010. The paper
was not re-read (no download), so this re-derives the number under this lane's populations; it is not a check of the paper's text.
This lane's conclusion no longer depends on that bound.

**Other classical systems (reported).**
- Leo II (|M| 42) is reached: need 4.27 vs Q95 4.47 (alt 3.94 vs 4.54).
- Sculptor (|M| 91) is not: 5.82 vs 4.51 (alt 5.39 vs 4.72).
- Antlia II, Fornax and Leo I have σ_obs at or below σ_law, so there is nothing to explain.

**Flag fractions (diagnostic only; not used to narrow the bracket).**
- The no-binary twin flags 1.0% of stars, as expected at the quoted errors.
- The observed n_rm/|M| is 0.026 for Crater II, 0.057 Draco, 0.081 Ursa Minor, 0.083 Carina and 0.172 Sextans.
- The simulations give 0.03–0.07 at f 0.3, 0.04–0.11 at f 0.5, 0.06–0.14 at f 0.7 and 0.08–0.20 at f 1.0.
- Draco, Ursa Minor and Carina fit f ≈ 0.3–0.7. Crater II flags fewer than any f ≥ 0.3 predicts, but that is one star of 39.
- **Sextans flags more than any physical population at f ≤ 0.7** (maximum 0.139). Its observed δ = −0.161 is in the tail of the
  simulated δ (P(δ_sim ≤ δ_obs) = 0.077 at P1 f0.5). With the zero point measured as negligible (below), Sextans' extra flags point to
  a binary fraction near 1 or to under-quoted errors in some runs. Even at f = 1.0, Q95 is 3.70, short of its need of 4.88.

## Sextans instrument zero point (reported)

- **Z1, measured.** M2FS HiRes − Hectochelle = **+0.023 ± 0.106 km/s** (128 shared M stars, 107 after 3σ clipping, χ²/dof 1.03).
  MedRes − HiRes = −1.37 ± 1.86 km/s (5 stars). Correcting the epochs leaves CFG861's numbers unchanged: σ_single(M) 9.563
  (was 9.562), σ_clean(M) 7.948, 33 removed, δ −0.161. No M star changes membership on a re-run. Sextans' need stays 4.88
  (alt 4.68), not reached.
- **Z2, bracket.** Injecting offsets of (0, +x, −x) km/s for x = 0.5–3 raises the simulated flag fraction to 0.34 at x = 3. It raises
  Sextans' Q95 only to 3.61 (most generous cell), against a need of 4.88 (alt 3.70 vs 4.68). No offset reaches the need.

Zero points are not why Sextans resists the binary explanation. They also do not produce its large CFG861 shift: the measured offset is
too small. Zero points between runs within one instrument are not modelled.

## Controls

- **K1 PASS (binary fraction 0 reproduces CFG861 exactly).** With zero binary motion on the real velocities, the lane's pipeline
  reproduces `cfg861_results.json` for all 10 systems with |M| > 0. |M|, n_rm, and σ_single(M) and σ_clean(M) with their ± errors all
  match with maximum difference 0. Every M star passes the re-applied window, and the per-star means, errors and p values are identical
  to the reducer's. Δ_LVD (both footings) is identical, and σ_law matches σ_LVD·10^(−Δ/2) to ≤ 4.4e-16 relative.
- **K1b PASS.** The vectorised MLE matches `mle_sigma` on the 20 real sets to ≤ 1.0e-6 km/s (tolerance 1e-4).
- **K2 PASS.** At f = 0, the median σ_clean,sim/σ_law is 0.979 (Crater II, 39 stars) and 0.997–0.999 for the others. False-flag
  fractions are 0.0099–0.0103.
- **K3 PASS.** 2π AU/yr = 29.7853 km/s vs 29.78 (1.8e-4). The circular-orbit RV at the analytic peak equals K to 1e-12. The period-mean
  RV at e = 0.6 is 1e-15 km/s. The Kepler residual at e = 0.95 is 9e-16.
- **MUTATE BITES (3/3).** Population: P ~ 16–63 d, q ~ U[0.5, 1], e = 0, no cut, f = 0.7.
  - (a) The median catch fraction is 0.77–0.88 in every graded dwarf (≥ 0.70 required).
  - (b) The cleaning cuts the median excess from 11–16 km/s (single) to 1.5–9.3 km/s (clean) in every dwarf.
  - (c) The single-epoch class is COULD EXPLAIN (all four dwarfs with a need reached).
  - For information, the cleaned class also flips to COULD EXPLAIN (all four reached). The grading responds when binaries are large
    enough to matter.

## What this means for the record

This closes CFG861's three caveats as far as the Walker+2023 multi-epoch data allow.
- (1) Undetected binaries are real: about 80–90% escape the cleaning. But they add only about 1.2–1.5 km/s in quadrature (median), at
  most about 3.5 km/s at the 95th percentile in the most generous allowed cell.
- (2) The Sextans zero point is measured at +0.02 ± 0.11 km/s and changes nothing.
- (3) The 4.5 km/s bound is replaced by a forward model at each dwarf's cadence. It gives a number of the same size, and the conclusion
  no longer leans on it.

The three classicals with the largest excess (Draco, Ursa Minor, Sextans; +0.35 to +0.60 dex after cleaning) cannot be explained by
binaries under any bracket tried. That includes f = 1 and orbits inside the giants' radii. Carina's smaller excess (+0.17 dex after
cleaning) can be explained only at the edge of the bracket, with P ≈ 0.05. The frozen rule therefore says PARTIAL. Physically, the
classical-dwarf excess is not a binary artefact, except possibly Carina's small one.

Together with CFG51/CFG93 (ultra-faints trimmed, not removed) and CFG861, binaries are not the shared systematic behind the
faint-dwarf excess. Other shared systematics (Υ, membership, the small-sample Wolf estimator, radial coverage) are not tested here.
Under the bare law the excess stands. In the framework it means bound cold energy mass inside r_1/2, which no supply channel on the
record provides for satellites (CFG842).

## Disclosures and limitations

- **Development runs.** Two development runs (R = 60 and R = 250, scratch copies, outputs discarded) were made for timing and
  debugging after the criteria commit. They showed Carina on the boundary: not reached at R = 60, reached at R = 250. `cfg892.py` was
  not changed after any run. The K3 implementation below was written before the first run.
- **K3 wording.** "A circular orbit's RV amplitude equals K to 1e-9" is checked as the RV at the analytic peak phase equal to K, plus
  the sampled RV staying within ±K. Sampled extrema cannot hit the peak to 1e-9.
- **The graded Q95 is a maximum over 15 Monte-Carlo cells,** so it is biased upward by MC noise. That bias is generous to binaries.
  The post hoc above gives its size.
- **σ_obs = min(W, L)** is the more generous choice. For Carina it is the Walker value. The LVD-scaled value alone gives CANNOT EXPLAIN.
- **Not varied:**
  - the intrinsic dispersion is uniform (no radial profile), and the M subset's footprint may differ from the LVD sample's;
  - Δ's own systematics (Υ_V, distance, r_h) are not varied;
  - errors are taken as quoted;
  - zero points between runs or configurations within one instrument are not modelled;
  - triples are ignored;
  - q and M1 are fixed;
  - field period shapes are assumed for old metal-poor giants;
  - single-epoch stars are not used (as in CFG861).
- **Post hoc.** `cfg892_post.py` (Carina seed check) was written after the graded run. It reuses `cfg892.py`'s functions via `ast` and
  does not change the class.

κ = ½ fitted; cold energy mass required; not theory closed.
