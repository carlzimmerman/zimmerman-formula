# Unified Galaxy HI Rotation Curve Corpus (v7.0)

**SPARC + THINGS + LITTLE THINGS + WALLABY DR2**

*Structured for Computational Astrophysics and LLM-Based Inference*

Flynn, D.C. (EPS Research, Laurel MD) | ORCID: 0000-0002-2768-6650

davidflynn@eps-research.com | DOI: 10.5281/zenodo.19425428

---

## 1. Summary

This corpus provides **8,963 individually resolved rotation curve measurements across 423 galaxies**, drawn from four major HI surveys: SPARC (Lelli, McGaugh & Schombert 2016), THINGS (de Blok et al. 2008; Walter et al. 2008), LITTLE THINGS (Oh et al. 2015), and WALLABY DR2 (Deg et al. 2022; Murugeshan et al. 2024). An additional 15 galaxies from the THINGS survey contribute verified kinematic metadata (distance, inclination, position angle) without per-point rotation curve data, bringing the catalog total to **438 galaxies**.

The primary deliverable is a **single JSON file** containing nested, per-ring rotation curve data for each galaxy alongside survey metadata, column definitions, data-quality annotations, and provenance. A companion **JSONL file** (one galaxy per line) provides the same content in a streaming format optimized for LLM retrieval-augmented generation (RAG) pipelines and vector database ingestion. A flat CSV/XLSX (one row per galaxy, 38 columns) provides a catalog-level summary for filtering, cross-matching, and sample selection. The JSON is the authoritative source; the JSONL and CSV are derived from it.

Version 7.0 updates the description and documentation from v6.0. All kinematic parameters (inclination, distance, PA, Vsys, coordinates) have been re-verified against scanned primary tables: de Blok et al. (2008) Tables 1 and 2 for THINGS, Oh et al. (2015) Table 1 for LITTLE THINGS, and Lelli et al. (2016) Table 1 (Lelli2016c.mrt) for SPARC. The corpus applies consistent unit conventions (kpc, km/s), cross-matches galaxies appearing in multiple surveys, and annotates data-quality issues at the galaxy level using a two-tier quality system. The JSON schema has been fully harmonized across all four surveys in this version: all surveys use a `data` key with standardized column names (`Rad`, `Vrot`, `Vdisp`).

The corpus was constructed to support both traditional numerical analysis and Large Language Model (LLM) retrieval-augmented generation (RAG) pipelines for astrophysical inference, including application of the empirical omega correction (Flynn & Cannaliato 2025).

---

## 2. What You Can Do With This Data

The JSON carries enough per-point data to directly plot rotation curves, compute baryonic mass models, fit dark matter halo profiles, apply the omega correction, or test MOND/RAR predictions — without returning to the original survey files. SPARC galaxies include full baryonic decomposition (Vgas, Vdisk, Vbul, surface brightness); THINGS and LITTLE THINGS galaxies include observed rotation velocities with uncertainties; WALLABY galaxies include per-ring rotation velocity and velocity dispersion.

### Minimal Plotting Example (Python, JSON)

```python
import json, matplotlib.pyplot as plt

with open('rotation_curve_corpus_v7.json') as f:
    corpus = json.load(f)

ddo161 = next(g for g in corpus['galaxies'] if g['galaxy'] == 'DDO161')
R    = [p['Rad']  for p in ddo161['data']]
Vobs = [p['Vobs'] for p in ddo161['data']]
errV = [p['errV'] for p in ddo161['data']]

plt.errorbar(R, Vobs, yerr=errV, fmt='o', label='Vobs')
plt.xlabel('R (kpc)'); plt.ylabel('V (km/s)')
plt.title('DDO 161 Rotation Curve'); plt.legend(); plt.show()
```

### RAG Pipeline Example (Python, JSONL)

```python
# Load all 438 galaxies into a list without reading the full JSON into memory
galaxies = []
with open('rotation_curve_corpus_v7.jsonl') as f:
    for line in f:
        galaxies.append(json.loads(line))

# Filter to omega-ready SPARC galaxies
omega_ready = [g for g in galaxies if g['omega_ready'] and g['survey'] == 'SPARC']
print(f"{len(omega_ready)} SPARC galaxies ready for omega correction")
```

