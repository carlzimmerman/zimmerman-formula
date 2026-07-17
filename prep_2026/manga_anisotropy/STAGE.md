# STAGE — MaNGA DR17 Stage-1 staging for the MG-impossible anisotropy discriminator

**Date:** 2026-07-17 (UTC). **Framework:** Carl Zimmerman's de Sitter–Unruh **MODIFIED INERTIA**,
judged on its own terms (own ν(y)=√(1+1/y)); **both footings everywhere** — canonical
a₀=9.36e-11 (cH_Λ/Z, ρ_DE), alt a₀=1.13e-10 (cH₀, ρ_tot). Target observable (forced,
η-independent in sign, derived 2026-07-16, never tested by anyone):
**d(offset)/d(radial-anisotropy) > 0** (MI) vs **exactly 0** (MG-with-same-ν) —
`mi_closure_pin/CONSEQUENCES.md` §1 A-2, `mi_eta_selection/SYNTHESIS.md` §2/§4.1.

**This lane is STAGING ONLY.** Cuts/estimator/proxies/regression-spec were **frozen at
2026-07-17T00:21:52Z, before any download** (`FROZEN.md`). The δ-vs-proxy regression was
deliberately **NOT run** (freeze-then-fire separation; exploratory firewall — no kill
conditions exist for this observable yet; this run creates the baseline and pre-registers
the full-Jeans Stage 2). The frozen zimmerman-formula repo was read-only throughout.

---

## 1. Data in hand (all validated, exit-0 drivers)

| file | source | size | validation |
|---|---|---|---|
| `data/dapall-v3_1_1-3.1.0.fits` | SDSS DR17 SAS | 146,030,400 B | HDU `HYB10-MILESHC-MASTARSSP` present, **10,782 rows**; all needed columns present |
| `data/drpall-v3_1_1.fits` | SDSS DR17 SAS | 75,360,960 B | HDU `MANGA`, **11,273 rows**; all NSA columns present |
| `data/maps/*.fits.gz` (48 files) | DR17 DAP HYB10-MILESHC-MASTARSSP | 116 MB total | 48/48 downloaded, 48/48 open + extract cleanly |

PLATEIFU crossmatch: **10,782/10,782 DAP rows matched** to drpall. Note: `prep_2026/` sits
**outside any git repo** (`~/new_physics` has no `.git`), so the big FITS files carry no
commit risk; nothing was added to the frozen repo.

## 2. The frozen cut cascade → Stage-1 catalog (`stage1_catalog.py` → `stage_catalog.csv`)

| gate (frozen order) | survivors |
|---|---|
| DAP×DRP matched | 10,782 |
| DAPDONE | 10,735 |
| DAPQUAL==0 | 9,027 |
| mngtarg1>0 (main sample) | 8,771 |
| NSA mass/R_e/z window | 8,766 |
| SNR_MED(g) ≥ 10 | 3,159 |
| σ_1Re ≥ 70 km/s (LSF floor) | 2,442 |
| MANGAID dedupe | **2,407 parent** |
| **(V/σ)_glob < 0.4 — PRIMARY pressure-supported** | **382** |
| (V/σ)_glob < 0.6 — VARIANT | 671 |

This lands inside the "hundreds-to-~2000 slow rotators" expectation. The two hungriest
gates are frozen quality guards: the g-band S/N≥10 cut and the 70 km/s dispersion floor
(the floor is what keeps the σ_e-based δ meaningful; stated cost: mass bias, revisit in
Stage 2).

`stage_catalog.csv` = 671 rows (VARIANT superset; `cut_primary` flags the 382), with per
galaxy: σ_e, (V/σ)_glob, log M*, log M_dyn (K_v=5.0), R_e(kpc), b/a, Sérsic n, z, SNR, and
the frozen offset **δ = log10(M_dyn) − log10(ν(y)·M_bar)** at **both footings × three IMF
brackets** (baseline NSA-Chabrier, common-mode ×1.55, σ-dependent bracket B). Distribution
zero-points (NOT the test — the slope is): PRIMARY δ_canon median **+0.235 dex**
(16–84% [+0.047,+0.388]), δ_alt **+0.229** [+0.032,+0.381]. The ~0.2-dex zero-point is
absorbed by K_v/IMF/aperture conventions and is common-mode for the slope discriminator.

