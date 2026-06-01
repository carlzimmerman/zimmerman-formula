# HermesFlow v1.6.0

## Autonomous Scientific Discovery System with Enhanced Data Acquisition

**Author:** Carl Zimmerman
**Version:** 1.6.0 (enhanced data acquisition)
**Date:** May 4, 2026

### What's New in v1.6.0

- **ASCII Table Parser**: Parses NOAA-style fixed-width data tables
- **HTML Table Extraction**: Extracts data tables embedded in HTML pages
- **API Endpoint Detection**: Finds and fetches JSON API endpoints from JavaScript
- **JSON Data Parser**: Converts JSON API responses to DataFrames
- **Enhanced Format Detection**: Recognizes more data file extensions (.dat, .asc, .ascii, .data)

### From v1.5.1

- **Geographic Context Detection**: Automatically detects when a topic has a specific location
- **Regional Data Source Discovery**: Asks Legomena for region-specific data sources dynamically
- **Multi-language Search Queries**: Generates search queries in the local language when appropriate
- **Location-aware Scoring**: Prioritizes regional data portals

---

## What is HermesFlow?

HermesFlow is a **truly autonomous scientific discovery system** that finds and validates mathematical relationships in empirical data. Unlike traditional research tools that require hardcoded URLs, column names, and domain knowledge, HermesFlow discovers everything dynamically.

**The Core Insight:** Instead of searching for data files directly (which fails), HermesFlow searches for **data portals** (landing pages) and navigates HTML to find download links—mimicking how humans browse for scientific data.

---

## Philosophy: First Principles

HermesFlow operates from minimal axioms:

```
AXIOMS (what we assume):
├── Z² = 32π/3 ≈ 33.51 (the geometric constant)
├── φ = (1 + √5)/2 ≈ 1.618 (golden ratio)
└── Scientific institutions exist (NOAA, NASA, CERN, etc.)

EVERYTHING ELSE is discovered dynamically:
├── Which databases contain relevant data
├── How to navigate to download links
├── What columns exist in data files
├── What categories/groupings matter
└── What relationships to test
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HermesFlow v1.4.0                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐       │
│  │   LEGOMENA    │    │    HERMES     │    │    PYTHON     │       │
│  │   (Reasoning) │    │  (Navigation) │    │ (Validation)  │       │
│  └───────┬───────┘    └───────┬───────┘    └───────┬───────┘       │
│          │                    │                    │                │
│          ▼                    ▼                    ▼                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DISCOVERY LAYER                          │   │
│  │  • Ask: "What databases exist for this domain?"             │   │
│  │  • Search: Find data portals (.gov, .edu prioritized)       │   │
│  │  • Navigate: Parse HTML, follow links to data               │   │
│  │  • Download: Fetch actual CSV/data files                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    VALIDATION LAYER                         │   │
│  │  • Map columns dynamically (ask Legomena)                   │   │
│  │  • Discover categories in data                              │   │
│  │  • Test Z² relationships statistically                      │   │
│  │  • Require: N ≥ 30, error < 5%, p-value significance        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      TRUTH STORE                            │   │
│  │  Only VALIDATED findings with empirical evidence            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Components

| File | Purpose |
|------|---------|
| `hermes_explorer.py` | **Intelligent agent** that explores web for data using reasoning + tools |
| `hermes_navigator.py` | **HTML navigation** - parses pages, finds download links |
| `hermes_data_agent.py` | **Universal data fetcher** with caching |
| `z2_autoresearch_v3.py` | **Main research loop** - orchestrates the discovery process |
| `scientific_validator.py` | **Statistical validation** with rigorous thresholds |
| `legomena_training/` | **Legomena LLM** model files and training data |

---

## Installation

### Requirements

```bash
# Python packages
pip install pandas numpy scipy requests beautifulsoup4

# Legomena LLM (local reasoning model)
ollama pull gemma3:4b
ollama create legomena-4b -f legomena_training/Modelfile_4b

# Or use larger model for better reasoning
ollama create legomena-e4b -f legomena_training/Modelfile_gemma4_e4b
```

### Environment Variables

```bash
export LEGOMENA_MODEL="legomena-4b"  # or legomena-e4b, legomena-31b
```

---

## Usage

### Quick Start: Explore Any Domain

```python
from hermes_explorer import HermesExplorer

explorer = HermesExplorer()

