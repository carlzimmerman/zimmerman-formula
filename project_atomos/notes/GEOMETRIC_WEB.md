# GEOMETRIC_WEB — how particle physics constrains ITSELF geometrically

*The self-constraining web. Built per Carl's refinement (2026-06-25): BEFORE brute-forcing more, map how the SM
constrains itself geometrically and use the web to REDUCE the search space, then brute-force WITHIN it. The discipline is
the a₀ lesson applied as a METHOD, not a bridge: a₀ = c²√(Λ/32π) showed a physical scale can be pinned by FORCED
GEOMETRIC FACTORS — √(8π/3) = √(8π)[Einstein field-eq measure] × √(1/3)[Friedmann/FRW geometry], written down BEFORE any
fit. We transfer the METHOD: build the particle search ONLY from forced-geometric primitives (rep dimensions, |G|,
root-system angles, Dynkin indices, measure factors, small integers from spatial/rep dimensions, discrete-group
invariants). We DO NOT inject a₀/Z/ρ_c — that regenerates the 164 FDR-dead re-labelings and INFLATES the space.
Restricting to forced primitives is what REDUCES it: a sparser reachable set means a hit carries real bits.*

**Machine-readable companion:** `targets/geometric_primitives.py` — the same primitives, interlocks, ledger, and hit-list
as named Python constants for the engine to consume as its constrained alphabet, with a `verify_primitives()` self-test
(21/21 sympy-exact checks pass, 2026-06-25).

**Same bar both ways.** Forced is labeled forced; free is labeled free. Where a relation is a near-miss (sin²θ_W running)
or a re-label of a real-but-underived puzzle (Koide), it is labeled as such — not dressed up as a win, not high-priested
away. There is NO forced bridge from cosmic density to SM masses (~60-order gap, corpus-confirmed); the MASS sector
likely lacks a forced kernel; the MIXING sector (CKM/PMNS) is where geometry genuinely lives — and the hit-list reflects
that.

---

## (a) The unified set of FORCED-GEOMETRIC PRIMITIVES — the reduced alphabet

52 forced primitives + 2 explicitly-free knobs. Each is pinned by a NAMED, pre-registered symmetry/geometry constraint
(the Gate-B provenance tag). A bare free integer is **not** in this pool; a representation dimension is, because it is
fixed by the group before any data. All numeric claims sympy-verified exact.

### Measure / geometry factors (the a₀-class — measure coefficients)
| primitive | value | forced by |
|---|---|---|
| π, 2π, 4π | — | circle / S² solid-angle measure |
| 8π | 25.13 | Einstein field-eq normalization (G_μν = 8πG T_μν). *Gravity-forced; listed but NOT a gauge building block.* |
| 4π/3 | 4.189 | unit 3-ball volume (the spatial dimension d=3) |

### Representation dimensions (forced by the gauge group; dim adj = N²−1 is a group identity)
| primitive | value | provenance |
|---|---|---|
| SU(3) fund / adj | 3 / 8 | color triplet / gluon octet |
| SU(2) fund / adj | 2 / 3 | weak doublet / W^a triplet |
| U(1) singlet | 1 | hypercharge |
| n_gen | 3 | generations (empirical counting fact — forced=fixed, not derived) |

### GUT embedding invariants (SU(5)/SO(10)/E₆ representation theory)
| primitive | value | provenance |
|---|---|---|
| dim SU(5) / SO(10) / E₆ | 24 / 45 / 78 | group dimensions |
| one generation | **15** (5̄+10) / **16** (spinor=15+ν_R) / **27** (16+10+1) | multiplet content |
| sin²θ_W tree (GUT) | **3/8** | Tr(T₃²)/Tr(Q²) = (1/2)/(4/3) over a complete 5̄; equiv (3/5)/((3/5)+1). **Rational-target — Gate-A value-exempt.** |
| GUT normalization | **5/3** | common Tr(T_a²); the SAME forced fact as 3/8 |
| Weyl orders \|W(A₄/D₅/E₆)\| | 120 / 1920 / 51840 | root systems A₄, D₅, E₆ |
| Coxeter numbers h | 5 / 8 / 12 | same root systems |

### Casimirs / Dynkin / β-coefficients (forced ratios that set the running)
| primitive | value | provenance |
|---|---|---|
| T(fund) | 1/2 | Dynkin index, every SU(N) |
| C₂(adj) | N (=3 SU3, =2 SU2) | adjoint Casimir |
| SM 1-loop β (GUT-norm U1) | (41/10, −19/6, −7) | rep-dim sums (gauge/ghost −11, −22/3; +4/3·n_gen; +Higgs) |
| (b₁−b₂)/(b₂−b₃) | 218/115 | forced β-coefficient ratio |

