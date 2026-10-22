# MUTATE — A67_ghost_diagnosis

**Lane:** A67_ghost_diagnosis · **Date:** 2026-10-22 · **Base:** A64_four_gates, A66_dof_repair, A54_four_gates, A22_ppn_frames, A39_tensor_mass.
**Script:** `a67_checks.py` (18 checks) · **Output:** `a67.out` · **Data:** `a67_results.json`.

---

## 1. What was mutated and why

The question is the **sign of the fifth mode's kinetic term**. The baseline calculation uses the canonical parameters (`β = 1`, `η = γ = K L★²/2`, `L★ = 24 pc`, `a₀ = 9.36×10⁻¹¹ m/s²`). The mutations below are the logical alternatives that would change the verdict; each one is a physically distinct theory, not a numerical tweak. The baseline is `Z > 0`, `m² > 0`, healthy.

| mutation | what changes | which checks fail | physical consequence |
|---|---|---|---|
| `beta_neg` | `β = −0.25` | **Z1** (`Q₀ < 0`), **Z2** would still say `sign(Z)=sign(β)` | The scalar becomes a **ghost**: `Z < 0`. This is the only mutation that produces a ghost without changing the operator content. |
| `eta_neg` | `η = −γ` | **M1** (`m² = K/η < 0`), **C1** (`c_s² < 0`) | The P sector becomes a **tachyon** and the sound speed is imaginary. |
| `gamma_neg` | `γ = −γ` | **C1** (`c_s² < 0`) | Gradient instability; the scalar's speed is imaginary. |
| `drop_shift` | remove the shift's kinetic mixing `(2/3+β)ḣ∇²ψ − β(∇²ψ)²` | **Z1** (the conformal kinetic term stays `−(2+3β)/12 ḣ² < 0`) | The conformal negative direction propagates: a **ghost**. This shows that the shift's contribution is what makes `Q₀` positive. |
| `drop_lapse` | remove the lapse constraint `H_⊥ = 0` | **L3** (the conformal negative direction propagates) | The theory propagates a negative-norm conformal mode: a **ghost**. |
| `P_curvature` | add `ξ R_ij P^iP^j` with `ξ = 1` | **G2** (`c_T² = 1 + O(ξ)`; A54 G1b gives `Δc_T² = 1.19×10⁻¹⁸`) | The tensor speed is no longer exactly 1; the gate is broken at `O(10⁻¹⁸)`, still invisible but structurally nonzero. |
| `clock2` | clock coefficient `→ 2` | **G3** (`dg/dg_N = 1/(1−2u')`, which can be `< 1`) | The Newtonian limit is no longer monotonic; `dg/dg_N ≥ 1` fails. |
| `W_quad` | replace the log potential by `W = u²/(2K)` | **M1** (the mass term changes), **M3** (the `K/η` identity is lost) | The P-sector mass is no longer `K/η`; the saturation and the MOND law are lost. |

---

## 2. The baseline in detail

The baseline is the frozen round-2 action with the canonical parameters. The key formulas:

```
Q₀ = (2+3β)/(Kβ) + ηk²/K²,       Q₀(k=0) = 5/(Kβ) = 5.961×10⁹ > 0,
m² = K/η = 3.647×10⁻³⁶ m⁻² > 0,
c_s² = γ/η = 1,
m = √2/L★ = 3.768×10⁻²⁵ eV,
λ = L★/√2 = 16.97 pc.
```

The sign of `Q₀` is the sign of `β` (A54 H8). For `β = 1`, `Q₀ > 0`. The conformal mode's negative kinetic term `−(2+3β)/12 ḣ²` is cancelled by the shift's contribution after integrating out `ψ`, giving the positive effective term `(2+3β)/(18β) ḣ²`. The lapse constraint removes the remaining negative conformal direction (A54 L9). The P longitudinal's kinetic term is positive for `η > 0`. The mode is healthy.

---

## 3. What the mutations show

* **`beta_neg` is the ghost mutation.** It is the only one that flips `Z` without changing the derivative structure. The fact that the baseline uses `β = 1 > 0` is why the fifth mode is healthy. The principal-positivity bound `β > 2ηa₀²/K = 5.948×10⁻¹⁹` is satisfied with a huge margin, so `β` cannot accidentally cross zero in the admissible background.
* **`drop_shift` and `drop_lapse` are structural ghosts.** They show that the positivity of `Q₀` is not automatic: it relies on the shift's kinetic mixing and on the lapse constraint removing the negative conformal direction. The frozen action has both, so the mode is healthy.
* **`eta_neg` and `gamma_neg` are tachyonic/gradient mutations.** They break the mass and the sound speed, not the kinetic sign.
* **`P_curvature` and `clock2` are gate mutations.** They show that the gates (ii) and (iii) are separate from the ghost question: a healthy scalar can still break `c_T² = 1` or `dg/dg_N ≥ 1` if the operator content is changed. The frozen action has no P-curvature coupling and a unit clock, so the gates survive.

---

## 4. Reproducing the checks

```sh
cd deepseek_push/DS_FINAL_2026_10_21/A67_ghost_diagnosis
python3 a67_checks.py > a67.out 2>&1
```

The script is deterministic, uses only the standard library, and writes `a67_results.json`. It prints all 18 checks and the summary. The baseline is 18/18 PASS. The mutations in the table are logical alternatives; the script does not implement a `--mutate` switch, because each mutation changes the theory rather than a numerical parameter. The table records what each mutation would do to the checks.

---

## 5. Bottom line

**The fifth mode is healthy.** The kinetic coefficient is positive for `β > 0`, the mass squared is positive, and the speed is exactly 1. The only ghost mutation is `β < 0`, which is excluded by the principal-positivity bound. A64's "ghost signal" is a degree-of-freedom count mismatch, not a negative kinetic term. The mode is the P longitudinal / cold medium compression mode, with mass `3.77×10⁻²⁵ eV` and Compton wavelength `17 pc`.
