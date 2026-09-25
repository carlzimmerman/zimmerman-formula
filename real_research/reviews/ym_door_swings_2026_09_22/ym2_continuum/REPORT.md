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

---

## 7. Swing 2 (2026-09-25): the three routes §5 did not test

Script: `swing2_routes.py`. Output: `swing2_stdout.txt` and `swing2_results.json`. It runs four
computed checks, all of which pass; the lines marked `[RECORD]` are sourced statements, not checks. The door
stays shut.

- **R1: stochastic quantisation** (regularity structures, paracontrolled calculus). The stochastic
  Yang–Mills heat flow is subcritical in d = 2 and d = 3. Those are the dimensions of the
  Chandra–Chevyrev–Hairer–Shen constructions. In d = 4 it is **exactly critical**: both the A∂A and the
  A³ terms have margin 0 against the noise. Hairer's theory needs subcriticality, and no theory of
  critical singular SPDEs exists. In the critical scalar analogue, φ⁴₄ is trivial (Aizenman &
  Duminil-Copin 2021). This route is closed by a gap in the field, not a gap in this repository.
- **R2: analytic continuation of the strong-coupling series.** Drouffe & Zuber (1983, Phys. Rep. 102, 1,
  §3.4.3) place the roughening point at t_R = 0.40 ± 0.01 in d = 4, independent of the group. For
  SU(3) it falls at β = 5.8–5.9, inside the scaling window, which starts at β = 5.7. So surface
  observables such as Wilson loops and the string tension cannot be continued into the window; the
  authors themselves call roughening the stumbling block of strong-coupling methods. Bulk observables,
  such as the glueball mass, escape roughening. But continuing them needs two things:
  (i) analyticity on the whole real β-axis, which is not proved;
  (ii) the β → ∞ asymptotics m(β) ~ C·a(β)·Λ, which *is* the continuum problem.
- **R3: a renormalisation-group bridge.** Start at β = 6.0, where m_G·a = 0.78. Two block-spin steps
  (a factor of 4) bring the correlation length to 0.32 block spacings, which is strong-coupling-like.
  The missing control therefore spans only O(1) blocking steps in scale. What is missing is a *class*
  of estimate. The blocked measure is not a Wilson action, and no theorem places it inside any
  convergent-expansion or Dobrushin–Shlosman regime. Balaban's multiscale analysis controls blocked
  actions only while the effective coupling is small. A computer-assisted finite-box criterion is the
  one concrete attack. It would need rigorous integration over ~10⁴ SU(3) link variables, far beyond
  interval arithmetic today.
- **Literature, 2025–26.** One claimed complete proof exists: arXiv:2506.00284, a constructive proof of
  SU(3) existence and mass gap. arXiv's administrators **withdrew** it as below research-content
  standards. arXiv:2603.15770 (Douglas et al., 2026) formalises in Lean the free 4D field satisfying the
  Glimm–Jaffe axioms. That is useful infrastructure, not Yang–Mills.

**Verdict.** D-YM2 remains world-open. The sharpest statement this repository can make is that the
missing idea sits in O(1) block-spin steps between g² ≈ 1 and a strong-coupling-like correlation
length, and that it must be a non-perturbative estimate for a non-Wilson blocked measure. Nothing
here is progress toward the Clay prize.

---

## 8. Swing 3 (2026-09-25): the RG-bridge door, via Tomboulis's decimation route

Script: `swing3_rg_bridge.py`. Output: `swing3_stdout.txt` and `swing3_results.json`. It runs seven checks,
all of which pass; one is marked post hoc. The door stays shut.

**The prior attempt.** Tomboulis (arXiv:0707.2179) tried exactly this bridge for 4D SU(2). He compared the
lattice theory with a Migdal–Kadanoff-type ("MKT") decimation. At each step the plaquette weight is raised
to the power 4, and each character coefficient to the power 4r, with r = 1 − ε. The comparison was meant to
carry the decimation's flow to strong coupling back to the real theory, giving 't Hooft confinement at
every coupling. Ito & Seiler (arXiv:0711.4930, 0803.3019, 0901.4246) showed three gaps:

- (a) with r < 1 the flow goes to the weak-coupling fixed point above a critical coupling;
- (b) the interpolation parameter α* is only shown to exist locally (a counterexample exists);
- (c) the fundamental one: at r = 1 the 4D decimation drives U(1) to strong coupling as well (Ito 1985).
  But the 4D U(1) theory deconfines at weak coupling (Guth 1980; Fröhlich–Spencer 1982). So any
  comparison that ignores the nonabelian structure must fail.

**Reproduced here.** The decimation is computed exactly in character space; it is exact on the
corresponding hierarchical lattice. The quadrature matches the Wilson coefficients to 3e-16.

- At r = 0.9, SU(2) has a critical coupling at β = 2.399 in the convention f = exp(β cos θ). That is
  exactly half of Ito–Seiler's 4.795, consistent with a factor-2 difference in coupling normalisation.
  This comparison is post hoc. Their text also states the flow directions the other way round; this
  is recorded, not fitted.
- At r = 1, SU(2) drifts toward strong coupling at −0.26 to −0.29 per step, the decimation's shadow of
  asymptotic freedom. U(1)'s drift is 10⁻¹¹ to 10⁻¹⁵, too small to resolve numerically. That is Ito's
  flow, with a sign that only his theorem fixes.

**Tested here: a vanishing margin.** Ito–Seiler report that Tomboulis hinted orally at an n-dependent r,
without saying how. The concrete schedule r_n = 1 − a/(n + n₀) was tested.

- **Scalar model.** Take β_{n+1} = β_n/r_n − c. For 0 < a ≤ 1, Σ_n Π_k r_k diverges, so any drift c > 0
  eventually wins. For a > 1 the sum converges.
- **SU(2).** With a = 0.5 and a = 0.75, SU(2) reaches strong coupling from every tested β (4, 16 and 64),
  within 15–27% of the scalar model's step count.
- **U(1).** With a = 0.5, U(1) from β ≥ 8 follows the drift-free growth to within 1% over 2,500 steps,
  with no turnaround.
- **Finding.** In the hierarchical model, a margin that shrinks like a/n separates SU(2) from U(1). SU(2)
  confines at every tested coupling while U(1) keeps growing at weak coupling. Ito–Seiler showed that
  fixed-r decimations cannot do this.

**Why the door stays shut.**

1. Tomboulis's comparison inequality needs r bounded away from 1. A margin ε_n = a/n violates that, and
   no one has shown that such an inequality survives a vanishing margin.
2. Gap (b), the interpolation parameter, is still unproved.
3. Even if both were closed, the result would be confinement in the lattice sense ('t Hooft string
   tension) at every bare coupling for SU(2). That is a major lattice theorem, but it is not the
   continuum mass gap the Clay problem asks for.

The sharpest open question this repository can pose on the bridge is: *does a Tomboulis-type comparison
inequality hold with margin ε_n = a/n, 0 < a ≤ 1?* Nothing here is progress toward the Clay prize.
