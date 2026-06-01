#!/usr/bin/env python3
"""
M4 Therapeutic Candidate Ranking
================================

Ranks all peptide candidates across all pipelines using multiple criteria:
1. Predicted binding affinity (from our heuristics)
2. Drug-likeness score
3. Novelty (from drug comparison)
4. Structural features (cyclic, disulfide, BBB-crossing)
5. Target importance (unmet medical need)

Produces a unified ranking of top therapeutic candidates.

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import re


# Target importance scores (unmet medical need, market size, etc.)
TARGET_IMPORTANCE = {
    # High unmet need (score 10)
    "Alzheimer": 10,
    "Parkinson": 10,
    "ALS": 10,
    "Huntington": 10,
    "Pancreatic cancer": 10,
    "Glioblastoma": 10,
    "c-Myc": 10,
    "KRAS": 10,

    # High need (score 8)
    "Depression": 8,
    "Anxiety": 8,
    "Obesity": 8,
    "NASH": 8,
    "Lupus": 8,
    "MS": 8,
    "DMD": 8,
    "SMA": 8,
    "CF": 8,

    # Moderate need (score 6)
    "Type 2 Diabetes": 6,
    "Rheumatoid Arthritis": 6,
    "IBD": 6,
    "Psoriasis": 6,
    "AMD": 6,
    "Glaucoma": 6,

    # Addressed but improvable (score 4)
    "Prolactinoma": 4,
    "Osteoporosis": 4,
    "Hypertension": 4,
}


@dataclass
class RankedCandidate:
    """A ranked therapeutic candidate."""
    rank: int
    peptide_id: str
    sequence: str
    target: str
    disease_area: str
    predicted_affinity_nM: float
    affinity_score: float  # Normalized 0-1
    druglikeness_score: float
    novelty_score: float
    structural_score: float
    target_importance: float
    composite_score: float
    source_pipeline: str
    notes: List[str]


def calculate_druglikeness(sequence: str) -> float:
    """Calculate drug-likeness score for a peptide."""
    score = 1.0

    # Length penalty (ideal: 8-25 aa)
    length = len(sequence)
    if length < 8:
        score *= 0.7
    elif length > 40:
        score *= 0.5
    elif length > 25:
        score *= 0.8

    # Charge (mild positive preferred for cell penetration)
    positive = sum(1 for aa in sequence if aa in "RKH")
    negative = sum(1 for aa in sequence if aa in "DE")
    net_charge = positive - negative

    if -2 <= net_charge <= 4:
        score *= 1.0
    elif net_charge > 6:
        score *= 0.7  # Too cationic - toxicity risk
    elif net_charge < -4:
        score *= 0.6  # Too anionic - poor cell penetration

    # Hydrophobicity (moderate preferred)
    hydrophobic = sum(1 for aa in sequence if aa in "AILMFWVY")
    hydro_frac = hydrophobic / length if length > 0 else 0

    if 0.3 <= hydro_frac <= 0.5:
        score *= 1.0
    elif hydro_frac > 0.7:
        score *= 0.6  # Too hydrophobic - aggregation risk
    elif hydro_frac < 0.2:
        score *= 0.8

    # Cyclic bonus (stability)
    if sequence.startswith("C") and sequence.endswith("C"):
        score *= 1.2
    elif sequence.count("C") >= 2 and sequence.count("C") % 2 == 0:
        score *= 1.1

    # Proline content (affects structure)
    proline_frac = sequence.count("P") / length if length > 0 else 0
    if proline_frac > 0.2:
        score *= 0.8  # Too many prolines

    # Methionine/Cysteine oxidation risk
    met_cys = sequence.count("M") + sequence.count("C")
    if met_cys > length * 0.15:
        score *= 0.9

    return min(1.0, score)


def calculate_structural_score(sequence: str, metadata: Dict) -> float:
    """Calculate structural feature score."""
    score = 0.5  # Base

    # Cyclic
    if sequence.startswith("C") and sequence.endswith("C"):
        score += 0.2
    elif "cyclic" in str(metadata).lower():
        score += 0.2

    # BBB-crossing
    if metadata.get("bbb_strategy") or "bbb" in str(metadata).lower():
        score += 0.2

    # Stability modifications mentioned
    if "stable" in str(metadata).lower() or "half-life" in str(metadata).lower():
        score += 0.1

    return min(1.0, score)


def get_target_importance(target: str, target system: str) -> float:
    """Get importance score for target/target system."""
    text = f"{target} {target system}".lower()

    for key, importance in TARGET_IMPORTANCE.items():
        if key.lower() in text:
            return importance / 10.0  # Normalize to 0-1

    return 0.5  # Default moderate importance


def load_all_peptides(base_dir: Path) -> List[Dict]:
    """Load all peptides from JSON result files."""
    peptides = []

    json_files = list(base_dir.glob("**/peptides/*.json")) + \
                 list(base_dir.glob("**/binders/*.json")) + \
                 list(base_dir.glob("**/*peptide*.json"))

    for json_path in json_files:
        try:
            with open(json_path) as f:
                data = json.load(f)

            # Handle different JSON structures
            if "peptides" in data:
                for p in data["peptides"]:
                    p["_source_file"] = str(json_path)
                    peptides.append(p)
            elif "results" in data:
                for p in data["results"]:
                    p["_source_file"] = str(json_path)
                    peptides.append(p)
            elif isinstance(data, list):
                for p in data:
                    p["_source_file"] = str(json_path)
                    peptides.append(p)

        except Exception as e:
            continue

    return peptides


def rank_peptides(peptides: List[Dict]) -> List[RankedCandidate]:
    """Rank all peptides by composite therapeutic score."""
    candidates = []

    for p in peptides:
        # Extract fields (handle different naming conventions)
        pep_id = p.get("peptide_id") or p.get("id") or p.get("name", "unknown")
        sequence = p.get("sequence", "")
        target = p.get("target") or p.get("target_gene") or p.get("target_name", "")
        target system = p.get("target system") or p.get("diseases", "") or p.get("indication", "")
        if isinstance(target system, list):
            target system = ", ".join(target system)

        # Get predicted affinity
        affinity = p.get("predicted_Kd_nM") or p.get("predicted_Ki_nM") or \
                   p.get("predicted_EC50_nM") or p.get("predicted_activity_nM") or \
                   p.get("Kd_nM") or 1000  # Default

        # Normalize affinity to 0-1 score (lower Kd = better = higher score)
        # Use log scale: 0.1 nM = 1.0, 1 nM = 0.9, 10 nM = 0.8, 100 nM = 0.6, 1000 nM = 0.4
        import math
        if affinity > 0:
            affinity_score = max(0, 1.0 - 0.1 * math.log10(affinity + 0.1))
        else:
            affinity_score = 0.5

        # Calculate other scores
        druglikeness = calculate_druglikeness(sequence)
        structural = calculate_structural_score(sequence, p)
        importance = get_target_importance(target, target system)

        # Novelty (from benchmark comparison if available)
        bench_comp = p.get("benchmark_comparison", "")
        if "better" in bench_comp.lower():
            novelty = 0.8
        elif "weaker" in bench_comp.lower():
            novelty = 0.4
        else:
            novelty = 0.6

        # Composite score (weighted)
        composite = (
            0.30 * affinity_score +
            0.20 * druglikeness +
            0.15 * novelty +
            0.15 * structural +
            0.20 * importance
        )

        # Determine source pipeline
        source = p.get("_source_file", "")
        if "metabolic" in source:
            pipeline = "Obesity/Metabolic"
        elif "neuro" in source:
            pipeline = "Neurological"
        elif "depression" in source or "anxiety" in source:
            pipeline = "Depression/Anxiety"
        elif "autoimmune" in source:
            pipeline = "Autoimmune"
        elif "pediatric" in source:
            pipeline = "Pediatric Genetic"
        elif "eye" in source:
            pipeline = "Eye/Vision"
        elif "prolactinoma" in source:
            pipeline = "Prolactinoma"
        elif "cmyc" in source or "dark_proteome" in source:
            pipeline = "Dark Proteome"
        else:
            pipeline = "Other"

        # Notes
        notes = []
        if affinity < 1:
            notes.append("Sub-nanomolar predicted affinity")
        if sequence.startswith("C") and sequence.endswith("C"):
            notes.append("Cyclic (disulfide)")
        if p.get("bbb_strategy"):
            notes.append(f"BBB-crossing: {p.get('bbb_strategy')}")
        if importance >= 0.8:
            notes.append("High unmet medical need")

        candidate = RankedCandidate(
            rank=0,  # Will be set after sorting
            peptide_id=pep_id,
            sequence=sequence,
            target=target,
            disease_area=target system,
            predicted_affinity_nM=affinity,
            affinity_score=round(affinity_score, 3),
            druglikeness_score=round(druglikeness, 3),
            novelty_score=round(novelty, 3),
            structural_score=round(structural, 3),
            target_importance=round(importance, 3),
            composite_score=round(composite, 4),
            source_pipeline=pipeline,
            notes=notes,
        )
        candidates.append(candidate)

    # Sort by composite score
    candidates.sort(key=lambda x: x.composite_score, reverse=True)

    # Assign ranks
    for i, c in enumerate(candidates):
        c.rank = i + 1

    return candidates


def run_ranking():
    """Run therapeutic candidate ranking."""
    print("=" * 70)
    print("M4 THERAPEUTIC CANDIDATE RANKING")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Load all peptides
    base_dir = Path(__file__).parent.parent
    peptides = load_all_peptides(base_dir)
    print(f"Loaded {len(peptides)} peptides from all pipelines")

    # Rank
    print("\nRanking peptides...")
    candidates = rank_peptides(peptides)
    print(f"Ranked {len(candidates)} candidates")

    # Top candidates
    print("\n" + "=" * 70)
    print("TOP 25 THERAPEUTIC CANDIDATES")
    print("=" * 70)

    for c in candidates[:25]:
        print(f"\n#{c.rank}: {c.peptide_id}")
        print(f"  Sequence: {c.sequence[:30]}{'...' if len(c.sequence) > 30 else ''}")
        print(f"  Target: {c.target}")
        print(f"  target system: {c.disease_area[:50] if c.disease_area else 'N/A'}")
        print(f"  Predicted Kd: {c.predicted_affinity_nM:.2f} nM")
        print(f"  Composite Score: {c.composite_score:.4f}")
        print(f"  Pipeline: {c.source_pipeline}")
        if c.notes:
            for note in c.notes:
                print(f"  * {note}")

    # Summary by pipeline
    print("\n" + "=" * 70)
    print("TOP CANDIDATES BY PIPELINE")
    print("=" * 70)

    pipelines = {}
    for c in candidates:
        if c.source_pipeline not in pipelines:
            pipelines[c.source_pipeline] = []
        pipelines[c.source_pipeline].append(c)

    for pipeline, cands in sorted(pipelines.items()):
        top = cands[0]
        print(f"\n{pipeline}:")
        print(f"  Best: {top.peptide_id} (score: {top.composite_score:.4f})")
        print(f"  Target: {top.target}")
        print(f"  Count: {len(cands)} candidates")

    # Save results
    output_dir = Path(__file__).parent / "rankings"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output = {
        "timestamp": datetime.now().isoformat(),
        "total_candidates": len(candidates),
        "ranking_criteria": [
            "Predicted binding affinity (30%)",
            "Drug-likeness (20%)",
            "Target importance (20%)",
            "Novelty (15%)",
            "Structural features (15%)",
        ],
        "top_25": [asdict(c) for c in candidates[:25]],
        "top_by_pipeline": {
            pipeline: asdict(cands[0]) if cands else None
            for pipeline, cands in pipelines.items()
        },
        "all_rankings": [
            {
                "rank": c.rank,
                "peptide_id": c.peptide_id,
                "sequence": c.sequence,
                "composite_score": c.composite_score,
                "pipeline": c.source_pipeline,
            }
            for c in candidates
        ],
    }

    json_path = output_dir / f"therapeutic_rankings_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved: {json_path}")

    # Summary stats
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total candidates ranked: {len(candidates)}")
    print(f"Pipelines represented: {len(pipelines)}")
    print(f"Top score: {candidates[0].composite_score:.4f}")
    print(f"Median score: {candidates[len(candidates)//2].composite_score:.4f}")

    sub_nano = sum(1 for c in candidates if c.predicted_affinity_nM < 1)
    high_importance = sum(1 for c in candidates if c.target_importance >= 0.8)
    print(f"Sub-nanomolar affinity: {sub_nano}")
    print(f"High importance targets: {high_importance}")

    return candidates


if __name__ == "__main__":
    run_ranking()
