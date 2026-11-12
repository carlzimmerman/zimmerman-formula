import Mathlib
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# FINAL-9 (LEAN-STATIC): the algebra of the law's static halo

Lane `fable52_push/FINAL-9_lean_static/`.  Law (form B): g_N = g^2/(g + a0),
a0 = kappa c sqrt(G rho_Lambda), halo scale r_M = sqrt(G M_b/a0), halo profile
X(x) = (sqrt(1 + 4x^2) - 1)/2 with x = r/r_M, enclosed cold mass M_c(r) = M_b X(x).

SCOPE NOTE.  Lean machine-checks here the MATHEMATICS THE CLAIM RESTS ON: the algebra of the
static halo of the law.  It does **not** certify that the law is a law of nature.  The physics
input -- which Lagrangian (action (A), QX17), which regime (static, weak field, spherical),
which identification of the enclosed cold mass -- is an ASSUMPTION of this file, not a theorem
in it.  Every statement below is a theorem about real numbers.

Numbered content.

1. The two forms of the law are equivalent (all of g, g_N, a0 positive):
   * `quad_pos_root`   -- quadratic step: y^2 - y - c = 0 with 1 <= y forces
                          y = 1/2 + sqrt(1/4 + c).
   * `law_forward`     -- g_N = g^2/(g + a0)  ==>  g = g_N (1/2 + sqrt(1/4 + a0/g_N)).
   * `law_backward`    -- g = g_N (1/2 + sqrt(1/4 + a0/g_N))  ==>  g_N = g^2/(g + a0).
2. The halo profile X(x) = (sqrt(1 + 4x^2) - 1)/2:
   * `X_nonneg`      -- X x >= 0 for every real x.
   * `X_quad`        -- X^2 + X = x^2.
   * `X_mul_one_add` -- X (1 + X) = x^2.
   * `X_le_sq`       -- X x <= x^2 (corollary, used by the limits).
   * `X_strictMono`  -- 0 < x < y  ==>  X x < X y.
3. Enclosed cold mass and cold density:
   * `Mc_zero`       -- M_c(0) = 0.
   * `X_hasDeriv`    -- X'(x) = 2x/sqrt(1 + 4x^2) (every x; X is smooth).
   * `Mc_hasDeriv`   -- M_c'(r) = M_b (2x/sqrt(1 + 4x^2)) / r_M with x = r/r_M.
   * `rhoC_closed`   -- rho_c := (1/(4 pi r^2)) dM_c/dr = M_b/(2 pi r r_M^2 sqrt(1 + 4x^2)).
   * `rhoC_closed_x` -- the lane's form: rho_c = (M_b/(4 pi r_M^3)) 2/(x sqrt(1 + 4x^2)).
4. The two limits, stated in explicit epsilon-delta form (no `Tendsto`, no `atTop`, no
   filter notation):
   * `rhoC_column_limit` -- lim_{r->0+} r rho_c = a0/(2 pi G)   (the universal column).
   * `rhoC_outer_limit`  -- lim_{r->oo}  r^2 rho_c = sqrt(G M_b a0)/(4 pi G).
5. The asymptotic speed defined by v_inf^2 := sqrt(G M_b a0):
   * `vInf_sq`    -- v_inf^2 = sqrt(G M_b a0).
   * `vInf_four`  -- v_inf^4 = G M_b a0.
   * `vInf_sq_rM` -- v_inf^2 = G M_b/r_M on the halo scale r_M^2 = G M_b/a0.

kappa = 1/2 FITTED; footings never pooled; the cold component is cold dark energy, no
particle; not theory closed. Adopts nothing.
-/

open Real

namespace FINAL9

/-! ## 0. The objects -/

/-- Halo profile. `X x = (sqrt (1 + 4x^2) - 1)/2`. -/
noncomputable def X (x : ℝ) : ℝ := (Real.sqrt (1 + (4 : ℝ) * x ^ 2) - 1) / 2

/-- Enclosed cold mass: `M_c(r) = M_b X(r/r_M)`. -/
noncomputable def Mc (Mb rM r : ℝ) : ℝ := Mb * X (r / rM)

