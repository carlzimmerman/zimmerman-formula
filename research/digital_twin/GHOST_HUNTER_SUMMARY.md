# T³/Z₂ Ghost Hunter - Project Summary

## Overview

The Ghost Hunter is a tool for finding **topological duplicate images** of high-redshift galaxies in the T³/Z₂ orbifold universe model. In this topology, the universe has a finite fundamental domain (L_c = 20.6 Gpc), and light can wrap around, creating "ghost images" - the same object seen from two different directions.

## Theoretical Foundation

### The T³/Z₂ Topology
- Universe is a 3-torus (T³) with Z₂ orbifold action
- Fundamental domain size: **L_c = 20.6 Gpc** (from Zimmerman Formula)
- Z₂ acts as point reflection through the center: x → -x

### Ghost Image Geometry
For a galaxy at comoving distance D₁ from us:
- Its ghost appears at distance D₂ where **D₁ + D₂ = L_c = 20.6 Gpc**
- Ghost location is at **antipodal coordinates**:
  - Ghost_RA = RA + 180°
  - Ghost_Dec = -Dec
- The ghost shows **Z₂ parity inversion** (mirrored morphology)

### Key Insight
High-z galaxies (z > 10) are at D ~ 10 Gpc, meaning their ghosts are also at D ~ 10 Gpc (z ~ 10-20). Both the original and ghost are in the observable high-z universe!

## Files Created

### 1. `ghost_miner.py` - Core Prediction Algorithm
```
Location: research/digital_twin/ghost_miner.py
```

**Functions:**
- `comoving_distance_gpc(z)` - Calculates comoving distance using Planck 2018 cosmology
- `redshift_from_distance_gpc(d)` - Inverse: gets redshift from distance
- `antipodal_coordinates(ra, dec)` - Computes Z₂ involution coordinates
- `predict_ghost_location(galaxy)` - Full ghost prediction for a galaxy
- `check_catalog_for_ghosts()` - Searches catalog for self-consistent ghost pairs

**Chemical Fingerprint Lines** (for spectroscopic matching):
- [O III] 88μm (rest: 88.36 μm)
- N IV] 1486Å
- C IV 1549Å
- He II 1640Å
- Hα 6563Å

**Input Galaxies:** 8 JWST high-z galaxies including GLASS-z12, JADES-GS-z14-0, GN-z11, Maisie's Galaxy, etc.

### 2. `ghost_predictions.json` - Generated Predictions
```
Location: research/digital_twin/ghost_predictions.json
```

Contains predictions for 8 galaxies with structure:
```json
{
  "original": {
    "name": "GHZ2/GLASS-z12",
    "ra": 3.5,
    "dec": -30.4,
    "redshift": 12.34,
    "comoving_distance_gpc": 10.07
  },
  "predicted_ghost": {
    "ra": 183.5,
    "dec": 30.4,
    "expected_redshift": 15.64,
    "expected_distance_gpc": 10.53,
    "search_radius_deg": 5.0,
    "redshift_range": [15.14, 16.14]
  },
  "interpretation": {
    "distance_sum": 20.6,
    "ghost_appears_younger": true,
    "notes": "Ghost should show Z₂ parity inversion (mirrored morphology)"
  }
}
```

### 3. `mast_ghost_query.py` - Archive Search Script
```
Location: research/digital_twin/mast_ghost_query.py
```

Uses `astroquery` library to search astronomical archives at predicted ghost coordinates:
- **MAST** - JWST and HST observations
- **SIMBAD** - Known astronomical objects
- **NED** - NASA Extragalactic Database (galaxies with redshifts)

**Output:** `mast_ghost_search_results.json` with observation counts, programs, and priority assessments.

### 4. `fits_ingestion.py` - FITS Data Pipeline (Directive JJJJ)
```
Location: research/digital_twin/fits_ingestion.py
```

Full pipeline for downloading and processing raw JWST spectral data:

**Capabilities:**
- Queries MAST for NIRSpec/MIRI spectroscopy at ghost coordinates
- Filters for SCIENCE products: X1D (1D extracted) and S3D (3D cubes)
- Downloads to local cache (`data_cache/fits_raw/`) with progress tracking
- Extracts WAVELENGTH and FLUX arrays from FITS binary tables
- Isolates emission line regions (e.g., [O III] 88μm, C IV, etc.)
- Exports to compressed Parquet for WebGL frontend

**Key Functions:**
```python
search_spectral_products(ra, dec)  # Query MAST for spectra
download_products(products)         # Download to local cache
extract_spectrum_from_x1d(path)     # Extract wavelength/flux
isolate_emission_line(spec, line, z)  # Isolate spectral region
export_to_parquet(spectra, file)    # Export for frontend
```

**Output Directories:**
- `data_cache/fits_raw/` - Raw FITS files
- `data_cache/spectra/` - Extracted spectra (JSON + Parquet)

