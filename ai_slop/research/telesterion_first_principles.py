#!/usr/bin/env python3
"""
Telesterion First-Principles Analysis
======================================

A RIGOROUS acoustic analysis that:
1. Clearly separates KNOWN facts from ASSUMPTIONS
2. Propagates uncertainties through all calculations
3. Reports confidence intervals, not point estimates
4. Makes NO claims beyond what physics supports

Author: Carl Zimmerman
Date: April 28, 2026

METHODOLOGY:
- Tier 1 (KNOWN): Archaeological measurements, established physics
- Tier 2 (ESTIMATED): Reasonable inferences with stated uncertainty
- Tier 3 (HYPOTHETICAL): Speculative but testable claims (clearly marked)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional
import json

# =============================================================================
# TIER 1: KNOWN FACTS (Archaeological/Physical Constants)
# =============================================================================

@dataclass
class KnownFacts:
    """
    ONLY values with direct archaeological or physical evidence.
    Each value includes its source and confidence level.
    """

    # Floor dimensions - WELL DOCUMENTED
    # Sources: Mylonas excavations, Perseus Digital Library, EFADA
    floor_length_m: float = 51.5
    floor_width_m: float = 51.5
    floor_dimension_uncertainty_m: float = 0.5  # ±0.5m based on source variation
    floor_confidence: str = "HIGH - multiple independent archaeological sources"

    # Column count - WELL DOCUMENTED
    num_columns: int = 42
    column_arrangement: str = "6 rows × 7 columns"
    column_confidence: str = "HIGH - visible in ruins, multiple sources agree"

    # Capacity estimates - DOCUMENTED but range
    capacity_min: int = 3000
    capacity_max: int = 5000
    capacity_confidence: str = "MEDIUM - archaeological estimates, not census data"

    # Materials - DOCUMENTED
    wall_material: str = "marble/limestone"
    floor_material: str = "stone"
    roof_material: str = "wood (destroyed)"
    material_confidence: str = "HIGH for walls/floor, MEDIUM for roof type"

    # Physical constants - ESTABLISHED PHYSICS
    speed_of_sound_20C: float = 343.0  # m/s
    speed_of_sound_coefficient: float = 0.606  # m/s per °C
    air_density_20C: float = 1.2  # kg/m³
    physics_confidence: str = "HIGH - textbook physics"


@dataclass
class EstimatedParameters:
    """
    TIER 2: Values inferred from evidence but with significant uncertainty.
    Each includes explicit uncertainty bounds and reasoning.
    """

    # Ceiling height - NO DIRECT EVIDENCE
    # Reasoning: Based on column proportions (Doric 6:1 to 8:1 height:diameter)
    # and structural requirements for spanning 51.5m with wood
    ceiling_height_m: float = 15.0
    ceiling_height_min_m: float = 12.0
    ceiling_height_max_m: float = 18.0
    ceiling_height_reasoning: str = """
    No archaeological evidence - ceiling completely destroyed.
    Estimate based on:
    1. Doric column proportions (6:1 to 8:1 height:diameter)
    2. Structural engineering for wooden roof spanning 51.5m
    3. Comparison to other Greek buildings of similar scale
    Uncertainty: ±3m (±20%)
    """
    ceiling_confidence: str = "LOW"

    # Column dimensions - INFERRED
    column_diameter_m: float = 1.75
    column_diameter_min_m: float = 1.5
    column_diameter_max_m: float = 2.0
    column_reasoning: str = "Based on Doric proportions and spacing requirements"
    column_confidence: str = "MEDIUM-LOW"

    # Anaktoron dimensions - PARTIAL RUINS
    anaktoron_length_m: float = 8.0
    anaktoron_width_m: float = 8.0
    anaktoron_uncertainty_m: float = 2.0
    anaktoron_confidence: str = "MEDIUM - ruins exist but interpretation varies"

    # Opaion (roof opening) - MENTIONED IN SOURCES, SIZE UNKNOWN
    opaion_exists: bool = True  # Documented in ancient sources
    opaion_area_min_m2: float = 10.0
    opaion_area_max_m2: float = 50.0
    opaion_confidence: str = "LOW - existence documented, size completely unknown"

    # Material absorption coefficients - FROM LITERATURE, NOT MEASURED
    marble_absorption_125Hz: Tuple[float, float] = (0.01, 0.02)  # (min, max)
    marble_absorption_1000Hz: Tuple[float, float] = (0.01, 0.02)
    absorption_confidence: str = "MEDIUM - literature values, not site-specific"


# =============================================================================
# FIRST-PRINCIPLES CALCULATIONS WITH UNCERTAINTY PROPAGATION
# =============================================================================

def speed_of_sound(temperature_c: float, uncertainty_c: float = 2.0) -> Tuple[float, float, float]:
    """
    Calculate speed of sound with uncertainty.

    Returns: (central_value, min_value, max_value)
    """
    c_central = 331.3 + 0.606 * temperature_c
    c_min = 331.3 + 0.606 * (temperature_c - uncertainty_c)
    c_max = 331.3 + 0.606 * (temperature_c + uncertainty_c)
    return (c_central, c_min, c_max)


def room_mode_frequency(nx: int, ny: int, nz: int,
                        Lx: float, Ly: float, Lz: float,
                        c: float) -> float:
    """
    Standard room mode formula.
    f = (c/2) × √[(nx/Lx)² + (ny/Ly)² + (nz/Lz)²]

    This is ESTABLISHED PHYSICS - no uncertainty in the formula itself.
    Uncertainty comes from input parameters.
    """
    if nx == 0 and ny == 0 and nz == 0:
        return 0.0

    term = np.sqrt((nx/Lx)**2 + (ny/Ly)**2 + (nz/Lz)**2)
    return (c / 2) * term


def room_mode_with_uncertainty(nx: int, ny: int, nz: int,
                               known: KnownFacts,
                               estimated: EstimatedParameters,
                               temperature_c: float = 20.0) -> Dict:
    """
    Calculate room mode frequency WITH FULL UNCERTAINTY PROPAGATION.

    Returns dict with central estimate and confidence interval.
    """
    # Get speed of sound range
    c_central, c_min, c_max = speed_of_sound(temperature_c)

    # Dimension ranges
    Lx_central = known.floor_length_m
    Lx_min = known.floor_length_m - known.floor_dimension_uncertainty_m
    Lx_max = known.floor_length_m + known.floor_dimension_uncertainty_m

    Ly_central = known.floor_width_m
    Ly_min = known.floor_width_m - known.floor_dimension_uncertainty_m
    Ly_max = known.floor_width_m + known.floor_dimension_uncertainty_m

    Lz_central = estimated.ceiling_height_m
    Lz_min = estimated.ceiling_height_min_m
    Lz_max = estimated.ceiling_height_max_m

    # Calculate frequency at all corners of parameter space
    frequencies = []
    for c in [c_min, c_central, c_max]:
        for Lx in [Lx_min, Lx_central, Lx_max]:
            for Ly in [Ly_min, Ly_central, Ly_max]:
                for Lz in [Lz_min, Lz_central, Lz_max]:
                    f = room_mode_frequency(nx, ny, nz, Lx, Ly, Lz, c)
                    if f > 0:
                        frequencies.append(f)

    if not frequencies:
        return {"mode": (nx, ny, nz), "frequency_hz": 0, "error": "Invalid mode"}

    f_central = room_mode_frequency(nx, ny, nz, Lx_central, Ly_central, Lz_central, c_central)
    f_min = min(frequencies)
    f_max = max(frequencies)

    # Determine dominant uncertainty source
    # For axial modes, which dimension dominates?
    if nz > 0 and nx == 0 and ny == 0:
        dominant_uncertainty = "ceiling_height (LOW confidence)"
    elif nz == 0:
        dominant_uncertainty = "floor_dimensions (HIGH confidence)"
    else:
        dominant_uncertainty = "mixed (ceiling dominates uncertainty)"

    return {
        "mode": (nx, ny, nz),
        "frequency_hz_central": round(f_central, 3),
        "frequency_hz_min": round(f_min, 3),
        "frequency_hz_max": round(f_max, 3),
        "uncertainty_percent": round(100 * (f_max - f_min) / (2 * f_central), 1),
        "dominant_uncertainty_source": dominant_uncertainty,
        "confidence": "HIGH" if nz == 0 else "LOW (ceiling height unknown)"
    }


def analyze_mode_degeneracy(known: KnownFacts) -> Dict:
    """
    Analyze mode degeneracy - this IS a first-principles result.

    For a square room (Lx = Ly), modes (m,n,p) and (n,m,p) have
    identical frequencies. This is MATHEMATICAL FACT, not speculation.
    """
    # Check if floor is square within uncertainty
    length_diff = abs(known.floor_length_m - known.floor_width_m)
    is_square = length_diff <= known.floor_dimension_uncertainty_m

    if is_square:
        explanation = """
