# MMU MaNGA scout — adversarial verification

**Date:** 2026-07-16. **Verdict: UPHELD (core), with two framing DOWNGRADES.**
Scripts re-run exit 0 and reproduce bit-for-bit; the data is genuinely real MMU MaNGA;
the honest headline (only 20 galaxies on HF; Test B >> Test A; both a₀ footings; no ΛCDM
verdict; a₀ postulated) stands. Two over-optimistic framing spots need correcting.

---

## 1. REAL data, not synthesized — CONFIRMED

Independent raw read of `train-00008-of-00012.parquet` (bypassing the loader's label filter):
- galaxy `12082-6102`, z=0.04921450838446617, **914 DAP maps**, `stellar_vel` a real
  **96×96 float64** map, 1293 finite spaxels, values −133.49..140.57 km/s, real spatial
  structure (row-40 slice −80.4,−80.4,−80.4,−85.2,…). md5(flux)=`d2c0a3f1cc027538`.
- The documented bytes-repr gotcha is real: raw labels are the literal `b'stellar_vel'`.
- HF is live; all 12 shards cached (~28 GB). **Fallback not needed / not used.** The pilot
  reads genuine MMU rows via `hf_hub_download`+`pyarrow`. **No synthesis anywhere.**

## 2. Scripts re-run — exit 0, reproduce

`pilot_extract.py`, `sampleAB_quantify.py` both exit 0; every number matches the committed
JSON (6/19 canon, 7/19 alt, 19/19 B; pilot A_outer/g_obs identical).

## 3. Test-A deep-MOND coverage — the make-or-break — HONEST count, MIS-STATED caveat, OPTIMISTIC projection

- **The gate is algebraically exact, not an "upper estimate."** I inverted the framework RAR
  g_obs=√(g_bar²+g_bar·a₀): g_obs<√2·a₀ **⇔ g_bar<a₀ exactly**. For 10223-12705,
  g_obs=1.04e-10 → g_bar/a₀=0.72 (canon)/0.55 (alt). So the scout's caveat "g_obs is an upper
  estimate vs a rigorous g_bar" is **mis-attributed** — the two are equivalent *through the RAR*.
  The real slack is **V_c systematics** (deprojection + beam), which the scout lists separately.
  Direction (could be over-counted) is right; the reason given is muddled.
- **The 6/19 (32% canon) count is honest and NOT inflated by fragile geometry.** The [30,75]°
  inclination gate correctly **excludes the near-face-on flagship** (10223-12705, inc=19°). 5 of
  the 6 usable_A galaxies sit at inc 46–72° with g/a₀=0.26–0.85 — comfortably deep-MOND, robust.
- **BUT severe inclination sensitivity** (g_obs/a₀ ∝ 1/sin²i): for the inc≈19° flagship, a ±10°
  error swings g_obs/a₀ from **0.50 to 4.91**. The pilot table (SCOUT §4) presents 10223-12705 as
  the clean "reaches deep-MOND YES" demo — but it is exactly such a fragile near-face-on
  deprojection, and it is a galaxy the scout's **own gate rejects** from usable_A. **DOWNGRADE:
  relabel it; the deep-MOND-reaching demonstrator should be an inc 46–72° galaxy** (e.g. 10223-12703).
- **Beam smearing** suppresses outer-edge V_c → biases the deep-MOND fraction HIGH (unbudgeted). A
  ~2× V_c correction drops 6→~3.
- **Projection optimism.** ~2252 test-A-usable = 10010 × 0.30[PRIOR] × **0.75**(deep-MOND | clean
  disk). The 0.75 is measured on a low-z, low-mass-skewed 8-galaxy slice and carried **un-discounted**
  into the ETG-rich, more-massive full survey (which will run higher-g_bar). **DOWNGRADE: "brackets
  N≈1157" is optimistic.** The qualitative story (A gated, short of N≈6000) survives.

## 4. Anisotropy proxy — does σ constrain radial anisotropy? NO (alone); scout framing OVERSTATED

- **A resolved LOS σ map ALONE does not constrain β=1−σ_t²/σ_r²** — the classic mass–anisotropy
  degeneracy. σ_e and d(lnσ)/d(lnR) are **plain dispersion + its gradient**, conflated with the
  mass profile, **not** anisotropy. σ_maj/min carries *partial* β info only through axisymmetric
  JAM modeling (inclination + mass-model assumptions).
- **The real observable** is β from JAM/Schwarzschild dynamical modeling; a clean break of the
  degeneracy needs **Gauss-Hermite h4**. **CONFIRMED: MMU/manga carries NO h3/h4** (search over all
  914 labels → NONE; only v, σ, σ_corr). So even full modeling off the extracted maps is degenerate
  without re-fitting the `spaxels[]` spectra for h4.
- The scout **does** label these "proxies" needing "full Jeans/JAM" (honest), but the ranking-table
  "**19/19 usable NOW**" / "strong match" **overstates**: the σ maps are a *necessary input*, not a
  delivered discriminator. **DOWNGRADE: reframe as "19/19 have the input σ data; the β inference is
  an unbuilt, degenerate modeling step (no h4 in MMU)."**
- Also, "19/19 usable for B" counts rotation-dominated disks where σ_maj/min conflates **rotation**
  with anisotropy. The discriminator's clean domain (pressure-supported, V_c/σ≲1) is only **~4–5/19**.
  So the ~9000 projection is "~9000 have σ data," not "~9000 clean discriminator targets."

## 5. Sample counts — sanity CONFIRMED

20 parquet rows, 1 bad-z (12082-9101, z=−9999), **19 good** — reproduces. 6/19 canon, 7/19 alt,
19/19 B reproduce. Extrapolation arithmetic checks (10010×0.30×0.75=2252; ×min(1.0,0.9)=9009).
Priors are flagged; the one un-flagged fragility is the 0.75 conditional (see §3).

## 6. HF-access claim — accurate

"HF works; MMU hosts only 20 galaxies, not ~10k" is **correct** — verified live and against the
cached shards. This central honesty point is solid.

---

## Bottom line

**UPHELD.** Real data, reproducible, exit 0; the load-bearing honest claims (20-galaxy slice;
B>>A; both footings; a₀ postulated; no ΛCDM verdict; no test passed) all hold, and the 6/19
test-A count is genuinely honest (inc gate did its job). **Two DOWNGRADES, both framing not fraud:**
(1) the pilot's flagship "reaches deep-MOND" galaxy is a fragile inc=19° deprojection the scout's
own gate rejects — relabel it; the ~2252 / "brackets N≈1157" test-A projection is optimistic
(un-discounted 75% on a low-mass slice + beam bias). (2) Test-B "19/19 usable / strong match"
overstates: σ maps are input, β is degenerate and unmodeled, **no h4 in MMU**, and the clean
pressure-supported discriminator sample is ~4–5/19 not 19/19. No finding flips the ranking (B
remains the better-powered lane) or touches the framework's postulates.
