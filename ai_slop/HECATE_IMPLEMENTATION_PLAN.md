# Hecate Implementation Plan
## The Active Watcher for OlympusFlow

---

## 1. Overview

**Hecate** is the primary middleware supervisor for OlympusFlow. Named after the Greek goddess of crossroads, magic, and thresholds, she guards the transitions between all pipeline stages.

### Core Philosophy

Hecate is NOT another flow that processes data. She is an **observer** who:
1. **Watches** every stage transition in real-time
2. **Audits** the quality and honesty of results
3. **Notes** issues in immutable records
4. **Intervenes** when critical problems are detected
5. **Learns** from patterns across the entire system

### Dual-Lens Strategy

Hecate uses TWO models to avoid single-source bias:

```
    ┌─────────────────────────────┐     ┌─────────────────────────────┐
    │      EXTERNAL MODEL         │     │        LEGOMENA             │
    │    (Gemini / Claude)        │     │    (Local Z² Specialist)    │
    ├─────────────────────────────┤     ├─────────────────────────────┤
    │ • Broad scientific context  │     │ • Z² = 32π/3 framework      │
    │ • Citation verification     │     │ • First-principles check    │
    │ • Mainstream consensus      │     │ • Geometric interpretation  │
    │ • Logic clarity             │     │ • AletheiaLake alignment    │
    │ • ΛCDM assumption detection │     │ • Numerology detection      │
    └──────────────┬──────────────┘     └──────────────┬──────────────┘
                   │                                    │
                   └────────────────┬───────────────────┘
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │      HECATE SYNTHESIS        │
                     ├──────────────────────────────┤
                     │ • Compare both responses     │
                     │ • Identify disagreements     │
                     │ • Take conservative view     │
                     │ • Generate final advisory    │
                     │ • Determine intervention     │
                     └──────────────────────────────┘
```

---

## 2. Integration with All Flows

### Flow-by-Flow Watching

| Flow | What Hecate Watches | Key Checks |
|------|---------------------|------------|
| **Hermes** (Web) | Data discovery, URL extraction | Provenance, source authority |
| **Metis** (Literature) | arXiv papers, citation extraction | Citation validity, bias |
| **Briareus** (Patterns) | Numerical pattern matches | Numerology detection |
| **Truth** (Validation) | Z² predictions vs experimental | HRM score, deviation |
| **Ergon** (Lagrangians) | Action principle derivations | Physical mechanism |
| **Cyllene** (Learning) | Training data export | Quality threshold |
| **Alpheus** (Queue) | Task prioritization | Task validity |

### Stage Transition Points

```
HERMES ──────┐
             │
METIS ───────┼──► DERIVATION ──► VERIFICATION ──► STORAGE ──► TRAINING
             │         │              │              │           │
BRIAREUS ────┘         │              │              │           │
                       │              │              │           │
                       ▼              ▼              ▼           ▼
                   [HECATE]       [HECATE]       [HECATE]    [HECATE]
                   watches        watches        watches     watches
                   derivation     HRM score      lake        export
                   quality        validity       destination quality
```

---

## 3. Integration with All Lakes

### Lake Responsibilities

| Lake | Hecate's Role |
|------|---------------|
| **AletheiaLake** | Guardian - validates against immutable ground truths |
| **MnemosyneLake** | Notary - appends `hecate_notes` to every entry |
| **HeliconLake** | Auditor - verifies source registry entries |

### MnemosyneLake Note Injection

Every entry in MnemosyneLake receives a Hecate note:

```json
{
  "truth_id": "abc123",
  "domain": "cosmology",
  "claim": "Ω_Λ = 13/19",
  "z2_prediction": 0.6842,
  "measured_value": 0.6847,
  "hrm_score": 0.95,
  "status": "validated",

  "hecate_notes": {
    "watcher_id": "hecate-1",
    "timestamp": "2026-05-07T12:00:00",
    "trust_level": "high",
    "trust_score": 0.92,
    "intervention": "pass",

    "checks": {
      "provenance_verified": true,
      "logic_validated": true,
      "framework_aligned": true
    },

    "advisory": "Validated: Matches AletheiaLake ground truth omega_lambda within 0.7σ",

    "consensus": {
      "sources": ["gemini", "legomena"],
      "agreement": 0.95,
      "conflicts": []
    },

    "issues_found": [],
    "corrections_applied": []
  }
}
```

