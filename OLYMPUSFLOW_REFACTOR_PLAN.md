# OlympusFlow Unified Architecture Refactoring Plan

**Date:** May 7, 2026
**Goal:** Consolidate all Flows and Lakes into OlympusFlow as subcomponents, creating a truly autonomous 24/7 research engine

---

## Current State Analysis

### What We Have (8 Flows, 3 Lakes)

```
zimmerman-formula/
├── OlympusFlow/         # Central orchestrator (v1.7.0)
├── AlpheusFlow/         # Queue management
├── CylleneFlow/         # Learning/deepening
├── HermesFlow/          # Web research agent
├── BriareusFlow/        # Pattern search
├── TruthFlow/           # Validation pipeline
├── MetisFlow/           # Literature research
├── ErgonFlow/           # Action principles (partial)
├── AletheiaLake/        # Ground truths
├── MnemosyneLake/       # Session memory
├── HeliconLake/         # Source registry
├── research/            # 992 files, 664 topics
├── full_pipeline_results/
├── run_*.py             # 10+ entry scripts
└── [many scattered outputs]
```

### Problems With Current Structure

1. **Fragmentation** - Components scattered across root directory
2. **Import complexity** - Each Flow imported separately
3. **Results mixed with code** - No clear separation
4. **Multiple entry points** - 10+ run_*.py scripts doing overlapping things
5. **Functionality drift** - Logic built then forgotten as new scripts created
6. **No unified daemon** - Can't run 24/7 without babysitting

---

## Proposed Architecture: OlympusFlow as Monorepo Core

### Directory Structure

