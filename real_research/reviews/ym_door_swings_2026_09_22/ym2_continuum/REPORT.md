# D-YM2 swing: the continuum limit, not unlocked

**Door.** R5 (the scaling window) and R6 (the four-dimensional continuum
limit with a surviving gap). This is the Clay problem itself. The reopen
directive gives its unlock as "a genuinely new analytic control that
survives the weak→strong crossover." It was swung as hard as this session
could, both on the framework's own terms and mathematically. **It did not
open, and no prize-level claim is made.** The numbers below come from
`wall_map.py` (exit 0, `results.json`).

## 1. What the prize requires

Jaffe–Witten's official problem statement asks for two things. First, a
quantum Yang–Mills theory on ℝ⁴ for a compact simple gauge group,
satisfying axioms at least as strong as Wightman or Osterwalder–Schrader,
with the short-distance behaviour of asymptotic freedom. Second, a mass gap
Δ > 0 in that theory.

On the lattice this means the following. Take a sequence a → 0 with
g²(a) → 0 along the asymptotic-freedom trajectory. For each spacing, bound
the lattice gap m(β) in lattice units, and show that m(β)/a(β) converges to
a finite, positive Δ. At the same time the correlation functions must
converge to a non-trivial limit satisfying the axioms.

## 2. What is now proved in the repository (all at fixed spacing)

| statement | window | explicit? |
|---|---|---|
| Kogut–Susskind gap ≥ 3x/16, uniform in N and volume (`ym1_hamiltonian`, this campaign) | g² ≥ 185.3 (all N); 120.4 (SU(3), b = N) | yes |
| Wilson transfer-matrix gap m ≥ −ln(18 tanh β), D = 4 (`ym1_euclidean`) | β_W < 0.0556, i.e. g² > 108 for SU(3) | yes, including the rate |
| Shen–Zhu–Zhu 2023 (CMP 400, 805) | β_W < N²/48, i.e. g² > 32 for SU(3) | threshold yes; rate only up to "∼" (their Rem. 4.12) |

**Refinement of the register.** `opus_49_doorE/REPORT.md` lane (b) says
no explicit, quantitative, volume-uniform strong-coupling gap theorem
exists for SU(N). SZZ 2023 does have an explicit threshold, but its rate
is not explicit and degrades with N. The two new files here make both the
threshold and the rate explicit.

## 3. The wall, quantified

For the SU(3) scaling window, a/r_0 comes from Necco–Sommer eq. (2.6) and
the lightest glueball from Morningstar–Peardon, r_0 m(0⁺⁺) = 4.21:

| β_W | g² | a [fm] | m_G a | ξ/a |
|---|---|---|---|---|
| 5.70 | 1.053 | 0.170 | 1.43 | 0.70 |
| 6.00 | 1.000 | 0.093 | 0.78 | 1.27 |
| 6.40 | 0.938 | 0.051 | 0.43 | 2.31 |
| 6.92 | 0.867 | 0.026 | 0.22 | 4.56 |

A two-loop extrapolation (illustrative only) gives m_G a ≈ 6×10⁻³ at
β = 10, 2×10⁻⁵ at β = 15 and 4×10⁻¹³ at β = 30. The continuum limit is
β → ∞.

- **Distance.** The best rigorous window (SZZ, SU(3)) ends at g² ≈ 32. The
  numerically established scaling window begins at g² ≈ 1.05. That is a
  factor of 30 in the coupling, and nothing rigorous covers it. Beyond the
  window there are infinitely many further halvings of a.
- **Shape.** This is the structural reason no strong-coupling method can
  finish the job, however sharp its constants. Every strong-coupling bound
  gives a lattice-unit gap that is bounded below by an O(1) number, and the
  bound grows toward stronger coupling (`rigorous_bound_shape_D4`). The
  continuum requires the lattice-unit gap to go to zero, as
  m a ∝ a(β)Λ → 0, at exactly the rate set by asymptotic freedom. A bound
  m(β) ≥ m_0 > 0 holding uniformly along β → ∞ would force Δ = m/a → ∞: a
  trivial (ultralocal) limit, not Yang–Mills. What is needed is a
  *two-sided* control of m(β)/(a(β)Λ) across the crossover. A lower bound
  from strong coupling is the wrong shape of statement.

