#!/usr/bin/env python3
"""
OLYMPUSFLOW - Data Contracts
============================

Strict type definitions for data flowing between pipeline stages.
All components must use these contracts for interoperability.

Design Principles:
- Immutable after creation (dataclasses with frozen=True for critical ones)
- Serializable to JSON for persistence
- Validatable at stage boundaries
- Self-documenting with clear field descriptions

Author: Carl Zimmerman
Date: May 4, 2026
"""

import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import hashlib


# =============================================================================
# ENUMS
# =============================================================================

class ResearchPhase(Enum):
    """Current phase of the research pipeline."""
    DISCOVERY = "discovery"
    VERIFICATION = "verification"
    STORAGE = "storage"
    TRAINING = "training"
    COMPLETE = "complete"
    FAILED = "failed"


class TruthStatus(Enum):
    """Status of a verified truth."""
    VALIDATED = "validated"      # HRM >= 0.8
    SPECULATIVE = "speculative"  # 0.5 <= HRM < 0.8
    PENDING = "pending"          # Needs verification
    REJECTED = "rejected"        # Failed verification
    DEPRECATED = "deprecated"    # Superseded


class DataFormat(Enum):
    """Format of discovered data."""
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    HTML_TABLE = "html_table"
    ASCII = "ascii"
    UNKNOWN = "unknown"


# =============================================================================
# BASE CONTRACT
# =============================================================================

@dataclass
class Contract:
    """Base class for all contracts with serialization."""

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str, indent=2)

    @classmethod
    def from_dict(cls, data: Dict) -> "Contract":
        """Create from dictionary."""
        # Filter to only valid fields
        valid_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**valid_fields)

    @classmethod
    def from_json(cls, json_str: str) -> "Contract":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))


# =============================================================================
# DISCOVERY CONTRACTS (HermesFlow output)
# =============================================================================

@dataclass
class DataSource(Contract):
    """Metadata about a discovered data source."""
    url: str
    title: str
    domain: str
    format: str = DataFormat.UNKNOWN.value
    rows: int = 0
    columns: int = 0
    column_names: List[str] = field(default_factory=list)
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def generate_id(self) -> str:
        """Generate unique ID for this source."""
        content = f"{self.url}:{self.domain}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


@dataclass
class Discovery(Contract):
    """
    Result of a data discovery operation.
    Flows: HermesFlow → VerificationStage
    """
    discovery_id: str
    topic: str
    domain: str
    quantities: List[str]
    success: bool
    source: Optional[DataSource] = None
    raw_data: Optional[Dict] = None  # Sample of data (first N rows as dict)
    steps_taken: int = 0
    exploration_log: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @staticmethod
    def generate_id(topic: str, domain: str) -> str:
        """Generate discovery ID."""
        content = f"{topic}:{domain}:{datetime.now().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


# =============================================================================
# FINDING CONTRACTS (Analysis output)
# =============================================================================

@dataclass
class Finding(Contract):
    """
    A potential Z² relationship found in data.
    Flows: AnalysisStage → VerificationStage
    """
    finding_id: str
    domain: str
    quantity: str
    measured_value: float
    target_constant: str  # e.g., "Z²", "φ", "π"
    target_value: float
    percent_error: float
    sample_size: int
    source_url: str
    measured_uncertainty: Optional[float] = None  # For AletheiaLake validation
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @staticmethod
    def generate_id(quantity: str, target: str) -> str:
        """Generate finding ID."""
        content = f"{quantity}:{target}:{datetime.now().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def is_significant(self, threshold: float = 5.0) -> bool:
        """Check if finding is statistically significant."""
        return self.percent_error < threshold and self.sample_size >= 30


# =============================================================================
# TRUTH CONTRACTS (Verified findings)
# =============================================================================

@dataclass
class HRMAssessment(Contract):
    """
    Hierarchical Recursive Meta-assessment result.
    Three-level honesty check for a finding.
    """
    level_1_score: float  # Basic honesty
    level_1_reasoning: str
    level_2_score: float  # Bias detection
    level_2_reasoning: str
    level_3_score: Optional[float] = None  # Final (if L1/L2 disagree)
    level_3_reasoning: Optional[str] = None
    final_score: float = 0.0

    def compute_final(self) -> float:
        """Compute final HRM score."""
        if abs(self.level_1_score - self.level_2_score) <= 0.2:
            self.final_score = (self.level_1_score + self.level_2_score) / 2
        elif self.level_3_score is not None:
            self.final_score = self.level_3_score
        else:
            self.final_score = min(self.level_1_score, self.level_2_score)
        return self.final_score


@dataclass
class VerifiedTruth(Contract):
    """
    A computationally verified truth.
    Flows: VerificationStage → MnemosyneLake
    """
    truth_id: str
    domain: str
    claim: str
    z2_formula: str
    z2_prediction: float
    measured_value: float
    measured_uncertainty: Optional[float] = None
    percent_error: float = 0.0
    sigma_deviation: Optional[float] = None
    hrm_score: float = 0.0
    hrm_assessment: Optional[HRMAssessment] = None
    status: str = TruthStatus.PENDING.value
    data_source: str = ""
    data_url: str = ""
    citations: List[str] = field(default_factory=list)
    verified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""
    ground_truth_ref: Optional[str] = None  # Reference to AletheiaLake truth if matched

    @staticmethod
    def generate_id(claim: str, domain: str) -> str:
        """Generate truth ID."""
        content = f"{domain}:{claim}".lower()
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def update_status(self):
        """Update status based on HRM score."""
        if self.hrm_score >= 0.8:
            self.status = TruthStatus.VALIDATED.value
        elif self.hrm_score >= 0.5:
            self.status = TruthStatus.SPECULATIVE.value
        elif self.hrm_score >= 0.3:
            self.status = TruthStatus.PENDING.value
        else:
            self.status = TruthStatus.REJECTED.value


