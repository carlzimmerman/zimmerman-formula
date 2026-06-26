# MI-tensor d=3 self-duality: SKEPTIC verdict — DECORATIVE/NOTATIONAL (2026-06-25)

*Final probe on the d=3 thread, gravity side. The d=3 verdict (`real_research/D3_SELFDUALITY_VERDICT_2026-06-25.md`)
graded the SCALAR a₀=c²√(Λ/32π) chain + flat-curve selection PARTIAL (real but standard-MOND-shared + decorative; Z²=32π/dim_SO(3)
re-labels 32π/3, no bivector in the scalar chain). It flagged the ONLY route to a non-decorative dim_SO(d) constraint:
the framework-DISTINCTIVE modified-inertia (MI) TENSOR content — the boost-induced inertia-tensor anisotropy
δI/I=(1−μ_fw)(g)(w/c)²·O(1) that induces the s^TX SME dipole and the α₂ PPN coefficient. This file stress-tests
"the MI tensor anisotropy SELECTS d=3" both ways. sympy/mpmath dps≥40. Quarantine: d=3 enters only as the target.*

scripts: `/tmp/mi_tensor_d3_test.py`, `/tmp/precession_d3_test.py`, `/tmp/aqual_shared_and_floor.py`,
`/tmp/thomas_bivector_steelman.py`. Inputs: `MI_PPN_ALPHA2_DERIVATION_2026-06-17.md`,
`S_TENSOR_SME_COMPONENT_LEDGER_2026-06-17.md`, `real_research/reviews/dsunruh_d_dimensional_derivation.py`.

---

## VERDICT: decorative-notational. The self-duality is used NOWHERE as physics — only to rename a bivector as a vector.

