# opus_49_doorF — DOSSIER: THE REAL YANG–MILLS MASS GAP, FRONTIER MAP
**Lane:** opus_49d doorF | **Date (conversation clock):** 2026-09-22 (UTC-04:00)
**Scope:** a cited, rung-by-rung map of the Clay Yang–Mills mass-gap problem as it actually
stands **in the world**, and where this repo's certified rungs sit on that map. No claim is
made beyond its proof. Items marked OBSERVED are from the sources cited; items marked
REPO-CERTIFIED are the repo's own certified fragments; everything else is OPEN with its
exact obstruction named.

---

## 0. THE THEOREM UNDER ATTACK (what "mass gap" means here)

The Clay problem (Jaffe–Witten, *Quantum Yang–Mills Theory*, in *The Millennium Prize
Problems*, Clay 2006) asks for a **nontrivial quantum Yang–Mills theory on ℝ⁴** for a
compact simple gauge group (e.g. SU(3)) satisfying the Wightman axioms (restricted to
gauge-invariant operators) **and** possessing a strictly positive **mass gap**: the lowest
non-zero eigenvalue m₀ > 0 of the (self-adjoint, positive) Hamiltonian H, equivalently
exponential decay of connected vacuum correlations of local gauge-invariant operators with
rate ≥ m₀.

Two logically independent demands:
1. **Existence** of the continuum theory (Euclidean measure satisfying the
   Osterwalder–Schrader axioms on the gauge-invariant algebra, or equivalently a
   Wightman field theory of gauge-invariant operators).
2. **The gap**: clustering / spectral gap m₀ > 0.

(Jaffe–Witten 2006; the nLab survey "Yang–Mills mass gap" states the problem remains open;
every serious review to 2026 agrees.)

---

## 1. THE COMPLETE CHAIN A CONTINUUM PROOF WOULD NEED

A standard modern proof-skeleton, with each rung's status today. The spacing is a,
g²(a) ~ −1/(2b₀ ln(aΛ)) the (one-loop) asymptotic-freedom trajectory, b₀ = 11N/(48π²) for
pure SU(N) (β(g) = μ dg/dμ = −b₀ g³ − …, so 1/g²(μ) = 2b₀ ln(μ/Λ) and g²(a) = −1/(2b₀ ln aΛ)
as a → 0⁺). The requirement is a⁻¹·Δ(a, g²(a)) → m₀ > 0 in units of Λ.

| Rung | Statement | World status | This repo |
|---|---|---|---|
| C1 | Fixed-spacing lattice Wilson measure exists (finite-dim integral); **reflection (OS) positivity**; strictly positive self-adjoint transfer matrix T | **PROVEN** (OS78, §3; Lüscher 77; Menotti–Pelissetto 87 for reflection planes through sites and through temporal links, all observables) | — (classical) |
| C2 | Infinite-volume lattice measure at fixed a (thermodynamic limit) | **PROVEN at strong coupling** (OS78: existence + analyticity of the strong-coupling infinite-volume limit; Wilson-loop confinement bound). Extended strong-coupling regime and large-N: Chatterjee 2019–21, Shen–Zhu–Zhu 2023 (Bakry–Émery: unique invariant measure, LSI/Poincaré, exponential clustering = correlation mass gap at strong coupling). **OPEN at weak coupling and in the crossover** | I15 many-plaquette gap (Yarotsky leaf) — fixed spacing, strong coupling |
| C3 | **UV stability**: bounds on the finite-volume lattice Gibbs/partition data uniform in a→0 (large-field control) | **Partial, the canonical reference: Balaban's RG program**, 1987–1989 (see §6). **Not completed as a published, verified, full construction**; Federbush's parallel phase-cell program also incomplete | — |
| C4 | **Tightness**: the family {μ_a} (after renormalization) is tight in a continuum functional topology; a subsequential continuum measure exists | **OPEN** | — |
| C5 | The limit measure satisfies **OS axioms**: Euclidean invariance, regularity, OS+ positivity (survives the limit), clustering | **OPEN** (OS+ passing to the limit is part of the construction; nothing on record does it in 4D) | — |
| C6 | **OS reconstruction** ⟹ Wightman theory of gauge-invariant operators, H = P⁰ ≥ 0 self-adjoint; T = e^{−aH} relation | Machinery, **PROVEN once C5 holds** (OS73/75; Seiler 82; Glimm–Jaffe 87) | — |
| C7 | **The gap along the trajectory**: liminf_a a⁻¹·gap(H_a) > 0 with H_a the transfer-matrix Hamiltonian at spacing a | **THE WALL**. No known a-trajectory carrying a proven gap; the proven gaps (strong-coupling) live at β ≤ β* (fixed spacing), the scaling trajectory is *weak-coupling* (g²(a)→0), and no proof spans the crossover | Registered as YM_ROADMAP R5/R6; gap conservation under a→0 is exactly the open item |
| C8 | Vacuum uniqueness / non-Gaussianity of the limit | **OPEN** | — |

