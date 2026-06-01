# Honest Code Audit: Meteorology Folder

*Carl Zimmerman, April 2026*

This document provides an honest assessment of the meteorology codebase, identifying what works, what doesn't, and what needs improvement.

---

## Executive Summary

**Overall Assessment**: The codebase is functional but has significant issues that limit scientific rigor and reproducibility.

| Category | Status | Details |
|----------|--------|---------|
| Core Physics | ✓ Good | Well-structured, documented, mathematically correct |
| ERA5 Integration | ✓ Works | Successfully loads cloud data |
| Calibration | ⚠ Flawed | Hardcoded eye_ratio undermines Z² claims |
| Scripts | ⚠ Redundant | Multiple overlapping scripts |
| Documentation | ⚠ Excessive | 10 research docs with some redundancy |
| Tests | ✗ Minimal | Only 1 test file, no CI |

---

## 1. CRITICAL ISSUES

### 1.1 Hardcoded eye_ratio in Calibration

**File**: `scripts/calibrate_expanded.py:362`
```python
predicted = compute_rate(point['wind_ms'], point['sst_k'], point['shear'], 0.18, params)
```

**Problem**: The calibration uses `eye_ratio = 0.18` for ALL storms instead of computing it from ERA5 data.

**Impact**:
- The high z2_weight (0.90) is likely an artifact
- Cannot claim Z² structure "contributes to skill" when structure is constant
- Undermines the main scientific claim

**Fix Required**: Use ERA5-derived eye_ratio for each storm, as done in `validate_calibrated_predictor.py`.

---

### 1.2 Parameters Hit Optimization Bounds

**File**: `src/physics/calibrated_params.py`
```python
'mpi_slope': 20.0000,      # At upper bound
'mpi_intercept': 50.0000,  # At upper bound
'shear_scale': 25.0000,    # At upper bound
```

**Problem**: Three parameters hit their bounds, indicating:
- The optimizer wanted to go further
- Current parameter values are constrained, not optimal
- Results are sensitive to arbitrary bound choices

**Fix Required**: Expand bounds and re-optimize, or use unbounded optimization.

---

## 2. CODE QUALITY ISSUES

### 2.1 Redundant Scripts

Multiple scripts do similar things:

| Script | Lines | Purpose | Status |
|--------|-------|---------|--------|
| `calibrate_intensity_model.py` | 567 | Original 5-storm calibration | Superseded |
| `calibrate_expanded.py` | 503 | 18-storm calibration | Current |
| `validate_calibrated_predictor.py` | 424 | Validation with structure | Works |
| `validate_model.py` | 283 | Generic validation | Unclear purpose |
| `train_era5.py` | 414 | Training script | May be unused |
| `train_fast.py` | 521 | Fast training | May be unused |
| `train_minimal.py` | 145 | Minimal training | May be unused |
| `test_predictor_era5.py` | 498 | ERA5 testing | Works |

**Recommendation**: Remove or archive superseded scripts.

### 2.2 Duplicate Model Implementations

Three files implement intensity prediction:
1. `src/physics/z2_intensity_model.py` - Full featured, 528 lines
2. `src/physics/z2_hurricane_predictor.py` - Predictor class, 655 lines
3. `src/physics/hurricane_z2.py` - Another implementation, 403 lines

**Problem**: Unclear which is canonical. Different formulations.

**Recommendation**: Consolidate into one module.

### 2.3 Missing Error Handling

Many scripts silently catch exceptions:
```python
except Exception as e:
    pass  # Silent failure
```

This hides errors and makes debugging difficult.

---

## 3. DOCUMENTATION ISSUES

### 3.1 Excessive Research Documents

10 markdown files in `/research/`:
- `EXPANDED_CALIBRATION_ANALYSIS.md` - Critical analysis ✓
- `FLUID_DYNAMICS_FROM_8D_MANIFOLD.md` - Speculative theory
- `FLASH_FLOOD_EARLY_WARNING.md` - Unrelated to core work
- `HURRICANE_GEOMETRY_ANALYSIS.md` - Overlaps with others
- `MODEL_COMPARISON_REPORT.md` - Useful comparison
- `RIGOROUS_SCIENTIFIC_ASSESSMENT.md` - Good honest assessment ✓
- `SCIENTIFIC_VALIDATION_REPORT.md` - Overlaps with assessment
- `UNIVERSAL_VORTEX_PREDICTION.md` - Speculative predictions
- `WHY_ONE_OVER_Z_DERIVATION.md` - Theoretical exploration
- `Z2_SPHERE_GEOMETRY_DERIVATION.md` - Mathematical proof ✓

