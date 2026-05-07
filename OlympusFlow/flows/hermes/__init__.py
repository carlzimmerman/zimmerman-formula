"""
HERMESFLOW - Web Research Agent
================================

Named after Hermes, the Greek messenger god. Like Hermes who crossed
boundaries between worlds, this flow bridges the gap between web data
and Z² research.

HermesFlow handles:
1. Web data discovery and acquisition
2. API query handling
3. Literature collection
4. Autonomous research loops
5. Scientific validation
6. Research bridging to OlympusFlow

Components:
- HermesFlowRunner: Main orchestrator for web research
- ResearchBridge: Bridge between web data and OlympusFlow
- AutonomousAgent: Self-directed research agent
- ScientificMethod: Hypothesis testing framework
- ScientificValidator: Data validation engine
- DatabaseQueryHandler: API query management
- HermesNavigator: Web navigation
- TruthDatabase: Research truth storage
- TopicValidator: Topic relevance checking
- HermesDataAgent: Data acquisition agent

Usage:
    from OlympusFlow.flows.hermes import HermesFlowRunner, ResearchBridge

    runner = HermesFlowRunner()
    results = runner.run_research("von Karman constant")
"""

__version__ = "1.0.0"

# Core components
from .hermesflow_runner import HermesFlowRunner, DataQualityFilter
from .research_bridge import ResearchBridge

# Autonomous research
from .autonomous_agent import AutonomousAgent, AgentState, Learning

# Scientific framework
from .scientific_method import (
    ScientificMethod, Hypothesis, Measurement,
    StatisticalTest, ExperimentResult
)
from .scientific_validator import (
    ScientificValidator, AuthoritativeSource,
    EmpiricalMeasurement, Z2Prediction, ValidationResult
)

# Data handling
from .database_query_handler import DatabaseQueryHandler, APIConfig, QueryResult
from .hermes_navigator import HermesNavigator, NavigationResult
from .hermes_data_agent import HermesDataAgent, DataSource, ParsedDataset

# Truth management
from .truth_database import (
    TruthDatabase, Truth, HRMAssessment,
    TruthCandidate, TruthConsistencyChecker, DynamicFlowManager
)

# Topic validation
from .topic_validator import TopicValidator

# Web search
from .firecrawl_search import FirecrawlSearcher

__all__ = [
    "__version__",
    # Core
    "HermesFlowRunner",
    "DataQualityFilter",
    "ResearchBridge",
    # Autonomous
    "AutonomousAgent",
    "AgentState",
    "Learning",
    # Scientific
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
    # Data
    "DatabaseQueryHandler",
    "APIConfig",
    "QueryResult",
    "HermesNavigator",
    "NavigationResult",
    "HermesDataAgent",
    "DataSource",
    "ParsedDataset",
    # Truth
    "TruthDatabase",
    "Truth",
    "HRMAssessment",
    "TruthCandidate",
    "TruthConsistencyChecker",
    "DynamicFlowManager",
    # Validation
    "TopicValidator",
    # Search
    "FirecrawlSearcher",
]
