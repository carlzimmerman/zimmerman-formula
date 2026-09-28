/-
AS234 (Tier-0b) Lean certificate - longitudinal moving-source response, order v^2.
Run dir: deepseek_push/astra_spawn_ideas/results/AS234/AS234-r1-20260928T195311Z-dsv4f-hermes
RESCUED (declare-rescue): the original worker executed the derivation (derive_raw.out,
116 KB of real residuals) but died before packaging; its certificate did not compile
and its claimed closed forms did not match the executed residual.

Verified from the raw output derive_raw.out (printed residual expression extracted
and reduced; NO physics re-run):
  * order-v^2 E_A consistency residual (pure-source row, no unknown coupling)
        R = -8 rho / D,   D = S_k*alpha*ell - 2*S_k*c_N*ell - 2*S_k*ell
                           - 4*alpha + 8*c_N + 24
    R is k-INDEPENDENT (the wave number cancels in every printed term) and c2-free.
  * branch point (alpha=0, c_N=1, S_k=1, ell=1, c2=1): D = 28 and
        R = -2*rho/7  != 0 for rho != 0     (raw print: "branch-eval (alpha=0): -2*rho/7")
    -> the pinned rest-isotropic configuration does NOT satisfy the moving-source
       EOMs at order v^2; the alpha2 extraction is OBSTRUCTED in this sector.
  * R = -8 rho/D never vanishes for rho != 0 and finite nonzero D: there is NO
    crossing on the pinned branch (alpha = 14/3 is a pole, D = 0).  The alpha = 8/3
    "crossing" of the original file existed only in its simplified model
    rho*(12*c2 - D)/(2*D), which is NOT the executed residual; that claim is dropped
    in the rescue (D(8/3,-1/3,1,1) = 12 is certified as algebra only).
  * density-only negative control: the printed C_M expression is nonzero
    ("fires (nonzero)? True"); with the (Psi+A)-rho*v^2 shift-matter source removed
    from the E_A residual the model gives 6*c2*rho/D -> 3*rho/14 at branch (k2 = 1),
    still nonzero: the obstruction is static, not sourced by the shift coupling.
The s0p/EA2 model below documents the worker's route with k2 kept explicit:
  EA2 = -(3 M_P2 c2 k2^2 s0p + rho)/2,   s0p = -4 rho/(M_P2 k2 Dv)
      = rho (12 c2 k2 - Dv)/(2 Dv)                          [EA2_closed]
  branch (c2=1, Dv=28): rho (3 k2 - 7)/14 ;  at k2 = 1: -2 rho/7
  density-only: EA2_dens = 6 c2 k2 rho/Dv ; branch: 3 k2 rho/14 ; k2 = 1: 3 rho/14
(The original file dropped k2 from these identities, producing the unprovable goal
k2 * rho * 56 = rho * 56 from the hypotheses k2 != 0, M_P2 * k2 * 28 != 0.)
-/
import Mathlib
open scoped BigOperators
noncomputable section

namespace AS234

/-- Static-sector denominator of the tied longitudinal system. -/
def D (alpha c_N S_k ell : ℝ) : ℝ :=
  S_k * alpha * ell - 2 * S_k * c_N * ell - 2 * S_k * ell - 4 * alpha + 8 * c_N + 24

