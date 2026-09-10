# Relativistic MOND / modified gravity vs. the 12-gate set — state of the art

Compiled 2026-09-10. Every non-trivial entry carries an arXiv number or DOI.
**Convention used in this file: no personal names.** Theories are referred to by their
non-eponymous names and every source is identified by arXiv ID / DOI / journal reference
only. Nothing here is weakened by that — every claim is traceable to a numbered source.

**Verification standard applied.** Entries are marked `N-A` (not addressed) rather than
`FAIL` whenever I could not find a *published* calculation. A missing calculation is not a
failure, and saying so is the whole point of §5. Where I have done arithmetic myself it is
labelled `[my arithmetic]` and is not load-bearing.

---

## 0. The gate set and the observational numbers behind it

| Gate | Statement | Bound / source |
|---|---|---|
| G1 | no ghost, no gradient instability | theory-internal |
| G2 | constraint-algebra closure, correct DOF count | theory-internal |
| G3 | well-posed Cauchy problem, no superluminal signalling | theory-internal |
| G4 | c_T = c | −3×10⁻¹⁵ < c_gw/c − 1 < 7×10⁻¹⁶ [R47] |
| G5 | PPN γ = 1 | γ − 1 = (2.1 ± 2.3)×10⁻⁵ [R48] |
| G6 | PPN β, and α₁, α₂ | α̂₁ = (−0.4 +3.7/−3.1)×10⁻⁵ (95%) [R50]; \|α₂\| < 4×10⁻⁷ solar-spin [R49], \|α̂₂\| < 1.6×10⁻⁹ solitary pulsars [R51] |
| G7 | deep-MOND limit + BTFR + SPARC RAR | [R52], [R53] |
| G8 | CMB (esp. 3rd peak) + P(k) + σ₈ | [R2] for the only full RMOND fit |
| G9 | BBN | — |
| G10 | is a₀ derived or fitted? | — |
| G11 | lensing, cluster + galaxy scale | — |
| G12 | cluster residual (MOND leaves ≈ factor 2) | [R52] §6.6, [R53] |

---

## 1. The scoring table

`PASS` = published, explicit, positive result. `PART` = partial / qualified / contested.
`FAIL` = published negative result. `N-A` = not addressed anywhere I could find.
`UNK` = addressed but unresolved in print.

### 1a. Gates G1–G6 (theoretical health + Solar System)

