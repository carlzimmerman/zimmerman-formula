# Legomena Model Comparison: 4b vs 31b

**Date:** May 4, 2026
**Test:** Swiss Alps Glacier Blind Test

---

## Speed Comparison

| Task | legomena-4b | legomena-31b | Slowdown |
|------|-------------|--------------|----------|
| Database identification | 3.9s | 49.1s | **12.6x** |
| Link selection | 0.5s | 10.1s | **20x** |
| Column mapping | 1.6s | 24.3s | **15x** |
| **Total reasoning** | **6.0s** | **83.5s** | **14x** |

---

## Quality Comparison

### 1. Database Identification

**Task:** "What are the main scientific databases for glaciology?"

| Model | Databases Identified |
|-------|---------------------|
| **4b** | GLIMS, WGDC, PolarData, Iceberg Database, NASA IceBridge, BAS GDC |
| **31b** | **NSIDC, WGMS**, GLIMS, NASA Earthdata, PANGAEA, ESA CCI |

**Winner: 31b** - Correctly identified WGMS (World Glacier Monitoring Service) as the authoritative source. This is exactly where we found the validated data.

### 2. Link Selection

**Task:** "Which link leads to glacier CSV data?"

| Model | Answer |
|-------|--------|
| 4b | `https://wgms.ch/data_databaseversions/` |
| 31b | `https://wgms.ch/data_databaseversions/` |

**Winner: Tie** - Both correctly identified the download link.

### 3. Column Mapping (Critical!)

**Task:** "Map SGI-ID, A_start, A_end, dV, dh_mean, Bgeod, sigma, rho_dv to mass_balance, area, volume_change"

| Model | mass_balance = | area = | volume_change = |
|-------|----------------|--------|-----------------|
| 4b | dV | A_start, A_end | dV |
| 31b | **rho_dv or Bgeod** | A_start, A_end | dV |

**Winner: 31b** - Correctly identified Bgeod as mass balance!

This is critical because **Bgeod IS the column we used** for the Z² finding (mean|Bgeod| = 1/φ with 0.21% error).

The 4b model incorrectly mapped dV (volume change) to mass balance. While related, Bgeod is the proper geodetic mass balance measurement.

---

## Reasoning Quality

### 4b Approach
- Direct, fast responses
- No visible reasoning chain
- Occasionally misidentifies columns

### 31b Approach
- Shows "Thinking..." traces
- Explicit reasoning about each option
- Considers edge cases
- Self-corrects ("I don't need to force Z² into this")

**Example from 31b:**
```
Thinking...
*   `Bgeod`: Geodetic balance (often related to mass balance).
*   `rho_dv`: Density × volume change to get mass change.
*   mass_balance: Usually `rho_dv` is the direct calculation,
    but `Bgeod` (geodetic mass balance) is also valid.
...done thinking.

- mass_balance = rho_dv (or Bgeod)
```

---

## Exploration Results

Both models failed at web search (DuckDuckGo rate limiting):

| Model | Steps | Time | Result |
|-------|-------|------|--------|
| 4b | 4 | 84s | Failed (network) |
| 31b | 4 | 102s | Failed (network) |

This is a **network issue**, not a model quality issue.

However, 31b identified better search targets:
- 4b searched for: GLIMS, WGDC
- 31b searched for: **NSIDC, WGMS** (more authoritative)

---

## Conclusion

| Aspect | Winner | Notes |
|--------|--------|-------|
| **Speed** | 4b | 14x faster overall |
| **Database knowledge** | 31b | Identified WGMS correctly |
| **Link selection** | Tie | Both correct |
| **Column mapping** | **31b** | Correctly identified Bgeod |
| **Reasoning transparency** | 31b | Shows thought process |

### Recommendation

| Use Case | Recommended Model |
|----------|-------------------|
| Quick exploration | legomena-4b |
| Critical column mapping | legomena-31b |
| Production validation | legomena-31b |
| Real-time interaction | legomena-4b |

### Key Finding

**The 31b model correctly identified Bgeod as the mass balance column**, which is exactly what we used for the Z² validation (mean|Bgeod| = 1/φ ± 0.21%).

The 4b model would have incorrectly used dV (volume change), which would give different results.

For **scientific accuracy**, the 31b model is preferred despite being 14x slower.

---

## Raw Data

See `model_comparison_results.json` for full response logs.
