# MMU MaNGA feasibility SCOUT + PILOT

**Date:** 2026-07-16. **Framework:** Carl Zimmerman's de Sitter–Unruh **MODIFIED INERTIA**
(own interpolation ν(y)=√(1+1/y), horizon-derived a₀=cH_Λ/Z). Both a₀ footings carried:
**canonical a₀=9.36×10⁻¹¹** (cH_Λ/Z, ρ_DE) and **alt a₀=1.13×10⁻¹⁰** (cH₀, ρ_tot). This is a
**data-feasibility scout**, not a physics test; no numerology; the frozen `zimmerman-formula`
repo was read-only. All work in `prep_2026/mmu_scout/`. Scripts exit 0, numbers computed from data.

---

## 0. HEADLINE (report straight, per honesty rails)

1. **HF access WORKS** here — `MultimodalUniverse/manga` loads via `huggingface_hub`.
2. **BUT the MMU-hosted MaNGA is only 20 galaxies, NOT ~10k.** The HF dataset is 12 parquet
   shards / 4.2 GB holding **1–2 galaxies each = 20 total** (one with bad z=−9999 → 19 usable).
   The full ~10,010-galaxy MaNGA is **not** on HF; obtaining it means running MMU's own build
   pipeline against the SDSS DR17 archive. Every "usable N" below has two numbers: the **real
   count out of 19** and a **clearly-flagged projection** to the full survey.
3. **Every DAP map the two tests need is present and populated** (stellar_vel, stellar_sigma,
   stellar_sigmacorr, Hα gas velocity/σ) with per-spaxel ivar, plus DAP-precomputed deprojected
   geometry (`spx_ellcoo`). No external NSA needed for geometry — validated below.
4. **MaNGA is far stronger for TEST B (anisotropy) than TEST A (deep-MOND rotation).**
   Test B: **19/19 (100%)** usable, no coverage gate. Test A: **6/19 (32%) canonical / 7/19 (37%)
   alt** are inclined rotating disks whose *outer optical spaxels* reach the low-acceleration
   regime — usable **in principle**, but gated hard by the 20-galaxy hosting and by two things
   MMU does **not** carry (g_ext direction; a baryonic g_bar model).

---

## 1. ACCESS + SCHEMA (`mmu_access.py`, live)

`HfApi.list_repo_files` + `pyarrow` footer reads. Per-galaxy schema (7 top-level fields):

| field | content |
|---|---|
| `object_id` | plate-IFU string, e.g. `12082-6102` (cross-matches to NSA/DRPall externally) |
| `z` | DRP redshift (float; one galaxy = −9999 sentinel) |
| `spaxel_size` | 0.5 arcsec (all) |
| `spaxels[]` | per-spaxel spectra **+ deprojected coords** (skycoo, ellcoo r/re/kpc/azimuth) |
| `images[]` | reconstructed **griz** images (raw material for a baryonic mass model) |
| `maps[]` | **the full DAP MAPS datamodel** — 39 groups, ~250 labelled 2-D maps, each flux+ivar+mask |

**Gotcha (documented for reuse):** `maps[].group` and `.label` are stored as the *repr of a
bytes object* — the literal string `b'stellar_vel'` (quotes + leading `b` included).
`_mmu.clean()` normalises it. Missed silently → zero matches.

**Kinematic maps present + populated** (galaxy 12082-6102, 1293 valid spaxels each):
`stellar_vel` (−133..141 km/s, ivar), `stellar_sigma` (29..159 km/s, ivar),
`stellar_sigmacorr_fit` (instrumental, for quadrature correction), `emline_gvel_ha_6564`
(−151..170 km/s, ivar), `emline_gsigma_ha_6564` (ivar). **Geometry** from `spx_ellcoo`:
elliptical_radius (arcsec), **r/re**, **r_h/kpc**, elliptical_azimuth (deg); weight `spx_mflux`.

**No NSA metadata columns** (elpetro_th50/ba/sersic_mass/objra/dec) are stored. Geometry
(Re, inclination, PA) is **recovered from the DAP maps themselves** — validated:
- `R_sky/R_ell → 0.996` near the major axis and `→ q=b/a` near the minor axis (12082-6102:
  q=0.907); axis-ratio fit `(R_sky/R_ell)² = 1−(1−q²)sin²φ` reproduces it (0.905).
