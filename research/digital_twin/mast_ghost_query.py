#!/usr/bin/env python3
"""
=============================================================================
MAST GHOST QUERY (Directive EEEE)
=============================================================================
Queries astronomical archives at predicted topological ghost coordinates
to find potential T³/Z₂ duplicate images.

Uses astroquery for reliable API access to:
1. MAST (JWST, HST observations)
2. SIMBAD (known objects)
3. NED (extragalactic database)

Author: Carl Zimmerman / Claude
=============================================================================
"""

import json
import time
import warnings
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Suppress astropy warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Astroquery imports
from astroquery.mast import Observations, Catalogs
from astroquery.simbad import Simbad
from astroquery.ipac.ned import Ned
from astropy.coordinates import SkyCoord
import astropy.units as u

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_SEARCH_RADIUS_ARCMIN = 10.0  # 10 arcminutes


# =============================================================================
# MAST QUERY FUNCTIONS
# =============================================================================

def search_mast_observations(ra: float, dec: float, radius_arcmin: float = DEFAULT_SEARCH_RADIUS_ARCMIN) -> dict:
    """
    Search for MAST observations at given coordinates.

    Returns dict with observation counts and details.
    """
    print(f"  Querying MAST observations at RA={ra:.3f}°, Dec={dec:.3f}°...")

    try:
        coord = SkyCoord(ra=ra, dec=dec, unit="deg")

        # Query CAOM (Common Archive Observation Model)
        obs_table = Observations.query_region(
            coord,
            radius=radius_arcmin * u.arcmin
        )

        if obs_table is None or len(obs_table) == 0:
            print(f"    No observations found")
            return {
                "total": 0,
                "jwst": 0,
                "hst": 0,
                "jwst_programs": [],
                "jwst_instruments": [],
                "observations": []
            }

        # Convert to list of dicts for easier processing
        obs_list = []
        for row in obs_table:
            obs_list.append({
                "obs_id": str(row["obs_id"]) if "obs_id" in row.colnames else None,
                "obs_collection": str(row["obs_collection"]) if "obs_collection" in row.colnames else None,
                "instrument_name": str(row["instrument_name"]) if "instrument_name" in row.colnames else None,
                "target_name": str(row["target_name"]) if "target_name" in row.colnames else None,
                "proposal_id": str(row["proposal_id"]) if "proposal_id" in row.colnames else None,
                "filters": str(row["filters"]) if "filters" in row.colnames else None,
            })

        # Filter by telescope
        jwst_obs = [o for o in obs_list if o.get("obs_collection") == "JWST"]
        hst_obs = [o for o in obs_list if o.get("obs_collection") == "HST"]

        # Get unique JWST programs
        jwst_programs = list(set(o["proposal_id"] for o in jwst_obs if o.get("proposal_id")))
        jwst_instruments = list(set(o["instrument_name"] for o in jwst_obs if o.get("instrument_name")))

        print(f"    Found {len(obs_list)} total, {len(jwst_obs)} JWST, {len(hst_obs)} HST")

        return {
            "total": len(obs_list),
            "jwst": len(jwst_obs),
            "hst": len(hst_obs),
            "jwst_programs": jwst_programs,
            "jwst_instruments": jwst_instruments,
            "observations": obs_list[:50]  # Limit stored observations
        }

    except Exception as e:
        print(f"    MAST query error: {e}")
        return {
            "total": 0,
            "jwst": 0,
            "hst": 0,
            "jwst_programs": [],
            "jwst_instruments": [],
            "observations": [],
            "error": str(e)
        }


