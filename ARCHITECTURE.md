# Z² Discovery Engine - Complete Architecture

## Date: May 6, 2026

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              Z² AUTONOMOUS DISCOVERY ENGINE                              │
│                                                                                          │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                         USER INPUT / RESEARCH QUESTION                             │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                          │                                               │
│                                          ▼                                               │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              HERMESFLOW (Research Agent)                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │ Web Search  │  │ Web Extract │  │ Web Crawl   │  │ Autonomous Research     │   │  │
│  │  │ (Exa/Tavily │  │ (Firecrawl) │  │ (Firecrawl) │  │ (discovery_engine.py)   │   │  │
│  │  │  /Parallel) │  │             │  │             │  │                         │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  │                                          │                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                    hermes_agent/ (Full Agent Toolkit)                        │  │  │
│  │  │  • Browser tools   • File tools     • Terminal     • MCP integration        │  │  │
│  │  │  • Vision tools    • Memory         • Skills       • Transcription          │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                          │                                               │
│                    ┌─────────────────────┴─────────────────────┐                        │
│                    ▼                                           ▼                        │
│  ┌─────────────────────────────────┐     ┌─────────────────────────────────────────┐   │
│  │        METISFLOW                │     │              ALPHEUSFLOW                 │   │
│  │    (Literature & Strategy)      │     │         (Queue & Orchestration)          │   │
│  │                                 │     │                                          │   │
│  │  ┌─────────────────────────┐   │     │  ┌──────────────────────────────────┐   │   │
│  │  │ literature_searcher.py  │   │     │  │          queue.py                 │   │   │
│  │  │ • Search papers         │   │     │  │  • ResearchTask                   │   │   │
│  │  │ • Find derivations      │   │     │  │  • TaskPriority                   │   │   │
│  │  │ • Z² relevance scoring  │   │     │  │  • BatchConfig                    │   │   │
│  │  └─────────────────────────┘   │     │  └──────────────────────────────────┘   │   │
│  │  ┌─────────────────────────┐   │     │  ┌──────────────────────────────────┐   │   │
│  │  │ derivation_strategy.py  │   │     │  │       orchestrator.py             │   │   │
│  │  │ • Approach selection    │   │     │  │  • Pull tasks                     │   │   │
│  │  │ • Framework matching    │   │     │  │  • Run through OlympusFlow        │   │   │
│  │  └─────────────────────────┘   │     │  │  • Record results                 │   │   │
│  └─────────────────────────────────┘     │  └──────────────────────────────────┘   │   │
│                    │                     └─────────────────────────────────────────┘   │
│                    │                                           │                        │
│                    └─────────────────────┬─────────────────────┘                        │
│                                          ▼                                               │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              OLYMPUSFLOW (Main Engine)                             │  │
│  │                                                                                     │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │  │
│  │  │ derivation_     │  │ formula_        │  │ sympy_          │  │ learning_    │  │  │
│  │  │ engine.py       │  │ generator.py    │  │ verifier.py     │  │ loop.py      │  │  │
│  │  │                 │  │                 │  │                 │  │              │  │  │
│  │  │ • Generate      │  │ • Template      │  │ • Algebraic     │  │ • Success    │  │  │
│  │  │   derivations   │→ │   expansion     │→ │   verification  │→ │   patterns   │  │  │
│  │  │ • HRM scoring   │  │ • LLM proposal  │  │ • Z² essential  │  │ • Failure    │  │  │
│  │  │                 │  │                 │  │   detection     │  │   analysis   │  │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘  │  │
│  │                                          │                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                      autonomous_controller.py                                │  │  │
│  │  │  • Continuous operation   • Queue integration   • Checkpointing              │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                          │                                               │
│                    ┌─────────────────────┴─────────────────────┐                        │
│                    ▼                                           ▼                        │
│  ┌─────────────────────────────────┐     ┌─────────────────────────────────────────┐   │
│  │        BRIAREUSFLOW             │     │              TRUTHFLOW                   │   │
│  │   (Brute-Force Discovery)       │     │         (Validation Pipeline)            │   │
│  │                                 │     │                                          │   │
│  │  ┌─────────────────────────┐   │     │  ┌──────────────────────────────────┐   │   │
│  │  │   pattern_search.py     │   │     │  │     robust_validator.py           │   │   │
│  │  │  • 34,000+ patterns     │   │     │  │  • Triple verification            │   │   │
│  │  │  • Fractions, π, √n     │   │     │  │  • Uncertainty propagation        │   │   │
│  │  │  • Z² terms, φ          │   │     │  │  • Statistical significance       │   │   │
│  │  └─────────────────────────┘   │     │  └──────────────────────────────────┘   │   │
│  │  ┌─────────────────────────┐   │     │  ┌──────────────────────────────────┐   │   │
│  │  │ geometric_interpreter   │   │     │  │   autonomous_discovery.py         │   │   │
│  │  │  • Pattern meaning      │   │     │  │  • Discovery mode                 │   │   │
│  │  │  • Cross-domain links   │   │     │  │  • Hypothesis generation          │   │   │
│  │  └─────────────────────────┘   │     │  └──────────────────────────────────┘   │   │
│  │  ┌─────────────────────────┐   │     └─────────────────────────────────────────┘   │
│  │  │    olympus_bridge.py    │   │                                                    │
│  │  │  • OlympusFlow link     │───┼────────────────────────────────────────────────┐   │
│  │  └─────────────────────────┘   │                                                │   │
│  └─────────────────────────────────┘                                                │   │
│                                          │                                          │   │
│                                          ▼                                          │   │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              CYLLENEFLOW (Deepening)                               │  │
│  │                                                                                     │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │  │
│  │  │   deepener.py   │  │ training_       │  │ iteration_      │  │ model_       │  │  │
│  │  │                 │  │ generator.py    │  │ runner.py       │  │ updater.py   │  │  │
│  │  │ • Generate      │  │ • Create        │  │ • Run training  │  │ • Fine-tune  │  │  │
│  │  │   questions     │→ │   training data │→ │   iterations    │→ │   Legomena   │  │  │
│  │  │ • Priority      │  │ • From verified │  │                 │  │              │  │  │
│  │  │   scoring       │  │   findings      │  │                 │  │              │  │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                          │                                               │
│                                          ▼                                               │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                  STORAGE LAKES                                     │  │
│  │                                                                                     │  │
│  │  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────┐ │  │
│  │  │      ALETHEIALAKE       │  │      HELICONLAKE        │  │    MNEMOSYNE LAKE   │ │  │
│  │  │    (Verified Truths)    │  │  (Research Sessions)    │  │ (Memory/Context)    │ │  │
│  │  │                         │  │                         │  │                     │ │  │
│  │  │  • Z² derivations       │  │  • Session history      │  │  • Working memory   │ │  │
│  │  │  • First-principles     │  │  • Discovery logs       │  │  • Past context     │ │  │
│  │  │  • Ground truths        │  │  • Failed attempts      │  │  • Learned patterns │ │  │
│  │  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Current Automation Gaps

