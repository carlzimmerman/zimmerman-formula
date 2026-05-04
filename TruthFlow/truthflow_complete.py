#!/usr/bin/env python3
"""
TruthFlow Complete - End-to-End Scientific Discovery Engine
============================================================

This system mimics the full scientific method with LLM assistance:

1. INPUT: Research question or topic
2. LITERATURE: Fetch papers, parse for testable claims
3. HYPOTHESIZE: Extract computationally testable predictions
4. EXPERIMENT: Generate Python scripts to test against real data
5. EVALUATE: Run experiments, classify results
6. LEARN: Analyze failures, generate new hypotheses
7. VALIDATE: Honesty assessment of successful predictions
8. META-VALIDATE: Honesty assessment of the honesty assessment
9. TRUTH: Arrive at first-principles scientific truth

Uses Legomena LLM (fine-tuned on Z² framework) throughout.

Author: Carl Zimmerman
Date: May 3, 2026
"""

import json
import requests
import numpy as np
import subprocess
import tempfile
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
import re
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "legomena"  # Our fine-tuned Z² model
ARXIV_API = "http://export.arxiv.org/api/query"

# Z² Constants (immutable)
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)

# Data directories
BASE_DIR = Path(__file__).parent
RESEARCH_DIR = BASE_DIR / "research_sessions"
RESEARCH_DIR.mkdir(exist_ok=True)

# ============================================================================
# MEASUREMENT DATABASE (Ground Truth)
# ============================================================================

MEASUREMENTS = {
    # Cosmology
    "Omega_Lambda": {"value": 0.6847, "uncertainty": 0.0073, "source": "Planck 2020"},
    "Omega_m": {"value": 0.315, "uncertainty": 0.007, "source": "Planck 2020"},
    "w0": {"value": -0.99, "uncertainty": 0.15, "source": "DESI 2024"},
    "H0_planck": {"value": 67.4, "uncertainty": 0.5, "source": "Planck 2020"},
    "H0_local": {"value": 73.04, "uncertainty": 1.04, "source": "SH0ES 2022"},
    "spectral_index_ns": {"value": 0.9649, "uncertainty": 0.0042, "source": "Planck 2020"},
    "optical_depth_tau": {"value": 0.0544, "uncertainty": 0.007, "source": "Planck 2020"},
    "tensor_scalar_r": {"value": None, "upper_limit": 0.036, "source": "BICEP/Keck 2021"},

    # Electroweak
    "alpha_inverse": {"value": 137.035999084, "uncertainty": 0.000000021, "source": "CODATA 2022"},
    "sin2_theta_W": {"value": 0.23122, "uncertainty": 0.00004, "source": "PDG 2024"},
    "alpha_strong": {"value": 0.1180, "uncertainty": 0.0009, "source": "PDG 2024"},
    "W_mass_GeV": {"value": 80.377, "uncertainty": 0.012, "source": "PDG 2024"},
    "Z_mass_GeV": {"value": 91.1876, "uncertainty": 0.0021, "source": "PDG 2024"},
    "Higgs_mass_GeV": {"value": 125.25, "uncertainty": 0.17, "source": "PDG 2024"},

    # Lepton masses
    "muon_electron_ratio": {"value": 206.7682830, "uncertainty": 0.0000046, "source": "CODATA 2022"},
    "tau_muon_ratio": {"value": 16.817029, "uncertainty": 0.0001, "source": "CODATA 2022"},
    "tau_electron_ratio": {"value": 3477.23, "uncertainty": 0.23, "source": "CODATA 2022"},
    "proton_electron_ratio": {"value": 1836.15267343, "uncertainty": 0.00000011, "source": "CODATA 2022"},

    # Quark mass ratios
    "top_charm_ratio": {"value": 136.0, "uncertainty": 3.0, "source": "PDG 2024"},
    "bottom_charm_ratio": {"value": 3.29, "uncertainty": 0.05, "source": "PDG 2024"},
    "charm_strange_ratio": {"value": 13.6, "uncertainty": 0.4, "source": "PDG 2024"},
    "strange_down_ratio": {"value": 20.2, "uncertainty": 1.5, "source": "PDG 2024"},
    "charm_up_ratio": {"value": 588.0, "uncertainty": 109.3, "source": "PDG 2024"},
    "up_down_ratio": {"value": 0.462, "uncertainty": 0.030, "source": "PDG 2024"},

    # Neutrinos
    "theta_12_degrees": {"value": 33.41, "uncertainty": 0.82, "source": "NuFIT 5.2"},
    "theta_23_degrees": {"value": 42.2, "uncertainty": 1.1, "source": "NuFIT 5.2"},
    "theta_13_degrees": {"value": 8.58, "uncertainty": 0.11, "source": "NuFIT 5.2"},
    "delta_CP_degrees": {"value": 195.0, "uncertainty": 25.0, "source": "T2K+NOvA 2024"},
    "dm21_squared": {"value": 7.53e-5, "uncertainty": 0.18e-5, "source": "NuFIT 5.2"},
    "dm31_squared": {"value": 2.453e-3, "uncertainty": 0.033e-3, "source": "NuFIT 5.2"},

    # CKM matrix
    "V_ud": {"value": 0.97373, "uncertainty": 0.00031, "source": "PDG 2024"},
    "V_us": {"value": 0.22650, "uncertainty": 0.00048, "source": "PDG 2024"},
    "V_ub": {"value": 0.00382, "uncertainty": 0.00020, "source": "PDG 2024"},
    "V_cb": {"value": 0.04182, "uncertainty": 0.00085, "source": "PDG 2024"},

    # Other
    "muon_g2_anomaly": {"value": 2.51e-9, "uncertainty": 0.59e-9, "source": "Fermilab 2023"},
    "baryon_asymmetry_eta": {"value": 6.14e-10, "uncertainty": 0.25e-10, "source": "Planck 2020"},
    "gauge_bosons": {"value": 12, "uncertainty": 0, "source": "Standard Model"},
    "fermion_generations": {"value": 3, "uncertainty": 0, "source": "Standard Model"},
}

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Claim:
    """A testable claim extracted from literature."""
    statement: str
    formula: Optional[str]
    predicted_value: Optional[float]
    measurement_key: Optional[str]
    source_paper: str
    confidence: str  # HIGH, MEDIUM, LOW

