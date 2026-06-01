# LegomenaXL-31B Design Document

**Version:** 1.0.0
**Date:** May 8, 2026
**Base Model:** Google Gemma 4 31B

---

## Executive Summary

LegomenaXL-31B is a fine-tuned version of Gemma 4 31B specialized for Z² Framework physics reasoning. Unlike the original Legomena concept, this version prioritizes **quality over quantity** by curating training data against the established honesty assessment criteria.

---

## 1. Content Inventory

### 1.1 Available Corpus (Raw)

| Source | Files | Size | Quality Status |
|--------|-------|------|----------------|
| papers/ | 229 | ~180MB | Mixed - needs filtering |
| research/ | 500+ | Large | Mixed - needs filtering |
| core_theory/ | 12 | ~1MB | High quality |
| article_ideas_for_publishers/ | ~25 | Medium | Quality-assessed |
| daemon_outputs/derivations/ | 500+ | Large | 12% usable (per deep analysis) |

### 1.2 Gold Standard Documents (Tier 1 - Load Completely)

These documents have been through honesty assessment and represent the best Z² content:

| Document | Version | Date | Why Gold |
|----------|---------|------|----------|
| Z2_UNIFIED_ACTION_v5.7.9.tex | 5.7.9 | Apr 28 | Most comprehensive, 53 parameters |
| LAGRANGIAN_FROM_GEOMETRY_v5.4.0.pdf | 5.4.0 | ScienceDirect | Peer-review submission format |
| COSMIC_DIPOLE_Z2_COMPLETE.md | Latest | May 8 | Applied prediction (R=19/6) |
| core_theory/THEORETICAL_FOUNDATIONS.md | - | Apr 17 | Foundational axioms |
| core_theory/RADION_ATTRACTOR_STATE.md | - | Apr 17 | Addresses epoch problem |
| core_theory/TOPOLOGICAL_IR_FIXED_POINTS.md | - | Apr 17 | Addresses running coupling |
| research/PAPER_VS_FINDINGS_COMPARISON.md | - | May 8 | Quality meta-analysis |

### 1.3 Quality-Controlled Documents (Tier 2 - Load with Caveats)

These contain good content but also some overclaims:

