# LEMMA doorC — the sharpest next lemma attempt: the exact Jacobi face of the
# single-plaquette model, the O(x⁻³) cancellation, and the precise obstruction
# to a uniform-in-coupling gap

Status line: **L1 PROVEN** (exact structure), **L2 PROVEN** (rigorous two-sided bound with
explicit constants), **L3 ATTEMPTED, NOT PROVEN** — the uniform-in-coupling single-plaquette
gap is *within reach*; its exact obstruction is stated in §5. No fake proof anywhere: every
claimed theorem below has a complete argument; the only theorem-shaped object that is not
proven is labelled as such and its missing step is named.

Model (single plaquette, SU(2), Kogut–Susskind, lattice spacing a=1):

    H = (x/2)·Σ_{ℓ=1}^{4} C_ℓ + (β/x)·(1 − (1/2) Re tr U_p),     x = g²,
    x > 0, β ≥ 0 (displayed lane value β=2; the certified I15 bound uses β=2N).

All facts here are derived, not quoted.

---

## L1. The exact Jacobi (half-line) representation — PROVEN

**Theorem L1.** Let ℋ be the physical (gauge-invariant) Hilbert space of the single
plaquette. ℋ ≅ L²(class functions on SU(2)) and the characters {χ_j : j = 0, 1/2, 1, …}
form an orthonormal basis (Peter–Weyl). With |n⟩ := χ_{n/2} (n ≥ 0) the Hamiltonian acts as
the real symmetric half-line Jacobi matrix

    H|n⟩ = [2x·j_n(j_n+1) + β/x]·|n⟩ − (β/(2x))·(|n−1⟩ + |n+1⟩),    j_n = n/2,   |−1⟩ := 0,
    i.e. d_n = x·n(n+2)/2 + β/x on the diagonal, constant off-diagonal a = −β/(2x).

**Proof.** (1) Gauge fixing a spanning tree of the square leaves a single holonomy U;
physical states are class functions f(U) = f(gUg⁻¹) (PROOF.md §3; standard single-loop
reduction, cf. Ligterink–Walet–Bishop hep-lat/0001028). (2) Peter–Weyl: the characters of
SU(2), χ_j with dim = 2j+1, are an orthonormal basis of the class functions; the Casimir in
the normalization tr(t_a t_b) = δ_ab/2 acts as C₂ χ_j = j(j+1)χ_j (C₂(1/2) = 3/4 = C_F ✓).
(3) Electric sector: each of the four links contributes (x/2)C_ℓ, so
(x/2)·ΣC_ℓ χ_j = 2x·j(j+1)χ_j (each link Casimir gives C₂(j) on the reduced model — the
recorded single-loop identity, PROOF.md §3). (4) Magnetic sector: for SU(2) the fundamental
is self-conjugate, so Re tr U = χ_{1/2}(U), hence (β/x)(1 − (1/2)Re tr U_p) acts by
multiplication with T := (β/x)(1 − (1/2)χ_{1/2}). (5) The product rule
χ_{1/2}·χ_j = χ_{j+1/2} + χ_{j−1/2} (Clebsch–Gordan 1/2 ⊗ j, multiplicity-free; χ_{−1/2} ≡ 0)
gives Tχ_j = (β/x)χ_j − (β/(2x))(χ_{j+1/2} + χ_{j−1/2}). Orthogonality kills all other
matrix elements: H is tridiagonal with the stated entries. ∎

*Remarks.* (i) L1 is new in-repo and is the exact, checkable kernel behind every
single-plaquette statement: it turns the model into one explicit symmetric tridiagonal
matrix on ℓ²(ℕ₀) — a discrete Schrödinger operator with linearly growing diagonal and
1/x-scaled hopping. (ii) Equivalently, in the angle parametrization of SU(2) class
functions, H is a Mathieu-type operator (a − (d²/dθ² + cot·d/dθ)-type Casimir with
(β/x)(1−cosθ)); this is why the model is exactly solvable numerically (truncated Jacobi),
and why it *never* collapses: the magnetic operator is bounded (‖T‖ ≤ 1) on a compact
group, and the discrete character ladder has isolated levels. (iii) T = (1/2)χ_{1/2} is
purely off-diagonal in the character basis, so the magnetic dressing of every diagonal is
second-order — this is the mechanism of L2.

