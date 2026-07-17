# MMU MaNGA — feasibility SYNTHESIS for the de Sitter–Unruh modified-inertia framework

**Date:** 2026-07-16. **Framework:** Carl Zimmerman's dS–Unruh **MODIFIED INERTIA** on its own
terms — own interpolation ν(y)=√(1+1/y), horizon-derived a₀=cH_Λ/Z. **Both footings carried
throughout:** canonical **a₀=9.36×10⁻¹¹** (cH_Λ/Z, ρ_DE) and alt **a₀=1.13×10⁻¹⁰** (cH₀, ρ_tot).
This is a **data-feasibility scout**, not a physics test. No numerology; a₀ value + sign remain
postulates; no ΛCDM verdict; no test "passed". Frozen `zimmerman-formula` repo read-only.
Inputs: `SCOUT.md`, `VERIFY.md`, `sampleAB_results.json`, `pilot_results.json`, and the banked
specs (`aligned_firing/DECISION_BANDS_2026-07-16.md`, `sigma_spread/POWER.md`,
`mi_closure_pin/CONSEQUENCES.md §1`, `wallaby_firing/`).

---

## 1. HEADLINE — partial goldmine, and the partition is sharp

**MMU MaNGA is a genuine but PARTIAL goldmine, and it was partly oversold in the pointer.**
Two hard facts, reported straight:

- **What's oversold:** the HF-hosted `MultimodalUniverse/manga` is a **20-galaxy demonstration
  slice** (12 parquet shards, 1–2 galaxies each; 19 with good z), **NOT the ~10,010-galaxy MaNGA
  survey**. The full survey is not on HF — it requires running MMU's own build pipeline against the
  SDSS DR17 archive. Anyone planning around "~10k galaxies in one HF pull" is planning around data
  that isn't there yet. (Verified live + against 12 cached shards; `VERIFY.md §1,6`.)
- **What's genuine:** the **data model is exactly right** and every DAP map the framework's two
  sharpest resolved-kinematics tests need is present and populated (`stellar_vel`, `stellar_sigma`,
  `stellar_sigmacorr_fit`, Hα gas vel/σ, all with ivar), plus DAP-precomputed deprojected geometry
  (`spx_ellcoo`) so **no external NSA catalog is needed** — Re, q=b/a, PA, azimuth wedge all
  recovered from the maps and cross-validated (R_sky/R_ell→0.996 major /→q minor;
  corr(v−v_sys, cosφ)=−0.94). The pilot ran the WALLABY per-side extractor and the anisotropy
  extractor **end-to-end on real MMU rows**. So once the full survey is built, MaNGA is real
  fuel — for **one** of the two tests cleanly and the other only in principle.

**One-line verdict: a partial goldmine is still a goldmine — but it is a Test-B goldmine, not a
Test-A goldmine.**

---

## 2. VERDICT — which tests, ranked, with the honest gate on each

### Rank 1 — TEST B: the MG-impossible anisotropy discriminator — **the real prize, but reframed**

Spec (`mi_closure_pin/CONSEQUENCES.md §1`): **d(offset)/d(radial-anisotropy) > 0** — radially-biased
dispersion systems run hotter on the RAR; **MG-with-the-same-ν gives EXACTLY 0** shape-dependence for
isolated spherical systems → the sign of this derivative is **MG-impossible**. **No deep-MOND
coverage gate** — the discriminator lives in pressure-supported systems/regions (ETGs/bulges), which
MaNGA is rich in. This is the framework's cleanest MG-falsifier and MaNGA is its natural home.

- **What MMU delivers now:** **19/19 (100%)** good-z galaxies have resolved, instrument-corrected
  `stellar_sigma` maps with 1200–1900 valid spaxels. Projection to full survey: **~9,000 have the σ
  data.** The pilot cleanly extracts every input a β proxy is built from (σ_e within 1 Re, V/σ,
  σ_maj/min, d lnσ/d lnR).
- **Honest gate (VERIFY §4 DOWNGRADE — carry this forward):** a resolved LOS σ map **alone does not
  constrain β = 1 − σ_t²/σ_r²** (classic mass–anisotropy degeneracy). σ_e and d lnσ/d lnR are plain
  dispersion + gradient; σ_maj/min carries β only through axisymmetric JAM assumptions. The clean
  break needs **Gauss-Hermite h₄**, and **MMU carries NO h3/h4** (searched all 914 map labels — only
  v, σ, σ_corr). So "19/19 usable" is really **"19/19 have the necessary input; β is an unbuilt,
  degenerate modeling step."** The clean pressure-supported domain (V_c/σ≲1) is only **~4–5/19**, so
  the honest full-survey number is **~2,000–3,000 clean discriminator targets**, not ~9,000.