## 4. The framework, tested on its own terms

The premise tested here is that the framework supplies a structure the
standard approaches lack. That was tested directly.

1. **Field content.** The committed action is one shift-symmetric scalar,
   L = Λ⁴ f(K) (`deepseek_push/THE_THEORY.md`, Lemma 5), coupled to
   gravity. The framework's own scorecard reads: "No gauge sector, no
   Higgs, no QCD" (`deepseek_push/TOE_STATUS.md`, lines 89 and 131). The
   Clay theory's only field is the SU(3) connection, so the framework's
   equations do not contain the object of the theorem.
2. **Coupling.** If Yang–Mills is added to the framework, the committed
   action couples the two only through the metric. The relative effect on
   the gluon sector is of order (m_G/M_Pl)² ≈ 2.0×10⁻³⁸. That cannot
   create, remove or control an O(1) gap, and the prize's theory has no
   gravity at all.
3. **Scales.** The framework's scales are ħa₀/c = 2.6×10⁻³⁴ eV and
   ħH₀ = 1.4×10⁻³³ eV, while the glueball mass is 1.73 GeV, a ratio of
   about 10⁴². These are infrared scales, and the missing control is
   ultraviolet-to-infrared transport along asymptotic freedom. An infrared
   regulator built from them produces a gap that vanishes when the
   regulator is removed, and the prize requires removing it.
4. **Framework-internal gap mechanisms on the record.** None survives:
   - The eaten-Goldstone gap is U(1)-class. SU(3) needs a rank-8 mass
     matrix and the framework supplies rank ≤ 1
     (`deepseek_push/yang_mills_gap/YM_NONABELIAN.md`).
   - The I14 Hardy wall was killed for μ₂ (door H). `../ym3_hardy/` now
     shows its 1/4 is the Laplacian's Hardy constant, for every
     single-scalar action.
   - The keV-scale "pinned gap" of the 2026-09-17 campaign is self-anchored
     and excluded by the wave-32 audit
     (`fable_independent_2026/L261_wave32_audit.py`).

**Verdict on its own terms.** The framework contains no structure that
bears on the Yang–Mills continuum limit. This is not a judgement of the
framework's dark-sector physics. The two simply do not intersect.

## 5. The mathematical attempts, and where each breaks

- **Sharpen the strong-coupling constants.** This breaks on the structural
  mismatch in §3: any such method is capped at fixed spacing.
- **Use the new explicit Hamiltonian expansion as the infrared endpoint of
  a renormalisation-group flow.** This would need the flow to deliver an
  effective Kogut–Susskind Hamiltonian with g_eff² ≥ 185 and controlled
  remainders. Existing multiscale control (Balaban's ultraviolet stability
  for four-dimensional lattice Yang–Mills; Magnen–Rivasseau–Sénéor with an
  infrared cutoff) holds only while g_eff is small. Nothing controls
  g_eff² between about 1 and 185. That gap is precisely the crossover.
- **Monotonicity in β through correlation inequalities.** No Griffiths- or
  Ginibre-type inequality is known for non-abelian Wilson theory. Even if
  one were, it would give lattice-unit monotonicity, not the physical-unit
  ratio the prize requires.
- **Framework infrared scale as a regulator.** As item 3 of §4 shows, the
  resulting gap is regulator-dependent and vanishes in the required limit.

## 6. Status

D-YM2 remains world-open. The unlock is unchanged: a new analytic idea
that controls m(β)/(a(β)Λ) across the weak→strong crossover. This session
did not find one, and nothing in the repository or the framework supplies
one. Nothing here is a claim toward the Clay prize.