```
zimmerman-formula/
│
├── OlympusFlow/                          # THE UNIFIED ENGINE
│   ├── __init__.py                       # Main entry point
│   ├── __main__.py                       # CLI: python -m OlympusFlow
│   ├── daemon.py                         # 24/7 autonomous daemon
│   │
│   ├── core/                             # Central orchestration
│   │   ├── __init__.py
│   │   ├── pipeline.py                   # Main pipeline class
│   │   ├── autonomous_controller.py      # Continuous operation
│   │   ├── learning_loop.py              # Pattern learning
│   │   ├── event_bus.py                  # Inter-component events
│   │   ├── config.py                     # Global configuration
│   │   └── logging.py                    # Unified logging
│   │
│   ├── derivation/                       # Derivation engine
│   │   ├── __init__.py
│   │   ├── engine.py                     # Main derivation logic
│   │   ├── contracts.py                  # Known derivations
│   │   ├── symbolic.py                   # SymPy verification
│   │   ├── formula_generator.py          # Pattern discovery
│   │   └── hrm.py                        # Holistic Reasoning Mechanism
│   │
│   ├── flows/                            # ALL FLOWS AS SUBMODULES
│   │   ├── __init__.py
│   │   │
│   │   ├── alpheus/                      # Queue & Orchestration
│   │   │   ├── __init__.py
│   │   │   ├── queue.py
│   │   │   ├── orchestrator.py
│   │   │   └── batch.py
│   │   │
│   │   ├── hermes/                       # Web Research Agent
│   │   │   ├── __init__.py
│   │   │   ├── agent.py                  # Autonomous agent
│   │   │   ├── research.py               # Research tools
│   │   │   ├── hypothesis.py             # Hypothesis engine
│   │   │   ├── literature.py             # Paper collector
│   │   │   └── blind_discovery.py        # Blind testing
│   │   │
│   │   ├── briareus/                     # Pattern Search
│   │   │   ├── __init__.py
│   │   │   ├── pattern_search.py
│   │   │   ├── controller.py
│   │   │   ├── geometric.py              # Geometric interpretation
│   │   │   └── phenomenological.py
│   │   │
│   │   ├── truth/                        # Validation Pipeline
│   │   │   ├── __init__.py
│   │   │   ├── engine.py                 # Truth engine
│   │   │   ├── validator.py              # Robust validation
│   │   │   ├── fetcher.py                # Data fetching
│   │   │   └── parser.py                 # Constant extraction
│   │   │
│   │   ├── cyllene/                      # Learning & Deepening
│   │   │   ├── __init__.py
│   │   │   ├── deepener.py               # Recursive investigation
│   │   │   ├── training.py               # Training data generation
│   │   │   ├── model_updater.py          # Legomena fine-tuning
│   │   │   └── iteration.py              # Iteration runner
│   │   │
│   │   ├── metis/                        # Literature Research
│   │   │   ├── __init__.py
│   │   │   ├── literature_searcher.py
│   │   │   ├── strategy.py
│   │   │   └── engine.py
│   │   │
│   │   └── ergon/                        # Action Principles
│   │       ├── __init__.py
│   │       ├── action_deriver.py
│   │       └── lagrangian_templates.py
│   │
│   ├── lakes/                            # ALL LAKES AS SUBMODULES
│   │   ├── __init__.py
│   │   │
│   │   ├── aletheia/                     # Ground Truths (Permanent)
│   │   │   ├── __init__.py
│   │   │   ├── lake.py
│   │   │   ├── schema.py
│   │   │   └── ground_truths.json
│   │   │
│   │   ├── mnemosyne/                    # Session Memory (Temporary)
│   │   │   ├── __init__.py
│   │   │   ├── lake.py
│   │   │   ├── schema.py
│   │   │   └── truths/                   # Session files
│   │   │
│   │   └── helicon/                      # Source Registry
│   │       ├── __init__.py
│   │       ├── lake.py
│   │       ├── registry.json
│   │       └── domain_index.json
│   │
│   ├── api/                              # External Data APIs
│   │   ├── __init__.py
│   │   ├── codata.py                     # NIST CODATA
│   │   ├── pdg.py                        # Particle Data Group
│   │   ├── planck.py                     # Planck Collaboration
│   │   └── experimental.py               # Unified interface
│   │
│   ├── statistical/                      # Statistical Validation
│   │   ├── __init__.py
│   │   ├── validator.py                  # Monte Carlo, FDR
│   │   ├── baseline.py                   # Random baseline
│   │   └── significance.py               # Significance testing
│   │
│   └── cli/                              # Command Line Interface
│       ├── __init__.py
│       ├── commands.py                   # CLI commands
│       └── daemon_manager.py             # Start/stop daemon
│
├── research/                             # RESEARCH DATA (separate)
│   ├── topics/                           # Topic definitions
│   │   └── research_topics.py
│   ├── investigations/                   # Per-topic investigations
│   │   ├── particle_physics/
│   │   ├── cosmology/
│   │   └── ...
│   └── archive/                          # Historical research
│
├── outputs/                              # ALL OUTPUTS (separate)
│   ├── results/                          # Pipeline results
│   │   └── YYYY-MM-DD_HHMMSS/
│   ├── discoveries/                      # Validated findings
│   ├── assessments/                      # Honesty assessments
│   ├── logs/                             # Daemon logs
│   └── checkpoints/                      # Resume state
│
├── docs/                                 # Documentation
│   ├── architecture.md
│   ├── flows/
│   └── lakes/
│
└── scripts/                              # Entry Points (minimal)
    ├── olympus                           # Main CLI entry
    ├── run_daemon.py                     # Start 24/7 daemon
    └── run_single.py                     # Run single topic
```

---

## The 24/7 Autonomous Daemon

### Core Concept