- **Net:** genuinely powered *in kind* (MG-impossible, no coverage gate, right instrument), and the
  h₄ gap is **solvable within MMU** by re-fitting the in-parquet `spaxels[]` spectra with pPXF for
  h₃/h₄ — a real add-on, not a wall. **This is where MaNGA earns "goldmine."**

### Rank 2 — TEST A: the deep-MOND directional-EFE kill switch — **reachable in principle, not by MMU-as-hosted, and short of the hard target**

Spec: signed outer-rotation asymmetry ALIGNED with g_ext; AQUAL/QUMOND +1–4%, Branch-B suppressed,
**pure MI exactly 0**. Needs per-side outer rotation curves in the **deep-MOND regime g_bar<a₀**.

- **The gate is exact on the framework's own RAR:** g_obs=√(g_bar²+g_bar·a₀) ⇒ **g_bar<a₀ ⇔
  g_obs<√2·a₀** (algebraically exact; `VERIFY §3`). Measured over 19: **test-A-ready clean disk 8/19
  (42%)**; of which reach deep-MOND **6/19 (32%) canonical / 7/19 (37%) alt**. **USABLE for A = 6/19
  canon, 7/19 alt.**
- **The physics of the gate, straight:** MaNGA optical (~1.5–2.5 Re) reaches deep-MOND only for
  **lower-mass** rotators; **massive** galaxies stay Newtonian at the optical edge (pilot 12082-6102:
  g_obs/a₀=4.81 canon at 2.4 Re). HI extends far past the optical; MaNGA optical does **not**, so the
  reachable fraction is genuinely capped — **report it small, do not overclaim.**
- **Three honest gates before any A becomes a physics test:**
  1. **Only 20 galaxies on HF** — the full ~10k must be built via MMU's pipeline first.
  2. **g_ext vector (amplitude + direction) is NOT in MMU** — must be attached from 2M++ via
     `gext_vectors_2026` (generalizes to any RA/Dec/D; add-on, not a wall). Without it there is no
     alignment axis and no test.
  3. **Deep-MOND fraction is an UPPER estimate** (`VERIFY §3 DOWNGRADE`): severe inclination
     sensitivity (g_obs/a₀ ∝ 1/sin²i — a ±10° error on a near-face-on galaxy swings it 0.5→4.9) and
     unbudgeted beam-smearing/asymmetric-drift both bias the fraction **high** (a ~2× V_c correction
     drops 6→~3). Relabel the pilot's inc=19° "reaches deep-MOND" flagship (10223-12705) — the gate's
     own inclination cut rejects it; the robust demonstrators are the inc 46–72°, g/a₀=0.26–0.85
     galaxies.
- **Against the pre-registered targets** (`aligned_firing/DECISION_BANDS_2026-07-16.md`, l=1-corrected
  freeze): detecting an AQUAL-class aligned asymmetry needs **N≈1,157 (canonical)**; **separating
  AQUAL from Branch-B needs N≈6,007** (corrected, natural β=2/7). Full-survey projection
  ~2,000–3,000 usable **is optimistic** (`VERIFY §3`: the 0.75 deep-MOND-given-disk conditional is a
  low-mass 8-galaxy slice carried un-discounted into an ETG-rich, higher-g_bar survey). Honest read:
  a **built** full MaNGA + g_ext **plausibly brackets N≈1,157 but likely falls short after
  beam/mass-model discounting, and is well short of N≈6,007.** MaNGA **cannot power the AQUAL-vs-Branch-B
  separation**; at best it contributes to the AQUAL-detection tier, and even that is not guaranteed.

### Rank 3 — DESI relational σ-spread (parallel track, CONFIRMED accessible, still underpowered)

