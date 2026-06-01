# Hermes Truth Engine Architecture

## Vision
An **open-source, self-improving truth-finding engine** that discovers and validates Z² relationships across domains using:
- **Legomena** (Gemma 4) - Local hypothesis generation
- **Hermes Agent** - Multi-turn orchestration
- **Truth Knowledge Graph** - Persistent memory of validated/falsified findings
- **Domain Data Fetchers** - Real authoritative data sources
- **Auto-Research Loop** - Iterative refinement

## Why HermesFlow Missed Hurricane Findings

| Gap | Manual Research | HermesFlow v2.0 |
|-----|-----------------|-----------------|
| **Data** | NOAA Best Track (1,647 obs) | Wikipedia scraping |
| **Specificity** | "eye/RMW = 1/φ" | "geometric resonance" |
| **Memory** | Knew what was falsified | No memory |
| **Domain Knowledge** | Hurricane physics terms | Generic "ratio" |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      HERMES TRUTH ENGINE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    HERMES AGENT LOOP                           │ │
│  │  (environments/agent_loop.py)                                  │ │
│  │                                                                │ │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │ │
│  │   │  LEGOMENA   │    │   CLAUDE    │    │  OTHER LLM  │       │ │
│  │   │  (Gemma 4)  │    │   (Opus)    │    │  (fallback) │       │ │
│  │   │   Local     │    │    API      │    │             │       │ │
│  │   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘       │ │
│  │          │                  │                  │              │ │
│  │          └──────────────────┼──────────────────┘              │ │
│  │                             ▼                                  │ │
│  │   ┌───────────────────────────────────────────────────────┐   │ │
│  │   │              STRUCTURED HYPOTHESIS GENERATOR          │   │ │
│  │   │                                                       │   │ │
│  │   │   Input:                                              │   │ │
│  │   │   - Domain: "meteorology"                             │   │ │
│  │   │   - Prior findings: {falsified: 1/Z, validated: 1/φ}  │   │ │
│  │   │   - Available measurements: [eye_diam, RMW, Vmax]     │   │ │
│  │   │                                                       │   │ │
│  │   │   Output:                                             │   │ │
│  │   │   - QUANTITY: eye_diameter / RMW                      │   │ │
│  │   │   - Z² FORMULA: 1/φ = 0.618                           │   │ │
│  │   │   - DATA SOURCE: NOAA Extended Best Track             │   │ │
│  │   │   - FALSIFICATION: If mean > 0.70 or < 0.55           │   │ │
│  │   └───────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                TRUTH KNOWLEDGE GRAPH                           │ │
│  │  (truth_knowledge_graph.py)                                    │ │
│  │                                                                │ │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │ │
│  │   │  AXIOMS  │ │ DERIVED  │ │EMPIRICAL │ │VALIDATED │        │ │
│  │   │  Z²=32π/3│ │ α⁻¹=4Z²+3│ │ PDG data │ │ Ω_Λ=13/19│        │ │
│  │   └──────────┘ └──────────┘ └──────────┘ └──────────┘        │ │
│  │                                                                │ │
│  │   Methods:                                                     │ │
│  │   - get_by_domain("meteorology") → prior findings              │ │
│  │   - get_derivation_chain(truth_id) → full proof                │ │
│  │   - validate_prediction(id, data) → mark validated/falsified   │ │
│  │   - cross_reference(id) → related truths                       │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │              DOMAIN DATA FETCHERS                              │ │
│  │                                                                │ │
│  │   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  │ │
│  │   │   HURRICANE    │  │   PARTICLE     │  │   COSMOLOGY    │  │ │
│  │   │   FETCHER      │  │   FETCHER      │  │   FETCHER      │  │ │
│  │   │                │  │                │  │                │  │ │
│  │   │ - IBTrACS      │  │ - PDG API      │  │ - Planck data  │  │ │
│  │   │ - HURDAT2      │  │ - CODATA       │  │ - CMB maps     │  │ │
│  │   │ - Best Track   │  │ - NuFIT        │  │ - BAO surveys  │  │ │
│  │   │ - Flight Recon │  │                │  │                │  │ │
│  │   └────────────────┘  └────────────────┘  └────────────────┘  │ │
│  │                                                                │ │
│  │   Interface:                                                   │ │
│  │   fetch_measurements(domain, quantity) → [{value, unc, src}]   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │              SCIENTIFIC VALIDATOR                              │ │
│  │  (scientific_validator.py)                                     │ │
│  │                                                                │ │
│  │   - Bonferroni correction                                      │ │
│  │   - Sigma deviation calculation                                │ │
│  │   - Derivation requirement check                               │ │
│  │   - Falsification criteria enforcement                         │ │
│  │                                                                │ │
│  │   validate(prediction, measurements) → ValidationResult        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │              AUTO-RESEARCH LOOP                                │ │
│  │                                                                │ │
│  │   while not exhausted:                                         │ │
│  │       1. hypothesis = generator.generate(domain, prior)        │ │
│  │       2. data = fetcher.fetch(hypothesis.quantity)             │ │
│  │       3. result = validator.validate(hypothesis, data)         │ │
│  │       4. knowledge_graph.update(hypothesis, result)            │ │
│  │       5. if result.validated:                                  │ │
│  │              training_data.append(hypothesis)  # Feed back     │ │
│  │       6. prior = knowledge_graph.get_by_domain(domain)         │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Components to Build