Corollary noted for orientation: **C1 + a fixed-spacing spectral gap ⟹ a fixed-spacing
Hamiltonian transfer-matrix gap; it does NOT by itself yield C7.** The a→0 step is the
entire difficulty; the fixed-spacing strong-coupling world is, rigorously, a *separate*
theory from the continuum one. This is the single most important honesty marker of this
dossier, and it matches the repo's registered position (YM_ROADMAP R4–R6).

---

## 2. TRUE STATE OF EACH RUNG, TODAY (with citations)

### 2.1 Reflection positivity / transfer matrix (rung C1) — PROVEN, classical
- K. Osterwalder, E. Seiler, *Gauge field theories on a lattice*, Ann. Phys. (NY) **110**
  (1978) 440: verifies physical positivity of the lattice YM Wall-meson measure, obtains a
  positive self-adjoint transfer matrix, strong-coupling infinite-volume limit and Wilson
  confinement bound. [OBSERVED: the paper's own abstract.]
- M. Lüscher, *Construction of a selfadjoint, strictly positive transfer matrix for
  Euclidean lattice gauge theories*, CMP **54** (1977) 283. Lüscher also showed the Wilson
  action satisfies RP both for planes cutting temporal links and planes containing sites
  [as recorded in the literature]. 
- P. Menotti, A. Pelissetto, *General proof of Osterwalder–Schrader positivity for the
  Wilson action*, CMP **113** (1987) 369: extends RP to planes containing sites, **all**
  gauge-invariant observables, relying on the specific structure of the Wilson action.
- Seiler, *Gauge Theories as a Problem of Constructive Quantum Field Theory*, Springer
  LNP 159 (1982), and Glimm–Jaffe, *Quantum Physics*, are the standard reconstruction
  references connecting Euclidean clustering to the spectrum of H.

So the fixed-spacing transfer-matrix rung the repo needs between its R4 gap and the
Hamiltonian spectrum is **classical, published, and checkable**. (This is the rung this
session permanently secures in ATTEMPT.md — restated, not claimed as new.)

### 2.2 Strong-coupling lattice: area law and correlation mass gap (rungs C2-fixed-spacing) — PROVEN, strong coupling
- Wilson 1974 (Phys. Rev. D10, 2445) strong-coupling expansion; OS78 (above); Fröhlich 1979
  (as cited in CNS25); Göpfert–Mack, CMP **82** (1981) 545: 3D U(1) area law for **all**
  coupling.
- S. Chatterjee, *Yang–Mills for probabilists* (survey, arXiv:1803.01950) and the 2021
  "mass gap implies area law" sufficient-condition work (Cha21, cited in CNS/2509.04688).
- H. Shen, R. Zhu, X. Zhu (SZZ), *A stochastic analysis approach to lattice Yang–Mills at
  strong coupling*, CMP **400** (2023) 805 (arXiv:2204.12737): d > 1, 't Hooft scaling,
  |β| < 1/16(d−1) for SU(N) and |β| < (N−2)/(32(d−1)N) for SO(N): unique invariant measure
  on the whole lattice, exponential ergodicity, finite-volume ⟶ infinite-volume convergence,
  log-Sobolev & Poincaré inequalities, exponential decay of correlations of a large class of
  observables (their "strictly positive mass gap", **a Euclidean correlation-clustering
  statement at fixed spacing — not a Hamiltonian spectrum gap in the continuum**), plus
  large-N results. [OBSERVED from arXiv:2204.12737 abstract.]
- **The repo's own certified fragment (REPO-CERTIFIED):** I15 (i15/PROOF.md,
  fable_independent_2026/lean_2026/I15_suN_lattice_gap.lean): a true *spectral* gap at fixed
  spacing — single plaquette exactly: gap ≥ 2xC_F − b_N/x ≥ 1 for x ≥ 2 (full-space min-max,
  N-unif.); and, via Yarotsky (math-ph/0411042v1, Theorems 1–3), a gap ≥ 3x/16 for x ≥ X_d on
  every finite open subgraph **uniform in N and volume**, X_d finite but **not numerically
  evaluated** (its defining constants c₁, c₂ live in a paywalled 2004 JMP source — registered
  obstruction; door-D REFEREE.md (j)). This is the fixed-spacing analogue of SZZ's correlation
  gap, expressed as a Hamiltonian spectral gap.

