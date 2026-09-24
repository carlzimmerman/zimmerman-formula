# L05 — THE MULTI-OBJECT a₀-RADIUS WINDOW TEST (REGISTERED JWST PROGRAM, SYNTHETIC)

**2026-09-23 · moment channel · synthetic power study · VERDICT: PASS (38/38 checks, exit 0)**
**Pre-registration follows J09 (central window 27/27), J10 (J10-I core), J11+K09 (volume curve).**
**K07 did NOT land (no `K07_results.json`; aborted run) → per J11's registered fallback the volume window curve = J11 values, as re-measured and verified 19/19 in K09 (`K07_volume_tau_surface`, 24 points + thin anchor e₀ = 0.3876, thin window 1.882).**

---

## 1. The registered program statement (ready for a JWST RM program)

### 1.1 Measurables (per object)
| symbol | quantity | measurement |
|---|---|---|
| A | **atom**: fraction of line photons arriving in the zero-lag, zero-width spike (no scattering) | spectral decomposition of the transfer-function response; S/N = relative precision = 1/σ(ln A) |
| d̄_phys | physical reverberation lag (mean delay of the broad-line response) | cross-correlation of continuum and line light curves; S/N 1/σ(ln d̄) |
| M_b | virial black-hole mass | virial estimator from line width + luminosity (calibrated) |
| ρ_B | BLR particle density (density-local input) | volume-averaged density from line ratios / photoionization fits |

### 1.2 The statistic (framework core)
```
    J10-I = −ln A · r_B / (c · d̄_phys) = (r_B/R) · window(τ₀, q)
```
- framework radius **r_B = √(G M_b / a₀(ρ_B))**, a₀(ρ_B) = (c/2)√(G ρ_B) (density-local one-boundary statement; NOT the deep-MOND √(GM/a₀) kpc radius);
- central-source window: −lnA/E[D] = (1+q/3)/(½+q/4) ∈ **[4/3, 2]** (q-free, τ₀-free);
- volume-source window: −lnA_v/E[D]_v = **the curve W_v(τ₀,q)** (J11 values as verified in K09; tabulated below/inside `L05_results.json`).
- Frozen scale: R/c = 5.4348 d at R = 941 AU; G = 6.6743e-11, c = 2.9979e8, M☉ = 1.9884e30.

### 1.3 Sample (design)
- N_obj ∈ {1, 3, 10, 30}; log M_b/M☉ ~ U[7.5, 9.5]; ρ_B ~ log-U[1e-12, 1e-8] kg m⁻³ → r_B spans ≈ 1–2000 ld (a semester-scaled RM feasibility range; lags d̄ = E[D]·R/c ≈ days–tens of days in the sample table).
- Per object, (τ₀, q) and S/N:
  - **central-truth targets**: τ₀ ~ U[0.3, 3], q ~ U[0, 10], accepted only where the atom is measurable (−ln A ≤ 5, i.e. A ≥ e⁻⁵ ≈ 6.7e-3 — photon budget N_ph ≳ S/N²/A stays observable);
  - **volume-truth targets**: placed **exactly on the 18 verified J11/K09 cells** (τ₀ ∈ {0.3, 0.5, 1, 1.5, 2, 3} × q ∈ {0, 3, 10}), all with measurable atoms (18/18, C6).  The volume curve is tabular (K07 did not land), so generation and classification share one table — **no interpolation**, removing the interpolation-mismatch failure mode (see §5, honest record).
- Per-object S/N covers **{10, 30, 100}** (mixed program design cycles the three levels across the sample; homogeneous-S/N grid also computed).

