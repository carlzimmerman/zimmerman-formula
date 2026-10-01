import Mathlib
open scoped BigOperators

noncomputable section
open Finset

/-! # AS263 -- Lean certificate: the time-dependent projector commutator

Certifies the algebraic core of seed AS263 on a finite mode set `Fin n` with
positive leaf weights `w_i(t)` (the leaf volume densities sqrt(h)(t,x_i)):
their transport law is `d/dt w_i = c_i * w_i` with `c_i = (N K)(x_i)` (the
lapse-weighted expansion), and `z_i(t)` is a test field with `d/dt z_i = zd_i`.

The varied intrinsic (volume) mean and the mean-zero projector of the action
are  Avg w f = (sum_i w_i f_i)/(sum_i w_i),  Proj w f = f - Avg w f.

* `covariance_centering`:  <c (z - <z>)> = <c z> - <z> <c>  (pure algebra).
* `mean_deriv_value`:      the quotient-rule value identity of the mean.
* `mean_deriv_quotient`:   d/dt <z>_h = <zd> + <c z> - <z><c> = <d/dt z + c P z>.
* `projector_commutator`:  [d/dt, Proj] z = -<c P z>:
   d/dt(Proj z)_i = (zd_i - <zd>) - <c (z - <z>)>  (pointwise).
* `constant_field_commutator`:  z constant  =>  d/dt(Proj z) = 0  (control 1).
* `homogeneous_sector`:  c constant and <z> = 0  =>  d/dt(Proj z) = P(zd):
   the commutator vanishes in exact homogeneity (control, homogeneous sector).

All sums are explicit `Finset.univ.sum` terms (this build's big-operator
binder elaborator rejects annotated binders).  Zero sorry; axioms must be
subset {propext, Classical.choice, Quot.sound}.
-/

namespace AS263

def S {n : ℕ} (w : Fin n → ℝ) : ℝ := Finset.univ.sum (fun i : Fin n => w i)

def Avg {n : ℕ} (w f : Fin n → ℝ) : ℝ :=
  (Finset.univ.sum (fun i : Fin n => w i * f i)) / S w

def Proj {n : ℕ} (w f : Fin n → ℝ) : Fin n → ℝ := fun i => f i - Avg w f

/-- Centering lemma:  <c (z - <z>)> = <c z> - <z> <c>. -/
theorem covariance_centering {n : ℕ} (w c z : Fin n → ℝ) (hW : S w ≠ 0) :
    Avg w (fun i => c i * (z i - Avg w z)) = Avg w (fun i => c i * z i) - Avg w z * Avg w c := by
  change (Finset.univ.sum (fun i : Fin n => w i * (c i * (z i - Avg w z))))
            / (Finset.univ.sum (fun i : Fin n => w i))
        = (Finset.univ.sum (fun i : Fin n => w i * (c i * z i)))
            / (Finset.univ.sum (fun i : Fin n => w i))
          - Avg w z * Avg w c
  have hlin : (fun i : Fin n => w i * (c i * (z i - Avg w z)))
            = fun i : Fin n => w i * c i * z i - w i * c i * Avg w z := by
    funext i
    ring
  have hcz : (fun i : Fin n => w i * (c i * z i)) = fun i : Fin n => w i * c i * z i := by
    funext i
    ring
  rw [hlin, hcz, Finset.sum_sub_distrib]
  rw [← Finset.sum_mul]
  unfold Avg S at *
  field_simp [hW]

/-- The quotient-rule value identity: the derivative value of the mean equals
    <zd> + <c z> - <z> <c>.  (Raw division form matches HasDerivAt.div.) -/
theorem mean_deriv_value {n : ℕ} (w z zd c : Fin n → ℝ) (hW : S w ≠ 0) :
    (((Finset.univ.sum (fun i : Fin n => (c i * w i) * z i + w i * zd i)) * S w
        - (Finset.univ.sum (fun i : Fin n => w i * z i))
          * (Finset.univ.sum (fun i : Fin n => c i * w i)))
       / S w ^ 2)
    = Avg w zd + Avg w (fun i => c i * z i) - Avg w z * Avg w c := by
  unfold Avg S at *
  rw [Finset.sum_add_distrib]
  have hcw : (Finset.univ.sum (fun i : Fin n => (c i * w i) * z i))
           = Finset.univ.sum (fun i : Fin n => w i * c i * z i) := by
    apply Finset.sum_congr rfl
    intro i hi
    ring
  have hcz : (fun i : Fin n => w i * (c i * z i)) = fun i : Fin n => w i * c i * z i := by
    funext i
    ring
  have hwc : (fun i : Fin n => c i * w i) = fun i : Fin n => w i * c i := by
    funext i
    ring
  rw [hcw, hcz, hwc]
  field_simp [hW]
  ring