@dataclass
class Experiment:
    """A computational experiment to test a claim."""
    claim: Claim
    python_code: str
    result: Optional[float] = None
    measured: Optional[float] = None
    uncertainty: Optional[float] = None
    sigma: Optional[float] = None
    percent_error: Optional[float] = None
    status: str = "PENDING"  # PENDING, VALIDATED, PRECISE, TENSION, FAILED, ERROR

@dataclass
class HonestyAssessment:
    """Assessment of whether a result is genuinely derived or just matches."""
    experiment: Experiment
    derivation_status: str  # DERIVED, MATCHES, SPECULATIVE, NUMEROLOGY
    mechanism_understood: bool
    falsifiable: bool
    independent_tests: List[str]
    honest_limitations: List[str]
    confidence_score: float  # 0-1

@dataclass
class MetaAssessment:
    """Meta-assessment of the honesty assessment itself."""
    honesty_assessment: HonestyAssessment
    bias_check: str
    alternative_explanations: List[str]
    statistical_significance: str
    reproducibility: str
    first_principles_status: str  # PROVEN, SUPPORTED, SPECULATIVE, UNFOUNDED
    final_verdict: str

@dataclass
class ResearchSession:
    """Complete research session tracking."""
    question: str
    timestamp: str
    papers_fetched: List[Dict]
    claims_extracted: List[Claim]
    experiments: List[Experiment]
    honesty_assessments: List[HonestyAssessment]
    meta_assessments: List[MetaAssessment]
    learnings: List[str]
    next_steps: List[str]

# ============================================================================
# LLM INTERFACE
# ============================================================================

def query_llm(prompt: str, temperature: float = 0.7, max_retries: int = 3) -> str:
    """Query the Legomena LLM."""
    for attempt in range(max_retries):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature}
                },
                timeout=120
            )
            return response.json().get("response", "")
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return f"LLM_ERROR: {e}"
    return "LLM_ERROR: Max retries exceeded"

