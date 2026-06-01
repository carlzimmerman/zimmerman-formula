"""
HERMESFLOW - Web Research Agent
================================

DEPRECATED: This module has moved to OlympusFlow.flows.hermes

Please update imports:
    OLD: from HermesFlow.research_bridge import ResearchBridge
    NEW: from OlympusFlow.flows.hermes import ResearchBridge

    OR: from OlympusFlow.flows import ResearchBridge

This file re-exports from the new location for backward compatibility.
"""

import warnings

warnings.warn(
    "HermesFlow has moved to OlympusFlow.flows.hermes. "
    "Please update imports: from OlympusFlow.flows.hermes import HermesFlowRunner",
    DeprecationWarning,
    stacklevel=2
)

__version__ = "3.0.0"

# Re-export from new location
from OlympusFlow.flows.hermes import (
    HermesFlowRunner,
    DataQualityFilter,
    ResearchBridge,
    AutonomousAgent,
    AgentState,
    Learning,
    ScientificMethod,
    Hypothesis,
    Measurement,
    StatisticalTest,
    ExperimentResult,
    ScientificValidator,
    AuthoritativeSource,
    EmpiricalMeasurement,
    Z2Prediction,
    ValidationResult,
    DatabaseQueryHandler,
    APIConfig,
    QueryResult,
    HermesNavigator,
    NavigationResult,
    HermesDataAgent,
    DataSource,
    ParsedDataset,
    TruthDatabase,
    Truth,
    HRMAssessment,
    TruthCandidate,
    TruthConsistencyChecker,
    DynamicFlowManager,
    TopicValidator,
    FirecrawlSearcher,
)

__all__ = [
    "__version__",
    "HermesFlowRunner",
    "DataQualityFilter",
    "ResearchBridge",
    "AutonomousAgent",
    "AgentState",
    "Learning",
    "ScientificMethod",
    "Hypothesis",
    "Measurement",
    "StatisticalTest",
    "ExperimentResult",
    "ScientificValidator",
    "AuthoritativeSource",
    "EmpiricalMeasurement",
    "Z2Prediction",
    "ValidationResult",
    "DatabaseQueryHandler",
    "APIConfig",
    "QueryResult",
    "HermesNavigator",
    "NavigationResult",
    "HermesDataAgent",
    "DataSource",
    "ParsedDataset",
    "TruthDatabase",
    "Truth",
    "HRMAssessment",
    "TruthCandidate",
    "TruthConsistencyChecker",
    "DynamicFlowManager",
    "TopicValidator",
    "FirecrawlSearcher",
]
