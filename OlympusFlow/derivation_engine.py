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

# Legomena model
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-moe")

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
        self.timing: Dict[str, float] = {}

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[DerivEngine {ts}] {msg}")

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

    def _ask_legomena(self, prompt: str, timeout: int = 60) -> str:
        """
        Ask Legomena for reasoning about physics.

        Returns empty string if not available.
        """
        if not self.legomena_available:
            return ""

        start = time.time()
        try:
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
            self._log(f"  Legomena timeout after {timeout}s")
        except Exception as e:
            self._log(f"  Legomena error: {e}")

        return ""

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
        normalized = constant_name.lower().replace(" ", "_").replace("-", "_")
        if normalized in KNOWN_FIRST_PRINCIPLES:
            self._log("Using known first-principles derivation template")
            chain = self._use_known_derivation(normalized, target_value)
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

        connection_response = self._ask_legomena(physical_prompt, timeout=90)

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

        self._log(f"  Connection: {connection}")
        self._log(f"  Mechanism: {mechanism[:50]}..." if len(mechanism) > 50 else f"  Mechanism: {mechanism}")
        self._log(f"  Confidence: {confidence}")

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
        Pattern match against Z² formulas.

        This is the FALLBACK when no physical derivation exists.
        Returns (formula, computed_value, percent_error)
        """
        # Generate candidates
        candidates = []

        # Simple fractions (mark as non-Z)
        for a in range(1, 30):
            for b in range(1, 30):
                if a != b:
                    val = a / b
                    err = abs(target - val) / target * 100
                    if err < 5:
                        candidates.append((f"{a}/{b}", val, err, False))

        # Z-based formulas
        z_formulas = [
            ("Z", Z), ("Z²", Z2), ("1/Z", 1/Z), ("1/Z²", 1/Z2),
            ("Z/10", Z/10), ("Z²/10", Z2/10), ("Z²/100", Z2/100),
            ("Z + 1", Z + 1), ("Z - 1", Z - 1),
            ("2Z", 2*Z), ("Z/2", Z/2),
            ("π/Z", math.pi/Z), ("Z/π", Z/math.pi),
        ]

        for formula, val in z_formulas:
            err = abs(target - val) / target * 100
            if err < 5:
                candidates.append((formula, val, err, True))

        # aZ + b forms
        for a in range(-5, 6):
            for b in range(-20, 21):
                if a != 0:
                    val = a * Z + b
                    err = abs(target - val) / target * 100
                    if err < 5:
                        candidates.append((f"{a}Z + {b}" if b >= 0 else f"{a}Z - {-b}", val, err, True))

        # Sort by error
        candidates.sort(key=lambda x: x[2])

        # Prefer Z-containing formulas
        z_candidates = [c for c in candidates if c[3]]
        if z_candidates:
            best = z_candidates[0]
            return best[0], best[1], best[2]
        elif candidates:
            best = candidates[0]
            return best[0], best[1], best[2]

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

            # Calculate deviation
            if verified.experimental_uncertainty > 0:
                verified.deviation_sigma = abs(
                    chain.computed_value - experimental_value
                ) / verified.experimental_uncertainty
            else:
                verified.deviation_sigma = abs(
                    chain.computed_value - experimental_value
                ) / experimental_value * 100

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
        Search for experimental value of a constant.

        Uses Legomena to parse search results if available.
        """
        # First, try asking Legomena directly (it has training data)
        if self.legomena_available:
            prompt = f"""What is the current best experimental measurement of {constant_name}?

Provide ONLY these fields:
VALUE: [number]
UNCERTAINTY: [number, 1-sigma error]
SOURCE: [measurement source]

Example:
VALUE: 0.6847
UNCERTAINTY: 0.0073
SOURCE: Planck 2018"""

            response = self._ask_legomena(prompt, timeout=30)

            if response:
                result = {}
                for line in response.split('\n'):
                    if 'VALUE:' in line:
                        try:
                            result['value'] = float(line.split('VALUE:')[1].strip())
                        except:
                            pass
                    elif 'UNCERTAINTY:' in line:
                        try:
                            result['uncertainty'] = float(line.split('UNCERTAINTY:')[1].strip())
                        except:
                            pass
                    elif 'SOURCE:' in line:
                        result['source'] = line.split('SOURCE:')[1].strip()

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