## L2. The magnetic shift cancels to first order: gap = 3x/2 + O(x⁻³) — PROVEN

**Theorem L2.** Let gap(x) = λ₂ − λ₁ be the spectral gap of H in L1. For all β ≥ 0 and
x² > β,

    3x/2 − 2ρ(x) ≤ gap(x) ≤ 3x/2 + β²/(3x³) + 2ρ(x),     ρ(x) := β² / ( 2x³(5 − 4β/x²) ).

In particular gap(x) = 3x/2 + O(x⁻³) as x → ∞: the certified bound's magnetic drag β/x
**cancels exactly at leading order** — the true gap exceeds both the lane's 2N/x bound and
the min–max bound 3x/2 − β/x by ~β/x + O(x⁻³).

**Proof.** Write H = D + V with D = diag(d_n), d_n = 2x·j_n(j_n+1) + β/x, and V the
off-diagonal Jacobi part; ‖V‖ ≤ β/x (row sums 2|a| = β/x). Let P project onto the cluster
C = span{χ_0, χ_{1/2}}, Q = 1−P, and W = QVP + PVQ (‖W‖ = β/(2x)).

*Step 1 (separation).* The cluster block P(D+V)P is the 2×2 matrix
[[β/x, −β/(2x)], [−β/(2x), 3x/2 + β/x]], with eigenvalues λ_± = (3x/4 + β/x) ∓
(1/2)√((3x/2)² + β²/x²) ⊆ [β/(2x), 3x/2 + 3β/(2x)] (Gershgorin on the block). The excited
band Q(D+V)Q has all eigenvalues ≥ 4x (Gershgorin: min diagonal 4x + β/x at |2⟩, row norm
β/x). Hence the spectral separation between cluster block and excited band is at least

    Δ := 4x − (3x/2 + 3β/(2x)) = 5x/2 − 3β/(2x) > 0 for x² > 3β/5.

*Step 2 (cluster bound).* With ‖W‖/Δ < 1/2 (i.e. β/(2x) < Δ/2 ⇔ x² > β, our hypothesis),
Schur complementation (Grushin/block Jacobi; the eigenvalues of H in the cluster window are
the zeros of det[P(D+V)P − z − W(z − Q(D+V)Q)⁻¹W] up to the analytic remainder, which
moves the roots by at most ‖W‖²/(Δ − ‖W‖)) gives exactly two eigenvalues λ₁, λ₂ of H with

    |λ₁ − λ_−| ≤ ρ,  |λ₂ − λ_+| ≤ ρ,  ρ := ‖W‖²/(Δ − ‖W‖) = β²/(2x³(5 − 4β/x²)).

(The denominator: Δ − ‖W‖ = 5x/2 − 3β/(2x) − β/(2x) = 5x/2 − 2β/x = (x/2)(5 − 4β/x²).)

*Step 3 (evaluate).* λ_+ − λ_− = √((3x/2)² + β²/x²). Lower: ≥ 3x/2. Upper:
√(s² + t²) ≤ s + t²/(2s) at s = 3x/2, t = β/x gives ≤ 3x/2 + β²/(3x³). Therefore

    gap = λ₂ − λ₁ ≥ (λ_+ − λ_−) − 2ρ ≥ 3x/2 − 2ρ,   and
    gap ≤ (λ_+ − λ_−) + 2ρ ≤ 3x/2 + β²/(3x³) + 2ρ.   ∎

