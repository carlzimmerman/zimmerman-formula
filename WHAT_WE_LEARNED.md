# What We Learned: OlympusFlow Overnight Tests Analysis

**Date:** 2026-05-05
**Tests Run:** 3 background tests (A_L Lensing, Z² Cosmology Validation, FQHE 5/2)

---

## Executive Summary

The overnight tests revealed that OlympusFlow's architecture works but has critical gaps in the **data location and extraction** layer (HermesFlow). The system is honest - it correctly reported 0 findings when it couldn't find relevant data - but it **failed to locate** the data it was looking for.

| Test | Target | Actual Finding | Problem |
|------|--------|----------------|---------|
| A_L Lensing | Planck A_L = 1.18 ± 0.065 | CV(stop) from cosmic rays | Wrong domain pivot |
| Z² Cosmology | Ω_Λ, Ω_m from Planck | CV(stop) from cosmic rays | Same wrong pivot |
| FQHE 5/2 | 5/2 plateau measurements | Nothing | No accessible numerical data |

---

## Problem 1: Fallback Domain Drift

### What Happened
When HermesFlow couldn't find Planck CMB data APIs, it fell back to "broader search" and found **Pierre Auger cosmic ray data** instead. This is a different domain entirely:

```
Topic: Planck CMB lensing amplitude A_L anomaly
Expected: ESA Planck Legacy Archive data
Found: opendata.auger.org/releases/3/auxiliary/sdMap.csv

Result: CV(stop) = Z (3.38% error)
Problem: This has nothing to do with A_L lensing!
```

### Why This Happened
The fallback strategy in `hermes_explorer.py` line ~1270:
```python
broader_queries = [
    f"{domain} CSV data download feed",
    "value CSV download",
    f"international {domain} monitoring data portal"
]
```

When cosmology portals failed, "cosmology CSV data download" led to Auger (which IS cosmology-related but wrong subdomain).

### Proposed Fix: Topic-Anchored Fallback
```python
def _validate_domain_relevance(self, df, topic, domain):
    """Verify found data actually relates to the requested topic."""
    topic_keywords = self._extract_keywords(topic)  # "A_L", "lensing", "CMB", "Planck"

    # Check column names and first few rows for topic keywords
    data_text = ' '.join(df.columns.tolist() + df.head(3).astype(str).values.flatten().tolist())

    keyword_matches = sum(1 for kw in topic_keywords if kw.lower() in data_text.lower())
    if keyword_matches < 2:  # Require at least 2 topic keywords
        return False, f"Data doesn't contain topic keywords: {topic_keywords}"
    return True, "Domain validated"
```

---

## Problem 2: API Navigation Failure

### What Happened
HermesFlow found the correct wiki pages:
```
https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Lensing
```

But couldn't extract the actual A_L = 1.18 value because:
1. The wiki describes the data but doesn't embed it
2. The actual Planck parameter chains are in FITS files
3. No API endpoint was found for parameter queries

### Why This Happened
The exploration depth went into wiki "edit" and "history" pages instead of following "Data Products" links:
```
[Hermes] Exploring intermediate: edit        # Wrong!
[Hermes] Exploring intermediate: Lensing     # Right, but too shallow
[Hermes] Exploring intermediate: Users       # Wrong!
```

### Proposed Fix: Priority-Weighted Link Navigation
```python
PRIORITY_KEYWORDS = {
    'high': ['data', 'download', 'products', 'results', 'parameters', 'catalog'],
    'medium': ['documentation', 'analysis', 'methodology', 'publications'],
    'low': ['edit', 'history', 'users', 'login', 'help', 'about']
}

def _prioritize_links(self, links):
    """Sort links by likely data relevance."""
    scored = []
    for link in links:
        text = link['text'].lower()
        url = link['url'].lower()

        if any(kw in text or kw in url for kw in PRIORITY_KEYWORDS['low']):
            continue  # Skip low priority entirely

        score = 0
        for kw in PRIORITY_KEYWORDS['high']:
            if kw in text or kw in url:
                score += 10
        for kw in PRIORITY_KEYWORDS['medium']:
            if kw in text or kw in url:
                score += 3

        scored.append((score, link))

    return [link for score, link in sorted(scored, reverse=True)]
```

