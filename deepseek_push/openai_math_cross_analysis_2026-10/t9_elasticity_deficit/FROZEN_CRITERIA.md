# T9 — FROZEN CRITERIA: the phantom-mass elasticity law ε(s)

**Claim to test (novel, derived from the campaign's own results):**
For a point baryon host in the Zimmerman framework (kernel ν(y) = 1/(1−e^{−√y}),
phantom density ρ_ph = ∇·[(ν−1)g_N]/(4πG)), the enclosed phantom mass at
radius r_out is, *kernel-exactly* (r_in → 0),

    M_ph(<r_out) = M_b · (ν−1)(r_out) = M_b / (e^{s} − 1),   s := r_t/r_out,
    r_t := √(G M_b / a₀)   (the transition radius, y(r_t) = 1).

Consequently the M_b-logarithmic elasticity of the enclosed phantom mass is

    ε(s) := d ln M_ph / d ln M_b = 1 − (s/2) e^{s}/(e^{s} − 1),

because d ln s/d ln M_b = 1/2. This is exact, holds at all radii (no deep-MOND
limit), and:

  (E1)  ε(s) → 1/2 as s → 0   (the deep-MOND √M_b law — the framework's own ½);
  (E2)  ε(s) < 1/2 for all s > 0   (universal sub-half deficit at finite r_out);
  (E3)  ε(s) → −∞?? no: monotone decreasing, zero at s* solving
        s e^{s} = 2(e^{s} − 1)  (s* ≈ 1.594, i.e. r_out ≈ 0.63 r_t).

**Screens (frozen):**
- Q1 derives a₀? NO — a₀ enters only through the unit s (and r_t is the
  framework's own definition). The claim derives the ELASTICITY law and its
  ½-limit from the fitted-a₀ framework. κ = ½ stays FITTED (the unification
  "κ = ½ = ε(0)" is DECLARED as an observation, not derived).
- Q2 forced or chosen? Every step of ε(s) follows from the closed form with
  NO inserted rational; the only inputs are the framework's kernel and the
  flux/Gauss definition of M_ph. The comparison radii (r_out = 818 kpc, MW
  canonical/alt) are T1's own.
- Q3 base-rate: not a constant search; the comparison is a FUNCTION (ε(s))
  against two measured numbers — no simple-form family applies. The measured
  numbers (0.4960/0.4964) are the T1 lane's outputs, committed 1fe0798a1.

**Checks that can fail (exit 1):**
- C1  ε_pred(canonical, s = r_t_can/818 kpc) ∈ [0.4960 − 0.0006, 0.4960 + 0.0006]
      (measured T1 elasticity 0.4960; window ±0.0006 declared).
- C2  ε_pred(alt, s = r_t_alt/818 kpc) ∈ [0.4964 − 0.0006, 0.4964 + 0.0006].
- C3  deep limit: ε(10⁻⁶) within 1e-9 of 1/2 (numeric instantiation of E1).
- C4  monotone: ε decreasing on [0.005, 3] (E2/E3 architecture check, 100 pts).
- C5  zero-crossing: |ε(s*) − 0(±1e-6)| for the declared root s* ± 1e-3.
- C6  bridge to T1 C6: exp(ε_can · ln 10^{+0.1}) − 1 ∈ [0.1200, 0.1220]
      (T1 measured +12.10%/+12.11% at +0.1-dex baryon error).
- C7  MUTATE isolation: T9_MUTATE=1 uses M_b^{1/3} scaling (s ∝ M_b^{1/3},
      ε = 1 − (s/3) e^{s}/(e^{s}−1)): C1, C2, C6 must flip (0.4963→0.6642,
      0.4966→0.6643, +12.1%→+18.7%); C3 must still pass (the deep limit stays
      1/2 under the MUTATE: 1 − (s/3)·(…)→1 − 1/3·… wait NO: (s/3) e^s/(e^s−1)
      → 1/3 at s→0 — so C3 flips too; declared: C1, C2, C3, C6 all fail under
      MUTATE), C4 must still pass (monotone decreasing on [0.005,3]),
      C5 must still pass (root s'* solves s e^{s} = 3(e^{s}−1) if checked —
      declared: root check re-solved, must pass with the MUTATE root).

**Language rules (frozen):** κ = ½ stays "fitted". ε(0) = ½ and κ = ½ are
declared a unification OBSERVATION ("the same ½ as the kernel's sub-leading
mode and the deep-limit elasticity"), never a derivation of κ. Both footings
reported separately. No "theory closed". No dark-matter particle; the cold
fluid's mass is still required (M_ph itself IS a required-mass statement).

**Deliverables:** this freeze, committed ALONE; then t9_elasticity_deficit.py
(main + MUTATE outs + 2 result jsons), t9_README.md, Lean certificate
cert_elasticity_deficit.lean (algebra payload: the closed form, the ε
identity, the factorisation (s/2)e^{s}/(e^{s}−1) = (s/2)/(1−e^{−s}), and the
tendsto-to-1/2 statement; numerics stay in the script, house practice).
Co-Authored-By: DeepSeek trailer on every commit.