/-- HasDerivAt.sum produces sum-of-functions; this is the pointwise reshape. -/
lemma sum_of_functions_id {n : ℕ} (w z : Fin n → ℝ → ℝ) :
    (fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t * z i t))
      = Finset.univ.sum (fun i : Fin n => fun t : ℝ => w i t * z i t) := by
  ext t
  simp only [Finset.sum_apply]

/-- Mean-derivative identity (differential form):
    d/dt <z>_h = <zd>_h + <c z>_h - <z>_h <c>_h,  for w' = c w.
    Equivalently d/dt <z>_h = <d/dt z + c P z>_h (see `mean_deriv_value`). -/
theorem mean_deriv_quotient {n : ℕ} (w z : Fin n → ℝ → ℝ) (zd c : Fin n → ℝ) (τ : ℝ)
    (hw : ∀ i, HasDerivAt (w i) (c i * w i τ) τ)
    (hz : ∀ i, HasDerivAt (z i) (zd i) τ)
    (hW : S (fun i => w i τ) ≠ 0) :
    HasDerivAt (fun t => Avg (fun i => w i t) (fun i => z i t))
      (Avg (fun i => w i τ) zd + Avg (fun i => w i τ) (fun i => c i * z i τ)
        - Avg (fun i => w i τ) (fun i => z i τ) * Avg (fun i => w i τ) c) τ := by
  have hN : HasDerivAt (fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t * z i t))
      (Finset.univ.sum (fun i : Fin n => (c i * w i τ) * z i τ + w i τ * zd i)) τ := by
    have hprod : ∀ i : Fin n, HasDerivAt (fun t : ℝ => w i t * z i t)
        ((c i * w i τ) * z i τ + w i τ * zd i) τ := by
      intro i
      exact (hw i).mul (hz i)
    have hS := HasDerivAt.sum (u := Finset.univ) (fun i _hi => hprod i)
    rw [sum_of_functions_id w z]
    exact hS
  have hD : HasDerivAt (fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t))
      (Finset.univ.sum (fun i : Fin n => c i * w i τ)) τ := by
    have hS := HasDerivAt.sum (u := Finset.univ) (fun i _hi => hw i)
    rw [show (fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t))
            = Finset.univ.sum (fun i : Fin n => fun t : ℝ => w i t) by
        ext t
        simp only [Finset.sum_apply]]
    exact hS
  have hdiv := hN.div hD hW
  have hval := mean_deriv_value (fun i : Fin n => w i τ) (fun i : Fin n => z i τ) zd c hW
  change HasDerivAt
      ((fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t * z i t))
        / (fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t)))
      (Avg (fun i => w i τ) zd + Avg (fun i => w i τ) (fun i => c i * z i τ)
        - Avg (fun i => w i τ) (fun i => z i τ) * Avg (fun i => w i τ) c) τ
  rw [← hval]
  exact hdiv

/-- The projector commutator at a point:
    d/dt (Proj z)_i = (zd_i - <zd>) - <c (z - <z>)>,   i.e.
    d/dt P_h Z = P_h (d/dt Z) - <N K P_h Z>_h  (leaf-constant remainder). -/
theorem projector_commutator {n : ℕ} (w z : Fin n → ℝ → ℝ) (zd c : Fin n → ℝ) (τ : ℝ)
    (hw : ∀ i, HasDerivAt (w i) (c i * w i τ) τ)
    (hz : ∀ i, HasDerivAt (z i) (zd i) τ)
    (hW : S (fun i => w i τ) ≠ 0) (i : Fin n) :
    deriv (fun t => Proj (fun j => w j t) (fun j => z j t) i) τ
      = zd i - Avg (fun j => w j τ) zd
        - Avg (fun j => w j τ) (fun j => c j * (z j τ - Avg (fun k => w k τ) (fun k => z k τ))) := by
  have hM := mean_deriv_quotient w z zd c τ hw hz hW
  have hsub : HasDerivAt (fun t : ℝ => z i t - Avg (fun j => w j t) (fun j => z j t))
      (zd i - (Avg (fun j => w j τ) zd + Avg (fun j => w j τ) (fun j => c j * z j τ)
                - Avg (fun j => w j τ) (fun j => z j τ) * Avg (fun j => w j τ) c)) τ :=
    (hz i).sub hM
  unfold Proj
  change deriv (fun t : ℝ => z i t - Avg (fun j => w j t) (fun j => z j t)) τ
      = zd i - Avg (fun j => w j τ) zd
        - Avg (fun j => w j τ) (fun j => c j * (z j τ - Avg (fun k => w k τ) (fun k => z k τ)))
  rw [hsub.deriv]
  have hcov := covariance_centering (fun j : Fin n => w j τ) c (fun j : Fin n => z j τ) hW
  rw [hcov]
  ring

