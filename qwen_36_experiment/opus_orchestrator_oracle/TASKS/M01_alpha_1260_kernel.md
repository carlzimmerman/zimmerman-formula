# M01 — The α ≥ 1.260 kernel the joint DEMANDS
COST: S | KILLS FAST: no | script: `mi_alpha1260_kernel_2026.py`

## The task
The joint over-determination (`mi_joint_overdetermination_2026.py`, 42/42) found the ephemeris **demands
α ≥ 1.260** and that the cost elsewhere is negligible: SPARC pays 0.0014 dex, clusters 0.0055 dex, wide
binaries 1.78 σ_sys. That makes the kernel tail the **first parameter this framework has fixed by data it
was not fitted to.** But nobody has written down the α = 1.260 kernel and priced it properly.

## Do
1. Write the α-family kernel explicitly (α is the exponent in the interpolation tail; get its definition
   from `mi_route_a_kernel.py` and the corpus's α = 1 / 2 / ∞ comparisons — do not invent it).
2. At α = 1.260 exactly: compute the RAR residual on SPARC, the cluster η(R500), the wide-binary γ_v, and
   the solar-system residual at Earth and Mars. Both a₀ footings.
3. Compare each against the α = 1 and α = 2 values the corpus already has. Report the full ledger.
4. Then the sharp question: is α = 1.260 a *boundary* (the ephemeris just barely allows it) or an
   *interior* point? If boundary, the tail is fixed to one value and that is a derived parameter — say so.

## Settles if / refuted if
SETTLED: a full five-front ledger for α = 1.260 with every number and both footings.
REFUTED: α = 1.260 fails a front the joint said it passes ⇒ re-check the joint's cost estimates.

## Known walls
α = 1 IS `g_obs² = g_bar² + a₀g_bar` and IS Milgrom 1999 eq 9, and it is excluded at **378σ** post-EFE.
The word "exact" is dead for that law. SPARC cannot distinguish α = 1 from α = 2 (0.0084 dex across
α = 1, 2, ∞), so SPARC will not decide this — the solar system already did.