### 2.3 't Hooft-scaling / area-law progress 2025 (see §5 for 2509.04688; CNS25 = Cao–Nissim–Sheffield, *Expanded regimes of area law for lattice Yang–Mills theories*, arXiv:2505.16585, June 2025)
- CNS25: area law for U(N) lattice YM in an extended strong-coupling regime (esp. N large),
  by master-loop-equation analysis of Wilson string expectations; improves OS78. [OBSERVED
  from arXiv:2505.16585.]
- 2509.04688 (Sep 2025): area law in the full 't Hooft regime for G ∈ {U(N), SU(N), SO(2N)}
  — detailed report in §5. This is **area law, fixed lattice spacing, strong coupling**; it is
  emphatically *not* a Hamiltonian mass gap (see §5).
- Statement of the honest boundary: **area law at fixed spacing ≠ continuum mass gap.** No
  2025 area-law result crosses a → 0. THE scaling-window rung (C7) remains untouched by all
  of these.

### 2.4 2D and 3D constructions
- **2D pure YM is (classically and on the lattice) solvable** (Migdal recursion; 2D QCD: 't
  Hooft 1974; Gross–Taylor large-N; exact loop expectations, area law with computable
  constants; see Fragment B in ATTEMPT.md for the exact U(1) constant −ln(I₁/I₀)). 2D is
  not the Clay problem but is the correct warm-up: it is the *only* dimension with an exact
  area-law constant.
- **3D (superrenormalizable, g² has mass dimension 1):** the mass gap is dimension-forced,
  m = c·g²·(group data). Physics-level rigorous-flavoured Hamiltonian analysis:
  D. Karabali, V.P. Nair, *A gauge invariant Hamiltonian analysis for non-abelian gauge
  theories in (2+1) dimensions*, Nucl. Phys. **B464** (1996) 135 (hep-th/9602155); and
  D. Karabali, C. Kim, V.P. Nair, *Planar Yang–Mills theory: Hamiltonian, regulators and
  mass gap*, Nucl. Phys. **B524** (1998) 661 (hep-th/9705087); glueball spectrum: R.G.
  Leigh, D. Minic, A. Yelnikov, *Glueball spectrum in 2+1*, Phys. Rev. **D76** (2007)
  065018 (hep-th/0604060), with good agreement to Teper's lattice data (m_{0⁺⁺} ≈ (3–4)·g²N).
  **BUT**: the KKN construction is a credible physics-level derivation (canonical
  quantisation on the gauge-invariant/holonomy space, a wavefunctional ansatz, infinite
  volume limits), **not a theorem of constructive QFT**; the continuum 3D Euclidean measure
  is **not rigorously constructed** and a 3D Hamiltonian mass gap is **not proven**. The
  newest explicit public statement confirms it: V.P. Nair, *Towards a Proof of Mass Gap in
  3d Yang–Mills Theory*, arXiv:2608.10133 (Aug 2026) — "outlines of a proof ... in terms of
  an inequality on the eigenvalues of the Laplacian on the gauge-invariant configuration
  space" [OBSERVED from the abstract: outlines, not a proof].
- Repo GPS on this: 3D superrenormalizability gives dimensional control but no theorem; the
  framework's own R1–R3 gap results are its scalar-gauged abelian sector (eaten Goldstone), a
  **different** object from continuum YM; the SU(3) obstructions (YM_NONABELIAN.md) prevent
  misreading the abelian mechanism as QCD.

