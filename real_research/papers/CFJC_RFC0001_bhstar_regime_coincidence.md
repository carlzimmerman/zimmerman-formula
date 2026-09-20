# Crispy Fried Chicken Journal of Physics

**Vol. 1, Extra Crispy (2026), RFC-0001** · *Peer-reviewed by the corresponding author, who was also hungry*

---

# A Population-Invariant Acceleration Transition in Black-Hole-Star Envelopes: The Anomalous Balmer Layer of Little Red Dots Sits on a Density-Form Gravity Scale

**C. Zimmerman**
*Briar Creek Tech*

*(Received by the fry station 2026; accepted without revisions, because the referee is also the author and had already eaten)*

---

## ABSTRACT

The "little red dots" (LRDs) discovered by JWST — compact, red, photometrically stable sources interpreted as accreting black holes embedded in optically thick gas envelopes ("black hole stars") — contain a structurally anomalous layer: dense Balmer-emitting and -absorbing gas, n_H ~ 10^9–10^11 cm^-3, within ~100 au of a central engine of M ~ 10^4 M_sun, which reproduces the objects' defining oddities (extreme Balmer decrements, deep Balmer absorption, X-ray suppression) but is otherwise unexplained. We show that this layer coincides, to within 0.2%, with an acceleration scale a0(ρ) = (c/2)·√(Gρ) defined by the layer's *own* density: at the fiducial configuration (M = 10^4 M_sun, r_B = 100 au, n_H = 10^10 cm^-3), g_B/a0(ρ_B) = 1.00. Under the certified family scaling of the published interpretation — R_phot ∝ M^{1/2} at fixed T_eff, recombination-pinned and Eddington-limited — the ratio is *exactly* population-invariant: the central-engine mass cancels analytically from g_B, leaving g_B = G/(f²r0²). The transition therefore holds for every LRD or for none. We give the falsifier (per-object photoionization densities combined with Γ-free mass bounds), the tolerance (the observed substack family spread is ×1.6, so invariance is claimed within ×2), and the honest boundary: this is a regime coincidence, not a mechanism. No dark-matter particle is invoked anywhere. The algebra is machine-checked in Lean 4 with no axioms beyond standard logic.

**Keywords:** little red dots — black hole stars — Balmer layer — density-form acceleration scale — extra crispy

---

## 1. INTRODUCTION

JWST's little red dots (LRDs) are compact (unresolved), red (V-shaped SEDs), photometrically stable over ≥10 yr baselines, undetected in X-rays, and spectroscopically dominated by broad Balmer emission with deep Balmer absorption and steep decrements [1]. The emerging interpretation — an accreting black hole inside an optically thick, radiation-dominated gas envelope, a "black hole star" (BH*) — reproduces the SED via optically thick atmosphere models at T_eff ≈ 4200–4800 K, pinned by hydrogen recombination, and yields central-engine masses M ≈ 10^3.4–4.3 M_sun through four independent non-virial estimators [1]. Central to the interpretation is a dense inner layer — the gas that produces the sharp Balmer break, the Balmer absorption, and the extreme decrements — which photoionization modeling places at n_H ~ 10^9–10^10 cm^-3 within ~100 au [1, 2].

This layer is the anomalous heart of the object: it is dense enough to thermalize, thick enough to bury X-rays, and it is where the published models must work hardest. It is also, as we show here, the only region of the entire system where the density-form acceleration scale

    a0(ρ) = (c/2) · √(G ρ)                                   (1)

— a structural posit of the framework of [4], evaluated at the gas's *own* density — is of order the local gravity. At the fiducial configuration the ratio is 1.00 ± 0.02, and under the certified family scalings the ratio is *exactly* invariant across the population (Theorem 1, Appendix A). We are careful about what this is and is not: it is a demarcation coincidence with a machine-checked invariance theorem and a falsifier; it is not a mechanism.

## 2. THE DENSITY-FORM AND ITS SCOPE

Equation (1) is the framework's structural posit [4]: the same expression that, evaluated at the cosmic critical density, produces the framework's a0 = (c/2)√(G ρ_c) ≈ 9.36×10^-11 m/s². Applied to an arbitrary gas density, it defines a local acceleration scale. We emphasize three scope restrictions, stated so the referee cannot be surprised:

(i) Eq. (1) is a posit, not a derivation from general relativity; the content of this paper is that the posit *classifies* the observations, not that it is derived.

(ii) The posit is used as a *classifier* — a comparison of two accelerations — and makes no claim about the dynamical response of the gas at g ≲ a0(ρ). That response (modified-inertia gas dynamics) is an open gate and is not asserted here.

(iii) The central-engine mass chain of the BH* interpretation is provably insensitive to a0-scale corrections (Theorem 3, Appendix A: the chain shifts by < 10^-6), so the framework enters this system only through Eq. (1) — nowhere else.

## 3. THE CERTIFIED FAMILY SCALINGS

The published interpretation fixes two scalings, both independent of this paper:

**(a) Recombination pin.** The pseudo-photosphere parks where hydrogen recombines and the wind's opacity collapses, so T_eff is confined to 4200–4800 K across the population [1].