# =============================================================================
# TRAINING CONTRACTS (Model training)
# =============================================================================

@dataclass
class TrainingExample(Contract):
    """
    A single training example for Legomena.
    Flows: MnemosyneLake → TrainingStage
    """
    instruction: str
    input: str
    output: str
    source_truth_id: Optional[str] = None

    def to_jsonl_line(self) -> str:
        """Convert to JSONL format line."""
        return json.dumps({
            "instruction": self.instruction,
            "input": self.input,
            "output": self.output
        })


@dataclass
class TrainingBatch(Contract):
    """
    A batch of training examples.
    Flows: TrainingStage → Legomena
    """
    batch_id: str
    examples: List[TrainingExample] = field(default_factory=list)
    source_domains: List[str] = field(default_factory=list)
    min_hrm_threshold: float = 0.8
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_example(self, example: TrainingExample):
        """Add an example to the batch."""
        self.examples.append(example)

    def to_jsonl(self) -> str:
        """Convert entire batch to JSONL format."""
        return '\n'.join(ex.to_jsonl_line() for ex in self.examples)


# =============================================================================
# PIPELINE CONTRACTS (Orchestration)
# =============================================================================

@dataclass
class PipelineConfig(Contract):
    """Configuration for a research pipeline."""
    name: str
    topic: str
    domain: str
    quantities: List[str] = field(default_factory=list)
    max_iterations: int = 10
    min_hrm_threshold: float = 0.8
    model_name: str = "legomena-moe"
    verbose: bool = True
    persist_state: bool = True


@dataclass
class StageResult(Contract):
    """Result from a single pipeline stage."""
    stage_name: str
    success: bool
    output: Optional[Any] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class PipelineState(Contract):
    """
    Current state of a running pipeline.
    Used for resumability and monitoring.
    """
    pipeline_id: str
    config: Dict
    current_phase: str = ResearchPhase.DISCOVERY.value
    current_iteration: int = 0
    stage_results: List[StageResult] = field(default_factory=list)
    discoveries: List[Discovery] = field(default_factory=list)
    findings: List[Finding] = field(default_factory=list)
    truths: List[VerifiedTruth] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @staticmethod
    def generate_id(name: str) -> str:
        """Generate pipeline ID."""
        content = f"{name}:{datetime.now().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def update(self):
        """Update timestamp."""
        self.updated_at = datetime.now().isoformat()


# =============================================================================
# EVENT CONTRACTS (Hooks and monitoring)
# =============================================================================

@dataclass
class Event(Contract):
    """An event emitted by the pipeline."""
    event_type: str
    source_stage: str
    payload: Dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_finding(finding: Finding) -> bool:
    """Validate a finding meets minimum criteria."""
    return (
        finding.percent_error < 10.0 and
        finding.sample_size >= 30 and
        finding.measured_value != 0
    )


def validate_truth(truth: VerifiedTruth) -> bool:
    """Validate a truth meets storage criteria."""
    return (
        truth.hrm_score >= 0.5 and
        truth.percent_error < 5.0 and
        truth.status != TruthStatus.REJECTED.value
    )


if __name__ == "__main__":
    # Demo
    print("OlympusFlow Data Contracts")
    print("=" * 40)

    # Create a discovery
    discovery = Discovery(
        discovery_id=Discovery.generate_id("earthquake", "seismology"),
        topic="USGS earthquake data",
        domain="seismology",
        quantities=["magnitude", "depth"],
        success=True,
        source=DataSource(
            url="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv",
            title="USGS Earthquake Feed",
            domain="seismology",
            format=DataFormat.CSV.value,
            rows=10000,
            columns=22
        )
    )
    print(f"Discovery: {discovery.discovery_id}")

    # Create a finding
    finding = Finding(
        finding_id=Finding.generate_id("CV(magnitude)", "Z²"),
        domain="seismology",
        quantity="CV(magnitude)",
        measured_value=33.51,
        target_constant="Z²",
        target_value=33.510321638291124,
        percent_error=0.001,
        sample_size=10000,
        source_url=discovery.source.url
    )
    print(f"Finding: {finding.finding_id} - {finding.quantity} = {finding.target_constant}")
    print(f"  Significant: {finding.is_significant()}")

    # Create verified truth
    truth = VerifiedTruth(
        truth_id=VerifiedTruth.generate_id("CV(magnitude) = Z²", "seismology"),
        domain="seismology",
        claim="CV(magnitude) = Z²",
        z2_formula="Z² = 32π/3",
        z2_prediction=33.510321638291124,
        measured_value=33.51,
        percent_error=0.001,
        hrm_score=0.95
    )
    truth.update_status()
    print(f"Truth: {truth.truth_id} - Status: {truth.status}")
