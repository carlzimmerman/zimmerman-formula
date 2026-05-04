# HermesFlow: Autonomous Z² Research Agent

**Author:** Carl Zimmerman
**Date:** May 3, 2026

---

## Overview

HermesFlow is an **autonomous AI scientist** that discovers physics patterns using the Z² = 32π/3 geometric framework. Unlike TruthFlow (a manual research tool), HermesFlow runs autonomously with an observe-decide-act-learn loop.

## Quick Start

```bash
# Run autonomous research (explores all domains)
python run.py

# Research specific domain
python run.py --domain cosmology

# Reset agent state and start fresh
python run.py --reset

# Start MCP server (for Hermes/external integration)
python run.py --mcp
```

## Results

In initial testing, HermesFlow discovered **8 validated Z² patterns** across 4 domains:

| Domain | Target | Formula | Error | Status |
|--------|--------|---------|-------|--------|
| Particle Physics | α⁻¹ | 4Z² + 3 | 0.004% | VALIDATED |
| Particle Physics | sin²θ_W | 3/13 | 0.195% | VALIDATED |
| Cosmology | Ω_Λ | 13/19 | 0.072% | VALIDATED |
| Cosmology | n_s | Z/6 | 0.010% | VALIDATED |
| Neutrino | θ₁₂ | 3Z + 16 | 0.130% | VALIDATED |
| Neutrino | θ₂₃ | 4Z + 19 | 0.106% | VALIDATED |
| Neutrino | θ₁₃ | 2Z - 3 | 0.028% | VALIDATED |
| Meteorology | TS threshold | Z² | 1.440% | VALIDATED |

**Statistical significance**: p = 1.11 × 10⁻¹⁶

---

## Agent Loop

HermesFlow implements a true agent loop:

```
┌─────────┐
│ OBSERVE │ ← Check state (domains explored, truths found)
└────┬────┘
     │
┌────▼────┐
│ DECIDE  │ ← Choose action (explore, test, cross-analyze)
└────┬────┘
     │
┌────▼────┐
│   ACT   │ ← Execute using MCP tools
└────┬────┘
     │
┌────▼────┐
│  LEARN  │ ← Update knowledge graph, track results
└────┬────┘
     │
     └────────→ REPEAT until complete
```

---

## Architecture

```
HermesFlow/
├── run.py              # Main entry point
├── autonomous_agent.py # Agent loop (observe → decide → act → learn)
├── mcp_server.py       # MCP tools (auto-starting)
├── scientific_method.py # Statistical validation
├── knowledge_graph.json # Discovered truths (persistent)
├── agent_state.json    # Agent state (persistent)
├── learning_log.json   # Learning history (persistent)
└── legomena_training/  # Legomena model configs
```

---

## MCP Server

The MCP server auto-starts and exposes these tools:

| Tool | Description |
|------|-------------|
| `fetch_data` | Get empirical data for a domain |
| `generate_hypothesis` | Create testable Z² hypothesis |
| `test_hypothesis` | Computationally test hypothesis |
| `validate_result` | Statistical validation |
| `add_truth` | Add to knowledge graph |
| `query_knowledge` | Query knowledge graph |
| `research_domain` | Full autonomous research |

### Using MCP Tools Directly

```python
from mcp_server import ResearchTools

tools = ResearchTools()

# Fetch data
data = tools.fetch_data("cosmology")

# Generate hypothesis
hyp = tools.generate_hypothesis("cosmology", "omega_lambda")

# Test
result = tools.test_hypothesis(hyp, data)

# Validate
validation = tools.validate_result(result)
print(f"Verdict: {validation['verdict']}")
```

---

## Domains Supported

| Domain | Targets | Data Source |
|--------|---------|-------------|
| `particle_physics` | α⁻¹, sin²θ_W, quark masses | CODATA 2022, PDG 2024 |
| `cosmology` | Ω_Λ, Ω_m, n_s, H₀ | Planck 2020 |
| `neutrino` | θ₁₂, θ₂₃, θ₁₃ | NuFIT 5.2 |
| `meteorology` | TS/Cat thresholds | NHC |

---

## Requirements

```bash
pip install scipy numpy requests

# Legomena models (optional, for LLM hypothesis generation)
ollama pull legomena-31b
# or create from Gemma 4:
ollama create legomena-31b -f legomena_training/Modelfile_gemma4_31b
```

---

## Z² Framework

The fundamental constant:

```
Z² = 32π/3 ≈ 33.51  (cube × sphere ratio)
Z  = √Z²  ≈ 5.79
```

This single geometric constant predicts:
- Fine structure constant: α⁻¹ = 4Z² + 3
- Dark energy density: Ω_Λ = 13/19
- Neutrino mixing angles: θ = nZ + m
- Hurricane thresholds: TS = Z² kt

---

## Scientific Method

All discoveries are validated using:

1. **Explicit predictions** - Exact numerical values from Z² formulas
2. **Empirical data** - From authoritative sources (CODATA, PDG, Planck, NuFIT)
3. **Statistical tests** - p-values, confidence intervals
4. **Combined probability** - Probability of N matches by chance

### Validation Thresholds

| Error | Verdict |
|-------|---------|
| < 0.5% | VALIDATED (HIGH confidence) |
| 0.5-2% | VALIDATED (MEDIUM confidence) |
| 2-5% | INCONCLUSIVE |
| > 5% | FALSIFIED |

---

## TruthFlow vs HermesFlow

| Feature | TruthFlow | HermesFlow |
|---------|-----------|------------|
| **Mode** | Manual research tool | Autonomous agent |
| **Control** | You drive | Agent decides |
| **Loop** | Single run | Observe-decide-act-learn |
| **Learning** | None | Persistent across sessions |
| **MCP** | None | Auto-starting server |

Use **TruthFlow** for manual, controlled research.
Use **HermesFlow** for autonomous discovery.

---

## License

MIT

---

*HermesFlow: Autonomous scientific discovery.*
