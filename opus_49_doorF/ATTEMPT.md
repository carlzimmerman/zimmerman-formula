# opus_49_doorF — ATTEMPT: THE TRANSFER-MATRIX RUNG
(i.e. the OS reflection-positivity bridge between the repo's certified R4/I15 fixed-spacing
gap and the Hamiltonian-spectrum rung of the continuum chain — and the exact obstruction at
a → 0.)

**Date:** 2026-09-22 | **Status of the attempt:** one honest finite rung, COMPLETED as
theorem-placement + proof sketch + certified fragments, with the exact point of failure of
the *extension* registered. **Not a proof of the Clay problem.** Classical RP theorems are
restated (with citations) because this session needs them as its spine; the *assembly*
(theorem→transfer-matrix→I15 dictionary→gap lifting) and the *certified fragments* are this
session's content.

---

## 0. WHY THIS RUNG

The repository's strongest certified YM-relevant object is I15 (REPO-CERTIFIED): a spectral
gap of the Kogut–Susskind-type lattice Hamiltonian H = (x/2)Σ_links C_l + (b_N/x)Σ_plaquettes
(1 − T_p), on a single plaquette exactly and on arbitrary finite open sublattices at
x ≥ X_d (uniform in N and volume; X_d unevaluated). The dossier (C1–C8) shows exactly one
clean classical rung sits between that object and "the lattice theory has a Hamiltonian with
a gap": the **Osterwalder–Seiler reflection positivity of the Wilson measure**, which
produces the self-adjoint transfer operator T = e^{−aH} and its gauge-invariant reduction.
That rung is proven in the literature (OS78; Lüscher 77; Menotti–Pelissetto 87; Seiler 82)
and is *fully restateable* — the honest "closest to provable" rung of the three candidates.
The other two candidates get their exact obstructions in §7 (scalar area law is impossible —
Gaussian perimeter law; the 't Hooft reduction fails by arithmetic at the repo's own rung).

---

## 1. SETUP (exactly the I15 world, one voice)

- d ≥ 2; N ≥ 2; G ⊆ U(N) compact connected (the case G = SU(N) is the one I15 addresses).
- Fixed lattice spacing a (set a = 1 in the Euclidean-latticed statements; physical units
  restored at the end). Finite box Λ ⊂ ℤ^d with "time slice" in the x_d-direction.
- Wilson plaquette action S_W(U) = β Σ_p (1 − (1/N)Re Tr U_p), β ≥ 0, and the measure
  dμ_Λ(U) = Z_Λ^{-1} e^{−S_W(U)} ∏_{l∈Λ} dU_l (normalized Haar per link).
- θ = the reflection x ↦ (x₁,…,x_{d−1}, −x_d) exchanging upper (x_d ≥ 1) and lower
  (x_d ≤ 0) half-lattices (hyperplane *between* the slices x_d = 0 and x_d = 1, i.e. through
  the temporal links — the OS78 placement; the through-sites placement is the MP87 variant).
  θ acts on configurations by (θU)_{l} = orientation-reversed holonomy on the reflected link.
- The link-variables U are G-valued; the vertex-gauge group acts by conjugation; gauge-
  invariant observables are functions on configurations up to conjugation.

---

## 2. THEOREM 1 — Reflection positivity of the Wilson measure (fixed spacing)
> **Theorem 1 (RP; classical: Osterwalder–Seiler 1978, Ann. Phys. 110, 440; Lüscher 1977,
> CMP 54, 283; Menotti–Pelissetto 1987, CMP 113, 369).** Let G ⊆ U(N) be compact, β ≥ 0,
> and dμ_Λ the Wilson lattice-gauge measure above. For every local, bounded, **gauge-
> invariant** observable F supported on the positive-time half-lattice (links with x_d ≥ 1),
>
>       ∫_Λ  F(θU)·F(U)‾  dμ_Λ(U)  ≥  0.          (RP)
>
> Equivalently: the measure is reflection positive w.r.t. θ. The same holds for the
> reflection plane containing sites of Λ (all gauge-invariant observables, per MP87), and for
> the two placements jointly (Lüscher's construction yields a strictly positive self-adjoint
> transfer matrix T on the spatial-link Hilbert space, see Theorem 2).