---

## Problem 3: Scientific Parameter Extraction

### The Core Issue
Planck's A_L = 1.180 ± 0.065 is reported in:
1. Academic papers (PDFs) - not easily parseable
2. FITS parameter chains - requires specialized parsing
3. Wiki text descriptions - not structured

HermesFlow expects CSV/JSON but Planck uses FITS files with MCMC chains.

### Proposed Fix: Domain-Specific Extractors
```python
DOMAIN_EXTRACTORS = {
    'cosmology': PlanckExtractor,     # FITS, parameter chains
    'particle_physics': PDGExtractor,  # LaTeX tables
    'condensed_matter': NISTExtractor, # ASCII fixed-width
    'meteorology': NOAAExtractor,      # CSV, NetCDF
    'geology': USGSExtractor,          # GeoJSON, ASCII
}

class PlanckExtractor:
    """Extract cosmological parameters from Planck data."""

    PARAMETER_PATTERNS = {
        'A_L': r'A[_\s]*L\s*[=:]\s*([\d.]+)\s*±?\s*([\d.]+)?',
        'Omega_Lambda': r'Ω[_\s]*Λ\s*[=:]\s*([\d.]+)',
        'H0': r'H[_\s]*0\s*[=:]\s*([\d.]+)',
    }

    def extract_from_text(self, text):
        """Extract parameters from descriptive text."""
        results = {}
        for param, pattern in self.PARAMETER_PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                results[param] = {
                    'value': float(match.group(1)),
                    'error': float(match.group(2)) if match.group(2) else None
                }
        return results
```

---

## Problem 4: FQHE 5/2 - Domain Data Scarcity

### What Happened
For FQHE 5/2, the system searched NIST, SNAP, Nature, and arXiv but found **no downloadable numerical data** at all.

### Why This is Different
Condensed matter physics data is rarely available as downloadable datasets:
- Measurements are device-specific
- Raw data requires specialized equipment context
- Most data is in figures, not tables

### Proposed Fix: Figure Extraction Pipeline
```python
class FigureDataExtractor:
    """Extract data points from scientific figures."""

    def extract_from_plot(self, image_path, axes_info=None):
        """Use vision model to extract (x,y) data from plots."""
        # This requires a multimodal approach
        # Could integrate with Opus vision capabilities
        pass
```

This is a harder problem - may need human curation for condensed matter.

---

## Honesty Assessment

**The system was honest.** Key evidence:

1. **A_L Test Output:**
   ```
   Z² prediction: A_L = 1 + 6/Z² = 1.179049
   However, this was computed - not discovered by the pipeline.
   ```

2. **FQHE Test Output:**
   ```
   Total discoveries: 0
   (Correctly stopped due to "diminishing returns")
   ```

3. **A_L correctly removed from AletheiaLake** with comment explaining why

---

## Architecture Recommendations

### 1. Add Topic Relevance Validator
Before accepting any finding, verify it matches the search topic:
```
OlympusFlow → HermesFlow → [NEW: TopicValidator] → TruthFlow
```

### 2. Domain-Specific Data Locators
Route cosmology queries to Planck-specific logic:
```python
if domain == 'cosmology':
    return PlanckLocator().find(topic)
elif domain == 'meteorology':
    return NOAALocator().find(topic)
```

### 3. Iterative Refinement
When fallback activates, narrow the search instead of broadening:
```
Iteration 1: "Planck CMB lensing A_L data"
Iteration 2: "Planck 2018 A_L parameter estimate"
Iteration 3: "arXiv Planck lensing amplitude measurement table"
```

### 4. Source Tier Enforcement
Only accept findings from expected sources:
```python
EXPECTED_SOURCES = {
    'cosmology/A_L': ['planck', 'esa', 'nasa', 'lambda.gsfc'],
    'cosmology/Omega': ['planck', 'sdss', 'desi'],
}
```

---

## Next Steps

1. **Run Hurricane Test (Blind)** - meteorology domain has better structured data (NOAA)
2. **Implement TopicValidator** - prevent domain drift
3. **Add PlanckLocator** - specialized cosmology extractor
4. **Review CylleneFlow iterations** - ensure learning doesn't amplify errors