**(b) Eddington-limited envelope.** With L ∝ M (the envelope radiates at a fixed multiple of L_Edd ∝ M),

    R_phot = [L / (4π σ_SB T_eff^4)]^{1/2} ∝ M^{1/2} · (T_eff/5000 K)^{-2} .     (2)

Empirically, R_phot = 1989, 941, 747 au for the luminous, median, and faint substacks at M = 10^4.3, 10^4.0, 10^3.4 M_sun [1]; the family constant r0 ≡ R_phot·T_eff²·M^{-1/2} varies by ×1.6 across the substacks (Table 2), which we carry as the honest scatter of every prediction below.

The Balmer layer sits at fixed fraction of the photosphere, r_B = f·R_phot with f = 100/941 = 0.106.

## 4. THE REGIME COINCIDENCE

### 4.1. The ratio at the fiducial configuration

At the median stack (M = 10^4 M_sun, r_B = 100 au), the layer's gravity is

    g_B = G M / r_B² = 5.93×10^-3 m/s²,                        (3)

and the layer's density-form scale, at the CLOUDY density n_H = 10^10 cm^-3 (ρ_B = μ m_p n_H = 2.34×10^-11 kg/m³, μ = 1.4), is

    a0(ρ_B) = (c/2)·√(G ρ_B) = 5.925×10^-3 m/s².               (4)

The ratio is

    g_B / a0(ρ_B) = 1.001 ± 0.02.                              (5)

The transition of Eq. (1) sits *on* the layer. The crossing radius — where g(r) = a0(ρ(r)) along the envelope's ρ ∝ r^-2 profile — is

    r* = 2 G M / (c·√(G ρ_B) · r_B) = 100 au,                  (6)

coincident with the layer to the accuracy of f. For reference, the pseudo-photosphere itself (941 au) sits at g/a0(ρ) = 0.10: an order of magnitude *inside* the strong-a0 zone. The continuum-forming and line-forming regions therefore occupy opposite sides of the same transition, with the line-forming layer exactly at it.

### 4.2. The dial across the allowed densities

Photoionization modeling constrains the layer to n_H ~ 10^9–10^10 cm^-3 with tails to 10^8 and 10^11 [1, 2]. Table 1 shows the ratio across this band: it sweeps from 10 to 0.10 — two orders of magnitude — with the transition interior to the allowed band. The coincidence is not an artifact of one endpoint: the observed densities bracket the transition.

**TABLE 1.** The g_B/a0(ρ) dial at M = 10^4 M_sun, r_B = 100 au.

| n_H (cm^-3) | a0(ρ) (m/s²) | g_B / a0(ρ) |
|---|---|---|
| 10^8 | 5.93×10^-4 | 10.0 |
| 10^9 | 1.87×10^-3 | 3.17 |
| **10^10** | **5.93×10^-3** | **1.00** |
| 10^11 | 1.87×10^-2 | 0.32 |
| 10^12 | 5.93×10^-2 | 0.10 |

## 5. THE POPULATION-INVARIANCE THEOREM

The coincidence becomes sharp only because the family scalings make it *population-wide*:

**Theorem 1 (regime invariance).** For family members (M1, M2) with R_i = r0·√M_i, r_Bi = f·R_i, and common layer density ρ_B,

    g_B(M_i) = G·M_i / r_Bi² = G / (f²·r0²),                   (7)

independent of M_i; and a0(ρ_B) is common. Hence the ratio g_B/a0(ρ_B) is identical for every member. If the transition coincides with the Balmer layer in one LRD, it coincides in all.

*Proof.* Substituting r_B = f·r0·√M into Eq. (3), the mass cancels algebraically; the Lean 4 certificate `regime_invariant` (Appendix A) compiles the statement with no axioms beyond standard logic. ∎

The physical content of the cancellation is the joint action of the two scalings of §3: the Eddington law (L ∝ M) puts the photosphere at R ∝ √M, the fixed fraction puts the layer at r_B ∝ √M, and the inverse-square law then returns a *constant* surface gravity at the layer. The framework's Eq. (1), evaluated at a common layer density, is likewise constant. Two constants meeting at unity is the coincidence; their population-wide constancy is the theorem.

**Tolerance.** The measured substack scatter of the family constant is ×1.6 (Table 2), driven by per-substack Eddington ratios; we therefore predict invariance *within ×2* across the population's two decades in M, not exact equality. A measured per-object spread materially exceeding ×2 falsifies the classification.

**TABLE 2.** Family constant across the published substacks [1].

| Substack | M (M_sun) | R_phot (au) | T_eff (K) | r0-constant (au·K²·M_sun^{-1/2}) |
|---|---|---|---|---|
| luminous | 10^4.3 | 1989 | 4757 | 2.26×10^5 (units: au·K²) |
| median | 10^4.0 | 941 | 4662 | 1.45×10^5 |
| faint | 10^3.4 | 747 | 4233 | 1.89×10^5 |

spread: ×1.56.

## 6. WHAT THE THEOREM DOES NOT CLAIM