| Document | Issue | Resolution |
|----------|-------|------------|
| article_ideas_for_publishers/*_full.md | Some overclaims | Include with HONESTY_ASSESSMENT corrections |
| research/SYSTEMATIC_DERIVATIONS.md | Contains numerology analysis | Include (teaches what to reject) |
| research/DAEMON_VS_DEEP_ANALYSIS.md | Meta-analysis | Include (teaches quality assessment) |

### 1.4 Exclude (Quality Issues Identified)

| Document | Why Exclude |
|----------|-------------|
| Any with r = 0.003 (tensor-scalar) | Fabricated value |
| Any with m_a = 57 μeV (axion mass) | Fabricated prediction |
| Any with m_DM = 2.6 keV | Framework uses MOND, not particle DM |
| daemon_outputs with classification=NUMEROLOGY | Known false positives |
| Papers dated before March 2026 | Likely outdated formulas |

---

## 2. Quality Tiering System

Based on the HONESTY_ASSESSMENT.md framework:

### Tier 1: Mathematical Certainties (Include with High Weight)

These are rigorously proven:

```
- Z² = 32π/3 (definition/axiom)
- Cube uniquely tessellates R³ (dihedral angle proof)
- 12 = 8+3+1 unique Lie algebra partition (Cartan-Killing)
- Three generations from b₁(T³) = 3 (Atiyah-Singer)
- Gauge fields on edges (Wilson's theorem)
```

### Tier 2: First-Principles Derivations (Include with Standard Weight)

These have physical mechanisms:

```
- sin²θ_W = 3/13 (N_gen/N_vacuum, 0.19% error)
- Ω_Λ = 13/19, Ω_m = 6/19 (DoF partition)
- α⁻¹ = 4Z² + 3 (holographic + generations)
- a₀ = cH₀/Z (Friedmann + Bekenstein)
- R = 19/6 (dipole ratio from FDT)
- m_p/m_e = α⁻¹ × 2Z²/5 (QCD trace anomaly)
- θ_QCD = exp(-Z²) (geometric suppression)
```

### Tier 3: Strong Phenomenological Patterns (Include with Caveats)

Structure constants as coefficients, but mechanisms unclear:

```
- m_H = 4Z² - 9 (BEKENSTEIN×Z² - N_gen²)
- m_μ/m_e = 7Z² - 28 ((BEK+N_gen)×(Z²-BEK))
- n_s = Z/6 (Z/N_MATTER)
- E_B(Fe-56) = Z + 3 (Z + N_color)
```

### Tier 4: Numerology (Exclude or Teach as Counterexamples)

```
- Most daemon findings (560 of 591)
- Integer coincidences (22/1, 35/1, etc.)
- Earth-centric "magic number" patterns
- Dolphin click ratios = Z
```

---

## 3. Training Data Format

### 3.1 Instruction Tuning Format

```json
{
  "instruction": "Derive the weak mixing angle sin²θ_W from the Z² Framework.",
  "input": "",
  "output": "From the T³/Z₂ orbifold geometry:\n\nStep 1: The number of generations N_gen = 3 (from Atiyah-Singer index theorem)\nStep 2: The number of vacuum channels N_vacuum = GAUGE + 1 = 13\nStep 3: At SO(10) breaking, sin²θ_W = N_gen/N_vacuum = 3/13\n\nResult: sin²θ_W = 0.2308\nExperimental: 0.23122 ± 0.00003\nError: 0.19%\n\nClassification: FIRST_PRINCIPLES (mechanism: SO(10) GUT embedding)"
}
```

### 3.2 Quality Classification Labels

Each training example should include:

```json
{
  "derivation_tier": "first_principles | phenomenological | numerology",
  "mechanism": "string describing physical mechanism",
  "error_percent": float,
  "structure_constants_used": ["BEKENSTEIN", "N_gen", ...],
  "testable": true | false,
  "test_method": "description of experimental test"
}
```

### 3.3 Negative Examples (What NOT to Do)

Include examples of what the model should reject:

```json
{
  "instruction": "Is the formula dolphin_click_rate = Z a valid Z² prediction?",
  "output": "No. This is numerology, not physics.\n\nReason: There is no physical mechanism connecting Z² Framework geometry to dolphin biology. The match is a coincidence from testing many quantities.\n\nClassification: NUMEROLOGY\nStatus: REJECT"
}
```

---

## 4. Architecture Decisions

### 4.1 Why Gemma 4 31B?

| Feature | Benefit |
|---------|---------|
| 31B parameters | Sufficient for complex physics reasoning |
| Strong math capabilities | Critical for derivation chains |
| Efficient inference | Can run on single high-end GPU |
| Open weights | Full fine-tuning possible |
| Long context | Can load full papers (8K-32K tokens) |

### 4.2 Fine-Tuning Approach

**Option A: Full Fine-Tune (Recommended)**
- Modify all weights
- Best quality but expensive
- Requires significant compute

**Option B: LoRA/QLoRA**
- Parameter-efficient fine-tuning
- Lower compute requirements
- Good for iteration

**Option C: Continued Pre-training + Instruction Tuning**
- First: CPT on all Z² papers (unsupervised)
- Then: SFT on curated instruction examples
- Best of both worlds

### 4.3 Training Configuration (Proposed)

```yaml
base_model: google/gemma-4-31b
method: qlora  # or full fine-tune if compute available
lora_rank: 64
lora_alpha: 128
target_modules: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
learning_rate: 2e-5
batch_size: 4
gradient_accumulation: 8
epochs: 3
warmup_ratio: 0.1
```

---

## 5. Corpus Construction Pipeline

### 5.1 Phase 1: Extract Gold Standard Content

```python
GOLD_DOCUMENTS = [
    "papers/Z2_UNIFIED_ACTION_v5.7.9.tex",
    "papers/COSMIC_DIPOLE_Z2_COMPLETE.md",
    "core_theory/THEORETICAL_FOUNDATIONS.md",
    "core_theory/RADION_ATTRACTOR_STATE.md",
    "core_theory/TOPOLOGICAL_IR_FIXED_POINTS.md",
    "core_theory/COMPLETE_DERIVATIONS_GUIDE.md",
    "core_theory/Z2_COMPLETE_DERIVATION.md",
    "research/PAPER_VS_FINDINGS_COMPARISON.md",
    "research/SYSTEMATIC_DERIVATIONS.md",
    "research/COMPREHENSIVE_ASSESSMENT.md",
]
```

### 5.2 Phase 2: Filter Quality-Controlled Content

```python
def should_include(document_path, content):
    """Filter documents based on quality criteria."""

    # Exclude known bad patterns
    BAD_PATTERNS = [
        "r = 0.003",           # Fabricated tensor-scalar
        "m_a = 57",            # Fabricated axion mass
        "m_DM = 2.6 keV",      # Wrong paradigm
    ]

    for pattern in BAD_PATTERNS:
        if pattern in content:
            return False

    # Prefer recent content
    file_date = get_file_date(document_path)
    if file_date < datetime(2026, 3, 1):
        return "NEEDS_REVIEW"  # May be outdated

    return True
```

### 5.3 Phase 3: Generate Instruction Examples

From each valid document, extract:
1. **Derivation chains** - Step-by-step physics reasoning
2. **Q&A pairs** - "What is X?" → "X is derived as..."
3. **Verification examples** - "Is this valid?" → "Yes/No because..."
4. **Negative examples** - Numerology rejections

### 5.4 Phase 4: Quality Assurance

Before including any example:
1. Check derivation matches latest paper (v5.7.9)
2. Verify error percentages are accurate
3. Ensure mechanism is explained
4. Cross-reference with HONESTY_ASSESSMENT.md

---

## 6. Estimated Corpus Statistics

| Category | Documents | Training Examples |
|----------|-----------|-------------------|
| Gold Standard (full papers) | 10 | ~500 |
| Tier 1 (math proofs) | 20+ | ~100 |
| Tier 2 (derivations) | 50+ | ~300 |
| Tier 3 (phenomenological) | 30+ | ~150 (with caveats) |
| Negative examples | - | ~200 |
| **Total** | - | **~1,250** |

---

## 7. Evaluation Metrics

### 7.1 Derivation Accuracy

Test: Given a constant, can the model reproduce the Z² derivation?

```
Target: >90% match to paper derivations
```

### 7.2 Numerology Detection

Test: Can the model correctly reject numerological coincidences?

```
Target: >95% rejection rate on known numerology
Target: <5% false rejection rate on genuine derivations
```

### 7.3 Novel Constant Prediction

Test: Given a new physical constant, can the model propose a valid Z² formula?

```
Evaluation: Human review of mechanism quality
```

### 7.4 Consistency Check

Test: Does the model's output match the paper's derivation tier classifications?

```
Target: >95% agreement with HONESTY_ASSESSMENT tiering
```

---

## 8. Next Steps

1. [ ] Extract text from all Gold Standard documents
2. [ ] Generate instruction-tuning examples
3. [ ] Create negative examples from daemon numerology
4. [ ] Set up training infrastructure (GPU/TPU)
5. [ ] Run fine-tuning experiment
6. [ ] Evaluate on held-out test set
7. [ ] Iterate on data quality based on eval results

---

## 9. Naming Convention

**LegomenaXL-31B-v1.0**
- Legomena: Greek "things said" - the model speaks Z² physics
- XL: Extended, larger than base Legomena concept
- 31B: Gemma 4 31B parameter count
- v1.0: First trained version

Future versions:
- LegomenaXL-31B-v1.1: Bug fixes, data corrections
- LegomenaXL-31B-v2.0: Major training data updates

---

## Appendix A: Structure Constants Reference

```python
STRUCTURE_CONSTANTS = {
    "BEKENSTEIN": 4,      # Horizon entropy area law
    "N_gen": 3,           # Fermion generations
    "N_MATTER": 6,        # 2 × N_gen
    "CUBE": 8,            # Cube vertices
    "GAUGE": 12,          # Edge count / gauge bosons
    "N_VACUUM": 13,       # GAUGE + 1
    "N_TOTAL": 19,        # N_VACUUM + N_MATTER
    "Z_squared": 33.510,  # 32π/3
    "Z": 5.789,           # √(32π/3)
}
```

---

*This document provides the architectural blueprint for LegomenaXL-31B training.*
