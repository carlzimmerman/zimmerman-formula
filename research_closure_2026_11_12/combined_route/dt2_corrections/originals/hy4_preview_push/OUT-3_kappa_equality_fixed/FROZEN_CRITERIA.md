# OUT-3 (EQUALITY-FIXED) — FROZEN CRITERIA

2026-11-12. Lane chartered to test one candidate mechanism for making `kappa = 1/2` an
OUTPUT rather than a fit.

**Standing.** kappa = 1/2 FITTED; not theory closed. Footings are graded separately and
never pooled. Cold dark energy is a gravitating field component, never a particle. This
lane adopts nothing and registers nothing; it grades one candidate.

**Order disclosure.** These criteria were written in the same session as the SYMPY leg
(`out3.py`). The SYMPY leg ran first; this file records the gates the leg was built to
answer and adds the one gate the leg did not decide (G4). Nothing below was chosen after
seeing a number that it grades.

---

## 1. The candidate under test

The charter's candidate, stated as three claims:

- **(C1) The degeneracy.** The clock's rate `Q = £_n τ = τ̇/N` and the leafwise measure
  `dV_h = √h d³x` carry one exact redundancy: `τ → f(τ)` rescales `Q → f'(τ)·Q` and leaves
  the leaf and its measure untouched. The invariant is the 4-volume per tick,
  `𝒱 = dV₄/dτ = V_Σ/Q`.
- **(C2) The normalization (the new physics).** The vacuum fixes the clock's rest rate —
  hence, by the degeneracy, the leafwise measure — by
  `ρ_τ(Q_vac) = ρ_Λ`, with `ρ_τ = μ_K²(Q−1)/(4πG)` the clock sector's cold-charge density
  (`V3_FULL_PICTURE` §2). This is a normalization of `τ`, not a force, not a field, not a
  new constant. It is the *only* new input this lane admits.
- **(C3) The output.** From (C1)+(C2), `a₀ = c√(Gρ_Λ)/2` follows from the geometry of the
  settle-down, and `1/2` is the ratio of the halo's enclosed cold charge to the cosmic
  share.

## 2. The construction this lane actually builds

(C2) fixes the vacuum's cold-charge density to `ρ_Λ`. The halo is a *redistribution* of
that charge (the framework's own result: the halo carries no net charge, `R541_why_the_cold_share`
§2), so its outer boundary — the **settle-down radius** `r_sd` — is where the halo's own
cold density returns to the vacuum value:

    (SD)   ρ_c(r_sd) = ρ_Λ .

**The ratio to be computed:**

    K := M_c(r_sd) / M_Λ(r_sd),
    M_c(r) = r² g_c(r)/G        (enclosed cold charge, Gauss),
    M_Λ(r) = (4π/3) ρ_Λ r³      (cosmic share in the same sphere).

The halo profile is the framework's own static spherical limit of law S
(`g_N = g²/(g+a₀)`, `CLOSURE.md` 2026-11-05 §1; `V3_FULL_PICTURE` §2). No profile is chosen
by this lane.

## 3. Pre-registered gates

The lane's label is decided by G1–G4. All four are reported regardless of outcome.

| Gate | Statement | PASS condition |
|---|---|---|
| **G1** (exact ratio) | Derive `K` exactly, in closed form, as a function of `x := g(r_sd)/a₀`, from law S + (SD). No numerics, no asymptotics. | A closed form is derived and SYMPY-verified against the direct expression. |
| **G2** (the number) | Report `K` for a mass grid spanning ≥ 5 dex on both footings. | `K` printed for every row; both footings. |
| **G3** (is it 1/2?) | Does `K = 1/2`, either exactly or within the grid's spread? | `|K − 1/2|` below the grid's own mass-drift, on both footings. |
| **G4** (universality) | `kappa` is universal (FINAL-15, FINAL-16). Does `K` drift with `M_b`? | Drift in `K` across the grid < 1 %. |

**Label rule.**
- G3 PASS and G4 PASS → the candidate **outputs** kappa = 1/2. Label `KAPPA DERIVED`.
- G3 PASS, G4 FAIL → the candidate outputs 1/2 but a mass-dependent one; not universal.
  Label `DERIVED BUT NOT UNIVERSAL`.
- G3 FAIL → the candidate does **not** output 1/2. Label `KAPPA NOT DERIVED (candidate
  refuted)`, with the number printed and the factor by which it misses.

## 4. Auxiliary gate (not part of the label)

**G5 (the turnaround variant).** A plausible alternative reading of "the geometry of the
settle-down" is the radius where the halo's cold pull balances the vacuum's Λ push,
`g_c = (8πGρ_Λ/3) r`. Report `K` there, and report whether the value carries any
information about the law: if the same `K` follows from Gauss + the Λ force law alone, for
an *arbitrary* enclosed mass, it is a tautology and cannot fix `a₀`. This is reported, not
weighted into the label.

## 5. Certification

The load-bearing algebra goes to Lean (`OUT3_equality_fixed.lean`), zero `sorry`, axioms
⊆ {propext, Classical.choice, Quot.sound}, with a `_MUTATE` twin that must fail. Per the
certification rules, a theorem that will not close is **deleted** with the blocker named,
never `sorry`'d, and never weakened into a lesser claim without saying so.

Lean certifies the mathematics of the statements, not that any statement is a law of
nature. The physical premises (C1), (C2), (SD) are inputs and are labelled as such in the
file header.

## 6. What this lane does not do

- It does not reopen the amount (5.41), the cluster offset, or hosted dwarfs.
- It does not fit anything.
- It does not pool footings: every row is printed per footing.