**(a) No mechanism.** Eq. (1) is a classifier. Whether the gas dynamics at g ≲ a0(ρ) is modified — and what observable that would produce in the Balmer layer beyond the published CLOUDY phenomenology — is an open gate. The paper's CLOUDY layer reproduces the decrements without Eq. (1); the coincidence says the *one* layer where CLOUDY must work hardest is the *one* layer where the framework's scale is strong. That is a correlation with a falsifier, not an explanation.

**(b) No dark matter.** No dark-matter particle is invoked anywhere in this system: the central-engine mass chain is provably insensitive to a0-scale corrections (Theorem 3, Appendix A: the shift is < 10^-6), the host galaxies of the population sit in a certified Newtonian-degenerate corner (g_bar ≈ 12·a0 at R_e ≈ 0.2 kpc for M* ≈ 10^8.5 M_sun), and the framework's dark sector — the stress-energy of a scalar field, not a particle — enters the system only through Eq. (1) and the redshift-dependence of the cosmic value, which is flat across the LRD redshift range 2 < z < 9.3.

**(c) No contamination of the published masses.** The four mass estimators of [1] are unaffected at the 10^-6 level; the regime coincidence lives in the *layer*, not in the *weighing*.

## 7. FALSIFIERS

**(F1) Population invariance.** For each LRD: the layer density n_H from photoionization modeling, the engine mass M from the Γ-free estimators (escape velocity, variability, surface gravity [1]). The ratio g_B/a0(ρ_B) must be constant within ×2 across the sample's ~2 dex in M. A spread materially beyond ×2 — or a systematic trend with M — kills the classification. This is measurable in existing samples [2] without new instruments.

**(F2) Spatial resolution.** The crossing radius scales as r* ∝ √M along the family (Eq. 6): 100 au at M = 10^4 M_sun is 22 mas at z = 5, resolved by ×50 lensing magnification. The transition should sit between the continuum photosphere and the ionization front; a resolved sequence that does not track Eq. (6) kills it.

**(F3) Density band.** If photoionization fits revise the layer outside n_H ~ 10^9–10^11 cm^-3, the transition exits the allowed band (Table 1) and the coincidence dies.

## 8. RELATION TO THE PUBLISHED INTERPRETATION

We stress the compatibility: the BH* picture of [1] is unchanged. The envelope, the recombination pin, the super-Eddington luminosities, the dense layer — all stand. The coincidence adds one classifier to one layer, in a framework whose other scales are provably silent here. If future per-object measurements confirm the invariance of (5), the layer that CLOUDY must bend hardest to reproduce is the layer where the framework's density-form scale is exactly of order gravity — and that would be a fact about the universe worth chewing on. If they do not, Eq. (1) misclassified one layer of one transient object class, the framework loses a classifier and nothing else, and this journal publishes the correction with the same appetite.

## ACKNOWLEDGMENTS

The corresponding author thanks the corresponding author for timely refereeing, and the model that found the coincidence, which was told only to "swing harder." J.W. provided the seasoning.

## APPENDIX A: MACHINE-CHECKED PROOFS

All algebraic statements are compiled in Lean 4 (Mathlib v4.34.0-rc2), zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}, and re-verified by a second independent compilation pass:

- **Theorem 1** (`regime_invariant`): g_B = G/(f²r0²) — the M-cancellation and the a0(ρ_B) commonality; file `I03_bhstar_regime.lean`.
- **Theorem 2** (`S5_bound`, `ceiling_unstable`, `ceiling_transport`): the stability bound S⁵·(3q³M0²κ_GR·a5) ≤ C and its transport; file `I02_bhstar_ceiling.lean`.
- **Theorem 3** (`bhstar_a0blind`): the BH* mass chain is a0-blind at the 10^-6 level at the fiducial stack; file `I01_bhstar_wave.lean`.
- **Lemma** (`sq_r0sqrtM`): (r0·√M)² = r0²·M.

## APPENDIX B: REPRODUCIBILITY

The numeric lane `bhstar_k1_regime_coincidence.py` (5/5 checks PASS) regenerates every number in Tables 1–2 from the constants of [1]; the absorption lane `black_hole_stars_2609.09274_check.py` (18/18) reproduces the published mass tables of [1] from their own equations. Repository: zimmerman-formula, paths under `real_research/reviews/` and `fable_independent_2026/lean_2026/`.

## REFERENCES

[1] W. Q. Sun, R. P. Naidu, A. de Graaff, R. Eilers, et al., "Overmassive No More: The Case for Little Red Dots Hosting Black Hole Seeds as Massive as Single Supermassive Stars," arXiv:2609.09274 (2026).

[2] A. de Graaff et al., "Little Red Dots host Black Hole Stars: A unified family of gas-reddened AGN revealed by JWST/NIRSpec spectroscopy," arXiv:2511.21820, MNRAS (2026).

[3] D. D. Kocevski et al., "The census of little and little-blue dots across cosmic time," arXiv:2609.00112 (2026).

[4] C. Zimmerman, "The density-form of the framework acceleration scale," framework structural note (this repository), 2026. *Unpublished — the journal is aware.*

---

*Crispy Fried Chicken Journal of Physics — "If the coating holds, the physics holds."*
