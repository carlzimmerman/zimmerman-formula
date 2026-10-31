# RF1_mw_halo_free_baryons: AMENDMENTS (dated; each states whether before or after the numbers it concerns)

**A1, 2026-10-31, after the UNDETERMINED result (fed5cbfee6) and before any graded number at the new row.**

A halo-free bulge mass is now on disk. The README's closing list (item 1) and the frozen criteria (verdict item 2,
9468ee04b2) say what follows: add the row to `HALO_FREE_BULGE`, wire the frozen grade, run. Nothing in the frozen lines,
grids, gas column, shapes or classes changes. Committed text above this file is left as written.

**The row.** Valenti, Zoccali, Gonzalez, Minniti, Alonso-García, Marchetti, Hempel, Renzini, Rejkuba 2016, A&A 587, L6
(arXiv:1510.07425). On disk: `_external_data/rf1_valenti2016/valenti2016.pdf` (sha256 77250ff5…95be1, the arXiv PDF) and its
extracted text `valenti2016.txt` (sha256 e395606d…8ed9f0c74b); both untracked, as the record keeps downloads. The script reads
the value from the text file, not from this note.

- Value: "The Milky Way bulge stellar mass within (|b| < 9.5°, |l| < 10°) is 2.0 ± 0.3 × 10¹⁰ M☉" (§3.2 and abstract).
- What it is: mass in stars and remnants, from VVV red-clump counts scaled to the Zoccali+03 SOFI luminosity function and the
  Zoccali+00 NICMOS main-sequence IMF measured down to 0.15 M☉; Salpeter above 1 M☉ and slope −0.3 below 0.15 M☉ assumed;
  Zoccali+00 initial-to-final mass relation for remnants; 18 % disc decontamination near the red clump.
- Class: **LITERATURE-INPUT, photometric star counts; no dynamics, no halo.** The paper: previous estimates were "all model
  dependent"; theirs is "the first fully empirical estimate".
- Error: ±15 % "including disk contamination, extrapolation of the IMF, mass of the remnants, and stellar population gradients".
- Caveats carried into the ledger: the window is a projected box ~2.8 × 2.7 kpc not limited along the line of sight, so it
  holds bar mass beyond the bulge's dynamical extent (the authors give this as the reason it sits above dynamical values); the
  RF1 bulge *shape* is still McMillan's rescaled, labelled; the IMF above 1 M☉ is assumed, not measured.

**Grade, as frozen (item 2).** At M_bb = 2.0 × 10¹⁰ on the Σ_b (McKee ±2σ, 5 values) × R_d (BH&G16 ±2σ, 7 values) box with
McKee's gas 13.7, background A, PRIMARY V_last: **PASS on halo-free baryons** if any cell passes L1, L2a, L2b, L3; **FAIL on
halo-free baryons** if none does; the LN16 tag (R_d in 2.38–2.90) is stated either way. Every cell of that box is inside both
±2σ ranges by construction. Graded keys: OS1|canonical|PRIMARY, OS1|alt|PRIMARY, N (footings coincide, K6).

**Reported, not graded:** the same box at 1.7 and 2.3 × 10¹⁰ (±1σ), VARIANT V_last, background B.

**New check K8:** the parsed value and error equal the sentence on disk, and the text file's sha256 equals the one above.

**Expectation on record, from the committed LOOKUP at 1.88 and 2.12 × 10¹⁰ (not a prior):** passes only at R_d 1.93 on OS1 alt
and native N; none at R_d ≥ 2.6; OS1 canonical PRIMARY none. So PASS (WIDE PRIORS ONLY, outside LN16) on alt and N, FAIL on
OS1 canonical. If the run differs, the run stands.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
Nothing here says the data favour the framework.

**A2, 2026-10-31, after A1's numbers; documentation only, no grade changes.** Open input 4 (R_d read directly) is now read
from the papers on disk: `_external_data/rf1_rd_sources/licquia_newman_2016.pdf` (arXiv:1607.05281) and
`bland_hawthorn_gerhard_2016.pdf` (arXiv:1602.07702), with extracted text; untracked.

- **Licquia & Newman 2016, Table 1 and Table 3.** 29 inputs, 15 visible and 14 infrared, every one photometric or star-count
  (Spacelab, COBE/DIRBE, 2MASS, DENIS, SDSS, SEGUE, GLIMPSE, pencil-beam CCD surveys); no rotation-curve or halo fit among them.
  Class: LITERATURE-INPUT, halo-free. Bayesian-model-averaged results (Table 4): IR only 2.51 (+0.15/−0.13), visible only
  2.71 (+0.22/−0.20), combined **2.64 ± 0.13 kpc**; raw ensemble median 2.5 ± 0.2 with interquartile range 1.2 kpc. Single
  exponential, R₀ = 8.33 assumed where the measurement scales with it (α = 1 for the IR map fits; at RF1's R₀ 8.122 those
  scale by 0.975). Individual halo-free inputs at or below 2.3 kpc: B06 1.90 (±0.48 assigned), LC&M14 2.00 ± 0.40, P98
  2.10 ± 0.53, P13 2.12 ± 0.20, R12 2.20, C99 / S02 / K07 2.25, D&S01 2.26 ± 0.22, O96 2.30, L&L00 2.30, M15 2.34 ± 0.48.
