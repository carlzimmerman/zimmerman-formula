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

**A3 result, 2026-10-31 (run eaec677e99; `rf1_a3_two_rd.out`, `rf1_a3_two_rd_results.json`, MUTATE twins).** Against the
expectation on record. K1 reproduces A1's cell to 1e-10, K2 1.9e-6, K3 0.38 GB; MUTATE fails K1 and exits 1. Runtime 8 s.

| rule (bg A, PRIMARY) | verdict as frozen | cells / 125 | where |
|---|---|---|---|
| OS1 canonical | **PASS on halo-free baryons (two-scale-length disc)** | 1 | Σ_b 50.5, R_t 2.38, R_T 1.6 |
| OS1 alt | **PASS** | 5 | Σ_b 50.5–53.9, R_t 2.38–2.90, R_T 1.6 (four) and 1.8 (one, at Σ_b 53.9) |
| Native N | **PASS** | 5 | Σ_b 47.1–53.9, R_t 2.38–2.64, R_T 1.6 (four) and 1.8 (one, at Σ_b 53.9) |

Reported: VARIANT V_last 229 passes 14–20 cells; background B agrees for OS1 and drops native N to 2 cells. No cell passes with
R_T ≥ 2.0 on any PRIMARY rule, and none with R_t ≥ 2.77 on canonical OS1 or N.

**Reading, as hard as a fail would get.** The pass exists, but it lives at a corner of the halo-free priors: the thick disc at
its −2σ edge (1.6 against 2.0 ± 0.2), the thin disc at or near LN16's −2σ edge (2.38–2.51 against 2.64 ± 0.13), and Σ_b at +1σ
to +2σ (50.5–53.9 against 47.1 ± 3.4). Canonical OS1 needs all three at once in one cell. In GD2's language this is FEASIBLE
on wide priors, not FEASIBLE IN PRIORS, and the frozen A3 line did not distinguish the two, so the verdict word is PASS and
this paragraph is the qualifier. The thick-disc share at R₀ is McMillan's (f_thin 0.7367), held and labelled; a halo-free
thick-disc fraction is the next open input, and it moves this result directly because the pass is carried by the thick
component's short scale length. The Milky Way on halo-free baryons under route E therefore reads: **not excluded; passes only
where every halo-free prior is pushed about 2σ the same way.** GD1's McMillan verdict keeps its label.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

**A4, 2026-10-31, FROZEN before any number from it.** The thick-disc share at R₀, which A3 held at McMillan's and which
carried A3's pass, replaced by the star-count value. BH&G16 §5.1.3 (on disk, A2): thick-to-thin local column ratio
**f_Σ = 12 % ± 4 %** from f_ρ = 4 % ± 2 % and the scale heights, "excludes all papers that do not" separate the components by
star counts; halo-free. McMillan's share corresponds to f_Σ = 0.357 (thick 26.3 % of the stellar column); the star-count
value gives thick 10.7 % (7.4–13.8 % at ±1σ).

- **Grid:** A3's 125 cells (Σ_b McKee, R_t 2.38–2.90, R_T 1.6–2.4, M_bb 2.0 × 10¹⁰, McKee gas) × f_Σ ∈ {0.04, 0.08, 0.12,
  0.16, 0.20} (±2σ in 1σ steps): 625 cells. Thin share of the stellar column at R₀ = 1/(1 + f_Σ). Everything else as A3.
  Separate script `rf1_a4_thick_share.py`; A3's outputs untouched.
- **Verdict per rule (bg A, PRIMARY), as A3:** PASS on halo-free baryons (two-scale-length disc, star-count thick share) if any
  of the 625 cells passes all four lines; FAIL if none does. Reported beside it: the count at f_Σ = 0.12 alone and within ±1σ
  (0.08–0.16), so a pass that exists only at f_Σ = 0.20 is visible as such.
- **Checks.** K1: with f_Σ set to McMillan's 0.3574 (f_thin 0.7367) the script reproduces A3's recorded best cell for
  OS1|canonical|PRIMARY|A and N|canonical|A (read from `rf1_a3_two_rd_results.json`, not typed) to 1e-9 relative. K2: grid
  mass vs analytic 2e-3 on every cell. K3: RSS < 1 GB. MUTATE as A3 (q = 0, S × 0.5): K1 must FAIL, exit 1.
- **Expectation on record:** FAIL on every rule at f_Σ ≤ 0.16; a pass, if any, only at f_Σ = 0.20 with R_T 1.6 and Σ_b high,
  because A3's pass was carried by the short thick disc at 26 % of the column. If the run differs, the run stands.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