### Discrete flavor-group invariants (the legitimate Gate-B pool for FLAVOR)
| group | \|G\| | key irreps / polytope |
|---|---|---|
| S₃ | 6 | 2-dim irrep (the 1+2 democratic/doublet split hosting the Koide circulant) |
| A₄ (tetrahedral) | 12 | {1,1′,1″,**3**}; tetra 4 vert / 6 edge — the canonical TBM triplet |
| S₄ (octahedral/cube) | 24 | {1,1′,2,**3**,3′}; cube 8 vert / 12 edge |
| Δ(27) | 27 | 9 singlets + 3 + 3̄ |

### Koide / circulant geometry (sympy-exact; r=√2 is the FREE knob)
- **Q = 1/3 + r²/6**, sympy-exact, with √mₖ = M(1 + r·cos(2πk/3 + δ)) — and **independent of the phase δ** (dQ/dδ = 0).
  The **1/3 democratic floor** and **1/6 amplitude coefficient** are FORCED by S₃/Z₃ circulant algebra.
- **cos²(angle of √-mass vector to (1,1,1)) = 1/(3Q)**; at Q=2/3 → **cos² = 1/2 → φ = 45°** (a forced-given-Q trig
  identity). *Correction baked in: the democratic angle is cos²=1/2 (45°), NOT cos²=3/4 — that would be Q=4/9, not Koide.*
- **FREE:** r=√2 (Q=2/3 ⟺ r²=2) and δ=2/9 (Brannen, fit). These are the two unforced numbers — flagged FREE, not forced.

### Mixing-sector forced rationals (the TBM Clebsch values — where geometry lives)
| primitive | TBM value | measured | provenance |
|---|---|---|---|
| sin²θ₁₂ | **1/3** (35.26°) | 0.303 (33.41°) | A₄/S₄ Clebsch |
| sin²θ₂₃ | **1/2** (45°, maximal) | 0.572 (49.1°) | A₄/S₄ Clebsch + μ-τ symmetry |
| sin²θ₁₃ | **0** | 0.02203 (8.54°) | TBM — **θ₁₃ is the TBM-breaking angle** (killed exact TBM in 2012) |

---

## (b) The INTERLOCK GRAPH — which observables are tied by which geometry

Seven interlocks. Each is a declared geometric closure tying ≥2 observables (mode C1) or ≥3 constants (mode C2). Status is
the honest gate reading.

```
                         ┌─────────────────────────── GAUGE SECTOR ───────────────────────────┐
  anomaly cancellation  ─┤
  + Yukawa invariance    │  HYPERCHARGE ANOMALY CLOSURE          [C2 · PASS]
                         │    ties: y_Q,y_L,y_e,y_d,y_u,y_H  +  Q_proton=−Q_electron  +  [U(1)]³=0
                         │    0 free params · cubic anomaly AUTOMATICALLY zero (overdetermination signature)
                         │    → the gauge analogue of a₀'s overdetermined √(8π/3). Bits STRUCTURAL not numerical.
                         │
  SU(5)/SO(10) embedding ┤  MULTIPLET CLOSURE                    [C2 · PASS]
                         │    ties: matter content ↔ 3/8 trace ↔ charge quantization (15 = 1 generation)
                         │
                         │  GUT UNIFICATION → sin²θ_W            [C1 · NEAR-MISS]
                         └    ties: sin²θ_W ↔ α_em ↔ α_s ↔ α_GUT  (1 free: α_GUT)
                              3/8 forced; minimal-SM running → ~0.20 vs measured 0.231 (few-% MISS). Needs SUSY/thresholds.

                         ┌─────────────────────────── FLAVOR / MASS ──────────────────────────┐
  S₃/Z₃ circulant       ─┤  KOIDE Q=2/3 (leptons)               [C2 · REAL-PUZZLE-RE-LABELED]
                         │    ties: m_e, m_μ, m_τ  (0 free params)
                         │    Gate A PASS (random-triple null ~1-in-48k; density peak NOT at 2/3 → special lepton angle)
                         │    Gate C2 PASS (3 masses, 0 params)
                         │    Gate B FAIL: r=√2 appears in ONLY ONE forced place (need ≥2); full spectrum needs δ=2/9 (2nd free #).
                         └    CROSS-FERMION FALSIFIES a family-universal mechanism (Q_up=0.85, Q_down=0.73 ≠ 2/3) → lepton-specific.

                         ┌─────────────────────────── MIXING (where geometry lives) ──────────┐
  A₄/S₄ Clebsch         ─┤  TBM A₄ PATTERN                       [C1 · NEAR-MISS]
                         │    ties: θ₁₂, θ₂₃, θ₁₃ (PMNS)  (1 free: the breaking)
                         │    sin²θ₁₂≈1/3, sin²θ₂₃≈1/2 strikingly close; θ₁₃=8.54° is the STRUCTURED breaking.
                         │    → forced-pattern + structured perturbation = the signature the gate certifies. HIGHEST unsolved prior.
                         │
  down-quark texture     │  GST MASS-MIXING                      [C2 · COINCIDENCE-CANDIDATE]
                         │    ties: m_d, m_s, |V_us|   √(m_d/m_s)=0.2242 vs |V_us|=0.22501 (~0.4%, but m_d is [L] ±10%)
                         │    → mass↔mixing, the quark-sector Koide analogue, 0 free params. Gated by light-quark error.
                         │
  GUT-scale CKM↔PMNS     │  QUARK-LEPTON COMPLEMENTARITY         [C2 · COINCIDENCE-CANDIDATE]
                         └    ties: θ_C, θ₁₂^PMNS, θ₁₃^PMNS   θ_C+θ₁₂=46.41° vs 45° (~3%);  λ/√2=0.1591 vs sinθ₁₃=0.1485 (~7%)
                              → cross-sector CKM↔PMNS, the hardest to fake; the recurring 45°/(1/√2) theme.
```