```python
# OlympusFlow/daemon.py

class OlympusDaemon:
    """
    24/7 Autonomous Research Daemon

    Runs continuously, doing what Carl did over 800 commits:
    1. Find interesting topics/constants
    2. Try Z² formulas against them
    3. Honestly assess results
    4. Learn from successes and failures
    5. Deepen into promising areas
    6. Generate new research questions
    7. Repeat forever
    """

    def __init__(self, config: DaemonConfig):
        # Initialize all flows
        self.hermes = HermesFlow()      # Web research
        self.alpheus = AlpheusFlow()    # Queue management
        self.metis = MetisFlow()        # Literature research
        self.briareus = BriareusFlow()  # Pattern search
        self.truth = TruthFlow()        # Validation
        self.cyllene = CylleneFlow()    # Learning/deepening
        self.ergon = ErgonFlow()        # Action principles

        # Initialize all lakes
        self.aletheia = AletheiaLake()  # Ground truths
        self.mnemosyne = MnemosyneLake()  # Session memory
        self.helicon = HeliconLake()    # Source registry

        # Core systems
        self.pipeline = OlympusPipeline(...)
        self.controller = AutonomousController(...)
        self.learning = LearningLoop(...)

    def run_forever(self):
        """Main daemon loop - emulates Carl's 800-commit research process"""

        while self.running:
            # 1. DISCOVER: Find new topics/constants
            new_topics = self.hermes.discover_topics()
            new_constants = self.hermes.extract_constants()

            # 2. QUEUE: Prioritize research
            self.alpheus.add_batch(new_topics + new_constants)

            # 3. RESEARCH: Literature context
            for task in self.alpheus.get_batch():
                context = self.metis.research_literature(task)

                # 4. PATTERN: Search for Z² matches
                patterns = self.briareus.search(task, context)

                # 5. DERIVE: Attempt derivations
                for pattern in patterns:
                    result = self.pipeline.derive(task, pattern)

                    # 6. VALIDATE: Check against real data
                    validation = self.truth.validate(result)

                    # 7. ASSESS: Honest evaluation
                    assessment = self.assess_honestly(result, validation)

                    # 8. STORE: Based on assessment
                    if assessment.is_first_principles:
                        self.aletheia.store(result)
                    elif assessment.is_promising:
                        self.mnemosyne.store(result)

                    # 9. LEARN: Update patterns
                    self.learning.learn(result, assessment)

                    # 10. DEEPEN: If significant, investigate further
                    if assessment.significance > 0.8:
                        questions = self.cyllene.deepen(result)
                        self.alpheus.add_batch(questions, priority=HIGH)

            # 11. CHECKPOINT: Save state for resumability
            self.checkpoint()

            # 12. REPORT: Periodic summaries
            if self.time_for_report():
                self.generate_report()
                self.run_meta_assessment()  # Honesty assessment of assessments
```

---

## The Scientific Method Loop

### Emulating Carl's 800-Commit Research Process

```
┌─────────────────────────────────────────────────────────────────────┐
│                    THE SCIENTIFIC METHOD LOOP                       │
│                 (What Carl did over 800 commits)                    │
└─────────────────────────────────────────────────────────────────────┘

1. OBSERVE (HermesFlow)
   │  "I wonder if there's a pattern in X..."
   │  • Web research for empirical data
   │  • Constant extraction
   │  • Literature review
   ▼

2. HYPOTHESIZE (BriareusFlow + MetisFlow)
   │  "Maybe X relates to Z² via formula Y..."
   │  • Pattern search (34,000+ combinations)
   │  • Literature context for plausibility
   │  • Formula generation
   ▼

3. TEST (OlympusFlow Core)
   │  "Does formula Y actually match the data?"
   │  • Numerical evaluation
   │  • Error calculation
   │  • SymPy verification
   ▼

4. VALIDATE (TruthFlow)
   │  "Is this match statistically significant?"
   │  • Monte Carlo baseline
   │  • FDR correction
   │  • Multi-source verification
   ▼

5. ASSESS HONESTLY (HRM + Statistical Validator)
   │  "Is this real physics or numerology?"
   │  • Evidence level classification
   │  • Mechanism plausibility
   │  • Selection bias quantification
   ▼

6. LEARN (CylleneFlow + LearningLoop)
   │  "What patterns worked? What failed?"
   │  • Success pattern extraction
   │  • Failure categorization
   │  • Template weight updates
   ▼

7. DEEPEN OR MOVE ON
   │  If significant: Generate new research questions
   │  If not: Archive and try next topic
   │
   └──────────────────────────────────────────────────────▶ BACK TO 1
```

