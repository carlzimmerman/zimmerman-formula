#!/usr/bin/env python3
"""
=============================================================================
FITS INGESTION PIPELINE (Directive JJJJ)
=============================================================================
Securely downloads, stores, and processes raw JWST and ALMA FITS files
for topological ghost candidate analysis.

Pipeline:
1. Query MAST for observations at predicted ghost coordinates
2. Filter for SCIENCE products (X1D spectra, S3D cubes)
3. Download to local cache with progress tracking
4. Extract WAVELENGTH and FLUX arrays from binary tables
5. Isolate emission line regions (e.g., [O III] 88μm)
6. Export to compressed Parquet for WebGL frontend

Author: Carl Zimmerman / Claude
=============================================================================
"""

import numpy as np
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# Progress tracking
from tqdm import tqdm

# Astroquery for MAST access
from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
import astropy.units as u

# FITS file handling
from astropy.io import fits

# Parquet export
try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False
    print("WARNING: pyarrow not installed. Parquet export disabled.")

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Local data cache
DATA_CACHE_DIR = Path(__file__).parent / "data_cache"
FITS_RAW_DIR = DATA_CACHE_DIR / "fits_raw"
SPECTRA_DIR = DATA_CACHE_DIR / "spectra"

# Ensure directories exist
FITS_RAW_DIR.mkdir(parents=True, exist_ok=True)
SPECTRA_DIR.mkdir(parents=True, exist_ok=True)

# Search parameters
DEFAULT_SEARCH_RADIUS_ARCMIN = 10.0

# Emission line rest wavelengths (μm) for targeting
EMISSION_LINES = {
    "OIII_88": 88.36,      # [O III] 88μm - key high-z diagnostic
    "OIII_52": 51.81,      # [O III] 52μm
    "NII_122": 121.90,     # [N II] 122μm
    "CII_158": 157.74,     # [C II] 158μm - brightest FIR line
    "Lya": 0.12157,        # Ly-α 1216Å
    "CIV": 0.1549,         # C IV 1549Å
    "HeII": 0.1640,        # He II 1640Å
    "CIII": 0.1909,        # C III] 1909Å
    "Halpha": 0.6563,      # Hα 6563Å
}


# =============================================================================
# MAST QUERY AND FILTERING
# =============================================================================

@dataclass
class SpectralProduct:
    """Metadata for a downloadable spectral product"""
    obs_id: str
    product_filename: str
    product_type: str  # X1D, S3D, etc.
    instrument: str
    target_name: str
    proposal_id: str
    file_size_mb: float
    local_path: Optional[Path] = None


def search_spectral_products(
    ra: float,
    dec: float,
    radius_arcmin: float = DEFAULT_SEARCH_RADIUS_ARCMIN
) -> List[SpectralProduct]:
    """
    Search MAST for spectral products at given coordinates.

    Filters for:
    - JWST NIRSpec or MIRI spectroscopy
    - productType == "SCIENCE"
    - productSubGroupDescription == "X1D" (1D extracted) or "S3D" (3D cube)

    Args:
        ra: Right Ascension in degrees
        dec: Declination in degrees
        radius_arcmin: Search radius

    Returns:
        List of SpectralProduct objects
    """
    print(f"Searching MAST at RA={ra:.3f}°, Dec={dec:.3f}° (r={radius_arcmin}')")

    coord = SkyCoord(ra=ra, dec=dec, unit="deg")

    # Query observations
    try:
        obs_table = Observations.query_region(
            coord,
            radius=radius_arcmin * u.arcmin
        )
    except Exception as e:
        print(f"  MAST query error: {e}")
        return []

    if obs_table is None or len(obs_table) == 0:
        print("  No observations found")
        return []

    # Filter for JWST spectroscopy
    jwst_spec = []
    for row in obs_table:
        collection = str(row["obs_collection"])
        instrument = str(row.get("instrument_name", ""))

        if collection != "JWST":
            continue

        # NIRSpec or MIRI for spectroscopy
        if "NIRSPEC" not in instrument.upper() and "MIRI" not in instrument.upper():
            continue

        jwst_spec.append(row)

    if not jwst_spec:
        print("  No JWST spectroscopy found")
        return []

    print(f"  Found {len(jwst_spec)} JWST spectroscopic observations")

    # Get product list for each observation
    products = []

    for obs in tqdm(jwst_spec, desc="  Fetching products"):
        try:
            obs_id = obs["obsid"]
            product_list = Observations.get_product_list(obs)

            if product_list is None:
                continue

            for prod in product_list:
                prod_type = str(prod.get("productType", ""))
                subgroup = str(prod.get("productSubGroupDescription", ""))

                # Filter for science spectra
                if prod_type != "SCIENCE":
                    continue

                if subgroup not in ["X1D", "S3D", "UNCAL", "CAL"]:
                    continue

                # Prefer X1D (extracted 1D) and S3D (3D cubes)
                if subgroup in ["X1D", "S3D"]:
                    filename = str(prod.get("productFilename", ""))
                    size_bytes = prod.get("size", 0)

                    products.append(SpectralProduct(
                        obs_id=str(obs_id),
                        product_filename=filename,
                        product_type=subgroup,
                        instrument=str(obs.get("instrument_name", "")),
                        target_name=str(obs.get("target_name", "")),
                        proposal_id=str(obs.get("proposal_id", "")),
                        file_size_mb=size_bytes / (1024 * 1024) if size_bytes else 0
                    ))

        except Exception as e:
            print(f"  Error getting products: {e}")
            continue

    print(f"  Total spectral products: {len(products)}")
    return products