The MI-tensor content is genuinely DISTINCTIVE vs a pure scalar in WHAT it is (an inertia-tensor / Thomas-precession
response), but its d-DEPENDENCE is a smooth coefficient, AQUAL-shared in structure, and below floor. It adds NO new
d=3 constraint. The d=3 self-duality (#vectors=#bivectors) is a Hodge dualization, not a selector.

## Q1 — SELF-DUALITY SMUGGLE: the distinctive objects don't live where the self-duality acts

The MI-distinctive observables decompose into three tensor sectors, and the self-duality (#vec=#bivec) acts on the
ANTISYMMETRIC sector only:

| Observable | Tensor type | Sector | Self-duality relevant? |
|---|---|---|---|
| δI_{ij} inertia anisotropy | symmetric rank-2 (A·δ_{ij}+B·n_i n_j) | symmetric-traceless (d(d+1)/2−1) | NO |
| s^TX boost dipole | (T, spatial-VECTOR) of symmetric 2-tensor s^{μν} | vector (d) | NO |
| α₂ / Thomas precession | antisymmetric a∧w acting on spin | bivector (d(d−1)/2) | only DUALIZES |

- A **pure boost** supplies ONE direction n_i=w_i/|w|. The only symmetric tensors buildable from {δ_{ij}, n_i} are
  δ_{ij} and n_i n_j — both SYMMETRIC, both defined in every d. No cross product, no curl, no angular-momentum vector
  enters a pure-boost inertia response. The anisotropy lives in the symmetric-traceless irrep, which the self-duality
  (an antisymmetric statement) never touches.
- The s^TX dipole is the (T, spatial-vector) part of the symmetric spacetime tensor s^{μν}=(a₀/2|a|)(u^μu^ν−trace).
  Its spatial index is an ordinary vector index ranging over d components; no ε-tensor, no #vec=#bivec identity. d only
  sets how many spatial components exist (X,Y,Z at d=3) — a smooth count.
- The α₂ precession IS a genuine bivector: the Thomas/Wigner rotation ω_{ij}~(a_i w_j−a_j w_i)=a∧w. **But** a∧w is a
  2-form (one 2-plane), defined and acting on the spin identically in every d≥2; its magnitude |a||w|sinθ is
  dimension-independent. In d=3 ONLY it can be Hodge-dualized to the pseudovector a×w. That dualization is the SOLE
  place d=3 enters anywhere in the MI-tensor content — and it is **notation**: the physics (bivector acting on a spin
  through the boost–spin 2-plane) is identical for all d. Self-duality renames a∧w → a×w; it selects nothing and
  cannot falsify d≠3.

## Q2 — AQUAL-SHARED: a scalar theory produces the SAME symmetric d-structure

The premise "a scalar AQUAL theory has no inertia-tensor response, so δI_{ij} is distinctive" is FALSE. AQUAL with the
external-field effect (Milgrom 1986) linearizes to an anisotropic kinetic operator μ·(δ_{ij}+L·n_i n_j),
L=dln(μ)/dln(x) — a SYMMETRIC δ+nn structure with EXACTLY the same one-direction d-geometry as δI_{ij}, in every d.
The genuine MI-vs-MG difference is NOT the tensor's d-structure but WHICH acceleration sets the anisotropy (internal
self-field for MI inertia vs external field for AQUAL) and the precession sign/relational content — banked
Cassini + relational-σ-spread, both a₀-degenerate and NOT a d-selection.

## Q3 — OBSERVABLE FLOOR: the anisotropy is O(β²), below every current floor

- The distinctive anisotropy δI/I~(1−μ)(g)·β² is O(β²): at a~a₀ (1−μ~½), δI/I~7.6×10⁻⁷; in the Solar System
  (a≫a₀) it is (a₀/2|a|)β²~10⁻¹⁷–10⁻¹⁸. The only near-floor observable is the O(β) s^TX DIPOLE (~9.6× under
  INPOP/Cassini, conservative) — and that is a VECTOR (d-agnostic structure), tested only in its β-suppressed
  projection. α₂~10⁻¹³ is ~10⁶× safe. So any "d=3 selection" carried by the tensor anisotropy is in-principle-only,
  never in-practice (consistent with the banked s^TX/α₂ standing).

## Smuggle-guard (ii) — CONSTRAINT or smooth coefficient?

Decisive both-ways test: **does anything in the MI-tensor content become ill-defined/inconsistent at d≠3?** NO. All
three sectors (symmetric anisotropy, vector dipole, bivector precession) are smooth, finite, and consistent for every
d≥2. The traceless projector's only d-dependence is the 1/d trace subtraction — smooth everywhere. The MI tensor
adds NO new d=3 constraint beyond the SCALAR flat-curve cancellation (d−1)=2 (already graded
decorative/standard-MOND-shared in the d=3 verdict), and the tensor does not sharpen it. A real constraint would make
the anisotropy ILL-DEFINED off d=3; instead it is a smooth coefficient. That is the signature of decorative, not
load-bearing.

## Both ways
- **CREDIT:** the MI-tensor content IS genuinely distinctive vs a pure scalar in WHAT it is (an inertia-tensor /
  Thomas-precession response a scalar value has no analogue of), and the s^TX dipole is a real near-term test.
- **CONCEDE:** its d-DEPENDENCE is a smooth coefficient, AQUAL-EFE shares the same symmetric δ+nn d-structure, the
  anisotropy is O(β²) below every floor, and the d=3 self-duality is used nowhere as physics — only to Hodge-dualize
  the one genuine bivector (a∧w) into the familiar a×w. So the MI tensor does NOT rescue a load-bearing dim_SO(d)
  selection; the d=3 verdict's PARTIAL/decorative standing is UNCHANGED.

## One line
The framework-distinctive MI-tensor content (inertia-tensor anisotropy → s^TX dipole + α₂ precession) is real physics
a scalar lacks, but its d=3 self-duality is NOTATIONAL: the anisotropy is symmetric and the dipole is a vector (sectors
the self-duality never touches), the one genuine bivector (Thomas a∧w) acts identically in every d with d=3 only
Hodge-dualizing it to a×w, AQUAL-EFE shares the same δ+nn d-structure, and the whole effect is O(β²) below floor —
nothing becomes inconsistent at d≠3, so the MI tensor adds no load-bearing dim_SO(d) constraint. **Decorative-notational.**