---

## 3. Survey Coverage

| Survey | Galaxies | Data Points | Tier | Primary Reference |
|--------|----------|-------------|------|-------------------|
| SPARC | 175 | 3,391 | 1 | Lelli et al. (2016), AJ 152, 157 |
| THINGS | 34 (19 w/ data) | 2,110 | 1 | de Blok et al. (2008), AJ 136, 2648 |
| LITTLE THINGS | 26 | 1,716 | 1 | Oh et al. (2015), AJ 149, 180 |
| WALLABY DR2 | 203 | 1,746 | 2 | Deg et al. (2022); Murugeshan et al. (2024) |
| **Total** | **438** | **8,963** | | |

Fifteen THINGS galaxies (NGC 628, NGC 1569, Ho II, M81dwA, DDO 53, Ho I, NGC 3077, M81dwB, NGC 3184, NGC 3351, NGC 4214, NGC 4449, NGC 5194, NGC 5236, NGC 5457) are included with verified kinematic metadata but without per-point rotation curves. These galaxies were observed as part of the THINGS survey (Walter et al. 2008) but were not included in the de Blok et al. (2008) tilted-ring kinematic analysis due to morphological disturbance, low inclination, strong non-circular motions, or other factors precluding reliable rotation curve extraction. Fourteen THINGS galaxies also appear in SPARC and carry full baryonic decomposition under their SPARC entries.

---

## 4. Quality Tiers

| Tier | Surveys | Description |
|------|---------|-------------|
| 1 | SPARC, THINGS, LITTLE THINGS | Hand-curated rotation curves with per-point uncertainties. Full baryonic decomposition (Vgas, Vdisk, Vbul) for SPARC. Kinematic parameters verified against scanned primary tables. |
| 2 | WALLABY DR2 | Automated WKAPP pipeline (3DBarolo + FAT), peer-reviewed. 30 arcsec ASKAP resolution. No per-ring uncertainties. No baryonic decomposition. Vrot unreliable below 50 km/s. Distances from Hubble flow (H₀ = 75 km/s/Mpc). |

---

## 5. Files

### 5.1 rotation_curve_corpus_v7.json — Master JSON (Primary Deliverable)

Single JSON document (~2.0 MB) containing all 438 galaxy entries in a unified schema. This is the authoritative source from which the JSONL and CSV are derived. The top-level object has two keys:

- **metadata**: corpus-level provenance including version, creator, survey descriptions, quality-tier definitions, citation, last-updated timestamp, and version_notes.
- **galaxies**: array of 438 objects, each containing (a) galaxy-level metadata (survey, distance, inclination, coordinates, quality tier, notes) and (b) per-ring rotation curve data with column definitions. 423 of 438 galaxies carry full per-point data.

All four surveys use a unified `data` key with standardized column names. The schema is fully harmonized in v7.0.

**Per-ring columns by survey:**

| Survey | Data Key | Per-Ring Columns |
|--------|----------|-----------------|
| SPARC (175) | `data` | Rad, Vobs, errV, Vgas, Vdisk, Vbul, SBdisk, SBbul |
| THINGS (19 w/ data) | `data` | Rad, Vrot, e_Vrot |
| LITTLE THINGS (26) | `data` | Rad, Vrot, errV |
| WALLABY (203) | `data` | Rad, Vrot, Vdisp |

Each entry includes a `columns` dictionary defining each field's unit and description.

### 5.2 rotation_curve_corpus_v7.jsonl — RAG Corpus (New in v7.0)

JSONL file (one JSON object per line, one galaxy per line, 438 lines total). Contains the same scientific content as the master JSON in a streaming format optimized for:

- LLM retrieval-augmented generation (RAG) pipelines
- Vector database ingestion (one embedding per galaxy)
- Memory-efficient processing without loading the full corpus

The JSONL schema extends the JSON with additional fields: `kinematic_model`, `ingest_mode`, `omega_ready`, `has_vgas_profile`, `has_stellar_mass`, `stellar_mass_method`, `distance_method`, `corpus_version`, and `corpus_source`. These fields are also present in the updated flat CSV.