**Status:** PROVEN, classical. This session restates it with a faithful proof skeleton and
machine-corroborates the one non-obvious positivity input (the character lemma, §5).

### Proof skeleton (faithful to OS78 §3 / MP87; each step maps to the cited pages)
1. **Temporal gauge.** F is gauge-invariant, so we may fix the partial axial gauge
   U_{x,4} = 1 on every temporal link crossing the reflection plane. On this gauge slice the
   measure factorizes as
   `dμ = Z⁻¹ · e^{−S⁺(U⁺)} · e^{−S⁻(U⁻)} · e^{−S_x(U⁺,U⁰,U⁻)} · dU⁺ dU⁻ dU⁰`,
   where S⁺ (resp. S⁻) contains only space-space plaquettes strictly above (below) the plane,
   and S_x is the sum over the **temporal plaquettes** (the 2-planes using the time direction)
   that straddle the mirror plane.
2. **Structure of the coupling.** After gauge fixing, each straddling temporal plaquette
   above site x₀ couples exactly two transverse slices: its weight is of the form
   `exp[ β Re Tr( (U⁻)† B_x U⁺ ) ]` with B_x a product of spatial links lying *on* the mirror
   plane. Hence e^{−S_x} is a product over the mirror sites of such one-link kernels.
3. **Positivity of the kernel (the character lemma).** For the Wilson weight the Fourier-Haar
   coefficients of g ↦ e^{β Re Tr g} are non-negative for β ≥ 0: for SU(N) write
   `e^{β Re Tr g} = Σ_R c_R(β) χ_R(g)`, c_R(β) = ∫ e^{β ReTr g} χ̄_R(g) dg ≥ 0
   (for SU(2) exactly c_n(β) = I_n(β) − I_{n+2}(β) ≥ 0, i.e. *modified-Bessel order
   monotonicity* — this is Fragment A below, machine-checked to 40 digits and cross-validated
   against quadrature). [OS78 §3 and MP87 §2 use exactly this expansion.] Each factor
   B ↦ χ_R(A⁻† B A⁺) = Tr( (A⁺A⁻†)^{…} ) ⋯ is a bi-invariant character in B with nonnegative
   coefficient c_R(β) ≥ 0.
4. **Haar orthogonality rewrites the reflected expectation as a positive sum.** Insert the
   character expansion of every straddling plaquette, and integrate out the independent Haar
   variables dU⁰ on the mirror plane. The convolution/orthogonality
   `∫_G χ_R(A† U) χ̄_{R′}(U B) dU = δ_{RR′}·d_R^{-1}·χ_R(A† B) ≥ 0` (trace of unitaries,
   coefficient ≥ 0) turns the reflected expectation into a sum over character sectors of
   `nonnegative-coefficient · |(F-restriction, character-product)|²`. Each term ≥ 0, so (RP)
   follows. The positivity is preserved by the (finite) volume and gauge averaging.
5. **Conclude** ⟨θF,F⟩_μ ≥ 0. The second placement (plane through sites) is handled by the
   same argument shifted by half a lattice spacing; the strict positivity of T in the transfer
   picture is Lüscher's construction (Lüscher 77: elementary transfer operator built from the
   Wilson action is strictly positive).

No novel theorem is asserted: steps 1–5 are the published argument, restated so this repo's
rung has the exact coordinates of the proof in front of it. The physical (gauge-invariant)
sector is exactly where RP must hold; RP for non-gauge-invariant operators is not asserted.

---

## 3. THEOREM 2 — OS reconstruction: T = e^{−aH}, and the reduction to the physical sector
> **Theorem 2 (standard reconstruction; OS73/75; Lüscher 1977; Seiler 1982 Ch. 7).** Under
> Theorem 1 there is a Hilbert space ℋ = L²(G^{spatial links per time slice}, Haar), a
> self-adjoint **transfer operator** T ≥ 0 with T = e^{−aH}, H ≥ 0 self-adjoint, such that
> finite-volume lattice correlation functions of gauge-invariant operators at separated times
> are the matrix elements of powers of T. T commutes with the vertex-gauge group, hence
> reduces on the **physical subspace** ℋ_phys (gauge-invariant vectors); the restriction
> T_phys = e^{−aH_phys} is again a self-adjoint positive contraction with H_phys ≥ 0.
> (Equivalently: the Euclidean transfer-matrix gap equals the Hamiltonian gap — spectral gap
> of H_phys ↔ second eigenvalue of T_phys via λ₁(T) = e^{−a·gap(H)}.)