---

## Honesty Assessment Hierarchy

### Three Levels of Honest Evaluation

```
LEVEL 1: Individual Finding Assessment
─────────────────────────────────────
For each Z² match:
• Numerical accuracy (% error)
• Formula simplicity
• Physical mechanism plausibility
• Selection bias estimate
• Verdict: FIRST_PRINCIPLES | DERIVED | NUMEROLOGY

LEVEL 2: Batch Assessment (Daily/Weekly)
─────────────────────────────────────────
Across all findings:
• Success rate vs random baseline
• Domain distribution
• Formula type distribution
• Are we finding patterns or just fitting?
• Verdict: SYSTEMATIC_FINDING | CHERRY_PICKING | NULL_RESULT

LEVEL 3: Meta-Assessment (Monthly)
───────────────────────────────────
Assessment of the assessments:
• Are our Level 1 verdicts calibrated?
• Are we being too generous or too harsh?
• What would a skeptical physicist say?
• What would change our mind?
• Verdict: HONEST | BIASED | NEEDS_RECALIBRATION
```

### Implementation

```python
# OlympusFlow/assessment/meta_assessment.py

class MetaAssessment:
    """Honesty assessment of the honesty assessments"""

    def assess_calibration(self, assessments: List[Assessment]) -> CalibrationReport:
        """
        Check if our assessments are calibrated:
        - If we say 70% confidence, are we right 70% of the time?
        - Are we systematically over/under confident?
        """
        pass

    def skeptic_review(self, findings: List[Finding]) -> SkepticReport:
        """
        What would a skeptical physicist say about our findings?
        - Are the mechanisms physically reasonable?
        - Is the selection bias accounted for?
        - Are there simpler explanations?
        """
        pass

    def update_criteria(self, meta_report: MetaReport):
        """
        Adjust assessment criteria based on meta-assessment:
        - Tighten HRM thresholds if too generous
        - Expand template search if too restrictive
        """
        pass
```

---

## Preserving the 800 Commits of Functionality

### Audit of Existing Logic to Preserve

| Logic | Current Location | Preserve In | Status |
|-------|------------------|-------------|--------|
| Z² formula matching | formula_generator.py | derivation/formula_generator.py | ✓ |
| HRM scoring | derivation_engine.py | derivation/hrm.py | ✓ |
| Multi-prompt skepticism | derivation_engine.py | derivation/engine.py | ✓ |
| SymPy verification | symbolic_engine.py | derivation/symbolic.py | ✓ |
| Learning loop | learning_loop.py | core/learning_loop.py | ✓ |
| Bandit selector | bandit_selector.py | core/bandit.py | ✓ |
| Pattern search | BriareusFlow/pattern_search.py | flows/briareus/pattern_search.py | ✓ |
| Web research | HermesFlow/autonomous_agent.py | flows/hermes/agent.py | ✓ |
| Deepening | CylleneFlow/deepener.py | flows/cyllene/deepener.py | ✓ |
| Literature search | MetisFlow/literature_searcher.py | flows/metis/literature.py | ✓ |
| Ground truth storage | AletheiaLake/lake.py | lakes/aletheia/lake.py | ✓ |
| Session memory | MnemosyneLake/lake.py | lakes/mnemosyne/lake.py | ✓ |
| Source registry | HeliconLake/lake.py | lakes/helicon/lake.py | ✓ |
| Known derivations | derivation_contracts.py | derivation/contracts.py | ✓ |
| Statistical validation | statistical_validator.py | statistical/validator.py | ✓ |

### Logic at Risk of Being Lost