# =============================================================================
# DOWNLOAD MANAGER
# =============================================================================

def download_products(
    products: List[SpectralProduct],
    max_size_mb: float = 500.0,
    skip_existing: bool = True
) -> List[SpectralProduct]:
    """
    Download spectral products to local cache.

    Args:
        products: List of products to download
        max_size_mb: Maximum total size to download
        skip_existing: Skip files that already exist locally

    Returns:
        List of products with local_path set
    """
    downloaded = []
    total_size = 0

    for prod in tqdm(products, desc="Downloading"):
        # Check size limit
        if total_size + prod.file_size_mb > max_size_mb:
            print(f"  Size limit reached ({max_size_mb} MB)")
            break

        # Check if already exists
        local_path = FITS_RAW_DIR / prod.product_filename

        if skip_existing and local_path.exists():
            print(f"  Cached: {prod.product_filename}")
            prod.local_path = local_path
            downloaded.append(prod)
            continue

        # Download
        try:
            # Use astroquery to download
            manifest = Observations.download_products(
                [prod.obs_id],
                productSubGroupDescription=[prod.product_type],
                download_dir=str(FITS_RAW_DIR)
            )

            if manifest is not None and len(manifest) > 0:
                # Find the downloaded file
                for row in manifest:
                    if prod.product_filename in str(row.get("Local Path", "")):
                        prod.local_path = Path(row["Local Path"])
                        downloaded.append(prod)
                        total_size += prod.file_size_mb
                        break

        except Exception as e:
            print(f"  Download error: {e}")
            continue

    print(f"Downloaded {len(downloaded)} files ({total_size:.1f} MB)")
    return downloaded


# =============================================================================
# SPECTRAL EXTRACTION ENGINE
# =============================================================================

@dataclass
class ExtractedSpectrum:
    """Extracted spectral data from FITS"""
    source_file: str
    instrument: str
    target_name: str

    # Core data
    wavelength_um: np.ndarray  # Wavelength in microns
    flux: np.ndarray           # Flux (units vary)
    flux_error: Optional[np.ndarray] = None

    # Metadata
    exposure_time: float = 0.0
    redshift_estimate: Optional[float] = None

    def to_dict(self) -> Dict:
        return {
            "source_file": self.source_file,
            "instrument": self.instrument,
            "target_name": self.target_name,
            "wavelength_um": self.wavelength_um.tolist(),
            "flux": self.flux.tolist(),
            "flux_error": self.flux_error.tolist() if self.flux_error is not None else None,
            "exposure_time": self.exposure_time,
            "redshift_estimate": self.redshift_estimate
        }


