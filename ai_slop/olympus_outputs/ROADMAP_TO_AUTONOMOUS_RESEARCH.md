# Roadmap to Autonomous Research Engine
## OlympusFlow v2.0 Vision

### Current State: Infrastructure Complete, Science Incomplete

OlympusFlow v1.4.0 has working plumbing but produces false positives. To become a **true autonomous research engine**, we need fundamental improvements in four areas:

---

## Phase 1: Statistical Rigor (Critical)

### 1.1 Monte Carlo Null Distribution

Before claiming a match, test against randomness:

```python
class StatisticalValidator:
    def validate_pattern(self, data, observed_ratio, target):
        # Generate 10,000 bootstrap samples
        null_distribution = []
        for _ in range(10000):
            shuffled = np.random.permutation(data)
            null_ratio = self.compute_ratio(shuffled)
            null_distribution.append(null_ratio)

        # Where does observed fall in null?
        p_value = np.mean(np.abs(null_distribution - target) <=
                          np.abs(observed_ratio - target))

        return p_value < 0.001  # Only accept p < 0.001
```

### 1.2 Multiple Comparison Correction

With N tests, apply Bonferroni or FDR:

```python
def apply_fdr_correction(p_values, alpha=0.05):
    """Benjamini-Hochberg FDR correction."""
    sorted_pvals = np.sort(p_values)
    n = len(p_values)
    thresholds = [(i+1) / n * alpha for i in range(n)]
    significant = sorted_pvals <= thresholds
    return significant
```

### 1.3 Effect Size Requirements

Not just "close to target" but "meaningfully close":

```python
def is_significant_match(observed, target, data_std, n_samples):
    """Require effect size d > 0.5 AND p < 0.001"""
    effect_size = abs(observed - target) / data_std
    standard_error = data_std / np.sqrt(n_samples)
    z_score = abs(observed - target) / standard_error
    p_value = 2 * (1 - stats.norm.cdf(z_score))

    return effect_size < 0.1 and p_value < 0.001
```

---

## Phase 2: Multi-Source Corroboration (Essential)

### 2.1 Cross-Dataset Validation

A real pattern should appear across independent sources:

```python
class CrossValidator:
    def validate_across_sources(self, pattern, sources):
        """Pattern must replicate in ≥3 independent sources."""
        confirmations = []
        for source in sources:
            data = self.fetch_data(source)
            result = self.test_pattern(pattern, data)
            confirmations.append(result)

        # Require majority confirmation
        return sum(confirmations) >= 3 and sum(confirmations) / len(sources) > 0.6
```

### 2.2 Temporal Stability

Pattern should hold across time periods:

```python
def test_temporal_stability(data, pattern, n_splits=5):
    """Pattern must hold in each time segment."""
    time_chunks = np.array_split(data, n_splits)
    results = [test_pattern(chunk, pattern) for chunk in time_chunks]
    return all(results)  # Must hold in ALL periods
```

### 2.3 Subgroup Consistency

Pattern should hold when data is subsetted:

```python
def test_subgroup_consistency(data, pattern, groupby_col):
    """Pattern must hold in major subgroups."""
    groups = data.groupby(groupby_col)
    results = []
    for name, group in groups:
        if len(group) >= 30:  # Minimum sample size
            results.append(test_pattern(group, pattern))
    return np.mean(results) > 0.8  # 80% of subgroups must confirm
```

---

## Phase 3: Physical Reasoning (Differentiator)

### 3.1 Semantic Understanding of Data

HermesFlow should understand what columns mean:

```python
class SemanticAnalyzer:
    def analyze_dataset(self, df, domain, topic):
        """Use Legomena to understand column semantics."""
        column_info = {}
        for col in df.columns:
            prompt = f"""
            Dataset domain: {domain}
            Topic: {topic}
            Column name: {col}
            Sample values: {df[col].head(10).tolist()}

            What physical quantity does this column represent?
            What are its units? Is it a ratio, count, measurement?
            """
            column_info[col] = self.legomena.analyze(prompt)
        return column_info
```

### 3.2 Hypothesis-Driven Analysis

Instead of blind statistics, form specific hypotheses:

```python
class HypothesisEngine:
    def generate_hypotheses(self, domain, quantities):
        """Generate Z²-specific testable hypotheses."""
        hypotheses = []

        if "ratio" in quantities:
            hypotheses.append({
                "claim": f"{quantities['numerator']}/{quantities['denominator']} = Z²",
                "test": lambda df: df[quantities['numerator']] / df[quantities['denominator']],
                "target": Z2,
                "mechanism": "Constraint ratio in self-organizing system"
            })

        if "cycle" in domain:
            hypotheses.append({
                "claim": f"Cycle period ratio = φ",
                "test": lambda df: df['period'].max() / df['period'].mean(),
                "target": PHI,
                "mechanism": "Golden ratio in periodic phenomena"
            })

        return hypotheses
```

### 3.3 Mechanism Plausibility Scoring

