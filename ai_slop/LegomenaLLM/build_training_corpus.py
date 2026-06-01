#!/usr/bin/env python3
"""
LegomenaXL-31B Training Corpus Builder

This script extracts, filters, and ranks content from the Z² Framework repository
to create a high-quality training corpus for fine-tuning Gemma 4 31B.

Quality tiers based on HONESTY_ASSESSMENT.md:
- Tier 1: Mathematical certainties (proofs)
- Tier 2: First-principles derivations (mechanisms)
- Tier 3: Phenomenological patterns (structure constants)
- Tier 4: Numerology (exclude or use as negative examples)
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

# Base path
BASE_PATH = Path("/Users/carlzimmerman/new_physics/zimmerman-formula")


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURE CONSTANTS (Reference)
# ═══════════════════════════════════════════════════════════════════════════════

STRUCTURE_CONSTANTS = {
    "BEKENSTEIN": 4,
    "N_gen": 3,
    "N_MATTER": 6,
    "CUBE": 8,
    "GAUGE": 12,
    "N_VACUUM": 13,
    "N_TOTAL": 19,
    "Z_squared": 33.510321638291124,  # 32π/3
    "Z": 5.788536897914519,           # √(32π/3)
}


# ═══════════════════════════════════════════════════════════════════════════════
# GOLD STANDARD DOCUMENTS
# ═══════════════════════════════════════════════════════════════════════════════

GOLD_DOCUMENTS = [
    # Main papers (highest priority)
    "papers/Z2_UNIFIED_ACTION_v5.7.9.tex",
    "papers/COSMIC_DIPOLE_Z2_COMPLETE.md",
    "papers/COSMIC_DIPOLE_Z2_COMPLETE.tex",

    # Core theory
    "core_theory/THEORETICAL_FOUNDATIONS.md",
    "core_theory/RADION_ATTRACTOR_STATE.md",
    "core_theory/TOPOLOGICAL_IR_FIXED_POINTS.md",
    "core_theory/COMPLETE_DERIVATIONS_GUIDE.md",
    "core_theory/Z2_COMPLETE_DERIVATION.md",
    "core_theory/HORIZON_CALCULATION.md",

    # Quality-assessed research
    "research/PAPER_VS_FINDINGS_COMPARISON.md",
    "research/SYSTEMATIC_DERIVATIONS.md",
    "research/DAEMON_VS_DEEP_ANALYSIS.md",
    "research/COMPREHENSIVE_ASSESSMENT.md",

    # Honesty assessments (meta-quality)
    "article_ideas_for_publishers/HONESTY_ASSESSMENT.md",
    "HONESTY_ASSESSMENT.md",
    "META_HONESTY_ASSESSMENT.md",
]

# Patterns that indicate content should be EXCLUDED
BAD_PATTERNS = [
    r"r\s*=\s*0\.003",           # Fabricated tensor-scalar ratio
    r"m_a\s*=\s*57",             # Fabricated axion mass
    r"m_DM\s*=\s*2\.6\s*keV",    # Wrong paradigm (particle DM)
    r"dark matter mass.*keV",    # Wrong paradigm
]

# Patterns that indicate HIGH QUALITY content
GOOD_PATTERNS = [
    r"sin²θ_W\s*=\s*3/13",
    r"Ω_Λ\s*=\s*13/19",
    r"Ω_m\s*=\s*6/19",
    r"α⁻¹\s*=\s*4Z²\s*\+\s*3",
    r"Z²\s*=\s*32π/3",
    r"Atiyah-Singer",
    r"Cartan-Killing",
    r"T³/Z₂",
    r"first.principles",
    r"DERIVED",
    r"PROVEN",
]


@dataclass
class TrainingExample:
    """A single training example for instruction tuning."""
    instruction: str
    input: str
    output: str
    derivation_tier: str  # first_principles, phenomenological, numerology
    source_file: str
    mechanism: Optional[str] = None
    error_percent: Optional[float] = None
    structure_constants_used: Optional[list] = None


@dataclass
class DocumentQuality:
    """Quality assessment for a document."""
    path: str
    tier: int  # 1-4
    good_pattern_count: int
    bad_pattern_count: int
    date_score: float  # 1.0 = recent, 0.0 = old
    include: bool
    reason: str


def assess_document_quality(filepath: Path) -> DocumentQuality:
    """Assess the quality tier of a document."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return DocumentQuality(
            path=str(filepath),
            tier=4,
            good_pattern_count=0,
            bad_pattern_count=1,
            date_score=0,
            include=False,
            reason=f"Read error: {e}"
        )

    # Check for bad patterns
    bad_count = sum(1 for p in BAD_PATTERNS if re.search(p, content, re.IGNORECASE))

    # Check for good patterns
    good_count = sum(1 for p in GOOD_PATTERNS if re.search(p, content, re.IGNORECASE))

    # Date scoring (prefer recent files)
    try:
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        days_old = (datetime.now() - mtime).days
        date_score = max(0, 1 - days_old / 60)  # Full score if <60 days old
    except:
        date_score = 0.5

    # Determine tier
    if bad_count > 0:
        tier = 4
        include = False
        reason = f"Contains {bad_count} bad patterns"
    elif good_count >= 5:
        tier = 1
        include = True
        reason = f"High quality: {good_count} good patterns"
    elif good_count >= 2:
        tier = 2
        include = True
        reason = f"Good quality: {good_count} good patterns"
    elif good_count >= 1:
        tier = 3
        include = True
        reason = f"Moderate quality: {good_count} good patterns"
    else:
        tier = 4
        include = date_score > 0.5  # Only include recent content without patterns
        reason = "No strong patterns, including based on recency" if include else "No patterns, too old"

    return DocumentQuality(
        path=str(filepath),
        tier=tier,
        good_pattern_count=good_count,
        bad_pattern_count=bad_count,
        date_score=date_score,
        include=include,
        reason=reason
    )