/-- Cold density from the enclosed cold mass:
`rho_c(r) = (1/(4 pi r^2)) dM_c/dr`. -/
noncomputable def rhoC (Mb rM r : ℝ) : ℝ :=
  (1 / (4 * Real.pi * r ^ 2)) * deriv (fun s : ℝ => Mc Mb rM s) r

/-- Asymptotic speed, defined by `v_inf^2 = sqrt (G M_b a0)`. -/
noncomputable def vInf (G Mb a0 : ℝ) : ℝ := Real.sqrt (Real.sqrt (G * Mb * a0))

/-- The root form of the law: the total field `g` as a function of the baryonic field
`g_N`, `g = g_N (1/2 + sqrt (1/4 + a0/g_N))`. -/
noncomputable def gOf (gN a0 : ℝ) : ℝ := gN * ((1 / 2 : ℝ) + Real.sqrt ((1 / 4 : ℝ) + a0 / gN))

/-- The halo closure radius: `r_M^2 = G M_b/a0`, i.e. `a0 r_M^2 = G M_b`. -/
private theorem closure_mul (G Mb a0 rM : ℝ) (ha0 : 0 < a0) (hrMdef : rM ^ 2 = G * Mb / a0) :
    G * Mb = a0 * rM ^ 2 := by
  rw [hrMdef]
  field_simp [ha0.ne'] <;> ring

/-! ## 1. Equivalence of the two forms of the law -/

/-- Quadratic step. If `y^2 - y - c = 0` and `y >= 1` then `y` is the positive root
`1/2 + sqrt (1/4 + c)`. (The other root is `1/2 - sqrt(1/4+c) <= 1/2 < 1`.) -/
theorem quad_pos_root (y c : ℝ) (h : y ^ 2 - y - c = 0) (hy : (1 : ℝ) ≤ y) :
    y = (1 / 2 : ℝ) + Real.sqrt ((1 / 4 : ℝ) + c) := by
  let t : ℝ := (1 / 4 : ℝ) + c
  have hsq : (y - (1 / 2 : ℝ)) ^ 2 = t := by
    dsimp [t]
    nlinarith
  have ht : 0 ≤ t := by
    rw [← hsq]
    exact sq_nonneg _
  have hs : (Real.sqrt t) ^ 2 = t := Real.sq_sqrt ht
  have hf : (y - (1 / 2 : ℝ)) ^ 2 = (Real.sqrt t) ^ 2 := by
    rw [hsq, hs]
  have hroot : y - (1 / 2 : ℝ) = Real.sqrt t := by
    rcases sq_eq_sq_iff_eq_or_eq_neg.mp hf with h1 | h2
    · exact h1
    · have hnn := Real.sqrt_nonneg t
      nlinarith
  nlinarith

/-- Forward: `g_N = g^2/(g + a0)` implies `g = g_N (1/2 + sqrt(1/4 + a0/g_N))`. -/
theorem law_forward (g gN a0 : ℝ) (hg : 0 < g) (hgN : 0 < gN) (ha0 : 0 < a0)
    (hlaw : gN = g ^ 2 / (g + a0)) :
    g = gN * ((1 / 2 : ℝ) + Real.sqrt ((1 / 4 : ℝ) + a0 / gN)) := by
  have hgp : g + a0 ≠ 0 := by linarith
  have hquad0 : gN * (g + a0) = g ^ 2 := by
    rw [hlaw]
    field_simp [hgp] <;> ring
  have hquad : (g / gN) ^ 2 - (g / gN) - a0 / gN = 0 := by
    field_simp [hgN.ne']
    nlinarith [hquad0]
  have hle : gN ≤ g := by
    rw [hlaw]
    rw [div_le_iff₀ (by linarith : 0 < g + a0)]
    nlinarith
  have hge1 : (1 : ℝ) ≤ g / gN := by
    rw [le_div_iff₀ hgN]
    nlinarith
  have hx := quad_pos_root (g / gN) (a0 / gN) hquad hge1
  have hgdef : g = gN * (g / gN) := by
    field_simp [hgN.ne']
  rw [hgdef, hx]

/-- Backward: `g = g_N (1/2 + sqrt(1/4 + a0/g_N))` implies `g_N = g^2/(g + a0)`. -/
theorem law_backward (gN a0 : ℝ) (hgN : 0 < gN) (ha0 : 0 < a0) :
    gN = (gOf gN a0) ^ 2 / (gOf gN a0 + a0) := by
  let s : ℝ := Real.sqrt ((1 / 4 : ℝ) + a0 / gN)
  have htpos : 0 < (1 / 4 : ℝ) + a0 / gN := by positivity
  have hs : s ^ 2 = (1 / 4 : ℝ) + a0 / gN := by
    dsimp [s]
    exact Real.sq_sqrt (le_of_lt htpos)
  have hdiv : gN ^ 2 * (a0 / gN) = gN * a0 := by
    field_simp [hgN.ne'] <;> ring
  have hmain : gN * (gN * ((1 / 2 : ℝ) + s) + a0) = (gN * ((1 / 2 : ℝ) + s)) ^ 2 := by
    nlinarith [hs, hdiv]
  have hsnonneg : 0 ≤ s := by
    dsimp [s]
    exact Real.sqrt_nonneg _
  have hden : gN * ((1 / 2 : ℝ) + s) + a0 ≠ 0 := by
    have hpos1 : 0 < gN * ((1 / 2 : ℝ) + s) := by positivity
    linarith
  change gN = (gN * ((1 / 2 : ℝ) + s)) ^ 2 / (gN * ((1 / 2 : ℝ) + s) + a0)
  rw [eq_div_iff hden]
  exact hmain

/-! ## 2. The halo profile X -/

theorem X_nonneg (x : ℝ) : 0 ≤ X x := by
  have h : (1 : ℝ) ≤ Real.sqrt (1 + (4 : ℝ) * x ^ 2) := by
    calc
      (1 : ℝ) = Real.sqrt 1 := by norm_num
      _ ≤ Real.sqrt (1 + (4 : ℝ) * x ^ 2) :=
        Real.sqrt_le_sqrt (by nlinarith [sq_nonneg x])
  dsimp [X]
  nlinarith

theorem X_quad (x : ℝ) : X x ^ 2 + X x = x ^ 2 := by
  have harg : 0 ≤ 1 + (4 : ℝ) * x ^ 2 := by nlinarith [sq_nonneg x]
  have hs : (Real.sqrt (1 + (4 : ℝ) * x ^ 2)) ^ 2 = 1 + (4 : ℝ) * x ^ 2 :=
    Real.sq_sqrt harg
  dsimp [X]
  nlinarith [hs]

theorem X_mul_one_add (x : ℝ) : X x * (1 + X x) = x ^ 2 := by
  have h := X_quad x
  nlinarith

theorem X_le_sq (x : ℝ) : X x ≤ x ^ 2 := by
  have hq := X_quad x
  have hn := X_nonneg x
  have hs : 0 ≤ X x ^ 2 := sq_nonneg (X x)
  nlinarith

/-- X is strictly increasing on the positive half-line: `0 < x < y` forces `X x < X y`. -/
theorem X_strictMono (x y : ℝ) (hx : 0 < x) (hxy : x < y) : X x < X y := by
  by_contra hnot
  have hle : X y ≤ X x := le_of_not_gt hnot
  have hsqle : X y ^ 2 ≤ X x ^ 2 := by
    rw [sq_le_sq]
    rw [abs_of_nonneg (X_nonneg y), abs_of_nonneg (X_nonneg x)]
    exact hle
  have hyss : y ^ 2 ≤ x ^ 2 := by
    have hxq := X_quad x
    have hyq := X_quad y
    nlinarith
  have hxyss : x ^ 2 < y ^ 2 := by
    rw [sq_lt_sq]
    rw [abs_of_pos hx, abs_of_pos (lt_trans hx hxy)]
    exact hxy
  nlinarith

/-! ## 3. Enclosed cold mass and cold density -/

/-- `sqrt (1 + 4x^2) = 1 + 2 X x`. -/
theorem one_add_two_X (x : ℝ) : 1 + 2 * X x = Real.sqrt (1 + (4 : ℝ) * x ^ 2) := by
  dsimp [X]
  ring

theorem Mc_zero (Mb rM r : ℝ) : Mc Mb rM 0 = 0 := by
  dsimp [Mc, X]
  norm_num

/-- `X` is differentiable everywhere, with `X'(x) = 2x/sqrt(1 + 4x^2)`. -/
theorem X_hasDeriv (x : ℝ) : HasDerivAt X (2 * x / Real.sqrt (1 + (4 : ℝ) * x ^ 2)) x := by
  unfold X
  have hargpos : 0 < 1 + (4 : ℝ) * x ^ 2 := by nlinarith [sq_nonneg x]
  have hargne : 1 + (4 : ℝ) * x ^ 2 ≠ 0 := ne_of_gt hargpos
  have h1a : HasDerivAt (fun y : ℝ => 1 + (4 : ℝ) * y ^ 2) ((4 : ℝ) * (2 * x)) x := by
    simpa using ((((hasDerivAt_id x).pow 2).const_mul (4 : ℝ)).const_add (1 : ℝ))
  have h1 : HasDerivAt (fun y : ℝ => 1 + (4 : ℝ) * y ^ 2) (8 * x) x := by
    simpa [show (4 : ℝ) * (2 * x) = 8 * x by ring] using h1a
  have h2 : HasDerivAt (fun y : ℝ => Real.sqrt (1 + (4 : ℝ) * y ^ 2))
      (8 * x / (2 * Real.sqrt (1 + (4 : ℝ) * x ^ 2))) x := by
    simpa using h1.sqrt hargne
  have h3 : HasDerivAt (fun y : ℝ => (Real.sqrt (1 + (4 : ℝ) * y ^ 2) - 1) / 2)
      ((8 * x / (2 * Real.sqrt (1 + (4 : ℝ) * x ^ 2))) / 2) x :=
    (h2.sub_const (1 : ℝ)).div_const (2 : ℝ)
  have hspos : 0 < Real.sqrt (1 + (4 : ℝ) * x ^ 2) := Real.sqrt_pos.2 hargpos
  have hval : (8 * x / (2 * Real.sqrt (1 + (4 : ℝ) * x ^ 2))) / 2 =
      2 * x / Real.sqrt (1 + (4 : ℝ) * x ^ 2) := by
    field_simp [hspos.ne'] <;> ring
  simpa [hval] using h3

/-- `M_c'(r) = M_b (2x/sqrt(1 + 4x^2)) / r_M` with `x = r/r_M`. -/
theorem Mc_hasDeriv (Mb rM r : ℝ) (hrM : rM ≠ 0) :
    HasDerivAt (fun s : ℝ => Mc Mb rM s)
      (Mb * ((2 * (r / rM) / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) * (1 / rM))) r := by
  have hlin : HasDerivAt (fun s : ℝ => s / rM) (1 / rM) r := by
    simpa [div_eq_mul_inv] using (hasDerivAt_id r).mul_const (rM⁻¹)
  have hc : HasDerivAt (fun s : ℝ => X (s / rM))
      ((2 * (r / rM) / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) * (1 / rM)) r := by
    simpa [Function.comp_def] using (X_hasDeriv (r / rM)).comp r hlin
  have hcM := HasDerivAt.const_mul Mb hc
  simpa [Mc] using hcM

/-- Closed form for the cold density:
`rho_c(r) = M_b / (2 pi r r_M^2 sqrt(1 + 4 (r/r_M)^2))`, valid for `r > 0`, `r_M > 0`. -/
theorem rhoC_closed (Mb rM r : ℝ) (hrM : rM ≠ 0) (hr : 0 < r) :
    rhoC Mb rM r = Mb / (2 * Real.pi * r * rM ^ 2 * Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hd : deriv (fun s : ℝ => Mc Mb rM s) r =
      Mb * ((2 * (r / rM) / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) * (1 / rM)) :=
    (Mc_hasDeriv Mb rM r hrM).deriv
  have hspos : 0 < Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2) := by
    apply Real.sqrt_pos.2
    nlinarith [sq_nonneg (r / rM)]
  dsimp [rhoC]
  rw [hd]
  field_simp [hr.ne', hrM, hspos.ne', hpi] <;> ring

/-- The lane's form of item 3:
`rho_c = (M_b/(4 pi r_M^3)) * 2/(x sqrt(1 + 4x^2))` with `x = r/r_M`. -/
theorem rhoC_closed_x (Mb rM r : ℝ) (hrM : 0 < rM) (hr : 0 < r) :
    rhoC Mb rM r = (Mb / (4 * Real.pi * rM ^ 3)) *
        (2 / ((r / rM) * Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2))) := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hspos : 0 < Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2) := by
    apply Real.sqrt_pos.2
    nlinarith [sq_nonneg (r / rM)]
  rw [rhoC_closed Mb rM r hrM.ne' hr]
  field_simp [hr.ne', hrM.ne', hspos.ne', hpi] <;> ring

/-- Multiplying by r removes the 1/r:
`r rho_c(r) = (M_b/r_M^2) / (2 pi sqrt(1 + 4(r/r_M)^2))`. -/
theorem rhoC_mul_r (Mb rM r : ℝ) (hrM : rM ≠ 0) (hr : 0 < r) :
    r * rhoC Mb rM r = (Mb / rM ^ 2) / (2 * Real.pi * Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hspos : 0 < Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2) := by
    apply Real.sqrt_pos.2
    nlinarith [sq_nonneg (r / rM)]
  rw [rhoC_closed Mb rM r hrM hr]
  field_simp [hr.ne', hrM, hspos.ne', hpi] <;> ring

/-! ## 3b. A square-root rescaling used by the outer limit -/

/-- `a sqrt b = sqrt (a^2 b)` for `a >= 0`, `b >= 0`. -/
theorem sqrt_mul_nonneg (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a * Real.sqrt b = Real.sqrt (a ^ 2 * b) := by
  have h1 : (a * Real.sqrt b) ^ 2 = a ^ 2 * b := by
    rw [mul_pow, Real.sq_sqrt hb]
  have h2 : (Real.sqrt (a ^ 2 * b)) ^ 2 = a ^ 2 * b := by
    exact Real.sq_sqrt (mul_nonneg (sq_nonneg a) hb)
  have heq : (a * Real.sqrt b) ^ 2 = (Real.sqrt (a ^ 2 * b)) ^ 2 := by
    rw [h1, h2]
  rcases sq_eq_sq_iff_eq_or_eq_neg.mp heq with h | h
  · exact h
  · have hn1 : 0 ≤ a * Real.sqrt b := mul_nonneg ha (Real.sqrt_nonneg b)
    have hn2 : 0 ≤ Real.sqrt (a ^ 2 * b) := Real.sqrt_nonneg _
    nlinarith

/-- The halo rescaling: with `x = r/r_M` and `y = r_M/r = 1/x`,
`x sqrt (4 + y^2) = sqrt (1 + 4x^2)` for `r > 0`, `r_M > 0`. -/
theorem halo_sqrt_identity (r rM : ℝ) (hr : 0 < r) (hrM : 0 < rM) :
    (r / rM) * Real.sqrt (4 + (rM / r) ^ 2) = Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2) := by
  have hxpos : 0 < r / rM := by positivity
  have hb : 0 ≤ 4 + (rM / r) ^ 2 := by positivity
  have h := sqrt_mul_nonneg (r / rM) (4 + (rM / r) ^ 2) (le_of_lt hxpos) hb
  have hinside : (r / rM) ^ 2 * (4 + (rM / r) ^ 2) = 1 + (4 : ℝ) * (r / rM) ^ 2 := by
    field_simp [hr.ne', hrM.ne'] <;> ring
  rw [hinside] at h
  exact h

/-- `r^2 rho_c(r) = (M_b/(2 pi r_M)) / sqrt (4 + (r_M/r)^2)`. -/
theorem rhoC_mul_rsq (Mb rM r : ℝ) (hrM : 0 < rM) (hr : 0 < r) :
    r ^ 2 * rhoC Mb rM r = (Mb / (2 * Real.pi * rM)) /
        Real.sqrt (4 + (rM / r) ^ 2) := by
  have hrm : rM ≠ 0 := ne_of_gt hrM
  have hrr : r ≠ 0 := ne_of_gt hr
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hs : Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2) ≠ 0 := by
    apply ne_of_gt
    apply Real.sqrt_pos.2
    nlinarith [sq_nonneg (r / rM)]
  have hT : Real.sqrt (4 + (rM / r) ^ 2) ≠ 0 := by
    apply ne_of_gt
    apply Real.sqrt_pos.2
    positivity
  have hxy : (r / rM) / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2) =
      1 / Real.sqrt (4 + (rM / r) ^ 2) := by
    rw [div_eq_iff hs]
    rw [one_div, mul_comm]
    exact (eq_div_iff hT).2 (halo_sqrt_identity r rM hr hrM)
  have hstep : r ^ 2 * rhoC Mb rM r =
      (Mb / (2 * Real.pi * rM)) * ((r / rM) / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) := by
    rw [rhoC_closed Mb rM r hrm hr]
    field_simp [hrr, hrm, hs, hpi] <;> ring
  rw [hstep, hxy]
  ring

/-! ## 4. The two limits (explicit epsilon-delta) -/

/-- Continuity helper for the inner (column) limit. `A / sqrt (1 + 4 (r/r_M)^2)` is
continuous at `r = 0` because the square-root argument is `>= 1` there. -/
private theorem cont_col (A rM : ℝ) (hrM : 0 < rM) :
    ContinuousAt (fun r : ℝ => A / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) 0 := by
  fun_prop (disch := positivity)

/-- Continuity helper for the outer limit: `A / sqrt (4 + y^2)` is continuous at `y = 0`. -/
private theorem cont_outer (A : ℝ) :
    ContinuousAt (fun y : ℝ => A / Real.sqrt (4 + y ^ 2)) 0 := by
  fun_prop (disch := positivity)

/-- **The universal column.** With `r_M^2 = G M_b/a0` (footing: the halo scale is the radius
at which the Newtonian field equals a0),
`r rho_c(r) -> a0/(2 pi G)` as `r -> 0+`: for every `eps > 0` there is a `delta > 0` with
`|r rho_c(r) - a0/(2 pi G)| < eps` for all `0 < r < delta`. -/
theorem rhoC_column_limit (G Mb a0 rM : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hrM : 0 < rM) (hrMdef : rM ^ 2 = G * Mb / a0) :
    ∀ ε > 0, ∃ δ > 0, ∀ r : ℝ, 0 < r → r < δ →
      |r * rhoC Mb rM r - a0 / (2 * Real.pi * G)| < ε := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hGM : G * Mb = a0 * rM ^ 2 := closure_mul G Mb a0 rM ha0 hrMdef
  have hA : a0 / (2 * Real.pi * G) = Mb / (2 * Real.pi * rM ^ 2) := by
    field_simp [hG.ne', hrM.ne', hpi] <;> nlinarith [hGM]
  intro ε hε
  have hcont : ContinuousAt
      (fun r : ℝ => (Mb / (2 * Real.pi * rM ^ 2)) / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2)) 0 :=
    cont_col (Mb / (2 * Real.pi * rM ^ 2)) rM hrM
  rcases (Metric.continuousAt_iff.mp hcont) ε hε with ⟨δ, hδpos, hδ⟩
  refine ⟨δ, hδpos, ?_⟩
  intro r hrpos hrlt
  have hd : dist r 0 < δ := by
    rw [Real.dist_eq, sub_zero, abs_of_pos hrpos]
    exact hrlt
  have hclose := hδ (x := r) hd
  have hrhor : r * rhoC Mb rM r =
      (Mb / (2 * Real.pi * rM ^ 2)) / Real.sqrt (1 + (4 : ℝ) * (r / rM) ^ 2) := by
    rw [rhoC_mul_r Mb rM r hrM.ne' hrpos]
    ring_nf
  have hphi0 : ((Mb / (2 * Real.pi * rM ^ 2)) /
        Real.sqrt (1 + (4 : ℝ) * (0 / rM) ^ 2)) = Mb / (2 * Real.pi * rM ^ 2) := by
    norm_num
  rw [hrhor, hA]
  simpa [Real.dist_eq, hphi0] using hclose

/-- **The weak-field (outer) limit.** With `r_M^2 = G M_b/a0`,
`r^2 rho_c(r) -> sqrt(G M_b a0)/(4 pi G)` as `r -> oo`: for every `eps > 0` there is a
`B > 0` with `|r^2 rho_c(r) - sqrt(G M_b a0)/(4 pi G)| < eps` for all `r >= B`. -/
theorem rhoC_outer_limit (G Mb a0 rM : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hrM : 0 < rM) (hrMdef : rM ^ 2 = G * Mb / a0) :
    ∀ ε > 0, ∃ B > 0, ∀ r : ℝ, B ≤ r →
      |r ^ 2 * rhoC Mb rM r - Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)| < ε := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hGM : G * Mb = a0 * rM ^ 2 := closure_mul G Mb a0 rM ha0 hrMdef
  have ha0eq : a0 = G * Mb / rM ^ 2 := by
    field_simp [hrM.ne'] <;> nlinarith [hGM]
  have hsqrt : Real.sqrt (G * Mb * a0) = G * Mb / rM := by
    have hsq1 : (G * Mb / rM) ^ 2 = G * Mb * a0 := by
      rw [ha0eq]
      field_simp [hrM.ne'] <;> ring
    have hsq2 : (Real.sqrt (G * Mb * a0)) ^ 2 = G * Mb * a0 := by
      exact Real.sq_sqrt (by positivity)
    have heq : (Real.sqrt (G * Mb * a0)) ^ 2 = (G * Mb / rM) ^ 2 := by
      rw [hsq2, hsq1]
    rcases sq_eq_sq_iff_eq_or_eq_neg.mp heq with h | h
    · exact h
    · have hn1 : 0 ≤ G * Mb / rM := by positivity
      have hn2 : 0 ≤ Real.sqrt (G * Mb * a0) := Real.sqrt_nonneg _
      nlinarith
  have hL : Real.sqrt (G * Mb * a0) / (4 * Real.pi * G) =
      (Mb / (2 * Real.pi * rM)) / 2 := by
    rw [hsqrt]
    field_simp [hG.ne', hrM.ne', hpi] <;> ring
  intro ε hε
  have hcont : ContinuousAt (fun y : ℝ => (Mb / (2 * Real.pi * rM)) /
      Real.sqrt (4 + y ^ 2)) 0 := cont_outer (Mb / (2 * Real.pi * rM))
  rcases (Metric.continuousAt_iff.mp hcont) ε hε with ⟨δ, hδpos, hδ⟩
  refine ⟨2 * rM / δ, by positivity, ?_⟩
  intro r hrge
  have hBpos : 0 < 2 * rM / δ := by positivity
  have hrpos : 0 < r := by linarith
  have hypos : 0 < rM / r := by positivity
  have hrd : 2 * rM ≤ r * δ := by
    have h := mul_le_mul_of_nonneg_right hrge (le_of_lt hδpos)
    have hcancel : (2 * rM / δ) * δ = 2 * rM := by
      field_simp [hδpos.ne'] <;> ring
    rwa [hcancel] at h
  have hult : dist (rM / r) 0 < δ := by
    rw [Real.dist_eq, sub_zero, abs_of_pos hypos]
    have hhalf : rM / r ≤ δ / 2 := by
      rw [div_le_iff₀ hrpos]
      nlinarith
    linarith
  have hclose := hδ (x := rM / r) hult
  have hrsq : r ^ 2 * rhoC Mb rM r =
      (Mb / (2 * Real.pi * rM)) / Real.sqrt (4 + (rM / r) ^ 2) :=
    rhoC_mul_rsq Mb rM r hrM hrpos
  rw [hrsq, hL]
  have hsqrt4' : Real.sqrt (4 : ℝ) = 2 := by norm_num
  simpa [Real.dist_eq, hsqrt4'] using hclose

/-! ## 5. The asymptotic speed -/

theorem vInf_sq (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    vInf G Mb a0 ^ 2 = Real.sqrt (G * Mb * a0) := by
  unfold vInf
  exact Real.sq_sqrt (by positivity : 0 ≤ Real.sqrt (G * Mb * a0))

/-- `v_inf^4 = G M_b a0`. -/
theorem vInf_four (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    vInf G Mb a0 ^ 4 = G * Mb * a0 := by
  have hs := vInf_sq G Mb a0 hG hMb ha0
  calc
    vInf G Mb a0 ^ 4 = (vInf G Mb a0 ^ 2) ^ 2 := by ring
    _ = (Real.sqrt (G * Mb * a0)) ^ 2 := by rw [hs]
    _ = G * Mb * a0 := Real.sq_sqrt (by positivity : 0 ≤ G * Mb * a0)

/-- On the halo scale, `v_inf^2 = G M_b/r_M`: the flat speed is the Newtonian speed at
the closure radius. -/
theorem vInf_sq_rM (G Mb a0 rM : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hrM : 0 < rM) (hrMdef : rM ^ 2 = G * Mb / a0) :
    vInf G Mb a0 ^ 2 = G * Mb / rM := by
  rw [vInf_sq G Mb a0 hG hMb ha0]
  have hGM : G * Mb = a0 * rM ^ 2 := closure_mul G Mb a0 rM ha0 hrMdef
  have ha0eq : a0 = G * Mb / rM ^ 2 := by
    field_simp [hrM.ne'] <;> nlinarith [hGM]
  rw [ha0eq]
  have hsq1 : (G * Mb / rM) ^ 2 = G * Mb * (G * Mb / rM ^ 2) := by
    field_simp [hrM.ne'] <;> ring
  have hsq2 : (Real.sqrt (G * Mb * (G * Mb / rM ^ 2))) ^ 2 =
      G * Mb * (G * Mb / rM ^ 2) := by
    exact Real.sq_sqrt (by positivity)
  have heq : (Real.sqrt (G * Mb * (G * Mb / rM ^ 2))) ^ 2 = (G * Mb / rM) ^ 2 := by
    rw [hsq2, hsq1]
  rcases sq_eq_sq_iff_eq_or_eq_neg.mp heq with h | h
  · exact h
  · have hn1 : 0 ≤ G * Mb / rM := by positivity
    have hn2 : 0 ≤ Real.sqrt (G * Mb * (G * Mb / rM ^ 2)) := Real.sqrt_nonneg _
    nlinarith

end FINAL9

#print axioms FINAL9.quad_pos_root
#print axioms FINAL9.law_forward
#print axioms FINAL9.law_backward
#print axioms FINAL9.X_nonneg
#print axioms FINAL9.X_quad
#print axioms FINAL9.X_mul_one_add
#print axioms FINAL9.X_le_sq
#print axioms FINAL9.X_strictMono
#print axioms FINAL9.Mc_zero
#print axioms FINAL9.X_hasDeriv
#print axioms FINAL9.Mc_hasDeriv
#print axioms FINAL9.rhoC_closed
#print axioms FINAL9.rhoC_closed_x
#print axioms FINAL9.rhoC_column_limit
#print axioms FINAL9.rhoC_outer_limit
#print axioms FINAL9.vInf_sq
#print axioms FINAL9.vInf_four
#print axioms FINAL9.vInf_sq_rM
-- kappa = 1/2 FITTED; footings never pooled; the cold component is cold dark energy, no
-- particle; not theory closed. Adopts nothing.