THINGS datacube stubs (15 galaxies with no per-point data) are included with `data: []` and `n_points: 0`, providing full kinematic metadata for cross-matching and pipeline filtering.

### 5.3 rotation_curve_corpus_v7_flat.csv — Catalog Table

One row per galaxy (438 rows, 38 columns). Designed for sample selection, filtering, and cross-matching. Contains summary statistics (n_points, r_max_kpc, vrot_max_kms, etc.) but not per-point data. Directly loadable with pandas, R, or any tabular analysis tool.

### 5.4 rotation_curve_corpus_v7_flat.xlsx — Catalog Table (Excel)

Identical content to the flat CSV, formatted as an Excel worksheet with frozen header row and auto-sized columns. Regenerated from the CSV in this version to ensure full schema alignment.

### 5.5 rotation_curve_corpus_v7_by_galaxy.zip — Per-Galaxy JSON Files

One JSON file per galaxy (438 files). Useful for galaxy-by-galaxy inspection and targeted ingestion workflows.

### 5.6 Scripts

- **make_v7_jsonl_v1.2.py** — Generates `rotation_curve_corpus_v7.jsonl` from the master JSON. Run with `python make_v7_jsonl_v1.2.py`.
- **clean_v7_json_v1.1.py** — Schema normalization script that produced the v7.0 cleaned JSON from the v6.0 source. Included for reproducibility.
- **update_v7_csv_v1.0.py** — Generates the updated flat CSV and XLSX from the master JSON. Run with `python update_v7_csv_v1.0.py`.
- **wallaby_ingest.py** — Original WALLABY DR2 ingestion script from CADC 3DBarolo model files.
- **make_figures_v7.py** — Figure generation script for the companion data descriptor paper.

---

## 6. Flat CSV/XLSX Schema (38 Columns)

| Field | Surveys | Coverage | Description |
|-------|---------|----------|-------------|
| `galaxy` | All | 438/438 | Galaxy identifier |
| `survey` | All | 438/438 | SPARC / THINGS / LITTLE_THINGS / WALLABY |
| `telescope` | THINGS, LT, WALLABY | 263/438 | Instrument identifier |
| `quality_tier` | All | 438/438 | 1 = hand-curated, 2 = automated pipeline |
| `ra_deg` | THINGS, LT, WALLABY | 263/438 | Right ascension (J2000, decimal degrees) |
| `dec_deg` | THINGS, LT, WALLABY | 263/438 | Declination (J2000, decimal degrees) |
| `distance_mpc` | All | 438/438 | Distance (Mpc) |
| `e_distance_mpc` | SPARC | 175/438 | Distance uncertainty (Mpc); Lelli2016c |
| `distance_method` | LT, WALLABY | 229/438 | Distance method: TRGB (LT) or Hubble (WALLABY) |
| `vsys_kms` | THINGS, LT, WALLABY | 263/438 | Systemic velocity (km/s) |
| `inc_deg` | All | 438/438 | Inclination (degrees); verified vs. primary tables |
| `e_inc_deg` | SPARC | 175/438 | Inclination uncertainty (degrees); Lelli2016c |
| `pa_deg` | THINGS, LT, WALLABY | 261/438 | Position angle (degrees); M81DwA/B undetermined |
| `hubble_type` | SPARC | 175/438 | RC3 morphological type string (e.g. Im, Sc, Sb) |
| `m2l_disk` | SPARC | 175/438 | Mass-to-light ratio at [3.6] at max disk; Starkman+2018 |
| `has_bulge` | SPARC, LT | 201/438 | Boolean bulge flag |
| `has_vgas_profile` | All | 438/438 | True if Vgas profile present in data array |
| `has_stellar_mass` | All | 438/438 | True if stellar mass decomposition present |
| `stellar_mass_method` | SPARC | 175/438 | Mass model method; SPARC_Upsilon1_normalized |
| `kinematic_model` | All | 438/438 | Model type: observed_rc / tilted_ring_3DFIT / tilted_ring_2DBAT / 3DBarolo |
| `ingest_mode` | All | 438/438 | Provenance: sparc_v7_transfer / things_datacube_stub / little_things_v7_transfer / wallaby_v7_transfer |
| `corpus_version` | All | 438/438 | v7.0 |
| `corpus_source` | All | 438/438 | rotation_curve_corpus_v7 |
| `omega_ready` | All | 438/438 | True if galaxy meets criteria for omega correction pipeline |
| `n_points` | All | 438/438 | Number of rotation curve points (0 for THINGS stubs) |
| `r_min_kpc` | All | 423/438 | Innermost radius of rotation curve (kpc) |
| `r_max_kpc` | All | 423/438 | Outermost radius (kpc) |
| `vrot_min_kms` | All | 423/438 | Minimum observed rotation velocity (km/s) |
| `vrot_mean_kms` | All | 423/438 | Mean rotation velocity (km/s) |
| `vrot_max_kms` | All | 423/438 | Peak rotation velocity (km/s) |
| `vdisp_mean_kms` | WALLABY | 203/438 | Mean velocity dispersion (km/s); WALLABY only |
| `vgas_negative_rows` | SPARC | 175/438 | Count of inner-disk rows where Vgas < 0 |
| `r0p3_kpc` | LITTLE THINGS | 26/438 | Radius at logarithmic slope = 0.3 (kpc); Oh+2015 |
| `v0p3_kms` | LITTLE THINGS | 26/438 | Velocity at r0.3 (km/s); Oh+2015 |
| `beam_arcsec` | WALLABY, LT | 229/438 | Synthesized beam FWHM (arcsec) |
| `qflag_model` | WALLABY | 203/438 | 3DBarolo model quality flag (0=good, 1=marginal) |
| `reference` | All | 438/438 | Primary citation string |
| `notes` | All | 41/438 | Data quality notes and provenance flags |