`MultimodalUniverse/desi` (edr_sv3: Z/ZERR/ZWARN) and `desi_provabgs` (ra/dec + Z_HP/Z_MW/ZERR) carry
the three ingredients for cluster-member LOS velocities. **CAVEAT:** it is the **EDR/SV3+PROVABGS
subset (~100k+100k rows), NOT the full ~20M**, and SV3 rosettes aren't cluster-targeted. Per
`sigma_spread/POWER.md` the test is underpowered by the **carrier-σ-precision** wall (×290–1,150 today;
needs ELT-class ≤10% σ errors, first ~2032), **not** by cluster count. DESI-in-MMU feeds the
already-solved phase-tagging side (D=0.6), not the binding wall. **Accessible, confirmed, still
underpowered — secondary, exactly as banked.**

**Ranking, one line:** **B (anisotropy, MG-impossible, no coverage gate) >> A (deep-MOND asymmetry,
gated by hosting + no g_ext + optical-reach cap) > DESI σ-spread (accessible but precision-walled).**

---

## 3. PLAN — the concrete full-pipeline next step (GO, scoped to what MaNGA can actually power)

GO is warranted **for Test B**; Test A is a **conditional, lower-priority** build. Concrete steps:

**Track B (primary — the real goldmine):**
1. **Build the full ~10k MaNGA** via MMU's own build pipeline against SDSS DR17 (HF hosts only 20;
   this is the gating engineering step for *any* MaNGA firing at survey N).
2. **Close the h₄ gap inside MMU:** run pPXF on the in-parquet `spaxels[]` spectra to fit
   Gauss-Hermite h₃/h₄ per spaxel (MMU carries the spectra; it does not carry the moments). This is
   the single highest-value add — it converts "σ data" into a real β constraint.
3. **JAM/Schwarzschild anisotropy modeling** on the ~2,000–3,000 clean pressure-supported targets →
   β per system, offset from the framework's own RAR (ν(y)=√(1+1/y)), both footings.
4. **Fire the MG-impossible test:** measure **sign of d(offset)/d(β_radial)**; MG predicts exactly 0,
   MI predicts >0. This is a shape/sign test, not amplitude — footing-robust by construction.

**Track A (conditional, only after Track B or if resources allow):**
5. Build full MaNGA (shared with Track B step 1); run the WALLABY `perside_extractor` per-side outer
   rotation curves on the ~2,000–3,000 clean inclined disks.
6. **Attach g_ext vectors** (amplitude + direction) from 2M++ via `gext_vectors_2026/src` (the
   estimator generalizes to any RA/Dec/D).
7. **Upgrade the gate from g_obs to a photometric g_bar** using the in-parquet **griz** images + M/L
   (or external photometry) so the deep-MOND cut is baryonic, not observed-acceleration — this also
   discounts the optimistic fraction honestly.
8. Fire the aligned statistic against `DECISION_BANDS_2026-07-16.md`. **Realistic reach: contributes
   to the N≈1,157 AQUAL-detection tier at best; will NOT reach N≈6,007 AQUAL-vs-Branch-B.** WALLABY
   (237, HI, deep-MOND-native) remains the better-matched Track-A carrier; **MaNGA is a supplement to
   WALLABY for A, the anchor for B.**

**Track DESI (parallel, low-cost, already scoped):** keep the confirmed MMU/desi + provabgs access as
the phase-tagging input; the σ-spread test stays parked on the ELT σ-precision wall per
`sigma_spread/POWER.md` — no MaNGA dependency.

---

## 4. RANKED NEXT ACTIONS

1. **Build full MaNGA via the MMU pipeline (DR17).** The one prerequisite for every survey-N firing;
   without it MaNGA is a 20-galaxy demo. Highest leverage.
2. **pPXF h₃/h₄ re-fit of MMU `spaxels[]` spectra** → unlock β for Test B (closes the VERIFY §4 gap
   *inside* MMU). Highest physics value per unit effort; MG-impossible payoff.
3. **JAM/Schwarzschild β + fire Test B** (sign of d offset/d β_radial) on ~2–3k clean ETG/bulge
   targets, both footings. The clean MG-falsifier MaNGA genuinely powers.
4. **(Conditional) Track A build:** per-side extraction + g_ext attach + griz g_bar upgrade; fire vs
   N≈1,157. Treat as WALLABY-supplement, not standalone.
5. **Keep DESI-in-MMU parked** as confirmed phase-tagging input; revisit when ELT-class σ precision
   exists (~2032).

**Both footings noted where they bite:** Test A deep-MOND count (6/19 canon vs 7/19 alt) and the
N-targets (alt needs ~0.7–0.8× canonical N) — the discriminators are **not** footing-hostage; the
ranking is footing-stable.