## 3. Resolved-proxy subsample + extraction (`download_maps.sh`, `extract_resolved_proxies.py`)

Frozen rule applied: SNR-top **16 per σ_e tercile** of the PRIMARY sample (tercile edges
133/201 km/s) → **N=48** (`maps_subsample.csv`), full target reached — no bandwidth
shortfall (MAPS gz are 2–6 MB each, 116 MB total, not the feared 50–100 MB each).

Extraction (mmu_scout `pilot_extract.py` machinery ported to native DR17 MAPS FITS:
STELLAR_SIGMA(+IVAR/MASK) ⊕ STELLAR_SIGMACORR quadrature ⊕ SPX_ELLCOO r/Re & azimuth ⊕
SPX_MFLUX weights) → `resolved_proxies.csv`, **48/48 clean**:

- **P2 (primary proxy)** dlnσ/dlnR over 0.5–1.5 Re: finite **48/48**, median **−0.113**,
  16–84% [−0.262, +0.011] — a real spread of falling-σ profiles, i.e. the proxy has
  dynamic range to regress against.
- **P1 (secondary)** σ_maj/σ_min in 0.5–1.0 Re: finite **33/48**, median 0.997,
  16–84% [0.961, 1.038]. All 15 non-finite are ≤37-fibre bundles failing the frozen
  ≥8-spaxel wedge floor — a bundle-size selection effect, stated; P1 is secondary by
  freeze anyway (inclination/shape-degenerate).
- **Integrity cross-checks:** resolved σ_e vs DAPall σ_1Re: corr 1.000, median ratio
  0.999 (the pipeline measures the same physical σ). Resolved V/σ vs the DAPall clipped
  proxy: corr 0.364 — expected-weak (different definitions + range restriction inside an
  already-selected V/σ<0.6 sample); the DAPall proxy remains the frozen selection variable.

## 4. Honesty rails carried (verbatim status)

1. **Frozen before touched:** FROZEN.md timestamp 2026-07-17T00:21:52Z precedes the first
   byte downloaded (HEAD checks only before freezing).
2. **The proxy is NOT β:** P1/P2 are LOS signatures contaminated by inclination, intrinsic
   shape, rotation residuals and M/L gradients; slow-rotator selection mitigates rotation
   only. Stage 2 (Jeans/JAM per-galaxy β) is the real test; the Jeans-theory sign map
   (radial anisotropy ↔ more negative P2; Binney & Mamon 1982; Cappellari 2008) is frozen.
3. **IMF confounder pre-registered with direction:** literature IMF-vs-σ trends can FAKE a
   positive MI-like slope if the proxy correlates with σ_e; the mandatory bracket-B rerun +
   log σ_e control are frozen in FROZEN.md §2; a slope that dies under bracket B is
   NOT robust, by freeze.
4. **Exploratory firewall:** nothing in this staging can support or kill the framework;
   no regression was run; the first number will be exploratory and reported straight,
   null/MG-favoring included.
5. **Both footings** in every δ column; **exit-0** drivers (`stage1_catalog.py`,
   `download_maps.sh`, `extract_resolved_proxies.py`); no hard-coded verdicts.

## 5. What fires next (the already-frozen spec, FROZEN.md §4)

δ (each footing × IMF bracket) vs **P2** (primary; P1 secondary) on the 48-galaxy resolved
subsample and — for the DAPall-level power statement — the catalog-level baseline; Huber
robust slope + partial Spearman with controls log M*, log R_e(kpc), z (+ log σ_e in the
bracket-B rerun); bootstrap CIs; full footing×bracket×cut grid reported, no cherry-pick.
**MI expects dδ/dP2 < 0 under the frozen sign map; MG-with-same-ν expects 0.** Power
statement for full-Jeans Stage 2 from the observed P2 scatter. If a public group catalog
is adopted for local density at firing time it must be named there; none was baked in here.