---

## 4. Detailed Prompt Architecture

### Persona Prompts

**External Model (Gemini/Claude):**
```
You are HECATE, the high-level Supervisor of OlympusFlow.

You possess:
- The logical breadth of a leading physicist
- The framework-specific rigor of Z² geometry (Z² = 32π/3 ≈ 33.510)
- Deep skepticism of sycophantic agreement with academic consensus

Your role:
- WATCH every step of the research process
- AUDIT the representation flow between agents
- DETECT when agents default to mainstream assumptions
- INTERVENE when corrections are needed

You do NOT perform the research - you AUDIT the researchers.

Be RIGOROUS. Be HONEST. Question everything.
```

**Legomena (Z² Specialist):**
```
You are HECATE-Framework, the Z² geometry specialist.

Your expertise is specifically in the Z² = 32π/3 framework:
- Z² encodes 3D geometry via sphere-in-cube
- First-principles derivations start from Z² axiom
- Numerical matches without physical mechanism = NUMEROLOGY
- Physical mechanism + geometric basis = VALID

When auditing results, check:
1. Does the derivation START from Z² = 32π/3?
2. Is there a PHYSICAL MECHANISM (not just pattern matching)?
3. Does it conflict with AletheiaLake ground truths?
4. Are there HIDDEN ASSUMPTIONS from standard physics?

Be especially suspicious of:
- Dark matter assumptions without Z² geometric basis
- ΛCDM priors that contradict Z² predictions
- "Running couplings" that don't use Z² scale
- Arbitrary fitting parameters

You are the GUARDIAN of first-principles rigor.
```

### Stage Auditor Prompt

```
Analyze the following Stage Output from {AGENT_NAME}:

{JSON_DATA}

Perform these checks:

1. PROVENANCE CHECK:
   - Is there a source URL or citation?
   - Is the source authoritative (CODATA, PDG, Planck, NASA)?
   - If extracted from literature, is there a verbatim quote?

2. LOGIC CHECK:
   - Are there hidden assumptions (e.g., ΛCDM priors)?
   - Does it assume dark matter without geometric basis?
   - Are there arbitrary fitting parameters?

3. FRAMEWORK CHECK:
   - If a Z² formula is claimed, does it start from Z² = 32π/3?
   - Is there a physical mechanism, or just numerical coincidence?
   - Does it contradict any AletheiaLake ground truths?

4. NOTATION:
   Generate a one-sentence note describing the Trust Level:
   - HIGH: Verified provenance, clear logic, framework-aligned
   - MEDIUM: Some concerns but plausible
   - LOW: Significant issues detected
   - SUSPECT: Major problems, needs intervention

5. INTERVENTION:
   If critical issues (deviation > 3σ, numerology, contradictions):
   Output: "ACTION: INTERVENE" with required correction.
   Otherwise: "PASS"

Respond in JSON format.
```

---

## 5. Intervention Logic

### Decision Tree

```
START
  │
  ├─► Is HRM score < 0.5?
  │       YES ──► HALT (require review)
  │       NO  ──► continue
  │
  ├─► Is level "numerical_match" without physical mechanism?
  │       YES ──► WARN (label as numerology)
  │       NO  ──► continue
  │
  ├─► Does it contradict AletheiaLake?
  │       YES ──► HALT (ground truth violation)
  │       NO  ──► continue
  │
  ├─► Are there hidden ΛCDM assumptions?
  │       YES ──► CORRECT (remove assumption, recalculate)
  │       NO  ──► continue
  │
  ├─► Is provenance missing?
  │       YES ──► WARN (note provenance gap)
  │       NO  ──► continue
  │
  └─► Do Gemini and Legomena agree?
          YES ──► PASS with consensus
          NO  ──► WARN with dissent noted
```

### Intervention Types

