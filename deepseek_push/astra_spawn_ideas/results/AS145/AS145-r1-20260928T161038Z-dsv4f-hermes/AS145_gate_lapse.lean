import Mathlib

/-!
AS145 (Tier-0): gate contribution to the lapse equation — algebraic core.

Pinned action: CA4-GNC host (real_research/common_action_2026_09_26/action/
FINAL_ACTION.md, sha256 b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e)
eq. (3), (4), (12), branch CA5-GNC-R (reciprocal dark sector).

Target (task math):  Y = J(DW_b) + ell * Delta_h W_b - theta, and
    delta_lnN S_gate = C_N * int N sqrt(h) dlnN * [G(Y_h) - ell Delta_h W_b],
with S_gate = C_N * int N sqrt(h) [G(Y_h) + ell a . DW_b],  a = D ln N,
varied at FIXED (h, U) (hence fixed W_b = S_h U) on a compact closed leaf,
before any field elimination.

Certified algebra over R (1D flat prototypes of the pointwise identities;
the semantic mapping is documented in derivation.md):
  1. `divergence_reduction`  — the pivotal identity
         Delta_N W = N^{-1} D_i (N D^i W) = Delta_h W + a . DW
     in 1D prototype form:  (1/N)(N W')' = W'' + (N'/N) W'.
  2. `lapse_acceleration`    — the lapse acceleration a is literally the log
     derivative:  a = (ln N)' = N^{-1} * N'  (HasDerivAt form).
  3. `lapse_divergence_reduction` — the subtraction form used in eq. (12):
         (1/N)(N W')' - (N'/N) W' = W''.
  4. `no_Gpp_term`          — why NO G'' term occurs in this first variation:
     if the gate argument Y has vanishing derivative (Y lapse-independent at
     fixed h, U:  delta_lnN Y_h = 0), then the flux derivative of
     G'(Y) * W' contains NO G'' contribution:  it equals G'(Y_z) * W''.
  5. `Gpp_split`            — negative control (Delta_h -> Delta_N inside Y):
     for a lapse-DEPENDENT argument (derivative y' != 0) the chain rule fires
     and the G''-proportional term g'' * y' * W' appears in the flux
     derivative.  This is exactly the term the unswapped construction lacks.
-/

namespace AS145

/-- Pivotal identity:  (1/N)(N f')' = f'' + (N'/N) f'.
    1D prototype of  Delta_N W = N^{-1} D_i (N D^i W) = Delta_h W + a . DW.
    Note: `N * fun x => deriv f x` is the pointwise product function
    `fun y => N y * deriv f y`; the notation matches `deriv_mul` in this
    build, so the rewrite below closes syntactically. -/
theorem divergence_reduction (N f : ℝ → ℝ) (z : ℝ)
    (hN : DifferentiableAt ℝ N z) (hNnz : N z ≠ 0)
    (hf2 : DifferentiableAt ℝ (fun x => deriv f x) z) :
    (1 / N z) * deriv (N * fun x => deriv f x) z
      = deriv (fun x => deriv f x) z + (deriv N z / N z) * deriv f z := by
  have h := deriv_mul hN hf2
  rw [h]
  field_simp [hNnz] <;> ring

/-- The lapse acceleration is the log derivative:  a = (ln N)' = N^{-1} * N'. -/
theorem lapse_acceleration (N : ℝ → ℝ) (z : ℝ)
    (hNnz : N z ≠ 0) (hN : DifferentiableAt ℝ N z) :
    HasDerivAt (fun x => Real.log (N x)) ((N z)⁻¹ * deriv N z) z := by
  have hlog := Real.hasDerivAt_log hNnz
  have hNd : HasDerivAt N (deriv N z) z := hN.hasDerivAt
  have hc := hlog.comp z hNd
  have hc' : HasDerivAt (Real.log ∘ N) ((N z)⁻¹ * deriv N z) z := hc
  change HasDerivAt (fun x => Real.log (N x)) ((N z)⁻¹ * deriv N z) z
  exact hc'

/-- Subtraction form used in eq. (12):  Delta_N W - a . DW = Delta_h W.
    Uses `divergence_reduction` + the log-lapse convention a = N'/N. -/
theorem lapse_divergence_reduction (N W : ℝ → ℝ) (z : ℝ)
    (hN : DifferentiableAt ℝ N z) (hNnz : N z ≠ 0)
    (hW2 : DifferentiableAt ℝ (fun x => deriv W x) z) :
    (1 / N z) * deriv (N * fun x => deriv W x) z
        - (deriv N z / N z) * deriv W z
      = deriv (fun x => deriv W x) z := by
  have h := divergence_reduction N W z hN hNnz hW2
  rw [h]
  field_simp [hNnz] <;> ring

/-- No G'' term: for a lapse-INDEPENDENT gate argument (deriv Y = 0) the flux
    derivative of  G'(Y) * W'  carries no G'' contribution; it collapses to
    G'(Y z) * W''(z).  This is the structural reason eq. (12) contains no
    G'' |DW|^2 lapse-gradient term:  delta_lnN Y_h = 0 at fixed (h, U). -/
theorem no_Gpp_term (G Y W : ℝ → ℝ) (z : ℝ)
    (hGp : DifferentiableAt ℝ (fun u => deriv G u) (Y z))
    (hY : HasDerivAt Y 0 z)
    (hW2 : DifferentiableAt ℝ (fun x => deriv W x) z) :
    deriv ((fun x => (fun u => deriv G u) (Y x)) * fun x => deriv W x) z
      = deriv G (Y z) * deriv (fun x => deriv W x) z := by
  have hcomp : HasDerivAt (fun x => (fun u => deriv G u) (Y x)) 0 z := by
    have h := (hGp.hasDerivAt).comp z hY
    have hz : HasDerivAt ((fun u => deriv G u) ∘ Y) 0 z := by
      simpa [mul_zero] using h
    change HasDerivAt (fun x => (fun u => deriv G u) (Y x)) 0 z
    exact hz
  have hd : DifferentiableAt ℝ (fun x => (fun u => deriv G u) (Y x)) z :=
    hcomp.differentiableAt
  have hm := deriv_mul hd hW2
  have hd0 : deriv (fun x => (fun u => deriv G u) (Y x)) z = 0 := hcomp.deriv
  rw [hm, hd0, zero_mul, zero_add]

/-- Negative control: for a lapse-DEPENDENT gate argument (deriv Y = y') the
    chain rule fires through G'' and the flux derivative of G'(Y) * W'
    acquires the G''-proportional term  g'' * y' * W'(z).
    Replacing Delta_h by Delta_N INSIDE Y makes Y lapse-dependent, and this
    is exactly the G'' term that then appears in the lapse equation. -/
theorem Gpp_split (G Y W : ℝ → ℝ) (y' g'' : ℝ) (z : ℝ)
    (hG2 : HasDerivAt (fun u => deriv G u) g'' (Y z))
    (hY : HasDerivAt Y y' z)
    (hW2 : DifferentiableAt ℝ (fun x => deriv W x) z) :
    deriv ((fun x => (fun u => deriv G u) (Y x)) * fun x => deriv W x) z
      = g'' * y' * deriv W z + deriv G (Y z) * deriv (fun x => deriv W x) z := by
  have hcomp : HasDerivAt (fun x => (fun u => deriv G u) (Y x)) (g'' * y') z := by
    have h := hG2.comp z hY
    have hz : HasDerivAt ((fun u => deriv G u) ∘ Y) (g'' * y') z := h
    change HasDerivAt (fun x => (fun u => deriv G u) (Y x)) (g'' * y') z
    exact hz
  have hd : DifferentiableAt ℝ (fun x => (fun u => deriv G u) (Y x)) z :=
    hcomp.differentiableAt
  have hm := deriv_mul hd hW2
  have hd0 : deriv (fun x => (fun u => deriv G u) (Y x)) z = g'' * y' := hcomp.deriv
  rw [hm, hd0]

end AS145

#print axioms AS145.divergence_reduction
#print axioms AS145.lapse_acceleration
#print axioms AS145.lapse_divergence_reduction
#print axioms AS145.no_Gpp_term
#print axioms AS145.Gpp_split