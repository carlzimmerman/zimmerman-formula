# HeliconLake

**Lake of Sources** - Data source registry for HermesFlow

## Naming

**Mount Helicon** was the sacred mountain of the **Muses** (goddesses of arts and sciences).
- Home to the springs **Hippocrene** and **Aganippe** - sources of inspiration and knowledge
- The Muses presided over all domains of knowledge
- Perfect for a lake cataloguing **sources** of scientific data

## Purpose

HeliconLake stores validated data source URLs and metadata so HermesFlow can:
1. Query known sources before falling back to web search
2. Track URL health and mark dead links
3. Build institutional memory of where data lives

## Lake Ecosystem

| Lake | Purpose | Contents |
|------|---------|----------|
| **AletheiaLake** | Validated truths | Z² patterns with HRM scores |
| **HeliconLake** | Data source registry | URLs, descriptions, domains |
| **MnemoLake** | Training memory | Strategy learning |

## Files

- `registry.json` - Main source catalogue
- `domain_index.json` - Domain → source ID mappings
- `validation_log.json` - URL validation history

## Registry Entry Schema

```json
{
  "id": "noaa-psl-ace-001",
  "url": "https://psl.noaa.gov/data/timeseries/month/HURRICANE_ACE/",
  "landing_page": true,
  "data_urls": ["...direct download URLs..."],
  "description": "Short description of the data",
  "domains": ["meteorology", "climatology"],
  "topics": ["hurricane", "ACE", "cyclone energy"],
  "quantities": ["ACE_index", "hurricane_count"],
  "format": "ascii_fixed_width | csv | json | api",
  "organization": "NOAA Physical Sciences Laboratory",
  "authority_score": 0.95,
  "last_validated": "2026-05-05T09:15:00Z",
  "validation_status": "active | dead | unknown",
  "discovered_by": "HermesFlow | manual",
  "discovery_method": "web_search | known_api | manual"
}
```

## Usage

```python
from HermesFlow.helicon_lake import HeliconLake

lake = HeliconLake()

# Find sources for a domain/topic
sources = lake.find_sources("meteorology", "hurricane")

# Register a new source
lake.register_source({
    "url": "https://...",
    "domains": ["meteorology"],
    "topics": ["hurricane"]
})

# Mark a dead URL
lake.mark_dead("noaa-psl-ace-001")

# Validate all sources
lake.validate_all()
```

## Version

- v1.0.0 (2026-05-05) - Initial creation
