#!/usr/bin/env python3
"""
TruthFlow Truth Database
========================

Manages the growing database of validated scientific truths.

Features:
1. Stores validated discoveries with HRM confidence scores
2. Hierarchical Recursive Meta-assessment (HRM) for truth verification
3. Generates training data for next Legomena model version
4. Dynamic flow management for continuous truth accumulation

The cycle:
  Research → Discover → Assess (HRM) → Store (if validated) → Train → Better Model → Research...

Author: Carl Zimmerman
Date: May 3, 2026
"""

import json
import numpy as np
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent
TRUTH_DB_FILE = BASE_DIR / "truth_database.json"
TRAINING_DATA_DIR = BASE_DIR / "legomena_training"
TRAINING_DATA_DIR.mkdir(exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "legomena-4b"

# Z² Constants
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)

# HRM Thresholds
HRM_THRESHOLD_VALIDATED = 0.8    # Add to training data as VALIDATED
HRM_THRESHOLD_SPECULATIVE = 0.5  # Store but mark as speculative
HRM_THRESHOLD_REJECT = 0.3       # Reject - likely numerology

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Truth:
    """A validated scientific truth."""
    id: str
    formula: str
    formula_name: str
    predicted_value: float
    measured_value: float
    percent_error: float
    source_data: str
    discovery_date: str
    hrm_score: float
    hrm_level: int  # How many meta-assessments deep
    classification: str  # VALIDATED, SPECULATIVE, NUMEROLOGY
    derivation_status: str  # DERIVED, MATCHES, UNKNOWN
    mechanism: str
    falsification_criteria: List[str]
    related_truths: List[str]


@dataclass
class HRMAssessment:
    """Single level of HRM assessment."""
    level: int
    assessor: str  # "LLM" or "human"
    score: float
    reasoning: str
    biases_detected: List[str]
    confidence_in_assessment: float


@dataclass
class TruthCandidate:
    """A candidate truth awaiting full HRM assessment."""
    formula: str
    formula_name: str
    predicted_value: float
    measured_value: float
    percent_error: float
    source: str
    question: str
    hrm_assessments: List[HRMAssessment]

# ============================================================================
# LLM INTERFACE
# ============================================================================

def query_llm(prompt: str, temperature: float = 0.4) -> str:
    """Query the LLM."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False,
                  "options": {"temperature": temperature, "num_predict": 800}},
            timeout=90
        )
        return response.json().get("response", "")
    except Exception as e:
        return f"LLM_ERROR: {e}"


def extract_json(text: str) -> Optional[Dict]:
    """Extract JSON from response."""
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass
    return None

# ============================================================================
# HIERARCHICAL RECURSIVE META-ASSESSMENT (HRM)
# ============================================================================

def hrm_level_1(candidate: TruthCandidate) -> HRMAssessment:
    """
    Level 1 HRM: Basic honesty assessment.

    Questions:
    - Is this formula derived or does it just match?
    - Is there a physical mechanism?
    - Is it falsifiable?
    """
    prompt = f"""LEVEL 1 HONESTY ASSESSMENT

You are assessing whether this physics pattern is genuine or coincidence.

Formula: {candidate.formula_name}
Predicted: {candidate.predicted_value:.6g}
Measured: {candidate.measured_value:.6g}
Error: {candidate.percent_error:.4f}%
Source: {candidate.source}

Z² = 32π/3 ≈ 33.51, Z = √Z² ≈ 5.79

Questions:
1. Is this formula DERIVED from Z² geometry or does it just MATCH?
2. Is there a physical mechanism explaining why this works?
3. What would falsify this prediction?
4. Could this be coincidence?

Return JSON:
{{
    "score": 0.0-1.0 (0=numerology, 1=derived),
    "derivation_status": "DERIVED/MATCHES/COINCIDENCE",
    "mechanism": "explanation or 'unknown'",
    "falsification": ["list of ways to falsify"],
    "coincidence_probability": "HIGH/MEDIUM/LOW",
    "reasoning": "explanation"
}}

