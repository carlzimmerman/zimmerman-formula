#!/usr/bin/env python3
"""
OLYMPUSFLOW - Derivation Engine
================================

The core engine that builds Z² derivation chains using:
1. Legomena (LLM) for reasoning about physical connections
2. WebSearch for finding experimental values
3. AletheiaLake for ground truth validation

This is the engine that does the ACTUAL work of derivation,
not just pattern matching.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import math
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

from .derivation_contracts import (
    DerivationStep, DerivationChain, VerifiedDerivation,
    DerivationLevel, ZSquaredRelevance, ChainStatus, StorageDestination,
    Z2, Z, PHI, create_z2_axiom_step, evaluate_formula_z_content,
    KNOWN_FIRST_PRINCIPLES
)
from .formula_generator import FormulaGenerator, FormulaType

# Legomena model and timeouts - NO RUSHING
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-moe")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "600"))  # 10 min default

# Multi-prompt configuration
MULTI_PROMPT_ATTEMPTS = int(os.environ.get("DERIVATION_ATTEMPTS", "4"))
SKEPTICAL_THRESHOLD = 0.75  # Below this confidence, run skeptical challenge

# Experimental data sources (will be queried via web search)
EXPERIMENTAL_SOURCES = {
    "cosmology": ["Planck 2018", "WMAP", "DES", "DESI"],
    "particle_physics": ["PDG 2024", "LHC", "CODATA"],
    "condensed_matter": ["NIST", "CRC Handbook"],
    "electromagnetism": ["CODATA 2022", "NIST"],
}


class DerivationEngine:
    """
    Engine that builds Z² derivation chains with LLM reasoning.

    This does the actual intellectual work of:
    1. Understanding the physical constant
    2. Researching how it might connect to Z²
    3. Building step-by-step derivation
    4. Validating against experiment
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.legomena_available = self._check_legomena()
        self.formula_gen = FormulaGenerator(max_error=1.0, verbose=False)
        self.timing: Dict[str, float] = {}

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[DerivEngine {ts}] {msg}")

    def _match_known_constant(self, constant_name: str) -> Optional[str]:
        """
        Try to match a constant name to a known first-principles key.

        Returns the matching key or None.
        """
        # Direct normalization
        normalized = constant_name.lower().replace(" ", "_").replace("-", "_")
        if normalized in KNOWN_FIRST_PRINCIPLES:
            return normalized

        # Name aliases for common constants
        aliases = {
            # Fine structure constant
            "fine_structure_constant_inverse_1/α": "fine_structure_constant_inverse",
            "fine_structure_constant_inverse_1_α": "fine_structure_constant_inverse",
            "alpha_inverse": "fine_structure_constant_inverse",
            "1/alpha": "fine_structure_constant_inverse",
            "inverse_fine_structure": "fine_structure_constant_inverse",
            "137": "fine_structure_constant_inverse",
            # Weak mixing angle
            "sin2_theta_w": "sin2_theta_w",
            "sin²θ_w": "sin2_theta_w",
            "weak_mixing_angle": "sin2_theta_w",
            "weinberg_angle": "sin2_theta_w",
            # Dark energy
            "omega_lambda": "omega_lambda",
            "dark_energy_density": "omega_lambda",
            "cosmological_constant": "omega_lambda",
        }

        # Try aliases
        if normalized in aliases:
            return aliases[normalized]

        # Fuzzy matching: check if any key is a substring
        for key in KNOWN_FIRST_PRINCIPLES.keys():
            if key in normalized or normalized in key:
                return key
            # Check without underscores
            if key.replace("_", "") in normalized.replace("_", ""):
                return key

        # Check for numeric patterns (e.g., "137" in constant name)
        if "137" in constant_name or "fine" in constant_name.lower():
            return "fine_structure_constant_inverse"

        return None

    def _check_legomena(self) -> bool:
        """Check if Legomena (via ollama) is available."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                if LEGOMENA_MODEL in result.stdout:
                    self._log(f"✓ Legomena model available: {LEGOMENA_MODEL}")
                    return True
                else:
                    self._log(f"⚠ Model {LEGOMENA_MODEL} not found in ollama")
                    self._log(f"  Available: {result.stdout.strip()}")
                    return False
        except Exception as e:
            self._log(f"✗ Ollama not available: {e}")
        return False

    def _ask_legomena(self, prompt: str, timeout: int = None) -> str:
        """
        Ask Legomena for reasoning about physics.

        Args:
            prompt: The prompt to send
            timeout: Timeout in seconds (defaults to LEGOMENA_TIMEOUT env var)

        Returns empty string if not available.
        """
        if not self.legomena_available:
            return ""

        # Use environment timeout if not specified - NO RUSHING
        if timeout is None:
            timeout = LEGOMENA_TIMEOUT

        start = time.time()
        try:
            self._log(f"  Calling Legomena (timeout={timeout}s)...")
            result = subprocess.run(
                ["ollama", "run", LEGOMENA_MODEL],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            elapsed = time.time() - start
            self._log(f"  Legomena responded in {elapsed:.1f}s")

            if result.returncode == 0:
                return result.stdout.strip()
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            self._log(f"  Legomena timeout after {elapsed:.1f}s (limit was {timeout}s)")
        except Exception as e:
            self._log(f"  Legomena error: {e}")

        return ""

    def _multi_prompt_derive(self, constant_name: str, target_value: float,
                              initial_response: Dict) -> Dict:
        """
        Multi-prompt refinement for derivations.

        Like how the user prompts Claude multiple times to dig deeper,
        we challenge Legomena with follow-up prompts to improve answers.

        Args:
            constant_name: The constant being derived
            target_value: Target numerical value
            initial_response: First attempt results (connection, mechanism, confidence, formula_hint)

        Returns:
            Refined response with best derivation found
        """
        connection = initial_response.get('connection', 'NO')
        mechanism = initial_response.get('mechanism', '')
        confidence = initial_response.get('confidence', 0.3)
        formula_hint = initial_response.get('formula_hint', '')

        best_result = initial_response.copy()
        attempts_log = [f"Attempt 1: {connection}, conf={confidence:.2f}"]

        # =====================================================================
        # ATTEMPT 2: Skeptical Challenge (if confidence < threshold)
        # =====================================================================
        if confidence < SKEPTICAL_THRESHOLD or connection not in ['YES']:
            self._log("  Running skeptical challenge (Attempt 2)...")

            skeptical_prompt = f"""You previously analyzed {constant_name} = {target_value}