| Logic | Current Location | Risk | Action |
|-------|------------------|------|--------|
| 664 research topics | research_topics.py | HIGH | Move to research/topics/ |
| Blind discovery mode | z2_blind_discovery.py | MEDIUM | Integrate into flows/hermes/ |
| Evidence levels | honest_pipeline.py | LOW | Already in derivation/ |
| Domain-specific templates | various | HIGH | Consolidate in derivation/templates/ |
| Historical research files | research/ (992 files) | HIGH | Archive properly |

---

## Migration Plan

### Phase 1: Create New Structure (Non-Breaking)

1. Create `OlympusFlow/flows/` directory
2. Create `OlympusFlow/lakes/` directory
3. Create symbolic links to existing code
4. Add `__init__.py` files for new imports

### Phase 2: Move Flows (Incremental)

Move one Flow at a time:
1. AlpheusFlow → OlympusFlow/flows/alpheus/
2. BriareusFlow → OlympusFlow/flows/briareus/
3. TruthFlow → OlympusFlow/flows/truth/
4. CylleneFlow → OlympusFlow/flows/cyllene/
5. MetisFlow → OlympusFlow/flows/metis/
6. ErgonFlow → OlympusFlow/flows/ergon/
7. HermesFlow → OlympusFlow/flows/hermes/ (largest, last)

### Phase 3: Move Lakes

1. AletheiaLake → OlympusFlow/lakes/aletheia/
2. MnemosyneLake → OlympusFlow/lakes/mnemosyne/
3. HeliconLake → OlympusFlow/lakes/helicon/

### Phase 4: Consolidate Entry Points

1. Create unified `olympus` CLI
2. Deprecate individual run_*.py scripts
3. Create `daemon.py` for 24/7 operation

### Phase 5: Separate Outputs

1. Create `outputs/` directory structure
2. Move all results to `outputs/results/`
3. Move assessments to `outputs/assessments/`
4. Configure all Flows to use new output paths

### Phase 6: Documentation

1. Update imports throughout
2. Add migration guide
3. Update README

---

## Success Criteria

### Technical

- [ ] Single import: `from OlympusFlow import Daemon`
- [ ] Run with: `python -m OlympusFlow daemon start`
- [ ] All existing tests pass
- [ ] No code lost in migration

### Autonomous Operation

- [ ] Daemon runs 24+ hours without intervention
- [ ] Automatically discovers new topics
- [ ] Learns from successes and failures
- [ ] Generates honest assessments
- [ ] Produces meta-assessments weekly

### Honesty

- [ ] Every finding has honest evidence level
- [ ] Selection bias quantified
- [ ] Meta-assessments catch over-confidence
- [ ] "Numerology until proven otherwise" default

---

## Questions for Carl

1. **Research data separation:** Should research/ stay in this repo or move to a separate repo?

2. **Historical preservation:** Archive the 992 research files as-is, or reorganize by domain?

3. **Daemon hosting:** Where will the 24/7 daemon run? (Local machine, cloud server, etc.)

4. **Output retention:** How long to keep results? (Forever, rolling window, etc.)

5. **Meta-assessment frequency:** Daily, weekly, or on-demand?

---

## Estimated Effort

| Phase | Files Affected | Lines of Code | Risk |
|-------|----------------|---------------|------|
| Phase 1: Structure | 50+ new | ~500 | Low |
| Phase 2: Move Flows | 100+ | ~8000 (move) | Medium |
| Phase 3: Move Lakes | 20+ | ~2000 (move) | Low |
| Phase 4: Entry Points | 10+ | ~1000 | Medium |
| Phase 5: Outputs | 20+ | ~500 | Low |
| Phase 6: Docs | 10+ | ~2000 | Low |

**Total:** Major refactoring, but incremental and reversible at each phase.

---

## Next Steps

1. Review and approve this plan
2. Create Phase 1 structure
3. Begin incremental migration
4. Test continuously
5. Deploy daemon when stable