| Step | Component | Status | Gap |
|------|-----------|--------|-----|
| 1 | HermesFlow web_tools | ✓ Built | Not integrated with pipeline |
| 2 | MetisFlow literature | ✓ Built | Uses mock, not real web |
| 3 | Domain Creation | ❌ Manual | Need JSON registry |
| 4-7 | BriareusFlow + OlympusFlow | ✓ Automated | None |
| 8 | CylleneFlow deepening | ✓ Built | Not looping back |

---

## Key Integration Needed

**HermesFlow has web tools but they're not connected to the pipeline!**

```
CURRENT:
  User → [Claude searches web manually] → Domain → BriareusFlow → ...

SHOULD BE:
  User → HermesFlow.web_search → MetisFlow.extract → DomainRegistry → BriareusFlow → ...
```

---

## Component Summary

| Component | Role | Files |
|-----------|------|-------|
| HermesFlow | Web research agent | web_tools.py, research.py, discovery_engine.py |
| MetisFlow | Literature strategy | literature_searcher.py, derivation_strategy.py |
| AlpheusFlow | Task queue | queue.py, orchestrator.py |
| OlympusFlow | Derivation engine | derivation_engine.py, sympy_verifier.py |
| BriareusFlow | Pattern search | pattern_search.py, geometric_interpreter.py |
| TruthFlow | Validation | robust_validator.py |
| CylleneFlow | Deepening | deepener.py, training_generator.py |
| AletheiaLake | Verified truths | lake.py |
| HeliconLake | Session history | - |
| MnemosyneLake | Memory | lake.py |

---

*Architecture document - May 6, 2026*
