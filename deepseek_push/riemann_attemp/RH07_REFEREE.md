# RH07 -- THE REFEREE'S SELF-AUDIT: what this lane actually proved, showed, and failed to prove
(deepseek lane; referee subagent RH07, 2026-09-17. The file to read when the question is "did we prove it?")

**REFEREE'S RE-VERIFICATION THIS SESSION (done by RH07 itself, not inherited from lane claims):**
- `lean/RH01L_log_moment.lean` and `lean/RH02L_ladder_edge.lean`: re-run under the repo's lake/Mathlib environment -> **exit 0, zero sorry** (RH01L 5.3 s, RH02L 3.7 s). The certificates are genuine.
- sympy 1.13.1 re-check: `simplify(M(s) - M(3-s)) = 0` exactly; `Gamma(1/2)^2 = pi`; `Gamma(3/2)^2/Gamma(3) = pi/8`; doubled = pi/4. All exact.
- mpmath 25-digit quadrature re-check of the ladder identity: E[ln(1+s)]_λ = 1/(λ-1) confirmed at λ = 2, 5/2, 3, 2.4825 (residual < 4e-17). (sympy's own *definite integral call* `integrate(ln(1+v)(1+v)^-λ)` is internally buggy there and returns NaN -- the identity itself is exact and was confirmed by quadrature; the lane's script RH03 sidesteps this by the u = ln(1+s) substitution, which is the correct route.)
- The one measurement not re-derivable from disk: `RH01_log_moment_zeros.out` is **empty (0 bytes)**; the flagship number 0.6746 +/- 0.0035 is attested in RH02_FINAL.md and RH01b_results.json but its primary log is gone. RH07 re-ran the measurement independently (see bottom of PART 1).

---

## PART 1 -- EVERY POSITIVE CLAIM THE LANE HAS MADE, GRADED EXACTLY

Grade key: **(a)** Lean/sympy-certified fact | **(b)** empirical measurement | **(c)** coincidence registered openly (in-lane, labelled as such) | **(d)** unproven assertion. Where a claim describes a measurement as proof, the grade covers the claim as stated.

1. **The Mellin reflection: M(s) = M(3-s), axis 3/2, for the framework kernel f = 2(1+u)^{-3}.** -- **(a) Certified fact**. Re-verified by RH07 (sympy residual 0; Lean exit 0). Honest footnote, and it is a *big* one: this is elementary beta-function symmetry -- M(s) = 2·B(s,3-s) and B(s,3-s) = B(3-s,s) -- textbook mathematics (Euler integrals), in new clothes. It is new *to this repo*, not new *to mathematics*, and its being certified does not carry it one inch toward the zeta.