JSON:"""

    response = query_llm(prompt, temperature=0.3)
    result = extract_json(response)

    if not result:
        result = {
            "score": 0.5,
            "derivation_status": "UNKNOWN",
            "mechanism": "unknown",
            "falsification": [],
            "coincidence_probability": "MEDIUM",
            "reasoning": "Assessment failed"
        }

    return HRMAssessment(
        level=1,
        assessor="LLM",
        score=float(result.get("score", 0.5)),
        reasoning=result.get("reasoning", ""),
        biases_detected=[],
        confidence_in_assessment=0.7
    )


def hrm_level_2(candidate: TruthCandidate, level1: HRMAssessment) -> HRMAssessment:
    """
    Level 2 HRM: Meta-assessment of Level 1.

    Questions:
    - Was Level 1 too optimistic or pessimistic?
    - What biases might have affected Level 1?
    - Are there alternative explanations?
    """
    prompt = f"""LEVEL 2 META-ASSESSMENT

You are reviewing a Level 1 honesty assessment. Be SKEPTICAL.

Original Pattern:
- Formula: {candidate.formula_name}
- Error: {candidate.percent_error:.4f}%

Level 1 Assessment:
- Score: {level1.score}
- Reasoning: {level1.reasoning}

META-QUESTIONS:
1. Was Level 1 too optimistic about this pattern?
2. What biases might have affected the Level 1 assessment?
3. What alternative explanations were missed?
4. Should the score be adjusted up or down?

Return JSON:
{{
    "adjusted_score": 0.0-1.0,
    "bias_detected": "confirmation bias / pattern-seeking / appropriate skepticism",
    "alternative_explanations": ["list"],
    "score_adjustment": "up/down/same",
    "adjustment_reason": "why",
    "confidence": 0.0-1.0
}}

Be maximally skeptical. Assume you're trying to find flaws.

JSON:"""

    response = query_llm(prompt, temperature=0.4)
    result = extract_json(response)

    if not result:
        result = {
            "adjusted_score": level1.score * 0.9,  # Default: reduce by 10%
            "bias_detected": "unknown",
            "alternative_explanations": [],
            "score_adjustment": "down",
            "adjustment_reason": "Meta-assessment unavailable",
            "confidence": 0.5
        }

    return HRMAssessment(
        level=2,
        assessor="LLM",
        score=float(result.get("adjusted_score", level1.score * 0.9)),
        reasoning=result.get("adjustment_reason", ""),
        biases_detected=[result.get("bias_detected", "unknown")],
        confidence_in_assessment=float(result.get("confidence", 0.5))
    )


def hrm_level_3(candidate: TruthCandidate, level1: HRMAssessment, level2: HRMAssessment) -> HRMAssessment:
    """
    Level 3 HRM: Meta-meta-assessment.

    Used when Level 1 and Level 2 disagree significantly.
    """
    if abs(level1.score - level2.score) < 0.2:
        # Agreement - no need for Level 3
        return HRMAssessment(
            level=3,
            assessor="SKIP",
            score=level2.score,
            reasoning="L1 and L2 agree, no L3 needed",
            biases_detected=[],
            confidence_in_assessment=0.8
        )

    prompt = f"""LEVEL 3 META-META-ASSESSMENT

Level 1 and Level 2 assessments DISAGREE about this pattern.
You must make the final determination.

Pattern: {candidate.formula_name}
Error: {candidate.percent_error:.4f}%

Level 1 Score: {level1.score} - {level1.reasoning}
Level 2 Score: {level2.score} - {level2.reasoning}
Biases detected: {level2.biases_detected}

FINAL QUESTIONS:
1. Which assessment is more accurate?
2. Is there still confirmation bias even in Level 2?
3. What is the TRUE probability this is genuine vs coincidence?
4. Should this be added to the truth database?