def extract_json(text: str) -> Optional[Dict]:
    """Extract JSON from LLM response."""
    try:
        # Find JSON in response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass

    # Try array
    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass

    return None

# ============================================================================
# PHASE 1: LITERATURE FETCH
# ============================================================================

def fetch_arxiv_papers(query: str, max_results: int = 20) -> List[Dict]:
    """Fetch papers from arXiv related to the query."""
    print(f"\n[LITERATURE] Fetching papers for: {query}")

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    try:
        response = requests.get(ARXIV_API, params=params, timeout=30)

        # Parse XML response
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)

        papers = []
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        for entry in root.findall("atom:entry", ns):
            paper = {
                "title": entry.find("atom:title", ns).text.strip().replace("\n", " "),
                "summary": entry.find("atom:summary", ns).text.strip().replace("\n", " ")[:500],
                "arxiv_id": entry.find("atom:id", ns).text.split("/")[-1],
                "published": entry.find("atom:published", ns).text[:10],
            }
            papers.append(paper)

        print(f"  Found {len(papers)} papers")
        return papers

    except Exception as e:
        print(f"  Error fetching papers: {e}")
        return []

# ============================================================================
# PHASE 2: PARSE LITERATURE FOR TESTABLE CLAIMS
# ============================================================================

def parse_for_claims(papers: List[Dict], research_question: str) -> List[Claim]:
    """Use LLM to extract testable claims from papers."""
    print(f"\n[PARSE] Extracting testable claims from {len(papers)} papers...")

    claims = []

    for paper in papers[:10]:  # Limit to first 10 for efficiency
        prompt = f"""You are analyzing physics papers to extract testable claims.

Research question: {research_question}

Paper: {paper['title']}
Abstract: {paper['summary']}

Extract any claims that can be tested computationally against measurements.
Focus on:
- Numerical predictions (values, ratios, constants)
- Mathematical relationships
- Quantitative comparisons

Return a JSON object:
{{
    "claims": [
        {{
            "statement": "The ratio X equals Y",
            "formula": "X/Y = 1.234 or python expression",
            "measurement_key": "name from: {list(MEASUREMENTS.keys())[:10]}...",
            "confidence": "HIGH/MEDIUM/LOW"
        }}
    ]
}}

If no testable claims found, return {{"claims": []}}

JSON:"""

        response = query_llm(prompt, temperature=0.3)
        result = extract_json(response)

        if result and "claims" in result:
            for c in result["claims"]:
                if c.get("statement"):
                    claims.append(Claim(
                        statement=c.get("statement", ""),
                        formula=c.get("formula"),
                        predicted_value=None,
                        measurement_key=c.get("measurement_key"),
                        source_paper=paper["arxiv_id"],
                        confidence=c.get("confidence", "LOW")
                    ))

    print(f"  Extracted {len(claims)} testable claims")
    return claims

# ============================================================================
# PHASE 3: GENERATE EXPERIMENT SCRIPTS
# ============================================================================

def generate_experiment(claim: Claim) -> Experiment:
    """Generate Python code to test a claim."""

    prompt = f"""Generate Python code to test this physics claim against real measurements.

Claim: {claim.statement}
Formula (if given): {claim.formula}
Measurement to compare: {claim.measurement_key}

Available constants:
Z2 = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z2)       # ≈ 5.79
np, pi, sqrt, exp, log are available

The code should:
1. Compute the predicted value
2. Print "PREDICTED: <value>"
3. Be a single expression or short calculation

Return ONLY executable Python code, no markdown, no explanation.
Example: print(f"PREDICTED: {{4*Z2 + 3}}")

Code:"""

    code = query_llm(prompt, temperature=0.2)

    # Clean up code
    code = code.strip()
    code = code.replace("```python", "").replace("```", "")
    code = code.strip()

    # Ensure it has a print statement
    if "PREDICTED:" not in code:
        code = f'print(f"PREDICTED: {{{claim.formula}}}")'

    return Experiment(
        claim=claim,
        python_code=code,
        status="PENDING"
    )