**The recurring geometric theme (a family resemblance, NOT yet a forced interlock):** cos²=1/2 / 45° shows up in Koide
(√-mass at exactly 45° to the democratic axis), in atmospheric θ₂₃ (≈45–49°, maximal mixing), and in quark-lepton
complementarity (θ_C+θ₁₂ ≈ 45°). And 1/√2 appears in both r=√2 (Koide amplitude) and θ₁₃≈θ_C/√2. The web NOTES this
resemblance — but does not (yet) claim a single forced kernel behind it. That is exactly the kind of thing the gate must
either certify or kill, not assume.

---

## (c) FORCED vs FREE ledger — per sector

| sector | FORCED (geometric, pre-fit) | FREE (unforced) |
|---|---|---|
| **gauge** | rep dims (8,3,2,1); the ENTIRE hypercharge pattern up to 1 scale (anomaly+Yukawa, cubic automatic); electric-charge quantization; sin²θ_W tree=3/8 + the 5/3 normalization; Casimirs/Dynkin (T_fund=1/2, C₂_adj=N); β-coefficients (41/10,−19/6,−7) as rep-dim sums | the **3 gauge coupling VALUES** (α_em=1/137.036, α_s=0.1180, sin²θ_W(M_Z)=0.23122); whether a GUT exists; y_Q=1/6 is a free normalization convention |
| **gut** | all GUT rep dims (24,45,78; 15,16,27); Weyl orders (120,1920,51840); Coxeter (5,8,12); multiplet closure (15=1 gen) | α_GUT, M_GUT, whether a GUT is realized |
| **flavor_group** | \|G\| and irrep dims of S₃/A₄/S₄/Δ(27) (6,12,24,27; 2,3,3); polytope vertex/edge counts (4/6, 8/12) | WHICH group is realized; the breaking vevs/flavons |
| **koide** | circulant identity Q=1/3+r²/6 (δ-independent); the 1/3 floor + 1/6 amplitude coefficient; cos²=1/(3Q) angle identity (45° at Q=2/3) | the amplitude **r=√2** (one forced appearance → Gate-B FAIL); the phase **δ=2/9** (fit; the 2nd free number) |
| **mixing** | TBM Clebsch (sin²θ₁₂=1/3, sin²θ₂₃=1/2, sin²θ₁₃=0) IF A₄/S₄ realized; the 1/√2 & 45° factors in the complementarity targets | the measured deviations (θ₁₃=8.54° breaks TBM); δ_CP; which group + which breaking; the CKM O(1) coefficients A, ρ̄, η̄ (look fitted) |

**The honest summary of the ledger:** forced STRUCTURE is rich (the whole hypercharge pattern, every rep dimension, the
TBM Clebsch values, the Koide circulant); forced NUMBERS that aren't already-known small rationals are **absent** — the 3
coupling values, the Yukawa eigenvalue ratios, r=√2, δ_CP all remain free. This is the same asymmetry the corpus found:
gravity forced √(8π/3); the SM hands the *mass* sector no analogous forced kernel. The web's job is to point the search at
the few places where that asymmetry might NOT hold — the mixing sector.

---

## (d) RANKED HIT-LIST — where a gate-passing interlock most plausibly hides

Ranked by **prior that a forced-kernel/interlock is actually REAL** (not by ease). Mixing/PMNS first, per the charter:
"the MIXING sector is where geometry genuinely lives and a real interlock most plausibly hides."

