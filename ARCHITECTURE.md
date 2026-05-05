# Z² Research System Architecture

## Current Modules

### Data Flow
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│  HermesFlow │────▶│  TruthFlow  │────▶│ CylleneFlow │────▶│ MnemosyneLake   │
│  (Discover) │     │  (Verify)   │     │  (Iterate)  │     │ (Store Truths)  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────────┘
                                                                    │
                                              ┌────────────────────┘
                                              ▼
                                        ┌─────────────┐
                                        │  Legomena   │
                                        │  (Reason)   │
                                        └─────────────┘
```

### Module Responsibilities

| Module | Role | Input | Output |
|--------|------|-------|--------|
| **HermesFlow** | Data Discovery | Topic, Domain | DataFrames from web |
| **TruthFlow** | Verification | Findings | Validated truths with HRM |
| **CylleneFlow** | Orchestration | Configuration | Iteration results |
| **MnemosyneLake** | Truth Storage | VerifiedTruth | Training data |
| **Legomena** | Reasoning | Questions | Answers |

## Proposed Architecture Improvements

### Option 1: Unified Pipeline (Recommended)
Create a single orchestrator that defines the pipeline declaratively.

```python
pipeline = Pipeline([
    DiscoverStage(source=HermesFlow, topic="USGS earthquakes"),
    VerifyStage(validator=TruthFlow, min_hrm=0.8),
    StoreStage(lake=MnemosyneLake),
    TrainStage(model=Legomena, method="quick_iteration"),
])

results = pipeline.run(iterations=10)
```

**Benefits:**
- Single entry point
- Clear stage ordering
- Easy to add/remove stages
- Testable stages

### Option 2: Event-Driven Architecture
Components publish events, others subscribe.

```python
@on_event("data_discovered")
def verify_finding(finding: Finding):
    truth_flow.validate(finding)

@on_event("truth_validated")
def store_truth(truth: VerifiedTruth):
    mnemosyne_lake.add(truth)

@on_event("truth_stored")
def trigger_training(truth: VerifiedTruth):
    if mnemosyne_lake.count() % 10 == 0:
        legomena.retrain()
```

**Benefits:**
- Loose coupling
- Easy to add new handlers
- Parallel processing potential
- Audit trail via event log

### Option 3: Hybrid (Pipeline + Events)
Main flow is pipeline-based, but key events trigger side effects.

```python
pipeline = Pipeline([
    DiscoverStage(...).on_success(emit("data_found")),
    VerifyStage(...).on_success(emit("truth_validated")),
    StoreStage(...),
])

@on_event("truth_validated")
def log_to_telemetry(truth):
    analytics.track("truth_validated", truth.domain)
```

## Data Contracts

### Finding (HermesFlow → TruthFlow)
```python
@dataclass
class Finding:
    topic: str
    source_url: str
    data: pd.DataFrame
    columns_of_interest: List[str]
    timestamp: datetime
```

### VerifiedTruth (TruthFlow → MnemosyneLake)
```python
@dataclass
class VerifiedTruth:
    truth_id: str
    domain: str
    claim: str
    z2_prediction: float
    measured_value: float
    percent_error: float
    hrm_score: float
    data_source: str
    timestamp: datetime
    status: TruthStatus
```

### TrainingExample (MnemosyneLake → Legomena)
```python
@dataclass
class TrainingExample:
    instruction: str
    input: str
    output: str
```

## Next Steps

1. **Create Pipeline Orchestrator** (`OlympusFlow/pipeline.py`)
   - Declarative pipeline definition
   - Stage interface with run() method
   - Error handling and retry logic

2. **Add Event System** (`OlympusFlow/events.py`)
   - Event bus for publish/subscribe
   - Event log for audit trail
   - Async event processing

3. **Define Data Contracts** (`OlympusFlow/contracts.py`)
   - Strict type definitions
   - Validation on stage boundaries
   - Serialization for persistence

4. **Monitoring Dashboard** (`OlympusFlow/dashboard.py`)
   - Real-time pipeline status
   - Truth accumulation metrics
   - Model performance tracking

## Naming Convention

Following the Greek mythology theme:
- **Hermes** - Messenger god (data discovery)
- **Cyllene** - Mountain where Hermes was born (iterative learning)
- **Mnemosyne** - Goddess of memory (truth storage)
- **Legomena** - "Things said" (reasoning)
- **Olympus** - Home of gods (unified orchestrator)
- **Aletheia** - Goddess of truth (verification)