### 2.5 The scaling window (rung C7) — OPEN, and named
- The strong-coupling expansions die exactly where the magnetic term ceases to dominate; the
  intermediate-β gap is Monte-Carlo lore only (SU(3) glueball m ≈ 1.6 GeV: Morningstar–Peadon,
  Phys. Rev. **D60** (1999) 034509). Numerical evidence is not a proof.
- No published theorem shows a gap along the asymptotically-free trajectory g²(a) =
  −1/(2b₀ ln aΛ). Balaban's UV-stability control is the closest published analytic handhold,
  but (i) its full completion (tightness of unblocked observables, OS axioms, clustering,
  infinite-volume + gap) is not on record verified line-by-line, and (ii) nothing in the
  lattice-strong-coupling or area-law literature measures the gap along a → 0.
- Repo register: YM_ROADMAP R5/R6 (OPEN — the Clay wall); YM00_CAMPAIGN K5 (the Clay scope
  explicitly out of the framework's own claim); door-D REFEREE (k)/(j).

### 2.6 Balaban / Federbush history (rung C3) — the honest summary
- **Balaban** (1987–1989, Comm. Math. Phys. series 109–122): *Renormalization group approach
  to lattice gauge field theories I* (CMP 109, 249), II (cluster expansions, CMP 116, 1),
  III (*Convergent renormalization expansions*, CMP 119, 243), *Large field renormalization I*
  (CMP 119, 243) and *II: Localization, exponentiation and bounds for the R operation*
  (CMP 122, 355). What he established is the **ultraviolet stability of 4D (and 2+1D) lattice
  Yang–Mills**: the large-field renormalization operation ℝ, polymer bounds, β-function
  extraction, and bounds uniform in the lattice spacing. This is the central analytic control
  of the whole construction.
- **Federbush** (1986–1989): *A phase cell approach to Yang–Mills theory*, I (CMP 107, 319),
  II (with C. Williamson, J. Math. Phys. 28 (1987) 1419), III (CMP 110, 293), IV (CMP 114,
  317), V (CMP 121, 143), VI (Ann. Inst. H. Poincaré 47 (1987) 17): a parallel, partly
  non-abelian phase-cell/lattice-continuum-duality programme; also never carried to a complete
  construction.
- Verdict on both: they constitute the authoritative **analysed scaffolding** for C3 and a
  major part of C4, but the literature records **no published, community-verified completion**
  of 4D continuum YM from either. Subsequent attempts (see §3) that "assume Balaban" carry an
  unverified technical hypothesis and say so explicitly. This repo registers Balaban's RG as
  the honest unresolved segment it would need to repeat or complete — nothing else.

---

## 3. CLAIMS OF A COMPLETE PROOF SINCE 2023 — STATUS OF EACH

| Claim | Venue/date | What it claims | Status as of 2026-09-22 |
|---|---|---|---|
| P. Mondal, *A geometric approach to the Yang–Mills mass gap* (arXiv:2301.06996) | JHEP **12** (2023) 191 (published, peer-reviewed) | regularized Bakry–Émery Ricci curvature gives a mass gap in 2+1 and 3+1 | **NOT a proof of the Clay problem**: the gap statement is explicitly **conditional on the existence of a quantized YM theory** on ℝ^{1,2}/ℝ^{1,3} — i.e. on exactly the unproven construction; the gap calculation is described by the author himself "at least as a heuristic one". Not retracted; correctly filed as geometric-analysis contribution, conditional/heuristic w.r.t. the Clay gap |
| S. Farinelli, *Renormalized Four Dimensional Gauge Invariant Quantum Yang–Mills Theory and Mass Gap* (arXiv:1406.4177, 2014) and *Four Dimensional Quantum Yang–Mills Theory for Weak Coupling Strength…* (arXiv:2406.16881, 2024) | arXiv math.GM | complete 4D mass gap proof | **Unverified / not accepted.** No peer review, no independent verification, math.GM (general mathematics); the 2024 companion itself conditions *confinement* on "the existence of the mass gap" (delegated to the 2014 companion). No retraction needed; none exists because none of it was an accepted proof |
| Y. Agawa, *A Rigorous Proof of the Mass Gap in SU(N) Yang-Mills Theory* (Mar 2025) + *The Essential Addendum on the Continuum Limit and Finite Gribov Uniqueness* (Jun 2025) | Cambridge Open Engage (working paper, not peer-reviewed) | holonomy-based non-local regularization; cluster expansion; OS axioms; mass gap; Gribov uniqueness via Morse theory | **RETRACTED BY THE AUTHOR.** Main paper v1 (Mar 2025) retracted; addendum v1 (Jun 2025) and v2 (Jul 2025) retracted. Author's statement: the work "presents a preliminary theoretical hypothesis that has not yet been sufficiently validated for formal publication". [OBSERVED from the venue's retraction pages.] The "holonomy-based Clay proof" that circulated in 2025 = this. **It is dead on the record.** |
| D.C. Jacobsen, *A Constructive Proof of Existence and Mass Gap for Pure SU(3) Yang–Mills in Four-Dimensional Space-Time* (arXiv:2506.00284, 30 May 2025) | arXiv **physics.gen-ph** (non-refereed general physics) | 5D orbifold-regulated Wilson lattice; polymer expansion required to be convergent for β > 630; Sturm–Liouville 5th-dim spectral identification | **Unverified / not accepted.** physics.gen-ph is not a refereed category; no independent verification; the claimed convergent-expansion window and the transfer-matrix spectral identification have not been certified by any expert. No known retraction (nothing to retract); treated by the community as an unverified claim. Repo rule applies: an unverified preprint that claims the Clay solution is *prima facie* not a proof |
| J. Nielsen, *The Definitive Proof of the Four-Dimensional Yang–Mills Mass Gap* (summer 2025/2026) | philarchive (non-peer-reviewed) | "representation-theoretic rigidity of holonomy distributions"/"TUFT" mass gap | **Not credible / unverified.** Non-refereed repository, no engagement with the analytic obstruction (cluster control, tightness), no verification. Filed under the noise floor |
| "Lluis Eriksson", *Ultraviolet Stability … Closing the Bałaban–Doob Circuit under a Quantitative Blocking Hypothesis* (2026) & companion | ai.viXra (AI-assisted e-prints) | conditional continuum limit on a *blocked-observable* algebra, fixed finite volume | **Explicitly conditional and self-limited.** Lists "Osterwalder–Schrader reconstruction, the thermodynamic limit, and the mass gap remain as identified open problems" [OBSERVED from the abstract]. An honest example of what is NOT a proof — and a good model of how to say so |
| Anon., *A Constructive Solution to the Clay Millennium Yang–Mills Problem* (OSF preprint, c. 2025) | OSF (non-peer-reviewed) | 7-step construction assuming Balaban, Faria da Veiga–O'Carroll, AFS chessboard | **Explicitly conditional**: "some technical results are assumed from prior literature … neither of which has been fully verified line-by-line by the community. We adopt these as technical hypotheses." Not a proof by its own admission |