- `corr(v−v_sys, cos(azimuth)) = −0.94` → the DAP azimuth is on-sky from the major axis and
  the kinematic axis aligns with the photometric one. So `cos(azimuth)` is the per-side wedge
  cosine the WALLABY `perside_extractor` wants, for free.

---

## 2. SAMPLE A — deep-MOND directional-EFE rotation (`sampleAB_quantify.py`)

**Test A needs** per-side outer rotation curves in the deep-MOND regime (g_bar<a₀). Gate on the
framework's **own** RAR g_obs=√(g_bar²+g_bar·a₀): g_bar<a₀ ⇔ **g_obs < √2·a₀**. g_obs=V_c²/r is
measured directly (deprojected V_c from the stellar_vel field, physical r from `spx_ellcoo r_h/kpc`).

**Usability = (resolved stellar_vel) ∧ (inc 30–75°) ∧ (rotation-dominated V_c/σ_e>1) ∧ (outer g_obs<√2·a₀).**

Census over **19 good-z galaxies** (both footings):

| flag | count | frac |
|---|---|---|
| resolved stellar_vel | 16/19 | 84% |
| inclination 30–75° | 11/19 | 58% |
| rotation-dominated (V_c/σ_e>1) | 14/19 | 74% |
| **test-A-ready clean disk** (vel∧inc∧rot) | **8/19** | **42%** |
| of which reach deep-MOND, **canon** | 6/19 | 32% |
| of which reach deep-MOND, **alt** | 7/19 | 37% |
| **USABLE for TEST A (canon / alt)** | **6 / 7 of 19** | **32% / 37%** |

**Projection to full ~10k MaNGA** (order-of-magnitude; priors flagged): rotation-disk×inclination
window ~30% [PRIOR, MaNGA is ETG-rich] → ~3000 clean-disk rotators; deep-MOND-reaching fraction
(measured, small-N) → **~2000–3000 test-A-usable**. That **brackets the N≈1157 canonical target**
but falls **short of the N≈6000 AQUAL-vs-BranchB target**.

**Honesty caveats (do NOT overclaim MaNGA reaches deep-MOND):**
- The gate uses **g_obs (observed)**, not **g_bar (baryonic)**. It flags the *low-acceleration
  outskirts*; a rigorous g_bar<a₀ needs a stars+gas mass model (derivable from the in-parquet
  **griz** images + M/L, or external photometry) — **not done in this scout**. So "32% reach
  deep-MOND" is an **upper estimate**.
- Many MMU galaxies are near-face-on (inc<30°) or pressure-supported — correctly excluded; this
  is *why* the clean-disk fraction is only 42%.
- **The directional test needs the g_ext vector** (amplitude+direction from 2M++/`gext_vectors_2026`),
  which MMU does **not** carry. The gext estimator generalises to any RA/Dec/D, so this is
  add-on work, not a wall — but it is required before any A-value becomes a physics test.
- Outer-ring V_c at the low-S/N optical edge carries beam/asymmetric-drift systematics not
  budgeted here.

---

## 3. SAMPLE B — MG-impossible anisotropy discriminator (`sampleAB_quantify.py`)

**Test B needs** resolved stellar-σ maps + a radial-anisotropy proxy (spec:
`mi_closure_pin/CONSEQUENCES.md` §1 — d(offset)/d(radial-anisotropy) **> 0**; MG-with-same-ν gives
**exactly 0** for isolated spherical systems → MG-impossible). **No deep-MOND coverage gate.**

**Result: 19/19 (100%)** have resolved `stellar_sigma` with ≥100 valid spaxels (all have 1200–1900).
Projection to full survey: **~9000 usable** — ample. **MaNGA is a strong match for test B**, exactly
as anticipated: early-types/bulges qualify directly and the σ maps are clean and instrument-corrected.

The pilot extracts the pieces a full Jeans/JAM β proxy is built from: σ_e (within 1 Re), V/σ,
a major-vs-minor LOS-σ ratio, and the d(lnσ)/d(lnR) slope. These are **proxies** — the full test
needs Jeans/Schwarzschild anisotropy modelling — but every input extracts cleanly on real data.

---

## 4. PILOT — real MMU galaxies (`pilot_extract.py`, N=3 explicit + 19 in the census)

