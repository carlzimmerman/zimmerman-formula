"""
OLYMPUSFLOW - Unified Research Orchestrator
============================================

OlympusFlow is the central orchestrator for Z² research, bringing together:
- HermesFlow (data discovery)
- TruthFlow (verification)
- CylleneFlow (iterative learning)
- MnemosyneLake (truth storage)
- Legomena (reasoning)

Named after Mount Olympus, home of the Greek gods.

Quick Start:
    from OlympusFlow import research

    results = research(
        topic="USGS earthquake magnitude data",
        domain="seismology",
        quantities=["magnitude", "depth"],
        iterations=5
    )

Full Control:
    from OlympusFlow import Pipeline, PipelineConfig
    from OlympusFlow.stages import (
        DiscoveryStage, AnalysisStage,
        VerificationStage, StorageStage
    )

    config = PipelineConfig(
        name="earthquake_research",
        topic="USGS earthquake data",
        domain="seismology",
        quantities=["magnitude", "depth"]
    )

    pipeline = Pipeline("eq_research", config)
    pipeline.add_stage(DiscoveryStage(...))
    pipeline.add_stage(AnalysisStage())
    pipeline.add_stage(VerificationStage())
    pipeline.add_stage(StorageStage())

    results = pipeline.run(max_iterations=10)

Event Hooks:
    from OlympusFlow.events import on, EventType

    @on(EventType.TRUTH_CREATED)
    def handle_truth(event):
        print(f"New truth: {event.payload['claim']}")

Author: Carl Zimmerman
Date: May 4, 2026

v1.4.0 Changes (May 5, 2026):
- Integrated CylleneFlow Deepener for recursive research
- When significant findings discovered, automatically investigates deeper
- Generates research questions from findings and runs HermesFlow on each
- New events: DEEPENING_TRIGGERED, DEEPENING_STARTED, DEEPENING_COMPLETED
- Pipeline summary now includes deepening_findings count
"""

__version__ = "1.5.0"  # Added StatisticalValidator for rigorous significance testing

# Core components
from .contracts import (
    # Enums
    ResearchPhase, TruthStatus, DataFormat,

    # Data contracts
    DataSource, Discovery, Finding,
    HRMAssessment, VerifiedTruth,
    TrainingExample, TrainingBatch,

    # Pipeline contracts
    PipelineConfig, StageResult, PipelineState, Event
)

from .events import (
    EventBus, EventType, EventEmitter,
    ConsoleLogger, MetricsCollector,
    get_event_bus, set_event_bus, on, emit
)

from .stages import (
    Stage,
    DiscoveryStage,
    AnalysisStage,
    VerificationStage,
    StorageStage,
    TrainingStage,
    SequentialStages
)

from .pipeline import Pipeline, research

# Constants (centralized Z² values and thresholds)
from .constants import (
    Z2, Z, PHI, INV_PHI, PI, E,
    Z2_TARGETS,
    HRMThresholds, PatternThresholds, ValidationThresholds,
    get_target, matches_z2_target, hrm_to_status
)

# Statistical validation (eliminates false positives)
from .statistical_validator import (
    StatisticalValidator,
    PatternCandidate,
    ValidationResult,
    MonteCarloValidator,
    MultipleComparisonCorrector,
    EffectSizeCalculator,
    TemporalStabilityTester,
    MultiSourceCorroborator,
    LegomenaCodeGenerator,
    validate_pattern_quick,
    TARGETS
)

__all__ = [
    # Version
    "__version__",

    # Enums
    "ResearchPhase", "TruthStatus", "DataFormat",

    # Data contracts
    "DataSource", "Discovery", "Finding",
    "HRMAssessment", "VerifiedTruth",
    "TrainingExample", "TrainingBatch",

    # Pipeline contracts
    "PipelineConfig", "StageResult", "PipelineState", "Event",

    # Events
    "EventBus", "EventType", "EventEmitter",
    "ConsoleLogger", "MetricsCollector",
    "get_event_bus", "set_event_bus", "on", "emit",

    # Stages
    "Stage",
    "DiscoveryStage",
    "AnalysisStage",
    "VerificationStage",
    "StorageStage",
    "TrainingStage",
    "SequentialStages",

    # Pipeline
    "Pipeline",
    "research",

    # Constants
    "Z2", "Z", "PHI", "INV_PHI", "PI", "E",
    "Z2_TARGETS",
    "HRMThresholds", "PatternThresholds", "ValidationThresholds",
    "get_target", "matches_z2_target", "hrm_to_status",

    # Statistical validation
    "StatisticalValidator",
    "PatternCandidate",
    "ValidationResult",
    "MonteCarloValidator",
    "MultipleComparisonCorrector",
    "EffectSizeCalculator",
    "TemporalStabilityTester",
    "MultiSourceCorroborator",
    "LegomenaCodeGenerator",
    "validate_pattern_quick",
    "TARGETS"
]