def search_hubble_catalog(ra: float, dec: float, radius_arcmin: float = DEFAULT_SEARCH_RADIUS_ARCMIN) -> dict:
    """
    Search Hubble Source Catalog v3 for sources.
    """
    print(f"  Querying Hubble Source Catalog...")

    try:
        coord = SkyCoord(ra=ra, dec=dec, unit="deg")

        # Query HSC
        catalog_data = Catalogs.query_region(
            coord,
            radius=radius_arcmin * u.arcmin,
            catalog="HSC",
            version=3
        )

        if catalog_data is None or len(catalog_data) == 0:
            print(f"    No HSC sources found")
            return {"count": 0, "sources": []}

        print(f"    Found {len(catalog_data)} HSC sources")

        # Extract key info
        sources = []
        for i, row in enumerate(catalog_data[:20]):  # Limit to 20
            sources.append({
                "MatchRA": float(row["MatchRA"]) if "MatchRA" in row.colnames else None,
                "MatchDec": float(row["MatchDec"]) if "MatchDec" in row.colnames else None,
                "CI": float(row["CI"]) if "CI" in row.colnames else None,  # Concentration index
            })

        return {"count": len(catalog_data), "sources": sources}

    except Exception as e:
        print(f"    HSC query error: {e}")
        return {"count": 0, "sources": [], "error": str(e)}


def search_simbad(ra: float, dec: float, radius_arcmin: float = DEFAULT_SEARCH_RADIUS_ARCMIN) -> dict:
    """
    Query SIMBAD for known objects at coordinates.
    """
    print(f"  Querying SIMBAD...")

    try:
        # Configure SIMBAD to return extra fields
        custom_simbad = Simbad()
        custom_simbad.add_votable_fields('otype', 'z_value', 'sptype')

        coord = SkyCoord(ra=ra, dec=dec, unit="deg")

        result = custom_simbad.query_region(
            coord,
            radius=radius_arcmin * u.arcmin
        )

        if result is None or len(result) == 0:
            print(f"    No SIMBAD objects found")
            return {"count": 0, "objects": [], "galaxies": 0, "with_redshift": 0}

        print(f"    Found {len(result)} SIMBAD objects")

        # Extract objects
        objects = []
        galaxies = 0
        with_redshift = 0

        for row in result:
            obj = {
                "main_id": str(row["MAIN_ID"]) if "MAIN_ID" in row.colnames else None,
                "otype": str(row["OTYPE"]) if "OTYPE" in row.colnames else None,
                "z_value": float(row["Z_VALUE"]) if "Z_VALUE" in row.colnames and row["Z_VALUE"] else None,
            }
            objects.append(obj)

            otype = str(obj.get("otype", "")).lower()
            if "galaxy" in otype or "g" == otype or otype.startswith("g"):
                galaxies += 1
            if obj.get("z_value"):
                with_redshift += 1

        return {
            "count": len(result),
            "objects": objects[:30],  # Limit stored
            "galaxies": galaxies,
            "with_redshift": with_redshift
        }

    except Exception as e:
        print(f"    SIMBAD query error: {e}")
        return {"count": 0, "objects": [], "galaxies": 0, "with_redshift": 0, "error": str(e)}


def search_ned(ra: float, dec: float, radius_arcmin: float = DEFAULT_SEARCH_RADIUS_ARCMIN) -> dict:
    """
    Query NED for extragalactic objects with redshifts.
    """
    print(f"  Querying NED...")

    try:
        coord = SkyCoord(ra=ra, dec=dec, unit="deg")

        result = Ned.query_region(
            coord,
            radius=radius_arcmin * u.arcmin
        )

        if result is None or len(result) == 0:
            print(f"    No NED objects found")
            return {"count": 0, "objects": [], "with_redshift": 0, "highz": []}

        print(f"    Found {len(result)} NED objects")

        # Extract objects, focusing on those with redshifts
        objects = []
        with_redshift = 0
        highz = []

        for row in result:
            obj = {
                "name": str(row["Object Name"]) if "Object Name" in row.colnames else None,
                "type": str(row["Type"]) if "Type" in row.colnames else None,
                "redshift": float(row["Redshift"]) if "Redshift" in row.colnames and row["Redshift"] else None,
            }
            objects.append(obj)

            if obj.get("redshift"):
                with_redshift += 1
                if obj["redshift"] > 5:
                    highz.append(obj)

        # Sort high-z by redshift
        highz.sort(key=lambda x: x.get("redshift", 0), reverse=True)

        print(f"    Objects with z: {with_redshift}, High-z (z>5): {len(highz)}")

        return {
            "count": len(result),
            "objects": objects[:30],
            "with_redshift": with_redshift,
            "highz": highz
        }

    except Exception as e:
        print(f"    NED query error: {e}")
        return {"count": 0, "objects": [], "with_redshift": 0, "highz": [], "error": str(e)}


