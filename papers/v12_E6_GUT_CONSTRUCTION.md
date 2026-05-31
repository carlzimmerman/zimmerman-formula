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
| sin²θ_W(M_Z) | **0.2309** vs measured 0.2312 (0.1%) | `e6_gauge_unification.py` |
| b–τ Yukawa unification | m_b/m_τ ~ 2.40 vs 2.35 (3rd gen) | `e6_gut_predictions.py` |
| Neutrino seesaw (νᶜ in 16) | m_ν ~ 0.01–0.1 eV (M_R ~ 10¹⁴⁻¹⁵) | works |
| Proton decay (dim-6) | τ ~ 10³⁶ yr | Hyper-K target |

## 5. Honest construction status

**Built (real):** the action; SM gauge group + 3 chiral generations; DT splitting; dim-5
proton-decay removal; gauge unification; sin²θ_W; b–τ; seesaw.

**Open (the hard parts, shared with all of string phenomenology):**
1. **Exotic-free vacuum** — lifting the vector-like 10+1 per 27 via explicit Wilson lines is
   the decades-hard model-building search (Faraggi et al.).
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
e6_gut_predictions, e6_doublet_triplet, generation_number_tadpole_anomaly}.py` and
`papers/v12_FORMAL_CORE_action.md`.*