/-- Order-v^0 solution of the (phi,psi,U) block (worker's route, k2 explicit). -/
def s0p (rho M_P2 k2 Dv : ℝ) : ℝ := -4 * rho / (M_P2 * k2 * Dv)

/-- Worker's model of the order-v^2 E_A consistency residual (k2 explicit). -/
def EA2 (rho M_P2 k2 c2 Dv : ℝ) : ℝ := -(3 * M_P2 * c2 * k2^2 * s0p rho M_P2 k2 Dv + rho) / 2

/-- Density-only variant: the -rho/2 stress source removed (no v^2 dust term). -/
def EA2_dens (rho M_P2 k2 c2 Dv : ℝ) : ℝ := -(3 * M_P2 * c2 * k2^2 * s0p rho M_P2 k2 Dv) / 2

/-- Executed residual closed form (from derive_raw.out; k- and c2-independent). -/
def resid_EA2 (rho Dv : ℝ) : ℝ := -8 * rho / Dv

/-- (1) Branch-faithful value of the denominator D. -/
theorem D_branch : D 0 1 1 1 = 28 := by
  unfold D
  norm_num

/-- (1a) Branch-faithful value of the executed residual (raw: -2*rho/7). -/
theorem resid_branch (rho : ℝ) : resid_EA2 rho (D 0 1 1 1) = -2 * rho / 7 := by
  unfold resid_EA2 D
  field_simp
  ring_nf

/-- (1b) The obstruction witness: nonzero for rho != 0 and Dv != 0. -/
theorem resid_nezero (rho Dv : ℝ) (hrho : rho ≠ 0) (hD : Dv ≠ 0) :
    resid_EA2 rho Dv ≠ 0 := by
  unfold resid_EA2
  exact mul_ne_zero (mul_ne_zero (by norm_num : (-8 : ℝ) ≠ 0) hrho) (inv_ne_zero hD)

/-- (2) Closed form of the worker's model at the exact static solution (k2 explicit). -/
theorem EA2_closed (rho M_P2 k2 c2 Dv : ℝ)
    (hP : M_P2 ≠ 0) (hk : k2 ≠ 0) (hD : Dv ≠ 0) :
    EA2 rho M_P2 k2 c2 Dv = rho * (12 * c2 * k2 - Dv) / (2 * Dv) := by
  unfold EA2 s0p
  have hA : M_P2 * k2 * Dv ≠ 0 := by positivity
  field_simp [hP, hk, hD, hA]
  ring_nf

/-- (3) Branch residual of the model: rho(3*k2-7)/14 (at k2=1 this is -2*rho/7). -/
theorem EA2_branch (rho M_P2 k2 : ℝ) (hP : M_P2 ≠ 0) (hk : k2 ≠ 0) :
    EA2 rho M_P2 k2 1 28 = rho * (3 * k2 - 7) / 14 := by
  have h := EA2_closed rho M_P2 k2 1 28 hP hk (by norm_num : (28 : ℝ) ≠ 0)
  rw [h]
  field_simp
  ring_nf

/-- (3a) k2 = 1 specialization = the executed branch value -2*rho/7. -/
theorem EA2_branch_k1 (rho M_P2 : ℝ) (hP : M_P2 ≠ 0) :
    EA2 rho M_P2 1 1 28 = -2 * rho / 7 := by
  have h := EA2_branch rho M_P2 1 hP (by norm_num : (1 : ℝ) ≠ 0)
  rw [h]
  field_simp
  ring_nf

/-- Nonzero: the consistency condition fails at branch-faithful parameters. -/
theorem resid_branch_nezero (rho : ℝ) (hrho : rho ≠ 0) : -2 * rho / 7 ≠ 0 := by
  exact mul_ne_zero (mul_ne_zero (by norm_num : (-2 : ℝ) ≠ 0) hrho)
    (inv_ne_zero (by norm_num : (7 : ℝ) ≠ 0))

/-- (4) D at the model's crossing candidate (alpha=8/3, c_N=-1/3): D = 12.
Certified as algebra only; the executed residual -8 rho/D = -2 rho/3 at this
point is still nonzero for rho != 0, so there is no branch crossing. -/
theorem D_cross_candidate : D (8 / 3 : ℝ) (-1 / 3 : ℝ) 1 1 = 12 := by
  unfold D
  norm_num

/-- (4a) On the pinned branch c_N = 1 - alpha/2 the residual stays nonzero
whenever D != 0: no crossing anywhere on the branch (alpha = 14/3 is a pole). -/
theorem pinned_no_crossing (rho alpha : ℝ) (hrho : rho ≠ 0)
    (hD : D alpha (1 - alpha / 2) 1 1 ≠ 0) :
    resid_EA2 rho (D alpha (1 - alpha / 2) 1 1) ≠ 0 := by
  exact resid_nezero rho (D alpha (1 - alpha / 2) 1 1) hrho hD

/-- (5) Density-only negative control (model): 3*k2*rho/14 at branch. -/
theorem EA2_dens_branch (rho M_P2 k2 : ℝ) (hP : M_P2 ≠ 0) (hk : k2 ≠ 0) :
    EA2_dens rho M_P2 k2 1 28 = 3 * k2 * rho / 14 := by
  unfold EA2_dens s0p
  have hA : M_P2 * k2 * 28 ≠ 0 := by positivity
  field_simp [hP, hk, hA]
  ring_nf

/-- (5a) k2 = 1 specialization: 3*rho/14. -/
theorem EA2_dens_branch_k1 (rho M_P2 : ℝ) (hP : M_P2 ≠ 0) :
    EA2_dens rho M_P2 1 1 28 = 3 * rho / 14 := by
  have h := EA2_dens_branch rho M_P2 1 hP (by norm_num : (1 : ℝ) ≠ 0)
  rw [h]
  field_simp

/-- The negative control fires: its residual is nonzero for rho != 0. -/
theorem densities_nezero (rho : ℝ) (hrho : rho ≠ 0) : (3 * rho / 14 : ℝ) ≠ 0 := by
  exact mul_ne_zero (mul_ne_zero (by norm_num : (3 : ℝ) ≠ 0) hrho)
    (inv_ne_zero (by norm_num : (14 : ℝ) ≠ 0))

end AS234