Proof the pipelines run on genuine MMU DAP maps (values are proof-of-life; feed no physics claim):

| galaxy | z | inc | Test A: A_outer, g_obs/a₀ (c/a), deep-MOND? | Test B: σ_e, V/σ, σ_maj/min, dlnσ/dlnR |
|---|---|---|---|---|
| 10223-12705 | 0.042 | 19° | A=+0.308, g/a₀=1.11 / 0.92 → **canon YES, alt YES** | 43.8, 0.67, 0.890, +0.32 |
| 12082-6102 | 0.049 | 25° | A=+0.034, g/a₀=4.81 / 3.98 → **NO** (massive, stays Newtonian at 2.4 Re) | 102.1, 0.61, 0.930, −0.61 |
| 10223-12704 | 0.021 | 18° | face-on → V_c unreliable, correctly **rejected** for A | 101.0 (σ extracts fine) |

The contrast is the physics: the **massive** galaxy (12082-6102) sits at ~5 a₀ at its optical edge —
MaNGA optical does **not** reach deep-MOND for massive systems; the **lower-mass** rotator
(10223-12705) reaches g_obs≈a₀ at its edge. This is the test-A feasibility story in one line.

---

## 5. DESI-in-MMU confirmation (`desi_confirm.py`, live)

For the cluster relational-σ-spread test (`sigma_spread/`, the clean MG-impossible discriminator:
MI 6–13%, MG exactly 0): **MMU/desi exposes member redshifts** — `Z`, `ZERR`, `ZWARN` in the main
`edr_sv3` config (object_id=TARGETID, coords via cross-match) and **`ra`/`dec` + `Z_HP`/`Z_MW`
directly in `desi_provabgs`**. Usable for cluster-member LOS velocities. **CAVEAT:** it is the DESI
**EDR/SV3 + PROVABGS subset (~100k + ~100k rows), not the full ~20M**; SV3 rosette fields are not
cluster-targeted, so per-cluster member counts remain the binding limit (already underpowered per
`sigma_spread/POWER.md`).

---

## 6. RANKING — what MMU can genuinely power for the framework

| test | MMU-as-hosted (20 gal) | full MaNGA projection | verdict |
|---|---|---|---|
| **B — anisotropy discriminator** | **19/19 usable NOW** | ~9000 | **STRONGEST.** No coverage gate, MG-impossible, σ maps clean. MaNGA is the natural home. |
| **A — deep-MOND directional-EFE** | 6–7/19 reach low-g outskirts | ~2000–3000 (brackets N≈1157, short of N≈6000) | **USABLE IN PRINCIPLE**, three caveats: only 20 on HF; g_ext direction not in MMU; g_obs≠g_bar (needs a mass model). |
| cluster σ-spread (DESI) | Z/coords present, subset only | needs full DESI + cluster targeting | secondary; confirmed accessible, still underpowered. |

**Bottom line, straight:** MMU MaNGA on HF is a **20-galaxy demonstration slice**, not the ~10k
survey — the single most important thing to know before planning around it. On its own terms it
**genuinely powers Test B** (resolved σ, MG-impossible, 100% usable) and the pipeline is proven on
real data. **Test A is reachable but not by MMU-as-hosted alone**: ~1/3 of inclined MaNGA disks
have outer optical spaxels in the low-acceleration regime (an *upper* estimate at the g_obs level),
which would clear the N≈1157 canonical target only after (i) building the full ~10k via MMU's
pipeline, (ii) attaching g_ext vectors, and (iii) upgrading the g_obs gate to a photometric g_bar.
Both footings tracked throughout; a₀'s value and sign remain postulates; no ΛCDM verdict claimed;
no test "passed" — this is feasibility only.

**Files (all `prep_2026/mmu_scout/`, exit 0):** `_mmu.py` (loader), `mmu_access.py` (schema+census),
`sampleAB_quantify.py` (→`sampleAB_results.json`), `pilot_extract.py` (→`pilot_results.json`),
`desi_confirm.py`. Templates reused read-only: `wallaby_prep/perside_extractor.py`,
`gext_vectors_2026/src/gext_estimator.py`, `mi_closure_pin/CONSEQUENCES.md`, `mi_eta_selection/SYNTHESIS.md`.