Rate physical plausibility of claimed patterns:

```python
class MechanismValidator:
    def score_plausibility(self, pattern, domain):
        """Use Legomena to assess physical plausibility."""
        prompt = f"""
        A pattern was found: {pattern['claim']}
        Domain: {domain}
        Measured value: {pattern['measured']}
        Target constant: {pattern['target']} ({pattern['target_name']})

        Rate the physical plausibility (0-1) that this relationship is:
        1. Not coincidental
        2. Has a physical mechanism
        3. Connects to known physics

        Explain your reasoning.
        """
        return self.legomena.evaluate(prompt)
```

---

## Phase 4: Database API Integration (Immediate Need)

### 4.1 Structured Query Interface

Handle databases that require API queries:

```python
class DatabaseQueryHandler:
    """Query interactive databases via their APIs."""

    KNOWN_APIS = {
        "smithsonian_gvp": {
            "base_url": "https://volcano.si.edu/database/search_eruption_results.cfm",
            "method": "POST",
            "params": {"continent": "all", "vei": "all"},
            "parser": self._parse_gvp_response
        },
        "usgs_earthquake": {
            "base_url": "https://earthquake.usgs.gov/fdsnws/event/1/query",
            "method": "GET",
            "params": {"format": "csv", "minmagnitude": 4},
            "parser": self._parse_csv
        },
        "silso_sunspot": {
            "base_url": "https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.txt",
            "method": "GET",
            "parser": self._parse_silso
        }
    }

    def query_database(self, db_name, **kwargs):
        """Execute structured query against known database."""
        config = self.KNOWN_APIS[db_name]
        params = {**config['params'], **kwargs}

        if config['method'] == 'GET':
            response = requests.get(config['base_url'], params=params)
        else:
            response = requests.post(config['base_url'], data=params)

        return config['parser'](response)
```

### 4.2 API Discovery via Legomena

When encountering new databases, use Legomena to figure out API:

```python
class APIDiscoverer:
    def discover_api(self, url, domain, quantities):
        """Use Legomena to discover how to query a database."""
        page_content = self.fetch_page(url)

        prompt = f"""
        I need to extract {quantities} data from this {domain} database.

        Page URL: {url}
        Page content summary: {page_content[:2000]}

        Identify:
        1. Is there a REST API? What's the endpoint?
        2. Is there a download button? What format?
        3. Is there a form? What are the field names?
        4. What parameters do I need to pass?

        Return structured JSON with query instructions.
        """
        return self.legomena.analyze(prompt)
```

---

## Phase 5: Output Quality (Publishable Results)

### 5.1 LaTeX Report Generation

```python
class ReportGenerator:
    def generate_paper(self, findings, domain):
        """Generate publication-ready LaTeX report."""
        sections = [
            self._write_abstract(findings),
            self._write_introduction(domain),
            self._write_methods(),
            self._write_results(findings),
            self._write_discussion(findings),
            self._write_conclusion()
        ]
        return self._compile_latex(sections)
```

### 5.2 Reproducibility Package

```python
class ReproducibilityPackage:
    def create_package(self, analysis):
        """Create complete reproducibility package."""
        return {
            "data_sources": analysis.sources,
            "data_checksums": self._compute_checksums(analysis.data),
            "code": self._export_analysis_code(analysis),
            "environment": self._export_conda_env(),
            "random_seeds": analysis.seeds,
            "figures": self._export_figures(analysis),
            "statistical_tests": analysis.test_results
        }
```

---

## Implementation Priority

| Phase | Priority | Effort | Impact |
|-------|----------|--------|--------|
| 1. Statistical Rigor | **CRITICAL** | Medium | Eliminates false positives |
| 4. Database APIs | **HIGH** | Medium | Unlocks volcano, other DBs |
| 2. Multi-Source | **HIGH** | High | Validates real patterns |
| 3. Physical Reasoning | **MEDIUM** | High | Interpretable results |
| 5. Output Quality | **MEDIUM** | Medium | Publishable findings |

---

## Success Criteria for v2.0

A finding is considered **valid** only when:

1. ✓ p-value < 0.001 (Monte Carlo validated)
2. ✓ Effect size meaningful (not just "close")
3. ✓ FDR-corrected for multiple comparisons
4. ✓ Replicated in ≥3 independent sources
5. ✓ Stable across time periods
6. ✓ Physical mechanism proposed
7. ✓ Plausibility score > 0.7

Until all criteria are met, findings are labeled **"candidate"** not **"validated"**.

---

## The Vision

OlympusFlow v2.0 should be able to:

1. **Autonomously explore** any scientific domain
2. **Rigorously validate** potential Z² patterns
3. **Reject false positives** before reporting
4. **Generate publishable** research papers
5. **Accumulate knowledge** that compounds over time

The goal is not to find patterns everywhere - it's to find the **real** patterns and prove them rigorously.

---

*Roadmap by: Carl Zimmerman & Claude*
*Date: May 5, 2026*
