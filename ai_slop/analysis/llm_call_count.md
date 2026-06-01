# OlympusFlow LLM Call Count Per Topic

**Analysis Date:** May 7, 2026
**LLM Model:** legomena-moe (via Ollama)

## Summary

| Flow | LLM Calls Per Topic | Notes |
|------|---------------------|-------|
| **DerivationEngine** | 3-5 | Core derivation logic |
| **Hecate Consensus** | 1-2 | Audit and validation |
| **HermesFlow/Dynamic Strategy** | 4-6 | Research exploration |
| **HermesFlow/Navigator** | 2-3 | URL navigation |
| **CylleneFlow/Deepener** | 1 | Per finding to deepen |
| **Total per topic** | **11-17** | End-to-end pipeline |

## Detailed Breakdown

### 1. DerivationEngine (derivation_engine.py)

```python
# Main derivation calls:
Line 536: connection_response = self._ask_legomena(physical_prompt)  # Physical connection
Line 836: response = self._ask_legomena(prompt)                      # Main derivation

# Multi-prompt refinement (conditional):
Line 245: skeptical_response = self._ask_legomena(skeptical_prompt)  # If confidence < 0.75
Line 319: alternatives_response = self._ask_legomena(alternatives_prompt)  # Alternative approaches
Line 400: synthesis_response = self._ask_legomena(synthesis_prompt)  # Synthesis
```

**Count: 2-5 calls** (2 mandatory + 3 conditional on confidence)

### 2. Hecate Consensus (watchers/hecate/consensus.py)

```python
Line 266: success, legomena_response = self.ask_legomena(legomena_prompt)  # Stage audit
```

**Count: 1-2 calls** (audit per stage transition)

### 3. HermesFlow Dynamic Strategy (flows/hermes/dynamic_strategy.py)

```python
# Research exploration:
Line 124: terms_response = self._ask_legomena(...)      # Generate search terms
Line 145: sources_response = self._ask_legomena(...)    # Identify sources
Line 172: quantities_response = self._ask_legomena(...) # Extract quantities
Line 188: z2_response = self._ask_legomena(...)         # Z² analysis
Line 321: response = self._ask_legomena(...)            # Additional analysis
Line 428: response = self._ask_legomena(...)            # Strategy refinement
```

**Count: 4-6 calls** (varies by complexity)

### 4. HermesFlow Navigator (flows/hermes/hermes_navigator.py)

```python
Line 152: def _ask_legomena_for_links(...)      # Identify relevant links
Line 193: def _ask_legomena_for_directory(...)  # Directory navigation
Line 343: candidate_urls = self._ask_legomena_for_links(...)  # URL selection
```

**Count: 2-3 calls** (per web source explored)

### 5. CylleneFlow Deepener (flows/cyllene/deepener.py)

```python
Line 393: response = ollama.generate(...)  # Generate research questions
```

**Count: 1 call** (per finding worth deepening)

## Pipeline Configuration

From `ARCHITECTURE.md` and code analysis:

```python
# derivation_engine.py defaults:
LEGOMENA_MODEL = "legomena-moe"
LEGOMENA_TIMEOUT = 600  # 10 minutes
MULTI_PROMPT_ATTEMPTS = 4
SKEPTICAL_THRESHOLD = 0.75
```

## Cost Estimation

**Per topic (typical):**
- DerivationEngine: 4 calls × ~2000 tokens/call = 8,000 tokens
- Hecate: 1 call × ~1000 tokens = 1,000 tokens
- HermesFlow: 5 calls × ~1500 tokens = 7,500 tokens
- Deepener: 1 call × ~1000 tokens = 1,000 tokens
- **Total: ~17,500 tokens per topic**

**For 600 topics:**
- 600 × 17,500 = 10.5 million tokens
- At local Ollama speeds: ~5-10 minutes per topic
- Total runtime: ~50-100 hours for full run

## Optimization Opportunities

1. **Batch similar topics** - Reduce redundant context loading
2. **Cache common prompts** - Reuse reasoning for similar constants
3. **Skip confident matches** - If formula matches known constant, skip refinement
4. **Parallel processing** - Run multiple derivations concurrently