# ============================================================================
# PHASE 4: RUN EXPERIMENTS
# ============================================================================

def run_experiment(experiment: Experiment) -> Experiment:
    """Execute the experiment code and compare to measurement."""

    # Build full script
    script = f"""
import numpy as np
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)
pi = np.pi
sqrt = np.sqrt
exp = np.exp
log = np.log
alpha = 1/137.036
alpha_inv = 137.036

try:
    {experiment.python_code}
except Exception as e:
    print(f"ERROR: {{e}}")
"""

    try:
        # Run in subprocess
        result = subprocess.run(
            ["python3", "-c", script],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.strip()

        # Extract predicted value
        if "PREDICTED:" in output:
            value_str = output.split("PREDICTED:")[-1].strip()
            experiment.result = float(value_str)
        elif "ERROR:" in output:
            experiment.status = "ERROR"
            return experiment

    except Exception as e:
        experiment.status = "ERROR"
        return experiment

    # Compare to measurement
    if experiment.claim.measurement_key and experiment.claim.measurement_key in MEASUREMENTS:
        meas = MEASUREMENTS[experiment.claim.measurement_key]
        experiment.measured = meas["value"]
        experiment.uncertainty = meas.get("uncertainty", 0)

        if experiment.measured is not None and experiment.result is not None:
            # Compute statistics
            if experiment.uncertainty and experiment.uncertainty > 0:
                experiment.sigma = abs(experiment.result - experiment.measured) / experiment.uncertainty
            else:
                experiment.sigma = 0

            experiment.percent_error = abs(experiment.result - experiment.measured) / abs(experiment.measured) * 100

            # Classify result
            if experiment.uncertainty == 0:
                experiment.status = "EXACT" if experiment.result == experiment.measured else "WRONG"
            elif experiment.sigma < 2:
                experiment.status = "VALIDATED"
            elif experiment.sigma < 3:
                experiment.status = "TENSION"
            elif experiment.percent_error < 0.5:
                experiment.status = "PRECISE"
            else:
                experiment.status = "FAILED"
    else:
        experiment.status = "NO_DATA"

    return experiment

# ============================================================================
# PHASE 5: LEARN FROM FAILURES
# ============================================================================

def analyze_failure(experiment: Experiment) -> Dict:
    """Analyze why an experiment failed and suggest next steps."""

    prompt = f"""Analyze why this physics prediction failed and suggest improvements.

Claim: {experiment.claim.statement}
Formula: {experiment.claim.formula}
Code: {experiment.python_code}
Predicted: {experiment.result}
Measured: {experiment.measured} ± {experiment.uncertainty}
Sigma: {experiment.sigma}
Error: {experiment.percent_error}%

Using Z² framework (Z² = 32π/3 ≈ 33.51):
1. Why might this prediction be wrong?
2. Is there a better Z² formula that might work?
3. What additional experiments could help?

Return JSON:
{{
    "failure_reason": "explanation",
    "alternative_formula": "new formula or null",
    "next_experiments": ["list of suggestions"],
    "learnings": ["what we learned"]
}}

JSON:"""

    response = query_llm(prompt, temperature=0.5)
    result = extract_json(response)

    return result or {
        "failure_reason": "Unknown",
        "alternative_formula": None,
        "next_experiments": [],
        "learnings": []
    }

# ============================================================================
# PHASE 6: HONESTY ASSESSMENT
# ============================================================================

def assess_honesty(experiment: Experiment) -> HonestyAssessment:
    """Perform rigorous honesty assessment of a validated result."""

    prompt = f"""Perform a rigorous honesty assessment of this physics result.

Claim: {experiment.claim.statement}
Formula: {experiment.claim.formula}
Predicted: {experiment.result}
Measured: {experiment.measured}
Error: {experiment.percent_error}%
Status: {experiment.status}

Answer these questions honestly:

1. DERIVATION: Is this formula DERIVED from first principles, or does it just MATCH the data?
   - DERIVED = mechanism understood, prediction follows from theory
   - MATCHES = formula works but we don't know why
   - SPECULATIVE = interesting pattern but not rigorous
   - NUMEROLOGY = likely coincidence

2. MECHANISM: Do we understand WHY this formula works?

3. FALSIFIABLE: What would prove this wrong?

4. INDEPENDENT TESTS: What other predictions follow from this?

5. LIMITATIONS: What are the honest limitations of this result?

Return JSON:
{{
    "derivation_status": "DERIVED/MATCHES/SPECULATIVE/NUMEROLOGY",
    "mechanism_understood": true/false,
    "mechanism_explanation": "explanation or 'unknown'",
    "falsifiable": true/false,
    "falsification_criteria": ["list of tests that would falsify"],
    "independent_tests": ["other predictions that follow"],
    "honest_limitations": ["list of limitations"],
    "confidence_score": 0.0-1.0
}}

Be brutally honest. Better to undersell than overclaim.

JSON:"""

    response = query_llm(prompt, temperature=0.3)
    result = extract_json(response)

    if not result:
        result = {
            "derivation_status": "SPECULATIVE",
            "mechanism_understood": False,
            "falsifiable": True,
            "independent_tests": [],
            "honest_limitations": ["Assessment failed"],
            "confidence_score": 0.3
        }

    return HonestyAssessment(
        experiment=experiment,
        derivation_status=result.get("derivation_status", "SPECULATIVE"),
        mechanism_understood=result.get("mechanism_understood", False),
        falsifiable=result.get("falsifiable", True),
        independent_tests=result.get("independent_tests", []),
        honest_limitations=result.get("honest_limitations", []),
        confidence_score=result.get("confidence_score", 0.5)
    )

# ============================================================================
# PHASE 7: META-ASSESSMENT (Honesty of the Honesty)
# ============================================================================

def meta_assess(honesty: HonestyAssessment) -> MetaAssessment:
    """Assess the honesty assessment itself for bias and rigor."""

    prompt = f"""You are a skeptical reviewer assessing an honesty assessment.

Original claim: {honesty.experiment.claim.statement}
Result: {honesty.experiment.status} with {honesty.experiment.percent_error}% error
Honesty assessment:
- Derivation status: {honesty.derivation_status}
- Mechanism understood: {honesty.mechanism_understood}
- Confidence score: {honesty.confidence_score}
- Limitations: {honesty.honest_limitations}

Now critique this assessment:

1. BIAS CHECK: Is this assessment too optimistic or pessimistic?
2. ALTERNATIVES: What alternative explanations exist?
3. STATISTICS: Is the statistical significance properly evaluated?
4. REPRODUCIBILITY: Can others reproduce this result?
5. FIRST PRINCIPLES: Does this reach genuine first-principles truth?

Return JSON:
{{
    "bias_check": "Too optimistic / Balanced / Too pessimistic",
    "bias_explanation": "why",
    "alternative_explanations": ["list of alternative explanations"],
    "statistical_significance": "Strong / Moderate / Weak / Questionable",
    "reproducibility": "High / Medium / Low",
    "first_principles_status": "PROVEN / SUPPORTED / SPECULATIVE / UNFOUNDED",
    "final_verdict": "One sentence conclusion about the truth status"
}}

Be maximally skeptical. Assume you're trying to find flaws.

JSON:"""

    response = query_llm(prompt, temperature=0.4)
    result = extract_json(response)

    if not result:
        result = {
            "bias_check": "Unknown",
            "alternative_explanations": [],
            "statistical_significance": "Questionable",
            "reproducibility": "Unknown",
            "first_principles_status": "SPECULATIVE",
            "final_verdict": "Insufficient data for conclusion"
        }

    return MetaAssessment(
        honesty_assessment=honesty,
        bias_check=result.get("bias_check", "Unknown"),
        alternative_explanations=result.get("alternative_explanations", []),
        statistical_significance=result.get("statistical_significance", "Unknown"),
        reproducibility=result.get("reproducibility", "Unknown"),
        first_principles_status=result.get("first_principles_status", "SPECULATIVE"),
        final_verdict=result.get("final_verdict", "No conclusion")
    )

# ============================================================================
# MAIN RESEARCH LOOP
# ============================================================================

def run_research(question: str, max_iterations: int = 3) -> ResearchSession:
    """Run complete research session on a question."""

    print("=" * 80)
    print("TRUTHFLOW COMPLETE - SCIENTIFIC DISCOVERY ENGINE")
    print("=" * 80)
    print(f"Research Question: {question}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Model: {MODEL_NAME}")
    print("=" * 80)

    session = ResearchSession(
        question=question,
        timestamp=datetime.now().isoformat(),
        papers_fetched=[],
        claims_extracted=[],
        experiments=[],
        honesty_assessments=[],
        meta_assessments=[],
        learnings=[],
        next_steps=[]
    )

    # PHASE 1: Literature fetch
    print("\n" + "=" * 40)
    print("PHASE 1: LITERATURE FETCH")
    print("=" * 40)

    papers = fetch_arxiv_papers(question, max_results=15)
    session.papers_fetched = papers

    if not papers:
        print("  No papers found, using Z² framework knowledge")

    # PHASE 2: Extract claims
    print("\n" + "=" * 40)
    print("PHASE 2: EXTRACT TESTABLE CLAIMS")
    print("=" * 40)

    claims = parse_for_claims(papers, question)
    session.claims_extracted = claims

    # Also ask LLM directly for Z² predictions
    direct_prompt = f"""Based on the Z² framework (Z² = 32π/3 ≈ 33.51), what testable predictions exist for:
{question}

Return JSON with claims:
{{
    "claims": [
        {{
            "statement": "description",
            "formula": "python expression using Z, Z2, pi, alpha",
            "measurement_key": "key from measurements database",
            "confidence": "HIGH/MEDIUM/LOW"
        }}
    ]
}}

Available measurement keys: {list(MEASUREMENTS.keys())[:15]}

JSON:"""

    response = query_llm(direct_prompt, temperature=0.4)
    result = extract_json(response)

    if result and "claims" in result:
        for c in result["claims"]:
            claims.append(Claim(
                statement=c.get("statement", ""),
                formula=c.get("formula"),
                predicted_value=None,
                measurement_key=c.get("measurement_key"),
                source_paper="Z2_framework",
                confidence=c.get("confidence", "MEDIUM")
            ))

    print(f"  Total claims to test: {len(claims)}")

    # PHASE 3 & 4: Generate and run experiments
    print("\n" + "=" * 40)
    print("PHASE 3 & 4: GENERATE AND RUN EXPERIMENTS")
    print("=" * 40)

    for i, claim in enumerate(claims[:10]):  # Limit to 10
        print(f"\n  [{i+1}] {claim.statement[:60]}...")

        experiment = generate_experiment(claim)
        experiment = run_experiment(experiment)
        session.experiments.append(experiment)

        status_symbol = {
            "VALIDATED": "✓", "EXACT": "✓", "PRECISE": "△",
            "TENSION": "⚠", "FAILED": "✗", "ERROR": "!", "NO_DATA": "?"
        }.get(experiment.status, "?")

        if experiment.result is not None:
            print(f"      {status_symbol} Predicted: {experiment.result:.6g}")
            if experiment.measured:
                print(f"        Measured:  {experiment.measured:.6g}")
                print(f"        Error:     {experiment.percent_error:.4f}%")
                print(f"        Status:    {experiment.status}")

    # PHASE 5: Learn from failures
    print("\n" + "=" * 40)
    print("PHASE 5: ANALYZE FAILURES")
    print("=" * 40)

    failed = [e for e in session.experiments if e.status in ["FAILED", "TENSION"]]

    for exp in failed[:3]:
        print(f"\n  Analyzing: {exp.claim.statement[:50]}...")
        analysis = analyze_failure(exp)

        if analysis.get("learnings"):
            session.learnings.extend(analysis["learnings"])
            print(f"    Learnings: {analysis['learnings']}")

        if analysis.get("next_experiments"):
            session.next_steps.extend(analysis["next_experiments"])

    # PHASE 6: Honesty assessment of successes
    print("\n" + "=" * 40)
    print("PHASE 6: HONESTY ASSESSMENT")
    print("=" * 40)

    validated = [e for e in session.experiments if e.status in ["VALIDATED", "EXACT", "PRECISE"]]

    for exp in validated[:5]:
        print(f"\n  Assessing: {exp.claim.statement[:50]}...")

        honesty = assess_honesty(exp)
        session.honesty_assessments.append(honesty)

        print(f"    Derivation: {honesty.derivation_status}")
        print(f"    Mechanism understood: {honesty.mechanism_understood}")
        print(f"    Confidence: {honesty.confidence_score:.2f}")

    # PHASE 7: Meta-assessment
    print("\n" + "=" * 40)
    print("PHASE 7: META-ASSESSMENT (Honesty of Honesty)")
    print("=" * 40)

    for honesty in session.honesty_assessments[:3]:
        print(f"\n  Meta-assessing: {honesty.experiment.claim.statement[:40]}...")

        meta = meta_assess(honesty)
        session.meta_assessments.append(meta)

        print(f"    Bias check: {meta.bias_check}")
        print(f"    First principles: {meta.first_principles_status}")
        print(f"    Final verdict: {meta.final_verdict}")

    # SUMMARY
    print("\n" + "=" * 80)
    print("RESEARCH SESSION SUMMARY")
    print("=" * 80)

    total = len(session.experiments)
    validated_count = len([e for e in session.experiments if e.status in ["VALIDATED", "EXACT"]])
    precise_count = len([e for e in session.experiments if e.status == "PRECISE"])
    failed_count = len([e for e in session.experiments if e.status == "FAILED"])

    print(f"\nPapers fetched: {len(session.papers_fetched)}")
    print(f"Claims extracted: {len(session.claims_extracted)}")
    print(f"Experiments run: {total}")
    print(f"  ✓ Validated: {validated_count}")
    print(f"  △ Precise: {precise_count}")
    print(f"  ✗ Failed: {failed_count}")

    if session.learnings:
        print(f"\nLearnings:")
        for learning in session.learnings[:5]:
            print(f"  • {learning}")

    if session.next_steps:
        print(f"\nNext steps:")
        for step in session.next_steps[:5]:
            print(f"  → {step}")

    # Save session
    save_session(session)

    return session

def save_session(session: ResearchSession):
    """Save research session to file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = RESEARCH_DIR / f"session_{timestamp}.json"

    # Convert to serializable format
    data = {
        "question": session.question,
        "timestamp": session.timestamp,
        "papers_fetched": session.papers_fetched,
        "claims_count": len(session.claims_extracted),
        "experiments": [
            {
                "claim": asdict(e.claim),
                "result": e.result,
                "measured": e.measured,
                "sigma": e.sigma,
                "percent_error": e.percent_error,
                "status": e.status
            }
            for e in session.experiments
        ],
        "honesty_assessments": [
            {
                "claim": h.experiment.claim.statement,
                "derivation_status": h.derivation_status,
                "mechanism_understood": h.mechanism_understood,
                "confidence_score": h.confidence_score
            }
            for h in session.honesty_assessments
        ],
        "meta_assessments": [
            {
                "claim": m.honesty_assessment.experiment.claim.statement,
                "first_principles_status": m.first_principles_status,
                "final_verdict": m.final_verdict
            }
            for m in session.meta_assessments
        ],
        "learnings": session.learnings,
        "next_steps": session.next_steps
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"\nSession saved to: {filename}")

# ============================================================================
# INTERACTIVE MODE
# ============================================================================

def interactive_mode():
    """Run TruthFlow in interactive mode."""
    print("\n" + "=" * 60)
    print("TRUTHFLOW COMPLETE - Interactive Mode")
    print("=" * 60)
    print("Enter a research question to investigate.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Research question: ").strip()

        if question.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            session = run_research(question)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Run with command line argument
        question = " ".join(sys.argv[1:])
        run_research(question)
    else:
        # Interactive mode
        interactive_mode()
