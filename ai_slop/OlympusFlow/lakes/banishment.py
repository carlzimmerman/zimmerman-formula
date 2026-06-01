#!/usr/bin/env python3
"""
BANISHMENT LAKES - Mythological Error Classification
=====================================================

Hecate, goddess of crossroads, decides which of three banishment lakes
a failed finding should be cast into:

1. TartarusLake - For Empirical Failures
   Logic sound, framework aligned, but data doesn't match (>3sigma)

2. LetheLake - For Hallucinations & Sycophancy
   Agent defaulted to consensus (dark matter, etc.) instead of Z² first principles

3. LabyrinthLake - For Logical Dead-Ends
   Circular reasoning, math singularities, or stuck computations

Author: Carl Zimmerman
Date: May 7, 2026
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum


class BanishmentType(Enum):
    """Why was this finding banished?"""
    TARTARUS = "tartarus"     # Empirical failure (good logic, bad match)
    LETHE = "lethe"           # Hallucination/sycophancy (consensus default)
    LABYRINTH = "labyrinth"   # Logical dead-end (stuck/circular)


class BanishmentSeverity(Enum):
    """How severe is the banishment?"""
    MINOR = "minor"           # Might be recoverable with more data
    MAJOR = "major"           # Serious issue requiring investigation
    CRITICAL = "critical"     # Fundamental flaw, do not resurrect


@dataclass
class HecateBanishmentNote:
    """
    The official note Hecate appends when banishing a finding.

    "I, HECATE, have found this entry to be [HALLUCINATED/FAILED/STUCK].
    It is hereby cast into [LETHE/TARTARUS/LABYRINTH]."
    """
    banishment_type: str
    severity: str
    reason: str
    correction_guidance: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    hecate_declaration: str = ""

    def __post_init__(self):
        if not self.hecate_declaration:
            type_desc = {
                "tartarus": "EMPIRICALLY FAILED",
                "lethe": "HALLUCINATED",
                "labyrinth": "LOGICALLY STUCK"
            }
            lake_name = self.banishment_type.upper()
            desc = type_desc.get(self.banishment_type, "REJECTED")

            self.hecate_declaration = (
                f"I, HECATE, have found this entry to be {desc}. "
                f"It is hereby cast into {lake_name}. "
                f"Reason: {self.reason}"
            )

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> 'HecateBanishmentNote':
        return cls(**d)


@dataclass
class BanishedEntry:
    """
    A finding that has been banished to one of the underworld lakes.
    """
    entry_id: str
    original_claim: str
    original_formula: str
    target_value: float
    computed_value: float
    percent_error: float
    sigma_deviation: float

    # Banishment details
    banishment_type: str
    banishment_reason: str
    banishment_note: Optional[HecateBanishmentNote] = None

    # Original derivation metadata
    derivation_level: str = ""
    hrm_score: float = 0.0
    physical_mechanism: str = ""

    # Tracking
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    original_task_id: str = ""
    recovery_attempts: int = 0
    last_recovery_attempt: str = ""

    # For learnings
    root_cause: str = ""
    lesson_learned: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        if self.banishment_note:
            d['banishment_note'] = self.banishment_note.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: Dict) -> 'BanishedEntry':
        if d.get('banishment_note') and isinstance(d['banishment_note'], dict):
            d['banishment_note'] = HecateBanishmentNote.from_dict(d['banishment_note'])
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class BaseBanishmentLake:
    """
    Base class for all banishment lakes.

    Provides common storage, retrieval, and analysis functionality.
    Each specific lake (Tartarus, Lethe, Labyrinth) inherits from this.
    """

    LAKE_NAME = "banishment"
    LAKE_DESCRIPTION = "Base banishment lake"

    def __init__(self, storage_path: Optional[str] = None):
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path(__file__).parent / self.LAKE_NAME / "entries"

        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_path / "index.json"
        self.entries: Dict[str, BanishedEntry] = {}

        self._load_index()

    def _load_index(self):
        """Load existing entries from disk."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    data = json.load(f)
                    for entry_id, entry_data in data.items():
                        self.entries[entry_id] = BanishedEntry.from_dict(entry_data)
            except Exception as e:
                print(f"[{self.LAKE_NAME}] Could not load index: {e}")

    def _save_index(self):
        """Save entries to disk."""
        try:
            data = {eid: e.to_dict() for eid, e in self.entries.items()}
            with open(self.index_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"[{self.LAKE_NAME}] Could not save index: {e}")

    @staticmethod
    def generate_id(claim: str, timestamp: str = None) -> str:
        """Generate unique ID for a banished entry."""
        ts = timestamp or datetime.now().isoformat()
        content = f"{claim}:{ts}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def banish(self, entry: BanishedEntry) -> str:
        """
        Cast a finding into this lake.

        Returns the entry_id.
        """
        if not entry.entry_id:
            entry.entry_id = self.generate_id(entry.original_claim)

        entry.timestamp = datetime.now().isoformat()
        self.entries[entry.entry_id] = entry
        self._save_index()

        return entry.entry_id

    def get_entry(self, entry_id: str) -> Optional[BanishedEntry]:
        """Retrieve a banished entry."""
        return self.entries.get(entry_id)

    def query(self,
              min_error: float = None,
              max_error: float = None,
              claim_contains: str = None,
              limit: int = 100) -> List[BanishedEntry]:
        """Query banished entries with filters."""
        results = []

        for entry in self.entries.values():
            if min_error is not None and entry.percent_error < min_error:
                continue
            if max_error is not None and entry.percent_error > max_error:
                continue
            if claim_contains and claim_contains.lower() not in entry.original_claim.lower():
                continue

            results.append(entry)
            if len(results) >= limit:
                break

        results.sort(key=lambda e: e.timestamp, reverse=True)
        return results

    def get_statistics(self) -> Dict:
        """Get statistics about banished entries."""
        if not self.entries:
            return {"total": 0, "lake": self.LAKE_NAME}

        errors = [e.percent_error for e in self.entries.values() if e.percent_error < 100]

        return {
            "lake": self.LAKE_NAME,
            "total": len(self.entries),
            "avg_error": sum(errors) / len(errors) if errors else 0,
            "recovery_attempts": sum(e.recovery_attempts for e in self.entries.values()),
            "with_lessons": sum(1 for e in self.entries.values() if e.lesson_learned)
        }

    def attempt_recovery(self, entry_id: str, new_data: Dict = None) -> bool:
        """
        Mark that a recovery was attempted for this entry.

        Returns True if entry exists and was updated.
        """
        entry = self.entries.get(entry_id)
        if not entry:
            return False

        entry.recovery_attempts += 1
        entry.last_recovery_attempt = datetime.now().isoformat()
        self._save_index()
        return True

    def add_lesson(self, entry_id: str, root_cause: str, lesson: str) -> bool:
        """Add root cause analysis and lesson learned."""
        entry = self.entries.get(entry_id)
        if not entry:
            return False

        entry.root_cause = root_cause
        entry.lesson_learned = lesson
        self._save_index()
        return True

    def export_for_learning(self) -> List[Dict]:
        """Export entries with lessons for Cyllene learning pipeline."""
        return [
            {
                "claim": e.original_claim,
                "formula": e.original_formula,
                "error": e.percent_error,
                "banishment_type": e.banishment_type,
                "root_cause": e.root_cause,
                "lesson": e.lesson_learned,
                "hecate_note": e.banishment_note.hecate_declaration if e.banishment_note else ""
            }
            for e in self.entries.values()
            if e.lesson_learned
        ]
