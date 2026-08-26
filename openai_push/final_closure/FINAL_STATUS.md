CONDITIONALLY_CLOSED

## Verdict

The Hamiltonian MMG candidate of the last commit (a 2-DOF tensor sector with the
static lapse equation replaced by the exact MOND elliptic constraint) **passes all
twelve algebraic gates on the generic branch** and is therefore promoted from the
previous ad-hoc "CONDITIONALLY CLOSED" note to a *checked* conditionally-closed
construction. It is **not** promoted to CLOSED.

The distinction is important and is the honest reading of the algebra.

---

## Why CONDITIONALLY_CLOSED and not CLOSED

Every one of the twelve gates PASSES on the **generic branch**
(defined below), and none of the eight automatic-rejection criteria of Gate 12 is
triggered. The two-DOF claim is therefore *earned*, not assumed:

- the Dirac count gives 20 − 12 − 4 = 4 phase-space dimensions = **2 DOF** (Gate 7);
- the rank condition (det Δ = (L_N K)² ≠ 0) is explicitly verified (Gates 3, 6);
- the preservation equations determine the four multipliers and generate **no**
  tertiary constraint (Gate 8).

The prompt forbids using the phrase "two DOF" unless all three of those have been
checked. They have. So the two-DOF statement is legitimate **on the generic branch**.

The reason the status is CONDITIONALLY_CLOSED rather than CLOSED is that closure
holds only on a restricted domain, and several items are *conditions* rather than
*theorems*:

1. **Domain restriction (the core condition).** The full-rank and two-DOF results
   hold only on the **generic branch**:

   - y = (c²/a₀)|D ln N| > 0  (nonzero lapse gradient — the MOND regime), and
   - k ≠ 0  (nonzero spatial mode).

   Two degeneracies are *excluded*, not resolved (Gate 6):
   - the **zero mode k = 0**: K = C_q k⁴ = 0, so det Δ = 0; the homogeneous
     (k = 0) modes of q and p survive S₂, S₃ and are reserved for a
     cosmological-background sector that is **not yet prescribed** (Gate 7);
   - the **zero-gradient branch y = 0**: both principal eigenvalues
     λ⊥ = μ(y) and λ∥ = μ(y) + y μ′(y) vanish, so L_N degenerates. This is the
     exact Newtonian (deep-GR) limit and needs separate treatment.

   A "global closure" claim would be an overclaim (Gate 12, criterion 8). The
   candidate does not make it.

2. **Not manifestly 4D generally covariant (Gate 11).** The lapse is removed by a
   **second-class** constraint pair (π_N, C_M), not a first-class refoliation
   multiplier. The theory has a **preferred foliation**. It is a Hamiltonian MMG
   theory with a local first-kind (phase-space) Lagrangian on a fixed foliation,
   *not* a manifestly 4D generally covariant local action. It must not be
   advertised as 4D covariant.

3. **Relativistic matter sector carries a defect (Gate 10).** Spatial
   diffeomorphism covariance of H_m and the Newtonian-limit matter equations are
   standard and consistent. But because the lapse equation is the MOND constraint
   (not the Hamiltonian constraint), the full 4D identity ∇_μ T^{μν} = 0 does **not**
   hold as a Bianchi-closure identity; the relativistic (v ~ c) matter EOM acquire a
   MOND-induced correction. This is a noted phenomenological defect, not a
   contradiction in the Newtonian regime.

4. **No-go boundary.** The construction is a *conditional* closure. It becomes
   fully CLOSED only after (a) a controlled zero-mode / cosmological prescription
   for the surviving k = 0 sector, (b) a separate treatment of the y = 0
   degenerate branch, and (c) a decision on whether the preferred-foliation /
   relativistic-matter defects are acceptable or must be repaired.

---

## Gate-by-gate result

| Gate | Subject | Result |
|------|---------|--------|
| 1 | Constitutive primitive G′(y)/(2y) = 1 − e⁻ʸ | PASS |
| 2 | Newtonian limit → MOND modified Poisson (c² cancels) | PASS |
| 3 | Dirac matrix structure; Pf = L_N K, det = (L_N K)² | PASS |
| 4 | Ellipticity: λ⊥, λ∥ > 0 for all y > 0 | PASS |
| 5 | Laplacian pair: {S₂(k),S₃(−k)} = ½ k⁴ ≠ 0 | PASS |
| 6 | Full rank on generic branch; k=0, y=0 excluded | PASS |
| 7 | DOF count: 20 − 12 − 4 = 4 = 2 DOF (TT pair) | PASS |
| 8 | Preservation determines multipliers; no tertiary | PASS |
| 9 | TT sector = GR; c_T = c, Q_T > 0, no scalar pole | PASS |
| 10 | Matter: spatially covariant, Newtonian-consistent | PASS |
| 11 | Hamiltonian MMG (not 4D covariant); first-kind L exists | PASS |
| 12 | Falsification: no auto-rejection triggered | PASS |

---

## What is now a theorem (on the generic branch)

- The exact MOND constitutive law μ(y) = 1 − e⁻ʸ from the local primitive
  G(y) = y² + 2(1+y)e⁻ʸ − 2.
- The exact Newtonian-limit reduction to the MOND modified Poisson equation with
  no missing sign or factor.
- The four-constraint Dirac matrix has Pfaffian L_N K and determinant (L_N K)²,
  independent of the off-diagonal couplings {C_M, D²q}, {C_M, D²p}.
- The lapse operator L_N is generically elliptic for y > 0.
- The inhomogeneous scalar pair (q, p) is removed by second-class constraints for
  k ≠ 0; the TT tensor pair is untouched.
- The physical gravitational sector has **two local propagating tensor degrees of
  freedom** with c_T = c and positive kinetic term, on the generic branch.
- The four multipliers are fixed by constraint preservation; no hidden tertiary
  constraint arises.

## What is NOT yet a theorem

- Global (all-k, all-y) closure — the k = 0 and y = 0 branches are excluded.
- A controlled cosmological zero-mode prescription.
- Manifest 4D general covariance (the theory is a preferred-foliation Hamiltonian
  MMG model).
- A closed relativistic matter sector with ∇_μ T^{μν} = 0 as an identity.

## Reproducibility

Run the full attack with:

    bash openai_push/final_closure/run_all.sh

Exit code 0 with "ALL GATES PASS" confirms the twelve gates. Each gate script is in
`openai_push/final_closure/scripts/`.