- **Bland-Hawthorn & Gerhard 2016, §5.1.2.** "A statistical analysis of the main papers (15 in all) on this topic leads to
  R_t = 2.6 ± 0.5 kpc", infrared point-source studies; 2.5 ± 0.4 without GLIMPSE. The ±0.5 is the spread of those papers, not
  an error on a mean. Their thick disc, chemistry-defined: **R_T = 2.0 ± 0.2 kpc** (§5.2.2). They add that "a short
  scalelength finds strong support from dynamical studies" (Bovy+12b mono-abundance populations, 2 kpc inner to 3 kpc outer);
  those are kinematic, not photometric, and are not used here.

**What this says about A1's passing cell (R_d 1.93 for both discs, P4's B3 single-R_d convention).**
- Against LN16's halo-free ensemble mean: 1.93 is 4.1σ below the IR-only value and 5.4σ below the combined value. Against
  BH&G16's spread it is 1.3σ low. Both statements are halo-free; they differ because one is an error on a mean and the other
  a scatter. The frozen LN16 tag (2.38–2.90) stands as the sharper of the two, and A1's PASS is correctly labelled WIDE PRIORS
  ONLY.
- A thin disc at 1.93 is not supported by the star-count ensemble; a **thick** disc at 1.93 is inside BH&G16's 2.0 ± 0.2.
  RF1's grid gives both discs one R_d, so no cell holds thin 2.5–2.6 with thick 2.0, which is what the halo-free star counts
  actually describe. That cell is the next thing to grade, and it is not in this lane's frozen box (it would be an A3 with
  its own frozen line, or a lane of its own).
- GD1's McMillan verdict keeps its label (FAIL against ΛCDM-processed baryons). On halo-free star counts the route E Milky
  Way verdict is: canonical OS1 FAIL; alt OS1 and native N pass only on a single-R_d disc the star-count ensemble disfavours
  at 4–5σ; a two-scale-length disc untested.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

**A3, 2026-10-31, FROZEN before any number from it.** The two-scale-length disc A2 named. Separate script `rf1_a3_two_rd.py`;
`rf1_mw.py` and its outputs are not touched.

- **Cell.** Stars: thin and thick exponential discs with their own radial scale lengths R_t and R_T, McMillan's vertical
  scale heights and McMillan's thin share of the stellar surface density at R₀ (both held and labelled, as in every RF1 cell);
  Σ_b at R₀ on McKee's grid (40.3, 43.7, 47.1, 50.5, 53.9); gas McKee 13.7 on McMillan's radial forms; bulge M_bb = 2.0 × 10¹⁰
  (Valenti+16, A1) on McMillan's shape rescaled.
- **Grid, from the halo-free star counts read in A2.** R_t ∈ {2.38, 2.51, 2.64, 2.77, 2.90} kpc (LN16 combined 2.64 ± 0.13,
  ±2σ, with the IR-only 2.51 inside it); R_T ∈ {1.6, 1.8, 2.0, 2.2, 2.4} kpc (BH&G16 thick 2.0 ± 0.2, ±2σ). 125 cells.
- **Lines, rules, backgrounds, footings:** exactly RF1's (L1, L2a, L2b, L3; OS1 PRIMARY per footing and native N; background
  A graded, B reported; VARIANT reported).
- **Verdict per rule:** **PASS on halo-free baryons (two-scale-length disc)** if any of the 125 cells passes all four lines;
  **FAIL on halo-free baryons (two-scale-length disc)** if none does. Counts per line, best-D cell and the largest v_c(R₀)
  reached are reported either way.
- **Checks.** K1: with R_t = R_T = 1.9333 at Σ_b 47.1 the cell reproduces A1's graded cell (N|canonical|A: v_c(R₀)
  232.0662339084003, K_z(R₀) 68.53649338303407; OS1 canonical PRIMARY 228.90290368882424 / 67.63556402087326) to 1e-9
  relative. K2: every cell's grid mass agrees with its analytic mass to 2e-3. K3: peak RSS < 1 GB, one thread. MUTATE
  (`RF1_MUTATE=1`, separate outputs): q = 0 and S × 0.5 as in RF1; K1 must FAIL and the script exit 1.
- **Expectation on record:** FAIL on every rule. The thick disc holds a minority of the stellar surface density at R₀, so
  shortening it alone cannot supply what the single 1.93 kpc disc did; the A1 lookup shows nothing passing at R_d ≥ 2.6. If
  the run differs, the run stands.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