| Theory | G1 ghost/grad | G2 algebra/DOF | G3 Cauchy/causal | G4 c_T=c | G5 γ=1 | G6 β, α₁, α₂ |
|---|---|---|---|---|---|---|
| **RAQUAL** (aquadratic Lagrangian) [R58] | UNK | N-A | **FAIL** — superluminal scalar [R1 §I; R52 §7.1] | PASS (conformal: same null cones) [R2] | N-A | N-A |
| **TeVeS** [R1] | **FAIL** — Schwarzschild-TeVeS linearly unstable at phenomenological parameters [R13] | N-A | **FAIL** — vector forms caustics / naked singularities before horizon formation [R14] | **FAIL** — excluded for all parameters [R12; stated also in R2] | PASS — γ = β = 1 [R15] | **FAIL/PART** — simple TeVeS: the vector-equation divergence locks φ₀ to K, which forbids cosmological evolution, so the case is set aside [R15]; Æther-TeVeS: α₁=α₂=0 solvable but only in a *narrow tuned* region (K₊ near 0.01) [R15] |
| **Generalized Einstein-aether** [R55] | UNK | N-A | UNK | **FAIL** for the MOND-relevant branch [R12] | PASS [R16] | PASS *by tuning* — α₁=α₂=0 requires c₄ = −c₃²/c₁ plus one more relation; "two parameters to spare" [R16] |
| **BIMOND** [R19] | **UNK/FAIL** — bimetric theories generically carry a Boulware–Deser ghost; not settled for BIMOND [R21] | N-A | UNK ([R20] raises super/subluminal GW and causality explicitly) | PASS — tensor GW speed = c in the studied formulations [R20] | N-A | N-A |
| **AeST** [R2] | **PART** — massive vector/scalar modes healthy and Hamiltonian bounded below, **but** a non-propagating mode with linear t-dependence has unbounded Hamiltonian for k < µ; authors argue µ ≲ Mpc⁻¹ makes it cosmological-scales-only [R3] | **PASS** — 4 first-class + 4 second-class constraints, **6 DOF nonlinearly** [R4] (vs 3 around Minkowski [R3] — background-dependent count, flagged by the authors themselves [R4 §I]) | UNK — no well-posedness proof published | PASS by construction (req. (v)) [R2] | **N-A** — no PPN computation published; [R5] only states "parametrically small post-Newtonian corrections" | **N-A** — α₁, α₂ have *never been computed in print* for AeST (see §5) |
| **Khronon (original foliation theory)** [R10] | PART — stationary MOND solutions stable to khronon perturbations for spherical/cylindrical/planar symmetry in the low-acceleration regime [R11]; instabilities exist in perturbations about flat spacetime [R11] | N-A | UNK | PASS (hypersurface-orthogonal aether; no extra tensor mode) [R10] | PASS [R10] | N-A |
| **Relativistic Khronon** [R8], **Khronon-Tensor** [R9] | **PART/FAIL** — ω² < 0 for √(1−α)k < µ. β=λ=0: mild (linear-in-t) instability, "harmless" per authors [R8 §5.1]. λ≠0: **exponential**, requiring Γ_max = µ√(λ/8) < H₀ [R8 §6.2] | **UNK** — 3 DOF on Minkowski asserted; full Hamiltonian analysis explicitly "left to future work" [R8 §6.2] | PART — third mode non-propagating for β=λ=0; luminal at high k in the λ=2α subcase [R8 eq. 6.8]; no well-posedness proof | **PASS** — "no propagating GW with helicity 0 or 1, so GW are the same as in GR" [R8 §7 item 4] (requires β = 0) | **PASS** (claimed) — "the same PPN limit as GR … viable in the Solar System and for binary pulsar tests" [R8 §3, verbatim] | **PASS (claimed, with a caveat)** — α₁ = −8(α−β)/(1−β) with β=0 and **α → 0 in the high-acceleration regime** [R8 eq. 6.6a + §3]. Caveat: α₂ (eq. 6.6b) has (β+λ) in the denominator and is **formally singular at β=λ=0**; a finite α₂ = 4α²/(1−α) is exhibited only in the λ=2α subcase, where α₁ = −8α and the α₁ bound then forces α ≲ 10⁻⁶ and µ ≲ 1000 H₀ [R8 §6.2] |
| **Superfluid dark matter** [R22] | PART — gravity is GR, but the superfluid EFT uses a non-analytic (X)^{3/2} kinetic term needing UV completion [R22] | PASS (GR sector) | PASS (GR sector) | PASS (GR) | PASS (GR) | PASS (GR) |
| **Dipolar dark matter** [R25], [R26] | **FAIL** — stability requires a postulated environment-dependent non-gravitational internal force [R26]; N-body simulations confirm the analytically predicted polarization instability, dissolving galaxies on cosmological timescales [R27] | N-A | UNK | PASS (GR tensor sector) | N-A | N-A |
| **Emergent (entropic) gravity** [R28] | N-A — no complete covariant theory; a candidate Lagrangian exists [R29] but its consistency was not established | N-A | N-A | N-A | N-A | N-A |
| **Gravitational self-interaction / GEFC** [R33] | N-A (claimed to be GR itself) | N/A | N/A | PASS (GR) | PASS (GR) | PASS (GR) |
| **Mimetic dark matter / mimetic MOND** [R36], [R38] | **FAIL** — Hamiltonian unbounded below where the mimetic energy density can run negative; plus caustic formation from the pressureless-dust nature [R37] | UNK | **FAIL** (caustics) [R37] | PASS | N-A | N-A |
| **Nonlocal metric MOND** [R40] | UNK (nonlocal — standard ghost analysis does not apply directly) | N-A | UNK | PASS by construction (metric-only, lensing built in) [R40] | N-A | N-A |
| **QUMOND / nonrelativistic Lagrangian family** [R43] | N/A (nonrelativistic) | N/A | N/A | N/A | N/A | N/A |
| **RMOND from modified entropic gravity** [R44] | N-A | N-A | N-A | N-A | N-A | N-A |

### 1b. Gates G7–G12 (phenomenology)

