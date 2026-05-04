#!/usr/bin/env python3
"""
TRUTH STORE
===========

Persistent storage for validated Z² discoveries.
Truths are findings that have been statistically validated
and can be used to train LegomenaLLM.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_STORE_PATH = Path(__file__).parent / "data" / "truth_store.json"


class TruthStore:
    """
    Persistent storage for validated scientific findings.

    Each truth includes:
    - domain: Scientific domain (e.g., glaciology, meteorology)
    - quantity: What was measured
    - value: Measured value
    - target: Z² constant it matches (e.g., "1/φ", "Z²")
    - target_value: Numerical value of target
    - error_percent: How close the match is
    - n_samples: Sample size for validation
    - data_source: Where the data came from
    - validation: Statistical validation details
    """

    def __init__(self, store_path: Path = None):
        self.store_path = store_path or DEFAULT_STORE_PATH
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        self.truths: List[Dict] = []
        self.load()

    def load(self):
        """Load truths from disk."""
        if self.store_path.exists():
            with open(self.store_path, 'r') as f:
                self.truths = json.load(f)

    def save(self):
        """Save truths to disk."""
        with open(self.store_path, 'w') as f:
            json.dump(self.truths, f, indent=2)

    def add(self, finding: Dict) -> bool:
        """
        Add a validated finding to the truth store.

        Returns True if added, False if duplicate.
        """
        # Check for duplicates
        key = (finding.get('domain'), finding.get('quantity'))
        for t in self.truths:
            if (t.get('domain'), t.get('quantity')) == key:
                return False  # Already exists

        # Add metadata
        finding['added_timestamp'] = datetime.now().isoformat()
        finding['incorporated_in_training'] = False

        self.truths.append(finding)
        self.save()
        return True

    def get_all(self) -> List[Dict]:
        """Get all truths."""
        return self.truths

    def get_by_domain(self, domain: str) -> List[Dict]:
        """Get truths for a specific domain."""
        return [t for t in self.truths if t.get('domain') == domain]

    def get_unincorporated(self) -> List[Dict]:
        """Get truths not yet added to training."""
        return [t for t in self.truths if not t.get('incorporated_in_training', False)]

    def mark_incorporated(self, quantity: str):
        """Mark a truth as incorporated into training."""
        for t in self.truths:
            if t.get('quantity') == quantity:
                t['incorporated_in_training'] = True
                t['incorporated_timestamp'] = datetime.now().isoformat()
        self.save()

    def get_summary(self) -> Dict:
        """Get summary statistics."""
        domains = set(t.get('domain') for t in self.truths)
        return {
            "total_truths": len(self.truths),
            "domains": list(domains),
            "incorporated": sum(1 for t in self.truths if t.get('incorporated_in_training')),
            "pending": sum(1 for t in self.truths if not t.get('incorporated_in_training'))
        }

    def export_for_training(self) -> List[Dict]:
        """Export truths in format suitable for training."""
        return [
            {
                "instruction": f"What is the Z² relationship for {t['quantity']}?",
                "response": (
                    f"The {t['quantity']} equals {t['target']} ({t['target_value']:.4f}) "
                    f"with {t['error_percent']:.2f}% error. "
                    f"Validated on {t.get('n_samples', 'N/A')} samples from {t.get('data_source', 'unknown')}."
                )
            }
            for t in self.truths
        ]