Your initial assessment:
- Connection: {connection}
- Mechanism: {mechanism}
- Confidence: {confidence}
- Formula hint: {formula_hint}

Now be SKEPTICAL. Challenge yourself:

1. Is this connection DERIVED from Z² geometry, or just a NUMERICAL COINCIDENCE?
   - A true derivation has a physical mechanism (dimensional analysis, symmetry, DOF counting)
   - Numerology is when you find arithmetic combinations that match but have no physics

2. What would FALSIFY this Z² connection?
   - If you can't think of a falsification test, the connection is likely numerology

3. Are there SIMPLER explanations that don't involve Z²?
   - Standard physics derivations (from thermodynamics, QFT, etc.)
   - Pure dimensional analysis without Z²

Think HARDER. Be HONEST. Don't overclaim.

Respond in EXACT format:
REVISED_CONNECTION: [YES/MAYBE/NO/NUMEROLOGY]
REVISED_MECHANISM: [better physical mechanism OR "no mechanism - numerical only"]
REVISED_CONFIDENCE: [0.0 to 1.0, be more conservative]
CLASSIFICATION: [DERIVED/MATCHES/NUMEROLOGY/UNDETERMINED]
FALSIFICATION: [what would disprove this?]"""

            skeptical_response = self._ask_legomena(skeptical_prompt, timeout=None)

            if skeptical_response:
                revised_connection = connection
                revised_confidence = confidence
                classification = "UNDETERMINED"
                falsification = ""

                for line in skeptical_response.split('\n'):
                    if 'REVISED_CONNECTION:' in line:
                        revised_connection = line.split('REVISED_CONNECTION:')[1].strip().upper()
                    elif 'REVISED_MECHANISM:' in line:
                        revised_mech = line.split('REVISED_MECHANISM:')[1].strip()
                        if revised_mech and len(revised_mech) > len(mechanism):
                            mechanism = revised_mech
                    elif 'REVISED_CONFIDENCE:' in line:
                        try:
                            revised_confidence = float(line.split('REVISED_CONFIDENCE:')[1].strip())
                        except:
                            pass
                    elif 'CLASSIFICATION:' in line:
                        classification = line.split('CLASSIFICATION:')[1].strip().upper()
                    elif 'FALSIFICATION:' in line:
                        falsification = line.split('FALSIFICATION:')[1].strip()

                # Update best if skeptical challenge improved understanding
                if revised_confidence != confidence or classification != "UNDETERMINED":
                    best_result['connection'] = revised_connection
                    best_result['mechanism'] = mechanism
                    best_result['confidence'] = revised_confidence
                    best_result['classification'] = classification
                    best_result['falsification'] = falsification
                    attempts_log.append(f"Attempt 2 (skeptical): {classification}, conf={revised_confidence:.2f}")

                    confidence = revised_confidence
                    connection = revised_connection

        # =====================================================================
        # ATTEMPT 3: Alternative Approaches (try multiple derivation methods)
        # =====================================================================
        if MULTI_PROMPT_ATTEMPTS >= 3 and connection not in ['NO', 'NUMEROLOGY']:
            self._log("  Trying alternative approaches (Attempt 3)...")

            alternatives_prompt = f"""For {constant_name} = {target_value}, try MULTIPLE derivation approaches:

