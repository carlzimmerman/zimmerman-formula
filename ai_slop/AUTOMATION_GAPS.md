# BriareusFlow Automation Gap Analysis

## Date: May 6, 2026

---

## Current Pipeline Architecture

```
User Query → [MANUAL: Claude researches] → Domain Definition
     ↓
run_full_discovery.py
     ↓
┌─────────────────────────────────────────────────────┐
│                   BriareusFlow                       │
│  ┌─────────────┐  ┌───────────────┐  ┌───────────┐ │
│  │ Pattern     │→ │ Geometric     │→ │ Olympus   │ │
│  │ Search      │  │ Interpreter   │  │ Bridge    │ │
│  └─────────────┘  └───────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────────────────┐
│                   OlympusFlow                        │
│  ┌─────────────┐  ┌───────────────┐  ┌───────────┐ │
│  │ SymPy       │→ │ HRM           │→ │ Learning  │ │
│  │ Verifier    │  │ Scoring       │  │ Loop      │ │
│  └─────────────┘  └───────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────┘
     ↓
[MANUAL: Claude interprets] → Results Summary
```

---

## Identified Automation Gaps

### GAP 1: Domain Research (HIGH PRIORITY)

**Current State:**
- User asks about a topic (e.g., "monarch butterfly navigation")
- Claude manually searches the web
- Claude reads papers and extracts numerical constants
- Claude decides which ratios to compute

**Where Claude Helps:**
- Web search query formulation
- Reading scientific text
- Extracting numerical values from prose
- Computing meaningful dimensionless ratios

**Proposed Solution: ResearchAgent**

```python
class ResearchAgent:
    """Autonomous research agent for domain discovery."""

    def research_topic(self, topic: str) -> DomainDefinition:
        """
        1. Generate search queries for topic
        2. Fetch scientific papers/data
        3. Extract numerical constants using NLP
        4. Compute all reasonable dimensionless ratios
        5. Build domain definition
        """

    def extract_constants(self, text: str) -> List[ExtractedConstant]:
        """Use regex + NLP to find values like '420 nm', '215 degrees'"""

    def generate_ratios(self, constants: List[ExtractedConstant]) -> List[Ratio]:
        """Generate all meaningful dimensionless combinations"""
```

**Implementation Options:**
1. **Offline NLP**: Use spaCy + custom entity recognition for physics values
2. **LLM-assisted**: Use Claude API for complex extraction (but expensive)
3. **Hybrid**: Simple regex for common patterns, LLM for ambiguous cases

---

### GAP 2: Dynamic Domain Creation (MEDIUM PRIORITY)

**Current State:**
- Domains are hardcoded in `run_full_discovery.py`
- Adding a new domain requires editing Python code
- Claude manually writes the domain dictionary

**Where Claude Helps:**
- Writing the Python dictionary structure
- Formatting values with correct keys
- Adding to `find_topic()` function

**Proposed Solution: Domain Registry**

```python
# Instead of hardcoded TOPIC_KNOWLEDGE, use:

class DomainRegistry:
    """Dynamic domain management."""

    def __init__(self, domains_dir: Path):
        self.domains_dir = domains_dir
        self.domains = {}
        self._load_all()

    def _load_all(self):
        """Load all .json domain files from domains_dir"""
        for f in self.domains_dir.glob("*.json"):
            domain = json.load(f.open())
            self.domains[domain["name"]] = domain

    def add_domain(self, domain: DomainDefinition) -> None:
        """Programmatically add a new domain"""
        path = self.domains_dir / f"{domain.name}.json"
        json.dump(domain.to_dict(), path.open("w"))
        self.domains[domain.name] = domain

    def search_topics(self, query: str) -> Optional[str]:
        """Fuzzy match query to domain names/keywords"""
```

**Benefits:**
- No code changes needed to add domains
- ResearchAgent can create domains directly
- Version control friendly (one file per domain)

---

### GAP 3: Result Interpretation & Cross-Domain Synthesis (MEDIUM PRIORITY)

**Current State:**
- BriareusFlow finds patterns
- Claude manually identifies "interesting" findings
- Claude notices cross-domain connections (e.g., 25/Z² in both Kleiber and Kolmogorov)

**Where Claude Helps:**
- Ranking findings by significance
- Identifying unexpected connections
- Writing natural language summaries

**Proposed Solution: PatternSynthesizer**

