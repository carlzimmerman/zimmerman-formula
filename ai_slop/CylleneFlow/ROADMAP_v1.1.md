# CylleneFlow v1.1 Roadmap

**Based on:** Venice + El Niño iteration experiments (May 4, 2026)
**Status:** Planning phase

---

## Lessons Learned from v1.0.0

### What Works Well

| Component | Status | Notes |
|-----------|--------|-------|
| Truth Store | ✅ Solid | Correctly stores and deduplicates findings |
| Training Generator | ✅ Solid | Generates 5 Q&A pairs per truth |
| Model Updater | ✅ Solid | Quick iteration via system prompt works |
| Iteration Runner | ✅ Solid | Diminishing returns detection works |
| Location Detection | ✅ Solid | (v1.5.1) Correctly identifies geographic context |

### What Needs Work

| Component | Issue | Priority |
|-----------|-------|----------|
| HermesFlow Data Acquisition | Can't find CSVs on modern portals | **CRITICAL** |
| Format Handling | Only handles simple CSVs | HIGH |
| API Integration | No JSON/API parsing | HIGH |
| HTML Table Extraction | No embedded table parsing | MEDIUM |
| Adaptive Search | Same queries each iteration | MEDIUM |

---

## v1.1 Feature Plan

### Phase 1: Data Acquisition Overhaul

#### 1.1 Multi-Format Parser

```python
class DataParser:
    """Parse data from multiple formats."""

    def parse(self, content: bytes, content_type: str) -> Optional[pd.DataFrame]:
        if content_type == 'text/csv':
            return self._parse_csv(content)
        elif content_type == 'application/json':
            return self._parse_json(content)
        elif content_type == 'text/html':
            return self._parse_html_tables(content)
        elif 'netcdf' in content_type:
            return self._parse_netcdf(content)
        elif self._looks_like_ascii_table(content):
            return self._parse_ascii_table(content)
        return None
```

#### 1.2 API Endpoint Detection

```python
def detect_api_endpoints(html: str, base_url: str) -> List[str]:
    """Find API endpoints mentioned in page."""
    patterns = [
        r'api\.[\w]+\.[\w]+/[\w/]+',
        r'/api/v\d+/[\w/]+',
        r'data\.json',
        r'\.csv\?',  # Parameterized CSV endpoints
    ]
    # Also look for JavaScript data URLs
    ...
```

#### 1.3 ASCII Table Parser

Many NOAA datasets are ASCII tables with fixed-width columns:
```
Year  Month  Value
2024  01     0.45
2024  02     0.67
```

Add parser to handle these:
```python
def parse_ascii_table(content: str) -> pd.DataFrame:
    """Parse fixed-width ASCII table."""
    lines = content.strip().split('\n')
    header = detect_header(lines[0])
    widths = detect_column_widths(lines)
    return pd.read_fwf(io.StringIO(content), widths=widths, names=header)
```

### Phase 2: Portal Navigation Improvements

#### 2.1 Deeper Navigation

Currently: 2 levels deep
Target: 4 levels deep for known data portals

```python
DEEP_NAVIGATION_DOMAINS = [
    'noaa.gov',
    'nasa.gov',
    'usgs.gov',
    'ncei.noaa.gov',
]

def should_navigate_deeper(url: str, current_depth: int) -> bool:
    domain = urlparse(url).netloc
    if any(d in domain for d in DEEP_NAVIGATION_DOMAINS):
        return current_depth < 4
    return current_depth < 2
```

#### 2.2 Known Data Source Registry

For commonly-requested datasets, include direct paths:

```python
KNOWN_DATA_SOURCES = {
    "ENSO": {
        "ONI": "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt",
        "SOI": "https://www.cpc.ncep.noaa.gov/data/indices/soi",
        "MEI": "https://psl.noaa.gov/enso/mei/data/meiv2.data",
    },
    "glaciers": {
        "GLAMOS": "https://glamos.ch/download/...",
        "WGMS": "https://wgms.ch/data/...",
    },
    "venice": {
        "Centro_Maree": "https://www.comune.venezia.it/archivio/marea/...",
    },
}
```

### Phase 3: Adaptive Iteration

#### 3.1 Search Strategy Evolution

When iteration N finds 0 results, iteration N+1 should try different approaches:

```python
def get_search_strategy(iteration: int, previous_success: bool) -> SearchStrategy:
    if iteration == 1 or previous_success:
        return SearchStrategy.STANDARD
    elif iteration == 2:
        return SearchStrategy.API_FOCUSED
    elif iteration == 3:
        return SearchStrategy.KNOWN_SOURCES
    else:
        return SearchStrategy.BROADER_TERMS
```

#### 3.2 Portal Memory

Remember which portals had promising links but no data:

```python
class PortalMemory:
    """Track portal exploration across iterations."""

    promising_but_empty: List[str]  # Had data links but no downloads
    dead_ends: List[str]            # No data links at all
    needs_registration: List[str]   # Requires auth

    def suggest_alternatives(self) -> List[str]:
        """Suggest new portals based on failure patterns."""
```

---

## Testing Plan for v1.1

### Test Cases

| Topic | Geographic | Expected Result |
|-------|------------|-----------------|
| Swiss glacier melt | Switzerland | ✅ Should find GLAMOS |
| El Niño indices | Global | Should find NOAA ASCII tables |
| Venice water levels | Italy | Should find Centro Maree |
| US hurricane tracks | USA | Should find HURDAT2 |
| UK river flow | UK | Should find NRFA |

### Success Criteria

1. **Format handling:** Parse at least 3 formats (CSV, ASCII, JSON)
2. **Data acquisition:** Download data from 4/5 test topics
3. **Iteration value:** At least one topic shows improvement over iterations

---

## Architecture Unchanged

The core CylleneFlow loop remains the same:

```
┌─────────────────────────────────────────────────────────┐
│                    CYLLENEFLOW v1.1                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  TRUTH      │    │  TRAINING   │    │   MODEL     │ │
│  │  STORE      │───▶│  GENERATOR  │───▶│   UPDATER   │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│        ▲                                     │         │
│        │                                     │         │
│        │         ┌───────────────┐           │         │
│        └─────────│   ITERATION   │◀──────────┘         │
│                  │   RUNNER      │                     │
│                  └───────┬───────┘                     │
│                          │                             │
│                          ▼                             │
│  ┌─────────────────────────────────────────────────┐  │
│  │              HERMESFLOW v1.6.0                  │  │
│  │  (Enhanced data acquisition + format handling)  │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

The investment is in **HermesFlow's capabilities**, not the iteration architecture.

---

## Timeline (Not Estimates)

1. **Multi-format parser** - First priority
2. **ASCII table handling** - Second priority
3. **Known sources registry** - Third priority
4. **Adaptive search** - Fourth priority
5. **Full test suite** - Final validation

---

*Roadmap created: May 4, 2026*
*Based on Venice + El Niño experiment analysis*