def scan_repository() -> dict:
    """Scan the repository and categorize all documents."""
    results = {
        "gold_standard": [],
        "tier_1": [],
        "tier_2": [],
        "tier_3": [],
        "excluded": [],
        "stats": {}
    }

    # Check gold standard documents
    for doc in GOLD_DOCUMENTS:
        filepath = BASE_PATH / doc
        if filepath.exists():
            results["gold_standard"].append(str(filepath))

    # Scan key directories
    scan_dirs = [
        BASE_PATH / "research",
        BASE_PATH / "papers",
        BASE_PATH / "core_theory",
        BASE_PATH / "article_ideas_for_publishers",
    ]

    all_assessments = []

    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue

        for filepath in scan_dir.rglob("*.md"):
            assessment = assess_document_quality(filepath)
            all_assessments.append(assessment)

            if not assessment.include:
                results["excluded"].append(asdict(assessment))
            elif assessment.tier == 1:
                results["tier_1"].append(asdict(assessment))
            elif assessment.tier == 2:
                results["tier_2"].append(asdict(assessment))
            else:
                results["tier_3"].append(asdict(assessment))

    # Also scan .tex files in papers/
    for filepath in (BASE_PATH / "papers").rglob("*.tex"):
        assessment = assess_document_quality(filepath)
        all_assessments.append(assessment)
        if assessment.include and assessment.tier <= 2:
            results["tier_1" if assessment.tier == 1 else "tier_2"].append(asdict(assessment))

    # Statistics
    results["stats"] = {
        "total_scanned": len(all_assessments),
        "gold_standard": len(results["gold_standard"]),
        "tier_1": len(results["tier_1"]),
        "tier_2": len(results["tier_2"]),
        "tier_3": len(results["tier_3"]),
        "excluded": len(results["excluded"]),
        "include_rate": f"{100 * (1 - len(results['excluded']) / max(1, len(all_assessments))):.1f}%"
    }

    return results


def extract_derivation_examples(filepath: Path) -> list[TrainingExample]:
    """Extract training examples from a document."""
    examples = []

    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except:
        return examples

    # Pattern: Look for derivation sections
    derivation_patterns = [
        # Match headers with derivation content
        r"(?:###?\s*)?(Deriv(?:ation|ing)|Proof|Result)[:\s]+([^\n]+)\n((?:.*?\n)*?(?=###?\s|\Z))",
        # Match "X = formula (error%)" patterns
        r"([α⁻¹|sin²θ_W|Ω_Λ|Ω_m|m_p/m_e][^=]*)\s*=\s*([^(]+)\s*\(([0-9.]+)%?\s*error\)",
    ]

    for pattern in derivation_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
        for match in matches[:5]:  # Limit per pattern
            if len(match) >= 2:
                examples.append(TrainingExample(
                    instruction=f"Derive {match[0].strip()} from the Z² Framework.",
                    input="",
                    output=match[1].strip() if len(match) > 1 else "",
                    derivation_tier="first_principles",  # Will be refined
                    source_file=str(filepath),
                ))

    return examples


def build_corpus():
    """Main function to build the training corpus."""
    print("=" * 70)
    print("LegomenaXL-31B Training Corpus Builder")
    print("=" * 70)

    # Step 1: Scan repository
    print("\n[1/4] Scanning repository...")
    results = scan_repository()

    print(f"\nScan Results:")
    print(f"  Total scanned: {results['stats']['total_scanned']}")
    print(f"  Gold standard: {results['stats']['gold_standard']}")
    print(f"  Tier 1 (high quality): {results['stats']['tier_1']}")
    print(f"  Tier 2 (good quality): {results['stats']['tier_2']}")
    print(f"  Tier 3 (moderate): {results['stats']['tier_3']}")
    print(f"  Excluded: {results['stats']['excluded']}")
    print(f"  Inclusion rate: {results['stats']['include_rate']}")

    # Step 2: Save assessment
    output_dir = BASE_PATH / "LegomenaLLM" / "corpus"
    output_dir.mkdir(parents=True, exist_ok=True)

    assessment_file = output_dir / "quality_assessment.json"
    with open(assessment_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n[2/4] Quality assessment saved to: {assessment_file}")

    # Step 3: Extract examples from gold standard
    print("\n[3/4] Extracting training examples...")
    all_examples = []

    for doc_path in results["gold_standard"]:
        filepath = Path(doc_path)
        if filepath.exists():
            examples = extract_derivation_examples(filepath)
            all_examples.extend(examples)
            print(f"  {filepath.name}: {len(examples)} examples")

    # Step 4: Save corpus
    corpus_file = output_dir / "training_corpus.jsonl"
    with open(corpus_file, 'w') as f:
        for ex in all_examples:
            f.write(json.dumps(asdict(ex)) + "\n")

    print(f"\n[4/4] Training corpus saved to: {corpus_file}")
    print(f"  Total examples: {len(all_examples)}")

    # Summary
    print("\n" + "=" * 70)
    print("CORPUS BUILD COMPLETE")
    print("=" * 70)
    print(f"\nFiles created:")
    print(f"  - {assessment_file}")
    print(f"  - {corpus_file}")
    print(f"\nNext steps:")
    print("  1. Review quality_assessment.json for excluded files")
    print("  2. Manually curate training_corpus.jsonl")
    print("  3. Add negative examples from daemon numerology")
    print("  4. Run fine-tuning with Gemma 4 31B")


if __name__ == "__main__":
    build_corpus()
