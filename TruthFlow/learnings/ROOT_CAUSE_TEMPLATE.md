# Root Cause Analysis Template

## Failure Information

**Date:** YYYY-MM-DD
**Prediction:** [Which Z² prediction failed]
**Formula:** [Z² formula used]
**Z² Value:** [Computed value]
**Empirical Value:** [Measured value ± uncertainty]
**Sigma Tension:** [How many sigma off]

---

## Root Cause Categories

### 1. Measurement Error
- [ ] Old/outdated measurement
- [ ] Known systematic error
- [ ] Conflicting measurements exist
- [ ] Measurement technique questioned

### 2. Z² Framework Error
- [ ] Formula derivation error
- [ ] Wrong geometric identity used
- [ ] Missing correction factor
- [ ] Approximation broke down

### 3. Implementation Error
- [ ] Code bug
- [ ] Unit conversion error
- [ ] Numerical precision issue
- [ ] Wrong constant value

### 4. Interpretation Error
- [ ] Comparing different quantities
- [ ] Running vs pole mass confusion
- [ ] Different renormalization scheme
- [ ] Definition mismatch

---

## Analysis

### What was compared?
[Detailed description of what Z² predicts vs what was measured]

### Why the discrepancy?
[Analysis of the most likely cause]

### Evidence
[Links to papers, calculations, or code that support the analysis]

---

## Resolution

### If Measurement Error:
- [ ] Wait for updated measurement
- [ ] Note conflicting measurements
- [ ] Track future experiments

### If Z² Error:
- [ ] Document the flaw
- [ ] Attempt correction
- [ ] Note impact on other predictions

### If Implementation Error:
- [ ] Fix the code
- [ ] Add test case
- [ ] Re-run validation

---

## Learning Captured

**What we learned:**
[Key insight from this failure]

**Future prevention:**
[How to avoid this type of error]

**Impact on Z² confidence:**
- [ ] No impact (implementation/measurement issue)
- [ ] Minor concern (small correction needed)
- [ ] Major concern (fundamental issue)
- [ ] Z² falsified (clear prediction wrong)

---

## Status

- [ ] Under investigation
- [ ] Resolved (measurement issue)
- [ ] Resolved (code fixed)
- [ ] Unresolved (Z² limitation documented)
- [ ] Z² FALSIFIED

---

*TruthFlow Learning System*
