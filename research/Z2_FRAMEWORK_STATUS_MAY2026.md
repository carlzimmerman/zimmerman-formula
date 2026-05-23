# Z2 Framework: Current Status

**Carl Zimmerman | May 2026 (Updated)**

---

## Executive Summary

The Z2 framework (Z2 = 32pi/3 = 33.510321) proposes that fundamental constants arise from T3/Z2 orbifold compactification. This document summarizes the current empirical status after critical self-corrections in May 2026.

**Overall Assessment:** Framework has excellent numerical matches but fewer rigorous derivations than previously claimed. Key findings:
- **Omega_Lambda/Omega_m:** Excellent match (0.1 sigma), but 13/6 split is NOT derived (only 19 total DOF is derived)
- **alpha, r:** Both are CONJECTURES (impressive patterns, but combinations not proven)
- **Birefringence:** Serious 6 sigma tension with beta = 0 prediction
- **Retracted:** h_x = 0 and r derivation (both relied on flawed argument)

Decisive tests coming 2027-2031.

---

## Prediction Status

### Verified (Excellent Match)

| Prediction | Z2 Value | Observed | Tension | Derivation Status |
|------------|----------|----------|---------|-------------------|
| Omega_Lambda/Omega_m | 13/6 = 2.167 | 2.172 +/- 0.05 | 0.1 sigma | INCOMPLETE |
| Omega_Lambda | 13/19 = 0.6842 | 0.6847 +/- 0.0073 | 0.1 sigma | INCOMPLETE |
| n_s | 1 - 2/N = 0.967 | 0.965 +/- 0.004 | 0.5 sigma | DERIVED |
| a_0 (MOND) | cH/Z = 1.18e-10 m/s2 | ~1.2e-10 m/s2 | <1 sigma | INCOMPLETE |

**Note on Omega derivation:** The total 19 DOF = 12 + 4 + 3 IS derived from orbifold structure. However, WHY 13 goes to dark energy and 6 to matter is NOT derived - the source document admits "Status: PLAUSIBLE but INCOMPLETE."

### Consistent (No Conflict)

| Prediction | Z2 Value | Current Data | Status |
|------------|----------|--------------|--------|
| w (dark energy) | -1 exactly | -1.03 +/- 0.03 | Consistent |
| N (e-folds) | 61 | 50-60 typical | Consistent |
| No QCD axion | Projected out | No detection | Consistent |
| No fifth force | lambda ~ 1e-34 m | None observed | Consistent |
| No PBH dark matter | f_PBH ~ 0 | Constrained | Consistent |
| Quadrupole suppression | L ~ 12-13 Gpc | 21% of expected | Explains anomaly |

### Tension

| Prediction | Z2 Value | Observed | Tension |
|------------|----------|----------|---------|
| Cosmic birefringence beta | 0 deg | 0.30 +/- 0.05 deg | **~6 sigma** |

**Note:** Combined Planck+ACT analysis shows ~7 sigma detection of rotation (with caveats about systematics). Dust EB systematic may contribute ~0.1 deg, reducing true cosmic signal. LiteBIRD (2028-2031) will be definitive.

**This is the most serious challenge to the Z2 framework.** See `BIREFRINGENCE_COMPREHENSIVE_ANALYSIS_MAY2026.md`.

### Conjectures (Not Derived)

| Prediction | Value | Match | Status |
|------------|-------|-------|--------|
| alpha^-1 | 4Z2 + 3 = 137.04 | 0.004% | Components meaningful, combination ASSUMED |
| r (tensor/scalar) | 1/(2Z2) = 0.015 | TBD | NO VALID DERIVATION |

**Note on alpha:** The components (4 = rank(G_SM), Z2 = 32pi/3, 3 = b_1(T3)) have geometric/topological meaning. The 0.004% match is impressive. However, the specific combination alpha^-1 = 4Z2 + 3 is assumed, not proven from first principles. See `ALPHA_DERIVATION_AUDIT_MAY2026.md`.

**Note on r:** The claimed derivation relied on h_x being projected out (WRONG). Additionally, the derivation documents themselves fail to derive 1/(2Z2) - `perturbation_theory.md` Appendix D gets r ~ 8/Z2 ~ 0.24, not 0.015. The value r = 0.015 was adopted after r = 8*alpha = 0.058 was ruled out by data. It fits current constraints but has NO derivation.

### Retracted (May 2026)

| Prediction | Original Claim | Reason for Retraction |
|------------|----------------|----------------------|
| h_x = 0 | Cross-polarization projected out | Z2 acts on extra dimensions (y -> -y), not 4D; h_munu has no y-indices, so both polarizations are Z2-EVEN |
| r = 1/(2Z2) derivation | Factor 1/2 from h_x projection | Relied on same flawed h_x argument; now classified as conjecture |

---

## What Is Actually Derived (Honest Assessment)

### Truly Derived (Rigorous)

From the T3/Z2 orbifold and Z2 = 32pi/3:

1. **Topological quantities:**
   - chi(T3/Z2) = 4 (Euler characteristic) - mathematical fact
   - N_gen = b_1(T3) = 3 (fermion generations) - index theorem
   - 8 fixed points (Z2 orbifold structure) - mathematical fact
   - GAUGE = 12 (direct calculation)

