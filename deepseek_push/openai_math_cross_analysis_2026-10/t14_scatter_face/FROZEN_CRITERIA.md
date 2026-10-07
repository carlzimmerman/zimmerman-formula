# T14 — FROZEN CRITERIA: the scatter face (completeness variance traces
# formation-time variance)

**Claim to test (novel derivation from T12's epoch-elasticity):**

The settling law f = 1 − e^{−Γt} propagates formation-time scatter into
completeness scatter EXACTLY through the T12 closed form:

    σ(f)/f = ε(f)·σ(ln t_f),    ε(f) = (1−f)·[−ln(1−f)]/f

  (S1)  The measured X-COP cluster scatter (f = 0.43 ± 0.15) reads:
        σ(ln t_c) = (0.15/0.43)/0.7451 = 0.468 — clusters' completeness
        spread is a FORMATION-TIME spread of ±47% in log-time, i.e.
        t_c ∈ [4.2, 10.7] Gyr across the sample — consistent with the
        z₁₄-evolution observed in halo-formation catalogs.
  (S2)  Groups (f = 0.60 ± 0.15): σ(ln t_g) = (0.15/0.60)/0.6109 = 0.409.
  (S3)  Clock universality: the two σ(ln t) agree within propagated
        errors (ratios 1.144 with ranges overlapping heavily) — the
        formation clocks of clusters and groups scatter alike at their
        respective masses. THE FALSIFIABLE SHAPE: σ(f)/[f·ε(f)] = σ(ln t)
        is SAMPLE-INDEPENDENT — plotting measured σ(f) vs f·ε(f) for any
        completeness samples must be a line through the origin with one
        slope σ(ln t) ≈ 0.4–0.5.
  (S4)  Memory-erasure corollary: because the settling is the heat
        equation (T10), completeness at fixed Δ carries NO environment
        correlation at fixed formation time — residual environmental
        clustering of f must vanish once t_f is controlled. (Testable
        with X-COP + assembly-epoch data; registered.)

**Falsifier (registered):** a completeness sample whose σ(f)/[f·ε(f)]
differs from 0.4–0.5 by > 2σ, or a slope ≠ constant across samples,
kills the exponential law's variance structure.

**Screens:** Q1 — derives from the framework's settling law (T12's
certified ε); a₀/κ not involved; Q2 — no inserted rational; the scatters
are measured inputs; Q3 — functional/variance law.

**Checks that can fail (exit 1):**
  C1  transport identity: numerical finite-difference of d ln f/d ln t
      matches ε(f) at 40 f-values to rel err < 1e-6 (the propagation
      coefficient is the exact T12 function).
  C2  cluster reading: |σ(ln t_c) − 0.468| < 0.005; t-range
      e^{±0.468} = [4.2, 10.7] Gyr around the 6.7-Gyr anchor.
  C3  group reading: |σ(ln t_g) − 0.409| < 0.005.
  C4  universality: σ(ln t_c)/σ(ln t_g) ∈ [1.0, 1.3] AND the propagated
      ranges overlap (σ(f) ∈ [0.05, 0.25] on both).
  C5  shape: σ(f)/[f·ε(f)] identical at f = 0.43 and 0.60 by
      construction; the CHECK is the sample-independence statement with
      the MW floor EXCLUDED (its scatter is unpublished — registered
      limitation).
  C6  MUTATE (T14_MUTATE=1: linear-branch ε ≡ 1 replaces the exact
      closed form): C1 must fail; C2–C5 must fail (0.349/0.25 values,
      ratio 1.40 > 1.3).
  C7  literature grounding: halo-formation-time scatter from the
      cluster-formation catalog literature (2603.19521 percentile
      ranges and/or 1–2 more sources): report the measured σ(ln t_f)
      vs the predicted 0.47 — registers as consistent or kill signal.

**Deliverables:** freeze committed ALONE; t14_scatter_face.py + .out ×2
+ results ×2; README (the readings, the falsifiable shape, the corollary,
the grounding verdict); algebra payload: the ε(f) closed form is already
certified in cert_epoch_elasticity.lean (T12) — this lane references it
and carries the derivative transport (house pattern: calculus rides in
the lane). No new cert unless the transport reduces to new pure algebra.
Language: nothing "closed"; falsifier first-class; κ/a₀ untouched.