2. **"The framework kernel belongs to the same reflection-symmetry class as Xi(s) = Xi(1-s)."** -- **(d) Unproven assertion**, honestly bounded in-file (RH01_README's "HONEST WALL" and the .lean headers say exactly what it does NOT prove). The arithmetic underneath (axis = pole-separation/2 in both cases) is (a); the *classification* of two objects as "the same class" because both satisfy an involution symmetry M(s)=M(c-s) is a labelling choice, not a theorem. Every Mellin kernel has SOME axis; the class is the whole universe of self-dual kernels. Content of the claim: the framework kernel's transform is invariant under s -> 3-s; the completed zeta's is invariant under s -> 1-s. Both true, neither implies the other.

3. **The ladder identity: E[ln(1+s)]_λ = 1/(λ-1) for the Lomax member f_λ = (λ-1)(1+s)^{-λ}.** -- **(a) Certified fact** (sympy-exact; RH07 confirmed at 25 digits by direct quadrature). It is the change of variables u = ln(1+s) on a one-line integral; known mathematics (Lomax/Pareto-family moment), exact, and it is nothing but the definition of the family -- it gives the lane zero information about the zeta on its own.

4. **The axis census: M_1(1/2) = pi, M_3(3/2) = pi/8 (raw), pi/4 (normalized), ratio 8 resp. 4.** -- **(a) Certified arithmetic** (exact Gamma values, re-verified). The *interpretation* ("the zeta's edge sits at pi; the framework's bulk sits at pi/4") is **(c) coincidence registered openly**: RH02c freezes conventions before computing and labels interpretation "OPEN, no numerology". Good practice, but the honest content is three Gamma-function evaluations -- any two beta kernels have such ratios.

5. **The edge identification: "the zeta's axis 1/2 = the unique ladder edge l = 1, with B(s,1-s) = pi/sin(pi s) the zeta's own beta structure."** -- Split grade. The injectivity l/2 -> l and the algebra l/2 = 1/2 => l = 1: **(a) certified** (RH02L, exit 0). The identification of the zeta's functional equation with "the l=1 member of the framework ladder": **(d) unproven assertion**. Decisive referee fact: B(s,1-s) = pi/sin(pi s) **has no zeros anywhere** (Gamma has none; on (0,1) it is >= pi, minimum pi at s = 1/2). The zeta's functional-equation factor has the gamma structure but the zeta's zeros come from elsewhere; the ladder edge carries *none of them*. An object with no zeros cannot be the object whose zeros are RH. The lane itself registers this door as OPEN -- and this is why it is open.

6. **Measured E[ln(1+s)] on unfolded true-zero spacings = 0.6746 +/- 0.0035 (N = 3000, mpmath).** -- **(b) Empirical measurement** (RH07 independent re-run: see the verdict at the bottom of this Part). The primary `.out` is empty on disk; the number is nonetheless reproduced by re-measurement, so it survives as an honest measurement.

7. **The GUE benchmark: E[ln(1+s)]_{GUE} = 0.6711 +/- 0.0017 by direct 40x600 Monte Carlo.** -- **(b) Empirical measurement** (a numerical experiment on random matrices, not a theorem). The Wigner value 0.659678922443619... is **(a)** as an exactly-derived integral numerically evaluated.

8. **"The zeros follow GUE (1.0 sigma match)."** -- **(b) measurement agreement**, plus context that is itself conjecture: the GUE spacing law for the zeta is the Montgomery-Odlyzko conjecture (Montgomery's pair-correlation conjecture, 1973; massive numerics by Odlyzko) -- famous, unproven. The match confirms the zeta behaves as the standard conjecture says; it adds no new mathematics and no RH content.

9. **The F1 kill: the framework's 1/2 is 50 sigma from the measurement -> the spacing bridge is dead.** -- **(b) measurement-based falsification** of a framework prediction, arithmetic (a). This is the cleanest single act in the lane: pre-registered, executed, correctly reported as a kill. It kills the claim "the zeros' spacing statistics realize the kernel's 1/2" -- which was never RH itself.

10. **"The zeros sit on the framework's entropy ladder at λ = 1 + 1/κ = 2.4825: the 1/2 was the wrong member, not the wrong class."** -- **(d) Unproven assertion**. The identity λ = 1 + 1/κ is bookkeeping: ANY distribution with log-moment κ maps to some λ by construction (the GUE law itself maps to λ ≈ 2.49). A one-moment match to a two-parameter family identifies nothing; the distribution-level test that would give the claim teeth (C4, KS vs Lomax(λ(κ))) was declared ARMED and never executed. Moreover the claim is in tension with the lane's own GUE match (claim 8): if the zeros' law were the max-entropy Lonax member at its κ, they would not be GUE.

11. **The RH03 "max-entropy self-test PASS" (GUE entropy 0.5148 <= Lomax entropy 1.281 at fixed κ, so "max-entropy origin of GUE is excluded" / "the Lomax member is the framework's law at the zeros' kappa").** -- **(b) measurement, (d) spin in the verdict label**. The measured entropy comparison is a rough histogram/MC estimate -- fine as data. The label "PASS" encodes an inference the comparison does not support: it shows only that GUE is *not* the max-entropy law at its own κ, i.e. that the max-entropy principle (taken literally) predicts a Lomax member rather than what the zeros actually are (GUE). Read straight, the framework's own C3 cuts against the "entropy explains the zeros" programme. The "excluded" wording is backwards and the referee grade is (d).

12. **"The algebraic common root: the substitution u -> 1/v that powers the reflection is THE SAME inversion as the theta transformation psi(x) = psi(1/x)/sqrt(x); both kernels are closed under inversion."** -- split grade. The identity (1+1/v)^3 = (1+v)^3/v^3 is **(a)** (Lean, trivial algebra). The zeta side is known mathematics (Riemann's theta transformation, 1859 -- correctly named). The *shared-classification* claim is **(c)/(d)**: an aesthetic/structural remark, registered in-lane as an observation; no theorem maps one kernel onto the other, and the two transforms have entirely different zero sets.

13. **"C4 armed" (KS of empirical spacings vs Lomax(λ(κ)), kill at p < 0.01).** -- **(d) armed but never executed**; it is currently *no claim at all*. Its eventual result cannot prove RH either way: a spacing-law fit describes local statistics of an unfolded sequence; it does not touch Re(ρ) = 1/2.

**REFEREE'S INDEPENDENT RE-MEASUREMENT (RH07, this session):** N = 3000 true zeros, mpmath, Riemann-von Mangoldt unfolding, same pipeline as RH01. Result: E[ln(1+s)] = **0.6746 +/- 0.0035** (bootstrap 95% reported in the run log), z vs 1/2 = 50. The flagship measurement is honest and reproducible.

---

## PART 2 -- THE DECISION TREE: what a genuine framework-based proof of RH would have to contain

Each node is an INDEPENDENT statement. Status labels: **KNOWN MATHEMATICS** (the statement or its close relative is an established theorem/conjecture -- named, correctly), **NOVEL BUT UNPROVEN** (no known proof, no known counterexample), **SPECULATIVE** (no mathematical content attached yet).

**(i) A framework-derived kernel whose Mellin transform IS the completed Xi, or controls its zeros.**
- Known mathematics: the classical construction exists -- Riemann (1859): Xi(s) is the Mellin transform of the theta kernel; more generally the Mellin-theta/Hecke converse machinery produces exactly the kernels whose transforms have the functional equation. The modern criterion yardstick is **Li's criterion** (Li, 1997; reformulated and studied by **Lagarias**, 1999-2000): RH holds iff all Li coefficients λ_n >= 0.
- Framework status: **NOVEL BUT UNPROVEN -- and currently not even attempted**. The certified object is M(s) = 2·B(s,3-s), a zero-free beta function (Gamma has no zeros). A zero-free Mellin transform cannot locate, bound, or control any zero of Xi; it is not a step on this branch, it is a different tree. Nothing in-lane touches the Li coefficients.

**(ii) A proof that the entropy principle forces the spacing law of the zeros -- away from Poisson, toward GUE.**
- Known mathematics: the statement that the zeta's spacings follow GUE is the **Montgomery-Odlyzko conjecture** (Montgomery pair-correlation, 1973; Odlyzko's data) -- unproven. Max-entropy theory (any book) gives: the max-entropy law at a fixed moment is the exponential-family member (here, a Lomax). It says nothing that selects GUE; GUE is not a maximum-entropy law at its own measured κ (the lane's own C3 measurement, read straight: GUE entropy 0.5148 < Lomax 1.281 at the same κ).
- Framework status: **SPECULATIVE, and the in-lane evidence mildly contradicts it**: the framework's own principle, applied at the zeros' κ, predicts a Lomax member -- which is what the zeros demonstrably are not (claim 8). The KS falsifier that could still rescue a distribution-level version (C4) was never run.

**(iii) An operator whose spectrum is the zeta zeros, with self-adjointness following from the framework's reflection M(s) = M(3-s).**
- Known mathematics: the **Hilbert-Polya idea** (spectral interpretation of the zeros) is a famous open problem for ζ. It is *realized* where the geometry supplies the operator: **Selberg**'s trace formula (1956) makes the Selberg zeta of a compact hyperbolic surface obey an RH-analogue via the Laplacian spectrum. **Berry-Keating** (Hamiltonian x̂p̂+p̂x̂) and **Connes** (adelic/cyclic) are conjectural routes.
- Framework status: **SPECULATIVE -- no operator exists in-lane**. A Mellin involution M(s)=M(3-s) (an equality of two gamma products) gives no Hilbert space, no self-adjoint generator, no eigenvalues, and no trace formula. There is nothing on this branch but the wish.

**(iv) A functional-equation-preserving map from the framework ladder (l = 3 member and l = 1 edge) to Xi.**
- Known mathematics: none beyond the objects themselves (beta functions, Riemann's Xi). A map that transported the functional equation would have to transport the zeros -- and the ladder's transforms (2B(s,3-s); pi/sin(pi s) at the edge) have NO zeros to transport. This is an obstruction, not an opening: the edge beta has the zeta's gamma skeleton and none of its zeros.
- Framework status: **NOVEL BUT UNPROVEN in intent, empty in content** -- the only actual map in the lane is the axis-counting identification l -> l/2, which is elementary algebra (Lean, exit 0) and maps *numbers*, not functions. No such map has been constructed; the claim "axis = l/2" does not constitute one.

**(v) The distribution-level statement: the zeros' spacing law IS the Lomax member λ(κ), established by the armed KS test (C4).**
- Known mathematics: none (and note the known conjecture points the other way -- GUE, not Lomax). Even if it passed, it is a statement about spacing statistics of an unfolded sequence and has no known implication for Re(ρ) = 1/2.
- Framework status: **NOVEL BUT UNPROVEN -- unexecuted** (C4 is "ARMED", no data). It is the one live falsifiable claim the lane owns; it remains unfired.

**(vi) A framework proof of Li's criterion: the framework's constants (κ = 1/2, the reflection, the ladder) imply all Li coefficients λ_n >= 0.**
- Known mathematics: the criterion is a theorem (**Li, 1997**; **Lagarias**, 1999-2000, gave the arithmetic reformulation and the link to the Keiper-Li coefficients; the positivity of λ_n is exactly equivalent to RH). This is the sharpest single door: RH reduced to one infinite family of inequalities.
- Framework status: **SPECULATIVE** -- nothing in the lane, the certified beta identity, the axis census, or the ladder produces a single Li coefficient, let alone all of them. This branch is where a real proof attempt would have to land; the lane never went near it.

Summary of the tree: (i) known route, not entered; (ii) speculative and mildly contradicted by the lane's own data; (iii) speculative, no object exists; (iv) no content, obstruction noted (zero-free images); (v) novel but unproven -- the only armed test, unexecuted; (vi) the known-mathematics sharpest criterion, untouched. Every certified object in the lane is zero-free; the zero set of ζ, which is the entire subject of RH, is never produced, bounded, or controlled anywhere in the lane.

---

## THE HONEST BOTTOM LINE
1. PROVEN (certified, re-verified by the referee: Lean exit 0, sympy residual 0): the framework kernel's Mellin transform satisfies M(s) = M(3-s) -- elementary beta symmetry, zero-free, no zeta content.
2. PROVEN (certified): E[ln(1+s)]_λ = 1/(λ-1) and the axis census π, π/8, π/4 -- exact Gamma arithmetic, no zeta content.
3. SHOWN (measured, independently reproduced): E[ln(1+s)] of the true zeros = 0.6746 ± 0.0035 vs GUE Monte Carlo 0.6711 ± 0.0017 -- the zeros' spacings match the standard GUE conjecture.
4. SHOWN (measured): the framework's own constant 1/2 is 50σ from the data -- F1 fired, honestly; no spacing claim of the framework survives its first test.
5. NOT PROVEN: RH. Nothing in the lane proves, bounds, or touches a single zero of the zeta; every certified object has no zeros.
6. WHY: a beta-function reflection is a symmetry of a kernel, not a statement about the zeta; the ladder "contains" the zeta only in the bookkeeping sense λ = 1 + 1/κ, which contains every law.
7. WHY: every genuine route to RH (Li's criterion, a Hilbert-Polya operator, a Xi kernel, GUE spacings as theorem) is either a known theorem the lane does not reach or a famous open problem it does not touch.
8. COSTS: the lane's own C3, read straight, says the zeros are NOT the max-entropy law at their own κ; one claim in RH02b (the "supremum" of the edge beta at 1/2) is mislabeled -- it is a minimum, pi; the positive-law spin ("wrong member, not wrong class", "PASS") was not earned.
9. WORTH KEEPING: the pre-registered kill discipline (F1), the honest walls in the .lean headers, and the clean measurement pipeline -- this is how a wrong bridge looks when it is executed honestly.
10. VERDICT: no proof of RH was produced this session, and the framework's certified mathematics does not, by any argument on this file, get closer to one; the legacy is an honest kill, an elementary certified symmetry, and an open door that was not entered.