### 1.4 Analysis / classification (3σ rule, pre-registered)
- Fake measurables: ln A, ln d̄ drawn Gaussian at stated 1/S/N; J10-I formed from the noisy pair; σ_rel² = (1/S/N)² + (1/(S/N·|ln A|))².
- **Central reading**: measured J10-I must intersect [4/3, 2]: violation ⟺ J10-I·(1−3σ_rel) > 2 **or** J10-I·(1+3σ_rel) < 4/3.
- **Volume reading**: measured J10-I must sit on the curve point W_v(τ₀,q): violation ⟺ |J10-I − W_v| > 3·σ_tot, σ_tot² = (J10-I·σ_rel)² + sW_pub² + sW_self² (measurement + published curve SE + this run's self-measurement SE — every declared uncertainty is paid).
- (τ₀,q) for the volume curve is the object's own (in the synthetic, truth-known — the maximum-information limit; a real program inverts (A, d̄) → (τ₀, q) via the K04 lane, in-flight, adding inversion error → the present power numbers are an **upper bound**, stated honestly).

### 1.5 Kill rule (pre-registered)
1. **Per-object**: ≥ 3σ violation of the correct window for the assumed geometry (central [4/3,2]; volume curve W_v) ⇒ the framework's BLR-radius assignment fails for that system.
2. **Family-wise (program level)**: ≥ 1 object violating at 3σ ⇒ trial fires; the rate is reported vs (N_obj, S/N, geometry truth, radius factor).
3. **Asymptotic kill**: if at S/N = 100 and N = 30 the test cannot detect a **2× radius discrepancy at 3σ** (rate < 0.8 in either geometry world) ⇒ the a₀-window test is **too weak asymptotically** and is reported as such (honest).

---

## 2. What was computed (synthetic, no real data touched)

The engine (`J02_moment_hierarchy.py::simulate`, central/volume) re-measured A_v and E[D]_v on the 24-point K09 grid at n = 600k/point.  The implied window W = −lnA_v/E[D]_v matches the published K09 curve at **every** point (max z = 2.24; C2), and the τ₀=1 row matches the J11 verdict values (max z = 2.31; C3); E[D]_v(1,0) = 0.33879 vs the J11-recorded 0.338 (z = 0.96; C4).  The A2744-QSO1 anchors reproduce (central q0 reading 1.818 = record; volume q0 1.716 ≈ record 1.719; C5) — the doorB scale r_B/R = 40.9/45 = 0.90889 stays CONSISTENT-OPEN.

## 3. POWER (family-wise P(≥1 object violates at 3σ); 4000 trials/cell)

### 3.1 Central geometry truth
| N_obj | S/N | f=1.0 **false-kill** | f=1.5 | f=2.0 |
|---|---|---:|---:|---:|
| 1 | 10 | 0.0003 | 0.312 | 0.919 |
| 1 | 30 | 0.0000 | 0.843 | 0.995 |
| 1 | 100 | 0.0000 | 0.961 | 1.000 |
| 3 | 10 | 0.0008 | 0.683 | 0.9998 |
| 3 | 30 | 0.0000 | 0.994 | 1.000 |
| 3 | 100 | 0.0000 | 1.000 | 1.000 |
| 10 | 10 | 0.0008 | 0.978 | 1.000 |
| 10 | 30 | 0.0000 | 1.000 | 1.000 |
| 10 | 100 | 0.0000 | 1.000 | 1.000 |
| 30 | 10 | 0.0025 | 1.000 | 1.000 |
| 30 | 30 | 0.0008 | 1.000 | 1.000 |
| 30 | 100 | 0.0000 | 1.000 | 1.000 |

### 3.2 Volume geometry truth (window = J11/K09 curve point; per-object false-kill floor ≈ 2.7e-3 two-sided 3σ + curve SEs)
| N_obj | S/N | f=1.0 **false-kill** | f=1.5 | f=2.0 |
|---|---|---:|---:|---:|
| 1 | 10 | 0.0032 | 0.675 | 0.915 |
| 1 | 30 | 0.0050 | 0.972 | 1.000 |
| 1 | 100 | 0.0029 | 1.000 | 1.000 |
| 3 | 10 | 0.0162 | 0.958 | 0.999 |
| 3 | 30 | 0.0120 | 1.000 | 1.000 |
| 3 | 100 | 0.0108 | 1.000 | 1.000 |
| 10 | 10 | 0.0393 | 1.000 | 1.000 |
| 10 | 30 | 0.0325 | 1.000 | 1.000 |
| 10 | 100 | 0.0298 | 1.000 | 1.000 |
| 30 | 10 | 0.1213 | 1.000 | 1.000 |
| 30 | 30 | 0.0853 | 1.000 | 1.000 |
| 30 | 100 | 0.0850 | 1.000 | 1.000 |

**Reading**: (i) the **false-kill rate under the correct consistent reading is the 3σ family floor** — ≈ 0 for central (interval test; only the q→0 window-edge cell contributes ≈ 2.5e-3 at N=30/S/N=10), and ≈ 1−(1−2.7e-3)^N for volume (point test) — 8.5% family-wise at N=30 even at S/N=100; this is a property of any 3σ point test, reported honestly, not a framework failure.  (ii) **Detection**: a **2× radius discrepancy is caught essentially with certainty** (≥ 0.9998) by any sample with N ≥ 3 at S/N = 10, and a 1.5× discrepancy at detection 0.98–1.00 by a 10-object program at S/N = 10 (central 0.978 / volume 1.000), rising to 1.000 at S/N ≥ 30.
**Mixed design** (S/N cycles 10/30/100 exactly as a JWST program would field): N=30 → false-kill 0.001 (central) / 0.092 (volume); detection 1.5× 1.000 / 2× 1.000; N=10 → 2× 1.000 both worlds.

## 4. THE BUDGET (bars of family-wise detection; 2000 trials/point)

| bar | geometry | required per-object S/N (N=10, 2×) | required N_obj (S/N=30, 2×) |
|---|---:|---:|---:|
| 0.50 | central | **≤ 5** (scan floor) | **1** |
| 0.50 | volume | **≤ 5** (scan floor) | **1** |
| 0.80 | central | **≤ 5** (scan floor) | **1** |
| 0.80 | volume | **≤ 5** (scan floor) | **1** |
| 0.95 | central | **≤ 5** (scan floor) | **1** |
| 0.95 | volume | **≤ 5** (scan floor) | **1** |

- Interpretation: a **10-object program detects a 2× radius discrepancy at 3σ family-wise with probability ≥ 0.95 already at per-object S/N ≈ 5** (the scan floor; the true threshold is lower — at S/N = 3 family detection at N=10 is 0.953, verified separately).  At fixed S/N = 30 **a single object suffices** (P = 0.995 central / 1.000 volume).  Caveats, stated: (a) the volume world's family-wise *false*-kill at N=10 is 3–4% at these S/N (the 3σ point-test floor, §3.2) — the program budget should be read as detection at the cost of that floor; (b) these numbers assume the (τ₀,q) inversion is exact (K04 in-flight) — inversion error weakens the volume reading → an upper bound; (c) virial-mass error enters r_B ∝ √M_b (5–10% typical) and dilutes S/N nominally by ~5% at S/N=10; not folded into this synthetic (cleaner falsification target).

## 5. Verdict (the kill rule applied)

**KILL CHECK (asymptotic weakness)**: detection(2× | N=30, S/N=100) = **1.0000 ± 0.0000 (central) / 1.0000 ± 0.0000 (volume)**, 5000 trials, bar 0.8.
⇒ **VERDICT: PASS — the a₀-window test is NOT asymptotically too weak.**  At the registered design point (S/N=100, N=30) a 2× radius error is detected at 3σ with certainty in both geometry worlds.  The test's power is not the asymptotic bottleneck; the honest constraints are the volume reading's family-wise 3σ false-kill floor (8.5% at N=30) and the (τ₀,q)-inversion term (K04, in-flight) that bounds the volume curve's usable precision.

**Honest record — a failure mode found and closed mid-flight**: the first L05 build drew volume-truth (τ₀,q) *continuously* and interpolated the re-measured A_v/E[D]_v while classifying against the published curve; the interpolation mismatch between the two surfaces (steep W-vs-q gradient, q ∈ [3,10] spans 1.88→0.71) produced a spurious **0.897 false-kill for a single consistent object at S/N=100**.  Closed by placing volume targets exactly on the verified 18 cells (no interpolation) and paying curve SEs in σ_tot; the guard check C7 now measures the false-kill floor at N=1/S/N=100 as central 0.00000 / volume 0.00287 — the clean 3σ floor.  Recorded verbatim here per lane rules.

## 6. Files
- `L05_a0_program.py` + `L05_a0_program.out` (full log, 38/38 checks) + `L05_results.json` (machine-parsed results).
- No git commit; no real data touched (synthetic generator only); `L05_results.json` contains the full power/budget/verdict tables.