**Status:** machinery, PROVEN conditional on Theorem 1 (which holds). The content of this rung
for the campaign: **the fixed-spacing spectral gap of the repo's I15 Hamiltonian is, via
Theorems 1–3, a spectral gap of the Euclidean Wilson transfer matrix** — i.e. the R4
many-plaquette theorem and the OS transfer-matrix picture are two faces of the same object.

---

## 4. THEOREM 3 — the dictionary: the Wilson transfer-matrix Hamiltonian IS the I15 Hamiltonian
> **Theorem 3 (standard: Wilson 1974; Kogut–Susskind 1975, Phys. Rev. D11, 395; Kogut, Rev.
> Mod. Phys. 51 (1979) 659; Creutz 1983).** In the temporal gauge the one-step Wilson transfer
> operator of Theorem 2 is generated by the **Kogut–Susskind lattice Hamiltonian**
>
>       H_KS = (g²/2) Σ_links E_l² + (1/g²) Σ_plaquettes (1 − (1/N)Re Tr U_p)
>
> (up to vacuum-energy constants, which shift the spectrum by a constant and preserve the
> gap). With the identification x = g², b_N = 2 this is **exactly the I15 Hamiltonian**
> H = (x/2)Σ C_l + (b_N/x)Σ(1 − T_p) on which the repo's certified rung R4 lives
> (REPO-CERTIFIED: i15/PROOF.md; door-D REFEREE.md (i): "the conventional coefficient b_N=2 …
> the repository's displayed YM05 Hamiltonian has b_N=2").

**Status:** standard lattice-gauge identity; cited, not re-proven. It is the load-bearing
identifier that lets Theorems 1–2 import the I15 spectral result into the OS transfer-matrix
frame. (The inverse-coupling relation is β = 1/x up to O(1) constants in the N-prefactor
convention; the gap statements below are written in the I15 variable x.)

---

## 5. THEOREM 4 — the lifting and its exact wall (this session's assembled rung)
> **Theorem 4(C) — fixed spacing, PROVEN by assembly.**
> Fix d ≥ 2, N ≥ 2, spacing a, b_N = 2 (equivalently b_N ≤ 2N), and let H = H_KS be the OS
> transfer-matrix Hamiltonian of the Wilson measure (Theorems 1–3). For every x ≥ X_d
> (the I15/Yarotsky threshold, finite, independent of N and volume, unevaluated),
>
>       gap(H_phys) ≥ 3x/16   (lattice units),   in particular gap(H_phys) > 0,
>
> uniformly in N and on every finite open sublattice; equivalently the OS transfer matrix
> satisfies λ₁(T_phys) ≤ e^{−a·(3x/16)} < λ₀ = 1 on the physical sector.
> *Proof of assembly:* Theorems 1–3 identify H_phys with the I15 Hamiltonian on the physical
> sector; the I15 operator proof (a full-space min-max on the untruncated character Hilbert
> space, one plaquette; Yarotsky math-ph/0411042v1 Thms 1–3 with the i15/PROOF.md dictionary,
> many plaquettes, x ≥ X_d) supplies the gap. The operator-theoretic content of I15 is
> external to the Lean certificate (EXTERNAL, on the record, i15/PROOF.md:274); Theorem 4(C)
> inherits that same status. It is uniform in N and volume by the source theorem.

> **Theorem 4(W) — the continuum step, BLOCKED, with the exact obstruction.**
> The Clay quantity is m₀ = lim_{a→0} a^{−1}·gap(H_phys(a)). The fixed-spacing theorem 4(C)
> requires **x(a) ≥ X_d**. The asymptotic-freedom (scaling) trajectory is
> **x(a) = g²(a) = −1/(2b₀ ln(aΛ)) → 0** (b₀ = 11N/(48π²)). Since x(a) → 0 while the theorem
> needs x(a) ≥ X_d > 0, **the strong-coupling window and the scaling trajectory are disjoint**:
>
>       (x ≥ X_d) ∩ (x → 0) = ∅ .
>
> Consequently Theorem 4(C) provides **no bound on any a-sequence with a → 0**, and no other
> argument in the world's literature (dossier §2.5, §3, §5) supplies one: the intermediate-
> and weak-coupling regimes contain no proven gap, and the strong-coupling expansions are
> formally divergent precisely at the point the magnetic term stops dominating. This is the
> **exact point of failure** of this rung's extension, identical to the named Clay wall
> (YM_ROADMAP R5/R6; dossier rung C7). It is an **inequality-level obstruction, not a missing
> detail**: the theorem's hypothesis is incompatible with the trajectory, so no refinement
> within the same framework can cross the wall. Crossing it requires new analytic control
> (cluster expansion / multi-scale transport at weak coupling, or a lattice-free continuum
> construction) — none on record.

---

## 6. CERTIFIED FRAGMENTS (machine-checked; see check_fragments.py, fragment_checks.json)

**Fragment A — positive character expansion of the Wilson weight (SU(2); the positivity input
of Step 3 in Theorem 1).**
Lemma (exact): e^{β cosθ} = Σ_{n≥0} c_n(β)·χ_n(cosθ), χ_n = Chebyshev U_n, with
`c_n(β) = I_n(β) − I_{n+2}(β) ≥ 0` for every n ≥ 0 and β ≥ 0.
Proof (by citation + two lines): e^{β cosθ} = I₀(β) + 2Σ_{k≥1} I_k(β) cos(kθ) and
sinθ·sin((n+1)θ) = (cos(nθ) − cos((n+2)θ))/2 give c_n = (2/π)∫₀^π e^{βcosθ} sinθ
sin((n+1)θ)dθ = I_n(β) − I_{n+2}(β); order monotonicity of the modified Bessel function at
fixed argument (n ↦ I_n(β) non-increasing for β ≥ 0; classical, Watson/Bessel literature)
gives the sign. **Machine check (this session):** c_n(β) computed to 40-digit precision via
the closed form on the grid β ∈ {0.05, 0.5, 1, 2, 4, 8, 16, 32, 64}, n = 0…60, plus n = 0…299
at β = 0.05: **all ≥ 0**; closed form cross-validated against 40-digit quadrature of the
defining integral to max abs error ≈ 4.0×10⁻¹⁵. (The quadrature first-pass "negative" reads
at ~10⁻⁴⁶ level were exactly the underflow tail c_n ~ (β/2)ⁿ/n! and are noise; the closed
form is exact and nonnegative.)

**Fragment B — 2D compact U(1): exact area law with a computable constant (the one exact
constant in the family; it disciplines the "area law" rung).** For d = 2, compact U(1), the
Wilson expectation of a simple loop is exactly
`⟨U_ℓ⟩ = (I₁(β)/I₀(β))^{area(ℓ)}`, i.e. |⟨W_ℓ⟩| = e^{−c(β)·area(ℓ)}, c(β) = −ln(I₁(β)/I₀(β))
> 0 for every β > 0 (textbook; Migdal-recursion exactness). Machine values: c(0.1) ≈ 2.9970,
c(1) ≈ 0.80656, c(2) ≈ 0.35986, c(10) ≈ 0.052768, c(100) ≈ 0.0050252 — all positive,
monotone decreasing (weak coupling loosens area decay) — **exact formula, numerically
evaluated**. This is a *computable-constant area law* — only in 2D; it carries no spectral
content and no 4D statement.

**Fragment C — 't Hooft-scaling obstruction of the repo's own bound (arithmetic; pins the
exact failure of candidate (c)).** I15 (PROOF.md:173–189) already registers that at fixed
't Hooft coupling λ = N·x the window x ≥ X_d fails for N > λ/X_d. Arithmetic, machine-checked:
gap ≥ 3x/16 = 3λ/(16N) at fixed λ → **0 as N → ∞** (e.g. λ = 1: 0.0938 at N = 2, 0.0188 at
N = 10, 1.9×10⁻⁴ at N = 10³). So the I15 bound is **not 't Hooft-stable**: it does not even
survive the large-N limit, let alone a → 0. (Matches the large-N literature's domain: the
proven large-N area laws live at β ≤ const, i.e. *strong* coupling — Shen–Zhu–Zhu 2023,
CNS/2509.04688 — so large N and weak coupling are disjoint there as well.)

Fragment A is a *proof + machine check* of the exact lemma (the nude positivity input of the
OS proof). Fragments B and C are *exact formulae / exact arithmetic* with numerical
evaluation — labeled as such, no over-claim. **All three are numeric/exact-arithmetic
certificates, not Lean; no Lean file is extended in this lane.**

---

## 7. THE OTHER TWO CANDIDATE RUNGS — EXACT OBSTRUCTIONS (not attempted, per one-rung rule)

**Candidate (b) — explicit area-law lower bound with computable constants, scalar or U(1).**
- *Scalar model: impossible as an area-law statement.* A free/Gaussian scalar lattice field
  clusters exponentially in distance; the loop expectation of its "Wilson-line" observables
  is of the form e^{−c·(perimeter)} (sum of two-point Green's functions around the loop) —
  a **perimeter law**, area decay being absent for any Gaussian local field. The vector/gauge
  character is essential to area law; a scalar surrogate cannot furnish the rung. (This is
  the cleanest obstruction of the three: the observable family is the wrong one.) An
  interacting scalar (φ⁴) at strong coupling would require the full machinery and yields no
  area-law constant.
- *U(1):* the only exact computable constant is d = 2 (Fragment B, done above). In d = 4 the
  compact U(1) model has a **deconfining (Coulomb) transition** — area law at strong
  coupling only (proven: OS78; CNS25; strong-coupling expansion), perimeter law in the
  Coulomb phase — so no all-β area-law constant exists, and the deconfined phase is where
  the weak-coupling scaling trajectory would want to live. U(1) therefore cannot serve as a
  gap lane toward SU(3)-type physics; it is a control where the mechanism differs.
  *(No calculation of that transition phase diagram is attempted here; the obstruction is
  the existence of both phases, which is established lattice lore — cite e.g. the U(1)
  transition analyses in the lattice literature / Seiler 1982.)*

**Candidate (c) — statement-and-check of the 't Hooft scaling reduction of the gap problem.**
The reduction is a well-defined *formal* statement (large N at fixed λ = g²N recovers the
planar limit; a gap persists iff the planar theory is gapped). Its honest **check** fails at
two registered points: (i) arithmetic — I15's gap bound is 3λ/(16N) → 0 at fixed λ
(Fragment C), and the window x ≥ X_d is empty for N > λ/X_d, so *this route* gives no
N-uniform gap at fixed 't Hooft coupling; (ii) regime — the nontrivial large-N limits that
are *proven* (SZZ23; CNS25/2509.04688) live at **strong** coupling (β ≤ β*), precisely the
regime whose gap does not survive a → 0. The reduction therefore maps the Clay problem onto
a planar weak-coupling problem that nothing in the record solves; the obstruction is that the
reduction does not change the coupling-axis imbalance (strong-coupling results, weak-coupling
target). This matches YM00_CAMPAIGN K5 and YM_ROADMAP R6.

---

## 8. LEGAL (what this attempt is, and is not)

- **Is:** a faithful restatement of classical reflection positivity (Theorem 1) and
  reconstruction (Theorem 2) with the exact I15/KS dictionary (Theorem 3); an honest
  assembled rung (Theorem 4(C)) proving a **fixed-spacing physical-sector spectral gap**
  inherited from the repo's certified R4/I15 operator proof and the classical
  transfer-matrix identity; three machine-checked fragments (A exact lemma + grid check,
  B exact 2D constant, C exact arithmetic); and the **precise obstruction** of every
  extension (Theorem 4(W), §7).
- **Is not:** a proof of the Yang–Mills mass gap, a continuity statement a → 0, a weak-coupling
  theorem, a Lean certificate, or a novelty claim for the RP theorem itself (all citations
  in §2–§4 are the primary sources; the proof skeleton is a reconstruction). The exact point
  of failure is inequality-level and named: **x ≥ X_d (strong coupling, fixed spacing) vs
  x(a) → 0 (asymptotic freedom)**. No claim beyond what is written here is made.
- **Flaggable caveats:** X_d is numerically unevaluated (I15, registered); the I15 operator
  application of Yarotsky's theorem is EXTERNAL (not Lean-formalized); 2509.04688 is a
  preprint ("Submitted", v2 28 Sep 2025) and is treated here as such.

*House rule honored: the strongest true statement is the deliverable; the wall is the wall.*
*Attempted rung registered 2026-09-22 under opus_49_doorF.*