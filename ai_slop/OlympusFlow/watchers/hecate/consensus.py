"""
CONSENSUS BRIDGE - Dual-Model Communication Layer
===================================================

Handles communication with both external APIs (Gemini/Claude)
and local Legomena model for dual-lens oversight.
"""

import os
import json
import subprocess
import time
from typing import Dict, Optional, Tuple
from datetime import datetime

from ..contracts import ConsensusCheck, ConsensusSource
from .prompts import HecatePrompts


class ConsensusBridge:
    """
    Bridge for communicating with multiple models for consensus checking.

    Supports:
    - Local Legomena (via Ollama)
    - Gemini API (Google)
    - Claude API (Anthropic)
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

        # Model availability
        self.legomena_available = self._check_legomena()
        self.gemini_available = self._check_gemini()
        self.claude_available = self._check_claude()

        # Timeouts
        self.legomena_timeout = int(os.environ.get("LEGOMENA_TIMEOUT", "120"))
        self.external_timeout = int(os.environ.get("EXTERNAL_API_TIMEOUT", "30"))

        # Model names
        self.legomena_model = os.environ.get("LEGOMENA_MODEL", "legomena-moe")

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[ConsensusBridge {ts}] {msg}")

    def _check_legomena(self) -> bool:
        """Check if Legomena is available via Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                model = os.environ.get("LEGOMENA_MODEL", "legomena-moe")
                return model in result.stdout
        except Exception:
            pass
        return False

    def _check_gemini(self) -> bool:
        """Check if Gemini API is configured."""
        return bool(os.environ.get("GOOGLE_API_KEY"))

    def _check_claude(self) -> bool:
        """Check if Claude API is configured."""
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    # =========================================================================
    # LEGOMENA (Local Model)
    # =========================================================================

    def ask_legomena(self, prompt: str, system: str = None,
                     timeout: int = None) -> Tuple[bool, Dict]:
        """
        Query the local Legomena model.

        Returns:
            (success: bool, response: Dict or error message)
        """
        if not self.legomena_available:
            return False, {"error": "Legomena not available"}

        timeout = timeout or self.legomena_timeout

        full_prompt = prompt
        if system:
            full_prompt = f"System: {system}\n\nUser: {prompt}"

        try:
            start = time.time()
            result = subprocess.run(
                ["ollama", "run", self.legomena_model],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            elapsed = time.time() - start

            if result.returncode == 0:
                response_text = result.stdout.strip()
                self._log(f"Legomena responded in {elapsed:.1f}s")

                # Try to parse as JSON
                try:
                    # Find JSON in response
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = response_text[json_start:json_end]
                        return True, json.loads(json_str)
                    else:
                        return True, {"raw_response": response_text}
                except json.JSONDecodeError:
                    return True, {"raw_response": response_text}

            return False, {"error": result.stderr}

        except subprocess.TimeoutExpired:
            return False, {"error": f"Timeout after {timeout}s"}
        except Exception as e:
            return False, {"error": str(e)}

    # =========================================================================
    # EXTERNAL APIs
    # =========================================================================

    def ask_gemini(self, prompt: str, system: str = None,
                   timeout: int = None) -> Tuple[bool, Dict]:
        """
        Query Gemini API.

        Returns:
            (success: bool, response: Dict or error message)
        """
        if not self.gemini_available:
            return False, {"error": "Gemini API not configured"}

        timeout = timeout or self.external_timeout

        try:
            import google.generativeai as genai

            api_key = os.environ.get("GOOGLE_API_KEY")
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel('gemini-pro')

            full_prompt = prompt
            if system:
                full_prompt = f"{system}\n\n{prompt}"

            start = time.time()
            response = model.generate_content(full_prompt)
            elapsed = time.time() - start

            self._log(f"Gemini responded in {elapsed:.1f}s")

            response_text = response.text

            # Try to parse as JSON
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    return True, json.loads(response_text[json_start:json_end])
                return True, {"raw_response": response_text}
            except json.JSONDecodeError:
                return True, {"raw_response": response_text}

        except ImportError:
            return False, {"error": "google-generativeai not installed"}
        except Exception as e:
            return False, {"error": str(e)}

    def ask_claude(self, prompt: str, system: str = None,
                   timeout: int = None) -> Tuple[bool, Dict]:
        """
        Query Claude API.

        Returns:
            (success: bool, response: Dict or error message)
        """
        if not self.claude_available:
            return False, {"error": "Claude API not configured"}

        timeout = timeout or self.external_timeout

        try:
            import anthropic

            client = anthropic.Anthropic()

            messages = [{"role": "user", "content": prompt}]

            start = time.time()
            response = client.messages.create(
                model="claude-3-haiku-20240307",  # Fast model for auditing
                max_tokens=1024,
                system=system or "",
                messages=messages
            )
            elapsed = time.time() - start

            self._log(f"Claude responded in {elapsed:.1f}s")

            response_text = response.content[0].text

            # Try to parse as JSON
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    return True, json.loads(response_text[json_start:json_end])
                return True, {"raw_response": response_text}
            except json.JSONDecodeError:
                return True, {"raw_response": response_text}

        except ImportError:
            return False, {"error": "anthropic not installed"}
        except Exception as e:
            return False, {"error": str(e)}

    # =========================================================================
    # DUAL-LENS CONSENSUS
    # =========================================================================

    def dual_audit(self, data: Dict, external_model: str = "gemini") -> ConsensusCheck:
        """
        Perform dual-lens audit using both external API and Legomena.

        Returns:
            ConsensusCheck with combined results
        """
        sources_queried = []
        source_results = {}

        # 1. Query external model
        external_prompt = HecatePrompts.stage_auditor("Pipeline", data)

        if external_model == "gemini":
            success, external_response = self.ask_gemini(
                external_prompt,
                system=HecatePrompts.SYSTEM_PERSONA
            )
            if success:
                sources_queried.append("gemini")
                source_results["gemini"] = external_response
        elif external_model == "claude":
            success, external_response = self.ask_claude(
                external_prompt,
                system=HecatePrompts.SYSTEM_PERSONA
            )
            if success:
                sources_queried.append("claude")
                source_results["claude"] = external_response

        # 2. Query Legomena (Z² specialist)
        legomena_prompt = HecatePrompts.stage_auditor("Pipeline", data)
        success, legomena_response = self.ask_legomena(
            legomena_prompt,
            system=HecatePrompts.SYSTEM_PERSONA_LEGOMENA
        )
        if success:
            sources_queried.append("legomena")
            source_results["legomena"] = legomena_response

        # 3. Analyze agreement
        overall_agreement, majority_view, dissenting_views, conflicts = \
            self._analyze_consensus(source_results)

        return ConsensusCheck(
            query=f"Audit of pipeline data",
            sources_queried=sources_queried,
            source_results=source_results,
            overall_agreement=overall_agreement,
            majority_view=majority_view,
            dissenting_views=dissenting_views,
            conflicts_detected=len(conflicts) > 0,
            conflict_description="; ".join(conflicts) if conflicts else ""
        )

    def _analyze_consensus(self, results: Dict) -> Tuple[float, str, list, list]:
        """
        Analyze consensus between model responses.

        Returns:
            (agreement_score, majority_view, dissenting_views, conflicts)
        """
        if not results:
            return 0.0, "unknown", [], []

        # Extract trust levels and actions
        trust_levels = []
        actions = []
        issues = []

        for source, result in results.items():
            if isinstance(result, dict):
                if "trust_level" in result:
                    trust_levels.append(result["trust_level"])
                if "action" in result:
                    actions.append(result["action"])
                if "issues" in result:
                    issues.extend(result.get("issues", []))
                if "logic" in result and "problems" in result["logic"]:
                    issues.extend(result["logic"]["problems"])

        # Calculate agreement
        if len(trust_levels) >= 2:
            # Check if they agree
            unique_levels = set(trust_levels)
            if len(unique_levels) == 1:
                agreement = 1.0
            elif len(unique_levels) == 2:
                agreement = 0.5
            else:
                agreement = 0.0
        else:
            agreement = 0.5  # Can't determine with single source

        # Majority view
        if trust_levels:
            from collections import Counter
            majority_view = Counter(trust_levels).most_common(1)[0][0]
        else:
            majority_view = "unknown"

        # Dissenting views
        dissenting = [tl for tl in trust_levels if tl != majority_view]

        # Conflicts (where models fundamentally disagree)
        conflicts = []
        if "PASS" in actions and "INTERVENE" in actions:
            conflicts.append("Models disagree on intervention need")

        return agreement, majority_view, dissenting, conflicts

    def get_available_models(self) -> Dict[str, bool]:
        """Get availability status of all models."""
        return {
            "legomena": self.legomena_available,
            "gemini": self.gemini_available,
            "claude": self.claude_available
        }