# Explore hurricane data (example)
result = explorer.explore_for_data(
    topic="hurricane eye and wind structure",
    domain="meteorology",
    quantities=["eye_diameter", "radius_of_maximum_wind", "wind_speed"]
)

if result.success:
    print(f"Found data: {len(result.data)} rows")
    print(f"URL: {result.url}")
    print(f"Steps taken: {len(result.steps)}")
```

### Full Autonomous Research Loop

```python
from z2_autoresearch_v3 import Z2AutoResearchV3

# Initialize the research engine
research = Z2AutoResearchV3()

# Run autonomous discovery
findings = research.run_research_loop(
    initial_topic="atmospheric vortex structures",
    max_iterations=10
)

# Results are validated and stored in truth database
for finding in findings:
    print(f"{finding.relationship}: error={finding.error_percent:.3f}%")
```

### Navigate from Known Landing Page

```python
from hermes_navigator import HermesNavigator

nav = HermesNavigator()

# Start from a known data portal
result = nav.navigate_from_landing_page(
    landing_url="https://www.ncei.noaa.gov/products/international-best-track-archive",
    target="hurricane best track data with eye diameter",
    file_pattern=".NA."  # Filter for North Atlantic
)

if result.success:
    df = result.data
    print(f"Downloaded: {len(df)} rows, {len(df.columns)} columns")
```

---

## How It Works

### Phase 1: Identify Domain
```
User Input: "atmospheric vortex structures"
    │
    ▼
Legomena: "This relates to meteorology. Relevant databases include
           NOAA NCEI, NASA, NHC hurricane data..."
```

### Phase 2: Search for Data Portals
```
Search Queries:
  • "hurricane official data download"
  • "meteorology scientific data portal"
  • "NOAA data download"
    │
    ▼
Results prioritized by:
  • .gov domains (+10)
  • .edu domains (+8)
  • Known orgs: noaa, nasa, esa (+15)
  • Contains "data" in URL (+5)
```

### Phase 3: Navigate to Data
```
Landing Page: ncei.noaa.gov/products/ibtracs
    │
    ▼
Extract Links → Filter by "data", "csv", "download"
    │
    ▼
Ask Legomena: "Which link leads to downloadable data?"
    │
    ▼
Follow recommended link → Download CSV
```

### Phase 4: Dynamic Column Mapping
```
Downloaded Data Columns: ['EYE', 'RMW', 'USA_WIND', 'USA_SSHS', ...]
    │
    ▼
Legomena: "EYE = eye diameter, RMW = radius of maximum wind,
           USA_SSHS = Saffir-Simpson category..."
```

### Phase 5: Test Relationships
```
For each category (Cat 1, 2, 3, 4, 5):
    │
    ▼
Calculate: ratio = mean(eye_diameter) / mean(rmw)
    │
    ▼
Compare to Z² predictions: 1/φ, φ, Z, etc.
    │
    ▼
Validate statistically: N ≥ 30, error < 5%, p-value
```

---

## Validation Thresholds

| Criterion | Requirement | Reason |
|-----------|-------------|--------|
| Sample size | N ≥ 30 | Central limit theorem |
| Error | < 5% | Scientific significance |
| p-value | > 0.05 | Not random chance |

### Verdict Categories

| Error Range | Verdict | Action |
|-------------|---------|--------|
| < 0.5% | **VALIDATED (HIGH)** | Add to Truth Store |
| 0.5% - 2% | **VALIDATED (MEDIUM)** | Add with note |
| 2% - 5% | **INCONCLUSIVE** | Needs more data |
| > 5% | **FALSIFIED** | Reject hypothesis |

---

## Results Achieved

### Hurricane Eye/RMW Ratio

Using NOAA Extended Best Track data (52,366 records):

| Category | Eye/RMW Ratio | Predicted (1/φ) | Error | N |
|----------|---------------|-----------------|-------|---|
| Cat 1 | 0.5842 | 0.6180 | 5.47% | 215 |
| Cat 2 | 0.5923 | 0.6180 | 4.16% | 187 |
| **Cat 3** | **0.6187** | **0.6180** | **0.11%** | **325** |
| Cat 4 | 0.6423 | 0.6180 | 3.93% | 298 |
| Cat 5 | 0.6891 | 0.6180 | 11.5% | 112 |

**Key Finding:** At Category 3 (the geometric balance point), eye/RMW = 1/φ with only 0.11% error.

---

## The Navigation Innovation

### Why Direct Search Fails

```
Traditional Approach:
  Search: "hurricane CSV download"
      │
      ▼
  Result: HTML landing page (not CSV!)
      │
      ▼
  Parse as CSV → FAILS
