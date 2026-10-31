# ND1_native_dwarfs: FROZEN CRITERIA (committed alone, before any number from this lane)

**Question.** X80 measured converged η at 10¹⁰ and 10¹¹. With those ratios, version N (no floor) passes SPARC's line. Does it also hold where Υ can't hide it: the gas-rich SPARC galaxies, LITTLE THINGS, the surface-brightness slope? And on the dwarf and lens ceilings, what does the smooth core at native N's S give, and how far does the native cusp, measured in the zooms, really lift it?

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input in any grade. Not "theory closed". Nothing here says the data favour the framework. No downloads. No parameter is fitted or scanned. A failing result is reported as found.

**Id.** `ls` and `git log` show no ND1 lane under `rebuild_2026_10_22`. The only "ND1" in the log is a label inside a `deepseek_push` commit, in a different namespace.

## 0. Seen before freezing (disclosed)
- **On record for native N:** `../NF1_no_floor_rule/nf1_native_read.out`: SPARC Υ 0.70 / 0.72, rms 0.0682 / 0.0694, and Υ, ΔV, S_rule by V_flat. Nothing else on native N for these data has been computed.
- **On record for other rules:** the brief's table (F, N0, N1, N2, law), `nf1_verify.json`, `nf1_bins.json`, `nf1_lt.json`, `hs1_results.json`, `pc1_results.json`, `argon_check.out`, Argon's predictions.
- **Zoom metadata only, no inner mass read:** ε 238 pc at 10¹⁰ and 558 pc at 10¹¹, ε = r_f/100, z_f 1.326 and 1.137, 57,777 particles, X80's per-run c_nfw and η in its JSON. ZN2's low-mass runs to z = 0 had not started when this was written.
- **Exact NFW arithmetic, no zoom and no native N:** the smooth core's own bound is M₃D(<r) ≤ 2.1907 S r² at r/r₀ = 1.027 (g ≤ 0.3487 a₀ at the floor's S). The 1.599 in PC1 and in the brief is Burkert's.
- **Three things in the existing path this lane must handle, found by reading it:**
  1. The rule's halo is the smooth core (X73's `B`, `SHAPE = "S"`), and η is a smooth-core η, but PC1's ceiling and `argon_check.py`'s gain use Burkert's 1.599. So the earlier check's gain, +0.36 to +0.43 dex, compares a cusp with a Burkert bound at a smooth-core S. Against the smooth core's own bound the same exact-NFW numbers give +0.22 to +0.29 dex. The cusp's absolute mass doesn't change; what it is compared with does.
  2. `nf1_verify.py`, `nf1_lt.py` and `hs1_slope.py` use CE1's pre-A4 η. `nf1_native_read.py` uses CE1's A4 η. Native N here means the A4 table. K1 and K2 must use the pre-A4 table to reproduce the record.
  3. `sigma_coll` is not valid below lg M_t = 7.301. Its σ(M) table starts at 10⁷, and below that it silently returns z_f = 0. The ultra-faints' own M200 fall there.

## 1. Native N
S(M200) = f_c η(M_t) 10^T(lg M_t) Σ_coll(M_t), M_t = M200/f_c, f_c = 0.84055.
- η: CE1's A4 medians (25.937, 23.536, 22.096 at lg M_t 12, 13, 14), linear in lg M_t, flat below 12.
- T: linear in lg M_t through (10, lg ρ₁₀), (11, lg ρ₁₁), (12, 0), flat below 10 and above 12. ρ₁₀ = 1.1280903506658675 and ρ₁₁ = 0.9383778261143368 from `x80_converged.json` at a42ae32a01. That's `nf1_native_read.py`'s rule.
- Halo: the smooth core, ρ₀r₀ = S, compact root of `solve_r0`, M200 from EM1's relation on each background.
- **Stated extrapolation:** below lg M_t = 10 no zoom exists. ρ is held at ρ₁₀.
- **Stated clamp:** below lg M_t = 7.301 Σ_coll isn't available, and S is held at its value there. That's generous to a ceiling, since S falls with mass. Cases are counted. SPARC and LITTLE THINGS must not reach it (printed).
- N has no a₀, so it has no footing. Its halo is stated once, and that isn't pooling. Floor rows and the law stay separate by footing.

