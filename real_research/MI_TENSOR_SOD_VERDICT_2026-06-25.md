# MI-tensor anisotropy vs the SO(d) self-duality — final d=3 verdict (2026-06-25)

**C. Zimmerman, 2026-06-25.** *Final probe on the d=3 thread, gravity side (the real domain). The d=3 verdict
(`real_research/D3_SELFDUALITY_VERDICT_2026-06-25.md`) graded the SCALAR a₀=c²√(Λ/32π) chain + flat-curve selection
**PARTIAL** — real but standard-MOND-shared and decorative; Z²=32π/dim SO(3) re-labels 32π/3 with no bivector entering
the scalar chain. It flagged the ONLY possible route to a non-decorative dim SO(d)=d constraint: the framework-DISTINCTIVE
modified-inertia (MI) TENSOR content — the boost-induced inertia-tensor anisotropy δI/I=(1−μ_fw)(g)(w/c)²·O(1) that
induces (a) the s̄^TX SME gravity dipole (the live ~9.6× INPOP/Cassini test) and (b) the α₂ PPN coefficient. This file
runs that route explicitly and adjudicates "the MI tensor anisotropy SELECTS d=3" as ruthlessly as "it is decorative."
sympy/mpmath dps≥40. Quarantine: d=3 enters only as the target; a₀ is the input throughout, nothing SM-side derived.*

Inputs: `opus_48_extended_research/reviews/derivation_chain/mi_ppn_alpha2_verify.py`,
`S_TENSOR_SME_COMPONENT_LEDGER_2026-06-17.md`, `MI_PPN_ALPHA2_DERIVATION_2026-06-17.md`,
`MI_TENSOR_D3_SELFDUALITY_SKEPTIC_2026-06-25.md`, `reviews/dsunruh_d_dimensional_derivation.py`.
Independent re-verification: `/tmp/mi_sod_verdict_verify.py` + `/tmp/mi_sod_check345.py` (all 5 checks reproduced clean).

---

## VERDICT: **(B) STAYS-PARTIAL** — the self-duality is DECORATIVE/NOTATIONAL.

The MI-tensor content is genuinely MODIFIED-INERTIA-distinctive in **WHAT it is** — an inertia-tensor / Thomas-precession
response a pure scalar AQUAL/MG value has no analogue of. But its **d-DEPENDENCE** is a smooth coefficient (1−1/d),
AQUAL-EFE-shared in structure, and O(β²) below every floor. The dim SO(d)=d self-duality is used **nowhere as physics** —
it only Hodge-dualizes the one genuine bivector (the Thomas wedge a∧w) into the familiar a×w. The MI tensor adds **no
load-bearing dim SO(d) constraint**; the d=3 verdict's PARTIAL/decorative standing is **UNCHANGED and sharpened**: the
route the prior verdict flagged as the only non-decorative path comes back smooth-in-d too.

---

## The distinctive object, reconstructed exactly (all sectors symmetric or vector — the self-duality acts on none of them)