---

## 7. Key Conventions

### 7.1 Radii

All radii in kiloparsecs. THINGS radii converted from arcseconds using R[kpc] = R[arcsec] × D[Mpc] × 1000 × π / 648000.

### 7.2 SPARC Baryonic Velocities and Quadrature Convention

Gas contribution Vgas may be negative at inner radii due to the sign-preserving quadrature convention used throughout SPARC. The total baryonic velocity is computed as:

    Vbar = sign(Vgas) × sqrt(|Vgas|² + Vdisk² + Vbul²)   [inner disk, where Vgas < 0]
    Vbar = sqrt(Vgas² + Vdisk² + Vbul²)                    [outer disk]

All velocity components are stored at mass-to-light ratio Υ = 1 (maximum disk values available via the `m2l_disk` column). The `vgas_negative_rows` column in the CSV records the count of inner-disk radii where Vgas < 0 for each SPARC galaxy, enabling downstream quadrature handling.

### 7.3 WALLABY Velocities

Vrot from the published 3DBarolo+FAT WKAPP pipeline. No baryonic decomposition available. Vrot values below 50 km/s should be treated with caution due to beam smearing at 30 arcsec resolution. The `qflag_model` field records the pipeline quality flag (0=good, 1=marginal).

### 7.4 Omega Correction

The corpus supports application of the empirical omega correction (Flynn & Cannaliato 2025): V_obs(R) = V_kepler(R) + R × ω. The `omega_ready` flag identifies galaxies that meet the pipeline criteria: clean Vgas profile (vgas_negative_rows = 0 for SPARC), full baryonic decomposition, and no missing radius values. 118 SPARC galaxies and all 26 LITTLE THINGS galaxies are omega-ready.

### 7.5 Kinematic Parameter Provenance

SPARC ra_deg/dec_deg/vsys_kms/pa_deg are null in the JSON and absent from the flat CSV: these were not published in a unified SPARC table and are distributed across approximately 50 individual source papers cited in Lelli et al. (2016) Table 1. All other kinematic parameters for SPARC have been verified against Lelli2016c.mrt (scanned). THINGS parameters verified against de Blok et al. (2008) Tables 1 and 2 (scanned). LITTLE THINGS parameters verified against Oh et al. (2015) Table 1 (scanned).

### 7.6 JSON Schema

All four surveys use a unified `data` key with standardized column names (`Rad`, `Vrot`, `Vdisp` where applicable). This is a breaking change from the pre-v7.0 schema in which WALLABY used a `rotation_curve` key with column names `rad_kpc`, `vrot_kms`, and `vdisp_kms`. Code written against the pre-v7.0 schema should be updated accordingly:

```python
# v7.0 unified access — works for all surveys
points = galaxy.get('data', [])
for p in points:
    radius = p['Rad']
    vrot   = p.get('Vrot') or p.get('Vobs')   # SPARC uses Vobs; others use Vrot
```

### 7.7 SPARC Velocity Column

SPARC per-ring data uses `Vobs` (observed rotation velocity) rather than `Vrot`. This distinction is intentional: SPARC `Vobs` is the raw observed velocity without asymmetric drift correction, whereas `Vrot` in THINGS, LITTLE THINGS, and WALLABY reflects modeled or corrected rotation. The `kinematic_model` field (`observed_rc` for SPARC) makes this machine-readable.

---

## 8. Known Limitations

**Fifteen THINGS galaxies lack per-point rotation curve data.** These galaxies (NGC 628, NGC 1569, Ho II, M81dwA, DDO 53, Ho I, NGC 3077, M81dwB, NGC 3184, NGC 3351, NGC 4214, NGC 4449, NGC 5194/M51, NGC 5236/M83, NGC 5457/M101) were observed as part of the THINGS survey (Walter et al. 2008) but were not included in the de Blok et al. (2008) tilted-ring kinematic analysis. They are included with verified kinematic metadata, `n_points = 0`, and `ingest_mode = things_datacube_stub`.

**SPARC entries lack coordinates and systemic velocities.** SPARC ra_deg, dec_deg, vsys_kms, and pa_deg are null because Lelli et al. (2016) did not publish these in a unified table. They are distributed across ~50 individual source papers. Distance method is similarly unavailable in a unified form.

**WALLABY rotation curves carry no per-ring uncertainties and no baryonic decomposition.** Vrot below 50 km/s is unreliable due to beam smearing at 30 arcsec ASKAP resolution. `qflag_model = 1` entries should be treated with additional caution.

**LITTLE THINGS data arrays contain duplicate radii.** The Oh et al. (2015) data includes both approach and receding half rotation curves at each radius, resulting in duplicate Rad values in the data array. Use the mean or handle explicitly in downstream pipelines.

---

## 9. Related Work

Flynn, D.C. & Cannaliato, J. (2025). "A new empirical fit to galaxy rotation curves." *Frontiers in Astronomy and Space Sciences*, 12. DOI: 10.3389/fspas.2025.1680387

Flynn, D.C. (2026). "Rotation Curve Corpus v7.0: A unified HI kinematic catalog." *Astronomy and Computing* (data descriptor, in revision).

---

## 10. Data Provenance

All underlying rotation curve data are drawn from published, publicly available sources:

- **SPARC**: Lelli, McGaugh & Schombert (2016), AJ 152, 157 — astroweb.cwru.edu/SPARC. Kinematic parameters from Lelli2016c.mrt (scanned Table 1).
- **THINGS RC**: de Blok et al. (2008), AJ 136, 2648. Tilted-ring rotation curves for 19 of 34 THINGS galaxies. Tilted-ring parameters from Table 2 (scanned). Indicative inclinations from Table 1 (scanned).
- **THINGS survey**: Walter et al. (2008), AJ 136, 2563. Coordinates and survey metadata for all 34 THINGS galaxies.
- **LITTLE THINGS**: Oh et al. (2015), AJ 149, 180. All kinematic parameters from Table 1 (scanned). VizieR J/AJ/149/180.
- **WALLABY DR2 kinematics**: Deg et al. (2022), PASA 39, e059; Murugeshan et al. (2024). Ingested from CADC 3DBarolo DR2 model files.
- **WALLABY survey**: Westmeier et al. (2022), PASA 39, e058.

---

## 11. License and Citation

The corpus (schema, normalization, annotations, crossmatch index, and unified structure) is original work by D.C. Flynn / EPS Research and is released under **CC BY 4.0**.

If you use this corpus, please cite:

> Flynn, D.C. (2026). *Unified Galaxy HI Rotation Curve Corpus (v7.0): SPARC + THINGS + LITTLE THINGS + WALLABY DR2.* Zenodo. DOI: 10.5281/zenodo.19425428

and the relevant underlying survey papers listed in Section 10.