## 2. Part A: SPARC, both backgrounds
Paths: `nf1_verify.py`'s `stats`, `nf1_bins.py`'s table, `hs1_slope.py`'s statistic, unchanged.
- **Offset:** nf1_verify's log(obs/pred) at Υ 0.50, weighted, on gas ≥ 0.7 (41 galaxies) and gas ≥ 0.5 (81), with gas = 1.33 M_HI/(0.5 L₃.₆ + 1.33 M_HI). Beside it: rms at free Υ and at 0.50, median Υ, fractions at the grid's ends.
- **By V_flat:** nf1_verify's groups (all galaxies in the bin) with the same statistics; and `sel`'s bins (n 13, 35, 23, 25, 18, 10) with median Υ, ΔV over 2–4 R_d at Υ 0.50, S_rule against ET1's interval.
- **SPARC line (EM1's):** rms ≤ 0.110 and median Υ in [0.50, 0.80], on both backgrounds, all 175.
- **HS1 slope:** δ = V_model/V_obs − 1 at 2 R_d, Υ 0.50, on lg SBeff, V_flat 60–120, Q ≤ 2, Inc ≥ 30°. FLAT if |b| ≤ 2σ_b, TILTED otherwise with its sign. Headline on background A, B beside it. The law's FLAT is on record. Stated in the verdict, not part of Argon's lines.
- **Comparators:** F, N0, N1, N2 and the law, from the record on A, recomputed on B and reported.

## 3. Part B: LITTLE THINGS
`nf1_lt.py`'s recipe (RT1's single point at R_max, SED mass, 20 galaxies). Median E, 16–84 %, rms; E and Z for IC 1613, WLM, DDO 210, DDO 216. Negative E is over-predicted. Backgrounds A and B.

## 4. Argon's lines for version N (frozen as stated)
1. SPARC's line on both backgrounds.
2. |offset at Υ 0.50, gas ≥ 0.7| ≤ 0.07, on both backgrounds.
3. |median E on LITTLE THINGS| ≤ 0.10, on both backgrounds.

**Labels:** **ARGON'S LINES PASS** if all three hold. **ARGON'S LINES FAIL: <lines>** otherwise. **[BACKGROUND-DEPENDENT]** appended if a line's outcome differs between A and B. **[NOISE-LIMITED]** appended if a line's outcome holds in fewer than 68 % of §7's draws.

Argon's other line on record: pass window ρ₁₀ 1.15–1.85, fail below 1.10 or above 1.90. ρ₁₀ 1.128 is in neither. Scored as that.

## 5. Part C: ceilings
**Objects and conventions, PC1's, unchanged.** X49's five classes (MW ultra-faint 31, bright M31 25, M31 others 5, MW classical 8, LG field 13), and reported Crater II, Antlia II, Sagittarius. r₁₂ = 4/3 r_h, g_obs = 3σ²/r₁₂, M_b(<r₁₂) = M_b/2, the Arroyo-Polonio correction. E_C = log₁₀(g_obs/(g_N + G C/r₁₂²)). PC1's bootstrap: 10,000 draws on the median, seed 20261026, per class in order. **Draco** is reported by itself, with s from X1. **J0946 dark** at 0.3 and 0.6 kpc: R = (M_obs − 2σ − M_b,max)/C, CFG666's inputs as in PC1. B1938 isn't regraded.

**PC1's classes.** J0946: ALLOWED R ≤ 1, MARGINAL 1 < R ≤ 2, EXCEEDS R > 2. Ultra-faints: NO M200 RESCUES if Z_C > +2, CEILING ADMITS if |Z_C| < 2, BELOW CEILING if Z_C < −2. Draco: above by more than 2 s, or not.

### 5a. C(i): the smooth core at native N's S
- **PRIMARY, free M200:** C_N(r) = the largest M(<r) over lg M200 in [4, 14], grid 0.02 dex, each halo with its own S(M200) and compact r₀. That's PC1's "free, no M200 relation, no stripping", now with S following M200. Background A; B reported. Only this reading can say NO M200 RESCUES.
- **Reported, reference mass lg M200 9** (the brief's and Argon's): the bound 2.1907 S r² with r₀ free, and the mass this halo actually holds at r with its own r₀.
- **Reported beside it:** Burkert's 1.599 at the same S, to compare with the brief's hand numbers; and N1's S at lg M200 9 under both bounds; and the floor's S under the smooth core's bound. PC1's Burkert floor rows are the record.

### 5b. C(ii): the native cusp, measured
**Measurement.** `../ZN1_zooms_to_z0/zn1_measure.py`'s `measure` on each ng 64 run: R200, M200, x_conv = 3ε/R200, ln m(x) on its grid, and `M ∝ r²` inside 3ε. Also n(<3ε), X48's c_nfw over [r_conv, r_vir], and d ln M/d ln r over [3ε, 6ε] against NFW's at that y. Tags 10¹⁰ and 10¹¹ are the lane's; 10¹², 10¹³, 10¹⁴ are read as well, for the rise with mass. Median over seeds of ln M at each radius. Fewer than 6 finished seeds at a tag: UNDECIDED at that tag.