**Recommendation**: Consolidate overlapping documents.

### 3.2 Unclear Main Entry Point

No clear "start here" for someone new to the codebase.

---

## 4. WHAT WORKS WELL

### 4.1 Core Physics (`src/physics/z2_intensity_model.py`)
- Well-documented classes
- Physically motivated formulations
- Proper use of dataclasses
- Self-test in `__main__`

### 4.2 ERA5 Data Loading (`src/data/era5_loader.py`)
- Successfully connects to Google Cloud
- Handles authentication
- Caches data appropriately

### 4.3 Eye/RMW Analysis
- `validate_calibrated_predictor.py` correctly computes eye/RMW from ERA5
- Shows mean ratio ≈ 0.174 (close to 1/Z = 0.173)
- This IS a valid scientific finding

### 4.4 Mathematical Derivations
- `Z2_SPHERE_GEOMETRY_DERIVATION.md` proves Z² = 32 × Vol(S⁷)/Vol(S⁵)
- This is mathematically correct and interesting

---

## 5. HONEST ASSESSMENT OF CLAIMS

### Claim: "Z² structure factor improves intensity predictions"

**Status**: NOT RIGOROUSLY PROVEN

**Why**: The calibration uses fixed eye_ratio = 0.18, so the "structure factor" is constant for all storms. The high z2_weight (0.90) is acting as a multiplier on rate_coeff, not capturing structural variation.

**What Would Prove It**: Calibration with real, varying eye_ratio measurements showing z2_weight > 0.

### Claim: "Eye/RMW → 1/Z ≈ 0.173"

**Status**: SUPPORTED

**Why**: `validate_calibrated_predictor.py` computes actual eye/RMW from ERA5 and finds mean ≈ 0.174 (0.7% from 1/Z). This is computed correctly.

### Claim: "Test RMSE improved 64.6%"

**Status**: TRUE BUT MISLEADING

**Why**: The improvement is real, but with fixed eye_ratio, it's due to parameter tuning, not Z² structure learning.

---

## 6. RECOMMENDED ACTIONS

### Immediate (Before Making More Claims):

1. **Fix calibrate_expanded.py** - Use real eye_ratio from ERA5
2. **Re-run calibration** - See if z2_weight is still significant
3. **Update research docs** - Reflect corrected results

### Short-term:

4. **Consolidate physics modules** - One canonical implementation
5. **Archive old scripts** - Move superseded files to `archive/`
6. **Add proper tests** - pytest with coverage

### Longer-term:

7. **Expand to more storms** - 50+ for robust statistics
8. **Add uncertainty quantification** - Bootstrap or Bayesian
9. **Compare to null model** - Does Z² beat simple regression?

---

## 7. FILE-BY-FILE STATUS

### Keep and Improve:
- `src/physics/z2_intensity_model.py` - Main intensity model
- `src/physics/calibrated_params.py` - Parameters (after re-calibration)
- `src/data/era5_loader.py` - Data loading
- `scripts/validate_calibrated_predictor.py` - Validation (correct approach)
- `research/RIGOROUS_SCIENTIFIC_ASSESSMENT.md` - Honest assessment

### Needs Fixing:
- `scripts/calibrate_expanded.py` - Hardcoded eye_ratio

### Consider Archiving:
- `scripts/calibrate_intensity_model.py` - Superseded
- `scripts/train_era5.py`, `train_fast.py`, `train_minimal.py` - Unclear purpose
- `src/physics/hurricane_z2.py` - Redundant?

### Consolidate:
- Research documents with overlapping content

---

## 8. CONCLUSION

The meteorology codebase contains genuinely interesting work:
- The eye/RMW → 1/Z finding IS supported by data
- The ERA5 integration works well
- The physics is well-motivated

However, the **intensity calibration claims are undermined by the hardcoded eye_ratio**. This is a fixable issue, but it means current claims about "Z² structure contributing to skill" are premature.

**Bottom line**: Good foundation, needs cleanup and rigorous re-validation before making scientific claims.

---

*Honest science requires honest code review.*

---

Carl Zimmerman, April 2026
