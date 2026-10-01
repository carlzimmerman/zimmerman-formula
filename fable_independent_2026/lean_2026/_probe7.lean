import Mathlib
import Mathlib.Tactic

noncomputable section

def mu2p (u : ℝ) : ℝ := u * (2 + u) / ((1 + u) * (1 + u))

-- 1: 2 + x via const_add
example (u : ℝ) : HasDerivAt (fun x : ℝ => 2 + x) 1 u := by
  simpa using (hasDerivAt_id u).const_add (2 : ℝ)

-- 2: product x*(2+x) direct assignment
example (u : ℝ) : HasDerivAt (fun x : ℝ => x * (2 + x)) (1 * (2 + u) + u * 1) u := by
  have h2x : HasDerivAt (fun x : ℝ => 2 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (2 : ℝ)
  exact (hasDerivAt_id u).mul h2x

-- 3: (1+x)*(1+x) direct assignment
example (u : ℝ) : HasDerivAt (fun x : ℝ => (1 + x) * (1 + x)) (1 * (1 + u) + (1 + u) * 1) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (1 : ℝ)
  exact hlin.mul hlin

-- 4: quotient, then change to mu2p
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt mu2p ((1 * (2 + u) + u * 1) * ((1 + u) * (1 + u))
      - (u * (2 + u)) * (1 * (1 + u) + (1 + u) * 1)) / (((1 + u) * (1 + u))^2) u := by
  have h2x : HasDerivAt (fun x : ℝ => 2 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (2 : ℝ)
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (1 : ℝ)
  have hn : HasDerivAt (fun x : ℝ => x * (2 + x)) (1 * (2 + u) + u * 1) u :=
    (hasDerivAt_id u).mul h2x
  have hd : HasDerivAt (fun x : ℝ => (1 + x) * (1 + x)) (1 * (1 + u) + (1 + u) * 1) u :=
    hlin.mul hlin
  have hdne : (1 + u) * (1 + u) ≠ 0 := mul_ne_zero hu hu
  have hq := hn.div hd hdne
  simpa [mu2p] using hq

-- 5: inv via hasDerivAt_inv comp
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-(((1 + u)^2)⁻¹)) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (1 : ℝ)
  simpa [Function.comp_def] using (hasDerivAt_inv hu).comp u hlin

-- 6: log comp
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt (fun x : ℝ => Real.log (1 + x)) ((1 + u)⁻¹) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (1 : ℝ)
  simpa [Function.comp_def] using (Real.hasDerivAt_log hu).comp u hlin

-- 7: chain of sub / const_mul / add_const
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt (fun x : ℝ => x^2 - 2 * Real.log (1 + x) - 2 * (1 + x)⁻¹ + 1)
      (2 * u - 2 * (1 + u)⁻¹ - 2 * (-(((1 + u)^2)⁻¹))) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by
    simpa using (hasDerivAt_id u).const_add (1 : ℝ)
  have hsq : HasDerivAt (fun x : ℝ => x^2) (2 * u) u := by simpa using hasDerivAt_pow 2 u
  have hlog : HasDerivAt (fun x : ℝ => Real.log (1 + x)) ((1 + u)⁻¹) u := by
    simpa [Function.comp_def] using (Real.hasDerivAt_log hu).comp u hlin
  have hinv : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-(((1 + u)^2)⁻¹)) u := by
    simpa [Function.comp_def] using (hasDerivAt_inv hu).comp u hlin
  exact (((hsq.sub (hlog.const_mul 2)).sub (hinv.const_mul 2)).add_const 1)