Each mass element of a body boosted with velocity **w** (unit ŵ, β=w/c) acquires an anisotropic inertial mass under the
dS–Unruh modified inertia: m_eff(r̂) = m·[1 − ε·(r̂·ŵ)²], ε = (1−μ_fw)(g)·β². The induced inertia-tensor anisotropy is the
traceless symmetric part **δI_ij/I ≈ ε·[ŵ_iŵ_j − (1/d)δ_ij]**. The MI-distinctive observables split into three tensor
sectors, and the self-duality (#vectors = #bivectors) acts on the **antisymmetric sector alone**:

| Observable | Tensor type | SO(d) sector | β | Self-duality used? |
|---|---|---|---|---|
| δI_ij inertia anisotropy | symmetric rank-2 (A·δ_ij + B·ŵ_iŵ_j) | **sym2-traceless** (d−1)(d+2)/2 | O(β²) | **NO** |
| s̄^TX boost dipole (live test) | (T, spatial-vector) of symmetric s̄^μν | **vector** d | O(β) | **NO** |
| α₂ / Thomas precession | antisymmetric a∧w on spin | **bivector** d(d−1)/2 | O(β²) | only **DUALIZES** |

A **pure boost** supplies ONE direction ŵ_i. The only symmetric tensors buildable from {δ_ij, ŵ_i} are δ_ij and ŵ_iŵ_j —
both SYMMETRIC, defined in every d. No cross product, no curl, no angular-momentum vector enters a pure-boost inertia
response. s̄^μν = (a₀/2|a|)(u^μu^ν − trace) is built from u^μ squared symmetrically; s̄^TX ~ β·n_X is a symmetric
(time, space) component — an l=1 VECTOR dipole, verified NOT antisymmetric and NOT a Hodge dual, existing in any D=d+1.

## Independent re-verification (sympy/mpmath dps≥40 — all five checks reproduced)

1. **Anisotropy is symmetric-traceless in ALL d.** Direct (d−1)-sphere integration gives ⟨(r̂·ŵ)²⟩ = 1/d exactly for
   d=2,3,4 (the trace, l=0). The remainder ε·(ŵ_iŵ_j − δ_ij/d) is a pure outer product of ONE vector — symmetric in
   i↔j, even in ŵ (no l=1 dipole), no antisymmetric/bivector piece in the static per-constituent anisotropy. ✓
2. **Irrep dimensions are smooth polynomials.** vector=d, bivector=dim SO(d)=d(d−1)/2, sym2-traceless=(d−1)(d+2)/2 =
   {2,5,9,14,20} for d={2,3,4,5,6}. The distinctive anisotropy lives in sym2-traceless — a smooth, non-degenerate,
   well-defined irrep for **all d≥2**. It equals the vector dim only accidentally at d=2 and the bivector dim only at
   d=1, **never via the self-duality d=3**. The boost→anisotropy map ŵ → ŵ⊗ŵ−trace = Sym²(vector)−trace exists in every
   dimension. ✓
3. **AQUAL-EFE shares the SAME d-structure.** The premise "a scalar has no inertia-tensor response, so δI_ij is
   distinctive for the d-question" is FALSE for the d-STRUCTURE. AQUAL with the external-field effect (Milgrom 1986)
   linearizes to an anisotropic kinetic operator μ·(δ_ij + L·n̂_in̂_j), L = dln μ/dln x — a SYMMETRIC δ+nn structure with
   EXACTLY the same one-direction d-geometry as δI_ij, in every d (verified L = 1/(1+x²) for μ=x/√(1+x²)). A scalar also
   carries the symmetric tidal tensor ∂_i∂_jΦ. So the tensor d-dependence is SHARED, not distinctive. ✓
4. **The lone bivector (Thomas a∧w) is d-agnostic; d=3 only renames it.** |a∧w| = |a||w|sin θ is one 2-plane, defined
   with dimension-independent magnitude for all d≥2, acting on the spin through the boost–spin 2-plane identically in
   every d. In d=3 ONLY (#vec=#bivec=3) can it be Hodge-dualized to the pseudovector a×w. That dualization is the SOLE
   place d=3 enters anywhere in the MI-tensor content — and it is **notation**, a bivector→vector rename, not a
   constraint. Even there the physics (a frame-dragging-like spin reorientation) survives in d≠3 as a bivector rotation
   rate; only the axial-vector packaging is d=3-special, and it is shared by every rank-2 source (tidal, J₂ oblateness),
   NOT framework physics. ✓
5. **Below floor.** δI/I ~ (1−μ)(g)·β² is O(β²): ~7.6×10⁻⁷ at a~a₀ (1−μ~½), ~1.2×10⁻¹⁴ in the Solar System (a≫a₀) —
   below every current SME floor. The only near-floor observable is the O(β) s̄^TX DIPOLE (~6×10⁻⁴ at a~a₀, ~9.6× under
   INPOP/Cassini conservative), and that is a VECTOR (d-agnostic structure), tested only in its β-suppressed projection.
   α₂ ~ a few ×10⁻¹³, ~10⁶× safe under Nordtvedt. ✓

## The decisive both-ways test — CONSTRAINT or smooth coefficient?

**Does anything in the MI-tensor content become ill-defined / inconsistent at d≠3?** **NO.** The trace projector 1/d is
finite for all d≥2; the sym2-traceless irrep (d−1)(d+2)/2 is a positive integer and non-degenerate for all d≥2; the
vector dipole (d components) and bivector precession (d(d−1)/2 components) are smooth polynomials. Nothing diverges,
vanishes, or becomes inconsistent off d=3. **That is the signature of decorative, not load-bearing.** Moreover, any
rank-2 boost effect — even special-relativistic inertia-tensor contraction ~β² — has the identical Sym²(vector)
d-structure and (1−1/d) factor, so the d-dependence is not even MI-distinctive.

## Smuggle-guard ledger (the three guards the prompt named)

| Guard | Question | Finding |
|---|---|---|
| (i) vector↔bivector smuggle | Does d=3 enter by assuming a 3-vector / cross-product / curl, or is SO(d) load-bearing? | **Notational.** The distinctive δI_ij and the live s̄^TX are symmetric/vector — the self-duality (antisymmetric statement) never touches them. The lone bivector a∧w is d-agnostic; d=3 only Hodge-dualizes it to a×w. |
| (ii) constraint vs coefficient | Is the d-dependence a real constraint (anisotropy ill-defined off d=3) or a smooth coefficient? | **Smooth coefficient (1−1/d).** Every sector well-defined and non-degenerate for all d≥2. Nothing inconsistent at d≠3. |
| (iii) AQUAL mimicry | Does a scalar really not share the d-dependence? | **AQUAL-EFE shares it.** μ·(δ_ij + L·n̂_in̂_j) is the same symmetric δ+nn one-direction d-geometry in every d. The genuine MI-vs-MG difference is WHICH acceleration (internal self-field vs external) and the precession sign / relational σ-spread — both a₀-degenerate, NOT a d-selection. |

## Both ways

- **CREDIT (full weight):** the MI-tensor content IS genuinely distinctive vs a pure scalar in **WHAT it is** — a
  velocity/boost-dependent inertia-tensor and Thomas-precession response that a scalar AQUAL/MG value has no analogue of
  (a scalar has a standard-GR matter sector with isotropic mass; its rank-2 tidal tensor ∂_i∂_jΦ is sourced by external
  field geometry, not by the body's boost relative to the cosmic frame u^μ). The EXISTENCE of the anisotropy does break
  the scalar degeneracy — this is the SME ledger's preferred-frame content — and the s̄^TX dipole is a real near-term test
  (~9.6×). The framework is right that AQUAL modifies gravity, not inertia.
- **CONCEDE (the decisive point for the d=3 question):** the **d-dependence** of that anisotropy is a SMOOTH coefficient
  (1−1/d), NOT a constraint; AQUAL-EFE shares the same symmetric δ+nn d-structure; the effect is O(β²) below every floor;
  and the dim SO(d)=d self-duality is used **nowhere as physics** — only to Hodge-dualize the one genuine bivector (a∧w)
  into a×w. The route flagged by the prior verdict as the **only** possible non-decorative path to a dim SO(d) constraint
  ALSO comes back smooth-in-d / decorative for the dimension question. Z²=32π/dim SO(3) remains a re-labeling of 32π/3.

## HONEST CEILING (regardless of the (A)/(B) call)

Even had this come back (A), it would have been a **gravity-side consistency/selection** insight on framework-distinctive
content, **NOT a from-below derivation of d=3** (nothing here explains *why* space is three-dimensional) and **NO
flavor/particle/TOE bridge** (consistent with the closed particle-numerology and TOE-path standing — the cosmology trick
does not transfer to the SM). The honest prior in the prompt — β-suppressed, below floor, likely smooth/decorative — is
**vindicated**. Quarantine held: a₀ is the input throughout; nothing SM-side derived; d=3 entered only as the target.

## One line

The framework-distinctive MI-tensor content (inertia-tensor anisotropy → s̄^TX dipole + α₂ precession) is real
modified-inertia physics a scalar lacks, but its d=3 self-duality is NOTATIONAL: the anisotropy is symmetric and the live
dipole is a vector (sectors the self-duality never touches), the one genuine bivector (Thomas a∧w) acts identically in
every d with d=3 only Hodge-dualizing it to a×w, AQUAL-EFE shares the same δ+nn d-structure, and the whole effect is
O(β²) below floor — nothing becomes inconsistent at d≠3, so the MI tensor adds **no load-bearing dim SO(d) constraint**.
**STAYS-PARTIAL / decorative.**

## Ledger

| Claim | Verdict |
|---|---|
| MI inertia-tensor anisotropy exists & is scalar-distinct in WHAT it is | **TRUE** (preferred-frame, boost-dependent; SME content) |
| δI_ij anisotropy = ε·(ŵ_iŵ_j − δ_ij/d), symmetric-traceless | **EXACT** all d (⟨(r̂·ŵ)²⟩=1/d verified d=2,3,4) |
| s̄^TX live dipole is a VECTOR (l=1), not a bivector/Hodge dual | **CONFIRMED** (d-agnostic structure) |
| The d-dependence requires d=3 / dim SO(d)=d | **NO** — smooth (1−1/d); nothing ill-defined off d=3 |
| AQUAL-EFE shares the δ+nn tensor d-structure | **YES** (μ(δ_ij+L n̂n̂), L=1/(1+x²)) |
| Lone bivector a∧w (Thomas/α₂) needs d=3 | **NO** — d-agnostic; d=3 only Hodge-dualizes (rename) |
| Effect observable / above floor | **NO** — δI/I O(β²), ~10⁻⁷ at a~a₀, ~10⁻¹⁴ at 1 AU; only s̄^TX (O(β), vector) near-floor |
| Z²=32π/dim SO(3) becomes non-decorative | **NO** — still a re-label of 32π/3 |
| From-below d=3 derivation / flavor-TOE bridge | **NONE** |

**NET: STAYS-PARTIAL.** The MI tensor anisotropy is well-defined for any d, the self-duality is only a notational
convenience (bivector→vector Hodge dual), AQUAL shares the d-dependence, and the effect is below floor. The d=3 lead
stays PARTIAL; the self-duality is decorative. This CONFIRMS and SHARPENS `D3_SELFDUALITY_VERDICT_2026-06-25.md`.