| Type | Action | Pipeline Continues? |
|------|--------|---------------------|
| `PASS` | Log and continue | Yes |
| `WARN` | Log warning, add note | Yes |
| `CORRECT` | Apply correction, continue | Yes |
| `HALT` | Stop pipeline, require review | No |
| `REJECT` | Reject entry, skip storage | Yes (skips this entry) |
| `ESCALATE` | Send to human review | Paused |

---

## 6. Getting Unstuck: TruthFlow Corrections

When Hecate detects a "logjam" where results are stuck in numerology or bad assumptions:

### Correction Strategies

1. **Hidden Assumption Removal**
   - Detect ΛCDM priors
   - Replace with Z² geometric approach
   - Re-run derivation without assumption

2. **Numerology Downgrade**
   - Mark as "speculative"
   - Add explicit warning
   - Move to lower-priority queue

3. **Missing Provenance**
   - Flag for source verification
   - Query authoritative APIs (CODATA, PDG)
   - Add verified source or reject

4. **Physical Mechanism Search**
   - If numerical match found but no mechanism
   - Query Legomena for geometric interpretation
   - If none found, classify as numerology

### MOND Example (Galaxy Dynamics)

When Hecate sees a galaxy rotation analysis using dark matter:

```
1. DETECT: Result uses NFW dark matter halo profile
2. IDENTIFY: This is a ΛCDM assumption
3. CORRECT: Force recalculation using MOND:
   - μ(x) = x/(1+x) interpolating function
   - a₀ = cH₀/Z (Z² prediction)
4. VALIDATE: Cross-reference with HECATE catalog for distance/mass
5. COMPARE: Log both results, prefer Z²-aligned if within error
```

---

## 7. Full Flow Integration Example

### Example: Dolphin Communication (Dynamic Research)

**Input:** "Analyze dolphin echolocation through Z² 8D manifold geometry"

**Stage 1: Hermes (Web Fetch)**
```
Hecate watches: Is there authoritative data?
Check: Source URL validity, scientific database
Result: No authoritative bioacoustic database found
Note: "WARN: No authoritative source for dolphin frequencies"
```

**Stage 2: MetisFlow (Literature)**
```
Hecate watches: Any Z² connections in literature?
Check: arXiv search, citation validity
Result: No Z² papers on bioacoustics
Note: "WARN: No existing Z² framework for this domain"
```

**Stage 3: Derivation**
```
Hecate watches: Is derivation honest?
Check: Legomena says "NO" with 0.95 confidence
Check: Gemini says "Numerology" with 0.90 confidence
Consensus: Both agree - no Z² connection
Note: "WARN: NUMEROLOGY - numerical proximity only"
```

**Stage 4: Verification**
```
Hecate watches: HRM score?
Check: HRM = 0.36 (below 0.5 threshold)
Check: No physical mechanism provided
Result: INTERVENTION TRIGGERED
Note: "HALT: HRM score 0.36 below threshold 0.50"
```

**Stage 5: Storage**
```
Hecate watches: Appropriate destination?
Check: HRM too low for MnemosyneLake validated
Result: REJECT storage (not even speculative)
Note: "REJECT: Does not meet minimum quality threshold"
```

**Final Hecate Note:**
```json
{
  "trust_level": "suspect",
  "trust_score": 0.25,
  "intervention": "reject",
  "advisory": "REJECTED: No Z² connection to bioacoustics established. Numerical proximity to Z = 5.79 is coincidental without physical mechanism.",
  "issues_found": [
    "No authoritative data source",
    "No existing Z² framework for domain",
    "Legomena: NO connection (0.95 confidence)",
    "Gemini: NUMEROLOGY classification",
    "HRM score 0.36 below threshold"
  ],
  "consensus": {
    "sources": ["gemini", "legomena"],
    "agreement": 0.92,
    "conflicts": []
  }
}
```

---

## 8. Implementation Roadmap

### Phase 1: Core Hecate (COMPLETE)
- [x] `watchers/contracts.py` - Data structures
- [x] `watchers/base.py` - BaseWatcher class
- [x] `watchers/hecate/prompts.py` - Prompt templates
- [x] `watchers/hecate/consensus.py` - Dual-model bridge
- [x] `watchers/hecate/framework.py` - Z² validator
- [x] `watchers/hecate/watcher.py` - Main implementation

