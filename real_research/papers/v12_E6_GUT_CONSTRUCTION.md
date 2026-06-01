# The E6 Skyscraper: An Orbifold-GUT Construction on M₄ × (T²)³/(Z₂×Z₂)

**v12 particle-physics core · Draft, 2026-05-31**

A consolidated, honest writeup of the legitimate construction the framework reduces to once
the numerology is dropped. It is **TOE-unify** (a real action realizing the SM structure),
not TOE-derive (it does not predict the parameter values — those are moduli, as in every
string vacuum). Every claim is backed by a runnable script in `reviews/`.

---

## 1. The construction

- **Spacetime:** M₄ × K, K = (T²)³/(Z₂×Z₂), the SUSY-preserving (det = +1) orbifold; even
  internal dimension, so a genuine chiral index exists (`z2z2_three_generations.py`).
- **Gauge group:** **E₆** (the GUT whose **27** = one generation). Bulk Einstein–Yang–Mills–
  Dirac action (`v12_FORMAL_CORE_action.md`).
- **Breaking:** E₆ → SO(10)/trinification → SU(3)×SU(2)×U(1) via the Z₂×Z₂ shift vectors +
  Wilson lines.
- **Compactification scale:** Z² = 32π/3 as the volume modulus (an ansatz/input, not derived).

## 2. Matter: three generations

The three twisted sectors (one per internal 2-plane) give **3 × 27**. Under E₆ → SO(10),
27 = 16 + 10 + 1, and the **16 is exactly one SM generation** (Q, uᶜ, dᶜ, L, eᶜ, νᶜ),
verified component-by-component (`e6_orbifold_spectrum.py`). Net: **three chiral SM
generations** + vector-like exotics (the 10+1 per 27) to be lifted. The trinification split
27 = (3,3̄,1)+(1,3,3̄)+(3̄,1,3) matches the three 2-planes — "three from three planes," done
rigorously.

**Honest:** the generation number 3 = the chosen flux/orbifold, not forced (anomalies are
generation-blind; tadpoles allow many — `generation_number_tadpole_anomaly.py`).

## 3. Doublet–triplet splitting + proton decay (a real orbifold advantage)

The same Z₂ parity P = diag(−,−,−,+,+) that breaks SU(5) → SM gives the Higgs **doublet a
surviving zero mode (+) and projects the color triplet out (−)** — **DT splitting with no
10¹⁴ fine-tuning** (`e6_doublet_triplet.py`, Kawamura; Hall–Nomura). With no light triplet,
the **dimension-5 proton decay that excludes minimal 4D SUSY SU(5) is removed.** The residual
dim-6 mode predicts τ(p→e⁺π⁰) ~ 10³⁶ yr — above Super-K, a Hyper-K target.

This converts the proton-decay *tension* I raised earlier into a *resolved feature* of
building on the orbifold rather than in 4D.

## 4. Quantitative predictions (inherited SUSY-GUT successes)

All real, all standard, all **inherited** (any SUSY SO(10)/E₆ gives them — they are not
distinctive to this framework):

| Prediction | Result | Status |
|---|---|---|
| Gauge unification | M_GUT ~ 2×10¹⁶ GeV, α_GUT⁻¹ ~ 24 | works (SUSY) |
| sin²θ_W(M_Z) | **0.231** (1-loop 0.2309 vs 0.2312; honest level **~1%**) | `e6_gauge_unification`, `e6_two_loop_unification` |
| b–τ Yukawa unification | m_b/m_τ ~ 2.40 vs 2.35 (3rd gen) | `e6_gut_predictions.py` |
| Neutrino seesaw (νᶜ in 16) | m_ν ~ 0.01–0.1 eV (M_R ~ 10¹⁴⁻¹⁵) | works |
| Proton decay (dim-6) | τ ~ 6×10³⁵ yr (**∝ M_X⁴**, soft) | Hyper-K target · `e6_proton_lifetime` |

**Honest caveats now backed by computation (don't oversell row 2 and row 5):**
- The sin²θ_W "0.1%" is a **leading-log corner**. Adding 2-loop running + the SUSY
  threshold spreads the prediction by ~0.0038 — *larger* than the 0.0003 gap to the
  measured value. The defensible claim is "SUSY unification predicts sin²θ_W ≈ 0.231,
  confirmed at the **~1%** level," not a part-per-thousand hit (`e6_two_loop_unification.py`).
- The proton lifetime scales as **M_X⁴**: a factor 3 in the GUT scale swings τ by 81×
  (3.7×10³⁴ → 3.0×10³⁶ yr). "A Hyper-K target" is honest only at the *low* end of the
  GUT-scale range (`e6_proton_lifetime.py`).

## 5. Honest construction status

**Built (real):** the action; SM gauge group + 3 chiral generations; DT splitting; dim-5
proton-decay removal; gauge unification; sin²θ_W; b–τ; seesaw.

**Open (the hard parts, shared with all of string phenomenology):**
1. **Exotic-free vacuum** — lifting the vector-like 10+1 per 27 via explicit Wilson lines is
   the decades-hard model-building search (Faraggi et al.). `e6_wilson_exotic_lifting.py`
   proves the *simplest* tool (a single U(1)_ψ Wilson line) provably **cannot** do it — the
   16 has charge ±1, which generates the whole charge lattice, so any Wilson line that keeps
   the 16 keeps the exotics too. A real solution needs the full shift + multi-Wilson +
   flat-direction machinery under modular invariance: a search, not a formula.
2. **SUSY** — every headline prediction requires it; it is unseen at the LHC.
3. **Moduli stabilization** — the parameter *values* (masses, couplings, and Z² itself)
   are moduli-dependent and not derived. The landscape.

**Net:** a competent, legitimate **SUSY E₆ orbifold GUT** — real, standard-adjacent physics
with a genuine DT/proton-decay advantage. It earns legitimacy by *being* real physics. It is
**not** a theory of everything, it does not derive the constants, and its successes are
inherited rather than distinctive. The one *distinctive* claim of the wider framework lives
outside this skyscraper entirely: the evolving-a₀ cosmology (which needs none of it).

---

*Reproducibility: `reviews/{z2z2_three_generations, e6_orbifold_spectrum, e6_gauge_unification,
e6_two_loop_unification, e6_gut_predictions, e6_doublet_triplet, e6_proton_lifetime,
e6_wilson_exotic_lifting, generation_number_tadpole_anomaly}.py` and
`papers/v12_FORMAL_CORE_action.md`.*