# =============================================================================
# GHOST SEARCH
# =============================================================================

def search_ghost_location(
    original_name: str,
    ghost_ra: float,
    ghost_dec: float,
    expected_z: float,
    search_radius_arcmin: float = DEFAULT_SEARCH_RADIUS_ARCMIN
) -> dict:
    """
    Comprehensive search at a predicted ghost location.
    """
    print(f"\n{'='*70}")
    print(f"SEARCHING FOR GHOST OF: {original_name}")
    print(f"{'='*70}")
    print(f"Predicted Location: RA={ghost_ra:.3f}°, Dec={ghost_dec:.3f}°")
    print(f"Expected Redshift: z≈{expected_z:.1f}")
    print(f"Search Radius: {search_radius_arcmin} arcmin")
    print(f"{'='*70}\n")

    # Run all searches
    mast_results = search_mast_observations(ghost_ra, ghost_dec, search_radius_arcmin)
    time.sleep(1)  # Rate limiting

    hsc_results = search_hubble_catalog(ghost_ra, ghost_dec, search_radius_arcmin)
    time.sleep(1)

    simbad_results = search_simbad(ghost_ra, ghost_dec, search_radius_arcmin)
    time.sleep(1)

    ned_results = search_ned(ghost_ra, ghost_dec, search_radius_arcmin)

    # Assess potential match
    potential_match = False
    match_notes = []
    priority = "LOW"

    # Check for JWST coverage
    if mast_results["jwst"] > 0:
        match_notes.append(f"✓ JWST has observed this region ({mast_results['jwst']} observations)")
        match_notes.append(f"  Programs: {', '.join(mast_results['jwst_programs'][:5])}")
        match_notes.append(f"  Instruments: {', '.join(mast_results['jwst_instruments'])}")
        priority = "MEDIUM"

        # Check for NIRSpec (spectroscopy)
        if any("NIRSPEC" in inst.upper() for inst in mast_results["jwst_instruments"]):
            match_notes.append(f"  ★ NIRSpec spectroscopy available!")
            priority = "HIGH"
    else:
        match_notes.append("✗ No JWST observations at this location")

    # Check for HST coverage
    if mast_results["hst"] > 0:
        match_notes.append(f"✓ HST coverage ({mast_results['hst']} observations)")

    # Check for high-z in NED
    if ned_results["highz"]:
        potential_match = True
        priority = "CRITICAL"
        match_notes.append(f"★★★ HIGH-Z CANDIDATES FOUND: {len(ned_results['highz'])} objects with z>5!")
        for obj in ned_results["highz"][:5]:
            match_notes.append(f"    → {obj['name']}: z={obj['redshift']:.2f}")

    # Check SIMBAD for known galaxies
    if simbad_results["galaxies"] > 0:
        match_notes.append(f"Known galaxies in region: {simbad_results['galaxies']}")
        if simbad_results["with_redshift"] > 0:
            match_notes.append(f"  Objects with redshift: {simbad_results['with_redshift']}")

    # Print summary
    print(f"\n--- SEARCH SUMMARY ---")
    print(f"Priority: {priority}")
    print(f"Potential Match: {'YES' if potential_match else 'No'}")
    print(f"\nNotes:")
    for note in match_notes:
        print(f"  {note}")

    return {
        "original_galaxy": original_name,
        "ghost_ra": ghost_ra,
        "ghost_dec": ghost_dec,
        "expected_z": expected_z,
        "mast": mast_results,
        "hsc": hsc_results,
        "simbad": simbad_results,
        "ned": ned_results,
        "potential_match": potential_match,
        "priority": priority,
        "match_notes": match_notes
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Query all archives at predicted ghost coordinates"""

    print("\n" + "="*70)
    print("T³/Z₂ GHOST HUNTER - ARCHIVE QUERY")
    print("Searching for topological duplicates in existing data")
    print("="*70 + "\n")

    # Load predictions
    predictions_file = Path(__file__).parent / "ghost_predictions.json"

    if not predictions_file.exists():
        print("ERROR: ghost_predictions.json not found!")
        print("Run ghost_miner.py first to generate predictions.")
        return

    with open(predictions_file) as f:
        predictions = json.load(f)

    print(f"Loaded {len(predictions)} ghost predictions\n")

    # Sort by expected redshift (lower z = more likely observable)
    predictions.sort(key=lambda p: p["predicted_ghost"]["expected_redshift"])

    results = []

    for pred in predictions:
        original = pred["original"]
        ghost = pred["predicted_ghost"]

        # Search at ghost coordinates
        result = search_ghost_location(
            original_name=original["name"],
            ghost_ra=ghost["ra"],
            ghost_dec=ghost["dec"],
            expected_z=ghost["expected_redshift"],
            search_radius_arcmin=10.0
        )

        results.append({
            "original": original,
            "predicted_ghost": ghost,
            "search_results": result
        })

        # Rate limiting between targets
        time.sleep(2)

    # Save results
    output_file = Path(__file__).parent / "mast_ghost_search_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n\n{'='*70}")
    print("GHOST SEARCH COMPLETE")
    print(f"{'='*70}")
    print(f"Results saved to: {output_file}")

    # Print summary table
    print(f"\n{'='*70}")
    print("SUMMARY TABLE")
    print(f"{'='*70}")
    print(f"{'Galaxy':<25} {'Ghost z':<8} {'JWST':<6} {'NED':<6} {'Priority':<10}")
    print("-" * 70)

    for r in results:
        name = r["original"]["name"][:24]
        ghost_z = r["predicted_ghost"]["expected_redshift"]
        jwst = r["search_results"]["mast"]["jwst"]
        ned = r["search_results"]["ned"]["count"]
        priority = r["search_results"]["priority"]
        print(f"{name:<25} {ghost_z:<8.1f} {jwst:<6} {ned:<6} {priority:<10}")

    # Highlight high-priority targets
    high_priority = [r for r in results if r["search_results"]["priority"] in ["HIGH", "CRITICAL"]]
    if high_priority:
        print(f"\n{'='*70}")
        print("★★★ HIGH PRIORITY TARGETS FOR GHOST HUNTING ★★★")
        print(f"{'='*70}")
        for r in high_priority:
            print(f"\n{r['original']['name']}:")
            print(f"  Ghost at: RA={r['predicted_ghost']['ra']:.2f}°, Dec={r['predicted_ghost']['dec']:.2f}°")
            print(f"  Expected z: {r['predicted_ghost']['expected_redshift']:.1f}")
            print(f"  Priority: {r['search_results']['priority']}")
            for note in r["search_results"]["match_notes"]:
                print(f"  {note}")

    # Summary stats
    print(f"\n{'='*70}")
    print("STATISTICS")
    print(f"{'='*70}")
    jwst_coverage = sum(1 for r in results if r["search_results"]["mast"]["jwst"] > 0)
    potential_matches = sum(1 for r in results if r["search_results"]["potential_match"])
    print(f"Ghost locations with JWST coverage: {jwst_coverage}/{len(results)}")
    print(f"Potential matches (z>5 objects found): {potential_matches}/{len(results)}")


if __name__ == "__main__":
    main()