```python
class PatternSynthesizer:
    """Cross-domain pattern analysis."""

    def __init__(self, results_db: ResultsDatabase):
        self.db = results_db

    def find_cross_domain_patterns(self) -> List[CrossDomainPattern]:
        """
        Find patterns that appear in multiple domains.
        e.g., 25/Z² appearing in Kleiber, Kolmogorov, blood vessels
        """
        # Group all findings by formula
        by_formula = defaultdict(list)
        for result in self.db.all_results():
            normalized = self.normalize_formula(result.formula)
            by_formula[normalized].append(result)

        # Find formulas appearing in 2+ domains
        cross_domain = []
        for formula, results in by_formula.items():
            domains = set(r.domain for r in results)
            if len(domains) >= 2:
                cross_domain.append(CrossDomainPattern(
                    formula=formula,
                    domains=list(domains),
                    results=results
                ))

        return cross_domain

    def generate_report(self, findings: List[Finding]) -> str:
        """Generate markdown report from findings"""
```

**Benefits:**
- Automatic detection of universal patterns
- No manual cross-referencing needed
- Builds evidence for fundamental geometric principles

---

### GAP 4: Constant Value Verification (LOW PRIORITY)

**Current State:**
- Constants are entered with assumed values
- No automatic verification against authoritative sources

**Where Claude Helps:**
- Looking up CODATA values
- Cross-checking multiple sources
- Flagging inconsistencies

**Proposed Solution: ConstantVerifier**

```python
class ConstantVerifier:
    """Verify constants against authoritative sources."""

    SOURCES = {
        "CODATA": "https://physics.nist.gov/cuu/Constants/",
        "PDG": "https://pdg.lbl.gov/",
        "NASA": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/",
    }

    def verify(self, name: str, value: float, uncertainty: float) -> VerificationResult:
        """Check if constant matches known values"""
```

---

## Implementation Priority

| Gap | Priority | Effort | Impact |
|-----|----------|--------|--------|
| ResearchAgent | HIGH | High | Enables fully autonomous discovery |
| Domain Registry | MEDIUM | Low | Removes code dependency |
| PatternSynthesizer | MEDIUM | Medium | Finds hidden connections |
| ConstantVerifier | LOW | Medium | Improves accuracy |

---

## Recommended First Step

**Create JSON-based Domain Registry** because:
1. Low effort (1-2 hours)
2. Immediate benefit (no code changes for new domains)
3. Enables ResearchAgent to create domains programmatically

```bash
BriareusFlow/
  domains/
    eddington.json
    roche.json
    titius-bode.json
    geodynamo.json
    ...
    monarch-butterfly.json  # New domains just need JSON files
```

---

## Fully Autonomous Pipeline Vision

```
User: "Research X"
       ↓
┌─────────────────────────────────────────────────────┐
│              ResearchAgent (NEW)                     │
│  • Web search for scientific data                   │
│  • NLP extraction of constants                      │
│  • Dimensionless ratio generation                   │
│  • Domain definition creation                       │
└─────────────────────────────────────────────────────┘
       ↓ (JSON domain file)
┌─────────────────────────────────────────────────────┐
│              DomainRegistry (NEW)                    │
│  • Load domain from JSON                            │
│  • Fuzzy topic matching                             │
└─────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────┐
│              BriareusFlow (EXISTS)                   │
│  • Pattern search                                   │
│  • Geometric interpretation                         │
└─────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────┐
│              OlympusFlow (EXISTS)                    │
│  • SymPy verification                               │
│  • HRM scoring                                      │
│  • Learning loop                                    │
└─────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────┐
│              PatternSynthesizer (NEW)                │
│  • Cross-domain pattern detection                   │
│  • Universal constant identification                │
│  • Report generation                                │
└─────────────────────────────────────────────────────┘
       ↓
Autonomous Discovery Report
```

---

## Current Z² Pattern Database (for cross-domain analysis)

| Pattern | Value | Domains Found |
|---------|-------|---------------|
| 25/Z² | 0.746 | Kleiber, Kolmogorov, Blood vessels |
| 20/Z² | 0.597 | Monarch migration, V_p jump |
| 5/Z² | 0.149 | Zipf density, Urban sublinear |
| 1 + 5/Z² | 1.149 | Zipf GDP |
| 1 - 5/Z² | 0.851 | Zipf infrastructure |
| Z² - 2 | 31.51 | Earthquake energy (10^1.5) |
| 4Z² + 3 | 137.04 | Fine structure constant |
| 2Z² - 27 | 40.02 | Critical Reynolds Rm |

---

*Document generated during monarch butterfly analysis session*