**Snapshots.** z_f (`X48_native_cf_zoom/runs/*/snap_zf.npz`) is graded. z = 0 (`ZN2_native_profile_sparc_groups/runs/M1e1[01]_s*_ng64/snap_z0.00.npz`) is graded the same way only if at least 6 of 9 seeds have finished at both masses when the script runs. If not, the README says so and z_f stands alone. Nothing waits for it.

**Cold mass and mapping.** M_c(<r) = f_c M(<r). At a tag: physical radius, no scaling. Below 10¹⁰, self-similar from the 10¹⁰ tag: M_c(<r; M_t) = f_c (M_t/10¹⁰) M(<r · r_f(10¹⁰)/r_f(M_t)), r_f from `zform` on background A, M_f = M_t/2. This needs no S, and it's what flat η means: M/r² scales as Σ_coll. Between tags: linear in lg M_t, in ln M at fixed r. The zooms are on background A, so the cusp has no B reading.

**Inside 3ε, three readings:**
- **PRIMARY, M ∝ r²** from the measured M(<3ε), ZN1's continuation.
- **Reported, the NFW fit at r:** M_vir m(c r/r_vir)/m(c) with that seed's c_nfw.
- **Reported, the limit** M/r² → 2π ρ_s r_s as r → 0. That's Argon's reading, with the measured ρ_s r_s in place of S.

**[INSIDE 3ε]:** every row says where r lies below 3ε at the mass used (0.03 r_f(M_t)), per system, with a count per class. There the number is a continuation, not a measurement. **[CONTINUATION-DEPENDENT]** if the NFW-fit reading changes a class.

**Why a reference mass.** A cusp's M/r² rises with M200 and has no maximum over M200, so unlike C_N it isn't a ceiling until M200 is stated. **PRIMARY: lg M200 9,** the brief's and Argon's mass. **Reported:** E and R at the tags 10¹⁰ to 10¹⁴; each system's own EM1 M200; and the M200 needed to supply the observed mass, against EM1's relation, on the M_t grid up to 10¹⁴, flagged "not reached" above it. The script prints whether M/r² at fixed r does rise monotonically with mass. If it doesn't, this paragraph's premise is wrong, and the README says so.

**Cusp labels at lg M200 9:** Draco CLEAR if E ≤ 2 s; J0946 CLEAR if R ≤ 2 at both radii; ultra-faints CLEAR unless NO M200 RESCUES. **ALL THREE CLEAR, SOME CLEAR: <names>, NONE CLEAR.** The tag at which J0946 first reaches R ≤ 2, or "none to 10¹⁴", is stated with it.

### 5c. Argon's cusp claim, rechecked
Claim: Draco with a native cusp on N1 is 0.104 dex under the ceiling, and J0946's R 31 falls to 7.9. The R 31 is the floor's, so its basis is the floor's S.
- **Ratio:** ρ_s r_s / S per seed at 10¹⁰, from each run's c_nfw and η_conv (X80's), median. Beside it: exact NFW at c 6, 7.75, 10, 15, 20, and c equivalent to N1's η at lg M200 9.
- **Draco on N1:** E with C = 2π (ratio) S_N1(9) r², by the measured ratio. Beside it: the same at c 15 and at c-equivalent, and the finite-r reading at this halo.
- **J0946:** R at the floor's S with the measured ratio (the score's basis). Beside it: at c 15, at N1's S, at native N's S.
- **Scored:** Draco HIT if within ±0.05 dex of −0.104. J0946 HIT if within ±15 % of 7.9. The earlier check's +0.076 and 12.0 are recomputed and reported as such, with what changed.

## 6. Comparators in the tables
PC1's floor (Burkert) from the record, by footing. Floor's S under the smooth core's bound, by footing. N1's S at lg M200 9, computed. Native N's core and cusp.

## 7. Noise
X80's ratios are [NOISE-LIMITED]. 200 draws, `default_rng(20261031)`: resample X80's nine `per_run` η at 10¹⁰, 10¹¹, 10¹² (`summary` in its JSON), take medians. The rule uses them: η(12) = η₁₂*, η(13), η(14) from the A4 table, T = [lg(η₁₀*/η₁₂*), lg(η₁₁*/η₁₂*), 0]. Per draw: all three of Argon's lines on both backgrounds, gas ≥ 0.5, the HS1 slope on A, the core's C_N (class medians, J0946's R, Draco's E) on A. For the cusp, the same seed indices resample the shape at the 10¹⁰ tag. A class holds if it's the same in at least 68 % of draws; otherwise **[NOISE-LIMITED]**. Reported as 68 % ranges. This propagates a measured error. It is not a scan and tunes nothing.