| Theory | G7 MOND/BTFR/RAR | G8 CMB + P(k) + σ₈ | G9 BBN | G10 a₀ derived? | G11 lensing | G12 clusters |
|---|---|---|---|---|---|---|
| **RAQUAL** | PASS by construction [R58] | N-A | N-A | **FAIL** (fitted) | **FAIL** — conformal coupling leaves null geodesics unchanged, so baryons cannot produce enough lensing [R2, verbatim] | FAIL [R52] |
| **TeVeS** | PASS by construction [R1] | **FAIL** — "ruled out by cosmic microwave background measurements from the Planck mission" [R18]. Earlier partial success: structure can grow [R17], driven by the *vector* perturbation, but the 3rd peak needed a ≈2 eV neutrino component | N-A | **FAIL** (fitted) | PASS — disformal coupling gives GR-strength lensing [R1] | **FAIL** — residual ≈ factor 2, patched with 2 eV neutrinos [R52 §6.6] |
| **Gen. Einstein-aether** | PART | PART — growth sourced by the new DOF [R55]; designer studies find Planck-compatible subclasses, but not a MOND-limited one | N-A | FAIL | PART | FAIL |
| **BIMOND** | PASS by construction [R19], [R21] | **N-A** — "A consistent model that complies with all the observations in cosmology … has not yet been presented" [R21] | N-A | FAIL | PASS (both metrics; lensing built in) [R19] | N-A |
| **AeST** | **PART** — MOND recovered only out to a finite radius r_C, beyond which the potential goes oscillatory [R5]; a weak-lensing analysis finds the predicted deviations from MOND are **not seen** in the data [R6] | **PASS** — the headline result: fits CMB and matter power spectra on linear scales [R2]; background phase-space analysis confirms a viable epoch sequence [R57]. **Contested**: [R45] argues the dynamic Lorentz-violating vector does not recover the faster MOND-regime growth and gives MOND only in the stationary limit | **N-A** — G̃ = (1 − K_B/2)Ĝ [R2] differs from the locally measured G, and no BBN bound on K_B has been published | **FAIL** (a₀ free) | PASS — Ψ = Φ by construction [R2] | **PART** — the oscillatory regime produces an RAR *peak* above MOND then a drop below, qualitatively like the observed cluster RAR, but "a full quantitative comparison … will require going beyond the isothermal case" [R7] |
| **Khronon (original)** [R10] | PASS for stationary systems; **order-unity corrections for non-stationary systems**, incl. MOND Kepler's third law [R11] | N-A | N-A | FAIL | **PASS** — "predicts the same gravitational lensing as general relativity but with a modified Poisson-type potential" [R10, verbatim] | N-A |
| **Relativistic Khronon / Khronon-Tensor** [R8], [R9] | **PART** — the authors' own restriction: MOND "with however the restriction to systems being stationary" [R8 §7 item 2] | **PASS (claimed)** — "it can be arbitrarily close to the Λ-CDM cosmological model at the level of linear cosmological perturbations, where it retrieves the full observed spectrum of CMB anisotropies" [R8 §7 item 5]. Authors also note the ΛCDM correspondence **breaks at second order** [R8 §7] | N-A | FAIL (free function J, a₀ input) | PASS (inherits [R10]) | N-A |
| **Superfluid DM** | **PART** — MOND-like phonon force only inside the superfluid core [R22]; galactic M/L and thermalization/fragmentation problems reported [doi:10.1051/0004-6361/202243216] | **PASS** — cosmologically it *is* CDM, so a⁻³ literally [R22] | PASS (particle DM) | FAIL | **PART/FAIL** — strong lensing of SLACS fits [R23]; **weak lensing at large radii in tension** because phonons do not deflect light [R24] | PART (superfluid phase ends, CDM-like outside) [R22] |
| **Dipolar DM** | PASS at galaxy scales [R25] | PART — recovers ΛCDM at cosmological scales by construction [R25], [R26]; Planck constrains the primordial dipole [R26] | N-A | FAIL | PART | N-A |
| **Emergent gravity** | PART — a₀-scale RAR emerges for isolated spherical systems only [R28] | **N-A** — no CMB calculation exists | N-A | **PART (the only candidate)** — a₀ tied to cH₀ via de Sitter entropy [R28], but the MOND derivation was shown not to be self-consistent, recovering Newtonian gravity when the averaging is done properly [R30] | PART — early weak-lensing test looked favourable [R31]; KiDS-1000 RAR analysis found ΛCDM favoured on reduced χ² and EG failing the colour dependence [R32] | N-A |
| **Self-interaction / GEFC** [R33] | **FAIL (contested)** — a direct nonlinear-GR calculation across several gauges and perturbation schemes found **no** flux-collapse phenomenon at next-to-leading order [R34]; gravitomagnetic effects are O(10⁻⁶) too small [R35] | N-A | N-A | PART (claimed to follow from GR) | N-A | N-A |
| **Mimetic DM / mimetic MOND** | PART — MOND-like law recoverable [R38] | **PASS trivially** — mimetic matter *is* exactly pressureless dust [R36] | N-A | FAIL | PART | N-A |
| **Nonlocal metric MOND** | PASS by construction, with sufficient lensing [R40] | **FAIL** — ΛCDM *expansion history* reproduced through BBN, recombination and most of Λ-domination [R41], but "the MOND enhancement is **not sufficient** to allow ordinary matter to drive structure formation" [R42, verbatim] | PASS (expansion history correct through BBN) [R41] | FAIL | PASS [R40] | N-A |
| **QUMOND** [R43] | PASS by construction | N/A | N/A | FAIL | N/A | FAIL (inherits MOND residual) [R52] |
| **RMOND from modified entropic gravity** [R44] | PART — fitted to one rotation curve (NGC 3198) [R44] | N-A | N-A | PART (a₀ from Unruh-temperature construction) [R44] | N-A | N-A |