MATHEMATICAL FACT: For a square room where Lx = Ly, the room mode formula
    f = (c/2) × √[(nx/Lx)² + (ny/Ly)² + (nz/Lz)²]
produces IDENTICAL frequencies for modes (m,n,p) and (n,m,p) where m ≠ n.

This is called MODE DEGENERACY. It means:
- Multiple distinct standing wave patterns exist at the same frequency
- These patterns can superimpose (constructive/destructive interference)
- The acoustic field becomes more complex than in non-square rooms

This is NOT speculation - it's a direct mathematical consequence of Lx = Ly.
The Telesterion floor plan (51.5m × 51.5m) satisfies this condition.
"""
        degeneracy_factor = "HIGH - square floor plan guarantees degeneracy"
    else:
        explanation = "Floor is not square within measurement uncertainty."
        degeneracy_factor = "UNCERTAIN"

    return {
        "floor_is_square": is_square,
        "length_m": known.floor_length_m,
        "width_m": known.floor_width_m,
        "difference_m": length_diff,
        "degeneracy_present": is_square,
        "explanation": explanation,
        "confidence": "HIGH - this is geometry, not speculation"
    }


# =============================================================================
# WHAT WE CAN AND CANNOT SAY
# =============================================================================

def first_principles_summary(known: KnownFacts, estimated: EstimatedParameters) -> Dict:
    """
    Generate a summary of what first-principles analysis actually tells us.
    """

    # Calculate key modes with uncertainty
    fund_x = room_mode_with_uncertainty(1, 0, 0, known, estimated)
    fund_y = room_mode_with_uncertainty(0, 1, 0, known, estimated)
    fund_z = room_mode_with_uncertainty(0, 0, 1, known, estimated)

    # Degeneracy analysis
    degeneracy = analyze_mode_degeneracy(known)

    summary = {
        "title": "TELESTERION FIRST-PRINCIPLES ANALYSIS",
        "methodology": "Only claims supported by established physics and documented evidence",

        "WHAT_WE_KNOW": {
            "floor_dimensions": {
                "value": f"{known.floor_length_m}m × {known.floor_width_m}m",
                "uncertainty": f"±{known.floor_dimension_uncertainty_m}m",
                "confidence": "HIGH",
                "source": "Archaeological consensus (Mylonas, Perseus, EFADA)"
            },
            "floor_is_square": {
                "value": True,
                "confidence": "HIGH",
                "implication": "Mode degeneracy is GUARANTEED by geometry"
            },
            "column_count": {
                "value": 42,
                "confidence": "HIGH",
                "source": "Visible in ruins"
            }
        },

        "WHAT_WE_CAN_CALCULATE": {
            "fundamental_mode_horizontal": {
                "frequency_hz": fund_x["frequency_hz_central"],
                "range_hz": f"{fund_x['frequency_hz_min']} - {fund_x['frequency_hz_max']}",
                "uncertainty": f"±{fund_x['uncertainty_percent']}%",
                "confidence": "HIGH (floor dimensions well-known)",
                "is_infrasonic": fund_x["frequency_hz_central"] < 20,
                "physics": "Standard room mode equation"
            },
            "fundamental_mode_vertical": {
                "frequency_hz": fund_z["frequency_hz_central"],
                "range_hz": f"{fund_z['frequency_hz_min']} - {fund_z['frequency_hz_max']}",
                "uncertainty": f"±{fund_z['uncertainty_percent']}%",
                "confidence": "LOW (ceiling height unknown)",
                "physics": "Standard room mode equation"
            },
            "mode_degeneracy": {
                "present": True,
                "confidence": "HIGH",
                "explanation": "Mathematical consequence of square floor plan"
            }
        },

        "WHAT_WE_CANNOT_CLAIM": [
            "That acoustics were INTENTIONALLY designed (no textual evidence)",
            "Specific SPL levels during ceremonies (no measurements)",
            "That infrasound CAUSED the documented experiences (correlation ≠ causation)",
            "Kykeon contents or effects (speculation, not evidence)",
            "CO2 levels or atmospheric effects (no ventilation data)",
            "Specific neurological effects on initiates (no EEG data)",
            "That this was 'psychotechnology' (strong claim, weak evidence)"
        ],

        "TESTABLE_HYPOTHESES": [
            {
                "hypothesis": "Room modes cluster around 3.3 Hz (±10%)",
                "test": "In-situ acoustic measurement with impulse response",
                "feasibility": "POSSIBLE - requires site access"
            },
            {
                "hypothesis": "RT60 exceeds 5 seconds at low frequencies",
                "test": "Reverberation time measurement",
                "feasibility": "POSSIBLE - ruins may still show acoustic character"
            },
            {
                "hypothesis": "Square floor creates measurable mode degeneracy",
                "test": "Spectral analysis of room response",
                "feasibility": "POSSIBLE with reconstruction or modeling"
            }
        ]
    }

    return summary


# =============================================================================
# INFRASOUND EFFECTS: WHAT THE LITERATURE ACTUALLY SAYS
# =============================================================================

@dataclass
class InfrasoundLiterature:
    """
    ACTUAL peer-reviewed findings on infrasound effects.
    NOT what we wish were true, but what's documented.
    """

    tandy_1998: Dict = field(default_factory=lambda: {
        "citation": "Tandy V. & Lawrence T. (1998). J. Society for Psychical Research, 62, 360-364",
        "finding": "18.98 Hz infrasound caused visual disturbances, anxiety, feeling of presence",
        "mechanism_proposed": "Eyeball resonance at ~19 Hz",
        "sample_size": "Case study (n=1 initial, later replicated)",
        "SPL": "Not precisely measured",
        "confidence": "LOW-MEDIUM - interesting but limited data"
    })

    wiseman_2003: Dict = field(default_factory=lambda: {
        "citation": "Wiseman R. et al. Concert hall infrasound study",
        "finding": "22% reported unusual experiences with infrasound vs control",
        "frequency": "~17 Hz",
        "sample_size": "750 subjects",
        "effect_size": "Small but statistically significant",
        "confidence": "MEDIUM - larger sample, controlled, but subtle effects"
    })

    vestibular_research: Dict = field(default_factory=lambda: {
        "finding": "Vestibular system responds to frequencies 0.5-10 Hz",
        "peak_sensitivity": "~7 Hz often cited, but individual variation is HIGH",
        "threshold": "Varies by individual, posture, exposure duration",
        "confidence": "MEDIUM - established but variable"
    })

    what_is_NOT_established: List[str] = field(default_factory=lambda: [
        "Specific SPL thresholds for vestibular effects (highly variable)",
        "That infrasound causes 'mystical experiences' (no controlled studies)",
        "That ancient peoples understood or exploited infrasound",
        "That 3.3 Hz specifically has unique effects (not studied at this frequency)",
        "Synergistic effects with psychoactive substances (not studied)",
        "Long-term effects of infrasound exposure at moderate levels"
    ])


# =============================================================================
# COMPARATIVE ANALYSIS: IS TELESTERION SPECIAL?
# =============================================================================

def comparative_room_modes() -> Dict:
    """
    Calculate room modes for OTHER ancient structures.

    If Telesterion's acoustics are special, they should differ
    from other large ancient buildings. If similar, the "special
    acoustic design" hypothesis weakens.
    """

    structures = {
        "Telesterion": {
            "dimensions_m": (51.5, 51.5, 15),
            "confidence": "floor HIGH, height LOW"
        },
        "Parthenon_cella": {
            "dimensions_m": (29.8, 19.2, 13),  # interior cella
            "confidence": "HIGH - well documented"
        },
        "Pantheon_Rome": {
            "dimensions_m": (43.3, 43.3, 43.3),  # diameter = height
            "confidence": "HIGH - intact building"
        },
        "Hagia_Sophia": {
            "dimensions_m": (77, 71, 55),  # main nave approximate
            "confidence": "HIGH - intact building"
        },
        "Generic_cathedral": {
            "dimensions_m": (100, 30, 30),  # typical gothic proportions
            "confidence": "MEDIUM - generalized"
        }
    }

    results = {}
    c = 343.0  # speed of sound at 20°C

    for name, data in structures.items():
        Lx, Ly, Lz = data["dimensions_m"]

        # Fundamental modes
        f_x = (c/2) / Lx if Lx > 0 else 0
        f_y = (c/2) / Ly if Ly > 0 else 0
        f_z = (c/2) / Lz if Lz > 0 else 0

        # Check for square floor (degeneracy)
        is_square = abs(Lx - Ly) / max(Lx, Ly) < 0.05  # within 5%

        results[name] = {
            "dimensions_m": (Lx, Ly, Lz),
            "fundamental_x_hz": round(f_x, 2),
            "fundamental_y_hz": round(f_y, 2),
            "fundamental_z_hz": round(f_z, 2),
            "lowest_mode_hz": round(min(f_x, f_y, f_z), 2),
            "is_infrasonic": min(f_x, f_y, f_z) < 20,
            "has_square_floor": is_square,
            "has_mode_degeneracy": is_square,
            "confidence": data["confidence"]
        }

    # Analysis
    infrasonic_count = sum(1 for r in results.values() if r["is_infrasonic"])
    square_count = sum(1 for r in results.values() if r["has_square_floor"])

    analysis = {
        "structures_analyzed": len(results),
        "structures_with_infrasonic_modes": infrasonic_count,
        "structures_with_square_floors": square_count,
        "conclusion": """
