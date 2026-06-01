# Z² Discovery Engine - Complete System Guide

**Date:** May 6, 2026
**Version:** 2.0 (Fully Automated Pipeline)

---

## Quick Start

```bash
# Run discovery on a known topic
python run_discovery.py "turbulence constants"

# Run discovery with web research (for unknown topics)
python run_discovery.py "any new topic" --research

# Test the automated pipeline
python test_automated_discovery.py --topic "kleiber law"
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Z² AUTONOMOUS DISCOVERY ENGINE                       │
│                                                                              │
│  USER INPUT: "Research topic X"                                              │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    HERMESFLOW (Research Layer)                       │    │
│  │                                                                      │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │    │
│  │  │ firecrawl_      │    │ research_       │    │ ConstantExtractor│ │    │
│  │  │ search.py       │───▶│ bridge.py       │───▶│ (NLP/Regex)     │ │    │
│  │  │                 │    │                 │    │                 │ │    │
│  │  │ • Web search    │    │ • Topic query   │    │ • Extract values│ │    │
│  │  │ • URL scraping  │    │ • Domain create │    │ • Parse text    │ │    │
│  │  │ • Firecrawl API │    │ • JSON export   │    │ • Find constants│ │    │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘ │    │
│  │                                │                                    │    │
│  │                                ▼                                    │    │
│  │                    ┌─────────────────────────┐                      │    │
│  │                    │     DomainRegistry      │                      │    │
│  │                    │  (JSON domain files)    │                      │    │
│  │                    └─────────────────────────┘                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                │                                             │
│                                ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    BRIAREUSFLOW (Pattern Search)                     │    │
│  │                                                                      │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │    │
│  │  │ pattern_search  │    │ geometric_      │    │ olympus_bridge  │ │    │
│  │  │     .py         │───▶│ interpreter.py  │───▶│     .py         │ │    │
│  │  │                 │    │                 │    │                 │ │    │
│  │  │ • 34,000+ combs │    │ • Physical      │    │ • Filter best   │ │    │
│  │  │ • Z², π, √n, φ  │    │   meaning       │    │ • Send to       │ │    │
│  │  │ • Fractions     │    │ • Cross-domain  │    │   OlympusFlow   │ │    │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘ │    │
│  │                                                                      │    │
│  │  briareus_controller.py: Multi-threaded orchestration (100 hands)   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                │                                             │
│                                ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    OLYMPUSFLOW (Validation Engine)                   │    │
│  │                                                                      │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │    │
│  │  │ derivation_     │    │ sympy_          │    │ learning_       │ │    │
│  │  │ engine.py       │───▶│ verifier.py     │───▶│ loop.py         │ │    │
│  │  │                 │    │                 │    │                 │ │    │
│  │  │ • LLM derivation│    │ • Algebraic     │    │ • Pattern       │ │    │
│  │  │ • Multi-pass    │    │   verification  │    │   learning      │ │    │
│  │  │ • HRM scoring   │    │ • Z² detection  │    │ • Template      │ │    │
│  │  └─────────────────┘    └─────────────────┘    │   extraction    │ │    │
│  │                                                └─────────────────┘ │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                │                                             │
│                    ┌───────────┴───────────┐                                │
│                    ▼                       ▼                                │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────────┐  │
│  │      TRUTHFLOW          │  │              STORAGE LAKES               │  │
│  │   (Validation)          │  │                                          │  │
│  │                         │  │  ┌───────────┐ ┌───────────┐ ┌────────┐ │  │
│  │  • Triple verification  │  │  │ ALETHEIA  │ │  HELICON  │ │MNEMOSYNE│ │  │
│  │  • Uncertainty prop.    │  │  │  LAKE     │ │   LAKE    │ │  LAKE   │ │  │
│  │  • Statistical signif.  │  │  │ (Truths)  │ │ (Sessions)│ │(Memory) │ │  │
│  │                         │  │  └───────────┘ └───────────┘ └────────┘ │  │
│  └─────────────────────────┘  └─────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Reference

### 1. HermesFlow (Web Research)

**Location:** `HermesFlow/`

| File | Purpose |
|------|---------|
| `firecrawl_search.py` | Standalone Firecrawl API wrapper |
| `research_bridge.py` | Connects web research to BriareusFlow |
| `hermes_agent/` | Full agent toolkit (browser, vision, MCP) |

**Usage:**
```python
from HermesFlow.research_bridge import ResearchBridge

