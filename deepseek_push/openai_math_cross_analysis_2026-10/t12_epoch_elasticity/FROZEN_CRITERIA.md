# T12 — FROZEN CRITERIA: the epoch-elasticity of completeness

**Claim to test (novel derivation from the settling law + the record):**

Given the settling law f = 1 − e^{−Γt} (CFG382's law; T10's heat-mode
origin; T11's ratio clock), the completeness-to-epoch sensitivity is the
EXACT function of f alone:

    ε(f) := d ln f / d ln t = Γt·e^{−Γt}/(1 − e^{−Γt})
          = (1 − f)·[−ln(1 − f)]/f        (closed form, Γ and t cancelled)

  (E1)  ε → 1 as f → 0 (young systems: f ≈ Γt, unit sensitivity —
        the linear branch) and ε → 0 as f → 1 (mature: saturation).
  (E2)  ε strictly DECREASING in f — the completeness of young, fast-
        assembling systems is MORE epoch-sensitive per unit log-time.
  (E3)  Values at the record's three clocks: MW floor f = 0.14 →
        ε = 0.930; groups f = 0.60 → ε = 0.611; clusters f = 0.43 →
        ε = 0.745. The cluster:group sensitivity ratio is 1.219 —
        clusters respond ~22% more per unit log-epoch than groups.
  (E4)  Single-λ consistency (error-propagated): at the R500 convention
        ρ_crit(z), the λ intervals recovered from the group and cluster
        clocks MUST overlap — the two solid clocks must agree on the
        same coupling. (The MW floor is NOT re-fitted here: CFG382's
        floor calibration used the diluted supply-ball density, a
        different convention — registered as a limitation, aligned
        with CFG382's own PARTIAL verdict.)

**Falsifier (registered):** an epoch-split completeness sample (stack by
red-sequence age / concentration / halo-formation redshift): the
measured d ln f/d ln t must follow the curve ε(f), in particular the
ordering ε(0.43) > ε(0.60) and the shape (1−f)·ln(1/(1−f))/f. A flat
sensitivity (ε ≈ const ≠ curve) kills the exponential law's empirical
face.

**Screens:** Q1 — derives from the framework's settling law; a₀/κ enter
not at all (ratio/elasticity-level statement); Q2 — no inserted rational;
the 0.14/0.43/0.60 are measured inputs; Q3 — functional law.

**Checks that can fail (exit 1):**
  C1  closed form: |ε_exact(f) − (1−f)(−ln(1−f))/f| < 1e-9 at the three
      recorded f's.
  C2  ordering: ε(0.43) > ε(0.60) (0.745 > 0.611, ratio 1.219 ± 0.001).
  C3  monotone decreasing: max numerical dε/df on f ∈ [0.01, 0.99]
      (1000 pts) < 0.
  C4  asymptotes: ε(0.01) ∈ (0.98, 1.02); ε(0.99) < 0.05.
  C5  single-λ: λ-intervals from group and cluster clocks at the R500
      convention (f ± 0.15, epochs t_c = 6.7 ± 1.0 Gyr from z₁₄ ≈ 0.8,
      t_g = 11.9 ± 1.5 Gyr, ρ = 500ρ_crit(z), z_c = 0.75, z_g = 0.15,
      H₀ = 68, Ωm = 0.3) INTERSECT — the union of the two must not be
      empty; report the joint window [λ_min, λ_max].
  C6  consistency-with-record report: CFG382 P1/P2 numbers (0.722/0.714
      at τ since z = 2) vs this lane's clock reading (λ-joint window)
      — registered discussion, no verdict change (CFG382's PARTIAL
      stands on its own criteria).
  C7  MUTATE (T12_MUTATE=1: law replaced by the LINEAR branch ε = 1):
      C1–C4 must FAIL (1 ≠ 0.745/0.611/0.930; no ordering; no decay);
      C5/λ unchanged in construction (uses f directly) — declared to
      pass.

**Deliverables:** freeze committed ALONE; t12_epoch_elasticity.py + .out
×2 + results ×2; README (curve table, falsifier, λ window, CFG382
cross-reference); Lean certificate of the closed-form identity (ε as a
pure function of f — algebra with the law; the derivative itself rides
in the lane, house pattern).
Language: nothing "closed"; κ/a₀ untouched; the law's empirical face is
killable and the kill condition is registered.