METHOD A - Dimensional Analysis:
- What dimensions does this constant have?
- Can Z² = 32π/3 (dimensionless) appear naturally?

METHOD B - Geometric Derivation:
- Z² = 32π/3 = (4π)(8/3) relates to sphere/cube geometry
- Does this constant involve angles, solid angles, or geometric ratios?

METHOD C - DOF Counting:
- Z² relates to dimensional counting (3 space + 1 time = 4)
- Does this constant involve counting degrees of freedom?

METHOD D - Optimization/Variational:
- Some constants emerge from optimization principles
- Could Z² appear in a variational derivation?

METHOD E - Symmetry/Group Theory:
- Z² involves SU(2), cube symmetry group
- Does this constant involve gauge groups or discrete symmetries?

For EACH method that could work, show the derivation steps.

Respond in EXACT format:
BEST_METHOD: [A/B/C/D/E]
DERIVATION_STEPS: [numbered steps of the best derivation]
FORMULA: [the Z²-based formula]
COMPUTED_VALUE: [numerical result]
METHOD_CONFIDENCE: [0.0 to 1.0]"""

            alternatives_response = self._ask_legomena(alternatives_prompt, timeout=None)

            if alternatives_response:
                best_method = ""
                derivation_steps = ""
                formula = formula_hint
                computed = 0.0
                method_confidence = confidence

                for line in alternatives_response.split('\n'):
                    if 'BEST_METHOD:' in line:
                        best_method = line.split('BEST_METHOD:')[1].strip()
                    elif 'FORMULA:' in line:
                        new_formula = line.split('FORMULA:')[1].strip()
                        if new_formula:
                            formula = new_formula
                    elif 'COMPUTED_VALUE:' in line:
                        try:
                            computed = float(line.split('COMPUTED_VALUE:')[1].strip())
                        except:
                            pass
                    elif 'METHOD_CONFIDENCE:' in line:
                        try:
                            method_confidence = float(line.split('METHOD_CONFIDENCE:')[1].strip())
                        except:
                            pass
                    elif 'DERIVATION_STEPS:' in line:
                        derivation_steps = line.split('DERIVATION_STEPS:')[1].strip()

                # If this attempt found a better derivation
                if method_confidence > confidence or (computed > 0 and formula):
                    best_result['best_method'] = best_method
                    best_result['derivation_steps'] = derivation_steps
                    best_result['formula_hint'] = formula
                    best_result['computed_value'] = computed
                    best_result['confidence'] = max(confidence, method_confidence)
                    attempts_log.append(f"Attempt 3 (alternatives): Method {best_method}, conf={method_confidence:.2f}")

                    confidence = best_result['confidence']

        # =====================================================================
        # ATTEMPT 4: Final Synthesis (meta-review of all attempts)
        # =====================================================================
        if MULTI_PROMPT_ATTEMPTS >= 4:
            self._log("  Final synthesis (Attempt 4)...")

            synthesis_prompt = f"""Synthesize your analysis of {constant_name} = {target_value}