ALL large enclosed spaces have infrasonic room modes.
This is simple physics: f = c/(2L), so any dimension > 8.6m gives f < 20 Hz.

The Telesterion IS unusual in having a SQUARE floor plan, which creates
mode degeneracy. But this could be:
1. Deliberate acoustic design
2. Ritual/symbolic requirement for square plan
3. Structural/practical consideration
4. Coincidence

We CANNOT distinguish these possibilities from acoustic analysis alone.
"""
    }

    return {"structures": results, "analysis": analysis}


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_first_principles_analysis():
    """Run complete first-principles analysis."""

    print("="*70)
    print("TELESTERION FIRST-PRINCIPLES ANALYSIS")
    print("="*70)
    print("\nMethodology: Only claims supported by established physics")
    print("             and documented archaeological evidence\n")

    # Initialize with known facts
    known = KnownFacts()
    estimated = EstimatedParameters()

    # 1. Summary of what we know vs. assume
    print("\n" + "="*70)
    print("SECTION 1: KNOWLEDGE TIERS")
    print("="*70)

    print("\nTIER 1 - KNOWN (High Confidence):")
    print(f"  Floor: {known.floor_length_m}m × {known.floor_width_m}m (±{known.floor_dimension_uncertainty_m}m)")
    print(f"  Columns: {known.num_columns} ({known.column_arrangement})")
    print(f"  Materials: {known.wall_material} walls, {known.roof_material} roof")

    print("\nTIER 2 - ESTIMATED (Low-Medium Confidence):")
    print(f"  Ceiling height: {estimated.ceiling_height_m}m")
    print(f"    Range: {estimated.ceiling_height_min_m}m - {estimated.ceiling_height_max_m}m")
    print(f"    Confidence: {estimated.ceiling_confidence}")
    print(f"    Reasoning: {estimated.ceiling_height_reasoning.strip()[:200]}...")

    # 2. Room mode calculations with uncertainty
    print("\n" + "="*70)
    print("SECTION 2: ROOM MODE CALCULATIONS")
    print("="*70)

    modes_to_calculate = [
        (1, 0, 0, "Fundamental X (horizontal)"),
        (0, 1, 0, "Fundamental Y (horizontal)"),
        (0, 0, 1, "Fundamental Z (vertical)"),
        (1, 1, 0, "First tangential"),
        (2, 0, 0, "Second harmonic X"),
    ]

    print("\n{:<25} {:>10} {:>20} {:>12}".format(
        "Mode", "Central", "Range", "Confidence"))
    print("-"*70)

    for nx, ny, nz, name in modes_to_calculate:
        result = room_mode_with_uncertainty(nx, ny, nz, known, estimated)
        print("{:<25} {:>10.2f} Hz {:>8.2f} - {:<8.2f} {:>10}".format(
            name,
            result["frequency_hz_central"],
            result["frequency_hz_min"],
            result["frequency_hz_max"],
            "HIGH" if result["confidence"].startswith("HIGH") else "LOW"
        ))

    # 3. Degeneracy analysis
    print("\n" + "="*70)
    print("SECTION 3: MODE DEGENERACY")
    print("="*70)

    deg = analyze_mode_degeneracy(known)
    print(f"\nFloor is square: {deg['floor_is_square']}")
    print(f"Degeneracy present: {deg['degeneracy_present']}")
    print(f"Confidence: {deg['confidence']}")
    print(deg['explanation'])

    # 4. Comparative analysis
    print("\n" + "="*70)
    print("SECTION 4: COMPARATIVE ANALYSIS")
    print("="*70)

    comparison = comparative_room_modes()

    print("\n{:<20} {:>12} {:>12} {:>10} {:>10}".format(
        "Structure", "Lowest Mode", "Square?", "Infra?", "Confidence"))
    print("-"*70)

    for name, data in comparison["structures"].items():
        print("{:<20} {:>10.2f} Hz {:>10} {:>10} {:>10}".format(
            name,
            data["lowest_mode_hz"],
            "YES" if data["has_square_floor"] else "no",
            "YES" if data["is_infrasonic"] else "no",
            data["confidence"].split()[0]
        ))

    print(comparison["analysis"]["conclusion"])

    # 5. What we can and cannot claim
    print("\n" + "="*70)
    print("SECTION 5: EPISTEMOLOGICAL BOUNDARIES")
    print("="*70)

    summary = first_principles_summary(known, estimated)

    print("\nWHAT WE CAN CLAIM (with evidence):")
    for key, val in summary["WHAT_WE_CAN_CALCULATE"].items():
        if isinstance(val, dict):
            print(f"  • {key}: {val.get('frequency_hz', val.get('present', 'N/A'))}")
            print(f"    Confidence: {val.get('confidence', 'N/A')}")

    print("\nWHAT WE CANNOT CLAIM (insufficient evidence):")
    for item in summary["WHAT_WE_CANNOT_CLAIM"]:
        print(f"  ✗ {item}")

    print("\nTESTABLE HYPOTHESES (for future research):")
    for hyp in summary["TESTABLE_HYPOTHESES"]:
        print(f"  → {hyp['hypothesis']}")
        print(f"    Test: {hyp['test']}")
        print(f"    Feasibility: {hyp['feasibility']}")

    # 6. Final assessment
    print("\n" + "="*70)
    print("SECTION 6: FIRST-PRINCIPLES CONCLUSIONS")
    print("="*70)

    print("""