2. **Inflationary parameters:**
   - N = 2Z2 - 6 = 61 e-folds (DERIVED)
   - n_s = 1 - 2/N = 0.967 (DERIVED, follows from N)

3. **Dark energy equation of state:**
   - w = -1 exactly (moduli frozen by orbifold fixed points)

4. **Null predictions:**
   - No QCD axion (B-field Z2-odd, projected out)
   - No observable KK modes (m ~ 1e18 GeV)
   - No PBH dark matter (insufficient perturbation amplitude)
   - beta = 0 deg (no pseudoscalar survives) - **but 6 sigma tension with data!**

### Incomplete Derivations (Gaps Remain)

5. **Cosmological parameters:**
   - Total DOF = 19 = 12 + 4 + 3 (DERIVED)
   - But WHY Omega_Lambda = 13/19 and Omega_m = 6/19 is NOT derived
   - The 13/6 split is assumed, not proven

6. **MOND acceleration:**
   - a_0 = cH/Z (holographic argument is plausible but incomplete)

---

## What Is Conjectured (Not Derived)

| Formula | Match | Issue |
|---------|-------|-------|
| alpha^-1 = 4Z2 + 3 | 0.004% | Components meaningful, but WHY this combination? |
| r = 1/(2Z2) | TBD | Original derivation INVALID, documents fail to derive it |

These are **patterns with physical intuition**, not first-principles derivations.

---

## Upcoming Tests

| Experiment | Observable | Z2 Prediction | Decisive? | Timeline |
|------------|------------|---------------|-----------|----------|
| LiteBIRD | beta | 0 deg | Yes | 2028-2031 |
| LiteBIRD | r | 0.015 (conjecture) | No | 2028-2031 |
| Euclid | w(z) | -1 exactly | Yes | 2027-2030 |
| DESI | w(z) | -1 exactly | Yes | 2025-2028 |
| ADMX | Axion | None | Moderate | Ongoing |
| CMB-S4 | r, beta | Various | Yes | 2030s |

---

## Falsification Criteria

**Z2 would be falsified if:**

| Observation | Threshold | Impact |
|-------------|-----------|--------|
| beta != 0 | >5 sigma detection | Fatal |
| w != -1 | >5 sigma evolution | Fatal |
| Axion detected | Any mass | Fatal (or major revision) |
| Fifth force | Any range | Fatal |
| Omega_Lambda/Omega_m | Outside 2.10-2.23 | Fatal |

**Z2 would NOT be falsified if:**

| Observation | Reason |
|-------------|--------|
| alpha^-1 != 4Z2 + 3 | Only a conjecture (though 0.004% match is striking) |
| r != 0.015 | Only a conjecture |
| h_x != 0 | Already retracted |
| PBH found | Would need extension |

---

## Confirmation Criteria

**Strong support if by 2031:**
- beta = 0.00 +/- 0.01 deg (null birefringence)
- w = -1.00 +/- 0.01 (exact cosmological constant)
- No axion despite full mu-eV coverage

**This would be striking because:**
- Current hints suggest beta != 0 and w != -1
- Most theories predict axions
- Z2 would have correctly predicted against trends

**Decisive evidence (extraordinary):**
- Direct detection of T3/Z2 topology
- Matched circles in CMB at L ~ 12-13 Gpc

---

## Honest Assessment

### Strengths
- Omega_Lambda/Omega_m match is excellent (0.1 sigma)
- Explains CMB quadrupole anomaly naturally
- Makes sharp, falsifiable predictions
- Self-correcting (retracted flawed derivations)

### Weaknesses
- Birefringence tension is serious (6 sigma)
- Omega 13/6 split is NOT derived (only 19 total is)
- alpha and r formulas are conjectures, not derivations
- No unique decisive confirmation yet

### Key Uncertainties
- Is beta = 0.30 deg real or systematic?
- Will w stay at -1 with better data?
- Can topology be detected directly?

---

## Summary Table

```
TRULY DERIVED:    chi=4, N_gen=3, GAUGE=12, N=61, n_s=0.967, w=-1, beta=0
INCOMPLETE:       Omega_Lambda=13/19 (19 derived, split assumed), a_0
VERIFIED MATCH:   Omega_Lambda/Omega_m, n_s, a_0 (excellent fits)
CONSISTENT:       w, axion, fifth force (no conflict)
TENSION:          beta = 0 deg vs 0.30 deg (6 sigma - CRITICAL)
CONJECTURE:       alpha^-1 = 4Z2 + 3, r = 1/(2Z2) (patterns, not derived)
RETRACTED:        h_x = 0, r derivation (May 2026 corrections)
```

---

## Timeline to Resolution

| Year | Milestone | Potential Outcome |
|------|-----------|-------------------|
| 2027 | Euclid first w(z) | w = -1 or tension |
| 2028 | LiteBIRD launch | - |
| 2028 | DESI full results | w constraint tightens |
| 2031 | LiteBIRD results | beta and r measured |
| 2031 | **Decisive verdict** | **Confirmed or falsified** |

---

*Document: Z2 Framework Status*
*Version: May 2026 (Updated with honest derivation assessment)*
*Status: Active research*