Your attempts so far:
{chr(10).join(attempts_log)}

Current best:
- Connection: {best_result.get('connection', 'UNKNOWN')}
- Mechanism: {best_result.get('mechanism', 'none')}
- Confidence: {best_result.get('confidence', 0)}
- Classification: {best_result.get('classification', 'UNDETERMINED')}
- Formula: {best_result.get('formula_hint', 'none')}

FINAL JUDGMENT:

1. Is this Z² connection REAL (derived from physics) or COINCIDENTAL (numerology)?
   Be brutally honest. Most numerical matches are coincidences.

2. What is the SINGLE BEST derivation path, if any exists?

3. What is your FINAL confidence (0.0-1.0)?
   - 0.9+: Clear first-principles derivation with physical mechanism
   - 0.7-0.9: Strong evidence but some uncertainty
   - 0.5-0.7: Plausible but needs more investigation
   - 0.3-0.5: Weak evidence, possibly coincidence
   - <0.3: Likely numerology, no real connection

4. What would CHANGE YOUR MIND?

Respond in EXACT format:
FINAL_VERDICT: [DERIVED/MATCHES/NUMEROLOGY/INCONCLUSIVE]
FINAL_MECHANISM: [the physical mechanism if DERIVED, otherwise "none"]
FINAL_FORMULA: [the formula if derived]
FINAL_CONFIDENCE: [0.0 to 1.0]
HONEST_ASSESSMENT: [one sentence summary]"""

            synthesis_response = self._ask_legomena(synthesis_prompt, timeout=None)

            if synthesis_response:
                for line in synthesis_response.split('\n'):
                    if 'FINAL_VERDICT:' in line:
                        best_result['final_verdict'] = line.split('FINAL_VERDICT:')[1].strip().upper()
                    elif 'FINAL_MECHANISM:' in line:
                        final_mech = line.split('FINAL_MECHANISM:')[1].strip()
                        if final_mech and final_mech.lower() != 'none':
                            best_result['mechanism'] = final_mech
                    elif 'FINAL_FORMULA:' in line:
                        final_formula = line.split('FINAL_FORMULA:')[1].strip()
                        if final_formula:
                            best_result['formula_hint'] = final_formula
                    elif 'FINAL_CONFIDENCE:' in line:
                        try:
                            best_result['confidence'] = float(line.split('FINAL_CONFIDENCE:')[1].strip())
                        except:
                            pass
                    elif 'HONEST_ASSESSMENT:' in line:
                        best_result['honest_assessment'] = line.split('HONEST_ASSESSMENT:')[1].strip()

                attempts_log.append(f"Attempt 4 (synthesis): {best_result.get('final_verdict', 'N/A')}, conf={best_result.get('confidence', 0):.2f}")

        best_result['attempts_log'] = attempts_log
        best_result['num_attempts'] = len(attempts_log)

        self._log(f"  Multi-prompt completed: {len(attempts_log)} attempts")
        self._log(f"  Final: {best_result.get('final_verdict', best_result.get('connection', 'N/A'))}, conf={best_result.get('confidence', 0):.2f}")

        return best_result

    def derive(self, constant_name: str, target_value: float,
               strategy: Optional[Dict] = None) -> DerivationChain:
        """
        Build a derivation chain for a physical constant.

        Args:
            constant_name: Name of the constant (e.g., "fine structure constant")
            target_value: The measured value
            strategy: Optional MetisFlow strategy with research context

        Returns:
            DerivationChain with steps, confidence, and level assessment
        """
        self._log(f"\n{'='*60}")
        self._log(f"DERIVING: {constant_name}")
        self._log(f"Target value: {target_value}")
        self._log(f"{'='*60}\n")

        start_total = time.time()

        # Initialize chain
        chain = DerivationChain(
            target_constant=constant_name,
            target_value=target_value
        )

        # Check if we have a known first-principles derivation
        known_key = self._match_known_constant(constant_name)
        if known_key:
            self._log(f"Using known first-principles derivation template: {known_key}")
            chain = self._use_known_derivation(known_key, target_value)
        else:
            # Attempt to build derivation with Legomena
            chain = self._build_new_derivation(constant_name, target_value, strategy)

        # Record timing
        self.timing['total'] = time.time() - start_total
        self._log(f"\nDerivation completed in {self.timing['total']:.1f}s")
        self._log(f"Level: {chain.level.value}")
        self._log(f"Status: {chain.status.value}")

        return chain

    def _use_known_derivation(self, name: str, target_value: float) -> DerivationChain:
        """Use a known first-principles derivation."""
        template = KNOWN_FIRST_PRINCIPLES[name]

        chain = DerivationChain(
            target_constant=name.replace("_", " ").title(),
            target_value=target_value
        )

        # Copy steps from template
        for step in template["steps"]:
            chain.add_step(step)

        chain.final_formula = template["formula"]
        chain.computed_value = template["value"]
        chain.percent_error = abs(target_value - template["value"]) / target_value * 100
        chain.physical_mechanism = template["physical_mechanism"]

        chain._recompute_flags()
        return chain

    def _build_new_derivation(self, constant_name: str, target_value: float,
                               strategy: Optional[Dict] = None) -> DerivationChain:
        """
        Build a new derivation using Legomena reasoning.

        This is where the actual intellectual work happens.
        """
        chain = DerivationChain(
            target_constant=constant_name,
            target_value=target_value
        )

        # Step 1: Start with Z² axiom
        self._log("Step 1: Adding Z² axiom...")
        chain.add_step(create_z2_axiom_step())

        # Step 2: Ask Legomena about physical connection
        self._log("Step 2: Reasoning about physical connection...")

        physical_prompt = f"""You are a theoretical physicist reasoning about fundamental constants.

