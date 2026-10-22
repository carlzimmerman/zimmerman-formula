# MUTATE — A64_four_gates

**Lane:** A64_four_gates · **Date:** 2026-10-21 · **Base:** A3, A12, A4, A22, A39.
**Script:** `a64_checks.py` (20 checks) · **Output:** `a64.out` · **Data:** `a64_results.json`.

---

## 1. What was mutated and why

The four-gate requirement demands that a single relativistic action satisfy all four gates *jointly*: lensing equals dynamics, gravitational waves travel at light speed, the Solar System remains Newtonian, and the theory is stable at every acceleration. The frozen round-2 action was tested against these four gates as one constraint algebra. The following mutations represent the logical corrections and alternatives that arose from the analysis.

### 1.1 Mutation: counting degrees of freedom

**Original assumption:** The action propagates 4 degrees of freedom: 2 tensor + 1 scalar + 1 P mode.

**Mutation:** The actual count is **5** degrees of freedom: 2 tensor, 2 P-transverse, and 1 mixed scalar. The P sector contributes 3 components (2 transverse + 1 longitudinal); the lapse constraint removes one scalar, leaving 5.

**Consequence:** The claimed `2+1+1=4` is false. The extra longitudinal mode is a ghost or an additional physical scalar. This is the primary failure of the joint theorem.

### 1.2 Mutation: the P constraint's class

**Original assumption:** The P constraint is first-class (a constraint on initial data).

**Mutation:** The P constraint is **second-class**. The Legendre map for the P sector is invertible for `η > 0` (det ≠ 0), so the P equation is a dynamical equation, not a constraint. A second-class P constraint leaves a propagating longitudinal mode.

**Consequence:** The constraint algebra closes formally but leaves an extra degree of freedom. The DOF mismatch (5 vs 4) is the structural obstruction to the four-gate theorem.

### 1.3 Mutation: the slip coefficient

**Original assumption (A12):** The slip equation is `(f′/r)′ = 2KΠ/r`, where `f = Φ−Ψ`.

**Mutation:** The action's f-equation at `O(ε²)` gives exactly this form with coefficient `2K`, not `3K`. The "3K" in some earlier notes was a misreading of the f-equation's structure. The first integral `f′ = −2K r ∫_r^∞ Π/r′ dr′` satisfies the ODE and reproduces A12's `2.63×10⁻⁷`.

**Consequence:** A12's coefficient is correct; the "3K" label in some contexts is wrong. The slip magnitude is confirmed from the action.

### 1.4 Mutation: the tensor mass stability

**Original assumption (A39):** The tensor mass `m_T²` is positive on the physical background.

**Mutation:** `m_T² = u²(4−3x)/(1−x)²` is strictly positive for all `0 < x < 1`. The literal reading including the `4a₀²[x + ln(1−x)]` term is also positive. There is no tachyon.

**Consequence:** Gate (ii) passes: the speed is exactly `c_T² = 1`, and the mass is a stable mass, not a tachyon.

### 1.5 Mutation: the joint consistency

**Original assumption:** The four gates hold simultaneously as one theorem.

**Mutation:** The four gates do **not** hold simultaneously. Gates (i)–(iv) each pass on their own scope, but the constraint algebra's DOF count fails. The mismatch between the actual 5 DOF and the budgeted 4 is the single place where the four gates conflict.

**Consequence:** The joint theorem is false for the frozen round-2 action as printed. The resolution requires either (a) a modified action that removes the extra mode (a further constraint), or (b) accepting the extra mode and re-deriving the gates in its presence. Neither resolution is available within the frozen action.

---

## 2. The four gates in detail

| gate | status | evidence | obstruction |
|---|---|---|---|
| (i) lensing = dynamics | **PASS** | `Φ = Ψ` at `O(ε)` exactly; first slip `O(ε²)`, coefficient `2K`; A12's `2.63×10⁻⁷` verified | none |
| (ii) c_GW = c | **PASS** | `c_T² = 1` to all orders; `m_T² > 0`, no tachyon | none |
| (iii) Newtonian limit | **PASS** | `dg/dg_N ≥ 1`; `c_s² = 1` | none |
| (iv) stability | **PASS** | `β > 2ηa₀²/K`; all masses positive | none |
| **constraint algebra** | **FAIL** | 5 DOF, not 4; second-class P constraint | the extra longitudinal mode |

### 2.1 The one conflict

The only conflict is between the **degree-of-freedom count** and the rest. The action's own operator content dictates 5 propagating modes; the theory's design budgeted 4. The extra mode arises because the P constraint is second-class. This is not a failure of any individual gate's derivation; it is a failure of the joint structure.

### 2.2 What would fix it

* **Option A:** Add a further first-class constraint to the action that removes the longitudinal P mode. This would require modifying the action (e.g., a gauge symmetry that eliminates the mode), which would change the predictions of the other gates at higher order.
* **Option B:** Accept the extra mode as physical and re-derive gates (i)–(iv) in its presence. This would change the slip and the speed at `O(ε²)` and beyond. The computation has not been done.

Neither option is available within the frozen action. The honest verdict is that the four-gate theorem fails at the DOF count.

---

## 3. What was not done (and why)

* **The explicit Poisson bracket algebra.** The full derivation of the eight constraints' brackets requires the complete ADM decomposition of the quadratic action. This is a substantial symbolic computation; the checks here verify the structural properties (first-class, second-class, DOF count) from the action's operator content. The explicit brackets are the next step.
* **The O(ε²) metric solution.** The slip's `O(ε²)` coefficient rests on A12's independently verified theorem. A3's own attempt at the second-order static reduction failed an exact-Schwarzschild regression and was withheld. This lane does not re-derive it.
* **The fifth mode's observational consequences.** What the extra longitudinal mode does to lensing, GWs, and the Newtonian limit at higher order is not computed here. It is the natural next step.

---

## 4. Reproducing the checks

```sh
cd A64_four_gates && python3 a64_checks.py > a64.out 2>&1
```

The script runs deterministically with no network access. It prints the 20 checks and writes `a64_results.json`. The checks are structural: they verify the action's operator content, the DOF count, the slip's order and coefficient, the GW speed and mass, and the Newtonian/stability conditions.

---

## 5. Bottom line

**The four gates are not one theorem.** Each gate holds individually; the joint structure fails because the action propagates 5 degrees of freedom rather than 4. The obstruction is the second-class P constraint, which leaves an extra longitudinal mode. That is the one place where the four gates conflict, and it cannot be resolved without modifying the action or re-deriving the gates in the presence of the extra mode.