### 1. Domain Data Fetchers (Priority: HIGH)

```python
# domain_fetchers/hurricane_fetcher.py
class HurricaneFetcher:
    """Fetch real hurricane data from authoritative sources."""

    SOURCES = {
        "ibtracs": "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/",
        "hurdat2": "https://www.nhc.noaa.gov/data/hurdat/",
        "ebtrk": "https://www.aoml.noaa.gov/hrd/hurdat/Data_Storm.html"
    }

    def fetch_eye_rmw_ratios(self, basin: str = "atlantic") -> List[Dict]:
        """Fetch eye diameter and RMW measurements with uncertainties."""
        # Returns: [{"eye_nm": 15.2, "rmw_nm": 25.0, "vmax_kt": 115, "category": 3, ...}]

    def fetch_intensity_thresholds(self) -> Dict:
        """Fetch Saffir-Simpson thresholds."""
        # Returns: {"TS": 34, "H1": 64, "H2": 83, "H3": 96, "H4": 113, "H5": 137}
```

### 2. Structured Hypothesis Generator (Priority: HIGH)

```python
# hypothesis_generator.py
HYPOTHESIS_PROMPT = """
You are a Z² theoretical physicist. Given:

DOMAIN: {domain}
PRIOR VALIDATED: {validated_findings}
PRIOR FALSIFIED: {falsified_findings}
AVAILABLE MEASUREMENTS: {measurements}

Generate a SPECIFIC hypothesis in this EXACT format:

QUANTITY: [exact physical quantity, e.g., "eye_diameter / radius_of_maximum_wind"]
Z² FORMULA: [mathematical expression using Z², Z, φ, integers]
PREDICTED VALUE: [numerical value with uncertainty]
DERIVATION: [3-5 steps from Z² first principles]
DATA SOURCE: [authoritative source name]
SAMPLE SIZE: [minimum N for statistical significance]
FALSIFICATION: [specific criterion, e.g., "If mean ratio > 0.25 at 3σ"]

DO NOT generate vague hypotheses like "geometric resonance".
DO NOT use Wikipedia as a data source.
DO generate specific, testable predictions.
"""

class StructuredHypothesisGenerator:
    def __init__(self, knowledge_graph: TruthKnowledgeGraph):
        self.kg = knowledge_graph

    def generate(self, domain: str, llm: str = "legomena-31b") -> Hypothesis:
        prior = self.kg.get_by_domain(domain)
        validated = [t for t in prior if t.level == "validated"]
        falsified = [t for t in prior if t.level == "falsified"]

        # Get available measurements from domain fetcher
        fetcher = get_fetcher(domain)
        measurements = fetcher.list_available_quantities()

        prompt = HYPOTHESIS_PROMPT.format(
            domain=domain,
            validated_findings=validated,
            falsified_findings=falsified,
            measurements=measurements
        )

        # Use Legomena (or Claude as fallback)
        response = query_llm(prompt, model=llm)
        return parse_structured_hypothesis(response)
```