WHAT FIRST-PRINCIPLES PHYSICS TELLS US:

1. The Telesterion HAS infrasonic room modes (~3.3 Hz fundamental)
   → Confidence: HIGH for horizontal modes, LOW for vertical
   → This is simple physics: large room = low-frequency modes

2. The square floor plan CREATES mode degeneracy
   → Confidence: HIGH (mathematical fact)
   → Degeneracy means multiple modes at same frequency

3. ALL large enclosed spaces have infrasonic modes
   → The Telesterion is not unique in this regard
   → The Pantheon, cathedrals, etc. all have similar properties

4. We CANNOT determine intentionality from acoustics alone
   → No textual evidence Greeks understood room modes
   → Square plan could have ritual, not acoustic, motivation

5. Correlation with ancient accounts is SUGGESTIVE but NOT PROOF
   → "Trembling, terror" could be infrasound OR
   → Fasting, kykeon, psychology, crowd effects, sleep deprivation

HONEST SUMMARY:

The Telesterion's acoustic properties are CONSISTENT WITH the hypothesis
that acoustics contributed to the initiate experience. However:

• We cannot prove acoustics were intentionally designed
• We cannot isolate acoustic effects from confounding factors
• We cannot verify specific SPL levels or neurological effects
• The "psychoacoustic engine" framing OVERSTATES the evidence

This is a PLAUSIBLE HYPOTHESIS worth testing, not an established fact.
""")

    # Save results
    output = {
        "summary": summary,
        "comparison": comparison,
        "degeneracy": deg,
        "known_facts": {
            "floor_dimensions_m": (known.floor_length_m, known.floor_width_m),
            "floor_uncertainty_m": known.floor_dimension_uncertainty_m,
            "columns": known.num_columns
        },
        "estimated_parameters": {
            "ceiling_height_m": estimated.ceiling_height_m,
            "ceiling_range_m": (estimated.ceiling_height_min_m, estimated.ceiling_height_max_m),
            "confidence": estimated.ceiling_confidence
        }
    }

    return output


if __name__ == "__main__":
    results = run_first_principles_analysis()

    # Save to JSON
    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/telesterion_analysis/first_principles_results.json"

    # Convert for JSON serialization
    def convert_for_json(obj):
        if isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_for_json(i) for i in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        else:
            return obj

    with open(output_path, 'w') as f:
        json.dump(convert_for_json(results), f, indent=2)

    print(f"\nResults saved to: {output_path}")