def extract_spectrum_from_x1d(fits_path: Path) -> Optional[ExtractedSpectrum]:
    """
    Extract wavelength and flux from a JWST X1D (1D extracted spectrum) FITS file.

    The X1D format typically has:
    - Extension 1: EXTRACT1D binary table with WAVELENGTH, FLUX, FLUX_ERROR columns

    Args:
        fits_path: Path to the X1D FITS file

    Returns:
        ExtractedSpectrum object or None if extraction fails
    """
    try:
        with fits.open(fits_path) as hdu:
            # Primary header metadata
            primary = hdu[0].header
            instrument = primary.get("INSTRUME", "UNKNOWN")
            target = primary.get("TARGNAME", "UNKNOWN")
            exptime = primary.get("EFFEXPTM", primary.get("EXPTIME", 0))

            # Find the EXTRACT1D extension
            extract_ext = None
            for ext in hdu:
                if ext.name == "EXTRACT1D":
                    extract_ext = ext
                    break

            if extract_ext is None:
                # Try first binary table
                for ext in hdu:
                    if isinstance(ext, fits.BinTableHDU):
                        extract_ext = ext
                        break

            if extract_ext is None:
                print(f"  No spectral data found in {fits_path.name}")
                return None

            # Extract columns
            data = extract_ext.data
            colnames = [c.upper() for c in data.columns.names]

            # Wavelength (might be in different units)
            if "WAVELENGTH" in colnames:
                wavelength = data["WAVELENGTH"]
            elif "WAVE" in colnames:
                wavelength = data["WAVE"]
            else:
                print(f"  No wavelength column in {fits_path.name}")
                return None

            # Convert to microns if needed
            wave_unit = extract_ext.header.get("TUNIT1", "um")
            if "angstrom" in wave_unit.lower() or wave_unit == "A":
                wavelength = wavelength / 10000.0  # Å to μm
            elif "nm" in wave_unit.lower():
                wavelength = wavelength / 1000.0   # nm to μm
            elif "m" == wave_unit.lower():
                wavelength = wavelength * 1e6      # m to μm

            # Flux
            if "FLUX" in colnames:
                flux = data["FLUX"]
            elif "FLUX_DENSITY" in colnames:
                flux = data["FLUX_DENSITY"]
            else:
                print(f"  No flux column in {fits_path.name}")
                return None

            # Flux error (optional)
            flux_err = None
            if "FLUX_ERROR" in colnames:
                flux_err = data["FLUX_ERROR"]
            elif "ERROR" in colnames:
                flux_err = data["ERROR"]

            # Clean data (remove NaNs and infinities)
            mask = np.isfinite(wavelength) & np.isfinite(flux)
            wavelength = wavelength[mask]
            flux = flux[mask]
            if flux_err is not None:
                flux_err = flux_err[mask]

            return ExtractedSpectrum(
                source_file=fits_path.name,
                instrument=instrument,
                target_name=target,
                wavelength_um=np.array(wavelength),
                flux=np.array(flux),
                flux_error=np.array(flux_err) if flux_err is not None else None,
                exposure_time=exptime
            )

    except Exception as e:
        print(f"  Extraction error for {fits_path.name}: {e}")
        return None


# =============================================================================
# EMISSION LINE ISOLATION
# =============================================================================

def isolate_emission_line(
    spectrum: ExtractedSpectrum,
    line_name: str,
    redshift: float,
    window_um: float = 0.5
) -> Optional[Dict]:
    """
    Isolate a spectral region around a specific emission line.

    Args:
        spectrum: The extracted spectrum
        line_name: Name of the emission line (key in EMISSION_LINES)
        redshift: Redshift of the target
        window_um: Window size around the line (in μm)

    Returns:
        Dict with isolated wavelength and flux arrays, or None
    """
    if line_name not in EMISSION_LINES:
        print(f"  Unknown emission line: {line_name}")
        return None

    rest_wavelength = EMISSION_LINES[line_name]
    observed_wavelength = rest_wavelength * (1 + redshift)

    # Find indices within window
    mask = (
        (spectrum.wavelength_um >= observed_wavelength - window_um) &
        (spectrum.wavelength_um <= observed_wavelength + window_um)
    )

    if not np.any(mask):
        return None

    return {
        "line_name": line_name,
        "rest_wavelength_um": rest_wavelength,
        "observed_wavelength_um": observed_wavelength,
        "redshift": redshift,
        "wavelength_um": spectrum.wavelength_um[mask].tolist(),
        "flux": spectrum.flux[mask].tolist(),
        "flux_error": spectrum.flux_error[mask].tolist() if spectrum.flux_error is not None else None
    }


# =============================================================================
# PARQUET EXPORT FOR WEBGL
# =============================================================================

