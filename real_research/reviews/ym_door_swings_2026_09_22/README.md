# Yang–Mills door swings (2026-09-22)

Every open YM door in `real_research/reviews/OPUS49_DOOR_REOPEN_DIRECTIVES_2026-09-22.md`
was swung. **The Clay problem is not solved here, and no prize-level claim
is made.**

| door | what it needed | result | where |
|---|---|---|---|
| **D-YM1**: explicit X_d for the I15 Kogut–Susskind gap | Yarotsky's paywalled 2004 constants, **or** a cluster expansion with tracked constants | **Closed by the second route.** X_3 = 185.3 for all N ≥ 2, b_N ≤ 2N; X_3 = 131.1 for SU(2) and 98.3 for SU(3) at b = 2. Gap ≥ 3x/16, uniform in volume. Fixed spacing and strong coupling only. | `ym1_hamiltonian/` |
| D-YM1, Euclidean companion | none | A one-page Dobrushin proof for Wilson SU(N): m ≥ −ln(6(D−1) tanh β), with β_W < 0.0556 in D = 4 for all N. Threshold and rate both explicit. It also refines door E lane (b): SZZ 2023 already has an explicit threshold, though not an explicit rate. | `ym1_euclidean/` |
| **D-YM2**: scaling window and continuum limit (the Clay wall) | a new analytic control across the weak→strong crossover | **Not unlocked (swung twice: 09-22 and 09-25).** Swing 2 closes stochastic quantisation (d = 4 is exactly critical), and strong-coupling continuation (roughening at β = 5.8–5.9 lies inside the window; the bulk route reduces to the problem itself). It localises the missing estimate to O(1) block-spin steps. The one claimed 2025 proof (arXiv:2506.00284) was withdrawn by arXiv. Swing 3 took the RG-bridge route (Tomboulis's decimation comparison). It reproduces the Ito–Seiler obstruction: fixed-r decimation cannot tell SU(2) from U(1). A vanishing margin r_n = 1 − a/n (0 < a ≤ 1) does separate them in the hierarchical model, but the needed comparison inequality with a vanishing margin is unproved. Even proved, it would give lattice confinement, not the continuum gap. Swing 4 took the vanishing-margin door. The margin is used only per step in Tomboulis's Appendix B, so a/n costs nothing at a finite number of steps. SU(2)'s drift is a constant −0.250 per step. All 24 schedules keep U(1) deconfined above β = 0.75 (true transition 1.011). What is left is Ito–Seiler's Problems 1–3 (the interpolation-parameter existence and global-extension steps), untouched. The wall is quantified: the rigorous windows end at g² ≈ 32; the scaling window sits at g² ≈ 0.87–1.05; the continuum is g² → 0. Strong-coupling bounds have the wrong shape for the continuum. On its own terms, the framework has no gauge sector: its coupling to Yang–Mills is ~(m_G/M_Pl)² ≈ 2×10⁻³⁸ and its scales lie ~10⁴² below the glueball mass. | `ym2_continuum/` |
| D-YM3: I14 Hardy route to κ = 1/2 | a different action | **Closed for all single-scalar f(K) actions.** The 1/4 is the Laplacian's Hardy constant ((n−2)/2)², and V → 0 in every deep-MOND corner. Not on the prize path. | `ym3_hardy/` |
| D-YM4: I13/MESA pulsational ceiling | accreting supermassive-star structure runs | **Not swung.** No stellar-evolution code is installed here, and the door needs real MESA/GENEC accretion runs. Not on the prize path. | — |

Each folder has a runnable script (exit 0, `ALL CHECKS PASSED`) and its
`results.json`. The two new proofs were independently reviewed before this
commit, and every flagged gap was fixed; see `ym1_hamiltonian/REVIEW.md`.

**2026-09-23 note:** the sharper D-YM1 thresholds are those of the independent L326 lane
(`real_research/ym1_bdl_extension_2026/`: X₂ ≈ 42.3, X₃ ≈ 59.9, X₄ ≈ 73.3, BDL route). The
`ym1_hamiltonian/` result here (131/185/227) is a second, independent method reaching the same
statement.

**2026-09-25 Lean certificates.** Each file compiles with `lake env lean` from
`fable_independent_2026/lean_2026/` (Lean 4.34.0-rc2, Mathlib v4.34.0-rc2). All exit 0 with zero
`sorry`, and every theorem's axioms are exactly {propext, Classical.choice, Quot.sound}. The analytic
lemmas stay in prose in the PROOF/REPORT files. Lean certifies only the scalar chain that turns them
into the stated numbers.

| certificate | door | theorems |
|---|---|---|
| `I21_ym1_polymer_threshold.lean` (+ `.out`) | D-YM1 Hamiltonian | 13: tree criticality, KP a₂ identity, boundary sum κ_B ≤ 0.95K*, marked-path ratio 3/4, e^{−a₁} lower bound, N-uniform ε, X₂/X₃/X₄ = 131.1/185.3/227, gap ≥ 3x/16 |
| `I22_ym1_dobrushin.lean` (+ `.out`) | D-YM1 Euclidean | 8: TV two-point lemma (perfect-square certificate), tanh–exp bound, α < 1 windows for D = 4/3/2, −ln α > 0, SZZ conversion β_W = N²β |
| `I23_ym3_hardy_class.lean` (+ `.out`) | D-YM3 | 7: Newtonian s = (n−2)/2, deep-MOND s = 0, μ = A + B/u ⇒ s = ½, s = ½ ⇒ a_r′ = 0, a_r′ ≡ 0 on (0,∞) ⇒ H affine (μ = A + B/u only), and that class has no deep-MOND corner |

Filename prefixes I21–I23 are shared with earlier, unrelated certificates
(`I21_ym1_combinatorics`, `I22_virial_floor`, `I23_rar_inversion_below_baryons`). The names are kept
because `deepseek_push/I21_VERDICT.md` (independent compile audit, PASS for I21/I22) already cites them.