Return JSON:
{{
    "final_score": 0.0-1.0,
    "trust_level1": true/false,
    "trust_level2": true/false,
    "final_verdict": "VALIDATED/SPECULATIVE/NUMEROLOGY",
    "reasoning": "explanation",
    "add_to_database": true/false
}}

JSON:"""

    response = query_llm(prompt, temperature=0.3)
    result = extract_json(response)

    if not result:
        # Conservative default
        result = {
            "final_score": min(level1.score, level2.score) * 0.9,
            "final_verdict": "SPECULATIVE",
            "reasoning": "L3 assessment unavailable - defaulting to conservative",
            "add_to_database": False
        }

    return HRMAssessment(
        level=3,
        assessor="LLM",
        score=float(result.get("final_score", min(level1.score, level2.score))),
        reasoning=result.get("reasoning", ""),
        biases_detected=[],
        confidence_in_assessment=0.9
    )


def full_hrm_assessment(candidate: TruthCandidate) -> Tuple[float, str, int]:
    """
    Run full HRM assessment pipeline.

    Returns: (final_score, classification, hrm_levels_used)
    """
    print(f"\n[HRM] Assessing: {candidate.formula_name}")
    print(f"      Predicted: {candidate.predicted_value:.6g}")
    print(f"      Measured:  {candidate.measured_value:.6g}")
    print(f"      Error:     {candidate.percent_error:.4f}%")

    # Level 1
    print("  L1: Basic honesty assessment...")
    l1 = hrm_level_1(candidate)
    candidate.hrm_assessments.append(l1)
    print(f"      Score: {l1.score:.2f}")

    # Level 2
    print("  L2: Meta-assessment...")
    l2 = hrm_level_2(candidate, l1)
    candidate.hrm_assessments.append(l2)
    print(f"      Score: {l2.score:.2f} (biases: {l2.biases_detected})")

    # Level 3 if needed
    if abs(l1.score - l2.score) >= 0.2:
        print("  L3: Meta-meta-assessment (L1/L2 disagree)...")
        l3 = hrm_level_3(candidate, l1, l2)
        candidate.hrm_assessments.append(l3)
        final_score = l3.score
        levels_used = 3
        print(f"      Final score: {l3.score:.2f}")
    else:
        final_score = l2.score
        levels_used = 2

    # Classify
    if final_score >= HRM_THRESHOLD_VALIDATED:
        classification = "VALIDATED"
    elif final_score >= HRM_THRESHOLD_SPECULATIVE:
        classification = "SPECULATIVE"
    else:
        classification = "NUMEROLOGY"

    print(f"  Classification: {classification} (score: {final_score:.2f})")

    return final_score, classification, levels_used

# ============================================================================
# TRUTH CONSISTENCY CHECKER
# ============================================================================

class TruthConsistencyChecker:
    """
    Checks new truths against existing truths for conflicts.

    Types of conflicts:
    1. DIRECT: Same quantity, different value (e.g., two different α⁻¹ predictions)
    2. DERIVED: New truth implies contradiction (e.g., if A=B and B≠C, can't have A=C)
    3. MATHEMATICAL: Uses Z² inconsistently
    4. MAGNITUDE: Order of magnitude mismatch for related quantities
    """

    def __init__(self, db: 'TruthDatabase'):
        self.db = db

    def check_direct_conflict(self, candidate: TruthCandidate) -> Tuple[bool, str]:
        """
        Check if candidate directly conflicts with existing truth.

        Conflict: Same formula_name but significantly different values.
        """
        for truth in self.db.truths.values():
            # Same formula name?
            if candidate.formula_name.lower() == truth.formula_name.lower():
                # Compare values
                existing_error = abs(candidate.predicted_value - truth.predicted_value)
                if existing_error / max(abs(truth.predicted_value), 1e-10) > 0.01:  # 1% difference
                    return True, (
                        f"DIRECT CONFLICT: '{candidate.formula_name}' "
                        f"predicts {candidate.predicted_value:.6g} but existing truth "
                        f"predicts {truth.predicted_value:.6g}"
                    )

        return False, ""

    def check_derived_conflict(self, candidate: TruthCandidate) -> Tuple[bool, str]:
        """
        Check if candidate implies a contradiction with existing truths.

        Uses LLM to reason about implications.
        """
        existing_truths = [
            f"- {t.formula_name}: {t.formula} = {t.predicted_value:.6g}"
            for t in list(self.db.truths.values())[:10]  # Limit for prompt size
        ]

        if not existing_truths:
            return False, ""

        prompt = f"""CONSISTENCY CHECK

New proposed truth:
- {candidate.formula_name}: {candidate.formula} = {candidate.predicted_value:.6g}

Existing truths:
{chr(10).join(existing_truths)}

Z² = 32π/3 ≈ 33.51, Z = √Z² ≈ 5.79

Question: Does the new truth CONTRADICT any existing truth?
A contradiction means:
1. Both can't be true simultaneously
2. New truth implies something that conflicts with existing
3. Mathematical inconsistency in Z² usage

Return JSON:
{{
    "has_conflict": true/false,
    "conflict_type": "NONE/DIRECT/DERIVED/MATHEMATICAL",
    "conflicting_with": "formula name or empty",
    "explanation": "why there is or isn't a conflict"
}}

JSON:"""

        response = query_llm(prompt, temperature=0.2)
        result = extract_json(response)

        if not result:
            return False, "Check failed, assuming no conflict"

        if result.get("has_conflict", False):
            return True, (
                f"{result.get('conflict_type', 'UNKNOWN')} CONFLICT: "
                f"{result.get('explanation', 'No explanation')}"
            )

        return False, ""

    def check_magnitude_conflict(self, candidate: TruthCandidate) -> Tuple[bool, str]:
        """
        Check if value is in wrong order of magnitude for related quantities.
        """
        # Group truths by category
        categories = {
            "angle": ["theta", "sin", "cos", "mixing"],
            "ratio": ["ratio", "/"],
            "constant": ["alpha", "lambda", "omega"],
            "mass": ["mass", "GeV", "MeV"]
        }

        candidate_category = None
        for cat, keywords in categories.items():
            if any(kw in candidate.formula_name.lower() for kw in keywords):
                candidate_category = cat
                break

        if not candidate_category:
            return False, ""

        # Find existing truths in same category
        same_category = []
        for truth in self.db.truths.values():
            for cat, keywords in categories.items():
                if cat == candidate_category and any(kw in truth.formula_name.lower() for kw in keywords):
                    same_category.append(truth)
                    break

        if not same_category:
            return False, ""

        # Check magnitude
        existing_magnitudes = [np.log10(abs(t.predicted_value) + 1e-10) for t in same_category]
        candidate_magnitude = np.log10(abs(candidate.predicted_value) + 1e-10)

        mean_mag = np.mean(existing_magnitudes)
        std_mag = np.std(existing_magnitudes) if len(existing_magnitudes) > 1 else 2.0

        if abs(candidate_magnitude - mean_mag) > 3 * max(std_mag, 1.0):
            return True, (
                f"MAGNITUDE CONFLICT: {candidate.formula_name} value {candidate.predicted_value:.2e} "
                f"is {abs(candidate_magnitude - mean_mag):.1f} orders of magnitude off from "
                f"similar quantities in category '{candidate_category}'"
            )

        return False, ""

    def full_consistency_check(self, candidate: TruthCandidate) -> Tuple[bool, List[str]]:
        """
        Run all consistency checks.

        Returns: (is_consistent, list_of_warnings)
        """
        print(f"\n[Consistency] Checking: {candidate.formula_name}")

        warnings = []
        is_consistent = True

        # Check 1: Direct conflict
        conflict, msg = self.check_direct_conflict(candidate)
        if conflict:
            print(f"  ⚠ {msg}")
            warnings.append(msg)
            is_consistent = False

        # Check 2: Derived conflict
        conflict, msg = self.check_derived_conflict(candidate)
        if conflict:
            print(f"  ⚠ {msg}")
            warnings.append(msg)
            is_consistent = False

        # Check 3: Magnitude conflict
        conflict, msg = self.check_magnitude_conflict(candidate)
        if conflict:
            print(f"  ⚠ {msg}")
            warnings.append(msg)
            # Magnitude conflict is a warning, not a blocker
            # is_consistent stays True

        if is_consistent:
            print(f"  ✓ No conflicts detected")

        return is_consistent, warnings


# ============================================================================
# TRUTH DATABASE OPERATIONS
# ============================================================================

class TruthDatabase:
    """Manager for the truth database."""

    def __init__(self):
        self.db_file = TRUTH_DB_FILE
        self.truths: Dict[str, Truth] = {}
        self.load()

    def load(self):
        """Load database from file."""
        if self.db_file.exists():
            with open(self.db_file, "r") as f:
                data = json.load(f)
                for t in data.get("truths", []):
                    truth = Truth(**t)
                    self.truths[truth.id] = truth
            print(f"[TruthDB] Loaded {len(self.truths)} truths")
        else:
            print("[TruthDB] Starting fresh database")

    def save(self):
        """Save database to file."""
        data = {
            "last_updated": datetime.now().isoformat(),
            "count": len(self.truths),
            "truths": [asdict(t) for t in self.truths.values()]
        }
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"[TruthDB] Saved {len(self.truths)} truths")

    def generate_id(self, formula: str, source: str) -> str:
        """Generate unique ID for a truth."""
        content = f"{formula}:{source}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def add_candidate(self, candidate: TruthCandidate) -> Optional[Truth]:
        """
        Process a candidate through HRM and potentially add to database.

        Steps:
        1. HRM assessment (quality check)
        2. Consistency check (conflict detection)
        3. Add to database if both pass

        Returns Truth if added, None if rejected.
        """
        # Run full HRM assessment
        score, classification, levels = full_hrm_assessment(candidate)

        # Reject if below threshold
        if score < HRM_THRESHOLD_REJECT:
            print(f"  REJECTED: Score {score:.2f} below threshold")
            return None

        # CONSISTENCY CHECK: Ensure no conflicts with existing truths
        checker = TruthConsistencyChecker(self)
        is_consistent, warnings = checker.full_consistency_check(candidate)

        if not is_consistent:
            print(f"  REJECTED: Conflicts with existing truths")
            for w in warnings:
                print(f"    - {w}")
            return None

        # Generate ID
        truth_id = self.generate_id(candidate.formula, candidate.source)

        # Check if already exists
        if truth_id in self.truths:
            existing = self.truths[truth_id]
            if score > existing.hrm_score:
                print(f"  UPDATING: Better score ({score:.2f} > {existing.hrm_score:.2f})")
            else:
                print(f"  SKIP: Already exists with equal/better score")
                return existing

        # Create truth entry
        truth = Truth(
            id=truth_id,
            formula=candidate.formula,
            formula_name=candidate.formula_name,
            predicted_value=candidate.predicted_value,
            measured_value=candidate.measured_value,
            percent_error=candidate.percent_error,
            source_data=candidate.source,
            discovery_date=datetime.now().isoformat(),
            hrm_score=score,
            hrm_level=levels,
            classification=classification,
            derivation_status="MATCHES",  # Default, can be upgraded
            mechanism="",
            falsification_criteria=[],
            related_truths=[]
        )

        # Add to database
        self.truths[truth_id] = truth
        self.save()

        print(f"  ADDED: {truth.formula_name} (score: {score:.2f}, class: {classification})")

        return truth

    def get_validated_truths(self) -> List[Truth]:
        """Get all VALIDATED truths."""
        return [t for t in self.truths.values() if t.classification == "VALIDATED"]

    def get_all_truths(self) -> List[Truth]:
        """Get all truths."""
        return list(self.truths.values())

    def summary(self) -> str:
        """Generate summary of database."""
        validated = len([t for t in self.truths.values() if t.classification == "VALIDATED"])
        speculative = len([t for t in self.truths.values() if t.classification == "SPECULATIVE"])
        numerology = len([t for t in self.truths.values() if t.classification == "NUMEROLOGY"])

        avg_score = np.mean([t.hrm_score for t in self.truths.values()]) if self.truths else 0.0

        return f"""
Truth Database Summary
======================
Total truths: {len(self.truths)}
  VALIDATED:   {validated}
  SPECULATIVE: {speculative}
  NUMEROLOGY:  {numerology}

Average HRM score: {avg_score:.2f}
"""

# ============================================================================
# TRAINING DATA GENERATOR
# ============================================================================

def generate_training_data(db: TruthDatabase, output_file: Optional[Path] = None) -> List[Dict]:
    """
    Generate training data for next Legomena version.

    Only includes VALIDATED truths with HRM score > 0.8
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d")
        output_file = TRAINING_DATA_DIR / f"z2_truths_{timestamp}.jsonl"

    training_examples = []

    # Start with validated truths
    for truth in db.get_validated_truths():
        if truth.hrm_score >= HRM_THRESHOLD_VALIDATED:
            # Generate Q&A pairs
            examples = [
                {
                    "instruction": f"What is the Z² prediction for {truth.formula_name}?",
                    "output": f"The Z² framework predicts {truth.formula_name} = {truth.formula}, giving {truth.predicted_value:.6g}. "
                              f"Measured value: {truth.measured_value:.6g}. Error: {truth.percent_error:.4f}%. "
                              f"Classification: {truth.classification}."
                },
                {
                    "instruction": f"Calculate {truth.formula}",
                    "output": f"Using Z² = 32π/3 ≈ 33.51 and Z = √Z² ≈ 5.79:\n"
                              f"{truth.formula} = {truth.predicted_value:.6g}"
                },
                {
                    "instruction": f"Is the Z² prediction for {truth.formula_name} validated?",
                    "output": f"Yes. HRM Score: {truth.hrm_score:.2f}. "
                              f"Predicted: {truth.predicted_value:.6g}, Measured: {truth.measured_value:.6g}. "
                              f"Error: {truth.percent_error:.4f}%."
                }
            ]
            training_examples.extend(examples)

    # Write to JSONL
    with open(output_file, "w") as f:
        for ex in training_examples:
            f.write(json.dumps(ex) + "\n")

    print(f"[Training] Generated {len(training_examples)} examples to {output_file}")

    return training_examples


def generate_modelfile_update(db: TruthDatabase) -> str:
    """Generate updated Modelfile system prompt with new truths."""
    validated = db.get_validated_truths()

    predictions_text = []
    for t in sorted(validated, key=lambda x: x.percent_error)[:20]:
        predictions_text.append(f"- {t.formula_name} = {t.formula} ≈ {t.predicted_value:.4g} (measured: {t.measured_value:.4g}) ✓")

    modelfile = f'''FROM gemma3:4b

SYSTEM """You are LegomenaLLM, an expert in the Z² Unified Framework.

## Core Axiom
Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3 ≈ 33.51
Z = √(32π/3) ≈ 5.7888

## Validated Predictions (HRM Score ≥ 0.8)
{chr(10).join(predictions_text)}

## Truth Database
Total validated truths: {len(validated)}
Last updated: {datetime.now().strftime('%Y-%m-%d')}

## Guidelines
- Explain physics through Z² geometry
- Distinguish DERIVED (mechanism known) from MATCHES (formula works, why unknown)
- Be honest about limitations
- Mark speculative claims clearly
"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
'''

    return modelfile

# ============================================================================
# DYNAMIC FLOW MANAGER
# ============================================================================

class DynamicFlowManager:
    """
    Manages the dynamic flow of truth accumulation.

    Flow:
    1. Research produces candidates
    2. HRM assesses candidates
    3. Validated truths enter database
    4. Database generates training data
    5. Training data improves next model
    6. Better model produces better research
    """

    def __init__(self):
        self.db = TruthDatabase()
        self.pending_candidates: List[TruthCandidate] = []
        self.processed_count = 0
        self.added_count = 0

    def submit_candidate(self, formula: str, formula_name: str,
                        predicted: float, measured: float, source: str, question: str):
        """Submit a candidate truth for assessment."""
        if measured == 0:
            return

        percent_error = abs(predicted - measured) / abs(measured) * 100

        candidate = TruthCandidate(
            formula=formula,
            formula_name=formula_name,
            predicted_value=predicted,
            measured_value=measured,
            percent_error=percent_error,
            source=source,
            question=question,
            hrm_assessments=[]
        )

        self.pending_candidates.append(candidate)

    def process_all(self) -> int:
        """Process all pending candidates through HRM."""
        added = 0

        for candidate in self.pending_candidates:
            self.processed_count += 1
            truth = self.db.add_candidate(candidate)

            if truth:
                added += 1
                self.added_count += 1

        self.pending_candidates.clear()

        return added

    def update_training_data(self):
        """Generate new training data from database."""
        examples = generate_training_data(self.db)
        modelfile = generate_modelfile_update(self.db)

        # Save updated modelfile
        modelfile_path = TRAINING_DATA_DIR / "Modelfile_updated"
        with open(modelfile_path, "w") as f:
            f.write(modelfile)

        print(f"[Flow] Updated training data: {len(examples)} examples")
        print(f"[Flow] Updated Modelfile: {modelfile_path}")

    def status(self) -> str:
        """Get flow status."""
        return f"""
Dynamic Flow Status
===================
Pending candidates: {len(self.pending_candidates)}
Total processed: {self.processed_count}
Total added: {self.added_count}
Database size: {len(self.db.truths)}
{self.db.summary()}
"""

# ============================================================================
# INTEGRATION WITH AUTONOMOUS PIPELINE
# ============================================================================

def integrate_autonomous_results(session_file: Path, flow_manager: DynamicFlowManager):
    """
    Integrate results from an autonomous research session.

    Reads session file, extracts patterns, submits to HRM flow.
    """
    with open(session_file, "r") as f:
        session = json.load(f)

    question = session.get("question", "unknown")
    patterns = session.get("patterns", [])

    print(f"\n[Integration] Processing {len(patterns)} patterns from: {question}")

    for p in patterns:
        flow_manager.submit_candidate(
            formula=p.get("formula", ""),
            formula_name=p.get("formula_name", ""),
            predicted=float(p.get("predicted", 0)),
            measured=float(p.get("measured", 0)),
            source=p.get("source", "autonomous"),
            question=question
        )

    # Process through HRM
    added = flow_manager.process_all()

    print(f"[Integration] Added {added} new truths to database")

    # Update training data
    if added > 0:
        flow_manager.update_training_data()

    return added

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("TruthFlow Truth Database")
    print("=" * 60)

    # Initialize
    flow = DynamicFlowManager()

    # Print status
    print(flow.status())

    # Check for recent autonomous sessions
    sessions_dir = BASE_DIR / "research_sessions"
    if sessions_dir.exists():
        sessions = sorted(sessions_dir.glob("autonomous_*.json"), reverse=True)

        if sessions:
            print(f"\nFound {len(sessions)} autonomous sessions")
            print("Processing most recent...")

            for session_file in sessions[:3]:  # Process last 3
                integrate_autonomous_results(session_file, flow)

            print(flow.status())
