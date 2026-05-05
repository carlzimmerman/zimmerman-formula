#!/usr/bin/env python3
"""
TOPIC VALIDATOR
===============

Validates that discovered data actually matches the requested search topic.
Prevents domain drift where a search for "Planck A_L lensing" returns
cosmic ray data instead.

The validator uses keyword extraction and semantic matching to ensure
findings are relevant to the original query.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import re
import subprocess
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pandas as pd

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-moe")


@dataclass
class ValidationResult:
    """Result of topic validation."""
    is_valid: bool
    confidence: float  # 0.0 to 1.0
    matched_keywords: List[str]
    missing_keywords: List[str]
    reason: str


class TopicValidator:
    """
    Validates that discovered data matches the requested topic.

    Uses:
    1. Keyword extraction from topic
    2. Keyword matching in data columns/values
    3. LLM semantic validation as fallback
    """

    # Domain-specific required keywords
    DOMAIN_KEYWORDS = {
        'cosmology': {
            'A_L': ['lensing', 'amplitude', 'planck', 'cmb'],
            'omega': ['density', 'lambda', 'matter', 'cosmological'],
            'tensor': ['scalar', 'ratio', 'primordial', 'gravitational'],
        },
        'meteorology': {
            'hurricane': ['storm', 'wind', 'pressure', 'cyclone', 'ace'],
            'temperature': ['celsius', 'fahrenheit', 'anomaly', 'average'],
            'precipitation': ['rain', 'snow', 'mm', 'inches'],
        },
        'particle_physics': {
            'mass': ['mev', 'gev', 'tev', 'particle'],
            'coupling': ['constant', 'alpha', 'beta', 'interaction'],
        },
        'condensed_matter': {
            'hall': ['quantum', 'plateau', 'resistance', 'conductance'],
            'transition': ['temperature', 'phase', 'critical'],
        }
    }

    # Synonyms for common topic keywords - expands matching
    SYNONYMS = {
        'hurricane': ['storm', 'cyclone', 'typhoon', 'tropical'],
        'storm': ['hurricane', 'cyclone', 'typhoon', 'disturbance', 'tornado', 'severe'],
        'wind': ['wind_speed', 'windspeed', 'winds', 'gust'],
        'pressure': ['pressure_mb', 'mslp', 'barometric'],
        'intensity': ['strength', 'power', 'category', 'saffir', 'ef_scale', 'fujita'],
        'atlantic': ['north_atlantic', 'basin', 'hurdat'],
        'ace': ['accumulated', 'cyclone_energy', 'energy'],
        'lensing': ['lens', 'gravitational_lens'],
        'cmb': ['cosmic_microwave', 'microwave_background'],
        'planck': ['esa', 'satellite', 'mission'],
        # Tornado-specific synonyms (added from tornado blind test)
        'tornado': ['storm', 'twister', 'funnel', 'cyclone', 'vortex', 'severe_weather'],
        'ef_scale': ['fujita', 'enhanced_fujita', 'tornado_intensity', 'rating'],
        'severe_weather': ['storm', 'tornado', 'hail', 'thunderstorm'],
        'noaa': ['ncei', 'nws', 'psl', 'spc', 'national_weather'],
        'statistics': ['count', 'frequency', 'annual', 'monthly', 'data'],
    }

    # Words to exclude from keyword matching
    STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'data', 'value', 'measurement',
        'official', 'download', 'csv', 'json', 'file', 'dataset'
    }

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(f"[TopicValidator] {msg}")

    def extract_keywords(self, topic: str) -> List[str]:
        """
        Extract meaningful keywords from the topic string.

        Args:
            topic: The search topic

        Returns:
            List of keywords (lowercased, stopwords removed)
        """
        # Split on spaces and common delimiters
        words = re.findall(r'\b[A-Za-z][A-Za-z0-9_]+\b', topic)

        # Filter and lowercase
        keywords = []
        for word in words:
            word_lower = word.lower()
            if word_lower not in self.STOPWORDS and len(word_lower) > 2:
                keywords.append(word_lower)

        # Also preserve important abbreviations/acronyms (all caps)
        acronyms = re.findall(r'\b[A-Z]{2,6}\b', topic)
        keywords.extend([a.lower() for a in acronyms])

        return list(set(keywords))

    def validate_dataframe(self, df: pd.DataFrame, topic: str,
                          domain: str) -> ValidationResult:
        """
        Validate that a DataFrame contains data relevant to the topic.

        Args:
            df: The DataFrame to validate
            topic: Original search topic
            domain: Expected domain

        Returns:
            ValidationResult with confidence and details
        """
        if df is None or df.empty:
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                matched_keywords=[],
                missing_keywords=[],
                reason="Empty or null DataFrame"
            )

        # Extract keywords from topic
        topic_keywords = self.extract_keywords(topic)
        self._log(f"Topic keywords: {topic_keywords}")

        # Build searchable text from DataFrame
        searchable_parts = []

        # Column names
        searchable_parts.extend([str(c).lower() for c in df.columns])

        # Sample of data values (first 10 rows)
        for col in df.columns:
            try:
                sample = df[col].head(10).astype(str).tolist()
                searchable_parts.extend([s.lower() for s in sample])
            except:
                pass

        searchable_text = ' '.join(searchable_parts)

        # Match keywords (with synonym expansion)
        matched = []
        missing = []

        for kw in topic_keywords:
            # Direct match
            if kw in searchable_text:
                matched.append(kw)
                continue

            # Try synonyms
            synonyms = self.SYNONYMS.get(kw, [])
            found_synonym = False
            for syn in synonyms:
                if syn in searchable_text:
                    matched.append(f"{kw}(via:{syn})")
                    found_synonym = True
                    break

            if not found_synonym:
                missing.append(kw)

        # Calculate base confidence
        if len(topic_keywords) > 0:
            match_ratio = len(matched) / len(topic_keywords)
        else:
            match_ratio = 0.0

        # Adjust confidence based on domain-specific requirements
        domain_boost = self._check_domain_keywords(searchable_text, topic, domain)

        confidence = min(1.0, match_ratio * 0.7 + domain_boost * 0.3)

        # Determine validity
        is_valid = confidence >= 0.4 and len(matched) >= 2

        if is_valid:
            reason = f"Found {len(matched)}/{len(topic_keywords)} topic keywords"
        else:
            reason = f"Insufficient relevance: only {len(matched)}/{len(topic_keywords)} keywords matched"

        result = ValidationResult(
            is_valid=is_valid,
            confidence=confidence,
            matched_keywords=matched,
            missing_keywords=missing,
            reason=reason
        )

        self._log(f"Validation: {result.is_valid} (confidence: {result.confidence:.2f})")
        self._log(f"  Matched: {matched}")
        self._log(f"  Missing: {missing}")

        return result

    def _check_domain_keywords(self, text: str, topic: str, domain: str) -> float:
        """
        Check for domain-specific required keywords.

        Returns a score 0.0 to 1.0 based on domain keyword presence.
        """
        domain_kws = self.DOMAIN_KEYWORDS.get(domain, {})

        # Find which sub-topic we're looking for
        topic_lower = topic.lower()
        matched_subtopic = None

        for subtopic, keywords in domain_kws.items():
            if subtopic.lower() in topic_lower:
                matched_subtopic = subtopic
                break

        if not matched_subtopic:
            return 0.5  # Neutral score if no specific subtopic

        required_keywords = domain_kws[matched_subtopic]
        matches = sum(1 for kw in required_keywords if kw in text)

        return matches / len(required_keywords) if required_keywords else 0.5

    def validate_with_llm(self, df: pd.DataFrame, topic: str,
                         domain: str) -> ValidationResult:
        """
        Use LLM to semantically validate data relevance.

        This is a fallback for ambiguous cases.
        """
        # Prepare data summary
        columns = list(df.columns)[:10]
        sample = df.head(5).to_string(max_cols=6)

        prompt = f"""I searched for: "{topic}"