**Corollary (vs the certified numbers).** β=2, x=2 (allowed, x²=4>β): gap ≥ 3 − 2ρ = 3 − 1/6
= 17/6 ≈ 2.833. This dominates the min–max bound 3x/2 − β/x = 2 *and* the certified
2N/x bound = 1. The exact gap at that point is 3.114 (verify_doorC.py), consistent.
For β=2N=4, x ≥ 2.01: gap ≥ 3x/2 − 2ρ with ρ = 16/(2x³(5−16/x²)).

**Machine check:** `verify_doorC.py` §D verifies the two-sided inequality on grids
x ∈ [2.008, 60] for β ∈ {1, 2, 4} against direct eigensolves of the truncated Jacobi
(J = 400): PASS. (Truncation is used only as a numerical test; the theorem itself is the
proof above.)

## L3. The uniform-in-coupling bound — ATTEMPTED, NOT PROVEN (precise obstruction)

**Target statement (the sharpest lemma we identified).** For the single-plaquette SU(2)
model with β = 2 (lane display), there is a constant c > 0 with gap(x) ≥ c for *every*
x > 0. Numerically the truth is c ≈ 2.196 (min at x ≈ 0.99, truncation-stable; §E of
verify_doorC.py), with finite band-bottom limits λ₁ → 2.12, λ₂ → 4.95 as x → 0.

**Where the elementary routes terminate (the obstruction, exactly).**

1. *Min–max/Gershgorin route.* gap ≥ 3x/2 − β/x (λ₂ ≥ λ₂(H_E) = 3x/2 — H ≥ H_E — and
   λ₁ ≤ ⟨1,H1⟩ = β/x) goes negative for x < √(2β/3): the vacuum-side bound is too poor.
   Gershgorin on the excited compression recovers only the same 3x/2.
2. *Perturbation route.* L2's cluster analysis is a *large-x* tool: its hypothesis x² > β
   is precisely the smallness of the hopping relative to the electric spacing. In the
   crossover x ~ 1 the hopping β/(2x) and the electric level spacing 3x/2 are comparable —
   no convergent small-parameter expansion exists around either end (the magnetic band
   width 2β/x and the electric gap 3x/2 cross).
3. *What the crossover is.* As x → 0, H = (β/x)(1−T) + 2xC_E: the problem is the half-line
   Jacobi with *large constant* hopping, i.e. a discrete Mathieu operator in the deep-band
   regime; the two lowest states sit at the band bottom with a localization length set by
   the electric well, and λ₁, λ₂ → finite positive limits (band-bottom eigenvalues of a
   bounded perturbation of a Toeplitz half-line chain). A rigorous lower bound requires a
   **continued-fraction / Sturm–Liouville (discrete) estimate**: e.g. proving that the
   continuant sequence at energy 3x/2 + c has exactly one sign change for all x (i.e. the
   number of eigenvalues below 3x/2 + c is exactly one), with constants uniform in x —
   equivalently a discrete-virial or commutator argument showing the ground-state support
   cannot delocalize in the chain. These are classical techniques (Mathieu gap theorems,
   Gautschi-type continued-fraction bounds), but a *correct, explicit, uniform-in-x*
   version is a several-page analytic effort that this opus did not complete.
4. *Consequence for the frontier.* The single-plaquette model *does* have a uniform gap
   (numerically: c ≥ 2.196); but this fact is a **toy fact** — it uses the compactness of
   SU(2), the boundedness of ‖T‖, and the discreteness of the character ladder, all of which
   are washed out in the thermodynamic limit, where the scaling-window problem (R5/R6)
   lives. Proving L3 would certify the toy; it would *not* move R5/R6 by itself (MAP.md §4).

**Honest verdict.** L1 and L2 are proven and machine-checked. L3 is the sharpest genuinely
reachable statement on this toy frontier, it is not proven here, and the precise reason is
stated above: the crossover regime x ~ 1 has no small parameter in the Jacobi data, so a
uniform bound needs a discrete spectral-analysis (Sturm/virial) argument that remains to be
written. This is the strongest true statement this opus can certify — no stronger claim is
made.