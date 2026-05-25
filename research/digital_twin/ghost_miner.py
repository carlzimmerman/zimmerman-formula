#!/usr/bin/env python3
"""
=============================================================================
TOPOLOGICAL GHOST MINER (Directive DDDD)
=============================================================================
Searches existing astronomical catalogs for topological ghost pairs in T³/Z₂

In the T³/Z₂ orbifold with L_c = 20.6 Gpc:
- Points p and -p are identified (Z₂ involution)
- Galaxies can have "ghost images" at antipodal positions
- D₁ + D₂ ≈ 20.6 Gpc (fundamental domain constraint)
- Ghosts share "cosmic DNA" but appear at different evolutionary stages

Author: Carl Zimmerman / Claude
=============================================================================
"""

import numpy as np
import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple
from pathlib import Path
import requests
from scipy.integrate import quad

# =============================================================================
# COSMOLOGICAL PARAMETERS (Planck 2018)
# =============================================================================

H0 = 67.4  # km/s/Mpc
OMEGA_M = 0.315
OMEGA_LAMBDA = 0.685
C_KM_S = 299792.458  # km/s

# Fundamental domain size
L_C_GPC = 20.6  # Gpc
L_C_MPC = L_C_GPC * 1000  # Mpc

# Matching tolerances
DISTANCE_TOLERANCE_GPC = 1.0  # Allow ±1 Gpc deviation from exact sum
ANGULAR_TOLERANCE_DEG = 5.0  # Allow ±5° deviation from exact antipodal
REDSHIFT_TOLERANCE = 0.5  # Allow some redshift uncertainty


# =============================================================================
# COMOVING DISTANCE CALCULATOR
# =============================================================================

def E(z: float) -> float:
    """Hubble parameter evolution E(z) = H(z)/H0"""
    return np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_LAMBDA)


def comoving_distance_mpc(z: float) -> float:
    """
    Calculate comoving distance in Mpc for a given redshift.
    D_c = (c/H0) * integral_0^z dz'/E(z')
    """
    if z <= 0:
        return 0.0

    integrand = lambda zp: 1.0 / E(zp)
    result, _ = quad(integrand, 0, z)

    # Convert to Mpc
    d_h = C_KM_S / H0  # Hubble distance in Mpc
    return d_h * result


def comoving_distance_gpc(z: float) -> float:
    """Calculate comoving distance in Gpc"""
    return comoving_distance_mpc(z) / 1000.0


def redshift_from_distance_gpc(d_gpc: float, z_min: float = 0.0, z_max: float = 30.0) -> float:
    """
    Invert the distance-redshift relation to find z from comoving distance.
    Uses binary search for efficiency.
    """
    if d_gpc <= 0:
        return 0.0

    # Binary search
    for _ in range(100):  # Max iterations
        z_mid = (z_min + z_max) / 2
        d_mid = comoving_distance_gpc(z_mid)

        if abs(d_mid - d_gpc) < 0.001:  # Converged
            return z_mid
        elif d_mid < d_gpc:
            z_min = z_mid
        else:
            z_max = z_mid

    return (z_min + z_max) / 2


# =============================================================================
# ANTIPODAL COORDINATE CALCULATOR
# =============================================================================

def antipodal_coordinates(ra: float, dec: float) -> Tuple[float, float]:
    """
    Calculate the antipodal (Z₂ inverted) sky coordinates.

    In T³/Z₂, the involution maps:
    - RA → RA + 180°
    - Dec → -Dec

    Args:
        ra: Right Ascension in degrees [0, 360)
        dec: Declination in degrees [-90, 90]

    Returns:
        (antipodal_ra, antipodal_dec)
    """
    anti_ra = (ra + 180.0) % 360.0
    anti_dec = -dec
    return (anti_ra, anti_dec)