bridge = ResearchBridge()
domain = await bridge.research_topic("turbulence constants")
targets = domain.to_search_targets()
```

**Environment Variables:**
```bash
FIRECRAWL_API_KEY=your_key  # or FIRECRAWL_ACCESS_TOKEN
```

### 2. BriareusFlow (Pattern Search)

**Location:** `BriareusFlow/`

| File | Purpose |
|------|---------|
| `briareus_controller.py` | Multi-threaded search orchestration |
| `pattern_search.py` | Brute-force pattern matching (~34,000 combinations) |
| `geometric_interpreter.py` | Physical meaning extraction |
| `olympus_bridge.py` | Interface to OlympusFlow |
| `phenomenological.py` | Finding data structures |
| `domains/*.json` | Saved domain definitions |

**Pattern Types Searched:**
- Fractions: a/b (up to 50/50)
- Z² expressions: aZ² + b, a/Z², etc.
- π expressions: aπ/b, a + bπ
- Square roots: √n/m
- Trigonometric: arccos(a/b), arctan(a/b)
- Golden ratio: φ, 1/φ, φ²

### 3. OlympusFlow (Derivation Engine)

**Location:** `OlympusFlow/`

| File | Purpose |
|------|---------|
| `derivation_engine.py` | LLM-based derivation attempts |
| `formula_generator.py` | Template expansion |
| `sympy_verifier.py` | Algebraic verification |
| `learning_loop.py` | Pattern learning from successes |
| `autonomous_controller.py` | Continuous operation |

**HRM Scoring:**
- **H**onesty: Does the derivation acknowledge assumptions?
- **R**igor: Is the math correct?
- **M**echanism: Is there a physical explanation?

### 4. MetisFlow (Literature Strategy)

**Location:** `MetisFlow/`

| File | Purpose |
|------|---------|
| `literature_searcher.py` | Search for existing derivations |
| `derivation_strategy.py` | Choose derivation approach |

### 5. AlpheusFlow (Queue Orchestration)

**Location:** `AlpheusFlow/`

| File | Purpose |
|------|---------|
| `queue.py` | Task queue management |
| `orchestrator.py` | Process tasks through OlympusFlow |

### 6. CylleneFlow (Deepening)

**Location:** `CylleneFlow/`

| File | Purpose |
|------|---------|
| `deepener.py` | Generate research questions |
| `training_generator.py` | Create training data |
| `model_updater.py` | Fine-tune Legomena |

### 7. TruthFlow (Validation)

**Location:** `TruthFlow/`

| File | Purpose |
|------|---------|
| `robust_validator.py` | Triple verification |
| `autonomous_discovery.py` | Discovery mode |

### 8. Storage Lakes

| Lake | Purpose | Location |
|------|---------|----------|
| **AletheiaLake** | Verified truths (immutable) | `AletheiaLake/` |
| **HeliconLake** | Session history | `HeliconLake/` |
| **MnemosyneLake** | Working memory | `MnemosyneLake/` |

---

## Available Domains

Run `python run_discovery.py "<topic>"` with:

| Topic | Constants | Key Findings |
|-------|-----------|--------------|
| `eddington` | 8 | Thomson 8π/3, Kerr efficiency |
| `roche` | 6 | Roche limit 2.44 |
| `titius-bode` | 8 | Planetary spacing |
| `geodynamo` | 6 | Critical Rm ≈ 2Z² - 27 |
| `golden` | 4 | φ, φ², ln(φ) |
| `snowflake` | 19 | 60° ≈ 2Z² - 7, tetrahedral |
| `turbulence` | 19 | κ ≈ 2/5, Strouhal ≈ 6/Z² |
| `river-network` | 19 | Hack h ≈ 19/Z² |

---

## Key Z² Discoveries

| Domain | Pattern | Value | Error |
|--------|---------|-------|-------|
| Fine structure | 4Z² + 3 | 137.04 | ~0.01% |
| Kleiber | 25/Z² | 0.746 ≈ 3/4 | <1% |
| Kolmogorov | 25/Z² | 0.746 ≈ 3/4 | <1% |
| Gutenberg-Richter | Z² - 2 | 31.5 ≈ 10^1.5 | <1% |
| Snowflake 60° | 2Z² - 7 | 60.02 | 0.03% |
| Water 104.5° | 3Z² + 4 | 104.53 | 0.03% |
| Strouhal wake | 6/Z² | 0.179 | 0.6% |
| Hack's law | 19/Z² | 0.567 | 0.18% |
| River fractal | 1 + 25/Z² | 1.746 | 0.23% |

---

## Entry Points

| Script | Purpose |
|--------|---------|
| `run_discovery.py` | Main CLI entry point |
| `run_full_discovery.py` | Extended discovery with more domains |
| `test_automated_discovery.py` | Test the pipeline |

---

## Configuration

### Firecrawl (Web Research)
```bash
# In ~/.env or /Users/carlzimmerman/new_physics/.env
FIRECRAWL_API_KEY=fc-your-key-here
```

### BriareusFlow
```python
config = SearchConfig(
    max_error_percent=1.0,    # Maximum error to report
    max_integer=50,           # Largest integer in fractions
    max_denominator=50,       # Largest denominator
    num_threads=8,            # Parallel workers
    verbose=True,
)
```

---

## Adding New Domains

### Method 1: Hardcoded (in run_discovery.py)
```python
TOPIC_KNOWLEDGE["my-domain"] = {
    "description": "My domain description",
    "constants": [
        {"name": "Constant A", "value": 1.234, "uncertainty": 0.01, "source": "Paper"},
        # ...
    ]
}
```

### Method 2: JSON (in BriareusFlow/domains/)
```json
{
  "name": "my-domain",
  "description": "My domain description",
  "keywords": ["keyword1", "keyword2"],
  "constants": [
    {"name": "Constant A", "value": 1.234, "uncertainty": 0.01, "source": "Paper"}
  ],
  "sources": ["https://source.url"]
}
```

### Method 3: Dynamic Research
```bash
python run_discovery.py "my new topic" --research
```

---

*Z² = 32π/3 ≈ 33.510322 — The compactification constant*