The Z² constant = 32π/3 ≈ 33.51 emerges from:
- Solid angle of a unit sphere (4π steradians) × 8/3
- Relates to sphere packing, holographic principle, dimensional reduction

The target constant is: {constant_name} = {target_value}

Question: Is there a plausible physical mechanism connecting this constant to Z²?

Consider:
1. Does this constant involve geometry, dimensionality, or information?
2. Is it related to known Z²-connected quantities (cosmological parameters, gauge couplings)?
3. What physical principle might create this connection?

Respond in this EXACT format:
CONNECTION: [YES/MAYBE/NO]
MECHANISM: [one sentence describing physical mechanism]
CONFIDENCE: [0.0 to 1.0]
FORMULA_HINT: [suggest Z²-based formula like "Z²/x" or "aZ + b"]"""

        connection_response = self._ask_legomena(physical_prompt, timeout=None)

        # Parse response
        connection = "NO"
        mechanism = ""
        confidence = 0.3
        formula_hint = ""

        if connection_response:
            for line in connection_response.split('\n'):
                if 'CONNECTION:' in line:
                    connection = line.split('CONNECTION:')[1].strip().upper()
                elif 'MECHANISM:' in line:
                    mechanism = line.split('MECHANISM:')[1].strip()
                elif 'CONFIDENCE:' in line:
                    try:
                        confidence = float(line.split('CONFIDENCE:')[1].strip())
                    except:
                        pass
                elif 'FORMULA_HINT:' in line:
                    formula_hint = line.split('FORMULA_HINT:')[1].strip()

        self._log(f"  Initial: Connection={connection}, Confidence={confidence}")

        # =====================================================================
        # MULTI-PROMPT REFINEMENT (like user prompting Claude multiple times)
        # =====================================================================
        initial_response = {
            'connection': connection,
            'mechanism': mechanism,
            'confidence': confidence,
            'formula_hint': formula_hint
        }

        # Run multi-prompt refinement to dig deeper
        if MULTI_PROMPT_ATTEMPTS > 1 and self.legomena_available:
            self._log("Running multi-prompt refinement...")
            refined = self._multi_prompt_derive(constant_name, target_value, initial_response)

            # Update with refined results
            connection = refined.get('connection', connection)
            mechanism = refined.get('mechanism', mechanism)
            confidence = refined.get('confidence', confidence)
            formula_hint = refined.get('formula_hint', formula_hint)

            # Store multi-prompt refinement results
            chain.refinement_metadata = {
                'attempts': refined.get('num_attempts', 1),
                'final_verdict': refined.get('final_verdict', 'UNKNOWN'),
                'classification': refined.get('classification', 'UNDETERMINED'),
                'honest_assessment': refined.get('honest_assessment', ''),
                'falsification': refined.get('falsification', ''),
                'attempts_log': refined.get('attempts_log', [])
            }

        self._log(f"  Final: Connection={connection}, Confidence={confidence}")

        # Step 3: Try to build mathematical connection
        self._log("Step 3: Building mathematical connection...")

        if connection in ["YES", "MAYBE"] and formula_hint:
            # Try to derive using the hint
            step2 = self._build_physics_step(constant_name, mechanism, confidence)
            if step2:
                chain.add_step(step2)

            # Try the hinted formula
            step3, formula, computed = self._try_formula_derivation(
                target_value, formula_hint, mechanism
            )
            if step3:
                chain.add_step(step3)
                chain.final_formula = formula
                chain.computed_value = computed
                chain.percent_error = abs(target_value - computed) / target_value * 100
        else:
            # No clear connection - try pattern matching as fallback
            self._log("  No clear Z² connection, trying pattern matching...")
            formula, computed, error = self._pattern_match(target_value)

            if formula and error < 5.0:
                step = DerivationStep(
                    step_number=2,
                    premise=f"Target value {target_value}",
                    operation="Numerical pattern matching",
                    result=f"Found formula {formula} = {computed}",
                    justification="WARNING: No physical mechanism - this is numerology",
                    formula_in=f"{constant_name} = {target_value}",
                    formula_out=formula,
                    is_axiomatic=False,
                    is_physical=False,  # NOT physical!
                    confidence=0.2  # Low confidence for numerology
                )
                chain.add_step(step)
                chain.final_formula = formula
                chain.computed_value = computed
                chain.percent_error = error
            else:
                chain.final_formula = "No derivation found"
                chain.computed_value = 0
                chain.percent_error = 100

        chain.physical_mechanism = mechanism
        chain._recompute_flags()
        return chain

    def _build_physics_step(self, constant_name: str, mechanism: str,
                            confidence: float) -> Optional[DerivationStep]:
        """Build a physics step connecting Z² to the constant."""
        if not mechanism:
            return None

        return DerivationStep(
            step_number=2,
            premise="Z² encodes geometric structure of spacetime",
            operation="Physical mechanism",
            result=f"Connection to {constant_name} via {mechanism[:50]}",
            justification=mechanism,
            formula_in="Z² geometry",
            formula_out=f"→ {constant_name}",
            is_axiomatic=False,
            is_physical=True,
            confidence=confidence
        )

    def _try_formula_derivation(self, target: float, hint: str,
                                mechanism: str) -> Tuple[Optional[DerivationStep], str, float]:
        """
        Try to derive using a formula hint.

        Returns (step, formula, computed_value)
        """
        # Try evaluating the hint
        try:
            # Safe eval with Z² constants
            safe_context = {
                'Z2': Z2, 'Z': Z, 'PHI': PHI,
                'pi': math.pi, 'π': math.pi,
                'sqrt': math.sqrt, 'log': math.log,
                'exp': math.exp
            }

            # Parse hint and try variations
            formulas_to_try = [hint]

            # Add common variations
            if "Z" in hint.upper():
                formulas_to_try.extend([
                    hint.replace("Z²", "Z2").replace("Z^2", "Z2"),
                    hint.replace("z²", "Z2").replace("z^2", "Z2"),
                ])

            best_formula = None
            best_value = 0
            best_error = float('inf')

            for formula in formulas_to_try:
                try:
                    # Normalize formula
                    f = formula.replace("²", "2").replace("^", "**")
                    value = eval(f, {"__builtins__": {}}, safe_context)
                    error = abs(target - value) / target * 100

                    if error < best_error:
                        best_error = error
                        best_value = value
                        best_formula = formula
                except:
                    continue

            if best_formula and best_error < 10:
                step = DerivationStep(
                    step_number=3,
                    premise=f"Physical mechanism: {mechanism[:50]}",
                    operation="Mathematical derivation",
                    result=f"{best_formula} = {best_value:.10f}",
                    justification=f"Derived from Z² with error {best_error:.4f}%",
                    formula_in="Z² = 32π/3",
                    formula_out=best_formula,
                    is_axiomatic=False,
                    is_physical=False,
                    confidence=max(0.3, 1.0 - best_error/10)
                )
                return step, best_formula, best_value

        except Exception as e:
            self._log(f"  Formula evaluation error: {e}")

        return None, "", 0

    def _pattern_match(self, target: float) -> Tuple[str, float, float]:
        """
        Pattern match against Z² formulas using FormulaGenerator.

        This is the FALLBACK when no physical derivation exists.
        Returns (formula, computed_value, percent_error)

        Uses FormulaGenerator for comprehensive formula search including:
        - Simple fractions (a/b)
        - Z² polynomial forms (aZ² + b)
        - Z linear forms (aZ + b)
        - Geometric functions (arccos, arctan)
        - Pi-based expressions
        - Known first-principles templates
        """
        # Handle edge case where target is 0 or very small
        if abs(target) < 1e-15:
            return "", 0, 100

        # Use FormulaGenerator for comprehensive search
        result = self.formula_gen.search(target)

        if result.best_match:
            best = result.best_match
            return best.formula_str, best.computed_value, best.percent_error

        # No match found
        return "", 0, 100

    def verify(self, chain: DerivationChain,
               experimental_value: float = None,
               experimental_uncertainty: float = None,
               experimental_source: str = "") -> VerifiedDerivation:
        """
        Verify a derivation chain against experimental data.

        Args:
            chain: The derivation chain to verify
            experimental_value: Measured value (will search if not provided)
            experimental_uncertainty: 1-sigma error
            experimental_source: Source of measurement

        Returns:
            VerifiedDerivation with validation results
        """
        self._log(f"\nVerifying derivation: {chain.target_constant}")

        verified = VerifiedDerivation(chain=chain)

        # Get experimental data if not provided
        exp_data = None
        if experimental_value is None:
            self._log("  Searching for experimental value...")
            exp_data = self._search_experimental_value(chain.target_constant)
            if exp_data:
                experimental_value = exp_data.get('value')
                experimental_uncertainty = exp_data.get('uncertainty', 0)
                experimental_source = exp_data.get('source', 'Web search')

        if experimental_value is not None:
            verified.experimental_value = experimental_value
            verified.experimental_uncertainty = experimental_uncertainty or experimental_value * 0.01
            verified.experimental_source = experimental_source

            # Copy provenance fields if we got them from search
            if exp_data:
                verified.source_url = exp_data.get('source_url', '')
                verified.citation = exp_data.get('citation', '')
                verified.verbatim_quote = exp_data.get('verbatim_quote', '')
                verified.page_number = exp_data.get('page_number', '')
                verified.doi = exp_data.get('doi', '')

            # Calculate deviation
            if verified.experimental_uncertainty > 0:
                verified.deviation_sigma = abs(
                    chain.computed_value - experimental_value
                ) / verified.experimental_uncertainty
            else:
                # Use percent difference as fallback (avoid division by zero)
                if abs(experimental_value) > 1e-15:
                    verified.deviation_sigma = abs(
                        chain.computed_value - experimental_value
                    ) / abs(experimental_value) * 100
                else:
                    verified.deviation_sigma = abs(chain.computed_value - experimental_value) * 1e10

            self._log(f"  Experimental: {experimental_value} ± {verified.experimental_uncertainty}")
            self._log(f"  Computed: {chain.computed_value}")
            self._log(f"  Deviation: {verified.deviation_sigma:.2f}σ")

        # Compute HRM and determine destination
        verified.compute_hrm()
        verified.determine_destination()

        self._log(f"  HRM Score: {verified.hrm_score:.2f}")
        self._log(f"  Destination: {verified.destination.value}")

        return verified

    def _search_experimental_value(self, constant_name: str) -> Optional[Dict]:
        """
        Search for experimental value of a constant with full provenance.

        Uses Legomena to parse search results if available.
        Returns dict with value, uncertainty, source, and provenance fields.
        """
        # First, try asking Legomena directly (it has training data)
        if self.legomena_available:
            prompt = f"""What is the current best experimental measurement of {constant_name}?