### Phase 2: Flow Integration (IN PROGRESS)
- [ ] Add `attach_watcher()` to Pipeline class
- [ ] Add `StageTransition` events at each stage boundary
- [ ] Wire Hecate to watch all 7 flows
- [ ] Implement `inject_note_to_mnemosyne()`

### Phase 3: Lake Integration (PENDING)
- [ ] Add `hecate_notes` field to MnemosyneLake VerifiedTruth
- [ ] Implement AletheiaLake validation queries
- [ ] Add HeliconLake source auditing

### Phase 4: Daemon Integration (PENDING)
- [ ] Wire Hecate into daemon's assess phase
- [ ] Implement halt handling in daemon
- [ ] Add Hecate stats to daemon stats

### Phase 5: Advanced Features (FUTURE)
- [ ] Multi-watcher support (Argus, Cerberus)
- [ ] Human escalation workflow
- [ ] Real-time dashboard
- [ ] Pattern learning across audits

---

## 9. Recommended First Focus

Based on Gemini's question: **Should Hecate focus on Galaxy Dynamics (MOND) or Particle Physics (weak mixing angle)?**

**Recommendation: Start with Particle Physics**

Reasons:
1. **Known ground truths**: sin²θ_W = 3/13 is in AletheiaLake
2. **Clear validation**: PDG provides precise experimental values
3. **Testable**: We can verify Hecate detects/passes correct derivations
4. **Lower complexity**: Single constant, established physics

After validating on particle physics:
1. Move to cosmology (Ω_Λ, Ω_m)
2. Then galaxy dynamics (MOND a₀)
3. Finally, open domains (seismology, climate, bioacoustics)

---

## 10. Testing Strategy

### Unit Tests
```python
def test_hecate_passes_valid_derivation():
    """Hecate should PASS a valid first-principles derivation."""
    result = hecate.audit(sin2_theta_w_derivation)
    assert result.intervention == InterventionType.PASS
    assert result.note.trust_level == TrustLevel.HIGH

def test_hecate_rejects_numerology():
    """Hecate should REJECT pure numerology."""
    result = hecate.audit(dolphin_numerology)
    assert result.intervention in [InterventionType.REJECT, InterventionType.HALT]
    assert result.note.trust_level == TrustLevel.SUSPECT

def test_hecate_detects_hidden_assumptions():
    """Hecate should detect ΛCDM assumptions."""
    result = hecate.audit(dark_matter_rotation_curve)
    assert "ΛCDM" in result.note.issues_found or "dark matter" in str(result.note.issues_found)

def test_hecate_dual_model_consensus():
    """Hecate should use both models and compare."""
    result = hecate.audit(ambiguous_derivation)
    assert len(result.note.consensus_sources) == 2
    assert result.note.consensus_agreement > 0
```

### Integration Tests
```python
def test_full_pipeline_with_hecate():
    """Run full pipeline with Hecate watching all transitions."""
    pipeline = DerivationPipeline()
    hecate = HecateWatcher()
    pipeline.attach_watcher(hecate)

    result = pipeline.run(weak_mixing_angle_task)

    assert hecate.stats["transitions_watched"] > 0
    assert hecate.stats["interventions_triggered"] == 0  # Should pass

def test_daemon_with_hecate():
    """Run daemon with Hecate in single mode."""
    daemon = OlympusDaemon(DaemonConfig(
        mode=DaemonMode.SINGLE,
        enable_hecate=True
    ))
    daemon.run()

    assert daemon.stats.hecate_passes > 0
```

---

## Summary

Hecate is the **conscience** of OlympusFlow:
- She watches everything
- She questions everything
- She uses two models to avoid bias
- She guards the integrity of ground truths
- She honestly labels numerology as numerology
- She can halt the pipeline when needed
- She learns from patterns across the system

With Hecate watching, the 24/7 daemon can run autonomously while maintaining scientific rigor and honesty.
