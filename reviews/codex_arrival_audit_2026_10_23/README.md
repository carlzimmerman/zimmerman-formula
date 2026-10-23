# Codex arrival audit, 2026-10-23 — RESULT

Criteria: `FROZEN_CRITERIA.md` (committed `3bdfc60fa0` before any script; amendments A1 `26e31555f0` pre-result,
A2 `5ef2b58b82` and A3 `fa5cb92e1b` each committed before the check it adds). κ = ½ FITTED. No data are used; a₀ does
not enter any check (W′(0) = 0 at every background used), so both footings give the same numbers. No dark-matter
particle. Nothing in `sol61_push/` or `deepseek_push/` was edited. Not theory closed.

## Verdicts

1. **Codex R1 REPRODUCED** (`420fde16a5`, `sol61_push/mechanism_reassessment_2026_10_22/RESULT.md` §R1). A54/A68's
   "26 dimensions, 8 first-class, 0 second-class ⇒ 5 DOF" for the DSF-21 / A33 action is false. My own lattice code
   (written from A54 §1.3; Codex's `checks.py` not read) puts Codex's witness exactly on all eight constraints
   (residual 2.2e-16) and gives `{H[sin x], H[cos x]} = −(J/η) n sin(2π/n)` to 2e-10–8e-10 at n = 32/64/128, at β = 0.02
   and β = 0, → −2πJ/η. Deleting the clock term `√h P^i∂_iN` makes it ≤ 5e-9 (A2).
2. **A second, independent obstruction CONFIRMED (mine).** With P = π_P = 0, flat metric, non-uniform foliation
   expansion and dust, the bracket is `(2β/(2+3β)) ∫ ∂π (N∂M − M∂N)` (rel 6e-4 at n = 128, converging), and exactly the
   lattice form; it vanishes at β = 0. This is the non-projectable Hořava λ ≠ 1 non-closure (λ = 1 + β). A54 §2.2 had
   seen this term ("not proportional to any constraint") and asserted it is "absorbed by the shift sector"; it is not.
   DSF-21 cannot set β = 0: A78 needs 0 < β < 0.028.
3. **Preservation of H_⊥ is `(1/N)∂_j(N²V^j)`** with V^j = (2β/(2+3β))∂^jπ + π_P^j/η + O(P) (A4, rel 4e-3 at n = 128,
   converging). With the identity ∫π∂(N²∂π) = −∫N²|∂π|² (A5, exact in 1D and 3D): **at β > 0, data with static P
   (P = π_P = 0) and non-uniform expansion are not admissible** for any lapse N > 0. Data with longitudinal P momentum
   can be (AMENDMENT A1 narrowed this from HKLG's "the lapse must vanish", before any number).
4. **Linear count on Minkowski stays 5, but with a different classification (A6, sympy, exact).** Preservation of
   H_⊥^(1) gives a tertiary `χ = (2β/(2+3β))π″ + (π_P^x)′/η` (mod ∂H_x); `{χ, H_⊥} = −(β/(Kη(2+3β))) k²Z` and
   `{π_N, ψ} = +(β/(Kη(2+3β))) k²Z`, with Z = K(2+3β)/β + ηk² — A68's own scalar kinetic coefficient; the bracket matrix
   has rank 4; only π_s, H_x are first class; scalar sector (10 − 4 − 4)/2 = 1. So π_N, H_⊥, χ, ψ are second class and
   **the lapse is determined by a fourth-order equation, not a gauge choice.** C5's and A68's linear mode counts stand.
5. **The count is background-dependent: a Hořava-type half mode when P moves (A7, sympy, exact reduced scalar
   sector).** On Codex's witness (π_P = J x̂, expanding) `{π_N, χ} = 2iJk/η ≠ 0`, so the chain stops at χ; the
   {π_N, H_⊥, χ} block has determinant **8iJ³k³/η³**: complex rank 3 for every J ≠ 0 tested (1, 0.1, 0.001), 2 at J = 0.
   That is **3/2 scalar DOF per mode with k·π_P ≠ 0, against 1 on π_P = 0 backgrounds** (5.5 vs 5 in total). The extra
   half mode's symplectic weight vanishes as J³ → 0, so **static-P backgrounds — Minkowski, static galaxies — are
   strongly coupled** in this sector. MUTATE (clock deleted): rank 2 at every J, 1 DOF — the half mode is the clock
   term's.
6. **The standard cure works, at a price (A8, design test outside DSF-21).** Adding Blanchet–Pujolàs–Sibiryakov's
   α a_ia^i makes `{π_N, C_N} = 2αk²`, rank 2 on every background: a uniform 2 scalar DOF per mode, i.e. **6 DOF in
   total**. Its health is not tested here.
7. **Codex compatible-gas numbers REPRODUCED** (`a64cd8be27`). Cooling scale byte-identical (ncrit(200 K) 758.35 /cm³,
   min t_cool/t_ff 0.9017 at f_H2 = 1e-3 and 9.017 at 1e-4, Jeans 3276.4 M☉); RESULT.md's resolution table matches the
   committed `analysis_v2/result.json` to the printed digits; reruns of `crossing_base` (n128, 52 s) and `ultra`
   (n512, 393 s) from hashed copies are **byte-identical** (2382 and 5838 numeric leaves), peak RSS 0.05 GB. The fixed
   gas-mass radius is 0.127 / 0.107 / 0.127 field cells, peak cold contrast ×3.985 / ×4.318 and first-cell cold mass
   ×0.498 / ×0.540 per doubling — an unresolved ∝ r⁻² cusp, while the 0.32 kpc aperture mass moves 0.185 %. The
   physics reading (no resolved bound core in this spherical realisation; a converged aperture is not a core) is
   Codex's, and the numbers support it.

## Checks

| script | result | MUTATE |
|---|---|---|
| `r1_bracket_check.py` (R0, A1–A6) | **20/20 PASS** (`r1_bracket_check.out`, `r1_results.json`) | clock deleted: 7 FAIL (A1 ×6, A6), exit 1 |
| `r1_rank_moving_P.py` (A7) | rank 3 at J ≠ 0, 2 at J = 0; det 8iJ³k³/η³ (`r1_rank_moving_P.out`) | clock deleted: rank 2 everywhere |
| `r1_rank_moving_P.py --bps` (A8) | rank 2 everywhere; det 4α²k⁴ (`r1_rank_moving_P_BPS.out`) | — |
| `cg_repro.py` (B1–B3) | **8/8 PASS** (`cg_repro.out`, `cg_repro_results.json`) | 3 FAIL (B1, B2, B3), exit 1 |

Execution note: the first B3 attempt failed before computing anything — `/usr/local/bin/timeout` is x86_64, so the
universal `/usr/bin/python3` ran under Rosetta and could not load the arm64 NumPy; kept in `cg_rerun/failed_run1/`;
fixed with `arch -arm64`. One thread, `nice -n 15`, while the 384³ L1 job ran.

## What this changes in the record

- `STANDING.md` Revision 12 block, item 1 ("the 5-DOF spine, machine-checked … 8 first-class constraints, 0
  second-class ⇒ 5 healthy DOF") and `deepseek_push/DS_FINAL_2026_10_21/README.md` (Q3 row; A54 "RESOLVED — 5 healthy
  modes"): the eight constraints are not first class; the 5 is a linear count on π_P = 0 backgrounds only; on moving-P
  backgrounds the count is 5.5 and the static-P backgrounds are strongly coupled. A fix-forward note is added at the
  top of `STANDING.md`; DS_FINAL files are not edited. The 87 Lean theorems check algebraic identities of the stated
  definitions; none of them is the constraint algebra (A68's C4 tests ∂H_⊥/∂N = 0, which says nothing about
  {H_⊥, H_⊥} — Codex's point, confirmed).
- `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1 ("DSF-21's A33 is this theory with η > 0, which C5 shows is
  ill-posed; v3 drops η"): independent support from the Hamiltonian side — η > 0 with the clock term gives the
  half mode (verdict 5). Note sent to the coordinator; the draft is theirs to edit.
- **Design rule for any future P kinetic term:** it needs a lapse term of the a_ia^i type, and then the theory has a
  sixth mode whose health must be shown (verdict 6).

## What this does not do

- **v3 is not tested.** v3 has β = 0 and η = 0 (P auxiliary, no π_P), so neither obstruction above applies as
  written; its own Dirac analysis (π_P ≈ 0 primary, the P equation as a secondary that contains N) is a different
  calculation and stays OPEN, as C4/C5 already say.
- Only the scalar sector with k ∥ π_P was ranked; k ⊥ π_P (where {π_N, χ} ∝ J·k = 0) and the vector/tensor sectors on
  the moving background were not. The nonlinear statement in verdict 3 is for P = π_P = 0 data.
- Of Codex's 553-file mechanism review only R1 was audited (R2's response-time table, R3 and the quantum-state results
  were read, not checked). Codex's gas solver physics (cooling fits, viscosity) is reproduced, not re-derived.
- Literature (looked up with search, summary only, provisional): Henneaux, Kleinschmidt & Lucena Gómez,
  arXiv:0912.0399 (PRD 81, 064002) — non-projectable Hořava's Hamiltonian constraints are generically second class and
  the lapse is forced to vanish; Blas, Pujolàs & Sibiryakov, arXiv:0906.3046 — the extra mode and its strong coupling;
  the same authors' a_ia^i extension, arXiv:0909.3525 (PRL 104, 181302), is the cure tested in A8.