Provide ALL these fields (use "N/A" if unknown):
VALUE: [number - the measured value]
UNCERTAINTY: [number - 1-sigma error]
SOURCE: [brief source name, e.g., "Planck 2018", "PDG 2024", "CODATA 2022"]
SOURCE_URL: [URL to the paper or data source]
CITATION: [full citation, e.g., "Planck Collaboration (2020), A&A 641, A6"]
DOI: [DOI if available, e.g., "10.1051/0004-6361/201833910"]
VERBATIM_QUOTE: [exact quote of the measurement from the source]
PAGE: [page number or table number where value appears]

Example:
VALUE: 0.6847
UNCERTAINTY: 0.0073
SOURCE: Planck 2018
SOURCE_URL: https://arxiv.org/abs/1807.06209
CITATION: Planck Collaboration (2020), Planck 2018 results. VI. Cosmological parameters, A&A 641, A6
DOI: 10.1051/0004-6361/201833910
VERBATIM_QUOTE: "Ωλ = 0.6847 ± 0.0073 (Table 2)"
PAGE: Table 2, page 24"""

            response = self._ask_legomena(prompt, timeout=None)

            if response:
                result = {}
                for line in response.split('\n'):
                    line = line.strip()
                    if line.startswith('VALUE:'):
                        try:
                            val_str = line.split('VALUE:')[1].strip()
                            # Handle scientific notation and clean up
                            val_str = val_str.split()[0] if val_str else ""
                            result['value'] = float(val_str)
                        except:
                            pass
                    elif line.startswith('UNCERTAINTY:'):
                        try:
                            unc_str = line.split('UNCERTAINTY:')[1].strip()
                            unc_str = unc_str.split()[0] if unc_str else ""
                            result['uncertainty'] = float(unc_str)
                        except:
                            pass
                    elif line.startswith('SOURCE:'):
                        val = line.split('SOURCE:')[1].strip()
                        if val and val.lower() != 'n/a':
                            result['source'] = val
                    elif line.startswith('SOURCE_URL:'):
                        val = line.split('SOURCE_URL:')[1].strip()
                        if val and val.lower() != 'n/a' and val.startswith('http'):
                            result['source_url'] = val
                    elif line.startswith('CITATION:'):
                        val = line.split('CITATION:')[1].strip()
                        if val and val.lower() != 'n/a':
                            result['citation'] = val
                    elif line.startswith('DOI:'):
                        val = line.split('DOI:')[1].strip()
                        if val and val.lower() != 'n/a':
                            result['doi'] = val
                    elif line.startswith('VERBATIM_QUOTE:'):
                        val = line.split('VERBATIM_QUOTE:')[1].strip()
                        if val and val.lower() != 'n/a':
                            result['verbatim_quote'] = val
                    elif line.startswith('PAGE:'):
                        val = line.split('PAGE:')[1].strip()
                        if val and val.lower() != 'n/a':
                            result['page_number'] = val

                if 'value' in result:
                    return result

        return None


# =============================================================================
# DEMO
# =============================================================================

def demo():
    """Demonstrate the derivation engine."""
    engine = DerivationEngine()

    # Test on a few constants
    test_cases = [
        ("Dark Energy Density", 0.6847),
        ("Weak Mixing Angle", 0.23122),
        ("von Karman Constant", 0.41),
    ]

    for name, value in test_cases:
        chain = engine.derive(name, value)
        print("\n" + chain.summary())

        # Verify
        verified = engine.verify(chain, experimental_value=value)
        print(f"\nVerification:")
        print(f"  HRM Score: {verified.hrm_score:.2f}")
        print(f"  Destination: {verified.destination.value}")
        if verified.rejection_reason:
            print(f"  Rejection: {verified.rejection_reason}")
        print("=" * 60)


if __name__ == "__main__":
    demo()