def export_to_parquet(
    spectra: List[ExtractedSpectrum],
    output_file: Path,
    downsample_factor: int = 1
) -> bool:
    """
    Export extracted spectra to Parquet format for WebGL frontend.

    Args:
        spectra: List of extracted spectra
        output_file: Output Parquet file path
        downsample_factor: Factor to reduce data size (1 = no downsampling)

    Returns:
        True if export successful
    """
    if not HAS_PYARROW:
        print("ERROR: pyarrow not installed. Cannot export to Parquet.")
        return False

    if not spectra:
        print("No spectra to export")
        return False

    # Build table data
    records = []

    for spec in spectra:
        # Downsample if requested
        wave = spec.wavelength_um[::downsample_factor]
        flux = spec.flux[::downsample_factor]

        records.append({
            "source_file": spec.source_file,
            "instrument": spec.instrument,
            "target_name": spec.target_name,
            "wavelength_um": wave.tolist(),
            "flux": flux.tolist(),
            "n_points": len(wave),
            "wave_min": float(wave.min()),
            "wave_max": float(wave.max()),
            "exposure_time": spec.exposure_time
        })

    # Create PyArrow table
    table = pa.Table.from_pylist(records)

    # Write with compression
    pq.write_table(
        table,
        output_file,
        compression='snappy'
    )

    print(f"Exported {len(spectra)} spectra to {output_file}")
    return True


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def process_ghost_location(
    ra: float,
    dec: float,
    target_name: str,
    expected_z: float,
    max_download_mb: float = 200.0
) -> Dict:
    """
    Full pipeline for a single ghost location.

    Args:
        ra, dec: Ghost coordinates
        target_name: Name of the original galaxy
        expected_z: Expected ghost redshift
        max_download_mb: Maximum data to download

    Returns:
        Results dictionary
    """
    print(f"\n{'='*70}")
    print(f"PROCESSING GHOST LOCATION: {target_name}")
    print(f"{'='*70}")
    print(f"Coordinates: RA={ra:.3f}°, Dec={dec:.3f}°")
    print(f"Expected z: {expected_z:.1f}")
    print(f"{'='*70}\n")

    results = {
        "target_name": target_name,
        "ghost_ra": ra,
        "ghost_dec": dec,
        "expected_z": expected_z,
        "products_found": 0,
        "products_downloaded": 0,
        "spectra_extracted": 0,
        "spectra": []
    }

    # Step 1: Search for products
    products = search_spectral_products(ra, dec)
    results["products_found"] = len(products)

    if not products:
        print("No spectral products found at this location")
        return results

    # Step 2: Download products
    downloaded = download_products(products, max_size_mb=max_download_mb)
    results["products_downloaded"] = len(downloaded)

    # Step 3: Extract spectra
    spectra = []
    for prod in downloaded:
        if prod.local_path and prod.local_path.exists():
            if prod.product_type == "X1D":
                spec = extract_spectrum_from_x1d(prod.local_path)
                if spec:
                    spectra.append(spec)

    results["spectra_extracted"] = len(spectra)

    # Step 4: Export to Parquet if we have spectra
    if spectra:
        parquet_file = SPECTRA_DIR / f"ghost_{target_name.replace(' ', '_')}.parquet"
        export_to_parquet(spectra, parquet_file)

        # Also save JSON version for debugging
        json_file = SPECTRA_DIR / f"ghost_{target_name.replace(' ', '_')}.json"
        with open(json_file, 'w') as f:
            json.dump([s.to_dict() for s in spectra], f, indent=2)

        results["spectra"] = [s.source_file for s in spectra]

    return results


def main():
    """Process all predicted ghost locations"""
    print("\n" + "="*70)
    print("FITS INGESTION PIPELINE (Directive JJJJ)")
    print("Downloading raw JWST spectral data for ghost candidates")
    print("="*70 + "\n")

    # Load ghost predictions
    predictions_file = Path(__file__).parent / "ghost_predictions.json"

    if not predictions_file.exists():
        print("ERROR: ghost_predictions.json not found!")
        print("Run ghost_miner.py first.")
        return

    with open(predictions_file) as f:
        predictions = json.load(f)

    print(f"Loaded {len(predictions)} ghost predictions\n")

    # Process each ghost location
    all_results = []

    for pred in predictions:
        original = pred["original"]
        ghost = pred["predicted_ghost"]

        result = process_ghost_location(
            ra=ghost["ra"],
            dec=ghost["dec"],
            target_name=original["name"],
            expected_z=ghost["expected_redshift"],
            max_download_mb=100.0  # Limit per target
        )

        all_results.append(result)

    # Save summary
    summary_file = DATA_CACHE_DIR / "ingestion_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    # Print summary
    print("\n" + "="*70)
    print("INGESTION COMPLETE")
    print("="*70)

    total_products = sum(r["products_found"] for r in all_results)
    total_downloaded = sum(r["products_downloaded"] for r in all_results)
    total_spectra = sum(r["spectra_extracted"] for r in all_results)

    print(f"Total products found: {total_products}")
    print(f"Total downloaded: {total_downloaded}")
    print(f"Total spectra extracted: {total_spectra}")
    print(f"Results saved to: {summary_file}")


if __name__ == "__main__":
    main()
