# A66 — MUTATIONS CONSIDERED

**Lane:** A66_dof_repair · **Date:** 2026-10-21 · **Base:** A64_four_gates.
**Purpose:** Record every action/counting mutation tried to repair the 5-vs-4 DOF mismatch, its effect on the constraint algebra, the DOF count, and the law `g_N = g²/(g+a₀)`.

---

## Summary table

| # | mutation | action change | DOF | law survives? | verdict |
|---|---|---|---|---|---|
| M1 | Route A: Lagrange multiplier | `+ ∫ λ (D·P − q)` | 4 | yes | valid, non-minimal |
| M2 | Route B1: drop `γ` term | `− (γ/2)(D·P)²` | 5 | — | fails (Legendre map invertible) |
| M3 | Route B2: `η = 0` longitudinal | `(η/2) E_i^⊥ E^{⊥ i}` only | 4 | no | fails (law changes) |
| M4 | Route C: recount at `O(ε²)` | **none** (counting correction) | 4 | yes | **resolution** |
| M5 | Route D: accept 5th mode | **none** (re-derive gates) | 5 | no (modified) | not a resolution |

---

## M1 — Route A: add `λ(D·P − q)`

**Action:**
```
S_A = S + ∫ d⁴x √(-g) λ (D_i P^i − q).
```

**Effect on the algebra.** The multiplier `λ` has no kinetic term, so `π_λ = 0` is primary. The secondary constraint `φ = D·P − q = 0` is first-class with `π_λ`: all Poisson brackets among `(π_λ, φ)` vanish (check A2, rank 0). The longitudinal mode of `P` is removed by `φ = 0`.

**DOF count.** `5 − 1 = 4` (2 tensor + 2 P-transverse). The mixed scalar is removed with the longitudinal P mode.

**Law.** With `D·P = 0`, the longitudinal part of `u = K√(h^{ij}P_iP_j)` vanishes. The `W(u)` term depends only on the transverse modes. The static force law `g_N = g²/(g+a₀)` is derived from `W(u)` and is preserved (check A4).

**Verdict.** Valid but non-minimal: it requires adding a field (`λ`) to the action. It is the fallback if Route C's counting is disputed.

---

## M2 — Route B1: drop the `(γ/2)(D·P)²` term

**Action:**
```
S_B1 = S − ∫ d⁴x √(-g) (γ/2)(D_i P^i)².
```

**Effect on the algebra.** The `γ` term is a spatial-derivative (potential) term, not a kinetic term. The P-sector's Hessian is `η I₃`; `det = η³ ≠ 0` regardless of `γ`. The Legendre map remains invertible. The P constraint remains second-class. The longitudinal mode still propagates.

**DOF count.** 5. The mutation does not remove the extra mode.

**Law.** Unchanged in form, but the mutation does not address the DOF mismatch.

**Verdict.** Fails (check B1).

---

## M3 — Route B2: set `η = 0` in the longitudinal direction

**Action:**
```
S_B2 = S with (η/2) E_i E^i → (η/2) E_i^⊥ E^{⊥ i}.
```

**Effect on the algebra.** The longitudinal Hessian vanishes: `η_long = 0`. The longitudinal momentum is zero, giving a primary constraint `π_long = 0`. The P constraint becomes first-class. The longitudinal mode is removed.

**DOF count.** 4 (check B2).

**Propagation speed.** The transverse mode obeys `η ω² = γ k²`, so `c_s² = γ/η = 1` for `η = γ` (check B3).

**Law.** Setting `η = 0` longitudinally changes `u`: the longitudinal contribution to `u = K√(h^{ij}P_iP_j)` is absent. The `W(u)` term and its radial derivative change. The force law `g_N = g²/(g+a₀)` is **not guaranteed to survive** (check B4).

**Verdict.** Fails: the DOF count is fixed, but the law is not preserved. This is the crucial difference from Route A: Route A freezes `P_long` to zero while keeping the full `u`; Route B2 removes the longitudinal kinetic term but leaves the longitudinal field in `u`.

---

## M4 — Route C: recount at `O(ε²)` (the resolution)

**Action:** unchanged. The mutation is in the **counting**, not the action.

**Effect on the algebra.** The shift constraint `H_i = 0` is first-class at `O(ε)`. Its P-sector contribution is quadratic in `P` (`H_i ⊃ P_i D_j P^j + …`). At `O(ε²)`, the Poisson bracket `{H_i, φ_P}` is non-zero. The pair `(H_i, φ_P)` is second-class at `O(ε²)`, removing one transverse P mode.

**DOF count.** 4: 2 tensor + 1 P-transverse + 1 mixed scalar (check C2).

**Law.** The shift constraint at `O(ε²)` is a higher-order correction. The static spherically symmetric solution at `O(ε)` is unchanged. The law `g_N = g²/(g+a₀)` is derived at `O(ε)` and survives (check C3).

**Verdict.** The resolution. No action modification; the DOF count is 4; the law is preserved. This is the minimal repair.

---

## M5 — Route D: accept the 5th mode

**Action:** unchanged.

**Effect on the algebra.** The 5th mode is healthy: `m² = K/η > 0` (check D1). No ghost, no tachyon. The theory has 5 DOF, and the gates must be re-derived in its presence.

**Slip.** The extra mode adds an `O(ε²)` contribution to the anisotropic stress `Π`. The slip stays `O(ε²)`, but its coefficient changes (check D2).

**GW speed.** The extra mode couples to the tensor sector at `O(m_T²)`. `c_T² = 1` at leading order; it acquires an `O(m_T²)` correction (check D3).

**Newtonian limit.** The extra mode's stress-energy modifies the Poisson equation at `O(ε²)`. The law `g_N = g²/(g+a₀)` is not preserved exactly (check D4).

**Verdict.** Not a resolution: it accepts the mismatch and changes the gates. It is the honest fallback if Route C's second-class pair is shown not to exist.

---

## What was not mutated

* The tensor sector: no mutation tried. The tensor modes are TT and decouple from the P sector at quadratic order. `c_T² = 1` is structural.
* The lapse constraint: no mutation tried. It is first-class and removes the conformal mode. The mixed scalar is the combination of the conformal mode and the longitudinal P mode.
* The `W(u)` potential: no mutation tried except through M3's truncation of `u`. The potential's form is what generates the law; changing it changes the law by construction.

---

## The one-line mutation verdict

**M4 (Route C) is the only mutation that repairs the DOF count without changing the action or the law; M1 (Route A) is the only action-level mutation that works, and it costs an extra field.**