## 8. Checks. Any K failure: no verdict, exit 1
- **K1:** ρ₁₀ = ρ₁₁ = 1 on CE1's pre-A4 table reproduces N0's record: every group in `nf1_verify.json`, every bin and S_at in `nf1_bins.json`, LG rows and all-20 in `nf1_lt.json`, N0 on both backgrounds in `hs1_results.json`. |d| ≤ 1e-9.
- **K2:** N1's slope (0.0927 per dex) on the same table reproduces N1's record in the same four files. |d| ≤ 1e-9.
- **K3:** native N on the A4 table reproduces `nf1_native_read.json`'s bins (Υ, ΔV, S_rule) to 1e-9. Its grader-path SPARC values are within rms 1e-4 and Υ 0.01. The two paths differ at 2.4e-5 in rms on N0's record, because the grader interpolates c_f and this path interpolates η.
- **K4:** the floor's S with Burkert reproduces `pc1_results.json`: class medians, sd and Z_C, J0946's R, on both footings, |d| ≤ 1e-9. Draco's E_C +0.148 / +0.068 within 0.001.
- **K5:** the zoom path reproduces `x80_converged.json`'s c_nfw and η_conv per run at 10¹⁰ and 10¹¹, |d| ≤ 1e-9. ZN1's inherited K2 (sampled NFW c 4) passes. `rf_phys` in the metadata equals `zform`'s r_f to 1e-3.
- **K6:** the free-M200 path with the floor's S and Burkert returns 1.599 S r² at J0946's radii and Draco's r₁₂ to 1e-3.
- **K7:** exact NFW reproduces `argon_check.out`'s η, ρ_s r_s, ratio and gain over 1.599 at the five c values, as printed there, to 5e-3.
- **MUTATE** (`--mutate`, separate outputs): S × 0.5 and the shape's r × 1.5. It must raise median Υ on both backgrounds, raise the gas ≥ 0.7 offset and LITTLE THINGS' median E by at least 0.02, halve the reference-mass bound exactly, raise the ultra-faints' Z_C on C_N, and raise the cusp's E by at least 0.02 dex in the median. If it doesn't bite: no verdict, exit 1.
- **Side effects:** no file outside this lane may change. `LS1_lstar_analogs`' loader writes its X74 by-products beside `__file__`, so this lane points `__file__` here and removes them. Bytecode writing is off, since X77's prefix imports from `X48_native_cf_zoom`.

## 9. My expectation, by hand from the record (not computed, and not a result)
Native N sits between N0 and N1 below 10¹¹, nearer N0. So gas ≥ 0.7 offset near 0, inside Argon's line, and LITTLE THINGS median E near +0.13, a narrow fail, possibly noise-limited given ρ₁₀'s range. HS1 slope near −0.18, TILTED −. Core: S at lg M200 9 near 29 against N1's 48.6, so Draco and J0946 worse than N1's, ultra-faints NO M200 RESCUES on C_N. Cusp at lg M200 9: Draco around +0.3 dex, J0946 EXCEEDS, ultra-faints admitted but almost all inside 3ε. Argon's −0.104 and 7.9: MISS. Scored in the README.

## 10. What this can't show
- It doesn't measure anything below 10¹⁰. ρ and the shape are extrapolated there, and every dwarf's own EM1 M200 is far below it.
- The zooms don't resolve the radii that matter. 3ε is 714 pc at 10¹⁰ and 1.67 kpc at 10¹¹, and most half-light radii lie below 0.03 r_f at any mass that holds enough mass. The inner profile there is assumed.
- The zooms are Newtonian and collisionless, with no baryons, stripping or heating. Stripping and heating lower inner mass, so ceilings stay upper bounds for them. Contraction would raise them (LC1).
- z_f snapshots stop before late growth. ZN1 found little change at 0.1–0.5 r_f by z = 0 at 10¹³–10¹⁴, not yet shown at low mass.
- Lens masses depend on assumed profiles, and perturbers may be line-of-sight objects. Dwarf kinematics assume equilibrium.
- A pass on Argon's lines wouldn't explain the RAR's tightness, and a₀ out of the cold sector stays the owner's call.