**Dossier verdict:** as of 2026-09-22 there is **no complete, verified 4D construction and
mass-gap proof in the world**. Every post-2023 "complete proof" is either retracted (Agawa),
explicitly conditional on the quantization existing (Mondal), unverified/non-accepted
(Farinelli, Jacobsen), conditional on unverified input (OSF), or non-refereed noise (Nielsen,
Eriksson, viXra). The field's own open-problem designations (Jaffe–Witten; nLab; every 2025
area-law paper's "remaining problem" section) all agree.

---

## 4. THE REPO'S OWN REGISTER ON THIS (what "we" hold)

- **R1–R3 (framework sector):** the framework's own scalar-gauged abelian mechanism with
  its pinned 5.089 keV ladder arithmetic — a *different* object from continuum QCD; the R1
  pin m_gauge = m_dust is BOUNDARY-REGISTERED by the door-D referee, not derived; no QCD
  sector exists (TOE_STATUS). K5 of YM00_CAMPAIGN denies any Clay claim by the framework.
- **R4 / I15 (REPO-CERTIFIED, this lane's handhold):** fixed-spacing strong-coupling spectral
  gap, single-plaquette exact and many-plaquette via Yarotsky at x ≥ X_d, uniform in N and
  volume; X_d unevaluated (obstruction registered); operator theory external, scalar parts
  Lean-certified (zero sorry; axioms exactly {propext, Classical.choice, Quot.sound}).
- **R5/R6 (OPEN — the Clay wall):** no continuum limit, no scaling window, no gap survival
  under a → 0; named, not papered over.
- **R7:** the Euclidean-facing equivalence (clustering ⟺ spectral gap) is standard machinery
  pending the C5 construction.
- **The world's wall, restated in one line:** a fixed-spacing strong-coupling gap exists
  uniformly in N and volume (REPO-CERTIFIED, via Yarotsky at unknown X_d); the continuum
  limit and the scaling window are open and named; **no complete 4D proof exists in the
  world**. This dossier defends exactly that state with the citations above.

---

## 5. **arXiv:2509.04688, READ CAREFULLY — WHAT IT PROVES AND WHAT IT DOES NOT**

S. Cao, R. Nissim, S. Sheffield, *Dynamical approach to area law for lattice Yang–Mills*,
arXiv:2509.04688 (v1 4 Sep 2025, v2 28 Sep 2025; math.PR / math-ph; 8 pages; "Submitted"
per v2 comments — **not yet peer-reviewed as of this writing**) — read in full for this
dossier.

**Setup:** d ≥ 2, N ≥ 2, G ∈ {U(N), SU(N), SO(2N)} (Theorem 1.6 states SO(2(N−1)) for N ≥ 2),
lattice torus Λ_L, 't Hooft-scaled Wilson action (the N-prefactor convention, eq. (1.2)),
β the inverse coupling. Thresholds (Def. 1.4): β*_{SU(N)} = β*_{U(N)} = 1/(8(d−1)),
β*_{SO(N)} = 1/(16(d−1)) + 1/(8N(d−1)).

**Theorem 1.6 (Area law in the 't Hooft regime).** For d ≥ 2, N ≥ 2, G as above and
**β < β*_G**, there are C = C(β,d,N), c = c(β,d,N) > 0 such that for every rectangular
loop ℓ in Λ_L with side lengths ≤ L/2,

    |⟨W_ℓ⟩_{Λ,β}| ≤ C·exp(−c·area(ℓ)).

**Method (their Summary + §2–§3):** (i) use the **Dürhuus–Fröhlich 1980 mass-gap condition**
(DF80, CMP 75, 103: split the lattice into height-1 slabs; condition on the boundary fields
at slab top/bottom; the conditional law of the slab-crossing edges is a variable-environment
σ-model; if those σ-models have exponential decay of correlations *uniform in the boundary
conditions*, area law follows — their Theorem 2.3 = combined DF80 Thms 1.2–1.3). (ii) Verify
that condition via the **Bakry–Émery condition** (from SZZ23), improved: the Hessian bound
|Hess S^{A,B}(v,v)| ≤ 4(d−1)Nβ|v|² (their (3.1); SZZ23's analogous one had an 8, so their
β* is twice SZZ23's threshold), whence the Bakry–Émery curvature K_{S^{A,B}} ≥ 1/2 −
4Nβ(d−1) > 0 for β < β*_G (their Prop. 3.2; estimates imported from SZZ23 Lemma 3.3, 4.1,
Cor. 4.4/4.11). (iii) The U(N) case by the conditioning trick U(N) = U(1)×× SU(N) (their
Cor. 3.6: for *linear* observables Cov ≤ C₁e^{−C₂d(Lf,Lg)}(|||f|||₈|||g|||₈ + ‖f‖₂‖g‖₂)).

**What it PROVES (exactly):**
1. **Wilson's area law** — |⟨W_ℓ⟩| ≤ C e^{−c·area(ℓ)} — for rectangular loops on the
   **fixed-spacing (a = 1) finite lattice torus**, in the **strong-coupling 't Hooft regime
   β < β*/₈₎**, for gauge groups with **nontrivial center** (the DF80 hypothesis; hence the
   SO(odd) exclusion, Remark 1.7), uniformly in the volume L (side lengths ≤ L/2). This is a
   confinement *observable* bound — Wilson's 1974 definition of quark confinement.
2. It **improves OS78** (whose strong-coupling regime was a proper subset) **and CNS25**
   (which held in a sub-regime, not the full 't Hooft regime).
3. The "mass gap" invoked (DF80 condition) is a **correlation-decay / mass-gap condition of
   the slab σ-models and of the lattice theory at fixed spacing** — i.e. exponential
   clustering of local observables — **not a Hamiltonian spectral gap of a continuum
   theory**.

**What it does NOT prove (exactly, and this is the mass-gap-relevant remainder):**
1. **No Hamiltonian/spectral mass gap.** There is no transfer-matrix spectral statement, no
   self-adjoint Hamiltonian, no spectrum(H) ∩ (0,m₀) = ∅ result anywhere in the paper.
2. **No continuum limit.** Everything is at **fixed lattice spacing a = 1** on a finite
   torus; there is **no a → 0**, no g²(a) scaling trajectory, no recovery of ℝ⁴, no OS
   functions of a continuum Wightman theory, and 0 ≤ a−¹Δ → m₀ is never addressed. The
   Euclidean measure on ℝ⁴ is untouched.
3. **Strong coupling only.** β < β*_G means *large* g²; the Clay scaling window has
   g²(a) → 0 (weak coupling) along asymptotic freedom — **opposite end** of the coupling
   axis (the β ≥ 1/(8(d−1)) region, containing the actual SU(3) θ = 0 physics, is
   untouched; the paper's own threshold structure says so).
4. **No vacuum uniqueness, no OS axioms in the limit, no rigidity/large-N spectrum.**
   The infinite-volume limit for *weak* coupling, uniqueness among all ground-state
   representations, periodic-torus subtleties for Wilson loops near the boundary, and any
   quantum Yang–Mills mass on ℝ⁴ are outside the paper.

**Dossier line on 2509.04688:** it is the current **frontier of the *area-law* rung at
fixed spacing**, i.e. a sharpened C2-style statement, squarely *within* the strong-coupling
lattice world. It does **not** touch the Clay wall (C7) and does not need to — the authors
claim only what they prove. It is mathematically consistent with this repo's position: the
fixed-spacing strong-coupling world marches forward; the continuum gap remains the open,
unnamed-in-the-litterature wall. (The paper is a short note in math.PR; "Submitted"; treat
peer-review status as pending as of 2026-09-22, and cite it as arXiv 2509.04688.)

---

## 6. BALABAN / FEDERBUSH — ONE-PARAGRAPH HISTORY (with citations)

Balaban's *Renormalization group approach to lattice gauge field theories* I–III and the
*Large field renormalization* I–II papers (CMP 109 (1987) 249; CMP 116 (1988) 1; CMP 119
(1988) 243; CMP 119 (1988) 243 for LFR I; CMP 122 (1989) 355 for LFR II) solved the hardest
combinatorial/analytic step of the 4D construction: a **large-field renormalization
operation** ℝ with bounds uniform in the spacing that remove the obstruction to **UV
stability** of 4D lattice gauge theories. Federbush's *phase cell* series (CMP 107 (1986)
319; J. Math. Phys. 28 (1987) 1419; CMP 110 (1987) 293; CMP 114 (1988) 317; CMP 121 (1989);
Ann. IHP 47 (1987) 17) pursued a parallel "lattice–continuum duality" route with gauge-
invariant loop variables. Neither produced, nor has anyone since produced, a **completed,
community-verified** theorem delivering the continuum 4D Euclidean YM measure with the OS
axioms and a positive mass gap; Balaban's control is universally regarded as the essential
analytic scaffolding that any future construction will build on, and the missing public
steps are exactly rungs C4–C8. (This matches the split accepted in the review literature and
in the 2023–2026 "assume Balaban" preprints, which say so explicitly — see §3.)

---

## 7. WHAT REMAINS (the honest open lane, in one list)
1. Evaluate (or bypass) the I15/X_d strong-coupling threshold to get a quantitative fixed-
   spacing window (Yarotsky's c₁,c₂ are existence constants; values paywalled — REPO
   obstruction).
2. Prove UV stability ⟶ tightness for a *complete* (unblocked) observable class along the
   AF trajectory (Balaban completion; C3/C4).
3. Prove OS axioms + non-Gaussianity + vacuum uniqueness of any limit measure (C5/C8).
4. Prove the gap survives a → 0 along g²(a) = −1/(2b₀ ln aΛ) (C7 — the Clay wall).
   No prior work, including 2509.04688 and everything in §3, does any of 2–4.

*House rule: nothing above is claimed beyond the cited record; every open item is open with
its exact content named.*