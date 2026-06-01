"""
WATCHER CONTRACTS - Data Structures for Oversight System
=========================================================

Defines the core contracts for watchers to communicate with
flows, lakes, and each other.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime


class InterventionType(Enum):
    """Types of interventions a watcher can trigger."""
    PASS = "pass"                    # No intervention needed
    WARN = "warn"                    # Log warning, continue
    CORRECT = "correct"              # Apply correction, continue
    HALT = "halt"                    # Stop pipeline, require review
    REJECT = "reject"                # Reject entry, skip storage
    ESCALATE = "escalate"            # Escalate to higher watcher


class TrustLevel(Enum):
    """Trust levels assigned by watchers."""
    HIGH = "high"                    # Verified, first-principles
    MEDIUM = "medium"                # Plausible, needs validation
    LOW = "low"                      # Speculative, weak evidence
    SUSPECT = "suspect"              # Potential issues detected
    UNTRUSTED = "untrusted"          # Failed validation


class WatcherPriority(Enum):
    """Priority levels for watcher alerts."""
    CRITICAL = 0    # Immediate action required
    HIGH = 1        # Process soon
    NORMAL = 2      # Standard priority
    LOW = 3         # Informational


class ConsensusSource(Enum):
    """Sources for consensus checking."""
    LEGOMENA = "legomena"            # Local Legomena model
    GEMINI = "gemini"                # Google Gemini API
    CLAUDE = "claude"                # Anthropic Claude API
    ARXIV = "arxiv"                  # arXiv literature
    CODATA = "codata"                # CODATA/NIST values
    PDG = "pdg"                      # Particle Data Group
    PLANCK = "planck"                # Planck collaboration


@dataclass
class WatcherNote:
    """
    Immutable note appended to MnemosyneLake entries.

    Once created, these notes cannot be modified - only superseded
    by newer notes with updated assessments.
    """
    watcher_id: str                  # Which watcher created this
    timestamp: str                   # When note was created

    # Assessment
    trust_level: TrustLevel
    trust_score: float               # 0.0 - 1.0
    intervention: InterventionType

    # Checks performed
    provenance_verified: bool        # Source URL/citation checked
    logic_validated: bool            # No hidden assumptions
    framework_aligned: bool          # Consistent with Z² principles

    # Details
    advisory: str                    # Human-readable note
    issues_found: List[str] = field(default_factory=list)
    corrections_applied: List[str] = field(default_factory=list)

    # Consensus
    consensus_sources: List[str] = field(default_factory=list)
    consensus_agreement: float = 0.0  # 0.0 - 1.0

    def to_dict(self) -> Dict:
        return {
            "watcher_id": self.watcher_id,
            "timestamp": self.timestamp,
            "trust_level": self.trust_level.value,
            "trust_score": self.trust_score,
            "intervention": self.intervention.value,
            "provenance_verified": self.provenance_verified,
            "logic_validated": self.logic_validated,
            "framework_aligned": self.framework_aligned,
            "advisory": self.advisory,
            "issues_found": self.issues_found,
            "corrections_applied": self.corrections_applied,
            "consensus_sources": self.consensus_sources,
            "consensus_agreement": self.consensus_agreement
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "WatcherNote":
        return cls(
            watcher_id=data["watcher_id"],
            timestamp=data["timestamp"],
            trust_level=TrustLevel(data["trust_level"]),
            trust_score=data["trust_score"],
            intervention=InterventionType(data["intervention"]),
            provenance_verified=data.get("provenance_verified", False),
            logic_validated=data.get("logic_validated", False),
            framework_aligned=data.get("framework_aligned", False),
            advisory=data.get("advisory", ""),
            issues_found=data.get("issues_found", []),
            corrections_applied=data.get("corrections_applied", []),
            consensus_sources=data.get("consensus_sources", []),
            consensus_agreement=data.get("consensus_agreement", 0.0)
        )


@dataclass
class StageTransition:
    """
    Represents a transition between pipeline stages.
    This is what watchers intercept and audit.
    """
    # Source
    source_stage: str                # Where data came from
    source_agent: str                # Which agent produced it

    # Destination
    target_stage: str                # Where data is going
    target_storage: str              # Lake or next stage

    # Payload
    result_type: str                 # Type of result (Finding, Truth, etc.)
    result_data: Dict                # The actual data being transferred

    # Context
    pipeline_id: str                 # Which pipeline run
    task_id: str                     # Which task
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # Metrics from source
    confidence: float = 0.0
    hrm_score: float = 0.0
    percent_error: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "source_stage": self.source_stage,
            "source_agent": self.source_agent,
            "target_stage": self.target_stage,
            "target_storage": self.target_storage,
            "result_type": self.result_type,
            "result_data": self.result_data,
            "pipeline_id": self.pipeline_id,
            "task_id": self.task_id,
            "timestamp": self.timestamp,
            "confidence": self.confidence,
            "hrm_score": self.hrm_score,
            "percent_error": self.percent_error
        }


@dataclass
class WatcherResult:
    """
    Result of a watcher's audit of a stage transition.
    """
    # Identity
    watcher_id: str
    transition_id: str               # Hash of transition
    timestamp: str

    # Decision
    intervention: InterventionType
    allow_continue: bool             # Can pipeline continue?

    # Assessment
    note: WatcherNote                # Detailed note for storage

    # If intervention required
    correction_applied: Optional[Dict] = None
    halt_reason: Optional[str] = None
    escalate_to: Optional[str] = None

    # Timing
    audit_duration_ms: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "watcher_id": self.watcher_id,
            "transition_id": self.transition_id,
            "timestamp": self.timestamp,
            "intervention": self.intervention.value,
            "allow_continue": self.allow_continue,
            "note": self.note.to_dict(),
            "correction_applied": self.correction_applied,
            "halt_reason": self.halt_reason,
            "escalate_to": self.escalate_to,
            "audit_duration_ms": self.audit_duration_ms
        }


@dataclass
class WatcherConfig:
    """
    Configuration for a watcher instance.
    """
    # Identity
    watcher_id: str = "hecate-1"
    watcher_name: str = "Hecate"

    # Behavior
    blocking_mode: bool = False      # If True, halt on issues
    blocking_threshold: float = 0.5  # HRM below this triggers block
    deviation_threshold: float = 3.0 # Sigma deviation threshold

    # Dual-model configuration
    dual_model: bool = True          # Use both external + Legomena
    external_model: str = "gemini"   # External API to use
    legomena_model: str = "legomena-moe"

    # Timeouts (seconds)
    external_timeout: int = 30
    legomena_timeout: int = 60

    # What to watch
    watch_stages: List[str] = field(default_factory=lambda: [
        "discovery", "analysis", "verification", "storage",
        "metis", "derivation", "training"
    ])

    # Storage
    notes_persist: bool = True       # Persist notes to disk
    notes_path: str = ""             # Path for notes storage

    # Logging
    verbose: bool = True
    log_all_transitions: bool = False


@dataclass
class ConsensusCheck:
    """
    Result of a consensus check across multiple sources.
    """
    query: str                       # What was checked
    sources_queried: List[str]

    # Results per source
    source_results: Dict[str, Dict]  # source -> {agrees, confidence, notes}

    # Aggregated
    overall_agreement: float         # 0.0 - 1.0
    majority_view: str               # What most sources say
    dissenting_views: List[str]      # Disagreements

    # Issues
    conflicts_detected: bool
    conflict_description: str = ""

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class FrameworkCheck:
    """
    Result of checking alignment with Z² framework principles.
    """
    # What was checked
    claim: str
    formula: str
    computed_value: float

    # Z² alignment
    uses_z2_constant: bool           # References Z² = 32π/3
    has_geometric_basis: bool        # Based on geometry, not fitting
    has_physical_mechanism: bool     # Explains WHY, not just WHAT

    # AletheiaLake validation
    aletheia_match: bool             # Matches ground truth
    aletheia_truth_name: str = ""    # Which truth it matches
    aletheia_deviation: float = 0.0  # Deviation in sigma

    # Hidden assumptions
    assumptions_detected: List[str] = field(default_factory=list)
    problematic_assumptions: List[str] = field(default_factory=list)

    # Score
    framework_score: float = 0.0     # 0.0 - 1.0

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
