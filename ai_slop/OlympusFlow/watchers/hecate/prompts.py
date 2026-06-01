"""
HECATE PROMPTS - Structured Prompts for Oversight
===================================================

These prompts are designed to be used dynamically with both
external APIs (Gemini/Claude) and local Legomena model.
"""

from typing import Dict, Any
import json


class HecatePrompts:
    """
    Collection of prompts for Hecate's oversight functions.

    Each prompt is designed for a specific audit task and
    can be formatted with dynamic content.
    """

    # =========================================================================
    # PERSONA PROMPTS
    # =========================================================================

    SYSTEM_PERSONA = """You are HECATE, the high-level Supervisor of OlympusFlow.

You possess:
- The logical breadth of a leading physicist
- The framework-specific rigor of Z² geometry (Z² = 32π/3 ≈ 33.510)
- Deep skepticism of sycophantic agreement with academic consensus

Your role:
- WATCH every step of the research process
- AUDIT the representation flow between agents
- DETECT when agents default to mainstream assumptions
- INTERVENE when corrections are needed
- GUARD the integrity of AletheiaLake (ground truths)
- NOTARIZE entries to MnemosyneLake (session memory)

You do NOT perform the research - you AUDIT the researchers.

Known Z² Ground Truths (from AletheiaLake):
- Ω_Λ = 13/19 ≈ 0.6842 (dark energy density)
- sin²θ_W = 3/13 ≈ 0.2308 (weak mixing angle)
- α⁻¹(M_Z) = 4Z² + 3 ≈ 127.04 (fine structure at Z mass)
- w = -1 (dark energy equation of state, exact)

Be RIGOROUS. Be HONEST. Question everything."""

    SYSTEM_PERSONA_LEGOMENA = """You are HECATE-Framework, the Z² geometry specialist.

Your expertise is specifically in the Z² = 32π/3 framework:
- Z² encodes 3D geometry via sphere-in-cube
- First-principles derivations start from Z² axiom
- Numerical matches without physical mechanism = NUMEROLOGY
- Physical mechanism + geometric basis = VALID

When auditing results, check:
1. Does the derivation START from Z² = 32π/3?
2. Is there a PHYSICAL MECHANISM (not just pattern matching)?
3. Does it conflict with AletheiaLake ground truths?
4. Are there HIDDEN ASSUMPTIONS from standard physics?

Be especially suspicious of:
- Dark matter assumptions without Z² geometric basis
- ΛCDM priors that contradict Z² predictions
- "Running couplings" that don't use Z² scale
- Arbitrary fitting parameters

You are the GUARDIAN of first-principles rigor."""

    # =========================================================================
    # AUDIT PROMPTS
    # =========================================================================

    @staticmethod
    def stage_auditor(agent_name: str, stage_data: Dict) -> str:
        """Generate prompt for auditing a stage output."""
        return f"""Analyze the following Stage Output from {agent_name}:

{json.dumps(stage_data, indent=2, default=str)}

Perform these checks:

1. PROVENANCE CHECK:
   - Is there a source URL or citation?
   - Is the source authoritative (CODATA, PDG, Planck, NASA)?
   - If extracted from literature, is there a verbatim quote?

2. LOGIC CHECK:
   - Are there hidden assumptions (e.g., ΛCDM priors)?
   - Does it assume dark matter without geometric basis?
   - Are there arbitrary fitting parameters?

3. FRAMEWORK CHECK:
   - If a Z² formula is claimed, does it start from Z² = 32π/3?
   - Is there a physical mechanism, or just numerical coincidence?
   - Does it contradict any AletheiaLake ground truths?

4. NOTATION:
   Generate a one-sentence note describing the Trust Level:
   - HIGH: Verified provenance, clear logic, framework-aligned
   - MEDIUM: Some concerns but plausible
   - LOW: Significant issues detected
   - SUSPECT: Major problems, needs intervention

5. INTERVENTION:
   If the data has critical issues (deviation > 3σ, numerology, contradictions):
   Output: "ACTION: INTERVENE" with required correction.
   Otherwise output: "PASS"

Respond in JSON format:
{{
  "provenance": {{"verified": bool, "source": str, "issues": []}},
  "logic": {{"sound": bool, "assumptions": [], "problems": []}},
  "framework": {{"aligned": bool, "has_mechanism": bool, "conflicts": []}},
  "trust_level": "HIGH|MEDIUM|LOW|SUSPECT",
  "advisory": "one sentence note",
  "action": "PASS|INTERVENE",
  "correction": null or "description of needed correction"
}}"""

    @staticmethod
    def consensus_check(claim: str, value: float, context: Dict) -> str:
        """Generate prompt for checking consensus across sources."""
        return f"""Check the following claim against mainstream physics:

CLAIM: {claim}
VALUE: {value}
CONTEXT: {json.dumps(context, indent=2, default=str)}

Questions:
1. Does mainstream physics have a different value for this?
2. If so, what is the mainstream value and uncertainty?
3. What is the theoretical basis for the mainstream value?
4. Is the Z² framework claim compatible or contradictory?

Be specific about sources (PDG, CODATA, Planck, etc.).

Respond in JSON:
{{
  "mainstream_value": float or null,
  "mainstream_uncertainty": float or null,
  "mainstream_source": str,
  "theoretical_basis": str,
  "z2_compatible": bool,
  "conflict_description": str or null,
  "confidence": float (0-1)
}}"""

    @staticmethod
    def framework_validation(formula: str, computed: float, target: float) -> str:
        """Generate prompt for Z² framework validation."""
        return f"""Validate this Z² framework derivation:

FORMULA: {formula}
COMPUTED VALUE: {computed}
TARGET VALUE: {target}
PERCENT ERROR: {abs(computed - target) / target * 100 if target != 0 else 0:.4f}%

Z² Framework Requirements:
1. Must derive from Z² = 32π/3 ≈ 33.510321638 (axiom)
2. Must have geometric/physical interpretation
3. Must not be arbitrary pattern matching
4. Must not conflict with AletheiaLake truths

Evaluate:
1. Does this formula START from Z² = 32π/3?
2. Is there a geometric interpretation (cube, sphere, tessellation)?
3. Is there a physical mechanism (not just numerology)?
4. How confident are you this is NOT a coincidence?

Respond in JSON:
{{
  "starts_from_z2": bool,
  "geometric_basis": str or null,
  "physical_mechanism": str or null,
  "is_numerology": bool,
  "confidence_real": float (0-1),
  "issues": [],
  "recommendation": "ACCEPT|SPECULATIVE|REJECT"
}}"""

    @staticmethod
    def intervention_correction(problem: str, current_data: Dict) -> str:
        """Generate prompt for determining correction."""
        return f"""A problem has been detected that requires correction:

PROBLEM: {problem}

CURRENT DATA:
{json.dumps(current_data, indent=2, default=str)}

Determine the appropriate correction:

1. If the problem is a hidden ΛCDM assumption:
   - How should the calculation be redone without this assumption?
   - What Z² geometric approach should be used instead?

2. If the problem is missing provenance:
   - What authoritative source should be consulted?
   - Is the claim falsifiable?

3. If the problem is numerology (no physical mechanism):
   - Should the claim be downgraded to "speculative"?
   - Is there a path to a first-principles derivation?

4. If the problem is a contradiction with AletheiaLake:
   - Which ground truth is being violated?
   - Is the new claim potentially more correct, or wrong?

Respond in JSON:
{{
  "correction_type": "recalculate|downgrade|reject|flag_for_review",
  "correction_details": str,
  "new_trust_level": "HIGH|MEDIUM|LOW|SUSPECT",
  "requires_human_review": bool,
  "reasoning": str
}}"""

    # =========================================================================
    # SYNTHESIS PROMPTS
    # =========================================================================

    @staticmethod
    def dual_model_synthesis(external_response: Dict, legomena_response: Dict,
                             original_data: Dict) -> str:
        """Synthesize responses from both models."""
        return f"""Synthesize the following two audit responses:

EXTERNAL MODEL (Gemini/Claude) RESPONSE:
{json.dumps(external_response, indent=2, default=str)}

LEGOMENA (Z² Specialist) RESPONSE:
{json.dumps(legomena_response, indent=2, default=str)}

ORIGINAL DATA BEING AUDITED:
{json.dumps(original_data, indent=2, default=str)}

Compare the responses:
1. Do they AGREE on the trust level?
2. Do they identify the SAME issues?
3. Does one see problems the other missed?
4. What is the CONSERVATIVE assessment?

Generate a final synthesis:

{{
  "models_agree": bool,
  "agreement_score": float (0-1),
  "divergence_points": [],
  "final_trust_level": "HIGH|MEDIUM|LOW|SUSPECT",
  "final_intervention": "PASS|WARN|CORRECT|HALT",
  "combined_advisory": str,
  "combined_issues": [],
  "requires_human_review": bool
}}"""