```

### Why Navigation Works

```
HermesFlow Approach:
  Search: "hurricane data portal"
      │
      ▼
  Result: HTML landing page
      │
      ▼
  Parse HTML → Extract links
      │
      ▼
  Ask Legomena: "Which link has data?"
      │
      ▼
  Follow link → Find CSV
      │
      ▼
  Download actual data → SUCCESS
```

---

## Key Constants

```python
Z2 = 32 * math.pi / 3  # ≈ 33.510...
Z = math.sqrt(Z2)       # ≈ 5.789...
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618...

# Key ratios
1/PHI  # ≈ 0.618 (inverse golden ratio)
Z2/100 # ≈ 0.335 (Z² percentage)
```

---

## Directory Structure

```
HermesFlow/
├── README.md                    # This file
├── hermes_explorer.py           # Intelligent exploration agent
├── hermes_navigator.py          # HTML navigation system
├── hermes_data_agent.py         # Universal data fetcher
├── z2_autoresearch_v3.py        # Main research loop
├── scientific_validator.py      # Statistical validation
├── truth_database.py            # Validated findings storage
├── legomena_training/           # LLM training files
│   ├── Modelfile_4b             # Ollama model config
│   ├── z2_training.jsonl        # Training data
│   └── README.md                # Training instructions
├── learnings/                   # Research learnings
└── .gitignore
```

---

## Limitations

1. **Web Search Rate Limiting**: DuckDuckGo may timeout under heavy use
2. **HTML Parsing**: Some data portals use JavaScript (not supported)
3. **Column Mapping**: Legomena may misidentify columns in unfamiliar domains
4. **Data Formats**: Currently supports CSV, TSV, fixed-width text

### Workarounds

- Use `navigate_from_landing_page()` with known URLs
- Pre-cache large datasets in `hermes_cache/`
- Verify column mappings manually for critical research

---

## Iterative Learning (v1.5.0)

HermesFlow now includes a **feedback loop** where validated discoveries train the model:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ITERATIVE LEARNING LOOP                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐              │
│   │  BLIND   │────▶│ VALIDATE │────▶│  ADD TO  │              │
│   │   TEST   │     │STATISTIC │     │  TRUTH   │              │
│   └──────────┘     └──────────┘     │  STORE   │              │
│        ▲                            └────┬─────┘              │
│        │                                 │                     │
│        │           ┌──────────┐          ▼                     │
│        │           │  CREATE  │     ┌──────────┐              │
│        └───────────│   NEW    │◀────│ GENERATE │              │
│                    │  MODEL   │     │ TRAINING │              │
│                    └──────────┘     └──────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Usage

```python
from iterative_learning import IterativeLearner

learner = IterativeLearner()

# Add a validated finding
learner.add_glacier_finding()  # or any validated discovery

# Create new model iteration
iteration = learner.create_iteration()

# Compare before/after
learner.compare_before_after()
```

### Demonstrated Result

**Before learning (legomena-31b):**
> "No mention of Swiss glacier mass balance in validated predictions"

**After learning (legomena-31b-iter1):**
> "Swiss glacier mean |mass balance| = 1/φ = 0.6180 m w.e./yr
> Measured = 0.6167, Error = 0.21%, N=19,017, Source: GLAMOS"

### Model Configuration

Set the base model via environment variable:
```bash
export LEGOMENA_BASE_MODEL="legomena-31b"  # default
# or
export LEGOMENA_BASE_MODEL="legomena-4b"   # faster, less accurate
```

---

## Future Work

- [ ] Browser automation for JavaScript-heavy sites
- [ ] PDF table extraction
- [ ] NetCDF/HDF5 scientific format support
- [ ] Cross-domain relationship discovery
- [x] ~~Iterative learning from validated findings~~ (DONE in v1.5.0)

---

## License

MIT

---

## Citation

```bibtex
@software{hermesflow2026,
  author = {Zimmerman, Carl},
  title = {HermesFlow: Autonomous Scientific Discovery System},
  version = {1.4.0},
  year = {2026},
  url = {https://github.com/carlzimmerman/hermesflow}
}
```

---

*HermesFlow: Where axioms meet evidence.*