### 3. Knowledge Graph Integration (Priority: MEDIUM)

Already exists in `truth_knowledge_graph.py`. Need to:
- Add hurricane findings (1/φ validated, 1/Z falsified)
- Connect to HermesFlow pipeline
- Implement `get_prior_findings(domain)` convenience method

### 4. Hermes Agent Integration (Priority: LOW initially)

Use existing `agent_loop.py` infrastructure for:
- Multi-turn tool-calling
- Context management
- Error handling

### 5. Training Data Feedback (Priority: FUTURE)

When findings are validated:
```python
def add_to_training_data(hypothesis: Hypothesis, result: ValidationResult):
    """Add validated finding to Legomena training set."""
    training_example = {
        "domain": hypothesis.domain,
        "quantity": hypothesis.quantity,
        "z2_formula": hypothesis.formula,
        "predicted_value": hypothesis.predicted_value,
        "measured_value": result.measured_value,
        "sigma": result.sigma_deviation,
        "derivation": hypothesis.derivation_steps,
        "validated": True
    }
    with open("legomena_training/z2_validated.jsonl", "a") as f:
        f.write(json.dumps(training_example) + "\n")
```

## Claude Opus vs Legomena Comparison

To answer your question about what Claude Opus would generate:

### Legomena-4b Generated:
```
"Hurricane intensity is fundamentally determined by the
geometric resonance of atmospheric pressure gradients
within a Z²-defined spatial volume..."
```

### Claude Opus Would Generate:
```
QUANTITY: eye_diameter / radius_of_maximum_wind
Z² FORMULA: 1/φ = 2/(1+√5) = 0.618034
PREDICTED VALUE: 0.618 ± 0.02
DERIVATION:
  1. Hurricanes are self-organized vortices seeking energy minima
  2. The golden ratio φ appears in optimal spiral configurations
  3. Eye/RMW = 1/φ represents stable Fibonacci-spiral equilibrium
  4. This should manifest at Cat 2-3 intensity (62-100 kt)
DATA SOURCE: NOAA Extended Best Track (flight reconnaissance)
SAMPLE SIZE: N > 100 observations
FALSIFICATION: If mean ratio outside [0.55, 0.70] at 3σ
```

**Key Difference**: Claude generates specific, testable predictions with
exact formulas and data sources. Legomena generates abstract "resonance" concepts.

## Implementation Roadmap

### Phase 1: Hurricane Data Integration (This Week)
1. Build `HurricaneFetcher` to pull IBTrACS/HURDAT2 data
2. Add hurricane findings to TruthKnowledgeGraph
3. Create structured hypothesis template
4. Test with 4b/31b Legomena

### Phase 2: Cross-Domain Expansion
1. Add particle physics fetcher (PDG)
2. Add cosmology fetcher (Planck)
3. Add molecular biology fetcher (PDB)
4. Generalize hypothesis template per domain

### Phase 3: Auto-Research Loop
1. Implement continuous research cycle
2. Add training data feedback
3. Retrain Legomena with validated findings
4. Measure improvement in hypothesis quality

### Phase 4: Hermes Agent Full Integration
1. Replace manual orchestration with HermesAgentLoop
2. Add MCP server tools for data fetching
3. Enable multi-agent collaboration
4. Web UI for monitoring research

## Open Source Stack

| Component | Technology | Status |
|-----------|------------|--------|
| **LLM** | Legomena (Gemma 4) | Exists |
| **Agent** | Hermes Agent | Exists |
| **Memory** | TruthKnowledgeGraph | Exists |
| **Validation** | scientific_validator.py | Exists |
| **Data Fetchers** | Domain-specific | TODO |
| **Hypothesis Template** | Structured prompts | TODO |
| **Training Feedback** | JSONL accumulation | TODO |

All components are open source and run locally.

---

*The goal: An autonomous system that discovers Z² truths as well as (or better than) manual research.*