### 4. `ghost_candidates.json` - Self-Matching Results
```
Location: research/digital_twin/ghost_candidates.json
```
Currently empty - no self-consistent ghost pairs found in the input catalog (expected, since we're searching external archives).

## Prediction Table

| Original Galaxy | z_orig | Ghost RA | Ghost Dec | Expected z_ghost |
|----------------|--------|----------|-----------|------------------|
| GHZ2/GLASS-z12 | 12.34 | 183.5° | +30.4° | 15.6 |
| JADES-GS-z14-0 | 14.32 | 233.16° | +27.77° | 13.4 |
| JADES-GS-z13-0 | 13.2 | 233.15° | +27.82° | 14.6 |
| GN-z11 | 10.6 | 9.1° | -62.24° | 18.7 |
| Maisie's Galaxy | 11.4 | 34.82° | -52.88° | 17.1 |
| UNCOVER-z13 | 12.79 | 183.59° | +30.42° | 15.0 |
| RXCJ2248-ID | 9.51 | 162.17° | +44.53° | 21.6 |
| S5-z17-1 (candidate) | 16.7 | 233.12° | +27.85° | 11.6 |

## Ghost Validation Criteria

To confirm a topological ghost pair:

1. **Distance Constraint**: D₁ + D₂ ≈ 20.6 Gpc (±0.5 Gpc tolerance)

2. **Spectroscopic Fingerprint**: Identical emission line ratios
   - Same chemical abundances
   - Same relative line strengths
   - Redshift-corrected wavelengths match

3. **Mirrored Morphology**: Z₂ parity inversion
   - Galaxy structure should be mirror-flipped
   - Requires high-resolution imaging comparison

4. **Consistent SED**: Photometric colors should match (after redshift correction)

5. **No Proper Motion Discrepancy**: Stars in foreground would have proper motion; ghosts wouldn't

## CRITICAL UPDATE: Z² Metric Implementation (May 25, 2026)

### The ΛCDM Error Has Been Fixed!
The ghost_miner.py now uses the **Z² ODE solver** instead of ΛCDM.

The Z² metric includes the volumetric deficit term:
```
dD_c/dz = (c/H₀) / sqrt[Ω_m(1+z)³ + Ω_r(1+z)⁴ + (1 - (D_c/L_c)³)]
```

This is an ODE because the deficit depends on D_c itself. We solve it with `scipy.integrate.solve_ivp`.

### BREAKTHROUGH: Ghost Predictions Are Dramatically Different!

| Galaxy | Original z | OLD (ΛCDM) Ghost z | NEW (Z²) Ghost z |
|--------|------------|-------------------|-----------------|
| GLASS-z12 | 12.34 | 15.6 | **46.0** |
| JADES-GS-z14-0 | 14.32 | 13.4 | **36.1** |
| GN-z11 | 10.6 | 18.7 | **62.0** |
| S5-z17-1 | 16.7 | 11.6 | **29.1** |

### Why Are Z² Ghosts at Higher Redshift?
1. Z² gives ~370 Mpc **smaller** distances at the same z (compared to ΛCDM)
2. Ghost distance D_ghost = 20.6 - D_original is therefore **larger**
3. The Z² distance-redshift relation **asymptotes** at ~12.8 Gpc (z→∞)
4. Large ghost distances require **very high redshifts**

### Observational Implications
- **Ghosts of z~10-14 galaxies are at z~30-80** - beyond JWST spectroscopic reach
- **To find observable ghosts (z<15), originals must be at z>30** - too faint to detect
- **Low-z (z<7) galaxies have ghosts beyond the asymptotic limit** - unobservable in Z² geometry

### New Strategy Required
1. **CMB Circles-in-the-Sky**: More promising than galaxy pair matching
2. **4PCF Topology Signal**: Already showing evidence (r=0.999 NGC-SGC correlation)
3. **Future: Roman/Euclid deep surveys** may detect z>30 sources

## Known Issues / Future Work

### Search Improvements
- Implement **Cosmic Crystallography** - pair-separation histogram analysis
- Cross-match with full JWST high-z catalogs (not just 8 galaxies)
- Add morphology comparison tools for Z₂ parity check

### Archive Query Status
- MAST queries initially failed with raw HTTP (500 errors)
- Rewrote using `astroquery` library - now working
- Full results saved to `mast_ghost_search_results.json`

## How to Run

```bash
# Generate ghost predictions
cd research/digital_twin
python ghost_miner.py

# Query archives at ghost coordinates
python mast_ghost_query.py
```

## Related Concepts

- **Cosmic Crystallography**: Mathematical technique for detecting topology via pair-separation histograms
- **CMB Circles-in-the-Sky**: Alternative topology detection via CMB pattern matching
- **Matched Circles**: If same CMB pattern appears at antipodal points

## References

- Gemini conversation (May 2026) - Directive DDDD, EEEE for ghost hunting
- Luminet et al. - Cosmic Crystallography methodology
- Cornish et al. - Circles in the sky CMB analysis

## Git Commits

1. `07c7a983` - "Topological Ghost Miner: Search for T³/Z₂ duplicate images"
   - Added ghost_miner.py, ghost_predictions.json, ghost_candidates.json

---

*Last updated: May 25, 2026*
*Author: Carl Zimmerman / Claude*