Domain: {domain}

I found this data:
Columns: {columns}
Sample:
{sample}

Does this data match what I was searching for?
Answer EXACTLY: "VALID" or "INVALID" followed by one sentence explanation.
"""

        try:
            result = subprocess.run(
                ["ollama", "run", LEGOMENA_MODEL],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                response = result.stdout.strip().upper()

                if response.startswith("VALID"):
                    return ValidationResult(
                        is_valid=True,
                        confidence=0.8,
                        matched_keywords=[],
                        missing_keywords=[],
                        reason=f"LLM validated: {result.stdout.strip()}"
                    )
                else:
                    return ValidationResult(
                        is_valid=False,
                        confidence=0.2,
                        matched_keywords=[],
                        missing_keywords=[],
                        reason=f"LLM rejected: {result.stdout.strip()}"
                    )

        except Exception as e:
            self._log(f"LLM validation failed: {e}")

        # Return uncertain result
        return ValidationResult(
            is_valid=False,
            confidence=0.5,
            matched_keywords=[],
            missing_keywords=[],
            reason="LLM validation failed, defaulting to invalid"
        )


# =============================================================================
# INTEGRATION WITH HERMESFLOW
# =============================================================================

def validate_discovery(df: pd.DataFrame, topic: str, domain: str,
                      use_llm_fallback: bool = True) -> Tuple[bool, str]:
    """
    Convenience function for HermesFlow integration.

    Args:
        df: Discovered DataFrame
        topic: Search topic
        domain: Domain
        use_llm_fallback: Whether to use LLM for uncertain cases

    Returns:
        (is_valid, reason) tuple
    """
    validator = TopicValidator(verbose=True)

    # First try keyword validation
    result = validator.validate_dataframe(df, topic, domain)

    if result.is_valid:
        return True, result.reason

    # If uncertain and LLM fallback enabled
    if use_llm_fallback and result.confidence >= 0.3:
        llm_result = validator.validate_with_llm(df, topic, domain)
        if llm_result.is_valid:
            return True, llm_result.reason

    return False, result.reason


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    import pandas as pd

    print("=" * 60)
    print("TOPIC VALIDATOR DEMO")
    print("=" * 60)

    # Test case: Correct match
    print("\nTest 1: Correct match (hurricane data for hurricane search)")
    df_hurricane = pd.DataFrame({
        'storm_name': ['Katrina', 'Harvey', 'Maria'],
        'wind_speed_mph': [175, 130, 175],
        'pressure_mb': [902, 938, 908],
        'ace_index': [34.3, 28.5, 41.6]
    })

    result = validate_discovery(
        df_hurricane,
        topic="Atlantic hurricane intensity measurements ACE",
        domain="meteorology",
        use_llm_fallback=False
    )
    print(f"Valid: {result[0]}, Reason: {result[1]}")

    # Test case: Domain drift (cosmic rays when searching for CMB)
    print("\nTest 2: Domain drift (cosmic ray data for CMB search)")
    df_cosmic = pd.DataFrame({
        'event_id': [1, 2, 3],
        'energy_eV': [1e18, 2e18, 3e18],
        'zenith_angle': [30, 45, 60],
        'CV_stop': [5.5, 5.8, 5.9]
    })

    result = validate_discovery(
        df_cosmic,
        topic="Planck CMB lensing amplitude A_L anomaly",
        domain="cosmology",
        use_llm_fallback=False
    )
    print(f"Valid: {result[0]}, Reason: {result[1]}")