def angular_separation(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """
    Calculate angular separation between two sky positions in degrees.
    Uses the Haversine formula.
    """
    ra1_rad = np.radians(ra1)
    dec1_rad = np.radians(dec1)
    ra2_rad = np.radians(ra2)
    dec2_rad = np.radians(dec2)

    delta_ra = ra2_rad - ra1_rad
    delta_dec = dec2_rad - dec1_rad

    a = np.sin(delta_dec/2)**2 + np.cos(dec1_rad) * np.cos(dec2_rad) * np.sin(delta_ra/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return np.degrees(c)


# =============================================================================
# GALAXY DATA STRUCTURES
# =============================================================================

@dataclass
class Galaxy:
    """Represents a galaxy from a catalog"""
    id: str
    name: str
    ra: float  # degrees
    dec: float  # degrees
    redshift: float
    comoving_distance_gpc: float

    # Spectroscopic properties (for fingerprint matching)
    has_oiii_88um: bool = False
    has_niv: bool = False
    has_civ: bool = False
    has_heii: bool = False
    has_halpha: bool = False
    metallicity: Optional[float] = None

    # Source catalog
    catalog: str = "unknown"

    def __post_init__(self):
        """Calculate comoving distance if not provided"""
        if self.comoving_distance_gpc == 0 and self.redshift > 0:
            self.comoving_distance_gpc = comoving_distance_gpc(self.redshift)


@dataclass
class GhostCandidate:
    """A pair of galaxies that may be topological ghosts of each other"""
    galaxy_a: Galaxy  # Lower redshift (the "adult")
    galaxy_b: Galaxy  # Higher redshift (the "baby")

    # Geometric match quality
    angular_separation_from_antipodal: float  # degrees
    distance_sum_gpc: float  # Should be ~20.6
    distance_deviation_gpc: float  # |D1 + D2 - 20.6|

    # Spectral match quality
    chemical_match_score: float  # 0-1
    matching_lines: List[str]

    # Overall confidence
    confidence: float  # 0-1

    def to_dict(self):
        return {
            "galaxy_a": asdict(self.galaxy_a),
            "galaxy_b": asdict(self.galaxy_b),
            "angular_separation_from_antipodal": self.angular_separation_from_antipodal,
            "distance_sum_gpc": self.distance_sum_gpc,
            "distance_deviation_gpc": self.distance_deviation_gpc,
            "chemical_match_score": self.chemical_match_score,
            "matching_lines": self.matching_lines,
            "confidence": self.confidence
        }


# =============================================================================
# KNOWN HIGH-Z GALAXIES (JWST ERA)
# =============================================================================

def get_known_highz_galaxies() -> List[Galaxy]:
    """
    Return a list of known high-redshift galaxies from JWST observations.
    These are prime candidates for ghost hunting.
    """
    return [
        Galaxy(
            id="GLASS-z12",
            name="GHZ2/GLASS-z12",
            ra=3.5,
            dec=-30.4,
            redshift=12.34,
            comoving_distance_gpc=0,  # Will be calculated
            has_oiii_88um=True,
            has_niv=True,
            has_civ=True,
            has_heii=True,
            has_halpha=True,
            catalog="JWST-GLASS"
        ),
        Galaxy(
            id="JADES-GS-z14-0",
            name="JADES-GS-z14-0",
            ra=53.16,
            dec=-27.77,
            redshift=14.32,
            comoving_distance_gpc=0,
            has_oiii_88um=False,
            catalog="JWST-JADES"
        ),
        Galaxy(
            id="JADES-GS-z13-0",
            name="JADES-GS-z13-0",
            ra=53.15,
            dec=-27.82,
            redshift=13.2,
            comoving_distance_gpc=0,
            catalog="JWST-JADES"
        ),
        Galaxy(
            id="GN-z11",
            name="GN-z11",
            ra=189.1,
            dec=62.24,
            redshift=10.6,
            comoving_distance_gpc=0,
            has_niv=True,
            has_civ=True,
            catalog="HST+JWST"
        ),
        Galaxy(
            id="CEERS-93316",
            name="Maisie's Galaxy",
            ra=214.82,
            dec=52.88,
            redshift=11.4,
            comoving_distance_gpc=0,
            catalog="JWST-CEERS"
        ),
        Galaxy(
            id="UNCOVER-z13",
            name="UNCOVER-z13",
            ra=3.59,
            dec=-30.42,
            redshift=12.79,
            comoving_distance_gpc=0,
            catalog="JWST-UNCOVER"
        ),
        Galaxy(
            id="RXCJ2248-ID",
            name="RXCJ2248-ID",
            ra=342.17,
            dec=-44.53,
            redshift=9.51,
            comoving_distance_gpc=0,
            catalog="JWST"
        ),
        Galaxy(
            id="S5-z17-1",
            name="S5-z17-1 (candidate)",
            ra=53.12,
            dec=-27.85,
            redshift=16.7,  # Photometric, needs confirmation
            comoving_distance_gpc=0,
            catalog="JWST-JADES"
        ),
    ]


# =============================================================================
# GHOST HUNTING ALGORITHM
# =============================================================================

def find_ghost_candidates(
    target_galaxy: Galaxy,
    catalog: List[Galaxy],
    distance_tolerance: float = DISTANCE_TOLERANCE_GPC,
    angular_tolerance: float = ANGULAR_TOLERANCE_DEG
) -> List[GhostCandidate]:
    """
    Search a catalog for potential ghost images of a target galaxy.

    The algorithm:
    1. Calculate the antipodal coordinates of the target
    2. Calculate the expected ghost distance: D_ghost = L_c - D_target
    3. Search for galaxies near the antipodal position with matching distance
    4. Score chemical fingerprint matches

    Args:
        target_galaxy: The galaxy to find ghosts of
        catalog: List of galaxies to search
        distance_tolerance: How close D1 + D2 must be to 20.6 Gpc
        angular_tolerance: How close to exact antipodal position (degrees)

    Returns:
        List of GhostCandidate pairs, sorted by confidence
    """
    candidates = []

    # Calculate target properties
    target_d = target_galaxy.comoving_distance_gpc
    anti_ra, anti_dec = antipodal_coordinates(target_galaxy.ra, target_galaxy.dec)
    expected_ghost_d = L_C_GPC - target_d

    print(f"\n{'='*60}")
    print(f"GHOST HUNT: {target_galaxy.name}")
    print(f"{'='*60}")
    print(f"Position: RA={target_galaxy.ra:.2f}°, Dec={target_galaxy.dec:.2f}°")
    print(f"Redshift: z={target_galaxy.redshift:.2f}")
    print(f"Comoving Distance: {target_d:.2f} Gpc")
    print(f"Antipodal Position: RA={anti_ra:.2f}°, Dec={anti_dec:.2f}°")
    print(f"Expected Ghost Distance: {expected_ghost_d:.2f} Gpc")
    print(f"Expected Ghost Redshift: z≈{redshift_from_distance_gpc(expected_ghost_d):.1f}")
    print(f"{'='*60}\n")

    for candidate in catalog:
        # Skip self
        if candidate.id == target_galaxy.id:
            continue

        # Check angular proximity to antipodal position
        ang_sep = angular_separation(anti_ra, anti_dec, candidate.ra, candidate.dec)

        if ang_sep > angular_tolerance:
            continue

        # Check distance constraint
        distance_sum = target_d + candidate.comoving_distance_gpc
        distance_deviation = abs(distance_sum - L_C_GPC)

        if distance_deviation > distance_tolerance:
            continue

        # Calculate chemical match score
        match_score, matching_lines = calculate_chemical_match(target_galaxy, candidate)

        # Calculate overall confidence
        # Weight factors: geometry (60%), chemistry (40%)
        geometric_score = 1.0 - (distance_deviation / distance_tolerance)
        angular_score = 1.0 - (ang_sep / angular_tolerance)

        confidence = 0.3 * geometric_score + 0.3 * angular_score + 0.4 * match_score

        ghost = GhostCandidate(
            galaxy_a=target_galaxy if target_galaxy.redshift < candidate.redshift else candidate,
            galaxy_b=candidate if target_galaxy.redshift < candidate.redshift else target_galaxy,
            angular_separation_from_antipodal=ang_sep,
            distance_sum_gpc=distance_sum,
            distance_deviation_gpc=distance_deviation,
            chemical_match_score=match_score,
            matching_lines=matching_lines,
            confidence=confidence
        )

        candidates.append(ghost)

        print(f"CANDIDATE FOUND: {candidate.name}")
        print(f"  Position: RA={candidate.ra:.2f}°, Dec={candidate.dec:.2f}°")
        print(f"  Angular separation from antipodal: {ang_sep:.2f}°")
        print(f"  Distance: {candidate.comoving_distance_gpc:.2f} Gpc, z={candidate.redshift:.2f}")
        print(f"  D1 + D2 = {distance_sum:.2f} Gpc (deviation: {distance_deviation:.2f} Gpc)")
        print(f"  Chemical match: {match_score:.1%}, lines: {matching_lines}")
        print(f"  CONFIDENCE: {confidence:.1%}")
        print()

    # Sort by confidence
    candidates.sort(key=lambda x: x.confidence, reverse=True)

    return candidates


def calculate_chemical_match(galaxy_a: Galaxy, galaxy_b: Galaxy) -> Tuple[float, List[str]]:
    """
    Calculate chemical fingerprint match between two galaxies.

    In T³/Z₂, ghost images are the same galaxy at different evolutionary stages,
    so they should share characteristic emission lines and metallicity patterns.

    Returns:
        (match_score, list_of_matching_features)
    """
    matching_lines = []
    total_features = 0
    matches = 0

    # Check emission line matches
    line_features = [
        ('has_oiii_88um', '[O III] 88μm'),
        ('has_niv', 'N IV'),
        ('has_civ', 'C IV'),
        ('has_heii', 'He II'),
        ('has_halpha', 'Hα'),
    ]

    for attr, name in line_features:
        a_has = getattr(galaxy_a, attr)
        b_has = getattr(galaxy_b, attr)

        if a_has or b_has:
            total_features += 1
            if a_has and b_has:
                matches += 1
                matching_lines.append(name)

    # Calculate score
    if total_features == 0:
        # No spectral data available
        return 0.5, ["No spectral data"]

    match_score = matches / total_features

    return match_score, matching_lines


# =============================================================================
# FULL CATALOG SWEEP
# =============================================================================

def sweep_all_pairs(catalog: List[Galaxy]) -> List[GhostCandidate]:
    """
    Sweep all pairs in a catalog to find potential ghost matches.
    This is O(n²) but necessary for comprehensive search.
    """
    all_candidates = []

    print("\n" + "="*70)
    print("FULL CATALOG SWEEP FOR TOPOLOGICAL GHOST PAIRS")
    print("="*70)
    print(f"Catalog size: {len(catalog)} galaxies")
    print(f"Fundamental domain: L_c = {L_C_GPC} Gpc")
    print(f"Distance tolerance: ±{DISTANCE_TOLERANCE_GPC} Gpc")
    print(f"Angular tolerance: ±{ANGULAR_TOLERANCE_DEG}°")
    print("="*70 + "\n")

    for target in catalog:
        candidates = find_ghost_candidates(target, catalog)
        all_candidates.extend(candidates)

    # Remove duplicates (A-B is same as B-A)
    unique_pairs = {}
    for c in all_candidates:
        key = tuple(sorted([c.galaxy_a.id, c.galaxy_b.id]))
        if key not in unique_pairs or c.confidence > unique_pairs[key].confidence:
            unique_pairs[key] = c

    unique_candidates = list(unique_pairs.values())
    unique_candidates.sort(key=lambda x: x.confidence, reverse=True)

    return unique_candidates


# =============================================================================
# PREDICT GHOST LOCATION
# =============================================================================

def predict_ghost_location(galaxy: Galaxy) -> dict:
    """
    For a given galaxy, predict exactly where its topological ghost should be.
    This can be used to target new observations.
    """
    # Calculate ghost position
    ghost_ra, ghost_dec = antipodal_coordinates(galaxy.ra, galaxy.dec)

    # Calculate ghost distance
    ghost_distance = L_C_GPC - galaxy.comoving_distance_gpc

    # Calculate ghost redshift
    ghost_redshift = redshift_from_distance_gpc(ghost_distance)

    # Calculate light travel time difference
    # This tells us how much younger/older the ghost appears
    lookback_direct = galaxy.redshift  # Approximate
    lookback_wrapped = ghost_redshift

    prediction = {
        "original": {
            "name": galaxy.name,
            "ra": galaxy.ra,
            "dec": galaxy.dec,
            "redshift": galaxy.redshift,
            "comoving_distance_gpc": galaxy.comoving_distance_gpc
        },
        "predicted_ghost": {
            "ra": ghost_ra,
            "dec": ghost_dec,
            "expected_redshift": ghost_redshift,
            "expected_distance_gpc": ghost_distance,
            "search_radius_deg": ANGULAR_TOLERANCE_DEG,
            "redshift_range": [ghost_redshift - REDSHIFT_TOLERANCE, ghost_redshift + REDSHIFT_TOLERANCE]
        },
        "interpretation": {
            "distance_sum": galaxy.comoving_distance_gpc + ghost_distance,
            "ghost_appears_younger": ghost_redshift > galaxy.redshift,
            "notes": f"Ghost should show Z₂ parity inversion (mirrored morphology)"
        }
    }

    return prediction


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Run the ghost mining algorithm on known high-z galaxies"""

    print("\n" + "="*70)
    print("T³/Z₂ TOPOLOGICAL GHOST MINER")
    print("Searching for duplicate images of galaxies in the cosmic topology")
    print("="*70 + "\n")

    # Get known high-z galaxies
    high_z_galaxies = get_known_highz_galaxies()

    # Calculate comoving distances
    for g in high_z_galaxies:
        g.comoving_distance_gpc = comoving_distance_gpc(g.redshift)
        print(f"{g.name}: z={g.redshift:.2f} → D_c={g.comoving_distance_gpc:.2f} Gpc")

    print("\n")

    # Generate predictions for each galaxy
    predictions = []
    for galaxy in high_z_galaxies:
        pred = predict_ghost_location(galaxy)
        predictions.append(pred)

        print(f"\n--- GHOST PREDICTION: {galaxy.name} ---")
        print(f"Original: RA={galaxy.ra:.2f}°, Dec={galaxy.dec:.2f}°, z={galaxy.redshift:.2f}")
        print(f"Ghost Location: RA={pred['predicted_ghost']['ra']:.2f}°, Dec={pred['predicted_ghost']['dec']:.2f}°")
        print(f"Expected Ghost z: {pred['predicted_ghost']['expected_redshift']:.1f}")
        print(f"Search Window: ±{ANGULAR_TOLERANCE_DEG}° radius, z={pred['predicted_ghost']['redshift_range'][0]:.1f}-{pred['predicted_ghost']['redshift_range'][1]:.1f}")

    # Sweep for self-matches within the catalog
    print("\n\n")
    candidates = sweep_all_pairs(high_z_galaxies)

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Galaxies analyzed: {len(high_z_galaxies)}")
    print(f"Ghost candidates found: {len(candidates)}")

    if candidates:
        print("\nTop candidates:")
        for i, c in enumerate(candidates[:5], 1):
            print(f"  {i}. {c.galaxy_a.name} ↔ {c.galaxy_b.name}")
            print(f"     Confidence: {c.confidence:.1%}")
            print(f"     D1+D2 = {c.distance_sum_gpc:.2f} Gpc")

    # Save results
    output_dir = Path(__file__).parent

    # Save predictions
    predictions_file = output_dir / "ghost_predictions.json"
    with open(predictions_file, 'w') as f:
        json.dump(predictions, f, indent=2)
    print(f"\nPredictions saved to: {predictions_file}")

    # Save candidates
    candidates_file = output_dir / "ghost_candidates.json"
    with open(candidates_file, 'w') as f:
        json.dump([c.to_dict() for c in candidates], f, indent=2)
    print(f"Candidates saved to: {candidates_file}")

    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("1. Query JWST MAST archive at predicted ghost coordinates")
    print("2. Cross-match with DESI/SDSS for lower-z counterparts")
    print("3. Compare emission line spectra for chemical fingerprints")
    print("4. Look for Z₂ parity inversion in galaxy morphology")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