/-- Control 1: a spatially constant test field has zero commutator. -/
theorem constant_field_commutator {n : ℕ} (w : Fin n → ℝ → ℝ) (z : Fin n → ℝ → ℝ)
    (C τ : ℝ) (hz : ∀ i t, z i t = C) (hW : ∀ t, S (fun j => w j t) ≠ 0) (i : Fin n) :
    deriv (fun t => Proj (fun j => w j t) (fun j => z j t) i) τ = 0 := by
  have h0 : ∀ t : ℝ, (Proj (fun j => w j t) (fun j => z j t)) i = 0 := by
    intro t
    unfold Proj Avg S at *
    change z i t - (Finset.univ.sum (fun j : Fin n => w j t * z j t)) / (Finset.univ.sum (fun j : Fin n => w j t)) = 0
    simp only [hz]
    have hsum : Finset.univ.sum (fun j : Fin n => w j t * C)
              = C * Finset.univ.sum (fun j : Fin n => w j t) := by
      rw [← Finset.sum_mul]
      ring
    rw [hsum]
    have hWt : Finset.univ.sum (fun j : Fin n => w j t) ≠ 0 := by
      simpa [S] using hW t
    field_simp [hWt]
    ring
  have hfunc : (fun t => Proj (fun j => w j t) (fun j => z j t) i) = fun _ : ℝ => 0 := by
    funext t
    exact h0 t
  rw [hfunc]
  simp

/-- Homogeneous sector: c constant (N K = 3H leaf-constant) and <z> = 0
    give d/dt P z = P (d/dt z): the commutator remainder vanishes. -/
theorem homogeneous_sector {n : ℕ} (w z : Fin n → ℝ → ℝ) (zd : Fin n → ℝ) (C τ : ℝ)
    (hw : ∀ i, HasDerivAt (w i) (C * w i τ) τ)
    (hz : ∀ i, HasDerivAt (z i) (zd i) τ)
    (hW : S (fun i => w i τ) ≠ 0) (hZ : Avg (fun j => w j τ) (fun j => z j τ) = 0) (i : Fin n) :
    deriv (fun t => Proj (fun j => w j t) (fun j => z j t) i) τ
      = zd i - Avg (fun j => w j τ) zd := by
  have hcomm := projector_commutator w z zd (fun _ : Fin n => C) τ hw hz hW i
  have hZ' : Avg (fun j : Fin n => w j τ) (fun j : Fin n => z j τ) = 0 := by
    simpa using hZ
  rw [hZ'] at hcomm
  have hZ0 : Finset.univ.sum (fun j : Fin n => w j τ * z j τ) = 0 := by
    unfold Avg S at hZ'
    have hZ'' : (Finset.univ.sum (fun j : Fin n => w j τ * z j τ))
                / (Finset.univ.sum (fun j : Fin n => w j τ)) = 0 := by
      simpa using hZ'
    have hWt0 : (Finset.univ.sum (fun j : Fin n => w j τ)) ≠ 0 := by
      simpa [S] using hW
    field_simp [hWt0] at hZ''
    simpa using hZ''
  have hlast : Avg (fun j => w j τ) (fun j => C * (z j τ - 0 : ℝ)) = 0 := by
    change (Finset.univ.sum (fun j : Fin n => w j τ * (C * (z j τ - 0 : ℝ))))
              / (Finset.univ.sum (fun j : Fin n => w j τ)) = 0
    have hlin : (fun j : Fin n => w j τ * (C * (z j τ - 0 : ℝ)))
              = fun j : Fin n => (w j τ * z j τ) * C := by
      funext j
      ring
    rw [hlin]
    rw [← Finset.sum_mul]
    rw [hZ0]
    simp
  rw [hlast] at hcomm
  simpa [Avg, S] using hcomm

#check covariance_centering
#check mean_deriv_value
#check mean_deriv_quotient
#check projector_commutator
#check constant_field_commutator
#check homogeneous_sector

#print axioms covariance_centering
#print axioms mean_deriv_value
#print axioms mean_deriv_quotient
#print axioms projector_commutator
#print axioms constant_field_commutator
#print axioms homogeneous_sector

end AS263