1. **PMNS / TBM via A₄ (S₄, Δ(27)), with θ₁₃≈8.5° as the breaking.** ⭐ The most symmetry-FORCED *unsolved* sector.
   sin²θ₁₂≈1/3 and sin²θ₂₃≈1/2 are forced-pattern Clebsch values; the discrete-group hypotheses are tailor-made; the
   charter's "probably geometric" instinct points here. The forced-pattern + structured breaking is exactly the
   forced-kernel-plus-perturbation signature the gate is built to certify. **The search-space reduction matters most
   here:** restrict the alphabet to {A₄/S₄ orders & irrep dims, the 1/3 & 1/2 Clebsch rationals, the 1/√2 correction
   factor} and hunt the θ₁₃/δ_CP deviation WITHIN that web.

2. **GST mass-mixing √(m_d/m_s) ≈ |V_us|.** A clean mass↔mixing interlock, 0 free params; √(4.70/93.5)=0.2242 vs
   |V_us|=0.22501 (~0.4% — strikingly good). The quark-sector analogue of Koide; cross-sector = the gate's strongest
   class. **Gated by the light-quark [L] error** (m_d ±10%): the width of the target caps the claim — that caveat is
   load-bearing, not a footnote.

3. **Quark-lepton complementarity θ_C + θ₁₂^PMNS ≈ 45° and θ₁₃^PMNS ≈ θ_C/√2.** Cross-sector CKM↔PMNS, the hardest to
   fake. θ_C+θ₁₂=46.41° vs 45° (~3%); λ/√2=0.1591 vs sinθ₁₃=0.1485 (~7%). If real → a GUT-scale forced kernel tying the
   two mixing matrices. The gate must decide coincidence vs structure at the ~3–7% level (the recurring 45°/(1/√2) theme
   is suggestive but not yet certified).

**Plus the calibration positive (rank 4, not new): Koide Q=2/3 → can a FLAVOR SYMMETRY force r=√2?** The ONE proven
interlock (re-find + re-certify), then attack the open knob: r=√2 is unforced and the gravity spine provably can't supply
it (√(2/Z)=0.588 ≠ √2, corpus re-label-dead). Cross-fermion demands a lepton-specific ingredient. **And rank 5 (gauge):**
unification + sin²θ_W=3/8 — real structural hint, but minimal-SM running misses 0.231 by a few % (near-miss, needs SUSY).

---

## How the web REDUCES the search (the operational payoff)

The point of the web is not the catalog — it is the **constrained alphabet**. The engine should run the brute-force
search over `forced_pool()` (52 forced primitives) **not** over a kitchen sink of integers + a₀/Z. Concretely:

- **Anonymize, then search WITHIN a sector's web.** For PMNS: feed the engine the dimensionless PMNS observables with
  names stripped, and an alphabet restricted to {A₄/S₄ orders & irreps, 1/3, 1/2, 0, 1/√2, small ints from the triplet}.
  A hit on θ₁₃/δ_CP from that sparse pool carries real bits; a hit from the full germ pool does not.
- **The rational-target exception is enforced.** 12 primitives are tagged `rational_target_exempt` (3/8, 1/3, 1/2, 2/3,
  the β-rationals…). Gate A on their VALUE is uninformative — the gate must score their EVIDENCE (the trace identity, the
  random-triple null), never the number. This stops the engine from "discovering" 2/3 = 8/12 and calling it physics.
- **The free knobs are quarantined.** r=√2 and δ=2/9 are in `free_pool()`, never in `forced_pool()` — so the engine can't
  use the answer as a building block (the FDR-dead failure mode).

**Bottom line, both ways.** The web is genuinely rich on the FORCED-STRUCTURE side (hypercharge closure is a real,
overdetermined, sympy-exact geometric closure — the gauge analogue of a₀; the Koide circulant and TBM Clebsch are real
forced patterns). It is genuinely EMPTY on the forced-NUMBER side outside the already-known small rationals (no coupling
value, no Yukawa ratio, no r=√2, no δ_CP is forced). The mixing sector is the one place where a NEW forced number might be
hiding, and that is where the reduced search should spend its budget. We will certify a real interlock if it's there, and
report FDR-dead honestly if it isn't — same bar both directions.

*Provenance: all numeric claims sympy-verified exact 2026-06-25 (`geometric_primitives.verify_primitives()`, 21/21 OK).
Sector maps: `notes/SECTOR1_GAUGE_GEOMETRY.md` (gauge), `targets/SM_PARAMETERS.md` §1,§5,§6 (flavor/CKM/PMNS hooks +
ranked hit-list). Gate spec: `notes/GATE_SPEC.md`. PDG-2024-class values from `targets/pdg_constants.py`. Group theory
standard (SU(5)/SO(10)/E₆ reps, root systems A₄/D₅/E₆, A₄/S₄/Δ(27) flavor symmetry, Koide 1981 + circulant algebra).*