---

## 2. THE KEY OUTPUT — which gate combinations have never been achieved

### 2.1 Does any published theory pass G6 (α₁) **and** G8 (CMB) simultaneously?

**Yes — one does, and it is architecturally very close to this programme's own branch.**

**Relativistic Khronon theory, JCAP 11 (2024) 040, arXiv:2404.06584 [R8]**, and its
successor Khronon-Tensor theory, arXiv:2507.00912 [R9], claim **both**:

- **G6.** *"In particular we conclude that the theory has the same parametrized
  post-Newtonian (PPN) limit as GR and is therefore viable in the Solar System and for
  binary pulsar tests; see eq. (6.6) where β = λ = 0, and with α = 0 in the high
  acceleration regime."* [R8 §3, verbatim]
  The mechanism is different from a cuscuton's: their Lorentz-violating coefficient α
  (the coefficient of Y = A_iA^i/c⁴ in the ADM Lagrangian) is **acceleration-dependent** —
  α = 1 in the deep-MOND regime, α → 0 in the Newtonian/high-acceleration regime,
  because J(Y) → Λ_∞ + O(a₀/y) there [R8 eq. 3.26]. So α₁ = −8α/(1) → 0 in the
  Solar System *asymptotically*, not identically.
- **G8.** *"it can be arbitrarily close to the Λ-CDM cosmological model at the level of
  linear cosmological perturbations, where it retrieves the full observed spectrum of CMB
  anisotropies (for a wide range of parameters λ_D and µ)"* [R8 §7 item 5, verbatim].

**This refutes the framing that "no published theory passes G6 and G8 together."** It must
be reported that way. But the pass comes with three documented qualifications, each of
which is in the paper itself:

1. **α₂ is formally undefined for their base theory.** Eq. (6.6b) carries (β+λ) in the
   denominator; at β = λ = 0 it is singular. A finite α₂ = 4α²/(1−α) is exhibited only in
   the λ = 2α subcase, and there α₁ = −8α with the observational bound forcing α ≲ 10⁻⁶
   and hence µ ≲ 1000 H₀ [R8 §6.2].
2. **G1 is not clean.** ω² < 0 for √(1−α)k < µ. For β = λ = 0 the growth is only linear in
   t (authors: "harmless"); for λ ≠ 0 it is **exponential**, and viability requires
   Γ_max = µ√(λ/8) < H₀ [R8 §6.2].
3. **G7 is restricted.** MOND holds only for **stationary** systems [R8 §7 item 2].
   Independently, [R11] finds order-unity corrections to MOND for non-stationary systems in
   this class (including a modified MOND Kepler third law relevant to wide binaries), and
   [R45] argues the MOND-regime growth enhancement is not recovered at all outside the
   stationary limit.

### 2.2 What is AeST's actual G6 status?

**Not "FAIL" — `NOT ADDRESSED`.** I could find **no published PPN calculation for AeST at
all**: not γ, not β, not α₁, not α₂. [R5] says only that post-Newtonian corrections are
"parametrically small". The Skordis-group publication list from 2021 onward contains the
PRL [R2], the Hamiltonian paper [R4], the quasistatic-solutions paper [R5] and the Khronon
paper [R8] — no PPN paper. This is a genuine hole in the literature, and it means the
programme's internal α₁ = −2(K_B + 2) result would be **the first published AeST PPN
number** if it is written up.

*[my arithmetic, not literature, offered only as an expectation check:]* the AeST vector
sector is a pure Maxwell term (K_B/2)F^{µν}F_{µν} [R2 eq. 5], which in Einstein-aether
variables is c₁ = −c₃; substituting into the published α₁ = −8(c₃² + c₁c₄)/(2c₁ − c₁² + c₃²)
[R16 eq. A.74] gives α₁ = −4c₁ ∝ −K_B, i.e. nonzero unless K_B → 0. This does **not**
settle AeST, because AeST also carries the 2(2−K_B)J^µ∇_µφ mixing term and the µ²Φ mass
term, neither of which is covered by [R16]. Treat as motivation for the calculation, not
as a result.

### 2.3 The combinations that genuinely have never been achieved

Stated as the tightest true frontier I can defend from the sources above:

| # | Combination | Status | Closest published attempt |
|---|---|---|---|
| **F1** | **G1 (clean, no IR instability) + G6 + G8** | **NEVER ACHIEVED** | [R8] passes G6+G8 but carries ω²<0 for k<µ; [R2] passes G8 but has an unbounded-Hamiltonian mode for k<µ [R3] and no G6 calculation. *Both* CMB-capable theories in the literature buy G8 with the same IR pathology, because both use the same ghost-condensate/dust mechanism. |
| **F2** | **G6 + G8 + a non-stationary MOND limit (full G7)** | **NEVER ACHIEVED** | [R8] restricts MOND to stationary systems by its own statement; [R11] and [R45] independently show the non-stationary sector is not MOND. |
| **F3** | **G8 by any mechanism other than an effective pressureless a⁻³ component** | **NEVER ACHIEVED** — see §3 | — |
| **F4** | **G2 (published full constraint algebra) + G6 + G8** | **NEVER ACHIEVED** | Only AeST has a published nonlinear Dirac analysis [R4]; it has no G6 calculation. The Khronon theory that has G6+G8 explicitly leaves the Hamiltonian analysis to future work [R8 §6.2]. |
| **F5** | **G10 (a₀ derived) + any healthy covariant action** | **NEVER ACHIEVED** | Only [R28] claims a derivation (a₀ ~ cH₀ from de Sitter entropy); it has no covariant theory, and its MOND derivation was shown not to be self-consistent [R30]. Every theory in §1 that passes G1–G6 takes a₀ as input. |
| **F6** | **G12 (cluster residual removed) without adding a cold component** | **NEVER ACHIEVED** | [R7] is the only structural mechanism proposed (AeST's oscillatory RAR peak) and is explicitly not yet quantitative. Every other RMOND either inherits the factor ≈2 [R52], [R53] or patches it with neutrinos [R18]. |
| **F7** | **G3 (published well-posedness/causality proof) for any RMOND that passes G7+G8** | **NEVER ACHIEVED** | No Cauchy well-posedness result is published for AeST or for the Khronon theories. RAQUAL failed on superluminality [R1 §I], TeVeS on caustics [R14], mimetic on caustics [R37]. |

**The single sharpest statement for the programme:** the frontier is not the *pair*
(G6, G8) — that pair was closed in 2024 by [R8]. The frontier is the *triple*
**(G1-clean, G6, G8)** and the *quadruple* **(G1-clean, G2-published, G6, G8)**, and,
orthogonally, **(G8 without a⁻³ dust)**.

---

## 3. Mechanisms for driving the third acoustic peak — and the classification

For each theory that has actually produced a CMB spectrum, in one sentence:

| Theory | Mechanism, one sentence | Class |
|---|---|---|
| **AeST** [R2] | A shift-symmetric k-essence with K(Q) = −2Λ + K₂(Q − Q₀)² + … sits at a nonzero minimum, so integrating its field equation gives dK/dQ = I₀/a³ and hence **ρ̄ = ρ̄₀/a³ + …**, an exactly dust-like background component that clusters and drives the potential wells. | **A** |
| **Relativistic Khronon** [R8] | The Khronon's K(Q) = µ²(Q−1)² is expandable about Q = 1, giving approximate dust solutions; at linear order the field's stress tensor **maps onto the Generalized Dark Matter fluid** with c²_vis = 0, a k-dependent c²_s, and w̃₀ ~ a³ — i.e. a dust with a small sound speed. | **A** |
| **Mimetic dark matter** [R36] | The conformal mode is made dynamical by a constraint and **is exactly pressureless dust**; [R39] shows any RMOND with a unit-timelike vector (TeVeS, AeST) can be recast in this mimetic/conformal-disformal-invariant form, so the whole family is one mechanism. | **A** |
| **Superfluid dark matter** [R22] | It is literally particle dark matter (eV-scale, strongly self-interacting) that is **CDM cosmologically** and only condenses to a MOND-mediating superfluid inside galaxies. | **A** |
| **Dipolar dark matter** [R25], [R26] | A polarizable dipolar medium whose background energy density **reduces to ΛCDM's dust plus Λ** at cosmological scales by construction. | **A** |
| **TeVeS** [R17] | Growth is sourced by the **vector-field perturbation**, whose growing mode feeds the metric potentials and can raise the third peak; this is a genuinely non-dust mechanism, but it was **never sufficient on its own** — the fits required a massive (≈2 eV) neutrino component, and the theory was subsequently ruled out by Planck [R18]. | **B (failed)** |
| **Generalized Einstein-aether** [R55] | Same class: growth sourced by the new vector degrees of freedom in a dynamical preferred frame. | **B (failed)** |
| **Nonlocal metric MOND** [R41], [R42] | The nonlocal free function is tuned to reproduce the **expansion history** including BBN and recombination, with no new component; explicitly **fails** to drive structure formation [R42]. | **C (failed)** |

### The answer to the question behind §3

**No. There is no published mechanism other than an effective pressureless a⁻³
clustering component that has ever been made to work on the CMB.**

- Class **A** (effective/actual a⁻³ dust) contains **every** success: [R2], [R8], [R36],
  [R22], [R25].
- Class **B** (Lorentz-violating vector perturbation growth) is the only genuinely
  distinct mechanism ever demonstrated to produce growth [R17], and it never fit the
  third peak without an extra real a⁻³ component (massive neutrinos); its host theory is
  now excluded by Planck [R18], and [R45] argues the vector's dynamical nature blocks
  the MOND growth enhancement entirely.
- Class **C** (nonlocal expansion-history matching) reproduces the background but is
  explicitly stated by its own authors to fail structure formation [R42].
- Class **D** (entropic/emergent, self-interaction) has **never produced a CMB spectrum
  at all** — no calculation exists.

This is the strongest single result in this map for the programme's purposes: the a⁻³
requirement is not a fashion, it is the *only* thing anyone has ever made work, and the
IR instability in F1 is the price both working constructions pay for it.

---

## 4. Results that would refute, and results that would support, this programme

### Would REFUTE (take these seriously; reproduce before contradicting)

1. **[R8] / [R9] — arXiv:2404.06584, arXiv:2507.00912.** A *foliation-clock* theory —
   the same architectural family as the programme's cuscuton-clock branch — that claims
   α₁ = α₂ = 0 in the Solar System **and** the full CMB spectrum. If the programme's
   position is "our branch passes G6 but fails G8, and nobody has both," that position is
   wrong as stated. The programme's real differentiators are (a) exactness of α₁ = 0 at
   *all* accelerations vs. their asymptotic α → 0, and (b) whatever it can say about the
   k < µ instability that they cannot.
2. **[R11] — doi:10.3847/1538-4357/ad003d (ApJ 958, 129, 2023).** Khronometric MOND has a
   consistent slow-motion limit and its stationary deep-MOND solutions are **stable** to
   khronon perturbations for spherical, cylindrical and planar symmetry. This is a direct
   published counter to any blanket "khronometric/foliation MOND is gradient-unstable"
   claim, and it is exactly the kind of result the 09-09 PAPER8 retraction should be
   checked against.
3. **[R7] — arXiv:2312.00889 (JCAP 04 (2024) 040).** AeST's µ-dominated oscillatory
   regime produces an RAR that peaks *above* MOND and then falls *below* it (as if a
   negative mass density), which the authors note resembles the reported cluster RAR.
   This is a live, published, dust-free mechanism for the cluster residual, and it is a
   direct challenge to "only cold DM satisfies all four cluster constraints."
4. **[R39] — arXiv:2503.11174 (JCAP 06 (2025) 059).** Any relativistic MOND with a
   unit-timelike vector can be embedded in a conformal/disformal-invariant mimetic
   framework. If correct, the programme's "mimetic/projectable dust gives no MOND source"
   conclusion needs re-testing on their embedding, not on the programme's own.
5. **[R34] — arXiv:2303.11094** is a refutation *of a rival* (GEFC), but it is also a
   methodological warning: a scalar-approximation argument survived for a decade before a
   direct nonlinear-GR calculation across multiple gauges killed it.

### Would SUPPORT

1. **[R3] — arXiv:2109.13287 (PRD 106, 104041).** AeST's own stability paper: a
   non-propagating mode with linear time dependence has **Hamiltonian unbounded below for
   k < µ**. The ghost-condensate architecture that generates the a⁻³ dust carries an IR
   pathology by construction. This is the published version of the programme's own
   dust-vs-health pincer.
2. **[R8] §6.2 — the same pathology in the Khronon theory** (ω² < 0 for √(1−α)k < µ,
   exponential once λ ≠ 0). Two independent constructions, same disease. Strong support
   for treating F1 as a structural obstruction rather than a technical nuisance.
3. **[R42] — arXiv:1804.01669.** "the MOND enhancement is **not sufficient** to allow
   ordinary matter to drive structure formation" — an independent, explicit statement of
   the same obstruction the programme found in g04h (the causal boost does not regenerate
   P(k) at linear order).
4. **[R45] — arXiv:2503.20151.** The dynamical Lorentz-violating vector gives MOND *only*
   in the stationary limit, and the faster MOND-regime growth is **not** recovered in the
   relativistic theory. Directly supports both the programme's growth-deficit result and
   its scepticism about vector-sector rescues.
5. **[R6] — arXiv:2301.03499 (A&A 676, A100).** AeST deviates from MOND at weak-lensing
   radii and the data show no such deviation. Independent published pressure on the
   leading rival's galaxy arm.
6. **[R4] — arXiv:2307.15126 (PRD 110, 044015).** AeST propagates **6 DOF nonlinearly**
   but 3 around Minkowski. Background-dependent DOF counting is the classic signature of a
   strong-coupling / constraint-algebra hazard, and it vindicates the programme's insistence
   on G2 as a first-class gate rather than a formality.
7. **[R14] — PRD 78, 044034.** Caustic formation in the vector sector of TeVeS on an
   infall timescale. Supports treating caustics (the programme's L1 lane) as a real,
   theory-killing gap rather than a smoothing detail.
8. **[R24] — arXiv:2303.08560 (JCAP 09 (2023) 004)** and **[R30] — arXiv:1710.00946**:
   the two nearest "MOND-plus-CDM" rivals (superfluid DM, emergent gravity) both fail on
   published, independent tests. The field is not crowded with survivors.

---

## 5. Where the literature is genuinely silent

These are open problems, and each is a place where a correct calculation is publishable.

1. **No PPN calculation exists for AeST.** Neither γ, β, α₁ nor α₂ has ever been computed
   in print for the theory that is widely described as the leading RMOND. [R5] only
   asserts that post-Newtonian corrections are "parametrically small." **This is the single
   biggest hole found.**
2. **No BBN analysis exists for AeST or for the Khronon theories.** AeST has
   G̃ = (1 − K_B/2)Ĝ [R2], so the gravitational constant during nucleosynthesis differs
   from the locally measured one, and nobody has published the resulting bound on K_B.
   G9 is `N-A` for essentially every RMOND except the nonlocal family [R41].
3. **No published preferred-frame analysis in the LOW-acceleration regime for anyone.**
   In [R8]'s own parametrisation α → 1 in deep MOND, and eq. (6.6a) read pointwise would
   give α₁ → −8 there — an enormous preferred-frame effect in exactly the systems (wide
   binaries, dwarf spheroidals, outer discs) where MOND is tested. *(Reading a PPN formula
   pointwise in a varying-α theory is a heuristic, not a result — which is precisely why
   the calculation is worth doing.)* No paper computes preferred-frame effects for any
   RMOND at a ~ a₀. This is an untouched observable and a natural discriminator against a
   theory whose α₁ = 0 is exact rather than asymptotic.
4. **No constraint-algebra / DOF analysis for the Khronon MOND theories.** [R8 §6.2]
   asserts 3 DOF on Minkowski and defers the Hamiltonian analysis. Only AeST has one [R4].
5. **No Cauchy well-posedness proof for any RMOND that passes G7 + G8.** G3 is `UNK` for
   both AeST and the Khronon family.
6. **No CMB calculation at all** for BIMOND [R21], emergent gravity [R28], self-interaction
   [R33], or entropic RMOND [R44].
7. **No quantitative cluster confrontation for AeST.** [R7] is explicit that the isothermal
   case is a first step only.
8. **Nonlinear cosmology is untouched for the CMB-passing theories.** [R8 §7] notes the
   ΛCDM correspondence breaks at second order and that N-body work is needed; [R5] says the
   same for AeST's quasistatic sector. The 2026 perturbative work [R46] treats a
   *phenomenological* generalized nonlinear Poisson equation, not a specific covariant
   theory, and finds no significant departure from ΛCDM in f σ₈ + DESI-DR2 BAO + SNe.
9. **σ₈ specifically.** No RMOND paper I found reports a σ₈ prediction as a falsifiable
   number; "matter power spectrum agreement" is claimed at the level of shape fits.

---

## Reference key

| Key | Identifier | Journal ref |
|---|---|---|
| R1 | arXiv:astro-ph/0403694 | Phys. Rev. D 70, 083509 (2004) |
| R2 | arXiv:2007.00082 | Phys. Rev. Lett. 127, 161302 (2021) |
| R3 | arXiv:2109.13287 | Phys. Rev. D 106, 104041 (2022) |
| R4 | arXiv:2307.15126 | Phys. Rev. D 110, 044015 (2024) |
| R5 | arXiv:2304.05134 | MNRAS 531, 272 (2024), doi:10.1093/mnras/stae1225 |
| R6 | arXiv:2301.03499 | A&A 676, A100 (2023) |
| R7 | arXiv:2312.00889 | JCAP 04 (2024) 040 |
| R8 | arXiv:2404.06584 | JCAP 11 (2024) 040 |
| R9 | arXiv:2507.00912 | (preprint, 1 Jul 2025) |
| R10 | arXiv:1107.5264 | Phys. Rev. D 84, 044056 (2011) |
| R11 | doi:10.3847/1538-4357/ad003d | ApJ 958, 129 (2023) |
| R12 | arXiv:1801.03382 | Phys. Rev. D 97, 084040 (2018) |
| R13 | doi:10.1103/PhysRevD.76.064002 | Phys. Rev. D 76, 064002 (2007) |
| R14 | doi:10.1103/PhysRevD.78.044034 | Phys. Rev. D 78, 044034 (2008) |
| R15 | arXiv:0905.4001 | Phys. Rev. D 80, 044032 (2009) |
| R16 | arXiv:gr-qc/0509083 | Phys. Rev. D 73, 064015 (2006) |
| R17 | arXiv:astro-ph/0505519 | Phys. Rev. Lett. 96, 011301 (2006) |
| R18 | arXiv:1412.4073 | Phys. Rev. D 92, 083505 (2015) |
| R19 | arXiv:0912.0790 | Phys. Rev. D 80, 123536 (2009) |
| R20 | arXiv:1308.5388 | Phys. Rev. D 89, 024027 (2014) |
| R21 | arXiv:2208.10882 | Phys. Rev. D 106, 084010 (2022) |
| R22 | arXiv:1507.01019 | Phys. Rev. D 92, 103510 (2015) |
| R23 | arXiv:1809.00840 | JCAP 02 (2019) 001 |
| R24 | arXiv:2303.08560 | JCAP 09 (2023) 004 |
| R25 | arXiv:0804.3518 | — |
| R26 | arXiv:0901.3114 | Phys. Rev. D 80, 023524 (2009) |
| R27 | arXiv:2209.07831 | — |
| R28 | arXiv:1611.02269 | SciPost Phys. 2, 016 (2017) |
| R29 | arXiv:1703.01415 | — |
| R30 | arXiv:1710.00946 | JHEP 11 (2017) 007 |
| R31 | arXiv:1612.03034 | MNRAS 466, 2547 (2017) |
| R32 | arXiv:2106.11677 | A&A (2021), doi:10.1051/0004-6361/202040108 |
| R33 | arXiv:0901.4005 | Phys. Lett. B 676, 21 (2009) |
| R34 | arXiv:2303.11094 | — |
| R35 | arXiv:2303.06115 | Class. Quantum Grav. 40, 215014 (2023) |
| R36 | arXiv:1308.5410 | JHEP 11 (2013) 135 |
| R37 | arXiv:1404.4008 | JHEP 12 (2014) 102 |
| R38 | arXiv:1708.00603 | — |
| R39 | arXiv:2503.11174 | JCAP 06 (2025) 059 |
| R40 | arXiv:1106.4984 | — |
| R41 | arXiv:1608.07858 | — |
| R42 | arXiv:1804.01669 | — |
| R43 | arXiv:0911.5464 | MNRAS 403, 886 (2010) |
| R44 | arXiv:2511.05632 | (preprint, rev. 17 Aug 2026) |
| R45 | arXiv:2503.20151 | (preprint, rev. 11 Aug 2025) |
| R46 | arXiv:2608.18229 | (preprint, 18 Aug 2026) |
| R47 | arXiv:1710.05834 | ApJL 848, L13 (2017) |
| R48 | doi:10.1038/nature01997 | Nature 425, 374 (2003) |
| R49 | arXiv:1403.7377 | Living Rev. Relativity 17, 4 (2014) |
| R50 | arXiv:1209.4503 | Class. Quantum Grav. 29, 215018 (2012) |
| R51 | arXiv:1307.2552 | Class. Quantum Grav. 30, 165019 (2013) |
| R52 | arXiv:1112.3960 | Living Rev. Relativity 15, 10 (2012) |
| R53 | arXiv:2501.17006 | (review chapter, 2025) |
| R54 | arXiv:astro-ph/0702002 | Phys. Rev. D 75, 083513 (2007) |
| R55 | arXiv:0711.0520 | Phys. Rev. D 77, 084010 (2008) |
| R56 | arXiv:2406.18225 | — |
| R57 | arXiv:2309.06232 | — |
| R58 | doi:10.1086/162570 | ApJ 286, 7 (1984) |

Cuscuton background for the programme's own branch: [R54] establishes that the cuscuton
introduces **no additional propagating degree of freedom** and does not violate
relativistic causality — its perturbations satisfy a constraint rather than an equation of
motion. No published work applies a cuscuton to MOND; that is itself a §5 silence.

---

## Caveats on this map

- I did not verify any theory's claims by recomputation. Every `PASS` is a *published
  claim*, not an independent confirmation. Where the claim is contested I have said so.
- `N-A` entries mean "I found no published calculation," not "no calculation exists."
  Negative literature results are the weakest kind of finding; treat each as a lead.
- The `[my arithmetic]` block in §2.2 is a plausibility check on a published formula, not
  a result, and is not used anywhere in §2.3.