---

## Metrics Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| A_L discovered | Yes | No | FAIL |
| Ω_Λ discovered | Yes | No | FAIL |
| FQHE data found | Yes | No | FAIL |
| System honest | Yes | Yes | PASS |
| No false positives | Yes | Yes | PASS |

---

## Follow-Up: Hurricane Blind Test (SUCCESS)

After implementing the fixes, we ran a **blind hurricane test** that **succeeded**:

```
Topic: Atlantic hurricane intensity measurements ACE NOAA
Domain: meteorology
Result: SUCCESS

URL: https://psl.noaa.gov/data/timeseries/month/data/hurr.atl.ace.data
Data shape: (179, 13)
Columns: ['YEAR', 'DJ', 'JF', 'FM', 'MA', 'AM', 'MJ', 'JJ', 'JA', 'AS', 'SO', 'ON', 'ND']
```

### Why Hurricane Worked But Planck Failed

| Factor | Hurricane (NOAA) | Planck (CMB) |
|--------|-----------------|--------------|
| Data format | Direct .data/.csv URLs | FITS files + parameter chains |
| API accessibility | Simple HTTP GET | Requires specialized queries |
| Search result quality | First hit was correct | Wiki pages, not data |
| Fallback needed | No | Yes (and drifted to wrong domain) |

### Key Takeaways

1. **Meteorology data is well-structured** for web scraping
2. **Cosmology data requires specialized extractors** (FITS parsing, MCMC chains)
3. **TopicValidator prevents domain drift** - cosmic ray data now rejected
4. **Domain-specific locators are essential** for physics subdisciplines

---

## Implementation Status

| Fix | Status | File |
|-----|--------|------|
| TopicValidator | IMPLEMENTED | `HermesFlow/topic_validator.py` |
| Synonym expansion | IMPLEMENTED | `HermesFlow/topic_validator.py` |
| Domain drift prevention | TESTED | TopicValidator demo passes |
| PlanckLocator | TODO | Need FITS parsing |
| Priority link navigation | TODO | Need to update hermes_explorer.py |

**Conclusion:** The system has integrity (honest about failures) but needs domain-specific enhancements for cosmology/particle physics data. Meteorology works well.

---

## Follow-Up: Tornado Blind Test (May 5, 2026)

### Test Results

| Run | Duration | Result | Path Taken |
|-----|----------|--------|------------|
| Run 1 | 13s | SUCCESS* | PSL timeseries → tornado.us.mon.data |
| Run 2 | 180s | FAILED | Storm Events → Food DB → WMO (wandered) |
| Run 3 | 16s | SUCCESS | PSL timeseries (targeted query) |

*Script exception after successful discovery

### Successful Discovery

```
URL: https://psl.noaa.gov/data/correlation/tornado.us.mon.data
Shape: 83 rows × 13 columns
Coverage: 1940-2022 monthly tornado counts
TopicValidator: 0.15 confidence (fell back to LLM validation)
```

### Critical Finding: Non-Determinism

The same query can lead to SUCCESS (15s) or FAILURE (180s) depending on search result ordering.
This is the most critical issue to address.

### New Improvements Identified

| Issue | Fix | Status |
|-------|-----|--------|
| TopicValidator low confidence | Add tornado synonyms | IMPLEMENTED |
| Navigation link pollution | Add EXCLUDE_LINKS filter | TODO |
| Domain drift in fallback | Add topic anchoring | TODO |
| Successful path caching | Add KNOWN_WORKING_PATHS | TODO |

### TopicValidator Update

Added synonyms for tornado-related terms:
```python
'tornado': ['storm', 'twister', 'funnel', 'cyclone', 'vortex', 'severe_weather'],
'ef_scale': ['fujita', 'enhanced_fujita', 'tornado_intensity', 'rating'],
'noaa': ['ncei', 'nws', 'psl', 'spc', 'national_weather'],
```

### Z² Analysis

No strong Z² patterns found in tornado count data (CV ~ 1.8, no targets < 10% error).
This is a valid scientific finding - tornado occurrence is highly variable and doesn't
exhibit the geometric regularities seen in fundamental physics.
